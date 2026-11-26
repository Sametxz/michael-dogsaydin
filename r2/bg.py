"""Dekorlar ve diegetik grafik objeler (SVG gövdeleri)."""
import math, random
from art2 import INK, shade, crown, serpent_body, serpent_head

GRAIN = ('<filter id="grain" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" seed="7"/>'
         '<feColorMatrix type="saturate" values="0"/><feComponentTransfer><feFuncA type="table" tableValues="0 0.10"/></feComponentTransfer></filter>'
         '<filter id="soft"><feGaussianBlur stdDeviation="18"/></filter><filter id="soft6"><feGaussianBlur stdDeviation="6"/></filter>'
         '<filter id="parch" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="4" seed="3"/>'
         '<feColorMatrix type="matrix" values="0 0 0 0 0.45  0 0 0 0 0.32  0 0 0 0 0.15  0 0 0 0.22 0"/></filter>')

def grain(w, h): return f'<rect width="{w}" height="{h}" filter="url(#grain)"/>'

def sky(w, h, c1, c2, c3=None):
    stops = f'<stop offset="0" stop-color="{c1}"/><stop offset="{0.6 if c3 else 1}" stop-color="{c2}"/>' + (f'<stop offset="1" stop-color="{c3}"/>' if c3 else "")
    return f'<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">{stops}</linearGradient></defs><rect width="{w}" height="{h}" fill="url(#sky)"/>'

def clouds(w, y, c, n=7, seed=1, s=1.0, a=1.0):
    r = random.Random(seed); out = []
    for i in range(n):
        x = r.uniform(-100, w + 100); yy = y + r.uniform(-40, 40); k = r.uniform(0.7, 1.4) * s
        out.append(f'<g transform="translate({x:.0f},{yy:.0f}) scale({k:.2f})" opacity="{a}"><ellipse cx="0" cy="0" rx="150" ry="38" fill="{c}"/>'
                   f'<ellipse cx="-50" cy="-24" rx="70" ry="44" fill="{c}"/><ellipse cx="50" cy="-30" rx="84" ry="52" fill="{c}"/>'
                   f'<ellipse cx="0" cy="12" rx="160" ry="20" fill="{shade(c,0.9)}"/></g>')
    return "".join(out)

def mountains(w, base, c, snow="#EEF2F5", seed=2, peaks=6, hmin=180, hmax=360):
    r = random.Random(seed); pts = [(-50, base)]; xs = sorted(r.uniform(0, w) for _ in range(peaks))
    snow_paths = []
    for x in xs:
        hh = r.uniform(hmin, hmax); pts += [(x - 160, base - hh*0.35), (x, base - hh), (x + 170, base - hh*0.3)]
        snow_paths.append(f'<path d="M{x-48},{base-hh*0.72:.0f} L{x},{base-hh:.0f} L{x+52},{base-hh*0.74:.0f} L{x+22},{base-hh*0.68:.0f} L{x+2},{base-hh*0.78:.0f} L{x-20},{base-hh*0.66:.0f} Z" fill="{snow}"/>')
    pts += [(w + 50, base)]
    return f'<polygon points="{" ".join(f"{x:.0f},{y:.0f}" for x, y in pts)} {w+50},{base+400} -50,{base+400}" fill="{c}"/>' + "".join(snow_paths)

def pines(w, base, c, n=24, seed=4, hmin=90, hmax=200):
    r = random.Random(seed); out = []
    for i in range(n):
        x = r.uniform(-40, w + 40); hh = r.uniform(hmin, hmax); ww = hh * 0.42
        out.append(f'<path d="M{x:.0f},{base-hh:.0f} L{x+ww*0.5:.0f},{base-hh*0.55:.0f} L{x+ww*0.3:.0f},{base-hh*0.55:.0f} L{x+ww*0.65:.0f},{base-hh*0.15:.0f} L{x+ww*0.1:.0f},{base-hh*0.15:.0f} L{x+ww*0.12:.0f},{base:.0f} L{x-ww*0.12:.0f},{base:.0f} L{x-ww*0.1:.0f},{base-hh*0.15:.0f} L{x-ww*0.65:.0f},{base-hh*0.15:.0f} L{x-ww*0.3:.0f},{base-hh*0.55:.0f} L{x-ww*0.5:.0f},{base-hh*0.55:.0f} Z" fill="{c}"/>')
    return "".join(out)

def ground(w, h, y, c, c2=None):
    return f'<path d="M0,{y} Q{w*0.3},{y-30} {w*0.55},{y-6} T{w},{y-10} V{h} H0 Z" fill="{c}"/>' + (f'<path d="M0,{y+60} Q{w*0.4},{y+30} {w},{y+70} V{h} H0 Z" fill="{c2}"/>' if c2 else "")

def sea(w, h, y, c1, c2, foam="#FFFFFF", a=0.3, seed=3):
    r = random.Random(seed)
    waves = "".join(f'<path d="M{r.uniform(0,w):.0f},{y + 30 + k*55:.0f} q30,-12 60,0 q30,12 60,0" stroke="{foam}" stroke-opacity="{a}" stroke-width="5" fill="none" stroke-linecap="round"/>' for k in range(int((h-y)/55)) for _ in range(5))
    return f'<defs><linearGradient id="sea" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient></defs><rect y="{y}" width="{w}" height="{h-y}" fill="url(#sea)"/>{waves}'

def longship(s=1.0, sail="#B23A2E", stripe="#E8D9B5", shields=("#C9A25A", "#2F4C6E", "#B23A2E"), oars=True, dragon=True, sail_up=True):
    o = [f'<g transform="scale({s})">']
    if sail_up:
        o.append(f'<rect x="-7" y="-330" width="14" height="330" fill="#6B4A2A" stroke="{INK}" stroke-width="5"/>')
        o.append(f'<path d="M-150,-310 Q0,-330 150,-310 Q160,-200 140,-100 Q0,-80 -140,-100 Q-160,-200 -150,-310 Z" fill="{sail}" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>')
        for k in (-80, -27, 27, 80):
            o.append(f'<path d="M{k},-318 Q{k*1.08},-200 {k},-92" stroke="{stripe}" stroke-width="22" fill="none" opacity="0.9"/>')
        o.append(f'<path d="M-150,-310 Q0,-330 150,-310 Q160,-200 140,-100 Q0,-80 -140,-100 Q-160,-200 -150,-310 Z" fill="none" stroke="{INK}" stroke-width="6"/>')
        o.append(f'<path d="M30,-300 Q60,-200 40,-110" stroke="#000" stroke-opacity="0.12" stroke-width="40" fill="none"/>')
    if oars:
        for i in range(-4, 5):
            o.append(f'<path d="M{i*52},-20 L{i*52-30},70" stroke="{INK}" stroke-width="10" stroke-linecap="round"/><path d="M{i*52},-20 L{i*52-30},70" stroke="#A07A4A" stroke-width="4" stroke-linecap="round"/>')
    o.append(f'<path d="M-300,-50 Q-280,40 0,44 Q280,40 300,-50 Q330,-110 316,-180 Q290,-110 260,-60 L-260,-60 Q-290,-110 -316,-180 Q-330,-110 -300,-50 Z" fill="#8C5A2E" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>')
    o.append(f'<path d="M-280,-24 Q0,0 280,-24" stroke="#6B4222" stroke-width="5" fill="none"/><path d="M-270,4 Q0,26 270,4" stroke="#6B4222" stroke-width="5" fill="none"/>')
    if dragon:
        o.append(f'<path d="M316,-180 Q330,-230 360,-226 Q384,-214 368,-196 Q352,-200 340,-188 Z" fill="#8C5A2E" stroke="{INK}" stroke-width="5"/><circle cx="356" cy="-214" r="4" fill="{INK}"/>')
    for i in range(-4, 5):
        o.append(f'<circle cx="{i*60}" cy="-44" r="24" fill="{shields[i % len(shields)]}" stroke="{INK}" stroke-width="4"/><circle cx="{i*60}" cy="-44" r="6" fill="#C3CCD3" stroke="{INK}" stroke-width="2.5"/>')
    o.append('</g>')
    return "".join(o)

def longhouse_interior(w=2100, h=1180, night=True):
    wall = "#4A3222" if night else "#7A5638"
    o = [f'<rect width="{w}" height="{h}" fill="{wall}"/>']
    for x in range(0, w, 120):
        o.append(f'<rect x="{x}" y="0" width="120" height="{h}" fill="{shade(wall, 0.92 if (x//120)%2 else 1.0)}"/>')
        o.append(f'<path d="M{x},0 V{h}" stroke="{INK}" stroke-opacity="0.45" stroke-width="4"/>')
        o.append(f'<path d="M{x+30},{(x*7)%300+100} q30,10 60,0 M{x+20},{(x*13)%400+500} q40,8 70,-4" stroke="{INK}" stroke-opacity="0.18" stroke-width="3" fill="none"/>')
    o.append(f'<path d="M0,0 L{w/2},-120 L{w},0 L{w},120 L{w/2},20 L0,120 Z" fill="#2E1E14"/>')
    for x in (180, w - 180):
        o.append(f'<rect x="{x-46}" y="0" width="92" height="{h}" fill="#5A3B22" stroke="{INK}" stroke-width="6"/><path d="M{x-30},0 V{h}" stroke="#7A5232" stroke-width="8"/>')
        for k in range(5):
            o.append(f'<path d="M{x-40},{150+k*170} q40,-20 80,0" stroke="#3A2414" stroke-width="5" fill="none"/>')
    o.append(f'<rect y="{h-260}" width="{w}" height="260" fill="#3A2818"/>')
    for x in range(0, w, 160):
        o.append(f'<path d="M{x},{h-260} L{x-60},{h}" stroke="#2A1C10" stroke-width="5"/>')
    # duvarda kalkanlar
    for i, (x, c) in enumerate(((420, "#B23A2E"), (640, "#2F4C6E"), (1460, "#C9A25A"), (1680, "#3B6B6B"))):
        o.append(f'<g transform="translate({x},330)"><circle r="78" fill="{c}" stroke="{INK}" stroke-width="6"/><circle r="66" fill="none" stroke="#9AA4AC" stroke-width="8"/>'
                 f'<path d="M0,-66 V66 M-66,0 H66" stroke="{shade(c,1.35)}" stroke-width="10"/><circle r="16" fill="#B9C2C9" stroke="{INK}" stroke-width="4"/></g>')
    return "".join(o)

def hearth(x, y, s=1.0):
    return (f'<g transform="translate({x},{y}) scale({s})"><ellipse cx="0" cy="10" rx="210" ry="40" fill="#2A1A10"/>'
            + "".join(f'<ellipse cx="{-170+i*48}" cy="{6 + (i%2)*6}" rx="30" ry="20" fill="#7D7468" stroke="{INK}" stroke-width="4"/>' for i in range(8))
            + f'<path d="M-90,0 L80,-26 M-80,-24 L90,4" stroke="#5A3B22" stroke-width="20" stroke-linecap="round"/><path d="M-90,0 L80,-26 M-80,-24 L90,4" stroke="{INK}" stroke-width="3" stroke-linecap="round" opacity="0.6"/></g>')

def flame(x, y, s=1.0, t=0.0):
    k = 1 + 0.08*math.sin(t*9) + 0.05*math.sin(t*13.7)
    sw = 6*math.sin(t*5.3)
    return (f'<g transform="translate({x},{y}) scale({s},{s*k:.3f})"><path d="M-80,0 Q-100,-90 -30,-150 Q-40,-90 0,-80 Q-10,-170 {40+sw:.0f},-230 Q30,-140 70,-110 Q90,-140 80,-170 Q130,-90 80,0 Z" fill="#F08A2A"/>'
            f'<path d="M-50,0 Q-60,-60 -10,-100 Q-10,-60 20,-56 Q20,-120 {50+sw:.0f},-150 Q50,-90 70,-60 Q80,-20 50,0 Z" fill="#FFC64A"/>'
            f'<path d="M-20,0 Q-26,-30 0,-56 Q6,-30 24,-30 Q40,-10 20,0 Z" fill="#FFF2B0"/></g>')

def parchment(w, h, c="#EAD7A8", edge="#B8955A"):
    r = random.Random(w*h)
    pts = []
    for i in range(24): pts.append((w*i/23, r.uniform(-6, 6)))
    for i in range(14): pts.append((w + r.uniform(-6, 6), h*i/13))
    for i in range(24): pts.append((w - w*i/23, h + r.uniform(-6, 6)))
    for i in range(14): pts.append((r.uniform(-6, 6), h - h*i/13))
    poly = " ".join(f"{x:.0f},{y:.0f}" for x, y in pts)
    return (f'<polygon points="{poly}" fill="#000" opacity="0.3" transform="translate(10,14)"/>'
            f'<polygon points="{poly}" fill="{c}" stroke="{edge}" stroke-width="5"/><polygon points="{poly}" filter="url(#parch)"/>'
            f'<polygon points="{poly}" fill="none" stroke="{INK}" stroke-width="3" opacity="0.6"/>')

def scroll_frame(w, h, c="#EAD7A8"):
    return (parchment(w, h, c) +
            f'<rect x="-30" y="-26" width="{w+60}" height="34" rx="17" fill="#B88A50" stroke="{INK}" stroke-width="5"/>'
            f'<rect x="-30" y="{h-8}" width="{w+60}" height="34" rx="17" fill="#B88A50" stroke="{INK}" stroke-width="5"/>'
            f'<circle cx="-30" cy="-9" r="20" fill="#8C5E34" stroke="{INK}" stroke-width="4"/><circle cx="{w+30}" cy="-9" r="20" fill="#8C5E34" stroke="{INK}" stroke-width="4"/>'
            f'<circle cx="-30" cy="{h+9}" r="20" fill="#8C5E34" stroke="{INK}" stroke-width="4"/><circle cx="{w+30}" cy="{h+9}" r="20" fill="#8C5E34" stroke="{INK}" stroke-width="4"/>')

def rune_border(w, h, c="#6B5A44"):
    runes = "ᚱᚨᚷᚾᚨᚱ ᛚᛟᚦᛒᚱᛟᚲ ᛋᛁᚷᚢᚱᚦᚱ ᚺᚱᛁᛜ ᚨᛋᛚᚨᚢᚷ "
    return (f'<rect x="18" y="18" width="{w-36}" height="{h-36}" rx="14" fill="none" stroke="{c}" stroke-width="4"/>'
            f'<rect x="34" y="34" width="{w-68}" height="{h-68}" rx="10" fill="none" stroke="{c}" stroke-width="2"/>')

def stone_slab(w, h, c="#7E7A72"):
    r = random.Random(5); pts = []
    for i in range(18): pts.append((w*i/17, 30*math.sin(i/17*math.pi)*-1 + r.uniform(-8, 8) + 30))
    for i in range(10): pts.append((w + r.uniform(-10, 10), h*i/9))
    for i in range(18): pts.append((w - w*i/17, h + r.uniform(-6, 6)))
    for i in range(10): pts.append((r.uniform(-10, 10), h - h*i/9))
    poly = " ".join(f"{x:.0f},{y:.0f}" for x, y in pts)
    cracks = "".join(f'<path d="M{r.uniform(0,w):.0f},{r.uniform(0,h):.0f} l{r.uniform(-60,60):.0f},{r.uniform(20,80):.0f} l{r.uniform(-40,40):.0f},{r.uniform(20,60):.0f}" stroke="{shade(c,0.7)}" stroke-width="3" fill="none"/>' for _ in range(10))
    lich = "".join(f'<circle cx="{r.uniform(0,w):.0f}" cy="{r.uniform(0,h):.0f}" r="{r.uniform(6,22):.0f}" fill="#8E9A6A" opacity="0.35"/>' for _ in range(14))
    return (f'<polygon points="{poly}" fill="#000" opacity="0.35" transform="translate(14,18)"/>'
            f'<polygon points="{poly}" fill="{c}" stroke="{INK}" stroke-width="6"/>'
            f'<polygon points="{poly}" filter="url(#grain)"/>{cracks}{lich}'
            f'<path d="M{w*0.72},40 Q{w*0.85},{h*0.5} {w*0.78},{h}" stroke="#000" stroke-opacity="0.12" stroke-width="{w*0.25:.0f}" fill="none"/>')

def map_vellum(w, h):
    return (f'<rect width="{w}" height="{h}" fill="#E4CC98"/><rect width="{w}" height="{h}" filter="url(#parch)"/>'
            f'<rect x="40" y="40" width="{w-80}" height="{h-80}" fill="none" stroke="#8C6B3E" stroke-width="8" stroke-dasharray="40 14"/>'
            + "".join(f'<path d="M{60+k*90},{h-100} q20,-10 40,0 q20,10 40,0" stroke="#7A9AAA" stroke-width="3" fill="none" opacity="0.6"/>' for k in range(int((w-120)/90))))

# kara parçaları (stilize)
SCANDI = "M1180,140 Q1260,90 1330,130 Q1420,110 1480,180 Q1520,260 1470,330 Q1500,420 1440,500 Q1380,560 1320,520 Q1290,600 1230,620 Q1170,600 1180,540 Q1120,480 1150,420 Q1100,360 1140,300 Q1110,230 1180,140 Z"
JUTLAND = "M1060,520 Q1110,500 1130,560 Q1150,640 1100,700 Q1060,720 1040,680 Q1020,600 1060,520 Z"
BRITAIN = "M560,200 Q620,160 670,220 Q700,300 690,380 Q740,460 700,560 Q640,620 560,600 Q500,560 530,480 Q480,400 520,330 Q500,260 560,200 Z"
FRANCE = "M520,700 Q650,650 820,680 Q960,700 1000,800 Q1010,920 900,1000 L520,1000 Q440,880 520,700 Z"

def land(path, c="#C8AE76", stroke="#6B5432"):
    return f'<path d="{path}" fill="{c}" stroke="{stroke}" stroke-width="6" stroke-linejoin="round"/><path d="{path}" fill="none" stroke="{stroke}" stroke-width="2" opacity="0.4" transform="translate(6,6)"/>'

def frame_portrait(w, h, inner, plate=None, c="#B8893A"):
    return (f'<rect x="-8" y="-8" width="{w+16}" height="{h+16}" rx="10" fill="#000" opacity="0.35" transform="translate(10,12)"/>'
            f'<rect x="-14" y="-14" width="{w+28}" height="{h+28}" rx="12" fill="{c}" stroke="{INK}" stroke-width="6"/>'
            f'<rect x="0" y="0" width="{w}" height="{h}" fill="#E9DAB4" stroke="{INK}" stroke-width="4"/>'
            f'<svg x="0" y="0" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{inner}</svg>'
            + (f'<rect x="{w/2-110}" y="{h-6}" width="220" height="44" rx="6" fill="#D9B45A" stroke="{INK}" stroke-width="4"/>'
               f'<text x="{w/2}" y="{h+26}" font-family="Alegreya SC" font-weight="bold" font-size="26" text-anchor="middle" fill="{INK}">{plate}</text>' if plate else ""))

def checkbox(x, y, checked=False):
    return (f'<rect x="{x}" y="{y}" width="52" height="52" rx="6" fill="#F6EBD0" stroke="{INK}" stroke-width="5"/>'
            + (f'<path d="M{x+8},{y+26} L{x+22},{y+42} L{x+50},{y-4}" stroke="#2E7D3A" stroke-width="10" fill="none" stroke-linecap="round" stroke-linejoin="round"/>' if checked else ""))

def stamp(text, c="#B8322A", rot=-12, size=60):
    w = len(text) * size * 0.66 + 60
    return (f'<g transform="rotate({rot})" opacity="0.9"><rect x="{-w/2}" y="{-size*0.8}" width="{w}" height="{size*1.5}" rx="10" fill="none" stroke="{c}" stroke-width="8"/>'
            f'<text y="{size*0.32}" font-family="Alegreya SC" font-weight="800" font-size="{size}" text-anchor="middle" fill="{c}" letter-spacing="3">{text}</text></g>')

def coins_pile(n=40, seed=1, w=420, h=160):
    r = random.Random(seed); o = []
    for i in range(n):
        x = r.gauss(0, w*0.22); y = -abs(r.gauss(0, h*0.35)) + abs(x)*0.25
        c = "#E2B23A" if r.random() < 0.6 else "#C9CDD2"
        o.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="26" ry="10" fill="{c}" stroke="{INK}" stroke-width="3.5"/>')
    return "".join(o)

def chest(open_=True, gold=True):
    o = f'<rect x="-140" y="-110" width="280" height="110" rx="10" fill="#7A4E2C" stroke="{INK}" stroke-width="6"/><rect x="-140" y="-70" width="280" height="14" fill="#C9A25A" stroke="{INK}" stroke-width="4"/>'
    if gold: o = f'<g transform="translate(0,-110)">{coins_pile(26, 2, 300, 90)}</g>' + o
    if open_: o = f'<path d="M-140,-110 L-120,-210 L120,-210 L140,-110 Z" fill="#8C5E34" stroke="{INK}" stroke-width="6"/>' + o
    return o
