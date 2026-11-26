"""Athelstan'ın ölümü (madde 12) animatiği v1."""
import sys, math, random, os, json
sys.path[:0] = ["/home/claude/r3", "/home/claude/r2", "/home/claude/r3/veda", "/home/claude/r3/floki"]
import skia
from engine import *
from fx import *
from art3 import figure, head3, EXP, shade, RAGNAR3
import puppet
exec(open('/home/claude/r3/floki/model_af.py').read().split("W_, H_ = 3000")[0].split("import subprocess")[1])
EXP["peace"] = (-6, 3, 0.92, 0.10, "soft_smile", "")
EXP["menace"] = (8, -6, 0.18, 0.04, "flat", "")
OUT = "/home/claude/r3/floki/out"; os.makedirs(OUT, exist_ok=True)
CUE = json.load(open("/home/claude/r3/floki/cues.json"))
def BG(svg): return sprite(f'<g transform="scale(2)">{svg}</g>', W, H)
def FIG(spec, view="front", expr="neutral", pose="stand", hands=("open", "open"), extra=""):
    g = figure(spec, view, "stand", expr, hands=hands) if pose == "stand" else figure(spec, "front", pose, expr, hands=hands)
    return sprite(f'<g transform="translate(400,1000)">{g}{extra}</g>', 800, 1100, ax=400, ay=1000)
def HEAD(spec, view, expr, s=1.0, flip=1):
    return sprite(f'<g transform="translate(400,400) scale({s*flip},{s})">{head3(spec, view, expr)}</g>', 800, 800, ax=400, ay=400)
def cam(c, z, cx, cy, fn):
    z = max(1.0, z); hw, hh = W / (2 * z), H / (2 * z)
    cx = min(max(cx, hw), W - hw); cy = min(max(cy, hh), H - hh)
    c.save(); c.translate(W / 2, H / 2); c.scale(z, z); c.translate(-cx, -cy); fn(); c.restore()
def post(c, warm=0.0, cold=0.2):
    if warm: grade(c, "#FFB060", warm, "screen")
    if cold: grade(c, "#7E96B0", cold, "multiply")
    vignette(c, 0.75); letterbox(c, 1.0, 70)
def candle(c, x, y, t, calm=1.0, lean=0.0, k=1.0):
    if k <= 0.02: return
    fl = (1 - calm) * (0.25 * math.sin(t * 23) + 0.15 * math.sin(t * 37)) + 0.04 * math.sin(t * 11)
    for cc, w, h in (("#F2A54A", 13, 50), ("#FFE9A8", 7, 30)):
        p = skia.Path(); hh = h * k * (1 + fl)
        p.moveTo(x - w, y); p.quadTo(x - w, y - hh * 0.5, x + lean * hh + 3 * fl * 10, y - hh); p.quadTo(x + w, y - hh * 0.5, x + w, y); p.close()
        c.drawPath(p, skia.Paint(Color4f=col(cc, 0.95), AntiAlias=True))
    glow(c, x, y - 30, 360, "#FFB050", 0.30 * k * (1 + fl * 0.5))

# ───── 1 · LİMAN, ŞAFAK
BG1 = BG('<defs><linearGradient id="d1" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7A8AA4"/><stop offset="0.62" stop-color="#E8C8A0"/></linearGradient></defs><rect width="960" height="540" fill="url(#d1)"/>'
         '<path d="M0,290 Q120,250 260,280 Q380,240 520,286 Q640,300 760,270 Q860,256 960,284 L960,330 L0,330 Z" fill="#5E6A78"/>'
         + "".join(f'<path d="M{x},300 l18,-16 l18,16 Z M{x+3},300 h30 v10 h-30 Z" fill="#4A4038"/><path d="M{x+18},280 q-6,-14 4,-28 q-8,-12 2,-24" stroke="#B8B0A8" stroke-width="3" fill="none" opacity="0.5"/>' for x in (690, 760, 830))
         + '<path d="M0,330 L960,330 L960,540 L0,540 Z" fill="#5A7088"/><path d="M40,330 L330,330 L330,345 L40,345 Z" fill="#5A4430" stroke="#1A1410" stroke-width="3"/>'
         + "".join(f'<rect x="{x}" y="345" width="8" height="60" fill="#4A3826"/>' for x in (60, 140, 220, 300))
         + '<path d="M110,352 L330,352 Q320,376 290,380 L150,380 Q120,376 110,352 Z" fill="#5A4028" stroke="#1A1410" stroke-width="3"/>'
         '<path d="M330,352 Q350,330 342,310 Q336,300 346,296 Q356,304 350,316" fill="none" stroke="#1A1410" stroke-width="5"/><path d="M110,352 Q96,336 102,322" fill="none" stroke="#1A1410" stroke-width="5"/>'
         '<path d="M220,352 L220,250" stroke="#3A2C20" stroke-width="5"/>' + "".join(f'<rect x="{186 + k*14}" y="262" width="14" height="66" fill="{["#B8322A","#E8E0D0"][k % 2]}" stroke="#1A1410" stroke-width="1.5"/>' for k in range(5))
         + "".join(f'<circle cx="{140 + k*30}" cy="356" r="9" fill="{["#8A3A2A","#C9A25A","#3A5A7A"][k%3]}" stroke="#1A1410" stroke-width="2"/>' for k in range(6)))
ATH_D = FIG(ATH, "front", "neutral"); ATH_U = FIG(ATH, "front", "awe", pose="arms_up")
WATER = sprite('<rect width="1920" height="600" fill="#5A7088"/>', 1920, 600, ax=0, ay=0)
SPK = Particles("dust", 40, seed=3, area=(1060, 100, 1360, 820), color="#FFF2C8", size=(2, 5), speed=25)
def shot1(c, t, d):
    L = CUE["isik"]; p = ease_out(lin(t, L - 0.2, L + 0.5))
    def world():
        draw(c, BG1, W / 2, H / 2)
        light_shaft(c, 1260, 120 + 80 * p, 1210, 140 + 260 * p, "#FFF2C8", 0.22 + 0.35 * p, t, y_top=-60, y_bot=840)
        bloom_spot(c, 1210, 520, 160 + 140 * p, "#FFF0C0", 0.15 + 0.35 * p)
        draw(c, ATH_U if t > L else ATH_D, 1210, 1010 + 6 * math.sin(t * 1.6), 0.62)
        c.drawRect(skia.Rect(-100, 820, W + 100, H + 100), skia.Paint(Color4f=col("#5A7088", 0.94)))
        for k in range(4):
            q = ((t * 0.5 + k / 4) % 1.0)
            c.drawOval(skia.Rect(1210 - 60 - 220 * q, 822 - 6 - 22 * q, 1210 + 60 + 220 * q, 822 + 6 + 22 * q), skia.Paint(Color4f=col("#DDE8F2", 0.6 * (1 - q)), Style=skia.Paint.kStroke_Style, StrokeWidth=3, AntiAlias=True))
        for k in range(14):
            rr = random.Random(k); x = (rr.uniform(0, W) + t * 40) % W; y = rr.uniform(840, 1060)
            c.drawLine(x, y, x + 50, y, skia.Paint(Color4f=col("#B8C8D8", 0.5), StrokeWidth=4, AntiAlias=True))
        SPK.draw(c, t, p)
    cam(c, 1.05, W / 2, 600 - 80 * ease_io(t / d), world)
    post(c, warm=0.08 * p, cold=0.0)

# ───── 2 · KULÜBE (diz çöküp dua)
def hut_svg():
    return ('<rect width="960" height="540" fill="#1E1812"/><rect y="400" width="960" height="140" fill="#2E241A"/>'
            + "".join(f'<rect x="{x}" y="40" width="44" height="360" fill="{["#2A2018", "#30251B"][i % 2]}"/>' for i, x in enumerate(range(0, 960, 44)))
            + '<g transform="translate(560,250)"><rect x="-10" y="-130" width="20" height="200" fill="#5A4430" stroke="#1A1410" stroke-width="4"/><rect x="-60" y="-90" width="120" height="18" fill="#5A4430" stroke="#1A1410" stroke-width="4"/></g>'
            + '<rect x="634" y="360" width="24" height="40" fill="#E8DCC0" stroke="#1A1410" stroke-width="3"/><rect x="600" y="398" width="90" height="10" fill="#4A3826"/>'
            + '<path d="M180,300 L330,300 L330,312 L180,312 Z" fill="#4A3826"/><ellipse cx="210" cy="294" rx="18" ry="7" fill="#6A5038" stroke="#1A1410" stroke-width="2"/>'
            + '<rect x="240" y="262" width="34" height="38" fill="#C8B890" stroke="#1A1410" stroke-width="2"/><path d="M246,272 h22 M246,280 h22 M246,288 h16" stroke="#6A5A40" stroke-width="2"/>'
            + '<path d="M40,400 Q60,372 170,374 Q220,378 230,400 Z" fill="#B8A070" stroke="#1A1410" stroke-width="3"/><path d="M70,396 Q120,370 200,384 L214,400 Z" fill="#6A5A70" stroke="#1A1410" stroke-width="3"/>'
            )
BG2 = BG(hut_svg())
KB = puppet.back_kneel_uc(dict(ATH, undercut=False, fur=False, cloak="#5A4E40"), pray=True, expr="peace", face=1)
DUST = Particles("dust", 30, seed=8, area=(1100, 400, 1500, 820), color="#FFD8A0", size=(1, 3), speed=12)
def shot2(c, t, d):
    Y = CUE["yalniz"]; calm = ease_io(lin(t, Y, Y + 0.6))
    def world():
        draw(c, BG2, W / 2, H / 2)
        candle(c, 1292, 722, t, calm=0.3 + 0.7 * calm)
        DUST.draw(c, t, 0.6)
        draw(c, KB, 940, 960, 0.78, sy=0.78 * (1 + 0.006 * math.sin(t * 1.8)))
    cam(c, 1.0 + 0.12 * ease_io(t / d), 1020, 600, world)
    post(c, warm=0.05)

# ───── 3 · KAPI, FLOKI
FLOs = FIG(FLO, "front", "menace", hands=("grip", "grip"), extra='<g transform="translate(-40,-180) rotate(-58)"><rect x="-7" y="-140" width="14" height="260" rx="4" fill="#6A5038" stroke="#1A1410" stroke-width="4"/><path d="M7,-138 Q66,-150 72,-86 Q44,-94 7,-80 Z" fill="#A8B0B8" stroke="#1A1410" stroke-width="4"/></g>')
DOOR = sprite('<rect x="0" y="0" width="80" height="560" fill="#3A2C20" stroke="#1A1410" stroke-width="8"/><path d="M10,120 L70,120 M10,420 L70,420" stroke="#2A2018" stroke-width="8"/>', 80, 560, ax=0, ay=0)
def shot3(c, t, d):
    K = CUE["kapi"]; op = ease_out(lin(t, K - 0.1, K + 0.7)); fa = ease_io(lin(t, K + 0.2, K + 1.0))
    def world():
        draw(c, BG2, W / 2, H / 2)
        dx0, dy0, dw, dh = 1500, 240, 300, 560
        c.drawRect(skia.Rect(dx0, dy0, dx0 + dw, dy0 + dh), skia.Paint(Color4f=col("#0E0C0A")))
        c.save(); c.clipRect(skia.Rect(dx0, dy0, dx0 + dw * op, dy0 + dh))
        c.drawRect(skia.Rect(dx0, dy0, dx0 + dw, dy0 + dh), skia.Paint(Color4f=col("#1C2A3E")))
        c.drawRect(skia.Rect(dx0, dy0, dx0 + dw, dy0 + 120), skia.Paint(Color4f=col("#2E4466")))
        c.drawCircle(dx0 + dw * 0.75, dy0 + 70, 26, skia.Paint(Color4f=col("#DDE6F0", 0.9), AntiAlias=True))
        rim(c, FLOs, dx0 + dw / 2, dy0 + dh + 10, 0.6, "#BFD2E8", -2, -1, 0.55 * fa)
        draw(c, FLOs, dx0 + dw / 2, dy0 + dh + 10, 0.6, rot=4, a=fa)
        c.restore()
        # açılan kapı kanadı (içe doğru, sol menteşe)
        pw = dw * (1 - op) + 40 * op
        dp = skia.Path(); dp.moveTo(dx0, dy0); dp.lineTo(dx0 + pw, dy0 + 30 * op); dp.lineTo(dx0 + pw, dy0 + dh + 30 * op); dp.lineTo(dx0, dy0 + dh); dp.close()
        c.drawPath(dp, skia.Paint(Color4f=col("#3A2C20"), AntiAlias=True)); c.drawPath(dp, skia.Paint(Color4f=col("#1A1410"), Style=skia.Paint.kStroke_Style, StrokeWidth=8, AntiAlias=True))
        # Floki'nin gölgesi zeminde Athelstan'a uzanır
        if fa > 0:
            gp = skia.Path(); fx = dx0 + dw / 2; gp.moveTo(fx - 40, dy0 + dh); gp.lineTo(fx + 40, dy0 + dh); gp.lineTo(760, 1080); gp.lineTo(560, 1080); gp.close()
            c.drawPath(gp, skia.Paint(Color4f=col("#05070A", 0.55 * fa), AntiAlias=True))
        p = skia.Path(); p.moveTo(dx0, dy0 + dh); p.lineTo(dx0 + dw * op, dy0 + dh); p.lineTo(dx0 + dw * op + 420 * op, 1080); p.lineTo(dx0 - 260 * op, 1080); p.close()
        c.drawPath(p, skia.Paint(Color4f=col("#8AA8C8", 0.28 * op), AntiAlias=True))
        candle(c, 1292, 722, t, calm=0.2, lean=0.9 * op, k=1 - 0.6 * op)
        draw(c, blurred(KB, 6), 520, 1160, 1.3)
    cam(c, 1.0, W / 2, H / 2, world)
    post(c, warm=0.03 * (1 - op), cold=0.15 + 0.2 * op)

# ───── 4 · YAKIN PLAN, GÜLÜMSEME, GÖLGE, FLAŞ
AH = HEAD(dict(ATH), "3q", "peace", 2.4)
NECK = sprite(f'<g transform="translate(400,0)"><rect x="-70" y="0" width="140" height="160" fill="{shade(ATH["skin"],0.85)}" stroke="#1A1410" stroke-width="7"/>'
              f'<path d="M-400,520 Q-380,180 -120,120 L120,120 Q380,180 400,520 Z" fill="{ATH["tunic"]}" stroke="#1A1410" stroke-width="8"/>'
              f'<path d="M-90,120 Q0,190 90,120" stroke="{shade(ATH["tunic"],0.75)}" stroke-width="12" fill="none"/>'
              f'<path d="M-60,110 Q0,250 60,110" stroke="#6A4A30" stroke-width="5" fill="none"/>'
              f'<g transform="translate(0,175) scale(2.4)"><rect x="-5" y="-6" width="10" height="34" fill="#4A3424" stroke="#1A1410" stroke-width="3"/><rect x="-14" y="2" width="28" height="9" fill="#4A3424" stroke="#1A1410" stroke-width="3"/><path d="M9,4 l4,3" stroke="#C8B89A" stroke-width="2"/></g></g>', 800, 520, ax=400, ay=0)
WALL = BG("".join(f'<rect x="{x}" y="0" width="60" height="540" fill="{["#2E2318","#33271B"][i % 2]}" stroke="#1E160F" stroke-width="2"/>' for i, x in enumerate(range(0, 960, 60))))
SHADOW = sprite('<g transform="translate(60,320)"><rect x="-10" y="-300" width="20" height="320" fill="#000"/><path d="M10,-300 Q120,-330 128,-190 Q70,-200 10,-170 Z" fill="#000"/></g>', 220, 360, ax=60, ay=320)
def shot4(c, t, d):
    G = CUE["gulumsuyor"]
    if t > G + 0.05:
        f = 1 - lin(t, G + 0.05, G + 0.35); fill(c, "#000", 1.0)
        if f > 0: fill(c, "#FFFFFF", f)
        return
    def world():
        draw(c, WALL, W / 2, H / 2)
        glow(c, 1500, 640, 800, "#FFB050", 0.28 + 0.03 * math.sin(t * 13))
        rise = ease_in(lin(t, 0.3, G)); jit = 6 * math.sin(t * 17)
        draw(c, SHADOW, 1440 + jit, 980 - 260 * rise, 1.4 + 0.5 * rise, rot=-70 + 80 * rise, a=0.55)
        draw(c, NECK, 860, 760, 1.0)
        draw(c, AH, 860, 540 + 4 * math.sin(t * 1.5), 1.0)
    cam(c, 1.0 + 0.05 * t / d, 900, 560, world)
    post(c, warm=0.06)

# ───── 5 · YERDE HAÇ, YAĞMUR BAŞLAR
CR = sprite(f'<g transform="translate(150,200) scale(5)">{CROSS_S.replace("translate(0,-400)", "translate(0,0)")}</g>', 300, 300, ax=150, ay=150)
FLOOR = BG('<rect width="960" height="540" fill="#2A2018"/>' + "".join(f'<rect x="0" y="{y}" width="960" height="44" fill="{["#30251B","#2A2018"][i % 2]}" stroke="#1E160F" stroke-width="2"/>' for i, y in enumerate(range(0, 540, 44)))
           + '<g transform="translate(640,330) rotate(80)"><rect x="-10" y="-30" width="20" height="56" fill="#E8DCC0" stroke="#1A1410" stroke-width="3"/></g><ellipse cx="600" cy="342" rx="40" ry="10" fill="#E8DCC0" opacity="0.5"/>')
MUD = BG('<rect width="960" height="540" fill="#3A2E22"/>' + "".join(f'<ellipse cx="{random.Random(k).uniform(0,960):.0f}" cy="{random.Random(k+50).uniform(0,540):.0f}" rx="{random.Random(k+9).uniform(20,70):.0f}" ry="8" fill="#5A4A3A" opacity="0.6"/>' for k in range(40)))
CRK = sprite(f'<g transform="translate(150,170) scale(5)"><path d="M-30,-60 Q-10,-30 0,-18" stroke="#6A4A30" stroke-width="3" fill="none"/><path d="M8,-30 Q20,-46 30,-58" stroke="#6A4A30" stroke-width="3" fill="none"/><g transform="translate(0,-18)"><rect x="-5" y="-6" width="10" height="34" fill="#4A3424" stroke="#1A1410" stroke-width="3"/><rect x="-14" y="2" width="28" height="9" fill="#4A3424" stroke="#1A1410" stroke-width="3"/><path d="M9,4 l4,3" stroke="#C8B89A" stroke-width="2"/></g></g>', 300, 340, ax=150, ay=150)
def shot5(c, t, d):
    K = CUE["kurtaramiyorsun"]; rv = ease_io(lin(t, 0.0, 1.4)); mx = ease_io(lin(t, K + 0.5, K + 1.4))
    fill(c, "#0A0807", 1.0)
    def world():
        draw(c, FLOOR, W / 2, H / 2, a=rv * (1 - mx))
        if mx > 0: draw(c, MUD, W / 2, H / 2, a=mx)
        for k in range(3):  # sönmüş mumdan tek duman şeridi
            q = ((t * 0.35 + k / 3) % 1.0)
            bloom_spot(c, 1180 + 30 * math.sin(q * 6 + k), 660 - 380 * q, 20 + 30 * q, "#8A8A8A", 0.25 * (1 - q) * rv * (1 - mx))
        draw(c, CRK, 960, 560, 1.0, rot=-12, a=rv)
        if mx > 0:
            for k in range(int(40 * mx)):
                rr = random.Random(k * 7); ph = (t * rr.uniform(0.8, 1.6) + rr.random()) % 1.0
                x, y = rr.uniform(200, 1720), rr.uniform(200, 900); r = 6 + 40 * ph
                c.drawOval(skia.Rect(x - r, y - r * 0.5, x + r, y + r * 0.5), skia.Paint(Color4f=col("#BFD8EC", 0.5 * (1 - ph) * mx), Style=skia.Paint.kStroke_Style, StrokeWidth=2, AntiAlias=True))
    sh = skia.GradientShader.MakeRadial(skia.Point(960, 560), 700, [col("#000000", 0), col("#000000", 0.85)])
    cam(c, 1.0 + 0.04 * t / d, 960, 560, world)
    c.drawRect(skia.Rect(0, 0, W, H), skia.Paint(Shader=sh))
    if mx > 0: Rain(300, seed=21, angle=6).draw(c, t, 0.6 * mx)
    post(c, warm=0.04 * (1 - mx), cold=0.25 * mx)

SHOTS = [(shot1, CUE["d"][0]), (shot2, CUE["d"][1]), (shot3, CUE["d"][2]), (shot4, CUE["d"][3]), (shot5, CUE["d"][4])]
def render(preview=None):
    surf = skia.Surface(W, H); c = surf.getCanvas()
    if preview:
        for i, frac in preview:
            fn, d = SHOTS[i]; c.clear(skia.ColorBLACK); fn(c, frac * d, d)
            surf.makeImageSnapshot().save(f"{OUT}/p{i}_{int(frac*100)}.png", skia.kPNG)
        return
    wr = Writer(f"{OUT}/olum.mp4"); dip = 6
    for si, (fn, d) in enumerate(SHOTS):
        n = int(round(d * FPS))
        for f in range(n):
            t = f / FPS; c.clear(skia.ColorBLACK); fn(c, t, d)
            if si > 0 and si != 4 and f < dip: fill(c, "#000", 1 - f / dip)
            if si < 3 and f >= n - dip: fill(c, "#000", (f - (n - dip)) / dip)
            wr.write(surf)
    wr.close()
if __name__ == "__main__":
    if sys.argv[1] == "prev": render([(0, 0.85), (1, 0.6), (2, 0.8), (3, 0.6), (4, 0.9)])
    else: render()
