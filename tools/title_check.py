#!/usr/bin/env python3
"""Approximate the title rubric from docs/05_titles_thumbnails.md (out of 100; target ≥ 75).
The 'not a spoiler' and 'truthful' items (20 pts) need a human: they are assumed OK and flagged.

Usage: python3 tools/title_check.py "Mother Realizes Her Son Is Hiding A Body In The Attic" ["title 2" ...]
"""
import re, sys

TEMPLATES = {
    "T1 Realization": r"\bRealiz(e|es|ed)\b",
    "T2 Discovery": r"\bDiscover(s|ed)?\b",
    "T3 Capture": r"^How (Police|Cops|Detectives|Deputies) (Captured|Caught|Hunted Down|Tracked Down)",
    "T4 Arrogance": r"\bThinks? (S?he|They) Can Get Away\b",
    "T5 Leads": r"\bLeads? (Police|Cops|Officers|Detectives) (To|Into)\b",
    "T6 Place": r"\b(Find|Finds|Found|Runs Into)\b.*\b(In|Inside)\b",
    "T7 Camera": r"\b(Caught On Camera|Being Recorded|Everything Was Filmed|Hidden Camera)\b",
}
RELATIONS = r"\b(Mom|Mother|Dad|Father|Son|Daughters?|Parents|Family|Wife|Husband|Girlfriend|Boyfriend|Brother|Sister|Twin|Grandma|Grandpa|Grandmother|Grandfather|Couple|Roommates?|Teacher|Student|Neighbor)('s)?\b"
ADJ_KILLER = r"\b(Rich|Secret|Smartest|Spoiled|College|Psycho|Teen|Mass|Serial|Wanted|Genius|Clueless|Killer)\b"
PLACES = r"\b(Garage|Attic|Vents?|Backyard|Bedroom|Shed|River|Trash Can|Garbage Bag|Car|Trunk|Mansion|House|Basement|Freezer|Suitcase|Closet|Woods|Forest|Hideout|Motel)\b"
NUMBERS = r"(\$[\d,]+|\b\d+\b|\bYears? Later\b)"
ACTION = r"\b(Realiz\w*|Discover\w*|Finds?|Found|Learn\w*|Leads?|Runs Into|Catch\w*|Captured)\b"
WEAK = r"\b(Arrested|Shocking|Insane|Crazy|Unbelievable|You Won't Believe|Gone Wrong)\b"


def score(t):
    pts, notes = 0, []
    tpl = [k for k, r in TEMPLATES.items() if re.search(r, t, re.I)]
    if tpl: pts += 15
    else: notes.append("no T1–T7 template matched")
    hits = bool(re.search(RELATIONS, t, re.I)) or bool(re.search(ADJ_KILLER, t, re.I))
    pts += 15 if hits else 0
    if not hits: notes.append("add a family relation or a strong killer adjective")
    hook = bool(re.search(PLACES, t, re.I)) or bool(re.search(NUMBERS, t))
    pts += 15 if hook else 0
    if not hook: notes.append("add an ordinary place, a number or a time span")
    act = bool(re.search(ACTION, t, re.I)); pts += 15 if act else 0
    if not act: notes.append("add a realization/discovery verb")
    words, chars = len(t.split()), len(t)
    title_case = all(w[0].isupper() or not w[0].isalpha() for w in t.split())
    fmt = 6 <= words <= 11 and chars <= 60 and title_case
    pts += 10 if fmt else 0
    if not fmt: notes.append(f"format: {words} words / {chars} chars / title-case={title_case} (want 6–11, ≤60, True)")
    if any(ord(c) > 127 and c not in "’'$" for c in t): notes.append("non-ASCII look-alike characters: remove"); weak = True
    else: weak = bool(re.search(WEAK, t, re.I))
    pts += 0 if weak else 10
    if weak: notes.append("weak/clickbait word or look-alike characters")
    pts += 20; notes.append("CHECK BY HAND: no spoiler of the verdict + every word true (20 pts assumed)")
    return pts, tpl, notes


def main():
    if len(sys.argv) < 2: print(__doc__); sys.exit(1)
    for t in sys.argv[1:]:
        p, tpl, notes = score(t)
        print(f"\n[{p:3d}/100] {'PASS' if p >= 75 else 'FAIL'}  {t}\n         templates: {', '.join(tpl) or '-'}")
        for n in notes: print("         -", n)


if __name__ == "__main__":
    main()
