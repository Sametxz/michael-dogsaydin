"""Prolog blok animatiği (F4b): 5 çekim + başlık kartı, kelimeye kilitli olaylar, anlamsal geçişler.
Döküm: dokum/prolog.json · Örgü: orgu/prolog_v1.md · Ses: ses/P0*.wav (yerel XTTS, geçici)
    python3 prolog.py onizle   → out/prolog_kare/*.png (960 px)
    python3 prolog.py render   → out/prolog_blok_960.mp4 (+ ses)
"""
import json, math, os, random, subprocess, sys
from pathlib import Path
P = Path(__file__).resolve().parent; REPO = P.parents[1]
sys.path[:0] = [str(REPO / "studyo/motor"), str(P), str(P / "stil"), str(REPO / "r3"), str(REPO / "r2")]
import numpy as np, soundfile as sf, skia
from sahne import *
from duygu import Duygu
from gecis import Film, Maske, ZoomIcinden, Eslesme, OnPlanSil, Kes, Karart
from kelime import zamanlar
import karakter as K
import stil_testi as ST

PLAN = "#7FE6FF"; OUT = P / "out"; SES = P / "ses"; OUT.mkdir(exist_ok=True)
FONT = skia.Typeface("DejaVu Sans", skia.FontStyle.Bold())

def Pn(h, a=1.0, w=0):
    p = paint(h, a)
    if w: p.setStyle(skia.Paint.kStroke_Style); p.setStrokeWidth(w); p.setStrokeCap(skia.Paint.kRound_Cap)
    return p
def grad_v(y0, y1, c0, c1): return skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(0, y0), (0, y1)], [hexcol(c0), hexcol(c1)]))
def radial(x, y, r, c, a): return skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeRadial((x, y), r, [hexcol(c, a), hexcol(c, 0)]))
def glow(h, a, w, blur=6):
    p = Pn(h, a, w); p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, blur)); return p
def metin(c, s, x, y, boy, renk, a=1.0, glow_=True, kirp=1.0):
    f = skia.Font(FONT, boy); w = f.measureText(s)
    c.save(); c.clipRect(skia.Rect(x - w / 2 - 10, y - boy * 1.2, x - w / 2 + (w + 20) * kirp, y + boy * 0.5))
    if glow_: c.drawString(s, x - w / 2, y, f, glow(renk, 0.8 * a, 0, 10))
    c.drawString(s, x - w / 2, y, f, Pn(renk, a)); c.restore()

# ── ses → kelime zamanları (çekim başına: önden boşluk + satırlar + aralar)
def cekim_sesi(ad, satirlar, on=0.35, ara=0.45, son=0.6):
    parcalar, sr = [], 24000
    parcalar.append(np.zeros(int(on * sr)))
    for i, s in enumerate(satirlar):
        y, sr = sf.read(SES / f"{s}.wav")
        son_kelime = zamanlar(str(SES / f"{s}.wav"))[-1][2]          # XTTS uydurma kuyruğunu kes
        y = y[: int((son_kelime + 0.15) * sr)]; parcalar.append(y)
        parcalar.append(np.zeros(int((ara if i < len(satirlar) - 1 else son) * sr)))
    y = np.concatenate(parcalar); yol = SES / f"{ad}.wav"; sf.write(yol, y, sr)
    return str(yol), len(y) / sr

def kilit(ck, adaylar, yedek_sira):
    for a in adaylar:
        try: return ck.k(a)
        except KeyError: pass
    return ck.kelimeler[min(yedek_sira, len(ck.kelimeler) - 1)][1]

def sprite_fig(svg, w=700, h=700, ay=660):
    return svg_sprite(f'<g transform="translate({w/2},{ay})">{svg}</g>', w, h, w / 2, ay, ss=1.0)
def ciz_sprite(sp): return lambda c, t, o: draw_sprite(c, sp)

# ════════════ P.01 · Fox River, gece
def gok(c, t, o):
    c.drawRect(skia.Rect(-1400, -900, 1400, 900), grad_v(-600, 500, "#060B16", "#1B2740"))
    r = random.Random(3)
    for i in range(160):
        x, y = r.uniform(-1300, 1300), r.uniform(-800, 200); c.drawCircle(x, y, r.uniform(0.8, 2.0), Pn("#DDE6FF", 0.3 + 0.3 * math.sin(t * 2 + i)))
def kule(c, t, o):
    c.drawRect(skia.Rect(-40, -420, 40, 0), grad_v(-420, 0, "#2A3242", "#151A24"))
    c.drawRect(skia.Rect(-90, -500, 90, -420), Pn("#1E2532")); c.drawRect(skia.Rect(-70, -485, 70, -440), Pn("#FFE8B0", 0.55))
    p = skia.Path(); p.moveTo(-110, -500); p.lineTo(0, -560); p.lineTo(110, -500); p.close(); c.drawPath(p, Pn("#131820"))
def projektor_isigi(c, t, o):
    ang = -0.9 + 0.75 * math.sin(t * 0.55)
    c.save(); c.rotate(math.degrees(ang))
    p = skia.Path(); p.moveTo(0, 0); p.lineTo(-170, 1500); p.lineTo(170, 1500); p.close()
    c.drawPath(p, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(0, 0), (0, 1500)], [hexcol("#FFF2C8", 0.42), hexcol("#FFF2C8", 0)])))
    c.restore(); c.drawCircle(0, 0, 30, radial(0, 0, 60, "#FFF6D8", 0.95))
def duvar(c, t, o):
    c.drawRect(skia.Rect(-1300, -330, 1300, 420), grad_v(-330, 420, "#4E5662", "#262B33"))
    for r_ in range(10):
        y = -330 + r_ * 75; off = 0 if r_ % 2 else 90
        c.drawLine(-1300, y, 1300, y, Pn("#20252C", 0.8, 3))
        for k in range(16):
            x = -1300 + off + k * 180; c.drawLine(x, y, x, y + 75, Pn("#20252C", 0.7, 3))
    c.drawRect(skia.Rect(-1300, -350, 1300, -320), Pn("#3A414C"))
    f = skia.Font(FONT, 64); c.drawString("FOX RIVER STATE PENITENTIARY", -560, -230, f, Pn("#C9CED6", 0.55))
def dikenli(c, t, o):
    for k in range(-14, 15):
        x = k * 95; c.drawCircle(x, 0, 38, Pn("#9AA3AE", 0.75, 3))
        for j in range(6):
            a = j * 1.05 + t * 0.1; c.drawLine(x + 38 * math.cos(a), 38 * math.sin(a), x + 48 * math.cos(a), 48 * math.sin(a), Pn("#BFC6CF", 0.8, 2))
def plan_duvar(c, t, o):   # duvarın plan çizgilerine çözülmüş hâli (camgöbeği)
    c.drawRect(skia.Rect(-1300, -330, 1300, 420), Pn("#071A2C", 0.92))
    for x in range(-1300, 1301, 40): c.drawLine(x, -330, x, 420, Pn("#1E4A6E", 0.35, 1))
    for y in range(-330, 421, 40): c.drawLine(-1300, y, 1300, y, Pn("#1E4A6E", 0.35, 1))
    hat = [(-900, -200, 900, -200), (-900, -200, -900, 300), (900, -200, 900, 300), (-900, 300, 900, 300), (-400, -200, -400, 300),
           (200, -200, 200, 100), (200, 100, 900, 100), (-900, 20, -400, 20), (500, 100, 500, 300)]
    for x0, y0, x1, y1 in hat:
        c.drawLine(x0, y0, x1, y1, glow(PLAN, 0.55, 8, 8)); c.drawLine(x0, y0, x1, y1, Pn(PLAN, 0.95, 3))
    for i in range(7):
        x = -860 + i * 60; c.drawRect(skia.Rect(x, -180, x + 44, -140), Pn(PLAN, 0.8, 2))
ROTA = [(-830, -150), (-830, 180), (-120, 180), (-120, -60), (380, -60), (380, 220), (820, 220)]
NOKTA = [(-830, -150), (-120, 180), (380, -60), (820, 220)]
def plan_noktalari(c, t, o):
    k = o.durum.get("ilerleme", 1.0)
    p = skia.Path(); p.moveTo(*ROTA[0]); [p.lineTo(*q) for q in ROTA[1:]]
    me = skia.PathMeasure(p, False); L = me.getLength(); seg = skia.Path(); me.getSegment(0, L * k, seg, True)
    pe = Pn(PLAN, 1.0, 7); pe.setPathEffect(skia.DashPathEffect.Make([26, 16], 0)); c.drawPath(seg, glow(PLAN, 0.6, 12, 8)); c.drawPath(seg, pe)
    f = skia.Font(FONT, 34)
    for i, (x, y) in enumerate(NOKTA):
        if k >= i / (len(NOKTA) - 1) - 0.02:
            c.drawCircle(x, y, 20, Pn(PLAN, 1, 4)); c.drawCircle(x, y, 22, glow(PLAN, 0.6, 6, 8)); c.drawString(f"{i+1:02d}", x + 26, y - 22, f, Pn(PLAN))
    if k > 0.98:
        c.drawLine(800, 200, 840, 240, Pn(PLAN, 1, 8)); c.drawLine(840, 200, 800, 240, Pn(PLAN, 1, 8))
def kinetik(s, renk=PLAN, boy=120):
    def f(c, t, o): metin(c, s, 0, 0, boy, renk, kirp=o.durum.get("kirp", 1.0))
    return f

def p01(kw, sure):
    ck = Cekim("P.01", sure, kelimeler=kw, duygu=Duygu("merak"))
    t_hap = kilit(ck, ["hapis"], 6); t_ezb = kilit(ck, ["ezber", "ez"], 7); t0 = ck.kelimeler[0][1]
    ck.ekle(Oge("gok", gok, derinlik=0.05),
            Oge("kule", kule, x=1500, y=640, derinlik=0.3),
            Oge("projektor", projektor_isigi, x=1500, y=150, derinlik=0.3, giris=("parla", t0 - 0.1, 0.6)),
            Oge("duvar", duvar, x=960, y=820, derinlik=0.7),
            Oge("plan_duvar", plan_duvar, x=960, y=820, derinlik=0.7, giris=("belir", t_hap - 0.1, 0.7)),
            Oge("plan_noktalari", plan_noktalari, x=960, y=820, derinlik=0.7, giris=("belir", t_ezb - 0.15, 0.2),
                eylemler=[(t_ezb - 0.15, 1.4, lambda p: {})]),
            Oge("ezbere", kinetik("EZBERE"), x=960, y=470, derinlik=0.85, giris=("ciz", t_ezb, 0.6)),
            Oge("dikenli", dikenli, x=960, y=410, derinlik=1.0, ikincil=[("titre", 0.4)]),
            Oge("cit", lambda c, t, o: [c.drawLine(x, -400, x, 400, Pn("#0A0D12", 1, 14)) for x in range(-1300, 1301, 110)], x=960, y=980, derinlik=1.4, blur=4))
    no = ck.oge("plan_noktalari"); te = t_ezb
    no.ciz = (lambda f: (lambda c, t, o: (o.durum.__setitem__("ilerleme", clamp((t - te + 0.1) / 1.5)), f(c, t, o))))(plan_noktalari)
    ez = ck.oge("ezbere"); ez.ciz = (lambda c, t, o: metin(c, "EZBERE", 0, 0, 120, PLAN, kirp=clamp((t - te) / 0.6)))
    ck.kamera = Kamera(x=Iz([(0, 1060), (sure, 900, "io")]), y=Iz([(0, 380), (sure, 640, "io")]), z=Iz([(0, 1.0), (sure, 1.15, "in")]))
    return ck

# ════════════ P.02 · hücre kapısını kendi çeker
def koridor(c, t, o):
    c.drawRect(skia.Rect(-1300, -800, 1300, 800), grad_v(-600, 600, "#3B4A44", "#1A221F"))
    for x in range(-1300, 1301, 160): c.drawLine(x, -800, x, 800, Pn("#2A3531", 0.6, 3))
def hucre_ic(c, t, o):
    c.drawRect(skia.Rect(-520, -520, 520, 420), grad_v(-520, 420, "#6B7478", "#3A4144"))
    for r_ in range(9):
        y = -520 + r_ * 104; c.drawLine(-520, y, 520, y, Pn("#4C5458", 0.8, 3))
    c.drawRect(skia.Rect(-480, 120, -180, 150), Pn("#2C3236")); c.drawRect(skia.Rect(-470, 96, -190, 122), Pn("#8D9488"))   # ranza
    c.drawRect(skia.Rect(260, 150, 400, 260), Pn("#C9CED2")); c.drawCircle(330, 150, 50, Pn("#AEB4B8"))                     # lavabo/klozet
    c.drawRect(skia.Rect(-520, 420, 520, 520), Pn("#2A2F31"))
def floresan(c, t, o):
    a = 0.75 + 0.25 * (1 if math.sin(t * 37) > -0.8 else 0.2)
    c.drawRect(skia.Rect(-200, -10, 200, 10), Pn("#E8FFF4", a)); c.drawCircle(0, 300, 800, radial(0, 300, 800, "#D8FFE8", 0.18 * a))
def parmaklik(c, t, o):
    for k in range(9):
        x = -520 + k * 130; c.drawRect(skia.Rect(x - 13, -600, x + 13, 600), grad_v(-600, 600, "#3C4246", "#1C2023"))
        c.drawLine(x - 6, -600, x - 6, 600, Pn("#7A848A", 0.5, 3))
    for y in (-420, 380): c.drawRect(skia.Rect(-560, y - 18, 560, y + 18), Pn("#2A2F33"))
def golge_parmak(c, t, o):
    for k in range(9): x = -520 + k * 130; c.drawRect(skia.Rect(x - 18, -800, x + 18, 800), Pn("#000000", 0.35))

def p02(kw, sure):
    ck = Cekim("P.02", sure, kelimeler=kw, duygu=Duygu("gerilim"))
    t_ken = kilit(ck, ["kendi"], 1); t_kil = kilit(ck, ["kilit", "kitle"], 3)
    pz = dict(govde=8, kol_on=(78, -20), el_on="grip", bas=2)
    mich = sprite_fig(K.figur2(K.MICHAEL, "kararli", pz), 760, 760, 720)
    kapi_x = Iz([(0, 560), (t_kil - 0.35, 560), (t_kil, 960, "in")])
    ck.ekle(Oge("koridor", koridor, derinlik=0.2),
            Oge("hucre", hucre_ic, x=960, y=560, derinlik=0.6),
            Oge("floresan", floresan, x=960, y=120, derinlik=0.6),
            Oge("michael", ciz_sprite(mich), x=1000, y=1000, s=1.15, derinlik=0.9, ikincil=[("nefes", 1)],
                eylemler=[(t_ken - 0.1, 0.5, lambda p: dict(dx=40 * p))]),
            Oge("golge", golge_parmak, x=kapi_x, y=560, derinlik=0.95, a=Iz([(0, 0), (t_kil, 0), (t_kil + 0.2, 1)])),
            Oge("kapi", parmaklik, x=kapi_x, y=560, derinlik=1.25))
    ck.kamera = Kamera(x=Iz([(0, 900), (sure, 960)]), y=540, z=Iz([(0, 1.08), (t_kil, 1.08), (sure, 1.0, "out")]), sarsinti=[(t_kil, 0.4, 16)])
    return ck

def perde(c, u):   # ön plan silme: tek kalın parmaklık geçer
    c.drawRect(skia.Rect(-160, -100, 160, H + 100), grad_v(0, H, "#30363A", "#111416")); c.drawLine(-60, -100, -60, H + 100, Pn("#7A848A", 0.5, 8))
    return 0

# ════════════ P.03 · sırttaki harita
SB = ST.STIL["B"]
def sirt_svg(isikli):
    body = ST.michael(SB)
    if not isikli: body = body.replace('filter="url(#glow)" opacity="0.95"', 'opacity="0"')
    return f'{ST.defs(SB)}{body}'
def hucre_duvar(c, t, o):
    c.drawRect(skia.Rect(-1200, -800, 1200, 800), grad_v(-600, 600, "#5C676E", "#30383E"))
    for r_ in range(14):
        y = -800 + r_ * 110; off = 0 if r_ % 2 else 120
        c.drawLine(-1200, y, 1200, y, Pn("#424A50", 0.9, 4))
        for k in range(10): x = -1200 + off + k * 240; c.drawLine(x, y, x, y + 110, Pn("#424A50", 0.8, 4))
    for k in range(4): c.drawRect(skia.Rect(400 + k * 140, -800, 440 + k * 140, 800), Pn("#000000", 0.18))
def havadaki_cizgiler(c, t, o):
    nab = 0.75 + 0.25 * math.sin(t * 5)
    yollar = [[(-120, 60), (-120, -40), (-40, -40), (-40, -160)], [(60, 80), (60, -20), (160, -20), (160, -140), (260, -140)],
              [(-260, -60), (-180, -60), (-180, -200)], [(-30, 0), (80, 0)]]
    for yol in yollar:
        p = skia.Path(); p.moveTo(*yol[0]); [p.lineTo(*q) for q in yol[1:]]
        c.drawPath(p, glow(PLAN, 0.5 * nab, 10, 9)); c.drawPath(p, Pn(PLAN, nab, 4))
    c.drawLine(-400, 120, 400, 120, glow(PLAN, 0.6, 10, 8)); c.drawLine(-400, 120, 400, 120, Pn(PLAN, 1, 4))   # eşleşme çizgisi
def p03(kw, sure):
    ck = Cekim("P.03", sure, kelimeler=kw, duygu=Duygu("merak"))
    t_har = kilit(ck, ["harita"], 3); t_ten = kilit(ck, ["ten"], 4); t_adam = kilit(ck, ["adam"], 6)
    s0 = svg_sprite(sirt_svg(False), 960, 600, 480, 330); s1 = svg_sprite(sirt_svg(True), 960, 600, 480, 330)
    ck.ekle(Oge("duvar", hucre_duvar, x=960, y=540, derinlik=0.4),
            Oge("sirt", ciz_sprite(s0), x=960, y=640, s=2.0, derinlik=1.0, ikincil=[("nefes", 1.5)]),
            Oge("dovme", ciz_sprite(s1), x=960, y=640, s=2.0, derinlik=1.0, ikincil=[("nefes", 1.5)], giris=("parla", t_har - 0.1, 0.5)),
            Oge("plan_cizgileri", havadaki_cizgiler, x=960, y=420, derinlik=1.15, giris=("yuksel", t_ten - 0.1, 0.8), ikincil=[("suz", 1.0)]),
            Oge("harita", kinetik("HARİTA", boy=110), x=960, y=230, derinlik=1.2, giris=("ciz", t_adam, 0.6)))
    hk = ck.oge("harita"); ta = t_adam; hk.ciz = lambda c, t, o: metin(c, "HARİTA", 0, 0, 110, PLAN, kirp=clamp((t - ta) / 0.6))
    ck.kamera = Kamera(x=Iz([(0, 940), (sure, 990)]), y=Iz([(0, 600), (sure, 520, "io")]), z=Iz([(0, 1.0), (sure, 1.18, "io")]))
    return ck

# ════════════ P.04 · karanlık depo, çocuk
def depo(c, t, o):
    c.drawRect(skia.Rect(-1300, -900, 1300, 900), Pn("#05070A"))
    for x in range(-1300, 1301, 120):   # tahta duvar kalasları, çok karanlık
        c.drawRect(skia.Rect(x, -900, x + 116, 300), Pn("#0C0F12")); c.drawLine(x, -900, x, 300, Pn("#000000", 0.9, 4))
    c.drawRect(skia.Rect(-1300, 300, 1300, 900), Pn("#07090B"))
def isik_cizgisi(c, t, o):
    c.drawRect(skia.Rect(-420, -6, 420, 6), Pn("#FFF1C8", 0.95)); c.drawRect(skia.Rect(-420, -6, 420, 6), glow("#FFE2A0", 0.8, 0, 14))
    p = skia.Path(); p.moveTo(-420, 6); p.lineTo(420, 6); p.lineTo(700, 420); p.lineTo(-700, 420); p.close()
    c.drawPath(p, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(0, 6), (0, 420)], [hexcol("#FFE6B0", 0.28), hexcol("#FFE6B0", 0)])))
    r = random.Random(5)
    for i in range(40):
        x = r.uniform(-500, 500); y = (r.uniform(0, 400) - t * 12) % 420; c.drawCircle(x, y, 1.6, Pn("#FFF1C8", 0.5))
def son_isik(c, t, o): c.drawRect(skia.Rect(-1300, -900, 1300, 900), Pn(PLAN, 0.55))
def cocuk_karanlik(sp):
    def f(c, t, o):
        draw_sprite(c, sp)
        g = skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(0, -660), (0, 0)], [hexcol("#000000", 0.55), hexcol("#000000", 0.2)]))
        c.drawRect(skia.Rect(-400, -700, 400, 40), g)
        h = skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(-200, 0), (160, 0)], [hexcol("#000000", 0.55), hexcol("#000000", 0)]))
        c.drawRect(skia.Rect(-400, -700, 400, 40), h)
    return f
def p04(kw, sure):
    ck = Cekim("P.04", sure, kelimeler=kw, duygu=Duygu("gerilim").gecis("korku", t0=0, sure=0.1))
    t_ama = kilit(ck, ["ama"], 0); t_yas = kilit(ck, ["yaşında", "yaş"], 5); t_kar = kilit(ck, ["karanlık"], 6)
    ck.duygu = Duygu("gerilim").gecis("korku", t0=t_kar, sure=1.0)
    cs = sprite_fig(K.figur2(K.MICHAEL_COCUK, "korku"), 700, 720, 690)
    ck.ekle(Oge("depo", depo, derinlik=0.3),
            Oge("isik_cizgisi", isik_cizgisi, x=960, y=930, derinlik=0.9),
            Oge("cocuk_ayak", cocuk_karanlik(cs), x=900, y=1330, s=2.3, derinlik=1.0, giris=("kay_sol", t_yas - 0.1, 0.6), ikincil=[("nefes", 1.5), ("titre", 0.3)]),
            Oge("cocuk_yuz", lambda c, t, o: None, x=930, y=330, derinlik=1.0, giris=("belir", t_kar, 0.4)),
            Oge("son_isik", son_isik, derinlik=1.5, cikis=("belir", t_ama, 0.25)))
    ck.kamera = Kamera(x=Iz([(0, 960), (sure, 930)]), y=Iz([(0, 880), (t_yas + 0.2, 880), (t_kar + 0.7, 430, "io"), (sure, 400)]),
                       z=Iz([(0, 1.0), (t_kar, 1.0), (sure, 1.12, "io")]), sarsinti=[(t_ama, 0.3, 6)])
    return ck

# ════════════ P.05 · ışığı sayan göz
def kapi_araligi(c, t, o):
    c.drawRect(skia.Rect(-900, -12, 900, 12), Pn("#FFF1C8", 0.95)); c.drawRect(skia.Rect(-900, -12, 900, 12), glow("#FFE2A0", 0.9, 0, 18))
    gx = (t * 260) % 2400 - 1200; c.drawRect(skia.Rect(gx, -12, gx + 160, 12), Pn("#000000", 0.75))   # ötesinden geçen gölge (açık döngü)
AYRINTI = [(-620, -180), (-300, -260), (180, -210), (520, -120), (-480, 60), (330, 40), (700, -40)]
def ayrinti_isiklari(c, t, o):
    t0 = o.durum.get("t0", 0)
    f = skia.Font(FONT, 30)
    for i, (x, y) in enumerate(AYRINTI):
        k = clamp((t - t0 - i * 0.28) / 0.25)
        if k <= 0: continue
        c.drawCircle(x, y, 12 * k, Pn(PLAN, 1, 3)); c.drawCircle(x, y, 16, glow(PLAN, 0.5 * k, 5, 6))
        c.drawLine(x - 40, y + 30, x + 50, y + 34, Pn(PLAN, 0.6 * k, 2))      # tahta çatlağı
        c.drawString(f"{i+1:02d}", x + 18, y - 16, f, Pn(PLAN, k))
def p05(kw, sure):
    ck = Cekim("P.05", sure, kelimeler=kw, duygu=Duygu("korku").gecis("merak", t0=0, sure=1))
    t_kap = kilit(ck, ["kapı"], 1); t_siz = kilit(ck, ["sızan", "sız"], 3); t_say = kilit(ck, ["sayıyor", "say"], 5)
    ck.duygu = Duygu("korku").gecis("merak", t0=t_say, sure=1.0)
    korku = svg_sprite(f'<g transform="translate(150,160)">{K.kafa(K.MICHAEL_COCUK, "3q", "korku")}</g>', 300, 320, 150, 160)
    plan_ = svg_sprite(f'<g transform="translate(150,160)">{K.kafa(K.MICHAEL_COCUK, "3q", "plan")}</g>', 300, 320, 150, 160)
    def yuz(sp):
        def f(c, t, o):
            draw_sprite(c, sp)
            h = skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(-120, 0), (60, 0)], [hexcol("#000000", 0.7), hexcol("#000000", 0)]))
            c.drawRect(skia.Rect(-150, -160, 150, 160), h)
        return f
    ck.ekle(Oge("depo", depo, derinlik=0.3),
            Oge("kapi_araligi", kapi_araligi, x=960, y=880, derinlik=0.6, eylemler=[(t_kap, 0.6, lambda p: dict(sy=1 + 1.2 * p))]),
            Oge("ayrinti_isiklari", ayrinti_isiklari, x=960, y=760, derinlik=0.7, giris=("belir", t_siz - 0.1, 0.2)),
            Oge("yuz_korku", yuz(korku), x=600, y=560, s=2.3, derinlik=1.1, ikincil=[("nefes", 2)], cikis=("belir", t_say, 0.5)),
            Oge("yuz_plan", yuz(plan_), x=600, y=560, s=2.3, derinlik=1.1, ikincil=[("nefes", 1)], giris=("belir", t_say, 0.5)))
    ai = ck.oge("ayrinti_isiklari"); ai.durum["t0"] = t_siz
    ck.kamera = Kamera(x=Iz([(0, 800), (sure, 940, "io")]), y=Iz([(0, 600), (t_say, 640), (sure, 760, "in")]), z=Iz([(0, 1.0), (t_say, 1.05), (sure, 1.3, "in")]))
    return ck

# ════════════ Başlık kartı
def baslik_ciz(c, t, o):
    c.drawRect(skia.Rect(-1300, -900, 1300, 900), grad_v(-600, 600, "#0B1C2E", "#050B14"))
    for x in range(-1300, 1301, 48): c.drawLine(x, -900, x, 900, Pn("#1E4A6E", 0.25, 1))
    for y in range(-900, 901, 48): c.drawLine(-1300, y, 1300, y, Pn("#1E4A6E", 0.25, 1))
    k = clamp(t / 1.6)
    metin(c, "MICHAEL SCOFIELD", 0, -40, 118, PLAN, kirp=k)
    metin(c, "OLARAK DOĞSAYDIN?", 0, 110, 84, "#F2F6FA", kirp=clamp((t - 0.6) / 1.4))
    c.drawLine(-700 * k, 170, 700 * k, 170, Pn(PLAN, 0.9, 3))
    tur = K.turna(1.0, isik=0.6, kanat=0.3 * math.sin(t * 4))
def baslik(sure=3.4):
    ck = Cekim("baslik", sure, kelimeler=[("", 0, 0.1)], duygu=Duygu("merak"))
    tsp = svg_sprite(f'<g transform="translate(160,120)">{K.turna(0.9, isik=0.7)}</g>', 320, 220, 160, 120)
    ck.ekle(Oge("baslik", baslik_ciz, derinlik=1.0),
            Oge("turna", ciz_sprite(tsp), x=Iz([(0, 1500), (sure, 1380)]), y=Iz([(0, 300), (sure, 260)]), derinlik=1.1, giris=("pop", 1.4, 0.5), ikincil=[("suz", 1.5)]))
    ck.kamera = Kamera(z=Iz([(0, 1.06), (sure, 1.0, "out")]))
    return ck

# ════════════ Film
CEKIMLER = [("P.01", ["P01a"], p01), ("P.02", ["P02a"], p02), ("P.03", ["P03a"], p03), ("P.04", ["P04a", "P04b", "P04c"], p04), ("P.05", ["P05a"], p05)]
def kur():
    cks, sesler = [], []
    for ad, satirlar, f in CEKIMLER:
        yol, sure = cekim_sesi(ad.replace(".", ""), satirlar, on=0.45 if ad != "P.01" else 0.3, son=0.9)
        kw = zamanlar(yol); cks.append(f(kw, max(sure, 3.2))); sesler.append(yol)
        print(ad, " ".join(f"{w}@{a:.2f}" for w, a, b in kw))
    B = baslik()
    film = Film([cks[0], ZoomIcinden((960 - 830 * 1.15 + 0, 540), sure=0.8, renk="#7FE6FF"), cks[1], OnPlanSil(perde, sure=0.7), cks[2],
                 Eslesme("plan_cizgileri", "isik_cizgisi", sure=0.9), cks[3], ZoomIcinden("cocuk_yuz", sure=0.8, renk="#000000"), cks[4],
                 Maske("kapi_araligi", boyut=(900, 26), sure=1.0), B])
    return film, sesler

def ses_miks(film, sesler, yol):
    sr = 24000; toplam = np.zeros(int((film.sure + 1) * sr))
    for (ad, bas, sure), s in zip(film.zaman_cizelgesi(), sesler):
        y, _ = sf.read(s); i = int(bas * sr); toplam[i:i + len(y)] += y[: len(toplam) - i]
    sf.write(yol, toplam, sr)

if __name__ == "__main__":
    film, sesler = kur()
    print("süre", round(film.sure, 2), film.zaman_cizelgesi())
    if sys.argv[1:] == ["onizle"]:
        ts = []
        for ad, bas, sure in film.zaman_cizelgesi(): ts += [bas + sure * 0.3, bas + sure * 0.75]
        print(film.onizle([round(t, 2) for t in ts], str(OUT / "prolog_kare"), olcek=0.5))
    elif sys.argv[1:] == ["render"]:
        v = OUT / "prolog_1080_tmp.mp4"; film.render(str(v), crf=26)
        ses_miks(film, sesler, str(OUT / "prolog_ses.wav"))
        son = OUT / "prolog_blok_960.mp4"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(v), "-i", str(OUT / "prolog_ses.wav"), "-vf", "scale=960:-2",
                        "-c:v", "libx264", "-preset", "veryfast", "-crf", "24", "-c:a", "aac", "-b:a", "128k", "-shortest", str(son)], check=True)
        v.unlink(); print(son)
