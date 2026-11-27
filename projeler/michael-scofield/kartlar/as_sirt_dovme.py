"""A-Sırt (Anatomik Sırt & Detaylı Özgün Tam Sırt Dövmesi) — Stil B + A Hibrit.

İzole modül: `prolog_blok.py` tarafından doğrudan import edilebilir:
  - sirt_dovme_svg(plan_glow=0.0) -> (defs_str, body_str)
    Yerel koordinat: 800×800, merkez (0, 0) sırt ortası (-400..400).
    plan_glow: 0.0 (gerçekçi koyu mürekkep #222E3B) -> 1.0 (gizli kat planı #7FE6FF parlar).

R1 sınırı: Dizideki gerçek şeytan/melek dövmesi ve gerçek oyuncu yüzü KESİNLİKLE kopyalanmaz.
Yalnızca özgün gotik-mimari kemer, ikiz origami kâğıt turna, vitray/taş filigran ve içine
gizlenmiş mimari hapishane kat planı (koridorlar, hücreler, altıgen cıvatalar, 01–04 noktaları)
yüksek işçilikli sinematik 2D olarak çizilir.
"""
from __future__ import annotations

import io
import math
import random
from pathlib import Path
import resvg_py
from PIL import Image

OUT_DIR = Path(__file__).resolve().parent

# ── Kilitli Stil B + A Hibrit Renk Paleti (A-Y v3 ile birebir uyumlu) ──
INK = "#1A1513"          # Ana dış kontur (2.1px)
INK_SOFT = "#422F26"     # İç anatomi konturları (1.1–1.4px)
INK_WARM = "#6E4936"     # Yumuşak kas/kemik geçiş hatları

SKIN_LIGHT = "#E9C5AC"   # Anahtar ışık düzlemi (sol-üst)
SKIN_BASE = "#D5A687"    # Ana ten rengi
SKIN_MID = "#BC8A6B"     # Yarı gölge
SKIN_SHADOW = "#97684E"  # Ana cel-gölge (sağ taraf)
SKIN_DEEP = "#724734"    # Derin gölge (koltuk altı, ense, omurga oluğu)
RIM_WARM = "#F5D9C3"     # Sıcak kenar rim ışığı

BUZZ_TOP = "#342C27"     # 1–2 numara buzzcut tepe tonu
BUZZ_MID = "#4B4039"     # Buzzcut şakak/ense fade geçişi
BUZZ_LIGHT = "#62544B"   # Tepe ışığı

PANTS_BASE = "#2B3646"   # Fox River koyu pantolon bel bandı
PANTS_DARK = "#1E2632"
PANTS_LIGHT = "#3B4A5F"

TATTOO_INK = "#222E3B"   # Cilde gömülü ana dövme mürekkebi
TATTOO_DARK = "#17202A"  # Koyu kontur/derinlik mürekkebi
TATTOO_SOFT = "#354656"  # İnce tarama ve gölgeleme mürekkebi
PLAN = "#7FE6FF"         # Camgöbeği plan görüşü
PLAN_CORE = "#E8FCFF"    # Parıltı iç çekirdeği
PLAN_DIM = "#3898B8"     # İkincil plan kılavuzu

_UID = 0


def _uid(prefix: str = "sd") -> str:
    global _UID
    _UID += 1
    return f"{prefix}_{_UID}"


def _clamp(v: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, float(v)))


def _lerp_hex(c1: str, c2: str, t: float) -> str:
    t = _clamp(t)
    r1, g1, b1 = int(c1[1:3], 16), int(c1[3:5], 16), int(c1[5:7], 16)
    r2, g2, b2 = int(c2[1:3], 16), int(c2[3:5], 16), int(c2[5:7], 16)
    r = int(round(r1 + (r2 - r1) * t))
    g = int(round(g1 + (g2 - g1) * t))
    b = int(round(b1 + (b2 - b1) * t))
    return f"#{r:02X}{g:02X}{b:02X}"


def _hex_bolt(cx: float, cy: float, r: float, stroke: str, sw: float, fill_inner: str = "none") -> str:
    """Altıgen cıvata / kilit sembolü."""
    pts = []
    for i in range(6):
        ang = math.radians(60 * i - 30)
        pts.append(f"{cx + r * math.cos(ang):.1f},{cy + r * math.sin(ang):.1f}")
    poly = "M" + " L".join(pts) + " Z"
    ir = r * 0.45
    return (
        f'<path d="{poly}" fill="{fill_inner}" stroke="{stroke}" stroke-width="{sw:.2f}" stroke-linejoin="round"/>'
        f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{ir:.1f}" fill="none" stroke="{stroke}" stroke-width="{sw * 0.85:.2f}"/>'
    )


def _origami_crane(side: int, ink: str, soft: str, plan_col: str, glow: float) -> str:
    """Kürek kemiği üzerinde kanatları açılmış özgün geometrik kâğıt turna.
    side: -1 (sol kürek kemiği), +1 (sağ kürek kemiği).
    Merkez yaklaşık x = side * 124, y = -22.
    """
    s = side

    def pt(lx: float, ly: float) -> tuple[float, float]:
        # Yerel turna koordinatından sırt koordinatına hafif diyagonal açıyla dönüştür
        # Kanat dış ucu omuz başına doğru hafif yukarı eğimli
        ang = math.radians(-11 * s)
        ca, sa = math.cos(ang), math.sin(ang)
        rx = lx * ca - ly * sa
        ry = lx * sa + ly * ca
        return (s * 124.0 + s * rx, -22.0 + ry)

    def P(lx: float, ly: float) -> str:
        x, y = pt(lx, ly)
        return f"{x:.1f},{y:.1f}"

    parts: list[str] = []

    # 1. Hafif mürekkep gölge yüzeyleri (kâğıt kat derinliği — cilt üzerinde yarı saydam)
    # Üst kanat ana düzlemi
    parts.append(
        f'<polygon points="{P(-44, 6)} {P(-8, -32)} {P(86, -42)} {P(38, 10)} {P(0, 14)}" '
        f'fill="{ink}" fill-opacity="0.11" stroke="none"/>'
    )
    # Alt-arka kanat gölge düzlemi
    parts.append(
        f'<polygon points="{P(-34, 8)} {P(2, -14)} {P(68, -6)} {P(18, 34)} {P(-18, 22)}" '
        f'fill="{ink}" fill-opacity="0.17" stroke="none"/>'
    )
    # Boyun ve kuyruk üçgenleri
    parts.append(
        f'<polygon points="{P(-44, 6)} {P(-64, -38)} {P(-30, -18)} {P(-16, 12)}" '
        f'fill="{ink}" fill-opacity="0.15" stroke="none"/>'
    )
    parts.append(
        f'<polygon points="{P(18, 34)} {P(54, 64)} {P(28, 12)}" '
        f'fill="{ink}" fill-opacity="0.14" stroke="none"/>'
    )

    # 2. Ana dış kontur (keskin origami silueti)
    outline_paths = [
        # Dış kanat üst & alt kenar
        f"M{P(-44, 6)} L{P(-8, -32)} L{P(86, -42)} L{P(58, -12)} L{P(38, 10)} L{P(18, 34)} L{P(-18, 22)} Z",
        # Arka/alt kanat uç çıkıntısı
        f"M{P(58, -12)} L{P(74, -4)} L{P(34, 18)}",
        # Boyun ve baş (merkez kemere doğru bakar)
        f"M{P(-44, 6)} L{P(-66, -42)} L{P(-54, -46)} L{P(-30, -18)}",
        # Gaga
        f"M{P(-66, -42)} L{P(-78, -34)} L{P(-59, -32)}",
        # Kuyruk (kürek kemiği altına uzanan keskin üçgen)
        f"M{P(18, 34)} L{P(56, 66)} L{P(32, 16)}",
    ]
    for d in outline_paths:
        parts.append(
            f'<path d="{d}" fill="none" stroke="{ink}" stroke-width="1.65" '
            f'stroke-linecap="round" stroke-linejoin="round" opacity="0.88"/>'
        )

    # 3. İç çokgen kat izleri (origami geometrik yüzeyleri)
    crease_paths = [
        f"M{P(-44, 6)} L{P(38, 10)}",
        f"M{P(-8, -32)} L{P(18, 34)}",
        f"M{P(-8, -32)} L{P(38, 10)}",
        f"M{P(86, -42)} L{P(0, 14)}",
        f"M{P(86, -42)} L{P(-18, 22)}",
        f"M{P(-30, -18)} L{P(0, 14)}",
        f"M{P(-30, -18)} L{P(-18, 22)}",
        f"M{P(-66, -42)} L{P(-44, 6)}",
        f"M{P(0, 14)} L{P(56, 66)}",
        f"M{P(20, -16)} L{P(58, -12)}",
        f"M{P(20, -16)} L{P(-8, -32)}",
        f"M{P(20, -16)} L{P(38, 10)}",
    ]
    for d in crease_paths:
        parts.append(
            f'<path d="{d}" fill="none" stroke="{ink}" stroke-width="1.05" '
            f'stroke-linecap="round" opacity="0.76"/>'
        )

    # 4. İnce iç tarama (engraving/hatching çizgileri — kâğıt gölge düzlemlerinde)
    for k in range(1, 7):
        t = k / 7.0
        # Kanat içi paralel tarama
        x1 = -4 + t * 52
        y1 = -24 + t * 8
        x2 = 10 + t * 44
        y2 = 12 - t * 6
        parts.append(
            f'<path d="M{P(x1, y1)} L{P(x2, y2)}" fill="none" stroke="{soft}" '
            f'stroke-width="0.7" opacity="0.52"/>'
        )
    # Kuyruk içi ince kesikli kat ekseni
    parts.append(
        f'<path d="M{P(10, 18)} L{P(48, 56)}" fill="none" stroke="{soft}" '
        f'stroke-width="0.85" stroke-dasharray="3,2.5" opacity="0.65"/>'
    )

    # 5. Kanat ucundan omuz başına uzanan ince mimari ölçüm yayları & filigran
    arc_cx, arc_cy = pt(34, -12)
    parts.append(
        f'<circle cx="{arc_cx:.1f}" cy="{arc_cy:.1f}" r="42" fill="none" '
        f'stroke="{soft}" stroke-width="0.85" stroke-dasharray="4,3" opacity="0.58"/>'
    )
    parts.append(
        f'<circle cx="{arc_cx:.1f}" cy="{arc_cy:.1f}" r="54" fill="none" '
        f'stroke="{ink}" stroke-width="0.75" opacity="0.45"/>'
    )
    # Küçük elmas & hedef nişangâh düğümü
    nx, ny = pt(86, -42)
    parts.append(
        f'<circle cx="{nx:.1f}" cy="{ny:.1f}" r="3.2" fill="none" stroke="{ink}" stroke-width="1.1" opacity="0.8"/>'
    )

    # 6. Plan görüşü aktifken turna eksenlerinde ince camgöbeği rezonans
    if glow > 0.02:
        go = 0.25 + 0.65 * glow
        parts.append(
            f'<path d="M{P(-66, -42)} L{P(-44, 6)} L{P(0, 14)} L{P(86, -42)}" '
            f'fill="none" stroke="{plan_col}" stroke-width="1.35" opacity="{go:.2f}" '
            f'stroke-linecap="round" stroke-linejoin="round"/>'
        )
        parts.append(
            f'<path d="M{P(-8, -32)} L{P(18, 34)} L{P(56, 66)}" '
            f'fill="none" stroke="{plan_col}" stroke-width="1.0" stroke-dasharray="4,3" '
            f'opacity="{go * 0.78:.2f}"/>'
        )
        cx0, cy0 = pt(0, 14)
        parts.append(
            f'<circle cx="{cx0:.1f}" cy="{cy0:.1f}" r="3.0" fill="{PLAN_CORE}" opacity="{go:.2f}"/>'
        )

    return "\n".join(parts)


def _shoulder_filigree(side: int, ink: str, soft: str) -> str:
    """Deltoid omuz başlarına sarılan gotik-geometrik kemer ve çark filigranı."""
    s = side
    parts: list[str] = []

    # Omuz başı kavisli kemer kaburgaları
    ox = s * 188.0
    oy = -28.0
    parts.append(
        f'<path d="M{s * 148:.1f},-88 C{s * 195:.1f},-82 {s * 238:.1f},-42 {s * 244:.1f},18 '
        f'C{s * 246:.1f},54 {s * 234:.1f},88 {s * 212:.1f},112" '
        f'fill="none" stroke="{ink}" stroke-width="1.5" opacity="0.72"/>'
    )
    parts.append(
        f'<path d="M{s * 156:.1f},-76 C{s * 194:.1f},-68 {s * 228:.1f},-34 {s * 232:.1f},18 '
        f'C{s * 234:.1f},48 {s * 224:.1f},76 {s * 204:.1f},98" '
        f'fill="none" stroke="{ink}" stroke-width="1.15" opacity="0.65"/>'
    )
    # Aradaki geometrik taş/kafes bölmeleri
    for i in range(6):
        t = i / 5.0
        ang = math.radians(-58 + t * 112)
        r1, r2 = 34.0, 52.0
        cx, cy = s * 190.0, 6.0
        x1 = cx + s * r1 * math.cos(ang)
        y1 = cy + r1 * math.sin(ang)
        x2 = cx + s * r2 * math.cos(ang)
        y2 = cy + r2 * math.sin(ang)
        parts.append(
            f'<path d="M{x1:.1f},{y1:.1f} L{x2:.1f},{y2:.1f}" fill="none" '
            f'stroke="{soft}" stroke-width="0.95" opacity="0.62"/>'
        )
    # Omuz ortasında yarım rozet / çark motifi
    parts.append(
        f'<circle cx="{s * 206:.1f}" cy="12" r="22" fill="none" stroke="{ink}" stroke-width="1.2" opacity="0.62"/>'
    )
    parts.append(
        f'<circle cx="{s * 206:.1f}" cy="12" r="14" fill="none" stroke="{soft}" stroke-width="0.9" '
        f'stroke-dasharray="3,2" opacity="0.58"/>'
    )
    parts.append(_hex_bolt(s * 206.0, 12.0, 6.5, ink, 1.0))

    # Alt deltoid üçgen sarkıtı
    parts.append(
        f'<path d="M{s * 194:.1f},44 L{s * 222:.1f},44 L{s * 208:.1f},82 Z" '
        f'fill="{ink}" fill-opacity="0.10" stroke="{ink}" stroke-width="1.15" opacity="0.7"/>'
    )
    parts.append(
        f'<path d="M{s * 208:.1f},44 L{s * 208:.1f},98" fill="none" stroke="{soft}" stroke-width="0.9" opacity="0.65"/>'
    )
    return "\n".join(parts)


def _tattoo_layers(plan_glow: float, glow_filter_id: str) -> str:
    """5 katmanlı yüksek detaylı özgün tam sırt dövmesi."""
    g = _clamp(plan_glow)
    ink = TATTOO_INK
    dark = TATTOO_DARK
    soft = TATTOO_SOFT

    parts: list[str] = []

    # ── KATMAN 1: MERKEZ GOTİK KATEDRAL / HAPİSHANE KEMERİ & SÜTUNLAR ──
    # Arka hafif mürekkep dolgu (kemer derinliği)
    parts.append(
        '<path d="M-56,225 L-56,-42 C-56,-84 -24,-112 0,-128 C24,-112 56,-84 56,-42 L56,225 Z" '
        f'fill="{ink}" fill-opacity="0.09" stroke="none"/>'
    )
    parts.append(
        '<path d="M-40,218 L-40,-36 C-40,-70 -16,-94 0,-108 C16,-94 40,-70 40,-36 L40,218 Z" '
        f'fill="{ink}" fill-opacity="0.08" stroke="none"/>'
    )

    # 3 kademeli sivri gotik kemer kaburgası (archivolts)
    for dx, top_y, sw, op in [
        (60, -134, 1.9, 0.90),
        (50, -122, 1.35, 0.84),
        (38, -108, 1.15, 0.78),
        (26, -94, 0.9, 0.65),
    ]:
        parts.append(
            f'<path d="M{-dx},232 L{-dx},-40 C{-dx},{-40 - dx * 0.75:.1f} {-dx * 0.42:.1f},{top_y + 18:.1f} '
            f'0,{top_y} C{dx * 0.42:.1f},{top_y + 18:.1f} {dx},{-40 - dx * 0.75:.1f} {dx},-40 L{dx},232" '
            f'fill="none" stroke="{ink}" stroke-width="{sw:.2f}" opacity="{op:.2f}" stroke-linejoin="round"/>'
        )

    # Kemer taş örgü radyal derz çizgileri (voussoirs)
    for k in range(-7, 8):
        ang = math.radians(k * 11.5 - 90)
        x1 = 38 * math.cos(ang)
        y1 = -56 + 52 * math.sin(ang)
        x2 = 60 * math.cos(ang)
        y2 = -58 + 74 * math.sin(ang)
        parts.append(
            f'<path d="M{x1:.1f},{y1:.1f} L{x2:.1f},{y2:.1f}" fill="none" '
            f'stroke="{soft}" stroke-width="0.85" opacity="0.62"/>'
        )

    # Tepe Gül Pencere / Kilit Taşı Rozeti (y = -72)
    rcy = -72.0
    for r, sw, op, dash in [
        (24.0, 1.4, 0.86, ""),
        (17.5, 1.0, 0.78, ""),
        (11.0, 0.9, 0.75, "2.5,2"),
        (5.2, 1.1, 0.85, ""),
    ]:
        da = f' stroke-dasharray="{dash}"' if dash else ""
        parts.append(
            f'<circle cx="0" cy="{rcy:.1f}" r="{r:.1f}" fill="none" stroke="{ink}" '
            f'stroke-width="{sw:.2f}" opacity="{op:.2f}"{da}/>'
        )
    # 12'li radyal vitray kolları ve küçük yaprak kemerleri
    for i in range(12):
        a = math.radians(i * 30)
        x1, y1 = 5.2 * math.cos(a), rcy + 5.2 * math.sin(a)
        x2, y2 = 24.0 * math.cos(a), rcy + 24.0 * math.sin(a)
        parts.append(
            f'<path d="M{x1:.1f},{y1:.1f} L{x2:.1f},{y2:.1f}" fill="none" '
            f'stroke="{ink}" stroke-width="0.8" opacity="0.72"/>'
        )
        # Dış taş elmasları
        a_mid = math.radians(i * 30 + 15)
        mx, my = 20.5 * math.cos(a_mid), rcy + 20.5 * math.sin(a_mid)
        parts.append(
            f'<circle cx="{mx:.1f}" cy="{my:.1f}" r="1.4" fill="{ink}" opacity="0.72"/>'
        )

    # Tepe kulesi / enseye uzanan gotik alem (finial, y = -134..-158)
    parts.append(
        f'<path d="M0,-134 L0,-158 M-10,-142 L0,-152 L10,-142 M-6,-136 L0,-144 L6,-136" '
        f'fill="none" stroke="{ink}" stroke-width="1.35" stroke-linecap="round" opacity="0.85"/>'
    )
    parts.append(
        f'<polygon points="0,-163 4,-157 0,-151 -4,-157" fill="{ink}" fill-opacity="0.78"/>'
    )

    # İki yanda yivli dikey sütunlar + sütun başlıkları + destek payandaları
    for s in (-1, 1):
        # Dikey yivler
        for xoff, sw in [(54, 1.1), (60, 1.6), (67, 1.15), (73, 1.4)]:
            parts.append(
                f'<path d="M{s * xoff},-36 L{s * xoff},226" fill="none" stroke="{ink}" '
                f'stroke-width="{sw:.2f}" opacity="0.78"/>'
            )
        # Sütun başlığı (y = -42..-26) ve orta bilezik (y = +78) ve taban (y = +218..+232)
        for by in (-36, 78, 222):
            parts.append(
                f'<path d="M{s * 48},{by - 4} L{s * 79},{by - 4} L{s * 76},{by + 5} L{s * 51},{by + 5} Z" '
                f'fill="{ink}" fill-opacity="0.22" stroke="{ink}" stroke-width="1.15" opacity="0.82"/>'
            )
        # Üst uçan payandalar (flying buttresses — kemeri kürek kemiklerine bağlar)
        parts.append(
            f'<path d="M{s * 60},-72 Q{s * 92},-74 {s * 120},-56" fill="none" stroke="{ink}" stroke-width="1.4" opacity="0.78"/>'
        )
        parts.append(
            f'<path d="M{s * 60},-62 Q{s * 88},-64 {s * 112},-46" fill="none" stroke="{soft}" stroke-width="1.0" opacity="0.68"/>'
        )
        # Payanda içi dikey çubuklar
        for bx in (74, 86, 98):
            parts.append(
                f'<path d="M{s * bx},-68 L{s * bx},-55" fill="none" stroke="{soft}" stroke-width="0.85" opacity="0.65"/>'
            )

    # Merkez dikey omurga vitray/kafes ızgarası (y = -42..+222)
    for y in range(-32, 218, 18):
        # İnce gotik pencere çaprazları
        parts.append(
            f'<path d="M-24,{y} L24,{y}" fill="none" stroke="{soft}" stroke-width="0.65" opacity="0.48"/>'
        )
        parts.append(
            f'<path d="M-24,{y} L0,{y + 9} L24,{y}" fill="none" stroke="{soft}" stroke-width="0.65" opacity="0.42"/>'
        )
    # Orta omurga dikey kılavuz çifti
    parts.append(
        f'<path d="M-7,-46 L-7,242 M7,-46 L7,242" fill="none" stroke="{ink}" stroke-width="0.9" opacity="0.62"/>'
    )

    # ── KATMAN 1B: TRAPEZ / ÜST OMUZ SPANDREL FİLİGRANI & TAŞ DOKUSU (y = -114..-44) ──
    for s in (-1, 1):
        # Trapez boyunca kavisli mimari köprü kemeri (kemer tepesinden omuza bağlanır)
        parts.append(
            f'<path d="M{s * 34},-112 C{s * 74},-104 {s * 116},-92 {s * 158},-76" '
            f'fill="none" stroke="{ink}" stroke-width="1.25" opacity="0.72"/>'
        )
        parts.append(
            f'<path d="M{s * 42},-102 C{s * 78},-94 {s * 114},-82 {s * 148},-66" '
            f'fill="none" stroke="{soft}" stroke-width="0.9" stroke-dasharray="3.5,2.5" opacity="0.62"/>'
        )
        # Spandrel içi küçük geometrik pusula/dişli rozeti (x = ±92, y = -76)
        parts.append(
            f'<circle cx="{s * 92}" cy="-76" r="11" fill="none" stroke="{ink}" stroke-width="0.95" opacity="0.65"/>'
        )
        parts.append(
            f'<circle cx="{s * 92}" cy="-76" r="6" fill="none" stroke="{soft}" stroke-width="0.8" opacity="0.6"/>'
        )
        for k in range(8):
            a = math.radians(k * 45)
            x1 = s * 92 + 6 * math.cos(a)
            y1 = -76 + 6 * math.sin(a)
            x2 = s * 92 + 11 * math.cos(a)
            y2 = -76 + 11 * math.sin(a)
            parts.append(
                f'<path d="M{x1:.1f},{y1:.1f} L{x2:.1f},{y2:.1f}" fill="none" stroke="{ink}" stroke-width="0.75" opacity="0.62"/>'
            )
        # Yan kemer ile merkez sütun arası ince yatay taş derzleri (ashlar masonry)
        for ty in range(-22, 206, 22):
            parts.append(
                f'<path d="M{s * 73},{ty} L{s * 80},{ty}" fill="none" stroke="{soft}" stroke-width="0.8" opacity="0.58"/>'
            )
        # Sütun üzeri ince çapraz gravür tarama (cross-hatching)
        for hy in range(-28, 212, 12):
            parts.append(
                f'<path d="M{s * 54},{hy} L{s * 60},{hy + 6}" fill="none" stroke="{soft}" stroke-width="0.6" opacity="0.44"/>'
            )
            parts.append(
                f'<path d="M{s * 67},{hy + 6} L{s * 73},{hy}" fill="none" stroke="{soft}" stroke-width="0.6" opacity="0.44"/>'
            )

    # ── KATMAN 2: YAN HAPİSHANE PENCERE KEMERLERİ & FİLİGRAN (x = ±80..±168, y = +40..+230) ──
    for s in (-1, 1):
        # Dış sivri yan kemer
        parts.append(
            f'<path d="M{s * 80},212 L{s * 80},76 C{s * 80},46 {s * 102},32 {s * 118},24 '
            f'C{s * 134},32 {s * 156},46 {s * 156},76 L{s * 156},196 C{s * 144},208 {s * 114},214 {s * 80},212 Z" '
            f'fill="{ink}" fill-opacity="0.08" stroke="{ink}" stroke-width="1.5" opacity="0.82"/>'
        )
        # İç yan kemer
        parts.append(
            f'<path d="M{s * 88},204 L{s * 88},80 C{s * 88},58 {s * 105},46 {s * 118},39 '
            f'C{s * 131},46 {s * 148},58 {s * 148},80 L{s * 148},190" '
            f'fill="none" stroke="{ink}" stroke-width="1.05" opacity="0.72"/>'
        )
        # Yan kemer içi dikey hapishane parmaklıkları & vitray baklavaları
        for px in (98, 108, 118, 128, 138):
            parts.append(
                f'<path d="M{s * px},52 L{s * px},196" fill="none" stroke="{soft}" stroke-width="0.75" opacity="0.52"/>'
            )
        # Yatay kat çizgileri (hücre katları gibi okunan mimari bölmeler)
        for py in (78, 106, 134, 162, 188):
            parts.append(
                f'<path d="M{s * 86},{py} L{s * 150},{py}" fill="none" stroke="{ink}" stroke-width="0.85" opacity="0.62"/>'
            )
        # Yan kemer üstü gotik üç yaprak (trefoil) niş
        parts.append(
            f'<circle cx="{s * 118}" cy="56" r="7" fill="none" stroke="{ink}" stroke-width="0.95" opacity="0.72"/>'
        )
        parts.append(
            f'<circle cx="{s * 111}" cy="64" r="5" fill="none" stroke="{ink}" stroke-width="0.85" opacity="0.65"/>'
        )
        parts.append(
            f'<circle cx="{s * 125}" cy="64" r="5" fill="none" stroke="{ink}" stroke-width="0.85" opacity="0.65"/>'
        )
        # Dış bel/latissimus geometrik kanat filigranı
        parts.append(
            f'<path d="M{s * 156},88 C{s * 176},96 {s * 184},122 {s * 174},154 '
            f'C{s * 166},176 {s * 150},196 {s * 132},216" '
            f'fill="none" stroke="{ink}" stroke-width="1.25" opacity="0.72"/>'
        )
        parts.append(
            f'<path d="M{s * 156},104 L{s * 173},118 L{s * 156},132 L{s * 170},148 L{s * 152},166" '
            f'fill="none" stroke="{soft}" stroke-width="0.95" opacity="0.65"/>'
        )

    # ── KATMAN 3: ALT SIRTTA TERS KEMER / MAHZEN & PRİZMA KİLİT TABANI (y = +218..+302) ──
    parts.append(
        f'<path d="M-86,216 L0,298 L86,216" fill="{ink}" fill-opacity="0.09" '
        f'stroke="{ink}" stroke-width="1.65" stroke-linejoin="round" opacity="0.86"/>'
    )
    parts.append(
        f'<path d="M-66,222 L0,282 L66,222" fill="none" stroke="{ink}" stroke-width="1.15" opacity="0.76"/>'
    )
    parts.append(
        f'<path d="M-44,228 L0,264 L44,228" fill="none" stroke="{soft}" stroke-width="0.95" opacity="0.68"/>'
    )
    # Alt mahzen 3'lü küçük kemer dizisi
    for cx in (-34, 0, 34):
        parts.append(
            f'<path d="M{cx - 12},246 L{cx - 12},232 C{cx - 12},223 {cx - 5},218 {cx},216 '
            f'C{cx + 5},218 {cx + 12},223 {cx + 12},232 L{cx + 12},246" '
            f'fill="none" stroke="{ink}" stroke-width="1.05" opacity="0.75"/>'
        )
    # Alt merkez elmas mührü
    parts.append(
        f'<polygon points="0,286 8,298 0,310 -8,298" fill="{ink}" fill-opacity="0.25" '
        f'stroke="{ink}" stroke-width="1.2" opacity="0.82"/>'
    )

    # ── KATMAN 4: İKİZ KÂĞIT TURNA (KÜREK KEMİKLERİ) + OMUZ FİLİGRANI ──
    parts.append(_origami_crane(-1, ink, soft, PLAN, g))
    parts.append(_origami_crane(1, ink, soft, PLAN, g))
    parts.append(_shoulder_filigree(-1, ink, soft))
    parts.append(_shoulder_filigree(1, ink, soft))

    # ── KATMAN 5: GİZLİ MİMARİ HAPİSHANE KAT PLANI (MÜREKKEP İÇİNDE GÖMÜLÜ + PLAN GÖRÜŞÜNDE PARLAR) ──
    # Normal durumda koyu mürekkep (#17202A/#222E3B) ile çizili; plan_glow > 0 olunca #7FE6FF ile yanar.
    plan_paths_main = [
        # Ana kaçış tüneli / boru hattı rotası: 01 (kilit taşı) -> merkez dikey -> 02 (sağ kavşak) -> orta geçiş -> 03 (sol blok) -> 04 (alt tahliye)
        "M0,-72 L0,-18 L24,-18 L24,42 L92,42 L92,92 L38,92 L38,118 L-104,118 L-104,174 L-22,174 L-22,228 L58,228",
        # İkincil havalandırma/boru kolu (sol üst hücre bloğu -> 01)
        "M-118,-10 L-76,-10 L-76,-54 L-26,-54 L-26,-72 L0,-72",
        # Sağ üst şaft bağlantısı (02 -> sağ omuz kilit rozeti)
        "M92,42 L134,42 L134,12 L198,12",
    ]
    plan_cells = [
        # Sağ A-Blok gizli hücre sıraları (küçük dikdörtgen bölmeler)
        "M92,78 L142,78 L142,102 L92,102 Z M108,78 L108,102 M125,78 L125,102",
        "M92,108 L142,108 L142,132 L92,132 Z M108,108 L108,132 M125,108 L125,132",
        # Sol B-Blok gizli hücre sıraları
        "M-142,78 L-92,78 L-92,102 L-142,102 Z M-125,78 L-125,102 M-108,78 L-108,102",
        "M-142,136 L-92,136 L-92,160 L-142,160 Z M-125,136 L-125,160 M-108,136 L-108,160",
        # Merkez avlu / revir dikdörtgen şeması
        "M-28,6 L28,6 L28,64 L-28,64 Z",
        "M-18,138 L22,138 L22,192 L-18,192 Z",
    ]
    plan_ticks = [
        # Teknik ölçüm kılavuzları (kısa çizgiler ve eksenler)
        "M-48,-72 L-30,-72 M30,-72 L48,-72",
        "M-46,42 L-34,42 M34,42 L48,42",
        "M-148,118 L-114,118 M102,42 L116,42",
        "M0,236 L0,276",
        "M-56,174 L-32,174 M32,174 L56,174",
    ]
    # Koordinat düğümleri: (x, y, etiket, lx_off, ly_off)
    nodes = [
        (0.0, -72.0, "01", 15.0, -10.0),
        (92.0, 42.0, "02", 14.0, -10.0),
        (-104.0, 118.0, "03", -26.0, -10.0),
        (58.0, 228.0, "04", 13.0, 4.0),
    ]
    # Altıgen cıvata / kilit noktaları
    bolts = [
        (0.0, -18.0, 5.5),
        (-76.0, -10.0, 5.2),
        (92.0, 92.0, 5.2),
        (-104.0, 174.0, 5.2),
        (0.0, 174.0, 6.0),
    ]

    # 5a) Her zaman cilde işli koyu mürekkep katmanı (plan_glow=0 iken gizli detay)
    for d in plan_cells:
        parts.append(
            f'<path d="{d}" fill="none" stroke="{ink}" stroke-width="0.95" opacity="0.68"/>'
        )
    for d in plan_paths_main:
        parts.append(
            f'<path d="{d}" fill="none" stroke="{dark}" stroke-width="1.35" '
            f'stroke-linecap="round" stroke-linejoin="round" opacity="0.72"/>'
        )
    for d in plan_ticks:
        parts.append(
            f'<path d="{d}" fill="none" stroke="{soft}" stroke-width="0.85" '
            f'stroke-dasharray="2.5,2.5" opacity="0.65"/>'
        )
    for bx, by, br in bolts:
        parts.append(_hex_bolt(bx, by, br, dark, 1.05))
    for nx, ny, lbl, dx, dy in nodes:
        parts.append(
            f'<circle cx="{nx:.1f}" cy="{ny:.1f}" r="5.2" fill="none" stroke="{dark}" stroke-width="1.15" opacity="0.78"/>'
        )
        parts.append(
            f'<circle cx="{nx:.1f}" cy="{ny:.1f}" r="1.8" fill="{dark}" opacity="0.82"/>'
        )
        parts.append(
            f'<text x="{nx + dx:.1f}" y="{ny + dy:.1f}" font-family="Consolas, monospace" '
            f'font-size="9.5" font-weight="700" fill="{dark}" opacity="0.75">{lbl}</text>'
        )

    # 5b) Camgöbeği Plan Görüşü Işıma Katmanı (plan_glow > 0)
    if g > 0.01:
        parts.append(f'<g opacity="{g:.2f}">')
        # Dış parıltı (glow filtresi ile)
        parts.append(f'<g filter="url(#{glow_filter_id})">')
        for d in plan_paths_main:
            parts.append(
                f'<path d="{d}" fill="none" stroke="{PLAN}" stroke-width="4.2" '
                f'stroke-linecap="round" stroke-linejoin="round" opacity="0.78"/>'
            )
        for d in plan_cells:
            parts.append(
                f'<path d="{d}" fill="none" stroke="{PLAN}" stroke-width="2.2" opacity="0.58"/>'
            )
        for nx, ny, _, _, _ in nodes:
            parts.append(
                f'<circle cx="{nx:.1f}" cy="{ny:.1f}" r="8.5" fill="none" stroke="{PLAN}" stroke-width="2.4" opacity="0.85"/>'
            )
        parts.append("</g>")

        # Keskin parlak çekirdek çizgiler
        for d in plan_cells:
            parts.append(
                f'<path d="{d}" fill="none" stroke="{PLAN}" stroke-width="1.15" opacity="0.88"/>'
            )
        for d in plan_ticks:
            parts.append(
                f'<path d="{d}" fill="none" stroke="{PLAN}" stroke-width="0.95" '
                f'stroke-dasharray="3,2.5" opacity="0.82"/>'
            )
        for d in plan_paths_main:
            parts.append(
                f'<path d="{d}" fill="none" stroke="{PLAN}" stroke-width="2.3" '
                f'stroke-linecap="round" stroke-linejoin="round"/>'
            )
            parts.append(
                f'<path d="{d}" fill="none" stroke="{PLAN_CORE}" stroke-width="0.95" '
                f'stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="10,4"/>'
            )
        for bx, by, br in bolts:
            parts.append(_hex_bolt(bx, by, br, PLAN, 1.35))
        for nx, ny, lbl, dx, dy in nodes:
            parts.append(
                f'<circle cx="{nx:.1f}" cy="{ny:.1f}" r="6.2" fill="none" stroke="{PLAN}" stroke-width="1.5"/>'
            )
            parts.append(
                f'<circle cx="{nx:.1f}" cy="{ny:.1f}" r="2.6" fill="{PLAN_CORE}"/>'
            )
            parts.append(
                f'<text x="{nx + dx:.1f}" y="{ny + dy:.1f}" font-family="Consolas, monospace" '
                f'font-size="11" font-weight="700" fill="{PLAN_CORE}">{lbl}</text>'
            )
        # Gül pencere + merkez kemer ince camgöbeği çerçeve vurgusu
        parts.append(
            f'<circle cx="0" cy="-72" r="24" fill="none" stroke="{PLAN}" stroke-width="1.15" '
            f'stroke-dasharray="5,3" opacity="0.65"/>'
        )
        parts.append("</g>")

    # ── İnce dotwork / stipple kenar geçişi (gerçekçi dövme dokusu) ──
    rng = random.Random(94941)
    dots: list[str] = []
    for _ in range(150):
        # Kemer ve yan filigran çevresinde simetrik hafif noktalama
        dx = rng.uniform(52, 162)
        dy = rng.uniform(-62, 224)
        # Kürek kemiği ve kemer boşluklarını yoğunlaştır
        if abs(dx - 115) < 42 and -60 < dy < 205:
            r = rng.uniform(0.55, 1.05)
            op = rng.uniform(0.22, 0.45)
            dots.append(f'<circle cx="{dx:.1f}" cy="{dy:.1f}" r="{r:.2f}" fill="{ink}" opacity="{op:.2f}"/>')
            dots.append(f'<circle cx="{-dx:.1f}" cy="{dy:.1f}" r="{r:.2f}" fill="{ink}" opacity="{op:.2f}"/>')
    parts.append("\n".join(dots))

    return "\n".join(parts)


def _buzzcut_head_back(uid: str, glow: float) -> tuple[str, str]:
    """A-Y v3 ile birebir uyumlu 1–2 numara kazınmış buzzcut baş arkası + kulaklar + ense."""
    g = _clamp(glow)
    head_clip = f"{uid}_head_clip"
    hair_grad = f"{uid}_hair_grad"
    fade_grad = f"{uid}_fade_grad"
    skin_neck = f"{uid}_neck_grad"

    # Kafa arkası silueti: üst parietal dolgunluk, kulak üstü hafif daralma, occipital kavis
    head_path = (
        "M0,-346 "
        "C44,-346 73,-322 75,-276 "
        "C76,-250 71,-222 61,-200 "
        "C52,-182 34,-170 0,-168 "
        "C-34,-170 -52,-182 -61,-200 "
        "C-71,-222 -76,-250 -75,-276 "
        "C-73,-322 -44,-346 0,-346 Z"
    )

    defs = f"""
    <clipPath id="{head_clip}">
      <path d="{head_path}"/>
    </clipPath>
    <radialGradient id="{hair_grad}" cx="36%" cy="28%" r="72%">
      <stop offset="0%" stop-color="{BUZZ_LIGHT}"/>
      <stop offset="38%" stop-color="{BUZZ_MID}"/>
      <stop offset="80%" stop-color="{BUZZ_TOP}"/>
      <stop offset="100%" stop-color="#221C18"/>
    </radialGradient>
    <linearGradient id="{fade_grad}" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="{BUZZ_TOP}" stop-opacity="0.98"/>
      <stop offset="56%" stop-color="{BUZZ_MID}" stop-opacity="0.95"/>
      <stop offset="74%" stop-color="{BUZZ_MID}" stop-opacity="0.62"/>
      <stop offset="86%" stop-color="{BUZZ_MID}" stop-opacity="0.22"/>
      <stop offset="96%" stop-color="{SKIN_BASE}" stop-opacity="0.0"/>
    </linearGradient>
    <linearGradient id="{skin_neck}" x1="15%" y1="0%" x2="85%" y2="20%">
      <stop offset="0%" stop-color="{SKIN_LIGHT}"/>
      <stop offset="48%" stop-color="{SKIN_BASE}"/>
      <stop offset="80%" stop-color="{SKIN_SHADOW}"/>
      <stop offset="100%" stop-color="{SKIN_DEEP}"/>
    </linearGradient>
    """

    # Kulaklar (arkadan görünüş: dış kıkırdak kavisi + antihelix + kulak arkası gölgesi)
    ears: list[str] = []
    for s in (-1, 1):
        ear_fill = SKIN_BASE if s == -1 else SKIN_SHADOW
        ear_hi = SKIN_LIGHT if s == -1 else SKIN_MID
        ears.append(
            f'<path d="M{s * 71},-270 C{s * 86},-274 {s * 91},-258 {s * 88},-241 '
            f'C{s * 86},-227 {s * 81},-216 {s * 71},-216 C{s * 65},-216 {s * 64},-226 {s * 66},-242 Z" '
            f'fill="{ear_fill}" stroke="{INK}" stroke-width="2.0" stroke-linejoin="round"/>'
        )
        # Kulak arkası kıkırdak sırtı ve iç gölge
        ears.append(
            f'<path d="M{s * 74},-264 C{s * 82},-262 {s * 84},-248 {s * 80},-234 '
            f'C{s * 78},-227 {s * 74},-223 {s * 70},-223" '
            f'fill="none" stroke="{INK_SOFT}" stroke-width="1.2" opacity="0.72"/>'
        )
        if s == -1:
            ears.append(
                f'<path d="M-76,-266 C-83,-262 -86,-250 -84,-238" '
                f'fill="none" stroke="{ear_hi}" stroke-width="1.5" stroke-linecap="round" opacity="0.75"/>'
            )

    # Deterministik buzzcut stipple (kısa kazınmış saç kökleri)
    rng = random.Random(2026)
    stipples: list[str] = []
    for _ in range(320):
        px = rng.uniform(-72, 72)
        py = rng.uniform(-344, -184)
        # Elips içi kontrolü
        nx = px / 74.0
        ny = (py + 260.0) / 86.0
        if nx * nx + ny * ny <= 0.96:
            # Enseye doğru seyrekleşen fade
            if py > -216 and rng.random() > (1.0 - (py + 216.0) / 34.0):
                continue
            r = rng.uniform(0.55, 1.15)
            col = "#1E1815" if px > 12 else "#2B2420"
            op = rng.uniform(0.28, 0.58)
            stipples.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{r:.2f}" fill="{col}" opacity="{op:.2f}"/>')

    rim_col = _lerp_hex(RIM_WARM, PLAN, g * 0.72)

    body = f"""
    <g id="{uid}_head_group">
      <!-- Kulaklar (kafa arkası altında) -->
      {''.join(ears)}

      <!-- Kafa arkası ten tabanı (ense fade görünümü için) -->
      <path d="{head_path}" fill="url(#{skin_neck})" stroke="none"/>

      <!-- Buzzcut saç dolgusu + enseye doğru yumuşak taper fade -->
      <g clip-path="url(#{head_clip})">
        <!-- Üst ve orta kafatası saç dolgusu (alt enseye doğru yumuşakça ten rengine erir) -->
        <rect x="-80" y="-352" width="160" height="190" fill="url(#{hair_grad})" opacity="0.86"/>
        <path d="M-76,-222 C-54,-208 -34,-196 0,-196 C34,-196 54,-208 76,-222 L76,-160 L-76,-160 Z"
              fill="url(#{skin_neck})" opacity="0.92"/>
        <!-- Yumuşak fade katmanı (sert yatay sınır olmadan kavisli geçiş) -->
        <path d="M-76,-228 C-52,-214 -30,-200 0,-198 C30,-200 52,-214 76,-228 L76,-352 L-76,-352 Z"
              fill="url(#{fade_grad})"/>
        <ellipse cx="0" cy="-196" rx="46" ry="18" fill="{BUZZ_MID}" opacity="0.22"/>
        <!-- Sol-üst anahtar ışık kafa derisi yansıması -->
        <ellipse cx="-24" cy="-306" rx="34" ry="22" fill="{BUZZ_LIGHT}" opacity="0.34" transform="rotate(-18 -24 -306)"/>
        <!-- Sağ taraf derin cel-gölge -->
        <path d="M22,-346 C54,-336 76,-308 76,-266 C76,-224 56,-184 18,-168 L84,-168 L84,-352 Z"
              fill="#171210" opacity="0.34"/>
        <!-- Buzzcut stipple saç kökleri -->
        {''.join(stipples)}
        <!-- Sağ kenar ince rim ışığı -->
        <path d="M44,-334 C66,-316 74,-286 73,-252 C72,-226 62,-204 46,-186"
              fill="none" stroke="{rim_col}" stroke-width="2.1" stroke-linecap="round" opacity="0.58"/>
      </g>

      <!-- Kafa dış konturu (2.1px #1A1513) -->
      <path d="{head_path}" fill="none" stroke="{INK}" stroke-width="2.1" stroke-linejoin="round"/>
    </g>
    """
    return defs, body


def sirt_dovme_svg(plan_glow: float = 0.0) -> tuple[str, str]:
    """Anatomik yetişkin erkek sırtı + 5 katmanlı özgün tam sırt dövmesi SVG üretir.

    Dönüş: (defs_str, body_str)
    Koordinat sistemi: 800×800, merkez (0, 0) sırt ortası (-400..+400).
    """
    g = _clamp(plan_glow)
    uid = _uid("sirt")

    torso_clip = f"{uid}_torso_clip"
    skin_grad = f"{uid}_skin_grad"
    arm_l_grad = f"{uid}_arm_l_grad"
    arm_r_grad = f"{uid}_arm_r_grad"
    glow_id = f"{uid}_plan_glow"
    pants_grad = f"{uid}_pants_grad"

    head_defs, head_body = _buzzcut_head_back(uid, g)

    # ── ANATOMİK SİLUETLER (Atletik, ince-kaslı yetişkin erkek sırtı — kaba yamuk YOK) ──
    # Ana sırt + ense + trapez + deltoid + üst kol birleşik gövde silueti
    # (Kollar koltuk altından aşağı ayrı konturlanır; dövme clipPath'i gövde+omuzları kapsar)
    torso_and_shoulders = (
        "M-49,-186 "
        # Sol ense -> trapez kavis -> sol deltoid omuz başı
        "C-51,-158 -58,-144 -78,-132 "
        "C-112,-112 -156,-106 -196,-92 "
        "C-234,-78 -262,-44 -270,8 "
        "C-276,48 -270,92 -264,132 "
        "C-258,184 -253,262 -246,366 "
        # Sol kol alt kenarından iç kol / koltuk altı hattına dönüş
        "L-192,366 "
        "C-194,264 -197,184 -204,114 "
        "C-206,96 -208,78 -204,64 "
        # Sol latissimus dorsi -> atletik V-daralması -> bel
        "C-196,98 -188,142 -176,184 "
        "C-164,226 -152,262 -148,316 "
        # Bel alt çizgisi
        "L148,316 "
        # Sağ bel -> sağ latissimus dorsi V-genişlemesi
        "C152,262 164,226 176,184 "
        "C188,142 196,98 204,64 "
        # Sağ koltuk altı -> sağ iç kol
        "C208,78 206,96 204,114 "
        "C197,184 194,264 192,366 "
        "L246,366 "
        # Sağ dış kol (triceps) -> sağ deltoid omuz başı -> sağ trapez -> sağ ense
        "C253,262 258,184 264,132 "
        "C270,92 276,48 270,8 "
        "C262,-44 234,-78 196,-92 "
        "C156,-106 112,-112 78,-132 "
        "C58,-144 51,-158 49,-186 Z"
    )

    # Sadece gövde + omuz başları (dövmenin kollara taşmaması için clipPath)
    tattoo_clip_path = (
        "M-49,-186 "
        "C-51,-158 -58,-144 -78,-132 "
        "C-112,-112 -156,-106 -196,-92 "
        "C-234,-78 -260,-44 -268,8 "
        "C-272,44 -266,86 -248,118 "
        "C-232,126 -214,106 -204,64 "
        "C-196,98 -188,142 -176,184 "
        "C-164,226 -152,262 -148,316 "
        "L148,316 "
        "C152,262 164,226 176,184 "
        "C188,142 196,98 204,64 "
        "C214,106 232,126 248,118 "
        "C266,86 272,44 268,8 "
        "C260,-44 234,-78 196,-92 "
        "C156,-106 112,-112 78,-132 "
        "C58,-144 51,-158 49,-186 Z"
    )

    rim_col = _lerp_hex(RIM_WARM, PLAN, g * 0.76)

    defs_str = f"""
    {head_defs}
    <clipPath id="{torso_clip}">
      <path d="{tattoo_clip_path}"/>
    </clipPath>
    <linearGradient id="{skin_grad}" x1="14%" y1="6%" x2="88%" y2="86%">
      <stop offset="0%" stop-color="{SKIN_LIGHT}"/>
      <stop offset="34%" stop-color="{SKIN_BASE}"/>
      <stop offset="70%" stop-color="{SKIN_MID}"/>
      <stop offset="100%" stop-color="{SKIN_SHADOW}"/>
    </linearGradient>
    <linearGradient id="{arm_l_grad}" x1="0%" y1="0%" x2="100%" y2="20%">
      <stop offset="0%" stop-color="{SKIN_LIGHT}"/>
      <stop offset="55%" stop-color="{SKIN_BASE}"/>
      <stop offset="100%" stop-color="{SKIN_SHADOW}"/>
    </linearGradient>
    <linearGradient id="{arm_r_grad}" x1="0%" y1="0%" x2="100%" y2="20%">
      <stop offset="0%" stop-color="{SKIN_MID}"/>
      <stop offset="55%" stop-color="{SKIN_SHADOW}"/>
      <stop offset="100%" stop-color="{SKIN_DEEP}"/>
    </linearGradient>
    <linearGradient id="{pants_grad}" x1="15%" y1="0%" x2="85%" y2="100%">
      <stop offset="0%" stop-color="{PANTS_LIGHT}"/>
      <stop offset="48%" stop-color="{PANTS_BASE}"/>
      <stop offset="100%" stop-color="{PANTS_DARK}"/>
    </linearGradient>
    <filter id="{glow_id}" x="-28%" y="-28%" width="156%" height="156%">
      <feGaussianBlur stdDeviation="5.2" result="blur"/>
    </filter>
    """

    tattoo_svg = _tattoo_layers(g, glow_id)

    # Plan aktifken sırtta çok hafif soğuk camgöbeği atmosferik yansıma
    plan_tint = ""
    if g > 0.02:
        plan_tint = (
            f'<path d="{torso_and_shoulders}" fill="{PLAN}" fill-opacity="{0.06 * g:.3f}" stroke="none"/>'
        )

    body_str = f"""
    <g id="{uid}_root">
      <!-- 1. ANA VÜCUT TEN DOLGUSU (Sırt + Omuzlar + Arka Kollar) -->
      <path d="{torso_and_shoulders}" fill="url(#{skin_grad})" stroke="none"/>

      <!-- Sol ve sağ arka kol hacim gradyanları -->
      <path d="M-270,8 C-276,48 -270,92 -264,132 C-258,184 -253,262 -246,366 L-192,366 C-194,264 -197,184 -204,114 C-206,96 -208,78 -204,64 C-216,44 -244,24 -270,8 Z"
            fill="url(#{arm_l_grad})" opacity="0.58" stroke="none"/>
      <path d="M270,8 C276,48 270,92 264,132 C258,184 253,262 246,366 L192,366 C194,264 197,184 204,114 C206,96 208,78 204,64 C216,44 244,24 270,8 Z"
            fill="url(#{arm_r_grad})" opacity="0.65" stroke="none"/>

      <!-- 2. ANATOMİK IŞIK & CEL-GÖLGE DÜZLEMLERİ (Sol-üst anahtar ışık, sağ derin gölge) -->
      <g clip-path="url(#{torso_clip})">
        <!-- Sol-üst anahtar ışık düzlemleri (trapez, deltoid, sol kürek kemiği, sol bel sütunu) -->
        <path d="M-46,-178 C-56,-146 -84,-126 -146,-106 C-202,-88 -244,-54 -258,-6 C-262,18 -254,48 -238,68 C-228,28 -212,-14 -176,-34 C-136,-56 -88,-84 -44,-112 C-34,-134 -34,-158 -46,-178 Z"
              fill="{SKIN_LIGHT}" opacity="0.72"/>
        <!-- Sol kürek kemiği (scapula) üst ışığı -->
        <path d="M-168,-54 C-132,-70 -84,-64 -54,-38 C-48,-8 -58,28 -86,52 C-122,38 -154,10 -168,-54 Z"
              fill="{SKIN_LIGHT}" opacity="0.46"/>
        <!-- Sol erector spinae (omurga sol kas sütunu) ışığı -->
        <path d="M-46,72 C-24,84 -16,136 -18,216 C-20,256 -28,286 -44,306 C-66,274 -72,210 -66,144 C-62,110 -56,88 -46,72 Z"
              fill="{SKIN_LIGHT}" opacity="0.38"/>

        <!-- Ense & baş altı düşme gölgesi -->
        <path d="M-54,-188 C-34,-166 34,-166 54,-188 L58,-154 C28,-138 -24,-138 -56,-154 Z"
              fill="{SKIN_DEEP}" opacity="0.48"/>
        <!-- Ense dikey kas çukuru (nuchal furrow) -->
        <path d="M-9,-172 L9,-172 L5,-124 L-5,-124 Z" fill="{SKIN_SHADOW}" opacity="0.42"/>
        <!-- C7 omur çıkıntısı hafif ışık noktası -->
        <ellipse cx="-2" cy="-126" rx="11" ry="6" fill="{SKIN_LIGHT}" opacity="0.45"/>

        <!-- Omurga oluğu (spinal furrow) derinlik gölgesi -->
        <path d="M-10,-112 C-14,-40 -12,48 -14,136 C-16,204 -12,262 -6,312 L14,312 C18,256 18,192 16,128 C14,48 16,-40 10,-112 Z"
              fill="{SKIN_SHADOW}" opacity="0.34"/>
        <path d="M-3,-104 C-4,-20 -3,80 -4,180 C-4,234 -2,276 0,308 L8,308 C10,264 10,204 9,144 C8,60 8,-24 5,-104 Z"
              fill="{SKIN_DEEP}" opacity="0.26"/>

        <!-- Sağ taraf derin cel-gölge düzlemi (trapez altı, sağ kürek kemiği, sağ latissimus, sağ deltoid) -->
        <path d="M46,-178 C58,-144 86,-126 146,-106 C206,-86 254,-48 268,10 C272,56 260,98 242,126 L204,64 C194,112 182,174 166,238 L148,316 L44,316 C64,254 78,188 84,122 C90,56 76,-14 54,-74 C44,-104 38,-142 46,-178 Z"
              fill="{SKIN_SHADOW}" opacity="0.44"/>
        <!-- Sağ kürek kemiği alt gölge düzlemi -->
        <path d="M62,-28 C98,-44 148,-46 178,-22 C186,18 170,58 134,82 C96,74 68,44 62,-28 Z"
              fill="{SKIN_SHADOW}" opacity="0.32"/>
        <!-- Sağ dış deltoid ve latissimus derin gölgesi -->
        <path d="M196,-92 C238,-74 266,-36 270,12 C272,58 256,102 238,124 L204,64 C196,106 184,164 164,236 L148,316 L112,316 C134,244 152,166 164,96 C174,40 198,-26 196,-92 Z"
              fill="{SKIN_DEEP}" opacity="0.38"/>
        <!-- Sol koltuk altı (posterior axillary fold) derin gölge -->
        <path d="M-204,64 C-194,96 -184,136 -170,186 C-182,148 -192,114 -192,76 C-192,48 -178,24 -156,6 C-180,18 -198,38 -204,64 Z"
              fill="{SKIN_DEEP}" opacity="0.46"/>
        <!-- Alt sırt bel gamzeleri (PSIS) yumuşak gölgeler -->
        <ellipse cx="-44" cy="284" rx="10" ry="6" fill="{SKIN_SHADOW}" opacity="0.34" transform="rotate(-14 -44 284)"/>
        <ellipse cx="44" cy="284" rx="10" ry="6" fill="{SKIN_DEEP}" opacity="0.38" transform="rotate(14 44 284)"/>
      </g>

      <!-- 3. YÜKSEK DETAYLI ÖZGÜN TAM SIRT DÖVMESİ (Vücut siluetine kırpılmış) -->
      <g clip-path="url(#{torso_clip})">
        {tattoo_svg}
        <!-- Dövmenin cilde gömülmesi için çok hafif anatomik gölge perdesi (sağ yarı + koltuk altı) -->
        <path d="M36,-140 L276,-140 L276,320 L36,320 C68,220 76,80 36,-140 Z"
              fill="{SKIN_DEEP}" opacity="0.11" stroke="none"/>
        <!-- Sol-üst hafif cilt parlaklığı (mürekkep üzerinden yumuşak ışık geçer) -->
        <ellipse cx="-142" cy="-42" rx="76" ry="44" fill="{SKIN_LIGHT}" opacity="0.11" transform="rotate(-18 -142 -42)"/>
      </g>

      {plan_tint}

      <!-- 4. İNCE ANATOMİK İÇ KONTURLAR (1.1–1.4px #422F26, fill="none") -->
      <!-- Ense kas sütunları ve trapez üst geçişi -->
      <path d="M-22,-168 C-24,-146 -30,-128 -48,-114" fill="none" stroke="{INK_SOFT}" stroke-width="1.2" opacity="0.58"/>
      <path d="M22,-168 C24,-146 30,-128 48,-114" fill="none" stroke="{INK_SOFT}" stroke-width="1.25" opacity="0.68"/>
      <!-- Omurga merkez çizgisi -->
      <path d="M0,-118 C-1,-38 1,56 0,164 C-1,222 0,268 0,302"
            fill="none" stroke="{INK_SOFT}" stroke-width="1.2" opacity="0.48"/>
      <!-- Sol & sağ kürek kemiği (scapula) alt-iç anatomik sınırları -->
      <path d="M-56,-34 C-52,10 -66,46 -98,64 C-128,54 -154,30 -168,-4"
            fill="none" stroke="{INK_WARM}" stroke-width="1.2" opacity="0.52" stroke-linecap="round"/>
      <path d="M56,-34 C52,10 66,46 98,64 C128,54 154,30 168,-4"
            fill="none" stroke="{INK_SOFT}" stroke-width="1.3" opacity="0.62" stroke-linecap="round"/>
      <!-- Arka deltoid -> triceps ayrım kıvrımları -->
      <path d="M-254,48 C-234,64 -216,70 -204,64 C-208,34 -202,6 -184,-16"
            fill="none" stroke="{INK_SOFT}" stroke-width="1.35" opacity="0.68" stroke-linecap="round"/>
      <path d="M254,48 C234,64 216,70 204,64 C208,34 202,6 184,-16"
            fill="none" stroke="{INK_SOFT}" stroke-width="1.45" opacity="0.76" stroke-linecap="round"/>
      <!-- Arka kol (triceps) uzun baş / yan baş ayrımı -->
      <path d="M-238,108 C-232,148 -226,188 -228,236" fill="none" stroke="{INK_WARM}" stroke-width="1.15" opacity="0.48"/>
      <path d="M238,108 C232,148 226,188 228,236" fill="none" stroke="{INK_SOFT}" stroke-width="1.25" opacity="0.58"/>
      <!-- Alt sırt (latissimus / thoracolumbar fascia) yumuşak konturu -->
      <path d="M-164,174 C-136,192 -94,204 -56,216" fill="none" stroke="{INK_WARM}" stroke-width="1.05" opacity="0.42"/>
      <path d="M164,174 C136,192 94,204 56,216" fill="none" stroke="{INK_SOFT}" stroke-width="1.15" opacity="0.52"/>

      <!-- 5. SAĞ KENAR SİNEMATİK RİM IŞIĞI (Sıcak veya Plan Camgöbeği) -->
      <path d="M84,-128 C126,-108 168,-100 204,-86 C238,-72 262,-36 268,14 C272,56 266,102 258,154"
            fill="none" stroke="{rim_col}" stroke-width="2.2" stroke-linecap="round" opacity="{0.52 + 0.34 * g:.2f}"/>
      <path d="M196,94 C186,144 172,202 154,284"
            fill="none" stroke="{rim_col}" stroke-width="1.6" stroke-linecap="round" opacity="{0.36 + 0.34 * g:.2f}"/>

      <!-- 6. ANA DIŞ KONTUR (2.1px #1A1513) + KOLTUK ALTI KIVRIMI -->
      <path d="{torso_and_shoulders}" fill="none" stroke="{INK}" stroke-width="2.1" stroke-linejoin="round"/>
      <!-- Kol-gövde ayrım iç çizgileri (koltuk altı üst uzantısı) -->
      <path d="M-204,64 C-198,46 -188,30 -174,18" fill="none" stroke="{INK}" stroke-width="1.8" stroke-linecap="round"/>
      <path d="M204,64 C198,46 188,30 174,18" fill="none" stroke="{INK}" stroke-width="1.8" stroke-linecap="round"/>

      <!-- 7. ALT BEL FOX RIVER PANTOLON BANDI (Temiz çerçeve sonlandırması, y = 308..366) -->
      <path d="M-150,308 C-86,320 86,320 150,308 L156,366 L-156,366 Z"
            fill="url(#{pants_grad})" stroke="{INK}" stroke-width="2.1" stroke-linejoin="round"/>
      <path d="M-148,324 C-84,335 84,335 148,324" fill="none" stroke="{INK}" stroke-width="1.3" opacity="0.72"/>
      <!-- Kemer köprüleri ve dikiş çizgisi -->
      <rect x="-92" y="311" width="12" height="24" rx="2" fill="{PANTS_DARK}" stroke="{INK}" stroke-width="1.4"/>
      <rect x="-6" y="315" width="12" height="24" rx="2" fill="{PANTS_DARK}" stroke="{INK}" stroke-width="1.4"/>
      <rect x="80" y="311" width="12" height="24" rx="2" fill="{PANTS_DARK}" stroke="{INK}" stroke-width="1.4"/>
      <path d="M-146,315 C-84,326 84,326 146,315" fill="none" stroke="{PANTS_LIGHT}" stroke-width="0.9"
            stroke-dasharray="4,3" opacity="0.55"/>

      <!-- 8. BUZZCUT BAŞ ARKASI (En üst katman — enseye doğal oturur) -->
      {head_body}
    </g>
    """
    return defs_str, body_str


# ── KART ŞABLONU VE RENDER YARDIMCILARI ───────────────────────────────────────

def _render_svg_to_png(svg_str: str, out_path: Path, width: int = 1280, height: int = 720) -> None:
    png_bytes = resvg_py.svg_to_bytes(svg_str, width=width, height=height)
    img = Image.open(io.BytesIO(png_bytes))
    img.save(out_path, format="PNG")


def _rising_blueprint_overlay(x: float, y: float) -> str:
    """Sağ panelde sırtın arkasından/yanından yükselen Stil B+A kat planı katmanı."""
    return f"""
    <g transform="translate({x:.1f},{y:.1f})" opacity="0.62">
      <!-- Arka plan ince teknik ızgara -->
      <rect x="-256" y="-266" width="512" height="456" fill="none" stroke="{PLAN}" stroke-width="0.6" opacity="0.24"/>
      {"".join(f'<path d="M{gx},-266 L{gx},190" fill="none" stroke="{PLAN}" stroke-width="0.45" opacity="0.16"/>' for gx in range(-200, 250, 50))}
      {"".join(f'<path d="M-256,{gy} L256,{gy}" fill="none" stroke="{PLAN}" stroke-width="0.45" opacity="0.16"/>' for gy in range(-216, 190, 50))}

      <!-- Yükselen üst-sağ Fox River şematik kat planı kutusu -->
      <g transform="translate(86, -242)">
        <rect x="0" y="0" width="166" height="104" fill="#091A26" fill-opacity="0.68" stroke="{PLAN}" stroke-width="1.35"/>
        <path d="M0,36 L66,36 M66,0 L66,104 M114,0 L114,62 L166,62 M66,72 L124,72 L124,104"
              fill="none" stroke="{PLAN}" stroke-width="1.0" opacity="0.88"/>
        <path d="M18,18 L48,18 L48,84 L92,84 L92,32 L140,32 L140,86"
              fill="none" stroke="{PLAN_CORE}" stroke-width="1.5" stroke-dasharray="5,3"/>
        <circle cx="18" cy="18" r="3.4" fill="{PLAN_CORE}"/>
        <circle cx="92" cy="84" r="3.4" fill="{PLAN_CORE}"/>
        <circle cx="140" cy="32" r="3.4" fill="{PLAN_CORE}"/>
        <circle cx="140" cy="86" r="3.4" fill="{PLAN_CORE}"/>
        <text x="24" y="15" font-family="Consolas, monospace" font-size="8.5" fill="{PLAN_CORE}">01</text>
        <text x="98" y="82" font-family="Consolas, monospace" font-size="8.5" fill="{PLAN_CORE}">02</text>
        <text x="146" y="29" font-family="Consolas, monospace" font-size="8.5" fill="{PLAN_CORE}">03</text>
        <text x="146" y="94" font-family="Consolas, monospace" font-size="8.5" fill="{PLAN_CORE}">04</text>
        <text x="4" y="-6" font-family="Consolas, monospace" font-size="9" fill="{PLAN}">FOX RIVER · SEKTÖR A-B</text>
      </g>

      <!-- Sırttan yukarı bağlanan ince kesikli projeksiyon hatları -->
      <path d="M0,-58 C26,-122 60,-168 104,-224" fill="none" stroke="{PLAN}" stroke-width="1.1" stroke-dasharray="4,3.5" opacity="0.78"/>
      <path d="M74,34 C118,-44 154,-104 178,-158" fill="none" stroke="{PLAN}" stroke-width="1.05" stroke-dasharray="4,3.5" opacity="0.68"/>
      <path d="M-84,96 C-156,28 -196,-74 -180,-184" fill="none" stroke="{PLAN}" stroke-width="0.95" stroke-dasharray="3,4" opacity="0.52"/>

      <!-- Sol üst ince ölçüm dairesi -->
      <circle cx="-178" cy="-188" r="34" fill="none" stroke="{PLAN}" stroke-width="0.95" stroke-dasharray="4,3" opacity="0.55"/>
      <circle cx="-178" cy="-188" r="20" fill="none" stroke="{PLAN}" stroke-width="0.75" opacity="0.45"/>
      <path d="M-220,-188 L-136,-188 M-178,-230 L-178,-146" fill="none" stroke="{PLAN}" stroke-width="0.65" opacity="0.45"/>
    </g>
    """


def build_model_card() -> str:
    """1280×720 Model Kartı: Sol = Normal koyu mürekkep, Sağ = Plan görüşü aktif."""
    d_norm, b_norm = sirt_dovme_svg(plan_glow=0.0)
    d_plan, b_plan = sirt_dovme_svg(plan_glow=1.0)

    swatches = [
        ("TEN", SKIN_BASE),
        ("SAÇ", BUZZ_TOP),
        ("MÜREKKEP", TATTOO_INK),
        ("PLAN", PLAN),
    ]
    sw_svg = []
    sx = 924
    for name, col in swatches:
        sw_svg.append(
            f'<rect x="{sx}" y="18" width="15" height="15" rx="3" fill="{col}" stroke="#43566B" stroke-width="1"/>'
            f'<text x="{sx + 21}" y="29.5" font-family="Segoe UI, sans-serif" font-size="10.2" fill="#9BB2C7">{name}</text>'
        )
        sx += 80 if name != "MÜREKKEP" else 102

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720" viewBox="0 0 1280 720">
  <defs>
    <linearGradient id="card_bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0D151F"/>
      <stop offset="100%" stop-color="#141F2C"/>
    </linearGradient>
    <radialGradient id="panel_glow_l" cx="50%" cy="46%" r="58%">
      <stop offset="0%" stop-color="#223041"/>
      <stop offset="100%" stop-color="#111A24"/>
    </radialGradient>
    <radialGradient id="panel_glow_r" cx="50%" cy="46%" r="60%">
      <stop offset="0%" stop-color="#173347"/>
      <stop offset="100%" stop-color="#0D1721"/>
    </radialGradient>
    <clipPath id="clip_left">
      <rect x="24" y="58" width="604" height="638" rx="12"/>
    </clipPath>
    <clipPath id="clip_right">
      <rect x="652" y="58" width="604" height="638" rx="12"/>
    </clipPath>
    {d_norm}
    {d_plan}
  </defs>

  <!-- Arka plan -->
  <rect width="1280" height="720" fill="url(#card_bg)"/>

  <!-- Üst başlık şeridi (çakışmasız temiz yerleşim) -->
  <text x="26" y="33" font-family="Segoe UI, sans-serif" font-size="16.5" font-weight="700" fill="#EDF4FA" letter-spacing="0.4">
    MICHAEL SCOFIELD · ANATOMİK SIRT &amp; DÖVME v1
  </text>
  <text x="456" y="32" font-family="Segoe UI, sans-serif" font-size="11" fill="#7B97B0" letter-spacing="0.3">
    STİL B+A HİBRİT · GOTİK-MİMARİ + İKİZ TURNA + GİZLİ PLAN
  </text>
  {"".join(sw_svg)}

  <!-- SOL PANEL: NORMAL KOYU MÜREKKEP -->
  <rect x="24" y="58" width="604" height="638" rx="12" fill="url(#panel_glow_l)" stroke="#293A4C" stroke-width="1.3"/>
  <g clip-path="url(#clip_left)">
    <g transform="translate(326, 396) scale(0.84)">
      {b_norm}
    </g>
    <!-- Alt yumuşak okunabilirlik bandı -->
    <rect x="24" y="654" width="604" height="42" fill="#0B131C" fill-opacity="0.72"/>
    <!-- Panel etiketi -->
    <rect x="38" y="72" width="296" height="28" rx="6" fill="#0B121B" fill-opacity="0.86" stroke="#2D4155" stroke-width="1"/>
    <text x="50" y="90" font-family="Segoe UI, sans-serif" font-size="11.8" font-weight="600" fill="#DCE8F2">
      1. NORMAL DURUM · KOYU MÜREKKEP (#222E3B)
    </text>
    <text x="326" y="680" text-anchor="middle" font-family="Segoe UI, sans-serif" font-size="11.5" fill="#9BB3C8">
      Atletik sırt anatomisi · 1–2 numara buzzcut fade · cilde gömülü özgün dövme
    </text>
  </g>

  <!-- SAĞ PANEL: PLAN GÖRÜŞÜ AKTİF -->
  <rect x="652" y="58" width="604" height="638" rx="12" fill="url(#panel_glow_r)" stroke="#2E637C" stroke-width="1.4"/>
  <g clip-path="url(#clip_right)">
    {_rising_blueprint_overlay(954, 396)}
    <g transform="translate(954, 396) scale(0.84)">
      {b_plan}
    </g>
    <rect x="652" y="654" width="604" height="42" fill="#08141E" fill-opacity="0.74"/>
    <rect x="666" y="72" width="328" height="28" rx="6" fill="#091620" fill-opacity="0.88" stroke="#367C9B" stroke-width="1"/>
    <text x="678" y="90" font-family="Segoe UI, sans-serif" font-size="11.8" font-weight="600" fill="{PLAN}">
      2. PLAN GÖRÜŞÜ AKTİF · CAMGÖBEĞİ (#7FE6FF)
    </text>
    <text x="954" y="680" text-anchor="middle" font-family="Segoe UI, sans-serif" font-size="11.5" fill="{PLAN}">
      Gizli kat planı (01–04), kaçış koridorları, hücreler ve yükselen şema
    </text>
  </g>
</svg>
"""


def build_r13_card() -> str:
    """1280×720 R13 %200 Yakın Kontrol Kartı (4 büyük panel)."""
    d1, b1 = sirt_dovme_svg(plan_glow=0.0)
    d2, b2 = sirt_dovme_svg(plan_glow=0.0)
    d3, b3 = sirt_dovme_svg(plan_glow=1.0)
    d4, b4 = sirt_dovme_svg(plan_glow=0.0)

    # 4 panel konumu (2×2) — başın tepesi, gül pencere + 01–03 ve ikiz turna tam çerçevede
    panels = [
        # (x, y, w, h, title, title_col, border_col, bg_id, tx, ty, sc, body)
        (24,  58, 604, 310, "1. ENSE + BUZZCUT + TRAPEZ ANATOMİSİ (%200)", "#DCE8F2", "#293A4C", "r13_bg_n",
         326, 540, 1.32, b1),
        (652, 58, 604, 310, "2. MERKEZ GOTİK KEMER &amp; GİZLİ KAT PLANI — NORMAL (%200)", "#DCE8F2", "#293A4C", "r13_bg_n",
         954, 224, 1.38, b2),
        (24, 386, 604, 310, "3. MERKEZ KAT PLANI — PLAN GÖRÜŞÜ #7FE6FF (%200)", PLAN, "#2E637C", "r13_bg_p",
         326, 552, 1.38, b3),
        (652, 386, 604, 310, "4. KÜREK KEMİĞİ İKİZ TURNA + OMUZ FİLİGRANI (%200)", "#DCE8F2", "#293A4C", "r13_bg_n",
         762, 566, 1.66, b4),
    ]

    clip_defs = []
    panel_elems = []
    for idx, (px, py, pw, ph, title, tcol, bcol, bgid, tx, ty, sc, body) in enumerate(panels, start=1):
        cid = f"r13_clip_{idx}"
        clip_defs.append(f'<clipPath id="{cid}"><rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="10"/></clipPath>')
        clean_len = len(title.replace("&amp;", "&"))
        panel_elems.append(f"""
        <rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="10" fill="url(#{bgid})" stroke="{bcol}" stroke-width="1.3"/>
        <g clip-path="url(#{cid})">
          <g transform="translate({tx},{ty}) scale({sc})">
            {body}
          </g>
          <rect x="{px + 12}" y="{py + 12}" width="{clean_len * 6.8 + 24:.0f}" height="25" rx="5"
                fill="#0B131C" fill-opacity="0.88" stroke="{bcol}" stroke-width="1"/>
          <text x="{px + 22}" y="{py + 29}" font-family="Segoe UI, sans-serif" font-size="11.2" font-weight="600" fill="{tcol}">
            {title}
          </text>
        </g>
        """)

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720" viewBox="0 0 1280 720">
  <defs>
    <linearGradient id="r13_card_bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0D151F"/>
      <stop offset="100%" stop-color="#141F2C"/>
    </linearGradient>
    <radialGradient id="r13_bg_n" cx="50%" cy="50%" r="60%">
      <stop offset="0%" stop-color="#202E3E"/>
      <stop offset="100%" stop-color="#111A24"/>
    </radialGradient>
    <radialGradient id="r13_bg_p" cx="50%" cy="50%" r="60%">
      <stop offset="0%" stop-color="#153246"/>
      <stop offset="100%" stop-color="#0C1721"/>
    </radialGradient>
    {"".join(clip_defs)}
    {d1}
    {d2}
    {d3}
    {d4}
  </defs>

  <rect width="1280" height="720" fill="url(#r13_card_bg)"/>
  <text x="26" y="35" font-family="Segoe UI, sans-serif" font-size="17.5" font-weight="700" fill="#EDF4FA" letter-spacing="0.4">
    R13 · %200 YAKIN KONTROL KARTI — ANATOMİK SIRT &amp; ÖZGÜN TAM SIRT DÖVMESİ
  </text>
  <text x="1256" y="34" text-anchor="end" font-family="Segoe UI, sans-serif" font-size="11.2" fill="#7B97B0">
    R1 / R13 · ANATOMİ + BUZZCUT + KEMER + TURNA + PLAN DOĞRULAMA
  </text>

  {"".join(panel_elems)}
</svg>
"""


def render_all() -> tuple[Path, Path]:
    p_model = OUT_DIR / "sirt_dovme_v1.png"
    p_r13 = OUT_DIR / "sirt_dovme_r13.png"
    _render_svg_to_png(build_model_card(), p_model, 1280, 720)
    _render_svg_to_png(build_r13_card(), p_r13, 1280, 720)
    return p_model, p_r13


if __name__ == "__main__":
    m, r = render_all()
    print(f"Üretildi: {m}")
    print(f"Üretildi: {r}")
