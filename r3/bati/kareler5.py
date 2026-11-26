"""I · Batı: Sahne 1–5 ham kareleri (örgü onayı 20.11). Born in Lore dili: isim kartları, düşünce balonu, karakter hep kadrajda.
R8–R12: kimlik tek kaynak, zemin altta, sert iklim, model gövdeleri, kalabalık 2–3 modelden rastgele, gerçek modeller.
python3 kareler5.py [e1..e8] → bati/<id>.png, kontakt5_960.png
"""
import sys, math, random
sys.path[:0] = ["/home/claude/r3", "/home/claude/r2", "/home/claude/r3/veda", "/home/claude/r3/veda2", "/home/claude/r3/kesis", "/home/claude/r3/bedel",
                "/home/claude/r3/floki", "/home/claude/r3/ivar2", "/home/claude/r3/kurul/test_ivar", "/home/claude/r3/bati"]
from kareler4 import *            # kareler3 + bedel yardımcıları (army, field, KL, P7, O7 ...)
from art3 import head3, figure, RAGNAR3
import importlib.util as _iu
_spec = _iu.spec_from_file_location('ivar_places', '/home/claude/r3/ivar2/places.py'); IPL = _iu.module_from_spec(_spec); _spec.loader.exec_module(IPL)
OUT = "/home/claude/r3/bati"
import gemi as G
EXP["laugh"] = EXP["laugh"]; EXP["pray"] = (-12, 10, 0.80, 0.10, "tremble", "")
HARALD = dict(RAGNAR3, hair="#CFC3A0", beard_c="#CFC3A0", beard_len=1.0, beard_w=1.0, old=True, beard_braid=True, iris="#7A8A8A", skin="#E6C2A0",
              tunic="#4A1A1A", trim="#C9A25A", cloak="#1E1A18", fur_collar="#5A4A3A", face_scar=False, knot=False, armring=True, clasp="",
              brow_c="#9A8E70", brow_k=0.8, no_blush=True)   # özgün: kül sarısı örgülü sakal, koyu kırmızı, siyah kürk (Horik'ten ayrışır)
MONK_H = ["#7A5636", "#3A2A1E", "#A0582E", "#8A8070", "#5A4030"]
def monk(seed):
    r = random.Random(seed); h = r.choice(MONK_H)
    return dict(ATHv, hair=h, beard_c=h, tunic="#5A4632", cloak="#4A3A2A", beard_len=r.uniform(0.0, 0.5), beardless=r.random() < 0.4, no_blush=True)

# ---------------------------------------------------------------- Born in Lore dili: isim kartı, düşünce balonu
def name_card(txt, sub=""):
    w = max(60 + 26 * len(txt), 40 + 11 * len(sub))
    s = (f'<g transform="translate({w/2+10},60) rotate(-3)"><rect x="{-w/2}" y="-34" width="{w}" height="{72 if sub else 62}" rx="6" fill="#EADBB4" stroke="{INK}" stroke-width="5"/>'
         f'<circle cx="0" cy="-34" r="9" fill="#B8322A" stroke="{INK}" stroke-width="3"/>'
         f'<text x="0" y="8" font-family="Georgia" font-weight="bold" font-size="34" fill="#2A1A10" text-anchor="middle" letter-spacing="2">{txt}</text>'
         + (f'<text x="0" y="30" font-family="Georgia" font-style="italic" font-size="18" fill="#6A4A28" text-anchor="middle">{sub}</text>' if sub else "") + '</g>')
    return sprite(s, w + 20, 130, None, None, 1.0)

def thought(inner, w=300, h=200):
    s = (f'<g transform="translate({w/2+20},{h/2+10})"><ellipse rx="{w/2}" ry="{h/2-10}" fill="#F4EAD6" stroke="{INK}" stroke-width="6"/>'
         f'<circle cx="{-w/2+30}" cy="{h/2+18}" r="18" fill="#F4EAD6" stroke="{INK}" stroke-width="5"/><circle cx="{-w/2+4}" cy="{h/2+50}" r="10" fill="#F4EAD6" stroke="{INK}" stroke-width="4"/>{inner}</g>')
    return sprite(s, w + 40, h + 90, None, None, 1.0)

QW = ('<text x="-60" y="26" font-family="Georgia" font-weight="bold" font-size="96" fill="#B8322A" text-anchor="middle">?</text>'
      '<path d="M90,0 H-10" stroke="#1A1410" stroke-width="14" stroke-linecap="round"/><path d="M90,0 H-10" stroke="#2E4A5E" stroke-width="7" stroke-linecap="round"/>'
      '<path d="M-6,-24 L-34,0 L-6,24" fill="none" stroke="#1A1410" stroke-width="10" stroke-linejoin="round"/>'
      '<text x="40" y="58" font-family="Georgia" font-size="26" fill="#2E4A5E" text-anchor="middle">BATI</text>')

def hide_map(x, y, s=1.0):
    """Duvarda gerili deri harita: doğuya kırmızı oklar (Jarl'ın akınları)."""
    return (f'<g transform="translate({x},{y}) scale({s})"><path d="M-170,-120 Q0,-140 170,-118 Q190,0 168,120 Q0,140 -172,118 Q-190,0 -170,-120 Z" fill="#C8A878" stroke="{INK}" stroke-width="7"/>'
            + "".join(f'<path d="M{a},{b} l-24,-18 M{a},{b} l-24,18" stroke="{INK}" stroke-width="5"/>' for a, b in ((-180, -110), (180, -110), (-180, 110), (180, 110)))
            + '<path d="M-120,-60 Q-60,-90 -20,-40 Q20,10 -40,60 Q-90,80 -120,40 Z" fill="#A88A5A" stroke="#5A3E22" stroke-width="4"/>'
            + "".join(f'<path d="M-20,{yy} Q60,{yy-30} 140,{yy}" stroke="#8A2A22" stroke-width="10" fill="none"/><path d="M128,{yy-18} L150,{yy} L128,{yy+16}" fill="#8A2A22"/>' for yy in (-50, 0, 50))
            + '</g>')

SUNBOARD = ('<g><ellipse cx="6" cy="16" rx="150" ry="58" fill="#000" opacity="0.35"/><ellipse rx="150" ry="56" fill="#9A6A3A" stroke="#1A1410" stroke-width="7"/>'
            + "".join(f'<ellipse rx="{r_}" ry="{r_*0.37:.0f}" fill="none" stroke="#5A3A1E" stroke-width="3"/>' for r_ in (40, 80, 120))
            + "".join(f'<path d="M0,0 L{140*math.cos(a):.0f},{52*math.sin(a):.0f}" stroke="#5A3A1E" stroke-width="2"/>' for a in [k * math.pi / 8 for k in range(16)])
            + '<path d="M-2,0 L-2,-90 L6,-90 L6,0 Z" fill="#6A4428" stroke="#1A1410" stroke-width="4"/><path d="M2,-4 L120,30" stroke="#000" stroke-width="10" opacity="0.35"/></g>')
SUNSTONE = ('<g><path d="M-40,-10 L-16,-46 L30,-40 L48,0 L22,40 L-26,36 Z" fill="#DDEAF0" fill-opacity="0.72" stroke="#1A1410" stroke-width="6" stroke-linejoin="round"/>'
            '<path d="M-16,-46 L-4,0 L22,40 M-4,0 L48,0 M-4,0 L-40,-10" stroke="#9ABACA" stroke-width="3"/><path d="M-26,-20 L-12,-34" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round"/></g>')

def ship_skeleton(x, y, s=1.0):
    o = [f'<g transform="translate({x},{y}) scale({s})">']
    o.append('<path d="M-420,0 Q0,60 420,0" stroke="#1A1410" stroke-width="30" fill="none"/><path d="M-420,0 Q0,60 420,0" stroke="#7A5232" stroke-width="20" fill="none"/>')   # omurga
    o.append('<path d="M420,0 Q470,-80 440,-200 Q460,-230 490,-220" stroke="#1A1410" stroke-width="24" fill="none"/><path d="M420,0 Q470,-80 440,-200 Q460,-230 490,-220" stroke="#7A5232" stroke-width="14" fill="none"/>')
    o.append('<path d="M-420,0 Q-470,-80 -440,-190" stroke="#1A1410" stroke-width="24" fill="none"/><path d="M-420,0 Q-470,-80 -440,-190" stroke="#7A5232" stroke-width="14" fill="none"/>')
    for k in range(-6, 7):   # kaburgalar
        xx = k * 58; hh = 150 - abs(k) * 12
        o.append(f'<path d="M{xx-hh*0.6:.0f},{-hh} Q{xx},{40-abs(k)*2} {xx+hh*0.6:.0f},{-hh}" stroke="#1A1410" stroke-width="16" fill="none"/><path d="M{xx-hh*0.6:.0f},{-hh} Q{xx},{40-abs(k)*2} {xx+hh*0.6:.0f},{-hh}" stroke="#9A6A3A" stroke-width="9" fill="none"/>')
    o.append('<path d="M-380,-90 Q0,-20 380,-96" stroke="#1A1410" stroke-width="18" fill="none"/><path d="M-380,-90 Q0,-20 380,-96" stroke="#B88A52" stroke-width="10" fill="none"/>')   # ilk kaplama tahtası
    for xx in (-300, 0, 300):   # sehpalar
        o.append(f'<path d="M{xx-50},120 L{xx},30 L{xx+50},120" stroke="#1A1410" stroke-width="16" fill="none"/><path d="M{xx-50},120 L{xx},30 L{xx+50},120" stroke="#5A3A20" stroke-width="9" fill="none"/>')
    r = random.Random(4)
    for k in range(40): o.append(f'<path d="M{r.uniform(-460,460):.0f},{r.uniform(110,150):.0f} q8,-8 18,0" stroke="#D8B884" stroke-width="4" fill="none"/>')   # talaş
    o.append('<g transform="translate(330,110) rotate(-20)"><rect x="-6" y="-80" width="12" height="90" fill="#5A3A20" stroke="#1A1410" stroke-width="4"/><path d="M-6,-80 Q-40,-90 -36,-56 L-6,-60 Z" fill="#A8B0B8" stroke="#1A1410" stroke-width="4"/></g>')   # keser
    o.append('</g>'); return "".join(o)

def storm_sea(t=0.0):
    r = random.Random(7); o = ['<defs><linearGradient id="sky5" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#141C26"/><stop offset="1" stop-color="#3A4A58"/></linearGradient></defs>',
                               f'<rect width="{W}" height="{H}" fill="url(#sky5)"/>']
    for k in range(14):
        o.append(f'<ellipse cx="{r.uniform(0,W):.0f}" cy="{r.uniform(60,360):.0f}" rx="{r.uniform(160,360):.0f}" ry="{r.uniform(40,90):.0f}" fill="#1E2832" opacity="{r.uniform(0.5,0.9):.2f}"/>')
    o.append('<path d="M1460,70 L1420,240 L1470,236 L1400,440" stroke="#EAF4FF" stroke-width="10" fill="none" stroke-linejoin="bevel"/><path d="M1460,70 L1420,240 L1470,236 L1400,440" stroke="#9AC8FF" stroke-width="26" fill="none" opacity="0.25"/>')
    for row, (yy, col_, amp) in enumerate([(560, "#2A3E4C", 40), (700, "#22343F", 60), (850, "#1A2A34", 80), (980, "#14222A", 70)]):
        d = f"M0,{H} L0,{yy} " + " ".join(f"Q{x+80},{yy-amp*(1+0.3*math.sin(x*0.01+row))} {x+160},{yy}" for x in range(0, W + 160, 160)) + f" L{W},{H} Z"
        o.append(f'<path d="{d}" fill="{col_}" stroke="#0E1820" stroke-width="5"/>')
        for x in range(40, W, 160): o.append(f'<path d="M{x},{yy-amp*0.8:.0f} q20,-14 40,-4" stroke="#C8DCE8" stroke-width="5" fill="none" opacity="0.6"/>')
    for k in range(160):
        x = r.uniform(0, W); y = r.uniform(0, H); o.append(f'<path d="M{x:.0f},{y:.0f} l-14,40" stroke="#A8BCCC" stroke-width="2" opacity="0.5"/>')
    return "".join(o)

def monastery():
    r = random.Random(3); o = ['<defs><linearGradient id="sky6" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9AA8B4"/><stop offset="1" stop-color="#D4D8D6"/></linearGradient></defs>',
                               f'<rect width="{W}" height="{H}" fill="url(#sky6)"/>', f'<rect y="520" width="{W}" height="200" fill="#6E8290"/>']
    o.append(f'<path d="M0,620 L700,560 Q900,540 1100,580 L{W},600 L{W},{H} L0,{H} Z" fill="#5E6A4A" stroke="#2A3020" stroke-width="6"/>')   # ada çimeni
    o.append(f'<path d="M0,760 Q500,720 960,740 Q1400,760 {W},730 L{W},{H} L0,{H} Z" fill="#7A6A52" stroke="#3A3020" stroke-width="5"/>')   # patika
    # kilise: taş duvar, yuvarlak kemerli pencereler, çan kulesi, haç
    o.append('<g transform="translate(1120,600)">')
    o.append('<rect x="-320" y="-220" width="560" height="220" fill="#9A9488" stroke="#1A1410" stroke-width="7"/>')
    for yy in range(-200, 0, 32):
        for xx in range(-320 + (yy // 32 % 2) * 30, 240, 60): o.append(f'<rect x="{xx}" y="{yy}" width="60" height="32" fill="none" stroke="#7A7468" stroke-width="2"/>')
    o.append('<path d="M-350,-210 L-40,-360 L270,-210 Z" fill="#5A4A3A" stroke="#1A1410" stroke-width="7"/>')
    for xx in (-230, -110, 10, 130): o.append(f'<path d="M{xx},-60 V-140 Q{xx+28},-176 {xx+56},-140 V-60 Z" fill="#2A2A30" stroke="#1A1410" stroke-width="5"/><path d="M{xx+28},-60 V-160" stroke="#5A5A60" stroke-width="3"/>')
    o.append('<rect x="240" y="-420" width="150" height="420" fill="#8E887C" stroke="#1A1410" stroke-width="7"/><path d="M226,-420 L315,-520 L404,-420 Z" fill="#5A4A3A" stroke="#1A1410" stroke-width="7"/>')
    o.append('<path d="M290,-300 V-360 Q315,-390 340,-360 V-300 Z" fill="#2A2A30" stroke="#1A1410" stroke-width="5"/><path d="M315,-520 V-610 M285,-580 H345" stroke="#1A1410" stroke-width="18"/><path d="M315,-520 V-610 M285,-580 H345" stroke="#D8B04A" stroke-width="9"/>')
    o.append('<path d="M-60,0 V-110 Q-20,-150 20,-110 V0 Z" fill="#4A3020" stroke="#1A1410" stroke-width="6"/></g>')
    o.append('<path d="M0,690 L560,640 L600,700 L0,760 Z" fill="#8A8476" stroke="#1A1410" stroke-width="6"/>')   # taş çit
    for k in range(9): o.append(f'<path d="M{40+k*62},{684-k*5} v-24" stroke="#5A5448" stroke-width="3"/>')
    for k in range(24): o.append(f'<ellipse cx="{r.uniform(0,W):.0f}" cy="{r.uniform(500,700):.0f}" rx="{r.uniform(160,400):.0f}" ry="{r.uniform(20,50):.0f}" fill="#E6EAEA" opacity="{r.uniform(0.15,0.35):.2f}"/>')   # sis
    o.append(O7.ground2(W, H, 840, seed=11))
    return "".join(o)

def shield_ring(cx, cy, rx, ry, front=True):
    o = []; r = random.Random(5)
    for k in range(22):
        a = math.pi * 2 * k / 22; x = cx + rx * math.cos(a); y = cy + ry * math.sin(a)
        if (math.sin(a) > 0) != front: continue
        c1, c2 = r.choice([("#8A2A22", "#D8C8A0"), ("#2E4A5E", "#C9A25A"), ("#3A5A34", "#D8C8A0"), ("#5A3A20", "#B8322A")])
        o.append(f'<g transform="translate({x:.0f},{y:.0f}) scale({0.45 + 0.15 * (math.sin(a) + 1) / 2:.2f})">{KL.shield_svg(c1, c2, style=k % 3)}</g>')
    return "".join(o)

RING_CHEST = ('<g><rect x="-150" y="-60" width="300" height="130" rx="8" fill="#6A4428" stroke="#1A1410" stroke-width="7"/><path d="M-150,-60 Q0,-170 150,-60" fill="#7A5232" stroke="#1A1410" stroke-width="7"/>'
              '<path d="M-150,0 H150 M-60,-60 V70 M60,-60 V70" stroke="#8A8A82" stroke-width="10"/>'
              + "".join(f'<ellipse cx="{-110+k*36}" cy="{-66+(k%2)*8}" rx="22" ry="12" fill="none" stroke="#1A1410" stroke-width="9"/><ellipse cx="{-110+k*36}" cy="{-66+(k%2)*8}" rx="22" ry="12" fill="none" stroke="#D8B04A" stroke-width="5"/>' for k in range(7))
              + '</g>')
RING_UP = '<g transform="translate(HX,HY)"><ellipse cx="0" cy="-40" rx="34" ry="34" fill="none" stroke="#1A1410" stroke-width="16"/><ellipse cx="0" cy="-40" rx="34" ry="34" fill="none" stroke="#D8B04A" stroke-width="9"/></g>'
SWORD_UP = ('<g transform="translate(HX,HY)"><path d="M0,10 L-14,-260" stroke="#1A1410" stroke-width="18" stroke-linecap="round"/><path d="M-2,-30 L-14,-260" stroke="#C8D0D8" stroke-width="10"/>'
            '<path d="M-36,-24 L32,-30" stroke="#1A1410" stroke-width="14" stroke-linecap="round"/><path d="M-36,-24 L32,-30" stroke="#8A7A5A" stroke-width="7"/></g>')
BOOK = '<g transform="translate(HX,HY)"><rect x="-56" y="-40" width="112" height="80" rx="6" fill="#6A1E1E" stroke="#1A1410" stroke-width="6"/><rect x="-30" y="-24" width="60" height="48" fill="none" stroke="#D8B04A" stroke-width="5"/><path d="M0,-18 V18 M-14,-4 H14" stroke="#D8B04A" stroke-width="5"/></g>'

def robe(s, facing=1, colr="#5A4632", w=1000, h=1300):
    """Keşiş cübbesi: model gövdesinin bacaklarını örten uzun etek + ip kemer (model ile aynı dönüşüm)."""
    return sprite(f'<g transform="translate({w/2},{h-60}) scale({s*facing},{s})"><path d="M-92,-300 Q-118,-150 -138,4 Q0,24 138,4 Q118,-150 92,-300 Z" fill="{colr}" stroke="{INK}" stroke-width="10"/>'
                  + "".join(f'<path d="M{x},-300 Q{x+6},-150 {x*1.3:.0f},0" stroke="{shade(colr, 0.7)}" stroke-width="6" fill="none"/>' for x in (-60, 0, 60)) +
                  f'<path d="M-96,-300 Q0,-284 96,-300" stroke="#C8B488" stroke-width="12" fill="none"/><path d="M30,-292 Q40,-220 26,-170" stroke="#C8B488" stroke-width="8" fill="none"/></g>', w, h, ax=w / 2, ay=h - 60, ss=1.0)

def G_fire(x, y, s=1.0):
    return f'<g transform="translate({x},{y}) scale({s})">' + "".join(f'<path d="M{dx-34},0 Q{dx-36},{-h*0.5} {dx},{-h} Q{dx+36},{-h*0.5} {dx+34},0 Z" fill="#E8742A" stroke="#1A1410" stroke-width="5"/><path d="M{dx-16},0 Q{dx-14},{-h*0.4} {dx},{-h*0.6} Q{dx+14},{-h*0.4} {dx+16},0 Z" fill="#FFD27A"/>' for dx, h in ((-90, 120), (-30, 190), (30, 150), (90, 110))) + '</g>'

def card_at(c, txt, x, y, sub="", s=1.0): draw(c, name_card(txt, sub), x, y, s)

# ================================================================= kareler
def e1():   # Jarl salonu: Haraldson yüksek koltukta, duvarda doğu okları; Ragnar ön planda düşünce balonu
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    draw(c, blurred(place(P7.greathall(0.8) + hide_map(1560, 330, 1.0)), 3), 0, 0, 1.0)
    army(c, "ragnar", [(860, 0.62, 9, 0.10)], t, seed0=40, facing=-1, x0=700, x1=1800)
    HS = full(HARALD, ex("smug", IF.blink_at(0.6)), 0.95, facing=-1, look=-0.3)
    with live(c, 1180, 960, phase=0.6, breathe=0.005):
        rim(c, HS, 1180, 960, 1.0, "#FFB070", dx=-5, dy=2, a=0.7); draw(c, HS, 1180, 960, 1.0); shade_side(c, HS, 1180, 960, 0.4, 1000, 1400, "#1A0E08")
    card_at(c, "JARL HARALDSON", 1180, 250)
    RGs = fig_bust(RG, ex("curious", IF.blink_at(0.2)), 0.6, 2.0)
    with live(c, 420, 1080, phase=0.2, breathe=0.006):
        rim(c, RGs, 420, 420, 1.0, "#FFB070", dx=4, dy=2, a=0.5); draw(c, RGs, 420, 420, 1.0); shade_side(c, RGs, 420, 420, 0.4, 600, 200, "#1A0E08")
    draw(c, thought(QW), 540, 200, 0.9)
    rays(c, 1320, 60, 105, 900, 10, 3, "#FFE0B0", 0.08, t or 0.0)
    glow(c, 960, 1000, 520, "#FF8A3A", 0.18); finish(c, cold=False, warm=0.05); return s

def e2():   # Gece: güneş tahtası + güneş taşı, ışık kırılır
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    draw(c, blurred(place(IPL.longhouse(0.5)), 6), 0, 0, 1.0)
    c.drawRect(skia.Rect(0, 0, W, H), skia.Paint(Color4f=col("#0A0E16", 0.45)))
    draw(c, svg_sprite(f'<rect x="300" y="820" width="1320" height="260" fill="#4A3020" stroke="{INK}" stroke-width="8"/><path d="M300,850 H1620" stroke="#2A1A10" stroke-width="5"/>'
                       f'<g transform="translate(1180,860)">{SUNBOARD}</g>' + candles_svg(1500, 830)
                       + "".join(f'<g transform="translate({x},{y}) scale(0.9)">{KL.shield_svg(a, b, style=k)}</g>' for k, (x, y, a, b) in enumerate([(1420, 300, "#8A2A22", "#D8C8A0"), (1640, 360, "#2E4A5E", "#C9A25A")]))
                       + '<path d="M1300,200 L1780,200" stroke="#3A2414" stroke-width="18"/>' + "".join(f'<path d="M{x},205 L{x+10},560" stroke="#1A1410" stroke-width="14"/><path d="M{x},205 L{x+10},560" stroke="#6A4428" stroke-width="7"/><path d="M{x-14},205 L{x},150 L{x+14},205 Z" fill="#A8B0B8" stroke="#1A1410" stroke-width="4"/>' for x in (1330, 1530, 1760))), 0, 0, 1.0)
    RGs = fig_bust(dict(RG, _arm_up=True, _hand_extra=f'<g transform="translate(HX,HY) scale(1.1)">{SUNSTONE}</g>'), ex("awe", IF.blink_at(0.3)), 0.3, 2.1)
    with live(c, 620, 1080, phase=0.3, breathe=0.006):
        rim(c, RGs, 620, 400, 1.0, "#FFD08A", dx=6, dy=0, a=0.6); draw(c, RGs, 620, 400, 1.0); shade_side(c, RGs, 620, 400, 0.5, 820, 300, "#0A0E16")
    rays(c, 860, 210, 62, 760, 14, 6, "#FFE6A8", 0.22, 0.0 if t is None else t); bloom_spot(c, 1180, 860, 160, "#FFE6A8", 0.35)
    for k in range(50): rr = random.Random(k); c.drawCircle(860 + rr.uniform(0, 360), 210 + rr.uniform(0, 640), rr.uniform(1.5, 3.5), skia.Paint(AntiAlias=True, Color4f=col("#FFF2C8", rr.uniform(0.3, 0.8))))   # taştan kırılan ışık
    bloom_spot(c, 860, 210, 120, "#FFF2C8", 0.5); bloom_spot(c, 1500, 760, 140, "#FFB060", 0.4)
    card_at(c, "GÜNEŞ TAŞI", 980, 130, s=0.8)
    finish(c, cold=True, warm=0.08); return s

def candles_svg(x, y):
    return (f'<g transform="translate({x},{y})"><rect x="-16" y="-90" width="32" height="90" fill="#E8DCC0" stroke="{INK}" stroke-width="5"/>'
            f'<path d="M-11,-92 Q-10,-118 0,-136 Q10,-118 11,-92 Z" fill="#F7A23A" stroke="{INK}" stroke-width="3"/></g>')

def e3():   # Floki'nin tersanesi: yarı kaplanmış uzun gemi, ejder başı oyulmuş, iskele, katran kazanı
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    draw(c, blurred(place(O7.kattegat4()), 5), 0, 0, 1.0)
    draw(c, svg_sprite(G.scaffold(1020, 790, 0.78) + G.longship(1020, 760, 0.78, built=0.58)), 0, 0, 1.0)
    FL = full(dict(FLOv, _arm_up=True, _hand_extra=AXE_HAND), ex("laugh", IF.blink_at(0.5)), 1.0, facing=1, look=0.6)
    with live(c, 250, 1040, phase=0.5, breathe=0.006, rot=1.0):
        draw(c, FL, 250, 1040, 1.0); shade_side(c, FL, 250, 1040, 0.35, 80, 420, "#1A2430")
    card_at(c, "FLOKİ", 260, 250, "gemi ustası")
    bloom_spot(c, 1020 + 620 * 0.78, 790 + 130 * 0.78, 90, "#FF9A3A", 0.45); snowfall(c, t, (0, 70, W, H - 70), 90)
    RGs = full(RG, ex("awe", IF.blink_at(0.2)), 0.92, facing=-1 if False else 1, look=-0.6)
    draw(c, RGs, 1800, 1040, 1.0); shade_side(c, RGs, 1800, 1040, 0.35, 1660, 1920, "#1A2430")
    finish(c, cold=True); return s

def e4():   # Fırtına: görkemli uzun gemi, çizgili yelken şişkin, kalkan sırası, kürekler; Floki pruvada güler, Ragnar kıçta dua eder
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]; tt = t or 0
    draw(c, place(storm_sea(tt)), 0, 0, 1.0)
    c.save(); c.translate(960, 760); c.scale(0.9, 0.9); c.rotate(-6 + 3 * math.sin(tt * 1.4)); c.translate(-960, -700)
    wet = "".join(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{rx*0.6:.0f}" fill="#000" opacity="0.13"/>' for x, y, rx in ((-120, -430, 60), (90, -330, 80), (200, -480, 40), (-40, -260, 50)))
    draw(c, svg_sprite(f'<g transform="translate(960,700) scale(1.12)">{G.mast_sail(2.1)}{wet}</g>'), 0, 0, 1.0)
    crew = [(KL.soldier_spec(60 + k, "ragnar"), x) for k, x in enumerate((700, 840, 1000, 1140))]
    for sp, x in crew: draw(c, full(dict(sp, _arm_up=False, _hand_extra=""), "pain", 0.9, facing=-1, look=-0.5), x, 760, 0.5)
    FL = full(dict(FLOv, _arm_up=True, _hand_extra=""), ex("laugh", IF.blink_at(0.5)), 0.6, facing=1, look=0.8)
    RGp = full(dict(RG, _carry_svg="<g/>"), ex("pray", IF.blink_at(0.2)), 0.6, facing=1, look=0.3)
    draw(c, FL, 1420, 720, 1.0); draw(c, RGp, 480, 740, 1.0)
    draw(c, svg_sprite(f'<g transform="translate(960,700) scale(1.12)">{G.hull(1.0, wet=True)}</g>'), 0, 0, 1.0)
    c.restore()
    r = random.Random(2); fg = []   # ön dalga + köpük + pruva serpintisi
    d = f"M0,{H} L0,880 " + " ".join(f"Q{x+80},{840 - 30 * math.sin(x * 0.02 + tt)} {x+160},880" for x in range(0, W + 160, 160)) + f" L{W},{H} Z"
    fg.append(f'<path d="{d}" fill="#14222A" stroke="#0A1418" stroke-width="5"/>')
    for k in range(60): fg.append(f'<circle cx="{r.uniform(0,W):.0f}" cy="{r.uniform(850,890):.0f}" r="{r.uniform(4,14):.0f}" fill="#DCEAF2" opacity="{r.uniform(0.4,0.8):.2f}"/>')
    for k in range(40): fg.append(f'<circle cx="{1640 + r.uniform(-60,120):.0f}" cy="{r.uniform(560,760):.0f}" r="{r.uniform(3,10):.0f}" fill="#E8F2F8" opacity="{r.uniform(0.4,0.9):.2f}"/>')
    draw(c, place("".join(fg)), 0, 0, 1.0)
    fill(c, "#BFD8FF", 0.08); glow(c, 1440, 260, 300, "#CFE4FF", 0.25); glow(c, 1420, 900, 260, "#CFE4FF", 0.18); glow(c, 1200, 560, 380, "#9AC8FF", 0.10)
    finish(c, cold=True); return s

def e5():   # Lindisfarne: sisli manastır, kaçışan keşişler, Viking adımları
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    draw(c, place(monastery()), 0, 0, 1.0)
    for k, (x, y, sc, f_, rot, kn) in enumerate([(860, 830, 0.64, 1, 5, False), (1020, 800, 0.56, 1, 7, False), (1500, 820, 0.6, -1, -4, False), (1270, 860, 0.68, -1, 0, True), (1660, 790, 0.5, 1, 6, False)]):
        sp = full(dict(monk(k * 5 + 2), **({"_kneel": 130, "_carry_svg": "<g/>"} if kn else {})), ["pain", "awe", "grief", "pray", "pain"][k], 0.9, facing=f_, look=0.6 * f_)
        p = skia.Paint(AntiAlias=True, Color4f=col("#000", 0.3), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 8)); c.drawOval(skia.Rect(x - 110 * sc, y - 14, x + 110 * sc, y + 14), p)
        c.save(); c.translate(x, y); c.rotate(rot); c.translate(-x, -y); draw(c, sp, x, y, sc)
        if not kn: draw(c, robe(0.9, f_), x, y, sc)
        c.restore()
    smoke = "".join(f'<circle cx="{1480 + k*14 + 30*math.sin(k):.0f}" cy="{300 - k*38}" r="{50 + k*7}" fill="#3A3A3A" opacity="{0.55 - k*0.04:.2f}"/>' for k in range(10))
    draw(c, place(smoke + G_fire(1420, 400, 1.1) + G_fire(960, 395, 0.7)), 0, 0, 1.0); glow(c, 1400, 380, 340, "#FF7A2A", 0.3)
    for k in range(40): rr = random.Random(k + 9); c.drawCircle(1300 + rr.uniform(0, 300), 120 + rr.uniform(0, 280), rr.uniform(2, 4), skia.Paint(AntiAlias=True, Color4f=col("#FFB040", rr.uniform(0.5, 1.0))))
    army(c, "ragnar", [(1080, 1.05, 4, 0.0)], t, seed0=7, facing=1, x0=-200, x1=700)
    draw(c, svg_sprite(f'<g transform="translate(1100,1000) rotate(-12)">{BOOK.replace("translate(HX,HY)", "translate(0,0) scale(1.2)")}</g><g transform="translate(1260,1010) rotate(80)"><rect x="-14" y="-60" width="28" height="60" fill="#E8DCC0" stroke="#1A1410" stroke-width="5"/></g>'), 0, 0, 1.0)
    card_at(c, "LINDISFARNE", 1180, 150, "793")
    finish(c, cold=True); return s

def e6():   # Athelstan sandığa/kitaba sarılmış, Ragnar baltayı indirir
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    draw(c, blurred(place(monastery()), 3), -300, -200, 1.3)
    AT = full(dict(ATHv, _kneel=130, _carry_svg=BOOK.replace("translate(HX,HY)", "translate(0,0)")), ex("pain", IF.blink_at(0.7)), 1.0, facing=-1, look=-0.6)
    draw(c, AT, 1300, 990, 0.95); shade_side(c, AT, 1300, 990, 0.35, 1100, 1500, "#1A2430")
    card_at(c, "ATHELSTAN", 1300, 420, "keşiş · senin dilini konuşuyor")
    RGs = fig_bust(dict(RG, _arm_up=True, _hand_extra=KL.BEARD_AXE), ex("curious", IF.blink_at(0.2)), 0.6, 1.7)
    with live(c, 600, 1080, phase=0.2, breathe=0.006):
        draw(c, RGs, 600, 560, 1.0); shade_side(c, RGs, 600, 560, 0.4, 800, 400, "#1A2430")
    bloom_spot(c, 760, 110, 70, "#F0F8FF", 0.6); bloom_spot(c, 1290, 640, 40, "#FFE6A0", 0.5)
    draw(c, place("".join(f'<path d="M{random.Random(k).uniform(0,W):.0f},{random.Random(k+99).uniform(70,H):.0f} l-10,34" stroke="#C8D8E4" stroke-width="2" opacity="0.5"/>' for k in range(160))), 0, 0, 1.0)
    fill(c, "#C8D2DC", 0.06)
    finish(c, cold=True); return s

def e7():   # Holmgang: kalkan çemberi, kalabalıkta Lagertha, Bjorn, Rollo
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    draw(c, blurred(place(O7.kattegat4()), 4), 0, 0, 1.0)
    army(c, "ragnar", [(760, 0.5, 14, 0.12), (840, 0.6, 11, 0.06)], t, seed0=21, facing=1, x0=40, x1=1880)
    for sp, x, y, f_ in ((LAGv, 360, 900, 1), (dict(BJv, _scale_child=True), 470, 910, 1), (ROLLO, 1560, 900, -1)):
        d_ = full(sp, "determined" if sp is not BJv else "awe", 0.9, facing=f_, look=0.6 * f_); draw(c, d_, x, y, 0.7 if sp is not ROLLO else 0.72)
    draw(c, svg_sprite(shield_ring(960, 860, 640, 200, front=False) + '<ellipse cx="960" cy="900" rx="560" ry="150" fill="#B8A07A" opacity="0.55"/><path d="M700,880 L1220,870 L1240,960 L680,970 Z" fill="#8A5A32" stroke="#1A1410" stroke-width="6" opacity="0.85"/>'), 0, 0, 1.0)
    HS = full(dict(HARALD, _arm_up=True, _hand_extra=SWORD_UP), ex("angry", IF.blink_at(0.6)), 0.95, facing=-1, look=-0.6)
    RGs = full(dict(RG, _arm_up=True, _hand_extra=KL.BEARD_AXE), ex("determined", IF.blink_at(0.2)), 0.95, facing=1, look=0.6)
    draw(c, RGs, 770, 930, 0.82); draw(c, HS, 1160, 930, 0.82)
    draw(c, svg_sprite(shield_ring(960, 860, 640, 200, front=True)), 0, 0, 1.0)
    card_at(c, "HOLMGANG", 960, 140, "kalkan çemberinde düello")
    finish(c, cold=True); return s

def e8():   # Yeni jarl: halkaları dağıtıyor (halka #2)
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    draw(c, blurred(place(P7.greathall(0.35)), 3), 0, 0, 1.0)
    draw(c, svg_sprite(f'<g transform="translate(1080,960)">{RING_CHEST}</g>'), 0, 0, 1.0)
    RGs = full(dict(RG, _arm_up=True, _hand_extra=RING_UP), ex("tender", IF.blink_at(0.2)), 1.0, facing=1, look=0.4)
    draw(c, RGs, 760, 1000, 1.0)
    for k, (x, f_) in enumerate(((1300, -1), (1500, -1), (1700, -1))):
        sp = full(dict(KL.soldier_spec(50 + k, "ragnar"), _kneel=130, _arm_up=False, _hand_extra="", _body_extra=""), "awe", 0.85, facing=f_, look=-0.4); rim(c, sp, x, 1010, 0.9, "#FFB070", dx=-4, dy=0, a=0.6); draw(c, sp, x, 1010, 0.9)
    bloom_spot(c, 700, 330, 120, "#FFE6A0", 0.45)
    for x_ in (1000, 1060, 1120, 1170): bloom_spot(c, x_, 895, 30, "#FFE6A0", 0.6)
    card_at(c, "JARL RAGNAR", 760, 150)
    glow(c, 960, 1000, 520, "#FF8A3A", 0.22); finish(c, cold=False, warm=0.05); return s

FR5 = {"e1": e1, "e2": e2, "e3": e3, "e4": e4, "e5": e5, "e6": e6, "e7": e7, "e8": e8}

def contact5(ids=tuple(FR5)):
    from PIL import Image
    sheet = Image.new("RGB", (960 * 2 + 30, 560 * 4 + 10), "#EDE2CC")
    for k, i in enumerate(ids): sheet.paste(Image.open(f"{OUT}/{i}.png").convert("RGB").resize((960, 540)), (10 + (k % 2) * 970, 10 + (k // 2) * 560))
    sheet.save(f"{OUT}/kontakt5_960.png")

if __name__ == "__main__":
    ids = sys.argv[1:] or list(FR5)
    for i in ids:
        T[0] = None; FR5[i]().makeImageSnapshot().save(f"{OUT}/{i}.png", skia.kPNG); print("kare", i)
    contact5()
