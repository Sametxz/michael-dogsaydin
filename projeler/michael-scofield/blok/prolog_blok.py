"""F4b Prolog Blok Animatiği v3 ("Kapının altındaki ışık") — Yüksek Tempolu, Canlı Kelime-Kelime Akış (960×540).

Kullanıcı yönlendirmesi (26.11.2026 18:28):
- 3. şahıstan ağır bir sinema filmi gibi değil; her cümle ve kelime ekranda anlık/canlı render oluyormuş gibi
  aktif, hızlı tepkili, yüksek tutuculuklu anlatım (lazer tarama çizgileri, seri patlayan 01–04 düğümleri,
  kinetik damgalar, keskin whip/snap kamera hareketleri).
- P.03'te yeni onaylı A-Sırt v1 anatomik sırt + 5 katmanlı özgün gotik/turna/gizli-plan dövmesi kullanılır.

Çıktılar:
  - blok/prolog_blok_960.mp4       (960×540, 20 fps)
  - blok/prolog_kontakt_960.png    (12 karelik kontakt sayfası: 6 çekim + 5 geçiş ortası + vurucu an)
  - blok/kareler/*.png             (alt ajan denetimi için tekil 960 px kareler)
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
from gecis import Film, ZoomIcinden, OnPlanSil, Eslesme, Maske
import karakter as K

PLAN_C = "#7FE6FF"
ALTIN = "#FFD88A"
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

def _yazi(c, metin, x, y, boyut=36, renk="#FFFFFF", a=1.0, bold=True, align="center", glow=None):
    font = skia.Font(TF_BOLD if bold else TF_REG, boyut)
    w = font.measureText(metin)
    tx = x - w / 2 if align == "center" else (x - w if align == "right" else x)
    if glow and not os.environ.get("STUDYO_FAST"):
        gp = skia.Paint(AntiAlias=True, Color4f=hexcol(glow, a * 0.45),
                        ImageFilter=skia.ImageFilters.Blur(6, 6))
        c.drawString(metin, tx, y, font, gp)
    elif glow:
        c.drawString(metin, tx + 2, y + 2, font, paint(glow, a * 0.28))
    c.drawString(metin, tx, y, font, paint(renk, a))

def _damga(c, metin, x, y, p, renk=PLAN_C, boyut=32):
    """Kelime anında ekrana vuran kinetik etiket/damga (Born in Lore tutuculuk)."""
    if p <= 0:
        return
    sc = 1.35 - 0.35 * ease("back", clamp(p))
    c.save()
    c.translate(x, y); c.scale(sc, sc)
    font = skia.Font(TF_BOLD, boyut)
    tw = font.measureText(metin)
    pad_x, pad_y = 18, 12
    rect = skia.Rect(-tw/2 - pad_x, -boyut/2 - pad_y, tw/2 + pad_x, boyut/2 + pad_y * 0.7)
    c.drawRect(rect, paint("#07121E", 0.82 * clamp(p * 2)))
    c.drawRect(rect, paint(renk, 0.95 * clamp(p * 2), Style=skia.Paint.kStroke_Style, StrokeWidth=2.8))
    _yazi(c, metin, 0, boyut * 0.32, boyut, renk, clamp(p * 2), bold=True, align="center")
    c.restore()

def _hud(cekim_id, cumle, aktif_kelime_fn):
    def _ciz(c, t):
        c.drawRect(skia.Rect(0, H - 68, W, H), paint("#070B12", 0.76))
        c.drawLine(0, H - 68, W, H - 68, paint(PLAN_C, 0.4, StrokeWidth=2))
        _yazi(c, cekim_id, 72, H - 25, 22, PLAN_C, 0.95, bold=True, align="left")
        _yazi(c, cumle, W / 2, H - 25, 25, "#EEF3F8", 0.94, bold=False, align="center")
        kw = aktif_kelime_fn(t)
        if kw:
            _yazi(c, f"«{kw}»", W - 64, H - 25, 21, ALTIN, 0.98, bold=True, align="right")
    return _ciz

# ───────── Kilitli F3 Sprite'ları (önbellekli, yan etkisiz)
def _sp_michael_figur():
    body = f'<g transform="translate(260,640) scale(1.0)">{K.michael_figur("odak", plan=False)}</g>'
    return svg_sprite(body, 520, 680, ax=260, ay=640, ss=0.75)

def _sp_cocuk_kafa_korku():
    body = f'<g transform="translate(170,170) scale(1.25)">{K.michael_cocuk_kafa("3q", "korku", lighting="prolog")}</g>'
    return svg_sprite(body, 340, 340, ax=170, ay=170, ss=0.85)

def _sp_depo_arka():
    defs, body = K.mekan_depo(katmanlar=["uzak", "orta", "sahne"], plan_gorusu=False)
    return svg_sprite(body, 960, 540, ax=480, ay=270, ss=1.0, defs=f"<defs>{defs}</defs>")

def _sp_hucre_arka():
    defs, body = K.mekan_hucre(katmanlar=["uzak", "orta", "sahne"], plan_gorusu=False)
    return svg_sprite(body, 960, 540, ax=480, ay=270, ss=1.0, defs=f"<defs>{defs}</defs>")

def _sp_sirt(plan_glow=0.0):
    defs, body = K.michael_sirt_dovme(plan_glow=plan_glow)
    wrapped = f'<g transform="translate(400,400)">{body}</g>'
    return svg_sprite(wrapped, 800, 800, ax=400, ay=400, ss=1.0, defs=f"<defs>{defs}</defs>")

# ───────── P.01 (3.8s) · Anlık projektör + CANLI CAD lazer tarama + seri 01–04 + EZBERE
def build_p01():
    kw = [("michael", 0.15, 0.75), ("hapishaneyi", 1.15, 1.95), ("ezbere", 2.15, 3.05)]
    ck = Cekim("P.01", sure=3.8, kelimeler=kw, duygu=Duygu("merak"), arka="#0B121D")

    def ciz_gok(c, t, o):
        sh = skia.GradientShader.MakeLinear([(0, -H/2), (0, H/2)], [hexcol("#08101C"), hexcol("#192B40")])
        c.drawRect(skia.Rect(-W, -H, W, H), skia.Paint(Shader=sh))
        for i, (bx, by, rw, rh) in enumerate([(-580, -320, 400, 65), (200, -360, 480, 75)]):
            dx = (t * (28 + i * 10)) % 420 - 210
            c.drawOval(skia.Rect(bx + dx - rw, by - rh, bx + dx + rw, by + rh), paint("#2B415C", 0.24))

    def ciz_kule_duvar(c, t, o):
        c.drawRect(skia.Rect(-760, -290, -640, 420), paint("#151F2B"))
        c.drawRect(skia.Rect(-790, -360, -610, -280), paint("#1E2C3B"))
        c.drawRect(skia.Rect(-775, -345, -625, -305), paint("#FFE2A0", 0.72))
        c.drawRect(skia.Rect(-900, -140, 960, 520), paint("#1C2735"))
        lp = paint("#0F1620", 0.72, Style=skia.Paint.kStroke_Style, StrokeWidth=3)
        for row in range(-120, 480, 48):
            c.drawLine(-900, row, 960, row, lp)
            off = 45 if (row // 48) % 2 else 0
            for col in range(-860 + off, 940, 96):
                c.drawLine(col, row, col, row + 48, lp)
        for wx, wy in [(-320, -40), (-40, -40), (240, -40), (520, -40), (-180, 120), (100, 120), (380, 120)]:
            c.drawRect(skia.Rect(wx - 28, wy - 20, wx + 28, wy + 20), paint("#0A1018"))
            c.drawRect(skia.Rect(wx - 28, wy - 20, wx + 28, wy + 20), paint("#304358", 0.85, Style=skia.Paint.kStroke_Style, StrokeWidth=2.5))

    def ciz_projektor(c, t, o):
        # hızlı projektör taraması + FOX RIVER kinetik damgası
        p = clamp((t - 0.15) / 1.4)
        target_x = -480 + 1180 * ease("out", p)
        path = skia.Path()
        path.moveTo(-700, -325); path.lineTo(target_x - 150, 320); path.lineTo(target_x + 170, 320); path.close()
        sh = skia.GradientShader.MakeLinear([(-700, -325), (target_x, 260)], [hexcol("#FFF3C8", 0.62), hexcol("#B8DCFF", 0.05)])
        c.drawPath(path, skia.Paint(AntiAlias=True, Shader=sh, BlendMode=skia.BlendMode.kScreen))
        c.drawCircle(-700, -325, 24, paint("#FFF5D6", 0.95))
        _damga(c, "FOX RIVER", -470, -235, clamp((t - 0.30) / 0.35), ALTIN, boyut=28)

    def ciz_canli_tarama(c, t, o):
        # CANLI CAD LAZER TARAMA: "hapishaneyi" kelimesinde soldan sağa tarayıp planı anlık çizer
        p = ease("out", clamp((t - 1.15) / 0.85))
        if p <= 0:
            return
        scan_x = -580 + 1280 * p
        c.save()
        c.clipRect(skia.Rect(-580, -140, scan_x, 370))
        c.drawRect(skia.Rect(-580, -135, 700, 365), paint("#0A2A3E", 0.52))
        gp = paint(PLAN_C, 0.82, Style=skia.Paint.kStroke_Style, StrokeWidth=2.5)
        gp_thin = paint(PLAN_C, 0.32, Style=skia.Paint.kStroke_Style, StrokeWidth=1.2)
        for x in range(-560, 700, 80): c.drawLine(x, -135, x, 365, gp_thin)
        for y in range(-135, 370, 65): c.drawLine(-580, y, 700, y, gp_thin)
        c.drawRect(skia.Rect(-480, -80, 600, 280), gp)
        c.drawLine(-480, 70, 600, 70, gp)
        c.drawLine(-100, -80, -100, 280, gp)
        c.drawLine(240, -80, 240, 280, gp)
        c.restore()
        # aktif dikey lazer tarama çizgisi
        if p < 0.99:
            c.drawLine(scan_x, -145, scan_x, 375, paint("#FFFFFF", 0.95, Style=skia.Paint.kStroke_Style, StrokeWidth=4))
            c.drawLine(scan_x, -145, scan_x, 375, paint(PLAN_C, 0.55, Style=skia.Paint.kStroke_Style, StrokeWidth=14))

    def ciz_noktalar_ve_ezbere(c, t, o):
        # seri patlayan 01 → 02 → 03 → 04 (0.14s arayla!) + canlı koşan rota + EZBERE damgası
        pts = [(240, -40, "01 · HÜCRE"), (240, 70, "02 · BORU"), (-100, 70, "03 · TÜNEL"), (-100, 210, "04 · DUVAR")]
        p_all = clamp((t - 2.15) / 0.85)
        if p_all <= 0:
            return
        dash = paint(PLAN_C, 0.95, Style=skia.Paint.kStroke_Style, StrokeWidth=4.5,
                     PathEffect=skia.DashPathEffect.Make([16, 10], -t * 110))
        for i, (a, b) in enumerate(zip(pts, pts[1:])):
            seg_p = ease("out", clamp((t - (2.22 + i * 0.14)) / 0.18))
            if seg_p > 0:
                c.drawLine(a[0], a[1], a[0] + (b[0] - a[0]) * seg_p, a[1] + (b[1] - a[1]) * seg_p, dash)
        for i, (px, py, lbl) in enumerate(pts):
            pi = ease("back", clamp((t - (2.15 + i * 0.14)) / 0.20))
            if pi <= 0:
                continue
            r = (14 + 4 * math.sin(t * 10 + i)) * pi
            c.drawCircle(px, py, r * 1.85, paint(PLAN_C, 0.28 * pi))
            c.drawCircle(px, py, r, paint(PLAN_C, 0.98, Style=skia.Paint.kStroke_Style, StrokeWidth=3))
            c.drawCircle(px, py, 5 * pi, paint("#FFFFFF", 1.0))
            _yazi(c, lbl, px + 26, py - 12, 21, PLAN_C, clamp(pi), bold=True, align="left")
        _damga(c, "EZBERE", 40, -210, clamp((t - 2.35) / 0.30), PLAN_C, boyut=46)

    ck.ekle(
        Oge("gok", ciz_gok, derinlik=0.05),
        Oge("duvar", ciz_kule_duvar, derinlik=0.65),
        Oge("projektor", ciz_projektor, derinlik=0.80),
        Oge("plan_duvar", ciz_canli_tarama, derinlik=0.95),
        Oge("nokta_01", ciz_noktalar_ve_ezbere, x=W/2, y=H/2, derinlik=1.0),
        Oge("hedef_01", lambda c, t, o: None, x=W/2 + 240, y=H/2 - 40, derinlik=1.0),
    )
    ck.kamera = Kamera(
        x=Iz([(0, W/2 - 90), (1.4, W/2 + 10, "out"), (3.8, W/2 + 125, "io")]),
        y=Iz([(0, H/2 + 70), (2.2, H/2 - 20, "out"), (3.8, H/2 - 45, "io")]),
        z=Iz([(0, 1.0), (1.2, 1.08, "out"), (2.3, 1.15, "out"), (3.8, 1.24, "in")]),
    )
    ck.ust.append(_hud("P.01", "Michael Scofield olarak doğsaydın, bir hapishaneyi ezbere bilirdin.",
                       lambda t: "ezbere" if t >= 2.15 else ("hapishaneyi" if t >= 1.15 else ("michael" if t >= 0.15 else ""))))
    return ck

# ───────── P.02 (2.6s) · Keskin adım + ağır demir kapı çarpması + KİLİT 94941 damgası
def build_p02():
    kw = [("kendini", 0.30, 0.90), ("kilitlerdin", 1.10, 1.95)]
    ck = Cekim("P.02", sure=2.6, kelimeler=kw, duygu=Duygu("gerilim"), arka="#0D1419")
    sp_hucre = _sp_hucre_arka()
    sp_mic = _sp_michael_figur()

    def ciz_hucre(c, t, o):
        c.save(); c.scale(2.0, 2.0); draw_sprite(c, sp_hucre); c.restore()
        fl = 0.08 + 0.06 * math.sin(33 * t) * math.sin(13 * t)
        c.drawRect(skia.Rect(-W/2, -H/2, W/2, H/2), paint("#AEE0E8", fl, BlendMode=skia.BlendMode.kScreen))

    def ciz_michael(c, t, o):
        c.save(); c.scale(1.52, 1.52); draw_sprite(c, sp_mic); c.restore()
        p = clamp((t - 1.10) / 0.22)
        if p > 0:
            for bx in range(-220, 260, 68):
                c.drawRect(skia.Rect(bx, -680, bx + 20, 40), paint("#05080D", 0.56 * p))

    def ciz_kapi(c, t, o):
        p = ease("expo", clamp((t - 1.10) / 0.25))
        kx = 820 * (1 - p)
        c.save(); c.translate(kx, 0)
        c.drawRect(skia.Rect(-560, -560, 560, -510), paint("#1A232B"))
        c.drawRect(skia.Rect(-560, 460, 560, 510), paint("#1A232B"))
        for bx in range(-500, 540, 92):
            c.drawRect(skia.Rect(bx - 12, -560, bx + 12, 560), paint("#1E2832"))
            c.drawRect(skia.Rect(bx - 12, -560, bx - 7, 560), paint("#4A6072", 0.55))
        c.drawRect(skia.Rect(-560, -40, -460, 70), paint("#2B3945"))
        # çarpma anı kıvılcım + KİLİT 94941 damgası
        if 0.70 < p < 1.0:
            sp = 1.0 - (p - 0.70) / 0.30
            c.drawCircle(-510, 15, 55 * sp, paint("#FFF5D0", 0.85 * sp))
        c.restore()
        _damga(c, "KİLİT · 94941", 340, -250, clamp((t - 1.22) / 0.25), PLAN_C, boyut=32)

    ck.ekle(
        Oge("hucre", ciz_hucre, derinlik=0.55),
        Oge("michael_el", ciz_michael, x=W/2 - 55, y=H + 220, derinlik=0.88,
            ikincil=[("nefes", 1.2)],
            eylemler=[(ck.k("kendini"), 0.50, lambda p: dict(dx=62 * ease("out", p), s=1.0 + 0.05 * ease("out", p)))]),
        Oge("hucre_kapisi", ciz_kapi, x=W/2, y=H/2, derinlik=1.18),
    )
    ck.kamera = Kamera(
        x=Iz([(0, W/2 - 35), (1.05, W/2 + 20, "out"), (2.6, W/2, "io")]),
        y=Iz([(0, H/2), (2.6, H/2 - 30, "out")]),
        z=Iz([(0, 1.04), (1.08, 1.18, "out"), (1.35, 1.06, "out"), (2.6, 1.14, "io")]),
        sarsinti=[(1.15, 0.32, 22)],
    )
    ck.ust.append(_hud("P.02", "Sonra kendini içine kilitlerdin.",
                       lambda t: "kilitlerdin" if t >= 1.10 else ("kendini" if t >= 0.30 else "")))
    return ck

def ciz_parmaklik_perde(c, u):
    c.drawRect(skia.Rect(-95, 0, 95, H), paint("#0C1218"))
    c.drawRect(skia.Rect(-88, 0, -70, H), paint("#435A6E", 0.6))
    c.drawRect(skia.Rect(70, 0, 92, H), paint("#040608", 0.85))

# ───────── P.03 (3.8s) · YENİ A-SIRT v1 ANATOMİK SIRT & 5 KATMANLI DÖVME + CANLI PLAN TARAMA
def build_p03():
    kw = [("haritası", 0.75, 1.50), ("teninde", 1.60, 2.40), ("adam", 2.50, 3.35)]
    ck = Cekim("P.03", sure=3.8, kelimeler=kw, duygu=Duygu("merak"), arka="#0A111A")
    sp_sirt_norm = _sp_sirt(0.0)
    sp_sirt_plan = _sp_sirt(1.0)

    def ciz_arka(c, t, o):
        sh = skia.GradientShader.MakeRadial((0, -60), 920, [hexcol("#1B2D40"), hexcol("#070C12")])
        c.drawRect(skia.Rect(-W, -H, W, H), skia.Paint(Shader=sh))
        # ince arka plan CAD ızgarası
        gp = paint(PLAN_C, 0.10, Style=skia.Paint.kStroke_Style, StrokeWidth=1.2)
        for x in range(-960, 980, 90): c.drawLine(x, -540, x, 540, gp)
        for y in range(-540, 560, 90): c.drawLine(-960, y, 960, y, gp)

    def ciz_sirt_ve_tarama(c, t, o):
        # 1) Normal yüksek detaylı anatomik sırt + 5 katmanlı dövme
        c.save(); c.scale(1.38, 1.38); draw_sprite(c, sp_sirt_norm); c.restore()
        # 2) "haritası" kelimesinde yukarıdan aşağı canlı lazer tarama ile camgöbeği kat planı yanar!
        scan_p = ease("out", clamp((t - 0.75) / 0.85))
        if scan_p > 0:
            scan_y = -480 + 960 * scan_p
            c.save()
            c.clipRect(skia.Rect(-560, -560, 560, scan_y))
            c.scale(1.38, 1.38); draw_sprite(c, sp_sirt_plan)
            c.restore()
            if scan_p < 0.99:
                c.drawLine(-420, scan_y, 420, scan_y, paint("#FFFFFF", 0.95, Style=skia.Paint.kStroke_Style, StrokeWidth=4))
                c.drawLine(-420, scan_y, 420, scan_y, paint(PLAN_C, 0.55, Style=skia.Paint.kStroke_Style, StrokeWidth=14))

    def ciz_kalkan_plan(c, t, o):
        # "teninde" kelimesinde sırtın üstünden havaya kalkan şematik plan + yatay eşleşme çizgisi
        p = ease("out", clamp((t - 1.60) / 0.70))
        if p <= 0:
            return
        c.save()
        c.translate(0, -32 * p)
        c.rotate(math.sin(t * 2.2) * 2.2 * p)
        # sağ üstte yükselen sektör şeması + sol üstte nişangâh
        c.drawRect(skia.Rect(210, -290, 540, -70), paint("#071624", 0.65 * p))
        c.drawRect(skia.Rect(210, -290, 540, -70), paint(PLAN_C, 0.85 * p, Style=skia.Paint.kStroke_Style, StrokeWidth=2.5))
        dash = paint(PLAN_C, 0.95 * p, Style=skia.Paint.kStroke_Style, StrokeWidth=3,
                     PathEffect=skia.DashPathEffect.Make([10, 7], -t * 75))
        c.drawLine(250, -245, 360, -245, dash); c.drawLine(360, -245, 360, -135, dash); c.drawLine(360, -135, 500, -135, dash)
        _yazi(c, "SEKTÖR A-B", 375, -305, 22, PLAN_C, p, bold=True, align="center")
        # geçişte kapı ışığına eşleşecek parlak yatay çizgi
        c.drawLine(-380 * p, 125, 380 * p, 125, paint(PLAN_C, 0.98, Style=skia.Paint.kStroke_Style, StrokeWidth=6))
        c.drawLine(-380 * p, 125, 380 * p, 125, paint("#FFFFFF", 0.75, Style=skia.Paint.kStroke_Style, StrokeWidth=2.5))
        c.restore()

    def ciz_harita_damga(c, t, o):
        # sol üst boşlukta (başla SIFIR çakışma!) kinetik HARİTA damgası
        _damga(c, "HARİTA", -430, -230, clamp((t - 2.50) / 0.28), PLAN_C, boyut=46)

    ck.ekle(
        Oge("arka", ciz_arka, derinlik=0.2),
        Oge("dovme_plan", ciz_sirt_ve_tarama, x=W/2, y=H/2 + 45, derinlik=0.95, ikincil=[("nefes", 1.1)]),
        Oge("yatay_cizgi", ciz_kalkan_plan, x=W/2, y=H/2 + 95, derinlik=1.1, ikincil=[("suz", 0.7)]),
        Oge("kinetik_harita", ciz_harita_damga, x=W/2, y=H/2, derinlik=1.2),
    )
    ck.kamera = Kamera(
        x=Iz([(0, W/2 - 30), (1.6, W/2 + 25, "out"), (3.8, W/2, "io")]),
        y=Iz([(0, H/2 - 20), (1.8, H/2 + 15, "out"), (3.8, H/2 + 45, "io")]),
        z=Iz([(0, 1.02), (1.6, 1.14, "out"), (3.8, 1.24, "io")]),
    )
    ck.ust.append(_hud("P.03", "Ve tarihe, haritası teninde yazılı adam olarak geçerdin.",
                       lambda t: "adam" if t >= 2.50 else ("teninde" if t >= 1.60 else ("haritası" if t >= 0.75 else ""))))
    return ck

# ───────── P.04 (4.1s) · Vurucu an! Ani kararma + ayakkabılar + hızlı whip-tilt 11 yaş Michael
def build_p04():
    kw = [("ama", 0.15, 0.70), ("yaşındasın", 1.15, 2.00), ("karanlıktasın", 2.25, 3.25)]
    ck = Cekim("P.04", sure=4.1, kelimeler=kw,
               duygu=Duygu("gerilim").gecis("korku", t0=2.25, sure=0.8), arka="#05080E")
    sp_cocuk = _sp_cocuk_kafa_korku()

    def ciz_karanlik_oda(c, t, o):
        c.drawRect(skia.Rect(-W, -H, W, H), paint("#060A12"))
        for x in range(-900, 960, 115):
            c.drawLine(x, -600, x, 600, paint("#0E1726", 0.75, Style=skia.Paint.kStroke_Style, StrokeWidth=3))
        if 0.12 <= t <= 0.34:
            fl = 1.0 - abs(t - 0.20) / 0.14
            c.drawRect(skia.Rect(-W, -H, W, H), paint("#FFFFFF", clamp(fl) * 0.55))

    def ciz_isik_cizgisi(c, t, o):
        sh = skia.GradientShader.MakeLinear([(0, 0), (0, 230)], [hexcol(ALTIN, 0.62), hexcol(ALTIN, 0.0)])
        beam = skia.Path()
        beam.moveTo(-295, 0); beam.lineTo(295, 0); beam.lineTo(510, 250); beam.lineTo(-510, 250); beam.close()
        c.drawPath(beam, skia.Paint(AntiAlias=True, Shader=sh, BlendMode=skia.BlendMode.kScreen))
        c.drawRect(skia.Rect(-300, -6, 300, 6), paint("#FFF7DE", 0.98))
        for i in range(16):
            dx = math.sin(t * 1.3 + i * 1.9) * 250
            dy = 22 + ((i * 37 + t * 28) % 165)
            c.drawCircle(dx, dy, 2.6, paint(ALTIN, 0.62))

    def ciz_ayakkabi(c, t, o):
        # gerçekçi çocuk spor ayakkabı uçları + üstten inen koyu kot paçaları + temas gölgesi
        fade_out = 1.0 - clamp((t - 2.00) / 0.30)
        if fade_out <= 0.01:
            return
        for sx in (-74, 74):
            # temas gölgesi
            c.drawOval(skia.Rect(sx - 56, 12, sx + 56, 36), paint("#030508", 0.72 * fade_out))
            # üstten inen koyu pantolon paçası + bilek
            c.drawRect(skia.Rect(sx - 30, -145, sx + 30, -14), paint("#1B2434", 0.96 * fade_out))
            c.drawRect(skia.Rect(sx - 30, -145, sx + 30, -14), paint(ALTIN, 0.32 * fade_out, Style=skia.Paint.kStroke_Style, StrokeWidth=2.5))
            # ayakkabı gövdesi (koyu lacivert/füme)
            shoe = skia.Path()
            shoe.moveTo(sx - 36, -20); shoe.quadTo(sx - 48, 8, sx - 44, 22)
            shoe.lineTo(sx + 44, 22); shoe.quadTo(sx + 48, 8, sx + 36, -20); shoe.close()
            c.drawPath(shoe, paint("#242C38", fade_out))
            c.drawPath(shoe, paint(INK, 0.9 * fade_out, Style=skia.Paint.kStroke_Style, StrokeWidth=3))
            # krem kauçuk taban + ön burun şeridi
            c.drawRect(skia.Rect(sx - 44, 14, sx + 44, 24), paint("#E5DFCE", 0.95 * fade_out))
            c.drawArc(skia.Rect(sx - 34, -4, sx + 34, 20), 180, 180, True, paint("#DDD6C4", 0.9 * fade_out))
            # bağcık çizgileri
            for ly in (-14, -8, -2):
                c.drawLine(sx - 12, ly, sx + 12, ly, paint("#EDE7D8", 0.85 * fade_out, Style=skia.Paint.kStroke_Style, StrokeWidth=2.5))
        _damga(c, "11 YAŞ", 295, -55, clamp((t - 1.22) / 0.25) * fade_out, ALTIN, boyut=30)

    def ciz_cocuk_yuz(c, t, o):
        # 11 yaş Michael v3 + boyun, çizgili kazak, sıcak alt rim ışığı (alt kenara tam oturur, R4 temiz)
        sh_path = skia.Path()
        sh_path.moveTo(-240, 420); sh_path.quadTo(-205, 175, -68, 150)
        sh_path.lineTo(68, 150); sh_path.quadTo(205, 175, 240, 420); sh_path.close()
        c.drawPath(sh_path, paint("#2B1917"))
        c.save(); c.clipPath(sh_path)
        for ry in range(180, 400, 34):
            c.drawRect(skia.Rect(-250, ry, 250, ry + 12), paint("#7A5944", 0.38))
        c.drawRect(skia.Rect(-250, 145, -10, 420), paint("#05080E", 0.72))
        c.restore()
        c.drawRect(skia.Rect(-36, 92, 36, 175), paint("#7A5945"))
        c.drawRect(skia.Rect(-36, 92, -4, 175), paint("#1E1820", 0.7))
        c.drawArc(skia.Rect(-68, 128, 68, 192), 0, 180, False, paint("#5A2922", 0.92, Style=skia.Paint.kStroke_Style, StrokeWidth=10))
        c.drawPath(sh_path, paint(ALTIN, 0.5, Style=skia.Paint.kStroke_Style, StrokeWidth=4))
        c.save(); c.scale(1.68, 1.68); draw_sprite(c, sp_cocuk); c.restore()
        c.drawCircle(24, -18, 4.8, paint(ALTIN, 0.9))
        c.drawCircle(-36, -18, 4.2, paint(ALTIN, 0.9))

    ck.ekle(
        Oge("oda", ciz_karanlik_oda, derinlik=0.35),
        Oge("isik_cizgisi", ciz_isik_cizgisi, x=W/2, y=H/2 + 230, derinlik=0.75,
            giris=("parla", ck.k("ama"), 0.25), cikis=("belir", 2.15, 0.35)),
        Oge("cocuk_ayakkabi", ciz_ayakkabi, x=W/2, y=H/2 + 315, derinlik=0.92,
            giris=("kay_sol", ck.k("yaşındasın"), 0.40)),
        Oge("cocuk_goz", ciz_cocuk_yuz, x=W/2, y=H/2 - 115, derinlik=1.0,
            giris=("belir", ck.k("karanlıktasın", -0.20), 0.40), ikincil=[("nefes", 1.6), ("titre", 0.4)]),
    )
    ck.kamera = Kamera(
        x=Iz([(0, W/2), (4.1, W/2 + 16, "io")]),
        y=Iz([(0, H/2 + 185), (1.95, H/2 + 170, "out"), (3.1, H/2 - 125, "out"), (4.1, H/2 - 135, "io")]),
        z=Iz([(0, 1.05), (2.0, 1.12, "out"), (4.1, 1.28, "in")]),
        sarsinti=[(0.16, 0.22, 16)],
    )
    ck.ust.append(_hud("P.04", "Ama şu an? On bir yaşındasın. Karanlıktasın.",
                       lambda t: "karanlıktasın" if t >= 2.25 else ("yaşındasın" if t >= 1.15 else ("ama" if t >= 0.15 else ""))))
    return ck

# ───────── P.05 (3.4s) · Kapı ötesi gölge + hızlı CAD çizimi + seri 01–04 sayma
def build_p05():
    kw = [("kapının", 0.20, 0.85), ("sızan", 1.00, 1.70), ("sayıyorsun", 1.75, 2.75)]
    ck = Cekim("P.05", sure=3.4, kelimeler=kw,
               duygu=Duygu("korku").gecis("merak", t0=1.75, sure=0.75), arka="#070C14")
    sp_depo = _sp_depo_arka()

    def ciz_depo(c, t, o):
        c.save(); c.scale(2.05, 2.05); draw_sprite(c, sp_depo); c.restore()

    def ciz_kapi_araligi(c, t, o):
        # am_mekanlar_v1'in yumuşak altın ışık huzmesi üzerine organik, yumuşak kenarlı yürüyen gölge (açık döngü!)
        p = clamp((t - 0.20) / 0.8)
        # hafif genişleyen sıcak altın eşik parıltısı (sert beyaz kutu YOK!)
        sh_g = skia.GradientShader.MakeLinear([(0, -10), (0, 140)], [hexcol(ALTIN, 0.45 + 0.2 * p), hexcol(ALTIN, 0.0)])
        beam = skia.Path()
        beam.moveTo(-215, 0); beam.lineTo(215, 0); beam.lineTo(390, 145); beam.lineTo(-390, 145); beam.close()
        c.drawPath(beam, skia.Paint(AntiAlias=True, Shader=sh_g, BlendMode=skia.BlendMode.kScreen))
        # kapı ötesinden geçen yumuşak kenarlı yürüyen ayak/figür gölgesi
        sp = clamp((t - 0.25) / 1.15)
        if 0 < sp < 1:
            sx = -260 + 520 * ease("io", sp)
            sh_shad = skia.GradientShader.MakeRadial((sx, 25), 95, [hexcol("#05080E", 0.78), hexcol("#05080E", 0.0)])
            c.drawOval(skia.Rect(sx - 100, -18, sx + 100, 95), skia.Paint(AntiAlias=True, Shader=sh_shad))

    def ciz_tahta_plan(c, t, o):
        p = ease("out", clamp((t - 1.00) / 0.65))
        if p <= 0:
            return
        gp = paint(PLAN_C, 0.92, Style=skia.Paint.kStroke_Style, StrokeWidth=3)
        c.drawLine(-280, -240, -280 + 25 * p, -240 + 280 * p, gp)
        c.drawLine(240, -180, 240 + 30 * p, -180 + 270 * p, gp)
        c.drawLine(-195 * p, 95, 195 * p, 95, paint(PLAN_C, 0.85, Style=skia.Paint.kStroke_Style, StrokeWidth=2.5,
                   PathEffect=skia.DashPathEffect.Make([12, 8], -t * 85)))

    def ciz_sayac(c, t, o):
        # ışık şeridiyle çakışmayan temiz konumlar
        tags = [(-268, -125, "01 · ÇATLAK"), (255, -75, "02 · ÇİVİ"), (-295, 155, "03 · TOZ"), (215, 155, "04 · IŞIK")]
        for i, (tx, ty, lbl) in enumerate(tags):
            pi = ease("back", clamp((t - (1.75 + i * 0.18)) / 0.22))
            if pi <= 0:
                continue
            c.drawCircle(tx, ty, (16 + 3.5 * math.sin(t * 10 + i)) * pi, paint(PLAN_C, 0.95, Style=skia.Paint.kStroke_Style, StrokeWidth=3))
            c.drawCircle(tx, ty, 5 * pi, paint("#FFFFFF", 1.0))
            _yazi(c, lbl, tx + 24, ty - 10, 22, PLAN_C, clamp(pi), bold=True, align="left")

    ck.ekle(
        Oge("depo", ciz_depo, derinlik=0.55),
        Oge("kapi_araligi", ciz_kapi_araligi, x=W/2, y=H/2 + 95, derinlik=0.85),
        Oge("tahta_ayrinti", ciz_tahta_plan, x=W/2, y=H/2, derinlik=1.0),
        Oge("sayac_noktalar", ciz_sayac, x=W/2, y=H/2, derinlik=1.1),
    )
    ck.kamera = Kamera(
        x=Iz([(0, W/2 - 20), (1.7, W/2 + 12, "out"), (3.4, W/2, "io")]),
        y=Iz([(0, H/2 - 15), (3.4, H/2 + 70, "io")]),
        z=Iz([(0, 1.04), (1.7, 1.16, "out"), (3.4, 1.30, "in")]),
    )
    ck.ust.append(_hud("P.05", "Ve kapının altından sızan ışığı sayıyorsun.",
                       lambda t: "sayıyorsun" if t >= 1.75 else ("sızan" if t >= 1.00 else ("kapının" if t >= 0.20 else ""))))
    return ck

# ───────── P.06 (2.2s) · Keskin Başlık Kartı
def build_p06():
    ck = Cekim("P.06", sure=2.2, kelimeler=[], duygu=Duygu("merak"), arka="#0B131E")

    def ciz_zemin(c, t, o):
        sh = skia.GradientShader.MakeRadial((0, 0), 960, [hexcol("#16293D"), hexcol("#070B12")])
        c.drawRect(skia.Rect(-W, -H, W, H), skia.Paint(Shader=sh))
        gp = paint(PLAN_C, 0.14, Style=skia.Paint.kStroke_Style, StrokeWidth=1.5)
        for x in range(-960, 980, 80): c.drawLine(x, -540, x, 540, gp)
        for y in range(-540, 560, 80): c.drawLine(-960, y, 960, y, gp)

    def ciz_kapi_cerceve(c, t, o):
        p = ease("out", clamp(t / 0.55))
        w, h = 280 + 380 * p, 440 + 80 * p
        c.drawRect(skia.Rect(-w/2, -h/2, w/2, h/2), paint("#FFFFFF", 0.06))
        c.drawRect(skia.Rect(-w/2, -h/2, w/2, h/2), paint(PLAN_C, 0.85, Style=skia.Paint.kStroke_Style, StrokeWidth=3))
        c.drawLine(-w/2, h/2, w/2, h/2, paint(ALTIN, 0.95, Style=skia.Paint.kStroke_Style, StrokeWidth=6))

    def ciz_baslik(c, t, o):
        p = ease("out", clamp((t - 0.25) / 0.65))
        if p <= 0:
            return
        c.save()
        c.clipRect(skia.Rect(-820, -180, -820 + 1640 * p, 180))
        _yazi(c, "MICHAEL SCOFIELD", 0, -28, 78, "#FFFFFF", 0.98, bold=True, align="center", glow=PLAN_C)
        _yazi(c, "OLARAK DOĞSAYDIN?", 0, 56, 56, PLAN_C, 0.96, bold=True, align="center", glow=PLAN_C)
        c.restore()

    ck.ekle(
        Oge("zemin", ciz_zemin, derinlik=0.2),
        Oge("baslik_kapi", ciz_kapi_cerceve, derinlik=0.75, giris=("buyu", 0.0, 0.5)),
        Oge("baslik_yazi", ciz_baslik, derinlik=1.0, giris=("ciz", 0.2, 0.7)),
    )
    ck.kamera = Kamera(z=Iz([(0, 1.0), (2.2, 1.09, "io")]))
    ck.ust.append(_hud("P.06", "BAŞLIK KARTI · Kapı aralığı → Bölüm I ev kapısına bağlanır", lambda t: "BAŞLIK"))
    return ck

def build_film():
    p01, p02, p03, p04, p05, p06 = build_p01(), build_p02(), build_p03(), build_p04(), build_p05(), build_p06()
    return Film([
        p01, ZoomIcinden("hedef_01", sure=0.65, renk=PLAN_C),
        p02, OnPlanSil(ciz_parmaklik_perde, sure=0.55),
        p03, Eslesme("yatay_cizgi", "isik_cizgisi", sure=0.65),
        p04, ZoomIcinden("cocuk_goz", sure=0.65, renk=ALTIN),
        p05, Maske("kapi_araligi", boyut=(380, 90), sure=0.70),
        p06,
    ])

def kontakt_olustur(film, kare_klasor, out_png):
    bas = film.bas
    anlar = [
        ("P.01 · CAD Tarama & EZBERE",   bas[0] + 2.85),
        ("GEÇİŞ 1 · ZoomIcinden (01)",   bas[1] + 0.32),
        ("P.02 · Kapı & KİLİT 94941",    bas[1] + 1.65),
        ("GEÇİŞ 2 · OnPlanSil",          bas[2] + 0.27),
        ("P.03 · Anatomik Sırt & HARİTA",bas[2] + 2.95),
        ("GEÇİŞ 3 · Eslesme (Çizgi)",    bas[3] + 0.32),
        ("P.04 · Vurucu An & 11 YAŞ",    bas[3] + 1.75),
        ("P.04 · 11 Yaş Gözler",         bas[3] + 3.25),
        ("GEÇİŞ 4 · ZoomIcinden (Göz)",  bas[4] + 0.32),
        ("P.05 · 01-04 & Gölge",         bas[4] + 2.55),
        ("GEÇİŞ 5 · Maske (Kapı)",       bas[5] + 0.35),
        ("P.06 · Başlık Kartı",          bas[5] + 1.55),
    ]
    pngler = film.onizle([t for _, t in anlar], str(kare_klasor), olcek=0.5)
    cols, rows = 4, 3
    tw, th = 440, 248
    pad, top = 16, 56
    cw, ch = cols * tw + (cols + 1) * pad, top + rows * (th + 28) + pad
    sheet = Image.new("RGB", (cw, ch), (11, 16, 24))
    draw = ImageDraw.Draw(sheet)
    try:
        f_title = ImageFont.truetype(str(REPO / "fonts" / "AlegreyaSC-Bold.ttf"), 22)
        f_lbl = ImageFont.truetype(str(REPO / "fonts" / "Alegreya.ttf"), 16)
    except Exception:
        f_title = f_lbl = ImageFont.load_default()
    draw.text((pad, 14), f"PROLOG F4b BLOK ANİMATİK KONTAKT v3 (Yüksek Tempo + A-Sırt) · {film.sure:.1f} sn · 5/5 Anlamsal Geçiş", fill=(127, 230, 255), font=f_title)
    for i, ((etiket, t), p) in enumerate(zip(anlar, pngler)):
        r, c = divmod(i, cols)
        x = pad + c * (tw + pad)
        y = top + r * (th + 28)
        im = Image.open(p).convert("RGB").resize((tw, th), Image.Resampling.LANCZOS)
        sheet.paste(im, (x, y))
        draw.rectangle([x, y, x + tw, y + th], outline=(60, 90, 115), width=2)
        draw.text((x + 4, y + th + 4), f"{etiket}  ({t:.2f}s)", fill=(225, 232, 240), font=f_lbl)
    sheet.save(out_png)
    return out_png, pngler

def render_taslak_960(film, yol, fps=20, crf=23):
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
        if f % 80 == 0:
            print(f"  kare {f}/{n}...", flush=True)
    proc.stdin.close()
    if proc.wait() != 0:
        raise RuntimeError("ffmpeg hata verdi")
    os.replace(tmp, yol)
    return yol

if __name__ == "__main__":
    film = build_film()
    print(f"Film v3 kuruldu: {len(film.cekimler)} çekim, toplam {film.sure:.2f} sn", flush=True)
    kareler = P / "kareler"
    kontakt_png = P / "prolog_kontakt_v3_960.png"
    kontakt_olustur(film, kareler, kontakt_png)
    print("Kontakt v3 tamam:", kontakt_png, flush=True)
    mp4 = P / "prolog_blok_v3_960.mp4"
    render_taslak_960(film, mp4, fps=20, crf=23)
    print("MP4 v3 tamam:", mp4, flush=True)
