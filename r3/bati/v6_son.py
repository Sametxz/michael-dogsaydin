"""Bölüm VI · Son Plan + Final ham kareleri (brief: kurul/BRIEF_bolum6.md). Tek görsel ajan.
python3 v6_son.py [model k22a ...] → /home/claude/r3/son/<id>.png (+ R13 kırpmaları), kontakt_son_960.png
Ortak dosyalara yazmaz. HASSAS: k26a–k26d kansız/şiddetsiz; yılanlar yalnızca çukur karanlığında kıvrılan gölge."""
import sys, os, math, random
sys.path.insert(0, "/home/claude/r3/bati")
from kareler6 import *
import tex
import v3_a as VA, v3_b as VB, v3_c as VC, v4_paris as VP, v5_kayip as VK
from v3_c import cloud_band, gradient, flames, soft_shadow, crop2x, mountain_range
from v4_paris import fig, river, fleet_svg, smoke, embers, chain
from v5_kayip import RGO, IVAR, IVAR_ST, UBBE, HVIT, SIG, arm_pts, ragnar_bust, sitting, sky_dusk, ridge_svg, torch, HOODC, STAFF, SHY
from art3 import RAGNAR3, figure, shade
import gemi as G
OUTS = "/home/claude/r3/son"; os.makedirs(OUTS, exist_ok=True)
R_ = random.Random
TEXD = tex.defs("ahsap", "tas", "deri", "kurk", "yun", "metal", "keten")
EXP["frozen"] = (-16, -14, 0.0, 0.0, "open_s", "")
EXP["defiant"] = (10, -6, 0.36, 0.12, "smirk", "")
EXP["serene"] = (-6, 0, 0.14, 0.02, "soft_smile", "")
EXP["fierce"] = (14, -8, 0.40, 0.16, "flat", "")
EXP["whisper"] = (-6, 3, 0.55, 0.10, "flat", "")

# ================================================================ modeller (art3 gövdesi, özgün)
GOLD_BAND = ('<path d="M-80,-58 Q0,-94 86,-62" stroke="#1A1410" stroke-width="14" fill="none"/><path d="M-80,-58 Q0,-94 86,-62" stroke="#D8B04A" stroke-width="8" fill="none"/>'
             '<path d="M-70,-64 Q0,-94 76,-68" stroke="#FFF0B0" stroke-width="2.5" fill="none" opacity="0.8"/>'
             + "".join(f'<circle cx="{x}" cy="{y}" r="5.5" fill="{cc}" stroke="#1A1410" stroke-width="2"/>' for x, y, cc in ((-44, -78, "#8E2A22"), (4, -86, "#2E5A8A"), (50, -80, "#8E2A22"))))
ECB_CLASP = ('<g transform="translate(0,-440)"><circle r="17" fill="#D8B04A" stroke="#1A1410" stroke-width="4"/><circle r="11" fill="#6A1E2A"/>'
             '<path d="M0,-8 V8 M-8,0 H8" stroke="#F4D88A" stroke-width="3.5"/></g>')
ECBERT = dict(RAGNAR3, hair="#7A6A5A", beard_c="#8A7A68", beard_len=0.38, beard_w=0.72, iris="#5A7A8A", skin="#ECC8A6", tunic="#6A1E2A", trim="#D8B04A",
              cloak="#4A1A3E", fur_collar="#D8CCB8", brow_c="#6A5646", brow_k=0.7, old=True, beard_braid=False, short_hair=True, nobraid=True, side_braids=False,
              armring=False, knot=False, face_scar=False, no_blush=True, clasp=ECB_CLASP, _head_extra=GOLD_BAND)
STEEL = ('<path d="M-84,-52 L-86,-104 L-62,-76 L-36,-116 L-12,-80 L14,-120 L38,-82 L62,-112 L86,-58 Q0,-86 -84,-52 Z" fill="#8A929A" stroke="#1A1410" stroke-width="6" stroke-linejoin="round"/>'
         '<path d="M-82,-56 Q0,-90 86,-60" stroke="#1A1410" stroke-width="16" fill="none"/><path d="M-82,-56 Q0,-90 86,-60" stroke="#6A727A" stroke-width="10" fill="none"/>'
         '<path d="M-60,-80 L-40,-108 M14,-88 L16,-112" stroke="#D8E0E8" stroke-width="3"/>' + "".join(f'<circle cx="{x}" cy="{y}" r="3.5" fill="#C8D0D8" stroke="#1A1410" stroke-width="1.5"/>' for x, y in ((-60, -66), (-20, -76), (24, -78), (64, -68))))
ELLA_CLASP = '<g transform="translate(0,-440)"><path d="M0,-18 L16,0 L0,18 L-16,0 Z" fill="#6A727A" stroke="#1A1410" stroke-width="4"/><circle r="5" fill="#2E5A3A"/></g>'
ELLA = dict(RAGNAR3, hair="#26201C", beard_c="#2E2622", stubble="#3A322C", beard_len=0.32, beard_w=0.95, iris="#4A3A2E", skin="#DDB492", tunic="#1E3A2A", trim="#7A8A8A",
            cloak="#0E1612", fur_collar="#3A3A34", brow_c="#14100C", brow_k=1.45, old=True, short_hair=True, nobraid=True, side_braids=False, beard_braid=False, jaw=1.22,
            armring=False, knot=False, face_scar=False, no_blush=True, nose2=True, clasp=ELLA_CLASP, _head_extra=STEEL)
CROSS_A = ('<g transform="translate(0,-436)"><path d="M-34,-44 Q0,8 34,-44" stroke="#5A4026" stroke-width="3.5" fill="none"/>'
           '<g transform="scale(1.35)"><rect x="-5" y="-6" width="10" height="36" rx="2" fill="#5A3E26" stroke="#1A1410" stroke-width="3"/><rect x="-15" y="3" width="30" height="9" rx="2" fill="#5A3E26" stroke="#1A1410" stroke-width="3"/>'
           '<path d="M-2,-2 V26 M-11,7 H11" stroke="#9A7A52" stroke-width="1.6" opacity="0.8"/></g></g>')   # Athelstan'ın tahta haçı
ALFRED = dict(RAGNAR3, hair="#2A201A", beard_c="#2A201A", beardless=True, smooth=True, short_hair=True, nobraid=True, side_braids=False, beard_braid=False,
              iris="#6A7E92", skin="#F6E0CE", tunic="#D2C6A8", trim="#5A4A8A", cloak="#34446A", fur_collar="#D8D0C0", brow_c="#2A201A", brow_k=0.5,
              armring=False, knot=False, face_scar=False, no_blush=False, clasp="")
ALFRED_X = dict(ALFRED, clasp=CROSS_A)
SHROUD = ('<path d="M-92,-74 Q0,-104 92,-74 L98,40 Q60,112 0,118 Q-60,112 -98,40 Z" fill="#B8AA90" stroke="#1A1410" stroke-width="6" filter="url(#t_keten)"/>'
          + "".join(f'<path d="M-96,{-50+k*30} Q0,{-66+k*30+(k%2)*10} 96,{-48+k*30}" stroke="#7A6C56" stroke-width="3" fill="none" opacity="0.8"/>' for k in range(6))
          + "".join(f'<path d="M{-60+k*24},{-80+abs(k-2.5)*3} l3,10" stroke="#3A2E22" stroke-width="2.5"/>' for k in range(6))
          + '<ellipse cx="-34" cy="-14" rx="22" ry="13" fill="#4A3C2C" opacity="0.45"/><ellipse cx="34" cy="-14" rx="22" ry="13" fill="#4A3C2C" opacity="0.45"/>'
          '<path d="M-12,30 Q0,50 12,30" fill="#4A3C2C" opacity="0.35"/>'
          '<path d="M-6,-60 V-30 M-6,-48 l-12,-12 M-6,-48 l12,-12 M44,22 l10,18 l10,-18" stroke="#5A3020" stroke-width="3.5" fill="none" opacity="0.8"/>'
          '<path d="M-80,40 Q-40,52 -10,90 M60,-60 Q80,-20 70,20" stroke="#6A5236" stroke-width="7" fill="none" opacity="0.35"/>')
SEER_HOOD = (SHROUD + HOODC("#2A2622")
             + "".join(f'<path d="M{x},{y} v{L}" stroke="#6A5A40" stroke-width="2"/><path d="M{x-5},{y+L} l5,{12} l5,-12 Z" fill="#E0D6C0" stroke="#1A1410" stroke-width="2"/>' for x, y, L in ((-92, 40, 40), (-80, 70, 52), (88, 46, 36), (74, 78, 48)))
             + '<path d="M-100,64 Q-110,120 -96,150 M100,64 Q112,124 98,152" stroke="#2A2622" stroke-width="14" fill="none" stroke-linecap="round"/>')
SEER_NECK = ('<g transform="translate(0,-430)">' + "".join(f'<path d="M{-50+k*20},{abs(k-2.5)*-6+12} l{(k-2.5)*2},26" stroke="#E0D6C0" stroke-width="6" stroke-linecap="round"/>' for k in range(6))
             + '<path d="M-60,-6 Q0,40 60,-6" stroke="#6A5A40" stroke-width="3" fill="none"/></g>')
SEER = dict(RAGNAR3, hair="#8A8478", beard_c="#8A8478", beardless=True, smooth=True, skin="#BCA898", iris="#9A9A90", tunic="#3E382E", trim="#2A2620", cloak="#24201C",
            fur_collar="#5A5048", brow_c="#8A8478", old=True, short_hair=True, nobraid=True, side_braids=False, armring=False, knot=False, face_scar=False, no_blush=True,
            clasp=SEER_NECK, _head_extra=SEER_HOOD)
SEER_ST = arm_pts(SEER, [(52, SHY + 16), (140, SHY + 110), (176, SHY + 30)], "grip", STAFF.replace("M6,-330 Q-6,-100 4,236", "M6,-300 Q-8,40 4,500").replace("M6,-330 q-20,-20 -6,-44 q20,-6 22,18", "M6,-300 q-20,-20 -6,-44 q20,-6 22,18"), ring=False, knot=False)

def saxon(seed, torch_=False):
    sp = dict(KL.soldier_spec(seed + 900, "saxon", "spear", torch=torch_)); sp.update(knot=False, face_scar=False)
    sp["tunic"] = R_(seed).choice(["#3E4A2E", "#5A4A32", "#4A3A2E", "#3A4238"]); return sp

def model():
    s = skia.Surface(W, H); c = s.getCanvas()
    bg = [TEXD, '<defs>' + gradient("mb", [(0, "#E8DCC4"), (1, "#CDBE9E")]) + '</defs><rect width="1920" height="1080" fill="url(#mb)"/>',
          '<rect width="1920" height="1080" fill="#B8A884" filter="url(#t_keten)" opacity="0.35"/>']
    for k in range(13): bg.append(f'<path d="M40,{90+k*66} H1880" stroke="#8A7A5A" stroke-width="1.5" opacity="0.3"/>')
    bg.append('<path d="M40,880 H1880" stroke="#3A2A1A" stroke-width="4"/>')
    bg.append('<text x="60" y="130" font-family="DejaVu Serif" font-size="30" font-weight="bold" fill="#3A2A1A">MODEL · Bölüm VI: Ecbert, Ella, Alfred, Kâhin (Ragnar ile boy karşılaştırma)</text>')
    draw(c, svg_sprite("".join(bg)), 0, 0, 1.0)
    G_ = 880; S = 0.87
    lst = [(RGO, "determined", "RAGNAR", "yaşlı · kuzgun broş", 230, 1.0, 1), (ECBERT, "tender", "ECBERT", "Wessex · altın bant · mor pelerin", 590, 0.98, 1),
           (ELLA, "cold", "ELLA", "Northumbria · çelik taç", 950, 1.0, 1), (ALFRED_X, "curious", "ALFRED", "~8 yaş · %60 · Athelstan'ın haçı", 1280, 0.6, 1),
           (SEER_ST, "neutral", "KÂHİN", "yüzü örtülü · asa · kemik muska", 1620, 0.95, -1)]
    for sp, e, nm, sub, x, sc, f_ in lst:
        fs = full(sp, e, 0.9, facing=f_, look=0.2); soft_shadow(c, x, G_ - 6, 120 * sc, 14, 0.4); draw(c, fs, x, G_, S * sc)
        card_at(c, nm, x, 960, sub, 0.9)
    finish(c, cold=False, warm=0.02); return s

# ================================================================ ortak yardımcılar
def rain(c, seed, n, box=(0, 0, 1920, 1080), L=(40, 90), ang=12, colr="#C8D4DC", a=(0.15, 0.4), w=(1.2, 2.4)):
    r = R_(seed); x0, y0, x1, y1 = box
    for k in range(n):
        x = r.uniform(x0, x1); y = r.uniform(y0, y1); l = r.uniform(*L); dx = math.tan(math.radians(ang)) * l
        c.drawLine(x, y, x - dx, y + l, skia.Paint(AntiAlias=True, StrokeWidth=r.uniform(*w), Color4f=col(colr, r.uniform(*a))))

def splashes(seed, n, x0, x1, y0, y1, colr="#D8E0E6"):
    r = R_(seed); o = []
    for k in range(n):
        x = r.uniform(x0, x1); y = r.uniform(y0, y1); q = (y - y0) / max(1, y1 - y0); rr = 4 + 12 * q
        o.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{rr:.0f}" ry="{rr*0.3:.1f}" fill="none" stroke="{colr}" stroke-width="1.5" opacity="{0.25+0.3*q:.2f}"/>')
    return "".join(o)

def puddles(seed, n, x0, x1, y0, y1, refl="#8A98A4", glint=None):
    r = R_(seed); o = []
    for k in range(n):
        x = r.uniform(x0, x1); y = r.uniform(y0, y1); q = (y - y0) / max(1, y1 - y0); rx = 40 + 140 * q; ry = rx * 0.16
        o.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{rx:.0f}" ry="{ry:.0f}" fill="{refl}" opacity="0.75" stroke="#1E1A16" stroke-width="2"/>'
                 f'<path d="M{x-rx*0.6:.0f},{y-ry*0.2:.0f} H{x+rx*0.3:.0f}" stroke="{glint or "#E8EEF2"}" stroke-width="2.5" opacity="0.6"/>')
    return "".join(o)

def snake_shadows(c, seed, n, box, a=0.55, sheen="#5E7A5A"):
    """Yılan İMASI: karanlıkta kıvrılan, başı/ağzı olmayan gölge şeritleri; yalnızca pul parıltısı."""
    r = R_(seed); x0, y0, x1, y1 = box; o = []
    for k in range(n):
        x = r.uniform(x0, x1); y = r.uniform(y0, y1); L = r.uniform(140, 320); amp = r.uniform(14, 34); ph = r.uniform(0, 6); rot = r.uniform(-30, 30)
        pts = [(x + L * q - L / 2, y + amp * math.sin(ph + q * 9)) for q in [i / 24 for i in range(25)]]
        d = "M" + " L".join(f"{px:.0f},{py:.0f}" for px, py in pts); wdt = r.uniform(12, 20)
        o.append(f'<g transform="rotate({rot:.0f} {x:.0f} {y:.0f})"><path d="{d}" stroke="#05080A" stroke-width="{wdt:.0f}" fill="none" stroke-linecap="round" opacity="0.9"/>'
                 f'<path d="{d}" stroke="{sheen}" stroke-width="2.2" fill="none" stroke-dasharray="14 22" opacity="0.35" transform="translate(0,{-wdt*0.28:.0f})"/></g>')
    draw(c, blurred(svg_sprite("".join(o)), 3.6), 0, 0, 1.0, a=a)

def vign(c, cx=0.5, cy=0.5, r=0.62, a=0.85, colr="#050302", inner=0.45):
    draw(c, svg_sprite(f'<defs><radialGradient id="vgn" cx="{cx}" cy="{cy}" r="{r}"><stop offset="{inner}" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="{colr}" stop-opacity="{a}"/></radialGradient></defs><rect width="1920" height="1080" fill="url(#vgn)"/>'), 0, 0, 1.0)

def tile_roof(x0, x1, y_top, y_eave, overhang=40, seed=1, col_="#9A4A32"):
    r = R_(seed); o = [f'<path d="M{x0-overhang},{y_eave} L{x0+60},{y_top} L{x1-60},{y_top} L{x1+overhang},{y_eave} Z" fill="{col_}" stroke="#1A1410" stroke-width="6"/>']
    rows = int((y_eave - y_top) / 16)
    for k in range(rows):
        y = y_top + k * 16 + 8; q = k / max(1, rows); xa = x0 + 60 - (100 + overhang) * q; xb = x1 - 60 + (100 + overhang) * q
        o.append(f'<path d="M{xa:.0f},{y} H{xb:.0f}" stroke="#5A2618" stroke-width="2.5"/>')
        o.append("".join(f'<path d="M{xx:.0f},{y-7} q6,8 12,0" stroke="{r.choice(["#C2684A", "#B05A3E", "#7A3424"])}" stroke-width="3" fill="none"/>' for xx in range(int(xa) + (k % 2) * 9, int(xb) - 10, 18)))
    for k in range(10): x = r.uniform(x0, x1); o.append(f'<ellipse cx="{x:.0f}" cy="{r.uniform(y_top+10, y_eave-6):.0f}" rx="{r.uniform(20,60):.0f}" ry="5" fill="#4A5A2E" opacity="0.55"/>')
    o.append(f'<path d="M{x0-overhang},{y_eave} L{x1+overhang},{y_eave}" stroke="#1A1410" stroke-width="10"/>')
    return "".join(o)

def column(x, yb, h, w=46, lit="#E8D8B8", body="#B8A888", dark="#6A5E4C"):
    return (f'<rect x="{x-w/2}" y="{yb-h}" width="{w}" height="{h}" fill="{body}" stroke="#1A1410" stroke-width="5" filter="url(#t_tas)"/>'
            + "".join(f'<path d="M{x-w/2+8+k*10},{yb-h+20} V{yb-20}" stroke="{dark}" stroke-width="2.5" opacity="0.7"/>' for k in range(int(w/10)-1))
            + f'<rect x="{x+w*0.12:.0f}" y="{yb-h}" width="{w*0.38:.0f}" height="{h}" fill="#000" opacity="0.25"/><path d="M{x-w/2+4},{yb-h+6} V{yb-8}" stroke="{lit}" stroke-width="4" opacity="0.8"/>'
            f'<rect x="{x-w/2-12}" y="{yb-h-24}" width="{w+24}" height="26" fill="{body}" stroke="#1A1410" stroke-width="5"/><path d="M{x-w/2-12},{yb-h-14} q{(w+24)/4},-14 {(w+24)/2},0 q{(w+24)/4},14 {(w+24)/2},0" stroke="{dark}" stroke-width="3" fill="none"/>'
            f'<rect x="{x-w/2-10}" y="{yb-20}" width="{w+20}" height="20" fill="{dark}" stroke="#1A1410" stroke-width="5"/>')

def wyvern_banner(x, y, w, h, c1="#8E1E22", c2="#D8B04A", seed=0, wet=True):
    o = [f'<path d="M{x-w/2-14},{y} H{x+w/2+14}" stroke="#1A1410" stroke-width="12" stroke-linecap="round"/><path d="M{x-w/2-14},{y} H{x+w/2+14}" stroke="#6A4A2E" stroke-width="6"/>',
         f'<path d="M{x-w/2},{y} H{x+w/2} V{y+h} L{x},{y+h-34} L{x-w/2},{y+h} Z" fill="{c1}" stroke="#1A1410" stroke-width="5" filter="url(#t_yun)"/>',
         f'<g transform="translate({x},{y+h*0.45}) scale({w/200})"><path d="M-40,40 Q-60,0 -20,-20 Q0,-50 30,-40 L50,-60 L44,-30 Q60,-10 40,10 L60,30 L30,24 Q10,50 -40,40 Z M-20,-20 L-60,-50 L-30,-10 Z" fill="{c2}" stroke="#1A1410" stroke-width="4"/>'
         f'<circle cx="34" cy="-36" r="3" fill="#1A1410"/></g>', f'<path d="M{x+w*0.15},{y} V{y+h-20}" stroke="#000" stroke-width="{w*0.3}" opacity="0.18"/>']
    if wet: o.append("".join(f'<path d="M{x-w/2+10+k*w/5:.0f},{y+h*0.2:.0f} v{h*0.6:.0f}" stroke="#000" stroke-width="3" opacity="0.15"/>' for k in range(5)))
    return "".join(o)

def candle_cluster(x, y, n=3, seed=1):
    r = R_(seed); return "".join(VA.drip_candle(x + k * 26 - n * 13, y, r.uniform(60, 120), 18, True, seed + k) for k in range(n))

# ================================================================ k22a · yağmurda Ecbert'in villasının kapısı
def villa_gate(c, t):
    o = [TEXD, VA.stone_wall(180, 470, 1740, 790, seed=61, wash=0.4) if False else VP.wall(160, 1760, 470, 790, 61, merlons=False, slits=False, lit="#C8C4B8", lita=0.10)]
    o.append(tile_roof(160, 1760, 380, 476, 50, 3, "#8A4232"))
    # kemerli kapı + kanat
    o.append('<path d="M860,790 L860,560 Q960,470 1060,560 L1060,790 Z" fill="#1A1410"/><path d="M880,790 L880,566 Q960,494 1040,566 L1040,790 Z" fill="#3A2416" filter="url(#t_ahsap)"/>'
             + "".join(f'<path d="M{900+k*28},{560 if k in (1,3,4) else 580} V790" stroke="#1E140C" stroke-width="4"/>' for k in range(6))
             + '<path d="M880,640 H1040 M880,730 H1040" stroke="#4A4A4A" stroke-width="10"/><circle cx="1010" cy="690" r="10" fill="none" stroke="#B89A5A" stroke-width="5"/>'
             '<path d="M960,690 V790" stroke="#0E0A06" stroke-width="5"/><path d="M970,700 L1040,700 L1040,790 L970,790 Z" fill="#FFB060" opacity="0.18"/>')
    for k in range(13):   # kemer taşları
        a = math.pi * (k / 12); xx = 960 - 104 * math.cos(a); yy = 566 - 84 * math.sin(a)
        o.append(f'<rect x="{xx-14:.0f}" y="{yy-12:.0f}" width="28" height="24" fill="#A89C88" stroke="#1A1410" stroke-width="3" transform="rotate({math.degrees(a)-90:.0f} {xx:.0f} {yy:.0f})"/>')
    o.append(column(820, 790, 270, 50) + column(1100, 790, 270, 50))
    for x in (380, 1540): o.append(f'<path d="M{x-50},640 L{x-50},560 Q{x},520 {x+50},560 L{x+50},640 Z" fill="#FFB060" stroke="#1A1410" stroke-width="6" opacity="0.9"/><path d="M{x},530 V640 M{x-50},590 H{x+50}" stroke="#2A1A10" stroke-width="7"/>')
    o.append(wyvern_banner(600, 500, 120, 200, seed=1) + wyvern_banner(1320, 500, 120, 200, seed=2))
    o.append('<ellipse cx="960" cy="480" rx="70" ry="22" fill="#5A6A3A" opacity="0.6"/>')
    draw(c, svg_sprite("".join(o)), 0, 0, 1.0)
    for x in (380, 1540): glow(c, x, 600, 220, "#FFA050", 0.35)
    torch(c, 790, 600, t, 1.1); torch(c, 1130, 600, t, 1.1)

def k22a():
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    draw(c, svg_sprite(sky_dusk("s22a", [(0, "#2E3442"), (0.5, "#5A6070"), (1, "#8A8A90")], 700)), 0, 0, 1.0)
    draw(c, blurred(svg_sprite(cloud_band(2201, 14, -100, 2000, 60, 420, "#262C38", "#6A7080", 0.95, lit_dy=-6, rx=(240, 520), ry=(30, 70))), 4), 0, 0, 1.0)
    draw(c, blurred(svg_sprite(VB.forest(-60, 1980, lambda x: 560 + 16 * math.sin(x / 120), 120, 260, 40, 2202, col="#2A3430", lit="#46524C", dark="#1A2220")), 3), 0, 0, 1.0, a=0.85)
    villa_gate(c, t)
    # zemin: ıslak taş döşeme, tekerlek izi, çamur, su birikintileri
    g = [TEXD, '<path d="M0,790 L1920,790 L1920,1080 L0,1080 Z" fill="#3A3632"/>', VP.stones(0, 790, 1920, 1080, 2203, pal=("#4A4642", "#55504A", "#3E3A36", "#5E5852"), row=(18, 40), wd=(40, 120), a=0.95),
         '<path d="M720,790 Q600,900 420,1080 M1200,790 Q1320,900 1500,1080" stroke="#2A2420" stroke-width="26" fill="none" opacity="0.6"/>',
         puddles(2204, 9, 200, 1700, 820, 1060, "#6A6058", "#FFC890"),
         '<path d="M900,860 Q960,850 1020,860" stroke="#FFB060" stroke-width="10" opacity="0.35"/>', splashes(2205, 140, 0, 1920, 800, 1080)]
    draw(c, svg_sprite("".join(g)), 0, 0, 1.0)
    # kapı nöbetçileri (Sakson)
    for k, (x, f_) in enumerate(((740, 1), (1180, -1))):
        fig(c, saxon(k + 3), "cold", x, 800, 0.48, facing=f_, look=0.3 * f_, rimc="#FFB060", rdx=4 * f_, shx=(x - 60 * f_, x + 80 * f_), shc="#141820")
    # Ragnar (sırtı dönük) ve Ivar (değnekli, yanında)
    fs = full(dict(RGO, cloak="#2A3040"), "neutral", 0.9, facing=1, view="back")
    soft_shadow(c, 800, 1000, 110, 16, 0.5); rim(c, fs, 800, 1006, 0.7, "#FFB070", dx=4, dy=-3, a=0.7); draw(c, fs, 800, 1006, 0.7); shade_side(c, fs, 800, 1006, 0.45, 720, 940, "#10141E")
    fig(c, IVAR_ST, "keen", 1110, 1012, 0.74, facing=-1, look=0.4, rimc="#FFB070", rdx=5, shx=(1220, 1000), shc="#10141E", sha=0.35)
    draw(c, svg_sprite(puddles(2206, 2, 820, 1180, 1030, 1050, "#5A524A", "#FFC890")), 0, 0, 1.0, a=0.6)
    # ön plan: bulanık sarmaşıklı sütun (sol), ıslak çalı (sağ)
    fg = [TEXD, column(70, 1100, 1100, 150, body="#5A5446", dark="#2A2620", lit="#8A8070")]
    r = R_(2207)
    for k in range(40): fg.append(f'<ellipse cx="{r.uniform(20,160):.0f}" cy="{r.uniform(100,1000):.0f}" rx="{r.uniform(12,26):.0f}" ry="{r.uniform(6,12):.0f}" fill="{r.choice(["#2E4A2A", "#3E5A32", "#1E3020"])}" transform="rotate({r.uniform(-40,40):.0f})"/>')
    for k in range(30): x = 1700 + r.uniform(0, 260); fg.append(f'<ellipse cx="{x:.0f}" cy="{r.uniform(880,1080):.0f}" rx="{r.uniform(30,60):.0f}" ry="{r.uniform(12,24):.0f}" fill="{r.choice(["#1E2A1C", "#2A3A26"])}"/>')
    draw(c, blurred(svg_sprite("".join(fg)), 7), 0, 0, 1.0)
    rain(c, 2208, 900, ang=10); rain(c, 2209, 120, L=(120, 200), ang=10, a=(0.2, 0.45), w=(2, 3.5))
    card_at(c, "ECBERT", 960, 150, "Wessex kralı · eski dost", 0.9)
    finish(c, cold=True, warm=0.03); return s

# ================================================================ k22b · ocak başı, şarap, satranç
def room_bg(c, t, fire=1.0, blur=3, dark=0.0):
    o = [TEXD, '<rect width="1920" height="1080" fill="#3A2C22"/>', VA.stone_wall(0, 0, 1920, 1080, seed=71, wash=0.45)]
    o.append('<rect x="0" y="120" width="1920" height="70" fill="#6A2A22" opacity="0.85"/>' + "".join(f'<path d="M{k*60},130 l30,25 l30,-25 M{k*60},180 l30,-25 l30,25" stroke="#D8B04A" stroke-width="3" fill="none" opacity="0.8"/>' for k in range(33)))
    # şömine (orta-sağ arka)
    o.append('<path d="M760,800 L760,420 Q960,300 1160,420 L1160,800 Z" fill="#6A5E50" stroke="#1A1410" stroke-width="8" filter="url(#t_tas)"/><path d="M820,800 L820,520 Q960,430 1100,520 L1100,800 Z" fill="#140C08"/>'
             '<rect x="740" y="400" width="440" height="34" fill="#8A7A64" stroke="#1A1410" stroke-width="6"/>')
    # pencere: gece yağmuru
    o.append('<path d="M240,620 L240,360 Q330,280 420,360 L420,620 Z" fill="#2A3A52" stroke="#1A1410" stroke-width="10"/><path d="M330,300 V620 M240,470 H420" stroke="#1A1410" stroke-width="8"/>'
             + "".join(f'<path d="M{250+k*16},{370+(k%3)*30} l-6,40" stroke="#8AA0BA" stroke-width="2" opacity="0.6"/>' for k in range(11)))
    # duvar halısı, raf, kitap, kandil
    o.append('<rect x="1440" y="250" width="300" height="420" fill="#4A2A3A" stroke="#1A1410" stroke-width="6" filter="url(#t_yun)"/><rect x="1460" y="270" width="260" height="380" fill="none" stroke="#D8B04A" stroke-width="5"/>'
             '<g transform="translate(1590,460) scale(1.1)"><path d="M0,-90 V90 M-60,-20 H60" stroke="#D8B04A" stroke-width="16"/><circle r="30" fill="none" stroke="#D8B04A" stroke-width="8"/></g>')
    o.append('<rect x="460" y="560" width="200" height="16" fill="#5A3E26" stroke="#1A1410" stroke-width="4"/>' + VA.gospel(520, 556, 0.35) + candle_cluster(620, 556, 2, 7))
    draw(c, blurred(svg_sprite("".join(o)), blur), 0, 0, 1.0)
    flames(c, 840, 1080, 790, 200 * fire, t, seed=4); glow(c, 960, 700, 640, "#FF8A3A", 0.38 * fire); glow(c, 960, 760, 220, "#FFC070", 0.4 * fire)
    if dark: fill(c, "#0A0604", dark)

def chessboard(cx, cy, w, seed=3):
    """Perspektif satranç tahtası + taşlar (fil, at, kale, piyon), bir kısmı devrilmiş."""
    r = R_(seed); o = []; h = w * 0.36
    o.append(f'<path d="M{cx-w/2},{cy+h/2} L{cx-w*0.38},{cy-h/2} L{cx+w*0.38},{cy-h/2} L{cx+w/2},{cy+h/2} Z" fill="#3A2416" stroke="#1A1410" stroke-width="6"/>'
             f'<path d="M{cx-w/2},{cy+h/2} L{cx+w/2},{cy+h/2} L{cx+w/2},{cy+h/2+16} L{cx-w/2},{cy+h/2+16} Z" fill="#2A180E" stroke="#1A1410" stroke-width="4"/>')
    n = 8
    for i in range(n):
        for j in range(n):
            def P(u, v): return (cx + (u - 0.5) * (w * (0.76 + 0.24 * v)), cy - h / 2 + v * h)
            a, b, cc, d = P(i / n, j / n), P((i + 1) / n, j / n), P((i + 1) / n, (j + 1) / n), P(i / n, (j + 1) / n)
            if (i + j) % 2: o.append(f'<path d="M{a[0]:.0f},{a[1]:.0f} L{b[0]:.0f},{b[1]:.0f} L{cc[0]:.0f},{cc[1]:.0f} L{d[0]:.0f},{d[1]:.0f} Z" fill="#D8C49A"/>')
    for i, (u, v, wh, kind) in enumerate([(0.2, 0.2, 1, "k"), (0.35, 0.45, 1, "p"), (0.6, 0.35, 0, "p"), (0.7, 0.7, 0, "r"), (0.45, 0.75, 1, "b"), (0.8, 0.25, 0, "k"), (0.15, 0.8, 0, "p")]):
        x = cx + (u - 0.5) * (w * (0.76 + 0.24 * v)); y = cy - h / 2 + v * h; fc = "#EDE2C8" if wh else "#2A1E18"; hgt = {"k": 54, "p": 26, "r": 36, "b": 44}[kind]
        o.append(f'<path d="M{x-11},{y} Q{x-6},{y-hgt*0.5} {x-5},{y-hgt} L{x+5},{y-hgt} Q{x+6},{y-hgt*0.5} {x+11},{y} Z" fill="{fc}" stroke="#1A1410" stroke-width="3"/><circle cx="{x}" cy="{y-hgt-6}" r="7" fill="{fc}" stroke="#1A1410" stroke-width="3"/>')
    o.append(f'<g transform="translate({cx+w*0.62},{cy+h*0.2}) rotate(80)"><path d="M-11,0 Q-6,-27 -5,-54 L5,-54 Q6,-27 11,0 Z" fill="#EDE2C8" stroke="#1A1410" stroke-width="3"/><circle cy="-60" r="7" fill="#EDE2C8" stroke="#1A1410" stroke-width="3"/></g>')   # devrik kral
    return "".join(o)

def goblet(x, y, s=1.0, wine=True):
    return (f'<g transform="translate({x},{y}) scale({s})"><ellipse cx="0" cy="0" rx="34" ry="9" fill="#8A8E96" stroke="#1A1410" stroke-width="4"/><path d="M-5,-4 L-5,-50 L5,-50 L5,-4 Z" fill="#A8AEB6" stroke="#1A1410" stroke-width="4"/>'
            f'<path d="M-36,-110 Q-34,-56 0,-50 Q34,-56 36,-110 Z" fill="#B8BEC6" stroke="#1A1410" stroke-width="5"/>' + (f'<ellipse cx="0" cy="-106" rx="32" ry="7" fill="#5A0E18"/>' if wine else '')
            + '<path d="M-26,-100 Q-24,-66 -8,-58" stroke="#F4F6F8" stroke-width="4" fill="none" opacity="0.8"/><circle cx="0" cy="-30" r="5" fill="#C9A25A" stroke="#1A1410" stroke-width="2"/></g>')

def table_front(y=860, seed=5):
    o = [TEXD, f'<path d="M-20,{y} Q960,{y-30} 1940,{y} L1940,1090 L-20,1090 Z" fill="#4A3020" filter="url(#t_ahsap)"/><path d="M-20,{y} Q960,{y-30} 1940,{y}" stroke="#1A1410" stroke-width="10" fill="none"/>',
         f'<path d="M-20,{y+6} Q960,{y-24} 1940,{y+6}" stroke="#E0A060" stroke-width="4" fill="none" opacity="0.6"/>']
    r = R_(seed)
    for k in range(14): o.append(f'<path d="M{r.uniform(0,1900):.0f},{r.uniform(y+30,1070):.0f} q120,-6 240,0" stroke="#2A1A10" stroke-width="2.5" fill="none" opacity="0.6"/>')
    return "".join(o)

def k22b():
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    room_bg(c, t, 1.0, 4, 0.1)
    ragnar_bust(c, RGO, "tender", 520, 470, 1.25, look=0.5, rimc="#FFB070", shx=(380, 560), shc="#140A06", phase=0.3)
    b = fig_bust(ECBERT, ex("tender", IF.blink_at(0.9)), 0.5, 1.2, flip=True)
    with live(c, 1400, 1080, phase=0.9, breathe=0.005):
        rim(c, b, 1400, 480, 1.0, "#FFB070", dx=-6, dy=-3, a=0.7); draw(c, b, 1400, 480, 1.0); shade_side(c, b, 1400, 480, 0.45, 1460, 1680, "#140A06")
    tb = [table_front(860), chessboard(960, 920, 460), goblet(640, 960, 0.9), goblet(1290, 970, 0.9),
          '<g transform="translate(1110,960)"><path d="M-40,0 Q-56,-80 -30,-120 L-18,-150 L18,-150 L30,-120 Q56,-80 40,0 Z" fill="#7A4A2A" stroke="#1A1410" stroke-width="5"/><path d="M40,-100 Q74,-90 44,-40" stroke="#1A1410" stroke-width="10" fill="none"/><path d="M-30,-90 Q-38,-50 -26,-20" stroke="#C88A5A" stroke-width="4" fill="none"/></g>',
          '<ellipse cx="780" cy="1010" rx="80" ry="26" fill="#C89A5A" stroke="#1A1410" stroke-width="5"/><path d="M720,1004 Q780,980 840,1004" stroke="#8A5A2A" stroke-width="4" fill="none"/>',
          candle_cluster(1560, 960, 3, 11)]
    draw(c, svg_sprite("".join(tb)), 0, 0, 1.0)
    for x in (1534, 1560, 1586): glow(c, x, 860, 70, "#FFD080", 0.4)
    glow(c, 960, 900, 300, "#FFB060", 0.15)
    draw(c, blurred(svg_sprite(TEXD + goblet(140, 1100, 2.2, False) + candle_cluster(1840, 1100, 2, 13)), 9), 0, 0, 1.0)
    embers(c, 2211, 26, (760, 400, 1160, 800))
    finish(c, cold=False, warm=0.07); return s

# ================================================================ k22c · yakın: kararlı Ragnar, donan Ecbert
def k22c():
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    room_bg(c, t, 0.8, 10, 0.35)
    VA.beam(c, 300, 0, 120, 600, 1080, 500, "#9AB0D0", 0.10, 20)
    ragnar_bust(c, RGO, "determined", 600, 470, 2.05, look=0.7, rimc="#FFB070", shx=(400, 760), shc="#120806", phase=0.2)
    b = fig_bust(ECBERT, ex("frozen", IF.blink_at(3.0)), 0.6, 1.85, flip=True)
    with live(c, 1420, 1080, phase=1.3, breathe=0.003):
        rim(c, b, 1420, 500, 1.0, "#9AB0D0", dx=6, dy=-3, a=0.55); draw(c, b, 1420, 500, 1.0); shade_side(c, b, 1420, 500, 0.5, 1300, 1700, "#0A1018")
    draw(c, blurred(svg_sprite(TEXD + goblet(980, 1150, 2.4) + chessboard(980, 1080, 600)), 10), 0, 0, 1.0)
    vign(c, 0.5, 0.45, 0.7, 0.7)
    finish(c, cold=False, warm=0.04); return s

# ================================================================ k23a · Ivar'a fısıltı; arkada gemi
def shore_bg(c, seed=2301, dusk=True):
    draw(c, svg_sprite(sky_dusk("s23", [(0, "#3A4052"), (0.55, "#9A8A8A"), (1, "#E8B888")], 640)), 0, 0, 1.0)
    draw(c, blurred(svg_sprite(cloud_band(seed, 12, -100, 2000, 60, 400, "#3A3E4E", "#D8A07A", 0.9, lit_dy=8, rx=(220, 480), ry=(26, 60))), 4), 0, 0, 1.0)
    glow(c, 1500, 560, 520, "#FFC080", 0.4)
    o = [TEXD, ridge_svg([(0, 470), (300, 420), (640, 480), (980, 440), (1300, 500), (1600, 450), (1920, 480)], 600, "#5A5A66"),
         VB.forest(-60, 1980, lambda x: 590 + 10 * math.sin(x / 70), 50, 110, 60, seed + 1, col="#3A4048", lit="#5A6068", dark="#2A3038"),
         river(590, 1080, seed + 2, top="#D8B898", mid="#6A7480", bot="#2A3440", glint=1500, gcol="#FFE0B0", n=90)]
    draw(c, svg_sprite("".join(o)), 0, 0, 1.0)
    draw(c, svg_sprite(G.longship(1450, 700, 0.55, sail=True, billow=0.4)), 0, 0, 1.0)
    VP.ripples(c, 1450, 740, 400)
    for k, x in enumerate((1080, 1160, 1250)): fig(c, saxon(k + 11), "neutral", x, 760, 0.2, facing=1, shadow=0.3)

def k23a():
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    shore_bg(c)
    draw(c, blurred(svg_sprite(TEXD + '<path d="M0,820 Q960,780 1920,830 L1920,1080 L0,1080 Z" fill="#5A5046" filter="url(#t_tas)"/>' + VC.pebbles(2302, 160, 0, 1920, 830, 1080, hl="#FFD8A8")), 2), 0, 0, 1.0)
    ragnar_bust(c, RGO, "whisper", 820, 450, 1.55, look=0.9, rimc="#FFC890", shx=(620, 860), shc="#141018", rot=12, phase=0.5)
    b = fig_bust(IVAR, ex("cold", IF.blink_at(2.0)), 0.3, 1.45, flip=True)
    with live(c, 1140, 1080, phase=1.1):
        rim(c, b, 1140, 500, 1.0, "#FFC890", dx=6, dy=-3, a=0.7); draw(c, b, 1140, 500, 1.0); shade_side(c, b, 1140, 500, 0.4, 1100, 1350, "#141018")
    bloom_spot(c, 990, 450, 90, "#FFE8C0", 0.18)
    draw(c, blurred(svg_sprite(TEXD + VK.crutch_line(1760, 1120, 1700, 640, 1.3) + '<path d="M-20,1000 Q200,940 420,1090 L-20,1090 Z" fill="#2A2420"/>'), 5), 0, 0, 1.0)
    for k in range(30): q = R_(k + 2310); c.drawCircle(q.uniform(400, 1600), q.uniform(200, 800), q.uniform(1, 2.4), skia.Paint(AntiAlias=True, Color4f=col("#FFE8C8", q.uniform(0.15, 0.45))))
    finish(c, cold=False, warm=0.05); return s

# ================================================================ k23b · Ivar'ın gözleri, arkada bulanık Ecbert, kırmızı ton
def k23b():
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    room_bg(c, t, 1.2, 12, 0.3)
    b = fig_bust(ECBERT, ex("neutral", IF.blink_at(0.5)), -0.3, 1.0)
    draw(c, blurred(b, 7), 470, 470, 1.0, a=0.85)
    fill(c, "#5A0808", 0.28); glow(c, 470, 470, 400, "#C02020", 0.25)
    b2 = fig_bust(IVAR, ex("fierce", IF.blink_at(4.0)), -0.2, 3.6, flip=True)
    with live(c, 1200, 1080, phase=2.0, breathe=0.002):
        rim(c, b2, 1200, 520, 1.0, "#FF5A3A", dx=-8, dy=-3, a=0.8); draw(c, b2, 1200, 520, 1.0); shade_side(c, b2, 1200, 520, 0.6, 1300, 1700, "#200406")
    for x, y in ((1080, 490), (1290, 490)): bloom_spot(c, x, y, 26, "#9AD8FF", 0.35)
    draw(c, svg_sprite('<defs><linearGradient id="rg" x1="0" x2="1"><stop offset="0" stop-color="#8A0A0A" stop-opacity="0.25"/><stop offset="0.6" stop-color="#8A0A0A" stop-opacity="0.0"/></linearGradient></defs><rect width="1920" height="1080" fill="url(#rg)"/>'), 0, 0, 1.0)
    embers(c, 2321, 30, (100, 200, 900, 900), "#FF7040")
    vign(c, 0.6, 0.48, 0.65, 0.85, "#120202")
    finish(c, cold=False, warm=0.03); return s

# ================================================================ k24 · avluda Alfred, haç
def courtyard_bg(c, t):
    draw(c, svg_sprite(sky_dusk("s24", [(0, "#8A9AAA"), (0.6, "#D8D4C8"), (1, "#F0E4CC")], 500)), 0, 0, 1.0)
    draw(c, blurred(svg_sprite(cloud_band(2401, 10, -100, 2000, 40, 260, "#9AA4B0", "#F4ECDC", 0.8, rx=(200, 420), ry=(20, 40))), 4), 0, 0, 1.0)
    o = [TEXD, VP.wall(0, 1920, 360, 760, 2402, merlons=False, slits=False, lit="#F2E2C2", lita=0.18), tile_roof(-40, 1960, 250, 360, 0, 4, "#9A4E36"),
         '<rect x="0" y="360" width="1920" height="400" fill="#1A1410" opacity="0.18"/>']
    for k in range(9): o.append(column(80 + k * 220, 760, 380, 44))
    for k in range(8): o.append(f'<path d="M{102+k*220},400 Q{190+k*220},350 {278+k*220},400" stroke="#1A1410" stroke-width="6" fill="none"/><rect x="{120+k*220}" y="430" width="140" height="330" fill="#2A2018" opacity="0.55"/>')
    o.append(wyvern_banner(1290, 420, 110, 190, seed=3, wet=False))
    draw(c, blurred(svg_sprite("".join(o)), 2), 0, 0, 1.0)
    # avlu zemini: taş + bahçe yatakları, kuyu, saksılar
    g = [TEXD, '<path d="M0,760 L1920,760 L1920,1080 L0,1080 Z" fill="#8A7E6A"/>', VP.stones(0, 760, 1920, 1080, 2403, row=(14, 34), wd=(36, 110)),
         '<path d="M0,780 L380,780 L300,860 L0,860 Z" fill="#4A5A2E"/>' + "".join(f'<path d="M{20+k*30},{850-(k%3)*6} q4,-40 -6,-70 M{30+k*30},{850} q-2,-30 10,-56" stroke="#6A8A3A" stroke-width="4" fill="none"/>' for k in range(11)),
         '<g transform="translate(1680,860)"><ellipse cx="0" cy="0" rx="110" ry="30" fill="#6A6458" stroke="#1A1410" stroke-width="6"/><path d="M-110,0 V-70 Q0,-96 110,-70 V0" fill="#8A8272" stroke="#1A1410" stroke-width="6" filter="url(#t_tas)"/>'
         '<ellipse cx="0" cy="-74" rx="110" ry="24" fill="#2A3038" stroke="#1A1410" stroke-width="6"/><path d="M-90,-74 V-230 M90,-74 V-230 M-110,-230 H110" stroke="#1A1410" stroke-width="16"/><path d="M-90,-74 V-230 M90,-74 V-230 M-110,-230 H110" stroke="#6A4C30" stroke-width="9"/>'
         '<path d="M20,-230 V-130" stroke="#A88E62" stroke-width="4"/><rect x="2" y="-136" width="36" height="40" fill="#6A4A2C" stroke="#1A1410" stroke-width="4"/></g>',
         "".join(f'<g transform="translate({x},{y})"><path d="M-30,0 L-24,-50 L24,-50 L30,0 Z" fill="#A85A3A" stroke="#1A1410" stroke-width="4"/><ellipse cy="-58" rx="40" ry="26" fill="#4A6A34" stroke="#1A1410" stroke-width="3"/></g>' for x, y in ((520, 800), (1440, 800)))]
    draw(c, svg_sprite("".join(g)), 0, 0, 1.0)
    fig(c, dict(monk(3)), "neutral", 360, 770, 0.3, facing=1, shadow=0.3)
    fig(c, saxon(21), "neutral", 1500, 770, 0.3, facing=-1, shadow=0.3)
    VA.beam(c, 1250, 0, 200, 1050, 1080, 600, "#FFF0D0", 0.16, 18)

def k24():
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    courtyard_bg(c, t)
    ax, ay, asc = 1150, 1010, 0.86
    fig(c, ALFRED_X, "awe", ax, ay, asc, facing=-1, look=-0.6, rimc="#FFF0D0", rdx=6, shx=(1100, 1300), shc="#2A2A38", sha=0.3)
    RC = arm_pts(RGO, [(52, SHY + 16), (190, SHY + 84), (330, SHY + 46)], "grip")
    ragnar_bust(c, RC, "tender", 640, 420, 1.42, look=0.8, rimc="#FFF0D0", shx=(420, 640), shc="#2A2430", rot=8, phase=0.6)
    cx, cy = ax, ay - 436 * 0.9 * asc + 20
    glow(c, cx, cy, 120, "#FFE6A0", 0.28); bloom_spot(c, cx, cy, 22, "#FFF6D8", 0.35); rays(c, cx, cy, 0, 110, 360, 10, "#FFF0C0", 0.06, 0.0)
    draw(c, blurred(svg_sprite(TEXD + '<path d="M1880,1100 Q1820,700 1940,300" stroke="#2A3A20" stroke-width="40" fill="none"/>' + "".join(f'<ellipse cx="{1860+(k%3)*20}" cy="{340+k*50}" rx="40" ry="18" fill="#3A5A2A" transform="rotate({-30+k*12} {1860+(k%3)*20} {340+k*50})"/>' for k in range(14))), 8), 0, 0, 1.0)
    card_at(c, "ALFRED", 1150, 330, "Athelstan'ın oğlu", 0.8)
    finish(c, cold=False, warm=0.05); return s

# ================================================================ k25a · yağmurda kafesli araba
def wheel(x, y, r_, s=1.0):
    return (f'<g transform="translate({x},{y})"><circle r="{r_}" fill="none" stroke="#1A1410" stroke-width="22"/><circle r="{r_}" fill="none" stroke="#5A3E26" stroke-width="13"/>'
            + "".join(f'<path d="M0,0 L{r_*math.cos(k*math.pi/4):.0f},{r_*math.sin(k*math.pi/4):.0f}" stroke="#1A1410" stroke-width="12"/><path d="M0,0 L{r_*math.cos(k*math.pi/4):.0f},{r_*math.sin(k*math.pi/4):.0f}" stroke="#6A4A2E" stroke-width="6"/>' for k in range(8))
            + f'<circle r="16" fill="#3A3A3A" stroke="#1A1410" stroke-width="5"/><path d="M{-r_*0.7:.0f},{r_*0.75:.0f} Q0,{r_*1.05:.0f} {r_*0.7:.0f},{r_*0.75:.0f}" stroke="#3A2A1C" stroke-width="10" fill="none" opacity="0.8"/></g>')

def cage_back(x, yb, w, h):
    return (f'<rect x="{x-w/2}" y="{yb-h}" width="{w}" height="{h}" fill="#2A2420" opacity="0.6"/>'
            + "".join(f'<path d="M{x-w/2+k*w/9:.0f},{yb-h} V{yb}" stroke="#3A2A1C" stroke-width="8" opacity="0.8"/>' for k in range(10)))

def cage_front(x, yb, w, h):
    o = [f'<path d="M{x-w/2-20},{yb} H{x+w/2+20} V{yb+40} H{x-w/2-20} Z" fill="#4A3220" stroke="#1A1410" stroke-width="6" filter="url(#t_ahsap)"/>',
         f'<path d="M{x-w/2-30},{yb-h-30} H{x+w/2+30} V{yb-h} H{x-w/2-30} Z" fill="#4A3220" stroke="#1A1410" stroke-width="6" filter="url(#t_ahsap)"/>']
    for k in range(10):
        xx = x - w / 2 + k * w / 9
        o.append(f'<rect x="{xx-9:.0f}" y="{yb-h}" width="18" height="{h}" fill="#5A3E26" stroke="#1A1410" stroke-width="5"/><path d="M{xx-4:.0f},{yb-h+10} V{yb-10}" stroke="#9A7A52" stroke-width="2.5" opacity="0.7"/>')
    o.append(f'<path d="M{x-w/2},{yb-h*0.5} H{x+w/2}" stroke="#1A1410" stroke-width="16"/><path d="M{x-w/2},{yb-h*0.5} H{x+w/2}" stroke="#5A3E26" stroke-width="8"/>')
    o.append(f'<g transform="translate({x+w*0.3},{yb-h*0.5})"><rect x="-18" y="-6" width="36" height="34" rx="6" fill="#4A4A4E" stroke="#1A1410" stroke-width="4"/><path d="M-10,-6 Q0,-30 10,-6" stroke="#4A4A4E" stroke-width="7" fill="none"/></g>')
    o.append(f'<path d="M{x-w/2-30},{yb-h-30} H{x+w/2+30}" stroke="#C8D4DC" stroke-width="3" opacity="0.6"/>')
    return "".join(o)

def k25a():
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    draw(c, svg_sprite(sky_dusk("s25", [(0, "#3A4248"), (1, "#7A8484")], 700)), 0, 0, 1.0)
    draw(c, blurred(svg_sprite(cloud_band(2501, 14, -100, 2000, 40, 380, "#2E363C", "#6A7478", 0.95, rx=(240, 520), ry=(30, 70))), 5), 0, 0, 1.0)
    draw(c, blurred(svg_sprite(VB.forest(-60, 1980, lambda x: 520 + 20 * math.sin(x / 140), 180, 360, 46, 2502, col="#2E3A34", lit="#4A564E", dark="#1E2622")), 4), 0, 0, 1.0, a=0.7)
    draw(c, blurred(svg_sprite("".join(VB.birch(x, 640, h, 2503 + k, dead=True, sc=0.7) for k, (x, h) in enumerate(((140, 420), (1760, 460), (1560, 380))))), 2), 0, 0, 1.0)
    g = [TEXD, '<path d="M0,620 Q960,600 1920,630 L1920,1080 L0,1080 Z" fill="#4A3E30" filter="url(#t_tas)"/>',
         '<path d="M0,700 Q900,660 1920,720 M0,760 Q900,720 1920,790" stroke="#2A221A" stroke-width="22" fill="none" opacity="0.7"/>',
         puddles(2504, 14, 0, 1920, 680, 1060, "#6A7274"), VB.footprints([(200, 900), (500, 880), (800, 870), (1100, 880)], "boot", 1.2, 3),
         "".join(VB.grass_tuft(x, y, 50, k) for k, (x, y) in enumerate(((60, 700), (300, 1040), (1650, 1020), (1850, 760), (980, 1060)))), splashes(2505, 200, 0, 1920, 640, 1080)]
    draw(c, svg_sprite("".join(g)), 0, 0, 1.0)
    # öküz (sola çekiyor), araba, kafes, içinde Ragnar
    cx, yb = 1080, 780
    draw(c, svg_sprite('<g transform="translate(1240,0) scale(-1,1)">' + VB.ox(620, 800, 0.85) + '</g>'), 0, 0, 1.0)
    draw(c, svg_sprite('<path d="M760,700 L860,720" stroke="#1A1410" stroke-width="18"/><path d="M760,700 L860,720" stroke="#6A4A2E" stroke-width="10"/>' + cage_back(cx, yb, 420, 330)), 0, 0, 1.0)
    rs = sitting(dict(RGO, cloak="#2A3040"), ex("cold", IF.blink_at(0.7)), 1.0, look=-0.2)
    glow(c, cx, yb - 150, 220, "#C8D4DC", 0.18); rim(c, rs, cx, yb + 10, 0.5, "#E8F0F4", dx=-5, dy=-3, a=0.85); draw(c, rs, cx, yb + 10, 0.5); shade_side(c, rs, cx, yb + 10, 0.3, cx - 100, cx + 200, "#10141A")
    draw(c, svg_sprite(TEXD + chain(cx - 60, yb - 120, cx - 200, yb - 20, 40, 30) + cage_front(cx, yb, 420, 330) + wheel(cx - 150, yb + 60, 80) + wheel(cx + 160, yb + 60, 80)), 0, 0, 1.0)
    soft_shadow(c, cx, yb + 140, 300, 20, 0.45)
    for k, (x, y, sc, f_) in enumerate(((1460, 880, 0.48, -1), (1640, 760, 0.36, -1), (360, 760, 0.36, -1), (1300, 660, 0.24, -1))):
        fig(c, saxon(k + 30, torch_=(k == 1)), "cold", x, y, sc, facing=f_, view="side" if False else None, look=-0.5, rimc="#C8D4DC", rdx=4, shx=(x - 80, x + 80), shc="#10141A") if False else fig(c, saxon(k + 30), "cold", x, y, sc, facing=f_, look=-0.5, rimc="#C8D4DC", rdx=4, shx=(x - 80, x + 80), shc="#10141A")
    draw(c, svg_sprite(wyvern_banner(1300, 360, 60, 110, seed=5)), 0, 0, 1.0, a=0.7)
    draw(c, blurred(svg_sprite("".join(f'<path d="M{x},1100 Q{x+40},{960} {x+120},{900+k*10}" stroke="#1E2A1C" stroke-width="{20+k*3}" fill="none" stroke-linecap="round"/>' for k, x in enumerate((-40, 40, 1760, 1840)))
                               + "".join(f'<ellipse cx="{x}" cy="{y}" rx="60" ry="20" fill="#24321E" transform="rotate({-30+(x%60)} {x} {y})"/>' for x, y in ((40, 930), (110, 980), (1800, 940), (1880, 990), (1700, 1010)))), 8), 0, 0, 1.0)
    rain(c, 2506, 1100, ang=14); rain(c, 2507, 140, L=(140, 220), ang=14, a=(0.25, 0.5), w=(2, 3.5))
    smoke(c, 2508, 6, (0, 500, 1920, 760), "#A8B0B4", 0.18)
    finish(c, cold=True, warm=0.0); return s

# ================================================================ k25b · sisli vizyon: Kâhin
def k25b():
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    draw(c, svg_sprite(sky_dusk("s25b", [(0, "#1E2A2E"), (0.6, "#4A5E60"), (1, "#8AA09C")], 1080)), 0, 0, 1.0)
    draw(c, blurred(svg_sprite(VB.forest(-60, 1980, lambda x: 640 + 30 * math.sin(x / 110), 200, 420, 40, 2511, col="#2A3A3A", lit="#3E5250", dark="#1A2626")), 7), 0, 0, 1.0, a=0.6)
    glow(c, 1360, 560, 520, "#C8F0E8", 0.35); bloom_spot(c, 1360, 520, 140, "#E8FFF8", 0.25)
    g = [TEXD, '<path d="M0,760 Q960,730 1920,770 L1920,1080 L0,1080 Z" fill="#2E3A36" filter="url(#t_tas)"/>',
         "".join(VB.birch(x, yb, h, 2512 + k, dead=True, sc=0.9, lean=ln) for k, (x, yb, h, ln) in enumerate(((1060, 790, 520, -0.1), (1720, 800, 600, 0.12)))),
         "".join(f'<g transform="translate({x},{y})"><path d="M-30,0 L-26,-{h} Q0,-{h+20} 26,-{h} L30,0 Z" fill="#5A645E" stroke="#1A1410" stroke-width="5" filter="url(#t_tas)"/><path d="M-10,-{h*0.7:.0f} l8,20 l8,-20 M2,-{h*0.4:.0f} v24" stroke="#2A3430" stroke-width="3" fill="none"/></g>' for x, y, h in ((1180, 790, 120), (1560, 800, 150), (1820, 790, 90))),
         "".join(VB.grass_tuft(x, y, 46, k, frost=0.3) for k, (x, y) in enumerate(((1100, 820), (1500, 860), (1700, 840), (1260, 900))))]
    draw(c, svg_sprite("".join(g)), 0, 0, 1.0)
    smoke(c, 2513, 10, (900, 600, 1920, 900), "#C8DCD8", 0.3, 20)
    fs = full(SEER_ST, "neutral", 0.9, facing=-1, look=-0.4)
    soft_shadow(c, 1380, 846, 130, 16, 0.45); rim(c, fs, 1380, 850, 0.8, "#D8FFF4", dx=5, dy=-4, a=0.8); draw(c, fs, 1380, 850, 0.8); shade_side(c, fs, 1380, 850, 0.4, 1200, 1500, "#0A1414")
    for k in range(40): q = R_(k + 2514); c.drawCircle(q.uniform(1100, 1650), q.uniform(250, 850), q.uniform(1, 3), skia.Paint(AntiAlias=True, Color4f=col("#E8FFF8", q.uniform(0.15, 0.5))))
    smoke(c, 2515, 8, (1000, 760, 1920, 960), "#D8E8E4", 0.35, 18)
    # sol ön: kafes içinde Ragnar (sağa, Kâhin'e bakar)
    draw(c, svg_sprite(TEXD + '<rect x="0" y="0" width="760" height="1080" fill="#141A1C" opacity="0.6"/>'), 0, 0, 1.0)
    ragnar_bust(c, dict(RGO, cloak="#2A3040"), "cold", 400, 470, 1.55, look=0.9, rimc="#C8F0E8", shx=(200, 520), shc="#0A1012", phase=0.8)
    bars = [TEXD] + [f'<rect x="{x-16}" y="-20" width="32" height="1120" fill="#3A2A1C" stroke="#0E0A06" stroke-width="6"/><path d="M{x-6},0 V1080" stroke="#7A9A94" stroke-width="3" opacity="0.6"/>' for x in (120, 330, 560, 760)]
    bars.append('<rect x="-20" y="880" width="820" height="40" fill="#3A2A1C" stroke="#0E0A06" stroke-width="6"/>')
    draw(c, svg_sprite("".join(bars)), 0, 0, 1.0)
    vign(c, 0.68, 0.5, 0.7, 0.8, "#040808")
    finish(c, cold=True, warm=0.0); return s

# ================================================================ k26a · Ella'nın sarayı
def k26a():
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    o = [TEXD, '<rect width="1920" height="1080" fill="#2A2622"/>', VA.stone_wall(0, 0, 1920, 900, seed=81, wash=0.3)]
    for x in (360, 960, 1560): o.append(f'<path d="M{x-40},420 L{x-40},180 Q{x},130 {x+40},180 L{x+40},420 Z" fill="#8AA0B4" stroke="#1A1410" stroke-width="8"/><path d="M{x},150 V420" stroke="#1A1410" stroke-width="6"/>')
    for x in (640, 1280): o.append(wyvern_banner(x, 200, 140, 380, "#1E3A2A", "#B8C0C8", seed=x, wet=False).replace("M-40,40 Q-60,0", "M-40,40 Q-60,0"))
    o.append('<path d="M0,900 L1920,900 L1920,1080 L0,1080 Z" fill="#3A342E"/>' + VP.stones(0, 900, 1920, 1080, 2601, pal=("#4A443E", "#3E3A34", "#55504A"), row=(20, 40), wd=(60, 160)))
    o.append('<path d="M780,900 L1140,900 L1300,1080 L620,1080 Z" fill="#3A2A22" opacity="0.8"/>')
    # taht: oymalı, yüksek arkalık
    o.append('<g transform="translate(1180,860)"><path d="M-150,0 L-150,-420 Q0,-500 150,-420 L150,0 Z" fill="#3A2A1C" stroke="#1A1410" stroke-width="8" filter="url(#t_ahsap)"/>'
             '<path d="M-120,-380 Q0,-450 120,-380" stroke="#B8C0C8" stroke-width="6" fill="none"/><circle cy="-410" r="20" fill="#1E3A2A" stroke="#B8C0C8" stroke-width="5"/>'
             '<rect x="-190" y="-20" width="380" height="60" fill="#4A3A2A" stroke="#1A1410" stroke-width="6"/></g>')
    draw(c, blurred(svg_sprite("".join(o)), 2), 0, 0, 1.0)
    VA.beam(c, 960, 160, 80, 600, 1080, 520, "#C8D8E8", 0.18, 16); VA.beam(c, 360, 160, 80, 300, 1080, 420, "#C8D8E8", 0.1, 16)
    es = sitting(ELLA, ex("cold", IF.blink_at(1.4)), 1.0, look=-0.6)
    rim(c, es, 1180, 900, 0.62, "#C8D8E8", dx=-4, dy=-3, a=0.6); draw(c, es, 1180, 900, 0.62); shade_side(c, es, 1180, 900, 0.45, 1180, 1400, "#0E1218")
    pr = dict(monk(7), tunic="#2A2A2E", cloak="#1A1A1E", _hand_extra=STAFF.replace("M6,-330 q-20,-20 -6,-44 q20,-6 22,18", "M-34,-380 H46 M6,-440 V-300").replace("#6A4C30", "#C9A25A"))
    fig(c, pr, "cold", 1420, 900, 0.56, facing=-1, look=-0.5, rimc="#C8D8E8", shx=(1400, 1600), shc="#0E1218")
    for k, (x, sc) in enumerate(((1640, 0.5), (1800, 0.6), (820, 0.48))):
        fig(c, saxon(k + 40), "cold", x, 900 + (40 if sc > 0.55 else 0), sc, facing=-1 if x > 1000 else 1, look=-0.4, rimc="#FFB060", shx=(x - 70, x + 90), shc="#0E1218")
    torch(c, 1560, 520, t, 1.0); torch(c, 760, 520, t, 1.0)
    # Ragnar ön sol: zincirli bilekler, meydan okuyan bakış
    RC = arm_pts(RGO, [(52, SHY + 16), (90, SHY + 170), (60, SHY + 300)], "fist")
    ragnar_bust(c, dict(RC, cloak="#2A2E36"), "defiant", 470, 470, 1.6, look=0.85, rimc="#E0E8F0", shx=(240, 520), shc="#0A0C10", phase=0.3)
    ch = [TEXD, chain(560, 1000, 900, 1100, 40, 34), chain(380, 1010, 120, 1100, 30, 30),
          '<g transform="translate(470,990)"><rect x="-120" y="-24" width="240" height="44" rx="12" fill="#5A5E64" stroke="#1A1410" stroke-width="6"/><path d="M-110,-14 H110" stroke="#B8C0C8" stroke-width="3"/><circle cx="-80" r="7" fill="#2A2A2A"/><circle cx="80" r="7" fill="#2A2A2A"/></g>']
    draw(c, svg_sprite("".join(ch)), 0, 0, 1.0)
    card_at(c, "KRAL ELLA", 1180, 230, "Northumbria", 0.85)
    finish(c, cold=True, warm=0.03); return s

# ================================================================ k26b · çukurun kenarı
def k26b():
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    draw(c, svg_sprite(sky_dusk("s26b", [(0, "#2A2A34"), (0.6, "#6A5A5E"), (1, "#B8907A")], 560)), 0, 0, 1.0)
    draw(c, blurred(svg_sprite(cloud_band(2621, 14, -100, 2000, 40, 380, "#2A2830", "#9A7A72", 0.95, lit_dy=6, rx=(240, 520), ry=(30, 70))), 5), 0, 0, 1.0)
    o = [TEXD, ridge_svg([(0, 430), (400, 400), (900, 440), (1400, 410), (1920, 440)], 560, "#3E3A40"), VP.wall(200, 1720, 330, 540, 2622, merlons=True, slits=True, lit="#C8A890", lita=0.1),
         '<path d="M0,540 Q960,520 1920,550 L1920,1080 L0,1080 Z" fill="#4A4036" filter="url(#t_tas)"/>']
    draw(c, blurred(svg_sprite("".join(o)), 3), 0, 0, 1.0)
    # çukur: büyük oval, taş ağız, içi zifiri
    pit = [TEXD, '<defs><radialGradient id="pg" cx="0.5" cy="0.35" r="0.65"><stop offset="0" stop-color="#020304"/><stop offset="0.7" stop-color="#080A0A"/><stop offset="1" stop-color="#1E1A16"/></radialGradient></defs>',
           '<ellipse cx="960" cy="860" rx="820" ry="250" fill="url(#pg)"/>', '<path d="M140,860 Q960,600 1780,860" stroke="#2A221C" stroke-width="40" fill="none" opacity="0.8"/>']
    r = R_(2623)
    for k in range(58):
        a = math.pi * 2 * k / 58; x = 960 + 840 * math.cos(a); y = 860 + 262 * math.sin(a); w_ = r.uniform(60, 110); h_ = r.uniform(30, 50) * (1 + 0.5 * max(0, math.sin(a)))
        pit.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{w_/2:.0f}" ry="{h_/2:.0f}" fill="{r.choice(["#6A6258", "#5A5248", "#7A7266"])}" stroke="#1A1410" stroke-width="4" filter="url(#t_tas)"/>'
                   f'<path d="M{x-w_*0.35:.0f},{y-h_*0.3:.0f} Q{x:.0f},{y-h_*0.5:.0f} {x+w_*0.35:.0f},{y-h_*0.3:.0f}" stroke="#C8A890" stroke-width="3" fill="none" opacity="0.6"/>')
    for k in range(12): x = r.uniform(300, 1600); pit.append(f'<path d="M{x:.0f},{620+abs(x-960)*0.1:.0f} q{r.uniform(-20,20):.0f},40 {r.uniform(-10,10):.0f},{r.uniform(60,120):.0f}" stroke="#3A2E22" stroke-width="5" fill="none"/>')
    draw(c, svg_sprite("".join(pit)), 0, 0, 1.0)
    iw = [TEXD, '<defs><linearGradient id="iw" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5A4434"/><stop offset="1" stop-color="#050404" stop-opacity="0"/></linearGradient>'
          '<clipPath id="pc"><ellipse cx="960" cy="860" rx="800" ry="240"/></clipPath></defs><g clip-path="url(#pc)"><path d="M140,860 Q960,580 1780,860 L1780,800 Q960,640 140,800 Z" fill="url(#iw)"/>'
          '<path d="M160,800 Q960,600 1760,800 L1760,1000 Q960,860 160,1000 Z" fill="url(#iw)" opacity="0.8" filter="url(#t_tas)"/>']
    r2 = R_(2626)
    for k in range(30): x = r2.uniform(250, 1650); y = 650 + abs(x - 960) * 0.18 + r2.uniform(0, 90); iw.append(f'<path d="M{x:.0f},{y:.0f} q{r2.uniform(-14,14):.0f},30 {r2.uniform(-8,8):.0f},{r2.uniform(40,90):.0f}" stroke="#2A2018" stroke-width="{r2.uniform(3,6):.0f}" fill="none"/>')
    iw.append('</g>'); draw(c, svg_sprite("".join(iw)), 0, 0, 1.0)
    glow(c, 960, 760, 380, "#FF9A40", 0.12)
    snake_shadows(c, 2624, 14, (520, 900, 1400, 1050), 0.7, "#6A8A60")
    # uzak kenar: Ella ve askerler aşağı bakıyor (meşaleler)
    for k, (x, sp, e, sc) in enumerate(((680, saxon(50, True), "cold", 0.42), (820, saxon(51), "cold", 0.44), (1100, saxon(52), "cold", 0.44), (1250, saxon(53, True), "cold", 0.42))):
        fig(c, sp, e, x, 640, sc, facing=1 if x < 960 else -1, look=0.0, rimc="#FFB060", shx=(x - 60, x + 60), shc="#141018")
    fig(c, ELLA, "cold", 960, 650, 0.5, facing=1, look=0.0, rimc="#FFC890", rdx=-5, shx=(940, 1100), shc="#141018")
    card_at(c, "KRAL ELLA", 960, 230, "", 0.75)
    for x in (680, 1250): glow(c, x, 380, 200, "#FF9A40", 0.3)
    smoke(c, 2625, 6, (300, 700, 1600, 900), "#3A3A38", 0.25, 18)
    draw(c, blurred(svg_sprite(TEXD + '<path d="M-20,1090 L-20,940 Q300,980 520,1090 Z M1940,1090 L1940,930 Q1600,980 1400,1090 Z" fill="#2A241E"/>' + VB.grass_tuft(60, 980, 80, 3) + VB.grass_tuft(1860, 970, 90, 4)), 6), 0, 0, 1.0)
    finish(c, cold=True, warm=0.04); return s

# ================================================================ k26c · çukurda yukarı bakan yüz, gökten ışık
def pit_walls(seed, dark="#1A1612"):
    r = R_(seed); o = [TEXD, f'<rect width="1920" height="1080" fill="{dark}"/>', '<rect width="1920" height="1080" fill="#2A2218" filter="url(#t_tas)" opacity="0.6"/>']
    for k in range(70):
        x = r.uniform(0, 1920); y = r.uniform(0, 1080); w_ = r.uniform(40, 120)
        o.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{w_/2:.0f}" ry="{w_/3:.0f}" fill="{r.choice(["#3A322A", "#2E2822", "#443A30"])}" stroke="#0A0806" stroke-width="3"/>')
    for k in range(16):
        x = r.uniform(0, 1920); o.append(f'<path d="M{x:.0f},0 q{r.uniform(-40,40):.0f},{r.uniform(80,160):.0f} {r.uniform(-20,20):.0f},{r.uniform(160,320):.0f}" stroke="#4A3A28" stroke-width="{r.uniform(3,7):.0f}" fill="none"/>')
    return "".join(o)

def k26c():
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    draw(c, blurred(svg_sprite(pit_walls(2631)), 1.8), 0, 0, 1.0); fill(c, "#0A0806", 0.35)
    VA.beam(c, 1120, -40, 380, 960, 1080, 900, "#FFF4D8", 0.3, 24); glow(c, 1000, 300, 600, "#FFE8C0", 0.35)
    ragnar_bust(c, RGO, "serene", 1080, 520, 2.3, look=0.6, rimc="#FFF0D0", shx=(820, 1100), shc="#0A0806", rot=-8, phase=1.0)
    bloom_spot(c, 1060, 420, 160, "#FFF4DC", 0.22)
    for k in range(70): q = R_(k + 2632); c.drawCircle(q.uniform(700, 1400), q.uniform(80, 900), q.uniform(1, 3), skia.Paint(AntiAlias=True, Color4f=col("#FFF4DC", q.uniform(0.15, 0.6))))
    snake_shadows(c, 2633, 7, (60, 900, 560, 1040), 0.5); snake_shadows(c, 2634, 7, (1380, 900, 1880, 1040), 0.5)
    vign(c, 0.53, 0.42, 0.62, 0.92, "#030202", 0.4)
    finish(c, cold=False, warm=0.05); return s

# ================================================================ k26d · gökte iki kuzgun, ışık açılıyor
def k26d():
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    draw(c, svg_sprite(sky_dusk("s26d", [(0, "#4A5A74"), (0.5, "#C8B8A8"), (1, "#FFE8C0")], 1080)), 0, 0, 1.0)
    glow(c, 960, 540, 520, "#FFF4D8", 0.45); bloom_spot(c, 960, 540, 120, "#FFFFF0", 0.45)
    draw(c, blurred(svg_sprite(cloud_band(2641, 16, -100, 2000, 60, 1000, "#5A6074", "#FFE0B0", 0.9, lit_dy=-10, rx=(260, 520), ry=(40, 90)).replace("", "")), 6), 0, 0, 1.0, a=0.75)
    glow(c, 960, 540, 220, "#FFF8E8", 0.4)
    rays(c, 960, 540, 0, 1200, 360, 18, "#FFF0C8", 0.09, 0.0)
    draw(c, svg_sprite(VB.raven(780, 440, 0.95, 1, "fly", 2).replace('<g transform="translate(780,440)', '<g transform="rotate(-30 780 440) translate(780,440)')
                       + VB.raven(1170, 640, 0.8, 1, "fly", 5).replace('<g transform="translate(1170,640)', '<g transform="rotate(150 1170 640) translate(1170,640)')), 0, 0, 1.0)
    # çukur ağzı (alttan bakış): kenarda taş, kök, sarkan otlar
    ring = [TEXD, '<defs><mask id="hole"><rect width="1920" height="1080" fill="#fff"/><ellipse cx="960" cy="540" rx="780" ry="470" fill="#000"/></mask></defs>',
            '<rect width="1920" height="1080" fill="#14100C" mask="url(#hole)"/>', '<rect width="1920" height="1080" fill="#2A2218" filter="url(#t_tas)" opacity="0.6" mask="url(#hole)"/>']
    r = R_(2642)
    for k in range(60):
        a = math.pi * 2 * k / 60; x = 960 + 790 * math.cos(a); y = 540 + 480 * math.sin(a); w_ = r.uniform(70, 130)
        ring.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{w_/2:.0f}" ry="{w_/2.6:.0f}" fill="{r.choice(["#3A322A", "#4A4036", "#2E2822"])}" stroke="#0A0806" stroke-width="4"/>'
                    f'<path d="M{x-w_*0.3:.0f},{y:.0f} Q{960+(x-960)*0.97:.0f},{540+(y-540)*0.97:.0f} {x+w_*0.3:.0f},{y:.0f}" stroke="#FFE0B0" stroke-width="3" fill="none" opacity="0.45"/>')
    for k in range(40):
        a = r.uniform(0, math.pi * 2); x = 960 + 760 * math.cos(a); y = 540 + 460 * math.sin(a); L = r.uniform(40, 120)
        ring.append(f'<path d="M{x:.0f},{y:.0f} q{-(x-960)*0.05:.0f},{-(y-540)*0.05:.0f} {-(x-960)*L/800:.0f},{-(y-540)*L/500:.0f}" stroke="{r.choice(["#3A4A26", "#5A6A34", "#2A3A1E"])}" stroke-width="{r.uniform(3,6):.0f}" fill="none"/>')
    draw(c, blurred(svg_sprite("".join(ring)), 4), 0, 0, 1.0)
    for k in range(50): q = R_(k + 2643); c.drawCircle(q.uniform(400, 1500), q.uniform(200, 900), q.uniform(1, 3), skia.Paint(AntiAlias=True, Color4f=col("#FFF8E8", q.uniform(0.2, 0.6))))
    finish(c, cold=False, warm=0.06); return s

# ================================================================ k27b · fiyorttan yelken açan dev filo
def k27b():
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    draw(c, svg_sprite(sky_dusk("s27b", [(0, "#3A4A6A"), (0.45, "#C88A7A"), (0.8, "#FFC890"), (1, "#FFE4B0")], 640)), 0, 0, 1.0)
    glow(c, 960, 560, 700, "#FFB070", 0.45); bloom_spot(c, 960, 570, 70, "#FFF4D0", 0.8)
    draw(c, blurred(svg_sprite(cloud_band(2701, 14, -100, 2000, 60, 420, "#4A4A66", "#FFB890", 0.9, lit_dy=8, rx=(220, 480), ry=(22, 54))), 4), 0, 0, 1.0)
    rays(c, 960, 570, 270, 1100, 70, 12, "#FFD8A0", 0.07, 0.0)
    mt = (mountain_range(2702, -100, 760, 640, 160, 90, "#3A3450", "#9A7088", snow="#E8C8C8", light=1, snow_y=300, cid="m1")
          + mountain_range(2703, 700, 2020, 640, 180, 90, "#3A3450", "#9A7088", snow="#E8C8C8", light=-1, snow_y=320, cid="m2")
          + mountain_range(2704, -100, 520, 660, 330, 60, "#2A2438", "#6A4A60", light=1, cid="m3") + mountain_range(2705, 1400, 2020, 660, 340, 60, "#2A2438", "#6A4A60", light=-1, cid="m4"))
    draw(c, svg_sprite(mt), 0, 0, 1.0)
    draw(c, svg_sprite(VPR.sea_svg(640, "#FFC890", "#1E2238", 960, 2706, glint="#FFE4A0", wl="#3A3050", hl="#FFC890", gn=170, spread=0.35)), 0, 0, 1.0)
    draw(c, blurred(svg_sprite(cloud_band(2707, 12, -100, 2000, 600, 680, "#E8B898", "#FFE0C0", 0.5, rx=(240, 500), ry=(10, 22))), 6), 0, 0, 1.0)
    r = R_(2708); items = []
    for row, (y, sc, n) in enumerate(((660, 0.07, 26), (680, 0.1, 20), (705, 0.14, 15), (740, 0.2, 11), (790, 0.28, 7))):
        for k in range(n): items.append((r.uniform(300, 1700) if row < 3 else r.uniform(80, 1500), y + r.uniform(-6, 6), sc, r.uniform(0.6, 1.0)))
    draw(c, svg_sprite(fleet_svg(items)), 0, 0, 1.0)
    for row in range(2): VP.ripples(c, 900, 760 + row * 40, 1400, n=6)
    # ön plan: büyük gemi pruvası (sağ), oğullar ayakta
    draw(c, svg_sprite(G.longship(1500, 930, 0.95, sail=True, billow=1.0)), 0, 0, 1.0)
    deck = 930 + 0.95 * -64
    for k, (sp, e, x, sc, f_) in enumerate(((UBBE, "determined", 1260, 0.5, -1), (HVIT, "determined", 1400, 0.48, -1), (SIG, "cold", 1540, 0.49, -1))):
        fig(c, sp, e, x, deck, sc, facing=f_, look=-0.5, rimc="#FFC890", rdx=-5, shx=(x, x + 120), shc="#1A1428", shadow=0)
    fig(c, IVAR_ST, "keen", 1120, deck, 0.5, facing=-1, look=-0.4, rimc="#FFC890", rdx=-5, shx=(1120, 1240), shc="#1A1428", shadow=0)
    draw(c, svg_sprite(G.longship(1500, 930, 0.95, sail=False).replace("", "")), 0, 0, 1.0, a=0.0)
    for k, (x, y) in enumerate([(400, 260), (520, 300), (1500, 240)]): draw(c, svg_sprite(VB.gull(x, y, 0.5, k)), 0, 0, 1.0)
    draw(c, blurred(svg_sprite(TEXD + '<path d="M-20,1090 L-20,820 Q120,800 260,900 Q340,980 380,1090 Z" fill="#1E1A24"/>' + VB.spruce(80, 900, 420, 3, col="#1A1E24", lit="#2A2E38", dark="#0E1014")), 6), 0, 0, 1.0)
    finish(c, cold=False, warm=0.08); return s

# ================================================================ k27c · boş yamaç, gün batımı, iki kuzgun (P1d - Ragnar)
import v3_prolog as VPR
def k27c():
    empty = svg_sprite("")
    old_full, old_ss = VPR.full, VPR.soft_shadow
    VPR.full = lambda *a, **k: empty; VPR.soft_shadow = lambda *a, **k: None
    try: s = VPR.p1d()
    finally: VPR.full, VPR.soft_shadow = old_full, old_ss
    c = s.getCanvas()
    vign(c, 0.6, 0.55, 0.7, 0.55, "#0A0410")
    letterbox(c, 1.0, 70) if "letterbox" in globals() else None
    return s

FR = {"model": model, "k22a": k22a, "k22b": k22b, "k22c": k22c, "k23a": k23a, "k23b": k23b, "k24": k24, "k25a": k25a, "k25b": k25b,
      "k26a": k26a, "k26b": k26b, "k26c": k26c, "k26d": k26d, "k27b": k27b, "k27c": k27c}

CROPS = {"model": [(1100, 280, 640, 420), (400, 280, 720, 420)], "k22b": [(700, 760, 520, 300), (1160, 260, 520, 420)], "k24": [(1000, 460, 400, 300), (420, 220, 640, 500)],
         "k26c": [(640, 160, 680, 600), (0, 820, 700, 260)], "k27b": [(1000, 560, 700, 380), (1500, 600, 420, 360)]}
# ================================================================ REVİZYON (kullanıcı, 20.11): k22c, k25a, k26b
from art3 import hand3
EXP["calmres"] = (6, -2, 0.34, 0.08, "firm", "")
EXP["stunned"] = (16, 16, 0.0, 0.0, "open_o", "")
def tilt_cup(spill=True):
    g = goblet(0, 0, 1.0, True)
    drops = "".join(f'<ellipse cx="{x}" cy="{y}" rx="{r_}" ry="{r_*1.4:.1f}" fill="#7A0E1E" stroke="#1A1410" stroke-width="2"/>' for x, y, r_ in ((70, -96, 7), (92, -66, 6), (108, -30, 5), (80, -40, 4)))
    arc = '<path d="M36,-112 Q70,-112 76,-80" stroke="#7A0E1E" stroke-width="9" fill="none" stroke-linecap="round"/>'
    return f'<g transform="translate(HX,HY) rotate(-58) translate(0,32)">{g}{arc if spill else ""}{drops if spill else ""}</g>'

def k22c():
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    room_bg(c, t, 0.9, 9, 0.4)
    glow(c, 0, 600, 900, "#FF8A3A", 0.35)
    ragnar_bust(c, RGO, "calmres", 560, 450, 1.75, look=0.8, rimc="#FFB060", shx=(560, 900), shc="#120806", rot=10, phase=0.2)
    EC = arm_pts(ECBERT, [(52, SHY + 16), (150, SHY + 120), (250, SHY + 60)], "grip", tilt_cup(), ring=False, knot=False)
    b = fig_bust(EC, ex("stunned", IF.blink_at(9.0)), 0.8, 1.65, flip=True)
    with live(c, 1400, 1080, phase=1.3, breathe=0.002):
        rim(c, b, 1400, 470, 1.0, "#FFB060", dx=-7, dy=-3, a=0.75); draw(c, b, 1400, 470, 1.0); shade_side(c, b, 1400, 470, 0.5, 1450, 1750, "#0A0608")
    draw(c, svg_sprite(table_front(870) + chessboard(960, 920, 540, 5) + goblet(660, 990, 0.85)), 0, 0, 1.0)
    glow(c, 960, 920, 260, "#FFB060", 0.18)
    draw(c, blurred(svg_sprite(TEXD + candle_cluster(1860, 1100, 2, 13)), 9), 0, 0, 1.0)
    embers(c, 2221, 20, (0, 300, 700, 900))
    vign(c, 0.5, 0.45, 0.72, 0.7)
    finish(c, cold=False, warm=0.05); return s

def lantern(x, y, s=1.0):
    return (f'<g transform="translate({x},{y}) scale({s})"><path d="M0,-70 V-30" stroke="#1A1410" stroke-width="5"/><path d="M-22,-30 L22,-30 L28,40 L-28,40 Z" fill="#FFD890" stroke="#1A1410" stroke-width="6"/>'
            '<path d="M-24,-30 L0,-52 L24,-30 Z M-30,40 H30 V52 H-30 Z" fill="#3A3A3E" stroke="#1A1410" stroke-width="5"/><path d="M0,-30 V40 M-26,6 H26" stroke="#2A2A2E" stroke-width="4"/>'
            '<ellipse cx="0" cy="14" rx="7" ry="13" fill="#FFF4D0"/></g>')

def cage_front2(x, yb, w, h, n=8):
    o = [f'<path d="M{x-w/2-24},{yb} H{x+w/2+24} V{yb+44} H{x-w/2-24} Z" fill="#4A3220" stroke="#1A1410" stroke-width="6" filter="url(#t_ahsap)"/>',
         f'<path d="M{x-w/2-34},{yb-h-34} H{x+w/2+34} V{yb-h} H{x-w/2-34} Z" fill="#4A3220" stroke="#1A1410" stroke-width="6" filter="url(#t_ahsap)"/>']
    for k in range(n + 1):
        xx = x - w / 2 + k * w / n
        o.append(f'<rect x="{xx-15:.0f}" y="{yb-h}" width="30" height="{h}" fill="#5E4228" stroke="#1A1410" stroke-width="6" filter="url(#t_ahsap)"/><path d="M{xx-7:.0f},{yb-h+10} V{yb-10}" stroke="#C89A62" stroke-width="3" opacity="0.6"/>'
                 f'<rect x="{xx+4:.0f}" y="{yb-h}" width="11" height="{h}" fill="#000" opacity="0.25"/>')
    for yy in (yb - h + 30, yb - h * 0.5, yb - 30):
        o.append(f'<rect x="{x-w/2-20}" y="{yy-10:.0f}" width="{w+40}" height="20" fill="#4A4E54" stroke="#1A1410" stroke-width="5"/><path d="M{x-w/2-16},{yy-6:.0f} H{x+w/2+16}" stroke="#A8B0B8" stroke-width="2.5" opacity="0.7"/>'
                 + "".join(f'<circle cx="{x-w/2+k*w/n:.0f}" cy="{yy:.0f}" r="5" fill="#2A2C30" stroke="#C8D0D8" stroke-width="1.5"/>' for k in range(n + 1)))
    o.append(f'<g transform="translate({x+w*0.32},{yb-h*0.5+18})"><rect x="-20" y="-4" width="40" height="38" rx="6" fill="#4A4A4E" stroke="#1A1410" stroke-width="4"/><path d="M-11,-4 Q0,-30 11,-4" stroke="#4A4A4E" stroke-width="8" fill="none"/></g>')
    o.append(f'<path d="M{x-w/2-34},{yb-h-34} H{x+w/2+34}" stroke="#C8D4DC" stroke-width="3" opacity="0.6"/>')
    return "".join(o)

def k25a():
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    draw(c, svg_sprite(sky_dusk("s25", [(0, "#3A4248"), (1, "#7A8484")], 700)), 0, 0, 1.0)
    draw(c, blurred(svg_sprite(cloud_band(2501, 14, -100, 2000, 40, 380, "#2E363C", "#6A7478", 0.95, rx=(240, 520), ry=(30, 70))), 5), 0, 0, 1.0)
    draw(c, blurred(svg_sprite(VB.forest(-60, 1980, lambda x: 470 + 20 * math.sin(x / 140), 180, 360, 46, 2502, col="#2E3A34", lit="#4A564E", dark="#1E2622")), 4), 0, 0, 1.0, a=0.7)
    draw(c, blurred(svg_sprite("".join(VB.birch(x, 600, h, 2503 + k, dead=True, sc=0.7) for k, (x, h) in enumerate(((120, 420), (1800, 460))))), 2), 0, 0, 1.0)
    g = [TEXD, '<path d="M0,580 Q960,560 1920,590 L1920,1080 L0,1080 Z" fill="#4A3E30" filter="url(#t_tas)"/>',
         '<path d="M0,700 Q900,660 1920,720 M0,800 Q900,760 1920,830" stroke="#2A221A" stroke-width="26" fill="none" opacity="0.7"/>',
         puddles(2504, 12, 0, 1920, 640, 1060, "#6A7274", "#FFC890"), VB.footprints([(150, 980), (450, 960), (750, 950)], "boot", 1.3, 3),
         "".join(VB.grass_tuft(x, y, 54, k) for k, (x, y) in enumerate(((60, 660), (1650, 1040), (1850, 700)))), splashes(2505, 220, 0, 1920, 600, 1080)]
    draw(c, svg_sprite("".join(g)), 0, 0, 1.0)
    cx, yb, w, h = 1060, 820, 600, 500
    draw(c, svg_sprite('<g transform="translate(860,0) scale(-1,1)">' + VB.ox(430, 830, 0.95) + '</g>'), 0, 0, 1.0)
    glow(c, 430, 640, 260, "#FFA050", 0.18)
    draw(c, svg_sprite('<path d="M560,720 L740,760" stroke="#1A1410" stroke-width="20"/><path d="M560,720 L740,760" stroke="#6A4A2E" stroke-width="11"/>'
                       + f'<rect x="{cx-w/2}" y="{yb-h}" width="{w}" height="{h}" fill="#2A2018"/>' + "".join(f'<path d="M{cx-w/2+k*w/8:.0f},{yb-h} V{yb}" stroke="#3A2A1C" stroke-width="12" opacity="0.8"/>' for k in range(9))), 0, 0, 1.0)
    glow(c, cx + 180, yb - h + 60, 420, "#FFB060", 0.55); glow(c, cx, yb - 250, 260, "#FFC070", 0.3)
    # Ragnar: kambur oturuyor, sağ eli parmaklıkta (yüz fenere dönük)
    RC = arm_pts(dict(RGO, cloak="#2A3040"), [(52, SHY + 16), (140, SHY + 40), (200, SHY - 80)], "grip")
    c.save(); c.clipRect(skia.Rect(cx - w / 2, yb - h, cx + w / 2, yb))
    ragnar_bust(c, RC, "cold", cx + 50, yb - 350, 1.3, look=0.7, rimc="#FFD080", shx=(cx - 250, cx - 60), shc="#140C08", rot=0, phase=0.7)
    glow(c, cx + 80, yb - 360, 200, "#FFC070", 0.3); c.restore()
    hx, hy = cx - 60 + 1.05 * 80 / 82 * (230 - 8) * math.cos(math.radians(14)), 0
    cf = [TEXD, cage_front2(cx, yb, w, h, 6), lantern(cx + 230, yb - h - 34 + 80, 1.1), '<path d="M' + f'{cx+230},{yb-h-34} V{yb-h+12}" stroke="#1A1410" stroke-width="5"/>',
          hand3(cx + 300, yb - 314, 27, "#EEC6A2", "grip", 1),
          wheel(cx - 190, yb + 70, 96) + wheel(cx + 200, yb + 70, 96), chain(cx - 260, yb - 40, cx - 340, yb + 60, 20, 16)]
    draw(c, svg_sprite("".join(cf)), 0, 0, 1.0)
    bloom_spot(c, cx + 230, yb - h + 60, 40, "#FFF4D0", 0.8); glow(c, cx + 230, yb - h + 60, 160, "#FFD080", 0.45)
    soft_shadow(c, cx, yb + 160, 360, 22, 0.5)
    fig(c, saxon(31, torch_=True), "cold", 1580, 1000, 0.62, facing=-1, look=-0.5, rimc="#FFB060", rdx=-5, shx=(1560, 1720), shc="#10141A")
    glow(c, 1500, 560, 300, "#FF9A40", 0.35)
    fig(c, saxon(33), "cold", 1760, 760, 0.4, facing=-1, look=-0.4, rimc="#FFB060", shx=(1700, 1820), shc="#10141A")
    fig(c, saxon(34), "cold", 660, 620, 0.28, facing=-1, look=-0.4, rimc="#C8D4DC", shx=(260, 380), shc="#10141A")
    draw(c, blurred(svg_sprite("".join(f'<path d="M{x},1100 Q{x+40},{960} {x+120},{900+k*10}" stroke="#1E2A1C" stroke-width="{20+k*3}" fill="none" stroke-linecap="round"/>' for k, x in enumerate((-40, 40, 1800, 1880)))), 8), 0, 0, 1.0)
    rain(c, 2506, 1000, ang=14); rain(c, 2507, 120, L=(140, 220), ang=14, a=(0.25, 0.5), w=(2, 3.5))
    smoke(c, 2508, 5, (0, 480, 1920, 640), "#A8B0B4", 0.16)
    finish(c, cold=True, warm=0.03); return s

def k26b():
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    draw(c, svg_sprite(sky_dusk("s26b", [(0, "#2A2A34"), (0.6, "#5A4E56"), (1, "#8A7068")], 520)), 0, 0, 1.0)
    draw(c, blurred(svg_sprite(cloud_band(2621, 14, -100, 2000, 40, 360, "#2A2830", "#8A6A66", 0.95, lit_dy=6, rx=(240, 520), ry=(30, 70))), 5), 0, 0, 1.0)
    draw(c, blurred(svg_sprite(TEXD + VP.wall(500, 1960, 250, 460, 2622, merlons=True, slits=True, lit="#C8A890", lita=0.1) + '<path d="M0,450 Q960,440 1920,460 L1920,1080 L0,1080 Z" fill="#3E362E" filter="url(#t_tas)"/>'), 3), 0, 0, 1.0)
    # çukur: taş örgülü derin kuyu (uzak iç duvar görünür), alt zifiri
    cx, cy, rx, ry = 1180, 760, 760, 300
    pit = [TEXD, f'<defs><clipPath id="pc2"><ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}"/></clipPath><linearGradient id="dk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity="0"/><stop offset="0.55" stop-color="#030404" stop-opacity="0.85"/><stop offset="1" stop-color="#010202"/></linearGradient></defs>',
           f'<g clip-path="url(#pc2)"><rect x="0" y="0" width="1920" height="1080" fill="#3A322A"/>', VP.stones(300, 440, 1960, 1080, 2627, pal=("#5A5046", "#4A4238", "#665A4E", "#3E362E"), row=(26, 44), wd=(50, 120), ink="#141010")]
    r = R_(2628)
    for k in range(26): x = r.uniform(450, 1900); y = r.uniform(470, 760); pit.append(f'<path d="M{x:.0f},{y:.0f} q{r.uniform(-10,10):.0f},40 {r.uniform(-4,4):.0f},{r.uniform(60,140):.0f}" stroke="#B8C8D0" stroke-width="2" opacity="0.35"/>')   # ıslak izler
    for k in range(16): x = r.uniform(450, 1900); pit.append(f'<path d="M{x:.0f},{470+abs(x-cx)*0.08:.0f} q{r.uniform(-30,30):.0f},50 {r.uniform(-14,14):.0f},{r.uniform(90,200):.0f} q{r.uniform(-10,10):.0f},30 {r.uniform(-20,20):.0f},50" stroke="#2A1E14" stroke-width="{r.uniform(4,9):.0f}" fill="none" stroke-linecap="round"/>')   # kökler
    pit.append(f'<rect x="0" y="560" width="1920" height="520" fill="url(#dk)"/></g>')
    for k in range(40):   # ağız taşları
        a = math.pi + math.pi * k / 39; x = cx + (rx + 10) * math.cos(a); y = cy + (ry + 6) * math.sin(a); w_ = r.uniform(70, 120)
        pit.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{w_/2:.0f}" ry="{w_/4:.0f}" fill="{r.choice(["#6A6258", "#5A5248", "#7A7266"])}" stroke="#1A1410" stroke-width="4" filter="url(#t_tas)"/>'
                   f'<path d="M{x-w_*0.35:.0f},{y-w_*0.12:.0f} Q{x:.0f},{y-w_*0.24:.0f} {x+w_*0.35:.0f},{y-w_*0.12:.0f}" stroke="#FFB070" stroke-width="3" fill="none" opacity="0.7"/>')
    draw(c, svg_sprite("".join(pit)), 0, 0, 1.0)
    glow(c, 1200, 960, 520, "#3A4A40", 0.55)
    snake_shadows(c, 2624, 12, (700, 880, 1700, 1020), 0.9, "#8AAA80")
    glow(c, 1300, 520, 420, "#FF9A40", 0.28)
    # uzak kenar: askerler ve rahip meşalelerle aşağı bakıyor
    for k, (x, sp, sc) in enumerate(((1000, saxon(50, True), 0.4), (1260, dict(monk(7), tunic="#2A2A2E", cloak="#1A1A1E", _arm_up=True, _hand_extra=STAFF.replace("M6,-330 q-20,-20 -6,-44 q20,-6 22,18", "M-34,-380 H46 M6,-440 V-300").replace("#6A4C30", "#C9A25A")), 0.42),
                                    (1480, saxon(52, True), 0.4), (1700, saxon(53), 0.38))):
        fig(c, sp, "cold", x, 470, sc, facing=-1, look=-0.2, rimc="#FFB060", rdx=4, shx=(x - 60, x + 60), shc="#141018", shadow=0.3)
    for x in (1000, 1480): glow(c, x, 300, 200, "#FF9A40", 0.35)
    # Aelle: büyük, ön plan sol, profil, çukura bakıyor
    eb = fig_bust(ELLA, ex("cold", IF.blink_at(1.7)), 0.7, 1.55)   # standart art3 "3q" baş; çukura (sağa) bakar
    c.save(); c.translate(400, 900); c.rotate(7); c.translate(-400, -900)
    with live(c, 400, 1080, phase=1.7, breathe=0.004):
        rim(c, eb, 400, 470, 1.0, "#FFB060", dx=7, dy=-3, a=0.85); draw(c, eb, 400, 470, 1.0); shade_side(c, eb, 400, 470, 0.5, 560, 160, "#0A0A10")
    c.restore()
    torch(c, 700, 540, t, 1.6); glow(c, 700, 480, 420, "#FF9A40", 0.3)
    card_at(c, "KRAL ELLA", 380, 170, "Northumbria", 0.85)
    rain(c, 2629, 600, ang=8, a=(0.12, 0.3), L=(30, 70))
    draw(c, blurred(svg_sprite(TEXD + '<path d="M-20,1090 L-20,1010 Q600,1040 1000,1090 Z" fill="#2A241E"/>' + VB.grass_tuft(900, 1080, 90, 4)), 6), 0, 0, 1.0)
    finish(c, cold=True, warm=0.04); return s

FR.update(k22c=k22c, k25a=k25a, k26b=k26b)
CROPS.update(k22c=[(1180, 200, 700, 520), (600, 820, 760, 260)], k25a=[(760, 280, 640, 560), (1360, 400, 500, 600)], k26b=[(80, 240, 720, 560), (700, 760, 1100, 300)])

def contact(ids):
    from PIL import Image
    n = len(ids); rows = (n + 1) // 2
    sheet = Image.new("RGB", (960 * 2 + 30, 560 * rows + 10), "#EDE2CC")
    for k, i in enumerate(ids): sheet.paste(Image.open(f"{OUTS}/{i}.png").convert("RGB").resize((960, 540)), (10 + (k % 2) * 970, 10 + (k // 2) * 560))
    sheet.save(f"{OUTS}/kontakt_son_960.png")
if __name__ == "__main__":
    ids = sys.argv[1:] or list(FR)
    for i in ids:
        T[0] = None; p = f"{OUTS}/{i}.png"
        FR[i]().makeImageSnapshot().save(p, skia.kPNG); print("kare", i, flush=True)
        for k, b in enumerate(CROPS.get(i, []), 1): crop2x(p, b, f"{OUTS}/{i}_crop{k}.png")
    contact([i for i in FR if os.path.exists(f"{OUTS}/{i}.png")])
