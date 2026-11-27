"""F4b Act I ("The Crane") Block Animatic v3 — 100% ENGLISH, High-Detail 5-Layer Parallax Sets (V1·V2·V3).

- Uses all 9 Görsel Kurul 3/3-approved 5-layer illustrated sets (b1_set_cocukluk, b1_set_turna, b1_set_muhendis)
  plus locked am_mekanlar Depo (1.04), Turna v4, 11yo Michael v3, and Lincoln v1.
- True 5-layer depth parallax (uzak 0.45, orta 0.72, sahne 1.0, plan 1.08 with live CAD scan reveal, onplan 1.25).
- 100% English narration HUD, kinetic stamps, and diegetic text; 9/9 semantic transitions.

Outputs:
  - blok/bolum1_v3_en_kontakt_960.png  (16-frame contact sheet: 10 shots + 6 key transitions)
  - blok/bolum1_v3_en_960.mp4          (960×540, 16 fps fast draft)
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
from kartlar.b1_set_cocukluk import set_101_kapi, set_102_mutfak, set_103_islahevi_kilit
from kartlar.b1_set_turna import set_105_sabah_yatak, set_106_lise_origami, set_107_lokanta_cek
from kartlar.b1_set_muhendis import set_108_chicago_ofis, set_109_taslak_masasi, set_110_idam_manset

PLAN_C = "#7FE6FF"
ALTIN = "#FFD88A"
KIRMIZI = "#FF4D38"
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

def _yazi(c, metin, x, y, boyut=34, renk="#FFFFFF", a=1.0, bold=True, align="center"):
    font = skia.Font(TF_BOLD if bold else TF_REG, boyut)
    w = font.measureText(metin)
    tx = x - w / 2 if align == "center" else (x - w if align == "right" else x)
    c.drawString(metin, tx, y, font, paint(renk, a))

def _damga(c, metin, x, y, p, renk=PLAN_C, boyut=30):
    if p <= 0.01:
        return
    sc = 1.28 - 0.28 * ease("back", clamp(p))
    al = clamp(p * 2.4)
    c.save()
    c.translate(x, y); c.scale(sc, sc)
    font = skia.Font(TF_BOLD, boyut)
    tw = font.measureText(metin)
    rect = skia.Rect(-tw/2 - 18, -boyut/2 - 10, tw/2 + 18, boyut/2 + 8)
    c.drawRect(rect, paint("#07121E", 0.85 * al))
    c.drawRect(rect, paint(renk, 0.95 * al, Style=skia.Paint.kStroke_Style, StrokeWidth=2.6))
    _yazi(c, metin, 0, boyut * 0.30, boyut, renk, al, bold=True, align="center")
    c.restore()

def _hud(cid, cumle, kw_fn):
    def _ciz(c, t):
        c.drawRect(skia.Rect(0, H - 62, W, H), paint("#060A10", 0.80))
        c.drawLine(0, H - 62, W, H - 62, paint(PLAN_C, 0.42, StrokeWidth=2))
        _yazi(c, cid, 64, H - 22, 21, PLAN_C, 0.95, bold=True, align="left")
        _yazi(c, cumle, W / 2, H - 22, 23, "#EEF3F8", 0.95, bold=False, align="center")
        kw = kw_fn(t)
        if kw:
            _yazi(c, f"«{kw}»", W - 56, H - 22, 20, ALTIN, 0.98, bold=True, align="right")
    return _ciz

# ───────── 5-Layer Set Sprite Helper (960×540 SVG → 1920×1080 world via scale 2.0)
def _sp_layer(fn, katmanlar, ss=1.0):
    defs, body = fn(katmanlar=katmanlar)
    return svg_sprite(body, 960, 540, ax=480, ay=270, ss=ss, defs=f"<defs>{defs}</defs>")

def _draw_2x(sp):
    return lambda c, t, o: (c.save(), c.scale(2.02, 2.02), draw_sprite(c, sp), c.restore())

def _draw_scan_2x(sp, t0, sure=0.75, vertical=False):
    """Canlı CAD lazer tarama ile plan katmanını kelime anında ekrana çizer!"""
    def _ciz(c, t, o):
        p = ease("out", clamp((t - t0) / sure))
        if p <= 0.005:
            return
        c.save()
        if vertical:
            sy = -H/2 + H * p
            c.clipRect(skia.Rect(-W/2, -H/2, W/2, sy))
            c.scale(2.02, 2.02); draw_sprite(c, sp)
            c.restore()
            if p < 0.98:
                c.drawLine(-W/2, sy, W/2, sy, paint("#FFFFFF", 0.95, Style=skia.Paint.kStroke_Style, StrokeWidth=4))
                c.drawLine(-W/2, sy, W/2, sy, paint(PLAN_C, 0.50, Style=skia.Paint.kStroke_Style, StrokeWidth=14))
        else:
            sx = -W/2 + W * p
            c.clipRect(skia.Rect(-W/2, -H/2, sx, H/2))
            c.scale(2.02, 2.02); draw_sprite(c, sp)
            c.restore()
            if p < 0.98:
                c.drawLine(sx, -H/2, sx, H/2, paint("#FFFFFF", 0.95, Style=skia.Paint.kStroke_Style, StrokeWidth=4))
                c.drawLine(sx, -H/2, sx, H/2, paint(PLAN_C, 0.50, Style=skia.Paint.kStroke_Style, StrokeWidth=14))
    return _ciz

# Locked props/characters
SP_TURNA = svg_sprite(f'<g transform="translate(150,120) scale(0.95)">{K.turna(1.0, isik=0.7, kanat=0.0)}</g>', 300, 240, ax=150, ay=120, ss=0.85)
SP_TURNA_UC = svg_sprite(f'<g transform="translate(150,120) scale(0.95)">{K.turna(1.0, isik=0.5, kanat=0.7)}</g>', 300, 240, ax=150, ay=120, ss=0.85)
SP_COCUK_FIG = svg_sprite(f'<g transform="translate(260,520) scale(1.0)">{K.michael_cocuk_figur("korku", lighting="prolog")}</g>', 520, 560, ax=260, ay=520, ss=0.8)
SP_DEPO_BASE = _sp_layer(lambda katmanlar=None: K.mekan_depo(katmanlar=katmanlar, plan_gorusu=False), ["uzak", "orta"])

# ───────── 1.01 · Family Front Door (BURROWS → SCOFIELD)
def build_101():
    kw = [("father", 0.30, 0.95), ("walks", 1.25, 1.90), ("name", 2.15, 3.00)]
    ck = Cekim("1.01", sure=3.6, kelimeler=kw, duygu=Duygu("huzur").gecis("yalnizlik", t0=1.25, sure=0.9), arka="#0E121A")
    sp_u = _sp_layer(set_101_kapi, ["uzak"])
    sp_o = _sp_layer(set_101_kapi, ["orta"])
    sp_s = _sp_layer(set_101_kapi, ["sahne"])
    sp_p = _sp_layer(set_101_kapi, ["plan"])
    sp_f = _sp_layer(set_101_kapi, ["onplan"])

    def ciz_yagmur_ve_damga(c, t, o):
        for i in range(18):
            rx = -820 + (i * 47) % 420
            ry = -420 + ((i * 73 + t * 520) % 760)
            c.drawLine(rx, ry, rx - 8, ry + 26, paint("#B8D4EE", 0.38, Style=skia.Paint.kStroke_Style, StrokeWidth=2))
        _damga(c, "BURROWS → SCOFIELD", 250, -320, clamp((t - 2.15) / 0.30), PLAN_C, boyut=32)

    ck.ekle(
        Oge("uzak", _draw_2x(sp_u), derinlik=0.45),
        Oge("orta", _draw_2x(sp_o), derinlik=0.72),
        Oge("sahne", _draw_2x(sp_s), derinlik=1.0),
        Oge("plan", _draw_scan_2x(sp_p, ck.k("name"), 0.55), derinlik=1.08),
        Oge("onplan", _draw_2x(sp_f), derinlik=1.22),
        Oge("fx_101", ciz_yagmur_ve_damga, derinlik=1.28),
    )
    ck.kamera = Kamera(
        x=Iz([(0, W/2 - 140), (1.4, W/2 - 20, "out"), (3.6, W/2 + 85, "io")]),
        y=Iz([(0, H/2 + 20), (3.6, H/2 - 15, "io")]),
        z=Iz([(0, 1.04), (1.3, 1.12, "out"), (3.6, 1.24, "in")]),
        sarsinti=[(1.40, 0.25, 14)],
    )
    ck.ust.append(_hud("1.01", "Before you're even born, your father walks out. Your name changes.",
                       lambda t: "name" if t >= 2.15 else ("walks" if t >= 1.25 else ("father" if t >= 0.30 else ""))))
    return ck

def ciz_kapi_sil(c, u):
    c.drawRect(skia.Rect(-115, 0, 115, H), paint("#2B1C14"))
    c.drawRect(skia.Rect(-115, 0, -98, H), paint(ALTIN, 0.35))
    c.drawRect(skia.Rect(92, 0, 115, H), paint("#06080C", 0.85))

# ───────── 1.02 · Rainy Kitchen (AGE 11 & '?')
def build_102():
    kw = [("eleven", 0.25, 0.90), ("dies", 1.45, 2.15), ("told", 2.60, 3.55)]
    ck = Cekim("1.02", sure=4.0, kelimeler=kw, duygu=Duygu("huzur").gecis("yas", t0=1.45, sure=0.85), arka="#101720")
    sp_u = _sp_layer(set_102_mutfak, ["uzak"])
    sp_o = _sp_layer(set_102_mutfak, ["orta"])
    sp_s = _sp_layer(set_102_mutfak, ["sahne"])
    sp_p = _sp_layer(set_102_mutfak, ["plan"])
    sp_f = _sp_layer(set_102_mutfak, ["onplan"])

    def ciz_fx(c, t, o):
        for i in range(16):
            rx = -340 + (i * 53) % 680
            ry = -340 + ((i * 61 + t * 220) % 340)
            c.drawLine(rx, ry, rx - 3, ry + 18, paint("#A6C8E4", 0.42, Style=skia.Paint.kStroke_Style, StrokeWidth=2))
        _damga(c, "AGE 11", -590, -295, clamp((t - 0.25) / 0.30) * (1.0 - clamp((t - 3.2) / 0.4)), ALTIN, boyut=30)

    ck.ekle(
        Oge("uzak", _draw_2x(sp_u), derinlik=0.45),
        Oge("orta", _draw_2x(sp_o), derinlik=0.75),
        Oge("sahne", _draw_2x(sp_s), derinlik=1.0),
        Oge("plan", _draw_scan_2x(sp_p, ck.k("told", -0.25), 0.65), derinlik=1.08),
        Oge("onplan", _draw_2x(sp_f), derinlik=1.24),
        Oge("fx_102", ciz_fx, derinlik=1.26),
        Oge("mutfak_pencere", lambda c, t, o: None, x=W/2 + 40, y=H/2 - 115, derinlik=0.8),
    )
    ck.kamera = Kamera(
        x=Iz([(0, W/2 - 80), (2.2, W/2 + 20, "io"), (4.0, W/2 + 55, "in")]),
        y=Iz([(0, H/2 + 55), (4.0, H/2 - 80, "io")]),
        z=Iz([(0, 1.04), (4.0, 1.24, "io")]),
    )
    ck.ust.append(_hud("1.02", "At eleven, your mother dies. At least, that's what you're told.",
                       lambda t: "told" if t >= 2.60 else ("dies" if t >= 1.45 else ("eleven" if t >= 0.25 else ""))))
    return ck

# ───────── 1.03 · Juvenile Hall & Foster Closet Lock (JUVENILE HALL / LOCKED)
def build_103():
    kw = [("lincoln", 0.25, 0.95), ("foster", 1.45, 2.15), ("locked", 2.35, 3.25)]
    ck = Cekim("1.03", sure=3.8, kelimeler=kw, duygu=Duygu("yalnizlik").gecis("korku", t0=2.35, sure=0.65), arka="#0A0F16")
    sp_u = _sp_layer(set_103_islahevi_kilit, ["uzak"])
    sp_o = _sp_layer(set_103_islahevi_kilit, ["orta"])
    sp_s = _sp_layer(set_103_islahevi_kilit, ["sahne"])
    sp_p = _sp_layer(set_103_islahevi_kilit, ["plan"])
    sp_f = _sp_layer(set_103_islahevi_kilit, ["onplan"])

    def ciz_fx(c, t, o):
        # çarpma kıvılcımı + LOCKED damgası
        ps = clamp((t - 2.35) / 0.28)
        if 0 < ps < 1:
            c.drawCircle(240, 80, 75 * (1 - ps), paint(ALTIN, 0.85 * (1 - ps)))
        _damga(c, "JUVENILE HALL", -440, -320, clamp((t - 0.35) / 0.30) * (1.0 - clamp((t - 1.9) / 0.3)), "#9EC2DC", boyut=28)
        _damga(c, "LOCKED", 340, -290, clamp((t - 2.40) / 0.26), ALTIN, boyut=36)

    ck.ekle(
        Oge("uzak", _draw_2x(sp_u), derinlik=0.45),
        Oge("orta", _draw_2x(sp_o), derinlik=0.75),
        Oge("sahne", _draw_2x(sp_s), derinlik=1.0),
        Oge("plan", _draw_scan_2x(sp_p, ck.k("locked", -0.2), 0.55), derinlik=1.08),
        Oge("onplan", _draw_2x(sp_f), derinlik=1.22),
        Oge("fx_103", ciz_fx, derinlik=1.26),
        Oge("kilit_surgu", lambda c, t, o: None, x=W/2 + 250, y=H/2 + 60, derinlik=1.0),
    )
    ck.kamera = Kamera(
        x=Iz([(0, W/2 - 220), (1.6, W/2 + 120, "out"), (3.8, W/2 + 210, "in")]),
        y=Iz([(0, H/2), (3.8, H/2 + 40, "io")]),
        z=Iz([(0, 1.12), (1.8, 1.06, "out"), (3.8, 1.30, "in")]),
        sarsinti=[(2.38, 0.30, 22)],
    )
    ck.ust.append(_hud("1.03", "Your brother Lincoln is in juvenile hall. Your foster home locks you in the dark.",
                       lambda t: "locked" if t >= 2.35 else ("foster" if t >= 1.45 else ("lincoln" if t >= 0.25 else ""))))
    return ck

# ───────── 1.04 · Dark Closet · Low Latent Inhibition (Live CAD Scan + 01–06)
def build_104():
    kw = [("dark", 0.25, 0.90), ("filter", 1.30, 2.10), ("everything", 2.45, 3.55)]
    ck = Cekim("1.04", sure=4.2, kelimeler=kw, duygu=Duygu("korku").gecis("merak", t0=2.45, sure=0.75), arka="#060A12")

    def ciz_depo(c, t, o):
        c.save(); c.scale(2.05, 2.05); draw_sprite(c, SP_DEPO_BASE); c.restore()
        sh = skia.GradientShader.MakeLinear([(0, 95), (0, 295)], [hexcol(ALTIN, 0.54), hexcol(ALTIN, 0.0)])
        beam = skia.Path()
        beam.moveTo(-210, 95); beam.lineTo(210, 95); beam.lineTo(420, 295); beam.lineTo(-420, 295); beam.close()
        c.drawPath(beam, skia.Paint(AntiAlias=True, Shader=sh, BlendMode=skia.BlendMode.kScreen))

    def ciz_cocuk(c, t, o):
        # Gerçek kilitli 11 yaş Michael v3 tam figür (çizgili kazak net görünür, karartı DEĞİL!)
        c.save(); c.translate(0, 390); c.scale(1.45, 1.45); draw_sprite(c, SP_COCUK_FIG); c.restore()
        # "everything" kelimesinde gözlerde camgöbeği parıltı
        gp = clamp((t - 2.45) / 0.35)
        if gp > 0:
            c.drawCircle(18, -125, 5.5 * gp, paint(PLAN_C, 0.95))
            c.drawCircle(-14, -125, 5.0 * gp, paint(PLAN_C, 0.95))

    def ciz_cad(c, t, o):
        p = ease("out", clamp((t - 1.30) / 0.95))
        if p <= 0:
            return
        sx = -760 + 1520 * p
        c.save(); c.clipRect(skia.Rect(-760, -400, sx, 400))
        gp = paint(PLAN_C, 0.88, Style=skia.Paint.kStroke_Style, StrokeWidth=2.6)
        c.drawLine(-520, -280, -490, 160, gp)
        c.drawLine(360, -260, 390, 180, gp)
        c.drawLine(-340, 115, 340, 115, paint(PLAN_C, 0.98, Style=skia.Paint.kStroke_Style, StrokeWidth=5))
        c.drawRect(skia.Rect(-640, 40, -340, 260), gp)
        c.drawRect(skia.Rect(340, 60, 620, 260), gp)
        c.restore()
        if p < 0.99:
            c.drawLine(sx, -420, sx, 420, paint("#FFFFFF", 0.95, Style=skia.Paint.kStroke_Style, StrokeWidth=4))
            c.drawLine(sx, -420, sx, 420, paint(PLAN_C, 0.5, Style=skia.Paint.kStroke_Style, StrokeWidth=14))

    def ciz_noktalar(c, t, o):
        pts = [(-505, -140, "01 · GRAIN"), (-120, -190, "02 · BOLT"), (200, -160, "03 · NAIL"), (375, -40, "04 · CRATE"), (0, 115, "05 · LIGHT")]
        for i, (px, py, lbl) in enumerate(pts):
            pi = ease("back", clamp((t - (2.45 + i * 0.13)) / 0.18))
            if pi <= 0:
                continue
            c.drawCircle(px, py, 14 * pi, paint(PLAN_C, 0.95, Style=skia.Paint.kStroke_Style, StrokeWidth=3))
            c.drawCircle(px, py, 4.5 * pi, paint("#FFFFFF", 1.0))
            _yazi(c, lbl, px + 20, py - 8, 20, PLAN_C, clamp(pi), bold=True, align="left")
        _damga(c, "LOW LATENT INHIBITION", 150, -285, clamp((t - 2.65) / 0.28), PLAN_C, boyut=34)

    ck.ekle(
        Oge("depo", ciz_depo, derinlik=0.55),
        Oge("cocuk_michael", ciz_cocuk, x=W/2 - 390, y=H/2 + 125, derinlik=0.92, ikincil=[("nefes", 1.5)]),
        Oge("tahta_catlak", ciz_cad, x=W/2, y=H/2 + 115, derinlik=1.0),
        Oge("plan_noktalar", ciz_noktalar, x=W/2, y=H/2, derinlik=1.1),
    )
    ck.kamera = Kamera(
        x=Iz([(0, W/2 - 200), (1.35, W/2, "out"), (4.2, W/2 + 40, "io")]),
        z=Iz([(0, 1.22), (1.35, 1.02, "out"), (4.2, 1.18, "io")]),
    )
    ck.ust.append(_hud("1.04", "In the dark, your mind can't filter details. Low latent inhibition: you see everything.",
                       lambda t: "everything" if t >= 2.45 else ("filter" if t >= 1.30 else ("dark" if t >= 0.25 else ""))))
    return ck

# ───────── 1.05 · Morning Bedside (I'M HERE + Turna v4)
def build_105():
    kw = [("morning", 0.25, 0.90), ("crane", 1.25, 2.00), ("here", 2.40, 3.40)]
    ck = Cekim("1.05", sure=4.0, kelimeler=kw, duygu=Duygu("yalnizlik").gecis("umut", t0=1.0, sure=0.85), arka="#1B1610")
    sp_u = _sp_layer(set_105_sabah_yatak, ["uzak"])
    sp_o = _sp_layer(set_105_sabah_yatak, ["orta"])
    sp_s = _sp_layer(set_105_sabah_yatak, ["sahne"])
    sp_p = _sp_layer(set_105_sabah_yatak, ["plan"])
    sp_f = _sp_layer(set_105_sabah_yatak, ["onplan"])

    def ciz_fx(c, t, o):
        for i in range(18):
            dx = -300 + (i * 59 + t * 28) % 720
            dy = -260 + ((i * 41 + t * 18) % 520)
            c.drawCircle(dx, dy, 2.8, paint(ALTIN, 0.55))
        _damga(c, "I'M HERE", 240, -290, clamp((t - 2.40) / 0.30), ALTIN, boyut=44)

    ck.ekle(
        Oge("sabah_isigi", _draw_2x(sp_u), derinlik=0.45),
        Oge("orta", _draw_2x(sp_o), derinlik=0.75),
        Oge("turna", _draw_2x(sp_s), derinlik=1.0),
        Oge("plan", _draw_scan_2x(sp_p, ck.k("crane"), 0.65), derinlik=1.08),
        Oge("onplan", _draw_2x(sp_f), derinlik=1.22),
        Oge("fx_105", ciz_fx, derinlik=1.26),
    )
    ck.kamera = Kamera(
        x=Iz([(0, W/2 - 60), (4.0, W/2 + 55, "io")]),
        y=Iz([(0, H/2 + 25), (4.0, H/2 - 20, "io")]),
        z=Iz([(0, 1.04), (4.0, 1.24, "io")]),
    )
    ck.ust.append(_hud("1.05", "The next morning, you find a paper crane by your bed. Lincoln's sign: I'm here.",
                       lambda t: "here" if t >= 2.40 else ("crane" if t >= 1.25 else ("morning" if t >= 0.25 else ""))))
    return ck

def ciz_ucan_turna(c, u):
    sp = SP_TURNA_UC if (int(u * 8) % 2 == 0) else SP_TURNA
    c.save(); c.scale(1.3, 1.3); draw_sprite(c, sp); c.restore()

# ───────── 1.06 · High School Craft Desk (HIGH SCHOOL + 5 Soaring Cranes)
def build_106():
    kw = [("high", 0.25, 0.85), ("origami", 1.15, 1.90), ("language", 2.20, 3.10)]
    ck = Cekim("1.06", sure=3.6, kelimeler=kw, duygu=Duygu("umut"), arka="#192029")
    sp_u = _sp_layer(set_106_lise_origami, ["uzak"])
    sp_o = _sp_layer(set_106_lise_origami, ["orta"])
    sp_s = _sp_layer(set_106_lise_origami, ["sahne"])
    sp_p = _sp_layer(set_106_lise_origami, ["plan"])
    sp_f = _sp_layer(set_106_lise_origami, ["onplan"])

    def ciz_fx(c, t, o):
        _damga(c, "HIGH SCHOOL · ORIGAMI", -410, -310, clamp((t - 0.25) / 0.30), ALTIN, boyut=28)

    ck.ekle(
        Oge("uzak", _draw_2x(sp_u), derinlik=0.45),
        Oge("orta", _draw_2x(sp_o), derinlik=0.75),
        Oge("turna", _draw_2x(sp_s), derinlik=1.0),
        Oge("plan", _draw_scan_2x(sp_p, ck.k("origami"), 0.65), derinlik=1.08),
        Oge("onplan", _draw_2x(sp_f), derinlik=1.22),
        Oge("fx_106", ciz_fx, derinlik=1.26),
    )
    ck.kamera = Kamera(
        x=Iz([(0, W/2 - 110), (3.6, W/2 + 135, "io")]),
        y=Iz([(0, H/2 + 30), (3.6, H/2 - 40, "io")]),
        z=Iz([(0, 1.06), (3.6, 1.18, "io")]),
    )
    ck.ust.append(_hud("1.06", "In high school shop class, you master origami. Paper becomes your language.",
                       lambda t: "language" if t >= 2.20 else ("origami" if t >= 1.15 else ("high" if t >= 0.25 else ""))))
    return ck

# ───────── 1.07 · Night Diner & $90,000 Sacrifice (Lincoln v1 + Loan Sharks Outside)
def build_107():
    kw = [("eighteen", 0.25, 0.90), ("ninety", 1.25, 2.00), ("insurance", 2.45, 3.45)]
    ck = Cekim("1.07", sure=4.0, kelimeler=kw, duygu=Duygu("umut").gecis("gerilim", t0=2.45, sure=0.8), arka="#0E121A")
    sp_u = _sp_layer(set_107_lokanta_cek, ["uzak"])
    sp_o = _sp_layer(set_107_lokanta_cek, ["orta"])
    sp_s = _sp_layer(set_107_lokanta_cek, ["sahne"])
    sp_p = _sp_layer(set_107_lokanta_cek, ["plan"])
    sp_f = _sp_layer(set_107_lokanta_cek, ["onplan"])

    def ciz_fx(c, t, o):
        _damga(c, "AGE 18 · $90,000", -480, -320, clamp((t - 0.25) / 0.30), ALTIN, boyut=28)

    ck.ekle(
        Oge("uzak", _draw_2x(sp_u), derinlik=0.65),
        Oge("cek_kagit", _draw_2x(_sp_layer(set_107_lokanta_cek, ["orta", "sahne", "onplan"])), derinlik=1.0),
        Oge("plan", _draw_scan_2x(sp_p, ck.k("insurance", -0.2), 0.60), derinlik=1.0),
        Oge("fx_107", ciz_fx, derinlik=1.0),
    )
    ck.kamera = Kamera(
        x=Iz([(0, W/2 - 120), (2.2, W/2 + 40, "io"), (4.0, W/2 + 140, "in")]),
        y=Iz([(0, H/2 + 40), (4.0, H/2 - 45, "io")]),
        z=Iz([(0, 1.06), (4.0, 1.24, "io")]),
    )
    ck.ust.append(_hud("1.07", "At eighteen, Lincoln hands you ninety thousand dollars. Your mother's insurance, he claims.",
                       lambda t: "insurance" if t >= 2.45 else ("ninety" if t >= 1.25 else ("eighteen" if t >= 0.25 else ""))))
    return ck

def ciz_cek_diploma(c, u):
    c.drawRect(skia.Rect(-175, -88, 175, 88), paint("#F0E8D4"))
    c.drawRect(skia.Rect(-175, -88, 175, 88), paint(ALTIN if u > 0.5 else INK, 0.95, Style=skia.Paint.kStroke_Style, StrokeWidth=4))
    _yazi(c, "$90,000" if u < 0.5 else "STRUCTURAL ENGINEER", 0, 12, 36 if u < 0.5 else 24, "#1A4D2E" if u < 0.5 else "#142438", 0.98, bold=True)

# ───────── 1.08 · Chicago Office & Live CAD Skyline Scan (STRUCTURAL ENGINEER)
def build_108():
    kw = [("engineer", 0.30, 1.05), ("inside", 1.65, 2.75)]
    ck = Cekim("1.08", sure=3.8, kelimeler=kw, duygu=Duygu("zafer"), arka="#0B1522")
    sp_u = _sp_layer(set_108_chicago_ofis, ["uzak"])
    sp_o = _sp_layer(set_108_chicago_ofis, ["orta"])
    sp_s = _sp_layer(set_108_chicago_ofis, ["sahne"])
    sp_p = _sp_layer(set_108_chicago_ofis, ["plan"])
    sp_f = _sp_layer(set_108_chicago_ofis, ["onplan"])

    def ciz_fx(c, t, o):
        _damga(c, "STRUCTURAL ENGINEER", 240, -320, clamp((t - 0.30) / 0.32), ALTIN, boyut=32)

    ck.ekle(
        Oge("uzak", _draw_2x(sp_u), derinlik=0.45),
        Oge("cad_plan", _draw_2x(sp_o), derinlik=0.75),
        Oge("diploma", _draw_2x(sp_s), derinlik=1.0),
        Oge("plan", _draw_scan_2x(sp_p, ck.k("inside", -0.2), 0.85), derinlik=1.08),
        Oge("onplan", _draw_2x(sp_f), derinlik=1.22),
        Oge("fx_108", ciz_fx, derinlik=1.26),
    )
    ck.kamera = Kamera(
        x=Iz([(0, W/2 - 140), (1.8, W/2 + 40, "out"), (3.8, W/2 + 120, "in")]),
        y=Iz([(0, H/2 + 30), (3.8, H/2 - 40, "io")]),
        z=Iz([(0, 1.06), (3.8, 1.24, "in")]),
    )
    ck.ust.append(_hud("1.08", "With that money, you become a Chicago structural engineer. You read every building from the inside.",
                       lambda t: "inside" if t >= 1.65 else ("engineer" if t >= 0.30 else "")))
    return ck

# ───────── 1.09 · Architect's Drafting Table (FOX RIVER STATE PENITENTIARY + Turna v4)
def build_109():
    kw = [("prison", 0.30, 1.00), ("blueprint", 1.35, 2.15), ("river", 2.35, 3.30)]
    ck = Cekim("1.09", sure=4.0, kelimeler=kw, duygu=Duygu("merak").gecis("gerilim", t0=2.35, sure=0.75), arka="#121820")
    sp_u = _sp_layer(set_109_taslak_masasi, ["uzak"])
    sp_o = _sp_layer(set_109_taslak_masasi, ["orta"])
    sp_s = _sp_layer(set_109_taslak_masasi, ["sahne"])
    sp_p = _sp_layer(set_109_taslak_masasi, ["plan"])
    sp_f = _sp_layer(set_109_taslak_masasi, ["onplan"])

    def ciz_fx(c, t, o):
        _damga(c, "FOX RIVER", 0, -325, clamp((t - 2.35) / 0.30), PLAN_C, boyut=42)

    ck.ekle(
        Oge("uzak", _draw_2x(sp_u), derinlik=0.45),
        Oge("orta", _draw_2x(sp_o), derinlik=0.75),
        Oge("masa_turna", _draw_2x(sp_s), derinlik=1.0),
        Oge("plan", _draw_scan_2x(sp_p, ck.k("blueprint"), 0.80), derinlik=1.08),
        Oge("onplan", _draw_2x(sp_f), derinlik=1.22),
        Oge("fx_109", ciz_fx, derinlik=1.26),
    )
    ck.kamera = Kamera(
        x=Iz([(0, W/2 - 50), (4.0, W/2 + 20, "io")]),
        z=Iz([(0, 1.04), (4.0, 1.26, "in")]),
    )
    ck.ust.append(_hud("1.09", "Your firm renovates a prison. On your desk lies one blueprint: Fox River.",
                       lambda t: "river" if t >= 2.35 else ("blueprint" if t >= 1.35 else ("prison" if t >= 0.30 else ""))))
    return ck

# ───────── 1.10 · Death Row Front Page (THE CHICAGO CHRONICLE · DEATH ROW + Lincoln v1)
def build_110():
    kw = [("change", 0.30, 1.10), ("death", 1.65, 2.75)]
    ck = Cekim("1.10", sure=3.8, kelimeler=kw, duygu=Duygu("gerilim").gecis("ofke", t0=1.65, sure=0.55), arka="#0A1018")
    sp_u = _sp_layer(set_110_idam_manset, ["uzak"])
    sp_o = _sp_layer(set_110_idam_manset, ["orta"])
    sp_s = _sp_layer(set_110_idam_manset, ["sahne"])
    sp_p = _sp_layer(set_110_idam_manset, ["plan"])
    sp_f = _sp_layer(set_110_idam_manset, ["onplan"])

    def ciz_flash(c, t, o):
        if 1.62 <= t <= 1.92:
            fl = 1.0 - (t - 1.62) / 0.30
            c.drawRect(skia.Rect(-W, -H, W, H), paint(KIRMIZI, 0.45 * fl))

    ck.ekle(
        Oge("uzak", _draw_2x(sp_u), derinlik=0.45),
        Oge("orta", _draw_2x(sp_o), derinlik=0.75),
        Oge("idam_manset", _draw_2x(sp_s), derinlik=1.0, giris=("dus", ck.k("death", -0.25), 0.32)),
        Oge("plan", _draw_scan_2x(sp_p, ck.k("death"), 0.50), derinlik=1.08),
        Oge("onplan", _draw_2x(sp_f), derinlik=1.22),
        Oge("fx_110", ciz_flash, derinlik=1.30),
    )
    ck.kamera = Kamera(
        z=Iz([(0, 1.04), (1.65, 1.10, "out"), (3.8, 1.24, "in")]),
        sarsinti=[(1.68, 0.34, 24)],
    )
    ck.ust.append(_hud("1.10", "You don't know it yet, but that plan will change your life. Your brother is on Death Row.",
                       lambda t: "death" if t >= 1.65 else ("change" if t >= 0.30 else "")))
    return ck

def build_film():
    c = [build_101(), build_102(), build_103(), build_104(), build_105(),
         build_106(), build_107(), build_108(), build_109(), build_110()]
    return Film([
        c[0], OnPlanSil(ciz_kapi_sil, sure=0.55),
        c[1], Maske("mutfak_pencere", boyut=(440, 320), sure=0.65),
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
        ("1.01 · Family Door (SCOFIELD)",  bas[0] + 2.75),
        ("1.02 · Rainy Kitchen (AGE 11)",  bas[1] + 3.10),
        ("TRANS · Window Mask",            bas[2] + 0.32),
        ("1.03 · Juvenile Hall & LOCKED",  bas[2] + 2.85),
        ("1.04 · Low Latent Inhibition",   bas[3] + 3.20),
        ("TRANS · Crack → Sunbeam",        bas[4] + 0.32),
        ("1.05 · Morning Crane (I'M HERE)",bas[4] + 3.00),
        ("TRANS · Crane Flight",           bas[5] + 0.40),
        ("1.06 · High School Origami",     bas[5] + 2.75),
        ("1.07 · Night Diner ($90,000)",   bas[6] + 3.05),
        ("TRANS · Check → Diploma",        bas[7] + 0.38),
        ("1.08 · Chicago CAD Skyline",     bas[7] + 2.65),
        ("1.09 · Fox River Blueprint",     bas[8] + 2.95),
        ("TRANS · Crane Zoom",             bas[9] + 0.30),
        ("1.10 · DEATH ROW Impact",        bas[9] + 2.35),
        ("1.10 · Act I Cliffhanger",       bas[9] + 3.35),
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
    draw.text((pad, 14), f"ACT I ('THE CRANE') F4b v3 ENGLISH — 5-LAYER PARALLAX SETS (960 px) · {film.sure:.1f}s · 9/9 Semantic", fill=(127, 230, 255), font=ft)
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
    print(f"Act I v3 EN kuruldu: {len(film.cekimler)} çekim, toplam {film.sure:.2f} sn", flush=True)
    kareler = P / "kareler_b1_v3"
    kontakt_png = P / "bolum1_v3_en_kontakt_960.png"
    kontakt_olustur(film, kareler, kontakt_png)
    print("Kontakt Act I v3 EN tamam:", kontakt_png, flush=True)
    mp4 = P / "bolum1_v3_en_960.mp4"
    render_taslak_960(film, mp4, fps=16, crf=24)
    print("MP4 Act I v3 EN tamam:", mp4, flush=True)
