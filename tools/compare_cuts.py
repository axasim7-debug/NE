#!/usr/bin/env python3
"""Check that the EN and AR cuts are genuinely different productions (anti-duplicate rule).

Usage: python3 tools/compare_cuts.py projects/<slug>
Reads en/edit/edl.csv and ar/edit/edl.csv. Reports:
  - footage overlap: seconds of the same source clip time-range used in both / shorter cut's footage time
  - opening overlap: same clips in the first 90 s of both cuts
  - order similarity: how similar the sequence of clip IDs is
PASS needs overlap < 60%, opening overlap < 50%, order similarity < 70%.
"""
import csv, sys
from difflib import SequenceMatcher
from pathlib import Path

VO_WPS = 2.55  # words/sec estimate for VO rows without timing


def ts(s):
    if not s: return 0.0
    h, m, x = s.split(":"); return int(h) * 3600 + int(m) * 60 + float(x)


def load(p):
    rows = list(csv.DictReader(open(p, encoding="utf-8")))
    spans, seq, t, opening = [], [], 0.0, set()
    for r in rows:
        if r["kind"] == "CLIP":
            a, b = ts(r["in"]), ts(r["out"]); d = b - a
        elif r["kind"] == "VO" and r["clip"]:
            a = ts(r["in"]); d = len(r["text"].split()) / VO_WPS; b = a + d
        else:
            t += float(r.get("card_dur") or 0); continue
        spans.append((r["clip"], a, b)); seq.append(r["clip"])
        if t < 90: opening.add(r["clip"])
        t += d
    return spans, seq, opening


def overlap(A, B):
    tot = 0.0
    for c, a1, b1 in A:
        for c2, a2, b2 in B:
            if c == c2: tot += max(0.0, min(b1, b2) - max(a1, a2))
    return tot


def main():
    proj = Path(sys.argv[1])
    A, sa, oa = load(proj / "en/edit/edl.csv"); B, sb, ob = load(proj / "ar/edit/edl.csv")
    ta, tb = sum(b - a for _, a, b in A), sum(b - a for _, a, b in B)
    ov = overlap(A, B) / max(1e-9, min(ta, tb))
    op = len(oa & ob) / max(1, min(len(oa), len(ob)))
    order = SequenceMatcher(None, sa, sb).ratio()
    ok = ov < 0.6 and op < 0.5 and order < 0.7
    print(f"EN footage {ta/60:.1f} min · AR footage {tb/60:.1f} min")
    print(f"footage overlap   {ov:6.0%}  (need < 60%)")
    print(f"opening overlap   {op:6.0%}  (need < 50%)")
    print(f"order similarity  {order:6.0%}  (need < 70%)")
    print("PASS — distinct productions" if ok else "FAIL — too similar, re-cut the AR version")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
