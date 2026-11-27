"""V7 (Act III — Visiting Glass, Yard Crew Cards & Warm Infirmary Scene Artist) — Style B + A Hybrid.

Isolated, side-effect-free module producing 3 richly detailed, 5-layer (960x540) cinematic 2D sets:
  - set_301_ziyaret_cami(katmanlar=None) -> (defs_svg, body_svg)  [Visiting Glass · GETTING YOU OUT / DAYS LEFT: 29]
  - set_302_ekip_kartlari(katmanlar=None) -> (defs_svg, body_svg) [Yard Crew Cards · LONG STORY.]
  - set_303_revir_sara(katmanlar=None)   -> (defs_svg, body_svg)  [Warm Infirmary & Sara · DAYS LEFT: 21]

Each scene uses 5 named <g> depth layers: uzak, orta, sahne, plan, onplan.
R4-PARALAKS COMPLIANCE: Every character's complete anatomy (head, neck, torso, arms, hands)
and any directly contacted prop live strictly inside the single `sahne` layer.
Locked character assets imported read-only from karakter.py:
  - K.michael_kafa(...)  [Michael v3]
  - K.lincoln_kafa(...)  [Lincoln v1]
  - K.sara_kafa(...)     [Sara v2]
All on-screen text and presentation cards are 100% ENGLISH.
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

INK = "#161414"
INK_WARM = "#211610"
PLAN = "#7FE6FF"
PLAN_CORE = "#E0FBFF"

_UID = 0


def _uid(prefix: str = "b3") -> str:
    global _UID
    _UID += 1
    return f"{prefix}_{_UID}"


def _katman_aktif(katmanlar: set[str] | list[str] | None, ad: str) -> bool:
    return katmanlar is None or ad in katmanlar


def _hud_days_left(x: float, y: float, days: int) -> str:
    """Clean Style B+A cyan CAD countdown badge in top-right corner."""
    return (
        f'<g id="hud-days-{days}">'
        f'<rect x="{x:.1f}" y="{y:.1f}" width="188" height="38" rx="3" fill="#08131E" opacity="0.90" stroke="{PLAN}" stroke-width="1.5"/>'
        f'<path d="M{x+6:.1f},{y+5:.1f} L{x+16:.1f},{y+5:.1f} M{x+172:.1f},{y+33:.1f} L{x+182:.1f},{y+33:.1f}" '
        f'fill="none" stroke="{PLAN}" stroke-width="1.3" opacity="0.82"/>'
        f'<circle cx="{x+15:.1f}" cy="{y+19:.1f}" r="3.6" fill="{PLAN_CORE}"/>'
        f'<text x="{x+28:.1f}" y="{y+24.5:.1f}" font-family="DejaVu Sans Mono, monospace" '
        f'font-size="15.2" font-weight="bold" fill="{PLAN_CORE}" letter-spacing="1.0">DAYS LEFT: {days}</text>'
        f'</g>'
    )


# =============================================================================
# 3.01 · VISITING GLASS ("GETTING YOU OUT" / "DAYS LEFT: 29")
# =============================================================================
def set_301_ziyaret_cami(katmanlar: set[str] | list[str] | None = None) -> tuple[str, str]:
    """Scratched prison visiting glass & perforated metal speaker grille; cold
    overhead fluorescent tubes vs. warm reflection; foreground-left locked
    Michael v3 parting his Fox River blue shirt to reveal glowing #7FE6FF
    original architectural blueprint tattoo on chest & forearm; behind the glass,
    locked Lincoln v1 pressing his tattoo-free palm (R3!) against the pane.
    R4-PARALAKS: Both Lincoln + glass + Michael live inside `sahne`."""
    rng = random.Random(301)
    p = _uid("s301")

    defs = f"""
    <linearGradient id="{p}_bg_wall" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#0E1722"/>
      <stop offset="42%" stop-color="#192836"/>
      <stop offset="100%" stop-color="#101A24"/>
    </linearGradient>
    <linearGradient id="{p}_fluor_cone" x1="0.5" y1="0" x2="0.5" y2="1">
      <stop offset="0%" stop-color="#DDF6FF" stop-opacity="0.34"/>
      <stop offset="52%" stop-color="#86C5E6" stop-opacity="0.12"/>
      <stop offset="100%" stop-color="#4A89B0" stop-opacity="0.0"/>
    </linearGradient>
    <linearGradient id="{p}_glass_tint" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#A6D9EE" stop-opacity="0.16"/>
      <stop offset="38%" stop-color="#E6F8FF" stop-opacity="0.07"/>
      <stop offset="72%" stop-color="#F2B86B" stop-opacity="0.13"/>
      <stop offset="100%" stop-color="#76B0CC" stop-opacity="0.18"/>
    </linearGradient>
    <linearGradient id="{p}_warm_refl" x1="0" y1="0" x2="1" y2="0.4">
      <stop offset="0%" stop-color="#FFCA7A" stop-opacity="0.0"/>
      <stop offset="48%" stop-color="#FFCA7A" stop-opacity="0.22"/>
      <stop offset="100%" stop-color="#FFCA7A" stop-opacity="0.0"/>
    </linearGradient>
    <linearGradient id="{p}_metal_frame" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#27313C"/>
      <stop offset="45%" stop-color="#465564"/>
      <stop offset="100%" stop-color="#1E262F"/>
    </linearGradient>
    <linearGradient id="{p}_counter" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#4A5866"/>
      <stop offset="35%" stop-color="#313C47"/>
      <stop offset="100%" stop-color="#1B222A"/>
    </linearGradient>
    <linearGradient id="{p}_shirt_m" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#7899BA"/>
      <stop offset="45%" stop-color="#5E7E9F"/>
      <stop offset="100%" stop-color="#3C546E"/>
    </linearGradient>
    <linearGradient id="{p}_shirt_l" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#6A89A8"/>
      <stop offset="55%" stop-color="#4B6885"/>
      <stop offset="100%" stop-color="#2E445A"/>
    </linearGradient>
    <radialGradient id="{p}_tat_glow" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0%" stop-color="#7FE6FF" stop-opacity="0.48"/>
      <stop offset="55%" stop-color="#34A8D8" stop-opacity="0.16"/>
      <stop offset="100%" stop-color="#1B6A94" stop-opacity="0.0"/>
    </radialGradient>
    <radialGradient id="{p}_vignette" cx="0.50" cy="0.48" r="0.70">
      <stop offset="48%" stop-color="#000000" stop-opacity="0.0"/>
      <stop offset="100%" stop-color="#060A10" stop-opacity="0.72"/>
    </radialGradient>
    <filter id="{p}_glow_cyan" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="2.6" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="{p}_blur_soft" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="5.0" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    """

    parts: list[str] = []

    # -------------------------------------------------------------------------
    # LAYER 1: UZAK (Cold prison visiting hall back wall, cinderblock courses,
    # fluorescent tubes, security door & adjacent empty booth silhouettes)
    # -------------------------------------------------------------------------
    if _katman_aktif(katmanlar, "uzak"):
        u: list[str] = ['<g id="s301-uzak">']
        u.append(f'<rect x="0" y="0" width="960" height="540" fill="url(#{p}_bg_wall)"/>')

        # Cinderblock horizontal & staggered vertical courses on far visiting wall
        for by in range(44, 380, 28):
            u.append(f'<path d="M0,{by} L960,{by}" fill="none" stroke="#0C141D" stroke-width="1.0" opacity="0.55"/>')
            offset = 32 if (by // 28) % 2 else 0
            for bx in range(offset, 960, 64):
                u.append(f'<path d="M{bx},{by} L{bx},{by+28}" fill="none" stroke="#0C141D" stroke-width="0.9" opacity="0.42"/>')

        # Institutional paint stripe along mid wall
        u.append('<rect x="0" y="246" width="960" height="16" fill="#2A3F52" opacity="0.55"/>')
        u.append('<path d="M0,246 L960,246 M0,262 L960,262" fill="none" stroke="#5E85A3" stroke-width="1.0" opacity="0.35"/>')

        # Steel security door on far back-left with barred window
        u.append(f'<rect x="66" y="102" width="118" height="248" fill="#182430" stroke="{INK}" stroke-width="1.6"/>')
        u.append(f'<rect x="92" y="128" width="66" height="54" fill="#294359" stroke="{INK}" stroke-width="1.4"/>')
        for gx in (108, 125, 142):
            u.append(f'<path d="M{gx},128 L{gx},182" fill="none" stroke="#131B24" stroke-width="2.4"/>')
        u.append('<text x="125" y="92" text-anchor="middle" font-family="DejaVu Sans Mono, monospace" font-size="8.5" font-weight="bold" fill="#7D9FB8" opacity="0.72">CELLBLOCK VISITING · BAY 4</text>')

        # Adjacent empty visiting booth partition on far right
        u.append(f'<rect x="816" y="70" width="144" height="310" fill="#131E29" stroke="{INK}" stroke-width="1.6"/>')
        u.append('<rect x="836" y="114" width="106" height="168" fill="#1E3142" opacity="0.65" stroke="#2D465C" stroke-width="1.2"/>')

        # Overhead cold fluorescent ceiling fixtures casting cool cones
        for fx_t in (240, 620):
            u.append(f'<rect x="{fx_t-74}" y="14" width="148" height="12" rx="2" fill="#273442" stroke="{INK}" stroke-width="1.4"/>')
            u.append(f'<rect x="{fx_t-66}" y="22" width="132" height="6" rx="2" fill="#E8FAFF"/>')
            u.append(f'<polygon points="{fx_t-66},28 {fx_t+66},28 {fx_t+158},360 {fx_t-158},360" fill="url(#{p}_fluor_cone)"/>')

        # Warm amber hallway exit bulb glow on far left (warm vs. cold contrast)
        u.append(f'<circle cx="44" cy="146" r="76" fill="#F2A94E" opacity="0.20" filter="url(#{p}_blur_soft)"/>')
        u.append('</g>')
        parts.append("".join(u))

    # -------------------------------------------------------------------------
    # LAYER 2: ORTA (Architectural booth steel dividers, rear visiting counter
    # & wall-mounted visitor telephone cradle — NO characters here per R4!)
    # -------------------------------------------------------------------------
    if _katman_aktif(katmanlar, "orta"):
        m: list[str] = ['<g id="s301-orta">']
        # Rear inmate-side steel counter shelf
        m.append(f'<rect x="346" y="376" width="540" height="44" fill="#232E38" stroke="{INK}" stroke-width="1.8"/>')
        m.append('<path d="M350,379 L882,379" fill="none" stroke="#89B8D4" stroke-width="1.4" opacity="0.45"/>')

        # Heavy bolted steel booth partition mullions framing the glass bay
        m.append(f'<rect x="340" y="34" width="22" height="456" fill="url(#{p}_metal_frame)" stroke="{INK}" stroke-width="2.0"/>')
        m.append(f'<rect x="854" y="34" width="24" height="456" fill="url(#{p}_metal_frame)" stroke="{INK}" stroke-width="2.0"/>')
        m.append(f'<rect x="340" y="30" width="538" height="24" fill="url(#{p}_metal_frame)" stroke="{INK}" stroke-width="2.0"/>')
        # Steel rivets along frame
        for ry in range(66, 440, 56):
            m.append(f'<circle cx="351" cy="{ry}" r="2.8" fill="#6F8496" stroke="{INK}" stroke-width="0.9"/>')
            m.append(f'<circle cx="866" cy="{ry}" r="2.8" fill="#6F8496" stroke="{INK}" stroke-width="0.9"/>')

        # Foreground visitor steel counter ledge spanning bottom
        m.append(f'<polygon points="0,446 960,424 960,540 0,540" fill="url(#{p}_counter)" stroke="{INK}" stroke-width="2.2"/>')
        m.append('<path d="M0,448 L960,426" fill="none" stroke="#9BC8E2" stroke-width="1.6" opacity="0.50"/>')

        # Coiled black handset cord & steel cradle on right edge of counter
        m.append(f'<rect x="866" y="344" width="32" height="58" rx="4" fill="#1D242C" stroke="{INK}" stroke-width="1.6"/>')
        m.append('<path d="M882,402 Q896,422 878,434 Q864,446 884,458 Q898,470 882,482" fill="none" stroke="#11151A" stroke-width="4.2" stroke-linecap="round"/>')
        m.append('<path d="M882,402 Q896,422 878,434 Q864,446 884,458 Q898,470 882,482" fill="none" stroke="#3D4C5C" stroke-width="1.2" stroke-dasharray="3 4"/>')

        m.append('</g>')
        parts.append("".join(m))

    # -------------------------------------------------------------------------
    # LAYER 3: SAHNE (R4-PARALAKS LOCKED: Locked Lincoln v1 + his tattoo-free
    # hand on glass + Scratched Visiting Glass & Speaker Grille + Locked
    # Michael v3 parting blue shirt to show glowing #7FE6FF blueprint tattoo!)
    # -------------------------------------------------------------------------
    if _katman_aktif(katmanlar, "sahne"):
        s: list[str] = ['<g id="s301-sahne">']

        # === 1) LOCKED LINCOLN V1 BEHIND THE VISITING GLASS (right side, facing left) ===
        # Locked proportions (al_lincoln_v1.png): head_w ~88px -> shoulder_w ~208px (2.36x head_w)
        # Collar-Over-Neck Z-Order: torso & arms -> K.lincoln_kafa(boyun=True) -> collar flaps on TOP!
        s.append('<g id="s301-lincoln">')
        # Lincoln's far/left upper arm (viewer's right, x=756..796)
        s.append(
            f'<path d="M758,260 L784,274 Q798,322 794,416 L758,416 L754,284 Z" '
            f'fill="#3D5670" stroke="{INK}" stroke-width="2.0" stroke-linejoin="round"/>'
        )
        # Athletic tailored Fox River blue prison shirt torso (x=592..768, crisp shoulder slope, NO dome!)
        s.append(
            f'<path d="M598,266 L644,246 L724,246 L768,266 L764,418 L602,418 Z" '
            f'fill="url(#{p}_shirt_l)" stroke="{INK}" stroke-width="2.1" stroke-linejoin="round"/>'
        )
        # White undershirt V-base
        s.append(f'<path d="M652,246 L682,298 L712,246 Z" fill="#DFE5E5" stroke="{INK}" stroke-width="1.5"/>')
        # Shirt placket, buttons & 79238 chest pocket
        s.append(f'<path d="M682,298 L682,418" fill="none" stroke="{INK}" stroke-width="1.4"/>')
        for lby in (326, 362, 398):
            s.append(f'<circle cx="682" cy="{lby}" r="2.6" fill="#E4E1D8" stroke="{INK}" stroke-width="0.9"/>')
        s.append(f'<rect x="704" y="314" width="42" height="38" rx="2" fill="none" stroke="{INK}" stroke-width="1.4" opacity="0.76"/>')
        s.append('<text x="702" y="308" font-family="DejaVu Sans Mono, monospace" font-size="9.5" font-weight="bold" fill="#DCE6EE" opacity="0.82">79238</text>')
        # Crisp shoulder-seam lines & cold overhead rim
        s.append(f'<path d="M604,268 L612,336 M760,268 L754,336" fill="none" stroke="{INK}" stroke-width="1.5" opacity="0.72"/>')
        s.append('<path d="M602,265 L644,247 L724,247 L764,265" fill="none" stroke="#B6E4FA" stroke-width="2.0" opacity="0.56" stroke-linecap="round"/>')

        # Lincoln's raised right arm: continuous shoulder -> upper arm -> rolled cuff -> TATTOO-FREE forearm (R3!) -> palm on glass
        s.append(
            f'<g id="s301-lincoln-arm">'
            # Upper arm descending from right shoulder seam (x=602, y=266) to elbow (x=548, y=318)
            f'<path d="M604,266 Q574,274 544,296 L532,324 Q568,332 606,318 L610,282 Z" '
            f'fill="url(#{p}_shirt_l)" stroke="{INK}" stroke-width="2.0" stroke-linejoin="round"/>'
            # Rolled shirt cuff at elbow
            f'<path d="M546,292 L528,284 L518,318 L538,326 Z" fill="#3B546E" stroke="{INK}" stroke-width="1.7" stroke-linejoin="round"/>'
            # Muscular TATTOO-FREE forearm rising cleanly from cuff to wrist (R3 strict!)
            f'<path d="M528,288 L494,276 L484,302 L520,316 Z" fill="#C99C7C" stroke="{INK}" stroke-width="1.9" stroke-linejoin="round"/>'
            # Flat open palm & five natural fingers pressed firmly against the glass (clean skin, zero tattoos)
            f'<path d="M472,256 Q464,254 464,266 L466,294 Q468,312 486,312 L498,306 Q506,298 504,282 '
            f'L503,244 Q501,234 495,235 Q490,237 490,250 L487,231 Q485,221 479,223 Q474,225 474,240 '
            f'L470,228 Q466,220 461,224 Q457,228 459,244 L454,241 Q448,240 447,248 Q448,257 457,270 L466,288 Z" '
            f'fill="#D4A889" stroke="{INK}" stroke-width="1.8" stroke-linejoin="round"/>'
            # Pressed palm pad flush against glass + faint condensation halo
            f'<ellipse cx="482" cy="282" rx="13" ry="16" fill="#E3BC9F" opacity="0.65"/>'
            f'<path d="M472,274 Q482,268 492,276 M474,288 Q484,284 494,292" fill="none" stroke="#9B6E52" stroke-width="1.1" opacity="0.65"/>'
            f'<ellipse cx="480" cy="268" rx="36" ry="46" fill="#D4F0FF" opacity="0.15"/>'
            f'</g>'
        )

        # Locked K.lincoln_kafa (view="3q", ifade="odak", flipped horizontally to face Michael!)
        s.append(
            f'<g transform="translate(684,180) scale(-0.62,0.62)">'
            f'{K.lincoln_kafa(view="3q", ifade="odak", look=0.32, boyun=True)}'
            f'</g>'
        )
        # COLLAR-OVER-NECK Z-ORDER: Shirt collar flaps & undershirt neckline drawn OVER neck base!
        s.append('<path d="M652,250 Q682,266 712,250 L708,266 Q682,282 656,266 Z" fill="#DFE5E5" stroke="{INK}" stroke-width="1.4"/>'.replace("{INK}", INK))
        s.append(f'<path d="M648,244 L636,282 L668,294 L662,254 Z" fill="#6383A4" stroke="{INK}" stroke-width="1.7" stroke-linejoin="round"/>')
        s.append(f'<path d="M716,244 L728,282 L696,294 L702,254 Z" fill="#4B6885" stroke="{INK}" stroke-width="1.7" stroke-linejoin="round"/>')
        s.append('</g>')

        # === 2) SCRATCHED VISITING GLASS PANE & PERFORATED METAL SPEAKER GRILLE ===
        s.append('<g id="s301-visiting-glass">')
        # Semi-transparent glass wash over Lincoln's bay
        s.append(f'<rect x="362" y="54" width="492" height="378" fill="url(#{p}_glass_tint)"/>')
        # Diagonal cold fluorescent & warm hallway reflection bands across the glass
        s.append('<polygon points="404,54 474,54 362,294 362,212" fill="#DDF6FF" opacity="0.12"/>')
        s.append(f'<polygon points="690,54 786,54 610,432 528,432" fill="url(#{p}_warm_refl)"/>')
        s.append('<polygon points="792,54 832,54 676,432 642,432" fill="#E8FAFF" opacity="0.09"/>')

        # Fine worn scratches & scuff arcs on prison acrylic glass
        scratches = [
            "M412,118 L468,144", "M426,126 L452,138", "M542,92 L584,116",
            "M442,320 Q478,308 518,326", "M736,162 L784,196", "M752,184 L792,206",
            "M578,362 L636,348", "M386,232 L416,262", "M804,284 L838,314",
        ]
        for sc in scratches:
            s.append(f'<path d="{sc}" fill="none" stroke="#E2F6FF" stroke-width="0.9" opacity="0.34" stroke-linecap="round"/>')

        # Circular perforated steel voice speaker grille mounted in center-lower glass (x=556, y=346)
        gx_c, gy_c = 558, 344
        s.append(f'<circle cx="{gx_c}" cy="{gy_c}" r="34" fill="#2A343E" stroke="{INK}" stroke-width="2.0"/>')
        s.append(f'<circle cx="{gx_c}" cy="{gy_c}" r="28" fill="#1C242C" stroke="#6B8094" stroke-width="1.3"/>')
        # Concentric speaker perforations
        for r_ring, count in [(0, 1), (8, 6), (16, 12), (23, 16)]:
            for idx in range(count):
                ang = (2 * math.pi * idx) / count
                hx = gx_c + r_ring * math.cos(ang)
                hy = gy_c + r_ring * math.sin(ang)
                s.append(f'<circle cx="{hx:.1f}" cy="{hy:.1f}" r="1.8" fill="#0B0F14"/>')
        # Four mounting screws around speaker rim
        for ang_d in (45, 135, 225, 315):
            rad = math.radians(ang_d)
            sx_r = gx_c + 31 * math.cos(rad)
            sy_r = gy_c + 31 * math.sin(rad)
            s.append(f'<circle cx="{sx_r:.1f}" cy="{sy_r:.1f}" r="2.0" fill="#8FA4B5" stroke="{INK}" stroke-width="0.8"/>')
        s.append('</g>')

        # === 3) LOCKED MICHAEL V3 IN FOREGROUND-LEFT (parting Fox River blue shirt to reveal glowing #7FE6FF tattoo!) ===
        # Locked proportions (ay_yetiskin_v3.png): head_w ~112px -> shoulder_w ~244px (2.18x head_w, athletic lean!)
        # Collar-Over-Neck Z-Order: torso/chest -> K.michael_kafa(boyun=True) -> collar flaps & parting arms on TOP!
        s.append('<g id="s301-michael">')
        # Left outer arm (viewer's left, x=32..78) descending naturally from rounded shoulder seam
        s.append(
            f'<path d="M68,295 Q46,304 38,332 Q28,402 32,540 L78,540 L82,364 Z" '
            f'fill="#567696" stroke="{INK}" stroke-width="2.2" stroke-linejoin="round"/>'
        )
        # Athletic tailored Fox River blue prison shirt torso (x=64..290, natural sloping shoulders, NO dome!)
        s.append(
            f'<path d="M68,295 Q96,280 132,268 L224,268 Q260,280 288,295 L284,540 L72,540 Z" '
            f'fill="url(#{p}_shirt_m)" stroke="{INK}" stroke-width="2.3" stroke-linejoin="round"/>'
        )
        # Crisp shoulder-to-armpit seam lines (matches ay_yetiskin_v3.png!)
        s.append(f'<path d="M76,304 L82,374 M280,304 L274,374" fill="none" stroke="{INK}" stroke-width="1.7" opacity="0.78"/>')

        # Parted shirt opening exposing warm chest skin + glowing original architectural tattoo!
        s.append(
            f'<path d="M138,268 L152,328 L168,422 L222,418 L240,326 L218,268 Z" '
            f'fill="#D5A687" stroke="{INK}" stroke-width="1.8" stroke-linejoin="round"/>'
        )
        # Subtle pectoral & sternum shadow
        s.append('<path d="M144,272 Q160,326 164,418" fill="none" stroke="#96684E" stroke-width="7" opacity="0.22"/>')

        # HIGH-DETAIL ORIGINAL ARCHITECTURAL & FILIGREE CHEST TATTOO (A-Sirt v1 craftsmanship — R1 compliant!)
        # Layered skin-embedded ink (#222E3B/#17202A/#354656), Gothic arch reliefs, organic scrollwork filigree,
        # twin origami crane wings, fine architectural hatching & organically woven #7FE6FF cyan Plan Vision!
        s.append(f'<ellipse cx="194" cy="358" rx="48" ry="44" fill="url(#{p}_tat_glow)"/>')
        s.append(
            f'<g id="s301-chest-tattoo">'
            # 1) Soft translucent ink shadow planes embedded in skin (depth & relief)
            f'<path d="M158,414 L158,340 Q194,298 230,340 L230,414 Z" fill="#222E3B" fill-opacity="0.13"/>'
            f'<path d="M168,414 L168,348 Q194,314 220,348 L220,414 Z" fill="#17202A" fill-opacity="0.14"/>'
            f'<polygon points="154,344 176,320 194,334 184,352 162,354" fill="#222E3B" fill-opacity="0.16"/>'
            f'<polygon points="234,344 212,320 194,334 204,352 226,354" fill="#222E3B" fill-opacity="0.16"/>'
            # 2) Double-framed Gothic lancet arch & keystone relief
            f'<path d="M156,416 L156,342 Q158,314 194,298 Q230,314 232,342 L232,416" '
            f'fill="none" stroke="#17202A" stroke-width="1.75" opacity="0.88" stroke-linecap="round"/>'
            f'<path d="M162,416 L162,344 Q164,320 194,305 Q224,320 226,344 L226,416" '
            f'fill="none" stroke="#222E3B" stroke-width="1.25" opacity="0.84"/>'
            f'<path d="M170,416 L170,352 Q173,330 194,318 Q215,330 218,352 L218,416" '
            f'fill="none" stroke="#222E3B" stroke-width="1.15" opacity="0.82"/>'
            # Gothic rose-window medallion & spokes at upper sternum
            f'<circle cx="194" cy="336" r="14" fill="none" stroke="#17202A" stroke-width="1.3" opacity="0.84"/>'
            f'<circle cx="194" cy="336" r="8.5" fill="none" stroke="#354656" stroke-width="0.9" opacity="0.78"/>'
            f'<path d="M194,322 L194,350 M180,336 L208,336 M184,326 L204,346 M204,326 L184,346" '
            f'fill="none" stroke="#354656" stroke-width="0.75" opacity="0.72"/>'
            # 3) Organic curved filigree / acanthus scrollwork flanking the Gothic arch
            f'<path d="M156,336 Q146,326 152,316 Q160,308 168,316 Q164,324 158,322" '
            f'fill="none" stroke="#17202A" stroke-width="1.15" opacity="0.82" stroke-linecap="round"/>'
            f'<path d="M232,336 Q242,326 236,316 Q228,308 220,316 Q224,324 230,322" '
            f'fill="none" stroke="#17202A" stroke-width="1.15" opacity="0.82" stroke-linecap="round"/>'
            f'<path d="M156,364 Q148,374 156,384 Q162,390 166,382 M232,364 Q240,374 232,384 Q226,390 222,382" '
            f'fill="none" stroke="#222E3B" stroke-width="1.1" opacity="0.80" stroke-linecap="round"/>'
            f'<path d="M170,392 Q182,382 194,394 Q206,382 218,392" '
            f'fill="none" stroke="#222E3B" stroke-width="1.05" opacity="0.78" stroke-linecap="round"/>'
            # 4) Twin symmetrical origami crane wings spreading across chest
            f'<path d="M194,334 L176,318 L150,336 L166,348 L184,350 Z M176,318 L166,348 M194,334 L162,338" '
            f'fill="none" stroke="#17202A" stroke-width="1.25" opacity="0.86" stroke-linejoin="round"/>'
            f'<path d="M194,334 L212,318 L238,336 L222,348 L204,350 Z M212,318 L222,348 M194,334 L226,338" '
            f'fill="none" stroke="#17202A" stroke-width="1.25" opacity="0.86" stroke-linejoin="round"/>'
            # 5) Fine architectural cross-hatching & micro blueprint masonry lines
            f'<path d="M162,356 L170,352 M162,364 L170,360 M162,372 L170,368 M162,380 L170,376 M162,388 L170,384 '
            f'M218,352 L226,356 M218,360 L226,364 M218,368 L226,372 M218,376 L226,380 M218,384 L226,388 '
            f'M176,356 L212,356 M174,372 L214,372 M176,404 L212,404" '
            f'fill="none" stroke="#354656" stroke-width="0.72" opacity="0.68"/>'
            # Hex bolt nodes hidden in the architecture
            f'<polygon points="194,307 197,309 197,313 194,315 191,313 191,309" fill="none" stroke="#222E3B" stroke-width="0.95" opacity="0.82"/>'
            f'<polygon points="178,378 181,380 181,384 178,386 175,384 175,380" fill="none" stroke="#222E3B" stroke-width="0.9" opacity="0.78"/>'
            # 6) Organically woven #7FE6FF Plan Vision corridor glowing from within the Gothic ink!
            f'<path d="M178,412 L178,382 Q178,372 188,372 L194,372 L194,344 Q194,336 202,336 L214,336 L214,324" '
            f'fill="none" stroke="{PLAN}" stroke-width="2.1" filter="url(#{p}_glow_cyan)" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="M178,412 L178,382 Q178,372 188,372 L194,372 L194,344 Q194,336 202,336 L214,336 L214,324" '
            f'fill="none" stroke="{PLAN_CORE}" stroke-width="0.85" opacity="0.92" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<circle cx="194" cy="336" r="2.8" fill="{PLAN_CORE}" filter="url(#{p}_glow_cyan)"/>'
            f'<circle cx="214" cy="324" r="2.6" fill="{PLAN_CORE}" filter="url(#{p}_glow_cyan)"/>'
            f'</g>'
        )

        # Shirt placket below parted opening, buttons & Fox River 94941 chest pocket
        s.append(f'<path d="M150,332 L166,430 L156,540 M240,332 L226,430 L236,540" fill="none" stroke="{INK}" stroke-width="1.9"/>')
        for by_btn in (446, 482, 518):
            s.append(f'<circle cx="164" cy="{by_btn}" r="3.0" fill="#E6E2D8" stroke="{INK}" stroke-width="1.1"/>')
        s.append(f'<rect x="92" y="366" width="44" height="42" rx="2" fill="none" stroke="{INK}" stroke-width="1.5" opacity="0.82"/>')
        s.append('<text x="90" y="359" font-family="DejaVu Sans Mono, monospace" font-size="11.0" font-weight="bold" fill="#EDE9DF" opacity="0.92">94941</text>')

        # Warm/cold rim highlight along Michael's crisp shoulder line
        s.append('<path d="M66,295 L130,269" fill="none" stroke="#FFE2B2" stroke-width="2.2" opacity="0.62" stroke-linecap="round"/>')
        s.append('<path d="M226,269 L290,295" fill="none" stroke="#A6E4FF" stroke-width="2.1" opacity="0.64" stroke-linecap="round"/>')

        # Locked K.michael_kafa (view="3q", ifade="kararli", boyun=True, looking intently across glass at Lincoln!)
        s.append(
            f'<g transform="translate(178,180) scale(0.84)">'
            f'{K.michael_kafa(view="3q", ifade="kararli", look=0.35, boyun=True)}'
            f'</g>'
        )
        # Seamless anatomical collarbone blend covering neck-base cut line inside open chest V
        s.append('<path d="M138,272 Q178,286 218,272 L222,294 Q178,306 140,294 Z" fill="#D5A687"/>')
        s.append('<path d="M150,292 Q178,303 194,291 M198,291 Q212,300 226,290" fill="none" stroke="#8C5D45" stroke-width="1.35" opacity="0.72" stroke-linecap="round"/>')

        # COLLAR-OVER-NECK Z-ORDER: Parted Fox River shirt collar flaps drawn cleanly OVER neck edges!
        s.append(f'<path d="M134,264 L114,304 L148,334 L154,316 L142,272 Z" fill="#7D9FC1" stroke="{INK}" stroke-width="1.8" stroke-linejoin="round"/>')
        s.append(f'<path d="M222,264 L248,304 L238,336 L226,316 L216,272 Z" fill="#4D6B8A" stroke="{INK}" stroke-width="1.8" stroke-linejoin="round"/>')

        # Michael's right arm: continuous shoulder (x=282, y=296) -> upper arm -> rolled cuff -> tattooed forearm -> hand parting lapel!
        s.append(
            f'<g id="s301-michael-arm">'
            # Upper arm descending smoothly from right shoulder seam to elbow (x=306, y=424)
            f'<path d="M286,294 Q306,304 314,330 Q324,382 314,432 L276,418 Q284,368 274,316 Z" '
            f'fill="#4D6B8A" stroke="{INK}" stroke-width="2.1" stroke-linejoin="round"/>'
            # Rolled shirt cuff at elbow
            f'<path d="M316,422 L280,406 L272,428 L308,444 Z" fill="#374E67" stroke="{INK}" stroke-width="1.8" stroke-linejoin="round"/>'
            # Sleek athletic forearm angling up-left to right shirt lapel with glowing #7FE6FF tattoo
            f'<path d="M300,440 Q272,426 244,408 L254,380 Q282,394 308,412 Z" '
            f'fill="#D5A687" stroke="{INK}" stroke-width="2.0" stroke-linejoin="round"/>'
            # Detailed organic filigree + Gothic arch forearm tattoo (matches chest & A-Sirt v1 quality!)
            f'<path d="M254,386 Q278,390 298,408 L292,424 Q270,418 250,404 Z" fill="#222E3B" fill-opacity="0.16"/>'
            f'<path d="M254,388 Q276,386 298,408 M252,402 Q274,418 294,424" '
            f'fill="none" stroke="#17202A" stroke-width="1.35" opacity="0.86" stroke-linecap="round"/>'
            f'<path d="M262,389 Q270,398 262,408 M274,393 Q282,404 273,414 M286,400 Q293,410 285,420" '
            f'fill="none" stroke="#222E3B" stroke-width="1.05" opacity="0.82" stroke-linecap="round"/>'
            f'<path d="M258,394 L292,412 M268,390 L264,404 M280,396 L276,410 M290,403 L286,417" '
            f'fill="none" stroke="#354656" stroke-width="0.72" opacity="0.72"/>'
            f'<path d="M256,397 Q268,402 276,409 L284,401 Q292,404 300,411" '
            f'fill="none" stroke="{PLAN}" stroke-width="1.85" filter="url(#{p}_glow_cyan)" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="M256,397 Q268,402 276,409 L284,401 Q292,404 300,411" '
            f'fill="none" stroke="{PLAN_CORE}" stroke-width="0.7" opacity="0.9" stroke-linecap="round"/>'
            # Hand gripping the parted right shirt lapel (natural fingers & thumb)
            f'<path d="M254,377 Q234,370 228,384 Q225,398 238,408 L254,412 Q262,396 254,377 Z" '
            f'fill="#D5A687" stroke="{INK}" stroke-width="1.9" stroke-linejoin="round"/>'
            f'<path d="M232,385 L247,387 M230,393 L245,395 M234,401 L247,403" fill="none" stroke="#8A5C44" stroke-width="1.15"/>'
            f'</g>'
        )
        s.append('</g>')

        s.append('</g>')
        parts.append("".join(s))

    # -------------------------------------------------------------------------
    # LAYER 4: PLAN (#7FE6FF CAD blueprint bridge from Michael's tattoo through
    # the glass to Lincoln + "GETTING YOU OUT" tag + top-right "DAYS LEFT: 29")
    # -------------------------------------------------------------------------
    if _katman_aktif(katmanlar, "plan"):
        pl: list[str] = ['<g id="s301-plan" opacity="0.90">']
        # Cyan CAD extraction vector connecting Michael's glowing chest tattoo to Lincoln's palm & eyes
        pl.append(
            f'<path d="M216,324 L378,324 L424,278 L466,278" fill="none" stroke="{PLAN}" '
            f'stroke-width="1.5" stroke-dasharray="6 4" filter="url(#{p}_glow_cyan)"/>'
        )
        pl.append(f'<circle cx="378" cy="324" r="3.0" fill="{PLAN_CORE}"/>')
        pl.append(f'<circle cx="466" cy="278" r="3.6" fill="{PLAN_CORE}" stroke="{PLAN}" stroke-width="1.2"/>')

        # Subtle CAD reticle around speaker grille
        pl.append(
            f'<path d="M514,310 L514,300 L526,300 M602,310 L602,300 L590,300 '
            f'M514,378 L514,388 L526,388 M602,378 L602,388 L590,388" '
            f'fill="none" stroke="{PLAN}" stroke-width="1.2" opacity="0.72"/>'
        )

        # Clean CAD callout tag: "GETTING YOU OUT"
        pl.append(f'<rect x="374" y="102" width="164" height="24" rx="3" fill="#08131E" opacity="0.86" stroke="{PLAN}" stroke-width="1.1"/>')
        pl.append(
            f'<text x="384" y="118" font-family="DejaVu Sans Mono, monospace" font-size="11.2" '
            f'font-weight="bold" fill="{PLAN_CORE}" letter-spacing="1.0">GETTING YOU OUT</text>'
        )
        pl.append(f'<path d="M456,126 L456,216" fill="none" stroke="{PLAN}" stroke-width="1.0" stroke-dasharray="4 3" opacity="0.65"/>')

        # Top-right DAYS LEFT: 29 counter
        pl.append(_hud_days_left(754, 16, 29))
        pl.append('</g>')
        parts.append("".join(pl))

    # -------------------------------------------------------------------------
    # LAYER 5: ONPLAN (Non-character outer booth framing, atmospheric dust motes,
    # cold/warm light bloom & cinematic vignette)
    # -------------------------------------------------------------------------
    if _katman_aktif(katmanlar, "onplan"):
        op: list[str] = ['<g id="s301-onplan">']
        # Subtle dark foreground booth edge columns (framing only, never covering faces)
        op.append('<rect x="0" y="0" width="16" height="540" fill="#0A1017" opacity="0.78"/>')
        op.append('<rect x="944" y="0" width="16" height="540" fill="#0A1017" opacity="0.78"/>')
        # Soft floating dust motes in cold fluorescent beam
        for _ in range(26):
            dx = rng.uniform(180, 880)
            dy = rng.uniform(44, 440)
            dr = rng.uniform(0.8, 1.8)
            op.append(f'<circle cx="{dx:.1f}" cy="{dy:.1f}" r="{dr:.1f}" fill="#DFF6FF" opacity="{rng.uniform(0.16, 0.44):.2f}"/>')
        op.append(f'<rect x="0" y="0" width="960" height="540" fill="url(#{p}_vignette)"/>')
        op.append('</g>')
        parts.append("".join(op))

    return defs, "".join(parts)


# =============================================================================
# 3.02 · YARD CREW CARDS ("LONG STORY.")
# =============================================================================
def _crew_portrait_abruzzi() -> str:
    """High-craft stylized 2D portrait: John Abruzzi archetype (R1 compliant —
    slicked-back glossy dark wavy hair with tapered temples, narrow sharp
    charismatic cheekbones/jaw, piercing narrowed gaze, light stubble shadow,
    half-open Fox River collar, confident cold mob-boss bearing)."""
    return (
        '<rect x="0" y="0" width="150" height="122" fill="#232A33"/>'
        '<rect x="0" y="0" width="150" height="122" fill="#121820" opacity="0.46"/>'
        # Prison mugshot height calibration rules
        '<path d="M0,24 L150,24 M0,48 L150,48 M0,72 L150,72 M0,96 L150,96" fill="none" stroke="#4D5F70" stroke-width="0.65" opacity="0.42"/>'
        # Confident angled shoulders & half-open Fox River blue shirt over white tee
        '<path d="M14,122 L28,90 L56,82 L94,82 L122,90 L136,122 Z" fill="#46627E" stroke="#161414" stroke-width="1.8" stroke-linejoin="round"/>'
        '<path d="M58,82 L75,110 L92,82 Z" fill="#E6E2D8" stroke="#161414" stroke-width="1.2"/>'
        # Half-open folded shirt collar lapels
        '<path d="M54,82 L44,102 L68,108 L64,84 Z" fill="#5D7D9E" stroke="#161414" stroke-width="1.4" stroke-linejoin="round"/>'
        '<path d="M96,82 L106,102 L82,108 L86,84 Z" fill="#3A536C" stroke="#161414" stroke-width="1.4" stroke-linejoin="round"/>'
        # Neck with sternocleidomastoid shadow
        '<path d="M65,68 L63,86 Q75,92 87,86 L85,68 Z" fill="#BC8E70" stroke="#161414" stroke-width="1.5"/>'
        '<path d="M66,72 Q75,80 84,72 L85,82 Q75,86 65,82 Z" fill="#8C5F46" opacity="0.48"/>'
        # Ears
        '<ellipse cx="50" cy="48" rx="4.2" ry="7.5" fill="#C99B7D" stroke="#161414" stroke-width="1.3"/>'
        '<ellipse cx="100" cy="48" rx="4.2" ry="7.5" fill="#B28366" stroke="#161414" stroke-width="1.3"/>'
        # Narrow, sharp charismatic face contour (defined cheekbones & chiseled jaw)
        '<path d="M51,38 Q51,15 75,15 Q99,15 99,38 L97,54 L90,70 Q83,79 75,80 Q67,79 60,70 L53,54 Z" '
        'fill="#D4A586" stroke="#161414" stroke-width="1.8" stroke-linejoin="round"/>'
        # Cinematic cel-shading plane (right cheek/jaw shadow + left cheekbone hollow)
        '<path d="M77,17 Q98,19 98,40 L95,55 L88,70 Q82,78 75,79 L75,17 Z" fill="#B28264" opacity="0.48"/>'
        '<path d="M54,52 Q60,59 64,66 M96,52 Q90,59 86,66" fill="none" stroke="#8C5D44" stroke-width="1.2" opacity="0.62" stroke-linecap="round"/>'
        # Light confident 2-3 day stubble shadow along jaw & upper lip
        '<path d="M56,57 Q75,84 94,57 L90,70 Q82,79 75,80 Q68,79 60,70 Z" fill="#2A2420" opacity="0.20"/>'
        # Signature slicked-back glossy dark wavy mob-boss hair (tapered temples, subtle volume on crown)
        '<path d="M48,43 Q45,26 52,16 Q63,7 76,8 Q92,9 100,19 Q104,29 101,43 '
        'Q96,30 92,24 Q84,20 75,21 Q64,20 57,25 Q53,31 48,43 Z" '
        'fill="#1D1917" stroke="#161414" stroke-width="1.6" stroke-linejoin="round"/>'
        # Glossy swept-back comb streaks & slight silver temple glint
        '<path d="M58,15 Q74,10 92,16 M62,19 Q76,15 90,20" fill="none" stroke="#4D443E" stroke-width="1.6" opacity="0.72" stroke-linecap="round"/>'
        '<path d="M66,13 Q76,11 86,14" fill="none" stroke="#7A7068" stroke-width="1.1" opacity="0.55" stroke-linecap="round"/>'
        '<path d="M50,36 L53,27 M100,36 L97,27" fill="none" stroke="#8B9298" stroke-width="1.4" opacity="0.55" stroke-linecap="round"/>'
        # Low, sharp dark brows & piercing narrowed calculating eyes
        '<path d="M56,41 L71,43 M79,43 L94,41" fill="none" stroke="#1B1715" stroke-width="2.5" stroke-linecap="round"/>'
        '<path d="M58,47 Q64,44.5 70,47.5 Q64,50 58,47 Z" fill="#F2EFEA" stroke="#161414" stroke-width="1.0"/>'
        '<circle cx="64.5" cy="47.2" r="2.2" fill="#2B3138"/>'
        '<circle cx="65.2" cy="46.5" r="0.7" fill="#FFFFFF"/>'
        '<path d="M80,47.5 Q86,44.5 92,47 Q86,50 80,47.5 Z" fill="#F2EFEA" stroke="#161414" stroke-width="1.0"/>'
        '<circle cx="85.5" cy="47.2" r="2.2" fill="#2B3138"/>'
        '<circle cx="86.2" cy="46.5" r="0.7" fill="#FFFFFF"/>'
        # Heavy upper eyelid crease & intense under-eye shadow
        '<path d="M57,45.5 L71,46.8 M79,46.8 L93,45.5" fill="none" stroke="#161414" stroke-width="1.4" stroke-linecap="round"/>'
        '<path d="M59,51 Q64,52.5 69,51 M81,51 Q86,52.5 91,51" fill="none" stroke="#7D543E" stroke-width="0.85" opacity="0.65"/>'
        # Sharp narrow nose bridge & thin serious mouth
        '<path d="M75,45 L73,58 Q75,60.5 78.5,58.5" fill="none" stroke="#6E4734" stroke-width="1.4" stroke-linecap="round"/>'
        '<path d="M66,67 Q75,65.5 84,67" fill="none" stroke="#4F2E24" stroke-width="1.8" stroke-linecap="round"/>'
        '<path d="M69,69.5 Q75,71 81,69.5" fill="none" stroke="#9E6A58" stroke-width="1.0" opacity="0.72" stroke-linecap="round"/>'
    )


def _crew_portrait_sucre() -> str:
    """High-craft stylized 2D portrait: Fernando Sucre archetype (R1 compliant —
    warm athletic slightly rounded face, ultra-short clean fade/buzz, friendly
    warm brown eyes, signature thin goatee & mustache contour, genuine warm grin)."""
    return (
        '<rect x="0" y="0" width="150" height="122" fill="#293845"/>'
        '<path d="M0,24 L150,24 M0,48 L150,48 M0,72 L150,72 M0,96 L150,96" fill="none" stroke="#567085" stroke-width="0.65" opacity="0.42"/>'
        # Fox River blue prison shirt & crisp white crewneck tee
        '<path d="M14,122 L28,90 L56,82 L94,82 L122,90 L136,122 Z" fill="#5D7FA1" stroke="#161414" stroke-width="1.8" stroke-linejoin="round"/>'
        '<path d="M58,82 L75,102 L92,82 Z" fill="#F0ECE2" stroke="#161414" stroke-width="1.2"/>'
        '<path d="M54,82 L47,98 L68,104 L63,84 Z" fill="#7395B8" stroke="#161414" stroke-width="1.3" stroke-linejoin="round"/>'
        '<path d="M96,82 L103,98 L82,104 L87,84 Z" fill="#4A6887" stroke="#161414" stroke-width="1.3" stroke-linejoin="round"/>'
        # Sturdy warm neck
        '<path d="M64,68 L62,86 Q75,92 88,86 L86,68 Z" fill="#B6805E" stroke="#161414" stroke-width="1.5"/>'
        # Ears
        '<ellipse cx="49" cy="48" rx="4.4" ry="7.4" fill="#C48D6B" stroke="#161414" stroke-width="1.3"/>'
        '<ellipse cx="101" cy="48" rx="4.4" ry="7.4" fill="#AC7656" stroke="#161414" stroke-width="1.3"/>'
        # Warm athletic slightly rounded oval head
        '<path d="M50,40 Q50,15 75,15 Q100,15 100,40 L98,58 Q93,75 75,78 Q57,75 52,58 Z" '
        'fill="#CE9773" stroke="#161414" stroke-width="1.8" stroke-linejoin="round"/>'
        '<path d="M77,17 Q99,19 99,42 L96,59 Q91,74 75,77 L75,17 Z" fill="#B07A58" opacity="0.44"/>'
        # Clean ultra-short buzz/fade haircut with crisp forehead hairline
        '<path d="M50,37 Q51,14 75,13 Q99,14 100,37 L96,34 Q94,24 75,23 Q56,24 54,34 Z" '
        'fill="#221D1A" stroke="#161414" stroke-width="1.4" stroke-linejoin="round"/>'
        '<path d="M56,20 Q75,16 94,20" fill="none" stroke="#463D37" stroke-width="1.6" opacity="0.55" stroke-linecap="round"/>'
        # Friendly expressive arched brows & warm brown eyes
        '<path d="M56,41 Q63,38 70,41 M80,41 Q87,38 94,41" fill="none" stroke="#1F1916" stroke-width="2.2" stroke-linecap="round"/>'
        '<ellipse cx="63" cy="47.5" rx="4.8" ry="3.0" fill="#F6F2EC" stroke="#161414" stroke-width="1.0"/>'
        '<circle cx="63.5" cy="47.5" r="2.2" fill="#472E1E"/>'
        '<circle cx="64.2" cy="46.8" r="0.75" fill="#FFFFFF"/>'
        '<ellipse cx="87" cy="47.5" rx="4.8" ry="3.0" fill="#F6F2EC" stroke="#161414" stroke-width="1.0"/>'
        '<circle cx="86.5" cy="47.5" r="2.2" fill="#472E1E"/>'
        '<circle cx="87.2" cy="46.8" r="0.75" fill="#FFFFFF"/>'
        # Warm natural nose
        '<path d="M75,45 L73,56 Q75,58.5 78.5,56.5" fill="none" stroke="#7A4E36" stroke-width="1.4" stroke-linecap="round"/>'
        # Signature Sucre thin neat goatee + pencil mustache framing a genuine friendly smile!
        '<path d="M64,62 Q75,59.5 86,62" fill="none" stroke="#231C18" stroke-width="1.8" opacity="0.88" stroke-linecap="round"/>'
        '<path d="M64,62 Q63,69 68,74 Q75,77.5 82,74 Q87,69 86,62" fill="none" stroke="#231C18" stroke-width="1.7" opacity="0.82" stroke-linecap="round"/>'
        '<path d="M70,73 Q75,76 80,73" fill="none" stroke="#231C18" stroke-width="2.6" opacity="0.86" stroke-linecap="round"/>'
        # Genuine warm smile inside goatee frame
        '<path d="M66,65.5 Q75,70.5 84,65.5" fill="none" stroke="#5E3428" stroke-width="1.7" stroke-linecap="round"/>'
        '<path d="M69,66.5 Q75,69.2 81,66.5" fill="none" stroke="#F7F4EE" stroke-width="1.2" opacity="0.82" stroke-linecap="round"/>'
    )


def _crew_portrait_westmoreland() -> str:
    """High-craft stylized 2D portrait: Charles Westmoreland archetype (R1 compliant —
    dignified older gentleman, neatly side-parted silver-white hair, thin wire-rimmed
    glasses, forehead & cheek age lines, calm wise eyes, neatly buttoned shirt)."""
    return (
        '<rect x="0" y="0" width="150" height="122" fill="#322F2B"/>'
        '<path d="M0,24 L150,24 M0,48 L150,48 M0,72 L150,72 M0,96 L150,96" fill="none" stroke="#6B6256" stroke-width="0.65" opacity="0.42"/>'
        # Neatly buttoned-up faded Fox River denim shirt (orderly gentleman)
        '<path d="M16,122 L30,90 L58,83 L92,83 L120,90 L134,122 Z" fill="#526B82" stroke="#161414" stroke-width="1.8" stroke-linejoin="round"/>'
        '<path d="M75,86 L75,122" fill="none" stroke="#161414" stroke-width="1.3"/>'
        '<circle cx="75" cy="95" r="2.0" fill="#DDD8CE" stroke="#161414" stroke-width="0.8"/>'
        '<circle cx="75" cy="110" r="2.0" fill="#DDD8CE" stroke="#161414" stroke-width="0.8"/>'
        # Neat closed shirt collar
        '<path d="M58,83 L66,97 L75,88 L84,97 L92,83 Z" fill="#637E96" stroke="#161414" stroke-width="1.4" stroke-linejoin="round"/>'
        # Neck
        '<path d="M66,68 L65,86 Q75,90 85,86 L84,68 Z" fill="#C49A7E" stroke="#161414" stroke-width="1.5"/>'
        # Ears
        '<ellipse cx="51" cy="49" rx="4.2" ry="7.6" fill="#D4AB8F" stroke="#161414" stroke-width="1.3"/>'
        '<ellipse cx="99" cy="49" rx="4.2" ry="7.6" fill="#BE9478" stroke="#161414" stroke-width="1.3"/>'
        # Dignified older oval face
        '<path d="M52,38 Q52,15 75,15 Q98,15 98,38 L95,59 Q90,75 75,77 Q60,75 55,59 Z" '
        'fill="#DFB69A" stroke="#161414" stroke-width="1.8" stroke-linejoin="round"/>'
        '<path d="M77,17 Q97,19 97,40 L94,59 Q89,73 75,76 L75,17 Z" fill="#C2987C" opacity="0.40"/>'
        # Neatly side-parted silver-white hair (left-side part, dignified combed volume)
        '<path d="M49,42 Q47,21 58,14 Q68,10 82,12 Q98,14 101,34 L100,42 '
        'Q96,29 88,24 Q74,23 62,27 Q57,24 54,32 L51,42 Z" '
        'fill="#C4C9CE" stroke="#161414" stroke-width="1.5" stroke-linejoin="round"/>'
        # Side part line & combed silver-white sheen
        '<path d="M62,14 L60,26" fill="none" stroke="#6E757C" stroke-width="1.2" opacity="0.78"/>'
        '<path d="M64,16 Q80,14 94,21 M65,20 Q80,18 92,24" fill="none" stroke="#EEF2F5" stroke-width="1.4" opacity="0.75" stroke-linecap="round"/>'
        # Forehead & nasolabial gentle age lines
        '<path d="M62,31 Q75,29.5 88,31 M65,35 Q75,34 85,35" fill="none" stroke="#9C735B" stroke-width="0.8" opacity="0.58" stroke-linecap="round"/>'
        '<path d="M62,58 Q59,64 62,69 M88,58 Q91,64 88,69" fill="none" stroke="#966C54" stroke-width="0.95" opacity="0.62" stroke-linecap="round"/>'
        # Soft grey brows & calm wise eyes behind thin wire-rimmed glasses
        '<path d="M56,41 Q63,39 70,41 M80,41 Q87,39 94,41" fill="none" stroke="#7A8086" stroke-width="1.9" stroke-linecap="round"/>'
        '<ellipse cx="63" cy="48.5" rx="4.0" ry="2.4" fill="#F4F0EA" stroke="#161414" stroke-width="0.8"/>'
        '<circle cx="63" cy="48.5" r="1.8" fill="#3D4E5A"/>'
        '<circle cx="63.6" cy="48.0" r="0.6" fill="#FFFFFF"/>'
        '<ellipse cx="87" cy="48.5" rx="4.0" ry="2.4" fill="#F4F0EA" stroke="#161414" stroke-width="0.8"/>'
        '<circle cx="87" cy="48.5" r="1.8" fill="#3D4E5A"/>'
        '<circle cx="87.6" cy="48.0" r="0.6" fill="#FFFFFF"/>'
        # Thin gold/steel wire-rimmed spectacles with subtle lens glint
        '<rect x="54.5" y="43.5" width="17" height="10.5" rx="3.2" fill="#E8F4FA" fill-opacity="0.22" stroke="#484E54" stroke-width="1.35"/>'
        '<rect x="78.5" y="43.5" width="17" height="10.5" rx="3.2" fill="#E8F4FA" fill-opacity="0.22" stroke="#484E54" stroke-width="1.35"/>'
        '<path d="M71.5,47.5 Q75,46 78.5,47.5 M51.5,47 L54.5,47 M95.5,47 L98.5,47" fill="none" stroke="#484E54" stroke-width="1.2"/>'
        '<path d="M57,45.5 L61,45.5 M81,45.5 L85,45.5" fill="none" stroke="#FFFFFF" stroke-width="0.9" opacity="0.65" stroke-linecap="round"/>'
        # Gentle nose & calm dignified closed mouth
        '<path d="M75,47 L73,58.5 Q75,60.5 78,59" fill="none" stroke="#8C624A" stroke-width="1.3" stroke-linecap="round"/>'
        '<path d="M67,66.5 Q75,68 83,66.5" fill="none" stroke="#6E493C" stroke-width="1.55" stroke-linecap="round"/>'
    )


def _red_paperclip(x: float, y: float, rot: float = -12.0) -> str:
    """Glossy red steel paperclip fastening a dossier photo."""
    return (
        f'<g transform="translate({x:.1f},{y:.1f}) rotate({rot:.1f})">'
        f'<path d="M-6,-18 L-6,14 Q-6,22 2,22 Q10,22 10,14 L10,-12 Q10,-18 4,-18 Q-2,-18 -2,-12 L-2,10 Q-2,14 2,14 Q6,14 6,10 L6,-8" '
        f'fill="none" stroke="#180808" stroke-width="4.2" stroke-linecap="round" stroke-linejoin="round"/>'
        f'<path d="M-6,-18 L-6,14 Q-6,22 2,22 Q10,22 10,14 L10,-12 Q10,-18 4,-18 Q-2,-18 -2,-12 L-2,10 Q-2,14 2,14 Q6,14 6,10 L6,-8" '
        f'fill="none" stroke="#C8262B" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>'
        f'<path d="M-4,-15 L-4,11" fill="none" stroke="#FF8A8E" stroke-width="0.9" opacity="0.7" stroke-linecap="round"/>'
        f'</g>'
    )


def set_302_ekip_kartlari(katmanlar: set[str] | list[str] | None = None) -> tuple[str, str]:
    """Sunlit, dusty Fox River yard concrete table (chain-link fence & watchtower
    silhouette behind) with 3 crisp polaroid/dossier cards slammed down:
      1) JOHN ABRUZZI · MOB BOSS
      2) FERNANDO SUCRE · CELLMATE
      3) CHARLES WESTMORELAND · D.B. COOPER?
    Red paperclips, cyan Plan Vision links, and a dry-humor red stamp: LONG STORY."""
    rng = random.Random(302)
    p = _uid("s302")

    defs = f"""
    <linearGradient id="{p}_sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#8AA8BE"/>
      <stop offset="52%" stop-color="#C8C4B4"/>
      <stop offset="100%" stop-color="#DFC498"/>
    </linearGradient>
    <linearGradient id="{p}_concrete_top" x1="0" y1="0" x2="1" y2="0.8">
      <stop offset="0%" stop-color="#B9B0A0"/>
      <stop offset="48%" stop-color="#9E9586"/>
      <stop offset="100%" stop-color="#7B7367"/>
    </linearGradient>
    <linearGradient id="{p}_card_paper" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#FAF6EC"/>
      <stop offset="72%" stop-color="#EDE4D1"/>
      <stop offset="100%" stop-color="#D8CCB4"/>
    </linearGradient>
    <linearGradient id="{p}_sun_wash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFE6AE" stop-opacity="0.34"/>
      <stop offset="55%" stop-color="#F2B864" stop-opacity="0.10"/>
      <stop offset="100%" stop-color="#C98A3A" stop-opacity="0.0"/>
    </linearGradient>
    <radialGradient id="{p}_vignette" cx="0.50" cy="0.54" r="0.72">
      <stop offset="50%" stop-color="#000000" stop-opacity="0.0"/>
      <stop offset="100%" stop-color="#14100C" stop-opacity="0.58"/>
    </radialGradient>
    <filter id="{p}_glow_cyan" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="2.2" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    """

    parts: list[str] = []

    # -------------------------------------------------------------------------
    # LAYER 1: UZAK (Sunlit hazy Fox River sky, high perimeter stone wall,
    # corner guard watchtower silhouette & coiled razor-wire crest)
    # -------------------------------------------------------------------------
    if _katman_aktif(katmanlar, "uzak"):
        u: list[str] = ['<g id="s302-uzak">']
        u.append(f'<rect x="0" y="0" width="960" height="220" fill="url(#{p}_sky)"/>')
        # Warm hazy afternoon sun disc upper-left
        u.append('<circle cx="146" cy="52" r="56" fill="#FFF2CE" opacity="0.32"/>')
        u.append('<circle cx="146" cy="52" r="26" fill="#FFF8E2" opacity="0.55"/>')

        # High Fox River limestone perimeter wall
        u.append('<rect x="0" y="96" width="960" height="92" fill="#8C8375" stroke="#5A5247" stroke-width="1.2"/>')
        for wy in (118, 140, 162):
            u.append(f'<path d="M0,{wy} L960,{wy}" fill="none" stroke="#70685B" stroke-width="0.9" opacity="0.55"/>')

        # Watchtower silhouette on right-back
        u.append(
            f'<g id="s302-watchtower" opacity="0.88">'
            f'<polygon points="782,188 796,86 842,86 856,188" fill="#46423D" stroke="{INK}" stroke-width="1.4"/>'
            f'<rect x="780" y="54" width="78" height="34" fill="#3B3834" stroke="{INK}" stroke-width="1.5"/>'
            f'<polygon points="772,54 819,36 866,54" fill="#2D2B28" stroke="{INK}" stroke-width="1.5"/>'
            f'<rect x="790" y="62" width="58" height="14" fill="#8EAAB8" opacity="0.72" stroke="{INK}" stroke-width="1.0"/>'
            f'</g>'
        )

        # Chain-link fence diamond mesh & razor wire along top of yard wall
        for fx in range(0, 960, 26):
            u.append(f'<path d="M{fx},86 L{fx+62},192 M{fx+62},86 L{fx},192" fill="none" stroke="#3B3D40" stroke-width="0.7" opacity="0.34"/>')
        for rx in range(10, 960, 28):
            u.append(f'<circle cx="{rx}" cy="92" r="10" fill="none" stroke="#3D4044" stroke-width="1.1" opacity="0.62"/>')

        # Distant dusty yard gravel strip
        u.append('<rect x="0" y="176" width="960" height="44" fill="#A6967E"/>')
        u.append('</g>')
        parts.append("".join(u))

    # -------------------------------------------------------------------------
    # LAYER 2: ORTA (Weathered sunlit Fox River yard concrete table top,
    # hairline cracks, aggregate speckles & diagonal fence shadow)
    # -------------------------------------------------------------------------
    if _katman_aktif(katmanlar, "orta"):
        m: list[str] = ['<g id="s302-orta">']
        # Concrete table perspective slab
        m.append(f'<polygon points="0,192 960,184 960,540 0,540" fill="url(#{p}_concrete_top)" stroke="{INK_WARM}" stroke-width="2.2"/>')
        m.append('<path d="M0,194 L960,186" fill="none" stroke="#EAE1CE" stroke-width="2.0" opacity="0.65"/>')

        # Weathered concrete cracks & pitted aggregate texture
        m.append('<path d="M46,246 L112,262 L148,252 L192,276" fill="none" stroke="#5A5348" stroke-width="1.2" opacity="0.52"/>')
        m.append('<path d="M842,226 L888,254 L938,244" fill="none" stroke="#5A5348" stroke-width="1.1" opacity="0.48"/>')
        m.append('<path d="M440,486 L496,508 L544,500" fill="none" stroke="#534C42" stroke-width="1.3" opacity="0.55"/>')
        for _ in range(110):
            sx = rng.uniform(12, 948)
            sy = rng.uniform(198, 532)
            sr = rng.uniform(0.8, 2.2)
            scol = "#6E675C" if rng.random() < 0.6 else "#D8CFC0"
            m.append(f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="{sr:.1f}" fill="{scol}" opacity="{rng.uniform(0.18, 0.42):.2f}"/>')

        # Soft diagonal cast shadow of yard fence post across top-right corner of concrete table
        m.append('<polygon points="690,186 960,184 960,340 824,340" fill="#2A2622" opacity="0.14"/>')
        m.append('</g>')
        parts.append("".join(m))

    # -------------------------------------------------------------------------
    # LAYER 3: SAHNE (3 slammed polaroid/dossier crew cards with red paperclips
    # + dry-humor red rubber stamp "LONG STORY." + yard drafting pencil)
    # -------------------------------------------------------------------------
    if _katman_aktif(katmanlar, "sahne"):
        s: list[str] = ['<g id="s302-sahne">']

        cards = [
            (
                186, 336, -6.5,
                _crew_portrait_abruzzi(),
                "JOHN ABRUZZI", "MOB BOSS",
                "ASSET: AIRSTRIP · PI CREW", "#9E1F24",
                "DOC #FR-114",
            ),
            (
                474, 326, 2.2,
                _crew_portrait_sucre(),
                "FERNANDO SUCRE", "CELLMATE",
                "ASSET: CELL 40 · DIGGER", "#275A82",
                "DOC #FR-040",
            ),
            (
                762, 334, 5.4,
                _crew_portrait_westmoreland(),
                "CHARLES WESTMORELAND", "D.B. COOPER?",
                "ASSET: $5,000,000 · UTAH", "#8B5A1B",
                "DOC #FR-215",
            ),
        ]

        for cx, cy, rot, portrait_svg, name, role, asset_note, role_col, doc_id in cards:
            s.append(f'<g transform="translate({cx},{cy}) rotate({rot:.1f})">')
            # Hard sunlit cast shadow on concrete table
            s.append('<rect x="-102" y="-116" width="214" height="248" rx="3" fill="#1C1814" opacity="0.34" transform="translate(8,10)"/>')
            # Manila dossier backing tab peeking out top-left
            s.append(f'<path d="M-104,-122 L-30,-122 L-18,-108 L104,-108 L104,126 L-104,126 Z" fill="#D4BA8B" stroke="{INK_WARM}" stroke-width="1.6"/>')
            s.append(f'<text x="-94" y="-111" font-family="DejaVu Sans Mono, monospace" font-size="7.2" font-weight="bold" fill="#463724">{doc_id}</text>')
            # Thick Polaroid / File Card body
            s.append(f'<rect x="-98" y="-106" width="196" height="226" rx="2" fill="url(#{p}_card_paper)" stroke="{INK_WARM}" stroke-width="1.8"/>')
            # Photo well with portrait
            s.append(f'<g transform="translate(-75,-90)">{portrait_svg}</g>')
            s.append(f'<rect x="-75" y="-90" width="150" height="122" fill="none" stroke="{INK_WARM}" stroke-width="1.5"/>')
            # Subtle glossy polaroid corner reflection
            s.append('<polygon points="-74,-89 -24,-89 -74,-34" fill="#FFFFFF" opacity="0.14"/>')
            # Name, Role & Asset Lines (100% English)
            name_sz = 11.2 if len(name) > 16 else 13.0
            s.append(
                f'<text x="0" y="54" text-anchor="middle" font-family="DejaVu Sans, Arial, sans-serif" '
                f'font-size="{name_sz}" font-weight="bold" fill="#1B1917" letter-spacing="0.4">{name}</text>'
            )
            # Role pill badge
            s.append(f'<rect x="-66" y="62" width="132" height="20" rx="2" fill="{role_col}"/>')
            s.append(
                f'<text x="0" y="76" text-anchor="middle" font-family="DejaVu Sans Mono, monospace" '
                f'font-size="10.4" font-weight="bold" fill="#FFF8EE" letter-spacing="1.0">{role}</text>'
            )
            # Handwritten/typewriter asset line
            s.append('<path d="M-78,94 L78,94" fill="none" stroke="#B6A890" stroke-width="0.9"/>')
            s.append(
                f'<text x="0" y="108" text-anchor="middle" font-family="DejaVu Sans Mono, monospace" '
                f'font-size="8.2" font-weight="bold" fill="#3B352D">{asset_note}</text>'
            )
            # Red paperclip clipping photo top-right
            s.append(_red_paperclip(68, -98, rot=-8))
            s.append('</g>')

        # Dry-humor red ink rubber stamp slammed on bottom-right concrete & card corner: "LONG STORY."
        s.append(
            '<g transform="translate(768,476) rotate(-7.5)">'
            '<rect x="-126" y="-28" width="252" height="56" rx="4" fill="#F6EDE0" fill-opacity="0.72" stroke="#A81B20" stroke-width="3.6"/>'
            '<rect x="-120" y="-22" width="240" height="44" rx="2" fill="none" stroke="#A81B20" stroke-width="1.3" stroke-dasharray="6 2"/>'
            '<text x="0" y="10" text-anchor="middle" font-family="DejaVu Sans Mono, monospace" '
            'font-size="27" font-weight="bold" fill="#A81B20" letter-spacing="2.2">LONG STORY.</text>'
            '</g>'
        )

        # Small drafting pencil resting on lower-left concrete edge
        s.append(
            f'<g transform="translate(174,496) rotate(6)">'
            f'<rect x="-66" y="-4.5" width="112" height="9" rx="1" fill="#D9A338" stroke="{INK_WARM}" stroke-width="1.4"/>'
            f'<polygon points="46,-4.5 62,0 46,4.5" fill="#E8CFA6" stroke="{INK_WARM}" stroke-width="1.2"/>'
            f'<polygon points="56,-1.6 62,0 56,1.6" fill="#1A1715"/>'
            f'<rect x="-78" y="-4.5" width="12" height="9" fill="#B85656" stroke="{INK_WARM}" stroke-width="1.2"/>'
            f'</g>'
        )
        s.append('</g>')
        parts.append("".join(s))

    # -------------------------------------------------------------------------
    # LAYER 4: PLAN (#7FE6FF cyan analytical links connecting the 3 crew cards)
    # -------------------------------------------------------------------------
    if _katman_aktif(katmanlar, "plan"):
        pl: list[str] = ['<g id="s302-plan" opacity="0.90">']
        # Cyan tactical link chain across the 3 dossier cards
        pl.append(
            f'<path d="M276,274 L334,244 L388,266 M566,266 L618,244 L674,274" '
            f'fill="none" stroke="{PLAN}" stroke-width="1.8" stroke-dasharray="6 4" filter="url(#{p}_glow_cyan)"/>'
        )
        # Lower triangulation link from Abruzzi -> Sucre -> Westmoreland
        pl.append(
            f'<path d="M242,438 L474,468 L698,434" fill="none" stroke="{PLAN}" '
            f'stroke-width="1.3" stroke-dasharray="4 4" opacity="0.72"/>'
        )
        for nx, ny in [(276, 274), (388, 266), (566, 266), (674, 274), (474, 468)]:
            pl.append(f'<circle cx="{nx}" cy="{ny}" r="3.6" fill="{PLAN_CORE}" stroke="{PLAN}" stroke-width="1.2"/>')

        # Mini cyan node tags between cards
        for tx, ty, lbl in [(302, 224, "FLIGHT"), (586, 224, "FUNDING")]:
            pl.append(f'<rect x="{tx}" y="{ty}" width="66" height="17" rx="2" fill="#08131E" opacity="0.86" stroke="{PLAN}" stroke-width="0.9"/>')
            pl.append(
                f'<text x="{tx+33}" y="{ty+12}" text-anchor="middle" font-family="DejaVu Sans Mono, monospace" '
                f'font-size="8.6" font-weight="bold" fill="{PLAN_CORE}" letter-spacing="0.8">{lbl}</text>'
            )

        # Top-left CAD header badge (clear of right watchtower silhouette)
        pl.append(f'<rect x="24" y="18" width="248" height="28" rx="3" fill="#08131E" opacity="0.88" stroke="{PLAN}" stroke-width="1.2"/>')
        pl.append(
            f'<text x="148" y="36" text-anchor="middle" font-family="DejaVu Sans Mono, monospace" '
            f'font-size="11.2" font-weight="bold" fill="{PLAN_CORE}" letter-spacing="1.0">ESCAPE CREW · FOX RIVER YARD</text>'
        )
        pl.append('</g>')
        parts.append("".join(pl))

    # -------------------------------------------------------------------------
    # LAYER 5: ONPLAN (Sunlit dusty yard atmosphere, golden glare & vignette)
    # -------------------------------------------------------------------------
    if _katman_aktif(katmanlar, "onplan"):
        op: list[str] = ['<g id="s302-onplan">']
        op.append(f'<polygon points="0,0 520,0 260,540 0,540" fill="url(#{p}_sun_wash)"/>')
        for _ in range(30):
            dx = rng.uniform(30, 930)
            dy = rng.uniform(40, 500)
            dr = rng.uniform(0.9, 2.0)
            op.append(f'<circle cx="{dx:.1f}" cy="{dy:.1f}" r="{dr:.1f}" fill="#FFF1CE" opacity="{rng.uniform(0.20, 0.50):.2f}"/>')
        op.append(f'<rect x="0" y="0" width="960" height="540" fill="url(#{p}_vignette)"/>')
        op.append('</g>')
        parts.append("".join(op))

    return defs, "".join(parts)


# =============================================================================
# 3.03 · WARM INFIRMARY & SARA ("DAYS LEFT: 21")
# =============================================================================
def set_303_revir_sara(katmanlar: set[str] | list[str] | None = None) -> tuple[str, str]:
    """Warm amber Fox River Infirmary contrasting sharply against the prison's
    cold blue: glass-front medicine cabinet, insulin vials, patient file,
    examination table; center-foreground locked Sara v2 (K.sara_kafa 3q sefkat
    + lab coat + stethoscope + clipboard ALL in single `sahne` layer per R4);
    barless infirmary exit window behind her framed in #7FE6FF CAD lines;
    top-right 'DAYS LEFT: 21'."""
    rng = random.Random(303)
    p = _uid("s303")

    defs = f"""
    <linearGradient id="{p}_wall_warm" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#4A3524"/>
      <stop offset="46%" stop-color="#6A4D33"/>
      <stop offset="100%" stop-color="#3E2B1C"/>
    </linearGradient>
    <linearGradient id="{p}_wainscot" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#8A6E4E"/>
      <stop offset="100%" stop-color="#5B4631"/>
    </linearGradient>
    <linearGradient id="{p}_win_dusk" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#1E354D"/>
      <stop offset="52%" stop-color="#526C7D"/>
      <stop offset="100%" stop-color="#D99C5E"/>
    </linearGradient>
    <radialGradient id="{p}_amber_glow" cx="0.5" cy="0.4" r="0.62">
      <stop offset="0%" stop-color="#FFE09C" stop-opacity="0.52"/>
      <stop offset="48%" stop-color="#E59F47" stop-opacity="0.18"/>
      <stop offset="100%" stop-color="#9A5C1E" stop-opacity="0.0"/>
    </radialGradient>
    <linearGradient id="{p}_counter_steel" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#C8C4BA"/>
      <stop offset="42%" stop-color="#9B968B"/>
      <stop offset="100%" stop-color="#69635B"/>
    </linearGradient>
    <linearGradient id="{p}_coat" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F7F4EC"/>
      <stop offset="55%" stop-color="#E7E1D5"/>
      <stop offset="100%" stop-color="#C8BFA9"/>
    </linearGradient>
    <radialGradient id="{p}_vignette" cx="0.50" cy="0.48" r="0.72">
      <stop offset="50%" stop-color="#000000" stop-opacity="0.0"/>
      <stop offset="100%" stop-color="#180F08" stop-opacity="0.64"/>
    </radialGradient>
    <filter id="{p}_glow_cyan" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="2.6" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    """

    parts: list[str] = []

    # -------------------------------------------------------------------------
    # LAYER 1: UZAK (Warm amber infirmary walls, glass-front medicine cabinet,
    # BARLESS infirmary window overlooking dusk yard, warm wall sconce)
    # -------------------------------------------------------------------------
    if _katman_aktif(katmanlar, "uzak"):
        u: list[str] = ['<g id="s303-uzak">']
        u.append(f'<rect x="0" y="0" width="960" height="540" fill="url(#{p}_wall_warm)"/>')
        # Warm lower wainscot & wood chair rail
        u.append(f'<rect x="0" y="308" width="960" height="232" fill="url(#{p}_wainscot)"/>')
        u.append(f'<rect x="0" y="302" width="960" height="10" fill="#4C3622" stroke="{INK_WARM}" stroke-width="1.4"/>')

        # Warm ambient lamp pool radiating across infirmary wall
        u.append(f'<ellipse cx="460" cy="210" rx="380" ry="240" fill="url(#{p}_amber_glow)"/>')

        # Glass-front wooden medicine cabinet on left wall (x=42..268, y=54..284)
        u.append(f'<rect x="42" y="54" width="226" height="230" rx="3" fill="#543B27" stroke="{INK_WARM}" stroke-width="2.0"/>')
        u.append('<rect x="54" y="66" width="202" height="206" fill="#2F2117" stroke="#3B291B" stroke-width="1.2"/>')
        # Three shelves stocked with amber medicine bottles, gauze boxes & vials
        for sy_c in (132, 198, 264):
            u.append(f'<rect x="54" y="{sy_c}" width="202" height="7" fill="#7D5C3E" stroke="{INK_WARM}" stroke-width="1.0"/>')
            bx_m = 66
            for bw, bh, bcol in [(16, 36, "#9E5326"), (12, 28, "#E8DFCF"), (18, 40, "#6E381B"),
                                 (24, 24, "#D4C6AE"), (14, 34, "#B56A32"), (16, 32, "#4E6B7B"),
                                 (14, 30, "#9E5326"), (22, 26, "#E3D8C5")]:
                if bx_m + bw < 248:
                    u.append(f'<rect x="{bx_m}" y="{sy_c-bh}" width="{bw}" height="{bh}" rx="2" fill="{bcol}" stroke="{INK_WARM}" stroke-width="1.0"/>')
                    u.append(f'<rect x="{bx_m+2}" y="{sy_c-bh+8}" width="{bw-4}" height="8" fill="#F5EFE2" opacity="0.72"/>')
                    bx_m += bw + 7
        # Cabinet glass doors reflection & vertical divider
        u.append('<rect x="152" y="66" width="6" height="206" fill="#543B27" stroke="#211610" stroke-width="1.1"/>')
        u.append('<polygon points="56,68 122,68 56,192" fill="#FFE6B5" opacity="0.10"/>')
        u.append('<polygon points="160,68 228,68 160,186" fill="#FFE6B5" opacity="0.08"/>')
        # Small red medical cross emblem above cabinet
        u.append('<rect x="148" y="24" width="14" height="22" rx="1" fill="#B6362F" opacity="0.82"/>')
        u.append('<rect x="144" y="28" width="22" height="14" rx="1" fill="#B6362F" opacity="0.82"/>')

        # === BARLESS INFIRMARY WINDOW (right-back, x=594..882, y=68..264) ===
        # Deliberately ZERO iron bars — the key weak point in Michael's Escape Plan!
        wx, wy, ww, wh = 594, 68, 288, 196
        u.append(f'<rect x="{wx-8}" y="{wy-8}" width="{ww+16}" height="{wh+16}" rx="2" fill="#4A3422" stroke="{INK_WARM}" stroke-width="2.0"/>')
        u.append(f'<rect x="{wx}" y="{wy}" width="{ww}" height="{wh}" fill="url(#{p}_win_dusk)"/>')
        # Distant yard silhouette visible through barless dusk window
        u.append(f'<rect x="{wx}" y="{wy+146}" width="{ww}" height="50" fill="#2A2624" opacity="0.72"/>')
        u.append(f'<path d="M{wx},{wy+146} L{wx+ww},{wy+146}" fill="none" stroke="#F0B56E" stroke-width="1.4" opacity="0.55"/>')
        # Simple wooden cross sash ONLY (NO prison bars!)
        u.append(f'<rect x="{wx+ww//2-4}" y="{wy}" width="8" height="{wh}" fill="#593F2A" stroke="{INK_WARM}" stroke-width="1.2"/>')
        u.append(f'<rect x="{wx}" y="{wy+wh//2-4}" width="{ww}" height="8" fill="#593F2A" stroke="{INK_WARM}" stroke-width="1.2"/>')
        # Window sill
        u.append(f'<rect x="{wx-14}" y="{wy+wh}" width="{ww+28}" height="12" rx="2" fill="#7D5C3E" stroke="{INK_WARM}" stroke-width="1.6"/>')

        # Warm amber sconce lamp between cabinet and window (x=328, y=104)
        u.append(f'<rect x="316" y="88" width="24" height="36" rx="6" fill="#FFE6A8" stroke="{INK_WARM}" stroke-width="1.5"/>')
        u.append('<circle cx="328" cy="106" r="56" fill="#FFD37A" opacity="0.22"/>')

        u.append('</g>')
        parts.append("".join(u))

    # -------------------------------------------------------------------------
    # LAYER 2: ORTA (Infirmary counter with INSULIN vials, syringe tray,
    # patient file folder, and examination bed on right — NO Sara here per R4!)
    # -------------------------------------------------------------------------
    if _katman_aktif(katmanlar, "orta"):
        m: list[str] = ['<g id="s303-orta">']

        # Right-side infirmary examination table with crisp white paper roll
        m.append(f'<rect x="646" y="346" width="314" height="32" rx="6" fill="#ECE6DA" stroke="{INK_WARM}" stroke-width="1.8"/>')
        m.append(f'<rect x="654" y="376" width="306" height="44" fill="#6F533B" stroke="{INK_WARM}" stroke-width="1.8"/>')
        m.append(f'<rect x="676" y="420" width="14" height="120" fill="#463426" stroke="{INK_WARM}" stroke-width="1.6"/>')
        # Paper roll cylinder at head of exam table
        m.append(f'<ellipse cx="662" cy="360" rx="10" ry="14" fill="#FAF6EE" stroke="{INK_WARM}" stroke-width="1.4"/>')
        m.append('<path d="M676,356 L956,356" fill="none" stroke="#C8BFA9" stroke-width="1.1"/>')

        # Left-foreground stainless medical counter (x=0..336, y=360..540)
        m.append(f'<polygon points="0,362 326,374 348,540 0,540" fill="url(#{p}_counter_steel)" stroke="{INK_WARM}" stroke-width="2.0"/>')
        m.append('<path d="M0,364 L324,376" fill="none" stroke="#FFF3DA" stroke-width="1.8" opacity="0.62"/>')

        # Open Patient File Folder on counter ("PATIENT: SCOFIELD, M.")
        m.append(
            f'<g transform="translate(108,452) rotate(-6)">'
            f'<rect x="-78" y="-36" width="156" height="76" rx="2" fill="#D8BE92" stroke="{INK_WARM}" stroke-width="1.5"/>'
            f'<rect x="-70" y="-28" width="140" height="62" fill="#FAF5EA" stroke="#9C8768" stroke-width="0.9"/>'
            f'<text x="-62" y="-12" font-family="DejaVu Sans Mono, monospace" font-size="8.0" font-weight="bold" fill="#2A201A">INFIRMARY CHART</text>'
            f'<path d="M-62,-6 L60,-6" fill="none" stroke="#8C7A64" stroke-width="0.8"/>'
            f'<text x="-62" y="7" font-family="DejaVu Sans Mono, monospace" font-size="7.6" font-weight="bold" fill="#8C2323">SCOFIELD, MICHAEL</text>'
            f'<text x="-62" y="19" font-family="DejaVu Sans Mono, monospace" font-size="6.8" fill="#463D34">TYPE 1 · INSULIN DAILY</text>'
            f'</g>'
        )

        # Two detailed glass INSULIN vials & kidney tray on counter (x=216..292)
        m.append(f'<ellipse cx="256" cy="420" rx="52" ry="15" fill="#B8B4AC" stroke="{INK_WARM}" stroke-width="1.5"/>')
        m.append('<ellipse cx="256" cy="418" rx="44" ry="10" fill="#DCD8CE"/>')
        for vx, vy, vcap in [(226, 386, "#C45B3B"), (252, 390, "#4B86A8")]:
            m.append(f'<rect x="{vx}" y="{vy}" width="18" height="30" rx="3" fill="#E8F4FA" fill-opacity="0.85" stroke="{INK_WARM}" stroke-width="1.4"/>')
            m.append(f'<rect x="{vx+2}" y="{vy+12}" width="14" height="16" fill="#C9E6F2" opacity="0.72"/>')
            m.append(f'<rect x="{vx+1}" y="{vy+8}" width="16" height="12" fill="#FAF5EA" stroke="#8C7D68" stroke-width="0.7"/>')
            m.append(f'<text x="{vx+9}" y="{vy+16}" text-anchor="middle" font-family="DejaVu Sans Mono, monospace" font-size="4.4" font-weight="bold" fill="#241D18">INS</text>')
            m.append(f'<rect x="{vx+3}" y="{vy-5}" width="12" height="6" rx="1" fill="{vcap}" stroke="{INK_WARM}" stroke-width="1.1"/>')
        # Small clean syringe resting in tray
        m.append(f'<path d="M276,416 L300,404" fill="none" stroke="#E8F2F6" stroke-width="4.0" stroke-linecap="round"/>')
        m.append(f'<path d="M276,416 L300,404" fill="none" stroke="{INK_WARM}" stroke-width="1.2"/>')

        m.append('</g>')
        parts.append("".join(m))

    # -------------------------------------------------------------------------
    # LAYER 3: SAHNE (R4-PARALAKS LOCKED: Complete Locked Sara v2 — head, neck,
    # lab coat, petrol-blue scrub, stethoscope, arms, hands & medical clipboard
    # ALL inside this single `sahne` layer!)
    # -------------------------------------------------------------------------
    if _katman_aktif(katmanlar, "sahne"):
        s: list[str] = ['<g id="s303-sahne">']

        # === LOCKED SARA V2 (as_sara_v2.png proportions: slender 1.95x head_w -> shoulder_w ~194px!) ===
        # Collar-Over-Neck Z-Order: torso/scrub -> K.sara_kafa(boyun=True) -> coat lapels, stethoscope & hair tips on TOP!
        s.append('<g id="s303-sara">')
        # Slender white doctor lab coat torso & tailored sloping shoulders (x=372..564, NO bulky dome!)
        s.append(
            f'<path d="M396,304 L436,284 L500,284 L540,304 L544,540 L392,540 Z" '
            f'fill="url(#{p}_coat)" stroke="{INK}" stroke-width="2.2" stroke-linejoin="round"/>'
        )
        # Petrol-blue medical scrub V-neck undershirt (matches Sara v2 palette #4E6B7B!)
        s.append(f'<path d="M442,284 L468,388 L494,284 Z" fill="#4E6B7B" stroke="{INK}" stroke-width="1.7"/>')
        s.append(f'<path d="M452,290 L468,334 L484,290" fill="none" stroke="#364C58" stroke-width="2.0"/>')
        # Coat center seam & chest pocket with pen
        s.append(f'<path d="M468,390 L468,540" fill="none" stroke="{INK}" stroke-width="1.6"/>')
        s.append(f'<rect x="492" y="388" width="38" height="42" rx="2" fill="#EFEBE1" stroke="{INK}" stroke-width="1.35"/>')
        s.append(f'<path d="M504,376 L504,392" fill="none" stroke="#2D4A68" stroke-width="3.0" stroke-linecap="round"/>')

        # Sara's slender sleeves & anatomical hands holding an infirmary clipboard (continuous from shoulder seams!)
        s.append(
            f'<g id="s303-sara-arms">'
            # Left sleeve descending gracefully from x=396, y=304 to elbow then bending inward to clipboard
            f'<path d="M396,304 L374,322 Q364,404 374,458 L414,484 L424,458 Q396,436 398,386 L402,316 Z" '
            f'fill="#F2EFE7" stroke="{INK}" stroke-width="2.1" stroke-linejoin="round"/>'
            # Right sleeve descending gracefully from x=540, y=304 to elbow then bending inward to clipboard
            f'<path d="M540,304 L562,322 Q572,404 562,458 L522,484 L512,458 Q540,436 538,386 L534,316 Z" '
            f'fill="#DFD9CC" stroke="{INK}" stroke-width="2.1" stroke-linejoin="round"/>'
            # Clipboard held at waist level
            f'<g transform="translate(468,486) rotate(-3)">'
            f'<rect x="-52" y="-42" width="104" height="88" rx="4" fill="#6E4E34" stroke="{INK}" stroke-width="1.7"/>'
            f'<rect x="-45" y="-33" width="90" height="72" fill="#FAF6EE" stroke="#9C8C76" stroke-width="0.9"/>'
            f'<rect x="-18" y="-46" width="36" height="11" rx="2" fill="#A8B2BA" stroke="{INK}" stroke-width="1.2"/>'
            f'<path d="M-36,-18 L36,-18 M-36,-6 L28,-6 M-36,6 L34,6 M-36,18 L20,18" fill="none" stroke="#8C7E6C" stroke-width="1.1"/>'
            f'</g>'
            # Slender hands gripping sides of clipboard (tattoo-free, Sara skin tone #E8C1A6)
            f'<path d="M406,460 Q422,456 428,468 Q428,482 414,486 L402,478 Z" fill="#E8C1A6" stroke="{INK}" stroke-width="1.6"/>'
            f'<path d="M530,458 Q514,454 508,466 Q508,480 522,484 L534,476 Z" fill="#D9AF92" stroke="{INK}" stroke-width="1.6"/>'
            f'</g>'
        )

        # Warm amber rim light along Sara's slender left shoulder
        s.append('<path d="M376,320 L398,303 L436,285" fill="none" stroke="#FFE4A8" stroke-width="2.1" opacity="0.68" stroke-linecap="round"/>')

        # Locked K.sara_kafa (view="3q", ifade="sefkat", boyun=True)
        s.append(
            f'<g transform="translate(468,196) scale(0.84)">'
            f'{K.sara_kafa(view="3q", ifade="sefkat", look=0.22, boyun=True)}'
            f'</g>'
        )

        # COLLAR-OVER-NECK Z-ORDER: Structured lab coat lapels, stethoscope & tapered hair tips OVER neck base!
        s.append(f'<path d="M438,282 L416,338 L454,402 L468,386 L444,284 Z" fill="#F7F4EC" stroke="{INK}" stroke-width="1.8" stroke-linejoin="round"/>')
        s.append(f'<path d="M498,282 L520,338 L482,402 L468,386 L492,284 Z" fill="#DFD9CC" stroke="{INK}" stroke-width="1.8" stroke-linejoin="round"/>')
        # Detailed Stethoscope draped naturally around Sara's neck over lapels
        s.append(
            f'<g id="s303-stethoscope">'
            f'<path d="M440,282 Q418,342 434,418 Q440,438 448,444" fill="none" stroke="#252B31" stroke-width="5.6" stroke-linecap="round"/>'
            f'<path d="M440,282 Q418,342 434,418 Q440,438 448,444" fill="none" stroke="#4F5A66" stroke-width="1.4" opacity="0.65" stroke-linecap="round"/>'
            f'<path d="M496,282 Q518,338 508,408" fill="none" stroke="#252B31" stroke-width="5.6" stroke-linecap="round"/>'
            f'<path d="M496,282 Q518,338 508,408" fill="none" stroke="#4F5A66" stroke-width="1.4" opacity="0.65" stroke-linecap="round"/>'
            # Metal chestpiece diaphragm on left
            f'<circle cx="448" cy="448" r="11" fill="#C4CED6" stroke="{INK}" stroke-width="1.7"/>'
            f'<circle cx="448" cy="448" r="6.2" fill="#7A8793" stroke="{INK}" stroke-width="1.0"/>'
            # Metal binaural earpieces on right
            f'<path d="M508,408 L499,428 M508,408 L517,428" fill="none" stroke="#B8C4CE" stroke-width="2.8" stroke-linecap="round"/>'
            f'<circle cx="499" cy="430" r="3.2" fill="#252B31" stroke="{INK}" stroke-width="1.0"/>'
            f'<circle cx="517" cy="430" r="3.2" fill="#252B31" stroke="{INK}" stroke-width="1.0"/>'
            f'</g>'
        )
        # Tapered chestnut-auburn hair tips falling softly over coat collar (matches as_sara_v2.png!)
        s.append(f'<path d="M412,268 Q410,296 420,318 Q428,298 426,272 Z" fill="#733726" stroke="{INK}" stroke-width="1.5" stroke-linejoin="round"/>')
        s.append(f'<path d="M518,266 Q522,294 510,314 Q504,294 506,270 Z" fill="#5D2A1D" stroke="{INK}" stroke-width="1.5" stroke-linejoin="round"/>')
        s.append('</g>')

        s.append('</g>')
        parts.append("".join(s))

    # -------------------------------------------------------------------------
    # LAYER 4: PLAN (#7FE6FF CAD exit frame highlighting the BARLESS infirmary
    # window behind Sara + top-right "DAYS LEFT: 21")
    # -------------------------------------------------------------------------
    if _katman_aktif(katmanlar, "plan"):
        pl: list[str] = ['<g id="s303-plan" opacity="0.92">']
        wx, wy, ww, wh = 594, 68, 288, 196
        # Glowing cyan CAD frame around barless exit window
        pl.append(
            f'<rect x="{wx-3}" y="{wy-3}" width="{ww+6}" height="{wh+6}" fill="none" '
            f'stroke="{PLAN}" stroke-width="2.0" stroke-dasharray="10 5" filter="url(#{p}_glow_cyan)"/>'
        )
        # Sharp CAD corner brackets
        pl.append(
            f'<path d="M{wx-12},{wy+16} L{wx-12},{wy-12} L{wx+16},{wy-12} '
            f'M{wx+ww+12},{wy+16} L{wx+ww+12},{wy-12} L{wx+ww-16},{wy-12} '
            f'M{wx-12},{wy+wh-16} L{wx-12},{wy+wh+12} L{wx+16},{wy+wh+12} '
            f'M{wx+ww+12},{wy+wh-16} L{wx+ww+12},{wy+wh+12} L{wx+ww-16},{wy+wh+12}" '
            f'fill="none" stroke="{PLAN_CORE}" stroke-width="1.6"/>'
        )
        # Diagonal CAD exit arrow pointing out the barless window
        pl.append(f'<path d="M686,216 L792,134" fill="none" stroke="{PLAN}" stroke-width="2.0" filter="url(#{p}_glow_cyan)"/>')
        pl.append(f'<path d="M778,134 L792,134 L788,148" fill="none" stroke="{PLAN_CORE}" stroke-width="2.0" stroke-linecap="round" stroke-linejoin="round"/>')

        # Clean CAD label below window
        pl.append(f'<rect x="632" y="284" width="212" height="22" rx="3" fill="#08131E" opacity="0.88" stroke="{PLAN}" stroke-width="1.1"/>')
        pl.append(
            f'<text x="738" y="299" text-anchor="middle" font-family="DejaVu Sans Mono, monospace" '
            f'font-size="10.2" font-weight="bold" fill="{PLAN_CORE}" letter-spacing="0.9">NO BARS · EXIT WINDOW</text>'
        )

        # Top-right DAYS LEFT: 21 counter
        pl.append(_hud_days_left(754, 16, 21))
        pl.append('</g>')
        parts.append("".join(pl))

    # -------------------------------------------------------------------------
    # LAYER 5: ONPLAN (Warm golden infirmary light haze, dust motes, dark door
    # jamb foreground edge & warm cinematic vignette)
    # -------------------------------------------------------------------------
    if _katman_aktif(katmanlar, "onplan"):
        op: list[str] = ['<g id="s303-onplan">']
        # Subtle dark infirmary door jamb on far left edge
        op.append('<rect x="0" y="0" width="18" height="540" fill="#1C130C" opacity="0.72"/>')
        # Warm golden dust motes floating in amber infirmary light
        for _ in range(28):
            dx = rng.uniform(120, 860)
            dy = rng.uniform(50, 470)
            dr = rng.uniform(0.9, 2.0)
            op.append(f'<circle cx="{dx:.1f}" cy="{dy:.1f}" r="{dr:.1f}" fill="#FFE7AE" opacity="{rng.uniform(0.20, 0.52):.2f}"/>')
        op.append(f'<rect x="0" y="0" width="960" height="540" fill="url(#{p}_vignette)"/>')
        op.append('</g>')
        parts.append("".join(op))

    return defs, "".join(parts)


# =============================================================================
# RENDERING & PRESENTATION CARDS (100% ENGLISH)
# =============================================================================
def _render_scene(scene_fn, scale: float = 2.0) -> Image.Image:
    defs, body = scene_fn()
    w = int(W_SCENE * scale)
    h = int(H_SCENE * scale)
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {W_SCENE} {H_SCENE}">'
        f'<defs>{defs}</defs>{body}</svg>'
    )
    png_bytes = resvg_py.svg_to_bytes(svg_string=svg)
    return Image.open(io.BytesIO(png_bytes)).convert("RGBA")


def _load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = (
        ["C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf", "C:/Windows/Fonts/calibrib.ttf"]
        if bold else
        ["C:/Windows/Fonts/segoeui.ttf", "C:/Windows/Fonts/arial.ttf", "C:/Windows/Fonts/calibri.ttf"]
    )
    for fp in candidates:
        if Path(fp).exists():
            return ImageFont.truetype(fp, size)
    return ImageFont.load_default()


def _draw_card_bg(w: int, h: int) -> Image.Image:
    bg = Image.new("RGBA", (w, h), (10, 16, 25, 255))
    d = ImageDraw.Draw(bg)
    for gx in range(0, w, 32):
        d.line((gx, 0, gx, h), fill=(18, 28, 42, 255), width=1)
    for gy in range(0, h, 32):
        d.line((0, gy, w, gy), fill=(18, 28, 42, 255), width=1)
    return bg


def _draw_panel_box(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int]) -> None:
    draw.rounded_rectangle(box, radius=8, fill=(14, 22, 34, 240), outline=(36, 55, 78, 255), width=1)


def _draw_swatches(draw: ImageDraw.ImageDraw, x: int, y: int, colors: list[str], size: int = 18, gap: int = 6) -> None:
    cx = x
    for col in colors:
        draw.rounded_rectangle((cx, y, cx + size, y + size), radius=3, fill=col, outline="#4B6682", width=1)
        cx += size + gap


def uret_kartlar(versiyon: str = "v1") -> tuple[Path, Path]:
    img_301 = _render_scene(set_301_ziyaret_cami, scale=2.0)   # 1920x1080
    img_302 = _render_scene(set_302_ekip_kartlari, scale=2.0)  # 1920x1080
    img_303 = _render_scene(set_303_revir_sara, scale=2.0)     # 1920x1080

    f_title = _load_font(19, bold=True)
    f_sub = _load_font(11, bold=False)
    f_card_t = _load_font(13, bold=True)
    f_card_s = _load_font(11, bold=False)
    f_small = _load_font(10, bold=False)

    # =========================================================================
    # OUTPUT 1: SET PRESENTATION CARD (1280 x 720 — 100% ENGLISH, 3 ROWS)
    # =========================================================================
    canvas = _draw_card_bg(1280, 720)
    draw = ImageDraw.Draw(canvas)

    draw.text((24, 11), "MICHAEL SCOFIELD  ·  ACT III SCENE SETS (3.01 – 3.03)", fill="#EBF3FA", font=f_title)
    draw.text((24, 35), "STYLE B+A HYBRID (CINEMATIC 2D + CYAN PLAN VISION)  ·  5-LAYER PARALLAX SETS (960×540)  ·  R4-PARALAKS LOCKED",
              fill="#7E97B0", font=f_sub)
    top_swatches = [("#192836", "GLASS"), ("#B9B0A0", "YARD"), ("#A81B20", "STAMP"),
                    ("#E59F47", "INFIRM"), ("#7FE6FF", "PLAN")]
    sx_top = 860
    for col, lbl in top_swatches:
        draw.rounded_rectangle((sx_top, 15, sx_top + 13, 28), radius=3, fill=col, outline="#3B536D", width=1)
        draw.text((sx_top + 18, 15), lbl, fill="#9BB2C8", font=f_small)
        sx_top += 80
    draw.line((24, 52, 1256, 52), fill="#213247", width=1)

    rows = [
        (
            60, img_301, "#7FE6FF", "#3A5A74",
            "3.01 · VISITING GLASS", "Act III · \"GETTING YOU OUT\" / DAYS LEFT: 29",
            ["#192836", "#5E7E9F", "#DDF6FF", "#FFCA7A", "#243342", "#7FE6FF"],
            [
                "• Scratched acrylic glass, steel frame & voice grille",
                "• Locked Michael v3 parting blue shirt (glowing tattoo)",
                "• Locked Lincoln v1 pressing tattoo-free palm on glass",
                "• Cold fluorescent overhead vs. warm reflection",
                "• Top-right CAD countdown: DAYS LEFT: 29",
            ],
            "R4-PARALAKS & R3 LOCKED",
            "Lincoln + palm + glass + Michael all live\nin single `s301-sahne` layer (zero drift).\nLincoln's forearm/palm are tattoo-free (R3).",
            "LAYERS: s301-uzak · orta · sahne · plan · onplan",
        ),
        (
            278, img_302, "#F2AE57", "#6B5E4D",
            "3.02 · YARD CREW CARDS", "Act III · \"LONG STORY.\"",
            ["#8AA8BE", "#B9B0A0", "#FAF6EC", "#C8262B", "#8B5A1B", "#7FE6FF"],
            [
                "• Sunlit Fox River concrete yard table & watchtower",
                "• 3 dossier polaroids: Abruzzi, Sucre, Westmoreland",
                "• Glossy red paperclips & manila Fox River file tabs",
                "• Dry-humor red rubber stamp: LONG STORY.",
                "• Cyan tactical link nodes: FLIGHT & FUNDING",
            ],
            "R1 ARCHETYPE PORTRAITS",
            "Original 2D stylized portraits only (no\nactor likeness). 100% English diegetic\nlabels, roles, and Fox River doc IDs.",
            "LAYERS: s302-uzak · orta · sahne · plan · onplan",
        ),
        (
            496, img_303, "#F6C367", "#7D5C3E",
            "3.03 · WARM INFIRMARY & SARA", "Act III · DAYS LEFT: 21",
            ["#4A3524", "#E59F47", "#F7F4EC", "#4E6B7B", "#9E5326", "#7FE6FF"],
            [
                "• Warm amber infirmary breaking cold prison palette",
                "• Locked Sara v2 (sefkat) + lab coat + stethoscope",
                "• Insulin vials, patient chart & examination table",
                "• Barless exit window framed in #7FE6FF CAD lines",
                "• Top-right CAD countdown: DAYS LEFT: 21",
            ],
            "R4-PARALAKS & CONTINUITY",
            "Sara v2 head, neck, coat, stethoscope,\nhands & clipboard live strictly in single\n`s303-sahne` layer. Barless exit highlighted.",
            "LAYERS: s303-uzak · orta · sahne · plan · onplan",
        ),
    ]

    for y0, img_s, tcol, bcol, title, sub, sw, bullets, rhead, rbody, lyr_txt in rows:
        _draw_panel_box(draw, (22, y0, 1258, y0 + 210))
        thumb = img_s.resize((320, 180), Image.Resampling.LANCZOS)
        canvas.paste(thumb, (32, y0 + 22), thumb)
        draw.rectangle((32, y0 + 22, 352, y0 + 202), outline=bcol, width=1)
        draw.text((32, y0 + 4), title, fill=tcol, font=f_card_t)
        draw.text((248, y0 + 6), sub, fill="#9DB0C4", font=f_small)

        rx = 368
        draw.text((rx, y0 + 22), "PALETTE", fill=tcol, font=f_small)
        _draw_swatches(draw, rx + 54, y0 + 18, sw, size=18, gap=6)
        draw.text((rx, y0 + 44), "KEY ELEMENTS (5)", fill="#9BB2C8", font=f_small)
        for bi, btxt in enumerate(bullets):
            draw.text((rx, y0 + 60 + bi * 22), btxt, fill="#E3ECF5", font=f_card_s)
        draw.text((rx, y0 + 184), lyr_txt, fill="#8AA3BC", font=f_small)

        draw.line((888, y0 + 18, 888, y0 + 196), fill="#233447", width=1)
        tx = 906
        draw.text((tx, y0 + 22), rhead, fill="#7FE6FF", font=f_card_t)
        draw.text((tx, y0 + 48), rbody, fill="#C5D5E4", font=f_card_s)

    out_main = OUT_DIR / f"b3_set_ziyaret_revir_{versiyon}.png"
    canvas.convert("RGB").save(out_main, quality=95)

    # =========================================================================
    # OUTPUT 2: R13 200% CROP QUALITY AUDIT CARD (1280 x 720 — 4 PANELS)
    # =========================================================================
    r13 = _draw_card_bg(1280, 720)
    d13 = ImageDraw.Draw(r13)
    d13.text((24, 13), "R13 · 200% ZOOM QUALITY AUDIT (ACT III: 3.01 – 3.03 SETS)", fill="#EBF3FA", font=f_title)
    d13.text((24, 37), "1:1 PIXEL CROPS FROM 1920×1080 RENDERS  ·  MICHAEL TATTOO, LINCOLN PALM (R3), CREW CARDS & SARA V2 INFIRMARY",
             fill="#7E97B0", font=f_sub)
    d13.line((24, 55, 1256, 55), fill="#213247", width=1)

    cw, ch = 600, 264
    crops = [
        (img_301, (388, 690), "1 · 3.01 HIGH-DETAIL CHEST & FOREARM FILIGREE TATTOO (200%)",
         "Gothic arch reliefs, twin crane wings, filigree scrollwork & glowing cyan plan", (22, 66)),
        (img_301, (1240, 440), "2 · 3.01 LOCKED LINCOLN V1 + TATTOO-FREE PALM ON GLASS (R3) (200%)",
         "Wider jaw/stubble contrast vs. Michael, clean palm on glass & speaker grille", (652, 66)),
        (img_302, None, "3 · 3.02 CREW PORTRAITS: ABRUZZI · SUCRE · WESTMORELAND (200%)",
         "Split 1:1 crop: Abruzzi (L) · Sucre (C) · Westmoreland (R) — R1 stylized 2D", (22, 392)),
        (img_303, (1120, 505), "4 · 3.03 LOCKED SARA V2 (SEFKAT) + COLLAR-OVER-NECK & BARLESS WINDOW (200%)",
         "Slender Sara v2 coat/collar/stethoscope fit & cyan barless exit window", (652, 392)),
    ]

    for src_img, center, title, sub, (bx, by) in crops:
        _draw_panel_box(d13, (bx, by, bx + 606, by + 314))
        if center is None:
            # 3-way 1:1 200% portrait split for Abruzzi (left), Sucre (mid), Westmoreland (right)
            pw = 198
            centers_302 = [(368, 610), (948, 594), (1532, 610)]
            for idx_p, (pcx, pcy) in enumerate(centers_302):
                px0 = max(0, min(src_img.width - pw, pcx - pw // 2))
                py0 = max(0, min(src_img.height - ch, pcy - ch // 2))
                p_img = src_img.crop((px0, py0, px0 + pw, py0 + ch))
                r13.paste(p_img, (bx + 3 + idx_p * (pw + 3), by + 44), p_img)
                if idx_p > 0:
                    d13.line((bx + 3 + idx_p * (pw + 3) - 2, by + 44, bx + 3 + idx_p * (pw + 3) - 2, by + 44 + ch), fill="#7FE6FF", width=2)
        else:
            cx, cy = center
            x0 = max(0, min(src_img.width - cw, cx - cw // 2))
            y0 = max(0, min(src_img.height - ch, cy - ch // 2))
            patch = src_img.crop((x0, y0, x0 + cw, y0 + ch))
            r13.paste(patch, (bx + 3, by + 44), patch)
        d13.rectangle((bx + 3, by + 44, bx + 3 + cw, by + 44 + ch), outline="#2F465E", width=1)
        d13.text((bx + 12, by + 8), title, fill="#7FE6FF", font=f_card_t)
        d13.text((bx + 12, by + 25), sub, fill="#96AEC6", font=f_small)

    out_r13 = OUT_DIR / "b3_set_ziyaret_revir_r13.png"
    r13.convert("RGB").save(out_r13, quality=95)
    print(f"Saved:\n  - {out_main}\n  - {out_r13}")
    return out_main, out_r13


if __name__ == "__main__":
    uret_kartlar("v1")
