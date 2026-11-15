# Packaging

## Titles (A/B/C — YouTube "Test & Compare")
- A:
- B:
- C:

Rubric: docs/05_titles_thumbnails.md (≥ 75/100). Run: `python3 tools/title_check.py "A" "B" "C"`

| | Template (T1–T7) | Auto score | Spoiler-free? | Every word true? |
|---|---|---|---|---|
| A | | | | |
| B | | | | |
| C | | | | |

## Thumbnails (3 concepts)
Rubric: docs/05_titles_thumbnails.md (≥ 75/100). Build: `python3 tools/make_thumbnail.py --video ... --at ... --out export/thumb_A.jpg`

| # | Pattern (A–G) | Source frame (C### @ time) | Face / expression | Place/evidence element | Text (0–4 words) | Arrow/circle | Blur | Score | Mobile 160×90 OK? |
|---|---|---|---|---|---|---|---|---|---|
| A | | | | | | | | | |
| B | | | | | | | | | |
| C | | | | | | | | | |

Rule: title says WHO + the SECRET; thumbnail shows the FACE + the PLACE. Never repeat the title on the image.

## Description
```
[Sponsor line + link — if any]
_______
[2-sentence case summary: crime + City, State + suspect + "captured on bodycam".]
_______
Chapters:
00:00 ...
_______
Sources & footage: [agency names]. Full source list: [link]
_______
This video was made for educational purposes only.
The video is presented to provide genuine footage of police incidents to promote transparency
in government while providing educational, informative and newsworthy content allowing viewers
to examine and assess public safety material. This is a fact-checked documentary using
authoritative sources. Corrections: [corrections page link]
```

## Tags
bodycam, police bodycam, true crime, [city], [state], [suspect name], [victim name], interrogation, 911 call, documentary

## Compliance
- [ ] First 30 s free of graphic gore
- [ ] Minors blurred / names bleeped where required
- [ ] Bodies / wounds blurred
- [ ] "Altered or synthetic content" disclosure: NO (real footage) — unless AI voice/visuals used
- [ ] Age restriction needed? ___
- [ ] Every footage asset has proof_note in assets.csv
