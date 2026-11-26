"""Lagertha vedası animatiği v1."""
import sys, math, random, os
sys.path[:0] = ["/home/claude/r3", "/home/claude/r2", "/home/claude/r3/veda"]
import skia
from engine import *
from fx import *
import storyboard as SBm
from storyboard import LAG, ASL, BJ, RG, sky, longhouse, mud, cart, belly, INK_
from art3 import figure, head3, EXP, shade
import puppet  # grief_closed vb. ifadeleri kaydeder
OUT = "/home/claude/r3/veda/out"; os.makedirs(OUT, exist_ok=True)

def BG(svg): return sprite(f'<g transform="scale(2)">{svg}</g>', W, H, ss=1.0)
def FIG(spec, view="3q", expr="neutral", s=1.0, facing=1, pose="stand", hands=("open", "fist")):
    g = figure(spec, view, "stand", expr, facing=facing, hands=hands) if pose == "stand" else figure(spec, "front", pose, expr, facing=facing, hands=hands)
    return sprite(f'<g transform="translate(400,1000) scale({s})">{g}</g>', 800, 1100, ax=400, ay=1000, ss=1.0)
def HEAD(spec, view="3q", expr="neutral", s=1.0, flip=1, look=None):
    return sprite(f'<g transform="translate(400,400) scale({s*flip},{s})">{head3(spec, view, expr, look)}</g>', 800, 800, ax=400, ay=400, ss=1.0)
CART = sprite(f'<g transform="translate(300,420)">{cart(0, 0, 1.0)}</g>', 1000, 520, ax=300, ay=420, ss=1.0)

def cam(c, z, cx, cy, fn):
    z = max(1.0, z); hw, hh = W / (2 * z), H / (2 * z)
    cx = min(max(cx, hw), W - hw); cy = min(max(cy, hh), H - hh)
    c.save(); c.translate(W / 2, H / 2); c.scale(z, z); c.translate(-cx, -cy); fn(); c.restore()
def post(c, cold_a=0.3, lb=1.0):
    gradient_grade(c, "#2A4A6E", "#1A2A3A", 0.35, "soft"); grade(c, "#9EB6CC", cold_a * 0.5, "multiply")
    vignette(c, 0.7); letterbox(c, lb, 70)
def wheel_spokes(c, x, y, r, ang):
    p = skia.Paint(Color4f=col("#1A1410", 1), StrokeWidth=5, AntiAlias=True)
    for k in range(4):
        a = ang + k * math.pi / 4
        c.drawLine(x - r * math.cos(a), y - r * math.sin(a), x + r * math.cos(a), y + r * math.sin(a), p)
def dust(c, t, x, y, n=8, seed=1, a=0.5):
    for k in range(n):
        q = ((t * 1.4 + k / n) % 1.0)
        rr = random.Random(seed * 100 + k)
        bloom_spot(c, x - 90 * q + rr.uniform(-20, 20), y - 30 * q + rr.uniform(-6, 6), 18 + 40 * q, "#A8987E", a * (1 - q))

# ───────── ÇEKİM 1 · AVLU
def _hall():
    r = random.Random(12); o = []
    o.append('<rect width="960" height="540" fill="#2A1F17"/>')
    o.append("".join(f'<rect x="{x}" y="60" width="38" height="360" fill="{["#3A2C20", "#35281D", "#3E2F22"][i % 3]}" stroke="#241A12" stroke-width="2"/>' for i, x in enumerate(range(0, 960, 38))))
    # çatı kirişleri
    o.append('<path d="M0,70 L480,-60 L960,70 L960,0 L0,0 Z" fill="#1E1610"/>')
    o.append("".join(f'<path d="M{x},74 L480,-50" stroke="#2E2218" stroke-width="12"/>' for x in (-200, 80, 330, 630, 880, 1160)))
    o.append('<rect x="0" y="60" width="960" height="16" fill="#2E2218"/>')
    # duman deliğinden ışık
    o.append('<path d="M440,0 L520,0 L600,430 L360,430 Z" fill="#C8D6E2" opacity="0.10"/>')
    # duvar halısı + kalkanlar
    o.append('<rect x="250" y="100" width="160" height="190" fill="#6E2A22" stroke="#1A1410" stroke-width="4"/>'
             + "".join(f'<path d="M250,{y} L410,{y}" stroke="#C9A25A" stroke-width="5"/>' for y in (130, 260))
             + "".join(f'<path d="M{x},145 l14,24 l-14,24 l-14,-24 Z" fill="#C9A25A" opacity="0.8"/>' for x in (275, 305, 335, 365, 395)))
    for cx, c1, c2 in ((175, "#8E3B2E", "#D8C8A0"), (485, "#2F4C6E", "#D8C8A0"), (640, "#5A6A3A", "#C9A25A")):
        o.append(f'<g transform="translate({cx},170)"><circle r="44" fill="{c1}" stroke="#1A1410" stroke-width="5"/><path d="M0,-44 A44,44 0 0,1 0,44 Z" fill="{c2}" opacity="0.85"/><circle r="12" fill="#9AA2AA" stroke="#1A1410" stroke-width="4"/></g>')
    # duvarda gerili av postu
    o.append('<path d="M18,110 Q40,96 60,112 Q80,96 96,110 L92,150 Q104,190 90,236 L66,250 Q57,270 48,250 L24,236 Q10,190 22,150 Z" fill="#8A6A48" stroke="#1A1410" stroke-width="4"/>'
             '<path d="M40,140 Q57,190 76,140" stroke="#6A4E34" stroke-width="5" fill="none"/><path d="M18,110 L10,100 M96,110 L104,100" stroke="#3A2C20" stroke-width="4"/>')
    # çapraz mızraklar (sağ sütun yanı)
    o.append('<path d="M590,110 L640,330 M640,110 L590,330" stroke="#6A5038" stroke-width="7"/><path d="M584,96 L590,120 L596,96 Z M634,96 L640,120 L646,96 Z" fill="#AAB2BA" stroke="#1A1410" stroke-width="3"/>')
    # hizmetkâr silueti (arka sol)
    o.append('<g opacity="0.85"><circle cx="205" cy="300" r="15" fill="#1C1510"/><path d="M188,318 Q205,310 222,318 L230,400 L180,400 Z" fill="#1C1510"/><path d="M222,330 L240,346 L236,352" stroke="#1C1510" stroke-width="8" fill="none"/><path d="M236,340 l14,0 l-2,14 l-10,0 Z" fill="#7A6A50"/></g>')
    # sütunlar (oyma)
    for x in (110, 760):
        o.append(f'<rect x="{x}" y="40" width="54" height="420" fill="#4A3826" stroke="#1A1410" stroke-width="5"/>')
        o.append("".join(f'<path d="M{x+6},{y} q21,14 42,0 M{x+6},{y+10} q21,-14 42,0" stroke="#2E2218" stroke-width="4" fill="none"/>' for y in range(90, 440, 46)))
    # yüksek koltuk (taht)
    o.append('<path d="M250,300 L250,180 Q330,150 410,180 L410,300 Z" fill="#4E3A26" stroke="#1A1410" stroke-width="5"/>')
    for x, sgn in ((250, -1), (410, 1)):
        o.append(f'<rect x="{x-12}" y="160" width="24" height="250" fill="#5A4430" stroke="#1A1410" stroke-width="4"/>'
                 f'<path d="M{x},162 q{18*sgn},-34 {4*sgn},-50 q-{14*sgn},-10 -{20*sgn},6 q{12*sgn},4 {10*sgn},16" fill="#5A4430" stroke="#1A1410" stroke-width="4"/><circle cx="{x+4*sgn}" cy="122" r="3" fill="#C9A25A"/>')
    o.append('<path d="M262,300 Q330,280 398,300 L404,330 Q330,340 256,330 Z" fill="#C8BCA6" stroke="#1A1410" stroke-width="4"/>')
    o.append('<rect x="240" y="400" width="180" height="22" fill="#3A2C20" stroke="#1A1410" stroke-width="4"/>')
    # yan masa: boynuz kadehler + testi
    o.append('<rect x="430" y="350" width="70" height="10" fill="#5A4430" stroke="#1A1410" stroke-width="3"/><path d="M440,360 L438,400 M490,360 L492,400" stroke="#4A3826" stroke-width="6"/>'
             '<path d="M442,348 Q446,326 462,320 L464,326 Q452,332 450,348 Z" fill="#D8C8A0" stroke="#1A1410" stroke-width="2.5"/><path d="M462,348 Q468,330 482,326 L483,332 Q472,336 470,348 Z" fill="#D8C8A0" stroke="#1A1410" stroke-width="2.5"/>'
             '<path d="M484,348 Q480,334 488,328 L496,328 Q502,334 498,348 Z" fill="#8A5A3A" stroke="#1A1410" stroke-width="2.5"/>')
    # sıralar + kürkler
    o.append('<rect x="0" y="370" width="200" height="30" fill="#4A3826" stroke="#1A1410" stroke-width="4"/><path d="M40,370 Q80,350 130,370 L120,392 L46,392 Z" fill="#8A7A62" stroke="#1A1410" stroke-width="3"/>')
    o.append('<rect x="560" y="370" width="200" height="30" fill="#4A3826" stroke="#1A1410" stroke-width="4"/><path d="M600,370 Q650,352 700,370 L690,392 L610,392 Z" fill="#6A5A48" stroke="#1A1410" stroke-width="3"/>')
    # zemin + uzun ocak
    o.append('<rect x="0" y="420" width="960" height="120" fill="#4A3A2A"/>')
    o.append("".join(f'<path d="M{r.uniform(0,960):.0f},{r.uniform(430,540):.0f} l{r.uniform(10,26):.0f},{r.uniform(-3,3):.0f}" stroke="#6A5A40" stroke-width="2" opacity="0.6"/>' for _ in range(60)))
    o.append('<rect x="420" y="455" width="420" height="44" rx="8" fill="#2A1E16" stroke="#6A6058" stroke-width="7" stroke-dasharray="22 6"/>')
    # meşale tutucular
    for x in (137, 787): o.append(f'<path d="M{x-10},250 L{x+10},250 L{x+5},282 L{x-5},282 Z" fill="#2A2A2A" stroke="#1A1410" stroke-width="3"/>')
    return "".join(o)
BG1 = BG(_hall())
ASLs = sprite(f'<g transform="translate(400,1000) scale(0.72)">{figure(ASL, "front", "sit", "neutral", hands=("open", "open"))}'
              f'<path d="M-62,-250 Q-80,-320 0,-338 Q80,-320 62,-250 Z" fill="{shade(ASL["tunic"],1.06)}" stroke="#1A1410" stroke-width="5"/>'
              f'<path d="M-30,-316 Q0,-330 28,-316" stroke="{shade(ASL["tunic"],1.4)}" stroke-width="8" fill="none" stroke-linecap="round" opacity="0.8"/>'
              + "".join(f'<path d="M{sg*60},-470 Q{sg*120},-380 {sg*112},-170 L{sg*62},-170 Q{sg*74},-330 {sg*44},-450 Z" fill="{ASL["cloak"]}" stroke="#1A1410" stroke-width="5"/>' for sg in (-1, 1))
              + f'<ellipse cx="34" cy="-276" rx="22" ry="15" fill="#F1CCA6" stroke="#1A1410" stroke-width="4"/><path d="M60,-300 Q66,-284 52,-272" stroke="{ASL["cloak"]}" stroke-width="22" fill="none" stroke-linecap="round"/>' + '</g>', 800, 1100, ax=400, ay=1000)
LAGP = {e: sprite(f'<g transform="translate(400,420) scale(-4,4)">{head3(LAG, "side", e)}</g><path d="M80,1100 Q200,840 600,880 L800,1100 Z" fill="{LAG["tunic"]}" stroke="{INK_}" stroke-width="10"/>', 800, 1100, ax=400, ay=420) for e in ("neutral", "cold")}
D1 = Particles("dust", 40, seed=4, color="#C8BCA6", size=(2, 5), speed=30)
def shot1(c, t, d, rack=3.42):
    p = ease_io(lin(t, rack - 0.15, rack + 0.45))
    def world():
        sb = int(round(7 * p))
        bgsp = blurred(BG1, sb) if sb else BG1
        draw(c, bgsp, W / 2, H / 2)
        for tx in (274, 1574):
            glow(c, tx, 520, 170, "#FF9A40", 0.35); flame(c, tx, 510, 0.32, t + tx)
        glow(c, 1260, 950, 380, "#FF8A30", 0.25 + 0.04 * math.sin(t * 7))
        asp = blurred(ASLs, sb) if sb else ASLs
        draw(c, asp, 660, 830, 1.0, sy=1 + 0.006 * math.sin(t * 2.2))
        fog(c, t, 300, "#8A8070", 0.12, seed=5)
        fb = int(round(10 * (1 - p)))
        lp = LAGP["cold" if p > 0.5 else "neutral"]
        draw(c, blurred(lp, fb) if fb else lp, 1520, 600, 1.0, rot=-2 * p)
    cam(c, 1.0 + 0.03 * t / d, W / 2, H / 2, world)
    D1.draw(c, t, 0.6); post(c)

# ───────── ÇEKİM 2 · EV İÇİ
BG2 = BG('<rect width="960" height="540" fill="#2E241C"/><rect x="0" y="380" width="960" height="160" fill="#3E3024"/>'
         '<path d="M0,0 L960,0 L960,90 L0,140 Z" fill="#241C16"/>' + "".join(f'<rect x="{x}" y="90" width="14" height="300" fill="#3A2C20"/>' for x in (120, 520, 760))
         + f'<rect x="200" y="330" width="150" height="90" fill="#6E5034" stroke="{INK_}" stroke-width="5"/><rect x="545" y="100" width="180" height="290" fill="none" stroke="#3A2C20" stroke-width="16"/>'
         + '<ellipse cx="420" cy="400" rx="80" ry="22" fill="#5A4636" stroke="#1A1410" stroke-width="4"/>')
LID = sprite(f'<g transform="translate(90,40)"><path d="M0,0 L150,0 L140,-30 L10,-30 Z" fill="#5A4028" stroke="{INK_}" stroke-width="4"/></g>', 260, 60, ax=90, ay=40)
LAG2 = FIG(LAG, "3q", "cold", 0.8, facing=-1, hands=("grip", "grip"))
RGB = FIG(RG, "back", "neutral", 1.5)
CLOTH = sprite(f'<rect x="10" y="10" width="80" height="34" rx="8" fill="#B8A88A" stroke="{INK_}" stroke-width="4"/><path d="M20,24 L80,24" stroke="#8A7A5E" stroke-width="3"/>', 100, 54)
EMB = Particles("ember", 30, seed=7, area=(760, 520, 920, 800), color="#FFC070", size=(2, 4), speed=60)
def flame(c, x, y, k, t):
    if k <= 0.01: return
    for i, (cc, w, h) in enumerate((("#F2A54A", 100, 260), ("#FFD27A", 66, 190), ("#FFF2C0", 30, 110))):
        fl = 1 + 0.12 * math.sin(t * 17 + i * 2) + 0.08 * math.sin(t * 29 + i)
        p = skia.Path(); hh = h * k * fl; ww = w * (0.6 + 0.4 * k)
        p.moveTo(x - ww, y); p.quadTo(x - ww * 0.6, y - hh * 0.6, x + 8 * math.sin(t * 9 + i), y - hh); p.quadTo(x + ww * 0.6, y - hh * 0.6, x + ww, y); p.close()
        c.drawPath(p, skia.Paint(Color4f=col(cc, 0.95), AntiAlias=True))
def shot2(c, t, d, out=4.0):
    k = 1 - ease_in(lin(t, out, out + 0.45)); close = ease_io(lin(t, out, out + 0.7))
    def world():
        draw(c, BG2, W / 2, H / 2)
        # kapıdan gelen ışık (daralır)
        dw = 340 * (1 - 0.82 * close)
        c.drawRect(skia.Rect(1100 + (340 - dw) / 2, 210, 1100 + (340 - dw) / 2 + dw, 770), skia.Paint(Color4f=col("#9AB0C4", 0.55)))
        light_shaft(c, 1270, dw, 1180, dw * 1.8, "#BFD2E2", 0.22 * (1 - close * 0.7), t, y_top=210, y_bot=1080)
        glow(c, 840, 760, 520, "#FF9A40", 0.45 * k)
        flame(c, 840, 800, k, t)
        if t > out:  # duman
            for j in range(4):
                q = lin(t, out + 0.2 + j * 0.2, out + 1.6 + j * 0.2)
                if 0 < q < 1: bloom_spot(c, 840 + 30 * math.sin(j + q * 3), 780 - 260 * q, 40 + 60 * q, "#6A6A6A", 0.4 * (1 - q))
        # Lagertha + bez sandığa
        bend = 3 * math.sin(lin(t, 0.6, 1.8) * math.pi)
        draw(c, LAG2, 600, 890, 1.0, rot=-bend)
        if t < 1.9:
            q = ease_io(lin(t, 0.7, 1.7)); draw(c, CLOTH, 520 - 60 * q, 660 + 20 * q - 60 * math.sin(q * math.pi), 1.0)
        lid = ease_out(lin(t, out + 0.1, out + 0.4))
        draw(c, LID, 400, 660 + 0 * lid, 1.0, sy=max(0.05, lid))
        EMB.draw(c, t, k)
        draw(c, RGB, 1660, 1300, 1.0, sy=1 + 0.006 * math.sin(t * 2.0))
    cam(c, 1.0 + 0.04 * t / d, W / 2, H / 2, world)
    grade(c, "#FFB070", 0.10 * k, "screen"); post(c, 0.25 + 0.25 * (1 - k))

# ───────── ÇEKİM 3 · YOL
ROAD = BG(sky("#7A8A98", "#C2CCD4") + '<path d="M0,330 Q300,300 960,320 L960,540 L0,540 Z" fill="#4E5E4C"/>' + "".join(f'<path d="M{x},{322 - 6*math.sin(x/90)} l-10,-34 l20,0 Z" fill="#3E4E40"/>' for x in range(0, 960, 37)) + mud(400))
RIDER = sprite(f'<g transform="translate(100,200)"><path d="M-50,140 Q-44,40 0,26 Q44,40 50,140 Z" fill="{LAG["cloak"]}" stroke="{INK_}" stroke-width="5"/><g transform="translate(0,0) scale(0.64)">{head3(LAG, "back", "neutral")}</g></g>', 200, 360, ax=100, ay=340)
RG3 = FIG(RG, "3q", "grief", 1.0); BJ3 = FIG(BJ, "3q", "grief", 0.64); BJ3b = FIG(BJ, "3q", "determined", 0.64)
def cart_draw(c, x, y, s, t, rider=True, lean=0):
    bob = 3 * abs(math.sin(t * 6))
    if rider: draw(c, RIDER, x - 60 * s, y - 150 * s - bob, s)
    draw(c, CART, x, y - bob * 0.5, s, rot=lean)
    for wx in (-70, 70): wheel_spokes(c, x + wx * s, y - 10 * s - bob * 0.5, 38 * s, t * 5)
def shot3a(c, t, d):
    def world():
        draw(c, ROAD, W / 2, H / 2)
        q = t / d; cx = 1250 + 330 * q; s = 1.05 - 0.2 * q
        dust(c, t, cx - 120 * s, 860, seed=3, a=0.35)
        cart_draw(c, cx, 870, s, t)
        draw(c, RG3, 340, 1000, 1.0, sy=1 + 0.005 * math.sin(t * 2))
        step = 26 * ease_io(lin(t, d - 0.8, d))
        draw(c, BJ3b if t > d - 0.8 else BJ3, 510 + step, 1000, 1.0)
    cam(c, 1.0, W / 2, H / 2, world); post(c)
BJR = FIG(BJ, "front", "determined", 1.0, pose="reach")
def shot3b(c, t, d, grip=2.56):
    def world():
        off = (t * 420) % 1920
        draw(c, ROAD, W / 2 - off, H / 2); draw(c, ROAD, W / 2 - off + 1920, H / 2)
        lx, ly = 860, 600
        c.drawPath(_torso(lx, ly), skia.Paint(Color4f=col("#1A1410"), AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=10))
        c.drawPath(_torso(lx, ly), skia.Paint(Color4f=col(LAG["tunic"]), AntiAlias=True))
        draw(c, LAGH, lx, ly - 150, 1.0)
        cart_draw(c, 1100, 960, 1.8, t, rider=False)
        # koşan Bjorn
        appr = ease_io(lin(t, 0, grip)); bx = 260 + 250 * appr; run = abs(math.sin(t * 2 * math.pi * 1.6))
        lift = ease_io(lin(t, grip + 0.5, d)); by = 1010 - 24 * run * (1 - lift) - 120 * lift
        dust(c, t, bx - 20, 1000, n=6, seed=8, a=0.4 * (1 - lift))
        BS = 0.82
        draw(c, BJR, bx + 140 * lift, by, BS, rot=6 * (1 - lift))
        wx, wy = bx + 140 * lift + BS * 210, by - BS * 360
        # kol: omuzdan bileğe uzanır
        reach = ease_out(lin(t, grip - 0.45, grip))
        sx_, sy_ = lx - 40, ly + 30
        ex, ey = sx_ + (wx - sx_) * reach, sy_ + (wy - sy_) * reach
        pa = skia.Path(); pa.moveTo(sx_, sy_); pa.quadTo((sx_ + ex) / 2, max(sy_, ey) + 40, ex, ey)
        c.drawPath(pa, skia.Paint(Color4f=col("#1A1410"), StrokeWidth=50, Style=skia.Paint.kStroke_Style, StrokeCap=skia.Paint.kRound_Cap, AntiAlias=True))
        c.drawPath(pa, skia.Paint(Color4f=col(LAG["tunic"]), StrokeWidth=40, Style=skia.Paint.kStroke_Style, StrokeCap=skia.Paint.kRound_Cap, AntiAlias=True))
        c.drawCircle(ex, ey, 24, skia.Paint(Color4f=col("#1A1410"), AntiAlias=True)); c.drawCircle(ex, ey, 19, skia.Paint(Color4f=col(LAG["skin"]), AntiAlias=True))
        if t > grip:
            g = math.exp(-(t - grip) * 3); bloom_spot(c, ex, ey, 90, "#FFE08A", 0.7 * g)
            rays(c, ex, ey, 0, 140, 360, 10, "#FFE8A8", 0.25 * g, t)
    cam(c, 1.0, W / 2, H / 2, world); post(c)
def _torso(x, y):
    p = skia.Path(); p.moveTo(x - 110, y + 260); p.quadTo(x - 110, y - 20, x, y - 40); p.quadTo(x + 110, y - 20, x + 110, y + 260); p.close(); return p
LAGH = HEAD(LAG, "3q", "tender", 1.15, flip=-1)

# ───────── ÇEKİM 4 · BAŞ ÖPME
BG4 = BG(sky("#6A7A8A", "#9AAAB8") + '<rect y="380" width="960" height="160" fill="#4A5646"/>')
BJH = HEAD(BJ, "3q", "grief", 2.3, flip=1, look=0.2)
RGH = {e: HEAD(RG, "side", e, 2.6, flip=-1) for e in ("grief", "grief_closed")}
BJT = sprite(f'<path d="M0,500 Q80,300 330,300 Q520,320 600,500 Z" fill="{BJ["tunic"]}" stroke="{INK_}" stroke-width="8"/>', 600, 500, ax=300, ay=500)
W4 = Particles("dust", 30, seed=11, color="#D8DEE4", size=(2, 4), speed=50)
def shot4(c, t, d, kiss=3.84):
    z = 1.0 + 0.09 * ease_io(t / d)
    def world():
        draw(c, blurred(BG4, 8), W / 2, H / 2)
        k = ease_io(lin(t, kiss - 0.9, kiss))
        rg = RGH["grief_closed" if t > kiss - 0.05 else "grief"]
        rx, ry = 1040 - 124 * k, 330 + 73 * k
        rim(c, rg, rx, ry, 1.0, "#FFD9A8", 6, -4, 0.6)
        draw(c, rg, rx, ry, 1.0, rot=8 * k)
        draw(c, BJT, 720, 1100, 1.0)
        draw(c, BJH, 720, 800, 1.0, rot=-6 * k)
    cam(c, z, 900, 600, world)
    W4.draw(c, t, 0.5); post(c)

# ───────── ÇEKİM 5 · YOL AYRIMI
r5 = random.Random(5)
TREES = "".join(f'<path d="M{x:.0f},{y:.0f} l-9,-26 l18,0 Z" fill="#2E3E32"/>' for x, y in [(r5.uniform(0, 960), r5.uniform(60, 540)) for _ in range(160)]
                if not (abs(x - (470 - (330 - y) * 0.45)) < 60 and y < 330) and not (abs(x - (520 + (300 - y) * 0.95)) < 60 and y < 330) and not (420 < x < 600 and y > 300))
BG5 = BG('<rect width="960" height="540" fill="#4E5E4C"/><path d="M430,540 L470,330 L330,48 L400,48 L520,300 L760,48 L840,48 L560,330 L560,540 Z" fill="#6A5A46" stroke="#1A1410" stroke-width="4"/>' + TREES)
RG5 = FIG(RG, "back", "neutral", 0.36)
CART5 = sprite(f'<g transform="translate(200,200) scale(-0.42,0.42)">{cart(0, 0, 1.0)}</g>{""}', 400, 300, ax=200, ay=200)
def shot5(c, t, d, gone=0.82, split=3.38):
    z = 1.35 - 0.35 * ease_io(t / d)
    def world():
        draw(c, BG5, W / 2, H / 2)
        q = ease_in(lin(t, 0, gone + 0.6)); x0, y0, x1, y1 = 860, 520, 600, -80
        if q < 1: draw(c, CART5, x0 + (x1 - x0) * q, y0 + (y1 - y0) * q, 1.0, rot=-25)
        draw(c, RG5, 1010, 960, 1.0, sy=1 + 0.006 * math.sin(t * 2))
        # sis yukarıda; "ayrılıyor"da açılır, iki yol görünür
        fa = 1 - ease_io(lin(t, split - 0.2, split + 1.0))
        sh = skia.GradientShader.MakeLinear([skia.Point(0, 300), skia.Point(0, 640)], [col("#C8D2DA", 0.6 * fa), col("#C8D2DA", 0.0)])
        c.drawRect(skia.Rect(-200, 300, W + 200, 640), skia.Paint(Shader=sh)); c.drawRect(skia.Rect(-200, -200, W + 200, 300), skia.Paint(Color4f=col("#C8D2DA", 0.6 * fa)))
    cam(c, z, 1010, 820 - 260 * ease_io(t / d), world)
    post(c, 0.32)

SHOTS = [(shot1, 5.0), (shot2, 5.8), (shot3a, 3.0), (shot3b, 4.2), (shot4, 6.0), (shot5, 5.8)]
def render(preview=None):
    surf = skia.Surface(W, H); c = surf.getCanvas()
    if preview:
        for i, frac in preview:
            fn, d = SHOTS[i]; c.clear(skia.ColorBLACK); fn(c, frac * d, d)
            surf.makeImageSnapshot().save(f"{OUT}/p{i}_{int(frac*100)}.png", skia.kPNG)
        return
    wr = Writer(f"{OUT}/veda.mp4"); dip = 6
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
    if sys.argv[1] == "prev": render([(0, 0.3), (0, 0.9)])
    else: render()
