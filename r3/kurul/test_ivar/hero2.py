"""Kahraman kare v2 · Ivar sahnesi: Ragnar bebeği öldüremiyor ("Yapamıyorsun").

Ivar parmağını kavrıyor, Ragnar aşağı bakıyor. Kurul hero_v1 kararındaki 6 düzeltme ve
nesne kartı v2'den kalanlar bu karede uygulandı:
1. Kol kadraj dışından giriyor, eli var, bebek parmağı kavrıyor.
2. Kırışıklar yalnızca alında.
3. Kaşlar model kalınlığında, pembe yanak lekesi yok.
4. Gözyaşı alt kapaktan iniyor, yara izinden ayrı.
5. Işık sol üstten geliyor; çekirdek gölge var, rim yalnızca ışık tarafında.
6. Tek sıcak vurgu halkada; ön planda dal ve zemin var.
"""
import sys, math, random
sys.path[:0] = ["/home/claude/r3", "/home/claude/r2", "/home/claude/r3/veda", "/home/claude/r3/ivar", "/home/claude/r3/kurul/test_ivar"]
import skia
from engine import *
from fx import *
from art3 import head3, EXP, RAGNAR_UC, shade
import ivar.anim as IA
import assets as A
INK = "#1A1410"
EXP["break2"] = (-14, 6, 0.44, 0.14, "tremble2", "")
SPEC = dict(RAGNAR_UC, brow_k=0.62, no_blush=True)

# ---------------------------------------------------------------- baş (aynalı: sola, bebeğe bakıyor)
HS = 2.75
HX, HY = 1290, 400
def head_svg():
    core = ('<g opacity="0.9">'
            '<path d="M-36,-14 Q-14,-24 10,-12 Q-14,4 -36,-14 Z M22,-14 Q42,-24 62,-12 Q44,4 22,-14 Z" fill="#9A6A50" opacity="0.18"/>'  # göz çukurları
            '<path d="M42,-4 Q36,18 40,40 Q48,44 54,40 Q44,18 42,-4 Z" fill="#9A6A50" opacity="0.5"/>'                                    # burnun gölge yanı (ışığa ters)
            '<path d="M-56,36 Q-30,52 -6,44 Q-30,62 -56,50 Z" fill="#9A6A50" opacity="0.35"/></g>')                                       # elmacık altı
    lines = ('<g stroke="#7A4E38" fill="none" stroke-linecap="round" opacity="0.7">'
             '<path d="M-22,-46 q16,-8 34,0 M-14,-56 q12,-5 24,0" stroke-width="1.8"/>'      # endişe kırışığı: YALNIZ alın
             '<path d="M8,-30 q3,-8 1,-14" stroke-width="2"/>'                                 # kaş arası
             '<path d="M-8,26 q-6,12 -2,24" stroke-width="2"/></g>')                           # nazolabial
    tear = ('<path d="M-18,10 Q-24,20 -26,30" stroke="#CFE6F6" stroke-width="3" fill="none" stroke-linecap="round" opacity="0.7"/>'
            '<ellipse cx="-26" cy="33" rx="3.4" ry="4.6" fill="#DDEEFA" stroke="#6A8CA8" stroke-width="1.3" opacity="0.9"/><circle cx="-27" cy="31.5" r="1.2" fill="#FFFFFF"/>')
    return (f'<g transform="translate(500,520) scale({-HS},{HS})">{head3(SPEC, "3q", "break2", -0.5)}{core}{lines}{tear}</g>')
HEAD = sprite(head_svg(), 1000, 1500, ax=500, ay=520, ss=1.0)

TOR = sprite(f'<g transform="translate(700,40)">'
             f'<path d="M-700,900 Q-640,260 -260,150 L300,140 Q660,260 720,900 Z" fill="{SPEC["tunic"]}" stroke="{INK}" stroke-width="11"/>'
             f'<path d="M720,900 Q650,300 300,170 L200,240 Q480,380 520,900 Z" fill="{SPEC["cloak"]}" stroke="{INK}" stroke-width="10"/>'
             f'<path d="M-420,170 Q-200,40 0,70 Q220,40 460,170 Q470,250 400,280 Q200,180 0,200 Q-200,180 -400,290 Q-470,240 -420,170 Z" fill="{SPEC["fur_collar"]}" stroke="{INK}" stroke-width="10"/>'
             + "".join(f'<path d="M{x},{y} q{(i%3-1)*8},18 {(i%2)*6-3},34" stroke="{shade(SPEC["fur_collar"],0.68)}" stroke-width="5" fill="none"/>' for i, (x, y) in enumerate([(random.Random(k).uniform(-380, 400), random.Random(k + 9).uniform(110, 230)) for k in range(46)]))
             + '</g>', 1400, 900, ax=700, ay=40, ss=1.0)

# ---------------------------------------------------------------- kol + bebek (tek kompozit, kare koordinatında)
EL = (1360, 1110)          # dirsek (kadraj dışı, sağ alt): kol gövdeden geliyor
ANG = 31.0; SC = 0.86      # aynala + döndür: el sol üste, bebeğe uzanıyor
def to_frame(x, y):
    x = -x; a = math.radians(ANG)
    return EL[0] + SC * (x * math.cos(a) - y * math.sin(a)), EL[1] + SC * (x * math.sin(a) + y * math.cos(a))
GRIP = to_frame(700, -30)
RINGP = to_frame(A.RING[0], A.RING[1])
def arm_svg(ring_only=False):
    lw = 7 / SC
    inner = A._ring_arc(False, lw) if ring_only else A.grip_composite(lw=lw)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}">{A.defs(SC, az=225)}'
            f'<g transform="translate({EL[0]},{EL[1]}) rotate({ANG}) scale({-SC},{SC})">{inner}</g></svg>')
ARM = sprite(arm_svg(), W, H, ax=0, ay=0, ss=1.0)
RING_TOP = sprite(arm_svg(True), W, H, ax=0, ay=0, ss=1.0)

# zemin: yosunlu toprak, kökler (bebeğin yattığı yer) + temas gölgesi
GROUND = sprite(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}">{A.defs(1.0)}'
                f'<path d="M-40,1100 L-40,860 Q200,800 420,830 Q640,860 820,940 Q980,1010 1100,1100 Z" fill="#33402F" stroke="{INK}" stroke-width="7"/>'
                f'<path d="M-40,880 Q200,826 420,852 Q600,876 760,940" stroke="#5E6E4A" stroke-width="10" fill="none" opacity="0.8"/>'
                + "".join(f'<path d="M{x},{y} q{random.Random(k).uniform(-8,8):.0f},-16 {random.Random(k+3).uniform(-4,10):.0f},-26" stroke="#6E7E52" stroke-width="4" fill="none" stroke-linecap="round" opacity="0.9"/>'
                          for k, (x, y) in enumerate([(random.Random(k).uniform(0, 900), random.Random(k + 50).uniform(880, 1060)) for k in range(70)]))
                + f'<path d="M80,900 Q160,860 260,880 Q360,900 420,960" stroke="#3C2E22" stroke-width="26" fill="none" stroke-linecap="round"/>'
                f'<path d="M80,900 Q160,860 260,880 Q360,900 420,960" stroke="#5A4634" stroke-width="12" fill="none" stroke-linecap="round" opacity="0.7"/>'
                '</svg>', W, H, ax=0, ay=0, ss=1.0)

def form_shade(c, sp, x, y, s, col_="#14202E", a=0.5, x0=None, x1=None):
    """Işık sol üstten: sağ-alt tarafı soğuk koyulaştır (form gölgesi, soğuk gölge rengi)."""
    c.saveLayer(None, None)
    draw(c, tinted(sp, col_), x, y, s)
    sh = skia.GradientShader.MakeLinear([skia.Point(x0, y - 300), skia.Point(x1, y + 200)], [col("#000000", 0), col("#000000", a)])
    p = skia.Paint(Shader=sh); p.setBlendMode(skia.BlendMode.kDstIn)
    c.drawRect(skia.Rect(0, 0, W, H), p); c.restore()

def soft_ellipse(c, x, y, rx, ry, color, a, blur=18):
    p = skia.Paint(Color4f=col(color, a), AntiAlias=True); p.setImageFilter(skia.ImageFilters.Blur(blur, blur))
    c.drawOval(skia.Rect(x - rx, y - ry, x + rx, y + ry), p)

def frame(t=0.0):
    surf = skia.Surface(W, H); c = surf.getCanvas(); c.clear(skia.ColorBLACK)
    # arka plan: sisli orman (bulanık), görünür ışık kaynağı sol üstte
    for L_ in (IA.FOG_FAR, IA.MID, IA.NEAR): draw(c, blurred(L_, 12), W / 2 + 140, H / 2 + 60, 1.15)
    fog(c, t, 640, "#DDE4EA", 0.45, seed=2, speed=14)
    bloom_spot(c, 260, 60, 620, "#EEF4FA", 0.55)
    light_shaft(c, 240, 260, 1150, 520, "#E6F0F8", 0.16, t=t, y_top=-60, y_bot=760)
    # gövde + baş (rim yalnız ışık tarafında: sol-üst)
    draw(c, TOR, 1330, 700, 1.0); form_shade(c, TOR, 1330, 700, 1.0, a=0.6, x0=1100, x1=1900)
    rim(c, HEAD, HX, HY, 1.0, "#EAF4FF", dx=-6, dy=-5, a=0.75)
    draw(c, HEAD, HX, HY, 1.0)
    form_shade(c, HEAD, HX, HY, 1.0, a=0.42, x0=1240, x1=1560)
    # nefes buharı (görünür)
    for k in range(3):
        q = ((t * 0.4 + k / 3) % 1.0); bloom_spot(c, 1180 - 170 * q, 590 + 40 * q, 36 + 70 * q, "#EEF4FA", 0.4 * (1 - q))
    # zemin + bebek temas gölgesi + kol kompoziti
    draw(c, GROUND, 0, 0, 1.0)
    soft_ellipse(c, GRIP[0] - 120, GRIP[1] + 150, 230, 60, "#0A1018", 0.5, 22)
    rim(c, ARM, 0, 0, 1.0, "#DCEBFA", dx=-4, dy=-4, a=0.55)
    draw(c, ARM, 0, 0, 1.0)
    form_shade(c, ARM, 0, 0, 1.0, a=0.4, x0=700, x1=1400)
    soft_ellipse(c, GRIP[0] + 8, GRIP[1] + 16, 26, 10, "#0A1018", 0.35, 6)       # kavrama temas gölgesi
    # ön plan: bulanık dal (sağ üst, kadraj içinde) + iri zerreler
    c.save(); p = skia.Paint(Color4f=col("#1A2026", 0.92), StrokeWidth=54, Style=skia.Paint.kStroke_Style, StrokeCap=skia.Paint.kRound_Cap, AntiAlias=True)
    p.setImageFilter(skia.ImageFilters.Blur(14, 14)); path = skia.Path(); path.moveTo(1960, 150); path.quadTo(1760, 170, 1600, 90); path.quadTo(1520, 50, 1460, 70); c.drawPath(path, p)
    p.setStrokeWidth(20); path2 = skia.Path(); path2.moveTo(1700, 140); path2.quadTo(1660, 210, 1610, 230); c.drawPath(path2, p); c.restore()
    Particles("dust", 34, seed=5, color="#E8EEF2", size=(3, 7), speed=10).draw(c, t, 0.7)
    gradient_grade(c, "#2A4A6E", "#1A2A3A", 0.33, "soft"); grade(c, "#9EB6CC", 0.16, "multiply")
    # grade SONRASI: tek sıcak vurgu = halka (+ kavrama noktasına çok hafif sıcaklık)
    draw(c, RING_TOP, 0, 0, 1.0)
    bloom_spot(c, RINGP[0], RINGP[1], 120, "#FFD98A", 0.32)
    bloom_spot(c, GRIP[0], GRIP[1], 70, "#FFE8C8", 0.14)
    vignette(c, 0.7); letterbox(c, 1.0, 70)
    return surf

if __name__ == "__main__":
    out = "/home/claude/r3/kurul/test_ivar/hero_v2.png"
    frame(1.2).makeImageSnapshot().save(out, skia.kPNG); print("ok", GRIP, RINGP)
