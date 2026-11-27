"""Act IV ('On the Run') F4b v2 EN — R19-CANLI-DUNYA DYNAMIC CHARACTER & MULTI-BEAT STORYTELLING.

Zero slideshow, zero frozen mannequins. Every shot tells its story VISUALLY with 2-3 live beats:
  - 4.01: Dark office -> FBI lamp snaps ON + scanning reticle on A-Sirt v1 -> live red strings shoot point-to-point -> 5-finger hand slams pin on UTAH with crimson shockwave!
  - 4.02: High-speed night chase! Racing 3D perspective road stripes + physically sweeping windshield wipers + flashing red/blue police lightbar across dash + 3 spinning fake IDs!
  - 4.03: Warm lamp sweeps open doctor bag -> Turna v4 lifts, rotates & physically unfolds -> glowing cyan dot-to-dot cipher route draws live across the fold grid!
  - 4.04: Living motel reunion! Running window rain + buzzing MOTEL neon + Michael & Sara visibly breathing/leaning + live wrapping white bandage coil around Michael's wrist!
  - 4.05: Pure visual emotion (0 violence)! Swaying sunset silhouettes -> dramatic cold shadow wave erases father into wind dust -> camera drops tracking brass watch falling, bouncing & cracking at 06:14!
  - 4.06: Kinetic montage! STEADMAN ALIVE! newspaper spins & slams with camera flash -> whip-pan to pardon as golden signature burns away into smoke -> crimson PARDON REVOKED slams with ink shock!
  - 4.07: Dynamic Panama ambush! Rolling emerald water reflections + drifting mist + CHRISTINA ROSE sailing/pitching -> police searchlight cones sweep the water + rotating crimson trap rings tighten!
  - 4.08: Epic Sona climax! Shimmering heat waves + Michael PHYSICALLY WALKS forward into Sona courtyard -> massive rusted iron doors accelerate & SLAM SHUT with steel lock-bar + dust shockwave + 4px sunlight beam!
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


# --------- 4.01 Mahone's FBI Desk (3 Beats: Lamp Snap ON -> Live Red Laser Threads -> Hand Pin Slam!)
def build_401():
    kw = [("genius", 0.35, 1.25), ("tattoo", 1.55, 2.55), ("map", 2.95, 4.25)]
    ck = Cekim("4.01", sure=4.8, kelimeler=kw, duygu=Duygu("gerilim").gecis("korku", t0=2.95, sure=0.8), arka="#070A10")
    sp_u = _sp_layer(set_401_fbi_masasi, ["uzak"])
    sp_base = _sp_layer(set_401_fbi_masasi, ["orta", "sahne"])
    sp_ip = _sp_layer(set_401_fbi_masasi, ["kirmizi_ip"])
    sp_igne = _sp_layer(set_401_fbi_masasi, ["harita_igne"])
    sp_p = _sp_layer(set_401_fbi_masasi, ["plan"])
    sp_f = _sp_layer(set_401_fbi_masasi, ["onplan"])

    def ciz_ip(c, t, o):
        # Beat 2 (1.35 -> 2.65s): Red investigation strings shoot across corkboard with glowing leading tip!
        p = ease("io", clamp((t - 1.30) / 1.25))
        if p <= 0.01:
            return
        sx = -W / 2 + W * p
        c.save()
        c.clipRect(skia.Rect(-W / 2, -H / 2, sx, H / 2))
        c.scale(2.02, 2.02); draw_sprite(c, sp_ip)
        c.restore()
        # Live animated tracking dot racing from tattoo photo (-430, -140) to UTAH (240, -70)
        if p < 0.98:
            tx = -430 + 670 * p
            ty = -140 + 70 * p
            c.drawCircle(tx, ty, 11, paint(KIRMIZI, 0.9))
            c.drawCircle(tx, ty, 24, paint(KIRMIZI, 0.35))

    def ciz_igne(c, t, o):
        # Beat 3 (2.60 -> 3.05s): Refined 5-finger FBI hand physically lunges in & SLAMS red pin into UTAH!
        p = ease("in", clamp((t - 2.60) / 0.42))
        if p <= 0.01:
            return
        dx = 340.0 * (1.0 - p)
        dy = -210.0 * (1.0 - p)
        # tiny settle press right after pin hits
        press = math.sin(clamp((t - 3.02) / 0.25) * math.pi) * 6.0 if t > 3.02 else 0.0
        c.save()
        c.translate(dx - press, dy + press)
        c.scale(2.02, 2.02); draw_sprite(c, sp_igne)
        c.restore()
        # Expanding crimson shockwave rings on impact!
        if t >= 3.02:
            for k in range(2):
                rp = clamp((t - 3.02 - k * 0.14) / 0.55)
                if 0 < rp < 1:
                    c.drawCircle(240, -70, 22 + 125 * rp, paint(KIRMIZI, 0.80 * (1.0 - rp), Style=skia.Paint.kStroke_Style, StrokeWidth=4))

    def ciz_fx(c, t, o):
        # Beat 1 (0.0 -> 0.45s): Office starts dark -> FBI lamp PHYSICALLY CLICKS ON with warm flash!
        dark = 0.62 * (1.0 - ease("out", clamp((t - 0.15) / 0.32)))
        if dark > 0.01:
            c.drawRect(skia.Rect(-W / 2, -H / 2, W / 2, H / 2), paint("#030508", dark))
        if 0.18 <= t <= 0.48:
            fl = 0.28 * (1.0 - (t - 0.18) / 0.30)
            c.drawCircle(-560, 100, 520, paint("#FFF0C2", fl))
        # Scanning reticle sweeping over A-Sirt v1 polaroid during 'genius' (0.45 -> 1.65s)
        if 0.45 <= t <= 1.85:
            sp = ease("io", (t - 0.45) / 1.40)
            ry = -280 + 250 * sp
            c.drawLine(-640, ry, -260, ry, paint(PLAN_C, 0.85, Style=skia.Paint.kStroke_Style, StrokeWidth=3))
            c.drawCircle(-450, ry, 18, paint(PLAN_C, 0.45, Style=skia.Paint.kStroke_Style, StrokeWidth=2))
        # Crimson takeover wash after 'map' pin slam
        if t >= 3.05:
            rw = ease("out", clamp((t - 3.05) / 0.65))
            c.drawRect(skia.Rect(-W / 2, -H / 2, W / 2, H / 2), paint(KIRMIZI, 0.09 * rw))

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
    # 2-stage dynamic camera: starts on A-Sirt polaroid (left), whips across to US map (right) as pin slams!
    ck.kamera = Kamera(
        x=Iz([(0, W / 2 - 95), (1.4, W / 2 - 70, "io"), (3.0, W / 2 + 75, "io"), (4.8, W / 2 + 85, "in")]),
        y=Iz([(0, H / 2 - 15), (4.8, H / 2 - 20, "io")]),
        z=Iz([(0, 1.08), (1.4, 1.04, "out"), (3.05, 1.10, "in"), (4.8, 1.12, "in")]),
        sarsinti=[(3.04, 0.28, 18)],
    )
    ck.ust.append(_hud("4.01", "Now an FBI genius studies your tattoo. Someone else is reading the map.",
                       lambda t: "map" if t >= 2.95 else ("tattoo" if t >= 1.55 else ("genius" if t >= 0.35 else ""))))
    return ck


# --------- 4.02 Night Highway Chase (Racing Road Stripes + Live Wipers + Sirens + Flying IDs!)
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
            p = ease("out", clamp((t - t0) / 0.38))
            if p <= 0.01:
                return
            dx = from_dx * (1.0 - p)
            dy = from_dy * (1.0 - p) + math.sin(t * 5.0 + t0) * 5.0 * p
            rot = from_rot * (1.0 - p)
            sc = 1.25 - 0.25 * p
            c.save()
            c.translate(dx, dy); c.rotate(rot); c.scale(sc, sc)
            c.scale(2.02, 2.02); draw_sprite(c, sp)
            c.restore()
        return _ciz

    def ciz_road_action(c, t, o):
        # 1. Racing 3D perspective yellow highway dashes rushing toward camera!
        for k in range(6):
            z = ((t * 2.2 + k / 6.0) % 1.0)
            y0 = -40 + z * z * 420
            y1 = -40 + min(1.0, (z + 0.10)) ** 2 * 420
            w = 4 + z * 16
            c.drawLine(0, y0, 0, y1, paint("#F5C469", 0.78 * z, Style=skia.Paint.kStroke_Style, StrokeWidth=w))
        # 2. Physically sweeping windshield wiper blade clearing rain!
        w_ang = -58.0 + 116.0 * (0.5 + 0.5 * math.sin(t * 5.2))
        c.save()
        c.translate(-120, 390); c.rotate(w_ang)
        c.drawLine(0, 0, 0, -560, paint("#0D131C", 0.72, Style=skia.Paint.kStroke_Style, StrokeWidth=10, StrokeCap=skia.Paint.kRound_Cap))
        c.restore()
        # 3. Diagonal speeding rain streaks + oncoming headlight flashes
        for i in range(32):
            rx = -880 + ((i * 71 + int(t * 150)) % 1760)
            ry = -460 + ((i * 83 + t * 680) % 920)
            c.drawLine(rx, ry, rx - 10, ry + 32, paint("#A8D4F5", 0.35, Style=skia.Paint.kStroke_Style, StrokeWidth=2.2))
        # 4. Flashing red/blue police siren wash pulsing across ENTIRE windshield & rearview mirror!
        sr = (0.14 if t < 2.6 else 0.28) * (0.5 + 0.5 * math.sin(t * 17.0))
        sb = (0.14 if t < 2.6 else 0.28) * (0.5 - 0.5 * math.sin(t * 17.0))
        c.drawCircle(-140, -320, 260, paint(KIRMIZI, sr))
        c.drawCircle(140, -320, 260, paint("#3B82F6", sb))
        c.drawRect(skia.Rect(-W / 2, -H / 2, W / 2, H / 2), paint(KIRMIZI, sr * 0.22))
        c.drawRect(skia.Rect(-W / 2, -H / 2, W / 2, H / 2), paint("#3B82F6", sb * 0.22))

    ck.ekle(
        Oge("uzak", _draw_2x(sp_u), derinlik=0.65),
        Oge("orta", _draw_2x(sp_o), derinlik=1.0),
        Oge("road_action", ciz_road_action, derinlik=1.0),
        Oge("kart1_anim", _fly_card(sp_k1, 0.50, -580, 260, -28), derinlik=1.0),
        Oge("kart2_anim", _fly_card(sp_k2, 1.30, 0, 460, 18), derinlik=1.0),
        Oge("kart3_anim", _fly_card(sp_k3, 2.05, 580, 260, 26), derinlik=1.0),
        Oge("sahne", _draw_2x(sp_s), derinlik=1.0),
        Oge("plan", _draw_scan_2x(sp_p, ck.k("trap", -0.25), 0.65, dy=-82.0), derinlik=1.0),
        Oge("onplan", _draw_2x(sp_f), derinlik=1.0),
    )
    # Energetic road-chase vibration + sway!
    ck.kamera = Kamera(
        x=Iz([(0, W / 2 - 35), (1.5, W / 2 + 30, "io"), (3.1, W / 2 - 20, "io"), (4.6, W / 2 + 10, "out")]),
        y=Iz([(0, H / 2 + 6), (2.3, H / 2 - 8, "io"), (4.6, H / 2 + 4, "io")]),
        z=Iz([(0, 1.03), (4.6, 1.08, "in")]),
        sarsinti=[(0.50, 0.16, 12), (1.30, 0.16, 12), (2.05, 0.18, 14), (3.15, 0.25, 16)],
    )
    ck.ust.append(_hud("4.02", "New city, new name: Michael Crane. Every road ahead is a trap.",
                       lambda t: "trap" if t >= 3.15 else ("name" if t >= 1.15 else ("city" if t >= 0.30 else ""))))
    return ck


# --------- 4.03 Sara's Coded Crane (Turna Lifts, Rotates & Unfolds -> Live Cyan Dot-to-Dot Cipher!)
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
        # Beat 1 (0.0->1.30s): Locked Turna v4 gently hovers & tilts over the warm table
        # Beat 2 (1.30->2.45s): Turna v4 physically lifts, rotates & unfolds into the creased cipher sheet with crease flash!
        u = ease("io", clamp((t - 1.30) / 1.10))
        if u > 0.02:
            sc_p = 0.55 + 0.45 * u
            rot_p = -14.0 * (1.0 - u)
            c.saveLayerAlpha(None, int(255 * clamp(u * 1.25)))
            c.rotate(rot_p); c.scale(sc_p, sc_p)
            c.scale(2.02, 2.02); draw_sprite(c, sp_acik)
            c.restore()
        if u < 0.98:
            hover_y = math.sin(t * 3.5) * 6.0 - 28.0 * u
            rot_k = 18.0 * u
            sc_k = 1.0 + 0.22 * u
            c.saveLayerAlpha(None, int(255 * clamp(1.0 - u)))
            c.translate(0, hover_y); c.rotate(rot_k); c.scale(sc_k, sc_k)
            c.scale(2.02, 2.02); draw_sprite(c, sp_kapali)
            c.restore()
        # Beat 3 (2.55->4.5s): Live glowing cyan dot-to-dot cipher route drawing across the unfolded grid!
        if t >= 2.55:
            cp = ease("io", clamp((t - 2.55) / 1.35))
            pts = [(-220, -140), (0, -20), (210, -120), (140, 140), (-160, 110)]
            for i in range(len(pts) - 1):
                seg_p = clamp(cp * (len(pts) - 1) - i)
                if seg_p > 0:
                    x0, y0 = pts[i]; x1, y1 = pts[i + 1]
                    mx, my = x0 + (x1 - x0) * seg_p, y0 + (y1 - y0) * seg_p
                    c.drawLine(x0, y0, mx, my, paint(PLAN_C, 0.88, Style=skia.Paint.kStroke_Style, StrokeWidth=3.5))
                    c.drawCircle(x0, y0, 7, paint(PLAN_C, 0.95))
                    if seg_p >= 0.98:
                        c.drawCircle(x1, y1, 8, paint(PLAN_C, 0.95))

    def ciz_fx(c, t, o):
        for i in range(16):
            mx = -680 + ((i * 97 + t * 22) % 1360)
            my = -320 + ((i * 71 - t * 18) % 620)
            c.drawCircle(mx, my, 2.8, paint(ALTIN, 0.34 + 0.16 * math.sin(t * 3.0 + i)))

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
        z=Iz([(0, 1.02), (1.3, 1.08, "io"), (2.6, 1.03, "out"), (4.8, 1.09, "in")]),
    )
    ck.ust.append(_hud("4.03", "Inside Sara's bag, a paper crane unfolds. Hidden numbers mark a rendezvous.",
                       lambda t: "numbers" if t >= 2.65 else ("unfolds" if t >= 1.35 else ("crane" if t >= 0.35 else ""))))
    return ck


# --------- 4.04 Living Motel Reunion (Breathing/Leaning Characters + Live Wrapping Bandage + Rain/Neon!)
def build_404():
    kw = [("waiting", 0.35, 1.35), ("bandages", 1.75, 3.05), ("stay", 3.35, 4.35)]
    ck = Cekim("4.04", sure=4.8, kelimeler=kw, duygu=Duygu("huzur").gecis("umut", t0=3.35, sure=0.8), arka="#16100C")
    sp_u = _sp_layer(set_404_motel_bulusma, ["uzak"])
    sp_o = _sp_layer(set_404_motel_bulusma, ["orta"])
    sp_s = _sp_layer(set_404_motel_bulusma, ["sahne"])
    sp_ban = _sp_layer(set_404_motel_bulusma, ["bandaj_sar"])
    sp_p = _sp_layer(set_404_motel_bulusma, ["plan"])
    sp_f = _sp_layer(set_404_motel_bulusma, ["onplan"])

    def ciz_characters_alive(c, t, o):
        # Living subtle breathing + gentle leaning forward together during 'bandages' & 'stay'!
        breath_y = math.sin(t * 2.4) * 4.5
        lean_sc = 1.0 + 0.014 * ease("io", clamp((t - 1.40) / 1.80))
        c.save()
        c.translate(0, breath_y)
        c.scale(lean_sc, lean_sc)
        c.scale(2.02, 2.02); draw_sprite(c, sp_s)
        c.restore()

    def ciz_bandaj(c, t, o):
        # Clean white bandage visibly wraps loop-by-loop around Michael's wrist with subtle motion!
        p = ease("io", clamp((t - 1.45) / 1.45))
        if p <= 0.01:
            return
        breath_y = math.sin(t * 2.4) * 4.5
        sx = -W / 2 + W * (0.36 + 0.34 * p)
        c.save()
        c.translate(0, breath_y)
        c.clipRect(skia.Rect(-W / 2, -H / 2, sx, H / 2))
        c.scale(2.02, 2.02); draw_sprite(c, sp_ban)
        c.restore()
        # Subtle warm highlight pulse on the wrapping gauze as Sara finishes
        if 1.50 <= t <= 3.10:
            ang = math.sin(t * 9.0) * 12.0
            c.drawCircle(-20 + ang, 165 + breath_y, 26, paint("#FFF8E8", 0.25 * math.sin(p * math.pi)))

    def ciz_fx(c, t, o):
        # Running rain streaks on the motel window + flickering red MOTEL neon wash + warm amber embrace!
        for i in range(18):
            rx = -340 + (i * 41) % 680
            ry = -440 + ((i * 59 + t * 340) % 420)
            c.drawLine(rx, ry, rx - 3, ry + 24, paint("#B4D4EC", 0.30, Style=skia.Paint.kStroke_Style, StrokeWidth=2))
        nf = 0.08 + 0.06 * (1.0 if math.sin(t * 22.0) > -0.6 else 0.15)
        c.drawCircle(-30, -240, 320, paint("#FF5A40", nf))
        # Warm amber hope glow rising at 'stay'
        if t >= 3.20:
            wp = ease("out", clamp((t - 3.20) / 1.10))
            c.drawCircle(0, 80, 620, paint(ALTIN, 0.12 * wp))

    ck.ekle(
        Oge("uzak", _draw_2x(sp_u), derinlik=0.65),
        Oge("orta", _draw_2x(sp_o), derinlik=1.0),
        Oge("sahne_alive", ciz_characters_alive, derinlik=1.0),
        Oge("bandaj_anim", ciz_bandaj, derinlik=1.0),
        Oge("plan", _draw_scan_2x(sp_p, ck.k("stay", -0.25), 0.65), derinlik=1.0),
        Oge("onplan", _draw_2x(sp_f), derinlik=1.0),
        Oge("fx_404", ciz_fx, derinlik=1.0),
    )
    # Intimate 2-stage push-in: establishing room -> close on hands & faces as Sara chooses to stay
    ck.kamera = Kamera(
        y=Iz([(0, H / 2 - 15), (2.2, H / 2 + 25, "io"), (4.8, H / 2 - 5, "io")]),
        z=Iz([(0, 1.01), (2.2, 1.09, "io"), (4.8, 1.07, "out")]),
    )
    ck.ust.append(_hud("4.04", "You find Sara waiting in the dark. She bandages your hand - and chooses to stay.",
                       lambda t: "stay" if t >= 3.35 else ("bandages" if t >= 1.75 else ("waiting" if t >= 0.35 else ""))))
    return ck


def ciz_perde_sil(c, u):
    c.drawRect(skia.Rect(-140, 0, 140, H), paint("#231A16"))
    for x in range(-110, 120, 38):
        c.drawLine(x, 0, x, H, paint("#120D0A", 0.65, Style=skia.Paint.kStroke_Style, StrokeWidth=10))


# --------- 4.05 The Father's Watch (ZERO VIOLENCE: Swaying Silhouettes -> Cold Shadow Sweep -> Falling/Bouncing Watch 06:14!)
def build_405():
    kw = [("father", 0.35, 1.55), ("shadows", 1.85, 2.75), ("watch", 3.05, 4.65)]
    ck = Cekim("4.05", sure=5.2, kelimeler=kw, duygu=Duygu("umut").gecis("yas", t0=2.55, sure=0.9), arka="#1B130B")
    sp_u = _sp_layer(set_405_baba_saati, ["uzak"])
    sp_o = _sp_layer(set_405_baba_saati, ["orta", "sahne"])
    sp_golge = _sp_layer(set_405_baba_saati, ["baba_golge"])
    sp_saat = _sp_layer(set_405_baba_saati, ["dusen_saat"])
    sp_p = _sp_layer(set_405_baba_saati, ["plan"])
    sp_f = _sp_layer(set_405_baba_saati, ["onplan"])

    def ciz_golge(c, t, o):
        # Beat 1 (0->1.8s): Two warm silhouettes gently breathe/sway together in golden sunset
        # Beat 2 (1.8->2.7s): Father silhouette drifts away into wind as cold shadow sweeps across!
        fade = 1.0 - ease("io", clamp((t - 1.75) / 0.95))
        if fade <= 0.01:
            return
        sway_x = math.sin(t * 1.8) * 6.0 - (1.0 - fade) * 45.0
        c.saveLayerAlpha(None, int(255 * fade))
        c.translate(sway_x, math.sin(t * 2.6) * 3.0)
        c.scale(2.02, 2.02); draw_sprite(c, sp_golge)
        c.restore()

    def ciz_saat(c, t, o):
        # Beat 3 (2.45->3.35s): Brass pocket watch PHYSICALLY FALLS, BOUNCES ONCE, & SWINGS to a halt at 06:14!
        if t < 2.45:
            return
        ft = t - 2.45
        if ft < 0.50:
            # accelerating drop
            p = ft / 0.50
            dy = -420.0 * (1.0 - p * p)
        elif ft < 0.78:
            # crisp physical bounce!
            bp = (ft - 0.50) / 0.28
            dy = -55.0 * math.sin(bp * math.pi)
        else:
            dy = 0.0
        sw_t = max(0.0, ft - 0.50)
        ang = math.sin(sw_t * 11.0) * 18.0 * math.exp(-sw_t * 2.0)
        c.save()
        c.translate(0, 80 + dy)
        c.rotate(ang)
        c.translate(0, -80)
        c.scale(2.02, 2.02); draw_sprite(c, sp_saat)
        c.restore()
        # Subtle dust puff + crystal glint right on watch impact!
        if 2.95 <= t <= 3.55:
            ip = (t - 2.95) / 0.60
            c.drawCircle(0, 145, 25 + 65 * ip, paint("#E8D4A2", 0.45 * (1.0 - ip), Style=skia.Paint.kStroke_Style, StrokeWidth=3))

    def ciz_fx(c, t, o):
        # Dramatic cold shadow wall sweeping left-to-right across the porch at 'shadows'
        if 1.65 <= t <= 2.90:
            sp = ease("io", (t - 1.65) / 1.25)
            sx = -W + W * 2.2 * sp
            c.drawRect(skia.Rect(sx - 380, -H / 2, sx + 380, H / 2), paint("#060A12", 0.52 * math.sin(sp * math.pi)))
        # Cold grief desaturation veil settling after the watch lands
        if t >= 2.75:
            gp = ease("out", clamp((t - 2.75) / 0.90))
            c.drawRect(skia.Rect(-W / 2, -H / 2, W / 2, H / 2), paint("#101722", 0.34 * gp))

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
    # Camera drops vertically following the falling watch!
    ck.kamera = Kamera(
        y=Iz([(0, H / 2 - 45), (2.4, H / 2 - 20, "io"), (3.1, H / 2 + 45, "out"), (5.2, H / 2 + 55, "in")]),
        z=Iz([(0, 1.02), (2.4, 1.05, "io"), (3.2, 1.12, "out"), (5.2, 1.15, "in")]),
        sarsinti=[(2.96, 0.18, 11)],
    )
    ck.ust.append(_hud("4.05", "Your father returns to save you from the shadows. Seconds later, only his watch remains.",
                       lambda t: "watch" if t >= 3.05 else ("shadows" if t >= 1.85 else ("father" if t >= 0.35 else ""))))
    return ck


# --------- 4.06 Conspiracy Headlines (Fast Spin Slam -> Whip-Pan -> Burning/Vanishing Signature -> REVOKED Impact!)
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
        # Beat 2 (2.45 -> 3.30s): Golden signature physically erases left-to-right into rising smoke wisps!
        erase = ease("in", clamp((t - 2.45) / 0.85))
        if erase >= 0.99:
            return
        ex = -640 + 480 * erase
        c.save()
        c.clipRect(skia.Rect(ex, -H / 2, W / 2, H / 2))
        c.scale(2.02, 2.02); draw_sprite(c, sp_imza)
        c.restore()
        if 0.02 < erase < 0.98:
            c.drawCircle(ex, 275, 22, paint(ALTIN, 0.72))
            c.drawCircle(ex + 10, 255 - erase * 35, 18, paint("#D8DCE2", 0.35))

    def ciz_gazete(c, t, o):
        # Beat 1 (0.15 -> 0.70s): STEADMAN ALIVE! spins 540 deg & slams onto desk with camera flash!
        p = ease("out", clamp((t - 0.15) / 0.52))
        if p <= 0.01:
            return
        ang = -540.0 * (1.0 - p)
        sc = 1.60 - 0.60 * p
        c.save()
        c.translate(0, 80); c.rotate(ang); c.scale(sc, sc); c.translate(0, -80)
        c.scale(2.02, 2.02); draw_sprite(c, sp_gaz)
        c.restore()

    def ciz_revoked(c, t, o):
        # Beat 3 (3.15s): Crimson PARDON REVOKED slams down with heavy 3D scale-bounce & red flash!
        if t < 3.15:
            return
        p = ease("out", clamp((t - 3.15) / 0.20))
        sc = 1.85 - 0.85 * p
        c.saveLayerAlpha(None, int(255 * clamp(p * 1.5)))
        c.translate(-420, 40); c.scale(sc, sc); c.translate(420, -40)
        c.scale(2.02, 2.02); draw_sprite(c, sp_rev)
        c.restore()
        if 3.15 <= t <= 3.45:
            fp = 1.0 - (t - 3.15) / 0.30
            c.drawRect(skia.Rect(-W / 2, -H / 2, W / 2, H / 2), paint(KIRMIZI, 0.22 * fp))

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
    # Dynamic 2-stage camera: punches on right newspaper -> whips left to vanishing pardon signature!
    ck.kamera = Kamera(
        x=Iz([(0, W / 2 + 75), (1.5, W / 2 + 60, "io"), (2.3, W / 2 - 80, "io"), (4.8, W / 2 - 90, "in")]),
        z=Iz([(0, 1.04), (0.75, 1.09, "out"), (2.3, 1.06, "io"), (3.25, 1.12, "in"), (4.8, 1.10, "out")]),
        sarsinti=[(0.67, 0.20, 14), (3.18, 0.30, 22)],
    )
    ck.ust.append(_hud("4.06", "You prove the murder was faked. Then the presidential pardon vanishes from the page.",
                       lambda t: "vanishes" if t >= 2.95 else ("pardon" if t >= 1.85 else ("faked" if t >= 0.35 else ""))))
    return ck


# --------- 4.07 Panama Boat & Ambush (Sailing Boat + Sweeping Police Searchlights + Contracting Trap Rings!)
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
        # CHRISTINA ROSE actively sails & pitches across emerald waves!
        bob_y = math.sin(t * 3.2) * 14.0
        tilt = math.sin(t * 2.5 + 0.4) * 2.6
        glide_x = -80.0 + 150.0 * ease("io", clamp(t / 4.6))
        c.save()
        c.translate(glide_x, bob_y); c.rotate(tilt)
        c.scale(2.02, 2.02); draw_sprite(c, sp_tekne)
        c.restore()

    def ciz_sis(c, t, o):
        dx = -90.0 + 180.0 * (t / 4.8)
        c.save()
        c.translate(dx, 0)
        c.scale(2.02, 2.02); draw_sprite(c, sp_sis)
        c.restore()

    def ciz_tuzak(c, t, o):
        # Rotating & contracting crimson Company trap rings snapping shut at 'trap' (t=2.55s)!
        if t < 2.55:
            return
        p = ease("out", clamp((t - 2.55) / 0.55))
        sc = 1.45 - 0.45 * p
        c.saveLayerAlpha(None, int(255 * clamp(p * 1.35)))
        c.scale(sc, sc)
        c.scale(2.02, 2.02); draw_sprite(c, sp_tuzak)
        c.restore()

    def ciz_fx(c, t, o):
        # Shimmering emerald harbor water ripples
        for k in range(10):
            wx = -700 + ((k * 165 + int(t * 55)) % 1400)
            wy = 90 + (k % 4) * 55
            c.drawLine(wx, wy, wx + 85, wy, paint("#A2E8DC", 0.22, Style=skia.Paint.kStroke_Style, StrokeWidth=3))
        # Sweeping police searchlight cones + strobing sirens converging on the boat at 'trap'!
        if t >= 2.40:
            tp = ease("out", clamp((t - 2.40) / 0.50))
            ang = -12.0 + math.sin(t * 4.5) * 16.0
            c.save()
            c.translate(-640, -60); c.rotate(ang)
            path = skia.Path()
            path.moveTo(0, 0); path.lineTo(950, -90); path.lineTo(950, 140); path.close()
            c.drawPath(path, paint("#E0F6FF", 0.16 * tp))
            c.restore()
            sr = 0.28 * (0.5 + 0.5 * math.sin(t * 16.0))
            sb = 0.28 * (0.5 - 0.5 * math.sin(t * 16.0))
            c.drawCircle(-620, -40, 180, paint(KIRMIZI, sr * tp))
            c.drawCircle(-500, -40, 180, paint("#3B82F6", sb * tp))

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
        x=Iz([(0, W / 2 - 40), (2.4, W / 2 + 10, "io"), (4.8, W / 2 + 45, "in")]),
        z=Iz([(0, 1.02), (2.4, 1.05, "io"), (4.8, 1.09, "in")]),
        sarsinti=[(2.65, 0.24, 14)],
    )
    ck.ust.append(_hud("4.07", "You sail to Panama for freedom. Instead, the Company's trap closes around you.",
                       lambda t: "trap" if t >= 2.75 else ("freedom" if t >= 1.65 else ("panama" if t >= 0.35 else ""))))
    return ck


# --------- 4.08 Sona Iron Gate (EPIC CLIMAX: Michael PHYSICALLY WALKS INTO SONA -> Massive Iron Doors SLAM SHUT!)
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

    def ciz_michael_walk(c, t, o):
        # Beat 1 (0.0 -> 2.75s): Michael PHYSICALLY WALKS FORWARD through the scorching archway into Sona!
        wp = ease("io", clamp(t / 2.85))
        stride_y = -abs(math.sin(t * 7.5)) * 10.0 * (1.0 - 0.5 * wp)
        walk_sc = 1.06 - 0.16 * wp  # stepping deeper into Sona's sunlit yard!
        walk_y = 26.0 - 44.0 * wp
        c.save()
        c.translate(0, walk_y + stride_y)
        c.scale(walk_sc, walk_sc)
        c.scale(2.02, 2.02); draw_sprite(c, sp_s)
        c.restore()

    def ciz_kapilar(c, t, o):
        # Beat 2 (2.40 -> 3.05s): Two massive rusted iron doors accelerate & SLAM SHUT (+122/-122px) leaving 4px sunlit slit!
        slam = ease("in", clamp((t - 2.40) / 0.62))
        shift = 122.0 * 2.02 * slam
        c.save()
        c.translate(shift, 0)
        c.scale(2.02, 2.02); draw_sprite(c, sp_sol)
        c.restore()
        c.save()
        c.translate(-shift, 0)
        c.scale(2.02, 2.02); draw_sprite(c, sp_sag)
        c.restore()
        # Blinding 4px vertical sunlight beam + steel dust explosion right on gate slam (t=3.02s)!
        if 3.00 <= t <= 4.10:
            dp = (t - 3.00) / 1.10
            c.drawRect(skia.Rect(-6, -H / 2, 6, H / 2), paint("#FFF5C8", 0.92 * (1.0 - 0.55 * dp)))
            for k in range(10):
                px = (k - 4.5) * 105 * (0.35 + dp)
                py = 360 - dp * 120 + math.sin(k * 1.9) * 32
                c.drawCircle(px, py, 28 + 42 * dp, paint("#C2AD88", 0.38 * (1.0 - dp)))

    def ciz_fx(c, t, o):
        # Blowing desert dust & blistering heat shimmer
        for i in range(22):
            dx = -900 + ((i * 113 + t * 230) % 1800)
            dy = -360 + ((i * 79 + math.sin(t * 3.5 + i) * 20) % 780)
            c.drawCircle(dx, dy, 3.6, paint("#E8D4A2", 0.36))

    ck.ekle(
        Oge("uzak", _draw_2x(sp_u), derinlik=0.65),
        Oge("orta", _draw_2x(sp_o), derinlik=1.0),
        Oge("michael_walk", ciz_michael_walk, derinlik=1.0),
        Oge("kapilar_anim", ciz_kapilar, derinlik=1.0),
        Oge("plan", _draw_scan_2x(sp_p, ck.k("shut", 0.20), 0.55, dy=-94.0), derinlik=1.0),
        Oge("onplan", _draw_2x(sp_f), derinlik=1.0),
        Oge("fx_408", ciz_fx, derinlik=1.0),
    )
    ck.kamera = Kamera(
        z=Iz([(0, 1.01), (2.4, 1.09, "in"), (3.05, 1.04, "out"), (5.0, 1.07, "in")]),
        sarsinti=[(3.03, 0.38, 28)],
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
        ("4.01 Mahone FBI Lamp & Pin Slam",  bas[0] + 3.25),
        ("4.02 Chase: Wipers, Road & IDs",   bas[1] + 3.25),
        ("4.03a Hovering Turna v4",          bas[2] + 0.85),
        ("4.03b Unfolded Live Cipher Route", bas[2] + 3.65),
        ("4.04 Living Motel & Bandage Wrap", bas[3] + 3.35),
        ("4.05a Dusk Silhouettes -> Shadow", bas[4] + 2.15),
        ("4.05b Watch Bounce & 06:14 Crack", bas[4] + 3.35),
        ("4.06 Vanishing Ink -> REVOKED",    bas[5] + 3.55),
        ("4.07 Panama Boat & Searchlights",  bas[6] + 3.45),
        ("TRANS 7 Whip -> Sona Gates",       bas[7] + 0.15),
        ("4.08a Michael Walks Into Sona",    bas[7] + 1.55),
        ("4.08b Iron Doors SLAM SHUT (4px)", bas[7] + 3.75),
    ]
    pngler = film.onizle([t for _, t in anlar], str(kare_klasor), olcek=0.5)
    cols, rows, tw, th, pad, top = 4, 3, 440, 248, 14, 54
    sheet = Image.new("RGB", (cols * tw + (cols + 1) * pad, top + rows * (th + 26) + pad), (10, 14, 22))
    draw = ImageDraw.Draw(sheet)
    ft = ImageFont.truetype(str(REPO / "fonts/AlegreyaSC-Bold.ttf"), 21)
    fl = ImageFont.truetype(str(REPO / "fonts/Alegreya.ttf"), 15)
    draw.text((pad, 14), f"ACT IV ('ON THE RUN') F4b v2 EN - R19-CANLI-DUNYA DYNAMIC ACTION · {film.sure:.1f}s · 7/7 Semantic", fill=(127, 230, 255), font=ft)
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
    print(f"Act IV v2 EN kuruldu: {len(film.cekimler)} cekim, toplam {film.sure:.2f} sn", flush=True)
    kontakt_png = P / "bolum4_en_kontakt_960.png"
    kontakt_olustur(film, P / "kareler_b4_en", kontakt_png)
    print("Kontakt Act IV v2 EN tamam:", kontakt_png, flush=True)
    mp4 = P / "bolum4_en_960.mp4"
    render_taslak_960(film, mp4, fps=16, crf=24)
    print("MP4 Act IV v2 EN tamam:", mp4, flush=True)
