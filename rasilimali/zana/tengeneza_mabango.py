#!/usr/bin/env python3
"""Tengeneza mabango ya README na nembo za lugha-swa: SVG -> PNG, mwanga na giza.

Muundo unatoka kwenye sanaa mbili maarufu zaidi za Waswahili:

- Nembo ni mlango wa kuchonga wa Zanzibar/Lamu: tao la feni juu ya
  kizingiti, nguzo ya katikati, na vifundo (studs) vya shaba.
- Bango ni kanga: pindo (mpaka) wa mnyororo -- mchoro wa fremu za
  milango hiyo hiyo, na pia mnyororo wetu wa kujikusanya -- katikati
  (mji), na jina: methali iliyochapishwa kwa kila hazina.

Rangi na fonti (Fraunces, IBM Plex) ni zile zile za tovuti. GitHub
haipakii fonti za wavuti ndani ya picha za README, kwa hiyo mabango
hutolewa kama PNG zilizochorwa tayari; pembe ni za mviringo na nje
yake ni wazi (transparent).

Matumizi: FONTCONFIG_FILE=... python3 tengeneza_mabango.py <saraka-ya-rasilimali>
"""
import math
import os
import subprocess
import sys
from html import escape

MANDHARI = {
    "mwanga": dict(bg="#FAF7EF", ink="#1F1810", muted="#6B5E4A", accent="#A34E14",
                   rule="#E4DBC6", soft="#EFE5D3"),
    "giza": dict(bg="#16110A", ink="#F2EAD8", muted="#A79A88", accent="#E3A04B",
                 rule="#33291B", soft="#251C12"),
}

# jina la faili -> (kichwa, maelezo, mstari wa sahihi, methali)
MABANGO = {
    "lugha-swa": ("lugha-swa",
                  "Programu za mifumo, kwa Kiswahili.",
                  "swa  ·  kawira  ·  uchapaji-swa  ·  tree-sitter-swa",
                  "Penye nia pana njia"),
    "swa": ("Swa",
            "Lugha ya kupanga ya Kiswahili inayojikusanya yenyewe.",
            "kwanza  →  mbegu  →  stage1  →  stage2 == stage3",
            "Haba na haba hujaza kibaba"),
    "kawira": ("Kawira",
               "Swa kwenye ring 0. Kernel iliyoandikwa kwa Swa.",
               "multiboot  →  long mode  →  kernel_main()  →  IDT + kibodi",
               "Mwenda pole hajikwai"),
    "uchapaji-swa": ("uchapaji-swa",
                     "Fonti za TrueType na kijazaji cha glyph, kwa Swa safi.",
                     "glyf  →  mikunjo  →  mistari  →  pikseli",
                     "Haraka haraka haina baraka"),
    "tree-sitter-swa": ("tree-sitter-swa",
                        "Sarufi ya Tree-sitter kwa lugha ya Swa.",
                        "chanzo.swa  →  mti wa sintaksia  →  rangi kwenye kihariri",
                        "Ukiona vyaelea, vimeundwa"),
}

UPANA, UREFU, PEMBE = 1600, 520, 40


# ---------------------------------------------------------------- nembo

def mlango(c):
    """Nembo kamili (100x100): feni, kizingiti, nguzo, vifundo sita."""
    o = [f'<path d="M18 92 V50 A32 32 0 0 1 82 50 V92 Z" fill="none" stroke="{c}" stroke-width="5" stroke-linejoin="round"/>',
         f'<line x1="20" y1="50" x2="80" y2="50" stroke="{c}" stroke-width="4" stroke-linecap="round"/>',
         f'<line x1="50" y1="50" x2="50" y2="90" stroke="{c}" stroke-width="4" stroke-linecap="round"/>']
    for k in range(1, 8):
        a = math.pi + k * math.pi / 8
        o.append(f'<line x1="{50 + 9 * math.cos(a):.1f}" y1="{50 + 9 * math.sin(a):.1f}" '
                 f'x2="{50 + 25 * math.cos(a):.1f}" y2="{50 + 25 * math.sin(a):.1f}" '
                 f'stroke="{c}" stroke-width="3.2" stroke-linecap="round"/>')
    o.append(f'<path d="M43 50 A7 7 0 0 1 57 50 Z" fill="{c}"/>')
    for x in (34, 66):
        for y in (62, 73, 84):
            o.append(f'<circle cx="{x}" cy="{y}" r="3.2" fill="{c}"/>')
    return "".join(o)


def mlango_mdogo(c):
    """Kibadala cha ukubwa mdogo (favicon): feni na nguzo tu, mistari minene."""
    o = [f'<path d="M14 92 V52 A36 36 0 0 1 86 52 V92 Z" fill="none" stroke="{c}" stroke-width="8" stroke-linejoin="round"/>',
         f'<line x1="50" y1="52" x2="50" y2="90" stroke="{c}" stroke-width="8" stroke-linecap="round"/>',
         f'<line x1="18" y1="52" x2="82" y2="52" stroke="{c}" stroke-width="7" stroke-linecap="round"/>']
    for k in (1, 2, 3, 4, 5):
        a = math.pi + k * math.pi / 6
        o.append(f'<line x1="50" y1="52" x2="{50 + 26 * math.cos(a):.1f}" y2="{52 + 26 * math.sin(a):.1f}" '
                 f'stroke="{c}" stroke-width="6" stroke-linecap="round"/>')
    return "".join(o)


def nyota8(cx, cy, r, rangi):
    """Nyota ya pembe nane ya michoro ya pwani (pembe za pindo)."""
    s = r * 0.72
    return (f'<g transform="translate({cx} {cy})" fill="{rangi}">'
            f'<rect x="{-s}" y="{-s}" width="{2 * s}" height="{2 * s}" rx="{s * 0.12}"/>'
            f'<rect x="{-s}" y="{-s}" width="{2 * s}" height="{2 * s}" rx="{s * 0.12}" transform="rotate(45)"/></g>')


# ---------------------------------------------------------------- bango

def mnyororo(x1, x2, y, c):
    """Viungo vya mnyororo vinavyopishana (wazi / imara) kando ya mstari."""
    o, step, rx, ry = [], 34, 18, 7.5
    n = int((x2 - x1) // step)
    start = x1 + ((x2 - x1) - n * step) / 2 + step / 2
    for i in range(n):
        cx = start + i * step
        if i % 2 == 0:
            o.append(f'<ellipse cx="{cx:.1f}" cy="{y}" rx="{rx}" ry="{ry}" fill="none" stroke="{c}" stroke-width="3.4"/>')
        else:
            o.append(f'<ellipse cx="{cx:.1f}" cy="{y}" rx="{rx * 0.62:.1f}" ry="{ry * 0.42:.1f}" fill="{c}"/>')
    return "".join(o)


def bango(kichwa, maelezo, sahihi, methali, m):
    ndani, ukanda = 22, 46
    juu, chini = ndani + ukanda, UREFU - ndani - ukanda      # mipaka ya "mji" (katikati)
    # Kizuizi cha maandishi: kichwa (urefu wa herufi ~92), maelezo,
    # sahihi, na kisanduku cha methali -- kimewekwa katikati wima.
    kizuizi = 300
    y0 = juu + (chini - juu - kizuizi) / 2
    xt = 470
    nembo_ukubwa = 220
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{UPANA}" height="{UREFU}" viewBox="0 0 {UPANA} {UREFU}">',
         f'<defs><clipPath id="pembe"><rect width="{UPANA}" height="{UREFU}" rx="{PEMBE}"/></clipPath></defs>',
         f'<g clip-path="url(#pembe)">',
         f'<rect width="{UPANA}" height="{UREFU}" fill="{m["bg"]}"/>',
         f'<rect x="{ndani}" y="{ndani}" width="{UPANA - 2 * ndani}" height="{UREFU - 2 * ndani}" '
         f'rx="{PEMBE - ndani + 6}" fill="none" stroke="{m["rule"]}" stroke-width="2"/>',
         mnyororo(ndani + 60, UPANA - ndani - 60, ndani + ukanda / 2, m["accent"]),
         mnyororo(ndani + 60, UPANA - ndani - 60, UREFU - ndani - ukanda / 2, m["accent"])]
    for cx in (ndani + 34, UPANA - ndani - 34):
        for cy in (ndani + ukanda / 2, UREFU - ndani - ukanda / 2):
            o.append(nyota8(cx, cy, 12, m["accent"]))
    o.append(f'<g transform="translate(150 {y0 + (kizuizi - nembo_ukubwa) / 2 - 6}) scale({nembo_ukubwa / 100})">'
             f'{mlango(m["accent"])}</g>')
    o.append(f'<text x="{xt}" y="{y0 + 92}" font-family="Fraunces" font-weight="600" font-size="122" '
             f'fill="{m["ink"]}" letter-spacing="-2">{escape(kichwa)}</text>')
    o.append(f'<text x="{xt + 4}" y="{y0 + 152}" font-family="IBM Plex Sans" font-size="34" '
             f'fill="{m["muted"]}">{escape(maelezo)}</text>')
    o.append(f'<text x="{xt + 4}" y="{y0 + 204}" font-family="IBM Plex Mono" font-weight="500" font-size="25" '
             f'fill="{m["accent"]}">{escape(sahihi)}</text>')
    upana_jina = UPANA - xt - 120
    o.append(f'<rect x="{xt}" y="{y0 + 244}" width="{upana_jina}" height="52" rx="26" fill="{m["soft"]}"/>')
    o.append(f'<text x="{xt + upana_jina / 2}" y="{y0 + 279}" text-anchor="middle" font-family="Fraunces" '
             f'font-weight="500" font-style="italic" font-size="27" letter-spacing="3" '
             f'fill="{m["ink"]}">{escape(methali)}</text>')
    o.append('</g></svg>\n')
    return "".join(o)


def chora(svg_maandishi, png, upana=None, urefu=None):
    tmp = png + ".svg"
    with open(tmp, "w") as f:
        f.write(svg_maandishi)
    cmd = ["rsvg-convert", "-o", png]
    if upana:
        cmd += ["-w", str(upana)]
    if urefu:
        cmd += ["-h", str(urefu)]
    subprocess.run(cmd + [tmp], check=True)
    os.remove(tmp)


def main():
    msingi = sys.argv[1] if len(sys.argv) > 1 else "rasilimali"
    mabango = os.path.join(msingi, "mabango")
    nembo = os.path.join(msingi, "nembo")
    os.makedirs(mabango, exist_ok=True)
    os.makedirs(nembo, exist_ok=True)

    for jina, (kichwa, maelezo, sahihi, methali) in MABANGO.items():
        for mandhari, m in MANDHARI.items():
            png = os.path.join(mabango, f"{jina}-{mandhari}.png")
            chora(bango(kichwa, maelezo, sahihi, methali, m), png, upana=UPANA)
            print(png)

    # Nembo: SVG za currentColor (kwa tovuti), na PNG za rangi ya chapa.
    kati = "#B8652A"  # inasomeka juu ya mandharinyuma ya mwanga na giza
    for faili, fn in (("nembo", mlango), ("nembo-ndogo", mlango_mdogo)):
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" role="img" '
               f'aria-label="Nembo ya Swa: mlango wa kuchonga">{fn("currentColor")}</svg>\n')
        with open(os.path.join(nembo, f"{faili}.svg"), "w") as f:
            f.write(svg)
        for z in (64, 256):
            chora(svg.replace("currentColor", kati), os.path.join(nembo, f"{faili}-{z}.png"), z, z)
            print(os.path.join(nembo, f"{faili}-{z}.png"))


if __name__ == "__main__":
    main()
