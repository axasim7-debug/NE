#!/usr/bin/env python3
"""Download thumbnails of the reference channel's top-N videos + labeled 2x2 contact sheets
for study (research/reference_thumbs/, git-ignored).

Usage: python3 tools/fetch_reference_thumbs.py [N=30]
"""
import csv, subprocess, sys, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
N = int(sys.argv[1]) if len(sys.argv) > 1 else 30
rows = list(csv.DictReader(open(ROOT / "research/reference_channel_videos.csv", encoding="utf-8")))
top = sorted(rows, key=lambda r: -int(r["views"] or 0))[:N]
out = ROOT / "research/reference_thumbs"; out.mkdir(exist_ok=True)
ids = []
for r in top:
    p = out / f"{r['video_id']}.jpg"
    if not p.exists():
        for q in ("maxresdefault", "hqdefault"):
            try:
                urllib.request.urlretrieve(f"https://i.ytimg.com/vi/{r['video_id']}/{q}.jpg", p); break
            except Exception: pass
    if p.exists(): ids.append(p)
with open(out / "index.md", "w", encoding="utf-8") as f:
    for i, r in enumerate(top, 1): f.write(f"{i}. {int(r['views'])/1e6:.0f}M — {r['title']} — {r['video_id']}.jpg\n")
font = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
for g in range(0, len(ids), 4):
    grp = ids[g:g + 4]; ins = sum([["-i", str(p)] for p in grp], [])
    fl = "".join(f"[{k}:v]scale=960:540,drawtext=fontfile={font}:text='#{g+k+1}':fontsize=40:fontcolor=yellow:box=1:boxcolor=black:x=10:y=10[v{k}];" for k in range(len(grp)))
    lay = "|".join(["0_0", "w0_0", "0_h0", "w0_h0"][:len(grp)])
    fl += "".join(f"[v{k}]" for k in range(len(grp))) + (f"xstack=inputs={len(grp)}:layout={lay}" if len(grp) > 1 else "null")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", *ins, "-filter_complex", fl, str(out / f"sheet_{g//4+1:02d}.jpg")])
print(f"{len(ids)} thumbnails + sheets in {out} (see index.md)")
