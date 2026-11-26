"""Sahne 7 · Lagertha'nın vedası, örgü v2 (dizi akışı, kullanıcı onayı 19.11 20:29): 6 ham kare.
1 Salon: Ragnar hükümdar koltuğunda, hamile Aslaug giriyor   2 Salon: "İki karın olabilir" (Aslaug kabul, Lagertha değil)
3 Kattegat sabah: Lagertha kılıcını kuşanıyor, eşek arabası; Bjorn babasının yanında   4 Lagertha Bjorn'u alnından öpüyor
5 Araba uzaklaşıyor, Bjorn ardından koşuyor; Ragnar izliyor   6 Ragnar salon kapısında yalnız, Aslaug koltuğun yanında
python3 kareler2.py [1..6] → veda2/k2_N.png, kontakt2_960.png
"""
import sys, math, random
sys.path[:0] = ["/home/claude/r3/veda2"]
from kareler import *          # LAGv, BJv, BELLY, SWORD, big_door, snowfall, full, yardımcılar
import places7 as P7
import obj7 as O7
EXP["demure"] = (-6, 3, 0.40, 0.10, "flat", "")
EXP["kiss_closed"] = (-8, 4, 0.92, 0.10, "flat", "")
EXP["tenderv"] = (-9, 5, 0.40, 0.10, "soft_smile", "")
EXP["nod"] = (-12, 6, 0.38, 0.10, "flat", "")

def crowd(c, xs, y, s, seed=0):
    for k, x in enumerate(xs):
        f_ = full(dict(BJv, tunic=["#4A4A3E", "#3E4A52", "#5A4A3A"][k % 3], hair=["#5A4A3A", "#7A6A4A", "#3A2E24"][k % 3]), "neutral", s, facing=1 if x < 960 else -1)
        draw(c, tinted(f_, "#1A120C"), x, y, 1.0, a=0.85)

def k1():
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    draw(c, blurred(place(P7.greathall(0.9)), 2), -384, -250, 1.4)          # koltuğa yakın kadraj
    RGsit = sprite(f'<g transform="translate(400,1000) scale(0.50)">{figure(RG, "front", "sit", ex("shock", IF.blink_at(0.3)), hands=("open", "open"))}</g>', 800, 1100, ax=400, ay=1000, ss=1.0)
    draw(c, RGsit, 960, 610, 1.0)                                       # jarl koltuğunda
    crowd(c, (200, 400, 1600, 1780), 1000, 0.78)
    q = 0.0 if t is None else ease_(lin_(t, 0, DUR[0] * 0.8))
    ASf = full(dict(ASLv, _body_extra=BELLY), ex("neutral", IF.blink_at(1.0)), 1.0, facing=-1, look=-0.3)
    with live(c, 1380, 1100, phase=1.0, breathe=0.004, ox=-90 * q, oy=-4 * abs(math.sin((t or 0) * 2.6))):
        rim(c, ASf, 1380, 1100, 1.0, "#FFD8A8", dx=-5, dy=-4, a=0.7)
        draw(c, ASf, 1380, 1100, 1.0)
    glow(c, 960, 900, 520, "#FF8A3A", 0.2)
    finish(c, cold=False, warm=0.04); return s

def k2():
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    draw(c, blurred(place(P7.greathall(0.9)), 7), 0, 0, 1.0)
    AS = fig_bust(dict(ASLv, _body_extra=BELLY), ex("demure", IF.blink_at(1.1)), 0.3, 1.5, h=1700)
    with live(c, 380, 1080, phase=1.1, breathe=0.004, rot=2.5 + 2.0 * (0 if t is None else ease_(lin_(t, CUE2.get("kabul", 99), CUE2.get("kabul", 99) + 0.6)))):  # başını eğer
        rim(c, AS, 380, 420, 1.0, "#FFB070", dx=-4, dy=3, a=0.55); draw(c, AS, 380, 420, 1.0)
    RGs = fig_bust(RG, ex("plead", IF.blink_at(0.3)), 1.0, 1.8)
    with live(c, 860, 1080, phase=0.3, breathe=0.006):
        rim(c, RGs, 860, 380, 1.0, "#FFB070", dx=4, dy=3, a=0.6); draw(c, RGs, 860, 380, 1.0)
        shade_side(c, RGs, 860, 380, 0.45, 1000, 600, "#1A0E08")
    LG = fig_bust(LAGv, ex("coldv", IF.blink_at(0.6)), 0.2, 2.05)
    with live(c, 1440, 1080, phase=0.6, breathe=0.005):
        rim(c, LG, 1440, 340, 1.0, "#FFB070", dx=-5, dy=3, a=0.6); draw(c, LG, 1440, 340, 1.0)
        shade_side(c, LG, 1440, 340, 0.55, 1300, 1800, "#1A0E08")
    finish(c, cold=False, warm=0.04); return s

def k3():
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    draw(c, place(O7.kattegat4()), 0, 0, 1.0)
    cart = svg_sprite(O7.defs(0.55) + O7.donkey_cart_rough(1440, 960, 0.6))
    draw(c, cart, 0, 0, 1.0)
    tie = 0.0 if t is None else ease_(lin_(t, 0.3, 1.6))
    LGf = full(dict(LAGv, _body_extra=SWORD), ex("coldv", IF.blink_at(0.6)), 0.98, look=0.4)
    RGf = full(RG, ex("nod", IF.blink_at(0.2)), 1.0, look=0.6)
    BJf = full(BJv, ex("torn", IF.blink_at(1.3)), 0.86, look=0.6)
    for sp_, x, y, ph in ((RGf, 360, 1120, 0.2), (BJf, 600, 1120, 1.3), (LGf, 1000, 1110, 0.6)):
        with live(c, x, y, phase=ph, breathe=0.005, oy=(-6 * tie if sp_ is LGf else 0)):
            rim(c, sp_, x, y, 1.0, "#E6F0FA", dx=4, dy=-4, a=0.7); draw(c, sp_, x, y, 1.0)
    snowfall(c, t, (0, 70, W, 1010), 50, seed=7)
    finish(c, cold=True); return s

def k4():
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    draw(c, blurred(place(O7.kattegat4()), 9), 0, 0, 1.0)
    k = 1.0 if t is None else ease_(lin_(t, 0.4, 1.4)) * (1 - ease_(lin_(t, 3.0, 3.8)))   # öpücük: Lagertha eğilir
    LG = fig_bust(dict(LAGv, _body_extra=SWORD), ex("kiss_closed" if k > 0.5 else "tenderv", IF.blink_at(0.6)), 0.9, 2.0)
    with live(c, 700, 1080, phase=0.6, breathe=0.005, rot=2 + 6 * k, ox=40 * k):
        rim(c, LG, 700, 380, 1.0, "#E6F0FA", dx=5, dy=-4, a=0.7); draw(c, LG, 700, 380, 1.0)
        shade_side(c, LG, 700, 380, 0.4, 580, 240)
    BJs = fig_bust(BJv, ex("kiss_closed" if k > 0.5 else "torn", IF.blink_at(1.3)), -0.5, 1.8, flip=True)
    with live(c, 1000, 1080, phase=1.3, breathe=0.005):                   # Bjorn önde, alnı annesinin dudağına
        rim(c, BJs, 1000, 600, 1.0, "#E6F0FA", dx=5, dy=-4, a=0.7); draw(c, BJs, 1000, 600, 1.0)
    snowfall(c, t, (0, 70, W, 1010), 40, seed=9)
    finish(c, cold=True); bloom_spot(c, 900, 470, 150, "#FFE8C8", 0.15); return s

def cart_riders(x, y, sc, bjorn=False, look_back=True):
    """Arabada oturan Lagertha (ve isteğe göre Bjorn): figürler arabanın ARKASINDA çizilir, bel altı kırpılır → oturuyor okunur."""
    lg = figure(LAGv, "front", "sit", "neutral")
    riders = f'<g transform="translate(-20,-150) scale(0.42)">{lg}</g>'
    if bjorn: riders = f'<g transform="translate(-130,-120) scale(0.37)">{figure(BJv, "front", "sit", "tenderv")}</g>' + riders
    return (f'<defs><clipPath id="rid"><rect x="-400" y="-900" width="800" height="{900-250}"/></clipPath></defs>'
            f'<g transform="translate({x},{y}) scale({sc})"><g clip-path="url(#rid)">{riders}</g></g>' + O7.donkey_cart_rough(x, y, sc))

def k5():
    """Araba patikadan sağa uzaklaşır, Lagertha arabada; Bjorn ardından koşar, yetişir ve annesinin yanına oturur."""
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    draw(c, place(O7.kattegat4()), 0, 0, 1.0)
    q = 0.55 if t is None else lin_(t, 0, DUR[0])                       # ham kare: koşu anı
    joined = q > 0.78
    cx = 1060 + 240 * q
    cart = svg_sprite(O7.defs(0.62) + cart_riders(1060, 990, 0.62, bjorn=joined))   # tek sprite, kaydırarak çizilir (bellek)
    draw(c, cart, cx - 1060, 0, 1.0)
    if not joined:   # Bjorn koşuyor: arabaya doğru, öne eğik, zıplayarak
        run = ease_(lin_(q, 0.0, 0.78))
        bx = 560 + (cx - 330 - 560) * run
        BJf = full(BJv, ex("torn", IF.blink_at(1.3)), 0.72, look=0.8)
        with live(c, bx, 1000, phase=1.3, breathe=0.0, rot=7, oy=-12 * abs(math.sin((t or 0) * 9))):
            rim(c, BJf, bx, 1000, 1.0, "#E6F0FA", dx=4, dy=-4, a=0.7); draw(c, BJf, bx, 1000, 1.0)
    RGs = fig_bust(RG, ex("nod", IF.blink_at(0.4)), 0.8, 2.15)
    nod = 0.0 if t is None else 2.5 * math.sin(math.pi * lin_(t, CUE2.get("onay", 99), CUE2.get("onay", 99) + 0.9))
    with live(c, 300, 1080, phase=0.4, breathe=0.006, rot=nod):
        rim(c, RGs, 300, 400, 1.0, "#E6F0FA", dx=6, dy=-4, a=0.8); draw(c, RGs, 300, 400, 1.0)
        shade_side(c, RGs, 300, 400, 0.5, 480, 80)
    snowfall(c, t, (0, 70, W, 1010), 50, seed=11)
    finish(c, cold=True); return s

def k6():
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    draw(c, blurred(place(P7.greathall(0.08)), 5), 0, 0, 1.0)
    ASf = full(dict(ASLv, _body_extra=BELLY), "neutral", 0.5, view="front")
    rim(c, ASf, 1060, 700, 1.0, "#FFB070", dx=0, dy=-4, a=0.5); draw(c, blurred(ASf, 2), 1060, 700, 1.0)
    die = 0.0 if t is None else lin_(t, 0, DUR[0])
    glow(c, 960, 880, 220, "#FF6A20", 0.14 * (1 - 0.7 * die))
    KR, KY = CUE2.get("kur", 99), CUE2.get("kayip", 99)
    crown = 0.0 if t is None else math.sin(math.pi * lin_(t, KR, KR + 1.6))             # "krallık kuruyorsun": koltuk bir an parlar
    shut = 0.0 if t is None else ease_(lin_(t, KY, KY + 2.4))                            # "aileyi kaybediyorsun": kapı kapanır
    glow(c, 1000, 520, 360, "#FFC070", 0.35 * crown)
    door = svg_sprite(big_door(1500, 1920, 120, snow=True))
    draw(c, door, 0, 0, 1.0); bloom_spot(c, 1720, 560, 480, "#C8DCF0", 0.5 * (1 - shut)); snowfall(c, t, (1520, 200, 1920, 1010), int(40 * (1 - shut)))
    if shut > 0:   # kapı kanadı soldan sağa kapanır, kalan ince ışık şeridi de söner
        c.drawRect(skia.Rect(1500, 0, 1500 + 420 * shut, H), skia.Paint(Color4f=col("#120C08", 1.0)))
        c.drawRect(skia.Rect(1500 + 420 * shut - 10, 0, 1500 + 420 * shut, H), skia.Paint(Color4f=col("#3A2C1E", 1.0)))
    RGs = fig_bust(RG, ex("hollow", IF.blink_at(0.9)), 0.9, 2.35)
    with live(c, 1180, 1080, phase=0.9, breathe=0.006):
        rim(c, RGs, 1180, 400, 1.0, "#DCEBFA", dx=7, dy=-4, a=0.85); draw(c, RGs, 1180, 400, 1.0)
        shade_side(c, RGs, 1180, 400, 0.6, 1400, 900)
    finish(c, cold=True); grade(c, "#9EB6CC", 0.08 + 0.1 * die, "multiply")
    if shut > 0:   # loş ışık daralır: Ragnar'ın yüzü çevresinde kapanan halka (yalnızlık)
        r = 1500 - 1180 * shut
        sh = skia.GradientShader.MakeRadial((1180, 420), r, [col("#000000", 0).toColor(), col("#000000", 0).toColor(), col("#000000", 0.96).toColor()], [0, 0.55, 1])
        c.drawRect(skia.Rect(0, 0, W, H), skia.Paint(Shader=sh))
        c.drawRect(skia.Rect(0, 0, W, H), skia.Paint(Color4f=col("#000000", 0.96 * max(0, shut - 0.55) / 0.45 * 0.0)))
        out_r = skia.Path(); out_r.addRect(skia.Rect(0, 0, W, H)); out_r.addCircle(1180, 420, r); out_r.setFillType(skia.PathFillType.kEvenOdd)
        c.drawPath(out_r, skia.Paint(Color4f=col("#000000", 0.96), AntiAlias=True))
    letterbox(c, 1.0, 70); return s

FR2 = {1: k1, 2: k2, 3: k3, 4: k4, 5: k5, 6: k6}

def contact2():
    from PIL import Image
    cw, ch = 960, 540; sheet = Image.new("RGB", (cw * 2 + 30, (ch + 20) * 3 + 10), "#EDE2CC")
    for k, i in enumerate(range(1, 7)):
        sheet.paste(Image.open(f"{OUT}/k2_{i}.png").convert("RGB").resize((cw, ch)), (10 + (k % 2) * (cw + 10), 10 + (k // 2) * (ch + 20)))
    sheet.save(f"{OUT}/kontakt2_960.png")

if __name__ == "__main__":
    ids = [int(a) for a in sys.argv[1:]] or list(range(1, 7))
    for i in ids:
        T[0] = None; FR2[i]().makeImageSnapshot().save(f"{OUT}/k2_{i}.png", skia.kPNG); print("kare", i)
    contact2()
