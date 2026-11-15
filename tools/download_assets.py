#!/usr/bin/env python3
"""Download every row of research/assets.csv with status=todo into footage/raw/.

Usage:  python3 tools/download_assets.py projects/<slug> [--retry-failed]

- YouTube / Facebook / X / Vimeo / news sites → yt-dlp (pip install yt-dlp)
  NOTE: YouTube blocks cloud servers. Run this on your own computer for YouTube links.
- Direct file links (.mp4 .mov .wav .mp3 .pdf .jpg .png .zip ...) → plain HTTP download.
Updates status → done/failed, local_file, sha256, downloaded_at.
"""
import csv, hashlib, shutil, subprocess, sys, urllib.request, datetime
from pathlib import Path
from urllib.parse import urlparse

DIRECT = {".mp4", ".mov", ".m4v", ".avi", ".mkv", ".wav", ".mp3", ".m4a", ".pdf", ".jpg", ".jpeg", ".png", ".zip", ".webm"}


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
    return h.hexdigest()


def main():
    if len(sys.argv) < 2: print(__doc__); sys.exit(1)
    proj = Path(sys.argv[1]).resolve(); retry = "--retry-failed" in sys.argv
    ap = proj / "research" / "assets.csv"; raw = proj / "footage" / "raw"; raw.mkdir(parents=True, exist_ok=True)
    with open(ap, encoding="utf-8") as f:
        rd = csv.DictReader(f); fields = rd.fieldnames; rows = list(rd)
    for r in rows:
        if r["status"] not in ({"todo", "failed"} if retry else {"todo"}) or not r["url"]: continue
        url, cid = r["url"].strip(), r["id"]
        ext = Path(urlparse(url).path).suffix.lower()
        print(f"→ {cid} {url}")
        try:
            if ext in DIRECT:
                out = raw / f"{cid}{ext}"
                req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req, timeout=120) as resp, open(out, "wb") as f: shutil.copyfileobj(resp, f)
            else:
                if not shutil.which("yt-dlp"): raise RuntimeError("yt-dlp not installed (pip install yt-dlp)")
                tmpl = str(raw / f"{cid}.%(ext)s")
                subprocess.run(["yt-dlp", "-f", "bv*[height<=1080]+ba/b", "--merge-output-format", "mp4",
                                "--write-info-json", "--no-playlist", "-o", tmpl, url], check=True)
                outs = [p for p in raw.glob(f"{cid}.*") if p.suffix not in (".json", ".part")]
                if not outs: raise RuntimeError("no output file")
                out = outs[0]
            r.update(status="done", local_file=str(out.relative_to(proj)), sha256=sha(out),
                     downloaded_at=datetime.datetime.now().isoformat(timespec="seconds"))
            print(f"   ✓ {out.name}")
        except Exception as e:
            r["status"] = "failed"; print(f"   ✗ {e}")
        with open(ap, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)
    print("done. Review research/assets.csv")


if __name__ == "__main__":
    main()
