import math, random
from functools import lru_cache
import skia
from engine import *
from art2 import *
from bg import *

# ───────── yardımcılar
@lru_cache(None)
def C(name, age="adult", pose="stand", expr="neutral", facing=1, props=(), ss=1.0, **kw):
    spec = dict(CAST[name]); spec.update(kw)
    return char_sprite(character(spec, age, pose, expr, facing=facing, props=props), ss=ss)

CAST = dict(ragnar=RAGNAR, lod=RAGNAR_LOD, old=RAGNAR_OLD, child=RAGNAR_CHILD, teen=RAGNAR_TEEN, hring=SIGURD_HRING,
            lagertha=LAGERTHA, thora=THORA, kraka=KRAKA, aslaug=ASLAUG, herraud=HERRAUD, ivar=IVAR, bjorn=BJORN,
            hvitserk=HVITSERK, sigurd=SIGURD_SNAKE, charles=CHARLES, aella=AELLA, scholar=SCHOLAR, warrior=WARRIOR,
            woman=WOMAN_WARRIOR, saxon=SAXON, baker=BAKER)

def actor(c, sp, x, y, s, t, ph=0.0, breathe=0.010, bob=0.0):
    k = 1 + breathe * math.sin(t * 2.4 + ph)
    draw(c, sp, x, y + bob * math.sin(t * 3 + ph), sx=s, sy=s * k)

class cam:
    def __init__(self, c, z=1.0, cx=W/2, cy=H/2, rot=0.0):
        self.c, self.z, self.cx, self.cy, self.rot = c, z, cx, cy, rot
    def __enter__(self):
        z = max(1.0, self.z); hw, hh = W/(2*z), H/(2*z)
        self.cx = min(max(self.cx, hw), W - hw); self.cy = min(max(self.cy, hh), H - hh)
        c = self.c; c.save(); c.translate(W/2, H/2); c.scale(self.z, self.z)
        if self.rot: c.rotate(self.rot)
        c.translate(-self.cx, -self.cy); return c
    def __exit__(self, *a): self.c.restore()

def S(body, w=W, h=H, ss=1.0, ax=None, ay=None):
    return sprite(body, w, h, ax=ax, ay=ay, ss=ss, defs=f"<defs>{GRAIN}</defs>")

def popdraw(c, sp, x, y, t, t0, s=1.0, rot=0.0, d=0.32):
    k = pop(t, t0, d)
    if k > 0: draw(c, sp, x, y, s * k, rot=rot, a=min(1, k * 1.5))

def arrow_at(c, t, t0, x0, y0, x1, y1, bend=0.25, color="#FFFFFF"):
    if t >= t0: hand_arrow(c, x0, y0, x1, y1, bend=bend, prog=ease_out(lin(t, t0, t0 + 0.35)), color=color)

def impact(c, x, y, t, t0, r=160, color="#FFE27A"):
    if t < t0 or t > t0 + 0.5: return
    p = lin(t, t0, t0 + 0.5); k = back(min(1, p * 2.2)); a = 1 - ease_in(p)
    path = skia.Path(); n = 14
    for i in range(n * 2):
        ang = i * math.pi / n; rr = r * k * (1 if i % 2 == 0 else 0.45)
        (path.moveTo if i == 0 else path.lineTo)(x + rr*math.cos(ang), y + rr*math.sin(ang))
    path.close()
    c.drawPath(path, skia.Paint(Color4f=col(color, a), AntiAlias=True))
    c.drawPath(path, skia.Paint(Color4f=col(INK, a), AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=6))

def speedlines(c, cx, cy, t, a=0.5, n=40, r0=420, seed=3):
    rnd = random.Random(seed + int(t * 12)); p = skia.Paint(AntiAlias=True, StrokeWidth=5, Color4f=col("#FFFFFF", a))
    for i in range(n):
        ang = rnd.uniform(0, 6.283); r1 = r0 + rnd.uniform(0, 200)
        c.drawLine(cx + r1*math.cos(ang), cy + r1*math.sin(ang), cx + (r1+500)*math.cos(ang), cy + (r1+500)*math.sin(ang), p)

def flash(c, t, t0, d=0.25, color="#FFFFFF"):
    if t0 <= t < t0 + d: fill(c, color, 0.85 * (1 - lin(t, t0, t0 + d)))

# ═══════════════════════════════ PROLOG: SAGA TAŞI
PANEL_NAMES = ["EJDERHA", "BİLMECE", "PARİS", "PANTOLON"]
def panel_art(i, lit):
    ink = INK if lit else "#4E4A44"; st = "#3A3630"
    if i == 0:   # ejderha / yılan
        b = serpent_body([(40, 300), (110, 230), (60, 170), (150, 120), (230, 160)], w=34, c="#6E9C4F" if lit else "#6A665E", belly="#C9D28A" if lit else "#7A766E", spots=lit)
        b += serpent_head(240, 150, 0.55, -10, c="#6E9C4F" if lit else "#6A665E", mouth_open=True)
        b += f'<path d="M30,330 L220,140" stroke="{st}" stroke-width="10"/><path d="M220,140 l-18,30 l28,-8 z" fill="#C3CCD3" stroke="{st}" stroke-width="4"/>' if lit else ""
    elif i == 1:  # bilmece: ağ + soğan + köpek
        b = (f'<text x="150" y="250" font-family="Pirata One" font-size="220" text-anchor="middle" fill="{"#E2B23A" if lit else "#5A5650"}" stroke="{st}" stroke-width="6">?</text>')
    elif i == 2:  # Paris + sikkeler
        c1 = "#8FA8C8" if lit else "#6A665E"
        b = (f'<rect x="40" y="160" width="220" height="120" fill="{c1}" stroke="{st}" stroke-width="6"/>'
             + "".join(f'<rect x="{40+k*44}" y="130" width="28" height="32" fill="{c1}" stroke="{st}" stroke-width="5"/>' for k in range(5))
             + f'<path d="M110,280 v-60 q40,-40 80,0 v60" fill="{"#3A4A6A" if lit else "#4A4640"}" stroke="{st}" stroke-width="5"/>'
             + (f'<g transform="translate(150,90)">{coins_pile(12, 4, 200, 60)}</g>' if lit else ""))
    else:  # pantolon
        fur = "#7A5432" if lit else "#6A665E"
        b = (f'<g transform="translate(150,170)">' + fur_leg(-34, -110, -50, 120, 64, fur) + fur_leg(34, -110, 50, 120, 64, fur)
             + f'<rect x="-80" y="-130" width="160" height="36" rx="6" fill="{"#4A3020" if lit else "#5A5650"}" stroke="{st}" stroke-width="5"/></g>')
    return b

@lru_cache(None)
def saga_stone_sprites():
    w, h = 1700, 860
    base = S(stone_slab(w, h, "#7A766E") + rune_border(w, h, "#4E4A44"), w + 40, h + 40, ss=1.0, ax=0, ay=0)
    title = label("RAGNAR'IN DESTANI", size=70, font="Cinzel Decorative", color="#E9DCC0", sw=10)
    panels = []
    for i in range(4):
        dim = S(f'<rect x="6" y="6" width="288" height="348" rx="16" fill="#5E5A54" stroke="#3A3630" stroke-width="8"/>{panel_art(i, False)}', 300, 360, ax=0, ay=0)
        lit = S(f'<rect x="6" y="6" width="288" height="348" rx="16" fill="#EAD7A8" stroke="#D8A93A" stroke-width="10"/><rect x="6" y="6" width="288" height="348" rx="16" filter="url(#parch)"/>{panel_art(i, True)}', 300, 360, ax=0, ay=0)
        name = label(PANEL_NAMES[i], size=44, font="Alegreya SC", color="#F6ECD4", sw=8, weight="800")
        panels.append((dim, lit, name))
    bg = S(f'<rect width="{W}" height="{H}" fill="#14100C"/>' + "".join(f'<rect x="{x}" y="0" width="160" height="{H}" fill="#1C1611" stroke="#0E0B08" stroke-width="4"/>' for x in range(0, W, 160)) + grain(W, H))
    return base, title, panels, bg

def saga_stone(c, x):
    t, sh = x.t, x.shot
    base, title, panels, bg = saga_stone_sprites()
    mode = sh.get("panel", 0)
    # hangi paneller yanık, hangisi şimdi yanıyor
    if mode in (0, 1, 2):
        order = [0, 2, 3]; lit_before = order[:mode]; now = order[mode]; now_t = x.c(len(sh["lines"]) - 1) + 0.15 if mode != 0 else x.c(1)
        if mode == 2: now_t = x.c(1)
        lit = {i: 1.0 for i in lit_before}; lit[now] = fade(t, now_t, 0.35)
        focus = now
    elif mode == 3:
        lit = {0: fade(t, x.c(0), 0.3), 1: fade(t, x.c(1), 0.3), 2: fade(t, x.c(2), 0.3), 3: 0.25}; focus = [0, 1, 2][min(2, x.idx())]
    else:
        lit = {0: 0.6, 1: 0.6, 2: 0.6, 3: fade(t, 0.2, 0.5)}; focus = 3
    draw(c, bg, W/2, H/2)
    z = 1.0 + 0.03 * ease_io(lin(t, 0, x.dur)) + (0.18 * ease_io(lin(t, x.dur - 1.2, x.dur)) if mode == 4 else 0)
    fx = 110 + 112 + focus * 400 + 150
    cx = W/2 + (fx - W/2) * (0.15 if mode != 4 else 0.6 * ease_io(lin(t, 0, x.dur)))
    with cam(c, z, cx, H/2):
        draw(c, base, 110, 120)
        draw(c, title, W/2, 205, 0.95)
        for i, (dim, litsp, name) in enumerate(panels):
            px, py = 112 + 110 + i * 400, 300
            draw(c, dim, px, py)
            a = lit.get(i, 0)
            if a > 0:
                glow(c, px + 150, py + 180, 260, "#FFB347", 0.35 * a)
                draw(c, litsp, px, py, a=a)
                draw(c, name, px + 150, py + 410, 0.9 * (0.9 + 0.1 * a), a=a)
    Particles("ember", 26, seed=11, area=(0, 0, W, H), color="#FFB35A", speed=30).draw(c, t, 0.8)
    for xx in (60, W - 60):
        glow(c, xx, 520, 380, "#FF9A40", 0.22 + 0.05 * math.sin(t * 7 + xx))
    vignette(c, 0.7)

# ═══════════════════════════════ BEŞİK
@lru_cache(None)
def cradle_sprites():
    room = S(longhouse_interior(W + 200, H + 120) + grain(W + 200, H + 120), W + 200, H + 120)
    crad = S(f'<g transform="translate(300,420)"><path d="M-230,-60 Q-240,60 0,70 Q240,60 230,-60 Z" fill="#8C5E34" stroke="{INK}" stroke-width="6"/>'
             f'<path d="M-260,50 Q0,150 260,50" stroke="#6B4222" stroke-width="20" fill="none" stroke-linecap="round"/>'
             f'<path d="M-260,50 Q0,150 260,50" stroke="{INK}" stroke-width="4" fill="none" opacity="0.5"/>'
             f'<g transform="translate(0,-10) scale(0.95)">{baby("sleepy")}</g>'
             f'<path d="M-232,-60 Q0,-20 232,-60" stroke="#6B4222" stroke-width="12" fill="none"/></g>', 600, 560, ax=300, ay=520, ss=1.3)
    skald = C("hring", pose="hold_front", expr="happy", tunic="#4A5E3A", cloak="#2F3E2A", circlet=False, armring=False, hair="#9A8A72", beard="full", beard_c="#8A7A62", hair_style="short")
    lyre = S(f'<path d="M-50,60 Q-70,-40 -40,-90 L40,-90 Q70,-40 50,60 Z" fill="none" stroke="#8C5E34" stroke-width="16"/><path d="M-50,60 Q-70,-40 -40,-90 L40,-90 Q70,-40 50,60 Z" fill="none" stroke="{INK}" stroke-width="3"/>'
             f'<rect x="-56" y="40" width="112" height="26" rx="8" fill="#8C5E34" stroke="{INK}" stroke-width="4"/>' + "".join(f'<path d="M{x},-84 V44" stroke="#E9DCC0" stroke-width="3"/>' for x in (-24, -8, 8, 24)), 160, 200)
    note = S(f'<g transform="translate(60,70)"><ellipse cx="-14" cy="20" rx="20" ry="14" fill="#F6ECD4" stroke="{INK}" stroke-width="4"/><path d="M4,20 V-50 Q30,-40 34,-20" stroke="{INK}" stroke-width="7" fill="none"/>'
             f'<path d="M4,20 V-50 Q30,-40 34,-20" stroke="#F6ECD4" stroke-width="3" fill="none"/></g>', 120, 140)
    crownnote = S(f'<g transform="translate(70,70)">{crown(0, 20, 0.7)}</g>', 140, 120)
    return room, crad, skald, lyre, note, crownnote

def cradle(c, x):
    t = x.t; room, crad, skald, lyre, note, crownnote = cradle_sprites()
    z = 1.08 - 0.06 * ease_io(lin(t, 0, x.dur)); cx = W/2 + 60 - 120 * ease_io(lin(t, 0, x.dur))
    with cam(c, z, cx, H/2 + 40):
        draw(c, room, W/2, H/2 - 20)
        glow(c, 1300, 860, 700, "#FF9A40", 0.35 + 0.05*math.sin(t*6))
        draw(c, hearth_sp(), 1300, 900)
        draw(c, flame_sp(int(t * 8) % 6), 1300, 880)
        actor(c, crad, 760, 980, 1.0, t, breathe=0.0)
        # beşik sallanması
        actor(c, skald, 1650, 1000, 0.95, t, ph=1.0)
        draw(c, lyre, 1640, 800, 0.8, rot=-12)
        if t > x.c(2):
            tt = t - x.c(2)
            for k in range(4):
                p = (tt - k * 0.55)
                if p > 0:
                    draw(c, crownnote if k % 2 else note, 1560 - p * 120, 650 - p * 140 + 18*math.sin(p*4), 0.8 + 0.1*k, a=clamp(1.6 - p * 0.45))
    Particles("ember", 30, seed=3, area=(1000, 300, 1600, 900), color="#FFC070", speed=50).draw(c, t)
    if t > x.c(1): draw(c, hand_label("sen →", 58), 420, 610, pop(t, x.c(1)), rot=-6)
    vignette(c, 0.65)

@lru_cache(None)
def hearth_sp(): return S(hearth(300, 120, 1.0), 600, 200, ax=300, ay=120)
@lru_cache(None)
def flame_sp(k): return S(flame(150, 300, 1.0, t=k * 0.37), 300, 320, ax=150, ay=300)

# ═══════════════════════════════ DUVAR HALISI: BRÁVELLIR
@lru_cache(None)
def tapestry_sprites():
    w, h = 1600, 900
    cloth = (f'<rect x="0" y="40" width="{w}" height="{h-60}" fill="#B9473A" stroke="{INK}" stroke-width="6"/>'
             f'<rect x="30" y="70" width="{w-60}" height="{h-120}" fill="#E7D3A8" stroke="#7A2E24" stroke-width="10"/>'
             f'<rect x="30" y="70" width="{w-60}" height="{h-120}" filter="url(#parch)"/>'
             + "".join(f'<path d="M{x},{h-20} v34" stroke="#B9473A" stroke-width="10" stroke-linecap="round"/>' for x in range(20, w, 26))
             + f'<rect x="-30" y="20" width="{w+60}" height="36" rx="18" fill="#6B4222" stroke="{INK}" stroke-width="6"/>'
             + "".join(f'<path d="M{x},{h-170} q20,-14 40,0 q20,14 40,0" stroke="#3E6E4A" stroke-width="6" fill="none"/>' for x in range(60, w-80, 80)).replace(f"{h-170}", f"{h-110}"))
    # iki ordu (dikiş stili)
    def stitch_army(x0, color, flip):
        o = ""
        for k in range(6):
            xx = x0 + k * 70 * flip; yy = 640 - (k % 2) * 30
            o += (f'<g transform="translate({xx},{yy})"><circle cx="0" cy="-90" r="22" fill="{color}" stroke="{INK}" stroke-width="4"/>'
                  f'<path d="M-22,-66 L22,-66 L26,0 L-26,0 Z" fill="{color}" stroke="{INK}" stroke-width="4"/>'
                  f'<path d="M{18*flip},-60 L{30*flip},-150" stroke="{INK}" stroke-width="5"/><circle cx="{-26*flip}" cy="-40" r="20" fill="#E9D6A0" stroke="{INK}" stroke-width="4"/></g>')
        return o
    armies = stitch_army(220, "#2F4C6E", 1) + stitch_army(1380, "#7A2E24", -1)
    labelA = '<text x="380" y="740" font-family="Alegreya SC" font-weight="bold" font-size="38" fill="#2F4C6E" text-anchor="middle">SIGURD HRING</text>'
    labelB = '<text x="1220" y="740" font-family="Alegreya SC" font-weight="bold" font-size="38" fill="#7A2E24" text-anchor="middle">HARALD SAVAŞDİŞ</text>'
    title = '<text x="330" y="190" font-family="Pirata One" font-size="96" fill="#5A2018" text-anchor="middle">Brávellir</text>'
    base = S(cloth + armies + labelA + labelB + title, w, h + 40, ss=1.0)
    king = S(f'<g transform="translate(100,240)"><circle cx="0" cy="-130" r="30" fill="#7A2E24" stroke="{INK}" stroke-width="5"/>{crown(0,-160,0.5)}'
             f'<path d="M-32,-100 L32,-100 L36,0 L-36,0 Z" fill="#7A2E24" stroke="{INK}" stroke-width="5"/></g>', 200, 260, ax=100, ay=240)
    odin = S(f'<g transform="translate(160,330)"><path d="M-80,0 L-60,-200 Q0,-240 60,-200 L80,0 Z" fill="#2E3A4E" stroke="{INK}" stroke-width="6"/>'
             f'<circle cx="0" cy="-240" r="40" fill="#E9D6A0" stroke="{INK}" stroke-width="5"/><path d="M-30,-250 h22" stroke="{INK}" stroke-width="8"/>'
             f'<path d="M-90,-262 Q0,-300 90,-262 L56,-262 Q0,-330 -56,-262 Z" fill="#3A3A44" stroke="{INK}" stroke-width="5"/>'
             f'<path d="M-30,-218 Q0,-140 30,-218" fill="#D9D3C7" stroke="{INK}" stroke-width="4"/>'
             f'<path d="M70,-170 L150,60" stroke="{INK}" stroke-width="12"/><path d="M70,-170 L150,60" stroke="#C9A25A" stroke-width="5"/>'
             f'<path d="M150,60 l-6,40 l18,-34 z" fill="#C3CCD3" stroke="{INK}" stroke-width="4"/>'
             f'<path d="M-140,-280 q20,-20 40,-4 q20,-16 40,4 q-20,0 -40,10 q-20,-10 -40,-10 Z" fill="{INK}"/><path d="M100,-300 q20,-20 40,-4 q20,-16 40,4 q-20,0 -40,10 q-20,-10 -40,-10 Z" fill="{INK}"/></g>', 340, 460, ax=160, ay=330)
    return base, king, odin

def tapestry(c, x):
    t = x.t; base, king, odin = tapestry_sprites()
    fill(c, "#2A1C14")
    z = 1.0 + 0.05 * ease_io(lin(t, 0, x.dur)); sw = 2.0 * math.sin(t * 0.9)
    with cam(c, z, W/2, H/2 + 10, rot=sw * 0.15):
        draw(c, base, W/2, H/2 + 10)
        kx, ky = W/2 + 1040 - 800, H/2 + 10 + 640 - 470
        t2 = x.c(2)
        # Odin iner
        oy = -300 + 900 * ease_out(lin(t, t2, t2 + 1.0))
        fall = ease_in(lin(t, t2 + 1.0, t2 + 1.5)) * 80
        draw(c, king, kx, ky, 1.0, rot=fall)
        if t > t2 - 0.2:
            glow(c, kx - 40, oy - 120, 300, "#FFF2C0", 0.4)
            draw(c, odin, kx - 170, oy, 0.95)
        impact(c, kx, ky - 120, t, t2 + 1.0, 130)
    if t > x.c(2) + 1.2:
        draw(c, label("ODİN", 66, rot=-4, sub="(bizzat)"), 520, 210, pop(t, x.c(2) + 1.2))
        arrow_at(c, t, x.c(2) + 1.3, 640, 260, 950, 420, 0.3)
    if t > x.c(0) + 0.3:
        draw(c, hand_label("baban", 56), 400, 900, pop(t, x.c(0) + 0.3)); arrow_at(c, t, x.c(0) + 0.4, 480, 870, 620, 760, -0.3)
    vignette(c, 0.55)

# ═══════════════════════════════ OCAK BAŞI
@lru_cache(None)
def hearth_scene_sprites():
    room = S(longhouse_interior(W + 200, H + 120) + grain(W + 200, H + 120), W + 200, H + 120)
    rug = S(f'<ellipse cx="300" cy="80" rx="290" ry="70" fill="#8A7A62" stroke="{INK}" stroke-width="5"/>' + "".join(f'<path d="M{20+k*30},{80+40*math.sin(k)} l-14,30" stroke="#6E604C" stroke-width="5"/>' for k in range(18)), 600, 170, ax=300, ay=80)
    dad_a = C("hring", pose="shrug", expr="happy", ss=1.2)
    dad_b = C("hring", pose="arms_up", expr="surprised", ss=1.2)
    kid_awake = C("child", "child", "sit", "happy", ss=1.2)
    kid_drowsy = C("child", "child", "sit", "sleepy", ss=1.2)
    zz = label("Zzz", 70, color="#CFE3FF")
    odin_bub = S(f'<g transform="translate(210,160)"><ellipse rx="190" ry="140" fill="#FFFDF5" stroke="{INK}" stroke-width="6"/>'
                 f'<circle cx="-150" cy="150" r="20" fill="#FFFDF5" stroke="{INK}" stroke-width="5"/><circle cx="-180" cy="196" r="12" fill="#FFFDF5" stroke="{INK}" stroke-width="4"/>'
                 f'<g transform="translate(-10,40) scale(0.48)"><path d="M-80,0 L-60,-200 Q0,-240 60,-200 L80,0 Z" fill="#2E3A4E" stroke="{INK}" stroke-width="8"/><circle cx="0" cy="-240" r="40" fill="#E9D6A0" stroke="{INK}" stroke-width="6"/>'
                 f'<path d="M-90,-262 Q0,-300 90,-262 L56,-262 Q0,-330 -56,-262 Z" fill="#3A3A44" stroke="{INK}" stroke-width="6"/><path d="M70,-170 L150,60" stroke="{INK}" stroke-width="14"/></g>'
                 f'<path d="M80,-60 l40,-20 M90,-20 l46,0 M80,20 l40,20" stroke="#E2B23A" stroke-width="8" stroke-linecap="round"/></g>', 420, 380)
    return room, rug, dad_a, dad_b, kid_awake, kid_drowsy, zz, odin_bub

def hearth_scene(c, x):
    t = x.t; room, rug, dad_a, dad_b, kid_a, kid_b, zz, bub = hearth_scene_sprites()
    t2 = x.c(2)
    z = 1.0 + 0.10 * ease_io(lin(t, x.c(1), x.c(2) + 0.6)); cx = W/2 + 150 * ease_io(lin(t, x.c(1), x.c(2) + 0.6))
    with cam(c, z, cx, H/2 + 60):
        draw(c, room, W/2, H/2 - 20)
        glow(c, W/2 - 120, 860, 750, "#FF9A40", 0.42 + 0.06*math.sin(t*6.3))
        draw(c, hearth_sp(), W/2 - 120, 930)
        draw(c, flame_sp(int(t * 8) % 6), W/2 - 120, 910)
        draw(c, rug, 1320, 1010)
        actor(c, dad_b if t > t2 else dad_a, 500, 1010, 1.05, t, ph=0.5)
        sleepy = t > x.c(1) + 0.6
        nod = 6 * math.sin(t * 2) if sleepy else 0
        actor(c, kid_b if sleepy else kid_a, 1320, 1012 + nod * 0.2, 1.15, t, ph=2.0)
        if t > t2: draw(c, bub, 760, 470, pop(t, t2, 0.4))
        if sleepy:
            for k in range(3):
                p = ((t - x.c(1)) * 0.6 + k * 0.33) % 1
                draw(c, zz, 1420 + p * 120, 600 - p * 220, 0.5 + p * 0.5, a=1 - p)
    Particles("ember", 40, seed=7, area=(500, 300, 1300, 950), color="#FFC070", speed=60).draw(c, t)
    vignette(c, 0.7)

# ═══════════════════════════════ BÜYÜME: KAPI PERVAZI
@lru_cache(None)
def growup_sprites():
    room = S(f'<rect width="{W}" height="{H}" fill="#6E4E34"/>' + "".join(f'<rect x="{x}" y="0" width="140" height="{H}" fill="{shade("#6E4E34", 1.0 if (x//140)%2 else 0.93)}" stroke="#3A2414" stroke-width="4"/>' for x in range(0, W, 140))
             + f'<rect y="{H-150}" width="{W}" height="150" fill="#3A2818"/>'
             + f'<rect x="300" y="60" width="120" height="{H-200}" fill="#8C6440" stroke="{INK}" stroke-width="6"/>'
             + "".join(f'<path d="M300,{H-150 - k*90} h40" stroke="#3A2414" stroke-width="4"/>' for k in range(1, 10)) + grain(W, H))
    kids = [C("child", "child", "hips", "happy", ss=1.0), C("teen", "teen", "hips", "smug", ss=1.0, crown=False, cloak=None, fur_collar=None),
            C("ragnar", "adult", "hips", "smug", ss=1.0)]
    marks = [S(f'<path d="M0,10 h70" stroke="#F6E2B0" stroke-width="7" stroke-linecap="round"/><text x="78" y="22" font-family="Caveat Brush" font-size="44" fill="#F6E2B0">{a}</text>', 200, 40, ax=0, ay=10)
             for a in ("6", "12", "18")]
    labs = [label("İRİ", 84, rot=-5), label("YAKIŞIKLI", 78, rot=4), label("AKILLI", 78, rot=-3)]
    card = S(scroll_frame(760, 250) + f'<text x="380" y="98" font-family="Alegreya SC" font-weight="bold" font-size="46" fill="{INK}" text-anchor="middle">Adamlarına: <tspan fill="#2E7D3A">İYİ</tspan></text>'
             f'<text x="380" y="178" font-family="Alegreya SC" font-weight="bold" font-size="46" fill="{INK}" text-anchor="middle">Düşmanlarına: <tspan fill="#B8322A">ACIMASIZ</tspan></text>', 840, 330, ax=40, ay=40)
    return room, kids, marks, labs, card

def growup(c, x):
    t = x.t; room, kids, marks, labs, card = growup_sprites()
    t0, t1 = x.c(0), x.c(1)
    seg = (t1 - t0) / 3
    stage = 0 if t < t0 + seg else 1 if t < t0 + 2*seg else 2
    with cam(c, 1.0 + 0.02*ease_io(lin(t, 0, x.dur)), W/2, H/2):
        draw(c, room, W/2, H/2)
        heights = [H - 150 - 340, H - 150 - 470, H - 150 - 560]
        for k in range(stage + 1):
            draw(c, marks[k], 300, heights[k] + 30, 1.0, a=1 if k < stage else fade(t, t0 + k*seg, 0.2))
        sp = kids[stage]; sc = [1.0, 1.0, 1.0][stage]
        k = pop(t, t0 + stage * seg, 0.3) if stage else 1
        actor(c, sp, 620, H - 150, sc * (0.85 + 0.15 * k), t)
    xs = [(1250, 300), (1450, 470), (1260, 640)]
    for i in range(3):
        ti = x.c(1 + i)
        if t > ti:
            draw(c, labs[i], xs[i][0], xs[i][1], pop(t, ti))
    arrow_at(c, t, x.c(1) + 0.1, 1120, 310, 760, 420, -0.25)
    arrow_at(c, t, x.c(2) + 0.1, 1260, 480, 720, 380, 0.25)
    arrow_at(c, t, x.c(3) + 0.1, 1100, 650, 700, 300, -0.3)
    if t > x.c(4): draw(c, card, 1150, 790, pop(t, x.c(4)) * 0.9)
    vignette(c, 0.5)

# ═══════════════════════════════ HARİTA ÇÖZÜLÜYOR
@lru_cache(None)
def map_sprites():
    m = S(map_vellum(W, H) + land(BRITAIN) + land(FRANCE) + land(JUTLAND, "#E2C27A") + land(SCANDI, "#E2C27A")
          + f'<path d="{SCANDI}" fill="none" stroke="#B8322A" stroke-width="10" stroke-dasharray="20 12"/>'
          + '<text x="1310" y="330" font-family="Cinzel" font-weight="700" font-size="44" fill="#6B2A1E" text-anchor="middle">HRING\'İN</text>'
          + '<text x="1310" y="380" font-family="Cinzel" font-weight="700" font-size="44" fill="#6B2A1E" text-anchor="middle">KRALLIĞI</text>' + grain(W, H))
    rnd = random.Random(9); pieces = []
    for k in range(9):
        cx, cy = rnd.uniform(1150, 1500), rnd.uniform(160, 640)
        pts = [(cx + 40*math.cos(a) * rnd.uniform(0.6, 1.2), cy + 40*math.sin(a) * rnd.uniform(0.6, 1.2)) for a in [i*1.2566 for i in range(5)]]
        pieces.append((S(f'<polygon points="{" ".join(f"{px-cx+60:.0f},{py-cy+60:.0f}" for px, py in pts)}" fill="#E2C27A" stroke="#6B5432" stroke-width="5"/>', 120, 120), cx, cy))
    hole = S(f'<rect width="{W}" height="{H}" fill="none"/>', W, H)
    oldking = C("hring", pose="stand", expr="sad", ss=1.0)
    return m, pieces, oldking

def map_crumble(c, x):
    t = x.t; m, pieces, oldk = map_sprites()
    z = 1.0 + 0.05*ease_io(lin(t, 0, x.dur))
    with cam(c, z, W/2 + 80, H/2):
        draw(c, m, W/2, H/2)
        t1 = x.c(1)
        for i, (sp, cx, cy) in enumerate(pieces):
            st = t1 + i * 0.25
            if t > st:
                p = t - st; ang = math.atan2(cy - 400, cx - 1310)
                draw(c, sp, cx + math.cos(ang) * p * 160, cy + math.sin(ang) * p * 160 + p*p*60, 1.0, rot=p * 60 * (1 if i % 2 else -1), a=clamp(1.4 - p * 0.5))
            else:
                draw(c, sp, cx, cy)
    actor(c, oldk, 300, 1060, 0.85 + 0.0*t, t)
    if t < x.c(1) + 0.5:
        draw(c, hand_label("baban (yaşlı)", 52), 340, 380, pop(t, x.c(0) + 0.2))
    vignette(c, 0.45)

# ═══════════════════════════════ 15 YAŞINDA TAHT
@lru_cache(None)
def throne_sprites():
    room = S(longhouse_interior(W + 200, H + 120, night=False) + grain(W + 200, H + 120), W + 200, H + 120)
    th = S(f'<g transform="translate(400,900)"><rect x="-260" y="-880" width="520" height="880" rx="30" fill="#6B4222" stroke="{INK}" stroke-width="8"/>'
           f'<rect x="-210" y="-830" width="420" height="440" rx="20" fill="#8E2A2A" stroke="{INK}" stroke-width="6"/>'
           f'<path d="M-260,-880 Q-300,-940 -240,-960 Q-200,-920 -220,-880 Z M260,-880 Q300,-940 240,-960 Q200,-920 220,-880 Z" fill="#C9A25A" stroke="{INK}" stroke-width="6"/>'
           f'<rect x="-300" y="-380" width="600" height="120" rx="16" fill="#7A4E2C" stroke="{INK}" stroke-width="7"/>'
           f'<rect x="-300" y="-270" width="70" height="270" fill="#5A3818" stroke="{INK}" stroke-width="6"/><rect x="230" y="-270" width="70" height="270" fill="#5A3818" stroke="{INK}" stroke-width="6"/></g>', 800, 960, ax=400, ay=900)
    teen = C("teen", "teen", "sit", "surprised", ss=1.1, crown=False)
    teen2 = C("teen", "teen", "sit", "determined", ss=1.1, crown=False)
    crw = S(crown(110, 90, 1.25), 220, 140)
    fifteen = label("15", 150, font="Cinzel Decorative", color="#F6ECD4", sw=14)
    neighbor = C("herraud", pose="hips", expr="smug", ss=1.0)
    nb2 = C("aella", pose="cross", expr="smug", ss=1.0)
    bub = S(f'<g transform="translate(170,130)"><ellipse rx="150" ry="110" fill="#FFFDF5" stroke="{INK}" stroke-width="6"/>'
            f'<circle cx="-120" cy="120" r="16" fill="#FFFDF5" stroke="{INK}" stroke-width="5"/>'
            f'<g transform="translate(-60,-40) scale(0.18)"><path d="{SCANDI}" transform="translate(-1150,-120)" fill="#E2C27A" stroke="{INK}" stroke-width="20"/></g>'
            f'<text x="50" y="40" font-family="Luckiest Guy" font-size="64" fill="#2E7D3A">$</text></g>', 340, 280)
    return room, th, teen, teen2, crw, fifteen, neighbor, nb2, bub

def teen_throne(c, x):
    t = x.t; room, th, teen, teen2, crw, fifteen, nb, nb2, bub = throne_sprites()
    t3 = x.c(3)
    z = 1.12 - 0.12 * ease_io(lin(t, x.c(3) - 0.4, x.c(3) + 0.6))
    with cam(c, z, W/2, H/2 + 40):
        draw(c, room, W/2, H/2 - 20)
        draw(c, th, W/2, 1040)
        swing = 10 * math.sin(t * 4)
        actor(c, teen2 if t > x.c(2) else teen, W/2, 1040 - 390 + 160, 1.0, t)
        # büyük taç kayıyor
        slip = ease_in(lin(t, x.c(2), x.c(2) + 0.8))
        draw(c, crw, W/2 + 6 + slip * 10, 350 + slip * 70, 1.0, rot=10 + slip * 18)
        if t > t3:
            p = ease_out(lin(t, t3, t3 + 0.7))
            actor(c, nb, -120 + 380 * p, 1060, 0.9, t)
            actor(c, nb2, W + 120 - 380 * p, 1060, 0.9, t, ph=1)
        if t > x.c(4):
            draw(c, bub, 420, 300, pop(t, x.c(4))); draw(c, bub, W - 420, 300, pop(t, x.c(4) + 0.15))
    if x.c(1) < t < x.c(3):
        draw(c, fifteen, 1450, 330, pop(t, x.c(1)))
        draw(c, hand_label("yaşında", 50), 1460, 450, pop(t, x.c(1) + 0.15))
    if x.c(0) + 0.6 < t < x.c(1):
        draw(c, hand_label("ayaklar: yere değmiyor", 50), 1350, 860, pop(t, x.c(0) + 0.6)); arrow_at(c, t, x.c(0) + 0.7, 1150, 860, 1010, 900, 0.3)
    vignette(c, 0.5)

# ═══════════════════════════════ II · FRØ
@lru_cache(None)
def fro_sprites():
    bg = S(f'<rect width="{W}" height="{H}" fill="#3A2A22"/>' + "".join(f'<rect x="{x}" y="0" width="160" height="{H}" fill="{shade("#3A2A22", 1.0 if (x//160)%2 else 0.9)}"/>' for x in range(0, W, 160)) + grain(W, H))
    def portrait(spec_name, expr, plate, extra=""):
        inner = f'<rect width="420" height="520" fill="#C9B48A"/><g transform="translate(210,608) scale(1.0)">{character(dict(CAST[spec_name]), "adult", "cross", expr)}</g>{extra}'
        return S(frame_portrait(420, 520, inner, plate), 480, 640, ax=240, ay=280)
    fro = portrait("aella", "smug", "FRØ · İSVEÇ", "")
    siw = portrait("hring", "neutral", "SIWARD · DEDEN")
    xmark = S(f'<path d="M30,30 L390,490 M390,30 L30,490" stroke="#B8322A" stroke-width="26" stroke-linecap="round" opacity="0.9"/>', 420, 520)
    women = S(f'<rect width="1200" height="260" fill="none"/>' + "".join(
        f'<g transform="translate({150+k*230},250) scale(0.42)">{character(dict(THORA, tunic=["#6E5844","#5A4E6E","#4E6A5A","#7A5A44","#5A5A5A"][k], hair=["#B5532E","#2C2420","#E3C27A","#7A5232","#C9A060"][k]), "adult", "hold_front", "sad")}</g>' for k in range(5)), 1200, 280)
    return bg, fro, siw, xmark, women

def frost_banner(c, x):
    t = x.t; bg, fro, siw, xm, women = fro_sprites()
    draw(c, bg, W/2, H/2)
    with cam(c, 1.0 + 0.04*ease_io(lin(t, 0, x.dur)), W/2, H/2):
        draw(c, siw, 560, 470, 0.95, rot=-3)
        if t > x.c(1) + 0.9: draw(c, xm, 560, 470, 0.95 * pop(t, x.c(1) + 0.9, 0.25), rot=-3)
        draw(c, fro, 1360, 470, 0.95 * (pop(t, x.c(1) - 0.1) if t < x.c(1) + 0.4 else 1), rot=3)
        if t > x.c(2): draw(c, women, W/2, 930, pop(t, x.c(2)) * 0.9)
    if t > x.c(1) + 0.3:
        draw(c, label("KÖTÜ ADAM", 62, color="#FF6A5A", rot=6), 1560, 150, pop(t, x.c(1) + 0.3)); arrow_at(c, t, x.c(1) + 0.4, 1560, 200, 1460, 300, 0.2)
    vignette(c, 0.6)

# ═══════════════════════════════ ORDU + KADINLAR
@lru_cache(None)
def army_sprites():
    land_ = S(sky(W, H, "#8FA8BE", "#D9D2C2") + clouds(W, 180, "#EEF0EE", 6, 3) + mountains(W, 640, "#7D8E9E", seed=8) + pines(W, 720, "#3E5A4E", 40, 2)
              + ground(W, H, 760, "#6E7E52", "#5E6E46") + grain(W, H))
    rag = C("ragnar", pose="one_up", expr="determined", props=("sword",), ss=1.1)
    w1 = C("warrior", pose="spear", props=("spear",), expr="angry")
    women = [C("woman", pose="spear", props=("shield", "spear"), expr="determined", hair=h, tunic=tc) for h, tc in (("#C9A060", "#5A5048"), ("#2C2420", "#4A5A6A"), ("#B5532E", "#5A4A3A"), ("#E3C27A", "#4E5A44"))]
    lab = label("KILIK: ERKEK", 60, rot=-4)
    return land_, rag, w1, women, lab

def army_women(c, x):
    t = x.t; land_, rag, w1, women, lab = army_sprites()
    with cam(c, 1.02 + 0.03*ease_io(lin(t, 0, x.dur)), W/2, H/2):
        draw(c, land_, W/2, H/2)
        for k in range(6):
            actor(c, w1, 200 + k * 120, 830, 0.55, t, ph=k)
        tw = x.c(1)
        for k, sp in enumerate(women):
            p = ease_out(lin(t, tw + k * 0.18, tw + 0.9 + k * 0.18))
            actor(c, sp, W + 200 - (W + 200 - (1080 + k * 190)) * p, 930 + (k % 2) * 30, 0.78, t, ph=k*0.7)
        actor(c, rag, 640, 1010, 1.05, t)
    if t > x.c(2): draw(c, lab, 1380, 260, pop(t, x.c(2))); arrow_at(c, t, x.c(2) + 0.1, 1380, 320, 1300, 440, 0.2)
    vignette(c, 0.45)

# ═══════════════════════════════ LAGERTHA KAHRAMAN ÇEKİMİ
@lru_cache(None)
def lag_sprites():
    bg = S(sky(W, H, "#4A3A5A", "#D98A5A", "#F2C27A") + clouds(W, 260, "#7A5A6A", 8, 5, 1.3, 0.8) + mountains(W, 760, "#3A3448", seed=11)
           + ground(W, H, 860, "#2E2A36", "#24202C") + grain(W, H))
    lag = C("lagertha", pose="shield", expr="determined", props=("shield", "sword"), ss=1.5)
    sil = S("".join(f'<g transform="translate({80+k*150},{300 + (k%3)*10}) scale(0.5)" opacity="0.85">{character(dict(WARRIOR, tunic="#1E1A24", skin="#1E1A24", hair="#1E1A24", beard_c="#1E1A24", trim="#1E1A24", pants="#1E1A24", boots="#1E1A24", belt="#1E1A24"), "adult", "spear", "neutral", props=("spear",))}</g>' for k in range(13)), W, 340, ay=300)
    name = label("Lagertha", 150, font="Pirata One", color="#F6ECD4", sw=12)
    return bg, lag, sil, name

def lagertha_hero(c, x):
    t = x.t; bg, lag, sil, name = lag_sprites()
    z = 1.18 - 0.14 * ease_io(lin(t, 0, x.dur))
    with cam(c, z, W/2, H/2 + 40):
        draw(c, bg, W/2, H/2)
        rays(c, W/2 + 200, 520, 200, 1400, 70, 7, "#FFE0A0", 0.12, t)
        draw(c, sil, W/2 - 60 * t * 0.2, 900)
        glow(c, W/2, 640, 520, "#FFC27A", 0.22)
        actor(c, lag, W/2 + 40, 1050, 1.15, t, breathe=0.008)
    Particles("dust", 60, seed=4, color="#FFE0B0", speed=80).draw(c, t)
    if t > x.c(2):
        draw(c, name, W/2, 220, pop(t, x.c(2), 0.4) * 1.0)
    if x.c(1) < t < x.c(2):
        draw(c, hand_label("savaşı çeviren", 56), 1500, 330, pop(t, x.c(1))); arrow_at(c, t, x.c(1) + 0.1, 1450, 380, 1160, 500, -0.2)
    vignette(c, 0.55)

# ═══════════════════════════════ LAGERTHA'NIN EVİ
@lru_cache(None)
def lhouse_sprites():
    bg = S(sky(W, H, "#5A6E8E", "#E7B08A") + mountains(W, 620, "#4E5E6E", seed=12) + pines(W, 700, "#2E4A3E", 30, 9)
           + ground(W, H, 760, "#5E6E46", "#4E5E3A")
           + f'<g transform="translate(1250,860)"><rect x="-300" y="-260" width="600" height="260" fill="#8C6239" stroke="{INK}" stroke-width="7"/>'
             f'<path d="M-340,-240 L0,-470 L340,-240 Z" fill="#5E4A2E" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
             f'<path d="M-40,-470 l-34,-46 M40,-470 l34,-46" stroke="{INK}" stroke-width="10" stroke-linecap="round"/>'
             f'<rect x="-60" y="-170" width="120" height="170" rx="8" fill="#3A2414" stroke="{INK}" stroke-width="6"/>'
             f'<rect x="150" y="-200" width="100" height="80" fill="#F6C46A" stroke="{INK}" stroke-width="6"/></g>' + grain(W, H))
    rag = C("ragnar", pose="hold_front", expr="smitten", ss=1.1)
    lagw = C("lagertha", pose="wave", expr="smug", ss=0.8)
    b = S(f'<g transform="translate(200,320)">{bear()}</g>', 400, 340, ax=200, ay=320, ss=1.2)
    d = S(f'<g transform="translate(200,180)">{hound()}</g>', 400, 200, ax=200, ay=180, ss=1.2)
    chain = S('<path d="M0,0 q30,20 60,0 q30,-20 60,0 q30,20 60,0" stroke="#7F8A93" stroke-width="8" fill="none"/>', 200, 40, ax=0, ay=20)
    flowers = S(f'<g transform="translate(60,60)"><path d="M0,40 L0,-10 M-10,40 L-20,0 M10,40 L22,2" stroke="#3E6E4A" stroke-width="5"/>'
                + "".join(f'<circle cx="{x}" cy="{y}" r="12" fill="{cc}" stroke="{INK}" stroke-width="3"/>' for x, y, cc in ((0, -16, "#E07FA0"), (-22, -4, "#F2C230"), (22, -2, "#7FA8E0"))) + '</g>', 120, 120)
    lab = label("KAPI GÖREVLİLERİ", 58, rot=-3)
    return bg, rag, lagw, b, d, chain, flowers, lab

def lagertha_house(c, x):
    t = x.t; bg, rag, lagw, b, d, chain, flowers, lab = lhouse_sprites()
    t2 = x.c(2)
    z = 1.0 + 0.35 * ease_io(lin(t, t2, t2 + 0.8)); cx = W/2 + 340 * ease_io(lin(t, t2, t2 + 0.8)); cy = H/2 + 120 * ease_io(lin(t, t2, t2 + 0.8))
    with cam(c, z, cx, cy):
        draw(c, bg, W/2, H/2)
        if t > x.c(1): actor(c, lagw, 1640, 1010, 0.8 * pop(t, x.c(1)), t, ph=2)
        actor(c, rag, 480 + 120 * ease_io(lin(t, 0, x.c(2))), 1020, 0.9, t)
        draw(c, flowers, 560 + 120 * ease_io(lin(t, 0, x.c(2))), 830, 0.9)
        if t > t2 - 0.2:
            draw(c, b, 1060, 880, 0.9 * pop(t, t2 - 0.2, 0.35)); draw(c, d, 1440, 880, 0.8 * pop(t, t2, 0.35))
    if t > t2 + 0.8: draw(c, lab, W/2, 180, pop(t, t2 + 0.8))
    if t > x.c(0) + 0.2 and t < x.c(2):
        draw(c, S(f'<g transform="translate(60,60)"><path d="M0,40 C-70,-10 -50,-60 0,-30 C50,-60 70,-10 0,40 Z" fill="#E0483C" stroke="{INK}" stroke-width="5"/></g>', 120, 110), 600 + 120 * ease_io(lin(t, 0, x.c(2))), 380 - 30 * math.sin(t*3), pop(t, x.c(0) + 0.2))
    vignette(c, 0.5)

@lru_cache(None)
def after_sprites():
    bg = S(sky(W, H, "#E9D6B0", "#F2E6CC") + grain(W, H))
    rag = C("ragnar", pose="thrust", expr="determined", props=("thrust",), ss=1.0)
    bd = S(f'<g transform="translate(200,320) rotate(-70 0 -100)">{bear()}</g><path d="M60,120 l30,30 m0,-30 l-30,30 M110,110 l30,30 m0,-30 l-30,30" stroke="{INK}" stroke-width="7"/>', 400, 400, ax=200, ay=320)
    hd = S(f'<g transform="translate(220,180) scale(1,-1) translate(0,140)">{hound()}</g>', 440, 260, ax=220, ay=180)
    wed = S(frame_portrait(560, 440, f'<rect width="560" height="440" fill="#D9C79E"/><g transform="translate(170,491) scale(0.75)">{character(dict(RAGNAR), "adult", "hold_front", "smitten")}</g>'
                           f'<g transform="translate(390,491) scale(0.75)">{character(dict(LAGERTHA), "adult", "hold_front", "happy", facing=-1)}</g>', "EVLİLİK"), 620, 560, ax=310, ay=260)
    crack = S('<path d="M300,0 L270,90 L330,170 L280,260 L340,350 L300,460" stroke="#1A120C" stroke-width="12" fill="none" stroke-linejoin="round"/>', 600, 480, ax=300, ay=240)
    kids = [S(f'<g transform="translate(110,300) scale(0.75)">{character(dict(RAGNAR_CHILD, **kw), "child", "wave", "happy")}</g>', 220, 320, ax=110, ay=300)
            for kw in (dict(), dict(hair="#EFD37A", hair_style="long", tunic="#3B6B6B"), dict(hair="#E3C27A", hair_style="long", tunic="#7A5A8A"))]
    labs = [label("+1 OĞUL", 46), label("+2 KIZ", 46)]
    return bg, rag, bd, hd, wed, crack, kids, labs

def lagertha_after(c, x):
    t = x.t; bg, rag, bd, hd, wed, crack, kids, labs = after_sprites()
    draw(c, bg, W/2, H/2)
    if t < x.c(1):
        with cam(c, 1.06, W/2, H/2):
            speedlines(c, 1100, 600, t, 0.35)
            actor(c, rag, 640, 1030, 1.0, t)
            draw(c, bd, 1280, 980, 1.0, rot=10 * ease_out(lin(t, 0.4, 0.8)))
            draw(c, hd, 1650, 1010, 0.8)
            impact(c, 1100, 620, t, 0.35, 150)
            draw(c, label("× ×", 70, color="#FFFFFF"), 1300, 380, pop(t, 0.6))
    else:
        with cam(c, 1.0 + 0.04*ease_io(lin(t, x.c(1), x.dur)), W/2, H/2):
            draw(c, wed, W/2, 480, pop(t, x.c(1), 0.3))
            for k in range(3):
                if t > x.c(2) + k * 0.2: draw(c, kids[k], 650 + k * 310, 1030, pop(t, x.c(2) + k * 0.2) * 0.85)
            if t > x.c(3) + 0.6:
                draw(c, crack, W/2, 480, 1.0, a=fade(t, x.c(3) + 0.6, 0.15)); flash(c, t, x.c(3) + 0.6, 0.15, "#000000")
                draw(c, label("AYIDAN ZOR", 64, color="#FFD27A", rot=-6), 1500, 180, pop(t, x.c(3) + 0.7))
    vignette(c, 0.4)
