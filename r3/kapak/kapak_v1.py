"""YouTube kapağı: solda çiftçi Ragnar ve ailesi (altın saat, huzur), sağda yaşlı kral Ragnar (fırtına, kuru meşe, kuzgunlar).
Çizim 2560×1440'ta yapılır, 1280×720 JPEG olarak verilir (YouTube sınırı 2 MB).  python3 kapak.py [dil ...]"""
import sys, os, math
sys.path[:0] = ["/home/claude/r3/bati", "/home/claude/r3", "/home/claude/r2", "/home/claude/r3/ivar2", "/home/claude/r3/veda2", "/home/claude/r3/veda", "/home/claude/r3/bedel"]
import skia
from v6_son import *                     # yardımcılar: full, draw, svg_sprite, glow, cloud_band, gradient, mountain_range, blurred, soft_shadow, rim ...
import v5_kayip as VK, v3_b as VB, v3_c as VC, ragnar_yas as YAS
from storyboard import LAG, BJ
from modeller import GYDA
import obj7
from v3_prolog import sea_svg, grass
from fx import rim
RVX, RVY = 2090, 930
W2, H2 = 2560, 1440; OUT = "/home/claude/r3/kapak"
METIN = {
 "tr": ("Her şeyi olan|bir çiftçiden", "Hiçbir şeyi olmayan|krala"),
 "en": ("From a farmer|who had everything", "To a king|with nothing"),
 "es": ("De un granjero|que lo tenía todo", "A un rey|sin nada"),
 "pt-BR": ("De um fazendeiro|que tinha tudo", "A um rei|sem nada"),
 "de": ("Vom Bauern,|der alles hatte", "Zum König,|der nichts hat"),
 "fr": ("D'un fermier|qui avait tout", "À un roi|qui n'a plus rien"),
 "ar": ("من مزارعٍ|يملك كلّ شيء", "إلى ملكٍ|لا يملك شيئًا"),
 "ru": ("От фермера,|у которого было всё", "К королю,|у которого нет ничего")}
FONT = {"ar": "Noto Kufi Arabic"}

import frames as IF
from engine import sprite as _sprite
def BIG(inner):
    """2560×1440 SVG katmanı (svg_sprite 1920×1080 ile sınırlı)."""
    return _sprite(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W2}" height="{H2}">{IF.A.defs(1.0, az=315)}{inner}</svg>', W2, H2, ax=0, ay=0, ss=1.0)

def UP(s, dil):
    if dil == "tr": s = s.replace("i", "İ").replace("ı", "I")
    return s if dil == "ar" else s.upper()

def esc(s): return s.replace("&", "&amp;").replace("<", "&lt;")

def yazi(c, txt, cx, cy, rot, fill, stroke, glowc, dil, size=118):
    """İki satır kalın başlık: kalın koyu kontur + iç dolgu + hafif dış parıltı. Satır uzunsa punto küçülür."""
    sat = UP(txt, dil).split("|"); fam = FONT.get(dil, "Alegreya SC"); w8 = "800"
    L = max(len(s) for s in sat); fs = min(size, int(size * 15.5 / max(15.5, L)))
    o = []
    for i, s in enumerate(sat):
        y = (i - (len(sat) - 1) / 2) * fs * 1.08 + fs * 0.35
        base = f'x="0" y="{y:.0f}" font-family="{fam}" font-weight="{w8}" font-size="{fs}" text-anchor="middle"'
        o.append(f'<text {base} fill="none" stroke="{stroke}" stroke-width="{fs*0.24:.0f}" stroke-linejoin="round">{esc(s)}</text>')
        o.append(f'<text {base} fill="{fill}">{esc(s)}</text>')
    svg = f'<g transform="translate(600,300) rotate({rot})">' + "".join(o) + "</g>"
    sp = svg_sprite_box(svg, 1200, 600)
    glow(c, cx, cy, 380, glowc, 0.22)
    draw(c, sp, cx - 600, cy - 300, 1.0)

def svg_sprite_box(body, w, h):
    from engine import sprite
    return sprite(body, w, h, 0, 0, 1.0)

def sol(c):
    """Altın saat: fiyort, çiftlik evi, aile."""
    c.save(); c.clipRect(skia.Rect(0, 0, 1330, H2))
    sky = f'<defs>{gradient("ksl", [(0, "#7FB6D8"), (0.45, "#BFD6D0"), (0.75, "#FFD898"), (1, "#FFC070")])}</defs><rect width="1400" height="900" fill="url(#ksl)"/>'
    draw(c, BIG(sky), 0, 0, 1.0)
    glow(c, 220, 520, 700, "#FFE2A0", 0.55); glow(c, 220, 520, 220, "#FFF4D0", 0.8)
    draw(c, blurred(BIG(cloud_band(901, 9, -100, 1400, 120, 380, "#F4EEE4", "#FFFFFF", 0.75, rx=(160, 360), ry=(26, 60))), 4), 0, 0, 1.0)
    far = mountain_range(902, -100, 1500, 720, 380, 70, "#7A90A6", "#A8BCC8", snow="#EEF4F6", light=1, snow_y=480, stroke="#4A5E70", cid="kf", taper=0)
    draw(c, BIG(far), 0, 0, 1.0)
    draw(c, BIG(sea_svg(716, "#8FC0D0", "#3E6A7E", 220, 71, glint="#FFF2C0", wl="#5A8A9A", hl="#FFF0C8", gn=60, spread=0.4)), 0, 0, 1.0)
    near = mountain_range(903, 700, 1500, 760, 560, 50, "#4E6A58", "#7A9A6A", light=-1, stroke="#2E4436", cid="kn", taper=420)
    draw(c, BIG(near + VB.forest(820, 1500, lambda x: 752, 40, 90, 30, 905, col="#3E5A44", lit="#5E7E58", dark="#24382A")), 0, 0, 1.0)
    # çayır + çiftlik evi
    mead = '<path d="M-40,1460 L-40,860 Q400,820 800,850 Q1100,872 1400,850 L1400,1460 Z" fill="#6E9A4A"/>'
    draw(c, BIG(mead), 0, 0, 1.0)
    draw(c, BIG(obj7.longhouse_ext(820, 860, 560, 170, 1.0, snow=False, smoke=True)), 0, 0, 1.0)
    gr = grass(-40, 1400, 880, 1440, 700, 907, ("#5A8A3A", "#86B04E", "#B8D070"), 18, 70, 24)
    draw(c, BIG(gr), 0, 0, 1.0)
    # aile: Lagertha arkada, Ragnar önde, çocuklar önde-yanda; hepsi gülümsüyor
    YAS.uygula(YAS.RG1)
    fam = [(dict(LAG, cloak="#6A5236"), "tender", 820, 1600, 1.62, -1, -0.3), (YAS.RG1, "laugh", 470, 1640, 1.72, 1, 0.3),
           (dict(BJ), "laugh", 1100, 1560, 1.02, -1, -0.2), (dict(GYDA), "laugh", 700, 1560, 0.92, 1, 0.1)]
    for sp, ex_, x, yb, s, fc, lk in fam:
        f = full(sp, ex_, s, facing=fc, look=lk, w=int(1000 * s), h=int(1350 * s)); soft_shadow(c, x, yb - 8, 220 * s, 20, 0.3)
        rim(c, f, x, yb, 1.0, "#FFE8B0", dx=-5 * fc, dy=-4, a=0.8); draw(c, f, x, yb, 1.0)
    glow(c, 640, 900, 900, "#FFD890", 0.12)
    c.restore()

def sag(c):
    """Fırtına: kızıl-gri gök, kuru meşe ve kuzgunlar, kambur yaşlı kral."""
    c.save(); c.clipRect(skia.Rect(1230, 0, W2, H2))
    sky = f'<defs>{gradient("ksr", [(0, "#1A1418"), (0.4, "#3A2228"), (0.75, "#7A2E22"), (1, "#C04A22")])}</defs><rect x="1200" width="1400" height="1100" fill="url(#ksr)"/>'
    draw(c, BIG(sky), 0, 0, 1.0)
    draw(c, blurred(BIG(cloud_band(911, 12, 1150, 2650, 40, 520, "#2A1E24", "#7A3A30", 0.85, lit_dy=10, rx=(200, 460), ry=(40, 90))), 6), 0, 0, 1.0)
    glow(c, 2150, 860, 600, "#FF6A2A", 0.35)
    ridge = mountain_range(912, 1150, 2700, 980, 700, 60, "#1E1418", "#3A2224", light=-1, stroke="#0E080A", cid="kr")
    draw(c, BIG(ridge), 0, 0, 1.0)
    # kuru meşe (onaylı Bölüm V meşesi, küçültülmüş), dallarında kuzgunlar
    pre, trunk, limbs, perch = VK.oak(880, 930, 31); S_ = 0.78; ox, oy = 1460, 300
    tree = f'<g transform="translate({ox},{oy}) scale({S_})">' + VK.TEXD + pre + trunk + limbs + "</g>"
    draw(c, BIG(tree.replace("#3E4430", "#2A2224")), 0, 0, 1.0, a=1.0)
    c.drawRect(skia.Rect(1200, 0, W2, H2), skia.Paint(Color4f=col("#2A1418", 0.35)))   # ağacı kızıl karanlığa göm
    pv = sorted([q for q in perch if 120 < q[1] < 700], key=lambda q: q[0]); pick = []
    for q in pv:
        if all(abs(q[0] - p[0]) > 190 or abs(q[1] - p[1]) > 130 for p in pick): pick.append(q)
    rv = "".join(VB.raven(ox + x * S_, oy + y * S_ - 14, 0.5, 1 if k % 2 else -1, "perch", k) for k, (x, y, w) in enumerate(pick[:6]))
    draw(c, BIG(rv), 0, 0, 1.0)
    # zemin: köklerin oturduğu engebeli tepe + sis + kor ışığı (düz bant yok)
    gnd = ('<path d="M1180,1460 L1180,1060 Q1420,1020 1640,1040 Q1900,1062 2120,1030 Q2380,996 2620,1040 L2620,1460 Z" fill="#1E1416"/>'
           '<path d="M1180,1062 Q1420,1022 1640,1042 Q1900,1064 2120,1032 Q2380,998 2620,1042" stroke="#7A2E1E" stroke-width="5" fill="none" opacity="0.7"/>')
    draw(c, BIG(gnd + grass(1180, 2620, 1030, 1460, 420, 917, ("#2A1A16", "#3E2420", "#5A2E22"), 16, 60, 20)), 0, 0, 1.0)
    draw(c, blurred(BIG(cloud_band(918, 12, 1150, 2650, 980, 1120, "#6A3A34", "#A0524A", 0.5, rx=(220, 480), ry=(20, 46))), 14), 0, 0, 1.0)
    glow(c, 2300, 1300, 700, "#FF5A20", 0.22)
    # yaşlı kral: kambur, ağarmış, yorgun; omzunda kuzgun
    YAS.uygula(YAS.RG4)
    sp = dict(YAS.RG4, cloak="#241C22"); S2 = 2.35
    f = full(sp, "grief", S2, facing=-1, look=0.25, w=int(1000 * S2), h=int(1350 * S2)); x, yb = 1990, 420 + 687 * S2
    glow(c, x, 760, 560, "#FF7A3A", 0.2)
    rim(c, f, x, yb, 1.0, "#FF8A4A", dx=7, dy=-5, a=0.95); draw(c, f, x, yb, 1.0)
    draw(c, BIG(VB.raven(RVX, RVY, 0.7, -1, "perch", 3)), 0, 0, 1.0)
    r = R_(915)
    for k in range(70):
        ex_, ey_ = r.uniform(1250, 2560), r.uniform(200, 1400)
        c.drawCircle(ex_, ey_, r.uniform(2, 5), skia.Paint(AntiAlias=True, Color4f=col(r.choice(["#FFB060", "#FF7A30", "#FFD080"]), r.uniform(0.4, 0.9))))
    for k in range(220):   # yağmur
        x0, y0 = r.uniform(1200, 2600), r.uniform(-50, 1440)
        c.drawLine(x0, y0, x0 - 14, y0 + 60, skia.Paint(AntiAlias=True, Color4f=col("#C8B8B8", 0.18), StrokeWidth=2.2))
    c.restore()

def ayrac(c):
    """Ortada yırtık/çatlak ayraç: koyu mürekkep + sol tarafta sıcak, sağda kızıl kenar ışığı."""
    r = R_(921); pts = []; y = -20
    while y < H2 + 40:
        pts.append((1280 + r.uniform(-60, 60) + 40 * math.sin(y / 260), y)); y += r.uniform(50, 110)
    d = "M" + " L".join(f"{x:.0f},{y:.0f}" for x, y in pts)
    draw(c, blurred(BIG(f'<path d="{d}" stroke="#FFD27A" stroke-width="34" fill="none" opacity="0.55"/>'), 14), -10, 0, 1.0)
    draw(c, blurred(BIG(f'<path d="{d}" stroke="#FF5A2A" stroke-width="34" fill="none" opacity="0.5"/>'), 14), 12, 0, 1.0)
    draw(c, BIG(f'<path d="{d}" stroke="#0E0A0C" stroke-width="22" fill="none" stroke-linejoin="round"/>'), 0, 0, 1.0)

def kapak(dil="tr", draft=False):
    s = skia.Surface(W2, H2); c = s.getCanvas(); c.clear(skia.ColorBLACK)
    sol(c); sag(c); ayrac(c)
    a, b = METIN[dil]
    yazi(c, a, 640, 190, -3, "#FFF6DA", "#3A2210", "#FFE6A0", dil)
    yazi(c, b, 1920, 190, 3, "#F4F0F0", "#14080A", "#FF5A2A", dil)
    img = s.makeImageSnapshot()
    os.makedirs(OUT, exist_ok=True)
    big = f"{OUT}/kapak_{dil}_2560.png"; img.save(big, skia.kPNG)
    from PIL import Image
    im = Image.open(big).convert("RGB").resize((1280, 720), Image.LANCZOS)
    jp = f"{OUT}/kapak_{dil}.jpg"; im.save(jp, quality=92, optimize=True)
    return jp, os.path.getsize(jp)

if __name__ == "__main__":
    for d in (sys.argv[1:] or ["tr"]): print(kapak(d))
