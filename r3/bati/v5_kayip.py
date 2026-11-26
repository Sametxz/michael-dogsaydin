"""Bölüm V · Kayıp On Yıl ham kareleri (brief: kurul/BRIEF_bolum5.md). Tek görsel ajan.
python3 v5_kayip.py [model k19a ...] → /home/claude/r3/kayip/<id>.png (+ R13 kırpmaları), kontakt_kayip_960.png
Ortak dosyalara yazmaz. HASSAS: k20a/k20b'de yöntem gösterilmez (boyunda ip/ilmek/asılı beden yok)."""
import sys, os, math, random
sys.path.insert(0, "/home/claude/r3/bati")
from kareler6 import *
import tex
import v3_a as VA, v3_b as VB, v3_c as VC, v4_paris as VP
from v3_c import cloud_band, gradient, flames, soft_shadow, crop2x, breath
from v4_paris import fig, stones, river, fleet_svg, smoke, embers, boulder, fur_pile
from art3 import figure, shade, INK as INK3
OUTK = "/home/claude/r3/kayip"; os.makedirs(OUTK, exist_ok=True)
R_ = random.Random
TEXD = tex.defs("ahsap", "tas", "deri", "kurk", "yun", "metal", "keten")
EXP["weary"] = (-9, 5, 0.50, 0.12, "flat", "")
EXP["hollow2"] = (-12, 6, 0.30, 0.08, "flat", "")
EXP["keen"] = (6, -6, 0.22, 0.10, "smirk", "")
EXP["warm"] = (-8, 4, 0.20, 0.04, "soft_smile", "")
EXP["sky"] = (-10, 6, 0.0, 0.0, "flat", "")

# ================================================================ modeller (art3 gövdesi, özgün)
SNAKE = ('<g transform="translate(50,30)"><path d="M-22,4 q8,-14 18,-4 q10,10 20,-2 q8,-10 16,-2" stroke="#2E4A3A" stroke-width="4.5" fill="none" stroke-linecap="round" opacity="0.85"/>'
         '<ellipse cx="34" cy="-3" rx="6" ry="4" fill="#2E4A3A" opacity="0.85"/><path d="M-22,4 l-8,6" stroke="#2E4A3A" stroke-width="3" opacity="0.85"/>'
         '<circle cx="-8" cy="-34" r="11" fill="none" stroke="#6A8A3A" stroke-width="2.5" opacity="0.7"/></g>')   # Sigurd: göz altında yılan dövmesi + irisi saran ince halka
UBBE = dict(BJv, beardless=False, hair="#C9A462", beard_c="#B08A52", brow_c="#8A6A3A", iris="#5E8CA8", beard_len=1.05, beard_w=1.05, beard_braid=True,
            side_braids=True, tunic="#6A3A26", trim="#C9A25A", cloak="#3A2C22", fur_collar="#8A7458", armring=True, nose2=True, old=False,
            clasp='<g transform="translate(0,-440)"><circle r="15" fill="#C9A25A" stroke="#1A1410" stroke-width="4"/><path d="M-7,-7 L7,7 M7,-7 L-7,7" stroke="#1A1410" stroke-width="3"/></g>')
HVIT = dict(BJv, beardless=False, hair="#E6D49A", beard_c="#D2BC80", brow_c="#B0945A", iris="#6A8AA0", beard_len=0.3, beard_w=0.85, beard_braid=False,
            short_hair=True, side_braids=False, tunic="#3E5A3A", trim="#A8B070", cloak="#5A4A32", fur_collar="#C8B890", armring=False,
            clasp='<g transform="translate(0,-440)"><path d="M0,-16 L14,0 L0,16 L-14,0 Z" fill="#B8C0C4" stroke="#1A1410" stroke-width="4"/></g>')
SIG = dict(BJv, beardless=False, no_blush=True, undercut=True, nobraid=True, hair="#3A2A1E", beard_c="#3A2A1E", stubble="#4E3E30", brow_c="#2A1E14", iris="#7A9A6A",
           beard_len=0.55, beard_w=0.9, beard_braid=False, tunic="#2E3A4A", trim="#8A9AAA", cloak="#1E222A", fur_collar="#4A4A48", armring=True,
           _head_extra=SNAKE, clasp='<g transform="translate(0,-440)"><circle r="14" fill="#5A7A3A" stroke="#1A1410" stroke-width="4"/><ellipse rx="3" ry="9" fill="#1A1410"/></g>')
IVAR = dict(BJv, beardless=True, smooth=True, short_hair=False, side_braids=False, undercut=False, long_braid=False, hair="#4A3424", no_blush=True,
            brow_c="#3A2A1C", iris="#3E9EE6", skin="#EAC6A6", tunic="#1E1C1E", trim="#6A4A8A", cloak="#2A2230", fur_collar="#3A3438",
            armring=True, face_scar=False, knot=False, nose2=True,
            clasp='<g transform="translate(0,-440)"><circle r="14" fill="#8A8E96" stroke="#1A1410" stroke-width="4"/><path d="M-6,6 L0,-8 L6,6" stroke="#1A1410" stroke-width="3" fill="none"/></g>')
RGO = dict(RG, hair="#6A5038", beard_c="#7A6650", stubble="#7A6A58", old=True)   # yaşlanmış Ragnar (kırlaşmış sakal)
RGO["beard_c"] = "#8E806C"

def crutch_svg(x, y, h, rot=0, s=1.0):
    """Koltuk değneği: çatal gövde, koltuk yastığı (deri sargılı), el tutamağı, demir uç."""
    return (f'<g transform="translate({x},{y}) rotate({rot}) scale({s})">'
            f'<path d="M0,0 L-18,{-h*0.62:.0f} L-26,{-h:.0f} M0,0 L18,{-h*0.62:.0f} L26,{-h:.0f}" stroke="#1A1410" stroke-width="22" fill="none" stroke-linecap="round"/>'
            f'<path d="M0,0 L-18,{-h*0.62:.0f} L-26,{-h:.0f} M0,0 L18,{-h*0.62:.0f} L26,{-h:.0f}" stroke="#7A5A3A" stroke-width="13" fill="none" stroke-linecap="round"/>'
            f'<path d="M-4,-4 L-16,{-h*0.6:.0f}" stroke="#B08A5E" stroke-width="3" opacity="0.7"/>'
            f'<rect x="-46" y="{-h-14:.0f}" width="92" height="26" rx="12" fill="#4A3020" stroke="#1A1410" stroke-width="6"/>'
            + "".join(f'<path d="M{-40+k*14},{-h-12:.0f} l6,22" stroke="#2A1A10" stroke-width="3"/>' for k in range(6))
            + f'<rect x="-26" y="{-h*0.55:.0f}" width="52" height="16" rx="6" fill="#5A3E28" stroke="#1A1410" stroke-width="5"/>'
            f'<path d="M-6,0 L6,0 L4,26 L-4,26 Z" fill="#6A7078" stroke="#1A1410" stroke-width="4"/></g>')

def sitting(spec, expr, s=1.0, look=None, view="front"):
    sp = dict(spec)
    return sprite(f'<g transform="translate(500,1240) scale({s})">{figure(sp, view, "sit", expr, look=look)}</g>', 1000, 1300, ax=500, ay=1240, ss=1.0)

def mpose(spec, expr, s=1.0, pose="arms_up", view="front", look=None):
    return sprite(f'<g transform="translate(500,1240) scale({s})">{figure(dict(spec), view, pose, expr, look=look)}</g>', 1000, 1300, ax=500, ay=1240, ss=1.0)

def bench(x, y, w, h=150, seed=3):
    """Oymalı sedir: ahşap oturak, kürk örtü, ejder başlı kol uçları."""
    return (f'<g transform="translate({x},{y})">'
            f'<rect x="{-w/2}" y="{-h}" width="{w}" height="{h}" fill="#4A3220" filter="url(#t_ahsap)" stroke="#1A1410" stroke-width="6"/>'
            f'<rect x="{-w/2}" y="{-h}" width="{w}" height="22" fill="#6A4A2E" stroke="#1A1410" stroke-width="5"/>'
            + "".join(f'<path d="M{-w/2+20+k*(w-40)/6:.0f},{-h+40} q14,30 0,60 q-14,30 0,50" stroke="#2A1A10" stroke-width="5" fill="none" opacity="0.7"/>' for k in range(7))
            + f'<path d="M{-w/2-10},{-h+4} Q{-w/2-40},{-h-50} {-w/2+6},{-h-70} Q{-w/2+30},{-h-60} {-w/2+14},{-h-34}" fill="#5A3E26" stroke="#1A1410" stroke-width="6"/>'
            f'<circle cx="{-w/2+2}" cy="{-h-52}" r="5" fill="#E2B23A"/>'
            f'<path d="M{-w/2+10},{-h} Q0,{-h-26} {w/2-10},{-h} L{w/2-30},{-h+50} Q0,{-h+30} {-w/2+30},{-h+50} Z" fill="#6A5A48" filter="url(#t_kurk)" stroke="#1A1410" stroke-width="4"/>'
            f'<rect x="{-w/2}" y="{-h}" width="{w*0.3:.0f}" height="{h}" fill="#000" opacity="0.18"/></g>')

def model():
    s = skia.Surface(W, H); c = s.getCanvas()
    bg = [TEXD, '<defs>' + gradient("mb", [(0, "#E8DCC4"), (1, "#CDBE9E")]) + '</defs><rect width="1920" height="1080" fill="url(#mb)"/>',
          '<rect width="1920" height="1080" fill="#B8A884" filter="url(#t_keten)" opacity="0.35"/>']
    for k in range(13): bg.append(f'<path d="M40,{90+k*66} H1880" stroke="#8A7A5A" stroke-width="1.5" opacity="0.3"/>')
    bg.append('<path d="M40,880 H1880" stroke="#3A2A1A" stroke-width="4"/>')
    bg.append('<text x="60" y="130" font-family="DejaVu Serif" font-size="30" font-weight="bold" fill="#3A2A1A">MODEL · Ragnar ve yetişkin oğulları (boy karşılaştırma)</text>')
    draw(c, svg_sprite("".join(bg)), 0, 0, 1.0)
    G = 880; S = 1.4
    xs = [230, 570, 910, 1250]
    specs = [(RGO, "weary", "RAGNAR", "yaşlı, kırlaşmış"), (UBBE, "neutral", "UBBE", "en büyük · örgülü sakal"), (HVIT, "tender", "HVITSERK", "en genç · kısa sakal"),
             (SIG, "cold", "SIGURD", "koyu saç · yılan gözü")]
    for (sp, e, nm, sub), x in zip(specs, xs):
        f_ = full(sp, e, 0.9, facing=1, look=0.2); soft_shadow(c, x, G - 6, 120, 14, 0.4); draw(c, f_, x, G, 0.62 * S)
        card_at(c, nm, x, 960, sub, 0.9)
    iv = full(IVAR_ST, "keen", 0.9, facing=-1, look=0.2)
    soft_shadow(c, 1600, G - 4, 140, 16, 0.45); draw(c, iv, 1600, G, 0.62 * S)
    card_at(c, "IVAR", 1600, 960, "bacak destekli · değnek · buz mavisi göz", 0.9)
    finish(c, cold=False, warm=0.02); return s


# ================================================================ ortak ekler
sys.path.insert(0, "/home/claude/r2")
from art2 import limb
from art3 import hand3, knot_mark
import gemi as G
SHY, HIP = -452, -240
HOOD = ('<path d="M-104,70 Q-122,-120 0,-132 Q122,-120 104,70 L88,96 Q96,-58 0,-100 Q-96,-58 -88,96 Z" fill="#2E2A26" stroke="#1A1410" stroke-width="6"/>'
        '<path d="M-96,40 Q-108,-96 -10,-118" stroke="#4E4840" stroke-width="8" fill="none" opacity="0.7"/><path d="M60,-104 Q100,-60 98,40" stroke="#000" stroke-width="16" fill="none" opacity="0.35"/>'
        + "".join(f'<path d="M{-80+k*28},{-100+abs(k-3)*8} l{6-k*2},40" stroke="#1A1410" stroke-width="2" opacity="0.4"/>' for k in range(7)))
CROWN = ('<g transform="translate(HX,HY) rotate(-8)"><ellipse cx="0" cy="-6" rx="66" ry="20" fill="none" stroke="#1A1410" stroke-width="20"/>'
         '<path d="M-64,-8 L-60,-58 L-38,-24 L-18,-70 L0,-28 L20,-70 L38,-24 L60,-58 L64,-8 Q0,18 -64,-8 Z" fill="#D8A93A" stroke="#1A1410" stroke-width="6" stroke-linejoin="round"/>'
         '<path d="M-56,-6 Q0,12 56,-6" stroke="#8A6214" stroke-width="7" fill="none"/><path d="M-40,-30 L-36,-48 M20,-36 L22,-60" stroke="#FFF0B0" stroke-width="5"/>'
         '<circle cx="0" cy="-2" r="8" fill="#8E1E22" stroke="#1A1410" stroke-width="3"/><circle cx="-34" cy="-6" r="6" fill="#2E5A8A" stroke="#1A1410" stroke-width="3"/><circle cx="34" cy="-6" r="6" fill="#2E5A8A" stroke="#1A1410" stroke-width="3"/></g>')

def arm_pts(sp, pts, hand="open", extra="", ring=True, knot=True):
    """Yakın kolu serbest yönle çizer (_noarm + _body_extra): model gövdesi korunur."""
    sp = dict(sp); o = [sp.get("_body_extra", "")]
    o.append(limb(pts, 38, sp["tunic"]))
    if ring and sp.get("armring", True): o.append(f'<circle cx="{(pts[1][0]+pts[2][0])/2:.0f}" cy="{(pts[1][1]+pts[2][1])/2:.0f}" r="23" fill="none" stroke="#D9A93A" stroke-width="8"/>')
    o.append(hand3(pts[-1][0], pts[-1][1], 21, sp.get("skin", "#EEC6A2"), hand, 1))
    if knot and sp.get("knot", True): o.append(knot_mark(pts[-1][0], pts[-1][1] - 2, 0.55))
    o.append(extra.replace("HX", f"{pts[-1][0]}").replace("HY", f"{pts[-1][1]}"))
    sp["_body_extra"] = "".join(o); sp["_noarm"] = True; return sp

def crutch_line(x0, y0, x1, y1, s=1.0):
    """Uç (x0,y0) → koltuk (x1,y1)."""
    h = math.hypot(x1 - x0, y1 - y0); rot = math.degrees(math.atan2(x1 - x0, -(y1 - y0)))
    return crutch_svg(x0, y0, h / s, rot, s)

BRACES = "".join(f'<path d="M{x-24},{-200} L{x2-24},{-30} M{x+24},{-200} L{x2+24},{-30}" stroke="#1A1410" stroke-width="11"/><path d="M{x-24},{-200} L{x2-24},{-30} M{x+24},{-200} L{x2+24},{-30}" stroke="#9AA2AA" stroke-width="5"/>'
                 + "".join(f'<rect x="{x+(x2-x)*q-32:.0f}" y="{-200+170*q-8:.0f}" width="64" height="16" rx="5" fill="#4A2E1C" stroke="#1A1410" stroke-width="4"/>' for q in (0.08, 0.5, 0.92))
                 for x, x2 in ((-26, -32), (30, 38)))
IVAR_ST = dict(IVAR, _body_extra=BRACES + crutch_line(86, 8, 52, -400))   # ayakta: bacak destekleri + değnek (yakın el tutamağı kavrar)
IVAR_ST["fur"] = "#3A3236"

def ivar_seat(c, x, hy, hs, expr, look=0.4, arms=False, rim_c="#FFB070", seed=0):
    """Oturan Ivar: bust (flip, kanonik yön sola) + dizlerini örten kürk + yanında değnek."""
    sp = IVAR
    if arms:   # kollarını açmış: yakın kol öne-yukarı, uzak kol yana
        far = limb([(-52, SHY + 16), (-150, SHY - 10), (-250, SHY - 70)], 34, shade(IVAR["tunic"], 0.8)) + hand3(-250, SHY - 70, 19, shade(IVAR["skin"], 0.92), "open", 1)
        sp = arm_pts(dict(IVAR, _body_extra=far), [(52, SHY + 16), (150, SHY + 40), (262, SHY - 20)], "open", knot=False)
    b = fig_bust(sp, ex(expr, IF.blink_at(0.6 + seed)), look, hs, flip=True)
    with live(c, x, hy + hs * 300, phase=0.6 + seed, breathe=0.005):
        if rim_c: rim(c, b, x, hy, 1.0, rim_c, dx=5, dy=-3, a=0.6)
        draw(c, b, x, hy, 1.0)
    return b

def ragnar_bust(c, spec, expr, x, hy, hs, look=0.3, rimc="#CFE0F0", shx=None, shc="#0E1620", rot=0.0, phase=0.2, flip=False):
    b = fig_bust(spec, ex(expr, IF.blink_at(phase)), look, hs, flip=flip)
    c.save(); c.translate(x, hy + hs * 260); c.rotate(rot); c.translate(-x, -(hy + hs * 260))
    with live(c, x, hy + hs * 300, phase=phase, breathe=0.005):
        if rimc: rim(c, b, x, hy, 1.0, rimc, dx=-6, dy=-3, a=0.7)
        draw(c, b, x, hy, 1.0)
        if shx: shade_side(c, b, x, hy, 0.5, shx[0], shx[1], shc)
    c.restore(); return b

def villager(seed, kid=False):
    r = R_(seed); sp = dict(KL.soldier_spec(seed + 700, "ragnar", None), _head_extra="", armring=False, knot=False, face_scar=False,
                            tunic=r.choice(["#6A5A42", "#4E5A4A", "#7A5A3A", "#5A4A5A", "#6E6A58"]), cloak=r.choice(["#3A3028", "#2E3438", "#4A3A2A"]))
    sp.update(shield=False, _hand_extra="", _carry_svg="", _body_extra="", weapon=None)
    if kid: sp.update(beardless=True, smooth=True, beard_len=0.0)
    if r.random() < 0.35 and not kid: sp.update(female=True, beardless=True, hair=r.choice(["#C8A060", "#8A6040", "#E0C890"]), crown=False, circlet=False, scratch=False)
    return sp

def sky_dusk(gid, stops, h=640):
    return '<defs>' + gradient(gid, stops) + f'</defs><rect width="1920" height="{h}" fill="url(#{gid})"/>'

def ridge_svg(pts, y_base, colr, a=1.0):
    return f'<path d="M-20,{y_base} ' + " ".join(f"L{x},{y}" for x, y in pts) + f' L1940,{y_base} Z" fill="{colr}" opacity="{a}"/>'

# ================================================================ k19a · alacakaranlıkta Kattegat girişi
def palisade(x0, x1, yb, h, seed, gate=None):
    r = R_(seed); o = []
    x = x0
    while x < x1:
        w = r.uniform(26, 36); hh = h * r.uniform(0.92, 1.06)
        if gate and gate[0] < x < gate[1]: x += w; continue
        o.append(f'<path d="M{x:.0f},{yb} L{x:.0f},{yb-hh:.0f} L{x+w/2:.0f},{yb-hh-w*0.9:.0f} L{x+w:.0f},{yb-hh:.0f} L{x+w:.0f},{yb} Z" fill="{r.choice(["#4A3624", "#55402A", "#3E2E1E"])}" stroke="#1A1410" stroke-width="3" filter="url(#t_ahsap)"/>'
                 f'<path d="M{x+w*0.65:.0f},{yb} V{yb-hh:.0f}" stroke="#000" stroke-width="{w*0.35:.0f}" opacity="0.25"/><path d="M{x+3:.0f},{yb-hh+4:.0f} V{yb-6}" stroke="#E8A868" stroke-width="2" opacity="0.35"/>')
        x += w
    o.append(f'<path d="M{x0},{yb-h*0.35:.0f} H{x1}" stroke="#2A1E14" stroke-width="10"/><path d="M{x0},{yb-h*0.75:.0f} H{x1}" stroke="#2A1E14" stroke-width="10"/>')
    return "".join(o)

def gate_posts(cx, yb, w, h):
    o = []
    for sx in (-1, 1):
        px = cx + sx * w / 2
        o.append(f'<rect x="{px-26}" y="{yb-h}" width="52" height="{h}" fill="#4A3424" stroke="#1A1410" stroke-width="5" filter="url(#t_ahsap)"/>'
                 f'<path d="M{px-14},{yb-h+30} q14,24 0,48 q-14,24 0,48 q14,24 0,48" stroke="#2A1A10" stroke-width="6" fill="none"/>'
                 f'<path d="M{px-30},{yb-h} Q{px - 10*sx},{yb-h-70} {px + 34*sx},{yb-h-86} Q{px + 64*sx},{yb-h-80} {px + 52*sx},{yb-h-58} L{px + 30*sx},{yb-h-50} Q{px+8*sx},{yb-h-30} {px+26},{yb-h} Z" fill="#5A3E26" stroke="#1A1410" stroke-width="5"/>'
                 f'<circle cx="{px + 40*sx}" cy="{yb-h-70}" r="5" fill="#E2B23A"/>')
    o.append(f'<path d="M{cx-w/2-40},{yb-h+10} Q{cx},{yb-h-40} {cx+w/2+40},{yb-h+10} L{cx+w/2+40},{yb-h+40} Q{cx},{yb-h-10} {cx-w/2-40},{yb-h+40} Z" fill="#4A3424" stroke="#1A1410" stroke-width="5" filter="url(#t_ahsap)"/>'
             + "".join(f'<path d="M{cx-w/2+k*w/6:.0f},{yb-h+14-26*math.sin(math.pi*k/6):.0f} l0,22" stroke="#C8B080" stroke-width="3" opacity="0.5"/>' for k in range(7)))
    return "".join(o)

def torch(c, x, y, t, s=1.0):
    draw(c, svg_sprite(f'<path d="M{x},{y} L{x+4*s},{y+90*s}" stroke="#1A1410" stroke-width="{12*s}"/><path d="M{x},{y} L{x+4*s},{y+90*s}" stroke="#5A3E26" stroke-width="{7*s}"/><path d="M{x-10*s},{y} h{20*s} v{14*s} h{-20*s} Z" fill="#2A2A2A" stroke="#1A1410" stroke-width="3"/>'), 0, 0, 1.0)
    flames(c, x - 16 * s, x + 16 * s, y, 60 * s, t or 0.0, seed=int(x)); glow(c, x, y - 20 * s, 220 * s, "#FF9A40", 0.35); bloom_spot(c, x, y - 20 * s, 26 * s, "#FFE8B0", 0.7)


APRON = ('<path d="M-46,-380 L58,-384 L66,-176 Q8,-164 -52,-178 Z" fill="#C8BC9E" stroke="#1A1410" stroke-width="5" filter="url(#t_keten)"/>'
         '<path d="M-60,-380 L72,-386" stroke="#6A5A40" stroke-width="7"/><path d="M40,-370 L48,-186" stroke="#000" stroke-width="16" opacity="0.12"/>')
HOODC = lambda colr: (f'<path d="M-100,70 Q-118,-116 0,-128 Q118,-116 100,70 L86,92 Q94,-56 0,-96 Q-94,-56 -86,92 Z" fill="{colr}" stroke="#1A1410" stroke-width="6"/>'
                      f'<path d="M58,-100 Q96,-58 94,40" stroke="#000" stroke-width="14" fill="none" opacity="0.3"/>')
BASKET = ('<g transform="translate(HX,HY)"><path d="M-46,-6 Q-50,56 -30,66 L34,66 Q52,56 48,-6 Z" fill="#9A7442" stroke="#1A1410" stroke-width="5"/>'
          + "".join(f'<path d="M{-44+k*12},0 l2,62" stroke="#6A4A26" stroke-width="3"/>' for k in range(8))
          + '<path d="M-48,20 H50 M-46,42 H48" stroke="#6A4A26" stroke-width="4"/><path d="M-40,-6 Q0,-60 40,-6" stroke="#1A1410" stroke-width="9" fill="none"/><path d="M-40,-6 Q0,-60 40,-6" stroke="#9A7442" stroke-width="5" fill="none"/>'
          '<ellipse cx="-14" cy="-8" rx="16" ry="10" fill="#B8A060" stroke="#1A1410" stroke-width="3"/><ellipse cx="14" cy="-10" rx="14" ry="9" fill="#C8B070" stroke="#1A1410" stroke-width="3"/></g>')
STAFF = ('<g transform="translate(HX,HY)"><path d="M6,-330 Q-6,-100 4,236" stroke="#1A1410" stroke-width="20" fill="none" stroke-linecap="round"/><path d="M6,-330 Q-6,-100 4,236" stroke="#6A4C30" stroke-width="12" fill="none"/>'
         '<path d="M6,-330 q-20,-20 -6,-44 q20,-6 22,18" stroke="#1A1410" stroke-width="9" fill="none"/></g>')
WOOL = ["#7A6A4E", "#5E6650", "#8A6A48", "#6A5A62", "#7E7A64", "#5A4E40", "#8A7E62"]

def civ(seed, kind="man"):
    r = R_(seed); sp = dict(KL.soldier_spec(seed + 700, "ragnar", None))
    for k in ("_head_extra", "_body_extra", "_hand_extra", "_carry_svg"): sp.pop(k, None)
    sp.update(_arm_up=False, armring=False, knot=False, face_scar=False, tunic=r.choice(WOOL), trim=r.choice(["#5A4A32", "#8A7A58", "#4A4A3A"]),
              cloak=r.choice(["#3A3028", "#4A4234", "#2E3430", "#5A4A3A"]), fur_collar=r.choice(["#6A5A48", "#8A7A62", "#5A5048"]), clasp="")
    if kind in ("woman", "mother"):
        sp.update(female=True, beardless=True, hair=r.choice(["#C8A060", "#8A6040", "#E0C890", "#6A4A30"]), crown=False, circlet=False, scratch=False, long_braid=True,
                  _body_extra=APRON, skin="#F0CCAA")
        if kind == "mother": sp["_hand_extra"] = BASKET
    elif kind == "old":
        sp.update(hair="#C8C4BA", beard_c="#D0CCC2", brow_c="#A8A49A", old=True, beard_len=0.9, _hand_extra=STAFF, cloak="#4A4234")
    elif kind == "kid":
        sp.update(beardless=True, smooth=True, beard_len=0.0, cloak=None)
    if kind in ("hood", "old") or (kind == "man" and r.random() < 0.3): sp["_head_extra"] = HOODC(r.choice(["#5A4A3A", "#4A4E46", "#6A5A44"]))
    if kind == "smith": sp["_body_extra"] = APRON.replace("#C8BC9E", "#5A3E28")
    return sp

def k19a_crowd(c):
    # sıra: (x, y, ölçek, tür, ifade, yön, poz)   yön -1: Ragnar'a (sola) bakar
    rows = [
        [(1000, 742, 0.22, "man", "curious", -1, ""), (1090, 744, 0.22, "woman", "neutral", -1, ""), (1180, 740, 0.21, "hood", "curious", -1, ""), (1270, 744, 0.22, "smith", "neutral", -1, ""),
         (1360, 742, 0.21, "woman", "curious", 1, "lean"), (1440, 744, 0.22, "man", "neutral", -1, "")],
        [(930, 790, 0.30, "smith", "curious", -1, "point"), (1040, 796, 0.30, "woman", "shock", -1, "lean"), (1130, 792, 0.31, "man", "curious", 1, "lean"), (1250, 798, 0.32, "old", "cold", -1, ""),
         (1380, 794, 0.30, "hood", "curious", -1, ""), (1480, 798, 0.31, "mother", "neutral", -1, "")],
        [(1600, 860, 0.40, "man", "curious", -1, "point"), (1750, 870, 0.41, "woman", "shock", -1, "lean")]]
    for ri, row in enumerate(rows):
        for k, (x, y, sc, kind, e, f_, pose) in enumerate(row):
            sp = civ(ri * 20 + k + 3, kind)
            if pose == "point": sp = arm_pts(sp, [(52, SHY + 16), (150, SHY + 50), (250, SHY + 30)], "open", knot=False, ring=False)
            fs = full(sp, e, 0.9, facing=f_, look=-0.6 if f_ < 0 else 0.5)
            rot = (-5 * f_) if pose == "lean" else 0.0
            soft_shadow(c, x, y - 4, 200 * sc, 26 * sc, 0.4)
            spr = blurred(fs, 1.2) if ri == 0 else fs
            rim(c, spr, x, y, sc, "#FFB070", dx=4, dy=-2, a=0.5); draw(c, spr, x, y, sc, rot=rot); shade_side(c, spr, x, y, 0.35, x - 70 * sc / 0.3, x + 70 * sc / 0.3, "#1A1020")
            if ri == 0: draw(c, svg_sprite(f'<rect x="{x-60}" y="{y-260}" width="120" height="270" fill="#6A5A70" opacity="0.12"/>'), 0, 0, 1.0)
    for k, (x, y) in enumerate([(1530, 830), (1680, 900)]):   # çocuklar annelerin arkasına kaçışıyor
        fs = full(civ(60 + k, "kid"), "shock", 0.9, facing=1); soft_shadow(c, x, y - 3, 40, 7, 0.35); draw(c, fs, x, y, 0.2 if k == 0 else 0.25, rot=8)

def k19a():
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    draw(c, svg_sprite(sky_dusk("s19", [(0, "#2A2A44"), (0.45, "#6A5A70"), (0.78, "#C8866A"), (1, "#E8B080")], 700)), 0, 0, 1.0)
    draw(c, blurred(svg_sprite(cloud_band(1901, 12, -100, 2000, 60, 300, "#3A3650", "#D89A80", 0.85, lit_dy=8, rx=(220, 460), ry=(18, 44))), 4), 0, 0, 1.0)
    glow(c, 1500, 560, 520, "#FFB880", 0.35)
    r = R_(190); o = [TEXD]
    o.append(ridge_svg([(0, 430), (180, 330), (330, 400), (520, 300), (760, 410), (980, 360), (1200, 440), (1420, 340), (1650, 420), (1920, 360)], 600, "#4A4660"))
    o.append(ridge_svg([(0, 480), (240, 420), (460, 470), (700, 430), (980, 490), (1300, 450), (1560, 500), (1920, 450)], 600, "#3A3848"))
    o.append(river(560, 700, 191, top="#C89A88", mid="#6A6070", bot="#2E2E3A", glint=1500, gcol="#FFD0A0", n=60))
    o.append(fleet_svg([(260, 590, 0.07, 0.0), (420, 596, 0.08, 0.0), (1700, 592, 0.06, 0.0)], sail=False))
    draw(c, blurred(svg_sprite("".join(o)), 1.5), 0, 0, 1.0)
    # köy: çim çatılı evler + duman (orta-arka)
    v = [TEXD]
    for k, (x, y, sc) in enumerate([(820, 640, 0.42), (1080, 630, 0.36), (1420, 640, 0.44), (1700, 650, 0.5), (620, 660, 0.4)]):
        v.append(O7.thatch_house(x, y, sc, smoke=True, light=True))
    draw(c, svg_sprite("".join(v)), 0, 0, 1.0)
    fill_ = svg_sprite(f'<rect y="600" width="1920" height="120" fill="#4A3A4A" opacity="0.25"/>'); draw(c, fill_, 0, 0, 1.0)
    # zemin: çamurlu yol, su birikintisi, ayak izleri
    g = [TEXD, '<path d="M0,700 Q600,680 1920,700 L1920,1080 L0,1080 Z" fill="#4A3E32" filter="url(#t_tas)"/>',
         '<path d="M760,1080 Q960,860 1120,700 L1260,700 Q1300,860 1560,1080 Z" fill="#5E4E3C" opacity="0.8"/>']
    for k in range(260):
        x = r.uniform(0, 1920); y = r.uniform(705, 1080); g.append(f'<path d="M{x:.0f},{y:.0f} l{r.uniform(-12,12):.0f},{r.uniform(-3,3):.0f}" stroke="{r.choice(["#2A2218", "#7A6A54", "#3A3024"])}" stroke-width="{1.5+(y-700)/200:.1f}" opacity="0.6"/>')
    g.append(VB.puddle(1240, 900, 120, 22, 192, sky_top="#C8907A", sky_bot="#5A4A5A"))
    g.append(VB.footprints([(1500, 1060), (1400, 960), (1320, 860), (1260, 760)], "boot", 0.8, 193))
    for x in (60, 300, 1840): g.append(VB.grass_tuft(x, 1000 + (x % 50), 60, x, col="#6A6A48", dark="#3A3A28"))
    draw(c, svg_sprite("".join(g)), 0, 0, 1.0)
    # çit + kapı
    draw(c, svg_sprite(TEXD + palisade(560, 1900, 720, 150, 194, gate=(1080, 1300)) + gate_posts(1190, 730, 230, 220)), 0, 0, 1.0)
    torch(c, 1050, 520, t, 1.0); torch(c, 1330, 520, t, 1.0)
    k19a_crowd(c)
    # fısıltı işaretleri
    for k, (x, y) in enumerate([(1010, 520), (1200, 528), (1380, 520)]):
        draw(c, svg_sprite(f'<path d="M{x},{y} q14,-14 28,0 M{x+6},{y-12} q10,-10 20,0" stroke="#F4E6D0" stroke-width="3" fill="none" opacity="0.55"/>'), 0, 0, 1.0)
    # Ragnar: ön plan solda, kapüşonlu, kapıya yürüyor
    RH = dict(RGO, _head_extra=HOOD, cloak="#2E2A26", fur_collar="#5A5248")
    ragnar_bust(c, RH, "weary", 470, 430, 1.7, look=0.5, rimc="#FFB890", shx=(260, 520), shc="#140E18", phase=0.3)
    # ön plan çerçevesi: odak dışı kurutma iskelesi + balık
    fg = [TEXD, '<rect x="1780" y="0" width="70" height="1080" fill="#2A1E14" filter="url(#t_ahsap)"/><path d="M1600,120 L1920,140" stroke="#2A1E14" stroke-width="26"/>']
    for k in range(5): fg.append(f'<path d="M{1630+k*50},{130+k*3} v120 q-10,20 0,40" stroke="#3A3A3A" stroke-width="18" fill="none"/><path d="M{1622+k*50},{250+k*3} q8,30 0,60 q-10,8 -14,0 Z" fill="#6A6458"/>')
    draw(c, blurred(svg_sprite("".join(fg)), 7), 0, 0, 1.0)
    breath(c, 640, 560, t, seed=19) if False else None
    card_at(c, "KATTEGAT", 1560, 150, "yıllar sonra", 0.9)
    finish(c, cold=False, warm=0.05); return s

# ================================================================ k19b · salonda dört oğul
def hall_bg(c, blur=4, dark=0.35, fire=1.0):
    draw(c, blurred(place(P7.greathall(fire)), blur), 0, 0, 1.0); fill(c, "#0A0604", dark)

def k19b():
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    hall_bg(c, 5, 0.3)
    glow(c, 960, 900, 700, "#FF8A3A", 0.25)
    # orta plan: ocak başı masa, boynuzlar, kalkanlar
    m = [TEXD, '<path d="M0,1080 L0,930 Q960,900 1920,930 L1920,1080 Z" fill="#3A2818" filter="url(#t_ahsap)"/><path d="M0,930 Q960,900 1920,930" stroke="#1A1410" stroke-width="10" fill="none"/><path d="M0,924 Q960,894 1920,924" stroke="#C8884A" stroke-width="3" fill="none" opacity="0.6"/>']
    draw(c, svg_sprite("".join(m)), 0, 0, 1.0)
    # Ubbe, Hvitserk, Sigurd (ayakta), Ivar (sedirde, sağ)
    for sp, e, x, hy, hs, lk, ph in [(UBBE, "neutral", 330, 400, 1.15, 0.3, 0.1), (HVIT, "smug", 760, 430, 1.1, 0.2, 0.7), (SIG, "cold", 1170, 420, 1.12, 0.1, 1.3)]:
        b = fig_bust(sp, ex(e, IF.blink_at(ph)), lk, hs)
        with live(c, x, 1080, phase=ph, breathe=0.005):
            rim(c, b, x, hy, 1.0, "#FFB070", dx=-5, dy=-2, a=0.55); draw(c, b, x, hy, 1.0); shade_side(c, b, x, hy, 0.4, x + 40, x + 260, "#120A06")
    draw(c, svg_sprite(TEXD + bench(1600, 1000, 520, 170)), 0, 0, 1.0)
    ivar_seat(c, 1600, 470, 1.05, "keen", look=0.6)
    lap = (f'{TEXD}<path d="M1380,1080 L1400,880 Q1600,830 1800,880 L1820,1080 Z" fill="#4A4040" filter="url(#t_kurk)" stroke="#1A1410" stroke-width="6"/>'
           + "".join(f'<path d="M{1400+k*30},{880-abs(k-7)*3} q-4,30 4,60" stroke="#2A2424" stroke-width="3" fill="none" opacity="0.6"/>' for k in range(14)))
    draw(c, svg_sprite(lap + crutch_line(1840, 1100, 1790, 640, 1.2)), 0, 0, 1.0)
    # ön plan masası: boynuz kadeh, ekmek, bıçak (bulanık)
    fgx = [TEXD, '<ellipse cx="200" cy="1060" rx="260" ry="60" fill="#2A1C10"/><path d="M120,1040 q40,-90 120,-110 l10,20 q-70,30 -100,100 Z" fill="#C8B488" stroke="#1A1410" stroke-width="5"/>',
           '<ellipse cx="1180" cy="1070" rx="140" ry="30" fill="#5A4026" stroke="#1A1410" stroke-width="5"/><ellipse cx="1180" cy="1050" rx="90" ry="26" fill="#B08A52" stroke="#1A1410" stroke-width="5"/>']
    draw(c, blurred(svg_sprite("".join(fgx)), 6), 0, 0, 1.0)
    embers(c, 1902, 30, (500, 500, 1400, 950))
    for nm, sub, x, y in [("UBBE", "en büyük", 330, 150), ("HVITSERK", "", 760, 175), ("SIGURD", "", 1170, 165), ("IVAR", "kemiksiz", 1600, 215)]:
        card_at(c, nm, x, y, sub, 0.82)
    finish(c, cold=False, warm=0.06); return s

# ================================================================ k19c · taç uzatılıyor, oğullar başını çeviriyor
def k19c():
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    hall_bg(c, 7, 0.5, 0.6)
    beam(c, 760, 0, 160, 900, 1080, 520, "#C8D8E8", 0.12, 14) if hasattr(VA, "beam") is False else VA.beam(c, 760, 0, 160, 900, 1080, 520, "#C8D8E8", 0.14, 14)
    # arka: Ivar gölgede oturuyor, izliyor (odak dışı)
    b = fig_bust(IVAR, ex("cold", IF.blink_at(0.9)), 0.6, 0.62, flip=True)
    draw(c, blurred(b, 3), 1500, 400, 1.0, a=0.75); fill(c, "#0A0806", 0.15)
    # oğullar: Ubbe sırtı dönük, Hvitserk yüzünü çeviriyor, Sigurd profil uzağa
    ub = full(UBBE, "neutral", 0.9, facing=1, view="back"); soft_shadow(c, 1300, 1070, 150, 18, 0.4); rim(c, ub, 1300, 1080, 0.95, "#C8D8E8", dx=-5, dy=-2, a=0.6); draw(c, ub, 1300, 1080, 0.95)
    hv = fig_bust(HVIT, ex("torn", IF.blink_at(0.4)), 0.9, 1.0)
    with live(c, 1560, 1080, phase=0.4): rim(c, hv, 1560, 520, 1.0, "#C8D8E8", dx=-6, dy=-2, a=0.6); draw(c, hv, 1560, 520, 1.0); shade_side(c, hv, 1560, 520, 0.5, 1360, 1700, "#0E1218")
    sg = full(SIG, "cold", 0.9, facing=1, view="side", look=0.8); soft_shadow(c, 1040, 1070, 110, 14, 0.4); rim(c, sg, 1040, 1080, 0.8, "#C8D8E8", dx=-5, dy=-2, a=0.6); draw(c, sg, 1040, 1080, 0.8); shade_side(c, sg, 1040, 1080, 0.45, 1040, 1260, "#0E1218")
    # Ragnar: sol önde, kolunu uzatmış, elinde taç
    RC = arm_pts(RGO, [(52, SHY + 16), (170, SHY + 40), (300, SHY + 10)], "grip", CROWN)
    ragnar_bust(c, RC, "hollow2", 360, 420, 1.55, look=0.5, rimc="#E8C890", shx=(120, 420), shc="#0A0806", phase=0.2)
    bloom_spot(c, 360 + 300 * 1.55 * 80 / 82 * 1.0 - 120, 420 + (SHY + 10 + 560) * 1.55 * 80 / 82 * 0 + 20, 60, "#FFE0A0", 0.25)
    r = R_(1931)
    for k in range(60): c.drawCircle(r.uniform(600, 1100), r.uniform(80, 900), r.uniform(1, 2.6), skia.Paint(AntiAlias=True, Color4f=col("#E8E4D8", r.uniform(0.2, 0.6))))
    finish(c, cold=True, warm=0.0); return s

# ================================================================ k19d · Ivar kucak açıyor; ışık ikisine
def k19d():
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    hall_bg(c, 9, 0.72, 0.5)
    glow(c, 1000, 520, 640, "#FFB060", 0.32); bloom_spot(c, 1000, 400, 200, "#FFE0B0", 0.18)
    VA.beam(c, 980, 0, 120, 1000, 1080, 700, "#FFD8A0", 0.18, 16)
    draw(c, svg_sprite(TEXD + bench(1270, 1080, 560, 300)), 0, 0, 1.0)
    ivar_seat(c, 1270, 470, 1.25, "warm", look=-0.2, arms=True, rim_c="#FFC080")
    draw(c, svg_sprite(TEXD + '<path d="M1040,1080 L1060,940 Q1270,900 1480,940 L1500,1080 Z" fill="#4A4040" filter="url(#t_kurk)" stroke="#1A1410" stroke-width="6"/>' + crutch_line(1560, 1100, 1530, 660, 1.3)), 0, 0, 1.0)
    ragnar_bust(c, RGO, "grief_closed" if "grief_closed" in EXP else "tender", 720, 470, 1.35, look=0.6, rimc="#FFC080", shx=(420, 640), shc="#120A06", rot=10, phase=0.4)
    vign = '<defs><radialGradient id="vg" cx="0.52" cy="0.45" r="0.62"><stop offset="0.45" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#050302" stop-opacity="0.85"/></radialGradient></defs><rect width="1920" height="1080" fill="url(#vg)"/>'
    draw(c, svg_sprite(vign), 0, 0, 1.0)
    embers(c, 1904, 26, (600, 200, 1500, 900), "#FFD090")
    finish(c, cold=False, warm=0.08); return s

# ================================================================ k20a · sisli orman, dev yaşlı ağaç
def giant_tree(cx, yb, seed=7):
    r = R_(seed); o = []; ol = []; fl = []
    # dallar (arkadan): kalın → ince, çatallanan
    def branch(x, y, ang, L, w, d):
        if d == 0 or w < 3: return
        x2 = x + math.cos(math.radians(ang)) * L; y2 = y + math.sin(math.radians(ang)) * L
        mx = (x + x2) / 2 + r.uniform(-L, L) * 0.15; my = (y + y2) / 2 + r.uniform(-L, L) * 0.15
        ol.append(f'<path d="M{x:.0f},{y:.0f} Q{mx:.0f},{my:.0f} {x2:.0f},{y2:.0f}" stroke="#1A1410" stroke-width="{w+6:.0f}" fill="none" stroke-linecap="round"/>')
        fl.append(f'<path d="M{x:.0f},{y:.0f} Q{mx:.0f},{my:.0f} {x2:.0f},{y2:.0f}" stroke="#4A4238" stroke-width="{w:.0f}" fill="none" stroke-linecap="round"/>')
        fl.append(f'<path d="M{x:.0f},{y-w*0.25:.0f} Q{mx:.0f},{my-w*0.25:.0f} {x2:.0f},{y2-w*0.2:.0f}" stroke="#8A8270" stroke-width="{max(1.5,w*0.18):.0f}" fill="none" stroke-linecap="round" opacity="0.6"/>')
        if w > 14 and r.random() < 0.6: fl.append(f'<ellipse cx="{mx:.0f}" cy="{my-w*0.4:.0f}" rx="{w*0.8:.0f}" ry="{w*0.3:.0f}" fill="#5E6A3A" opacity="0.8"/>')   # yosun
        for k in range(2 if d > 1 else 3):
            branch(x2, y2, ang + r.uniform(-38, 38), L * r.uniform(0.6, 0.8), w * 0.62, d - 1)
    for ang, L, w in [(-160, 470, 96), (-132, 420, 104), (-100, 320, 96), (-64, 400, 100), (-30, 470, 90), (-8, 420, 70), (-178, 420, 70)]:
        branch(cx + (ang + 90) * 0.6, yb - 600, ang, L, w, 5)
    # gövde + kökler
    trunk = (f'M{cx-420},{yb} Q{cx-230},{yb-30} {cx-200},{yb-180} Q{cx-150},{yb-420} {cx-170},{yb-640} Q{cx-60},{yb-720} {cx+150},{yb-650} Q{cx+130},{yb-420} {cx+200},{yb-180} Q{cx+250},{yb-30} {cx+450},{yb} Z')
    o.append(f'<defs><clipPath id="tr{seed}"><path d="{trunk}"/></clipPath>' + gradient(f"tg{seed}", [(0, "#6E665A"), (0.4, "#4E463C"), (1, "#24201C")], x2=1, y2=0) + '</defs>')
    o.append(f'<path d="{trunk}" fill="url(#tg{seed})"/><g clip-path="url(#tr{seed})"><rect x="{cx-400}" y="{yb-760}" width="800" height="760" filter="url(#t_ahsap)" fill="#3A342C" opacity="0.5"/>')
    for k in range(46):   # kabuk yarıkları
        x = cx + r.uniform(-260, 280); y0 = yb - r.uniform(0, 700); L = r.uniform(80, 260)
        o.append(f'<path d="M{x:.0f},{y0:.0f} q{r.uniform(-20,20):.0f},{-L/2:.0f} {r.uniform(-14,14):.0f},{-L:.0f}" stroke="#1A1612" stroke-width="{r.uniform(3,8):.1f}" fill="none" opacity="0.7"/>'
                 f'<path d="M{x-6:.0f},{y0:.0f} q{r.uniform(-20,20):.0f},{-L/2:.0f} {r.uniform(-14,14):.0f},{-L:.0f}" stroke="#9A9282" stroke-width="2" fill="none" opacity="0.3"/>')
    for k in range(9): o.append(f'<ellipse cx="{cx + r.uniform(-200,200):.0f}" cy="{yb - r.uniform(100, 640):.0f}" rx="{r.uniform(30,90):.0f}" ry="{r.uniform(14,40):.0f}" fill="#5E6A3A" opacity="0.55"/>')
    o.append(f'<path d="M{cx-40},{yb-420} q30,-50 70,-10 q-20,60 -70,10 Z" fill="#14100C" stroke="#2A2218" stroke-width="5"/>')   # kovuk
    o.append('</g>' + f'<path d="{trunk}" fill="none" stroke="#1A1410" stroke-width="8"/>')
    for sx, L in ((-1, 300), (-1, 200), (1, 280), (1, 420), (-1, 440)):   # yüzeysel kökler
        x0 = cx + sx * r.uniform(80, 200); x1 = x0 + sx * L
        o.append(f'<path d="M{x0:.0f},{yb-40} Q{(x0+x1)/2:.0f},{yb-70:.0f} {x1:.0f},{yb+20}" stroke="#1A1410" stroke-width="44" fill="none" stroke-linecap="round"/><path d="M{x0:.0f},{yb-40} Q{(x0+x1)/2:.0f},{yb-70:.0f} {x1:.0f},{yb+20}" stroke="#4A4238" stroke-width="34" fill="none" stroke-linecap="round"/>'
                 f'<path d="M{x0:.0f},{yb-52} Q{(x0+x1)/2:.0f},{yb-82:.0f} {x1:.0f},{yb+8}" stroke="#8A8270" stroke-width="5" fill="none" opacity="0.5"/>')
    return "".join(o + ol + fl)

def k20a():
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    draw(c, svg_sprite(sky_dusk("s20", [(0, "#6E7A80"), (0.6, "#A8B0AE"), (1, "#C8CCC4")], 1080)), 0, 0, 1.0)
    glow(c, 1500, 260, 520, "#F0F0E0", 0.35)
    for k, (yb, hm, al, bl) in enumerate([(760, (260, 420), 0.35, 5), (840, (320, 520), 0.55, 3)]):
        f_ = VB.forest(-60, 1980, lambda x, yb=yb: yb + 10 * math.sin(x / 140), hm[0], hm[1], 34, 2000 + k, col="#3A4440", lit="#5A6460", dark="#2A3230")
        draw(c, blurred(svg_sprite(f_), bl), 0, 0, 1.0, a=al)
        draw(c, blurred(svg_sprite(cloud_band(2010 + k, 14, -100, 2000, yb - 220, yb - 40, "#C8CCC6", "#E8EAE4", 0.55, rx=(240, 520), ry=(30, 70))), 14), 0, 0, 1.0)
    # zemin: yosun, kök, yaprak, taşlar
    g = [TEXD, '<path d="M0,900 Q500,860 960,880 Q1400,860 1920,900 L1920,1080 L0,1080 Z" fill="#3E4430" filter="url(#t_tas)"/>']
    r = R_(2020)
    for k in range(320):
        x = r.uniform(0, 1920); y = r.uniform(880, 1080); g.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r.uniform(3,9):.0f}" ry="{r.uniform(1.5,4):.0f}" fill="{r.choice(["#7A5A34", "#8A6A3A", "#5A6A3A", "#2E3424"])}" opacity="0.8"/>')
    g.append(boulder(330, 960, 60, 2021, "#6A6A60") + boulder(1650, 990, 80, 2022, "#5E5E56"))
    for x in (120, 520, 1400, 1800): g.append(VB.grass_tuft(x, 1000 + (x % 40), 70, x, col="#6A7048", dark="#3A3E28"))
    draw(c, svg_sprite("".join(g)), 0, 0, 1.0)
    draw(c, svg_sprite(TEXD + giant_tree(960, 910, 11)), 0, 0, 1.0)
    VA.beam(c, 1420, 0, 140, 1120, 1000, 380, "#F4F4E8", 0.16, 18)
    # kuzgunlar dallarda
    rv = "".join(VB.raven(x, y, sc, fl, "perch", k) for k, (x, y, sc, fl) in enumerate([(430, 300, 0.32, 1), (640, 170, 0.28, -1), (1340, 230, 0.3, -1), (1560, 330, 0.26, 1), (1180, 120, 0.24, 1)]))
    draw(c, svg_sprite(rv), 0, 0, 1.0)
    # Ragnar: kökün dibinde, küçük, sırtı bükük (diz çökmüş, öne eğik); sisin önünde
    RK = dict(RGO, _kneel=120, cloak="#2E2A26")
    fs = full(RK, "hollow", 0.9, facing=1, look=-0.2)
    glow(c, 1120, 860, 160, "#F4F4E8", 0.25)
    soft_shadow(c, 1120, 958, 80, 12, 0.55)
    c.save(); c.translate(1120, 962); c.rotate(14); rim(c, fs, 0, 0, 0.3, "#F4F8F0", dx=-4, dy=-2, a=0.8); draw(c, fs, 0, 0, 0.3); c.restore()
    # ön plan: odak dışı eğrelti/dal
    fg = [f'<path d="M-40,1080 Q60,860 220,800" stroke="#1A1E14" stroke-width="30" fill="none"/>'] + [f'<path d="M{60+k*22},{1000-k*26} q{-50},{-10} {-80},{20}" stroke="#2A3220" stroke-width="12" fill="none"/>' for k in range(7)]
    draw(c, blurred(svg_sprite("".join(fg)), 8), 0, 0, 1.0)
    finish(c, cold=True, warm=0.0); return s


# ================================================================ k20a v2 · Yggdrasil benzeri dev ağaç (düzeltme turu)
def _taper(pts, w0, w1):
    n = len(pts); L = []; Rr = []
    for i, (x, y) in enumerate(pts):
        a = pts[min(i + 1, n - 1)]; b = pts[max(i - 1, 0)]; dx, dy = a[0] - b[0], a[1] - b[1]; d = math.hypot(dx, dy) or 1
        nx, ny = -dy / d, dx / d; w = (w0 + (w1 - w0) * i / (n - 1)) / 2
        L.append((x + nx * w, y + ny * w)); Rr.append((x - nx * w, y - ny * w))
    P_ = L + Rr[::-1]
    return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in P_) + " Z"

def _qpts(x0, y0, mx, my, x1, y1, n=18):
    return [((1-t)**2*x0 + 2*(1-t)*t*mx + t*t*x1, (1-t)**2*y0 + 2*(1-t)*t*my + t*t*y1) for t in [i/(n-1) for i in range(n)]]

def _blob(x, y, rx, ry, seed, n=16):
    r = R_(seed); pts = [(x + rx*math.cos(a)*r.uniform(0.55, 1.15), y + ry*math.sin(a)*r.uniform(0.55, 1.15)) for a in [i*2*math.pi/n for i in range(n)]]
    return "M" + " L".join(f"{px:.0f},{py:.0f}" for px, py in pts) + " Z"

def lichen(x, y, rx, ry, seed):
    r = R_(seed); o = [f'<path d="{_blob(x, y, rx, ry, seed)}" fill="#6E7E58" filter="url(#t_kurk)" opacity="0.55"/>',
                       f'<path d="{_blob(x + rx*0.1, y - ry*0.1, rx*0.6, ry*0.6, seed + 1)}" fill="#9AA87E" filter="url(#t_tas)" opacity="0.45"/>']
    for _ in range(int(rx * ry / 140) + 4):
        px = x + r.gauss(0, rx * 0.6); py = y + r.gauss(0, ry * 0.6)
        o.append(f'<circle cx="{px:.0f}" cy="{py:.0f}" r="{r.uniform(1.2, 3.8):.1f}" fill="{r.choice(["#8A9A6A", "#5A6A40", "#6E7E56", "#9AA47E"])}" opacity="0.6"/>')
    return "".join(o)

def ygg(cx, yb, seed=21):
    r = R_(seed); OL, FL, DET, perch = [], [], [], []
    top = 210
    # --- dallar (tapered, çatallanan) ---
    def limb_(x, y, ang, L, w, d):
        if d == 0 or w < 4: 
            for k in range(3):   # uçlarda sarkan kuru ince dallar
                DET.append(f'<path d="M{x:.0f},{y:.0f} q{r.uniform(-8,8):.0f},{r.uniform(20,40):.0f} {r.uniform(-14,14):.0f},{r.uniform(40,110):.0f}" stroke="#2E2A24" stroke-width="{r.uniform(1.5,3):.1f}" fill="none"/>')
            return
        x2 = x + math.cos(math.radians(ang)) * L; y2 = y + math.sin(math.radians(ang)) * L
        mx = (x + x2) / 2 + r.uniform(-0.2, 0.2) * L; my = (y + y2) / 2 + r.uniform(-0.25, 0.1) * L
        pts = _qpts(x, y, mx, my, x2, y2); w2 = w * r.uniform(0.55, 0.68); d_ = _taper(pts, w, w2)
        OL.append(f'<path d="{d_}" fill="#1A1410" stroke="#1A1410" stroke-width="7" stroke-linejoin="round"/>')
        FL.append(f'<path d="{d_}" fill="{r.choice(["#4A4238", "#463E34", "#524A3E"])}"/>')
        FL.append('<path d="M' + " L".join(f"{px:.0f},{py - (w + (w2 - w) * i / 17) * 0.36:.0f}" for i, (px, py) in enumerate(pts)) + f'" stroke="#8A8474" stroke-width="{max(1.5, w*0.07):.1f}" fill="none" opacity="0.55" stroke-linecap="round"/>')
        FL.append('<path d="M' + " L".join(f"{px:.0f},{py + (w + (w2 - w) * i / 17) * 0.3:.0f}" for i, (px, py) in enumerate(pts)) + f'" stroke="#16120E" stroke-width="{max(2, w*0.22):.1f}" fill="none" opacity="0.45" stroke-linecap="round"/>')
        for k in range(2 if w > 30 else 1):   # kabuk yarığı (dal yönünde)
            off = r.uniform(-0.25, 0.25) * w
            FL.append('<path d="M' + " L".join(f"{px:.0f},{py+off+r.uniform(-1.5,1.5):.0f}" for px, py in pts[1:-2]) + f'" stroke="#221C16" stroke-width="{max(1.5, w*0.06):.1f}" fill="none" opacity="0.7"/>')
        if 22 < w < 70 and abs(math.sin(math.radians(ang))) < 0.55: perch.append((pts[len(pts)//2][0], pts[len(pts)//2][1] - w * 0.45, ang))
        if w > 26 and r.random() < 0.5: DET.append(lichen(mx, my - w * 0.3, w * 0.9, w * 0.25, r.randint(0, 9999)))
        if w < 40:
            for k in range(2):   # sarkan ince dal + yaşlı adam sakalı likeni
                px, py = pts[r.randint(3, len(pts) - 3)]
                DET.append(f'<path d="M{px:.0f},{py:.0f} q{r.uniform(-10,10):.0f},{r.uniform(30,60):.0f} {r.uniform(-16,16):.0f},{r.uniform(60,150):.0f}" stroke="{r.choice(["#2E2A24", "#A8B098"])}" stroke-width="{r.uniform(1.5,3.2):.1f}" fill="none" opacity="0.8"/>')
        nb = 2 if d > 1 else 3
        for k in range(nb): limb_(x2, y2, ang + r.uniform(-34, 34) + (k - (nb - 1) / 2) * 18, L * r.uniform(0.62, 0.8), w2, d - 1)
    for ang, L, w, ox in [(-172, 430, 150, -150), (-150, 400, 160, -110), (-118, 330, 140, -50), (-88, 260, 130, 10), (-60, 340, 150, 70), (-28, 420, 160, 120), (-6, 430, 140, 160), (-196, 380, 110, -170)]:
        limb_(cx + ox, top + 60, ang, L, w, 5)
    # kırık dal kütüğü (yukarıda, solda): kısa, kalın, uç kıymıklı
    sx0, sy0 = cx - 150, top + 230; stub = _qpts(sx0, sy0, sx0 - 90, sy0 - 40, sx0 - 190, sy0 - 50, 10)
    OL.append(f'<path d="{_taper(stub, 110, 80)}" fill="#1A1410" stroke="#1A1410" stroke-width="7"/>'); FL.append(f'<path d="{_taper(stub, 110, 80)}" fill="#4E463A"/>')
    ex_, ey_ = stub[-1]
    FL.append(f'<path d="M{ex_+6},{ey_-42} L{ex_-18},{ey_-30} L{ex_-4},{ey_-16} L{ex_-26},{ey_-2} L{ex_-8},{ey_+10} L{ex_-22},{ey_+26} L{ex_+6},{ey_+40} Z" fill="#C8B48C" stroke="#1A1410" stroke-width="4" stroke-linejoin="round"/>'
              f'<path d="M{ex_-4},{ey_-28} l-10,8 M{ex_-6},{ey_+4} l-12,4 M{ex_-6},{ey_+22} l-10,6" stroke="#7A6646" stroke-width="3"/>')
    # --- gövde: burgulu lif demetleri ---
    strands = []
    for k in range(7):
        bx = cx + (-330 + k * 110) * 1.0 + r.uniform(-20, 20); tx = cx + (-300 + k * 100); ph = k * 0.9 + r.uniform(0, 0.5)
        pts = []
        for i in range(26):
            t = i / 25; y = yb - t * (yb - top - 70)
            x = bx + (tx - bx) * t ** 0.55 + 46 * math.sin(t * math.pi * 1.6 + ph) * (1 - t * 0.3) + (-60 * t * (1 - t))
            pts.append((x, y))
        strands.append((pts, r.uniform(190, 240), r.uniform(18, 30)))
    tr_ol = "".join(f'<path d="{_taper(p, w0, w1)}" fill="#1A1410" stroke="#1A1410" stroke-width="9" stroke-linejoin="round"/>' for p, w0, w1 in strands)
    cid = f"yg{seed}"
    clip = "".join(f'<path d="{_taper(p, w0, w1)}"/>' for p, w0, w1 in strands)
    tr = [f'<defs><clipPath id="{cid}">{clip}</clipPath>' + gradient(f"ygg{seed}", [(0, "#2A2620"), (0.45, "#4A4238"), (0.8, "#6A6458"), (1, "#8A8478")], x2=1, y2=0) + '</defs>']
    for k, (p, w0, w1) in enumerate(strands):
        tr.append(f'<path d="{_taper(p, w0, w1)}" fill="{["#3E372E", "#4A4238", "#433C32", "#50473C"][k % 4]}" stroke="#1E1A14" stroke-width="5"/>')
    tr.append(f'<g clip-path="url(#{cid})"><rect x="{cx-700}" y="{top-60}" width="1400" height="{yb-top+80}" fill="url(#ygg{seed})" opacity="0.55"/>'
              f'<rect x="{cx-700}" y="{top-60}" width="1400" height="{yb-top+80}" filter="url(#t_ahsap)" fill="#3A342C" opacity="0.45"/>')
    for p, w0, w1 in strands:   # derin kabuk yarıkları lif yönünde
        for j in range(3):
            f_ = (j - 1) / 1.8; jit = r.uniform(-8, 8)
            line = []
            for i, (x, y) in enumerate(p):
                w = (w0 + (w1 - w0) * i / 25) / 2; line.append((x + f_ * w + jit + r.uniform(-3, 3), y))
            a0 = r.randint(0, 8); a1 = r.randint(14, 25)
            d_ = "M" + " L".join(f"{x:.0f},{y:.0f}" for x, y in line[a0:a1])
            tr.append(f'<path d="{d_}" stroke="#14100C" stroke-width="{r.uniform(3, 6):.1f}" fill="none" stroke-linejoin="round" opacity="0.85"/><path d="{d_}" stroke="#8A8272" stroke-width="2" fill="none" opacity="0.35" transform="translate(5,0)"/>')
    for (kx, ky, kr) in [(cx + 230, yb - 300, 40), (cx - 240, yb - 200, 30)]:   # budak / yumru
        tr.append(f'<path d="{_blob(kx, ky, kr*1.4, kr, kx)}" fill="#3A342A" stroke="#14100C" stroke-width="4" stroke-linejoin="round"/>'
                  + f'<path d="{_blob(kx, ky + 3, kr*0.8, kr*0.5, ky)}" fill="none" stroke="#1E1A14" stroke-width="3" opacity="0.6"/>'
                  + f'<ellipse cx="{kx}" cy="{ky}" rx="{kr*0.35:.0f}" ry="{kr*0.25:.0f}" fill="#120E0A"/><path d="M{kx-kr},{ky-kr*0.7:.0f} q{kr},{-kr*0.5:.0f} {kr*2:.0f},0" stroke="#9A9282" stroke-width="3" fill="none" opacity="0.5"/>')
    tr.append(f'<path d="M{cx+60},{yb-150} q20,-70 56,-30 q8,60 -18,90 q-44,-10 -38,-60 Z" fill="#0E0A08" stroke="#2A2218" stroke-width="7"/>')   # kovuk
    for k in range(10): tr.append(lichen(cx + r.uniform(-120, 300), yb - r.uniform(120, 640), r.uniform(26, 60), r.uniform(18, 40), 900 + k))
    tr.append('</g>')
    # --- payanda kökler: incelen, çatallanan, taşı saran, toprağa gömülen ---
    rocks = boulder(cx - 520, yb + 30, 70, 31, "#6A6A60") + boulder(cx + 560, yb + 40, 90, 32, "#5E5E56") + boulder(cx - 260, yb + 70, 44, 33, "#727268")
    RO, RF, SOIL = [], [], []
    for (sx, ex2, ey2, w0, sp) in [(-300, -760, 40, 170, 1), (-220, -480, 110, 140, 1), (-120, -230, 130, 110, 0), (40, 120, 140, 110, 0), (200, 440, 120, 140, 1), (300, 820, 50, 170, 1), (260, 640, 10, 120, 0)]:
        x0 = cx + sx; y0 = yb - 160; x1 = cx + ex2; y1 = yb + ey2
        pts = _qpts(x0, y0, x0 + (x1 - x0) * 0.55, y0 - 10 + (y1 - y0) * 0.2, x1, y1, 22)
        RO.append(f'<path d="{_taper(pts, w0, 8)}" fill="#1A1410" stroke="#1A1410" stroke-width="8" stroke-linejoin="round"/>')
        RF.append(f'<path d="{_taper(pts, w0, 8)}" fill="#4A4238" filter="url(#t_ahsap)"/>'
                  + '<path d="M' + " L".join(f"{px:.0f},{py - (w0 + (8 - w0) * i / 21) * 0.4:.0f}" for i, (px, py) in enumerate(pts)) + '" stroke="#8A8474" stroke-width="4" fill="none" opacity="0.5"/>'
                  + '<path d="M' + " L".join(f"{px:.0f},{py + (w0 + (8 - w0) * i / 21) * 0.32:.0f}" for i, (px, py) in enumerate(pts)) + f'" stroke="#16120E" stroke-width="{w0*0.2:.0f}" fill="none" opacity="0.5" stroke-linecap="round"/>')
        for j in range(3):
            off = (j - 1) * w0 * 0.18
            RF.append('<path d="M' + " L".join(f"{px:.0f},{py+off*(1-i/22):.0f}" for i, (px, py) in enumerate(pts[1:-4])) + '" stroke="#1A1612" stroke-width="3" fill="none" opacity="0.5"/>')
        if sp:   # çatal: yan kök dalı
            mxp, myp = pts[11]; qx = mxp + (x1 - x0) * 0.35; qy = yb + 60
            p2 = _qpts(mxp, myp, (mxp + qx) / 2, myp + 10, qx, qy, 14)
            RO.append(f'<path d="{_taper(p2, w0*0.45, 6)}" fill="#1A1410" stroke="#1A1410" stroke-width="7"/>'); RF.append(f'<path d="{_taper(p2, w0*0.45, 6)}" fill="#433C32"/>')
            SOIL.append(f'<path d="{_blob(qx, qy + 6, 40, 14, int(qx))}" fill="#2E2A1E"/>')
        SOIL.append(f'<path d="{_blob(x1, y1 + 6, 50, 16, int(x1) + 7)}" fill="#2E2A1E"/>' + VB.grass_tuft(x1 + 10, y1 + 10, 46, int(x1), col="#6A7048", dark="#3A3E28"))
        if w0 > 130: RF.append(lichen(x0 + (x1 - x0) * 0.3, y0 + (y1 - y0) * 0.2 - w0 * 0.2, 40, 16, int(x0) + 5))
    trunk_base = f'<path d="M{cx-380},{yb+10} Q{cx},{yb-60} {cx+400},{yb+10} Z" fill="#2E2A22"/>'
    perch.sort(key=lambda q: q[0])
    return rocks + "".join(OL) + "".join(FL) + "".join(DET), tr_ol + "".join(tr) + trunk_base + "".join(RO) + "".join(RF) + "".join(SOIL), perch

def k20a():
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    draw(c, svg_sprite(sky_dusk("s20", [(0, "#5E6A72"), (0.6, "#A0A8A8"), (1, "#C4C8C0")], 1080)), 0, 0, 1.0)
    glow(c, 1560, 200, 560, "#F0F2EA", 0.35)
    for k, (yb, hm, al, bl) in enumerate([(700, (240, 380), 0.3, 6), (800, (300, 480), 0.5, 4)]):
        f_ = VB.forest(-60, 1980, lambda x, yb=yb: yb + 10 * math.sin(x / 140), hm[0], hm[1], 34, 2000 + k, col="#3A4440", lit="#5A6460", dark="#2A3230")
        draw(c, blurred(svg_sprite(f_), bl), 0, 0, 1.0, a=al)
        draw(c, blurred(svg_sprite(cloud_band(2010 + k, 14, -100, 2000, yb - 200, yb - 40, "#C8CCC6", "#E8EAE4", 0.55, rx=(240, 520), ry=(30, 70))), 14), 0, 0, 1.0)
    g = [TEXD, '<path d="M0,900 Q500,880 960,890 Q1400,876 1920,900 L1920,1080 L0,1080 Z" fill="#3E4430" filter="url(#t_tas)"/>']
    r = R_(2020)
    for k in range(340):
        x = r.uniform(0, 1920); y = r.uniform(890, 1080); g.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r.uniform(3,9):.0f}" ry="{r.uniform(1.5,4):.0f}" fill="{r.choice(["#7A5A34", "#8A6A3A", "#5A6A3A", "#2E3424"])}" opacity="0.8"/>')
    draw(c, svg_sprite("".join(g)), 0, 0, 1.0)
    crown, trunk, perch = ygg(900, 930, 21)
    draw(c, svg_sprite(TEXD + trunk), 0, 0, 1.0)
    draw(c, svg_sprite(TEXD + crown), 0, 0, 1.0)
    # taç sise karışıyor: üst sis + uzak dal uçları soluk
    draw(c, blurred(svg_sprite(cloud_band(2040, 16, -100, 2000, -60, 110, "#B8BEBC", "#E0E2DE", 0.4, rx=(260, 560), ry=(40, 90))), 16), 0, 0, 1.0)
    for x0, x1 in ((-100, 260), (1660, 2020)):
        draw(c, blurred(svg_sprite(cloud_band(2041 + x0, 6, x0, x1, 160, 600, "#B8BEBC", "#E0E2DE", 0.2, rx=(160, 300), ry=(60, 140))), 18), 0, 0, 1.0)
    # kuzgunlar dallarda (dal üst kenarına oturur)
    pv = [q for q in perch if 230 < q[1] < 700 and 40 < q[0] < 1880 and not (700 < q[0] < 1120)]
    pk = [pv[i] for i in sorted(set(int(j * (len(pv) - 1) / 4) for j in range(5)))] if pv else []
    rv = "".join(VB.raven(x, y - 12, 0.34, (1 if k % 2 else -1), "perch", k) for k, (x, y, a) in enumerate(pk))
    draw(c, svg_sprite(rv), 0, 0, 1.0)
    # soğuk ışık hüzmesi Ragnar'a
    VA.beam(c, 1500, 0, 160, 1190, 990, 300, "#EEF4F8", 0.2, 18)
    draw(c, blurred(svg_sprite(cloud_band(2030, 12, -100, 2000, 960, 1040, "#D8DCD6", "#ECEEEA", 0.22, rx=(260, 560), ry=(14, 30))), 12), 0, 0, 1.0)
    RK = dict(RGO, _kneel=120, cloak="#2E2A26")
    fs = full(RK, "hollow", 0.9, facing=1, look=-0.2)
    glow(c, 1190, 900, 170, "#EEF4F8", 0.3)
    soft_shadow(c, 1190, 990, 80, 12, 0.55)
    c.save(); c.translate(1190, 994); c.rotate(14); rim(c, fs, 0, 0, 0.27, "#F4F8FA", dx=4, dy=-3, a=0.9); draw(c, fs, 0, 0, 0.27); c.restore()
    fg = [f'<path d="M-40,1080 Q60,860 220,800" stroke="#1A1E14" stroke-width="30" fill="none"/>'] + [f'<path d="M{60+k*22},{1000-k*26} q{-50},{-10} {-80},{20}" stroke="#2A3220" stroke-width="12" fill="none"/>' for k in range(7)]
    draw(c, blurred(svg_sprite("".join(fg)), 8), 0, 0, 1.0)
    finish(c, cold=True, warm=0.0); return s


# ================================================================ k20a v3 · tek gövdeli yaşlı ağaç (kullanıcı: "tek gövdeden yukarı çıkıyor")
def _furrow(x, y0, y1, r, wmax=7, col="#15110D", sway=10):
    """Düzensiz kabuk yarığı: kırık kırık, kalınlığı değişen, yer yer kopan çizgi."""
    o = []; y = y0; xx = x
    while y > y1:
        seg = r.uniform(30, 90); y2 = max(y1, y - seg); x2 = xx + r.uniform(-sway, sway)
        if r.random() > 0.15:
            mx = (xx + x2) / 2 + r.uniform(-6, 6)
            o.append(f'<path d="M{xx:.0f},{y:.0f} Q{mx:.0f},{(y+y2)/2:.0f} {x2:.0f},{y2:.0f}" stroke="{col}" stroke-width="{r.uniform(2, wmax):.1f}" fill="none" stroke-linecap="round"/>')
            if r.random() < 0.5: o.append(f'<path d="M{xx+4:.0f},{y:.0f} Q{mx+4:.0f},{(y+y2)/2:.0f} {x2+4:.0f},{y2:.0f}" stroke="#8C8476" stroke-width="1.6" fill="none" opacity="0.35"/>')
        y = y2 - r.uniform(0, 14); xx = x2
    return "".join(o)

def oak(cx, yb, seed=31):
    r = R_(seed)
    # gövde ekseni: hafif burgu; genişlik tabanda kök yayılmasıyla açılır
    def half(y):   # gövde yarı genişliği
        t = (yb - y) / (yb - 0)
        return 150 + 260 * math.exp(-t * 9) + 30 * math.sin(t * 7 + 1) * (1 - t)
    def axis(y):
        t = (yb - y) / yb; return cx + 40 * math.sin(t * 3.2 - 0.6)
    ys = [yb + 10 - i * (yb + 30) / 40 for i in range(41)]
    left = [(axis(y) - half(y) - (8 * math.sin(y / 37) if y < yb - 60 else 0), y) for y in ys]
    right = [(axis(y) + half(y) * 1.05 + (6 * math.sin(y / 29) if y < yb - 60 else 0), y) for y in ys]
    trunk_d = "M" + " L".join(f"{x:.0f},{y:.0f}" for x, y in left) + " L" + " L".join(f"{x:.0f},{y:.0f}" for x, y in right[::-1]) + " Z"
    # ---- kökler (gövdeden önce; tabanları gövde altında kalır)
    ROOT = []
    for (sx, ex2, ey2, w0, curl) in [(-260, -700, 70, 150, -40), (-180, -420, 120, 110, 20), (-60, -170, 140, 80, 0), (120, 260, 140, 90, 0), (240, 520, 110, 120, -20), (300, 820, 60, 150, 30)]:
        x0 = cx + sx * 0.8; y0 = yb - 30; x1 = cx + ex2; y1 = yb + ey2
        pts = _qpts(x0, y0, x0 + (x1 - x0) * 0.5, yb - 40 + curl * 0.4, x1, y1, 22); d_ = _taper(pts, w0, 6)
        ROOT.append(f'<path d="{d_}" fill="#1A1410" stroke="#1A1410" stroke-width="8" stroke-linejoin="round"/><path d="{d_}" fill="#4A4238"/><path d="{d_}" fill="#3A342C" filter="url(#t_ahsap)" opacity="0.5"/>')
        ROOT.append('<path d="M' + " L".join(f"{px:.0f},{py - (w0 + (6 - w0) * i / 21) * 0.38:.0f}" for i, (px, py) in enumerate(pts[:-3])) + '" stroke="#8A8474" stroke-width="3" fill="none" opacity="0.4"/>')
        for k in range(3):   # kısa düzensiz yarıklar
            i0 = r.randint(1, 10); seg = pts[i0:i0 + r.randint(4, 8)]; off = r.uniform(-0.2, 0.2) * w0
            ROOT.append('<path d="M' + " L".join(f"{px + r.uniform(-2,2):.0f},{py + off * (1 - (i0 + j) / 22):.0f}" for j, (px, py) in enumerate(seg)) + f'" stroke="#15110D" stroke-width="{r.uniform(2,4):.1f}" fill="none" opacity="0.7"/>')
        ROOT.append(f'<path d="{_blob(x1, y1 + 8, 46, 14, int(x1) + 3)}" fill="#2E2A1E"/>' + VB.grass_tuft(x1 + 8, y1 + 12, 40, int(x1), col="#6A7048", dark="#3A3E28"))
        if w0 > 120: ROOT.append(lichen(x0 + (x1 - x0) * 0.35, yb - 70, 34, 12, int(x0) + 9))
    rocks = boulder(cx - 560, yb + 30, 70, 31, "#6A6A60") + boulder(cx + 600, yb + 40, 86, 32, "#5E5E56") + boulder(cx - 300, yb + 80, 40, 33, "#727268")
    # ---- dallar: gövdenin YÜKSEĞİNDEN, geniş yayılan; uzun yatay ana dal (sol)
    LO, LF, DET, perch = [], [], [], []
    def limb_(x, y, ang, L, w, d, bend=0.0):
        if d == 0 or w < 3.5:
            for k in range(2): DET.append(f'<path d="M{x:.0f},{y:.0f} q{r.uniform(-8,8):.0f},{r.uniform(-30,-10):.0f} {r.uniform(-20,20):.0f},{r.uniform(-60,-20):.0f}" stroke="#2E2A24" stroke-width="{r.uniform(1.4,2.6):.1f}" fill="none"/>')
            return
        x2 = x + math.cos(math.radians(ang)) * L; y2 = y + math.sin(math.radians(ang)) * L
        mx = (x + x2) / 2 + r.uniform(-0.12, 0.12) * L; my = (y + y2) / 2 + (bend + r.uniform(-0.12, 0.08)) * L
        pts = _qpts(x, y, mx, my, x2, y2); w2 = w * r.uniform(0.6, 0.72); d_ = _taper(pts, w, w2)
        LO.append(f'<path d="{d_}" fill="#1A1410" stroke="#1A1410" stroke-width="7" stroke-linejoin="round"/>')
        LF.append(f'<path d="{d_}" fill="#463E34"/>')
        LF.append('<path d="M' + " L".join(f"{px:.0f},{py - (w + (w2 - w) * i / 17) * 0.36:.0f}" for i, (px, py) in enumerate(pts[1:-1], 1)) + f'" stroke="#8A8474" stroke-width="{max(1.2, w*0.06):.1f}" fill="none" opacity="0.4" stroke-linecap="round"/>')
        if w > 18:
            for k in range(2):
                i0 = r.randint(1, 9); seg = pts[i0:i0 + r.randint(3, 7)]; off = r.uniform(-0.15, 0.2) * w
                LF.append('<path d="M' + " L".join(f"{px + r.uniform(-1.5,1.5):.0f},{py + off:.0f}" for px, py in seg) + f'" stroke="#15110D" stroke-width="{max(1.5, w*0.05):.1f}" fill="none" opacity="0.65"/>')
        if 12 < w < 52 and abs(math.sin(math.radians(ang))) < 0.45:
            perch.append((pts[len(pts) // 2][0], pts[len(pts) // 2][1] - (w + w2) / 4, w))
        if w > 30 and r.random() < 0.45: DET.append(lichen(mx, my - w * 0.32, w * 0.8, w * 0.22, r.randint(0, 9999)))
        if w < 30 and r.random() < 0.6:
            px, py = pts[r.randint(4, 14)]; DET.append(f'<path d="M{px:.0f},{py:.0f} q{r.uniform(-6,6):.0f},{r.uniform(20,40):.0f} {r.uniform(-12,12):.0f},{r.uniform(40,100):.0f}" stroke="#2E2A24" stroke-width="{r.uniform(1.3,2.4):.1f}" fill="none"/>')   # sarkan kuru ince dal
        nb = 2 if d > 2 else 3
        for k in range(nb): limb_(x2, y2, ang + (k - (nb - 1) / 2) * r.uniform(22, 34) + r.uniform(-10, 10), L * r.uniform(0.6, 0.76), w2, d - 1, bend * 0.6)
    TY = 360
    # (başlangıç y, yön, açı, uzunluk, kalınlık, bükülme)
    for (y0, side, ang, L, w, bend, dp) in [(TY + 30, -1, 181, 430, 84, -0.04, 6),   # dizideki uzun, neredeyse yatay sol dal
                                        (TY - 70, -1, 208, 300, 72, 0.0, 5), (TY - 170, -1, 236, 250, 64, 0.0, 5),
                                        (TY - 10, 1, -10, 380, 80, 0.03, 6), (TY - 120, 1, -36, 300, 70, 0.0, 5), (TY - 220, 1, -64, 240, 62, 0.0, 5), (TY - 250, -1, -112, 220, 60, 0.0, 4)]:
        x0 = axis(y0) + side * (half(y0) - 30)
        limb_(x0, y0, ang, L, w, dp, bend)
    # ---- gövde dolgusu + doku (tek gövde)
    cid = f"ok{seed}"
    T_ = [f'<defs><clipPath id="{cid}"><path d="{trunk_d}"/></clipPath>' + gradient(f"okg{seed}", [(0, "#24201A"), (0.35, "#3E372E"), (0.7, "#5A5246"), (0.9, "#7A7262"), (1, "#5A5246")], x2=1, y2=0) + '</defs>',
          f'<path d="{trunk_d}" fill="url(#okg{seed})" stroke="#1A1410" stroke-width="9" stroke-linejoin="round"/>', f'<g clip-path="url(#{cid})">',
          f'<rect x="{cx-500}" y="-40" width="1000" height="{yb+80}" fill="#3A342C" filter="url(#t_ahsap)" opacity="0.5"/>',
          f'<rect x="{cx-500}" y="-40" width="1000" height="{yb+80}" fill="#2A2620" filter="url(#t_tas)" opacity="0.35"/>']
    for k in range(64):   # derin dikey yarıklar (hafif burguyu izler)
        y0 = yb + 10 - r.uniform(0, 120); y1 = r.uniform(-20, 300); xo = r.uniform(-1, 1)
        x = axis(y0) + xo * half(y0) * 0.92
        T_.append(_furrow(x, y0, y1, r, 10 if abs(xo) < 0.7 else 6, sway=12))
    for k in range(8):   # yatay çatlak kıvrımları
        y = r.uniform(80, yb - 120); x = axis(y) + r.uniform(-0.6, 0.6) * half(y)
        T_.append(f'<path d="M{x-30:.0f},{y:.0f} q30,{r.uniform(-8,8):.0f} 60,0" stroke="#15110D" stroke-width="3" fill="none" opacity="0.7"/>')
    for (ky, kxo, kr) in [(yb - 620, -0.55, 32), (yb - 260, -0.7, 24)]:   # budaklar (yüz oluşturmayacak şekilde dağınık)
        kx = axis(ky) + kxo * half(ky)
        T_.append(f'<path d="{_blob(kx, ky, kr*1.3, kr*0.95, int(ky))}" fill="#3A342A" stroke="#14100C" stroke-width="4" stroke-linejoin="round"/>'
                  f'<path d="{_blob(kx, ky + 2, kr*0.7, kr*0.45, int(ky)+1)}" fill="none" stroke="#1E1A14" stroke-width="3" opacity="0.6"/><ellipse cx="{kx:.0f}" cy="{ky+2:.0f}" rx="{kr*0.28:.0f}" ry="{kr*0.2:.0f}" fill="#120E0A"/>')
    hx = axis(yb - 200) + 0.15 * half(yb - 200)   # kovuk: tabana yakın, tek
    T_.append(f'<path d="M{hx-30:.0f},{yb-130} Q{hx-40:.0f},{yb-250} {hx:.0f},{yb-290} Q{hx+40:.0f},{yb-250} {hx+30:.0f},{yb-130} Q{hx:.0f},{yb-118} {hx-30:.0f},{yb-130} Z" fill="#0E0A08" stroke="#2A2218" stroke-width="7"/>'
              f'<path d="M{hx+34:.0f},{yb-140} Q{hx+46:.0f},{yb-250} {hx+4:.0f},{yb-296}" stroke="#8A8272" stroke-width="4" fill="none" opacity="0.5"/>')
    for k in range(11):
        y = r.uniform(120, yb - 80); T_.append(lichen(axis(y) + r.uniform(-0.8, 0.5) * half(y), y, r.uniform(24, 56), r.uniform(16, 34), 1200 + k))
    T_.append(f'<path d="M{cx-600},{yb-40} H{cx+600} V{yb+40} H{cx-600} Z" fill="#1E1A14" opacity="0.25"/></g>')
    mound = (f'<path d="M{cx-560},{yb+40} Q{cx-300},{yb-10} {cx},{yb-6} Q{cx+320},{yb-12} {cx+600},{yb+40} Z" fill="#33382A" filter="url(#t_tas)"/>'
             + "".join(VB.grass_tuft(cx + k * 90 - 500, yb + 14 + (k % 3) * 6, 50 + (k % 2) * 20, 700 + k, col="#6A7048", dark="#3A3E28") for k in range(12)))
    T_.append(mound)
    pre = rocks + "".join(ROOT) + "".join(LO)
    return pre, "".join(T_), "".join(LF) + "".join(DET), perch

def k20a():
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    draw(c, svg_sprite(sky_dusk("s20", [(0, "#5E6A72"), (0.6, "#A0A8A8"), (1, "#C4C8C0")], 1080)), 0, 0, 1.0)
    glow(c, 1560, 200, 560, "#F0F2EA", 0.35)
    for k, (yb, hm, al, bl) in enumerate([(700, (240, 380), 0.3, 6), (800, (300, 480), 0.5, 4)]):
        f_ = VB.forest(-60, 1980, lambda x, yb=yb: yb + 10 * math.sin(x / 140), hm[0], hm[1], 34, 2000 + k, col="#3A4440", lit="#5A6460", dark="#2A3230")
        draw(c, blurred(svg_sprite(f_), bl), 0, 0, 1.0, a=al)
        draw(c, blurred(svg_sprite(cloud_band(2010 + k, 14, -100, 2000, yb - 200, yb - 40, "#C8CCC6", "#E8EAE4", 0.5, rx=(240, 520), ry=(30, 70))), 14), 0, 0, 1.0)
    g = [TEXD, '<path d="M0,900 Q500,884 960,892 Q1400,880 1920,900 L1920,1080 L0,1080 Z" fill="#3E4430" filter="url(#t_tas)"/>']
    r = R_(2020)
    for k in range(340):
        x = r.uniform(0, 1920); y = r.uniform(890, 1080); g.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r.uniform(3,9):.0f}" ry="{r.uniform(1.5,4):.0f}" fill="{r.choice(["#7A5A34", "#8A6A3A", "#5A6A3A", "#2E3424"])}" opacity="0.8"/>')
    draw(c, svg_sprite("".join(g)), 0, 0, 1.0)
    pre, trunk, limbs, perch = oak(880, 930, 31)
    draw(c, svg_sprite(TEXD + pre), 0, 0, 1.0)
    draw(c, svg_sprite(TEXD + trunk), 0, 0, 1.0)
    draw(c, svg_sprite(TEXD + limbs), 0, 0, 1.0)
    # taç sise karışır
    draw(c, blurred(svg_sprite(cloud_band(2040, 16, -100, 2000, -60, 120, "#B8BEBC", "#E0E2DE", 0.45, rx=(260, 560), ry=(40, 90))), 16), 0, 0, 1.0)
    for x0, x1 in ((-100, 200), (1720, 2020)):
        draw(c, blurred(svg_sprite(cloud_band(2041 + x0, 6, x0, x1, 120, 560, "#B8BEBC", "#E0E2DE", 0.25, rx=(160, 300), ry=(60, 140))), 18), 0, 0, 1.0)
    # kuzgunlar: onaylı model, tek ölçek; Ragnar'ın iki yanındakiler ona döner
    RX = 1190; SC = 0.36
    pv = sorted([q for q in perch if 180 < q[1] < 640 and 60 < q[0] < 1860], key=lambda q: q[0])
    pick = []; 
    for q in pv:
        if all(abs(q[0] - p[0]) > 170 or abs(q[1] - p[1]) > 120 for p in pick): pick.append(q)
    for q in [(300, 352, 40), (560, 332, 50), (1180, 304, 50), (1340, 282, 44)]:
        if all(abs(q[0] - p[0]) > 150 or abs(q[1] - p[1]) > 100 for p in pick): pick.append(q)
    pick = sorted(pick, key=lambda q: q[0])[:7]
    rv = "".join(VB.raven(x, y - 40 * SC, SC, (1 if x < RX else -1) if k % 3 != 2 else (-1 if x < RX else 1), "perch", k) for k, (x, y, w) in enumerate(pick))
    draw(c, svg_sprite(rv), 0, 0, 1.0)
    # soğuk ışık hüzmesi + Ragnar (kökler arasında, küçük, bükük)
    VA.beam(c, 1520, 0, 170, 1200, 990, 300, "#EEF4F8", 0.2, 18)
    draw(c, blurred(svg_sprite(cloud_band(2030, 12, -100, 2000, 985, 1050, "#D8DCD6", "#ECEEEA", 0.14, rx=(260, 560), ry=(12, 26))), 12), 0, 0, 1.0)
    RK = dict(RGO, _kneel=120, cloak="#2E2A26")
    fs = full(RK, "hollow", 0.9, facing=1, look=-0.2)
    glow(c, RX, 900, 170, "#EEF4F8", 0.3); soft_shadow(c, RX, 990, 80, 12, 0.55)
    c.save(); c.translate(RX, 994); c.rotate(14); rim(c, fs, 0, 0, 0.27, "#F4F8FA", dx=4, dy=-3, a=0.9); draw(c, fs, 0, 0, 0.27); c.restore()
    fg = [f'<path d="M-40,1080 Q60,860 220,800" stroke="#1A1E14" stroke-width="30" fill="none"/>'] + [f'<path d="M{60+k*22},{1000-k*26} q{-50},{-10} {-80},{20}" stroke="#2A3220" stroke-width="12" fill="none"/>' for k in range(7)]
    draw(c, blurred(svg_sprite("".join(fg)), 8), 0, 0, 1.0)
    K20A_PERCH[:] = pick
    finish(c, cold=True, warm=0.0); return s
K20A_PERCH = []

# ================================================================ k20b · kopmuş ip ucu, kuzgunlar; yerde Ragnar gökyüzüne bakıyor
def rope_end(x, y, L, seed=5):
    """Dala sarılı ip + kısa sarkan, ucu kopuk ve lif lif dağılmış (ilmek yok)."""
    r = R_(seed); o = []
    for k in range(3):   # dala sarım
        o.append(f'<path d="M{x-40+k*26},{y-34} q14,40 26,70" stroke="#1A1410" stroke-width="22" fill="none" stroke-linecap="round"/><path d="M{x-40+k*26},{y-34} q14,40 26,70" stroke="#A88E62" stroke-width="14" fill="none" stroke-linecap="round"/>')
    o.append(f'<path d="M{x+10},{y+30} Q{x+18},{y+L*0.5:.0f} {x+8},{y+L:.0f}" stroke="#1A1410" stroke-width="24" fill="none" stroke-linecap="round"/><path d="M{x+10},{y+30} Q{x+18},{y+L*0.5:.0f} {x+8},{y+L:.0f}" stroke="#A88E62" stroke-width="15" fill="none"/>')
    for k in range(int(L / 16)):   # bükülmüş halat dokusu
        yy = y + 36 + k * 16; o.append(f'<path d="M{x+2},{yy} l15,10" stroke="#6A5434" stroke-width="3"/>')
    for k in range(14):   # kopuk uç: dağılmış lifler
        a = r.uniform(-50, 50); l = r.uniform(18, 48)
        o.append(f'<path d="M{x+8},{y+L-4:.0f} q{math.sin(math.radians(a))*l*0.5:.0f},{l*0.6:.0f} {math.sin(math.radians(a))*l:.0f},{l:.0f}" stroke="{r.choice(["#C8B088", "#A88E62", "#8A7448"])}" stroke-width="{r.uniform(1.5,3.5):.1f}" fill="none" stroke-linecap="round"/>')
    return "".join(o)

def k20b():
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    draw(c, svg_sprite(sky_dusk("s20b", [(0, "#8A969C"), (0.5, "#C8CEC8"), (1, "#7A846E")], 1080)), 0, 0, 1.0)
    draw(c, blurred(svg_sprite(VB.forest(-60, 1980, lambda x: 640 + 20 * math.sin(x / 90), 300, 520, 30, 2050, col="#4A5450", lit="#6A7470", dark="#3A4240")), 6), 0, 0, 1.0, a=0.5)
    glow(c, 1300, 120, 480, "#FFFFF0", 0.4)
    # yer: yosun ve yapraklar (yakın)
    g = [TEXD, '<path d="M0,640 Q900,600 1920,650 L1920,1080 L0,1080 Z" fill="#4A5236" filter="url(#t_kurk)"/>']
    r = R_(2051)
    for k in range(420):
        x = r.uniform(0, 1920); y = r.uniform(640, 1080); q = (y - 640) / 440
        g.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{4+q*12:.0f}" ry="{2+q*5:.0f}" fill="{r.choice(["#8A6A3A", "#A07A42", "#6A7A42", "#3A4228", "#B08A4A"])}" transform="rotate({r.uniform(-40,40):.0f} {x:.0f} {y:.0f})" opacity="0.85"/>')
    draw(c, svg_sprite("".join(g)), 0, 0, 1.0)
    # Ragnar sırtüstü: baş solda, yüz yukarı, gözler açık
    b = fig_bust(RGO, ex("sky", IF.blink_at(2.0)), 0.9, 1.25)
    soft_shadow(c, 980, 900, 520, 60, 0.45)
    c.save(); c.translate(560, 820); c.rotate(-88)
    with live(c, 0, 0, phase=2.0, breathe=0.006):
        rim(c, b, 0, 0, 1.0, "#F4F4E4", dx=-4, dy=-4, a=0.5); draw(c, b, 0, 0, 1.0)
    c.restore()
    for k in range(60):   # gövde etrafında yapraklar (yere oturma)
        x = r.uniform(300, 1700); y = r.uniform(900, 1060)
        c.drawOval(skia.Rect(x - 10, y - 4, x + 10, y + 4), skia.Paint(AntiAlias=True, Color4f=col(r.choice(["#8A6A3A", "#A07A42", "#6A7A42"]), 0.9)))
    VA.beam(c, 1300, 0, 160, 620, 900, 420, "#FFFCE8", 0.2, 16)
    bloom_spot(c, 600, 760, 140, "#FFF8E0", 0.18)
    # üst: kalın dal, kopmuş ip ucu, iki kuzgun lifleri gagalıyor
    br = [TEXD, '<path d="M-40,250 Q600,170 1200,210 Q1600,236 1980,170 L1980,250 Q1600,300 1200,276 Q600,250 -40,330 Z" fill="#4A4238" stroke="#1A1410" stroke-width="8" filter="url(#t_ahsap)"/>',
          '<path d="M-40,262 Q600,184 1200,222 Q1600,248 1980,184" stroke="#9A9282" stroke-width="6" fill="none" opacity="0.6"/>',
          '<ellipse cx="400" cy="220" rx="140" ry="22" fill="#5E6A3A" opacity="0.85"/><ellipse cx="1600" cy="226" rx="110" ry="16" fill="#5E6A3A" opacity="0.8"/>',
          rope_end(1250, 250, 190, 7),
          VB.raven(1080, 236, 1.0, 1, "perch", 3).replace('<g transform="translate(1080,236)', '<g transform="rotate(26 1080 236) translate(1080,236)'),
          VB.raven(1450, 262, 0.92, -1, "perch", 4).replace('<g transform="translate(1450,262)', '<g transform="rotate(-22 1450 262) translate(1450,262)')]
    draw(c, svg_sprite("".join(br)), 0, 0, 1.0)
    for k in range(9):   # süzülen lifler
        x = 1260 + r.uniform(-80, 120); y = 470 + r.uniform(0, 300); c.drawLine(x, y, x + r.uniform(-12, 12), y + r.uniform(10, 26), skia.Paint(AntiAlias=True, StrokeWidth=2, Color4f=col("#C8B088", 0.8)))
    finish(c, cold=True, warm=0.02); return s

# ================================================================ k21a · boş iskele, tek gemi, Ivar
def k21a():
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    draw(c, svg_sprite(sky_dusk("s21", [(0, "#4A5664"), (0.6, "#98A4AE"), (1, "#D8D4C4")], 600)), 0, 0, 1.0)
    draw(c, blurred(svg_sprite(cloud_band(2101, 12, -100, 2000, 60, 360, "#4E5A68", "#C8D0D6", 0.85, lit_dy=-8, rx=(220, 460), ry=(20, 50))), 4), 0, 0, 1.0)
    glow(c, 1300, 420, 400, "#F4ECD8", 0.35)
    o = [TEXD, ridge_svg([(0, 420), (260, 360), (520, 440), (800, 380), (1100, 450), (1400, 390), (1700, 440), (1920, 400)], 560, "#5A6670"),
         river(540, 1080, 2102, top="#A8B0B4", mid="#5E6E78", bot="#22303A", glint=1300, gcol="#F4ECD8", n=100)]
    draw(c, svg_sprite("".join(o)), 0, 0, 1.0)
    # tek gemi (sağ orta), yelken bağlı
    sh = f'<g transform="translate(1340,700) scale(0.62)">{G.mast_sail(0.0, reefed=True)}{G.hull(1.0, shields=True, oars=False)}</g>'
    draw(c, svg_sprite(sh), 0, 0, 1.0)
    ripples(c, 1340, 800, 360) if hasattr(VP, "ripples") is False else VP.ripples(c, 1340, 810, 360)
    # Ivar güvertede (kanonik yön sola), değnekli
    fs = full(IVAR_ST, "keen", 0.9, facing=-1, look=0.3)
    rim(c, fs, 1300, 700, 0.3, "#E8EEF0", dx=4, dy=-2, a=0.6); draw(c, fs, 1300, 700, 0.3)
    draw(c, svg_sprite(f'<g transform="translate(1340,700) scale(0.62)">' + G.hull(1.0, shields=True, oars=False).split("<!--front-->")[0][:0] + '</g>'), 0, 0, 1.0)
    # iskele: perspektifte uzanan boş tahta yol, kazıklar, boş babalar, gevşek halatlar
    pier = [TEXD, '<path d="M-20,1080 L-20,900 L1000,760 L1120,770 L560,1080 Z" fill="#5A4430" filter="url(#t_ahsap)"/>']
    for k in range(24):
        q = k / 24; y = 1080 - (1080 - 765) * q ** 0.8; x0 = -20 + 0 * q; xr = 560 + (1120 - 560) * q ** 0.8
        pier.append(f'<path d="M{-20 + 1020*q**0.8:.0f},{900 - 140*q**0.8:.0f} L{xr:.0f},{y:.0f}" stroke="#2A1E14" stroke-width="{max(1.5, 5*(1-q)):.1f}"/>')
    pier.append('<path d="M-20,900 L1000,760" stroke="#1A1410" stroke-width="6"/><path d="M560,1080 L1120,770" stroke="#1A1410" stroke-width="10"/>')
    for k in range(7):
        q = k / 6; x = 560 + (1120 - 560) * q ** 0.8; y = 1080 - (1080 - 770) * q ** 0.8; h = 140 * (1 - q * 0.75); w = 30 * (1 - q * 0.7)
        pier.append(f'<rect x="{x-w/2:.0f}" y="{y-h*0.35:.0f}" width="{w:.0f}" height="{h:.0f}" fill="#3A2A1C" stroke="#1A1410" stroke-width="3"/><rect x="{x-w/2:.0f}" y="{y+h*0.4:.0f}" width="{w:.0f}" height="{h*0.12:.0f}" fill="#4E5A3A" opacity="0.7"/>')
        if k in (1, 3, 5): pier.append(f'<path d="M{x:.0f},{y-h*0.3:.0f} Q{x+60*(1-q):.0f},{y+h*0.5:.0f} {x+130*(1-q*0.6):.0f},{y+h*0.3:.0f}" stroke="#A88E62" stroke-width="{max(2,6*(1-q)):.1f}" fill="none"/>')
    pier.append(VB.post(1180, 820, 120, 26, 9) + '<path d="M1180,740 Q1240,800 1300,770" stroke="#A88E62" stroke-width="5" fill="none"/>')
    for k in range(3): pier.append(f'<ellipse cx="300" cy="{1000-k*7}" rx="{80-k*12}" ry="{20-k*3}" fill="none" stroke="#1A1410" stroke-width="12"/><ellipse cx="300" cy="{1000-k*7}" rx="{80-k*12}" ry="{20-k*3}" fill="none" stroke="#B8A070" stroke-width="7" stroke-dasharray="8 3"/>')
    pier.append('<g transform="translate(150,940)"><rect x="-50" y="-90" width="100" height="90" rx="12" fill="#6A4A2C" stroke="#1A1410" stroke-width="5"/><path d="M-50,-60 H50 M-50,-28 H50" stroke="#2A2A2A" stroke-width="7"/></g>')
    draw(c, svg_sprite("".join(pier)), 0, 0, 1.0)
    # Ragnar iskelede, sırtı dönük, gemiye bakıyor
    rb = full(RGO, "neutral", 0.9, facing=1, view="back")
    soft_shadow(c, 700, 852, 60, 9, 0.45); rim(c, rb, 700, 856, 0.33, "#E8EEF0", dx=-3, dy=-2, a=0.6); draw(c, rb, 700, 856, 0.33)
    for k, (x, y) in enumerate([(300, 200), (1650, 260), (900, 150)]): draw(c, svg_sprite(VB.gull(x, y, 0.5, k)), 0, 0, 1.0)
    draw(c, blurred(svg_sprite(cloud_band(2103, 10, -100, 2000, 700, 820, "#D8DCDA", "#EEEEE8", 0.3, rx=(200, 420), ry=(14, 28))), 10), 0, 0, 1.0)
    finish(c, cold=True, warm=0.0); return s

# ================================================================ k21b · sabah kıyısı, enkaz, Ragnar ve Ivar
def plank(x, y, L, rot, w=26, seed=0):
    r = R_(seed)
    return (f'<g transform="translate({x},{y}) rotate({rot})"><path d="M0,0 L{L},{r.uniform(-4,4):.0f} L{L-10},{w} L{L*0.6:.0f},{w-4} L{L*0.5:.0f},{w+8} L0,{w} Z" fill="#6A4A2E" stroke="#1A1410" stroke-width="4" filter="url(#t_ahsap)"/>'
            f'<path d="M6,{w*0.4:.0f} H{L-20}" stroke="#2A1A10" stroke-width="2" opacity="0.6"/><circle cx="{L*0.3:.0f}" cy="{w/2:.0f}" r="3" fill="#2A2A2A"/><path d="M{L-10},0 l12,-8 l-2,14 l10,4" stroke="#C8A878" stroke-width="2" fill="none"/></g>')

def k21b():
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    draw(c, svg_sprite(sky_dusk("s21b", [(0, "#3A4050"), (0.4, "#8A8A94"), (0.75, "#E8C090"), (1, "#F4D8A8")], 620)), 0, 0, 1.0)
    draw(c, blurred(svg_sprite(cloud_band(2111, 12, 900, 2100, 40, 300, "#2A2E3A", "#A88A80", 0.95, lit_dy=10, rx=(260, 520), ry=(40, 90))), 4), 0, 0, 1.0)   # çekilen fırtına
    for k in range(30):   # uzakta yağmur perdesi
        x = 1300 + k * 22; draw(c, svg_sprite(f'<path d="M{x},300 l-30,260" stroke="#4A4E5A" stroke-width="3" opacity="0.35"/>'), 0, 0, 1.0)
    glow(c, 420, 540, 560, "#FFD8A0", 0.45); bloom_spot(c, 420, 560, 70, "#FFF4DC", 0.8); rays(c, 420, 560, 20, 1400, 50, 9, "#FFE8C0", 0.07, 0.0)
    o = [TEXD, river(560, 800, 2112, top="#E8C8A0", mid="#7A8A94", bot="#3A4A54", glint=420, gcol="#FFE8C0", n=80)]
    o.append(f'<g transform="translate(1500,600) rotate(70) scale(0.12)">{G.mast_sail(0.6)}</g>')   # uzakta devrik direk
    draw(c, svg_sprite("".join(o)), 0, 0, 1.0)
    # kumsal + çakıl + yosun
    g = [TEXD, '<path d="M0,760 Q500,730 960,770 Q1400,800 1920,760 L1920,1080 L0,1080 Z" fill="#8A7A64" filter="url(#t_tas)"/>',
         '<path d="M0,770 Q500,740 960,780 Q1400,810 1920,770" stroke="#E8E6DC" stroke-width="10" fill="none" opacity="0.7"/>',
         VC.pebbles(2113, 260, 0, 1920, 780, 1080, hl="#F4D8A8")]
    r = R_(2114)
    for k in range(40): x = r.uniform(0, 1920); y = r.uniform(790, 1060); g.append(f'<path d="M{x:.0f},{y:.0f} q20,-10 40,0 q20,8 40,-2" stroke="#3A4A28" stroke-width="5" fill="none" opacity="0.8"/>')
    # enkaz: kırık gövde parçası, tahtalar, yırtık yelken, kürek, kırık kalkanlar, ejder başı, fıçı, halat
    g.append(f'<g transform="translate(1000,860) rotate(-8) scale(0.45)"><defs><clipPath id="hc"><rect x="-200" y="-300" width="760" height="600"/></clipPath></defs><g clip-path="url(#hc)">{G.hull(1.0, shields=False, oars=False, wet=True)}</g>'
             '<path d="M-200,-300 L-170,-120 L-210,-40 L-180,120 L-200,300" stroke="#E8D0A0" stroke-width="8" fill="none"/></g>')
    g.append('<g transform="translate(-330,90)"><path d="M500,900 Q620,850 760,890 Q800,940 740,990 Q620,1010 520,970 Z" fill="#C8B49A" stroke="#1A1410" stroke-width="5"/>'
             '<path d="M520,920 L760,910 M540,950 L740,945" stroke="#B8322A" stroke-width="22" opacity="0.85"/><path d="M600,860 L620,1000" stroke="#1A1410" stroke-width="3" opacity="0.5"/></g>')
    for k, (x, y, L, rot) in enumerate([(200, 960, 260, -12), (1300, 990, 300, 8), (1500, 900, 220, -20), (820, 1020, 200, 4), (60, 860, 180, 16)]): g.append(plank(x, y, L, rot, 26, k))
    g.append('<path d="M1620,1000 L1900,860" stroke="#1A1410" stroke-width="20" stroke-linecap="round"/><path d="M1620,1000 L1900,860" stroke="#8A6A46" stroke-width="12"/><path d="M1590,1010 l40,-10 l20,40 l-50,10 Z" fill="#8A6A46" stroke="#1A1410" stroke-width="4"/>')
    g.append(VP.broken_shield(380, 1030, 0.7, "#8E1E22", "#E8D8B0", rot=-10) + VP.broken_shield(1180, 940, 0.55, "#2E4478", "#E8D8B0", rot=14))
    g.append(G.dragon_head(1420, 820, 0.55, "#5A4632"))
    g.append('<g transform="translate(1760,1000) rotate(80)"><rect x="-50" y="-70" width="100" height="140" rx="20" fill="#6A4A2C" stroke="#1A1410" stroke-width="5"/><path d="M-50,-30 H50 M-50,30 H50" stroke="#2A2A2A" stroke-width="8"/></g>')
    for k in range(5): g.append(f'<path d="M{80+k*12},{1040-k*6} q60,-20 120,0" stroke="#A88E62" stroke-width="6" fill="none"/>')
    draw(c, svg_sprite("".join(g)), 0, 0, 1.0)
    # Ragnar: ayakta, ıslak, denize bakıyor (sol); Ivar enkaz üstünde oturuyor (sağ, sola bakar)
    fs = full(dict(RGO, cloak="#2A3040"), "weary", 0.9, facing=1, look=0.3)
    soft_shadow(c, 640, 900, 90, 12, 0.5); rim(c, fs, 640, 906, 0.5, "#FFD8A0", dx=-6, dy=-2, a=0.85); draw(c, fs, 640, 906, 0.5); shade_side(c, fs, 640, 906, 0.4, 660, 780, "#1A2030")
    hullseat = (TEXD + '<path d="M1010,960 Q1000,800 1060,770 L1320,770 Q1380,800 1370,960 Z" fill="#5A3E26" stroke="#1A1410" stroke-width="6" filter="url(#t_ahsap)"/>'
                + "".join(f'<path d="M{1010+k*3},{790+k*34} Q1190,{770+k*34} {1370-k*2},{790+k*34}" stroke="#2A1A10" stroke-width="5" fill="none"/>' for k in range(5))
                + "".join(f'<circle cx="{1050+k*60}" cy="{810+(k%2)*60}" r="5" fill="#3A3A3A"/>' for k in range(6))
                + '<path d="M1010,960 Q1190,990 1370,960" stroke="#1A1410" stroke-width="8" fill="none"/><path d="M1060,770 L1320,770" stroke="#C8A878" stroke-width="4"/>')
    draw(c, svg_sprite(hullseat + crutch_line(1040, 1000, 1080, 640, 0.62)), 0, 0, 1.0)
    ivar_seat(c, 1190, 560, 0.62, "hollow2", look=0.3, rim_c="#FFD8A0", seed=1.1)
    draw(c, svg_sprite(TEXD + '<path d="M1080,800 Q1190,740 1310,790 L1300,840 Q1190,860 1070,840 Z" fill="#3A3236" stroke="#1A1410" stroke-width="5" filter="url(#t_kurk)"/>' + crutch_line(1350, 1000, 1310, 660, 0.62)), 0, 0, 1.0)
    r2 = R_(2115)
    for k in range(40): c.drawCircle(r2.uniform(0, 1920), r2.uniform(760, 800), r2.uniform(1, 3), skia.Paint(AntiAlias=True, Color4f=col("#FFF4DC", r2.uniform(0.3, 0.8))))
    finish(c, cold=False, warm=0.05); return s

FR = {"model": model, "k19a": k19a, "k19b": k19b, "k19c": k19c, "k19d": k19d, "k20a": k20a, "k20b": k20b, "k21a": k21a, "k21b": k21b}

CROPS = {"model": [(1440, 300, 480, 420), (1100, 440, 520, 300)], "k19c": [(250, 150, 700, 600), (700, 300, 700, 700)], "k20a": [(640, 240, 640, 720), (1100, 180, 520, 300)], "k20b": [(1000, 120, 640, 560), (250, 500, 900, 520)]}
def contact(ids):
    from PIL import Image
    n = len(ids); rows = (n + 1) // 2
    sheet = Image.new("RGB", (960 * 2 + 30, 560 * rows + 10), "#EDE2CC")
    for k, i in enumerate(ids): sheet.paste(Image.open(f"{OUTK}/{i}.png").convert("RGB").resize((960, 540)), (10 + (k % 2) * 970, 10 + (k // 2) * 560))
    sheet.save(f"{OUTK}/kontakt_kayip_960.png")
if __name__ == "__main__":
    ids = sys.argv[1:] or list(FR)
    for i in ids:
        T[0] = None; p = f"{OUTK}/{i}.png"
        FR[i]().makeImageSnapshot().save(p, skia.kPNG); print("kare", i, flush=True)
        for k, b in enumerate(CROPS.get(i, []), 1): crop2x(p, b, f"{OUTK}/{i}_crop{k}.png")
    contact([i for i in FR if os.path.exists(f"{OUTK}/{i}.png")])
