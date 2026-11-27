"""F4b Act II ("Wearing the Map") Block Animatic — 100% ENGLISH, 5-Layer Parallax Sets (V4·V5·V6).

- Uses all 7 Görsel Kurul 3/3-approved 5-layer illustrated sets (b2_set_mahkeme, b2_set_plan_dovme, b2_set_banka_kapi).
- True 5-layer depth parallax + live CAD laser scanline reveals on keywords + 6/6 semantic transitions.
- 100% English narration HUD, kinetic stamps, and diegetic text (EXECUTION IN 30 DAYS synced with Act I MAY 11).

Outputs:
  - blok/bolum2_en_kontakt_960.png  (12-frame contact sheet: 7 shots + 5 key transitions)
  - blok/bolum2_en_960.mp4          (960×540, 16 fps fast draft)
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
from gecis import Film, ZoomIcinden, OnPlanSil, Eslesme, Maske, Savurma
from kartlar.b2_set_mahkeme import set_201_mahkeme, set_202_mektup
from kartlar.b2_set_plan_dovme import set_203_plan_duvari, set_204_dovme_studyosu
from kartlar.b2_set_banka_kapi import set_205_banka, set_206_dosya_94941, set_207_fox_kapilar

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

def _sp_layer(fn, katmanlar, ss=1.0):
    defs, body = fn(katmanlar=katmanlar)
    return svg_sprite(body, 960, 540, ax=480, ay=270, ss=ss, defs=f"<defs>{defs}</defs>")

def _draw_2x(sp):
    return lambda c, t, o: (c.save(), c.scale(2.02, 2.02), draw_sprite(c, sp), c.restore())

def _draw_scan_2x(sp, t0, sure=0.70, vertical=False):
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

# ───────── 2.01 · Courtroom Sentencing (GUILTY? / DEATH SENTENCE)
def build_201():
    kw = [("lincoln", 0.25, 0.95), ("sentenced", 1.35, 2.15), ("guilty", 2.55, 3.55)]
    ck = Cekim("2.01", sure=4.2, kelimeler=kw, duygu=Duygu("ofke"), arka="#101218")
    sp_u, sp_o, sp_s, sp_p, sp_f = (_sp_layer(set_201_mahkeme, [k]) for k in ("uzak", "orta", "sahne", "plan", "onplan"))

    def ciz_fx(c, t, o):
        # kamera flaş patlamaları + GUILTY? damgası (saçtan temiz ayrık)
        for ft in (1.38, 2.60):
            if ft <= t <= ft + 0.22:
                c.drawRect(skia.Rect(-W/2, -H/2, W/2, H/2), paint("#FFFFFF", 0.35 * (1 - (t - ft) / 0.22)))
        _damga(c, "GUILTY?", -260, -320, clamp((t - 2.55) / 0.28), KIRMIZI, boyut=38)

    # R4-PARALAKS: orta + sahne + onplan tek karakter/etkileşim düzleminde (derinlik=1.0) — kafa/el ASLA kopmaz!
    sp_main = _sp_layer(set_201_mahkeme, ["orta", "sahne", "onplan"])
    ck.ekle(
        Oge("uzak", _draw_2x(sp_u), derinlik=0.65),
        Oge("sahne", _draw_2x(sp_main), derinlik=1.0),
        Oge("plan", _draw_scan_2x(sp_p, ck.k("sentenced"), 0.60), derinlik=1.0),
        Oge("fx_201", ciz_fx, derinlik=1.0),
    )
    ck.kamera = Kamera(
        x=Iz([(0, W/2 + 90), (1.5, W/2, "out"), (4.2, W/2 - 140, "io")]),
        z=Iz([(0, 1.06), (1.5, 1.12, "out"), (4.2, 1.24, "in")]),
        sarsinti=[(1.38, 0.30, 20)],
    )
    ck.ust.append(_hud("2.01", "Lincoln is framed for murder and sentenced to death. At first, you believe he's guilty.",
                       lambda t: "guilty" if t >= 2.55 else ("sentenced" if t >= 1.35 else ("lincoln" if t >= 0.25 else ""))))
    return ck

def ciz_zarf_sil(c, u):
    c.drawRect(skia.Rect(-125, 0, 125, H), paint("#7A5A3A"))
    c.drawRect(skia.Rect(102, 0, 125, H), paint("#080A0F", 0.85))

# ───────── 2.02 · Apartment Truth Letter ($90,000 LOAN / FOR YOU)
def build_202():
    kw = [("truth", 0.35, 1.15), ("you", 2.15, 3.35)]
    ck = Cekim("2.02", sure=4.2, kelimeler=kw, duygu=Duygu("ofke").gecis("yas", t0=0.95, sure=0.9), arka="#0A0F18")
    sp_u, sp_o, sp_s, sp_p, sp_f = (_sp_layer(set_202_mektup, [k]) for k in ("uzak", "orta", "sahne", "plan", "onplan"))

    def ciz_fx(c, t, o):
        for i in range(16):
            rx = -800 + (i * 41) % 520
            ry = -440 + ((i * 67 + t * 320) % 560)
            c.drawLine(rx, ry, rx - 5, ry + 20, paint("#9BC2E0", 0.35, Style=skia.Paint.kStroke_Style, StrokeWidth=2))
        _damga(c, "FOR YOU", -480, -310, clamp((t - 2.15) / 0.30), PLAN_C, boyut=38)

    sp_main = _sp_layer(set_202_mektup, ["orta", "sahne", "onplan"])
    ck.ekle(
        Oge("uzak", _draw_2x(sp_u), derinlik=0.65),
        Oge("sahne", _draw_2x(sp_main), derinlik=1.0),
        Oge("plan", _draw_scan_2x(sp_p, ck.k("you", -0.25), 0.65), derinlik=1.0),
        Oge("fx_202", ciz_fx, derinlik=1.0),
        Oge("michael_goz", lambda c, t, o: None, x=W/2 + 430, y=H/2 - 175, derinlik=1.0),
    )
    ck.kamera = Kamera(
        x=Iz([(0, W/2 - 120), (2.2, W/2 + 120, "io"), (4.2, W/2 + 240, "in")]),
        y=Iz([(0, H/2 + 60), (4.2, H/2 - 90, "io")]),
        z=Iz([(0, 1.06), (4.2, 1.32, "in")]),
    )
    ck.ust.append(_hud("2.02", "Then you learn the truth. That ninety-thousand-dollar debt was taken out for you.",
                       lambda t: "you" if t >= 2.15 else ("truth" if t >= 0.35 else "")))
    return ck

# ───────── 2.03 · Conspiracy Planning Wall (1 YEAR · PRISON BREAK)
def build_203():
    kw = [("choice", 0.25, 0.95), ("year", 1.45, 2.25), ("break", 2.55, 3.55)]
    ck = Cekim("2.03", sure=4.2, kelimeler=kw, duygu=Duygu("merak").gecis("gerilim", t0=2.55, sure=0.75), arka="#0C1018")
    sp_u, sp_o, sp_s, sp_p, sp_f = (_sp_layer(set_203_plan_duvari, [k]) for k in ("uzak", "orta", "sahne", "plan", "onplan"))

    def ciz_fx(c, t, o):
        _damga(c, "1 YEAR · PRISON BREAK", 0, -330, clamp((t - 1.45) / 0.30), PLAN_C, boyut=34)

    ck.ekle(
        Oge("uzak", _draw_2x(sp_u), derinlik=0.45), Oge("orta", _draw_2x(sp_o), derinlik=0.75),
        Oge("plan_duvar", _draw_2x(sp_s), derinlik=1.0),
        Oge("plan", _draw_scan_2x(sp_p, ck.k("break", -0.35), 0.85), derinlik=1.08),
        Oge("onplan", _draw_2x(sp_f), derinlik=1.22),
        Oge("fx_203", ciz_fx, derinlik=1.26),
    )
    ck.kamera = Kamera(
        x=Iz([(0, W/2 - 140), (2.2, W/2 + 80, "io"), (4.2, W/2 + 20, "io")]),
        z=Iz([(0, 1.06), (4.2, 1.24, "in")]),
    )
    ck.ust.append(_hud("2.03", "You make an impossible choice. You spend a year planning a prison break.",
                       lambda t: "break" if t >= 2.55 else ("year" if t >= 1.45 else ("choice" if t >= 0.25 else ""))))
    return ck

# ───────── 2.04 · Tattoo Parlor (4 MONTHS · THE MAP — A-Sırt v1!)
def build_204():
    kw = [("needle", 0.30, 1.05), ("corridor", 1.55, 2.45), ("ink", 2.85, 3.90)]
    ck = Cekim("2.04", sure=4.5, kelimeler=kw, duygu=Duygu("gerilim"), arka="#0B0E14")
    sp_u, sp_o, sp_s, sp_p, sp_f = (_sp_layer(set_204_dovme_studyosu, [k]) for k in ("uzak", "orta", "sahne", "plan", "onplan"))

    def ciz_fx(c, t, o):
        # dövme iğnesi kıvılcımı + 4 MONTHS damgası
        if 1.2 <= t <= 3.8:
            c.drawCircle(110, -45, 10 + 6 * math.sin(t * 28), paint(PLAN_C, 0.75))
        _damga(c, "4 MONTHS · THE MAP", -430, -320, clamp((t - 0.40) / 0.30), PLAN_C, boyut=32)

    sp_main = _sp_layer(set_204_dovme_studyosu, ["orta", "sahne"])
    ck.ekle(
        Oge("uzak", _draw_2x(sp_u), derinlik=0.65),
        Oge("dovme_plan", _draw_2x(sp_main), derinlik=1.0, ikincil=[("nefes", 0.9)]),
        Oge("plan", _draw_scan_2x(sp_p, ck.k("corridor", -0.25), 0.95, vertical=True), derinlik=1.0),
        Oge("onplan", _draw_2x(sp_f), derinlik=1.0, ikincil=[("titre", 0.45)]),
        Oge("fx_204", ciz_fx, derinlik=1.0),
    )
    ck.kamera = Kamera(
        x=Iz([(0, W/2 - 40), (4.5, W/2 + 30, "io")]),
        y=Iz([(0, H/2 - 20), (4.5, H/2 + 25, "io")]),
        z=Iz([(0, 1.04), (4.5, 1.26, "in")]),
    )
    ck.ust.append(_hud("2.04", "Four months under the needle. Every corridor of Fox River hidden inside gothic ink.",
                       lambda t: "ink" if t >= 2.85 else ("corridor" if t >= 1.55 else ("needle" if t >= 0.30 else ""))))
    return ck

# ───────── 2.05 · Polite Bank Robbery (POLITELY — Zero Violence!)
def build_205():
    kw = [("rob", 0.35, 1.15), ("bank", 1.35, 2.05), ("politely", 2.35, 3.30)]
    ck = Cekim("2.05", sure=3.8, kelimeler=kw, duygu=Duygu("merak"), arka="#10141B")
    sp_u, sp_o, sp_s, sp_p, sp_f = (_sp_layer(set_205_banka, [k]) for k in ("uzak", "orta", "sahne", "plan", "onplan"))

    def ciz_fx(c, t, o):
        # tavandan dökülen alçı tozu + siren parıltısı
        if 0.35 <= t <= 0.55:
            c.drawRect(skia.Rect(-W/2, -H/2, W/2, H/2), paint("#FFF5D0", 0.35 * (1 - (t - 0.35) / 0.20)))
        for i in range(18):
            dx = -380 + (i * 53) % 760
            dy = -420 + ((i * 61 + t * 240) % 720)
            c.drawCircle(dx, dy, 3.0, paint("#EAE4D4", 0.55))
        _damga(c, "POLITELY", 380, -305, clamp((t - 2.35) / 0.28), ALTIN, boyut=42)

    sp_main = _sp_layer(set_205_banka, ["orta", "sahne", "onplan"])
    ck.ekle(
        Oge("uzak", _draw_2x(sp_u), derinlik=0.65),
        Oge("sahne", _draw_2x(sp_main), derinlik=1.0),
        Oge("plan", _draw_scan_2x(sp_p, ck.k("politely", -0.2), 0.55), derinlik=1.0),
        Oge("fx_205", ciz_fx, derinlik=1.0),
    )
    ck.kamera = Kamera(
        y=Iz([(0, H/2 - 70), (1.8, H/2 + 25, "out"), (3.8, H/2 + 55, "io")]),
        z=Iz([(0, 1.06), (3.8, 1.22, "io")]),
        sarsinti=[(0.38, 0.22, 14)],
    )
    ck.ust.append(_hud("2.05", "For the first time in your life, you rob a bank. Politely.",
                       lambda t: "politely" if t >= 2.35 else ("bank" if t >= 1.35 else ("rob" if t >= 0.35 else ""))))
    return ck

# ───────── 2.06 · Inmate File #94941 (FOX RIVER · 5 YEARS)
def build_206():
    kw = [("charges", 0.30, 1.15), ("river", 1.85, 2.95)]
    ck = Cekim("2.06", sure=3.8, kelimeler=kw, duygu=Duygu("gerilim"), arka="#14110E")
    sp_u, sp_o, sp_s, sp_p, sp_f = (_sp_layer(set_206_dosya_94941, [k]) for k in ("uzak", "orta", "sahne", "plan", "onplan"))

    ck.ekle(
        Oge("uzak", _draw_2x(sp_u), derinlik=0.45), Oge("orta", _draw_2x(sp_o), derinlik=0.75),
        Oge("sahne", _draw_2x(sp_s), derinlik=1.0, giris=("kay_sol", 0.0, 0.45)),
        Oge("dosya_damga", _draw_scan_2x(sp_p, ck.k("river", -0.2), 0.45), x=W/2 + 280, y=H/2 + 120, derinlik=1.08),
        Oge("onplan", _draw_2x(sp_f), derinlik=1.22),
    )
    ck.kamera = Kamera(
        x=Iz([(0, W/2 - 60), (3.8, W/2 + 100, "in")]),
        z=Iz([(0, 1.04), (1.8, 1.12, "out"), (3.8, 1.28, "in")]),
        sarsinti=[(1.88, 0.32, 22)],
    )
    ck.ust.append(_hud("2.06", "You don't fight the charges. You ask for one thing: Fox River.",
                       lambda t: "river" if t >= 1.85 else ("charges" if t >= 0.30 else "")))
    return ck

# ───────── 2.07 · Fox River Gates & Countdown (EXECUTION IN 30 DAYS)
def build_207():
    kw = [("gates", 0.25, 1.00), ("countdown", 1.55, 2.45), ("execution", 2.75, 3.85)]
    ck = Cekim("2.07", sure=4.4, kelimeler=kw, duygu=Duygu("gerilim").gecis("ofke", t0=1.55, sure=0.75), arka="#080D14")
    sp_u, sp_o, sp_s, sp_p, sp_f = (_sp_layer(set_207_fox_kapilar, [k]) for k in ("uzak", "orta", "sahne", "plan", "onplan"))

    def ciz_fx(c, t, o):
        # fırtına yağmuru + EXECUTION IN 30 DAYS nabzı
        for i in range(22):
            rx = -880 + (i * 83) % 1760
            ry = -480 + ((i * 71 + t * 540) % 920)
            c.drawLine(rx, ry, rx - 10, ry + 28, paint("#9BC2E0", 0.32, Style=skia.Paint.kStroke_Style, StrokeWidth=2))
        if t >= 1.55:
            pulse = 0.5 + 0.5 * math.sin(t * 10)
            c.drawRect(skia.Rect(215, -455, 760, -335), paint(KIRMIZI, 0.22 * pulse, Style=skia.Paint.kStroke_Style, StrokeWidth=6))

    sp_main = _sp_layer(set_207_fox_kapilar, ["orta", "sahne", "onplan"])
    ck.ekle(
        Oge("uzak", _draw_2x(sp_u), derinlik=0.65),
        Oge("sahne", _draw_2x(sp_main), derinlik=1.0),
        Oge("plan", _draw_scan_2x(sp_p, ck.k("execution", -0.35), 0.70), derinlik=1.0),
        Oge("fx_207", ciz_fx, derinlik=1.0),
    )
    ck.kamera = Kamera(
        y=Iz([(0, H/2 + 25), (4.4, H/2 - 20, "io")]),
        z=Iz([(0, 1.0), (1.5, 1.05, "out"), (4.4, 1.10, "in")]),
        sarsinti=[(0.30, 0.34, 24)],
    )
    ck.ust.append(_hud("2.07", "The gates slam behind you. Now the countdown begins: thirty days to execution.",
                       lambda t: "execution" if t >= 2.75 else ("countdown" if t >= 1.55 else ("gates" if t >= 0.25 else ""))))
    return ck

def build_film():
    c = [build_201(), build_202(), build_203(), build_204(), build_205(), build_206(), build_207()]
    return Film([
        c[0], OnPlanSil(ciz_zarf_sil, sure=0.55),
        c[1], ZoomIcinden("michael_goz", sure=0.60, renk=PLAN_C),
        c[2], Eslesme("plan_duvar", "dovme_plan", sure=0.65),
        c[3], ZoomIcinden("dovme_plan", sure=0.60, renk=PLAN_C),
        c[4], Savurma(yon=1, sure=0.45),
        c[5], Maske("dosya_damga", boyut=(360, 180), sure=0.70),
        c[6],
    ])

def kontakt_olustur(film, kare_klasor, out_png):
    bas = film.bas
    anlar = [
        ("2.01 · Courtroom (GUILTY?)",      bas[0] + 2.95),
        ("TRANS 1 · Envelope Wipe",         bas[1] + 0.28),
        ("2.02 · Truth Letter (FOR YOU)",   bas[1] + 2.85),
        ("TRANS 2 · Cyan Eye Zoom",         bas[2] + 0.30),
        ("2.03 · Planning Wall (1 YEAR)",   bas[2] + 3.05),
        ("TRANS 3 · Wall → Back Tattoo",    bas[3] + 0.32),
        ("2.04 · Tattoo Parlor (A-Sırt)",   bas[3] + 3.15),
        ("2.05 · Bank Robbery (POLITELY)",  bas[4] + 2.75),
        ("TRANS 5 · Whip → Judge Desk",     bas[5] + 0.22),
        ("2.06 · Inmate File #94941",       bas[5] + 2.45),
        ("TRANS 6 · Stamp Mask → Gates",    bas[6] + 0.35),
        ("2.07 · EXECUTION IN 30 DAYS",     bas[6] + 3.25),
    ]
    pngler = film.onizle([t for _, t in anlar], str(kare_klasor), olcek=0.5)
    cols, rows, tw, th, pad, top = 4, 3, 440, 248, 14, 54
    sheet = Image.new("RGB", (cols*tw+(cols+1)*pad, top+rows*(th+26)+pad), (10, 14, 22))
    draw = ImageDraw.Draw(sheet)
    ft = ImageFont.truetype(str(REPO / "fonts/AlegreyaSC-Bold.ttf"), 21)
    fl = ImageFont.truetype(str(REPO / "fonts/Alegreya.ttf"), 15)
    draw.text((pad, 14), f"ACT II ('WEARING THE MAP') F4b EN — 5-LAYER PARALLAX SETS (960 px) · {film.sure:.1f}s · 6/6 Semantic", fill=(127, 230, 255), font=ft)
    for i, ((etiket, t), p) in enumerate(zip(anlar, pngler)):
        r, c = divmod(i, cols); x, y = pad + c*(tw+pad), top + r*(th+26)
        sheet.paste(Image.open(p).convert("RGB").resize((tw, th), Image.Resampling.LANCZOS), (x, y))
        draw.rectangle([x, y, x+tw, y+th], outline=(55, 85, 110), width=2)
        draw.text((x+4, y+th+4), f"{etiket} ({t:.1f}s)", fill=(220, 230, 240), font=fl)
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
    print(f"Act II EN kuruldu: {len(film.cekimler)} çekim, toplam {film.sure:.2f} sn", flush=True)
    kontakt_png = P / "bolum2_en_kontakt_960.png"
    kontakt_olustur(film, P / "kareler_b2_en", kontakt_png)
    print("Kontakt Act II EN tamam:", kontakt_png, flush=True)
    mp4 = P / "bolum2_en_960.mp4"
    render_taslak_960(film, mp4, fps=16, crf=24)
    print("MP4 Act II EN tamam:", mp4, flush=True)
