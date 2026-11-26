import random
"""Eklemli kukla parçaları (profil, diz çökme, 3/4 yakın kafa, arkadan diz çökme).
Her parça kendi eklem noktasına (pivot) göre çizilir; skia'da döndürülerek oynatılır."""
import sys, math
sys.path.insert(0, "/home/claude/r3"); sys.path.insert(0, "/home/claude/r2")
import art2
from art2 import INK, shade, limb
from art3 import head3, hand3, RAGNAR_UC, braid, strands, EXP, knot_mark
from engine import sprite
from bg import GRAIN

SPEC = dict(RAGNAR_UC, cloak="#26344A")
SK = SPEC["skin"]; TUN = SPEC["tunic"]; FUR = SPEC["fur"]; CLOAK = SPEC["cloak"]
HS = 82 / 80
WET = dict(SPEC, hair=shade(SPEC["hair"], 0.72), beard_c=shade(SPEC["beard_c"], 0.72), brow_k=0.68)   # kafa ölçeği (tall gövde)

EXP["grief_closed"] = (-11, 5, 0.95, 0.10, "tremble", "")
EXP["grief_wet"] = (-11, 5, 0.26, 0.12, "tremble", "")
EXP["grief_wet2"] = (-12, 5, 0.28, 0.12, "tremble2", "")
EXP["grief_down"] = (-11, 5, 0.55, 0.12, "tremble", "")
EXP["grief"] = (-10, 5, 0.45, 0.10, "tremble", "tear")

def part(svg, w, h, ox, oy, ss=1.4):
    return sprite(f'<g transform="translate({ox},{oy})">{svg}</g>', w, h, ax=ox, ay=oy, ss=ss, defs=f"<defs>{GRAIN}</defs>")

# ───────── PROFİL (sağa bakar). Kök: kalça (0,0). Omuz (24,-196). Boyun (14,-250). Ayak yere y=+240
def leg_side(shade_k=1.0):
    fur = shade(FUR, shade_k); boots = shade("#2E2016", shade_k)
    s = art2.fur_leg(0, 0, 0, 214, 54, fur)
    s += f'<path d="M-26,206 L22,206 Q52,216 48,236 L-28,236 Z" fill="{boots}" stroke="{INK}" stroke-width="4.5" stroke-linejoin="round"/>'
    return part(s, 200, 320, 90, 40)

def torso_side():
    o = []
    # pelerin (arkada)
    o.append(f'<path d="M-46,-206 Q-110,-60 -96,40 L0,40 Q-10,-80 -16,-210 Z" fill="{CLOAK}" stroke="{INK}" stroke-width="5"/>')
    o.append(f'<path d="M-60,-180 Q-86,-60 -76,30" stroke="{shade(CLOAK,0.72)}" stroke-width="20" fill="none" opacity="0.8"/>')
    torso = "M-40,-212 Q-58,-110 -38,0 L-46,60 Q0,72 56,54 L46,0 Q64,-140 50,-212 Q0,-226 -40,-212 Z"
    o.append(f'<defs><clipPath id="tsd"><path d="{torso}"/></clipPath></defs><path d="{torso}" fill="{TUN}"/>')
    o.append(f'<g clip-path="url(#tsd)"><rect x="18" y="-240" width="80" height="320" fill="{shade(TUN,0.78)}"/><path d="M-60,50 Q0,66 70,46" stroke="{SPEC["trim"]}" stroke-width="12" fill="none"/></g>')
    o.append(f'<path d="{torso}" fill="none" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>')
    o.append(f'<path d="M-42,-6 Q0,4 50,-8" stroke="#3A2418" stroke-width="18" fill="none"/><rect x="38" y="-18" width="22" height="22" rx="4" fill="#D8A93A" stroke="{INK}" stroke-width="3.5"/>')
    o.append(f'<rect x="-6" y="-262" width="40" height="60" fill="{shade(SK,0.85)}" stroke="{INK}" stroke-width="4"/>')
    for i in range(6):
        t = i / 5; x = -50 + 100 * t; y = -214 + 6 * math.sin(t * math.pi)
        o.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="22" fill="{SPEC["fur_collar"]}" stroke="{INK}" stroke-width="4"/>')
    return part("".join(o), 300, 380, 130, 280)

def head_side(expr="grief"):
    return part(f'<g transform="scale({HS})">{head3(WET, "side", expr)}</g>', 340, 420, 150, 230)

def arms_carry(near=True):
    """Omuz pivotu (0,0). Kollar öne bükük, sarılı beden kolların üstünde."""
    o = []
    col = TUN if near else shade(TUN, 0.7); sk = SK if near else shade(SK, 0.88)
    o.append(limb([(0, 0), (34, 108), (150, 96)], 36, col))
    o.append(hand3(160, 92, 20, sk, "grip", 1))
    return part("".join(o), 360, 260, 80, 60)

def shroud():
    lin_ = "#D9D2C2"
    s = (f'<path d="M-196,-30 Q-214,-62 -178,-70 Q-140,-74 -128,-40 Q-60,-20 0,6 Q90,-10 150,-34 Q196,-44 206,-6 Q212,30 170,44 Q90,70 0,72 Q-80,62 -150,30 Q-206,28 -196,-30 Z" fill="{lin_}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
         f'<path d="M-150,-30 Q-70,10 0,34 Q90,24 170,-4" stroke="#B8B0A0" stroke-width="12" fill="none" opacity="0.7"/>'
         f'<path d="M-170,-52 Q-150,-40 -160,-20" stroke="#B8B0A0" stroke-width="5" fill="none"/>'
         + "".join(f'<path d="M{x},{y0} Q{x+10},{(y0+y1)/2} {x},{y1}" stroke="#7A6248" stroke-width="7" fill="none"/>' for x, y0, y1 in ((-128,-42,30), (-30,-2,66), (80,-14,64), (160,-36,40)))
         + f'<path d="M-30,70 Q-34,110 -20,140 M40,68 Q50,104 40,132" stroke="{lin_}" stroke-width="12" fill="none" stroke-linecap="round" opacity="0.9"/>')
    return part(s, 480, 260, 240, 90)

# ───────── PROFİL DİZ ÇÖKME. Kök: diz yerde (0,0); kalça (-30,-130); omuz (-6,-326)
def kneel_side():
    o = []
    fur = FUR; boots = "#2E2016"
    o.append(f'<path d="M-60,-300 Q-130,-150 -120,20 L-10,20 Q-30,-120 -26,-306 Z" fill="{CLOAK}" stroke="{INK}" stroke-width="5"/>')
    # arka bacak: diz yerde, kaval yerde geriye
    o.append(art2.fur_leg(-30, -130, -10, -8, 54, shade(fur, 0.85)))
    o.append(art2.fur_leg(-10, -8, -190, 6, 50, shade(fur, 0.85)))
    o.append(f'<path d="M-200,-16 L-240,-10 Q-250,6 -236,18 L-196,18 Z" fill="{boots}" stroke="{INK}" stroke-width="4"/>')
    # ön bacak: diz yukarı
    o.append(art2.fur_leg(-24, -128, 110, -110, 54, fur))
    o.append(art2.fur_leg(110, -110, 106, 0, 50, fur))
    o.append(f'<path d="M84,-10 L134,-10 Q160,2 154,18 L82,18 Z" fill="{boots}" stroke="{INK}" stroke-width="4.5"/>')
    torso = "M-58,-340 Q-74,-230 -56,-130 L-64,-80 Q-20,-64 34,-84 L28,-130 Q50,-260 38,-340 Q-10,-352 -58,-340 Z"
    o.append(f'<defs><clipPath id="tks"><path d="{torso}"/></clipPath></defs><path d="{torso}" fill="{TUN}"/>')
    o.append(f'<g clip-path="url(#tks)"><rect x="6" y="-360" width="80" height="300" fill="{shade(TUN,0.78)}"/><path d="M-80,-86 Q-10,-70 50,-90" stroke="{SPEC["trim"]}" stroke-width="12" fill="none"/></g>')
    o.append(f'<path d="{torso}" fill="none" stroke="{INK}" stroke-width="5"/>')
    o.append(f'<path d="M-60,-136 Q-14,-126 32,-138" stroke="#3A2418" stroke-width="18" fill="none"/>')
    o.append(f'<rect x="-24" y="-392" width="40" height="60" fill="{shade(SK,0.85)}" stroke="{INK}" stroke-width="4"/>')
    for i in range(6):
        t = i / 5; x = -70 + 104 * t; y = -342 + 6 * math.sin(t * math.pi)
        o.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="22" fill="{SPEC["fur_collar"]}" stroke="{INK}" stroke-width="4"/>')
    return part("".join(o), 520, 480, 280, 420)

def arms_cross():
    """Omuz pivotu (0,0): iki kol öne, ellerde dikey haç kazığı (tutuş noktası el)."""
    o = []
    o.append(limb([(0, 0), (70, 70), (150, 40)], 36, shade(TUN, 0.7)))
    wood = "#6E5034"
    o.append(f'<rect x="150" y="-110" width="20" height="440" fill="{wood}" stroke="{INK}" stroke-width="5"/>'
             f'<rect x="104" y="-70" width="112" height="20" fill="{wood}" stroke="{INK}" stroke-width="5"/>'
             f'<path d="M150,330 L160,362 L170,330 Z" fill="{wood}" stroke="{INK}" stroke-width="4"/>')
    o.append(hand3(158, 34, 20, shade(SK, 0.9), "grip", 1))
    o.append(limb([(4, 6), (80, 90), (160, 70)], 38, TUN))
    o.append(hand3(166, 66, 21, SK, "grip", 1))
    o.append(knot_mark(166, 60, 0.6))
    return part("".join(o), 420, 600, 100, 160)

def cross_planted():
    wood = "#6E5034"
    return part(f'<rect x="-10" y="-200" width="20" height="210" fill="{wood}" stroke="{INK}" stroke-width="5"/><rect x="-56" y="-160" width="112" height="20" fill="{wood}" stroke="{INK}" stroke-width="5"/>', 160, 260, 80, 230)

# ───────── YAKIN PLAN 3/4 KAFA + omuz
def fur_mantle(x0, x1, y, d, n=22, seed=3):
    r = random.Random(seed); fc = SPEC["fur_collar"]
    top = f"M{x0},{y+d}"
    pts = []
    for i in range(n + 1):
        t = i / n; x = x0 + (x1 - x0) * t; yy = y - 40 * math.sin(t * math.pi) + r.uniform(-8, 8)
        pts.append((x, yy))
    d_ = f"M{x0},{y+d} " + " ".join(f"L{x:.0f},{yy:.0f} L{x+(x1-x0)/n/2:.0f},{yy-r.uniform(14,30):.0f}" for x, yy in pts) + f" L{x1},{y+d} "
    d_ += " ".join(f"L{x1-(x1-x0)*i/n:.0f},{y+d+r.uniform(-6,26):.0f}" for i in range(n + 1)) + " Z"
    out = f'<path d="{d_}" fill="{fc}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
    for i in range(30):
        x = r.uniform(x0 + 20, x1 - 20); yy = r.uniform(y - 20, y + d - 10)
        out += f'<path d="M{x:.0f},{yy:.0f} q{r.uniform(-8,8):.0f},{r.uniform(10,22):.0f} {r.uniform(-4,4):.0f},{r.uniform(22,34):.0f}" stroke="{shade(fc,0.7)}" stroke-width="3" fill="none"/>'
    return out

def wet_overlay():
    """Baş koordinatında (3q) ıslaklık: alın/yanak parlaması, alna yapışmış tutamlar, sakalda damlalar."""
    r = random.Random(8); hc = WET["hair"]
    o = [f'<path d="M-6,-52 Q14,-58 34,-50" stroke="#FFFFFF" stroke-width="3" fill="none" opacity="0.55" stroke-linecap="round"/>',
         f'<path d="M50,6 Q58,12 58,24" stroke="#FFFFFF" stroke-width="2.6" fill="none" opacity="0.5" stroke-linecap="round"/>',
         f'<path d="M-30,10 Q-34,18 -32,26" stroke="#FFFFFF" stroke-width="2.2" fill="none" opacity="0.4" stroke-linecap="round"/>',
         f'<path d="M6,-74 Q0,-56 8,-38 Q10,-30 4,-24" stroke="{hc}" stroke-width="4" fill="none" stroke-linecap="round"/>',
         f'<path d="M16,-74 Q14,-60 20,-48" stroke="{hc}" stroke-width="3" fill="none" stroke-linecap="round"/>']
    for i in range(16):
        x = r.uniform(-40, 70); y = r.uniform(50, 110)
        o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r.uniform(1.6,3.2):.1f}" fill="#E8F4FF" opacity="0.85"/>')
    return "".join(o)

def bust_3q(expr="grief_wet", cross=False):
    o = []
    o.append(f'<path d="M-330,620 Q-320,320 -140,260 L150,250 Q330,320 340,620 Z" fill="{TUN}" stroke="{INK}" stroke-width="6"/>')
    o.append(f'<path d="M60,260 Q200,300 230,520 L280,520 Q270,300 130,240 Z" fill="{shade(TUN,0.78)}"/>')
    o.append(fur_mantle(-300, 320, 250, 90))
    # Athelstan'ın haçı (göğüste)
    if cross: o.append(f'<path d="M-40,250 Q10,340 60,250" stroke="#8A7A5A" stroke-width="3" fill="none"/><g transform="translate(10,350)"><rect x="-7" y="-10" width="14" height="52" fill="#C9A25A" stroke="{INK}" stroke-width="3"/><rect x="-22" y="2" width="44" height="12" fill="#C9A25A" stroke="{INK}" stroke-width="3"/></g>')
    o.append(f'<rect x="-50" y="120" width="100" height="140" fill="{shade(SK,0.85)}" stroke="{INK}" stroke-width="5"/>')
    o.append(f'<g transform="translate(6,0) scale(2.0)">{head3(WET, "3q", expr, look=-0.25)}{wet_overlay()}</g>')
    return part("".join(o), 820, 1100, 410, 440, ss=1.2)

# ───────── ARKADAN DİZ ÇÖKME (siluet için). Kök: dizler yer (0,0)
def back_kneel_uc(spec=None, pray=False, expr="grief_down", face=-1):
    """Sırttan diz çökme. pray=True: eller göğüs önünde birleşik (görünmez), kollar öne, pelerin/kürk spec'ten."""
    spec = spec or WET
    cl = spec.get("cloak", CLOAK); tun = spec.get("tunic", TUN); sk = spec.get("skin", SK)
    o = []
    for sx in (-1, 1):  # topuklar + kıvrık bacak tabanı
        o.append(f'<path d="M{sx*20},-6 Q{sx*70},-34 {sx*110},-14 L{sx*108},10 Q{sx*60},4 {sx*20},12 Z" fill="#3A2C20" stroke="{INK}" stroke-width="5"/>')
        o.append(f'<ellipse cx="{sx*100}" cy="-4" rx="24" ry="16" fill="#2E2016" stroke="{INK}" stroke-width="5"/>')
    if not pray:
        o.append(limb([(-80, -230), (-160, -150), (-250, -70)], 36, shade(tun, 0.8)))
        o.append(hand3(-262, -62, 20, sk, "open", -1))
    else:
        for sx in (-1, 1):  # kollar öne bükük, dirsekler yanlardan görünür
            o.append(f'<path d="M{sx*118},-250 Q{sx*150},-180 {sx*112},-150" stroke="{INK}" stroke-width="44" fill="none" stroke-linecap="round"/><path d="M{sx*118},-250 Q{sx*150},-180 {sx*112},-150" stroke="{shade(tun,0.85)}" stroke-width="36" fill="none" stroke-linecap="round"/>')
    o.append(f'<path d="M-110,-270 Q-160,-130 -150,0 L150,0 Q160,-130 110,-270 Q0,-290 -110,-270 Z" fill="{cl}" stroke="{INK}" stroke-width="6"/>')
    o.append(f'<path d="M40,-260 Q76,-130 66,-6" stroke="{shade(cl,0.72)}" stroke-width="32" fill="none" opacity="0.8"/>')
    if spec.get("fur", True): o.append(fur_mantle(-150, 150, -282, 46, n=14, seed=5))
    else: o.append(f'<path d="M-100,-282 Q0,-300 100,-282 L96,-262 Q0,-278 -96,-262 Z" fill="{shade(tun,0.9)}" stroke="{INK}" stroke-width="5"/>')
    if pray:
        o.append(f'<path d="M{20*face},-350 L{50*face},-290 L{-10*face},-282 L{-30*face},-330 Z" fill="{shade(sk,0.85)}" stroke="{INK}" stroke-width="5"/>')
        o.append(f'<g transform="translate({138*face},-228) rotate({-20*face})"><ellipse rx="22" ry="15" fill="{sk}" stroke="{INK}" stroke-width="4"/><path d="M{-6*face},-14 L{14*face},-34 L{22*face},-22 Z" fill="{sk}" stroke="{INK}" stroke-width="4"/></g>')
    o.append(f'<g transform="translate({60*face},-420) rotate({22*face}) scale({HS*face},{HS})">{head3(spec, "side", expr)}</g>')
    return part("".join(o), 700, 720, 360, 640)
