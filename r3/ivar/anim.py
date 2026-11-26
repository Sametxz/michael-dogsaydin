"""Ivar nehir kıyısında (madde 9) animatiği v1."""
import sys, math, random, os, json
sys.path[:0] = ["/home/claude/r3", "/home/claude/r2", "/home/claude/r3/veda", "/home/claude/r3/ivar"]
import skia
from engine import *
from fx import *
from common import *
OUT = "/home/claude/r3/ivar/out"; os.makedirs(OUT, exist_ok=True)
CUE = json.load(open("/home/claude/r3/ivar/cues.json"))
EXP["stern_tw"] = (6, -2, 0.30, 0.06, "firm", "")
EXP["relief"] = (-12, 6, 0.55, 0.12, "soft_smile", "tear")
def BG(svg): return sprite(f'<g transform="scale(2)">{svg}</g>', W, H)
def SP(svg, w, h, ax, ay): return sprite(svg, w, h, ax=ax, ay=ay)
def FIG(spec, view="3q", expr="neutral", facing=1, pose="stand", hands=("open", "fist"), extra=""):
    g = figure(spec, view, "stand", expr, facing=facing, hands=hands) if pose == "stand" else figure(spec, "front", pose, expr, facing=facing, hands=hands)
    return SP(f'<g transform="translate(400,1000)">{g}{extra}</g>', 800, 1100, 400, 1000)
def cam(c, z, cx, cy, fn):
    z = max(1.0, z); hw, hh = W / (2 * z), H / (2 * z)
    cx = min(max(cx, hw), W - hw); cy = min(max(cy, hh), H - hh)
    c.save(); c.translate(W / 2, H / 2); c.scale(z, z); c.translate(-cx, -cy); fn(); c.restore()
def post(c, warm=0.0, cold=0.25):
    if warm: grade(c, "#FFB060", warm, "screen")
    gradient_grade(c, "#2A4A6E", "#1A2A3A", 0.3, "soft"); grade(c, "#9EB6CC", cold, "multiply")
    vignette(c, 0.72); letterbox(c, 1.0, 70)

# ── ev (kral evinden ölçülü öğeler)
def house_svg(door=True):
    o = '<rect width="960" height="540" fill="#22190F"/>' + "".join(f'<rect x="{x}" y="60" width="38" height="360" fill="{["#32261B","#2E2318","#36291D"][i % 3]}"/>' for i, x in enumerate(range(0, 960, 38)))
    o += '<path d="M0,70 L480,-60 L960,70 L960,0 L0,0 Z" fill="#1A120C"/><rect x="0" y="400" width="960" height="140" fill="#3A2E22"/>'
    o += '<rect x="610" y="40" width="50" height="400" fill="#4A3826" stroke="#1A1410" stroke-width="5"/>' + "".join(f'<path d="M616,{y} q19,12 38,0" stroke="#2E2218" stroke-width="4" fill="none"/>' for y in range(90, 430, 46))
    o += '<rect x="80" y="330" width="330" height="70" fill="#4A3826" stroke="#1A1410" stroke-width="4"/><path d="M70,330 Q240,296 420,330 L410,352 L80,352 Z" fill="#8A7A62" stroke="#1A1410" stroke-width="4"/>'
    o += '<rect x="440" y="442" width="150" height="30" rx="8" fill="#1E140E"/>' + "".join(f'<ellipse cx="{440 + k*15}" cy="{442 if k % 2 else 472}" rx="11" ry="8" fill="{["#6A6058","#7A7068","#5A5048"][k % 3]}" stroke="#1A1410" stroke-width="2"/>' for k in range(11)) + '<ellipse cx="436" cy="457" rx="9" ry="14" fill="#6A6058" stroke="#1A1410" stroke-width="2"/><ellipse cx="594" cy="457" rx="9" ry="14" fill="#6A6058" stroke="#1A1410" stroke-width="2"/>'
    if door: o += '<rect x="770" y="140" width="120" height="270" fill="#2E4466" stroke="#1A1410" stroke-width="6"/>'
    return o
BGH = BG(house_svg())
ASLs = FIG(ASL, "3q", "determined", facing=-1, hands=("grip", "grip"), extra=baby(-30, -330, 1.3))
RGs = FIG(RG, "3q", "cold", facing=-1); RGt = FIG(RG, "3q", "stern_tw", facing=-1)
FOOT = SP(f'<g transform="translate(470,300)">{baby(-60, 0, 4.0, foot=True)}</g>', 1000, 560, 470, 300)
def embers(c, x, y, t, k=1.0):
    glow(c, x, y, 300, "#FF7A30", 0.28 * k * (1 + 0.1 * math.sin(t * 9)))
    for j in range(9):  # nabız gibi atan közler
        rr = random.Random(j + 40); px = x - 120 + rr.uniform(0, 240); pu = 0.6 + 0.4 * math.sin(t * rr.uniform(2, 4) + j)
        c.drawCircle(px, y + 14 + rr.uniform(-6, 6), rr.uniform(6, 11), skia.Paint(Color4f=col("#FF6A20", 0.55 * k * pu), AntiAlias=True))
    for j in range(3):
        q = ((t * 0.25 + j / 3) % 1.0); bloom_spot(c, x + 30 * math.sin(q * 5 + j), y - 300 * q, 24 + 40 * q, "#6A6460", 0.18 * (1 - q) * k)
    for j in range(6):
        q = ((t * 0.5 + j / 6) % 1.0); rr = random.Random(j)
        c.drawCircle(x + rr.uniform(-120, 120), y - 200 * q, 3 * (1 - q), skia.Paint(Color4f=col("#FFB060", 0.8 * (1 - q)), AntiAlias=True))
def shot1(c, t, d):
    B = CUE["bacak"]
    if B < t < B + 1.0:   # ayak: tek, kısa yakın plan
        def w2():
            c.drawRect(skia.Rect(0, 0, W, H), skia.Paint(Color4f=col("#2A2018")))
            draw(c, FOOT, 900, 560, 1.0)
            glow(c, 1260, 640, 260, "#FFB060", 0.35)
        cam(c, 1.0 + 0.08 * (t - B), 1150, 600, w2); post(c, warm=0.06, cold=0.15); return
    q = lin(t, B + 1.0, d); z = 1.0 + (0.0 if t < B else 0.35 * ease_io(q))
    def world():
        draw(c, BGH, W / 2, H / 2); embers(c, 1030, 914, t)
        draw(c, ASLs, 520, 900, 0.92, sy=0.92 * (1 + 0.006 * math.sin(t * 2.4)))
        draw(c, RGt if (t > B + 1.6 and int(t * 5) % 3 == 0) else RGs, 1300, 1000, 0.98)
    cam(c, z, 960 if t < B else 1300, 540 if t < B else 430, world); post(c, warm=0.06, cold=0.18)

BGH2 = BG(house_svg())
SLEEP = SP(f'<g transform="translate(300,140)"><ellipse cx="-190" cy="-6" rx="70" ry="22" fill="#C8B898" stroke="#1A1410" stroke-width="4"/>'
           f'<path d="M-170,-10 Q20,-56 200,-20 Q230,10 200,34 L-160,34 Z" fill="#6A5A70" stroke="#1A1410" stroke-width="5"/>'
           f'<g transform="translate(-190,-40) rotate(-80) scale(0.5)">{head3(dict(ASL), "side", "grief_closed")}</g>'
           f'<path d="M-150,-20 Q-60,-10 20,-4" stroke="{ASL["hair"]}" stroke-width="16" fill="none" stroke-linecap="round"/><path d="M-150,-20 Q-60,-10 20,-4" stroke="#1A1410" stroke-width="2" fill="none" stroke-dasharray="6 8"/></g>', 600, 260, 300, 140)
RG2 = FIG(RG, "side", "cold", extra=baby(60, -360, 1.2)); RG2b = FIG(RG, "side", "stern_tw", facing=-1, extra=baby(-60, -360, 1.2)); RG2n = FIG(RG, "side", "cold")
def shot2(c, t, d):
    A = CUE["aliyor"]; take = ease_io(lin(t, A - 0.6, A)); look = A + 0.1 < t < A + 0.7; close = ease_io(lin(t, A + 0.7, A + 1.3))
    def world():
        draw(c, BGH2, W / 2, H / 2); embers(c, 1030, 914, t, 0.4)
        c.drawRect(skia.Rect(1540 + 240 * close, 280, 1780, 820), skia.Paint(Color4f=col("#4A6A92", 0.6)))
        light_shaft(c, 1660, 240 * (1 - close), 1300, 500 * (1 - close), "#9AB6D6", 0.25 * (1 - close), t, y_top=280, y_bot=1080)
        draw(c, SLEEP, 520, 700, 1.0)
        x = 900 + 600 * ease_in(lin(t, A + 0.7, d))
        if t < A:   # bebek yalnızca yatakta, sonra yalnızca kucakta
            draw(c, BABYs, 720 + 60 * take, 700 - 120 * take, 1.0)
            draw(c, RG2n, 900, 1000, 0.92)
        else:
            draw(c, RG2b if look else RG2, x, 1000, 0.92)
    cam(c, 1.0, W / 2, H / 2, world); post(c, cold=0.35 + 0.15 * close)
BABYs = SP(f'<g transform="translate(120,90)">{baby(0, 0, 1.4)}</g>', 240, 150, 120, 90)

# ── nehir kıyısı: 3 katmanlı sisli orman
def forest_layer(seed, n, y, hmin, hmax, wmin, wmax, color, roots=False):
    r = random.Random(seed); o = ""
    for _ in range(n):
        x = r.uniform(-40, 1000); h = r.uniform(hmin, hmax); w = r.uniform(wmin, wmax); top = y - h
        o += f'<path d="M{x-w/2:.0f},{y} L{x-w*0.35:.0f},{top:.0f} L{x+w*0.35:.0f},{top:.0f} L{x+w/2:.0f},{y} Z" fill="{color}"/>'
        for k in range(3):
            by_ = top + h * r.uniform(0.15, 0.6); sd = r.choice([-1, 1])
            o += f'<path d="M{x:.0f},{by_:.0f} q{sd*20:.0f},{-14:.0f} {sd*r.uniform(30,60):.0f},{-r.uniform(20,50):.0f}" stroke="{color}" stroke-width="{max(2, w*0.25):.0f}" fill="none" stroke-linecap="round"/>'
        if roots: o += f'<path d="M{x-w*1.2:.0f},{y+6} Q{x-w*0.5:.0f},{y-10} {x:.0f},{y-14} Q{x+w*0.5:.0f},{y-10} {x+w*1.2:.0f},{y+6} Z" fill="{color}"/>'
    return o
FOG_FAR = BG('<rect width="960" height="540" fill="url(#g)"/><defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8E9CAA"/><stop offset="1" stop-color="#C8D2DA"/></linearGradient></defs>'
             + forest_layer(1, 40, 360, 120, 200, 6, 10, "#9AA6B2"))
MID = BG(forest_layer(2, 22, 372, 180, 280, 10, 18, "#6E7A86") + '<path d="M-20,372 Q480,362 980,374 L980,390 L-20,390 Z" fill="#6E7A86"/>')
NEAR = BG('<path d="M0,380 Q480,360 960,382 L960,440 Q480,420 0,446 Z" fill="#6E8496"/>'
          + forest_layer(3, 6, 452, 380, 460, 22, 34, "#33393E", roots=True)
          + '<path d="M0,430 Q480,410 960,436 L960,540 L0,540 Z" fill="#5A5248"/>'
          + "".join(f'<ellipse cx="{random.Random(k).uniform(0,960):.0f}" cy="{random.Random(k+70).uniform(450,540):.0f}" rx="{random.Random(k+5).uniform(10,30):.0f}" ry="{random.Random(k+9).uniform(6,12):.0f}" fill="{["#7A7268","#8A8278","#6A6258"][k%3]}" stroke="#3A342C" stroke-width="2"/>' for k in range(44)))
def river_env(c, t, fogk=1.0):
    draw(c, FOG_FAR, W / 2, H / 2)
    fog(c, t, 640, "#D8E0E6", 0.45 * fogk, seed=2, speed=14)
    draw(c, MID, W / 2, H / 2)
    fog(c, t, 760, "#DDE4EA", 0.40 * fogk, seed=5, speed=22)
    draw(c, NEAR, W / 2, H / 2)
    for k in range(16):  # su yüzeyi kırık yansımalar + buhar
        rr = random.Random(k); x = (rr.uniform(0, W) + t * 30) % W; y = rr.uniform(790, 860)
        c.drawLine(x, y, x + rr.uniform(30, 70), y, skia.Paint(Color4f=col("#D8E6F0", 0.45), StrokeWidth=3, AntiAlias=True))
    for k in range(5):
        q = ((t * 0.12 + k / 5) % 1.0); bloom_spot(c, 200 + k * 380 + 40 * q, 800 - 120 * q, 120, "#E8EEF2", 0.18 * math.sin(q * math.pi))
KN = puppet.kneel_side(); HK = puppet.head_side("grief_down")
BB = SP(f'<g transform="translate(150,110)">{baby(0, 0, 1.6, cry=True)}</g>', 300, 180, 150, 110)
KNF = SP(f'<g transform="translate(40,130)">{knife(0, 0, 1.2)}</g>', 80, 200, 40, 130)
def shot3(c, t, d):
    K = CUE["bicak"]; lift = ease_out(lin(t, 0.6, K))
    def world():
        river_env(c, t)
        kx, ky, ks = 620, 960, 0.66
        draw(c, KN, kx, ky, ks); draw(c, HK, kx - 2, ky - ks * 470, ks, rot=6)
        sx_, sy_ = kx - 4, ky - ks * 326
        hx, hy = sx_ + 70 + 10 * lift, sy_ - 40 - 150 * lift       # el baş hizasında, bebekten uzak
        pa = skia.Path(); pa.moveTo(sx_, sy_); pa.quadTo(sx_ + 60, sy_ - 10, hx, hy)
        c.drawPath(pa, skia.Paint(Color4f=col("#1A1410"), StrokeWidth=34, Style=skia.Paint.kStroke_Style, StrokeCap=skia.Paint.kRound_Cap, AntiAlias=True))
        c.drawPath(pa, skia.Paint(Color4f=col(RG["tunic"]), StrokeWidth=26, Style=skia.Paint.kStroke_Style, StrokeCap=skia.Paint.kRound_Cap, AntiAlias=True))
        draw(c, KNF, hx, hy, 1.0, rot=6 * math.sin(t * 20) * lin(t, K, d))
        c.drawCircle(hx, hy, 14, skia.Paint(Color4f=col(RG["skin"]), AntiAlias=True))
        if t > K: g = math.exp(-(t - K) * 3); bloom_spot(c, hx + 4, hy - 120, 60, "#FFFFFF", 0.8 * g); rays(c, hx + 4, hy - 120, 0, 60, 160, 8, "#FFFFFF", 0.3 * g, t)
        draw(c, BB, 1320, 930, 1.0)
    cam(c, 1.0 + 0.05 * t / d, 900, 620, world); post(c, cold=0.28)

ARM = SP(f'<g transform="translate(0,0)"><path d="M1920,180 Q1400,300 1040,560 L960,700 L1060,780 L1960,500 Z" fill="{RG["tunic"]}" stroke="#1A1410" stroke-width="10"/>'
         f'<circle cx="1110" cy="640" r="86" fill="none" stroke="#1A1410" stroke-width="40"/><circle cx="1110" cy="640" r="86" fill="none" stroke="#D9A93A" stroke-width="28"/>'
         f'<ellipse cx="985" cy="735" rx="58" ry="40" fill="{RG["skin"]}" stroke="#1A1410" stroke-width="8" transform="rotate(-35,985,735)"/></g>', W, H, 0, 0)
BBIG = SP(f'<g transform="translate(330,240)">{baby(0, 0, 4.4)}</g>', 760, 480, 330, 240)
KNF2 = SP(f'<g transform="translate(60,200)">{knife(0, 0, 2.2)}</g>', 140, 320, 60, 200)
def shot4(c, t, d):
    Y = CUE["yapam"]; touch = ease_out(lin(t, 0.2, 0.9)); fall = lin(t, Y, Y + 0.35)
    def world():
        for L_ in (FOG_FAR, MID, NEAR): draw(c, blurred(L_, 10), W / 2, H / 2)
        bloom_spot(c, 960, 500, 700, "#E8EEF2", 0.25)
        draw(c, BBIG, 820, 860, 1.0)
        draw(c, ARM, 0, 0)
        hx0, hy0, hx1, hy1 = 800, 700, 1010, 640   # bebeğin eli kola uzanır
        ex, ey = hx0 + (hx1 - hx0) * touch, hy0 + (hy1 - hy0) * touch
        p = skia.Path(); p.moveTo(hx0, hy0); p.quadTo((hx0 + ex) / 2, min(hy0, ey) - 30, ex, ey)
        c.drawPath(p, skia.Paint(Color4f=col("#1A1410"), StrokeWidth=38, Style=skia.Paint.kStroke_Style, StrokeCap=skia.Paint.kRound_Cap, AntiAlias=True))
        c.drawPath(p, skia.Paint(Color4f=col("#F2CDAA"), StrokeWidth=30, Style=skia.Paint.kStroke_Style, StrokeCap=skia.Paint.kRound_Cap, AntiAlias=True))
        c.drawCircle(ex, ey, 26, skia.Paint(Color4f=col("#1A1410"), AntiAlias=True)); c.drawCircle(ex, ey, 21, skia.Paint(Color4f=col("#F2CDAA"), AntiAlias=True))
        if touch > 0.95: bloom_spot(c, 1110, 640, 120, "#FFE6A0", 0.3)
        if t > Y:  # bıçak kadraj dışından düşer, taşa çarpar (bebekten uzak, sağ alt)
            kx, ky = 1640, -200 + 1180 * min(1, fall) ** 2
            draw(c, KNF2, kx, min(ky, 960), 1.0, rot=40 + 60 * fall if fall < 1 else 100)
        tq = lin(t, Y + 0.6, Y + 1.5)  # tek gözyaşı damlası
        if 0 < tq < 1: c.drawCircle(1300, -40 + 640 * tq * tq, 9, skia.Paint(Color4f=col("#DDF0FF", 0.9), AntiAlias=True))
    cam(c, 1.0, W / 2, H / 2, world); post(c, cold=0.22)

RGB5 = FIG(RG, "back", "neutral")
def shot5a(c, t, d):
    def world():
        river_env(c, t)
        q = ease_io(t / d); s = 0.62 - 0.3 * q
        draw(c, BB, 980, 980, 1.0)
        draw(c, RGB5, 640 - 200 * q, 960 - 140 * q, s, a=1 - 0.75 * q)
        fog(c, t, 860 - 140 * q, "#E0E6EC", 0.5 * q, seed=7, speed=18)
    cam(c, 1.0 + 0.1 * ease_io(t / d), 900, 600 - 60 * ease_io(t / d), world); post(c, cold=0.3)
ASLR = FIG(ASL, "front", "relief", pose="reach")
ASLK = FIG(ASL, "3q", "relief", facing=-1, hands=("grip", "grip"))
STONES = BG("".join(f'<ellipse cx="{430 + k*22}" cy="{500 + (k%3)*8}" rx="{18 + (k%4)*4}" ry="12" fill="{["#7A7268","#8A8278","#6A6258"][k%3]}" stroke="#3A342C" stroke-width="2"/>' for k in range(10)))
def shot5b(c, t, d):
    A = CUE["annesi"]; run = ease_in(lin(t, 0.0, A)); hold = t > A
    lightk = ease_io(lin(t, A - 0.1, A + 1.2))
    def world():
        river_env(c, t, fogk=1 - 0.6 * lightk)
        light_shaft(c, 1000, 140 + 200 * lightk, 1000, 260 + 360 * lightk, "#FFF2D8", 0.15 + 0.4 * lightk, t, y_top=-60, y_bot=1000)
        if not hold:
            draw(c, ASLR, 1700 - 640 * run, 980 - 10 * abs(math.sin(t * 9)), 0.7)
            draw(c, BB, 980, 980, 1.0)
        else:
            draw(c, ASLK, 1000, 1180, 0.8, rot=-6)
            draw(c, BB, 905, 905, 0.95, rot=14)
            draw(c, STONES, W / 2, H / 2)
        bloom_spot(c, 1000, 760, 260, "#FFF0D0", 0.35 * lightk)
    cam(c, 1.0 + 0.08 * ease_io(t / d), 1000, 600, world); post(c, warm=0.1 * lightk, cold=0.28 * (1 - lightk) + 0.1)

SHOTS = list(zip([shot1, shot2, shot3, shot4, shot5a, shot5b], CUE["d"]))
def render(preview=None):
    surf = skia.Surface(W, H); c = surf.getCanvas()
    if preview:
        for i, frac in preview:
            fn, d = SHOTS[i]; c.clear(skia.ColorBLACK); fn(c, frac * d, d)
            surf.makeImageSnapshot().save(f"{OUT}/p{i}_{int(frac*100)}.png", skia.kPNG)
        return
    wr = Writer(f"{OUT}/ivar.mp4"); dip = 6
    for si, (fn, d) in enumerate(SHOTS):
        n = int(round(d * FPS))
        for f in range(n):
            t = f / FPS; c.clear(skia.ColorBLACK); fn(c, t, d)
            if si > 0 and f < dip: fill(c, "#000", 1 - f / dip)
            if si < len(SHOTS) - 1 and f >= n - dip: fill(c, "#000", (f - (n - dip)) / dip)
            if si == len(SHOTS) - 1 and f >= n - 24: fill(c, "#000", (f - (n - 24)) / 24)
            wr.write(surf)
    wr.close()
if __name__ == "__main__":
    if sys.argv[1] == "prev": render([(0, 0.2), (0, 0.45), (0, 0.85), (1, 0.4), (1, 0.85), (2, 0.6), (3, 0.5), (3, 0.9), (4, 0.6), (5, 0.8)])
    else: render()
