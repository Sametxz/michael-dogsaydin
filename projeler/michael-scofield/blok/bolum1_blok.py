"""F4b Bölüm I ("Turna") Blok Animatiği — Yüksek Tempolu, Canlı Kelime-Kelime Akış (960×540).

10 çekim (1.01–1.10) · 9/9 (%100) anlamsal geçiş · Kilitli F3 varlıkları (Turna v4, 11 Yaş v3, Lincoln v1, Depo).
Çıktılar:
  - blok/bolum1_kontakt_960.png    (16 karelik kontakt: 10 çekim + 6 kritik geçiş orta karesi)
  - blok/bolum1_blok_960.mp4       (960×540 blok animatik)
"""
import math, os, sys
from pathlib import Path
import skia
from PIL import Image, ImageDraw, ImageFont

P = Path(__file__).resolve().parent
PROJE = P.parent
REPO = PROJE.parents[1]
sys.path[:0] = [str(REPO / "studyo/motor"), str(PROJE), str(REPO / "r3"), str(REPO / "r2")]

from sahne import W, H, FPS, Iz, sabit, Oge, Kamera, Cekim, svg_sprite, draw_sprite, paint, hexcol, clamp, ease
from duygu import Duygu
from gecis import Film, ZoomIcinden, OnPlanSil, Eslesme, Maske, NesneTasi, Savurma
import karakter as K

PLAN_C = "#7FE6FF"
ALTIN = "#FFD88A"
KIRMIZI = "#FF5A3C"
INK = "#15110E"

def _tf(bold=False):
    for name in ("AlegreyaSC-Bold.ttf" if bold else "Alegreya.ttf", "Cinzel.ttf"):
        p = REPO / "fonts" / name
        if p.exists():
            tf = skia.Typeface.MakeFromFile(str(p))
            if tf:
                return tf
    return skia.Typeface("Arial", skia.FontStyle.Bold() if bold else skia.FontStyle.Normal())

TF_REG = _tf(False)
TF_BOLD = _tf(True)

def _yazi(c, metin, x, y, boyut=36, renk="#FFFFFF", a=1.0, bold=True, align="center"):
    font = skia.Font(TF_BOLD if bold else TF_REG, boyut)
    w = font.measureText(metin)
    tx = x - w / 2 if align == "center" else (x - w if align == "right" else x)
    c.drawString(metin, tx, y, font, paint(renk, a))

def _damga(c, metin, x, y, p, renk=PLAN_C, boyut=30):
    if p <= 0.01:
        return
    sc = 1.3 - 0.3 * ease("back", clamp(p))
    al = clamp(p * 2.2)
    c.save()
    c.translate(x, y); c.scale(sc, sc)
    font = skia.Font(TF_BOLD, boyut)
    tw = font.measureText(metin)
    rect = skia.Rect(-tw/2 - 18, -boyut/2 - 10, tw/2 + 18, boyut/2 + 8)
    c.drawRect(rect, paint("#07121E", 0.84 * al))
    c.drawRect(rect, paint(renk, 0.95 * al, Style=skia.Paint.kStroke_Style, StrokeWidth=2.6))
    _yazi(c, metin, 0, boyut * 0.30, boyut, renk, al, bold=True, align="center")
    c.restore()

def _hud(cid, cumle, kw_fn):
    def _ciz(c, t):
        c.drawRect(skia.Rect(0, H - 64, W, H), paint("#070B12", 0.78))
        c.drawLine(0, H - 64, W, H - 64, paint(PLAN_C, 0.4, StrokeWidth=2))
        _yazi(c, cid, 68, H - 23, 21, PLAN_C, 0.95, bold=True, align="left")
        _yazi(c, cumle, W / 2, H - 23, 23, "#EEF3F8", 0.94, bold=False, align="center")
        kw = kw_fn(t)
        if kw:
            _yazi(c, f"«{kw}»", W - 58, H - 23, 20, ALTIN, 0.98, bold=True, align="right")
    return _ciz

# ───────── Kilitli F3 Sprite'ları
def _sp_turna(isik=0.7, kanat=0.0):
    body = f'<g transform="translate(150,120) scale(0.95)">{K.turna(1.0, isik=isik, kanat=kanat)}</g>'
    return svg_sprite(body, 300, 240, ax=150, ay=120, ss=0.85)

def _sp_cocuk_korku():
    body = f'<g transform="translate(170,170) scale(1.2)">{K.michael_cocuk_kafa("3q", "korku", lighting="prolog")}</g>'
    return svg_sprite(body, 340, 340, ax=170, ay=170, ss=0.8)

def _sp_lincoln_sefkat():
    body = f'<g transform="translate(170,175) scale(1.12)">{K.lincoln_kafa("3q", "sefkat", boyun=True)}</g>'
    return svg_sprite(body, 340, 350, ax=170, ay=175, ss=0.8)

def _sp_lincoln_odak():
    body = f'<g transform="translate(170,175) scale(1.12)">{K.lincoln_kafa("front", "odak", boyun=True)}</g>'
    return svg_sprite(body, 340, 350, ax=170, ay=175, ss=0.8)

def _sp_depo():
    # A1 lore uyumu: 1.04'te henüz turna yok (turna ilk kez 1.05'te belirir) → sahne katmanı hariç, yumuşak ışık ayrı çizilir
    defs, body = K.mekan_depo(katmanlar=["uzak", "orta"], plan_gorusu=False)
    return svg_sprite(body, 960, 540, ax=480, ay=270, ss=1.0, defs=f"<defs>{defs}</defs>")

SP_TURNA = _sp_turna(0.7, 0.0)
SP_TURNA_UC = _sp_turna(0.5, 0.7)
SP_COCUK = _sp_cocuk_korku()
SP_LINC_S = _sp_lincoln_sefkat()
SP_LINC_O = _sp_lincoln_odak()
SP_DEPO = _sp_depo()

# ───────── 1.01 · Baba kapıdan çıkar, BURROWS → SCOFIELD
def build_101():
    kw = [("baban", 0.35, 1.0), ("gidiyor", 1.35, 2.0), ("soyadın", 2.25, 3.1)]
    ck = Cekim("1.01", sure=3.6, kelimeler=kw, duygu=Duygu("huzur").gecis("yalnizlik", t0=1.35, sure=0.9), arka="#12161E")

    def ciz_ev(c, t, o):
        # sıcak ev içi → kapı kapanınca soğuk koridor
        p = ease("out", clamp((t - 1.35) / 0.55))
        c.drawRect(skia.Rect(-W, -H, W, H), paint("#1E242E"))
        # kapı çerçevesi
        c.drawRect(skia.Rect(-220, -340, 220, 420), paint("#0C1118"))
        # dışarıdan gelen yağmurlu sokak ışığı (kapı kapanınca kısılır)
        c.drawRect(skia.Rect(-200, -320, 200 * (1 - p * 0.92), 400), paint("#FFE0A8", 0.55 * (1 - p * 0.85)))
        # kapı kanadı
        c.drawRect(skia.Rect(-200 + 380 * (1 - p), -320, 200, 400), paint("#3D2B22"))
        c.drawRect(skia.Rect(-200 + 380 * (1 - p), -320, 200, 400), paint(INK, 0.9, Style=skia.Paint.kStroke_Style, StrokeWidth=4))

    def ciz_baba(c, t, o):
        p = clamp((t - 0.35) / 1.0)
        if p >= 0.95:
            return
        dx = -20 + 210 * ease("in", p)
        al = 1.0 - p
        c.save(); c.translate(dx, 20)
        c.drawOval(skia.Rect(-42, -230, 42, -145), paint("#0A0D12", al))
        c.drawRect(skia.Rect(-75, -145, 75, 240), paint("#0A0D12", al))
        c.restore()

    def ciz_plaka(c, t, o):
        # pirinç plaka: BURROWS → ters dönerek SCOFIELD!
        p = ease("io", clamp((t - 2.25) / 0.55))
        sy = abs(math.cos(p * math.pi))
        c.save(); c.scale(1.0, max(0.08, sy))
        c.drawRect(skia.Rect(-175, -46, 175, 46), paint("#C89B54"))
        c.drawRect(skia.Rect(-175, -46, 175, 46), paint(INK, 0.9, Style=skia.Paint.kStroke_Style, StrokeWidth=4))
        lbl = "BURROWS" if p < 0.5 else "SCOFIELD"
        col = "#24190E" if p < 0.5 else "#071824"
        _yazi(c, lbl, 0, 14, 40, col, 0.98, bold=True)
        c.restore()
        if 0.4 < p < 0.95:
            c.drawRect(skia.Rect(-182, -52, 182, 52), paint(PLAN_C, 0.85 * (1 - abs(p - 0.65) * 3), Style=skia.Paint.kStroke_Style, StrokeWidth=4))

    ck.ekle(
        Oge("ev_kapisi", ciz_ev, derinlik=0.7),
        Oge("baba_golge", ciz_baba, x=W/2 - 60, y=H/2 + 40, derinlik=0.85),
        Oge("soyadi_plaka", ciz_plaka, x=W/2, y=H/2 + 45, derinlik=1.05, giris=("pop", 2.0, 0.3)),
    )
    ck.kamera = Kamera(z=Iz([(0, 1.0), (1.4, 1.12, "out"), (3.6, 1.24, "io")]), sarsinti=[(1.55, 0.25, 16)])
    ck.ust.append(_hud("1.01", "Henüz doğmadan baban kapıdan çıkıp gidiyor. Soyadın değişiyor.",
                       lambda t: "soyadın" if t >= 2.25 else ("gidiyor" if t >= 1.35 else ("baban" if t >= 0.35 else ""))))
    return ck

def ciz_kapi_sil(c, u):
    c.drawRect(skia.Rect(-110, 0, 110, H), paint("#2B1E18"))
    c.drawRect(skia.Rect(85, 0, 110, H), paint("#080A0F", 0.8))

# ───────── 1.02 · 11 yaş, soğuyan fincan, camda iki çocuk + '?'
def build_102():
    kw = [("yaşına", 0.30, 0.95), ("ölüyor", 1.50, 2.20), ("söyleniyor", 2.75, 3.60)]
    ck = Cekim("1.02", sure=4.2, kelimeler=kw, duygu=Duygu("huzur").gecis("yas", t0=1.50, sure=0.9), arka="#111822")

    def ciz_mutfak(c, t, o):
        c.drawRect(skia.Rect(-W, -H, W, H), paint("#18212C"))
        # mutfak masası
        c.drawRect(skia.Rect(-960, 140, 960, 540), paint("#2E231D"))
        c.drawLine(-960, 140, 960, 140, paint(INK, 0.85, Style=skia.Paint.kStroke_Style, StrokeWidth=4))

    def ciz_pencere(c, t, o):
        # mutfak penceresi (sağ-orta) + yağmur + iki çocuk silueti + ince '?'
        c.drawRect(skia.Rect(-220, -200, 220, 140), paint("#0E1A2B"))
        c.drawRect(skia.Rect(-220, -200, 220, 140), paint("#435468", 0.9, Style=skia.Paint.kStroke_Style, StrokeWidth=10))
        c.drawLine(0, -200, 0, 140, paint("#435468", 0.9, Style=skia.Paint.kStroke_Style, StrokeWidth=6))
        c.drawLine(-220, -30, 220, -30, paint("#435468", 0.9, Style=skia.Paint.kStroke_Style, StrokeWidth=6))
        # yağmur damlaları
        for i in range(14):
            rx = -190 + (i * 31) % 380
            ry = -180 + ((i * 53 + t * 90) % 300)
            c.drawLine(rx, ry, rx - 3, ry + 16, paint("#9BC2E0", 0.45, Style=skia.Paint.kStroke_Style, StrokeWidth=2))
        # iki çocuk silueti + '?'
        p = ease("out", clamp((t - 2.65) / 0.6))
        if p > 0:
            # büyük ağabey (15 yaş) + küçük kardeş (11 yaş)
            c.drawCircle(-45, 25, 28, paint("#070C14", 0.85 * p))
            c.drawRect(skia.Rect(-85, 55, -5, 138), paint("#070C14", 0.85 * p))
            c.drawCircle(38, 52, 22, paint("#070C14", 0.85 * p))
            c.drawRect(skia.Rect(8, 76, 68, 138), paint("#070C14", 0.85 * p))
            _yazi(c, "?", 130, -65, 86, PLAN_C, 0.92 * p, bold=True)

    def ciz_fincanlar(c, t, o):
        # iki çay fincanı + buharı "ölüyor"da aniden kesilir
        buhar_a = 1.0 - clamp((t - 1.50) / 0.28)
        for fx in (-120, 60):
            c.drawRect(skia.Rect(fx - 38, -20, fx + 38, 52), paint("#D8D2C5"))
            c.drawRect(skia.Rect(fx - 38, -20, fx + 38, 52), paint(INK, 0.85, Style=skia.Paint.kStroke_Style, StrokeWidth=3))
            c.drawArc(skia.Rect(fx + 28, -6, fx + 58, 36), -90, 180, False, paint("#D8D2C5", 1.0, Style=skia.Paint.kStroke_Style, StrokeWidth=6))
            if buhar_a > 0.02:
                for k in (-12, 12):
                    sw = math.sin(t * 4 + k) * 8
                    c.drawLine(fx + k, -30, fx + k + sw, -95, paint("#FFFFFF", 0.45 * buhar_a, Style=skia.Paint.kStroke_Style, StrokeWidth=4))
        _damga(c, "11 YAŞ", -340, -190, clamp((t - 0.30) / 0.3) * (1.0 - clamp((t - 3.3) / 0.4)), ALTIN, boyut=30)

    ck.ekle(
        Oge("mutfak", ciz_mutfak, derinlik=0.5),
        Oge("mutfak_pencere", ciz_pencere, x=W/2 + 190, y=H/2 - 60, derinlik=0.8),
        Oge("cay_fincan", ciz_fincanlar, x=W/2 - 220, y=H/2 + 155, derinlik=1.05, giris=("pop", 0.2, 0.35)),
    )
    ck.kamera = Kamera(
        x=Iz([(0, W/2 - 120), (2.2, W/2 + 60, "io"), (4.2, W/2 + 165, "in")]),
        y=Iz([(0, H/2 + 30), (4.2, H/2 - 55, "io")]),
        z=Iz([(0, 1.0), (4.2, 1.24, "io")]),
    )
    ck.ust.append(_hud("1.02", "On bir yaşına geldiğinde annen ölüyor. En azından sana öyle söyleniyor.",
                       lambda t: "söyleniyor" if t >= 2.75 else ("ölüyor" if t >= 1.50 else ("yaşına" if t >= 0.30 else ""))))
    return ck

# ───────── 1.03 · Lincoln ıslahevinde, koruyucu ev depo sürgüsü kapanır
def build_103():
    kw = [("lincoln", 0.35, 1.0), ("koruyucu", 1.55, 2.2), ("kilitliyor", 2.40, 3.2)]
    ck = Cekim("1.03", sure=3.8, kelimeler=kw, duygu=Duygu("yalnizlik").gecis("korku", t0=2.40, sure=0.7), arka="#0A0E16")

    def ciz_koridor(c, t, o):
        # R7 çözümü: soğuk tavan ampul huzmesi + net parmaklık ve koridor derinliği
        sh = skia.GradientShader.MakeRadial((-320, -280), 680, [hexcol("#3A526B", 0.72), hexcol("#0E1520", 1.0)])
        c.drawRect(skia.Rect(-W, -H, W, H), skia.Paint(Shader=sh))
        # solda parmaklık ardında genç Lincoln silueti (omuzlu, kenar ışıklı)
        p_l = clamp((t - 0.35) / 1.0)
        c.save(); c.translate(-340 - 35 * p_l, 25)
        c.drawCircle(0, -155, 42, paint("#2B394A", 0.95))
        body = skia.Path()
        body.moveTo(-88, 220); body.quadTo(-82, -85, -35, -108); body.lineTo(35, -108); body.quadTo(82, -85, 88, 220); body.close()
        c.drawPath(body, paint("#253344", 0.95))
        c.drawPath(body, paint("#8EB4D4", 0.45, Style=skia.Paint.kStroke_Style, StrokeWidth=3))
        for bx in range(-125, 145, 48):
            c.drawRect(skia.Rect(bx - 6, -340, bx + 6, 340), paint("#0C121A"))
            c.drawLine(bx - 5, -340, bx - 5, 340, paint("#6A85A0", 0.5, Style=skia.Paint.kStroke_Style, StrokeWidth=2))
        c.restore()
        _damga(c, "ISLAHEVİ", -360, -245, clamp((t - 0.45) / 0.3) * (1.0 - clamp((t - 2.2) / 0.3)), "#9FB4C8", boyut=26)

    def ciz_depo_kapi_ve_surgu(c, t, o):
        # sağdan kapanan ağır ahşap depo kapısı + R7 metalik kenar ışıklı sürgü
        pk = ease("out", clamp((t - 1.55) / 0.55))
        kx = 540 * (1 - pk)
        c.save(); c.translate(kx, 0)
        c.drawRect(skia.Rect(-260, -420, 460, 420), paint("#3D2E24"))
        for tx in range(-240, 440, 75):
            c.drawLine(tx, -420, tx, 420, paint("#1A120D", 0.85, Style=skia.Paint.kStroke_Style, StrokeWidth=4))
        c.drawLine(-260, -420, -260, 420, paint("#A8C2D8", 0.45, Style=skia.Paint.kStroke_Style, StrokeWidth=4))
        # ağır demir sürgü ("kilitliyor"da şak diye sola kayar + parlak metalik üst kenar!)
        ps = ease("expo", clamp((t - 2.40) / 0.25))
        c.drawRect(skia.Rect(-225, -28, 185, 28), paint("#1E2833"))
        c.drawRect(skia.Rect(-225, -28, 185, 28), paint("#7A94AD", 0.65, Style=skia.Paint.kStroke_Style, StrokeWidth=2.5))
        c.drawRect(skia.Rect(-140 - 110 * ps, -15, 140 - 110 * ps, 15), paint("#8EA4B8"))
        c.drawLine(-140 - 110 * ps, -14, 140 - 110 * ps, -14, paint("#E2EEF8", 0.9, Style=skia.Paint.kStroke_Style, StrokeWidth=3))
        c.drawRect(skia.Rect(-140 - 110 * ps, -15, 140 - 110 * ps, 15), paint(INK, 0.9, Style=skia.Paint.kStroke_Style, StrokeWidth=3))
        if 0.65 < ps < 1.0:
            c.drawCircle(-220, 0, 56 * (1 - (ps - 0.65) / 0.35), paint(ALTIN, 0.9))
        c.restore()
        _damga(c, "KİLİT", 120, -125, clamp((t - 2.45) / 0.25), ALTIN, boyut=32)

    ck.ekle(
        Oge("lincoln_genc", ciz_koridor, derinlik=0.65),
        Oge("kilit_surgu", ciz_depo_kapi_ve_surgu, x=W/2 + 120, y=H/2, derinlik=1.0),
    )
    ck.kamera = Kamera(
        x=Iz([(0, W/2 - 140), (1.8, W/2 + 80, "out"), (3.8, W/2 + 120, "io")]),
        z=Iz([(0, 1.0), (2.4, 1.15, "out"), (3.8, 1.32, "in")]),
        sarsinti=[(2.48, 0.30, 20)],
    )
    ck.ust.append(_hud("1.03", "Ağabeyin Lincoln ıslahevinde. Seni koruyucu aile karanlık bir depoya kilitliyor.",
                       lambda t: "kilitliyor" if t >= 2.40 else ("koruyucu" if t >= 1.55 else ("lincoln" if t >= 0.35 else ""))))
    return ck

# ───────── 1.04 · Vurucu an! Düşük örtük ketlenme: canlı CAD tarama + 01–06 + HER ŞEYİ GÖRÜYORSUN
def build_104():
    kw = [("karanlıkta", 0.25, 0.95), ("süzemiyor", 1.35, 2.2), ("görüyorsun", 2.55, 3.6)]
    ck = Cekim("1.04", sure=4.3, kelimeler=kw, duygu=Duygu("korku").gecis("merak", t0=2.55, sure=0.8), arka="#060A12")

    def ciz_depo_oda(c, t, o):
        c.save(); c.scale(2.05, 2.05); draw_sprite(c, SP_DEPO); c.restore()
        # yumuşak altın kapı altı ışık huzmesi (turna YOK!)
        sh = skia.GradientShader.MakeLinear([(0, 95), (0, 290)], [hexcol(ALTIN, 0.52), hexcol(ALTIN, 0.0)])
        beam = skia.Path()
        beam.moveTo(-210, 95); beam.lineTo(210, 95); beam.lineTo(410, 290); beam.lineTo(-410, 290); beam.close()
        c.drawPath(beam, skia.Paint(AntiAlias=True, Shader=sh, BlendMode=skia.BlendMode.kScreen))

    def ciz_cocuk(c, t, o):
        # sol-altta 11 yaş Michael portre (omuz+boyunlu, R4 temiz)
        sh = skia.Path()
        sh.moveTo(-180, 320); sh.quadTo(-160, 155, -58, 132); sh.lineTo(58, 132); sh.quadTo(160, 155, 180, 320); sh.close()
        c.drawPath(sh, paint("#2B1917"))
        c.drawRect(skia.Rect(-30, 82, 30, 155), paint("#7A5945"))
        c.save(); c.scale(1.45, 1.45); draw_sprite(c, SP_COCUK); c.restore()
        # "görüyorsun"da gözlerde camgöbeği parıltı
        gp = clamp((t - 2.55) / 0.4)
        if gp > 0:
            c.drawCircle(20, -15, 6 * gp, paint(PLAN_C, 0.95))
            c.drawCircle(-32, -15, 5.5 * gp, paint(PLAN_C, 0.95))

    def ciz_cad_tarama(c, t, o):
        # canlı CAD lazer tarama: soldan sağa tüm depo ayrıntılarını çizer!
        p = ease("out", clamp((t - 1.35) / 1.0))
        if p <= 0:
            return
        sx = -760 + 1520 * p
        c.save(); c.clipRect(skia.Rect(-760, -400, sx, 400))
        gp = paint(PLAN_C, 0.85, Style=skia.Paint.kStroke_Style, StrokeWidth=2.6)
        # çatlaklar, sandık kenarları ve yatay eşleşme çatlağı
        c.drawLine(-520, -280, -490, 160, gp)
        c.drawLine(360, -260, 390, 180, gp)
        c.drawLine(-340, 120, 340, 120, paint(PLAN_C, 0.98, Style=skia.Paint.kStroke_Style, StrokeWidth=5))
        c.drawRect(skia.Rect(-640, 40, -340, 260), gp)
        c.drawRect(skia.Rect(340, 60, 620, 260), gp)
        c.restore()
        if p < 0.99:
            c.drawLine(sx, -420, sx, 420, paint("#FFFFFF", 0.95, Style=skia.Paint.kStroke_Style, StrokeWidth=4))
            c.drawLine(sx, -420, sx, 420, paint(PLAN_C, 0.5, Style=skia.Paint.kStroke_Style, StrokeWidth=14))

    def ciz_noktalar(c, t, o):
        pts = [(-505, -140, "01"), (-485, 60, "02"), (-120, -190, "03"), (200, -160, "04"), (375, -40, "05"), (0, 120, "06")]
        for i, (px, py, lbl) in enumerate(pts):
            pi = ease("back", clamp((t - (2.55 + i * 0.12)) / 0.18))
            if pi <= 0:
                continue
            c.drawCircle(px, py, 14 * pi, paint(PLAN_C, 0.95, Style=skia.Paint.kStroke_Style, StrokeWidth=3))
            c.drawCircle(px, py, 4.5 * pi, paint("#FFFFFF", 1.0))
            _yazi(c, lbl, px + 20, py - 8, 20, PLAN_C, clamp(pi), bold=True, align="left")
        _damga(c, "HER ŞEYİ GÖRÜYORSUN", 140, -270, clamp((t - 2.80) / 0.30), PLAN_C, boyut=36)

    ck.ekle(
        Oge("depo", ciz_depo_oda, derinlik=0.55),
        Oge("cocuk_michael", ciz_cocuk, x=W/2 - 390, y=H/2 + 125, derinlik=0.92, ikincil=[("nefes", 1.5)]),
        Oge("tahta_catlak", ciz_cad_tarama, x=W/2, y=H/2 + 120, derinlik=1.0),
        Oge("plan_noktalar", ciz_noktalar, x=W/2, y=H/2, derinlik=1.1),
    )
    ck.kamera = Kamera(
        x=Iz([(0, W/2 - 220), (1.4, W/2, "out"), (4.3, W/2 + 40, "io")]),
        z=Iz([(0, 1.24), (1.4, 1.02, "out"), (4.3, 1.16, "io")]),
    )
    ck.ust.append(_hud("1.04", "Karanlıkta beynin ayrıntıları süzemiyor. Düşük örtük ketlenme: her şeyi görüyorsun.",
                       lambda t: "görüyorsun" if t >= 2.55 else ("süzemiyor" if t >= 1.35 else ("karanlıkta" if t >= 0.25 else ""))))
    return ck

# ───────── 1.05 · Ertesi sabah, kilitli Turna v4 + BURADAYIM (soğuk → sıcak altın!)
def build_105():
    kw = [("sabah", 0.25, 0.9), ("turna", 1.30, 2.05), ("buradayım", 2.45, 3.45)]
    ck = Cekim("1.05", sure=4.2, kelimeler=kw, duygu=Duygu("yalnizlik").gecis("umut", t0=1.15, sure=0.9), arka="#1B1814")

    def ciz_yatak(c, t, o):
        # sıcak sabah çarşafı ve ahşap başucu
        sh = skia.GradientShader.MakeLinear([(0, -H/2), (0, H/2)], [hexcol("#3A2F24"), hexcol("#D4C4A8")])
        c.drawRect(skia.Rect(-W, -H, W, H), skia.Paint(Shader=sh))
        # güneş pencere şeridi (yatay altın huzme)
        p = ease("out", clamp((t - 0.25) / 0.8))
        sh2 = skia.GradientShader.MakeLinear([(-400, -100), (400, 180)], [hexcol("#FFF3C4", 0.65 * p), hexcol(ALTIN, 0.05)])
        beam = skia.Path()
        beam.moveTo(-620, -240); beam.lineTo(620, -240); beam.lineTo(760, 240); beam.lineTo(-480, 240); beam.close()
        c.drawPath(beam, skia.Paint(AntiAlias=True, Shader=sh2, BlendMode=skia.BlendMode.kScreen))

    def ciz_turna(c, t, o):
        c.save(); c.scale(1.65, 1.65); draw_sprite(c, SP_TURNA); c.restore()

    def ciz_buradayim(c, t, o):
        _damga(c, "BURADAYIM", 0, -245, clamp((t - 2.45) / 0.35), ALTIN, boyut=46)

    ck.ekle(
        Oge("sabah_isigi", ciz_yatak, derinlik=0.5),
        Oge("turna", ciz_turna, x=W/2, y=H/2 + 40, derinlik=1.0, giris=("dus", ck.k("turna"), 0.55), ikincil=[("suz", 0.35)]),
        Oge("buradayim_yazi", ciz_buradayim, x=W/2, y=H/2, derinlik=1.15),
    )
    ck.kamera = Kamera(y=Iz([(0, H/2 + 30), (4.2, H/2 - 25, "io")]), z=Iz([(0, 1.0), (4.2, 1.22, "io")]))
    ck.ust.append(_hud("1.05", "Ertesi sabah yatağının yanında bir kâğıt turna buluyorsun. Lincoln'ün işareti: Buradayım.",
                       lambda t: "buradayım" if t >= 2.45 else ("turna" if t >= 1.30 else ("sabah" if t >= 0.25 else ""))))
    return ck

def ciz_ucan_turna(c, u):
    # NesneTasi için kanat çırpan Turna v4
    sp = SP_TURNA_UC if (int(u * 8) % 2 == 0) else SP_TURNA
    c.save(); c.scale(1.3, 1.3); draw_sprite(c, sp); c.restore()

# ───────── 1.06 · Lise sırası, 3 hızlı origami katlama, 5 turna havalanır
def build_106():
    kw = [("lisede", 0.25, 0.85), ("origamiyi", 1.20, 1.95), ("dilin", 2.25, 3.10)]
    ck = Cekim("1.06", sure=3.6, kelimeler=kw, duygu=Duygu("umut"), arka="#1D222B")

    def ciz_sinif(c, t, o):
        c.drawRect(skia.Rect(-W, -H, W, H), paint("#212A34"))
        # okul sırası yüzeyi
        c.drawRect(skia.Rect(-680, 40, 680, 440), paint("#9C744E"))
        c.drawRect(skia.Rect(-680, 40, 680, 440), paint(INK, 0.8, Style=skia.Paint.kStroke_Style, StrokeWidth=4))
        _damga(c, "LİSE · ORIGAMI", -410, -230, clamp((t - 0.25) / 0.30), ALTIN, boyut=28)

    def ciz_turna_in(c, t, o):
        c.save(); c.scale(1.1, 1.1); draw_sprite(c, SP_TURNA); c.restore()

    def ciz_katlama_ve_suru(c, t, o):
        # 3 hızlı katlama adımı ("origamiyi") → 5 turna sağa doğru havalanır ("dilin")
        pk = clamp((t - 1.20) / 0.75)
        if 0 < pk < 1:
            # kare kâğıt → üçgen → elmas katlama
            pts = [(-90, -90), (90, -90), (90, 90), (-90, 90)] if pk < 0.33 else ([(-95, 70), (0, -95), (95, 70)] if pk < 0.66 else [(-110, 0), (0, -75), (110, 0), (0, 65)])
            path = skia.Path()
            path.moveTo(*pts[0])
            for pt in pts[1:]: path.lineTo(*pt)
            path.close()
            c.drawPath(path, paint("#F5EFE2"))
            c.drawPath(path, paint(INK, 0.9, Style=skia.Paint.kStroke_Style, StrokeWidth=3.5))
        ps = clamp((t - 2.25) / 1.2)
        if ps > 0:
            for i in range(5):
                pi = clamp((ps - i * 0.12) / 0.65)
                if pi <= 0:
                    continue
                tx = -160 + 820 * ease("out", pi) + i * 30
                ty = 40 - 240 * ease("out", pi) - i * 28
                c.save(); c.translate(tx, ty); c.scale(0.65 + 0.12 * i, 0.65 + 0.12 * i); draw_sprite(c, SP_TURNA_UC); c.restore()

    ck.ekle(
        Oge("sinif", ciz_sinif, derinlik=0.5),
        Oge("turna", ciz_turna_in, x=W/2 - 260, y=H/2 + 160, derinlik=0.95),
        Oge("turna_suru", ciz_katlama_ve_suru, x=W/2 + 40, y=H/2 + 120, derinlik=1.05),
    )
    ck.kamera = Kamera(x=Iz([(0, W/2 - 60), (3.6, W/2 + 120, "io")]), z=Iz([(0, 1.0), (3.6, 1.14, "io")]))
    ck.ust.append(_hud("1.06", "Lisede el sanatları dersinde origamiyi öğreniyorsun. Kâğıt senin dilin oluyor.",
                       lambda t: "dilin" if t >= 2.25 else ("origamiyi" if t >= 1.20 else ("lisede" if t >= 0.25 else ""))))
    return ck

# ───────── 1.07 · 18 yaş, Lincoln + $90.000 çek + arka camda tefeci gölgeleri
def build_107():
    kw = [("sekizinde", 0.25, 0.9), ("doksan", 1.30, 2.05), ("sigortası", 2.55, 3.45)]
    ck = Cekim("1.07", sure=4.2, kelimeler=kw, duygu=Duygu("umut").gecis("gerilim", t0=2.55, sure=0.8), arka="#10151D")

    def ciz_lokanta(c, t, o):
        c.drawRect(skia.Rect(-W, -H, W, H), paint("#1A222E"))
        c.drawRect(skia.Rect(-560, -340, 560, 60), paint("#0D1522"))
        c.drawRect(skia.Rect(-560, -340, 560, 60), paint("#435568", 0.9, Style=skia.Paint.kStroke_Style, StrokeWidth=8))
        # tefeci siluetleri (gerçekçi palto/omuz konturlu, şematik daire değil!)
        pg = ease("out", clamp((t - 2.55) / 0.55))
        if pg > 0:
            c.drawRect(skia.Rect(130, -330, 460, 52), paint(KIRMIZI, 0.24 * pg))
            for gx, sc in ((220, 1.0), (370, 0.92)):
                c.save(); c.translate(gx, -70); c.scale(sc, sc)
                coat = skia.Path()
                coat.moveTo(-78, 130); coat.quadTo(-74, -20, -32, -45); coat.lineTo(32, -45); coat.quadTo(74, -20, 78, 130); coat.close()
                c.drawPath(coat, paint("#06090F", 0.94 * pg))
                c.drawOval(skia.Rect(-26, -110, 26, -44), paint("#06090F", 0.94 * pg))
                c.drawPath(coat, paint(KIRMIZI, 0.45 * pg, Style=skia.Paint.kStroke_Style, StrokeWidth=2.5))
                c.restore()

    def ciz_lincoln(c, t, o):
        # geniş omuzlu anatomik gövde + yaka (R4 temiz)
        torso = skia.Path()
        torso.moveTo(-215, 380); torso.quadTo(-195, 110, -72, 82); torso.lineTo(72, 82); torso.quadTo(195, 110, 215, 380); torso.close()
        c.drawPath(torso, paint("#2F4258"))
        c.drawPath(torso, paint(INK, 0.9, Style=skia.Paint.kStroke_Style, StrokeWidth=4))
        c.drawPath(skia.Path.Polygon([(-48, 82), (0, 155), (48, 82)], True), paint("#E8E4DA"))
        c.save(); c.scale(1.25, 1.25); draw_sprite(c, SP_LINC_S); c.restore()

    def ciz_cek(c, t, o):
        c.drawRect(skia.Rect(-180, -68, 180, 68), paint("#EDE5D2"))
        c.drawRect(skia.Rect(-180, -68, 180, 68), paint(INK, 0.9, Style=skia.Paint.kStroke_Style, StrokeWidth=3.5))
        _yazi(c, "$90.000", 0, 14, 52, "#1A4D2E", 0.98, bold=True)
        _yazi(c, "MICHAEL SCOFIELD", -150, -36, 16, "#3A3A3A", 0.85, bold=False, align="left")
        # 18 YAŞ damgası sol üst boşlukta (Lincoln'ün kafasından tamamen ayrı!)
        _damga(c, "18 YAŞ", -540, -410, clamp((t - 0.25) / 0.30), ALTIN, boyut=28)

    ck.ekle(
        Oge("tefeci_golge", ciz_lokanta, derinlik=0.5),
        Oge("lincoln", ciz_lincoln, x=W/2 - 220, y=H/2 - 30, derinlik=0.85, ikincil=[("nefes", 1.1)]),
        Oge("cek_kagit", ciz_cek, x=W/2 + 120, y=H/2 + 195, derinlik=1.05, giris=("dus", ck.k("doksan", -0.2), 0.45)),
    )
    ck.kamera = Kamera(x=Iz([(0, W/2 - 40), (4.2, W/2 + 75, "io")]), z=Iz([(0, 1.0), (4.2, 1.20, "io")]))
    ck.ust.append(_hud("1.07", "On sekizinde Lincoln sana doksan bin dolar uzatıyor. Annenin sigortası diyor.",
                       lambda t: "sigortası" if t >= 2.55 else ("doksan" if t >= 1.30 else ("sekizinde" if t >= 0.25 else ""))))
    return ck

def ciz_cek_diploma(c, u):
    # NesneTasi: $90.000 çek dönerken diplomaya dönüşür!
    c.drawRect(skia.Rect(-170, -85, 170, 85), paint("#F0E8D4"))
    c.drawRect(skia.Rect(-170, -85, 170, 85), paint(ALTIN if u > 0.5 else INK, 0.95, Style=skia.Paint.kStroke_Style, StrokeWidth=4))
    _yazi(c, "$90.000" if u < 0.5 else "YAPI MÜHENDİSİ", 0, 12, 36 if u < 0.5 else 28, "#1A4D2E" if u < 0.5 else "#142438", 0.98, bold=True)

# ───────── 1.08 · Chicago yapı mühendisi + gökdelenlerin canlı CAD lazer taraması
def build_108():
    kw = [("mühendisi", 0.30, 1.1), ("okuyorsun", 1.70, 2.7)]
    ck = Cekim("1.08", sure=3.8, kelimeler=kw, duygu=Duygu("zafer"), arka="#0D1926")

    def ciz_chicago(c, t, o):
        sh = skia.GradientShader.MakeLinear([(0, -H/2), (0, H/2)], [hexcol("#102238"), hexcol("#284664")])
        c.drawRect(skia.Rect(-W, -H, W, H), skia.Paint(Shader=sh))
        # Chicago gökdelen siluetleri
        binalar = [(-680, -240, 160), (-490, -340, 180), (-280, -190, 140), (-110, -380, 210), (140, -280, 170), (350, -320, 190), (570, -210, 160)]
        for bx, by, bw in binalar:
            c.drawRect(skia.Rect(bx, by, bx + bw, 460), paint("#13202E"))
        # "okuyorsun"da canlı CAD lazer tarama gökdelenleri camgöbeği çelik iskelete çözer!
        p = ease("out", clamp((t - 1.70) / 1.1))
        if p > 0:
            sx = -740 + 1500 * p
            c.save(); c.clipRect(skia.Rect(-740, -440, sx, 460))
            gp = paint(PLAN_C, 0.88, Style=skia.Paint.kStroke_Style, StrokeWidth=2.4)
            for bx, by, bw in binalar:
                c.drawRect(skia.Rect(bx, by, bx + bw, 460), gp)
                for wy in range(by + 40, 440, 52):
                    c.drawLine(bx, wy, bx + bw, wy, paint(PLAN_C, 0.45, Style=skia.Paint.kStroke_Style, StrokeWidth=1.5))
                c.drawLine(bx, by, bx + bw, 460, paint(PLAN_C, 0.3, Style=skia.Paint.kStroke_Style, StrokeWidth=1.5))
            c.restore()
            if p < 0.99:
                c.drawLine(sx, -440, sx, 460, paint("#FFFFFF", 0.95, Style=skia.Paint.kStroke_Style, StrokeWidth=4))
                c.drawLine(sx, -440, sx, 460, paint(PLAN_C, 0.5, Style=skia.Paint.kStroke_Style, StrokeWidth=14))

    def ciz_diploma(c, t, o):
        # sol üstte diploma damgası (cam ofis üstünde)
        _damga(c, "LOYOLA · YAPI MÜHENDİSİ", -310, -240, clamp((t - 0.30) / 0.35), ALTIN, boyut=30)

    ck.ekle(
        Oge("cad_plan", ciz_chicago, derinlik=0.75),
        Oge("diploma", ciz_diploma, x=W/2, y=H/2, derinlik=1.05),
    )
    ck.kamera = Kamera(y=Iz([(0, H/2 + 40), (3.8, H/2 - 40, "io")]), z=Iz([(0, 1.0), (3.8, 1.20, "in")]))
    ck.ust.append(_hud("1.08", "O parayla Chicago'da yapı mühendisi oluyorsun. Her binayı içeriden okuyorsun.",
                       lambda t: "okuyorsun" if t >= 1.70 else ("mühendisi" if t >= 0.30 else "")))
    return ck

# ───────── 1.09 · Masada açılan mavi plan, kâğıt turna konar, FOX RIVER parlar
def build_109():
    kw = [("yeniliyor", 0.30, 1.0), ("planda", 1.45, 2.2), ("fox", 2.40, 3.3)]
    ck = Cekim("1.09", sure=4.0, kelimeler=kw, duygu=Duygu("merak").gecis("gerilim", t0=2.40, sure=0.8), arka="#121820")

    def ciz_masa_ve_plan(c, t, o):
        c.drawRect(skia.Rect(-W, -H, W, H), paint("#2B211A"))
        # hızla soldan sağa açılan mavi mimari plan rulosu
        p = ease("out", clamp((t - 0.30) / 0.75))
        rw = 1120 * max(0.08, p)
        c.drawRect(skia.Rect(-560, -320, -560 + rw, 300), paint("#0C2C46"))
        c.drawRect(skia.Rect(-560, -320, -560 + rw, 300), paint(PLAN_C, 0.85, Style=skia.Paint.kStroke_Style, StrokeWidth=3))
        gp = paint(PLAN_C, 0.35, Style=skia.Paint.kStroke_Style, StrokeWidth=1.5)
        for x in range(-520, int(-560 + rw), 70): c.drawLine(x, -300, x, 280, gp)
        for y in range(-280, 280, 60): c.drawLine(-540, y, -560 + rw - 20, y, gp)
        # "fox" kelimesinde FOX RIVER başlığı camgöbeği parlar
        pf = clamp((t - 2.40) / 0.35)
        if pf > 0:
            _damga(c, "FOX RIVER · TADİLAT PLANI", 190, -210, pf, PLAN_C, boyut=32)

    def ciz_masa_turna(c, t, o):
        c.save(); c.scale(1.3, 1.3); draw_sprite(c, SP_TURNA); c.restore()

    ck.ekle(
        Oge("mavi_rulo", ciz_masa_ve_plan, derinlik=0.75),
        Oge("masa_turna", ciz_masa_turna, x=W/2 - 60, y=H/2 + 30, derinlik=1.0, giris=("dus", ck.k("planda"), 0.45)),
    )
    ck.kamera = Kamera(z=Iz([(0, 1.0), (4.0, 1.24, "in")]))
    ck.ust.append(_hud("1.09", "Çalıştığın firma bir hapishaneyi yeniliyor. Masandaki mavi planda tek ad var: Fox River.",
                       lambda t: "fox" if t >= 2.40 else ("planda" if t >= 1.45 else ("yeniliyor" if t >= 0.30 else ""))))
    return ck

# ───────── 1.10 · Vurucu açık döngü! Turna gölgesi parmaklığa uzar + İDAM KARARI gazete manşeti
def build_110():
    kw = [("değiştirecek", 0.30, 1.15), ("idamla", 1.75, 2.85)]
    ck = Cekim("1.10", sure=3.8, kelimeler=kw, duygu=Duygu("gerilim").gecis("ofke", t0=1.75, sure=0.6), arka="#0A121C")

    def ciz_plan_ve_golge(c, t, o):
        c.drawRect(skia.Rect(-W, -H, W, H), paint("#0C273D"))
        gp = paint(PLAN_C, 0.3, Style=skia.Paint.kStroke_Style, StrokeWidth=1.5)
        for x in range(-960, 980, 80): c.drawLine(x, -540, x, 540, gp)
        for y in range(-540, 560, 80): c.drawLine(-960, y, 960, y, gp)
        # turna + parmaklığa uzayan gölge
        c.save(); c.translate(-260, 60); c.scale(1.1, 1.1); draw_sprite(c, SP_TURNA); c.restore()
        pg = ease("out", clamp((t - 0.30) / 0.85))
        for bx in range(-720, 760, 110):
            c.drawRect(skia.Rect(bx, -540, bx + 34 * pg, 540), paint("#04060A", 0.55 * pg))

    def ciz_gazete(c, t, o):
        # "idamla"da kırmızı flaşla masaya düşen İDAM KARARI gazete manşeti + Lincoln fotoğrafı
        if 1.75 <= t <= 2.00:
            fl = 1.0 - (t - 1.75) / 0.25
            c.drawRect(skia.Rect(-W, -H, W, H), paint(KIRMIZI, 0.42 * fl))
        c.save(); c.rotate(-3.5)
        c.drawRect(skia.Rect(-360, -250, 360, 260), paint("#E8E1D0"))
        c.drawRect(skia.Rect(-360, -250, 360, 260), paint(INK, 0.95, Style=skia.Paint.kStroke_Style, StrokeWidth=5))
        c.drawRect(skia.Rect(-330, -220, 330, -135), paint("#181512"))
        _yazi(c, "İDAM KARARI", 0, -162, 54, "#FFFFFF", 0.98, bold=True)
        # Lincoln fotoğraf karesi
        c.drawRect(skia.Rect(-290, -110, -30, 170), paint("#252B33"))
        c.save(); c.translate(-160, 35); c.scale(0.75, 0.75); draw_sprite(c, SP_LINC_O); c.restore()
        _yazi(c, "LINCOLN BURROWS", 150, -55, 24, "#1A1512", 0.95, bold=True)
        _yazi(c, "FOX RIVER", 150, -15, 22, "#8C2218", 0.95, bold=True)
        for ly in range(30, 160, 24):
            c.drawLine(15, ly, 295, ly, paint("#4A443C", 0.7, Style=skia.Paint.kStroke_Style, StrokeWidth=6))
        c.restore()

    ck.ekle(
        Oge("parmaklik_golge", ciz_plan_ve_golge, derinlik=0.65),
        Oge("idam_manset", ciz_gazete, x=W/2 + 40, y=H/2 - 10, derinlik=1.05, giris=("dus", ck.k("idamla"), 0.35)),
    )
    ck.kamera = Kamera(z=Iz([(0, 1.0), (1.75, 1.08, "out"), (3.8, 1.24, "in")]), sarsinti=[(1.78, 0.32, 22)])
    ck.ust.append(_hud("1.10", "Henüz bilmiyorsun ama o plan hayatını değiştirecek. Çünkü ağabeyin idamla yargılanıyor.",
                       lambda t: "idamla" if t >= 1.75 else ("değiştirecek" if t >= 0.30 else "")))
    return ck

def build_film():
    c = [build_101(), build_102(), build_103(), build_104(), build_105(),
         build_106(), build_107(), build_108(), build_109(), build_110()]
    return Film([
        c[0], OnPlanSil(ciz_kapi_sil, sure=0.55),
        c[1], Maske("mutfak_pencere", boyut=(420, 320), sure=0.65),
        c[2], ZoomIcinden("kilit_surgu", sure=0.60, renk="#101824"),
        c[3], Eslesme("tahta_catlak", "sabah_isigi", sure=0.65),
        c[4], NesneTasi("turna", "turna", ciz_ucan_turna, sure=0.80, kavis=-200),
        c[5], Savurma(yon=1, sure=0.45),
        c[6], NesneTasi("cek_kagit", "diploma", ciz_cek_diploma, sure=0.75, kavis=-180),
        c[7], ZoomIcinden("cad_plan", sure=0.60, renk=PLAN_C),
        c[8], ZoomIcinden("masa_turna", sure=0.60, renk=PLAN_C),
        c[9],
    ])

def kontakt_olustur(film, kare_klasor, out_png):
    bas = film.bas
    anlar = [
        ("1.01 · BURROWS → SCOFIELD",     bas[0] + 2.85),
        ("1.02 · 11 YAŞ & Camda '?'",     bas[1] + 3.25),
        ("GEÇİŞ · Pencere Maskesi",       bas[2] + 0.32),
        ("1.03 · Islahevi & Kilit",       bas[2] + 2.85),
        ("1.04 · CAD Tarama & 01–06",     bas[3] + 3.30),
        ("GEÇİŞ · Çatlak → Sabah",        bas[4] + 0.32),
        ("1.05 · Turna v4 & BURADAYIM",   bas[4] + 3.10),
        ("GEÇİŞ · Turna Uçuşu",           bas[5] + 0.40),
        ("1.06 · Lise & 5 Turna",         bas[5] + 2.85),
        ("1.07 · $90.000 & Tefeciler",    bas[6] + 3.15),
        ("GEÇİŞ · Çek → Diploma",         bas[7] + 0.38),
        ("1.08 · Chicago CAD Tarama",     bas[7] + 2.65),
        ("1.09 · FOX RIVER & Turna",      bas[8] + 2.95),
        ("GEÇİŞ · Turna Zoom",            bas[9] + 0.30),
        ("1.10 · İDAM KARARI Flaş",       bas[9] + 2.55),
        ("1.10 · Bölüm I Kapanış",        bas[9] + 3.45),
    ]
    pngler = film.onizle([t for _, t in anlar], str(kare_klasor), olcek=0.5)
    cols, rows, tw, th, pad, top = 4, 4, 420, 236, 12, 52
    sheet = Image.new("RGB", (cols*tw+(cols+1)*pad, top+rows*(th+24)+pad), (10, 14, 22))
    draw = ImageDraw.Draw(sheet)
    try:
        ft = ImageFont.truetype(str(REPO / "fonts/AlegreyaSC-Bold.ttf"), 20)
        fl = ImageFont.truetype(str(REPO / "fonts/Alegreya.ttf"), 14)
    except Exception:
        ft = fl = ImageFont.load_default()
    draw.text((pad, 14), f"BÖLÜM I ('TURNA') F4b BLOK ANİMATİK KONTAKT (960 px) · {film.sure:.1f} sn · 9/9 Anlamsal Geçiş", fill=(127, 230, 255), font=ft)
    for i, ((etiket, t), p) in enumerate(zip(anlar, pngler)):
        r, c = divmod(i, cols)
        x, y = pad + c*(tw+pad), top + r*(th+24)
        im = Image.open(p).convert("RGB").resize((tw, th), Image.Resampling.LANCZOS)
        sheet.paste(im, (x, y))
        draw.rectangle([x, y, x+tw, y+th], outline=(55, 85, 110), width=2)
        draw.text((x+4, y+th+3), f"{etiket} ({t:.1f}s)", fill=(220, 230, 240), font=fl)
    sheet.save(out_png)
    return out_png

def render_taslak_960(film, yol, fps=16, crf=24):
    import shutil, subprocess
    rw, rh = 960, 540
    ff = shutil.which("ffmpeg")
    if not ff:
        import imageio_ffmpeg
        ff = imageio_ffmpeg.get_ffmpeg_exe()
    tmp = str(yol)[:-4] + "_tmp.mp4"
    proc = subprocess.Popen(
        [ff, "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{rw}x{rh}", "-r", str(fps), "-i", "-",
         "-c:v", "libx264", "-preset", "ultrafast", "-crf", str(crf), "-pix_fmt", "yuv420p", tmp],
        stdin=subprocess.PIPE
    )
    surf = skia.Surface(rw, rh)
    sa, sb = skia.Surface(W, H), skia.Surface(W, H)
    info = skia.ImageInfo.Make(rw, rh, skia.kRGBA_8888_ColorType, skia.kPremul_AlphaType)
    buf = bytearray(rw * rh * 4)
    n = int(round(film.sure * fps))
    c = surf.getCanvas()
    for f in range(n):
        c.save(); c.scale(0.5, 0.5)
        film.kare(c, f / fps, sa, sb)
        c.restore()
        surf.readPixels(info, buf, rw * 4)
        proc.stdin.write(buf)
        if f % 100 == 0:
            print(f"  kare {f}/{n}...", flush=True)
    proc.stdin.close()
    if proc.wait() != 0:
        raise RuntimeError("ffmpeg hata verdi")
    os.replace(tmp, yol)
    return yol

if __name__ == "__main__":
    film = build_film()
    print(f"Bölüm I kuruldu: {len(film.cekimler)} çekim, toplam {film.sure:.2f} sn", flush=True)
    kareler = P / "kareler_b1"
    kontakt_png = P / "bolum1_kontakt_960.png"
    kontakt_olustur(film, kareler, kontakt_png)
    print("Kontakt Bölüm I tamam:", kontakt_png, flush=True)
    mp4 = P / "bolum1_blok_960.mp4"
    render_taslak_960(film, mp4, fps=16, crf=24)
    print("MP4 Bölüm I tamam:", mp4, flush=True)
