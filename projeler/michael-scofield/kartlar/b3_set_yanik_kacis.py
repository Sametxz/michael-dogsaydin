"""V9 (Act III: Scorched Tattoo, Unlocked Infirmary Door, Escape Cable & Manhunt).

Style B+A Hybrid (Cinematic 2D + Cyan Blueprint Vision) — 5-layer parallax-ready scenes (960x540):
  - set_307_yanik_dovme(katmanlar=None)    -> (defs_str, body_str)
  - set_308_acik_kapi(katmanlar=None)      -> (defs_str, body_str)
  - set_309_kablo_kacisi(katmanlar=None)   -> (defs_str, body_str)
  - set_310_pist_insan_avi(katmanlar=None) -> (defs_str, body_str)

All on-screen text is 100% ENGLISH. Every stroked <path> explicitly specifies fill="none".
R4-PARALLAX STRICT: Every character's full anatomy + held/contacted object lives in a single `sahne` layer.
Uses locked assets from karakter.py (K.michael_sirt_dovme, K.sara_figur) without modifying karakter.py.
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
PLAN_CORE = "#DDFBFF"
EMBER = "#FF7A24"
EMBER_HOT = "#FFD07A"
AMBER_GOLD = "#F5C26B"
RED_ALERT = "#E63244"
SIREN_BLUE = "#2E8CFF"
SIREN_RED = "#FF2E48"

_UID = 0


def _uid(prefix: str = "b3") -> str:
    global _UID
    _UID += 1
    return f"{prefix}_{_UID}"


def _katman_aktif(katmanlar: set[str] | list[str] | None, ad: str) -> bool:
    return katmanlar is None or ad in katmanlar


# =============================================================================
# SCENE 3.07: SCORCHED TATTOO & CAD REBUILD ("REBUILT · 3 DAYS LEFT")
# =============================================================================
def set_307_yanik_dovme(
    katmanlar: set[str] | list[str] | None = None,
) -> tuple[str, str]:
    """Locked A-Sirt v1 (K.michael_sirt_dovme(plan_glow=0.6)) with a glowing ember-orange
    burn ring erasing a critical tattoo section (zero blood/gore, only warm glowing ember
    rim and subtle wisps of smoke), and a floating #7FE6FF cyan CAD puzzle piece rebuilding
    the missing corridor segment right above it ('REBUILT · 3 DAYS LEFT').
    """
    rng = random.Random(307)
    p = _uid("s307")

    sirt_defs, sirt_body = K.michael_sirt_dovme(plan_glow=0.6)

    defs = f"""
    {sirt_defs}
    <linearGradient id="{p}_bg_wall" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#080F18"/>
      <stop offset="48%" stop-color="#101B29"/>
      <stop offset="100%" stop-color="#070C14"/>
    </linearGradient>
    <radialGradient id="{p}_moon_pool" cx="0.32" cy="0.22" r="0.56">
      <stop offset="0%" stop-color="#3B6288" stop-opacity="0.32"/>
      <stop offset="60%" stop-color="#16283D" stop-opacity="0.12"/>
      <stop offset="100%" stop-color="#080F18" stop-opacity="0.0"/>
    </radialGradient>
    <radialGradient id="{p}_ember_ambient" cx="0.46" cy="0.56" r="0.38">
      <stop offset="0%" stop-color="#FF7A24" stop-opacity="0.30"/>
      <stop offset="52%" stop-color="#C84A12" stop-opacity="0.11"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.0"/>
    </radialGradient>
    <radialGradient id="{p}_burn_void" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0%" stop-color="#2D1D17" stop-opacity="0.96"/>
      <stop offset="58%" stop-color="#4A2718" stop-opacity="0.92"/>
      <stop offset="82%" stop-color="#D95D1E" stop-opacity="0.95"/>
      <stop offset="93%" stop-color="#FFB85C" stop-opacity="0.92"/>
      <stop offset="100%" stop-color="#FF6A1A" stop-opacity="0.0"/>
    </radialGradient>
    <radialGradient id="{p}_burn_halo" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0%" stop-color="#FFB85C" stop-opacity="0.55"/>
      <stop offset="48%" stop-color="#FF6A1A" stop-opacity="0.28"/>
      <stop offset="100%" stop-color="#FF6A1A" stop-opacity="0.0"/>
    </radialGradient>
    <linearGradient id="{p}_smoke_g" x1="0" y1="1" x2="0" y2="0">
      <stop offset="0%" stop-color="#B9C4D0" stop-opacity="0.28"/>
      <stop offset="55%" stop-color="#96A8BC" stop-opacity="0.14"/>
      <stop offset="100%" stop-color="#7E93A8" stop-opacity="0.0"/>
    </linearGradient>
    <linearGradient id="{p}_holo_beam" x1="0" y1="1" x2="1" y2="0">
      <stop offset="0%" stop-color="{PLAN}" stop-opacity="0.30"/>
      <stop offset="55%" stop-color="{PLAN}" stop-opacity="0.12"/>
      <stop offset="100%" stop-color="{PLAN}" stop-opacity="0.04"/>
    </linearGradient>
    <linearGradient id="{p}_puzzle_fill" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#10364D" stop-opacity="0.88"/>
      <stop offset="100%" stop-color="#071B2A" stop-opacity="0.92"/>
    </linearGradient>
    <radialGradient id="{p}_cad_glow" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0%" stop-color="{PLAN}" stop-opacity="0.36"/>
      <stop offset="60%" stop-color="{PLAN}" stop-opacity="0.10"/>
      <stop offset="100%" stop-color="{PLAN}" stop-opacity="0.0"/>
    </radialGradient>
    <radialGradient id="{p}_vig" cx="0.5" cy="0.5" r="0.72">
      <stop offset="52%" stop-color="#000000" stop-opacity="0.0"/>
      <stop offset="100%" stop-color="#03060B" stop-opacity="0.72"/>
    </radialGradient>
    <filter id="{p}_glow_cyan" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="3.2" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="{p}_glow_ember" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="4.5" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    """

    parts: list[str] = []

    # ── LAYER 1: uzak (Cold Fox River concrete block wall + subtle architectural grid) ──
    if _katman_aktif(katmanlar, "uzak"):
        uzak: list[str] = ['<g id="s307-uzak">']
        uzak.append(f'<rect x="0" y="0" width="960" height="540" fill="url(#{p}_bg_wall)"/>')
        uzak.append(f'<rect x="0" y="0" width="960" height="540" fill="url(#{p}_moon_pool)"/>')
        uzak.append(f'<rect x="0" y="0" width="960" height="540" fill="url(#{p}_ember_ambient)"/>')
        # Subtle concrete cinderblock seams
        for row in range(0, 540, 48):
            uzak.append(f'<line x1="0" y1="{row}" x2="960" y2="{row}" stroke="#1E3044" stroke-width="1" opacity="0.28"/>')
            off = 0 if (row // 48) % 2 == 0 else 48
            for col in range(off, 960, 96):
                uzak.append(f'<line x1="{col}" y1="{row}" x2="{col}" y2="{row + 48}" stroke="#1E3044" stroke-width="1" opacity="0.22"/>')
        # Faint blueprint coordinate grid on right side
        for gx in range(520, 960, 32):
            uzak.append(f'<line x1="{gx}" y1="0" x2="{gx}" y2="540" stroke="{PLAN}" stroke-width="0.6" opacity="0.09"/>')
        for gy in range(0, 540, 32):
            uzak.append(f'<line x1="520" y1="{gy}" x2="960" y2="{gy}" stroke="{PLAN}" stroke-width="0.6" opacity="0.09"/>')
        uzak.append("</g>")
        parts.append("\n".join(uzak))

    # ── LAYER 2: orta (Cell bar light cast + ambient pipe silhouette) ──
    if _katman_aktif(katmanlar, "orta"):
        orta: list[str] = ['<g id="s307-orta">']
        # Diagonal cell bar shadows on left wall
        for bx in range(36, 220, 36):
            orta.append(
                f'<polygon points="{bx},0 {bx + 14},0 {bx - 36},540 {bx - 50},540" '
                f'fill="#04080E" opacity="0.34"/>'
            )
        # Distant steam pipe silhouette on far left (story motif of the burn)
        orta.append('<rect x="34" y="0" width="22" height="540" fill="#15202C" opacity="0.55"/>')
        orta.append('<rect x="40" y="0" width="5" height="540" fill="#2A3E54" opacity="0.35"/>')
        for fy in (110, 290, 460):
            orta.append(f'<rect x="28" y="{fy}" width="34" height="10" rx="2" fill="#1D2B3A" opacity="0.62"/>')
        orta.append("</g>")
        parts.append("\n".join(orta))

    # ── LAYER 3: sahne (Locked A-Sirt v1 + scorched ember burn ring & smoke wisps) ──
    if _katman_aktif(katmanlar, "sahne"):
        sahne: list[str] = ['<g id="s307-sahne">']
        # Locked A-Sirt v1 placed on center-left, entire torso+head+tattoo in single sahne layer
        sahne.append('<g transform="translate(340, 332) scale(0.76)">')
        sahne.append(sirt_body)
        # Scorched burn ring on right-upper back (erasing Node 02 area, zero blood/gore)
        # Center around local (82, 16) -> screen ~(402, 344)
        sahne.append(f'<circle cx="82" cy="18" r="78" fill="url(#{p}_burn_halo)"/>')
        # Organic scorched void (covers tattoo ink cleanly in that ring)
        burn_shape = (
            "M 82,-34 C 110,-36 134,-18 136,12 C 138,44 116,66 84,68 "
            "C 50,70 28,48 26,18 C 24,-14 48,-32 82,-34 Z"
        )
        sahne.append(f'<path d="{burn_shape}" fill="url(#{p}_burn_void)"/>')
        # Subtle seared skin texture inside void (clean amber-charcoal, no gore)
        sahne.append(
            '<path d="M 52,8 C 68,-6 96,-4 110,14 C 98,34 68,36 52,18 Z" '
            'fill="#2A1912" opacity="0.55"/>'
        )
        # Glowing ember-orange burn ring rim
        sahne.append(
            f'<path d="{burn_shape}" fill="none" stroke="{EMBER}" stroke-width="4.2" '
            f'filter="url(#{p}_glow_ember)" opacity="0.95"/>'
        )
        sahne.append(
            f'<path d="{burn_shape}" fill="none" stroke="{EMBER_HOT}" stroke-width="1.6" '
            f'stroke-dasharray="14 6 5 8" opacity="0.92"/>'
        )
        # Inner hairline ember crackles
        sahne.append(
            f'<path d="M 46,-10 Q 64,-22 88,-20 M 118,4 Q 124,26 106,46 M 44,36 Q 66,54 96,50" '
            f'fill="none" stroke="{EMBER_HOT}" stroke-width="1.3" opacity="0.72"/>'
        )
        # Subtle rising smoke wisps from the scorched ring
        for idx, sx in enumerate((56, 82, 108)):
            sw = 18 + idx * 4
            sahne.append(
                f'<path d="M {sx},-26 C {sx - sw},-74 {sx + sw},-118 {sx - 8},-172 '
                f'C {sx - 18},-206 {sx + 14},-236 {sx + 4},-268" '
                f'fill="none" stroke="url(#{p}_smoke_g)" stroke-width="{12 - idx * 2}" '
                f'stroke-linecap="round"/>'
            )
        sahne.append("</g>")
        sahne.append("</g>")
        parts.append("\n".join(sahne))

    # ── LAYER 4: plan (Floating #7FE6FF CAD puzzle piece rebuilding the missing section) ──
    if _katman_aktif(katmanlar, "plan"):
        plan: list[str] = ['<g id="s307-plan">']
        # Projection cone from scorched void (402, 344) to floating CAD puzzle module (690, 210)
        plan.append(
            f'<polygon points="366,318 438,370 842,306 562,118" fill="url(#{p}_holo_beam)"/>'
        )
        plan.append(
            f'<line x1="366" y1="318" x2="562" y2="118" stroke="{PLAN}" stroke-width="1.2" '
            f'stroke-dasharray="5 5" opacity="0.65"/>'
        )
        plan.append(
            f'<line x1="438" y1="370" x2="842" y2="306" stroke="{PLAN}" stroke-width="1.2" '
            f'stroke-dasharray="5 5" opacity="0.65"/>'
        )
        # Missing-sector cyan target ring around the burn
        plan.append(
            f'<circle cx="402" cy="346" r="52" fill="none" stroke="{PLAN}" stroke-width="1.4" '
            f'stroke-dasharray="6 4" opacity="0.88"/>'
        )
        plan.append(
            f'<path d="M 402,286 L 402,298 M 402,394 L 402,406 M 342,346 L 354,346 M 450,346 L 462,346" '
            f'fill="none" stroke="{PLAN}" stroke-width="1.6" opacity="0.9"/>'
        )
        # Floating cyan glow behind puzzle module
        plan.append(f'<ellipse cx="705" cy="215" rx="185" ry="125" fill="url(#{p}_cad_glow)"/>')

        # Interlocking CAD puzzle piece shape (top/left/right/bottom tabs)
        puzzle_d = (
            "M 575,122 L 664,122 "
            "C 664,104 682,94 700,94 C 718,94 736,104 736,122 "
            "L 832,122 L 832,188 "
            "C 850,188 860,204 860,220 C 860,236 850,252 832,252 "
            "L 832,306 L 736,306 "
            "C 736,290 718,280 700,280 C 682,280 664,290 664,306 "
            "L 575,306 L 575,248 "
            "C 592,248 602,234 602,216 C 602,198 592,184 575,184 Z"
        )
        plan.append(
            f'<path d="{puzzle_d}" fill="url(#{p}_puzzle_fill)" stroke="{PLAN}" '
            f'stroke-width="2.4" filter="url(#{p}_glow_cyan)"/>'
        )
        plan.append(
            f'<path d="{puzzle_d}" fill="none" stroke="{PLAN_CORE}" stroke-width="1.0" opacity="0.85"/>'
        )

        # Internal CAD blueprint grid & rebuilt escape corridor inside puzzle piece
        for ix in range(600, 825, 25):
            plan.append(f'<line x1="{ix}" y1="132" x2="{ix}" y2="296" stroke="{PLAN}" stroke-width="0.6" opacity="0.22"/>')
        for iy in range(140, 295, 25):
            plan.append(f'<line x1="585" y1="{iy}" x2="822" y2="{iy}" stroke="{PLAN}" stroke-width="0.6" opacity="0.22"/>')

        # Rebuilt pipe & corridor route inside puzzle piece
        rebuilt_route = "M 604,258 L 656,258 L 656,196 L 738,196 L 738,154 L 802,154"
        plan.append(
            f'<path d="{rebuilt_route}" fill="none" stroke="{PLAN}" stroke-width="4.2" '
            f'stroke-linecap="round" stroke-linejoin="round" filter="url(#{p}_glow_cyan)"/>'
        )
        plan.append(
            f'<path d="{rebuilt_route}" fill="none" stroke="{PLAN_CORE}" stroke-width="1.6" '
            f'stroke-linecap="round" stroke-linejoin="round"/>'
        )
        # Junction nodes inside puzzle
        for nx, ny, lbl in ((656, 196, "02-A"), (738, 196, "PIPE"), (802, 154, "INF")):
            plan.append(f'<circle cx="{nx}" cy="{ny}" r="6" fill="#071B2A" stroke="{PLAN}" stroke-width="2"/>')
            plan.append(f'<circle cx="{nx}" cy="{ny}" r="2.2" fill="{PLAN_CORE}"/>')
            plan.append(
                f'<text x="{nx}" y="{ny - 11}" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif" '
                f'font-size="9" font-weight="700" fill="{PLAN_CORE}">{lbl}</text>'
            )

        # Architectural gothic arch micro-motif inside puzzle (echoing back tattoo)
        plan.append(
            f'<path d="M 678,274 L 678,224 Q 700,198 722,224 L 722,274" '
            f'fill="none" stroke="{PLAN}" stroke-width="1.1" stroke-dasharray="3 3" opacity="0.68"/>'
        )

        # Vector snap arrow showing puzzle drops into burn gap
        plan.append(
            f'<path d="M 566,262 C 510,278 482,302 454,326" fill="none" stroke="{PLAN}" '
            f'stroke-width="2.0" stroke-dasharray="6 4"/>'
        )
        plan.append(f'<polygon points="446,333 460,330 453,318" fill="{PLAN}"/>')

        # Labels & HUD badges (100% English)
        plan.append(
            f'<text x="575" y="88" font-family="Segoe UI, Arial, sans-serif" font-size="10" '
            f'font-weight="700" letter-spacing="1.4" fill="{PLAN}">MEMORY CAD // PIECE #02</text>'
        )
        plan.append(
            f'<text x="402" y="424" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif" '
            f'font-size="10" font-weight="700" letter-spacing="1.2" fill="{EMBER_HOT}">SCORCHED SECTOR · GAP</text>'
        )

        # Hero status HUD top-right: REBUILT · 3 DAYS LEFT
        plan.append(
            f'<rect x="598" y="348" width="296" height="62" rx="6" fill="#07131E" fill-opacity="0.88" '
            f'stroke="{PLAN}" stroke-width="1.6"/>'
        )
        plan.append(f'<rect x="608" y="358" width="8" height="42" rx="2" fill="{PLAN}"/>')
        plan.append(
            f'<text x="628" y="376" font-family="Segoe UI, Arial, sans-serif" font-size="11" '
            f'font-weight="700" letter-spacing="1.8" fill="{PLAN}">BLUEPRINT STATUS · RESTORED</text>'
        )
        plan.append(
            f'<text x="628" y="399" font-family="Segoe UI, Arial, sans-serif" font-size="19" '
            f'font-weight="800" letter-spacing="1.2" fill="{PLAN_CORE}">REBUILT · 3 DAYS LEFT</text>'
        )
        plan.append("</g>")
        parts.append("\n".join(plan))

    # ── LAYER 5: onplan (Warm ember motes + viewfinder corners + vignette) ──
    if _katman_aktif(katmanlar, "onplan"):
        onplan: list[str] = ['<g id="s307-onplan">']
        for _ in range(22):
            ex = rng.uniform(330, 520)
            ey = rng.uniform(120, 420)
            er = rng.uniform(1.1, 2.6)
            op = rng.uniform(0.35, 0.85)
            col = EMBER_HOT if rng.random() > 0.4 else EMBER
            onplan.append(f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="{er:.1f}" fill="{col}" opacity="{op:.2f}"/>')
        # Subtle cyan data dust near puzzle
        for _ in range(16):
            cx = rng.uniform(560, 880)
            cy = rng.uniform(90, 330)
            cr = rng.uniform(0.9, 2.0)
            onplan.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{cr:.1f}" fill="{PLAN_CORE}" opacity="0.55"/>')
        onplan.append(f'<rect x="0" y="0" width="960" height="540" fill="url(#{p}_vig)"/>')
        # Viewfinder corners
        onplan.append(
            f'<path d="M 22,42 L 22,22 L 42,22 M 918,22 L 938,22 L 938,42 '
            f'M 22,498 L 22,518 L 42,518 M 918,518 L 938,518 L 938,498" '
            f'fill="none" stroke="{PLAN}" stroke-width="1.3" opacity="0.45"/>'
        )
        onplan.append("</g>")
        parts.append("\n".join(onplan))

    return defs, "\n".join(parts)


# =============================================================================
# SCENE 3.08: UNLOCKED INFIRMARY DOOR ("DOOR UNLOCKED · TONIGHT")
# =============================================================================
def set_308_acik_kapi(
    katmanlar: set[str] | list[str] | None = None,
) -> tuple[str, str]:
    """Visual Echo 2 (echoing P04 closet golden light): Warm amber Fox River infirmary,
    locked Sara v2 (K.sara_figur('kararli')) in a single `sahne` layer holding the brass
    INF-04 key in her hand as she walks away from the slightly ajar infirmary door, with
    a blazing warm golden light stripe spilling through the open doorway + #7FE6FF
    'DOOR UNLOCKED · TONIGHT' HUD.
    """
    rng = random.Random(308)
    p = _uid("s308")

    sara_body = K.sara_figur("kararli")

    defs = f"""
    <linearGradient id="{p}_wall_bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#1E1813"/>
      <stop offset="48%" stop-color="#2D231A"/>
      <stop offset="100%" stop-color="#16110D"/>
    </linearGradient>
    <linearGradient id="{p}_wall_lower" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#272F2B"/>
      <stop offset="100%" stop-color="#161C19"/>
    </linearGradient>
    <linearGradient id="{p}_floor_g" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#1C1915"/>
      <stop offset="45%" stop-color="#27211B"/>
      <stop offset="100%" stop-color="#120E0B"/>
    </linearGradient>
    <linearGradient id="{p}_door_slit" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#FFF5D6"/>
      <stop offset="55%" stop-color="#FFD074"/>
      <stop offset="100%" stop-color="#E59836"/>
    </linearGradient>
    <linearGradient id="{p}_gold_beam" x1="0.08" y1="0.15" x2="0.92" y2="0.88">
      <stop offset="0%" stop-color="#FFE8A8" stop-opacity="0.72"/>
      <stop offset="38%" stop-color="#F5B856" stop-opacity="0.32"/>
      <stop offset="78%" stop-color="#C9832B" stop-opacity="0.10"/>
      <stop offset="100%" stop-color="#C9832B" stop-opacity="0.0"/>
    </linearGradient>
    <linearGradient id="{p}_floor_spill" x1="0.05" y1="0.0" x2="0.95" y2="1.0">
      <stop offset="0%" stop-color="#FFEAB0" stop-opacity="0.88"/>
      <stop offset="45%" stop-color="#F0AE4A" stop-opacity="0.44"/>
      <stop offset="100%" stop-color="#B06C1E" stop-opacity="0.0"/>
    </linearGradient>
    <linearGradient id="{p}_door_leaf" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#1B2126"/>
      <stop offset="72%" stop-color="#293138"/>
      <stop offset="100%" stop-color="#3E362C"/>
    </linearGradient>
    <linearGradient id="{p}_brass_key" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFF0B0"/>
      <stop offset="48%" stop-color="#D9A344"/>
      <stop offset="100%" stop-color="#8A5E18"/>
    </linearGradient>
    <radialGradient id="{p}_warm_lamp" cx="0.65" cy="0.16" r="0.48">
      <stop offset="0%" stop-color="#FFD480" stop-opacity="0.34"/>
      <stop offset="55%" stop-color="#C98332" stop-opacity="0.12"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.0"/>
    </radialGradient>
    <radialGradient id="{p}_vig" cx="0.5" cy="0.5" r="0.72">
      <stop offset="50%" stop-color="#000000" stop-opacity="0.0"/>
      <stop offset="100%" stop-color="#070504" stop-opacity="0.72"/>
    </radialGradient>
    <filter id="{p}_glow_gold" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="5" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    """

    parts: list[str] = []

    # ── LAYER 1: uzak (Warm amber Fox River infirmary interior + cabinets & floor) ──
    if _katman_aktif(katmanlar, "uzak"):
        uzak: list[str] = ['<g id="s308-uzak">']
        uzak.append(f'<rect x="0" y="0" width="960" height="398" fill="url(#{p}_wall_bg)"/>')
        uzak.append(f'<rect x="0" y="246" width="960" height="152" fill="url(#{p}_wall_lower)"/>')
        uzak.append('<line x1="0" y1="246" x2="960" y2="246" stroke="#4D4235" stroke-width="3"/>')
        uzak.append(f'<rect x="0" y="398" width="960" height="142" fill="url(#{p}_floor_g)"/>')
        uzak.append(f'<rect x="0" y="0" width="960" height="540" fill="url(#{p}_warm_lamp)"/>')

        # Perspective tile grid on infirmary floor
        for ty in (418, 444, 476, 514):
            uzak.append(f'<line x1="0" y1="{ty}" x2="960" y2="{ty}" stroke="#3A3127" stroke-width="1" opacity="0.45"/>')
        for tx in range(-120, 1120, 96):
            uzak.append(f'<line x1="{tx}" y1="540" x2="{480 + (tx - 480) * 0.46:.1f}" y2="398" stroke="#3A3127" stroke-width="1" opacity="0.38"/>')

        # Infirmary wall medicine cabinet & glass panes (background right)
        uzak.append('<rect x="692" y="102" width="196" height="132" rx="4" fill="#1A2220" stroke="#46524D" stroke-width="2"/>')
        uzak.append('<rect x="704" y="114" width="80" height="108" fill="#23302D" stroke="#576862" stroke-width="1.2"/>')
        uzak.append('<rect x="796" y="114" width="80" height="108" fill="#23302D" stroke="#576862" stroke-width="1.2"/>')
        # Subtle shelves & bottles inside cabinet
        for sy in (148, 184):
            uzak.append(f'<line x1="706" y1="{sy}" x2="782" y2="{sy}" stroke="#4E605A" stroke-width="1.2"/>')
            uzak.append(f'<line x1="798" y1="{sy}" x2="874" y2="{sy}" stroke="#4E605A" stroke-width="1.2"/>')
        for bx in (718, 734, 756, 812, 832, 852):
            uzak.append(f'<rect x="{bx}" y="132" width="8" height="15" rx="1.5" fill="#6F8A82" opacity="0.55"/>')
            uzak.append(f'<rect x="{bx + 2}" y="168" width="9" height="15" rx="1.5" fill="#C49A58" opacity="0.45"/>')

        # Examination table silhouette far right
        uzak.append('<rect x="735" y="316" width="210" height="22" rx="4" fill="#2B3330" stroke="#151918" stroke-width="1.6"/>')
        uzak.append('<rect x="752" y="338" width="10" height="72" fill="#202624"/>')
        uzak.append('<rect x="916" y="338" width="10" height="72" fill="#202624"/>')

        # Wall clock (21:45 — night of escape)
        uzak.append('<circle cx="486" cy="112" r="24" fill="#241F1A" stroke="#5B4D3E" stroke-width="2.2"/>')
        uzak.append('<circle cx="486" cy="112" r="19" fill="#E6D9BE" opacity="0.88"/>')
        uzak.append('<line x1="486" y1="112" x2="476" y2="105" stroke="#1B1815" stroke-width="2.2" stroke-linecap="round"/>')
        uzak.append('<line x1="486" y1="112" x2="473" y2="112" stroke="#1B1815" stroke-width="1.6" stroke-linecap="round"/>')
        uzak.append('<circle cx="486" cy="112" r="2" fill="#1B1815"/>')

        # Warm overhead infirmary lamp fixture
        uzak.append('<rect x="520" y="18" width="170" height="10" rx="4" fill="#3B332A"/>')
        uzak.append('<rect x="532" y="26" width="146" height="5" rx="2" fill="#FFE4A4" opacity="0.85"/>')
        uzak.append("</g>")
        parts.append("\n".join(uzak))

    # ── LAYER 2: orta (Ajar infirmary door frame, leaf, sign & unlocked latch) ──
    if _katman_aktif(katmanlar, "orta"):
        orta: list[str] = ['<g id="s308-orta">']
        # Heavy steel door frame on the left
        orta.append('<rect x="78" y="64" width="232" height="346" fill="#15181C" stroke="#373D42" stroke-width="3"/>')
        # Slightly ajar heavy steel door leaf (angled slightly inward)
        orta.append(
            f'<polygon points="88,72 246,78 246,408 88,402" fill="url(#{p}_door_leaf)" '
            f'stroke="{INK}" stroke-width="2.4"/>'
        )
        # Wired-glass infirmary door window
        orta.append('<rect x="122" y="114" width="92" height="110" rx="3" fill="#2A261E" stroke="#4D4A42" stroke-width="2"/>')
        orta.append('<rect x="126" y="118" width="84" height="102" fill="#F2BE68" opacity="0.26"/>')
        for wy in range(128, 218, 18):
            orta.append(f'<line x1="126" y1="{wy}" x2="210" y2="{wy}" stroke="#3F3B34" stroke-width="0.8" opacity="0.5"/>')
        # Door sign: INFIRMARY · RM 04
        orta.append('<rect x="116" y="238" width="104" height="22" rx="2" fill="#182026" stroke="#536370" stroke-width="1"/>')
        orta.append(
            '<text x="168" y="253" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif" '
            'font-size="9.5" font-weight="700" letter-spacing="1.0" fill="#E3D6B8">INFIRMARY · 04</text>'
        )
        # Brass door handle & retracted (unlocked) deadbolt latch on door edge
        orta.append('<rect x="220" y="246" width="16" height="44" rx="2" fill="#9A7634" stroke="#1A130F" stroke-width="1.2"/>')
        orta.append('<circle cx="228" cy="274" r="5" fill="#DFB256" stroke="#1A130F" stroke-width="1.1"/>')
        # Retracted latch indicator (flush = unlocked!)
        orta.append('<rect x="244" y="254" width="4" height="12" fill="#FFD980"/>')
        orta.append("</g>")
        parts.append("\n".join(orta))

    # ── LAYER 2B: kapi_isik (Independently animatable golden doorway light slit, beam & floor spill) ──
    if _katman_aktif(katmanlar, "kapi_isik"):
        kapi_isik: list[str] = ['<g id="s308-kapi_isik">']
        # Blazing warm amber doorway gap (ajar opening on right edge of door: x=246..300)
        kapi_isik.append(f'<rect x="246" y="72" width="54" height="334" fill="url(#{p}_door_slit)" filter="url(#{p}_glow_gold)"/>')
        # Volumetric golden light beam spilling into infirmary room
        kapi_isik.append(
            f'<polygon points="246,72 300,72 645,425 246,406" fill="url(#{p}_gold_beam)"/>'
        )
        # Golden light stripe across the floor (Visual Echo 2 of P04 closet door!)
        kapi_isik.append(
            f'<polygon points="246,406 300,406 592,540 288,540" fill="url(#{p}_floor_spill)"/>'
        )
        kapi_isik.append("</g>")
        parts.append("\n".join(kapi_isik))

    # ── LAYER 3: sahne (Locked Sara v2 + brass INF-04 key in her hand — ALL ONE LAYER) ──
    if _katman_aktif(katmanlar, "sahne"):
        sahne: list[str] = ['<g id="s308-sahne">']
        # Ground cast shadow from the golden doorway light
        sahne.append('<ellipse cx="578" cy="512" rx="92" ry="15" fill="#0A0705" opacity="0.52"/>')
        # Locked Dr. Sara Tancredi v2 (feet at local y=0 -> screen y=514), walking away right
        sahne.append('<g transform="translate(534, 514) scale(0.84)">')
        sahne.append(sara_body)
        # Brass INF-04 key held directly in Sara's near right hand (local x=57, y=-228)
        # Same `sahne` group -> 100% R4-PARALLAX compliant!
        sahne.append('<g transform="translate(58, -220) rotate(24)">')
        # Key ring
        sahne.append(
            f'<circle cx="0" cy="0" r="8.5" fill="none" stroke="#C8CFD6" stroke-width="2.2"/>'
        )
        # Brass key bow + shaft + teeth
        sahne.append(
            f'<ellipse cx="14" cy="0" rx="8" ry="6" fill="url(#{p}_brass_key)" stroke="{INK_WARM}" stroke-width="1.4"/>'
        )
        sahne.append('<circle cx="14" cy="0" r="2.2" fill="#2A2016"/>')
        sahne.append(
            f'<path d="M 21,-2.2 L 48,-2.2 L 48,2.2 L 43,2.2 L 43,6 L 39,6 L 39,2.2 '
            f'L 34,2.2 L 34,5.5 L 30,5.5 L 30,2.2 L 21,2.2 Z" '
            f'fill="url(#{p}_brass_key)" stroke="{INK_WARM}" stroke-width="1.2"/>'
        )
        # Small metal tag hanging from ring: INF-04
        sahne.append(
            f'<rect x="-12" y="9" width="32" height="13" rx="2.5" fill="#202830" '
            f'stroke="#9EB0C0" stroke-width="1.2"/>'
        )
        sahne.append(
            '<text x="4" y="18.2" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif" '
            'font-size="6.8" font-weight="800" fill="#FFE6A8">INF-04</text>'
        )
        sahne.append("</g>")
        # Warm golden rim light highlight along Sara's left coat edge (catching doorway light)
        sahne.append(
            '<path d="M -52,-412 C -58,-360 -56,-290 -58,-154" fill="none" '
            'stroke="#FFE09A" stroke-width="2.4" opacity="0.58"/>'
        )
        sahne.append("</g>")
        sahne.append("</g>")
        parts.append("\n".join(sahne))

    # ── LAYER 4: plan (#7FE6FF CAD doorway callouts + DOOR UNLOCKED · TONIGHT HUD) ──
    if _katman_aktif(katmanlar, "plan"):
        plan: list[str] = ['<g id="s308-plan">']
        # Cyan lock-status bracket on the ajar door latch
        plan.append(
            f'<circle cx="246" cy="260" r="18" fill="none" stroke="{PLAN}" stroke-width="1.6" '
            f'stroke-dasharray="4 3" opacity="0.92"/>'
        )
        plan.append(
            f'<path d="M 264,254 L 312,228 L 438,228" fill="none" stroke="{PLAN}" stroke-width="1.3" opacity="0.88"/>'
        )
        plan.append(
            f'<rect x="314" y="206" width="150" height="20" rx="3" fill="#071520" fill-opacity="0.85" '
            f'stroke="{PLAN}" stroke-width="1.1"/>'
        )
        plan.append(
            f'<text x="389" y="219.5" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif" '
            f'font-size="9.5" font-weight="700" letter-spacing="1.0" fill="{PLAN_CORE}">LATCH OPEN · 12° AJAR</text>'
        )

        # Callout to Sara's brass INF-04 key (shifted with Sara to x=598)
        plan.append(
            f'<circle cx="598" cy="336" r="24" fill="none" stroke="{PLAN}" stroke-width="1.4" '
            f'stroke-dasharray="5 3" opacity="0.85"/>'
        )
        plan.append(
            f'<path d="M 622,336 L 686,336 L 702,320" fill="none" stroke="{PLAN}" stroke-width="1.2" opacity="0.85"/>'
        )
        plan.append(
            f'<rect x="690" y="294" width="126" height="24" rx="3" fill="#071520" fill-opacity="0.85" '
            f'stroke="{PLAN}" stroke-width="1.1"/>'
        )
        plan.append(
            f'<text x="753" y="309.5" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif" '
            f'font-size="9.5" font-weight="700" letter-spacing="0.9" fill="{AMBER_GOLD}">KEY: INF-04</text>'
        )

        # Hero HUD badge top-right: DOOR UNLOCKED · TONIGHT (generous >=18px padding both sides, zero overflow)
        plan.append(
            f'<rect x="610" y="30" width="328" height="58" rx="6" fill="#07131E" fill-opacity="0.90" '
            f'stroke="{PLAN}" stroke-width="1.6"/>'
        )
        plan.append(f'<rect x="622" y="39" width="7" height="40" rx="2" fill="{AMBER_GOLD}"/>')
        plan.append(
            f'<text x="640" y="54" font-family="Segoe UI, Arial, sans-serif" font-size="10" '
            f'font-weight="700" letter-spacing="1.3" fill="{PLAN}">INFIRMARY ACCESS · CONFIRMED</text>'
        )
        plan.append(
            f'<text x="640" y="76" font-family="Segoe UI, Arial, sans-serif" font-size="16" '
            f'font-weight="800" letter-spacing="0.7" fill="{PLAN_CORE}">DOOR UNLOCKED · TONIGHT</text>'
        )
        plan.append("</g>")
        parts.append("\n".join(plan))

    # ── LAYER 5: onplan (Floating golden dust motes in light beam + vignette) ──
    if _katman_aktif(katmanlar, "onplan"):
        onplan: list[str] = ['<g id="s308-onplan">']
        for _ in range(36):
            dx = rng.uniform(248, 560)
            dy = rng.uniform(110, 515)
            dr = rng.uniform(0.9, 2.5)
            op = rng.uniform(0.28, 0.85)
            onplan.append(f'<circle cx="{dx:.1f}" cy="{dy:.1f}" r="{dr:.1f}" fill="#FFE8A8" opacity="{op:.2f}"/>')
        onplan.append(f'<rect x="0" y="0" width="960" height="540" fill="url(#{p}_vig)"/>')
        onplan.append(
            f'<path d="M 22,42 L 22,22 L 42,22 M 918,22 L 938,22 L 938,42 '
            f'M 22,498 L 22,518 L 42,518 M 918,518 L 938,518 L 938,498" '
            f'fill="none" stroke="{PLAN}" stroke-width="1.3" opacity="0.40"/>'
        )
        onplan.append("</g>")
        parts.append("\n".join(onplan))

    return defs, "\n".join(parts)


# =============================================================================
# SCENE 3.09: NIGHT ESCAPE CABLE ("ESCAPED!")
# =============================================================================
def set_309_kablo_kacisi(
    katmanlar: set[str] | list[str] | None = None,
) -> tuple[str, str]:
    """Stormy rainy Fox River night: taut steel cable stretched from high infirmary window
    to the top of the outer Fox River stone wall, two determined figure silhouettes
    (Michael & Lincoln) sliding across the cable (all anatomy + grip in single `sahne` layer),
    dual volumetric searchlight beams from giant watchtowers narrowly missing them,
    red alarm beacon glow, and 'ESCAPED!' callout.
    """
    rng = random.Random(309)
    p = _uid("s309")

    defs = f"""
    <linearGradient id="{p}_sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#040913"/>
      <stop offset="52%" stop-color="#0B1626"/>
      <stop offset="100%" stop-color="#142336"/>
    </linearGradient>
    <linearGradient id="{p}_stone_wall" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#19232F"/>
      <stop offset="50%" stop-color="#253242"/>
      <stop offset="100%" stop-color="#131B26"/>
    </linearGradient>
    <linearGradient id="{p}_beam_icy" x1="0" y1="0" x2="1" y2="0.4">
      <stop offset="0%" stop-color="#E6F8FF" stop-opacity="0.72"/>
      <stop offset="48%" stop-color="#9BD6F2" stop-opacity="0.26"/>
      <stop offset="100%" stop-color="#6CB2D8" stop-opacity="0.0"/>
    </linearGradient>
    <linearGradient id="{p}_beam_amber" x1="1" y1="0" x2="0" y2="0.6">
      <stop offset="0%" stop-color="#FFE6A3" stop-opacity="0.70"/>
      <stop offset="48%" stop-color="#E8B254" stop-opacity="0.24"/>
      <stop offset="100%" stop-color="#C98830" stop-opacity="0.0"/>
    </linearGradient>
    <radialGradient id="{p}_red_alarm" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0%" stop-color="{RED_ALERT}" stop-opacity="0.92"/>
      <stop offset="35%" stop-color="{RED_ALERT}" stop-opacity="0.34"/>
      <stop offset="100%" stop-color="{RED_ALERT}" stop-opacity="0.0"/>
    </radialGradient>
    <radialGradient id="{p}_win_warm" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0%" stop-color="#FFD88A" stop-opacity="0.75"/>
      <stop offset="65%" stop-color="#C88232" stop-opacity="0.25"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.0"/>
    </radialGradient>
    <radialGradient id="{p}_vig" cx="0.5" cy="0.5" r="0.72">
      <stop offset="52%" stop-color="#000000" stop-opacity="0.0"/>
      <stop offset="100%" stop-color="#02050A" stop-opacity="0.74"/>
    </radialGradient>
    <filter id="{p}_glow_soft" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="3.5" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    """

    parts: list[str] = []

    # ── LAYER 1: uzak (Stormy night sky, layered clouds, lightning, cellblock & ground mist) ──
    if _katman_aktif(katmanlar, "uzak"):
        uzak: list[str] = ['<g id="s309-uzak">']
        uzak.append(f'<rect x="0" y="0" width="960" height="540" fill="url(#{p}_sky)"/>')
        # Multi-layered storm cloud banks with moonlit silver rim
        uzak.append('<ellipse cx="220" cy="76" rx="290" ry="62" fill="#122236" opacity="0.72"/>')
        uzak.append('<ellipse cx="520" cy="48" rx="310" ry="52" fill="#182C44" opacity="0.56"/>')
        uzak.append('<ellipse cx="760" cy="74" rx="280" ry="58" fill="#0E1B2D" opacity="0.74"/>')
        uzak.append(
            '<path d="M 180,104 Q 340,78 510,94 Q 680,110 860,82" fill="none" '
            'stroke="#4A7298" stroke-width="2.2" opacity="0.22"/>'
        )
        # Distant forked lightning bolt
        uzak.append(
            f'<path d="M 412,0 L 396,46 L 414,52 L 386,112 L 400,116 L 378,162" '
            f'fill="none" stroke="#CFEFFF" stroke-width="2.2" opacity="0.82" filter="url(#{p}_glow_soft)"/>'
        )
        uzak.append(
            '<path d="M 396,46 L 426,82 L 418,108" fill="none" stroke="#9ED8F5" stroke-width="1.2" opacity="0.58"/>'
        )
        # Distant Fox River cellblock roofline & tiny lit cell windows
        uzak.append('<rect x="190" y="346" width="560" height="194" fill="#09111C"/>')
        uzak.append('<polygon points="435,346 470,296 505,346" fill="#0D1624"/>')
        for r_y in (374, 404, 434):
            for c_x in range(220, 720, 28):
                if (c_x + r_y) % 56 == 0:
                    uzak.append(f'<rect x="{c_x}" y="{r_y}" width="10" height="14" rx="1" fill="#E3A854" opacity="0.46"/>')
                else:
                    uzak.append(f'<rect x="{c_x}" y="{r_y}" width="10" height="14" rx="1" fill="#182738" opacity="0.55"/>')
        # Rising low yard mist bands
        uzak.append('<ellipse cx="480" cy="495" rx="420" ry="72" fill="#2A4663" opacity="0.22"/>')
        uzak.append('<ellipse cx="320" cy="525" rx="310" ry="54" fill="#3B5D7E" opacity="0.16"/>')
        uzak.append("</g>")
        parts.append("\n".join(uzak))

    # ── LAYER 2: orta (High infirmary building left, outer stone wall + razor wire right, watchtowers) ──
    if _katman_aktif(katmanlar, "orta"):
        orta: list[str] = ['<g id="s309-orta">']
        # Left high infirmary stone wing + wet rain sheen
        orta.append(f'<rect x="0" y="42" width="168" height="498" fill="url(#{p}_stone_wall)" stroke="{INK}" stroke-width="2"/>')
        for sy in range(72, 540, 32):
            orta.append(f'<line x1="0" y1="{sy}" x2="168" y2="{sy}" stroke="#101822" stroke-width="1" opacity="0.6"/>')
        # Wet stone specular highlight along right edge of infirmary wing
        orta.append('<line x1="166" y1="44" x2="166" y2="540" stroke="#5A7A99" stroke-width="1.8" opacity="0.45"/>')
        # Broken-bar infirmary escape window (warm interior glow)
        orta.append(f'<circle cx="122" cy="148" r="82" fill="url(#{p}_win_warm)"/>')
        orta.append('<rect x="86" y="108" width="66" height="84" rx="3" fill="#2A2016" stroke="#4D5C6B" stroke-width="3"/>')
        orta.append('<rect x="92" y="114" width="54" height="72" fill="#F2B85E" opacity="0.48"/>')
        # Bent/removed bar stubs
        orta.append('<line x1="108" y1="114" x2="108" y2="128" stroke="#182028" stroke-width="3"/>')
        orta.append('<line x1="130" y1="114" x2="130" y2="126" stroke="#182028" stroke-width="3"/>')
        orta.append('<line x1="108" y1="172" x2="108" y2="186" stroke="#182028" stroke-width="3"/>')

        # Left-background watchtower (behind infirmary)
        orta.append('<rect x="218" y="138" width="54" height="402" fill="#15202D" stroke="#0B1118" stroke-width="1.6"/>')
        orta.append('<polygon points="206,138 245,98 284,138" fill="#1D2B3B" stroke="#0B1118" stroke-width="1.6"/>')
        orta.append('<rect x="212" y="138" width="66" height="24" fill="#1E2D3E" stroke="#3B5066" stroke-width="1.2"/>')
        orta.append('<circle cx="245" cy="94" r="3.5" fill="#52161E" stroke="#1B0A0D" stroke-width="1"/>')

        # Right-side giant watchtower & outer Fox River perimeter stone wall
        orta.append('<rect x="822" y="108" width="68" height="432" fill="#16212E" stroke="#0B1118" stroke-width="1.8"/>')
        orta.append('<polygon points="808,108 856,62 904,108" fill="#1F2E40" stroke="#0B1118" stroke-width="1.8"/>')
        orta.append('<rect x="814" y="108" width="84" height="30" fill="#223346" stroke="#425972" stroke-width="1.4"/>')
        # Guard silhouette inside right tower
        orta.append('<circle cx="848" cy="120" r="4.5" fill="#0B1017"/>')
        orta.append('<rect x="842" y="125" width="12" height="12" rx="2" fill="#0B1017"/>')
        orta.append('<circle cx="856" cy="58" r="4" fill="#52161E" stroke="#1B0A0D" stroke-width="1"/>')

        # Outer Fox River stone perimeter wall (right foreground-mid) + wet top sheen
        orta.append(f'<rect x="756" y="344" width="204" height="196" fill="url(#{p}_stone_wall)" stroke="{INK}" stroke-width="2.2"/>')
        orta.append('<rect x="748" y="336" width="212" height="14" rx="2" fill="#324357" stroke="#0D141C" stroke-width="1.6"/>')
        orta.append('<line x1="750" y1="337" x2="958" y2="337" stroke="#8FB2D4" stroke-width="1.4" opacity="0.58"/>')
        for wy in range(374, 540, 28):
            orta.append(f'<line x1="756" y1="{wy}" x2="960" y2="{wy}" stroke="#0E151E" stroke-width="1.1" opacity="0.65"/>')
        # Concertina razor wire coils along top of outer stone wall
        for cx in range(754, 956, 16):
            orta.append(f'<circle cx="{cx}" cy="326" r="10" fill="none" stroke="#89A4BE" stroke-width="1.15" opacity="0.78"/>')
        orta.append("</g>")
        parts.append("\n".join(orta))

    # ── LAYER 2B: alarm (Independently animatable red watchtower alarm beacons & roof spill) ──
    if _katman_aktif(katmanlar, "alarm"):
        alarm: list[str] = ['<g id="s309-alarm">']
        # Left watchtower red alarm beacon
        alarm.append(f'<circle cx="245" cy="94" r="54" fill="url(#{p}_red_alarm)"/>')
        alarm.append('<circle cx="245" cy="94" r="5" fill="#FFABB3"/>')
        # Right watchtower red alarm beacon
        alarm.append(f'<circle cx="856" cy="58" r="68" fill="url(#{p}_red_alarm)"/>')
        alarm.append('<circle cx="856" cy="58" r="5.5" fill="#FFABB3"/>')
        # Red alarm wash on tower eaves
        alarm.append('<line x1="210" y1="138" x2="280" y2="138" stroke="#FF4A5C" stroke-width="2" opacity="0.55"/>')
        alarm.append('<line x1="812" y1="108" x2="900" y2="108" stroke="#FF4A5C" stroke-width="2.2" opacity="0.62"/>')
        alarm.append("</g>")
        parts.append("\n".join(alarm))

    # ── LAYER 2C: projektor_1 (Left tower icy-white volumetric searchlight, pivot 274,156) ──
    if _katman_aktif(katmanlar, "projektor_1"):
        p1: list[str] = ['<g id="s309-projektor_1">']
        p1.append(
            f'<polygon points="274,150 864,14 912,134 274,162" fill="url(#{p}_beam_icy)"/>'
        )
        p1.append(f'<circle cx="274" cy="156" r="6.5" fill="#EBF9FF" filter="url(#{p}_glow_soft)"/>')
        p1.append("</g>")
        parts.append("\n".join(p1))

    # ── LAYER 2D: projektor_2 (Right tower warm-amber volumetric searchlight, pivot 818,138) ──
    if _katman_aktif(katmanlar, "projektor_2"):
        p2: list[str] = ['<g id="s309-projektor_2">']
        p2.append(
            f'<polygon points="818,132 162,438 286,540 826,148" fill="url(#{p}_beam_amber)"/>'
        )
        p2.append(f'<circle cx="818" cy="138" r="7" fill="#FFF1C2" filter="url(#{p}_glow_soft)"/>')
        p2.append("</g>")
        parts.append("\n".join(p2))

    # ── LAYER 3: sahne (Taut steel escape cable & anchor hardware) ──
    if _katman_aktif(katmanlar, "sahne"):
        sahne: list[str] = ['<g id="s309-sahne">']
        # Taut steel cable from high infirmary window (136,154) to outer wall anchor (812,338)
        cable_d = "M 136,154 Q 478,264 812,338"
        sahne.append(f'<path d="{cable_d}" fill="none" stroke="#080D14" stroke-width="6.4"/>')
        sahne.append(f'<path d="{cable_d}" fill="none" stroke="#8BA5BE" stroke-width="2.8"/>')
        sahne.append(f'<path d="{cable_d}" fill="none" stroke="#E4F5FF" stroke-width="1.0" opacity="0.80"/>')
        # Anchor cleats at window sill & outer wall crest
        sahne.append('<circle cx="136" cy="154" r="4.5" fill="#324457" stroke="#0D141C" stroke-width="1.4"/>')
        sahne.append('<circle cx="812" cy="338" r="5" fill="#3A4E63" stroke="#0D141C" stroke-width="1.5"/>')
        sahne.append("</g>")
        parts.append("\n".join(sahne))

    # ── LAYER 3B: kacanlar (Michael & Lincoln sliding on cable + friction sparks — R4-PARALLAX 1-layer) ──
    if _katman_aktif(katmanlar, "kacanlar"):
        kac: list[str] = ['<g id="s309-kacanlar">']

        # Cinematic 2D sculpted silhouette figures sliding on cable (ALL anatomy + grip in single group)
        def _escapee(cx: float, cy: float, scale: float, broad: bool, shirt_col: str, rim_col: str) -> str:
            w = 1.14 if broad else 1.0
            return f"""
            <g transform="translate({cx},{cy}) rotate(14.5) scale({scale})">
              <!-- Back arm & cloth grip on cable -->
              <path d="M -24,-6 L -12,-6 C -10,-6 -9,-2 -11,4 L -15,24 L -4,32 L -14,38 L -24,22 L -25,0 Z"
                    fill="#16212E" stroke="{INK}" stroke-width="1.5" stroke-linejoin="round"/>
              <!-- Back leg swinging behind -->
              <path d="M -8,64 L -26,84 L -46,79 L -49,87 L -23,95 L -2,74 Z"
                    fill="#111822" stroke="{INK}" stroke-width="1.5" stroke-linejoin="round"/>
              <!-- Torso (sculpted prison shirt / jacket with shoulder blade & waist taper) -->
              <path d="M {-15 * w:.1f},28 C {-17 * w:.1f},38 {-13 * w:.1f},56 {-10 * w:.1f},70 L {11 * w:.1f},70
                       C {14 * w:.1f},54 {17 * w:.1f},38 {15 * w:.1f},27 C {6 * w:.1f},24 {-6 * w:.1f},24 {-15 * w:.1f},28 Z"
                    fill="{shirt_col}" stroke="{INK}" stroke-width="1.7" stroke-linejoin="round"/>
              <!-- Sculpted profile head (buzzcut, forehead, nose bridge, sharp jaw looking right) -->
              <path d="M -5,14 C -5,6 1,2 8,3 C 14,4 16,9 16,14 L 18,17 L 15,19 L 15,24 C 12,27 6,27 2,26 L -3,23 Z"
                    fill="#18222F" stroke="{INK}" stroke-width="1.5" stroke-linejoin="round"/>
              <!-- Rim light on forehead/nose/shoulder catching searchlight spill -->
              <path d="M 3,3 C 10,3 15,7 16,13 L 18,17" fill="none" stroke="{rim_col}" stroke-width="1.4" opacity="0.88"/>
              <path d="M {-13 * w:.1f},29 C {-2 * w:.1f},25 {8 * w:.1f},25 {14 * w:.1f},28" fill="none" stroke="{rim_col}" stroke-width="1.8" opacity="0.78"/>
              <!-- Front leg bent forward with knee fold & boot -->
              <path d="M 2,66 L 24,82 L 15,107 L 23,111 L 12,114 L 4,108 L 12,86 L -4,73 Z"
                    fill="#182230" stroke="{INK}" stroke-width="1.5" stroke-linejoin="round"/>
              <!-- Front arm gripping cable firmly with cloth wrap -->
              <path d="M 10,33 L 17,22 L 18,2 L 14,-6 L 27,-6 L 29,4 L 25,26 L 13,40 Z"
                    fill="{shirt_col}" stroke="{INK}" stroke-width="1.5" stroke-linejoin="round"/>
              <!-- Cloth wrap highlights on cable -->
              <rect x="-25" y="-7" width="14" height="9" rx="2.5" fill="#3B4959" stroke="{INK}" stroke-width="1.2"/>
              <rect x="14" y="-7" width="14" height="9" rx="2.5" fill="#3B4959" stroke="{INK}" stroke-width="1.2"/>
            </g>
            """

        # Leading figure: Michael (nearer to outer wall, steel-blue prison shirt)
        kac.append(_escapee(556, 274, 0.96, broad=False, shirt_col="#274766", rim_col="#BCE8FF"))
        # Trailing figure: Lincoln (broader shoulders, dark jacket)
        kac.append(_escapee(374, 224, 1.02, broad=True, shirt_col="#1D2733", rim_col="#FFE0A6"))

        # Friction sparks & rain spray at cable contact points
        for sx, sy in ((556, 274), (374, 224)):
            for _ in range(9):
                ang = rng.uniform(-2.7, -0.4)
                dist = rng.uniform(9, 25)
                kac.append(
                    f'<line x1="{sx}" y1="{sy}" x2="{sx + math.cos(ang) * dist:.1f}" '
                    f'y2="{sy + math.sin(ang) * dist:.1f}" stroke="#FFE49E" stroke-width="1.3" opacity="0.88"/>'
                )
        kac.append("</g>")
        parts.append("\n".join(kac))

    # ── LAYER 4: plan (#7FE6FF escape trajectory + blind-arc CAD + ESCAPED! highlight) ──
    if _katman_aktif(katmanlar, "plan"):
        plan: list[str] = ['<g id="s309-plan">']
        # Cyan trajectory overlay parallel to cable
        plan.append(
            f'<path d="M 140,142 Q 480,250 812,324" fill="none" stroke="{PLAN}" '
            f'stroke-width="1.3" stroke-dasharray="7 5" opacity="0.82"/>'
        )
        # Blind-arc safe corridor markers between the two beams
        plan.append(
            f'<path d="M 442,192 L 486,192 L 486,184" fill="none" stroke="{PLAN}" stroke-width="1.2" opacity="0.78"/>'
        )
        plan.append(
            f'<text x="488" y="176" font-family="Segoe UI, Arial, sans-serif" font-size="9.5" '
            f'font-weight="700" letter-spacing="1.0" fill="{PLAN}">BLIND ARC · 1.2M CLEARANCE</text>'
        )
        # Anchor node on outer wall
        plan.append(f'<circle cx="812" cy="338" r="11" fill="none" stroke="{PLAN}" stroke-width="1.6"/>')
        plan.append(f'<circle cx="812" cy="338" r="3" fill="{PLAN_CORE}"/>')
        plan.append(
            f'<text x="790" y="366" text-anchor="end" font-family="Segoe UI, Arial, sans-serif" '
            f'font-size="9.5" font-weight="700" letter-spacing="1.0" fill="{PLAN_CORE}">PERIMETER WALL · CLEARED</text>'
        )

        # Red alert + ESCAPED! hero badge top-left/center-top
        plan.append(
            f'<rect x="330" y="24" width="300" height="58" rx="6" fill="#0A121D" fill-opacity="0.88" '
            f'stroke="{RED_ALERT}" stroke-width="1.8"/>'
        )
        plan.append(f'<rect x="340" y="33" width="8" height="40" rx="2" fill="{RED_ALERT}"/>')
        plan.append(
            f'<text x="360" y="48" font-family="Segoe UI, Arial, sans-serif" font-size="10" '
            f'font-weight="700" letter-spacing="1.8" fill="#FF8C97">FOX RIVER ALARM · BREACH</text>'
        )
        plan.append(
            f'<text x="360" y="72" font-family="Segoe UI, Arial, sans-serif" font-size="22" '
            f'font-weight="900" letter-spacing="2.4" fill="{PLAN_CORE}">ESCAPED!</text>'
        )
        plan.append("</g>")
        parts.append("\n".join(plan))

    # ── LAYER 5: onplan (Heavy diagonal storm rain + red alarm lens glow + vignette) ──
    if _katman_aktif(katmanlar, "onplan"):
        onplan: list[str] = ['<g id="s309-onplan">']
        for _ in range(115):
            rx = rng.uniform(-40, 990)
            ry = rng.uniform(-20, 520)
            rl = rng.uniform(16, 38)
            op = rng.uniform(0.14, 0.44)
            onplan.append(
                f'<line x1="{rx:.1f}" y1="{ry:.1f}" x2="{rx - rl * 0.34:.1f}" y2="{ry + rl:.1f}" '
                f'stroke="#C6E4FA" stroke-width="1.0" opacity="{op:.2f}"/>'
            )
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
# SCENE 3.10: AIRSTRIP & MANHUNT ("MANHUNT" + ACT IV OPEN LOOP)
# =============================================================================
def set_310_pist_insan_avi(
    katmanlar: set[str] | list[str] | None = None,
) -> tuple[str, str]:
    """Wet night airstrip: small twin-engine plane departing & shrinking into the dark sky
    with glowing tail/nav lights, Michael & Lincoln silhouettes sprinting into the night
    on the wet asphalt (all anatomy in single `sahne` layer), red-blue police sirens
    painting the wet runway from behind, and top-right Act IV Open Loop inset (FBI desk
    lamp illuminating Michael's tattoo photograph + 'MANHUNT').
    """
    rng = random.Random(310)
    p = _uid("s310")

    sirt_defs, sirt_body = K.michael_sirt_dovme(plan_glow=0.55)

    defs = f"""
    {sirt_defs}
    <linearGradient id="{p}_night_sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#040811"/>
      <stop offset="58%" stop-color="#0C1726"/>
      <stop offset="100%" stop-color="#152336"/>
    </linearGradient>
    <linearGradient id="{p}_asphalt" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#0E151F"/>
      <stop offset="45%" stop-color="#17202D"/>
      <stop offset="100%" stop-color="#0A0F16"/>
    </linearGradient>
    <radialGradient id="{p}_siren_red" cx="0.16" cy="0.58" r="0.44">
      <stop offset="0%" stop-color="{SIREN_RED}" stop-opacity="0.72"/>
      <stop offset="46%" stop-color="{SIREN_RED}" stop-opacity="0.24"/>
      <stop offset="100%" stop-color="{SIREN_RED}" stop-opacity="0.0"/>
    </radialGradient>
    <radialGradient id="{p}_siren_blue" cx="0.34" cy="0.62" r="0.44">
      <stop offset="0%" stop-color="{SIREN_BLUE}" stop-opacity="0.70"/>
      <stop offset="46%" stop-color="{SIREN_BLUE}" stop-opacity="0.22"/>
      <stop offset="100%" stop-color="{SIREN_BLUE}" stop-opacity="0.0"/>
    </radialGradient>
    <linearGradient id="{p}_headlight" x1="0" y1="0.5" x2="1" y2="0.5">
      <stop offset="0%" stop-color="#FFF5D6" stop-opacity="0.52"/>
      <stop offset="55%" stop-color="#C8DCF2" stop-opacity="0.16"/>
      <stop offset="100%" stop-color="#C8DCF2" stop-opacity="0.0"/>
    </linearGradient>
    <radialGradient id="{p}_plane_glow" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0%" stop-color="#FF5266" stop-opacity="0.92"/>
      <stop offset="45%" stop-color="#FF5266" stop-opacity="0.26"/>
      <stop offset="100%" stop-color="#FF5266" stop-opacity="0.0"/>
    </radialGradient>
    <radialGradient id="{p}_fbi_lamp" cx="0.35" cy="0.22" r="0.78">
      <stop offset="0%" stop-color="#FFE4A3" stop-opacity="0.62"/>
      <stop offset="48%" stop-color="#D9983A" stop-opacity="0.24"/>
      <stop offset="100%" stop-color="#120E0B" stop-opacity="0.0"/>
    </radialGradient>
    <radialGradient id="{p}_vig" cx="0.5" cy="0.5" r="0.74">
      <stop offset="52%" stop-color="#000000" stop-opacity="0.0"/>
      <stop offset="100%" stop-color="#02050A" stop-opacity="0.74"/>
    </radialGradient>
    <clipPath id="{p}_fbi_clip">
      <rect x="652" y="24" width="284" height="176" rx="8"/>
    </clipPath>
    <clipPath id="{p}_photo_clip">
      <rect x="-58" y="-48" width="116" height="86"/>
    </clipPath>
    """

    parts: list[str] = []

    # ── LAYER 1: uzak (Stormy night horizon, clouds, treeline, hangar & airport beacon) ──
    if _katman_aktif(katmanlar, "uzak"):
        uzak: list[str] = ['<g id="s310-uzak">']
        uzak.append(f'<rect x="0" y="0" width="960" height="310" fill="url(#{p}_night_sky)"/>')
        # Layered storm horizon clouds
        uzak.append('<ellipse cx="260" cy="94" rx="310" ry="52" fill="#122136" opacity="0.58"/>')
        uzak.append('<ellipse cx="640" cy="118" rx="320" ry="56" fill="#0F1C2E" opacity="0.52"/>')
        uzak.append('<ellipse cx="460" cy="272" rx="460" ry="44" fill="#1D324A" opacity="0.34"/>')
        # Distant small airstrip hangar & control tower silhouette (left-center horizon)
        uzak.append('<path d="M 278,298 L 278,266 Q 312,252 346,266 L 346,298 Z" fill="#0B131F"/>')
        uzak.append('<rect x="358" y="256" width="16" height="42" fill="#0B131F"/>')
        uzak.append('<rect x="354" y="246" width="24" height="11" rx="1" fill="#142336"/>')
        uzak.append('<rect x="357" y="249" width="18" height="4" fill="#7FE6FF" opacity="0.38"/>')
        uzak.append('<circle cx="366" cy="242" r="2.2" fill="#72FFA8" opacity="0.85"/>')
        # Distant dark pine treeline along horizon (y ~ 292)
        tree_pts = ["0,310"]
        for tx in range(0, 980, 18):
            th = 276 + rng.randint(-12, 10)
            tree_pts.append(f"{tx},{th}")
        tree_pts.append("960,310")
        uzak.append(f'<polygon points="{" ".join(tree_pts)}" fill="#070D16"/>')
        uzak.append("</g>")
        parts.append("\n".join(uzak))

    # ── LAYER 1B: ucak (Independently animatable departing small aircraft + nav/tail lights) ──
    if _katman_aktif(katmanlar, "ucak"):
        ucak: list[str] = ['<g id="s310-ucak">']
        # Departing small twin-engine plane climbing & shrinking into upper sky (456, 118)
        ucak.append('<g transform="translate(456, 118) rotate(-11)">')
        # Subtle climb contrail / engine wake
        ucak.append(
            '<path d="M -104,28 Q -52,15 -10,3" fill="none" stroke="#8EB2D4" stroke-width="1.5" '
            'stroke-dasharray="5 4" opacity="0.38"/>'
        )
        # Sculpted twin-prop aircraft silhouette (wings, engine nacelles, fuselage, tail fin)
        ucak.append(
            '<path d="M -32,3 L -12,1 L -12,-2 L -8,-2 L -8,1 L 8,0 L 8,-3 L 12,-3 L 12,0 L 32,-2 '
            'L 30,2 L 5,4 L 7,11 L -5,11 L -3,4 L -30,5 Z" fill="#18273B" stroke="#6B8BAE" stroke-width="0.9"/>'
        )
        ucak.append('<polygon points="-3.5,1 0,-12 3.5,1" fill="#1E3048"/>')
        # Glowing red tail beacon, red/green wingtip nav lights & warm landing light
        ucak.append(f'<circle cx="0" cy="-11" r="16" fill="url(#{p}_plane_glow)"/>')
        ucak.append('<circle cx="0" cy="-11" r="2.4" fill="#FFA6B0"/>')
        ucak.append('<circle cx="-31" cy="3" r="2.2" fill="#FF4B5C"/>')
        ucak.append('<circle cx="31" cy="-2" r="2.2" fill="#7AFFB2"/>')
        ucak.append('<circle cx="0" cy="6" r="1.8" fill="#FFF4D2" opacity="0.9"/>')
        ucak.append("</g>")
        ucak.append("</g>")
        parts.append("\n".join(ucak))

    # ── LAYER 2: orta (Wet reflective night runway, long puddle reflections, police cruisers & sirens) ──
    if _katman_aktif(katmanlar, "orta"):
        orta: list[str] = ['<g id="s310-orta">']
        # Wet asphalt airstrip
        orta.append(f'<rect x="0" y="298" width="960" height="242" fill="url(#{p}_asphalt)"/>')
        # Wet rain puddle specular bands across tarmac
        orta.append('<ellipse cx="470" cy="410" rx="290" ry="22" fill="#23364C" opacity="0.28"/>')
        orta.append('<ellipse cx="640" cy="488" rx="220" ry="18" fill="#1E3044" opacity="0.26"/>')
        # Red-blue siren washes across wet tarmac & horizon
        orta.append(f'<rect x="0" y="190" width="960" height="350" fill="url(#{p}_siren_red)"/>')
        orta.append(f'<rect x="0" y="190" width="960" height="350" fill="url(#{p}_siren_blue)"/>')

        # Perspective runway edges & dashed centerline converging toward (460, 298)
        orta.append('<line x1="460" y1="298" x2="20" y2="540" stroke="#5A738E" stroke-width="2.2" opacity="0.62"/>')
        orta.append('<line x1="460" y1="298" x2="940" y2="540" stroke="#5A738E" stroke-width="2.2" opacity="0.62"/>')
        # Dashed centerline stripes + wet reflections
        for i in range(6):
            t0 = 0.08 + i * 0.15
            t1 = t0 + 0.08
            y0 = 298 + t0 * 242
            y1 = 298 + t1 * 242
            x0 = 460 + (t0 * 50)
            x1 = 460 + (t1 * 50)
            w0 = 2 + t0 * 8
            w1 = 2 + t1 * 8
            orta.append(
                f'<polygon points="{x0 - w0:.1f},{y0:.1f} {x0 + w0:.1f},{y0:.1f} '
                f'{x1 + w1:.1f},{y1:.1f} {x1 - w1:.1f},{y1:.1f}" fill="#E4EEF7" opacity="0.52"/>'
            )

        # Runway edge amber lights + elongated wet-asphalt vertical reflections
        for i in range(6):
            t = 0.10 + i * 0.17
            ry = 298 + t * 230
            lx = 460 - t * 420
            rx = 460 + t * 455
            rad = 2.4 + t * 2.0
            refl_h = 10 + t * 28
            for px in (lx, rx):
                orta.append(f'<circle cx="{px:.1f}" cy="{ry:.1f}" r="{rad * 2.2:.1f}" fill="#FFD27D" opacity="0.22"/>')
                orta.append(f'<circle cx="{px:.1f}" cy="{ry:.1f}" r="{rad:.1f}" fill="#FFE4A0"/>')
                orta.append(
                    f'<ellipse cx="{px:.1f}" cy="{ry + refl_h * 0.65:.1f}" rx="{rad * 1.1:.1f}" '
                    f'ry="{refl_h:.1f}" fill="#F5AE45" opacity="0.34"/>'
                )

        # Runway taxi sign on right edge (RWY 09)
        orta.append('<rect x="836" y="458" width="48" height="18" rx="2" fill="#E8B948" stroke="#1A150B" stroke-width="1.4"/>')
        orta.append(
            '<text x="860" y="470.5" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif" '
            'font-size="8.5" font-weight="900" fill="#14110A">RWY 09</text>'
        )

        # Approaching police cruisers on left runway (sharper details, headlights & sweeping siren reflections)
        for cx, cy, sc in ((128, 354, 1.05), (226, 326, 0.74)):
            orta.append(f'<g transform="translate({cx},{cy}) scale({sc})">')
            # Long volumetric headlight beams sweeping right across wet runway
            orta.append(f'<polygon points="48,14 340,-16 340,56 48,26" fill="url(#{p}_headlight)"/>')
            # Cruiser sculpted body + windshield + wheels + push bumper
            orta.append(
                f'<path d="M -46,24 L -40,7 L -18,-7 L 22,-7 L 38,7 L 54,11 L 54,26 L -46,26 Z" '
                f'fill="#0C141F" stroke="#364C64" stroke-width="1.3"/>'
            )
            orta.append('<polygon points="-14,-4 18,-4 32,7 -28,7" fill="#1B2C40" opacity="0.72"/>')
            orta.append('<circle cx="-26" cy="26" r="7" fill="#070B10" stroke="#324456" stroke-width="1.2"/>')
            orta.append('<circle cx="28" cy="26" r="7" fill="#070B10" stroke="#324456" stroke-width="1.2"/>')
            orta.append('<circle cx="52" cy="18" r="3" fill="#FFF7DC"/>')
            # Lightbar (bright red + blue)
            orta.append(f'<rect x="-9" y="-12" width="12" height="5.5" rx="1.5" fill="{SIREN_RED}"/>')
            orta.append(f'<rect x="3" y="-12" width="12" height="5.5" rx="1.5" fill="{SIREN_BLUE}"/>')
            # Elongated wet-runway siren reflections
            orta.append(f'<ellipse cx="-3" cy="60" rx="18" ry="34" fill="{SIREN_RED}" opacity="0.38"/>')
            orta.append(f'<ellipse cx="16" cy="64" rx="18" ry="36" fill="{SIREN_BLUE}" opacity="0.38"/>')
            orta.append("</g>")
        orta.append("</g>")
        parts.append("\n".join(orta))

    # ── LAYER 3: sahne (Foreground wet tarmac reflections & mist) ──
    if _katman_aktif(katmanlar, "sahne"):
        sahne: list[str] = ['<g id="s310-sahne">']
        sahne.append('<ellipse cx="580" cy="512" rx="190" ry="16" fill="#2A4668" opacity="0.18"/>')
        sahne.append('<ellipse cx="420" cy="526" rx="140" ry="12" fill="#FF3B52" opacity="0.10"/>')
        sahne.append("</g>")
        parts.append("\n".join(sahne))

    # ── LAYER 3B: kosucular (Independently animatable Michael & Lincoln sprinting — R4-PARALLAX 1-layer) ──
    if _katman_aktif(katmanlar, "kosucular"):
        kos: list[str] = ['<g id="s310-kosucular">']

        def _runner(rx: float, ry: float, sc: float, broad: bool, rim_col: str, coat_col: str) -> str:
            w = 1.15 if broad else 1.0
            # Sculpted 2D cinematic sprinting silhouette + wet tarmac puddle reflection (ALL IN ONE LAYER)
            return f"""
            <g transform="translate({rx},{ry}) scale({sc})">
              <!-- Wet asphalt puddle reflection & contact shadow -->
              <ellipse cx="0" cy="4" rx="{32 * w:.1f}" ry="6.5" fill="#04070C" opacity="0.68"/>
              <path d="M -18,6 L 16,6 L 26,48 L -26,48 Z" fill="{rim_col}" opacity="0.20"/>
              <!-- Back arm swinging behind -->
              <path d="M -4,-84 L -24,-70 L -34,-54 L -28,-50 L -18,-62 L -2,-74 Z"
                    fill="#0D141F" stroke="{INK}" stroke-width="1.3" stroke-linejoin="round"/>
              <!-- Back leg pushing off -->
              <path d="M -4,-48 L -24,-24 L -39,-4 L -32,0 L -16,-19 L 4,-44 Z"
                    fill="#0E1520" stroke="{INK}" stroke-width="1.4" stroke-linejoin="round"/>
              <!-- Forward-leaning sculpted torso (jacket/shirt collar & hem) -->
              <path d="M {-10 * w:.1f},-90 L {14 * w:.1f},-86 L {11 * w:.1f},-46 L {-11 * w:.1f},-47 Z"
                    fill="{coat_col}" stroke="{INK}" stroke-width="1.6" stroke-linejoin="round"/>
              <!-- Front leg striding forward -->
              <path d="M 4,-47 L 26,-25 L 18,-1 L 26,1 L 15,3 L 10,-2 L 15,-22 L -3,-43 Z"
                    fill="#141F2E" stroke="{INK}" stroke-width="1.4" stroke-linejoin="round"/>
              <!-- Front arm pumping forward -->
              <path d="M 8,-81 L 25,-66 L 38,-74 L 41,-68 L 24,-57 L 4,-73 Z"
                    fill="{coat_col}" stroke="{INK}" stroke-width="1.3" stroke-linejoin="round"/>
              <!-- Sculpted profile head leaning forward -->
              <path d="M 0,-104 C 1,-112 9,-114 15,-111 C 19,-108 19,-103 18,-99 L 20,-96 L 16,-94 L 13,-90 L 4,-91 L 0,-96 Z"
                    fill="#121B28" stroke="{INK}" stroke-width="1.4" stroke-linejoin="round"/>
              <!-- Siren rim light catching back of head, shoulder & jacket edge -->
              <path d="M 1,-107 C -1,-101 0,-95 3,-91 M {-10 * w:.1f},-89 L {-11 * w:.1f},-48 M -23,-24 L -37,-4"
                    fill="none" stroke="{rim_col}" stroke-width="2.2" opacity="0.90" stroke-linecap="round"/>
            </g>
            """

        # Michael sprinting ahead right (blue siren rim light, steel-blue shirt)
        kos.append(_runner(624, 466, 1.04, broad=False, rim_col="#66B2FF", coat_col="#1D334A"))
        # Lincoln sprinting close behind (red siren rim light, broader dark jacket)
        kos.append(_runner(534, 482, 1.12, broad=True, rim_col="#FF6878", coat_col="#16202C"))
        kos.append("</g>")
        parts.append("\n".join(kos))

    # ── LAYER 4: plan (Flight-missed telemetry + MANHUNT HUD badge) ──
    if _katman_aktif(katmanlar, "plan"):
        plan: list[str] = ['<g id="s310-plan">']
        # Subtle cyan flight-missed & on-foot escape telemetry
        plan.append(
            f'<path d="M 476,126 L 548,154 L 636,154" fill="none" stroke="{PLAN}" stroke-width="1.1" '
            f'stroke-dasharray="4 4" opacity="0.68"/>'
        )
        plan.append(
            f'<text x="456" y="88" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif" '
            f'font-size="9.5" font-weight="700" letter-spacing="1.1" fill="{PLAN}">AIRCRAFT DEPARTED</text>'
        )

        # Hero MANHUNT HUD badge top-left
        plan.append(
            f'<rect x="28" y="24" width="268" height="60" rx="6" fill="#08111C" fill-opacity="0.90" '
            f'stroke="{RED_ALERT}" stroke-width="1.8"/>'
        )
        plan.append(f'<rect x="38" y="33" width="8" height="42" rx="2" fill="{RED_ALERT}"/>')
        plan.append(
            f'<text x="58" y="49" font-family="Segoe UI, Arial, sans-serif" font-size="10" '
            f'font-weight="700" letter-spacing="1.6" fill="{PLAN}">FOX RIVER EIGHT · ON FOOT</text>'
        )
        plan.append(
            f'<text x="58" y="74" font-family="Segoe UI, Arial, sans-serif" font-size="22" '
            f'font-weight="900" letter-spacing="2.4" fill="#FF6B78">MANHUNT</text>'
        )
        plan.append("</g>")
        parts.append("\n".join(plan))

    # ── LAYER 4B: fbi_kutu (Independently animatable Act IV Open Loop FBI desk lamp + locked A-Sirt v1 photo) ──
    if _katman_aktif(katmanlar, "fbi_kutu"):
        fbi: list[str] = ['<g id="s310-fbi_kutu">']
        fbi.append(f'<g clip-path="url(#{p}_fbi_clip)">')
        # Dark walnut FBI investigation desk background
        fbi.append('<rect x="652" y="24" width="284" height="176" fill="#18120E"/>')
        fbi.append(f'<rect x="652" y="24" width="284" height="176" fill="url(#{p}_fbi_lamp)"/>')
        # Brass/green FBI desk lamp shade in upper-left of inset
        fbi.append('<path d="M 672,24 L 686,42 L 732,42 L 746,24 Z" fill="#23483A" stroke="#101815" stroke-width="1.5"/>')
        fbi.append('<ellipse cx="709" cy="43" rx="22" ry="4" fill="#FFE6A8" opacity="0.85"/>')

        # Tilted surveillance photograph of Michael's back tattoo pinned on desk
        fbi.append('<g transform="translate(794, 114) rotate(-6)">')
        fbi.append('<rect x="-66" y="-56" width="132" height="112" rx="2" fill="#EDE6D8" stroke="#1B1612" stroke-width="1.5"/>')
        fbi.append('<rect x="-58" y="-48" width="116" height="86" fill="#1B2430"/>')
        # Locked A-Sirt v1 (K.michael_sirt_dovme(plan_glow=0.55)) clipped cleanly inside polaroid window
        fbi.append(f'<g clip-path="url(#{p}_photo_clip)">')
        fbi.append('<rect x="-58" y="-48" width="116" height="86" fill="#131B26"/>')
        fbi.append('<g transform="translate(0, 12) scale(0.185)">')
        fbi.append(sirt_body)
        fbi.append("</g>")
        fbi.append("</g>")
        # Red FBI investigation circle, callout arrow & pin over the locked back tattoo photo
        fbi.append(
            f'<circle cx="4" cy="4" r="23" fill="none" stroke="{RED_ALERT}" stroke-width="1.9" stroke-dasharray="5 3"/>'
        )
        fbi.append(
            f'<path d="M 21,-11 L 44,-24" fill="none" stroke="{RED_ALERT}" stroke-width="1.4"/>'
        )
        fbi.append(f'<polygon points="18,-9 25,-10 21,-16" fill="{RED_ALERT}"/>')
        fbi.append(f'<circle cx="0" cy="-50" r="4.5" fill="{RED_ALERT}" stroke="#4A0A12" stroke-width="1.2"/>')
        fbi.append(
            '<text x="0" y="50" text-anchor="middle" font-family="Consolas, monospace" '
            'font-size="7.5" font-weight="700" fill="#2A2420">FBI EXHIBIT · #94941 TATTOO</text>'
        )
        fbi.append("</g>")

        # Inset bottom-left micro tag: ACT IV · FBI TRAIL
        fbi.append(
            '<rect x="662" y="174" width="136" height="18" rx="3" fill="#09131E" fill-opacity="0.88"/>'
        )
        fbi.append(
            f'<text x="730" y="186" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif" '
            f'font-size="8.5" font-weight="700" letter-spacing="1.1" fill="{AMBER_GOLD}">ACT IV · FBI TRAIL</text>'
        )
        fbi.append("</g>")
        # Crisp border around FBI Act IV inset
        fbi.append(
            f'<rect x="652" y="24" width="284" height="176" rx="8" fill="none" '
            f'stroke="{AMBER_GOLD}" stroke-width="1.6" opacity="0.88"/>'
        )
        fbi.append("</g>")
        parts.append("\n".join(fbi))

    # ── LAYER 5: onplan (Light night drizzle + siren bokeh + vignette) ──
    if _katman_aktif(katmanlar, "onplan"):
        onplan: list[str] = ['<g id="s310-onplan">']
        for _ in range(52):
            rx = rng.uniform(0, 960)
            ry = rng.uniform(0, 520)
            rl = rng.uniform(10, 22)
            onplan.append(
                f'<line x1="{rx:.1f}" y1="{ry:.1f}" x2="{rx - rl * 0.2:.1f}" y2="{ry + rl:.1f}" '
                f'stroke="#B6D4EE" stroke-width="0.9" opacity="0.22"/>'
            )
        # Subtle red-blue siren lens bokeh on left edge
        onplan.append(f'<circle cx="64" cy="436" r="24" fill="{SIREN_RED}" opacity="0.14"/>')
        onplan.append(f'<circle cx="118" cy="462" r="28" fill="{SIREN_BLUE}" opacity="0.14"/>')
        onplan.append(f'<rect x="0" y="0" width="960" height="540" fill="url(#{p}_vig)"/>')
        onplan.append(
            f'<path d="M 22,42 L 22,22 L 42,22 M 918,22 L 938,22 L 938,42 '
            f'M 22,498 L 22,518 L 42,518 M 918,518 L 938,518 L 938,498" '
            f'fill="none" stroke="{PLAN}" stroke-width="1.3" opacity="0.42"/>'
        )
        onplan.append("</g>")
        parts.append("\n".join(onplan))

    return defs, "\n".join(parts)


# =============================================================================
# RENDERING & CARD GENERATION (1280x720 SET CARD + 1280x720 R13 200% CROP CARD)
# =============================================================================
def _render_scene_png(scene_fn, scale: int = 2) -> Image.Image:
    defs, body = scene_fn()
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
    img_307 = _render_scene_png(set_307_yanik_dovme, scale=2)  # 1920x1080
    img_308 = _render_scene_png(set_308_acik_kapi, scale=2)
    img_309 = _render_scene_png(set_309_kablo_kacisi, scale=2)
    img_310 = _render_scene_png(set_310_pist_insan_avi, scale=2)

    f_title = _font(19, bold=True)
    f_sub = _font(11, bold=False)
    f_card_t = _font(12, bold=True)
    f_card_s = _font(10, bold=False)
    f_small = _font(9, bold=True)

    # =========================================================================
    # OUTPUT 1: 4-PANEL ACT III SET CARD (1280 x 720, 100% ENGLISH)
    # =========================================================================
    canvas = _draw_card_bg(1280, 720)
    draw = ImageDraw.Draw(canvas)

    draw.text((24, 12), "MICHAEL SCOFIELD · ACT III SCORCHED TATTOO, OPEN DOOR, ESCAPE & MANHUNT", fill="#EBF3FA", font=f_title)
    draw.text(
        (24, 36),
        "STYLE B+A HYBRID (CINEMATIC 2D + CYAN BLUEPRINT VISION)  ·  SCENES 3.07 – 3.10  ·  5-LAYER PARALLAX  ·  R4-PARALLAX LOCKED",
        fill="#7E97B0",
        font=f_sub,
    )
    # Header palette chips
    top_chips = [("EMBER", "#FF7A24"), ("AMBER", "#F5C26B"), ("STORM", "#1B2C40"), ("SIREN", "#E63244"), ("CAD", "#7FE6FF")]
    cx = 928
    for lbl, col in top_chips:
        draw.rounded_rectangle((cx, 16, cx + 14, 30), radius=3, fill=col, outline="#3B5168", width=1)
        draw.text((cx + 18, 17), lbl, fill="#9DB3C9", font=f_small)
        cx += 66
    draw.line((24, 54, 1256, 54), fill="#213247", width=1)

    panels = [
        (
            (22, 64, 632, 378),
            img_307,
            "01 · 3.07 SCORCHED TATTOO & REBUILD",
            "\"REBUILT · 3 DAYS LEFT\"",
            "#FFB85C",
            ["#101B29", "#B88462", "#FF7A24", "#7FE6FF", "#DDFBFF"],
            [
                "• Locked A-Sirt v1 (glow=0.6)",
                "• Ember burn ring (no gore)",
                "• Subtle rising smoke wisps",
                "• Floating cyan CAD puzzle",
                "• REBUILT · 3 DAYS LEFT",
            ],
            "Cold cell + ember & CAD",
            "s307-uzak/orta/sahne/plan/onplan",
        ),
        (
            (646, 64, 1256, 378),
            img_308,
            "02 · 3.08 UNLOCKED INFIRMARY DOOR",
            "Visual Echo 2 · \"TONIGHT\"",
            "#F5C26B",
            ["#251D16", "#293138", "#FFE4A4", "#D9A344", "#7FE6FF"],
            [
                "• Warm amber infirmary",
                "• Locked Sara v2 (1 layer)",
                "• Brass INF-04 key in hand",
                "• Golden ajar door spill",
                "• DOOR UNLOCKED · TONIGHT",
            ],
            "Golden doorway spill",
            "s308-uzak/orta/sahne/plan/onplan",
        ),
        (
            (22, 390, 632, 704),
            img_309,
            "03 · 3.09 NIGHT ESCAPE CABLE",
            "Storm Climax · \"ESCAPED!\"",
            "#7FE6FF",
            ["#081220", "#253242", "#FFE6A3", "#E63244", "#7FE6FF"],
            [
                "• Window-to-wall steel cable",
                "• Michael & Lincoln sliding",
                "• Dual near-miss beams",
                "• Red alarm + storm rain",
                "• Blind-arc CAD + ESCAPED!",
            ],
            "Storm + dual searchlights",
            "s309-uzak/orta/sahne/plan/onplan",
        ),
        (
            (646, 390, 1256, 704),
            img_310,
            "04 · 3.10 AIRSTRIP & MANHUNT",
            "Act IV Loop · \"MANHUNT\"",
            "#FF6B78",
            ["#0A1320", "#FF2E48", "#2E8CFF", "#F5C26B", "#7FE6FF"],
            [
                "• Wet runway & fleeing plane",
                "• Brothers sprinting on foot",
                "• Red-blue police sirens",
                "• FBI lamp + tattoo photo",
                "• Act IV Open Loop MANHUNT",
            ],
            "Wet sirens + FBI desk lamp",
            "s310-uzak/orta/sahne/plan/onplan",
        ),
    ]

    for box, src, title, sub, tcol, pal, elems, light, lyrs in panels:
        x0, y0, x1, y1 = box
        _draw_panel_box(draw, box)
        thumb = src.resize((424, 238), Image.Resampling.LANCZOS)
        canvas.paste(thumb, (x0 + 10, y0 + 34), thumb)
        draw.rectangle((x0 + 10, y0 + 34, x0 + 10 + 424, y0 + 34 + 238), outline="#2E455E", width=1)
        draw.text((x0 + 10, y0 + 10), title, fill=tcol, font=f_card_t)
        draw.text((x0 + 276, y0 + 12), sub, fill="#8AA3BC", font=f_card_s)

        ix = x0 + 444
        draw.text((ix, y0 + 34), "PALETTE", fill="#7FE6FF", font=f_small)
        _draw_swatches(draw, ix, y0 + 49, pal, size=16, gap=5)
        draw.text((ix, y0 + 76), "KEY ELEMENTS", fill="#9BB2C8", font=f_small)
        for idx, item in enumerate(elems):
            draw.text((ix, y0 + 92 + idx * 19), item, fill="#D5E2EE", font=f_card_s)
        draw.text((ix, y0 + 196), "KEY LIGHTING", fill="#9BB2C8", font=f_small)
        draw.text((ix, y0 + 210), light, fill="#F6C367", font=f_card_s)
        draw.text((ix, y0 + 234), "LAYERS (5)", fill="#9BB2C8", font=f_small)
        draw.text((ix, y0 + 248), "uzak · orta · sahne\nplan · onplan", fill="#8AA3BC", font=f_small)
        draw.text((x0 + 10, y0 + 282), f"PARALLAX: {lyrs}  ·  R4-PARALLAX SINGLE-LAYER ANATOMY", fill="#6E87A0", font=f_small)

    out_main = OUT_DIR / f"b3_set_yanik_kacis_{versiyon}.png"
    canvas.convert("RGB").save(out_main, quality=95)

    # =========================================================================
    # OUTPUT 2: R13 200% ZOOM QUALITY CONTROL CARD (1280 x 720 — 4 PANELS)
    # =========================================================================
    r13 = _draw_card_bg(1280, 720)
    d13 = ImageDraw.Draw(r13)
    d13.text((24, 12), "R13 · 200% ZOOM QUALITY CONTROL (ACT III SCORCHED, DOOR, CABLE & MANHUNT)", fill="#EBF3FA", font=f_title)
    d13.text(
        (24, 36),
        "1:1 PIXEL CROPS FROM 1920×1080 SOURCE  ·  R4-PARALLAX ANATOMY, LOCKED ASSETS, LIGHTING & ENGLISH TYPOGRAPHY",
        fill="#7E97B0",
        font=f_sub,
    )
    d13.line((24, 54, 1256, 54), fill="#213247", width=1)

    cw, ch = 600, 264
    crops = [
        (
            img_307,
            (1030, 560),
            "1 · 3.07 EMBER BURN RING & FLOATING CAD PUZZLE (200%)",
            "Locked A-Sirt v1 scorched void (zero gore) + #7FE6FF rebuilt puzzle piece & HUD",
            (22, 64),
        ),
        (
            img_308,
            (1530, 180),
            "2 · 3.08 DOOR UNLOCKED · TONIGHT HUD & SARA v2 (200%)",
            "Zero-overflow HUD box (>=18px padding) + locked Sara v2 & warm golden spill",
            (652, 64),
        ),
        (
            img_309,
            (940, 515),
            "3 · 3.09 CABLE ESCAPEES & NEAR-MISS SEARCHLIGHTS (200%)",
            "Sculpted Michael & Lincoln silhouettes sliding between dual near-miss beams",
            (22, 392),
        ),
        (
            img_310,
            (1560, 235),
            "4 · 3.10 ACT IV OPEN LOOP: FBI DESK LAMP & TATTOO PHOTO (200%)",
            "Warm FBI desk lamp illuminating Michael's back tattoo photo + Exhibit #94941 clue",
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

    out_r13 = OUT_DIR / "b3_set_yanik_kacis_r13.png"
    r13.convert("RGB").save(out_r13, quality=95)
    print(f"Saved:\n  - {out_main}\n  - {out_r13}")
    return out_main, out_r13


if __name__ == "__main__":
    uret_kartlar("v1")
