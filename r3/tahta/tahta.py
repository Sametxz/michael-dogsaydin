"""Saga Tahtası köprüleri: üç stil önerisi (aynı an, K4: üç oğul, Wessex seferi, Kattegat yanıyor, kartal, üç gece).
A · oymalı meşe tahta + pullar   B · harita masası   C · duvar halısı (dokuma)
python3 tahta.py → tahta/stil_A.png, stil_B.png, stil_C.png, stil_kontakt_960.png
"""
import sys, math, random, subprocess
sys.path[:0] = ["/home/claude/r3", "/home/claude/r2", "/home/claude/r3/veda", "/home/claude/r3/veda2", "/home/claude/r3/ivar2",
                "/home/claude/r3/bedel", "/home/claude/r3/floki", "/home/claude/r3/kurul/test_ivar"]
from art3 import head3, RAGNAR_UC
from frames import RG, ASLv
from kareler import BJv
from modeller import BORG
import assets as A
OUT = "/home/claude/r3/tahta"; W, H = 1920, 1080; INK = "#1A1410"
UBBE = dict(BJv, hair="#C9A462", iris="#5E8CA8"); HVIT = dict(BJv, hair="#E2D3A0", iris="#6A8AA0"); SIG = dict(BJv, hair="#6A4A30", iris="#7A9A6A")
R = random.Random(4)

def token(spec, x, y, r, rim="#6E4A2A", expr="neutral", tint=None, stitch=False, mark=""):
    """Karakter pulu: ahşap disk, içinde model kafası (kırpılmış), dışta halka."""
    k = r / 150.0; cid = f"tk{int(x)}_{int(y)}"
    face = (f'<clipPath id="{cid}"><circle r="{r*0.84:.0f}"/></clipPath>'
            f'<g clip-path="url(#{cid})"><circle r="{r}" fill="{tint or "#D8C4A0"}"/>'
            f'<g transform="translate({r*0.06:.0f},{r*0.32:.0f}) scale({k*0.95:.3f})">{head3(spec, "3q", expr, 0.15)}</g></g>')
    if stitch:
        ring = (f'<circle r="{r*0.92:.0f}" fill="none" stroke="#8A2A22" stroke-width="{r*0.13:.0f}"/>'
                f'<circle r="{r*0.92:.0f}" fill="none" stroke="#E8D6A8" stroke-width="3" stroke-dasharray="9 7"/>'
                f'<circle r="{r*0.99:.0f}" fill="none" stroke="#3A2A1E" stroke-width="3" stroke-dasharray="4 5"/>')
        base = ""
    else:
        base = (f'<ellipse cx="6" cy="{r*0.16:.0f}" rx="{r*1.04:.0f}" ry="{r*1.06:.0f}" fill="#000" opacity="0.45"/>'
                f'<circle r="{r}" fill="{rim}" stroke="{INK}" stroke-width="5"/>')
        ring = (f'<circle r="{r*0.84:.0f}" fill="none" stroke="{INK}" stroke-width="5"/>'
                f'<circle r="{r*0.92:.0f}" fill="none" stroke="#C99A4A" stroke-width="3" opacity="0.8"/>'
                f'<path d="M{-r*0.7:.0f},{-r*0.7:.0f} A{r} {r} 0 0 1 {r*0.7:.0f},{-r*0.7:.0f}" stroke="#FFF" stroke-width="4" fill="none" opacity="0.18"/>')
    return f'<g transform="translate({x},{y})">{base}{face}{ring}{mark}</g>'

def snake_mark(r):   # Sigurd: yılan gözü işareti (küçük oyma)
    return (f'<g transform="translate({r*0.62:.0f},{r*0.62:.0f})"><circle r="{r*0.26:.0f}" fill="#E8D6A8" stroke="{INK}" stroke-width="4"/>'
            f'<path d="M{-r*0.16:.0f},0 Q0,{-r*0.16:.0f} {r*0.16:.0f},0 Q0,{r*0.16:.0f} {-r*0.16:.0f},0 Z" fill="#5A7A3A" stroke="{INK}" stroke-width="2"/><ellipse rx="2" ry="{r*0.1:.0f}" fill="{INK}"/></g>')

def knot_band(x0, y0, x1, y1, col, w=26):
    """Kenar düğüm bandı: iç içe geçen iki dalgalı şerit."""
    L = math.hypot(x1 - x0, y1 - y0); a = math.degrees(math.atan2(y1 - y0, x1 - x0)); n = int(L / 60)
    p1 = "M0,0 " + " ".join(f"Q{i*60+30},{(-1)**i*w*0.6:.0f} {i*60+60},0" for i in range(n))
    p2 = "M0,0 " + " ".join(f"Q{i*60+30},{(-1)**(i+1)*w*0.6:.0f} {i*60+60},0" for i in range(n))
    return (f'<g transform="translate({x0},{y0}) rotate({a:.1f})">'
            f'<path d="{p1}" stroke="{INK}" stroke-width="{w*0.62:.0f}" fill="none"/><path d="{p1}" stroke="{col}" stroke-width="{w*0.36:.0f}" fill="none"/>'
            f'<path d="{p2}" stroke="{INK}" stroke-width="{w*0.62:.0f}" fill="none"/><path d="{p2}" stroke="{col}" stroke-width="{w*0.36:.0f}" fill="none"/></g>')

# ---------- ikonlar (oyma/çizim; renk parametreli)
def ship(x, y, s, body="#6A4428", sail="#B8322A", line=INK):
    return (f'<g transform="translate({x},{y}) scale({s})"><path d="M-120,0 Q-60,40 0,40 Q60,40 120,0 L104,-6 Q60,18 0,18 Q-60,18 -104,-6 Z" fill="{body}" stroke="{line}" stroke-width="6"/>'
            f'<path d="M-104,-6 Q-128,-40 -112,-64 Q-100,-50 -96,-30" fill="none" stroke="{line}" stroke-width="7"/><path d="M104,-6 Q128,-40 112,-64" fill="none" stroke="{line}" stroke-width="7"/>'
            f'<path d="M0,18 L0,-150" stroke="{line}" stroke-width="7"/><path d="M-62,-140 L62,-140 L54,-30 L-54,-30 Z" fill="{sail}" stroke="{line}" stroke-width="6"/>'
            + "".join(f'<path d="M{-50+i*25},-138 L{-46+i*23},-32" stroke="#F0E0C0" stroke-width="7" opacity="0.7"/>' for i in range(0, 5, 2))
            + "".join(f'<circle cx="{-80+i*32}" cy="8" r="11" fill="#C9A25A" stroke="{line}" stroke-width="4"/>' for i in range(6)) + '</g>')

def hall(x, y, s, wall="#7A5434", roof="#4A3420", line=INK):
    return (f'<g transform="translate({x},{y}) scale({s})"><path d="M-110,0 L-110,-70 L110,-70 L110,0 Z" fill="{wall}" stroke="{line}" stroke-width="6"/>'
            f'<path d="M-140,-62 L0,-150 L140,-62 Z" fill="{roof}" stroke="{line}" stroke-width="6"/><path d="M-20,0 L-20,-44 L20,-44 L20,0" fill="#2A1A10" stroke="{line}" stroke-width="5"/>'
            f'<path d="M-30,-150 L-48,-178 M30,-150 L48,-178" stroke="{line}" stroke-width="7"/></g>')

def flames(x, y, s, a=1.0):
    out = []
    for i, (dx, h) in enumerate([(-80, 120), (-30, 170), (20, 140), (70, 110), (-55, 90), (45, 80)]):
        out.append(f'<path d="M{dx-28},0 Q{dx-30},{-h*0.5} {dx},{-h} Q{dx+30},{-h*0.5} {dx+28},0 Z" fill="#E8742A" stroke="{INK}" stroke-width="4"/>'
                   f'<path d="M{dx-14},0 Q{dx-12},{-h*0.4} {dx},{-h*0.6} Q{dx+12},{-h*0.4} {dx+14},0 Z" fill="#FFD27A"/>')
    return f'<g transform="translate({x},{y}) scale({s})" opacity="{a}">' + "".join(out) + '</g>'

def eagle(x, y, s, fill="#8A6A3A", line=INK):
    """Kartal oyması (kansız): açık kanat, üç sıra tüy, kuyruk yelpazesi, kancalı gaga."""
    dk = "#5A3E22" if fill.startswith("#8") or fill.startswith("#7") else "#7A4A22"
    def wing(sx):
        o = []
        for row, (n, L, y0) in enumerate([(7, 70, 0), (6, 54, -26), (5, 38, -48)]):
            for k in range(n):
                ax = sx * (30 + k * 24 + row * 6); ay = y0 - k * 7 + row * 4
                o.append(f'<path d="M{ax},{ay} q{sx*8},{L*0.5} {sx*4},{L} q{sx*-12},{-L*0.3} {sx*-14},{-L*0.9} Z" fill="{fill if row else dk}" stroke="{line}" stroke-width="4"/>')
        o.append(f'<path d="M{sx*20},-40 Q{sx*110},-110 {sx*200},-60 Q{sx*120},-50 {sx*30},-4 Z" fill="{fill}" stroke="{line}" stroke-width="5"/>')
        return "".join(o[::-1])
    tail = "".join(f'<path d="M0,60 L{-30+k*15},{140+abs(k-2)*-8} L{-18+k*15},{140+abs(k-2)*-8} Z" fill="{dk}" stroke="{line}" stroke-width="4"/>' for k in range(5))
    return (f'<g transform="translate({x},{y}) scale({s})">{tail}{wing(-1)}{wing(1)}'
            f'<path d="M-26,-20 Q0,-64 26,-20 L20,70 Q0,92 -20,70 Z" fill="{fill}" stroke="{line}" stroke-width="6"/>'
            + "".join(f'<path d="M{-12+(k%2)*12},{-6+k*14} q6,6 12,0" stroke="{line}" stroke-width="3" fill="none"/>' for k in range(5)) +
            f'<circle cy="-50" r="20" fill="{fill}" stroke="{line}" stroke-width="5"/><circle cx="6" cy="-54" r="4" fill="{line}"/>'
            f'<path d="M16,-56 Q38,-52 30,-34 Q24,-44 14,-42 Z" fill="#D8B04A" stroke="{line}" stroke-width="3"/></g>')

def horn(x, y, s, rot=0):
    return (f'<g transform="translate({x},{y}) rotate({rot}) scale({s})"><path d="M-110,10 Q-20,40 90,-50 L110,-30 Q10,70 -110,40 Z" fill="#D8C8A0" stroke="{INK}" stroke-width="6"/>'
            f'<path d="M80,-56 L116,-24" stroke="#B08A3A" stroke-width="14"/><path d="M-60,22 Q-56,40 -62,46 M-20,30 Q-16,48 -22,54" stroke="#B08A3A" stroke-width="8"/></g>')

def coins(x, y, n=7, seed=2):
    r = random.Random(seed); o = []
    for k in range(n):
        cx, cy = x + r.uniform(-60, 60), y + r.uniform(-24, 24)
        o.append(f'<ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="20" ry="13" fill="#C9A23A" stroke="{INK}" stroke-width="4"/><ellipse cx="{cx-4:.0f}" cy="{cy-3:.0f}" rx="8" ry="4" fill="#F0D88A"/>')
    return "".join(o)

def seax(x, y, s, rot=0):
    return (f'<g transform="translate({x},{y}) rotate({rot}) scale({s})"><path d="M0,0 L230,-8 Q250,6 228,16 L0,14 Z" fill="#B8C0C8" stroke="{INK}" stroke-width="5"/>'
            f'<path d="M10,4 L210,0" stroke="#E8EEF2" stroke-width="3"/><rect x="-110" y="-6" width="110" height="26" rx="8" fill="#4A2E1A" stroke="{INK}" stroke-width="5"/>'
            f'<rect x="-14" y="-12" width="16" height="38" fill="#B08A3A" stroke="{INK}" stroke-width="4"/></g>')

def runes(x, y, txt_n=26, s=1.0, col="#2A1608", seed=1):
    r = random.Random(seed); o = []
    shapes = ["M0,0 V40 M0,8 L14,0 M0,20 L14,12", "M0,0 V40 M0,0 L14,14 L0,26", "M0,0 V40 M14,0 V40 M0,14 L14,26", "M0,0 V40 M0,6 L14,18 L0,30",
              "M0,0 L14,40 M14,0 L0,40", "M7,0 V40 M0,10 L7,20 L14,10", "M0,0 V40 M0,0 L14,10 L0,20 L14,30 L0,40", "M0,40 L7,0 L14,40"]
    for k in range(txt_n):
        o.append(f'<path d="{r.choice(shapes)}" transform="translate({x+k*26*s:.0f},{y}) scale({s})" stroke="{col}" stroke-width="5" fill="none" stroke-linecap="round"/>')
        if k % 6 == 5: o.append(f'<circle cx="{x+k*26*s+20*s:.0f}" cy="{y+20*s:.0f}" r="{3*s:.1f}" fill="{col}"/>')
    return "".join(o)

def candles(x, y, s, lit=(True, False, False), wax="#E8DCC0", line=INK, glow=True):
    out = []
    for i, on in enumerate(lit):
        cx = (i - 1) * 70
        out.append(f'<rect x="{cx-16}" y="-90" width="32" height="90" rx="4" fill="{wax}" stroke="{line}" stroke-width="5"/>'
                   f'<path d="M{cx},-90 L{cx},-104" stroke="{line}" stroke-width="4"/>')
        if on:
            if glow: out.append(f'<circle cx="{cx}" cy="-124" r="46" fill="url(#glow)"/>')
            out.append(f'<path d="M{cx-11},-104 Q{cx-10},-128 {cx},-146 Q{cx+10},-128 {cx+11},-104 Z" fill="#F7A23A" stroke="{line}" stroke-width="3"/><path d="M{cx-5},-106 Q{cx},-124 {cx+5},-106 Z" fill="#FFE6A0"/>')
        else:
            out.append(f'<path d="M{cx},-106 q-10,-20 4,-34 q12,-14 0,-30" stroke="#9A9A9A" stroke-width="5" fill="none" opacity="0.6"/>')
    return f'<g transform="translate({x},{y}) scale({s})">' + "".join(out) + '</g>'

def thread(pts, col="#B8322A", w=6, dash=""):
    d = "M" + " Q".join(f"{x},{y}" for x, y in pts[:1]) + "".join(
        f" Q{(pts[i][0]+pts[i+1][0])/2:.0f},{min(pts[i][1],pts[i+1][1])-50:.0f} {pts[i+1][0]},{pts[i+1][1]}" for i in range(len(pts) - 1))
    return (f'<path d="{d}" stroke="#000" stroke-width="{w+4}" fill="none" opacity="0.35" transform="translate(4,6)"/>'
            f'<path d="{d}" stroke="{col}" stroke-width="{w}" fill="none" stroke-linecap="round" {dash}/>')

def carved(svg, depth=4):
    """Oyma etkisi: içe gölge (koyu kopya kaydırılmış) + açık kenar."""
    return (f'<g transform="translate({-depth*0.6},{-depth*0.6})" opacity="0.35" filter="url(#lite)">{svg}</g>'
            f'<g transform="translate({depth},{depth})" opacity="0.6" filter="url(#dark)">{svg}</g>{svg}')

def label(x, y, txt, size=46, col="#E8D6A8", font="Georgia", anchor="middle", weight="bold"):
    return (f'<text x="{x+3}" y="{y+4}" font-family="{font}" font-size="{size}" font-weight="{weight}" fill="#000" opacity="0.55" text-anchor="{anchor}" letter-spacing="3">{txt}</text>'
            f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" font-weight="{weight}" fill="{col}" text-anchor="{anchor}" letter-spacing="3">{txt}</text>')

COMMON_DEFS = ('<radialGradient id="glow"><stop offset="0" stop-color="#FFD890" stop-opacity="0.75"/><stop offset="1" stop-color="#FFB040" stop-opacity="0"/></radialGradient>'
               '<filter id="dark"><feColorMatrix values="0 0 0 0 0.05  0 0 0 0 0.03  0 0 0 0 0.02  0 0 0 1 0"/></filter>'
               '<filter id="lite"><feColorMatrix values="0 0 0 0 1  0 0 0 0 0.92  0 0 0 0 0.8  0 0 0 1 0"/></filter>'
               '<radialGradient id="vig" cx="0.5" cy="0.5" r="0.75"><stop offset="0.55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity="0.75"/></radialGradient>')

def wood_grain(x0, y0, w, h, base, dark, seed=1, n=70, vertical=False):
    r = random.Random(seed); out = [f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" fill="{base}"/>']
    for i in range(n):
        yy = y0 + r.uniform(0, h); amp = r.uniform(4, 22); ph = r.uniform(0, 300)
        d = f"M{x0},{yy:.0f} " + " ".join(f"Q{x0+k*160+80+ph%80:.0f},{yy+amp*(-1)**k:.0f} {x0+(k+1)*160:.0f},{yy:.0f}" for k in range(int(w / 160) + 1))
        out.append(f'<path d="{d}" stroke="{dark}" stroke-width="{r.uniform(1.5,5):.1f}" fill="none" opacity="{r.uniform(0.18,0.5):.2f}"/>')
    for i in range(4):   # budak
        cx, cy = x0 + r.uniform(80, w - 80), y0 + r.uniform(60, h - 60)
        out.append(f'<ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="{r.uniform(18,34):.0f}" ry="{r.uniform(8,14):.0f}" fill="{dark}" opacity="0.45"/>'
                   f'<ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="40" ry="18" fill="none" stroke="{dark}" stroke-width="3" opacity="0.3"/>')
    return "".join(out)

def frame_svg(inner, defs=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}"><defs>{COMMON_DEFS}{defs}</defs>{A.defs(1.0)}{inner}'
            f'<rect width="{W}" height="{H}" fill="url(#vig)"/><rect width="{W}" height="70" fill="#000"/><rect y="{H-70}" width="{W}" height="70" fill="#000"/></svg>')

# ======================================================== A · oymalı meşe tahta + pullar
def stil_A():
    o = [wood_grain(0, 0, W, H, "#3A2416", "#1A0E06", seed=2, n=50)]                     # masa (koyu)
    o.append('<rect x="150" y="110" width="1620" height="880" rx="26" fill="#000" opacity="0.5" transform="translate(14,18)"/>')
    o.append(f'<g><clipPath id="board"><rect x="150" y="110" width="1620" height="880" rx="26"/></clipPath><g clip-path="url(#board)">{wood_grain(150, 110, 1620, 880, "#8A5A32", "#4A2C14", seed=7, n=90)}</g></g>')
    o.append(f'<rect x="150" y="110" width="1620" height="880" rx="26" fill="none" stroke="{INK}" stroke-width="10"/>')
    for (a, b, c_, d) in [(196, 152, 1724, 152), (196, 948, 1724, 948)]: o.append(knot_band(a, b, c_, d, "#B98A4E"))
    for (a, b, c_, d) in [(192, 156, 192, 944), (1728, 156, 1728, 944)]: o.append(knot_band(a, b, c_, d, "#B98A4E"))
    o.append('<rect x="232" y="190" width="1456" height="720" rx="8" fill="#000" opacity="0.12" stroke="#2A1608" stroke-width="5"/>')
    # oyma ikonlar ve iplik
    o.append(carved(hall(470, 610, 1.0, "#6A4428", "#4A2C14")))
    o.append(flames(470, 470, 0.9, 0.95))
    o.append(carved(ship(1380, 520, 0.9, "#6A4428", "#9A2A22")))
    o.append(thread([(560, 540), (1260, 470)], "#B8322A", 7, 'stroke-dasharray="2 0"'))
    o.append(carved(eagle(960, 360, 0.75, "#7A5432")))
    o.append(candles(1460, 870, 0.9, (True, False, False)))
    o.append(token(RG, 960, 650, 120, expr="neutral"))
    o.append(token(ASLv, 720, 820, 80))
    for i, (sp, mk) in enumerate([(UBBE, ""), (HVIT, ""), (SIG, snake_mark(54))]):
        o.append(token(sp, 980 + i * 125, 840, 54, mark=mk))
    o.append(thread([(800, 820), (926, 840)], "#B8322A", 5))
    o.append(carved(runes(640, 900, 26, 1.0, "#3A2010", 3), 2))
    o.append(horn(110, 380, 0.9, 80)); o.append(coins(1840, 560, 9)); o.append(seax(1760, 1000, 0.9, -28))
    for k, (gx, gy) in enumerate([(300, 820), (340, 860), (390, 830), (1620, 300), (1580, 340)]):   # hnefatafl taşları
        o.append(f'<ellipse cx="{gx+4}" cy="{gy+8}" rx="20" ry="12" fill="#000" opacity="0.4"/><circle cx="{gx}" cy="{gy}" r="18" fill="{"#E8DCC0" if k < 3 else "#2A1A10"}" stroke="{INK}" stroke-width="4"/>')
    o.append(label(960, 250, "DÖRT YIL", 64, "#E8D6A8"))
    o.append(label(1380, 630, "WESSEX", 38, "#D8C4A0")); o.append(label(470, 650, "KATTEGAT", 38, "#D8C4A0"))
    return frame_svg("".join(o))

# ======================================================== B · harita masası
def coast(pts, fill, line=INK, w=6):
    d = "M" + " L".join(f"{x},{y}" for x, y in pts) + " Z"
    return f'<path d="{d}" fill="{fill}" stroke="{line}" stroke-width="{w}" stroke-linejoin="round"/>'

def stil_B():
    o = [wood_grain(0, 0, W, H, "#2E1C10", "#140A04", seed=3, n=40)]
    # parşömen
    par = "M180,140 L1760,120 Q1790,300 1770,520 Q1800,760 1750,960 L170,980 Q140,760 175,540 Q150,320 180,140 Z"
    o.append(f'<path d="{par}" fill="#000" opacity="0.5" transform="translate(16,20)"/><path d="{par}" fill="#E2CFA2" stroke="#6A4A28" stroke-width="6"/>')
    r = random.Random(9)
    for i in range(120): o.append(f'<circle cx="{r.uniform(200,1740):.0f}" cy="{r.uniform(150,950):.0f}" r="{r.uniform(10,60):.0f}" fill="#B89A60" opacity="{r.uniform(0.04,0.12):.2f}"/>')
    sea = "#B9B593"
    o.append(f'<path d="{par}" fill="{sea}" opacity="0.35"/>')
    # İngiltere (sol) ve İskandinavya (sağ) kaba kıyılar
    o.append(coast([(300, 200), (420, 180), (470, 300), (520, 380), (560, 520), (610, 640), (640, 780), (560, 850), (430, 880), (330, 900), (360, 780), (300, 700), (340, 600), (280, 480), (320, 380), (270, 300)], "#CDBB8A", "#5A3E22", 5))
    o.append(coast([(1240, 150), (1480, 140), (1640, 170), (1700, 320), (1660, 520), (1560, 640), (1480, 700), (1400, 620), (1330, 520), (1360, 420), (1290, 330)], "#CDBB8A", "#5A3E22", 5))
    o.append(coast([(1300, 720), (1420, 740), (1450, 860), (1360, 950), (1260, 930), (1240, 820)], "#CDBB8A", "#5A3E22", 5))   # Jutland/Danimarka
    for i in range(14):   # dalga işaretleri
        x, y = r.uniform(720, 1180), r.uniform(220, 880)
        o.append(f'<path d="M{x:.0f},{y:.0f} q12,-10 24,0 q12,10 24,0" stroke="#6A5A3A" stroke-width="3" fill="none" opacity="0.6"/>')
    # rota (kesik çizgi) ve gemi
    o.append(f'<path d="M1330,600 Q960,420 620,560" stroke="#8A2A22" stroke-width="6" fill="none" stroke-dasharray="18 12"/>')
    o.append(ship(900, 500, 0.6, "#6A4428", "#9A2A22"))
    # Kattegat: ev + alev, Wessex: haç işaretli ev
    o.append(hall(1420, 610, 0.55)); o.append(flames(1420, 535, 0.5))
    o.append(hall(560, 700, 0.5, "#8A6A44", "#5A4028")); o.append(f'<path d="M560,560 L560,610 M544,578 L576,578" stroke="{INK}" stroke-width="6"/>')
    o.append(label(1420, 670, "Kattegat", 34, "#3A2614", "Georgia", "middle", "bold"))
    o.append(label(560, 770, "Wessex", 34, "#3A2614", "Georgia", "middle", "bold"))
    o.append(label(960, 230, "Dört yıl", 52, "#5A2A1A"))
    # kartal mührü (balmumu)
    o.append(f'<circle cx="1610" cy="840" r="70" fill="#8A2A22" stroke="{INK}" stroke-width="5"/>' + eagle(1610, 846, 0.32, "#B8402E"))
    # pullar parşömen üstünde
    o.append(token(RG, 820, 760, 95)); o.append(token(ASLv, 1250, 380, 72))
    for i, (sp, mk) in enumerate([(UBBE, ""), (HVIT, ""), (SIG, snake_mark(46))]):
        o.append(token(sp, 1150 + i * 100, 500, 46, mark=mk))
    # masa üstü mumlar (köşe)
    o.append(candles(1700, 1000, 0.8, (True, False, False)))
    o.append(horn(120, 720, 0.8, 70)); o.append(seax(250, 1000, 0.8, -12)); o.append(coins(1840, 300, 8, 4))
    cx_, cy_ = 1560, 300   # pusula gülü
    o.append(f'<g transform="translate({cx_},{cy_})"><circle r="70" fill="none" stroke="#6A4A28" stroke-width="4"/><circle r="56" fill="none" stroke="#6A4A28" stroke-width="2" stroke-dasharray="6 6"/>'
             + "".join(f'<path d="M0,-86 L12,-12 L0,0 L-12,-12 Z" fill="{"#8A2A22" if k == 0 else "#6A4A28"}" stroke="{INK}" stroke-width="3" transform="rotate({k*90})"/>' for k in range(4)) + '</g>')
    o.append(runes(1000, 150, 22, 0.6, "#6A4A28", 8))
    return frame_svg("".join(o))

# ======================================================== C · duvar halısı (dokuma)
def stil_C():
    weave = ('<pattern id="weave" width="8" height="8" patternUnits="userSpaceOnUse"><rect width="8" height="8" fill="#D9C8A0"/>'
             '<path d="M0,2 H8 M0,6 H8" stroke="#C6B486" stroke-width="2"/><path d="M2,0 V8 M6,0 V8" stroke="#E8DABA" stroke-width="1.2" opacity="0.7"/></pattern>'
             '<filter id="cloth"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="3"/><feColorMatrix values="0 0 0 0 0.3  0 0 0 0 0.22  0 0 0 0 0.12  0 0 0 0.35 0"/><feComposite in2="SourceGraphic" operator="in"/></filter>'
             '<filter id="stitch"><feTurbulence type="turbulence" baseFrequency="0.25 1.6" numOctaves="1" seed="5"/><feDisplacementMap in="SourceGraphic" scale="3"/></filter>')
    o = [wood_grain(0, 0, W, H, "#4A3424", "#22160C", seed=5, n=30, vertical=True)]   # duvar tahtaları
    o.append('<path d="M120,80 Q960,60 1800,80" stroke="#3A2A1A" stroke-width="22" fill="none"/>')   # askı sırığı
    cloth = "M140,92 L1780,92 L1784,1000 Q1700,986 1620,1002 Q1500,984 1400,1000 Q1200,986 960,1000 Q700,984 520,1002 Q330,986 136,1000 Z"
    o.append(f'<path d="{cloth}" fill="#000" opacity="0.45" transform="translate(12,16)"/><path d="{cloth}" fill="url(#weave)"/>')
    o.append(f'<path d="{cloth}" fill="#000" filter="url(#cloth)"/>')
    o.append(f'<path d="{cloth}" fill="none" stroke="#7A2A22" stroke-width="40" opacity="0.92"/>')
    o.append(f'<path d="{cloth}" fill="none" stroke="#E8D6A8" stroke-width="4" stroke-dasharray="12 8" transform="translate(0,0)"/>')
    for x in range(180, 1760, 70):   # üst bant motifi (dokuma üçgenler)
        o.append(f'<path d="M{x},150 l22,-30 l22,30 Z" fill="#2E4A5E" stroke="#1A2A3A" stroke-width="3"/>')
        o.append(f'<path d="M{x},960 l22,-30 l22,30 Z" fill="#2E4A5E" stroke="#1A2A3A" stroke-width="3"/>')
    st = 'filter="url(#stitch)"'
    o.append(f'<g {st}>' + hall(450, 640, 1.0, "#8A5A32", "#5A3A20") + flames(450, 500, 0.95) + '</g>')
    o.append(f'<g {st}>' + ship(1400, 560, 0.95, "#5A3A20", "#8A2A22") + '</g>')
    for i in range(5): o.append(f'<path d="M{1240+i*60},{640+(i%2)*10} q15,-14 30,0 q15,14 30,0" stroke="#2E4A5E" stroke-width="7" fill="none" {st}/>')   # dokuma dalga
    o.append(f'<g {st}>' + eagle(960, 360, 0.8, "#B07A3A") + '</g>')
    o.append(f'<g {st}>' + candles(1520, 880, 0.75, (True, False, False), "#E8DCC0", INK, False) + '</g>')
    o.append(token(RG, 960, 650, 115, stitch=True)); o.append(token(ASLv, 720, 830, 76, stitch=True))
    for i, (sp, mk) in enumerate([(UBBE, ""), (HVIT, ""), (SIG, snake_mark(52))]):
        o.append(token(sp, 990 + i * 120, 840, 52, stitch=True, mark=mk))
    o.append(f'<path d="M560,560 Q900,430 1280,520" stroke="#7A2A22" stroke-width="8" fill="none" stroke-dasharray="14 10" {st}/>')
    o.append(label(960, 228, "DÖRT YIL", 58, "#7A2A22"))
    return frame_svg("".join(o), weave)

def render(name, svg):
    p = f"{OUT}/{name}.svg"; open(p, "w").write(svg)
    subprocess.run(["rsvg-convert", "-w", str(W), "-h", str(H), p, "-o", f"{OUT}/{name}.png"], check=True)

if __name__ == "__main__":
    import os; os.makedirs(OUT, exist_ok=True)
    for n, f in [("stil_A", stil_A), ("stil_B", stil_B), ("stil_C", stil_C)]: render(n, f()); print(n)
    from PIL import Image, ImageDraw, ImageFont
    sheet = Image.new("RGB", (960, 3 * 560 + 10), "#EDE2CC"); d = ImageDraw.Draw(sheet)
    for i, n in enumerate(["stil_A", "stil_B", "stil_C"]):
        sheet.paste(Image.open(f"{OUT}/{n}.png").convert("RGB").resize((940, 528)), (10, 10 + i * 560))
    sheet.save(f"{OUT}/stil_kontakt_960.png")
