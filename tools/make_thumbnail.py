#!/usr/bin/env python3
"""Build a channel-style thumbnail: real frame + enhancement + our camera HUD + optional text/arrow/circle/blur.

Usage examples:
  # grab a frame from a video at 00:14:41 and build thumbnail A
  python3 tools/make_thumbnail.py --video projects/<p>/footage/raw/C002.mp4 --at 00:14:41 \
      --out projects/<p>/export/thumb_A.jpg

  # from an image, with text + arrow + blur box + red circle
  python3 tools/make_thumbnail.py --image frame.png --out thumb_B.jpg \
      --small "we found the" --big "BODIES." --text-pos 0.55,0.25 \
      --arrow 0.52,0.30:0.40,0.45 --circle 0.80,0.80,0.08 --blur 0.30,0.55,0.50,0.85 \
      --stamp "MAY 20 2023 17:47"

Coordinates are fractions of width/height (0..1). Outputs <out> (1280x720) and <out>_mobile.png (160x90 check).
Needs: pip install pillow ; ffmpeg for --video.
"""
import argparse, subprocess, tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

W, H = 1280, 720
FONTS_BOLD = ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
              "C:/Windows/Fonts/arialbd.ttf", "/Library/Fonts/Arial Bold.ttf"]
FONTS_MONO = ["/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", "/System/Library/Fonts/Menlo.ttc",
              "C:/Windows/Fonts/consolab.ttf"]


def font(cands, size):
    for p in cands:
        if Path(p).exists(): return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def fxy(s):
    return [float(v) for v in s.split(",")]


def grab(video, at):
    tmp = Path(tempfile.mkdtemp()) / "f.png"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", at, "-i", video, "-frames:v", "1", str(tmp)], check=True)
    return Image.open(tmp)


def cover(img):
    img = img.convert("RGB"); r = max(W / img.width, H / img.height)
    img = img.resize((round(img.width * r), round(img.height * r)), Image.LANCZOS)
    x, y = (img.width - W) // 2, (img.height - H) // 2
    return img.crop((x, y, x + W, y + H))


def enhance(img, strength=1.0):
    img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=int(120 * strength), threshold=2))
    img = ImageEnhance.Contrast(img).enhance(1 + 0.18 * strength)
    img = ImageEnhance.Color(img).enhance(1 + 0.35 * strength)
    img = ImageEnhance.Brightness(img).enhance(1 + 0.04 * strength)
    return img


def blur_box(img, box):
    x0, y0, x1, y1 = [int(v * (W if i % 2 == 0 else H)) for i, v in enumerate(box)]
    region = img.crop((x0, y0, x1, y1))
    small = region.resize((max(1, (x1 - x0) // 18), max(1, (y1 - y0) // 18)), Image.NEAREST)
    img.paste(small.resize(region.size, Image.NEAREST), (x0, y0))


def hud(img, stamp, cam):
    """Our own HUD (distinct from the reference channel): amber accents, mono font, 'CAM' label, date stamp."""
    d = ImageDraw.Draw(img, "RGBA")
    m, L, t = 36, 70, 5                      # margin, corner length, line thickness
    white = (255, 255, 255, 235)
    for (x, y, dx, dy) in [(m, m, 1, 1), (W - m, m, -1, 1), (m, H - m, 1, -1), (W - m, H - m, -1, -1)]:
        d.line([(x, y), (x + dx * L, y)], fill=white, width=t)
        d.line([(x, y), (x, y + dy * L)], fill=white, width=t)
    mono = font(FONTS_MONO, 30)
    # REC
    d.ellipse((m + 26, m + 24, m + 50, m + 48), fill=(230, 30, 30, 255))
    d.text((m + 60, m + 20), "REC", font=mono, fill=white)
    # battery (top-right)
    bx, by = W - m - 110, m + 22
    d.rectangle((bx, by, bx + 70, by + 30), outline=white, width=3)
    d.rectangle((bx + 70, by + 9, bx + 76, by + 21), fill=white)
    d.rectangle((bx + 6, by + 6, bx + 30, by + 24), fill=(255, 190, 40, 255))   # low-ish battery, amber
    # cam label (bottom-right) + stamp (bottom-left)
    small = font(FONTS_MONO, 26)
    d.text((W - m - 150, H - m - 52), cam, font=small, fill=white)
    if stamp: d.text((m + 26, H - m - 52), stamp, font=small, fill=white)


def outlined_text(d, xy, text, f, fill=(255, 255, 255, 255)):
    x, y = xy
    for dx, dy in [(-3, 3), (3, 3), (0, 5), (4, 6)]:
        d.text((x + dx, y + dy), text, font=f, fill=(0, 0, 0, 170))
    d.text((x, y), text, font=f, fill=fill)


def main():
    ap = argparse.ArgumentParser()
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--image"); src.add_argument("--video")
    ap.add_argument("--at", default="00:00:01")
    ap.add_argument("--out", required=True)
    ap.add_argument("--small", default=""); ap.add_argument("--big", default="")
    ap.add_argument("--text-pos", default="0.05,0.30", help="x,y of the text block")
    ap.add_argument("--arrow", action="append", default=[], help="x1,y1:x2,y2 (tail:head)")
    ap.add_argument("--circle", action="append", default=[], help="cx,cy,r (r as fraction of width)")
    ap.add_argument("--blur", action="append", default=[], help="x0,y0,x1,y1 pixelate box")
    ap.add_argument("--stamp", default=""); ap.add_argument("--cam", default="CAM 02")
    ap.add_argument("--enhance", type=float, default=1.0)
    ap.add_argument("--no-hud", action="store_true")
    a = ap.parse_args()

    img = cover(Image.open(a.image) if a.image else grab(a.video, a.at))
    img = enhance(img, a.enhance)
    for b in a.blur: blur_box(img, fxy(b))
    d = ImageDraw.Draw(img, "RGBA")
    for c in a.circle:
        cx, cy, r = fxy(c); cx, cy, r = cx * W, cy * H, r * W
        d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=(235, 25, 25, 255), width=9)
    for ar in a.arrow:
        (x1, y1), (x2, y2) = [fxy(p) for p in ar.split(":")]
        x1, y1, x2, y2 = x1 * W, y1 * H, x2 * W, y2 * H
        d.line([(x1, y1), (x2, y2)], fill=(255, 255, 255, 255), width=9)
        import math
        ang = math.atan2(y2 - y1, x2 - x1)
        for s in (2.6, -2.6):
            d.line([(x2, y2), (x2 + 38 * math.cos(ang + s), y2 + 38 * math.sin(ang + s))], fill=(255, 255, 255, 255), width=9)
    if a.small or a.big:
        tx, ty = fxy(a.text_pos); tx, ty = tx * W, ty * H
        fs, fb = font(FONTS_BOLD, 64), font(FONTS_BOLD, 128)
        if a.small: outlined_text(d, (tx, ty), a.small, fs); ty += 72
        if a.big: outlined_text(d, (tx, ty), a.big, fb)
    if not a.no_hud: hud(img, a.stamp, a.cam)

    out = Path(a.out); out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, quality=92)
    img.resize((160, 90), Image.LANCZOS).resize((480, 270), Image.NEAREST).save(out.with_name(out.stem + "_mobile.png"))
    print(f"saved {out} (+ {out.stem}_mobile.png for the 160x90 readability check)")


if __name__ == "__main__":
    main()
