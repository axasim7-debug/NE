#!/usr/bin/env python3
"""Build an automatic rough cut from edit/edl.csv + footage + recorded VO.

Usage:
  python3 tools/assemble.py projects/<slug> [--duck 0.12] [--preview]

Inputs:
  research/assets.csv     id → local_file (else footage/raw/<id>.*)
  edit/edl.csv            from: tools/script_lint.py docs/script.md --export
  vo/VO##.wav|mp3|m4a     one file per VO block

Outputs:
  export/rough_cut.mp4    1920x1080 30fps, AAC 48k
  export/captions.srt     narration subtitles
  export/chapters.txt     YouTube chapters from ## headings
  edit/segments/          intermediate renders (safe to delete)
"""
import csv, json, re, subprocess, sys, shutil
from pathlib import Path

W, H, FPS = 1920, 1080, 30
FONT = next((p for p in ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                         "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
                         "C:/Windows/Fonts/arialbd.ttf"] if Path(p).exists()), None)
VENC = ["-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", "-r", str(FPS)]
AENC = ["-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2"]
SCALE = f"scale={W}:{H}:force_original_aspect_ratio=decrease,pad={W}:{H}:(ow-iw)/2:(oh-ih)/2,setsar=1,fps={FPS}"


def ts(s):
    if not s: return 0.0
    h, m, sec = s.split(":"); return int(h) * 3600 + int(m) * 60 + float(sec)


def srt_t(t):
    ms = int(round(t * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: sys.exit(f"ffmpeg failed:\n{' '.join(cmd)}\n{r.stderr[-1500:]}")


def probe(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration:stream=codec_type",
                        "-of", "json", str(p)], capture_output=True, text=True)
    j = json.loads(r.stdout or "{}")
    return float(j.get("format", {}).get("duration", 0)), any(s.get("codec_type") == "audio" for s in j.get("streams", []))


def find_clip(proj, cid, assets):
    lf = assets.get(cid, "")
    if lf and (proj / lf).exists(): return proj / lf
    hits = sorted((proj / "footage" / "raw").glob(f"{cid}.*")) + sorted((proj / "footage" / "raw").glob(f"{cid}_*"))
    return hits[0] if hits else None


def find_vo(proj, vid):
    for ext in ("wav", "mp3", "m4a", "flac", "aac"):
        p = proj / "vo" / f"{vid}.{ext}"
        if p.exists(): return p
    return None


def seg_clip(src, tin, dur, vol, out):
    _, has_a = probe(src)
    cmd = ["ffmpeg", "-y", "-ss", str(tin), "-t", str(dur), "-i", str(src)]
    if not has_a: cmd += ["-f", "lavfi", "-t", str(dur), "-i", "anullsrc=r=48000:cl=stereo"]
    af = f"volume={vol/100:.2f},aresample=48000,aformat=channel_layouts=stereo"
    cmd += ["-vf", SCALE, "-af", af, "-map", "0:v:0", "-map", "0:a:0" if has_a else "1:a:0",
            *VENC, *AENC, "-shortest", str(out)]
    run(cmd)


def seg_vo(src, tin, vo, duck, out, hold=0.35):
    dur, _ = probe(vo)
    dur += hold  # footage keeps running after the narration stops (pacing)
    if src is None:
        cmd = ["ffmpeg", "-y", "-f", "lavfi", "-t", str(dur), "-i", f"color=c=black:s={W}x{H}:r={FPS}",
               "-i", str(vo), "-filter_complex",
               "[1:a]aresample=48000,aformat=channel_layouts=stereo,apad[a]",
               "-map", "0:v", "-map", "[a]", "-t", str(dur), *VENC, *AENC, str(out)]
    else:
        sdur, has_a = probe(src)
        cmd = ["ffmpeg", "-y", "-ss", str(tin), "-t", str(dur)]
        # loop short sources so B-roll covers the whole VO
        if sdur - tin < dur: cmd = ["ffmpeg", "-y", "-stream_loop", "-1", "-ss", str(tin), "-t", str(dur)]
        cmd += ["-i", str(src), "-i", str(vo)]
        if has_a:
            fc = (f"[0:v]{SCALE}[v];[0:a]aresample=48000,aformat=channel_layouts=stereo,volume={duck}[bg];"
                  f"[1:a]aresample=48000,aformat=channel_layouts=stereo,apad[n];"
                  f"[bg][n]amix=inputs=2:duration=first:normalize=0[a]")
        else:
            fc = f"[0:v]{SCALE}[v];[1:a]aresample=48000,aformat=channel_layouts=stereo,apad[a]"
        cmd += ["-filter_complex", fc, "-map", "[v]", "-map", "[a]", "-t", str(dur), *VENC, *AENC, str(out)]
    run(cmd)
    return dur


def seg_card(text, dur, out):
    safe = text.replace("\\", "\\\\").replace(":", "\\:").replace("'", "\u2019")
    font = f"fontfile='{FONT}':" if FONT else ""
    vf = (f"drawtext={font}text='{safe}':fontcolor=white:fontsize=64:x=(w-text_w)/2:y=(h-text_h)/2:"
          f"alpha='if(lt(t,0.5),t/0.5,if(gt(t,{dur}-0.5),({dur}-t)/0.5,1))'")
    run(["ffmpeg", "-y", "-f", "lavfi", "-t", str(dur), "-i", f"color=c=black:s={W}x{H}:r={FPS}",
         "-f", "lavfi", "-t", str(dur), "-i", "anullsrc=r=48000:cl=stereo",
         "-vf", vf, *VENC, *AENC, "-shortest", str(out)])


def chunk_caption(text, start, dur, max_chars=84):
    words, chunks, cur = text.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > max_chars and cur: chunks.append(cur); cur = w
        else: cur = f"{cur} {w}".strip()
    if cur: chunks.append(cur)
    total = sum(len(c) for c in chunks) or 1
    t, out = start, []
    for c in chunks:
        d = dur * len(c) / total
        mid = len(c) // 2
        sp = c.find(" ", mid) if len(c) > 42 else -1
        out.append((t, t + d, c if sp < 0 else c[:sp] + "\n" + c[sp + 1:])); t += d
    return out


def main():
    if len(sys.argv) < 2: print(__doc__); sys.exit(1)
    proj = Path(sys.argv[1]).resolve()
    duck = float(sys.argv[sys.argv.index("--duck") + 1]) if "--duck" in sys.argv else 0.12
    assets = {}
    ap = proj / "research" / "assets.csv"
    if ap.exists():
        with open(ap, encoding="utf-8") as f: assets = {r["id"]: r.get("local_file", "") for r in csv.DictReader(f)}
    with open(proj / "edit" / "edl.csv", encoding="utf-8") as f: rows = list(csv.DictReader(f))
    segdir = proj / "edit" / "segments"; shutil.rmtree(segdir, ignore_errors=True); segdir.mkdir(parents=True)
    (proj / "export").mkdir(exist_ok=True)
    segs, caps, chapters, t, last_ch, missing = [], [], [], 0.0, None, []
    for r in rows:
        k, out = r["kind"], segdir / f"{int(r['seq']):04d}.mp4"
        if r["chapter"] and r["chapter"] != last_ch:
            last_ch = r["chapter"]; chapters.append((t, re.sub(r"^[①-⑨]\s*", "", last_ch).title()))
        if k == "CLIP":
            src = find_clip(proj, r["clip"], assets)
            if not src: missing.append(r["clip"]); continue
            dur = ts(r["out"]) - ts(r["in"])
            seg_clip(src, ts(r["in"]), dur, int(r["vol"] or 100), out)
        elif k == "VO":
            vo = find_vo(proj, r["vo_id"])
            if not vo: missing.append(r["vo_id"]); continue
            src = find_clip(proj, r["clip"], assets) if r["clip"] else None
            if r["clip"] and not src: missing.append(r["clip"])
            m = re.search(r"hold=([\d.]+)", r.get("note", ""))
            hold = float(m.group(1)) if m else 0.35
            dur = seg_vo(src, ts(r["in"]), vo, duck, out, hold)
            caps += chunk_caption(r["text"], t, dur - hold)
        elif k == "CARD":
            dur = float(r["card_dur"] or 4); seg_card(r["text"], dur, out)
        else: continue
        segs.append(out); t += probe(out)[0]
        print(f"  {r['seq']:>4} {k:<4} {r.get('clip') or r.get('vo_id') or ''} → {t/60:6.2f} min", flush=True)
    if not segs: sys.exit("nothing to render")
    lst = segdir / "list.txt"
    lst.write_text("".join(f"file '{s.name}'\n" for s in segs))
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(proj / "export" / "rough_cut.mp4")])
    with open(proj / "export" / "captions.srt", "w", encoding="utf-8") as f:
        for i, (a, b, c) in enumerate(caps, 1): f.write(f"{i}\n{srt_t(a)} --> {srt_t(b)}\n{c}\n\n")
    with open(proj / "export" / "chapters.txt", "w", encoding="utf-8") as f:
        for a, name in chapters: f.write(f"{int(a//60):02d}:{int(a%60):02d} {name}\n")
    print(f"\nrough cut: {proj/'export'/'rough_cut.mp4'}  ({t/60:.1f} min)")
    if missing: print("MISSING (skipped):", ", ".join(sorted(set(missing))))


if __name__ == "__main__":
    main()
