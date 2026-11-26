"""Kahraman kare testi: Ivar sahnesi 'Yapamıyorsun' — Ragnar ¾ yakın plan (ham kare)."""
import sys, math, random
sys.path[:0] = ["/home/claude/r3", "/home/claude/r2", "/home/claude/r3/veda", "/home/claude/r3/ivar"]
import skia
from engine import *
from fx import *
from art3 import head3, EXP, RAGNAR_UC, shade, hand3
import ivar.anim as IA  # orman katmanları
INK = "#1A1410"
EXP["break"] = (-15, 7, 0.40, 0.16, "tremble", "tear")
SPEC = dict(RAGNAR_UC)
HS = 3.3
def head_svg(extra=""):
    lines = ('<g stroke="#7A4E38" fill="none" stroke-linecap="round" opacity="0.75">'
             '<path d="M2,-52 q4,-12 2,-22 M14,-50 q2,-10 0,-18" stroke-width="2.4"/>'      # kaş arası çatık
             '<path d="M-14,-66 q18,-10 40,0 M-8,-76 q14,-6 30,0" stroke-width="2"/>'       # endişe kırışığı
             '<path d="M-6,22 q-6,14 -2,28 M44,22 q8,12 6,24" stroke-width="2.6"/>'         # nazolabial gerilim
             '<path d="M30,-12 q8,6 18,4" stroke-width="2"/></g>')                           # göz altı
    return f'<g transform="translate(500,520) scale({HS})">{head3(SPEC, "3q", "break", -0.55)}{lines}{extra}</g>'
HEAD = sprite(head_svg(), 1000, 1500, ax=500, ay=520, ss=1.0)
TOR = sprite(f'<g transform="translate(700,40)">'
             f'<path d="M-700,900 Q-640,260 -260,150 L300,140 Q660,260 720,900 Z" fill="{SPEC["tunic"]}" stroke="{INK}" stroke-width="12"/>'
             f'<path d="M-700,900 Q-650,300 -300,170 L-200,240 Q-480,380 -520,900 Z" fill="{SPEC["cloak"]}" stroke="{INK}" stroke-width="10"/>'
             f'<path d="M-420,170 Q-200,40 0,70 Q220,40 460,170 Q470,250 400,280 Q200,180 0,200 Q-200,180 -400,290 Q-470,240 -420,170 Z" fill="{SPEC["fur_collar"]}" stroke="{INK}" stroke-width="10"/>'
             + "".join(f'<path d="M{x},{y} q{(i%3-1)*8},18 {(i%2)*6-3},34" stroke="{shade(SPEC["fur_collar"],0.68)}" stroke-width="6" fill="none"/>' for i, (x, y) in enumerate([(random.Random(k).uniform(-380, 400), random.Random(k + 9).uniform(110, 230)) for k in range(46)]))
             + '</g>', 1400, 900, ax=700, ay=40, ss=1.0)
ARM = sprite(f'<g><path d="M-40,620 Q160,520 420,470 L470,560 Q220,640 0,760 Z" fill="{SPEC["tunic"]}" stroke="{INK}" stroke-width="10"/>'
             f'<path d="M400,470 Q520,440 600,470 L610,560 Q520,580 450,560 Z" fill="{SPEC["skin"]}" stroke="{INK}" stroke-width="9"/>'
             f'<circle cx="380" cy="515" r="70" fill="none" stroke="{INK}" stroke-width="34"/><circle cx="380" cy="515" r="70" fill="none" stroke="#D9A93A" stroke-width="22"/>'
             f'<path d="M340,462 q30,-10 60,0" stroke="#FFF0B0" stroke-width="6" fill="none" opacity="0.8"/></g>', 700, 800, ax=0, ay=0, ss=1.0)
BABYH = sprite(f'<g><path d="M120,800 Q170,700 300,600" stroke="{INK}" stroke-width="44" fill="none" stroke-linecap="round"/><path d="M120,800 Q170,700 300,600" stroke="#F2CDAA" stroke-width="34" fill="none" stroke-linecap="round"/>'
               f'<ellipse cx="318" cy="584" rx="30" ry="24" fill="#F2CDAA" stroke="{INK}" stroke-width="7"/>'
               + "".join(f'<path d="M{330+k*10},{566+k*4} q12,-10 20,-6" stroke="{INK}" stroke-width="5" fill="#F2CDAA" stroke-linecap="round"/>' for k in range(3)) + '</g>', 500, 820, ax=0, ay=0, ss=1.0)
def form_shade(c, sp, x, y, s, col_="#14202E", a=0.55, x0=None, x1=None):
    """Işık soldan-yukarıdan: sağ-alt tarafı koyulaştır (form gölgesi)."""
    c.saveLayer(None, None)
    draw(c, tinted(sp, col_), x, y, s)
    x0 = x - sp.w * s * 0.15 if x0 is None else x0; x1 = x + sp.w * s * 0.35 if x1 is None else x1
    sh = skia.GradientShader.MakeLinear([skia.Point(x0, y - 300), skia.Point(x1, y + 200)], [col("#000000", 0), col("#000000", a)])
    p = skia.Paint(Shader=sh); p.setBlendMode(skia.BlendMode.kDstIn)
    c.drawRect(skia.Rect(0, 0, W, H), p); c.restore()
def frame(t=0.0):
    surf = skia.Surface(W, H); c = surf.getCanvas(); c.clear(skia.ColorBLACK)
    # arka plan: sisli orman, çok bulanık, hafif yukarı bakan
    for L_ in (IA.FOG_FAR, IA.MID, IA.NEAR): draw(c, blurred(L_, 14), W / 2, H / 2 + 120, 1.1)
    fog(c, t, 700, "#DDE4EA", 0.5, seed=2, speed=14)
    bloom_spot(c, 420, 220, 520, "#E8F0F6", 0.35)   # soğuk anahtar ışık kaynağı (sol üst)
    # gövde + baş
    tx, ty = 1150, 700
    draw(c, TOR, tx, ty, 1.0); form_shade(c, TOR, tx, ty, 1.0, a=0.55, x0=900, x1=1700)
    hx, hy = 1120, 430
    rim(c, HEAD, hx, hy, 1.0, "#EAF4FF", dx=-6, dy=-4, a=0.7)
    draw(c, HEAD, hx, hy, 1.0)
    form_shade(c, HEAD, hx, hy, 1.0, a=0.45, x0=1080, x1=1420)
    # nefes buharı
    for k in range(3):
        q = ((t * 0.4 + k / 3) % 1.0); bloom_spot(c, 1040 - 160 * q, 620 + 30 * q, 40 + 70 * q, "#EEF4FA", 0.22 * (1 - q))
    # ön plan: halkalı kol + bebeğin eli (alt sol), sıcak tek vurgu halkada
    draw(c, ARM, -60, 260, 1.25); form_shade(c, ARM, -60, 260, 1.25, a=0.45, x0=200, x1=700)
    draw(c, BABYH, 60, 300, 1.2)
    bloom_spot(c, 415, 905, 120, "#FFD98A", 0.3)
    # ön plan bulanık dal (derinlik), uçuşan zerreler
    c.save(); p = skia.Paint(Color4f=col("#20262C", 0.85), StrokeWidth=60, Style=skia.Paint.kStroke_Style, StrokeCap=skia.Paint.kRound_Cap, AntiAlias=True)
    p.setImageFilter(skia.ImageFilters.Blur(18, 18)); path = skia.Path(); path.moveTo(1980, 60); path.quadTo(1700, 120, 1560, 40); c.drawPath(path, p); c.restore()
    Particles("dust", 40, seed=5, color="#E8EEF2", size=(2, 4), speed=10).draw(c, t, 0.6)
    gradient_grade(c, "#2A4A6E", "#1A2A3A", 0.35, "soft"); grade(c, "#9EB6CC", 0.18, "multiply")
    vignette(c, 0.75); letterbox(c, 1.0, 70)
    return surf
if __name__ == "__main__":
    frame(1.2).makeImageSnapshot().save("/home/claude/r3/kurul/test_ivar/hero_v1.png", skia.kPNG); print("ok")
