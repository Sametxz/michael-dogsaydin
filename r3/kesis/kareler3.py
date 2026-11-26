"""III · Keşiş bölümü: Sahne 11 (2 kare), Sahne 12 (4 kare), Sahne 14 (1 kare). Örgü onayı: kullanıcı 19.11 22:08.
Kural: mekânlar dolu, nesne ve doku bakımından zengin; R8 (kimlik tek kaynaktan), R9 (zemin altta), R10 (sert iklim tonu).
python3 kareler3.py [a1 a2 b1 b2 b3 b4 c1] → kesis/<id>.png, kontakt3_960.png
"""
import sys, math, random
sys.path[:0] = ["/home/claude/r3", "/home/claude/r2", "/home/claude/r3/veda", "/home/claude/r3/veda2", "/home/claude/r3/floki", "/home/claude/r3/ivar2", "/home/claude/r3/kurul/test_ivar"]
from kareler import *                        # live, ex, fig_bust, full, place, svg_sprite, shade_side, finish, RG, T, DUR, CUE2, snowfall
import puppet
from model_af import ATH, FLO, AXE
import obj7 as O7
OUT = "/home/claude/r3/kesis"
EXP["peace"] = (-6, 3, 0.92, 0.10, "soft_smile", "")
EXP["awe2"] = (-10, 6, 0.10, 0.04, "open_s", "")
EXP["talk"] = (-3, 2, 0.30, 0.08, "soft_smile", "")
EXP["listen"] = (-6, 3, 0.26, 0.08, "flat", "")
EXP["broken"] = (-16, 8, 0.50, 0.14, "tremble2", "tear")
ATHv = dict(ATH, no_blush=True)
FLOv = dict(FLO, no_blush=True)
INK = "#1A1410"

def cross_hand(x, y, s=1.0, glow_a=0.0):
    """Athelstan'ın avucunda tahta haç (kimlik nesnesi; model_af CROSS_S biçimiyle aynı)."""
    return (f'<g transform="translate({x},{y}) scale({s})">'
            f'<path d="M-40,30 Q-50,-10 -20,-26 Q10,-34 34,-16 Q48,4 40,30 Z" fill="#F0CCA8" stroke="{INK}" stroke-width="5"/>'
            f'<rect x="-7" y="-70" width="14" height="70" fill="#4A3424" stroke="{INK}" stroke-width="4"/><rect x="-24" y="-54" width="48" height="13" fill="#4A3424" stroke="{INK}" stroke-width="4"/>'
            f'<path d="M-30,-6 Q0,-20 30,-6" stroke="#F0CCA8" stroke-width="12" fill="none" stroke-linecap="round"/><path d="M-30,-6 Q0,-20 30,-6" stroke="{INK}" stroke-width="3" fill="none"/></g>')

def table_props():
    """Ocak başı masası: boynuz kadehler, testi, ekmek, tahta tabak, mum (ön plan)."""
    return (f'<g filter="url(#t_ahsap)"><path d="M520,1080 L600,900 L1320,900 L1400,1080 Z" fill="#5A4430"/></g><path d="M520,1080 L600,900 L1320,900 L1400,1080 Z" fill="none" stroke="{INK}" stroke-width="8"/>'
            f'<path d="M600,900 L1320,900" stroke="#7A5E40" stroke-width="10"/>'
            f'<path d="M700,900 Q712,840 760,826 L766,840 Q730,852 726,900 Z" fill="#D8C8A0" stroke="{INK}" stroke-width="5"/><path d="M1150,900 Q1160,846 1204,832 L1210,846 Q1176,858 1172,900 Z" fill="#D8C8A0" stroke="{INK}" stroke-width="5"/>'
            f'<path d="M880,900 Q870,850 900,830 L940,830 Q968,850 958,900 Z" fill="#8A5A3A" stroke="{INK}" stroke-width="5"/><path d="M900,830 Q920,816 940,830" stroke="{INK}" stroke-width="5" fill="none"/>'
            f'<ellipse cx="1040" cy="896" rx="80" ry="14" fill="#6A5038" stroke="{INK}" stroke-width="5"/><path d="M990,890 Q1010,862 1050,866 Q1080,872 1084,890 Z" fill="#B88A50" stroke="{INK}" stroke-width="4"/>'
            f'<rect x="806" y="850" width="18" height="50" fill="#E8DCC0" stroke="{INK}" stroke-width="4"/><path d="M815,850 Q808,830 815,816 Q822,830 815,850 Z" fill="#FFC060"/>')

def house_dressing():
    """Ev içini dolduran nesneler: asılı ot demetleri, kurutulmuş balık, kazan, çuval, balta, ağ."""
    o = []
    for x in (420, 470, 1500, 1550):
        o.append(f'<path d="M{x},230 L{x},280" stroke="#3A2A1A" stroke-width="3"/><path d="M{x-14},280 Q{x},340 {x+14},280 Z" fill="#6E7A4A" stroke="{INK}" stroke-width="3"/>')
    o.append(f'<path d="M260,620 Q300,560 360,560 Q420,560 440,620 L430,700 L270,700 Z" fill="#3A3A38" stroke="{INK}" stroke-width="6" filter="url(#t_metal)"/>'
             f'<path d="M250,620 L450,620" stroke="{INK}" stroke-width="10"/>'
             f'<path d="M1620,700 Q1600,620 1660,600 Q1720,620 1700,700 Z" fill="#9A8A64" stroke="{INK}" stroke-width="5"/><path d="M1640,612 Q1660,590 1690,612" stroke="#6A5A3A" stroke-width="5" fill="none"/>'
             f'<path d="M1720,300 l70,-30 M1790,270 q24,30 -6,56 q-24,-12 6,-56" stroke="{INK}" stroke-width="8" fill="#8A8A86"/>'
             + "".join(f'<path d="M{1480+k*22},420 l0,{40+k%3*10}" stroke="#7A6A4A" stroke-width="3"/>' for k in range(8))
             + f'<path d="M1470,420 L1660,420" stroke="#3A2A1A" stroke-width="6"/>')
    return "".join(o)

def warm_room(fire=1.0, blur=3):
    return blurred(place(P.longhouse(fire) + house_dressing()), blur)

# ------------------------------------------------------------------ Sahne 11 · Kare 1: ocak başı sohbet
def a1():
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    draw(c, warm_room(1.0, 4), 0, 0, 1.0)
    RGs = fig_bust(RG, ex("listen", IF.blink_at(0.5)), 0.9, 1.9)
    with live(c, 520, 1080, phase=0.5, breathe=0.006, sway=0.3):
        rim(c, RGs, 520, 420, 1.0, "#FFB070", dx=5, dy=2, a=0.6); draw(c, RGs, 520, 420, 1.0)
        shade_side(c, RGs, 520, 420, 0.5, 700, 260, "#1A0E08")
    AT = fig_bust(ATHv, ex("talk", IF.blink_at(1.4)), -0.6, 1.85, flip=True)
    with live(c, 1400, 1080, phase=1.4, breathe=0.005, sway=0.6):
        rim(c, AT, 1400, 430, 1.0, "#FFB070", dx=-5, dy=2, a=0.6); draw(c, AT, 1400, 430, 1.0)
        shade_side(c, AT, 1400, 430, 0.5, 1260, 1700, "#1A0E08")
    hand = svg_sprite(cross_hand(1250, 900, 0.9))
    draw(c, hand, 0, 0, 1.0)
    props = svg_sprite("<defs>" + tex.TEX["ahsap"] + "</defs>" + table_props())
    draw(c, props, 0, 0, 1.0)
    glow(c, 960, 1000, 560, "#FF8A3A", 0.3); bloom_spot(c, 1290, 790, 70, "#FFE0A0", 0.35)
    finish(c, cold=False, warm=0.05); return s

# ------------------------------------------------------------------ Sahne 11 · Kare 2: nehirde ışık
def a2():
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    draw(c, place(P.riverbank()), 0, 0, 1.0)
    AT = fig_bust(ATHv, ex("awe2", IF.blink_at(0.8)), 0.9, 1.7)
    with live(c, 980, 1080, phase=0.8, breathe=0.005, oy=4 * math.sin((t or 0) * 1.2)):
        rim(c, AT, 980, 470, 1.0, "#FFF6DC", dx=0, dy=-7, a=0.95); draw(c, AT, 980, 470, 1.0)
    hand = svg_sprite(cross_hand(1080, 760, 0.9))
    draw(c, hand, 0, 0, 1.0)
    water = svg_sprite('<defs><linearGradient id="wv" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8EA6BA" stop-opacity="0.92"/><stop offset="1" stop-color="#3E5466"/></linearGradient></defs>'
                       '<path d="M0,830 Q480,816 960,826 Q1440,836 1920,820 L1920,1080 L0,1080 Z" fill="url(#wv)"/>'
                       + "".join(f'<path d="M{x},{y} q40,-6 90,0" stroke="#E6EEF4" stroke-width="3" fill="none" opacity="0.7"/>' for x, y in [(random.Random(k).uniform(0, 1900), random.Random(k + 5).uniform(840, 1060)) for k in range(36)])
                       + '<ellipse cx="980" cy="832" rx="220" ry="16" fill="none" stroke="#F0F6FA" stroke-width="4" opacity="0.8"/>')
    draw(c, water, 0, 0, 1.0)
    light_shaft(c, 1000, 160, 980, 520, "#FFF4D8", 0.32, t=t or 0, y_top=-60, y_bot=900)
    bloom_spot(c, 1000, 120, 420, "#FFF6E0", 0.6); bloom_spot(c, 1080, 700, 90, "#FFE6B0", 0.45)
    fog(c, t or 0, 720, "#E6ECF0", 0.35, seed=4, speed=10)
    finish(c, cold=True); bloom_spot(c, 1000, 400, 260, "#FFF0D0", 0.18); return s

# ------------------------------------------------------------------ Sahne 12 · Kare 1: dua ve kapıdaki gölge
AXE_HAND = ('<g transform="translate(HX,HY)"><path d="M10,40 L-50,-240" stroke="#1A1410" stroke-width="18" stroke-linecap="round"/><path d="M10,40 L-50,-240" stroke="#6A5038" stroke-width="10" stroke-linecap="round"/>'
            '<path d="M-46,-226 Q20,-280 50,-200 Q10,-196 -30,-180 Z" fill="#A8B0B8" stroke="#1A1410" stroke-width="5"/><path d="M30,-246 Q48,-226 46,-206" stroke="#E8EEF2" stroke-width="3" fill="none"/></g>')
def kneel_ath(expr="peace", s_=1.0):   # model gövdesiyle diz çökmüş, elleri göğüste (dua) — puppet gövdesi KULLANILMAZ
    return full(dict(ATHv, _kneel=130, _carry_svg="<g/>"), expr, s_, look=0.6)
KB = None
def altar():
    return (f'<g filter="url(#t_ahsap)"><rect x="1500" y="560" width="300" height="40" fill="#5A4430"/><rect x="1520" y="600" width="24" height="200" fill="#4A3826"/><rect x="1756" y="600" width="24" height="200" fill="#4A3826"/></g>'
            f'<rect x="1500" y="560" width="300" height="40" fill="none" stroke="{INK}" stroke-width="6"/>'
            f'<rect x="1636" y="420" width="28" height="140" fill="#4A3424" stroke="{INK}" stroke-width="5"/><rect x="1600" y="456" width="100" height="24" fill="#4A3424" stroke="{INK}" stroke-width="5"/>'   # oyma haç
            + "".join(f'<rect x="{x}" y="520" width="16" height="40" fill="#E8DCC0" stroke="{INK}" stroke-width="3"/><path d="M{x+8},520 Q{x},500 {x+8},486 Q{x+16},500 {x+8},520 Z" fill="#FFC060"/>' for x in (1530, 1740))
            + f'<path d="M1560,560 Q1590,540 1620,560" stroke="#C8B89A" stroke-width="4" fill="none"/>')

def b1():
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    draw(c, blurred(place(P.longhouse(0.25) + house_dressing() + altar()), 2), 0, 0, 1.0)
    c.drawRect(skia.Rect(0, 0, W, H), skia.Paint(Color4f=col("#05040A", 0.35)))
    door = svg_sprite(big_door(240, 600, 160, snow=True))
    draw(c, door, 0, 0, 1.0); bloom_spot(c, 420, 560, 360, "#B8D4F0", 0.4)
    fl = full(dict(FLOv, _body_extra=AXE), "neutral", 0.92, look=0.8)
    step = 0.0 if t is None else ease_(lin_(t, 0.4, DUR[0]))
    draw(c, tinted(fl, "#0A0C12"), 420 + 160 * step, 1010, 1.0)
    rim(c, fl, 420 + 160 * step, 1010, 1.0, "#CFE4FF", dx=-4, dy=-3, a=0.9); draw(c, tinted(fl, "#0A0C12"), 420 + 160 * step, 1010, 1.0)
    axe = svg_sprite(f'<g transform="translate({480 + 160 * step:.0f},780)" fill="#0A0C12"><path d="M0,0 L60,-300" stroke="#0A0C12" stroke-width="16" stroke-linecap="round"/>'
                     f'<path d="M52,-290 Q130,-330 140,-240 Q100,-250 60,-230 Z"/><path d="M52,-290 Q130,-330 140,-240" stroke="#CFE4FF" stroke-width="4" fill="none" opacity="0.9"/></g>')
    draw(c, axe, 0, 0, 1.0)
    kb = kneel_ath("peace", 1.15)
    with live(c, 1300, 1010, phase=0.2, breathe=0.004):
        rim(c, kb, 1300, 1010, 1.0, "#FFC070", dx=5, dy=-2, a=0.6); draw(c, kb, 1300, 1010, 1.0)
    glow(c, 1650, 520, 300, "#FFB060", 0.35); bloom_spot(c, 1530, 490, 50, "#FFE0A0", 0.5); bloom_spot(c, 1748, 490, 50, "#FFE0A0", 0.5)
    finish(c, cold=True); return s

# ------------------------------------------------------------------ Sahne 12 · Kare 2: baltanın gölgesi, huzur
def b2():
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    draw(c, blurred(place(P.longhouse(0.25) + house_dressing() + altar()), 9), -500, -80, 1.15)
    AT = fig_bust(ATHv, ex("peace", False), 0.6, 2.3)
    with live(c, 900, 1080, phase=0.3, breathe=0.004):
        rim(c, AT, 900, 420, 1.0, "#FFC070", dx=6, dy=0, a=0.7); draw(c, AT, 900, 420, 1.0)
        shade_side(c, AT, 900, 420, 0.5, 1050, 650, "#120A06")
    rise = 1.0 if t is None else ease_(lin_(t, 0.2, 2.2))                # baltanın gölgesi yükselir ve üstüne düşer
    sh = svg_sprite(f'<g transform="translate({-200 + 260*rise:.0f},{160 - 120*rise:.0f}) rotate({-30 + 25*rise:.0f} 400 700)">'
                    f'<path d="M380,1100 L420,1100 L440,380 L404,380 Z" fill="#000"/><path d="M430,400 Q560,330 600,460 Q520,440 440,470 Z" fill="#000"/></g>')
    draw(c, sh, 0, 0, 1.0, a=0.55)
    glow(c, 1500, 500, 480, "#FFB060", 0.25)
    finish(c, cold=True); return s

# ------------------------------------------------------------------ Sahne 12 · Kare 3: beyaz flaş, duvarda iki siluet
def sil_floki(x, y, s=1.0, raise_=1.0):
    a = -20 - 70 * raise_          # kol açısı (derece)
    ax = math.cos(math.radians(a)); ay = math.sin(math.radians(a))
    hx, hy = 30 + 170 * ax, -560 + 170 * ay
    return (f'<g transform="translate({x},{y}) scale({s})" fill="#16120E">'
            f'<circle cx="10" cy="-640" r="62"/><path d="M-30,-700 Q-60,-740 -20,-760 Q10,-720 0,-700 Z"/>'           # baş + tepe saçı
            f'<path d="M-60,-580 Q10,-610 70,-580 L80,-300 Q10,-280 -60,-300 Z"/>'                                     # gövde
            f'<path d="M-50,-300 L-90,0 L-40,0 L0,-260 L40,0 L90,0 L60,-300 Z"/>'                                      # bacaklar
            f'<path d="M30,-560 L{hx:.0f},{hy:.0f}" stroke="#16120E" stroke-width="46" stroke-linecap="round"/>'        # kollar
            f'<path d="M{hx:.0f},{hy:.0f} L{hx + 260*ax:.0f},{hy + 260*ay:.0f}" stroke="#16120E" stroke-width="18" stroke-linecap="round"/>'   # sap
            f'<g transform="translate({hx + 250*ax:.0f},{hy + 250*ay:.0f}) rotate({a + 90:.0f})"><path d="M-10,-20 Q-90,-40 -100,40 Q-50,20 -10,30 Z"/></g></g>')

def sil_athelstan(x, y, s=1.0):
    return (f'<g transform="translate({x},{y}) scale({s})" fill="#16120E">'
            f'<circle cx="60" cy="-420" r="58"/>'
            f'<path d="M-40,-370 Q40,-400 90,-360 L100,-160 L-60,-150 Z"/>'
            f'<path d="M-80,-160 L120,-160 L130,-60 Q150,0 60,0 L-120,0 Q-160,-40 -80,-160 Z"/>'
            f'<path d="M90,-330 L150,-300 L150,-250" stroke="#16120E" stroke-width="36" stroke-linecap="round" fill="none"/></g>')

def b3():
    s = skia.Surface(W, H); c = s.getCanvas()
    c.drawRect(skia.Rect(0, 0, W, H), skia.Paint(Color4f=col("#F4F1EA")))
    wall = svg_sprite("<defs>" + tex.TEX["ahsap"] + "</defs>" + "".join(f'<rect x="{x}" y="0" width="64" height="1080" fill="#EAE4D8" filter="url(#t_ahsap)" opacity="0.5"/>' for x in range(0, 1920, 64)))
    draw(c, wall, 0, 0, 1.0)
    t = T[0]; r = 1.0 if t is None else ease_(lin_(t, 0.0, 0.5))
    fl = full(dict(FLOv, _arm_up=True, _hand_extra=AXE_HAND), "neutral", 0.95, look=0.8)   # gölge: model gövdesi + kalkık kol ve balta
    kb = kneel_ath("peace", 1.1)
    # R12: siluet yerine gerçek modeller — beyaz flaşın içinde aşırı pozlanmış, renkleri solmuş
    for sp_, x in ((fl, 760), (kb, 1240)):
        draw(c, sp_, x, 1060, 1.0)
    c.drawRect(skia.Rect(0, 0, W, H), skia.Paint(Color4f=col("#FFFFFF", 0.42)))
    grade(c, "#E8E0D0", 0.25, "color")
    vignette(c, 0.4); letterbox(c, 1.0, 70); return s

# ------------------------------------------------------------------ Sahne 12 · Kare 4: Ragnar kapıda, yerde haç
def b4():
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    draw(c, blurred(place(P.longhouse(0.15) + house_dressing() + altar()), 5), 0, 0, 1.0)
    c.drawRect(skia.Rect(0, 0, W, H), skia.Paint(Color4f=col("#05060C", 0.4)))
    floor = svg_sprite(f'<path d="M0,900 L1920,900 L1920,1080 L0,1080 Z" fill="#2A2018"/>'
                       f'<g transform="translate(1180,960) rotate(-28) scale(1.35)"><rect x="-8" y="-70" width="16" height="80" fill="#4A3424" stroke="{INK}" stroke-width="4"/><rect x="-28" y="-52" width="56" height="15" fill="#4A3424" stroke="{INK}" stroke-width="4"/>'
                       f'<path d="M0,-70 Q-60,-120 -140,-110" stroke="#6A4A30" stroke-width="4" fill="none"/></g>'
                       f'<path d="M1300,1080 Q1360,990 1520,980 Q1700,980 1800,1080 Z" fill="#5A4E40" stroke="{INK}" stroke-width="6"/>')    # pelerin ucu (beden kadraj dışında)
    draw(c, floor, 0, 0, 1.0)
    sink = 0.0 if t is None else ease_(lin_(t, CUE2.get("cok", 1.0), CUE2.get("cok", 1.0) + 1.0))   # dizlerinin üstüne çöker
    RGs = fig_bust(RG, ex("broken", IF.blink_at(0.6)), 0.95, 2.1)
    with live(c, 640, 1080, phase=0.6, breathe=0.008, oy=120 * sink, rot=3 * sink):
        rim(c, RGs, 640, 380, 1.0, "#CFE4FF", dx=-6, dy=-4, a=0.85); draw(c, RGs, 640, 380, 1.0)
        shade_side(c, RGs, 640, 380, 0.55, 760, 380)
    bloom_spot(c, 1180, 940, 80, "#E8F0F8", 0.3)
    finish(c, cold=True); grade(c, "#8AA6C8", 0.12, "multiply"); letterbox(c, 1.0, 70); return s

# ------------------------------------------------------------------ Sahne 14 · yorum çağrısı
def c1():
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    rb = P.riverbank()
    mound = (f'<path d="M560,900 Q760,700 960,690 Q1180,700 1360,900 Z" fill="#4A4034" stroke="{INK}" stroke-width="8"/>'
             f'<path d="M640,860 Q800,740 960,734 Q1100,738 1260,850 Q1100,800 960,796 Q800,800 640,860 Z" fill="#E6ECF2" opacity="0.9"/>'
             + "".join(f'<ellipse cx="{x}" cy="{y}" rx="{r}" ry="{r*0.6:.0f}" fill="#7A766E" stroke="{INK}" stroke-width="4"/>' for x, y, r in ((660, 880, 28), (760, 820, 22), (1200, 860, 26), (1290, 890, 30), (900, 900, 20)))
             + f'<g transform="translate(960,700)"><rect x="-14" y="-240" width="28" height="250" fill="#4A3424" stroke="{INK}" stroke-width="6"/><rect x="-80" y="-190" width="160" height="26" fill="#4A3424" stroke="{INK}" stroke-width="6"/>'
             f'<path d="M-14,-240 L14,-240" stroke="#E6ECF2" stroke-width="10"/><path d="M-80,-190 L80,-190" stroke="#E6ECF2" stroke-width="8"/></g>')
    draw(c, place(rb + mound), 0, 0, 1.0)
    fog(c, t or 0, 700, "#DDE4EA", 0.4, seed=8, speed=10)
    snowfall(c, t, (0, 70, W, 1010), 120, seed=5)
    finish(c, cold=True)
    card = svg_sprite('<rect x="460" y="120" width="1000" height="150" rx="14" fill="#0E1218" opacity="0.72"/>'
                      '<text x="960" y="190" text-anchor="middle" font-family="Pirata One" font-size="64" fill="#EDE2CC">Sırada hangi karakter doğsun?</text>'
                      '<text x="960" y="246" text-anchor="middle" font-family="Alegreya SC" font-size="36" fill="#C9A25A">Yorumlara yaz</text>')
    a = 1.0 if t is None else ease_(lin_(t, 0.6, 1.4))
    draw(c, card, 0, 0, 1.0, a=a)
    return s

FR3 = {"a1": a1, "a2": a2, "b1": b1, "b2": b2, "b3": b3, "b4": b4, "c1": c1}
import tex

def contact3(ids=("a1", "a2", "b1", "b2", "b3", "b4", "c1")):
    from PIL import Image
    cw, ch = 960, 540; rows = (len(ids) + 1) // 2; sheet = Image.new("RGB", (cw * 2 + 30, (ch + 20) * rows + 10), "#EDE2CC")
    for k, i in enumerate(ids):
        sheet.paste(Image.open(f"{OUT}/{i}.png").convert("RGB").resize((cw, ch)), (10 + (k % 2) * (cw + 10), 10 + (k // 2) * (ch + 20)))
    sheet.save(f"{OUT}/kontakt3_960.png")

if __name__ == "__main__":
    ids = sys.argv[1:] or list(FR3)
    for i in ids:
        T[0] = None; FR3[i]().makeImageSnapshot().save(f"{OUT}/{i}.png", skia.kPNG); print("kare", i)
    contact3()
