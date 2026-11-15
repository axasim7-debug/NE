#!/usr/bin/env python3
"""Lint a script.md against the channel style guide, and optionally export
edit/edl.csv + vo/VO_SCRIPT.txt.

Usage:
  python3 tools/script_lint.py projects/<slug>/docs/script.md [--export]
"""
import csv, re, sys
from pathlib import Path

BANNED = [
    "delve", "tapestry", "testament to", "in a world where", "it's important to note",
    "it is important to note", "stark reminder", "chilling reminder", "shrouded in mystery",
    "sent shockwaves", "send shockwaves", "navigating", "unwavering", "palpable",
    "in the realm of", "the stakes have never been higher", "fate had in store",
    "a web of", "unbeknownst to all", "little did anyone know", "plot twist",
    "buckle up", "let's dive", "dive into", "join us as", "in this video we",
    "smash that", "don't forget to subscribe",
]
INTENSIFIERS = ["disturbing", "horrifying", "chilling", "terrifying", "gruesome", "shocking"]

CLIP_RE = re.compile(r"^\[CLIP (C\d{3,})\s+(\d\d:\d\d:\d\d(?:\.\d+)?)-(\d\d:\d\d:\d\d(?:\.\d+)?)\]\s*(.*?)(?:\(vol (\d+)\))?\s*$")
VO_RE = re.compile(r"^\[VO (\d+)\]\s*(?:\(on:\s*(C\d{3,})\s+(\d\d:\d\d:\d\d(?:\.\d+)?)[^)]*\))?\s*(.*)$")
CARD_RE = re.compile(r'^\[CARD\]\s*"(.+?)"\s*(\d+(?:\.\d+)?)s')
CHAP_RE = re.compile(r"^##\s+(.+)$")
SRC_RE = re.compile(r"\s*\[S\d+(?:,\s*S\d+)*\]")


def parse(path):
    lines = Path(path).read_text(encoding="utf-8").splitlines()
    lines = [l for l in lines]
    items, i, chapter = [], 0, ""
    text = "\n".join(lines)
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    lines = text.splitlines()
    while i < len(lines):
        l = lines[i].strip()
        if m := CHAP_RE.match(l):
            chapter = m.group(1)
        elif m := CLIP_RE.match(l):
            items.append(dict(kind="CLIP", clip=m[1], tin=m[2], tout=m[3], note=m[4].strip(),
                              vol=int(m[5] or 100), chapter=chapter, line=i + 1))
        elif m := VO_RE.match(l):
            body = []
            j = i + 1
            while j < len(lines) and lines[j].strip() and not lines[j].strip().startswith("["):
                body.append(lines[j].strip()); j += 1
            items.append(dict(kind="VO", vo=f"VO{int(m[1]):02d}", clip=m[2] or "", tin=m[3] or "",
                              note=m[4].strip(), text=" ".join(body), chapter=chapter, line=i + 1))
            i = j - 1
        elif m := CARD_RE.match(l):
            items.append(dict(kind="CARD", text=m[1], dur=float(m[2]), chapter=chapter, line=i + 1))
        i += 1
    return items


def lint(items, assets_ids):
    errs, warns = [], []
    vo = [x for x in items if x["kind"] == "VO"]
    all_vo_text = " ".join(SRC_RE.sub("", x["text"]) for x in vo)
    words = len(all_vo_text.split())
    seen = set()
    for x in vo:
        t = SRC_RE.sub("", x["text"])
        n = len(t.split())
        where = f"line {x['line']} {x['vo']}"
        if x["vo"] in seen: errs.append(f"{where}: duplicate VO id")
        seen.add(x["vo"])
        if n == 0: errs.append(f"{where}: empty VO block")
        elif n > 95: errs.append(f"{where}: {n} words (max ~80) — split it and insert footage")
        elif n > 80: warns.append(f"{where}: {n} words (target 30–80)")
        # short blocks are fine when the block is a mid-sentence split (narration continues after a clip)
        if "—" in t or " - " in t: errs.append(f"{where}: em-dash / spaced hyphen — use comma or period")
        low = t.lower()
        for b in BANNED:
            if b in low: errs.append(f"{where}: banned AI phrase '{b}'")
        if low.count("?") > 1: warns.append(f"{where}: multiple rhetorical questions")
        sents = [s for s in re.split(r"(?<=[.!?])\s+", t) if s]
        if len(sents) >= 3:
            lens = [len(s.split()) for s in sents]
            if max(lens) - min(lens) < 5: warns.append(f"{where}: sentence lengths too uniform {lens}")
        if not x["clip"]: warns.append(f"{where}: no '(on: C### time)' footage under VO")
    for x in items:
        c = x.get("clip")
        if c and assets_ids is not None and c not in assets_ids:
            errs.append(f"line {x['line']}: {c} not found in research/assets.csv")
    # intensifier density: per ~450 VO words (≈3 min) max 1 each
    low = all_vo_text.lower()
    budget = max(1, words // 450)
    for w in INTENSIFIERS:
        c = len(re.findall(rf"\b{w}\b", low))
        if c > budget + 1: warns.append(f"'{w}' used {c}× (budget ≈{budget} for {words} words)")
    full = all_vo_text
    if not re.search(r"\bThis is\b", full): warns.append("no 'This is [age] [name]' hook found")
    if not re.search(r"\bIt's\b[^.]{0,60}\b(19|20)\d\d\b|\bIt's (Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday|just|approximately|around|an? )", full):
        warns.append("no \"It's [time] on [date] in [city]\" setup found")
    if not re.search(r"sentenced|pleads? guilty|convicted|acquitted|charged", full, re.I):
        warns.append("no verdict / sentence found in VO")
    return errs, warns, words


def export(items, proj):
    (proj / "edit").mkdir(exist_ok=True); (proj / "vo").mkdir(exist_ok=True)
    with open(proj / "edit" / "edl.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["seq", "kind", "clip", "in", "out", "vo_id", "text", "card_dur", "vol", "chapter", "note"])
        for k, x in enumerate(items, 1):
            w.writerow([k, x["kind"], x.get("clip", ""), x.get("tin", ""), x.get("tout", ""), x.get("vo", ""),
                        SRC_RE.sub("", x.get("text", "")), x.get("dur", ""), x.get("vol", ""),
                        x.get("chapter", ""), x.get("note", "")])
    # ONE continuous read-through: the narrator records it in a single take; tools/align_vo.py cuts it.
    with open(proj / "vo" / "VO_SCRIPT.txt", "w", encoding="utf-8") as f:
        f.write("READ STRAIGHT THROUGH IN ONE TAKE -> save as vo/full_take.wav\n"
                "Mistake? Pause 2 s and re-read the WHOLE sentence. No need to pause between paragraphs.\n")
        ch, para = None, []
        for x in items:
            if x["kind"] != "VO": continue
            if x["chapter"] != ch:
                if para: f.write(" ".join(para) + "\n"); para = []
                ch = x["chapter"]; f.write(f"\n# {ch}\n")
            para.append(SRC_RE.sub("", x["text"]))
        if para: f.write(" ".join(para) + "\n")


def main():
    if len(sys.argv) < 2: print(__doc__); sys.exit(1)
    sp = Path(sys.argv[1]).resolve()
    proj = sp.parent.parent
    ap = proj / "research" / "assets.csv"
    ids = None
    if ap.exists():
        with open(ap, encoding="utf-8") as f: ids = {r["id"] for r in csv.DictReader(f)}
    items = parse(sp)
    errs, warns, words = lint(items, ids)
    n_vo = sum(1 for x in items if x["kind"] == "VO")
    print(f"VO blocks: {n_vo} · VO words: {words} · est. VO time: {words/155:.1f} min "
          f"· est. video length (VO ≈ 1/3): {words/155*3:.0f} min")
    for e in errs: print("ERROR  ", e)
    for w in warns: print("warn   ", w)
    print(f"\n{len(errs)} error(s), {len(warns)} warning(s)")
    if "--export" in sys.argv:
        export(items, proj); print(f"exported → {proj/'edit'/'edl.csv'} and {proj/'vo'/'VO_SCRIPT.txt'}")
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    main()
