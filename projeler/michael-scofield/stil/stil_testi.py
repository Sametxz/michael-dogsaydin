"""F3 stil testi: aynı an, üç görsel dil.
An: "Sırtındaki harita duvara akıyor." Michael hücrede duvara dönük (sırt kameraya, yüz yok),
özgün dövmedeki plan çizgileri tenden kalkıp duvarda bir kaçış haritasına dönüşür.
Çıktı: stil_A/B/C.png (960x540) + stil_kontakt.png. Kullanım: python3 stil_testi.py
"""
import math, random, subprocess
from pathlib import Path

P = Path(__file__).resolve().parent
W, H = 960, 540

STIL = {
    # A · Mavi plan: dünya çizgiden kurulur, Michael'ın zihni gibi
    "A": dict(ad="Mavi plan (blueprint)", bg0="#0B1F33", bg1="#071422", wall="#0E2840", wall_line="#3E7FB0",
              ink="#BFE6FF", skin="none", skin_line="#BFE6FF", hair="none", tat="#7FC8F0", glow="#9FF0FF",
              bar="#2C6A99", bar_fill="none", light="#7FD8FF", lw=1.6, fills=False, grid=True, halftone=False),
    # B · Sinematik 2D: dolu renk, kalın kontur, yönlü ışık; plan ışığı yalnız efekt
    "B": dict(ad="Sinematik 2D", bg0="#2A3540", bg1="#141A20", wall="#5A6670", wall_line="#3A444C",
              ink="#15110E", skin="#D8A887", skin_line="#15110E", hair="#2A221C", tat="#2E3A48", glow="#7FE6FF",
              bar="#22282E", bar_fill="#3A434B", light="#FFD9A0", lw=4.0, fills=True, grid=False, halftone=False),
    # C · Grafik roman / noir: siyah, kemik beyazı, tek turuncu vurgu, tram
    "C": dict(ad="Grafik roman (noir)", bg0="#E8DFCC", bg1="#CFC3AA", wall="#E2D8C2", wall_line="#1A1612",
              ink="#100D0A", skin="#E8DFCC", skin_line="#100D0A", hair="#100D0A", tat="#100D0A", glow="#FF7A1E",
              bar="#100D0A", bar_fill="#100D0A", light="#FFF4DE", lw=3.4, fills=True, grid=False, halftone=True),
}

def defs(s):
    d = ['<defs>',
         f'<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{s["bg0"]}"/><stop offset="1" stop-color="{s["bg1"]}"/></linearGradient>',
         f'<radialGradient id="lamp" cx="0.82" cy="0.35" r="0.6"><stop offset="0" stop-color="{s["light"]}" stop-opacity="0.55"/><stop offset="1" stop-color="{s["light"]}" stop-opacity="0"/></radialGradient>',
         f'<radialGradient id="skinsh" cx="0.75" cy="0.25" r="0.9"><stop offset="0" stop-color="#F0C4A0"/><stop offset="0.55" stop-color="{s["skin"] if s["skin"]!="none" else "#000"}"/><stop offset="1" stop-color="#8A5E48"/></radialGradient>',
         '<filter id="glow" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="3.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>',
         '<filter id="soft"><feGaussianBlur stdDeviation="6"/></filter>',
         '<filter id="beton" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="4" seed="3" result="n"/>'
         '<feDiffuseLighting in="n" lighting-color="#ffffff" surfaceScale="2.2" result="l"><feDistantLight azimuth="210" elevation="58"/></feDiffuseLighting>'
         '<feBlend in="SourceGraphic" in2="l" mode="multiply" result="m"/><feComposite in="m" in2="SourceGraphic" operator="in"/></filter>',
         '<pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M24,0 H0 V24" fill="none" stroke="#2D5F86" stroke-width="0.6" opacity="0.5"/></pattern>',
         '<pattern id="tram" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(35)"><circle cx="3.5" cy="3.5" r="1.5" fill="#100D0A"/></pattern>',
         '<pattern id="tram2" width="5" height="5" patternUnits="userSpaceOnUse" patternTransform="rotate(35)"><circle cx="2.5" cy="2.5" r="1.0" fill="#100D0A"/></pattern>',
         '<clipPath id="back"><path d="M282,560 L288,430 Q284,352 334,322 Q398,300 448,266 L512,266 Q562,300 626,322 Q676,352 672,430 L678,560 Z"/></clipPath>',
         '</defs>']
    return "".join(d)

def oda(s):
    o = [f'<rect width="{W}" height="{H}" fill="url(#bg)"/>']
    # duvar blokları (Michael'ın baktığı duvar)
    wall = f'<rect x="60" y="20" width="700" height="430" fill="{s["wall"]}" {"filter=\"url(#beton)\"" if s["fills"] and not s["halftone"] else ""}/>'
    o.append(wall)
    if s["grid"]: o.append('<rect x="60" y="20" width="700" height="430" fill="url(#grid)"/>')
    for r_ in range(9):
        y = 20 + r_ * 48; off = 0 if r_ % 2 else 50
        o.append(f'<path d="M60,{y} H760" stroke="{s["wall_line"]}" stroke-width="{1.2 if not s["fills"] else 2}" opacity="0.8"/>')
        for c in range(8):
            x = 60 + off + c * 100
            if 60 < x < 760: o.append(f'<path d="M{x},{y} v48" stroke="{s["wall_line"]}" stroke-width="{1.2 if not s["fills"] else 2}" opacity="0.8"/>')
    # ranza (solda) ve lavabo
    o.append(f'<rect x="20" y="300" width="230" height="22" rx="3" fill="{s["bar_fill"] if s["fills"] else "none"}" stroke="{s["ink"]}" stroke-width="{s["lw"]*0.8}"/>'
             f'<rect x="28" y="282" width="214" height="20" rx="8" fill="{"#8A8F86" if s["fills"] and not s["halftone"] else ("url(#tram2)" if s["halftone"] else "none")}" stroke="{s["ink"]}" stroke-width="{s["lw"]*0.8}"/>'
             f'<path d="M30,322 V540 M240,322 V540" stroke="{s["ink"]}" stroke-width="{s["lw"]*1.4}"/>')
    o.append(f'<path d="M30,120 H246 M30,120 V300 M240,120 V300" stroke="{s["ink"]}" stroke-width="{s["lw"]*1.1}" fill="none" opacity="0.85"/>'
             f'<rect x="28" y="104" width="214" height="18" rx="7" fill="{"#7A7F76" if s["fills"] and not s["halftone"] else "none"}" stroke="{s["ink"]}" stroke-width="{s["lw"]*0.8}"/>')
    # sağda parmaklıklar + koridor ışığı
    o.append(f'<rect x="760" y="0" width="200" height="{H}" fill="url(#lamp)"/>')
    for k in range(6):
        x = 776 + k * 32
        o.append(f'<rect x="{x}" y="0" width="12" height="{H}" fill="{s["bar_fill"] if s["fills"] else "none"}" stroke="{s["bar"]}" stroke-width="{s["lw"]*0.8}"/>')
    o.append(f'<rect x="760" y="210" width="200" height="14" fill="{s["bar_fill"] if s["fills"] else "none"}" stroke="{s["bar"]}" stroke-width="{s["lw"]*0.8}"/>')
    # parmaklık gölgeleri duvara (ışık sağdan)
    if s["fills"]:
        for k in range(5):
            x0 = 560 - k * 70
            o.append(f'<path d="M{x0},20 L{x0+26},20 L{x0-40},450 L{x0-66},450 Z" fill="{"#000" if not s["halftone"] else "url(#tram)"}" opacity="{0.22 if not s["halftone"] else 0.85}"/>')
    return "".join(o)

def dovme(s, plan_only=False):
    """Özgün dövme: omurga boyunca gotik kapı kemeri, kürek kemiklerinde açık kanatlı turnalar,
    kemer sütunları; ince plan çizgileri süslemenin içine gizli."""
    t = s["tat"]; lw = 2.2 if s["fills"] else 1.4
    o = []
    if not plan_only:
        # kapı kemeri (omurga)
        o.append(f'<path d="M452,560 V360 Q480,300 508,360 V560" fill="none" stroke="{t}" stroke-width="{lw*1.6}"/>'
                 f'<path d="M462,560 V366 Q480,320 498,366 V560" fill="none" stroke="{t}" stroke-width="{lw}"/>')
        for y in range(380, 560, 22):
            o.append(f'<path d="M452,{y} h-10 M508,{y} h10" stroke="{t}" stroke-width="{lw}"/>')
        # turnalar (kürek kemikleri)
        for sx in (-1, 1):
            cx = 480 + sx * 92; cy = 360
            o.append(f'<g transform="translate({cx},{cy}) scale({sx},1)">'
                     f'<path d="M0,0 L-46,-34 L-20,4 Z M0,0 L44,-40 L18,6 Z M-20,4 L0,26 L18,6 Z M0,26 L4,48" fill="{t if s["halftone"] else "none"}" fill-opacity="{0.25 if s["halftone"] else 0}" stroke="{t}" stroke-width="{lw}" stroke-linejoin="round"/>'
                     f'<path d="M18,6 L40,-6 L46,-2" fill="none" stroke="{t}" stroke-width="{lw}"/></g>')
        # sütunlar ve kemer süsleri (yanlar)
        for sx in (-1, 1):
            x = 480 + sx * 130
            o.append(f'<path d="M{x},560 V430 Q{x+sx*-18},404 {x+sx*-36},430 V560" fill="none" stroke="{t}" stroke-width="{lw}"/>')
            for k in range(5):
                o.append(f'<circle cx="{x+sx*-18}" cy="{450+k*24}" r="4" fill="none" stroke="{t}" stroke-width="{lw*0.8}"/>')
    # gizli plan çizgileri (koridor, boru, rota) — ışıklandığında görünür
    g = s["glow"]
    plan = ("M396,520 H440 V470 H470 M520,470 H560 V420 H590 M410,440 H436 M524,400 H566 V360 "
            "M380,480 V420 H420 M580,500 V450")
    o.append(f'<path d="{plan}" fill="none" stroke="{g}" stroke-width="{2.2 if s["fills"] else 1.8}" stroke-linecap="square" filter="url(#glow)" opacity="0.95"/>')
    return "".join(o)

def michael(s):
    """Sırttan, belden yukarı; kısa kazınmış saç, atlet yok (dövme görünür). Yüz yok."""
    sk = s["skin"]; ln = s["skin_line"]; lw = s["lw"]
    o = []
    body = "M282,560 L288,430 Q284,352 334,322 Q398,300 448,266 L512,266 Q562,300 626,322 Q676,352 672,430 L678,560 Z"
    if s["fills"] and not s["halftone"]:
        o.append(f'<path d="{body}" fill="url(#skinsh)"/>')
    elif s["halftone"]:
        o.append(f'<path d="{body}" fill="{sk}"/>'
                 f'<g clip-path="url(#back)"><path d="M300,300 Q380,420 360,560 L300,560 Z M470,300 Q440,420 470,560 L420,560 Q430,420 440,300 Z" fill="url(#tram)"/></g>')
    # sırt anatomisi (kürek kemiği, omurga oluğu)
    o.append(f'<g clip-path="url(#back)">'
             f'<path d="M380,350 Q400,400 430,410 M580,350 Q560,400 530,410" stroke="{ln}" stroke-width="{lw*0.45}" fill="none" opacity="0.45"/>'
             f'<path d="M480,300 V560" stroke="{ln}" stroke-width="{lw*0.4}" opacity="0.3"/>'
             f'<path d="M336,400 Q330,480 332,560 M624,400 Q630,480 628,560" stroke="{ln}" stroke-width="{lw*0.7}" fill="none" opacity="0.8"/>'
             f'<path d="M300,380 Q318,340 350,330 M660,380 Q642,340 610,330" stroke="{ln}" stroke-width="{lw*0.45}" fill="none" opacity="0.5"/>'
             + dovme(s) + '</g>')
    # kenar ışığı (sağ omuz, koridor ışığından)
    if s["fills"]:
        o.append(f'<path d="M626,322 Q676,352 672,430 L678,560" fill="none" stroke="{s["light"] if not s["halftone"] else s["glow"]}" stroke-width="{5 if not s["halftone"] else 4}" opacity="0.85"/>')
    o.append(f'<path d="{body}" fill="none" stroke="{ln}" stroke-width="{lw}" stroke-linejoin="round"/>')
    # boyun + baş (arkadan): kısa kazınmış saç
    o.append(f'<path d="M452,270 L456,226 L504,226 L508,270 Z" fill="{sk if s["fills"] else "none"}" stroke="{ln}" stroke-width="{lw}"/>')
    o.append(f'<ellipse cx="480" cy="190" rx="52" ry="60" fill="{sk if s["fills"] else "none"}" stroke="{ln}" stroke-width="{lw}"/>')
    o.append(f'<ellipse cx="428" cy="198" rx="9" ry="15" fill="{sk if s["fills"] else "none"}" stroke="{ln}" stroke-width="{lw*0.8}"/>'
             f'<ellipse cx="532" cy="198" rx="9" ry="15" fill="{sk if s["fills"] else "none"}" stroke="{ln}" stroke-width="{lw*0.8}"/>')
    hair_fill = {"A": "none", "B": s["hair"], "C": "url(#tram)"}[[k for k, v in STIL.items() if v is s][0]]
    cap = "M430,214 Q424,138 480,129 Q536,138 530,214 Q522,236 504,240 Q480,232 456,240 Q438,236 430,214 Z"
    o.append(f'<path d="{cap}" fill="{hair_fill}" opacity="{0.8 if s["fills"] else 1}" stroke="{ln}" stroke-width="{lw*0.5}"/>')
    rr = random.Random(9)
    for _ in range(140 if s["fills"] else 60):
        a = rr.uniform(0, 6.283); rad = rr.uniform(0, 1) ** 0.5
        x, y = 480 + 46 * rad * math.cos(a), 186 + 50 * rad * math.sin(a)
        if y < 232: o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="0.9" fill="{ln if not s["fills"] else "#000"}" opacity="0.35"/>')
    if s["fills"]:
        o.append(f'<path d="M520,150 Q536,180 530,210" stroke="{s["light"] if not s["halftone"] else s["glow"]}" stroke-width="4" fill="none" opacity="0.8"/>')
    return "".join(o)

def akis(s, sadece_yay=False):
    """Plan çizgileri tenden kalkıp omuz üstünden duvara akar ve kaçış haritasını kurar."""
    g = s["glow"]; r = random.Random(4); o = []
    # akış şeritleri (omuzdan duvara)
    for (x0, y0, x1, y1) in ((330, 440, 442, 130), (380, 500, 442, 225), (290, 470, 467, 98), (360, 410, 560, 300)):
        cx, cy = (x0 + x1) / 2 + r.uniform(-30, 30), min(y0, y1) - 40
        o.append(f'<path d="M{x0},{y0} Q{cx:.0f},{cy:.0f} {x1},{y1}" fill="none" stroke="{g}" stroke-width="2.2" stroke-dasharray="6 7" filter="url(#glow)" opacity="0.9"/>'
                 f'<circle cx="{x0}" cy="{y0}" r="3.5" fill="{g}" filter="url(#glow)"/>')
    if sadece_yay: return "".join(o)
    # duvardaki harita: koridorlar, hücre, revir, dış duvar, rota ve hedef
    m = ("M440,60 H740 V300 H440 Z M440,130 H560 M560,60 V300 M640,60 V190 H740 M680,190 V300 "
         "M452,76 h30 v22 h-30 Z M490,76 h30 v22 h-30 Z M528,76 h26 v22 h-26 Z M580,220 h40 v40 h-40 Z")
    o.append(f'<path d="{m}" fill="none" stroke="{g}" stroke-width="2" filter="url(#glow)" opacity="0.9"/>')
    route = "M467,98 V220 H600 V120 H690 V270 H726"
    o.append(f'<path d="{route}" fill="none" stroke="{g}" stroke-width="4" stroke-dasharray="14 8" stroke-linecap="round" filter="url(#glow)"/>')
    o.append(f'<path d="M714,258 l24,24 M738,258 l-24,24" stroke="{g}" stroke-width="5" stroke-linecap="round" filter="url(#glow)"/>')
    # havada yanan ayrıntı noktaları (düşük örtük ketlenme imzası): numaralı ışık noktaları
    for k, (x, y) in enumerate(((467, 98), (600, 220), (690, 120), (726, 270)), 1):
        o.append(f'<circle cx="{x}" cy="{y}" r="9" fill="none" stroke="{g}" stroke-width="2" filter="url(#glow)"/>'
                 f'<text x="{x+12}" y="{y-10}" font-family="DejaVu Sans Mono" font-size="14" fill="{g}">{k:02d}</text>')
    # tozlar
    for _ in range(40):
        x, y = r.uniform(80, 740), r.uniform(40, 460)
        o.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r.uniform(0.8, 2.0):.1f}" fill="{g}" opacity="{r.uniform(0.15, 0.6):.2f}"/>')
    return "".join(o)

def letterbox():
    return f'<rect x="0" y="0" width="{W}" height="36" fill="#000"/><rect x="0" y="{H-36}" width="{W}" height="36" fill="#000"/>'

def kare(k):
    s = STIL[k]
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
           + defs(s) + oda(s) + akis(s) + f'<g transform="translate(-150,30)">' + michael(s) + '</g>' + akis(s, sadece_yay=True)
           + (f'<rect width="{W}" height="{H}" fill="#FF7A1E" opacity="0.04"/>' if s["halftone"] else "")
           + f'<rect width="{W}" height="{H}" fill="none" stroke="#000" stroke-width="60" opacity="0.25" filter="url(#soft)"/>'
           + letterbox()
           + f'<text x="20" y="{H-12}" font-family="DejaVu Sans" font-size="15" fill="#fff">{k} · {s["ad"]}</text></svg>')
    f = P / f"stil_{k}.svg"; f.write_text(svg)
    subprocess.run(["rsvg-convert", "-w", str(W), "-o", str(P / f"stil_{k}.png"), str(f)], check=True)
    f.unlink()

if __name__ == "__main__":
    for k in STIL: kare(k)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(P / "stil_A.png"), "-i", str(P / "stil_B.png"), "-i", str(P / "stil_C.png"),
                    "-filter_complex", "[0][1][2]vstack=3,scale=640:-1", str(P / "stil_kontakt.png")], check=True)
    print("tamam")
