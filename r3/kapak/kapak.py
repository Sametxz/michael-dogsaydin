"""YouTube kapağı v2 (kurul: Ajan 1 CTR + Ajan 2 sanat yönetmeni, 21.11.2026).
Solda altın saatte gülen çiftçi Ragnar ve ailesi; sağda kararmış, yana kaymış taçlı, ağlayan yaşlı kral; arada yırtık ayraç.
Paneller çatlak yolunun kendisiyle kırpılır (düz dikey kesik yok). İki büyük yüz aynı yükseklikte karşılıklı durur.
Başlık iki katmanlı: büyük karşıt kelime (HER ŞEYİ altın / HİÇBİR ŞEYİ kor) + %70 boyutta kalan cümle.
Çizim 2560×1440, çıktı 1280×720 JPEG.   python3 kapak.py [dil ...]   (v1: kapak_v1.py)"""
import sys, os, math
sys.path[:0] = ["/home/claude/r3/bati", "/home/claude/r3", "/home/claude/r2", "/home/claude/r3/ivar2", "/home/claude/r3/veda2", "/home/claude/r3/veda", "/home/claude/r3/bedel"]
import skia
from v6_son import *
import v5_kayip as VK, v3_b as VB, v3_c as VC, ragnar_yas as YAS
from storyboard import LAG, BJ
from modeller import GYDA
import obj7, art3
from v3_prolog import sea_svg, grass
from fx import rim
W2, H2 = 2560, 1440; OUT = "/home/claude/r3/kapak"
HC = art3.BODY["tall"]["head_cy"]          # ayaktan kafa merkezine (model birimi)

# (üst küçük satır, BÜYÜK VURGU, alt küçük satır) — vurgu her dilde karşıt kelime; kalan cümle o dilin doğal sırasıyla bölünür
METIN = {
 "tr": (("", "Her şeyi", "olan bir çiftçiden"), ("", "Hiçbir şeyi", "olmayan krala")),
 "en": (("From a farmer who had", "Everything", ""), ("To a king with", "Nothing", "")),
 "es": (("De un granjero que lo tenía", "Todo", ""), ("A un rey sin", "Nada", "")),
 "pt-BR": (("De um fazendeiro que tinha", "Tudo", ""), ("A um rei sem", "Nada", "")),
 "de": (("Vom Bauern mit", "Allem", ""), ("Zum König mit", "Nichts", "")),
 "fr": (("D'un fermier qui avait", "Tout", ""), ("À un roi qui n'a", "Rien", "")),
 "ar": (("من مزارعٍ يملك", "كلّ شيء", ""), ("إلى ملكٍ", "بلا شيء", "")),
 "ru": (("От фермера, имевшего", "Всё", ""), ("К королю, у которого нет", "Ничего", ""))}
FONT = {"ar": "Noto Kufi Arabic"}

# kapak ifadesi: açık göz, kalkık kaş, dişli gülüş (laugh'ın kapalı/çatık gözü küçük boyutta öfke okunuyordu)
# (art3 kaş işareti: negatif iç değer kaşın iç ucunu indirir; test: /tmp/r13/exp.png)
art3.EXP["joy_m"] = (-4, 6, 0.0, 0.18, "laugh", "")
art3.EXP["joy"] = (14, 14, 0.06, 0.18, "laugh", "")

import frames as IF
from engine import sprite as _sprite
def BIG(inner):
    return _sprite(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W2}" height="{H2}">{IF.A.defs(1.0, az=315)}{inner}</svg>', W2, H2, ax=0, ay=0, ss=1.0)

def UP(s, dil):
    if dil == "tr": s = s.replace("i", "İ").replace("ı", "I")
    return s if dil == "ar" else s.upper()
def esc(s): return s.replace("&", "&amp;").replace("<", "&lt;")

def _tf(dil):
    return skia.Typeface(FONT.get(dil, "Alegreya SC"), skia.FontStyle(800, 5, skia.FontStyle.kUpright_Slant))
def tw(s, dil, fs):
    """Ölçülen metin genişliği (px) + kontur payı."""
    return skia.Font(_tf(dil), fs).measureText(s) * (1.12 if dil == "ar" else 1.0) + fs * 0.32

MAXW = 1060
def boyutlar(dil):
    """İki tarafın vurgu puntosu eşit; küçük satırlar eşit. Uzun dilde ikisi birlikte küçülür."""
    (a, b) = METIN[dil]
    fa = min(176, *[int(176 * MAXW / max(MAXW, tw(UP(t[1], dil), dil, 176))) for t in (a, b)])
    fk = int(fa * 0.70)
    for t in (a, b):
        for s in (t[0], t[2]):
            if s: fk = min(fk, int(fk * 1150 / max(1150, tw(UP(s, dil), dil, fk))))
    return fa, fk

def yazi(c, parca, cx, top, rot, acc, fill, stroke, halo, dil, fa, fk, side):
    """Kalın koyu kontur + 10 px alt gölge + koyu hale; vurgu kelimesi dikey degrade dolgulu."""
    ust, vur, alt = (UP(p, dil) for p in parca); fam = FONT.get(dil, "Alegreya SC")
    rows = ([(ust, fk, False)] if ust else []) + [(vur, fa, True)] + ([(alt, fk, False)] if alt else [])
    o = [f'<defs><linearGradient id="ac{side}" x1="0" y1="0" x2="0" y2="1">' + "".join(f'<stop offset="{p}" stop-color="{q}"/>' for p, q in acc) + '</linearGradient>'
         f'<filter id="ds{side}" x="-20%" y="-40%" width="140%" height="180%"><feGaussianBlur stdDeviation="7"/></filter></defs>']
    y = 0; lines = []
    for s, fs, big in rows:
        g = 1.3 if dil == "ar" else 1.0   # Kufi: uzun üst/alt uzantılar, satır aralığı açılır
        y += fs * (0.86 if big else 0.92) * g; lines.append((s, fs, big, y)); y += fs * (0.16 if big else 0.14) * g
    for s, fs, big, yy in lines:
        base = f'x="0" y="{yy:.0f}" font-family="{fam}" font-weight="800" font-size="{fs}" text-anchor="middle"'
        sw = fs * (0.30 if big else 0.32)
        o.append(f'<text {base} fill="#000" stroke="#000" stroke-width="{sw:.0f}" stroke-linejoin="round" opacity="0.75" transform="translate(0,{fs*0.07:.0f})" filter="url(#ds{side})">{esc(s)}</text>')
        o.append(f'<text {base} fill="none" stroke="{stroke}" stroke-width="{sw:.0f}" stroke-linejoin="round">{esc(s)}</text>')
        o.append(f'<text {base} fill="{"url(#ac%s)" % side if big else fill}">{esc(s)}</text>')
        if big: o.append(f'<text {base} fill="none" stroke="#FFFFFF" stroke-width="2.5" opacity="0.35" transform="translate(0,-3)">{esc(s)}</text>')
    svg = f'<g transform="translate(700,40) rotate({rot})">' + "".join(o) + "</g>"
    sp = _sprite(svg, 1400, int(y + 140), 0, 0, 1.0)
    glow(c, cx, top + y * 0.5, 560, halo, 0.42)
    draw(c, sp, cx - 700, top - 40, 1.0)
    return top + y

def catlak():
    r = R_(921); pts = []; y = -30
    while y < H2 + 60:
        pts.append((1280 + r.uniform(-42, 42) + 34 * math.sin(y / 260), y)); y += r.uniform(46, 96)
    pts.append((pts[-1][0] + 20, H2 + 60))   # son nokta kadrajın altına: alt köşede boş üçgen kalmasın
    return pts

def yol(pts, sag):
    p = skia.Path(); x0 = W2 + 20 if sag else -20
    p.moveTo(x0, -40)
    for x, y in pts: p.lineTo(x, y)
    p.lineTo(x0, H2 + 80); p.close(); return p

def tint(c, f, x, yb, color, a):
    """Figürü panel ışığına göre tonlar (yalnız figürün piksellerinde)."""
    c.saveLayer(); draw(c, f, x, yb, 1.0)
    c.drawRect(skia.Rect(0, 0, W2, H2), skia.Paint(Color4f=col(color, a), BlendMode=skia.BlendMode.kSrcATop)); c.restore()

BRONZ = art3.RAVEN_CLASP.replace('translate(-70,-430)">', 'translate(-70,-430)"><g transform="scale(0.6)">', 1).replace("#C8CDD2", "#6E4E2C").replace("#9AA2AA", "#B08848") + "</g>"
TOKA = '<g transform="translate(0,-440)"><circle r="10" fill="#8A6234" stroke="#1A1410" stroke-width="4"/><circle r="4" fill="#C89A50"/></g>'

def sol(c, pts):
    """Altın saat: fiyort, çiftlik evi, sıcak güneş haresi; aile üçgen grup halinde."""
    c.save(); c.clipPath(yol(pts, False), doAntiAlias=True)
    sky = f'<defs>{gradient("ksl", [(0, "#6FA8D2"), (0.38, "#B4D2D2"), (0.62, "#FFD898"), (1, "#FFB860")])}</defs><rect width="1440" height="900" fill="url(#ksl)"/>'
    draw(c, BIG(sky), 0, 0, 1.0)
    glow(c, 1060, 600, 900, "#FFD27A", 0.6); glow(c, 1060, 600, 300, "#FFF6D8", 0.85)
    rays = "".join(f'<path d="M1060,600 L{1060 + 1500*math.cos(a - 0.035):.0f},{600 + 1500*math.sin(a - 0.035):.0f} L{1060 + 1500*math.cos(a + 0.035):.0f},{600 + 1500*math.sin(a + 0.035):.0f} Z" fill="#FFF2C0" opacity="0.10"/>'
                   for a in [math.pi + k * 0.26 for k in range(-3, 9)])
    draw(c, blurred(BIG(rays), 6), 0, 0, 1.0)
    draw(c, blurred(BIG(cloud_band(901, 9, -100, 1440, 330, 470, "#F8EEDC", "#FFFFFF", 0.7, rx=(160, 360), ry=(22, 50))), 4), 0, 0, 1.0)
    draw(c, BIG("".join(VB.gull(x, y, 0.42, k) for k, (x, y) in enumerate([(240, 420), (310, 470), (180, 500)]))), 0, 0, 1.0)
    far = mountain_range(902, -100, 1500, 720, 400, 70, "#7A90A6", "#B4C4CC", snow="#F2F4F0", light=1, snow_y=500, stroke="#4A5E70", cid="kf", taper=0)
    draw(c, blurred(BIG(far), 1.2), 0, 0, 1.0)
    draw(c, BIG(sea_svg(716, "#9CC4CC", "#3E6A7E", 220, 71, glint="#FFF2C0", wl="#5A8A9A", hl="#FFF0C8", gn=80, spread=0.5)), 0, 0, 1.0)
    near = mountain_range(903, 700, 1500, 760, 560, 50, "#4E6A58", "#7A9A6A", light=-1, stroke="#2E4436", cid="kn", taper=420)
    draw(c, BIG(near + VB.forest(820, 1500, lambda x: 752, 40, 90, 30, 905, col="#3E5A44", lit="#5E7E58", dark="#24382A")), 0, 0, 1.0)
    mead = '<path d="M-40,1460 L-40,860 Q400,820 800,850 Q1100,872 1440,850 L1440,1460 Z" fill="#7EA24A"/>'
    draw(c, BIG(mead), 0, 0, 1.0)
    draw(c, BIG(obj7.longhouse_ext(560, 860, 560, 170, 1.0, snow=False, smoke=False)), 0, 0, 1.0)
    puf = "".join(f'<circle cx="{860 + k*14 + 10*math.sin(k):.0f}" cy="{770 - k*55}" r="{18 + k*7}" fill="#EDE6DA" opacity="{0.5 - k*0.07:.2f}"/>' for k in range(6))
    draw(c, blurred(BIG(puf), 9), 0, 0, 1.0)
    draw(c, BIG(grass(-40, 1440, 880, 1440, 700, 907, ("#6A8A3A", "#9AB44E", "#D8D070"), 18, 70, 24)), 0, 0, 1.0)
    glow(c, 1000, 980, 700, "#FFC860", 0.25)
    YAS.uygula(YAS.RG1)
    S = 2.75
    fam = [  # spec, ifade, x, ayak_y, ölçek, bakış, look, eğim
        (dict(LAG, cloak="#6A5236", clasp=TOKA), "joy", 975, 770 - HC * S * 0.97, S * 0.97, -1, -0.45, -2.5),
        (dict(YAS.RG1, clasp=BRONZ), "joy_m", 450, 760 - HC * S, S, 1, 0.35, 0),
        (dict(GYDA, armring=False, clasp=""), "joy", 700, 1190 - HC * 1.5, 1.5, 1, 0.2, 0),
        (dict(BJ, armring=False, face_scar=False, clasp=""), "joy", 1040, 1170 - HC * 1.6, 1.6, -1, -0.3, 0)]
    for sp, ex_, x, yb, s, fc, lk, eg in fam:
        f = full(sp, ex_, s, facing=fc, look=lk, w=int(1000 * s), h=int(1350 * s))
        c.save(); c.rotate(eg, x, yb)
        rim(c, f, x, yb, 1.0, "#FFE6A0", dx=7, dy=-5, a=0.85)
        tint(c, f, x, yb, "#FFB040", 0.09)
        c.restore()
    r = R_(931)
    for k in range(60):   # altın polen / parıltı
        x, y = r.uniform(0, 1250), r.uniform(380, 1400)
        c.drawCircle(x, y, r.uniform(1.5, 4.5), skia.Paint(AntiAlias=True, Color4f=col(r.choice(["#FFF0B0", "#FFD870", "#FFFFFF"]), r.uniform(0.35, 0.8))))
    glow(c, 1060, 600, 1100, "#FFD890", 0.08)
    c.restore()

def tac():
    """Kararmış, yana kaymış sade demir-altın taç (kafa yerel koordinatı; dizideki tasarım değil): düşük beş diş, aşınmış bant."""
    teeth = "M-82,0 L-82,-26 L-64,-12 L-44,-40 L-24,-14 L0,-46 L24,-14 L46,-40 L66,-12 L86,-28 L86,0 Q2,12 -82,0 Z"
    return (f'<g transform="translate(8,-88) rotate(-17) scale(0.8)">'
            f'<path d="{teeth}" fill="#4E3E26" stroke="#120A08" stroke-width="7" stroke-linejoin="round"/>'
            f'<path d="M-82,-2 Q2,10 86,-2 L86,14 Q2,28 -82,14 Z" fill="#3A2C1C" stroke="#120A08" stroke-width="7" stroke-linejoin="round"/>'
            f'<path d="M-70,-10 L-64,-12 L-46,-34 M-20,-16 L0,-40 M28,-16 L46,-34" stroke="#A8783A" stroke-width="3.5" fill="none" opacity="0.8"/>'
            f'<path d="M-76,6 Q2,18 80,6" stroke="#9A6A34" stroke-width="3" fill="none" opacity="0.7"/>'
            f'<circle cx="0" cy="6" r="7" fill="#5A1A14" stroke="#120A08" stroke-width="3"/><circle cx="-44" cy="4" r="5" fill="#2A2420" stroke="#120A08" stroke-width="2.5"/><circle cx="46" cy="4" r="5" fill="#2A2420" stroke="#120A08" stroke-width="2.5"/>'
            f'<path d="M-10,-8 l6,10 M30,0 l4,8" stroke="#120A08" stroke-width="2" opacity="0.7"/></g>')

GOZYASI = ('<path d="M47,8 Q51,22 49,32" stroke="#DDEFFF" stroke-width="4.5" fill="none" stroke-linecap="round" opacity="0.8"/>'
           '<ellipse cx="49" cy="36" rx="4.2" ry="5.6" fill="#DDEFFF" opacity="0.9" stroke="#5A8AB0" stroke-width="1.2"/><circle cx="47.6" cy="34" r="1.5" fill="#fff"/>')   # ince iz + küçük damla, bıyığa değmez

def sag(c, pts):
    """Fırtına: kızıl-gri gök, kuru meşe siluetinde 3 kuzgun, taçlı ağlayan yaşlı kral; yüz panelin en açık değeri."""
    c.save(); c.clipPath(yol(pts, True), doAntiAlias=True)
    sky = f'<defs>{gradient("ksr", [(0, "#1A1418"), (0.4, "#3A2228"), (0.75, "#7A2E22"), (1, "#C04A22")])}</defs><rect x="1140" width="1440" height="1100" fill="url(#ksr)"/>'
    draw(c, BIG(sky), 0, 0, 1.0)
    draw(c, blurred(BIG(cloud_band(911, 12, 1150, 2650, 40, 520, "#2A1E24", "#7A3A30", 0.85, lit_dy=10, rx=(200, 460), ry=(40, 90))), 6), 0, 0, 1.0)
    ridge = mountain_range(912, 1150, 2700, 990, 760, 140, "#241618", "#3A2224", light=-1, stroke="#0E080A", cid="kr")
    draw(c, blurred(BIG(ridge), 2.5), 0, 0, 1.0)
    glow(c, 1930, 760, 640, "#FF7A3A", 0.42)                      # başın arkasında kor boşluğu (yüz kontrastı)
    pre, trunk, limbs, perch = VK.oak(880, 930, 31); S_ = 0.95; ox, oy = 1720, 40
    tree = f'<g transform="translate({ox},{oy}) scale({S_})">' + VK.TEXD + pre + trunk + limbs + "</g>"
    draw(c, BIG(tree.replace("#3E4430", "#1A1214")), 0, 0, 1.0)
    c.drawRect(skia.Rect(1140, 0, W2, H2), skia.Paint(Color4f=col("#1A0C10", 0.30)))
    gnd = ('<path d="M1150,1460 L1150,1060 Q1420,1020 1640,1040 Q1900,1062 2120,1030 Q2380,996 2620,1040 L2620,1460 Z" fill="#1E1416"/>'
           '<path d="M1150,1062 Q1420,1022 1640,1042 Q1900,1064 2120,1032 Q2380,998 2620,1042" stroke="#7A2E1E" stroke-width="5" fill="none" opacity="0.7"/>')
    draw(c, BIG(gnd + grass(1150, 2620, 1030, 1460, 420, 917, ("#2A1A16", "#3E2420", "#5A2E22"), 16, 60, 20)), 0, 0, 1.0)
    draw(c, blurred(BIG(cloud_band(918, 14, 1150, 2650, 990, 1130, "#6A3A34", "#A0524A", 0.42, rx=(160, 420), ry=(24, 60))), 22), 0, 0, 1.0)
    r = R_(915)
    for k in range(200):   # yağmur ve köz figürden ÖNCE: yüzü kesmez
        x0, y0 = r.uniform(1150, 2600), r.uniform(-50, 1440)
        c.drawLine(x0, y0, x0 - 14, y0 + 60, skia.Paint(AntiAlias=True, Color4f=col("#C8B8B8", 0.16), StrokeWidth=2.2))
    for k in range(50):
        c.drawCircle(r.uniform(1220, 2560), r.uniform(200, 1400), r.uniform(2, 5), skia.Paint(AntiAlias=True, Color4f=col(r.choice(["#FFB060", "#FF7A30", "#FFD080"]), r.uniform(0.4, 0.9))))
    # kuzgunlar: 2 tünemiş (dal siluetinde, büyük) + 1 kanat açmış
    # kuzgunlar: ufuk korunun önünde iki tünemiş, net profil siluet; zemine gömülü kırık kazıkların üstünde, krala bakar
    st = ""
    for kx, top, h_ in ((1470, 905, 190), (2440, 860, 230)):
        st += (f'<path d="M{kx-17},{top+h_} L{kx-13},{top+10} L{kx-4},{top} L{kx+6},{top+12} L{kx+15},{top+h_} Z" fill="#1A1012" stroke="#0A0406" stroke-width="5" stroke-linejoin="round"/>'
               f'<path d="M{kx+6},{top+20} L{kx+9},{top+h_-10}" stroke="#7A3A26" stroke-width="3" opacity="0.8"/>')
    draw(c, BIG(st), 0, 0, 1.0)
    draw(c, blurred(BIG(f'<ellipse cx="1470" cy="1090" rx="120" ry="26" fill="#5A2A26" opacity="0.8"/><ellipse cx="2440" cy="1090" rx="130" ry="26" fill="#5A2A26" opacity="0.8"/>'), 10), 0, 0, 1.0)
    rv = BIG(VB.raven(1452, 905 - 44 * 1.25, 1.25, 1, "perch", 1) + VB.raven(2462, 860 - 44 * 1.1, 1.1, -1, "perch", 2))
    rim(c, rv, 0, 0, 1.0, "#FF8A4A", dx=3, dy=-4, a=0.95); draw(c, rv, 0, 0, 1.0)
    # yaşlı kral
    YAS.uygula(YAS.RG4)
    S2 = 2.85; x = 1930; yb = 770 - HC * S2
    sp = dict(YAS.RG4, cloak="#241C22", clasp=BRONZ, armring=False, _noarm=True, _head_extra=tac())
    f = full(sp, "grief", S2, facing=-1, look=0.3, w=int(1000 * S2), h=int(1350 * S2))
    rim(c, f, x, yb, 1.0, "#FF8A4A", dx=8, dy=-5, a=0.95)
    tint(c, f, x, yb, "#5A1418", 0.14)
    # vinyet: yüz dışı köşeler koyulaşır
    vg = skia.GradientShader.MakeRadial((1900, 760), 1000, [col("#000000", 0.0), col("#000000", 0.0), col("#0A0406", 0.55)], [0, 0.45, 1.0])
    c.drawRect(skia.Rect(1140, 0, W2, H2), skia.Paint(Shader=vg))
    c.restore()

def ayrac(c, pts):
    """İnce yırtık ayraç: sol yanda altın, sağ yanda kor kenar ışığı (her biri kendi panelinde kırpılı)."""
    d = "M" + " L".join(f"{x:.0f},{y:.0f}" for x, y in pts)
    for sag_, colr in ((False, "#FFD27A"), (True, "#FF5A2A")):
        c.save(); c.clipPath(yol(pts, sag_), doAntiAlias=True)
        draw(c, blurred(BIG(f'<path d="{d}" stroke="{colr}" stroke-width="46" fill="none" opacity="0.75"/>'), 12), 0, 0, 1.0)
        c.restore()
    draw(c, BIG(f'<path d="{d}" stroke="#0E0A0C" stroke-width="15" fill="none" stroke-linejoin="miter"/>'
                f'<path d="{d}" stroke="#FFE8B0" stroke-width="2.5" fill="none" opacity="0.5" transform="translate(-9,0)"/>'), 0, 0, 1.0)

def kapak(dil="tr"):
    s = skia.Surface(W2, H2); c = s.getCanvas(); c.clear(skia.ColorBLACK)
    pts = catlak(); sol(c, pts); sag(c, pts); ayrac(c, pts)
    a, b = METIN[dil]; fa, fk = boyutlar(dil)
    yazi(c, a, 640, 34, -2.5, [(0, "#FFF2A0"), (0.55, "#FFD24A"), (1, "#E89A1A")], "#FFF6DA", "#3A1E08", "#2A1404", dil, fa, fk, "L")
    yazi(c, b, 1920, 34, 2.5, [(0, "#FF9A5A"), (0.5, "#FF4A22"), (1, "#C21A12")], "#F4ECE8", "#12060A", "#000000", dil, fa, fk, "R")
    img = s.makeImageSnapshot(); os.makedirs(OUT, exist_ok=True)
    big = f"{OUT}/kapak_{dil}_2560.png"; img.save(big, skia.kPNG)
    from PIL import Image
    im = Image.open(big).convert("RGB").resize((1280, 720), Image.LANCZOS)
    jp = f"{OUT}/kapak_{dil}.jpg"; im.save(jp, quality=92, optimize=True)
    print("ok", dil, fa, fk, jp, os.path.getsize(jp)); return jp

if __name__ == "__main__":
    for d in (sys.argv[1:] or ["tr"]): kapak(d)
