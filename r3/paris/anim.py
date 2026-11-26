"""Paris'te sahte ölüm (madde 16) animatiği v1."""
import sys, math, random, os, json
sys.path[:0] = ["/home/claude/r3", "/home/claude/r2", "/home/claude/r3/paris"]
import skia
from engine import *
from fx import *
from models import *
import importlib.util as _u
_s = _u.spec_from_file_location('vsb', '/home/claude/r3/veda/storyboard.py'); _m = _u.module_from_spec(_s); _s.loader.exec_module(_m); LAG = _m.LAG
exec(open('/home/claude/r3/floki/model_af.py').read().split("W_, H_ = 3000")[0].split("import subprocess")[1])
FLO = dict(FLO, smooth=True, beard_w=0.8)
OUT = "/home/claude/r3/paris/out"; os.makedirs(OUT, exist_ok=True)
CUE = json.load(open("/home/claude/r3/paris/cues.json"))
EXP["dead_smirk"] = (0, 0, 1.0, 0.0, "smirk", "")
EXP["peek"] = (4, -2, 0.12, 0.0, "flat", "")
def BG(svg): return sprite(f'<g transform="scale(2)">{svg}</g>', W, H)
def FIG(spec, view="front", expr="neutral", extra="", facing=1):
    return sprite(f'<g transform="translate(400,1000) scale({facing},1)">{figure(spec, view, "stand", expr)}{extra}</g>', 800, 1100, ax=400, ay=1000)
def HEAD(spec, view, expr, s=1.0, flip=1, extra=""):
    return sprite(f'<g transform="translate(400,400) scale({s*flip},{s})">{head3(spec, view, expr)}{extra}</g>', 800, 800, ax=400, ay=400)
def cam(c, z, cx, cy, fn, shake=0):
    z = max(1.0, z); hw, hh = W / (2 * z), H / (2 * z)
    cx = min(max(cx, hw), W - hw) + shake * math.sin(c.__hash__() % 7 + cx); cy = min(max(cy, hh), H - hh)
    c.save(); c.translate(W / 2, H / 2); c.scale(z, z); c.translate(-cx, -cy); fn(); c.restore()
def post(c, warm=0.06, cold=0.08):
    if warm: grade(c, "#FFB060", warm, "screen")
    if cold: grade(c, "#9EB6CC", cold, "multiply")
    vignette(c, 0.7); letterbox(c, 1.0, 70)
def wall_svg():
    return ('<rect width="960" height="540" fill="#9AA6B0"/><path d="M0,150 L960,120 L960,540 L0,540 Z" fill="#8A8478"/>'
            + "".join(f'<rect x="{x}" y="{110 - 30*(x % 3 == 0)}" width="46" height="40" fill="#8A8478" stroke="#5A564E" stroke-width="3"/>' for x in range(0, 960, 70))
            + "".join(f'<path d="M{x + (y // 40 % 2) * 30},{y} h60" stroke="#6A665E" stroke-width="2"/>' for x in range(0, 960, 60) for y in range(170, 420, 40)))
COFFIN = sprite('<g transform="translate(220,70)"><path d="M-190,-40 L190,-50 L210,0 L190,40 L-190,30 L-210,0 Z" fill="#4A3424" stroke="#1A1410" stroke-width="6"/>'
                '<path d="M-160,-10 q20,-12 40,0 q20,12 40,0 q20,-12 40,0 q20,12 40,0 q20,-12 40,0 q20,12 40,0 q20,-12 40,0" stroke="#7A5A3A" stroke-width="5" fill="none"/></g>', 440, 140, ax=220, ay=70)
LID = sprite('<g transform="translate(220,30)"><path d="M-200,-14 L200,-22 L210,8 L-200,14 Z" fill="#5A4030" stroke="#1A1410" stroke-width="6"/></g>', 440, 60, ax=220, ay=30)
DUST = Particles("dust", 50, seed=3, color="#E8D8B8", size=(2, 5), speed=20)

# 1 · KAMP
BG1 = BG(wall_svg() + '<path d="M0,430 L960,430 L960,540 L0,540 Z" fill="#6A6A4A"/>'
         + '<path d="M80,430 L210,250 L340,430 Z" fill="#C8B898" stroke="#1A1410" stroke-width="5"/><path d="M210,250 L210,430" stroke="#8A7A5A" stroke-width="4"/><path d="M200,430 L210,380 L220,430 Z" fill="#2A2018"/>'
         + '<path d="M70,438 L80,430 M350,438 L340,430" stroke="#5A4430" stroke-width="5"/><path d="M60,446 L84,426 M356,446 L334,426" stroke="#4A3424" stroke-width="4"/>')
RLY = {e: sprite(f'<g transform="translate(560,180) rotate(-90) scale(0.62)">{figure(RAG3D, "front", "stand", e)}</g>', 1120, 360, ax=560, ay=180) for e in ("fakedead", "dead_smirk")}
PRIEST = FIG(BISH, "front", "neutral", extra=ROBE_B)
def smoke(c, x, y, t, k=1.0):
    for j in range(4):
        q = ((t * 0.18 + j / 4) % 1.0); bloom_spot(c, x + 40 * math.sin(q * 4 + j), y - 420 * q, 40 + 80 * q, "#8A8A88", 0.22 * (1 - q) * k)
def shot1(c, t, d):
    O = CUE["olmeye"]
    def world():
        draw(c, BG1, W / 2, H / 2); smoke(c, 1500, 820, t); smoke(c, 1720, 840, t + 1.3)
        draw(c, RLY["dead_smirk" if O < t < O + 1.4 else "fakedead"], 900, 900, 1.0)
        tilt = ease_io(lin(t, O - 1.0, O - 0.3)) * (1 - ease_io(lin(t, O + 0.6, O + 1.2)))
        draw(c, PRIEST, 1300, 1010, 0.62)
        # testiden su (kelimede başına değer)
        bx, by = 1180, 640
        c.drawPath(_jug(bx, by, -40 * tilt), skia.Paint(Color4f=col("#8A6A4A"), AntiAlias=True))
        if tilt > 0.6:
            for k in range(14):
                q = ((t * 2.2 + k / 14) % 1.0); x = bx - 40 - 120 * q; y = by + 10 + 230 * q * q
                c.drawCircle(x, y, 5, skia.Paint(Color4f=col("#BFE0F6", 0.85), AntiAlias=True))
            bloom_spot(c, 1030, 880, 60, "#DDF0FF", 0.4)
    cam(c, 1.0 + 0.06 * t / d, 1000, 640, world); post(c)
def _jug(x, y, rot):
    p = skia.Path(); p.addOval(skia.Rect(x - 28, y - 36, x + 28, y + 36)); m = skia.Matrix(); m.setRotate(rot, x, y); p.transform(m); return p

# 2 · TABUTTAN BAKIŞ
LAGH = HEAD(LAG, "front", "cold", 3.0); FLOH = {e: HEAD(FLO, "front", e, 3.0) for e in ("smug", "laugh")}
RIN = {e: HEAD(RAG3D, "front", e, 3.2) for e in ("fakedead", "peek")}
def shot2(c, t, d):
    D_ = CUE["duyuyor"]
    if D_ < t < D_ + 0.8:  # tabutun içi: tek ışık şeridi, göz aralanır
        fill(c, "#050403", 1.0)
        c.save(); c.clipRect(skia.Rect(0, 440, W, 650))
        draw(c, RIN["peek" if t > D_ + 0.25 else "fakedead"], 960, 560, 1.0)
        c.restore(); fill(c, "#000", 0.25); letterbox(c, 1.0, 70); return
    def world():
        c.drawRect(skia.Rect(0, 0, W, H), skia.Paint(Color4f=col("#7A8A9A")))
        if t < 1.6:
            k = ease_io(lin(t, 0.2, 0.8)) * (1 - ease_io(lin(t, 1.2, 1.6)))
            draw(c, LAGH, 960, 1500 - 860 * k, 1.0)
        else:
            k = ease_io(lin(t, 1.6, 2.2)) * (1 - ease_io(lin(t, D_ - 0.2, D_)))
            talk = int(t * 6) % 2 == 0
            draw(c, FLOH["laugh" if talk and t > 2.4 else "smug"], 960, 1520 - 900 * k, 1.0, rot=6 * math.sin(t * 2))
        # tabut çerçevesi (kapak aralığı)
        p = skia.Path(); p.moveTo(0, 0); p.lineTo(W, 0); p.lineTo(W, H); p.lineTo(0, H); p.close()
        q = skia.Path(); q.moveTo(400, 96); q.lineTo(1520, 96); q.lineTo(1400, 984); q.lineTo(520, 984); q.close()
        c.drawPath(skia.Op(p, q, skia.PathOp.kDifference_PathOp), skia.Paint(Color4f=col("#22180F")))
        for k_ in range(6): c.drawLine(0, 100 + k_ * 160, 400, 120 + k_ * 160, skia.Paint(Color4f=col("#3A2A1A"), StrokeWidth=4))
    cam(c, 1.0, W / 2, H / 2, world); post(c, warm=0.0, cold=0.1)

# 3 · ŞEHİR KAPISI
BG3 = BG(wall_svg() + '<rect x="320" y="150" width="320" height="300" fill="#2A2018" stroke="#1A1410" stroke-width="7"/><path d="M320,150 Q480,90 640,150" fill="#8A8478" stroke="#5A564E" stroke-width="5"/><path d="M0,440 L960,440 L960,540 L0,540 Z" fill="#7A7060"/>')
FR = [FIG(dict(FRANK, beard_len=bl, hair=hc, beard_c=hc), extra=MAIL + HELM + SPEAR) for bl, hc in ((0.35, "#5A4A3A"), (0.2, "#3A2E22"), (0.5, "#7A5A3A"))]
FRt = FIG(FRANK, "3q", "cold", extra=MAIL + HELM + SPEAR, facing=1)
CAR = [FIG(CARRY, "3q", "cold"), FIG(CARRY2, "3q", "cold")]
def shot3(c, t, d):
    S_ = CUE["silah"]; walk = t / d
    def world():
        draw(c, BG3, W / 2, H / 2)
        for k, x in enumerate((180, 330, 1590, 1740)):
            sp = FRt if (k == 2 and t > S_ + 0.15) else FR[k % 3]
            draw(c, sp, x, 1000, 0.5)
        bx = 760 + 360 * walk
        for row, dy, sc in ((0, -46, 0.46), (1, 0, 0.54)):
            for j in range(3):
                bob = 6 * abs(math.sin(t * 3.2 + j + row))
                draw(c, CAR[(j + row) % 2], bx - 150 + j * 150 + (75 if row == 0 else 0), 1010 + dy - bob, sc)
            if row == 0:
                hop = 26 * math.exp(-(t - S_) * 8) * abs(math.sin((t - S_) * 30)) if t > S_ else 0
                draw(c, COFFIN, bx + 20, 640, 1.0)
                draw(c, LID, bx + 20, 590 - hop, 1.0)
    cam(c, 1.05, 960, 520, world); post(c)

# 4 · KİLİSE: KALKIŞ + REHİNE
BG4 = BG('<rect width="960" height="540" fill="#3A3028"/>' + "".join(f'<rect x="{x}" y="40" width="60" height="420" fill="#4A4036" stroke="#2A2018" stroke-width="3"/><path d="M{x},40 Q{x+30},0 {x+60},40" fill="#4A4036"/>' for x in (40, 180, 720, 860))
         + '<rect x="400" y="300" width="160" height="70" fill="#6A5040" stroke="#1A1410" stroke-width="4"/><rect x="474" y="190" width="12" height="110" fill="#C9A25A"/><rect x="450" y="220" width="60" height="12" fill="#C9A25A"/>'
         + "".join(f'<rect x="{x}" y="280" width="8" height="20" fill="#E8DCC0"/>' for x in (414, 430, 520, 536))
         + "".join(f'<g opacity="0.55"><circle cx="{x}" cy="300" r="14" fill="#1A1410"/><path d="M{x-20},318 L{x+20},318 L{x+24},400 L{x-24},400 Z" fill="#1A1410"/></g>' for x in (150, 260, 700, 810))
         + '<path d="M0,420 L960,420 L960,540 L0,540 Z" fill="#4A4036"/>')
BISHf = FIG(BISH, "front", "neutral", extra=ROBE_B + MITRE + CROZIER); BISHs = FIG(BISH, "front", "awe", extra=ROBE_B + MITRE)
RUP = FIG(RAG3, "3q", "sly", facing=-1)
BSH = HEAD(BISH, "3q", "awe", 3.2, extra=f'<g transform="scale(0.98)">{MITRE.replace("translate(0,-630)", "translate(0,-70)")}</g>')
SWORD = sprite('<g transform="translate(30,330)"><rect x="-8" y="-320" width="16" height="320" fill="#AAB2BA" stroke="#1A1410" stroke-width="4"/><rect x="-34" y="0" width="68" height="12" fill="#5A4430" stroke="#1A1410" stroke-width="3"/><rect x="-8" y="12" width="16" height="50" fill="#4A3424"/></g>', 70, 420, ax=30, ay=330)
def shot4(c, t, d):
    K = CUE["kalk"]; P_ = CUE["program"]
    if P_ < t < P_ + 0.9:  # piskoposun donmuş şok yüzü
        def w2():
            draw(c, blurred(BG4, 10), W / 2, H / 2); draw(c, BSH, 960, 600, 1.0)
        cam(c, 1.0 + 0.04 * (t - P_), W / 2, H / 2, w2); post(c); return
    rise = ease_out(lin(t, K, K + 0.35)); host = ease_io(lin(t, K + 0.7, K + 1.3))
    shake = 10 * math.exp(-(t - K) * 5) if t > K else 0
    def world():
        draw(c, BG4, W / 2, H / 2)
        light_shaft(c, 960, 260, 960, 520, "#FFE8B0", 0.28, t, y_top=-60, y_bot=860)
        DUST.draw(c, t, 0.6)
        bx = 1400 - 60 * host
        draw(c, BISHs if t > K else BISHf, bx, 940, 0.62)
        draw(c, COFFIN, 900, 840, 1.0)
        if t < K: draw(c, LID, 900, 800, 1.0)
        else:
            q = lin(t, K, K + 0.9); draw(c, LID, 900 + 520 * q, 800 - 600 * q + 900 * q * q, 1.0, rot=-200 * q)
            for k in range(18):
                rr = random.Random(k); a = rr.uniform(-3.0, -0.1); v = rr.uniform(150, 420)
                bloom_spot(c, 900 + math.cos(a) * v * q, 820 + math.sin(a) * v * q, 30 + 40 * q, "#E8D8B8", 0.5 * (1 - q))
            rx = 900 + (bx - 230 - 900) * host
            draw(c, RUP, rx, 980 - 260 * (1 - rise) + 60 * (1 - rise), 0.62 * (0.9 + 0.1 * rise))
            if host > 0.5:  # kılıç piskoposun omzunun üstünde, boynuna değmez
                draw(c, SWORD, bx - 110, 560, 1.0, rot=-74)
    cam(c, 1.0 + 0.12 * ease_out(lin(t, K, K + 0.4)), 1060 + shake * math.sin(t * 80), 600, world); post(c, warm=0.1)

# 5 · KAPILAR
BG5 = BG(wall_svg() + '<path d="M0,440 L960,440 L960,540 L0,540 Z" fill="#7A7060"/>')
DOORL = sprite('<rect x="0" y="0" width="200" height="640" fill="#4A3424" stroke="#1A1410" stroke-width="10"/><path d="M10,120 h180 M10,520 h180" stroke="#2A1E14" stroke-width="12"/>', 200, 640, ax=0, ay=0)
VSIL = sprite('<g transform="translate(60,200)" fill="#1A1410"><circle cx="0" cy="-150" r="30"/><path d="M-36,-120 L36,-120 L44,40 L-44,40 Z"/><circle cx="-50" cy="-60" r="40"/><path d="M30,-200 L36,-120" stroke="#1A1410" stroke-width="8"/></g>', 140, 260, ax=60, ay=240)
RFALL = FIG(RAG3D, "3q", "fakedead", facing=-1); BJ5 = FIG(BJA, "3q", "grief", facing=-1, extra=BJ_EXTRA[1])
def shot5(c, t, d):
    A = CUE["acil"]; Y = CUE["yigil"]; op = ease_io(lin(t, A - 0.1, A + 0.9)); fall = ease_in(lin(t, Y - 0.5, Y))
    def world():
        draw(c, BG5, W / 2, H / 2)
        gx, gy, gw, gh = 600, 280, 720, 640
        c.drawRect(skia.Rect(gx, gy, gx + gw, gy + gh), skia.Paint(Color4f=col("#F2E6C8")))
        bloom_spot(c, gx + gw / 2, gy + gh / 2, 500, "#FFF0D0", 0.5 * op)
        for k in range(10):  # akın eden Viking siluetleri
            rr = random.Random(k); q = ((t - A) * rr.uniform(0.25, 0.4) + rr.random() * 0.4) if t > A else 0
            s = 0.4 + 0.9 * q
            if t > A and q < 1.2: draw(c, VSIL, gx + gw / 2 + rr.uniform(-280, 280) * (0.5 + q), gy + gh - 40 + 120 * q, s, a=min(1, q * 3))
        for side in (0, 1):
            w_ = 360 * (1 - op * 0.82)
            draw(c, DOORL, gx + (0 if side == 0 else gw - w_), gy, 1.0, sx=w_ / 200, sy=1.0)
        dust(c, t, gx + gw / 2, gy + gh) if False else None
        draw(c, BJ5, 1220, 1060, 0.66)
        draw(c, RFALL, 980 + 120 * fall, 1060 - 40 * fall, 0.62, rot=-26 * fall)
        if t > Y: g = math.exp(-(t - Y) * 2.5); bloom_spot(c, 1160, 700, 70, "#FFE08A", 0.6 * g)
    cam(c, 1.0 + 0.2 * ease_io(lin(t, Y - 1.0, d)), 1000 + 120 * ease_io(lin(t, Y - 1.0, d)), 600, world); post(c, warm=0.08)

SHOTS = list(zip([shot1, shot2, shot3, shot4, shot5], CUE["d"]))
def render(preview=None):
    surf = skia.Surface(W, H); c = surf.getCanvas()
    if preview:
        for i, frac in preview:
            fn, d = SHOTS[i]; c.clear(skia.ColorBLACK); fn(c, frac * d, d)
            surf.makeImageSnapshot().save(f"{OUT}/p{i}_{int(frac*100)}.png", skia.kPNG)
        return
    wr = Writer(f"{OUT}/paris.mp4"); dip = 6
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
    if sys.argv[1] == "prev": render([(0, 0.65), (1, 0.15), (1, 0.6), (1, 0.82), (2, 0.75), (3, 0.15), (3, 0.5), (3, 0.75), (4, 0.4), (4, 0.75)])
    else: render()
