#!/usr/bin/env python3
"""Download a YouTube video's storyboard (one frame every ~2-10 s, 320x180) and save
2x(3x3) contact sheets for visual study of editing style — works even where video download is blocked.

Usage: python3 tools/fetch_storyboard.py <video_id> [out_dir=research/storyboards]
Needs: yt-dlp, pillow
"""
import email, subprocess, sys
from pathlib import Path
from PIL import Image

vid = sys.argv[1]
out = Path(sys.argv[2] if len(sys.argv) > 2 else "research/storyboards") / vid
out.mkdir(parents=True, exist_ok=True)
mh = out / f"{vid}.mhtml"
subprocess.run(["yt-dlp", "-q", "--no-progress", "-f", "sb0", "--extractor-args", "youtube:player_client=mweb",
                "-o", str(mh), f"https://www.youtube.com/watch?v={vid}"], check=True)
grids = []
for i, part in enumerate(p for p in email.message_from_bytes(mh.read_bytes()).walk() if p.get_content_type() == "image/jpeg"):
    g = out / f"grid_{i:03d}.jpg"; g.write_bytes(part.get_payload(decode=True)); grids.append(g)
for a in range(0, len(grids), 2):
    ims = [Image.open(g) for g in grids[a:a + 2]]
    sheet = Image.new("RGB", (ims[0].width, sum(i.height for i in ims)))
    y = 0
    for im in ims: sheet.paste(im, (0, y)); y += im.height
    sheet.save(out / f"sheet_{a//2:02d}.jpg", quality=85)
mh.unlink()
print(f"{len(grids)} grids -> {out} (sheet_XX.jpg = 18 frames each, in time order)")
