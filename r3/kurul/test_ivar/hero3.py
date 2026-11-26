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
sys.path.insert(0, "/home/claude/r3/ivar2")
from bust import fig_bust
import tex
INK = "#1A1410"
EXP["break2"] = (-14, 6, 0.44, 0.14, "tremble2", "")
SPEC = dict(RAGNAR_UC, brow_k=0.62, no_blush=True, nose2=True, bead_c=("#7E7A6C", "#A8A496"))

# ---------------------------------------------------------------- baş (aynalı: sola, bebeğe bakıyor)
HS = 2.75
HX, HY = 650, 400
def head_svg():
    core = ('<g opacity="0.9">'
            '<path d="M-36,-14 Q-14,-24 10,-12 Q-14,4 -36,-14 Z M22,-14 Q42,-24 62,-12 Q44,4 22,-14 Z" fill="#9A6A50" opacity="0.18"/>'  # göz çukurları
            '<path d="M-62,30 Q-30,50 -2,42 Q-24,70 -60,58 Z" fill="#8A5A44" opacity="0.5"/></g>')                                       # elmacık altı
    lines = ('<g stroke="#7A4E38" fill="none" stroke-linecap="round" opacity="0.7">'
             '<path d="M-22,-46 q16,-8 34,0 M-14,-56 q12,-5 24,0" stroke-width="1.8"/>'      # endişe kırışığı: YALNIZ alın
             '<path d="M8,-30 q3,-8 1,-14" stroke-width="2"/>'                                 # kaş arası
             '<path d="M-8,26 q-6,12 -2,24" stroke-width="2"/></g>')                           # nazolabial
    tear = ('<path d="M-18,10 Q-24,20 -26,30" stroke="#CFE6F6" stroke-width="3" fill="none" stroke-linecap="round" opacity="0.7"/>'
            '<ellipse cx="-26" cy="33" rx="3.4" ry="4.6" fill="#DDEEFA" stroke="#6A8CA8" stroke-width="1.3" opacity="0.9"/><circle cx="-27" cy="31.5" r="1.2" fill="#FFFFFF"/>')
    return core + lines + tear
HEAD_OLD = None
HEAD = fig_bust(dict(SPEC, _head_extra=head_svg()), "break2", 0.75, HS, noarm=True)
EXP["break2_b"] = (EXP["break2"][0], EXP["break2"][1], 0.96) + tuple(EXP["break2"][3:])
HEAD_B = fig_bust(dict(SPEC, _head_extra=head_svg()), "break2_b", 0.75, HS, noarm=True)
LIVE = [False]   # animatik: göz kırpma + nefes + kolda hafif titreme

TOR = sprite(f'<g transform="translate(700,40)">'
             f'<path d="M-700,900 Q-640,260 -260,150 L300,140 Q660,260 720,900 Z" fill="{SPEC["tunic"]}" stroke="{INK}" stroke-width="11"/>'
             f'<path d="M720,900 Q650,300 300,170 L200,240 Q480,380 520,900 Z" fill="{SPEC["cloak"]}" stroke="{INK}" stroke-width="10"/>'
             f'<path d="M-420,170 Q-200,40 0,70 Q220,40 460,170 Q470,250 400,280 Q200,180 0,200 Q-200,180 -400,290 Q-470,240 -420,170 Z" fill="{SPEC["fur_collar"]}" stroke="{INK}" stroke-width="10"/>'
             + "".join(f'<path d="M{x},{y} q{(i%3-1)*8},18 {(i%2)*6-3},34" stroke="{shade(SPEC["fur_collar"],0.68)}" stroke-width="5" fill="none"/>' for i, (x, y) in enumerate([(random.Random(k).uniform(-380, 400), random.Random(k + 9).uniform(110, 230)) for k in range(46)]))
             + '</g>', 1400, 900, ax=700, ay=40, ss=1.0)

# ---------------------------------------------------------------- kol + bebek (tek kompozit, kare koordinatında)
EL = (520, 1130)          # dirsek (kadraj dışı, sağ alt): kol gövdeden geliyor
ANG = -31.0; SC = 0.86     # aynasız (model yönü korunur): el sağ üste, bebeğe uzanıyor
def to_frame(x, y):
    a = math.radians(ANG)
    return EL[0] + SC * (x * math.cos(a) - y * math.sin(a)), EL[1] + SC * (x * math.sin(a) + y * math.cos(a))
GRIP = to_frame(700, -30)
RINGP = to_frame(A.RING[0], A.RING[1])
def arm_svg(ring_only=False):
    lw = 7 / SC
    inner = A._ring_arc(False, lw) if ring_only else A.grip_composite(lw=lw)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}">{A.defs(SC, az=315)}'
            f'<g transform="translate({EL[0]},{EL[1]}) rotate({ANG}) scale({SC})">{inner}</g></svg>')
ARM = sprite(arm_svg(), W, H, ax=0, ay=0, ss=1.0)
RING_TOP = sprite(arm_svg(True), W, H, ax=0, ay=0, ss=1.0)

# zemin: nehir kıyısı (sağ): yosunlu toprak, kök, taşlar + temas gölgesi
R = random.Random
def _stone(x, y, rx, ry, k):
    return (f'<g filter="url(#t_tas_k)"><ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="#5E6670"/></g>'
            f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="none" stroke="{INK}" stroke-width="6"/>'
            f'<path d="M{x-rx*0.6},{y-ry*0.5} Q{x},{y-ry*1.05} {x+rx*0.5},{y-ry*0.6}" stroke="#9AA6B2" stroke-width="5" fill="none" opacity="0.7"/>'
            f'<path d="M{x-rx*0.9},{y+ry*0.3} Q{x},{y+ry} {x+rx*0.9},{y+ry*0.3}" stroke="#3E5A3A" stroke-width="8" fill="none" opacity="0.7"/>')
TAS = tex.TEX["tas"].replace('id="t_tas"', 'id="t_tas_k"')
GROUND = sprite(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}"><defs>{TAS}</defs>'
                f'<path d="M1960,1100 L1960,840 Q1700,770 1460,790 Q1200,800 1000,880 Q860,960 780,1100 Z" fill="#33402F" stroke="{INK}" stroke-width="7"/>'
                f'<path d="M1960,862 Q1700,794 1460,812 Q1220,822 1060,880" stroke="#5E6E4A" stroke-width="10" fill="none" opacity="0.8"/>'
                + "".join(f'<path d="M{x:.0f},{y:.0f} q{R(k).uniform(-8,8):.0f},-16 {R(k+3).uniform(-4,10):.0f},-26" stroke="#6E7E52" stroke-width="4" fill="none" stroke-linecap="round" opacity="0.9"/>'
                          for k, (x, y) in enumerate([(R(k).uniform(1000, 1940), R(k + 50).uniform(880, 1060)) for k in range(80)]))
                + '</svg>', W, H, ax=0, ay=0, ss=1.0)
def _rock(x, y, r, k):
    rr = R(k); pts = [(x + r * (1 + rr.uniform(-0.25, 0.2)) * math.cos(a) * 1.4, y + r * (1 + rr.uniform(-0.25, 0.2)) * math.sin(a) * 0.8) for a in [i * math.pi / 5 for i in range(10)]]
    d = "M" + " L".join(f"{px:.0f},{py:.0f}" for px, py in pts) + " Z"
    return (f'<g filter="url(#t_tas_k)"><path d="{d}" fill="#5A626C" stroke-linejoin="round"/></g><path d="{d}" fill="none" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
            f'<path d="M{x-r*0.9:.0f},{y-r*0.35:.0f} Q{x:.0f},{y-r*0.9:.0f} {x+r*0.8:.0f},{y-r*0.45:.0f}" stroke="#A6B2BE" stroke-width="4" fill="none" opacity="0.6"/>'
            f'<path d="M{x-r*1.2:.0f},{y+r*0.5:.0f} Q{x:.0f},{y+r*0.9:.0f} {x+r*1.2:.0f},{y+r*0.5:.0f}" stroke="#3E5A3A" stroke-width="7" fill="none" opacity="0.6"/>')
FG = sprite(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}"><defs>{TAS}</defs>'
            + _rock(1130, 958, 34, 1) + _rock(1214, 985, 22, 2) + _rock(1830, 950, 46, 3) + _rock(1744, 985, 24, 4)
            + '</svg>', W, H, ax=0, ay=0, ss=1.0)
# nehir: sisli su şeridi (orta plan) + karşı kıyı
RIVER = sprite(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}"><defs><linearGradient id="rv" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#B8C8D6"/><stop offset="1" stop-color="#6E8498"/></linearGradient></defs>'
               f'<path d="M-20,640 Q500,610 1000,630 Q1500,650 1940,620 L1940,720 Q1400,750 900,730 Q400,712 -20,740 Z" fill="url(#rv)"/>'
               + "".join(f'<path d="M{x:.0f},{y:.0f} h{R(k).uniform(40,140):.0f}" stroke="#E6EEF4" stroke-width="3" opacity="0.6" stroke-linecap="round"/>' for k, (x, y) in enumerate([(R(k).uniform(0, 1900), R(k + 9).uniform(645, 720)) for k in range(26)]))
               + f'<path d="M-20,640 Q500,610 1000,630 Q1500,650 1940,620 L1940,590 Q1500,600 1000,596 Q500,590 -20,606 Z" fill="#46545E" opacity="0.55"/>'
               '</svg>', W, H, ax=0, ay=0, ss=1.0)

def form_shade(c, sp, x, y, s, col_="#14202E", a=0.5, x0=None, x1=None):
    """Işık sağ üstten: sol taraf soğuk koyulaşır (form gölgesi, soğuk gölge rengi)."""
    c.saveLayer(None, None)
    draw(c, tinted(sp, col_), x, y, s)
    sh = skia.GradientShader.MakeLinear([skia.Point(x0, y - 300), skia.Point(x1, y + 200)], [col("#000000", 0), col("#000000", a)])
    p = skia.Paint(Shader=sh); p.setBlendMode(skia.BlendMode.kDstIn)
    c.drawRect(skia.Rect(0, 0, W, H), p); c.restore()

def soft_ellipse(c, x, y, rx, ry, color, a, blur=18):
    p = skia.Paint(Color4f=col(color, a), AntiAlias=True); p.setImageFilter(skia.ImageFilters.Blur(blur, blur))
    c.drawOval(skia.Rect(x - rx, y - ry, x + rx, y + ry), p)

def side_dark(c, a=0.45):
    """Başın arkası (sol) koyu: yüz arka plandan ayrışsın."""
    sh = skia.GradientShader.MakeLinear([skia.Point(0, 0), skia.Point(1100, 0)], [col("#0A121C", a), col("#0A121C", 0)])
    c.drawRect(skia.Rect(0, 0, W, H), skia.Paint(Shader=sh))

def frame(t=0.0):
    surf = skia.Surface(W, H); c = surf.getCanvas(); c.clear(skia.ColorBLACK)
    # arka plan: sisli orman + nehir; görünür ışık kaynağı SAĞ üstte (bebeğin tarafı)
    for L_ in (IA.FOG_FAR, IA.MID): draw(c, blurred(L_, 12), W / 2 - 100, H / 2 + 20, 1.15)
    draw(c, blurred(RIVER, 6), 0, 0, 1.0)
    draw(c, blurred(IA.NEAR, 12), W / 2 - 100, H / 2 + 60, 1.15)
    fog(c, t, 620, "#DDE4EA", 0.42, seed=2, speed=14)
    bloom_spot(c, 1700, 40, 640, "#EEF4FA", 0.6)
    side_dark(c, 0.5)
    light_shaft(c, 1560, 300, 820, 460, "#E6F0F8", 0.17, t=t, y_top=-60, y_bot=760)
    # gövde + baş (rim yalnız ışık tarafında: sağ-üst)
    hd = HEAD_B if (LIVE[0] and ((t + 0.6) % 3.6) < 0.14) else HEAD
    if LIVE[0]:
        c.save(); c.translate(HX, 1080); c.scale(1, 1 + 0.008 * math.sin(t * 2 * math.pi / 4.2)); c.rotate(0.35 * math.sin(t * 0.9)); c.translate(-HX, -1080)
    rim(c, hd, HX, HY, 1.0, "#EAF4FF", dx=7, dy=-5, a=0.8)
    draw(c, hd, HX, HY, 1.0)
    form_shade(c, hd, HX, HY, 1.0, a=0.6, x0=HX + 120, x1=HX - 200)
    if LIVE[0]: c.restore()
    # nefes buharı (sağa, bebeğe doğru)
    for k in range(3):
        q = ((t * 0.4 + k / 3) % 1.0); bloom_spot(c, 760 + 170 * q, 590 + 40 * q, 36 + 70 * q, "#EEF4FA", 0.4 * (1 - q))
    # zemin + bebek temas gölgesi + kol kompoziti
    draw(c, GROUND, 0, 0, 1.0)
    soft_ellipse(c, GRIP[0] + 130, GRIP[1] + 150, 230, 60, "#0A1018", 0.5, 22)
    if LIVE[0]:   # parmak kavrandıkça kol hafifçe titrer
        c.save(); c.translate(*EL); c.rotate(0.45 * math.sin(t * 7.0) * min(1.0, t / 2.0)); c.translate(-EL[0], -EL[1])
    rim(c, ARM, 0, 0, 1.0, "#DCEBFA", dx=5, dy=-4, a=0.55)
    draw(c, ARM, 0, 0, 1.0)
    if LIVE[0]: c.restore()
    form_shade(c, ARM, 0, 0, 1.0, a=0.42, x0=1200, x1=400)
    soft_ellipse(c, GRIP[0] - 8, GRIP[1] + 16, 26, 10, "#0A1018", 0.35, 6)       # kavrama temas gölgesi
    draw(c, blurred(FG, 3), 0, 0, 1.0)
    # ön plan: bulanık dal (sol üst, kadraj içinde) + iri zerreler
    c.save(); p = skia.Paint(Color4f=col("#1A2026", 0.92), StrokeWidth=54, Style=skia.Paint.kStroke_Style, StrokeCap=skia.Paint.kRound_Cap, AntiAlias=True)
    p.setImageFilter(skia.ImageFilters.Blur(14, 14)); path = skia.Path(); path.moveTo(-40, 150); path.quadTo(160, 170, 320, 90); path.quadTo(400, 50, 460, 70); c.drawPath(path, p)
    p.setStrokeWidth(20); path2 = skia.Path(); path2.moveTo(220, 140); path2.quadTo(260, 210, 310, 230); c.drawPath(path2, p); c.restore()
    Particles("dust", 34, seed=5, color="#E8EEF2", size=(3, 7), speed=10).draw(c, t, 0.7)
    gradient_grade(c, "#2A4A6E", "#1A2A3A", 0.33, "soft"); grade(c, "#9EB6CC", 0.16, "multiply")
    # grade SONRASI: tek sıcak vurgu = halka (+ kavrama noktasına çok hafif sıcaklık)
    draw(c, RING_TOP, 0, 0, 1.0)
    bloom_spot(c, RINGP[0], RINGP[1], 120, "#FFD98A", 0.32)
    bloom_spot(c, GRIP[0], GRIP[1], 70, "#FFE8C8", 0.14)
    vignette(c, 0.7); letterbox(c, 1.0, 70)
    return surf

if __name__ == "__main__":
    out = "/home/claude/r3/kurul/test_ivar/hero_v5.png"
    frame(1.2).makeImageSnapshot().save(out, skia.kPNG); print("ok", GRIP, RINGP)
