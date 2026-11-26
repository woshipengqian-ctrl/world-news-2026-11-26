#!/usr/bin/env python3
"""Draw the 26 November 2026 world-news front page (1024x1024 PNG).

Run once, locally, to produce news.png. The submitted entry (main.py)
only copies that committed PNG; this generator is not part of the run.
All six stories were verified against news reports dated 26 Nov 2026.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 229)
INK = (20, 20, 20)
RED = (164, 31, 31)
GREY = (90, 86, 76)
SKY = (214, 228, 238)
BLUE = (38, 70, 110)
SAND = (228, 222, 206)
ORANGE = (226, 110, 30)

FDIR = "/usr/share/fonts/truetype/dejavu"
SERIF_B = os.path.join(FDIR, "DejaVuSerif-Bold.ttf")
SERIF = os.path.join(FDIR, "DejaVuSerif.ttf")
SANS = os.path.join(FDIR, "DejaVuSans.ttf")
SANS_B = os.path.join(FDIR, "DejaVuSans-Bold.ttf")


def fnt(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, font, width):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=font) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def story(d, x, y, width, kicker, head, deck, hsize=30, dsize=17):
    fk = fnt(SANS_B, 15)
    fh = fnt(SERIF_B, hsize)
    fd = fnt(SANS, dsize)
    d.text((x, y), kicker, font=fk, fill=RED)
    y += 22
    for line in wrap(d, head, fh, width):
        d.text((x, y), line, font=fh, fill=INK)
        y += hsize + 4
    y += 4
    for line in wrap(d, deck, fd, width):
        d.text((x, y), line, font=fd, fill=(60, 58, 50))
        y += dsize + 5
    return y


def hrule(d, x0, y, x1, w=2):
    d.line([(x0, y), (x1, y)], fill=INK, width=w)


def star(d, cx, cy, r, fill):
    pts = []
    for i in range(10):
        ang = -90 + i * 36
        rr = r if i % 2 == 0 else r * 0.42
        import math
        pts.append((cx + rr * math.cos(math.radians(ang)),
                    cy + rr * math.sin(math.radians(ang))))
    d.polygon(pts, fill=fill)


# --- pictograms -------------------------------------------------------
def icon_missile(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    # atom orbits
    cx, cy = x + 88, y + 108
    d.ellipse([cx - 52, cy - 18, cx + 52, cy + 18], outline=BLUE, width=4)
    d.ellipse([cx - 18, cy - 52, cx + 18, cy + 52], outline=BLUE, width=4)
    d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=RED)
    # missile rising, right side
    mx = x + 250
    d.polygon([(mx, y + 24), (mx + 26, y + 58), (mx, y + 150),
               (mx - 26, y + 58)], fill=(52, 58, 66))
    d.rectangle([mx - 34, y + 120, mx - 18, y + 150], fill=(52, 58, 66))
    d.rectangle([mx + 18, y + 120, mx + 34, y + 150], fill=(52, 58, 66))
    d.polygon([(mx - 10, y + 150), (mx, y + 196), (mx + 10, y + 150)],
              fill=ORANGE)
    d.ellipse([mx - 16, y + 188, mx + 16, y + 212], fill=(240, 200, 120))
    star(d, x + w - 40, y + h - 36, 15, RED)


def icon_tariff(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SAND)
    # rising bars
    bars = [40, 56, 48, 72, 62, 84]
    bw, gap = 16, 6
    bx = x + 14
    for i, bh in enumerate(bars):
        d.rectangle([bx + i * (bw + gap), y + h - 22 - bh,
                     bx + i * (bw + gap) + bw, y + h - 22],
                    fill=(52, 58, 66))
    d.line([(x + 10, y + 42), (x + w - 12, y + 32)], fill=RED, width=4)
    d.text((x + 14, y + 8), "%", font=fnt(SERIF_B, 30), fill=RED)


def icon_tanker(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    for i, wy in enumerate((y + h - 40, y + h - 24, y + h - 10)):
        d.arc([x + 8 + i * 6, wy, x + w - 8, wy + 24], start=180, end=360,
              fill=BLUE, width=4)
    # tanker hull
    d.polygon([(x + 18, y + h - 58), (x + 132, y + h - 58),
               (x + 118, y + h - 30), (x + 32, y + h - 30)],
              fill=(52, 58, 66))
    d.rectangle([x + 30, y + h - 88, x + 120, y + h - 58], fill=(120, 40, 40))
    d.rectangle([x + 96, y + h - 106, x + 112, y + h - 88], fill=(52, 58, 66))
    # explosion burst over the deck
    bx, by = x + 78, y + 52
    d.polygon([(bx, by - 30), (bx + 12, by - 10), (bx + 32, by - 18),
               (bx + 20, by + 2), (bx + 34, by + 12), (bx + 12, by + 16),
               (bx + 8, by + 34), (bx - 6, by + 14), (bx - 28, by + 18),
               (bx - 16, by - 2), (bx - 32, by - 8), (bx - 12, by - 12)],
              fill=ORANGE)
    d.ellipse([bx - 10, by - 12, bx + 10, by + 8], fill=(240, 200, 120))
    # smoke
    d.ellipse([x + 116, y + 14, x + 142, y + 40], fill=(150, 148, 142))
    d.ellipse([x + 130, y + 4, x + 152, y + 26], fill=(170, 168, 162))


def icon_chart(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SAND)
    # falling line
    pts = [(x + 12, y + 30), (x + 42, y + 44), (x + 66, y + 38),
           (x + 92, y + 78), (x + 118, y + 104), (x + 138, y + 128)]
    d.line(pts, fill=RED, width=5)
    d.polygon([(x + 138, y + 128), (x + 138, y + 112), (x + 122, y + 128)],
              fill=RED)
    d.polygon([(x + 138, y + 128), (x + 122, y + 128), (x + 138, y + 144)],
              fill=RED)
    # dashed grid
    for gy in (y + 44, y + 84, y + 124):
        for gx in range(x + 12, x + w - 10, 12):
            d.line([(gx, gy), (gx + 6, gy)], fill=(190, 184, 168), width=2)
    d.text((x + 12, y + h - 34), "-4%", font=fnt(SERIF_B, 30), fill=RED)


def icon_balloon(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    d.ellipse([x + 10, y + 14, x + 74, y + 42], fill=(255, 255, 255))
    d.ellipse([x + 96, y + 108, x + 146, y + 130], fill=(255, 255, 255))
    # big balloon
    cx, cy = x + 82, y + 62
    d.ellipse([cx - 46, cy - 40, cx + 46, cy + 40], fill=(214, 84, 60))
    d.ellipse([cx - 46, cy - 40, cx - 10, cy + 40], fill=(226, 110, 30))
    d.polygon([(cx - 14, cy + 38), (cx + 14, cy + 38), (cx, cy + 50)],
              fill=(120, 40, 40))
    d.line([(cx - 10, cy + 50), (cx - 10, cy + 96)], fill=INK, width=2)
    d.line([(cx + 10, cy + 50), (cx + 10, cy + 96)], fill=INK, width=2)
    d.line([(cx, cy + 50), (cx, cy + 96)], fill=INK, width=2)
    d.rectangle([cx - 18, cy + 96, cx + 18, cy + 112], fill=(120, 90, 60))
    # rain streaks
    for rx in (x + 118, x + 132, x + 146):
        d.line([(rx, y + 18), (rx - 6, y + 44)], fill=BLUE, width=3)


def icon_flame(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SAND)
    cx = x + w // 2
    # flame
    d.polygon([(cx, y + 8), (cx + 30, y + 44), (cx + 20, y + 54),
               (cx + 34, y + 80), (cx + 10, y + 102), (cx - 30, y + 102),
               (cx - 34, y + 80), (cx - 20, y + 54), (cx - 26, y + 42)],
              fill=ORANGE)
    d.polygon([(cx, y + 48), (cx + 16, y + 72), (cx + 7, y + 80),
               (cx + 14, y + 98), (cx - 14, y + 98), (cx - 7, y + 80),
               (cx - 16, y + 72)], fill=(240, 200, 60))
    # charred cars, clear of the flame
    d.rectangle([x + 10, y + h - 26, x + 52, y + h - 10], fill=(52, 58, 66))
    d.rectangle([x + 98, y + h - 26, x + 140, y + h - 10], fill=(70, 76, 84))


# --- page ----------------------------------------------------------------
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 36

    # masthead
    d.text((W // 2, 30), "THE WORLD TODAY", font=fnt(SERIF_B, 66),
           fill=INK, anchor="ma")
    hrule(d, M, 116, W - M, 3)
    d.text((W // 2, 126), "THURSDAY  \u00b7  26 NOVEMBER 2026",
           font=fnt(SANS_B, 24), fill=INK, anchor="ma")
    d.text((W // 2, 156), "ONE DAY  \u00b7  SIX STORIES  \u00b7  THE WORLD IN A PAGE",
           font=fnt(SANS, 15), fill=GREY, anchor="ma")
    hrule(d, M, 184, W - M, 2)

    # lead story: North Korea
    ly = 202
    icon_missile(d, W - M - 360, ly + 6, 360, 216)
    story(d, M, ly, 560, "NORTH KOREA",
          "Kim orders wider nuclear rollout",
          "Kim Jong Un inspects nuclear plants and says Pyongyang "
          "should deploy tactical nuclear weapons across multiple "
          "domains \u2014 its status as a nuclear state \u201cabsolutely "
          "inviolable\u201d.",
          hsize=40, dsize=19)
    hrule(d, M, 440, W - M, 2)

    # 2x2 grid
    grid = [
        ("UNITED STATES", "Trump fires new tariff salvo",
         "New levies proposed on 14 trading partners, China facing "
         "20%, after an eight-month probe into excess capacity.",
         icon_tariff),
        ("MIDDLE EAST", "Tankers hit mines in Hormuz",
         "Iran says tankers struck naval mines and caught fire in "
         "the Strait \u2014 a third, an LNG carrier, ablaze by night.",
         icon_tanker),
        ("MARKETS", "Nasdaq plunges 4% in AI rout",
         "Tech stocks tumble as doubts over AI spending returns "
         "deepen; Nvidia falls 9% intraday before paring losses.",
         icon_chart),
        ("UNITED STATES", "Parade postponed, first time ever",
         "Macy\u2019s Thanksgiving Day Parade moves to Saturday as a "
         "nor\u2019easter bears down \u2014 the first weather delay in "
         "100 years.",
         icon_balloon),
    ]
    gx, gy = M, 462
    cw, ch = (W - 2 * M - 24) // 2, 178
    for i, (kick, head, deck, icon) in enumerate(grid):
        x = gx + (i % 2) * (cw + 24)
        y = gy + (i // 2) * (ch + 14)
        icon(d, x, y, 150, 150)
        story(d, x + 164, y + 2, cw - 164, kick, head, deck,
              hsize=23, dsize=15)
        if i % 2 == 0:
            d.line([(x + cw + 12, y + 4), (x + cw + 12, y + ch - 8)],
                   fill=(190, 184, 168), width=1)
    hrule(d, M, 850, W - M, 2)

    # bottom strip: Cairo fire
    by = 868
    icon_flame(d, M, by, 150, 116)
    story(d, M + 164, by + 2, W - 2 * M - 164, "EGYPT",
          "31 killed in Cairo tanker fire",
          "A fuel tanker overturns on the capital\u2019s Ring Road and "
          "bursts into flames, engulfing dozens of cars; 21 hurt.",
          hsize=26, dsize=16)
    hrule(d, M, 998, W - M, 2)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "news.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
