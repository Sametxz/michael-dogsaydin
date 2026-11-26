"""Bölüm IV · Paris ham kareleri (brief: kurul/BRIEF_bolum4.md). Tek görsel ajan.
python3 v4_paris.py [p15b ...] → /home/claude/r3/paris/<id>.png (+ R13 kırpmaları), kontakt_paris_960.png
Ortak dosyalara yazmaz; v3 tekniklerini (v3_a/b/c) içe aktarır.
"""
import sys, os, math, random
sys.path.insert(0, "/home/claude/r3/bati")
from kareler6 import *
import tex
import v3_a as VA, v3_b as VB, v3_c as VC
from v3_c import cloud_band, gradient, flames, soft_shadow, crop2x, gull, pebbles, breath
OUTP = "/home/claude/r3/paris"; os.makedirs(OUTP, exist_ok=True)
R_ = random.Random
TEXD = tex.defs("ahsap", "tas", "deri", "kurk", "yun", "metal", "keten")
EXP["dead"] = (0, 0, 1.0, 0.0, "flat", "")

# ================================================================ karakterler (model gövdeleri)
FHELM = ('<path d="M-86,-28 Q-82,-104 0,-154 Q82,-104 86,-28 Z" fill="#8E969C" stroke="#1A1410" stroke-width="6"/>'
         '<path d="M-24,-140 Q-54,-92 -62,-36" stroke="#D8DEE2" stroke-width="7" fill="none" opacity="0.8"/><path d="M30,-136 Q60,-90 66,-36" stroke="#4A5258" stroke-width="10" fill="none" opacity="0.6"/>'
         '<path d="M-88,-34 L88,-34" stroke="#1A1410" stroke-width="18"/><path d="M-88,-34 L88,-34" stroke="#6A7278" stroke-width="10"/>'
         + "".join(f'<circle cx="{x}" cy="-34" r="3.5" fill="#C8D0D6"/>' for x in range(-76, 80, 19))
         + '<rect x="-9" y="-40" width="18" height="74" rx="4" fill="#8E969C" stroke="#1A1410" stroke-width="4"/>'
         '<path d="M-84,-28 Q-96,30 -70,70 L-50,40 Q-70,10 -66,-28 Z M84,-28 Q96,30 70,70 L50,40 Q70,10 66,-28 Z" fill="#7A8288" stroke="#1A1410" stroke-width="4"/>')   # zincir yanak örtüsü
MITRE_H = ('<path d="M-68,-46 L-56,-176 Q-28,-206 0,-222 Q28,-206 56,-176 L68,-46 Z" fill="#F2ECDE" stroke="#1A1410" stroke-width="6"/>'
           '<path d="M0,-216 L0,-50 M-62,-110 L62,-110" stroke="#C9A25A" stroke-width="12"/><path d="M-68,-50 L68,-50" stroke="#1A1410" stroke-width="18"/><path d="M-68,-50 L68,-50" stroke="#C9A25A" stroke-width="11"/>'
           '<circle cx="0" cy="-110" r="11" fill="#8E1E22" stroke="#1A1410" stroke-width="3"/><path d="M40,-170 L56,-60" stroke="#C8BEA8" stroke-width="10" opacity="0.6"/>'
           '<path d="M-70,-46 Q-82,10 -92,70 M70,-46 Q82,10 92,70" stroke="#C9A25A" stroke-width="10" fill="none"/>')   # infulae (sarkan bantlar)

def surcoat(c1, c2):
    """Zincir zırh üstü Frank cüppesi (gövde önü) + zincir halka dokusu (figür koordinatı)."""
    mail = "".join(f'<path d="M{x},{y} q5,6 10,0" stroke="#4A5258" stroke-width="2.4" fill="none"/>' for y in range(-440, -250, 11) for x in range(-84 + (y // 11 % 2) * 5, 80, 10))
    return (f'<g>{mail}<path d="M-56,-430 L56,-430 L74,-170 Q0,-150 -74,-170 Z" fill="{c1}" stroke="#1A1410" stroke-width="6"/>'
            f'<path d="M0,-430 L0,-160" stroke="{c2}" stroke-width="12"/><path d="M-60,-340 L62,-340" stroke="{c2}" stroke-width="10"/>'
            f'<path d="M30,-420 L48,-176" stroke="#000" stroke-width="20" opacity="0.18"/></g>')

def kite(c1, c2, x=58, y=-300, s=1.0):
    return (f'<g transform="translate({x},{y}) scale({s})"><path d="M0,-150 Q84,-140 82,-50 Q70,70 0,170 Q-70,70 -82,-50 Q-84,-140 0,-150 Z" fill="{c1}" stroke="#1A1410" stroke-width="7"/>'
            f'<path d="M0,-140 Q76,-130 74,-50 Q62,64 0,158" stroke="#000" stroke-width="16" fill="none" opacity="0.2"/>'
            f'<path d="M0,-140 L0,160 M-74,-50 L74,-50" stroke="{c2}" stroke-width="12"/><circle cx="0" cy="-50" r="16" fill="#B8BEC4" stroke="#1A1410" stroke-width="4"/>'
            f'<path d="M0,-150 Q84,-140 82,-50 Q70,70 0,170 Q-70,70 -82,-50 Q-84,-140 0,-150 Z" fill="none" stroke="#5A5A58" stroke-width="5"/></g>')

FCOL = [("#2E4478", "#E2B23A"), ("#8E1E22", "#E2B23A"), ("#2E4478", "#C8C2B0"), ("#6A1A22", "#C8C2B0")]
def frank(seed, weapon="spear", shield=True, arm=None):
    r = R_(seed); h = r.choice(KL.HAIR); c1, c2 = FCOL[seed % 4]
    sp = dict(KL.soldier_spec(seed + 400, "ragnar", weapon), hair=h, beard_c=h, beard_len=r.uniform(0.15, 0.5), tunic="#7C848A", trim="#5A6268",
              cloak=r.choice(["#2A3450", "#4A1A1E", "#33302C"]), fur_collar="#5A6268", armring=False, _head_extra=FHELM)
    sp["_body_extra"] = surcoat(c1, c2) + (kite(c1, c2) if shield else "")
    if arm is not None: sp["_arm_up"] = arm
    return sp

ROLLO_F = dict(ROLLO, tunic="#7C848A", trim="#C9A25A", cloak="#8E1E22", fur_collar="#C9A25A", _head_extra=FHELM, _body_extra=surcoat("#8E1E22", "#E2B23A"))
CROZIER = ('<g transform="translate(HX,HY)"><path d="M0,140 L0,-430" stroke="#1A1410" stroke-width="16" stroke-linecap="round"/><path d="M0,140 L0,-430" stroke="#C9A25A" stroke-width="8"/>'
           '<path d="M0,-430 Q0,-520 60,-520 Q110,-516 104,-466 Q96,-430 60,-440" stroke="#1A1410" stroke-width="16" fill="none" stroke-linecap="round"/><path d="M0,-430 Q0,-520 60,-520 Q110,-516 104,-466 Q96,-430 60,-440" stroke="#E8C060" stroke-width="8" fill="none" stroke-linecap="round"/>'
           '<rect x="-14" y="-420" width="28" height="22" rx="6" fill="#E2B23A" stroke="#1A1410" stroke-width="4"/></g>')
EWER = ('<g transform="translate(HX,HY) rotate(-55)"><path d="M-30,-10 Q-44,-70 -20,-96 L20,-96 Q44,-70 30,-10 Z" fill="#D8A440" stroke="#1A1410" stroke-width="5"/><path d="M14,-90 Q30,-60 22,-14" stroke="#7A5214" stroke-width="8" fill="none" opacity="0.6"/>'
        '<path d="M20,-90 Q60,-110 74,-140" stroke="#1A1410" stroke-width="10" fill="none"/><path d="M20,-90 Q60,-110 74,-140" stroke="#E2B23A" stroke-width="5" fill="none"/>'
        '<ellipse cx="0" cy="-96" rx="22" ry="6" fill="#C9A25A" stroke="#1A1410" stroke-width="3"/><path d="M-14,-80 Q-22,-50 -14,-24" stroke="#FFF2C0" stroke-width="4" fill="none"/></g>')
BISHOP = dict(ATHv, hair="#D8D4CC", beard_c="#D8D4CC", beard_len=0.25, beard_w=0.8, brow_c="#B8B4AC", skin="#EACAAE", tunic="#ECE6D6", trim="#C9A25A",
              cloak="#B8923A", fur_collar="#ECE6D6", clasp="", armring=False, _head_extra=MITRE_H,
              _body_extra='<path d="M-40,-440 L0,-300 L40,-440" stroke="#1A1410" stroke-width="22" fill="none"/><path d="M-40,-440 L0,-300 L40,-440 M0,-300 L0,-160" stroke="#F2ECDE" stroke-width="13" fill="none"/>'
                          '<path d="M-10,-250 h20 M0,-262 v24" stroke="#1A1410" stroke-width="5"/>')   # pallium
PRIEST = lambda seed: dict(monk(seed), tunic="#2A2622", cloak="#1E1A18")
CROSS_P = ('<g transform="translate(0,-430)"><path d="M-34,-46 Q0,-6 34,-46" stroke="#5A4026" stroke-width="3" fill="none"/>'
           '<rect x="-6" y="-12" width="12" height="40" fill="#C8B070" stroke="#1A1410" stroke-width="3"/><rect x="-16" y="-2" width="32" height="10" fill="#C8B070" stroke="#1A1410" stroke-width="3"/></g>')   # Athelstan'ın haçı

def fig(c, spec, expr, x, y, sc, facing=1, look=None, rimc=None, rdx=-5, rdy=-3, ra=0.6, shx=None, sha=0.4, shc="#14202E", fs=0.9, shadow=0.45, phase=0.0):
    sp = full(spec, expr, fs, facing=facing, look=look)
    if shadow: soft_shadow(c, x, y - 6 * sc, 120 * sc, 16 * sc, shadow)
    with live(c, x, y, phase=phase):
        if rimc: rim(c, sp, x, y, sc, rimc, dx=rdx, dy=rdy, a=ra)
        draw(c, sp, x, y, sc)
        if shx: shade_side(c, sp, x, y, sha, shx[0], shx[1], shc)
    return sp

def lying(c, spec, expr, x, y, sc, deg=-90, look=0.0, fs=0.9):
    """Yatan figür: ayak tabanı çapası (x,y), tuval döndürülür (aynalama yok)."""
    sp = full(spec, expr, fs, facing=1, look=look)
    c.save(); c.translate(x, y); c.rotate(deg); draw(c, sp, 0, 0, sc); c.restore(); return sp

# ================================================================ ortak mekân yardımcıları
def stones(x0, y0, x1, y1, seed, pal=("#8A8274", "#7A7264", "#958C7C", "#6E675A", "#827A6A"), row=(16, 26), wd=(26, 60), ink="#2E2820", sw=1.6, a=1.0):
    """Taş derzleri: sıra sıra düzensiz bloklar."""
    r = R_(seed); o = []; y = y0
    while y < y1:
        h = r.uniform(*row); x = x0 - r.uniform(0, wd[1])
        while x < x1:
            w = r.uniform(*wd); o.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" rx="{min(w,h)*0.18:.1f}" fill="{r.choice(pal)}" stroke="{ink}" stroke-width="{sw}" opacity="{a}"/>'); x += w
        y += h
    return "".join(o)

def wall(x0, x1, yt, yb, seed, s=1.0, pal=None, lit="#F2D8A8", lita=0.18, merlons=True, slits=True, stain=True):
    """Düz sur: taş dokusu, mazgallar, mazgal deliği, yosun/islak lekeler, üst ışık kenarı."""
    pal = pal or ("#8A8274", "#7A7264", "#958C7C", "#6E675A", "#827A6A")
    cid = f"wl{seed}"; o = [f'<defs><clipPath id="{cid}"><rect x="{x0}" y="{yt}" width="{x1-x0}" height="{yb-yt}"/></clipPath></defs>',
                           f'<rect x="{x0}" y="{yt}" width="{x1-x0}" height="{yb-yt}" fill="{pal[0]}"/>', f'<g clip-path="url(#{cid})">']
    o.append(stones(x0, yt, x1, yb, seed, pal, (16 * s, 26 * s), (26 * s, 62 * s), sw=max(0.8, 1.8 * s)))
    o.append(f'<rect x="{x0}" y="{yt}" width="{x1-x0}" height="{yb-yt}" filter="url(#t_tas)" fill="#7A7264" opacity="0.35"/>')
    r = R_(seed + 1)
    if stain:
        for k in range(int((x1 - x0) / (90 * s)) + 1):   # yağmur izi / yosun (aşağı süzülen)
            x = r.uniform(x0, x1); o.append(f'<path d="M{x:.0f},{yt+8*s:.0f} q{r.uniform(-6,6)*s:.0f},{(yb-yt)*0.4:.0f} {r.uniform(-10,10)*s:.0f},{(yb-yt)*r.uniform(0.5,0.9):.0f}" stroke="#3A3A2A" stroke-width="{r.uniform(6,18)*s:.0f}" fill="none" opacity="0.22"/>')
        o.append(f'<rect x="{x0}" y="{yb-(yb-yt)*0.18:.0f}" width="{x1-x0}" height="{(yb-yt)*0.18:.0f}" fill="#3E4430" opacity="0.35"/>')
    if slits:
        for x in range(int(x0 + 60 * s), int(x1), int(140 * s)):
            yy = yt + (yb - yt) * 0.38; o.append(f'<rect x="{x}" y="{yy:.0f}" width="{8*s:.0f}" height="{34*s:.0f}" fill="#16120E"/>')
    o.append(f'<rect x="{x0}" y="{yt}" width="{x1-x0}" height="{6*s:.0f}" fill="{lit}" opacity="{lita}"/></g>')
    o.append(f'<rect x="{x0}" y="{yt}" width="{x1-x0}" height="{yb-yt}" fill="none" stroke="#1A1410" stroke-width="{max(1.5, 4*s):.1f}"/>')
    if merlons:
        mw = 30 * s; gap = 22 * s; x = x0
        while x < x1 - mw * 0.5:
            o.append(f'<rect x="{x:.0f}" y="{yt-26*s:.0f}" width="{mw:.0f}" height="{27*s:.0f}" fill="{pal[2]}" stroke="#1A1410" stroke-width="{max(1.2, 3*s):.1f}"/>'
                     f'<rect x="{x+mw*0.62:.0f}" y="{yt-26*s:.0f}" width="{mw*0.38:.0f}" height="{27*s:.0f}" fill="#000" opacity="0.2"/>'
                     f'<rect x="{x:.0f}" y="{yt-26*s:.0f}" width="{mw:.0f}" height="{4*s:.0f}" fill="{lit}" opacity="{lita*1.5:.2f}"/>')
            x += mw + gap
    return "".join(o)

_tid = [0]
def tower(cx, yb, w, h, s=1.0, roof="cone", seed=1, banner=None, lit="#F2D8A8", light=-1, rc="#4E5662"):
    """Yuvarlak kule: silindirik gölge, taş sıraları, mazgal, külah çatı (kayrak) ya da mazgallı taç; sancak."""
    _tid[0] += 1; gid = f"tw{_tid[0]}"; x0 = cx - w / 2; yt = yb - h
    st = [(0, "#B8AE9A"), (0.35, "#8E8676"), (1, "#4E4A42")] if light < 0 else [(0, "#4E4A42"), (0.65, "#8E8676"), (1, "#B8AE9A")]
    o = ['<defs>' + gradient(gid, st, x2=1, y2=0) + f'<clipPath id="c{gid}"><rect x="{x0}" y="{yt}" width="{w}" height="{h}"/></clipPath></defs>', f'<rect x="{x0}" y="{yt}" width="{w}" height="{h}" fill="url(#{gid})"/>', f'<g clip-path="url(#c{gid})">']
    r = R_(seed)
    for k, y in enumerate(range(int(yt + 8 * s), int(yb), max(4, int(18 * s)))):
        o.append(f'<path d="M{x0},{y} Q{cx},{y + 6*s:.0f} {x0+w},{y}" stroke="#2E2820" stroke-width="{max(0.8, 1.6*s):.1f}" fill="none" opacity="0.7"/>')
        for j in range(5):
            xx = x0 + w * (j + 0.5 * (k % 2)) / 5; o.append(f'<path d="M{xx:.0f},{y} v{18*s:.0f}" stroke="#2E2820" stroke-width="{max(0.6, 1.2*s):.1f}" opacity="0.5"/>')
    o.append(f'<rect x="{x0}" y="{yt}" width="{w}" height="{h}" filter="url(#t_tas)" fill="#7A7264" opacity="0.3"/>')
    for y in (yt + h * 0.3, yt + h * 0.62): o.append(f'<rect x="{cx - 4*s:.0f}" y="{y:.0f}" width="{8*s:.0f}" height="{30*s:.0f}" fill="#16120E"/>')
    o.append('</g>' + f'<rect x="{x0}" y="{yt}" width="{w}" height="{h}" fill="none" stroke="#1A1410" stroke-width="{max(1.2, 3.5*s):.1f}"/>')
    if roof == "cone":
        rh = w * 1.15; o.append(f'<path d="M{x0 - 8*s:.0f},{yt} L{cx},{yt - rh:.0f} L{x0 + w + 8*s:.0f},{yt} Z" fill="{rc}" stroke="#1A1410" stroke-width="{max(1.2, 3.5*s):.1f}"/>')
        for k in range(1, 6):
            yy = yt - rh * k / 6; ww = (w / 2 + 8 * s) * (1 - k / 6); o.append(f'<path d="M{cx-ww:.0f},{yy:.0f} Q{cx},{yy+5*s:.0f} {cx+ww:.0f},{yy:.0f}" stroke="#2A2E36" stroke-width="{max(0.8,1.6*s):.1f}" fill="none"/>')
        o.append(f'<path d="M{cx},{yt - rh:.0f} L{(x0 + w + 8*s) if light < 0 else (x0 - 8*s):.0f},{yt} L{cx},{yt} Z" fill="#000" opacity="0.28"/>')
        top = yt - rh
    else:
        o.append(wall(x0 - 6 * s, x0 + w + 6 * s, yt, yt + 12 * s, seed + 7, s * 0.9, slits=False, stain=False)); top = yt - 26 * s
    if banner:
        o.append(f'<path d="M{cx},{top} V{top - 60*s:.0f}" stroke="#1A1410" stroke-width="{max(1.5, 4*s):.1f}"/>'
                 f'<path d="M{cx},{top - 58*s:.0f} q{30*s:.0f},{-8*s:.0f} {60*s:.0f},{4*s:.0f} l{-10*s:.0f},{10*s:.0f} l{10*s:.0f},{10*s:.0f} q{-30*s:.0f},{-10*s:.0f} {-60*s:.0f},{2*s:.0f} Z" fill="{banner}" stroke="#1A1410" stroke-width="{max(1, 2.5*s):.1f}"/>'
                 f'<path d="M{cx + 18*s:.0f},{top - 52*s:.0f} v{12*s:.0f} M{cx + 12*s:.0f},{top - 46*s:.0f} h{12*s:.0f}" stroke="#E2B23A" stroke-width="{max(1, 3*s):.1f}"/>')
    return "".join(o)

def house(x, yb, w, h, seed, s=1.0, roofc=None, smoke=False):
    """Yarı ahşap şehir evi: badanalı dolgu, koyu kirişler, dik çatı, pencere."""
    r = R_(seed); roofc = roofc or r.choice(["#6A4A3A", "#5A4E46", "#4E5560", "#7A5440"]); wc = r.choice(["#CFC2A4", "#BDB094", "#D8CCB0", "#B4A88E"])
    rh = h * r.uniform(0.8, 1.1); sw = max(1, 3 * s)
    o = [f'<rect x="{x}" y="{yb-h:.0f}" width="{w}" height="{h}" fill="{wc}" stroke="#1A1410" stroke-width="{sw:.1f}"/>',
         f'<path d="M{x},{yb-h:.0f} L{x+w},{yb:.0f} M{x+w},{yb-h:.0f} L{x},{yb:.0f}" stroke="#3A2A1E" stroke-width="{sw*1.3:.1f}" opacity="0.8"/>' if r.random() < 0.5 else
         f'<path d="M{x+w*0.33:.0f},{yb-h:.0f} V{yb} M{x+w*0.66:.0f},{yb-h:.0f} V{yb} M{x},{yb-h*0.5:.0f} H{x+w}" stroke="#3A2A1E" stroke-width="{sw*1.3:.1f}"/>',
         f'<rect x="{x+w*0.4:.0f}" y="{yb-h*0.75:.0f}" width="{w*0.2:.0f}" height="{h*0.25:.0f}" fill="#2A2018"/>',
         f'<path d="M{x-w*0.08:.0f},{yb-h:.0f} L{x+w*0.5:.0f},{yb-h-rh:.0f} L{x+w*1.08:.0f},{yb-h:.0f} Z" fill="{roofc}" stroke="#1A1410" stroke-width="{sw:.1f}"/>',
         f'<path d="M{x+w*0.5:.0f},{yb-h-rh:.0f} L{x+w*1.08:.0f},{yb-h:.0f} L{x+w*0.5:.0f},{yb-h:.0f} Z" fill="#000" opacity="0.22"/>',
         f'<rect x="{x+w*0.62:.0f}" y="{yb-h:.0f}" width="{w*0.38:.0f}" height="{h}" fill="#000" opacity="0.14"/>']
    for k in range(1, 4): o.append(f'<path d="M{x+w*0.5-w*0.58*k/4:.0f},{yb-h-rh+rh*k/4:.0f} H{x+w*0.5+w*0.58*k/4:.0f}" stroke="#000" stroke-width="{sw*0.6:.1f}" opacity="0.3"/>')
    if smoke: o.append(f'<path d="M{x+w*0.7:.0f},{yb-h-rh*0.6:.0f} q{-14*s:.0f},{-40*s:.0f} {6*s:.0f},{-70*s:.0f} q{18*s:.0f},{-30*s:.0f} {-4*s:.0f},{-70*s:.0f}" stroke="#C8C8C4" stroke-width="{14*s:.0f}" fill="none" opacity="0.4" stroke-linecap="round"/>')
    return "".join(o)

def basilica(x, yb, s=1.0):
    """Ada kilisesi (Saint-Étienne benzeri): uzun nef, kemerli pencereler, iki batı kulesi, merkez çan kulesi + haç."""
    o = [f'<g transform="translate({x},{yb}) scale({s})">']
    o.append(f'<rect x="-260" y="-150" width="460" height="150" fill="#B4AA96"/>' + stones(-260, -150, 200, 0, 901, ("#B4AA96", "#A89E8A", "#C0B6A2"), (18, 22), (30, 60), sw=1.2)
             + '<rect x="-260" y="-150" width="460" height="150" fill="none" stroke="#1A1410" stroke-width="4"/>')
    for xx in range(-230, 190, 56): o.append(f'<path d="M{xx},-40 V-96 Q{xx+14},-116 {xx+28},-96 V-40 Z" fill="#2A2830" stroke="#1A1410" stroke-width="3"/><path d="M{xx+14},-40 V-104" stroke="#6A6A72" stroke-width="2"/>')
    o.append('<path d="M-276,-146 L-40,-250 L216,-146 Z" fill="#4E5662" stroke="#1A1410" stroke-width="4"/><path d="M-40,-250 L216,-146 L60,-146 Z" fill="#000" opacity="0.25"/>')
    for k in range(1, 6): o.append(f'<path d="M{-40-236*k/6:.0f},{-250+104*k/6:.0f} H{-40+256*k/6:.0f}" stroke="#2E343C" stroke-width="2"/>')
    o.append('<path d="M200,-150 L200,0 L300,0 L300,-120 Q250,-160 200,-150 Z" fill="#9E9482" stroke="#1A1410" stroke-width="4"/>')   # apsis
    for tx in (-330, -250):   # batı kuleleri
        o.append(tower(tx + 40, 0, 80, 300, 1.0, "cone", seed=tx + 999, banner=None, rc="#4E5662"))
    o.append(tower(-40, -150, 70, 190, 1.0, "cone", seed=777, rc="#4E5662"))
    o.append('<path d="M-40,-460 V-530 M-62,-506 H-18" stroke="#1A1410" stroke-width="12"/><path d="M-40,-460 V-530 M-62,-506 H-18" stroke="#E2C060" stroke-width="6"/>')
    o.append('<path d="M-300,0 Q-280,-60 -290,-140" stroke="#000" stroke-width="0"/></g>')
    return "".join(o)

def river(y0, y1, seed, top="#9AA6AE", mid="#5E7280", bot="#24343E", glint=None, gcol="#FFF0D4", n=110, lineD="#1E2C36", lineL="#C8D2D8"):
    r = R_(seed); gid = f"rv{seed}"; o = ['<defs>' + gradient(gid, [(0, top), (0.3, mid), (1, bot)]) + '</defs>', f'<rect y="{y0}" width="1920" height="{y1-y0}" fill="url(#{gid})"/>']
    D = y1 - y0
    for k in range(n):
        y = y0 + 4 + (k / n) ** 1.7 * D; x = r.uniform(-150, 1900); q = (y - y0) / D; w_ = 30 + q * 500; sw = 1 + q * 6
        o.append(f'<path d="M{x:.0f},{y:.0f} q{w_*0.25:.0f},-{2+q*14:.1f} {w_*0.5:.0f},0 q{w_*0.25:.0f},{1+q*10:.1f} {w_*0.5:.0f},0" stroke="{lineD}" stroke-width="{sw:.1f}" fill="none" opacity="0.5"/>'
                 f'<path d="M{x+w_*0.1:.0f},{y-2-q*10:.0f} q{w_*0.2:.0f},-{1+q*8:.1f} {w_*0.4:.0f},0" stroke="{lineL}" stroke-width="{sw*0.7:.1f}" fill="none" opacity="0.38"/>')
    if glint is not None:
        for k in range(120):
            y = y0 + 4 + (k / 120) ** 1.4 * D * 0.9; q = (y - y0) / D; x = glint + r.gauss(0, 16 + q * 260); w_ = r.uniform(8, 22) + q * 50
            o.append(f'<path d="M{x-w_/2:.0f},{y:.0f} h{w_:.0f}" stroke="{gcol}" stroke-width="{1.5+q*5:.1f}" stroke-linecap="round" opacity="{r.uniform(0.3, 0.85):.2f}"/>')
    return "".join(o)

def willow(x, yb, h, seed, s=1.0, col="#3E4A2E", lit="#7A8A52"):
    """Söğüt: eğri gövde, sarkan dal perdeleri (çizgi + yaprak lekeleri)."""
    r = R_(seed); o = [f'<path d="M{x-14*s:.0f},{yb} Q{x-24*s:.0f},{yb-h*0.4:.0f} {x+6*s:.0f},{yb-h*0.7:.0f} L{x+22*s:.0f},{yb-h*0.68:.0f} Q{x+4*s:.0f},{yb-h*0.4:.0f} {x+16*s:.0f},{yb} Z" fill="#3A2E24" stroke="#1A1410" stroke-width="{3*s:.1f}"/>']
    for k in range(int(70 * min(1.6, s + 0.4))):
        a = r.uniform(-1.2, 1.2); sx = x + 10 * s + math.sin(a) * h * 0.55; sy = yb - h * 0.72 - math.cos(a) * h * 0.3 + r.uniform(-10, 10) * s; L = h * r.uniform(0.35, 0.8)
        o.append(f'<path d="M{sx:.0f},{sy:.0f} q{r.uniform(-8,8)*s:.0f},{L*0.5:.0f} {r.uniform(-14,14)*s:.0f},{L:.0f}" stroke="{r.choice([col, lit, "#56663A"])}" stroke-width="{r.uniform(3,7)*s:.1f}" fill="none" stroke-linecap="round" opacity="0.9"/>')
    return "".join(o)

def arrows(seed, n, box, ang, L=(60, 110), col="#2A1E14", fl="#D8CCB0", a=0.9, sw=3):
    r = R_(seed); o = []; ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    for _ in range(n):
        x, y = r.uniform(box[0], box[2]), r.uniform(box[1], box[3]); l = r.uniform(*L)
        o.append(f'<g opacity="{a}"><path d="M{x:.0f},{y:.0f} l{l*ca:.0f},{l*sa:.0f}" stroke="{col}" stroke-width="{sw}"/><path d="M{x+l*ca:.0f},{y+l*sa:.0f} l{-10*ca+4*sa:.0f},{-10*sa-4*ca:.0f} M{x+l*ca:.0f},{y+l*sa:.0f} l{-10*ca-4*sa:.0f},{-10*sa+4*ca:.0f}" stroke="#9AA2AA" stroke-width="{sw}"/>'
                 f'<path d="M{x:.0f},{y:.0f} l{-6*sa+8*ca:.0f},{6*ca+8*sa:.0f} M{x:.0f},{y:.0f} l{6*sa+8*ca:.0f},{-6*ca+8*sa:.0f}" stroke="{fl}" stroke-width="{sw}"/></g>')
    return "".join(o)

def tent_bg(seed=5, flap=True, warm=True):
    """Deri çadır iç cephesi: dikişli panolar, sarkık kumaş, direkler, asılı otlar; sağda kapı aralığı (soğuk gün ışığı)."""
    r = R_(seed); o = [TEXD, '<defs>' + gradient("tb", [(0, "#2A1C12"), (0.6, "#4A3420"), (1, "#2A1C12")]) + '</defs>', '<rect width="1920" height="1080" fill="url(#tb)"/>']
    for k in range(9):   # panolar
        x = -80 + k * 250; o.append(f'<path d="M{x},0 Q{x+125},{60 + r.uniform(-10,10):.0f} {x+250},0 L{x+250},860 L{x},860 Z" fill="{r.choice(["#5A4028", "#4E3822", "#62462C"])}" filter="url(#t_deri)"/>'
                                     f'<path d="M{x},0 V860" stroke="#1E140C" stroke-width="7"/><path d="M{x+6},0 V860" stroke="#8A6A46" stroke-width="2" stroke-dasharray="10 8" opacity="0.6"/>'
                                     f'<path d="M{x+20},40 Q{x+125},{100:.0f} {x+230},40" stroke="#1E140C" stroke-width="4" fill="none" opacity="0.5"/>')
    if flap:
        o.append('<path d="M1500,0 L1500,860 L1700,860 Q1640,420 1660,0 Z" fill="#A8B8C8" opacity="0.9"/><path d="M1540,860 L1690,860 L1660,500 Z" fill="#C8D4DE" opacity="0.6"/>'
                 '<path d="M1500,0 Q1560,400 1540,860 L1480,860 Q1500,420 1460,0 Z" fill="#3A2818" stroke="#1A1410" stroke-width="6" filter="url(#t_deri)"/>')
    for x in (300, 1200):   # direkler
        o.append(f'<rect x="{x-18}" y="0" width="36" height="880" fill="#3A2818" filter="url(#t_ahsap)"/><rect x="{x-18}" y="0" width="36" height="880" fill="none" stroke="#120A06" stroke-width="5"/>')
    for k, x in enumerate((420, 470, 900, 960, 1010)):   # asılı kuru ot demetleri
        o.append(f'<path d="M{x},120 V170" stroke="#1A1410" stroke-width="3"/><path d="M{x-14},170 Q{x},250 {x+14},170 Z" fill="{["#6A7448", "#7A6A3A", "#5A6A3A"][k%3]}" stroke="#1A1410" stroke-width="3"/>'
                 + "".join(f'<path d="M{x},176 l{j*5-10},{50 + j%2*14}" stroke="#4A5230" stroke-width="2"/>' for j in range(5)))
    o.append('<rect y="840" width="1920" height="240" fill="#2A1E14"/>' + "".join(f'<path d="M{r.uniform(0,1920):.0f},{r.uniform(850,1080):.0f} l{r.uniform(-14,14):.0f},{r.uniform(-4,4):.0f}" stroke="#8A7048" stroke-width="2.5" opacity="0.6"/>' for _ in range(220)))
    return "".join(o)

def fur_pile(x, y, w, h, seed, col="#6A5038", dark="#3A2A1C", lit="#A88A62"):
    r = R_(seed); pts = [(x + w / 2 * math.cos(a) * r.uniform(0.85, 1.1), y + h / 2 * math.sin(a) * r.uniform(0.8, 1.15)) for a in [i * math.pi / 9 for i in range(18)]]
    d = "M" + " L".join(f"{px:.0f},{py:.0f}" for px, py in pts) + " Z"
    o = [f'<path d="{d}" fill="{col}" filter="url(#t_kurk)"/><path d="{d}" fill="none" stroke="#120A06" stroke-width="5"/>']
    for k in range(int(w / 6)):
        px = x + r.uniform(-w / 2, w / 2) * 0.95; py = y + r.uniform(-h / 2, h / 2) * 0.8; o.append(f'<path d="M{px:.0f},{py:.0f} q{r.uniform(-4,4):.0f},10 {r.uniform(-8,8):.0f},18" stroke="{r.choice([dark, lit])}" stroke-width="2.5" fill="none" opacity="0.7"/>')
    return "".join(o)

def smoke(c, seed, n, box, colr="#4A4440", a=0.25, blur=16, rx=(80, 200), ry=(40, 100)):
    draw(c, blurred(place(cloud_band(seed, n, box[0], box[2], box[1], box[3], colr, colr, a, rx=rx, ry=ry)), blur), 0, 0, 1.0)

def embers(c, seed, n, box, colr="#FFC070"):
    r = R_(seed)
    for _ in range(n): c.drawCircle(r.uniform(box[0], box[2]), r.uniform(box[1], box[3]), r.uniform(1.5, 4), skia.Paint(AntiAlias=True, Color4f=col(colr, r.uniform(0.4, 0.95))))

def fleet_svg(items, sail=True):
    """items: (x, y, s, billow) arkadan öne sıralı. Uzaktaki gemiler soluk."""
    return "".join(f'<g transform="translate({x},{y}) scale({s})">{G.mast_sail(b) if sail else ""}{G.hull(1.0, shields=True, oars=True)}</g>' for x, y, s, b in sorted(items, key=lambda q: q[1]))

def mini_men(c, specs_xy, sc):
    for sp, x, y, f_ in specs_xy: draw(c, full(sp, "neutral", 0.9, facing=f_), x, y, sc)

def bridge(x0, y0, x1, y1, th0, th1, n, seed, houses=True):
    """Taş köprü: tabla + kemer ayakları (perspektifte incelir), üstünde küçük evler."""
    o = [f'<path d="M{x0},{y0} L{x1},{y1} L{x1},{y1+th1} L{x0},{y0+th0} Z" fill="#8A8274" stroke="#1A1410" stroke-width="2.5"/>']
    for k in range(n):
        q0, q1 = k / n, (k + 1) / n; ax0 = x0 + (x1 - x0) * (q0 + 0.12 / n); ax1 = x0 + (x1 - x0) * (q1 - 0.12 / n)
        ay = y0 + (y1 - y0) * (q0 + q1) / 2; th = th0 + (th1 - th0) * (q0 + q1) / 2
        o.append(f'<path d="M{ax0:.0f},{ay+th*2.2:.0f} L{ax0:.0f},{ay+th*0.9:.0f} Q{(ax0+ax1)/2:.0f},{ay+th*0.2:.0f} {ax1:.0f},{ay+th*0.9:.0f} L{ax1:.0f},{ay+th*2.2:.0f} Z" fill="#2A2A2C" opacity="0.85"/>')
        o.append(f'<path d="M{ax1:.0f},{ay+th*0.9:.0f} L{ax1+(x1-x0)*0.24/n:.0f},{ay+th*0.9:.0f} L{ax1+(x1-x0)*0.24/n:.0f},{ay+th*2.4:.0f} L{ax1:.0f},{ay+th*2.4:.0f} Z" fill="#6E675A" stroke="#1A1410" stroke-width="1.5"/>')
    o.append(f'<path d="M{x0},{y0} L{x1},{y1}" stroke="#C8BCA0" stroke-width="2" opacity="0.7"/>')
    if houses:
        r = R_(seed)
        for k in range(n * 2):
            q = (k + 0.5) / (n * 2); hx = x0 + (x1 - x0) * q; hy = y0 + (y1 - y0) * q; th = th0 + (th1 - th0) * q
            o.append(house(hx - th * 0.9, hy, th * 1.8, th * 1.4, seed * 10 + k, s=th / 30))
    return "".join(o)

def ladder(x0, y0, x1, y1, w, sw=6, col="#6A4C30", rungs=None):
    L = math.hypot(x1 - x0, y1 - y0); nx, ny = -(y1 - y0) / L * w / 2, (x1 - x0) / L * w / 2; n = rungs or int(L / (w * 0.9))
    o = []
    for k in range(1, n):
        q = k / n; px, py = x0 + (x1 - x0) * q, y0 + (y1 - y0) * q
        o.append(f'<path d="M{px+nx:.0f},{py+ny:.0f} L{px-nx:.0f},{py-ny:.0f}" stroke="#1A1410" stroke-width="{sw+4}"/><path d="M{px+nx:.0f},{py+ny:.0f} L{px-nx:.0f},{py-ny:.0f}" stroke="{col}" stroke-width="{sw}"/>')
    for sgn in (1, -1):
        o.append(f'<path d="M{x0+sgn*nx:.0f},{y0+sgn*ny:.0f} L{x1+sgn*nx:.0f},{y1+sgn*ny:.0f}" stroke="#1A1410" stroke-width="{sw*1.6+5:.0f}" stroke-linecap="round"/><path d="M{x0+sgn*nx:.0f},{y0+sgn*ny:.0f} L{x1+sgn*nx:.0f},{y1+sgn*ny:.0f}" stroke="{col}" stroke-width="{sw*1.6:.0f}" stroke-linecap="round"/>')
    return "".join(o)

def boulder(x, y, r_, seed, col="#7A7264"):
    r = R_(seed); pts = [(x + r_ * math.cos(a) * r.uniform(0.75, 1.1), y + r_ * 0.8 * math.sin(a) * r.uniform(0.75, 1.1)) for a in [i * math.pi / 5 for i in range(10)]]
    d = "M" + " L".join(f"{px:.0f},{py:.0f}" for px, py in pts) + " Z"
    return (f'<ellipse cx="{x}" cy="{y + r_*0.75:.0f}" rx="{r_*1.1:.0f}" ry="{r_*0.22:.0f}" fill="#000" opacity="0.4"/><path d="{d}" fill="{col}" stroke="#1A1410" stroke-width="{max(2, r_*0.08):.1f}" stroke-linejoin="round"/>'
            f'<path d="M{x - r_*0.6:.0f},{y - r_*0.3:.0f} Q{x:.0f},{y - r_*0.85:.0f} {x + r_*0.5:.0f},{y - r_*0.5:.0f}" stroke="#D8CCB4" stroke-width="{max(1.5, r_*0.08):.1f}" fill="none" opacity="0.6"/>'
            f'<path d="M{x + r_*0.1:.0f},{y + r_*0.1:.0f} L{x + r_*0.9:.0f},{y + r_*0.3:.0f} L{x + r_*0.5:.0f},{y + r_*0.75:.0f} Z" fill="#000" opacity="0.25"/>')

def broken_shield(x, y, s, c1, c2, rot=0, half=True):
    clip = f'<clipPath id="bs{int(x)}{int(y)}"><path d="M-80,-80 L40,-80 L10,-20 L30,20 L-10,80 L-80,80 Z"/></clipPath>' if half else ""
    return (f'<g transform="translate({x},{y}) rotate({rot}) scale({s},{s*0.45})"><defs>{clip}</defs><g {"clip-path=" + chr(34) + "url(#bs" + str(int(x)) + str(int(y)) + ")" + chr(34) if half else ""}>'
            f'<circle r="70" fill="{c1}" stroke="#1A1410" stroke-width="7"/><path d="M0,-70 L0,70 M-70,0 L70,0" stroke="{c2}" stroke-width="16"/><circle r="70" fill="none" stroke="#5A5A58" stroke-width="7"/><circle r="15" fill="#8A8A86" stroke="#1A1410" stroke-width="4"/></g>'
            + (f'<path d="M40,-80 L10,-20 L30,20 L-10,80" stroke="#E8D8B0" stroke-width="5" fill="none"/>' if half else "") + '</g>')

def axe_svg(x, y, rot, s=1.0):
    return (f'<g transform="translate({x},{y}) rotate({rot}) scale({s})"><path d="M0,0 L0,-300" stroke="#1A1410" stroke-width="20" stroke-linecap="round"/><path d="M0,0 L0,-300" stroke="#7A5A3A" stroke-width="11" stroke-linecap="round"/>'
            '<path d="M0,-150 l-10,0 M0,-120 l-10,0" stroke="#3A2A1A" stroke-width="4"/>'
            '<path d="M4,-290 Q60,-300 96,-330 Q110,-270 96,-200 Q60,-230 4,-236 Z" fill="#AEB6BE" stroke="#1A1410" stroke-width="6" stroke-linejoin="round"/>'
            '<path d="M92,-322 Q104,-268 92,-208" stroke="#F2F6FA" stroke-width="4" fill="none"/><path d="M20,-282 Q50,-276 70,-262" stroke="#6E767E" stroke-width="4" fill="none"/></g>')

# ================================================================ p15b · Seine'de ada, sabah sisi, filo
def p15b():
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    sky = ['<defs>' + gradient("s15", [(0, "#56647A"), (0.45, "#98A2AC"), (0.8, "#DCCCB0"), (1, "#F0D8B0")]) + '</defs>', '<rect width="1920" height="580" fill="url(#s15)"/>']
    draw(c, svg_sprite("".join(sky)), 0, 0, 1.0)
    glow(c, 1640, 430, 560, "#FFD8A0", 0.38); glow(c, 1640, 430, 110, "#FFF4DC", 0.7)
    draw(c, blurred(svg_sprite(cloud_band(151, 13, -100, 2000, 90, 250, "#66728A", "#EAD2B4", 0.8, lit_dy=9, rx=(220, 460), ry=(20, 46))
                               + cloud_band(152, 9, -100, 2000, 270, 390, "#A4AAB6", "#F4DEC2", 0.55, lit_dy=6, rx=(160, 360), ry=(10, 24))), 5), 0, 0, 1.0)
    rays(c, 1640, 430, 165, 1300, 40, 9, "#FFE8C0", 0.07, t or 0.0)
    r = R_(150); o = [TEXD]
    o.append('<path d="M0,510 Q260,470 520,490 Q820,455 1120,488 Q1420,462 1920,492 L1920,560 L0,560 Z" fill="#8E949C"/>')   # uzak tepeler
    for k in range(150):   # uzak kıyı ağaçları
        x = r.uniform(-20, 1940); y = 528 + r.uniform(-8, 14); w_ = r.uniform(14, 34)
        o.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{w_:.0f}" ry="{w_*0.8:.0f}" fill="{r.choice(["#6E7880", "#78828A", "#646E76"])}"/>')
    o.append('<path d="M0,546 H1920 V562 H0 Z" fill="#7A8288"/>')
    o.append(river(556, 1080, 15, top="#C8C4B6", mid="#7A8A94", bot="#2A3A44", glint=1640, gcol="#FFE8C0", n=120))
    # ada: arka sur, evler, kilise, ön sur + kuleler
    o.append('<path d="M640,650 Q700,560 900,548 L1500,546 Q1680,556 1720,650 Z" fill="#6E6A5A"/>')
    o.append(wall(700, 1660, 540, 566, 153, s=0.42, pal=("#9A9282", "#8E8676", "#A49C8C", "#847C6C", "#968E7E")))
    for k in range(34):   # çatılar (arkadan öne)
        x = 700 + (k * 97) % 940 + r.uniform(-10, 10); yb = 590 + (k // 10) * 16
        o.append(house(x, yb, r.uniform(34, 56), r.uniform(26, 36), 1500 + k, s=0.4, smoke=(k % 7 == 3)))
    o.append(basilica(1120, 600, 0.55))
    o.append(tower(905, 600, 40, 150, 0.45, "cone", seed=21, banner="#2E4478"))   # ikinci çan kulesi
    o.append(wall(660, 1680, 606, 664, 154, s=0.55, lit="#FFE0B0", lita=0.3))
    for k, x in enumerate(range(660, 1700, 150)):
        o.append(tower(x, 668, 50, 104 + (k % 2) * 16, 0.55, "cone", seed=30 + k, banner=("#2E4478" if k % 2 else "#8E1E22"), lit="#FFE0B0", light=1))
    o.append('<path d="M640,668 H1720 L1700,684 H660 Z" fill="#4E4A3E"/>')
    for k in range(40):   # suya yansıma
        x = r.uniform(650, 1700); y = r.uniform(684, 760); o.append(f'<path d="M{x:.0f},{y:.0f} h{r.uniform(20,70):.0f}" stroke="{r.choice(["#8E8676", "#6E6A5E", "#B0A890"])}" stroke-width="{r.uniform(2,4):.1f}" opacity="0.45"/>')
    o.append(bridge(640, 640, 250, 556, 26, 12, 5, 7))   # Büyük Köprü → kuzey kıyı
    o.append(tower(240, 566, 60, 110, 0.5, "crenel", seed=40, banner="#2E4478"))
    o.append(bridge(1700, 640, 1940, 590, 26, 18, 3, 8))
    draw(c, svg_sprite("".join(o)), 0, 0, 1.0)
    # sur üstünde minik muhafızlar
    for k, x in enumerate(range(700, 1660, 46)): draw(c, full(frank(k, shield=False), "neutral", 0.9, facing=(-1) ** k), x, 616, 0.042)
    draw(c, svg_sprite(wall(660, 1680, 606, 664, 154, s=0.55, lit="#FFE0B0", lita=0.3, slits=False).split('<rect x="660" y="606" width="1020" height="58" fill="none"')[0].replace('<g clip-path', '<g opacity="0" clip-path')), 0, 0, 1.0) if False else None
    glow(c, 1500, 560, 300, "#FFD8A8", 0.12)
    # sabah sisi (nehir üstü), filo
    draw(c, blurred(svg_sprite(cloud_band(155, 16, -100, 2000, 600, 700, "#E4E2DC", "#F6EADA", 0.38, rx=(240, 520), ry=(16, 34))), 9), 0, 0, 1.0)
    far = [(150, 690, 0.08, 1), (420, 700, 0.10, 1), (700, 712, 0.09, 1), (960, 724, 0.10, 0.9), (290, 742, 0.12, 1), (560, 760, 0.14, 1), (860, 790, 0.16, 0.9)]
    fl = blurred(svg_sprite(fleet_svg(far)), 1.0); draw(c, fl, 0, 0, 1.0); draw(c, tinted(fl, "#C8CCCE"), 0, 0, 1.0, a=0.35)
    near = [(140, 840, 0.22, 1), (520, 880, 0.26, 1.0), (240, 1020, 0.40, 1.1), (860, 960, 0.30, 0.9)]
    draw(c, svg_sprite(fleet_svg(near)), 0, 0, 1.0)
    for x, y, w_ in ((240, 1020, 230), (520, 880, 150), (860, 960, 175), (140, 840, 125)):   # pruva köpüğü + iz
        rr = R_(x)
        for k in range(14): c.drawLine(x - w_ - rr.uniform(0, 160), y + rr.uniform(-6, 18), x - w_ - rr.uniform(0, 160) + rr.uniform(20, 60), y + rr.uniform(-6, 18), skia.Paint(AntiAlias=True, StrokeWidth=2.5, Color4f=col("#E8EEF0", rr.uniform(0.3, 0.7))))
    draw(c, blurred(svg_sprite(cloud_band(156, 8, -100, 1300, 760, 860, "#E8E6E0", "#F6EADA", 0.22, rx=(200, 420), ry=(12, 26))), 10), 0, 0, 1.0)
    # sağ ön kıyı: kamp (çadır, ateş, kalkanlar, sazlık)
    k_ = [TEXD, '<path d="M1180,1080 Q1300,960 1480,930 Q1700,900 1920,890 L1920,1080 Z" fill="#3E3A2C" filter="url(#t_tas)"/><path d="M1180,1080 Q1300,960 1480,930 Q1700,900 1920,890" stroke="#1A1410" stroke-width="5" fill="none"/>',
          '<path d="M1200,1060 Q1310,968 1480,940 Q1700,910 1920,900" stroke="#9AA090" stroke-width="3" fill="none" opacity="0.5"/>']
    for x, y, w_ in ((1560, 930, 170), (1780, 916, 150)):   # deri çadırlar
        k_.append(f'<path d="M{x-w_/2},{y} L{x},{y-w_*0.75:.0f} L{x+w_/2},{y} Z" fill="#7A5E40" stroke="#1A1410" stroke-width="5" filter="url(#t_deri)"/><path d="M{x-w_/2},{y} L{x},{y-w_*0.75:.0f} L{x+w_/2},{y} Z" fill="none" stroke="#1A1410" stroke-width="5"/>'
                  f'<path d="M{x},{y-w_*0.75:.0f} L{x+w_/2},{y} L{x},{y} Z" fill="#000" opacity="0.3"/><path d="M{x-14},{y} L{x},{y-w_*0.4:.0f} L{x+14},{y} Z" fill="#1E140C"/><path d="M{x},{y-w_*0.75:.0f} l-14,-20 M{x},{y-w_*0.75:.0f} l14,-20" stroke="#4A3420" stroke-width="5"/>')
    for k, (x, c1, c2) in enumerate(((1420, "#8E3B2E", "#D8C8A0"), (1480, "#2F4C6E", "#D8C8A0"), (1690, "#5A6A3A", "#C9A25A"))):
        k_.append(f'<g transform="translate({x},{948 - k*4}) rotate({(-1)**k*10}) scale(0.4)"><circle r="70" fill="{c1}" stroke="#1A1410" stroke-width="8"/><path d="M0,-70 L0,70 M-70,0 L70,0" stroke="{c2}" stroke-width="16"/><circle r="15" fill="#8A8A86" stroke="#1A1410" stroke-width="4"/></g>')
    k_.append('<g transform="translate(1660,990)"><ellipse rx="60" ry="12" fill="#1A1410"/>' + "".join(f'<path d="M{x},-2 l{(x%3-1)*6},-26" stroke="#3A2A1A" stroke-width="7"/>' for x in range(-40, 44, 14)) + '</g>')
    for k in range(60): x = 1180 + k * 13 + R_(k).uniform(-6, 6); y = 1080 - max(0, (x - 1180)) * 0.0 - 4; k_.append(f'<path d="M{x:.0f},{1085} q{R_(k).uniform(-10,10):.0f},-60 {R_(k).uniform(-20,20):.0f},-{R_(k).uniform(60,140):.0f}" stroke="{["#4A4A2A", "#6A6A3A", "#3A3A22"][k%3]}" stroke-width="5" fill="none"/>' if x < 1500 else "")
    draw(c, svg_sprite("".join(k_)), 0, 0, 1.0)
    flames(c, 1625, 1695, 986, 70, t, seed=15); glow(c, 1660, 960, 220, "#FF8A3A", 0.30)
    smoke(c, 157, 6, (1560, 520, 1760, 930), "#C8C4BC", 0.25, 14, rx=(40, 90), ry=(60, 140))
    for k, (x, f_) in enumerate(((1600, 1), (1730, -1))):
        fig(c, KL.soldier_spec(160 + k, "ragnar"), "neutral", x, 1000, 0.26, facing=f_, rimc="#FFB070", rdx=6 * -f_, ra=0.7, shadow=0.3)
    # kuşlar (kargalar, şehrin üstünde)
    draw(c, svg_sprite("".join(gull(x, y, s_, f_, col_="#2E2E34", dark="#141418", rot=r_) for x, y, s_, f_, r_ in ((980, 260, 0.30, 0.3, -6), (1060, 230, 0.24, 1.0, 4), (1240, 280, 0.2, 0.5, 0), (1330, 240, 0.18, 0.8, -8), (820, 300, 0.16, 0.1, 6)))), 0, 0, 1.0)
    # sol üst: sarkan söğüt dalları (ön plan çerçeve)
    wl = "".join(f'<path d="M{x},-20 q{(k%3-1)*14},{160+k%5*40} {(k%4-2)*20},{300+k%6*60}" stroke="{["#2E3A22", "#3E4A2C", "#24301C"][k%3]}" stroke-width="{6+k%4*2}" fill="none" stroke-linecap="round"/>' for k, x in enumerate(range(-20, 520, 16)) if x < 380 or k % 3 == 0)
    draw(c, blurred(svg_sprite(wl), 6), 0, 0, 1.0)
    card_at(c, "PARİS", 560, 150, "Seine nehrinde bir ada")
    finish(c, cold=True, warm=0.10); return s

# ================================================================ p15c · ilk saldırı: sur dibi, kaynar yağ, oklar
def p15c():
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    draw(c, svg_sprite('<defs>' + gradient("s15c", [(0, "#3A3634"), (0.5, "#7A6A58"), (1, "#B8946A")]) + '</defs><rect width="1920" height="1080" fill="url(#s15c)"/>'), 0, 0, 1.0)
    smoke(c, 1531, 14, (-100, 60, 1100, 500), "#2A2624", 0.55, 18, rx=(160, 340), ry=(60, 140))
    glow(c, 300, 300, 500, "#FFB060", 0.15)
    # uzak kale silueti (sol, sis arkasında)
    o = [TEXD, tower(180, 760, 110, 380, 0.9, "cone", seed=51, banner="#2E4478"), wall(230, 560, 520, 780, 152, s=0.8), tower(520, 780, 120, 330, 0.9, "crenel", seed=52)]
    fs_ = blurred(svg_sprite("".join(o)), 3); draw(c, fs_, 0, 0, 1.0); draw(c, tinted(fs_, "#8A7A66"), 0, 0, 1.0, a=0.55)
    # büyük sur: alt açı, sağa doğru yükselen üst kenar
    defenders = [(980, 190), (1120, 176), (1420, 150), (1560, 140), (1740, 124)]
    for k, (x, y) in enumerate(defenders):
        fig(c, frank(60 + k, shield=False, arm=(k % 2 == 0)), "angry", x, y + 120, 0.30, facing=-1, look=-0.5, shadow=0)
    W_ = [TEXD, '<g transform="matrix(1,-0.085,0,1,0,70)">', wall(700, 1960, 220, 1000, 155, s=1.5, lit="#FFC890", lita=0.3), '</g>']
    W_.append(tower(760, 1010, 230, 760, 1.5, "crenel", seed=53, lit="#FFC890", light=-1))
    draw(c, svg_sprite("".join(W_)), 0, 0, 1.0)
    # kaynar yağ: devrilen kazan + duvardan akan turuncu sel + buhar
    oil = ('<g transform="translate(1280,140) rotate(-35)"><path d="M-60,-10 Q-70,60 0,70 Q70,60 60,-10 Z" fill="#2A2420" stroke="#1A1410" stroke-width="7"/><ellipse cx="0" cy="-10" rx="62" ry="16" fill="#3A302A" stroke="#1A1410" stroke-width="6"/><path d="M-30,30 Q0,40 30,30" stroke="#6A5E54" stroke-width="4" fill="none"/></g>'
           '<path d="M1300,150 Q1330,230 1300,330 Q1280,460 1310,600 Q1330,760 1290,900 L1250,900 Q1290,760 1270,600 Q1250,460 1270,330 Q1290,230 1262,160 Z" fill="#E87A1E" opacity="0.92"/>'
           '<path d="M1290,170 Q1310,240 1288,330 Q1272,460 1296,600 Q1312,760 1278,890" stroke="#FFD27A" stroke-width="7" fill="none"/>')
    draw(c, svg_sprite(oil), 0, 0, 1.0); glow(c, 1290, 520, 260, "#FF8A2A", 0.35); glow(c, 1280, 900, 240, "#FFA040", 0.45)
    smoke(c, 1532, 10, (1150, 300, 1450, 980), "#E8C8A0", 0.35, 14, rx=(40, 110), ry=(40, 90))
    # merdivenler: biri surda (tırmanan), biri geriye devriliyor
    draw(c, svg_sprite(ladder(1020, 1000, 1090, 200, 70, 7)), 0, 0, 1.0)
    for k, (y, sc) in enumerate(((700, 0.36), (520, 0.32))):
        fig(c, dict(KL.soldier_spec(170 + k, "ragnar"), _arm_up=True, _hand_extra=""), "fierce", 1030 + (1000 - y) * 0.05, y, sc, rimc="#FFB070", rdx=5, shadow=0)
    draw(c, svg_sprite(ladder(860, 1010, 520, 250, 66, 7)), 0, 0, 1.0)
    fall = full(dict(KL.soldier_spec(175, "ragnar"), _arm_up=True, _hand_extra=""), "shock", 0.9)
    c.save(); c.translate(620, 420); c.rotate(-58); draw(c, fall, 0, 0, 0.32); c.restore()
    draw(c, svg_sprite('<path d="M560,250 Q470,300 430,400" stroke="#F2E6D0" stroke-width="5" fill="none" opacity="0.5" stroke-dasharray="20 14"/><path d="M600,220 Q480,250 420,340" stroke="#F2E6D0" stroke-width="3" fill="none" opacity="0.35" stroke-dasharray="14 12"/>'), 0, 0, 1.0)
    # zemin: çamur, düşen taşlar, kırık kalkanlar, saplanmış oklar
    g = [TEXD, '<path d="M0,900 Q600,880 1100,920 Q1500,950 1920,960 L1920,1080 L0,1080 Z" fill="#3A3024" filter="url(#t_tas)"/>', '<path d="M0,900 Q600,880 1100,920 Q1500,950 1920,960" stroke="#1A1410" stroke-width="4" fill="none"/>']
    for k, (x, y, rr) in enumerate(((1150, 960, 34), (1380, 1000, 26), (940, 1010, 20), (1600, 1030, 40), (300, 960, 22))): g.append(boulder(x, y, rr, 600 + k))
    g.append(broken_shield(1240, 1000, 0.8, "#8E3B2E", "#D8C8A0", rot=-10) + broken_shield(760, 1010, 0.7, "#2F4C6E", "#C9A25A", rot=14))
    r = R_(158)
    for k in range(22):
        x = r.uniform(100, 1800); y = r.uniform(930, 1060); g.append(f'<path d="M{x:.0f},{y:.0f} l{-24:.0f},{-46:.0f}" stroke="#2A1E14" stroke-width="4"/><path d="M{x-24:.0f},{y-46:.0f} l-6,-14 M{x-24:.0f},{y-46:.0f} l8,-12" stroke="#D8CCB0" stroke-width="3"/>')
    draw(c, svg_sprite("".join(g)), 0, 0, 1.0)
    # kalkan duvarı: Vikingler (gerçek modeller, sıralı), kalkanlar havada
    army(c, "ragnar", [(880, 0.36, 9, 0.05), (950, 0.46, 7, 0.02)], t, seed0=151, facing=1, x0=-40, x1=880)
    fill(c, "#B8946A", 0.05)
    draw(c, svg_sprite(arrows(159, 46, (-100, 80, 1500, 860), 118, (70, 120), a=0.85)), 0, 0, 1.0)
    smoke(c, 1533, 8, (-100, 760, 2000, 1000), "#C8B49A", 0.22, 16, rx=(200, 400), ry=(30, 60))
    embers(c, 160, 50, (1100, 200, 1500, 1000), "#FFB060")
    fg = (broken_shield(120, 1080, 2.4, "#5A6A3A", "#C9A25A", rot=-6) + '<path d="M1700,1080 L1960,500" stroke="#1A1410" stroke-width="26"/><path d="M1700,1080 L1960,500" stroke="#6A5038" stroke-width="14"/>')
    draw(c, blurred(svg_sprite(fg), 8), 0, 0, 1.0)
    finish(c, cold=False, warm=0.08); return s

# ================================================================ p15d · Ragnar surdan düşüyor
def p15d():
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    draw(c, svg_sprite('<defs>' + gradient("s15d", [(0, "#4A5260"), (0.55, "#8A8E92"), (1, "#C8B898")]) + '</defs><rect width="1920" height="1080" fill="url(#s15d)"/>'), 0, 0, 1.0)
    glow(c, 360, 220, 420, "#F4E8D0", 0.35); glow(c, 360, 220, 90, "#FFF8E8", 0.6)
    draw(c, blurred(svg_sprite(cloud_band(161, 12, -100, 2000, 80, 420, "#5A606A", "#C8C0B0", 0.6, lit_dy=-8, rx=(200, 420), ry=(30, 70))), 10), 0, 0, 1.0)
    # çok aşağıda: nehir, gemiler, sur dibindeki kalabalık (yükseklik hissi)
    low = [TEXD, river(820, 1080, 162, top="#9AA0A0", mid="#6A7880", bot="#3A4650", n=60), fleet_svg([(200, 900, 0.07, 1), (420, 950, 0.08, 1), (700, 990, 0.09, 1), (120, 1010, 0.08, 1)])]
    low.append('<path d="M0,800 Q400,790 900,820 L1300,850 L1300,1080 L0,1080 Z" fill="#000" opacity="0"/>')
    lw = blurred(svg_sprite("".join(low)), 2.5); draw(c, lw, 0, 0, 1.0); draw(c, tinted(lw, "#A8A49A"), 0, 0, 1.0, a=0.35)
    smoke(c, 163, 10, (-100, 700, 1400, 1000), "#D8D2C4", 0.35, 14, rx=(200, 400), ry=(30, 70))
    # sur (sağ): üst mazgal + merdiven ucu
    wl = [TEXD, wall(1380, 1960, 330, 1100, 165, s=1.5, lit="#F4E8D0", lita=0.35), tower(1450, 1100, 180, 900, 1.5, "crenel", seed=66, light=-1)]
    fr = frank(70, shield=False, arm=True)
    fig(c, dict(fr, _hand_extra=KL.SPEAR), "angry", 1640, 480, 0.62, facing=-1, look=-0.8, shadow=0, rimc="#F4E8D0", rdx=-5)
    draw(c, svg_sprite("".join(wl)), 0, 0, 1.0)
    draw(c, svg_sprite(ladder(1130, 1120, 1340, 300, 92, 9)), 0, 0, 1.0)
    # taş parçaları + oklar + hız çizgileri
    r = R_(167); deb = []
    for k in range(16):
        x = r.uniform(780, 1380); y = r.uniform(250, 900); rr = r.uniform(6, 22); deb.append(boulder(x, y, rr, 700 + k, "#8A8274"))
        deb.append(f'<path d="M{x:.0f},{y - rr:.0f} v{-r.uniform(30, 80):.0f}" stroke="#F4F0E8" stroke-width="2" opacity="0.4"/>')
    deb.append(arrows(168, 7, (1300, 120, 1800, 500), 196, (90, 130), a=0.9, sw=4))
    for k in range(14):   # hız çizgileri (yukarı akan)
        x = r.uniform(380, 1200); y = r.uniform(80, 760); deb.append(f'<path d="M{x:.0f},{y:.0f} v{-r.uniform(60, 180):.0f}" stroke="#FFFFFF" stroke-width="{r.uniform(2,4):.1f}" opacity="{r.uniform(0.15, 0.4):.2f}" stroke-linecap="round"/>')
    draw(c, svg_sprite("".join(deb)), 0, 0, 1.0)
    # Ragnar: geriye düşüyor; kol boşluğa uzanmış, pelerin yukarı savruluyor
    fx, fy, rot, sc = 1170, 600, -68, 1.02
    cl = (f'<g transform="translate({fx},{fy}) rotate({rot})">'
          f'<path d="M-60,{-400*sc:.0f} Q-180,{-300*sc:.0f} -250,{-150*sc:.0f} Q-300,{-60*sc:.0f} -360,{-20*sc:.0f} Q-280,{-120*sc:.0f} -230,{-80*sc:.0f} Q-200,{-200*sc:.0f} -120,{-150*sc:.0f} Q-140,{-260*sc:.0f} 30,{-380*sc:.0f} Z" fill="#26344A" stroke="#1A1410" stroke-width="7"/>'
          f'<path d="M-90,{-360*sc:.0f} Q-180,{-260*sc:.0f} -250,{-120*sc:.0f}" stroke="#3A4C66" stroke-width="6" fill="none"/></g>')
    RGf = full(dict(RG, _arm_up=True, _hand_extra=""), "shock", 0.9, facing=1, look=0.8)
    c.save(); c.translate(fx, fy); c.rotate(rot)
    rim(c, RGf, 0, 0, sc, "#FFF4DC", dx=-6, dy=-4, a=0.8); draw(c, RGf, 0, 0, sc); draw(c, tinted(RGf, "#1A2230"), 0, 0, sc, a=0.22)
    c.restore()
    # elinden kayan balta
    draw(c, svg_sprite(axe_svg(1030, 250, 38, 0.95) + '<path d="M900,300 Q960,200 1080,170" stroke="#FFFFFF" stroke-width="4" fill="none" opacity="0.45" stroke-dasharray="16 12"/>'), 0, 0, 1.0)
    bloom_spot(c, 1110, 120, 30, "#FFFFFF", 0.5)
    fg = '<path d="M-40,1080 L-40,700 Q120,680 220,760 L300,1080 Z" fill="#2A2420"/>' + "".join(f'<path d="M{x},{1080} q{(k%3-1)*16},-80 {(k%5-2)*18},-{120+k%4*40}" stroke="#3A3222" stroke-width="9" fill="none"/>' for k, x in enumerate(range(0, 240, 18)))
    draw(c, blurred(svg_sprite(fg), 9), 0, 0, 1.0)
    finish(c, cold=True, warm=0.04); return s

# ================================================================ p15e · çadırda ateşler içinde
BANDAGE = ('<g><path d="M-92,-400 Q0,-380 96,-402 L98,-370 Q0,-350 -94,-368 Z" fill="#E8E0CC" stroke="#1A1410" stroke-width="5"/>'
           '<path d="M-90,-350 Q0,-330 94,-352 L96,-322 Q0,-302 -92,-320 Z" fill="#E2D8C2" stroke="#1A1410" stroke-width="5"/>'
           '<path d="M10,-372 q16,-6 24,6 q4,14 -12,18 q-18,0 -12,-24 Z" fill="#9A2A22" opacity="0.85"/></g>')
def p15e():
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    draw(c, blurred(svg_sprite(tent_bg(5)), 3), 0, 0, 1.0)
    fill(c, "#0A0604", 0.35)
    rays(c, 1590, 0, 108, 1000, 10, 4, "#BFD4F0", 0.10, t or 0.0)   # kapı aralığından soğuk ışık
    # eşyalar: direğe dayalı kalkan ve balta, su testisi
    it = [TEXD, f'<g transform="translate(1270,700)">' + KL.shield_svg("#8E3B2E", "#D8C8A0", style=1).replace('translate(70,-330) scale(0.62)', 'translate(0,0) scale(1.1)') + '</g>',
          axe_svg(1150, 880, 12, 0.9), '<g transform="translate(1400,860)"><path d="M-40,0 Q-56,-70 -30,-110 L-20,-140 L20,-140 L30,-110 Q56,-70 40,0 Z" fill="#8A5A36" stroke="#1A1410" stroke-width="6"/><path d="M-30,-60 Q0,-50 30,-60" stroke="#5A3A20" stroke-width="5" fill="none"/><path d="M-26,-110 Q-40,-60 -30,-10" stroke="#C8946A" stroke-width="4" fill="none"/></g>']
    draw(c, blurred(svg_sprite("".join(it)), 1.2), 0, 0, 1.0)
    # yatak: post yığını, yastık rulosu
    bed = [TEXD, fur_pile(1080, 880, 1240, 150, 81, "#5A4430"), fur_pile(1020, 860, 1100, 110, 82, "#7A6044", lit="#B8986C"), fur_pile(690, 790, 230, 90, 83, "#8A7A62", lit="#C8B898")]
    draw(c, svg_sprite("".join(bed)), 0, 0, 1.0)
    # Ragnar yatıyor (baş solda), göğüste sargı
    RGl = dict(RG, _arm_up=False, _body_extra=BANDAGE)
    sp = full(RGl, "sick", 0.9, facing=1, look=-0.2)
    fx, fy, sc = 1520, 790, 1.30
    c.save(); c.translate(fx, fy); c.rotate(-90)
    rim(c, sp, 0, 0, sc, "#FFB070", dx=-5, dy=-5, a=0.6); rim(c, sp, 0, 0, sc, "#9EB8D8", dx=5, dy=4, a=0.5); draw(c, sp, 0, 0, sc)
    c.restore()
    # bel altına kürk örtü
    draw(c, svg_sprite(TEXD + fur_pile(1330, 800, 520, 140, 84, "#6A5A48", lit="#A8946C") + '<path d="M1070,760 Q1100,840 1090,880" stroke="#1A1410" stroke-width="6" fill="none"/>'), 0, 0, 1.0)
    # ateş: yüzde kızarıklık + ter damlaları
    glow(c, 760, 760, 90, "#E05A3A", 0.22)
    r = R_(85)
    for k in range(9):
        x = 700 + r.uniform(-30, 70); y = 700 + r.uniform(-20, 70)
        c.drawOval(skia.Rect(x - 4, y - 6, x + 4, y + 6), skia.Paint(AntiAlias=True, Color4f=col("#DDF0FF", 0.85))); c.drawCircle(x - 1, y - 2, 1.6, skia.Paint(AntiAlias=True, Color4f=col("#FFFFFF", 1)))
    # Floki: başucunda diz çökmüş, endişeli
    fig(c, dict(FLOv, _kneel=140, _arm_up=False), ex("worry", IF.blink_at(0.5)), 430, 960, 1.0, facing=1, look=0.7, rimc="#FFB070", rdx=6, ra=0.8, shx=(560, 260), sha=0.5, shc="#0E0806")
    # ön plan: ilaç kâsesi, kanlı bez, mumlar
    fgi = [TEXD, VA.GRAD, '<g transform="translate(860,945)"><ellipse cx="0" cy="18" rx="110" ry="16" fill="#000" opacity="0.5"/><path d="M-90,-10 Q-80,40 0,44 Q80,40 90,-10 Z" fill="#6A4428" stroke="#1A1410" stroke-width="6" filter="url(#t_ahsap)"/>'
           '<path d="M-90,-10 Q-80,40 0,44 Q80,40 90,-10 Z" fill="none" stroke="#1A1410" stroke-width="6"/><ellipse cx="0" cy="-10" rx="90" ry="18" fill="#4A5A2A" stroke="#1A1410" stroke-width="5"/><ellipse cx="-20" cy="-14" rx="40" ry="6" fill="#8A9A4A" opacity="0.7"/>'
           '<path d="M30,-20 l50,-50 M40,-14 l60,-40" stroke="#5A6A3A" stroke-width="6"/><circle cx="82" cy="-72" r="8" fill="#7A8A4A" stroke="#1A1410" stroke-width="3"/></g>',
           '<g transform="translate(1110,975)"><path d="M-110,0 Q-60,-40 0,-20 Q60,-50 120,-6 Q60,20 0,10 Q-60,26 -110,0 Z" fill="#E2D8C2" stroke="#1A1410" stroke-width="5"/><path d="M-40,-14 q20,-10 40,0 q10,14 -20,16 q-30,0 -20,-16 Z M30,-20 q16,-4 20,8 q-10,8 -20,-8 Z" fill="#8E2A22" opacity="0.85"/></g>',
           VA.candlestick(200, 1040, 140, seed=3), VA.drip_candle(1720, 1010, 110, 28, True, 4), VA.drip_candle(1780, 1020, 80, 24, True, 5)]
    draw(c, svg_sprite("".join(fgi)), 0, 0, 1.0)
    for x, y in ((200, 680), (1720, 840), (1780, 880)): glow(c, x, y, 260, "#FF9A40", 0.20); bloom_spot(c, x, y + 10, 40, "#FFE6A8", 0.6)
    glow(c, 460, 700, 600, "#FF8A3A", 0.12)
    smoke(c, 86, 6, (100, 200, 1100, 700), "#5A4A40", 0.15, 16)
    draw(c, blurred(svg_sprite('<rect x="0" y="0" width="70" height="1080" fill="#1E140C"/>' + fur_pile(1760, 1110, 600, 160, 87, "#3A2A1C")), 9), 0, 0, 1.0)
    finish(c, cold=False, warm=0.05); return s

# ================================================================ p16a · plan: kömürle tabut ve kapı
PLAN = ('<g stroke="#1E1A16" fill="none" stroke-linecap="round" stroke-linejoin="round">'
        '<ellipse cx="90" cy="10" rx="170" ry="110" stroke-width="7"/><ellipse cx="92" cy="12" rx="166" ry="106" stroke-width="2.5" opacity="0.6"/>'
        + "".join(f'<path d="M{90 + 170*math.cos(a):.0f},{10 + 110*math.sin(a):.0f} l{14*math.cos(a):.0f},{14*math.sin(a):.0f}" stroke-width="5"/>' for a in [i * math.pi / 10 for i in range(20)])
        + '<path d="M-60,-30 Q-90,-80 -60,-120 M-60,50 Q-100,90 -70,140" stroke-width="3" opacity="0.6"/>'   # nehir
        '<path d="M-92,-26 L-92,30 L-70,30 L-70,-14 Q-81,-36 -92,-26 Z" fill="#1E1A16" fill-opacity="0.25" stroke-width="6"/>'   # kapı
        '<path d="M60,-40 V-90 M44,-74 H76" stroke-width="5"/><path d="M40,-40 H140 V40 H40 Z" stroke-width="4" opacity="0.7"/>'   # kilise
        '<path d="M-270,-10 L-250,-38 L-170,-38 L-150,-10 L-170,18 L-250,18 Z" stroke-width="7"/><path d="M-210,-30 V8 M-226,-16 H-194" stroke-width="5"/>'   # tabut
        '<path d="M-140,-6 Q-120,-14 -100,-4" stroke-width="6" stroke-dasharray="14 10"/><path d="M-70,0 Q0,10 60,0" stroke-width="6" stroke-dasharray="14 10"/><path d="M50,-16 L66,0 L48,14" stroke-width="7"/>'
        '<path d="M150,60 l20,20 M170,60 l-20,20" stroke="#8E1E18" stroke-width="7"/>'
        + "".join(f'<path d="M{-250 + k*22},{-100} l10,-26" stroke-width="4"/>' for k in range(6)) + '</g>')
def p16a():
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    draw(c, blurred(svg_sprite(tent_bg(6, flap=False)), 9), 0, 0, 1.0)
    fill(c, "#080402", 0.55)
    # deri parşömen (sağ), masada; kömür çizim
    rr = R_(91); pts = [(1340 + 330 * math.cos(a) * rr.uniform(0.9, 1.05), 600 + 250 * math.sin(a) * rr.uniform(0.88, 1.06)) for a in [i * math.pi / 12 for i in range(24)]]
    d = "M" + " L".join(f"{x:.0f},{y:.0f}" for x, y in pts) + " Z"
    tb = [TEXD, '<path d="M760,1080 L900,820 L1920,780 L1920,1080 Z" fill="#3A2616" filter="url(#t_ahsap)"/><path d="M900,820 L1920,780" stroke="#0A0604" stroke-width="8"/><path d="M900,826 L1920,786" stroke="#C88A50" stroke-width="3" opacity="0.5"/>',
          f'<path d="{d}" fill="#000" opacity="0.5" transform="translate(10,14)"/><path d="{d}" fill="#C8A878" filter="url(#t_deri)"/><path d="{d}" fill="none" stroke="#4A3420" stroke-width="5"/>',
          f'<g transform="translate(1360,600) rotate(3)">{PLAN}</g>',
          '<g transform="translate(1600,800) rotate(-20)"><rect x="-70" y="-9" width="140" height="18" rx="8" fill="#1E1A16" stroke="#0A0604" stroke-width="3"/><path d="M-60,-4 H50" stroke="#5A5650" stroke-width="2"/></g>',
          '<ellipse cx="1520" cy="760" rx="40" ry="14" fill="#1E1A16" opacity="0.25"/><ellipse cx="1180" cy="430" rx="30" ry="10" fill="#1E1A16" opacity="0.2"/>']
    draw(c, svg_sprite("".join(tb)), 0, 0, 1.0)
    glow(c, 1340, 600, 360, "#FFC070", 0.16)   # çizim belirir (sıcak parıltı)
    # Ragnar: gözler açık, sinsi bakış (yarım yüz mum ışığında)
    RGb = fig_bust(dict(RG, _arm_up=False), ex("sly", IF.blink_at(0.3)), 0.7, 2.3)
    with live(c, 560, 1080, phase=0.3, breathe=0.005):
        rim(c, RGb, 560, 420, 1.0, "#FFB060", dx=7, dy=-2, a=0.9); draw(c, RGb, 560, 420, 1.0); shade_side(c, RGb, 560, 420, 0.6, 760, 300, "#0A0604")
    glow(c, 640, 380, 180, "#FFB060", 0.10)
    draw(c, svg_sprite(VA.drip_candle(960, 1060, 170, 34, True, 7)), 0, 0, 1.0)
    glow(c, 960, 840, 480, "#FF9A40", 0.25); bloom_spot(c, 960, 850, 50, "#FFE6A8", 0.7)
    smoke(c, 92, 5, (700, 100, 1400, 600), "#6A5040", 0.12, 18)
    draw(c, blurred(svg_sprite(fur_pile(260, 1110, 700, 180, 93, "#3A2A1C")), 8), 0, 0, 1.0)
    finish(c, cold=False, warm=0.06); return s

def city_far(x, yb, s, seed=0):
    """Uzak Paris: sur + kuleler + kilise (ölçekli)."""
    o = [f'<g transform="translate({x},{yb}) scale({s})">', wall(-600, 600, -120, 0, 300 + seed, s=0.8)]
    for k, xx in enumerate(range(-600, 640, 200)): o.append(tower(xx, 4, 70, 170 + (k % 2) * 30, 0.8, "cone", seed=310 + k + seed, banner=("#2E4478" if k % 2 else "#8E1E22")))
    o.append(basilica(60, -110, 0.7)); o.append('</g>'); return "".join(o)

def reeds(seed, n, x0, x1, yb, h=(60, 140), cols=("#4A4A2A", "#6A6A3A", "#3A3A22")):
    r = R_(seed); return "".join(f'<path d="M{(x:=r.uniform(x0, x1)):.0f},{yb + r.uniform(-6, 10):.0f} q{r.uniform(-10,10):.0f},-{(hh:=r.uniform(*h))*0.5:.0f} {r.uniform(-24,24):.0f},-{hh:.0f}" stroke="{r.choice(cols)}" stroke-width="{r.uniform(3,6):.1f}" fill="none" stroke-linecap="round"/>' for _ in range(n))

def ripples(c, x, y, w, n=4, colr="#E8F0F4", a=0.55):
    for j in range(n):
        c.drawOval(skia.Rect(x - w * (0.5 + j * 0.3), y - 8 - j * 4, x + w * (0.5 + j * 0.3), y + 8 + j * 4), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=2.5, Color4f=col(colr, a - j * 0.11)))

PROC_CROSS = ('<g transform="translate({x},{y})"><path d="M0,0 V-560" stroke="#1A1410" stroke-width="14"/><path d="M0,0 V-560" stroke="#6A5038" stroke-width="7"/>'
              '<g transform="translate(0,-600)"><rect x="-10" y="-70" width="20" height="140" fill="url(#goldv)" stroke="#1A1410" stroke-width="5"/><rect x="-54" y="-40" width="108" height="20" fill="url(#goldv)" stroke="#1A1410" stroke-width="5"/>'
              '<circle cx="0" cy="-30" r="12" fill="url(#gem_r)" stroke="#1A1410" stroke-width="3"/></g></g>')

# ================================================================ p16b1 · vaftiz (nehir kıyısı)
def p16b1():
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    draw(c, svg_sprite('<defs>' + gradient("s16", [(0, "#4E5866"), (0.5, "#8A949C"), (1, "#C4C2B6")]) + '</defs><rect width="1920" height="620" fill="url(#s16)"/>'), 0, 0, 1.0)
    draw(c, blurred(svg_sprite(cloud_band(1611, 14, -100, 2000, 70, 380, "#4A5260", "#B8BEC4", 0.85, lit_dy=10, rx=(220, 460), ry=(30, 70))), 9), 0, 0, 1.0)
    glow(c, 760, 150, 260, "#FFF4DC", 0.45)
    o = [TEXD, VA.GRAD, '<path d="M0,540 Q500,515 960,530 Q1500,515 1920,535 L1920,600 L0,600 Z" fill="#7E8880"/>', city_far(1380, 560, 0.42, 5), city_far(380, 556, 0.30, 9)]
    o.append(river(570, 1080, 1612, top="#A8AEAA", mid="#6E7C7C", bot="#2E3E40", glint=780, gcol="#F4F0E0", n=100))
    o.append('<path d="M0,690 Q300,660 560,700 Q700,730 640,800 Q500,860 0,880 Z" fill="#4A4A34" filter="url(#t_tas)"/><path d="M0,690 Q300,660 560,700 Q700,730 640,800 Q500,860 0,880" stroke="#1A1410" stroke-width="4" fill="none"/>')   # sol kıyı (Vikingler)
    o.append('<path d="M1920,700 Q1600,680 1360,720 Q1240,760 1300,820 Q1500,860 1920,880 Z" fill="#4E4C38" filter="url(#t_tas)"/><path d="M1920,700 Q1600,680 1360,720 Q1240,760 1300,820 Q1500,860 1920,880" stroke="#1A1410" stroke-width="4" fill="none"/>')   # sağ kıyı (Franklar)
    draw(c, svg_sprite("".join(o)), 0, 0, 1.0)
    VA.beam(c, 720, 80, 160, 820, 980, 520, "#FFF2D0", 0.22, 14)
    # Vikingler (sol kıyı) + Floki, Rollo
    army(c, "ragnar", [(720, 0.30, 8, 0.05), (780, 0.38, 6, 0.0)], t, seed0=161, facing=1, x0=-20, x1=560)
    fig(c, ROLLO, "stone", 470, 840, 0.50, facing=1, look=0.6, rimc="#E8F0F8", rdx=-4, ra=0.6)
    fig(c, FLOv, ex("stone", IF.blink_at(0.5)), 330, 860, 0.52, facing=1, look=0.7, rimc="#E8F0F8", rdx=-4, ra=0.6)
    # Franklar (sağ kıyı): muhafızlar, sancaklar, haç taşıyan rahip, buhurdan
    for k, x in enumerate(range(1400, 1940, 90)): fig(c, frank(80 + k), "cold", x, 760 + (k % 2) * 10, 0.34, facing=-1, look=-0.5, shadow=0.3)
    ban = "".join(f'<g transform="translate({x},740)"><path d="M0,0 V-380" stroke="#1A1410" stroke-width="10"/><path d="M0,0 V-380" stroke="#6A5038" stroke-width="5"/><path d="M0,-374 h90 v130 l-45,-26 l-45,26 Z" fill="{c1}" stroke="#1A1410" stroke-width="4"/><path d="M45,-350 v70 M25,-320 h40" stroke="#E2B23A" stroke-width="8"/></g>' for x, c1 in ((1460, "#2E4478"), (1760, "#8E1E22")))
    draw(c, svg_sprite(VA.GRAD + ban + PROC_CROSS.format(x=1330, y=850)), 0, 0, 1.0)
    for k, (x, y) in enumerate(((1300, 860), (1420, 850))):
        sp = PRIEST(k + 4); fig(c, sp, "pray" if k else "neutral", x, y, 0.5, facing=-1, look=-0.5, shadow=0.3); draw(c, robe(0.9, -1, "#2A2622"), x, y, 0.5)
    draw(c, svg_sprite('<g transform="translate(1460,700)"><path d="M0,-90 V0" stroke="#C9A25A" stroke-width="3"/>' + VA.censer_svg(0, 0) + '</g>'), 0, 0, 1.0)
    smoke(c, 1613, 7, (1300, 420, 1520, 690), "#D8D4CC", 0.35, 12, rx=(30, 70), ry=(40, 90))
    # piskopos: suda, ibrikten su döküyor
    bx, by = 1130, 960
    fig(c, dict(BISHOP, _arm_up=True, _hand_extra=EWER), "neutral", bx, by, 0.92, facing=-1, look=-0.7, rimc="#FFF4DC", rdx=5, ra=0.7, shx=(1000, 1260), sha=0.4, shadow=0)
    draw(c, robe(0.9, -1, "#ECE6D6"), bx, by, 0.92)
    draw(c, svg_sprite(f'<g transform="translate(1080,{by - 6}) rotate(-90) scale(0.9)">' + CROZIER.replace("translate(HX,HY)", "translate(0,0) rotate(90)") + '</g>'), 0, 0, 1.0) if False else None
    # Ragnar: diz çökmüş, suda, gözler kapalı (sakin)
    rx, ry = 790, 980
    fig(c, dict(RG, _kneel=150, _arm_up=False), ex("peace", IF.blink_at(0.3)), rx, ry, 0.95, facing=1, look=0.4, rimc="#FFF4DC", rdx=-6, ra=0.75, shx=(700, 960), sha=0.4, shadow=0)
    # su: dizlere kadar örtü + halkalar
    wv = skia.Paint(AntiAlias=True, Color4f=col("#3E4E52", 0.88))
    for x0_, x1_, y_ in ((rx - 160, rx + 170, ry - 70), (bx - 180, bx + 170, by - 60)):
        c.drawRect(skia.Rect(x0_, y_, x1_, y_ + 140), wv)
        ripples(c, (x0_ + x1_) / 2, y_ + 4, (x1_ - x0_) * 0.42, 4)
    draw(c, svg_sprite(river(980, 1080, 1614, top="#3E4E52", mid="#33444A", bot="#24343A", n=30)), 0, 0, 1.0)
    # dökülen su
    stream = '<path d="M1012,402 Q900,380 850,440 Q826,480 826,520" stroke="#DDEEF6" stroke-width="10" fill="none" opacity="0.85" stroke-linecap="round"/><path d="M1012,402 Q930,380 880,430" stroke="#FFFFFF" stroke-width="3" fill="none"/>'
    stream += "".join(f'<circle cx="{840 + R_(k).uniform(-50, 60):.0f}" cy="{470 + R_(k+9).uniform(0, 260):.0f}" r="{R_(k+3).uniform(2, 5):.1f}" fill="#E8F4FA" opacity="0.8"/>' for k in range(18))
    draw(c, svg_sprite(stream), 0, 0, 1.0)
    fgr = reeds(1615, 60, -40, 380, 1090, (140, 300)) + reeds(1616, 40, 1680, 1960, 1090, (120, 260))
    draw(c, blurred(svg_sprite(fgr), 6), 0, 0, 1.0)
    draw(c, svg_sprite("".join(gull(x, y, s_, f_, rot=r_) for x, y, s_, f_, r_ in ((1040, 230, 0.4, 0.2, -6), (1150, 200, 0.3, 1.0, 4), (560, 260, 0.26, 0.5, 0)))), 0, 0, 1.0)
    card_at(c, "VAFTİZ", 420, 150, "Frank piskoposunun elinden")
    finish(c, cold=True, warm=0.06); return s

# ================================================================ p16b2 · sahte ölüm: çadırda yas
SHROUD = ('<path d="M-30,-40 Q120,-80 300,-70 Q460,-74 640,-50 Q700,-20 660,40 L-20,40 Q-50,0 -30,-40 Z" fill="#E8E2D2" stroke="#1A1410" stroke-width="7"/>'
          + "".join(f'<path d="M{x},-{60 - (x % 3) * 6} q20,40 {10 + x % 20},{90}" stroke="#B8B0A0" stroke-width="5" fill="none"/>' for x in range(40, 640, 70))
          + '<path d="M-20,-30 Q300,-90 640,-40" stroke="#FFFFFF" stroke-width="4" fill="none" opacity="0.6"/>')
def p16b2():
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    draw(c, blurred(svg_sprite(tent_bg(7, flap=False)), 4), 0, 0, 1.0)
    fill(c, "#0A0604", 0.4)
    # yas tutanlar (sedyenin arkasında)
    mourn = [(KL.soldier_spec(190, "ragnar"), 560, "grief_down"), (LAGv, 760, "grief"), (KL.soldier_spec(191, "ragnar"), 1180, "grief_down"), (ROLLO, 1360, "stone"), (KL.soldier_spec(193, "ragnar"), 1530, "grief")]
    for k, (sp, x, e) in enumerate(mourn):
        fig(c, dict(sp, _arm_up=False, _hand_extra=""), ex(e, IF.blink_at(k * 0.7)), x, 860, 0.74, facing=(1 if x < 960 else -1) if sp is not ROLLO else -1, look=0.0, rimc="#FFB070", rdx=-4, ra=0.6, shadow=0)
    # sedye (oyma uçlar) + Ragnar kefen içinde
    bier = [TEXD, '<rect x="470" y="800" width="1000" height="60" rx="8" fill="#4A3020" filter="url(#t_ahsap)"/><rect x="470" y="800" width="1000" height="60" rx="8" fill="none" stroke="#0A0604" stroke-width="6"/>',
            '<path d="M470,806 H1470" stroke="#C88A50" stroke-width="3" opacity="0.6"/>']
    for x in (500, 1440):
        bier.append(f'<rect x="{x-16}" y="860" width="32" height="110" fill="#3A2416" stroke="#0A0604" stroke-width="5"/><path d="M{x},800 q{30 if x>900 else -30},-60 {10 if x>900 else -10},-110 q{-24 if x>900 else 24},-10 {-30 if x>900 else 30},20" fill="#4A3020" stroke="#0A0604" stroke-width="6"/>')
    bier.append(fur_pile(960, 800, 980, 40, 171, "#5A4632"))
    draw(c, svg_sprite("".join(bier)), 0, 0, 1.0)
    sp = full(dict(RG, _arm_up=False), "dead", 0.9, facing=1, look=0.0)
    c.save(); c.translate(1400, 790); c.rotate(-90); rim(c, sp, 0, 0, 1.2, "#FFB070", dx=-4, dy=-4, a=0.6); draw(c, sp, 0, 0, 1.2); c.restore()
    draw(c, svg_sprite(f'<g transform="translate(800,770)">{SHROUD}</g>' + axe_svg(1060, 935, -96, 0.6)
                       + '<g transform="translate(1250,742)">' + KL.shield_svg("#2F4C6E", "#D8C8A0", style=0).replace('translate(70,-330) scale(0.62)', 'translate(0,0) scale(0.7)') + '</g>'), 0, 0, 1.0)
    glow(c, 690, 650, 100, "#C8D0D8", 0.10)   # ölü solgunluğu
    # ölü hediyeleri: sikkeler, boynuz, kol halkası; mumlar
    gifts = [VA.GRAD, '<g transform="translate(700,920)">' + "".join(f'<ellipse cx="{R_(k).uniform(-80,80):.0f}" cy="{R_(k+5).uniform(-10,14):.0f}" rx="12" ry="5" fill="url(#gold)" stroke="#1A1410" stroke-width="2"/>' for k in range(14)) + '</g>',
             '<g transform="translate(1130,925) rotate(-10)"><path d="M-80,0 Q-40,-50 50,-56 L62,-40 Q-6,-30 -50,12 Z" fill="#D8C8A0" stroke="#0A0604" stroke-width="5"/><path d="M46,-54 l16,14" stroke="#B08A3A" stroke-width="8"/></g>',
             '<ellipse cx="960" cy="930" rx="34" ry="12" fill="none" stroke="#1A1410" stroke-width="12"/><ellipse cx="960" cy="930" rx="34" ry="12" fill="none" stroke="#E2B23A" stroke-width="7"/>']
    for k, x in enumerate((560, 640, 1290, 1380)): gifts.append(VA.drip_candle(x, 990 - (k % 2) * 10, 70 + (k % 3) * 20, 24, True, k + 20))
    gifts += [VA.candlestick(380, 990, 150, seed=31), VA.candlestick(1560, 990, 150, seed=32)]
    draw(c, svg_sprite("".join(gifts)), 0, 0, 1.0)
    for x, y in ((380, 610), (1560, 610), (560, 860), (640, 850), (1290, 840), (1380, 850)): glow(c, x, y, 200, "#FF9A40", 0.16); bloom_spot(c, x, y, 26, "#FFE6A8", 0.5)
    # Floki: ön planda, başı eğik, gizli sırıtış
    fig(c, dict(FLOv, _arm_up=False), ex("sly", IF.blink_at(0.5)), 250, 1060, 1.02, facing=1, look=0.4, rimc="#FFB070", rdx=6, ra=0.85, shx=(380, 100), sha=0.55, shc="#0A0604")
    smoke(c, 172, 6, (200, 150, 1700, 600), "#6A5A4A", 0.12, 18)
    draw(c, blurred(svg_sprite(fur_pile(1760, 1110, 600, 200, 173, "#3A2A1C")), 8), 0, 0, 1.0)
    finish(c, cold=False, warm=0.06); return s

# ================================================================ p16c · tabut Paris kapısında
def gatehouse(cx, yb, s=1.0, open_=0.2, inside=False):
    """Kapı: iki yuvarlak kule, kemerli geçit, yukarı çekilmiş parmaklık, demir kuşaklı kanatlar, zincir, meşale yuvaları."""
    o = [TEXD]
    aw, ah = 400 * s, 520 * s; ax0 = cx - aw / 2
    o.append(wall(cx - 520 * s, cx + 520 * s, yb - 760 * s, yb, 401, s=1.3 * s, lit="#E8EEF2", lita=0.25))
    arch = f"M{ax0:.0f},{yb} L{ax0:.0f},{yb - ah + aw/2:.0f} A{aw/2:.0f},{aw/2:.0f} 0 0 1 {ax0 + aw:.0f},{yb - ah + aw/2:.0f} L{ax0 + aw:.0f},{yb} Z"
    o.append(f'<defs>' + gradient("gin", [(0, "#0E0C0A"), (1, "#2A2420")]) + f'</defs><path d="{arch}" fill="url(#gin)"/>')
    # voussoir taşları
    for k in range(15):
        a0 = math.pi + k * math.pi / 15; a1 = a0 + math.pi / 15; R0, R1 = aw / 2, aw / 2 + 50 * s; ccx, ccy = cx, yb - ah + aw / 2
        P_ = [(ccx + R0 * math.cos(a0), ccy + R0 * math.sin(a0)), (ccx + R1 * math.cos(a0), ccy + R1 * math.sin(a0)), (ccx + R1 * math.cos(a1), ccy + R1 * math.sin(a1)), (ccx + R0 * math.cos(a1), ccy + R0 * math.sin(a1))]
        o.append(f'<path d="M' + " L".join(f"{x:.0f},{y:.0f}" for x, y in P_) + f' Z" fill="{["#A49C8C", "#968E7E", "#B0A898"][k % 3]}" stroke="#1A1410" stroke-width="{3*s:.1f}"/>')
    # parmaklık (yukarıda)
    py = yb - ah + aw / 2 - aw * 0.25
    for x in range(int(ax0 + 30 * s), int(ax0 + aw), int(44 * s)):
        o.append(f'<path d="M{x},{yb - ah:.0f} V{py + 70*s:.0f}" stroke="#1A1410" stroke-width="{12*s:.0f}"/><path d="M{x},{yb - ah:.0f} V{py + 70*s:.0f}" stroke="#4A4E52" stroke-width="{6*s:.0f}"/><path d="M{x - 8*s:.0f},{py + 70*s:.0f} L{x},{py + 96*s:.0f} L{x + 8*s:.0f},{py + 70*s:.0f} Z" fill="#4A4E52" stroke="#1A1410" stroke-width="{2*s:.1f}"/>')
    for y in (py + 10 * s, py + 50 * s): o.append(f'<path d="M{ax0 + 20*s:.0f},{y:.0f} H{ax0 + aw - 20*s:.0f}" stroke="#1A1410" stroke-width="{10*s:.0f}"/><path d="M{ax0 + 20*s:.0f},{y:.0f} H{ax0 + aw - 20*s:.0f}" stroke="#4A4E52" stroke-width="{5*s:.0f}"/>')
    # açık kanatlar (geçit içinde, perspektif)
    dw = aw * 0.5 * (1 - open_)
    for sg in (-1, 1):
        x_out = cx + sg * aw / 2; x_in = x_out - sg * dw
        o.append(f'<path d="M{x_out:.0f},{yb:.0f} L{x_out:.0f},{yb - ah + aw*0.32:.0f} L{x_in:.0f},{yb - ah + aw*0.42:.0f} L{x_in:.0f},{yb - 20*s:.0f} Z" fill="#4A3020" stroke="#1A1410" stroke-width="{4*s:.1f}" filter="url(#t_ahsap)"/>'
                 f'<path d="M{x_out:.0f},{yb:.0f} L{x_out:.0f},{yb - ah + aw*0.32:.0f} L{x_in:.0f},{yb - ah + aw*0.42:.0f} L{x_in:.0f},{yb - 20*s:.0f} Z" fill="#000" opacity="0.35"/>')
        for q in (0.25, 0.55, 0.85):
            o.append(f'<path d="M{x_out:.0f},{yb - (ah - aw*0.32) * (1-q):.0f} L{x_in:.0f},{yb - 20*s - (ah - aw*0.42 - 20*s) * (1-q):.0f}" stroke="#2A2A2C" stroke-width="{10*s:.0f}"/>')
    for sg in (-1, 1):   # kuleler + meşale yuvaları + zincir
        o.append(tower(cx + sg * 420 * s, yb, 260 * s, 900 * s, 1.3 * s, "crenel", seed=410 + sg, light=-1, banner="#2E4478" if sg < 0 else "#8E1E22"))
        tx = cx + sg * (aw / 2 + 90 * s); ty = yb - 330 * s
        o.append(f'<path d="M{tx:.0f},{ty:.0f} l{-sg*6*s:.0f},{40*s:.0f}" stroke="#1A1410" stroke-width="{12*s:.0f}"/><path d="M{tx - 16*s:.0f},{ty:.0f} h{32*s:.0f} l{-6*s:.0f},{-40*s:.0f} h{-20*s:.0f} Z" fill="#3A3A3A" stroke="#1A1410" stroke-width="{3*s:.1f}"/>')
        o.append(f'<path d="M{cx + sg * (aw/2 + 30*s):.0f},{yb - ah - 30*s:.0f} Q{cx + sg*(aw/2 + 60*s):.0f},{yb - 400*s:.0f} {cx + sg * (aw/2 + 20*s):.0f},{yb - 180*s:.0f}" stroke="#2A2A2C" stroke-width="{9*s:.0f}" stroke-dasharray="{12*s:.0f} {5*s:.0f}" fill="none"/>')
    # asılı sancak (kemer üstü)
    o.append(f'<path d="M{cx - 70*s:.0f},{yb - 740*s:.0f} h{140*s:.0f} v{150*s:.0f} l{-70*s:.0f},{40*s:.0f} l{-70*s:.0f},{-40*s:.0f} Z" fill="#2E4478" stroke="#1A1410" stroke-width="{4*s:.1f}"/><path d="M{cx:.0f},{yb - 720*s:.0f} v{110*s:.0f} M{cx - 34*s:.0f},{yb - 680*s:.0f} h{68*s:.0f}" stroke="#E2B23A" stroke-width="{10*s:.0f}"/>')
    return "".join(o), (cx, yb, aw, ah)

COFFIN = ('<g><path d="M-250,-40 L-200,-86 L230,-86 L270,-40 L230,10 L-200,10 Z" fill="#5A3A22" stroke="#1A1410" stroke-width="7" filter="url(#t_ahsap)"/>'
          '<path d="M-250,-40 L-200,-86 L230,-86 L270,-40 L230,10 L-200,10 Z" fill="none" stroke="#1A1410" stroke-width="7"/><path d="M-250,-40 L270,-40" stroke="#2A1A10" stroke-width="5"/>'
          '<path d="M-200,-84 L230,-84" stroke="#C88A50" stroke-width="3" opacity="0.6"/><path d="M0,-80 V-6 M-30,-50 H30" stroke="#C9A25A" stroke-width="10"/>'
          '<path d="M-150,10 Q-120,50 -60,40 L-40,10 Z M120,10 Q150,46 200,36 L210,10 Z" fill="#8E2A22" stroke="#1A1410" stroke-width="4"/></g>')
def p16c():
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    draw(c, svg_sprite('<defs>' + gradient("s16c", [(0, "#5A6676"), (0.6, "#9AA4AE"), (1, "#C4C8C8")]) + '</defs><rect width="1920" height="1080" fill="url(#s16c)"/>'), 0, 0, 1.0)
    draw(c, blurred(svg_sprite(cloud_band(1621, 12, -100, 2000, 60, 300, "#5A6472", "#C8CED4", 0.8, lit_dy=-8, rx=(200, 420), ry=(30, 60))), 9), 0, 0, 1.0)
    # sur üstünde bakan muhafızlar (mazgallar arkasında)
    for k, x in enumerate((780, 900, 1020, 1140, 1260)): fig(c, frank(100 + k, shield=False), "cold", x, 250, 0.26, facing=-1, look=-0.6, shadow=0)
    gh, (gx, gy, aw, ah) = gatehouse(1020, 900, 1.0, open_=0.3)
    draw(c, svg_sprite(gh), 0, 0, 1.0)
    # yol: çamur, su birikintisi, ayak izleri, tekerlek izi
    g = [TEXD, '<path d="M0,880 Q900,860 1920,890 L1920,1080 L0,1080 Z" fill="#4A4234" filter="url(#t_tas)"/><path d="M0,880 Q900,860 1920,890" stroke="#1A1410" stroke-width="4" fill="none"/>',
         '<path d="M820,900 L1220,900 L1500,1080 L500,1080 Z" fill="#5A5040" opacity="0.6"/>' + pebbles(1622, 160, 560, 1460, 905, 1060, cols=("#6A6458", "#5A554A", "#7A7266"), hl="#C8C4B8", grow=0.8)]
    for x, y, rx_ in ((700, 980, 90), (1350, 1010, 120)): g.append(f'<ellipse cx="{x}" cy="{y}" rx="{rx_}" ry="{rx_*0.18:.0f}" fill="#8A949C" opacity="0.8"/><path d="M{x - rx_*0.6:.0f},{y - 3} h{rx_*0.8:.0f}" stroke="#D8DEE2" stroke-width="3" opacity="0.6"/>')
    draw(c, svg_sprite("".join(g)), 0, 0, 1.0)
    # rahipler (kapının sağında) + şüpheli muhafızlar
    for k, (x, y) in enumerate(((1330, 905), (1420, 912))):
        fig(c, PRIEST(k + 11), "worry", x, y, 0.5, facing=-1, look=-0.6, shadow=0.35); draw(c, robe(0.9, -1, "#2A2622"), x, y, 0.5)
    draw(c, svg_sprite(VA.GRAD + PROC_CROSS.format(x=1470, y=915).replace('V-560', 'V-420').replace('translate(0,-600)', 'translate(0,-460)')), 0, 0, 1.0)
    for k, (x, e) in enumerate(((760, "stone"), (1220, "cold"), (1560, "angry"))):
        fig(c, dict(frank(110 + k), _hand_extra=KL.SPEAR), ex(e, IF.blink_at(k)), x, 930 + k * 6, 0.62, facing=-1, look=-0.7, rimc="#E8EEF2", rdx=4, ra=0.5, shx=(x + 100, x - 100), sha=0.35)
    # tabut omuzlarda: dört taşıyıcı + önde Bjorn yerine yaşlı savaşçı
    for k, (x, y) in enumerate(((210, 985), (430, 985), (290, 1000), (510, 1000))):
        fig(c, dict(KL.soldier_spec(200 + k, "ragnar"), _arm_up=True, _hand_extra="", _body_extra=""), ex("grief_down", IF.blink_at(k * 0.5)), x, y, 0.62, facing=1, look=0.5, rimc="#E8EEF2", rdx=-4, ra=0.5, phase=k)
        if k == 1: draw(c, svg_sprite(TEXD + f'<g transform="translate(360,640) rotate(-2) scale(0.95)">{COFFIN}</g>'), 0, 0, 1.0)
    fig(c, FLOv, ex("grief", IF.blink_at(0.4)), 640, 985, 0.62, facing=1, look=0.6, rimc="#E8EEF2", rdx=-4, ra=0.5)
    for k, x in enumerate((1250, 790)):   # meşale alevleri
        flames(c, x - 14, x + 14, 570, 50, t, seed=40 + k); glow(c, x, 540, 120, "#FF9A40", 0.35)
    fg = '<path d="M1700,1080 L1940,380" stroke="#1A1410" stroke-width="22"/><path d="M1700,1080 L1940,380" stroke="#6A5038" stroke-width="12"/>' + reeds(1623, 30, -40, 220, 1090, (120, 240))
    draw(c, blurred(svg_sprite(fg), 7), 0, 0, 1.0)
    fill(c, "#B8C4CC", 0.04); finish(c, cold=True); return s

# ================================================================ p16e · kapılar açılıyor, Paris düşüyor
def p16e():
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    draw(c, svg_sprite('<defs>' + gradient("s16e", [(0, "#4A3A30"), (0.5, "#C88A50"), (1, "#F2D8A8")]) + '</defs><rect width="1920" height="1080" fill="url(#s16e)"/>'), 0, 0, 1.0)
    glow(c, 960, 640, 520, "#FFF0D0", 0.6)
    # dışarıdan akan Viking seli (kemer içinde)
    c.save(); c.clipRect(skia.Rect(620, 200, 1300, 1010))
    army(c, "ragnar", [(700, 0.26, 10, 0.10), (760, 0.34, 8, 0.06)], t, seed0=171, facing=1, x0=640, x1=1280)
    army(c, "ragnar", [(820, 0.44, 5, 0.03)], t, seed0=172, facing=-1, x0=660, x1=1260)
    c.restore()
    rays(c, 960, 560, 90, 900, 70, 10, "#FFF2D8", 0.12, t or 0.0)
    smoke(c, 1631, 10, (600, 300, 1320, 760), "#F4E8D8", 0.35, 14)
    # iç cephe: kemerli kapı boşluğu (evenodd), açılan kanatlar
    cx, aw, top, yb = 960, 640, 230, 1010
    arch = f"M{cx - aw/2},{yb} L{cx - aw/2},{top + aw/2} A{aw/2},{aw/2} 0 0 1 {cx + aw/2},{top + aw/2} L{cx + aw/2},{yb} Z"
    st = stones(0, 0, 1920, 1080, 1632, ("#5A5248", "#4E463E", "#625A50", "#463E36"), (34, 46), (60, 130), sw=2.5)
    o = [TEXD, f'<defs><clipPath id="ih"><path d="M0,0 H1920 V1080 H0 Z {arch}" clip-rule="evenodd"/></clipPath></defs>', f'<g clip-path="url(#ih)">{st}<rect width="1920" height="1080" fill="#7A6A5A" filter="url(#t_tas)" opacity="0.3"/></g>']
    o.append(f'<path d="{arch}" fill="none" stroke="#1A1410" stroke-width="10"/><path d="{arch}" fill="none" stroke="#FFD8A0" stroke-width="5" opacity="0.6" transform="translate(4,0)"/>')
    for sg in (-1, 1):   # içe açılan kanatlar (kameraya doğru)
        xe = cx + sg * aw / 2; xo = cx + sg * (aw / 2 + 300)
        o.append(f'<path d="M{xe},{yb} L{xe},{top + 120} L{xo},{top - 20} L{xo},{yb + 90} Z" fill="#4A3020" filter="url(#t_ahsap)"/><path d="M{xe},{yb} L{xe},{top + 120} L{xo},{top - 20} L{xo},{yb + 90} Z" fill="none" stroke="#0A0604" stroke-width="8"/>')
        for q in (0.15, 0.45, 0.75):
            o.append(f'<path d="M{xe},{top + 120 + (yb - top - 120) * q:.0f} L{xo},{top - 20 + (yb + 110 - top) * q:.0f}" stroke="#1A1A1C" stroke-width="22"/>'
                     + "".join(f'<circle cx="{xe + (xo - xe) * u:.0f}" cy="{top + 120 + (yb - top - 120) * q + ((top - 20 + (yb + 110 - top) * q) - (top + 120 + (yb - top - 120) * q)) * u:.0f}" r="7" fill="#6A6E72"/>' for u in (0.2, 0.5, 0.8)))
        for k in range(8): o.append(f'<path d="M{xe + (xo - xe) * k / 8:.0f},{top + 120 - 140 * k / 8:.0f} L{xe + (xo - xe) * k / 8:.0f},{yb + 90 * k / 8:.0f}" stroke="#2A1A10" stroke-width="3"/>')
    # kırık sürgü + düşmüş muhafızın kalkanı/miğferi
    o.append('<g transform="translate(980,960) rotate(6)"><path d="M-300,-24 L-20,-30 L0,-10 L-10,10 L-300,12 Z" fill="#5A3A22" stroke="#0A0604" stroke-width="6" filter="url(#t_ahsap)"/><path d="M-300,-24 L-20,-30 L0,-10 L-10,10 L-300,12 Z" fill="none" stroke="#0A0604" stroke-width="6"/>'
             '<path d="M30,-20 L20,0 L36,16 L320,22 L320,-18 Z" fill="#5A3A22" stroke="#0A0604" stroke-width="6"/><path d="M-6,-26 l14,-30 M4,8 l18,26 M24,-20 l10,-24" stroke="#E8C890" stroke-width="5"/></g>')
    o.append(kite("#2E4478", "#E2B23A", 1380, 1000, 0.6).replace('translate(1380,1000)', 'translate(1380,1000) rotate(70)'))
    draw(c, svg_sprite("".join(o)), 0, 0, 1.0)
    # yanan şehir (iki yanda evler)
    hs = TEXD + house(-60, 760, 330, 300, 1641, 1.6) + house(1640, 760, 340, 300, 1642, 1.6)
    hsp = svg_sprite(hs); draw(c, hsp, 0, 0, 1.0); draw(c, tinted(hsp, "#1A0E08"), 0, 0, 1.0, a=0.45)
    for x0_, x1_, y_ in ((-40, 280, 470), (1660, 1960, 470), (-40, 260, 760), (1650, 1940, 760)):
        flames(c, x0_, x1_, y_, 300, t, seed=x0_ % 97); glow(c, (x0_ + x1_) / 2, y_ - 80, 300, "#FF7A2A", 0.35)
    smoke(c, 1633, 12, (-100, 60, 400, 500), "#2A2420", 0.55, 16); smoke(c, 1634, 12, (1520, 60, 2020, 500), "#2A2420", 0.55, 16)
    embers(c, 1635, 120, (0, 80, 1920, 1000), "#FFC070")
    # düşen Frank muhafız (yerde)
    lying(c, frank(120, shield=False), "pain", 1560, 980, 0.62, deg=-84)
    # Ragnar: kapının yanında, balta kalkık
    fig(c, dict(RG, _arm_up=True, _hand_extra=KL.BEARD_AXE), ex("fierce", IF.blink_at(0.2)), 420, 1040, 1.0, facing=1, look=0.6, rimc="#FFB060", rdx=-7, ra=0.9, shx=(560, 250), sha=0.45, shc="#140A06")
    finish(c, cold=False, warm=0.12); return s

# ================================================================ p17 · dönüş: "Biliyorum."
def p17():
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    o = ['<defs>' + gradient("s17", [(0, "#46525E"), (0.6, "#8A96A0"), (1, "#B4BCC0")]) + '</defs><rect width="1920" height="600" fill="url(#s17)"/>',
         cloud_band(1701, 12, -100, 2000, 80, 400, "#4E5A66", "#A8B2BA", 0.8, lit_dy=-8, rx=(220, 460), ry=(24, 60)),
         river(560, 1080, 1702, top="#7E8A90", mid="#4A5A64", bot="#1E2A32", n=110), fleet_svg([(260, 600, 0.06, 1), (1560, 596, 0.05, 1), (1720, 606, 0.07, 1)])]
    draw(c, blurred(svg_sprite("".join(o)), 3), 0, 0, 1.0)
    glow(c, 300, 300, 420, "#DCE6EE", 0.25)
    # direk + halatlar + yelken kenarı (arka plan, odak dışı)
    rg = ('<path d="M120,0 V1080" stroke="#1A1410" stroke-width="56"/><path d="M120,0 V1080" stroke="#5A3E26" stroke-width="40"/><path d="M104,0 V1080" stroke="#8A6A46" stroke-width="6" opacity="0.6"/>'
          '<path d="M150,60 L1000,700 M150,200 L760,900" stroke="#2A1E14" stroke-width="9"/><path d="M1920,0 Q1700,140 1720,330 L1920,330 Z" fill="#B8322A"/><path d="M1920,0 Q1780,120 1800,330" stroke="#E8DCC0" stroke-width="44" fill="none"/>')
    draw(c, blurred(svg_sprite(rg), 5), 0, 0, 1.0)
    # Floki: geride solda, yüzü donmuş
    FLb = fig_bust(FLOv, ex("dread", IF.blink_at(0.5)), 0.8, 1.85)
    with live(c, 600, 1080, phase=0.5, breathe=0.005):
        rim(c, FLb, 600, 470, 1.0, "#CFE0F0", dx=-6, dy=-3, a=0.7); draw(c, FLb, 600, 470, 1.0); shade_side(c, FLb, 600, 470, 0.45, 450, 800, "#0E1620")
    # Ragnar: önde, denize bakıyor; boynunda Athelstan'ın haçı
    RGb = fig_bust(dict(RG, _body_extra=CROSS_P), ex("coldv", IF.blink_at(0.2)), -0.45, 2.25)
    with live(c, 1240, 1080, phase=0.2, breathe=0.005):
        rim(c, RGb, 1240, 420, 1.0, "#E6F0FA", dx=-7, dy=-3, a=0.85); draw(c, RGb, 1240, 420, 1.0); shade_side(c, RGb, 1240, 420, 0.45, 1100, 1500, "#0E1620")
    # ön plan: küpeşte, halat kangalı, serpinti
    fg = [TEXD, '<path d="M-20,1080 L-20,960 Q900,930 1940,990 L1940,1080 Z" fill="#4A3220" filter="url(#t_ahsap)"/><path d="M-20,960 Q900,930 1940,990" stroke="#1A1410" stroke-width="18" fill="none"/><path d="M-20,954 Q900,924 1940,984" stroke="#9A7448" stroke-width="6" fill="none"/>']
    for k in range(4): fg.append(f'<ellipse cx="1640" cy="{1000 - k*8}" rx="{120 - k*14}" ry="{30 - k*3}" fill="none" stroke="#1A1410" stroke-width="14"/><ellipse cx="1640" cy="{1000 - k*8}" rx="{120 - k*14}" ry="{30 - k*3}" fill="none" stroke="#B8A070" stroke-width="8" stroke-dasharray="9 3"/>')
    draw(c, svg_sprite("".join(fg)), 0, 0, 1.0)
    r = R_(1703)
    for k in range(60): c.drawCircle(r.uniform(0, 1920), r.uniform(80, 1000), r.uniform(1.5, 4), skia.Paint(AntiAlias=True, Color4f=col("#EEF4F8", r.uniform(0.25, 0.7))))
    for k in range(8): c.drawCircle(r.uniform(0, 1920), r.uniform(100, 900), r.uniform(12, 26), skia.Paint(AntiAlias=True, Color4f=col("#F4F8FA", 0.1), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 4)))
    fill(c, "#9EB0C0", 0.05); finish(c, cold=True); return s

# ================================================================ p18a · doğudan gelen ilaç
VIAL = ('<g transform="translate(HX,HY) rotate(-15)"><path d="M-10,-70 L10,-70 L10,-50 Q30,-36 28,0 Q26,26 0,28 Q-26,26 -28,0 Q-30,-36 -10,-50 Z" fill="#7AB89A" fill-opacity="0.7" stroke="#1A1410" stroke-width="5"/>'
        '<path d="M-24,0 Q-22,22 0,24 Q22,22 24,0 Z" fill="#C8D8A0"/><rect x="-12" y="-86" width="24" height="18" rx="4" fill="#6A4428" stroke="#1A1410" stroke-width="4"/><path d="M-16,-36 Q-20,-10 -14,10" stroke="#FFFFFF" stroke-width="4" fill="none" opacity="0.7"/></g>')
def p18a():
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    draw(c, blurred(svg_sprite(tent_bg(9, flap=False) + fur_pile(500, 700, 900, 200, 181, "#4A3A2A") + fur_pile(420, 640, 500, 120, 182, "#6A5440")), 9), 0, 0, 1.0)
    fill(c, "#060806", 0.6)
    # Ragnar: solgun, terli; şişeyi yüzüne kaldırmış
    RGP = dict(RG, skin="#D8CDB4", _arm_up=True, _hand_extra=VIAL)
    RGb = fig_bust(RGP, ex("sick", IF.blink_at(0.3)), -0.5, 2.2)
    with live(c, 1180, 1080, phase=0.3, breathe=0.008):
        rim(c, RGb, 1180, 430, 1.0, "#B8E0A0", dx=-5, dy=-2, a=0.35); draw(c, RGb, 1180, 430, 1.0); shade_side(c, RGb, 1180, 430, 0.6, 1000, 1500, "#040604")
    r = R_(1801)
    for k in range(10):
        x = 1180 + r.uniform(-110, 110); y = 300 + r.uniform(-40, 60)
        c.drawOval(skia.Rect(x - 4, y - 6, x + 4, y + 6), skia.Paint(AntiAlias=True, Color4f=col("#DDF0E8", 0.85))); c.drawCircle(x - 1, y - 2, 1.6, skia.Paint(AntiAlias=True, Color4f=col("#FFFFFF", 1)))
    # masa: dökülmüş toz, boş kâse, tek mum (yeşilimsi ton)
    tb = [TEXD, VA.GRAD, '<path d="M0,1080 L120,840 L1100,820 L1180,1080 Z" fill="#2A2016" filter="url(#t_ahsap)"/><path d="M120,840 L1100,820" stroke="#0A0604" stroke-width="8"/><path d="M120,846 L1100,826" stroke="#9AB880" stroke-width="3" opacity="0.4"/>',
          '<g transform="translate(560,905)"><ellipse rx="150" ry="30" fill="#D8D8C0" opacity="0.65"/>' + "".join(f'<circle cx="{r.uniform(-200,200):.0f}" cy="{r.uniform(-30,40):.0f}" r="{r.uniform(1.5,4):.1f}" fill="#E8E8D0" opacity="0.8"/>' for _ in range(70)) + '<path d="M-60,-6 q40,-14 90,-4" stroke="#B8B8A0" stroke-width="4" fill="none"/></g>',
          '<g transform="translate(380,900) rotate(80)"><path d="M-10,-70 L10,-70 L10,-50 Q30,-36 28,0 Q26,26 0,28 Q-26,26 -28,0 Q-30,-36 -10,-50 Z" fill="#7AB89A" fill-opacity="0.55" stroke="#1A1410" stroke-width="5"/></g>',
          '<g transform="translate(860,920)"><path d="M-80,-10 Q-70,40 0,44 Q70,40 80,-10 Z" fill="#5A3A22" stroke="#1A1410" stroke-width="6"/><ellipse cx="0" cy="-10" rx="80" ry="16" fill="#1A120C" stroke="#1A1410" stroke-width="5"/></g>',
          '<g transform="translate(700,930) rotate(-12)"><rect x="-70" y="-5" width="120" height="10" rx="4" fill="#8A7A5A" stroke="#1A1410" stroke-width="3"/><ellipse cx="60" cy="0" rx="18" ry="10" fill="#8A7A5A" stroke="#1A1410" stroke-width="3"/></g>',
          VA.drip_candle(240, 880, 90, 28, True, 9)]
    draw(c, svg_sprite("".join(tb)), 0, 0, 1.0)
    glow(c, 240, 760, 420, "#C8E08A", 0.20); bloom_spot(c, 240, 770, 40, "#F0FFD0", 0.7)
    glow(c, 1500, 250, 160, "#9AE0A0", 0.22)
    smoke(c, 1802, 7, (200, 150, 1500, 700), "#6A7A60", 0.18, 18)
    fill(c, "#2A4A2A", 0.10); finish(c, cold=False, warm=0.0); return s

# ================================================================ p18c · surda Frank zırhlı Rollo; nehirde Ragnar
def mangonel(x, y, s=1.0):
    return (f'<g transform="translate({x},{y}) scale({s})"><path d="M-160,0 L-40,-260 L80,0 M-120,-90 L40,-90" stroke="#1A1410" stroke-width="30"/><path d="M-160,0 L-40,-260 L80,0 M-120,-90 L40,-90" stroke="#6A4C30" stroke-width="18"/>'
            '<path d="M-40,-240 L-300,-420" stroke="#1A1410" stroke-width="26"/><path d="M-40,-240 L-300,-420" stroke="#7A5A3A" stroke-width="14"/><path d="M-300,-420 q-30,20 -10,50 q30,10 40,-20 Z" fill="#5A4630" stroke="#1A1410" stroke-width="5"/>'
            '<rect x="-200" y="-10" width="320" height="30" fill="#4A3220" stroke="#1A1410" stroke-width="6"/><circle cx="-40" cy="-250" r="16" fill="#3A3A3A" stroke="#1A1410" stroke-width="5"/></g>')
def p18c():
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    draw(c, svg_sprite('<defs>' + gradient("s18c", [(0, "#3A4250"), (0.6, "#7A848E"), (1, "#A8B0B4")]) + '</defs><rect width="1920" height="1080" fill="url(#s18c)"/>'), 0, 0, 1.0)
    draw(c, blurred(svg_sprite(cloud_band(1811, 14, -100, 2000, 60, 420, "#3E4652", "#9AA4AE", 0.85, lit_dy=-10, rx=(220, 460), ry=(30, 70))), 10), 0, 0, 1.0)
    glow(c, 1300, 120, 360, "#E8EEF2", 0.25)
    # sol alt: nehir, Ragnar'ın gemisi
    draw(c, svg_sprite(river(640, 1080, 1812, top="#8A949A", mid="#4E5E66", bot="#1E2A30", n=80)), 0, 0, 1.0)
    # sancaklar + mancınık (sur üstü, arkada)
    ban = "".join(f'<g transform="translate({x},600)"><path d="M0,0 V-500" stroke="#1A1410" stroke-width="12"/><path d="M0,0 V-500" stroke="#6A5038" stroke-width="6"/><path d="M0,-494 h130 q-20,60 0,120 q20,60 0,120 h-130 Z" fill="{c1}" stroke="#1A1410" stroke-width="5"/><path d="M60,-460 v150 M20,-400 h80" stroke="#E2B23A" stroke-width="12"/></g>' for x, c1 in ((900, "#2E4478"), (1620, "#8E1E22")))
    draw(c, svg_sprite(ban + mangonel(1840, 600, 0.9)), 0, 0, 1.0)
    for k, (x, sc) in enumerate(((980, 0.78), (1480, 0.80), (1740, 0.72))):
        fig(c, dict(frank(130 + k), _hand_extra=KL.SPEAR), ex("cold", IF.blink_at(k)), x, 790, sc, facing=-1, look=-0.7, rimc="#E8EEF2", rdx=4, ra=0.6, shx=(x - 100, x + 100), sha=0.35, shadow=0)
    # Rollo: alt açı, heybetli
    fig(c, ROLLO_F, ex("coldv", IF.blink_at(1.0)), 1240, 820, 1.12, facing=-1, look=-0.85, rimc="#F2F6FA", rdx=5, rdy=-4, ra=0.9, shx=(1100, 1420), sha=0.45, shadow=0)
    draw(c, svg_sprite(TEXD + '<g transform="matrix(1,0.04,0,1,0,-30)">' + wall(640, 1960, 640, 1100, 1813, s=1.6, lit="#E8EEF2", lita=0.35) + '</g>' + tower(660, 1100, 220, 560, 1.6, "crenel", seed=1814, light=-1)), 0, 0, 1.0)
    # Ragnar: gemide, yukarı bakıyor
    sh = f'<g transform="translate(260,1000) scale(0.62)">{G.hull(1.0, shields=True, oars=True, wet=True)}</g>'
    fig(c, dict(RG, _arm_up=False), ex("torn", IF.blink_at(0.2)), 330, 985, 0.52, facing=1, look=0.9, rimc="#E8EEF2", rdx=-4, ra=0.6, shadow=0)
    draw(c, svg_sprite(sh), 0, 0, 1.0)
    for k in range(20): x = R_(k).uniform(-60, 600); c.drawLine(x, 1000 + R_(k + 7).uniform(-10, 20), x + 40, 1000 + R_(k + 7).uniform(-10, 20), skia.Paint(AntiAlias=True, StrokeWidth=2.5, Color4f=col("#C8D4DA", 0.5)))
    smoke(c, 1815, 8, (-100, 560, 700, 700), "#D8DEE2", 0.25, 12, rx=(200, 400), ry=(20, 50))
    draw(c, svg_sprite("".join(gull(x, y, s_, f_, col_="#2E2E34", dark="#141418", rot=r_) for x, y, s_, f_, r_ in ((420, 300, 0.35, 0.3, -6), (520, 260, 0.28, 1.0, 4), (300, 360, 0.22, 0.5, 0)))), 0, 0, 1.0)
    card_at(c, "ROLLO", 1500, 150, "artık bir Frank")
    finish(c, cold=True); return s

# ================================================================ p18d · zincir, yanan gemiler, geri çekilme
def chain(x0, y0, x1, y1, sag, n=70):
    o = []
    for k in range(n):
        q = k / n; x = x0 + (x1 - x0) * q; y = y0 + (y1 - y0) * q + sag * 4 * q * (1 - q)
        o.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{11 if k%2 else 4}" ry="{6}" fill="none" stroke="#1A1410" stroke-width="6"/><ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{11 if k%2 else 4}" ry="6" fill="none" stroke="#6A6E72" stroke-width="3"/>')
    return "".join(o)
def p18d():
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    draw(c, svg_sprite('<defs>' + gradient("s18d", [(0, "#2A2238"), (0.45, "#6A3E48"), (0.8, "#D8784A"), (1, "#F2B068")]) + '</defs><rect width="1920" height="620" fill="url(#s18d)"/>'), 0, 0, 1.0)
    draw(c, blurred(svg_sprite(cloud_band(1821, 12, -100, 2000, 80, 360, "#3A2A3A", "#E89A6A", 0.8, lit_dy=10, rx=(220, 460), ry=(24, 56))), 8), 0, 0, 1.0)
    o = [TEXD, '<path d="M0,560 Q500,540 960,552 Q1400,540 1920,556 L1920,600 L0,600 Z" fill="#3A2A30"/>', city_far(960, 572, 0.32, 21)]
    o.append(river(590, 1080, 1822, top="#C8805A", mid="#5A3A40", bot="#1A141E", glint=960, gcol="#FFB070", n=110, lineD="#140E14", lineL="#E8A070"))
    o.append(tower(170, 700, 170, 420, 1.0, "cone", seed=1823, banner="#2E4478", light=1) + tower(1760, 690, 170, 420, 1.0, "cone", seed=1824, banner="#8E1E22"))
    o.append(chain(240, 560, 1680, 560, 110))
    draw(c, svg_sprite("".join(o)), 0, 0, 1.0)
    # yanan gemiler (zincire takılmış), eğik direkler
    ships = [(620, 700, 0.24, -14), (980, 690, 0.22, 10), (1340, 712, 0.26, -22)]
    for x, y, sc, rot in ships:
        draw(c, svg_sprite(f'<g transform="translate({x},{y}) scale({sc})"><g transform="rotate({rot} 20 -60)">{G.mast_sail(0.6)}</g>{G.hull(1.0, shields=True, oars=False)}</g>'), 0, 0, 1.0)
        flames(c, x - 120 * sc / 0.24, x + 130 * sc / 0.24, y - 10, 170, t, seed=x % 91)
        glow(c, x, y - 60, 300, "#FF7A2A", 0.40)
        for k in range(16): rr = R_(x + k); yy = y + 30 + rr.uniform(0, 150); c.drawLine(x + rr.gauss(0, 60), yy, x + rr.gauss(0, 60) + rr.uniform(20, 60), yy, skia.Paint(AntiAlias=True, StrokeWidth=3, Color4f=col("#FFB060", rr.uniform(0.3, 0.8))))
    smoke(c, 1825, 16, (400, 80, 1500, 600), "#1E1618", 0.6, 18, rx=(80, 200), ry=(80, 160))
    # alevli oklar (kulelerden)
    arc = "".join(f'<path d="M{x0},{y0} Q{(x0+x1)/2},{y0 - 220} {x1},{y1}" stroke="#FFB060" stroke-width="3" fill="none" opacity="0.5" stroke-dasharray="4 10"/><circle cx="{x1}" cy="{y1}" r="6" fill="#FFE0A0"/>'
                  for x0, y0, x1, y1 in ((230, 320, 700, 640), (260, 330, 1000, 620), (1700, 320, 1300, 660), (1720, 300, 900, 600), (1690, 340, 1500, 760)))
    draw(c, svg_sprite(arc), 0, 0, 1.0)
    for x, y in ((700, 640), (1000, 620), (1300, 660), (900, 600), (1500, 760)): glow(c, x, y, 40, "#FFC070", 0.6)
    embers(c, 1826, 140, (400, 100, 1600, 760), "#FFB060")
    # Ragnar'ın gemisi: önde, geri çekiliyor (pruva sola)
    rs = f'<g transform="translate(560,960) scale(-0.55,0.55)">{G.mast_sail(0.0, reefed=True)}</g>'
    draw(c, svg_sprite(rs), 0, 0, 1.0)
    fig(c, dict(RG, _arm_up=False), ex("broken", IF.blink_at(0.2)), 760, 960, 0.40, facing=1, look=0.8, rimc="#FF9A50", rdx=6, ra=0.9, shadow=0)
    for k, x in enumerate((420, 560)): fig(c, dict(KL.soldier_spec(220 + k, "ragnar"), _arm_up=False, _body_extra=""), "pain", x, 962, 0.36, facing=1, look=0.6, rimc="#FF9A50", rdx=6, ra=0.8, shadow=0)
    draw(c, svg_sprite(f'<g transform="translate(560,960) scale(-0.55,0.55)">{G.hull(1.0, shields=True, oars=True, wet=True)}</g>'), 0, 0, 1.0)
    glow(c, 700, 860, 300, "#FF8A3A", 0.12)
    for k in range(26): rr = R_(k + 90); x = 900 + rr.uniform(0, 300); y = 990 + rr.uniform(-10, 20); c.drawLine(x, y, x + rr.uniform(30, 80), y, skia.Paint(AntiAlias=True, StrokeWidth=2.5, Color4f=col("#F2C8A0", 0.5)))
    finish(c, cold=False, warm=0.06); return s

# ================================================================ REVİZYON (kullanıcı, 20.11): p15d, p16b2, p18a
def _xf(px, py, wy, arch, rot, fx, fy):
    """yerel figür noktası → dünya (bel üstü 'arch' kadar bükülü, sonra 'rot')."""
    if py < wy:
        a = math.radians(arch); dx, dy = px, py - wy; px, py = dx * math.cos(a) - dy * math.sin(a), wy + dx * math.sin(a) + dy * math.cos(a)
    r = math.radians(rot); return fx + px * math.cos(r) - py * math.sin(r), fy + px * math.sin(r) + py * math.cos(r)

def p15d():
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    draw(c, svg_sprite('<defs>' + gradient("s15d2", [(0, "#2E3644"), (0.5, "#6E7682"), (1, "#B8AE98")]) + '</defs><rect width="1920" height="1080" fill="url(#s15d2)"/>'), 0, 0, 1.0)
    glow(c, 520, 160, 480, "#F4E8D0", 0.35); glow(c, 520, 160, 90, "#FFF8E8", 0.65)
    rays(c, 520, 160, 60, 1300, 50, 9, "#FFF2D8", 0.07, t or 0.0)
    smoke(c, 2161, 14, (-100, 60, 1400, 700), "#3A3634", 0.45, 16, rx=(160, 340), ry=(50, 120))
    # alttan bakış: yukarı doğru daralan devasa sur (sağ) + üstte uzak kule
    wl = [TEXD, '<g transform="matrix(1,0,-0.36,1,389,0)">', wall(1180, 2400, 270, 1100, 2162, s=1.7, lit="#F4E8D0", lita=0.4), '</g>']
    far = TEXD + '<g transform="matrix(1,0,-0.2,1,60,0)">' + tower(560, 1100, 160, 980, 1.2, "crenel", seed=2163) + '</g>'
    fsp = blurred(svg_sprite(far), 3); draw(c, fsp, 0, 0, 1.0); draw(c, tinted(fsp, "#6E7682"), 0, 0, 1.0, a=0.55)
    # parapetten eğilen Frank muhafız (sur çizilmeden önce: alt gövdesi mazgalın arkasında)
    fr = full(dict(frank(70, shield=False, arm=True), _hand_extra=KL.SPEAR), "angry", 0.9, facing=-1, look=-0.9)
    c.save(); c.translate(1700, 480); c.rotate(-30); rim(c, fr, 0, 0, 0.62, "#F4E8D0", dx=-5, dy=-4, a=0.7); draw(c, fr, 0, 0, 0.62); c.restore()
    draw(c, svg_sprite("".join(wl)), 0, 0, 1.0)
    draw(c, svg_sprite(ladder(1250, 1120, 1360, 290, 96, 9)), 0, 0, 1.0)
    # Ragnar: geriye bükülmüş, kollar savrulmuş, baş aşağı kameraya doğru düşüyor
    fx, fy, rot, arch, sc, fs = 1060, 250, -146, -34, 1.12, 0.9
    wy = -235 * fs * sc
    farm = (f'<path d="M-60,-430 Q-170,-470 -250,-560" stroke="#1A1410" stroke-width="58" stroke-linecap="round" fill="none"/><path d="M-60,-430 Q-170,-470 -250,-560" stroke="{RG["tunic"]}" stroke-width="44" stroke-linecap="round" fill="none"/>'
            f'<ellipse cx="-268" cy="-584" rx="26" ry="30" fill="{RG["skin"]}" stroke="#1A1410" stroke-width="5"/><path d="M-284,-604 l-14,-20 M-270,-610 l-6,-24 M-256,-608 l2,-22" stroke="#1A1410" stroke-width="5" stroke-linecap="round"/>')
    RGf = full(dict(RG, _arm_up=True, _hand_extra="", _body_extra=farm), "shock", fs, facing=1, look=0.8)
    hx, hy = _xf(0, -560 * fs * sc, wy, arch, rot, fx, fy); shx_, shy_ = _xf(-40, -430 * fs * sc, wy, arch, rot, fx, fy)
    # yukarı savrulan pelerin + örgüler (dünya yönünde yukarı), arkada
    r = R_(2164); fl = []
    fl.append(f'<path d="M{shx_-90:.0f},{shy_:.0f} Q{shx_-160:.0f},{shy_-220:.0f} {shx_-60:.0f},{shy_-420:.0f} Q{shx_+10:.0f},{shy_-300:.0f} {shx_+60:.0f},{shy_-380:.0f} Q{shx_+90:.0f},{shy_-200:.0f} {shx_+120:.0f},{shy_-60:.0f} Z" fill="{RG["cloak"]}" stroke="#1A1410" stroke-width="7"/>'
              f'<path d="M{shx_-60:.0f},{shy_-40:.0f} Q{shx_-110:.0f},{shy_-220:.0f} {shx_-50:.0f},{shy_-380:.0f}" stroke="#3E5270" stroke-width="7" fill="none"/>')
    for k in range(5):
        a0 = r.uniform(-40, 40); fl.append(f'<path d="M{hx + a0:.0f},{hy - 20:.0f} q{r.uniform(-40,40):.0f},-90 {r.uniform(-30,30):.0f},-{r.uniform(150,230):.0f}" stroke="#1A1410" stroke-width="22" fill="none" stroke-linecap="round"/><path d="M{hx + a0:.0f},{hy - 20:.0f} q{r.uniform(-40,40):.0f},-90 {r.uniform(-30,30):.0f},-{r.uniform(150,230):.0f}" stroke="{RG["hair"]}" stroke-width="13" fill="none" stroke-linecap="round" stroke-dasharray="16 5"/>')
    draw(c, svg_sprite("".join(fl)), 0, 0, 1.0)
    def body(sp, a=1.0, blur=None):
        c.save(); c.translate(fx, fy); c.rotate(rot)
        for part in (0, 1):
            c.save()
            if part: c.translate(0, wy); c.rotate(arch); c.translate(0, -wy); c.clipRect(skia.Rect(-2000, -4000, 2000, wy + 24))
            else: c.clipRect(skia.Rect(-2000, wy, 2000, 4000))
            if a == 1.0: rim(c, sp, 0, 0, sc, "#FFF4DC", dx=-6, dy=-4, a=0.8)
            draw(c, sp if blur is None else blurred(sp, blur), 0, 0, sc, a=a); c.restore()
        c.restore()
    c.save(); c.translate(0, -70); body(RGf, 0.25, 6); c.restore()   # hareket bulanıklığı izi
    c.save(); c.translate(0, -35); body(RGf, 0.35, 3); c.restore()
    body(RGf); draw(c, tinted(RGf, "#1A2230"), 0, 0, 0.0)
    deb = []
    for k in range(30):   # hız çizgileri (düşüş yönüne paralel)
        x = r.uniform(300, 1300); y = r.uniform(80, 1000); deb.append(f'<path d="M{x:.0f},{y:.0f} l{r.uniform(-20,0):.0f},{-r.uniform(80, 220):.0f}" stroke="#FFFFFF" stroke-width="{r.uniform(2,5):.1f}" opacity="{r.uniform(0.15, 0.4):.2f}" stroke-linecap="round"/>')
    for k in range(12): x = r.uniform(600, 1400); y = r.uniform(150, 900); deb.append(boulder(x, y, r.uniform(8, 26), 900 + k, "#8A8274"))
    deb.append(arrows(2165, 6, (1100, 100, 1700, 600), 160, (90, 130), a=0.9, sw=4))
    draw(c, svg_sprite("".join(deb)), 0, 0, 1.0)
    ax = svg_sprite(axe_svg(470, 760, -125, 1.1)); draw(c, blurred(ax, 5), 0, -40, 1.0, a=0.4); draw(c, ax, 0, 0, 1.0)
    draw(c, svg_sprite('<path d="M520,600 Q380,640 360,780" stroke="#FFFFFF" stroke-width="5" fill="none" opacity="0.45" stroke-dasharray="18 12"/>'), 0, 0, 1.0)
    for j in range(40): q = R_(j + 3000); c.drawCircle(q.uniform(0, 1920), q.uniform(80, 1000), q.uniform(2, 5), skia.Paint(AntiAlias=True, Color4f=col("#E8E2D6", q.uniform(0.3, 0.7))))
    finish(c, cold=True, warm=0.05); return s

def shroud_svg(x0, x1, ytop, seed=1):
    """Gövde biçimine oturan kefen: omuz-göğüs-bel-kalça-diz-ayak kabartısı; sedyenin önünden sarkan kıvrımlı etek."""
    r = R_(seed); L = x1 - x0
    prof = [(0, 34), (0.05, 8), (0.14, -4), (0.26, 4), (0.36, 22), (0.46, 14), (0.58, 26), (0.74, 40), (0.84, 30), (0.93, 6), (0.98, 0), (1.0, 40)]
    pt = lambda q: ytop + next(h0 + (h1 - h0) * (q - q0) / (q1 - q0) for (q0, h0), (q1, h1) in zip(prof, prof[1:]) if q0 <= q <= q1)
    top = " ".join(f"{x0 + L*q:.0f},{pt(q):.0f}" for q in [k / 60 for k in range(61)])
    hem = " ".join(f"{x1 - L*q:.0f},{ytop + 168 + 16*math.sin(q*31) + r.uniform(-4,4):.0f}" for q in [k / 40 for k in range(41)])
    d = f"M{x0-4},{ytop+60} L{top} Q{x1+30},{ytop+80} {x1+20},{ytop+168} L{hem} Q{x0-20},{ytop+140} {x0-4},{ytop+60} Z"
    o = ['<defs>' + gradient("shr", [(0, "#F6F2E8"), (0.35, "#E2DACA"), (0.7, "#B8B0A0"), (1, "#8A8274")]) + '</defs>', f'<path d="{d}" fill="url(#shr)" stroke="#1A1410" stroke-width="6" stroke-linejoin="round"/>']
    for k in range(22):   # gövdeden sedye kenarına inen eğri kıvrımlar
        q = (k + 0.5) / 22; x = x0 + L * q; y0 = pt(q) + 8; sw_ = r.uniform(-30, 30)
        o.append(f'<path d="M{x:.0f},{y0:.0f} C{x + sw_*0.3:.0f},{y0 + 40:.0f} {x + sw_:.0f},{ytop + 110:.0f} {x + sw_*0.7:.0f},{ytop + 164:.0f}" stroke="#7E766A" stroke-width="{r.uniform(3,7):.1f}" fill="none" opacity="0.65"/>'
                 f'<path d="M{x+9:.0f},{y0+6:.0f} C{x + 9 + sw_*0.3:.0f},{y0 + 40:.0f} {x + 9 + sw_:.0f},{ytop + 110:.0f} {x + 9 + sw_*0.7:.0f},{ytop + 158:.0f}" stroke="#FFFFFF" stroke-width="2.5" fill="none" opacity="0.45"/>')
    for q, w_ in ((0.36, 70), (0.58, 60), (0.74, 90)):   # göğüs, kalça, diz hacmi: kumaşın gerildiği yatay çekiş
        x = x0 + L * q; y = pt(q); o.append(f'<path d="M{x-w_:.0f},{y+26:.0f} Q{x:.0f},{y+6:.0f} {x+w_:.0f},{y+28:.0f}" stroke="#9A9282" stroke-width="4" fill="none"/><path d="M{x-w_*0.6:.0f},{y+8:.0f} Q{x:.0f},{y-2:.0f} {x+w_*0.6:.0f},{y+10:.0f}" stroke="#FFFFFF" stroke-width="5" fill="none" opacity="0.7"/>')
    o.append(f'<path d="M{x0+L*0.97:.0f},{ytop+2:.0f} q14,-30 34,-6 M{x0+L*0.97:.0f},{ytop+6:.0f} q-6,-26 -24,-14" stroke="#8A8272" stroke-width="4" fill="none"/>')   # ayak uçları
    o.append(f'<path d="M{x0-2},{ytop+56} Q{x0+30},{ytop+30} {x0+60},{ytop+28}" stroke="#7E766A" stroke-width="6" fill="none"/>')   # boyunda kıvrılan kenar
    return "".join(o)

def p16b2():
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    draw(c, blurred(svg_sprite(tent_bg(7, flap=False)), 4), 0, 0, 1.0)
    fill(c, "#0A0604", 0.4)
    mourn = [(KL.soldier_spec(190, "ragnar"), 560, "grief_down"), (LAGv, 760, "grief"), (KL.soldier_spec(191, "ragnar"), 1180, "grief_down"), (ROLLO, 1360, "stone"), (KL.soldier_spec(193, "ragnar"), 1530, "grief")]
    for k, (sp, x, e) in enumerate(mourn):
        fig(c, dict(sp, _arm_up=False, _hand_extra=""), ex(e, IF.blink_at(k * 0.7)), x, 860, 0.74, facing=(1 if x < 960 else -1) if sp is not ROLLO else -1, look=0.0, rimc="#FFB070", rdx=-4, ra=0.6, shadow=0)
    bier = [TEXD, '<rect x="470" y="800" width="1000" height="60" rx="8" fill="#4A3020" filter="url(#t_ahsap)"/><rect x="470" y="800" width="1000" height="60" rx="8" fill="none" stroke="#0A0604" stroke-width="6"/>']
    for x in (500, 1440):
        bier.append(f'<rect x="{x-16}" y="860" width="32" height="110" fill="#3A2416" stroke="#0A0604" stroke-width="5"/><path d="M{x},800 q{30 if x>900 else -30},-60 {10 if x>900 else -10},-110 q{-24 if x>900 else 24},-10 {-30 if x>900 else 30},20" fill="#4A3020" stroke="#0A0604" stroke-width="6"/>')
    bier.append(fur_pile(960, 800, 980, 40, 171, "#5A4632"))
    bier.append('<g transform="translate(1280,905)">' + KL.shield_svg("#2F4C6E", "#D8C8A0", style=0).replace('translate(70,-330) scale(0.62)', 'translate(0,0) scale(0.55)') + '</g>')   # sedyeye dayalı kalkan
    draw(c, svg_sprite("".join(bier)), 0, 0, 1.0)
    sp = full(dict(RG, _arm_up=False, skin="#DCD2C2"), "dead", 0.9, facing=1, look=0.0)
    c.save(); c.translate(1400, 790); c.rotate(-90); rim(c, sp, 0, 0, 1.2, "#FFB070", dx=-4, dy=-4, a=0.6); draw(c, sp, 0, 0, 1.2); c.restore()
    # kefen, göğüste haç ve kılıç, üstünde çaprazlanmış eller
    sk = "#D8CCBA"
    hand = lambda x, y, rt: (f'<g transform="translate({x},{y}) rotate({rt})"><path d="M-30,-14 Q-8,-24 26,-16 Q40,-8 34,8 Q10,18 -30,12 Z" fill="{sk}" stroke="#1A1410" stroke-width="4"/>'
                              + "".join(f'<path d="M{6+j*8},-14 l4,22" stroke="#9A8A78" stroke-width="2"/>' for j in range(3)) + f'<path d="M-30,-14 L-70,-20 L-70,14 L-30,12 Z" fill="{RG["tunic"]}" stroke="#1A1410" stroke-width="4"/></g>')
    top = shroud_svg(885, 1440, 696, 3)
    sw = ('<g transform="translate(990,742) rotate(1)"><path d="M40,-6 L380,-4 L404,2 L380,8 L40,8 Z" fill="#C8D0D8" stroke="#1A1410" stroke-width="5"/><path d="M50,-1 H380" stroke="#F4F8FC" stroke-width="2"/>'
          '<rect x="26" y="-24" width="14" height="50" rx="4" fill="#8A7A5A" stroke="#1A1410" stroke-width="4"/><rect x="-30" y="-6" width="56" height="14" rx="5" fill="#4A2A1A" stroke="#1A1410" stroke-width="4"/><circle cx="-36" cy="1" r="10" fill="#C9A25A" stroke="#1A1410" stroke-width="4"/></g>')
    cross = '<g transform="translate(1110,712)"><path d="M-40,-30 Q-20,10 0,8 Q20,10 40,-30" stroke="#5A4026" stroke-width="3" fill="none"/><rect x="-6" y="-2" width="12" height="40" fill="#C8B070" stroke="#1A1410" stroke-width="3"/><rect x="-16" y="8" width="32" height="10" fill="#C8B070" stroke="#1A1410" stroke-width="3"/></g>'
    draw(c, svg_sprite(top + cross + sw + hand(1026, 746, 14) + hand(1032, 734, -16)), 0, 0, 1.0)
    glow(c, 780, 640, 110, "#C8D0D8", 0.14)   # ölü solgunluğu
    gifts = [VA.GRAD, '<g transform="translate(700,920)">' + "".join(f'<ellipse cx="{R_(k).uniform(-80,80):.0f}" cy="{R_(k+5).uniform(-10,14):.0f}" rx="12" ry="5" fill="url(#gold)" stroke="#1A1410" stroke-width="2"/>' for k in range(14)) + '</g>',
             '<g transform="translate(1100,925) rotate(-10)"><path d="M-80,0 Q-40,-50 50,-56 L62,-40 Q-6,-30 -50,12 Z" fill="#D8C8A0" stroke="#0A0604" stroke-width="5"/><path d="M46,-54 l16,14" stroke="#B08A3A" stroke-width="8"/></g>',
             '<ellipse cx="960" cy="930" rx="34" ry="12" fill="none" stroke="#1A1410" stroke-width="12"/><ellipse cx="960" cy="930" rx="34" ry="12" fill="none" stroke="#E2B23A" stroke-width="7"/>', axe_svg(860, 960, -94, 0.55)]
    for k, x in enumerate((560, 640, 1390, 1460)): gifts.append(VA.drip_candle(x, 990 - (k % 2) * 10, 70 + (k % 3) * 20, 24, True, k + 20))
    gifts += [VA.candlestick(380, 990, 150, seed=31), VA.candlestick(1590, 990, 150, seed=32)]
    draw(c, svg_sprite("".join(gifts)), 0, 0, 1.0)
    for x, y in ((380, 610), (1590, 610), (560, 860), (640, 850), (1390, 840), (1460, 850)): glow(c, x, y, 200, "#FF9A40", 0.16); bloom_spot(c, x, y, 26, "#FFE6A8", 0.5)
    glow(c, 1100, 720, 380, "#FFB070", 0.10)
    fig(c, dict(FLOv, _arm_up=False), ex("sly", IF.blink_at(0.5)), 250, 1060, 1.02, facing=1, look=0.4, rimc="#FFB070", rdx=6, ra=0.85, shx=(380, 100), sha=0.55, shc="#0A0604")
    smoke(c, 172, 6, (200, 150, 1700, 600), "#6A5A4A", 0.12, 18)
    draw(c, blurred(svg_sprite(fur_pile(1760, 1110, 600, 200, 173, "#3A2A1C")), 8), 0, 0, 1.0)
    finish(c, cold=False, warm=0.06); return s

EXP["haze"] = (-8, 4, 0.62, 0.14, "flat", "")
VIAL_S = ('<g transform="translate(HX,HY) rotate(-70) scale(0.7)"><path d="M-10,-70 L10,-70 L10,-50 Q30,-36 28,0 Q26,26 0,28 Q-26,26 -28,0 Q-30,-36 -10,-50 Z" fill="#8AB89A" fill-opacity="0.75" stroke="#1A1410" stroke-width="6"/>'
          '<path d="M-24,0 Q-22,22 0,24 Q22,22 24,0 Z" fill="#D8DCC0"/><rect x="-12" y="-86" width="24" height="18" rx="4" fill="#6A4428" stroke="#1A1410" stroke-width="4"/></g>')
def p18a():
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    draw(c, blurred(svg_sprite(tent_bg(9, flap=False) + fur_pile(1500, 760, 900, 220, 181, "#4A3A2A") + fur_pile(1600, 690, 500, 120, 182, "#5A4636")), 9), 0, 0, 1.0)
    fill(c, "#050705", 0.62)
    # yaslandığı direk
    draw(c, svg_sprite(TEXD + '<rect x="560" y="0" width="120" height="1080" fill="#2A1C12" filter="url(#t_ahsap)"/><rect x="560" y="0" width="120" height="1080" fill="none" stroke="#0A0604" stroke-width="7"/><path d="M570,0 V1080" stroke="#7A8A60" stroke-width="4" opacity="0.35"/>'), 0, 0, 1.0)
    # Ragnar: direğe çökmüş, göz kapakları ağır; titreyen el şişeyi ağzının altında tutuyor, öteki kol sarkık
    RGP = dict(RG, skin="#D2CBB2", _carry_svg="<g/>", _hand_extra=VIAL_S)
    RGb = fig_bust(RGP, ex("haze", None), -0.6, 2.05)
    bx, by = 900, 400
    c.save(); c.translate(bx, 1080); c.rotate(-9); c.translate(-bx, -1080)
    for dx, a in ((-9, 0.18), (8, 0.14)): draw(c, RGb, bx + dx, by + 3, 1.0, a=a)   # titreme (çift görüntü)
    rim(c, RGb, bx, by, 1.0, "#A8C890", dx=6, dy=-3, a=0.45); draw(c, RGb, bx, by, 1.0); shade_side(c, RGb, bx, by, 0.65, 1150, 700, "#040604")
    c.restore()
    r = R_(1801)
    for k in range(14):
        x = 860 + r.uniform(-110, 120); y = 450 + r.uniform(-90, 90)
        c.drawOval(skia.Rect(x - 3.5, y - 5.5, x + 3.5, y + 5.5), skia.Paint(AntiAlias=True, Color4f=col("#DDEEE0", 0.8))); c.drawCircle(x - 1, y - 2, 1.4, skia.Paint(AntiAlias=True, Color4f=col("#FFFFFF", 1)))
    # ön plan zemin/sandık: dökülmüş toz, devrilmiş kupa, boş kâse, kaşık, tek mum
    tb = [TEXD, '<path d="M1000,1080 L1080,860 L1920,840 L1920,1080 Z" fill="#241A12" filter="url(#t_ahsap)"/><path d="M1080,860 L1920,840" stroke="#0A0604" stroke-width="8"/><path d="M1080,866 L1920,846" stroke="#9AB880" stroke-width="3" opacity="0.35"/>',
          '<g transform="translate(1380,925)"><ellipse rx="170" ry="30" fill="#D0D2BC" opacity="0.6"/>' + "".join(f'<circle cx="{r.uniform(-220,220):.0f}" cy="{r.uniform(-28,40):.0f}" r="{r.uniform(1.5,4):.1f}" fill="#E4E6D0" opacity="0.8"/>' for _ in range(80)) + '</g>',
          '<g transform="translate(1600,930) rotate(-100)"><path d="M-40,-50 L40,-50 L32,40 Q0,52 -32,40 Z" fill="#6A4A30" stroke="#1A1410" stroke-width="6"/><ellipse cx="0" cy="-50" rx="40" ry="12" fill="#2A1A10" stroke="#1A1410" stroke-width="5"/></g>',
          '<path d="M1530,950 q-60,14 -110,6 q-30,-4 -60,8" stroke="#3A4A2A" stroke-width="10" fill="none" opacity="0.7" stroke-linecap="round"/>',
          '<g transform="translate(1200,935)"><path d="M-70,-10 Q-60,36 0,40 Q60,36 70,-10 Z" fill="#5A3A22" stroke="#1A1410" stroke-width="6"/><ellipse cx="0" cy="-10" rx="70" ry="14" fill="#1A120C" stroke="#1A1410" stroke-width="5"/></g>',
          VA.drip_candle(1780, 900, 70, 26, True, 9)]
    draw(c, svg_sprite("".join(tb)), 0, 0, 1.0)
    glow(c, 1780, 790, 520, "#B8C890", 0.20); bloom_spot(c, 1780, 800, 40, "#E8F4D0", 0.65)
    glow(c, 1000, 560, 120, "#A8D8A0", 0.15)
    smoke(c, 1802, 7, (500, 150, 1700, 700), "#5A6A50", 0.18, 18)
    draw(c, blurred(svg_sprite(fur_pile(300, 1100, 800, 240, 183, "#2A2016")), 8), 0, 0, 1.0)
    fill(c, "#2A3A2A", 0.12); finish(c, cold=False, warm=0.0); return s

FR = {"p15b": p15b, "p15c": p15c, "p15d": p15d, "p15e": p15e, "p16a": p16a, "p16b1": p16b1, "p16b2": p16b2, "p16c": p16c, "p16e": p16e,
      "p17": p17, "p18a": p18a, "p18c": p18c, "p18d": p18d}
# R13 kırpmaları (x, y, w, h) — yalnızca en riskli 4 kare: 15b, 16b(1), 16e, 17
CROPS = {"p15b": [(860, 260, 640, 400), (60, 760, 700, 300)], "p16b1": [(700, 300, 560, 520), (1250, 380, 560, 480)],
         "p16e": [(250, 300, 500, 720), (640, 560, 640, 440)], "p17": [(380, 220, 500, 560), (1000, 180, 560, 760)],
         "p15d": [(560, 80, 760, 820)], "p16b2": [(660, 560, 820, 300)], "p18a": [(560, 120, 700, 760)]}
def contact(ids):
    from PIL import Image
    n = len(ids); rows = (n + 1) // 2
    sheet = Image.new("RGB", (960 * 2 + 30, 560 * rows + 10), "#EDE2CC")
    for k, i in enumerate(ids): sheet.paste(Image.open(f"{OUTP}/{i}.png").convert("RGB").resize((960, 540)), (10 + (k % 2) * 970, 10 + (k // 2) * 560))
    sheet.save(f"{OUTP}/kontakt_paris_960.png")
if __name__ == "__main__":
    ids = sys.argv[1:] or list(FR)
    for i in ids:
        T[0] = None; p = f"{OUTP}/{i}.png"
        FR[i]().makeImageSnapshot().save(p, skia.kPNG); print("kare", i, flush=True)
        for k, b in enumerate(CROPS.get(i, []), 1): crop2x(p, b, f"{OUTP}/{i}_crop{k}.png")
    contact([i for i in FR if os.path.exists(f"{OUTP}/{i}.png")])
