"""Motor demosu (~11 sn): kelimeye kilitli girişler, paralaks, ikincil hareket, duygu dönüşümü ve iki anlamsal geçiş.
  A "ev_dis"   : gece çiftlik evi. "penceresinde" kelimesinde pencere ışığı parlar.     → Maske("pencere") ile içeri girilir
  B "ic_mekan" : mum ışığında masa. "halka" kelimesinde kol halkası masaya düşer.        → NesneTasi("halka") ile halka uçar
  C "firtina"  : fırtınalı kıyı. Halka taşa oturur, "savaşa" kelimesinde şimşek + sarsıntı; duygu huzur → gerilim.
Çizimler bilerek basit: amaç görsel kalite değil hareket dilini göstermek.
    cd studyo/motor && python3 ornek/demo.py [onizle]
"""
import sys, os, math, random
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import skia
from sahne import *
from duygu import Duygu
from gecis import Film, Maske, NesneTasi, Kes

def P(h, a=1.0, stroke=0):
    p = paint(h, a)
    if stroke: p.setStyle(skia.Paint.kStroke_Style); p.setStrokeWidth(stroke)
    return p
def grad_v(y0, y1, c0, c1): return skia.Paint(Shader=skia.GradientShader.MakeLinear([(0, y0), (0, y1)], [hexcol(c0), hexcol(c1)]))
def radial(x, y, r, c, a): return skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeRadial((x, y), r, [hexcol(c, a), hexcol(c, 0)]))

# ── A: ev dışı
def gok(c, t, o):
    c.drawRect(skia.Rect(-1200, -700, 1200, 700), grad_v(-540, 540, "#0B1326", "#2B3550"))
    rnd = random.Random(4)
    for i in range(140):
        x, y = rnd.uniform(-1100, 1100), rnd.uniform(-560, 120); a = 0.35 + 0.35 * math.sin(t * 2 + i)
        c.drawCircle(x, y, rnd.uniform(0.8, 2.2), P("#E8EEFF", a))
def ay(c, t, o):
    c.drawCircle(0, 0, 220, radial(0, 0, 220, "#DDE6FF", 0.25)); c.drawCircle(0, 0, 58, P("#E9EEF8"))
    c.drawCircle(-14, -10, 12, P("#C9D0DE")); c.drawCircle(18, 14, 8, P("#C9D0DE"))
def tepe(renk, tepeler):
    def f(c, t, o):
        p = skia.Path(); p.moveTo(-1400, 400); [p.lineTo(x, y) for x, y in tepeler]; p.lineTo(1400, 400); p.close(); c.drawPath(p, P(renk))
    return f
def ev(c, t, o):
    c.drawRect(skia.Rect(-260, -170, 260, 140), grad_v(-170, 140, "#3A2A1E", "#21170F"))
    for i in range(-250, 260, 26): c.drawLine(i, -170, i, 140, P("#1A110B", 0.6, 2))
    roof = skia.Path(); roof.moveTo(-320, -160); roof.lineTo(0, -360); roof.lineTo(320, -160); roof.close(); c.drawPath(roof, grad_v(-360, -160, "#5A4A30", "#2E2416"))
    c.drawRect(skia.Rect(150, -330, 196, -230), P("#2A2018"))                         # baca
    c.drawRect(skia.Rect(-210, -10, -110, 140), P("#140D08"))                           # kapı
    c.drawRect(skia.Rect(40, -90, 200, 70), P("#0E0A08"))                               # pencere boşluğu (ışık ayrı öğe)
def pencere(c, t, o):
    c.drawCircle(0, 0, 330, radial(0, 0, 330, "#FFB45A", 0.35))
    c.drawRect(skia.Rect(-80, -80, 80, 80), P("#FFC877", 0.95))
    c.drawRect(skia.Rect(-80, -80, 80, 80), radial(0, 30, 110, "#FFF2C8", 0.8))
    c.drawLine(0, -80, 0, 80, P("#2A1A10", 1, 9)); c.drawLine(-80, 0, 80, 0, P("#2A1A10", 1, 9))
def duman(c, t, o):
    for i in range(7):
        k = ((t * 0.35 + i / 7) % 1.0); c.drawCircle(math.sin(k * 6 + i) * 30 * k, -k * 380, 26 + 60 * k, P("#8890A0", 0.22 * (1 - k)))
def cimen(c, t, o):
    rnd = random.Random(2)
    for i in range(170):
        x = rnd.uniform(-1100, 1100); h = rnd.uniform(60, 200); sw = math.sin(t * 1.6 + x * 0.01) * 18
        p = skia.Path(); p.moveTo(x, 0); p.quadTo(x + sw * 0.5, -h * 0.5, x + sw, -h); c.drawPath(p, P("#0B120C", 0.95, rnd.uniform(4, 9)))
    c.drawRect(skia.Rect(-1200, 0, 1200, 400), P("#070B08"))

A = Cekim("ev_dis", 4.6, kelimeler=[("Gece.", 0.2, 0.7), ("Evinin", 1.0, 1.4), ("penceresinde", 1.4, 2.1), ("bir", 2.1, 2.3), ("ışık", 2.3, 2.7), ("yanıyor.", 2.7, 3.3)],
          duygu=Duygu("yalnizlik").gecis("huzur", t0=1.4, sure=1.2))
A.ekle(Oge("gok", gok, derinlik=0.05), Oge("ay", ay, x=1460, y=230, derinlik=0.1, ikincil=[("suz", 0.6)]),
       Oge("tepe_uzak", tepe("#1C2438", [(-1400, 120), (-700, 10), (-200, 90), (400, -30), (1000, 70), (1400, 0)]), x=960, y=760, derinlik=0.3),
       Oge("tepe_yakin", tepe("#141A22", [(-1400, 160), (-500, 60), (300, 140), (900, 50), (1400, 120)]), x=960, y=860, derinlik=0.6),
       Oge("duman", duman, x=1133, y=520, derinlik=1.0),
       Oge("ev", ev, x=960, y=780, derinlik=1.0),
       Oge("pencere", pencere, x=1080, y=770, derinlik=1.0, giris=("parla", A.k("penceresinde", -0.1), 0.7), ikincil=[("alev", 0.4)]),
       Oge("cimen", cimen, x=960, y=1100, derinlik=1.45, blur=3))
A.kamera = Kamera(x=Iz([(0, 900), (4.6, 1070, "io")]), y=Iz([(0, 560), (4.6, 700, "io")]), z=Iz([(0, 1.0), (4.6, 1.22, "in")]))

# ── B: iç mekân
def duvar(c, t, o):
    c.drawRect(skia.Rect(-1100, -700, 1100, 700), grad_v(-600, 500, "#2C1C12", "#140C07"))
    for y in range(-560, 520, 70): c.drawLine(-1100, y, 1100, y + 6, P("#0F0905", 0.7, 5))
def masa(c, t, o):
    c.drawRect(skia.Rect(-700, 0, 700, 60), grad_v(0, 60, "#6A4A2C", "#3A2614")); c.drawRect(skia.Rect(-700, 60, 700, 420), P("#1E130A"))
def mum(c, t, o):
    c.drawRect(skia.Rect(-22, -120, 22, 0), grad_v(-120, 0, "#E8DCC0", "#B8A888"))
    c.save(); c.scale(1, o.durum.get("sy", 1)); fl = skia.Path(); fl.moveTo(0, -205); fl.quadTo(24, -150, 0, -122); fl.quadTo(-24, -150, 0, -205)
    c.drawPath(fl, P("#FFD27A")); c.restore()
def mum_isigi(c, t, o):
    k = 0.85 + 0.1 * math.sin(t * 13) * math.sin(t * 3.1)
    p = radial(0, 0, 900, "#FFB060", 0.42 * k); p.setBlendMode(skia.BlendMode.kScreen); c.drawCircle(0, 0, 900, p)
def halka_ciz(c, u=0):
    c.drawCircle(0, 0, 70, P("#2A1A06", 0.5, 30)); c.drawCircle(0, -4, 70, P("#C8962E", 1, 24)); c.drawCircle(-6, -10, 70, P("#FFE29A", 0.7, 6))
    for k in range(0, 360, 30):
        a = math.radians(k); c.drawCircle(math.cos(a) * 70, math.sin(a) * 70 - 4, 5, P("#7A5414"))
def halka(c, t, o): halka_ciz(c)

B = Cekim("ic_mekan", 4.4, kelimeler=[("İçeride,", 0.2, 0.8), ("babanın", 0.9, 1.4), ("halkası", 1.4, 2.0), ("masada.", 2.1, 2.8)], duygu=Duygu("huzur"))
B.ekle(Oge("duvar", duvar, derinlik=0.4), Oge("masa", masa, x=960, y=760, derinlik=1.0),
       Oge("mum", mum, x=640, y=760, derinlik=1.0, ikincil=[("alev", 1.0)]), Oge("isik", mum_isigi, x=640, y=560, derinlik=1.0),
       Oge("halka", halka, x=1080, y=700, s=Iz([(0, 1.0)]), derinlik=1.0, giris=("dus", B.k("halkası", -0.15), 0.8)))
B.kamera = Kamera(x=Iz([(0, 880), (4.4, 1040, "io")]), y=Iz([(0, 560), (4.4, 640)]), z=Iz([(0, 1.05), (4.4, 1.25, "io")]))

# ── C: fırtına kıyısı
def gok_f(c, t, o): c.drawRect(skia.Rect(-1200, -700, 1200, 700), grad_v(-540, 300, "#1A1F28", "#4A3A34"))
def deniz(c, t, o):
    c.drawRect(skia.Rect(-1200, 0, 1200, 500), grad_v(0, 400, "#1C2630", "#0A0E12"))
    for i in range(9):
        p = skia.Path(); y = 20 + i * 38; p.moveTo(-1200, y)
        for x in range(-1200, 1240, 60): p.lineTo(x, y + 10 * math.sin(x * 0.01 + t * (1.5 + i * 0.2) + i))
        c.drawPath(p, P("#5A6A78", 0.25, 3))
def tas(c, t, o):
    p = skia.Path(); p.moveTo(-260, 0); p.lineTo(-200, -120); p.lineTo(-40, -170); p.lineTo(150, -140); p.lineTo(270, 0); p.close(); c.drawPath(p, grad_v(-170, 0, "#4A4A4E", "#1E1E22"))
def yagmur(c, t, o):
    rnd = random.Random(9)
    for i in range(260):
        x0 = rnd.uniform(-1100, 1200); sp = rnd.uniform(900, 1400); y = (rnd.uniform(0, 1200) + t * sp) % 1200 - 600
        c.drawLine(x0 - y * 0.18, y, x0 - y * 0.18 - 10, y + 34, P("#A8B8C8", 0.35, 1.6))
def simsek(c, t, o):
    c.drawRect(skia.Rect(-2000, -1400, 2000, 1400), P("#E8F0FF", 0.75))   # saydamlık Oge katmanından gelir

C = Cekim("firtina", 4.4, kelimeler=[("Yıllar", 0.3, 0.7), ("sonra", 0.7, 1.0), ("aynı", 1.1, 1.4), ("halka", 1.4, 1.8), ("savaşa", 1.9, 2.5), ("gidiyor.", 2.5, 3.1)],
          duygu=Duygu("huzur").gecis("gerilim", t0=1.6, sure=0.9))
C.ekle(Oge("gok", gok_f, derinlik=0.05), Oge("deniz", deniz, x=960, y=640, derinlik=0.5),
       Oge("tas", tas, x=1000, y=900, derinlik=1.0), Oge("halka", halka, x=990, y=730, s=0.8, derinlik=1.0),
       Oge("yagmur", yagmur, derinlik=1.2, giris=("belir", C.k("savaşa", -0.3), 0.6)),
       Oge("simsek", simsek, derinlik=1.5, giris=("belir", C.k("savaşa"), 0.05), cikis=("belir", C.k("savaşa", 0.12), 0.35)))
C.kamera = Kamera(x=Iz([(0, 960), (4.4, 1000)]), y=Iz([(0, 600), (4.4, 640)]), z=Iz([(0, 1.25), (C.k("savaşa"), 1.12, "out"), (4.4, 1.0, "io")]),
                  sarsinti=[(C.k("savaşa"), 0.6, 14)])

FILM = Film([A, Maske("pencere", boyut=(160, 160), sure=1.1), B, NesneTasi("halka", "halka", halka_ciz, sure=1.2), C])

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out"); os.makedirs(out, exist_ok=True)
    if len(sys.argv) > 1 and sys.argv[1] == "onizle":
        print(FILM.onizle([0.5, 2.6, 3.9, 4.4, 5.6, 7.1, 7.9, 8.4, 9.9, 11.0], out)); sys.exit()
    print(FILM.render(f"{out}/demo.mp4"), f"{FILM.sure:.2f} sn", FILM.zaman_cizelgesi())
