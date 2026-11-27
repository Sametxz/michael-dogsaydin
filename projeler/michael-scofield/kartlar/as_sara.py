"""A-S (Sara Tancredi Üretici) — v2 Sinematik 2D (Stil B + A hibrit).
Onaylı Yetişkin Michael v3 (ay_yetiskin_v3.png) ile birebir aynı sinematik 2D stil dili:
  - Ana dış kontur: 2.0–2.1px (#1A1513), iç anatomi hatları: 1.1–1.4px (#4A3128 / #7F523D)
  - Göz: zarif doğal badem form, canlı zeytin-yeşil / ela iris (#6E9674), koyu limbal halka (#273D2C),
    zarif kavisli üst kirpik hattı, üst kapak gölgesi ve tek temiz yansıma (anime/çizgi film YASAK - R10).
  - R1: Oyuncunun (Sarah Wayne Callies) gerçek portre yüzü kopyalanmaz; karakter arketipi çizilir.
  - R3: Dövme YOK.
  - R4: Zarif anatomik boyun + köprücük kemiği ipucu, scrub + doktor önlüğü yakasına sağlam oturum.

v2 Revizyonu (Kullanıcı + Kurul geri bildirimi):
  - Daha zarif, sıcak, feminen oval-kalp yüz oranları, ince burun, doğal gül-şeftali dolgun dudaklar.
  - ~%10 daha etkileyici badem gözler, daha yumuşak zarif kavisli kaşlar.
  - Uçları incelen (tapered), doğal dalgalı, yüzü çerçeveleyen yan perçemli kestane-kızıl saç + altın-bakır ışık.
  - Alt panelde revir anahtarını (INF-04) tutan ince parmaklı, anatomik eklemli zarif el.

İzole modül — import sırasında yan etkisiz fonksiyonlar:
  - kafa_sara(view="3q", ifade="odak", look=0.25, boyun=False)
  - figur_sara(ifade="odak")
"""
from __future__ import annotations

import io
from pathlib import Path
import resvg_py
from PIL import Image

OUT_DIR = Path(__file__).resolve().parent

# ── Sinematik 2D Renk Paleti (v2 — Stil B + A hibrit, A-Y v3 uyumlu) ──
INK = "#1A1513"          # Sıcak koyu mürekkep (dış hat: 2.0–2.1px)
INK_SOFT = "#4E342A"     # İç yüz anatomisi konturu (1.1–1.4px)

SKIN_BASE = "#E8C1A6"    # Sıcak aydınlık açık ten
SKIN_LIGHT = "#F8DFCC"   # Işık düzlemi (alın, burun sırtı, elmacık üstü)
SKIN_MID = "#D1A184"     # Yarı gölge (elmacık altı, şakak)
SKIN_SHADOW = "#AC7B61"  # Ana gölge (göz çukuru, uzak yanak, burun yanı)
SKIN_DEEP = "#82543F"    # Derin gölge (çene altı, kapak kıvrımı)

HAIR_BASE = "#733726"    # Zengin kestane-kızıl ana ton
HAIR_LIGHT = "#9C523A"   # Sıcak katman ışığı
HAIR_RIM = "#D4865B"     # Altın-bakır ışık yansıması
HAIR_GOLD = "#E8A878"    # İnce sıcak parıltı vurgusu
HAIR_DARK = "#4C2217"    # Derin tutam gölgesi
HAIR_DEEP = "#2E130D"    # En derin saç altı/arka gölge

BROW_COL = "#542A1E"     # Yumuşak sıcak kestane kaş

IRIS_BASE = "#6E9674"    # Canlı zeytin-yeşil / ela iris
IRIS_DARK = "#273D2C"    # Koyu limbal halka
IRIS_LIGHT = "#B5D6AA"   # Alt ela-yeşil parlama hilali
IRIS_WARM = "#CBD89A"    # İnce sıcak altın-ela alt ışıltı

LIP_TOP = "#AE5856"      # Sıcak belirgin gül-şeftali üst dudak
LIP_BOT = "#CF7772"      # Dolgun doğal gül-şeftali alt dudak

COAT_BASE = "#EDEAE2"    # Kırık-beyaz doktor önlüğü
COAT_LIGHT = "#F8F6F1"   # Önlük omuz/göğüs ışığı
COAT_MID = "#D5D0C4"     # Önlük yarı gölge
COAT_DARK = "#ABA598"    # Önlük derin kıvrım gölgesi

SCRUB_BASE = "#4E6B7B"   # Petrol-mavi / gri-mavi scrub
SCRUB_LIGHT = "#678697"  # Scrub ışık düzlemi
SCRUB_DARK = "#364C58"   # Scrub gölge

STETH_TUBE = "#252B31"   # Stetoskop esnek tüpü
STETH_HI = "#49535E"     # Tüp yansıması
STETH_METAL = "#C4CED6"  # Metal diyafram ve kulaklık
STETH_MDARK = "#7A8793"  # Metal gölge

PANTS_BASE = "#29323E"   # Koyu antrasit-lacivert pantolon
PANTS_LIGHT = "#3B4757"
PANTS_DARK = "#1C232C"

SHOE_BASE = "#221E1D"
SHOE_SOLE = "#141110"

WARM_LIGHT = "#F4C57A"   # Revir sıcak koridor/kapı ışığı
PLAN_ACCENT = "#7FE6FF"  # Kart ızgara aksanı (A-Y v3 ortak UI dili)

_UID_COUNTER = 0


def _uid(prefix: str = "s") -> str:
    global _UID_COUNTER
    _UID_COUNTER += 1
    return f"{prefix}{_UID_COUNTER}"


# İfade tablosu: (kaş_iç_y, kaş_dış_y, üst_kapak, alt_kapak, ağız_türü, ekstra)
IFADE = {
    "odak":    (0.0, -0.6, 0.18, 0.10, "calm", ""),
    "sefkat":  (-2.2, 1.4, 0.22, 0.24, "warm_smile", "warm"),
    "endise":  (-6.8, 4.0, 0.04, 0.08, "tense_open", "worry"),
    "korku":   (-7.2, 4.2, 0.03, 0.06, "tense_open", "worry"),
    "kararli": (4.4, -2.6, 0.26, 0.16, "firm", "frown"),
    "yas":     (-7.4, 4.6, 0.40, 0.14, "sad", "tear"),
    "neutral": (0.0, 0.0, 0.18, 0.08, "calm", ""),
}


def _render_eye(
    cx: float,
    cy: float,
    rx: float,
    ry: float,
    lu: float,
    ll: float,
    look: float,
    side: bool = False,
    wet: bool = False,
    flip_lash: bool = False,
) -> str:
    """Sinematik 2D göz (v2 — R10 uyumlu): zarif etkileyici badem form, canlı zeytin-yeşil/ela iris
    (#6E9674), koyu limbal halka (#273D2C), zarif kavisli üst kirpik hattı ve tek temiz yansıma.
    """
    cid = _uid("seye")
    if side:
        shape = (
            f"M{cx - rx * 0.84:.1f},{cy + ry * 0.14:.1f} "
            f"Q{cx - rx * 0.04:.1f},{cy - ry * 1.14:.1f} {cx + rx * 0.96:.1f},{cy - ry * 0.14:.1f} "
            f"Q{cx + rx * 0.10:.1f},{cy + ry * 0.90:.1f} {cx - rx * 0.84:.1f},{cy + ry * 0.14:.1f} Z"
        )
    else:
        shape = (
            f"M{cx - rx:.1f},{cy + ry * 0.16:.1f} "
            f"Q{cx - rx * 0.34:.1f},{cy - ry * 1.16:.1f} {cx + rx * 0.36:.1f},{cy - ry * 0.98:.1f} "
            f"Q{cx + rx * 0.84:.1f},{cy - ry * 0.42:.1f} {cx + rx:.1f},{cy + ry * 0.02:.1f} "
            f"Q{cx + rx * 0.28:.1f},{cy + ry * 0.92:.1f} {cx - rx * 0.34:.1f},{cy + ry * 0.86:.1f} "
            f"Q{cx - rx * 0.78:.1f},{cy + ry * 0.54:.1f} {cx - rx:.1f},{cy + ry * 0.16:.1f} Z"
        )

    ix = cx + look * rx * 0.30
    iy = cy + ry * 0.04
    ir = ry * 0.80 if not side else ry * 0.74
    pr = ir * 0.42

    uy = cy - ry * 1.06 + lu * (ry * 1.48)
    ly = cy + ry * 0.94 - ll * (ry * 1.16)

    # Zarif kavisli üst kirpik hattı + dış köşede çok hafif doğal yukarı incelen kuyruk
    if side:
        lash_ext = (
            f'<path d="M{cx - rx * 0.86:.1f},{cy + ry * 0.06:.1f} '
            f'Q{cx:.1f},{min(uy - 1.3, cy - ry * 0.94):.1f} {cx + rx * 1.06:.1f},{cy - ry * 0.18:.1f}" '
            f'fill="none" stroke="{INK}" stroke-width="2.3" stroke-linecap="round"/>'
        )
    elif flip_lash:
        # Sol göz (dış köşe solda)
        lash_ext = (
            f'<path d="M{cx - rx * 1.12:.1f},{cy - ry * 0.08:.1f} '
            f'Q{cx - rx * 0.24:.1f},{min(uy - 1.4, cy - ry * 0.96):.1f} {cx + rx * 0.98:.1f},{cy + ry * 0.10:.1f}" '
            f'fill="none" stroke="{INK}" stroke-width="2.35" stroke-linecap="round"/>'
        )
    else:
        # Sağ göz (dış köşe sağda)
        lash_ext = (
            f'<path d="M{cx - rx * 0.98:.1f},{cy + ry * 0.10:.1f} '
            f'Q{cx + rx * 0.22:.1f},{min(uy - 1.4, cy - ry * 0.96):.1f} {cx + rx * 1.12:.1f},{cy - ry * 0.08:.1f}" '
            f'fill="none" stroke="{INK}" stroke-width="2.35" stroke-linecap="round"/>'
        )

    out = [
        f'<defs><clipPath id="{cid}"><path d="{shape}"/></clipPath></defs>',
        f'<path d="{shape}" fill="#F2F0EB"/>',
        f'<g clip-path="url(#{cid})">',
        # İris: koyu limbal halka + canlı zeytin-yeşil/ela + alt sıcak hilal
        f'<circle cx="{ix:.1f}" cy="{iy:.1f}" r="{ir:.1f}" fill="{IRIS_DARK}"/>',
        f'<circle cx="{ix:.1f}" cy="{iy:.1f}" r="{ir * 0.81:.1f}" fill="{IRIS_BASE}"/>',
        f'<ellipse cx="{ix:.1f}" cy="{iy + ir * 0.34:.1f}" rx="{ir * 0.56:.1f}" ry="{ir * 0.28:.1f}" fill="{IRIS_LIGHT}" opacity="0.86"/>',
        f'<ellipse cx="{ix + ir * 0.10:.1f}" cy="{iy + ir * 0.42:.1f}" rx="{ir * 0.32:.1f}" ry="{ir * 0.15:.1f}" fill="{IRIS_WARM}" opacity="0.65"/>',
        # Göz bebeği
        f'<circle cx="{ix:.1f}" cy="{iy:.1f}" r="{pr:.1f}" fill="#121614"/>',
        # Üst kapak yumuşak döküm gölgesi
        f'<rect x="{cx - rx - 4:.1f}" y="{cy - ry - 4:.1f}" width="{rx * 2 + 8:.1f}" height="{(uy - (cy - ry - 4)) + ry * 0.40:.1f}" fill="#3D4641" opacity="0.22"/>',
        # Tek temiz parlama (catchlight)
        f'<circle cx="{ix - ir * 0.30:.1f}" cy="{iy - ir * 0.24:.1f}" r="{max(1.3, ir * 0.23):.1f}" fill="#FFFFFF" opacity="0.97"/>',
        (
            f'<path d="M{cx - rx * 0.55:.1f},{ly - 0.8:.1f} Q{cx:.1f},{ly + 0.6:.1f} {cx + rx * 0.55:.1f},{ly - 0.8:.1f}" '
            f'fill="none" stroke="#E4F4FF" stroke-width="1.35" opacity="0.82" stroke-linecap="round"/>'
            if wet else ""
        ),
        f'<rect x="{cx - rx - 6:.1f}" y="{cy - ry * 2.2:.1f}" width="{rx * 2 + 12:.1f}" height="{uy - (cy - ry * 2.2):.1f}" fill="{SKIN_SHADOW}" opacity="0.72"/>',
        f'<rect x="{cx - rx - 6:.1f}" y="{ly:.1f}" width="{rx * 2 + 12:.1f}" height="{ry * 2.2:.1f}" fill="{SKIN_BASE}"/>',
        f'<path d="M{cx - rx - 2:.1f},{uy + 0.9:.1f} Q{cx:.1f},{uy - 2.5:.1f} {cx + rx + 2:.1f},{uy + 0.4:.1f}" fill="none" stroke="{INK}" stroke-width="2.4" stroke-linecap="round"/>',
        '</g>',
        lash_ext,
        f'<path d="M{cx - rx * 0.76:.1f},{cy + ry * 0.34:.1f} Q{cx:.1f},{min(ly + 0.7, cy + ry * 0.90):.1f} {cx + rx * 0.76:.1f},{cy + ry * 0.28:.1f}" fill="none" stroke="{INK_SOFT}" stroke-width="0.95" opacity="0.48" stroke-linecap="round"/>',
        f'<path d="M{cx - rx * 0.86:.1f},{cy - ry * 0.86:.1f} Q{cx:.1f},{cy - ry * 1.50:.1f} {cx + rx * 0.88:.1f},{cy - ry * 0.76:.1f}" fill="none" stroke="{SKIN_DEEP}" stroke-width="1.15" opacity="0.58" stroke-linecap="round"/>',
    ]
    return "".join(out)


def _render_brow(
    x_in: float,
    y_in: float,
    x_out: float,
    y_out: float,
    arch_y: float = -4.6,
    thick: float = 3.6,
) -> str:
    """Yumuşak, zarif kavisli sıcak kestane kadın kaşı."""
    mx = x_in * 0.34 + x_out * 0.66
    my = (y_in + y_out) * 0.5 + arch_y
    t_in = thick * 0.52
    t_mid = thick * 0.42
    t_out = thick * 0.14
    d = (
        f"M{x_in:.1f},{y_in - t_in:.1f} "
        f"Q{mx:.1f},{my - t_mid:.1f} {x_out:.1f},{y_out - t_out:.1f} "
        f"L{x_out:.1f},{y_out + t_out:.1f} "
        f"Q{mx:.1f},{my + t_mid * 0.65:.1f} {x_in:.1f},{y_in + t_in * 0.78:.1f} Z"
    )
    return (
        f'<path d="{d}" fill="{BROW_COL}"/>'
        f'<path d="M{x_in:.1f},{y_in - t_in * 0.45:.1f} Q{mx:.1f},{my - t_mid * 0.45:.1f} {x_out:.1f},{y_out:.1f}" '
        f'fill="none" stroke="#854B36" stroke-width="0.85" opacity="0.46"/>'
    )


def _render_mouth(mx: float, my: float, mw: float, kind: str, view: str) -> str:
    """Sinematik 2D zarif, doğal dolgun gül-şeftali dudak hacmi (v2)."""
    if view == "side":
        if kind == "tense_open":
            return (
                f'<path d="M{mx + 2:.1f},{my - 3.6:.1f} Q{mx - 9.5:.1f},{my + 1.0:.1f} {mx + 2:.1f},{my + 7.0:.1f}" '
                f'fill="#5C2B28" stroke="{INK}" stroke-width="1.4"/>'
            )
        dy = -3.0 if kind == "warm_smile" else (2.4 if kind == "sad" else -1.0)
        return (
            f'<path d="M{mx + 2.4:.1f},{my - 5.6:.1f} Q{mx - 5.0:.1f},{my - 4.4:.1f} {mx - 12.2:.1f},{my - 0.5:.1f} L{mx + 2.4:.1f},{my:.1f} Z" fill="{LIP_TOP}" opacity="0.86"/>'
            f'<path d="M{mx + 2.0:.1f},{my + 0.4:.1f} Q{mx - 5.6:.1f},{my + 7.0:.1f} {mx - 11.4:.1f},{my + 0.8:.1f} Z" fill="{LIP_BOT}" opacity="0.84"/>'
            f'<path d="M{mx + 2.4:.1f},{my:.1f} Q{mx - 5.5:.1f},{my + 1.0 + dy * 0.4:.1f} {mx - 12.5:.1f},{my + dy:.1f}" '
            f'fill="none" stroke="{INK}" stroke-width="1.55" stroke-linecap="round"/>'
            f'<path d="M{mx - 2.0:.1f},{my + 8.2:.1f} Q{mx - 6.8:.1f},{my + 9.4:.1f} {mx - 10.2:.1f},{my + 7.0:.1f}" fill="none" stroke="{SKIN_DEEP}" stroke-width="1.2" opacity="0.44" stroke-linecap="round"/>'
        )

    asym = 0.0 if view == "front" else 0.10
    lx = mx - mw * (1.0 - asym)
    rx = mx + mw * (1.0 + asym)

    if kind == "tense_open":
        return (
            f'<path d="M{lx + 1.5:.1f},{my + 1.0:.1f} Q{mx:.1f},{my - 5.8:.1f} {rx - 1.5:.1f},{my + 1.0:.1f} '
            f'Q{mx:.1f},{my + 9.4:.1f} {lx + 1.5:.1f},{my + 1.0:.1f} Z" fill="#5A2B28" stroke="{INK}" stroke-width="1.45"/>'
            f'<path d="M{lx + 5.2:.1f},{my - 0.6:.1f} Q{mx:.1f},{my - 2.3:.1f} {rx - 5.2:.1f},{my - 0.6:.1f}" fill="none" stroke="#F4EFE8" stroke-width="2.2" stroke-linecap="round"/>'
            f'<path d="M{lx + 0.8:.1f},{my + 1.2:.1f} Q{mx:.1f},{my + 11.4:.1f} {rx - 0.8:.1f},{my + 1.2:.1f}" fill="none" stroke="{LIP_BOT}" stroke-width="2.5" opacity="0.82" stroke-linecap="round"/>'
            f'<path d="M{mx - mw * 0.42:.1f},{my + 12.4:.1f} Q{mx:.1f},{my + 13.8:.1f} {mx + mw * 0.42:.1f},{my + 12.0:.1f}" fill="none" stroke="{SKIN_DEEP}" stroke-width="1.2" opacity="0.42" stroke-linecap="round"/>'
        )

    # Varsayılan odak: çok hafif sıcak ve dingin duruş (soğuk/gergin değil)
    c_l, c_r, mid_dip = -1.6, -1.8, 1.5
    if kind == "warm_smile":
        c_l, c_r, mid_dip = -4.4, -5.0, 2.8
    elif kind == "sad":
        c_l, c_r, mid_dip = 3.0, 2.8, -1.4
    elif kind == "firm":
        c_l, c_r, mid_dip = 0.5, 0.3, 0.3

    upper_lip = (
        f"M{lx:.1f},{my + c_l:.1f} "
        f"Q{mx - mw * 0.35:.1f},{my - 7.5:.1f} {mx - mw * 0.14:.1f},{my - 6.6:.1f} "
        f"Q{mx:.1f},{my - 4.4:.1f} {mx + mw * 0.14:.1f},{my - 6.6:.1f} "
        f"Q{mx + mw * 0.35:.1f},{my - 7.5:.1f} {rx:.1f},{my + c_r:.1f} "
        f"Q{mx:.1f},{my + mid_dip:.1f} {lx:.1f},{my + c_l:.1f} Z"
    )
    lower_lip = (
        f"M{lx + mw * 0.08:.1f},{my + c_l * 0.6 + 0.4:.1f} "
        f"Q{mx:.1f},{my + 11.2 + mid_dip * 0.44:.1f} {rx - mw * 0.08:.1f},{my + c_r * 0.6 + 0.4:.1f} "
        f"Q{mx:.1f},{my + mid_dip + 0.4:.1f} {lx + mw * 0.08:.1f},{my + c_l * 0.6 + 0.4:.1f} Z"
    )
    seam = (
        f"M{lx:.1f},{my + c_l:.1f} "
        f"Q{mx - mw * 0.34:.1f},{my + mid_dip * 0.45:.1f} {mx:.1f},{my + mid_dip + 0.5:.1f} "
        f"Q{mx + mw * 0.34:.1f},{my + mid_dip * 0.45:.1f} {rx:.1f},{my + c_r:.1f}"
    )

    smile_dimple = ""
    if kind == "warm_smile":
        smile_dimple = (
            f'<path d="M{lx - 3.2:.1f},{my + c_l - 3.2:.1f} Q{lx - 5.0:.1f},{my + c_l + 1.2:.1f} {lx - 2.0:.1f},{my + c_l + 3.8:.1f}" '
            f'fill="none" stroke="{SKIN_SHADOW}" stroke-width="1.0" opacity="0.40" stroke-linecap="round"/>'
            f'<path d="M{rx + 3.2:.1f},{my + c_r - 3.2:.1f} Q{rx + 5.0:.1f},{my + c_r + 1.2:.1f} {rx + 2.0:.1f},{my + c_r + 3.8:.1f}" '
            f'fill="none" stroke="{SKIN_SHADOW}" stroke-width="1.0" opacity="0.40" stroke-linecap="round"/>'
        )

    return (
        f'<path d="{upper_lip}" fill="{LIP_TOP}" opacity="0.90"/>'
        f'<path d="{lower_lip}" fill="{LIP_BOT}" opacity="0.88"/>'
        # Cupid's bow zarif parlama
        f'<path d="M{mx - mw * 0.22:.1f},{my - 6.0:.1f} Q{mx:.1f},{my - 4.3:.1f} {mx + mw * 0.22:.1f},{my - 6.0:.1f}" fill="none" stroke="{SKIN_LIGHT}" stroke-width="1.2" opacity="0.72" stroke-linecap="round"/>'
        # Alt dudak yumuşak doğal parlama
        f'<path d="M{mx - mw * 0.34:.1f},{my + 4.8:.1f} Q{mx:.1f},{my + 6.4:.1f} {mx + mw * 0.30:.1f},{my + 4.6:.1f}" fill="none" stroke="#FCE3D8" stroke-width="2.1" opacity="0.70" stroke-linecap="round"/>'
        # Dudak ayrım çizgisi (ince, zarif)
        f'<path d="{seam}" fill="none" stroke="{INK_SOFT}" stroke-width="1.55" stroke-linecap="round"/>'
        f'<path d="M{lx + 2.5:.1f},{my + c_l * 0.7:.1f} Q{mx:.1f},{my + mid_dip + 0.5:.1f} {rx - 2.5:.1f},{my + c_r * 0.7:.1f}" fill="none" stroke="{INK}" stroke-width="1.2" opacity="0.75" stroke-linecap="round"/>'
        # Köşe yumuşak gölge
        f'<ellipse cx="{lx - 0.5:.1f}" cy="{my + c_l + 0.3:.1f}" rx="1.6" ry="0.9" fill="{SKIN_DEEP}" opacity="0.34"/>'
        f'<ellipse cx="{rx + 0.5:.1f}" cy="{my + c_r + 0.3:.1f}" rx="1.6" ry="0.9" fill="{SKIN_DEEP}" opacity="0.34"/>'
        f'{smile_dimple}'
        # Alt dudak altı hafif gölge
        f'<path d="M{mx - mw * 0.40:.1f},{my + 11.2:.1f} Q{mx:.1f},{my + 12.8:.1f} {mx + mw * 0.40:.1f},{my + 11.0:.1f}" '
        f'fill="none" stroke="{SKIN_DEEP}" stroke-width="1.3" opacity="0.44" stroke-linecap="round"/>'
    )


def _hair_back(view: str, gid_hdark: str | None = None) -> str:
    """Omuz hizasında katmanlı, uçları incelen (tapered), doğal dalgalı kestane-kızıl saç — arka katman.
    Küt/tüp uçlar YOK; katmanlı ve incelen doğal uçlarla biter.
    """
    own_defs = ""
    if gid_hdark is None:
        gid_hdark = _uid("shd")
        own_defs = (
            f'<defs><linearGradient id="{gid_hdark}" x1="0.2" y1="0.0" x2="0.8" y2="1.0">'
            f'<stop offset="0%" stop-color="{HAIR_BASE}"/>'
            f'<stop offset="52%" stop-color="{HAIR_DARK}"/>'
            f'<stop offset="100%" stop-color="{HAIR_DEEP}"/>'
            f'</linearGradient></defs>'
        )

    if view == "front":
        back_d = (
            "M-76,-24 C-84,-78 -44,-110 0,-112 C44,-110 84,-78 76,-24 "
            "C86,12 96,52 94,94 C92,114 100,132 88,144 "
            "C80,136 76,128 70,138 C64,148 52,146 46,132 "
            "C36,140 20,142 0,138 C-20,142 -36,140 -46,132 "
            "C-52,146 -64,148 -70,138 C-76,128 -80,136 -88,144 "
            "C-100,132 -92,114 -94,94 C-96,52 -86,12 -76,-24 Z"
        )
        return (
            f'{own_defs}'
            f'<path d="{back_d}" fill="url(#{gid_hdark})" stroke="{INK}" stroke-width="2.05" stroke-linejoin="round"/>'
            f'<path d="M-78,36 C-88,72 -88,108 -78,136 M78,36 C88,72 88,108 78,136" '
            f'fill="none" stroke="{HAIR_DEEP}" stroke-width="1.9" opacity="0.60" stroke-linecap="round"/>'
            f'<path d="M-68,72 C-62,102 -56,122 -52,138 M68,72 C62,102 56,122 52,138" '
            f'fill="none" stroke="{HAIR_LIGHT}" stroke-width="1.5" opacity="0.34" stroke-linecap="round"/>'
        )
    elif view == "3q":
        back_d = (
            "M-80,-20 C-88,-78 -44,-110 4,-112 C48,-112 78,-84 76,-34 "
            "C86,6 88,52 84,96 C82,114 88,130 76,140 "
            "C68,134 62,126 56,136 C48,144 36,138 28,128 "
            "C8,136 -20,142 -48,144 C-60,148 -72,144 -78,134 "
            "C-84,142 -94,136 -96,122 C-102,78 -94,24 -80,-20 Z"
        )
        return (
            f'{own_defs}'
            f'<path d="{back_d}" fill="url(#{gid_hdark})" stroke="{INK}" stroke-width="2.05" stroke-linejoin="round"/>'
            f'<path d="M-84,20 C-94,64 -92,104 -76,134 M-70,52 C-74,90 -66,120 -52,140" '
            f'fill="none" stroke="{HAIR_DEEP}" stroke-width="2.0" opacity="0.62" stroke-linecap="round"/>'
            f'<path d="M-88,18 C-96,56 -92,94 -80,124" '
            f'fill="none" stroke="{HAIR_RIM}" stroke-width="2.2" opacity="0.46" stroke-linecap="round"/>'
        )
    else:  # side (sağa bakar)
        back_d = (
            "M-78,-16 C-88,-76 -44,-112 4,-112 C44,-112 68,-84 68,-44 "
            "L56,-34 C46,-54 22,-66 -2,-58 C-26,-50 -36,-22 -36,12 "
            "C-36,48 -24,90 -6,132 C-16,144 -28,144 -38,134 "
            "C-48,146 -64,146 -76,134 C-94,118 -100,70 -92,22 Z"
        )
        return (
            f'{own_defs}'
            f'<path d="{back_d}" fill="url(#{gid_hdark})" stroke="{INK}" stroke-width="2.05" stroke-linejoin="round"/>'
            f'<path d="M-76,-6 C-90,40 -88,88 -70,130 M-60,12 C-70,54 -66,98 -48,136" '
            f'fill="none" stroke="{HAIR_DEEP}" stroke-width="2.0" opacity="0.60" stroke-linecap="round"/>'
            f'<path d="M-86,8 C-94,48 -92,88 -78,124" '
            f'fill="none" stroke="{HAIR_RIM}" stroke-width="2.3" opacity="0.48" stroke-linecap="round"/>'
        )


def _hair_front(view: str, gid_hair: str) -> str:
    """v2 Saç: Uçları incelen (tapered), doğal S-dalgalı, yüzü yumuşakça çerçeveleyen yan perçemli
    zengin kestane-kızıl saç ve sıcak altın-bakır ışık yansıması.
    """
    if view == "front":
        # Sol ana dalgalı katman — omuz hizasında doğal dışa-içe dalgalanıp incelen (tapered) uç
        left_lock = (
            "M-16,-110 C-56,-106 -84,-76 -84,-24 C-86,18 -92,66 -84,114 "
            "C-80,128 -74,138 -64,144 C-66,130 -64,116 -60,104 "
            "C-54,118 -46,128 -36,130 C-48,108 -56,74 -58,34 "
            "C-60,-4 -54,-38 -36,-56 C-26,-64 -16,-68 -12,-74 C-10,-86 -12,-98 -16,-110 Z"
        )
        # Sağ ana dalgalı katman — yumuşak yan perçem akışı + incelen (tapered) uç
        right_lock = (
            "M-16,-110 C24,-114 70,-92 84,-42 C90,-6 92,50 84,114 "
            "C80,128 74,138 64,144 C66,130 64,116 60,104 "
            "C54,118 46,128 36,130 C48,108 56,74 58,34 "
            "C60,-4 52,-40 28,-58 C12,-68 -4,-70 -16,-74 C-16,-88 -16,-100 -16,-110 Z"
        )
        # Yüzü yumuşak çerçeveleyen doğal yan perçem (üst kenar ana saça gömülü — aralık yok)
        bang_sweep = (
            "M-16,-84 C8,-82 38,-66 56,-34 C62,-18 64,2 60,26 "
            "C54,8 48,-12 36,-28 C20,-48 0,-60 -16,-66 Z"
        )
        # Sol elmacık hizasında ince yüz çerçeveleme tutamı (tapered tip)
        left_frame = (
            "M-56,-10 C-64,22 -64,58 -54,94 C-46,104 -38,108 -32,106 "
            "C-42,92 -48,66 -50,36 C-52,16 -52,0 -56,-10 Z"
        )
        return (
            f'<path d="{left_lock}" fill="url(#{gid_hair})" stroke="{INK}" stroke-width="2.0" stroke-linejoin="round"/>'
            f'<path d="{right_lock}" fill="url(#{gid_hair})" stroke="{INK}" stroke-width="2.0" stroke-linejoin="round"/>'
            f'<path d="{left_frame}" fill="{HAIR_BASE}" stroke="{INK}" stroke-width="1.65" stroke-linejoin="round"/>'
            f'<path d="{bang_sweep}" fill="url(#{gid_hair})"/>'
            f'<path d="M-15,-64 C2,-58 20,-46 34,-26 C46,-10 52,8 58,24" fill="none" stroke="{INK}" stroke-width="1.45" opacity="0.82" stroke-linecap="round"/>'
            # Doğal yan ayrım gölgesi
            f'<path d="M-16,-108 Q-14,-90 -15,-74" fill="none" stroke="{HAIR_DEEP}" stroke-width="1.6" opacity="0.70" stroke-linecap="round"/>'
            # Dalgalı tutam çizgileri
            f'<path d="M-38,-94 C-66,-72 -76,-34 -74,16 C-72,58 -76,96 -68,132" fill="none" stroke="{HAIR_DARK}" stroke-width="1.45" opacity="0.66" stroke-linecap="round"/>'
            f'<path d="M18,-96 C54,-80 72,-42 74,14 C76,58 76,96 68,132" fill="none" stroke="{HAIR_DARK}" stroke-width="1.45" opacity="0.66" stroke-linecap="round"/>'
            f'<path d="M-26,-78 C-48,-62 -60,-36 -62,-4 M10,-80 C38,-68 56,-44 62,-8" fill="none" stroke="{HAIR_DARK}" stroke-width="1.3" opacity="0.54" stroke-linecap="round"/>'
            # Zengin altın-bakır ışık yansıması ve sıcak kenar rim ışığı
            f'<path d="M-48,-88 C-24,-102 6,-102 34,-88" fill="none" stroke="{HAIR_RIM}" stroke-width="3.6" opacity="0.66" stroke-linecap="round"/>'
            f'<path d="M-36,-92 C-16,-100 6,-100 24,-92" fill="none" stroke="{HAIR_GOLD}" stroke-width="1.6" opacity="0.62" stroke-linecap="round"/>'
            f'<path d="M-70,-50 C-78,-14 -82,30 -76,78" fill="none" stroke="{HAIR_RIM}" stroke-width="2.4" opacity="0.52" stroke-linecap="round"/>'
            f'<path d="M46,-74 C66,-52 76,-18 78,24" fill="none" stroke="{HAIR_RIM}" stroke-width="2.2" opacity="0.48" stroke-linecap="round"/>'
        )
    elif view == "3q":
        # Uzak (sağ) taraf omuza doğru doğal incelen (tapered) katman
        far_lock = (
            "M16,-108 C56,-104 78,-74 80,-24 C82,16 82,62 74,114 "
            "C70,126 62,134 54,136 C56,122 54,108 48,96 "
            "C58,64 62,28 60,-10 C58,-44 42,-64 20,-70 Z"
        )
        # Yakın (sol) taraf hacimli, doğal S-dalgalı, uçları incelen (tapered) kestane-kızıl katman
        near_lock = (
            "M16,-110 C-28,-114 -78,-88 -86,-28 C-92,20 -94,76 -80,128 "
            "C-74,140 -64,146 -54,148 C-58,132 -56,116 -50,104 "
            "C-44,120 -34,132 -22,134 C-38,108 -50,68 -52,22 "
            "C-54,-22 -40,-52 -8,-66 C6,-72 16,-72 22,-72 C22,-88 20,-102 16,-110 Z"
        )
        # Ön omuza yumuşak düşen, ucu incelen (tapered) ikincil dalgalı tutam
        wave_lock = (
            "M-56,8 C-70,48 -70,90 -58,128 C-50,138 -40,142 -32,138 "
            "C-42,120 -46,96 -46,68 C-46,46 -44,26 -44,12 Z"
        )
        # Alından sol şakağa doğal akıp incelen yüz çerçeveleme perçemi (üst kenar ana saça gömülü — aralık yok)
        bang_3q = (
            "M20,-84 C-4,-82 -36,-64 -52,-30 C-58,-12 -58,10 -52,32 "
            "C-46,14 -42,-4 -32,-22 C-20,-44 -2,-58 20,-64 Z"
        )
        return (
            f'<path d="{far_lock}" fill="url(#{gid_hair})" opacity="0.94" stroke="{INK}" stroke-width="2.0" stroke-linejoin="round"/>'
            f'<path d="{far_lock}" fill="{HAIR_DARK}" opacity="0.30"/>'
            f'<path d="{near_lock}" fill="url(#{gid_hair})" stroke="{INK}" stroke-width="2.0" stroke-linejoin="round"/>'
            f'<path d="{wave_lock}" fill="{HAIR_BASE}" stroke="{INK}" stroke-width="1.75" stroke-linejoin="round"/>'
            f'<path d="{bang_3q}" fill="url(#{gid_hair})"/>'
            f'<path d="M20,-64 C-2,-58 -20,-44 -32,-22 C-42,-4 -46,14 -52,32" fill="none" stroke="{INK}" stroke-width="1.45" opacity="0.82" stroke-linecap="round"/>'
            # Ayrım & katman gölgeleri
            f'<path d="M16,-108 Q18,-88 20,-72" fill="none" stroke="{HAIR_DEEP}" stroke-width="1.6" opacity="0.70" stroke-linecap="round"/>'
            f'<path d="M-14,-98 C-50,-84 -72,-44 -74,12 C-76,62 -72,102 -60,136" fill="none" stroke="{HAIR_DARK}" stroke-width="1.55" opacity="0.70" stroke-linecap="round"/>'
            f'<path d="M-30,-74 C-50,-54 -60,-16 -58,32 C-56,70 -50,104 -38,130" fill="none" stroke="{HAIR_DARK}" stroke-width="1.35" opacity="0.60" stroke-linecap="round"/>'
            f'<path d="M40,-86 C60,-68 72,-34 70,22" fill="none" stroke="{HAIR_DEEP}" stroke-width="1.35" opacity="0.58" stroke-linecap="round"/>'
            # Zengin altın-bakır parıltı ve sol kenar rim ışığı
            f'<path d="M-42,-90 C-14,-104 16,-104 40,-90" fill="none" stroke="{HAIR_RIM}" stroke-width="3.6" opacity="0.68" stroke-linecap="round"/>'
            f'<path d="M-30,-94 C-10,-102 12,-102 30,-94" fill="none" stroke="{HAIR_GOLD}" stroke-width="1.6" opacity="0.64" stroke-linecap="round"/>'
            f'<path d="M-70,-54 C-82,-16 -84,34 -74,88" fill="none" stroke="{HAIR_RIM}" stroke-width="2.5" opacity="0.54" stroke-linecap="round"/>'
            f'<path d="M-48,-44 C-56,-12 -56,26 -48,68" fill="none" stroke="{HAIR_GOLD}" stroke-width="1.8" opacity="0.46" stroke-linecap="round"/>'
        )
    else:  # side (profil, sağa bakar — yüzle tam birleşik, uçları incelen)
        side_lock = (
            "M60,-46 C54,-84 26,-110 -10,-110 C-56,-108 -88,-74 -90,-16 "
            "C-92,36 -86,90 -68,136 C-60,144 -50,146 -42,140 "
            "C-46,126 -42,114 -36,106 C-30,122 -20,134 -8,136 "
            "C-18,96 -22,52 -16,12 C-12,-14 -2,-34 16,-48 "
            "C30,-58 46,-56 60,-46 Z"
        )
        cheek_strand = (
            "M20,-48 C8,-24 4,10 4,48 C4,78 8,104 18,124 "
            "C8,132 -4,128 -12,116 C-20,82 -20,38 -14,-6 C-10,-30 0,-46 20,-48 Z"
        )
        return (
            f'<path d="{side_lock}" fill="url(#{gid_hair})" stroke="{INK}" stroke-width="2.0" stroke-linejoin="round"/>'
            f'<path d="{cheek_strand}" fill="{HAIR_BASE}" stroke="{INK}" stroke-width="1.75" stroke-linejoin="round"/>'
            f'<path d="M-16,-98 C-54,-84 -76,-42 -76,16 C-76,64 -70,102 -54,136" fill="none" stroke="{HAIR_DARK}" stroke-width="1.6" opacity="0.70" stroke-linecap="round"/>'
            f'<path d="M12,-86 C-26,-74 -48,-36 -48,20 C-48,66 -40,100 -24,128" fill="none" stroke="{HAIR_DARK}" stroke-width="1.4" opacity="0.62" stroke-linecap="round"/>'
            f'<path d="M-38,-90 C-10,-104 22,-100 44,-80" fill="none" stroke="{HAIR_RIM}" stroke-width="3.4" opacity="0.64" stroke-linecap="round"/>'
            f'<path d="M-28,-94 C-6,-102 18,-98 34,-84" fill="none" stroke="{HAIR_GOLD}" stroke-width="1.5" opacity="0.60" stroke-linecap="round"/>'
            f'<path d="M-76,-44 C-86,-4 -86,46 -72,98" fill="none" stroke="{HAIR_RIM}" stroke-width="2.4" opacity="0.52" stroke-linecap="round"/>'
        )


def kafa_sara(
    view: str = "3q",
    ifade: str = "odak",
    look: float = 0.25,
    boyun: bool = False,
    arka_sac: bool = True,
) -> str:
    """Sara Tancredi kafası v2 (Stil B + A hibrit — A-Y v3 ile uyumlu, daha zarif ve çekici).
    Merkez (0, 0), yüz yüksekliği ~182 (y: -90 .. +92). view: 'front' | '3q' | 'side'.
    """
    bi, bo, lu, ll, mk, extra = IFADE.get(ifade, IFADE["odak"])
    is_wet = extra == "tear"

    o: list[str] = []
    defs: list[str] = []

    cid_face = _uid("sfclip")
    gid_skin = _uid("sskin")
    gid_cheek = _uid("scheek")
    gid_hair = _uid("shair")
    gid_hdark = _uid("shdark")

    defs.append(
        f'<linearGradient id="{gid_skin}" x1="0.14" y1="0.08" x2="0.88" y2="0.92">'
        f'<stop offset="0%" stop-color="{SKIN_LIGHT}"/>'
        f'<stop offset="48%" stop-color="{SKIN_BASE}"/>'
        f'<stop offset="100%" stop-color="{SKIN_MID}"/>'
        f'</linearGradient>'
    )
    defs.append(
        f'<linearGradient id="{gid_cheek}" x1="0.0" y1="0.5" x2="1.0" y2="0.35">'
        f'<stop offset="0%" stop-color="{SKIN_SHADOW}" stop-opacity="0.28"/>'
        f'<stop offset="65%" stop-color="{SKIN_SHADOW}" stop-opacity="0.10"/>'
        f'<stop offset="100%" stop-color="{SKIN_SHADOW}" stop-opacity="0.0"/>'
        f'</linearGradient>'
    )
    defs.append(
        f'<linearGradient id="{gid_hair}" x1="0.12" y1="0.05" x2="0.86" y2="0.96">'
        f'<stop offset="0%" stop-color="{HAIR_LIGHT}"/>'
        f'<stop offset="38%" stop-color="{HAIR_BASE}"/>'
        f'<stop offset="100%" stop-color="{HAIR_DARK}"/>'
        f'</linearGradient>'
    )
    defs.append(
        f'<linearGradient id="{gid_hdark}" x1="0.2" y1="0.0" x2="0.8" y2="1.0">'
        f'<stop offset="0%" stop-color="{HAIR_BASE}"/>'
        f'<stop offset="52%" stop-color="{HAIR_DARK}"/>'
        f'<stop offset="100%" stop-color="{HAIR_DEEP}"/>'
        f'</linearGradient>'
    )

    # ── 1. Yüz Silueti (v2: zarif, feminen oval-kalp form, yumuşak narin çene) ──
    if view == "front":
        face_d = (
            "M-58,-22 C-59,-66 -34,-90 0,-91 C34,-90 59,-66 58,-22 "
            "C58,4 56,24 48,44 C40,62 28,78 14,88 C6,92 -6,92 -14,88 "
            "C-28,78 -40,62 -48,44 C-56,24 -58,4 -58,-22 Z"
        )
        ears = [(-58, 6, -1), (58, 6, 1)]
        eye_specs = [(-25.0, -6.5, 16.0, 9.1, False, True), (25.0, -6.5, 16.0, 9.1, False, False)]
        lk = 0.0 if look == 0.25 else look
        mx, my, mw = 0.0, 48.5, 20.8
    elif view == "3q":
        face_d = (
            "M-57,-20 C-59,-66 -32,-90 8,-91 C44,-90 62,-66 62,-24 "
            "C63,-8 64,4 62,18 C59,32 54,46 47,58 "
            "C39,72 30,84 19,89 C9,92 -4,88 -18,79 "
            "C-34,68 -46,50 -52,30 C-56,16 -57,-2 -57,-20 Z"
        )
        ears = [(-56, 8, -1)]
        eye_specs = [(-4.2, -6.5, 16.0, 9.1, False, True), (40.2, -6.5, 13.2, 8.6, False, False)]
        lk = look
        mx, my, mw = 23.0, 48.5, 18.6
    else:  # side (profil, sağa bakar)
        face_d = (
            "M-62,-18 C-65,-66 -34,-91 6,-91 C40,-91 60,-70 61,-36 "
            "L62,-16 C63,-10 65,-6 68,-1 L78,22 C80,27 76,31 69,32 "
            "L65,32 L68,42 C70,46 67,49 63,50 L66,57 C67,62 63,67 58,69 "
            "L59,80 C59,88 50,92 36,92 L16,91 C-2,90 -20,82 -32,66 "
            "C-48,46 -58,20 -62,-18 Z"
        )
        ears = [(-8, 10, -1)]
        eye_specs = [(45.5, -7.0, 12.4, 8.4, True, False)]
        lk = max(0.35, look)
        mx, my, mw = 61.0, 49.0, 11.8

    defs.append(f'<clipPath id="{cid_face}"><path d="{face_d}"/></clipPath>')
    o.insert(0, f'<defs>{"".join(defs)}</defs>')

    # ── 2. Arka Saç Katmanı ──
    if arka_sac:
        o.append(_hair_back(view, gid_hdark))

    # ── 3. Opsiyonel Zarif Anatomik Boyun (R4) ──
    if boyun:
        if view == "front":
            nk_d = "M-24,68 L-27,130 Q0,140 27,130 L24,68 Z"
            sh_d = "M-24,68 Q0,108 24,68 L26,98 Q0,113 -26,98 Z"
            scm = (
                f'<path d="M-21,84 Q-13,110 -5,128 M21,84 Q13,110 5,128" fill="none" stroke="{SKIN_SHADOW}" stroke-width="1.4" opacity="0.44" stroke-linecap="round"/>'
                f'<path d="M-7,124 Q0,129 7,124" fill="none" stroke="{SKIN_DEEP}" stroke-width="1.25" opacity="0.44" stroke-linecap="round"/>'
            )
        elif view == "3q":
            nk_d = "M-29,60 L-32,130 Q-4,140 18,126 L17,76 Z"
            sh_d = "M-29,60 Q0,108 18,74 L18,104 Q-4,118 -31,94 Z"
            scm = (
                f'<path d="M-25,82 Q-13,108 -2,128 M10,90 Q8,110 10,126" fill="none" stroke="{SKIN_SHADOW}" stroke-width="1.4" opacity="0.44" stroke-linecap="round"/>'
                f'<path d="M-7,110 Q0,115 6,110" fill="none" stroke="{SKIN_DEEP}" stroke-width="1.2" opacity="0.40" stroke-linecap="round"/>'
            )
        else:
            nk_d = "M-36,58 L-43,130 Q-10,140 14,126 L11,80 Z"
            sh_d = "M-36,58 Q-8,106 13,78 L12,104 Q-10,118 -38,96 Z"
            scm = f'<path d="M-26,80 Q-13,106 -3,126" fill="none" stroke="{SKIN_SHADOW}" stroke-width="1.5" opacity="0.44" stroke-linecap="round"/>'
        o.append(
            f'<path d="{nk_d}" fill="{SKIN_MID}"/>'
            f'<path d="{sh_d}" fill="{SKIN_DEEP}" opacity="0.50"/>'
            f'{scm}'
            f'<path d="{nk_d}" fill="none" stroke="{INK}" stroke-width="2.0" stroke-linejoin="round"/>'
        )

    # ── 4. Kulaklar ──
    for ex, ey, side_sgn in ears:
        ew = 9.6 if view != "side" else 11.2
        eh = 17.5
        ear_d = (
            f"M{ex},{ey - eh * 0.85:.1f} "
            f"C{ex + side_sgn * ew * 1.15:.1f},{ey - eh * 0.88:.1f} {ex + side_sgn * ew * 1.22:.1f},{ey + eh * 0.1:.1f} {ex + side_sgn * ew * 0.72:.1f},{ey + eh * 0.72:.1f} "
            f"C{ex + side_sgn * ew * 0.42:.1f},{ey + eh * 0.98:.1f} {ex},{ey + eh * 0.90:.1f} {ex},{ey + eh * 0.65:.1f} Z"
        )
        o.append(
            f'<path d="{ear_d}" fill="{SKIN_MID}" stroke="{INK}" stroke-width="1.9" stroke-linejoin="round"/>'
            f'<path d="M{ex + side_sgn * ew * 0.25:.1f},{ey - eh * 0.46:.1f} '
            f'Q{ex + side_sgn * ew * 0.80:.1f},{ey - eh * 0.14:.1f} {ex + side_sgn * ew * 0.30:.1f},{ey + eh * 0.44:.1f}" '
            f'fill="none" stroke="{SKIN_DEEP}" stroke-width="1.3" stroke-linecap="round"/>'
        )

    # ── 5. Yüz Tabanı + Zarif Sinematik Yüz Düzlemleri ──
    o.append(f'<path d="{face_d}" fill="url(#{gid_skin})"/>')
    inner: list[str] = []

    if view == "front":
        inner.append(
            f'<path d="M28,-94 C44,-52 43,-12 37,22 C33,48 22,74 8,96 L84,96 L84,-94 Z" fill="{SKIN_SHADOW}" opacity="0.20"/>'
            f'<path d="M-46,-21 Q-25,-29 -6,-17 Q-9,3 -25,4 Q-44,2 -46,-21 Z" fill="{SKIN_SHADOW}" opacity="0.32"/>'
            f'<path d="M46,-21 Q25,-29 6,-17 Q9,3 25,4 Q44,2 46,-21 Z" fill="{SKIN_SHADOW}" opacity="0.35"/>'
            # Zarif elmacık altı yumuşak gölge
            f'<path d="M-55,18 L-38,29 L-30,54 L-50,44 Z" fill="{SKIN_SHADOW}" opacity="0.18"/>'
            f'<path d="M55,18 L38,29 L30,54 L50,44 Z" fill="{SKIN_SHADOW}" opacity="0.26"/>'
            # Alın + ince burun sırtı + elmacık üstü ışığı
            f'<path d="M-28,-48 Q0,-54 24,-44 Q14,-28 -12,-30 Z" fill="{SKIN_LIGHT}" opacity="0.54"/>'
            f'<path d="M-2.2,-12 L1.9,-12 L2.8,21 L-2.8,21 Z" fill="{SKIN_LIGHT}" opacity="0.68"/>'
            f'<path d="M2.2,-12 L7.6,21 L1.2,27 L-5.6,25 L-2.4,21 Z" fill="{SKIN_SHADOW}" opacity="0.22"/>'
            # Zarif elmacık üstü ışık ve sıcak şeftali-gül canlılığı
            f'<ellipse cx="-32" cy="14" rx="13" ry="6.5" fill="{SKIN_LIGHT}" opacity="0.46"/>'
            f'<ellipse cx="32" cy="14" rx="13" ry="6.5" fill="{SKIN_LIGHT}" opacity="0.36"/>'
            f'<ellipse cx="-31" cy="20" rx="14" ry="8" fill="#E09484" opacity="0.21"/>'
            f'<ellipse cx="31" cy="20" rx="14" ry="8" fill="#E09484" opacity="0.18"/>'
            # Çene altı hafif gölge
            f'<path d="M-32,76 Q0,90 32,76 L32,98 L-32,98 Z" fill="{SKIN_DEEP}" opacity="0.22"/>'
            # Saçın alına düşen yumuşak gölgesi
            f'<path d="M-58,-44 Q-22,-64 16,-64 Q44,-60 58,-38 L58,-94 L-58,-94 Z" fill="{SKIN_DEEP}" opacity="0.18"/>'
            f'<path d="M-55,-14 L-53,16 C-50,40 -40,60 -22,78" fill="none" stroke="#FFF8F2" stroke-width="2.2" opacity="0.36" stroke-linecap="round"/>'
        )
    elif view == "3q":
        inner.append(
            f'<path d="M40,-94 C54,-54 56,-16 54,18 C51,46 42,72 24,96 L84,96 L84,-94 Z" fill="{SKIN_SHADOW}" opacity="0.26"/>'
            f'<path d="M-54,16 C-38,22 -18,32 -14,48 C-22,64 -34,74 -46,60 Z" fill="url(#{gid_cheek})"/>'
            f'<path d="M-24,-21 Q-4,-29 15,-17 Q11,4 -5,5 Q-22,3 -24,-21 Z" fill="{SKIN_SHADOW}" opacity="0.32"/>'
            f'<path d="M26,-21 Q42,-28 57,-16 Q53,3 39,4 Q28,2 26,-21 Z" fill="{SKIN_SHADOW}" opacity="0.35"/>'
            f'<path d="M-28,-48 Q4,-56 32,-46 Q20,-28 -12,-30 Z" fill="{SKIN_LIGHT}" opacity="0.56"/>'
            f'<path d="M-38,8 Q-18,1 -4,10 Q-12,24 -32,20 Z" fill="{SKIN_LIGHT}" opacity="0.54"/>'
            f'<ellipse cx="-18" cy="21" rx="15" ry="8.5" fill="#E09484" opacity="0.22"/>'
            f'<path d="M-32,74 Q16,90 46,72 L46,98 L-32,98 Z" fill="{SKIN_DEEP}" opacity="0.24"/>'
            f'<path d="M-56,-34 C-42,-58 -10,-70 24,-68 C46,-66 60,-52 66,-30 L66,-94 L-56,-94 Z" fill="{SKIN_DEEP}" opacity="0.18"/>'
            f'<path d="M-54,-12 L-52,16 C-48,42 -36,64 -16,84" fill="none" stroke="#FFF8F2" stroke-width="2.2" opacity="0.34" stroke-linecap="round"/>'
        )
    else:  # side
        inner.append(
            f'<path d="M-64,14 C-42,24 -10,34 12,52 C24,68 34,84 54,94 L-64,98 Z" fill="{SKIN_SHADOW}" opacity="0.24"/>'
            f'<path d="M29,-21 Q47,-28 62,-16 Q58,4 43,4 Q32,2 29,-21 Z" fill="{SKIN_SHADOW}" opacity="0.34"/>'
            f'<path d="M46,-48 Q58,-38 60,-16 L50,-14 Q46,-34 39,-44 Z" fill="{SKIN_LIGHT}" opacity="0.54"/>'
            f'<ellipse cx="30" cy="22" rx="14" ry="8" fill="#E09484" opacity="0.20"/>'
            f'<path d="M60,-34 L62,-16 L76,22" fill="none" stroke="#FFF8F2" stroke-width="2.0" opacity="0.38" stroke-linecap="round"/>'
        )

    o.append(f'<g clip-path="url(#{cid_face})">{"".join(inner)}</g>')

    # ── 6. Yüz Ana Dış Konturu (2.0px — A-Y v3 uyumlu) ──
    o.append(f'<path d="{face_d}" fill="none" stroke="{INK}" stroke-width="2.0" stroke-linejoin="round"/>')

    # ── 7. Gözler + Yumuşak Zarif Kavisli Kestane Kaşlar ──
    for idx, (ex, ey, erx, ery, is_side, fl) in enumerate(eye_specs):
        o.append(_render_eye(ex, ey, erx, ery, lu, ll, lk, side=is_side, wet=is_wet, flip_lash=fl))
        if view == "front":
            sgn = -1 if ex < 0 else 1
            x_in = ex - sgn * (erx * 0.90)
            x_out = ex + sgn * (erx * 1.18)
            y_in = ey - ery * 1.84 + bi * 0.65
            y_out = ey - ery * 1.82 + bo * 0.65
            o.append(_render_brow(x_in, y_in, x_out, y_out, arch_y=-4.6, thick=3.6))
        elif view == "3q":
            if idx == 0:
                x_in, x_out = ex + erx * 0.92, ex - erx * 1.18
            else:
                x_in, x_out = ex - erx * 0.90, ex + erx * 1.10
            y_in = ey - ery * 1.84 + bi * 0.65
            y_out = ey - ery * 1.82 + bo * 0.65
            o.append(_render_brow(x_in, y_in, x_out, y_out, arch_y=-4.5, thick=3.6 if idx == 0 else 3.3))
        else:
            x_in, x_out = ex + erx * 1.08, ex - erx * 1.22
            y_in = ey - ery * 1.84 + bi * 0.65
            y_out = ey - ery * 1.82 + bo * 0.65
            o.append(_render_brow(x_in, y_in, x_out, y_out, arch_y=-4.0, thick=3.5))

    gx = 0.0 if view == "front" else (19.0 if view == "3q" else 56.0)
    if view != "side" and extra in ("frown", "worry"):
        op_g = 0.62 if extra == "frown" else 0.48
        o.append(
            f'<path d="M{gx - 2.4:.1f},-23.5 L{gx - 1.8:.1f},-16.5 M{gx + 2.4:.1f},-23.5 L{gx + 1.8:.1f},-16.5" '
            f'fill="none" stroke="{SKIN_DEEP}" stroke-width="1.1" opacity="{op_g}" stroke-linecap="round"/>'
        )

    # ── 8. Burun (v2: daha ince, narin ve zarif köprü/uç) ──
    if view == "front":
        o.append(
            f'<path d="M-2.8,-10 L-3.8,18" fill="none" stroke="{SKIN_SHADOW}" stroke-width="0.95" opacity="0.40" stroke-linecap="round"/>'
            f'<path d="M-7.2,22.2 Q-4.0,26.6 0,27.0 Q4.0,26.6 7.2,22.2" fill="none" stroke="{INK_SOFT}" stroke-width="1.35" stroke-linecap="round"/>'
            f'<path d="M-8.8,21.2 Q-9.4,24.4 -5.8,25.2 M8.8,21.2 Q9.4,24.4 5.8,25.2" fill="none" stroke="{INK_SOFT}" stroke-width="0.95" opacity="0.52" stroke-linecap="round"/>'
            f'<ellipse cx="-3.6" cy="25.0" rx="1.7" ry="0.82" fill="{SKIN_DEEP}" opacity="0.56"/>'
            f'<ellipse cx="3.6" cy="25.0" rx="1.7" ry="0.82" fill="{SKIN_DEEP}" opacity="0.56"/>'
        )
    elif view == "3q":
        o.append(
            f'<path d="M20.8,-11 L29.8,18.8 Q27.2,27.0 18.2,26.4 L16.0,22.0 Z" fill="{SKIN_SHADOW}" opacity="0.24"/>'
            f'<path d="M20.4,-11 Q25.0,4 29.6,18.4 Q30.8,23.6 25.4,26.4 Q21.2,27.4 17.6,25.6" '
            f'fill="none" stroke="{INK_SOFT}" stroke-width="1.55" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="M29.4,18.8 Q30.4,23.4 25.6,26.0" fill="none" stroke="{INK}" stroke-width="1.35" opacity="0.72" stroke-linecap="round"/>'
            f'<path d="M15.4,21.8 Q14.4,25.0 17.8,26.0" fill="none" stroke="{INK_SOFT}" stroke-width="1.05" opacity="0.62" stroke-linecap="round"/>'
            f'<ellipse cx="21.6" cy="25.4" rx="1.8" ry="0.85" fill="{SKIN_DEEP}" opacity="0.62"/>'
            f'<path d="M19.4,-8 L27.0,17.2" fill="none" stroke="#FFF8F2" stroke-width="1.5" opacity="0.54" stroke-linecap="round"/>'
        )
    else:
        o.append(
            f'<path d="M60.2,23.0 Q58.6,27.2 64.4,28.0" fill="none" stroke="{INK_SOFT}" stroke-width="1.15" opacity="0.70" stroke-linecap="round"/>'
            f'<ellipse cx="66.2" cy="26.8" rx="2.1" ry="0.9" fill="{SKIN_DEEP}" opacity="0.60"/>'
        )

    # ── 9. Philtrum + Dolgun Gül-Şeftali Dudak + Yumuşak Çene Vurgusu ──
    if view == "front":
        o.append(
            f'<path d="M-1.8,30.5 L-2.1,39.0 M1.8,30.5 L2.1,39.0" fill="none" stroke="{SKIN_SHADOW}" stroke-width="0.9" opacity="0.30" stroke-linecap="round"/>'
        )
    elif view == "3q":
        o.append(
            f'<path d="M22.8,30.5 L23.3,39.0" fill="none" stroke="{SKIN_SHADOW}" stroke-width="0.95" opacity="0.30" stroke-linecap="round"/>'
        )
    o.append(_render_mouth(mx, my, mw, mk, view))

    if view == "front":
        o.append(
            f'<path d="M-6,81 Q0,84 6,81" fill="none" stroke="{SKIN_DEEP}" stroke-width="0.95" opacity="0.28" stroke-linecap="round"/>'
        )
    elif view == "3q":
        o.append(
            f'<path d="M10,82 Q17,84 24,81" fill="none" stroke="{SKIN_DEEP}" stroke-width="0.95" opacity="0.28" stroke-linecap="round"/>'
        )

    # ── 10. İfade Ekstraları (yas gözyaşı) ──
    if extra == "tear":
        ex, ey = eye_specs[-1][0], eye_specs[-1][1]
        o.append(
            f'<path d="M{ex - 0.8:.1f},{ey + 8.5:.1f} Q{ex + 2.4:.1f},{ey + 22:.1f} {ex + 0.8:.1f},{ey + 34:.1f}" '
            f'fill="none" stroke="#D2EEFF" stroke-width="2.1" opacity="0.82" stroke-linecap="round"/>'
            f'<ellipse cx="{ex + 0.8:.1f}" cy="{ey + 38:.1f}" rx="2.3" ry="3.6" fill="#D6F0FF" stroke="#6898B5" stroke-width="1.0"/>'
            f'<circle cx="{ex:.1f}" cy="{ey + 36.6:.1f}" r="0.85" fill="#FFFFFF"/>'
        )

    # ── 11. Ön Katmanlı, Uçları İncelen Dalgalı Kestane-Kızıl Saç ──
    o.append(_hair_front(view, gid_hair))

    return "".join(o)


def _render_hand(cx: float, cy: float, scale: float, skin: str, skin_sh: str, mirror: bool = False) -> str:
    """Zarif ama anatomik yetişkin kadın eli (gevşek doğal duruş)."""
    sx = -scale if mirror else scale
    return (
        f'<g transform="translate({cx:.1f},{cy:.1f}) scale({sx:.3f},{scale:.3f})">'
        f'<path d="M-9,-4 C-11,8 -10,17 -8,23 L7,22 C10,15 11,6 9,-4 Z" fill="{skin}" stroke="{INK}" stroke-width="2.05" stroke-linejoin="round"/>'
        f'<path d="M-8,2 C-15,8 -16,17 -12,24 C-9,26 -6,23 -7,18 L-6,11" fill="{skin}" stroke="{INK}" stroke-width="1.95" stroke-linecap="round" stroke-linejoin="round"/>'
        f'<path d="M-7,21 L-8,38 C-8,41 -3.8,41 -3.8,38 L-3,22" fill="{skin}" stroke="{INK}" stroke-width="1.85" stroke-linejoin="round"/>'
        f'<path d="M-2.8,21 L-2.8,41 C-2.8,44 1.6,44 1.6,41 L1.6,22" fill="{skin}" stroke="{INK}" stroke-width="1.85" stroke-linejoin="round"/>'
        f'<path d="M1.8,21 L2.8,39 C2.8,42 7.0,42 7.0,39 L6.0,21" fill="{skin}" stroke="{INK}" stroke-width="1.85" stroke-linejoin="round"/>'
        f'<path d="M6.0,19 L7.8,33 C7.8,36 11.4,36 11.4,33 L9.6,18" fill="{skin_sh}" stroke="{INK}" stroke-width="1.75" stroke-linejoin="round"/>'
        f'<path d="M-3,4 L-2,16 M2,4 L3,16" fill="none" stroke="{skin_sh}" stroke-width="1.1" opacity="0.58" stroke-linecap="round"/>'
        f'</g>'
    )


def _render_stethoscope() -> str:
    """Boyunda gerçekçi doktor stetoskopu (esnek tüp + metal başlık + çift kulaklık)."""
    return (
        f'<path d="M-22,-438 C-28,-422 -33,-394 -33,-358 C-33,-336 -29,-318 -23,-306" '
        f'fill="none" stroke="{INK}" stroke-width="9.0" stroke-linecap="round"/>'
        f'<path d="M-22,-438 C-28,-422 -33,-394 -33,-358 C-33,-336 -29,-318 -23,-306" '
        f'fill="none" stroke="{STETH_TUBE}" stroke-width="5.4" stroke-linecap="round"/>'
        f'<path d="M-23,-434 C-29,-418 -34,-392 -34,-358" '
        f'fill="none" stroke="{STETH_HI}" stroke-width="1.45" opacity="0.72" stroke-linecap="round"/>'
        f'<path d="M21,-438 C29,-420 33,-392 33,-358 C33,-342 31,-330 27,-322" '
        f'fill="none" stroke="{INK}" stroke-width="9.0" stroke-linecap="round"/>'
        f'<path d="M21,-438 C29,-420 33,-392 33,-358 C33,-342 31,-330 27,-322" '
        f'fill="none" stroke="{STETH_TUBE}" stroke-width="5.4" stroke-linecap="round"/>'
        f'<path d="M20,-434 C28,-416 32,-390 32,-358" '
        f'fill="none" stroke="{STETH_HI}" stroke-width="1.45" opacity="0.70" stroke-linecap="round"/>'
        f'<path d="M27,-324 C21,-314 19,-302 21,-294 M27,-324 C35,-314 37,-302 35,-294" '
        f'fill="none" stroke="{INK}" stroke-width="5.0" stroke-linecap="round"/>'
        f'<path d="M27,-324 C21,-314 19,-302 21,-294 M27,-324 C35,-314 37,-302 35,-294" '
        f'fill="none" stroke="{STETH_METAL}" stroke-width="2.3" stroke-linecap="round"/>'
        f'<circle cx="21" cy="-293" r="3.3" fill="{STETH_TUBE}" stroke="{INK}" stroke-width="1.3"/>'
        f'<circle cx="35" cy="-293" r="3.3" fill="{STETH_TUBE}" stroke="{INK}" stroke-width="1.3"/>'
        f'<circle cx="-21" cy="-301" r="10.0" fill="{STETH_MDARK}" stroke="{INK}" stroke-width="2.0"/>'
        f'<circle cx="-21" cy="-301" r="7.2" fill="{STETH_METAL}" stroke="{INK}" stroke-width="1.1"/>'
        f'<circle cx="-21" cy="-301" r="3.1" fill="{STETH_MDARK}"/>'
        f'<path d="M-26,-305 Q-21,-309 -16,-305" fill="none" stroke="#FFFFFF" stroke-width="1.45" opacity="0.78" stroke-linecap="round"/>'
    )


def figur_sara(ifade: str = "odak") -> str:
    """Tam boy Dr. Sara Tancredi v2 (Fox River Revir — Stil B + A hibrit, A-Y v3 uyumlu).
    Ayak tabanı y=0, toplam boy ~540 (y: -540 .. 0). Doğal 3/4 duruş, sağa bakar.
    Arka saç katmanı omuz ve boynun arkasında çizilir; boyun + yaka + stetoskop tam ve net görünür (R4).
    """
    o: list[str] = []

    gid_coat = _uid("coatg")
    gid_scrub = _uid("scrubg")
    gid_pt = _uid("sptg")
    cid_cr = _uid("coatrc")

    coat_right = (
        "M22,-436 C36,-428 50,-422 56,-412 C58,-372 52,-326 48,-290 "
        "C56,-250 60,-196 58,-142 C38,-136 22,-136 10,-140 "
        "L14,-288 L18,-394 Z"
    )

    o.append(
        f'<defs>'
        f'<linearGradient id="{gid_coat}" x1="0.12" y1="0.06" x2="0.92" y2="0.94">'
        f'<stop offset="0%" stop-color="{COAT_LIGHT}"/>'
        f'<stop offset="46%" stop-color="{COAT_BASE}"/>'
        f'<stop offset="100%" stop-color="{COAT_MID}"/>'
        f'</linearGradient>'
        f'<linearGradient id="{gid_scrub}" x1="0.1" y1="0.0" x2="0.9" y2="1.0">'
        f'<stop offset="0%" stop-color="{SCRUB_LIGHT}"/>'
        f'<stop offset="48%" stop-color="{SCRUB_BASE}"/>'
        f'<stop offset="100%" stop-color="{SCRUB_DARK}"/>'
        f'</linearGradient>'
        f'<linearGradient id="{gid_pt}" x1="0.15" y1="0.0" x2="0.85" y2="1.0">'
        f'<stop offset="0%" stop-color="{PANTS_LIGHT}"/>'
        f'<stop offset="48%" stop-color="{PANTS_BASE}"/>'
        f'<stop offset="100%" stop-color="{PANTS_DARK}"/>'
        f'</linearGradient>'
        f'<clipPath id="{cid_cr}"><path d="{coat_right}"/></clipPath>'
        f'</defs>'
    )

    o.append('<ellipse cx="4" cy="4" rx="80" ry="12" fill="#000000" opacity="0.34"/>')

    # ── 0. Arka Saç Katmanı (omuz ve boynun arkasında) ──
    o.append(
        f'<g transform="translate(6,-488) scale(0.475)">'
        f'{_hair_back("3q")}'
        f'</g>'
    )

    # ── 1. Bacaklar & Sade Koyu Doktor Ayakkabıları ──
    leg_back = (
        "M-36,-250 L-39,-132 C-40,-116 -37,-86 -34,-22 L-6,-22 "
        "C-4,-86 -4,-116 -6,-136 L-2,-250 Z"
    )
    o.append(
        f'<path d="{leg_back}" fill="{PANTS_DARK}" stroke="{INK}" stroke-width="2.1" stroke-linejoin="round"/>'
        f'<path d="M-32,-140 Q-20,-135 -10,-142 M-28,-34 Q-18,-30 -10,-36" fill="none" stroke="#131820" stroke-width="1.4" opacity="0.65" stroke-linecap="round"/>'
        f'<path d="M-36,-24 L-6,-24 C6,-20 15,-12 15,-2 L-38,-2 Z" fill="{SHOE_BASE}" stroke="{INK}" stroke-width="2.1" stroke-linejoin="round"/>'
        f'<path d="M-38,-6 L15,-6 L15,-1 L-38,-1 Z" fill="{SHOE_SOLE}"/>'
    )

    leg_front = (
        "M-2,-250 L3,-134 C5,-116 12,-82 19,-18 L48,-18 "
        "C45,-82 42,-116 40,-136 L39,-250 Z"
    )
    o.append(
        f'<path d="{leg_front}" fill="url(#{gid_pt})" stroke="{INK}" stroke-width="2.1" stroke-linejoin="round"/>'
        f'<path d="M6,-238 L12,-136 L22,-26" fill="none" stroke="#4D5E74" stroke-width="2.8" opacity="0.26" stroke-linecap="round"/>'
        f'<path d="M8,-138 Q22,-131 37,-142 M19,-32 Q32,-27 45,-34" fill="none" stroke="#161C26" stroke-width="1.4" opacity="0.62" stroke-linecap="round"/>'
        f'<path d="M17,-20 L48,-20 C62,-16 74,-9 74,2 L15,2 Z" fill="{SHOE_BASE}" stroke="{INK}" stroke-width="2.1" stroke-linejoin="round"/>'
        f'<path d="M15,-4 L74,-4 L74,2 L15,2 Z" fill="{SHOE_SOLE}"/>'
        f'<path d="M48,-15 Q62,-12 69,-6" fill="none" stroke="#4D4540" stroke-width="1.4" opacity="0.52" stroke-linecap="round"/>'
    )

    # ── 2. Uzak Kol ──
    sleeve_l = (
        "M-50,-418 C-64,-406 -74,-370 -76,-324 C-78,-292 -76,-262 -72,-234 "
        "L-48,-236 C-46,-268 -44,-302 -44,-334 C-42,-368 -40,-396 -38,-414 Z"
    )
    o.append(
        _render_hand(-60, -234, 0.82, SKIN_MID, SKIN_SHADOW, mirror=True)
        + f'<path d="{sleeve_l}" fill="{COAT_MID}" stroke="{INK}" stroke-width="2.1" stroke-linejoin="round"/>'
        f'<path d="M-74,-322 Q-60,-316 -46,-322 M-73,-246 Q-60,-242 -48,-246" fill="none" stroke="{COAT_DARK}" stroke-width="1.4" opacity="0.72" stroke-linecap="round"/>'
    )

    # ── 3. İç Petrol-Mavi Doktor Scrub Üstü ──
    scrub_d = "M-36,-432 L34,-432 L38,-248 Q2,-240 -38,-248 Z"
    o.append(
        f'<path d="{scrub_d}" fill="url(#{gid_scrub})" stroke="{INK}" stroke-width="1.8" stroke-linejoin="round"/>'
        f'<path d="M-18,-364 Q4,-356 26,-364 M-22,-294 Q2,-286 24,-294" fill="none" stroke="{SCRUB_DARK}" stroke-width="1.4" opacity="0.64" stroke-linecap="round"/>'
    )

    # ── 4. Kırık-Beyaz Doktor Önlüğü ──
    coat_left = (
        "M-20,-436 C-34,-428 -48,-422 -54,-412 C-56,-372 -50,-326 -46,-290 "
        "C-54,-250 -58,-196 -56,-142 C-34,-136 -10,-136 8,-140 "
        "L2,-288 L-6,-394 Z"
    )
    o.append(
        f'<path d="{coat_left}" fill="url(#{gid_coat})"/>'
        f'<path d="M-52,-404 C-40,-372 -38,-324 -42,-284 C-48,-244 -50,-192 -48,-146" fill="none" stroke="#FFFFFF" stroke-width="4.2" opacity="0.45" stroke-linecap="round"/>'
        f'<path d="M-44,-284 Q-22,-276 -2,-284 M-52,-196 Q-24,-186 2,-194" fill="none" stroke="{COAT_DARK}" stroke-width="1.4" opacity="0.62" stroke-linecap="round"/>'
        f'<path d="M-40,-376 L-12,-376 L-12,-344 Q-26,-339 -40,-344 Z" fill="{COAT_MID}" opacity="0.44" stroke="{INK}" stroke-width="1.5" stroke-linejoin="round"/>'
        f'<path d="M-40,-369 L-12,-369" fill="none" stroke="{COAT_DARK}" stroke-width="1.15" opacity="0.72"/>'
        f'<path d="M-19,-376 L-16,-392 L-13,-392 L-15,-376 Z" fill="#3B688C" stroke="{INK}" stroke-width="1.15"/>'
        f'<path d="M-16,-389 L-14,-378" fill="none" stroke="#D2DCE4" stroke-width="1.1"/>'
        f'<rect x="-39" y="-370" width="19" height="24" rx="2.2" fill="#F2F4F7" stroke="{INK}" stroke-width="1.3"/>'
        f'<rect x="-39" y="-370" width="19" height="5.5" rx="1.2" fill="{SCRUB_BASE}"/>'
        f'<rect x="-36" y="-362" width="6.5" height="7.5" rx="1" fill="#C9A892"/>'
        f'<path d="M-28,-360 H-22 M-28,-356 H-22 M-36,-350 H-22" fill="none" stroke="#4D5B6B" stroke-width="1.05"/>'
        f'<path d="M-48,-244 L-12,-244 L-10,-200 Q-29,-194 -49,-200 Z" fill="{COAT_MID}" opacity="0.34" stroke="{INK}" stroke-width="1.45" stroke-linejoin="round"/>'
        f'<path d="{coat_left}" fill="none" stroke="{INK}" stroke-width="2.1" stroke-linejoin="round"/>'
        f'<path d="{coat_right}" fill="{COAT_MID}"/>'
        f'<g clip-path="url(#{cid_cr})">'
        f'<path d="M36,-436 C46,-386 46,-324 44,-280 C50,-238 52,-188 50,-138 L64,-138 L64,-436 Z" fill="{COAT_DARK}" opacity="0.46"/>'
        f'</g>'
        f'<path d="M22,-244 L50,-244 L52,-200 Q36,-194 21,-200 Z" fill="{COAT_DARK}" opacity="0.32" stroke="{INK}" stroke-width="1.45" stroke-linejoin="round"/>'
        f'<path d="{coat_right}" fill="none" stroke="{INK}" stroke-width="2.1" stroke-linejoin="round"/>'
        f'<circle cx="-1" cy="-340" r="2.6" fill="#F8F6F1" stroke="{INK}" stroke-width="1.1"/>'
        f'<circle cx="1" cy="-296" r="2.6" fill="#F8F6F1" stroke="{INK}" stroke-width="1.1"/>'
        f'<circle cx="3" cy="-252" r="2.6" fill="#F8F6F1" stroke="{INK}" stroke-width="1.1"/>'
    )

    # ── 5. R4: Zarif Anatomik Boyun + Köprücük + Scrub + Önlük Yakası ──
    o.append(
        f'<path d="M-24,-438 Q2,-450 26,-438 L23,-424 Q2,-432 -21,-424 Z" fill="{COAT_MID}" stroke="{INK}" stroke-width="1.95" stroke-linejoin="round"/>'
    )
    o.append(
        f'<path d="M-19,-430 L4,-394 L22,-430 L17,-430 L4,-404 L-14,-430 Z" fill="{SCRUB_DARK}" stroke="{INK}" stroke-width="1.45" stroke-linejoin="round"/>'
    )
    neck_d = (
        "M-14,-468 L-16,-436 C-16,-426 -9,-414 3,-403 "
        "C13,-414 17,-426 16,-436 L13,-464 Z"
    )
    o.append(
        f'<path d="{neck_d}" fill="{SKIN_BASE}"/>'
        f'<path d="M2,-466 L14,-464 L16,-434 C14,-422 9,-412 3,-404 L2,-434 Z" fill="{SKIN_SHADOW}" opacity="0.42"/>'
        f'<path d="M-14,-468 L14,-464 L15,-446 Q1,-436 -15,-448 Z" fill="{SKIN_DEEP}" opacity="0.52"/>'
        f'<path d="M-12,-454 Q-5,-438 2,-420 M10,-452 Q8,-438 6,-422" fill="none" stroke="{SKIN_SHADOW}" stroke-width="1.3" opacity="0.48" stroke-linecap="round"/>'
        f'<path d="M-11,-420 Q-4,-416 1,-418 M11,-420 Q6,-416 2,-418" fill="none" stroke="{SKIN_DEEP}" stroke-width="1.2" opacity="0.50" stroke-linecap="round"/>'
        f'<path d="M-14,-468 L-16,-436 M13,-464 L16,-436" fill="none" stroke="{INK}" stroke-width="2.0" stroke-linecap="round"/>'
    )
    o.append(
        f'<path d="M-24,-438 L-15,-430 L-6,-392 L-24,-402 L-19,-412 L-28,-416 Z" fill="{COAT_LIGHT}" stroke="{INK}" stroke-width="1.95" stroke-linejoin="round"/>'
        f'<path d="M26,-438 L18,-430 L16,-392 L32,-404 L26,-414 L34,-418 Z" fill="{COAT_BASE}" stroke="{INK}" stroke-width="1.95" stroke-linejoin="round"/>'
        f'<path d="M-24,-400 L-6,-390 M16,-390 L32,-402" fill="none" stroke="{COAT_DARK}" stroke-width="1.9" opacity="0.55" stroke-linecap="round"/>'
    )

    # ── 6. Boyunda Gerçekçi Stetoskop ──
    o.append(_render_stethoscope())

    # ── 7. Baş (yüz + ön saç tutamları) ──
    o.append(
        f'<g transform="translate(6,-488) scale(0.475)">'
        f'{kafa_sara(view="3q", ifade=ifade, look=0.25, boyun=False, arka_sac=False)}'
        f'</g>'
    )

    # ── 8. Yakın Kol ──
    sleeve_r = (
        "M54,-412 C68,-400 76,-368 78,-322 C78,-290 74,-258 68,-228 "
        "L45,-230 C44,-264 44,-300 44,-334 C44,-364 44,-386 44,-396 C48,-404 51,-409 54,-412 Z"
    )
    o.append(
        _render_hand(57, -228, 0.85, SKIN_BASE, SKIN_SHADOW, mirror=False)
        + f'<path d="{sleeve_r}" fill="url(#{gid_coat})"/>'
        f'<path d="M54,-412 C68,-400 76,-368 78,-322 C78,-290 74,-258 68,-228 L45,-230 C44,-264 44,-300 44,-334 C44,-364 44,-386 44,-396" '
        f'fill="none" stroke="{INK}" stroke-width="2.1" stroke-linejoin="round" stroke-linecap="round"/>'
        f'<path d="M44,-396 C47,-405 50,-410 54,-412" fill="none" stroke="{COAT_DARK}" stroke-width="1.4" opacity="0.72" stroke-linecap="round"/>'
        f'<path d="M58,-398 C66,-372 68,-342 66,-316 M48,-318 Q60,-312 74,-318 M46,-242 Q58,-238 68,-242" '
        f'fill="none" stroke="{COAT_DARK}" stroke-width="1.4" opacity="0.62" stroke-linecap="round"/>'
        f'<path d="M49,-386 L48,-248" fill="none" stroke="#FFFFFF" stroke-width="2.8" opacity="0.34" stroke-linecap="round"/>'
    )

    return "".join(o)


def _portre_revir_anahtar() -> str:
    """Alt sağ panel için sinematik yakın plan omuz-portre (v2):
    Revir sıcak koridor ışığında, kapı aralığı atmosferi ve ince parmaklı, anatomik eklemli
    zarif kadın elinde tutulan INF-04 pirinç revir anahtarı.
    """
    gid_warm = _uid("rwarm")
    gid_beam = _uid("rbeam")
    gid_key = _uid("rkey")
    gid_kglow = _uid("rkglow")
    gid_hand = _uid("rhand")

    return (
        f'<defs>'
        f'<radialGradient id="{gid_warm}" cx="0.24" cy="0.46" r="0.66">'
        f'<stop offset="0%" stop-color="{WARM_LIGHT}" stop-opacity="0.40"/>'
        f'<stop offset="50%" stop-color="#D99652" stop-opacity="0.14"/>'
        f'<stop offset="100%" stop-color="#141B23" stop-opacity="0.0"/>'
        f'</radialGradient>'
        f'<linearGradient id="{gid_beam}" x1="0.0" y1="0.3" x2="1.0" y2="0.65">'
        f'<stop offset="0%" stop-color="#FFE6B5" stop-opacity="0.36"/>'
        f'<stop offset="55%" stop-color="{WARM_LIGHT}" stop-opacity="0.12"/>'
        f'<stop offset="100%" stop-color="{WARM_LIGHT}" stop-opacity="0.0"/>'
        f'</linearGradient>'
        f'<linearGradient id="{gid_key}" x1="0.0" y1="0.0" x2="1.0" y2="1.0">'
        f'<stop offset="0%" stop-color="#F6DFA6"/>'
        f'<stop offset="52%" stop-color="#C89F58"/>'
        f'<stop offset="100%" stop-color="#7B5C29"/>'
        f'</linearGradient>'
        f'<radialGradient id="{gid_kglow}" cx="0.5" cy="0.5" r="0.5">'
        f'<stop offset="0%" stop-color="{WARM_LIGHT}" stop-opacity="0.24"/>'
        f'<stop offset="60%" stop-color="{WARM_LIGHT}" stop-opacity="0.06"/>'
        f'<stop offset="100%" stop-color="{WARM_LIGHT}" stop-opacity="0.0"/>'
        f'</radialGradient>'
        f'<linearGradient id="{gid_hand}" x1="0.0" y1="0.1" x2="0.95" y2="0.9">'
        f'<stop offset="0%" stop-color="{SKIN_LIGHT}"/>'
        f'<stop offset="48%" stop-color="{SKIN_BASE}"/>'
        f'<stop offset="100%" stop-color="{SKIN_MID}"/>'
        f'</linearGradient>'
        f'</defs>'
        f'<rect x="-432" y="-104" width="864" height="208" fill="url(#{gid_warm})"/>'
        # Sol: aralık bırakılmış revir kapısı ve sıcak ışık huzmesi
        f'<rect x="-420" y="-104" width="114" height="208" fill="#10151C"/>'
        f'<path d="M-306,-104 L-264,-104 L-264,104 L-306,104 Z" fill="#F8D99B" opacity="0.24"/>'
        f'<path d="M-264,-104 L-252,-104 L-252,104 L-264,104 Z" fill="#1E2733" stroke="#2D3B4C" stroke-width="1.2"/>'
        f'<path d="M-306,-96 L120,-42 L120,104 L-306,104 Z" fill="url(#{gid_beam})"/>'
        f'<path d="M190,-90 H415 M190,-30 H415 M190,30 H415 M285,-96 V96 M365,-96 V96" '
        f'fill="none" stroke="{WARM_LIGHT}" stroke-width="0.7" opacity="0.11"/>'
        f'<rect x="-324" y="4" width="15" height="32" rx="3" fill="#2A3340" stroke="#4D5C6E" stroke-width="1.1"/>'
        f'<circle cx="-316" cy="20" r="3.0" fill="#8C99A8"/>'
        # Orta: Sara'nın yakın plan omuz-portresi (kararlı ifade — kapıyı açık bırakma anı)
        f'<g transform="translate(8, 492) scale(1.04)">'
        f'{figur_sara(ifade="kararli")}'
        f'</g>'
        # Sağ ön plan: Zarif, ince parmaklı, anatomik eklemli kadın eli + INF-04 revir anahtarı
        f'<g transform="translate(262, 34) rotate(-6)">'
        f'<circle cx="-22" cy="-4" r="78" fill="url(#{gid_kglow})"/>'
        # Arka kıvrılan parmaklar (yüzük + serçe — zarif anatomik gölgeli)
        f'<path d="M4,18 C16,18 28,20 40,22 C44,24 44,30 38,32 C24,33 12,32 2,28 C-3,26 -2,19 4,18 Z" '
        f'fill="{SKIN_SHADOW}" stroke="{INK}" stroke-width="1.65" stroke-linejoin="round"/>'
        f'<path d="M-2,10 C12,10 28,12 44,16 C49,18 48,25 41,26 C26,26 12,24 -2,20 C-8,18 -8,11 -2,10 Z" '
        f'fill="{SKIN_MID}" stroke="{INK}" stroke-width="1.75" stroke-linejoin="round"/>'
        # Pirinç revir anahtarı + halka + INF-04 etiketi (işaret ve başparmak arasında)
        f'<g transform="translate(-40, 4) rotate(-20)">'
        f'<circle cx="-30" cy="0" r="10.2" fill="none" stroke="#BAC6D0" stroke-width="2.1"/>'
        f'<circle cx="-30" cy="0" r="10.2" fill="none" stroke="{INK}" stroke-width="0.8"/>'
        f'<rect x="-60" y="6" width="32" height="14" rx="2.5" fill="#2A3644" stroke="{INK}" stroke-width="1.35" transform="rotate(14 -44 13)"/>'
        f'<text x="-44" y="16" text-anchor="middle" font-family="Consolas, DejaVu Sans Mono, monospace" font-size="6.2" fill="#E8D2A0" transform="rotate(14 -44 13)">INF-04</text>'
        f'<circle cx="-12" cy="0" r="13.2" fill="url(#{gid_key})" stroke="{INK}" stroke-width="1.85"/>'
        f'<circle cx="-15" cy="0" r="4.8" fill="#171F2A" stroke="{INK}" stroke-width="1.35"/>'
        f'<path d="M1,-3.6 L48,-3.6 L52,0 L48,3.6 L41,3.6 L41,11.2 L34,11.2 L34,4.8 L27,4.8 L27,12.2 L20,12.2 L20,3.6 L1,3.6 Z" '
        f'fill="url(#{gid_key})" stroke="{INK}" stroke-width="1.75" stroke-linejoin="round"/>'
        f'<path d="M5,-1.1 L44,-1.1" fill="none" stroke="#FFF4D0" stroke-width="1.25" opacity="0.72" stroke-linecap="round"/>'
        f'</g>'
        # El sırtı + ince zarif işaret parmağı (eklem boğumlarıyla)
        f'<path d="M-20,-6 C-10,-12 4,-14 20,-13 C34,-12 48,-11 64,-8 L108,-2 L106,32 L62,30 '
        f'C44,28 28,22 14,14 C2,8 -10,4 -20,1 C-24,-1 -24,-4 -20,-6 Z" '
        f'fill="url(#{gid_hand})" stroke="{INK}" stroke-width="1.85" stroke-linejoin="round"/>'
        # İşaret parmağı eklem çizgileri + zarif tırnak ipucu
        f'<path d="M-19,-3.5 C-15,-5.5 -11,-4.5 -11,-2.2 C-11,-0.2 -15,0.2 -19,-1.5 Z" fill="#F6DFD2" stroke="{SKIN_SHADOW}" stroke-width="0.8"/>'
        f'<path d="M0,-9.5 Q1,-5 0,-1 M18,-9.5 Q19,-4.5 18,0" fill="none" stroke="{SKIN_SHADOW}" stroke-width="1.05" opacity="0.58" stroke-linecap="round"/>'
        f'<path d="M40,-7 Q44,4 42,16" fill="none" stroke="{SKIN_SHADOW}" stroke-width="1.1" opacity="0.44" stroke-linecap="round"/>'
        # Başparmak (anahtar başını narinçe kavrayan, ince eklemli)
        f'<path d="M-26,6 C-16,-1 -2,-4 14,-2 C24,0 32,6 28,12 C23,17 10,15 -4,14 C-14,13 -22,13 -26,11 C-29,10 -29,8 -26,6 Z" '
        f'fill="{SKIN_LIGHT}" stroke="{INK}" stroke-width="1.8" stroke-linejoin="round"/>'
        f'<path d="M-25,7.5 C-21,6.2 -17,6.8 -17,8.8 C-17,10.2 -21,10.6 -25,9.5 Z" fill="#FCE6DA" stroke="{SKIN_SHADOW}" stroke-width="0.75"/>'
        f'<path d="M-6,1 Q-5,5 -7,10" fill="none" stroke="{SKIN_SHADOW}" stroke-width="1.0" opacity="0.52" stroke-linecap="round"/>'
        # İnce bilek + doktor önlüğü manşet ucu
        f'<path d="M88,-14 L152,-8 L150,44 L82,38 Z" fill="{COAT_BASE}" stroke="{INK}" stroke-width="2.0" stroke-linejoin="round"/>'
        f'<path d="M94,-10 L88,34" fill="none" stroke="{COAT_DARK}" stroke-width="1.5" opacity="0.65"/>'
        f'<circle cx="106" cy="24" r="2.6" fill="#F8F6F1" stroke="{INK}" stroke-width="1.05"/>'
        f'</g>'
    )


def build_model_card_svg() -> str:
    """1280x720 Dr. Sara Tancredi Model Kartı v2 (as_sara_v2.png)."""
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
    parts.append(f'<path d="{" ".join(grid)}" fill="none" stroke="{PLAN_ACCENT}" stroke-width="0.6" opacity="0.045"/>')

    parts.append(
        '<text x="28" y="34" font-family="Segoe UI, DejaVu Sans, sans-serif" font-weight="700" font-size="18" fill="#E8EEF5" letter-spacing="1.0">'
        'SARA TANCREDI · FOX RIVER REVİR MODEL KARTI v2</text>'
        '<text x="546" y="33" font-family="Segoe UI, DejaVu Sans, sans-serif" font-size="12.5" fill="#9EC0A2">'
        'STİL B+A HİBRİT · ZARİF PORTRE &amp; SAÇ REVİZYONU</text>'
    )
    swatches = [
        (SKIN_BASE, "TEN"),
        (HAIR_BASE, "SAÇ"),
        (IRIS_BASE, "GÖZ"),
        (SCRUB_BASE, "SCRUB"),
        (COAT_BASE, "ÖNLÜK"),
    ]
    for i, (col, lbl) in enumerate(swatches):
        sx = 890 + i * 74
        parts.append(
            f'<rect x="{sx}" y="16" width="15" height="15" rx="3" fill="{col}" stroke="#44566B" stroke-width="1"/>'
            f'<text x="{sx + 20}" y="27.5" font-family="Segoe UI, DejaVu Sans, sans-serif" font-size="10" fill="#9BB0C5">{lbl}</text>'
        )

    # ── SOL PANEL: Tam Boy Dr. Sara Tancredi ──
    parts.append(
        '<rect x="24" y="54" width="350" height="642" rx="12" fill="#171F2A" stroke="#2C3B4D" stroke-width="1.4"/>'
        '<ellipse cx="199" cy="360" rx="150" ry="275" fill="url(#spotL)"/>'
        '<path d="M44,126 H354 M44,376 H354 M44,648 H354" fill="none" stroke="#7FE6FF" stroke-width="0.7" opacity="0.14" stroke-dasharray="4,5"/>'
        f'<g transform="translate(196,648) scale(0.95)">{figur_sara(ifade="odak")}</g>'
        '<text x="199" y="680" text-anchor="middle" font-family="Segoe UI, DejaVu Sans, sans-serif" font-weight="600" font-size="13" fill="#C9D6E4">'
        'DR. SARA TANCREDI · FOX RIVER REVİR</text>'
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
            f'<g transform="translate({cx},158) scale(0.58)">{kafa_sara(view=vw, ifade="odak", look=lk, boyun=True)}</g>'
            f'<text x="{cx}" y="264" text-anchor="middle" font-family="Segoe UI, DejaVu Sans, sans-serif" font-size="12" fill="#C4D3E2">{lbl}</text>'
        )

    # ── ORTA SAĞ PANEL: 5 İfade ──
    parts.append(
        '<rect x="392" y="288" width="864" height="190" rx="12" fill="#171F2A" stroke="#2C3B4D" stroke-width="1.4"/>'
        '<text x="410" y="310" font-family="Segoe UI, DejaVu Sans, sans-serif" font-weight="600" font-size="11.5" fill="#7F98B2" letter-spacing="1">'
        'BEŞ İFADE (ODAK · ŞEFKAT · ENDİŞE / KORKU · KARARLI · YAS)</text>'
    )
    exps = [
        ("odak", "odak (doktor)", "#C4D3E2"),
        ("sefkat", "şefkat", "#E9C7A8"),
        ("endise", "endişe / korku", "#C4D3E2"),
        ("kararli", "kararlı (revir)", WARM_LIGHT),
        ("yas", "yas", "#C4D3E2"),
    ]
    for idx, (ek, elbl, col) in enumerate(exps):
        cx = 482 + idx * 171
        parts.append(
            f'<g transform="translate({cx},384) scale(0.47)">{kafa_sara(view="3q", ifade=ek, look=0.25, boyun=False)}</g>'
            f'<text x="{cx}" y="464" text-anchor="middle" font-family="Segoe UI, DejaVu Sans, sans-serif" font-weight="{"600" if ek in ("kararli", "sefkat") else "500"}" font-size="12" fill="{col}">{elbl}</text>'
        )

    # ── ALT SAĞ PANEL: Yakın Plan Omuz-Portre ──
    parts.append(
        '<rect x="392" y="490" width="864" height="206" rx="12" fill="#131B25" stroke="#5A4B38" stroke-width="1.5"/>'
        f'<g clip-path="url(#clipPortre)"><g transform="translate(824,593)">{_portre_revir_anahtar()}</g></g>'
        '<rect x="402" y="498" width="356" height="22" rx="5" fill="#0E151E" opacity="0.84"/>'
        '<text x="410" y="513" font-family="Segoe UI, DejaVu Sans, sans-serif" font-weight="600" font-size="10.8" fill="#F4C57A" letter-spacing="0.6">'
        'YAKIN PLAN OMUZ-PORTRE · REVİR IŞIĞI &amp; KAPI ARALIĞI</text>'
    )

    parts.append('</svg>')
    return "".join(parts)


def build_r13_svg() -> str:
    """1280x720 R13 %200 Kırpma Kartı v2 (as_sara_r13_v2.png) — 4 yakın kontrol paneli."""
    W, H = 1280, 720
    panels = [
        (20, 48, 610, 316, "1. 3/4 ODAK — YÜZ YAKIN (%200)", False),
        (650, 48, 610, 316, "2. ÖNDEN — YÜZ YAKIN (%200)", False),
        (20, 384, 610, 316, "3. KARARLI İFADESİ — YÜZ YAKIN (%200)", True),
        (650, 384, 610, 316, "4. BOYUN / YAKA / STETOSKOP / OMUZ (%200)", False),
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
        'R13 · %200 YAKIN KONTROL KARTI — SARA TANCREDI v2</text>'
        '<text x="1256" y="30" text-anchor="end" font-family="Segoe UI, DejaVu Sans, sans-serif" font-size="12" fill="#9EC0A2">'
        'R1 / R3 / R4 / R10 / R13 · ZARİF PORTRE + TAPERED SAÇ + STETOSKOP</text>'
    )

    contents = [
        f'<g transform="translate(325,204) scale(1.16)">{kafa_sara(view="3q", ifade="odak", look=0.25, boyun=True)}</g>',
        f'<g transform="translate(955,204) scale(1.16)">{kafa_sara(view="front", ifade="odak", look=0.0, boyun=True)}</g>',
        f'<g transform="translate(325,540) scale(1.16)">{kafa_sara(view="3q", ifade="kararli", look=0.25, boyun=True)}</g>',
        f'<g transform="translate(960,1148) scale(1.44)">{figur_sara(ifade="odak")}</g>',
    ]

    for i, (px, py, pw, ph, title, is_w) in enumerate(panels):
        stroke = "#6D563B" if is_w else "#2C3B4D"
        tcol = WARM_LIGHT if is_w else "#9CB2C8"
        parts.append(
            f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="10" fill="#161E29" stroke="{stroke}" stroke-width="1.5"/>'
            f'<g clip-path="url(#pclip{i})">{contents[i]}</g>'
            f'<rect x="{px+10}" y="{py+10}" width="{min(pw - 20, len(title)*7.1 + 18):.0f}" height="24" rx="5" fill="#0F151D" opacity="0.86"/>'
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
    render_svg_to_png(build_model_card_svg(), OUT_DIR / "as_sara_v2.png")
    render_svg_to_png(build_r13_svg(), OUT_DIR / "as_sara_r13_v2.png")


if __name__ == "__main__":
    main()
