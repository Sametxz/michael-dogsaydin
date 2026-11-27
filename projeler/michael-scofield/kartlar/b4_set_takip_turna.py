"""V10 (Act IV: FBI Desk & Tattoo Wall, Night Highway Fake Aliases & Coded Origami Crane).

Style B+A Hybrid (Cinematic 2D + Cyan Blueprint Vision) — R18-HAREKET multi-layer scenes (960x540):
  - set_401_fbi_masasi(katmanlar=None)     -> (defs_str, body_str)
  - set_402_otoyol_kimlik(katmanlar=None)  -> (defs_str, body_str)
  - set_403_sifreli_turna(katmanlar=None)  -> (defs_str, body_str)

All on-screen text is 100% ENGLISH. Every stroked <path> explicitly specifies fill="none".
R4-PARALLAX STRICT: Every character/hand + held/contacted object lives in a single layer.
Uses locked assets from karakter.py (K.michael_sirt_dovme, K.turna, K.michael_kafa) read-only.
Side-effect-free on import.
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
PLAN_CORE = "#E2FCFF"
AMBER_GOLD = "#F5C26B"
AMBER_HOT = "#FFE6A8"
RED_ALERT = "#E63244"
RED_BRIGHT = "#FF5C6C"
SIREN_BLUE = "#2E8CFF"
SIREN_RED = "#FF2E48"

_UID = 0


def _uid(prefix: str = "b4") -> str:
    global _UID
    _UID += 1
    return f"{prefix}_{_UID}"


def _katman_aktif(katmanlar: set[str] | list[str] | None, ad: str) -> bool:
    return katmanlar is None or ad in katmanlar


# =============================================================================
# SCENE 4.01: MAHONE'S FBI DESK & TATTOO WALL ("ANOTHER MIND")
# =============================================================================
def set_401_fbi_masasi(
    katmanlar: set[str] | list[str] | None = None,
) -> tuple[str, str]:
    """A2 continuity from 3.10 FBI inset: dark nocturnal FBI office with warm emerald/brass
    banker's desk lamp, corkboard evidence wall with locked A-Sirt v1 (plan_glow=0.55)
    polaroid photo, US highway map (UTAH, NEW MEXICO, PANAMA), FBI CASE #94941 · MAHONE
    dossier, animatable red strings (`kirmizi_ip`), stylized FBI hand pinning UTAH
    (`harita_igne` — single R4 layer), and cyan-to-red DECODING MAP · UTAH CAD (`plan`).
    """
    rng = random.Random(401)
    p = _uid("s401")

    sirt_defs, sirt_body = K.michael_sirt_dovme(plan_glow=0.55)

    defs = f"""
    {sirt_defs}
    <linearGradient id="{p}_wall_bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0B0F15"/>
      <stop offset="50%" stop-color="#141312"/>
      <stop offset="100%" stop-color="#090C11"/>
    </linearGradient>
    <linearGradient id="{p}_cork_bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#4A3524"/>
      <stop offset="50%" stop-color="#3B291B"/>
      <stop offset="100%" stop-color="#2A1D13"/>
    </linearGradient>
    <linearGradient id="{p}_desk_top" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#281C14"/>
      <stop offset="42%" stop-color="#1E140E"/>
      <stop offset="100%" stop-color="#120C08"/>
    </linearGradient>
    <radialGradient id="{p}_lamp_pool" cx="0.22" cy="0.44" r="0.62">
      <stop offset="0%" stop-color="#FFE6A8" stop-opacity="0.42"/>
      <stop offset="35%" stop-color="#E8A244" stop-opacity="0.22"/>
      <stop offset="72%" stop-color="#8A511B" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.0"/>
    </radialGradient>
    <radialGradient id="{p}_lamp_desk_glow" cx="0.18" cy="0.72" r="0.34">
      <stop offset="0%" stop-color="#FFEBB8" stop-opacity="0.52"/>
      <stop offset="48%" stop-color="#D98F34" stop-opacity="0.18"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.0"/>
    </radialGradient>
    <linearGradient id="{p}_shade_green" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#1D4B3A"/>
      <stop offset="55%" stop-color="#296B52"/>
      <stop offset="100%" stop-color="#143629"/>
    </linearGradient>
    <linearGradient id="{p}_brass" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#8C6324"/>
      <stop offset="45%" stop-color="#F2CA74"/>
      <stop offset="100%" stop-color="#7A5218"/>
    </linearGradient>
    <linearGradient id="{p}_map_paper" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#EFE6D2"/>
      <stop offset="60%" stop-color="#E2D5BA"/>
      <stop offset="100%" stop-color="#CEBE9D"/>
    </linearGradient>
    <linearGradient id="{p}_manila" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#DFC494"/>
      <stop offset="100%" stop-color="#B99966"/>
    </linearGradient>
    <linearGradient id="{p}_cyan_to_red" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{PLAN}"/>
      <stop offset="52%" stop-color="#8FA8E6"/>
      <stop offset="100%" stop-color="{RED_BRIGHT}"/>
    </linearGradient>
    <linearGradient id="{p}_hand_skin" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#E6BA9C"/>
      <stop offset="62%" stop-color="#C99677"/>
      <stop offset="100%" stop-color="#9A6B52"/>
    </linearGradient>
    <radialGradient id="{p}_vig" cx="0.5" cy="0.5" r="0.74">
      <stop offset="54%" stop-color="#000000" stop-opacity="0.0"/>
      <stop offset="100%" stop-color="#05070B" stop-opacity="0.76"/>
    </radialGradient>
    <clipPath id="{p}_polaroid_main">
      <rect x="-78" y="-66" width="156" height="118" rx="1"/>
    </clipPath>
    <clipPath id="{p}_polaroid_mini">
      <rect x="-38" y="-32" width="76" height="56" rx="1"/>
    </clipPath>
    <filter id="{p}_glow_cad" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="2.8" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="{p}_glow_red" x="-35%" y="-35%" width="170%" height="170%">
      <feGaussianBlur stdDeviation="3.4" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    """

    parts: list[str] = []

    # ── LAYER 1: uzak (Nocturnal FBI office wall + venetian blinds night glow) ──
    if _katman_aktif(katmanlar, "uzak"):
        uzak: list[str] = ['<g id="s401-uzak">']
        uzak.append(f'<rect x="0" y="0" width="960" height="540" fill="url(#{p}_wall_bg)"/>')
        # Distant venetian blind window on far left (cool night blue contrast)
        uzak.append('<rect x="14" y="24" width="94" height="290" fill="#0B1929" stroke="#1E2A38" stroke-width="2"/>')
        for by in range(34, 310, 14):
            uzak.append(f'<line x1="16" y1="{by}" x2="106" y2="{by}" stroke="#19304A" stroke-width="5" opacity="0.65"/>')
            uzak.append(f'<line x1="16" y1="{by + 4}" x2="106" y2="{by + 4}" stroke="#3C6B94" stroke-width="1" opacity="0.32"/>')
        # Subtle wood wall wainscoting on right
        for wx in range(860, 960, 24):
            uzak.append(f'<line x1="{wx}" y1="0" x2="{wx}" y2="390" stroke="#1C1917" stroke-width="1.2" opacity="0.55"/>')
        uzak.append("</g>")
        parts.append("\n".join(uzak))

    # ── LAYER 2: orta (Corkboard evidence wall, walnut desk, emerald/brass FBI banker's lamp) ──
    if _katman_aktif(katmanlar, "orta"):
        orta: list[str] = ['<g id="s401-orta">']
        # Corkboard wooden frame + cork texture
        orta.append(
            f'<rect x="112" y="26" width="816" height="338" rx="4" fill="url(#{p}_cork_bg)" '
            f'stroke="#1D130C" stroke-width="10"/>'
        )
        orta.append(
            '<rect x="117" y="31" width="806" height="328" rx="2" fill="none" '
            'stroke="#5E432C" stroke-width="1.8" opacity="0.7"/>'
        )
        # Subtle cork speckles
        for _ in range(110):
            cx = rng.uniform(126, 914)
            cy = rng.uniform(40, 352)
            cr = rng.uniform(0.8, 1.9)
            col = "#5E442F" if rng.random() > 0.45 else "#24180F"
            orta.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{cr:.1f}" fill="{col}" opacity="0.34"/>')

        # Dark walnut FBI desk surface
        orta.append(f'<polygon points="0,374 960,374 960,540 0,540" fill="url(#{p}_desk_top)"/>')
        orta.append('<line x1="0" y1="374" x2="960" y2="374" stroke="#4D3725" stroke-width="2.4"/>')
        orta.append('<line x1="0" y1="378" x2="960" y2="378" stroke="#120C08" stroke-width="2"/>')
        # Subtle wood grain lines on desk
        for gy in (402, 434, 472, 510):
            orta.append(f'<line x1="0" y1="{gy}" x2="960" y2="{gy}" stroke="#332318" stroke-width="1" opacity="0.42"/>')

        # Warm ambient lamp light pools across corkboard & desk (A2 continuity from 3.10)
        orta.append(f'<rect x="0" y="0" width="960" height="540" fill="url(#{p}_lamp_pool)"/>')
        orta.append(f'<rect x="0" y="365" width="960" height="175" fill="url(#{p}_lamp_desk_glow)"/>')

        # Classic emerald-green & brass FBI banker's desk lamp (left side)
        # Base
        orta.append(
            f'<ellipse cx="88" cy="442" rx="46" ry="12" fill="#0B0705" opacity="0.58"/>'
            f'<ellipse cx="88" cy="436" rx="42" ry="11" fill="url(#{p}_brass)" stroke="{INK_WARM}" stroke-width="1.8"/>'
            f'<path d="M 64,434 C 68,420 108,420 112,434 Z" fill="url(#{p}_brass)" stroke="{INK_WARM}" stroke-width="1.5"/>'
        )
        # Curved brass arm
        orta.append(
            f'<path d="M 88,424 L 88,334 Q 88,298 118,298 L 138,298" fill="none" '
            f'stroke="{INK_WARM}" stroke-width="10" stroke-linecap="round"/>'
            f'<path d="M 88,424 L 88,334 Q 88,298 118,298 L 138,298" fill="none" '
            f'stroke="url(#{p}_brass)" stroke-width="6.4" stroke-linecap="round"/>'
        )
        # Emerald glass banker shade + warm bulb glow underneath
        orta.append(
            f'<ellipse cx="144" cy="319" rx="52" ry="11" fill="{AMBER_HOT}" opacity="0.92"/>'
            f'<path d="M 96,314 Q 144,274 192,314 L 184,322 Q 144,310 104,322 Z" '
            f'fill="url(#{p}_shade_green)" stroke="{INK_WARM}" stroke-width="2" stroke-linejoin="round"/>'
            f'<path d="M 110,305 Q 144,284 178,305" fill="none" stroke="#62B592" stroke-width="1.8" opacity="0.55"/>'
        )
        # Pull chain
        orta.append(
            '<path d="M 122,320 L 122,356" fill="none" stroke="#D9B05B" stroke-width="1.4"/>'
            '<circle cx="122" cy="359" r="3.4" fill="#F2CA74" stroke="#1A130F" stroke-width="1.1"/>'
        )
        # Subtle amber coffee mug on left-front desk
        orta.append(
            '<ellipse cx="192" cy="462" rx="22" ry="6" fill="#090604" opacity="0.55"/>'
            '<rect x="174" y="422" width="34" height="38" rx="4" fill="#2A2F36" stroke="#121417" stroke-width="1.6"/>'
            '<path d="M 208,430 C 219,430 219,448 208,448" fill="none" stroke="#2A2F36" stroke-width="4.2"/>'
            '<ellipse cx="191" cy="422" rx="17" ry="4.5" fill="#1A1410" stroke="#424952" stroke-width="1.2"/>'
        )
        orta.append("</g>")
        parts.append("\n".join(orta))

    # ── LAYER 3: sahne (Locked A-Sirt v1 polaroid + US Highway Map UTAH/NEW MEXICO/PANAMA + FBI CASE #94941 dossier) ──
    if _katman_aktif(katmanlar, "sahne"):
        sahne: list[str] = ['<g id="s401-sahne">']

        # ── A. Locked A-Sirt v1 Polaroid Photograph (A2 Continuity with 3.10!) ──
        sahne.append('<g transform="translate(278, 182) rotate(-4.5)">')
        # Drop shadow on corkboard
        sahne.append('<rect x="-86" y="-72" width="178" height="162" rx="2" fill="#0A0705" opacity="0.48"/>')
        # Polaroid cream frame
        sahne.append('<rect x="-89" y="-76" width="178" height="160" rx="2" fill="#EFE8DA" stroke="#1A1410" stroke-width="1.6"/>')
        # Clipped dark surveillance backdrop + locked K.michael_sirt_dovme(plan_glow=0.55)
        sahne.append(f'<g clip-path="url(#{p}_polaroid_main)">')
        sahne.append('<rect x="-78" y="-66" width="156" height="118" fill="#131B26"/>')
        sahne.append('<g transform="translate(0, 14) scale(0.245)">')
        sahne.append(sirt_body)
        sahne.append("</g>")
        sahne.append("</g>")
        sahne.append('<rect x="-78" y="-66" width="156" height="118" fill="none" stroke="#26201B" stroke-width="1.1"/>')
        # Red FBI marker annotation on polaroid
        sahne.append(
            f'<circle cx="6" cy="4" r="30" fill="none" stroke="{RED_ALERT}" stroke-width="2.0" stroke-dasharray="5 3"/>'
        )
        sahne.append(
            '<text x="0" y="72" text-anchor="middle" font-family="Consolas, monospace" '
            'font-size="9" font-weight="700" fill="#221C18">EXHIBIT #94941 · BACK TATTOO</text>'
        )
        # Red pushpin at top center of polaroid
        sahne.append(f'<circle cx="0" cy="-68" r="5.5" fill="{RED_ALERT}" stroke="#4A0A12" stroke-width="1.4"/>')
        sahne.append('<circle cx="-1.5" cy="-69.5" r="1.8" fill="#FF9AA4"/>')
        sahne.append("</g>")

        # ── B. Secondary detail polaroid (Forearm / Node clue) ──
        sahne.append('<g transform="translate(418, 102) rotate(5)">')
        sahne.append('<rect x="-42" y="-36" width="88" height="80" rx="2" fill="#0A0705" opacity="0.42"/>')
        sahne.append('<rect x="-44" y="-39" width="88" height="78" rx="2" fill="#EAE2D2" stroke="#1A1410" stroke-width="1.3"/>')
        sahne.append(f'<g clip-path="url(#{p}_polaroid_mini)">')
        sahne.append('<rect x="-38" y="-32" width="76" height="56" fill="#0E1B28"/>')
        # Blueprint fragment preview inside mini photo
        sahne.append(
            f'<path d="M -28,12 L -28,-12 L 4,-12 L 4,6 L 26,6 M -12,-24 L -12,18" '
            f'fill="none" stroke="{PLAN}" stroke-width="1.6" opacity="0.85"/>'
            f'<circle cx="4" cy="-12" r="4" fill="none" stroke="{RED_BRIGHT}" stroke-width="1.5"/>'
        )
        sahne.append("</g>")
        sahne.append(
            '<text x="0" y="33" text-anchor="middle" font-family="Consolas, monospace" '
            'font-size="6.8" font-weight="700" fill="#2A221D">NODE 03 · ROUTE</text>'
        )
        sahne.append(f'<circle cx="0" cy="-34" r="4.2" fill="{AMBER_GOLD}" stroke="#4A3210" stroke-width="1.2"/>')
        sahne.append("</g>")

        # ── C. Pinned US Highway Map (UTAH, NEW MEXICO, PANAMA) ──
        sahne.append('<g transform="translate(514, 52)">')
        # Map drop shadow & parchment sheet
        sahne.append('<rect x="5" y="6" width="374" height="282" rx="2" fill="#0A0705" opacity="0.45"/>')
        sahne.append(
            f'<rect x="0" y="0" width="374" height="282" rx="2" fill="url(#{p}_map_paper)" '
            f'stroke="#2A2118" stroke-width="1.8"/>'
        )
        # Map header bar
        sahne.append('<rect x="10" y="10" width="354" height="24" fill="#252C34"/>')
        sahne.append(
            '<text x="22" y="25.5" font-family="Segoe UI, Arial, sans-serif" font-size="10.5" '
            'font-weight="800" letter-spacing="1.4" fill="#EFE6D2">U.S. INTERSTATE &amp; BORDER CORRIDOR</text>'
        )
        sahne.append(
            '<text x="352" y="25.5" text-anchor="end" font-family="Consolas, monospace" '
            'font-size="9" font-weight="700" fill="#7FE6FF">GRID W-4</text>'
        )

        # Subtle map lat/lon grid inside map frame
        for gx in range(44, 360, 44):
            sahne.append(f'<line x1="{gx}" y1="36" x2="{gx}" y2="272" stroke="#B7A88B" stroke-width="0.7" opacity="0.55"/>')
        for gy in range(74, 270, 44):
            sahne.append(f'<line x1="12" y1="{gy}" x2="362" y2="{gy}" stroke="#B7A88B" stroke-width="0.7" opacity="0.55"/>')

        # Stylized Western / Southern US State Polygons
        # UTAH (hero central-left state highlighted subtly in warm ochre)
        sahne.append(
            '<polygon points="78,56 146,56 146,82 170,82 170,162 78,162" '
            'fill="#D9C398" stroke="#6E5D46" stroke-width="1.6"/>'
        )
        # COLORADO (right of Utah)
        sahne.append(
            '<polygon points="170,82 268,82 268,162 170,162" '
            'fill="#E4D7BC" stroke="#85755C" stroke-width="1.2"/>'
        )
        # ARIZONA (below-left of Utah)
        sahne.append(
            '<polygon points="78,162 162,162 162,248 96,242 74,206" '
            'fill="#E4D7BC" stroke="#85755C" stroke-width="1.2"/>'
        )
        # NEW MEXICO (below Colorado / SE of Utah)
        sahne.append(
            '<polygon points="162,162 254,162 254,250 182,250 182,242 162,242" '
            'fill="#D8C49E" stroke="#6E5D46" stroke-width="1.6"/>'
        )
        # TEXAS / SOUTH BORDER CORRIDOR
        sahne.append(
            '<polygon points="254,162 344,162 344,236 286,256 254,242" '
            'fill="#E5D9C0" stroke="#85755C" stroke-width="1.2"/>'
        )

        # Highway network lines (I-80, I-15, I-40, South Escape Route)
        sahne.append(
            '<path d="M 24,104 Q 78,108 124,114 T 230,104 L 352,118" '
            'fill="none" stroke="#8B6F4B" stroke-width="2.0" stroke-dasharray="5 3"/>'
        )
        sahne.append(
            '<path d="M 124,48 L 124,114 L 116,188 L 198,208 L 288,246 L 334,264" '
            'fill="none" stroke="#A6463A" stroke-width="2.4" stroke-linecap="round"/>'
        )
        # State & Target Labels (100% English, crisp, readable)
        sahne.append(
            '<text x="122" y="138" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif" '
            'font-size="13.5" font-weight="900" letter-spacing="1.4" fill="#2A1E15">UTAH</text>'
        )
        sahne.append(
            '<text x="208" y="204" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif" '
            'font-size="10.5" font-weight="800" letter-spacing="0.8" fill="#2A1E15">NEW MEXICO</text>'
        )
        sahne.append(
            '<circle cx="208" cy="216" r="3.2" fill="#2A1E15"/>'
        )
        # PANAMA southern inset box (cleanly padded)
        sahne.append(
            '<rect x="262" y="236" width="98" height="34" rx="3" fill="#232B33" stroke="#A6463A" stroke-width="1.4"/>'
            '<text x="311" y="251" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif" '
            'font-size="8" font-weight="700" letter-spacing="1.0" fill="#7FE6FF">SOUTH EXIT</text>'
            '<text x="311" y="264" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif" '
            'font-size="11" font-weight="900" letter-spacing="1.4" fill="#FFE6A8">PANAMA</text>'
        )
        # Corner pushpins holding the map
        for px, py in ((16, 16), (358, 16), (16, 268), (358, 268)):
            sahne.append(f'<circle cx="{px}" cy="{py}" r="4.2" fill="#C9A24B" stroke="#3B2910" stroke-width="1.1"/>')
        sahne.append("</g>")

        # ── D. FBI CASE #94941 · MAHONE Manila Dossier on Walnut Desk ──
        sahne.append('<g transform="translate(316, 392) rotate(-2.5)">')
        sahne.append('<rect x="4" y="6" width="332" height="124" rx="4" fill="#090604" opacity="0.58"/>')
        # Manila folder tab
        sahne.append(
            f'<path d="M 16,0 L 138,0 L 152,18 L 328,18 L 328,120 L 0,120 L 0,18 L 8,18 Z" '
            f'fill="url(#{p}_manila)" stroke="{INK_WARM}" stroke-width="1.8" stroke-linejoin="round"/>'
        )
        sahne.append(
            '<text x="76" y="13" text-anchor="middle" font-family="Consolas, monospace" '
            'font-size="9.5" font-weight="800" fill="#261C14">CASE #94941</text>'
        )
        # White typed FBI summary sheet peeking inside folder
        sahne.append('<rect x="18" y="28" width="292" height="80" rx="2" fill="#F4EFE3" stroke="#9B896D" stroke-width="1.1"/>')
        sahne.append(
            '<text x="34" y="49" font-family="Segoe UI, Arial, sans-serif" font-size="13" '
            'font-weight="900" letter-spacing="1.1" fill="#181F28">FBI CASE #94941 · MAHONE</text>'
        )
        sahne.append('<line x1="34" y1="56" x2="294" y2="56" stroke="#8C7E69" stroke-width="1.1"/>')
        sahne.append(
            '<text x="34" y="74" font-family="Consolas, monospace" font-size="10" '
            'font-weight="700" fill="#2E3640">SUBJECT: MICHAEL SCOFIELD · STRUCTURAL ENG.</text>'
        )
        sahne.append(
            '<text x="34" y="92" font-family="Consolas, monospace" font-size="10" '
            'font-weight="700" fill="#9E222E">LEAD: TATTOO BLUEPRINT -&gt; UTAH / NM / PANAMA</text>'
        )
        sahne.append("</g>")

        sahne.append("</g>")
        parts.append("\n".join(sahne))

    # ── LAYER 3B: kirmizi_ip (Independently animatable red investigation strings) ──
    if _katman_aktif(katmanlar, "kirmizi_ip"):
        ip: list[str] = ['<g id="s401-kirmizi_ip">']
        # String anchor coordinates (world space):
        # Polaroid pin (272, 115), Polaroid tattoo center (284, 186), Mini photo pin (421, 68),
        # Map UTAH pin (636, 166), Map NEW MEXICO dot (722, 268), Map PANAMA box (825, 294)
        strings = [
            "M 272,115 Q 350,76 421,68",
            "M 421,68 Q 528,118 636,166",
            "M 284,186 Q 462,216 636,166",
            "M 636,166 Q 684,224 722,268",
            "M 722,268 Q 776,286 825,294",
        ]
        for sd in strings:
            # Soft shadow on corkboard
            ip.append(
                f'<path d="{sd}" fill="none" stroke="#160608" stroke-width="3.6" '
                f'opacity="0.45" transform="translate(2, 4)"/>'
            )
            # Crisp red yarn thread
            ip.append(
                f'<path d="{sd}" fill="none" stroke="{RED_ALERT}" stroke-width="2.4" '
                f'stroke-linecap="round"/>'
            )
            # Fine highlight sheen on thread
            ip.append(
                f'<path d="{sd}" fill="none" stroke="#FF8D98" stroke-width="0.7" '
                f'opacity="0.65"/>'
            )
        # Small red junction pins on New Mexico & Panama
        for jx, jy in ((722, 268), (825, 294)):
            ip.append(f'<circle cx="{jx}" cy="{jy}" r="4.5" fill="{RED_ALERT}" stroke="#4A0A12" stroke-width="1.2"/>')
        ip.append("</g>")
        parts.append("\n".join(ip))

    # ── LAYER 3C: harita_igne (R4 SINGLE LAYER: anatomical 5-finger FBI hand pressing red pushpin onto UTAH) ──
    if _katman_aktif(katmanlar, "harita_igne"):
        igne: list[str] = ['<g id="s401-harita_igne">']
        # Red concentric target ring directly around UTAH pin (636, 166)
        igne.append(
            f'<circle cx="636" cy="166" r="24" fill="none" stroke="{RED_BRIGHT}" stroke-width="1.8" '
            f'stroke-dasharray="5 4" filter="url(#{p}_glow_red)"/>'
        )
        igne.append(
            f'<circle cx="636" cy="166" r="13" fill="none" stroke="{RED_ALERT}" stroke-width="1.5" opacity="0.9"/>'
        )

        # Soft cast shadow beneath the hand, curled fingers & wrist on map (leaves UTAH/NM/PANAMA clear)
        igne.append(
            '<path d="M 652,162 C 674,174 714,182 752,166 L 960,96 L 960,34 L 768,100 '
            'C 726,110 676,120 652,150 Z" fill="#140B06" opacity="0.22"/>'
        )

        # 1. Steel needle + glossy red pushpin body planted at UTAH (636, 166)
        igne.append('<line x1="636" y1="166" x2="646" y2="155" stroke="#C8CFD6" stroke-width="2.0" stroke-linecap="round"/>')
        igne.append(
            f'<ellipse cx="647" cy="154" rx="6.8" ry="6.2" fill="#B51B2B" stroke="#3D0810" stroke-width="1.4"/>'
            f'<circle cx="650" cy="151" r="6.2" fill="{RED_ALERT}" stroke="#3D0810" stroke-width="1.4"/>'
            '<circle cx="648" cy="148.5" r="2.0" fill="#FFB8C0" opacity="0.9"/>'
        )

        # 2. Curled 5th (pinky), 4th (ring) & 3rd (middle) fingers tucked naturally behind palm (back-to-front)
        # Pinky finger (smallest, deepest shadow)
        igne.append(
            f'<path d="M 738,144 C 728,158 718,166 711,164 C 706,162 707,154 714,148 L 732,136 Z" '
            f'fill="#A6755B" stroke="{INK_WARM}" stroke-width="1.4" stroke-linejoin="round"/>'
        )
        # Ring finger (medium length, soft shadow)
        igne.append(
            f'<path d="M 730,138 C 716,156 702,168 693,165 C 687,163 689,153 698,145 L 720,130 Z" '
            f'fill="#B9876B" stroke="{INK_WARM}" stroke-width="1.5" stroke-linejoin="round"/>'
        )
        igne.append(
            '<path d="M 702,152 Q 707,157 704,162" fill="none" stroke="#7A4F3A" stroke-width="1.0" stroke-linecap="round"/>'
        )
        # Middle finger (longest curled finger, resting cleanly below index & behind thumb)
        igne.append(
            f'<path d="M 720,130 C 702,148 686,162 677,159 C 671,156 674,146 684,138 L 710,122 Z" '
            f'fill="#C89578" stroke="{INK_WARM}" stroke-width="1.5" stroke-linejoin="round"/>'
        )
        igne.append(
            '<path d="M 688,144 Q 693,149 690,155" fill="none" stroke="#7A4F3A" stroke-width="1.0" stroke-linecap="round"/>'
        )

        # 3. Slender wrist + anatomical palm / back of hand + rounded thenar eminence (thumb base)
        igne.append(
            f'<path d="M 786,98 L 748,104 C 732,107 718,110 708,116 C 700,122 702,136 714,146 '
            f'C 726,154 748,154 768,144 L 796,136 Z" '
            f'fill="url(#{p}_hand_skin)" stroke="{INK_WARM}" stroke-width="1.7" stroke-linejoin="round"/>'
        )
        # Warm key-light highlight on back of hand & subtle metacarpal tendons
        igne.append(
            '<path d="M 776,105 Q 746,109 722,115" fill="none" stroke="#F5D7BE" stroke-width="2.4" opacity="0.55" stroke-linecap="round"/>'
            '<path d="M 768,116 Q 746,120 726,124 M 772,126 Q 752,130 734,135" fill="none" '
            'stroke="#91624B" stroke-width="1.0" opacity="0.42" stroke-linecap="round"/>'
        )

        # 4. Natural Thumb supporting pushpin from underneath/side with thenar eminence curve
        igne.append(
            f'<path d="M 744,145 C 724,154 700,160 680,161 C 666,161 654,160 651,155 '
            f'C 649,151 654,147 662,148 C 674,149 686,146 702,139 C 714,134 728,132 742,135" '
            f'fill="url(#{p}_hand_skin)" stroke="{INK_WARM}" stroke-width="1.65" stroke-linecap="round" stroke-linejoin="round"/>'
        )
        # Thumb underside shadow + IP joint crease + subtle nail rim
        igne.append(
            '<path d="M 656,158 Q 682,160 718,152" fill="none" stroke="#8C5D46" stroke-width="1.6" opacity="0.55" stroke-linecap="round"/>'
            '<path d="M 681,150 Q 683,155 680,159" fill="none" stroke="#7A4F3A" stroke-width="1.0" stroke-linecap="round"/>'
            '<path d="M 652,155 Q 655,151 660,151" fill="none" stroke="#F6DEC8" stroke-width="1.1" opacity="0.7" stroke-linecap="round"/>'
        )

        # 5. Graceful Index Finger curving naturally onto top of red pushpin (fingernail + 2 joint creases)
        igne.append(
            f'<path d="M 718,113 C 702,113 688,115 676,122 C 664,129 653,138 648,145 '
            f'C 645,149 650,153 656,150 C 664,146 673,138 684,132 C 696,126 708,125 722,126" '
            f'fill="url(#{p}_hand_skin)" stroke="{INK_WARM}" stroke-width="1.65" stroke-linecap="round" stroke-linejoin="round"/>'
        )
        # Index finger warm top highlight
        igne.append(
            '<path d="M 710,116 C 696,116 684,119 672,126" fill="none" stroke="#F6D8BF" stroke-width="1.7" opacity="0.62" stroke-linecap="round"/>'
        )
        # Index finger 2 anatomical knuckle/joint creases (PIP & DIP)
        igne.append(
            '<path d="M 685,119 Q 689,123 687,127 M 667,129 Q 670,133 668,137" fill="none" '
            'stroke="#7A4F3A" stroke-width="1.05" stroke-linecap="round"/>'
        )
        # Delicate fingernail on upper curve of index fingertip
        igne.append(
            '<path d="M 649,144 C 651,140 656,138 659,140 C 657,143 653,146 649,144 Z" '
            'fill="#F6DFCE" stroke="#7A4F3A" stroke-width="0.9" stroke-linejoin="round"/>'
        )

        # 6. Slender white dress-shirt cuff + silver cufflink + tailored dark charcoal FBI suit sleeve
        igne.append(
            f'<path d="M 776,94 L 804,84 L 820,134 L 792,143 Z" '
            f'fill="#ECE9E0" stroke="{INK}" stroke-width="1.6" stroke-linejoin="round"/>'
        )
        igne.append(
            '<path d="M 782,135 L 814,125" fill="none" stroke="#C5C0B4" stroke-width="1.8" opacity="0.75"/>'
            '<circle cx="801" cy="126" r="3.0" fill="#9AA8B8" stroke="#1E242C" stroke-width="1.0"/>'
        )
        igne.append(
            f'<path d="M 800,80 L 960,24 L 960,92 L 818,138 Z" '
            f'fill="#1A2029" stroke="{INK}" stroke-width="2.0" stroke-linejoin="round"/>'
        )
        igne.append(
            '<path d="M 812,92 L 954,42" fill="none" stroke="#364254" stroke-width="2.0" opacity="0.65"/>'
        )
        igne.append("</g>")
        parts.append("\n".join(igne))

    # ── LAYER 4: plan (Cyan-to-red DECODING MAP · UTAH CAD + ANOTHER MIND HUD) ──
    if _katman_aktif(katmanlar, "plan"):
        plan: list[str] = ['<g id="s401-plan">']
        # Cyan-to-red CAD decoding trajectory from A-Sirt v1 polaroid to UTAH pin
        plan.append(
            f'<path d="M 284,186 C 390,118 524,114 636,166" fill="none" '
            f'stroke="url(#{p}_cyan_to_red)" stroke-width="2.6" stroke-dasharray="8 5" '
            f'filter="url(#{p}_glow_cad)"/>'
        )
        # Cyan targeting bracket on A-Sirt v1 polaroid
        plan.append(
            f'<path d="M 234,142 L 224,142 L 224,152 M 332,142 L 342,142 L 342,152 '
            f'M 234,230 L 224,230 L 224,220 M 332,230 L 342,230 L 342,220" '
            f'fill="none" stroke="{PLAN}" stroke-width="1.6" opacity="0.88"/>'
        )
        # CAD decoding callout chip placed cleanly in open corkboard space below strings (zero overlap!)
        plan.append(
            f'<rect x="292" y="294" width="212" height="24" rx="4" fill="#08121D" fill-opacity="0.92" '
            f'stroke="url(#{p}_cyan_to_red)" stroke-width="1.4"/>'
        )
        plan.append(
            f'<text x="398" y="310" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif" '
            f'font-size="10.5" font-weight="800" letter-spacing="1.4" fill="{PLAN_CORE}">DECODING MAP · UTAH</text>'
        )

        # Hero HUD badge top-left: ANOTHER MIND (box width 276px -> generous >=22px right padding)
        plan.append(
            f'<rect x="26" y="24" width="276" height="62" rx="6" fill="#08111B" fill-opacity="0.90" '
            f'stroke="url(#{p}_cyan_to_red)" stroke-width="1.7"/>'
        )
        plan.append(f'<rect x="38" y="34" width="8" height="42" rx="2" fill="{RED_ALERT}"/>')
        plan.append(
            f'<text x="58" y="51" font-family="Segoe UI, Arial, sans-serif" font-size="10" '
            f'font-weight="700" letter-spacing="1.5" fill="{PLAN}">FBI SPECIAL AGENT · MAHONE</text>'
        )
        plan.append(
            f'<text x="58" y="75" font-family="Segoe UI, Arial, sans-serif" font-size="20" '
            f'font-weight="900" letter-spacing="1.8" fill="#FFE6EA">ANOTHER MIND</text>'
        )
        plan.append("</g>")
        parts.append("\n".join(plan))

    # ── LAYER 5: onplan (Warm lamp dust motes, vignette & viewfinder corners) ──
    if _katman_aktif(katmanlar, "onplan"):
        onplan: list[str] = ['<g id="s401-onplan">']
        for _ in range(26):
            dx = rng.uniform(50, 440)
            dy = rng.uniform(160, 470)
            dr = rng.uniform(0.9, 2.2)
            op = rng.uniform(0.22, 0.62)
            onplan.append(f'<circle cx="{dx:.1f}" cy="{dy:.1f}" r="{dr:.1f}" fill="{AMBER_HOT}" opacity="{op:.2f}"/>')
        onplan.append(f'<rect x="0" y="0" width="960" height="540" fill="url(#{p}_vig)"/>')
        onplan.append(
            f'<path d="M 22,42 L 22,22 L 42,22 M 918,22 L 938,22 L 938,42 '
            f'M 22,498 L 22,518 L 42,518 M 918,518 L 938,518 L 938,498" '
            f'fill="none" stroke="{PLAN}" stroke-width="1.3" opacity="0.45"/>'
        )
        onplan.append("</g>")
        parts.append("\n".join(onplan))

    return defs, "\n".join(parts)


# =============================================================================
# SCENE 4.02: NIGHT HIGHWAY & FAKE ALIASES (GAG 2: "NEW NAME.")
# =============================================================================
def set_402_otoyol_kimlik(
    katmanlar: set[str] | list[str] | None = None,
) -> tuple[str, str]:
    """Rainy night US highway seen through car windshield: rushing yellow-dashed road,
    distant red-blue police headlights in rearview mirror, and 3 independently animatable
    fake alias cards (`kart_1`: MICHAEL CRANE · DRIVER LICENSE with locked K.michael_kafa
    'front'/'odak' & clean Collar-Over-Neck, `kart_2`: E.F.G. · PASSPORT · UTAH,
    `kart_3`: LINCOLN STADMAN · ID CARD + red NEW NAME. stamp) + ALIAS TRACKER CAD.
    """
    rng = random.Random(402)
    p = _uid("s402")

    michael_head = K.michael_kafa("front", "odak", look=0.0, boyun=False)

    defs = f"""
    <linearGradient id="{p}_sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#050A12"/>
      <stop offset="56%" stop-color="#0D192B"/>
      <stop offset="100%" stop-color="#1A293C"/>
    </linearGradient>
    <radialGradient id="{p}_horizon_glow" cx="0.50" cy="0.48" r="0.44">
      <stop offset="0%" stop-color="#48688C" stop-opacity="0.34"/>
      <stop offset="55%" stop-color="#1A2C42" stop-opacity="0.14"/>
      <stop offset="100%" stop-color="#050A12" stop-opacity="0.0"/>
    </radialGradient>
    <linearGradient id="{p}_road" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#0F1722"/>
      <stop offset="45%" stop-color="#172230"/>
      <stop offset="100%" stop-color="#0B1119"/>
    </linearGradient>
    <linearGradient id="{p}_headlight_cone" x1="0.5" y1="1" x2="0.5" y2="0">
      <stop offset="0%" stop-color="#FFF2CC" stop-opacity="0.32"/>
      <stop offset="65%" stop-color="#C9DDF0" stop-opacity="0.10"/>
      <stop offset="100%" stop-color="#C9DDF0" stop-opacity="0.0"/>
    </linearGradient>
    <linearGradient id="{p}_dash_g" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#18202B"/>
      <stop offset="35%" stop-color="#10151D"/>
      <stop offset="100%" stop-color="#070A0F"/>
    </linearGradient>
    <linearGradient id="{p}_dl_card" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F2F6FA"/>
      <stop offset="65%" stop-color="#DFE8F0"/>
      <stop offset="100%" stop-color="#C6D4E0"/>
    </linearGradient>
    <linearGradient id="{p}_passport_cov" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#1A2C47"/>
      <stop offset="58%" stop-color="#122036"/>
      <stop offset="100%" stop-color="#0A1424"/>
    </linearGradient>
    <linearGradient id="{p}_id3_card" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F6F2E9"/>
      <stop offset="62%" stop-color="#E6DFD0"/>
      <stop offset="100%" stop-color="#D2C8B4"/>
    </linearGradient>
    <radialGradient id="{p}_vig" cx="0.5" cy="0.5" r="0.74">
      <stop offset="52%" stop-color="#000000" stop-opacity="0.0"/>
      <stop offset="100%" stop-color="#03060B" stop-opacity="0.78"/>
    </radialGradient>
    <clipPath id="{p}_photo_clip_k1">
      <rect x="-108" y="-36" width="76" height="90" rx="3"/>
    </clipPath>
    <clipPath id="{p}_photo_clip_k3">
      <rect x="-106" y="-34" width="68" height="82" rx="3"/>
    </clipPath>
    <filter id="{p}_glow_siren" x="-45%" y="-45%" width="190%" height="190%">
      <feGaussianBlur stdDeviation="4.0" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="{p}_glow_cad" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="2.6" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    """

    parts: list[str] = []

    # ── LAYER 1: uzak (Stormy night sky, desert/interstate horizon & rushing wet yellow-dashed highway) ──
    if _katman_aktif(katmanlar, "uzak"):
        uzak: list[str] = ['<g id="s402-uzak">']
        uzak.append(f'<rect x="0" y="0" width="960" height="270" fill="url(#{p}_sky)"/>')
        uzak.append(f'<rect x="0" y="0" width="960" height="300" fill="url(#{p}_horizon_glow)"/>')
        # Distant low mesas / highway treeline silhouette
        uzak.append(
            '<path d="M 0,266 L 90,256 L 170,258 L 245,244 L 340,254 L 440,262 '
            'L 530,262 L 620,252 L 730,248 L 835,258 L 960,250 L 960,276 L 0,276 Z" '
            'fill="#0B131E"/>'
        )
        # Wet night interstate highway perspective
        uzak.append(f'<rect x="0" y="266" width="960" height="274" fill="url(#{p}_road)"/>')
        # Road shoulder polygons
        uzak.append('<polygon points="0,266 446,266 110,450 0,450" fill="#0B111A"/>')
        uzak.append('<polygon points="514,266 960,266 960,450 850,450" fill="#0B111A"/>')
        # White outer shoulder lines
        uzak.append('<line x1="446" y1="266" x2="122" y2="446" stroke="#89A4BE" stroke-width="2.2" opacity="0.55"/>')
        uzak.append('<line x1="514" y1="266" x2="838" y2="446" stroke="#89A4BE" stroke-width="2.2" opacity="0.55"/>')
        # Rushing golden-yellow center dashes
        dashes = [
            (478, 272, 482, 272, 483, 286, 477, 286),
            (476, 300, 484, 300, 486, 326, 474, 326),
            (472, 348, 488, 348, 492, 392, 468, 392),
            (466, 414, 494, 414, 498, 448, 462, 448),
        ]
        for pts in dashes:
            uzak.append(
                f'<polygon points="{pts[0]},{pts[1]} {pts[2]},{pts[3]} {pts[4]},{pts[5]} {pts[6]},{pts[7]}" '
                f'fill="#F6C945" opacity="0.92"/>'
            )
            # Wet asphalt reflection under each yellow dash
            uzak.append(
                f'<polygon points="{pts[0] - 4},{pts[5]} {pts[2] + 4},{pts[5]} {pts[4] + 6},{pts[5] + 10} {pts[6] - 6},{pts[5] + 10}" '
                f'fill="#F6C945" opacity="0.18"/>'
            )
        # Car headlights illuminating wet tarmac ahead
        uzak.append(f'<polygon points="220,446 432,272 528,272 740,446" fill="url(#{p}_headlight_cone)"/>')
        # Distant highway overhead lamps
        for lx, ly, lr in ((398, 250, 2.2), (562, 250, 2.2), (322, 240, 3.0), (638, 240, 3.0)):
            uzak.append(f'<circle cx="{lx}" cy="{ly}" r="{lr * 3.5:.1f}" fill="#FFCE73" opacity="0.20"/>')
            uzak.append(f'<circle cx="{lx}" cy="{ly}" r="{lr:.1f}" fill="#FFF1C2" opacity="0.88"/>')
        uzak.append("</g>")
        parts.append("\n".join(uzak))

    # ── LAYER 2: orta (Car cockpit interior: A-pillars, wet windshield, dashboard, rearview mirror with red-blue police lights) ──
    if _katman_aktif(katmanlar, "orta"):
        orta: list[str] = ['<g id="s402-orta">']
        # Subtle windshield wiper sweep arc on glass
        orta.append(
            '<path d="M 160,418 A 340,340 0 0 1 780,418" fill="none" stroke="#8AB4D8" '
            'stroke-width="1.2" opacity="0.16"/>'
        )
        # Car interior roof headliner + left & right A-pillars
        orta.append('<polygon points="0,0 960,0 960,48 0,48" fill="#0B0F15"/>')
        orta.append('<polygon points="0,0 92,0 38,448 0,448" fill="#0D121A" stroke="#1E2936" stroke-width="1.5"/>')
        orta.append('<polygon points="868,0 960,0 960,448 922,448" fill="#0D121A" stroke="#1E2936" stroke-width="1.5"/>')

        # Dashboard cowl + subtle speedometer dial + steering wheel rim
        orta.append(
            f'<path d="M 0,442 Q 240,404 480,412 Q 720,404 960,442 L 960,540 L 0,540 Z" '
            f'fill="url(#{p}_dash_g)" stroke="#243040" stroke-width="2"/>'
        )
        # Subtle cyan-green instrument cluster glow on driver side (left)
        orta.append('<ellipse cx="220" cy="468" rx="76" ry="26" fill="#09131C" stroke="#24384C" stroke-width="1.6"/>')
        orta.append('<circle cx="192" cy="470" r="18" fill="none" stroke="#366E8C" stroke-width="1.6" opacity="0.7"/>')
        orta.append('<line x1="192" y1="470" x2="203" y2="459" stroke="#FF6B78" stroke-width="1.8" stroke-linecap="round"/>')
        orta.append(
            '<text x="242" y="474" text-anchor="middle" font-family="Consolas, monospace" '
            'font-size="11" font-weight="700" fill="#7FE6FF">74 MPH</text>'
        )
        # Upper steering wheel arc silhouette on left
        orta.append(
            '<path d="M 104,540 A 126,126 0 0 1 336,540" fill="none" stroke="#0B0F14" stroke-width="22"/>'
            '<path d="M 104,540 A 126,126 0 0 1 336,540" fill="none" stroke="#25303D" stroke-width="2.2" opacity="0.7"/>'
        )

        # Rearview Mirror mounted top-center with glowing distant RED & BLUE police headlights!
        orta.append('<rect x="474" y="30" width="12" height="24" fill="#121820"/>')
        orta.append(
            f'<rect x="372" y="48" width="216" height="58" rx="12" fill="#0E141D" '
            f'stroke="#344456" stroke-width="2.6"/>'
        )
        orta.append('<rect x="380" y="55" width="200" height="44" rx="8" fill="#08101A"/>')
        # Reflected dark road inside rearview mirror
        orta.append('<polygon points="454,76 506,76 544,99 416,99" fill="#131F2E"/>')
        # Distant glowing RED & BLUE police cruiser headlights + siren bar in mirror
        orta.append(
            f'<circle cx="464" cy="74" r="12" fill="{SIREN_RED}" opacity="0.58" filter="url(#{p}_glow_siren)"/>'
            f'<circle cx="496" cy="74" r="12" fill="{SIREN_BLUE}" opacity="0.58" filter="url(#{p}_glow_siren)"/>'
            f'<circle cx="464" cy="74" r="3.4" fill="#FFD6DC"/>'
            f'<circle cx="496" cy="74" r="3.4" fill="#D8ECFF"/>'
            '<circle cx="472" cy="83" r="2.2" fill="#FFF4C8"/>'
            '<circle cx="488" cy="83" r="2.2" fill="#FFF4C8"/>'
        )
        # Subtle mirror glass diagonal sheen
        orta.append('<line x1="392" y1="58" x2="418" y2="96" stroke="#A6CCE8" stroke-width="2.2" opacity="0.16"/>')

        orta.append("</g>")
        parts.append("\n".join(orta))

    # ── LAYER 3A: kart_1 (Independently animatable Card 1: MICHAEL CRANE · DRIVER LICENSE with locked K.michael_kafa) ──
    if _katman_aktif(katmanlar, "kart_1"):
        k1: list[str] = ['<g id="s402-kart_1">']
        k1.append('<g transform="translate(216, 266) rotate(-11)">')
        # Card drop shadow
        k1.append('<rect x="-120" y="-76" width="248" height="154" rx="10" fill="#04080E" opacity="0.56"/>')
        # Card base
        k1.append(
            f'<rect x="-124" y="-80" width="248" height="154" rx="10" fill="url(#{p}_dl_card)" '
            f'stroke="{INK}" stroke-width="2.2"/>'
        )
        # Top state header bar
        k1.append('<path d="M -124,-70 Q -124,-80 -114,-80 L 114,-80 Q 124,-80 124,-70 L 124,-46 L -124,-46 Z" fill="#1D446E"/>')
        k1.append(
            '<text x="0" y="-58" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif" '
            'font-size="11.5" font-weight="900" letter-spacing="1.6" fill="#F2F8FC">DRIVER LICENSE · US</text>'
        )
        # Gold micro security stripe
        k1.append('<rect x="-124" y="-46" width="248" height="4" fill="#D9A84A"/>')

        # Clipped ID photo window + locked K.michael_kafa("front", "odak") with clean Collar-Over-Neck!
        k1.append(f'<g clip-path="url(#{p}_photo_clip_k1)">')
        k1.append('<rect x="-108" y="-36" width="76" height="90" fill="#88A6BF"/>')
        # Neck (drawn first, behind collar & head)
        k1.append('<rect x="-80" y="18" width="20" height="24" fill="#B8876A" stroke="#1A1513" stroke-width="1.2"/>')
        # Shirt & dark jacket Collar-Over-Neck (covers lower neck cleanly!)
        k1.append(
            '<path d="M -110,56 L -102,34 Q -70,26 -38,34 L -30,56 Z" fill="#2A3848" stroke="#1A1513" stroke-width="1.5"/>'
            '<path d="M -83,31 L -70,47 L -57,31 Z" fill="#EAE6DC" stroke="#1A1513" stroke-width="1.1"/>'
            '<path d="M -88,32 L -74,47 L -82,54 M -52,32 L -66,47 L -58,54" fill="none" stroke="#4D6B8A" stroke-width="2.0" stroke-linecap="round"/>'
        )
        # Locked Adult Michael Front Head centered cleanly above collar
        k1.append('<g transform="translate(-70, -6) scale(0.305)">')
        k1.append(michael_head)
        k1.append("</g>")
        k1.append("</g>")
        k1.append('<rect x="-108" y="-36" width="76" height="90" rx="3" fill="none" stroke="#2D4359" stroke-width="1.5"/>')

        # License text fields (100% English, crisp, zero overflow)
        k1.append(
            '<text x="-22" y="-22" font-family="Segoe UI, Arial, sans-serif" font-size="8" '
            'font-weight="700" letter-spacing="0.9" fill="#466078">FULL NAME</text>'
            '<text x="-22" y="-6" font-family="Segoe UI, Arial, sans-serif" font-size="13.5" '
            'font-weight="900" fill="#121D2B">MICHAEL CRANE</text>'
            '<text x="-22" y="13" font-family="Consolas, monospace" font-size="8.8" '
            'font-weight="700" fill="#2D4156">DL #8841-CR-09</text>'
            '<text x="-22" y="28" font-family="Consolas, monospace" font-size="8.5" '
            'font-weight="700" fill="#466078">DOB: 10/08/1974</text>'
            '<text x="-22" y="42" font-family="Consolas, monospace" font-size="8.5" '
            'font-weight="700" fill="#466078">CLASS: D · EXP 09/12</text>'
        )
        # Stylized signature + barcode strip
        k1.append(
            '<path d="M -22,56 Q -4,47 8,55 T 38,53 T 66,56" fill="none" stroke="#1B2E46" stroke-width="1.5" stroke-linecap="round"/>'
        )
        for bx in range(-106, -34, 5):
            bw = 2.4 if (bx % 3 == 0) else 1.2
            k1.append(f'<rect x="{bx}" y="58" width="{bw}" height="9" fill="#18222C"/>')
        k1.append("</g>")
        k1.append("</g>")
        parts.append("\n".join(k1))

    # ── LAYER 3B: kart_2 (Independently animatable Card 2: E.F.G. · PASSPORT · UTAH) ──
    if _katman_aktif(katmanlar, "kart_2"):
        k2: list[str] = ['<g id="s402-kart_2">']
        k2.append('<g transform="translate(492, 224) rotate(4)">')
        # Drop shadow
        k2.append('<rect x="-86" y="-102" width="180" height="214" rx="10" fill="#04080E" opacity="0.58"/>')
        # Navy passport cover
        k2.append(
            f'<rect x="-90" y="-106" width="180" height="214" rx="10" fill="url(#{p}_passport_cov)" '
            f'stroke="{INK}" stroke-width="2.2"/>'
        )
        # Gold border inlay
        k2.append(
            '<rect x="-80" y="-96" width="160" height="194" rx="6" fill="none" '
            'stroke="#D9B05B" stroke-width="1.3" opacity="0.82"/>'
        )
        # Header
        k2.append(
            '<text x="0" y="-72" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif" '
            'font-size="13" font-weight="900" letter-spacing="2.4" fill="#F2CA74">PASSPORT</text>'
        )
        # Stylized gold globe/crest emblem
        k2.append('<circle cx="0" cy="-26" r="28" fill="none" stroke="#D9B05B" stroke-width="1.8"/>')
        k2.append('<ellipse cx="0" cy="-26" rx="14" ry="28" fill="none" stroke="#D9B05B" stroke-width="1.2"/>')
        k2.append('<line x1="-28" y1="-26" x2="28" y2="-26" stroke="#D9B05B" stroke-width="1.2"/>')
        k2.append('<line x1="-24" y1="-39" x2="24" y2="-39" stroke="#D9B05B" stroke-width="1.0"/>')
        k2.append('<line x1="-24" y1="-13" x2="24" y2="-13" stroke="#D9B05B" stroke-width="1.0"/>')
        # Alias details
        k2.append(
            '<rect x="-66" y="16" width="132" height="44" rx="4" fill="#0D192B" stroke="#D9B05B" stroke-width="1.1"/>'
            '<text x="0" y="36" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif" '
            'font-size="16" font-weight="900" letter-spacing="2.6" fill="#FFE6A8">E.F.G.</text>'
            '<text x="0" y="53" text-anchor="middle" font-family="Consolas, monospace" '
            'font-size="10" font-weight="700" letter-spacing="1.4" fill="#7FE6FF">UTAH · TRANSIT</text>'
        )
        # Bottom gold passport chip icon
        k2.append(
            '<rect x="-18" y="72" width="36" height="16" rx="2" fill="none" stroke="#D9B05B" stroke-width="1.4"/>'
            '<circle cx="0" cy="80" r="4.2" fill="none" stroke="#D9B05B" stroke-width="1.3"/>'
        )
        k2.append("</g>")
        k2.append("</g>")
        parts.append("\n".join(k2))

    # ── LAYER 3C: kart_3 (Independently animatable Card 3: LINCOLN STADMAN · ID CARD + red NEW NAME. stamp) ──
    if _katman_aktif(katmanlar, "kart_3"):
        k3: list[str] = ['<g id="s402-kart_3">']
        k3.append('<g transform="translate(756, 272) rotate(9.5)">')
        # Drop shadow
        k3.append('<rect x="-118" y="-74" width="244" height="152" rx="10" fill="#04080E" opacity="0.58"/>')
        # Card base
        k3.append(
            f'<rect x="-122" y="-78" width="244" height="152" rx="10" fill="url(#{p}_id3_card)" '
            f'stroke="{INK}" stroke-width="2.2"/>'
        )
        # Dark slate-crimson header bar
        k3.append('<path d="M -122,-68 Q -122,-78 -112,-78 L 112,-78 Q 122,-78 122,-68 L 122,-46 L -122,-46 Z" fill="#2A323D"/>')
        k3.append(
            '<text x="0" y="-57.5" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif" '
            'font-size="11" font-weight="900" letter-spacing="1.8" fill="#F2EDE2">STATE ID CARD</text>'
        )
        # Clipped stylized portrait silhouette (broad-shouldered Lincoln alias)
        k3.append(f'<g clip-path="url(#{p}_photo_clip_k3)">')
        k3.append('<rect x="-106" y="-34" width="68" height="82" fill="#9EB2C2"/>')
        k3.append('<path d="M -108,52 L -102,24 Q -72,14 -42,24 L -36,52 Z" fill="#28313D" stroke="#161B22" stroke-width="1.4"/>')
        k3.append('<rect x="-82" y="8" width="20" height="18" fill="#BA8466"/>')
        k3.append('<ellipse cx="-72" cy="-6" rx="19" ry="23" fill="#CE9778" stroke="#1A1513" stroke-width="1.5"/>')
        k3.append('<path d="M -90,-12 Q -88,-30 -72,-30 Q -56,-30 -54,-12 Q -62,-20 -72,-20 Q -82,-20 -90,-12 Z" fill="#261F1A"/>')
        # Eyes + brow + firm mouth
        k3.append('<line x1="-83" y1="-11" x2="-74" y2="-11" stroke="#1E1814" stroke-width="2.4" stroke-linecap="round"/>')
        k3.append('<line x1="-70" y1="-11" x2="-61" y2="-11" stroke="#1E1814" stroke-width="2.4" stroke-linecap="round"/>')
        k3.append('<circle cx="-78" cy="-6" r="1.8" fill="#1E2830"/>')
        k3.append('<circle cx="-66" cy="-6" r="1.8" fill="#1E2830"/>')
        k3.append('<line x1="-77" y1="6" x2="-67" y2="6" stroke="#4D2E25" stroke-width="1.7" stroke-linecap="round"/>')
        k3.append("</g>")
        k3.append('<rect x="-106" y="-34" width="68" height="82" rx="3" fill="none" stroke="#3A4554" stroke-width="1.4"/>')

        # Card text fields
        k3.append(
            '<text x="-28" y="-22" font-family="Segoe UI, Arial, sans-serif" font-size="7.8" '
            'font-weight="700" letter-spacing="0.9" fill="#5A5348">ALIAS HOLDER</text>'
            '<text x="-28" y="-7" font-family="Segoe UI, Arial, sans-serif" font-size="12.5" '
            'font-weight="900" fill="#1A1C20">LINCOLN STADMAN</text>'
            '<text x="-28" y="11" font-family="Consolas, monospace" font-size="8.6" '
            'font-weight="700" fill="#3B3A36">ID #0492-LS · ACTIVE</text>'
            '<text x="-28" y="25" font-family="Consolas, monospace" font-size="8.4" '
            'font-weight="700" fill="#5A5348">ISSUED: PHOENIX AZ</text>'
        )

        # Bold crimson rubber stamp: "NEW NAME." (generous width 164px -> >=20px padding each side!)
        k3.append('<g transform="translate(22, 46) rotate(-14)">')
        k3.append(
            f'<rect x="-82" y="-18" width="164" height="36" rx="4" fill="#F8ECEC" fill-opacity="0.90" '
            f'stroke="{RED_ALERT}" stroke-width="2.6"/>'
        )
        k3.append(
            f'<rect x="-77" y="-13" width="154" height="26" rx="2" fill="none" '
            f'stroke="{RED_ALERT}" stroke-width="1.0" stroke-dasharray="4 2"/>'
        )
        k3.append(
            f'<text x="0" y="6.5" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif" '
            f'font-size="17" font-weight="900" letter-spacing="2.0" fill="{RED_ALERT}">NEW NAME.</text>'
        )
        k3.append("</g>")

        k3.append("</g>")
        k3.append("</g>")
        parts.append("\n".join(k3))

    # ── LAYER 3D: sahne (Windshield rain streaks & motion air-trails behind flying alias cards) ──
    if _katman_aktif(katmanlar, "sahne"):
        sahne: list[str] = ['<g id="s402-sahne">']
        # Subtle speed/toss motion arcs trailing behind the 3 cards
        sahne.append(
            '<path d="M 88,332 Q 146,312 190,298 M 382,160 Q 430,152 472,156 M 632,334 Q 686,324 724,312" '
            'fill="none" stroke="#9AC8EA" stroke-width="1.4" stroke-dasharray="10 6" opacity="0.28"/>'
        )
        # Windshield rain droplets & streaks
        for _ in range(46):
            rx = rng.uniform(54, 906)
            ry = rng.uniform(52, 412)
            rl = rng.uniform(8, 22)
            sahne.append(
                f'<line x1="{rx:.1f}" y1="{ry:.1f}" x2="{rx - rl * 0.25:.1f}" y2="{ry + rl:.1f}" '
                f'stroke="#B8D8F0" stroke-width="1.0" opacity="0.24"/>'
            )
        sahne.append("</g>")
        parts.append("\n".join(sahne))

    # ── LAYER 4: plan (Cyan #7FE6FF ALIAS TRACKER · 3 IDENTITIES HUD & card telemetry) ──
    if _katman_aktif(katmanlar, "plan"):
        plan: list[str] = ['<g id="s402-plan">']
        # Cyan CAD connector lines linking the 3 alias cards
        plan.append(
            f'<path d="M 336,244 L 404,228 M 580,228 L 636,248" fill="none" '
            f'stroke="{PLAN}" stroke-width="1.5" stroke-dasharray="5 4" filter="url(#{p}_glow_cad)"/>'
        )
        for nx, ny, tag in ((216, 152, "ID-01"), (626, 134, "ID-02"), (756, 162, "ID-03")):
            plan.append(
                f'<rect x="{nx - 32}" y="{ny - 11}" width="64" height="19" rx="3" fill="#07131E" '
                f'fill-opacity="0.88" stroke="{PLAN}" stroke-width="1.1"/>'
            )
            plan.append(
                f'<text x="{nx}" y="{ny + 2}" text-anchor="middle" font-family="Consolas, monospace" '
                f'font-size="9.5" font-weight="800" fill="{PLAN_CORE}">{tag}</text>'
            )

        # Hero bottom-right HUD badge: ALIAS TRACKER · 3 IDENTITIES (width 368px -> >=26px padding each side)
        plan.append(
            f'<rect x="564" y="454" width="368" height="60" rx="6" fill="#07111B" fill-opacity="0.92" '
            f'stroke="{PLAN}" stroke-width="1.6"/>'
        )
        plan.append(f'<rect x="576" y="464" width="8" height="40" rx="2" fill="{PLAN}"/>')
        plan.append(
            f'<text x="596" y="480" font-family="Segoe UI, Arial, sans-serif" font-size="10" '
            f'font-weight="700" letter-spacing="1.6" fill="{AMBER_GOLD}">HIGHWAY EVASION · GAG 02</text>'
        )
        plan.append(
            f'<text x="596" y="503" font-family="Segoe UI, Arial, sans-serif" font-size="17" '
            f'font-weight="900" letter-spacing="1.2" fill="{PLAN_CORE}">ALIAS TRACKER · 3 IDENTITIES</text>'
        )
        plan.append("</g>")
        parts.append("\n".join(plan))

    # ── LAYER 5: onplan (Foreground glass droplets, siren reflections & vignette) ──
    if _katman_aktif(katmanlar, "onplan"):
        onplan: list[str] = ['<g id="s402-onplan">']
        for _ in range(18):
            gx = rng.uniform(44, 916)
            gy = rng.uniform(56, 396)
            gr = rng.uniform(1.8, 3.8)
            onplan.append(f'<circle cx="{gx:.1f}" cy="{gy:.1f}" r="{gr:.1f}" fill="#CBE6FF" opacity="0.24"/>')
        # Soft red/blue siren bokeh on top glass edge
        onplan.append(f'<circle cx="442" cy="76" r="30" fill="{SIREN_RED}" opacity="0.10"/>')
        onplan.append(f'<circle cx="518" cy="76" r="30" fill="{SIREN_BLUE}" opacity="0.10"/>')
        onplan.append(f'<rect x="0" y="0" width="960" height="540" fill="url(#{p}_vig)"/>')
        onplan.append(
            f'<path d="M 22,42 L 22,22 L 42,22 M 918,22 L 938,22 L 938,42 '
            f'M 22,498 L 22,518 L 42,518 M 918,518 L 938,518 L 938,498" '
            f'fill="none" stroke="{PLAN}" stroke-width="1.3" opacity="0.45"/>'
        )
        onplan.append("</g>")
        parts.append("\n".join(onplan))

    return defs, "\n".join(parts)


# =============================================================================
# SCENE 4.03: SARA'S CODED ORIGAMI CRANE ("FOLDED CODE")
# =============================================================================
def set_403_sifreli_turna(
    katmanlar: set[str] | list[str] | None = None,
) -> tuple[str, str]:
    """Warm wooden motel table bathed in golden lamp light, half-open brown leather doctor's
    bag, locked Turna v4 (`turna_kapali`, K.turna() centered), unfolded crease-grid paper
    square (`turna_acik` with GILA · NM · 04:00 & dot-matrix cipher lines — live morph target),
    and glowing #7FE6FF CAD cipher coordinates (RENDEZVOUS · GILA NM / FOLDED CODE).
    """
    rng = random.Random(403)
    p = _uid("s403")

    turna_svg = K.turna(s=0.84, isik=0.58, kanat=0.06, kagit="#F7F3EA", golge=True)

    defs = f"""
    <linearGradient id="{p}_room_wall" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#1E1510"/>
      <stop offset="52%" stop-color="#291D15"/>
      <stop offset="100%" stop-color="#140E0A"/>
    </linearGradient>
    <linearGradient id="{p}_wood_table" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#4B2E1B"/>
      <stop offset="38%" stop-color="#3E2515"/>
      <stop offset="100%" stop-color="#26160C"/>
    </linearGradient>
    <radialGradient id="{p}_lamp_pool" cx="0.28" cy="0.34" r="0.64">
      <stop offset="0%" stop-color="#FFE8B0" stop-opacity="0.54"/>
      <stop offset="38%" stop-color="#E8A248" stop-opacity="0.24"/>
      <stop offset="76%" stop-color="#7A4416" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.0"/>
    </radialGradient>
    <linearGradient id="{p}_leather" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#6B3C22"/>
      <stop offset="55%" stop-color="#4D2916"/>
      <stop offset="100%" stop-color="#2E170B"/>
    </linearGradient>
    <linearGradient id="{p}_paper_open" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FBF7EE"/>
      <stop offset="55%" stop-color="#F1E8D5"/>
      <stop offset="100%" stop-color="#DFD2B8"/>
    </linearGradient>
    <radialGradient id="{p}_cad_aura" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0%" stop-color="{PLAN}" stop-opacity="0.24"/>
      <stop offset="60%" stop-color="{PLAN}" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="{PLAN}" stop-opacity="0.0"/>
    </radialGradient>
    <radialGradient id="{p}_vig" cx="0.5" cy="0.5" r="0.74">
      <stop offset="52%" stop-color="#000000" stop-opacity="0.0"/>
      <stop offset="100%" stop-color="#090503" stop-opacity="0.74"/>
    </radialGradient>
    <filter id="{p}_glow_cad" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="2.8" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    """

    parts: list[str] = []

    # ── LAYER 1: uzak (Warm nocturnal motel wall + vintage stripes) ──
    if _katman_aktif(katmanlar, "uzak"):
        uzak: list[str] = ['<g id="s403-uzak">']
        uzak.append(f'<rect x="0" y="0" width="960" height="175" fill="url(#{p}_room_wall)"/>')
        for sx in range(24, 960, 42):
            uzak.append(f'<line x1="{sx}" y1="0" x2="{sx}" y2="175" stroke="#36261B" stroke-width="10" opacity="0.28"/>')
        uzak.append('<rect x="0" y="168" width="960" height="8" fill="#1C120B"/>')
        uzak.append("</g>")
        parts.append("\n".join(uzak))

    # ── LAYER 2: orta (Warm wooden motel table, motel lamp edge & half-open brown leather doctor's bag) ──
    if _katman_aktif(katmanlar, "orta"):
        orta: list[str] = ['<g id="s403-orta">']
        # Wooden motel table surface
        orta.append(f'<rect x="0" y="174" width="960" height="366" fill="url(#{p}_wood_table)"/>')
        # Perspective wood planks & subtle grain
        for py in (226, 286, 354, 430, 506):
            orta.append(f'<line x1="0" y1="{py}" x2="960" y2="{py}" stroke="#23140A" stroke-width="1.8" opacity="0.62"/>')
            orta.append(f'<line x1="0" y1="{py + 2}" x2="960" y2="{py + 2}" stroke="#694228" stroke-width="0.9" opacity="0.32"/>')
        for _ in range(36):
            gx = rng.uniform(20, 900)
            gy = rng.uniform(184, 528)
            gw = rng.uniform(45, 130)
            orta.append(
                f'<path d="M {gx:.1f},{gy:.1f} Q {gx + gw * 0.5:.1f},{gy + rng.uniform(-3, 3):.1f} {gx + gw:.1f},{gy:.1f}" '
                f'fill="none" stroke="#2A170C" stroke-width="1.1" opacity="0.35"/>'
            )

        # Warm golden motel lamp shade & brass stand on upper-left
        orta.append(
            '<ellipse cx="118" cy="250" rx="54" ry="13" fill="#180D06" opacity="0.58"/>'
            '<ellipse cx="118" cy="242" rx="46" ry="12" fill="#9E7334" stroke="#1E1208" stroke-width="1.8"/>'
            '<rect x="110" y="142" width="16" height="100" fill="#B8883E" stroke="#1E1208" stroke-width="1.6"/>'
            '<polygon points="44,148 192,148 168,38 68,38" fill="#DFC391" stroke="#362212" stroke-width="2.2"/>'
            '<ellipse cx="118" cy="148" rx="74" ry="11" fill="#FFF0C4" opacity="0.92"/>'
        )

        # Half-open brown leather doctor's bag on upper-right of table
        orta.append('<g transform="translate(756, 214) rotate(-6)">')
        # Contact shadow
        orta.append('<ellipse cx="6" cy="54" rx="142" ry="26" fill="#120904" opacity="0.62"/>')
        # Back leather body
        orta.append(
            f'<path d="M -124,-18 Q -132,-56 -96,-64 L 96,-64 Q 132,-56 124,-18 L 132,46 Q 132,62 114,62 '
            f'L -114,62 Q -132,62 -132,46 Z" fill="url(#{p}_leather)" stroke="{INK_WARM}" stroke-width="2.4"/>'
        )
        # Half-open dark interior cavity (showing medical contents!)
        orta.append(
            '<path d="M -102,-50 L 102,-50 L 94,-16 L -94,-16 Z" fill="#1A0E08" stroke="#2D180D" stroke-width="1.6"/>'
        )
        # White folded prescription/medical pad + stethoscope peeking out of half-open mouth
        orta.append(
            '<polygon points="-74,-46 -12,-48 -18,-18 -78,-18" fill="#EFEAE0" stroke="#2B241E" stroke-width="1.2"/>'
            '<line x1="-66" y1="-36" x2="-26" y2="-36" stroke="#7A8E9E" stroke-width="1.2"/>'
            '<line x1="-68" y1="-28" x2="-34" y2="-28" stroke="#7A8E9E" stroke-width="1.2"/>'
        )
        # Stethoscope tube draping subtly over bag rim
        orta.append(
            '<path d="M 18,-44 C 36,-72 68,-64 74,-34 C 78,-16 62,-4 46,4" fill="none" '
            'stroke="#232930" stroke-width="5.2" stroke-linecap="round"/>'
            '<circle cx="44" cy="6" r="8.5" fill="#C4CCD4" stroke="#1E242B" stroke-width="1.8"/>'
            '<circle cx="44" cy="6" r="3.2" fill="#475360"/>'
        )
        # Front leather flap & brass clasp frame
        orta.append(
            f'<path d="M -124,-14 L 124,-14 L 130,46 Q 130,60 112,60 L -112,60 Q -130,60 -130,46 Z" '
            f'fill="url(#{p}_leather)" stroke="{INK_WARM}" stroke-width="2.2"/>'
        )
        # Brass hinge bar + center clasp
        orta.append('<rect x="-106" y="-20" width="212" height="8" rx="3" fill="#C99B48" stroke="#2B1C0A" stroke-width="1.4"/>')
        orta.append('<rect x="-14" y="-24" width="28" height="22" rx="3" fill="#E6BC66" stroke="#2B1C0A" stroke-width="1.5"/>')
        orta.append('<circle cx="0" cy="-12" r="3.4" fill="#3B250C"/>')
        # Leather handle arched above bag
        orta.append(
            '<path d="M -52,-64 C -52,-98 52,-98 52,-64" fill="none" stroke="#1A0E08" stroke-width="11" stroke-linecap="round"/>'
            '<path d="M -52,-64 C -52,-98 52,-98 52,-64" fill="none" stroke="#5E331B" stroke-width="7.2" stroke-linecap="round"/>'
        )
        # Stitch detail along front leather face
        orta.append(
            '<path d="M -112,-2 L -116,48 L 116,48 L 112,-2" fill="none" stroke="#8C5938" '
            'stroke-width="1.2" stroke-dasharray="5 4" opacity="0.65"/>'
        )
        orta.append("</g>")

        # Warm golden lamp light pool across entire table
        orta.append(f'<rect x="0" y="0" width="960" height="540" fill="url(#{p}_lamp_pool)"/>')
        orta.append("</g>")
        parts.append("\n".join(orta))

    # ── LAYER 3A: turna_acik (Independently animatable unfolded origami paper square + GILA · NM · 04:00 + dot-matrix cipher) ──
    if _katman_aktif(katmanlar, "turna_acik"):
        acik: list[str] = ['<g id="s403-turna_acik">']
        # Centered at (480, 326) so it shares the hero table focus with turna_kapali
        acik.append('<g transform="translate(480, 326)">')
        # Soft table drop shadow under unfolded square
        acik.append('<rect x="-132" y="-122" width="272" height="252" rx="3" fill="#120904" opacity="0.46"/>')
        # Unfolded origami paper square
        acik.append(
            f'<rect x="-136" y="-126" width="272" height="252" rx="2" fill="url(#{p}_paper_open)" '
            f'stroke="#5E4D3B" stroke-width="1.8"/>'
        )
        # Authentic origami crease lines (diagonals, horizontal/vertical medians, bird-base diamond creases)
        creases = [
            "M -136,-126 L 136,126",
            "M 136,-126 L -136,126",
            "M 0,-126 L 0,126",
            "M -136,0 L 136,0",
            "M 0,-126 L 136,0 L 0,126 L -136,0 Z",
            "M -68,-126 L 136,68",
            "M 68,-126 L -136,68",
        ]
        for cd in creases:
            acik.append(f'<path d="{cd}" fill="none" stroke="#B6A387" stroke-width="1.15" opacity="0.72"/>')

        # Dot-matrix cipher lines & pinhole nodes across the unfolded sheet
        dot_nodes = [
            (-96, -86), (-44, -86), (44, -86), (96, -86),
            (-96, -28), (96, -28),
            (-96, 36), (-44, 36), (44, 36), (96, 36),
        ]
        acik.append(
            '<path d="M -96,-86 L -44,-86 L 44,36 L 96,36 M -96,36 L -44,36 L 44,-86 L 96,-86" '
            'fill="none" stroke="#366E85" stroke-width="1.4" stroke-dasharray="3 4" opacity="0.75"/>'
        )
        for dx, dy in dot_nodes:
            acik.append(f'<circle cx="{dx}" cy="{dy}" r="3.2" fill="#2A4C5E" opacity="0.82"/>')
            acik.append(f'<circle cx="{dx}" cy="{dy}" r="1.2" fill="#7FE6FF" opacity="0.9"/>')

        # Decoded rendezvous coordinates clearly stamped on the lower crease band (generous >=18px padding)
        acik.append(
            '<rect x="-122" y="64" width="244" height="46" rx="3" fill="#EAE0CA" fill-opacity="0.92" '
            'stroke="#6F5E48" stroke-width="1.2"/>'
        )
        acik.append(
            '<text x="0" y="84" text-anchor="middle" font-family="Consolas, monospace" '
            'font-size="14.5" font-weight="900" letter-spacing="1.6" fill="#1E2832">GILA · NM · 04:00</text>'
        )
        acik.append(
            '<text x="0" y="101" text-anchor="middle" font-family="Consolas, monospace" '
            'font-size="8.2" font-weight="700" letter-spacing="0.6" fill="#32596E">CIPHER · 32°58\'N 108°35\'W</text>'
        )
        acik.append("</g>")
        acik.append("</g>")
        parts.append("\n".join(acik))

    # ── LAYER 3B: turna_kapali (Independently animatable locked Turna v4 K.turna() centered on table) ──
    if _katman_aktif(katmanlar, "turna_kapali"):
        kapali: list[str] = ['<g id="s403-turna_kapali">']
        # Centered hero placement at (480, 268) so Turna v4 sits cleanly above the unfolded cipher band
        kapali.append('<g transform="translate(480, 268)">')
        kapali.append(turna_svg)
        kapali.append("</g>")
        kapali.append("</g>")
        parts.append("\n".join(kapali))

    # ── LAYER 3C: sahne (Tabletop storytelling props: brass pen & Motel Room 14 key tag) ──
    if _katman_aktif(katmanlar, "sahne"):
        sahne: list[str] = ['<g id="s403-sahne">']
        # Vintage green plastic diamond motel key fob + brass key on lower-left table
        sahne.append('<g transform="translate(186, 408) rotate(-22)">')
        sahne.append('<polygon points="-44,0 0,-22 44,0 0,22" fill="#1C5440" stroke="#0F261E" stroke-width="1.8"/>')
        sahne.append('<polygon points="-36,0 0,-16 36,0 0,16" fill="none" stroke="#D9B05B" stroke-width="1.0" opacity="0.8"/>')
        sahne.append(
            '<text x="0" y="3.5" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif" '
            'font-size="9" font-weight="800" letter-spacing="0.8" fill="#F2E4C4">RM 14</text>'
        )
        # Brass motel key ring & blade
        sahne.append('<circle cx="48" cy="0" r="6.5" fill="none" stroke="#C8CFD6" stroke-width="2.0"/>')
        sahne.append(
            '<path d="M 55,-3 L 86,-3 L 86,2 L 80,2 L 80,6 L 75,6 L 75,2 L 68,2 L 68,5 L 63,5 L 63,2 L 55,2 Z" '
            'fill="#D9A84A" stroke="#2A1C0A" stroke-width="1.2"/>'
        )
        sahne.append("</g>")
        # Sleek metallic pen resting on right side of table
        sahne.append('<g transform="translate(744, 386) rotate(18)">')
        sahne.append('<rect x="-64" y="-3.5" width="122" height="7" rx="3" fill="#232B34" stroke="#0F1318" stroke-width="1.4"/>')
        sahne.append('<polygon points="58,-3.5 74,0 58,3.5" fill="#D4C29A" stroke="#0F1318" stroke-width="1.2"/>')
        sahne.append('<rect x="-42" y="-3.5" width="8" height="7" fill="#D9B05B"/>')
        sahne.append("</g>")
        sahne.append("</g>")
        parts.append("\n".join(sahne))

    # ── LAYER 4: plan (Glowing #7FE6FF cipher coordinates, dot-matrix projection & FOLDED CODE / RENDEZVOUS HUD) ──
    if _katman_aktif(katmanlar, "plan"):
        plan: list[str] = ['<g id="s403-plan">']
        # Soft cyan cipher aura around the crane / unfolded sheet
        plan.append(f'<ellipse cx="480" cy="306" rx="220" ry="145" fill="url(#{p}_cad_aura)"/>')
        # Glowing cyan cipher projection ring & vector brackets
        plan.append(
            f'<circle cx="480" cy="296" r="154" fill="none" stroke="{PLAN}" stroke-width="1.2" '
            f'stroke-dasharray="6 6" opacity="0.62"/>'
        )
        # Floating cyan coordinate callouts connected to paper corners
        plan.append(
            f'<path d="M 384,240 L 296,204 L 222,204" fill="none" stroke="{PLAN}" stroke-width="1.4" '
            f'filter="url(#{p}_glow_cad)"/>'
        )
        plan.append(
            f'<rect x="78" y="191" width="146" height="24" rx="4" fill="#07131E" fill-opacity="0.90" '
            f'stroke="{PLAN}" stroke-width="1.2"/>'
        )
        plan.append(
            f'<text x="151" y="207" text-anchor="middle" font-family="Consolas, monospace" '
            f'font-size="10" font-weight="800" fill="{PLAN_CORE}">32.97°N · 108.58°W</text>'
        )

        # Right-side cyan cipher callout
        plan.append(
            f'<path d="M 576,362 L 664,334 L 708,334" fill="none" stroke="{PLAN}" stroke-width="1.4" '
            f'filter="url(#{p}_glow_cad)"/>'
        )
        plan.append(
            f'<rect x="708" y="320" width="166" height="26" rx="4" fill="#07131E" fill-opacity="0.90" '
            f'stroke="{PLAN}" stroke-width="1.2"/>'
        )
        plan.append(
            f'<text x="791" y="337" text-anchor="middle" font-family="Consolas, monospace" '
            f'font-size="10.5" font-weight="800" fill="{PLAN_CORE}">GILA · NM · 04:00</text>'
        )

        # Top-left Hero HUD badge: FOLDED CODE (width 256px -> >=22px padding each side)
        plan.append(
            f'<rect x="26" y="24" width="256" height="60" rx="6" fill="#08121C" fill-opacity="0.90" '
            f'stroke="{PLAN}" stroke-width="1.6"/>'
        )
        plan.append(f'<rect x="38" y="34" width="8" height="40" rx="2" fill="{PLAN}"/>')
        plan.append(
            f'<text x="58" y="50" font-family="Segoe UI, Arial, sans-serif" font-size="10" '
            f'font-weight="700" letter-spacing="1.6" fill="{AMBER_GOLD}">SARA · ORIGAMI CIPHER</text>'
        )
        plan.append(
            f'<text x="58" y="73" font-family="Segoe UI, Arial, sans-serif" font-size="19" '
            f'font-weight="900" letter-spacing="1.8" fill="{PLAN_CORE}">FOLDED CODE</text>'
        )

        # Bottom-right Hero HUD badge: RENDEZVOUS · GILA NM (width 308px -> >=22px padding each side)
        plan.append(
            f'<rect x="626" y="454" width="308" height="58" rx="6" fill="#08121C" fill-opacity="0.90" '
            f'stroke="{PLAN}" stroke-width="1.6"/>'
        )
        plan.append(f'<rect x="638" y="464" width="8" height="38" rx="2" fill="{AMBER_GOLD}"/>')
        plan.append(
            f'<text x="658" y="479" font-family="Segoe UI, Arial, sans-serif" font-size="9.5" '
            f'font-weight="700" letter-spacing="1.5" fill="{PLAN}">DECODED COORDINATES</text>'
        )
        plan.append(
            f'<text x="658" y="501" font-family="Segoe UI, Arial, sans-serif" font-size="17" '
            f'font-weight="900" letter-spacing="1.2" fill="{PLAN_CORE}">RENDEZVOUS · GILA NM</text>'
        )
        plan.append("</g>")
        parts.append("\n".join(plan))

    # ── LAYER 5: onplan (Warm lamp dust motes, vignette & viewfinder corners) ──
    if _katman_aktif(katmanlar, "onplan"):
        onplan: list[str] = ['<g id="s403-onplan">']
        for _ in range(28):
            mx = rng.uniform(60, 620)
            my = rng.uniform(80, 480)
            mr = rng.uniform(0.9, 2.3)
            op = rng.uniform(0.24, 0.64)
            col = AMBER_HOT if rng.random() > 0.35 else PLAN_CORE
            onplan.append(f'<circle cx="{mx:.1f}" cy="{my:.1f}" r="{mr:.1f}" fill="{col}" opacity="{op:.2f}"/>')
        onplan.append(f'<rect x="0" y="0" width="960" height="540" fill="url(#{p}_vig)"/>')
        onplan.append(
            f'<path d="M 22,42 L 22,22 L 42,22 M 918,22 L 938,22 L 938,42 '
            f'M 22,498 L 22,518 L 42,518 M 918,518 L 938,518 L 938,498" '
            f'fill="none" stroke="{PLAN}" stroke-width="1.3" opacity="0.45"/>'
        )
        onplan.append("</g>")
        parts.append("\n".join(onplan))

    return defs, "\n".join(parts)


# =============================================================================
# RENDERING & CARD GENERATION (1280x720 SET CARD + 1280x720 R13 200% CROP CARD)
# =============================================================================
def _render_scene_png(scene_fn, scale: int = 2, katmanlar: set[str] | list[str] | None = None) -> Image.Image:
    defs, body = scene_fn(katmanlar=katmanlar)
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{W_SCENE * scale}" height="{H_SCENE * scale}" '
        f'viewBox="0 0 {W_SCENE} {H_SCENE}">'
        f"<defs>{defs}</defs>"
        f"{body}"
        f"</svg>"
    )
    png_bytes = resvg_py.svg_to_bytes(svg_string=svg)
    return Image.open(io.BytesIO(png_bytes)).convert("RGBA")


def _font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = (
        ["C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf"]
        if bold
        else ["C:/Windows/Fonts/segoeui.ttf", "C:/Windows/Fonts/arial.ttf"]
    )
    for fp in candidates:
        if Path(fp).exists():
            return ImageFont.truetype(fp, size)
    return ImageFont.load_default()


def _draw_card_bg(w: int, h: int) -> Image.Image:
    img = Image.new("RGBA", (w, h), "#0B111A")
    draw = ImageDraw.Draw(img)
    for x in range(0, w, 32):
        draw.line((x, 0, x, h), fill="#121C29", width=1)
    for y in range(0, h, 32):
        draw.line((0, y, w, y), fill="#121C29", width=1)
    return img


def _draw_panel_box(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int]) -> None:
    draw.rounded_rectangle(box, radius=10, fill="#0F1824", outline="#24374C", width=1)


def _draw_swatches(draw: ImageDraw.ImageDraw, x: int, y: int, colors: list[str], size: int = 16, gap: int = 5) -> None:
    for i, c in enumerate(colors):
        sx = x + i * (size + gap)
        draw.rounded_rectangle((sx, y, sx + size, y + size), radius=3, fill=c, outline="#3B5168", width=1)


def uret_kartlar(versiyon: str = "v1") -> tuple[Path, Path]:
    img_401 = _render_scene_png(set_401_fbi_masasi, scale=2)     # 1920x1080
    img_402 = _render_scene_png(set_402_otoyol_kimlik, scale=2)
    img_403 = _render_scene_png(set_403_sifreli_turna, scale=2)
    img_403_acik = _render_scene_png(
        set_403_sifreli_turna,
        scale=2,
        katmanlar={"uzak", "orta", "turna_acik", "sahne", "plan", "onplan"},
    )

    f_title = _font(19, bold=True)
    f_sub = _font(11, bold=False)
    f_card_t = _font(12, bold=True)
    f_card_s = _font(10, bold=False)
    f_small = _font(9, bold=True)

    # =========================================================================
    # OUTPUT 1: 3-SCENE ACT IV SET CARD (1280 x 720, 100% ENGLISH)
    # =========================================================================
    canvas = _draw_card_bg(1280, 720)
    draw = ImageDraw.Draw(canvas)

    draw.text((24, 12), "MICHAEL SCOFIELD · ACT IV FBI DESK, FAKE ALIASES & CODED ORIGAMI CRANE", fill="#EBF3FA", font=f_title)
    draw.text(
        (24, 36),
        "STYLE B+A HYBRID (CINEMATIC 2D + CYAN BLUEPRINT VISION)  ·  SCENES 4.01 – 4.03  ·  R18-HAREKET LIVE LAYERS  ·  R4-PARALLAX LOCKED",
        fill="#7E97B0",
        font=f_sub,
    )
    top_chips = [("FBI LAMP", "#F5C26B"), ("ALERT", "#E63244"), ("HIGHWAY", "#1B2C40"), ("ORIGAMI", "#F7F3EA"), ("CAD", "#7FE6FF")]
    cx = 872
    for lbl, col in top_chips:
        draw.rounded_rectangle((cx, 16, cx + 14, 30), radius=3, fill=col, outline="#3B5168", width=1)
        draw.text((cx + 18, 17), lbl, fill="#9DB3C9", font=f_small)
        cx += 78
    draw.line((24, 54, 1256, 54), fill="#213247", width=1)

    # Top row: 2 panels (4.01 & 4.02); Bottom row: full-width showcase for 4.03 (Folded + Unfolded morph preview!)
    top_panels = [
        (
            (22, 64, 632, 378),
            img_401,
            "01 · 4.01 MAHONE'S FBI DESK & TATTOO WALL",
            "\"ANOTHER MIND\"",
            "#FF6B78",
            ["#1D4B3A", "#F5C26B", "#E63244", "#EFE6D2", "#7FE6FF"],
            [
                "• A2 continuity: 3.10 lamp",
                "• Locked A-Sirt v1 (0.55)",
                "• US map: UTAH/NM/PANAMA",
                "• Live red string & FBI hand",
                "• Cyan->Red DECODING CAD",
            ],
            "Emerald brass desk lamp",
            "uzak/orta/sahne/kirmizi_ip/harita_igne/plan/onplan",
        ),
        (
            (646, 64, 1256, 378),
            img_402,
            "02 · 4.02 NIGHT HIGHWAY & FAKE ALIASES",
            "Gag 2 · \"NEW NAME.\"",
            "#7FE6FF",
            ["#0D192B", "#F6C945", "#FF2E48", "#2E8CFF", "#7FE6FF"],
            [
                "• Wet windshield & sirens",
                "• kart_1: MICHAEL CRANE",
                "• Locked K.michael_kafa",
                "• kart_2: E.F.G. PASSPORT",
                "• kart_3: NEW NAME. stamp",
            ],
            "Headlights + mirror sirens",
            "uzak/orta/kart_1/kart_2/kart_3/sahne/plan/onplan",
        ),
    ]

    for box, src, title, sub, tcol, pal, elems, light, lyrs in top_panels:
        x0, y0, x1, y1 = box
        _draw_panel_box(draw, box)
        thumb = src.resize((424, 238), Image.Resampling.LANCZOS)
        canvas.paste(thumb, (x0 + 10, y0 + 34), thumb)
        draw.rectangle((x0 + 10, y0 + 34, x0 + 10 + 424, y0 + 34 + 238), outline="#2E455E", width=1)
        draw.text((x0 + 10, y0 + 10), title, fill=tcol, font=f_card_t)
        draw.text((x0 + 318, y0 + 12), sub, fill="#8AA3BC", font=f_card_s)

        ix = x0 + 444
        draw.text((ix, y0 + 34), "PALETTE", fill="#7FE6FF", font=f_small)
        _draw_swatches(draw, ix, y0 + 49, pal, size=16, gap=5)
        draw.text((ix, y0 + 76), "KEY ELEMENTS", fill="#9BB2C8", font=f_small)
        for idx, item in enumerate(elems):
            draw.text((ix, y0 + 92 + idx * 19), item, fill="#D5E2EE", font=f_card_s)
        draw.text((ix, y0 + 196), "KEY LIGHTING", fill="#9BB2C8", font=f_small)
        draw.text((ix, y0 + 210), light, fill="#F6C367", font=f_card_s)
        draw.text((ix, y0 + 234), "R18 LIVE LAYERS", fill="#9BB2C8", font=f_small)
        draw.text((ix, y0 + 248), "Individually\nanimatable", fill="#8AA3BC", font=f_small)
        draw.text((x0 + 10, y0 + 282), f"LAYERS: {lyrs}", fill="#6E87A0", font=f_small)

    # Bottom wide panel: 4.03 Coded Origami Crane (Composite + Unfolded Morph Target side-by-side)
    b403 = (22, 390, 1256, 704)
    _draw_panel_box(draw, b403)
    draw.text((34, 400), "03 · 4.03 SARA'S CODED ORIGAMI CRANE  (\"FOLDED CODE\" · RENDEZVOUS GILA NM)", fill="#F5C26B", font=f_card_t)
    draw.text((716, 402), "R18 MORPH: turna_kapali (Turna v4)  ->  turna_acik (GILA · NM · 04:00)", fill="#7FE6FF", font=f_card_s)

    t403_full = img_403.resize((424, 238), Image.Resampling.LANCZOS)
    t403_open = img_403_acik.resize((424, 238), Image.Resampling.LANCZOS)
    canvas.paste(t403_full, (34, 424), t403_full)
    draw.rectangle((34, 424, 458, 662), outline="#2E455E", width=1)
    canvas.paste(t403_open, (474, 424), t403_open)
    draw.rectangle((474, 424, 898, 662), outline="#2E455E", width=1)

    ix3 = 918
    draw.text((ix3, 424), "PALETTE", fill="#7FE6FF", font=f_small)
    _draw_swatches(draw, ix3, 439, ["#3E2515", "#6B3C22", "#FFE8B0", "#F7F3EA", "#7FE6FF"], size=16, gap=6)
    draw.text((ix3, 468), "KEY ELEMENTS (4.03)", fill="#9BB2C8", font=f_small)
    elems_403 = [
        "• Warm wooden motel table + lamp",
        "• Half-open brown leather doctor bag",
        "• turna_kapali: Locked Turna v4",
        "• turna_acik: Creased cipher square",
        "• GILA · NM · 04:00 dot-matrix code",
        "• #7FE6FF RENDEZVOUS · GILA NM",
    ]
    for idx, item in enumerate(elems_403):
        draw.text((ix3, 485 + idx * 20), item, fill="#D5E2EE", font=f_card_s)
    draw.text((ix3, 614), "KEY LIGHTING: Warm motel lamp + Cyan CAD", fill="#F6C367", font=f_card_s)
    draw.text((ix3, 634), "LAYERS (7): uzak · orta · turna_acik", fill="#8AA3BC", font=f_small)
    draw.text((ix3, 648), "turna_kapali · sahne · plan · onplan", fill="#8AA3BC", font=f_small)
    draw.text((34, 672), "LEFT: Composite (katmanlar=None)  ·  CENTER: Unfolded Cipher Layer (turna_acik)  ·  RIGHT: Spec & Palette", fill="#6E87A0", font=f_small)

    out_main = OUT_DIR / f"b4_set_takip_turna_{versiyon}.png"
    canvas.convert("RGB").save(out_main, quality=95)

    # =========================================================================
    # OUTPUT 2: R13 200% ZOOM QUALITY CONTROL CARD (1280 x 720 — 4 PANELS)
    # =========================================================================
    r13 = _draw_card_bg(1280, 720)
    d13 = ImageDraw.Draw(r13)
    d13.text((24, 12), "R13 · 200% ZOOM QUALITY CONTROL (ACT IV FBI DESK, FAKE ALIASES & CODED CRANE)", fill="#EBF3FA", font=f_title)
    d13.text(
        (24, 36),
        "1:1 PIXEL CROPS FROM 1920×1080 SOURCE  ·  A-SIRT v1, K.MICHAEL_KAFA COLLAR-OVER-NECK, TURNA v4 & ZERO-OVERFLOW HUD",
        fill="#7E97B0",
        font=f_sub,
    )
    d13.line((24, 54, 1256, 54), fill="#213247", width=1)

    cw, ch = 600, 264
    crops = [
        (
            img_401,
            (570, 355),
            "1 · 4.01 LOCKED A-SIRT v1 POLAROID & RED STRINGS (200%)",
            "K.michael_sirt_dovme(0.55) Exhibit #94941 + ANOTHER MIND HUD & cyan-red CAD",
            (22, 64),
        ),
        (
            img_401,
            (1310, 355),
            "2 · 4.01 FBI HAND PINNING UTAH ON US MAP (200%)",
            "Single R4 layer harita_igne + UTAH / NEW MEXICO / PANAMA & red pushpin ring",
            (652, 64),
        ),
        (
            img_402,
            (440, 530),
            "3 · 4.02 MICHAEL CRANE ID (K.MICHAEL_KAFA) & NEW NAME (200%)",
            "Locked front/odak head with clean Collar-Over-Neck + crisp Driver License typography",
            (22, 392),
        ),
        (
            img_403,
            (960, 555),
            "4 · 4.03 LOCKED TURNA v4 & GILA · NM · 04:00 CIPHER (200%)",
            "K.turna() centered over unfolded crease-grid paper & dot-matrix cipher coordinates",
            (652, 392),
        ),
    ]

    for src_img, (cx0, cy0), title, sub, (bx, by) in crops:
        _draw_panel_box(d13, (bx, by, bx + 606, by + 314))
        x0 = max(0, min(src_img.width - cw, cx0 - cw // 2))
        y0 = max(0, min(src_img.height - ch, cy0 - ch // 2))
        patch = src_img.crop((x0, y0, x0 + cw, y0 + ch))
        r13.paste(patch, (bx + 3, by + 44), patch)
        d13.rectangle((bx + 3, by + 44, bx + 3 + cw, by + 44 + ch), outline="#2F465E", width=1)
        d13.text((bx + 12, by + 8), title, fill="#7FE6FF", font=f_card_t)
        d13.text((bx + 12, by + 25), sub, fill="#96AEC6", font=f_small)

    out_r13 = OUT_DIR / "b4_set_takip_turna_r13.png"
    r13.convert("RGB").save(out_r13, quality=95)
    print(f"Saved:\n  - {out_main}\n  - {out_r13}")
    return out_main, out_r13


if __name__ == "__main__":
    uret_kartlar("v1")
