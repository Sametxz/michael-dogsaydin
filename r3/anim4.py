"""Yas sahnesi animatiği — 4 çekim, ses yok."""
import sys, math, random, os
sys.path.insert(0, "/home/claude/r3"); sys.path.insert(0, "/home/claude/r2")
import skia
from engine import *
from fx import *
from art3 import head3, braid, hand3, EXP
import random
import stylefr as SF
import puppet as PP

OUT = "/home/claude/r3/anim4"; os.makedirs(OUT, exist_ok=True)
EA = SF.env_layers("A", grave_on=False)
EG = SF.env_layers("A", grave_on=True)
EC = SF.env_layers("C", grave_on=True)
P = dict(bustW2=None, legF=PP.leg_side(1.0), legB=PP.leg_side(0.78), torso=PP.torso_side(), head=PP.head_side("grief"),
         armN=PP.arms_carry(True), armF=PP.arms_carry(False), shroud=PP.shroud(), kneel=PP.kneel_side(),
         armsX=PP.arms_cross(), crossP=PP.cross_planted(), bust=PP.bust_3q("grief_wet"), bustC=PP.bust_3q("grief_closed"),
         back=PP.back_kneel_uc(dict(PP.WET, shaved=True)), headK=PP.head_side("grief_down"))
P["bust2"] = PP.bust_3q("grief_wet2")
DIRT = sprite('<g transform="translate(140,70)"><path d="M-120,10 Q-90,-38 -20,-46 Q40,-50 90,-30 Q130,-10 120,10 Z" fill="#4A3624" stroke="#1E1610" stroke-width="5"/>'
              '<path d="M-70,-30 q20,-8 40,-4 M10,-40 q24,-4 44,6" stroke="#6A4E34" stroke-width="5" fill="none" stroke-linecap="round"/>'
              '<ellipse cx="-30" cy="-30" rx="14" ry="4" fill="#8A7A6A" opacity="0.6"/></g>', 280, 90, ax=140, ay=70, ss=1.4)

def ground_y(x):
    return 820 - 130 * min(1, x / 620) ** 0.9 if x < 620 else 690 + (x - 620) * 0.2

def env(c, L, t, blur=0, style="A"):
    SFsky = L["sky"]; draw(c, SFsky, W/2, H/2)
    draw(c, blurred(L["far"], 7 + blur), W/2, H/2)
    fog(c, t, 600, "#C8D4DE", 0.45, seed=3)
    draw(c, blurred(L["cliff"], blur) if blur else L["cliff"], W/2, H/2)
    SF.waterfall(c, t, style=style)
    fog(c, t, 860, "#D8E2EA", 0.35, seed=7, speed=20)
    draw(c, blurred(L["hill"], blur) if blur else L["hill"], W/2, H/2)

def walker(c, x, y, s, t, rim_col="#E4F0FF"):
    """Ağır taşıma: yavaş adım, öne eğik gövde, inişte çöküş, kefen gecikmeli sallanır."""
    ph = t * 2 * math.pi / 1.5
    sw = 13 * math.sin(ph); dip = abs(math.cos(ph)); bob = 9 * (1 - dip) ** 2
    y = y + bob * s
    lean = 9 + 2 * (1 - dip)
    def pr(sp, px, py, rot=0, a=1.0):
        rim(c, sp, x + px * s, y + py * s, s, rim_col, dx=-4, dy=-3, a=0.55)
        draw(c, sp, x + px * s, y + py * s, s, rot=rot, a=a)
    sway = 2.5 * math.sin(ph - 0.9)
    pr(P["armF"], 22, -196, rot=4 + sway)
    draw(c, P["legB"], x - 6 * s, y, s, rot=-sw)
    pr(P["torso"], 0, 0, rot=lean)
    draw(c, P["legF"], x + 4 * s, y, s, rot=sw)
    draw(c, P["head"], x + 58 * s, y - 322 * s, s, rot=16 + 2 * (1 - dip))
    pr(P["shroud"], 162, -96 + 6 * (1 - dip), rot=4 + sway)
    pr(P["armN"], 40, -192, rot=3 + sway)

def shot1(c, t, d):
    z = 1.0 + 0.06 * ease_io(t / d)
    with_cam(c, z, W/2 - 80, H/2 + 20, lambda: (
        env(c, EG, t),
        light_shaft(c, 1150, 240, 700, 560, "#FFF0C8", 0.22, t, y_top=-60, y_bot=830),
        walker(c, 160 + 300 * (t / d), ground_y(160 + 300 * (t / d)) - 108 * 0.5 + 4, 0.52, t)))
    R1.draw(c, t, 1.0); R1.splashes(c, t, 760, 1060, 60, alpha=0.5)
    post_A(c)

def shot2(c, t, d, imp=1.5):
    shake = (4 * math.sin(t * 90) * (1 - lin(t, imp, imp + 0.35))) if t > imp else 0
    z = 1.85
    kx, ky, ks = 400, 770, 0.6
    th = math.radians(6); lx, ly = 160 * ks, 362 * ks
    def tip(dy=0):
        return kx - 4 + lx * math.cos(th) - ly * math.sin(th), ky - ks * 326 + dy + lx * math.sin(th) + ly * math.cos(th)
    def world():
        env(c, EG, t, blur=4)
        lift = ease_out(lin(t, 0.15, imp - 0.55)); drive = ease_in(lin(t, imp - 0.25, imp))
        rot = -10 * lift * (1 - drive) + 6 * drive
        dy = -34 * lift * (1 - drive)
        sink = 14 * ease_out(lin(t, imp, imp + 0.15))
        slump = 8 * ease_io(lin(t, imp + 0.2, imp + 1.0))
        tx, ty = tip(sink)
        rim(c, P["kneel"], kx, ky + slump * 0.5, ks, "#E4F0FF", -4, -3, 0.6)
        draw(c, P["kneel"], kx, ky + slump * 0.5, ks)
        draw(c, P["headK"], kx - 2 + slump * 0.8, ky - ks * 470 + 6 * drive + slump, ks, rot=12 + 8 * drive + slump)
        gy = tip(0)[1] - 18          # zemin çizgisi: kazığın ~24px'i toprağa girer
        c.save(); c.clipRect(skia.Rect(0, 0, W, gy + 2))
        draw(c, P["armsX"], kx - 4, ky - ks * 326 + dy + sink + slump * 0.6, ks, rot=rot)
        c.restore()
        if t > imp:
            pop = back(lin(t, imp, imp + 0.22))
            draw(c, DIRT, tx + 2, gy + 5, 0.42 * max(0.01, pop), sy=0.3 * max(0.01, pop))
        if t > imp:
            p = lin(t, imp, imp + 0.7)
            rnd = random.Random(4)
            for k in range(22):
                ang = rnd.uniform(-2.9, -0.25); v = rnd.uniform(70, 220); rr = rnd.uniform(4, 10)
                px = tx + math.cos(ang) * v * p; py = ty + math.sin(ang) * v * p + 340 * p * p
                if p < 1:
                    c.drawCircle(px, py, rr * (1 - p * 0.3), skia.Paint(Color4f=col("#3E2C1C", 1), AntiAlias=True))
                    c.drawCircle(px - rr * 0.3, py - rr * 0.3, rr * 0.3, skia.Paint(Color4f=col("#C8B8A0", 0.7), AntiAlias=True))
            # yere düşen ıslak lekeler kalır
            q = lin(t, imp + 0.5, imp + 0.7)
            if q > 0:
                rnd = random.Random(14)
                for k in range(10):
                    px = tx + rnd.uniform(-120, 110); py = ty + 24 + rnd.uniform(-6, 18)
                    c.drawOval(skia.Rect(px - 9, py - 3, px + 9, py + 3), skia.Paint(Color4f=col("#3A2A1A", 0.9 * q), AntiAlias=True))
    with_cam(c, z, 470 + shake, 640 + shake * 0.5, world)
    spd = 1.0 if t < imp else 0.5
    R2.draw(c, t * spd, 0.9); R2.splashes(c, t, 760, 1060, 40, alpha=0.4)
    post_A(c)

def shot3(c, t, d):
    z = 1.0 + 0.15 * ease_io(t / d)
    blur = int(4 + 10 * ease_io(t / d))
    bx, by, bs = 1180, 500, 0.95
    def world():
        env(c, EG, t, blur=min(14, blur))
        bl = 1.35 < t < 1.47 or 3.3 < t < 3.42 or 6.6 < t < 7.2
        tilt = -4 * ease_io(t / d) + 0.6 * math.sin(t * 1.3)
        trem = 3.7 < t < 7.4 and int(t * 6) % 2 == 1
        sp = P["bustC"] if bl else (P["bust2"] if trem else P["bust"])
        draw(c, tinted(sp, "#FFD9A8"), bx + 7, by - 4, bs, rot=tilt, a=0.8)
        draw(c, sp, bx, by, bs, rot=tilt)
        # gözyaşı: büst koordinatında yanaktan aşağı
        p = lin(t, 0.9, 3.6)
        if 0 < p < 1:
            c.save(); c.translate(bx, by); c.rotate(tilt); c.scale(bs, bs)
            x0, y0, x1, y1 = -20, 6, -30, 92
            tx, ty = x0 + (x1 - x0) * ease_in(p), y0 + (y1 - y0) * ease_in(p)
            tr = skia.Path(); tr.moveTo(x0, y0); tr.quadTo(x0 + 3, (y0 + ty) / 2, tx, ty)
            c.drawPath(tr, skia.Paint(Color4f=col("#DDF0FF", 0.55), StrokeWidth=5, Style=skia.Paint.kStroke_Style, AntiAlias=True))
            c.drawCircle(tx, ty + 4, 6.5, skia.Paint(Color4f=col("#E8F6FF", 0.95), AntiAlias=True))
            c.drawCircle(tx - 2, ty + 2, 2, skia.Paint(Color4f=col("#FFFFFF", 1), AntiAlias=True))
            c.restore()
        # omuzlara düşen yağmur sıçramaları + alından süzülen damla
        rnd = random.Random(int(t * 30))
        for k in range(7):
            u = rnd.uniform(-280, 300); v = 230 - 40 * math.sin((u + 300) / 620 * math.pi) + rnd.uniform(-10, 10)
            sx_, sy_ = bx + u * bs, by + v * bs
            for a_ in (-1, 1):
                c.drawLine(sx_, sy_, sx_ + a_ * rnd.uniform(5, 11), sy_ - rnd.uniform(6, 12), skia.Paint(Color4f=col("#E6F0FA", 0.75), StrokeWidth=2.2, AntiAlias=True))
        c.save(); c.translate(bx, by); c.rotate(tilt); c.scale(bs, bs)
        for k, (dx0, ph0) in enumerate(((40, 0.0), (-6, 1.3))):
            q = ((t + ph0) % 2.6) / 2.6
            c.drawCircle(dx0 + 4 * q, -120 + 90 * q * q, 4.5, skia.Paint(Color4f=col("#EAF6FF", 0.8 * (1 - q)), AntiAlias=True))
        c.restore()
        # nefes buharı (ağızdan sola, bakış yönüne)
        for k in range(3):
            q = ((t - 0.4 - k * 0.22) % 2.3) / 1.3
            if 0 < q < 1: bloom_spot(c, bx + 40 - 90 * q, by + 120 - 20 * q, 26 + 50 * q, "#EEF4FA", 0.3 * (1 - q))
    with_cam(c, z, 1080, 560, world)
    R3.draw(c, t, 0.65)
    post_A(c, warm=True)

def shot4(c, t, d):
    z = 1.14 - 0.14 * ease_io(t / d)
    fx_, fy, fs = 980, 840, 0.9
    gap = ease_io(lin(t, 0.4, 2.6))
    def world():
        draw(c, EC["sky"], W/2, H/2)
        bloom_spot(c, 1000, 160, 260 + 260 * gap, "#FFE6B0", 0.3 + 0.35 * gap)
        draw(c, EC["far"], W/2, H/2); draw(c, EC["cliff"], W/2, H/2)
        SF.waterfall(c, t, style="C")
        grade(c, "#000000", 0.35, "multiply")   # şelale baskın olmasın
        draw(c, EC["hill"], W/2, H/2); draw(c, EC["cross"], W/2, H/2)
        light_shaft(c, 1000, 120 + 160 * gap, fx_ + 20, 260 + 260 * gap, "#FFD99A", 0.22 + 0.42 * gap, t, y_top=-60, y_bot=fy + 20)
        bloom_spot(c, fx_, fy - 300, 220, "#FFD99A", 0.25 * gap)
        # sarsılan omuzlar: hıçkırık patlamaları
        sob = max(0, math.sin(t * 2 * math.pi / 1.6)) ** 3 * (0.4 + 0.6 * lin(t, 0.8, 1.6)) * (1 - lin(t, 3.2, 4.0))
        jit = sob * 3 * math.sin(t * 2 * math.pi * 7)
        rim(c, P["back"], fx_, fy + jit, fs, "#FFD89A", -5, -5, 0.6 + 0.4 * gap)
        draw(c, tinted(P["back"], "#0B0D10"), fx_, fy + jit, sx=fs, sy=fs * (1 + 0.012 * sob + 0.006 * math.sin(t * 1.6)))
    with_cam(c, z, W/2 - 60, H/2 - 30 * (1 - ease_io(t / d)), world)
    R4.draw(c, t * 0.6, 0.55 * (1 - 0.6 * gap))
    grade(c, "#1A2030", 0.25, "multiply"); vignette(c, 0.8); letterbox(c, 1.0, 110)
    if t > 2.0:
        p = ease_out(lin(t, 2.0, 3.4))
        sp = NAME
        c.save(); c.clipRect(skia.Rect(W/2 - sp.w / 2, 0, W/2 - sp.w / 2 + sp.w * p, H))
        draw(c, sp, W/2, 920, 1.0, a=0.92)
        c.restore()


# ───────── TIRAŞ ÇEKİMİ
HK = 2.3
def _hpart(spec, expr):
    return sprite(f'<g transform="translate(330,330) scale({HK})">{head3(spec, "side", expr)}</g>', 660, 800, ax=330, ay=330, ss=1.3)
HV = {k: _hpart(sp, "grief_down") for k, sp in (("full", PP.WET), ("nob", dict(PP.WET, nobraid=True)), ("shv", dict(PP.WET, shaved=True)))}
HCL = {k: _hpart(sp, "grief_closed") for k, sp in (("full", PP.WET), ("nob", dict(PP.WET, nobraid=True)), ("shv", dict(PP.WET, shaved=True)))}
BRAID = sprite(f'<g transform="translate(60,40) scale({HK})">{braid(0, 0, -34, 178, 24, PP.WET["hair"], (0.45, 0.85), 37)}<rect x="-13" y="-8" width="26" height="20" rx="6" fill="#5A3A22" stroke="#1A1410" stroke-width="3.5"/></g>', 260, 520, ax=60, ay=40, ss=1.3)
BODYP = sprite('<g transform="translate(420,40)">'
               f'<path d="M-380,700 Q-400,260 -200,150 L120,140 Q330,230 360,700 Z" fill="{PP.TUN}" stroke="#1A1410" stroke-width="7"/>'
               f'<path d="M-200,150 Q-330,260 -380,700 L-300,700 Q-280,330 -160,200 Z" fill="{PP.CLOAK}" stroke="#1A1410" stroke-width="6"/>'
               f'{PP.fur_mantle(-330, 300, 170, 120, n=18, seed=9)}'
               '</g>', 840, 760, ax=420, ay=40, ss=1.1)
KNIFE = sprite('<g transform="translate(90,170)">'
               f'<path d="M-30,30 L-36,360 L36,360 L30,30 Z" fill="{PP.TUN}" stroke="#1A1410" stroke-width="5"/>'
               f'<path d="M-32,40 L32,40 L30,70 L-30,70 Z" fill="{PP.SK}" stroke="#1A1410" stroke-width="4"/>'
               '<path d="M-6,-20 L-10,-150 Q0,-170 12,-150 L8,-20 Z" fill="#C8D0D8" stroke="#1A1410" stroke-width="4"/>'
               '<path d="M-2,-30 L0,-140" stroke="#FFFFFF" stroke-width="2" opacity="0.8"/>'
               '<rect x="-16" y="-24" width="32" height="10" rx="3" fill="#6A5038" stroke="#1A1410" stroke-width="3"/>'
               '<rect x="-9" y="-14" width="18" height="60" rx="5" fill="#4A3424" stroke="#1A1410" stroke-width="3"/>'
               + hand3(0, 10, 26, PP.SK, "grip", 1) + '</g>', 180, 540, ax=90, ay=180, ss=1.3)
CROSSP = sprite('<g transform="translate(40,20)"><rect x="-8" y="0" width="16" height="64" fill="#4A3424" stroke="#1A1410" stroke-width="4"/>'
                '<rect x="-26" y="14" width="52" height="14" fill="#4A3424" stroke="#1A1410" stroke-width="4"/><path d="M14,16 l7,5" stroke="#C8B89A" stroke-width="3"/><path d="M-3,6 L-3,56" stroke="#7A5A40" stroke-width="3" opacity="0.7"/></g>', 80, 100, ax=40, ay=4, ss=1.3)

def shot_tiras(c, t, d, cut=1.26, s0=1.45, s1=2.75, land=4.02):
    hx, hy = 960, 500
    z = 1.0 + 0.06 * ease_io(t / d)
    camy = 540
    def world():
        env(c, EG, t, blur=14)
        grade(c, "#0A1018", 0.25, "multiply")
        draw(c, BODYP, hx - 40, hy + 160, 1.0)
        breathe = 2 * math.sin(t * 2.2)
        closed = cut - 0.15 < t < cut + 0.35
        H = HCL if closed else HV
        # örgü kesilmeden önce sallanır
        if t < cut:
            saw = 10 * math.sin(t * 2 * math.pi * 6) * lin(t, 0.25, 0.45)
            draw(c, H["full"], hx, hy + breathe, 1.0, rot=-6)
            kx, ky = hx - 200 + saw, hy - 170
            draw(c, KNIFE, kx, ky, 1.4, rot=80)
        else:
            # düşen örgü
            q = t - cut; bx, by = hx - 165 - 40 * q, hy - 175 + 0.5 * 2200 * q * q
            if by < 1400: draw(c, BRAID, bx, by, 1.0, rot=-8 + 140 * q)
            if t < s0:
                draw(c, H["nob"], hx, hy + breathe, 1.0, rot=-6)
                kx, ky = hx - 200 - 40 * ease_out(lin(t, cut, s0)), hy - 170 - 70 * ease_out(lin(t, cut, s0))
                draw(c, KNIFE, kx, ky, 1.4, rot=80)
            elif t < s1:
                p = ease_io(lin(t, s0, s1))
                # bıçak kafa üstünde arkadan öne kayar; arkası tıraşlı
                ang = math.radians(-160 + 115 * p)
                kx, ky = hx + 210 * math.cos(ang), hy - 30 + 230 * math.sin(ang)
                draw(c, H["shv"], hx, hy + breathe, 1.0, rot=-6)
                c.save(); c.clipRect(skia.Rect(kx - 10, 0, W, H_)); draw(c, H["nob"], hx, hy + breathe, 1.0, rot=-6); c.restore()
                draw(c, KNIFE, kx, ky, 1.4, rot=70 + 50 * p)
                # saç kırpıntıları
                rnd = random.Random(int(t * 30))
                for k in range(8):
                    a0 = rnd.uniform(0, 0.5); px = kx - rnd.uniform(0, 60) - 30 * a0; py = ky + 20 + 420 * a0 * a0 + rnd.uniform(0, 80)
                    c.drawLine(px, py, px + rnd.uniform(-8, 8), py + rnd.uniform(6, 14), skia.Paint(Color4f=col(PP.WET["hair"], 0.9), StrokeWidth=3, AntiAlias=True))
            else:
                draw(c, H["shv"], hx, hy + breathe, 1.0, rot=-6)
        # haç kolye: boyuna iner, sallanır, parlar
        if t > land - 0.5:
            q = lin(t, land - 0.5, land); yy = hy + 360 - 330 * (1 - ease_in(q))
            sw = 0 if t < land else 14 * math.exp(-(t - land) * 2.2) * math.sin((t - land) * 9)
            cx_ = hx + 120
            cord = skia.Path(); cord.moveTo(hx + 40, hy + 200); cord.quadTo(cx_ + 10, yy - 140, cx_ + sw * 0.3, yy)
            c.drawPath(cord, skia.Paint(Color4f=col("#6A4A30", 0.95), StrokeWidth=4, Style=skia.Paint.kStroke_Style, AntiAlias=True))
            draw(c, CROSSP, cx_ + sw * 0.3, yy, 1.7, rot=sw)
            if t > land: bloom_spot(c, cx_ + 4, yy + 30, 50, "#E8D8B0", 0.25 * math.exp(-(t - land) * 3))
    with_cam(c, z, 960, camy, world)
    R3.draw(c, t, 0.55)
    post_A(c)
H_ = H

def with_cam(c, z, cx, cy, fn):
    z = max(1.0, z); hw, hh = W / (2 * z), H / (2 * z)
    cx = min(max(cx, hw), W - hw); cy = min(max(cy, hh), H - hh)
    c.save(); c.translate(W/2, H/2); c.scale(z, z); c.translate(-cx, -cy); fn(); c.restore()

def post_A(c, warm=False):
    gradient_grade(c, "#2A4A6E", "#1A2A3A", 0.5, "soft"); grade(c, "#9EB6CC", 0.16, "multiply")
    if warm: grade(c, "#FFB070", 0.08, "screen")
    vignette(c, 0.72); letterbox(c, 1.0, 70)

R1 = Rain(560, seed=9, angle=10); R2 = Rain(420, seed=11, angle=8); R3 = Rain(300, seed=13, angle=6, length=(40, 90)); R4 = Rain(300, seed=15, angle=8)
NAME = label("Athelstan", 110, font="Cormorant Garamond", color="#F2E6CC", sw=0, weight="600")

SHOTS = [(shot1, 8.6), (shot2, 3.6), (shot3, 8.0), (shot_tiras, 5.6), (shot4, 5.0)]

def render(preview=None):
    surf = skia.Surface(W, H); c = surf.getCanvas()
    if preview:
        for i, frac in preview:
            fn, d = SHOTS[i]; c.clear(skia.ColorBLACK); fn(c, frac * d, d)
            surf.makeImageSnapshot().save(f"{OUT}/p{i}_{int(frac*100)}.png", skia.kPNG)
        return
    wr = Writer(f"{OUT}/yas_animatik.mp4"); dip = 8
    for si, (fn, d) in enumerate(SHOTS):
        n = int(d * FPS)
        for f in range(n):
            t = f / FPS; c.clear(skia.ColorBLACK); fn(c, t, d)
            if si > 0 and f < dip: fill(c, "#000", 1 - f / dip)
            if si < len(SHOTS) - 1 and f >= n - dip: fill(c, "#000", (f - (n - dip)) / dip)
            if si == len(SHOTS) - 1 and f >= n - 20: fill(c, "#000", (f - (n - 20)) / 20)
            wr.write(surf)
    wr.close()

if __name__ == "__main__":
    if sys.argv[1] == "prev":
        render([(3, 0.1), (3, 0.24), (3, 0.38), (3, 0.82), (4, 0.7), (2, 0.85)])
    else:
        render()
