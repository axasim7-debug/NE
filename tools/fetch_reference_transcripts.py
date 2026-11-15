#!/usr/bin/env python3
"""Pull reference transcripts of Dr Insanity videos (public pages on forensicfiles.com)
for style study / competitor check. Output → research/reference_transcripts/ (git-ignored).

Usage: python3 tools/fetch_reference_transcripts.py [N=40]
Picks the N most-viewed + 12 newest titles from research/reference_channel_videos.csv.
"""
import csv, html, re, sys, time, unicodedata, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
N = int(sys.argv[1]) if len(sys.argv) > 1 else 40
rows = list(csv.DictReader(open(ROOT / "research/reference_channel_videos.csv", encoding="utf-8")))
pick, seen = [], set()
for r in rows[:12] + sorted(rows, key=lambda r: -int(r["views"] or 0))[:N]:
    if r["video_id"] not in seen: seen.add(r["video_id"]); pick.append(r)
out = ROOT / "research/reference_transcripts"; out.mkdir(exist_ok=True)

def slug(t):
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")

ok = 0
for r in pick:
    dest = out / f"{r['video_id']}.txt"
    if dest.exists(): ok += 1; continue
    try:
        req = urllib.request.Request("https://forensicfiles.com/episodes/" + slug(r["title"]), headers={"User-Agent": "Mozilla/5.0"})
        page = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "ignore")
    except Exception as e:
        print("miss", r["title"], e); continue
    m = re.search(r">Transcript<(.*)", page, re.S)
    if not m: print("no transcript", r["title"]); continue
    body = re.sub(r"<script.*?</script>|<style.*?</style>", "", m.group(1), flags=re.S)
    body = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", body)))
    body = re.sub(r" Show more Tension.*", "", body)
    dest.write_text(f"TITLE: {r['title']}\nVIEWS: {r['views']}\nDUR_MIN: {r['duration_min']}\nTRANSCRIPT:\n{body}\n", encoding="utf-8")
    ok += 1; time.sleep(1)
print(f"{ok}/{len(pick)} transcripts in {out}")
