#!/usr/bin/env python3
"""Draw the world-news infographic for Friday 20 November 2026.

1024x1024 PNG, four stories in a 2x2 grid under a dated header.
No network, no randomness, no timestamps, so repeated runs write
identical bytes.
"""

import hashlib
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = "entry.png"

PAGE = (13, 24, 40)
PANEL = (24, 40, 63)
EDGE = (56, 82, 114)
WHITE = (243, 245, 248)
SOFT = (178, 191, 206)
GOLD = (233, 185, 76)
TEAL = (64, 178, 164)
GREEN = (110, 190, 96)
RED = (214, 90, 74)
PURPLE = (158, 124, 206)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def load(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_TITLE = load("DejaVuSerif-Bold.ttf", 64)
F_DATE = load("DejaVuSans-Bold.ttf", 30)
F_TAG = load("DejaVuSans-Bold.ttf", 22)
F_HEAD = load("DejaVuSans-Bold.ttf", 31)
F_BODY = load("DejaVuSans.ttf", 22)
F_FOOT = load("DejaVuSans.ttf", 20)


def wrap(draw, text, font, max_w):
    """Greedy word wrap; returns lines that fit max_w pixels."""
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


STORIES = [
    {
        "tag": "CYCLONE",
        "color": TEAL,
        "head": "Cyclone Akvan Hits India's East Coast",
        "body": "Landfall in Odisha on Friday afternoon. Over 120,000 people "
                "evacuated, 300 rescue teams deployed and 60 trains cancelled.",
    },
    {
        "tag": "CLIMATE",
        "color": GREEN,
        "head": "COP31 Ends Without Fossil-Fuel Pledge",
        "body": "The near-final text drops the fossil-fuel transition, "
                "drawing outrage from climate campaigners.",
    },
    {
        "tag": "GAZA",
        "color": RED,
        "head": "Israel Launches Ground Operation in Gaza",
        "body": "A renewed military escalation as Israeli forces enter "
                "Hamas-controlled central Gaza.",
    },
    {
        "tag": "RIYADH",
        "color": PURPLE,
        "head": "Houthi Strike Hits Riyadh's Tallest Tower",
        "body": "The tower houses the headquarters of the Saudi sovereign "
                "wealth fund (PIF).",
    },
]


def draw_panel(draw, x, y, pw, ph, story):
    draw.rounded_rectangle([x, y, x + pw, y + ph], radius=18,
                           fill=PANEL, outline=EDGE, width=2)
    # accent bar across the top, rounded top corners only
    draw.rounded_rectangle([x, y, x + pw, y + 14], radius=8,
                           fill=story["color"])
    draw.rectangle([x, y + 7, x + pw, y + 14], fill=story["color"])
    tx = x + 26
    ty = y + 32
    draw.text((tx, ty), story["tag"], font=F_TAG, fill=story["color"])
    hy = ty + 40
    for line in wrap(draw, story["head"], F_HEAD, pw - 52):
        draw.text((tx, hy), line, font=F_HEAD, fill=WHITE)
        hy += 40
    by = hy + 16
    for line in wrap(draw, story["body"], F_BODY, pw - 52):
        draw.text((tx, by), line, font=F_BODY, fill=SOFT)
        by += 30


def build():
    img = Image.new("RGB", (W, H), PAGE)
    draw = ImageDraw.Draw(img)
    title = "WORLD NEWS"
    tw = draw.textlength(title, font=F_TITLE)
    draw.text(((W - tw) / 2, 24), title, font=F_TITLE, fill=WHITE)
    date = "FRIDAY 20 NOVEMBER 2026"
    dw = draw.textlength(date, font=F_DATE)
    draw.text(((W - dw) / 2, 94), date, font=F_DATE, fill=GOLD)
    draw.line([(28, 138), (W - 28, 138)], fill=GOLD, width=3)
    gx, gy, gap = 28, 156, 20
    pw = (W - 2 * gx - gap) // 2
    ph = 372
    for i, story in enumerate(STORIES):
        px = gx + (i % 2) * (pw + gap)
        py = gy + (i // 2) * (ph + gap)
        draw_panel(draw, px, py, pw, ph, story)
    foot = "Sources: major wire and newspaper roundups, 20 Nov 2026"
    fw = draw.textlength(foot, font=F_FOOT)
    draw.text(((W - fw) / 2, 960), foot, font=F_FOOT, fill=SOFT)
    img.save(OUT, format="PNG")


def verify_output():
    """Check the PNG exists, is small enough, and is exactly 1024x1024."""
    assert os.path.exists(OUT), "entry.png missing"
    size = os.path.getsize(OUT)
    assert size <= 1024 * 1024, f"entry.png too big: {size} bytes"
    with Image.open(OUT) as im:
        assert im.size == (1024, 1024), f"wrong size: {im.size}"
        assert im.format == "PNG"
    return size


def describe():
    size = verify_output()
    digest = hashlib.sha256(open(OUT, "rb").read()).hexdigest()
    print(f"entry.png: {size} bytes, sha256 {digest}")
    print("Four stories: Cyclone Akvan landfall; COP31 fossil-fuel text "
          "dropped; Israel ground operation in Gaza; Houthi strike on "
          "Riyadh tower.")
    print("Dated FRIDAY 20 NOVEMBER 2026.")


if __name__ == "__main__":
    build()
    describe()
