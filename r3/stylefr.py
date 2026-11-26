import math
import sys, math, random
sys.path.insert(0, "/home/claude/r3")
import skia
from engine import *
from art2 import *
from bg import GRAIN, grain, clouds, mountains, pines
from fx import *

def S(body, w=W, h=H, ss=1.0, ax=None, ay=None):
    return sprite(body, w, h, ax=ax, ay=ay, ss=ss, defs=f"<defs>{GRAIN}</defs>")

CROSS_CHEST = f'<g transform="translate(0,-300)"><path d="M0,-40 L0,0" stroke="#C9A25A" stroke-width="3"/><rect x="-4" y="0" width="8" height="30" fill="#C9A25A" stroke="{INK}" stroke-width="2.5"/><rect x="-12" y="7" width="24" height="7" fill="#C9A25A" stroke="{INK}" stroke-width="2.5"/></g>'
MOURN = dict(RAGNAR_LOD, hair_style="bald", hair="#B9853F", tunic="#5A4A40", trim="#8A7A68", cloak="#2E3A48", fur_collar="#7A7468", chest=CROSS_CHEST)

def forest(style):
    """3 sıra orman: her sıra kendi sırtına oturur (gövdeler gömülür), uzak sıra sise karışır."""
    import random as _r
    C = style == "C"
    rows = [  # (taban_y, dalga, hmin, hmax, renk, sırt rengi, adet, x aralıkları)
        (560, 10, 50, 95, "#5A6772" if not C else "#1C2026", "#56626D" if not C else "#1C2026", 46, [(0, 1920)]),
        (615, 14, 95, 160, "#48574F" if not C else "#16191E", "#435149" if not C else "#16191E", 30, [(-40, 1010), (1450, 1960)]),
        (668, 18, 150, 240, "#37463D" if not C else "#101216", "#334038" if not C else "#101216", 18, [(-60, 980), (1470, 1980)])]
    out = []
    for ri, (by, amp, hmin, hmax, c, rc, n, ranges) in enumerate(rows):
        rr = _r.Random(40 + ri)
        yb = lambda x: by + amp * math.sin(x / 260 + ri) + amp * 0.5 * math.sin(x / 97 + 2 * ri)
        for _ in range(n):
            a, b = rr.choice(ranges); x = rr.uniform(a, b); hh = rr.uniform(hmin, hmax); ww = hh * rr.uniform(0.34, 0.46)
            base = yb(x) + rr.uniform(4, 14); tiers = 3 if hh > 120 else 2
            d = f"M{x:.0f},{base-hh:.0f} "
            for k in range(tiers):
                f0 = (k + 1) / tiers; wk = ww * (0.35 + 0.65 * f0)
                d += f"L{x+wk*0.5:.0f},{base-hh*(1-f0)+(hh*0.08 if k<tiers-1 else 0):.0f} L{x+wk*0.22:.0f},{base-hh*(1-f0)+(hh*0.08 if k<tiers-1 else 0)-hh*0.05:.0f} " if k < tiers - 1 else f"L{x+wk*0.5:.0f},{base:.0f} "
            for k in reversed(range(tiers)):
                f0 = (k + 1) / tiers; wk = ww * (0.35 + 0.65 * f0)
                d += f"L{x-wk*0.22:.0f},{base-hh*(1-f0)+hh*0.08-hh*0.05:.0f} L{x-wk*0.5:.0f},{base-hh*(1-f0)+hh*0.08:.0f} " if k < tiers - 1 else f"L{x-wk*0.5:.0f},{base:.0f} "
            out.append(f'<path d="{d}Z" fill="{c}"/>')
            if not C and ri > 0:
                out.append(f'<path d="M{x:.0f},{base-hh:.0f} L{x+ww*0.18:.0f},{base-hh*0.62:.0f} L{x:.0f},{base-hh*0.7:.0f} Z" fill="#FFFFFF" opacity="0.07"/>')
        pts = " ".join(f"L{x},{yb(x):.0f}" for x in range(-20, 1960, 40))
        out.append(f'<path d="M-20,1080 {pts} L1960,1080 Z" fill="{rc}"/>')
        if not C:
            out.append(f'<defs><linearGradient id="fg{ri}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#B8C4CE" stop-opacity="0"/><stop offset="0.6" stop-color="#B8C4CE" stop-opacity="{0.22 if ri==0 else 0.12}"/><stop offset="1" stop-color="#B8C4CE" stop-opacity="0"/></linearGradient></defs>'
                       f'<rect x="0" y="{by-110}" width="1920" height="150" fill="url(#fg{ri})"/>')
    return "".join(out)

def env_layers(style, grave_on=True):
    soft = style == "B"
    sk = "#3E4A58" if style != "C" else "#22262E"
    sky_ = (f'<defs><linearGradient id="g1" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{sk}"/><stop offset="0.55" stop-color="#7C8C9A"/><stop offset="1" stop-color="#B8C2C8"/></linearGradient>'
            f'<radialGradient id="gap" cx="0.62" cy="0.18" r="0.35"><stop offset="0" stop-color="#FFF4D8" stop-opacity="{0.95 if style=="C" else 0.75}"/><stop offset="1" stop-color="#FFF4D8" stop-opacity="0"/></radialGradient></defs>'
            f'<rect width="{W}" height="{H}" fill="url(#g1)"/><rect width="{W}" height="{H}" fill="url(#gap)"/>' + clouds(W, 140, "#56626E" if style != "C" else "#1A1E26", 9, 4, 1.6, 0.95) + clouds(W, 300, "#6A7684" if style != "C" else "#262A32", 7, 9, 1.2, 0.8))
    far_c = "#4E5A66" if style != "C" else "#1E2228"
    far = mountains(W, 560, far_c, snow="#7C8894" if style != "C" else far_c, seed=21, hmin=200, hmax=330)
    stroke = "" if soft or style == "C" else f' stroke="{INK}" stroke-width="6"'
    cl = "#4E5A52" if style == "A" else "#56645C" if style == "B" else "#0E1013"
    cliff = (f'<path d="M1020,1080 L1060,420 Q1120,330 1240,320 L1300,330 L1310,1080 Z" fill="{cl}"{stroke}/>'
             f'<path d="M1440,1080 L1430,330 Q1520,300 1640,340 Q1760,380 1920,360 V1080 Z" fill="{cl}"{stroke}/>'
             + ("" if style == "C" else f'<path d="M1080,500 l60,40 M1100,640 l50,20 M1460,480 l70,30 M1520,620 l80,10" stroke="{shade(cl,0.7)}" stroke-width="8" stroke-linecap="round"/>'))
    trees = forest(style)
    gc = "#5E6E4E" if style == "A" else "#6A7A58" if style == "B" else "#0C0E10"
    hill = (f'<path d="M0,1080 L0,820 Q300,700 620,690 Q900,690 1100,760 Q1300,830 1920,860 V1080 Z" fill="{gc}"{stroke}/>'
            + ("" if style == "C" else "".join(f'<path d="M{x},{y} l-6,-22 M{x+8},{y} l4,-26 M{x+16},{y} l10,-20" stroke="{shade(gc,0.75)}" stroke-width="4" stroke-linecap="round"/>' for x, y in ((120, 860), (260, 820), (420, 790), (980, 760), (1500, 900), (1700, 940), (760, 760)))))
    mound_c = "#4A3A2C" if style != "C" else "#0C0E10"
    grave = (f'<ellipse cx="640" cy="740" rx="190" ry="44" fill="{mound_c}"{stroke}/>'
             + "".join(f'<ellipse cx="{x}" cy="{y}" rx="26" ry="16" fill="{"#7E7A72" if style!="C" else "#0C0E10"}"{stroke.replace("6","4")}/>' for x, y in ((470, 750), (520, 768), (590, 778), (680, 780), (760, 770), (810, 752))))
    wood = "#7A5A3A" if style != "C" else "#0C0E10"
    cross_ = f'<g transform="translate(640,720)"><rect x="-10" y="-190" width="20" height="200" fill="{wood}"{stroke.replace("6","5")}/><rect x="-62" y="-150" width="124" height="20" fill="{wood}"{stroke.replace("6","5")}/><path d="M-8,-135 l16,16 M8,-135 l-16,16" stroke="#3A2A1A" stroke-width="5"/></g>'
    tex = grain(W, H) + ('<rect width="1920" height="1080" filter="url(#parch)" opacity="0.6"/>' if soft else "")
    return dict(sky=S(sky_), far=S(far), cliff=S(trees + cliff), hill=S(hill + (grave if grave_on else '')), cross=S(cross_), tex=S(f'<rect width="{W}" height="{H}" fill="none"/>' + tex))

def waterfall(c, t, x0=1310, x1=1440, y0=330, y1=900, style="A"):
    p = skia.Paint(AntiAlias=True, StrokeCap=skia.Paint.kRound_Cap)
    c.drawRect(skia.Rect(x0, y0, x1, y1), skia.Paint(Color4f=col("#9FB8C8" if style != "C" else "#C8D8E8", 0.85)))
    r = random.Random(4)
    for i in range(46):
        x = r.uniform(x0 + 6, x1 - 6); L = r.uniform(60, 180); sp = r.uniform(380, 620); ph = r.uniform(0, 1000)
        y = y0 + ((t * sp + ph) % (y1 - y0 + L)) - L
        p.setStrokeWidth(r.uniform(3, 7)); p.setColor4f(col("#FFFFFF", r.uniform(0.35, 0.8)))
        c.drawLine(x, max(y0, y), x, min(y1, y + L), p)
    for k in range(14):
        ph = (t * 0.35 + k / 14) % 1
        bloom_spot(c, (x0 + x1) / 2 + math.sin(k * 2.1) * 90, y1 - 10 - ph * 120, 70 + ph * 80, "#E8F0F6", 0.25 * (1 - ph))

def frame(style, t, out=None, cam_z=None):
    L = env_layers(style)
    rag = char_sprite(character(MOURN, "adult", "hold_front", "sad"), ss=1.3)
    surf = skia.Surface(W, H); c = surf.getCanvas()
    z = cam_z if cam_z is not None else 1.0 + 0.06 * min(1, t / 3)
    c.save(); c.translate(W / 2, H / 2); c.scale(z, z); c.translate(-W / 2 - 40 * (z - 1) * 10, -H / 2)
    draw(c, L["sky"], W / 2, H / 2)
    if style == "A": draw(c, blurred(L["far"], 6), W / 2 + 10 * math.sin(t * 0.1), H / 2)
    else: draw(c, L["far"], W / 2, H / 2)
    if style != "C": fog(c, t, 600, "#C8D4DE", 0.45, seed=3)
    draw(c, L["cliff"], W / 2, H / 2)
    waterfall(c, t, style=style)
    if style != "C": fog(c, t, 860, "#D8E2EA", 0.35, seed=7, speed=20)
    draw(c, L["hill"], W / 2, H / 2)
    # ışık şaftı mezara
    light_shaft(c, 1190, 260, 650, 520, "#FFF0C8", 0.38 if style != "C" else 0.55, t, y_top=-60, y_bot=820)
    draw(c, L["cross"], W / 2, H / 2)
    bloom_spot(c, 640, 560, 160, "#FFF2CC", 0.25)
    rx, ry, rs = 900, 1010, 0.95
    if style == "C":
        draw(c, tinted(rag, "#0B0D10"), rx, ry, rs)
        rim(c, rag, rx, ry, rs, "#FFD89A", dx=-4, dy=-3, a=0.95)
        draw(c, tinted(rag, "#0B0D10"), rx + 1, ry, rs)
    else:
        shadow_drop(c, rag, rx + 20, ry, rs, a=0.25, skew=-0.6)
        rim(c, rag, rx, ry, rs, "#E4F0FF" if style == "A" else "#FFE6C0", dx=-6, dy=-3, a=0.85)
        draw(c, rag, rx, ry, rs)
    c.restore()
    rain = Rain(520 if style != "B" else 380, seed=9, angle=10)
    rain.draw(c, t, 0.9 if style != "C" else 0.6); rain.splashes(c, t, 760, 1060, 50, alpha=0.5)
    if style == "A":
        gradient_grade(c, "#2A4A6E", "#1A2A3A", 0.55, "soft"); grade(c, "#9EB6CC", 0.18, "multiply"); vignette(c, 0.7); letterbox(c, 1.0, 70)
    elif style == "B":
        gradient_grade(c, "#6E7E9E", "#E0B07A", 0.45, "soft"); draw(c, L["tex"], W / 2, H / 2, a=0.9); vignette(c, 0.45)
    else:
        grade(c, "#1A2030", 0.25, "multiply"); vignette(c, 0.8); letterbox(c, 1.0, 110)
    if out: surf.makeImageSnapshot().save(out, skia.kPNG)
    return surf

if __name__ == "__main__":
    import os; os.makedirs("/home/claude/r3/style", exist_ok=True)
    for s in "ABC":
        frame(s, 1.7, f"/home/claude/r3/style/style_{s}.png")
    print("ok")

def back_kneel(skin="#F0C49C", cloak="#2E3A48", fur="#7A7468", stub="#B9853F", reach=True):
    """Sırttan görünen, diz çökmüş, başı eğik figür; ayak tabanı (0,0)."""
    o = []
    # dizler/çizme tabanları (arkadan görünen)
    for sx in (-1, 1):
        o.append(f'<ellipse cx="{sx*52}" cy="-10" rx="40" ry="18" fill="#3A2818" stroke="{INK}" stroke-width="5"/>')
    # uzanan kol (sol, mezara doğru)
    if reach:
        o.append(limb([(-70, -200), (-150, -130), (-230, -60)], 34, "#5A4A40"))
        o.append(f'<ellipse cx="-240" cy="-52" rx="20" ry="14" fill="{skin}" stroke="{INK}" stroke-width="4"/>')
    # pelerin
    o.append(f'<path d="M-95,-250 Q-150,-120 -140,0 L140,0 Q150,-120 95,-250 Q0,-270 -95,-250 Z" fill="{cloak}" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>')
    o.append(f'<path d="M30,-240 Q70,-120 60,-6" stroke="{shade(cloak,0.75)}" stroke-width="30" fill="none" opacity="0.8"/>')
    o.append(f'<path d="M-60,-230 Q-90,-130 -80,-10" stroke="{shade(cloak,1.25)}" stroke-width="10" fill="none" opacity="0.5"/>')
    # kürk yaka
    for i in range(9):
        t = i / 8; x = -110 + 220 * t; y = -258 + 10 * math.sin(t * math.pi)
        o.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="22" fill="{fur}" stroke="{INK}" stroke-width="4"/>')
    # baş (eğik, arkadan, traşlı)
    o.append(f'<ellipse cx="-58" cy="-292" rx="11" ry="16" fill="{skin}" stroke="{INK}" stroke-width="4"/><ellipse cx="58" cy="-292" rx="11" ry="16" fill="{skin}" stroke="{INK}" stroke-width="4"/>')
    o.append(f'<ellipse cx="0" cy="-300" rx="62" ry="66" fill="{skin}" stroke="{INK}" stroke-width="5"/>')
    o.append(f'<ellipse cx="0" cy="-310" rx="56" ry="56" fill="{stub}" opacity="0.35"/>')
    o.append(f'<path d="M-26,-340 q10,24 4,50 M8,-350 q6,22 -2,48 M30,-336 q-4,20 4,40" stroke="#9A2E24" stroke-width="4" fill="none" opacity="0.55" stroke-linecap="round"/>')
    o.append(f'<path d="M20,-350 Q46,-330 50,-296" stroke="{shade(skin,0.82)}" stroke-width="14" fill="none" opacity="0.8"/>')
    return "".join(o)

def frame2(style, t, out=None, push=True):
    L = env_layers(style)
    fig = char_sprite(back_kneel(), ss=1.3, w=700, h=600, foot=560)
    surf = skia.Surface(W, H); c = surf.getCanvas()
    p = min(1, t / 4) if push else 0.6
    z = 1.0 + 0.10 * (p * p * (3 - 2 * p)); cx = W / 2 - 160 * (z - 1) / 0.10 * 0.5
    c.save(); c.translate(W / 2, H / 2); c.scale(z, z); c.translate(-cx, -H / 2 - 30 * (z - 1) / 0.1)
    draw(c, L["sky"], W / 2, H / 2)
    draw(c, blurred(L["far"], 7) if style != "C" else L["far"], W / 2, H / 2)
    if style != "C": fog(c, t, 600, "#C8D4DE", 0.45, seed=3)
    draw(c, L["cliff"], W / 2, H / 2)
    waterfall(c, t, style=style)
    if style != "C": fog(c, t, 860, "#D8E2EA", 0.35, seed=7, speed=20)
    draw(c, L["hill"], W / 2, H / 2)
    sh_a = (0.30 + 0.25 * min(1, t / 3)) if style != "C" else 0.6
    light_shaft(c, 1150, 240, 700, 560, "#FFF0C8", sh_a, t, y_top=-60, y_bot=830)
    draw(c, L["cross"], W / 2, H / 2, sy=1.0)
    bloom_spot(c, 640, 560, 180, "#FFF2CC", 0.22 + 0.1 * min(1, t / 3))
    fx_, fy, fs = 900, 815, 0.62
    breath = 1 + 0.008 * math.sin(t * 1.6)
    if style == "C":
        rim(c, fig, fx_, fy, fs, "#FFD89A", dx=-4, dy=-4, a=0.95, sy=fs * breath)
        draw(c, tinted(fig, "#0B0D10"), fx_, fy, sx=fs, sy=fs * breath)
    else:
        rim(c, fig, fx_, fy, fs, "#FFF0D0" if style == "A" else "#FFE0B0", dx=-4, dy=-5, a=0.9, sy=fs * breath)
        draw(c, fig, fx_, fy, sx=fs, sy=fs * breath)
    c.restore()
    rain = Rain(560 if style != "B" else 400, seed=9, angle=10)
    rain.draw(c, t, 0.9 if style != "C" else 0.65); rain.splashes(c, t, 760, 1060, 50, alpha=0.5)
    if style == "A":
        gradient_grade(c, "#2A4A6E", "#1A2A3A", 0.55, "soft"); grade(c, "#9EB6CC", 0.18, "multiply"); vignette(c, 0.72); letterbox(c, 1.0, 70)
    elif style == "B":
        gradient_grade(c, "#6E7E9E", "#E0B07A", 0.45, "soft"); draw(c, L["tex"], W / 2, H / 2, a=0.9); vignette(c, 0.45)
    else:
        grade(c, "#1A2030", 0.25, "multiply"); vignette(c, 0.8); letterbox(c, 1.0, 110)
    if out: surf.makeImageSnapshot().save(out, skia.kPNG)
    return surf
