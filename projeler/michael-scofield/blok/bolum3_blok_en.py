"""Act III ('Fox River') F4b v2 EN — TRUE LIVE ANIMATED 2D ACTION (R18-HAREKET + R4-ANATOMI).

Imports 10 locked 5-layer + action-separated 960x540 scene sets from V7, V8, V9.
Real in-scene physical motion (NOT a slideshow):
  - 3.04: Toilet starts flush on wall -> Allen bolt physically spins out -> toilet slides left revealing pipes!
  - 3.06: High-voltage breaker lever physically lifts + corridor lights surge/dim -> red phone handset shakes & halts hand!
  - 3.08: Zero-overflow HUD + breathing golden doorway light beam.
  - 3.09: Brothers physically slide along steel cable with sparks + dual watchtower searchlights sweep + red alarms strobe!
  - 3.10: Plane physically climbs & shrinks into night sky + brothers sprint + sirens strobe + FBI desk lamp clicks ON!
"""
import math, os, sys
from pathlib import Path
import skia
from PIL import Image, ImageDraw, ImageFont

P = Path(__file__).resolve().parent
PROJE = P.parent
REPO = PROJE.parents[1]
sys.path[:0] = [str(REPO / "studyo/motor"), str(PROJE), str(PROJE / "kartlar"), str(REPO / "r3"), str(REPO / "r2")]

from sahne import W, H, Iz, ease, clamp, paint, svg_sprite, draw_sprite, Oge, Kamera, Cekim
from duygu import Duygu
from gecis import Film, ZoomIcinden, OnPlanSil, Eslesme, Maske, Savurma

from b3_set_ziyaret_revir import set_301_ziyaret_cami, set_302_ekip_kartlari, set_303_revir_sara
from b3_set_duvar_idam import set_304_duvar_civata, set_305_isyan_kanal, set_306_idam_telefon
from b3_set_yanik_kacis import (
    set_307_yanik_dovme, set_308_acik_kapi, set_309_kablo_kacisi, set_310_pist_insan_avi,
)

PLAN_C  = "#7FE6FF"
ALTIN   = "#F5C469"
KIRMIZI = "#E03E3E"
BEYAZ   = "#EAF2F8"


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


def font(ad, boyut):
    return skia.Font(TF_BOLD if "Bold" in ad else TF_REG, float(boyut))


def _sp_layer(fn, katmanlar, **kwargs):
    defs, body = fn(katmanlar=katmanlar, **kwargs)
    return svg_sprite(body, 960, 540, defs=f"<defs>{defs}</defs>")


def _draw_2x(sp):
    return lambda c, t, o: (c.save(), c.scale(2.02, 2.02), draw_sprite(c, sp), c.restore())


def _draw_scan_2x(sp, t0, sure=0.65, vertical=False):
    def _ciz(c, t, o):
        p = ease("out", clamp((t - t0) / sure))
        if p <= 0.005:
            return
        c.save()
        if vertical:
            sy = -H / 2 + H * p
            c.clipRect(skia.Rect(-W / 2, -H / 2, W / 2, sy))
            c.scale(2.02, 2.02); draw_sprite(c, sp)
            c.restore()
            if p < 0.98:
                c.drawLine(-W / 2, sy, W / 2, sy, paint("#FFFFFF", 0.95, Style=skia.Paint.kStroke_Style, StrokeWidth=4))
                c.drawLine(-W / 2, sy, W / 2, sy, paint(PLAN_C, 0.50, Style=skia.Paint.kStroke_Style, StrokeWidth=14))
        else:
            sx = -W / 2 + W * p
            c.clipRect(skia.Rect(-W / 2, -H / 2, sx, H / 2))
            c.scale(2.02, 2.02); draw_sprite(c, sp)
            c.restore()
            if p < 0.98:
                c.drawLine(sx, -H / 2, sx, H / 2, paint("#FFFFFF", 0.95, Style=skia.Paint.kStroke_Style, StrokeWidth=4))
                c.drawLine(sx, -H / 2, sx, H / 2, paint(PLAN_C, 0.50, Style=skia.Paint.kStroke_Style, StrokeWidth=14))
    return _ciz


def _damga(c, metin, x, y, p, renk=PLAN_C, boyut=40):
    if p <= 0.01:
        return
    ep = ease("out", clamp(p))
    sc = 1.30 - 0.30 * ep
    c.save()
    c.translate(x, y); c.scale(sc, sc)
    f = font("AlegreyaSC-Bold", boyut)
    w = f.measureText(metin)
    pad_x, pad_y = 22, 12
    box = skia.Rect(-w / 2 - pad_x, -boyut * 0.72 - pad_y, w / 2 + pad_x, pad_y + 6)
    c.drawRect(box, paint("#070C14", 0.86 * ep))
    c.drawRect(box, paint(renk, 0.95 * ep, Style=skia.Paint.kStroke_Style, StrokeWidth=3))
    c.drawString(metin, -w / 2, 0, f, paint(renk, ep))
    c.restore()


def _hud(cid, altyazi, aktif_fn):
    def _ciz(c, t):
        c.drawRect(skia.Rect(0, H - 72, W, H), paint("#060A12", 0.78))
        c.drawLine(0, H - 72, W, H - 72, paint(PLAN_C, 0.28, Style=skia.Paint.kStroke_Style, StrokeWidth=1.5))
        f_id = font("AlegreyaSC-Bold", 20)
        f_tx = font("Alegreya", 25)
        c.drawString(cid, 32, H - 28, f_id, paint(PLAN_C, 0.95))
        tw = f_tx.measureText(altyazi)
        c.drawString(altyazi, (W - tw) / 2, H - 27, f_tx, paint(BEYAZ, 0.96))
        kw = aktif_fn(t)
        if kw:
            f_kw = font("AlegreyaSC-Bold", 19)
            tag = f"<<{kw.upper()}>>"
            c.drawString(tag, W - f_kw.measureText(tag) - 32, H - 28, f_kw, paint(ALTIN, 0.95))
    return _ciz


# --------- 3.01 Visiting Glass (GETTING YOU OUT / DAYS LEFT: 29)
def build_301():
    kw = [("glass", 0.25, 1.05), ("shirt", 1.55, 2.35), ("glows", 2.65, 3.85)]
    ck = Cekim("3.01", sure=4.6, kelimeler=kw, duygu=Duygu("merak").gecis("gerilim", t0=2.65, sure=0.8), arka="#0A101A")
    sp_u = _sp_layer(set_301_ziyaret_cami, ["uzak"])
    sp_main = _sp_layer(set_301_ziyaret_cami, ["orta", "sahne", "onplan"])
    sp_p = _sp_layer(set_301_ziyaret_cami, ["plan"])

    def ciz_fx(c, t, o):
        # live fluorescent flicker + cyan blueprint glow pulse on Michael's chest at 'glows'
        fl = 0.04 * (0.5 + 0.5 * math.sin(t * 28.0))
        c.drawRect(skia.Rect(-W / 2, -H / 2, W / 2, H / 2), paint("#B8E6FF", fl))
        if t >= 2.55:
            gp = ease("out", clamp((t - 2.55) / 0.45))
            pulse = 0.22 + 0.12 * math.sin(t * 10.0)
            c.drawCircle(-620, 80, 125, paint(PLAN_C, pulse * gp))

    ck.ekle(
        Oge("uzak", _draw_2x(sp_u), derinlik=0.65),
        Oge("sahne", _draw_2x(sp_main), derinlik=1.0),
        Oge("plan", _draw_scan_2x(sp_p, ck.k("glows", -0.15), 0.70), derinlik=1.0),
        Oge("fx_301", ciz_fx, derinlik=1.0),
        Oge("cam_el", lambda c, t, o: None, x=W / 2 + 120, y=H / 2 - 40, derinlik=1.0),
    )
    ck.kamera = Kamera(
        x=Iz([(0, W / 2 + 16), (4.6, W / 2 + 12, "io")]),
        y=Iz([(0, H / 2 - 10), (4.6, H / 2 - 14, "io")]),
        z=Iz([(0, 1.01), (4.6, 1.05, "in")]),
    )
    ck.ust.append(_hud("3.01", "At the visiting glass, you open your shirt. The blueprint glows: I'm getting you out.",
                       lambda t: "glows" if t >= 2.65 else ("shirt" if t >= 1.55 else ("glass" if t >= 0.25 else ""))))
    return ck


# --------- 3.02 Yard Crew Cards (Abruzzi / Sucre / Westmoreland - LONG STORY.)
def build_302():
    kw = [("mob", 0.55, 1.35), ("cellmate", 1.65, 2.35), ("cooper", 2.65, 3.35), ("story", 3.65, 4.55)]
    ck = Cekim("3.02", sure=5.0, kelimeler=kw, duygu=Duygu("merak"), arka="#14181E")
    sp_u = _sp_layer(set_302_ekip_kartlari, ["uzak"])
    sp_main = _sp_layer(set_302_ekip_kartlari, ["orta", "sahne", "onplan"])
    sp_p = _sp_layer(set_302_ekip_kartlari, ["plan"])

    def ciz_fx(c, t, o):
        for cx, ct in ((-520, 0.55), (0, 1.65), (520, 2.65)):
            if ct <= t <= ct + 0.35:
                a = 0.32 * (1.0 - (t - ct) / 0.35)
                c.drawRect(skia.Rect(cx - 210, -180, cx + 210, 260), paint(PLAN_C, a, Style=skia.Paint.kStroke_Style, StrokeWidth=5))

    ck.ekle(
        Oge("uzak", _draw_2x(sp_u), derinlik=0.65),
        Oge("sahne", _draw_2x(sp_main), derinlik=1.0),
        Oge("plan", _draw_scan_2x(sp_p, ck.k("mob"), 1.80), derinlik=1.0),
        Oge("fx_302", ciz_fx, derinlik=1.0),
    )
    ck.kamera = Kamera(
        x=Iz([(0, W / 2 - 140), (1.7, W / 2, "io"), (3.5, W / 2 + 120, "io"), (5.0, W / 2 + 60, "out")]),
        z=Iz([(0, 1.08), (3.5, 1.14, "io"), (5.0, 1.10, "out")]),
        sarsinti=[(0.55, 0.14, 10), (1.65, 0.14, 10), (2.65, 0.14, 10), (3.65, 0.18, 14)],
    )
    ck.ust.append(_hud("3.02", "You need a crew: a mob boss, a cellmate, and D.B. Cooper. Long story.",
                       lambda t: "story" if t >= 3.65 else ("cooper" if t >= 2.65 else ("cellmate" if t >= 1.65 else ("mob" if t >= 0.55 else "")))))
    return ck


# --------- 3.03 Warm Infirmary & Sara (DAYS LEFT: 21)
def build_303():
    kw = [("infirmary", 0.45, 1.35), ("day", 1.75, 2.55), ("sara", 3.05, 4.15)]
    ck = Cekim("3.03", sure=4.8, kelimeler=kw, duygu=Duygu("merak").gecis("huzur", t0=3.05, sure=0.9), arka="#1B140E")
    sp_u = _sp_layer(set_303_revir_sara, ["uzak"])
    sp_main = _sp_layer(set_303_revir_sara, ["orta", "sahne", "onplan"])
    sp_p = _sp_layer(set_303_revir_sara, ["plan"])

    def ciz_fx(c, t, o):
        for i in range(16):
            mx = -760 + ((i * 113 + t * 28) % 1520)
            my = -360 + ((i * 79 - t * 20) % 680)
            c.drawCircle(mx, my, 3.0, paint(ALTIN, 0.30 + 0.16 * math.sin(t * 2.8 + i)))
        _damga(c, "INFIRMARY · EXIT", 360, -340, clamp((t - 1.75) / 0.35), PLAN_C, boyut=32)

    ck.ekle(
        Oge("uzak", _draw_2x(sp_u), derinlik=0.65),
        Oge("sahne", _draw_2x(sp_main), derinlik=1.0),
        Oge("plan", _draw_scan_2x(sp_p, ck.k("day", -0.15), 0.70), derinlik=1.0),
        Oge("fx_303", ciz_fx, derinlik=1.0),
        Oge("revir_pencere", lambda c, t, o: None, x=W / 2 + 430, y=H / 2 - 120, derinlik=1.0),
    )
    ck.kamera = Kamera(
        x=Iz([(0, W / 2 - 40), (4.8, W / 2 + 30, "io")]),
        z=Iz([(0, 1.03), (4.8, 1.10, "in")]),
    )
    ck.ust.append(_hud("3.03", "You fake diabetes to visit the infirmary every day. That's where you meet Sara.",
                       lambda t: "sara" if t >= 3.05 else ("day" if t >= 1.75 else ("infirmary" if t >= 0.45 else ""))))
    return ck


# --------- 3.04 Allen Bolt & Hidden Heart — TRUE R18-HAREKET LIVE ACTION!
# Toilet starts FLUSH on wall -> Allen bolt physically spins & pulls out -> Toilet slides LEFT revealing pipes!
def build_304():
    kw = [("bolt", 0.35, 1.45), ("wall", 1.75, 2.85), ("heart", 3.05, 4.25)]
    ck = Cekim("3.04", sure=4.8, kelimeler=kw, duygu=Duygu("gerilim"), arka="#0B111A")
    sp_u = _sp_layer(set_304_duvar_civata, ["uzak"])
    sp_o = _sp_layer(set_304_duvar_civata, ["orta"])
    sp_oyuk = _sp_layer(set_304_duvar_civata, ["duvar_oyuk"])
    # tuvalet_dx=0.0 => toilet sits FLUSH covering the wall breach; we slide it live in ciz_tuvalet!
    sp_tuvalet = _sp_layer(set_304_duvar_civata, ["tuvalet"], tuvalet_dx=0.0)
    sp_civata = _sp_layer(set_304_duvar_civata, ["civata"])
    sp_p = _sp_layer(set_304_duvar_civata, ["plan"])
    sp_f = _sp_layer(set_304_duvar_civata, ["onplan"])

    def ciz_tuvalet(c, t, o):
        # 0.0 -> 1.65s: toilet is bolted flush against the wall (dx=0)
        # 1.65 -> 2.95s ('wall'): toilet physically slides -295px (x2.02) to the left, exposing the pipe shaft!
        slide = ease("io", clamp((t - 1.65) / 1.25))
        dx = -295.0 * 2.02 * slide
        # slight heave rattle while sliding
        dy = math.sin(slide * math.pi * 6.0) * 4.5 * (1.0 - slide) if 0.01 < slide < 0.99 else 0.0
        c.save()
        c.translate(dx, dy)
        c.scale(2.02, 2.02)
        draw_sprite(c, sp_tuvalet)
        c.restore()
        # concrete dust puffs during the slide
        if 0.05 < slide < 0.95:
            for k in range(6):
                px = 180 - slide * 280 + k * 28
                py = 240 - slide * 60 + math.sin(k * 2.1 + t * 8) * 24
                c.drawCircle(px, py, 16 + 18 * slide, paint("#9BA8B5", 0.28 * (1.0 - slide)))

    def ciz_civata(c, t, o):
        # 0.35 -> 1.60s ('bolt'): Allen bolt visibly spins & backs out toward foreground!
        spin_p = ease("io", clamp((t - 0.35) / 1.25))
        # pivot near bolt head in centered 1920x1080 space (~ -220, +135)
        bx, by = -205.0, 140.0
        ang = spin_p * 540.0  # 1.5 full turns unscrewing!
        pull_x = 18.0 * spin_p
        pull_y = 26.0 * spin_p
        sc = 0.85 + 0.22 * spin_p
        c.save()
        c.translate(bx + pull_x, by + pull_y)
        c.rotate(ang)
        c.scale(sc, sc)
        c.translate(-bx, -by)
        c.scale(2.02, 2.02)
        draw_sprite(c, sp_civata)
        c.restore()
        if 0.35 <= t <= 1.60:
            c.drawCircle(bx + pull_x, by + pull_y, 38 + 38 * spin_p,
                         paint(PLAN_C, 0.50 * (1.0 - spin_p), Style=skia.Paint.kStroke_Style, StrokeWidth=3))

    def ciz_fx(c, t, o):
        _damga(c, "HIDDEN HEART", -440, -340, clamp((t - 3.05) / 0.32), PLAN_C, boyut=36)

    ck.ekle(
        Oge("uzak", _draw_2x(sp_u), derinlik=0.65),
        Oge("orta", _draw_2x(sp_o), derinlik=1.0),
        Oge("oyuk", _draw_2x(sp_oyuk), derinlik=1.0),
        Oge("tuvalet_anim", ciz_tuvalet, derinlik=1.0),
        Oge("civata_anim", ciz_civata, derinlik=1.0),
        Oge("plan", _draw_scan_2x(sp_p, ck.k("heart", -0.25), 0.75), derinlik=1.0),
        Oge("onplan", _draw_2x(sp_f), derinlik=1.0),
        Oge("fx_304", ciz_fx, derinlik=1.0),
        Oge("duvar_delik", lambda c, t, o: None, x=W / 2 + 190, y=H / 2 - 10, derinlik=1.0),
    )
    ck.kamera = Kamera(
        x=Iz([(0, W / 2 + 10), (2.2, W / 2 + 20, "io"), (4.8, W / 2 + 65, "in")]),
        z=Iz([(0, 1.02), (4.8, 1.12, "in")]),
        sarsinti=[(1.70, 0.30, 14)],
    )
    ck.ust.append(_hud("3.04", "One stolen bolt loosens the toilet. Behind your cell wall lies Fox River's hidden heart.",
                       lambda t: "heart" if t >= 3.05 else ("wall" if t >= 1.75 else ("bolt" if t >= 0.35 else ""))))
    return ck


# --------- 3.05 Riot Air Vent Rescue (R4-ANATOMI FIXED: Slim Michael + Sara BOTH arms!)
def build_305():
    kw = [("riot", 0.35, 1.45), ("vents", 1.85, 2.75), ("save", 3.05, 4.15)]
    ck = Cekim("3.05", sure=4.8, kelimeler=kw, duygu=Duygu("ofke").gecis("korku", t0=3.05, sure=0.75), arka="#1B0B06")
    sp_u = _sp_layer(set_305_isyan_kanal, ["uzak"])
    sp_main = _sp_layer(set_305_isyan_kanal, ["orta", "sahne", "onplan"])
    sp_p = _sp_layer(set_305_isyan_kanal, ["plan"])

    def ciz_fx(c, t, o):
        # pulsing orange riot firelight reflection + rising embers
        fire_p = 0.08 + 0.06 * math.sin(t * 13.0)
        c.drawRect(skia.Rect(-W / 2, -H / 2, W / 2, H / 2), paint("#FF6A2B", fire_p))
        for i in range(20):
            ex = -780 + ((i * 97 + int(t * 95)) % 1560)
            ey = 440 - ((i * 61 + t * 260) % 920)
            c.drawCircle(ex, ey, 3.8, paint("#FF9B42", 0.72))
        _damga(c, "104F · RIOT", -480, -340, clamp((t - 0.40) / 0.28), KIRMIZI, boyut=36)

    ck.ekle(
        Oge("uzak", _draw_2x(sp_u), derinlik=0.65),
        Oge("sahne", _draw_2x(sp_main), derinlik=1.0),
        Oge("plan", _draw_scan_2x(sp_p, ck.k("vents", -0.15), 0.65, vertical=True), derinlik=1.0),
        Oge("fx_305", ciz_fx, derinlik=1.0),
    )
    ck.kamera = Kamera(
        y=Iz([(0, H / 2 + 45), (4.8, H / 2 - 45, "io")]),
        z=Iz([(0, 1.03), (4.8, 1.10, "in")]),
        sarsinti=[(0.35, 0.35, 14), (3.05, 0.22, 10)],
    )
    ck.ust.append(_hud("3.05", "A prison riot erupts. You crawl through the vents to save Sara.",
                       lambda t: "save" if t >= 3.05 else ("vents" if t >= 1.85 else ("riot" if t >= 0.35 else ""))))
    return ck


def ciz_izgara_sil(c, u):
    c.drawRect(skia.Rect(-140, 0, 140, H), paint("#1E2836"))
    for gy in range(40, H, 54):
        c.drawRect(skia.Rect(-115, gy, 115, gy + 16), paint("#0C121B"))
    c.drawRect(skia.Rect(118, 0, 140, H), paint("#05080D", 0.9))


# --------- 3.06 Execution Night & Red Phone — TRUE R18-HAREKET LIVE LEVER + LIGHTING + PHONE!
def build_306():
    kw = [("fails", 0.85, 1.95), ("rings", 2.85, 3.95), ("stay", 4.15, 5.05)]
    ck = Cekim("3.06", sure=5.4, kelimeler=kw, duygu=Duygu("korku").gecis("umut", t0=2.85, sure=0.75), arka="#080D16")
    sp_u = _sp_layer(set_306_idam_telefon, ["uzak"])
    sp_base = _sp_layer(set_306_idam_telefon, ["orta", "sahne", "onplan"])
    sp_salter = _sp_layer(set_306_idam_telefon, ["salter_kol"])
    sp_ahize = _sp_layer(set_306_idam_telefon, ["telefon_ahize"])
    sp_p = _sp_layer(set_306_idam_telefon, ["plan"])

    def ciz_salter(c, t, o):
        # Lever & hand physically rise from lowered position (+38px) toward HIGH VOLTAGE ON (-24px),
        # then FREEZE & recoil cleanly at t=2.85s when the red court phone rings!
        if t < 2.85:
            pull = ease("io", clamp((t - 1.15) / 1.65))
            dy = 36.0 - 54.0 * pull
            trem = math.sin(t * 32.0) * 2.2 * pull
        else:
            recoil = ease("out", clamp((t - 2.85) / 0.35))
            dy = -18.0 + 26.0 * recoil  # halts and eases back off the switch!
            trem = 0.0
        c.save()
        c.translate(trem, dy)
        c.scale(2.02, 2.02)
        draw_sprite(c, sp_salter)
        c.restore()

    def ciz_ahize(c, t, o):
        # Red telephone handset physically rattles & bounces when the phone rings at t=2.85s!
        if t >= 2.85:
            ring_env = 0.5 + 0.5 * math.sin((t - 2.85) * 14.0)
            rx = math.sin(t * 58.0) * 6.5 * ring_env
            ry = -abs(math.sin(t * 42.0)) * 9.0 * ring_env
            ang = math.sin(t * 52.0) * 3.5 * ring_env
            px, py = -620.0, 175.0
            c.save()
            c.translate(px + rx, py + ry)
            c.rotate(ang)
            c.translate(-px, -py)
            c.scale(2.02, 2.02)
            draw_sprite(c, sp_ahize)
            c.restore()
        else:
            c.save(); c.scale(2.02, 2.02); draw_sprite(c, sp_ahize); c.restore()

    def ciz_fx(c, t, o):
        # Dynamic room lighting reacts to the lever + spark + red phone!
        if t < 2.85:
            # power strain dimming as the lever rises (1.15 -> 2.85s) + electric blue spark strobe on 'fails'
            strain = ease("in", clamp((t - 1.15) / 1.65))
            flicker = 0.14 * abs(math.sin(t * 34.0)) if 0.85 <= t <= 2.40 else 0.0
            c.drawRect(skia.Rect(-W / 2, -H / 2, W / 2, H / 2), paint("#030710", 0.34 * strain))
            if 0.85 <= t <= 2.40:
                c.drawRect(skia.Rect(-W / 2, -H / 2, W / 2, H / 2), paint(PLAN_C, flicker))
                c.drawCircle(-20, 310, 56 + 24 * abs(math.sin(t * 40.0)), paint(PLAN_C, 0.55 * (1.0 - (t - 0.85) / 1.55)))
        else:
            # Red phone ring shockwave + warm relief light surge across the cold corridor!
            rel = ease("out", clamp((t - 2.85) / 0.55))
            c.drawRect(skia.Rect(-W / 2, -H / 2, W / 2, H / 2), paint(ALTIN, 0.10 * rel))
            for k in range(3):
                p = ((t - 2.85) * 1.45 + k * 0.33) % 1.0
                c.drawCircle(-620, 210, 60 + 290 * p, paint(KIRMIZI, 0.78 * (1.0 - p), Style=skia.Paint.kStroke_Style, StrokeWidth=5))
            if t <= 3.12:
                c.drawRect(skia.Rect(-W / 2, -H / 2, W / 2, H / 2), paint("#FFFFFF", 0.34 * (1.0 - (t - 2.85) / 0.27)))

    ck.ekle(
        Oge("uzak", _draw_2x(sp_u), derinlik=0.65),
        Oge("sahne", _draw_2x(sp_base), derinlik=1.0),
        Oge("salter_anim", ciz_salter, derinlik=1.0),
        Oge("ahize_anim", ciz_ahize, derinlik=1.0),
        Oge("plan", _draw_scan_2x(sp_p, ck.k("rings", -0.05), 0.45), derinlik=1.0),
        Oge("fx_306", ciz_fx, derinlik=1.0),
        Oge("kivilcim", lambda c, t, o: None, x=W / 2 - 20, y=H / 2 + 310, derinlik=1.0),
    )
    ck.kamera = Kamera(
        x=Iz([(0, W / 2 + 12), (2.7, W / 2 + 20, "io"), (3.1, W / 2 + 8, "out"), (5.4, W / 2 + 4, "in")]),
        y=Iz([(0, H / 2 - 12), (5.4, H / 2 - 14, "io")]),
        z=Iz([(0, 1.01), (2.8, 1.05, "in"), (3.1, 1.03, "out"), (5.4, 1.04, "in")]),
        sarsinti=[(0.85, 0.22, 12), (2.85, 0.34, 24)],
    )
    ck.ust.append(_hud("3.06", "Execution night: your sabotage fails. Then the phone rings - a two-week stay.",
                       lambda t: "stay" if t >= 4.15 else ("rings" if t >= 2.85 else ("fails" if t >= 0.85 else ""))))
    return ck


# --------- 3.07 Scorched Tattoo & Rebuild (REBUILT / 3 DAYS LEFT)
def build_307():
    kw = [("burns", 0.35, 1.45), ("rebuild", 2.35, 3.95)]
    ck = Cekim("3.07", sure=4.8, kelimeler=kw, duygu=Duygu("korku").gecis("merak", t0=2.35, sure=0.8), arka="#0A0F18")
    sp_u = _sp_layer(set_307_yanik_dovme, ["uzak"])
    sp_main = _sp_layer(set_307_yanik_dovme, ["orta", "sahne", "onplan"])
    sp_p = _sp_layer(set_307_yanik_dovme, ["plan"])

    def ciz_fx(c, t, o):
        ep = 0.24 + 0.14 * math.sin(t * 9.0)
        c.drawCircle(-220, 40, 76, paint("#FF7A2F", ep * (1.0 - 0.5 * clamp((t - 2.35) / 0.8))))

    ck.ekle(
        Oge("uzak", _draw_2x(sp_u), derinlik=0.65),
        Oge("sahne", _draw_2x(sp_main), derinlik=1.0),
        Oge("plan", _draw_scan_2x(sp_p, ck.k("rebuild", -0.15), 0.70), derinlik=1.0),
        Oge("fx_307", ciz_fx, derinlik=1.0),
        Oge("yanik_kor", lambda c, t, o: None, x=W / 2 - 220, y=H / 2 + 40, derinlik=1.0),
        Oge("eksik_parca", lambda c, t, o: None, x=W / 2 + 310, y=H / 2 - 90, derinlik=1.0),
    )
    ck.kamera = Kamera(
        x=Iz([(0, W / 2 - 60), (2.2, W / 2 - 20, "io"), (4.8, W / 2 + 60, "in")]),
        z=Iz([(0, 1.04), (4.8, 1.14, "in")]),
    )
    ck.ust.append(_hud("3.07", "A scorched pipe burns away part of your tattoo. You rebuild the missing map.",
                       lambda t: "rebuild" if t >= 2.35 else ("burns" if t >= 0.35 else "")))
    return ck


# --------- 3.08 Unlocked Infirmary Door — Visual Echo 2 (ZERO OVERFLOW + BREATHING GOLDEN BEAM)
def build_308():
    kw = [("tonight", 0.25, 1.05), ("favor", 1.55, 2.45), ("unlocked", 2.85, 4.15)]
    ck = Cekim("3.08", sure=4.8, kelimeler=kw, duygu=Duygu("gerilim").gecis("umut", t0=2.85, sure=0.85), arka="#17110A")
    sp_u = _sp_layer(set_308_acik_kapi, ["uzak"])
    sp_o = _sp_layer(set_308_acik_kapi, ["orta"])
    sp_isik = _sp_layer(set_308_acik_kapi, ["kapi_isik"])
    sp_s = _sp_layer(set_308_acik_kapi, ["sahne", "onplan"])
    sp_p = _sp_layer(set_308_acik_kapi, ["plan"])

    def ciz_kapi_isik(c, t, o):
        # Golden doorway beam subtly swells & breathes as 'unlocked' hits
        boost = 0.65 + 0.35 * ease("out", clamp((t - 2.65) / 0.85)) + 0.08 * math.sin(t * 4.5)
        c.saveLayerAlpha(None, int(255 * clamp(boost)))
        c.scale(2.02, 2.02)
        draw_sprite(c, sp_isik)
        c.restore()

    def ciz_fx(c, t, o):
        for i in range(14):
            mx = -480 + ((i * 53 + t * 20) % 360)
            my = -260 + ((i * 71 - t * 24) % 580)
            c.drawCircle(mx, my, 3.2, paint(ALTIN, 0.38 + 0.16 * math.sin(t * 3.0 + i)))

    ck.ekle(
        Oge("uzak", _draw_2x(sp_u), derinlik=0.65),
        Oge("orta", _draw_2x(sp_o), derinlik=1.0),
        Oge("kapi_isik_anim", ciz_kapi_isik, derinlik=1.0),
        Oge("sahne", _draw_2x(sp_s), derinlik=1.0),
        Oge("plan", _draw_scan_2x(sp_p, ck.k("unlocked", -0.20), 0.65), derinlik=1.0),
        Oge("fx_308", ciz_fx, derinlik=1.0),
        Oge("revir_kapisi", lambda c, t, o: None, x=W / 2 - 360, y=H / 2 + 20, derinlik=1.0),
    )
    ck.kamera = Kamera(
        x=Iz([(0, W / 2 + 16), (4.8, W / 2 + 6, "io")]),
        y=Iz([(0, H / 2 - 12), (4.8, H / 2 - 14, "io")]),
        z=Iz([(0, 1.01), (4.8, 1.04, "in")]),
    )
    ck.ust.append(_hud("3.08", "Tonight is the night. You ask Sara for one favor: leave the door unlocked.",
                       lambda t: "unlocked" if t >= 2.85 else ("favor" if t >= 1.55 else ("tonight" if t >= 0.25 else ""))))
    return ck


# --------- 3.09 Night Escape Cable — TRUE R18-HAREKET SLIDING ESCAPEES + SWEEPING BEAMS + ALARMS!
def build_309():
    kw = [("cable", 0.35, 1.35), ("spotlights", 1.75, 2.85), ("wall", 3.25, 4.45)]
    ck = Cekim("3.09", sure=5.0, kelimeler=kw, duygu=Duygu("gerilim").gecis("zafer", t0=3.25, sure=0.75), arka="#070B13")
    sp_u = _sp_layer(set_309_kablo_kacisi, ["uzak"])
    sp_o = _sp_layer(set_309_kablo_kacisi, ["orta"])
    sp_alarm = _sp_layer(set_309_kablo_kacisi, ["alarm"])
    sp_p1 = _sp_layer(set_309_kablo_kacisi, ["projektor_1"])
    sp_p2 = _sp_layer(set_309_kablo_kacisi, ["projektor_2"])
    sp_s = _sp_layer(set_309_kablo_kacisi, ["sahne"])
    sp_kac = _sp_layer(set_309_kablo_kacisi, ["kacanlar"])
    sp_p = _sp_layer(set_309_kablo_kacisi, ["plan"])
    sp_f = _sp_layer(set_309_kablo_kacisi, ["onplan"])

    def ciz_alarm(c, t, o):
        # Flashing crimson watchtower alarm beacons!
        a = 0.22 + 0.78 * (0.5 + 0.5 * math.sin(t * 13.0))
        c.saveLayerAlpha(None, int(255 * clamp(a)))
        c.scale(2.02, 2.02); draw_sprite(c, sp_alarm)
        c.restore()

    def ciz_projektorler(c, t, o):
        # Sweeping dual watchtower searchlight cones around their exact tower pivots!
        # Left pivot (274, 156) in 960x540 -> (-206*2.02, -114*2.02) in centered 1920x1080
        p1x, p1y = (274 - 480) * 2.02, (156 - 270) * 2.02
        ang1 = math.sin(t * 2.4) * 14.0
        c.save()
        c.translate(p1x, p1y); c.rotate(ang1); c.translate(-p1x, -p1y)
        c.scale(2.02, 2.02); draw_sprite(c, sp_p1)
        c.restore()
        # Right pivot (818, 138) in 960x540 -> (+338*2.02, -132*2.02)
        p2x, p2y = (818 - 480) * 2.02, (138 - 270) * 2.02
        ang2 = math.sin(t * 2.9 + 1.4) * 15.0
        c.save()
        c.translate(p2x, p2y); c.rotate(ang2); c.translate(-p2x, -p2y)
        c.scale(2.02, 2.02); draw_sprite(c, sp_p2)
        c.restore()

    def ciz_kacanlar(c, t, o):
        # Michael & Lincoln PHYSICALLY SLIDE down the steel cable (from upper-left to lower-right wall)!
        # Cable slope: (136,154) -> (812,338) => ratio dy/dx = 184/676 = 0.272
        prog = ease("io", clamp((t - 0.25) / 4.25))
        dx = (-240.0 + 460.0 * prog)  # screen-space slide along cable!
        dy = dx * 0.272 + math.sin(t * 14.0) * 3.5  # subtle cable bounce vibration
        c.save()
        c.translate(dx, dy)
        c.scale(2.02, 2.02)
        draw_sprite(c, sp_kac)
        c.restore()
        # Live trailing friction sparks shooting off behind their hands!
        for k in range(5):
            sp_t = ((t * 4.5 + k * 0.2) % 1.0)
            sx = -180 + dx - sp_t * 65 + (k - 2) * 8
            sy = -15 + dy - sp_t * 26 + sp_t * sp_t * 32
            c.drawCircle(sx, sy, 3.5 * (1.0 - sp_t), paint(ALTIN, 0.9 * (1.0 - sp_t)))

    def ciz_fx(c, t, o):
        # Storm rain streaks + occasional lightning flash
        for i in range(34):
            rx = -920 + ((i * 73 + int(t * 165)) % 1840)
            ry = -500 + ((i * 89 + t * 680) % 1000)
            c.drawLine(rx, ry, rx - 12, ry + 36, paint("#A8D4F5", 0.34, Style=skia.Paint.kStroke_Style, StrokeWidth=2))
        if 1.95 <= t <= 2.12 or 3.30 <= t <= 3.44:
            c.drawRect(skia.Rect(-W / 2, -H / 2, W / 2, H / 2), paint("#DFF4FF", 0.22))

    ck.ekle(
        Oge("uzak", _draw_2x(sp_u), derinlik=0.65),
        Oge("orta", _draw_2x(sp_o), derinlik=1.0),
        Oge("alarm_anim", ciz_alarm, derinlik=1.0),
        Oge("projektor_anim", ciz_projektorler, derinlik=1.0),
        Oge("sahne", _draw_2x(sp_s), derinlik=1.0),
        Oge("kacanlar_anim", ciz_kacanlar, derinlik=1.0),
        Oge("plan", _draw_scan_2x(sp_p, ck.k("wall", -0.25), 0.70), derinlik=1.0),
        Oge("onplan", _draw_2x(sp_f), derinlik=1.0),
        Oge("fx_309", ciz_fx, derinlik=1.0),
    )
    ck.kamera = Kamera(
        x=Iz([(0, W / 2 - 55), (5.0, W / 2 + 55, "io")]),
        z=Iz([(0, 1.04), (5.0, 1.09, "in")]),
        sarsinti=[(1.75, 0.22, 10), (3.25, 0.28, 16)],
    )
    ck.ust.append(_hud("3.09", "You cross a steel cable under sweeping spotlights. You make it over the wall.",
                       lambda t: "wall" if t >= 3.25 else ("spotlights" if t >= 1.75 else ("cable" if t >= 0.35 else ""))))
    return ck


# --------- 3.10 Airstrip & Manhunt — TRUE R18-HAREKET TAKEOFF + SPRINT + SIRENS + FBI LAMP CLICK!
def build_310():
    kw = [("late", 0.35, 1.15), ("plane", 1.55, 2.45), ("manhunt", 2.95, 4.15)]
    ck = Cekim("3.10", sure=4.6, kelimeler=kw, duygu=Duygu("zafer").gecis("korku", t0=2.95, sure=0.70), arka="#080B14")
    sp_u = _sp_layer(set_310_pist_insan_avi, ["uzak"])
    sp_ucak = _sp_layer(set_310_pist_insan_avi, ["ucak"])
    sp_o = _sp_layer(set_310_pist_insan_avi, ["orta"])
    sp_s = _sp_layer(set_310_pist_insan_avi, ["sahne"])
    sp_kos = _sp_layer(set_310_pist_insan_avi, ["kosucular"])
    sp_p = _sp_layer(set_310_pist_insan_avi, ["plan"])
    sp_fbi = _sp_layer(set_310_pist_insan_avi, ["fbi_kutu"])
    sp_f = _sp_layer(set_310_pist_insan_avi, ["onplan"])

    def ciz_ucak(c, t, o):
        # Twin-engine plane PHYSICALLY climbs up & right while shrinking into the night sky!
        p = ease("in", clamp(t / 4.2))
        px, py = -120.0 + 230.0 * p, -160.0 - 140.0 * p
        sc = 1.24 - 0.56 * p
        c.save()
        c.translate(px, py)
        c.scale(sc, sc)
        c.translate(120.0, 160.0)
        c.scale(2.02, 2.02)
        draw_sprite(c, sp_ucak)
        c.restore()
        # Blinking aircraft tail/wing strobe
        if math.sin(t * 18.0) > 0.35:
            c.drawCircle(px + 25, py - 8, 7 * sc, paint("#FF4A4A", 0.85))

    def ciz_kosucular(c, t, o):
        # Brothers PHYSICALLY sprint down the wet runway with animated stride bounce & forward advance!
        p = ease("out", clamp(t / 4.4))
        stride_y = -abs(math.sin(t * 11.5)) * 12.0
        adv_x = -26.0 + 42.0 * p
        adv_y = 22.0 - 34.0 * p
        sc = 1.04 - 0.08 * p
        c.save()
        c.translate(adv_x, adv_y + stride_y)
        c.scale(sc, sc)
        c.scale(2.02, 2.02)
        draw_sprite(c, sp_kos)
        c.restore()

    def ciz_fbi(c, t, o):
        # Act IV Open Loop: FBI desk lamp PHYSICALLY clicks ON at 'manhunt' (t=2.90s)!
        if t < 2.88:
            return
        ep = ease("out", clamp((t - 2.88) / 0.28))
        c.saveLayerAlpha(None, int(255 * ep))
        c.scale(2.02, 2.02)
        draw_sprite(c, sp_fbi)
        c.restore()
        if t <= 3.16:
            c.drawRect(skia.Rect(240, -490, 910, -110), paint("#FFF5D6", 0.52 * (1.0 - (t - 2.88) / 0.28)))

    def ciz_fx(c, t, o):
        # Alternating red/blue police siren strobes sweeping across the wet runway!
        s_red = 0.22 * (0.5 + 0.5 * math.sin(t * 16.0))
        s_blu = 0.22 * (0.5 - 0.5 * math.sin(t * 16.0))
        c.drawCircle(-560, 200, 340, paint(KIRMIZI, s_red))
        c.drawCircle(-340, 220, 340, paint("#3B82F6", s_blu))

    ck.ekle(
        Oge("uzak", _draw_2x(sp_u), derinlik=0.65),
        Oge("ucak_anim", ciz_ucak, derinlik=0.80),
        Oge("orta", _draw_2x(sp_o), derinlik=1.0),
        Oge("sahne", _draw_2x(sp_s), derinlik=1.0),
        Oge("kosucular_anim", ciz_kosucular, derinlik=1.0),
        Oge("plan", _draw_scan_2x(sp_p, ck.k("manhunt", -0.10), 0.48), derinlik=1.0),
        Oge("fbi_anim", ciz_fbi, derinlik=1.0),
        Oge("onplan", _draw_2x(sp_f), derinlik=1.0),
        Oge("fx_310", ciz_fx, derinlik=1.0),
    )
    ck.kamera = Kamera(
        x=Iz([(0, W / 2 - 25), (2.8, W / 2, "io"), (4.6, W / 2 + 25, "in")]),
        y=Iz([(0, H / 2 + 12), (4.6, H / 2 - 14, "io")]),
        z=Iz([(0, 1.02), (4.6, 1.07, "in")]),
        sarsinti=[(2.90, 0.24, 14)],
    )
    ck.ust.append(_hud("3.10", "You reach the airstrip seconds too late. The plane takes off - now the manhunt begins.",
                       lambda t: "manhunt" if t >= 2.95 else ("plane" if t >= 1.55 else ("late" if t >= 0.35 else ""))))
    return ck


def build_film():
    c = [
        build_301(), build_302(), build_303(), build_304(), build_305(),
        build_306(), build_307(), build_308(), build_309(), build_310(),
    ]
    return Film([
        c[0], ZoomIcinden("cam_el", sure=0.55, renk=PLAN_C),
        c[1], Savurma(yon=1, sure=0.45),
        c[2], Maske("revir_pencere", boyut=(340, 220), sure=0.65),
        c[3], ZoomIcinden("duvar_delik", sure=0.55, renk=PLAN_C),
        c[4], OnPlanSil(ciz_izgara_sil, sure=0.55),
        c[5], Eslesme("kivilcim", "yanik_kor", sure=0.60),
        c[6], ZoomIcinden("eksik_parca", sure=0.55, renk=PLAN_C),
        c[7], Maske("revir_kapisi", boyut=(220, 460), sure=0.65),
        c[8], Savurma(yon=1, sure=0.45),
        c[9],
    ])


def kontakt_olustur(film, kare_klasor, out_png):
    bas = film.bas
    anlar = [
        ("3.01 Visiting Glass (29d)",        bas[0] + 3.25),
        ("3.02 Crew (Abruzzi/Sucre/West.)",  bas[1] + 4.10),
        ("3.03 Warm Infirmary & Sara",       bas[2] + 3.35),
        ("3.04a Toilet SEALED + Bolt Spin",  bas[3] + 1.00),
        ("3.04b Toilet SLIDES OPEN -> Pipes",bas[3] + 3.55),
        ("3.05 Riot Rescue (Slim + 2 Arms)", bas[4] + 3.35),
        ("3.06a Lever Rising + Spark Surge", bas[5] + 2.15),
        ("3.06b Phone Rings -> +14 DAYS",    bas[5] + 3.65),
        ("3.07 Scorched Tattoo Rebuild",     bas[6] + 3.25),
        ("3.08 Unlocked Door (0 Overflow)",  bas[7] + 3.35),
        ("3.09 Escape Cable (Live Slide)",   bas[8] + 3.45),
        ("3.10 Airstrip + FBI Lamp Click",   bas[9] + 3.60),
    ]
    pngler = film.onizle([t for _, t in anlar], str(kare_klasor), olcek=0.5)
    cols, rows, tw, th, pad, top = 4, 3, 440, 248, 14, 54
    sheet = Image.new("RGB", (cols * tw + (cols + 1) * pad, top + rows * (th + 26) + pad), (10, 14, 22))
    draw = ImageDraw.Draw(sheet)
    ft = ImageFont.truetype(str(REPO / "fonts/AlegreyaSC-Bold.ttf"), 21)
    fl = ImageFont.truetype(str(REPO / "fonts/Alegreya.ttf"), 15)
    draw.text((pad, 14), f"ACT III ('FOX RIVER') F4b v2 EN - LIVE ACTION (R18-HAREKET) · {film.sure:.1f}s · 9/9 Semantic", fill=(127, 230, 255), font=ft)
    for i, ((etiket, t), p) in enumerate(zip(anlar, pngler)):
        r, c = divmod(i, cols); x, y = pad + c * (tw + pad), top + r * (th + 26)
        sheet.paste(Image.open(p).convert("RGB").resize((tw, th), Image.Resampling.LANCZOS), (x, y))
        draw.rectangle([x, y, x + tw, y + th], outline=(55, 85, 110), width=2)
        draw.text((x + 4, y + th + 4), f"{etiket} ({t:.1f}s)", fill=(220, 230, 240), font=fl)
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
        if f % 80 == 0:
            print(f"  kare {f}/{n}...", flush=True)
    proc.stdin.close()
    if proc.wait() != 0:
        raise RuntimeError("ffmpeg hata verdi")
    os.replace(tmp, yol)
    return yol


if __name__ == "__main__":
    film = build_film()
    print(f"Act III v2 EN kuruldu: {len(film.cekimler)} cekim, toplam {film.sure:.2f} sn", flush=True)
    kontakt_png = P / "bolum3_en_kontakt_960.png"
    kontakt_olustur(film, P / "kareler_b3_en", kontakt_png)
    print("Kontakt Act III v2 EN tamam:", kontakt_png, flush=True)
    mp4 = P / "bolum3_en_960.mp4"
    render_taslak_960(film, mp4, fps=16, crf=24)
    print("MP4 Act III v2 EN tamam:", mp4, flush=True)
