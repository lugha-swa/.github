#!/usr/bin/env python3
"""Tengeneza mabango (banners) ya README za lugha-swa: SVG -> PNG, mwanga na giza.

Rangi na fonti ni zile zile za tovuti (lugha-swa.github.io/style.css).
GitHub haipakii fonti za wavuti ndani ya picha za README, kwa hiyo
mabango hutolewa kama PNG zilizochorwa tayari.

Matumizi: FONTCONFIG_FILE=... python3 tengeneza_mabango.py <saraka-ya-pato>
"""
import os
import subprocess
import sys
from html import escape

MANDHARI = {
    "mwanga": dict(bg="#FAF7EF", bg_alt="#F2ECDF", ink="#1F1810", muted="#6B5E4A",
                   accent="#A34E14", rule="#E4DBC6"),
    "giza": dict(bg="#16110A", bg_alt="#1D1710", ink="#F2EAD8", muted="#A79A88",
                 accent="#E3A04B", rule="#33291B"),
}

# jina la faili -> (kichwa, maelezo, mstari wa sahihi)
MABANGO = {
    "lugha-swa": ("lugha-swa",
                  "Programu za mifumo, kwa Kiswahili.",
                  "swa  ·  kawira  ·  uchapaji-swa  ·  tree-sitter-swa"),
    "swa": ("Swa",
            "Lugha ya kupanga ya Kiswahili inayojikusanya yenyewe.",
            "kwanza  →  mbegu  →  stage1  →  stage2 == stage3"),
    "kawira": ("Kawira",
               "Swa kwenye ring 0. Kernel iliyoandikwa kwa Swa.",
               "multiboot  →  long mode  →  kernel_main()  →  IDT + kibodi"),
    "uchapaji-swa": ("uchapaji-swa",
                     "Fonti za TrueType na kijazaji cha glyph, kwa Swa safi.",
                     "glyf  →  mikunjo  →  mistari  →  pikseli"),
    "tree-sitter-swa": ("tree-sitter-swa",
                        "Sarufi ya Tree-sitter kwa lugha ya Swa.",
                        "chanzo.swa  →  mti wa sintaksia  →  rangi kwenye kihariri"),
}

UPANA, UREFU = 1600, 520


def nembo(x, y, ukubwa, rangi):
    """Nembo ya tovuti (lango lenye nyota tisa), imepanuliwa kutoka 48x48."""
    s = ukubwa / 48.0
    nyota = []
    for (cx, cy) in [(14, 15), (24, 15), (34, 15), (14, 25), (24, 25), (34, 25),
                     (14, 35), (24, 35), (34, 35)]:
        r = 4 if (cx, cy) == (24, 25) else 3
        nyota.append(
            f'<g transform="translate({cx} {cy})">'
            f'<rect x="{-r}" y="{-r}" width="{2*r}" height="{2*r}"/>'
            f'<rect x="{-r}" y="{-r}" width="{2*r}" height="{2*r}" transform="rotate(45)"/></g>')
    return (f'<g transform="translate({x} {y}) scale({s})">'
            f'<path d="M6 42 V22 A18 18 0 0 1 42 22 V42 Z" fill="none" stroke="{rangi}" stroke-width="2.4"/>'
            f'<g fill="{rangi}">{"".join(nyota)}</g></g>')


def bango(kichwa, maelezo, sahihi, m):
    kushoto = 120
    nembo_ukubwa = 240
    maandishi_x = kushoto + nembo_ukubwa + 90
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{UPANA}" height="{UREFU}" viewBox="0 0 {UPANA} {UREFU}">
  <rect width="100%" height="100%" fill="{m["bg"]}"/>
  {nembo(kushoto, (UREFU - nembo_ukubwa) / 2 - 10, nembo_ukubwa, m["accent"])}
  <text x="{maandishi_x}" y="250" font-family="Fraunces" font-weight="600" font-size="128"
        fill="{m["ink"]}" letter-spacing="-2">{escape(kichwa)}</text>
  <text x="{maandishi_x + 4}" y="316" font-family="IBM Plex Sans" font-weight="400" font-size="36"
        fill="{m["muted"]}">{escape(maelezo)}</text>
  <line x1="{maandishi_x + 4}" y1="362" x2="{UPANA - 120}" y2="362" stroke="{m["rule"]}" stroke-width="2"/>
  <text x="{maandishi_x + 4}" y="410" font-family="IBM Plex Mono" font-weight="500" font-size="26"
        fill="{m["accent"]}">{escape(sahihi)}</text>
</svg>
'''


def main():
    pato = sys.argv[1] if len(sys.argv) > 1 else "mabango"
    os.makedirs(pato, exist_ok=True)
    for jina, (kichwa, maelezo, sahihi) in MABANGO.items():
        for mandhari, m in MANDHARI.items():
            svg = os.path.join(pato, f"{jina}-{mandhari}.svg")
            png = os.path.join(pato, f"{jina}-{mandhari}.png")
            with open(svg, "w") as f:
                f.write(bango(kichwa, maelezo, sahihi, m))
            subprocess.run(["rsvg-convert", "-w", str(UPANA), "-o", png, svg], check=True)
            os.remove(svg)
            print(png)


if __name__ == "__main__":
    main()
