"""Sahne 7 · Lagertha'nın vedası v3: 5 ham kare (örgü onayı: kullanıcı 19.11 20:10).

1 Kral evi, gece  · Aslaug kapıdan giriyor, karnı belirgin; Ragnar ocak başında donup kalıyor.
2 Lagertha        · yakın plan, sıyrık; sırtı Ragnar'a dönük, kılıç kemerini bağlıyor; arkada Ragnar (bulanık).
3 Kapı eşiği      · Bjorn ortada, bir annesine bir babasına bakıyor; Lagertha kapıda, Ragnar solda.
4 Gidiş           · Lagertha ve Bjorn kapıdan kara çıkıyor (sırtları dönük); ön planda Ragnar'ın omzu.
5 Yalnız          · Ragnar kapı eşiğinde soğuk ışıkta; arkada Aslaug tahtta, ateş sönüyor.
Yardımcılar ivar2/frames.py'den (live, ex, fig_bust, place, svg_sprite, shade_side, finish).
python3 kareler.py [1 2 3 4 5]  → veda2/kare_N.png, kontakt_960.png
"""
import sys, math, random, os
sys.path[:0] = ["/home/claude/r3", "/home/claude/r2", "/home/claude/r3/veda", "/home/claude/r3/kurul/test_ivar", "/home/claude/r3/ivar2"]
import skia
from engine import *
from fx import *
from art3 import figure, EXP, shade
from storyboard import LAG, BJ
import frames as IF
from frames import live, ex, fig_bust, place, svg_sprite, shade_side, finish, RG, ASLv, INK, T, DUR, CUE2, lin_, ease_
import places as P
OUT = "/home/claude/r3/veda2"
LAGv = dict(LAG, brow_k=0.6, no_blush=True,   # Lagertha'nın broşu: kalkan düğümü (artı biçimi Athelstan'ın haçıyla karışıyordu)
            clasp='<g transform="translate(0,-440)"><circle r="16" fill="#C9D2D6" stroke="#1A1410" stroke-width="4"/><circle r="8" fill="none" stroke="#1A1410" stroke-width="3"/><circle r="2.5" fill="#1A1410"/></g>')
BJv = dict(BJ, brow_k=0.6, no_blush=True, face_scar=False, knot=False)   # Ragnar'ın kimlik izleri Bjorn'a sızmasın (R8)
EXP["shock"] = (-16, 12, 0.0, 0.0, "open_o", "")
EXP["coldv"] = (5, -2, 0.38, 0.10, "firm", "")
EXP["plead"] = (-13, 7, 0.14, 0.04, "open_s", "")
EXP["torn"] = (-11, 6, 0.18, 0.06, "flat", "")
EXP["hollow"] = (-14, 7, 0.42, 0.12, "tremble", "")

BELLY = (f'<path d="M-20,-380 Q60,-392 112,-330 Q140,-280 112,-230 Q80,-196 20,-204 Q-30,-214 -40,-260 Z" fill="{shade(ASLv["tunic"], 1.08)}" stroke="{INK}" stroke-width="5"/>'
         f'<path d="M50,-366 Q108,-340 114,-282" stroke="{shade(ASLv["tunic"], 1.45)}" stroke-width="8" fill="none" stroke-linecap="round" opacity="0.85"/>'
         f'<path d="M-10,-226 Q50,-206 104,-236" stroke="{shade(ASLv["tunic"], 0.7)}" stroke-width="10" fill="none" stroke-linecap="round" opacity="0.7"/>')
SWORD = (f'<path d="M-70,-262 Q0,-236 64,-270" stroke="#3A2418" stroke-width="14" fill="none"/>'                                   # kılıç kemeri
         f'<path d="M40,-262 L96,-40" stroke="{INK}" stroke-width="26" stroke-linecap="round"/><path d="M40,-262 L96,-40" stroke="#4A3424" stroke-width="18" stroke-linecap="round"/>'   # kın
         f'<path d="M26,-300 L44,-252" stroke="{INK}" stroke-width="14" stroke-linecap="round"/><path d="M26,-300 L44,-252" stroke="#6A5038" stroke-width="8" stroke-linecap="round"/>'   # kabza
         f'<path d="M14,-262 L62,-276" stroke="{INK}" stroke-width="12" stroke-linecap="round"/><path d="M14,-262 L62,-276" stroke="#A8B0B8" stroke-width="6" stroke-linecap="round"/>'  # balçak
         f'<circle cx="24" cy="-306" r="8" fill="#A8B0B8" stroke="{INK}" stroke-width="3"/>')

def throne(x, y, s=1.0):
    """Kral evinin yüksek koltuğu (taht karesi v4'teki biçim)."""
    return (f'<g transform="translate({x},{y}) scale({s})">'
            f'<path d="M-170,0 L-170,-260 Q0,-320 170,-260 L170,0 Z" fill="#4E3A26" stroke="{INK}" stroke-width="8"/>'
            f'<rect x="-170" y="-330" width="340" height="80" fill="#6E2A22" stroke="{INK}" stroke-width="6"/>'
            + "".join(f'<path d="M{-150+k*60},-250 l30,-50 l30,50 Z" fill="#C9A25A" opacity="0.85"/>' for k in range(5))
            + "".join(f'<rect x="{sx-20}" y="-360" width="40" height="380" fill="#5A4430" stroke="{INK}" stroke-width="6"/>'
                      f'<path d="M{sx},-358 q{24*g},-54 {6*g},-80 q{-20*g},-14 {-30*g},10" fill="#5A4430" stroke="{INK}" stroke-width="6"/>' for sx, g in ((-170, -1), (170, 1)))
            + f'<path d="M-150,-120 Q0,-160 150,-120 L156,-70 Q0,-50 -156,-70 Z" fill="#C8BCA6" stroke="{INK}" stroke-width="6"/></g>')

def hall(fire=1.0):
    return P.longhouse(fire) + throne(960, 640, 0.62)

def big_door(x0, x1, top, bot=1080, snow=True):
    w = x1 - x0; cx = (x0 + x1) / 2
    o = [f'<defs><linearGradient id="out" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9AB4CE"/><stop offset="0.62" stop-color="#C8D8E6"/><stop offset="0.63" stop-color="#E6EEF4"/><stop offset="1" stop-color="#C6D2DE"/></linearGradient></defs>',
         f'<path d="M{x0},{bot} L{x0},{top+w*0.25:.0f} Q{cx},{top-w*0.08:.0f} {x1},{top+w*0.25:.0f} L{x1},{bot} Z" fill="url(#out)"/>']
    if snow:   # dışarıda: karlı patika ve uzak ağaçlar
        hy = top + (bot - top) * 0.62
        o.append("".join(f'<path d="M{x0 + (k*37) % w:.0f},{hy:.0f} l-10,-34 l20,0 Z" fill="#7E92A6" opacity="0.8"/>' for k in range(int(w / 37) + 1)))
        o.append(f'<path d="M{cx-30},{bot} Q{cx},{hy+40} {cx+10},{hy+4} L{cx+30},{hy+4} Q{cx+40},{hy+40} {cx+90},{bot} Z" fill="#D8E2EC" opacity="0.8"/>')
    o.append(f'<path d="M{x0},{bot} L{x0},{top+w*0.25:.0f} Q{cx},{top-w*0.08:.0f} {x1},{top+w*0.25:.0f} L{x1},{bot}" fill="none" stroke="{INK}" stroke-width="44"/>'
             f'<path d="M{x0},{bot} L{x0},{top+w*0.25:.0f} Q{cx},{top-w*0.08:.0f} {x1},{top+w*0.25:.0f} L{x1},{bot}" fill="none" stroke="#4A3826" stroke-width="30"/>')
    return "".join(o)

def snowfall(c, t, box, n=60, seed=3):
    t = t or 0.0
    for j in range(n):
        r = random.Random(seed * 1000 + j); x = box[0] + (r.uniform(0, 1) * (box[2] - box[0]) + 20 * math.sin(t * 0.8 + j)) % (box[2] - box[0])
        y = box[1] + (r.uniform(0, 1) * (box[3] - box[1]) + t * r.uniform(30, 70)) % (box[3] - box[1])
        c.drawCircle(x, y, r.uniform(1.5, 3.5), skia.Paint(Color4f=col("#FFFFFF", 0.85), AntiAlias=True))

def full(spec, expr, s, facing=1, view="3q", look=None, extra="", w=1000, h=1300):
    sp = dict(spec)
    if extra: sp["_body_extra"] = extra
    return sprite(f'<g transform="translate({w/2},{h-60}) scale({s*facing},{s})">{figure(sp, view, "stand", expr, look=look)}</g>', w, h, ax=w / 2, ay=h - 60, ss=1.0)

# ------------------------------------------------------------------ 1 · Aslaug geliyor
def k1():
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    draw(c, blurred(place(hall()), 4), 0, 0, 1.0)
    door = svg_sprite(big_door(1360, 1760, 180, snow=True))
    draw(c, door, 0, 0, 1.0); bloom_spot(c, 1560, 560, 420, "#B8D4F0", 0.45)
    snowfall(c, t, (1380, 260, 1740, 1010), 40)
    q = 0.0 if t is None else ease_(lin_(t, 0, 2.2))                   # Aslaug kapıdan içeri adım atar
    AS2 = sprite(f'<g transform="translate(700,{520 + 1.6*80/82*560:.0f}) scale({-1.6*80/82:.4f},{1.6*80/82:.4f})">{figure(dict(ASLv, _body_extra=BELLY, _carry_svg=""), "3q", "stand", ex("neutral", IF.blink_at(1.0)), look=-0.5)}</g>', 1400, 1600, ax=700, ay=520, ss=1.0)
    with live(c, 1500, 1080, phase=1.0, breathe=0.004, ox=-60 * q if t is not None else 0):
        rim(c, AS2, 1500, 330, 1.0, "#CFE4FF", dx=-6, dy=-4, a=0.9)
        draw(c, AS2, 1500, 330, 1.0)
        shade_side(c, AS2, 1500, 330, 0.45, 1300, 1700, "#0E1622")
    RGs = fig_bust(RG, ex("shock", IF.blink_at(0.3)), 0.8, 2.0)
    with live(c, 560, 1080, phase=0.3, breathe=0.006):
        rim(c, RGs, 560, 380, 1.0, "#FFB070", dx=-4, dy=3, a=0.6)
        draw(c, RGs, 560, 380, 1.0)
        shade_side(c, RGs, 560, 380, 0.5, 700, 260, "#1A0E08")
    glow(c, 900, 1010, 460, "#FF8A3A", 0.3)
    finish(c, cold=False, warm=0.04); return s

# ------------------------------------------------------------------ 2 · Lagertha kılıcını kuşanıyor
def k2():
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    draw(c, blurred(place(hall()), 8), -300, 0, 1.0)
    RGs = fig_bust(RG, ex("plead", IF.blink_at(1.7)), 0.9, 1.45)
    with live(c, 520, 1080, phase=1.7, breathe=0.005):
        draw(c, blurred(RGs, 5), 520, 420, 1.0)                        # arkada, odak dışı
    c.drawRect(skia.Rect(0, 0, W, H), skia.Paint(Color4f=col("#0A0604", 0.25)))
    tie = 0.0 if t is None else ease_(lin_(t, CUE2.get("kusan", 99) - 0.4, CUE2.get("kusan", 99) + 0.8))
    sp = dict(LAGv, _body_extra=SWORD)
    LG = fig_bust(sp, ex("coldv", IF.blink_at(0.5)), 1.0, 2.15)
    with live(c, 1180, 1080, phase=0.5, breathe=0.005, oy=-8 * tie):
        rim(c, LG, 1180, 330, 1.0, "#FFB070", dx=-5, dy=3, a=0.6)
        draw(c, LG, 1180, 330, 1.0)
        shade_side(c, LG, 1180, 330, 0.5, 1050, 1550, "#1A0E08")
    glow(c, 700, 1060, 520, "#FF8A3A", 0.28)
    finish(c, cold=False, warm=0.04); return s

# ------------------------------------------------------------------ 3 · Bjorn ikisinin arasında
def k3():
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    draw(c, place(hall(0.7)), 0, 0, 1.0)
    door = svg_sprite(big_door(1300, 1720, 160, snow=True))
    draw(c, door, 0, 0, 1.0); bloom_spot(c, 1510, 540, 380, "#B8D4F0", 0.4); snowfall(c, t, (1320, 240, 1700, 1010), 36)
    look = 0.0 if t is None else math.sin(t * 1.6)                     # Bjorn bir annesine bir babasına bakar
    LGf = full(LAGv, ex("coldv", IF.blink_at(0.5)), 1.0, look=0.6)
    BJf = full(BJv, ex("torn", IF.blink_at(1.4)), 0.90, facing=1 if look >= 0 else -1, look=0.4)
    RGf = full(RG, ex("plead", IF.blink_at(0.2)), 1.02, look=0.7)
    for sp_, x, y, ph, rimc in ((RGf, 470, 1240, 0.2, "#FFB070"), (BJf, 960, 1250, 1.4, "#DCE8F6"), (LGf, 1440, 1240, 0.5, "#CFE4FF")):
        with live(c, x, y, phase=ph, breathe=0.005):
            rim(c, sp_, x, y, 1.0, rimc, dx=4 if x > 900 else -4, dy=-3, a=0.7)
            draw(c, sp_, x, y, 1.0)
    glow(c, 800, 1060, 420, "#FF8A3A", 0.22)
    finish(c, cold=True); return s

# ------------------------------------------------------------------ 4 · gidiş
def k4():
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    c.drawRect(skia.Rect(0, 0, W, H), skia.Paint(Color4f=col("#1C140E")))
    draw(c, blurred(place(P.longhouse(0.4)), 10), -200, 0, 1.0)
    c.drawRect(skia.Rect(0, 0, W, H), skia.Paint(Color4f=col("#05040A", 0.5)))
    door = svg_sprite(big_door(620, 1380, 90, snow=True))
    draw(c, door, 0, 0, 1.0); bloom_spot(c, 1000, 560, 560, "#C8DCF0", 0.35)
    q = 0.0 if t is None else ease_(lin_(t, 0, DUR[0] * 0.9))           # kara doğru uzaklaşırlar
    for spec, x, sc in ((LAGv, 930, 0.56), (BJv, 1080, 0.50)):
        f_ = sprite(f'<g transform="translate(400,1040) scale({sc})">{figure(spec, "back", "stand", "neutral")}</g>', 800, 1100, ax=400, ay=1040, ss=1.0)
        k = 1 - 0.45 * q; xx = x + (x - 1000) * 0.2 * q; yy = 1000 - 220 * q - 5 * abs(math.sin((t or 0) * 3.4 + x))
        rim(c, f_, xx, yy, k, "#F4F8FC", dx=3, dy=-3, a=0.9 * (1 - 0.3 * q))
        draw(c, f_, xx, yy, k, a=1 - 0.3 * q)
        draw(c, tinted(f_, "#2A3442"), xx, yy, k, a=0.55 * (1 - 0.3 * q))     # karşı ışıkta, ama biçimleri okunur
    snowfall(c, t, (640, 120, 1360, 1010), 70)
    RGb = sprite(f'<g transform="translate(500,1100) scale(1.5)">{figure(RG, "back", "stand", "neutral")}</g>', 1000, 1300, ax=500, ay=1100, ss=1.0)
    with live(c, 300, 1400, phase=0.4, breathe=0.004):
        draw(c, blurred(tinted(RGb, "#120C08"), 3), 300, 1400, 1.0)    # ön planda Ragnar'ın omzu (siluet)
    finish(c, cold=True); return s

# ------------------------------------------------------------------ 5 · yalnız
def k5():
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    draw(c, blurred(place(hall(0.08)), 5), 0, 0, 1.0)
    ASf = sprite(f'<g transform="translate(400,1000) scale(0.62)">{figure(dict(ASLv, _body_extra=BELLY), "front", "sit", "neutral", hands=("open", "open"))}</g>', 800, 1100, ax=400, ay=1000, ss=1.0)
    rim(c, ASf, 960, 650, 0.78, "#FFB070", dx=0, dy=-4, a=0.5)
    draw(c, blurred(ASf, 2), 960, 650, 0.78)                            # tahtta (hafif odak dışı)
    die = 0.0 if t is None else lin_(t, 0, DUR[0])
    glow(c, 960, 880, 220, "#FF6A20", 0.14 * (1 - 0.7 * die))           # sönmekte olan köz
    door = svg_sprite(big_door(1500, 1920, 120, snow=True))
    draw(c, door, 0, 0, 1.0); bloom_spot(c, 1720, 560, 480, "#C8DCF0", 0.5); snowfall(c, t, (1520, 200, 1920, 1010), 40)
    RGs = fig_bust(RG, ex("hollow", IF.blink_at(0.9)), 0.9, 2.35)
    with live(c, 1180, 1080, phase=0.9, breathe=0.006):
        rim(c, RGs, 1180, 400, 1.0, "#DCEBFA", dx=7, dy=-4, a=0.85)
        draw(c, RGs, 1180, 400, 1.0)
        shade_side(c, RGs, 1180, 400, 0.6, 1400, 900)
    finish(c, cold=True); grade(c, "#9EB6CC", 0.08 + 0.1 * die, "multiply"); letterbox(c, 1.0, 70); return s

FR = {1: k1, 2: k2, 3: k3, 4: k4, 5: k5}

def contact(ids=(1, 2, 3, 4, 5)):
    from PIL import Image
    cw, ch = 960, 540; sheet = Image.new("RGB", (cw * 2 + 30, (ch + 20) * 3 + 10), "#EDE2CC")
    for k, i in enumerate(ids):
        sheet.paste(Image.open(f"{OUT}/kare_{i}.png").convert("RGB").resize((cw, ch)), (10 + (k % 2) * (cw + 10), 10 + (k // 2) * (ch + 20)))
    sheet.save(f"{OUT}/kontakt_960.png")

if __name__ == "__main__":
    ids = [int(a) for a in sys.argv[1:]] or [1, 2, 3, 4, 5]
    for i in ids:
        T[0] = None; FR[i]().makeImageSnapshot().save(f"{OUT}/kare_{i}.png", skia.kPNG); print("kare", i)
    contact()
