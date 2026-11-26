"""Yas sahnesi animatiği — 4 çekim, ses yok."""
import sys, math, random, os
sys.path.insert(0, "/home/claude/r3"); sys.path.insert(0, "/home/claude/r2")
import skia
from engine import *
from fx import *
import stylefr as SF
import puppet as PP

OUT = "/home/claude/r3/anim"; os.makedirs(OUT, exist_ok=True)
EA = SF.env_layers("A", grave_on=False)
EG = SF.env_layers("A", grave_on=True)
EC = SF.env_layers("C", grave_on=True)
P = dict(legF=PP.leg_side(1.0), legB=PP.leg_side(0.78), torso=PP.torso_side(), head=PP.head_side("grief"),
         armN=PP.arms_carry(True), armF=PP.arms_carry(False), shroud=PP.shroud(), kneel=PP.kneel_side(),
         armsX=PP.arms_cross(), crossP=PP.cross_planted(), bust=PP.bust_3q("grief_wet"), bustC=PP.bust_3q("grief_closed"),
         back=PP.back_kneel_uc(), headK=PP.head_side("grief_wet"))

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
    """Profil yürüyüş + taşıma. Kök kalça (x,y)."""
    ph = t * 2 * math.pi / 1.15
    sw = 17 * math.sin(ph); bob = -6 * abs(math.cos(ph))
    y = y + bob * s
    def pr(sp, px, py, rot=0, a=1.0):
        rim(c, sp, x + px * s, y + py * s, s, rim_col, dx=-4, dy=-3, a=0.55) if a > 0.9 else None
        draw(c, sp, x + px * s, y + py * s, s, rot=rot, a=a)
    pr(P["armF"], 10, -200, rot=-4 + 2 * math.sin(ph))
    draw(c, P["legB"], x - 6 * s, y, s, rot=-sw)
    pr(P["torso"], 0, 0, rot=4)
    draw(c, P["legF"], x + 4 * s, y, s, rot=sw)
    draw(c, P["head"], x + 26 * s, y - 330 * s, s, rot=8 + 2 * math.sin(ph * 2))
    pr(P["shroud"], 150, -112, rot=-3 + 1.5 * math.sin(ph))
    pr(P["armN"], 30, -196, rot=-2 + 2 * math.sin(ph))

def shot1(c, t, d):
    z = 1.0 + 0.06 * ease_io(t / d)
    with_cam(c, z, W/2 - 80, H/2 + 20, lambda: (
        env(c, EA, t),
        light_shaft(c, 1150, 240, 700, 560, "#FFF0C8", 0.22, t, y_top=-60, y_bot=830),
        walker(c, 210 + 300 * (t / d), ground_y(210 + 300 * (t / d)) - 108 * 0.5, 0.5, t)))
    R1.draw(c, t, 1.0); R1.splashes(c, t, 760, 1060, 60, alpha=0.5)
    post_A(c)

def shot2(c, t, d, imp=1.7):
    shake = (3 * math.sin(t * 90) * (1 - lin(t, imp, imp + 0.3))) if t > imp else 0
    z = 1.85
    def world():
        env(c, EA, t, blur=4)
        # haç inişi
        raise_ = ease_out(lin(t, 0.3, 1.3)); drive = ease_in(lin(t, 1.3, imp))
        rot = -28 * raise_ + 34 * drive
        kx, ky = 470, 790
        rim(c, P["kneel"], kx, ky, 0.6, "#E4F0FF", -4, -3, 0.6)
        draw(c, P["kneel"], kx, ky, 0.6)
        draw(c, P["headK"], kx - 2, ky - 0.6 * 470 + 6 * drive, 0.6, rot=10 + 8 * drive)
        sink = 10 * ease_out(lin(t, imp, imp + 0.15))
        draw(c, P["armsX"], kx - 4, ky - 0.6 * 326 + sink, 0.6, rot=rot)
        # çamur sıçraması
        if t > imp:
            p = lin(t, imp, imp + 0.6)
            rnd = random.Random(4)
            for k in range(26):
                ang = rnd.uniform(-2.8, -0.3); v = rnd.uniform(60, 180)
                th = math.radians(6); lx, ly = 160 * 0.6, 322 * 0.6
                tipx = kx - 4 + lx * math.cos(th) - ly * math.sin(th); tipy = ky - 0.6 * 326 + 10 + lx * math.sin(th) + ly * math.cos(th)
                px = tipx + math.cos(ang) * v * p; py = tipy + math.sin(ang) * v * p + 260 * p * p
                c.drawCircle(px, py, rnd.uniform(2, 5) * (1 - p * 0.5), skia.Paint(Color4f=col("#3A2A1C", 1 - p), AntiAlias=True))
    with_cam(c, z, 520 + shake, 640, world)
    spd = 1.0 if t < imp else 0.5
    R2.draw(c, t * spd, 0.9); R2.splashes(c, t, 760, 1060, 40, alpha=0.4)
    post_A(c)

def shot3(c, t, d):
    z = 1.0 + 0.15 * ease_io(t / d)
    blur = int(4 + 10 * ease_io(t / d))
    bx, by, bs = 1180, 500, 0.95
    def world():
        env(c, EG, t, blur=min(14, blur))
        bl = 1.35 < t < 1.47 or 3.15 < t < 3.27
        tilt = -5 * ease_io(t / d) + 0.8 * math.sin(t * 1.7)
        sp = P["bustC"] if bl else P["bust"]
        draw(c, tinted(sp, "#FFD9A8"), bx + 7, by - 4, bs, rot=tilt, a=0.8)
        draw(c, sp, bx, by, bs, rot=tilt)
        # gözyaşı: büst koordinatında yanaktan aşağı
        p = lin(t, 0.7, 2.8)
        if 0 < p < 1:
            c.save(); c.translate(bx, by); c.rotate(tilt); c.scale(bs, bs)
            x0, y0, x1, y1 = 90, 8, 102, 96
            tx, ty = x0 + (x1 - x0) * ease_in(p), y0 + (y1 - y0) * ease_in(p)
            tr = skia.Path(); tr.moveTo(x0, y0); tr.quadTo(x0 + 3, (y0 + ty) / 2, tx, ty)
            c.drawPath(tr, skia.Paint(Color4f=col("#DDF0FF", 0.55), StrokeWidth=5, Style=skia.Paint.kStroke_Style, AntiAlias=True))
            c.drawCircle(tx, ty + 4, 6.5, skia.Paint(Color4f=col("#E8F6FF", 0.95), AntiAlias=True))
            c.drawCircle(tx - 2, ty + 2, 2, skia.Paint(Color4f=col("#FFFFFF", 1), AntiAlias=True))
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
    def world():
        draw(c, EC["sky"], W/2, H/2)
        # bulutlar aralanır
        gap = ease_io(lin(t, 0.4, 2.6))
        bloom_spot(c, 1190, 200, 260 + 260 * gap, "#FFE6B0", 0.35 + 0.4 * gap)
        draw(c, EC["far"], W/2, H/2); draw(c, EC["cliff"], W/2, H/2)
        SF.waterfall(c, t, style="C")
        draw(c, EC["hill"], W/2, H/2); draw(c, EC["cross"], W/2, H/2)
        light_shaft(c, 1150, 120 + 220 * gap, 720, 200 + 420 * gap, "#FFD99A", 0.25 + 0.4 * gap, t, y_top=-60, y_bot=830)
        fx_, fy, fs = 880, 812, 0.6
        rim(c, P["back"], fx_, fy, fs, "#FFD89A", -4, -4, 0.95)
        draw(c, tinted(P["back"], "#0B0D10"), fx_, fy, sx=fs, sy=fs * (1 + 0.008 * math.sin(t * 1.6)))
    with_cam(c, z, W/2 + 40, H/2 - 30 * (1 - ease_io(t / d)), world)
    R4.draw(c, t * 0.6, 0.55)
    grade(c, "#1A2030", 0.25, "multiply"); vignette(c, 0.8); letterbox(c, 1.0, 110)
    # el yazısı "Athelstan" (soldan açılır)
    if t > 1.9:
        p = ease_out(lin(t, 1.9, 3.2))
        sp = NAME
        c.save(); c.clipRect(skia.Rect(W/2 - sp.w / 2, 0, W/2 - sp.w / 2 + sp.w * p, H))
        draw(c, sp, W/2, 900, 1.0, a=0.95)
        c.restore()

def with_cam(c, z, cx, cy, fn):
    z = max(1.0, z); hw, hh = W / (2 * z), H / (2 * z)
    cx = min(max(cx, hw), W - hw); cy = min(max(cy, hh), H - hh)
    c.save(); c.translate(W/2, H/2); c.scale(z, z); c.translate(-cx, -cy); fn(); c.restore()

def post_A(c, warm=False):
    gradient_grade(c, "#2A4A6E", "#1A2A3A", 0.5, "soft"); grade(c, "#9EB6CC", 0.16, "multiply")
    if warm: grade(c, "#FFB070", 0.08, "screen")
    vignette(c, 0.72); letterbox(c, 1.0, 70)

R1 = Rain(560, seed=9, angle=10); R2 = Rain(420, seed=11, angle=8); R3 = Rain(300, seed=13, angle=6, length=(40, 90)); R4 = Rain(300, seed=15, angle=8)
NAME = label("Athelstan", 92, font="Caveat Brush", color="#F6ECD4", sw=8)

SHOTS = [(shot1, 4.2), (shot2, 3.4), (shot3, 4.2), (shot4, 4.2)]

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
        render([(0, 0.6), (1, 0.4), (1, 0.6), (2, 0.6), (3, 0.85)])
    else:
        render()
