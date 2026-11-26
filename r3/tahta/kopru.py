"""Saga Tahtası köprüleri K1–K6 (stil A+B: oymalı meşe tahta, ortasına gömülü parşömen harita).
Pullar kayar, iplik gerilir, ikonlar pop-in ile belirir; zamanlama TTS satır başlangıçlarına kilitli.
python3 kopru.py kare      → tahta/K1..K6.png (statik, son durum) + kopru_kontakt_960.png
python3 kopru.py [K1 ..]   → tahta/out/K?.mp4 (ses dahil)
"""
import sys, math, random, os, subprocess
sys.path[:0] = ["/home/claude/r3/tahta", "/home/claude/r3", "/home/claude/r2", "/home/claude/r3/veda", "/home/claude/r3/veda2", "/home/claude/r3/ivar2",
                "/home/claude/r3/bedel", "/home/claude/r3/floki", "/home/claude/r3/kurul/test_ivar"]
import numpy as np, soundfile as sf, skia
from engine import sprite, draw, Writer, fill, vignette, col, lin, ease_io, ease_out, pop, fade, W, H, FPS
import tahta as T
from tahta import INK, token, snake_mark, knot_band, ship, hall, flames, eagle, candles, carved, label, wood_grain, horn, coins, seax, runes, COMMON_DEFS
from frames import RG, ASLv
from kareler import BJv, LAGv, full
from modeller import ROLLO, HORIK, BORG, GOLD_BAND
from model_af import ATH, FLO
import assets as A
OUT = "/home/claude/r3/tahta"; VOUT = f"{OUT}/out"; SES = f"{OUT}/ses"; SR = 24000
os.makedirs(VOUT, exist_ok=True)
ECBERT = dict(HORIK, hair="#6A5646", beard_c="#7E6C5A", beard_len=0.38, beard_w=0.72, iris="#5A7A8A", skin="#ECC8A6", tunic="#6A1E2A",
              cloak="#3A1A22", fur_collar="#D8CCB8", brow_c="#5A4636", brow_k=0.7, old=False, beard_braid=False)   # özgün tasarım: kısa sakal, altın bant
ATHv = dict(ATH, no_blush=True); FLOv = dict(FLO, no_blush=True)
UBBE, HVIT, SIG = T.UBBE, T.HVIT, T.SIG
from art3 import RAGNAR3
GISLA = dict(LAGv, hair="#3A2418", iris="#5A7A9A", skin="#F0D2BC", tunic="#2E3A7A", trim="#D8B04A", cloak="#5A1E2A", face_scar=False, knot=False, no_blush=True)   # Frank prensesi (yalnızca pul, özgün)
HARALD = dict(RAGNAR3, hair="#CFC3A0", beard_c="#CFC3A0", beard_len=1.0, beard_w=1.0, old=True, beard_braid=True, iris="#7A8A8A", skin="#E6C2A0",
              tunic="#4A1A1A", trim="#C9A25A", cloak="#1E1A18", fur_collar="#5A4A3A", face_scar=False, knot=False, armring=True, clasp="",
              brow_c="#9A8E70", brow_k=0.8, no_blush=True)   # bati/kareler5.py ile aynı (R8)
DEFS = A.defs(1.0) + f"<defs>{COMMON_DEFS}</defs>"

# ---------------------------------------------------------------- harita (B) tahtaya gömülü (A)
MAP = (330, 230, 1590, 860)   # x0, y0, x1, y1
P = {"paris": (880, 840), "kattegat": (1290, 470), "gotaland": (1470, 650), "danimarka": (1300, 760), "wessex": (560, 700), "nortumbria": (600, 420), "deniz": (930, 520)}

def coast(pts, fill="#CDBB8A", line="#5A3E22", w=5):
    return f'<path d="M' + " L".join(f"{x},{y}" for x, y in pts) + f' Z" fill="{fill}" stroke="{line}" stroke-width="{w}" stroke-linejoin="round"/>'

def board_svg():
    o = []
    o.append('<rect x="150" y="110" width="1620" height="880" rx="26" fill="#000" opacity="0.5" transform="translate(14,18)"/>')
    o.append(f'<clipPath id="board"><rect x="150" y="110" width="1620" height="880" rx="26"/></clipPath><g clip-path="url(#board)">{wood_grain(150, 110, 1620, 880, "#8A5A32", "#4A2C14", seed=7, n=90)}</g>')
    o.append(f'<rect x="150" y="110" width="1620" height="880" rx="26" fill="none" stroke="{INK}" stroke-width="10"/>')
    for a, b, c_, d in [(196, 152, 1724, 152), (196, 948, 1724, 948), (192, 156, 192, 944), (1728, 156, 1728, 944)]: o.append(knot_band(a, b, c_, d, "#B98A4E"))
    # gömülü harita: oyma yuva + parşömen
    x0, y0, x1, y1 = MAP
    o.append(f'<rect x="{x0-22}" y="{y0-22}" width="{x1-x0+44}" height="{y1-y0+44}" rx="10" fill="#3A2010" stroke="{INK}" stroke-width="6"/>')
    o.append(f'<rect x="{x0-10}" y="{y0-10}" width="{x1-x0+20}" height="{y1-y0+20}" rx="6" fill="none" stroke="#B98A4E" stroke-width="3" opacity="0.7"/>')
    par = f"M{x0},{y0} L{x1},{y0+6} Q{x1+6},{(y0+y1)/2} {x1-4},{y1} L{x0+4},{y1-4} Q{x0-6},{(y0+y1)/2} {x0},{y0} Z"
    o.append(f'<path d="{par}" fill="#E2CFA2"/>')
    r = random.Random(9)
    o.append(f'<clipPath id="mapc"><path d="{par}"/></clipPath><g clip-path="url(#mapc)">')
    for i in range(110): o.append(f'<circle cx="{r.uniform(x0,x1):.0f}" cy="{r.uniform(y0,y1):.0f}" r="{r.uniform(10,60):.0f}" fill="#B89A60" opacity="{r.uniform(0.04,0.12):.2f}"/>')
    o.append(f'<rect x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}" fill="#B9B593" opacity="0.32"/>')
    o.append(coast([(400, 250), (560, 240), (600, 330), (640, 420), (690, 540), (720, 660), (700, 790), (600, 850), (470, 870), (380, 860), (420, 760), (360, 680), (400, 590), (350, 480), (390, 380), (360, 300)]))   # Britanya
    o.append(coast([(1170, 240), (1420, 236), (1560, 270), (1590, 400), (1560, 560), (1520, 680), (1440, 720), (1380, 640), (1300, 560), (1230, 520), (1200, 420), (1150, 340)]))   # İskandinavya
    o.append(coast([(1250, 700), (1360, 710), (1380, 800), (1330, 860), (1240, 860), (1220, 780)]))   # Jutland
    o.append(coast([(730, 870), (750, 806), (830, 784), (930, 792), (1030, 806), (1130, 820), (1210, 870)]))   # Frankia kıyısı
    o.append('<path d="M860,792 Q880,812 870,832 Q860,850 890,866" stroke="#6A8AA0" stroke-width="5" fill="none"/>')   # Seine
    for i in range(16):
        x, y = r.uniform(780, 1130), r.uniform(280, 830)
        o.append(f'<path d="M{x:.0f},{y:.0f} q12,-10 24,0 q12,10 24,0" stroke="#6A5A3A" stroke-width="3" fill="none" opacity="0.55"/>')
    for nm, (x, y) in [("Kattegat", (1250, 600)), ("Götaland", (1490, 720)), ("Wessex", (560, 790)), ("Nortumbria", (560, 330)), ("Frankia", (1080, 852))]:
        o.append(f'<text x="{x}" y="{y}" font-family="Georgia" font-size="28" font-style="italic" fill="#5A3A1E" text-anchor="middle" opacity="0.85">{nm}</text>')
    o.append('</g>')
    o.append(f'<path d="{par}" fill="none" stroke="#6A4A28" stroke-width="5"/>')
    cx_, cy_ = 1530, 330   # pusula gülü (harita köşesi)
    o.append(f'<g transform="translate({cx_},{cy_}) scale(0.8)"><circle r="70" fill="none" stroke="#6A4A28" stroke-width="4"/><circle r="56" fill="none" stroke="#6A4A28" stroke-width="2" stroke-dasharray="6 6"/>'
             + "".join(f'<path d="M0,-86 L12,-12 L0,0 L-12,-12 Z" fill="{"#8A2A22" if k == 0 else "#6A4A28"}" stroke="{INK}" stroke-width="3" transform="rotate({k*90})"/>' for k in range(4)) + '</g>')
    # oyma kenar boşlukları: run bantları + köşe süsleri
    o.append(carved(runes(330, 890, 46, 0.62, "#3A2010", 3), 2))
    for x, y in [(240, 200), (1680, 200), (240, 900), (1680, 900)]:
        o.append(carved(f'<g transform="translate({x},{y})"><circle r="26" fill="#7A4E2A" stroke="{INK}" stroke-width="5"/><path d="M-14,-14 L14,14 M14,-14 L-14,14" stroke="{INK}" stroke-width="5"/><circle r="8" fill="#B98A4E" stroke="{INK}" stroke-width="3"/></g>', 2))
    # başlık yuvası (oyma plaka; yazı ayrı katman)
    o.append(f'<rect x="740" y="128" width="440" height="78" rx="12" fill="#5A3418" stroke="{INK}" stroke-width="6"/><rect x="752" y="140" width="416" height="54" rx="8" fill="none" stroke="#B98A4E" stroke-width="3"/>')
    return "".join(o)

BX, BY, BS = 486, 92, 0.76   # tahta → ekran dönüşümü (duvara asılı)
def wall_svg():
    r = random.Random(21); o = [f'<rect width="{W}" height="{H}" fill="#2A1A10"/>']
    x = 0
    while x < W:   # dikey ev tahtaları
        w_ = r.randint(90, 140); col_ = r.choice(["#4A3020", "#45301E", "#50341F", "#3F2A1A"])
        o.append(f'<rect x="{x}" y="0" width="{w_}" height="{H}" fill="{col_}" stroke="#1A0E06" stroke-width="5"/>')
        for k in range(7): o.append(f'<path d="M{x+r.uniform(10,w_-10):.0f},0 q{r.uniform(-14,14):.0f},{H/2} {r.uniform(-8,8):.0f},{H}" stroke="#24160C" stroke-width="{r.uniform(1.5,4):.1f}" fill="none" opacity="0.45"/>')
        o.append(f'<circle cx="{x+w_/2:.0f}" cy="150" r="6" fill="#1A0E06"/><circle cx="{x+w_/2:.0f}" cy="930" r="6" fill="#1A0E06"/>')
        x += w_
    o.append(f'<rect x="0" y="60" width="{W}" height="54" fill="#5A3A20" stroke="{INK}" stroke-width="6"/>' + knot_band(20, 87, 1900, 87, "#9A6A3A", 22))   # oymalı kiriş
    o.append(f'<rect x="0" y="990" width="{W}" height="90" fill="#22160C"/><path d="M0,990 H{W}" stroke="#120A04" stroke-width="8"/>')   # zemin
    for (x_, y_, c1, c2) in [(120, 360, "#8A2A22", "#D8C8A0"), (270, 300, "#2E4A5E", "#C9A25A")]:   # duvar kalkanları
        o.append(f'<g transform="translate({x_},{y_})"><circle r="92" fill="#000" opacity="0.35" transform="translate(10,12)"/><circle r="92" fill="{c1}" stroke="{INK}" stroke-width="7"/>'
                 + "".join(f'<path d="M0,0 L{92*math.cos(a):.0f},{92*math.sin(a):.0f}" stroke="{c2}" stroke-width="22"/>' for a in [k * math.pi / 3 for k in range(6)][::2])
                 + f'<circle r="92" fill="none" stroke="{INK}" stroke-width="7"/><circle r="24" fill="#8A8A82" stroke="{INK}" stroke-width="6"/></g>')
    for tx in (420, 1860):   # meşale yuvaları
        o.append(f'<g transform="translate({tx},420)"><rect x="-10" y="0" width="20" height="90" fill="#4A2E1A" stroke="{INK}" stroke-width="5"/><path d="M-26,0 h52 l-10,22 h-32 Z" fill="#6A6A62" stroke="{INK}" stroke-width="5"/></g>')
    o.append(f'<g transform="translate({BX},{BY}) scale({BS})">{board_svg()}</g>')
    o.append(f'<path d="M{BX+150*BS+200:.0f},{BY+110*BS:.0f} L{BX+960*BS:.0f},{BY-20} L{BX+1770*BS-200:.0f},{BY+110*BS:.0f}" stroke="#2A1A10" stroke-width="7" fill="none"/><circle cx="{BX+960*BS:.0f}" cy="{BY-20}" r="10" fill="#8A8A82" stroke="{INK}" stroke-width="4"/>')   # askı ipi
    return "".join(o)

def S(body, w, h, ax=None, ay=None):
    return sprite(body, w, h, ax, ay, 1.0, DEFS)

BASE = None
def base():
    global BASE
    if BASE is None: BASE = S(wall_svg(), W, H, 0, 0)
    return BASE

def tok(spec, r, expr="neutral", mark=""):
    pad = int(r * 0.3) + 10; d = 2 * (r + pad)
    return S(token(spec, r + pad, r + pad, r, expr=expr, mark=mark), d, d)

def ico(svg, w, h): return S(f'<g transform="translate({w/2},{h/2})">{svg}</g>', w, h)

def title_sp(txt):
    return S(label(220, 52, txt, min(44, int(520 / max(1, len(txt)))), "#F0DEB0"), 440, 78)

PLAGUE = ('<g>' + "".join(f'<circle cx="{x}" cy="{y}" r="{r_}" fill="#7A7A72" stroke="{INK}" stroke-width="4" opacity="0.92"/>' for x, y, r_ in
          [(-60, 10, 40), (-10, -20, 52), (50, 4, 42), (10, 30, 44), (-40, 36, 30)]) +
          '<path d="M-14,-24 a14,14 0 1 1 28,0 l-4,14 h-20 Z" fill="#E8DCC0" stroke="#1A1410" stroke-width="4"/><circle cx="-6" cy="-24" r="4" fill="#1A1410"/><circle cx="6" cy="-24" r="4" fill="#1A1410"/></g>')
RING = '<g><circle r="34" fill="none" stroke="#1A1410" stroke-width="16"/><circle r="34" fill="none" stroke="#D8B04A" stroke-width="9"/><circle cx="0" cy="-34" r="7" fill="#F0D88A" stroke="#1A1410" stroke-width="3"/></g>'
STONES = "".join(f'<g transform="rotate({k*45}) translate(0,-62)"><path d="M-12,14 L-10,-18 Q0,-26 10,-18 L12,14 Z" fill="#8A8A82" stroke="#1A1410" stroke-width="4"/></g>' for k in range(8)) + '<circle r="16" fill="#6A4428" stroke="#1A1410" stroke-width="4"/>'
CRACK = '<path d="M-20,-30 L0,-6 L-10,4 L12,30" stroke="#1A1410" stroke-width="7" fill="none"/>'
CHEST = ('<g><rect x="-50" y="-26" width="100" height="56" rx="6" fill="#6A4428" stroke="#1A1410" stroke-width="5"/><path d="M-50,-26 Q0,-70 50,-26" fill="#7A5232" stroke="#1A1410" stroke-width="5"/>'
         + "".join(f'<circle cx="{-30+k*15}" cy="{-32+(k%2)*6}" r="9" fill="#D8B04A" stroke="#1A1410" stroke-width="3"/>' for k in range(5)) + '<path d="M-50,2 H50" stroke="#8A8A82" stroke-width="6"/></g>')
CITY = ('<g><path d="M-60,30 L-60,-10 L-40,-10 L-40,-30 L-24,-30 L-24,-10 L24,-10 L24,-40 L40,-40 L40,-10 L60,-10 L60,30 Z" fill="#9A9488" stroke="#1A1410" stroke-width="5"/>'
        '<path d="M24,-40 L32,-60 L40,-40" fill="#5A4A3A" stroke="#1A1410" stroke-width="4"/><path d="M32,-60 V-76 M24,-70 H40" stroke="#D8B04A" stroke-width="4"/>'
        '<path d="M-14,30 V8 Q0,-6 14,8 V30" fill="#2A2018" stroke="#1A1410" stroke-width="4"/>' + "".join(f'<rect x="{x}" y="-18" width="8" height="8" fill="#1A1410"/>' for x in (-56, -44, 28, 44)) + '</g>')
CHAIN = "".join(f'<ellipse cx="{-48+k*24}" cy="0" rx="14" ry="9" fill="none" stroke="#1A1410" stroke-width="10" transform="rotate({(k%2)*90} {-48+k*24} 0)"/><ellipse cx="{-48+k*24}" cy="0" rx="14" ry="9" fill="none" stroke="#9A9A92" stroke-width="5" transform="rotate({(k%2)*90} {-48+k*24} 0)"/>' for k in range(5))
CROWN = '<g><path d="M-50,20 L-50,-20 L-26,4 L0,-30 L26,4 L50,-20 L50,20 Z" fill="#D8B04A" stroke="#1A1410" stroke-width="6"/><circle cx="0" cy="4" r="8" fill="#8E2A22" stroke="#1A1410" stroke-width="3"/></g>'
SCROLL = ('<g><rect x="-60" y="-34" width="120" height="68" fill="#E8DCB8" stroke="#1A1410" stroke-width="5"/><circle cx="-60" cy="0" r="12" fill="#C8B488" stroke="#1A1410" stroke-width="4"/>'
          '<circle cx="60" cy="0" r="12" fill="#C8B488" stroke="#1A1410" stroke-width="4"/><path d="M-36,-14 h70 M-36,0 h60 M-36,14 h50" stroke="#6A4A28" stroke-width="4"/>'
          '<circle cx="34" cy="20" r="12" fill="#8A2A22" stroke="#1A1410" stroke-width="3"/></g>')
CROSS = '<g><path d="M0,-50 V50 M-30,-18 H30" stroke="#1A1410" stroke-width="18" stroke-linecap="round"/><path d="M0,-50 V50 M-30,-18 H30" stroke="#C9A25A" stroke-width="9" stroke-linecap="round"/></g>'
SUN = ('<g>' + "".join(f'<path d="M0,-40 L8,-62 L-8,-62 Z" fill="#D8B04A" stroke="#1A1410" stroke-width="3" transform="rotate({k*30})"/>' for k in range(12)) +
       '<circle r="34" fill="#D8B04A" stroke="#1A1410" stroke-width="5"/><path d="M-14,-10 h28 M0,-24 v40 M-14,10 h28" stroke="#8A5A22" stroke-width="4"/></g>')
SHADOW = '<ellipse rx="100" ry="100" fill="#000" opacity="0.5"/>'

# ---------------------------------------------------------------- olay dili
def dur(k, i): return sf.info(f"{SES}/{k}_{i}.wav").duration
def bridge_plan(k):
    n = len([f for f in os.listdir(SES) if f.startswith(k + "_") and f.endswith(".wav")]); t = 0.6; st = []
    for i in range(n):
        st.append(t); t += dur(k, i) + (0.35 if i < n - 1 else 0)
    return st, t + 1.4

def P2(name, dx=0, dy=0): x, y = P[name]; return (x + dx, y + dy)

def slide(t, keys):
    """keys: [(t, x, y)] → konum (ease)."""
    if t <= keys[0][0]: return keys[0][1:]
    for (ta, xa, ya), (tb, xb, yb) in zip(keys, keys[1:]):
        if t <= tb: q = ease_io(lin(t, ta, tb)); return (xa + (xb - xa) * q, ya + (yb - ya) * q)
    return keys[-1][1:]

def thread(c, a, b, prog, colr="#B8322A", w=6, sag=40, gap=None):
    if prog <= 0: return
    (x0, y0), (x1, y1) = a, b; mx, my = (x0 + x1) / 2, max(y0, y1) + sag
    pts = []
    N = 40
    for i in range(int(N * min(1, prog)) + 1):
        q = i / N; pts.append(((1-q)**2*x0 + 2*(1-q)*q*mx + q*q*x1, (1-q)**2*y0 + 2*(1-q)*q*my + q*q*y1))
    for wid, cc, dy in ((w + 4, "#000000", 6), (w, colr, 0)):
        p = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=wid, Color4f=col(cc, 0.35 if cc == "#000000" else 1), StrokeCap=skia.Paint.kRound_Cap)
        path = skia.Path(); first = True
        for i, (x, y) in enumerate(pts):
            if gap and gap[0] < i / N < gap[1]: first = True; continue
            if first: path.moveTo(x + dy * 0.6, y + dy); first = False
            else: path.lineTo(x + dy * 0.6, y + dy)
        c.drawPath(path, p)

def popd(c, sp, x, y, t, t0, s=1.0, out=None):
    k = pop(t, t0) if t is not None else 1.0
    if out is not None and t is not None: k *= 1 - ease_io(lin(t, out, out + 0.4))
    draw(c, sp, x, y, s * k)

def shadow_under(c, x, y, r):
    p = skia.Paint(AntiAlias=True, Color4f=col("#000", 0.35), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 10))
    c.drawOval(skia.Rect(x - r + 8, y - r * 0.9 + 14, x + r + 8, y + r * 1.0 + 14), p)

def tokd(c, sp, x, y, t, t0, s=1.0, lift=False, flip=1.0, a=1.0):
    k = (pop(t, t0) if t is not None else 1.0)
    if k <= 0: return
    if lift: shadow_under(c, x, y, sp.w * 0.32 * k)
    draw(c, sp, x, y - (8 if lift else 0), s * k, sx=s * k * flip, sy=s * k, a=a)

def flame_flicker(c, sp, x, y, t, t0, s=1.0, out=None):
    if t is not None and t < t0: return
    a = 1.0 if out is None or t is None else 1 - ease_io(lin(t, out, out + 0.8))
    if a <= 0: return
    tt = 0 if t is None else t; g = pop(t, t0, 0.5) if t is not None else 1.0
    draw(c, sp, x, y, s * g * (1 + 0.04 * math.sin(tt * 13)), sy=s * g * (1 + 0.08 * math.sin(tt * 9 + 1)), a=a)
    p = skia.Paint(Color4f=col("#FF9A3A", 0.22 * a * g * (0.8 + 0.2 * math.sin(tt * 7))), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 60), BlendMode=skia.BlendMode.kScreen)
    c.drawCircle(x, y, 150 * s, p)

# sprite kütüphanesi
def L():
    return dict(rg=tok(RG, 74), rg_s=tok(RG, 60), asl=tok(ASLv, 58), rollo=tok(ROLLO, 58), horik=tok(HORIK, 62), borg=tok(BORG, 58),
                ubbe=tok(UBBE, 40), hvit=tok(HVIT, 40), sig=tok(SIG, 40, mark=snake_mark(40)), floki=tok(FLOv, 56), ecb=tok(ECBERT, 62), ath=tok(ATHv, 56),
                hall=ico(hall(0, 40, 0.5), 200, 140), fl=ico(flames(0, 60, 0.55), 220, 140), ship=ico(ship(0, 40, 0.55), 180, 150),
                eagle=ico(carved(eagle(0, 0, 0.62, "#7A5432")), 300, 220), plague=ico(PLAGUE, 200, 140), ring=ico(RING, 90, 100), stones=ico(STONES, 180, 180),
                crack=ico(CRACK, 60, 80), crown=ico(CROWN, 120, 70), scroll=ico(SCROLL, 160, 100), cross=ico(CROSS, 90, 120), sun=ico(SUN, 140, 140),
                harald=tok(HARALD, 66), city=ico(CITY, 140, 130), gisla=tok(GISLA, 52), chest=ico(CHEST, 120, 110), chain=ico(CHAIN, 140, 50),
                c3=ico(candles(0, 70, 0.7, (True, True, True)), 200, 140), c1=ico(candles(0, 70, 0.7, (True, False, False)), 200, 140))
LIB = {}

# ---------------------------------------------------------------- köprüler
def K1(c, t, st):
    l = LIB; s0, s1 = st
    draw(c, l["hall"], *P2("kattegat", 0, 20))
    tokd(c, l["horik"], *P2("danimarka", 60, 0), t, s0 + 0.1, lift=True)
    tokd(c, l["borg"], *P2("gotaland", 20, 0), t, s0 + 0.9, lift=True)
    x, y = slide(t if t is not None else 99, [(s0 + 0.4, *P2("kattegat", 0, -60)), (s0 + 1.8, *P2("gotaland", -110, -40)), (s1 - 0.1, *P2("gotaland", -110, -40)), (s1 + 0.9, *P2("kattegat", 0, -60))])
    if t is None or t > s0 + 0.9: thread(c, P2("danimarka", 60, 0), (x, y), 1 if t is None else lin(t, s0 + 0.9, s0 + 1.7), "#B8322A")
    tokd(c, l["rg"], x, y, t, 0.0, lift=True)
    popd(c, l["plague"], *P2("kattegat", 120, 70), t, s1 + 1.4)

def K2(c, t, st):
    l = LIB; s0, s1, s2 = st
    draw(c, l["hall"], *P2("kattegat", 0, 20)); tokd(c, l["borg"], *P2("gotaland", 20, 0), t, 0)
    snap = (0.48, 0.56) if t is None or t > s0 + 0.6 else None
    thread(c, P2("kattegat", -40, -60), P2("gotaland", 20, 0), 1.0, "#B8322A", gap=snap)
    tokd(c, l["rg"], *P2("kattegat", -40, -60), t, 0, lift=True)
    popd(c, l["ring"], *slide(t if t is not None else 99, [(s1 + 0.4, *P2("gotaland", 20, -90)), (s1 + 1.6, *P2("kattegat", 130, 40))]), t, s1 + 0.2)
    x, y = slide(t if t is not None else 99, [(s2 + 0.2, *P2("kattegat", 120, 40)), (s2 + 1.6, *P2("gotaland", -80, 60))])
    dim = 0 if t is None else lin(t, s2 + 0.2, s2 + 1.6)
    tokd(c, l["rollo"], x, y, t, 0, lift=True)
    if t is None or dim > 0:   # gölge: Ragnar'ın gölgesi Rollo'nun üstüne düşer
        p = skia.Paint(AntiAlias=True, Color4f=col("#000", 0.35 * (1 if t is None else dim)), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 12)); c.drawCircle(x, y, 66, p)

def K3(c, t, st):
    l = LIB; s0, s1 = st
    draw(c, l["hall"], *P2("kattegat", 0, 20))
    popd(c, l["stones"], *P2("kattegat", -200, 40), t, s0 + 0.1)
    x, y = slide(t if t is not None else 99, [(s0 + 0.3, *P2("kattegat", -200, 40)), (s0 + 1.6, *P2("kattegat", 120, 40))])
    thread(c, P2("kattegat", -40, -60), (x, y), 1 if t is None else lin(t, s0 + 1.4, s0 + 2.2), "#B8322A")
    popd(c, l["crack"], *P2("kattegat", 50, 10), t, s0 + 2.3)
    tokd(c, l["rg"], *P2("kattegat", -40, -60), t, 0, lift=True); tokd(c, l["rollo"], x, y, t, 0, lift=True)
    ax, ay = slide(t if t is not None else 99, [(s1 + 0.2, 1700, 560), (s1 + 1.8, *P2("kattegat", 150, -150))])
    tokd(c, l["asl"], ax, ay, t, s1 + 0.1, lift=True)

def K4(c, t, st):
    l = LIB; s0, s1, s2, s3, s4, s5 = st
    burn = s2 + 1.4
    draw(c, l["hall"], *P2("kattegat", 0, 20))
    flame_flicker(c, l["fl"], *P2("kattegat", 0, -40), t, burn, 1.0, out=s3 + 0.4)
    if t is None or t < s3 + 0.8: tokd(c, l["borg"], *P2("kattegat", 150, -40), t, burn - 0.4)
    tokd(c, l["asl"], *P2("kattegat", -130, 60), t, s0 + 0.2, lift=True)
    for i, (key, dt) in enumerate([("ubbe", 1.6), ("hvit", 2.3), ("sig", 3.0)]):
        tokd(c, l[key], *P2("kattegat", -60 + i * 90, 150), t, s1 + dt)
    sx, sy = slide(t if t is not None else 99, [(s2 + 0.1, *P2("kattegat", -150, -100)), (s2 + 1.6, *P2("wessex", 60, -90)), (s3 + 0.1, *P2("wessex", 60, -90)), (s3 + 1.2, *P2("kattegat", -150, -100))])
    if t is not None and s2 < t < s3 + 1.3:
        thread(c, P2("kattegat", -150, -100), (sx, sy), 1.0, "#8A2A22", 5, 60)
    draw(c, l["ship"], sx, sy + 60, 0.9)
    tokd(c, l["rg_s"], sx, sy - 10, t, 0, lift=True)
    popd(c, l["eagle"], 960, 330, t, s3 + 1.2)
    if t is None or t < s5 + 0.3: popd(c, l["c3"], 1460, 800, t, s4 + 0.4)
    else: draw(c, l["c1"], 1460, 800)
    if t is not None and s5 + 0.3 < t < s5 + 1.6:   # sönen mum dumanı
        p = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=4, Color4f=col("#BBBBBB", 0.6 * (1 - lin(t, s5 + 0.3, s5 + 1.6))))
        for dx in (0, 49):
            path = skia.Path(); path.moveTo(1460 + dx, 742); path.quadTo(1450 + dx, 700 - 30 * lin(t, s5, s5 + 1.6), 1466 + dx, 660 - 40 * lin(t, s5, s5 + 1.6)); c.drawPath(path, p)

def K5(c, t, st):
    l = LIB; s0, s1, s2 = st
    draw(c, l["hall"], *P2("kattegat", 0, 20))
    tokd(c, l["rg"], *P2("kattegat", -60, -80), t, 0, lift=True)
    hx, hy = P2("danimarka", 140, -10)
    if t is None or t > s0:
        p = skia.Paint(AntiAlias=True, Color4f=col("#000", 0.4 * (1 if t is None else lin(t, s0, s0 + 0.8))), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 30)); c.drawCircle(hx, hy, 120, p)
    tokd(c, l["horik"], hx, hy, t, s0 + 0.1, lift=True)
    fx, fy = slide(t if t is not None else 99, [(s1 + 0.3, *P2("kattegat", 110, 30)), (s1 + 1.6, *P2("danimarka", 30, -110))])
    thread(c, (hx, hy), (fx, fy), 1 if t is None else lin(t, s1, s1 + 0.6), "#5A5A5A")
    flip = 1.0 if t is None or t < s2 + 0.3 else math.cos(math.pi * min(1, lin(t, s2 + 0.3, s2 + 0.9)))
    flip = -1.0 if t is None else flip
    if t is None or t > s2 + 0.9: thread(c, (fx, fy), P2("kattegat", -60, -80), 1 if t is None else lin(t, s2 + 0.9, s2 + 1.6), "#D8B04A")
    tokd(c, l["floki"], fx, fy, t, 0, lift=True, flip=flip if abs(flip) > 0.05 else 0.05)

def K6(c, t, st):
    l = LIB; s0, s1, s2 = st
    draw(c, l["hall"], *P2("kattegat", 0, 20))
    sx, sy = slide(t if t is not None else 99, [(s0 + 0.1, *P2("kattegat", -150, -100)), (s0 + 1.8, *P2("wessex", 150, -60))])
    draw(c, l["ship"], sx, sy + 60, 0.9); tokd(c, l["rg_s"], sx, sy - 10, t, 0, lift=True); popd(c, l["crown"], sx, sy - 90, t, s0 + 0.2, 0.7)
    ex, ey = P2("wessex", -60, 20); tokd(c, l["ecb"], ex, ey, t, s1 + 0.1, lift=True)
    popd(c, l["scroll"], *slide(t if t is not None else 99, [(s1 + 0.6, ex + 40, ey - 100), (s1 + 1.6, sx + 90, sy + 10)]), t, s1 + 0.5)
    popd(c, l["cross"], 820, 430, t, s2 + 0.2); popd(c, l["sun"], 1080, 430, t, s2 + 0.4, 0.8)
    q = 0 if t is None else math.sin(max(0, t - s2 - 0.6) * 2.4) * min(1, max(0, t - s2 - 0.6))
    tokd(c, l["ath"], 950 + 90 * q, 450, t, s2 + 0.1, lift=True)

EXPR = {"K7": ["curious"], "K8": ["cold"], "K0": ["cold", "angry", "angry"], "K1": ["determined", "cold"], "K2": ["cold", "angry", "grief"], "K3": ["neutral", "curious"],
        "K4": ["neutral", "tender", "angry", "determined", "curious", "smug"], "K5": ["cold", "smug", "smug"], "K6": ["determined", "neutral", "curious"]}
sys.path.insert(0, "/home/claude/r3"); import ragnar_yas as YAS
_KEV = {"K0": YAS.RG1, "K8": YAS.RG3}
def ragnar(c, k, t, st):
    i = 0 if t is None else max([j for j, s0 in enumerate(st) if t >= s0 - 0.2] or [0])
    if t is None: i = len(st) - 1
    sp = full(_KEV.get(k, YAS.RG2), EXPR[k][i], 0.7, 1, "3q", 0.35, "", 1000, 1400)
    br = 1 + 0.006 * math.sin((t or 0) * 2.1)
    p = skia.Paint(AntiAlias=True, Color4f=col("#000", 0.45), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 14)); c.drawOval(skia.Rect(160, 990, 480, 1030), p)
    draw(c, sp, 330, 1010, 1.0, sx=1.0, sy=br)

def tally(c, t, t0, n=4):   # zaman atlaması: yere dayalı run taşı, çentikler sırayla
    if t is not None and t < t0: return
    k = 1.0 if t is None else pop(t, t0, 0.4)
    m = n if t is None else min(n, int((t - t0) / 0.28) + 1)
    lich = "".join(f'<circle cx="{x}" cy="{y}" r="{r_}" fill="#7E8A5A" opacity="0.7"/>' for x, y, r_ in ((-70, 90, 10), (-56, 100, 7), (80, 70, 9), (60, -70, 6)))
    marks = "".join(f'<path d="M{-56+i*30},{-6} L{-44+i*30},{74}" stroke="#E8DCC0" stroke-width="13" stroke-linecap="round"/><path d="M{-56+i*30},{-6} L{-44+i*30},{74}" stroke="#2A1A10" stroke-width="5" stroke-linecap="round"/>' for i in range(m))
    TL = LIB.setdefault(f"tally{m}", S('<g transform="translate(150,170)"><path d="M-130,130 L-120,10 Q-110,-90 -20,-122 Q70,-140 112,-60 Q132,0 128,130 Z" fill="#8A8A80" stroke="#1A1410" stroke-width="7"/>'
        '<path d="M-96,40 Q-90,-80 0,-100 Q90,-104 100,20" stroke="#5E5E56" stroke-width="16" fill="none"/><path d="M-96,40 Q-90,-80 0,-100 Q90,-104 100,20" stroke="#B8322A" stroke-width="5" fill="none" stroke-dasharray="16 10"/>'
        + lich + marks + '</g>', 300, 310))
    draw(c, TL, 560, 862, 0.9 * k)

def K0(c, t, st):
    l = LIB; s0, s1, s2 = st; T_ = t if t is not None else 99
    draw(c, l["hall"], *P2("kattegat", -140, 30))
    hx, hy = P2("kattegat", -150, -90); rx, ry = P2("kattegat", 140, -90)
    if t is None or t > s1:
        p = skia.Paint(AntiAlias=True, Color4f=col("#000", 0.4 * (1 if t is None else lin(t, s1, s1 + 0.8))), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 30)); c.drawCircle(hx, hy, 120, p)
    tokd(c, l["harald"], hx, hy, t, 0.0, lift=True)
    popd(c, l["chest"], *slide(T_, [(s0 + 0.4, rx, ry + 110), (s0 + 1.8, hx + 10, hy + 110)]), t, s0 + 0.1)
    thread(c, (hx, hy), (rx, ry), 1 if t is None else lin(t, s1 + 0.2, s1 + 1.0), "#8A2A22")
    tokd(c, l["rg"], rx, ry, t, 0.0, lift=True)
    ox, oy = P2("kattegat", 260, 80); tokd(c, l["rollo"], ox, oy, t, s2 + 0.05, lift=True); popd(c, l["chain"], ox, oy + 10, t, s2 + 0.6)
    draw(c, l["hall"], *P2("kattegat", 150, 110), 0.8); flame_flicker(c, l["fl"], *P2("kattegat", 150, 60), t, s2 + 1.9, 0.75)

def K7(c, t, st):
    l = LIB; s0 = st[0]
    draw(c, l["hall"], *P2("kattegat", 0, 20))
    tokd(c, l["ath"], *P2("kattegat", -120, -80), t, 0.0, lift=True)
    popd(c, l["city"], *P2("paris", 0, -40), t, s0 + 1.6)
    thread(c, P2("kattegat", -120, -80), P2("paris", 0, -60), 1 if t is None else lin(t, s0 + 0.6, s0 + 1.8), "#D8B04A", 6, 120)

def K8(c, t, st):
    l = LIB; s0 = st[0]
    draw(c, l["city"], *P2("paris", 0, -40))
    rx, ry = slide(t if t is not None else 99, [(s0 + 0.2, *P2("kattegat", 60, -60)), (s0 + 1.4, *P2("paris", -110, -120))])
    tokd(c, l["rollo"], rx, ry, t, 0.0, lift=True)
    tokd(c, l["gisla"], *P2("paris", 90, -130), t, s0 + 1.8, lift=True)
    popd(c, l["crown"], *P2("paris", 90, -230), t, s0 + 2.3, 0.7)
    thread(c, (rx, ry), P2("paris", 90, -130), 0 if t is not None and t < s0 + 2.0 else (1 if t is None else lin(t, s0 + 2.0, s0 + 2.6)), "#D8B04A", 5, 20)

KS = {"K7": (K7, "PARİS"), "K8": (K8, "ROLLO"), "K0": (K0, "JARL HARALDSON"), "K1": (K1, "GÖTALAND"), "K2": (K2, "İHANET"), "K3": (K3, "MECLİS"), "K4": (K4, "DÖRT YIL"), "K5": (K5, "KRAL HORİK"), "K6": (K6, "WESSEX")}

def frame(c, k, t, st, tot):
    if not LIB: LIB.update(L())
    draw(c, base(), 0, 0)
    for tx in (420, 1860):   # meşale alevi + titreyen ışık
        tt = t or 0; draw(c, LIB.setdefault("torch", ico(flames(0, 60, 0.32), 140, 100)), tx, 400, 1.0, sy=1 + 0.08 * math.sin(tt * 11 + tx))
        p = skia.Paint(Color4f=col("#FF9A3A", 0.18 + 0.04 * math.sin(tt * 7 + tx)), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 90), BlendMode=skia.BlendMode.kScreen); c.drawCircle(tx, 400, 260, p)
    c.save(); c.translate(BX, BY); c.scale(BS, BS)
    f, ttl = KS[k]; draw(c, title_sp(ttl), 960, 167, 1.0, a=1.0 if t is None else fade(t, 0.1, 0.5))
    f(c, t, st); c.restore()
    if k == "K4": tally(c, t, st[0] + 0.2)
    ragnar(c, k, t, st)
    # sıcak mum ışığı + vinyet + letterbox
    p = skia.Paint(Color4f=col("#FFB060", 0.07), BlendMode=skia.BlendMode.kScreen); c.drawRect(skia.Rect(0, 0, W, H), p)
    vignette(c, 0.6)
    c.drawRect(skia.Rect(0, 0, W, 70), skia.Paint(Color4f=col("#000"))); c.drawRect(skia.Rect(0, H - 70, W, H), skia.Paint(Color4f=col("#000")))

# ---------------------------------------------------------------- ses
def mix(k, st, tot, path):
    N = int(tot * SR); tt = np.arange(N) / SR; rng = np.random.default_rng(11)
    lp = lambda x, n: np.convolve(x, np.ones(max(1, int(n))) / max(1, int(n)), mode="same").astype(np.float32)
    def put(buf, a, s): i = int(s * SR); e = min(N, i + len(a)); buf[i:e] += a[:e - i]
    voice = np.zeros(N, np.float32)
    for i, s in enumerate(st):
        a, _ = sf.read(f"{SES}/{k}_{i}.wav", dtype="float32"); put(voice, a / (np.abs(a).max() + 1e-6) * 0.8, s)
    vact = np.clip(lp((np.abs(voice) > 0.02).astype(np.float32), 0.35 * SR) * 3, 0, 1); duck = 1 - 0.55 * vact
    def tock(s, amp=0.25):   # ahşap pul sesi
        n = int(0.12 * SR); x = np.arange(n) / SR
        put(sfx, ((np.sin(2 * np.pi * 420 * x) + 0.5 * np.sin(2 * np.pi * 860 * x)) * np.exp(-x * 45) * amp).astype(np.float32), s)
    def scrape(s, d, amp=0.06):
        n = int(d * SR); put(sfx, lp(rng.standard_normal(n).astype(np.float32), 6) * np.sin(np.linspace(0, np.pi, n)) * amp, s)
    sfx = np.zeros(N, np.float32)
    for s in st: tock(s + 0.15, 0.18)
    for s in st[1:]: scrape(s + 0.3, 1.2)
    drone = np.zeros(N, np.float32); f0 = {"K7": 110.0, "K8": 87.3, "K0": 92.5, "K1": 98.0, "K2": 92.5, "K3": 103.8, "K4": 87.3, "K5": 92.5, "K6": 110.0}[k]
    ph = 2 * np.pi * np.cumsum(f0 * (1 + 0.004 * np.sin(2 * np.pi * 4.5 * tt))) / SR
    drone[:] = sum(np.sin(j * ph) / j ** 1.4 for j in range(1, 7)) * 0.04 * np.minimum(1, tt / 1.2) * np.minimum(1, (tot - tt) / 1.4)
    room = lp(rng.standard_normal(N).astype(np.float32), 50) * 0.25
    if k == "K4":
        b0 = st[2] + 1.4; fire = lp(rng.standard_normal(N).astype(np.float32), 30) * np.interp(tt, [0, b0, b0 + 0.6, st[3] + 0.4, st[3] + 1.2, tot], [0, 0, 1.0, 1.0, 0, 0]).astype(np.float32)
        room += fire * 0.6
        n = int(0.4 * SR); x = np.arange(n) / SR; put(sfx, lp(rng.standard_normal(n).astype(np.float32), 3) * np.exp(-x * 9) * 0.12, st[5] + 0.3)   # mum söner
    out = voice + duck * (drone + room * 0.15) + sfx
    out *= np.minimum(1, (tot - tt) / 0.8) * np.minimum(1, tt / 0.3)
    sf.write(path + ".raw.wav", out / (np.abs(out).max() + 1e-6) * 0.9, SR)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", path + ".raw.wav", "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "48000", "-ac", "2", path], check=True)
    os.remove(path + ".raw.wav")

def render(k):
    st, tot = bridge_plan(k); mix(k, st, tot, f"{VOUT}/{k}.wav")
    surf = skia.Surface(W, H); c = surf.getCanvas(); tmp = f"{VOUT}/{k}_tmp.mp4"; wr = Writer(tmp); n = int(round(tot * FPS))
    for f in range(n):
        t = f / FPS; c.clear(skia.ColorBLACK)
        z = 1.0 + 0.03 * ease_io(t / tot)   # yavaş itme
        c.save(); c.translate(W / 2, H / 2); c.scale(z, z); c.translate(-W / 2, -H / 2); frame(c, k, t, st, tot); c.restore()
        if f < 8: fill(c, "#000", 1 - f / 8)
        if f >= n - 10: fill(c, "#000", (f - (n - 10)) / 10)
        wr.write(surf)
    wr.close()
    out = f"{VOUT}/{k}.mp4"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", tmp, "-i", f"{VOUT}/{k}.wav", "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", out + ".tmp.mp4"], check=True)
    os.replace(out + ".tmp.mp4", out); os.remove(tmp); return tot

def stills():
    from PIL import Image
    fake = {"K0": [0, 3, 6], "K7": [0], "K8": [0], "K1": [0, 3], "K2": [0, 2, 5], "K3": [0, 3], "K4": [0, 2, 6, 10, 13, 16], "K5": [0, 3, 6], "K6": [0, 3, 6]}
    surf = skia.Surface(W, H); c = surf.getCanvas()
    for k in KS:
        c.clear(skia.ColorBLACK); frame(c, k, None, fake[k], 0); surf.makeImageSnapshot().save(f"{OUT}/{k}.png", skia.kPNG)
    sheet = Image.new("RGB", (960 * 2 + 30, 560 * 5 + 10), "#EDE2CC")
    for i, k in enumerate(KS): sheet.paste(Image.open(f"{OUT}/{k}.png").convert("RGB").resize((960, 540)), (10 + (i % 2) * 970, 10 + (i // 2) * 560))
    sheet.save(f"{OUT}/kopru_kontakt_960.png")

if __name__ == "__main__":
    if sys.argv[1:2] == ["kare"]: stills(); sys.exit()
    for k in (sys.argv[1:] or list(KS)): print(k, round(render(k), 2))
