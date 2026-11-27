"""A-Ç: 11 Yaş Michael Scofield — Sinematik 2D Model ve R13 Kartı Üreticisi (v3).

Stil B + A hibrit (A-Y yetişkin model kartıyla tam hizalı ince kontur + yüz düzlem gölgelemesi).
İleride `karakter.py` içine doğrudan entegre edilebilecek temiz fonksiyonlar:
  - kafa_cocuk(view="3q", ifade="odak", look=0.25, lighting="studio", boyun=False)
  - figur_cocuk(ifade="odak", lighting="studio")

Kurallar:
  - R1: Hiçbir gerçek oyuncunun yüzü kopyalanmaz; yalnızca genel imza özellikler
        (buz-mavisi/gri-yeşil göz #7EB6BE, koyu düz kaş karakteri, zeki/gözlemci bakış).
  - R3: 11 yaş Michael'da dövme YOKTUR.
  - R4: Kafa gövdeye sağlam, anatomik boyun + klavikula/omuz eğimi + yaka ribanası ile bağlanır.
  - R10 & G1: Çizgi film sevimliliği yok; A-Y ile aynı ince kontur, yüz düzlem gölgeleri,
        sakin hafif ağır kapaklı (hooded) badem göz, tek küçük ışık yansıması.
  - D2: Doğal 11 yaş kol boyu ve dirsekte hafif kırık/eğim.
  - Çizgi olan her <path> öğesinde mutlaka fill="none" bulunur.
"""
from io import BytesIO
from pathlib import Path
import resvg_py
from PIL import Image

OUT_DIR = Path(__file__).resolve().parent

# ── Renk Paleti (A-Y yetişkin Michael ile tam hizalı ten, saç ve #7EB6BE buz-mavi göz)
INK = "#1B1512"
INK_SOFT = "#352923"
PLAN = "#7FE6FF"

PAL = dict(
    skin="#D9A887",
    skin_hi="#ECC6AA",
    skin_sh="#B88467",
    skin_dk="#8C5D46",
    skin_deep="#6B4332",
    blush="#C87E6A",
    lip="#B26E5E",
    lip_sh="#8E5245",
    iris="#7EB6BE",       # Yetişkin Michael ile tam eşit buz-mavisi / gri-yeşil
    iris_dk="#36555E",
    iris_hi="#B2DCE2",
    sclera="#EFECE6",
    sclera_sh="#C9CDD2",
    brow="#271E19",
    hair="#332721",
    hair_dk="#1F1713",
    hair_hi="#544237",
    hair_rim="#8AA6BC",
    shirt="#B24C37",
    shirt_sh="#843425",
    shirt_dk="#5E2318",
    shirt_hi="#C9654F",
    stripe="#E5D5B8",
    stripe_sh="#B9A486",
    pants="#324052",
    pants_sh="#202A37",
    pants_hi="#495B72",
    shoe="#292422",
    shoe_sh="#181514",
    shoe_sole="#DAD3C6",
    shoe_sole_sh="#A8A194",
)

_UID_COUNTER = 0


def _uid(prefix: str) -> str:
    global _UID_COUNTER
    _UID_COUNTER += 1
    return f"{prefix}_{_UID_COUNTER}"


def _stroke_path(d: str, stroke: str, width: float, opacity: float = 1.0,
                 cap: str = "round", join: str = "round") -> str:
    """Çizgi amaçlı <path> yardımcısı — daima fill='none' ekler."""
    op = f' opacity="{opacity:.2f}"' if opacity < 0.999 else ""
    return (f'<path d="{d}" fill="none" stroke="{stroke}" stroke-width="{width:.2f}" '
            f'stroke-linecap="{cap}" stroke-linejoin="{join}"{op}/>')


# ── Göz çizici (v3: R10 & G1 — dar badem/hafif ağır kapaklı, tek küçük kısık parlama, #7EB6BE iris)
def _cocuk_goz(cx: float, cy: float, rx: float, ry: float,
               upper_cover: float, lower_cover: float,
               look_x: float, look_y: float,
               pupil_scale: float = 1.0,
               warm_catch: bool = False,
               tear_pool: bool = False,
               squint_smile: bool = False,
               side_view: bool = False) -> str:
    cid = _uid("eye")
    # Sakin, hafif ağır kapaklı (hooded) badem göz formu
    top_y = cy - ry * (1.0 - upper_cover * 0.96)
    bot_y = cy + ry * (1.0 - lower_cover * 0.85)
    bot_ctrl_y = bot_y - ry * 0.16 if squint_smile else bot_y + ry * 0.18

    if side_view:
        x0, x1 = cx - rx * 0.82, cx + rx * 0.92
        eye_d = (f"M{x0:.1f},{cy+0.8:.1f} "
                 f"Q{cx+rx*0.10:.1f},{top_y-ry*0.14:.1f} {x1:.1f},{cy-0.6:.1f} "
                 f"Q{cx+rx*0.08:.1f},{bot_ctrl_y:.1f} {x0:.1f},{cy+0.8:.1f} Z")
    else:
        x0, x1 = cx - rx, cx + rx
        eye_d = (f"M{x0:.1f},{cy+1.0:.1f} "
                 f"C{cx-rx*0.48:.1f},{top_y-ry*0.20:.1f} {cx+rx*0.48:.1f},{top_y-ry*0.20:.1f} {x1:.1f},{cy+0.2:.1f} "
                 f"C{cx+rx*0.45:.1f},{bot_ctrl_y:.1f} {cx-rx*0.45:.1f},{bot_ctrl_y:.1f} {x0:.1f},{cy+1.0:.1f} Z")

    # İris boyutu: üst kapağın altına doğal oturur, yuvarlak şaşkın çizgi film görünümü yok
    ir_r = min(rx * 0.56, ry * 0.96) if not side_view else ry * 0.86
    ix = cx + look_x * rx * 0.30 + (rx * 0.24 if side_view else 0.0)
    iy = cy + look_y * ry * 0.18 + 0.4
    pr = ir_r * 0.44 * pupil_scale

    ig_id = _uid("ig")
    o = [
        f'<defs><clipPath id="{cid}"><path d="{eye_d}"/></clipPath>'
        f'<radialGradient id="{ig_id}" cx="48%" cy="42%" r="58%">'
        f'<stop offset="0%" stop-color="{PAL["iris_hi"]}"/>'
        f'<stop offset="56%" stop-color="{PAL["iris"]}"/>'
        f'<stop offset="100%" stop-color="{PAL["iris_dk"]}"/>'
        f'</radialGradient></defs>'
    ]
    o.append(f'<path d="{eye_d}" fill="{PAL["sclera"]}"/>')
    o.append(f'<g clip-path="url(#{cid})">')
    # Üst kapak döküm gölgesi (sklera ve iris üstüne)
    o.append(f'<rect x="{cx-rx-4:.1f}" y="{cy-ry-6:.1f}" width="{rx*2+8:.1f}" '
             f'height="{ry*1.02 + upper_cover*ry*0.62:.1f}" fill="{PAL["sclera_sh"]}" opacity="0.58"/>')
    # İris + koyu limbal kenar
    ir_rx = ir_r * (0.62 if side_view else 0.95)
    o.append(f'<ellipse cx="{ix:.1f}" cy="{iy:.1f}" rx="{ir_rx:.1f}" ry="{ir_r:.1f}" '
             f'fill="url(#{ig_id})" stroke="{PAL["iris_dk"]}" stroke-width="1.35"/>')
    # Gözbebeği
    o.append(f'<ellipse cx="{ix:.1f}" cy="{iy:.1f}" rx="{pr*(0.66 if side_view else 1.0):.1f}" ry="{pr:.1f}" fill="#14191E"/>')
    # Üst iris koyu gölge bandı (ağır kapak / derinlik)
    o.append(f'<path d="M{cx-rx-2:.1f},{top_y-4:.1f} Q{cx:.1f},{top_y+ry*0.46:.1f} {cx+rx+2:.1f},{top_y-4:.1f} '
             f'L{cx+rx+2:.1f},{cy-ry-8:.1f} L{cx-rx-2:.1f},{cy-ry-8:.1f} Z" fill="#182028" opacity="0.38"/>')
    # Tek, küçük, kısık ışık yansıması (çift parlak çizgi film noktası YOK)
    c1 = "#FFF0CE" if warm_catch else "#F2F8FA"
    r1 = max(1.15, ir_r * (0.20 if warm_catch else 0.16))
    op1 = 0.88 if warm_catch else 0.72
    o.append(f'<circle cx="{ix - ir_rx*0.30:.1f}" cy="{iy - ir_r*0.24:.1f}" r="{r1:.2f}" fill="{c1}" opacity="{op1:.2f}"/>')

    if tear_pool:
        o.append(f'<path d="M{x0+2:.1f},{bot_y-0.5:.1f} Q{cx:.1f},{bot_y+2.2:.1f} {x1-2:.1f},{bot_y-0.5:.1f}" '
                 f'fill="none" stroke="#CBE9FF" stroke-width="2.0" opacity="0.82" stroke-linecap="round"/>')
    o.append('</g>')

    # Zarif ince üst kirpik/kapak çizgisi + çok ince alt kapak hattı (A-Y çizgi ağırlığı)
    if side_view:
        o.append(_stroke_path(
            f"M{x0:.1f},{cy+0.8:.1f} Q{cx+rx*0.10:.1f},{top_y-ry*0.16:.1f} {x1+1.0:.1f},{cy-0.8:.1f}",
            INK, 2.1))
        o.append(_stroke_path(
            f"M{x0+1:.1f},{cy+1.0:.1f} Q{cx+rx*0.08:.1f},{bot_ctrl_y:.1f} {x1:.1f},{cy-0.3:.1f}",
            INK_SOFT, 0.9, opacity=0.55))
    else:
        o.append(_stroke_path(
            f"M{x0-0.8:.1f},{cy+1.0:.1f} C{cx-rx*0.48:.1f},{top_y-ry*0.22:.1f} {cx+rx*0.48:.1f},{top_y-ry*0.22:.1f} {x1+1.0:.1f},{cy+0.1:.1f}",
            INK, 2.2))
        o.append(_stroke_path(
            f"M{x0+2.0:.1f},{cy+1.2:.1f} C{cx-rx*0.44:.1f},{bot_ctrl_y:.1f} {cx+rx*0.44:.1f},{bot_ctrl_y:.1f} {x1-1.5:.1f},{cy+0.5:.1f}",
            INK_SOFT, 0.9, opacity=0.52))

    # Hafif ağır (hooded) üst göz kapağı kat izi
    crease_y = top_y - ry * (0.28 if not side_view else 0.26)
    o.append(_stroke_path(
        f"M{x0+rx*0.12:.1f},{crease_y+1.8:.1f} Q{cx:.1f},{crease_y-1.6:.1f} {x1-rx*0.10:.1f},{crease_y+1.4:.1f}",
        PAL["skin_dk"], 1.15, opacity=0.62))
    return "".join(o)


# ── Kaş çizici (A-Y ile akraba koyu düz karakter, ince kontursuz doğal kütlesel kaş)
def _cocuk_kas(cx: float, cy: float, w: float, inner_dy: float, outer_dy: float,
               arch: float, toward_outer: int, thick: float = 4.2) -> str:
    xi = cx - toward_outer * w * 0.96
    xo = cx + toward_outer * w * 1.16
    yi = cy - 13.8 + inner_dy
    yo = cy - 14.5 + outer_dy
    mx = (xi + xo) * 0.5 + toward_outer * w * 0.16
    my = (yi + yo) * 0.5 - arch
    t_in = thick * 0.54
    t_mid = thick * 0.44
    t_out = thick * 0.18
    d = (f"M{xi:.1f},{yi-t_in:.1f} Q{mx:.1f},{my-t_mid:.1f} {xo:.1f},{yo-t_out:.1f} "
         f"L{xo+toward_outer*1.4:.1f},{yo+t_out:.1f} "
         f"Q{mx:.1f},{my+t_mid:.1f} {xi:.1f},{yi+t_in:.1f} Z")
    return f'<path d="{d}" fill="{PAL["brow"]}"/>'


# ── Ağız çizici (v3: G1 — ince tek çizgi yerine hafif hacimli doğal dudak + alt çukur gölgesi)
def _cocuk_agiz(mx: float, my: float, w: float, kind: str, view: str) -> str:
    o = []
    sk_dk = PAL["skin_dk"]
    if view == "side":
        if kind == "korku":
            o.append(f'<path d="M{mx-9:.1f},{my-1.6:.1f} Q{mx-3:.1f},{my-3.0:.1f} {mx+3.5:.1f},{my-1.5:.1f} '
                     f'Q{mx-2:.1f},{my+4.2:.1f} {mx-9:.1f},{my+1.2:.1f} Z" fill="#472320" stroke="{INK}" stroke-width="1.3"/>')
            o.append(_stroke_path(f"M{mx-6:.1f},{my-0.9:.1f} L{mx+1:.1f},{my-0.8:.1f}", "#ECE7DF", 1.5))
        elif kind == "sefkat":
            o.append(_stroke_path(f"M{mx-10:.1f},{my+0.4:.1f} Q{mx-3:.1f},{my+1.8:.1f} {mx+4:.1f},{my-1.5:.1f}", INK, 1.5))
        elif kind == "yas":
            o.append(_stroke_path(f"M{mx-9.5:.1f},{my+2.0:.1f} Q{mx-3:.1f},{my-0.8:.1f} {mx+3:.1f},{my+1.4:.1f}", INK, 1.5))
        else:
            o.append(_stroke_path(f"M{mx-10:.1f},{my:.1f} Q{mx-3:.1f},{my+0.6:.1f} {mx+4:.1f},{my:.1f}", INK, 1.5))
        o.append(_stroke_path(f"M{mx-5:.1f},{my+5.8:.1f} Q{mx-2:.1f},{my+6.6:.1f} {mx+1:.1f},{my+5.6:.1f}", sk_dk, 1.2, opacity=0.52))
        return "".join(o)

    if kind == "odak":
        # Hafif hacimli üst dudak düzlemi + ince dudak birleşimi + alt dudak ışığı ve gölgesi
        o.append(f'<path d="M{mx-w*0.80:.1f},{my+0.3:.1f} Q{mx-w*0.25:.1f},{my-2.6:.1f} {mx:.1f},{my-1.6:.1f} '
                 f'Q{mx+w*0.25:.1f},{my-2.6:.1f} {mx+w*0.80:.1f},{my-0.2:.1f} '
                 f'Q{mx:.1f},{my+1.2:.1f} {mx-w*0.80:.1f},{my+0.3:.1f} Z" fill="{PAL["lip"]}" opacity="0.44"/>')
        o.append(f'<path d="M{mx-w*0.64:.1f},{my+1.0:.1f} Q{mx:.1f},{my+5.4:.1f} {mx+w*0.64:.1f},{my+0.6:.1f} '
                 f'Q{mx:.1f},{my+2.0:.1f} {mx-w*0.64:.1f},{my+1.0:.1f} Z" fill="{PAL["lip"]}" opacity="0.28"/>')
        o.append(_stroke_path(f"M{mx-w*0.26:.1f},{my+3.4:.1f} Q{mx:.1f},{my+4.1:.1f} {mx+w*0.26:.1f},{my+3.2:.1f}", PAL["skin_hi"], 1.3, opacity=0.35))
        o.append(_stroke_path(f"M{mx-w*0.88:.1f},{my+0.4:.1f} Q{mx:.1f},{my+1.5:.1f} {mx+w*0.88:.1f},{my-0.2:.1f}", INK, 1.65))
        o.append(_stroke_path(f"M{mx-w*0.42:.1f},{my+5.8:.1f} Q{mx:.1f},{my+6.8:.1f} {mx+w*0.42:.1f},{my+5.6:.1f}", sk_dk, 1.35, opacity=0.58))
    elif kind == "kararli":
        o.append(f'<path d="M{mx-w*0.82:.1f},{my+0.8:.1f} Q{mx:.1f},{my-2.4:.1f} {mx+w*0.82:.1f},{my+0.4:.1f} '
                 f'Q{mx:.1f},{my+0.2:.1f} {mx-w*0.82:.1f},{my+0.8:.1f} Z" fill="{PAL["lip_sh"]}" opacity="0.45"/>')
        o.append(_stroke_path(f"M{mx-w*0.92:.1f},{my+1.0:.1f} Q{mx:.1f},{my-0.7:.1f} {mx+w*0.92:.1f},{my+0.6:.1f}", INK, 1.85))
        o.append(_stroke_path(f"M{mx-w*0.46:.1f},{my+6.0:.1f} Q{mx:.1f},{my+7.0:.1f} {mx+w*0.46:.1f},{my+5.8:.1f}", sk_dk, 1.45, opacity=0.65))
    elif kind == "korku":
        # Gergin hafif aralanmış yatay dudaklar + belli belirsiz diş çizgisi (asla yuvarlak "o" değil)
        mouth_d = (f"M{mx-w*0.86:.1f},{my+2.2:.1f} "
                   f"Q{mx:.1f},{my-3.0:.1f} {mx+w*0.86:.1f},{my+1.6:.1f} "
                   f"Q{mx:.1f},{my+6.0:.1f} {mx-w*0.86:.1f},{my+2.2:.1f} Z")
        o.append(f'<path d="{mouth_d}" fill="#44211E" stroke="{INK}" stroke-width="1.45" stroke-linejoin="round"/>')
        o.append(_stroke_path(f"M{mx-w*0.48:.1f},{my+0.2:.1f} Q{mx:.1f},{my-0.6:.1f} {mx+w*0.48:.1f},{my+0.1:.1f}", "#ECE8E1", 1.7, opacity=0.88))
        o.append(_stroke_path(f"M{mx-w*0.46:.1f},{my+8.8:.1f} Q{mx:.1f},{my+9.8:.1f} {mx+w*0.46:.1f},{my+8.6:.1f}", sk_dk, 1.35, opacity=0.60))
    elif kind == "yas":
        o.append(f'<path d="M{mx-w*0.72:.1f},{my+2.6:.1f} Q{mx:.1f},{my-1.8:.1f} {mx+w*0.72:.1f},{my+2.4:.1f} '
                 f'Q{mx:.1f},{my+0.8:.1f} {mx-w*0.72:.1f},{my+2.6:.1f} Z" fill="{PAL["lip"]}" opacity="0.38"/>')
        o.append(_stroke_path(
            f"M{mx-w*0.80:.1f},{my+3.2:.1f} Q{mx-w*0.24:.1f},{my-0.6:.1f} {mx:.1f},{my+0.3:.1f} "
            f"Q{mx+w*0.24:.1f},{my-0.6:.1f} {mx+w*0.80:.1f},{my+3.0:.1f}", INK, 1.65))
        o.append(_stroke_path(f"M{mx-w*0.36:.1f},{my+6.8:.1f} Q{mx:.1f},{my+7.8:.1f} {mx+w*0.36:.1f},{my+6.6:.1f}", sk_dk, 1.3, opacity=0.58))
    elif kind == "sefkat":
        o.append(f'<path d="M{mx-w*0.85:.1f},{my-0.2:.1f} Q{mx:.1f},{my+1.4:.1f} {mx+w*0.88:.1f},{my-1.2:.1f} '
                 f'Q{mx:.1f},{my+6.2:.1f} {mx-w*0.85:.1f},{my-0.2:.1f} Z" fill="{PAL["lip"]}" opacity="0.34"/>')
        o.append(_stroke_path(
            f"M{mx-w*0.92:.1f},{my-0.4:.1f} Q{mx:.1f},{my+5.6:.1f} {mx+w*0.96:.1f},{my-1.5:.1f}", INK, 1.65))
        o.append(_stroke_path(f"M{mx-w*0.44:.1f},{my+6.4:.1f} Q{mx:.1f},{my+8.0:.1f} {mx+w*0.44:.1f},{my+6.0:.1f}", sk_dk, 1.25, opacity=0.50))
    return "".join(o)


# ── İfade parametre tablosu (v3: daha ağır/odaklı kapaklar, sakin sinematik 2D)
# (kaş_iç_dy, kaş_dış_dy, kaş_kavis, üst_kapak, alt_kapak, göz_bebeği_ölçek, ağız_türü, ekstra)
COCUK_IFADE = {
    "odak":    (1.0,  -0.4, 1.0, 0.38, 0.14, 1.00, "odak",    ""),
    "korku":   (-6.2,  2.2, 3.8, 0.08, 0.14, 0.78, "korku",   "tension"),
    "yas":     (-6.8,  4.8, 2.4, 0.42, 0.14, 1.02, "yas",     "tear"),
    "sefkat":  (-1.8, -1.2, 3.0, 0.30, 0.26, 1.04, "sefkat",  "warm"),
    "kararli": (3.8,  -2.2, 0.6, 0.44, 0.20, 0.96, "kararli", "brow_line"),
}


def kafa_cocuk(view: str = "3q", ifade: str = "odak", look: float = 0.25,
               lighting: str = "studio", boyun: bool = False) -> str:
    """11 Yaş Michael Scofield başı (v3) — merkez (0,0), yaklaşık 176x208 birim.
    view: 'front' | '3q' | 'side' (3q ve side sağa bakar).
    ifade: 'odak' | 'korku' | 'yas' | 'sefkat' | 'kararli'.
    lighting: 'studio' | 'depo_korku' | 'prolog_warm'.
    boyun: True ise 3 görünüş kartı için A-Y ile uyumlu kısa boyun kesiti çizer.
    """
    bi, bo, b_arch, lu, ll, p_sc, mk, extra = COCUK_IFADE.get(ifade, COCUK_IFADE["odak"])
    cid = _uid("face")
    o = []

    # 0. Opsiyonel kısa boyun kesiti (3 görünüş kartında A-Y ile tam stil bütünlüğü)
    if boyun:
        if view == "front":
            nd = "M-24,74 L-26,118 Q0,126 26,118 L24,74 Z"
            ns = "M-24,76 Q0,98 24,76 L24,96 Q0,108 -24,96 Z"
        elif view == "3q":
            nd = "M-32,68 L-34,118 Q-4,126 22,116 L18,76 Z"
            ns = "M-32,70 Q-4,98 18,78 L19,98 Q-4,110 -32,94 Z"
        else:
            nd = "M-38,62 L-40,118 Q-10,126 16,116 L14,76 Z"
            ns = "M-38,64 Q-10,96 14,78 L15,96 Q-10,108 -38,90 Z"
        o.append(f'<path d="{nd}" fill="{PAL["skin"]}" stroke="{INK}" stroke-width="1.8" stroke-linejoin="round"/>')
        o.append(f'<path d="{ns}" fill="{PAL["skin_dk"]}" opacity="0.48"/>')
        if view != "front":
            o.append(f'<path d="M-36,70 L-18,70 L-20,118 L-38,116 Z" fill="{PAL["skin_sh"]}" opacity="0.45"/>')

    # 1. Arka saç kütlesi (ince kontur: 1.7px)
    if view == "front":
        o.append(f'<path d="M-72,-16 C-82,-68 -60,-108 0,-110 C60,-108 82,-68 72,-16 '
                 f'L68,16 C60,30 48,28 44,16 L-44,16 C-48,28 -60,30 -68,16 Z" '
                 f'fill="{PAL["hair_dk"]}" stroke="{INK}" stroke-width="1.7" stroke-linejoin="round"/>')
    elif view == "3q":
        o.append(f'<path d="M-74,-12 C-84,-66 -56,-110 8,-110 C64,-108 78,-70 72,-22 '
                 f'L-46,38 C-64,36 -76,18 -74,-12 Z" '
                 f'fill="{PAL["hair_dk"]}" stroke="{INK}" stroke-width="1.7" stroke-linejoin="round"/>')
    else:
        o.append(f'<path d="M-82,-16 C-90,-70 -56,-112 4,-112 C54,-110 70,-76 64,-34 '
                 f'L-44,48 C-66,46 -80,24 -82,-16 Z" '
                 f'fill="{PAL["hair_dk"]}" stroke="{INK}" stroke-width="1.7" stroke-linejoin="round"/>')

    # 2. Yüz silüeti (11 yaş: yumuşak elmacık-çene geçişi, yetişkinden kısa alt yüz, zarif çene)
    if view == "front":
        face_d = (
            "M-62,-22 C-64,-76 -40,-96 0,-96 C40,-96 64,-76 62,-22 "
            "C62,14 56,42 40,64 C26,81 12,88 0,88 C-12,88 -26,81 -40,64 C-56,42 -62,14 -62,-22 Z"
        )
        ears = [(-64, 4, -1), (64, 4, 1)]
        # Göz yüksekliği %18-20 kısıldı (ry=8.2) -> sakin, zeki, gözlemci
        eyes = [(-25.5, -2, 14.8, 8.2, -1), (25.5, -2, 14.8, 8.2, 1)]
        mx, my, mw = 0.0, 48.0, 14.5
    elif view == "3q":
        face_d = (
            "M-58,-20 C-62,-76 -34,-96 10,-96 C54,-94 72,-70 70,-22 "
            "C70,-4 72,12 68,26 C64,46 52,66 36,80 C22,89 8,90 -8,84 "
            "C-32,74 -50,50 -56,20 Z"
        )
        ears = [(-56, 6, -1)]
        eyes = [(-6.5, -2, 13.6, 8.2, -1), (40.5, -2.4, 15.0, 8.3, 1)]
        mx, my, mw = 23.0, 48.5, 13.5
    else:  # side
        face_d = (
            "M-66,-20 C-70,-76 -40,-96 6,-96 C46,-94 60,-72 60,-34 "
            "L62,-12 L66,-1 L80,19 C82,23 78,28 69,29 "
            "L68,37 C72,41 70,45 65,48 L67,55 C67,60 62,65 58,68 "
            "C57,78 48,86 35,88 C16,90 -10,84 -32,68 C-54,50 -62,20 -66,-20 Z"
        )
        ears = [(-16, 8, -1)]
        eyes = [(42.5, -2.8, 13.0, 7.9, 1)]
        mx, my, mw = 61.5, 48.5, 10.0

    # 3. Kulaklar (ince kontur: 1.6px)
    for ex, ey, eside in ears:
        erx = 9.6 if view != "side" else 11.2
        ery = 16.5
        o.append(f'<ellipse cx="{ex:.1f}" cy="{ey:.1f}" rx="{erx:.1f}" ry="{ery:.1f}" '
                 f'fill="{PAL["skin_sh"] if eside > 0 and view == "front" else PAL["skin"]}" '
                 f'stroke="{INK}" stroke-width="1.6"/>')
        o.append(_stroke_path(f"M{ex-eside*1.8:.1f},{ey-7.0:.1f} Q{ex-eside*6.0:.1f},{ey:.1f} {ex-eside*1.0:.1f},{ey+7.0:.1f}",
                              PAL["skin_dk"], 1.35, opacity=0.72))

    # 4. Yüz tabanı + A-Y ile hizalı yüz düzlem gölgeleri (eye sockets, cheek, jaw, nose bridge)
    shadow_grad_id = _uid("shg")
    o.append(f'<defs><clipPath id="{cid}"><path d="{face_d}"/></clipPath>')
    if lighting in ("depo_korku", "prolog_warm"):
        o.append(
            f'<linearGradient id="{shadow_grad_id}" x1="14%" y1="35%" x2="88%" y2="62%">'
            f'<stop offset="0%" stop-color="#1A1B27" stop-opacity="0.86"/>'
            f'<stop offset="46%" stop-color="#2D2835" stop-opacity="0.64"/>'
            f'<stop offset="68%" stop-color="#583E38" stop-opacity="0.16"/>'
            f'<stop offset="100%" stop-color="#FFCA84" stop-opacity="0.0"/>'
            f'</linearGradient>'
        )
    o.append('</defs>')

    base_skin = PAL["skin"] if lighting == "studio" else "#D9A682"
    o.append(f'<path d="{face_d}" fill="{base_skin}"/>')

    o.append(f'<g clip-path="url(#{cid})">')
    if lighting == "depo_korku":
        o.append(f'<rect x="-90" y="-110" width="180" height="220" fill="url(#{shadow_grad_id})"/>')
        o.append(f'<path d="M-85,-110 L-12,-110 C-24,-55 -18,10 -24,105 L-85,105 Z" fill="#1A1A28" opacity="0.44"/>')
        # Organik kaş altı / göz çukuru gölgesi (elips izi yok)
        o.append(f'<path d="M-24,-15 Q-6,-20 10,-12 Q6,5 -8,6 Q-22,4 -24,-15 Z" fill="{PAL["skin_deep"]}" opacity="0.30"/>')
        o.append(f'<path d="M24,-13 Q42,-20 58,-14 Q55,4 40,5 Q26,4 24,-13 Z" fill="{PAL["skin_dk"]}" opacity="0.24"/>')
        o.append(f'<path d="M44,-44 C66,-12 72,30 46,88 L88,88 L88,-44 Z" fill="#FFD194" opacity="0.28"/>')
        o.append(_stroke_path("M64,-14 C70,18 59,56 35,80", "#FFE4B8", 3.6, opacity=0.72))
    elif lighting == "prolog_warm":
        o.append(f'<rect x="-90" y="-110" width="180" height="220" fill="url(#{shadow_grad_id})"/>')
        o.append(f'<path d="M-85,-110 L-10,-110 C-22,-55 -16,12 -22,105 L-85,105 Z" fill="#121420" opacity="0.52"/>')
        o.append(f'<path d="M-24,-15 Q-6,-20 10,-12 Q6,5 -8,6 Q-22,4 -24,-15 Z" fill="{PAL["skin_deep"]}" opacity="0.34"/>')
        o.append(f'<path d="M24,-13 Q42,-20 58,-14 Q55,4 40,5 Q26,4 24,-13 Z" fill="{PAL["skin_dk"]}" opacity="0.20"/>')
        o.append(f'<path d="M26,-95 L86,-95 L86,95 L22,95 C38,40 36,-30 26,-95 Z" fill="#FFBE73" opacity="0.24"/>')
        o.append(_stroke_path("M65,-24 C71,14 62,54 35,82", "#FFE8C0", 4.4, opacity=0.84))
    else:
        # Stüdyo sinematik 2D yüz düzlemleri (A-Y ile aynı görsel dil, 11 yaşa yumuşatılmış)
        if view == "front":
            # Sağ yüz yan düzlem gölgesi + sol şakak hafif düzlemi
            o.append(f'<path d="M34,-100 C46,-36 44,32 20,90 L78,90 L78,-100 Z" fill="{PAL["skin_sh"]}" opacity="0.72"/>')
            o.append(f'<path d="M-66,-100 L-44,-100 C-50,-40 -48,26 -30,86 L-66,86 Z" fill="{PAL["skin_sh"]}" opacity="0.34"/>')
            # Göz çukuru / kaş altı düzlem gölgeleri
            o.append(f'<path d="M-44,-15 Q-26,-20 -8,-12 Q-12,4 -26,5 Q-40,4 -44,-15 Z" fill="{PAL["skin_sh"]}" opacity="0.56"/>')
            o.append(f'<path d="M8,-12 Q26,-20 44,-15 Q40,4 26,5 Q12,4 8,-12 Z" fill="{PAL["skin_sh"]}" opacity="0.64"/>')
            # Elmacık altı ve çene altı yumuşak düzlemler
            o.append(f'<path d="M-52,32 Q-38,54 -22,64 L-38,76 Q-56,52 -58,28 Z" fill="{PAL["skin_sh"]}" opacity="0.36"/>')
            o.append(f'<path d="M52,32 Q38,54 22,64 L38,76 Q56,52 58,28 Z" fill="{PAL["skin_dk"]}" opacity="0.24"/>')
            o.append(f'<path d="M-40,68 Q0,88 40,68 L44,96 L-44,96 Z" fill="{PAL["skin_dk"]}" opacity="0.24"/>')
            # Alın, burun sırtı ve elmacık ışık düzlemleri
            o.append(f'<ellipse cx="-14" cy="-34" rx="22" ry="14" fill="{PAL["skin_hi"]}" opacity="0.34"/>')
            o.append(f'<ellipse cx="-26" cy="18" rx="14" ry="9" fill="{PAL["skin_hi"]}" opacity="0.26"/>')
            o.append(f'<path d="M-3,-8 L2,-8 L1,20 L-3,20 Z" fill="{PAL["skin_hi"]}" opacity="0.32"/>')
        elif view == "3q":
            # Sol yüz yan düzlemi (A-Y'deki gibi net ama çocukta yumuşak elmacık-çene geçişi)
            o.append(f'<path d="M-66,-100 L-22,-100 C-36,-34 -34,36 -2,90 L-66,90 Z" fill="{PAL["skin_sh"]}" opacity="0.76"/>')
            # Sol elmacık altı yumuşak gölge düzlemi
            o.append(f'<path d="M-46,24 C-32,46 -18,64 2,74 L-18,86 C-40,72 -54,48 -56,22 Z" fill="{PAL["skin_dk"]}" opacity="0.24"/>')
            # Göz çukuru / kaş altı düzlem gölgeleri
            o.append(f'<path d="M-24,-15 Q-6,-20 10,-12 Q6,5 -8,6 Q-22,4 -24,-15 Z" fill="{PAL["skin_sh"]}" opacity="0.62"/>')
            o.append(f'<path d="M24,-13 Q42,-20 58,-14 Q55,4 40,5 Q26,4 24,-13 Z" fill="{PAL["skin_sh"]}" opacity="0.52"/>')
            # Çene altı düzlem gölgesi
            o.append(f'<path d="M-34,68 Q12,88 50,66 L54,96 L-40,96 Z" fill="{PAL["skin_dk"]}" opacity="0.24"/>')
            # Alın + sağ elmacık + burun sırtı + çene ucu ışık düzlemleri
            o.append(f'<ellipse cx="22" cy="-34" rx="24" ry="14" fill="{PAL["skin_hi"]}" opacity="0.34"/>')
            o.append(f'<ellipse cx="44" cy="18" rx="14" ry="9" fill="{PAL["skin_hi"]}" opacity="0.28"/>')
            o.append(f'<ellipse cx="21" cy="70" rx="10" ry="5.5" fill="{PAL["skin_hi"]}" opacity="0.22"/>')
            o.append(f'<path d="M19,-6 L23,-6 L28,18 L24,18 Z" fill="{PAL["skin_hi"]}" opacity="0.32"/>')
            # İnce soğuk rim-light (sol yanak kenarı)
            o.append(_stroke_path("M-55,-6 C-53,28 -37,58 -12,79", "#B6D4E4", 2.0, opacity=0.32))
        else:  # side
            o.append(f'<path d="M-74,-100 L14,-100 C2,-24 4,40 22,90 L-74,90 Z" fill="{PAL["skin_sh"]}" opacity="0.64"/>')
            # Göz çukuru + elmacık altı + çene altı
            o.append(f'<path d="M28,-14 Q44,-18 56,-12 Q52,4 40,5 Q30,4 28,-14 Z" fill="{PAL["skin_sh"]}" opacity="0.56"/>')
            o.append(f'<path d="M10,32 C22,52 34,64 52,70 L36,88 C10,82 -14,66 -26,44 Z" fill="{PAL["skin_dk"]}" opacity="0.22"/>')
            o.append(f'<ellipse cx="36" cy="-34" rx="18" ry="12" fill="{PAL["skin_hi"]}" opacity="0.28"/>')
            o.append(_stroke_path("M64,-10 L76,18 M65,46 L63,64", PAL["skin_hi"], 2.0, opacity=0.40))

    # Hafif canlı yanak sıcaklığı (şefkatte belirgin, diğerlerinde çok ince)
    blush_op = 0.18 if extra == "warm" else (0.05 if lighting != "studio" else 0.08)
    if view == "front":
        o.append(f'<ellipse cx="-32" cy="24" rx="13" ry="7" fill="{PAL["blush"]}" opacity="{blush_op:.2f}"/>')
        o.append(f'<ellipse cx="32" cy="24" rx="13" ry="7" fill="{PAL["blush"]}" opacity="{blush_op:.2f}"/>')
    elif view == "3q":
        o.append(f'<ellipse cx="-14" cy="24" rx="12" ry="7" fill="{PAL["blush"]}" opacity="{blush_op:.2f}"/>')
        o.append(f'<ellipse cx="45" cy="22" rx="11" ry="6.5" fill="{PAL["blush"]}" opacity="{blush_op:.2f}"/>')
    else:
        o.append(f'<ellipse cx="38" cy="24" rx="12" ry="7" fill="{PAL["blush"]}" opacity="{blush_op:.2f}"/>')

    # Saçın alına düşen yumuşak gölgesi
    o.append(f'<path d="M-70,-48 Q-30,-36 0,-40 Q35,-34 76,-44 L76,-106 L-70,-106 Z" fill="{PAL["skin_dk"]}" opacity="0.24"/>')
    o.append('</g>')

    # Yüz dış konturu (v3: A-Y ile aynı zarif 1.85px incelik)
    o.append(f'<path d="{face_d}" fill="none" stroke="{INK}" stroke-width="1.85" stroke-linejoin="round"/>')

    # 5. Gözler + Kaşlar
    warm_c = lighting in ("depo_korku", "prolog_warm") or extra == "warm"
    tear_p = extra == "tear"
    squint = extra == "warm"
    brows_svg = []
    for ex, ey, erx, ery, side_dir in eyes:
        # Çok ince göz altı çukuru vurgusu
        if view != "side":
            o.append(_stroke_path(f"M{ex-erx*0.48:.1f},{ey+ery*1.38:.1f} Q{ex:.1f},{ey+ery*1.58:.1f} {ex+erx*0.48:.1f},{ey+ery*1.32:.1f}",
                                  PAL["skin_dk"], 1.0, opacity=0.34 if ifade != "korku" else 0.50))
        o.append(_cocuk_goz(
            ex, ey, erx, ery, lu, ll,
            look_x=look if view != "front" else look * 0.30,
            look_y=0.05 if ifade == "yas" else (-0.02 if ifade == "korku" else 0.0),
            pupil_scale=p_sc,
            warm_catch=warm_c,
            tear_pool=tear_p,
            squint_smile=squint,
            side_view=(view == "side"),
        ))
        tw = side_dir if view != "side" else -1
        brows_svg.append(_cocuk_kas(ex, ey, erx * (0.98 if view != "side" else 0.86),
                                    bi, bo, b_arch, tw, thick=4.3 if view != "side" else 3.9))

    if extra == "tension":
        gx = 0 if view == "front" else (18 if view == "3q" else 50)
        brows_svg.append(_stroke_path(f"M{gx-4.5:.1f},-19 Q{gx:.1f},-16 {gx+4.5:.1f},-19", PAL["skin_dk"], 1.25, opacity=0.58))
        brows_svg.append(_stroke_path(f"M{gx-3:.1f},-27 Q{gx:.1f},-29.5 {gx+3.5:.1f},-27", PAL["skin_dk"], 1.1, opacity=0.44))
    elif extra == "brow_line":
        gx = 0 if view == "front" else (18 if view == "3q" else 50)
        brows_svg.append(_stroke_path(f"M{gx-1.5:.1f},-19 L{gx-1.5:.1f},-11", PAL["skin_dk"], 1.3, opacity=0.58))

    # 6. Burun (A-Y gibi temiz gölge düzlemi + çok ince zarif uç/kanat hattı, kalın siyah çizgi YOK)
    if view == "front":
        # Sağ yan burun köprüsü düzlem gölgesi + alt üçgen gölge
        o.append(f'<path d="M2,-6 L6,21 L0,25 L-5,22 L1,18 Z" fill="{PAL["skin_sh"]}" opacity="0.68"/>')
        o.append(f'<path d="M-6,22 Q0,28 6,22 Q0,24.5 -6,22 Z" fill="{PAL["skin_dk"]}" opacity="0.48"/>')
        o.append(_stroke_path("M-6.2,23.2 Q0,26.8 6.2,23.2", PAL["skin_dk"], 1.45, opacity=0.82))
        o.append(_stroke_path("M-4.2,24.2 Q-2.2,25.2 -0.5,24.2", INK, 1.1, opacity=0.48))
        o.append(_stroke_path("M0.8,24.2 Q2.6,25.2 4.5,24.2", INK, 1.1, opacity=0.48))
    elif view == "3q":
        # Temiz burun köprüsü gölge düzlemi + ince çizgi
        o.append(f'<path d="M15,-6 L20,-4 L28,20 L21,26 L12,23 Q17,14 15,-6 Z" fill="{PAL["skin_sh"]}" opacity="0.64"/>')
        o.append(f'<path d="M13,23 Q21,28 28,22 Q22,25 13,23 Z" fill="{PAL["skin_dk"]}" opacity="0.50"/>')
        o.append(_stroke_path("M20,-2 L28.5,19.5 Q27,24.5 19.5,24.5", INK, 1.55))
        o.append(_stroke_path("M14.5,23.2 Q17.5,25.2 20.5,24.4", PAL["skin_dk"], 1.2, opacity=0.75))
    else:
        o.append(_stroke_path("M67,24 Q63,26.2 60,24", PAL["skin_dk"], 1.3, opacity=0.72))

    # 7. Ağız
    o.append(_cocuk_agiz(mx, my, mw, mk, view))

    # 8. Gözyaşı (yas)
    if extra == "tear":
        tx = 37.0 if view == "3q" else (23.0 if view == "front" else 46.0)
        o.append(_stroke_path(f"M{tx:.1f},8 Q{tx+2.8:.1f},24 {tx+1:.1f},38", "#CBE8FF", 2.4, opacity=0.74))
        o.append(f'<path d="M{tx+1:.1f},36 C{tx+3.8:.1f},42 {tx+3.0:.1f},47 {tx+0.5:.1f},47 '
                 f'C{tx-2.0:.1f},47 {tx-2.0:.1f},42 {tx+1:.1f},36 Z" fill="#D8F0FF" stroke="#6E99B8" stroke-width="1.0" opacity="0.88"/>')

    o.extend(brows_svg)

    # 9. Ön saç kütlesi (katmanlı kısa-dağınık koyu kahve, A-Y gibi ince 1.7px kontur + doğal düzlem ışığı)
    h_rim = "#FFE0AC" if lighting in ("depo_korku", "prolog_warm") else PAL["hair_rim"]
    h_hi = PAL["hair_hi"] if lighting != "depo_korku" else "#48382F"

    if view == "front":
        hair_d = (
            "M-68,-12 C-76,-52 -64,-96 -24,-108 C-10,-114 6,-114 20,-110 "
            "C34,-112 46,-104 56,-90 C72,-68 74,-36 68,-12 "
            "C64,-24 58,-38 50,-44 C46,-30 42,-22 37,-20 C40,-36 33,-48 22,-52 "
            "C16,-34 8,-22 -2,-20 C4,-38 -2,-52 -14,-54 C-22,-36 -30,-26 -40,-24 "
            "C-34,-38 -40,-48 -48,-46 C-54,-36 -60,-24 -63,-8 Z"
        )
        o.append(f'<path d="{hair_d}" fill="{PAL["hair"]}" stroke="{INK}" stroke-width="1.7" stroke-linejoin="round"/>')
        o.append(f'<path d="M18,-110 C56,-100 72,-58 66,-16 C60,-34 48,-46 34,-52 C38,-74 32,-94 18,-110 Z" '
                 f'fill="{PAL["hair_dk"]}" opacity="0.54"/>')
        o.append(_stroke_path("M-38,-84 Q-6,-98 30,-86", h_hi, 5.2, opacity=0.48))
        o.append(_stroke_path("M-22,-70 Q0,-78 18,-70", h_hi, 2.6, opacity=0.36))
        o.append(_stroke_path("M-30,-52 Q-22,-74 -10,-92", PAL["hair_dk"], 1.5, opacity=0.58))
        o.append(_stroke_path("M14,-52 Q22,-74 16,-92", PAL["hair_dk"], 1.5, opacity=0.58))
        o.append(_stroke_path("M-62,-50 C-64,-76 -42,-100 -16,-106", h_rim, 1.5, opacity=0.34))
    elif view == "3q":
        # Perçem uçları kaşların üstünde temiz kalır (korku/yas kaş hareketi engellenmez)
        hair_d = (
            "M-60,6 C-74,-28 -72,-78 -32,-102 C-12,-114 14,-116 36,-108 "
            "C56,-100 72,-78 76,-48 C78,-34 74,-22 68,-18 "
            "C66,-34 58,-44 46,-48 C42,-34 36,-25 27,-22 "
            "C32,-38 24,-50 12,-53 C4,-36 -6,-26 -18,-24 "
            "C-12,-40 -18,-50 -30,-48 C-40,-36 -46,-18 -49,0 C-52,-8 -56,-10 -60,6 Z"
        )
        o.append(f'<path d="{hair_d}" fill="{PAL["hair"]}" stroke="{INK}" stroke-width="1.7" stroke-linejoin="round"/>')
        o.append(f'<path d="M-60,4 C-72,-34 -66,-76 -26,-102 C-42,-74 -44,-38 -48,-2 Z" '
                 f'fill="{PAL["hair_dk"]}" opacity="0.58"/>')
        o.append(_stroke_path("M-24,-88 Q14,-102 50,-80", h_hi, 5.2, opacity=0.48))
        o.append(_stroke_path("M-6,-70 Q20,-78 42,-64", h_hi, 2.5, opacity=0.34))
        o.append(_stroke_path("M-18,-48 Q-8,-74 12,-94", PAL["hair_dk"], 1.5, opacity=0.58))
        o.append(_stroke_path("M22,-48 Q32,-70 40,-86", PAL["hair_dk"], 1.4, opacity=0.56))
        o.append(_stroke_path("M-40,-40 Q-38,-66 -22,-86", PAL["hair_dk"], 1.4, opacity=0.48))
        if lighting in ("depo_korku", "prolog_warm"):
            o.append(_stroke_path("M48,-88 C68,-72 74,-48 70,-20", h_rim, 2.2, opacity=0.72))
        else:
            o.append(_stroke_path("M-64,-22 C-68,-56 -50,-88 -20,-102", h_rim, 1.5, opacity=0.34))
    else:  # side
        hair_d = (
            "M-54,36 C-80,12 -86,-46 -58,-88 C-28,-116 32,-118 64,-74 "
            "C72,-60 72,-40 62,-32 C56,-44 44,-50 30,-48 "
            "C24,-34 14,-26 2,-28 C6,-44 -2,-54 -14,-50 "
            "C-24,-38 -30,-18 -28,2 C-22,6 -20,16 -28,22 C-38,28 -46,34 -54,36 Z"
        )
        o.append(f'<path d="{hair_d}" fill="{PAL["hair"]}" stroke="{INK}" stroke-width="1.7" stroke-linejoin="round"/>')
        o.append(f'<path d="M-54,34 C-78,10 -82,-44 -56,-84 C-48,-46 -42,-2 -34,26 Z" '
                 f'fill="{PAL["hair_dk"]}" opacity="0.54"/>')
        o.append(_stroke_path("M-42,-84 Q2,-104 44,-80", h_hi, 5.2, opacity=0.48))
        o.append(_stroke_path("M-20,-52 Q-14,-80 6,-96", PAL["hair_dk"], 1.5, opacity=0.58))
        o.append(_stroke_path("M16,-52 Q26,-74 36,-86", PAL["hair_dk"], 1.4, opacity=0.54))
        o.append(_stroke_path("M-70,-46 C-66,-78 -40,-102 -10,-108", h_rim, 1.5, opacity=0.34))

    return "".join(o)


# ── Doğal 2D çocuk eli (ince 1.6px kontur, zarif parmak silüeti)
def _cocuk_el(cx: float, cy: float, scale: float = 1.0, flip_x: int = 1,
              rot: float = 0.0, shade_dark: bool = False) -> str:
    sk = PAL["skin_sh"] if shade_dark else PAL["skin"]
    sd = PAL["skin_dk"] if shade_dark else PAL["skin_sh"]
    sx = scale * flip_x
    sy = scale
    hand_d = (
        "M-8.5,-13 C-11,-4 -11,7 -9.5,16 "
        "C-7.5,21.5 -3,22.5 0,18.5 L2,12 "
        "C3,19 5.8,24 9,23 C11.5,22 12,17 11,11 "
        "C13.8,15.5 16,17.5 17.5,15 C19.2,12 17.5,4.5 15,-3 "
        "C13,-8.5 11,-12 7.5,-14 Z"
    )
    thumb_d = "M-8.5,-7.5 C-16,-4 -18.5,2 -15.5,6.5 C-13,8.5 -8.5,6.5 -6.5,2"
    return (
        f'<g transform="translate({cx:.1f},{cy:.1f}) rotate({rot:.1f}) scale({sx:.3f},{sy:.3f})">'
        f'<path d="{hand_d}" fill="{sk}" stroke="{INK}" stroke-width="1.7" stroke-linejoin="round"/>'
        f'<path d="{thumb_d}" fill="{sk}" stroke="{INK}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>'
        f'<path d="M-1,-3 Q3.5,5 4.5,14 M4.5,-4 Q9,4 10,11" fill="none" stroke="{sd}" stroke-width="1.2" stroke-linecap="round" opacity="0.72"/>'
        f'</g>'
    )


def figur_cocuk(ifade: str = "odak", lighting: str = "studio") -> str:
    """11 Yaş Michael Scofield tam boy figür (v3) — ayak ortası (0, 0), boy ~442 birim.
    Sağa 3/4 bakar. Dövme YOK (R3). Sağlam boyun-yaka bağlantısı (R4).
    D2: Kısa doğal çocuk kol boyu ve dirsekte hafif kırık/eğim.
    G1: A-Y ile aynı zarif ince kontur (~1.9px).
    """
    o = []

    # 1. Yer temas gölgesi
    o.append('<ellipse cx="2" cy="5" rx="84" ry="13" fill="#080B10" opacity="0.34"/>')
    o.append('<ellipse cx="-30" cy="4" rx="33" ry="7" fill="#05070B" opacity="0.46"/>')
    o.append('<ellipse cx="30" cy="6" rx="35" ry="7.5" fill="#05070B" opacity="0.48"/>')

    # 2. Arka (sol) kol — D2: hafif kısaltılmış, dirsekte hafif geriye-öne doğal kırık
    arm_bg_d = (
        "M-42,-314 C-56,-298 -68,-274 -73,-246 "
        "C-74,-238 -72,-228 -68,-216 C-64,-204 -60,-192 -56,-184 "
        "L-36,-188 C-40,-200 -44,-214 -45,-226 "
        "C-46,-236 -43,-246 -38,-260 C-33,-274 -26,-286 -22,-294 Z"
    )
    cid_ab = _uid("arm_b")
    o.append(f'<defs><clipPath id="{cid_ab}"><path d="{arm_bg_d}"/></clipPath></defs>')
    o.append(f'<path d="{arm_bg_d}" fill="{PAL["shirt_sh"]}"/>')
    o.append(f'<g clip-path="url(#{cid_ab})">')
    for k in range(7):
        sy = -306 + k * 21.5
        o.append(_stroke_path(f"M-86,{sy-1:.1f} Q-56,{sy+5.0:.1f} -20,{sy-2:.1f}", PAL["stripe_sh"], 7.6))
    o.append(f'<path d="M-82,-314 L-52,-314 L-54,-180 L-82,-180 Z" fill="{PAL["shirt_dk"]}" opacity="0.44"/>')
    o.append(_stroke_path("M-68,-242 Q-54,-236 -44,-242", PAL["shirt_dk"], 1.5, opacity=0.62))
    o.append('</g>')
    o.append(f'<path d="{arm_bg_d}" fill="none" stroke="{INK}" stroke-width="1.9" stroke-linejoin="round"/>')
    # Arka manşet + el (kalça/uyluk üst hizasında doğal biter)
    o.append(f'<path d="M-57,-186 Q-46,-182 -35,-187 L-34,-179 Q-46,-175 -56,-179 Z" '
             f'fill="{PAL["shirt_dk"]}" stroke="{INK}" stroke-width="1.6" stroke-linejoin="round"/>')
    o.append(_cocuk_el(-44, -166, scale=0.80, flip_x=-1, rot=-8, shade_dark=True))

    # 3. Bacaklar (koyu lacivert pantolon, ince 1.9px kontur)
    leg_b = (
        "M-38,-184 L-44,-98 C-46,-64 -44,-34 -42,-16 "
        "L-10,-16 C-10,-40 -8,-72 -6,-102 L-2,-184 Z"
    )
    o.append(f'<path d="{leg_b}" fill="{PAL["pants_sh"]}" stroke="{INK}" stroke-width="1.9" stroke-linejoin="round"/>')
    o.append(_stroke_path("M-36,-104 Q-24,-98 -12,-103", "#18202B", 1.5, opacity=0.68))

    leg_f = (
        "M-4,-184 L4,-100 C8,-66 12,-34 14,-14 "
        "L46,-14 C48,-38 46,-72 42,-104 L42,-184 Z"
    )
    cid_lf = _uid("leg_f")
    o.append(f'<defs><clipPath id="{cid_lf}"><path d="{leg_f}"/></clipPath></defs>')
    o.append(f'<path d="{leg_f}" fill="{PAL["pants"]}"/>')
    o.append(f'<g clip-path="url(#{cid_lf})">')
    o.append(f'<path d="M-8,-186 L18,-186 L24,-10 L-8,-10 Z" fill="{PAL["pants_sh"]}" opacity="0.46"/>')
    o.append(_stroke_path("M34,-170 Q38,-110 38,-24", PAL["pants_hi"], 4.8, opacity=0.34))
    o.append(_stroke_path("M10,-102 Q26,-95 42,-102", "#1A222E", 1.5, opacity=0.62))
    o.append(_stroke_path("M14,-44 Q28,-39 44,-45", "#1A222E", 1.3, opacity=0.46))
    o.append('</g>')
    o.append(f'<path d="{leg_f}" fill="none" stroke="{INK}" stroke-width="1.9" stroke-linejoin="round"/>')

    # 4. Spor ayakkabılar (ince 1.8px kontur)
    for sx, sy, dark in [(-32, -16, True), (24, -14, False)]:
        sh_c = PAL["shoe_sh"] if dark else PAL["shoe"]
        sl_c = PAL["shoe_sole_sh"] if dark else PAL["shoe_sole"]
        o.append(
            f'<path d="M{sx-14},{sy} L{sx+18},{sy} C{sx+28},{sy+4} {sx+42},{sy+9} {sx+44},{sy+16} '
            f'L{sx-16},{sy+16} Z" fill="{sh_c}" stroke="{INK}" stroke-width="1.8" stroke-linejoin="round"/>'
        )
        o.append(
            f'<path d="M{sx-16},{sy+13} L{sx+44},{sy+13} Q{sx+45},{sy+19} {sx+40},{sy+20} '
            f'L{sx-14},{sy+20} Q{sx-17},{sy+19} {sx-16},{sy+13} Z" fill="{sl_c}" stroke="{INK}" stroke-width="1.6" stroke-linejoin="round"/>'
        )
        o.append(_stroke_path(f"M{sx+12},{sy+3} L{sx+20},{sy+6} M{sx+17},{sy+6} L{sx+25},{sy+9}", sl_c, 1.5, opacity=0.84))

    # 5. Gövde — 11 yaş çocuk anatomisi (ince 1.9px kontur + kumaş kıvrımları)
    torso_d = (
        "M-46,-314 C-32,-324 -16,-330 2,-330 C22,-330 40,-322 52,-310 "
        "C56,-282 54,-248 48,-212 C46,-196 46,-184 44,-176 "
        "C16,-168 -18,-168 -44,-176 C-46,-192 -48,-222 -48,-254 "
        "C-48,-278 -48,-298 -46,-314 Z"
    )
    cid_t = _uid("torso")
    o.append(f'<defs><clipPath id="{cid_t}"><path d="{torso_d}"/></clipPath></defs>')
    o.append(f'<path d="{torso_d}" fill="{PAL["shirt"]}"/>')
    o.append(f'<g clip-path="url(#{cid_t})">')
    for k in range(7):
        sy = -306 + k * 21.5
        o.append(_stroke_path(f"M-62,{sy-2:.1f} Q4,{sy+6.5:.1f} 66,{sy-3:.1f}", PAL["stripe"], 8.2))
    o.append(f'<path d="M-60,-340 L-12,-340 C-20,-280 -18,-220 -8,-164 L-60,-164 Z" fill="{PAL["shirt_dk"]}" opacity="0.45"/>')
    o.append(f'<path d="M10,-326 C34,-320 48,-292 46,-238 C32,-248 16,-276 10,-326 Z" fill="{PAL["shirt_hi"]}" opacity="0.26"/>')
    o.append(_stroke_path("M-32,-206 Q-8,-196 14,-204", PAL["shirt_dk"], 1.7, opacity=0.52))
    o.append(_stroke_path("M20,-244 Q34,-238 46,-246", PAL["shirt_dk"], 1.6, opacity=0.48))
    o.append(_stroke_path("M-40,-272 Q-26,-266 -18,-276", PAL["shirt_dk"], 1.6, opacity=0.45))
    o.append(f'<path d="M-50,-184 Q0,-176 50,-184 L50,-166 L-50,-166 Z" fill="{PAL["shirt_sh"]}" opacity="0.70"/>')
    o.append(_stroke_path("M-45,-308 C-47,-266 -46,-220 -43,-180", "#9EC4D8", 2.4, opacity=0.34))
    o.append('</g>')
    o.append(f'<path d="{torso_d}" fill="none" stroke="{INK}" stroke-width="1.9" stroke-linejoin="round"/>')

    # Ön (sağ) kol — D2: kısaltılmış, dirsekte belirgin ama doğal hafif kırık (üst kol dışa, ön kol hafif öne-içe)
    arm_fg_fill = (
        "M40,-318 C59,-308 74,-284 78,-250 "
        "C79,-239 75,-226 68,-212 C61,-199 54,-189 48,-182 "
        "L29,-187 C35,-201 43,-217 47,-233 "
        "C49,-245 45,-263 36,-282 Z"
    )
    cid_af = _uid("arm_f")
    o.append(f'<defs><clipPath id="{cid_af}"><path d="{arm_fg_fill}"/></clipPath></defs>')
    o.append(f'<path d="{arm_fg_fill}" fill="{PAL["shirt"]}"/>')
    o.append(f'<g clip-path="url(#{cid_af})">')
    for k in range(7):
        sy = -306 + k * 21.5
        o.append(_stroke_path(f"M22,{sy-2:.1f} Q54,{sy+4.5:.1f} 86,{sy-2:.1f}", PAL["stripe"], 8.0))
    o.append(f'<path d="M22,-320 L48,-320 L44,-178 L22,-178 Z" fill="{PAL["shirt_sh"]}" opacity="0.40"/>')
    # Dirsek içi kumaş kıvrımı
    o.append(_stroke_path("M47,-242 Q62,-235 75,-244", PAL["shirt_dk"], 1.7, opacity=0.60))
    o.append(_stroke_path("M46,-235 Q58,-231 68,-237", PAL["shirt_dk"], 1.2, opacity=0.44))
    o.append(_stroke_path("M70,-290 Q76,-248 58,-190", PAL["shirt_hi"], 3.0, opacity=0.34))
    o.append('</g>')
    # Pürüzsüz dış kol + koltuk altı konturu (omuz dikişinde kırık yok)
    o.append(_stroke_path(
        "M42,-317 C60,-307 74,-284 78,-250 C79,-239 75,-226 68,-212 "
        "C61,-199 54,-189 48,-182 L29,-187 C35,-201 43,-217 47,-233 C49,-247 44,-265 36,-282",
        INK, 1.9))
    o.append(_stroke_path("M36,-282 Q40,-292 44,-298", PAL["shirt_dk"], 1.5, opacity=0.62))
    # Ön kol manşet ribanası
    o.append(f'<path d="M28,-189 Q39,-183 49,-184 L47,-175 Q37,-175 27,-180 Z" '
             f'fill="{PAL["shirt_sh"]}" stroke="{INK}" stroke-width="1.6" stroke-linejoin="round"/>')
    # Ön el (hafif içe-öne doğal eğimli)
    o.append(_cocuk_el(36, -163, scale=0.83, flip_x=1, rot=12, shade_dark=False))

    # 6. Boyun + Yaka Ribanası + Baş (R4 kesin çözüm + ince 1.8px kontur)
    o.append(f'<ellipse cx="2" cy="-323" rx="18" ry="5.5" fill="{PAL["shirt_dk"]}"/>')
    neck_d = "M-14,-362 L-14,-322 Q2,-314 18,-322 L17,-362 Z"
    o.append(f'<path d="{neck_d}" fill="{PAL["skin"]}" stroke="{INK}" stroke-width="1.8" stroke-linejoin="round"/>')
    o.append(f'<path d="M-13,-358 Q3,-338 17,-356 L16,-336 Q2,-326 -13,-338 Z" fill="{PAL["skin_dk"]}" opacity="0.48"/>')
    o.append(f'<path d="M-13,-358 L-4,-358 L-5,-322 L-13,-324 Z" fill="{PAL["skin_sh"]}" opacity="0.50"/>')

    o.append(f'<path d="M-21,-327 C-12,-314 14,-314 25,-327 C27,-318 20,-309 2,-309 C-16,-309 -23,-318 -21,-327 Z" '
             f'fill="{PAL["shirt_sh"]}" stroke="{INK}" stroke-width="1.8" stroke-linejoin="round"/>')
    o.append(_stroke_path("M-14,-318 Q2,-313 18,-318", PAL["shirt_dk"], 1.3, opacity=0.65))

    o.append(f'<g transform="translate(4,-385) scale(0.56)">{kafa_cocuk("3q", ifade, look=0.25, lighting=lighting)}</g>')

    return "".join(o)


# ── Prolog atmosferinde yakın plan portre paneli (kuruldan övgü alan atmosfer + yeni v3 ince konturlu yüz)
def _prolog_portre_panel(x: float, y: float, w: float, h: float) -> str:
    cid = _uid("prolog")
    bg_g = _uid("pbg")
    beam_g = _uid("pbeam")
    vig_g = _uid("pvig")
    o = [
        f'<defs>'
        f'<clipPath id="{cid}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10"/></clipPath>'
        f'<linearGradient id="{bg_g}" x1="0%" y1="0%" x2="100%" y2="100%">'
        f'<stop offset="0%" stop-color="#0A0E16"/>'
        f'<stop offset="58%" stop-color="#131A26"/>'
        f'<stop offset="100%" stop-color="#1D2028"/>'
        f'</linearGradient>'
        f'<linearGradient id="{beam_g}" x1="100%" y1="95%" x2="22%" y2="18%">'
        f'<stop offset="0%" stop-color="#FFD496" stop-opacity="0.54"/>'
        f'<stop offset="42%" stop-color="#F2A95A" stop-opacity="0.22"/>'
        f'<stop offset="100%" stop-color="#F2A95A" stop-opacity="0.0"/>'
        f'</linearGradient>'
        f'<radialGradient id="{vig_g}" cx="52%" cy="50%" r="65%">'
        f'<stop offset="55%" stop-color="#000000" stop-opacity="0.0"/>'
        f'<stop offset="100%" stop-color="#05070B" stop-opacity="0.55"/>'
        f'</radialGradient>'
        f'</defs>',
        f'<g clip-path="url(#{cid})">',
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#{bg_g})"/>',
    ]
    for k in range(10):
        px = x + k * 88
        o.append(f'<rect x="{px}" y="{y}" width="3" height="{h}" fill="#070A10" opacity="0.55"/>')
    o.append(f'<polygon points="{x+w},{y+h} {x+w},{y+h-38} {x+w*0.28},{y+14} {x+w*0.18},{y+h}" fill="url(#{beam_g})"/>')
    o.append(f'<rect x="{x+w-160}" y="{y+h-11}" width="160" height="6" fill="#FFE8BC" opacity="0.90"/>')
    o.append(f'<rect x="{x+w-175}" y="{y+h-18}" width="175" height="18" fill="#FFBE6B" opacity="0.24"/>')

    cx, cy = x + w * 0.50, y + h * 0.58
    o.append(f'<g transform="translate({cx:.1f},{cy+84:.1f}) scale(1.02)">'
             f'<path d="M-86,44 C-74,-6 -48,-24 0,-24 C48,-24 76,-6 88,44 Z" fill="#4E251D" stroke="{INK}" stroke-width="2.0"/>'
             f'<path d="M-66,12 Q0,20 68,12" fill="none" stroke="#85745F" stroke-width="10" opacity="0.62"/>'
             f'<path d="M-22,-32 L-21,-15 Q0,-5 21,-15 L19,-32 Z" fill="#8C6552" stroke="{INK}" stroke-width="1.8"/>'
             f'<path d="M-27,-21 C-14,-8 14,-8 27,-21 C27,-12 18,-4 0,-4 C-18,-4 -27,-12 -27,-21 Z" fill="#3B1B15" stroke="{INK}" stroke-width="1.7"/>'
             f'<path d="M26,-19 C56,-13 74,4 82,36" fill="none" stroke="#FFD699" stroke-width="3.6" opacity="0.70" stroke-linecap="round"/>'
             f'</g>')
    o.append(f'<g transform="translate({cx:.1f},{cy-12:.1f}) scale(0.80)">'
             f'{kafa_cocuk("3q", "korku", look=0.36, lighting="prolog_warm")}</g>')

    dust = [(0.64, 0.28, 1.8), (0.72, 0.42, 1.4), (0.78, 0.62, 2.0), (0.68, 0.72, 1.2),
            (0.84, 0.48, 1.5), (0.58, 0.66, 1.3), (0.88, 0.78, 1.9)]
    for dx, dy, dr in dust:
        o.append(f'<circle cx="{x+w*dx:.1f}" cy="{y+h*dy:.1f}" r="{dr:.1f}" fill="#FFE9BE" opacity="0.70"/>')

    o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#{vig_g})"/>')

    o.append(f'<text x="{x+18}" y="{y+26}" font-family="DejaVu Sans, Segoe UI, sans-serif" font-size="12" '
             f'font-weight="bold" fill="#F0C892" letter-spacing="1.2">PROLOG ATMOSFERİ · KARANLIK DEPO</text>')
    o.append(f'<text x="{x+18}" y="{y+44}" font-family="DejaVu Sans, Segoe UI, sans-serif" font-size="11" '
             f'fill="#9AA8BA">Kapı altından sızan sıcak ışık çizgisi · gözde parlama</text>')
    o.append('</g>')
    o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="none" stroke="#3D4C60" stroke-width="1.4"/>')
    return "".join(o)


def _card_bg(w: int, h: int) -> str:
    o = [
        '<defs>'
        '<radialGradient id="card_bg" cx="24%" cy="46%" r="78%">'
        '<stop offset="0%" stop-color="#222C3A"/>'
        '<stop offset="55%" stop-color="#171E28"/>'
        '<stop offset="100%" stop-color="#10151D"/>'
        '</radialGradient>'
        '<radialGradient id="hero_halo" cx="50%" cy="50%" r="50%">'
        '<stop offset="0%" stop-color="#3C5068" stop-opacity="0.44"/>'
        '<stop offset="70%" stop-color="#243142" stop-opacity="0.14"/>'
        '<stop offset="100%" stop-color="#171E28" stop-opacity="0.0"/>'
        '</radialGradient>'
        '<radialGradient id="warm_halo" cx="50%" cy="50%" r="50%">'
        '<stop offset="0%" stop-color="#F2C28B" stop-opacity="0.20"/>'
        '<stop offset="65%" stop-color="#F2C28B" stop-opacity="0.05"/>'
        '<stop offset="100%" stop-color="#19202B" stop-opacity="0.0"/>'
        '</radialGradient>'
        '</defs>',
        f'<rect width="{w}" height="{h}" fill="url(#card_bg)"/>',
    ]
    for gx in range(40, w, 40):
        o.append(f'<line x1="{gx}" y1="0" x2="{gx}" y2="{h}" stroke="{PLAN}" stroke-width="0.6" opacity="0.04"/>')
    for gy in range(40, h, 40):
        o.append(f'<line x1="0" y1="{gy}" x2="{w}" y2="{gy}" stroke="{PLAN}" stroke-width="0.6" opacity="0.04"/>')
    return "".join(o)


def build_model_card_svg() -> str:
    W, H = 1280, 720
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
    o.append(_card_bg(W, H))

    # Üst başlık barı + A-Y ile hizalı renk paleti göstergesi
    o.append('<text x="32" y="36" font-family="DejaVu Sans, Segoe UI, sans-serif" font-size="19" '
             'font-weight="bold" fill="#EEF3F8" letter-spacing="0.8">MICHAEL SCOFIELD · 11 YAŞ MODEL KARTI v3</text>')
    o.append('<text x="530" y="36" font-family="DejaVu Sans, Segoe UI, sans-serif" font-size="11.5" '
             'fill="#8D9DB0">STİL B+A HİBRİT · PROLOG &amp; BÖLÜM I · DÖVME YOK (R3)</text>')

    swatches = [("TEN", PAL["skin"]), ("SAÇ", PAL["hair"]), ("GÖZ", PAL["iris"]), ("KAZAK", PAL["shirt"]), ("PLAN", PLAN)]
    for i, (lbl, col) in enumerate(swatches):
        sx = 940 + i * 64
        o.append(f'<rect x="{sx}" y="22" width="13" height="13" rx="3" fill="{col}" stroke="#4E5F73" stroke-width="0.9"/>')
        o.append(f'<text x="{sx+17}" y="33" font-family="DejaVu Sans, Segoe UI, sans-serif" font-size="9.5" fill="#9BB0C4">{lbl}</text>')
    o.append('<line x1="32" y1="48" x2="1248" y2="48" stroke="#324154" stroke-width="1.1"/>')

    # ── SOL PANEL: Tam boy 11 yaş Michael
    o.append('<rect x="32" y="64" width="356" height="628" rx="12" fill="#131922" fill-opacity="0.72" stroke="#2D3B4D" stroke-width="1.3"/>')
    o.append('<ellipse cx="210" cy="390" rx="145" ry="250" fill="url(#hero_halo)"/>')
    for gy, lbl in [(162, "BAŞ ÜSTÜ"), (292, "OMUZ"), (452, "BEL"), (640, "ZEMİN")]:
        o.append(f'<line x1="52" y1="{gy}" x2="368" y2="{gy}" stroke="{PLAN}" stroke-width="0.8" stroke-dasharray="4 5" opacity="0.16"/>')
        o.append(f'<text x="56" y="{gy-5}" font-family="DejaVu Sans, Segoe UI, sans-serif" font-size="9" fill="#6F8999" opacity="0.72">{lbl}</text>')

    o.append(f'<g transform="translate(210, 636) scale(1.06)">{figur_cocuk("odak", lighting="studio")}</g>')
    o.append('<text x="210" y="676" text-anchor="middle" font-family="DejaVu Sans, Segoe UI, sans-serif" '
             'font-size="12" font-weight="bold" fill="#DCE5F0">TAM BOY · 3/4 DURUŞ (11 YAŞ)</text>')

    # ── ÜST SAĞ: 3 Görünüş (Önden, 3/4, Yandan — A-Y gibi boyun kesitli)
    o.append('<rect x="410" y="64" width="838" height="214" rx="12" fill="#131922" fill-opacity="0.72" stroke="#2D3B4D" stroke-width="1.3"/>')
    o.append('<text x="428" y="86" font-family="DejaVu Sans, Segoe UI, sans-serif" font-size="11.5" '
             'font-weight="bold" fill="#7FE6FF" letter-spacing="1.0">ÜÇ GÖRÜNÜŞ (ÖNDEN · 3/4 · YANDAN)</text>')
    o.append('<line x1="440" y1="168" x2="1220" y2="168" stroke="#7FE6FF" stroke-width="0.8" stroke-dasharray="5 5" opacity="0.20"/>')

    views = [("front", "ÖNDEN", 550, 0.0), ("3q", "3/4 (ANA AÇI)", 828, 0.22), ("side", "YANDAN (PROFİL)", 1106, 0.14)]
    for vw, label, vx, lk in views:
        o.append(f'<g transform="translate({vx}, 170) scale(0.64)">{kafa_cocuk(vw, "odak", look=lk, lighting="studio", boyun=True)}</g>')
        o.append(f'<text x="{vx}" y="266" text-anchor="middle" font-family="DejaVu Sans, Segoe UI, sans-serif" '
                 f'font-size="11" fill="#C4D2E2">{label}</text>')

    # ── ORTA SAĞ: 5 İfade
    o.append('<rect x="410" y="292" width="838" height="190" rx="12" fill="#131922" fill-opacity="0.72" stroke="#2D3B4D" stroke-width="1.3"/>')
    o.append('<text x="428" y="314" font-family="DejaVu Sans, Segoe UI, sans-serif" font-size="11.5" '
             'font-weight="bold" fill="#7FE6FF" letter-spacing="1.0">BEŞ İFADE (ODAK · KORKU · YAS · ŞEFKAT · KARARLI)</text>')

    exprs = [
        ("odak",    "odak",    "studio",     0.22),
        ("korku",   "korku",   "depo_korku", 0.34),
        ("yas",     "yas",     "studio",     0.10),
        ("sefkat",  "şefkat",  "studio",     0.20),
        ("kararli", "kararlı", "studio",     0.26),
    ]
    for i, (key, label, lgt, lk) in enumerate(exprs):
        ex = 496 + i * 166
        bg_box = "#101620" if key == "korku" else "#18212D"
        st_box = "#44556A" if key != "korku" else "#735840"
        o.append(f'<rect x="{ex-72}" y="324" width="144" height="146" rx="8" fill="{bg_box}" stroke="{st_box}" stroke-width="1.0"/>')
        o.append(f'<g transform="translate({ex}, 392) scale(0.50)">{kafa_cocuk("3q", key, look=lk, lighting=lgt)}</g>')
        o.append(f'<text x="{ex}" y="460" text-anchor="middle" font-family="DejaVu Sans, Segoe UI, sans-serif" '
                 f'font-size="11.5" fill="{"#F0C892" if key=="korku" else "#C8D5E4"}">{label}</text>')

    # ── ALT SAĞ: Prolog Atmosferinde Yakın Plan Portre
    o.append(_prolog_portre_panel(410, 496, 838, 196))

    o.append('</svg>')
    return "".join(o)


def build_r13_card_svg() -> str:
    """R13 %200 Kırpma Kontrol Kartı (v3, 1280x720) — 4 büyük yakın plan panel."""
    W, H = 1280, 720
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
    o.append(_card_bg(W, H))

    o.append('<text x="32" y="36" font-family="DejaVu Sans, Segoe UI, sans-serif" font-size="18" '
             'font-weight="bold" fill="#EEF3F8" letter-spacing="0.8">MICHAEL 11 YAŞ · R13 (%200) YAKIN PLAN KONTROL KARTI v3</text>')
    o.append('<text x="1248" y="34" text-anchor="end" font-family="DejaVu Sans, Segoe UI, sans-serif" '
             'font-size="11" fill="#8D9DB0">R1 · R3 · R4 · R10 · G1 · D2 DOĞRULAMA</text>')
    o.append('<line x1="32" y1="48" x2="1248" y2="48" stroke="#324154" stroke-width="1.1"/>')

    panels = [
        (32,  62, 600, 308, "1 · 3/4 ODAK YÜZ YAKIN (%200)",    "#161E29", "odak_face"),
        (648, 62, 600, 308, "2 · KORKU İFADESİ YAKIN (%200)",   "#10151E", "korku_face"),
        (32,  386, 600, 308, "3 · ŞEFKAT İFADESİ YAKIN (%200)", "#19202B", "sefkat_face"),
        (648, 386, 600, 308, "4 · BOYUN-YAKA-OMUZ YAKIN (R4)",  "#161E29", "neck_joint"),
    ]
    for px, py, pw, ph, title, bg, mode in panels:
        cid = _uid("r13")
        o.append(f'<defs><clipPath id="{cid}"><rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="10"/></clipPath></defs>')
        o.append(f'<g clip-path="url(#{cid})">')
        o.append(f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" fill="{bg}"/>')
        cx, cy = px + pw * 0.5, py + ph * 0.54
        if mode == "odak_face":
            o.append(f'<g transform="translate({cx:.1f},{cy:.1f}) scale(1.24)">{kafa_cocuk("3q", "odak", look=0.22, lighting="studio")}</g>')
        elif mode == "korku_face":
            bg_b = _uid("kbeam")
            o.append(f'<defs><linearGradient id="{bg_b}" x1="100%" y1="90%" x2="30%" y2="30%">'
                     f'<stop offset="0%" stop-color="#F2AA5C" stop-opacity="0.28"/>'
                     f'<stop offset="100%" stop-color="#F2AA5C" stop-opacity="0.0"/>'
                     f'</linearGradient></defs>')
            o.append(f'<polygon points="{px+pw},{py+ph} {px+pw},{py+36} {px+pw*0.30},{py+ph}" fill="url(#{bg_b})"/>')
            o.append(f'<g transform="translate({cx:.1f},{cy:.1f}) scale(1.24)">{kafa_cocuk("3q", "korku", look=0.34, lighting="depo_korku")}</g>')
        elif mode == "sefkat_face":
            o.append(f'<ellipse cx="{cx+20:.1f}" cy="{cy-10:.1f}" rx="220" ry="155" fill="url(#warm_halo)"/>')
            o.append(f'<g transform="translate({cx:.1f},{cy:.1f}) scale(1.24)">{kafa_cocuk("3q", "sefkat", look=0.20, lighting="studio")}</g>')
        elif mode == "neck_joint":
            o.append(f'<g transform="translate({cx-6:.1f},{py+ph*0.5+664:.1f}) scale(2.05)">{figur_cocuk("odak", lighting="studio")}</g>')
            o.append(f'<line x1="{px+20}" y1="{py+ph*0.52:.1f}" x2="{px+pw-20}" y2="{py+ph*0.52:.1f}" '
                     f'stroke="{PLAN}" stroke-width="0.8" stroke-dasharray="4 5" opacity="0.22"/>')
        o.append(f'<rect x="{px+12}" y="{py+10}" width="268" height="24" rx="5" fill="#0B0F16" opacity="0.72"/>')
        o.append(f'<text x="{px+22}" y="{py+26}" font-family="DejaVu Sans, Segoe UI, sans-serif" font-size="11.5" '
                 f'font-weight="bold" fill="#7FE6FF">{title}</text>')
        o.append('</g>')
        o.append(f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="10" fill="none" stroke="#36475C" stroke-width="1.4"/>')

    o.append('</svg>')
    return "".join(o)


def render_svg_to_png(svg_str: str, out_path: Path, width: int = 1280, height: int = 720) -> None:
    png_bytes = resvg_py.svg_to_bytes(svg_string=svg_str, width=width, height=height)
    img = Image.open(BytesIO(png_bytes)).convert("RGBA")
    img.save(out_path, "PNG")


def main() -> None:
    model_svg = build_model_card_svg()
    r13_svg = build_r13_card_svg()
    out_model = OUT_DIR / "ac_cocuk_v3.png"
    out_r13 = OUT_DIR / "ac_cocuk_r13_v3.png"
    render_svg_to_png(model_svg, out_model)
    render_svg_to_png(r13_svg, out_r13)
    print(f"Üretildi: {out_model}")
    print(f"Üretildi: {out_r13}")


if __name__ == "__main__":
    main()
