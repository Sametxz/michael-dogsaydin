import math, random
from functools import lru_cache
import skia
from engine import *
from art2 import *
from bg import *
from scenes_a import C, CAST, actor, cam, S, popdraw, arrow_at, impact, speedlines, flash, hearth_sp, flame_sp

def heart_sp():
    return S(f'<g transform="translate(60,60)"><path d="M0,40 C-70,-10 -50,-60 0,-30 C50,-60 70,-10 0,40 Z" fill="#E0483C" stroke="{INK}" stroke-width="5"/><path d="M-30,-20 q10,-10 20,0" stroke="#fff" stroke-width="5" fill="none" opacity="0.7"/></g>', 120, 110)

def bubble_sp(inner, w=360, h=260, tail="left"):
    tx = -w*0.32 if tail == "left" else w*0.32
    return S(f'<g transform="translate({w/2+20},{h/2+10})"><path d="M{tx},{h*0.32} L{tx*1.25},{h*0.62} L{tx*0.6},{h*0.36} Z" fill="#FFFDF5" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
             f'<rect x="{-w/2}" y="{-h/2}" width="{w}" height="{h*0.8}" rx="40" fill="#FFFDF5" stroke="{INK}" stroke-width="6"/>'
             f'<path d="M{tx*0.9},{h*0.28} L{tx*0.65},{h*0.28}" stroke="#FFFDF5" stroke-width="10"/>{inner}</g>', w + 40, h + 40)

# ═══════════════════════════════ III · HEDİYE YILAN
@lru_cache(None)
def hall_day():
    return S(longhouse_interior(W + 200, H + 120, night=False) + grain(W + 200, H + 120), W + 200, H + 120)

@lru_cache(None)
def gift_sprites():
    jarl = C("herraud", pose="give", expr="happy", ss=1.1)
    thora = C("thora", pose="hold_front", expr="happy", facing=-1, ss=1.1)
    thora2 = C("thora", pose="hold_front", expr="surprised", facing=-1, ss=1.1)
    box_closed = S(f'<g transform="translate(130,170)"><rect x="-100" y="-90" width="200" height="110" rx="10" fill="#B8322A" stroke="{INK}" stroke-width="6"/>'
                   f'<rect x="-110" y="-120" width="220" height="40" rx="8" fill="#C9443A" stroke="{INK}" stroke-width="6"/><rect x="-14" y="-120" width="28" height="140" fill="#E2B23A" stroke="{INK}" stroke-width="4"/>'
                   f'<path d="M0,-120 q-50,-60 -60,-10 q30,10 60,10 q30,0 60,-10 q-10,-50 -60,10" fill="#E2B23A" stroke="{INK}" stroke-width="5"/></g>', 260, 200, ay=170)
    box_open = S(f'<g transform="translate(130,170)"><path d="M-110,-90 L-140,-170 L80,-150 L110,-90 Z" fill="#C9443A" stroke="{INK}" stroke-width="6"/>'
                 f'<g transform="translate(0,-90)">{coins_pile(18, 7, 180, 50)}</g>'
                 f'{serpent_body([(-40,-90),(-10,-120),(30,-100),(10,-140)], w=26, c="#7FB04A")}{serpent_head(10,-150,0.42,-30,c="#7FB04A",cute=True)}'
                 f'<rect x="-100" y="-90" width="200" height="110" rx="10" fill="#B8322A" stroke="{INK}" stroke-width="6"/><rect x="-14" y="-90" width="28" height="110" fill="#E2B23A" stroke="{INK}" stroke-width="4"/></g>', 260, 260, ay=230)
    return jarl, thora, thora2, box_closed, box_open

def gift_snake(c, x):
    t = x.t; jarl, thora, thora2, bc, bo = gift_sprites()
    t1, t2 = x.c(1), x.c(2)
    z = 1.0 + 0.25 * ease_io(lin(t, t2 - 0.3, t2 + 0.6)); cy = H/2 + 120 * ease_io(lin(t, t2 - 0.3, t2 + 0.6))
    with cam(c, z, W/2, cy):
        draw(c, hall_day(), W/2, H/2 - 20)
        actor(c, jarl, 640, 1030, 1.0, t)
        actor(c, thora2 if t > t1 + 0.6 else thora, 1300, 1030, 1.0, t, ph=1)
        bx = 900 + 120 * ease_io(lin(t, t1 - 0.3, t1 + 0.3))
        draw(c, bo if t > t1 + 0.5 else bc, bx + 60, 740, 1.0 + 0.08 * pop(t, t1 + 0.5))
    if t > t1 + 0.7: draw(c, label("BEDAVA YILAN", 58, rot=-4), 760, 220, pop(t, t1 + 0.7))
    if t > t2 + 0.5:
        draw(c, hand_label("altın yatak", 54), 1000, 330, pop(t, t2 + 0.5)); arrow_at(c, t, t2 + 0.6, 1000, 380, 1010, 540, 0.25)
    vignette(c, 0.4)

@lru_cache(None)
def grow_sprites():
    room = S(f'<rect width="{W}" height="{H}" fill="#7A5638"/>' + "".join(f'<rect x="{x}" y="0" width="120" height="{H}" fill="{shade("#7A5638", 1.0 if (x//120)%2 else 0.92)}" stroke="#3A2414" stroke-width="4"/>' for x in range(0, W, 120))
             + f'<rect y="{H-160}" width="{W}" height="160" fill="#3A2818"/>' + grain(W, H))
    gold = S(f'<g transform="translate(300,140)">{coins_pile(70, 3, 520, 160)}</g>', 600, 180, ay=140)
    snake = S(f'<g transform="translate(400,330)">{serpent_body([(-300,0),(-200,-60),(-80,10),(40,-70),(140,-10),(200,-90)], w=70, c="#5E8A3A")}{serpent_head(200,-110,1.0,-20,c="#5E8A3A",mouth_open=False)}</g>', 800, 420, ax=400, ay=330, ss=1.2)
    thora = C("thora", pose="shrug", expr="surprised", ss=1.0)
    tape = [label(s, 70 + i * 26, rot=(-6, 3, -2)[i], color=("#FFFFFF", "#FFE27A", "#FF7A5A")[i]) for i, s in enumerate(("büyüyor", "BÜYÜYOR", "BÜYÜYOR!"))]
    return room, gold, snake, thora, tape

def snake_grow(c, x):
    t = x.t; room, gold, snake, thora, tape = grow_sprites()
    stage = x.idx()
    targets = [0.35, 0.9, 2.2]
    prev = targets[stage - 1] if stage else 0.15
    k = prev + (targets[stage] - prev) * back(lin(t, x.c(stage), x.c(stage) + 0.45))
    shake = (6 * math.sin(t * 60) if (t - x.c(stage)) < 0.25 and stage > 0 else 0)
    with cam(c, 1.0, W/2 + shake, H/2):
        draw(c, room, W/2, H/2)
        draw(c, gold, 700, 940, 0.6 + 0.5 * k)
        draw(c, snake, 700, 900, k)
        actor(c, thora, 1540, 1000, 0.9, t)
    for i in range(stage + 1):
        draw(c, tape[i], 1400 - i * 60, 220 + i * 150, pop(t, x.c(i)))
    vignette(c, 0.45)

@lru_cache(None)
def bower_sprites():
    bg = S(sky(W, H, "#3E4A3A", "#9AA27A", "#C9C08A") + clouds(W, 200, "#6E7A5A", 6, 7, 1.2, 0.7) + pines(W, 760, "#2A3A2A", 30, 5, 200, 380)
           + ground(W, H, 820, "#4A5A36", "#3A4A2A")
           + f'<g transform="translate({W/2},860)"><rect x="-200" y="-420" width="400" height="420" fill="#8C6239" stroke="{INK}" stroke-width="7"/>'
             f'<path d="M-240,-400 L0,-640 L240,-400 Z" fill="#5E4A2E" stroke="{INK}" stroke-width="7"/><rect x="-60" y="-300" width="120" height="100" fill="#F6C46A" stroke="{INK}" stroke-width="6"/>'
             f'<rect x="-60" y="-140" width="120" height="140" rx="6" fill="#3A2414" stroke="{INK}" stroke-width="6"/></g>'
           + "".join(f'<g transform="translate({x},{820}) scale(0.8)"><path d="M0,0 L0,-120 M0,-60 L-40,-110 M0,-80 L36,-120" stroke="#3A2A1E" stroke-width="12" stroke-linecap="round"/></g>' for x in (260, 420, 1560, 1700)) + grain(W, H))
    coil_back = S(serpent_body([(W/2-260, 640), (W/2, 560), (W/2+260, 640)], w=90, c="#4E7A30"), W, H)
    coil_front = S(serpent_body([(W/2+300, 860), (W/2+260, 760), (W/2, 720), (W/2-260, 760), (W/2-320, 850), (W/2-480, 840), (W/2-560, 760)], w=96, c="#5E8A3A")
                   + serpent_head(W/2-600, 690, 1.25, -30, c="#5E8A3A", mouth_open=True), W, H, ss=1.0)
    jarl = C("herraud", pose="point", expr="determined", props=("scroll",), ss=1.0)
    decree = S(scroll_frame(560, 300) + f'<text x="280" y="90" font-family="Pirata One" font-size="60" fill="{INK}" text-anchor="middle">İlan</text>'
               f'<text x="280" y="160" font-family="Alegreya" font-weight="bold" font-size="38" fill="{INK}" text-anchor="middle">Yılanı öldüren,</text>'
               f'<text x="280" y="210" font-family="Alegreya" font-weight="bold" font-size="38" fill="{INK}" text-anchor="middle">kızımı alır.</text>'
               + f'<g transform="translate(450,250)">{stamp("JARL", "#7A2E8A", -14, 36)}</g>', 640, 380, ax=40 + 280, ay=40 + 150)
    return bg, coil_back, coil_front, jarl, decree

def bower_coil(c, x):
    t = x.t; bg, cb, cf, jarl, decree = bower_sprites()
    with cam(c, 1.05 - 0.05 * ease_io(lin(t, 0, x.dur)), W/2, H/2):
        draw(c, bg, W/2, H/2); draw(c, cb, W/2, H/2)
        glow(c, W/2, 800, 700, "#9AE07A", 0.18 + 0.05 * math.sin(t * 3))
        draw(c, cf, W/2, H/2 + 4 * math.sin(t * 1.8))
        if t > x.c(1): actor(c, jarl, 1620, 1060, 0.75, t)
    Particles("dust", 50, seed=8, color="#B8F08A", speed=30).draw(c, t, 0.7)
    if t > x.c(1) + 0.2: draw(c, decree, 1250, 300, pop(t, x.c(1) + 0.2) * 0.95, rot=-3)
    if t > x.c(0) + 0.6 and t < x.c(1):
        draw(c, label("ZEHİR", 64, color="#B8F08A", rot=5), 520, 300, pop(t, x.c(0) + 0.6)); arrow_at(c, t, x.c(0) + 0.7, 520, 360, 420, 560, -0.2, "#B8F08A")
    vignette(c, 0.6)

@lru_cache(None)
def recipe_sprites():
    bg = S(f'<rect width="{W}" height="{H}" fill="#3A2818"/>' + "".join(f'<rect x="0" y="{y}" width="{W}" height="90" fill="{shade("#5A3E26", 1.0 if (y//90)%2 else 0.9)}" stroke="#2A1A10" stroke-width="3"/>' for y in range(0, H, 90)) + grain(W, H))
    card = S(parchment(1500, 860) + rune_border(1500, 860, "#8C6B3E")
             + f'<text x="750" y="120" font-family="Pirata One" font-size="96" fill="#5A2018" text-anchor="middle">Kıllı Pantolon Tarifi</text>'
             + f'<path d="M420,150 H1080" stroke="#5A2018" stroke-width="4"/>', 1540, 900, ax=20, ay=20)
    steps = []
    icons = [
        f'<g transform="translate(150,170)">{fur_leg(-34,-120,-46,90,58,"#6B4A2E")}{fur_leg(34,-120,46,90,58,"#6B4A2E")}<rect x="-74" y="-140" width="148" height="34" rx="6" fill="#4A3020" stroke="{INK}" stroke-width="5"/>'
        f'<g transform="translate(110,-60) scale(0.7)"><path d="M-60,-80 L60,-80 L80,60 L-80,60 Z" fill="#7A5A3A" stroke="{INK}" stroke-width="6"/><path d="M-60,-80 L0,-110 L60,-80" fill="#7A5A3A" stroke="{INK}" stroke-width="6"/></g></g>',
        f'<g transform="translate(150,190)"><path d="M-110,-60 Q-120,80 0,90 Q120,80 110,-60 Z" fill="#2E2A26" stroke="{INK}" stroke-width="6"/><ellipse cx="0" cy="-60" rx="110" ry="30" fill="#1A1410" stroke="{INK}" stroke-width="6"/>'
        + "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#3A3430" stroke="{INK}" stroke-width="3"/>' for x, y, r in ((-40, -70, 14), (20, -76, 10), (50, -62, 16)))
        + f'<path d="M-60,100 l-20,40 M60,100 l20,40" stroke="{INK}" stroke-width="10"/><path d="M-50,140 q50,-60 100,0" fill="#F08A2A"/></g>',
        f'<g transform="translate(150,190)"><path d="M-90,-70 L90,-70 L70,90 L-70,90 Z" fill="#A8A29A" stroke="{INK}" stroke-width="6"/><ellipse cx="0" cy="-70" rx="90" ry="24" fill="#E3CC8A" stroke="{INK}" stroke-width="5"/>'
        + "".join(f'<circle cx="{x}" cy="{y}" r="4" fill="#B89A5A"/>' for x, y in ((-30, -74), (10, -66), (40, -78), (-60, -70), (60, -68))) + '</g>',
        f'<g transform="translate(150,190)"><rect x="-80" y="-80" width="160" height="160" rx="24" fill="#BFE6FF" stroke="{INK}" stroke-width="6" opacity="0.95"/><path d="M-50,-50 l30,0 M-50,-50 l0,30" stroke="#fff" stroke-width="10" stroke-linecap="round"/>'
        + "".join(f'<path d="M0,-40 V40 M-34,-20 L34,20 M-34,20 L34,-20" stroke="#5AA8E0" stroke-width="6" transform="translate({0},{0}) scale(0.6)"/>' for _ in range(1)) + '</g>',
    ]
    texts = ["1 · Kıllı pantolon", "2 · Katranda kaynat", "3 · Kuma bula", "+ Saxo: buz tuttur"]
    for i in range(4):
        steps.append(S(f'<g transform="translate(40,0)">{icons[i]}</g><text x="190" y="360" font-family="Alegreya" font-weight="bold" font-size="32" fill="{INK}" text-anchor="middle">{texts[i]}</text>', 380, 380))
    return bg, card, steps

def recipe(c, x):
    t = x.t; bg, card, steps = recipe_sprites()
    draw(c, bg, W/2, H/2)
    with cam(c, 1.0 + 0.03 * ease_io(lin(t, 0, x.dur)), W/2, H/2):
        draw(c, card, 210, 110, 1.0, a=fade(t, 0, 0.3))
        for i in range(4):
            ti = x.c(i + 1)
            if t > ti: draw(c, steps[i], 400 + i * 375, 620, pop(t, ti), rot=(-3, 2, -2, 4)[i])
    if t > x.c(4) + 0.4: draw(c, label("SAXO", 50, color="#BFE6FF", rot=8), 1640, 330, pop(t, x.c(4) + 0.4))
    vignette(c, 0.5)

@lru_cache(None)
def fight_sprites():
    bg = S(sky(W, H, "#3E3A5A", "#E79A6A", "#F6D08A") + clouds(W, 300, "#9A6A7A", 6, 9, 1.1, 0.7) + pines(W, 780, "#2A2A3A", 24, 6, 180, 320) + ground(W, H, 840, "#3A3A30", "#2E2E26") + grain(W, H))
    rag_walk = C("lod", pose="shield", expr="determined", props=("shield", "spear"), ss=1.2)
    rag_hit = C("lod", pose="shield", expr="surprised", props=("shield", "spear"), ss=1.2)
    body = S(serpent_body([(2100, 1000), (1900, 900), (1700, 960), (1560, 860), (1500, 700), (1520, 560)], w=110, c="#5E8A3A"), 2200, H, ax=1100, ay=H/2)
    headc = S(serpent_head(150, 150, 1.6, -15, c="#5E8A3A", mouth_open=False), 420, 300, ax=150, ay=150, ss=1.1)
    heado = S(serpent_head(150, 150, 1.6, -15, c="#5E8A3A", mouth_open=True), 420, 300, ax=150, ay=150, ss=1.1)
    goo = S('<path d="M20,40 Q60,0 100,30 Q130,60 90,80 Q60,100 30,80 Q0,60 20,40 Z" fill="#8FD05A" stroke="#2A4A1A" stroke-width="5"/>', 140, 120)
    tut = label("TUTTU ✓", 76, color="#B8F08A", rot=-5)
    return bg, rag_walk, rag_hit, body, headc, heado, goo, tut

def serpent_fight(c, x):
    t = x.t; bg, rw, rh, body, hc, ho, goo, tut = fight_sprites()
    t1, t2 = x.c(1), x.c(2)
    with cam(c, 1.0 + 0.06 * ease_io(lin(t, t1, t2)), W/2 + 80 * ease_io(lin(t, t1, t2)), H/2):
        draw(c, bg, W/2, H/2)
        rise = ease_out(lin(t, t1 - 0.4, t1 + 0.4))
        draw(c, body, W/2 + 180, H/2 + 140 - 140 * rise)
        hx, hy = 1520 + 200, 560 + 140 - 140 * rise
        draw(c, ho if t > t1 + 0.3 else hc, hx - 160, hy - 40, 1.0, rot=-6 * rise)
        rx = 300 + 420 * ease_io(lin(t, 0, t1))
        actor(c, rh if t > t1 + 0.9 else rw, rx, 1030, 0.95, t, bob=6 if t < t1 else 0)
        if t > t1 + 0.4:
            for k in range(6):
                p = lin(t, t1 + 0.4 + k * 0.08, t1 + 1.0 + k * 0.08)
                if 0 < p:
                    gx = (hx - 220) + (rx + 60 - (hx - 220)) * p; gy = hy + (880 - hy) * p - 220 * math.sin(p * math.pi)
                    draw(c, goo, gx + k * 14, gy + k * 10, 0.7 + 0.1 * k, a=1 if p < 1 else 0.85)
    if t > t2: draw(c, tut, 760, 300, pop(t, t2)); arrow_at(c, t, t2 + 0.1, 760, 360, 760, 760, 0.2, "#B8F08A")
    vignette(c, 0.55)

@lru_cache(None)
def kill_sprites():
    bg = S(sky(W, H, "#F6D08A", "#E79A6A") + grain(W, H))
    rag = C("lod", pose="thrust", expr="angry", props=("shield", "thrust"), ss=1.2)
    head_dead = S(serpent_head(150, 150, 2.0, 25, c="#5E8A3A", mouth_open=True) + '<path d="M180,90 l26,26 m0,-26 l-26,26" stroke="#2A1D14" stroke-width="8"/>', 460, 360, ax=150, ay=150, ss=1.1)
    body = S(serpent_body([(1300, 1100), (1450, 900), (1650, 780), (1900, 820)], w=130, c="#5E8A3A"), W, H)
    return bg, rag, head_dead, body

def serpent_kill(c, x):
    t = x.t; bg, rag, hd, body = kill_sprites()
    t1 = x.c(1)
    draw(c, bg, W/2, H/2)
    speedlines(c, 1150, 560, t, 0.45, 50, 380)
    sh = 10 * math.sin(t * 70) * (1 - lin(t, t1, t1 + 0.4)) if t > t1 else 0
    with cam(c, 1.12 - 0.08 * ease_out(lin(t, t1, t1 + 0.5)), W/2 + sh, H/2):
        draw(c, body, W/2, H/2)
        draw(c, hd, 1060, 560, 1.0, rot=12 * ease_out(lin(t, t1, t1 + 0.5)))
        lunge = 140 * ease_out(lin(t, t1 - 0.2, t1))
        actor(c, rag, 420 + lunge, 1050, 1.1, t)
        impact(c, 1000, 600, t, t1, 200)
    flash(c, t, t1, 0.18)
    vignette(c, 0.45)

@lru_cache(None)
def title_sprites():
    bg = S(longhouse_interior(W + 200, H + 120, night=True) + grain(W + 200, H + 120), W + 200, H + 120)
    rag = C("lod", pose="arms_up", expr="happy", ss=1.2)
    thora = C("thora", pose="hold_front", expr="smitten", facing=-1, ss=1.2)
    crowd = S("".join(f'<g transform="translate({90+k*170},{360 + (k%2)*20}) scale(0.55)">{character(dict(WARRIOR, helmet=False, tunic=["#5A4A3A","#4A5A6A","#6A4A3A","#3E5A4A"][k%4]), "adult", "arms_up", "happy")}</g>' for k in range(11)), W, 380, ay=360)
    plaque = S(f'<rect x="0" y="0" width="1100" height="300" rx="26" fill="#7A4E2C" stroke="{INK}" stroke-width="8"/>'
               + "".join(f'<path d="M10,{y} Q550,{y+14} 1090,{y}" stroke="#5E3A1E" stroke-width="4" fill="none"/>' for y in range(30, 300, 34))
               + f'<rect x="20" y="20" width="1060" height="260" rx="18" fill="none" stroke="#C9A25A" stroke-width="5"/>'
               + f'<text x="550" y="215" font-family="Pirata One" font-size="210" fill="#F2D27A" stroke="{INK}" stroke-width="8" paint-order="stroke" text-anchor="middle">Loðbrók</text>', 1100, 300, ss=1.2)
    sub = label("= KILLI PANTOLON", 68, color="#FFFFFF")
    return bg, rag, thora, crowd, plaque, sub

def lodbrok_title(c, x):
    t = x.t; bg, rag, thora, crowd, plaque, sub = title_sprites()
    with cam(c, 1.0 + 0.05 * ease_io(lin(t, 0, x.dur)), W/2, H/2 + 40):
        draw(c, bg, W/2, H/2 - 20)
        glow(c, W/2, 700, 800, "#FFB35A", 0.25)
        if t > x.c(1) - 0.3: draw(c, crowd, W/2, 1110 + 30 * math.sin(t * 8) * fade(t, x.c(1) - 0.3, 0.3) * 0.3, 1.0, a=fade(t, x.c(1) - 0.3))
        actor(c, rag, 820, 1050, 1.0, t, bob=8 if t > x.c(1) else 0)
        actor(c, thora, 1150, 1050, 0.95, t, ph=1)
    if t > x.c(2): draw(c, plaque, W/2, 230 - 80 * (1 - ease_out(lin(t, x.c(2), x.c(2) + 0.3))), 1.0 * (0.9 + 0.1 * pop(t, x.c(2))), a=fade(t, x.c(2), 0.15))
    if t > x.c(3): draw(c, sub, W/2 + 260, 440, pop(t, x.c(3))); arrow_at(c, t, x.c(3) + 0.15, 1330, 480, 900, 860, 0.25)
    vignette(c, 0.55)

# ═══════════════════════════════ IV · KRÁKA
@lru_cache(None)
def loss_sprites():
    bg = S(f'<rect width="{W}" height="{H}" fill="#1C2230"/>' + f'<rect x="{W/2-260}" y="160" width="520" height="560" fill="#2A3346" stroke="#0E121A" stroke-width="12"/>'
           + f'<path d="M{W/2},160 V720 M{W/2-260},440 H{W/2+260}" stroke="#0E121A" stroke-width="12"/>' + clouds(W, 300, "#3A4458", 3, 4, 0.8, 0.5).replace("translate(", "translate(") + grain(W, H))
    candle = S(f'<rect x="40" y="60" width="40" height="120" rx="6" fill="#E9DCC0" stroke="{INK}" stroke-width="5"/><rect x="20" y="170" width="80" height="16" rx="6" fill="#7A5A3A" stroke="{INK}" stroke-width="4"/>', 120, 200, ay=60)
    flame_ = S('<path d="M30,60 Q10,30 30,0 Q50,30 30,60 Z" fill="#FFC64A"/><path d="M30,56 Q22,40 30,24 Q38,40 30,56 Z" fill="#FFF2B0"/>', 60, 64, ay=60)
    smoke = S('<path d="M20,100 q-20,-25 0,-50 q20,-25 0,-50" stroke="#9AA4B0" stroke-width="8" fill="none" stroke-linecap="round" opacity="0.6"/>', 40, 110, ay=100)
    boys = [C("child", "child", "stand", "sad", tunic="#3E5A6A", hair=h) for h in ("#B5532E", "#D9B060")]
    return bg, candle, flame_, smoke, boys

def thora_loss(c, x):
    t = x.t; bg, candle, fl, smoke, boys = loss_sprites()
    t1 = x.c(1); out = t > t1 + 0.9
    with cam(c, 1.0 + 0.05 * ease_io(lin(t, 0, x.dur)), W/2, H/2):
        draw(c, bg, W/2, H/2)
        draw(c, candle, W/2, 820, 1.4)
        if not out:
            glow(c, W/2, 770, 380, "#FFB35A", 0.4 * (1 - 0.3 * math.sin(t * 9)))
            draw(c, fl, W/2, 770, 1.4 * (1 + 0.06 * math.sin(t * 11)))
        else:
            p = lin(t, t1 + 0.9, t1 + 2.5); draw(c, smoke, W/2, 760 - p * 80, 1.4, a=1 - p)
        for k, b_ in enumerate(boys):
            if t > 0.3 + k * 0.3: actor(c, b_, 620 + k * 680, 1060, 0.85 * pop(t, 0.3 + k * 0.3), t, ph=k)
    fill(c, "#000000", 0.25 * lin(t, t1 + 0.9, t1 + 1.5))
    vignette(c, 0.75)

@lru_cache(None)
def lonely_sprites():
    bg = S(sky(W, H, "#4A5562", "#8A949E") + clouds(W, 180, "#5A6470", 9, 12, 1.3, 0.9) + sea(W, H, 640, "#3E5060", "#2A3846", "#C8D0D8", 0.25) + grain(W, H))
    ship = S(f'<g transform="translate(420,420)">{longship(0.9, sail="#5A4A44", stripe="#8A7A70")}</g>', 840, 520, ax=420, ay=420)
    rag = C("lod", pose="stand", expr="sad", ss=1.0)
    return bg, ship, rag

def lonely_sea(c, x):
    t = x.t; bg, ship, rag = lonely_sprites()
    with cam(c, 1.0 + 0.04 * ease_io(lin(t, 0, x.dur)), W/2, H/2):
        draw(c, bg, W/2, H/2)
        bob = 8 * math.sin(t * 1.4); rot = 1.6 * math.sin(t * 1.1)
        sx = 1100 - 120 * lin(t, 0, x.dur)
        draw(c, ship, sx, 760 + bob, 0.9, rot=rot)
        actor(c, rag, sx - 60, 620 + bob, 0.26, t)
    Particles("rain", 160, seed=2, color="#C8D4E0", speed=60).draw(c, t)
    if t > x.c(0) + 0.6 and t < x.c(1) + 0.3:
        draw(c, hand_label("yemin: bir daha asla", 56, color="#E8EEF4"), 1400, 300, pop(t, x.c(0) + 0.6))
    vignette(c, 0.6)

@lru_cache(None)
def cta_sprites():
    bg = S(f'<rect width="{W}" height="{H}" fill="#2A1C14"/>' + "".join(f'<rect x="{x}" y="0" width="160" height="{H}" fill="{shade("#3A2818", 1.0 if (x//160)%2 else 0.9)}"/>' for x in range(0, W, 160)) + grain(W, H))
    stone = S(stone_slab(1100, 640, "#8A857C") + rune_border(1100, 640, "#4E4A44")
              + f'<text x="550" y="200" font-family="Cinzel Decorative" font-weight="900" font-size="64" fill="#2A2420" text-anchor="middle">Sırada kim</text>'
              + f'<text x="550" y="290" font-family="Cinzel Decorative" font-weight="900" font-size="64" fill="#2A2420" text-anchor="middle">doğsun?</text>'
              + f'<path d="M250,350 H850" stroke="#4E4A44" stroke-width="4"/>'
              + f'<text x="550" y="450" font-family="Caveat Brush" font-size="64" fill="#3A3430" text-anchor="middle">yorumlara kazı ↓</text>', 1140, 680)
    rag = C("ragnar", pose="point", expr="smug", ss=1.0)
    return bg, stone, rag

def cta(c, x):
    t = x.t; bg, stone, rag = cta_sprites()
    draw(c, bg, W/2, H/2)
    draw(c, stone, W/2 + 220, H/2 - 20, 0.95 * pop(t, 0.05, 0.4))
    actor(c, rag, 380, 1060, 0.95, t)
    for xx in (120, W - 120): glow(c, xx, 520, 360, "#FF9A40", 0.22 + 0.05 * math.sin(t * 7 + xx))
    vignette(c, 0.6)

@lru_cache(None)
def bread_sprites():
    bg = S(sky(W, H, "#9CC6E0", "#E9EEF0") + clouds(W, 170, "#FFFFFF", 6, 21) + mountains(W, 600, "#6E8A9E", seed=31, hmin=260, hmax=420)
           + sea(W, H, 640, "#4D8BB0", "#3B7398") + f'<path d="M0,760 Q400,700 900,740 Q1300,770 1920,720 V1080 H0 Z" fill="#7E9B6A"/>'
           + f'<g transform="translate(1500,740)"><rect x="-160" y="-150" width="320" height="150" fill="#8C6239" stroke="{INK}" stroke-width="6"/><path d="M-190,-140 L0,-260 L190,-140 Z" fill="#6E8A4E" stroke="{INK}" stroke-width="6"/></g>' + grain(W, H))
    ship = S(f'<g transform="translate(420,420)">{longship(0.75)}</g>', 840, 520, ax=420, ay=420)
    bakers = [C("baker", pose="hold_front", expr="smitten", tunic=tc, beard_c=bc) for tc, bc in (("#7A6A4A", "#6A4A2E"), ("#5A6A7A", "#A07A4A"), ("#6A4A3A", "#3A2A20"))]
    loaf = S('<ellipse cx="60" cy="40" rx="56" ry="30" fill="#1E1612" stroke="#000" stroke-width="5"/><path d="M30,30 l14,-8 M60,24 l14,-8 M88,30 l10,-6" stroke="#3A2A20" stroke-width="5"/>', 120, 80)
    smoke = S('<path d="M20,100 q-20,-25 0,-50 q20,-25 0,-50" stroke="#555" stroke-width="10" fill="none" stroke-linecap="round" opacity="0.6"/>', 40, 110, ay=100)
    rag = C("lod", pose="hips", expr="angry", ss=1.0)
    return bg, ship, bakers, loaf, smoke, rag

def burnt_bread(c, x):
    t = x.t; bg, ship, bakers, loaf, smoke, rag = bread_sprites()
    t1 = x.c(1)
    with cam(c, 1.0 + 0.05 * ease_io(lin(t, t1, x.dur)), W/2 - 100 * ease_io(lin(t, t1, x.dur)), H/2):
        draw(c, bg, W/2, H/2)
        draw(c, ship, 420, 760 + 6 * math.sin(t * 1.5), 1.0, rot=math.sin(t) * 1.2)
        actor(c, rag, 360, 560, 0.42, t)
        if t > t1 - 0.2:
            for k, b_ in enumerate(bakers):
                bx = 1450 - 520 * ease_out(lin(t, t1 - 0.2, t1 + 1.2)) + k * 150
                actor(c, b_, bx, 950 + (k % 2) * 20, 0.62, t, ph=k, bob=6)
                draw(c, loaf, bx + 4, 805, 0.7)
                for j in range(2):
                    p = ((t * 0.8 + j * 0.5 + k * 0.3) % 1)
                    draw(c, smoke, bx + j * 20, 700 - p * 90, 0.6, a=1 - p)
    if t > t1 + 1.0: draw(c, label("KÖMÜR", 70, color="#FFB35A", rot=-6), 1300, 330, pop(t, t1 + 1.0)); arrow_at(c, t, t1 + 1.1, 1240, 380, 1060, 600, -0.25)
    vignette(c, 0.4)

@lru_cache(None)
def kraka_sprites():
    bg = S(sky(W, H, "#B8D8E6", "#F0EEE0") + pines(W, 640, "#4E7A5E", 34, 12, 180, 300) + ground(W, H, 700, "#7E9B6A")
           + f'<path d="M0,820 Q500,760 960,820 T1920,800 V940 Q1400,900 960,950 T0,930 Z" fill="#6AA8C8" stroke="#3E6E8A" stroke-width="5"/>'
           + "".join(f'<path d="M{x},{860+(x%3)*12} q20,-8 40,0" stroke="#fff" stroke-width="4" fill="none" opacity="0.6"/>' for x in range(60, W, 140)) + grain(W, H))
    kr = C("kraka", pose="hold_front", expr="smug", ss=1.2)
    bush = S(f'<g transform="translate(260,200)">' + "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#3E6E3E" stroke="{INK}" stroke-width="5"/>' for x, y, r in ((-150, 0, 90), (-40, -40, 110), (90, -10, 100), (180, 30, 70))) + '</g>', 520, 300, ay=200)
    heads = S("".join(f'<g transform="translate({120+k*140},{150 + (k%2)*12}) scale(0.72)">{head(dict(BAKER, beard_c=bc), 76, 0, "smitten")}</g>' for k, bc in enumerate(("#6A4A2E", "#A07A4A", "#3A2A20"))), 560, 280, ay=150)
    hl = label("SAÇ: AYAK BİLEĞİNE KADAR", 54, rot=-3)
    name = label("Kráka", 140, font="Pirata One", color="#F6ECD4", sw=12, sub="(= karga)")
    return bg, kr, bush, heads, hl, name

def kraka_reveal(c, x):
    t = x.t; bg, kr, bush, heads, hl, name = kraka_sprites()
    z = 1.12 - 0.1 * ease_io(lin(t, 0, x.dur))
    with cam(c, z, W/2 + 60, H/2):
        draw(c, bg, W/2, H/2)
        glow(c, 1150, 640, 520, "#FFF4D0", 0.25)
        actor(c, kr, 1150, 900, 0.95, t, breathe=0.006)
        draw(c, heads, 420, 700 - 20 * ease_out(lin(t, 0.2, 0.8)))
        draw(c, bush, 420, 820)
        for k in range(3):
            p = ((t * 0.5 + k * 0.33) % 1)
            draw(c, heart_sp(), 340 + k * 120, 540 - p * 160, 0.5 + 0.2 * p, a=1 - p)
    if t > x.c(1): draw(c, name, 1530, 210, pop(t, x.c(1), 0.4))
    if t > x.c(2): draw(c, hl, 1480, 960, pop(t, x.c(2))); arrow_at(c, t, x.c(2) + 0.1, 1330, 930, 1230, 870, -0.3)
    vignette(c, 0.4)

@lru_cache(None)
def riddle_sprites():
    bg = S(f'<rect width="{W}" height="{H}" fill="#3A2818"/>' + "".join(f'<rect x="0" y="{y}" width="{W}" height="90" fill="{shade("#5A3E26", 1.0 if (y//90)%2 else 0.9)}" stroke="#2A1A10" stroke-width="3"/>' for y in range(0, H, 90)) + grain(W, H))
    card = S(scroll_frame(1240, 760) + f'<text x="620" y="120" font-family="Pirata One" font-size="92" fill="#5A2018" text-anchor="middle">Bilmece</text>'
             + f'<text x="620" y="190" font-family="Alegreya" font-style="italic" font-size="38" fill="{INK}" text-anchor="middle">Gemime gelsin, ama…</text>', 1320, 840, ax=40, ay=40)
    rows = [S(f'<text x="0" y="50" font-family="Alegreya" font-weight="bold" font-size="54" fill="{INK}">{s}</text>', 900, 70, ax=0, ay=35)
            for s in ("Ne giyinik, ne çıplak", "Ne aç, ne tok", "Ne yalnız, ne de biriyle")]
    box = S(checkbox(6, 6), 64, 64); boxc = S(checkbox(6, 6, True), 70, 64)
    return bg, card, rows, box, boxc

def riddle(c, x):
    t = x.t; bg, card, rows, box, boxc = riddle_sprites()
    draw(c, bg, W/2, H/2)
    with cam(c, 1.0 + 0.03 * ease_io(lin(t, 0, x.dur)), W/2, H/2):
        draw(c, card, 340, 150, 1.0, a=fade(t, x.c(1) - 0.3, 0.3))
        for i in range(3):
            ti = x.c(2 + i)
            if t > ti:
                draw(c, box, 520, 500 + i * 130, pop(t, ti)); draw(c, rows[i], 610, 500 + i * 130, 1.0, a=fade(t, ti, 0.2))
    if t < x.c(1): draw(c, C("ragnar", pose="hips", expr="smug"), W/2, 1060, 1.0)
    vignette(c, 0.5)

@lru_cache(None)
def answer_sprites():
    bg = S(sky(W, H, "#F2C49A", "#F6E2C0") + sea(W, H, 700, "#5A8EAE", "#3E6E8E") + f'<rect y="760" width="{W}" height="320" fill="#8C5A2E"/>'
           + "".join(f'<path d="M0,{y} H{W}" stroke="#6B4222" stroke-width="5"/>' for y in range(800, H, 60)) + grain(W, H))
    net = "".join(f'<path d="M{-80+i*26},-470 L{-60+i*22},-20" stroke="#E9DCC0" stroke-width="3" opacity="0.85"/>' for i in range(7)) + "".join(f'<path d="M-90,{-450+j*40} Q0,{-440+j*40} 90,{-450+j*40}" stroke="#E9DCC0" stroke-width="3" opacity="0.85"/>' for j in range(11))
    kr = C("kraka", pose="hold_front", expr="smug", props=("onion",), ss=1.2, tunic="#2C2420", trim="#2C2420", **{})
    netsp = S(f'<g transform="translate(150,520)">{net}</g>', 300, 560, ax=150, ay=520)
    dog = S(f'<g transform="translate(130,140)">{dog_small()}</g>', 260, 160, ay=140)
    mini = S(f'<rect x="0" y="0" width="560" height="270" rx="18" fill="#EAD7A8" stroke="{INK}" stroke-width="6"/>' + parchment(560, 270)
             + "".join(f'<text x="96" y="{70+i*80}" font-family="Alegreya" font-weight="bold" font-size="36" fill="{INK}">{s}</text>' for i, s in enumerate(("ağ + saç", "bir ısırık soğan", "bir köpek"))), 560, 270, ax=0, ay=0)
    tick = S(checkbox(6, 6, True), 70, 64)
    rag = C("lod", pose="hold_front", expr="smitten", facing=-1, ss=1.0)
    return bg, kr, netsp, dog, mini, tick, rag

def riddle_answer(c, x):
    t = x.t; bg, kr, netsp, dog, mini, tick, rag = answer_sprites()
    with cam(c, 1.0 + 0.04 * ease_io(lin(t, 0, x.dur)), W/2, H/2):
        draw(c, bg, W/2, H/2)
        kx = 700 + 120 * ease_io(lin(t, 0, x.c(1)))
        actor(c, kr, kx, 1000, 0.95, t)
        draw(c, netsp, kx, 1000 - 30, 0.95, a=0.9)
        if t > x.c(3): draw(c, dog, kx + 220, 1010, pop(t, x.c(3)))
        actor(c, rag, 1560, 1000, 0.95, t, ph=1)
        if t > x.c(4):
            for k in range(4):
                p = ((t - x.c(4)) * 0.6 + k * 0.25) % 1
                draw(c, heart_sp(), 1500 + k * 30, 420 - p * 200, 0.6 + 0.3 * p, a=1 - p)
    if t < x.c(4):
        draw(c, mini, 60, 60, 0.9, a=fade(t, x.c(1) - 0.2, 0.2))
        for i in range(3):
            if t > x.c(1 + i) + 0.4: draw(c, tick, 60 + 40 * 0.9, 60 + (40 + i * 80) * 0.9, pop(t, x.c(1 + i) + 0.4) * 0.9)
    else:
        draw(c, label("YEMİN: İPTAL", 66, color="#FF8A7A", rot=-5), 1200, 200, pop(t, x.c(4)))
    vignette(c, 0.4)

@lru_cache(None)
def tree_sprites():
    bg = S(f'<rect width="{W}" height="{H}" fill="#2A1C14"/>' + "".join(f'<rect x="{x}" y="0" width="160" height="{H}" fill="{shade("#3A2818", 1.0 if (x//160)%2 else 0.9)}"/>' for x in range(0, W, 160)) + grain(W, H))
    sig_inner = (f'<rect width="460" height="400" fill="#C9B48A"/>' + serpent_body([(20, 380), (120, 300), (60, 230), (180, 180)], w=40, c="#B8322A", belly="#E9A87A") + serpent_head(190, 170, 0.6, -20, c="#B8322A", mouth_open=True)
                 + f'<g transform="translate(330,430) scale(0.62)">{character(dict(RAGNAR, hair="#D9B060", beard="short", cloak="#4A3A6A", tunic="#6A6A7A", armor="#9AA5AD"), "adult", "thrust", "determined", facing=-1, props=("thrust",))}</g>')
    sig = S(frame_portrait(460, 400, sig_inner, "SIGURD"), 520, 520, ax=260, ay=220)
    asl = S(frame_portrait(380, 440, f'<rect width="380" height="440" fill="#C9B48A"/><g transform="translate(190,476) scale(0.72)">{character(dict(ASLAUG), "adult", "hold_front", "smug")}</g>', "ASLAUG"), 440, 560, ax=220, ay=240)
    return bg, sig, asl

def family_tree(c, x):
    t = x.t; bg, sig, asl = tree_sprites()
    draw(c, bg, W/2, H/2)
    with cam(c, 1.0 + 0.04 * ease_io(lin(t, 0, x.dur)), W/2, H/2):
        if t > x.c(1): draw(c, asl, 1360, 520, pop(t, x.c(1), 0.4), rot=2)
        if t > x.c(2):
            draw(c, sig, 540, 470, pop(t, x.c(2), 0.4), rot=-2)
            arrow_at(c, t, x.c(2) + 0.4, 820, 470, 1120, 520, -0.2, "#E2B23A")
    if t > x.c(1) + 0.4 and t < x.c(2):
        draw(c, label("KRÁKA = ASLAUG", 62, rot=-3), 1360, 1000, pop(t, x.c(1) + 0.4))
    if t > x.c(2) + 0.8: draw(c, hand_label("babası", 60, color="#FFE27A"), 960, 380, pop(t, x.c(2) + 0.8))
    if t > x.c(2) + 0.5: draw(c, hand_label("Fáfnir'in katili", 50), 540, 860, pop(t, x.c(2) + 0.5))
    for xx in (80, W - 80): glow(c, xx, 520, 360, "#FF9A40", 0.2)
    vignette(c, 0.55)

@lru_cache(None)
def sons_sprites():
    bg = S(f'<rect width="{W}" height="{H}" fill="#2A1C14"/>' + "".join(f'<rect x="{x}" y="0" width="160" height="{H}" fill="{shade("#3A2818", 1.0 if (x//160)%2 else 0.9)}"/>' for x in range(0, W, 160)) + grain(W, H))
    def por(name, plate, pose="cross", expr="smug", props=(), extra=""):
        sp = dict(CAST[name])
        return S(frame_portrait(330, 400, f'<rect width="330" height="400" fill="#C9B48A"/>{extra}<g transform="translate(165,448) scale(0.66)">{character(sp, "adult", pose, expr, props=props)}</g>', plate), 380, 520, ax=190, ay=220)
    stretcher = '<rect x="20" y="330" width="290" height="26" rx="8" fill="#8C5E34" stroke="#2A1D14" stroke-width="5"/>'
    ps = [por("ivar", "IVAR · KEMİKSİZ", "sit", "cold", extra=stretcher), por("bjorn", "BJÖRN · DEMİR BÖĞÜR", "cross", "determined"),
          por("hvitserk", "HVITSERK", "hips", "smug"), por("sigurd", "SIGURD", "cross", "cold")]
    eye = S(f'<g transform="translate(400,300)"><ellipse rx="380" ry="230" fill="#FFFDF7" stroke="{INK}" stroke-width="14"/><circle r="190" fill="#5A8A4A"/><circle r="92" fill="{INK}"/>'
            f'<circle r="146" fill="none" stroke="#B8F08A" stroke-width="22"/><path d="M146,0 l40,-22 l-6,44 Z" fill="#B8F08A"/><circle cx="-60" cy="-70" r="34" fill="#fff"/></g>', 800, 600, ss=1.0)
    return bg, ps, eye

def sons_lineup(c, x):
    t = x.t; bg, ps, eye = sons_sprites()
    t3 = x.c(3)
    draw(c, bg, W/2, H/2)
    z = 1.0 + 1.6 * ease_in(lin(t, t3, t3 + 0.9))
    with cam(c, z, W/2 + (1620 - W/2) * ease_io(lin(t, t3, t3 + 0.9)), H/2 + (380 - H/2) * ease_io(lin(t, t3, t3 + 0.9))):
        times = [x.c(1), x.c(1), x.c(2), x.c(2) + 0.3]
        for i in range(4):
            if t > times[i] - 0.3 or i == 3 and t > x.c(2):
                draw(c, ps[i], 300 + i * 440, 500, pop(t, times[i] - 0.3 + (0.2 if i == 1 else 0)), rot=(-2, 1, -1, 2)[i])
    if t > t3 + 0.8:
        fill(c, "#000", 0.5 * fade(t, t3 + 0.8, 0.3))
        draw(c, eye, W/2, H/2, pop(t, t3 + 0.8, 0.45) * 1.2, rot=4 * math.sin(t))
    if x.c(0) < t < x.c(1): draw(c, label("+4 OĞUL", 80), W/2, H/2, pop(t, x.c(0)))
    for xx in (80, W - 80): glow(c, xx, 520, 360, "#FF9A40", 0.2)
    vignette(c, 0.55)

# ═══════════════════════════════ V · PARİS
@lru_cache(None)
def seine_sprites():
    m = S(map_vellum(W, H) + land("M0,0 H1920 V1080 H0 Z", "#D8BE82") +
          '<path d="M180,140 Q420,240 560,360 Q700,470 840,450 Q1000,430 1080,560 Q1180,700 1360,720 Q1500,730 1600,820" stroke="#5A8EAE" stroke-width="34" fill="none" stroke-linecap="round"/>'
          '<path d="M180,140 Q420,240 560,360 Q700,470 840,450 Q1000,430 1080,560 Q1180,700 1360,720 Q1500,730 1600,820" stroke="#8FC0D8" stroke-width="12" fill="none" stroke-linecap="round"/>'
          f'<g transform="translate(1600,820)"><circle r="40" fill="#B8322A" stroke="{INK}" stroke-width="6"/><text y="90" font-family="Cinzel" font-weight="700" font-size="56" text-anchor="middle" fill="#5A2018">PARİS</text></g>'
          '<text x="460" y="200" font-family="Alegreya" font-style="italic" font-size="46" fill="#3E6E8A">Seine</text>' + grain(W, H))
    ship = S(f'<g transform="translate(60,70) scale(0.22)">{longship(1.0)}</g>', 140, 110)
    return m, ship

SEINE = [(180, 140), (420, 240), (560, 360), (700, 470), (840, 450), (1000, 430), (1080, 560), (1180, 700), (1360, 720), (1500, 730), (1600, 820)]
def seine_pt(p):
    p = clamp(p) * (len(SEINE) - 1); i = min(int(p), len(SEINE) - 2); f = p - i
    return SEINE[i][0] + (SEINE[i+1][0] - SEINE[i][0]) * f, SEINE[i][1] + (SEINE[i+1][1] - SEINE[i][1]) * f

def seine_map(c, x):
    t = x.t; m, ship = seine_sprites()
    with cam(c, 1.05, W/2, H/2):
        draw(c, m, W/2, H/2)
        for k in range(14):
            p = ease_io(lin(t, x.c(1) - 0.2, x.dur)) - k * 0.035
            if p > 0:
                px, py = seine_pt(p * 0.92); draw(c, ship, px + (k % 3 - 1) * 26, py - 30 + (k % 2) * 20, 0.9)
    if t > x.c(0): draw(c, label("845", 130, font="Cinzel Decorative", color="#F6ECD4", sw=12), 360, 820, pop(t, x.c(0)))
    if t > x.c(1) + 0.6: draw(c, label("120 GEMİ", 70, rot=-4), 1350, 300, pop(t, x.c(1) + 0.6))
    vignette(c, 0.4)

@lru_cache(None)
def paris_sprites():
    bg = S(sky(W, H, "#9CC6E0", "#F0EEE0") + clouds(W, 160, "#FFFFFF", 6, 41)
           + "".join(f'<rect x="{x}" y="{560-h}" width="{w}" height="{h}" fill="#C9C0AE" stroke="{INK}" stroke-width="5"/><path d="M{x-10},{560-h} L{x+w/2},{490-h} L{x+w+10},{560-h} Z" fill="#4E6A8A" stroke="{INK}" stroke-width="5"/>' for x, w, h in ((140, 160, 160), (360, 120, 230), (560, 220, 170), (840, 140, 300), (1060, 200, 190), (1320, 160, 240), (1540, 240, 160)))
           + f'<rect y="560" width="{W}" height="520" fill="#B9AE9A" stroke="{INK}" stroke-width="6"/>' + "".join(f'<rect x="{x+10}" y="500" width="70" height="62" fill="#B9AE9A" stroke="{INK}" stroke-width="6"/>' for x in range(0, W, 120)) + grain(W, H))
    ch = C("charles", pose="give", expr="sad", ss=1.2)
    ch2 = C("charles", pose="shrug", expr="surprised", ss=1.2)
    chest_ = S(f'<g transform="translate(180,240)">{chest(True, True)}</g>', 360, 280, ay=240, ss=1.1)
    kel = label("KEL", 80, rot=-6, sub="(resmî lakabı)")
    sweat = S('<path d="M20,0 Q36,24 20,40 Q4,24 20,0 Z" fill="#8FD0F0" stroke="#2A1D14" stroke-width="4"/>', 40, 44)
    rag = C("lod", pose="hips", expr="smug", ss=1.0)
    return bg, ch, ch2, chest_, kel, sweat, rag

def paris_king(c, x):
    t = x.t; bg, ch, ch2, chest_, kel, sweat, rag = paris_sprites()
    with cam(c, 1.0 + 0.05 * ease_io(lin(t, 0, x.dur)), W/2, H/2):
        draw(c, bg, W/2, H/2)
        actor(c, rag, 1500, 1060, 0.95, t, ph=1)
        actor(c, ch2 if t < x.c(2) else ch, 760, 1060, 1.0, t)
        draw(c, sweat, 860, 430 + ((t * 1.5) % 1) * 60, 1.0, a=1 - ((t * 1.5) % 1))
        if t > x.c(2): draw(c, chest_, 1080, 1030, pop(t, x.c(2)))
    if t > x.c(1) + 0.4: draw(c, kel, 420, 230, pop(t, x.c(1) + 0.4)); arrow_at(c, t, x.c(1) + 0.5, 520, 300, 700, 360, -0.25)
    if t > x.c(0) + 0.2 and t < x.c(1): draw(c, hand_label("Paskalya, 845", 54), 1400, 200, pop(t, x.c(0) + 0.2))
    vignette(c, 0.4)

@lru_cache(None)
def ransom_sprites():
    bg = S(f'<rect width="{W}" height="{H}" fill="#2E2A3A"/>' + grain(W, H))
    rec = S(parchment(900, 760) + f'<text x="450" y="110" font-family="Pirata One" font-size="90" fill="#2E2A5A" text-anchor="middle">Makbuz</text>'
            f'<text x="80" y="230" font-family="Alegreya" font-size="40" fill="{INK}">Ödeyen: Kel Charles</text>'
            f'<text x="80" y="300" font-family="Alegreya" font-size="40" fill="{INK}">Alan: Reginherus (?)</text>'
            f'<path d="M80,340 H820" stroke="{INK}" stroke-width="3" stroke-dasharray="10 8"/>'
            f'<text x="80" y="420" font-family="Alegreya" font-weight="bold" font-size="58" fill="{INK}">7.000 livre</text>'
            f'<text x="80" y="480" font-family="Alegreya" font-size="38" fill="{INK}">gümüş + altın</text>', 940, 800, ax=470, ay=400)
    ton = label("≈ 2,5 TON", 88, color="#FFE27A", rot=-5)
    paid = S(f'<g transform="translate(260,110)">{stamp("ÖDENDİ", "#B8322A", -14, 80)}</g>', 520, 220)
    pile = S(f'<g transform="translate(400,260)">{coins_pile(140, 9, 760, 260)}</g>', 800, 300, ay=260)
    return bg, rec, ton, paid, pile

def ransom(c, x):
    t = x.t; bg, rec, ton, paid, pile = ransom_sprites()
    draw(c, bg, W/2, H/2)
    with cam(c, 1.0 + 0.04 * ease_io(lin(t, 0, x.dur)), W/2, H/2):
        glow(c, W/2, 900, 700, "#FFD27A", 0.25)
        draw(c, pile, W/2, 1080, 1.0 + 0.1 * pop(t, x.c(1)))
        draw(c, rec, 700, 470, pop(t, 0.05, 0.35), rot=-3)
        if t > x.c(0) + 1.0: draw(c, paid, 820, 700, pop(t, x.c(0) + 1.0, 0.2) * 1.0)
    if t > x.c(1): draw(c, ton, 1450, 380, pop(t, x.c(1)))
    vignette(c, 0.5)

@lru_cache(None)
def hist_sprites():
    left = S(f'<rect width="960" height="{H}" fill="#3A3A4A"/>' + "".join(f'<rect x="{40+k*80}" y="{140+(k%3)*30}" width="60" height="{300}" fill="{["#7A2E2A","#2E4E7A","#3E6E4A","#7A6A2E"][k%4]}" stroke="{INK}" stroke-width="4"/>' for k in range(11)) + f'<rect y="440" width="960" height="30" fill="#5A3B22" stroke="{INK}" stroke-width="4"/>' + grain(960, H), 960, H)
    right = S(f'<rect width="960" height="{H}" fill="#6E4E34"/>' + grain(960, H), 960, H)
    s1 = C("scholar", pose="point", expr="angry", props=("scroll",))
    s2 = C("scholar", pose="shrug", expr="surprised", facing=-1, hair="#6A5A4A", beard_c="#8A7A6A", tunic="#4A3A3A")
    q = label("REGINHERUS = RAGNAR?", 52, rot=-3)
    rag = C("lod", pose="count", expr="happy", props=("coin",), ss=1.0)
    pile = S(f'<g transform="translate(260,140)">{coins_pile(50, 5, 420, 140)}</g>', 520, 170, ay=140)
    return left, right, s1, s2, q, rag, pile

def historians(c, x):
    t = x.t; left, right, s1, s2, q, rag, pile = hist_sprites()
    split = W/2 if t > x.c(1) - 0.2 else W/2 + (W/2) * (1 - 0)
    rr = ease_out(lin(t, x.c(1) - 0.3, x.c(1) + 0.2))
    lw = W - (W/2) * rr
    c.save(); c.clipRect(skia.Rect(0, 0, lw, H))
    draw(c, left, lw/2 if rr < 1 else W/4, H/2, sx=lw/960 if rr < 1 else 1, sy=1)
    actor(c, s1, lw * 0.3, 1050, 0.85, t, bob=4); actor(c, s2, lw * 0.72, 1050, 0.85, t, ph=1)
    draw(c, q, lw / 2, 160, pop(t, 0.3))
    c.restore()
    if rr > 0:
        c.save(); c.clipRect(skia.Rect(lw, 0, W, H))
        draw(c, right, lw + 480, H/2)
        draw(c, pile, lw + 480, 1040)
        actor(c, rag, lw + 480, 1000, 0.9, t, bob=3)
        c.restore()
        c.drawRect(skia.Rect(lw - 6, 0, lw + 6, H), skia.Paint(Color4f=col(INK)))
    if t > x.c(2): draw(c, label("SAYIYORSUN", 64, color="#FFE27A", rot=4), 1440, 200, pop(t, x.c(2)))
    vignette(c, 0.45)

# ═══════════════════════════════ VI · İKİ GEMİ
@lru_cache(None)
def fame_sprites():
    bg = S(longhouse_interior(W + 200, H + 120, night=True) + grain(W + 200, H + 120), W + 200, H + 120)
    rag = C("old", pose="cross", expr="cold", ss=1.0)
    skald = C("hring", pose="arms_up", expr="happy", tunic="#4A5E3A", cloak="#2F3E2A", circlet=False, armring=False, hair="#9A8A72", beard="full", beard_c="#8A7A62", hair_style="short", facing=-1)
    hud = S(f'<rect x="0" y="0" width="760" height="230" rx="16" fill="#120D09" opacity="0.7"/>'
            f'<text x="30" y="70" font-family="Alegreya SC" font-weight="bold" font-size="40" fill="#F1E3C2">RAGNAR · ÜN</text>'
            f'<text x="30" y="170" font-family="Alegreya SC" font-weight="bold" font-size="40" fill="#F1E3C2">OĞULLAR · ÜN</text>', 760, 230, ax=0, ay=0)
    return bg, rag, skald, hud

def fame_bars(c, x):
    t = x.t; bg, rag, skald, hud = fame_sprites()
    with cam(c, 1.0 + 0.04 * ease_io(lin(t, 0, x.dur)), W/2, H/2 + 40):
        draw(c, bg, W/2, H/2 - 20)
        glow(c, 1000, 860, 650, "#FF9A40", 0.35)
        draw(c, hearth_sp(), 1000, 940); draw(c, flame_sp(int(t * 8) % 6), 1000, 920)
        actor(c, rag, 520, 1040, 1.0, t)
        actor(c, skald, 1480, 1040, 0.95, t, bob=6)
    p = ease_io(lin(t, x.c(1), x.c(2) + 1.0))
    draw(c, hud, 50, 40, 1.0, a=fade(t, 0.3))
    for i, (v, cc) in enumerate(((0.95 - 0.6 * p, "#E2B23A"), (0.2 + 0.78 * p, "#5FB0E0"))):
        y = 40 + 88 + i * 100
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(80, y, 80 + 700, y + 30), 10, 10), skia.Paint(Color4f=col("#3A3028")))
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(80, y, 80 + 700 * v, y + 30), 10, 10), skia.Paint(Color4f=col(cc)))
    Particles("ember", 30, seed=5, area=(700, 400, 1300, 950), color="#FFC070").draw(c, t)
    vignette(c, 0.6)

@lru_cache(None)
def twoship_sprites():
    m = S(map_vellum(W, H) + land(BRITAIN) + land(JUTLAND, "#E2C27A") + land(SCANDI, "#E2C27A") + land(FRANCE) + grain(W, H))
    ship = S(f'<g transform="translate(90,100) scale(0.34)">{longship(1.0)}</g>', 200, 150)
    big = S(f'<g transform="translate(90,100) scale(0.34)">{longship(1.0, sail="#7A6A58", stripe="#A8977E", oars=False)}</g>', 200, 150)
    lab = label("PLAN: 2 GEMİ", 70, rot=-4)
    rag = C("old", pose="point", expr="determined", ss=1.0)
    return m, ship, big, lab, rag

def two_ships(c, x):
    t = x.t; m, ship, big, lab, rag = twoship_sprites()
    with cam(c, 1.0, W/2, H/2):
        draw(c, m, W/2, H/2)
        p = ease_io(lin(t, x.c(1), x.dur))
        for k in range(2):
            draw(c, big, 1120 - 400 * p + k * 70, 560 - 160 * p + k * 40, 1.1 + 0.2 * pop(t, x.c(1) + 0.3 + k * 0.2))
        actor(c, rag, 1700, 1080, 0.85, t)
    if t > x.c(1) + 0.8: draw(c, lab, 960, 220, pop(t, x.c(1) + 0.8))
    vignette(c, 0.4)

@lru_cache(None)
def warn_sprites():
    bg = S(longhouse_interior(W + 200, H + 120, night=False) + grain(W + 200, H + 120), W + 200, H + 120)
    asl = C("aslaug", pose="cross", expr="angry", ss=1.1)
    rag = C("old", pose="wave", expr="smug", facing=-1, ss=1.1)
    bub = bubble_sp(f'<g transform="translate(-60,-30) scale(0.28)">{longship(1.0, oars=False)}</g><path d="M-170,60 Q-60,30 40,70 L40,90 L-170,90 Z" fill="#C8AE76" stroke="{INK}" stroke-width="5"/>'
                    f'<path d="M60,-90 L150,0 M150,-90 L60,0" stroke="#B8322A" stroke-width="16" stroke-linecap="round"/>', 400, 280, "left")
    no = label("DİNLEMİYORSUN", 64, color="#FF8A7A", rot=5)
    return bg, asl, rag, bub, no

def aslaug_warn(c, x):
    t = x.t; bg, asl, rag, bub, no = warn_sprites()
    with cam(c, 1.0 + 0.04 * ease_io(lin(t, 0, x.dur)), W/2, H/2 + 40):
        draw(c, bg, W/2, H/2 - 20)
        actor(c, asl, 680, 1050, 1.0, t)
        actor(c, rag, 1300, 1050, 1.0, t, ph=1)
    draw(c, bub, 980, 330, pop(t, x.c(0) + 0.2) * (1 - fade(t, x.c(1) + 0.3, 0.2)))
    if t > x.c(1): draw(c, no, 1420, 300, pop(t, x.c(1)))
    vignette(c, 0.45)

@lru_cache(None)
def shirt_sprites():
    bg = S(f'<rect width="{W}" height="{H}" fill="#1E1A28"/>' + grain(W, H))
    shirt = S(f'<g transform="translate(260,260)"><path d="M-150,-180 L-60,-205 Q0,-175 60,-205 L150,-180 L250,60 L200,90 L130,-40 L140,230 Q0,250 -140,230 L-130,-40 L-200,90 L-250,60 Z" fill="#E9E4F2" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
              + "".join(f'<text x="{x}" y="{y}" font-family="DejaVu Sans" font-size="40" fill="#A08AE0" text-anchor="middle">{r}</text>' for x, y, r in ((-70, 40, "ᚨ"), (0, 100, "ᛊ"), (70, 40, "ᛚ"), (0, -40, "ᚢ"), (-60, 150, "ᚷ"), (60, 150, "ᛟ")))
              + f'<path d="M-60,-200 Q0,-140 60,-200" fill="none" stroke="{INK}" stroke-width="6"/><path d="M-100,-150 Q-40,40 -90,220" stroke="#fff" stroke-width="14" opacity="0.6" fill="none"/><path d="M-140,215 Q0,240 140,215" stroke="#A08AE0" stroke-width="10" fill="none"/></g>', 520, 540, ss=1.2)
    asl = C("aslaug", pose="give", expr="sad", ss=1.0)
    lab = label("DEMİR İŞLEMEZ", 70, color="#D8C8FF", rot=-4)
    return bg, shirt, asl, lab

def silk_shirt(c, x):
    t = x.t; bg, shirt, asl, lab = shirt_sprites()
    draw(c, bg, W/2, H/2)
    rays(c, 1150, 500, -90, 900, 360, 14, "#C8B8FF", 0.10, t)
    glow(c, 1150, 500, 500, "#B8A8FF", 0.35 + 0.05 * math.sin(t * 3))
    draw(c, shirt, 1150, 500 + 10 * math.sin(t * 1.5), 0.95 * pop(t, x.c(0) + 0.5, 0.45), rot=3 * math.sin(t))
    actor(c, asl, 520, 1060, 1.0, t)
    Particles("dust", 50, seed=13, color="#E0D8FF", speed=40).draw(c, t)
    if t > x.c(1): draw(c, lab, 1300, 900, pop(t, x.c(1)))
    vignette(c, 0.6)

# ═══════════════════════════════ VII · ÇUKUR
@lru_cache(None)
def battle_sprites():
    bg = S(sky(W, H, "#5A6270", "#A8AEB4") + clouds(W, 200, "#6E7682", 8, 51, 1.2, 0.9) + ground(W, H, 780, "#5E6A4E", "#4E5A40") + grain(W, H))
    sax = S("".join(f'<g transform="translate({60+k*120},{430 + (k%3)*30}) scale(0.5)">{character(dict(SAXON, tunic=["#8A2A2A","#7A3A2A","#6A2A3A"][k%3]), "adult", "spear", "angry", facing=-1, props=("shield","spear"))}</g>' for k in range(16)), W, 470, ay=430)
    rag = C("old", pose="thrust", expr="angry", props=("thrust",), ss=1.1, tunic="#E9E4F2", trim="#A08AE0", cloak="#2F4C6E")
    spark = S('<g transform="translate(60,60)">' + "".join(f'<path d="M0,0 L{40*math.cos(a):.0f},{40*math.sin(a):.0f}" stroke="#FFE27A" stroke-width="7" stroke-linecap="round"/>' for a in [i*0.785 for i in range(8)]) + '</g>', 120, 120)
    tally = [label(str(i), 90, color="#FFFFFF") for i in range(1, 5)]
    return bg, sax, rag, spark, tally

def last_battle(c, x):
    t = x.t; bg, sax, rag, spark, tally = battle_sprites()
    with cam(c, 1.05, W/2 + 20 * math.sin(t * 2), H/2):
        draw(c, bg, W/2, H/2)
        draw(c, sax, W/2 + 260, 830); draw(c, sax, W/2 + 120, 900, 1.15)
        k = int(max(0, (t - x.c(1)) / ((x.c(2) - x.c(1)) / 4))) if t > x.c(1) else 0
        lunge = 80 * math.sin(min(4, max(0, (t - x.c(1)) / ((x.c(2) - x.c(1)) / 4))) * math.pi)
        actor(c, rag, 520 + lunge, 1050, 1.0, t)
        if t > x.c(2):
            for j in range(4):
                tt = x.c(2) + j * 0.25
                if tt < t < tt + 0.3: draw(c, spark, 560 + (j % 2) * 60, 640 + j * 40, pop(t, tt, 0.15))
    if t > x.c(1):
        n = min(4, 1 + int((t - x.c(1)) / max(0.3, (x.c(2) - x.c(1)) / 4)))
        draw(c, tally[n - 1], 1700, 160, 1.0 + 0.2 * (1 - lin((t - x.c(1)) % max(0.3, (x.c(2) - x.c(1)) / 4), 0, 0.2)))
        draw(c, hand_label("kez", 50), 1790, 230, 1.0)
    vignette(c, 0.55)

@lru_cache(None)
def captive_sprites():
    bg = S(longhouse_interior(W + 200, H + 120, night=True).replace("#4A3222", "#3A3A44") + grain(W + 200, H + 120), W + 200, H + 120)
    th = S(f'<g transform="translate(200,600)"><rect x="-150" y="-560" width="300" height="560" rx="20" fill="#5A2A2A" stroke="{INK}" stroke-width="7"/><rect x="-190" y="-220" width="380" height="80" rx="12" fill="#6A3A2A" stroke="{INK}" stroke-width="6"/></g>', 400, 620, ay=600)
    aella = C("aella", pose="point", expr="cold", facing=-1, ss=1.1)
    rag = C("old", pose="bound", expr="cold", ss=1.1, tunic="#E9E4F2", trim="#A08AE0")
    q = bubble_sp('<text x="0" y="30" font-family="Luckiest Guy" font-size="80" text-anchor="middle" fill="#2A1D14">ADIN?</text>', 320, 200, "right")
    dots = bubble_sp('<text x="0" y="30" font-family="Luckiest Guy" font-size="96" text-anchor="middle" fill="#2A1D14">. . .</text>', 260, 180, "left")
    return bg, th, aella, rag, q, dots

def captive(c, x):
    t = x.t; bg, th, aella, rag, q, dots = captive_sprites()
    with cam(c, 1.0 + 0.06 * ease_io(lin(t, 0, x.dur)), W/2, H/2 + 40):
        draw(c, bg, W/2, H/2 - 20)
        draw(c, th, 1450, 1040, 1.0)
        actor(c, aella, 1450, 1060, 1.0, t)
        actor(c, rag, 640, 1060, 1.0, t)
    if t > x.c(1): draw(c, q, 1180, 300, pop(t, x.c(1)))
    if t > x.c(2): draw(c, dots, 760, 330, pop(t, x.c(2)))
    vignette(c, 0.65)

@lru_cache(None)
def pit_sprites():
    bg = S(f'<rect width="{W}" height="{H}" fill="#0E1014"/><ellipse cx="{W/2}" cy="560" rx="900" ry="620" fill="#1A1E24"/>' + "".join(f'<path d="M{x},0 L{x+40},{H}" stroke="#14171C" stroke-width="30"/>' for x in range(0, W, 140)) + grain(W, H))
    rag = C("old", pose="cross", expr="determined", ss=1.1, tunic="#E9E4F2", trim="#A08AE0", cloak=None, fur_collar=None)
    snakes = []
    for k in range(8):
        pts = [(80 + k*30, 360), (140, 300 - (k % 3) * 20), (200, 330), (260, 290)]
        snakes.append(S(serpent_body(pts, w=26, c=["#4E7A30", "#5E6A30", "#3E6A3A"][k % 3]) + serpent_head(270, 280, 0.42, -20, c=["#4E7A30", "#5E6A30", "#3E6A3A"][k % 3], mouth_open=k % 2 == 0), 420, 420))
    return bg, rag, snakes

def pit(c, x):
    t = x.t; bg, rag, snakes = pit_sprites()
    draw(c, bg, W/2, H/2)
    with cam(c, 1.0 + 0.05 * ease_io(lin(t, 0, x.dur)), W/2, H/2):
        glow(c, W/2, 700, 420, "#C8B8FF", 0.28)
        actor(c, rag, W/2, 1000, 0.95, t, breathe=0.004)
        recoil = ease_out(lin(t, x.c(1), x.c(1) + 0.6))
        for k, sp in enumerate(snakes):
            side = -1 if k % 2 == 0 else 1; j = k // 2
            R = 300 + j * 140 + 160 * recoil
            sx_ = W/2 + side * R; sy_ = 900 + (j % 2) * 70 + 10 * math.sin(t * 2 + k)
            draw(c, sp, sx_, sy_, 0.9, sx=0.9 * side, sy=0.9)
    if t > x.c(1) + 0.3: draw(c, label("GÖMLEK", 60, color="#D8C8FF", rot=-4), W/2 + 380, 380, pop(t, x.c(1) + 0.3)); arrow_at(c, t, x.c(1) + 0.4, W/2 + 300, 430, W/2 + 80, 600, 0.2, "#D8C8FF")
    vignette(c, 0.85)

def shirt_off(c, x):
    t = x.t; bg, rag, snakes = pit_sprites(); _, shirt, _, _ = shirt_sprites()
    draw(c, bg, W/2, H/2)
    p = ease_in(lin(t, 0.3, x.dur - 0.3))
    glow(c, W/2, 700, 420, "#C8B8FF", 0.28 * (1 - p))
    draw(c, shirt, W/2 + 200 * p, 520 - 380 * p, 0.6, rot=40 * p, a=1 - p)
    fill(c, "#000", 0.6 * p)
    vignette(c, 0.9)

@lru_cache(None)
def trip_sprites():
    def panel(inner): return S(f'<rect x="10" y="10" width="520" height="700" rx="20" fill="#E7D3A8" stroke="#8C6B3E" stroke-width="10"/><rect x="10" y="10" width="520" height="700" rx="20" filter="url(#parch)"/>{inner}', 540, 720)
    p1 = panel(f'<g transform="translate(270,420)">{serpent_body([(-60,40),(-20,0),(30,30),(10,-20)], w=30, c="#7FB04A")}{serpent_head(10,-40,0.5,-30,c="#7FB04A",cute=True)}</g>'
               f'<g transform="translate(270,520)"><rect x="-90" y="-20" width="180" height="70" rx="8" fill="#B8322A" stroke="{INK}" stroke-width="5"/></g>')
    p2 = panel(f'<g transform="translate(-40,200) scale(0.6)">{serpent_body([(200,700),(300,500),(600,520),(700,300),(500,180)], w=90, c="#5E8A3A")}{serpent_head(480,170,1.3,-160,c="#5E8A3A",mouth_open=True)}</g>'
               + f'<text x="270" y="660" font-family="Pirata One" font-size="64" text-anchor="middle" fill="#5A2018">Loðbrók</text>')
    p3 = panel(f'<ellipse cx="270" cy="460" rx="220" ry="90" fill="#1A1E24" stroke="{INK}" stroke-width="6"/>' + "".join(f'<g transform="translate({140+k*70},{450 + (k%2)*20}) scale(0.4)">{serpent_head(0,0,1.0,-60 + k*30,c="#4E7A30",mouth_open=True)}</g>' for k in range(4)))
    return [p1, p2, p3]

def snake_triptych(c, x):
    t = x.t; ps = trip_sprites()
    fill(c, "#0E0B08")
    for i in range(3):
        ti = x.c(i)
        if t > ti - 0.2:
            a = fade(t, ti - 0.2, 0.4) * (0.45 if i < x.idx() else 1.0)
            draw(c, ps[i], 380 + i * 580, 540, 0.95 + 0.03 * ease_out(lin(t, ti, ti + 1)), a=a)
    vignette(c, 0.7)

@lru_cache(None)
def words_sprites():
    stone = S(stone_slab(1300, 720, "#6E6A62") + rune_border(1300, 720, "#3A3630"), 1340, 760)
    l1 = S(f'<text x="600" y="70" font-family="Cinzel" font-weight="700" font-size="58" fill="#E9DCC0" text-anchor="middle">"Yaşlı domuzun ne çektiğini</text>', 1200, 100)
    l2 = S(f'<text x="600" y="70" font-family="Cinzel" font-weight="700" font-size="58" fill="#E9DCC0" text-anchor="middle">bilseler, yavrular</text>', 1200, 100)
    l3 = S(f'<text x="600" y="70" font-family="Cinzel" font-weight="700" font-size="58" fill="#E9DCC0" text-anchor="middle">nasıl hırıldardı."</text>', 1200, 100)
    return stone, [l1, l2, l3]

def last_words(c, x):
    t = x.t; stone, ls = words_sprites()
    fill(c, "#0E0B08")
    with cam(c, 1.0 + 0.05 * ease_io(lin(t, 0, x.dur)), W/2, H/2):
        draw(c, stone, W/2, H/2, 1.0, a=fade(t, 0, 0.4))
        for i, l in enumerate(ls):
            ti = x.c(1) if i == 0 else x.c(1) + (x.c(2) - x.c(1)) * 0.6 if i == 1 else x.c(2)
            if t > ti:
                a = fade(t, ti, 0.4); glow(c, W/2, 420 + i * 110, 300, "#FF9A40", 0.18 * a)
                draw(c, l, W/2, 420 + i * 110, 1.0, a=a)
    Particles("ember", 40, seed=17, color="#FF8A3A", speed=40).draw(c, t)
    vignette(c, 0.75)

# ═══════════════════════════════ VIII · YAVRULAR
@lru_cache(None)
def news_sprites():
    def panel(inner, bgc): return S(f'<rect width="600" height="1000" fill="{bgc}"/>{inner}<rect width="600" height="1000" fill="none" stroke="{INK}" stroke-width="12"/>', 600, 1000)
    bj = panel(f'<rect x="270" y="0" width="60" height="1000" fill="#8C5E34" stroke="{INK}" stroke-width="6"/>' + "".join(f'<ellipse cx="300" cy="{430+k*60}" rx="36" ry="12" fill="#5A3818"/>' for k in range(4))
               + f'<path d="M150,380 Q120,520 160,640 L440,640 Q480,520 450,380 Z" fill="#F0C49C" stroke="{INK}" stroke-width="8"/>' + "".join(f'<path d="M{170+k*0},{420+k*55} Q300,{400+k*55} 440,{420+k*55}" stroke="{INK}" stroke-width="6" fill="none"/>' for k in range(4)), "#4A4E56")
    hv = panel(f'<path d="M140,380 Q120,540 170,640 L430,640 Q480,540 460,380 Q300,330 140,380 Z" fill="#F0C49C" stroke="{INK}" stroke-width="8"/>'
               f'<g transform="translate(300,300) scale(2.4)"><path d="M-9,10 L9,10 L6,-6 Q10,-14 0,-20 Q-10,-14 -6,-6 Z" fill="#E9E1D0" stroke="{INK}" stroke-width="3.5"/><path d="M-12,-2 L12,6 M-8,8 L10,-8" stroke="{INK}" stroke-width="3"/></g>'
               f'<path d="M200,640 q10,40 0,80 M280,650 q10,40 0,90" stroke="#B8322A" stroke-width="10" fill="none" stroke-linecap="round" opacity="0.8"/>', "#ECE6D6")
    sg = panel(f'<g transform="translate(300,560) scale(2.4)">{head(dict(SIGURD_SNAKE), 76, 0, "cold")}</g><g transform="translate(470,820) rotate(-40)"><rect x="-8" y="-120" width="16" height="110" fill="#C3CCD3" stroke="{INK}" stroke-width="5"/><rect x="-12" y="-10" width="24" height="80" rx="6" fill="#5A3B22" stroke="{INK}" stroke-width="5"/></g>', "#6E3A2E")
    labs = [hand_label("parmak izi → tahtada", 46), hand_label("satranç taşı: ezik", 46), hand_label("kemiğe kadar", 46)]
    return [bj, hv, sg], labs

def sons_news(c, x):
    t = x.t; ps, labs = news_sprites()
    fill(c, "#0E0B08")
    for i in range(3):
        ti = x.c(1 + i)
        if t > ti - 0.15:
            k = ease_out(lin(t, ti - 0.15, ti + 0.25))
            draw(c, ps[i], 320 + i * 640, H/2 + 120 * (1 - k), 1.0, a=k)
            if t > ti + 0.6: draw(c, labs[i], 320 + i * 640, 960, pop(t, ti + 0.6))
    if t > x.c(4):
        draw(c, label("FARK ETMİYOR.", 80, color="#FF8A7A", rot=-3), 1600, 140, pop(t, x.c(4)))
    if t < x.c(1) + 0.2: draw(c, label("HABER GELDİ", 80, color="#FFE27A"), W/2, H/2, pop(t, 0.1))
    vignette(c, 0.6)

@lru_cache(None)
def ox_sprites():
    bg = S(sky(W, H, "#8A98A6", "#D0D4D2") + sea(W, H, 560, "#5A7A8E", "#3E5A6E") + f'<path d="M0,700 Q500,640 960,690 T1920,660 V1080 H0 Z" fill="#7A8A5A"/>' + grain(W, H))
    ships = S("".join(f'<g transform="translate({150+k*230},{220 + (k%2)*30}) scale(0.3)">{longship(1.0)}</g>' for k in range(8)), W, 320, ay=220)
    ivar = C("ivar", pose="give", expr="smug", ss=1.0)
    bearers = C("warrior", pose="grip", expr="neutral")
    stretch = S(f'<rect x="0" y="0" width="420" height="30" rx="10" fill="#8C5E34" stroke="{INK}" stroke-width="6"/>', 420, 30)
    aella = C("aella", pose="cross", expr="smug", facing=-1, ss=1.0)
    hide = S(f'<g transform="translate(240,180)">{ox_hide()}</g>', 480, 360, ss=1.1)
    lab = label("1 ÖKÜZ DERİSİ", 64, rot=-3, sub="(o kadar)")
    return bg, ships, ivar, bearers, stretch, aella, hide, lab

def ox_hide_scene(c, x):
    t = x.t; bg, ships, ivar, bearers, stretch, aella, hide, lab = ox_sprites()
    with cam(c, 1.0 + 0.04 * ease_io(lin(t, 0, x.dur)), W/2, H/2):
        draw(c, bg, W/2, H/2)
        draw(c, ships, W/2 + 40 * math.sin(t * 0.5), 600)
        actor(c, bearers, 380, 1060, 0.85, t); actor(c, bearers, 700, 1060, 0.85, t, ph=1)
        draw(c, stretch, 540, 790)
        actor(c, ivar, 560, 800, 0.62, t, ph=2)
        actor(c, aella, 1500, 1060, 0.95, t)
        if t > x.c(1) + 0.5: draw(c, hide, 1050, 620, pop(t, x.c(1) + 0.5) * 0.8)
    if t > x.c(1) + 1.0: draw(c, lab, 1050, 230, pop(t, x.c(1) + 1.0))
    if t < x.c(1): draw(c, label("BÜYÜK ORDU", 70, color="#FFE27A", rot=-4), W/2, 160, pop(t, x.c(0) + 0.2))
    vignette(c, 0.45)

@lru_cache(None)
def york_sprites():
    m = S(f'<rect width="{W}" height="{H}" fill="#7A8A5A"/>' + "".join(f'<circle cx="{(k*397)%W}" cy="{(k*233)%H}" r="{30+(k%5)*8}" fill="#6E7E50"/>' for k in range(40))
          + f'<g transform="translate({W/2},{H/2})"><rect x="-360" y="-260" width="720" height="520" fill="#B9AE9A" stroke="{INK}" stroke-width="10"/>'
            + "".join(f'<rect x="{x-30}" y="{y-30}" width="60" height="60" fill="#A89E8A" stroke="{INK}" stroke-width="6"/>' for x, y in ((-360, -260), (360, -260), (-360, 260), (360, 260)))
            + "".join(f'<rect x="{-300+k*110}" y="{-200+(k%2)*160}" width="80" height="100" fill="#8C6239" stroke="{INK}" stroke-width="5"/>' for k in range(6))
            + '<rect x="-190" y="-340" width="380" height="110" rx="12" fill="#EAD7A8" stroke="#2A1D14" stroke-width="6"/><text y="-255" font-family="Cinzel" font-weight="700" font-size="84" text-anchor="middle" fill="#5A2018">YORK</text></g>' + grain(W, H))
    crw = S(crown(110, 90, 1.4), 220, 160)
    yr = label("867", 130, font="Cinzel Decorative", color="#F6ECD4", sw=12)
    return m, crw, yr

def york(c, x):
    t = x.t; m, crw, yr = york_sprites()
    with cam(c, 1.0 + 0.06 * ease_io(lin(t, 0, x.dur)), W/2, H/2):
        draw(c, m, W/2, H/2)
        p = ease_io(lin(t, x.c(0), x.c(1) + 1.2))
        # deri şeridi kalenin etrafında
        rect = [(W/2 - 430, H/2 - 330), (W/2 + 430, H/2 - 330), (W/2 + 430, H/2 + 330), (W/2 - 430, H/2 + 330), (W/2 - 430, H/2 - 330)]
        per = sum(math.hypot(rect[i+1][0]-rect[i][0], rect[i+1][1]-rect[i][1]) for i in range(4)); L = per * p
        path = skia.Path(); path.moveTo(*rect[0]); acc = 0
        for i in range(4):
            seg = math.hypot(rect[i+1][0]-rect[i][0], rect[i+1][1]-rect[i][1])
            if acc + seg <= L: path.lineTo(*rect[i+1]); acc += seg
            else:
                f = (L - acc) / seg; path.lineTo(rect[i][0] + (rect[i+1][0]-rect[i][0])*f, rect[i][1] + (rect[i+1][1]-rect[i][1])*f); break
        c.drawPath(path, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=16, Color4f=col(INK)))
        c.drawPath(path, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=8, Color4f=col("#B07A4A")))
    if t > x.c(0) + 0.5 and t < x.c(2): draw(c, hand_label("kıl inceliğinde deri şeridi", 56), W/2, 120, pop(t, x.c(0) + 0.5))
    if t > x.c(2): draw(c, yr, 300, 160, pop(t, x.c(2)))
    if t > x.c(3):
        p = ease_in(lin(t, x.c(3), x.c(3) + 0.8)); draw(c, crw, 1500, 300 + 600 * p, 1.0, rot=200 * p)
        draw(c, hand_label("Ælla", 60), 1500, 200, pop(t, x.c(3)))
    vignette(c, 0.45)

# ═══════════════════════════════ SON
@lru_cache(None)
def legacy_sprites():
    bg = S(f'<rect width="{W}" height="{H}" fill="#2A1C14"/>' + "".join(f'<rect x="{x}" y="0" width="160" height="{H}" fill="{shade("#3A2818", 1.0 if (x//160)%2 else 0.9)}"/>' for x in range(0, W, 160)) + grain(W, H))
    def por(name, plate, pose="cross", expr="smug", w=360):
        return S(frame_portrait(w, 440, f'<rect width="{w}" height="440" fill="#C9B48A"/><g transform="translate({w/2},476) scale(0.72)">{character(dict(CAST[name]), "adult", pose, expr)}</g>', plate), w + 60, 560, ax=w/2 + 30, ay=240)
    dad = por("hring", "BABA · EFSANE", "stand", "happy")
    me = por("ragnar", "SEN", "hips", "smug")
    sons = S(frame_portrait(560, 440, f'<rect width="560" height="440" fill="#C9B48A"/>' + "".join(f'<g transform="translate({90+k*125},397) scale(0.55)">{character(dict(CAST[n]), "adult", "cross", "smug")}</g>' for k, n in enumerate(("ivar", "bjorn", "hvitserk", "sigurd"))), "OĞULLAR · EFSANE"), 620, 560, ax=310, ay=240)
    return bg, dad, me, sons

def legacy(c, x):
    t = x.t; bg, dad, me, sons = legacy_sprites()
    draw(c, bg, W/2, H/2)
    draw(c, me, W/2, 500, pop(t, 0.1))
    if t > x.c(0) + 0.4: draw(c, dad, 330, 520, pop(t, x.c(0) + 0.4), rot=-3); arrow_at(c, t, x.c(0) + 0.6, 560, 500, 720, 500, 0.0, "#E2B23A")
    if t > x.c(1) + 0.4: draw(c, sons, 1530, 520, pop(t, x.c(1) + 0.4), rot=3); arrow_at(c, t, x.c(1) + 0.6, 1200, 500, 1290, 500, 0.0, "#E2B23A")
    for xx in (80, W - 80): glow(c, xx, 520, 360, "#FF9A40", 0.2)
    vignette(c, 0.55)

@lru_cache(None)
def dawn_sprites():
    bg = S(sky(W, H, "#3A4A6E", "#E9907A", "#F6D2A0") + f'<circle cx="1400" cy="620" r="150" fill="#FFE8B0" opacity="0.95"/>' + clouds(W, 300, "#C97A7A", 5, 61, 1.2, 0.6)
           + sea(W, H, 640, "#6A6A8A", "#3A3E5A", "#FFD8B0", 0.35) + grain(W, H))
    ships = [S(f'<g transform="translate(420,420)">{longship(0.8)}</g>', 840, 520, ax=420, ay=420) for _ in range(2)]
    rag = C("old", pose="stand", expr="smug", ss=1.0)
    q = label("Yine yola çıkar mıydın?", 76, font="Cinzel Decorative", color="#F6ECD4", sw=10)
    return bg, ships, rag, q

def final_dawn(c, x):
    t = x.t; bg, ships, rag, q = dawn_sprites()
    with cam(c, 1.0 + 0.06 * ease_io(lin(t, 0, x.dur)), W/2, H/2):
        draw(c, bg, W/2, H/2)
        rays(c, 1400, 620, 180, 1600, 140, 9, "#FFE0B0", 0.08, t)
        glow(c, 1400, 620, 600, "#FFD8A0", 0.3)
        for k, sp in enumerate(ships):
            sx_ = 760 + k * 360 + 60 * t * 0.15; bob = 6 * math.sin(t * 1.4 + k)
            draw(c, sp, sx_, 780 + k * 40 + bob, 0.75 - k * 0.08, rot=math.sin(t + k))
            if k == 0: actor(c, rag, sx_ - 50, 680 + bob, 0.22, t)
    if t > x.c(1): draw(c, q, W/2, 180, pop(t, x.c(1), 0.4))
    fill(c, "#000", lin(t, x.dur - 1.2, x.dur))
    vignette(c, 0.55)
