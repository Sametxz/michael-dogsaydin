"""Ivar sahnesi v2 · 5 ham kare (hero_v4 çıtası: model yönü korunur, ışık yönlü, tek sıcak/soğuk vurgu, 3 plan).

1 Gece, ev         · Ragnar (sol, korku) ve Aslaug (sağ, kararlı), kucakta ağlayan Ivar; ışık ocaktan, aşağıdan, sıcak.
2 Şafak öncesi     · kapı aralığında Ragnar'ın silueti, kucağında bebek; ocak sönük; kapıdan soğuk ışık.
3 Nehir, bıçak     · alçak açı; seax havada, soğuk parıltı; ön planda bulanık kundak.
4 Yapamıyorsun     · hero_v4.
5 Kurtarma         · geniş plan; Ragnar sise karışarak uzaklaşıyor, Aslaug bebeği kucağına almış; sis içinden ışık.
Çalıştırma: python3 frames.py [1 2 3 5]  → ivar2/kare_N.png ve kontakt_960.png
"""
import sys, math, random, os
sys.path[:0] = ["/home/claude/r3", "/home/claude/r2", "/home/claude/r3/veda", "/home/claude/r3/kurul/test_ivar", "/home/claude/r3/ivar2"]
import skia
from engine import *
from fx import *
from art3 import head3, figure, EXP, RAGNAR_UC, shade
from storyboard import ASL
import assets as A
import places as P
from bust import fig_bust, baby_in_arms
from art3 import BODY
INK = "#1A1410"
OUT = "/home/claude/r3/ivar2"
import math as _m
EL3 = (1010, 790); AN3 = -64
def _tf(x, y, el=EL3, an=AN3, sc=0.82):
    a = _m.radians(an); return el[0] + sc * (x * _m.cos(a) - y * _m.sin(a)), el[1] + sc * (x * _m.sin(a) + y * _m.cos(a))
def _rot(p, o, deg):
    a = _m.radians(deg); x, y = p[0] - o[0], p[1] - o[1]; return o[0] + x * _m.cos(a) - y * _m.sin(a), o[1] + x * _m.sin(a) + y * _m.cos(a)
_b = _m.radians(-26); GLINT = _tf(650 + 0.9 * 524 * _m.cos(_b), 0.9 * 524 * _m.sin(_b))
RG = dict(RAGNAR_UC, brow_k=0.62, no_blush=True, nose2=True, bead_c=("#8A7E62", "#B0A48A"))
ASLv = dict(ASL, hair="#B4683E", iris="#5A8A6E", brow_c="#8A4E2E", loose=True, side_braids=False, long_braid=False, crown=False, brow_k=0.7, no_blush=True, skin="#F4D6BC", fur_collar="#D8CFC0")   # Aslaug: kızıl, dalgalı açık saç, ince altın taç bandı
KF = lambda hs: hs * 80 / BODY["tall"]["head_r"]
EXP["dread"] = (-10, 6, 0.08, 0.04, "flat", "")
EXP["horror"] = (-14, 8, 0.02, 0.0, "grit", "")
EXP["resolve"] = (8, -3, 0.30, 0.08, "firm", "")
EXP["worry"] = (-14, 7, 0.12, 0.04, "open_s", "")
EXP["aworry"] = (-9, 4, 0.28, 0.08, "flat", "")
EXP["relief"] = (-12, 6, 0.12, 0.10, "soft_smile", "tear")
EXP["shame"] = (-8, 4, 0.55, 0.10, "tremble", "")

# ---- hafif canlandırma (kullanıcı 19.11 19:07): göz kırpma, nefes, salınım, küçük eylemler.
# T[0] None iken kareler onaylı ham kareyle birebir aynıdır.
T = [None]; DUR = [1.0]; CUE2 = {}
from contextlib import contextmanager
def ex(e, blink):
    if not blink: return e
    b = e + "_b"
    if b not in EXP: v = EXP[e]; EXP[b] = (v[0], v[1], 0.96, v[3], v[4], v[5])
    return b
def blink_at(phase):
    t = T[0]; return t is not None and ((t + phase) % 3.4) < 0.13
@contextmanager
def live(c, px, py, phase=0.0, sway=0.0, breathe=0.006, rot=0.0, ox=0.0, oy=0.0, sc=1.0):
    """Karakteri pivot (px,py) çevresinde nefes/salınım/öteleme ile çizer."""
    t = T[0]
    if t is None: yield; return
    r = rot + sway * math.sin(t * 1.1 + phase); sy = 1 + breathe * math.sin(t * 2 * math.pi / 3.6 + phase)
    c.save(); c.translate(px + ox, py + oy); c.rotate(r); c.scale(sc, sc * sy); c.translate(-px, -py)
    yield
    c.restore()
lin_ = lambda t, a, b: min(1.0, max(0.0, (t - a) / (b - a))) if b > a else float(t >= a)
ease_ = lambda q: q * q * (3 - 2 * q)

def place(svg_inner):
    return sprite(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}">{svg_inner}</svg>', W, H, ax=0, ay=0, ss=1.0)

def bust(spec, expr, look, hs, flip=False, w=1400, h=1500):
    """Baş + gövde (omuz, kürk yaka). Yerel: baş merkezi (700,520). flip: yalnız asimetrik kimliği olmayan karakterler."""
    fur = spec.get("fur_collar", shade(spec["cloak"], 1.3))
    sx = -hs if flip else hs
    tor = (f'<g transform="translate(700,{520 + hs*150:.0f}) scale({hs/2.75:.3f})">'
           f'<path d="M-700,900 Q-640,260 -260,150 L300,140 Q660,260 720,900 Z" fill="{spec["tunic"]}" stroke="{INK}" stroke-width="11"/>'
           f'<path d="M720,900 Q650,300 300,170 L200,240 Q480,380 520,900 Z" fill="{spec["cloak"]}" stroke="{INK}" stroke-width="10"/>'
           f'<path d="M-420,170 Q-200,40 0,70 Q220,40 460,170 Q470,250 400,280 Q200,180 0,200 Q-200,180 -400,290 Q-470,240 -420,170 Z" fill="{fur}" stroke="{INK}" stroke-width="10"/>'
           + "".join(f'<path d="M{random.Random(k).uniform(-380,400):.0f},{random.Random(k+9).uniform(110,230):.0f} q{(k%3-1)*8},18 {(k%2)*6-3},34" stroke="{shade(fur,0.68)}" stroke-width="5" fill="none"/>' for k in range(46))
           + '</g>')
    return sprite(f'{tor}<g transform="translate(700,520) scale({sx},{hs})">{head3(spec, "3q", expr, look)}</g>', w, h, ax=700, ay=520, ss=1.0)

def shade_side(c, sp, x, y, a, x0, x1, colr="#14202E"):
    c.saveLayer(None, None); draw(c, tinted(sp, colr), x, y, 1.0)
    sh = skia.GradientShader.MakeLinear([skia.Point(x0, y - 300), skia.Point(x1, y + 200)], [col("#000000", 0), col("#000000", a)])
    p = skia.Paint(Shader=sh); p.setBlendMode(skia.BlendMode.kDstIn); c.drawRect(skia.Rect(0, 0, W, H), p); c.restore()

def svg_sprite(inner, defs_s=1.0, az=315):
    return sprite(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}">{A.defs(defs_s, az=az)}{inner}</svg>', W, H, ax=0, ay=0, ss=1.0)

def finish(c, cold=True, warm=0.0):
    if warm: grade(c, "#FFB060", warm, "screen")
    if cold: gradient_grade(c, "#2A4A6E", "#1A2A3A", 0.3, "soft"); grade(c, "#9EB6CC", 0.16, "multiply")
    vignette(c, 0.72); letterbox(c, 1.0, 70)

# ------------------------------------------------------------------ 1 · gece, ev
def k1():
    s = skia.Surface(W, H); c = s.getCanvas()
    draw(c, blurred(place(P.longhouse()), 5), 0, 0, 1.0)
    # Aslaug (sağ, aynalı: asimetrik kimliği yok) + kucağında ağlayan Ivar, bacak dışarıda
    AS = fig_bust(ASLv, ex("aworry", blink_at(1.3)), -0.4, 2.0, flip=True, carry=baby_in_arms(KF(2.0), cry=True, leg_out=True))
    with live(c, 1420, 1080, phase=1.3, sway=1.1, breathe=0.004):     # Aslaug bebeği sallıyor
        rim(c, AS, 1420, 380, 1.0, "#FFB070", dx=-5, dy=3, a=0.6)
        draw(c, AS, 1420, 380, 1.0)
        shade_side(c, AS, 1420, 380, 0.5, 1300, 1800, "#1A0E08")            # ışık aşağı-soldan (ocak): sağ taraf koyu
    # Ragnar (sol, model yönü sağa bakar) · korku
    RGs = fig_bust(RG, ex("worry", blink_at(0.4)), 0.8, 2.25)
    t = T[0] or 0.0; look_away = ease_(lin_(t, CUE2.get("kacir", 99), CUE2.get("kacir", 99) + 0.8))
    with live(c, 520, 1080, phase=0.4, sway=0.25, breathe=0.007, rot=-2.0 * look_away):   # "gözlerini kaçırıyorsun": baş hafif yana döner
        rim(c, RGs, 520, 360, 1.0, "#FFB070", dx=4, dy=3, a=0.6)
        draw(c, RGs, 520, 360, 1.0)
        shade_side(c, RGs, 520, 360, 0.55, 600, 200, "#1A0E08")
    glow(c, 960, 1000, 520, "#FF8A3A", 0.35)                             # ocak ışığı aşağıdan
    bloom_spot(c, 1400, 880, 160, "#FFD8A8", 0.18)
    finish(c, cold=False, warm=0.05); return s

# ------------------------------------------------------------------ 2 · şafak öncesi, kapı
def k2():
    s = skia.Surface(W, H); c = s.getCanvas()
    draw(c, blurred(place(P.longhouse(fire=0.2)), 7), W / 2 - 200, H / 2, 1.0)
    c.drawRect(skia.Rect(0, 0, W, H), skia.Paint(Color4f=col("#05060A", 0.55)))
    # büyük kapı aralığı (sağ): dışarıda şafak öncesi mavi
    door = svg_sprite('<path d="M1240,1080 L1240,250 Q1420,150 1600,250 L1600,1080 Z" fill="#7EA2C8"/>'
                      '<path d="M1240,1080 L1240,250 Q1420,150 1600,250 L1600,1080" fill="none" stroke="#1A1410" stroke-width="40"/>'
                      '<path d="M1290,1080 L1290,300 M1550,1080 L1550,300" stroke="#9EBAD8" stroke-width="6" opacity="0.6"/>')
    draw(c, door, 0, 0, 1.0); bloom_spot(c, 1420, 520, 420, "#B8D4F0", 0.55)
    light_shaft(c, 1420, 340, 900, 900, "#B8D4F0", 0.16, y_top=260, y_bot=1080)
    # Ragnar: kapıya yürüyor (sağa), kucağında kundak; yüz gölgede, soğuk kenar ışığı
    RGs = fig_bust(RG, ex("worry", blink_at(2.0)), 0.9, 2.1, carry=baby_in_arms(KF(2.1)))
    t = T[0]; wq = 0.0 if t is None else t / DUR[0]
    _lv = live(c, 820, 1080, phase=2.0, sway=0.0, breathe=0.005, ox=70 * wq, oy=-6 * abs(math.sin((t or 0) * 3.0)))   # kapıya doğru yürüyüş
    _lv.__enter__()
    for sp_, x_, y_ in ((RGs, 820, 390),):
        rim(c, sp_, x_, y_, 1.0, "#CFE4FF", dx=7, dy=-3, a=0.95)
        draw(c, sp_, x_, y_, 1.0)
        c.saveLayer(None, None); draw(c, tinted(sp_, "#0A0E16"), x_, y_, 1.0)
        sh = skia.GradientShader.MakeLinear([skia.Point(1200, 0), skia.Point(500, 0)], [col("#000000", 0.2), col("#000000", 0.6)])
        p = skia.Paint(Shader=sh); p.setBlendMode(skia.BlendMode.kDstIn); c.drawRect(skia.Rect(0, 0, W, H), p); c.restore()
    _lv.__exit__(None, None, None)
    # ön plan: uyuyan Aslaug'un saçı ve kürk (sol alt, bulanık)
    fg = svg_sprite('<path d="M-20,1080 L-20,820 Q200,760 420,840 Q520,900 560,1080 Z" fill="#4A3A2C"/>'
                    '<path d="M40,860 Q160,800 300,850 Q200,900 60,940 Z" fill="#C8B88A"/>' + "".join(f'<path d="M{60+k*30},{850-k*4} q20,30 10,60" stroke="#A8986A" stroke-width="6" fill="none"/>' for k in range(8)))
    gradient_grade(c, "#203A5E", "#0E1620", 0.35, "soft"); grade(c, "#8AA6C8", 0.18, "multiply")
    vignette(c, 0.8); letterbox(c, 1.0, 70); return s

def _path(d):
    return skia.Path.FromSVGString(d) if hasattr(skia.Path, "FromSVGString") else skia.Path()

def cam(c, z, cx, cy, fn):
    hw, hh = W / (2 * z), H / (2 * z); cx = min(max(cx, hw), W - hw); cy = min(max(cy, hh), H - hh)
    c.save(); c.translate(W / 2, H / 2); c.scale(z, z); c.translate(-cx, -cy); fn(); c.restore()

# ------------------------------------------------------------------ 3 · nehir, bıçak (alçak açı)
def k3():
    s = skia.Surface(W, H); c = s.getCanvas()
    c.clear(col("#4E6276").toColor())   # onaylı karenin (alfa atılmış) gökyüzüyle aynı ton
    rb = place(P.riverbank())
    draw(c, blurred(rb, 4), W / 2, H / 2 + 260, 1.0)                     # ufuk aşağıda: alçak açı
    bloom_spot(c, 1500, 120, 520, "#EEF4FA", 0.5)
    RGs = fig_bust(RG, ex("horror", blink_at(0.9)), 0.2, 2.55, noarm=True)
    with live(c, 760, 1080, phase=0.9, breathe=0.012):                 # ağır, hızlı nefes
        rim(c, RGs, 760, 470, 1.0, "#EAF4FF", dx=6, dy=-5, a=0.8)
        draw(c, RGs, 760, 470, 1.0)
        shade_side(c, RGs, 760, 470, 0.55, 980, 520)
    # kalkık kol (omuzdan yukarı) + seax: bıçağın ağzı gökyüzüne
    arm = svg_sprite(f'<g transform="translate({EL3[0]},{EL3[1]}) rotate({AN3}) scale(0.82)">{A.arm(index_out=False, s=0.82, lw=7/0.82)}'
                     f'<g transform="translate(650,0) rotate(-26) scale(0.9)">{P.seax()}</g></g>', 0.82)
    t = T[0]; K = CUE2.get("kaldir", 1.0)
    up = 0.0 if t is None else 1 - ease_(lin_(t, K - 0.6, K + 0.5))        # "kaldırıyorsun"da kol kalkar
    tr = 0.0 if t is None else 1.4 * math.sin(t * 21) * lin_(t, K + 0.5, K + 2.0)   # sonra titrer
    ang = 34 * up + tr
    c.save(); c.translate(*EL3); c.rotate(ang); c.translate(-EL3[0], -EL3[1]); draw(c, arm, 0, 0, 1.0); c.restore()
    GL = _rot(GLINT, EL3, ang)
    # ön plan: bulanık kundak (alt sağ)
    bb = svg_sprite(f'<g transform="translate(1560,1000) scale(0.9) rotate(10)">{A.baby(s=0.9, lw=8)}</g>', 0.9)
    finish(c)
    bloom_spot(c, *GL, 90, "#F4FAFF", 0.85 * (1 - up)); bloom_spot(c, GL[0], GL[1] + 220, 40, "#E8F2FF", 0.35 * (1 - up))
    return s

# ------------------------------------------------------------------ 5 · kurtarma (geniş)
def k5():
    s = skia.Surface(W, H); c = s.getCanvas()
    draw(c, place(P.riverbank()), 0, 0, 1.0)
    # Ragnar: solda, sırtı dönük, sise karışarak uzaklaşıyor
    rgf = sprite(f'<g transform="translate(300,700) scale(0.36)">{figure(RG, "back", "stand", "neutral")}</g>', 600, 760, ax=300, ay=700, ss=1.0)
    t = T[0]; q = 0.0 if t is None else ease_(lin_(t, 0, DUR[0] * 0.7))       # Ragnar sise doğru uzaklaşır ve kaybolur
    draw(c, tinted(rgf, "#6E8296"), 360 - 160 * q, 760 - 30 * q - 4 * abs(math.sin((t or 0) * 3.2)) * (1 - q), 1.0 - 0.25 * q, a=1.0 - 0.85 * q)
    fog(c, 0.0, 700, "#DDE4EA", 0.6, seed=7, speed=10)
    light_shaft(c, 1300, 300, 1300, 700, "#F4F0E0", 0.3, y_top=-60, y_bot=1080)
    bloom_spot(c, 1320, 80, 460, "#FFF6E0", 0.5)
    # Aslaug: orta plan, ışıkta; bebek kucağında (kare 1 ile aynı model ve kucak)
    AS = fig_bust(ASLv, ex("relief", blink_at(0.2)), -0.6, 2.05, flip=True, carry=baby_in_arms(KF(2.05), awake=True))
    with live(c, 1300, 1080, phase=0.2, sway=0.9, breathe=0.005):
        rim(c, AS, 1300, 400, 1.0, "#FFF6E0", dx=-5, dy=-5, a=0.85)
        draw(c, AS, 1300, 400, 1.0)
        shade_side(c, AS, 1300, 400, 0.35, 1200, 1700)
    finish(c)
    bloom_spot(c, 1300, 860, 120, "#FFE4B8", 0.25)                        # tek sıcak vurgu: anne-bebek
    return s

FR = {1: k1, 2: k2, 3: k3, 5: k5}

def contact(ids):
    from PIL import Image
    ims = [Image.open(f"{OUT}/kare_{i}.png") if i != 4 else Image.open("/home/claude/r3/kurul/test_ivar/hero_v5.png") for i in ids]
    cw, ch = 960, 540; sheet = Image.new("RGB", (cw * 2 + 30, (ch + 20) * ((len(ims) + 1) // 2) + 10), "#EDE2CC")
    for k, im in enumerate(ims):
        sheet.paste(im.resize((cw, ch)), (10 + (k % 2) * (cw + 10), 10 + (k // 2) * (ch + 20)))
    sheet.save(f"{OUT}/kontakt_960.png")

if __name__ == "__main__":
    ids = [int(a) for a in sys.argv[1:]] or [1, 2, 3, 5]
    for i in ids:
        FR[i]().makeImageSnapshot().save(f"{OUT}/kare_{i}.png", skia.kPNG); print("kare", i)
    contact([1, 2, 3, 4, 5])
