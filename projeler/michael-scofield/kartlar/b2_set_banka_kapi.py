"""V6 (Act II: Polite Bank Robbery, Inmate File #94941 & Fox River Gates).

Style B+A Hybrid (Cinematic 2D + Cyan Blueprint Vision) — 5-layer parallax-ready scenes (960x540):
  - set_205_banka(katmanlar=None)       -> (defs_str, body_str)
  - set_206_dosya_94941(katmanlar=None) -> (defs_str, body_str)
  - set_207_fox_kapilar(katmanlar=None) -> (defs_str, body_str)

All on-screen text is in ENGLISH. All stroked <path> elements explicitly set fill="none".
Uses locked Michael v3 assets K.michael_kafa and K.michael_figur from karakter.py without modifying it.
"""
from __future__ import annotations

import io
import math
import random
import sys
from pathlib import Path

import resvg_py
from PIL import Image, ImageDraw, ImageFont

OUT_DIR = Path(__file__).resolve().parent
PROJ_DIR = OUT_DIR.parent
if str(PROJ_DIR) not in sys.path:
    sys.path.insert(0, str(PROJ_DIR))

import karakter as K  # noqa: E402

W_SCENE, H_SCENE = 960, 540

INK = "#11161D"
INK_WARM = "#1A130F"
PLAN = "#7FE6FF"
PLAN_CORE = "#DDFBFF"
RED_ALERT = "#E63244"
SIREN_BLUE = "#2E8CFF"
SIREN_RED = "#FF2E48"

_UID = 0


def _uid(prefix: str = "b2") -> str:
    global _UID
    _UID += 1
    return f"{prefix}_{_UID}"


def _katman_aktif(katmanlar: set[str] | list[str] | None, ad: str) -> bool:
    return katmanlar is None or ad in katmanlar


# =============================================================================
# SCENE 2.05: POLITE BANK ROBBERY ("POLITELY")
# =============================================================================
def set_205_banka(
    katmanlar: set[str] | list[str] | None = None,
) -> tuple[str, str]:
    """Grand Chicago marble bank lobby with brass teller grilles, velvet stanchions,
    red-blue police siren glow outside glass doors, gentle ceiling plaster dust falling
    (zero violence/blood), and calm suited Michael politely placing a dark pistol
    silhouette on the polished counter. Dry-humor highlight: 'POLITELY'.
    """
    rng = random.Random(205)
    p = _uid("s205")

    defs = f"""
    <linearGradient id="{p}_night_ext" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#060B14"/>
      <stop offset="55%" stop-color="#0E1828"/>
      <stop offset="100%" stop-color="#172438"/>
    </linearGradient>
    <radialGradient id="{p}_siren_blue" cx="0.24" cy="0.46" r="0.38">
      <stop offset="0%" stop-color="{SIREN_BLUE}" stop-opacity="0.72"/>
      <stop offset="45%" stop-color="{SIREN_BLUE}" stop-opacity="0.24"/>
      <stop offset="100%" stop-color="{SIREN_BLUE}" stop-opacity="0.0"/>
    </radialGradient>
    <radialGradient id="{p}_siren_red" cx="0.76" cy="0.46" r="0.38">
      <stop offset="0%" stop-color="{SIREN_RED}" stop-opacity="0.68"/>
      <stop offset="45%" stop-color="{SIREN_RED}" stop-opacity="0.22"/>
      <stop offset="100%" stop-color="{SIREN_RED}" stop-opacity="0.0"/>
    </radialGradient>
    <linearGradient id="{p}_wall_marble" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#1F242B"/>
      <stop offset="35%" stop-color="#2D323A"/>
      <stop offset="78%" stop-color="#22262D"/>
      <stop offset="100%" stop-color="#14171C"/>
    </linearGradient>
    <linearGradient id="{p}_col_grad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#7E7970"/>
      <stop offset="22%" stop-color="#CEC8BC"/>
      <stop offset="48%" stop-color="#E5E0D5"/>
      <stop offset="76%" stop-color="#9A948A"/>
      <stop offset="100%" stop-color="#4A4640"/>
    </linearGradient>
    <linearGradient id="{p}_brass" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F7DF94"/>
      <stop offset="35%" stop-color="#C99A45"/>
      <stop offset="72%" stop-color="#E5C068"/>
      <stop offset="100%" stop-color="#7E591E"/>
    </linearGradient>
    <linearGradient id="{p}_brass_v" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#F6DC8D"/>
      <stop offset="50%" stop-color="#B98B38"/>
      <stop offset="100%" stop-color="#6F4E19"/>
    </linearGradient>
    <linearGradient id="{p}_wood_dark" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#3C2518"/>
      <stop offset="50%" stop-color="#291810"/>
      <stop offset="100%" stop-color="#170D08"/>
    </linearGradient>
    <linearGradient id="{p}_counter_top" x1="0" y1="0" x2="1" y2="0.4">
      <stop offset="0%" stop-color="#C8C3B8"/>
      <stop offset="35%" stop-color="#ECE8DF"/>
      <stop offset="68%" stop-color="#D6D1C6"/>
      <stop offset="100%" stop-color="#8F8A80"/>
    </linearGradient>
    <linearGradient id="{p}_floor" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#1A1E24"/>
      <stop offset="50%" stop-color="#252930"/>
      <stop offset="100%" stop-color="#12151A"/>
    </linearGradient>
    <radialGradient id="{p}_chandelier_glow" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0%" stop-color="#FFE6A3" stop-opacity="0.62"/>
      <stop offset="45%" stop-color="#D69A42" stop-opacity="0.22"/>
      <stop offset="100%" stop-color="#D69A42" stop-opacity="0.0"/>
    </radialGradient>
    <radialGradient id="{p}_dust_cloud" cx="0.5" cy="0.45" r="0.5">
      <stop offset="0%" stop-color="#F2EFE8" stop-opacity="0.46"/>
      <stop offset="55%" stop-color="#D9D5CC" stop-opacity="0.16"/>
      <stop offset="100%" stop-color="#D9D5CC" stop-opacity="0.0"/>
    </radialGradient>
    <linearGradient id="{p}_suit" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#2D333D"/>
      <stop offset="55%" stop-color="#1D2229"/>
      <stop offset="100%" stop-color="#111419"/>
    </linearGradient>
    <linearGradient id="{p}_velvet" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#A82433"/>
      <stop offset="55%" stop-color="#6E121D"/>
      <stop offset="100%" stop-color="#3F080F"/>
    </linearGradient>
    <radialGradient id="{p}_vig" cx="0.5" cy="0.48" r="0.68">
      <stop offset="55%" stop-color="#000000" stop-opacity="0.0"/>
      <stop offset="100%" stop-color="#05070B" stop-opacity="0.68"/>
    </radialGradient>
    <clipPath id="{p}_door_clip">
      <rect x="332" y="106" width="296" height="210" rx="4"/>
    </clipPath>
    <clipPath id="{p}_mhead_clip">
      <rect x="260" y="130" width="140" height="140"/>
    </clipPath>
    """

    parts: list[str] = []

    # ── LAYER 1: uzak (Night Chicago street + glass entrance + police sirens) ──
    if _katman_aktif(katmanlar, "uzak"):
        uzak: list[str] = [f'<g id="s205-uzak">']
        uzak.append(f'<rect x="0" y="0" width="960" height="540" fill="url(#{p}_wall_marble)"/>')
        # Arched glass entrance bay
        uzak.append(f'<rect x="332" y="106" width="296" height="210" fill="url(#{p}_night_ext)"/>')
        uzak.append(f'<g clip-path="url(#{p}_door_clip)">')
        # Distant Chicago buildings across street
        for bx, bw, bh in [(336, 44, 130), (384, 56, 155), (446, 62, 120), (514, 52, 148), (570, 58, 135)]:
            by = 296 - bh
            uzak.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" fill="#0A111D"/>')
            for wy in range(by + 12, 275, 16):
                for wx in range(bx + 7, bx + bw - 8, 12):
                    if rng.random() > 0.58:
                        uzak.append(f'<rect x="{wx}" y="{wy}" width="5" height="7" fill="#E9C77B" opacity="{rng.uniform(0.18, 0.45):.2f}"/>')
        # Police cruisers silhouettes outside
        uzak.append(
            '<path d="M342,296 L354,274 L416,274 L434,296 Z" fill="#090D14"/>'
            '<rect x="372" y="268" width="26" height="6" rx="2" fill="#182230"/>'
            '<rect x="373" y="268" width="11" height="5" fill="#4BA3FF"/>'
            '<rect x="386" y="268" width="11" height="5" fill="#FF445A"/>'
            '<path d="M520,296 L536,272 L602,272 L620,296 Z" fill="#090D14"/>'
            '<rect x="556" y="266" width="26" height="6" rx="2" fill="#182230"/>'
            '<rect x="557" y="266" width="11" height="5" fill="#FF445A"/>'
            '<rect x="570" y="266" width="11" height="5" fill="#4BA3FF"/>'
        )
        # Police siren volumetric cones through glass
        uzak.append(f'<rect x="332" y="106" width="296" height="210" fill="url(#{p}_siren_blue)"/>')
        uzak.append(f'<rect x="332" y="106" width="296" height="210" fill="url(#{p}_siren_red)"/>')
        # Glass door reflections & mullions
        uzak.append(
            '<path d="M350,106 L396,316 M414,106 L448,316 M552,106 L584,316" fill="none" stroke="#CFE9FF" stroke-width="8" opacity="0.06"/>'
            '<line x1="406" y1="106" x2="406" y2="316" stroke="#1E252E" stroke-width="5"/>'
            '<line x1="480" y1="106" x2="480" y2="316" stroke="#151B22" stroke-width="7"/>'
            '<line x1="554" y1="106" x2="554" y2="316" stroke="#1E252E" stroke-width="5"/>'
            '<line x1="332" y1="168" x2="628" y2="168" stroke="#1B222A" stroke-width="6"/>'
            # Brass push bars on doors
            '<rect x="414" y="236" width="58" height="5" rx="2" fill="url(#' + p + '_brass)"/>'
            '<rect x="488" y="236" width="58" height="5" rx="2" fill="url(#' + p + '_brass)"/>'
        )
        uzak.append("</g>")
        # Arch frame around glass entrance
        uzak.append(
            f'<rect x="328" y="102" width="304" height="218" rx="4" fill="none" stroke="url(#{p}_brass)" stroke-width="5"/>'
            f'<rect x="334" y="108" width="292" height="206" fill="none" stroke="{INK}" stroke-width="2"/>'
        )
        uzak.append("</g>")
        parts.append("".join(uzak))

    # ── LAYER 2: orta (Marble columns, cornice, brass teller grilles, ceiling plaster dust) ──
    if _katman_aktif(katmanlar, "orta"):
        orta: list[str] = [f'<g id="s205-orta">']
        # Coffered ceiling & cornice
        orta.append(
            f'<rect x="0" y="0" width="960" height="82" fill="#181B21"/>'
            f'<rect x="0" y="70" width="960" height="16" fill="#3B3833" stroke="{INK}" stroke-width="1.5"/>'
            f'<rect x="0" y="84" width="960" height="6" fill="url(#{p}_brass)"/>'
        )
        # Bank header plaque positioned cleanly at top frieze (above chandelier)
        orta.append(
            f'<rect x="336" y="12" width="288" height="28" rx="2" fill="#13171D" stroke="url(#{p}_brass)" stroke-width="2.2"/>'
            '<text x="480" y="31" text-anchor="middle" font-family="Georgia, Times New Roman, serif" font-weight="bold" '
            'font-size="14" letter-spacing="2.6" fill="#F2D78E">FIRST CHICAGO TRUST</text>'
        )

        # Side walnut wall paneling & marble wainscoting
        for wx, ww in [(0, 326), (634, 326)]:
            orta.append(f'<rect x="{wx}" y="90" width="{ww}" height="240" fill="url(#{p}_wood_dark)" stroke="{INK}" stroke-width="2"/>')
            for px in range(wx + 24, wx + ww - 24, 96):
                orta.append(
                    f'<rect x="{px}" y="114" width="76" height="176" rx="2" fill="#23140D" stroke="#4D3121" stroke-width="1.5"/>'
                    f'<rect x="{px + 7}" y="121" width="62" height="162" fill="none" stroke="#160C07" stroke-width="1.2"/>'
                )

        # Back brass teller cages (left & right wings)
        for tx_base, label in [(112, "TELLER 01"), (674, "TELLER 02")]:
            orta.append(
                f'<rect x="{tx_base}" y="142" width="174" height="166" fill="#12151B" stroke="url(#{p}_brass)" stroke-width="3"/>'
                f'<rect x="{tx_base + 22}" y="150" width="130" height="18" rx="2" fill="#1E1812" stroke="url(#{p}_brass)" stroke-width="1.3"/>'
                f'<text x="{tx_base + 87}" y="163" text-anchor="middle" font-family="DejaVu Sans, Arial, sans-serif" font-weight="bold" font-size="10.5" letter-spacing="1.8" fill="#E7CA7E">{label}</text>'
            )
            # Brass vertical grille bars
            for gx in range(tx_base + 12, tx_base + 166, 13):
                orta.append(f'<line x1="{gx}" y1="172" x2="{gx}" y2="306" stroke="url(#{p}_brass_v)" stroke-width="2.6"/>')
            # Arched teller pass-through window
            orta.append(
                f'<path d="M{tx_base + 54},306 L{tx_base + 54},242 Q{tx_base + 87},216 {tx_base + 120},242 L{tx_base + 120},306 Z" '
                f'fill="#0A0D12" stroke="url(#{p}_brass)" stroke-width="3"/>'
            )

        # Four grand fluted marble columns
        for cx in [78, 294, 666, 882]:
            orta.append(
                f'<rect x="{cx - 26}" y="90" width="52" height="252" fill="url(#{p}_col_grad)" stroke="{INK}" stroke-width="2"/>'
                # Capital & base
                f'<rect x="{cx - 34}" y="86" width="68" height="16" rx="2" fill="#CFC9BD" stroke="{INK}" stroke-width="1.8"/>'
                f'<rect x="{cx - 30}" y="102" width="60" height="8" fill="url(#{p}_brass)"/>'
                f'<rect x="{cx - 34}" y="330" width="68" height="16" rx="2" fill="#8B857B" stroke="{INK}" stroke-width="1.8"/>'
            )
            for fl in (-14, -5, 5, 14):
                orta.append(f'<line x1="{cx + fl}" y1="112" x2="{cx + fl}" y2="328" stroke="#625E57" stroke-width="1.4" opacity="0.55"/>')

        # Grand brass chandelier hanging cleanly below the top frieze + ceiling plaster puff (zero violence)
        orta.append(
            f'<ellipse cx="480" cy="96" rx="92" ry="42" fill="url(#{p}_chandelier_glow)"/>'
            f'<ellipse cx="566" cy="58" rx="54" ry="26" fill="url(#{p}_dust_cloud)"/>'
            # Small plaster chip crater in ceiling
            '<ellipse cx="566" cy="48" rx="8" ry="3.5" fill="#0B0D11" stroke="#CFCBC2" stroke-width="1.5"/>'
            '<path d="M558,48 L549,54 M574,48 L583,55 M566,51 L564,60" fill="none" stroke="#C5C0B5" stroke-width="1.2" opacity="0.8"/>'
            # Chandelier chain & ring
            f'<line x1="480" y1="42" x2="480" y2="74" stroke="url(#{p}_brass)" stroke-width="3.2"/>'
            f'<path d="M430,92 Q480,106 530,92" fill="none" stroke="url(#{p}_brass)" stroke-width="3.8"/>'
            f'<path d="M446,76 Q480,88 514,76" fill="none" stroke="url(#{p}_brass)" stroke-width="2.4"/>'
        )
        for lx in [434, 456, 480, 504, 526]:
            orta.append(
                f'<rect x="{lx - 2.5}" y="78" width="5" height="14" rx="1.5" fill="#F8F1DC"/>'
                f'<circle cx="{lx}" cy="75" r="4.5" fill="#FFE8A6" opacity="0.92"/>'
            )
        # Falling fine white plaster flakes & dust trail from ceiling
        for _ in range(38):
            dx = rng.uniform(508, 592)
            dy = rng.uniform(42, 290)
            dr = rng.uniform(0.9, 2.8)
            op = rng.uniform(0.28, 0.78)
            orta.append(f'<circle cx="{dx:.1f}" cy="{dy:.1f}" r="{dr:.1f}" fill="#EAE6DC" opacity="{op:.2f}"/>')
        for px, py, sz in [(536, 98, 4.5), (558, 134, 3.8), (544, 178, 5.0), (566, 214, 3.2), (528, 238, 4.0)]:
            orta.append(
                f'<polygon points="{px},{py} {px + sz},{py + 1.5} {px + sz * 0.6},{py + sz} {px - 1},{py + sz * 0.7}" '
                f'fill="#E4DFD4" stroke="#7E7A72" stroke-width="0.6" opacity="0.88"/>'
            )

        orta.append("</g>")
        parts.append("".join(orta))

    # ── LAYER 3: sahne (Marble floor, velvet stanchions, counter, suited Michael & pistol) ──
    if _katman_aktif(katmanlar, "sahne"):
        sahne: list[str] = [f'<g id="s205-sahne">']
        # Polished marble floor with perspective grid & siren reflection
        sahne.append(f'<rect x="0" y="330" width="960" height="210" fill="url(#{p}_floor)"/>')
        for fy in [346, 368, 396, 432, 478, 534]:
            sahne.append(f'<line x1="0" y1="{fy}" x2="960" y2="{fy}" stroke="#383E48" stroke-width="1.2" opacity="0.55"/>')
        for fx in range(-120, 1120, 110):
            dx_top = 480 + (fx - 480) * 0.36
            sahne.append(f'<line x1="{dx_top:.1f}" y1="330" x2="{fx}" y2="540" stroke="#383E48" stroke-width="1.2" opacity="0.48"/>')
        # Blue-red siren reflections on floor
        sahne.append(
            f'<ellipse cx="388" cy="368" rx="120" ry="26" fill="{SIREN_BLUE}" opacity="0.16"/>'
            f'<ellipse cx="574" cy="368" rx="120" ry="26" fill="{SIREN_RED}" opacity="0.14"/>'
        )

        # Velvet rope stanchions (left & right)
        for sx1, sx2 in [(136, 254), (712, 834)]:
            for sx in (sx1, sx2):
                sahne.append(
                    f'<ellipse cx="{sx}" cy="396" rx="15" ry="5" fill="#0A0C10" opacity="0.65"/>'
                    f'<ellipse cx="{sx}" cy="393" rx="12" ry="4" fill="url(#{p}_brass)" stroke="{INK}" stroke-width="1.2"/>'
                    f'<rect x="{sx - 3}" y="314" width="6" height="79" fill="url(#{p}_brass)" stroke="{INK}" stroke-width="1.2"/>'
                    f'<circle cx="{sx}" cy="312" r="6.5" fill="url(#{p}_brass)" stroke="{INK}" stroke-width="1.3"/>'
                )
            mid_x = (sx1 + sx2) / 2
            sahne.append(
                f'<path d="M{sx1 + 4},324 Q{mid_x},362 {sx2 - 4},324" fill="none" stroke="{INK}" stroke-width="9" stroke-linecap="round"/>'
                f'<path d="M{sx1 + 4},324 Q{mid_x},362 {sx2 - 4},324" fill="none" stroke="url(#{p}_velvet)" stroke-width="6.5" stroke-linecap="round"/>'
                f'<path d="M{sx1 + 6},322 Q{mid_x},358 {sx2 - 6},322" fill="none" stroke="#D95766" stroke-width="1.4" opacity="0.45" stroke-linecap="round"/>'
            )

        # Calm Michael in dark tailored suit behind counter (left-center)
        # R4-Anatomy: Shoulder width ~2.2x head width (138px vs 62.6px), crisp athletic suit,
        # Collar-Over-Neck Z-Order (shirt collar, tie knot & jacket lapels drawn OVER neck).
        m_head = K.michael_kafa("3q", "odak", look=0.35, boyun=True)
        sahne.append(
            '<g id="s205-michael">'
            # Left (far/relaxed) suit arm resting calmly at his side
            f'<path d="M276,264 C264,270 258,284 256,310 L252,386 L284,386 L288,314 L292,274 Z" '
            f'fill="#1A1F26" stroke="{INK}" stroke-width="2.2" stroke-linejoin="round"/>'
            # Athletic V-tapered tailored charcoal suit torso (shoulder span ~138px = 2.2x head width)
            f'<path d="M266,266 C278,255 304,249 334,249 C364,249 390,255 402,268 '
            f'L394,386 L274,386 Z" '
            f'fill="url(#{p}_suit)" stroke="{INK}" stroke-width="2.3" stroke-linejoin="round"/>'
            # Subtle shoulder highlight & structured seam
            '<path d="M272,266 Q298,256 320,254 M348,254 Q374,256 396,268" '
            'fill="none" stroke="#4D5766" stroke-width="1.6" opacity="0.55" stroke-linecap="round"/>'
            # 1) Locked Michael v3 head WITH neck (drawn BEFORE collar/tie/lapels!)
            f'<g transform="translate(336, 198) scale(0.46)">{m_head}</g>'
            # 2) COLLAR-OVER-NECK Z-ORDER: Crisp white shirt V-front & spread collar wings OVER neck base
            f'<path d="M316,251 L336,314 L356,251 Q336,260 316,251 Z" '
            f'fill="#F2EFE8" stroke="{INK}" stroke-width="1.4" stroke-linejoin="round"/>'
            # Left & right spread shirt collar wings wrapping cleanly over neck
            f'<path d="M316,249 L321,264 L334,262 L322,247 Z" fill="#FAF8F2" stroke="{INK}" stroke-width="1.5" stroke-linejoin="round"/>'
            f'<path d="M354,249 L349,264 L337,262 L348,247 Z" fill="#ECE8DF" stroke="{INK}" stroke-width="1.5" stroke-linejoin="round"/>'
            # Silk charcoal tie knot (Windsor) & slim blade over shirt
            f'<path d="M331,260 L341,260 L339,269 L333,269 Z" fill="#18202A" stroke="{INK}" stroke-width="1.2" stroke-linejoin="round"/>'
            f'<path d="M333,269 L339,269 L343,314 L336,324 L329,314 Z" fill="#1E2733" stroke="{INK}" stroke-width="1.2" stroke-linejoin="round"/>'
            '<path d="M335,272 L335,310" fill="none" stroke="#4B5B70" stroke-width="1.1" opacity="0.55"/>'
            # Sharp notched suit lapels OVER shirt collar edges
            f'<path d="M314,250 L297,282 L307,286 L301,294 L336,334 L336,318 L318,256 Z" '
            f'fill="#262D37" stroke="{INK}" stroke-width="1.8" stroke-linejoin="round"/>'
            f'<path d="M358,250 L375,282 L365,286 L371,294 L336,334 L336,318 L354,256 Z" '
            f'fill="#202630" stroke="{INK}" stroke-width="1.8" stroke-linejoin="round"/>'
            # Jacket front closure seam, buttons & crisp white pocket square
            '<line x1="336" y1="334" x2="336" y2="384" stroke="#0F1318" stroke-width="1.6"/>'
            '<circle cx="336" cy="348" r="2.6" fill="#11151B" stroke="#4A5564" stroke-width="0.9"/>'
            '<path d="M362,312 L380,310 L379,315 L362,316 Z" fill="#F0ECE4" stroke="#181C22" stroke-width="0.9"/>'
            '<line x1="360" y1="316" x2="383" y2="314" stroke="#11151B" stroke-width="1.5"/>'
            '</g>'
        )

        # Foreground grand marble & walnut bank counter (center-bottom focal stage)
        sahne.append(
            # Counter front walnut body
            f'<path d="M168,424 L792,424 L824,540 L136,540 Z" fill="url(#{p}_wood_dark)" stroke="{INK}" stroke-width="2.5"/>'
            # Carved front walnut recessed panels
            f'<rect x="218" y="446" width="236" height="74" rx="3" fill="#21130C" stroke="#533624" stroke-width="1.8"/>'
            f'<rect x="506" y="446" width="236" height="74" rx="3" fill="#21130C" stroke="#533624" stroke-width="1.8"/>'
            f'<rect x="228" y="454" width="216" height="58" fill="none" stroke="url(#{p}_brass)" stroke-width="1.1" opacity="0.6"/>'
            f'<rect x="516" y="454" width="216" height="58" fill="none" stroke="url(#{p}_brass)" stroke-width="1.1" opacity="0.6"/>'
            # Counter marble top surface (perspective trapezoid)
            f'<path d="M214,378 L746,378 L798,426 L162,426 Z" fill="url(#{p}_counter_top)" stroke="{INK}" stroke-width="2.4" stroke-linejoin="round"/>'
            # Marble veins on counter top
            '<path d="M240,404 Q320,394 404,412 M568,388 Q640,406 728,396" fill="none" stroke="#9D988E" stroke-width="1.3" opacity="0.45"/>'
            # Brass front trim lip
            f'<rect x="162" y="424" width="636" height="6" fill="url(#{p}_brass)" stroke="{INK}" stroke-width="1.2"/>'
        )

        # Brass teller divider screen on right side of counter
        sahne.append(
            f'<path d="M634,378 L634,274 L742,274 L742,378" fill="none" stroke="url(#{p}_brass)" stroke-width="4"/>'
            f'<rect x="636" y="276" width="104" height="102" fill="#9AC2D8" opacity="0.10"/>'
        )
        for bx in range(648, 738, 14):
            sahne.append(f'<line x1="{bx}" y1="276" x2="{bx}" y2="378" stroke="url(#{p}_brass_v)" stroke-width="2.2"/>')

        # Brass "NEXT TELLER" desk plaque on left of counter
        sahne.append(
            f'<path d="M244,410 L254,390 L338,390 L346,410 Z" fill="#1C1916" stroke="url(#{p}_brass)" stroke-width="1.8"/>'
            '<text x="295" y="404" text-anchor="middle" font-family="DejaVu Sans, Arial, sans-serif" font-weight="bold" font-size="8.5" letter-spacing="1.2" fill="#EBD08A">NEXT TELLER</text>'
        )

        # FOCAL OBJECT: Dark pistol silhouette resting calmly & politely on brass tray / marble counter
        # Zero muzzle flash, zero smoke, zero violence — pure quiet surrender
        sahne.append(
            '<g id="s205-pistol" transform="translate(494, 398)">'
            # Soft contact shadow on marble
            '<ellipse cx="6" cy="12" rx="56" ry="8" fill="#0B0E14" opacity="0.36"/>'
            # Small polite folded deposit slip / receipt under pistol
            '<path d="M-56,8 L54,4 L66,16 L-46,18 Z" fill="#F4EFE3" stroke="#8C8578" stroke-width="1.1"/>'
            '<line x1="-40" y1="11" x2="28" y2="9" stroke="#B6AFA2" stroke-width="0.9"/>'
            # Dark matte steel handgun silhouette (cleanly resting flat on slip)
            f'<path d="M-38,-6 L30,-6 L34,-1 L30,5 L14,5 L24,21 L7,23 L-5,7 L-19,7 L-17,13 L-7,13 L-5,15 L-21,15 L-25,7 L-38,6 Z" '
            f'fill="#1B212A" stroke="{INK}" stroke-width="1.8" stroke-linejoin="round"/>'
            # Subtle cool rim highlight along slide top
            '<path d="M-36,-4.2 L28,-4.2" fill="none" stroke="#889EB8" stroke-width="1.5" opacity="0.82" stroke-linecap="round"/>'
            '<line x1="12" y1="-5" x2="12" y2="3" stroke="#455264" stroke-width="1.2"/>'
            '<line x1="16" y1="-5" x2="16" y2="3" stroke="#455264" stroke-width="1.2"/>'
            '<line x1="20" y1="-5" x2="20" y2="3" stroke="#455264" stroke-width="1.2"/>'
            '</g>'
            # Michael's continuous right arm (shoulder -> elbow -> forearm -> white cuff -> calm hand)
            # Drawn over the counter edge so the arm connects seamlessly from shoulder to wrist
            '<g id="s205-arm-counter">'
            # Soft cast shadow of forearm & hand onto marble counter top
            '<path d="M396,380 L452,394 C464,398 468,406 456,408 L412,404 L388,388 Z" fill="#0B0E14" opacity="0.22"/>'
            # Continuous tailored sleeve from right shoulder (396,268) through elbow (410,336) to wrist (436,382)
            f'<path d="M398,266 C408,274 414,292 417,318 C419,332 422,340 434,358 L446,376 L428,392 L404,368 '
            f'C392,354 388,342 386,324 L382,276 Z" '
            f'fill="url(#{p}_suit)" stroke="{INK}" stroke-width="2.2" stroke-linejoin="round"/>'
            # Sleeve crease & outer rim highlight
            '<path d="M402,276 Q412,306 414,334 Q422,352 438,374" fill="none" stroke="#4D5868" stroke-width="1.4" opacity="0.52" stroke-linecap="round"/>'
            '<path d="M396,342 Q405,346 414,338" fill="none" stroke="#10141A" stroke-width="1.3" opacity="0.65" stroke-linecap="round"/>'
            # Crisp white French cuff emerging cleanly from sleeve end
            f'<path d="M442,374 L452,382 L440,396 L428,389 Z" fill="#F2EFE8" stroke="{INK}" stroke-width="1.4" stroke-linejoin="round"/>'
            '<circle cx="442" cy="389" r="1.4" fill="#B68B3A"/>'
            # Calm hand resting gently on marble as he releases the pistol
            f'<path d="M448,381 C462,381 474,387 473,394 C471,399 456,401 441,394 Z" fill="#D5A687" stroke="{INK}" stroke-width="1.7" stroke-linejoin="round"/>'
            '<path d="M457,388 L469,391 M454,392 L465,395" fill="none" stroke="#8A5E47" stroke-width="1.0" stroke-linecap="round"/>'
            '</g>'
        )

        # Fine plaster dust settled lightly on counter right
        for _ in range(18):
            px = rng.uniform(520, 625)
            py = rng.uniform(384, 418)
            sahne.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{rng.uniform(0.8, 1.9):.1f}" fill="#EAE6DC" opacity="0.65"/>')

        sahne.append("</g>")
        parts.append("".join(sahne))

    # ── LAYER 4: plan (Cyan #7FE6FF tactical blueprint overlay + dry-humor "POLITELY") ──
    if _katman_aktif(katmanlar, "plan"):
        plan: list[str] = [f'<g id="s205-plan">']
        # Subtle cyan architectural grid lines on lobby & counter
        plan.append(
            f'<g stroke="{PLAN}" fill="none" opacity="0.34">'
            '<path d="M328,102 L632,102 M328,320 L632,320" stroke-width="0.9" stroke-dasharray="6,4"/>'
            '<path d="M162,426 L214,378 L746,378 L798,426" stroke-width="0.9" stroke-dasharray="5,4"/>'
            '</g>'
        )
        # Calm tactical callout around pistol on counter (placed cleanly in open dark space)
        plan.append(
            f'<circle cx="494" cy="402" r="46" fill="none" stroke="{PLAN}" stroke-width="1.25" stroke-dasharray="5,4" opacity="0.78"/>'
            f'<path d="M528,372 L566,342 L722,342" fill="none" stroke="{PLAN}" stroke-width="1.2" opacity="0.88"/>'
            f'<circle cx="528" cy="372" r="2.8" fill="{PLAN}"/>'
            '<rect x="568" y="324" width="158" height="32" rx="3" fill="#09131F" fill-opacity="0.78"/>'
            f'<text x="574" y="338" font-family="DejaVu Sans Mono, Consolas, monospace" font-weight="bold" font-size="9.5" fill="{PLAN}">NON-VIOLENT SURRENDER</text>'
            f'<text x="574" y="351" font-family="DejaVu Sans Mono, Consolas, monospace" font-size="8.2" fill="{PLAN_CORE}" opacity="0.88">CPD RESPONSE: 01:48 · NO PLEA</text>'
        )
        # Dry-humor editorial badge: "POLITELY"
        plan.append(
            f'<g transform="translate(756, 456)">'
            f'<rect x="0" y="0" width="174" height="54" rx="4" fill="#091422" fill-opacity="0.90" stroke="{PLAN}" stroke-width="1.5"/>'
            f'<path d="M0,12 L0,0 L14,0 M160,54 L174,54 L174,42" fill="none" stroke="{PLAN_CORE}" stroke-width="2.2"/>'
            f'<text x="87" y="19" text-anchor="middle" font-family="DejaVu Sans Mono, Consolas, monospace" font-weight="bold" font-size="8.8" letter-spacing="1.6" fill="#C4E6F5">ARMED ROBBERY</text>'
            f'<text x="87" y="43" text-anchor="middle" font-family="Georgia, Times New Roman, serif" font-weight="bold" font-style="italic" font-size="22" letter-spacing="2.4" fill="#F8DC92">POLITELY</text>'
            '</g>'
        )
        plan.append("</g>")
        parts.append("".join(plan))

    # ── LAYER 5: onplan (Foreground vignette, floating plaster motes, siren rim glow) ──
    if _katman_aktif(katmanlar, "onplan"):
        onplan: list[str] = [f'<g id="s205-onplan">']
        # Subtle red/blue edge light leak from doors
        onplan.append(
            f'<rect x="0" y="0" width="960" height="540" fill="url(#{p}_vig)"/>'
            f'<path d="M0,0 L120,0 L70,540 L0,540 Z" fill="{SIREN_BLUE}" opacity="0.06"/>'
            f'<path d="M840,0 L960,0 L960,540 L890,540 Z" fill="{SIREN_RED}" opacity="0.06"/>'
        )
        # Floating foreground dust motes catching light
        for _ in range(22):
            mx = rng.uniform(180, 780)
            my = rng.uniform(60, 480)
            mr = rng.uniform(0.8, 2.1)
            onplan.append(f'<circle cx="{mx:.1f}" cy="{my:.1f}" r="{mr:.1f}" fill="#F6F2E8" opacity="{rng.uniform(0.16, 0.44):.2f}"/>')
        onplan.append("</g>")
        parts.append("".join(onplan))

    return defs, "".join(parts)


# =============================================================================
# SCENE 2.06: INMATE FILE #94941 ("FOX RIVER · 5 YEARS")
# =============================================================================
def set_206_dosya_94941(
    katmanlar: set[str] | list[str] | None = None,
) -> tuple[str, str]:
    """Top-down judge's mahogany desk with opened manila IDOC inmate transfer folder
    ('ILLINOIS DEPT. OF CORRECTIONS · INMATE #94941 · SCOFIELD, MICHAEL'), paperclipped
    locked Michael v3 mugshot (K.michael_kafa('front', 'odak', boyun=True)), bold fresh
    crimson ink stamp 'FOX RIVER · 5 YEARS', judge's fountain pen, and steel binder clip.
    """
    rng = random.Random(206)
    p = _uid("s206")

    defs = f"""
    <linearGradient id="{p}_desk" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#311E13"/>
      <stop offset="48%" stop-color="#22140C"/>
      <stop offset="100%" stop-color="#130B06"/>
    </linearGradient>
    <radialGradient id="{p}_lamp" cx="0.22" cy="0.18" r="0.62">
      <stop offset="0%" stop-color="#FFE19C" stop-opacity="0.42"/>
      <stop offset="45%" stop-color="#D69240" stop-opacity="0.14"/>
      <stop offset="100%" stop-color="#D69240" stop-opacity="0.0"/>
    </radialGradient>
    <linearGradient id="{p}_manila_l" x1="0" y1="0" x2="1" y2="0.2">
      <stop offset="0%" stop-color="#DFC48D"/>
      <stop offset="82%" stop-color="#E7CF9C"/>
      <stop offset="100%" stop-color="#B89B65"/>
    </linearGradient>
    <linearGradient id="{p}_manila_r" x1="0" y1="0" x2="1" y2="0.2">
      <stop offset="0%" stop-color="#C0A36D"/>
      <stop offset="12%" stop-color="#EAD4A2"/>
      <stop offset="92%" stop-color="#DEC38B"/>
      <stop offset="100%" stop-color="#C9AC74"/>
    </linearGradient>
    <linearGradient id="{p}_paper" x1="0" y1="0" x2="0.2" y2="1">
      <stop offset="0%" stop-color="#F7F2E4"/>
      <stop offset="100%" stop-color="#E5DCC6"/>
    </linearGradient>
    <linearGradient id="{p}_mug_bg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#C5CCD2"/>
      <stop offset="100%" stop-color="#9AA3AB"/>
    </linearGradient>
    <linearGradient id="{p}_gold" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F8E29D"/>
      <stop offset="50%" stop-color="#C5963E"/>
      <stop offset="100%" stop-color="#7B561B"/>
    </linearGradient>
    <linearGradient id="{p}_steel" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#E4ECF2"/>
      <stop offset="45%" stop-color="#9AA8B5"/>
      <stop offset="100%" stop-color="#4A5562"/>
    </linearGradient>
    <radialGradient id="{p}_vig" cx="0.5" cy="0.5" r="0.68">
      <stop offset="56%" stop-color="#000000" stop-opacity="0.0"/>
      <stop offset="100%" stop-color="#070504" stop-opacity="0.66"/>
    </radialGradient>
    <clipPath id="{p}_mug_clip">
      <rect x="-192" y="-138" width="132" height="162" rx="2"/>
    </clipPath>
    """

    parts: list[str] = []

    # ── LAYER 1: uzak (Judge's mahogany desk + leather blotter edge) ──
    if _katman_aktif(katmanlar, "uzak"):
        uzak: list[str] = [f'<g id="s206-uzak">']
        uzak.append(f'<rect x="0" y="0" width="960" height="540" fill="url(#{p}_desk)"/>')
        # Subtle mahogany wood grain lines
        for gy in range(14, 540, 22):
            off = rng.uniform(-12, 12)
            uzak.append(
                f'<path d="M0,{gy} Q480,{gy + off:.1f} 960,{gy - off * 0.5:.1f}" '
                f'fill="none" stroke="#160C07" stroke-width="{rng.uniform(1.0, 2.6):.1f}" opacity="0.34"/>'
            )
        # Green leather desk blotter mat with gold tooling border
        uzak.append(
            f'<rect x="44" y="28" width="872" height="484" rx="6" fill="#172A24" stroke="#0C1713" stroke-width="3"/>'
            f'<rect x="54" y="38" width="852" height="464" rx="3" fill="none" stroke="#B69148" stroke-width="1.2" opacity="0.52"/>'
            f'<rect x="58" y="42" width="844" height="456" rx="2" fill="none" stroke="#B69148" stroke-width="0.6" opacity="0.34"/>'
        )
        uzak.append("</g>")
        parts.append("".join(uzak))

    # ── LAYER 2: orta (Secondary court sentencing sheet, ink stamp pad, gavel corner) ──
    if _katman_aktif(katmanlar, "orta"):
        orta: list[str] = [f'<g id="s206-orta">']
        # Underlying Cook County court order paper peeking from top-left
        orta.append(
            '<g transform="translate(154, 108) rotate(-8)">'
            '<rect x="-92" y="-70" width="210" height="160" rx="2" fill="#0B0E0D" opacity="0.35" transform="translate(5,6)"/>'
            f'<rect x="-92" y="-70" width="210" height="160" rx="2" fill="#DDD5C0" stroke="#7A7263" stroke-width="1.2"/>'
            '<text x="-78" y="-48" font-family="Times New Roman, Georgia, serif" font-weight="bold" font-size="8.5" fill="#2A2722">CIRCUIT COURT OF COOK COUNTY</text>'
            '<line x1="-78" y1="-41" x2="100" y2="-41" stroke="#4D483F" stroke-width="1"/>'
            '<text x="-78" y="-28" font-family="DejaVu Sans Mono, Consolas, monospace" font-size="7" fill="#46423A">ORDER OF COMMITMENT · 05-CR-4418</text>'
            '</g>'
        )
        # Red ink stamp pad at top-right corner of desk
        orta.append(
            '<g transform="translate(838, 92) rotate(11)">'
            '<rect x="-52" y="-32" width="104" height="64" rx="6" fill="#0A0B0D" opacity="0.45" transform="translate(5,6)"/>'
            f'<rect x="-52" y="-32" width="104" height="64" rx="6" fill="#2B3038" stroke="{INK}" stroke-width="2"/>'
            '<rect x="-44" y="-24" width="88" height="48" rx="3" fill="#8E1A24" stroke="#5A0E15" stroke-width="1.5"/>'
            '<rect x="-40" y="-20" width="80" height="40" rx="2" fill="#B8212E" opacity="0.72"/>'
            '<text x="0" y="3" text-anchor="middle" font-family="DejaVu Sans, Arial, sans-serif" font-weight="bold" font-size="7.5" letter-spacing="1.2" fill="#F2B8BE" opacity="0.55">RED INK PAD</text>'
            '</g>'
        )
        # Judge's wooden gavel head peeking at bottom-left
        orta.append(
            '<g transform="translate(86, 446) rotate(-32)">'
            '<rect x="-12" y="14" width="24" height="110" rx="6" fill="#5A341D" stroke="#180D07" stroke-width="2"/>'
            '<rect x="-44" y="-22" width="88" height="40" rx="6" fill="#6E4124" stroke="#180D07" stroke-width="2.2"/>'
            f'<rect x="-26" y="-22" width="10" height="40" fill="url(#{p}_gold)"/>'
            f'<rect x="16" y="-22" width="10" height="40" fill="url(#{p}_gold)"/>'
            '</g>'
        )
        orta.append("</g>")
        parts.append("".join(orta))

    # ── LAYER 3: sahne (Opened Manila Folder #94941 + Michael v3 mugshot + FOX RIVER stamp + pen + clip) ──
    if _katman_aktif(katmanlar, "sahne"):
        sahne: list[str] = [f'<g id="s206-sahne">']
        # Centered opened manila folder tilted slightly for natural tabletop dynamism
        sahne.append('<g transform="translate(476, 276) rotate(-2.2)">')

        # Drop shadow under opened folder
        sahne.append(
            '<rect x="-356" y="-202" width="718" height="414" rx="5" fill="#060807" opacity="0.52" transform="translate(9, 11)"/>'
        )
        # Left manila folder flap + top index tab
        sahne.append(
            f'<path d="M-356,-202 L-148,-202 L-134,-226 L-28,-226 L-14,-202 L0,-202 L0,210 L-356,210 Z" '
            f'fill="url(#{p}_manila_l)" stroke="{INK_WARM}" stroke-width="2.2" stroke-linejoin="round"/>'
            '<text x="-82" y="-209" text-anchor="middle" font-family="DejaVu Sans Mono, Consolas, monospace" font-weight="bold" font-size="10.5" fill="#2A2218">94941 · SCOFIELD</text>'
        )
        # Right manila folder flap
        sahne.append(
            f'<rect x="0" y="-202" width="356" height="412" rx="3" fill="url(#{p}_manila_r)" stroke="{INK_WARM}" stroke-width="2.2"/>'
            # Center fold crease shadow
            '<line x1="0" y1="-200" x2="0" y2="208" stroke="#6E5734" stroke-width="2.5" opacity="0.65"/>'
            '<line x1="4" y1="-200" x2="4" y2="208" stroke="#FFF4D6" stroke-width="1.2" opacity="0.35"/>'
        )

        # ── LEFT PAGE: Mugshot + Fingerprint Card + Offender Bio ──
        sahne.append(
            f'<rect x="-334" y="-182" width="314" height="374" rx="2" fill="url(#{p}_paper)" stroke="#A79B82" stroke-width="1.2"/>'
            '<text x="-318" y="-158" font-family="DejaVu Sans, Arial, sans-serif" font-weight="bold" font-size="10.5" letter-spacing="1.2" fill="#232830">IDOC IDENTIFICATION RECORD</text>'
            '<line x1="-318" y1="-150" x2="-36" y2="-150" stroke="#2D333C" stroke-width="1.6"/>'
        )

        # Locked Michael v3 Mugshot clipped neatly inside photo frame
        m_mug = K.michael_kafa("front", "odak", look=0.0, boyun=True)
        sahne.append(
            '<g id="s206-mugshot">'
            # Photo drop shadow & white border
            '<rect x="-198" y="-144" width="144" height="174" fill="#1C1A16" opacity="0.22" transform="translate(3,4)"/>'
            '<rect x="-198" y="-144" width="144" height="174" fill="#FAF7F0" stroke="#6E675A" stroke-width="1.2"/>'
            f'<g clip-path="url(#{p}_mug_clip)">'
            f'<rect x="-192" y="-138" width="132" height="162" fill="url(#{p}_mug_bg)"/>'
        )
        # Height chart lines behind mugshot
        for hy, hlbl in [(-118, "6'2\""), (-92, "6'0\""), (-66, "5'10\""), (-40, "5'8\""), (-14, "5'6\"")]:
            sahne.append(
                f'<line x1="-192" y1="{hy}" x2="-60" y2="{hy}" stroke="#59636E" stroke-width="0.9" opacity="0.65"/>'
                f'<text x="-188" y="{hy - 3}" font-family="DejaVu Sans Mono, Consolas, monospace" font-size="7" fill="#3B434C">{hlbl}</text>'
            )
        # Fox River denim collar shoulders + Locked Michael v3 front head
        sahne.append(
            '<path d="M-182,30 C-178,-6 -156,-14 -126,-14 C-96,-14 -74,-6 -70,30 Z" fill="#5D7D9E" stroke="#1A1513" stroke-width="2"/>'
            '<path d="M-142,-12 L-126,12 L-110,-12 Z" fill="#EEEAE1" stroke="#1A1513" stroke-width="1.3"/>'
            f'<g transform="translate(-126, -73) scale(0.47)">{m_mug}</g>'
            # Mugshot chest placard
            '<rect x="-176" y="4" width="100" height="20" fill="#151920" stroke="#2D3642" stroke-width="1"/>'
            '<text x="-126" y="17.5" text-anchor="middle" font-family="DejaVu Sans Mono, Consolas, monospace" font-weight="bold" font-size="9.5" letter-spacing="1.2" fill="#F0ECE2">IDOC · 94941</text>'
            '</g>'
            # Metallic paperclip holding mugshot at top-right corner
            f'<path d="M-80,-152 L-80,-122 C-80,-116 -70,-116 -70,-122 L-70,-146 C-70,-150 -76,-150 -76,-146 L-76,-126" '
            f'fill="none" stroke="{INK}" stroke-width="3.6" stroke-linecap="round"/>'
            f'<path d="M-80,-152 L-80,-122 C-80,-116 -70,-116 -70,-122 L-70,-146 C-70,-150 -76,-150 -76,-146 L-76,-126" '
            f'fill="none" stroke="url(#{p}_steel)" stroke-width="2.1" stroke-linecap="round"/>'
            '</g>'
        )

        # Left column text next to mugshot
        left_meta = [
            ("DOB:", "10/08/1974"),
            ("SEX / HT:", "M · 6'0\""),
            ("EYES:", "BLUE-GREEN"),
            ("HAIR:", "BROWN / BUZZ"),
            ("OCCUP.:", "STRUCT. ENG."),
            ("PRIOR:", "NONE"),
        ]
        for idx, (k_lbl, v_lbl) in enumerate(left_meta):
            ly = -126 + idx * 24
            sahne.append(
                f'<text x="-318" y="{ly}" font-family="DejaVu Sans, Arial, sans-serif" font-weight="bold" font-size="8.2" fill="#5D584D">{k_lbl}</text>'
                f'<text x="-318" y="{ly + 11}" font-family="DejaVu Sans Mono, Consolas, monospace" font-weight="bold" font-size="9.2" fill="#1D2229">{v_lbl}</text>'
            )

        # Fingerprint strip at bottom of left page
        sahne.append(
            '<rect x="-318" y="48" width="282" height="126" fill="#EFE8D7" stroke="#A69B84" stroke-width="1"/>'
            '<text x="-308" y="64" font-family="DejaVu Sans, Arial, sans-serif" font-weight="bold" font-size="8.5" letter-spacing="1.0" fill="#3D3830">FINGERPRINT CLASSIFICATION · R-INDEX / L-THUMB</text>'
            '<line x1="-308" y1="70" x2="-46" y2="70" stroke="#A69B84" stroke-width="0.9"/>'
        )
        for fi, fx in enumerate([-274, -206, -138, -74]):
            sahne.append(f'<rect x="{fx - 26}" y="78" width="52" height="62" fill="#F8F4E8" stroke="#BFB59F" stroke-width="0.9"/>')
            for r_rad in (5, 9, 13, 17, 21):
                sahne.append(
                    f'<ellipse cx="{fx}" cy="109" rx="{r_rad * 0.72:.1f}" ry="{r_rad:.1f}" '
                    f'fill="none" stroke="#2B2E34" stroke-width="1.0" stroke-dasharray="{14 + fi * 3},3" opacity="0.58"/>'
                )
            sahne.append(f'<text x="{fx}" y="156" text-anchor="middle" font-family="DejaVu Sans Mono, Consolas, monospace" font-size="7.2" fill="#544E44">R-0{fi + 1}</text>')

        # ── RIGHT PAGE: Official IDOC Header, #94941 Transfer Record & Crimson Stamp ──
        sahne.append(
            f'<rect x="20" y="-182" width="316" height="374" rx="2" fill="url(#{p}_paper)" stroke="#A79B82" stroke-width="1.2"/>'
            # State seal badge top-left of right sheet
            '<circle cx="52" cy="-148" r="17" fill="none" stroke="#2D3745" stroke-width="1.8"/>'
            '<circle cx="52" cy="-148" r="13" fill="none" stroke="#2D3745" stroke-width="0.8" stroke-dasharray="2,2"/>'
            '<text x="52" y="-145" text-anchor="middle" font-family="Georgia, serif" font-weight="bold" font-size="8.5" fill="#2D3745">IL</text>'
            # Official header
            '<text x="78" y="-154" font-family="Georgia, Times New Roman, serif" font-weight="bold" font-size="11.5" letter-spacing="0.8" fill="#18202B">ILLINOIS DEPT. OF CORRECTIONS</text>'
            '<text x="78" y="-139" font-family="DejaVu Sans, Arial, sans-serif" font-weight="bold" font-size="8.2" letter-spacing="1.6" fill="#5A6370">INMATE TRANSFER &amp; CLASSIFICATION DOSSIER</text>'
            '<line x1="36" y1="-124" x2="320" y2="-124" stroke="#1E2630" stroke-width="2.2"/>'
            '<line x1="36" y1="-120" x2="320" y2="-120" stroke="#1E2630" stroke-width="0.8"/>'
            # Prominent Inmate Number & Name
            '<text x="38" y="-96" font-family="DejaVu Sans Mono, Consolas, monospace" font-weight="bold" font-size="19" letter-spacing="1.2" fill="#131921">INMATE #94941</text>'
            '<text x="38" y="-73" font-family="DejaVu Sans, Arial, sans-serif" font-weight="bold" font-size="14" letter-spacing="1.0" fill="#263140">SCOFIELD, MICHAEL</text>'
            '<line x1="36" y1="-62" x2="320" y2="-62" stroke="#B4AA95" stroke-width="1"/>'
        )

        # Case details lines
        case_rows = [
            ("CASE DOCKET:", "05-CR-4418 · COOK COUNTY"),
            ("OFFENSE:", "ARMED ROBBERY (NO INJURY)"),
            ("PLEA ENTERED:", "NO CONTEST · NO APPEAL"),
            ("FACILITY REQ.:", "FOX RIVER STATE PENITENTIARY"),
            ("SECURITY LEVEL:", "LEVEL 1 — MAXIMUM"),
            ("SENTENCE TERM:", "FIVE (5) YEARS — IMMEDIATE"),
        ]
        for idx, (rk, rv) in enumerate(case_rows):
            ry = -42 + idx * 24
            sahne.append(
                f'<text x="38" y="{ry}" font-family="DejaVu Sans, Arial, sans-serif" font-weight="bold" font-size="8.5" fill="#5D574C">{rk}</text>'
                f'<text x="134" y="{ry}" font-family="DejaVu Sans Mono, Consolas, monospace" font-weight="bold" font-size="9.2" fill="#1A2028">{rv}</text>'
                f'<line x1="38" y1="{ry + 6}" x2="318" y2="{ry + 6}" stroke="#D1C7B2" stroke-width="0.8"/>'
            )

        # Judge signature block at bottom right
        sahne.append(
            '<text x="38" y="138" font-family="DejaVu Sans, Arial, sans-serif" font-size="8" fill="#5D574C">PRESIDING JUDGE SIGNATURE</text>'
            '<path d="M44,162 C60,144 74,170 92,150 C106,136 116,164 134,152 C150,142 166,158 192,150" '
            'fill="none" stroke="#182438" stroke-width="2.1" stroke-linecap="round"/>'
            '<line x1="38" y1="170" x2="210" y2="170" stroke="#4D483E" stroke-width="1"/>'
            '<text x="38" y="182" font-family="DejaVu Sans Mono, Consolas, monospace" font-size="7.8" fill="#544E44">HON. R. CARTER · CIRCUIT COURT</text>'
            '<text x="232" y="166" font-family="DejaVu Sans Mono, Consolas, monospace" font-weight="bold" font-size="9" fill="#2A323D">DATE: APR 11</text>'
            '<line x1="226" y1="170" x2="316" y2="170" stroke="#4D483E" stroke-width="1"/>'
        )

        # BOLD FRESH CRIMSON STAMP SLAMMED ACROSS RIGHT PAGE: "FOX RIVER · 5 YEARS"
        sahne.append(
            '<g transform="translate(180, 74) rotate(-11)" opacity="0.93">'
            # Subtle ink bleed halo
            '<rect x="-132" y="-36" width="264" height="72" rx="5" fill="#C91D2B" opacity="0.10"/>'
            # Outer & inner double stamp border
            '<rect x="-128" y="-32" width="256" height="64" rx="4" fill="none" stroke="#C81D2B" stroke-width="4.4"/>'
            '<rect x="-121" y="-25" width="242" height="50" rx="2" fill="none" stroke="#C81D2B" stroke-width="1.5"/>'
            '<text x="0" y="-1" text-anchor="middle" font-family="Impact, Arial Black, DejaVu Sans, sans-serif" font-weight="900" font-size="25" letter-spacing="1.8" fill="#C81D2B">FOX RIVER · 5 YEARS</text>'
            '<text x="0" y="17" text-anchor="middle" font-family="DejaVu Sans Mono, Consolas, monospace" font-weight="bold" font-size="9.5" letter-spacing="2.2" fill="#B51926">TRANSFER APPROVED · MAX SECURITY</text>'
            # Slight ink distressed speckling so it feels authentically rubber-stamped
            '<line x1="-112" y1="-10" x2="-40" y2="-10" stroke="#F0E8D6" stroke-width="1.1" opacity="0.32"/>'
            '<line x1="22" y1="6" x2="108" y2="6" stroke="#F0E8D6" stroke-width="1.2" opacity="0.28"/>'
            '</g>'
        )

        # Large black/steel binder clip clamped at top edge of right sheet
        sahne.append(
            '<g transform="translate(262, -196) rotate(4)">'
            '<path d="M-12,-24 C-22,-42 -2,-52 0,-32 C2,-52 22,-42 12,-24" fill="none" stroke="#DCE4EC" stroke-width="2.4" stroke-linecap="round"/>'
            f'<rect x="-22" y="-24" width="44" height="22" rx="2" fill="#1E242C" stroke="{INK}" stroke-width="1.8"/>'
            '<line x1="-18" y1="-18" x2="18" y2="-18" stroke="#4D5A6B" stroke-width="1.4"/>'
            '</g>'
        )

        sahne.append("</g>")  # end folder group

        # Judge's black & gold fountain pen resting on right side of desk
        sahne.append(
            '<g transform="translate(838, 344) rotate(14)">'
            '<rect x="-8" y="-128" width="16" height="236" rx="7" fill="#060807" opacity="0.46" transform="translate(8,8)"/>'
            f'<path d="M-7,-126 C-7,-136 7,-136 7,-126 L8,68 L5,88 L-5,88 L-8,68 Z" fill="#14181F" stroke="{INK}" stroke-width="2"/>'
            # Gold cap band & clip
            f'<rect x="-8" y="-36" width="16" height="10" fill="url(#{p}_gold)" stroke="{INK}" stroke-width="1"/>'
            f'<rect x="-3" y="-116" width="6" height="72" rx="2" fill="url(#{p}_gold)" stroke="{INK}" stroke-width="1"/>'
            # Gold fountain nib
            f'<path d="M-5,88 L5,88 L0,116 Z" fill="url(#{p}_gold)" stroke="{INK}" stroke-width="1.4" stroke-linejoin="round"/>'
            '<line x1="0" y1="90" x2="0" y2="112" stroke="#2D1E0A" stroke-width="1.1"/>'
            # Gloss specular stripe
            '<line x1="-3.5" y1="-118" x2="-3.5" y2="66" stroke="#6E7C8E" stroke-width="1.6" opacity="0.55" stroke-linecap="round"/>'
            '</g>'
        )

        sahne.append("</g>")
        parts.append("".join(sahne))

    # ── LAYER 4: plan (Subtle #7FE6FF blueprint overlay on file & mugshot) ──
    if _katman_aktif(katmanlar, "plan"):
        plan: list[str] = [f'<g id="s206-plan">']
        plan.append(
            f'<g stroke="{PLAN}" fill="none" opacity="0.48">'
            # Corner brackets framing inmate #94941
            '<path d="M500,152 L500,140 L516,140 M732,140 L748,140 L748,152" stroke-width="1.4"/>'
            '<path d="M500,192 L500,204 L516,204 M732,204 L748,204 L748,192" stroke-width="1.4"/>'
            # Subtle targeting cross on mugshot
            '<path d="M286,144 L298,144 M404,144 L416,144" stroke-width="1.0" stroke-dasharray="3,2"/>'
            '</g>'
            # Bottom-left blueprint status badge
            '<g transform="translate(64, 466)">'
            f'<rect x="0" y="0" width="234" height="32" rx="3" fill="#091522" fill-opacity="0.82" stroke="{PLAN}" stroke-width="1.1"/>'
            f'<text x="12" y="13" font-family="DejaVu Sans Mono, Consolas, monospace" font-size="8.2" fill="{PLAN}">PHASE I · ENTRY PROTOCOL</text>'
            f'<text x="12" y="25" font-family="DejaVu Sans Mono, Consolas, monospace" font-weight="bold" font-size="9.5" fill="{PLAN_CORE}">TARGET LOCKED: FOX RIVER (#94941)</text>'
            '</g>'
        )
        plan.append("</g>")
        parts.append("".join(plan))

    # ── LAYER 5: onplan (Warm banker's lamp pool + dramatic tabletop vignette) ──
    if _katman_aktif(katmanlar, "onplan"):
        onplan: list[str] = [f'<g id="s206-onplan">']
        onplan.append(f'<rect x="0" y="0" width="960" height="540" fill="url(#{p}_lamp)"/>')
        onplan.append(f'<rect x="0" y="0" width="960" height="540" fill="url(#{p}_vig)"/>')
        # Subtle green glass banker's lamp shade edge in top-left
        onplan.append(
            '<path d="M-10,-10 L132,-10 L96,42 Q40,56 -10,40 Z" fill="#174534" stroke="#0B1E17" stroke-width="2.5"/>'
            '<path d="M-6,36 Q42,50 92,38" fill="none" stroke="#F4D382" stroke-width="2.2" opacity="0.65"/>'
        )
        onplan.append("</g>")
        parts.append("".join(onplan))

    return defs, "".join(parts)


    # =============================================================================
# SCENE 2.07: FOX RIVER GATES & COUNTDOWN ("EXECUTION IN 30 DAYS")
# =============================================================================
def set_207_fox_kapilar(
    katmanlar: set[str] | list[str] | None = None,
) -> tuple[str, str]:
    """Epic low-angle hero frame: towering stone Fox River walls, watchtowers,
    sweeping searchlights, and heavy closing steel gates under a stormy night sky;
    foreground-center locked Michael v3 (K.michael_figur('kararli', plan=True))
    in blue 94941 shirt with glowing tattooed forearms; #7FE6FF blueprint grid
    projected onto the fortress walls and top-right 'EXECUTION IN 30 DAYS' countdown.
    """
    rng = random.Random(207)
    p = _uid("s207")

    defs = f"""
    <linearGradient id="{p}_storm_sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#040811"/>
      <stop offset="42%" stop-color="#0B182C"/>
      <stop offset="78%" stop-color="#172A44"/>
      <stop offset="100%" stop-color="#22364F"/>
    </linearGradient>
    <radialGradient id="{p}_moon_haze" cx="0.50" cy="0.28" r="0.46">
      <stop offset="0%" stop-color="#8BC4E8" stop-opacity="0.34"/>
      <stop offset="48%" stop-color="#2E547A" stop-opacity="0.14"/>
      <stop offset="100%" stop-color="#091322" stop-opacity="0.0"/>
    </radialGradient>
    <linearGradient id="{p}_beam_l" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#E6F6FF" stop-opacity="0.54"/>
      <stop offset="55%" stop-color="#8FD4FF" stop-opacity="0.16"/>
      <stop offset="100%" stop-color="#8FD4FF" stop-opacity="0.0"/>
    </linearGradient>
    <linearGradient id="{p}_beam_r" x1="1" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#E6F6FF" stop-opacity="0.50"/>
      <stop offset="55%" stop-color="#8FD4FF" stop-opacity="0.15"/>
      <stop offset="100%" stop-color="#8FD4FF" stop-opacity="0.0"/>
    </linearGradient>
    <linearGradient id="{p}_stone_wall" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#26313F"/>
      <stop offset="48%" stop-color="#1D2632"/>
      <stop offset="100%" stop-color="#11171F"/>
    </linearGradient>
    <linearGradient id="{p}_stone_tower" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#19212C"/>
      <stop offset="42%" stop-color="#2C3847"/>
      <stop offset="100%" stop-color="#121821"/>
    </linearGradient>
    <linearGradient id="{p}_steel_gate" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#1A222B"/>
      <stop offset="50%" stop-color="#2A3542"/>
      <stop offset="100%" stop-color="#141B23"/>
    </linearGradient>
    <linearGradient id="{p}_yard_ground" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#131B26"/>
      <stop offset="45%" stop-color="#192330"/>
      <stop offset="100%" stop-color="#0A0F17"/>
    </linearGradient>
    <radialGradient id="{p}_hero_rim" cx="0.50" cy="0.62" r="0.32">
      <stop offset="0%" stop-color="#7FE6FF" stop-opacity="0.28"/>
      <stop offset="55%" stop-color="#4AA8D8" stop-opacity="0.10"/>
      <stop offset="100%" stop-color="#4AA8D8" stop-opacity="0.0"/>
    </radialGradient>
    <radialGradient id="{p}_vig" cx="0.5" cy="0.48" r="0.68">
      <stop offset="52%" stop-color="#000000" stop-opacity="0.0"/>
      <stop offset="100%" stop-color="#03060B" stop-opacity="0.72"/>
    </radialGradient>
    """

    parts: list[str] = []

    # ── LAYER 1: uzak (Stormy night sky, clouds, searchlight beams) ──
    if _katman_aktif(katmanlar, "uzak"):
        uzak: list[str] = [f'<g id="s207-uzak">']
        uzak.append(f'<rect x="0" y="0" width="960" height="540" fill="url(#{p}_storm_sky)"/>')
        uzak.append(f'<rect x="0" y="0" width="960" height="360" fill="url(#{p}_moon_haze)"/>')

        # Dramatic layered storm clouds
        clouds = [
            "M-20,120 Q80,68 188,92 Q290,48 412,86 Q530,52 640,94 Q770,58 980,104 L980,210 L-20,210 Z",
            "M-20,170 Q120,124 256,154 Q390,108 524,148 Q670,114 812,152 Q900,132 980,164 L980,260 L-20,260 Z",
        ]
        uzak.append(f'<path d="{clouds[0]}" fill="#0A1424" opacity="0.78"/>')
        uzak.append(f'<path d="{clouds[1]}" fill="#112136" opacity="0.68"/>')

        # Subtle distant lightning fork in upper-left clouds
        uzak.append(
            '<path d="M276,22 L262,56 L274,60 L254,104" fill="none" stroke="#CBEBFF" stroke-width="1.6" opacity="0.58" stroke-linecap="round" stroke-linejoin="round"/>'
            '<path d="M276,22 L262,56 L274,60 L254,104" fill="none" stroke="#7FE6FF" stroke-width="5" opacity="0.16"/>'
        )

        # Sweeping searchlight cones crossing the stormy sky (anchored to tower lamps at y=148)
        uzak.append(
            f'<polygon points="154,144 592,-10 740,56 164,154" fill="url(#{p}_beam_l)"/>'
            f'<polygon points="806,144 368,-10 220,56 796,154" fill="url(#{p}_beam_r)"/>'
            f'<polygon points="158,150 496,422 414,432 148,160" fill="url(#{p}_beam_l)" opacity="0.48"/>'
            f'<polygon points="802,150 464,422 546,432 812,160" fill="url(#{p}_beam_r)" opacity="0.44"/>'
        )
        uzak.append("</g>")
        parts.append("".join(uzak))

    # ── LAYER 2: orta (Low-angle towering Fox River stone fortress, watchtowers & closing steel gates) ──
    if _katman_aktif(katmanlar, "orta"):
        orta: list[str] = [f'<g id="s207-orta">']

        # Main towering limestone penitentiary walls (low-angle inward perspective)
        orta.append(
            f'<path d="M0,186 L342,158 L342,418 L0,432 Z" fill="url(#{p}_stone_wall)" stroke="{INK}" stroke-width="2.4"/>'
            f'<path d="M960,186 L618,158 L618,418 L960,432 Z" fill="url(#{p}_stone_wall)" stroke="{INK}" stroke-width="2.4"/>'
            # Central gothic stone gatehouse arch rising high
            f'<path d="M324,132 L636,132 L646,418 L314,418 Z" fill="url(#{p}_stone_wall)" stroke="{INK}" stroke-width="2.6"/>'
            # Battlement crenellations on gatehouse top
            f'<path d="M324,132 L324,112 L354,112 L354,124 L388,124 L388,112 L422,112 L422,124 L458,124 L458,112 '
            f'L502,112 L502,124 L538,124 L538,112 L572,112 L572,124 L606,124 L606,112 L636,112 L636,132 Z" '
            f'fill="#222C39" stroke="{INK}" stroke-width="2"/>'
        )

        # Stone masonry block courses on walls
        for wy in range(178, 412, 26):
            orta.append(f'<line x1="0" y1="{wy}" x2="314" y2="{wy - 10}" stroke="#0D131A" stroke-width="1.3" opacity="0.65"/>')
            orta.append(f'<line x1="646" y1="{wy - 10}" x2="960" y2="{wy}" stroke="#0D131A" stroke-width="1.3" opacity="0.65"/>')
            for bx in range(28, 300, 56):
                off = 24 if (wy // 26) % 2 else 0
                orta.append(f'<line x1="{bx + off}" y1="{wy - 10}" x2="{bx + off}" y2="{wy + 16}" stroke="#0D131A" stroke-width="1.1" opacity="0.55"/>')
            for bx in range(664, 940, 56):
                off = 24 if (wy // 26) % 2 else 0
                orta.append(f'<line x1="{bx + off}" y1="{wy - 10}" x2="{bx + off}" y2="{wy + 16}" stroke="#0D131A" stroke-width="1.1" opacity="0.55"/>')

        # Coiled razor wire along top of left & right walls
        for wx_start, wx_end in [(8, 310), (650, 952)]:
            for cx in range(wx_start, wx_end, 16):
                cy = 178 - (cx / 960) * 12 if cx < 480 else 166 + ((cx - 650) / 310) * 14
                orta.append(f'<circle cx="{cx}" cy="{cy:.1f}" r="9" fill="none" stroke="#6E8298" stroke-width="1.0" opacity="0.68"/>')

        # Left & Right Towering Stone Watchtowers (kept clear of top-right HUD)
        for tx, side in [(126, -1), (834, 1)]:
            orta.append(
                # Tapered tower shaft
                f'<path d="M{tx - 46},422 L{tx - 38},164 L{tx + 38},164 L{tx + 46},422 Z" fill="url(#{p}_stone_tower)" stroke="{INK}" stroke-width="2.5"/>'
                # Observation deck overhang
                f'<rect x="{tx - 48}" y="150" width="96" height="16" rx="2" fill="#2A3646" stroke="{INK}" stroke-width="2"/>'
                # Guard booth glass windows
                f'<rect x="{tx - 38}" y="116" width="76" height="34" fill="#182330" stroke="{INK}" stroke-width="2"/>'
                f'<rect x="{tx - 30}" y="124" width="60" height="18" fill="#F2C978" opacity="0.38"/>'
                f'<line x1="{tx - 10}" y1="124" x2="{tx - 10}" y2="142" stroke="{INK}" stroke-width="2.2"/>'
                f'<line x1="{tx + 10}" y1="124" x2="{tx + 10}" y2="142" stroke="{INK}" stroke-width="2.2"/>'
                # Peaked roof + antenna
                f'<polygon points="{tx - 50},116 {tx},88 {tx + 50},116" fill="#161E29" stroke="{INK}" stroke-width="2.2"/>'
                f'<line x1="{tx}" y1="88" x2="{tx}" y2="74" stroke="#7A8FA6" stroke-width="1.6"/>'
                f'<circle cx="{tx}" cy="74" r="2.4" fill="{RED_ALERT}"/>'
                # Searchlight lamp housing
                f'<circle cx="{tx + side * (-28)}" cy="148" r="7" fill="#E8F8FF" stroke="{INK}" stroke-width="1.5"/>'
            )

        # Carved Stone Plaque on Gatehouse: "FOX RIVER STATE PENITENTIARY"
        orta.append(
            f'<rect x="352" y="142" width="256" height="30" rx="2" fill="#151D27" stroke="#425469" stroke-width="1.8"/>'
            '<text x="480" y="161" text-anchor="middle" font-family="Georgia, Times New Roman, serif" font-weight="bold" '
            'font-size="12" letter-spacing="1.6" fill="#C7D6E6">FOX RIVER PENITENTIARY</text>'
        )

        # Archway opening + Glowing inner prison yard mist
        orta.append(
            f'<path d="M366,418 L366,246 Q480,174 594,246 L594,418 Z" fill="#0B1624" stroke="{INK}" stroke-width="3"/>'
            f'<ellipse cx="480" cy="346" rx="112" ry="96" fill="url(#{p}_hero_rim)"/>'
        )

        # HEAVY CLOSING STEEL GATES (slightly ajar in center, heavy iron bars & riveted plates)
        # Left gate leaf
        orta.append(
            f'<path d="M366,418 L366,246 Q418,214 462,210 L462,418 Z" fill="url(#{p}_steel_gate)" stroke="{INK}" stroke-width="2.4"/>'
            f'<rect x="366" y="346" width="96" height="72" fill="#17202A" stroke="{INK}" stroke-width="2"/>'
        )
        for gx in range(380, 456, 15):
            orta.append(f'<line x1="{gx}" y1="226" x2="{gx}" y2="346" stroke="#0C1117" stroke-width="3.4"/>')
            orta.append(f'<line x1="{gx + 1.5}" y1="226" x2="{gx + 1.5}" y2="346" stroke="#4E6278" stroke-width="1.0" opacity="0.55"/>')
        # Right gate leaf
        orta.append(
            f'<path d="M594,418 L594,246 Q542,214 498,210 L498,418 Z" fill="url(#{p}_steel_gate)" stroke="{INK}" stroke-width="2.4"/>'
            f'<rect x="498" y="346" width="96" height="72" fill="#17202A" stroke="{INK}" stroke-width="2"/>'
        )
        for gx in range(508, 586, 15):
            orta.append(f'<line x1="{gx}" y1="226" x2="{gx}" y2="346" stroke="#0C1117" stroke-width="3.4"/>')
            orta.append(f'<line x1="{gx + 1.5}" y1="226" x2="{gx + 1.5}" y2="346" stroke="#4E6278" stroke-width="1.0" opacity="0.55"/>')
        # Heavy horizontal lock beams & rivets
        orta.append(
            f'<rect x="366" y="284" width="96" height="12" fill="#232E3B" stroke="{INK}" stroke-width="1.8"/>'
            f'<rect x="498" y="284" width="96" height="12" fill="#232E3B" stroke="{INK}" stroke-width="1.8"/>'
        )

        orta.append("</g>")
        parts.append("".join(orta))

    # ── LAYER 3: sahne (Wet stone courtyard + foreground-center locked Michael v3 hero) ──
    if _katman_aktif(katmanlar, "sahne"):
        sahne: list[str] = [f'<g id="s207-sahne">']
        # Wet stone/asphalt prison approach ground
        sahne.append(f'<rect x="0" y="416" width="960" height="124" fill="url(#{p}_yard_ground)"/>')
        # Perspective stone paving & wet light reflections
        for gy in [432, 454, 482, 516]:
            sahne.append(f'<line x1="0" y1="{gy}" x2="960" y2="{gy}" stroke="#273648" stroke-width="1.2" opacity="0.45"/>')
        for gx in range(-80, 1080, 120):
            dx_top = 480 + (gx - 480) * 0.42
            sahne.append(f'<line x1="{dx_top:.1f}" y1="416" x2="{gx}" y2="540" stroke="#273648" stroke-width="1.1" opacity="0.40"/>')
        # Cool searchlight puddle reflections on ground
        sahne.append(
            '<ellipse cx="480" cy="482" rx="190" ry="24" fill="#7FE6FF" opacity="0.10"/>'
            '<ellipse cx="260" cy="466" rx="95" ry="12" fill="#8FD4FF" opacity="0.08"/>'
            '<ellipse cx="700" cy="466" rx="95" ry="12" fill="#8FD4FF" opacity="0.08"/>'
        )

        # Locked Michael v3 full figure (K.michael_figur("kararli", plan=True))
        # Commanding low-angle hero foreground presence with cyan rim backlit mist
        m_fig = K.michael_figur("kararli", plan=True, numara_goster=True)
        sahne.append(
            '<g id="s207-michael-hero">'
            # Dramatic backlit cyan-silver rim halo behind Michael
            f'<ellipse cx="480" cy="376" rx="102" ry="158" fill="url(#{p}_hero_rim)" opacity="1.0"/>'
            f'<g transform="translate(480, 534) scale(0.61)">{m_fig}</g>'
            '</g>'
        )
        sahne.append("</g>")
        parts.append("".join(sahne))

    # ── LAYER 4: plan (Glowing #7FE6FF blueprint grid on prison walls + "EXECUTION IN 28 DAYS") ──
    if _katman_aktif(katmanlar, "plan"):
        plan: list[str] = [f'<g id="s207-plan">']
        # Architectural CAD wireframe projected onto Fox River walls & watchtowers
        plan.append(
            f'<g stroke="{PLAN}" fill="none">'
            # Left wall CAD elevation & underground pipe trace
            '<path d="M18,200 L314,174 L314,412 L18,424 Z" stroke-width="1.1" stroke-dasharray="6,4" opacity="0.58"/>'
            '<path d="M46,248 L294,230 M46,304 L294,292 M46,362 L294,354" stroke-width="0.85" opacity="0.44"/>'
            '<path d="M126,136 L126,422 M88,136 L164,136" stroke-width="1.0" stroke-dasharray="4,3" opacity="0.52"/>'
            # Right wall CAD elevation
            '<path d="M646,174 L942,200 L942,424 L646,412 Z" stroke-width="1.1" stroke-dasharray="6,4" opacity="0.58"/>'
            '<path d="M666,230 L914,248 M666,292 L914,304 M666,354 L914,362" stroke-width="0.85" opacity="0.44"/>'
            '<path d="M834,136 L834,422 M796,136 L872,136" stroke-width="1.0" stroke-dasharray="4,3" opacity="0.52"/>'
            # Central gate arch CAD structural arc & hidden subterranean route
            '<path d="M366,246 Q480,174 594,246" stroke-width="1.6" opacity="0.78"/>'
            '<path d="M314,418 L384,458 L576,458 L646,418" stroke-width="1.3" stroke-dasharray="5,3" opacity="0.68"/>'
            '</g>'
        )
        # Technical blueprint callout labels on walls
        plan.append(
            f'<g font-family="DejaVu Sans Mono, Consolas, monospace" fill="{PLAN}" opacity="0.82">'
            '<text x="34" y="222" font-size="8.5">WALL ELEV: +34.5 FT</text>'
            '<text x="34" y="236" font-size="7.8" opacity="0.72">TOWER 01 · BLIND ARC 14°</text>'
            '<text x="720" y="222" font-size="8.5">INFIRMARY WALL · NORTH</text>'
            '<text x="720" y="236" font-size="7.8" opacity="0.72">SUB-TUNNEL: PIPE SHAFT A</text>'
            '</g>'
        )

        # TOP-RIGHT DRAMATIC COUNTDOWN HUD: "EXECUTION IN 30 DAYS" (cleanly in stormy sky above tower)
        plan.append(
            '<g transform="translate(664, 14)">'
            # Dark tactical glass panel with crimson alert accent
            f'<rect x="0" y="0" width="276" height="56" rx="4" fill="#0A0F1A" fill-opacity="0.92" stroke="{RED_ALERT}" stroke-width="1.8"/>'
            f'<rect x="0" y="0" width="8" height="56" rx="2" fill="{RED_ALERT}"/>'
            # Corner cyan CAD ticks
            f'<path d="M262,0 L276,0 L276,14 M262,56 L276,56 L276,42" fill="none" stroke="{PLAN}" stroke-width="1.8"/>'
            f'<circle cx="24" cy="16" r="3.8" fill="{RED_ALERT}"/>'
            '<text x="36" y="19" font-family="DejaVu Sans Mono, Consolas, monospace" font-weight="bold" font-size="8.6" letter-spacing="1.6" fill="#FF8C97">LINCOLN BURROWS · #79238</text>'
            '<text x="20" y="45" font-family="Impact, Arial Black, DejaVu Sans, sans-serif" font-weight="900" font-size="22" letter-spacing="1.4" fill="#FFFFFF">EXECUTION IN <tspan fill="#FF4356">30 DAYS</tspan></text>'
            '</g>'
        )
        plan.append("</g>")
        parts.append("".join(plan))

    # ── LAYER 5: onplan (Slanted storm rain streaks, foreground mist & dark vignette) ──
    if _katman_aktif(katmanlar, "onplan"):
        onplan: list[str] = [f'<g id="s207-onplan">']
        # Diagonal fine rain streaks across stormy night
        rain: list[str] = []
        for _ in range(72):
            rx = rng.uniform(0, 960)
            ry = rng.uniform(0, 520)
            rl = rng.uniform(14, 34)
            rain.append(
                f'<line x1="{rx:.1f}" y1="{ry:.1f}" x2="{rx - rl * 0.24:.1f}" y2="{ry + rl:.1f}" '
                f'stroke="#B9E2FF" stroke-width="{rng.uniform(0.6, 1.2):.1f}" opacity="{rng.uniform(0.14, 0.34):.2f}"/>'
            )
        onplan.append("".join(rain))
        onplan.append(f'<rect x="0" y="0" width="960" height="540" fill="url(#{p}_vig)"/>')
        onplan.append("</g>")
        parts.append("".join(onplan))

    return defs, "".join(parts)


# =============================================================================
# RENDERING & PRESENTATION CARD BUILDERS (1280x720 SET + R13 200% CROPS)
# =============================================================================
def _sahne_svg(fn, w: int = 1920, h: int = 1080) -> str:
    defs, body = fn(None)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {W_SCENE} {H_SCENE}">'
        f"<defs>{defs}</defs>{body}</svg>"
    )


def _render_scene_pil(fn, w: int = 1920, h: int = 1080) -> Image.Image:
    svg_str = _sahne_svg(fn, w=w, h=h)
    png_bytes = resvg_py.svg_to_bytes(svg_string=svg_str)
    return Image.open(io.BytesIO(png_bytes)).convert("RGBA")


def _load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/calibrib.ttf" if bold else "C:/Windows/Fonts/calibri.ttf",
    ]
    for fp in candidates:
        if Path(fp).exists():
            return ImageFont.truetype(fp, size)
    return ImageFont.load_default()


def _draw_card_bg(w: int, h: int) -> Image.Image:
    svg = f"""
    <svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
      <defs>
        <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0%" stop-color="#0A121E"/>
          <stop offset="50%" stop-color="#101A29"/>
          <stop offset="100%" stop-color="#070D16"/>
        </linearGradient>
      </defs>
      <rect width="{w}" height="{h}" fill="url(#bg)"/>
      <g stroke="#1E3046" stroke-width="0.6" opacity="0.32">
        {"".join(f'<line x1="{x}" y1="0" x2="{x}" y2="{h}"/>' for x in range(0, w, 64))}
        {"".join(f'<line x1="0" y1="{y}" x2="{w}" y2="{y}"/>' for y in range(0, h, 64))}
      </g>
    </svg>
    """
    return Image.open(io.BytesIO(resvg_py.svg_to_bytes(svg_string=svg))).convert("RGBA")


def _draw_panel_box(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    radius: int = 10,
    fill=(17, 26, 39, 235),
    outline=(42, 62, 86, 255),
) -> None:
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=1)


def _draw_swatches(
    draw: ImageDraw.ImageDraw, x: int, y: int, colors: list[str], size: int = 16, gap: int = 6
) -> None:
    for i, hex_c in enumerate(colors):
        cx = x + i * (size + gap)
        draw.rounded_rectangle((cx, y, cx + size, y + size), radius=3, fill=hex_c, outline="#384D66", width=1)


def uret_kartlar(versiyon: str = "v1") -> tuple[Path, Path]:
    print("Rendering 3 Act II scenes (2.05, 2.06, 2.07) at 1920x1080...")
    img_205 = _render_scene_pil(set_205_banka, 1920, 1080)
    img_206 = _render_scene_pil(set_206_dosya_94941, 1920, 1080)
    img_207 = _render_scene_pil(set_207_fox_kapilar, 1920, 1080)

    # =========================================================================
    # OUTPUT 1: SET PRESENTATION CARD (1280 x 720 — 100% ENGLISH)
    # =========================================================================
    canvas = _draw_card_bg(1280, 720)
    draw = ImageDraw.Draw(canvas)

    f_title = _load_font(20, bold=True)
    f_sub = _load_font(12, bold=False)
    f_card_t = _load_font(13, bold=True)
    f_card_s = _load_font(11, bold=False)
    f_small = _load_font(10, bold=False)

    draw.text((24, 14), "MICHAEL SCOFIELD  ·  ACT II BANK, #94941 FILE & FOX RIVER GATES", fill="#EBF3FA", font=f_title)
    draw.text(
        (24, 39),
        "STYLE B+A HYBRID (CINEMATIC 2D + CYAN BLUEPRINT VISION)  ·  SCENES 2.05 – 2.07",
        fill="#7E97B0",
        font=f_sub,
    )
    top_swatches = [
        ("#E5C068", "BRASS"),
        ("#2E8CFF", "SIREN"),
        ("#E5CE9A", "MANILA"),
        ("#C81D2B", "STAMP"),
        ("#7FE6FF", "CAD PLAN"),
    ]
    sx_top = 816
    for col, lbl in top_swatches:
        draw.rounded_rectangle((sx_top, 18, sx_top + 14, 32), radius=3, fill=col, outline="#3B536D", width=1)
        draw.text((sx_top + 19, 19), lbl, fill="#9BB2C8", font=f_small)
        sx_top += 88
    draw.line((24, 58, 1256, 58), fill="#213247", width=1)

    # --- TOP-LEFT PANEL: 2.05 POLITE BANK ROBBERY ---
    _draw_panel_box(draw, (22, 68, 630, 366))
    t205 = img_205.resize((448, 252), Image.Resampling.LANCZOS)
    canvas.paste(t205, (34, 98), t205)
    draw.rectangle((34, 98, 34 + 448, 98 + 252), outline="#2E455E", width=1)
    draw.text((34, 76), "01 · 2.05 BANK LOBBY", fill="#F4D484", font=f_card_t)
    draw.text((208, 78), "Title Card: \"POLITELY\" · Zero Violence", fill="#8AA3BC", font=f_card_s)
    ix = 492
    draw.text((ix, 98), "PALETTE", fill="#7FE6FF", font=f_small)
    _draw_swatches(draw, ix, 114, ["#262B33", "#E5C068", "#8A1926", "#2E8CFF", "#7FE6FF"], size=18, gap=5)
    draw.text((ix, 146), "KEY ELEMENTS", fill="#9BB2C8", font=f_small)
    for k_i, item in enumerate(
        [
            "• Marble Columns & Brass",
            "• Police Siren Glass Glow",
            "• Ceiling Plaster Dust",
            "• Calm Pistol Surrender",
            "• Dry-Humor \"POLITELY\"",
        ]
    ):
        draw.text((ix, 164 + k_i * 19), item, fill="#D5E2EE", font=f_card_s)
    draw.text((ix, 272), "KEY LIGHTING", fill="#9BB2C8", font=f_small)
    draw.text((ix, 288), "Warm brass + siren glow", fill="#F6C367", font=f_card_s)
    draw.text((ix, 314), "LAYERS (5)", fill="#9BB2C8", font=f_small)
    draw.text((ix, 330), "uzak · orta · sahne\nplan · onplan", fill="#8AA3BC", font=f_small)

    # --- TOP-RIGHT PANEL: 2.06 INMATE FILE #94941 ---
    _draw_panel_box(draw, (648, 68, 1256, 366))
    t206 = img_206.resize((448, 252), Image.Resampling.LANCZOS)
    canvas.paste(t206, (660, 98), t206)
    draw.rectangle((660, 98, 660 + 448, 98 + 252), outline="#2E455E", width=1)
    draw.text((660, 76), "02 · 2.06 INMATE FILE #94941", fill="#FF6B78", font=f_card_t)
    draw.text((876, 78), "Stamp: \"FOX RIVER · 5 YEARS\"", fill="#8AA3BC", font=f_card_s)
    ix2 = 1118
    draw.text((ix2, 98), "PALETTE", fill="#7FE6FF", font=f_small)
    _draw_swatches(draw, ix2, 114, ["#26160E", "#172A24", "#E5CE9A", "#C81D2B", "#7FE6FF"], size=18, gap=5)
    draw.text((ix2, 146), "KEY ELEMENTS", fill="#9BB2C8", font=f_small)
    for k_i, item in enumerate(
        [
            "• Opened IDOC Folder",
            "• Locked Michael v3 Mug",
            "• Red FOX RIVER Stamp",
            "• Judge Pen & Steel Clip",
            "• Fingerprint Strip",
        ]
    ):
        draw.text((ix2, 164 + k_i * 19), item, fill="#D5E2EE", font=f_card_s)
    draw.text((ix2, 272), "KEY LIGHTING", fill="#9BB2C8", font=f_small)
    draw.text((ix2, 288), "Warm banker lamp pool", fill="#F6C367", font=f_card_s)
    draw.text((ix2, 314), "LAYERS (5)", fill="#9BB2C8", font=f_small)
    draw.text((ix2, 330), "uzak · orta · sahne\nplan · onplan", fill="#8AA3BC", font=f_small)

    # --- BOTTOM WIDE PANEL: 2.07 FOX RIVER GATES & COUNTDOWN ---
    _draw_panel_box(draw, (22, 378, 1256, 704))
    t207 = img_207.resize((512, 288), Image.Resampling.LANCZOS)
    canvas.paste(t207, (34, 404), t207)
    draw.rectangle((34, 404, 34 + 512, 404 + 288), outline="#35516E", width=1)
    draw.text((34, 384), "03 · 2.07 FOX RIVER GATES & COUNTDOWN", fill="#7FE6FF", font=f_card_t)
    draw.text((322, 386), "Hero Low-Angle · \"EXECUTION IN 30 DAYS\"", fill="#B88E92", font=f_card_s)

    rx = 564
    draw.text((rx, 404), "PALETTE (STORM STEEL, CYAN PLAN & CRIMSON CLOCK)", fill="#7FE6FF", font=f_small)
    _draw_swatches(draw, rx, 422, ["#07101E", "#222E3D", "#6182A3", "#E63244", "#7FE6FF", "#DDFBFF"], size=22, gap=7)
    draw.text((rx, 458), "KEY ELEMENTS", fill="#9BB2C8", font=f_small)
    for k_i, item in enumerate(
        [
            "• Low-angle towering Fox River stone walls & watchtowers",
            "• Sweeping searchlights & closing heavy iron steel gates",
            "• Locked Michael v3 hero (K.michael_figur, plan=True)",
            "• #7FE6FF CAD wall overlay + EXECUTION IN 30 DAYS HUD",
        ]
    ):
        draw.text((rx, 476 + k_i * 21), item, fill="#E3ECF5", font=f_card_s)
    draw.text((rx, 572), "DRAMATIC CLIMAX", fill="#9BB2C8", font=f_small)
    draw.text(
        (rx, 590),
        "Michael completes Phase I: from politely surrendering\n"
        "in Chicago, through Judge Carter's 5-year stamp, straight\n"
        "into Fox River's storm-lit gates with 30 days left.",
        fill="#C9D8E6",
        font=f_card_s,
    )
    draw.text((rx, 650), "LAYERS (5)", fill="#9BB2C8", font=f_small)
    draw.text((rx, 666), "s207-uzak · s207-orta · s207-sahne · s207-plan · s207-onplan", fill="#8AA3BC", font=f_small)

    draw.line((880, 404, 880, 692), fill="#233447", width=1)
    tx = 898
    draw.text((tx, 404), "ACT II VISUAL ARC & ENGINE SPEC", fill="#7FE6FF", font=f_card_t)
    notes = [
        (
            "2.05 -> 2.06 -> 2.07 PROGRESSION",
            "Transitions from the marble Chicago bank heist\n"
            "(calm non-violent surrender) to the stamped #94941\n"
            "transfer dossier, ending at Fox River's gates.",
        ),
        (
            "LOCKED MICHAEL v3 INTEGRATION",
            "Embeds K.michael_kafa('front','odak',boyun=True)\n"
            "inside the IDOC mugshot (2.06) and K.michael_figur\n"
            "('kararli', plan=True) with glowing tattoos (2.07).",
        ),
        (
            "PARALLAX & CLEAN SVG SPEC",
            "Side-effect-free module returning pure (defs, body)\n"
            "at 960x540 with 5 named <g> depth layers and\n"
            "fill='none' on every stroked <path>.",
        ),
    ]
    ny = 432
    for heading, body_txt in notes:
        draw.text((tx, ny), heading, fill="#F6C367" if "PROGRESSION" in heading else "#9EC5DE", font=f_small)
        draw.text((tx, ny + 16), body_txt, fill="#C5D5E4", font=f_card_s)
        ny += 86

    out_main = OUT_DIR / f"b2_set_banka_kapi_{versiyon}.png"
    canvas.convert("RGB").save(out_main, quality=95)

    # =========================================================================
    # OUTPUT 2: R13 200% ZOOM QUALITY CONTROL CARD (1280 x 720 — 4 PANELS)
    # =========================================================================
    r13 = _draw_card_bg(1280, 720)
    d13 = ImageDraw.Draw(r13)
    d13.text((24, 13), "R13 · 200% ZOOM QUALITY CONTROL (ACT II BANK, FILE & GATES)", fill="#EBF3FA", font=f_title)
    d13.text(
        (24, 37),
        "1:1 PIXEL CROPS FROM 1920×1080 SOURCE  ·  TYPOGRAPHY, LOCKED MICHAEL v3, LIGHTING & DETAILS",
        fill="#7E97B0",
        font=f_sub,
    )
    d13.line((24, 55, 1256, 55), fill="#213247", width=1)

    cw, ch = 600, 264
    crops = [
        (
            img_205,
            (800, 625),
            "1 · 2.05 MICHAEL SUIT ANATOMY, COLLAR & PISTOL (200%)",
            "Collar-over-neck Z-order, ~2.2x athletic shoulders, seamless arm & calm pistol",
            (22, 66),
        ),
        (
            img_206,
            (720, 440),
            "2 · 2.06 LOCKED MICHAEL v3 MUGSHOT & PAPERCLIP (200%)",
            "K.michael_kafa('front','odak',boyun=True) against height chart + IDOC 94941",
            (652, 66),
        ),
        (
            img_206,
            (1420, 610),
            "3 · 2.06 FOX RIVER · 5 YEARS STAMP & JUDGE PEN (200%)",
            "Crimson rubber-stamp typography, IDOC dossier #94941 & gold-nib fountain pen",
            (22, 392),
        ),
        (
            img_207,
            (960, 635),
            "4 · 2.07 MICHAEL v3 HERO & FOX RIVER GATES (200%)",
            "K.michael_figur('kararli',plan=True) with glowing tattoo forearms & steel gates",
            (652, 392),
        ),
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

    out_r13 = OUT_DIR / "b2_set_banka_kapi_r13.png"
    r13.convert("RGB").save(out_r13, quality=95)
    print(f"Saved:\n  - {out_main}\n  - {out_r13}")
    return out_main, out_r13


if __name__ == "__main__":
    uret_kartlar("v1")
