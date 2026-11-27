"""Act IV ('On the Run') F4b EN — TRUE LIVE ANIMATED 2D ACTION (R18-HAREKET + R4-ANATOMI).

Imports 8 locked R18-HAREKET scene sets from V10, V11, V12 (zero side effects).
Real physical in-scene animation in EVERY shot (zero slideshow):
  - 4.01: FBI desk lamp brightens -> red strings snap across corkboard -> anatomical FBI hand physically pins UTAH!
  - 4.02: Scrolling wet night highway + wipers + rearview sirens -> 3 fake ID cards physically fly/fan into frame!
  - 4.03: Locked Turna v4 physically unfolds into creased cipher paper -> cyan coordinates ignite (GILA NM 04:00)!
  - 4.04: Flickering MOTEL neon + warm lamp motes -> clean white bandage physically wraps Michael's wrist (0 blood)!
  - 4.05: Warm dusk silhouettes fade under cold shadow -> brass pocket watch physically drops & swings to 06:14!
  - 4.06: STEADMAN ALIVE! newspaper spins & slams -> golden pardon signature physically vanishes -> PARDON REVOKED slams!
  - 4.07: CHRISTINA ROSE sailboat physically bobs & glides through drifting mist -> crimson Company trap rings contract!
  - 4.08: Blistering desert heat -> massive rusted Sona iron gate doors (+122px/-122px) physically SLAM SHUT (4px slit)!
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

from b4_set_takip_turna import set_401_fbi_masasi, set_402_otoyol_kimlik, set_403_sifreli_turna
from b4_set_bulusma_manset import set_404_motel_bulusma, set_405_baba_saati, set_406_manset_af
from b4_set_panama_sona import set_407_panama_tekne, set_408_sona_kapisi

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


def _sp_layer(fn, katmanlar):
    defs, body = fn(katmanlar=katmanlar)
    return svg_sprite(body, 960, 540, defs=f"<defs>{defs}</defs>")


def _draw_2x(sp):
    return lambda c, t, o: (c.save(), c.scale(2.02, 2.02), draw_sprite(c, sp), c.restore())


def _draw_scan_2x(sp, t0, sure=0.65, vertical=False, dy=0.0):
    def _ciz(c, t, o):
        p = ease("out", clamp((t - t0) / sure))
        if p <= 0.005:
            return
        c.save()
        if vertical:
            sy = -H / 2 + H * p
            c.clipRect(skia.Rect(-W / 2, -H / 2, W / 2, sy))
            c.translate(0, dy); c.scale(2.02, 2.02); draw_sprite(c, sp)
            c.restore()
            if p < 0.98:
                c.drawLine(-W / 2, sy, W / 2, sy, paint("#FFFFFF", 0.95, Style=skia.Paint.kStroke_Style, StrokeWidth=4))
                c.drawLine(-W / 2, sy, W / 2, sy, paint(PLAN_C, 0.50, Style=skia.Paint.kStroke_Style, StrokeWidth=14))
        else:
            sx = -W / 2 + W * p
            c.clipRect(skia.Rect(-W / 2, -H / 2, sx, H / 2))
            c.translate(0, dy); c.scale(2.02, 2.02); draw_sprite(c, sp)
            c.restore()
            if p < 0.98:
                c.drawLine(sx, -H / 2, sx, H / 2, paint("#FFFFFF", 0.95, Style=skia.Paint.kStroke_Style, StrokeWidth=4))
                c.drawLine(sx, -H / 2, sx, H / 2, paint(PLAN_C, 0.50, Style=skia.Paint.kStroke_Style, StrokeWidth=14))
    return _ciz


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


# --------- 4.01 Mahone's FBI Desk & Tattoo Wall (ANOTHER MIND)
def build_401():
    kw = [("genius", 0.35, 1.25), ("tattoo", 1.55, 2.55), ("map", 2.95, 4.25)]
    ck = Cekim("4.01", sure=4.8, kelimeler=kw, duygu=Duygu("gerilim").gecis("korku", t0=2.95, sure=0.8), arka="#0A0E14")
    sp_u = _sp_layer(set_401_fbi_masasi, ["uzak"])
    sp_base = _sp_layer(set_401_fbi_masasi, ["orta", "sahne"])
    sp_ip = _sp_layer(set_401_fbi_masasi, ["kirmizi_ip"])
    sp_igne = _sp_layer(set_401_fbi_masasi, ["harita_igne"])
    sp_p = _sp_layer(set_401_fbi_masasi, ["plan"])
    sp_f = _sp_layer(set_401_fbi_masasi, ["onplan"])

    def ciz_ip(c, t, o):
        # Red investigation strings physically sweep left-to-right from A-Sirt v1 photo to US map!
        p = ease("out", clamp((t - 1.35) / 1.15))
        if p <= 0.01:
            return
        sx = -W / 2 + W * p
        c.save()
        c.clipRect(skia.Rect(-W / 2, -H / 2, sx, H / 2))
        c.scale(2.02, 2.02); draw_sprite(c, sp_ip)
        c.restore()

    def ciz_igne(c, t, o):
        # Refined anatomical FBI hand physically lunges in from top-right to pin UTAH at 'map' (t=2.85s)!
        p = ease("out", clamp((t - 2.65) / 0.45))
        if p <= 0.01:
            return
        dx = 260.0 * (1.0 - p)
        dy = -160.0 * (1.0 - p)
        c.save()
        c.translate(dx, dy)
        c.scale(2.02, 2.02); draw_sprite(c, sp_igne)
        c.restore()
        if 3.05 <= t <= 3.55:
            rp = (t - 3.05) / 0.50
            c.drawCircle(240, -70, 26 + 85 * rp, paint(KIRMIZI, 0.72 * (1.0 - rp), Style=skia.Paint.kStroke_Style, StrokeWidth=4))

    def ciz_fx(c, t, o):
        # Desk lamp click-brighten at 'genius' + drifting office dust
        lamp = 0.06 + 0.08 * ease("out", clamp((t - 0.30) / 0.45))
        c.drawCircle(-560, 120, 380, paint(ALTIN, lamp))
        for i in range(12):
            mx = -720 + ((i * 89 + t * 18) % 520)
            my = -220 + ((i * 67 - t * 14) % 440)
            c.drawCircle(mx, my, 2.6, paint(ALTIN, 0.25))

    ck.ekle(
        Oge("uzak", _draw_2x(sp_u), derinlik=0.65),
        Oge("sahne", _draw_2x(sp_base), derinlik=1.0),
        Oge("ip_anim", ciz_ip, derinlik=1.0),
        Oge("igne_anim", ciz_igne, derinlik=1.0),
        Oge("plan", _draw_scan_2x(sp_p, ck.k("map", -0.15), 0.65), derinlik=1.0),
        Oge("onplan", _draw_2x(sp_f), derinlik=1.0),
        Oge("fx_401", ciz_fx, derinlik=1.0),
        Oge("harita_igne", lambda c, t, o: None, x=W / 2 + 240, y=H / 2 - 70, derinlik=1.0),
    )
    ck.kamera = Kamera(
        x=Iz([(0, W / 2 - 20), (4.8, W / 2 + 20, "io")]),
        z=Iz([(0, 1.01), (4.8, 1.06, "in")]),
        sarsinti=[(3.08, 0.22, 14)],
    )
    ck.ust.append(_hud("4.01", "Now an FBI genius studies your tattoo. Someone else is reading the map.",
                       lambda t: "map" if t >= 2.95 else ("tattoo" if t >= 1.55 else ("genius" if t >= 0.35 else ""))))
    return ck


# --------- 4.02 Night Highway & Fake Aliases (Gag 2: NEW NAME.)
def build_402():
    kw = [("city", 0.30, 1.00), ("name", 1.15, 2.55), ("trap", 3.15, 4.25)]
    ck = Cekim("4.02", sure=4.6, kelimeler=kw, duygu=Duygu("merak").gecis("gerilim", t0=3.15, sure=0.75), arka="#070B12")
    sp_u = _sp_layer(set_402_otoyol_kimlik, ["uzak"])
    sp_o = _sp_layer(set_402_otoyol_kimlik, ["orta"])
    sp_k1 = _sp_layer(set_402_otoyol_kimlik, ["kart_1"])
    sp_k2 = _sp_layer(set_402_otoyol_kimlik, ["kart_2"])
    sp_k3 = _sp_layer(set_402_otoyol_kimlik, ["kart_3"])
    sp_s = _sp_layer(set_402_otoyol_kimlik, ["sahne"])
    sp_p = _sp_layer(set_402_otoyol_kimlik, ["plan"])
    sp_f = _sp_layer(set_402_otoyol_kimlik, ["onplan"])

    def _fly_card(sp, t0, from_dx, from_dy, from_rot):
        def _ciz(c, t, o):
            p = ease("out", clamp((t - t0) / 0.42))
            if p <= 0.01:
                return
            dx = from_dx * (1.0 - p)
            dy = from_dy * (1.0 - p)
            rot = from_rot * (1.0 - p)
            c.save()
            c.translate(dx, dy); c.rotate(rot)
            c.scale(2.02, 2.02); draw_sprite(c, sp)
            c.restore()
        return _ciz

    def ciz_fx(c, t, o):
        # Scrolling night highway raindrops + rearview red/blue police siren strobe at 'trap'
        for i in range(26):
            rx = -880 + ((i * 71 + int(t * 95)) % 1760)
            ry = -460 + ((i * 83 + t * 520) % 920)
            c.drawLine(rx, ry, rx - 6, ry + 24, paint("#9BC8EB", 0.30, Style=skia.Paint.kStroke_Style, StrokeWidth=2))
        if t >= 2.75:
            sr = 0.22 * (0.5 + 0.5 * math.sin(t * 16.0))
            sb = 0.22 * (0.5 - 0.5 * math.sin(t * 16.0))
            c.drawCircle(-40, -340, 120, paint(KIRMIZI, sr))
            c.drawCircle(60, -340, 120, paint("#3B82F6", sb))

    ck.ekle(
        Oge("uzak", _draw_2x(sp_u), derinlik=0.65),
        Oge("orta", _draw_2x(sp_o), derinlik=1.0),
        Oge("kart1_anim", _fly_card(sp_k1, 0.55, -520, 260, -24), derinlik=1.0),
        Oge("kart2_anim", _fly_card(sp_k2, 1.35, 0, 420, 16), derinlik=1.0),
        Oge("kart3_anim", _fly_card(sp_k3, 2.15, 540, 260, 22), derinlik=1.0),
        Oge("sahne", _draw_2x(sp_s), derinlik=1.0),
        Oge("plan", _draw_scan_2x(sp_p, ck.k("trap", -0.25), 0.65, dy=-82.0), derinlik=1.0),
        Oge("onplan", _draw_2x(sp_f), derinlik=1.0),
        Oge("fx_402", ciz_fx, derinlik=1.0),
    )
    ck.kamera = Kamera(
        x=Iz([(0, W / 2 - 20), (2.3, W / 2 + 20, "io"), (4.6, W / 2, "out")]),
        z=Iz([(0, 1.02), (4.6, 1.06, "in")]),
        sarsinti=[(0.55, 0.14, 10), (1.35, 0.14, 10), (2.15, 0.16, 12)],
    )
    ck.ust.append(_hud("4.02", "New city, new name: Michael Crane. Every road ahead is a trap.",
                       lambda t: "trap" if t >= 3.15 else ("name" if t >= 1.15 else ("city" if t >= 0.30 else ""))))
    return ck


# --------- 4.03 Sara's Coded Origami Crane (FOLDED CODE — Turna v4 Unfolds!)
def build_403():
    kw = [("crane", 0.35, 1.15), ("unfolds", 1.35, 2.35), ("numbers", 2.65, 4.15)]
    ck = Cekim("4.03", sure=4.8, kelimeler=kw, duygu=Duygu("merak").gecis("umut", t0=2.65, sure=0.85), arka="#17110B")
    sp_u = _sp_layer(set_403_sifreli_turna, ["uzak"])
    sp_o = _sp_layer(set_403_sifreli_turna, ["orta"])
    sp_acik = _sp_layer(set_403_sifreli_turna, ["turna_acik"])
    sp_kapali = _sp_layer(set_403_sifreli_turna, ["turna_kapali"])
    sp_s = _sp_layer(set_403_sifreli_turna, ["sahne"])
    sp_p = _sp_layer(set_403_sifreli_turna, ["plan"])
    sp_f = _sp_layer(set_403_sifreli_turna, ["onplan"])

    def ciz_turna_morph(c, t, o):
        # Locked Turna v4 physically unfolds into the creased cipher sheet at 'unfolds' (t=1.35 -> 2.45s)!
        u = ease("io", clamp((t - 1.35) / 1.05))
        # Unfolded paper expands smoothly from center as crane opens
        if u > 0.02:
            sc_p = 0.72 + 0.28 * u
            c.saveLayerAlpha(None, int(255 * clamp(u * 1.15)))
            c.scale(sc_p, sc_p)
            c.scale(2.02, 2.02); draw_sprite(c, sp_acik)
            c.restore()
        # Folded Turna v4 gently lifts & fades out as paper flattens open
        if u < 0.98:
            sc_k = 1.0 + 0.14 * u
            c.saveLayerAlpha(None, int(255 * clamp(1.0 - u)))
            c.scale(sc_k, sc_k)
            c.scale(2.02, 2.02); draw_sprite(c, sp_kapali)
            c.restore()

    def ciz_fx(c, t, o):
        for i in range(14):
            mx = -680 + ((i * 97 + t * 18) % 1360)
            my = -320 + ((i * 71 - t * 16) % 620)
            c.drawCircle(mx, my, 2.8, paint(ALTIN, 0.30 + 0.14 * math.sin(t * 2.8 + i)))

    ck.ekle(
        Oge("uzak", _draw_2x(sp_u), derinlik=0.65),
        Oge("orta", _draw_2x(sp_o), derinlik=1.0),
        Oge("turna_morph", ciz_turna_morph, derinlik=1.0),
        Oge("sahne", _draw_2x(sp_s), derinlik=1.0),
        Oge("plan", _draw_scan_2x(sp_p, ck.k("numbers", -0.15), 0.70, dy=-72.0), derinlik=1.0),
        Oge("onplan", _draw_2x(sp_f), derinlik=1.0),
        Oge("fx_403", ciz_fx, derinlik=1.0),
        Oge("sifre_kod", lambda c, t, o: None, x=W / 2, y=H / 2 + 20, derinlik=1.0),
    )
    ck.kamera = Kamera(
        z=Iz([(0, 1.01), (4.8, 1.06, "in")]),
    )
    ck.ust.append(_hud("4.03", "Inside Sara's bag, a paper crane unfolds. Hidden numbers mark a rendezvous.",
                       lambda t: "numbers" if t >= 2.65 else ("unfolds" if t >= 1.35 else ("crane" if t >= 0.35 else ""))))
    return ck


# --------- 4.04 Motel Reunion & Bandage (STILL HERE — 0 Blood, 2 Complete Arms!)
def build_404():
    kw = [("waiting", 0.35, 1.35), ("bandages", 1.75, 3.05), ("stay", 3.35, 4.35)]
    ck = Cekim("4.04", sure=4.8, kelimeler=kw, duygu=Duygu("huzur").gecis("umut", t0=3.35, sure=0.8), arka="#16100C")
    sp_u = _sp_layer(set_404_motel_bulusma, ["uzak"])
    sp_main = _sp_layer(set_404_motel_bulusma, ["orta", "sahne"])
    sp_ban = _sp_layer(set_404_motel_bulusma, ["bandaj_sar"])
    sp_p = _sp_layer(set_404_motel_bulusma, ["plan"])
    sp_f = _sp_layer(set_404_motel_bulusma, ["onplan"])

    def ciz_bandaj(c, t, o):
        # Clean white bandage physically wraps progressively onto Michael's wrist at 'bandages' (t=1.65 -> 2.85s)!
        p = ease("io", clamp((t - 1.55) / 1.25))
        if p <= 0.01:
            return
        sx = -W / 2 + W * (0.35 + 0.35 * p)
        c.save()
        c.clipRect(skia.Rect(-W / 2, -H / 2, sx, H / 2))
        c.scale(2.02, 2.02); draw_sprite(c, sp_ban)
        c.restore()

    def ciz_fx(c, t, o):
        # Warm flickering MOTEL neon glow through rainy window + dust motes
        nf = 0.07 + 0.05 * math.sin(t * 17.0)
        c.drawCircle(-40, -240, 260, paint("#FF5A40", nf))
        for i in range(12):
            mx = -640 + ((i * 107 + t * 14) % 1280)
            my = -280 + ((i * 73 - t * 14) % 560)
            c.drawCircle(mx, my, 2.6, paint(ALTIN, 0.28))

    ck.ekle(
        Oge("uzak", _draw_2x(sp_u), derinlik=0.65),
        Oge("sahne", _draw_2x(sp_main), derinlik=1.0),
        Oge("bandaj_anim", ciz_bandaj, derinlik=1.0),
        Oge("plan", _draw_scan_2x(sp_p, ck.k("stay", -0.25), 0.65), derinlik=1.0),
        Oge("onplan", _draw_2x(sp_f), derinlik=1.0),
        Oge("fx_404", ciz_fx, derinlik=1.0),
    )
    ck.kamera = Kamera(
        z=Iz([(0, 1.01), (4.8, 1.05, "in")]),
    )
    ck.ust.append(_hud("4.04", "You find Sara waiting in the dark. She bandages your hand - and chooses to stay.",
                       lambda t: "stay" if t >= 3.35 else ("bandages" if t >= 1.75 else ("waiting" if t >= 0.35 else ""))))
    return ck


def ciz_perde_sil(c, u):
    c.drawRect(skia.Rect(-140, 0, 140, H), paint("#231A16"))
    for x in range(-110, 120, 38):
        c.drawLine(x, 0, x, H, paint("#120D0A", 0.65, Style=skia.Paint.kStroke_Style, StrokeWidth=10))


# --------- 4.05 The Father's Watch (06:14 — ZERO VIOLENCE, Live Dropping Watch!)
def build_405():
    kw = [("father", 0.35, 1.55), ("shadows", 1.85, 2.75), ("watch", 3.05, 4.65)]
    ck = Cekim("4.05", sure=5.2, kelimeler=kw, duygu=Duygu("umut").gecis("yas", t0=2.85, sure=0.9), arka="#1B130B")
    sp_u = _sp_layer(set_405_baba_saati, ["uzak"])
    sp_o = _sp_layer(set_405_baba_saati, ["orta", "sahne"])
    sp_golge = _sp_layer(set_405_baba_saati, ["baba_golge"])
    sp_saat = _sp_layer(set_405_baba_saati, ["dusen_saat"])
    sp_p = _sp_layer(set_405_baba_saati, ["plan"])
    sp_f = _sp_layer(set_405_baba_saati, ["onplan"])

    def ciz_golge(c, t, o):
        # Warm dusk memory silhouettes fade away under cold shadow sweep at 'shadows' (t=1.85 -> 2.85s)!
        fade = 1.0 - ease("io", clamp((t - 1.85) / 1.00))
        if fade <= 0.01:
            return
        c.saveLayerAlpha(None, int(255 * fade))
        c.scale(2.02, 2.02); draw_sprite(c, sp_golge)
        c.restore()

    def ciz_saat(c, t, o):
        # Brass pocket watch physically drops from above into (480,310) -> (0, +80) & swings gently to a halt!
        if t < 2.55:
            return
        dp = ease("out", clamp((t - 2.55) / 0.55))
        dy = -340.0 * (1.0 - dp)
        # damped pendulum swing after landing
        sw_t = max(0.0, t - 3.05)
        ang = math.sin(sw_t * 10.0) * 14.0 * math.exp(-sw_t * 2.2)
        c.save()
        c.translate(0, 80 + dy)
        c.rotate(ang)
        c.translate(0, -80)
        c.scale(2.02, 2.02); draw_sprite(c, sp_saat)
        c.restore()

    def ciz_fx(c, t, o):
        # Cold shadow sweep at 'shadows' + subtle grief cool veil after 'watch'
        if 1.75 <= t <= 2.95:
            sp = ease("io", (t - 1.75) / 1.20)
            sx = -W + W * 2.0 * sp
            c.drawRect(skia.Rect(sx - 280, -H / 2, sx + 280, H / 2), paint("#080B12", 0.38 * math.sin(sp * math.pi)))
        if t >= 2.85:
            gp = ease("out", clamp((t - 2.85) / 0.90))
            c.drawRect(skia.Rect(-W / 2, -H / 2, W / 2, H / 2), paint("#141B26", 0.28 * gp))

    ck.ekle(
        Oge("uzak", _draw_2x(sp_u), derinlik=0.65),
        Oge("orta", _draw_2x(sp_o), derinlik=1.0),
        Oge("golge_anim", ciz_golge, derinlik=1.0),
        Oge("saat_anim", ciz_saat, derinlik=1.0),
        Oge("plan", _draw_scan_2x(sp_p, ck.k("watch", 0.05), 0.70), derinlik=1.0),
        Oge("onplan", _draw_2x(sp_f), derinlik=1.0),
        Oge("fx_405", ciz_fx, derinlik=1.0),
        Oge("dusen_saat", lambda c, t, o: None, x=W / 2, y=H / 2 + 80, derinlik=1.0),
    )
    ck.kamera = Kamera(
        y=Iz([(0, H / 2 - 14), (5.2, H / 2 + 12, "io")]),
        z=Iz([(0, 1.01), (5.2, 1.06, "in")]),
        sarsinti=[(3.08, 0.16, 8)],
    )
    ck.ust.append(_hud("4.05", "Your father returns to save you from the shadows. Seconds later, only his watch remains.",
                       lambda t: "watch" if t >= 3.05 else ("shadows" if t >= 1.85 else ("father" if t >= 0.35 else ""))))
    return ck


# --------- 4.06 Conspiracy Headlines & Vanishing Pardon (STEADMAN ALIVE! -> REVOKED)
def build_406():
    kw = [("faked", 0.35, 1.55), ("pardon", 1.85, 2.75), ("vanishes", 2.95, 4.35)]
    ck = Cekim("4.06", sure=4.8, kelimeler=kw, duygu=Duygu("umut").gecis("ofke", t0=2.95, sure=0.70), arka="#140F0B")
    sp_u = _sp_layer(set_406_manset_af, ["uzak"])
    sp_base = _sp_layer(set_406_manset_af, ["orta", "sahne"])
    sp_imza = _sp_layer(set_406_manset_af, ["af_imza"])
    sp_gaz = _sp_layer(set_406_manset_af, ["gazete_1"])
    sp_rev = _sp_layer(set_406_manset_af, ["damga_revoked"])
    sp_p = _sp_layer(set_406_manset_af, ["plan"])
    sp_f = _sp_layer(set_406_manset_af, ["onplan"])

    def ciz_imza(c, t, o):
        # Golden presidential signature physically fades/erases itself at 'vanishes' (t=2.75 -> 3.55s)!
        fade = 1.0 - ease("in", clamp((t - 2.75) / 0.80))
        if fade <= 0.01:
            return
        c.saveLayerAlpha(None, int(255 * fade))
        c.scale(2.02, 2.02); draw_sprite(c, sp_imza)
        c.restore()

    def ciz_gazete(c, t, o):
        # STEADMAN ALIVE! newspaper physically spins 360 deg & slams onto desk at 'faked' (t=0.25 -> 0.85s)!
        p = ease("out", clamp((t - 0.20) / 0.55))
        if p <= 0.01:
            return
        ang = -360.0 * (1.0 - p)
        sc = 1.42 - 0.42 * p
        c.save()
        c.translate(0, 80); c.rotate(ang); c.scale(sc, sc); c.translate(0, -80)
        c.scale(2.02, 2.02); draw_sprite(c, sp_gaz)
        c.restore()

    def ciz_revoked(c, t, o):
        # Crimson PARDON REVOKED rubber stamp physically slams down at 'vanishes' (t=3.15s)!
        if t < 3.15:
            return
        p = ease("out", clamp((t - 3.15) / 0.22))
        sc = 1.55 - 0.55 * p
        c.saveLayerAlpha(None, int(255 * clamp(p * 1.4)))
        c.translate(-420, 40); c.scale(sc, sc); c.translate(420, -40)
        c.scale(2.02, 2.02); draw_sprite(c, sp_rev)
        c.restore()

    ck.ekle(
        Oge("uzak", _draw_2x(sp_u), derinlik=0.65),
        Oge("sahne", _draw_2x(sp_base), derinlik=1.0),
        Oge("imza_anim", ciz_imza, derinlik=1.0),
        Oge("gazete_anim", ciz_gazete, derinlik=1.0),
        Oge("revoked_anim", ciz_revoked, derinlik=1.0),
        Oge("plan", _draw_scan_2x(sp_p, ck.k("vanishes", 0.15), 0.60), derinlik=1.0),
        Oge("onplan", _draw_2x(sp_f), derinlik=1.0),
        Oge("gazete_muhur", lambda c, t, o: None, x=W / 2, y=H / 2 + 80, derinlik=1.0),
        Oge("af_imza", lambda c, t, o: None, x=W / 2 - 420, y=H / 2 + 40, derinlik=1.0),
    )
    ck.kamera = Kamera(
        z=Iz([(0, 1.01), (4.8, 1.06, "in")]),
        sarsinti=[(0.75, 0.18, 12), (3.18, 0.28, 20)],
    )
    ck.ust.append(_hud("4.06", "You prove the murder was faked. Then the presidential pardon vanishes from the page.",
                       lambda t: "vanishes" if t >= 2.95 else ("pardon" if t >= 1.85 else ("faked" if t >= 0.35 else ""))))
    return ck


# --------- 4.07 Panama Boat & The Trap (CHRISTINA ROSE + Closing Company Trap!)
def build_407():
    kw = [("panama", 0.35, 1.45), ("freedom", 1.65, 2.45), ("trap", 2.75, 4.25)]
    ck = Cekim("4.07", sure=4.8, kelimeler=kw, duygu=Duygu("umut").gecis("korku", t0=2.75, sure=0.75), arka="#0A1820")
    sp_u = _sp_layer(set_407_panama_tekne, ["uzak"])
    sp_o = _sp_layer(set_407_panama_tekne, ["orta"])
    sp_tekne = _sp_layer(set_407_panama_tekne, ["tekne"])
    sp_sis = _sp_layer(set_407_panama_tekne, ["sis_katman"])
    sp_s = _sp_layer(set_407_panama_tekne, ["sahne"])
    sp_tuzak = _sp_layer(set_407_panama_tekne, ["tuzak_halka"])
    sp_p = _sp_layer(set_407_panama_tekne, ["plan"])
    sp_f = _sp_layer(set_407_panama_tekne, ["onplan"])

    def ciz_tekne(c, t, o):
        # White sailboat CHRISTINA ROSE physically bobs on harbor waves & glides gently right!
        bob_y = math.sin(t * 2.8) * 10.0
        tilt = math.sin(t * 2.2 + 0.5) * 1.8
        glide_x = -45.0 + 90.0 * ease("io", clamp(t / 4.6))
        c.save()
        c.translate(glide_x, bob_y); c.rotate(tilt)
        c.scale(2.02, 2.02); draw_sprite(c, sp_tekne)
        c.restore()

    def ciz_sis(c, t, o):
        # Drifting dawn harbor mist
        dx = -60.0 + 120.0 * (t / 4.8)
        c.save()
        c.translate(dx, 0)
        c.scale(2.02, 2.02); draw_sprite(c, sp_sis)
        c.restore()

    def ciz_tuzak(c, t, o):
        # Crimson Company trap rings physically contract & lock around the sailboat at 'trap' (t=2.65s)!
        if t < 2.65:
            return
        p = ease("out", clamp((t - 2.65) / 0.55))
        sc = 1.28 - 0.28 * p
        c.saveLayerAlpha(None, int(255 * clamp(p * 1.25)))
        c.scale(sc, sc)
        c.scale(2.02, 2.02); draw_sprite(c, sp_tuzak)
        c.restore()

    def ciz_fx(c, t, o):
        # Flashing distant Panama police patrol strobes at 'trap'
        if t >= 2.55:
            sr = 0.22 * (0.5 + 0.5 * math.sin(t * 15.0))
            sb = 0.22 * (0.5 - 0.5 * math.sin(t * 15.0))
            c.drawCircle(-620, -40, 140, paint(KIRMIZI, sr))
            c.drawCircle(-520, -40, 140, paint("#3B82F6", sb))

    ck.ekle(
        Oge("uzak", _draw_2x(sp_u), derinlik=0.65),
        Oge("orta", _draw_2x(sp_o), derinlik=1.0),
        Oge("tekne_anim", ciz_tekne, derinlik=1.0),
        Oge("sis_anim", ciz_sis, derinlik=1.0),
        Oge("sahne", _draw_2x(sp_s), derinlik=1.0),
        Oge("tuzak_anim", ciz_tuzak, derinlik=1.0),
        Oge("plan", _draw_scan_2x(sp_p, ck.k("panama"), 0.70, dy=-26.0), derinlik=1.0),
        Oge("onplan", _draw_2x(sp_f), derinlik=1.0),
        Oge("fx_407", ciz_fx, derinlik=1.0),
    )
    ck.kamera = Kamera(
        x=Iz([(0, W / 2 - 20), (4.8, W / 2 + 20, "io")]),
        z=Iz([(0, 1.01), (4.8, 1.05, "in")]),
        sarsinti=[(2.75, 0.22, 12)],
    )
    ck.ust.append(_hud("4.07", "You sail to Panama for freedom. Instead, the Company's trap closes around you.",
                       lambda t: "trap" if t >= 2.75 else ("freedom" if t >= 1.65 else ("panama" if t >= 0.35 else ""))))
    return ck


# --------- 4.08 Sona's Iron Gate (ACT V OPEN LOOP — Massive Iron Doors Physically SLAM SHUT!)
def build_408():
    kw = [("sara", 0.35, 1.25), ("fall", 1.45, 2.35), ("shut", 2.85, 4.55)]
    ck = Cekim("4.08", sure=5.0, kelimeler=kw, duygu=Duygu("korku").gecis("yas", t0=2.85, sure=0.8), arka="#241E14")
    sp_u = _sp_layer(set_408_sona_kapisi, ["uzak"])
    sp_o = _sp_layer(set_408_sona_kapisi, ["orta"])
    sp_s = _sp_layer(set_408_sona_kapisi, ["sahne"])
    sp_sol = _sp_layer(set_408_sona_kapisi, ["kapi_sol"])
    sp_sag = _sp_layer(set_408_sona_kapisi, ["kapi_sag"])
    sp_p = _sp_layer(set_408_sona_kapisi, ["plan"])
    sp_f = _sp_layer(set_408_sona_kapisi, ["onplan"])

    def ciz_kapilar(c, t, o):
        # Two massive rusted iron gate doors physically swing & SLAM SHUT (+122px / -122px x 2.02) at 'shut' (t=2.55 -> 3.15s)!
        # Leaving a 4px scorching sunlit slit at x=0 (Act V Open Loop!)
        slam = ease("in", clamp((t - 2.45) / 0.65))
        shift = 122.0 * 2.02 * slam
        c.save()
        c.translate(shift, 0)
        c.scale(2.02, 2.02); draw_sprite(c, sp_sol)
        c.restore()
        c.save()
        c.translate(-shift, 0)
        c.scale(2.02, 2.02); draw_sprite(c, sp_sag)
        c.restore()
        # Dust shockwave + vertical scorching sunlight slit flash right on impact (t=3.10s)!
        if 3.05 <= t <= 3.75:
            dp = (t - 3.05) / 0.70
            c.drawRect(skia.Rect(-5, -H / 2, 5, H / 2), paint("#FFF5C8", 0.85 * (1.0 - dp)))
            for k in range(8):
                px = (k - 3.5) * 90 * (0.4 + dp)
                py = 360 - dp * 90 + math.sin(k * 1.9) * 28
                c.drawCircle(px, py, 24 + 34 * dp, paint("#C2AD88", 0.34 * (1.0 - dp)))

    def ciz_fx(c, t, o):
        # Blistering yellow-grey desert heat haze + blowing dust
        for i in range(18):
            dx = -900 + ((i * 113 + t * 185) % 1800)
            dy = -360 + ((i * 79 + math.sin(t * 3 + i) * 18) % 780)
            c.drawCircle(dx, dy, 3.2, paint("#E8D4A2", 0.32))

    ck.ekle(
        Oge("uzak", _draw_2x(sp_u), derinlik=0.65),
        Oge("orta", _draw_2x(sp_o), derinlik=1.0),
        Oge("sahne", _draw_2x(sp_s), derinlik=1.0),
        Oge("kapilar_anim", ciz_kapilar, derinlik=1.0),
        Oge("plan", _draw_scan_2x(sp_p, ck.k("shut", 0.20), 0.55, dy=-94.0), derinlik=1.0),
        Oge("onplan", _draw_2x(sp_f), derinlik=1.0),
        Oge("fx_408", ciz_fx, derinlik=1.0),
    )
    ck.kamera = Kamera(
        z=Iz([(0, 1.01), (3.0, 1.05, "in"), (3.2, 1.03, "out"), (5.0, 1.05, "in")]),
        sarsinti=[(3.10, 0.34, 24)],
    )
    ck.ust.append(_hud("4.08", "To save Sara, you take the fall. Behind you, the gates of Sona slam shut.",
                       lambda t: "shut" if t >= 2.85 else ("fall" if t >= 1.45 else ("sara" if t >= 0.35 else ""))))
    return ck


def build_film():
    c = [
        build_401(), build_402(), build_403(), build_404(),
        build_405(), build_406(), build_407(), build_408(),
    ]
    return Film([
        c[0], ZoomIcinden("harita_igne", sure=0.55, renk=KIRMIZI),
        c[1], Savurma(yon=1, sure=0.45),
        c[2], Maske("sifre_kod", boyut=(340, 340), sure=0.65),
        c[3], OnPlanSil(ciz_perde_sil, sure=0.55),
        c[4], Eslesme("dusen_saat", "gazete_muhur", sure=0.60),
        c[5], ZoomIcinden("af_imza", sure=0.55, renk=KIRMIZI),
        c[6], Savurma(yon=1, sure=0.45),
        c[7],
    ])


def kontakt_olustur(film, kare_klasor, out_png):
    bas = film.bas
    anlar = [
        ("4.01 Mahone FBI Desk & Pin",       bas[0] + 3.45),
        ("4.02 Highway & Flying Aliases",    bas[1] + 3.35),
        ("4.03a Folded Turna v4",            bas[2] + 0.90),
        ("4.03b Unfolded Cipher (GILA NM)",  bas[2] + 3.35),
        ("4.04 Motel Reunion & Bandage",     bas[3] + 3.35),
        ("4.05a Father Dusk Silhouettes",    bas[4] + 1.15),
        ("4.05b Empty Chair & 06:14 Watch",  bas[4] + 3.75),
        ("4.06 STEADMAN ALIVE -> REVOKED",   bas[5] + 3.65),
        ("4.07 Panama Boat & Company Trap",  bas[6] + 3.45),
        ("TRANS 7 Whip -> Sona Gates",       bas[7] + 0.15),
        ("4.08a Sona Gates Open (Michael)",  bas[7] + 1.65),
        ("4.08b Sona Gates SLAM SHUT (4px)", bas[7] + 3.85),
    ]
    pngler = film.onizle([t for _, t in anlar], str(kare_klasor), olcek=0.5)
    cols, rows, tw, th, pad, top = 4, 3, 440, 248, 14, 54
    sheet = Image.new("RGB", (cols * tw + (cols + 1) * pad, top + rows * (th + 26) + pad), (10, 14, 22))
    draw = ImageDraw.Draw(sheet)
    ft = ImageFont.truetype(str(REPO / "fonts/AlegreyaSC-Bold.ttf"), 21)
    fl = ImageFont.truetype(str(REPO / "fonts/Alegreya.ttf"), 15)
    draw.text((pad, 14), f"ACT IV ('ON THE RUN') F4b EN - LIVE ACTION (R18-HAREKET) · {film.sure:.1f}s · 7/7 Semantic", fill=(127, 230, 255), font=ft)
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
    print(f"Act IV EN kuruldu: {len(film.cekimler)} cekim, toplam {film.sure:.2f} sn", flush=True)
    kontakt_png = P / "bolum4_en_kontakt_960.png"
    kontakt_olustur(film, P / "kareler_b4_en", kontakt_png)
    print("Kontakt Act IV EN tamam:", kontakt_png, flush=True)
    mp4 = P / "bolum4_en_960.mp4"
    render_taslak_960(film, mp4, fps=16, crf=24)
    print("MP4 Act IV EN tamam:", mp4, flush=True)
