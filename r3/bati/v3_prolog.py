"""Prolog ham kareleri P1a-P3c (brief: kurul/BRIEF_prolog.md). python3 v3_prolog.py [p1a ... | test | all]
Çıktı: /home/claude/r3/prolog/<id>.png, kontakt_prolog_960.png, cocuk_deneme.png, <id>_crop1/2.png"""
import sys, os, math, random
sys.path.insert(0, "/home/claude/r3/bati")
from v3_c import *
import v3_a as A
import v3_b as Bm
from modeller import GYDA
from art3 import forearm_band
OUTP = "/home/claude/r3/prolog"; os.makedirs(OUTP, exist_ok=True)
SK = A.SKO; SK2 = A.SKO2; SK3 = A.SKO3
GR = A.GRAD
def S(*p): return svg_sprite("".join(p))
def SD(*p): return svg_sprite(GR + TEXD + "".join(p))

# ------------------------------------------------------------------ ortak yardımcılar
def sea_svg(y0, top, bot, gx, seed, glint="#FFE6B0", wl="#243644", hl="#C8D8E4", gn=150, ga=1.0, spread=0.5):
    r = R_(seed); o = [f'<defs>{gradient("sea%d" % seed, [(0, top), (1, bot)])}</defs>', f'<rect y="{y0}" width="1920" height="{1080-y0}" fill="url(#sea{seed})"/>']
    for k in range(130):
        y = y0 + 6 + (k / 130) ** 1.6 * (1080 - y0); x = r.uniform(-140, 1900); w_ = 30 + (y - y0) * 1.1; sw = 1 + (y - y0) * 0.012
        o.append(f'<path d="M{x:.0f},{y:.0f} q{w_*0.25:.0f},-{2+(y-y0)*0.03:.1f} {w_*0.5:.0f},0 q{w_*0.25:.0f},{1+(y-y0)*0.02:.1f} {w_*0.5:.0f},0" stroke="{wl}" stroke-width="{sw:.1f}" fill="none" opacity="0.6"/>'
                 f'<path d="M{x+w_*0.1:.0f},{y-2-(y-y0)*0.02:.0f} q{w_*0.2:.0f},-{1+(y-y0)*0.02:.1f} {w_*0.4:.0f},0" stroke="{hl}" stroke-width="{sw*0.7:.1f}" fill="none" opacity="0.4"/>')
    for k in range(gn):
        y = y0 + 4 + (k / gn) ** 1.3 * (1080 - y0) * 0.85; sp = 14 + (y - y0) * spread; x = gx + r.gauss(0, sp * 0.5); w_ = r.uniform(8, 24) + (y - y0) * 0.12
        o.append(f'<path d="M{x-w_/2:.0f},{y:.0f} h{w_:.0f}" stroke="{glint}" stroke-width="{1.5+(y-y0)*0.012:.1f}" stroke-linecap="round" opacity="{ga*r.uniform(0.35, 0.9):.2f}"/>')
    return "".join(o)

def capsule(d, w, fill, sh=SK2, hl="#F2D4B4", ink=INK):
    return (f'<path d="{d}" stroke="{ink}" stroke-width="{w+10:.0f}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="{d}" stroke="{fill}" stroke-width="{w:.0f}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="{d}" transform="translate(0,{w*0.24:.1f})" stroke="{sh}" stroke-width="{w*0.4:.1f}" fill="none" stroke-linecap="round" opacity="0.75"/>'
            f'<path d="{d}" transform="translate(0,{-w*0.26:.1f})" stroke="{hl}" stroke-width="{w*0.16:.1f}" fill="none" stroke-linecap="round" opacity="0.75"/>')

def foam_line(x0, x1, y, seed, a=0.8, amp=6):
    r = R_(seed); o = []
    x = x0
    while x < x1:
        l = r.uniform(30, 90); o.append(f'<path d="M{x:.0f},{y + r.uniform(-amp, amp):.0f} q{l/2:.0f},{-r.uniform(3, 9):.0f} {l:.0f},0" stroke="#F2F6F8" stroke-width="{r.uniform(2, 5):.1f}" fill="none" stroke-linecap="round" opacity="{a*r.uniform(0.5, 1):.2f}"/>'); x += l * r.uniform(0.7, 1.5)
    return "".join(o)

def sparks(c, x, y, n, h, seed, col_="#FFC070", w=120):
    for j in range(n):
        q = R_(seed + j); c.drawCircle(x + q.uniform(-w, w), y - q.uniform(0, h), q.uniform(1.4, 3.4), skia.Paint(AntiAlias=True, Color4f=col(col_, q.uniform(0.4, 0.95))))

def grass(x0, x1, y0, y1, n, seed, cols=("#3A3A1E", "#5A5A2C", "#7A7A3E"), hmin=20, hmax=70, lean=18):
    r = R_(seed); o = []
    for _ in range(n):
        x = r.uniform(x0, x1); y = r.uniform(y0, y1); h = r.uniform(hmin, hmax) * (0.5 + (y - y0) / max(1, y1 - y0)); l = r.uniform(-lean, lean * 1.6)
        o.append(f'<path d="M{x:.0f},{y:.0f} Q{x + l*0.3:.0f},{y - h*0.6:.0f} {x + l:.0f},{y - h:.0f}" stroke="{r.choice(cols)}" stroke-width="{r.uniform(2, 4):.1f}" fill="none" stroke-linecap="round"/>')
    return "".join(o)

def rock(x, y, w, h, seed, col="#4A4650", lit="#8A8090", dark="#1E1C22", ldir=1):
    r = R_(seed); n = 9; pts = []
    for k in range(n):
        a = math.pi * k / (n - 1); pts.append((x + math.cos(a) * w * r.uniform(0.85, 1.05), y - math.sin(a) * h * r.uniform(0.8, 1.05)))
    d = f"M{x - w:.0f},{y:.0f} " + " ".join(f"L{px:.0f},{py:.0f}" for px, py in pts[::-1]) + f" L{x + w:.0f},{y:.0f} Z"
    return (f'<ellipse cx="{x + w*0.1:.0f}" cy="{y + 4:.0f}" rx="{w*1.15:.0f}" ry="{h*0.14:.0f}" fill="#000" opacity="0.4"/><path d="{d}" fill="{col}" filter="url(#t_tas)"/><path d="{d}" fill="{col}" opacity="0.6"/>'
            f'<path d="M{x - w*0.9:.0f},{y - h*0.3:.0f} L{x - w*0.3:.0f},{y - h*0.9:.0f} L{x + w*0.2:.0f},{y - h*0.95:.0f} L{x - w*0.1:.0f},{y - h*0.35:.0f} Z" fill="{lit}" opacity="0.4"/>'
            f'<path d="M{x + w*0.3:.0f},{y - h*0.8:.0f} L{x + w:.0f},{y:.0f} L{x + w*0.1:.0f},{y:.0f} Z" fill="{dark}" opacity="0.45"/><path d="{d}" fill="none" stroke="{dark}" stroke-width="4" stroke-linejoin="round"/>'
            f'<path d="M{x - w*0.5:.0f},{y - h*0.5:.0f} l{w*0.3:.0f},{h*0.2:.0f} M{x + w*0.1:.0f},{y - h*0.7:.0f} l{w*0.2:.0f},{h*0.5:.0f}" stroke="{dark}" stroke-width="2.5" opacity="0.7"/>')

def sitfig(spec, expr, s, look=None, view="front"):
    return sprite(f'<g transform="translate(400,1000) scale({s})">{figure(spec, view, "sit", expr, hands=("open", "open"), look=look)}</g>', 800, 1100, ax=400, ay=1000, ss=1.0)

def backfig(spec, s, w=1000, h=1300):
    return sprite(f'<g transform="translate({w/2},{h-60}) scale({s})">{figure(spec, "back", "stand", "neutral")}</g>', w, h, ax=w / 2, ay=h - 60, ss=1.0)

CH, CHD = 0.72, 0.62      # çocuk boy oranları: Bjorn(12), Gyda(10)

# ------------------------------------------------------------------ boy denemesi
def test():
    s = skia.Surface(W, H); c = s.getCanvas(); c.clear(col("#2A2018").toColor())
    draw(c, S('<rect width="1920" height="1080" fill="#2A2018"/><rect y="960" width="1920" height="120" fill="#3A2C1E"/>'), 0, 0, 1.0)
    lst = ((RG, "Ragnar", 1.0, "determined"), (LAGv, "Lagertha", 0.97, "determined"), (dict(BJv), "Bjorn 12", CH, "awe"), (GYDA, "Gyda 10", CHD, "tender"))
    for k, (sp, nm, sc, e) in enumerate(lst):
        f = full(sp, e, 0.9, facing=1, look=0.3); x = 330 + k * 420
        draw(c, f, x, 960, sc)
        draw(c, name_card(nm), x, 190, 0.7)
    s.makeImageSnapshot().save(f"{OUTP}/cocuk_deneme.png", skia.kPNG)

# ================================================================== P1a · şafakta gemi
def p1a():
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    sky = (f'<defs>{gradient("sk1", [(0, "#2A3658"), (0.35, "#6A6C94"), (0.7, "#E0A27A"), (1, "#FFD9A0")])}</defs><rect width="1920" height="600" fill="url(#sk1)"/>')
    draw(c, S(sky), 0, 0, 1.0)
    glow(c, 1010, 540, 620, "#FFC880", 0.55); glow(c, 1010, 540, 200, "#FFF0D0", 0.7)
    cl = (cloud_band(11, 10, -100, 800, 120, 330, "#3A4064", "#F0A870", 0.95, lit_dy=10, rx=(220, 460), ry=(30, 60)) + cloud_band(12, 10, 1250, 2050, 110, 330, "#3A4064", "#F0A870", 0.95, lit_dy=10, rx=(220, 460), ry=(30, 60))
          + cloud_band(13, 8, 300, 1700, 40, 150, "#454C74", "#D89080", 0.8, lit_dy=8, rx=(240, 480), ry=(22, 44)) + cloud_band(14, 10, -100, 2000, 380, 470, "#B88A8A", "#FFD0A0", 0.55, lit_dy=-6, rx=(200, 420), ry=(12, 24)))
    draw(c, blurred(S(cl), 5), 0, 0, 1.0)
    rays(c, 1010, 300, 90, 1000, 42, 11, "#FFE0A8", 0.13, t or 0.0)
    draw(c, S(mountain_range(21, -40, 1960, 592, 470, 50, "#5A4A6A", "#8A6070", light=-1, stroke="#3A2E48", cid="pa") + mountain_range(22, -40, 1960, 600, 520, 28, "#6A5A78", "#9A7078", light=-1, stroke="#3A2E48", cid="pb")), 0, 0, 1.0)
    draw(c, blurred(S(cloud_band(15, 14, -100, 2000, 540, 600, "#E8C8B0", "#FFE4C0", 0.5, rx=(260, 520), ry=(14, 30))), 6), 0, 0, 1.0)
    draw(c, S(sea_svg(588, "#C8967C", "#1E2C3E", 1010, 31, glint="#FFE8B8", wl="#3A3C54", hl="#F0C8A0", spread=0.65)), 0, 0, 1.0)
    # filo: gerçek gemiler (uzak, sisli)
    fl = "".join(f'<g transform="translate({x},{y}) scale({s_})">{G.mast_sail(1.2)}{G.hull(1.0, shields=True, oars=False)}</g>' for x, y, s_ in ((250, 640, 0.30), (1560, 622, 0.22), (1760, 606, 0.14), (520, 612, 0.12)))
    f_ = blurred(S(fl), 1.6); draw(c, f_, 0, 0, 1.0); draw(c, tinted(f_, "#D8A890"), 0, 0, 1.0, a=0.35)
    draw(c, blurred(S(cloud_band(16, 9, -100, 2000, 598, 660, "#F0D0B0", "#FFE8C8", 0.35, rx=(220, 480), ry=(12, 22))), 8), 0, 0, 1.0)
    # ana gemi: sağ arkada, şafak ışığında
    sx, sy, ss = 1190, 800, 0.86
    draw(c, S(f'<g transform="translate({sx},{sy}) scale({ss})">{G.mast_sail(1.2)}</g>'), 0, 0, 1.0)
    glow(c, sx + 20, sy - 330, 320, "#FFD08A", 0.22)
    hull = G.hull(1.0, shields=True, oars=False, wet=True)
    draw(c, S(f'<g transform="translate({sx},{sy}) scale({ss})">{hull}</g>'), 0, 0, 1.0)
    glow(c, sx, sy - 60, 380, "#FFB070", 0.10)
    RGp = fig_bust(dict(RG), ex("determined", IF.blink_at(0.3)), 0.8, 2.35)
    bx_, by_ = 560, 470
    with live(c, bx_, by_ + 600, phase=0.2, breathe=0.004, sway=0.012):
        rim(c, RGp, bx_, by_, 1.0, "#FFC888", dx=7, dy=-3, a=0.95); rim(c, RGp, bx_, by_, 1.0, "#FFE8B8", dx=3, dy=-4, a=0.5)
        draw(c, RGp, bx_, by_, 1.0); shade_side(c, RGp, bx_, by_, 0.42, bx_ + 220, bx_ - 200, "#1A1020")
    glow(c, bx_ + 260, by_ + 40, 260, "#FFC070", 0.14)
    # su çizgisi: köpük, dalga kırığı, gövde yansıması
    draw(c, S(f'<rect x="{sx-470}" y="{sy+66}" width="960" height="60" fill="#2A2C42" opacity="0.55"/>' + foam_line(sx - 500, sx + 520, sy + 70, 5, 0.9, 5) + foam_line(sx - 400, sx + 480, sy + 92, 6, 0.6, 5) + foam_line(sx - 300, sx + 420, sy + 118, 7, 0.4, 6)), 0, 0, 1.0)
    for k in range(40):
        q = R_(k + 90); y = sy + 100 + q.uniform(0, 120); x = sx + q.uniform(-420, 420)
        c.drawLine(x, y, x + q.uniform(14, 60), y, skia.Paint(AntiAlias=True, StrokeWidth=2, Color4f=col("#F0C8A0", q.uniform(0.2, 0.5))))
    # ön plan: iri dalga sırtı + serpinti + martılar
    fgw = ('<path d="M-40,1090 L-40,955 Q200,900 440,950 Q640,990 860,990 Q1200,990 1500,930 Q1760,880 1960,940 L1960,1090 Z" fill="#141C2A"/>'
           '<path d="M-40,968 Q200,916 440,962 Q640,1000 860,1000 Q1200,1000 1500,942 Q1760,894 1960,950" stroke="#6A8AA8" stroke-width="6" fill="none" opacity="0.6"/>'
           + foam_line(-20, 1940, 950, 9, 0.9, 12) + foam_line(-20, 1940, 985, 10, 0.5, 10)
           + "".join(f'<path d="M{x},{1090} q{(k%3-1)*30},-40 {(k%5-2)*24},-{70+k%4*20}" stroke="#E8F0F4" stroke-width="3" fill="none" opacity="0.35"/>' for k, x in enumerate(range(0, 1920, 90))))
    draw(c, S(fgw), 0, 0, 1.0)
    draw(c, blurred(S(fgw), 5), 0, 0, 1.0, a=0.0)
    r = R_(77)
    for k in range(90):
        x = r.gauss(300, 360) % 1920; y = 930 - abs(r.gauss(0, 120)); rr_ = r.uniform(2, 8)
        c.drawCircle(x, y, rr_, skia.Paint(AntiAlias=True, Color4f=col("#F4F8FA", r.uniform(0.3, 0.85))))
    for k in range(8): c.drawCircle(r.uniform(100, 1800), r.uniform(200, 900), r.uniform(12, 26), skia.Paint(AntiAlias=True, Color4f=col("#F8FCFF", 0.10), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 5)))
    draw(c, S("".join(C_gull(x, y, s_, f_, rot=r_) for x, y, s_, f_, r_ in ((520, 300, 0.5, 0.2, -6), (640, 250, 0.36, 0.9, 4), (1500, 330, 0.4, 0.5, 6), (1640, 290, 0.28, 0.1, -4), (1380, 230, 0.22, 0.7, 0)))), 0, 0, 1.0)
    draw(c, blurred(S(C_gull(1760, 160, 1.5, 0.4, rot=8)), 6), 0, 0, 1.0)
    card_at(c, "RAGNAR LOTHBROK", 1500, 175, "Kattegat çiftçisi")
    finish(c, cold=False, warm=0.08); return s

def C_gull(*a, **k): return gull(*a, **k)

# ================================================================== P1b · kral Ragnar
def p1b():
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    draw(c, blurred(place(P7.greathall(0.9)), 2), -384, -250, 1.4)
    # duvarlarda kalkanlar, asılı kürkler, boynuzlar
    wall = "".join(f'<g transform="translate({x},{y}) scale({sc})">' + KL.shield_svg(*cl_, style=k % 3).replace('translate(70,-330) scale(0.62)', 'translate(0,0) scale(0.75)') + '</g>'
                   for k, (x, y, sc, cl_) in enumerate(((140, 330, 0.62, ("#8E3B2E", "#D8C8A0")), (230, 440, 0.55, ("#2F4C6E", "#C9A25A")), (150, 560, 0.5, ("#5A6A3A", "#D8C8A0")), (1780, 340, 0.62, ("#2F4C6E", "#D8C8A0")), (1690, 450, 0.55, ("#8E3B2E", "#C9A25A")), (1770, 570, 0.5, ("#3A3A38", "#B8302A")))))
    wall += ('<path d="M40,250 q60,40 120,0 l-10,140 q-50,20 -100,0 Z" fill="#4A3424" filter="url(#t_kurk)"/><path d="M40,250 q60,40 120,0 l-10,140 q-50,20 -100,0 Z" fill="none" stroke="#0E0804" stroke-width="5"/>'
             '<path d="M1760,250 q60,40 120,0 l-10,150 q-50,20 -100,0 Z" fill="#5A4430" filter="url(#t_kurk)"/><path d="M1760,250 q60,40 120,0 l-10,150 q-50,20 -100,0 Z" fill="none" stroke="#0E0804" stroke-width="5"/>')
    draw(c, SD(wall), 0, 0, 1.0)
    rays(c, 960, -40, 90, 900, 20, 6, "#F6E6C0", 0.13, t or 0.0)
    # diz çöken savaşçılar (iki yan)
    for side, xs in ((1, (300, 460, 620)), (-1, (1300, 1460, 1620))):
        for k, x in enumerate(xs):
            sp = full(dict(KL.soldier_spec(200 + k + (3 if side < 0 else 0), "ragnar"), _kneel=200, _arm_up=False), "awe" if k % 2 else "neutral", 0.9, facing=side, look=0.5 * side)
            y = 965 - k * 14; sc = 0.78 - k * 0.04
            soft_shadow(c, x, y - 6, 90 * sc / 0.7, 14, 0.5)
            rim(c, sp, x, y, sc, "#FFB070", dx=-4 * side, dy=-2, a=0.6); draw(c, sp, x, y, sc); shade_side(c, sp, x, y, 0.4, x - 140 * side, x + 140 * side, "#140A06")
    # tahtta Ragnar
    RGsit = sitfig(dict(RG, armring=True), ex("determined", IF.blink_at(0.4)), 0.64)
    soft_shadow(c, 960, 660, 170, 18, 0.5)
    with live(c, 960, 640, phase=0.4, breathe=0.004):
        rim(c, RGsit, 960, 640, 1.0, "#FFD8A0", dx=-5, dy=-3, a=0.8); draw(c, RGsit, 960, 640, 1.0); shade_side(c, RGsit, 960, 640, 0.3, 1060, 860, "#140A06")
    # orta koridor: uzun ocak
    draw(c, SD(hearth(960, 1030, 0.62)), 0, 0, 1.0)
    flames(c, 790, 1130, 1004, 120, t, seed=2)
    glow(c, 960, 960, 520, "#FF7A2A", 0.28); glow(c, 960, 990, 200, "#FFC070", 0.35)
    sparks(c, 960, 960, 40, 560, 300, w=200)
    draw(c, blurred(place(cloud_band(94, 8, 700, 1200, 200, 800, "#5A4A40", "#7A6656", 0.20, rx=(80, 200), ry=(40, 90))), 14), 0, 0, 1.0)
    # ön plan çerçeve
    draw(c, blurred(SD(hall_fg_left()), 6), 0, 0, 1.0); draw(c, blurred(SD(hall_fg_right()), 5), 0, 0, 1.0)
    finish(c, cold=False, warm=0.06); return s

# ================================================================== P1c · tabuttan kalkan el
def grip_hand(x, y, s=1.0):
    """Tabut kenarını kavrayan el: yeşil yün kol + kürk manşet, önkolda düğüm bandı (art3.forearm_band), parmaklar kenarı sarar."""
    tun = RG.get("tunic", "#3B5A4A")
    o = [f'<g transform="translate({x},{y}) rotate(-8) scale({s})">']
    # yün kol (yukarıda geniş, kıvrımlı) + kürk manşet
    o.append(f'<defs><linearGradient id="fa" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0A0604" stop-opacity="0.5"/><stop offset="0.6" stop-color="#0A0604" stop-opacity="0.12"/><stop offset="1" stop-color="#0A0604" stop-opacity="0"/></linearGradient></defs>')
    sl = "M-70,-150 Q-120,-230 -108,-340 Q0,-366 110,-340 Q122,-230 72,-150 Q0,-134 -70,-150 Z"
    o.append(f'<path d="{sl}" fill="{tun}" filter="url(#t_yun)" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>')
    o.append('<path d="M-70,-170 Q-96,-250 -84,-330 M-10,-150 Q-16,-250 -4,-346 M50,-160 Q70,-250 64,-338 M-40,-160 Q-50,-230 -44,-300" stroke="#1A2E22" stroke-width="5" fill="none" opacity="0.7"/>')
    o.append(f'<path d="M30,-150 Q96,-190 98,-230 Q110,-290 104,-340 Q96,-250 40,-170 Z" fill="#000" opacity="0.25"/><path d="{sl}" fill="url(#fa)"/>')
    # önkol: bilekte dar, dirsekte geniş; düğüm bandı
    o.append(f'<path d="M-60,-20 Q-70,-80 -76,-146 L76,-146 Q72,-80 58,-20 Z" fill="{SK}" stroke="{INK}" stroke-width="8"/><path d="M22,-146 Q66,-80 58,-20 L26,-18 Q14,-80 -2,-146 Z" fill="{SK2}" opacity="0.7"/>')
    o.append(f'<g transform="translate(-66,-112) scale(1.16,1.0)">{forearm_band()}</g>')
    o.append('<path d="M-30,-60 q-6,-20 4,-40" stroke="#6A7A9A" stroke-width="5" fill="none" opacity="0.4" stroke-linecap="round"/>')
    o.append(f'<path d="M-92,-150 Q-100,-170 -70,-186 Q0,-198 76,-186 Q104,-170 96,-148 Q0,-124 -92,-150 Z" fill="#CFC3A0" filter="url(#t_kurk)" stroke="{INK}" stroke-width="7"/>'
             + "".join(f'<path d="M{-80 + k*22},{-176 + (k%2)*4} l{(k%3-1)*4},22" stroke="#7A6E54" stroke-width="3" opacity="0.8"/>' for k in range(9)))
    # elin sırtı
    o.append(f'<path d="M-100,-40 Q-110,10 -96,48 Q0,70 100,48 Q114,10 100,-40 Q0,-60 -100,-40 Z" fill="{SK}" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/><path d="M20,-44 Q80,-40 100,-40 Q114,10 100,48 Q60,60 30,60 Z" fill="{SK2}" opacity="0.6"/>')
    o.append('<path d="M-70,-20 L-66,34 M-24,-24 L-22,40 M24,-24 L24,40 M70,-20 L68,34" stroke="#B08A68" stroke-width="3" opacity="0.5"/><path d="M-80,-30 Q-40,-50 20,-48" stroke="#F4DCBC" stroke-width="4" fill="none" opacity="0.5"/>')
    for k, fx in enumerate((-72, -24, 26, 74)):
        L = (96, 108, 100, 84)[k]
        o.append(capsule(f"M{fx},40 Q{fx + (k-1.5)*3:.0f},{40 + L*0.7:.0f} {fx + (k-1.5)*5:.0f},{40 + L:.0f}", 40, SK, SK2))
        o.append(f'<path d="M{fx-14},{58} q14,8 28,0 M{fx-12},{40 + L*0.55:.0f} q12,8 24,0" stroke="{SK3}" stroke-width="3" fill="none"/><ellipse cx="{fx + (k-1.5)*5:.0f}" cy="{40 + L - 6:.0f}" rx="13" ry="10" fill="#E8C8A8" stroke="{INK}" stroke-width="4"/><path d="M{fx + (k-1.5)*5 - 8:.0f},{40 + L - 12:.0f} q8,-6 16,0" stroke="#6A5038" stroke-width="4" fill="none"/>')
        o.append(f'<circle cx="{fx}" cy="30" r="14" fill="{SK}" stroke="{SK3}" stroke-width="3"/><path d="M{fx-10},24 q10,-9 20,0" stroke="#F4DCBC" stroke-width="3" fill="none" opacity="0.85"/><path d="M{fx-8},38 q8,8 16,0" stroke="{SK3}" stroke-width="3" fill="none" opacity="0.8"/>')
        if k < 3: o.append(f'<path d="M{fx+25},56 L{fx+24},{40 + L*0.8:.0f}" stroke="#5A3A24" stroke-width="3" opacity="0.6"/>')
    o.append(capsule("M-96,-10 Q-150,10 -150,64", 42, SK, SK2))
    o.append(f'<path d="M-40,-10 l30,4 M40,14 l24,-6" stroke="#8A2A22" stroke-width="3" opacity="0.7"/><ellipse cx="60" cy="0" rx="10" ry="6" fill="#4A3A2A" opacity="0.4"/></g>')
    return "".join(o)

def p1c():
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    o = [GR, TEXD, f'<defs>{gradient("fl1c", [(0, "#2A2A30"), (1, "#14141A")])}</defs>', A.stone_wall(0, 0, 1920, 720, seed=41, wash=0.35, row=(80, 120), wd=(120, 240), base="#26241F")]
    # yuvarlak kemerli nef: kalın sütunlar + kemerler
    for cx in (330, 760, 1160, 1590):
        o.append(f'<rect x="{cx-52}" y="170" width="104" height="560" fill="#6A6558" filter="url(#t_tas)"/><rect x="{cx-52}" y="170" width="104" height="560" fill="none" stroke="#14100C" stroke-width="6"/>'
                 f'<rect x="{cx-70}" y="150" width="140" height="34" fill="#7A7468" stroke="#14100C" stroke-width="6"/><rect x="{cx-66}" y="708" width="132" height="30" fill="#5A5448" stroke="#14100C" stroke-width="6"/>'
                 f'<rect x="{cx+14}" y="184" width="38" height="526" fill="#000" opacity="0.28"/><rect x="{cx-50}" y="184" width="10" height="526" fill="#E8D4A8" opacity="0.14"/>')
    for a, b in ((330, 760), (760, 1160), (1160, 1590)):
        mid = (a + b) / 2; rad = (b - a) / 2 - 40
        o.append(f'<path d="M{a+52},170 A{rad},{rad*0.9:.0f} 0 0 1 {b-52},170" fill="none" stroke="#14100C" stroke-width="64"/><path d="M{a+52},170 A{rad},{rad*0.9:.0f} 0 0 1 {b-52},170" fill="none" stroke="#7A7468" stroke-width="50" filter="url(#t_tas)"/>'
                 f'<path d="M{a+52},170 A{rad},{rad*0.9:.0f} 0 0 1 {b-52},170" fill="none" stroke="#2A261E" stroke-width="3" stroke-dasharray="26 22"/>')
    o.append('<path d="M330,170 A215,190 0 0 0 -100,170 L-100,0 L330,0 Z M1590,170 A215,190 0 0 1 2020,170 L2020,0 L1590,0 Z" fill="#1E1C18"/>')
    # yüksek yuvarlak vitray
    cx_, cy_ = 960, 250
    o.append(f'<circle cx="{cx_}" cy="{cy_}" r="116" fill="#14100C"/>' + "".join(f'<path d="M{cx_},{cy_} L{cx_ + 104*math.cos(a):.0f},{cy_ + 104*math.sin(a):.0f} A104,104 0 0 1 {cx_ + 104*math.cos(a + math.pi/4):.0f},{cy_ + 104*math.sin(a + math.pi/4):.0f} Z" fill="{["#B8322A", "#2E4A9E", "#D8B04A", "#2E8A5E"][k % 4]}" stroke="#14100C" stroke-width="6"/>' for k, a in enumerate([k * math.pi / 4 for k in range(8)]))
             + f'<circle cx="{cx_}" cy="{cy_}" r="30" fill="#E8D4A8" stroke="#14100C" stroke-width="6"/><circle cx="{cx_}" cy="{cy_}" r="110" fill="none" stroke="#14100C" stroke-width="12"/>')
    # zemin: taş levhalar
    o.append('<path d="M0,1080 L0,720 L1920,720 L1920,1080 Z" fill="url(#fl1c)"/>')
    r = R_(4)
    for k in range(1, 9):
        y = 720 + (k / 9) ** 1.5 * 360; o.append(f'<path d="M0,{y:.0f} H1920" stroke="#0E0C0A" stroke-width="{2 + k*0.6:.1f}"/>')
    for k in range(-14, 15):
        o.append(f'<path d="M{960 + k*70},720 L{960 + k*190},1080" stroke="#0E0C0A" stroke-width="3"/>')
    # kürsü (katafalk) ve kırmızı kumaş
    o.append('<path d="M430,800 L1490,800 L1580,900 L340,900 Z" fill="#6A6458" filter="url(#t_tas)"/><path d="M430,800 L1490,800 L1580,900 L340,900 Z" fill="none" stroke="#14100C" stroke-width="7"/><path d="M340,900 L1580,900 L1620,960 L300,960 Z" fill="#4A463E" stroke="#14100C" stroke-width="7"/>'
             '<path d="M500,800 L1420,800 L1500,900 L420,900 Z" fill="#7A1E22" opacity="0.9"/><path d="M500,800 L1420,800 L1500,900 L420,900 Z" fill="none" stroke="#D8B04A" stroke-width="5"/>')
    draw(c, S(*o), 0, 0, 1.0)
    fill(c, "#0A0C14", 0.30)
    # vitray ışığı: renkli hüzmeler zemine
    for (x1, w1, cl_) in ((660, 120, "#C84A3A"), (880, 150, "#4A6AD8"), (1120, 130, "#E8C050")):
        A.beam(c, 960, 260, 60, x1, 760, w1, cl_, 0.16, 10)
    A.beam(c, 960, 250, 120, 960, 800, 520, "#CFE0F4", 0.10, 30)
    bloom_spot(c, 960, 250, 260, "#DCEAFF", 0.35)
    # mum sıraları (sütun diplerinde), ışık sıcak
    cn = []
    for k, x in enumerate((130, 240, 540, 560, 1360, 1380, 1690, 1800)):
        y = 770 + (k % 3) * 40; sc = 0.36 + (y - 770) / 400
        cn.append(f'<g transform="translate({x},{y}) scale({sc:.2f})">{A.candlestick(0, 0, 150 + (k % 3) * 30, k + 3)}</g>')
        bloom_spot(c, x, y - 230 * sc, 60 * sc + 20, "#FFC070", 0.45)
    # rahipler: şaşkın, cübbeli
    pri = []
    for k, (x, y, f_, sc, e) in enumerate(((210, 950, 1, 0.80, "horror"), (470, 880, 1, 0.64, "shock"), (1440, 880, -1, 0.64, "horror"), (1720, 950, -1, 0.80, "shock"), (900, 735, 1, 0.20, "shock"), (1030, 735, -1, 0.20, "shock"))):
        sp = full(monk(k * 4 + 2), e, 0.9, facing=f_, look=0.3 * f_)
        pri.append((sp, robe(0.9, f_), x, y, sc))
    draw(c, SD(*cn), 0, 0, 1.0)
    for sp, rb, x, y, sc in pri:
        soft_shadow(c, x, y - 4, 90 * sc / 0.4, 12, 0.5)
        rim(c, sp, x, y, sc, "#FFC888", dx=3, dy=-2, a=0.5); draw(c, sp, x, y, sc); draw(c, rb, x, y, sc)
    # tütsü: sallanan buhurdan + duman
    draw(c, blurred(S("".join(A.smoke_svg(1500 + k * 10, 560, 420, seed=k + 3, a=0.22, w=70).replace('stroke-width="', 'stroke-width="2') for k in range(5))), 9), 0, 0, 1.0)
    draw(c, SD(A.censer_svg(1500, 470)), 0, 0, 1.0)
    # devrilmiş şamdan: yerde, mum alevi yerde yanıyor
    draw(c, SD(f'<g transform="translate(280,990) rotate(80) scale(0.9)">{A.candlestick(0, 0, 150, 9)}</g>'), 0, 0, 1.0)
    flames(c, 228, 300, 972, 46, t, seed=9, a=0.9); glow(c, 270, 950, 160, "#FF9A40", 0.25)
    sparks(c, 270, 940, 10, 80, 800, w=30)
    # tabut: büyük ön plan
    cof = (f'<g transform="translate(0,0)"><path d="M380,1100 L380,860 L1560,860 L1560,1100 Z" fill="#3A2416" filter="url(#t_ahsap)"/><path d="M380,1100 L380,860 L1560,860 L1560,1100 Z" fill="none" stroke="{INK}" stroke-width="9"/>'
           + "".join(f'<path d="M{380+k*72},860 V1100" stroke="#1E120A" stroke-width="3" opacity="0.7"/>' for k in range(1, 17))
           + '<path d="M380,880 H1560 M380,1010 H1560" stroke="#6A5A3A" stroke-width="12"/><path d="M380,880 H1560" stroke="#D8B860" stroke-width="3" opacity="0.5"/>'
           + "".join(f'<circle cx="{x}" cy="{y_}" r="9" fill="#8A7A4A" stroke="{INK}" stroke-width="3"/>' for x in (420, 700, 980, 1260, 1520) for y_ in (880, 1010))
           + '<path d="M380,860 L440,780 L1500,780 L1560,860 Z" fill="#14100C" stroke="#0A0806" stroke-width="8"/>'     # açıklık (karanlık)
           '<path d="M440,780 L1500,780 L1560,860 L1380,860 L1100,800 Z" fill="#2A1C12" opacity="0.5"/>'
           '<path d="M380,860 L440,780 L1500,780 L1560,860" fill="none" stroke="#6A4A2A" stroke-width="16" stroke-linejoin="round"/><path d="M380,858 L440,778 L1500,778 L1560,858" fill="none" stroke="#B88A52" stroke-width="5" opacity="0.7"/>'
           # kayan kapak: sol-üstte, çapraz, yarısı kenarda
           f'<g transform="translate(-300,10) rotate(-7 700 780)"><path d="M300,790 L430,690 L1130,690 L1050,830 L360,848 Z" fill="#4A2E1C" filter="url(#t_ahsap)"/><path d="M300,790 L430,690 L1130,690 L1050,830 L360,848 Z" fill="none" stroke="{INK}" stroke-width="9" stroke-linejoin="round"/>'
           + "".join(f'<path d="M{330+k*60},{800-k*8} L{450+k*60},{696}" stroke="#2A180E" stroke-width="3" opacity="0.7"/>' for k in range(13))
           + '<path d="M440,700 L1120,700" stroke="#C89A60" stroke-width="3" opacity="0.6"/><path d="M730,700 V820 M690,740 H770" stroke="#8A7A4A" stroke-width="14"/></g></g>')
    RGf = fig_bust(dict(RG), ex("fierce", IF.blink_at(1.3)), 0.2, 1.75)
    bxf, byf = 1000, 640
    glow(c, 780, 560, 380, "#FFB060", 0.20)
    with live(c, bxf, byf + 400, phase=0.2, breathe=0.003):
        rim(c, RGf, bxf, byf, 1.0, "#FFC888", dx=-6, dy=-2, a=0.9); draw(c, RGf, bxf, byf, 1.0); shade_side(c, RGf, bxf, byf, 0.36, bxf - 200, bxf + 220, "#0A0608")
    draw(c, SD(cof), 0, 0, 1.0)
    lin = ('<path d="M820,810 Q840,740 920,722 Q1000,708 1080,724 Q1160,742 1180,812 Q1000,846 820,810 Z" fill="#D8CFB4" filter="url(#t_keten)" stroke="#14100C" stroke-width="7" stroke-linejoin="round"/>'
           '<path d="M880,800 Q900,750 940,730 M1000,826 Q1004,770 1000,718 M1110,800 Q1096,750 1060,728" stroke="#8A7E62" stroke-width="4" fill="none" opacity="0.7"/><path d="M1060,730 Q1160,744 1180,812 Q1120,830 1080,826 Z" fill="#7A6E54" opacity="0.45"/>')
    draw(c, SD(lin), 0, 0, 1.0)
    # karanlık açıklıktan sızan tütsü ve sıcak mum ışığı eli yakalar
    bloom_spot(c, 980, 640, 260, "#FFC890", 0.16)
    draw(c, blurred(S("".join(A.smoke_svg(1250 + k * 30, 780, 300, seed=k + 31, a=0.28, w=50) for k in range(3))), 8), 0, 0, 1.0)
    fg = (f'<path d="M0,1090 L0,930 Q60,880 160,900 L210,1090 Z" fill="#0A0806"/><path d="M1920,1090 L1920,900 Q1840,870 1760,910 L1720,1090 Z" fill="#0A0806"/>')
    draw(c, blurred(S(fg), 10), 0, 0, 1.0)
    A.Particles("dust", 160, seed=5, area=(300, 200, 1600, 800), color="#FFF2D8", size=(2, 4.5), speed=8).draw(c, t or 0.0, 1.0) if hasattr(A, "Particles") else None
    card_at(c, "PARİS · 845", 960, 130, "kendi tabutundan")
    sh = skia.GradientShader.MakeRadial((960, 640), 1100, [col("#000", 0).toColor(), col("#000", 0).toColor(), col("#05060A", 0.62).toColor()], [0, 0.45, 1])
    c.drawRect(skia.Rect(0, 0, W, H), skia.Paint(Shader=sh))
    finish(c, cold=False, warm=0.03); return s

# ================================================================== P1d · batıya bakan sırt
def p1d():
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    sky = f'<defs>{gradient("sk1d", [(0, "#241A48"), (0.3, "#6A2E6A"), (0.62, "#E8683A"), (0.9, "#FFC070"), (1, "#FFE0A0")])}</defs><rect width="1920" height="640" fill="url(#sk1d)"/>'
    draw(c, S(sky), 0, 0, 1.0)
    for k in range(60):
        q = R_(k + 5); c.drawCircle(q.uniform(0, 1920), q.uniform(70, 260), q.uniform(0.8, 1.8), skia.Paint(AntiAlias=True, Color4f=col("#F0E4FF", q.uniform(0.2, 0.6))))
    sxp, syp = 1300, 590
    glow(c, sxp, syp, 700, "#FF8A3A", 0.50); glow(c, sxp, syp, 260, "#FFD080", 0.65)
    draw(c, S(f'<circle cx="{sxp}" cy="{syp}" r="92" fill="#FFF0C0"/><circle cx="{sxp}" cy="{syp}" r="92" fill="none" stroke="#FFD890" stroke-width="10" opacity="0.5"/>'), 0, 0, 1.0)
    cl = (cloud_band(51, 12, -100, 2000, 150, 330, "#5A2A5A", "#FF9A5A", 0.9, lit_dy=9, rx=(200, 480), ry=(22, 50)) + cloud_band(52, 10, -100, 2000, 360, 480, "#A04A5A", "#FFC080", 0.8, lit_dy=-6, rx=(160, 380), ry=(12, 26))
          + cloud_band(53, 6, 800, 1800, 440, 520, "#D8704A", "#FFE0A0", 0.7, lit_dy=-5, rx=(140, 300), ry=(8, 16)))
    draw(c, blurred(S(cl), 5), 0, 0, 1.0)
    rays(c, sxp, syp, 270, 1200, 60, 12, "#FFC878", 0.07, t or 0.0)
    # uzak adalar + sırtlar
    far = (mountain_range(61, 700, 2000, 610, 500, 40, "#6A3A66", "#B05A6A", light=-1, stroke="#4A2A4E", cid="d1") + mountain_range(62, -40, 1000, 640, 440, 70, "#4A2A58", "#8A4A66", snow="#C88A9A", light=1, snow_y=520, stroke="#2E1A3A", cid="d2"))
    isl = "".join(f'<path d="M{x},640 Q{x + w/2},{640 - h} {x + w},640 Z" fill="#3A2248" stroke="#24142E" stroke-width="3"/>' for x, w, h in ((980, 150, 34), (1120, 90, 22), (1540, 200, 40), (1800, 120, 26)))
    draw(c, S(far, isl), 0, 0, 1.0)
    draw(c, blurred(S(cloud_band(54, 12, -100, 2000, 600, 660, "#F0B890", "#FFE0B0", 0.4, rx=(240, 500), ry=(12, 24))), 7), 0, 0, 1.0)
    draw(c, S(sea_svg(636, "#E8884A", "#2A1E3E", sxp, 71, glint="#FFE4A0", wl="#4A2E5A", hl="#FFC890", gn=170, spread=0.4)), 0, 0, 1.0)
    # fiyort karşı yamaç
    # fiyort karşı yamaç: sol uç suya inen eteklerle başlar (dikey kesik yok), taban kıyı çizgisi + sudaki yansıma
    mr = mountain_range(63, 800, 2100, 700, 560, 60, "#2E1E3A", "#5A3248", light=-1, stroke="#1A1024", cid="d3", taper=520)
    refl = (f'<defs><linearGradient id="rf3" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2E1E3A" stop-opacity="0.55"/><stop offset="1" stop-color="#2E1E3A" stop-opacity="0"/></linearGradient></defs>'
            f'<path d="M-100,700 Q600,694 900,698 L2000,698 L2000,760 L-100,760 Z" fill="url(#rf3)"/>')
    draw(c, blurred(S(refl), 4), 0, 0, 1.0)
    draw(c, S(mr, Bm.forest(1200, 2000, lambda x: 690, 26, 58, 40, 3, col="#1E1830", lit="#3A2A48", dark="#120C1A")), 0, 0, 1.0)
    draw(c, blurred(S('<path d="M-100,701 Q700,696 1100,700 T2000,699" stroke="#FFB070" stroke-width="3" fill="none" opacity="0.55"/>'
                      + cloud_band(55, 11, -200, 2100, 680, 712, "#C8789A", "#FFD0A0", 0.35, rx=(180, 420), ry=(6, 12))), 5), 0, 0, 1.0)
    # sağ-alt: yamaç + çimen (Ragnar yamaçta)
    slope = "M-40,1090 L-40,760 Q300,730 560,800 Q900,880 1240,930 Q1600,980 1960,1000 L1960,1090 Z"
    gr = (f'<defs>{gradient("hl", [(0, "#4A3A3A"), (0.5, "#2A2430"), (1, "#14101C")])}<clipPath id="slp"><path d="{slope}"/></clipPath></defs><path d="{slope}" fill="url(#hl)"/>'
          f'<g clip-path="url(#slp)"><rect width="1920" height="1080" filter="url(#t_tas)" fill="#3A3030" opacity="0.45"/>' + grass(-40, 1960, 780, 1080, 700, 8, ("#5A3E2A", "#8A5A34", "#B8803E"), 16, 60, 22)
          + '<path d="M-40,764 Q300,734 560,804 Q900,884 1240,934 Q1600,984 1960,1004" stroke="#FF9A50" stroke-width="7" fill="none" opacity="0.6"/></g>')
    draw(c, SD(gr), 0, 0, 1.0)
    draw(c, SD(rock(1180, 960, 90, 64, 3, "#4A3A44", "#C88A6A", "#1A1020"), rock(1320, 985, 56, 38, 4, "#4A3A44", "#C88A6A", "#1A1020"), rock(250, 790, 60, 40, 5, "#4A3A44", "#C88A6A", "#1A1020"), rock(1560, 1000, 110, 60, 6, "#4A3A44", "#C88A6A", "#1A1020")), 0, 0, 1.0)
    RGd = full(dict(RG, _arm_up=False, _carry_svg=""), ex("determined", IF.blink_at(0.4)), 0.95, facing=1, look=0.9); rx_, ry_ = 640, 935
    soft_shadow(c, rx_ + 40, ry_ - 4, 170, 16, 0.5)
    with live(c, rx_, ry_, phase=0.3, breathe=0.004, sway=0.008):
        rim(c, RGd, rx_, ry_, 1.0, "#FFA860", dx=7, dy=-3, a=0.9); rim(c, RGd, rx_, ry_, 1.0, "#FFD890", dx=3, dy=-4, a=0.5)
        draw(c, RGd, rx_, ry_, 1.0); shade_side(c, RGd, rx_, ry_, 0.38, rx_ + 200, rx_ - 160, "#241034")
    draw(c, S(grass(480, 800, 890, 940, 160, 41, ("#3A2A1E", "#6A4A2C", "#A8703A"), 40, 110, 30)), 0, 0, 1.0)
    # ön plan çimenler (rüzgâr), bulanık
    fgg = grass(-40, 1960, 1000, 1090, 260, 11, ("#14101A", "#241A22", "#3A2A28"), 60, 150, 40) + grass(-40, 620, 930, 1090, 120, 12, ("#1A121C", "#2A1E26"), 70, 170, 46)
    draw(c, blurred(S(fgg), 4), 0, 0, 1.0)
    # iki kuzgun (Huginn, Muninn) güneşe doğru
    draw(c, S(Bm.raven(930, 360, 0.55, 1, "fly", 2), Bm.raven(1080, 300, 0.42, 1, "fly", 5)), 0, 0, 1.0)
    for k in range(12):
        q = R_(k + 700); c.drawLine(q.uniform(0, 1900), 900 + q.uniform(-20, 100), q.uniform(0, 1900) * 0 + 400 + q.uniform(0, 1500), 880 + q.uniform(0, 100), skia.Paint(AntiAlias=True, StrokeWidth=0.01, Color4f=col("#000", 0.0)))
    card_at(c, "BATI", 1480, 200, "") if False else None
    finish(c, cold=False, warm=0.10); return s

# ================================================================== P2a / P2b / P2c : ocak başı
def loom(x, y, s=1.0):
    o = [f'<g transform="translate({x},{y}) scale({s})">',
         f'<path d="M-120,0 L-110,-380 M120,0 L110,-380" stroke="{INK}" stroke-width="26"/><path d="M-120,0 L-110,-380 M120,0 L110,-380" stroke="#6A4428" stroke-width="15" filter="url(#t_ahsap)"/>',
         f'<path d="M-128,-380 L128,-380" stroke="{INK}" stroke-width="22"/><path d="M-128,-380 L128,-380" stroke="#7A5232" stroke-width="12"/>']
    for k in range(-9, 10): o.append(f'<path d="M{k*11},-372 L{k*11 + (k%3-1)*2},-130" stroke="#C8B890" stroke-width="2.2" opacity="0.9"/>')
    for k in range(-9, 10, 2): o.append(f'<g transform="translate({k*11},-124)"><path d="M0,0 v18" stroke="#8A7A58" stroke-width="2"/><path d="M-7,18 h14 l-3,26 h-8 Z" fill="#5A5248" stroke="{INK}" stroke-width="3"/></g>')
    o.append(f'<path d="M-100,-372 H100 V-240 H-100 Z" fill="#8A3A24" filter="url(#t_yun)" opacity="0.95"/><path d="M-100,-372 H100 V-240 H-100 Z" fill="none" stroke="{INK}" stroke-width="3"/>' + "".join(f'<path d="M-100,{-366 + k*12} H100" stroke="#D8B060" stroke-width="2" opacity="0.5"/>' for k in range(10)))
    o.append('</g>'); return "".join(o)

def herbs(x, y, n, seed):
    r = R_(seed); o = [f'<path d="M{x-40},{y} L{x + n*54},{y + 10}" stroke="{INK}" stroke-width="7"/>']
    for k in range(n):
        xx = x + 20 + k * 54; ln = r.uniform(60, 110); cl_ = r.choice(["#6A7A3A", "#8A8A4A", "#7A5A3A", "#9A6A8A"])
        o.append(f'<path d="M{xx},{y+4} v14" stroke="#3A2A1A" stroke-width="3"/><path d="M{xx-10},{y+18} Q{xx-16},{y+18+ln*0.6:.0f} {xx-6},{y+18+ln:.0f} L{xx+6},{y+18+ln:.0f} Q{xx+16},{y+18+ln*0.6:.0f} {xx+10},{y+18} Z" fill="{cl_}" stroke="{INK}" stroke-width="3"/>'
                 + "".join(f'<path d="M{xx + j*3 - 3},{y + 24} l{r.uniform(-2, 2):.0f},{ln*0.8:.0f}" stroke="#3A3A1A" stroke-width="1.5" opacity="0.6"/>' for j in range(4)))
    return "".join(o)

def cauldron(x, y, s=1.0):
    return (f'<g transform="translate({x},{y}) scale({s})"><path d="M-90,0 L0,-250 L90,0 M0,-250 L0,0" stroke="{INK}" stroke-width="14"/><path d="M-90,0 L0,-250 L90,0" stroke="#3A3A3E" stroke-width="7"/>'
            f'<path d="M0,-250 L0,-120" stroke="{INK}" stroke-width="6"/><path d="M-60,-120 Q-66,-40 -30,-20 L30,-20 Q66,-40 60,-120 Z" fill="#2A2A2E" filter="url(#t_metal)" stroke="{INK}" stroke-width="7"/>'
            f'<ellipse cx="0" cy="-120" rx="60" ry="12" fill="#5A4A3A" stroke="{INK}" stroke-width="5"/><path d="M-50,-124 Q0,-134 50,-124" stroke="#C88A50" stroke-width="3" fill="none" opacity="0.6"/>'
            f'<path d="M-50,-110 Q-60,-50 -34,-30" stroke="#8A8A92" stroke-width="3" fill="none" opacity="0.5"/>'
            f'<path d="M-8,-140 q-12,-34 6,-60 q16,-26 -4,-60" stroke="#D8D4CC" stroke-width="10" fill="none" opacity="0.4" stroke-linecap="round"/></g>')

def sleeping_dog(x, y, s=1.0):
    return (f'<g transform="translate({x},{y}) scale({s})"><ellipse cx="0" cy="8" rx="110" ry="18" fill="#000" opacity="0.45"/>'
            f'<path d="M-100,-4 Q-110,-50 -60,-66 Q0,-86 60,-62 Q108,-46 102,-8 Q60,8 0,6 Q-60,10 -100,-4 Z" fill="#6A5A48" filter="url(#t_kurk)"/><path d="M-100,-4 Q-110,-50 -60,-66 Q0,-86 60,-62 Q108,-46 102,-8 Q60,8 0,6 Q-60,10 -100,-4 Z" fill="none" stroke="{INK}" stroke-width="5"/>'
            f'<path d="M-90,-30 Q-40,-76 40,-64 Q90,-50 100,-16 Q50,-50 -10,-44 Q-60,-40 -90,-30 Z" fill="#8A7660" opacity="0.7"/><path d="M-60,-8 Q0,4 70,-6" stroke="#2A1E14" stroke-width="3" fill="none" opacity="0.6"/>'
            f'<path d="M70,-30 Q116,-44 134,-18 Q140,0 120,4 L84,6 Q62,-6 70,-30 Z" fill="#7A6652" stroke="{INK}" stroke-width="5"/><path d="M96,-40 Q86,-62 104,-60 Q112,-48 108,-38 Z" fill="#4A3A2C" stroke="{INK}" stroke-width="4"/>'
            f'<path d="M126,-12 q8,2 12,8" stroke="{INK}" stroke-width="4" fill="none"/><path d="M104,-14 q6,3 12,0" stroke="{INK}" stroke-width="3" fill="none"/>'
            f'<path d="M-100,-14 Q-132,-30 -126,-4 Q-120,10 -96,4" fill="#6A5A48" stroke="{INK}" stroke-width="5"/></g>')

def pelt(x, y, w, h, seed, col_="#5A4430"):
    r = R_(seed); pts = [(x + math.cos(a) * w * r.uniform(0.9, 1.1), y + math.sin(a) * h * r.uniform(0.9, 1.1)) for a in [k * math.pi / 8 for k in range(16)]]
    d = "M" + " L".join(f"{px:.0f},{py:.0f}" for px, py in pts) + " Z"
    return (f'<path d="{d}" fill="{col_}" filter="url(#t_kurk)"/><path d="{d}" fill="none" stroke="#0E0804" stroke-width="5" stroke-linejoin="round"/>'
            + "".join(f'<path d="M{px:.0f},{py:.0f} l{(x-px)*0.12:.0f},{(y-py)*0.12:.0f}" stroke="#2A1C10" stroke-width="3" opacity="0.7"/>' for px, py in pts))

def hall_base():
    return place(IPL.longhouse(1.0))

def p2a():
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    draw(c, hall_base(), 0, 0, 1.0); fill(c, "#0A0604", 0.10)
    draw(c, SD(herbs(160, 150, 6, 1), herbs(1400, 160, 7, 2), loom(1700, 700, 0.85)), 0, 0, 1.0)
    draw(c, SD(hearth(1060, 850, 0.74), cauldron(1060, 826, 0.62)), 0, 0, 1.0)
    flames(c, 790, 1330, 828, 100, t, seed=4)
    glow(c, 1060, 800, 760, "#FF7A2A", 0.32); glow(c, 1060, 830, 260, "#FFC070", 0.4)
    # yetişkinler: orta plan büstler (3/4, ocağa ve çocuklara bakar)
    LAb = fig_bust(LAGv, ex("tender", IF.blink_at(0.9)), 0.6, 1.55)
    RGb = fig_bust(dict(RG), ex("talk", IF.blink_at(0.3)), 0.6, 1.9)
    for sp, x, y, ph in ((LAb, 250, 500, 0.9), (RGb, 640, 470, 0.3)):
        with live(c, x, y + 600, phase=ph, breathe=0.004):
            rim(c, sp, x, y, 1.0, "#FFB070", dx=6, dy=-2, a=0.85); draw(c, sp, x, y, 1.0); shade_side(c, sp, x, y, 0.38, x + 220, x - 200, "#140A06")
    # yün eğiren Lagertha: iğ ve yün yumağı
    draw(c, S('<path d="M360,720 Q372,790 358,860" stroke="#E8DCC0" stroke-width="3" fill="none"/><path d="M356,860 l8,0 l-4,50 Z" fill="#8A6A3A" stroke="#1A1410" stroke-width="3"/><ellipse cx="360" cy="866" rx="14" ry="6" fill="#B8A070" stroke="#1A1410" stroke-width="3"/><ellipse cx="376" cy="712" rx="30" ry="22" fill="#E8DCC0" stroke="#1A1410" stroke-width="4"/>'), 0, 0, 1.0)
    # alçak bank + postlar (büst gövdelerinin altını kapatır)
    bank = ('<rect x="0" y="900" width="1000" height="200" fill="#2E2014" filter="url(#t_ahsap)"/><rect x="0" y="896" width="1000" height="14" fill="#5A4028" stroke="#0E0804" stroke-width="4"/>'
            + pelt(180, 920, 200, 40, 5, "#4A3A2C") + pelt(520, 925, 220, 40, 6, "#6A5A48") + pelt(840, 925, 160, 36, 7, "#3A2E24"))
    draw(c, SD(bank), 0, 0, 1.0)
    # çocuklar: postlar üzerinde, ocağın sağında, başları Ragnar'a dönük
    draw(c, SD(pelt(1320, 1000, 300, 60, 8, "#5A4430"), pelt(1650, 1000, 230, 50, 9, "#6A5A48")), 0, 0, 1.0)
    BJs = full(dict(BJv, _kneel=150, _arm_up=False), ex("listen", IF.blink_at(1.2)), 0.9, facing=-1, look=-0.9)
    GYs = full(dict(GYDA, _kneel=130, _arm_up=False), ex("awe", IF.blink_at(0.6)), 0.9, facing=-1, look=-0.9)
    for sp, x, y, ph, sc in ((BJs, 1290, 1000, 1.2, CH * 1.2), (GYs, 1650, 1004, 0.6, CHD * 1.2)):
        soft_shadow(c, x, y + 4, 130, 14, 0.55)
        with live(c, x, y, phase=ph, breathe=0.005, rot=-2):
            rim(c, sp, x, y, sc, "#FFB070", dx=-5, dy=-2, a=0.8); draw(c, sp, x, y, sc); shade_side(c, sp, x, y, 0.35, x - 200, x + 200, "#140A06")
    draw(c, SD(sleeping_dog(1480, 1008, 0.8)), 0, 0, 1.0)
    draw(c, blurred(place(cloud_band(96, 9, 900, 1260, 160, 700, "#6A5A50", "#8A7666", 0.20, rx=(80, 200), ry=(40, 90))), 14), 0, 0, 1.0)
    sparks(c, 1060, 800, 50, 600, 410, w=260)
    draw(c, blurred(SD(hall_fg_left()), 7), -60, 0, 1.0)
    finish(c, cold=False, warm=0.08); return s

def wolf(x, y, s=1.0, flip=1):
    o = [f'<g transform="translate({x},{y}) scale({s*flip},{s})">']
    o.append('<ellipse cx="10" cy="4" rx="120" ry="12" fill="#000" opacity="0.4"/>')
    for lx, lw in ((-70, 1), (-44, 0), (46, 0), (70, 1)):   # bacaklar
        o.append(f'<path d="M{lx},-40 L{lx + 4},0" stroke="#050A18" stroke-width="22" stroke-linecap="round"/><path d="M{lx},-40 L{lx + 4},0" stroke="{"#5A6070" if lw else "#7A8090"}" stroke-width="14" stroke-linecap="round"/>')
    body = "M-104,-78 Q-96,-112 -40,-110 Q20,-118 70,-106 Q90,-100 100,-120 L116,-150 Q136,-166 160,-152 L196,-130 Q214,-120 200,-110 L160,-104 Q140,-92 126,-84 Q110,-50 80,-40 L-70,-38 Q-98,-44 -104,-78 Z"
    o.append(f'<path d="{body}" fill="#7A8090" stroke="#050A18" stroke-width="6" stroke-linejoin="round"/>')
    o.append('<path d="M-96,-90 Q-40,-120 70,-108 Q96,-104 104,-124 L116,-150 Q96,-118 70,-98 Q-20,-86 -90,-70 Z" fill="#4A5060"/>')
    o.append("".join(f'<path d="M{-90 + k*20},{-100 + (k%3)*8} l{6 + (k%2)*4},-12 l4,14" stroke="#B8C0CC" stroke-width="2.5" fill="none" opacity="0.8"/>' for k in range(10)))
    o.append('<path d="M-104,-78 Q-150,-70 -164,-30 Q-150,-52 -118,-54" fill="#5A6070" stroke="#050A18" stroke-width="5"/>')   # kuyruk
    o.append('<path d="M150,-152 L146,-188 L170,-160 Z" fill="#5A6070" stroke="#050A18" stroke-width="4"/>')   # kulak
    o.append('<path d="M170,-130 Q190,-126 202,-118" stroke="#050A18" stroke-width="4" fill="none"/><path d="M178,-128 q8,12 16,6" stroke="#F4F0E0" stroke-width="3" fill="none"/>')   # çene dişleri
    o.append('<circle cx="160" cy="-138" r="14" fill="#FFD060" opacity="0.35"/><path d="M152,-140 q8,-6 16,0 q-8,5 -16,0 Z" fill="#FFE890" stroke="#050A18" stroke-width="2.5"/><circle cx="160" cy="-140" r="2.5" fill="#050A18"/>')
    o.append('</g>'); return "".join(o)

def tapestry():
    from itertools import product
    r = R_(8); o = []
    PD = 'M590,100 Q960,86 1330,100 Q1340,540 1330,950 Q960,964 590,950 Q580,540 590,100 Z'
    GOLD, GOLDL, DK = "#E8C860", "#FFF0B0", "#050A18"
    o.append(f'<defs><clipPath id="tp"><path d="{PD}"/></clipPath><clipPath id="mail"><path d="M818,366 Q776,404 788,474 L850,640 L1070,640 L1132,474 Q1144,404 1102,366 Q960,334 818,366 Z"/></clipPath>'
             '<radialGradient id="halo" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#FFE8A0" stop-opacity="0.8"/><stop offset="1" stop-color="#FFE8A0" stop-opacity="0"/></radialGradient></defs>')
    o.append(f'<path d="{PD}" fill="#0F1838" filter="url(#t_yun)"/><g clip-path="url(#tp)">')
    o.append(f'<defs>{gradient("bgp", [(0, "#1A1650"), (0.45, "#2A2A78"), (1, "#0F1838")])}</defs><rect x="580" y="90" width="760" height="870" fill="url(#bgp)" opacity="0.9"/>')
    # aurora (dikişli bantlar) + ilahi ışınlar + şimşek
    for k, (cl_, y0) in enumerate((("#3AC8A8", 250), ("#7A5AE0", 200), ("#3A8AE0", 300))):
        d = f"M570,{y0} Q760,{y0-90} 960,{y0-10} T1350,{y0-40}"
        o.append(f'<path d="{d}" stroke="{cl_}" stroke-width="40" fill="none" opacity="0.35" stroke-linecap="round"/><path d="{d}" stroke="{cl_}" stroke-width="22" fill="none" opacity="0.5" stroke-linecap="round"/><path d="{d}" stroke="{GOLDL}" stroke-width="3" fill="none" stroke-dasharray="9 6" opacity="0.7"/>')
    o.append('<circle cx="960" cy="290" r="360" fill="url(#halo)" opacity="0.7"/>')
    for k in range(18):
        a = math.radians(-170 + k * 160 / 17); o.append(f'<path d="M{960 + 120*math.cos(a):.0f},{290 + 120*math.sin(a):.0f} L{960 + 800*math.cos(a):.0f},{290 + 800*math.sin(a):.0f}" stroke="{GOLD}" stroke-width="{4 + (k%2)*3}" stroke-dasharray="14 10" opacity="0.30"/>')
    for pts in (((690, 110), (650, 220), (700, 232), (630, 380)), ((1260, 110), (1216, 200), (1262, 214), (1196, 340))):
        d = "M" + " L".join(f"{x},{y}" for x, y in pts)
        o.append(f'<path d="{d}" stroke="#FFFFFF" stroke-width="14" fill="none" opacity="0.35" stroke-linejoin="bevel"/><path d="{d}" stroke="{GOLDL}" stroke-width="6" fill="none" stroke-linejoin="bevel"/><path d="{d}" stroke="#FFFFFF" stroke-width="2" fill="none"/>')
    for k in range(40):
        x, y = r.uniform(610, 1310), r.uniform(130, 500); o.append(f'<path d="M{x-5:.0f},{y:.0f} h10 M{x:.0f},{y-5:.0f} v10" stroke="{GOLD}" stroke-width="2.5" opacity="0.7"/>')
    # kuzgunlar (Huginn, Muninn)
    o.append('<circle cx="720" cy="270" r="70" fill="#E8C860" opacity="0.18"/><circle cx="1250" cy="560" r="64" fill="#E8C860" opacity="0.16"/>')
    o.append(Bm.raven(722, 272, 0.62, -1, "fly", 3) + Bm.raven(1250, 566, 0.52, 1, "fly", 6) + Bm.raven(780, 470, 0.36, 1, "fly", 9))
    # pelerin: koyu, rüzgârda dalgalı, kırmızı astar
    cl = "M830,350 Q700,420 652,640 Q612,780 596,946 L1318,946 Q1310,800 1296,660 Q1260,430 1092,350 Z"
    o.append(f'<path d="{cl}" fill="#0E1630" stroke="{DK}" stroke-width="8"/><path d="M830,360 Q730,450 690,640 Q662,780 652,940 L772,940 Q782,760 806,600 Q826,470 872,380 Z" fill="#7A1E28"/>')
    o.append(f'<path d="M1092,350 Q1260,430 1296,660 Q1310,800 1318,946 L1200,946 Q1180,760 1160,600 Q1140,440 1092,350 Z" fill="#1A2450" opacity="0.8"/>')
    for k in range(5): o.append(f'<path d="M{830 - k*34},{420 + k*60} Q{760 - k*40},{640} {700 - k*18},{946}" stroke="{GOLD}" stroke-width="3" stroke-dasharray="9 6" fill="none" opacity="0.55"/>')
    o.append(f'<path d="{cl}" fill="none" stroke="{GOLD}" stroke-width="4" stroke-dasharray="12 8" opacity="0.8"/>')
    # Gungnir (mızrak): sağ elde yükselmiş, rünler parlar
    o.append(f'<path d="M1160,950 L1242,132" stroke="{DK}" stroke-width="20" stroke-linecap="round"/><path d="M1160,950 L1242,132" stroke="#8A5A2A" stroke-width="12" stroke-linecap="round"/><path d="M1164,950 L1246,132" stroke="#D8A860" stroke-width="3" opacity="0.8"/>')
    for k in range(10):
        t = 0.1 + k * 0.08; x = 1160 + 82 * (1 - t) ; y = 950 - 818 * (1 - (1 - t))
    for k in range(9):
        t_ = 0.38 + k * 0.065; x = 1160 + 82 * t_; y = 950 - 818 * t_
        o.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="12" fill="#FFE890" opacity="0.28"/><path d="M{x-5:.0f},{y-6:.0f} l5,12 l5,-12 M{x-5:.0f},{y:.0f} h10" stroke="#FFF4C0" stroke-width="3" stroke-linecap="round"/>')
    o.append(f'<circle cx="1244" cy="86" r="58" fill="url(#halo)"/><path d="M1244,10 Q1274,70 1244,136 Q1214,70 1244,10 Z" fill="#CFD6E4" stroke="{DK}" stroke-width="6"/><path d="M1244,24 Q1252,70 1244,124" stroke="#FFFFFF" stroke-width="3" fill="none"/><path d="M1232,126 h24 l-4,16 h-16 Z" fill="{GOLD}" stroke="{DK}" stroke-width="4"/>')
    # gövde: zincir zırh
    o.append(f'<path d="M818,366 Q776,404 788,474 L850,640 L1070,640 L1132,474 Q1144,404 1102,366 Q960,334 818,366 Z" fill="#59606F" stroke="{DK}" stroke-width="7"/><g clip-path="url(#mail)">')
    for row in range(14):
        y = 372 + row * 21
        for x in range(770 + (row % 2) * 12, 1150, 24): o.append(f'<path d="M{x},{y} a12,11 0 0 0 24,0" stroke="#252B3A" stroke-width="2.4" fill="none" opacity="0.8"/><path d="M{x+2},{y-1} a10,9 0 0 1 20,0" stroke="#A8B0C0" stroke-width="1.2" fill="none" opacity="0.45"/>')
    o.append('<path d="M1020,360 L1140,360 L1140,650 L1010,650 Z" fill="#000" opacity="0.28"/><path d="M820,370 L850,370 L880,640 L856,640 Z" fill="#CFD6E8" opacity="0.18"/></g>')
    o.append(f'<path d="M818,366 Q776,404 788,474 L850,640 L1070,640 L1132,474 Q1144,404 1102,366" fill="none" stroke="{GOLD}" stroke-width="3" stroke-dasharray="9 6" opacity="0.7"/>')
    # kürk omuzluk
    fur = []
    for k in range(26):
        t_ = k / 25; x = 760 + t_ * 400; yb = 392 - 40 * math.sin(math.pi * t_) + 36 * (1 - math.sin(math.pi * t_)) * 0.6
        fur.append(f'<path d="M{x-14:.0f},{yb-6:.0f} L{x + r.uniform(-6, 6):.0f},{yb + 30 + r.uniform(0, 22):.0f} L{x+14:.0f},{yb-6:.0f} Z" fill="{["#7A7468", "#8A8478", "#6A6458"][k%3]}" stroke="{DK}" stroke-width="3"/>')
    o.append(f'<path d="M760,396 Q960,300 1160,396 Q960,356 760,396 Z" fill="#8A8478" stroke="{DK}" stroke-width="6"/>' + "".join(fur) + '<path d="M790,380 Q960,320 1130,380" stroke="#C8C2B4" stroke-width="5" fill="none" opacity="0.6" stroke-dasharray="6 5"/>')
    # kemer, deri şeritler, bacaklar
    o.append(f'<rect x="846" y="632" width="228" height="32" rx="6" fill="#3A2616" stroke="{DK}" stroke-width="6"/><circle cx="960" cy="648" r="22" fill="{GOLD}" stroke="{DK}" stroke-width="5"/><circle cx="960" cy="648" r="11" fill="none" stroke="#7A4E10" stroke-width="4"/>')
    for k in range(8): o.append(f'<path d="M{858 + k*27},664 h24 l-2,92 q-10,8 -20,0 Z" fill="#5A3A22" stroke="{DK}" stroke-width="4"/><circle cx="{870 + k*27}" cy="680" r="4" fill="{GOLD}"/>')
    for x0 in (872, 966):
        o.append(f'<path d="M{x0},752 L{x0 + 82},752 L{x0 + 72},900 L{x0 + 6},900 Z" fill="#232A3C" stroke="{DK}" stroke-width="6"/><path d="M{x0 + 8},760 L{x0 + 14},890" stroke="#8A94AA" stroke-width="4" opacity="0.6"/><path d="M{x0 - 6},900 h94 l6,30 h-110 Z" fill="#3A2616" stroke="{DK}" stroke-width="6"/>')
    # sol kol: kılıç kabzasına
    o.append(capsule("M826,396 Q780,470 800,540", 56, "#59606F", "#252B3A", "#A8B0C0") + capsule("M800,540 Q820,600 858,634", 46, "#59606F", "#252B3A", "#A8B0C0"))
    o.append(f'<circle cx="866" cy="640" r="26" fill="{SK}" stroke="{DK}" stroke-width="6"/><path d="M846,634 q10,-8 20,0 M850,648 q10,6 22,0" stroke="{SK3}" stroke-width="3" fill="none"/><path d="M866,616 L866,540" stroke="{DK}" stroke-width="16"/><path d="M866,616 L866,540" stroke="#3A2616" stroke-width="9"/><circle cx="866" cy="532" r="14" fill="{GOLD}" stroke="{DK}" stroke-width="4"/>')
    # kurtlar: Geri ve Freki
    o.append(wolf(742, 934, 0.95, 1) + wolf(1180, 940, 0.95, -1))
    # sağ kol: kalkık, mızrağı tutar; Draupnir altın halka
    o.append(capsule("M1110,404 Q1190,420 1214,470", 58, "#59606F", "#252B3A", "#A8B0C0") + capsule("M1214,470 Q1230,400 1210,340", 48, "#59606F", "#252B3A", "#A8B0C0"))
    o.append(f'<ellipse cx="1226" cy="418" rx="34" ry="14" transform="rotate(-80 1226 418)" fill="none" stroke="{DK}" stroke-width="14"/><ellipse cx="1226" cy="418" rx="34" ry="14" transform="rotate(-80 1226 418)" fill="none" stroke="{GOLD}" stroke-width="8"/>')
    o.append(f'<circle cx="1210" cy="322" r="28" fill="{SK}" stroke="{DK}" stroke-width="6"/><path d="M1190,310 q20,-12 40,0 M1190,324 q20,-8 40,2 M1196,338 q16,6 30,-2" stroke="{SK3}" stroke-width="3" fill="none"/><path d="M1244,300 L1252,350" stroke="{DK}" stroke-width="14" stroke-linecap="round"/>')
    # kanatlı miğfer + yüz
    for sg in (-1, 1):
        for k in range(6):
            ex_ = 960 + sg * (150 + k * 28); ey_ = 150 + k * 16
            o.append(f'<path d="M{960 + sg*78},{236 - k*7} Q{960 + sg*(110 + k*14)},{176 - k*6} {ex_},{ey_ + 40}" stroke="{DK}" stroke-width="20" fill="none" stroke-linecap="round"/><path d="M{960 + sg*78},{236 - k*7} Q{960 + sg*(110 + k*14)},{176 - k*6} {ex_},{ey_ + 40}" stroke="#181628" stroke-width="13" fill="none" stroke-linecap="round"/><path d="M{960 + sg*80},{234 - k*7} Q{960 + sg*(112 + k*14)},{178 - k*6} {ex_ - sg*4},{ey_ + 38}" stroke="#6A68A8" stroke-width="2.5" fill="none" opacity="0.8"/>')
    o.append(f'<path d="M905,250 Q960,232 1015,250 Q1024,320 992,372 Q960,394 928,372 Q896,320 905,250 Z" fill="#D2AE8C" stroke="{DK}" stroke-width="6"/><path d="M984,250 Q1015,250 1015,262 Q1024,320 992,372 Q984,320 984,250 Z" fill="#A8845E" opacity="0.5"/>')
    o.append(f'<path d="M914,266 L958,306" stroke="#7A1E22" stroke-width="7" stroke-linecap="round"/><path d="M920,284 q16,10 32,2" stroke="{DK}" stroke-width="5" fill="none"/><path d="M912,254 Q930,266 954,268" stroke="#6A6A74" stroke-width="9" stroke-linecap="round"/>')   # yara izli kapalı sol göz
    o.append('<circle cx="990" cy="284" r="34" fill="url(#halo)"/>' + f'<path d="M974,284 q16,-14 32,0 q-16,12 -32,0 Z" fill="#FFF8D8" stroke="{DK}" stroke-width="4"/><circle cx="990" cy="284" r="6" fill="#FFB820"/><circle cx="990" cy="284" r="2.5" fill="{DK}"/><path d="M968,268 Q990,256 1012,270" stroke="#6A6A74" stroke-width="9" stroke-linecap="round"/>')
    o.append(f'<path d="M960,300 q-6,30 -2,44 q12,6 24,0" stroke="#8A6A4A" stroke-width="4" fill="none"/>')
    o.append(f'<path d="M880,266 Q878,166 960,156 Q1042,166 1040,266 Q960,242 880,266 Z" fill="#6A7280" stroke="{DK}" stroke-width="7"/><path d="M900,250 Q902,184 950,172" stroke="#D8DEEA" stroke-width="6" fill="none" opacity="0.7"/><path d="M1010,180 Q1034,210 1034,258" stroke="#2A3040" stroke-width="10" fill="none" opacity="0.5"/>'
             f'<path d="M882,262 Q960,238 1038,262" stroke="{GOLD}" stroke-width="10" fill="none"/><path d="M882,262 Q960,238 1038,262" stroke="{DK}" stroke-width="2" fill="none" stroke-dasharray="6 6"/><rect x="954" y="236" width="12" height="86" rx="4" fill="#8A94AA" stroke="{DK}" stroke-width="4"/>'
             f'<path d="M886,270 Q884,320 908,356 L916,350 Q900,314 902,268 Z" fill="#6A7280" stroke="{DK}" stroke-width="4"/><path d="M1034,270 Q1036,320 1012,356 L1004,350 Q1020,314 1018,268 Z" fill="#6A7280" stroke="{DK}" stroke-width="4"/>')
    # sakal: gri, örgülü, altın halkalı
    o.append(f'<path d="M900,326 Q872,430 924,530 Q960,596 996,530 Q1048,430 1020,326 Q960,372 900,326 Z" fill="#C2C6CE" stroke="{DK}" stroke-width="6"/>' + "".join(f'<path d="M{904 + k*13},{352 + (k%3)*8} Q{898 + k*14},{470} {924 + k*8},{560}" stroke="#7A8294" stroke-width="2.5" stroke-dasharray="6 4" fill="none"/>' for k in range(9)))
    for bx in (930, 960, 990):
        o.append("".join(f'<ellipse cx="{bx + (k%2)*3 - 1}" cy="{440 + k*16}" rx="9" ry="9" fill="#AEB2BC" stroke="{DK}" stroke-width="3"/>' for k in range(7)) + f'<circle cx="{bx}" cy="552" r="9" fill="none" stroke="{GOLD}" stroke-width="5"/><circle cx="{bx}" cy="470" r="8" fill="none" stroke="{GOLD}" stroke-width="4"/>')
    o.append(f'<path d="M926,338 Q960,356 994,338 Q978,368 960,362 Q942,368 926,338 Z" fill="#B0B4BC" stroke="{DK}" stroke-width="4"/>')
    # dokuma dokusu
    for k in range(0, 860, 5): o.append(f'<path d="M580,{100 + k} H1340" stroke="{"#FFFFFF" if k % 10 == 0 else "#000000"}" stroke-width="2" stroke-dasharray="5 3" opacity="0.10"/>')
    o.append('</g>')
    o.append(f'<path d="{PD}" fill="none" stroke="#7A1E22" stroke-width="22"/><path d="{PD}" fill="none" stroke="{GOLD}" stroke-width="5" stroke-dasharray="14 8"/>')
    o.append('<path d="M590,950 Q960,964 1330,950" stroke="#0C1630" stroke-width="3" fill="none"/>' + "".join(f'<path d="M{600 + k*18},958 l0,{22 + (k%3)*6}" stroke="#C8A850" stroke-width="3"/>' for k in range(40)))
    return "".join(o)

def smoke_curls(seed, n, x0, x1, ybot, ytop, w=60, a=0.3):
    r = R_(seed); o = []
    for k in range(n):
        x = r.uniform(x0, x1); d = f"M{x:.0f},{ybot}"
        for j in range(8):
            d += f" Q{x + r.uniform(-w, w):.0f},{ybot - (j + 0.5) * (ybot - ytop) / 8:.0f} {x + r.uniform(-w, w) * 0.6:.0f},{ybot - (j + 1) * (ybot - ytop) / 8:.0f}"
        o.append(f'<path d="{d}" stroke="#D8D0C8" stroke-width="{r.uniform(22, 60):.0f}" fill="none" stroke-linecap="round" opacity="{a * r.uniform(0.5, 1):.2f}"/>')
    return "".join(o)

def p2b():
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    draw(c, blurred(hall_base(), 5), 0, 0, 1.0); fill(c, "#0A0604", 0.5)
    glow(c, 960, 1000, 900, "#FF7A2A", 0.30)
    glow(c, 960, 520, 620, "#E8B84E", 0.22)
    draw(c, SD(tapestry()), 0, 0, 1.0)
    glow(c, 990, 284, 120, "#FFE8B0", 0.22)
    # duman: halıyı sarar; alt kenar ve kenarlarda yoğun, ortada seyrek
    sm = smoke_curls(3, 9, 560, 1380, 1070, 120, 90, 0.34) + smoke_curls(7, 5, 480, 520, 1000, 200, 40, 0.3) + smoke_curls(9, 5, 1400, 1460, 1000, 200, 40, 0.3)
    draw(c, blurred(S(sm), 12), 0, 0, 1.0)
    draw(c, blurred(S(smoke_curls(5, 5, 600, 1320, 1070, 820, 50, 0.28)), 5), 0, 0, 1.0)
    draw(c, S(*(f'<path d="M{x},{1010 - k*20} q-40,-90 10,-170 q50,-70 -6,-150" stroke="#E8E0D4" stroke-width="3" fill="none" opacity="0.35"/>' for k, x in enumerate((700, 820, 1080, 1210)))), 0, 0, 1.0)
    # alev tabanı + kıvılcım
    flames(c, 700, 1220, 1020, 90, t, seed=12, a=0.9)
    glow(c, 960, 1020, 420, "#FFB050", 0.30)
    sparks(c, 960, 960, 60, 800, 520, w=400)
    draw(c, blurred(S(smoke_curls(11, 4, 300, 1700, 1080, 700, 120, 0.3)), 18), 0, 0, 1.0)
    card_at(c, "ODİN", 1600, 190, "savaş ve bilgelik tanrısı")
    finish(c, cold=False, warm=0.05); return s

def p2c():
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    draw(c, blurred(hall_base(), 11), 0, 0, 1.0); fill(c, "#0A0604", 0.45)
    for k in range(26):    # bokeh: arkadaki ateş/kor
        q = R_(k + 1); c.drawCircle(q.uniform(100, 1800), q.uniform(200, 700), q.uniform(14, 40), skia.Paint(AntiAlias=True, Color4f=col("#FF9A40", q.uniform(0.05, 0.18)), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 6)))
    glow(c, 960, 1100, 1000, "#FF7A2A", 0.42)
    BJb = fig_bust(dict(BJv), ex("listen", IF.blink_at(1.2)), 0.5, 2.05)
    GYb = fig_bust(dict(GYDA), ex("tender", IF.blink_at(0.5)), -0.3, 1.95)
    for sp, x, y, ph, lt in ((BJb, 700, 470, 0.5, 1), (GYb, 1230, 540, 1.1, -1)):
        with live(c, x, y + 600, phase=ph, breathe=0.004):
            rim(c, sp, x, y, 1.0, "#FFB070", dx=-6 * lt, dy=4, a=0.8); rim(c, sp, x, y, 1.0, "#FFD8A0", dx=-3 * lt, dy=2, a=0.5)
            draw(c, sp, x, y, 1.0); shade_side(c, sp, x, y, 0.34, x + 160 * (-lt), x + 260 * lt, "#140A06")
        glow(c, x + 40 * -lt, y + 60, 200, "#FF9A40", 0.16)
    sparks(c, 960, 900, 60, 700, 600, w=700)
    # ön plan: bulanık post + Ragnar'ın pelerini ve parlayan kuzgun broş
    draw(c, blurred(SD(pelt(150, 1010, 300, 120, 21, "#4A3A2C"), pelt(1780, 1020, 280, 110, 22, "#5A4430")), 14), 0, 0, 1.0)
    cl = ('<path d="M560,1090 Q700,880 960,850 Q1220,880 1360,1090 Z" fill="#2E4A44" filter="url(#t_yun)"/><path d="M560,1090 Q700,880 960,850 Q1220,880 1360,1090 Z" fill="none" stroke="#0A0A08" stroke-width="7"/>'
          '<path d="M700,1090 Q780,940 960,900 M1220,1090 Q1140,940 960,900" stroke="#1A2A26" stroke-width="5" fill="none" opacity="0.7"/>'
          '<path d="M600,1000 Q780,870 960,850 Q1140,870 1320,1000 Q1140,930 960,920 Q780,930 600,1000 Z" fill="#6A5A48" filter="url(#t_kurk)" stroke="#0A0A08" stroke-width="5"/>')
    draw(c, SD(cl), 0, 0, 1.0)
    glow(c, 960, 940, 260, "#FFB050", 0.38)
    br = ('<g transform="translate(960,960)"><circle r="72" fill="#1A1410"/><circle r="64" fill="url(#gold)" stroke="#1A1410" stroke-width="5"/><circle r="50" fill="#2A1E14" stroke="#7A4E10" stroke-width="4"/>'
          '<path d="M-34,10 Q-28,-24 6,-30 Q26,-34 34,-18 L52,-16 L36,-6 Q30,24 -6,30 L-22,40 Z" fill="#101018" stroke="#FFE08A" stroke-width="2.5"/><circle cx="16" cy="-18" r="4" fill="#FFE08A"/>'
          '<path d="M-58,-20 a60,60 0 0 1 40,-40" stroke="#FFF6C8" stroke-width="5" fill="none" stroke-linecap="round" opacity="0.9"/>'
          + "".join(f'<circle cx="{58*math.cos(a):.0f}" cy="{58*math.sin(a):.0f}" r="4" fill="#FFF0B0" stroke="#1A1410" stroke-width="2"/>' for a in [k * math.pi / 8 for k in range(16)]) + '</g>')
    draw(c, SD(br), 0, 0, 1.0)
    bloom_spot(c, 940, 940, 120, "#FFE8A8", 0.6); glow(c, 960, 960, 100, "#FFF0C0", 0.5)
    finish(c, cold=False, warm=0.08); return s

# ================================================================== P3a / P3b / P3c
def stones_ring(front):
    r = R_(31); o = []
    for k in range(18):
        a = 2 * math.pi * k / 18; x = 1180 + 600 * math.cos(a); y = 790 + 108 * math.sin(a)
        if (math.sin(a) > 0) != front: continue
        sc = 0.7 + 0.5 * (math.sin(a) + 1) / 2
        o.append(rock(x, y + 8, 30 * sc, r.uniform(80, 130) * sc, k + 100, "#6A6A68", "#C8CED0", "#26282A"))
    return "".join(o)

def banner_pole(x, y, h, c1, c2):
    return (f'<path d="M{x},{y} V{y-h}" stroke="{INK}" stroke-width="12"/><path d="M{x},{y} V{y-h}" stroke="#6A5038" stroke-width="6"/>'
            f'<path d="M{x+4},{y-h+8} Q{x+60},{y-h+0} {x+110},{y-h+20} L{x+84},{y-h+50} L{x+112},{y-h+86} Q{x+60},{y-h+70} {x+4},{y-h+84} Z" fill="{c1}" stroke="{INK}" stroke-width="4"/>'
            f'<path d="M{x+22},{y-h+30} l40,14 l-40,16" stroke="{c2}" stroke-width="5" fill="none"/>')

def p3a():
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    sky = f'<defs>{gradient("sk3a", [(0, "#8A98AA"), (0.6, "#C8D0D6"), (1, "#E4E6E4")])}</defs><rect width="1920" height="700" fill="url(#sk3a)"/>'
    draw(c, S(sky), 0, 0, 1.0)
    draw(c, blurred(S(cloud_band(81, 12, -100, 2000, 80, 300, "#9AA6B2", "#E8ECEE", 0.8, lit_dy=8, rx=(220, 460), ry=(30, 60))), 10), 0, 0, 1.0)
    glow(c, 520, 160, 400, "#FFF6E0", 0.25)
    draw(c, S(mountain_range(82, -40, 1960, 600, 250, 120, "#6A7886", "#9AA8B4", snow="#E8EEF2", light=1, snow_y=380, stroke="#3A4450", cid="a1") + mountain_range(83, -40, 1960, 640, 430, 60, "#4A5A52", "#6A7A70", snow="#C8D4D8", light=1, snow_y=500, stroke="#26302C", cid="a2")), 0, 0, 1.0)
    # fiyort + bağlı kayıklar
    fj = '<rect y="620" width="1920" height="70" fill="#5E7486"/><path d="M0,624 H1920" stroke="#A8B8C8" stroke-width="3" opacity="0.6"/>' + "".join(f'<g transform="translate({x},{y}) scale({s_})">{G.hull(1.0, shields=False, oars=False)}</g>' for x, y, s_ in ((200, 676, 0.24), (420, 664, 0.18), (1760, 672, 0.22)))
    draw(c, S(fj), 0, 0, 1.0)
    draw(c, blurred(S(cloud_band(84, 10, -100, 2000, 600, 690, "#E4E8EA", "#F6F8F8", 0.40, rx=(260, 500), ry=(14, 28))), 8), 0, 0, 1.0)
    # zemin: çiğnenmiş toprak, kırağı, çimen
    gd = O7.ground2(W, H, 680, seed=5) + grass(0, 1920, 700, 1060, 300, 15, ("#6A6A44", "#8A8A58", "#A8A878"), 12, 40, 14)
    draw(c, SD(gd), 0, 0, 1.0)
    fill(c, "#C8D2DC", 0.06)
    draw(c, S(stones_ring(False)), 0, 0, 1.0)
    # sancak direkleri + ateş çukuru
    bp = "".join(banner_pole(x, y, h, *cl_) for x, y, h, cl_ in ((560, 720, 300, ("#2F4C6E", "#D8C8A0")), (860, 700, 360, ("#8E2A22", "#C9A25A")), (1480, 700, 340, ("#3A5A34", "#D8C8A0")), (1780, 724, 290, ("#5A3A20", "#B8322A"))))
    draw(c, S(bp), 0, 0, 1.0)
    # kalabalık: halka içinde ve çevresinde
    army(c, "ragnar", [(745, 0.30, 16, 0.16), (775, 0.37, 15, 0.10)], t, seed0=71, facing=-1, x0=420, x1=1900)
    army(c, "ragnar", [(745, 0.30, 5, 0.16)], t, seed0=72, facing=1, x0=20, x1=420)
    # ateş çukuru
    pit = ('<g transform="translate(1180,800)"><ellipse cx="0" cy="8" rx="130" ry="30" fill="#000" opacity="0.4"/><ellipse cx="0" cy="0" rx="120" ry="26" fill="#2A221A"/>'
           + "".join(f'<ellipse cx="{120*math.cos(a):.0f}" cy="{26*math.sin(a):.0f}" rx="18" ry="11" fill="#5A5650" stroke="#14100C" stroke-width="3"/>' for a in [k * math.pi / 9 for k in range(18)]) + '</g>')
    draw(c, S(pit), 0, 0, 1.0)
    flames(c, 1100, 1260, 800, 110, t, seed=6, a=0.95); glow(c, 1180, 760, 260, "#FF9A40", 0.30)
    draw(c, blurred(S(smoke_curls(13, 3, 1150, 1210, 760, 330, 40, 0.4)), 8), 0, 0, 1.0)
    draw(c, S(stones_ring(True)), 0, 0, 1.0)
    draw(c, blurred(S(cloud_band(85, 8, -100, 2000, 700, 780, "#E8ECEE", "#F6F8F8", 0.20, rx=(240, 480), ry=(14, 30))), 10), 0, 0, 1.0)
    # Ragnar ve Bjorn
    RGw = full(dict(RG, _arm_up=False, _carry_svg=""), ex("determined", IF.blink_at(0.3)), 0.95, facing=1, look=0.5)
    BJw = full(dict(BJv, _arm_up=False), ex("awe", IF.blink_at(0.9)), 0.95, facing=1, look=0.6)
    rx_, ry_, bx_, by_ = 560, 1005, 830, 1012
    for sp, x, y, sc, ph in ((RGw, rx_, ry_, 0.98, 0.2), (BJw, bx_, by_, 0.98 * CH, 0.8)):
        soft_shadow(c, x + 20, y - 4, 130 * sc, 16, 0.5)
        with live(c, x, y, phase=ph, breathe=0.005):
            rim(c, sp, x, y, sc, "#FFF4DC", dx=-5, dy=-3, a=0.6); draw(c, sp, x, y, sc); shade_side(c, sp, x, y, 0.35, x - 150, x + 200, "#1A2430")
    # baba eli oğlunun omzunda
    sh_x, sh_y = rx_ + 36, ry_ - 372
    tx_, ty_ = bx_ - 32, by_ - 292
    arm = (f'<path d="M{sh_x},{sh_y} Q{sh_x + 110},{sh_y + 70} {tx_},{ty_}" stroke="{INK}" stroke-width="44" fill="none" stroke-linecap="round"/>'
           f'<path d="M{sh_x},{sh_y} Q{sh_x + 110},{sh_y + 70} {tx_},{ty_}" stroke="{RG.get("tunic", "#3B5A4A")}" stroke-width="32" fill="none" stroke-linecap="round"/>'
           f'<path d="M{sh_x},{sh_y - 6} Q{sh_x + 110},{sh_y + 62} {tx_},{ty_ - 8}" stroke="#FFFFFF" stroke-width="4" fill="none" opacity="0.18" stroke-linecap="round"/>'
           f'<path d="M{tx_ - 8},{ty_ - 8} q30,-12 62,4 q8,12 -4,20 q-34,6 -58,-6 Z" fill="{SK}" stroke="{INK}" stroke-width="5"/><path d="M{tx_ + 10},{ty_ + 6} v14 M{tx_ + 24},{ty_ + 6} v14 M{tx_ + 38},{ty_ + 4} v13" stroke="{SK3}" stroke-width="3"/>')
    draw(c, S(arm), 0, 0, 1.0)
    breath(c, rx_ + 40, ry_ - 0.98 * 585, 0.9, 0.5); breath(c, bx_ + 36, by_ - 0.98 * CH * 585, 0.7, 0.45)
    snowfall(c, t, (0, 70, W, H - 70), 40) if t else None
    card_at(c, "ŞEHİR MECLİSİ", 1250, 150, "Thing · yasa ve adalet meydanı") if False else None
    finish(c, cold=True); return s

def p3b():
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    draw(c, S(GR, TEXD, '<rect width="1920" height="1080" fill="#1E1812"/>'), 0, 0, 1.0)
    # arka plan: bulanık salon, kalabalık yüzleri
    draw(c, blurred(place(P7.greathall(0.9)), 12), -200, -120, 1.2)
    HSb = fig_bust(HARALD, ex("cold", IF.blink_at(0.7)), -0.4, 1.8, flip=False)
    draw(c, blurred(HSb, 14), 320, 400, 0.9); draw(c, blurred(fig_bust(dict(RG), ex("determined", IF.blink_at(0.2)), 0.2, 1.6), 16), 1580, 360, 0.9)
    fill(c, "#0A0604", 0.35)
    glow(c, 860, 600, 700, "#FFB060", 0.20)
    ring_b = ('<g transform="translate(1124,688) rotate(4)"><path d="M0,-92 A30,92 0 0 0 0,92" fill="none" stroke="#1A1410" stroke-width="30"/><path d="M0,-92 A30,92 0 0 0 0,92" fill="none" stroke="#9A6A1E" stroke-width="18"/></g>')
    ring_f = ('<g transform="translate(1124,688) rotate(4)"><path d="M0,-92 A30,92 0 0 1 0,92" fill="none" stroke="#1A1410" stroke-width="30"/><path d="M0,-92 A30,92 0 0 1 0,92" fill="none" stroke="url(#gold)" stroke-width="18"/>'
              '<path d="M10,-84 A30,86 0 0 1 24,-30" stroke="#FFF6C8" stroke-width="5" fill="none" stroke-linecap="round"/>'
              + "".join(f'<path d="M{30*math.sin(a):.0f},{-92*math.cos(a):.0f} l3,{10*math.cos(a)*-1:.0f}" stroke="#7A4E10" stroke-width="3"/>' for a in [k * math.pi / 12 for k in range(1, 12)]) + '</g>')
    draw(c, SD(ring_b), 0, 0, 1.0)
    # Bjorn'un genç önkolu (sağdan, yatay) + kürk yen + deri bileklik
    arm = ('<path d="M1920,520 Q1500,540 1260,600 L1270,760 Q1560,740 1920,760 Z" fill="#6A5238" filter="url(#t_kurk)"/><path d="M1920,520 Q1500,540 1260,600 L1270,760 Q1560,740 1920,760 Z" fill="none" stroke="#0E0804" stroke-width="8"/>'
           + "".join(f'<path d="M{1300 + k*34},{606 + k*4} q-8,40 2,80" stroke="#3A2A1A" stroke-width="3" opacity="0.7"/>' for k in range(16))
           + f'<path d="M1260,600 Q1130,612 1050,632 L1056,744 Q1150,742 1270,760 Z" fill="{SK}" stroke="{INK}" stroke-width="8"/><path d="M1050,632 Q1080,690 1056,744 L1270,760 L1260,600 Q1130,612 1050,632 Z" fill="{SK2}" opacity="0.30"/>'
           f'<path d="M1110,640 Q1170,626 1250,606" stroke="#F2D4B4" stroke-width="5" fill="none" opacity="0.7"/>'
           + '<path d="M1200,606 Q1180,680 1204,756" stroke="#0E0804" stroke-width="44"/><path d="M1200,606 Q1180,680 1204,756" stroke="#4A2E1A" stroke-width="32"/><path d="M1204,606 Q1184,680 1206,756" stroke="#8A6240" stroke-width="4" stroke-dasharray="8 6" fill="none"/>'
           + f'<path d="M1050,634 q-50,30 -48,60 q2,40 54,52 L1056,744" fill="{SK}" stroke="{INK}" stroke-width="8"/>'    # el (sıkılı yumruk, solda)
           f'<path d="M1034,650 q-26,20 -22,44 M1030,676 q-20,10 -16,30" stroke="{SK3}" stroke-width="3.5" fill="none"/>')
    draw(c, SD(arm), 0, 0, 1.0)
    # halka: bileğe geçiyor. Arka yarı bileğin arkasında, ön yarı önünde (dar elips: önkolu çevreler)
    draw(c, SD(ring_f), 0, 0, 1.0)
    sl = ('<g transform="translate(250,250)"><path d="M-20,150 Q300,170 560,300 L620,470 Q320,400 -20,380 Z" fill="#4A1A1A" filter="url(#t_yun)"/><path d="M-20,150 Q300,170 560,300 L620,470 Q320,400 -20,380 Z" fill="none" stroke="#0E0804" stroke-width="8"/>'
          + "".join(f'<path d="M{40 + k*50},{170 + k*10} Q{60 + k*52},{290} {40 + k*50},{390}" stroke="#2A0C0C" stroke-width="5" fill="none" opacity="0.7"/>' for k in range(10))
          + '<path d="M540,296 Q600,380 620,470 L700,470 Q690,360 600,290 Z" fill="#CFC3A0" filter="url(#t_kurk)" stroke="#0E0804" stroke-width="6"/></g>')
    draw(c, SD(sl), 0, 0, 1.0)
    SKo = "#D6B08C"
    oh = (f'<g transform="translate(880,690) scale(1.0)"><path d="M0,-40 Q60,-60 130,-50 L130,40 Q60,50 0,34 Z" fill="{SKo}" stroke="{INK}" stroke-width="7"/><path d="M0,-40 Q60,-60 130,-50" stroke="#F2D4B4" stroke-width="4" fill="none" opacity="0.7"/>'
          + capsule("M130,-34 Q190,-90 226,-100", 26, SKo, "#A88062") + capsule("M130,6 Q196,-10 226,-70", 23, SKo, "#A88062")
          + capsule("M120,30 Q170,50 190,36", 20, SKo, "#A88062") + capsule("M110,40 Q150,70 176,60", 18, SKo, "#A88062")
          + "".join(f'<path d="M{x},{y} q-6,{h_} 0,{h_*2}" stroke="#7A5A42" stroke-width="2.5" fill="none" opacity="0.8"/>' for x, y, h_ in ((170, -72, 9), (190, -88, 9), (200, -36, 8), (214, -48, 8)))
          + '<path d="M40,-30 q20,-4 50,2 M30,10 q40,6 80,-2" stroke="#8A6A4A" stroke-width="3" fill="none" opacity="0.6"/><path d="M60,-20 Q70,-10 60,0 M96,-26 q4,10 0,22" stroke="#7A8AA8" stroke-width="4" fill="none" opacity="0.4"/>'
          + '<circle cx="80" cy="12" r="4" fill="#8A5A38" opacity="0.5"/><path d="M-10,-40 Q-18,0 -8,36" stroke="#C8923A" stroke-width="10" fill="none"/></g>')
    draw(c, SD(oh), 0, 0, 1.0)
    # halkanın üzerine düşen ışık, parıltı
    bloom_spot(c, 1150, 640, 120, "#FFF2C0", 0.28); glow(c, 1124, 688, 420, "#FFC060", 0.22)
    for k in range(10):
        q = R_(k + 40); a = q.uniform(0, 6.28); r_ = q.uniform(120, 220)
        draw(c, S(f'<path d="M{1124 + r_*math.cos(a):.0f},{676 + r_*math.sin(a) - 14:.0f} v28 M{1124 + r_*math.cos(a) - 14:.0f},{676 + r_*math.sin(a):.0f} h28" stroke="#FFF6D0" stroke-width="3" opacity="0.8"/>'), 0, 0, 1.0)
    # ön plan: bulanık kürk ve deri parçası
    draw(c, blurred(SD(pelt(120, 1020, 260, 110, 31, "#3A2C20"), pelt(1760, 1040, 240, 90, 32, "#4A3828")), 15), 0, 0, 1.0)
    sh = skia.GradientShader.MakeRadial((880, 600), 1000, [col("#000", 0).toColor(), col("#000", 0).toColor(), col("#05030A", 0.6).toColor()], [0, 0.4, 1])
    c.drawRect(skia.Rect(0, 0, W, H), skia.Paint(Shader=sh))
    card_at(c, "KOL HALKASI", 1500, 190, "ilk halka") if False else None
    finish(c, cold=False, warm=0.08); return s

def p3c():
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    sky = f'<defs>{gradient("sk3c", [(0, "#4A5668"), (0.5, "#8A98A6"), (1, "#E8D8B8")])}</defs><rect width="1920" height="650" fill="url(#sk3c)"/>'
    draw(c, S(sky), 0, 0, 1.0)
    cl = (cloud_band(91, 11, -100, 1000, 70, 330, "#4A566A", "#C8CEDA", 0.95, lit_dy=9, rx=(220, 480), ry=(30, 64)) + cloud_band(92, 11, 1100, 2050, 70, 330, "#4A566A", "#C8CEDA", 0.95, lit_dy=9, rx=(220, 480), ry=(30, 64)))
    draw(c, blurred(S(cl), 6), 0, 0, 1.0)
    glow(c, 1080, 220, 700, "#FFE0A0", 0.45); glow(c, 1080, 220, 220, "#FFF6DC", 0.6)
    rays(c, 1080, 180, 90, 1100, 52, 12, "#FFE8B8", 0.14, t or 0.0)
    draw(c, S(mountain_range(93, -40, 1960, 610, 380, 100, "#586878", "#98A8B8", snow="#E8EEF2", light=1, snow_y=470, stroke="#2E3844", cid="c1") + mountain_range(94, -40, 1960, 640, 520, 40, "#3A4A48", "#6A7A70", light=1, stroke="#1E2826", cid="c2")), 0, 0, 1.0)
    draw(c, blurred(S(cloud_band(95, 12, -100, 2000, 590, 650, "#F0E4CC", "#FFF4DC", 0.4, rx=(240, 500), ry=(12, 24))), 7), 0, 0, 1.0)
    draw(c, S(sea_svg(634, "#C8B08A", "#1E2C3A", 1080, 96, glint="#FFF0C8", wl="#2E4252", hl="#E8E0C8", gn=150, spread=0.5)), 0, 0, 1.0)
    # kıyıdaki gemiler: direkler (sağda ve solda)
    shp = "".join(f'<g transform="translate({x},{y}) scale({s_})">{G.mast_sail(1.0, reefed=True)}{G.hull(1.0, shields=True, oars=False)}</g>' for x, y, s_ in ((230, 730, 0.46), (1620, 700, 0.34), (1820, 690, 0.22)))
    shf = blurred(S(shp), 0.8); draw(c, shf, 0, 0, 1.0)
    # kıyı: çakıl, ıslak taşlar, sığ dalga
    shore = "M0,780 Q500,760 1000,800 Q1500,840 1920,830 L1920,1090 L0,1090 Z"
    sh_svg = (f'<defs>{gradient("sh3", [(0, "#4A4640"), (0.5, "#2A2824"), (1, "#16140F")])}<clipPath id="shc3"><path d="{shore}"/></clipPath></defs><path d="{shore}" fill="url(#sh3)"/><g clip-path="url(#shc3)"><rect width="1920" height="1080" filter="url(#t_tas)" fill="#4A4640" opacity="0.5"/>'
              + pebbles(120, 560, -20, 1940, 790, 1090, hl="#F0E0B8") + '<path d="M0,790 Q500,772 1000,812 Q1500,852 1920,842" stroke="#FFE8B0" stroke-width="10" fill="none" opacity="0.30"/></g>'
              + foam_line(-20, 1940, 800, 21, 0.9, 10) + foam_line(-20, 1940, 826, 22, 0.55, 12))
    draw(c, SD(sh_svg), 0, 0, 1.0)
    draw(c, SD(rock(1500, 1010, 120, 80, 12, "#3A3A3C", "#B8B0A0", "#14120E"), rock(1720, 1020, 70, 46, 13, "#3A3A3C", "#B8B0A0", "#14120E"), rock(320, 1020, 100, 60, 14, "#3A3A3C", "#B8B0A0", "#14120E")), 0, 0, 1.0)
    # baba ve oğul: arkadan
    RGb = sprite(f'<g transform="translate(500,1240) scale(0.95,0.95)">{figure(dict(RG, _arm_up=True, _carry_svg=""), "3q", "stand", ex("determined", IF.blink_at(0.3)), hands=("open", "point"), look=0.9)}</g>', 1000, 1300, ax=500, ay=1240, ss=1.0)
    BJb = full(dict(BJv, _arm_up=False), ex("awe", IF.blink_at(0.9)), 0.95, facing=1, look=0.9)
    rx_, ry_, bx_, by_ = 760, 1000, 1070, 1006
    for sp, x, y, ph, sc in ((RGb, rx_, ry_, 0.2, 1.0), (BJb, bx_, by_, 0.9, CH)):
        soft_shadow(c, x, y - 4, 120 * sc, 14, 0.5)
        with live(c, x, y, phase=ph, breathe=0.004, sway=0.006, rot=(-2.5 if sc < 1 else 0)):
            rim(c, sp, x, y, sc, "#FFE8B0", dx=6, dy=-3, a=0.85); draw(c, sp, x, y, sc); shade_side(c, sp, x, y, 0.30, x + 200, x - 160, "#1A1420")
    # kuzgun, umut ışığı, serpinti
    draw(c, S(Bm.raven(1480, 330, 0.5, 1, "fly", 3)), 0, 0, 1.0)
    glow(c, 1260, 460, 260, "#FFE8B0", 0.12)
    draw(c, blurred(S(grass(-40, 1960, 1030, 1090, 200, 24, ("#14120E", "#241E16"), 50, 120, 30)), 5), 0, 0, 1.0)
    card_at(c, "BJORN", 1340, 760, "12 yaşında · ilk halka")
    finish(c, cold=False, warm=0.07); return s

FR = {"p1a": p1a, "p1b": p1b, "p1c": p1c, "p1d": p1d, "p2a": p2a, "p2b": p2b, "p2c": p2c, "p3a": p3a, "p3b": p3b, "p3c": p3c}
CROPS = {"p1c": [(760, 440, 480, 270), (1000, 640, 480, 270)], "p2b": [(720, 130, 480, 270), (700, 480, 480, 270)], "p3b": [(600, 420, 480, 270), (1000, 440, 480, 270)], "p1d": [(480, 380, 480, 270), (900, 280, 480, 270)]}

def contact():
    from PIL import Image
    ids = list(FR); sheet = Image.new("RGB", (960 * 2 + 30, 560 * 5 + 10), "#EDE2CC")
    for k, i in enumerate(ids):
        p = f"{OUTP}/{i}.png"
        if os.path.exists(p): sheet.paste(Image.open(p).convert("RGB").resize((960, 540)), (10 + (k % 2) * 970, 10 + (k // 2) * 560))
    sheet.save(f"{OUTP}/kontakt_prolog_960.png")

if __name__ == "__main__":
    a = sys.argv[1:] or ["all"]
    if "test" in a: T[0] = None; test(); a = [x for x in a if x != "test"]
    ids = list(FR) if a == ["all"] else a
    for i in ids:
        if i not in FR: continue
        T[0] = None; p = f"{OUTP}/{i}.png"
        try:
            FR[i]().makeImageSnapshot().save(p, skia.kPNG); print("kare", i)
            for k, b in enumerate(CROPS.get(i, []), 1): crop2x(p, b, f"{OUTP}/{i}_crop{k}.png")
        except Exception as e:
            import traceback; traceback.print_exc()
    contact()

# ---------------------------------------------------------------- P2b v3: Odin, model gövdesiyle kahraman savaşçı tanrı (kullanıcı 20.11)
def _odin_extras():
    def wing(sx):   # düzgün katmanlı kuzgun kanadı yanak koruyucu: geriye ve aşağı (boynuz değil)
        o = []
        for k in range(6):
            L = 70 + k * 10; ang = 18 + k * 9
            x0, y0 = sx * 80, -70 + k * 6
            x1 = x0 + sx * L * math.cos(math.radians(ang)); y1 = y0 + L * math.sin(math.radians(ang))
            o.append(f'<path d="M{x0},{y0} Q{(x0+x1)/2 + sx*6:.0f},{(y0+y1)/2 - 14:.0f} {x1:.0f},{y1:.0f} Q{(x0+x1)/2 - sx*4:.0f},{(y0+y1)/2 + 6:.0f} {x0},{y0+12} Z" fill="{"#20222C" if k % 2 else "#2C3040"}" stroke="#08080C" stroke-width="3.5"/>'
                     f'<path d="M{x0},{y0+5} L{x1 - sx*6:.0f},{y1 - 3:.0f}" stroke="#6A7A9A" stroke-width="1.6"/>')
        return "".join(o[::-1])
    return (wing(-1) + wing(1) + HELMET_O +
            '<path d="M-36,-20 Q-15,-30 6,-20 Q8,4 -15,10 Q-36,4 -36,-20 Z" fill="#2A1A10" stroke="#0A0604" stroke-width="4"/>'
            '<path d="M-80,-44 L-34,-16 M6,-18 L78,-48" stroke="#2A1A10" stroke-width="7"/>'
            '<circle cx="42" cy="-7" r="9" fill="#DFF6FF"/><circle cx="42" cy="-7" r="18" fill="#9CDCFF" opacity="0.35"/><circle cx="42" cy="-7" r="30" fill="#9CDCFF" opacity="0.15"/>')
HELMET_O = ('<path d="M-84,-28 Q-88,-128 0,-132 Q88,-128 84,-28 Z" fill="#6E747C" stroke="#1A1410" stroke-width="7"/>'
            '<path d="M-84,-36 L84,-36" stroke="#C9A25A" stroke-width="12"/><path d="M0,-132 L0,-34" stroke="#C9A25A" stroke-width="9"/>'
            '<path d="M-60,-100 Q0,-122 60,-100" stroke="#9AA2AC" stroke-width="5" fill="none"/>'
            '<rect x="-7" y="-38" width="14" height="40" fill="#5A5E64" stroke="#1A1410" stroke-width="4"/>')
GUNGNIR = ('<g transform="translate(HX,HY)"><path d="M0,160 L0,-360" stroke="#1A1410" stroke-width="20" stroke-linecap="round"/><path d="M0,160 L0,-360" stroke="#5A4028" stroke-width="12"/>'
           + "".join(f'<path d="M-4,{-60 - k*70} l8,14 l-8,14 M4,{-60 - k*70} v28" stroke="#FFD27A" stroke-width="4" fill="none"/>' for k in range(4))
           + '<circle cx="0" cy="-400" r="70" fill="#9CDCFF" opacity="0.25"/><path d="M0,-480 L26,-380 L0,-350 L-26,-380 Z" fill="#DCE6EE" stroke="#1A1410" stroke-width="6"/>'
           '<path d="M0,-470 L0,-360" stroke="#FFFFFF" stroke-width="4"/><path d="M-30,-346 L30,-346" stroke="#C9A25A" stroke-width="12"/></g>')
ODIN = dict(RAGNAR3, hair="#C8C4BC", beard_c="#D0CCC4", beard_len=1.25, beard_w=1.1, old=True, beard_braid=True, iris="#8FCFF0", skin="#E2C2A2",
            tunic="#5E646C", trim="#C9A25A", cloak="#141A2A", fur_collar="#5E5244", face_scar=False, knot=False, armring=True, clasp="",
            brow_c="#B8B4AC", brow_k=0.9, no_blush=True)

def _raven(x, y, s=1.0, flip=1):
    return (f'<g transform="translate({x},{y}) scale({s*flip},{s})"><path d="M0,0 Q-60,-70 -170,-60 Q-110,-40 -130,-20 Q-80,-24 -90,0 Q-40,-6 0,10 Z" fill="#14141A" stroke="#000" stroke-width="4"/>'
            '<path d="M0,0 Q50,-80 150,-90 Q100,-60 120,-40 Q70,-40 80,-16 Q40,-14 0,10 Z" fill="#1E1E28" stroke="#000" stroke-width="4"/>'
            '<path d="M-20,4 Q10,-10 40,4 Q20,22 -20,18 Z" fill="#14141A" stroke="#000" stroke-width="4"/><path d="M40,2 L62,8 L40,12 Z" fill="#3A3A3A"/>'
            '<path d="M-20,12 L-56,30 L-30,10 Z" fill="#14141A"/><circle cx="32" cy="4" r="3" fill="#9CDCFF"/></g>')

def p2b():
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    draw(c, blurred(hall_base(), 6), 0, 0, 1.0); fill(c, "#06080E", 0.55)
    vis = ['<defs><radialGradient id="vg" cx="0.5" cy="0.45" r="0.6"><stop offset="0" stop-color="#E8D49A" stop-opacity="0.55"/><stop offset="0.45" stop-color="#3A4E8A" stop-opacity="0.45"/><stop offset="1" stop-color="#0A0E1E" stop-opacity="0"/></radialGradient></defs>',
           '<ellipse cx="960" cy="520" rx="760" ry="560" fill="url(#vg)"/>']
    for k in range(16):   # ışık hüzmeleri
        a = -math.pi / 2 + (k - 7.5) * 0.11; vis.append(f'<path d="M960,430 L{960 + 1200*math.cos(a-0.03):.0f},{430 + 1200*math.sin(a-0.03):.0f} L{960 + 1200*math.cos(a+0.03):.0f},{430 + 1200*math.sin(a+0.03):.0f} Z" fill="#F4E2A8" opacity="0.07"/>')
    for k, (col_, yy) in enumerate((("#5ADFB0", 170), ("#7A6AE8", 230), ("#4AB0E8", 290))):   # aurora
        vis.append(f'<path d="M180,{yy} Q600,{yy-90} 960,{yy-20} Q1340,{yy+50} 1740,{yy-60}" stroke="{col_}" stroke-width="{40-k*8}" fill="none" opacity="0.28"/>')
    vis.append('<path d="M330,120 L290,260 L340,256 L270,430" stroke="#EAF4FF" stroke-width="9" fill="none"/><path d="M1600,110 L1640,240 L1590,236 L1660,400" stroke="#EAF4FF" stroke-width="9" fill="none"/>')
    draw(c, svg_sprite("".join(vis)), 0, 0, 1.0)
    cloak = ('<path d="M820,730 Q620,760 470,1020 Q560,990 600,1040 Q660,980 720,1040 Q780,990 840,1040 L980,1040 Q1060,990 1120,1040 Q1180,980 1240,1040 Q1300,990 1380,1030 Q1220,760 1000,600 Z" fill="#141A2A" stroke="#05070C" stroke-width="8"/>'
             '<path d="M470,1020 Q560,990 600,1040 Q660,980 720,1040 Q780,990 840,1040 M1120,1040 Q1180,980 1240,1040 Q1300,990 1380,1030" stroke="#C9A25A" stroke-width="8" fill="none"/>'
             + "".join(f'<path d="M{900 + dx},{770} Q{900 + dx*1.6:.0f},{840} {900 + dx*2.2:.0f},{1030}" stroke="#0A0E18" stroke-width="5" fill="none"/>' for dx in (-160, -90, 80, 150))
             + '<ellipse cx="910" cy="740" rx="190" ry="70" fill="#4E4436" stroke="#1A1410" stroke-width="6"/>'
             + "".join(f'<path d="M{760 + k*22},{730 + (k % 3)*10} q6,26 -2,48" stroke="#2E2820" stroke-width="5" fill="none"/>' for k in range(15)))
    draw(c, svg_sprite(cloak), 0, 0, 1.0)
    OD = full(dict(ODIN, _head_extra=_odin_extras(), _arm_up=True, _hand_extra=GUNGNIR), ex("fierce", IF.blink_at(0.4)), 1.18, facing=1, look=0.2)
    rim(c, OD, 900, 1230, 1.0, "#BFE6FF", dx=-8, dy=-4, a=0.9); draw(c, OD, 900, 1230, 1.0)
    shade_side(c, OD, 900, 1230, 0.35, 700, 1100, "#0A0E1E")
    import v3_b as _VB
    draw(c, svg_sprite(_VB.raven(470, 330, 1.6, 1, 'fly', 1) + _VB.raven(1430, 300, 1.4, -1, 'fly', 2)), 0, 0, 1.0)
    smoke = "".join(f'<ellipse cx="{960 + random.Random(k).uniform(-700, 700):.0f}" cy="{random.Random(k + 50).uniform(780, 1040):.0f}" rx="{random.Random(k + 7).uniform(160, 360):.0f}" ry="{random.Random(k + 9).uniform(50, 110):.0f}" fill="#B8B4C8" opacity="0.10"/>' for k in range(26))
    draw(c, blurred(svg_sprite(smoke), 10), 0, 0, 1.0)
    weave = "".join(f'<path d="M0,{y} H1920" stroke="#E8D49A" stroke-width="1" opacity="0.06"/>' for y in range(70, 1010, 6))
    draw(c, svg_sprite(weave), 0, 0, 1.0)   # anlatılan masal: hafif dokuma dokusu
    glow(c, 960, 1060, 800, "#FF7A2A", 0.28); bloom_spot(c, 960, 1040, 260, "#FFB060", 0.4)
    card_at(c, "ODİN", 1620, 200, "savaş ve bilgelik tanrısı")
    finish(c, cold=False, warm=0.04); return s
FR["p2b"] = p2b

# ---------------------------------------------------------------- P2b v4: devasa, ilahi Odin; göğe yükselen tanrı, altta minik ev (kullanıcı 20.11)
def p2b():
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    sky = ['<defs><linearGradient id="ns" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#05070F"/><stop offset="0.6" stop-color="#1A2340"/><stop offset="1" stop-color="#2A2E44"/></linearGradient>'
           '<radialGradient id="halo" cx="0.5" cy="0.32" r="0.5"><stop offset="0" stop-color="#F6E6B0" stop-opacity="0.75"/><stop offset="0.5" stop-color="#7A8AD0" stop-opacity="0.25"/><stop offset="1" stop-color="#05070F" stop-opacity="0"/></radialGradient></defs>',
           f'<rect width="{W}" height="{H}" fill="url(#ns)"/><ellipse cx="960" cy="340" rx="900" ry="620" fill="url(#halo)"/>']
    for k in range(24):
        a = -math.pi / 2 + (k - 11.5) * 0.13; sky.append(f'<path d="M960,300 L{960 + 1500*math.cos(a-0.035):.0f},{300 + 1500*math.sin(a-0.035):.0f} L{960 + 1500*math.cos(a+0.035):.0f},{300 + 1500*math.sin(a+0.035):.0f} Z" fill="#F4E2A8" opacity="0.06"/>')
    for k, (col_, yy) in enumerate((("#5ADFB0", 120), ("#7A6AE8", 175), ("#4AB0E8", 230))):
        sky.append(f'<path d="M-40,{yy+60} Q500,{yy-60} 960,{yy} Q1420,{yy+60} 1960,{yy-40}" stroke="{col_}" stroke-width="{56-k*12}" fill="none" opacity="0.22"/>')
    r = random.Random(3)
    for k in range(160): sky.append(f'<circle cx="{r.uniform(0,W):.0f}" cy="{r.uniform(70,520):.0f}" r="{r.uniform(0.8,2.2):.1f}" fill="#FFFFFF" opacity="{r.uniform(0.3,0.9):.2f}"/>')
    draw(c, svg_sprite("".join(sky)), 0, 0, 1.0)
    # devasa Odin büstü (model gövdesi), mızrak kalkık
    OD = fig_bust(dict(ODIN, _head_extra=_odin_extras(), _arm_up=True, _hand_extra=GUNGNIR), ex("fierce", IF.blink_at(0.4)), 0.15, 2.35)
    cape = ('<path d="M960,560 Q500,620 120,1080 L1800,1080 Q1420,620 960,560 Z" fill="#101626" stroke="#05070C" stroke-width="10"/>'
            + "".join(f'<path d="M960,600 Q{960 + dx*0.6:.0f},820 {960 + dx},1080" stroke="#070A14" stroke-width="7" fill="none"/>' for dx in (-700, -420, -160, 160, 420, 700)))
    draw(c, svg_sprite(cape), 0, 0, 1.0)
    rim(c, OD, 960, 420, 1.0, "#CFEAFF", dx=0, dy=-8, a=0.9); draw(c, OD, 960, 420, 1.0)
    glow(c, 960, 300, 520, "#F6E6B0", 0.12)
    # Gungnir ucundan yıldırım
    bolt = '<path d="M1240,150 L1320,300 L1270,310 L1390,520 L1340,526 L1480,780" stroke="#EAF6FF" stroke-width="12" fill="none" stroke-linejoin="bevel"/><path d="M1240,150 L1320,300 L1270,310 L1390,520 L1340,526 L1480,780" stroke="#9CC8FF" stroke-width="34" fill="none" opacity="0.25"/>'
    # Odin'in alt bedenini yutan bulutlar + altta minik dünya: fiyort, dağlar, uzun ev ve göğe yükselen duman
    clouds = "".join(f'<ellipse cx="{r.uniform(-100, 2020):.0f}" cy="{r.uniform(760, 900):.0f}" rx="{r.uniform(220, 460):.0f}" ry="{r.uniform(70, 140):.0f}" fill="{r.choice(["#2A3050", "#343A5C", "#3E4466"])}" opacity="0.92"/>' for _ in range(30))
    clouds += "".join(f'<ellipse cx="{r.uniform(0, 1920):.0f}" cy="{r.uniform(740, 800):.0f}" rx="{r.uniform(160, 320):.0f}" ry="{r.uniform(30, 60):.0f}" fill="#8A90B8" opacity="0.35"/>' for _ in range(14))
    world = ('<path d="M0,900 L180,820 L340,860 L520,780 L700,850 L900,800 L1100,860 L1300,790 L1500,850 L1700,800 L1920,860 L1920,1080 L0,1080 Z" fill="#0E1220" stroke="#05070C" stroke-width="5"/>'
             '<path d="M0,960 Q500,930 960,950 Q1400,970 1920,940 L1920,1080 L0,1080 Z" fill="#1A2236"/><path d="M200,975 Q700,955 1200,975" stroke="#4A5A7A" stroke-width="3" fill="none" opacity="0.6"/>')
    house = (f'<g transform="translate(960,1000) scale(0.32)">{O7.thatch_house(0, 0, 1.0, smoke=False)}</g>'
             '<rect x="952" y="985" width="16" height="14" fill="#FFB060"/>')
    smoke = "".join(f'<ellipse cx="{960 + 40*math.sin(k*0.7):.0f}" cy="{950 - k*22}" rx="{16 + k*5}" ry="{12 + k*3}" fill="#B8B4C8" opacity="{0.45 - k*0.018:.2f}"/>' for k in range(18))
    draw(c, svg_sprite(bolt + clouds + world + smoke + house), 0, 0, 1.0)
    import v3_b as _VB
    draw(c, svg_sprite(_VB.raven(420, 420, 1.0, 1, 'fly', 1) + _VB.raven(1560, 560, 0.85, -1, 'fly', 2)), 0, 0, 1.0)
    bloom_spot(c, 960, 990, 60, "#FFB060", 0.6); bloom_spot(c, 1240, 150, 160, "#DDEEFF", 0.5)
    card_at(c, "ODİN", 1620, 170, "savaş ve bilgelik tanrısı")
    finish(c, cold=False, warm=0.02); return s
FR["p2b"] = p2b
