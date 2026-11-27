"""F4b Prolog Block Animatic — 100% ENGLISH ("The Light Under the Door", 960×540).

- 100% English narration HUD, kinetic stamps (FOX RIVER, BY HEART, LOCKED · 94941, MAP, SECTOR A-B, AGE 11,
  01–04, WHAT IF YOU WERE BORN AS MICHAEL SCOFIELD?).
- Uses locked A-Sırt v1 (anatomical back + 5-layer tattoo), Adult Michael v3, real 11yo Michael v3 full striped
  sweater figure (no dark silhouette!), and Fox River Cell / Dark Closet sets.
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
from kartlar.p_set_prolog import set_p01_fox_river_gece, set_p04_depo_zemin

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

def _yazi(c, metin, x, y, boyut=36, renk="#FFFFFF", a=1.0, bold=True, align="center"):
    font = skia.Font(TF_BOLD if bold else TF_REG, boyut)
    w = font.measureText(metin)
    tx = x - w / 2 if align == "center" else (x - w if align == "right" else x)
    c.drawString(metin, tx, y, font, paint(renk, a))

def _damga(c, metin, x, y, p, renk=PLAN_C, boyut=32):
    if p <= 0.01:
        return
    sc = 1.32 - 0.32 * ease("back", clamp(p))
    al = clamp(p * 2.2)
    c.save()
    c.translate(x, y); c.scale(sc, sc)
    font = skia.Font(TF_BOLD, boyut)
    tw = font.measureText(metin)
    rect = skia.Rect(-tw/2 - 18, -boyut/2 - 10, tw/2 + 18, boyut/2 + 8)
    c.drawRect(rect, paint("#07121E", 0.84 * al))
    c.drawRect(rect, paint(renk, 0.95 * al, Style=skia.Paint.kStroke_Style, StrokeWidth=2.8))
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

SP_MIC = svg_sprite(f'<g transform="translate(260,640) scale(1.0)">{K.michael_figur("odak", plan=False)}</g>', 520, 680, ax=260, ay=640, ss=0.75)
SP_COCUK_FIG = svg_sprite(f'<g transform="translate(260,520) scale(1.0)">{K.michael_cocuk_figur("korku", lighting="prolog")}</g>', 520, 560, ax=260, ay=520, ss=0.85)
def _sp_depo():
    defs, body = K.mekan_depo(katmanlar=["uzak", "orta"], plan_gorusu=False)
    return svg_sprite(body, 960, 540, ax=480, ay=270, ss=1.0, defs=f"<defs>{defs}</defs>")
def _sp_hucre():
    defs, body = K.mekan_hucre(katmanlar=["uzak", "orta", "sahne"], plan_gorusu=False)
    return svg_sprite(body, 960, 540, ax=480, ay=270, ss=1.0, defs=f"<defs>{defs}</defs>")
def _sp_sirt(g=0.0):
    defs, body = K.michael_sirt_dovme(plan_glow=g)
    return svg_sprite(f'<g transform="translate(400,400)">{body}</g>', 800, 800, ax=400, ay=400, ss=1.0, defs=f"<defs>{defs}</defs>")

SP_DEPO = _sp_depo()
SP_HUCRE = _sp_hucre()
SP_SIRT_0 = _sp_sirt(0.0)
SP_SIRT_1 = _sp_sirt(1.0)

def _sp_layer(fn, katmanlar, ss=1.0):
    defs, body = fn(katmanlar=katmanlar)
    return svg_sprite(body, 960, 540, ax=480, ay=270, ss=ss, defs=f"<defs>{defs}</defs>")

def _draw_2x(sp):
    return lambda c, t, o: (c.save(), c.scale(2.02, 2.02), draw_sprite(c, sp), c.restore())

def _draw_scan_2x(sp, t0, sure=0.75):
    def _ciz(c, t, o):
        p = ease("out", clamp((t - t0) / sure))
        if p <= 0.005: return
        sx = -W/2 + W * p
        c.save(); c.clipRect(skia.Rect(-W/2, -H/2, sx, H/2)); c.scale(2.02, 2.02); draw_sprite(c, sp); c.restore()
        if p < 0.98:
            c.drawLine(sx, -H/2, sx, H/2, paint("#FFFFFF", 0.95, Style=skia.Paint.kStroke_Style, StrokeWidth=4))
            c.drawLine(sx, -H/2, sx, H/2, paint(PLAN_C, 0.50, Style=skia.Paint.kStroke_Style, StrokeWidth=14))
    return _ciz

def build_p01():
    kw = [("michael", 0.15, 0.75), ("prison", 1.15, 1.95), ("heart", 2.15, 3.05)]
    ck = Cekim("P.01", sure=3.8, kelimeler=kw, duygu=Duygu("merak"), arka="#08101C")
    sp_u = _sp_layer(set_p01_fox_river_gece, ["uzak"])
    sp_main = _sp_layer(set_p01_fox_river_gece, ["orta", "sahne", "onplan"])
    sp_p = _sp_layer(set_p01_fox_river_gece, ["plan"])

    def ciz_fx(c, t, o):
        # yağmur damlaları + BY HEART damgası
        for i in range(24):
            rx = -880 + (i * 79) % 1760
            ry = -480 + ((i * 67 + t * 560) % 920)
            c.drawLine(rx, ry, rx - 10, ry + 26, paint("#B4D4EE", 0.34, Style=skia.Paint.kStroke_Style, StrokeWidth=2))
        _damga(c, "FOX RIVER", -540, -325, clamp((t - 0.25) / 0.30), ALTIN, boyut=28)
        _damga(c, "BY HEART", 0, -325, clamp((t - 2.15) / 0.28), PLAN_C, boyut=42)

    ck.ekle(
        Oge("gok", _draw_2x(sp_u), derinlik=0.60),
        Oge("duvar", _draw_2x(sp_main), derinlik=1.0),
        Oge("plan_duvar", _draw_scan_2x(sp_p, ck.k("prison"), 0.90), derinlik=1.0),
        Oge("fx_p01", ciz_fx, derinlik=1.0),
        Oge("hedef_01", lambda c, t, o: None, x=W/2 - 420, y=H/2 - 40, derinlik=1.0),
    )
    ck.kamera = Kamera(
        x=Iz([(0, W/2 + 40), (1.8, W/2 - 40, "out"), (3.8, W/2 - 140, "in")]),
        y=Iz([(0, H/2 + 35), (3.8, H/2 - 20, "io")]),
        z=Iz([(0, 1.02), (1.8, 1.10, "out"), (3.8, 1.24, "in")]),
    )
    ck.ust.append(_hud("P.01", "If you were born as Michael Scofield, you'd know a prison by heart.",
                       lambda t: "heart" if t >= 2.15 else ("prison" if t >= 1.15 else ("michael" if t >= 0.15 else ""))))
    return ck

def build_p02():
    kw = [("yourself", 0.30, 0.90), ("locked", 1.10, 1.95)]
    ck = Cekim("P.02", sure=2.6, kelimeler=kw, duygu=Duygu("gerilim"), arka="#0D1419")

    def ciz_hucre(c, t, o):
        c.save(); c.scale(2.0, 2.0); draw_sprite(c, SP_HUCRE); c.restore()
        fl = 0.08 + 0.06 * math.sin(33 * t) * math.sin(13 * t)
        c.drawRect(skia.Rect(-W/2, -H/2, W/2, H/2), paint("#AEE0E8", fl, BlendMode=skia.BlendMode.kScreen))

    def ciz_michael(c, t, o):
        c.save(); c.scale(1.52, 1.52); draw_sprite(c, SP_MIC); c.restore()
        p = clamp((t - 1.10) / 0.22)
        if p > 0:
            for bx in range(-220, 260, 68): c.drawRect(skia.Rect(bx, -680, bx + 20, 40), paint("#05080D", 0.56 * p))

    def ciz_kapi(c, t, o):
        p = ease("expo", clamp((t - 1.10) / 0.25))
        c.save(); c.translate(820 * (1 - p), 0)
        c.drawRect(skia.Rect(-560, -560, 560, -510), paint("#1A232B"))
        c.drawRect(skia.Rect(-560, 460, 560, 510), paint("#1A232B"))
        for bx in range(-500, 540, 92):
            c.drawRect(skia.Rect(bx - 12, -560, bx + 12, 560), paint("#1E2832"))
            c.drawRect(skia.Rect(bx - 12, -560, bx - 7, 560), paint("#4A6072", 0.55))
        c.drawRect(skia.Rect(-560, -40, -460, 70), paint("#2B3945"))
        if 0.70 < p < 1.0:
            c.drawCircle(-510, 15, 55 * (1 - (p - 0.70) / 0.30), paint("#FFF5D0", 0.85))
        c.restore()
        _damga(c, "LOCKED · 94941", 340, -250, clamp((t - 1.22) / 0.25), PLAN_C, boyut=32)

    ck.ekle(Oge("hucre", ciz_hucre, derinlik=0.55),
            Oge("michael_el", ciz_michael, x=W/2 - 55, y=H + 220, derinlik=0.88, ikincil=[("nefes", 1.2)],
                eylemler=[(ck.k("yourself"), 0.50, lambda p: dict(dx=62 * ease("out", p), s=1.0 + 0.05 * ease("out", p)))]),
            Oge("hucre_kapisi", ciz_kapi, x=W/2, y=H/2, derinlik=1.18))
    ck.kamera = Kamera(x=Iz([(0, W/2 - 35), (1.05, W/2 + 20, "out"), (2.6, W/2, "io")]),
                       y=Iz([(0, H/2), (2.6, H/2 - 30, "out")]),
                       z=Iz([(0, 1.04), (1.08, 1.18, "out"), (1.35, 1.06, "out"), (2.6, 1.14, "io")]),
                       sarsinti=[(1.15, 0.32, 22)])
    ck.ust.append(_hud("P.02", "Then you'd lock yourself inside.",
                       lambda t: "locked" if t >= 1.10 else ("yourself" if t >= 0.30 else "")))
    return ck

def ciz_parmaklik_perde(c, u):
    c.drawRect(skia.Rect(-95, 0, 95, H), paint("#0C1218"))
    c.drawRect(skia.Rect(-88, 0, -70, H), paint("#435A6E", 0.6))
    c.drawRect(skia.Rect(70, 0, 92, H), paint("#040608", 0.85))

def build_p03():
    kw = [("map", 0.75, 1.50), ("skin", 1.60, 2.40), ("history", 2.50, 3.35)]
    ck = Cekim("P.03", sure=3.8, kelimeler=kw, duygu=Duygu("merak"), arka="#0A111A")

    def ciz_arka(c, t, o):
        sh = skia.GradientShader.MakeRadial((0, -60), 920, [hexcol("#1B2D40"), hexcol("#070C12")])
        c.drawRect(skia.Rect(-W, -H, W, H), skia.Paint(Shader=sh))
        gp = paint(PLAN_C, 0.10, Style=skia.Paint.kStroke_Style, StrokeWidth=1.2)
        for x in range(-960, 980, 90): c.drawLine(x, -540, x, 540, gp)
        for y in range(-540, 560, 90): c.drawLine(-960, y, 960, y, gp)

    def ciz_sirt(c, t, o):
        c.save(); c.scale(1.38, 1.38); draw_sprite(c, SP_SIRT_0); c.restore()
        sp = ease("out", clamp((t - 0.75) / 0.85))
        if sp > 0:
            sy = -480 + 960 * sp
            c.save(); c.clipRect(skia.Rect(-560, -560, 560, sy)); c.scale(1.38, 1.38); draw_sprite(c, SP_SIRT_1); c.restore()
            if sp < 0.99:
                c.drawLine(-420, sy, 420, sy, paint("#FFFFFF", 0.95, Style=skia.Paint.kStroke_Style, StrokeWidth=4))
                c.drawLine(-420, sy, 420, sy, paint(PLAN_C, 0.55, Style=skia.Paint.kStroke_Style, StrokeWidth=14))

    def ciz_plan(c, t, o):
        p = ease("out", clamp((t - 1.60) / 0.70))
        if p <= 0: return
        c.save(); c.translate(0, -32 * p); c.rotate(math.sin(t * 2.2) * 2.2 * p)
        c.drawRect(skia.Rect(210, -290, 540, -70), paint("#071624", 0.65 * p))
        c.drawRect(skia.Rect(210, -290, 540, -70), paint(PLAN_C, 0.85 * p, Style=skia.Paint.kStroke_Style, StrokeWidth=2.5))
        dash = paint(PLAN_C, 0.95 * p, Style=skia.Paint.kStroke_Style, StrokeWidth=3, PathEffect=skia.DashPathEffect.Make([10, 7], -t * 75))
        c.drawLine(250, -245, 360, -245, dash); c.drawLine(360, -245, 360, -135, dash); c.drawLine(360, -135, 500, -135, dash)
        _yazi(c, "SECTOR A-B", 375, -305, 22, PLAN_C, p, bold=True)
        c.drawLine(-380 * p, 125, 380 * p, 125, paint(PLAN_C, 0.98, Style=skia.Paint.kStroke_Style, StrokeWidth=6))
        c.drawLine(-380 * p, 125, 380 * p, 125, paint("#FFFFFF", 0.75, Style=skia.Paint.kStroke_Style, StrokeWidth=2.5))
        c.restore()

    ck.ekle(Oge("arka", ciz_arka, derinlik=0.2), Oge("dovme_plan", ciz_sirt, x=W/2, y=H/2 + 45, derinlik=0.95, ikincil=[("nefes", 1.1)]),
            Oge("yatay_cizgi", ciz_plan, x=W/2, y=H/2 + 95, derinlik=1.1, ikincil=[("suz", 0.7)]),
            Oge("kinetik_harita", lambda c, t, o: _damga(c, "THE MAP", -430, -230, clamp((t - 2.50) / 0.28), PLAN_C, boyut=44), x=W/2, y=H/2, derinlik=1.2))
    ck.kamera = Kamera(x=Iz([(0, W/2 - 30), (1.6, W/2 + 25, "out"), (3.8, W/2, "io")]),
                       y=Iz([(0, H/2 - 20), (1.8, H/2 + 15, "out"), (3.8, H/2 + 45, "io")]),
                       z=Iz([(0, 1.02), (1.6, 1.14, "out"), (3.8, 1.24, "io")]))
    ck.ust.append(_hud("P.03", "And go down in history as the man with a map on his skin.",
                       lambda t: "history" if t >= 2.50 else ("skin" if t >= 1.60 else ("map" if t >= 0.75 else ""))))
    return ck

def build_p04():
    kw = [("now", 0.15, 0.70), ("eleven", 1.15, 2.00), ("dark", 2.25, 3.25)]
    ck = Cekim("P.04", sure=4.1, kelimeler=kw, duygu=Duygu("gerilim").gecis("korku", t0=2.25, sure=0.8), arka="#05080E")
    sp_zemin = _sp_layer(set_p04_depo_zemin, ["uzak", "orta", "sahne", "plan", "onplan"])

    def ciz_zemin_ve_flash(c, t, o):
        fo = 1.0 - clamp((t - 2.15) / 0.35)
        if fo > 0.01:
            c.save(); lp = skia.Paint(); lp.setAlphaf(fo); c.saveLayer(None, lp)
            c.scale(2.02, 2.02); draw_sprite(c, sp_zemin)
            c.restore(); c.restore()
            _damga(c, "AGE 11", 340, -180, clamp((t - 1.15) / 0.25) * fo, ALTIN, boyut=32)
        if 0.12 <= t <= 0.34:
            c.drawRect(skia.Rect(-W/2, -H/2, W/2, H/2), paint("#FFFFFF", clamp(1.0 - abs(t - 0.20) / 0.14) * 0.55))

    def ciz_cocuk(c, t, o):
        # Gerçek kilitli 11 yaş Michael v3 çizgili kazaklı figür (R4-PARALAKS tek katman!)
        c.save(); c.translate(0, 560); c.scale(1.80, 1.80); draw_sprite(c, SP_COCUK_FIG); c.restore()

    ck.ekle(
        Oge("isik_cizgisi", ciz_zemin_ve_flash, x=W/2, y=H/2, derinlik=1.0),
        Oge("cocuk_goz", ciz_cocuk, x=W/2, y=H/2 - 115, derinlik=1.0, giris=("belir", ck.k("dark", -0.20), 0.40), ikincil=[("nefes", 1.5), ("titre", 0.35)]),
    )
    ck.kamera = Kamera(x=Iz([(0, W/2), (4.1, W/2 + 12, "io")]),
                       y=Iz([(0, H/2 + 85), (1.95, H/2 + 75, "out"), (3.1, H/2 - 90, "out"), (4.1, H/2 - 105, "io")]),
                       z=Iz([(0, 1.04), (2.0, 1.12, "out"), (4.1, 1.24, "in")]), sarsinti=[(0.16, 0.22, 16)])
    ck.ust.append(_hud("P.04", "But right now? You're eleven. Locked in the dark.",
                       lambda t: "dark" if t >= 2.25 else ("eleven" if t >= 1.15 else ("now" if t >= 0.15 else ""))))
    return ck

def build_p05():
    kw = [("door", 0.20, 0.85), ("seeping", 1.00, 1.70), ("counting", 1.75, 2.75)]
    ck = Cekim("P.05", sure=3.4, kelimeler=kw, duygu=Duygu("korku").gecis("merak", t0=1.75, sure=0.75), arka="#070C14")

    def ciz_depo(c, t, o):
        c.save(); c.scale(2.05, 2.05); draw_sprite(c, SP_DEPO); c.restore()
        sh = skia.GradientShader.MakeLinear([(0, 95), (0, 295)], [hexcol(ALTIN, 0.52), hexcol(ALTIN, 0.0)])
        beam = skia.Path(); beam.moveTo(-210, 95); beam.lineTo(210, 95); beam.lineTo(410, 295); beam.lineTo(-410, 295); beam.close()
        c.drawPath(beam, skia.Paint(AntiAlias=True, Shader=sh, BlendMode=skia.BlendMode.kScreen))

    def ciz_golge(c, t, o):
        sp = clamp((t - 0.25) / 1.15)
        if 0 < sp < 1:
            sx = -260 + 520 * ease("io", sp)
            sh = skia.GradientShader.MakeRadial((sx, 25), 95, [hexcol("#05080E", 0.78), hexcol("#05080E", 0.0)])
            c.drawOval(skia.Rect(sx - 100, -18, sx + 100, 95), skia.Paint(AntiAlias=True, Shader=sh))

    def ciz_plan(c, t, o):
        p = ease("out", clamp((t - 1.00) / 0.65))
        if p <= 0: return
        gp = paint(PLAN_C, 0.92, Style=skia.Paint.kStroke_Style, StrokeWidth=3)
        c.drawLine(-280, -240, -280 + 25 * p, -240 + 280 * p, gp)
        c.drawLine(240, -180, 240 + 30 * p, -180 + 270 * p, gp)
        c.drawLine(-195 * p, 95, 195 * p, 95, paint(PLAN_C, 0.85, Style=skia.Paint.kStroke_Style, StrokeWidth=2.5, PathEffect=skia.DashPathEffect.Make([12, 8], -t * 85)))

    def ciz_sayac(c, t, o):
        tags = [(-268, -125, "01 · CRACK"), (255, -75, "02 · NAIL"), (-295, 155, "03 · DUST"), (215, 155, "04 · LIGHT")]
        for i, (tx, ty, lbl) in enumerate(tags):
            pi = ease("back", clamp((t - (1.75 + i * 0.18)) / 0.22))
            if pi <= 0: continue
            c.drawCircle(tx, ty, (16 + 3.5 * math.sin(t * 10 + i)) * pi, paint(PLAN_C, 0.95, Style=skia.Paint.kStroke_Style, StrokeWidth=3))
            c.drawCircle(tx, ty, 5 * pi, paint("#FFFFFF", 1.0))
            _yazi(c, lbl, tx + 24, ty - 10, 22, PLAN_C, clamp(pi), bold=True, align="left")

    ck.ekle(Oge("depo", ciz_depo, derinlik=0.55), Oge("kapi_araligi", ciz_golge, x=W/2, y=H/2 + 95, derinlik=0.85),
            Oge("tahta_ayrinti", ciz_plan, x=W/2, y=H/2, derinlik=1.0), Oge("sayac_noktalar", ciz_sayac, x=W/2, y=H/2, derinlik=1.1))
    ck.kamera = Kamera(x=Iz([(0, W/2 - 20), (1.7, W/2 + 12, "out"), (3.4, W/2, "io")]),
                       y=Iz([(0, H/2 - 15), (3.4, H/2 + 70, "io")]), z=Iz([(0, 1.04), (1.7, 1.16, "out"), (3.4, 1.30, "in")]))
    ck.ust.append(_hud("P.05", "And you're counting the light seeping under the door.",
                       lambda t: "counting" if t >= 1.75 else ("seeping" if t >= 1.00 else ("door" if t >= 0.20 else ""))))
    return ck

def build_p06():
    ck = Cekim("P.06", sure=2.2, kelimeler=[], duygu=Duygu("merak"), arka="#0B131E")

    def ciz_zemin(c, t, o):
        sh = skia.GradientShader.MakeRadial((0, 0), 960, [hexcol("#16293D"), hexcol("#070B12")])
        c.drawRect(skia.Rect(-W, -H, W, H), skia.Paint(Shader=sh))
        gp = paint(PLAN_C, 0.14, Style=skia.Paint.kStroke_Style, StrokeWidth=1.5)
        for x in range(-960, 980, 80): c.drawLine(x, -540, x, 540, gp)
        for y in range(-540, 560, 80): c.drawLine(-960, y, 960, y, gp)

    def ciz_kapi(c, t, o):
        p = ease("out", clamp(t / 0.55))
        w, h = 340 + 460 * p, 420 + 80 * p
        c.drawRect(skia.Rect(-w/2, -h/2, w/2, h/2), paint("#FFFFFF", 0.06))
        c.drawRect(skia.Rect(-w/2, -h/2, w/2, h/2), paint(PLAN_C, 0.85, Style=skia.Paint.kStroke_Style, StrokeWidth=3))
        c.drawLine(-w/2, h/2, w/2, h/2, paint(ALTIN, 0.95, Style=skia.Paint.kStroke_Style, StrokeWidth=6))

    def ciz_baslik(c, t, o):
        p = ease("out", clamp((t - 0.25) / 0.65))
        if p <= 0: return
        c.save(); c.clipRect(skia.Rect(-820, -180, -820 + 1640 * p, 180))
        _yazi(c, "WHAT IF YOU WERE BORN AS", 0, -42, 42, PLAN_C, 0.95, bold=True)
        _yazi(c, "MICHAEL SCOFIELD?", 0, 46, 76, "#FFFFFF", 0.98, bold=True)
        c.restore()

    ck.ekle(Oge("zemin", ciz_zemin, derinlik=0.2), Oge("baslik_kapi", ciz_kapi, derinlik=0.75, giris=("buyu", 0.0, 0.5)),
            Oge("baslik_yazi", ciz_baslik, derinlik=1.0, giris=("ciz", 0.2, 0.7)))
    ck.kamera = Kamera(z=Iz([(0, 1.0), (2.2, 1.09, "io")]))
    ck.ust.append(_hud("P.06", "TITLE CARD · Light under the door opens into Act I", lambda t: "TITLE"))
    return ck

def build_film():
    p = [build_p01(), build_p02(), build_p03(), build_p04(), build_p05(), build_p06()]
    return Film([
        p[0], ZoomIcinden("hedef_01", sure=0.65, renk=PLAN_C),
        p[1], OnPlanSil(ciz_parmaklik_perde, sure=0.55),
        p[2], Eslesme("yatay_cizgi", "isik_cizgisi", sure=0.65),
        p[3], ZoomIcinden("cocuk_goz", sure=0.65, renk=ALTIN),
        p[4], Maske("kapi_araligi", boyut=(380, 90), sure=0.70),
        p[5],
    ])

if __name__ == "__main__":
    film = build_film()
    bas = film.bas
    anlar = [
        ("P.01 · CAD Scan & BY HEART",    bas[0] + 2.85), ("TRANS 1 · Zoom (01 CELL)",      bas[1] + 0.32),
        ("P.02 · LOCKED · 94941",         bas[1] + 1.65), ("TRANS 2 · Bar Wipe",            bas[2] + 0.27),
        ("P.03 · Anatomical Back & MAP",  bas[2] + 2.95), ("TRANS 3 · Line → Door Light",   bas[3] + 0.32),
        ("P.04 · AGE 11 Sneakers",        bas[3] + 1.75), ("P.04 · 11yo Striped Sweater",   bas[3] + 3.25),
        ("TRANS 4 · Eye Zoom",            bas[4] + 0.32), ("P.05 · 01–04 Counting Light",   bas[4] + 2.55),
        ("TRANS 5 · Door Mask",           bas[5] + 0.35), ("P.06 · English Title Card",     bas[5] + 1.55),
    ]
    pngler = film.onizle([t for _, t in anlar], str(P / "kareler_prolog_en"), olcek=0.5)
    cols, rows, tw, th, pad, top = 4, 3, 440, 248, 16, 56
    sheet = Image.new("RGB", (cols*tw+(cols+1)*pad, top+rows*(th+28)+pad), (11, 16, 24))
    draw = ImageDraw.Draw(sheet)
    ft = ImageFont.truetype(str(REPO / "fonts/AlegreyaSC-Bold.ttf"), 22)
    fl = ImageFont.truetype(str(REPO / "fonts/Alegreya.ttf"), 16)
    draw.text((pad, 14), f"PROLOG F4b ENGLISH KONTAKT (960 px) · {film.sure:.1f}s · 5/5 Semantic Transitions", fill=(127,230,255), font=ft)
    for i, ((etiket, t), p) in enumerate(zip(anlar, pngler)):
        r, c = divmod(i, cols); x, y = pad + c*(tw+pad), top + r*(th+28)
        sheet.paste(Image.open(p).convert("RGB").resize((tw, th), Image.Resampling.LANCZOS), (x, y))
        draw.rectangle([x, y, x+tw, y+th], outline=(60, 90, 115), width=2)
        draw.text((x+4, y+th+4), f"{etiket} ({t:.2f}s)", fill=(225, 232, 240), font=fl)
    out_png = P / "prolog_en_kontakt_960.png"
    sheet.save(out_png)
    print("PROLOG EN KONTAKT OK:", out_png, flush=True)
