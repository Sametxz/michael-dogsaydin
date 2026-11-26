"""II · Bedel: Sahne 6 (veba, 3 kare), 8 (Rollo, 2 kare), 10 (Horik, 3 kare). Örgü + model onayı: 19.11 23:00.
R8/R9/R10/R11: kimlik tek kaynaktan, zemin altta, sert iklim tonu, gövde ve gölgeler model gövdesinden.
python3 kareler4.py [d1..d8] → bedel/<id>.png, kontakt4_960.png
"""
import sys, math, random
sys.path[:0] = ["/home/claude/r3", "/home/claude/r2", "/home/claude/r3/veda", "/home/claude/r3/veda2", "/home/claude/r3/kesis", "/home/claude/r3/bedel",
                "/home/claude/r3/floki", "/home/claude/r3/ivar2", "/home/claude/r3/kurul/test_ivar"]
from kareler3 import *            # veda2/kareler + yardımcılar, house_dressing, warm_room, ATHv, FLOv
from modeller import ROLLO, HORIK, BORG, GYDA
from art3 import head3, figure
import assets as A
import places7 as P7
import kalabalik as KL
import tex
OUT = "/home/claude/r3/bedel"
EXP["sick"] = (-6, 3, 0.94, 0.12, "flat", "")
EXP["dread_l"] = (-14, 8, 0.26, 0.08, "tremble", "")
EXP["stone"] = (-12, 6, 0.40, 0.12, "flat", "")
EXP["sly"] = (6, -2, 0.42, 0.10, "smirk", "")
EXP["shame_r"] = (-10, 5, 0.70, 0.12, "flat", "")
EXP["fierce"] = (12, -5, 0.22, 0.06, "grit", "")
LAGv2 = dict(LAGv)
INK = "#1A1410"
SWORD_DOWN = ('<g transform="translate(HX,HY)"><path d="M0,0 L40,250" stroke="#1A1410" stroke-width="16" stroke-linecap="round"/><path d="M0,0 L40,250" stroke="#B8C0C8" stroke-width="9" stroke-linecap="round"/>'
              '<path d="M-24,-6 L26,6" stroke="#1A1410" stroke-width="12" stroke-linecap="round"/><path d="M-24,-6 L26,6" stroke="#8A7A5A" stroke-width="6" stroke-linecap="round"/></g>')
TORCH = ('<g transform="translate(HX,HY)"><path d="M0,30 L-10,-120" stroke="#1A1410" stroke-width="18" stroke-linecap="round"/><path d="M0,30 L-10,-120" stroke="#5A4028" stroke-width="10" stroke-linecap="round"/>'
         '<path d="M-30,-120 Q-20,-200 -6,-230 Q8,-190 16,-120 Z" fill="#F08A2A" stroke="#1A1410" stroke-width="3"/><path d="M-16,-124 Q-10,-170 -4,-186 Q4,-160 6,-124 Z" fill="#FFD27A"/></g>')
HORN_UP = ('<g transform="translate(HX,HY)"><path d="M-10,10 Q-30,-60 10,-110 L22,-100 Q-6,-56 12,8 Z" fill="#D8C8A0" stroke="#1A1410" stroke-width="5"/><path d="M8,-108 l14,10" stroke="#B08A3A" stroke-width="6"/></g>')
DAGGER_UP = ('<g transform="translate(HX,HY)"><path d="M0,10 L-6,-150" stroke="#1A1410" stroke-width="12" stroke-linecap="round"/><path d="M-2,-40 L-6,-150" stroke="#C8D0D8" stroke-width="7"/><path d="M-22,-36 L18,-40" stroke="#1A1410" stroke-width="10"/></g>')

def bed_with_gyda(x, y, s=1.0, pale=True):
    """Kürklü yatakta yatan Gyda: model başı (GYDA) yatay, yastıkta; gövde kürk örtü altında."""
    g = dict(GYDA, skin="#E8D4C4" if pale else GYDA["skin"])
    return (f'<g transform="translate({x},{y}) scale({s})">'
            f'<g filter="url(#t_ahsap)"><rect x="-420" y="0" width="840" height="120" fill="#4A3826"/></g><rect x="-420" y="0" width="840" height="120" fill="none" stroke="{INK}" stroke-width="7"/>'
            f'<ellipse cx="-300" cy="-20" rx="130" ry="56" fill="#D8CDB8" stroke="{INK}" stroke-width="6"/>'                                   # yastık
            f'<g transform="translate(-290,-90) rotate(-78) scale(0.95)">{head3(g, "3q", "sick", 0.2)}</g>'
            f'<g filter="url(#t_kurk)"><path d="M-220,-100 Q0,-150 410,-80 L420,10 L-230,10 Q-250,-50 -220,-100 Z" fill="#8A7A62"/></g>'
            f'<path d="M-220,-100 Q0,-150 410,-80 L420,10 L-230,10 Q-250,-50 -220,-100 Z" fill="none" stroke="{INK}" stroke-width="6"/>'
            + "".join(f'<path d="M{-180 + k*42},{-104 + (k%3)*4} q8,16 0,30" stroke="#5A4A38" stroke-width="4" fill="none"/>' for k in range(14))
            + '</g>')

def kid_hand(x, y, s=1.0):
    return (f'<g transform="translate({x},{y}) scale({s})"><path d="M-10,0 Q-30,-14 -18,-30 Q0,-36 16,-22 Q24,-6 14,6 Z" fill="#E8D4C4" stroke="{INK}" stroke-width="4"/>'
            + "".join(f'<path d="M{-14 + k*8},-28 l2,-12" stroke="{INK}" stroke-width="7" stroke-linecap="round"/><path d="M{-14 + k*8},-28 l2,-12" stroke="#E8D4C4" stroke-width="4" stroke-linecap="round"/>' for k in range(4)) + '</g>')

def sick_room(fire=0.35, blur=4):
    return blurred(place(P.longhouse(fire) + house_dressing()), blur)

def candle(c, x, y, t, out_at=None):
    lit = 1.0 if (t is None or out_at is None) else 1 - lin_(t, out_at, out_at + 0.25)
    c.drawRect(skia.Rect(x - 9, y, x + 9, y + 60), skia.Paint(Color4f=col("#E8DCC0"), AntiAlias=True))
    c.drawRect(skia.Rect(x - 9, y, x + 9, y + 60), skia.Paint(Color4f=col(INK), Style=skia.Paint.kStroke_Style, StrokeWidth=3))
    if lit > 0.02:
        fl = 1 + 0.12 * math.sin((t or 0) * 13) + 0.06 * math.sin((t or 0) * 29)
        p = skia.Path(); p.moveTo(x, y); p.quadTo(x - 9, y - 18 * fl, x, y - 34 * fl); p.quadTo(x + 9, y - 18 * fl, x, y); c.drawPath(p, skia.Paint(Color4f=col("#FFC060", lit), AntiAlias=True))
        glow(c, x, y - 20, 260, "#FFB060", 0.32 * lit * fl)
    elif out_at is not None and t is not None:   # duman ipliği
        q = lin_(t, out_at + 0.25, out_at + 2.5)
        bloom_spot(c, x + 10 * math.sin(q * 6), y - 40 - 120 * q, 20 + 30 * q, "#B8B8B8", 0.25 * (1 - q))

# ------------------------------------------------------------------ 6/1 · veba: Lagertha hasta Gyda'nın başında
def d1():
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    draw(c, sick_room(0.3, 4), 0, 0, 1.0)
    win = svg_sprite('<rect x="1560" y="250" width="180" height="230" fill="#9AA8B4"/><rect x="1560" y="250" width="180" height="230" fill="none" stroke="#1A1410" stroke-width="18"/>'
                     '<path d="M1650,250 L1650,480 M1560,365 L1740,365" stroke="#1A1410" stroke-width="10"/>')
    draw(c, win, 0, 0, 1.0); fog(c, t or 0, 360, "#DDE4EA", 0.35, seed=3, speed=8)
    bed = svg_sprite("<defs>" + tex.TEX["ahsap"] + tex.TEX["kurk"] + "</defs>" + bed_with_gyda(1220, 860, 1.0))
    draw(c, bed, 0, 0, 1.0)
    LG = fig_bust(LAGv2, ex("dread_l", IF.blink_at(0.7)), 0.9, 2.0)
    with live(c, 560, 1080, phase=0.7, breathe=0.007, rot=4):
        rim(c, LG, 560, 400, 1.0, "#FFB070", dx=5, dy=2, a=0.55); draw(c, LG, 560, 400, 1.0)
        shade_side(c, LG, 560, 400, 0.5, 720, 300, "#140A06")
    candle(c, 860, 780, t)
    finish(c, cold=True); grade(c, "#7E8A7A", 0.12, "multiply"); letterbox(c, 1.0, 70); return s

# ------------------------------------------------------------------ 6/2 · Ragnar Gyda'nın elini tutuyor, mum söner
def d2():
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    draw(c, sick_room(0.2, 6), -200, 0, 1.0)
    bed = svg_sprite("<defs>" + tex.TEX["ahsap"] + tex.TEX["kurk"] + "</defs>" + bed_with_gyda(1240, 900, 1.15))
    draw(c, bed, 0, 0, 1.0)
    RGs = fig_bust(RG, ex("broken", IF.blink_at(0.5)), 0.95, 2.1, noarm=True)
    with live(c, 520, 1080, phase=0.5, breathe=0.008, rot=5):
        rim(c, RGs, 520, 400, 1.0, "#FFB070", dx=5, dy=2, a=0.55); draw(c, RGs, 520, 400, 1.0)
        shade_side(c, RGs, 520, 400, 0.5, 680, 300, "#140A06")
    arm = svg_sprite(f'{A.defs(0.7)}<g transform="translate(560,960) rotate(-12) scale(0.7)">{A.arm(index_out=False, s=0.7, lw=10)}</g>{kid_hand(1000, 862, 1.3)}')
    draw(c, arm, 0, 0, 1.0)
    candle(c, 1500, 720, t, CUE2.get("mum", None))
    finish(c, cold=True); grade(c, "#7E8A7A", 0.10, "multiply"); letterbox(c, 1.0, 70); return s

# ------------------------------------------------------------------ 6/3 · cenaze ateşi
def pyre_svg(x, y, s=1.0):
    o = [f'<g transform="translate({x},{y}) scale({s})">']
    for k in range(6):
        yy = -k * 34
        o.append(f'<g filter="url(#t_ahsap)"><rect x="{-230 + k*14}" y="{yy-30}" width="{460 - k*28}" height="30" rx="14" fill="#5A4430"/></g><rect x="{-230 + k*14}" y="{yy-30}" width="{460 - k*28}" height="30" rx="14" fill="none" stroke="{INK}" stroke-width="5"/>')
    o.append(f'<path d="M-150,-206 Q0,-250 150,-206 Q150,-180 0,-178 Q-150,-180 -150,-206 Z" fill="#D8CDB8" stroke="{INK}" stroke-width="6"/>'   # kefen
             f'<path d="M-100,-212 Q-60,-226 -20,-212 M30,-214 Q70,-226 110,-212" stroke="#A89C84" stroke-width="4" fill="none"/></g>')
    return "".join(o)

def d3():
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    draw(c, place(O7.kattegat4()), 0, 0, 1.0)
    c.drawRect(skia.Rect(0, 0, W, H), skia.Paint(Color4f=col("#05070E", 0.66)))
    YAK = CUE2.get("yak", 99); burn = 0.5 if t is None else ease_(lin_(t, YAK, YAK + 2.0))
    # arka sıra: meşaleli Kattegat halkı (model gövdeleri, rastgele türetme)
    for k in range(9):
        r = random.Random(40 + k); side = -1 if k < 5 else 1; x = (170 + k * 90) if k < 5 else (1330 + (k - 5) * 120)
        sp = full(KL.soldier_spec(20 + k % 4, "ragnar", torch=True), "stone", 0.62, facing=-side, look=0.5)
        draw(c, sp, x, 820 + r.uniform(-8, 8), 1.0, a=0.95)
        glow(c, x - 6 * side, 820 - 0.62 * 900, 90, "#FFB060", 0.35)
    pyre = svg_sprite(O7.defs() + KL.pyre_grand(960, 900, 0.9))
    draw(c, pyre, 0, 0, 1.0)
    if burn > 0.01:
        for layer, (colr, sc_, a_) in enumerate((("#C8401A", 1.0, 0.85), ("#F08A2A", 0.75, 0.9), ("#FFD27A", 0.45, 0.95))):
            for j in range(15):
                r_ = random.Random(j * 7 + layer); fl = 0.75 + 0.25 * math.sin((t or 0) * (7 + j % 3) + j * 1.9)
                x = 660 + j * 43 + r_.uniform(-10, 10); base = 880 - r_.uniform(0, 120) * burn - 200 * max(0, burn - 0.6)
                hh = (120 + 90 * r_.random()) * burn * fl * sc_; w_ = 28 * sc_ + 6
                p = skia.Path(); p.moveTo(x - w_, base); p.cubicTo(x - w_, base - hh * 0.5, x - w_ * 0.2, base - hh * 0.7, x + 6 * math.sin((t or 0) * 5 + j), base - hh)
                p.cubicTo(x + w_ * 0.3, base - hh * 0.65, x + w_, base - hh * 0.45, x + w_, base); p.close()
                c.drawPath(p, skia.Paint(Color4f=col(colr, a_ * burn), AntiAlias=True))
        for j in range(40):
            q = (((t or 0) * 0.35 + j / 40) % 1.0); r = random.Random(j)
            c.drawCircle(960 + r.uniform(-260, 260) + 40 * math.sin(q * 5 + j), 620 - 560 * q, 3.5 * (1 - q), skia.Paint(Color4f=col("#FFC070", 0.9 * (1 - q) * burn), AntiAlias=True))
        bloom_spot(c, 960, 200, 260, "#6A6460", 0.3 * burn)                       # duman sütunu
    glow(c, 960, 640, 760, "#FF7A30", 0.15 + 0.35 * burn)
    # Lagertha meşaleyle yığına yürür; "yakıyor"da meşaleyi uzatır
    walk = 1.0 if t is None else ease_(lin_(t, 0.0, YAK))
    LGf = full(dict(LAGv2, _arm_up=True, _hand_extra=KL.TORCH2), ex("stone", IF.blink_at(0.6)), 0.95, facing=-1, look=-0.7) if False else full(dict(LAGv2, _arm_up=True, _hand_extra=KL.TORCH2), ex("stone", IF.blink_at(0.6)), 0.95, look=0.7)
    lx = 380 + 260 * walk
    with live(c, lx, 1110, phase=0.6, breathe=0.006, oy=-5 * abs(math.sin((t or 0) * 3)) * (1 - walk)):
        rim(c, LGf, lx, 1110, 1.0, "#FFA050", dx=5, dy=-2, a=0.9); draw(c, LGf, lx, 1110, 1.0)
    RGf = full(RG, ex("broken", IF.blink_at(0.2)), 1.0, facing=-1, look=-0.9) if False else full(RG, ex("broken", IF.blink_at(0.2)), 1.0, look=0.9)
    BJf = full(BJv, ex("torn", IF.blink_at(1.3)), 0.82, look=0.9)
    for sp_, x, y, ph in ((RGf, 1430, 1130, 0.2), (BJf, 1620, 1130, 1.3)):
        with live(c, x, y, phase=ph, breathe=0.006):
            rim(c, sp_, x, y, 1.0, "#FFA050", dx=-5, dy=-2, a=0.85); draw(c, sp_, x, y, 1.0)
    finish(c, cold=False, warm=0.06); return s

# ------------------------------------------------------------------ 8/1 · savaş alanı, Rollo karşı safta
def field():
    o = ['<defs><linearGradient id="fs" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7E8C98"/><stop offset="1" stop-color="#B8C2CA"/></linearGradient></defs>',
         '<rect width="1920" height="1080" fill="url(#fs)"/>',
         '<path d="M0,520 L300,430 L620,500 L980,410 L1320,490 L1640,420 L1920,480 L1920,640 L0,640 Z" fill="#6A7680"/>',
         '<path d="M0,600 Q960,570 1920,600 L1920,1080 L0,1080 Z" fill="#4A5038"/>']
    o.append(O7.ground2(1920, 1080, 640, seed=5))
    for row, (y, sc, n, c1) in enumerate(((610, 0.30, 26, "#3A3E44"), (640, 0.38, 22, "#2E3238"))):   # uzak kalkan duvarı
        for k in range(n):
            x = 980 + k * (900 / n)
            o.append(f'<rect x="{x:.0f}" y="{y - 90*sc*3:.0f}" width="{14*sc*3:.0f}" height="{90*sc*3:.0f}" fill="{c1}"/><circle cx="{x + 7*sc*3:.0f}" cy="{y - 40*sc*3:.0f}" r="{18*sc*3:.0f}" fill="{["#5A6A34", "#8A7A3A", "#4A5A2A"][k % 3]}" stroke="{INK}" stroke-width="3"/>')
    o.append('<path d="M1500,600 L1500,330" stroke="#1A1410" stroke-width="10"/><path d="M1504,334 L1640,350 L1600,392 L1640,434 L1504,420 Z" fill="#4A5A2A" stroke="#1A1410" stroke-width="5"/><path d="M1530,360 l40,24 l-40,24" stroke="#C9A25A" stroke-width="6" fill="none"/>')   # Borg sancağı
    return "".join(o)

def army(c, side, rows, t=None, seed0=0, facing=1, x0=0, x1=1920):
    """rows: [(y, ölçek, adet, sis)] arkadan öne. 6 varyant/taraf (önbellek), sıra içinde rastgele kaydırma ve nefes."""
    for ri, (y, sc, n, haze) in enumerate(rows):
        for k in range(n):
            r = random.Random(seed0 * 100 + ri * 37 + k); v = (seed0 + k * 7 + ri * 3) % 6
            sp = full(KL.soldier_spec(seed0 * 10 + v, side, "spear" if v % 3 else "axe"), "fierce" if v % 2 else "neutral", 0.9, facing=facing, look=0.5 * facing)
            x = x0 + (x1 - x0) * (k + 0.5) / n + r.uniform(-18, 18); yy = y + r.uniform(-6, 6) - 3 * abs(math.sin((t or 0) * 1.3 + k))
            draw(c, sp, x, yy, sc)
        c.drawRect(skia.Rect(0, 0, W, H), skia.Paint(Color4f=col("#C8D2DC", haze)))

def d4():
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    draw(c, place(field()), 0, 0, 1.0)
    army(c, "borg", [(600, 0.26, 26, 0.10), (640, 0.34, 20, 0.08), (690, 0.44, 15, 0.0)], t, seed0=3, facing=-1, x0=900, x1=1920)
    fog(c, t or 0, 620, "#D8E0E6", 0.3, seed=6, speed=12)
    RLf = full(dict(ROLLO, _arm_up=True, _hand_extra=KL.BEARD_AXE.replace("#C9A25A", "#8A7A5A")), ex("stone", IF.blink_at(1.0)), 0.80, facing=-1, look=-0.6)
    with live(c, 1240, 980, phase=1.0, breathe=0.006):
        rim(c, RLf, 1240, 980, 1.0, "#E6F0FA", dx=-4, dy=-3, a=0.8); draw(c, RLf, 1240, 980, 1.0)
    army(c, "ragnar", [(1000, 0.62, 5, 0.0)], t, seed0=1, facing=1, x0=-150, x1=760)
    RGs = fig_bust(dict(RG, _arm_up=True, _hand_extra=KL.BEARD_AXE.replace('<g transform="translate(HX,HY)">', '<g transform="translate(HX,HY) rotate(48)">')), ex("fierce", IF.blink_at(0.4)), 0.9, 2.0)
    with live(c, 420, 1080, phase=0.4, breathe=0.007):
        rim(c, RGs, 420, 420, 1.0, "#E6F0FA", dx=6, dy=-4, a=0.85); draw(c, RGs, 420, 420, 1.0)
        shade_side(c, RGs, 420, 420, 0.45, 600, 200)
    finish(c, cold=True); return s

# ------------------------------------------------------------------ 8/2 · Rollo kılıcını bırakıp diz çöker
def d5():
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    draw(c, place(field()), 0, 0, 1.0)
    army(c, "borg", [(610, 0.28, 24, 0.1), (650, 0.36, 18, 0.06)], t, seed0=3, facing=-1, x0=1000, x1=1920)
    army(c, "ragnar", [(610, 0.28, 18, 0.1), (650, 0.36, 14, 0.06)], t, seed0=1, facing=1, x0=0, x1=820)
    fog(c, t or 0, 640, "#D8E0E6", 0.35, seed=7, speed=10)
    sw = svg_sprite(f'<g transform="translate(1180,960) rotate(-8)"><path d="M-160,0 L120,0" stroke="{INK}" stroke-width="16" stroke-linecap="round"/><path d="M-160,0 L120,0" stroke="#B8C0C8" stroke-width="9" stroke-linecap="round"/>'
                    f'<path d="M120,-20 L124,20" stroke="{INK}" stroke-width="12"/><path d="M124,0 L180,0" stroke="#6A5038" stroke-width="12"/></g>')
    draw(c, sw, 0, 0, 1.0)
    kneel = 1.0 if t is None else ease_(lin_(t, 0.3, 1.4))
    RLk = full(dict(ROLLO, _kneel=130), ex("shame_r", IF.blink_at(1.0)), 0.92, facing=-1, look=-0.2)
    RLs = full(ROLLO, ex("shame_r", IF.blink_at(1.0)), 0.92, facing=-1, look=-0.2)
    sp = RLk if kneel > 0.5 else RLs
    rim(c, sp, 1300, 990, 1.0, "#E6F0FA", dx=-4, dy=-3, a=0.8); draw(c, sp, 1300, 990, 1.0)
    low = 1.0 if t is None else ease_(lin_(t, CUE2.get("indir", 2.0), CUE2.get("indir", 2.0) + 0.8))
    AXE_DOWN = KL.BEARD_AXE.replace('<g transform="translate(HX,HY)">', '<g transform="translate(HX,HY) rotate(160)">')
    RGf = full(dict(RG, _arm_up=low < 0.5, _hand_extra=KL.BEARD_AXE if low < 0.5 else AXE_DOWN), ex("broken", IF.blink_at(0.3)), 1.0, look=0.5)
    rim(c, RGf, 700, 1100, 1.0, "#E6F0FA", dx=5, dy=-4, a=0.85); draw(c, RGf, 700, 1100, 1.0)
    finish(c, cold=True); return s

# ------------------------------------------------------------------ 10/1 · Horik ile kadeh
def d6():
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    draw(c, blurred(place(P7.greathall(0.9)), 6), 0, 0, 1.0)
    RGs = fig_bust(dict(RG, _arm_up=True, _hand_extra=HORN_UP), ex("sly", IF.blink_at(0.4)), 1.0, 1.9)
    with live(c, 600, 1080, phase=0.4, breathe=0.006):
        rim(c, RGs, 600, 400, 1.0, "#FFB070", dx=4, dy=2, a=0.6); draw(c, RGs, 600, 400, 1.0)
        shade_side(c, RGs, 600, 400, 0.45, 760, 340, "#1A0E08")
    HK = fig_bust(dict(HORIK, _arm_up=True, _hand_extra=HORN_UP), ex("sly", IF.blink_at(1.2)), -0.8, 1.9, flip=True)
    with live(c, 1320, 1080, phase=1.2, breathe=0.006):
        rim(c, HK, 1320, 400, 1.0, "#FFB070", dx=-4, dy=2, a=0.6); draw(c, HK, 1320, 400, 1.0)
        shade_side(c, HK, 1320, 400, 0.45, 1160, 1600, "#1A0E08")
    glow(c, 960, 1000, 520, "#FF8A3A", 0.25)
    finish(c, cold=False, warm=0.05); return s

# ------------------------------------------------------------------ 10/2 · gece salonda iki siluet, hançer
def d7():
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    draw(c, blurred(place(P7.greathall(0.5)), 4), 0, 0, 1.0)
    c.drawRect(skia.Rect(0, 0, W, H), skia.Paint(Color4f=col("#020206", 0.7)))
    glow(c, 960, 900, 640, "#FF6A20", 0.35)
    HKf = full(dict(HORIK, _arm_up=True, _hand_extra=DAGGER_UP), "fierce", 1.0, facing=-1, look=-0.6)
    RGf = full(RG, "fierce", 1.0, look=0.6)
    for sp_, x, x0, x1 in ((RGf, 760, 960, 500), (HKf, 1180, 960, 1420)):   # gerçek modeller, ateş ışığı ortadan; dış yarı karanlıkta
        rim(c, sp_, x, 1100, 1.0, "#FFA050", dx=4 if x < 960 else -4, dy=-4, a=0.9); draw(c, sp_, x, 1100, 1.0)
        shade_side(c, sp_, x, 1100, 0.78, x0, x1, "#08060A")
    g = 1.0 if t is None else math.sin(math.pi * lin_(t, CUE2.get("flas", 1.0), CUE2.get("flas", 1.0) + 0.5))
    bloom_spot(c, 1290, 380, 120, "#F4FAFF", 0.8 * g)
    finish(c, cold=False); return s

# ------------------------------------------------------------------ 10/3 · Ragnar hükümdar koltuğunda, salon diz çöker
def d8():
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    draw(c, blurred(place(P7.greathall(0.6)), 2), -384, -250, 1.4)
    RGsit = sprite(f'<g transform="translate(400,1000) scale(0.50)">{figure(RG, "front", "sit", ex("stone", IF.blink_at(0.3)), hands=("open", "open"))}</g>', 800, 1100, ax=400, ay=1000, ss=1.0)
    draw(c, RGsit, 960, 610, 1.0)
    kq = 1.0 if t is None else ease_(lin_(t, 0.4, 1.6))
    for k, (x, f_) in enumerate(((180, 1), (360, 1), (540, 1), (1380, -1), (1560, -1), (1740, -1))):
        sp = full(dict(KL.soldier_spec(30 + k, "ragnar"), _kneel=130 if kq > 0.5 else 0, _arm_up=False, _hand_extra="", _body_extra=""), "neutral", 0.85, facing=f_, look=0.4)
        rim(c, sp, x, 1080, 1.0, "#FFB070", dx=0, dy=-4, a=0.7); draw(c, sp, x, 1080, 1.0)
        shade_side(c, sp, x, 1080, 0.55, 960, x, "#120A06")
    one = 1.0 if t is None else 1 - 0.6 * lin_(t, CUE2.get("kral", 99), CUE2.get("kral", 99) + 1.5)   # tek ışık kalır
    c.drawRect(skia.Rect(0, 0, W, H), skia.Paint(Color4f=col("#000000", 0.55 * (1 - one))))
    bloom_spot(c, 960, 420, 300, "#FFE8C0", 0.35)
    finish(c, cold=False, warm=0.03); return s

FR4 = {"d1": d1, "d2": d2, "d3": d3, "d4": d4, "d5": d5, "d6": d6, "d7": d7, "d8": d8}

def contact4(ids=tuple(FR4)):
    from PIL import Image
    cw, ch = 960, 540; rows = (len(ids) + 1) // 2; sheet = Image.new("RGB", (cw * 2 + 30, (ch + 20) * rows + 10), "#EDE2CC")
    for k, i in enumerate(ids):
        sheet.paste(Image.open(f"{OUT}/{i}.png").convert("RGB").resize((cw, ch)), (10 + (k % 2) * (cw + 10), 10 + (k // 2) * (ch + 20)))
    sheet.save(f"{OUT}/kontakt4_960.png")

if __name__ == "__main__":
    ids = sys.argv[1:] or list(FR4)
    for i in ids:
        T[0] = None; FR4[i]().makeImageSnapshot().save(f"{OUT}/{i}.png", skia.kPNG); print("kare", i)
    contact4()
