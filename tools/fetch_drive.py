#!/usr/bin/env python3
"""Pull footage the user uploaded to a shared Google Drive folder into a project.

Usage: python3 tools/fetch_drive.py projects/<slug> "<google drive folder link>"
The folder must be shared as "Anyone with the link". Files land in footage/raw/ and
assets.csv rows are marked done when a file named <C###>.* is found.
Needs: pip install gdown
"""
import csv, subprocess, sys
from pathlib import Path

proj, link = Path(sys.argv[1]).resolve(), sys.argv[2]
raw = proj / "footage" / "raw"; raw.mkdir(parents=True, exist_ok=True)
subprocess.run(["gdown", "--folder", link, "-O", str(raw), "--remaining-ok"], check=False)
for p in list(raw.rglob("*")):           # flatten sub-folders
    if p.is_file() and p.parent != raw: p.rename(raw / p.name)
ap = proj / "research" / "assets.csv"
rows = list(csv.DictReader(open(ap, encoding="utf-8"))); fields = list(rows[0].keys())
for r in rows:
    hits = [p for p in raw.glob(f"{r['id']}.*") if p.suffix not in (".json", ".part")]
    if hits: r.update(status="done", local_file=str(hits[0].relative_to(proj)))
with open(ap, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)
print(sum(r["status"] == "done" for r in rows), "assets present")
