#!/usr/bin/env python3
"""Split one long VO recording into vo/VO01.wav, VO02.wav ... on silences ≥ 1.5 s.

Usage: python3 tools/split_vo.py projects/<slug>/vo/full_take.wav [--min-silence 1.5] [--db -35] [--start 1]
Read each block in VO_SCRIPT.txt order, leaving ~2 s of silence between blocks.
Check the printed count matches the number of VO blocks in the script.
"""
import re, subprocess, sys
from pathlib import Path

def arg(name, default):
    return type(default)(sys.argv[sys.argv.index(name) + 1]) if name in sys.argv else default

src = Path(sys.argv[1]).resolve(); out = src.parent
ms, db, start = arg("--min-silence", 1.5), arg("--db", -35), arg("--start", 1)
r = subprocess.run(["ffmpeg", "-i", str(src), "-af", f"silencedetect=noise={db}dB:d={ms}", "-f", "null", "-"],
                   capture_output=True, text=True).stderr
starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", r)]
ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", r)]
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(src)],
                         capture_output=True, text=True).stdout.strip())
cuts, t = [], 0.0
for s, e in zip(starts, ends + [dur] * (len(starts) - len(ends))):
    if s - t > 0.3: cuts.append((t, s))
    t = e
if dur - t > 0.3: cuts.append((t, dur))
for i, (a, b) in enumerate(cuts, start):
    o = out / f"VO{i:02d}.wav"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{max(0,a-0.15):.3f}", "-to", f"{b+0.2:.3f}",
                    "-i", str(src), "-ar", "48000", str(o)], check=True)
    print(f"{o.name}: {a:7.2f} → {b:7.2f}  ({b-a:.1f}s)")
print(f"\n{len(cuts)} blocks written. Compare with the VO block count in the script.")
