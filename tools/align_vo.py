#!/usr/bin/env python3
"""Cut ONE continuous voice-over take into the script's VO blocks — anywhere, even mid-sentence.

The narrator reads vo/VO_SCRIPT.txt straight through in one file (no pauses needed).
This tool transcribes the take with word timestamps, aligns it to the script text,
and writes vo/VO01.wav, VO02.wav ... exactly at the block boundaries defined in edit/edl.csv.

Usage:
  python3 tools/align_vo.py projects/<slug> [--take vo/full_take.wav] [--model small.en]

Needs: pip install faster-whisper ; ffmpeg
Outputs: vo/VO##.wav, vo/alignment.json, and a report of weak matches / unmatched audio
(retakes, ad-libs, mistakes) for review.
"""
import csv, json, re, subprocess, sys
from difflib import SequenceMatcher
from pathlib import Path

NUM = {"0": "zero", "1": "one", "2": "two", "3": "three", "4": "four", "5": "five", "6": "six",
       "7": "seven", "8": "eight", "9": "nine", "10": "ten", "11": "eleven", "12": "twelve"}


def norm(w):
    w = w.lower().replace("’", "'")
    w = re.sub(r"[^a-z0-9']", "", w)
    return NUM.get(w, w)


def arg(name, default):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else default


def main():
    if len(sys.argv) < 2: print(__doc__); sys.exit(1)
    proj = Path(sys.argv[1]).resolve()
    take = proj / arg("--take", "vo/full_take.wav")
    if not take.exists():
        cands = [p for p in (proj / "vo").glob("*") if p.suffix.lower() in (".wav", ".mp3", ".m4a", ".flac") and not re.match(r"VO\d+", p.stem)]
        if len(cands) != 1: sys.exit(f"take not found: {take} (put your single recording in vo/)")
        take = cands[0]
    rows = [r for r in csv.DictReader(open(proj / "edit" / "edl.csv", encoding="utf-8")) if r["kind"] == "VO"]
    if not rows: sys.exit("no VO rows in edit/edl.csv — run script_lint.py --export first")

    # script words, tagged with their block
    s_words, s_block = [], []
    for bi, r in enumerate(rows):
        for w in re.split(r"[\s\-–]+", r["text"]):
            n = norm(w)
            if n: s_words.append(n); s_block.append(bi)

    from faster_whisper import WhisperModel
    model = WhisperModel(arg("--model", "small.en"), device="cpu", compute_type="int8")
    prompt = " ".join(r["text"] for r in rows)[:800]
    import numpy as np  # decode with ffmpeg ourselves (avoids PyAV version issues)
    pcm = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", str(take), "-f", "s16le", "-ac", "1", "-ar", "16000", "-"],
                         capture_output=True, check=True).stdout
    audio = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768.0
    segs, _ = model.transcribe(audio, word_timestamps=True, initial_prompt=prompt, vad_filter=False, beam_size=5,
                              condition_on_previous_text=False)
    a_words = []
    for sg in segs:
        for w in sg.words:
            parts = [norm(x) for x in re.split(r"[\-–]+", w.word) if norm(x)]
            step = (w.end - w.start) / max(1, len(parts))
            for k, x in enumerate(parts): a_words.append((x, w.start + k * step, w.start + (k + 1) * step))
    print(f"take: {take.name} · {len(a_words)} words heard · {len(s_words)} words in script")

    sm = SequenceMatcher(None, s_words, [w for w, _, _ in a_words], autojunk=False)
    s2a = {}
    for blk in sm.get_matching_blocks():
        for k in range(blk.size): s2a[blk.a + k] = blk.b + k

    def unmatched_runs():
        used, runs, run = set(s2a.values()), [], []
        for k in range(len(a_words)):
            if k not in used: run.append(k)
            else:
                if run: runs.append(run)
                run = []
        if run: runs.append(run)
        return runs

    # RETAKES: if an unmatched stretch ENDS with the same words the script just matched before it,
    # the narrator re-read that part -> the LAST take wins (remap those words onto the retake).
    for _ in range(3):
        changed = False
        for R in unmatched_runs():
            prev = sorted(i for i, x in s2a.items() if x < R[0])
            for k in range(min(len(R), len(prev)), 1, -1):
                if [s_words[i] for i in prev[-k:]] == [a_words[x][0] for x in R[-k:]]:
                    for i, x in zip(prev[-k:], R[-k:]): s2a[i] = x
                    changed = True; break
        if not changed: break

    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(take)],
                               capture_output=True, text=True).stdout.strip())
    # each block = matched words, split into pieces wherever unused audio (mistakes/ad-libs) sits in between
    blocks = []
    for bi, r in enumerate(rows):
        idx = [i for i, b in enumerate(s_block) if b == bi]
        hits = sorted(s2a[i] for i in idx if i in s2a)
        miss = [i for i in idx if i not in s2a]
        ratio = len(hits) / max(1, len(idx))
        if not hits: blocks.append(None); continue
        pieces, cur = [], [hits[0], hits[0]]
        for h in hits[1:]:
            gap = a_words[h][1] - a_words[cur[1]][2]
            extra_audio = h - cur[1] - 1
            # only cut out audio that the script can't explain (a mistake/ad-lib), never a misheard word
            if extra_audio >= 3 and extra_audio > 3 * len(miss) + 2 and gap > 0.6: pieces.append(cur); cur = [h, h]
            else: cur[1] = h
        pieces.append(cur)
        blocks.append(([[a_words[p0][1], a_words[p1][2]] for p0, p1 in pieces], ratio))

    report = []
    flat = [(bi, pc) for bi, bl in enumerate(blocks) if bl for pc in bl[0]]
    for bi, (r, bl) in enumerate(zip(rows, blocks)):
        if bl is None: print(f"  ✗ {r['vo_id']}: no match"); report.append({"vo": r["vo_id"], "status": "missing"}); continue
        pieces, ratio = bl
        cut = []
        for pc in pieces:
            k = flat.index((bi, pc))
            prev_end = flat[k - 1][1][1] if k else 0.0
            next_st = flat[k + 1][1][0] if k + 1 < len(flat) else dur
            a = max(prev_end + (pc[0] - prev_end) / 2, pc[0] - 0.25, 0)
            b = min(pc[1] + (next_st - pc[1]) / 2, pc[1] + 0.30)
            cut.append((a, b))
        out = proj / "vo" / f"{r['vo_id']}.wav"
        parts = []
        for j, (a, b) in enumerate(cut):
            fade = min(0.04, (b - a) / 4)
            parts.append(f"[0:a]atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS,afade=t=in:d={fade:.3f},"
                         f"afade=t=out:st={b-a-fade:.3f}:d={fade:.3f}[p{j}]")
        fc = ";".join(parts) + ";" + "".join(f"[p{j}]" for j in range(len(cut))) + f"concat=n={len(cut)}:v=0:a=1[o]"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(take), "-filter_complex", fc, "-map", "[o]",
                        "-ar", "48000", "-ac", "1", str(out)], check=True)
        tot = sum(b - a for a, b in cut)
        flag = "" if ratio >= 0.85 else "  ⚠ check (low match — misread?)"
        joined = f"  [{len(cut)} pieces joined, mistake removed]" if len(cut) > 1 else ""
        print(f"  {r['vo_id']}: {cut[0][0]:8.2f} → {cut[-1][1]:8.2f}  ({tot:5.1f}s)  match {ratio:.0%}{joined}{flag}")
        report.append({"vo": r["vo_id"], "pieces": [[round(a, 3), round(b, 3)] for a, b in cut], "match": round(ratio, 3)})
    matched_a = set(s2a.values())

    # unmatched audio stretches (retakes / ad-libs) longer than 3 words
    extra, run = [], []
    for k, (w, s, e) in enumerate(a_words):
        if k not in matched_a: run.append((w, s, e))
        else:
            if len(run) > 3: extra.append(run)
            run = []
    if len(run) > 3: extra.append(run)
    extra = [x for x in extra if x[-1][2] - x[0][1] > 0.12 * len(x)]  # drop decoder hallucinations
    for x in extra:
        print(f"  ℹ unmatched audio {x[0][1]:.1f}s–{x[-1][2]:.1f}s: \"{' '.join(w for w, _, _ in x)[:90]}\" (retake? not used)")
    json.dump({"take": take.name, "blocks": report,
               "unmatched": [{"start": x[0][1], "end": x[-1][2], "text": " ".join(w for w, _, _ in x)} for x in extra]},
              open(proj / "vo" / "alignment.json", "w"), indent=1)
    print("written: vo/VO##.wav + vo/alignment.json")


if __name__ == "__main__":
    main()
