"""A-M (F3 Ana Mekân Sanatçısı) — Sinematik 2D + Camgöbeği Plan Görüşü (Stil B + A hibrit).

İzole modül: ileride studyo/motor/ katmanlarına kolayca bölünebilir 3 ana mekân üretir:
  - mekan_depo(katmanlar=None, plan_gorusu=True)  -> (defs_svg, body_svg)
  - mekan_hucre(katmanlar=None, plan_gorusu=True) -> (defs_svg, body_svg)
  - mekan_revir(katmanlar=None, plan_gorusu=True) -> (defs_svg, body_svg)

Her mekân 960x540 (16:9) dahili koordinat sisteminde 5 ayrı derinlik katmanıyla üretilir:
  uzak, orta, sahne, plan, onplan.
"""
from __future__ import annotations

import io
import math
import random
from pathlib import Path
import resvg_py
from PIL import Image, ImageDraw, ImageFont

OUT_DIR = Path(__file__).resolve().parent
W_SCENE, H_SCENE = 960, 540

# Ortak Stil B + A Hibrit Sabitleri
INK = "#14181E"
INK_WARM = "#1C1511"
PLAN = "#7FE6FF"
PLAN_CORE = "#D8FAFF"

_UID = 0


def _uid(prefix: str = "m") -> str:
    global _UID
    _UID += 1
    return f"{prefix}_{_UID}"


def _katman_aktif(katmanlar: set[str] | list[str] | None, ad: str) -> bool:
    return katmanlar is None or ad in katmanlar


def _turna_svg(cx: float, cy: float, scale: float = 1.0, rot: float = 0.0,
               fill_light: str = "#F5ECDA", fill_mid: str = "#D7C9B0",
               fill_dark: str = "#9E8E76", stroke: str = "#221C18",
               rim: str = "") -> str:
    """Küçük origami kâğıt turna (tüm çizgi path'leri fill='none')."""
    rim_el = ""
    if rim:
        rim_el = (
            f'<path d="M-24,-6 L-6,-18 L12,-22 L28,-12 L10,-4" '
            f'fill="none" stroke="{rim}" stroke-width="1.4" opacity="0.85"/>'
        )
    return (
        f'<g transform="translate({cx:.1f},{cy:.1f}) rotate({rot:.1f}) scale({scale:.2f})">'
        # Zemin temas gölgesi
        f'<ellipse cx="2" cy="11" rx="20" ry="4.2" fill="#05080D" opacity="0.48"/>'
        # Arka kanat
        f'<polygon points="-4,-2 8,-22 26,-11 6,1" fill="{fill_dark}" stroke="{stroke}" stroke-width="1.1" stroke-linejoin="round"/>'
        # Gövde alt
        f'<polygon points="-16,2 0,-6 16,2 2,9" fill="{fill_mid}" stroke="{stroke}" stroke-width="1.2" stroke-linejoin="round"/>'
        # Boyun ve kafa
        f'<polygon points="-15,2 -24,-14 -20,-17 -11,-2" fill="{fill_light}" stroke="{stroke}" stroke-width="1.1" stroke-linejoin="round"/>'
        f'<polygon points="-24,-14 -31,-11 -21,-10" fill="{fill_mid}" stroke="{stroke}" stroke-width="1.0" stroke-linejoin="round"/>'
        # Kuyruk
        f'<polygon points="14,1 28,-12 20,2" fill="{fill_mid}" stroke="{stroke}" stroke-width="1.1" stroke-linejoin="round"/>'
        # Ön kanat (ışık alan yüzey)
        f'<polygon points="-8,1 -1,-18 17,-4 2,5" fill="{fill_light}" stroke="{stroke}" stroke-width="1.2" stroke-linejoin="round"/>'
        # Katlama izi
        f'<path d="M-1,-18 L2,5 M-16,2 L16,2" fill="none" stroke="{stroke}" stroke-width="0.7" opacity="0.55"/>'
        f'{rim_el}'
        f'</g>'
    )


# =============================================================================
# 1. KARANLIK DEPO (Prolog & Bölüm I — "Kapının altındaki ışık")
# =============================================================================
def mekan_depo(katmanlar: set[str] | list[str] | None = None,
               plan_gorusu: bool = True) -> tuple[str, str]:
    """Karanlık ahşap depo: soğuk gece mavisi + kapı altından tek sıcak altın ışık çizgisi."""
    rng = random.Random(101)
    p = _uid("depo")

    defs = f"""
    <linearGradient id="{p}_wall_back" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#070D17"/>
      <stop offset="55%" stop-color="#0E1A2B"/>
      <stop offset="92%" stop-color="#1A2636"/>
      <stop offset="100%" stop-color="#352B21"/>
    </linearGradient>
    <linearGradient id="{p}_wall_left" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#060B13"/>
      <stop offset="65%" stop-color="#0E1929"/>
      <stop offset="100%" stop-color="#16253A"/>
    </linearGradient>
    <linearGradient id="{p}_wall_right" x1="1" y1="0" x2="0" y2="0">
      <stop offset="0%" stop-color="#050A12"/>
      <stop offset="62%" stop-color="#0D1726"/>
      <stop offset="100%" stop-color="#152336"/>
    </linearGradient>
    <linearGradient id="{p}_ceil" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#04080F"/>
      <stop offset="100%" stop-color="#0C1524"/>
    </linearGradient>
    <linearGradient id="{p}_floor_base" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#161D28"/>
      <stop offset="35%" stop-color="#0E1520"/>
      <stop offset="100%" stop-color="#070B12"/>
    </linearGradient>
    <linearGradient id="{p}_door_wood" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#121D2E"/>
      <stop offset="60%" stop-color="#182538"/>
      <stop offset="88%" stop-color="#272A32"/>
      <stop offset="100%" stop-color="#6B4F2B"/>
    </linearGradient>
    <linearGradient id="{p}_slit_core" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#E7A243" stop-opacity="0.35"/>
      <stop offset="15%" stop-color="#FFD98B" stop-opacity="0.95"/>
      <stop offset="50%" stop-color="#FFF7DC" stop-opacity="1.0"/>
      <stop offset="85%" stop-color="#FFD98B" stop-opacity="0.95"/>
      <stop offset="100%" stop-color="#E7A243" stop-opacity="0.35"/>
    </linearGradient>
    <linearGradient id="{p}_light_cone" x1="0.5" y1="0" x2="0.5" y2="1">
      <stop offset="0%" stop-color="#FFE6A8" stop-opacity="0.72"/>
      <stop offset="16%" stop-color="#F2B95E" stop-opacity="0.46"/>
      <stop offset="52%" stop-color="#C98332" stop-opacity="0.18"/>
      <stop offset="100%" stop-color="#8A511A" stop-opacity="0.0"/>
    </linearGradient>
    <radialGradient id="{p}_light_halo" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0%" stop-color="#FFEBB5" stop-opacity="0.75"/>
      <stop offset="38%" stop-color="#EAA74B" stop-opacity="0.28"/>
      <stop offset="100%" stop-color="#A8641F" stop-opacity="0.0"/>
    </radialGradient>
    <linearGradient id="{p}_crate_top" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#293446"/>
      <stop offset="100%" stop-color="#18202D"/>
    </linearGradient>
    <linearGradient id="{p}_crate_side" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#101722"/>
      <stop offset="72%" stop-color="#1B2534"/>
      <stop offset="100%" stop-color="#383028"/>
    </linearGradient>
    <linearGradient id="{p}_box_warm" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#1E1D21"/>
      <stop offset="70%" stop-color="#2C2724"/>
      <stop offset="100%" stop-color="#5B4229"/>
    </linearGradient>
    <radialGradient id="{p}_vignette" cx="0.5" cy="0.56" r="0.62">
      <stop offset="55%" stop-color="#000000" stop-opacity="0.0"/>
      <stop offset="100%" stop-color="#02050A" stop-opacity="0.72"/>
    </radialGradient>
    <filter id="{p}_glow_gold" x="-25%" y="-40%" width="150%" height="200%">
      <feGaussianBlur stdDeviation="5.5" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="{p}_glow_cyan" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="2.6" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    """

    parts: list[str] = []

    # --- KATMAN 1: UZAK (Arka duvar, kapı, kapı altı altın ışık çizgisi, sürgü) ---
    if _katman_aktif(katmanlar, "uzak"):
        u: list[str] = [f'<g id="depo-uzak">']
        # Tavan + arka duvar ana form
        u.append(f'<rect x="0" y="0" width="960" height="540" fill="#060B13"/>')
        u.append(f'<polygon points="0,0 960,0 715,108 245,108" fill="url(#{p}_ceil)"/>')
        u.append(f'<rect x="245" y="108" width="470" height="232" fill="url(#{p}_wall_back)"/>')

        # Arka duvar dikey ahşap tahtaları (düz renk yok, her tahta tonlu + damar çizgili)
        plank_xs = [245, 290, 336, 382, 412, 548, 594, 640, 682, 715]
        for i in range(len(plank_xs) - 1):
            x0, x1 = plank_xs[i], plank_xs[i + 1]
            if x0 >= 382 and x1 <= 548:
                continue  # kapı alanı
            shade = rng.choice(["#0B1422", "#101B2D", "#132033", "#0D1726"])
            u.append(f'<rect x="{x0}" y="108" width="{x1-x0}" height="232" fill="{shade}" opacity="0.55"/>')
            u.append(f'<path d="M{x0},108 L{x0},340" fill="none" stroke="#060A11" stroke-width="1.6"/>')
            # Ahşap damarları
            for _ in range(3):
                gx = x0 + rng.uniform(5, max(6, x1 - x0 - 5))
                u.append(
                    f'<path d="M{gx:.1f},112 Q{gx+rng.uniform(-4,4):.1f},220 {gx+rng.uniform(-3,3):.1f},336" '
                    f'fill="none" stroke="#1E3048" stroke-width="0.9" opacity="0.45"/>'
                )

        # Kapı çerçevesi (kalın koyu ahşap pervaz)
        u.append(f'<rect x="372" y="128" width="186" height="212" fill="#09101B" stroke="{INK}" stroke-width="2.0"/>')
        # Kapı gövdesi (altında 7px ışık aralığı bırakır: y=136..333)
        u.append(f'<rect x="382" y="136" width="166" height="197" fill="url(#{p}_door_wood)" stroke="{INK}" stroke-width="1.8"/>')

        # Kapının dikey ahşap kanat tahtaları + çapraz destek (Z-kuşağı)
        for dx in (415, 448, 482, 515):
            u.append(f'<path d="M{dx},136 L{dx},333" fill="none" stroke="#0A1019" stroke-width="1.5"/>')
            u.append(f'<path d="M{dx+2},138 L{dx+2},331" fill="none" stroke="#263952" stroke-width="0.7" opacity="0.5"/>')
        # Yatay kuşaklar
        u.append(f'<rect x="384" y="168" width="162" height="18" fill="#131E2E" stroke="#080D15" stroke-width="1.4"/>')
        u.append(f'<rect x="384" y="286" width="162" height="18" fill="#1C232E" stroke="#080D15" stroke-width="1.4"/>')
        # Alt kuşağa vuran sıcak altın yansıma
        u.append(f'<path d="M385,304 L545,304" fill="none" stroke="#E8A94D" stroke-width="1.4" opacity="0.55"/>')
        # Kapı ahşap damar, budak ve çatlak detayları (R13 %200 doku zenginliği)
        for cx_d in (396, 430, 464, 498, 530):
            u.append(
                f'<path d="M{cx_d},142 C{cx_d+3},190 {cx_d-3},250 {cx_d+1},328" '
                f'fill="none" stroke="#253852" stroke-width="0.9" opacity="0.52"/>'
            )
            u.append(
                f'<path d="M{cx_d+7},146 C{cx_d+5},205 {cx_d+9},260 {cx_d+6},325" '
                f'fill="none" stroke="#0B131E" stroke-width="0.8" opacity="0.55"/>'
            )
        # Kapı ahşap budakları ve alt kenar aşınma çizikleri
        for kx, ky in [(404, 216), (470, 248), (506, 198), (434, 314)]:
            u.append(f'<ellipse cx="{kx}" cy="{ky}" rx="3.2" ry="6.5" fill="none" stroke="#0A111A" stroke-width="1.0" opacity="0.65"/>')
            u.append(f'<ellipse cx="{kx}" cy="{ky}" rx="1.2" ry="2.6" fill="#080D14" opacity="0.65"/>')
        # Yatay kuşak çivi başları ve ahşap lifleri
        for ny_k in (177, 295):
            for nx_k in (398, 432, 466, 500, 532):
                u.append(f'<circle cx="{nx_k}" cy="{ny_k}" r="1.6" fill="#070B11"/>')
                u.append(f'<circle cx="{nx_k-0.5}" cy="{ny_k-0.5}" r="0.6" fill="#5A6C82" opacity="0.6"/>')
            u.append(f'<path d="M386,{ny_k-4} L544,{ny_k-4}" fill="none" stroke="#2A3C52" stroke-width="0.7" opacity="0.45"/>')

        # Sol menteşeler (ağır dövme demir)
        for my in (169, 287):
            u.append(f'<rect x="374" y="{my+2}" width="34" height="12" rx="1.5" fill="#1A222D" stroke="{INK}" stroke-width="1.3"/>')
            u.append(f'<circle cx="381" cy="{my+8}" r="2.2" fill="#3B4B5E"/>')
            u.append(f'<circle cx="399" cy="{my+8}" r="1.6" fill="#0C1118"/>')

        # Sağda ağır metal kilit sürgüsü + kol (Kimlik Öğesi 1 parçası)
        u.append(f'<rect x="514" y="226" width="42" height="24" rx="2" fill="#1C2531" stroke="{INK}" stroke-width="1.5"/>')
        u.append(f'<rect x="522" y="233" width="38" height="8" rx="2" fill="#3A495A" stroke="{INK}" stroke-width="1.2"/>')
        u.append(f'<path d="M524,234 L558,234" fill="none" stroke="#7E97B3" stroke-width="1.0" opacity="0.65"/>')
        u.append(f'<circle cx="526" cy="237" r="4.5" fill="#2A3644" stroke="{INK}" stroke-width="1.2"/>')
        # Kilit plakasının üstüne hafif sıcak alt ışık yansıması
        u.append(f'<path d="M515,250 L555,250" fill="none" stroke="#D99B49" stroke-width="1.0" opacity="0.45"/>')

        # *** KAPININ ALTINDAKİ TEK SICAK ALTIN IŞIK ÇİZGİSİ (Bookend Motifi!) ***
        u.append(f'<ellipse cx="465" cy="336" rx="125" ry="26" fill="url(#{p}_light_halo)"/>')
        u.append(f'<rect x="378" y="332" width="174" height="8.5" rx="2" fill="url(#{p}_slit_core)" filter="url(#{p}_glow_gold)"/>')
        u.append(f'<rect x="383" y="334.5" width="164" height="3.8" rx="1.5" fill="#FFFDF2"/>')
        # Kapı sağ yan aralığından çok ince dikey ışık sızıntısı
        u.append(f'<path d="M549,140 L549,333" fill="none" stroke="#F6C56B" stroke-width="1.1" opacity="0.42"/>')

        # Tavan kirişleri
        for ky in (28, 66, 98):
            x_l = int(ky * 2.25)
            x_r = 960 - x_l
            u.append(f'<path d="M{x_l},{ky} L{x_r},{ky}" fill="none" stroke="#0C1626" stroke-width="6"/>')
            u.append(f'<path d="M{x_l},{ky+3} L{x_r},{ky+3}" fill="none" stroke="#1A2C44" stroke-width="1.1" opacity="0.5"/>')

        u.append('</g>')
        parts.append("\n".join(u))

    # --- KATMAN 2: ORTA (Perspektifli yan ahşap duvarlar, çatlaklar, raflar) ---
    if _katman_aktif(katmanlar, "orta"):
        o: list[str] = [f'<g id="depo-orta">']
        # Sol duvar + sağ duvar ana yüzeyleri
        o.append(f'<polygon points="0,0 245,108 245,340 0,500" fill="url(#{p}_wall_left)" stroke="{INK}" stroke-width="1.5"/>')
        o.append(f'<polygon points="960,0 715,108 715,340 960,500" fill="url(#{p}_wall_right)" stroke="{INK}" stroke-width="1.5"/>')

        # Sol duvar perspektifli dikey ahşap panelleri + damarlar + çatlaklar (Kimlik Öğesi 2)
        left_t = [0.0, 0.16, 0.32, 0.48, 0.63, 0.77, 0.89, 1.0]
        for i in range(len(left_t) - 1):
            t0, t1 = left_t[i], left_t[i + 1]
            x0, x1 = t0 * 245, t1 * 245
            yt0, yt1 = t0 * 108, t1 * 108
            yb0, yb1 = 500 - t0 * 160, 500 - t1 * 160
            tone = ["#0A1220", "#0F1B2E", "#122136", "#0D1727"][i % 4]
            o.append(f'<polygon points="{x0:.1f},{yt0:.1f} {x1:.1f},{yt1:.1f} {x1:.1f},{yb1:.1f} {x0:.1f},{yb0:.1f}" fill="{tone}" opacity="0.55"/>')
            o.append(f'<path d="M{x1:.1f},{yt1:.1f} L{x1:.1f},{yb1:.1f}" fill="none" stroke="#050911" stroke-width="2.0"/>')
            o.append(f'<path d="M{x1-2:.1f},{yt1+4:.1f} L{x1-2:.1f},{yb1-4:.1f}" fill="none" stroke="#223650" stroke-width="0.8" opacity="0.45"/>')
            # Ahşap çatlakları ve budaklar
            mx = (x0 + x1) * 0.5
            my = (yt0 + yb0) * 0.5
            o.append(
                f'<path d="M{mx:.1f},{yt0+18:.1f} Q{mx+3:.1f},{my:.1f} {mx-2:.1f},{yb0-22:.1f}" '
                f'fill="none" stroke="#1E304A" stroke-width="0.9" opacity="0.42"/>'
            )
            if i in (2, 4):
                # Belirgin çatlak (Michael'ın plan görüşüne bağlanacak)
                o.append(
                    f'<path d="M{mx-4:.1f},{my-48:.1f} L{mx+2:.1f},{my-12:.1f} L{mx-3:.1f},{my+28:.1f} L{mx+3:.1f},{my+62:.1f}" '
                    f'fill="none" stroke="#04070D" stroke-width="2.1"/>'
                )
                o.append(
                    f'<path d="M{mx-3:.1f},{my-48:.1f} L{mx+3:.1f},{my-12:.1f} L{mx-2:.1f},{my+28:.1f}" '
                    f'fill="none" stroke="#314C6E" stroke-width="0.9" opacity="0.65"/>'
                )

        # Sağ duvar perspektifli dikey ahşap panelleri
        for i in range(len(left_t) - 1):
            t0, t1 = left_t[i], left_t[i + 1]
            x0, x1 = 960 - t0 * 245, 960 - t1 * 245
            yt0, yt1 = t0 * 108, t1 * 108
            yb0, yb1 = 500 - t0 * 160, 500 - t1 * 160
            tone = ["#09111E", "#0E192B", "#111E32", "#0B1524"][i % 4]
            o.append(f'<polygon points="{x0:.1f},{yt0:.1f} {x1:.1f},{yt1:.1f} {x1:.1f},{yb1:.1f} {x0:.1f},{yb0:.1f}" fill="{tone}" opacity="0.55"/>')
            o.append(f'<path d="M{x1:.1f},{yt1:.1f} L{x1:.1f},{yb1:.1f}" fill="none" stroke="#050911" stroke-width="2.0"/>')
            mx = (x0 + x1) * 0.5
            my = (yt0 + yb0) * 0.5
            o.append(
                f'<path d="M{mx:.1f},{yt0+20:.1f} Q{mx-3:.1f},{my:.1f} {mx+2:.1f},{yb0-20:.1f}" '
                f'fill="none" stroke="#1D2F47" stroke-width="0.9" opacity="0.4"/>'
            )

        # Sağ duvara monteli eski ahşap raf ve karanlık kavanoz/kutu siluetleri
        o.append(f'<polygon points="738,214 915,176 915,190 738,226" fill="#131F30" stroke="{INK}" stroke-width="1.5"/>')
        o.append(f'<polygon points="738,214 915,176 896,172 728,208" fill="#1F3047" stroke="{INK}" stroke-width="1.2"/>')
        # Rafta eski kutular
        o.append(f'<polygon points="760,164 818,150 818,196 760,208" fill="#152132" stroke="{INK}" stroke-width="1.4"/>')
        o.append(f'<polygon points="828,136 892,120 892,178 828,193" fill="#101A28" stroke="{INK}" stroke-width="1.4"/>')
        o.append(f'<path d="M760,208 L760,164 L818,150" fill="none" stroke="#364E6D" stroke-width="1.0" opacity="0.55"/>')

        o.append('</g>')
        parts.append("\n".join(o))

    # --- KATMAN 3: SAHNE (Ahşap zemin, altın ışık huzmesi, sandıklar, kâğıt turna) ---
    if _katman_aktif(katmanlar, "sahne"):
        s: list[str] = [f'<g id="depo-sahne">']
        # Ahşap zemin ana yüzey
        s.append(f'<polygon points="0,500 245,340 715,340 960,500 960,540 0,540" fill="url(#{p}_floor_base)"/>')

        # Perspektif zemin tahta çizgileri (kaçış noktası 465, 295)
        for bx in range(-180, 1180, 74):
            # y=340'dan y=540'a perspektif ışınları
            top_x = 465 + (bx - 465) * 0.42
            s.append(f'<path d="M{top_x:.1f},340 L{bx:.1f},540" fill="none" stroke="#070C14" stroke-width="1.7" opacity="0.82"/>')
            s.append(f'<path d="M{top_x+2:.1f},340 L{bx+3:.1f},540" fill="none" stroke="#243347" stroke-width="0.7" opacity="0.35"/>')
        # Yatay tahta ek yerleri
        for fy in (362, 392, 430, 476, 522):
            s.append(f'<path d="M0,{fy} L960,{fy}" fill="none" stroke="#080D16" stroke-width="1.0" opacity="0.45"/>')

        # *** ZEMİNE YAYILAN TEK SICAK ALTIN IŞIK KONİSİ ***
        s.append(f'<polygon points="380,339 550,339 760,540 175,540" fill="url(#{p}_light_cone)"/>')
        # Yumuşak merkez ışık çekirdeği + ahşap tahta dokusu üzerinde organik altın yansıma
        s.append(f'<polygon points="402,339 528,339 642,540 296,540" fill="url(#{p}_light_cone)" opacity="0.55"/>')
        for rx_top, rx_bot, op in [(394, 224, 0.10), (434, 355, 0.14), (474, 488, 0.14), (514, 620, 0.09)]:
            s.append(f'<polygon points="{rx_top},340 {rx_top+32},340 {rx_bot+78},540 {rx_bot},540" fill="#FFE2A1" opacity="{op}"/>')
        # Işık konisi içindeki tahta lifleri ve mikro yansıma parıltıları
        for lx_t in range(392, 542, 18):
            lx_b = 465 + (lx_t - 465) * 2.55
            s.append(f'<path d="M{lx_t},341 L{lx_b:.1f},520" fill="none" stroke="#FFF0C4" stroke-width="0.8" opacity="0.22"/>')

        # Sol orta planda eski ahşap depo sandıkları + karton kutu (Kimlik Öğesi 3, R9 zemin temas gölgesi)
        # Temas gölgesi (sandık zemine oturur)
        s.append(f'<polygon points="88,432 288,432 308,468 72,468" fill="#03060B" opacity="0.82"/>')
        # Büyük ahşap sandık
        s.append(f'<polygon points="94,318 228,318 228,442 94,442" fill="#131C2A" stroke="{INK}" stroke-width="1.9"/>')
        s.append(f'<polygon points="228,318 278,300 278,418 228,442" fill="url(#{p}_crate_side)" stroke="{INK}" stroke-width="1.9"/>')
        s.append(f'<polygon points="94,318 148,300 278,300 228,318" fill="url(#{p}_crate_top)" stroke="{INK}" stroke-width="1.7"/>')
        # Sandık çıtaları ve çapraz destek
        s.append(f'<path d="M94,358 L228,358 M94,400 L228,400 M106,326 L216,434" fill="none" stroke="#090F18" stroke-width="2.0"/>')
        s.append(f'<path d="M228,358 L278,340 M228,400 L278,382" fill="none" stroke="#090F18" stroke-width="1.6"/>')
        # Altın ışık huzmesinden sandığın sağ kenarına vuran sıcak rim-light!
        s.append(f'<path d="M277,301 L277,417 L229,441" fill="none" stroke="#F0B55A" stroke-width="2.0" opacity="0.72"/>')
        s.append(f'<path d="M228,319 L228,440" fill="none" stroke="#C98D3F" stroke-width="1.2" opacity="0.45"/>')

        # Sandığın üstünde bağlanmış eski karton kutu
        s.append(f'<polygon points="122,254 218,254 218,312 122,312" fill="#1E2028" stroke="{INK}" stroke-width="1.6"/>')
        s.append(f'<polygon points="218,254 252,242 252,298 218,312" fill="url(#{p}_box_warm)" stroke="{INK}" stroke-width="1.6"/>')
        s.append(f'<polygon points="122,254 156,242 252,242 218,254" fill="#2B2E38" stroke="{INK}" stroke-width="1.5"/>')
        s.append(f'<path d="M168,254 L168,312 M235,248 L235,305" fill="none" stroke="#5D4D3D" stroke-width="2.2" opacity="0.7"/>')
        s.append(f'<path d="M251,243 L251,297" fill="none" stroke="#E5A852" stroke-width="1.4" opacity="0.58"/>')

        # Sağ tarafta ikinci küçük ahşap sandık (gölgeye oturmuş)
        s.append(f'<polygon points="690,418 858,418 874,458 672,458" fill="#03060B" opacity="0.82"/>')
        s.append(f'<polygon points="718,326 848,326 848,434 718,434" fill="#111A27" stroke="{INK}" stroke-width="1.8"/>')
        s.append(f'<polygon points="682,312 718,326 718,434 682,414" fill="#1E252E" stroke="{INK}" stroke-width="1.8"/>')
        s.append(f'<polygon points="682,312 812,312 848,326 718,326" fill="#1E2B3D" stroke="{INK}" stroke-width="1.6"/>')
        s.append(f'<path d="M683,313 L683,413 L717,433" fill="none" stroke="#EAB056" stroke-width="1.8" opacity="0.65"/>')

        # *** KÜÇÜK KÂĞIT TURNA (Kimlik Öğesi 4 — ışık huzmesinin ucunda tek başına!) ***
        # Turnanın altına sıcak ışık havuzu
        s.append(f'<ellipse cx="566" cy="454" rx="44" ry="11" fill="#FFDA8E" opacity="0.22"/>')
        s.append(_turna_svg(566, 448, scale=1.08, rot=-6,
                            fill_light="#FFF2D6", fill_mid="#DFC295", fill_dark="#8D7354",
                            stroke="#1B1510", rim="#FFF9E6"))

        s.append('</g>')
        parts.append("\n".join(s))

    # --- KATMAN 4: PLAN GÖRÜŞÜ (Tahta çatlakları & kapı aralığında camgöbeği ipuçları) ---
    if plan_gorusu and _katman_aktif(katmanlar, "plan"):
        pl: list[str] = [f'<g id="depo-plan" filter="url(#{p}_glow_cyan)" opacity="0.88">']
        # Sol duvardaki çatlakların üstünde ince camgöbeği ölçüm hattı
        pl.append(
            f'<path d="M126,204 L132,240 L127,280 L133,314" '
            f'fill="none" stroke="{PLAN}" stroke-width="1.35" stroke-dasharray="5,3"/>'
        )
        pl.append(
            f'<path d="M126,204 L196,204 M133,314 L196,314 M186,204 L186,314" '
            f'fill="none" stroke="{PLAN}" stroke-width="0.9" opacity="0.62"/>'
        )
        # Kapı sürgüsü + alt ışık aralığı ölçüm çizgileri (Michael'ın "her şeyi görmesi")
        pl.append(
            f'<path d="M535,237 L592,237 L592,336 L556,336" '
            f'fill="none" stroke="{PLAN}" stroke-width="1.2" stroke-dasharray="4,3"/>'
        )
        # Kapı alt aralığı ölçü tırnağı
        pl.append(
            f'<path d="M382,348 L548,348 M382,343 L382,353 M548,343 L548,353" '
            f'fill="none" stroke="{PLAN}" stroke-width="1.05" opacity="0.78"/>'
        )
        # Düğüm noktaları (01, 02, 03)
        for nx, ny, lbl in [(132, 240, "01"), (535, 237, "02"), (554, 336, "03")]:
            pl.append(f'<circle cx="{nx}" cy="{ny}" r="5.5" fill="none" stroke="{PLAN}" stroke-width="1.3"/>')
            pl.append(f'<circle cx="{nx}" cy="{ny}" r="2.0" fill="{PLAN_CORE}"/>')
            pl.append(f'<text x="{nx+9}" y="{ny+4}" fill="{PLAN}" font-family="Consolas,monospace" font-size="10" font-weight="bold">{lbl}</text>')
        pl.append('</g>')
        parts.append("\n".join(pl))

    # --- KATMAN 5: ÖN PLAN (Işık huzmesinde uçuşan toz zerreleri + siluet kenar + vinyet) ---
    if _katman_aktif(katmanlar, "onplan"):
        f: list[str] = [f'<g id="depo-onplan">']
        # Işık huzmesinde süzülen altın toz zerreleri
        for _ in range(34):
            ty = rng.uniform(336, 520)
            spread = (ty - 332) / 208.0
            tx = rng.uniform(385 - spread * 175, 545 + spread * 175)
            tr = rng.uniform(0.9, 2.5)
            top = rng.uniform(0.28, 0.85)
            col = "#FFF4D2" if tr < 1.6 else "#F6C873"
            f.append(f'<circle cx="{tx:.1f}" cy="{ty:.1f}" r="{tr:.1f}" fill="{col}" opacity="{top:.2f}"/>')

        # Ön plan koyu siluet çerçeveleme (sol ve sağ alt köşede yakın sandık/direk köşesi)
        f.append(f'<polygon points="0,415 62,438 48,540 0,540" fill="#04070D" opacity="0.88"/>')
        f.append(f'<polygon points="960,402 894,432 912,540 960,540" fill="#04070D" opacity="0.88"/>')
        # Sinematik vinyet
        f.append(f'<rect x="0" y="0" width="960" height="540" fill="url(#{p}_vignette)"/>')
        f.append('</g>')
        parts.append("\n".join(f))

    return defs, "\n".join(parts)


# =============================================================================
# 2. FOX RIVER HÜCRESİ (Bölüm III — "Plan ve Kaçış")
# =============================================================================
def mekan_hucre(katmanlar: set[str] | list[str] | None = None,
                plan_gorusu: bool = True) -> tuple[str, str]:
    """Fox River hücresi: yeşilimsi-soğuk floresan + parmaklık gölgesi + cıvata plan çizgisi."""
    rng = random.Random(202)
    p = _uid("hucre")

    defs = f"""
    <linearGradient id="{p}_corr_bg" x1="0" y1="0" x2="1" y2="0.4">
      <stop offset="0%" stop-color="#1E363B"/>
      <stop offset="55%" stop-color="#335358"/>
      <stop offset="100%" stop-color="#1A2C30"/>
    </linearGradient>
    <linearGradient id="{p}_wall_back" x1="0.7" y1="0" x2="0.2" y2="1">
      <stop offset="0%" stop-color="#4A6466"/>
      <stop offset="45%" stop-color="#354A4D"/>
      <stop offset="100%" stop-color="#1F2E32"/>
    </linearGradient>
    <linearGradient id="{p}_wall_left" x1="0" y1="0" x2="1" y2="0.5">
      <stop offset="0%" stop-color="#1B292D"/>
      <stop offset="60%" stop-color="#293D41"/>
      <stop offset="100%" stop-color="#384F53"/>
    </linearGradient>
    <linearGradient id="{p}_floor" x1="0.8" y1="0" x2="0.1" y2="1">
      <stop offset="0%" stop-color="#3C5254"/>
      <stop offset="45%" stop-color="#253437"/>
      <stop offset="100%" stop-color="#141E21"/>
    </linearGradient>
    <linearGradient id="{p}_ceil" x1="0.5" y1="0" x2="0.5" y2="1">
      <stop offset="0%" stop-color="#162326"/>
      <stop offset="100%" stop-color="#293E42"/>
    </linearGradient>
    <linearGradient id="{p}_steel" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#3D4C52"/>
      <stop offset="32%" stop-color="#7B8F96"/>
      <stop offset="58%" stop-color="#9BB0B6"/>
      <stop offset="100%" stop-color="#354348"/>
    </linearGradient>
    <linearGradient id="{p}_steel_dark" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#222D32"/>
      <stop offset="45%" stop-color="#4A5B62"/>
      <stop offset="100%" stop-color="#1B2428"/>
    </linearGradient>
    <linearGradient id="{p}_blanket" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#5B6E75"/>
      <stop offset="60%" stop-color="#415157"/>
      <stop offset="100%" stop-color="#2A363B"/>
    </linearGradient>
    <radialGradient id="{p}_fluor_glow" cx="0.5" cy="0.2" r="0.65">
      <stop offset="0%" stop-color="#C8F2E8" stop-opacity="0.45"/>
      <stop offset="42%" stop-color="#6EA39E" stop-opacity="0.18"/>
      <stop offset="100%" stop-color="#2A4244" stop-opacity="0.0"/>
    </radialGradient>
    <linearGradient id="{p}_corr_beam" x1="1" y1="0.2" x2="0" y2="0.8">
      <stop offset="0%" stop-color="#B9E6DF" stop-opacity="0.32"/>
      <stop offset="65%" stop-color="#75A8A3" stop-opacity="0.12"/>
      <stop offset="100%" stop-color="#2D4A4C" stop-opacity="0.0"/>
    </linearGradient>
    <radialGradient id="{p}_vignette" cx="0.52" cy="0.48" r="0.66">
      <stop offset="58%" stop-color="#000000" stop-opacity="0.0"/>
      <stop offset="100%" stop-color="#060C0E" stop-opacity="0.66"/>
    </radialGradient>
    <filter id="{p}_glow_cyan" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="2.8" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="{p}_glow_soft" x="-25%" y="-25%" width="150%" height="150%">
      <feGaussianBlur stdDeviation="4.5" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    """

    parts: list[str] = []

    # --- KATMAN 1: UZAK (Parmaklıkların arkasındaki Fox River koridoru) ---
    if _katman_aktif(katmanlar, "uzak"):
        u: list[str] = [f'<g id="hucre-uzak">']
        u.append(f'<rect x="0" y="0" width="960" height="540" fill="#121D20"/>')
        # Sağdaki koridor görünümü (x=725..960)
        u.append(f'<rect x="720" y="0" width="240" height="540" fill="url(#{p}_corr_bg)"/>')
        # Koridorda uzak duvar tuğlaları + üst floresan lamba
        for cy_b in range(60, 440, 32):
            u.append(f'<path d="M725,{cy_b} L960,{cy_b+18}" fill="none" stroke="#1B2E32" stroke-width="1.2" opacity="0.5"/>')
        # Koridor tavan floresanı (anahtar ışık kaynağı!)
        u.append(f'<polygon points="790,54 918,32 924,48 796,68" fill="#DFFAF2" filter="url(#{p}_glow_soft)"/>')
        u.append(f'<polygon points="794,56 914,36 918,44 798,63" fill="#FFFFFF"/>')
        # Koridor zemini
        u.append(f'<polygon points="725,404 960,468 960,540 725,540" fill="#23373B"/>')
        u.append('</g>')
        parts.append("\n".join(u))

    # --- KATMAN 2: ORTA (Beton blok duvarlar, floresan ışığı, çapraz parmaklık gölgeleri) ---
    if _katman_aktif(katmanlar, "orta"):
        o: list[str] = [f'<g id="hucre-orta">']
        # Tavan, arka duvar, sol duvar, zemin
        o.append(f'<polygon points="0,0 730,0 730,84 185,84" fill="url(#{p}_ceil)"/>')
        o.append(f'<rect x="185" y="84" width="545" height="316" fill="url(#{p}_wall_back)" stroke="{INK}" stroke-width="1.6"/>')
        o.append(f'<polygon points="0,0 185,84 185,400 0,510" fill="url(#{p}_wall_left)" stroke="{INK}" stroke-width="1.6"/>')
        o.append(f'<polygon points="0,510 185,400 730,400 960,510 960,540 0,540" fill="url(#{p}_floor)"/>')

        # Arka duvar beton blok derzleri (düz renk yok: her blok farklı ton + hafif sıva dokusu)
        row_h = 26
        block_w = 54
        for r_idx, by in enumerate(range(84, 400, row_h)):
            offset = (block_w // 2) if (r_idx % 2 == 1) else 0
            for bx in range(185 - offset, 730, block_w):
                rx = max(185, bx)
                rw = min(730, bx + block_w) - rx
                if rw <= 2:
                    continue
                rh = min(400 - by, row_h)
                b_tone = rng.choice(["#2C3F42", "#344A4D", "#3B5255", "#293B3E", "#41595C"])
                o.append(f'<rect x="{rx}" y="{by}" width="{rw}" height="{rh}" fill="{b_tone}" opacity="0.42"/>')
                # Üst ışık kenarı
                o.append(f'<path d="M{rx+1},{by+1} L{rx+rw-1},{by+1}" fill="none" stroke="#627E80" stroke-width="0.7" opacity="0.32"/>')
            o.append(f'<path d="M185,{by} L730,{by}" fill="none" stroke="#172326" stroke-width="1.25" opacity="0.72"/>')
            for bx in range(185 - offset, 730, block_w):
                if 185 < bx < 730:
                    o.append(f'<path d="M{bx},{by} L{bx},{min(400, by+row_h)}" fill="none" stroke="#172326" stroke-width="1.2" opacity="0.68"/>')

        # Beton duvarda hafif nem / kılcal çatlak dokusu (lavabo arkasında belirgin)
        o.append(f'<ellipse cx="525" cy="312" rx="68" ry="48" fill="#182426" opacity="0.32"/>')
        o.append(f'<path d="M498,262 L512,286 L508,314 L524,344" fill="none" stroke="#142022" stroke-width="1.4" opacity="0.75"/>')
        o.append(f'<path d="M565,248 L556,278 L564,302" fill="none" stroke="#142022" stroke-width="1.1" opacity="0.6"/>')

        # Sol duvar perspektifli beton blok hatları
        for ly_i in range(1, 9):
            t = ly_i / 9.0
            y_l = t * 510
            y_r = 84 + t * 316
            o.append(f'<path d="M0,{y_l:.1f} L185,{y_r:.1f}" fill="none" stroke="#141F22" stroke-width="1.3" opacity="0.65"/>')

        # Hücre içi tavan floresan lambası (ikincil dolgu)
        o.append(f'<rect x="370" y="28" width="160" height="12" rx="3" fill="#233336" stroke="{INK}" stroke-width="1.4"/>')
        o.append(f'<rect x="378" y="33" width="144" height="5" rx="2" fill="#D5F5EC" filter="url(#{p}_glow_soft)"/>')
        o.append(f'<rect x="185" y="84" width="545" height="316" fill="url(#{p}_fluor_glow)"/>')

        # *** KORİDORDAN PARMAKLIKLARIN DÜŞÜRDÜĞÜ ÇAPRAZ GÖLGE ŞERİTLERİ (Kimlik Öğesi 2) ***
        o.append(f'<polygon points="730,84 310,400 730,400" fill="url(#{p}_corr_beam)"/>')
        # Parmaklık gölge şeritleri arka duvarda diyagonal + zeminde uzanan şeritler
        for sx in (265, 338, 412, 486, 560, 634):
            o.append(
                f'<polygon points="{sx+95},84 {sx+124},84 {sx-32},400 {sx-62},400" '
                f'fill="#0A1316" opacity="0.34"/>'
            )
            # Zeminde kırılıp öne uzanan gölge şeridi
            o.append(
                f'<polygon points="{sx-62},400 {sx-32},400 {sx-175},540 {sx-215},540" '
                f'fill="#081012" opacity="0.38"/>'
            )
        # Yatay parmaklık kayıt gölgesi
        o.append(f'<polygon points="185,222 730,170 730,188 185,242" fill="#0A1316" opacity="0.28"/>')

        # Zemin beton derzleri
        for fx in (140, 310, 480, 650, 810):
            top_x = 460 + (fx - 460) * 0.56
            o.append(f'<path d="M{top_x:.1f},400 L{fx:.1f},540" fill="none" stroke="#131E21" stroke-width="1.2" opacity="0.55"/>')
        o.append(f'<path d="M90,458 L875,458" fill="none" stroke="#131E21" stroke-width="1.2" opacity="0.5"/>')

        o.append('</g>')
        parts.append("\n".join(o))

    # --- KATMAN 3: SAHNE (Çelik ranza, metal tuvalet/lavabo + cıvata, duvar rafı + kâğıt turna) ---
    if _katman_aktif(katmanlar, "sahne"):
        s: list[str] = [f'<g id="hucre-sahne">']

        # === 1) ÇELİK RANZA (İki Katlı, Sol Tarafta — Kimlik Öğesi 1) ===
        # Zemin temas gölgesi (R9)
        s.append(f'<polygon points="34,474 328,394 358,410 74,496" fill="#070D0F" opacity="0.72"/>')
        # Arka dikmeler
        s.append(f'<rect x="292" y="138" width="11" height="266" fill="url(#{p}_steel_dark)" stroke="{INK}" stroke-width="1.5"/>')
        s.append(f'<rect x="196" y="156" width="10" height="248" fill="url(#{p}_steel_dark)" stroke="{INK}" stroke-width="1.4"/>')

        # Alt yatak gövdesi (perspektifli çelik kasa + şilte + katlanmış gri battaniye)
        s.append(f'<polygon points="48,378 298,322 308,334 58,396" fill="url(#{p}_steel)" stroke="{INK}" stroke-width="1.7"/>')
        # Alt şilte ve battaniye
        s.append(f'<polygon points="56,356 294,306 300,322 60,378" fill="#5D6F75" stroke="{INK}" stroke-width="1.5"/>')
        s.append(f'<polygon points="56,356 176,331 190,342 66,374" fill="url(#{p}_blanket)" stroke="{INK}" stroke-width="1.4"/>')
        # Alt yastık (şilte içine tam oturur)
        s.append(f'<polygon points="216,312 276,300 286,310 226,322" fill="#899EA3" stroke="{INK}" stroke-width="1.3"/>')
        s.append(f'<path d="M222,315 L274,305" fill="none" stroke="#BDD2D6" stroke-width="1.1" opacity="0.72"/>')
        # Alt battaniye dikiş ve katlama çizgileri
        s.append(f'<path d="M78,360 L172,338 M92,366 L180,344" fill="none" stroke="#222E33" stroke-width="1.0" opacity="0.55"/>')

        # Üst yatak gövdesi
        s.append(f'<polygon points="48,220 298,186 308,198 58,236" fill="url(#{p}_steel)" stroke="{INK}" stroke-width="1.7"/>')
        # Üst şilte + battaniye kıvrımları
        s.append(f'<polygon points="56,202 292,172 298,186 60,220" fill="#63767C" stroke="{INK}" stroke-width="1.5"/>')
        s.append(f'<polygon points="108,194 252,176 260,192 114,212" fill="url(#{p}_blanket)" stroke="{INK}" stroke-width="1.4"/>')
        s.append(f'<path d="M122,202 Q185,193 246,184" fill="none" stroke="#222D31" stroke-width="1.2" opacity="0.65"/>')
        # Üst korkuluk borusu
        s.append(f'<path d="M136,196 L136,162 L268,148 L268,180" fill="none" stroke="#6E8289" stroke-width="4.5" stroke-linejoin="round"/>')
        s.append(f'<path d="M136,196 L136,162 L268,148 L268,180" fill="none" stroke="{INK}" stroke-width="1.5" stroke-linejoin="round"/>')

        # Ön ana dikmeler + çelik merdiven basamakları
        s.append(f'<rect x="44" y="138" width="14" height="346" fill="url(#{p}_steel)" stroke="{INK}" stroke-width="1.8"/>')
        s.append(f'<path d="M52,140 L52,482" fill="none" stroke="#B6CCD1" stroke-width="1.1" opacity="0.65"/>')
        s.append(f'<rect x="132" y="176" width="11" height="282" fill="url(#{p}_steel)" stroke="{INK}" stroke-width="1.6"/>')
        for ry in (256, 294, 332, 370, 408):
            s.append(f'<line x1="56" y1="{ry+8}" x2="134" y2="{ry}" stroke="{INK}" stroke-width="6"/>')
            s.append(f'<line x1="56" y1="{ry+8}" x2="134" y2="{ry}" stroke="#7D9299" stroke-width="3.2"/>')

        # === 2) METAL TUVALET / LAVABO ÜNİTESİ & BELİRGİN CIVATA (Kimlik Öğesi 3) ===
        # Duvar temas gölgesi ve zemin gölgesi (R9)
        s.append(f'<ellipse cx="526" cy="408" rx="68" ry="12" fill="#070D0F" opacity="0.72"/>')
        s.append(f'<rect x="466" y="256" width="124" height="148" rx="4" fill="#121C1F" opacity="0.45"/>')

        # Ana çelik konsol gövde (Fox River tipi tek parça paslanmaz çelik kombi ünite)
        s.append(f'<rect x="472" y="258" width="110" height="142" rx="4" fill="url(#{p}_steel)" stroke="{INK}" stroke-width="1.9"/>')
        # Fırçalanmış çelik yatay doku çizgileri & hafif pas/nem izi
        for sy_m in range(288, 396, 12):
            s.append(f'<path d="M476,{sy_m} L578,{sy_m}" fill="none" stroke="#B6C9CE" stroke-width="0.6" opacity="0.22"/>')
        s.append(f'<path d="M527,284 L527,326" fill="none" stroke="#2C3C40" stroke-width="1.5" opacity="0.32"/>')
        # Lavabo çanağı üst düzlem
        s.append(f'<polygon points="468,266 586,266 576,284 478,284" fill="#8EA4AA" stroke="{INK}" stroke-width="1.6"/>')
        s.append(f'<ellipse cx="527" cy="274" rx="34" ry="7" fill="#324247" stroke="{INK}" stroke-width="1.3"/>')
        # Musluk ve düğmeler
        s.append(f'<rect x="521" y="246" width="12" height="18" rx="2" fill="#6F858C" stroke="{INK}" stroke-width="1.3"/>')
        s.append(f'<path d="M527,252 Q527,264 527,268" fill="none" stroke="#B7CDD3" stroke-width="2.2"/>')
        s.append(f'<circle cx="506" cy="254" r="3.5" fill="#7D949B" stroke="{INK}" stroke-width="1.1"/>')
        s.append(f'<circle cx="548" cy="254" r="3.5" fill="#7D949B" stroke="{INK}" stroke-width="1.1"/>')

        # Tuvalet klozet çıkıntısı (öne uzanan çelik koni + oturak)
        s.append(f'<path d="M484,334 L570,334 L556,404 L498,404 Z" fill="url(#{p}_steel_dark)" stroke="{INK}" stroke-width="1.8"/>')
        s.append(f'<ellipse cx="527" cy="336" rx="44" ry="13" fill="#8AA0A6" stroke="{INK}" stroke-width="1.7"/>')
        s.append(f'<ellipse cx="527" cy="336" rx="31" ry="8.5" fill="#233034" stroke="{INK}" stroke-width="1.3"/>')
        s.append(f'<path d="M492,334 Q527,326 562,334" fill="none" stroke="#C7DCE0" stroke-width="1.4" opacity="0.7"/>')

        # *** DUVAR BİRLEŞİMİNDEKİ BELİRGİN ALTIGEN CIVATA DETAYI (Kaçışın kilit noktası!) ***
        # Sol-alt ve sağ-alt duvar flanş kulakları + büyük altıgen cıvata başları
        for fx_bolt, fy_bolt, active in [(462, 294, True), (462, 368, True), (582, 294, False), (582, 368, False)]:
            s.append(f'<rect x="{fx_bolt-6}" y="{fy_bolt-9}" width="18" height="18" rx="2" fill="#465960" stroke="{INK}" stroke-width="1.4"/>')
            # Altıgen cıvata başı
            cx_b, cy_b = fx_bolt + 3, fy_bolt
            r_b = 5.6
            hex_pts = " ".join(
                f"{cx_b + r_b*math.cos(math.radians(a)):.1f},{cy_b + r_b*math.sin(math.radians(a)):.1f}"
                for a in range(0, 360, 60)
            )
            fill_b = "#9FB8BE" if active else "#667A80"
            s.append(f'<polygon points="{hex_pts}" fill="{fill_b}" stroke="{INK}" stroke-width="1.3"/>')
            s.append(f'<circle cx="{cx_b}" cy="{cy_b}" r="1.8" fill="#263438"/>')
            if active:
                # Cıvata etrafında sökülme / tork çizik izi
                s.append(f'<path d="M{cx_b-9},{cy_b-6} A11,11 0 0,1 {cx_b+9},{cy_b-5}" fill="none" stroke="#BFE8F0" stroke-width="1.0" opacity="0.65"/>')

        # === 3) DUVARDA KÜÇÜK RAF + KÂĞIT TURNA (Kimlik Öğesi 4) ===
        s.append(f'<polygon points="368,214 452,214 446,222 362,222" fill="#4F6369" stroke="{INK}" stroke-width="1.4"/>')
        s.append(f'<polygon points="362,222 446,222 446,228 362,228" fill="#2B3A3E" stroke="{INK}" stroke-width="1.3"/>')
        # Raf destekleri
        s.append(f'<polygon points="374,228 380,228 374,242" fill="#233135" stroke="{INK}" stroke-width="1.1"/>')
        s.append(f'<polygon points="434,228 440,228 440,242" fill="#233135" stroke="{INK}" stroke-width="1.1"/>')
        # Rafta küçük kitap/not defteri
        s.append(f'<rect x="374" y="206" width="32" height="8" fill="#324659" stroke="{INK}" stroke-width="1.1"/>')
        s.append(f'<path d="M376,209 L404,209" fill="none" stroke="#C5D3D8" stroke-width="1.0"/>')
        # Rafta kâğıt turna!
        s.append(_turna_svg(426, 206, scale=0.72, rot=-4,
                            fill_light="#EBF5F2", fill_mid="#B9CFCB", fill_dark="#6E8684",
                            stroke="#162124", rim="#D2FAF0"))

        s.append('</g>')
        parts.append("\n".join(s))

    # --- KATMAN 4: PLAN GÖRÜŞÜ (Cıvata, lavabo arkası duvar ve kaçış rotası #7FE6FF) ---
    if plan_gorusu and _katman_aktif(katmanlar, "plan"):
        pl: list[str] = [f'<g id="hucre-plan" filter="url(#{p}_glow_cyan)" opacity="0.92">']
        # Lavabo arkasındaki gizli tesisat boşluğu şematik karesi
        pl.append(
            f'<rect x="462" y="246" width="128" height="156" fill="#7FE6FF" fill-opacity="0.06" '
            f'stroke="{PLAN}" stroke-width="1.2" stroke-dasharray="6,4"/>'
        )
        # Cıvata hedef halkaları (01)
        pl.append(f'<circle cx="465" cy="294" r="11" fill="none" stroke="{PLAN}" stroke-width="1.5"/>')
        pl.append(f'<circle cx="465" cy="294" r="2.5" fill="{PLAN_CORE}"/>')
        pl.append(f'<circle cx="465" cy="368" r="9" fill="none" stroke="{PLAN}" stroke-width="1.2" stroke-dasharray="3,2"/>')
        # Cıvatadan duvar içi tesisat borusuna kesik kaçış rotası
        pl.append(
            f'<path d="M465,294 L430,294 L430,176 L548,176 L548,244" '
            f'fill="none" stroke="{PLAN}" stroke-width="1.6" stroke-dasharray="6,4"/>'
        )
        # Tesisat boşluğu iç dikdörtgen ve tork ölçüsü
        pl.append(
            f'<path d="M548,176 L628,176 L628,136 L680,136" '
            f'fill="none" stroke="{PLAN}" stroke-width="1.4" stroke-dasharray="5,3"/>'
        )
        # Ölçü tırnakları
        pl.append(f'<path d="M472,238 L582,238 M472,234 L472,242 M582,234 L582,242" fill="none" stroke="{PLAN}" stroke-width="0.95" opacity="0.75"/>')
        # Düğüm etiketleri (lavabo üzerine binmeyecek şekilde temiz lider çizgisiyle)
        pl.append(f'<path d="M454,294 L424,294" fill="none" stroke="{PLAN}" stroke-width="1.0" opacity="0.8"/>')
        pl.append(f'<text x="358" y="290" fill="{PLAN}" font-family="Consolas,monospace" font-size="10.5" font-weight="bold">01 · CIVATA</text>')
        for nx, ny, txt in [(548, 176, "02 · DUVAR"), (628, 136, "03 · HAT")]:
            pl.append(f'<circle cx="{nx}" cy="{ny}" r="4.2" fill="{PLAN_CORE}"/>')
            pl.append(f'<text x="{nx+8}" y="{ny-6}" fill="{PLAN}" font-family="Consolas,monospace" font-size="10.5" font-weight="bold">{txt}</text>')
        pl.append('</g>')
        parts.append("\n".join(pl))

    # --- KATMAN 5: ÖN PLAN (Ağır çelik hücre parmaklıkları + toz + vinyet) ---
    if _katman_aktif(katmanlar, "onplan"):
        f: list[str] = [f'<g id="hucre-onplan">']
        # Sağdaki ağır çelik parmaklıklı hücre kapısı çerçevesi (x=724..960)
        f.append(f'<rect x="720" y="0" width="18" height="540" fill="url(#{p}_steel_dark)" stroke="{INK}" stroke-width="2.0"/>')
        # Dikey parmaklık çubukları (perspektifle kalınlaşan)
        bars = [(754, 11), (792, 12), (832, 13), (876, 14), (924, 16)]
        for bx, bw in bars:
            f.append(f'<rect x="{bx}" y="0" width="{bw}" height="540" fill="url(#{p}_steel_dark)" stroke="{INK}" stroke-width="1.8"/>')
            # Koridor ışığından sağ kenar parıltısı (rim-light)
            f.append(f'<path d="M{bx+bw-2},0 L{bx+bw-2},540" fill="none" stroke="#9FC7C4" stroke-width="1.4" opacity="0.62"/>')
        # Yatay kalın çelik kayıtlar + kilit kutusu
        for hy, hh in [(148, 18), (358, 20)]:
            f.append(f'<rect x="720" y="{hy}" width="240" height="{hh}" fill="#1C272B" stroke="{INK}" stroke-width="2.0"/>')
            f.append(f'<path d="M722,{hy+2} L958,{hy+2}" fill="none" stroke="#6E898D" stroke-width="1.2" opacity="0.55"/>')
        # Kilit kutusu
        f.append(f'<rect x="726" y="244" width="44" height="56" rx="3" fill="#202D31" stroke="{INK}" stroke-width="1.8"/>')
        f.append(f'<circle cx="748" cy="272" r="5.5" fill="#0E1518" stroke="#6E888C" stroke-width="1.2"/>')

        # Havada hafif floresan toz zerreleri
        for _ in range(20):
            dx = rng.uniform(200, 710)
            dy = rng.uniform(70, 460)
            dr = rng.uniform(0.8, 1.8)
            f.append(f'<circle cx="{dx:.1f}" cy="{dy:.1f}" r="{dr:.1f}" fill="#C8ECE6" opacity="{rng.uniform(0.18, 0.45):.2f}"/>')

        f.append(f'<rect x="0" y="0" width="960" height="540" fill="url(#{p}_vignette)"/>')
        f.append('</g>')
        parts.append("\n".join(f))

    return defs, "\n".join(parts)


# =============================================================================
# 3. FOX RIVER REVİR (Bölüm III — "Sıcak Yakınlık ve Açık Kapı")
# =============================================================================
def mekan_revir(katmanlar: set[str] | list[str] | None = None,
                plan_gorusu: bool = True) -> tuple[str, str]:
    """Fox River revir: sıcak amber-krem ışık + cam ilaç dolabı + aralık kapı & pirinç anahtar."""
    rng = random.Random(303)
    p = _uid("revir")

    defs = f"""
    <linearGradient id="{p}_wall_upper" x1="0.6" y1="0" x2="0.2" y2="1">
      <stop offset="0%" stop-color="#6B5642"/>
      <stop offset="50%" stop-color="#4F3E30"/>
      <stop offset="100%" stop-color="#352920"/>
    </linearGradient>
    <linearGradient id="{p}_wall_tile" x1="0.5" y1="0" x2="0.5" y2="1">
      <stop offset="0%" stop-color="#8C775E"/>
      <stop offset="65%" stop-color="#6A5844"/>
      <stop offset="100%" stop-color="#473A2D"/>
    </linearGradient>
    <linearGradient id="{p}_floor" x1="0.7" y1="0" x2="0.2" y2="1">
      <stop offset="0%" stop-color="#5B4A3A"/>
      <stop offset="52%" stop-color="#3D3127"/>
      <stop offset="100%" stop-color="#221A15"/>
    </linearGradient>
    <radialGradient id="{p}_amber_key" cx="0.62" cy="0.46" r="0.58">
      <stop offset="0%" stop-color="#FFF0C8" stop-opacity="0.55"/>
      <stop offset="32%" stop-color="#F2BA68" stop-opacity="0.26"/>
      <stop offset="72%" stop-color="#B87632" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="#4A2D15" stop-opacity="0.0"/>
    </radialGradient>
    <linearGradient id="{p}_door_gap" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#C8F0EC"/>
      <stop offset="50%" stop-color="#FFF0CC"/>
      <stop offset="100%" stop-color="#F3C171"/>
    </linearGradient>
    <linearGradient id="{p}_door_spill" x1="0.5" y1="0" x2="0.3" y2="1">
      <stop offset="0%" stop-color="#FFE6B3" stop-opacity="0.58"/>
      <stop offset="45%" stop-color="#E5B26B" stop-opacity="0.22"/>
      <stop offset="100%" stop-color="#9A6A34" stop-opacity="0.0"/>
    </linearGradient>
    <linearGradient id="{p}_glass" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFF5DF" stop-opacity="0.32"/>
      <stop offset="35%" stop-color="#D4E8E6" stop-opacity="0.08"/>
      <stop offset="65%" stop-color="#FFF0CC" stop-opacity="0.22"/>
      <stop offset="100%" stop-color="#8FA8A6" stop-opacity="0.06"/>
    </linearGradient>
    <linearGradient id="{p}_table_top" x1="0" y1="0" x2="1" y2="0.4">
      <stop offset="0%" stop-color="#785B40"/>
      <stop offset="60%" stop-color="#9A7653"/>
      <stop offset="100%" stop-color="#614731"/>
    </linearGradient>
    <linearGradient id="{p}_bed_pad" x1="0" y1="0" x2="1" y2="0.3">
      <stop offset="0%" stop-color="#354B4C"/>
      <stop offset="55%" stop-color="#4A6768"/>
      <stop offset="100%" stop-color="#283A3B"/>
    </linearGradient>
    <linearGradient id="{p}_brass" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFF0B0"/>
      <stop offset="45%" stop-color="#E3B14C"/>
      <stop offset="100%" stop-color="#8E601D"/>
    </linearGradient>
    <radialGradient id="{p}_vignette" cx="0.52" cy="0.5" r="0.65">
      <stop offset="56%" stop-color="#000000" stop-opacity="0.0"/>
      <stop offset="100%" stop-color="#110B07" stop-opacity="0.66"/>
    </radialGradient>
    <filter id="{p}_glow_warm" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="5.0" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="{p}_glow_cyan" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="2.2" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    """

    parts: list[str] = []

    # --- KATMAN 1: UZAK (Aralık revir kapısı ve ardındaki koridor ışığı — İmge Yankısı 2!) ---
    if _katman_aktif(katmanlar, "uzak"):
        u: list[str] = [f'<g id="revir-uzak">']
        u.append(f'<rect x="0" y="0" width="960" height="540" fill="#2A2018"/>')
        # Koridor boşluğu (kapı aralığından görünen soğuk-sıcak geçişli koridor)
        u.append(f'<rect x="706" y="102" width="128" height="278" fill="#1E3136"/>')
        u.append(f'<rect x="706" y="102" width="128" height="278" fill="url(#{p}_door_gap)" opacity="0.72"/>')
        # Koridor tavan ışık yansıması
        u.append(f'<rect x="716" y="108" width="28" height="270" fill="#FFF7DF" opacity="0.82" filter="url(#{p}_glow_warm)"/>')
        u.append('</g>')
        parts.append("\n".join(u))

    # --- KATMAN 2: ORTA (Sıcak krem duvar & fayans, cam kapaklı ilaç/insülin dolabı, aralık kapı) ---
    if _katman_aktif(katmanlar, "orta"):
        o: list[str] = [f'<g id="revir-orta">']
        # Tavan + arka duvar üst sıva + alt fayans
        o.append(f'<polygon points="0,0 960,0 860,64 110,64" fill="#2D231B"/>')
        o.append(f'<rect x="110" y="64" width="750" height="172" fill="url(#{p}_wall_upper)"/>')
        o.append(f'<rect x="110" y="236" width="750" height="144" fill="url(#{p}_wall_tile)"/>')
        # Sol duvar
        o.append(f'<polygon points="0,0 110,64 110,380 0,480" fill="#3B2E24" stroke="{INK_WARM}" stroke-width="1.5"/>')
        # Sağ duvar
        o.append(f'<polygon points="960,0 860,64 860,380 960,480" fill="#35291F" stroke="{INK_WARM}" stroke-width="1.5"/>')
        # Zemin
        o.append(f'<polygon points="0,480 110,380 860,380 960,480 960,540 0,540" fill="url(#{p}_floor)"/>')

        # Alt duvar sıcak krem-bej fayans karoları (düz renk yok, ton varyasyonlu)
        tile_s = 28
        for ty in range(236, 380, tile_s):
            for tx in range(110, 860, tile_s):
                if 702 <= tx <= 838:
                    continue  # kapı alanı
                t_col = rng.choice(["#7A6751", "#857159", "#6F5D49", "#8E7A61"])
                o.append(f'<rect x="{tx}" y="{ty}" width="{tile_s}" height="{min(tile_s, 380-ty)}" fill="{t_col}" opacity="0.38"/>')
                o.append(f'<path d="M{tx},{ty} L{tx+tile_s},{ty} M{tx},{ty} L{tx},{min(380, ty+tile_s)}" fill="none" stroke="#3F3226" stroke-width="0.9" opacity="0.55"/>')
        # Fayans üst çıtası
        o.append(f'<rect x="110" y="232" width="592" height="7" fill="#524031" stroke="{INK_WARM}" stroke-width="1.2"/>')

        # Zemin linolyum/karo ızgarası
        for gx in range(-60, 1080, 92):
            top_x = 480 + (gx - 480) * 0.62
            o.append(f'<path d="M{top_x:.1f},380 L{gx:.1f},540" fill="none" stroke="#261D17" stroke-width="1.1" opacity="0.55"/>')
        for gy in (408, 444, 488):
            o.append(f'<path d="M0,{gy} L960,{gy}" fill="none" stroke="#261D17" stroke-width="1.1" opacity="0.5"/>')

        # === CAM KAPAKLI İLAÇ / İNSÜLİN DOLABI (Kimlik Öğesi 2) ===
        # Dolap duvar gölgesi
        o.append(f'<rect x="382" y="102" width="212" height="156" rx="4" fill="#1D150F" opacity="0.45"/>')
        # Dolap metal/ahşap kasası
        o.append(f'<rect x="376" y="96" width="210" height="154" rx="4" fill="#D5C8B4" stroke="{INK_WARM}" stroke-width="2.0"/>')
        o.append(f'<rect x="386" y="106" width="190" height="134" fill="#3B3128" stroke="{INK_WARM}" stroke-width="1.5"/>')
        # İç raflar + raf altı gölgeleri
        for ry in (148, 192):
            o.append(f'<rect x="387" y="{ry+6}" width="188" height="4" fill="#1D1610" opacity="0.45"/>')
            o.append(f'<rect x="387" y="{ry}" width="188" height="6" fill="#9E8F7B" stroke="{INK_WARM}" stroke-width="1.1"/>')

        # İçindeki amber/mavi insülin flakonları ve tıbbi şişeler (detay zenginliği!)
        bottles = [
            # Üst raf
            (398, 122, 13, 26, "#C67B35", "#FFE2A8"),
            (416, 126, 11, 22, "#C67B35", "#FFE2A8"),
            (432, 118, 16, 30, "#4E8999", "#C5EEF7"),
            (455, 125, 12, 23, "#D9A84E", "#FFF0C2"),
            (496, 120, 18, 28, "#C8C2B4", "#FFFFFF"),
            (520, 126, 12, 22, "#4E8999", "#C5EEF7"),
            (538, 122, 14, 26, "#C67B35", "#FFE2A8"),
            # Orta raf (insülin flakonları + küçük şırınga kutusu)
            (398, 168, 11, 24, "#5FA4B5", "#DCF8FF"),
            (413, 168, 11, 24, "#5FA4B5", "#DCF8FF"),
            (428, 168, 11, 24, "#5FA4B5", "#DCF8FF"),
            (448, 174, 34, 18, "#DDD2BF", "#FFF8EC"),
            (500, 166, 14, 26, "#B96B2B", "#FFD999"),
            (520, 170, 13, 22, "#B96B2B", "#FFD999"),
            (540, 165, 22, 27, "#E3D8C5", "#FFFFFF"),
            # Alt raf
            (402, 212, 36, 26, "#D8CEBC", "#FFF9EE"),
            (448, 214, 14, 24, "#4C8394", "#C2EDF7"),
            (468, 218, 12, 20, "#C67B35", "#FFE2A8"),
            (504, 210, 48, 28, "#C4B69F", "#F2E6D2"),
        ]
        for bx, by, bw, bh, bcol, cap in bottles:
            o.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="2" fill="{bcol}" stroke="{INK_WARM}" stroke-width="1.1"/>')
            # Şişe etiketi + minik yazı çizgisi + cam parlama çizgisi + kapak
            eh = max(6, bh // 3)
            o.append(f'<rect x="{bx+2}" y="{by+6}" width="{bw-4}" height="{eh}" fill="{cap}" opacity="0.78"/>')
            o.append(f'<path d="M{bx+4},{by+9} L{bx+bw-4},{by+9}" fill="none" stroke="#5A4A3A" stroke-width="0.7" opacity="0.65"/>')
            o.append(f'<path d="M{bx+2.5},{by+3} L{bx+2.5},{by+bh-3}" fill="none" stroke="#FFF9E8" stroke-width="0.8" opacity="0.45"/>')
            if bw <= 18:
                o.append(f'<rect x="{bx+2}" y="{by-4}" width="{bw-4}" height="4" rx="1" fill="#E8DFCE" stroke="{INK_WARM}" stroke-width="0.9"/>')

        # Cam kapak çerçeveleri + diyagonal cam yansıması + küçük kırmızı haç işareti
        o.append(f'<rect x="386" y="106" width="93" height="134" fill="url(#{p}_glass)" stroke="#B7A994" stroke-width="2.2"/>')
        o.append(f'<rect x="483" y="106" width="93" height="134" fill="url(#{p}_glass)" stroke="#B7A994" stroke-width="2.2"/>')
        # Cam parlama şeritleri
        o.append(f'<polygon points="396,108 424,108 388,184 388,154" fill="#FFF7E2" opacity="0.22"/>')
        o.append(f'<polygon points="512,108 538,108 485,204 485,178" fill="#FFF7E2" opacity="0.18"/>')
        # Dolap kulpları
        o.append(f'<rect x="470" y="164" width="4" height="18" rx="1.5" fill="#7D6B55" stroke="{INK_WARM}" stroke-width="1.0"/>')
        o.append(f'<rect x="488" y="164" width="4" height="18" rx="1.5" fill="#7D6B55" stroke="{INK_WARM}" stroke-width="1.0"/>')
        # Sol üstte küçük revir haç işareti
        o.append(f'<rect x="394" y="113" width="12" height="4" fill="#B6493E" opacity="0.82"/>')
        o.append(f'<rect x="398" y="109" width="4" height="12" fill="#B6493E" opacity="0.82"/>')

        # Sol arka duvarda klinik panosu (anatomi / nöbet çizelgesi)
        o.append(f'<rect x="172" y="114" width="136" height="94" rx="3" fill="#4B3B2D" stroke="{INK_WARM}" stroke-width="1.7"/>')
        o.append(f'<rect x="180" y="122" width="120" height="78" fill="#9E8262"/>')
        o.append(f'<rect x="190" y="130" width="44" height="54" fill="#EFE4CE" stroke="{INK_WARM}" stroke-width="1.0"/>')
        o.append(f'<rect x="242" y="136" width="48" height="40" fill="#E6D7BC" stroke="{INK_WARM}" stroke-width="1.0"/>')
        o.append(f'<path d="M196,142 L226,142 M196,152 L222,152 M196,162 L218,162" fill="none" stroke="#6E5A46" stroke-width="1.1"/>')

        # Dolap ile kapı arasındaki duvarda küçük revir termometresi ve elektrik anahtarı (doku zenginliği)
        o.append(f'<rect x="628" y="138" width="24" height="62" rx="3" fill="#C9B99F" stroke="{INK_WARM}" stroke-width="1.3"/>')
        o.append(f'<path d="M640,146 L640,192" fill="none" stroke="#6E5B48" stroke-width="2.2"/>')
        o.append(f'<path d="M640,168 L640,192" fill="none" stroke="#C14B3C" stroke-width="2.2"/>')
        o.append(f'<circle cx="640" cy="192" r="3.4" fill="#C14B3C" stroke="{INK_WARM}" stroke-width="0.9"/>')
        for ty_t in (152, 160, 168, 176, 184):
            o.append(f'<path d="M634,{ty_t} L638,{ty_t}" fill="none" stroke="#3D3127" stroke-width="0.8"/>')
        # Duvar ışık anahtarı
        o.append(f'<rect x="658" y="256" width="16" height="24" rx="2" fill="#D4C5AC" stroke="{INK_WARM}" stroke-width="1.2"/>')
        o.append(f'<rect x="663" y="264" width="6" height="9" fill="#9E8C73" stroke="{INK_WARM}" stroke-width="0.9"/>')

        # === ARALIK DURAN REVİR KAPISI (Kimlik Öğesi 4 — İmge Yankısı 2!) ===
        # Kapı kasası (x=702..838, y=96..382)
        o.append(f'<rect x="700" y="96" width="142" height="286" fill="none" stroke="#4D3D2F" stroke-width="9"/>')
        o.append(f'<rect x="696" y="92" width="150" height="292" fill="none" stroke="{INK_WARM}" stroke-width="2.0"/>')
        # Kapı kanadı: hafif aralık açılmış (solda ~34px parlak ışık aralığı bırakır!)
        o.append(f'<polygon points="738,104 834,98 834,380 738,378" fill="#5A4839" stroke="{INK_WARM}" stroke-width="2.0"/>')
        # Kapı üst cam penceresi (telli revir camı)
        o.append(f'<polygon points="752,126 818,122 818,212 752,214" fill="#7D8F8A" stroke="{INK_WARM}" stroke-width="1.6"/>')
        o.append(f'<polygon points="752,126 818,122 818,212 752,214" fill="url(#{p}_glass)"/>')
        # Telli cam ızgarası
        for wy in (148, 170, 192):
            o.append(f'<path d="M753,{wy} L817,{wy-2}" fill="none" stroke="#3A4745" stroke-width="0.8" opacity="0.65"/>')
        for wx in (774, 796):
            o.append(f'<path d="M{wx},124 L{wx},213" fill="none" stroke="#3A4745" stroke-width="0.8" opacity="0.65"/>')
        # Kapı kolu & kilit dili (pirinç)
        o.append(f'<rect x="744" y="246" width="12" height="32" rx="2" fill="url(#{p}_brass)" stroke="{INK_WARM}" stroke-width="1.2"/>')
        o.append(f'<path d="M749,258 L764,258" fill="none" stroke="#F8D27D" stroke-width="4.2" stroke-linecap="round"/>')
        o.append(f'<path d="M749,258 L764,258" fill="none" stroke="{INK_WARM}" stroke-width="1.2" stroke-linecap="round"/>')
        # Aralık kapı kenarındaki sıcak altın rim-light
        o.append(f'<path d="M738,104 L738,378" fill="none" stroke="#FFF1CC" stroke-width="2.6" opacity="0.92"/>')

        # Aralık kapıdan zemine sızan ışık şeridi
        o.append(f'<polygon points="706,380 742,380 658,540 538,540" fill="url(#{p}_door_spill)"/>')

        o.append('</g>')
        parts.append("\n".join(o))

    # --- KATMAN 3: SAHNE (Muayene sedyesi, doktor masası, dosya, stetoskop, pirinç anahtar, sıcak lamba) ---
    if _katman_aktif(katmanlar, "sahne"):
        s: list[str] = [f'<g id="revir-sahne">']

        # === 1) MUAYENE SEDYESİ / MASASI (Sol-Orta — Kimlik Öğesi 1) ===
        # Zemin temas gölgesi (R9)
        s.append(f'<polygon points="74,474 396,422 436,444 114,502" fill="#120C08" opacity="0.72"/>')
        # Sedye alt metal çerçeve ve bacaklar
        for lx, ly, lh in [(104, 378, 102), (168, 366, 98), (356, 336, 94), (402, 344, 96)]:
            s.append(f'<rect x="{lx}" y="{ly}" width="10" height="{lh}" fill="#7D7265" stroke="{INK_WARM}" stroke-width="1.5"/>')
            s.append(f'<path d="M{lx+7},{ly+2} L{lx+7},{ly+lh-2}" fill="none" stroke="#D9C8AE" stroke-width="1.0" opacity="0.6"/>')
        # Alt dolap/çekmece gövdesi
        s.append(f'<polygon points="102,366 364,324 364,376 102,424" fill="#9E8F7B" stroke="{INK_WARM}" stroke-width="1.8"/>')
        s.append(f'<polygon points="364,324 414,344 414,394 364,376" fill="#6F6151" stroke="{INK_WARM}" stroke-width="1.7"/>')
        # Çekmece çizgileri ve kulplar
        s.append(f'<path d="M188,352 L188,408 M276,338 L276,392" fill="none" stroke="{INK_WARM}" stroke-width="1.4"/>')
        for cx_k, cy_k in [(142, 386), (230, 370), (318, 354)]:
            s.append(f'<path d="M{cx_k},{cy_k} L{cx_k+20},{cy_k-3}" fill="none" stroke="#3D3228" stroke-width="3.0" stroke-linecap="round"/>')
        # Sedye minderi (koyu klinik yeşil-petrol) + beyaz kâğıt muayene örtüsü
        s.append(f'<polygon points="90,342 362,302 422,324 148,370" fill="url(#{p}_bed_pad)" stroke="{INK_WARM}" stroke-width="1.8"/>')
        s.append(f'<polygon points="90,342 148,370 148,384 90,356" fill="#243536" stroke="{INK_WARM}" stroke-width="1.6"/>')
        s.append(f'<polygon points="148,370 422,324 422,338 148,384" fill="#314748" stroke="{INK_WARM}" stroke-width="1.6"/>')
        # Üstte hafif kırışık beyaz muayene kâğıdı + baş yastığı
        s.append(f'<polygon points="154,332 342,304 388,321 200,352" fill="#F2E6D2" stroke="{INK_WARM}" stroke-width="1.3"/>')
        s.append(f'<path d="M210,330 Q262,326 318,314 M242,338 Q290,331 352,321" fill="none" stroke="#CBBAA0" stroke-width="1.1"/>')
        # Baş yastığı (sağ uçta hafif eğimli)
        s.append(f'<polygon points="342,294 398,286 418,308 362,316" fill="#E6D7BE" stroke="{INK_WARM}" stroke-width="1.4"/>')

        # === 2) DOKTOR MASASI, DOSYA, STETOSKOP, PİRİNÇ ANAHTAR & SICAK LAMBA (Kimlik Öğesi 3) ===
        # Zemin temas gölgesi (R9)
        s.append(f'<polygon points="486,472 824,472 848,512 466,512" fill="#120B07" opacity="0.78"/>')
        # Masa gövdesi ve ayakları
        s.append(f'<rect x="514" y="384" width="12" height="104" fill="#4B3726" stroke="{INK_WARM}" stroke-width="1.6"/>')
        s.append(f'<rect x="786" y="384" width="12" height="104" fill="#4B3726" stroke="{INK_WARM}" stroke-width="1.6"/>')
        s.append(f'<rect x="694" y="384" width="96" height="92" fill="#59422F" stroke="{INK_WARM}" stroke-width="1.7"/>')
        s.append(f'<path d="M696,416 L788,416 M696,448 L788,448" fill="none" stroke="{INK_WARM}" stroke-width="1.4"/>')
        # Masa tablası
        s.append(f'<polygon points="496,368 814,368 832,390 478,390" fill="url(#{p}_table_top)" stroke="{INK_WARM}" stroke-width="1.9"/>')
        s.append(f'<rect x="478" y="390" width="354" height="12" fill="#543D2B" stroke="{INK_WARM}" stroke-width="1.7"/>')

        # Sıcak amber masa lambası (Anahtar ışık kaynağı — Sara'nın sıcak varlığı!)
        s.append(f'<ellipse cx="536" cy="378" rx="22" ry="6.5" fill="#4E3B2B" stroke="{INK_WARM}" stroke-width="1.4"/>')
        s.append(f'<path d="M536,374 C530,340 538,318 558,314" fill="none" stroke="#8C735B" stroke-width="4.5" stroke-linecap="round"/>')
        s.append(f'<path d="M536,374 C530,340 538,318 558,314" fill="none" stroke="{INK_WARM}" stroke-width="1.4" stroke-linecap="round"/>')
        # Lamba başlığı + sıcak ampul parıltısı
        s.append(f'<polygon points="546,304 584,312 596,332 544,324" fill="#3B534F" stroke="{INK_WARM}" stroke-width="1.6"/>')
        s.append(f'<ellipse cx="570" cy="328" rx="16" ry="6" fill="#FFF4D0" filter="url(#{p}_glow_warm)"/>')
        # Lambadan masaya düşen sıcak ışık konisi
        s.append(f'<polygon points="548,326 594,332 694,390 492,390" fill="#FFE2A1" opacity="0.22"/>')

        # Açık Tıbbi Dosya (masada)
        s.append(f'<polygon points="562,374 646,371 658,386 556,388" fill="#D4B47C" stroke="{INK_WARM}" stroke-width="1.4"/>')
        s.append(f'<polygon points="568,373 604,372 608,385 566,386" fill="#F8EED8" stroke="{INK_WARM}" stroke-width="0.9"/>')
        s.append(f'<polygon points="608,372 642,371 649,384 612,385" fill="#F2E5C9" stroke="{INK_WARM}" stroke-width="0.9"/>')
        s.append(f'<path d="M574,377 L598,376 M574,381 L596,380 M615,376 L638,375 M616,380 L634,379" fill="none" stroke="#6E5A44" stroke-width="1.0"/>')

        # Kıvrımlı Stetoskop (dosyanın sağında)
        s.append(
            f'<path d="M674,373 C660,368 658,384 678,385 C698,386 716,374 704,370 C694,367 686,375 696,382" '
            f'fill="none" stroke="#222B30" stroke-width="3.2" stroke-linecap="round"/>'
        )
        s.append(
            f'<path d="M674,373 C660,368 658,384 678,385 C698,386 716,374 704,370" '
            f'fill="none" stroke="#53656E" stroke-width="1.0" opacity="0.7"/>'
        )
        # Stetoskop diyafram başı
        s.append(f'<circle cx="698" cy="383" r="5.5" fill="#C9D3D6" stroke="{INK_WARM}" stroke-width="1.3"/>')
        s.append(f'<circle cx="698" cy="383" r="2.2" fill="#6F7D82"/>')

        # *** PİRİNÇ ANAHTAR (Masanın sağ kenarında sıcak ışıkta parlar — Sara'nın açık kapısı!) ***
        s.append(f'<ellipse cx="754" cy="380" rx="22" ry="6" fill="#FFE094" opacity="0.32"/>')
        s.append(f'<circle cx="742" cy="379" r="5.8" fill="none" stroke="url(#{p}_brass)" stroke-width="2.6"/>')
        s.append(f'<circle cx="742" cy="379" r="5.8" fill="none" stroke="{INK_WARM}" stroke-width="0.9"/>')
        s.append(f'<path d="M748,379 L772,379 M763,379 L763,384 M769,379 L769,383" fill="none" stroke="url(#{p}_brass)" stroke-width="2.6" stroke-linecap="round"/>')
        s.append(f'<path d="M748,378 L771,378" fill="none" stroke="#FFF9D6" stroke-width="1.0" opacity="0.9"/>')

        # Genel sıcak amber anahtar ışık sarmalaması
        s.append(f'<rect x="0" y="0" width="960" height="540" fill="url(#{p}_amber_key)"/>')
        s.append('</g>')
        parts.append("\n".join(s))

    # --- KATMAN 4: PLAN GÖRÜŞÜ (İnce, zarif #7FE6FF kapı kilidi & anahtar bağlantısı) ---
    if plan_gorusu and _katman_aktif(katmanlar, "plan"):
        pl: list[str] = [f'<g id="revir-plan" filter="url(#{p}_glow_cyan)" opacity="0.72">']
        # Pirinç anahtardan aralık kapı kilidine ince kesik rota (sıcak atmosferi bozmadan hibrit imza)
        pl.append(
            f'<path d="M756,370 L756,310 L750,310 L750,266" '
            f'fill="none" stroke="{PLAN}" stroke-width="1.25" stroke-dasharray="5,3"/>'
        )
        pl.append(f'<circle cx="756" cy="379" r="9.5" fill="none" stroke="{PLAN}" stroke-width="1.15" stroke-dasharray="3,2"/>')
        pl.append(f'<circle cx="750" cy="258" r="8.5" fill="none" stroke="{PLAN}" stroke-width="1.25"/>')
        pl.append(f'<circle cx="750" cy="258" r="2.0" fill="{PLAN_CORE}"/>')
        pl.append(f'<text x="763" y="254" fill="{PLAN_CORE}" font-family="Consolas,monospace" font-size="10.5" font-weight="bold">KİLİT · AÇIK</text>')
        pl.append('</g>')
        parts.append("\n".join(pl))

    # --- KATMAN 5: ÖN PLAN (Sıcak ışık zerreleri + sol ön köşede serum askısı silueti + vinyet) ---
    if _katman_aktif(katmanlar, "onplan"):
        f: list[str] = [f'<g id="revir-onplan">']
        # Sol ön köşede flu/koyu muayene perdesi / serum askısı silueti (derinlik çerçevesi)
        f.append(f'<path d="M0,0 L46,0 C38,160 54,340 28,540 L0,540 Z" fill="#1C140E" opacity="0.82"/>')
        f.append(f'<path d="M46,0 C38,160 54,340 28,540" fill="none" stroke="#6E5238" stroke-width="1.3" opacity="0.4"/>')
        # Sıcak ışıkta süzülen toz zerreleri
        for _ in range(24):
            dx = rng.uniform(340, 820)
            dy = rng.uniform(110, 480)
            dr = rng.uniform(0.9, 2.2)
            f.append(f'<circle cx="{dx:.1f}" cy="{dy:.1f}" r="{dr:.1f}" fill="#FFF0C8" opacity="{rng.uniform(0.22, 0.58):.2f}"/>')
        f.append(f'<rect x="0" y="0" width="960" height="540" fill="url(#{p}_vignette)"/>')
        f.append('</g>')
        parts.append("\n".join(f))

    return defs, "\n".join(parts)


# =============================================================================
# RENDER & KART OLUŞTURMA (1280x720 Mekân Kartı + 1280x720 R13 %200 Kırpma)
# =============================================================================
def _render_scene_pil(scene_fn, width: int = 1920, height: int = 1080,
                      plan_gorusu: bool = True) -> Image.Image:
    defs, body = scene_fn(plan_gorusu=plan_gorusu)
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {W_SCENE} {H_SCENE}">'
        f'<defs>{defs}</defs>'
        f'{body}'
        f'</svg>'
    )
    png_bytes = resvg_py.svg_to_bytes(svg_string=svg)
    return Image.open(io.BytesIO(png_bytes)).convert("RGBA")


def _load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = (
        ["C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf"]
        if bold else
        ["C:/Windows/Fonts/segoeui.ttf", "C:/Windows/Fonts/arial.ttf"]
    )
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def _draw_card_bg(w: int = 1280, h: int = 720) -> Image.Image:
    svg = f"""
    <svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
      <defs>
        <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0%" stop-color="#091019"/>
          <stop offset="55%" stop-color="#0F1824"/>
          <stop offset="100%" stop-color="#0A121C"/>
        </linearGradient>
      </defs>
      <rect width="{w}" height="{h}" fill="url(#bg)"/>
      <g stroke="#1C2B3D" stroke-width="1" opacity="0.28">
        {"".join(f'<line x1="{x}" y1="0" x2="{x}" y2="{h}"/>' for x in range(0, w, 64))}
        {"".join(f'<line x1="0" y1="{y}" x2="{w}" y2="{y}"/>' for y in range(0, h, 64))}
      </g>
    </svg>
    """
    return Image.open(io.BytesIO(resvg_py.svg_to_bytes(svg_string=svg))).convert("RGBA")


def _draw_panel_box(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int],
                    radius: int = 10, fill=(17, 26, 39, 235), outline=(42, 62, 86, 255)) -> None:
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=1)


def _draw_swatches(draw: ImageDraw.ImageDraw, x: int, y: int, colors: list[str],
                   size: int = 16, gap: int = 6) -> None:
    for i, hex_c in enumerate(colors):
        cx = x + i * (size + gap)
        draw.rounded_rectangle((cx, y, cx + size, y + size), radius=3, fill=hex_c, outline="#384D66", width=1)


def uret_kartlar(versiyon: str = "v1") -> tuple[Path, Path]:
    print("3 ana mekan 1920x1080 yuksek cozunurlukte render ediliyor...")
    img_depo = _render_scene_pil(mekan_depo, 1920, 1080)
    img_hucre = _render_scene_pil(mekan_hucre, 1920, 1080)
    img_revir = _render_scene_pil(mekan_revir, 1920, 1080)

    # =========================================================================
    # ÇIKTI 1: ANA MEKÂN KARTI (1280 x 720)
    # =========================================================================
    canvas = _draw_card_bg(1280, 720)
    draw = ImageDraw.Draw(canvas)

    f_title = _load_font(20, bold=True)
    f_sub = _load_font(12, bold=False)
    f_card_t = _load_font(13, bold=True)
    f_card_s = _load_font(11, bold=False)
    f_small = _load_font(10, bold=False)

    # Üst başlık barı
    draw.text((24, 14), "MICHAEL SCOFIELD  ·  ANA MEKÂN KARTLARI", fill="#EBF3FA", font=f_title)
    draw.text((24, 39), "STİL B+A HİBRİT (SİNEMATİK 2D + CAMGÖBEĞİ PLAN GÖRÜŞÜ)  ·  PROLOG & BÖLÜM I–III",
              fill="#7E97B0", font=f_sub)
    # Sağ üst genel palet özeti
    top_swatches = [("#0C1726", "DEPO"), ("#F6C367", "IŞIK"), ("#354A4D", "HÜCRE"),
                    ("#E8C89B", "REVİR"), ("#7FE6FF", "PLAN")]
    sx_top = 874
    for col, lbl in top_swatches:
        draw.rounded_rectangle((sx_top, 18, sx_top + 14, 32), radius=3, fill=col, outline="#3B536D", width=1)
        draw.text((sx_top + 19, 19), lbl, fill="#9BB2C8", font=f_small)
        sx_top += 76
    draw.line((24, 58, 1256, 58), fill="#213247", width=1)

    # --- ÜST SOL PANEL: 01 KARANLIK DEPO ---
    _draw_panel_box(draw, (22, 68, 630, 366))
    depo_thumb = img_depo.resize((448, 252), Image.Resampling.LANCZOS)
    canvas.paste(depo_thumb, (34, 98), depo_thumb)
    draw.rectangle((34, 98, 34 + 448, 98 + 252), outline="#2E455E", width=1)
    draw.text((34, 76), "01 · KARANLIK DEPO", fill="#F6C367", font=f_card_t)
    draw.text((196, 78), "Prolog & Bölüm I · \"Kapının altındaki ışık\"", fill="#8AA3BC", font=f_card_s)
    # Sağ bilgi kolonu (x=492..620)
    ix = 492
    draw.text((ix, 98), "PALET", fill="#7FE6FF", font=f_small)
    _draw_swatches(draw, ix, 114, ["#070D17", "#15243A", "#F6C367", "#FFF4D2", "#7FE6FF"], size=18, gap=5)
    draw.text((ix, 146), "KİMLİK ÖĞELERİ", fill="#9BB2C8", font=f_small)
    for k_i, item in enumerate([
        "• Kapı altı tek altın ışık",
        "• Ağır kilit sürgüsü",
        "• Tahta çatlak + plan",
        "• Eski ahşap sandıklar",
        "• Işık ucunda kâğıt turna",
    ]):
        draw.text((ix, 164 + k_i * 19), item, fill="#D5E2EE", font=f_card_s)
    draw.text((ix, 272), "ANAHTAR IŞIK", fill="#9BB2C8", font=f_small)
    draw.text((ix, 288), "Kapı aralığı altın huzme", fill="#F6C367", font=f_card_s)
    draw.text((ix, 314), "KATMANLAR (5)", fill="#9BB2C8", font=f_small)
    draw.text((ix, 330), "uzak · orta · sahne\nplan · önplan", fill="#8AA3BC", font=f_small)

    # --- ÜST SAĞ PANEL: 02 FOX RIVER HÜCRESİ ---
    _draw_panel_box(draw, (648, 68, 1256, 366))
    hucre_thumb = img_hucre.resize((448, 252), Image.Resampling.LANCZOS)
    canvas.paste(hucre_thumb, (660, 98), hucre_thumb)
    draw.rectangle((660, 98, 660 + 448, 98 + 252), outline="#2E455E", width=1)
    draw.text((660, 76), "02 · FOX RIVER HÜCRESİ", fill="#7FE6FF", font=f_card_t)
    draw.text((842, 78), "Bölüm III · \"Plan ve Kaçış\"", fill="#8AA3BC", font=f_card_s)
    ix2 = 1118
    draw.text((ix2, 98), "PALET", fill="#7FE6FF", font=f_small)
    _draw_swatches(draw, ix2, 114, ["#142126", "#354A4D", "#84B3AA", "#9BB0B6", "#7FE6FF"], size=18, gap=5)
    draw.text((ix2, 146), "KİMLİK ÖĞELERİ", fill="#9BB2C8", font=f_small)
    for k_i, item in enumerate([
        "• İki katlı çelik ranza",
        "• Parmaklık + çapraz gölge",
        "• Lavabo & altıgen cıvata",
        "• Camgöbeği kaçış hattı",
        "• Duvar rafı + kâğıt turna",
    ]):
        draw.text((ix2, 164 + k_i * 19), item, fill="#D5E2EE", font=f_card_s)
    draw.text((ix2, 272), "ANAHTAR IŞIK", fill="#9BB2C8", font=f_small)
    draw.text((ix2, 288), "Soğuk floresan + koridor", fill="#9BD1C8", font=f_card_s)
    draw.text((ix2, 314), "KATMANLAR (5)", fill="#9BB2C8", font=f_small)
    draw.text((ix2, 330), "uzak · orta · sahne\nplan · önplan", fill="#8AA3BC", font=f_small)

    # --- ALT BÜYÜK PANEL: 03 FOX RIVER REVİR + HİKÂYE/IŞIK ÖZETİ ---
    _draw_panel_box(draw, (22, 378, 1256, 704))
    revir_thumb = img_revir.resize((512, 288), Image.Resampling.LANCZOS)
    canvas.paste(revir_thumb, (34, 404), revir_thumb)
    draw.rectangle((34, 404, 34 + 512, 404 + 288), outline="#4E3F31", width=1)
    draw.text((34, 384), "03 · FOX RIVER REVİR", fill="#E8C89B", font=f_card_t)
    draw.text((208, 386), "Bölüm III · \"Sıcak Yakınlık ve Açık Kapı\" (İmge Yankısı 2)", fill="#9D8C78", font=f_card_s)

    # Orta-sağ Revir detay sütunu (x=564..864)
    rx = 564
    draw.text((rx, 404), "PALET (SICAK AMBER-KREM AYRIMI)", fill="#E8C89B", font=f_small)
    _draw_swatches(draw, rx, 422, ["#2A2018", "#5A4839", "#8C775E", "#E8C89B", "#FFF0C8", "#7FE6FF"], size=22, gap=7)
    draw.text((rx, 458), "KİMLİK ÖĞELERİ (4)", fill="#9BB2C8", font=f_small)
    for k_i, item in enumerate([
        "• Muayene sedyesi ve kâğıt örtü",
        "• Cam kapaklı ilaç / insülin dolabı (flakonlar)",
        "• Masa: açık tıbbi dosya, stetoskop, pirinç anahtar",
        "• Aralık duran revir kapısı ve sızan koridor ışığı",
    ]):
        draw.text((rx, 476 + k_i * 21), item, fill="#E3ECF5", font=f_card_s)
    draw.text((rx, 572), "ANAHTAR IŞIK & DUYGU", fill="#9BB2C8", font=f_small)
    draw.text((rx, 590), "Sıcak amber masa lambası + aralık kapı ışığı.\nFox River'ın soğuk yeşil-mavisinden ayrışarak\nSara'nın varlığını ve güveni taşır.",
              fill="#D4C2AB", font=f_card_s)
    draw.text((rx, 650), "KATMANLAR (5)", fill="#9BB2C8", font=f_small)
    draw.text((rx, 666), "revir-uzak · revir-orta · revir-sahne · revir-plan · revir-onplan",
              fill="#8AA3BC", font=f_small)

    # Sağ teknik/motor kutusu (x=896..1240)
    draw.line((880, 404, 880, 692), fill="#233447", width=1)
    tx = 898
    draw.text((tx, 404), "STİL B+A & MOTOR KATMAN MİMARİSİ", fill="#7FE6FF", font=f_card_t)
    notes = [
        ("BOOKEND IŞIK YANKISI",
         "Depo kapısı altındaki tek altın ışık çizgisi,\nRevir'de Sara'nın açık bıraktığı kapı aralığına\nevriliyor (soğuk → sıcak → açık kapı)."),
        ("PLAN GÖRÜŞÜ (#7FE6FF)",
         "Düşük örtük ketlenme anlarında tahta çatlağı,\nlavabo cıvatası ve revir kilidi numaralı plan\nhatlarıyla aydınlanır."),
        ("PARALAKS HAZIRLIĞI",
         "Her mekân 960×540 SVG'de 5 ayrı <g> katmanı\n(uzak/orta/sahne/plan/onplan) döndürür;\nstudyo/motor/ kamerasına doğrudan bağlanır."),
    ]
    ny = 432
    for heading, body_txt in notes:
        draw.text((tx, ny), heading, fill="#F6C367" if "BOOKEND" in heading else "#9EC5DE", font=f_small)
        draw.text((tx, ny + 16), body_txt, fill="#C5D5E4", font=f_card_s)
        ny += 86

    out_main = OUT_DIR / f"am_mekanlar_{versiyon}.png"
    canvas.convert("RGB").save(out_main, quality=95)

    # =========================================================================
    # ÇIKTI 2: R13 %200 KIRPMA KARTI (1280 x 720 — 4 PANEL)
    # =========================================================================
    r13 = _draw_card_bg(1280, 720)
    d13 = ImageDraw.Draw(r13)
    d13.text((24, 13), "R13 · %200 YAKINLAŞTIRMA KALİTE KONTROLÜ (ANA MEKÂNLAR)", fill="#EBF3FA", font=f_title)
    d13.text((24, 37), "1920×1080 KAYNAKTAN 1:1 PİKSEL KIRPMA  ·  DOKU, IŞIK, PERSPEKTİF VE PLAN ÇİZGİSİ DENETİMİ",
             fill="#7E97B0", font=f_sub)
    d13.line((24, 55, 1256, 55), fill="#213247", width=1)

    # 1920x1080 kaynakta 600x264 piksel kırpma -> tam %200 yakınlaştırma!
    cw, ch = 600, 264
    crops = [
        # (img, (cx_center, cy_center), title, subtitle, box_xy)
        (img_depo, (955, 575), "1 · DEPO KAPI ALTI IŞIK + TAHTA DOKUSU (%200)",
         "Kapı aralığı altın huzme, kilit sürgüsü, dikey tahta damarları", (22, 66)),
        (img_hucre, (985, 595), "2 · HÜCRE LAVABO / CIVATA + PLAN ÇİZGİSİ (%200)",
         "Paslanmaz çelik kombi ünite, altıgen cıvata, #7FE6FF rota hattı", (652, 66)),
        (img_revir, (1320, 445), "3 · REVİR İLAÇ DOLABI + ARALIK KAPI IŞIĞI (%200)",
         "Cam dolap flakon yansımaları, açık kapı aralığı ve kilit parıltısı", (22, 392)),
        (img_hucre, (455, 510), "4 · HÜCRE PARMAKLIK GÖLGESİ + RANZA DOKUSU (%200)",
         "Çelik ranza boruları, battaniye, beton blok derzleri, çapraz gölge", (652, 392)),
    ]

    for src_img, (cx, cy), title, sub, (bx, by) in crops:
        _draw_panel_box(d13, (bx, by, bx + 606, by + 314))
        x0 = max(0, min(src_img.width - cw, cx - cw // 2))
        y0 = max(0, min(src_img.height - ch, cy - ch // 2))
        patch = src_img.crop((x0, y0, x0 + cw, y0 + ch))
        r13.paste(patch, (bx + 3, by + 44), patch)
        d13.rectangle((bx + 3, by + 44, bx + 3 + cw, by + 44 + ch), outline="#2F465E", width=1)
        d13.text((bx + 12, by + 8), title, fill="#7FE6FF", font=f_card_t)
        d13.text((bx + 12, by + 25), sub, fill="#96AEC6", font=f_small)

    out_r13 = OUT_DIR / "am_mekanlar_r13.png"
    r13.convert("RGB").save(out_r13, quality=95)
    print(f"Kaydedildi:\n  - {out_main}\n  - {out_r13}")
    return out_main, out_r13


if __name__ == "__main__":
    uret_kartlar("v1")
