"""A-L (Lincoln Burrows Üretici) — v1 Sinematik 2D (Stil B + A hibrit).
İzole modül: ileride karakter.py'ye entegre edilebilir temiz, yan etkisiz fonksiyonlar:
  - kafa_lincoln(view="3q", ifade="odak", look=0.25, boyun=False)
  - figur_lincoln(ifade="odak", numara_goster=True)

Kilitli stil uyumu (Yetişkin Michael v3 ile birebir aynı sinematik 2D dil):
  - Ana dış kontur: 2.1px (#1A1513), iç anatomi çizgileri: 1.1–1.4px
  - Göz: ağır kapaklı, derin yerleşimli çelik/fıstık-gri (#6F7F88), koyu limbal halka (#2B373E),
    üst kapak döküm gölgesi ve tek keskin yansıma (R10 uyumlu)
  - Saç: kafatasına sıfır oturan koyu kahve/siyah buzzcut (#322A25), şakak/alın fade + clipPath stipple
  - R1: Gerçek oyuncu portresi kopyalanmaz; yalnızca karakter arketipi çizilir.
  - R3: Lincoln'ün kollarında kesinlikle dövme YOKTUR (dövmesiz güçlü kaslı kollar).
  - R4: Kalın, kaslı anatomik boyun (SCM + trapez) ve gömlek yakasına sağlam oturum.
"""
from __future__ import annotations

import io
import random
from pathlib import Path
import resvg_py
from PIL import Image

OUT_DIR = Path(__file__).resolve().parent

# ── Sinematik 2D Renk Paleti (Lincoln Burrows — A-Y v3 ile uyumlu, daha sıcak/bronz & sert) ──
INK = "#1A1513"          # Sıcak koyu mürekkep (ana dış kontur: 2.1px)
INK_SOFT = "#3D2A21"     # İç anatomi çizgileri (1.1–1.4px)

SKIN_BASE = "#C99C7C"    # Daha sıcak/bronz ana ten
SKIN_LIGHT = "#DFB89B"   # Işık düzlemi (alın, burun sırtı, elmacık üstü)
SKIN_MID = "#AE7E5E"     # Yarı gölge (elmacık altı, şakak, boyun tabanı)
SKIN_SHADOW = "#895C42"  # Ana gölge (kaş kemiği altı, uzak yanak, burun yanı)
SKIN_DEEP = "#613C2A"    # Derin gölge (çene altı, göz çukuru, boyun düşmesi)

STUBBLE = "#28211D"      # Belirgin 2-3 günlük sakal gölgesi
BUZZ_TOP = "#322A25"     # Koyu kahve/siyah kısa kazınmış saç tepe tonu
BUZZ_MID = "#463B34"     # Buzzcut şakak/orta geçiş tonu
BUZZ_LIGHT = "#5E5047"   # Tepe ışığı

IRIS_BASE = "#6F7F88"    # Derin yerleşimli fıstık-gri / çelik gözler
IRIS_DARK = "#2B373E"    # Koyu limbal halka
IRIS_LIGHT = "#A8B9C1"   # İris alt parlama hilali
BROW_COL = "#201A17"     # Kalın, hafif çatık/koruyucu koyu kaş

LIP_TOP = "#8E584A"      # Üst dudak (gölgede)
LIP_BOT = "#B87E6E"      # Alt dudak (doğal hacim)

SHIRT_BASE = "#5B7B9C"   # Fox River İdam Koğuşu mavi gömleği
SHIRT_LIGHT = "#7697B9"  # Gömlek omuz/göğüs ışığı
SHIRT_MID = "#486583"    # Gömlek yarı gölge
SHIRT_DARK = "#31475E"   # Gömlek derin gölge
UNDER_BASE = "#EEEAE1"   # İç beyaz atlet
UNDER_SH = "#CCC6B8"     # Atlet gölgesi
PANTS_BASE = "#283240"   # Koyu pantolon
PANTS_DARK = "#1B222D"
PANTS_LIGHT = "#374558"
SHOE_BASE = "#211C1A"    # Ağır bot
SHOE_SOLE = "#141110"

COLD_RIM = "#8DC5DF"     # İdam koridoru soğuk floresan rim ışığı
WARM_RIM = "#F5BA7A"     # Ziyaret odası sıcak ışık vurgusu

_UID_COUNTER = 0


def _uid(prefix: str = "ln") -> str:
    global _UID_COUNTER
    _UID_COUNTER += 1
    return f"{prefix}{_UID_COUNTER}"


# İfade tablosu: (kaş_iç_y, kaş_dış_y, üst_kapak, alt_kapak, ağız_türü, ekstra)
IFADE = {
    "odak":     (4.4, -1.0, 0.38, 0.18, "firm", "frown_soft"),
    "koruyucu": (-2.6, 1.4, 0.30, 0.18, "warm_smile", ""),
    "sefkat":   (-2.6, 1.4, 0.30, 0.18, "warm_smile", ""),
    "ofke":     (9.8, -5.2, 0.42, 0.28, "grit", "frown_hard"),
    "yas":      (-7.6, 4.6, 0.46, 0.16, "sad", "tear"),
    "gerilim":  (5.6, -2.4, 0.26, 0.22, "tense", "cold_corridor"),
    "neutral":  (1.5, 0.0, 0.30, 0.12, "calm", ""),
}


def _render_eye(
    cx: float,
    cy: float,
    rx: float,
    ry: float,
    lu: float,
    ll: float,
    look: float,
    cold_light: bool = False,
    side: bool = False,
) -> str:
    """Sinematik 2D göz (Lincoln): ağır kapaklı, derin yerleşimli fıstık-gri/çelik (#6F7F88),
    koyu limbal halka (#2B373E), üst kapak döküm gölgesi ve tek keskin yansıma.
    """
    cid = _uid("eye")
    if side:
        shape = (
            f"M{cx - rx * 0.85:.1f},{cy + ry * 0.14:.1f} "
            f"Q{cx - rx * 0.04:.1f},{cy - ry * 1.06:.1f} {cx + rx * 0.94:.1f},{cy - ry * 0.08:.1f} "
            f"Q{cx + rx * 0.12:.1f},{cy + ry * 0.88:.1f} {cx - rx * 0.85:.1f},{cy + ry * 0.14:.1f} Z"
        )
    else:
        shape = (
            f"M{cx - rx:.1f},{cy + ry * 0.16:.1f} "
            f"Q{cx - rx * 0.28:.1f},{cy - ry * 1.06:.1f} {cx + rx * 0.34:.1f},{cy - ry * 0.88:.1f} "
            f"Q{cx + rx * 0.82:.1f},{cy - ry * 0.40:.1f} {cx + rx:.1f},{cy + ry * 0.08:.1f} "
            f"Q{cx + rx * 0.26:.1f},{cy + ry * 0.88:.1f} {cx - rx * 0.34:.1f},{cy + ry * 0.84:.1f} "
            f"Q{cx - rx * 0.78:.1f},{cy + ry * 0.54:.1f} {cx - rx:.1f},{cy + ry * 0.16:.1f} Z"
        )

    ix = cx + look * rx * 0.32
    iy = cy + ry * 0.06
    ir = ry * 0.78 if not side else ry * 0.72
    pr = ir * 0.44

    # Ağır üst kapak (hooded)
    uy = cy - ry * 1.00 + lu * (ry * 1.68)
    ly = cy + ry * 0.90 - ll * (ry * 1.18)

    iris_col = "#7D95A2" if cold_light else IRIS_BASE
    hilal_col = "#CBE6F2" if cold_light else IRIS_LIGHT

    out = [
        f'<defs><clipPath id="{cid}"><path d="{shape}"/></clipPath></defs>',
        f'<path d="{shape}" fill="#E6E4DD"/>',
        f'<g clip-path="url(#{cid})">',
        # İris: koyu limbal halka + fıstık-gri/çelik + alt parlama hilali
        f'<circle cx="{ix:.1f}" cy="{iy:.1f}" r="{ir:.1f}" fill="{IRIS_DARK}"/>',
        f'<circle cx="{ix:.1f}" cy="{iy:.1f}" r="{ir * 0.79:.1f}" fill="{iris_col}"/>',
        f'<ellipse cx="{ix:.1f}" cy="{iy + ir * 0.35:.1f}" rx="{ir * 0.54:.1f}" ry="{ir * 0.26:.1f}" fill="{hilal_col}" opacity="0.78"/>',
        # Göz bebeği
        f'<circle cx="{ix:.1f}" cy="{iy:.1f}" r="{pr:.1f}" fill="#101417"/>',
        # Üst kapak döküm gölgesi (derin, kararlı bakış)
        f'<rect x="{cx - rx - 4:.1f}" y="{cy - ry - 4:.1f}" width="{rx * 2 + 8:.1f}" height="{(uy - (cy - ry - 4)) + ry * 0.58:.1f}" fill="#354048" opacity="0.38"/>',
        # Tek keskin küçük yansıma
        f'<circle cx="{ix - ir * 0.30:.1f}" cy="{iy - ir * 0.20:.1f}" r="{max(1.15, ir * 0.21):.1f}" fill="#FFFFFF" opacity="0.95"/>',
        # Üst ve alt göz kapağı ten parçaları
        f'<rect x="{cx - rx - 6:.1f}" y="{cy - ry * 2.2:.1f}" width="{rx * 2 + 12:.1f}" height="{uy - (cy - ry * 2.2):.1f}" fill="{SKIN_SHADOW}" opacity="0.90"/>',
        f'<rect x="{cx - rx - 6:.1f}" y="{ly:.1f}" width="{rx * 2 + 12:.1f}" height="{ry * 2.2:.1f}" fill="{SKIN_BASE}"/>',
        # Keskin üst kirpik hattı
        f'<path d="M{cx - rx - 2:.1f},{uy + 1.0:.1f} Q{cx:.1f},{uy - 2.2:.1f} {cx + rx + 2:.1f},{uy + 0.6:.1f}" fill="none" stroke="{INK}" stroke-width="2.5" stroke-linecap="round"/>',
        '</g>',
        # Göz dış çerçevesi
        f'<path d="M{cx - rx:.1f},{cy + ry * 0.16:.1f} Q{cx - rx * 0.24:.1f},{min(uy - 1.0, cy - ry * 0.82):.1f} {cx + rx:.1f},{cy + ry * 0.08:.1f}" fill="none" stroke="{INK}" stroke-width="2.1" stroke-linecap="round"/>',
        f'<path d="M{cx - rx * 0.80:.1f},{cy + ry * 0.34:.1f} Q{cx:.1f},{min(ly + 0.8, cy + ry * 0.88):.1f} {cx + rx * 0.80:.1f},{cy + ry * 0.28:.1f}" fill="none" stroke="{INK_SOFT}" stroke-width="1.1" opacity="0.72" stroke-linecap="round"/>',
        # Ağır kapak kıvrımı (hooded crease)
        f'<path d="M{cx - rx * 0.96:.1f},{cy - ry * 0.72:.1f} Q{cx:.1f},{cy - ry * 1.28:.1f} {cx + rx * 0.96:.1f},{cy - ry * 0.64:.1f}" fill="none" stroke="{SKIN_DEEP}" stroke-width="1.45" opacity="0.82" stroke-linecap="round"/>',
        # Alt orbital hat (derin yerleşimli göz altı)
        f'<path d="M{cx - rx * 0.72:.1f},{cy + ry * 1.26:.1f} Q{cx:.1f},{cy + ry * 1.62:.1f} {cx + rx * 0.70:.1f},{cy + ry * 1.18:.1f}" fill="none" stroke="{SKIN_DEEP}" stroke-width="1.15" opacity="0.56" stroke-linecap="round"/>',
    ]
    return "".join(out)


def _render_brow(
    x_in: float,
    y_in: float,
    x_out: float,
    y_out: float,
    arch_y: float = -1.0,
    thick: float = 7.4,
) -> str:
    """Kalın, alçak, hafif çatık/koruyucu erkek kaşı (Lincoln)."""
    mx = x_in * 0.36 + x_out * 0.64
    my = (y_in + y_out) * 0.5 + arch_y
    t_in = thick * 0.60
    t_mid = thick * 0.56
    t_out = thick * 0.26
    d = (
        f"M{x_in:.1f},{y_in - t_in:.1f} "
        f"Q{mx:.1f},{my - t_mid:.1f} {x_out:.1f},{y_out - t_out:.1f} "
        f"L{x_out:.1f},{y_out + t_out:.1f} "
        f"Q{mx:.1f},{my + t_mid * 0.76:.1f} {x_in:.1f},{y_in + t_in * 0.88:.1f} Z"
    )
    return (
        f'<path d="{d}" fill="{BROW_COL}"/>'
        f'<path d="M{x_in:.1f},{y_in - t_in * 0.52:.1f} Q{mx:.1f},{my - t_mid * 0.52:.1f} {x_out:.1f},{y_out:.1f}" '
        f'fill="none" stroke="#453A33" stroke-width="1.0" opacity="0.38"/>'
    )


def _render_mouth(mx: float, my: float, mw: float, kind: str, view: str) -> str:
    """Sinematik 2D ağız (Lincoln): sağlam, kararlı dudak yapısı ve ifadeler."""
    if view == "side":
        if kind == "grit":
            return (
                f'<path d="M{mx + 2.5:.1f},{my - 3.5:.1f} Q{mx - 11:.1f},{my + 0.5:.1f} {mx + 2.5:.1f},{my + 6.5:.1f} Z" '
                f'fill="#3E1E1A" stroke="{INK}" stroke-width="1.6"/>'
                f'<path d="M{mx + 1.5:.1f},{my + 1.0:.1f} L{mx - 8.5:.1f},{my + 1.0:.1f}" fill="none" stroke="#EAE4DA" stroke-width="2.6" stroke-linecap="round"/>'
                f'<path d="M{mx - 2:.1f},{my + 9.5:.1f} Q{mx - 8:.1f},{my + 11:.1f} {mx - 12:.1f},{my + 8:.1f}" fill="none" stroke="{SKIN_DEEP}" stroke-width="1.6" opacity="0.68" stroke-linecap="round"/>'
            )
        dy = -2.6 if kind == "warm_smile" else (2.8 if kind == "sad" else (1.2 if kind in ("firm", "tense") else 0.0))
        return (
            f'<path d="M{mx + 2.5:.1f},{my - 5.2:.1f} Q{mx - 5.5:.1f},{my - 4.0:.1f} {mx - 13.5:.1f},{my - 0.4:.1f} L{mx + 2.5:.1f},{my:.1f} Z" fill="{LIP_TOP}" opacity="0.78"/>'
            f'<path d="M{mx + 2.0:.1f},{my + 0.6:.1f} Q{mx - 6.0:.1f},{my + 6.8:.1f} {mx - 12.5:.1f},{my + 1.2:.1f} Z" fill="{LIP_BOT}" opacity="0.72"/>'
            f'<path d="M{mx + 2.5:.1f},{my:.1f} Q{mx - 6:.1f},{my + 1.0 + dy * 0.4:.1f} {mx - 14.0:.1f},{my + dy:.1f}" '
            f'fill="none" stroke="{INK}" stroke-width="1.9" stroke-linecap="round"/>'
            f'<path d="M{mx - 2:.1f},{my + 8.8:.1f} Q{mx - 8:.1f},{my + 10.6:.1f} {mx - 12.5:.1f},{my + 7.6:.1f}" fill="none" stroke="{SKIN_DEEP}" stroke-width="1.6" opacity="0.65" stroke-linecap="round"/>'
        )

    asym = 0.0 if view == "front" else 0.10
    lx = mx - mw * (1.0 - asym)
    rx = mx + mw * (1.0 + asym)

    if kind == "grit":
        # Öfke: sıkılı çene, belirgin dudak gerilimi ve gergin diş hattı
        return (
            f'<path d="M{lx - 0.5:.1f},{my + 2.4:.1f} Q{mx:.1f},{my - 6.2:.1f} {rx + 0.5:.1f},{my + 2.2:.1f} '
            f'Q{mx:.1f},{my + 10.0:.1f} {lx - 0.5:.1f},{my + 2.4:.1f} Z" fill="{LIP_TOP}" opacity="0.65"/>'
            f'<path d="M{lx + 1.2:.1f},{my + 2.2:.1f} Q{mx:.1f},{my - 3.8:.1f} {rx - 1.2:.1f},{my + 2.0:.1f} '
            f'Q{mx:.1f},{my + 7.4:.1f} {lx + 1.2:.1f},{my + 2.2:.1f} Z" fill="#321714" stroke="{INK}" stroke-width="1.8"/>'
            f'<path d="M{lx + 3.6:.1f},{my + 1.4:.1f} Q{mx:.1f},{my - 1.2:.1f} {rx - 3.6:.1f},{my + 1.2:.1f} '
            f'L{rx - 4.4:.1f},{my + 4.5:.1f} Q{mx:.1f},{my + 3.4:.1f} {lx + 4.4:.1f},{my + 4.5:.1f} Z" fill="#EAE4DA" stroke="{INK}" stroke-width="0.9"/>'
            f'<path d="M{lx + 5.2:.1f},{my + 2.8:.1f} Q{mx:.1f},{my + 1.5:.1f} {rx - 5.2:.1f},{my + 2.6:.1f}" fill="none" stroke="{INK_SOFT}" stroke-width="0.9" opacity="0.72"/>'
            f'<path d="M{mx - mw * 0.58:.1f},{my + 11.4:.1f} Q{mx:.1f},{my + 14.0:.1f} {mx + mw * 0.58:.1f},{my + 11.2:.1f}" fill="none" stroke="{SKIN_DEEP}" stroke-width="1.9" opacity="0.74" stroke-linecap="round"/>'
        )

    if kind == "tense":
        # Gerilim: sıkı, gergin düz hat + köşelerde hafif çekilme
        c_l, c_r, mid_dip = 1.6, 1.4, -0.4
    elif kind == "warm_smile":
        # Koruyucu/şefkat: kardeşi için sıcak, güven veren yarım gülümseme
        c_l, c_r, mid_dip = -3.4, -4.0, 2.2
    elif kind == "sad":
        c_l, c_r, mid_dip = 3.8, 3.6, -1.8
    elif kind == "firm":
        c_l, c_r, mid_dip = 1.2, 1.0, 0.2
    else:
        c_l, c_r, mid_dip = 0.0, -0.1, 1.1

    upper_lip = (
        f"M{lx:.1f},{my + c_l:.1f} "
        f"Q{mx - mw * 0.34:.1f},{my - 6.0:.1f} {mx - mw * 0.14:.1f},{my - 5.0:.1f} "
        f"Q{mx:.1f},{my - 3.6:.1f} {mx + mw * 0.14:.1f},{my - 5.0:.1f} "
        f"Q{mx + mw * 0.34:.1f},{my - 6.0:.1f} {rx:.1f},{my + c_r:.1f} "
        f"Q{mx:.1f},{my + mid_dip:.1f} {lx:.1f},{my + c_l:.1f} Z"
    )
    lower_lip = (
        f"M{lx + mw * 0.10:.1f},{my + c_l * 0.6 + 0.6:.1f} "
        f"Q{mx:.1f},{my + 9.0 + mid_dip * 0.42:.1f} {rx - mw * 0.10:.1f},{my + c_r * 0.6 + 0.6:.1f} "
        f"Q{mx:.1f},{my + mid_dip + 0.5:.1f} {lx + mw * 0.10:.1f},{my + c_l * 0.6 + 0.6:.1f} Z"
    )
    seam = (
        f"M{lx:.1f},{my + c_l:.1f} "
        f"Q{mx - mw * 0.35:.1f},{my + mid_dip * 0.42:.1f} {mx:.1f},{my + mid_dip + 0.5:.1f} "
        f"Q{mx + mw * 0.35:.1f},{my + mid_dip * 0.42:.1f} {rx:.1f},{my + c_r:.1f}"
    )
    return (
        f'<path d="{upper_lip}" fill="{LIP_TOP}" opacity="0.82"/>'
        f'<path d="{lower_lip}" fill="{LIP_BOT}" opacity="0.72"/>'
        f'<path d="M{mx - mw * 0.24:.1f},{my - 5.2:.1f} Q{mx:.1f},{my - 3.9:.1f} {mx + mw * 0.24:.1f},{my - 5.2:.1f}" fill="none" stroke="{SKIN_LIGHT}" stroke-width="1.2" opacity="0.56" stroke-linecap="round"/>'
        f'<path d="M{mx - mw * 0.34:.1f},{my + 4.8:.1f} Q{mx:.1f},{my + 6.0:.1f} {mx + mw * 0.30:.1f},{my + 4.6:.1f}" fill="none" stroke="#EBC8B6" stroke-width="1.7" opacity="0.52" stroke-linecap="round"/>'
        f'<path d="{seam}" fill="none" stroke="{INK}" stroke-width="1.9" stroke-linecap="round"/>'
        f'<ellipse cx="{lx - 0.8:.1f}" cy="{my + c_l + 0.5:.1f}" rx="2.4" ry="1.4" fill="{SKIN_DEEP}" opacity="0.52"/>'
        f'<ellipse cx="{rx + 0.8:.1f}" cy="{my + c_r + 0.5:.1f}" rx="2.4" ry="1.4" fill="{SKIN_DEEP}" opacity="0.52"/>'
        f'<path d="M{mx - mw * 0.52:.1f},{my + 10.6:.1f} Q{mx:.1f},{my + 13.0:.1f} {mx + mw * 0.52:.1f},{my + 10.4:.1f}" '
        f'fill="none" stroke="{SKIN_DEEP}" stroke-width="1.9" opacity="0.70" stroke-linecap="round"/>'
    )


def _buzzcut_stipple(view: str) -> str:
    """Koyu kahve/siyah kısa kazınmış saç için ince stipple dokusu (clipPath içinde kullanılır)."""
    rng = random.Random(142 if view == "front" else (177 if view == "3q" else 199))
    pts: list[str] = []
    for _ in range(155):
        if view == "front":
            x = rng.uniform(-67, 67)
            y = rng.uniform(-95, -52)
            if (x / 69) ** 2 + ((y + 20) / 77) ** 2 > 0.95:
                continue
        elif view == "3q":
            x = rng.uniform(-65, 68)
            y = rng.uniform(-95, -48)
            if ((x - 3) / 70) ** 2 + ((y + 20) / 77) ** 2 > 0.95:
                continue
        else:
            x = rng.uniform(-68, 60)
            y = rng.uniform(-95, -38)
            if ((x + 3) / 69) ** 2 + ((y + 18) / 78) ** 2 > 0.95:
                continue
        op = rng.uniform(0.20, 0.42)
        r = rng.uniform(0.58, 0.90)
        pts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.2f}" fill="#171210" opacity="{op:.2f}"/>')
    return "".join(pts)


def _stubble_stipple(view: str) -> str:
    """Belirgin 2-3 günlük sakal gölgesi dokusu (Michael'dan daha yoğun ve sert)."""
    rng = random.Random(401 if view == "front" else (402 if view == "3q" else 403))
    pts: list[str] = []
    for _ in range(175):
        if view == "front":
            x = rng.uniform(-62, 62)
            y = rng.uniform(38, 104)
        elif view == "3q":
            x = rng.uniform(-54, 66)
            y = rng.uniform(40, 104)
        else:
            x = rng.uniform(4, 68)
            y = rng.uniform(40, 104)
        # Dudak alanını temiz bırak
        if view == "front" and abs(x) < 24 and 49 < y < 68:
            continue
        if view == "3q" and 4 < x < 50 and 49 < y < 68:
            continue
        if view == "side" and x > 50 and 49 < y < 68:
            continue
        op = rng.uniform(0.20, 0.38)
        r = rng.uniform(0.62, 0.84)
        pts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.2f}" fill="{STUBBLE}" opacity="{op:.2f}"/>')
    return "".join(pts)


def kafa_lincoln(
    view: str = "3q",
    ifade: str = "odak",
    look: float = 0.25,
    boyun: bool = False,
) -> str:
    """Lincoln Burrows kafası (v1 — Stil B + A hibrit, A-Y v3 ile birebir uyumlu sinematik 2D).
    Merkez (0, 0), yükseklik ~204 (y: -96 .. +107), daha geniş kare çene ve kalın boyun.
    view: 'front' | '3q' | 'side'.
    """
    bi, bo, lu, ll, mk, extra = IFADE.get(ifade, IFADE["odak"])
    is_cold = extra == "cold_corridor"

    o: list[str] = []
    defs: list[str] = []

    cid_face = _uid("fclip")
    cid_buzz = _uid("bclip")
    gid_skin = _uid("sking")
    gid_buzz = _uid("buzzg")
    gid_sidefade = _uid("sfade")
    gid_cheek = _uid("chekg")
    gid_stub = _uid("stubg")
    gid_cold = _uid("coldg")

    defs.append(
        f'<linearGradient id="{gid_skin}" x1="0.14" y1="0.08" x2="0.88" y2="0.92">'
        f'<stop offset="0%" stop-color="{SKIN_LIGHT}"/>'
        f'<stop offset="46%" stop-color="{SKIN_BASE}"/>'
        f'<stop offset="100%" stop-color="{SKIN_MID}"/>'
        f'</linearGradient>'
    )
    defs.append(
        f'<linearGradient id="{gid_cheek}" x1="0.0" y1="0.5" x2="1.0" y2="0.35">'
        f'<stop offset="0%" stop-color="{SKIN_SHADOW}" stop-opacity="0.52"/>'
        f'<stop offset="65%" stop-color="{SKIN_SHADOW}" stop-opacity="0.24"/>'
        f'<stop offset="100%" stop-color="{SKIN_SHADOW}" stop-opacity="0.0"/>'
        f'</linearGradient>'
    )
    defs.append(
        f'<linearGradient id="{gid_buzz}" x1="0.35" y1="0.0" x2="0.55" y2="1.0">'
        f'<stop offset="0%" stop-color="{BUZZ_TOP}" stop-opacity="0.94"/>'
        f'<stop offset="56%" stop-color="{BUZZ_MID}" stop-opacity="0.86"/>'
        f'<stop offset="86%" stop-color="{BUZZ_MID}" stop-opacity="0.48"/>'
        f'<stop offset="100%" stop-color="{SKIN_BASE}" stop-opacity="0.0"/>'
        f'</linearGradient>'
    )
    defs.append(
        f'<linearGradient id="{gid_sidefade}" x1="0.5" y1="0.0" x2="0.5" y2="1.0">'
        f'<stop offset="0%" stop-color="{BUZZ_MID}" stop-opacity="0.66"/>'
        f'<stop offset="68%" stop-color="{BUZZ_MID}" stop-opacity="0.24"/>'
        f'<stop offset="100%" stop-color="{SKIN_BASE}" stop-opacity="0.0"/>'
        f'</linearGradient>'
    )
    # 2-3 günlük daha belirgin sakal gölgesi
    defs.append(
        f'<linearGradient id="{gid_stub}" x1="0.5" y1="0.0" x2="0.5" y2="1.0">'
        f'<stop offset="0%" stop-color="{STUBBLE}" stop-opacity="0.0"/>'
        f'<stop offset="30%" stop-color="{STUBBLE}" stop-opacity="0.24"/>'
        f'<stop offset="100%" stop-color="{STUBBLE}" stop-opacity="0.40"/>'
        f'</linearGradient>'
    )
    if is_cold:
        defs.append(
            f'<linearGradient id="{gid_cold}" x1="1.0" y1="0.30" x2="0.38" y2="0.62">'
            f'<stop offset="0%" stop-color="{COLD_RIM}" stop-opacity="0.34"/>'
            f'<stop offset="48%" stop-color="{COLD_RIM}" stop-opacity="0.10"/>'
            f'<stop offset="100%" stop-color="{COLD_RIM}" stop-opacity="0.0"/>'
            f'</linearGradient>'
        )

    # Opsiyonel kalın, kaslı anatomik boyun (R4 — Michael'dan belirgin biçimde daha kalın)
    if boyun:
        if view == "front":
            nk_d = "M-44,72 L-54,132 Q0,144 54,132 L44,72 Z"
            sh_d = "M-44,72 Q0,120 44,72 L48,108 Q0,126 -48,108 Z"
            scm = (
                f'<path d="M-40,86 Q-24,114 -10,134 M40,86 Q24,114 10,134" fill="none" stroke="{SKIN_SHADOW}" stroke-width="2.2" opacity="0.62" stroke-linecap="round"/>'
                f'<path d="M-12,128 Q0,135 12,128" fill="none" stroke="{SKIN_DEEP}" stroke-width="1.6" opacity="0.60" stroke-linecap="round"/>'
            )
        elif view == "3q":
            nk_d = "M-50,60 L-58,132 Q-6,144 34,130 L32,82 Z"
            sh_d = "M-50,60 Q0,120 32,80 L33,112 Q-6,128 -53,104 Z"
            scm = (
                f'<path d="M-44,82 Q-24,112 -6,134 M18,92 Q14,114 16,130" fill="none" stroke="{SKIN_SHADOW}" stroke-width="2.2" opacity="0.62" stroke-linecap="round"/>'
                f'<path d="M-12,116 Q0,122 10,116" fill="none" stroke="{SKIN_DEEP}" stroke-width="1.5" opacity="0.52" stroke-linecap="round"/>'
            )
        else:
            nk_d = "M-54,60 L-64,134 Q-12,144 24,132 L18,86 Z"
            sh_d = "M-54,60 Q-12,114 20,84 L20,110 Q-12,126 -58,104 Z"
            scm = f'<path d="M-42,80 Q-22,110 -6,132" fill="none" stroke="{SKIN_SHADOW}" stroke-width="2.3" opacity="0.62" stroke-linecap="round"/>'
        o.append(
            f'<path d="{nk_d}" fill="{SKIN_MID}"/>'
            f'<path d="{sh_d}" fill="{SKIN_DEEP}" opacity="0.66"/>'
            f'{scm}'
            f'<path d="{nk_d}" fill="none" stroke="{INK}" stroke-width="2.1" stroke-linejoin="round"/>'
        )

    # ── 1. Kafatası + Güçlü Kare Çeneli Geniş Yüz Silueti (Michael'dan daha geniş & kemikli) ──
    if view == "front":
        face_d = (
            "M-69,-22 C-70,-69 -42,-95 0,-96 C42,-95 70,-69 69,-22 "
            "L68,16 C67,38 64,58 58,74 L44,94 C32,104 18,106 0,106 "
            "C-18,106 -32,104 -44,94 L-58,74 C-64,58 -67,38 -68,16 Z"
        )
        ears = [(-70, 6, -1), (70, 6, 1)]
        eye_specs = [(-28.5, -5.0, 15.0, 7.6, False), (28.5, -5.0, 15.0, 7.6, False)]
        lk = 0.0 if look == 0.25 else look
        mx, my, mw = 0.0, 57.5, 24.0
    elif view == "3q":
        face_d = (
            "M-68,-20 C-70,-70 -38,-95 8,-96 C48,-95 71,-71 71,-26 "
            "C73,-12 72,2 73,16 C74,30 70,50 64,66 "
            "L55,90 C46,101 34,106 20,106 C2,107 -18,102 -36,90 "
            "L-55,70 C-62,54 -66,32 -67,10 Z"
        )
        ears = [(-67, 8, -1)]
        eye_specs = [(-5.5, -5.0, 15.0, 7.6, False), (44.0, -5.0, 12.0, 7.2, False)]
        lk = look
        mx, my, mw = 26.0, 57.5, 21.0
    else:  # side (profil, sağa bakar)
        face_d = (
            "M-71,-18 C-74,-71 -38,-96 6,-96 C44,-96 65,-75 66,-38 "
            "L67,-16 C68,-10 70,-6 73,0 L86,28 C88,34 83,39 74,39 "
            "L69,39 L72,49 C74,53 71,56 67,57 L71,64 C73,69 69,75 64,77 "
            "L68,91 C69,102 58,107 40,107 L12,106 C-10,105 -28,96 -41,78 "
            "C-58,56 -67,25 -71,-18 Z"
        )
        ears = [(-12, 10, -1)]
        eye_specs = [(48.5, -5.5, 11.4, 7.0, True)]
        lk = max(0.35, look)
        mx, my, mw = 65.5, 58.0, 12.8

    defs.append(f'<clipPath id="{cid_face}"><path d="{face_d}"/></clipPath>')
    o.insert(0, f'<defs>{"".join(defs)}</defs>')

    # ── 2. Kulaklar ──
    for ex, ey, side_sgn in ears:
        ew = 11.8 if view != "side" else 13.8
        eh = 21.2
        ear_d = (
            f"M{ex},{ey - eh * 0.85:.1f} "
            f"C{ex + side_sgn * ew * 1.15:.1f},{ey - eh * 0.9:.1f} {ex + side_sgn * ew * 1.25:.1f},{ey + eh * 0.1:.1f} {ex + side_sgn * ew * 0.75:.1f},{ey + eh * 0.72:.1f} "
            f"C{ex + side_sgn * ew * 0.45:.1f},{ey + eh * 1.0:.1f} {ex},{ey + eh * 0.92:.1f} {ex},{ey + eh * 0.65:.1f} Z"
        )
        o.append(
            f'<path d="{ear_d}" fill="{SKIN_MID}" stroke="{INK}" stroke-width="2.0" stroke-linejoin="round"/>'
            f'<path d="M{ex + side_sgn * ew * 0.25:.1f},{ey - eh * 0.48:.1f} '
            f'Q{ex + side_sgn * ew * 0.85:.1f},{ey - eh * 0.15:.1f} {ex + side_sgn * ew * 0.32:.1f},{ey + eh * 0.45:.1f}" '
            f'fill="none" stroke="{SKIN_DEEP}" stroke-width="1.5" stroke-linecap="round"/>'
            f'<path d="M{ex + side_sgn * ew * 0.18:.1f},{ey - 2:.1f} Q{ex + side_sgn * ew * 0.52:.1f},{ey + 4:.1f} {ex + side_sgn * ew * 0.2:.1f},{ey + 9:.1f}" '
            f'fill="none" stroke="{SKIN_DEEP}" stroke-width="1.3" opacity="0.72" stroke-linecap="round"/>'
        )

    # ── 3. Yüz Tabanı + Sert Kemik Düzlemleri + Sakal Gölgesi + Buzzcut ──
    o.append(f'<path d="{face_d}" fill="url(#{gid_skin})"/>')
    inner: list[str] = []

    if view == "front":
        inner.append(
            # Sağ yarı ana sinematik gölge
            f'<path d="M28,-98 C49,-56 48,-14 42,26 C38,56 26,84 8,112 L96,112 L96,-98 Z" fill="{SKIN_SHADOW}" opacity="0.36"/>'
            # Güçlü kaş kemiği altı (brow ridge) & derin göz çukuru gölgesi
            f'<path d="M-54,-22 Q-28,-30 -4,-17 Q-8,5 -28,7 Q-50,5 -54,-22 Z" fill="{SKIN_SHADOW}" opacity="0.60"/>'
            f'<path d="M54,-22 Q28,-30 4,-17 Q8,5 28,7 Q50,5 54,-22 Z" fill="{SKIN_SHADOW}" opacity="0.64"/>'
            f'<path d="M-49,-20 Q-28,-27 -8,-17 L-10,-8 Q-28,-17 -47,-10 Z" fill="{SKIN_DEEP}" opacity="0.42"/>'
            f'<path d="M49,-20 Q28,-27 8,-17 L10,-8 Q28,-17 47,-10 Z" fill="{SKIN_DEEP}" opacity="0.45"/>'
            # Geniş elmacık altı ve kare çene düzlem gölgeleri
            f'<path d="M-68,16 L-44,32 L-40,70 L-66,54 Z" fill="{SKIN_SHADOW}" opacity="0.42"/>'
            f'<path d="M68,16 L44,32 L40,70 L66,54 Z" fill="{SKIN_SHADOW}" opacity="0.54"/>'
            # Alın + geniş burun sırtı ışığı
            f'<path d="M-38,-52 Q0,-58 32,-48 Q20,-30 -16,-32 Z" fill="{SKIN_LIGHT}" opacity="0.46"/>'
            f'<path d="M-4.8,-14 L4.0,-14 L6.0,27 L-6.0,27 Z" fill="{SKIN_LIGHT}" opacity="0.58"/>'
            f'<path d="M4.5,-14 L13,27 L3,36 L-10,34 L-5,27 Z" fill="{SKIN_SHADOW}" opacity="0.40"/>'
            # Kare çene altı derin gölge
            f'<path d="M-50,88 Q0,106 50,88 L50,114 L-50,114 Z" fill="{SKIN_DEEP}" opacity="0.44"/>'
            # 2-3 günlük belirgin sakal gölgesi
            f'<path d="M-66,34 C-48,46 -26,40 0,41 C26,40 48,46 66,34 L66,112 L-66,112 Z" fill="url(#{gid_stub})"/>'
            + _stubble_stipple("front")
            + f'<path d="M-67,-16 L-65,18 C-63,48 -54,74 -36,94" fill="none" stroke="#FFF2E4" stroke-width="2.8" opacity="0.30" stroke-linecap="round"/>'
        )
        buzz_top = (
            "M-72,-10 L-72,-102 L72,-102 L72,-10 "
            "L66,-12 C64,-30 58,-44 47,-51 C36,-57 24,-61 0,-61 "
            "C-24,-61 -36,-57 -47,-51 C-58,-44 -64,-30 -66,-12 Z"
        )
        buzz_fade = (
            "M-72,12 L-65,12 C-63,-14 -58,-32 -47,-42 C-36,-51 -22,-56 0,-56 "
            "C22,-56 36,-51 47,-42 C58,-32 63,-14 65,12 L72,12 L72,-102 L-72,-102 Z"
        )
        inner.append(
            f'<defs><clipPath id="{cid_buzz}"><path d="{buzz_top}"/></clipPath></defs>'
            f'<path d="{buzz_fade}" fill="url(#{gid_sidefade})"/>'
            f'<path d="{buzz_top}" fill="url(#{gid_buzz})"/>'
            f'<g clip-path="url(#{cid_buzz})">{_buzzcut_stipple("front")}</g>'
            f'<ellipse cx="-4" cy="-84" rx="30" ry="6.5" fill="{BUZZ_LIGHT}" opacity="0.30"/>'
        )

    elif view == "3q":
        inner.append(
            # Uzak taraf ana gölge
            f'<path d="M42,-98 C60,-58 62,-18 60,22 C58,54 48,84 28,112 L96,112 L96,-98 Z" fill="{SKIN_SHADOW}" opacity="0.46"/>'
            # Yakın elmacık altı ve masseter (çene kası) gölgesi
            f'<path d="M-66,15 C-44,22 -22,36 -18,58 C-26,78 -44,90 -60,74 Z" fill="url(#{gid_cheek})"/>'
            # Güçlü kaş kemiği altı & derin göz çukuru gölgesi
            f'<path d="M-28,-22 Q-5,-30 18,-17 Q14,6 -6,7 Q-26,5 -28,-22 Z" fill="{SKIN_SHADOW}" opacity="0.60"/>'
            f'<path d="M28,-21 Q46,-29 63,-16 Q59,5 43,6 Q30,4 28,-21 Z" fill="{SKIN_SHADOW}" opacity="0.64"/>'
            f'<path d="M-24,-19 Q-5,-26 14,-17 L11,-8 Q-5,-17 -22,-10 Z" fill="{SKIN_DEEP}" opacity="0.42"/>'
            f'<path d="M30,-19 Q46,-26 60,-16 L58,-8 Q46,-16 32,-10 Z" fill="{SKIN_DEEP}" opacity="0.45"/>'
            # Alın + yakın elmacık üstü ışık düzlemi
            f'<path d="M-36,-52 Q4,-60 38,-49 Q24,-31 -16,-33 Z" fill="{SKIN_LIGHT}" opacity="0.48"/>'
            f'<path d="M-46,8 Q-24,0 -6,11 Q-16,27 -40,24 Z" fill="{SKIN_LIGHT}" opacity="0.44"/>'
            # Kare çene altı gölgesi
            f'<path d="M-46,86 Q18,106 58,84 L58,114 L-46,114 Z" fill="{SKIN_DEEP}" opacity="0.44"/>'
            # 2-3 günlük belirgin sakal gölgesi
            f'<path d="M-62,38 C-34,48 4,42 28,42 C48,42 64,46 72,36 L72,112 L-62,112 Z" fill="url(#{gid_stub})"/>'
            + _stubble_stipple("3q")
            + f'<path d="M-66,-14 L-64,20 C-60,52 -48,78 -24,98" fill="none" stroke="#FFF2E4" stroke-width="2.8" opacity="0.30" stroke-linecap="round"/>'
        )
        buzz_top = (
            "M-72,12 L-72,-102 L76,-102 L76,-28 "
            "L70,-30 C67,-46 57,-56 40,-60 C18,-65 -10,-63 -32,-53 "
            "C-44,-46 -51,-32 -54,-10 L-58,12 Z"
        )
        buzz_fade = (
            "M-72,24 L-56,24 L-52,-6 C-49,-26 -42,-40 -30,-48 C-8,-58 18,-60 40,-55 "
            "C56,-51 66,-42 70,-26 L76,-26 L76,-102 L-72,-102 Z"
        )
        inner.append(
            f'<defs><clipPath id="{cid_buzz}"><path d="{buzz_top}"/></clipPath></defs>'
            f'<path d="{buzz_fade}" fill="url(#{gid_sidefade})"/>'
            f'<path d="{buzz_top}" fill="url(#{gid_buzz})"/>'
            f'<g clip-path="url(#{cid_buzz})">{_buzzcut_stipple("3q")}</g>'
            f'<ellipse cx="4" cy="-84" rx="32" ry="6.5" fill="{BUZZ_LIGHT}" opacity="0.30"/>'
        )

    else:  # side
        inner.append(
            f'<path d="M-74,14 C-50,24 -14,36 12,58 C26,76 38,98 60,108 L-74,112 Z" fill="{SKIN_SHADOW}" opacity="0.38"/>'
            f'<path d="M31,-22 Q50,-29 66,-16 Q62,6 46,6 Q34,4 31,-22 Z" fill="{SKIN_SHADOW}" opacity="0.60"/>'
            f'<path d="M48,-52 Q62,-42 64,-18 L54,-16 Q50,-36 42,-48 Z" fill="{SKIN_LIGHT}" opacity="0.46"/>'
            f'<path d="M-14,38 C-4,66 10,74 28,62 C44,50 58,46 74,42 L74,112 L-14,112 Z" fill="url(#{gid_stub})"/>'
            + _stubble_stipple("side")
            + f'<path d="M65,-36 L67,-16 L84,28" fill="none" stroke="#FFF2E4" stroke-width="2.2" opacity="0.34" stroke-linecap="round"/>'
        )
        buzz_top = (
            "M-76,22 L-76,-102 L72,-102 L72,-40 "
            "L63,-42 C57,-56 40,-63 18,-63 C-6,-63 -21,-52 -25,-30 "
            "L-27,-4 L-36,16 L-52,24 Z"
        )
        buzz_fade = (
            "M-76,34 L-50,34 L-33,20 L-24,-2 L-22,-26 C-18,-46 -4,-58 18,-58 "
            "C40,-58 56,-50 63,-36 L72,-36 L72,-102 L-76,-102 Z"
        )
        inner.append(
            f'<defs><clipPath id="{cid_buzz}"><path d="{buzz_top}"/></clipPath></defs>'
            f'<path d="{buzz_fade}" fill="url(#{gid_sidefade})"/>'
            f'<path d="{buzz_top}" fill="url(#{gid_buzz})"/>'
            f'<g clip-path="url(#{cid_buzz})">{_buzzcut_stipple("side")}</g>'
            f'<ellipse cx="0" cy="-84" rx="30" ry="6.5" fill="{BUZZ_LIGHT}" opacity="0.30"/>'
        )

    # İdam koridoru soğuk floresan rim ışığı (gerilim ifadesi — yumuşak sinematik rim)
    if is_cold:
        inner.append(f'<rect x="-82" y="-98" width="184" height="218" fill="url(#{gid_cold})"/>')
        if view == "front":
            inner.append(
                f'<path d="M67,-14 L66,26 C62,54 52,78 36,96" fill="none" stroke="{COLD_RIM}" stroke-width="2.2" opacity="0.56" stroke-linecap="round"/>'
            )
        elif view == "3q":
            inner.append(
                f'<path d="M70,-22 L72,18 C69,50 58,78 38,100" fill="none" stroke="{COLD_RIM}" stroke-width="2.3" opacity="0.58" stroke-linecap="round"/>'
            )
        else:
            inner.append(
                f'<path d="M66,-36 L67,-16 L85,28 M69,40 L71,68 L67,92" fill="none" stroke="{COLD_RIM}" stroke-width="2.0" opacity="0.56" stroke-linecap="round"/>'
            )

    o.append(f'<g clip-path="url(#{cid_face})">{"".join(inner)}</g>')

    # ── 4. Ana Dış Kontur (2.1px kilitli) ──
    o.append(f'<path d="{face_d}" fill="none" stroke="{INK}" stroke-width="2.1" stroke-linejoin="round"/>')

    # ── 5. Gözler + Kalın Hafif Çatık/Koruyucu Kaşlar ──
    for idx, (ex, ey, erx, ery, is_side) in enumerate(eye_specs):
        o.append(_render_eye(ex, ey, erx, ery, lu, ll, lk, cold_light=is_cold, side=is_side))
        if view == "front":
            sgn = -1 if ex < 0 else 1
            x_in = ex - sgn * (erx * 0.96)
            x_out = ex + sgn * (erx * 1.20)
            y_in = ey - ery * 1.80 + bi * 0.72
            y_out = ey - ery * 1.88 + bo * 0.72
            o.append(_render_brow(x_in, y_in, x_out, y_out, arch_y=-1.0, thick=7.4))
        elif view == "3q":
            if idx == 0:
                x_in, x_out = ex + erx * 0.98, ex - erx * 1.22
            else:
                x_in, x_out = ex - erx * 0.96, ex + erx * 1.14
            y_in = ey - ery * 1.80 + bi * 0.72
            y_out = ey - ery * 1.88 + bo * 0.72
            o.append(_render_brow(x_in, y_in, x_out, y_out, arch_y=-1.0, thick=7.3 if idx == 0 else 6.4))
        else:
            x_in, x_out = ex + erx * 1.16, ex - erx * 1.26
            y_in = ey - ery * 1.80 + bi * 0.72
            y_out = ey - ery * 1.88 + bo * 0.72
            o.append(_render_brow(x_in, y_in, x_out, y_out, arch_y=-0.9, thick=7.0))

    # Kaş arası (glabella) çizgileri — Lincoln'de daha belirgin, koruyucu/sert karakter
    gx = 0.0 if view == "front" else (20.5 if view == "3q" else 59.5)
    if view != "side":
        op_g = 0.88 if extra == "frown_hard" else (0.62 if extra in ("frown_soft", "cold_corridor") else 0.36)
        o.append(
            f'<path d="M{gx - 3.6:.1f},-24.0 L{gx - 2.4:.1f},-13.5 M{gx + 3.6:.1f},-24.0 L{gx + 2.4:.1f},-13.5" '
            f'fill="none" stroke="{SKIN_DEEP}" stroke-width="1.4" opacity="{op_g}" stroke-linecap="round"/>'
        )
        if extra == "frown_hard":
            o.append(
                f'<path d="M{gx - 5.5:.1f},-13.0 Q{gx:.1f},-11.0 {gx + 5.5:.1f},-13.0" '
                f'fill="none" stroke="{SKIN_DEEP}" stroke-width="1.35" opacity="0.72" stroke-linecap="round"/>'
            )

    # Alın çizgileri (olgun ağabey ifadesi, öfke/gerilimde belirginleşir)
    if view != "side" and extra in ("frown_hard", "cold_corridor", "tear"):
        fx = 0.0 if view == "front" else 14.0
        o.append(
            f'<path d="M{fx - 24:.1f},-41 Q{fx:.1f},-44 {fx + 24:.1f},-41 M{fx - 18:.1f},-35 Q{fx:.1f},-37 {fx + 18:.1f},-35" '
            f'fill="none" stroke="{SKIN_DEEP}" stroke-width="1.15" opacity="0.45" stroke-linecap="round"/>'
        )

    # ── 6. Burun (Michael'dan biraz daha geniş ve sağlam köprülü) ──
    if view == "front":
        o.append(
            f'<path d="M-5.8,-12 L-7.4,24" fill="none" stroke="{SKIN_SHADOW}" stroke-width="1.3" opacity="0.62" stroke-linecap="round"/>'
            f'<path d="M-12.4,27.5 Q-7.2,34.0 0,34.6 Q7.2,34.0 12.4,27.5" fill="none" stroke="{INK_SOFT}" stroke-width="1.85" stroke-linecap="round"/>'
            f'<path d="M-14.6,25.8 Q-15.6,30.6 -9.8,31.8 M14.6,25.8 Q15.6,30.6 9.8,31.8" fill="none" stroke="{INK_SOFT}" stroke-width="1.3" opacity="0.78" stroke-linecap="round"/>'
            f'<ellipse cx="-6.4" cy="31.5" rx="2.9" ry="1.3" fill="{SKIN_DEEP}" opacity="0.78"/>'
            f'<ellipse cx="6.4" cy="31.5" rx="2.9" ry="1.3" fill="{SKIN_DEEP}" opacity="0.78"/>'
        )
    elif view == "3q":
        o.append(
            f'<path d="M21.4,-12 L36.0,25.0 Q32.2,35.6 19.6,34.4 L16.0,28.0 Z" fill="{SKIN_SHADOW}" opacity="0.44"/>'
            f'<path d="M21.0,-13 L35.2,24.6 Q37.0,30.8 29.8,34.2 Q23.8,35.6 18.4,33.0" '
            f'fill="none" stroke="{INK}" stroke-width="1.95" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="M15.4,27.4 Q13.8,31.8 19.0,33.2" fill="none" stroke="{INK_SOFT}" stroke-width="1.35" opacity="0.82" stroke-linecap="round"/>'
            f'<ellipse cx="24.6" cy="32.4" rx="3.0" ry="1.3" fill="{SKIN_DEEP}" opacity="0.82"/>'
            f'<path d="M19.8,-9 L31.2,22.6" fill="none" stroke="#FFF2E4" stroke-width="2.0" opacity="0.44" stroke-linecap="round"/>'
        )
    else:
        o.append(
            f'<path d="M64.0,28.5 Q61.8,34.2 69.2,35.2" fill="none" stroke="{INK_SOFT}" stroke-width="1.4" opacity="0.86" stroke-linecap="round"/>'
            f'<ellipse cx="71.2" cy="33.5" rx="3.2" ry="1.35" fill="{SKIN_DEEP}" opacity="0.80"/>'
        )

    # ── 7. Philtrum + Ağız + Güçlü Nazolabial/Çene Hatları ──
    if view == "front":
        o.append(
            f'<path d="M-2.6,37.5 L-3.0,48.5 M2.6,37.5 L3.0,48.5" fill="none" stroke="{SKIN_SHADOW}" stroke-width="1.05" opacity="0.42" stroke-linecap="round"/>'
        )
    elif view == "3q":
        o.append(
            f'<path d="M25.6,37.5 L26.2,48.5" fill="none" stroke="{SKIN_SHADOW}" stroke-width="1.15" opacity="0.40" stroke-linecap="round"/>'
        )
    o.append(_render_mouth(mx, my, mw, mk, view))

    if view == "front":
        o.append(
            f'<path d="M-50,25 Q-46,45 -38,60" fill="none" stroke="{SKIN_DEEP}" stroke-width="1.25" opacity="0.42" stroke-linecap="round"/>'
            f'<path d="M50,25 Q46,45 38,60" fill="none" stroke="{SKIN_DEEP}" stroke-width="1.25" opacity="0.46" stroke-linecap="round"/>'
            f'<path d="M-12,95 Q0,99 12,95" fill="none" stroke="{SKIN_DEEP}" stroke-width="1.35" opacity="0.52" stroke-linecap="round"/>'
        )
    elif view == "3q":
        o.append(
            f'<path d="M-44,25 Q-37,46 -24,62" fill="none" stroke="{SKIN_DEEP}" stroke-width="1.25" opacity="0.40" stroke-linecap="round"/>'
            f'<path d="M10,95 Q22,99 34,94" fill="none" stroke="{SKIN_DEEP}" stroke-width="1.35" opacity="0.52" stroke-linecap="round"/>'
        )

    # ── 8. İfade Ekstraları ──
    if extra == "tear":
        ex, ey = eye_specs[-1][0], eye_specs[-1][1]
        o.append(
            f'<path d="M{ex - 1:.1f},{ey + 8:.1f} Q{ex + 3:.1f},{ey + 23:.1f} {ex + 1:.1f},{ey + 36:.1f}" '
            f'fill="none" stroke="#C4E6FA" stroke-width="2.3" opacity="0.82" stroke-linecap="round"/>'
            f'<ellipse cx="{ex + 1:.1f}" cy="{ey + 40:.1f}" rx="2.5" ry="4.0" fill="#CBEBFF" stroke="#5A8FB0" stroke-width="1.05"/>'
            f'<circle cx="{ex:.1f}" cy="{ey + 38.6:.1f}" r="0.95" fill="#FFFFFF"/>'
        )
    elif is_cold:
        # İdam koridoru gerilimi: şakakta ince ter damlası
        sx = -49 if view != "side" else 16
        o.append(
            f'<path d="M{sx},-30 Q{sx - 3.6},-19 {sx},-15 Q{sx + 3.6},-19 {sx},-30 Z" '
            f'fill="#D6EFFF" stroke="#6E99B8" stroke-width="1.0" opacity="0.84"/>'
        )

    return "".join(o)


def _render_hand(cx: float, cy: float, scale: float, skin: str, skin_sh: str, mirror: bool = False) -> str:
    """Anatomik sinematik 2D el (Lincoln: biraz daha geniş/ağır el yapısı)."""
    sx = -scale if mirror else scale
    return (
        f'<g transform="translate({cx:.1f},{cy:.1f}) scale({sx:.3f},{scale:.3f})">'
        f'<path d="M-13,-4 C-15,9 -15,19 -11,26 L9,25 C14,17 15,6 12,-4 Z" fill="{skin}" stroke="{INK}" stroke-width="2.1" stroke-linejoin="round"/>'
        f'<path d="M-11,2 C-20,8 -21,19 -15,27 C-12,29 -8,26 -9,19 L-8,12" fill="{skin}" stroke="{INK}" stroke-width="2.0" stroke-linecap="round" stroke-linejoin="round"/>'
        f'<path d="M-9,23 L-10,41 C-10,45 -5,45 -5,41 L-4,25" fill="{skin}" stroke="{INK}" stroke-width="1.9" stroke-linejoin="round"/>'
        f'<path d="M-4,24 L-4,44 C-4,48 2,48 2,44 L2,25" fill="{skin}" stroke="{INK}" stroke-width="1.9" stroke-linejoin="round"/>'
        f'<path d="M2,24 L3,42 C3,46 9,46 9,42 L8,24" fill="{skin}" stroke="{INK}" stroke-width="1.9" stroke-linejoin="round"/>'
        f'<path d="M8,22 L10,36 C10,39 15,39 15,36 L12,20" fill="{skin_sh}" stroke="{INK}" stroke-width="1.8" stroke-linejoin="round"/>'
        f'<path d="M-5,4 L-4,17 M2,4 L3,17" fill="none" stroke="{skin_sh}" stroke-width="1.3" opacity="0.68" stroke-linecap="round"/>'
        f'</g>'
    )


def figur_lincoln(ifade: str = "odak", numara_goster: bool = True) -> str:
    """Tam boy Lincoln Burrows (v1 — Stil B + A hibrit, sinematik 2D).
    Ayak tabanı y=0, toplam boy ~574 (y: -574 .. 0).
    Michael'dan ~1.18x daha geniş omuzlu, ağır/kaslı yapılı, kalın boyunlu (R4),
    DÖVMESİZ güçlü kollar (R3), Fox River İdam Koğuşu gömleği (79238).
    """
    o: list[str] = []

    tid_torso = _uid("torso")
    cid_fa_l = _uid("fal")
    cid_fa_r = _uid("far")
    gid_sh = _uid("shg")
    gid_pt = _uid("ptg")

    o.append(
        f'<defs>'
        f'<linearGradient id="{gid_sh}" x1="0.1" y1="0.05" x2="0.92" y2="0.95">'
        f'<stop offset="0%" stop-color="{SHIRT_LIGHT}"/>'
        f'<stop offset="44%" stop-color="{SHIRT_BASE}"/>'
        f'<stop offset="100%" stop-color="{SHIRT_DARK}"/>'
        f'</linearGradient>'
        f'<linearGradient id="{gid_pt}" x1="0.15" y1="0.0" x2="0.85" y2="1.0">'
        f'<stop offset="0%" stop-color="{PANTS_LIGHT}"/>'
        f'<stop offset="45%" stop-color="{PANTS_BASE}"/>'
        f'<stop offset="100%" stop-color="{PANTS_DARK}"/>'
        f'</linearGradient>'
        f'</defs>'
    )

    # Zemin gölgesi (daha ağır/geniş duruş)
    o.append('<ellipse cx="4" cy="4" rx="102" ry="14" fill="#000000" opacity="0.38"/>')

    # ── 1. Bacaklar & Ağır Botlar (daha sağlam ve kaslı) ──
    leg_back = (
        "M-52,-254 L-58,-132 C-60,-116 -56,-88 -54,-24 L-12,-24 "
        "C-10,-88 -10,-118 -12,-140 L-4,-254 Z"
    )
    o.append(
        f'<path d="{leg_back}" fill="{PANTS_DARK}" stroke="{INK}" stroke-width="2.2" stroke-linejoin="round"/>'
        f'<path d="M-48,-144 Q-32,-136 -16,-146 M-44,-36 Q-30,-30 -16,-38" fill="none" stroke="#11161F" stroke-width="1.6" opacity="0.72" stroke-linecap="round"/>'
        # Ağır sol bot
        f'<path d="M-56,-28 L-12,-28 C2,-23 14,-15 16,-2 L-58,-2 Z" fill="{SHOE_BASE}" stroke="{INK}" stroke-width="2.2" stroke-linejoin="round"/>'
        f'<path d="M-58,-7 L16,-7 L16,-1 L-58,-1 Z" fill="{SHOE_SOLE}"/>'
        f'<path d="M-24,-22 L-14,-18 M-20,-16 L-10,-12" fill="none" stroke="#4A423D" stroke-width="1.3" opacity="0.6" stroke-linecap="round"/>'
    )

    leg_front = (
        "M-4,-254 L4,-134 C6,-116 14,-82 22,-22 L66,-22 "
        "C62,-82 58,-118 56,-138 L54,-254 Z"
    )
    o.append(
        f'<path d="{leg_front}" fill="url(#{gid_pt})" stroke="{INK}" stroke-width="2.2" stroke-linejoin="round"/>'
        f'<path d="M6,-242 L15,-136 L28,-30" fill="none" stroke="#4F627B" stroke-width="3.6" opacity="0.28" stroke-linecap="round"/>'
        f'<path d="M10,-142 Q30,-134 52,-146 M16,-126 Q32,-120 48,-130 M26,-36 Q44,-30 62,-38" fill="none" stroke="#141A24" stroke-width="1.6" opacity="0.68" stroke-linecap="round"/>'
        # Ağır sağ bot (kalın tabanlı)
        f'<path d="M20,-24 L66,-24 C84,-19 96,-11 98,2 L18,2 Z" fill="{SHOE_BASE}" stroke="{INK}" stroke-width="2.2" stroke-linejoin="round"/>'
        f'<path d="M18,-6 L98,-6 L98,2 L18,2 Z" fill="{SHOE_SOLE}"/>'
        f'<path d="M62,-18 Q78,-15 90,-8 M52,-21 L62,-17 M56,-15 L66,-11" fill="none" stroke="#4D4540" stroke-width="1.5" opacity="0.60" stroke-linecap="round"/>'
    )

    # ── 2. Uzak Kol (Sol kol — sıvalı, KASLI ve KESİNLİKLE DÖVMESİZ — R3!) ──
    ua_l = "M-74,-438 C-94,-426 -106,-386 -106,-338 L-66,-334 C-62,-374 -58,-404 -58,-430 Z"
    fa_l = "M-102,-336 C-108,-302 -102,-266 -92,-234 L-68,-236 C-65,-272 -65,-304 -68,-336 Z"
    o.append(
        f'<defs><clipPath id="{cid_fa_l}"><path d="{fa_l}"/></clipPath></defs>'
        f'<path d="{fa_l}" fill="{SKIN_MID}"/>'
        f'<g clip-path="url(#{cid_fa_l})">'
        # Dövme YOK — yalnızca kaslı önkol anatomisi (brachioradialis gölgesi & ışık)
        f'<path d="M-106,-336 L-102,-234 L-88,-234 L-92,-336 Z" fill="{SKIN_SHADOW}" opacity="0.44"/>'
        f'<path d="M-86,-324 Q-80,-292 -82,-250" fill="none" stroke="{SKIN_DEEP}" stroke-width="1.4" opacity="0.34" stroke-linecap="round"/>'
        f'</g>'
        f'<path d="{fa_l}" fill="none" stroke="{INK}" stroke-width="2.15" stroke-linejoin="round"/>'
        + _render_hand(-80, -234, 0.94, SKIN_MID, SKIN_SHADOW, mirror=True)
        + f'<path d="{ua_l}" fill="{SHIRT_DARK}" stroke="{INK}" stroke-width="2.15" stroke-linejoin="round"/>'
        f'<path d="M-110,-350 Q-86,-343 -62,-348 L-64,-330 Q-86,-325 -108,-332 Z" fill="{SHIRT_MID}" stroke="{INK}" stroke-width="2.0" stroke-linejoin="round"/>'
        f'<path d="M-106,-340 Q-86,-335 -66,-339" fill="none" stroke="{SHIRT_DARK}" stroke-width="1.4" opacity="0.72"/>'
    )

    # ── 3. Gövde (1.18x Geniş Omuzlu, Ağır/Kaslı Fox River İdam Koğuşu Gömleği) ──
    torso_d = (
        "M-78,-432 C-80,-388 -70,-338 -64,-300 L-68,-248 "
        "C-24,-237 28,-237 68,-250 L64,-300 "
        "C72,-340 82,-388 80,-430 C64,-444 46,-452 32,-462 "
        "L-30,-462 C-44,-452 -62,-444 -78,-432 Z"
    )
    o.append(
        f'<defs><clipPath id="{tid_torso}"><path d="{torso_d}"/></clipPath></defs>'
        f'<path d="{torso_d}" fill="url(#{gid_sh})"/>'
    )

    torso_inner = [
        # Sağ yarı derin gölge
        f'<path d="M30,-464 C52,-416 50,-342 40,-240 L88,-240 L88,-464 Z" fill="{SHIRT_DARK}" opacity="0.50"/>',
        # Geniş göğüs kası (pektoral) ışık ve alt gölge vurgusu
        f'<path d="M-66,-424 C-50,-390 -48,-336 -52,-260" fill="none" stroke="#9EBEDB" stroke-width="6.5" opacity="0.22" stroke-linecap="round"/>',
        f'<path d="M-56,-372 Q-26,-364 -2,-370 M22,-370 Q46,-364 68,-374" fill="none" stroke="{SHIRT_DARK}" stroke-width="1.6" opacity="0.46" stroke-linecap="round"/>',
        # Düğme patı (üstten daha açık)
        f'<path d="M4,-394 L8,-242 M16,-394 L20,-242" fill="none" stroke="{SHIRT_DARK}" stroke-width="1.45" opacity="0.72"/>',
        "".join(
            f'<circle cx="{12.2 + k * 0.9:.1f}" cy="{-376 + k * 34:.1f}" r="2.8" fill="#E6E3DA" stroke="{INK}" stroke-width="1.1"/>'
            for k in range(4)
        ),
        # Sol göğüs cebi
        f'<path d="M-54,-386 L-12,-386 L-12,-350 Q-33,-343 -54,-350 Z" fill="{SHIRT_MID}" opacity="0.36" stroke="{INK}" stroke-width="1.65" stroke-linejoin="round"/>',
        f'<path d="M-54,-378 L-12,-378" fill="none" stroke="{SHIRT_DARK}" stroke-width="1.25" opacity="0.72"/>',
        # Kumaş kıvrımları
        f'<path d="M-64,-396 Q-44,-388 -32,-394 M-56,-284 Q-26,-276 -4,-286 M28,-292 Q48,-286 62,-296 M38,-388 Q56,-380 72,-394" '
        f'fill="none" stroke="{SHIRT_DARK}" stroke-width="1.5" opacity="0.64" stroke-linecap="round"/>',
        f'<path d="M-68,-252 Q0,-241 68,-254" fill="none" stroke="{SHIRT_DARK}" stroke-width="3.2" opacity="0.52"/>',
    ]
    if numara_goster:
        torso_inner.append(
            '<text x="-52" y="-393" font-family="Consolas, DejaVu Sans Mono, monospace" font-weight="bold" '
            'font-size="14" letter-spacing="0.7" fill="#EEF2F6" opacity="0.95">79238</text>'
        )

    o.append(
        f'<g clip-path="url(#{tid_torso})">{"".join(torso_inner)}</g>'
        f'<path d="{torso_d}" fill="none" stroke="{INK}" stroke-width="2.2" stroke-linejoin="round"/>'
    )

    # ── 4. R4: Kalın, Kaslı Anatomik Boyun + Belirgin Trapezler + Açık Yaka + Beyaz Atlet ──
    # Arka yaka bandı
    o.append(
        f'<path d="M-36,-458 Q4,-474 38,-458 L34,-442 Q4,-452 -32,-442 Z" fill="{SHIRT_DARK}" stroke="{INK}" stroke-width="2.05" stroke-linejoin="round"/>'
    )
    # Üstten açık gömleğin altından belirgin görünen beyaz atlet (V-açıklık)
    o.append(
        f'<path d="M-28,-448 Q4,-416 32,-448 L12,-392 L-4,-392 Z" fill="{UNDER_BASE}" stroke="{INK}" stroke-width="1.8" stroke-linejoin="round"/>'
        f'<path d="M-22,-442 Q4,-422 28,-442" fill="none" stroke="{UNDER_SH}" stroke-width="2.5" opacity="0.84"/>'
        f'<path d="M-12,-418 Q4,-412 18,-418" fill="none" stroke="{UNDER_SH}" stroke-width="1.6" opacity="0.65"/>'
    )
    # Kalın boyun + trapez kasları (Michael'dan belirgin biçimde daha kalın ve güçlü)
    neck_d = (
        "M-27,-492 L-30,-456 C-34,-448 -24,-438 -10,-428 "
        "Q4,-420 18,-428 C30,-438 34,-448 30,-456 L26,-488 Z"
    )
    o.append(
        f'<path d="{neck_d}" fill="{SKIN_BASE}"/>'
        # Sağ yarı boyun gölgesi
        f'<path d="M4,-490 L26,-488 L30,-454 C28,-442 18,-432 8,-426 L6,-452 Z" fill="{SKIN_SHADOW}" opacity="0.50"/>'
        # Çene altı derin düşüm gölgesi
        f'<path d="M-27,-492 L26,-488 L29,-462 Q4,-448 -29,-464 Z" fill="{SKIN_DEEP}" opacity="0.68"/>'
        # Güçlü SCM kasları ve köprücük çukuru
        f'<path d="M-24,-476 Q-12,-452 2,-432 M22,-472 Q16,-452 10,-434" fill="none" stroke="{SKIN_SHADOW}" stroke-width="2.1" opacity="0.66" stroke-linecap="round"/>'
        f'<path d="M-6,-434 Q4,-428 14,-434" fill="none" stroke="{SKIN_DEEP}" stroke-width="1.7" opacity="0.64" stroke-linecap="round"/>'
        # Boyun dış hatları (yaka içine temiz oturum, taşma yok)
        f'<path d="M-27,-492 L-30,-456 M26,-488 L30,-456" '
        f'fill="none" stroke="{INK}" stroke-width="2.15" stroke-linecap="round"/>'
    )
    # Açık gömlek yakası kanatları (boyuna ve omuzlara sağlam oturur)
    o.append(
        f'<path d="M-36,-458 L-28,-448 L-4,-398 L-38,-416 Z" fill="{SHIRT_LIGHT}" stroke="{INK}" stroke-width="2.05" stroke-linejoin="round"/>'
        f'<path d="M38,-458 L30,-448 L16,-398 L44,-418 Z" fill="{SHIRT_BASE}" stroke="{INK}" stroke-width="2.05" stroke-linejoin="round"/>'
        f'<path d="M-36,-414 L-4,-396 M16,-396 L42,-416" fill="none" stroke="{SHIRT_DARK}" stroke-width="2.3" opacity="0.58" stroke-linecap="round"/>'
    )

    # ── 5. Baş (Geniş gövdeye oranlı güçlü yerleşim) ──
    o.append(
        f'<g transform="translate(8,-520) scale(0.51)">'
        f'{kafa_lincoln(view="3q", ifade=ifade, look=0.25, boyun=False)}'
        f'</g>'
    )

    # ── 6. Yakın Kol (Sağ kol — sıvalı, KASLI ve KESİNLİKLE DÖVMESİZ — R3!) ──
    ua_r = "M78,-430 C96,-416 108,-382 108,-334 L64,-328 C62,-364 62,-390 62,-406 C68,-418 73,-426 78,-430 Z"
    fa_r = "M104,-332 C108,-296 102,-260 92,-226 L68,-228 C65,-264 65,-300 68,-332 Z"
    o.append(
        f'<defs><clipPath id="{cid_fa_r}"><path d="{fa_r}"/></clipPath></defs>'
        f'<path d="{fa_r}" fill="{SKIN_BASE}"/>'
        f'<g clip-path="url(#{cid_fa_r})">'
        # Dövme YOK — güçlü önkol kas düzlemi ve sıcak rim ışığı
        f'<path d="M90,-332 L110,-332 L104,-226 L84,-226 Z" fill="{SKIN_SHADOW}" opacity="0.40"/>'
        f'<path d="M84,-320 Q80,-288 82,-248" fill="none" stroke="{SKIN_DEEP}" stroke-width="1.5" opacity="0.34" stroke-linecap="round"/>'
        f'<path d="M72,-324 L71,-236" fill="none" stroke="#FFF2E4" stroke-width="3.2" opacity="0.30" stroke-linecap="round"/>'
        f'</g>'
        f'<path d="{fa_r}" fill="none" stroke="{INK}" stroke-width="2.15" stroke-linejoin="round"/>'
        + _render_hand(80, -226, 0.96, SKIN_BASE, SKIN_SHADOW, mirror=False)
        + f'<path d="{ua_r}" fill="url(#{gid_sh})"/>'
        f'<path d="M78,-430 C96,-416 108,-382 108,-334 L64,-328 C62,-364 62,-390 62,-406" fill="none" stroke="{INK}" stroke-width="2.2" stroke-linejoin="round" stroke-linecap="round"/>'
        f'<path d="M62,-406 C66,-418 72,-426 78,-430" fill="none" stroke="{SHIRT_DARK}" stroke-width="1.5" opacity="0.72" stroke-linecap="round"/>'
        f'<path d="M84,-416 C96,-388 98,-362 96,-344" fill="none" stroke="{SHIRT_DARK}" stroke-width="1.6" opacity="0.56" stroke-linecap="round"/>'
        # Kıvrılmış gömlek kolu manşeti
        f'<path d="M62,-344 Q86,-337 112,-344 L109,-324 Q86,-319 63,-326 Z" fill="{SHIRT_LIGHT}" stroke="{INK}" stroke-width="2.1" stroke-linejoin="round"/>'
        f'<path d="M65,-334 Q86,-329 107,-334" fill="none" stroke="{SHIRT_DARK}" stroke-width="1.5" opacity="0.70"/>'
    )

    return "".join(o)


def _portre_ziyaret_cami() -> str:
    """Alt sağ panel için yakın plan omuz-portre:
    Fox River ziyaret camı yansıması + sıcak (sol) / soğuk (sağ) kontrast ışığı.
    """
    gid_warm = _uid("warmg")
    gid_cold = _uid("coldg")
    gid_glass = _uid("glassg")
    return (
        f'<defs>'
        f'<radialGradient id="{gid_warm}" cx="0.22" cy="0.38" r="0.58">'
        f'<stop offset="0%" stop-color="{WARM_RIM}" stop-opacity="0.26"/>'
        f'<stop offset="60%" stop-color="{WARM_RIM}" stop-opacity="0.06"/>'
        f'<stop offset="100%" stop-color="{WARM_RIM}" stop-opacity="0.0"/>'
        f'</radialGradient>'
        f'<radialGradient id="{gid_cold}" cx="0.80" cy="0.44" r="0.58">'
        f'<stop offset="0%" stop-color="{COLD_RIM}" stop-opacity="0.26"/>'
        f'<stop offset="60%" stop-color="{COLD_RIM}" stop-opacity="0.06"/>'
        f'<stop offset="100%" stop-color="{COLD_RIM}" stop-opacity="0.0"/>'
        f'</radialGradient>'
        f'<linearGradient id="{gid_glass}" x1="0" y1="0" x2="1" y2="1">'
        f'<stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.14"/>'
        f'<stop offset="35%" stop-color="#D4ECFA" stop-opacity="0.03"/>'
        f'<stop offset="68%" stop-color="#FFFFFF" stop-opacity="0.11"/>'
        f'<stop offset="100%" stop-color="#8DC5DF" stop-opacity="0.04"/>'
        f'</linearGradient>'
        f'</defs>'
        # Ziyaret odası arka duvar + idam koğuşu parmaklık derinliği
        f'<rect x="-432" y="-104" width="864" height="208" fill="#131A23"/>'
        f'<rect x="-432" y="-104" width="864" height="208" fill="url(#{gid_warm})"/>'
        f'<rect x="-432" y="-104" width="864" height="208" fill="url(#{gid_cold})"/>'
        # Arka planda bulanık/ince dikey parmaklık & beton fugalar
        f'<g opacity="0.20" stroke="#4D667D" fill="none">'
        f'<path d="M-360,-104 V104 M-285,-104 V104 M-210,-104 V104 M220,-104 V104 M295,-104 V104 M370,-104 V104" stroke-width="5.5"/>'
        f'<path d="M-432,-30 H432 M-432,38 H432" stroke-width="1.2" opacity="0.6"/>'
        f'</g>'
        # Lincoln yakın plan omuz-portre (hafif sola ofsetli, sağa/kardeşine bakan koruyucu-gerilimli bakış)
        f'<g transform="translate(-14, 496) scale(0.98)">'
        f'{figur_lincoln(ifade="gerilim", numara_goster=True)}'
        f'</g>'
        # Ziyaret camı: diyagonal yansıma bantları + ince çizikler + metal konuşma ızgarası (sağ alt)
        f'<polygon points="-240,-104 -145,-104 -290,104 -385,104" fill="url(#{gid_glass})"/>'
        f'<polygon points="105,-104 165,-104 20,104 -40,104" fill="url(#{gid_glass})"/>'
        f'<polygon points="240,-104 268,-104 123,104 95,104" fill="#FFFFFF" opacity="0.06"/>'
        f'<path d="M-310,-62 L-190,-68 M185,18 L270,12 M-140,42 L-82,36" fill="none" stroke="#E4F4FF" stroke-width="0.9" opacity="0.24" stroke-linecap="round"/>'
        # Ziyaret camı konuşma ızgarası (sağ tarafta sinematik detay)
        f'<g transform="translate(270, 22)" opacity="0.58">'
        f'<circle cx="0" cy="0" r="34" fill="#18222D" stroke="#4D657B" stroke-width="2.0"/>'
        f'<circle cx="0" cy="0" r="27" fill="none" stroke="#2D3E4F" stroke-width="1.2"/>'
        + "".join(
            f'<circle cx="{dx}" cy="{dy}" r="2.1" fill="#0B1016"/>'
            for dx in (-14, -7, 0, 7, 14)
            for dy in (-14, -7, 0, 7, 14)
            if dx * dx + dy * dy <= 21 * 21
        )
        + '</g>'
        # Camın üst ve alt çelik çerçeve kenarı
        f'<path d="M-432,-98 H432 M-432,98 H432" fill="none" stroke="#3B5268" stroke-width="2.2" opacity="0.50"/>'
    )


def build_model_card_svg() -> str:
    """1280x720 Lincoln Burrows Model Kartı v1 (al_lincoln_v1.png)."""
    W, H = 1280, 720
    parts: list[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
        '<defs>',
        '<linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">'
        '<stop offset="0%" stop-color="#131921"/>'
        '<stop offset="55%" stop-color="#1B232E"/>'
        '<stop offset="100%" stop-color="#11161D"/>'
        '</linearGradient>',
        '<radialGradient id="spotL" cx="0.5" cy="0.46" r="0.52">'
        '<stop offset="0%" stop-color="#2D3C4E" stop-opacity="0.72"/>'
        '<stop offset="100%" stop-color="#141B23" stop-opacity="0.0"/>'
        '</radialGradient>',
        '<clipPath id="clipPortre"><rect x="394" y="492" width="860" height="202" rx="10"/></clipPath>',
        '</defs>',
        f'<rect width="{W}" height="{H}" fill="url(#bgGrad)"/>',
    ]

    grid = [f"M{x},0 V{H}" for x in range(0, W + 1, 40)] + [f"M0,{y} H{W}" for y in range(0, H + 1, 40)]
    parts.append(f'<path d="{" ".join(grid)}" fill="none" stroke="{COLD_RIM}" stroke-width="0.6" opacity="0.045"/>')

    # Üst başlık ve renk paleti
    parts.append(
        '<text x="28" y="34" font-family="Segoe UI, DejaVu Sans, sans-serif" font-weight="700" font-size="18" fill="#E8EEF5" letter-spacing="1.0">'
        'LINCOLN BURROWS · MODEL KARTI v1</text>'
        '<text x="436" y="33" font-family="Segoe UI, DejaVu Sans, sans-serif" font-size="12.5" fill="#8DC5DF">'
        'STİL B+A HİBRİT · FOX RIVER İDAM KOĞUŞU (A-Y v3 UYUMLU)</text>'
    )
    swatches = [
        (SKIN_BASE, "TEN"),
        (BUZZ_TOP, "SAÇ"),
        (IRIS_BASE, "GÖZ"),
        (SHIRT_BASE, "GÖMLEK"),
        (COLD_RIM, "KORİDOR"),
    ]
    for i, (col, lbl) in enumerate(swatches):
        sx = 876 + i * 76
        parts.append(
            f'<rect x="{sx}" y="16" width="15" height="15" rx="3" fill="{col}" stroke="#44566B" stroke-width="1"/>'
            f'<text x="{sx + 20}" y="27.5" font-family="Segoe UI, DejaVu Sans, sans-serif" font-size="10" fill="#9BB0C5">{lbl}</text>'
        )

    # ── SOL PANEL: Tam Boy Lincoln ──
    parts.append(
        '<rect x="24" y="54" width="350" height="642" rx="12" fill="#171F2A" stroke="#2C3B4D" stroke-width="1.4"/>'
        '<ellipse cx="199" cy="360" rx="154" ry="275" fill="url(#spotL)"/>'
        '<path d="M44,118 H354 M44,376 H354 M44,648 H354" fill="none" stroke="#8DC5DF" stroke-width="0.7" opacity="0.14" stroke-dasharray="4,5"/>'
        f'<g transform="translate(194,648) scale(0.92)">{figur_lincoln(ifade="odak", numara_goster=True)}</g>'
        '<text x="199" y="680" text-anchor="middle" font-family="Segoe UI, DejaVu Sans, sans-serif" font-weight="600" font-size="12.5" fill="#C9D6E4">'
        'FOX RIVER · İDAM KOĞUŞU (79238 · DÖVMESİZ)</text>'
    )

    # ── ÜST SAĞ PANEL: 3 Görünüş ──
    parts.append(
        '<rect x="392" y="54" width="864" height="222" rx="12" fill="#171F2A" stroke="#2C3B4D" stroke-width="1.4"/>'
        '<text x="410" y="76" font-family="Segoe UI, DejaVu Sans, sans-serif" font-weight="600" font-size="11.5" fill="#7F98B2" letter-spacing="1">'
        'ÜÇ GÖRÜNÜŞ (ÖNDEN · 3/4 · YANDAN)</text>'
    )
    views = [
        ("front", "ÖNDEN", 540, 0.0),
        ("3q", "3/4 (ANA AÇI)", 824, 0.25),
        ("side", "YANDAN (PROFİL)", 1108, 0.40),
    ]
    for vw, lbl, cx, lk in views:
        parts.append(
            f'<g transform="translate({cx},158) scale(0.60)">{kafa_lincoln(view=vw, ifade="odak", look=lk, boyun=True)}</g>'
            f'<text x="{cx}" y="264" text-anchor="middle" font-family="Segoe UI, DejaVu Sans, sans-serif" font-size="12" fill="#C4D3E2">{lbl}</text>'
        )

    # ── ORTA SAĞ PANEL: 5 İfade ──
    parts.append(
        '<rect x="392" y="288" width="864" height="190" rx="12" fill="#171F2A" stroke="#2C3B4D" stroke-width="1.4"/>'
        '<text x="410" y="310" font-family="Segoe UI, DejaVu Sans, sans-serif" font-weight="600" font-size="11.5" fill="#7F98B2" letter-spacing="1">'
        'BEŞ İFADE (ODAK · KORUYUCU/ŞEFKAT · ÖFKE · YAS · GERİLİM)</text>'
    )
    exps = [
        ("odak", "odak", "#C4D3E2"),
        ("koruyucu", "koruyucu / şefkat", "#E9C89B"),
        ("ofke", "öfke", "#E8A49B"),
        ("yas", "yas", "#C4D3E2"),
        ("gerilim", "gerilim (koridor)", COLD_RIM),
    ]
    for idx, (ek, elbl, col) in enumerate(exps):
        cx = 482 + idx * 170
        parts.append(
            f'<g transform="translate({cx},386) scale(0.51)">{kafa_lincoln(view="3q", ifade=ek, look=0.25, boyun=False)}</g>'
            f'<text x="{cx}" y="464" text-anchor="middle" font-family="Segoe UI, DejaVu Sans, sans-serif" font-weight="{"700" if ek=="gerilim" else "500"}" font-size="12" fill="{col}">{elbl}</text>'
        )

    # ── ALT SAĞ PANEL: Yakın Plan Omuz-Portre (Ziyaret Camı & Sıcak-Soğuk Kontrast) ──
    parts.append(
        '<rect x="392" y="490" width="864" height="206" rx="12" fill="#131B25" stroke="#2E566B" stroke-width="1.5"/>'
        f'<g clip-path="url(#clipPortre)"><g transform="translate(824,593)">{_portre_ziyaret_cami()}</g></g>'
        '<rect x="402" y="498" width="368" height="22" rx="5" fill="#0E151E" opacity="0.84"/>'
        '<text x="410" y="513" font-family="Segoe UI, DejaVu Sans, sans-serif" font-weight="600" font-size="10.8" fill="#8DC5DF" letter-spacing="0.6">'
        'YAKIN PLAN OMUZ-PORTRE · ZİYARET CAMI (SICAK-SOĞUK KONTRAST)</text>'
    )

    parts.append('</svg>')
    return "".join(parts)


def build_r13_svg() -> str:
    """1280x720 R13 %200 Kırpma Kartı (al_lincoln_r13.png) — 4 yakın kontrol paneli:
      1: 3/4 odak yüz (%200)
      2: önden yüz (%200)
      3: öfke & gerilim ifadeleri (%200)
      4: tam figür boyun-yaka-omuz & dövmesiz kol (%200 — R4 + R3 doğrulaması)
    """
    W, H = 1280, 720
    panels = [
        (20, 48, 610, 316, "1. 3/4 ODAK — YÜZ YAKIN (%200)", False),
        (650, 48, 610, 316, "2. ÖNDEN — YÜZ YAKIN (%200)", False),
        (20, 384, 610, 316, "3. ÖFKE &amp; GERİLİM — İFADE YAKIN (%200)", True),
        (650, 384, 610, 316, "4. BOYUN / YAKA / OMUZ + DÖVMESİZ KOL (%200 · R4+R3)", False),
    ]

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
        '<defs>',
        '<linearGradient id="r13bg" x1="0" y1="0" x2="1" y2="1">'
        '<stop offset="0%" stop-color="#111720"/><stop offset="100%" stop-color="#1A222D"/>'
        '</linearGradient>',
    ]
    for i, (px, py, pw, ph, _, _) in enumerate(panels):
        parts.append(f'<clipPath id="pclip{i}"><rect x="{px+2}" y="{py+2}" width="{pw-4}" height="{ph-4}" rx="9"/></clipPath>')
    parts.append('</defs>')
    parts.append(f'<rect width="{W}" height="{H}" fill="url(#r13bg)"/>')
    parts.append(
        '<text x="22" y="30" font-family="Segoe UI, DejaVu Sans, sans-serif" font-weight="700" font-size="16" fill="#E8EEF5" letter-spacing="1">'
        'R13 · %200 YAKIN KONTROL KARTI — LINCOLN BURROWS v1</text>'
        '<text x="1256" y="30" text-anchor="end" font-family="Segoe UI, DejaVu Sans, sans-serif" font-size="12" fill="#8DC5DF">'
        'R1 / R3 (DÖVMESİZ) / R4 / R10 / R13 DOĞRULAMA</text>'
    )

    contents = [
        # Panel 1: 3/4 odak yüz %200
        f'<g transform="translate(325,208) scale(1.22)">{kafa_lincoln(view="3q", ifade="odak", look=0.25, boyun=True)}</g>',
        # Panel 2: Önden yüz %200
        f'<g transform="translate(955,208) scale(1.22)">{kafa_lincoln(view="front", ifade="odak", look=0.0, boyun=True)}</g>',
        # Panel 3: Öfke (sol) ve Gerilim (sağ) %200 yan yana (temiz rozet etiketlerle)
        (
            f'<g transform="translate(178,542) scale(1.12)">{kafa_lincoln(view="3q", ifade="ofke", look=0.25, boyun=True)}</g>'
            f'<g transform="translate(472,542) scale(1.12)">{kafa_lincoln(view="3q", ifade="gerilim", look=0.25, boyun=True)}</g>'
            f'<rect x="136" y="672" width="84" height="20" rx="4" fill="#0E151E" opacity="0.88"/>'
            f'<text x="178" y="686" text-anchor="middle" font-family="Segoe UI, DejaVu Sans, sans-serif" font-weight="600" font-size="10.5" fill="#E8A49B">ÖFKE</text>'
            f'<rect x="394" y="672" width="156" height="20" rx="4" fill="#0E151E" opacity="0.88"/>'
            f'<text x="472" y="686" text-anchor="middle" font-family="Segoe UI, DejaVu Sans, sans-serif" font-weight="600" font-size="10.5" fill="{COLD_RIM}">GERİLİM (SOĞUK IŞIK)</text>'
        ),
        # Panel 4: Tam figür boyun-yaka-omuz + sıvalı dövmesiz önkollar (R4 + R3 doğrulaması)
        f'<g transform="translate(952,992) scale(1.06)">{figur_lincoln(ifade="odak", numara_goster=True)}</g>',
    ]

    for i, (px, py, pw, ph, title, is_p) in enumerate(panels):
        stroke = "#2E6A82" if is_p else "#2C3B4D"
        tcol = COLD_RIM if is_p else "#9CB2C8"
        parts.append(
            f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="10" fill="#161E29" stroke="{stroke}" stroke-width="1.5"/>'
            f'<g clip-path="url(#pclip{i})">{contents[i]}</g>'
            f'<rect x="{px+10}" y="{py+10}" width="{min(pw - 20, len(title)*7.0 + 18):.0f}" height="24" rx="5" fill="#0F151D" opacity="0.86"/>'
            f'<text x="{px+18}" y="{py+26}" font-family="Segoe UI, DejaVu Sans, sans-serif" font-weight="600" font-size="11.0" fill="{tcol}">{title}</text>'
        )

    parts.append('</svg>')
    return "".join(parts)


def render_svg_to_png(svg_str: str, out_path: Path) -> None:
    png_bytes = resvg_py.svg_to_bytes(svg_str)
    img = Image.open(io.BytesIO(png_bytes))
    img.save(out_path, format="PNG")
    print(f"Kaydedildi: {out_path} ({img.size[0]}x{img.size[1]})")


def main() -> None:
    render_svg_to_png(build_model_card_svg(), OUT_DIR / "al_lincoln_v1.png")
    render_svg_to_png(build_r13_svg(), OUT_DIR / "al_lincoln_r13.png")


if __name__ == "__main__":
    main()
