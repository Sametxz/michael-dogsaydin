"""A-Y (Yetişkin Michael Üretici) — v3 Sinematik 2D (Stil B + A hibrit).
İzole modül: ileride karakter.py'ye entegre edilebilir temiz fonksiyonlar içerir:
  - kafa_yetiskin(view="3q", ifade="odak", look=0.25)
  - figur_yetiskin(ifade="odak", plan=False)
  - dovme_onkol_yetiskin(w=48, h=140, plan=False)

Hizalama sabitleri (A-Ç ile ortak dil):
  - Ana dış kontur: 2.1px (#1A1513), iç anatomi hatları: 1.1–1.4px (#422F26 / #784D39)
  - Göz: buz-mavisi/gri-yeşil #7EB6BE, limbal halka #2F5059, iris yarıçapı ~0.78*ry, odak üst kapak örtüsü 0.36

R1 sınırı: Hiçbir gerçek oyuncunun yüzü veya dizideki gerçek dövme kopyalanmaz.
Yalnızca karakterin genel arketipi (1-2 numara buzzcut, delici sakin buz-mavisi gözler,
alçak düz kaş ve güçlü kaş kemiği gölgesi, keskin kemik yapısı, sakin dolgun dudaklar,
Fox River 94941 gömleği ve özgün mimari/turna plan dövmesi) sinematik 2D kalitesinde çizilir.
"""
from __future__ import annotations

import io
import random
from pathlib import Path
import resvg_py
from PIL import Image

OUT_DIR = Path(__file__).resolve().parent

# ── Sinematik 2D Renk Paleti (v3 — Stil B + A hibrit) ──
INK = "#1A1513"          # Sıcak koyu mürekkep (dış hat: 2.1px)
INK_SOFT = "#422F26"     # İç yüz çizgileri için yumuşak koyu ten konturu (1.1–1.4px)
SKIN_BASE = "#D5A687"    # Ana ten (sıcak nötr-sinematik)
SKIN_LIGHT = "#E9C5AC"   # Işık düzlemi (alın, burun sırtı, elmacık üstü)
SKIN_MID = "#BC8A6B"     # Yarı gölge (elmacık altı, şakak)
SKIN_SHADOW = "#97684E"  # Ana gölge (kaş kemiği altı, uzak yanak, burun yanı)
SKIN_DEEP = "#724734"    # Derin gölge (çene altı boyun düşmesi, göz çukuru)
STUBBLE = "#352C27"      # 1-2 günlük temiz sakal gölgesi
BUZZ_TOP = "#342C27"     # 1-2 numara buzzcut tepe tonu
BUZZ_MID = "#4B4039"     # Buzzcut orta/şakak geçiş tonu
BUZZ_LIGHT = "#62544B"   # Kafa derisi tepe ışığı
IRIS_BASE = "#7EB6BE"    # Buz-mavisi / gri-yeşil odaklı göz
IRIS_DARK = "#2F5059"    # Belirgin koyu limbal halka
IRIS_LIGHT = "#C2E8ED"   # İris alt parlama hilali
BROW_COL = "#241E1A"     # Alçak, düz, belirgin koyu kaş
LIP_TOP = "#9B6355"      # Üst dudak (gölgede, doğal dolgun)
LIP_BOT = "#C78B7B"      # Alt dudak (sakin hacim)

SHIRT_BASE = "#6182A3"   # Fox River mavi gömlek
SHIRT_LIGHT = "#7D9FC1"  # Gömlek omuz/göğüs ışığı
SHIRT_MID = "#4D6B8A"    # Gömlek yarı gölge
SHIRT_DARK = "#374E67"   # Gömlek derin gölge
UNDER_BASE = "#EEEAE1"   # İç beyaz atlet
UNDER_SH = "#CFC9BC"     # Atlet gölgesi
PANTS_BASE = "#2B3646"   # Koyu lacivert-gri pantolon
PANTS_DARK = "#1E2632"
PANTS_LIGHT = "#3B4A5F"
SHOE_BASE = "#231F1D"
SHOE_SOLE = "#151211"

PLAN = "#7FE6FF"         # Camgöbeği plan görüşü
TATTOO_INK = "#273542"   # Özgün mimari dövme mürekkebi

_UID_COUNTER = 0


def _uid(prefix: str = "id") -> str:
    global _UID_COUNTER
    _UID_COUNTER += 1
    return f"{prefix}{_UID_COUNTER}"


# İfade tablosu: (kaş_iç_y, kaş_dış_y, üst_kapak, alt_kapak, ağız_türü, ekstra)
IFADE = {
    "odak":    (3.2, -0.4, 0.36, 0.16, "calm", ""),
    "kararli": (6.8, -3.2, 0.40, 0.22, "firm", "frown"),
    "yas":     (-8.0, 4.2, 0.46, 0.14, "sad", "tear"),
    "korku":   (-7.8, -7.2, 0.04, 0.04, "tense_open", "sweat"),
    "sefkat":  (-3.5, 1.5, 0.32, 0.18, "soft_smile", ""),
    "plan":    (2.8, -1.2, 0.32, 0.14, "calm", "plan"),
    "ofke":    (9.0, -4.8, 0.38, 0.24, "firm", "frown"),
    "neutral": (0.0, 0.0, 0.22, 0.08, "calm", ""),
}


def _render_eye(
    cx: float,
    cy: float,
    rx: float,
    ry: float,
    lu: float,
    ll: float,
    look: float,
    plan: bool = False,
    side: bool = False,
) -> str:
    """Sinematik 2D göz (v3): hafif ağır kapaklı (hooded), delici buz-mavisi/gri-yeşil (#7EB6BE),
    belirgin koyu limbal halka (#2F5059), üst kapak gölgesi ve tek keskin yansıma.
    """
    cid = _uid("eye")
    if side:
        shape = (
            f"M{cx - rx * 0.85:.1f},{cy + ry * 0.12:.1f} "
            f"Q{cx - rx * 0.05:.1f},{cy - ry * 1.10:.1f} {cx + rx * 0.95:.1f},{cy - ry * 0.10:.1f} "
            f"Q{cx + rx * 0.10:.1f},{cy + ry * 0.90:.1f} {cx - rx * 0.85:.1f},{cy + ry * 0.12:.1f} Z"
        )
    else:
        shape = (
            f"M{cx - rx:.1f},{cy + ry * 0.14:.1f} "
            f"Q{cx - rx * 0.28:.1f},{cy - ry * 1.12:.1f} {cx + rx * 0.34:.1f},{cy - ry * 0.92:.1f} "
            f"Q{cx + rx * 0.82:.1f},{cy - ry * 0.42:.1f} {cx + rx:.1f},{cy + ry * 0.06:.1f} "
            f"Q{cx + rx * 0.26:.1f},{cy + ry * 0.92:.1f} {cx - rx * 0.34:.1f},{cy + ry * 0.86:.1f} "
            f"Q{cx - rx * 0.78:.1f},{cy + ry * 0.56:.1f} {cx - rx:.1f},{cy + ry * 0.14:.1f} Z"
        )

    ix = cx + look * rx * 0.34
    iy = cy + ry * 0.05
    ir = ry * 0.80 if not side else ry * 0.74
    pr = ir * 0.43

    # Hafif ağır üst kapak (hooded)
    uy = cy - ry * 1.02 + lu * (ry * 1.72)
    ly = cy + ry * 0.92 - ll * (ry * 1.20)

    out = [
        f'<defs><clipPath id="{cid}"><path d="{shape}"/></clipPath></defs>',
        # Sklera (hafif soğuk-nötr beyaz, sinematik gerçekçilik)
        f'<path d="{shape}" fill="#EAE8E2"/>',
        f'<g clip-path="url(#{cid})">',
        # İris: belirgin koyu limbal halka + buz-mavisi/gri-yeşil + alt parlak hilal
        f'<circle cx="{ix:.1f}" cy="{iy:.1f}" r="{ir:.1f}" fill="{IRIS_DARK}"/>',
        f'<circle cx="{ix:.1f}" cy="{iy:.1f}" r="{ir * 0.80:.1f}" fill="{PLAN if plan else IRIS_BASE}"/>',
        f'<ellipse cx="{ix:.1f}" cy="{iy + ir * 0.36:.1f}" rx="{ir * 0.56:.1f}" ry="{ir * 0.28:.1f}" fill="{PLAN if plan else IRIS_LIGHT}" opacity="0.82"/>',
        # Göz bebeği
        f'<circle cx="{ix:.1f}" cy="{iy:.1f}" r="{pr:.1f}" fill="#101519"/>',
        # Plan görüşü ince camgöbeği halka yansıması
        (
            f'<circle cx="{ix:.1f}" cy="{iy:.1f}" r="{ir * 0.66:.1f}" fill="none" stroke="#E4FBFF" stroke-width="1.05" opacity="0.92"/>'
            f'<circle cx="{ix:.1f}" cy="{iy:.1f}" r="{ir * 0.94:.1f}" fill="none" stroke="{PLAN}" stroke-width="0.95" opacity="0.80"/>'
            if plan else ""
        ),
        # Üst kapak döküm gölgesi (sklera ve irisin üst 1/3'ünü keskin gölgeler — delici bakış)
        f'<rect x="{cx - rx - 4:.1f}" y="{cy - ry - 4:.1f}" width="{rx * 2 + 8:.1f}" height="{(uy - (cy - ry - 4)) + ry * 0.54:.1f}" fill="#3D4C56" opacity="0.34"/>',
        # Tek keskin yansıma (catchlight)
        f'<circle cx="{ix - ir * 0.32:.1f}" cy="{iy - ir * 0.22:.1f}" r="{max(1.25, ir * 0.23):.1f}" fill="#FFFFFF" opacity="0.96"/>',
        # Üst göz kapağı ten parçası (gölgeli)
        f'<rect x="{cx - rx - 6:.1f}" y="{cy - ry * 2.2:.1f}" width="{rx * 2 + 12:.1f}" height="{uy - (cy - ry * 2.2):.1f}" fill="{SKIN_SHADOW}" opacity="0.88"/>',
        # Alt göz kapağı ten parçası
        f'<rect x="{cx - rx - 6:.1f}" y="{ly:.1f}" width="{rx * 2 + 12:.1f}" height="{ry * 2.2:.1f}" fill="{SKIN_BASE}"/>',
        # Keskin üst kirpik hattı
        f'<path d="M{cx - rx - 2:.1f},{uy + 1.0:.1f} Q{cx:.1f},{uy - 2.3:.1f} {cx + rx + 2:.1f},{uy + 0.5:.1f}" fill="none" stroke="{INK}" stroke-width="2.5" stroke-linecap="round"/>',
        '</g>',
        # Göz dış çerçevesi (üst keskin, alt ince)
        f'<path d="M{cx - rx:.1f},{cy + ry * 0.14:.1f} Q{cx - rx * 0.24:.1f},{min(uy - 1.1, cy - ry * 0.85):.1f} {cx + rx:.1f},{cy + ry * 0.06:.1f}" fill="none" stroke="{INK}" stroke-width="2.1" stroke-linecap="round"/>',
        f'<path d="M{cx - rx * 0.80:.1f},{cy + ry * 0.34:.1f} Q{cx:.1f},{min(ly + 0.8, cy + ry * 0.90):.1f} {cx + rx * 0.80:.1f},{cy + ry * 0.28:.1f}" fill="none" stroke="{INK_SOFT}" stroke-width="1.05" opacity="0.68" stroke-linecap="round"/>',
        # Ağır kapak kıvrımı (hooded crease — üst kirpik hattına yakın ve net)
        f'<path d="M{cx - rx * 0.95:.1f},{cy - ry * 0.72:.1f} Q{cx:.1f},{cy - ry * 1.32:.1f} {cx + rx * 0.96:.1f},{cy - ry * 0.65:.1f}" fill="none" stroke="{SKIN_DEEP}" stroke-width="1.4" opacity="0.78" stroke-linecap="round"/>',
        # Alt orbital hat (sakin, derin bakış)
        f'<path d="M{cx - rx * 0.66:.1f},{cy + ry * 1.24:.1f} Q{cx:.1f},{cy + ry * 1.54:.1f} {cx + rx * 0.64:.1f},{cy + ry * 1.16:.1f}" fill="none" stroke="{SKIN_SHADOW}" stroke-width="1.05" opacity="0.52" stroke-linecap="round"/>',
    ]
    return "".join(out)


def _render_brow(
    x_in: float,
    y_in: float,
    x_out: float,
    y_out: float,
    arch_y: float = -1.2,
    thick: float = 6.0,
) -> str:
    """Alçak, düz, belirgin koyu erkek kaşı (güçlü kaş kemiği duygusu)."""
    mx = x_in * 0.38 + x_out * 0.62
    my = (y_in + y_out) * 0.5 + arch_y
    t_in = thick * 0.56
    t_mid = thick * 0.54
    t_out = thick * 0.24
    d = (
        f"M{x_in:.1f},{y_in - t_in:.1f} "
        f"Q{mx:.1f},{my - t_mid:.1f} {x_out:.1f},{y_out - t_out:.1f} "
        f"L{x_out:.1f},{y_out + t_out:.1f} "
        f"Q{mx:.1f},{my + t_mid * 0.72:.1f} {x_in:.1f},{y_in + t_in * 0.85:.1f} Z"
    )
    return (
        f'<path d="{d}" fill="{BROW_COL}"/>'
        f'<path d="M{x_in:.1f},{y_in - t_in * 0.55:.1f} Q{mx:.1f},{my - t_mid * 0.55:.1f} {x_out:.1f},{y_out:.1f}" '
        f'fill="none" stroke="#473C35" stroke-width="0.95" opacity="0.40"/>'
    )


def _render_mouth(mx: float, my: float, mw: float, kind: str, view: str) -> str:
    """Sinematik 2D ağız (v3): sakin, olgun, doğal üst/alt dudak hacmi ve köşe gölgesi."""
    if view == "side":
        if kind == "tense_open":
            return (
                f'<path d="M{mx + 2:.1f},{my - 3.5:.1f} Q{mx - 10:.1f},{my + 1:.1f} {mx + 2:.1f},{my + 7:.1f}" '
                f'fill="#4C2621" stroke="{INK}" stroke-width="1.5"/>'
            )
        dy = -2.2 if kind == "soft_smile" else (2.6 if kind == "sad" else 0.0)
        return (
            f'<path d="M{mx + 2.5:.1f},{my - 5.5:.1f} Q{mx - 5.5:.1f},{my - 4.2:.1f} {mx - 13:.1f},{my - 0.5:.1f} L{mx + 2.5:.1f},{my:.1f} Z" fill="{LIP_TOP}" opacity="0.78"/>'
            f'<path d="M{mx + 2.0:.1f},{my + 0.5:.1f} Q{mx - 6.0:.1f},{my + 6.5:.1f} {mx - 12.0:.1f},{my + 1.0:.1f} Z" fill="{LIP_BOT}" opacity="0.72"/>'
            f'<path d="M{mx + 2.5:.1f},{my:.1f} Q{mx - 6:.1f},{my + 1.1 + dy * 0.4:.1f} {mx - 13.5:.1f},{my + dy:.1f}" '
            f'fill="none" stroke="{INK}" stroke-width="1.8" stroke-linecap="round"/>'
            f'<path d="M{mx - 2:.1f},{my + 8.5:.1f} Q{mx - 7.5:.1f},{my + 10.0:.1f} {mx - 11.5:.1f},{my + 7.2:.1f}" fill="none" stroke="{SKIN_DEEP}" stroke-width="1.5" opacity="0.62" stroke-linecap="round"/>'
        )

    asym = 0.0 if view == "front" else 0.10
    lx = mx - mw * (1.0 - asym)
    rx = mx + mw * (1.0 + asym)

    if kind == "tense_open":
        return (
            f'<path d="M{lx + 2.5:.1f},{my + 1:.1f} Q{mx:.1f},{my - 5.5:.1f} {rx - 2.5:.1f},{my + 1:.1f} '
            f'Q{mx:.1f},{my + 9.5:.1f} {lx + 2.5:.1f},{my + 1:.1f} Z" fill="#4B2520" stroke="{INK}" stroke-width="1.5"/>'
            f'<path d="M{lx + 6:.1f},{my - 0.6:.1f} Q{mx:.1f},{my - 2.6:.1f} {rx - 6:.1f},{my - 0.6:.1f}" fill="none" stroke="#EAE4DA" stroke-width="2.2" stroke-linecap="round"/>'
            f'<path d="M{mx - mw * 0.46:.1f},{my + 11.5:.1f} Q{mx:.1f},{my + 13.2:.1f} {mx + mw * 0.46:.1f},{my + 11.0:.1f}" fill="none" stroke="{SKIN_DEEP}" stroke-width="1.6" opacity="0.60" stroke-linecap="round"/>'
        )

    c_l, c_r, mid_dip = -0.3, -0.4, 1.4
    if kind == "soft_smile":
        c_l, c_r, mid_dip = -2.8, -3.4, 2.4
    elif kind == "sad":
        c_l, c_r, mid_dip = 3.5, 3.3, -1.6
    elif kind == "firm":
        c_l, c_r, mid_dip = 1.0, 0.8, 0.3

    # Üst dudak: belirgin Cupid's bow ve sıcak gölge düzlemi
    upper_lip = (
        f"M{lx:.1f},{my + c_l:.1f} "
        f"Q{mx - mw * 0.34:.1f},{my - 6.4:.1f} {mx - mw * 0.14:.1f},{my - 5.4:.1f} "
        f"Q{mx:.1f},{my - 3.9:.1f} {mx + mw * 0.14:.1f},{my - 5.4:.1f} "
        f"Q{mx + mw * 0.34:.1f},{my - 6.4:.1f} {rx:.1f},{my + c_r:.1f} "
        f"Q{mx:.1f},{my + mid_dip:.1f} {lx:.1f},{my + c_l:.1f} Z"
    )
    # Alt dudak: sakin, doğal dolgunluk
    lower_lip = (
        f"M{lx + mw * 0.10:.1f},{my + c_l * 0.6 + 0.6:.1f} "
        f"Q{mx:.1f},{my + 9.2 + mid_dip * 0.45:.1f} {rx - mw * 0.10:.1f},{my + c_r * 0.6 + 0.6:.1f} "
        f"Q{mx:.1f},{my + mid_dip + 0.5:.1f} {lx + mw * 0.10:.1f},{my + c_l * 0.6 + 0.6:.1f} Z"
    )
    # Dudak ayrım çizgisi: doğal hafif M-dalgalı, köşelerde incelen
    seam = (
        f"M{lx:.1f},{my + c_l:.1f} "
        f"Q{mx - mw * 0.35:.1f},{my + mid_dip * 0.45:.1f} {mx:.1f},{my + mid_dip + 0.6:.1f} "
        f"Q{mx + mw * 0.35:.1f},{my + mid_dip * 0.45:.1f} {rx:.1f},{my + c_r:.1f}"
    )
    return (
        f'<path d="{upper_lip}" fill="{LIP_TOP}" opacity="0.82"/>'
        f'<path d="{lower_lip}" fill="{LIP_BOT}" opacity="0.74"/>'
        # Üst dudak üst sınır yumuşak ışık (Cupid's bow highlight)
        f'<path d="M{mx - mw * 0.24:.1f},{my - 5.6:.1f} Q{mx:.1f},{my - 4.2:.1f} {mx + mw * 0.24:.1f},{my - 5.6:.1f}" fill="none" stroke="{SKIN_LIGHT}" stroke-width="1.25" opacity="0.62" stroke-linecap="round"/>'
        # Alt dudak yumuşak ışık
        f'<path d="M{mx - mw * 0.34:.1f},{my + 4.8:.1f} Q{mx:.1f},{my + 6.2:.1f} {mx + mw * 0.30:.1f},{my + 4.6:.1f}" fill="none" stroke="#F6D8C9" stroke-width="1.8" opacity="0.56" stroke-linecap="round"/>'
        # Dudak ayrım çizgisi
        f'<path d="{seam}" fill="none" stroke="{INK}" stroke-width="1.85" stroke-linecap="round"/>'
        # Ağız köşesi gölgeleri (olgun ifade)
        f'<ellipse cx="{lx - 0.8:.1f}" cy="{my + c_l + 0.5:.1f}" rx="2.2" ry="1.3" fill="{SKIN_DEEP}" opacity="0.48"/>'
        f'<ellipse cx="{rx + 0.8:.1f}" cy="{my + c_r + 0.5:.1f}" rx="2.2" ry="1.3" fill="{SKIN_DEEP}" opacity="0.48"/>'
        # Alt dudak altı belirgin gölge çukuru (mentolabial sulcus)
        f'<path d="M{mx - mw * 0.48:.1f},{my + 10.6:.1f} Q{mx:.1f},{my + 12.8:.1f} {mx + mw * 0.48:.1f},{my + 10.4:.1f}" '
        f'fill="none" stroke="{SKIN_DEEP}" stroke-width="1.85" opacity="0.66" stroke-linecap="round"/>'
    )


def _buzzcut_stipple(view: str) -> str:
    """1-2 numara kazınmış saç (buzzcut) için çok ince, doğal kısa tüy dokusu.
    Asla beyaz nokta/kepek değil; koyu kahve-kömür tonunda mikro stipple.
    """
    rng = random.Random(42 if view == "front" else (77 if view == "3q" else 99))
    pts: list[str] = []
    count = 135
    for _ in range(count):
        if view == "front":
            x = rng.uniform(-61, 61)
            y = rng.uniform(-94, -56)
            if (x / 63) ** 2 + ((y + 22) / 76) ** 2 > 0.94:
                continue
        elif view == "3q":
            x = rng.uniform(-59, 64)
            y = rng.uniform(-94, -52)
            if ((x - 4) / 65) ** 2 + ((y + 22) / 76) ** 2 > 0.94:
                continue
        else:
            x = rng.uniform(-62, 58)
            y = rng.uniform(-94, -42)
            if ((x + 2) / 64) ** 2 + ((y + 20) / 77) ** 2 > 0.94:
                continue
        op = rng.uniform(0.18, 0.38)
        r = rng.uniform(0.55, 0.85)
        pts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.2f}" fill="#1C1714" opacity="{op:.2f}"/>')
    return "".join(pts)


def _stubble_stipple(view: str) -> str:
    """1-2 günlük temiz kısa sakal dokusu (çene ve yanak altlarında mikro noktacıklar)."""
    rng = random.Random(301 if view == "front" else (302 if view == "3q" else 303))
    pts: list[str] = []
    for _ in range(95):
        if view == "front":
            x = rng.uniform(-52, 52)
            y = rng.uniform(46, 100)
        elif view == "3q":
            x = rng.uniform(-44, 62)
            y = rng.uniform(48, 100)
        else:
            x = rng.uniform(10, 66)
            y = rng.uniform(48, 100)
        # Dudak bölgesini boş bırak
        if view == "front" and abs(x) < 22 and 49 < y < 68:
            continue
        if view == "3q" and 6 < x < 48 and 49 < y < 68:
            continue
        if view == "side" and x > 50 and 49 < y < 68:
            continue
        op = rng.uniform(0.14, 0.28)
        pts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="0.62" fill="{STUBBLE}" opacity="{op:.2f}"/>')
    return "".join(pts)


def kafa_yetiskin(
    view: str = "3q",
    ifade: str = "odak",
    look: float = 0.25,
    boyun: bool = False,
) -> str:
    """Yetişkin Michael kafası (v3 — Stil B + A hibrit, sinematik 2D).
    Merkez (0, 0), yükseklik ~202 (y: -96 .. +105). view: 'front' | '3q' | 'side'.
    """
    bi, bo, lu, ll, mk, extra = IFADE.get(ifade, IFADE["odak"])
    is_plan = extra == "plan"

    o: list[str] = []
    defs: list[str] = []

    cid_face = _uid("fclip")
    cid_buzz = _uid("bclip")
    gid_skin = _uid("sking")
    gid_buzz = _uid("buzzg")
    gid_sidefade = _uid("sfade")
    gid_cheek = _uid("chekg")
    gid_stub = _uid("stubg")
    gid_plan = _uid("plang")

    defs.append(
        f'<linearGradient id="{gid_skin}" x1="0.14" y1="0.08" x2="0.88" y2="0.92">'
        f'<stop offset="0%" stop-color="{SKIN_LIGHT}"/>'
        f'<stop offset="46%" stop-color="{SKIN_BASE}"/>'
        f'<stop offset="100%" stop-color="{SKIN_MID}"/>'
        f'</linearGradient>'
    )
    defs.append(
        f'<linearGradient id="{gid_cheek}" x1="0.0" y1="0.5" x2="1.0" y2="0.35">'
        f'<stop offset="0%" stop-color="{SKIN_SHADOW}" stop-opacity="0.46"/>'
        f'<stop offset="65%" stop-color="{SKIN_SHADOW}" stop-opacity="0.22"/>'
        f'<stop offset="100%" stop-color="{SKIN_SHADOW}" stop-opacity="0.0"/>'
        f'</linearGradient>'
    )
    # 1-2 numara kazınmış buzzcut: kafa derisine sıfır oturan, aşağı doğru yumuşak fade gradyanı
    defs.append(
        f'<linearGradient id="{gid_buzz}" x1="0.35" y1="0.0" x2="0.55" y2="1.0">'
        f'<stop offset="0%" stop-color="{BUZZ_TOP}" stop-opacity="0.92"/>'
        f'<stop offset="55%" stop-color="{BUZZ_MID}" stop-opacity="0.84"/>'
        f'<stop offset="86%" stop-color="{BUZZ_MID}" stop-opacity="0.46"/>'
        f'<stop offset="100%" stop-color="{SKIN_BASE}" stop-opacity="0.0"/>'
        f'</linearGradient>'
    )
    defs.append(
        f'<linearGradient id="{gid_sidefade}" x1="0.5" y1="0.0" x2="0.5" y2="1.0">'
        f'<stop offset="0%" stop-color="{BUZZ_MID}" stop-opacity="0.62"/>'
        f'<stop offset="65%" stop-color="{BUZZ_MID}" stop-opacity="0.22"/>'
        f'<stop offset="100%" stop-color="{SKIN_BASE}" stop-opacity="0.0"/>'
        f'</linearGradient>'
    )
    defs.append(
        f'<linearGradient id="{gid_stub}" x1="0.5" y1="0.0" x2="0.5" y2="1.0">'
        f'<stop offset="0%" stop-color="{STUBBLE}" stop-opacity="0.0"/>'
        f'<stop offset="38%" stop-color="{STUBBLE}" stop-opacity="0.16"/>'
        f'<stop offset="100%" stop-color="{STUBBLE}" stop-opacity="0.28"/>'
        f'</linearGradient>'
    )
    if is_plan:
        defs.append(
            f'<linearGradient id="{gid_plan}" x1="1.0" y1="0.42" x2="0.48" y2="0.60">'
            f'<stop offset="0%" stop-color="{PLAN}" stop-opacity="0.28"/>'
            f'<stop offset="45%" stop-color="{PLAN}" stop-opacity="0.06"/>'
            f'<stop offset="100%" stop-color="{PLAN}" stop-opacity="0.0"/>'
            f'</linearGradient>'
        )

    # Opsiyonel anatomik boyun
    if boyun:
        if view == "front":
            nk_d = "M-34,74 L-38,130 Q0,140 38,130 L34,74 Z"
            sh_d = "M-34,74 Q0,118 34,74 L36,108 Q0,124 -36,108 Z"
            scm = (
                f'<path d="M-32,88 Q-20,114 -8,132 M32,88 Q20,114 8,132" fill="none" stroke="{SKIN_SHADOW}" stroke-width="1.9" opacity="0.56" stroke-linecap="round"/>'
                f'<path d="M-10,128 Q0,133 10,128" fill="none" stroke="{SKIN_DEEP}" stroke-width="1.5" opacity="0.56" stroke-linecap="round"/>'
            )
        elif view == "3q":
            nk_d = "M-40,62 L-43,130 Q-6,142 25,128 L24,82 Z"
            sh_d = "M-40,62 Q0,118 25,80 L25,112 Q-6,126 -42,102 Z"
            scm = (
                f'<path d="M-36,84 Q-20,112 -4,132 M14,94 Q10,114 12,129" fill="none" stroke="{SKIN_SHADOW}" stroke-width="1.9" opacity="0.56" stroke-linecap="round"/>'
                f'<path d="M-10,114 Q0,120 8,114" fill="none" stroke="{SKIN_DEEP}" stroke-width="1.4" opacity="0.46" stroke-linecap="round"/>'
            )
        else:
            nk_d = "M-45,62 L-53,132 Q-12,142 18,130 L14,86 Z"
            sh_d = "M-45,62 Q-10,112 16,84 L15,110 Q-12,124 -47,102 Z"
            scm = f'<path d="M-35,82 Q-18,110 -4,130" fill="none" stroke="{SKIN_SHADOW}" stroke-width="2.0" opacity="0.56" stroke-linecap="round"/>'
        o.append(
            f'<path d="{nk_d}" fill="{SKIN_MID}"/>'
            f'<path d="{sh_d}" fill="{SKIN_DEEP}" opacity="0.62"/>'
            f'{scm}'
            f'<path d="{nk_d}" fill="none" stroke="{INK}" stroke-width="2.1" stroke-linejoin="round"/>'
        )

    # ── 1. Kafatası + Keskin Köşeli Yüz Silueti (kask kabarması yok; kafa kendi temiz konturunda) ──
    if view == "front":
        face_d = (
            "M-63,-22 C-64,-68 -38,-94 0,-95 C38,-94 64,-68 63,-22 "
            "L62,14 C61,32 58,50 53,64 L36,87 C23,100 12,105 0,105 "
            "C-12,105 -23,100 -36,87 L-53,64 C-58,50 -61,32 -62,14 Z"
        )
        ears = [(-64, 6, -1), (64, 6, 1)]
        eye_specs = [(-27.0, -5.0, 15.2, 8.0, False), (27.0, -5.0, 15.2, 8.0, False)]
        lk = 0.0 if look == 0.25 else look
        mx, my, mw = 0.0, 56.5, 22.0
    elif view == "3q":
        face_d = (
            "M-62,-20 C-64,-69 -34,-94 8,-95 C45,-94 67,-70 67,-26 "
            "C69,-12 68,2 70,16 C71,29 66,46 60,59 "
            "L49,85 C41,98 31,104 20,105 C6,106 -11,100 -27,87 "
            "L-47,64 C-55,50 -60,30 -61,10 Z"
        )
        ears = [(-61, 8, -1)]
        eye_specs = [(-5.0, -5.0, 15.2, 8.0, False), (42.5, -5.0, 12.2, 7.6, False)]
        lk = look
        mx, my, mw = 25.5, 56.5, 19.2
    else:  # side (profil, sağa bakar)
        face_d = (
            "M-65,-18 C-68,-70 -35,-95 6,-95 C41,-95 62,-74 63,-38 "
            "L64,-16 C65,-10 67,-6 70,0 L82,27 C84,33 80,37 72,37 "
            "L67,37 L70,48 C72,52 69,55 65,56 L69,63 C71,68 67,73 62,75 "
            "L65,89 C66,99 56,105 40,105 L16,104 C-4,103 -22,93 -34,75 "
            "C-51,53 -61,24 -65,-18 Z"
        )
        ears = [(-10, 10, -1)]
        eye_specs = [(47.0, -5.5, 11.6, 7.4, True)]
        lk = max(0.35, look)
        mx, my, mw = 63.5, 57.0, 12.2

    defs.append(f'<clipPath id="{cid_face}"><path d="{face_d}"/></clipPath>')
    o.insert(0, f'<defs>{"".join(defs)}</defs>')

    # ── 2. Kulaklar ──
    for ex, ey, side_sgn in ears:
        ew = 11.2 if view != "side" else 13.2
        eh = 20.5
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
            f'fill="none" stroke="{SKIN_DEEP}" stroke-width="1.3" opacity="0.7" stroke-linecap="round"/>'
        )

    # ── 3. Yüz Tabanı + Sinematik Kemik Düzlemleri + 1-2 Numara Buzzcut (kafatası içinde, sıfır oturan) ──
    o.append(f'<path d="{face_d}" fill="url(#{gid_skin})"/>')
    inner: list[str] = []

    if view == "front":
        inner.append(
            # Sağ yarı ana sinematik gölge
            f'<path d="M26,-98 C45,-56 44,-14 38,24 C34,54 22,82 6,110 L90,110 L90,-98 Z" fill="{SKIN_SHADOW}" opacity="0.34"/>'
            # Güçlü kaş kemiği altı (brow ridge) & göz çukuru gölgesi
            f'<path d="M-49,-20 Q-26,-28 -5,-16 Q-8,4 -27,6 Q-47,4 -49,-20 Z" fill="{SKIN_SHADOW}" opacity="0.54"/>'
            f'<path d="M49,-20 Q26,-28 5,-16 Q8,4 27,6 Q47,4 49,-20 Z" fill="{SKIN_SHADOW}" opacity="0.58"/>'
            f'<path d="M-45,-19 Q-26,-25 -8,-16 L-10,-8 Q-26,-16 -43,-10 Z" fill="{SKIN_DEEP}" opacity="0.34"/>'
            f'<path d="M45,-19 Q26,-25 8,-16 L10,-8 Q26,-16 43,-10 Z" fill="{SKIN_DEEP}" opacity="0.38"/>'
            # Elmacık altı düzlem oyukları (keskin kemik yapısı)
            f'<path d="M-62,16 L-41,30 L-36,64 L-60,50 Z" fill="{SKIN_SHADOW}" opacity="0.38"/>'
            f'<path d="M62,16 L41,30 L36,64 L60,50 Z" fill="{SKIN_SHADOW}" opacity="0.50"/>'
            # Alın + elmacık üstü + dar temiz burun sırtı ışığı
            f'<path d="M-34,-50 Q0,-56 28,-46 Q18,-29 -14,-31 Z" fill="{SKIN_LIGHT}" opacity="0.48"/>'
            f'<path d="M-3.2,-14 L2.6,-14 L4.2,27 L-4.2,27 Z" fill="{SKIN_LIGHT}" opacity="0.62"/>'
            f'<path d="M3.5,-14 L11,27 L2,35 L-8,33 L-4,27 Z" fill="{SKIN_SHADOW}" opacity="0.38"/>'
            # Çene altı gölgesi
            f'<path d="M-44,86 Q0,104 44,86 L44,112 L-44,112 Z" fill="{SKIN_DEEP}" opacity="0.38"/>'
            # 1-2 günlük temiz sakal gölgesi (stubble)
            f'<path d="M-58,36 C-44,48 -24,42 0,43 C24,42 44,48 58,36 L58,110 L-58,110 Z" fill="url(#{gid_stub})"/>'
            + _stubble_stipple("front")
            # Sol kenar sıcak rim ışığı
            + f'<path d="M-61,-16 L-59,16 C-57,44 -47,68 -28,90" fill="none" stroke="#FFF4E8" stroke-width="2.8" opacity="0.34" stroke-linecap="round"/>'
        )
        # 1-2 numara buzzcut (kafatasına sıfır oturan, stipple kesinlikle saç içine kırpılı)
        buzz_top = (
            "M-66,-10 L-66,-100 L66,-100 L66,-10 "
            "L60,-12 C58,-30 53,-44 43,-51 C33,-57 22,-61 0,-61 "
            "C-22,-61 -33,-57 -43,-51 C-53,-44 -58,-30 -60,-12 Z"
        )
        buzz_fade = (
            "M-66,10 L-59,10 C-57,-14 -53,-32 -43,-42 C-33,-51 -20,-56 0,-56 "
            "C20,-56 33,-51 43,-42 C53,-32 57,-14 59,10 L66,10 L66,-100 L-66,-100 Z"
        )
        inner.append(
            f'<defs><clipPath id="{cid_buzz}"><path d="{buzz_top}"/></clipPath></defs>'
            f'<path d="{buzz_fade}" fill="url(#{gid_sidefade})"/>'
            f'<path d="{buzz_top}" fill="url(#{gid_buzz})"/>'
            f'<g clip-path="url(#{cid_buzz})">{_buzzcut_stipple("front")}</g>'
            f'<ellipse cx="-4" cy="-83" rx="28" ry="6.5" fill="{BUZZ_LIGHT}" opacity="0.32"/>'
        )

    elif view == "3q":
        inner.append(
            # Uzak taraf ana gölge
            f'<path d="M40,-98 C56,-58 58,-18 56,20 C54,52 44,82 26,110 L90,110 L90,-98 Z" fill="{SKIN_SHADOW}" opacity="0.44"/>'
            # Yakın elmacık altı yumuşak düzlem gölgesi (sinematik geçiş)
            f'<path d="M-60,15 C-40,22 -20,34 -16,54 C-24,74 -39,86 -53,70 Z" fill="url(#{gid_cheek})"/>'
            # Güçlü kaş kemiği altı & göz çukuru gölgesi
            f'<path d="M-26,-20 Q-5,-28 16,-16 Q12,5 -6,6 Q-24,4 -26,-20 Z" fill="{SKIN_SHADOW}" opacity="0.54"/>'
            f'<path d="M27,-20 Q44,-27 60,-15 Q56,4 41,5 Q29,3 27,-20 Z" fill="{SKIN_SHADOW}" opacity="0.58"/>'
            f'<path d="M-22,-18 Q-5,-24 12,-16 L10,-8 Q-5,-16 -20,-10 Z" fill="{SKIN_DEEP}" opacity="0.35"/>'
            f'<path d="M29,-18 Q44,-24 57,-15 L55,-8 Q44,-15 31,-10 Z" fill="{SKIN_DEEP}" opacity="0.38"/>'
            # Alın + yakın elmacık üstü ışık düzlemi
            f'<path d="M-32,-50 Q4,-58 34,-48 Q22,-30 -14,-32 Z" fill="{SKIN_LIGHT}" opacity="0.50"/>'
            f'<path d="M-42,9 Q-22,1 -6,11 Q-14,26 -36,23 Z" fill="{SKIN_LIGHT}" opacity="0.46"/>'
            # Çene altı gölgesi
            f'<path d="M-40,84 Q18,104 54,82 L54,112 L-40,112 Z" fill="{SKIN_DEEP}" opacity="0.40"/>'
            # 1-2 günlük temiz sakal gölgesi
            f'<path d="M-54,42 C-30,50 4,44 26,44 C46,44 60,48 68,38 L68,110 L-54,110 Z" fill="url(#{gid_stub})"/>'
            + _stubble_stipple("3q")
            # Sol kenar sıcak rim ışığı
            + f'<path d="M-60,-14 L-58,18 C-54,48 -41,74 -18,96" fill="none" stroke="#FFF4E8" stroke-width="2.8" opacity="0.34" stroke-linecap="round"/>'
        )
        # 1-2 numara buzzcut (kafatasına sıfır oturan, stipple kesinlikle saç içine kırpılı)
        buzz_top = (
            "M-66,12 L-66,-100 L72,-100 L72,-28 "
            "L66,-30 C63,-46 54,-56 38,-60 C18,-65 -8,-63 -28,-53 "
            "C-40,-46 -46,-32 -49,-10 L-53,12 Z"
        )
        buzz_fade = (
            "M-66,22 L-51,22 L-47,-6 C-44,-26 -38,-40 -26,-48 C-6,-58 18,-60 38,-55 "
            "C53,-51 62,-42 66,-26 L72,-26 L72,-100 L-66,-100 Z"
        )
        inner.append(
            f'<defs><clipPath id="{cid_buzz}"><path d="{buzz_top}"/></clipPath></defs>'
            f'<path d="{buzz_fade}" fill="url(#{gid_sidefade})"/>'
            f'<path d="{buzz_top}" fill="url(#{gid_buzz})"/>'
            f'<g clip-path="url(#{cid_buzz})">{_buzzcut_stipple("3q")}</g>'
            f'<ellipse cx="4" cy="-83" rx="30" ry="6.5" fill="{BUZZ_LIGHT}" opacity="0.32"/>'
        )

    else:  # side
        inner.append(
            f'<path d="M-68,14 C-46,24 -12,34 12,56 C24,74 36,96 58,106 L-68,110 Z" fill="{SKIN_SHADOW}" opacity="0.36"/>'
            f'<path d="M30,-20 Q49,-27 64,-15 Q60,5 45,5 Q33,3 30,-20 Z" fill="{SKIN_SHADOW}" opacity="0.54"/>'
            f'<path d="M47,-50 Q60,-40 62,-18 L52,-16 Q48,-36 41,-46 Z" fill="{SKIN_LIGHT}" opacity="0.48"/>'
            f'<path d="M8,46 C28,50 54,48 72,44 L72,110 L8,110 Z" fill="url(#{gid_stub})"/>'
            + _stubble_stipple("side")
            + f'<path d="M62,-36 L64,-16 L80,27" fill="none" stroke="#FFF4E8" stroke-width="2.2" opacity="0.36" stroke-linecap="round"/>'
        )
        buzz_top = (
            "M-70,22 L-70,-100 L68,-100 L68,-40 "
            "L60,-42 C54,-56 38,-63 18,-63 C-4,-63 -18,-52 -22,-30 "
            "L-24,-4 L-32,16 L-48,24 Z"
        )
        buzz_fade = (
            "M-70,32 L-46,32 L-29,20 L-21,-2 L-19,-26 C-15,-46 -2,-58 18,-58 "
            "C38,-58 53,-50 60,-36 L68,-36 L68,-100 L-70,-100 Z"
        )
        inner.append(
            f'<defs><clipPath id="{cid_buzz}"><path d="{buzz_top}"/></clipPath></defs>'
            f'<path d="{buzz_fade}" fill="url(#{gid_sidefade})"/>'
            f'<path d="{buzz_top}" fill="url(#{gid_buzz})"/>'
            f'<g clip-path="url(#{cid_buzz})">{_buzzcut_stipple("side")}</g>'
            f'<ellipse cx="2" cy="-83" rx="28" ry="6.5" fill="{BUZZ_LIGHT}" opacity="0.32"/>'
        )

    # Plan görüşü: yüzün sağ kenarına vuran keskin camgöbeği rim/yansıma (ten tonunu bozmadan)
    if is_plan:
        inner.append(f'<rect x="-80" y="-98" width="180" height="215" fill="url(#{gid_plan})"/>')
        if view == "front":
            inner.append(
                f'<path d="M61,-12 L60,24 C56,48 46,70 29,90" fill="none" stroke="{PLAN}" stroke-width="2.5" opacity="0.78" stroke-linecap="round"/>'
            )
        elif view == "3q":
            inner.append(
                f'<path d="M66,-20 L68,18 C65,46 53,74 33,98" fill="none" stroke="{PLAN}" stroke-width="2.7" opacity="0.82" stroke-linecap="round"/>'
            )
        else:
            inner.append(
                f'<path d="M63,-36 L64,-16 L81,27 M67,38 L69,65 L64,91" fill="none" stroke="{PLAN}" stroke-width="2.3" opacity="0.78" stroke-linecap="round"/>'
            )

    o.append(f'<g clip-path="url(#{cid_face})">{"".join(inner)}</g>')

    # ── 4. Kafatası & Yüz Ana Dış Konturu (zarif 2.1px — kask çizgisi yok, tek doğal siluet!) ──
    o.append(f'<path d="{face_d}" fill="none" stroke="{INK}" stroke-width="2.1" stroke-linejoin="round"/>')

    # ── 5. Gözler + Alçak Düz Kaşlar ──
    for idx, (ex, ey, erx, ery, is_side) in enumerate(eye_specs):
        o.append(_render_eye(ex, ey, erx, ery, lu, ll, lk, plan=is_plan, side=is_side))
        if view == "front":
            sgn = -1 if ex < 0 else 1
            x_in = ex - sgn * (erx * 0.94)
            x_out = ex + sgn * (erx * 1.16)
            y_in = ey - ery * 1.78 + bi * 0.72
            y_out = ey - ery * 1.84 + bo * 0.72
            o.append(_render_brow(x_in, y_in, x_out, y_out, arch_y=-1.2, thick=6.0))
        elif view == "3q":
            if idx == 0:
                x_in, x_out = ex + erx * 0.96, ex - erx * 1.18
            else:
                x_in, x_out = ex - erx * 0.94, ex + erx * 1.12
            y_in = ey - ery * 1.78 + bi * 0.72
            y_out = ey - ery * 1.84 + bo * 0.72
            o.append(_render_brow(x_in, y_in, x_out, y_out, arch_y=-1.2, thick=5.9 if idx == 0 else 5.2))
        else:
            x_in, x_out = ex + erx * 1.14, ex - erx * 1.24
            y_in = ey - ery * 1.78 + bi * 0.72
            y_out = ey - ery * 1.86 + bo * 0.72
            o.append(_render_brow(x_in, y_in, x_out, y_out, arch_y=-1.1, thick=5.7))

    gx = 0.0 if view == "front" else (20.0 if view == "3q" else 58.0)
    if view != "side":
        op_g = 0.78 if extra == "frown" else 0.44
        o.append(
            f'<path d="M{gx - 3.0:.1f},-22.5 L{gx - 2.2:.1f},-14.0 M{gx + 3.0:.1f},-22.5 L{gx + 2.2:.1f},-14.0" '
            f'fill="none" stroke="{SKIN_DEEP}" stroke-width="1.25" opacity="{op_g}" stroke-linecap="round"/>'
        )

    # ── 6. Burun (temiz, keskin, düz köprü) ──
    if view == "front":
        o.append(
            f'<path d="M-4.2,-12 L-5.8,24" fill="none" stroke="{SKIN_SHADOW}" stroke-width="1.2" opacity="0.58" stroke-linecap="round"/>'
            f'<path d="M-10.2,27.5 Q-6.0,33.2 0,33.8 Q6.0,33.2 10.2,27.5" fill="none" stroke="{INK_SOFT}" stroke-width="1.75" stroke-linecap="round"/>'
            f'<path d="M-12.2,26.0 Q-13.2,30.2 -8.2,31.2 M12.2,26.0 Q13.2,30.2 8.2,31.2" fill="none" stroke="{INK_SOFT}" stroke-width="1.2" opacity="0.72" stroke-linecap="round"/>'
            f'<ellipse cx="-5.2" cy="31.0" rx="2.5" ry="1.15" fill="{SKIN_DEEP}" opacity="0.74"/>'
            f'<ellipse cx="5.2" cy="31.0" rx="2.5" ry="1.15" fill="{SKIN_DEEP}" opacity="0.74"/>'
        )
    elif view == "3q":
        o.append(
            f'<path d="M22.2,-12 L34.6,24.5 Q31.2,34.5 19.8,33.5 L16.8,27.5 Z" fill="{SKIN_SHADOW}" opacity="0.40"/>'
            f'<path d="M21.8,-13 L33.8,24.2 Q35.2,30.0 28.8,33.2 Q23.6,34.6 19.0,32.2" '
            f'fill="none" stroke="{INK}" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="M16.2,27.2 Q14.8,31.2 19.4,32.5" fill="none" stroke="{INK_SOFT}" stroke-width="1.3" opacity="0.80" stroke-linecap="round"/>'
            f'<ellipse cx="24.0" cy="31.8" rx="2.6" ry="1.15" fill="{SKIN_DEEP}" opacity="0.80"/>'
            f'<path d="M20.6,-9 L30.4,22.2" fill="none" stroke="#FFF4E8" stroke-width="1.7" opacity="0.48" stroke-linecap="round"/>'
        )
    else:
        o.append(
            f'<path d="M62.5,28.0 Q60.5,33.2 67.0,34.0" fill="none" stroke="{INK_SOFT}" stroke-width="1.35" opacity="0.85" stroke-linecap="round"/>'
            f'<ellipse cx="69.0" cy="32.5" rx="2.9" ry="1.2" fill="{SKIN_DEEP}" opacity="0.78"/>'
        )

    # ── 7. Philtrum + Sakin Dolgun Ağız + İnce Kemik Hatları ──
    if view == "front":
        o.append(
            f'<path d="M-2.2,37 L-2.6,47.5 M2.2,37 L2.6,47.5" fill="none" stroke="{SKIN_SHADOW}" stroke-width="1.0" opacity="0.40" stroke-linecap="round"/>'
        )
    elif view == "3q":
        o.append(
            f'<path d="M25.2,37 L25.8,47.5" fill="none" stroke="{SKIN_SHADOW}" stroke-width="1.1" opacity="0.38" stroke-linecap="round"/>'
        )
    o.append(_render_mouth(mx, my, mw, mk, view))

    if view == "front":
        o.append(
            f'<path d="M-46,24 Q-42,42 -34,55" fill="none" stroke="{SKIN_DEEP}" stroke-width="1.1" opacity="0.34" stroke-linecap="round"/>'
            f'<path d="M46,24 Q42,42 34,55" fill="none" stroke="{SKIN_DEEP}" stroke-width="1.1" opacity="0.40" stroke-linecap="round"/>'
            f'<path d="M-9,93 Q0,97 9,93" fill="none" stroke="{SKIN_DEEP}" stroke-width="1.2" opacity="0.44" stroke-linecap="round"/>'
        )
    elif view == "3q":
        o.append(
            f'<path d="M-39,24 Q-33,44 -21,58" fill="none" stroke="{SKIN_DEEP}" stroke-width="1.15" opacity="0.34" stroke-linecap="round"/>'
            f'<path d="M12,94 Q21,97 30,93" fill="none" stroke="{SKIN_DEEP}" stroke-width="1.2" opacity="0.44" stroke-linecap="round"/>'
        )

    # ── 8. İfade Ekstraları (Kurul notu: Plan HUD kaşla çakışmaz, temiz yerleşim) ──
    if extra == "tear":
        ex, ey = eye_specs[-1][0], eye_specs[-1][1]
        o.append(
            f'<path d="M{ex - 1:.1f},{ey + 8:.1f} Q{ex + 3:.1f},{ey + 24:.1f} {ex + 1:.1f},{ey + 38:.1f}" '
            f'fill="none" stroke="#C6E9FF" stroke-width="2.5" opacity="0.84" stroke-linecap="round"/>'
            f'<ellipse cx="{ex + 1:.1f}" cy="{ey + 42:.1f}" rx="2.7" ry="4.3" fill="#CBEBFF" stroke="#5A8FB0" stroke-width="1.1"/>'
            f'<circle cx="{ex:.1f}" cy="{ey + 40.5:.1f}" r="1.0" fill="#FFFFFF"/>'
        )
    elif extra == "sweat":
        sx = -46 if view != "side" else 16
        o.append(
            f'<path d="M{sx},-30 Q{sx - 4},-18 {sx},-14 Q{sx + 4},-18 {sx},-30 Z" fill="#D5EEFF" stroke="#6F9AB8" stroke-width="1.0" opacity="0.85"/>'
        )
    elif is_plan:
        # Kurul düzeltmesi: HUD çizgileri kaşların üstünden/altından geçer, sol kaşa kesinlikle taşmaz
        if view == "3q":
            o.append(
                f'<g opacity="0.74">'
                f'<path d="M14,-31 L74,-31 M-26,18 L74,18" fill="none" stroke="{PLAN}" stroke-width="0.9" stroke-dasharray="5,4"/>'
                f'<path d="M62,-36 L74,-36 L74,-24 M-30,12 L-30,22 L-20,22" fill="none" stroke="{PLAN}" stroke-width="1.25"/>'
                f'<circle cx="43" cy="-5" r="15" fill="none" stroke="{PLAN}" stroke-width="0.85" opacity="0.68"/>'
                f'</g>'
            )
        elif view == "front":
            o.append(
                f'<g opacity="0.72">'
                f'<path d="M-46,-31 L46,-31 M-44,18 L44,18" fill="none" stroke="{PLAN}" stroke-width="0.9" stroke-dasharray="5,4"/>'
                f'<circle cx="27" cy="-5" r="15" fill="none" stroke="{PLAN}" stroke-width="0.85" opacity="0.65"/>'
                f'</g>'
            )

    return f'<g transform="scale(0.92, 1.01)">{"".join(o)}</g>'


def dovme_onkol_yetiskin(w: float = 48.0, h: float = 140.0, plan: bool = False) -> str:
    """Özgün gotik kemer + telkari + turna kanadı önkol dövmesi (A-Sırt v1 kalitesinde, R1 uyumlu)."""
    t = TATTOO_INK
    t_soft = "#3B4C5D"
    o: list[str] = []

    # 1. Yumuşak mürekkep gölge tabanı (düz çizgi değil, organik kol sarımı)
    o.append(
        f'<path d="M{-w * 0.40:.1f},{h * 0.14:.1f} Q0,{h * 0.04:.1f} {w * 0.40:.1f},{h * 0.14:.1f} '
        f'Q{w * 0.44:.1f},{h * 0.50:.1f} {w * 0.34:.1f},{h * 0.88:.1f} '
        f'Q0,{h * 0.94:.1f} {-w * 0.34:.1f},{h * 0.88:.1f} '
        f'Q{-w * 0.44:.1f},{h * 0.50:.1f} {-w * 0.40:.1f},{h * 0.14:.1f} Z" '
        f'fill="{t}" opacity="0.14"/>'
    )
    # 2. Üst gotik kemer & gül pencere madalyonu (kıvrımlı mimari)
    o.append(
        f'<path d="M{-w * 0.34:.1f},{h * 0.86:.1f} C{-w * 0.36:.1f},{h * 0.56:.1f} {-w * 0.34:.1f},{h * 0.36:.1f} 0,{h * 0.16:.1f} '
        f'C{w * 0.34:.1f},{h * 0.36:.1f} {w * 0.36:.1f},{h * 0.56:.1f} {w * 0.34:.1f},{h * 0.86:.1f}" '
        f'fill="none" stroke="{t}" stroke-width="1.8" opacity="0.86"/>'
        f'<path d="M{-w * 0.24:.1f},{h * 0.86:.1f} C{-w * 0.26:.1f},{h * 0.58:.1f} {-w * 0.24:.1f},{h * 0.40:.1f} 0,{h * 0.24:.1f} '
        f'C{w * 0.24:.1f},{h * 0.40:.1f} {w * 0.26:.1f},{h * 0.58:.1f} {w * 0.24:.1f},{h * 0.86:.1f}" '
        f'fill="none" stroke="{t}" stroke-width="1.2" opacity="0.76"/>'
        f'<circle cx="0" cy="{h * 0.36:.1f}" r="{w * 0.18:.1f}" fill="none" stroke="{t}" stroke-width="1.2" opacity="0.80"/>'
        f'<circle cx="0" cy="{h * 0.36:.1f}" r="{w * 0.09:.1f}" fill="none" stroke="{t_soft}" stroke-width="0.9" opacity="0.72"/>'
    )
    # 3. Kıvrımlı organik telkari / filigree sarmaşıkları (A-Sırt v1 dili)
    o.append(
        f'<path d="M{-w * 0.38:.1f},{h * 0.28:.1f} Q{-w * 0.18:.1f},{h * 0.20:.1f} 0,{h * 0.28:.1f} '
        f'Q{w * 0.18:.1f},{h * 0.20:.1f} {w * 0.38:.1f},{h * 0.28:.1f}" '
        f'fill="none" stroke="{t}" stroke-width="1.25" opacity="0.78"/>'
        f'<path d="M{-w * 0.36:.1f},{h * 0.52:.1f} C{-w * 0.18:.1f},{h * 0.44:.1f} {-w * 0.14:.1f},{h * 0.62:.1f} 0,{h * 0.54:.1f} '
        f'C{w * 0.14:.1f},{h * 0.62:.1f} {w * 0.18:.1f},{h * 0.44:.1f} {w * 0.36:.1f},{h * 0.52:.1f}" '
        f'fill="none" stroke="{t}" stroke-width="1.15" opacity="0.76"/>'
        f'<path d="M{-w * 0.32:.1f},{h * 0.72:.1f} Q{-w * 0.14:.1f},{h * 0.64:.1f} 0,{h * 0.74:.1f} '
        f'Q{w * 0.14:.1f},{h * 0.64:.1f} {w * 0.32:.1f},{h * 0.72:.1f}" '
        f'fill="none" stroke="{t}" stroke-width="1.15" opacity="0.74"/>'
    )
    # 4. İkiz origami turna kanadı motifi (üst önkol)
    o.append(
        f'<path d="M{-w * 0.40:.1f},{h * 0.18:.1f} Q{-w * 0.18:.1f},{h * 0.08:.1f} 0,{h * 0.15:.1f} '
        f'Q{w * 0.18:.1f},{h * 0.08:.1f} {w * 0.40:.1f},{h * 0.18:.1f} '
        f'Q{w * 0.16:.1f},{h * 0.24:.1f} 0,{h * 0.22:.1f} Q{-w * 0.16:.1f},{h * 0.24:.1f} {-w * 0.40:.1f},{h * 0.18:.1f} Z" '
        f'fill="{t}" opacity="0.20"/>'
        f'<path d="M{-w * 0.40:.1f},{h * 0.18:.1f} Q{-w * 0.18:.1f},{h * 0.08:.1f} 0,{h * 0.15:.1f} '
        f'Q{w * 0.18:.1f},{h * 0.08:.1f} {w * 0.40:.1f},{h * 0.18:.1f}" '
        f'fill="none" stroke="{t}" stroke-width="1.45" opacity="0.86"/>'
    )
    # 5. İnce gotik taş kemer nişleri & gölge taraması (düz kaba X değil)
    for k in range(3):
        yy = h * (0.46 + k * 0.13)
        o.append(
            f'<path d="M{-w * 0.32:.1f},{yy + h * 0.09:.1f} Q{-w * 0.24:.1f},{yy:.1f} {-w * 0.16:.1f},{yy + h * 0.09:.1f}" '
            f'fill="none" stroke="{t_soft}" stroke-width="0.95" opacity="0.70"/>'
            f'<path d="M{w * 0.16:.1f},{yy + h * 0.09:.1f} Q{w * 0.24:.1f},{yy:.1f} {w * 0.32:.1f},{yy + h * 0.09:.1f}" '
            f'fill="none" stroke="{t_soft}" stroke-width="0.95" opacity="0.70"/>'
        )
    # 6. Gizli kaçış rotası (mürekkeple bütünleşik, plan=True iken camgöbeği parlar)
    route = (
        f"M{-w * 0.14:.1f},{h * 0.86:.1f} V{h * 0.66:.1f} H{w * 0.12:.1f} "
        f"V{h * 0.48:.1f} H{-w * 0.08:.1f} V{h * 0.36:.1f} L0,{h * 0.22:.1f}"
    )
    if plan:
        o.append(
            f'<path d="{route}" fill="none" stroke="{PLAN}" stroke-width="4.6" opacity="0.28" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="{route}" fill="none" stroke="{PLAN}" stroke-width="2.0" opacity="0.96" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="{route}" fill="none" stroke="#E8FCFF" stroke-width="0.9" opacity="0.95" stroke-linecap="round" stroke-linejoin="round"/>'
        )
        for nx, ny in [(-w * 0.14, h * 0.66), (w * 0.12, h * 0.66), (w * 0.12, h * 0.48), (0.0, h * 0.36), (0.0, h * 0.22)]:
            o.append(
                f'<circle cx="{nx:.1f}" cy="{ny:.1f}" r="2.8" fill="{PLAN}" opacity="0.88"/>'
                f'<circle cx="{nx:.1f}" cy="{ny:.1f}" r="1.2" fill="#FFFFFF"/>'
            )
    else:
        o.append(
            f'<path d="{route}" fill="none" stroke="{t}" stroke-width="1.05" opacity="0.48" stroke-linecap="round" stroke-linejoin="round"/>'
        )

    return "".join(o)


def _render_hand(cx: float, cy: float, scale: float, skin: str, skin_sh: str, mirror: bool = False) -> str:
    """Anatomik sinematik 2D el (gevşek doğal duruş)."""
    sx = -scale if mirror else scale
    return (
        f'<g transform="translate({cx:.1f},{cy:.1f}) scale({sx:.3f},{scale:.3f})">'
        f'<path d="M-11,-4 C-13,8 -13,18 -10,25 L8,24 C12,16 13,6 10,-4 Z" fill="{skin}" stroke="{INK}" stroke-width="2.1" stroke-linejoin="round"/>'
        f'<path d="M-10,2 C-18,8 -19,18 -14,26 C-11,28 -7,25 -8,19 L-7,12" fill="{skin}" stroke="{INK}" stroke-width="2.0" stroke-linecap="round" stroke-linejoin="round"/>'
        f'<path d="M-8,22 L-9,40 C-9,44 -4,44 -4,40 L-3,24" fill="{skin}" stroke="{INK}" stroke-width="1.9" stroke-linejoin="round"/>'
        f'<path d="M-3,23 L-3,43 C-3,47 2,47 2,43 L2,24" fill="{skin}" stroke="{INK}" stroke-width="1.9" stroke-linejoin="round"/>'
        f'<path d="M2,23 L3,41 C3,45 8,45 8,41 L7,23" fill="{skin}" stroke="{INK}" stroke-width="1.9" stroke-linejoin="round"/>'
        f'<path d="M7,21 L9,35 C9,38 13,38 13,35 L11,19" fill="{skin_sh}" stroke="{INK}" stroke-width="1.8" stroke-linejoin="round"/>'
        f'<path d="M-4,4 L-3,17 M2,4 L3,17" fill="none" stroke="{skin_sh}" stroke-width="1.2" opacity="0.65" stroke-linecap="round"/>'
        f'</g>'
    )


def figur_yetiskin(ifade: str = "odak", plan: bool = False, numara_goster: bool = True) -> str:
    """Tam boy yetişkin Michael Scofield (v3 — Stil B + A hibrit, sinematik 2D).
    Ayak tabanı y=0, toplam boy ~562 (y: -562 .. 0). Doğal 3/4 duruş, sağa bakar.
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
        f'<stop offset="42%" stop-color="{SHIRT_BASE}"/>'
        f'<stop offset="100%" stop-color="{SHIRT_DARK}"/>'
        f'</linearGradient>'
        f'<linearGradient id="{gid_pt}" x1="0.15" y1="0.0" x2="0.85" y2="1.0">'
        f'<stop offset="0%" stop-color="{PANTS_LIGHT}"/>'
        f'<stop offset="45%" stop-color="{PANTS_BASE}"/>'
        f'<stop offset="100%" stop-color="{PANTS_DARK}"/>'
        f'</linearGradient>'
        f'</defs>'
    )

    o.append('<ellipse cx="4" cy="4" rx="88" ry="13" fill="#000000" opacity="0.34"/>')

    # ── 1. Bacaklar & Ayakkabılar ──
    leg_back = (
        "M-42,-256 L-46,-132 C-47,-118 -44,-92 -42,-24 L-8,-24 "
        "C-6,-90 -6,-120 -8,-140 L-2,-256 Z"
    )
    o.append(
        f'<path d="{leg_back}" fill="{PANTS_DARK}" stroke="{INK}" stroke-width="2.2" stroke-linejoin="round"/>'
        f'<path d="M-38,-144 Q-24,-138 -12,-146 M-34,-36 Q-22,-32 -12,-38" fill="none" stroke="#131922" stroke-width="1.5" opacity="0.7" stroke-linecap="round"/>'
        f'<path d="M-44,-26 L-8,-26 C4,-22 14,-14 14,-2 L-46,-2 Z" fill="{SHOE_BASE}" stroke="{INK}" stroke-width="2.2" stroke-linejoin="round"/>'
        f'<path d="M-46,-6 L14,-6 L14,-1 L-46,-1 Z" fill="{SHOE_SOLE}"/>'
    )

    leg_front = (
        "M-2,-256 L4,-136 C6,-118 14,-82 22,-20 L58,-20 "
        "C54,-82 50,-118 48,-138 L46,-256 Z"
    )
    o.append(
        f'<path d="{leg_front}" fill="url(#{gid_pt})" stroke="{INK}" stroke-width="2.2" stroke-linejoin="round"/>'
        f'<path d="M6,-244 L14,-138 L26,-28" fill="none" stroke="#51647E" stroke-width="3.2" opacity="0.28" stroke-linecap="round"/>'
        f'<path d="M8,-142 Q26,-134 44,-146 M14,-128 Q28,-122 42,-130 M24,-34 Q40,-28 54,-36" fill="none" stroke="#161D28" stroke-width="1.5" opacity="0.65" stroke-linecap="round"/>'
        f'<path d="M20,-22 L58,-22 C74,-18 86,-10 86,2 L18,2 Z" fill="{SHOE_BASE}" stroke="{INK}" stroke-width="2.2" stroke-linejoin="round"/>'
        f'<path d="M18,-4 L86,-4 L86,2 L18,2 Z" fill="{SHOE_SOLE}"/>'
        f'<path d="M56,-17 Q72,-14 80,-7" fill="none" stroke="#4D4540" stroke-width="1.5" opacity="0.55" stroke-linecap="round"/>'
    )

    # ── 2. Uzak Kol (Sol kol, sıvalı + dövmeli) ──
    ua_l = "M-60,-432 C-74,-422 -84,-386 -86,-344 L-54,-340 C-50,-376 -46,-404 -46,-426 Z"
    fa_l = "M-82,-342 C-86,-310 -82,-276 -76,-242 L-56,-244 C-54,-278 -54,-310 -56,-342 Z"
    o.append(
        f'<defs><clipPath id="{cid_fa_l}"><path d="{fa_l}"/></clipPath></defs>'
        f'<path d="{fa_l}" fill="{SKIN_MID}"/>'
        f'<g clip-path="url(#{cid_fa_l})">'
        f'<g transform="translate(-70,-344) rotate(4)">{dovme_onkol_yetiskin(34, 102, plan=plan)}</g>'
        f'<path d="M-84,-342 L-82,-242 L-72,-242 L-74,-342 Z" fill="{SKIN_SHADOW}" opacity="0.34"/>'
        f'</g>'
        f'<path d="{fa_l}" fill="none" stroke="{INK}" stroke-width="2.1" stroke-linejoin="round"/>'
        + _render_hand(-66, -242, 0.84, SKIN_MID, SKIN_SHADOW, mirror=True)
        + f'<path d="{ua_l}" fill="{SHIRT_DARK}" stroke="{INK}" stroke-width="2.15" stroke-linejoin="round"/>'
        f'<path d="M-89,-354 Q-70,-348 -51,-352 L-52,-336 Q-70,-332 -88,-338 Z" fill="{SHIRT_MID}" stroke="{INK}" stroke-width="2.0" stroke-linejoin="round"/>'
        f'<path d="M-86,-345 Q-70,-341 -54,-344" fill="none" stroke="{SHIRT_DARK}" stroke-width="1.3" opacity="0.7"/>'
    )

    # ── 3. Gövde (Atletik V-taper Fox River Gömleği) ──
    torso_d = (
        "M-64,-428 C-66,-388 -58,-340 -52,-304 L-56,-250 "
        "C-20,-240 24,-240 56,-252 L52,-304 "
        "C58,-342 68,-388 66,-426 C52,-438 36,-444 24,-452 "
        "L-22,-452 C-34,-444 -50,-438 -64,-428 Z"
    )
    o.append(
        f'<defs><clipPath id="{tid_torso}"><path d="{torso_d}"/></clipPath></defs>'
        f'<path d="{torso_d}" fill="url(#{gid_sh})"/>'
    )

    torso_inner = [
        f'<path d="M26,-454 C44,-410 42,-340 34,-244 L76,-244 L76,-454 Z" fill="{SHIRT_DARK}" opacity="0.48"/>',
        f'<path d="M-56,-422 C-42,-388 -40,-336 -44,-262" fill="none" stroke="#A6C4E0" stroke-width="5.5" opacity="0.24" stroke-linecap="round"/>',
        f'<path d="M4,-406 L8,-244 M15,-406 L19,-244" fill="none" stroke="{SHIRT_DARK}" stroke-width="1.4" opacity="0.72"/>',
        "".join(
            f'<circle cx="{11.5 + k * 0.9:.1f}" cy="{-386 + k * 34:.1f}" r="2.7" fill="#E6E3DA" stroke="{INK}" stroke-width="1.1"/>'
            for k in range(4)
        ),
        f'<path d="M-44,-386 L-8,-386 L-8,-352 Q-26,-346 -44,-352 Z" fill="{SHIRT_MID}" opacity="0.35" stroke="{INK}" stroke-width="1.6" stroke-linejoin="round"/>',
        f'<path d="M-44,-378 L-8,-378" fill="none" stroke="{SHIRT_DARK}" stroke-width="1.2" opacity="0.7"/>',
        f'<path d="M-54,-394 Q-36,-386 -26,-392 M-48,-286 Q-22,-278 -4,-288 M24,-294 Q40,-288 52,-298 M32,-384 Q48,-378 60,-390" '
        f'fill="none" stroke="{SHIRT_DARK}" stroke-width="1.4" opacity="0.62" stroke-linecap="round"/>',
        f'<path d="M-56,-254 Q0,-244 56,-256" fill="none" stroke="{SHIRT_DARK}" stroke-width="3.0" opacity="0.5"/>',
    ]
    if numara_goster:
        torso_inner.append(
            '<text x="-45" y="-393" font-family="Consolas, DejaVu Sans Mono, monospace" font-weight="bold" '
            'font-size="13.5" letter-spacing="0.6" fill="#EEF2F6" opacity="0.95">94941</text>'
        )

    o.append(
        f'<g clip-path="url(#{tid_torso})">{"".join(torso_inner)}</g>'
        f'<path d="{torso_d}" fill="none" stroke="{INK}" stroke-width="2.2" stroke-linejoin="round"/>'
    )

    # ── 4. R4: Anatomik Boyun + Köprücük + Yaka Birleşimi ──
    o.append(
        f'<path d="M-27,-450 Q4,-463 29,-450 L26,-436 Q4,-444 -24,-436 Z" fill="{SHIRT_DARK}" stroke="{INK}" stroke-width="2.0" stroke-linejoin="round"/>'
    )
    o.append(
        f'<path d="M-20,-442 Q4,-416 25,-442 L10,-404 L-4,-404 Z" fill="{UNDER_BASE}" stroke="{INK}" stroke-width="1.7" stroke-linejoin="round"/>'
        f'<path d="M-16,-438 Q4,-422 22,-438" fill="none" stroke="{UNDER_SH}" stroke-width="2.2" opacity="0.8"/>'
    )
    neck_d = (
        "M-20,-482 L-22,-450 C-23,-442 -15,-434 -6,-426 "
        "Q4,-420 14,-426 C22,-434 24,-442 22,-450 L18,-478 Z"
    )
    o.append(
        f'<path d="{neck_d}" fill="{SKIN_BASE}"/>'
        f'<path d="M2,-480 L19,-478 L22,-448 C20,-438 14,-430 6,-425 L4,-448 Z" fill="{SKIN_SHADOW}" opacity="0.48"/>'
        f'<path d="M-20,-482 L19,-478 L21,-456 Q2,-444 -21,-458 Z" fill="{SKIN_DEEP}" opacity="0.64"/>'
        f'<path d="M-18,-468 Q-8,-448 2,-430 M16,-464 Q12,-448 8,-432" fill="none" stroke="{SKIN_SHADOW}" stroke-width="1.7" opacity="0.60" stroke-linecap="round"/>'
        f'<path d="M-4,-432 Q4,-427 11,-432" fill="none" stroke="{SKIN_DEEP}" stroke-width="1.5" opacity="0.58" stroke-linecap="round"/>'
        f'<path d="M-20,-482 L-22,-450 M18,-478 L22,-450" fill="none" stroke="{INK}" stroke-width="2.1" stroke-linecap="round"/>'
    )
    o.append(
        f'<path d="M-27,-450 L-20,-442 L-4,-408 L-29,-420 Z" fill="{SHIRT_LIGHT}" stroke="{INK}" stroke-width="2.0" stroke-linejoin="round"/>'
        f'<path d="M29,-450 L23,-442 L14,-408 L35,-422 Z" fill="{SHIRT_BASE}" stroke="{INK}" stroke-width="2.0" stroke-linejoin="round"/>'
        f'<path d="M-28,-418 L-4,-406 M14,-406 L34,-420" fill="none" stroke="{SHIRT_DARK}" stroke-width="2.2" opacity="0.55" stroke-linecap="round"/>'
    )

    # ── 5. Baş ──
    o.append(
        f'<g transform="translate(8,-508) scale(0.50)">'
        f'{kafa_yetiskin(view="3q", ifade=ifade, look=0.25, boyun=False)}'
        f'</g>'
    )

    # ── 6. Yakın Kol (Sağ kol — akıcı omuz dikişi) ──
    ua_r = "M64,-426 C78,-414 88,-382 88,-338 L52,-334 C50,-366 50,-390 50,-404 C56,-414 60,-422 64,-426 Z"
    fa_r = "M84,-336 C88,-302 82,-268 74,-236 L54,-238 C52,-272 52,-306 54,-336 Z"
    o.append(
        f'<defs><clipPath id="{cid_fa_r}"><path d="{fa_r}"/></clipPath></defs>'
        f'<path d="{fa_r}" fill="{SKIN_BASE}"/>'
        f'<g clip-path="url(#{cid_fa_r})">'
        f'<g transform="translate(68,-338) rotate(5)">{dovme_onkol_yetiskin(38, 104, plan=plan)}</g>'
        f'<path d="M74,-336 L88,-336 L84,-236 L68,-236 Z" fill="{SKIN_SHADOW}" opacity="0.34"/>'
        f'<path d="M56,-330 L56,-244" fill="none" stroke="#FFF4E8" stroke-width="2.6" opacity="0.28" stroke-linecap="round"/>'
        f'</g>'
        f'<path d="{fa_r}" fill="none" stroke="{INK}" stroke-width="2.15" stroke-linejoin="round"/>'
        + _render_hand(64, -236, 0.88, SKIN_BASE, SKIN_SHADOW, mirror=False)
        + f'<path d="{ua_r}" fill="url(#{gid_sh})"/>'
        f'<path d="M64,-426 C78,-414 88,-382 88,-338 L52,-334 C50,-366 50,-390 50,-404" fill="none" stroke="{INK}" stroke-width="2.2" stroke-linejoin="round" stroke-linecap="round"/>'
        f'<path d="M50,-404 C54,-416 58,-424 64,-426" fill="none" stroke="{SHIRT_DARK}" stroke-width="1.5" opacity="0.72" stroke-linecap="round"/>'
        f'<path d="M68,-414 C78,-388 80,-364 78,-348" fill="none" stroke="{SHIRT_DARK}" stroke-width="1.5" opacity="0.55" stroke-linecap="round"/>'
        f'<path d="M50,-348 Q70,-342 91,-348 L89,-330 Q70,-325 51,-332 Z" fill="{SHIRT_LIGHT}" stroke="{INK}" stroke-width="2.05" stroke-linejoin="round"/>'
        f'<path d="M53,-339 Q70,-334 87,-339" fill="none" stroke="{SHIRT_DARK}" stroke-width="1.4" opacity="0.68"/>'
    )

    return "".join(o)


def _portre_plan_omuz() -> str:
    """Alt sağ panel için yakın plan 3/4 omuz-portre (plan görüşü ışık efektli)."""
    gid_glow = _uid("pglow")
    return (
        f'<defs>'
        f'<radialGradient id="{gid_glow}" cx="0.68" cy="0.40" r="0.62">'
        f'<stop offset="0%" stop-color="{PLAN}" stop-opacity="0.28"/>'
        f'<stop offset="58%" stop-color="{PLAN}" stop-opacity="0.06"/>'
        f'<stop offset="100%" stop-color="{PLAN}" stop-opacity="0.0"/>'
        f'</radialGradient>'
        f'</defs>'
        f'<rect x="-215" y="-110" width="430" height="220" fill="url(#{gid_glow})"/>'
        f'<g opacity="0.30" stroke="{PLAN}" fill="none">'
        f'<path d="M-190,-70 H190 M-190,-15 H190 M-190,40 H190 M-110,-100 V100 M20,-100 V100 M125,-100 V100" stroke-width="0.7"/>'
        f'<path d="M85,-65 L130,-65 L130,-20 M-150,15 L-105,15 L-105,60" stroke-width="1.2"/>'
        f'<circle cx="115" cy="-35" r="24" stroke-width="0.8" stroke-dasharray="4,3"/>'
        f'</g>'
        f'<g transform="translate(18, 502) scale(1.04)">'
        f'{figur_yetiskin(ifade="plan", plan=True, numara_goster=True)}'
        f'</g>'
    )


def _onkol_detay(plan: bool = False) -> str:
    """Yakın önkol + özgün mimari/turna dövme detay kesiti."""
    cid = _uid("armd")
    arm_d = "M-32,-78 C-34,-26 -28,28 -22,74 L22,74 C28,28 34,-26 32,-78 Z"
    glow = (
        f'<ellipse cx="0" cy="0" rx="48" ry="86" fill="{PLAN}" opacity="0.14"/>'
        if plan else ""
    )
    return (
        f'{glow}'
        f'<defs><clipPath id="{cid}"><path d="{arm_d}"/></clipPath></defs>'
        f'<path d="{arm_d}" fill="{SKIN_BASE}"/>'
        f'<g clip-path="url(#{cid})">'
        f'<path d="M12,-80 L38,-80 L32,80 L8,80 Z" fill="{SKIN_SHADOW}" opacity="0.38"/>'
        f'<path d="M-24,-74 L-18,72" fill="none" stroke="#FFF4E8" stroke-width="4.0" opacity="0.26" stroke-linecap="round"/>'
        f'<g transform="translate(0,-76)">{dovme_onkol_yetiskin(54, 148, plan=plan)}</g>'
        f'</g>'
        f'<path d="{arm_d}" fill="none" stroke="{INK}" stroke-width="2.2" stroke-linejoin="round"/>'
        f'<path d="M-38,-92 Q0,-86 38,-92 L35,-72 Q0,-66 -35,-72 Z" fill="{SHIRT_LIGHT}" stroke="{INK}" stroke-width="2.1" stroke-linejoin="round"/>'
        f'<path d="M-34,-82 Q0,-77 34,-82" fill="none" stroke="{SHIRT_DARK}" stroke-width="1.5" opacity="0.65"/>'
    )


def build_model_card_svg() -> str:
    """1280x720 Yetişkin Michael Model Kartı v3 (ay_yetiskin_v3.png)."""
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
        '<clipPath id="clipPortre"><rect x="394" y="492" width="424" height="202" rx="10"/></clipPath>',
        '</defs>',
        f'<rect width="{W}" height="{H}" fill="url(#bgGrad)"/>',
    ]

    grid = [f"M{x},0 V{H}" for x in range(0, W + 1, 40)] + [f"M0,{y} H{W}" for y in range(0, H + 1, 40)]
    parts.append(f'<path d="{" ".join(grid)}" fill="none" stroke="{PLAN}" stroke-width="0.6" opacity="0.045"/>')

    parts.append(
        '<text x="28" y="34" font-family="Segoe UI, DejaVu Sans, sans-serif" font-weight="700" font-size="18" fill="#E8EEF5" letter-spacing="1.0">'
        'MICHAEL SCOFIELD · YETİŞKİN MODEL KARTI v3</text>'
        '<text x="518" y="33" font-family="Segoe UI, DejaVu Sans, sans-serif" font-size="12.5" fill="#7EB6BE">'
        'STİL B+A HİBRİT · BUZZCUT &amp; İMZA REVİZYONU</text>'
    )
    swatches = [
        (SKIN_BASE, "TEN"),
        (BUZZ_TOP, "SAÇ"),
        (IRIS_BASE, "GÖZ"),
        (SHIRT_BASE, "GÖMLEK"),
        (PLAN, "PLAN"),
    ]
    for i, (col, lbl) in enumerate(swatches):
        sx = 895 + i * 72
        parts.append(
            f'<rect x="{sx}" y="16" width="15" height="15" rx="3" fill="{col}" stroke="#44566B" stroke-width="1"/>'
            f'<text x="{sx + 20}" y="27.5" font-family="Segoe UI, DejaVu Sans, sans-serif" font-size="10" fill="#9BB0C5">{lbl}</text>'
        )

    # ── SOL PANEL: Tam Boy Figür ──
    parts.append(
        '<rect x="24" y="54" width="350" height="642" rx="12" fill="#171F2A" stroke="#2C3B4D" stroke-width="1.4"/>'
        '<ellipse cx="199" cy="360" rx="150" ry="275" fill="url(#spotL)"/>'
        '<path d="M44,122 H354 M44,376 H354 M44,648 H354" fill="none" stroke="#7FE6FF" stroke-width="0.7" opacity="0.14" stroke-dasharray="4,5"/>'
        f'<g transform="translate(196,648) scale(0.94)">{figur_yetiskin(ifade="odak", plan=False, numara_goster=True)}</g>'
        '<text x="199" y="680" text-anchor="middle" font-family="Segoe UI, DejaVu Sans, sans-serif" font-weight="600" font-size="13" fill="#C9D6E4">'
        'YETİŞKİN · FOX RIVER (94941)</text>'
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
            f'<g transform="translate({cx},158) scale(0.62)">{kafa_yetiskin(view=vw, ifade="odak", look=lk, boyun=True)}</g>'
            f'<text x="{cx}" y="264" text-anchor="middle" font-family="Segoe UI, DejaVu Sans, sans-serif" font-size="12" fill="#C4D3E2">{lbl}</text>'
        )

    # ── ORTA SAĞ PANEL: 6 İfade ──
    parts.append(
        '<rect x="392" y="288" width="864" height="190" rx="12" fill="#171F2A" stroke="#2C3B4D" stroke-width="1.4"/>'
        '<text x="410" y="310" font-family="Segoe UI, DejaVu Sans, sans-serif" font-weight="600" font-size="11.5" fill="#7F98B2" letter-spacing="1">'
        'ALTI İFADE (ODAK · KARARLI · YAS · KORKU · ŞEFKAT · PLAN GÖRÜŞÜ)</text>'
    )
    exps = [
        ("odak", "odak", "#C4D3E2"),
        ("kararli", "kararlı", "#C4D3E2"),
        ("yas", "yas", "#C4D3E2"),
        ("korku", "korku", "#C4D3E2"),
        ("sefkat", "şefkat", "#C4D3E2"),
        ("plan", "plan görüşü", PLAN),
    ]
    for idx, (ek, elbl, col) in enumerate(exps):
        cx = 468 + idx * 142
        parts.append(
            f'<g transform="translate({cx},386) scale(0.51)">{kafa_yetiskin(view="3q", ifade=ek, look=0.25, boyun=False)}</g>'
            f'<text x="{cx}" y="464" text-anchor="middle" font-family="Segoe UI, DejaVu Sans, sans-serif" font-weight="{"700" if ek=="plan" else "500"}" font-size="12" fill="{col}">{elbl}</text>'
        )

    # ── ALT SAĞ PANEL: Yakın Plan Omuz-Portre + Önkol Dövmesi ──
    parts.append(
        '<rect x="392" y="490" width="428" height="206" rx="12" fill="#131B25" stroke="#2E566B" stroke-width="1.5"/>'
        f'<g clip-path="url(#clipPortre)"><g transform="translate(606,596)">{_portre_plan_omuz()}</g></g>'
        '<rect x="402" y="498" width="236" height="22" rx="5" fill="#0E151E" opacity="0.82"/>'
        '<text x="410" y="513" font-family="Segoe UI, DejaVu Sans, sans-serif" font-weight="600" font-size="10.8" fill="#7FE6FF" letter-spacing="0.6">'
        'YAKIN PLAN OMUZ-PORTRE · PLAN GÖRÜŞÜ</text>'
    )

    parts.append(
        '<rect x="834" y="490" width="422" height="206" rx="12" fill="#171F2A" stroke="#2C3B4D" stroke-width="1.4"/>'
        '<text x="852" y="512" font-family="Segoe UI, DejaVu Sans, sans-serif" font-weight="600" font-size="11.5" fill="#7F98B2" letter-spacing="0.8">'
        'ÖZGÜN ÖNKOL DÖVMESİ (MİMARİ + TURNA)</text>'
        f'<g transform="translate(950,602) scale(0.84)">{_onkol_detay(plan=False)}</g>'
        '<text x="950" y="684" text-anchor="middle" font-family="Segoe UI, DejaVu Sans, sans-serif" font-size="11.5" fill="#C4D3E2">normal</text>'
        f'<g transform="translate(1140,602) scale(0.84)">{_onkol_detay(plan=True)}</g>'
        f'<text x="1140" y="684" text-anchor="middle" font-family="Segoe UI, DejaVu Sans, sans-serif" font-weight="600" font-size="11.5" fill="{PLAN}">plan ışıklandığında</text>'
    )

    parts.append('</svg>')
    return "".join(parts)


def build_r13_svg() -> str:
    """1280x720 R13 %200 Kırpma Kartı v3 (ay_yetiskin_r13_v3.png) — 5 yakın kontrol paneli
    (1: 3/4 odak yüz, 2: önden yüz, 3: plan görüşü yüz, 4: boyun-yaka-omuz, 5: özgün önkol dövmesi).
    """
    W, H = 1280, 720
    panels = [
        (20, 48, 610, 316, "1. 3/4 ODAK — YÜZ YAKIN (%200)", False),
        (650, 48, 610, 316, "2. ÖNDEN — YÜZ YAKIN (%200)", False),
        (20, 384, 610, 316, "3. PLAN GÖRÜŞÜ — YÜZ YAKIN (%200)", True),
        (650, 384, 300, 316, "4. BOYUN / YAKA / OMUZ", False),
        (960, 384, 300, 316, "5. ÖNKOL DÖVMESİ (%200)", True),
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
        'R13 · %200 YAKIN KONTROL KARTI — YETİŞKİN MICHAEL v3</text>'
        '<text x="1256" y="30" text-anchor="end" font-family="Segoe UI, DejaVu Sans, sans-serif" font-size="12" fill="#7EB6BE">'
        'R1 / R4 / R10 / R13 · BUZZCUT + GÖZ + DÖVME DOĞRULAMA</text>'
    )

    contents = [
        f'<g transform="translate(325,208) scale(1.26)">{kafa_yetiskin(view="3q", ifade="odak", look=0.25, boyun=True)}</g>',
        f'<g transform="translate(955,208) scale(1.26)">{kafa_yetiskin(view="front", ifade="odak", look=0.0, boyun=True)}</g>',
        f'<g transform="translate(325,544) scale(1.26)">{kafa_yetiskin(view="3q", ifade="plan", look=0.25, boyun=True)}</g>',
        # Panel 4: Boyun / Yaka / Omuz yakın
        f'<g transform="translate(796,1438) scale(1.80)">{figur_yetiskin(ifade="odak", plan=False, numara_goster=True)}</g>',
        # Panel 5: Özgün önkol dövmesi yakın plan (normal ve ışıklı yan yana)
        (
            f'<g transform="translate(1042,566) scale(1.32)">{_onkol_detay(plan=False)}</g>'
            f'<g transform="translate(1178,566) scale(1.32)">{_onkol_detay(plan=True)}</g>'
        ),
    ]

    for i, (px, py, pw, ph, title, is_p) in enumerate(panels):
        stroke = "#2E6A82" if is_p else "#2C3B4D"
        tcol = PLAN if is_p else "#9CB2C8"
        parts.append(
            f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="10" fill="#161E29" stroke="{stroke}" stroke-width="1.5"/>'
            f'<g clip-path="url(#pclip{i})">{contents[i]}</g>'
            f'<rect x="{px+10}" y="{py+10}" width="{min(pw - 20, len(title)*7.2 + 18):.0f}" height="24" rx="5" fill="#0F151D" opacity="0.86"/>'
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
    render_svg_to_png(build_model_card_svg(), OUT_DIR / "ay_yetiskin_v3.png")
    render_svg_to_png(build_r13_svg(), OUT_DIR / "ay_yetiskin_r13_v3.png")


if __name__ == "__main__":
    main()
