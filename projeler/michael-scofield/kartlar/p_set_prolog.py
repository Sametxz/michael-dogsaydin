"""V-Prolog (Prologue Opening Hook & Dark Closet Floor High-Detail Set Art).

Style B+A Hybrid (Cinematic 2D + Cyan Blueprint Vision) — 5-layer parallax-ready scenes (960x540):
  - set_p01_fox_river_gece(katmanlar=None) -> (defs_str, body_str)
  - set_p04_depo_zemin(katmanlar=None)     -> (defs_str, body_str)

Rules enforced:
  - R4-PARALLAX: No character body parts split across layers (jeans cuffs, sneakers & contact
    shadows remain unified inside p04-sahne).
  - 100% ENGLISH on-screen and card typography.
  - Every stroked <path> explicitly specifies fill="none".
  - Isolated module; does not touch karakter.py.
"""
from __future__ import annotations

import io
import math
import random
import re
from pathlib import Path

import resvg_py
from PIL import Image, ImageDraw, ImageFont

OUT_DIR = Path(__file__).resolve().parent

W_SCENE, H_SCENE = 960, 540

INK = "#0E131B"
INK_WARM = "#18100B"
PLAN = "#7FE6FF"
PLAN_CORE = "#E2FCFF"
AMBER_LIGHT = "#F8C86E"
AMBER_HOT = "#FFF3CC"
ALERT_RED = "#FF3B4E"

_UID = 0


def _uid(prefix: str = "pr") -> str:
    global _UID
    _UID += 1
    return f"{prefix}_{_UID}"


def _katman_aktif(katmanlar: set[str] | list[str] | None, ad: str) -> bool:
    return katmanlar is None or ad in katmanlar


# =============================================================================
# SCENE P01: EPIC FOX RIVER NIGHT OPENING HOOK ("FOX RIVER" / "BY HEART")
# =============================================================================
def set_p01_fox_river_gece(
    katmanlar: set[str] | list[str] | None = None,
) -> tuple[str, str]:
    """High-activity cinematic opening frame of Fox River State Penitentiary at night:
    - uzak:   Stormy night sky, moonlit layered clouds, distant lightning, Chicago skyline glow
    - orta:   Towering Gothic stone Fox River fortress, twin watchtowers with guards,
              lit multi-story cellblock windows, concertina razor wire, wet yard reflections
    - sahne:  Sweeping dual-tone volumetric searchlight beams (cold icy white + warm amber),
              chain-link perimeter fence silhouette, layered diagonal rain & splashes
    - plan:   Multi-layer #7FE6FF cyan CAD architectural X-ray blueprint over stone walls:
              01 CELL -> 02 PIPE -> 03 TUNNEL -> 04 WALL dashed escape route
    - onplan: Foreground dark razor-wire framing + corner technical HUD brackets
    """
    rng = random.Random(101)
    p = _uid("p01")

    defs = f"""
    <linearGradient id="{p}_sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#030710"/>
      <stop offset="32%" stop-color="#091527"/>
      <stop offset="68%" stop-color="#142740"/>
      <stop offset="100%" stop-color="#1E334C"/>
    </linearGradient>
    <radialGradient id="{p}_moon_glow" cx="0.50" cy="0.21" r="0.44">
      <stop offset="0%" stop-color="#C8ECFF" stop-opacity="0.42"/>
      <stop offset="32%" stop-color="#6AA8D4" stop-opacity="0.20"/>
      <stop offset="68%" stop-color="#224468" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="#060D1A" stop-opacity="0.0"/>
    </radialGradient>
    <radialGradient id="{p}_chicago_glow" cx="0.82" cy="0.58" r="0.32">
      <stop offset="0%" stop-color="#F0A54A" stop-opacity="0.28"/>
      <stop offset="52%" stop-color="#A65E2A" stop-opacity="0.11"/>
      <stop offset="100%" stop-color="#0A1424" stop-opacity="0.0"/>
    </radialGradient>
    <linearGradient id="{p}_stone_dark" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#283444"/>
      <stop offset="48%" stop-color="#1C2532"/>
      <stop offset="100%" stop-color="#10161F"/>
    </linearGradient>
    <linearGradient id="{p}_stone_mid" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#334254"/>
      <stop offset="55%" stop-color="#232E3D"/>
      <stop offset="100%" stop-color="#141B26"/>
    </linearGradient>
    <linearGradient id="{p}_tower_l" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#131B26"/>
      <stop offset="38%" stop-color="#2B394B"/>
      <stop offset="76%" stop-color="#3B4D63"/>
      <stop offset="100%" stop-color="#18212E"/>
    </linearGradient>
    <linearGradient id="{p}_tower_r" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#18212E"/>
      <stop offset="28%" stop-color="#3B4D63"/>
      <stop offset="68%" stop-color="#283546"/>
      <stop offset="100%" stop-color="#111822"/>
    </linearGradient>
    <linearGradient id="{p}_gate_steel" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#141C25"/>
      <stop offset="50%" stop-color="#283442"/>
      <stop offset="100%" stop-color="#121821"/>
    </linearGradient>
    <linearGradient id="{p}_yard" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#111A26"/>
      <stop offset="36%" stop-color="#172434"/>
      <stop offset="72%" stop-color="#0E1722"/>
      <stop offset="100%" stop-color="#070C13"/>
    </linearGradient>
    <linearGradient id="{p}_beam_cool" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F2FCFF" stop-opacity="0.70"/>
      <stop offset="30%" stop-color="#A8E2FF" stop-opacity="0.30"/>
      <stop offset="72%" stop-color="#6BC3F5" stop-opacity="0.09"/>
      <stop offset="100%" stop-color="#6BC3F5" stop-opacity="0.0"/>
    </linearGradient>
    <linearGradient id="{p}_beam_cool_up" x1="0" y1="1" x2="1" y2="0">
      <stop offset="0%" stop-color="#E8F9FF" stop-opacity="0.54"/>
      <stop offset="45%" stop-color="#8FD8FF" stop-opacity="0.18"/>
      <stop offset="100%" stop-color="#8FD8FF" stop-opacity="0.0"/>
    </linearGradient>
    <linearGradient id="{p}_beam_amber" x1="1" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#FFF2CC" stop-opacity="0.68"/>
      <stop offset="34%" stop-color="#F7C266" stop-opacity="0.28"/>
      <stop offset="74%" stop-color="#D98B38" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="#D98B38" stop-opacity="0.0"/>
    </linearGradient>
    <linearGradient id="{p}_beam_amber_up" x1="1" y1="1" x2="0" y2="0">
      <stop offset="0%" stop-color="#FFF0C4" stop-opacity="0.48"/>
      <stop offset="48%" stop-color="#F0B152" stop-opacity="0.16"/>
      <stop offset="100%" stop-color="#F0B152" stop-opacity="0.0"/>
    </linearGradient>
    <radialGradient id="{p}_lamp_cool" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="1.0"/>
      <stop offset="35%" stop-color="#B8EBFF" stop-opacity="0.72"/>
      <stop offset="100%" stop-color="#7FE6FF" stop-opacity="0.0"/>
    </radialGradient>
    <radialGradient id="{p}_lamp_amber" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0%" stop-color="#FFF8E2" stop-opacity="1.0"/>
      <stop offset="35%" stop-color="#F8C466" stop-opacity="0.72"/>
      <stop offset="100%" stop-color="#E28F34" stop-opacity="0.0"/>
    </radialGradient>
    <radialGradient id="{p}_red_beacon" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0%" stop-color="#FF9EA8" stop-opacity="1.0"/>
      <stop offset="40%" stop-color="#FF2F45" stop-opacity="0.65"/>
      <stop offset="100%" stop-color="#FF2F45" stop-opacity="0.0"/>
    </radialGradient>
    <linearGradient id="{p}_xray_fill" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#072236" stop-opacity="0.56"/>
      <stop offset="100%" stop-color="#041524" stop-opacity="0.72"/>
    </linearGradient>
    <radialGradient id="{p}_vig" cx="0.5" cy="0.48" r="0.70">
      <stop offset="48%" stop-color="#000000" stop-opacity="0.0"/>
      <stop offset="86%" stop-color="#03070E" stop-opacity="0.52"/>
      <stop offset="100%" stop-color="#02050A" stop-opacity="0.82"/>
    </radialGradient>
    <radialGradient id="{p}_plaque_wash" cx="0.5" cy="0.3" r="0.6">
      <stop offset="0%" stop-color="#C8ECFF" stop-opacity="0.34"/>
      <stop offset="55%" stop-color="#7FE6FF" stop-opacity="0.10"/>
      <stop offset="100%" stop-color="#7FE6FF" stop-opacity="0.0"/>
    </radialGradient>
    <clipPath id="{p}_fence_l"><rect x="0" y="312" width="148" height="228"/></clipPath>
    <clipPath id="{p}_fence_r"><rect x="812" y="312" width="148" height="228"/></clipPath>
    """

    parts: list[str] = []

    # ── LAYER 1: uzak (Stormy sky, moonlit clouds, lightning, distant Chicago glow) ──
    if _katman_aktif(katmanlar, "uzak"):
        uzak: list[str] = ['<g id="p01-uzak">']
        uzak.append(f'<rect x="0" y="0" width="960" height="540" fill="url(#{p}_sky)"/>')
        uzak.append(f'<rect x="0" y="0" width="960" height="390" fill="url(#{p}_moon_glow)"/>')
        uzak.append(f'<rect x="0" y="130" width="960" height="260" fill="url(#{p}_chicago_glow)"/>')

        # Pale full moon peeking behind storm clouds
        uzak.append(
            '<circle cx="482" cy="96" r="26" fill="#E6F6FF" opacity="0.24"/>'
            '<circle cx="482" cy="96" r="16" fill="#F2FBFF" opacity="0.48"/>'
        )

        # 3 layered storm cloud banks with moonlit silver rim edges
        cloud_layers = [
            (
                "M-20,104 Q72,48 168,78 Q272,34 384,74 Q482,42 588,78 Q710,36 832,76 Q908,58 980,88 L980,196 L-20,196 Z",
                "#081222",
                0.82,
            ),
            (
                "M-20,148 Q98,98 220,132 Q336,84 468,124 Q594,88 726,126 Q844,96 980,136 L980,248 L-20,248 Z",
                "#0F1F35",
                0.76,
            ),
            (
                "M-20,192 Q132,150 264,178 Q402,138 548,176 Q682,144 824,180 Q912,162 980,188 L980,290 L-20,290 Z",
                "#15273E",
                0.68,
            ),
        ]
        for d_cl, col, op in cloud_layers:
            uzak.append(f'<path d="{d_cl}" fill="{col}" opacity="{op}"/>')

        # Subtle moonlit silver cloud-edge highlights
        uzak.append(
            '<path d="M362,74 Q482,42 588,78" fill="none" stroke="#B6E2FF" stroke-width="1.8" opacity="0.36"/>'
            '<path d="M342,124 Q468,94 592,126" fill="none" stroke="#8EC9EC" stroke-width="1.4" opacity="0.28"/>'
        )

        # Forked distant lightning bolt in upper-left storm cell
        uzak.append(
            '<path d="M254,18 L242,48 L254,53 L236,92 L244,95 L228,124" '
            'fill="none" stroke="#DDF4FF" stroke-width="1.8" opacity="0.72" stroke-linecap="round" stroke-linejoin="round"/>'
            '<path d="M242,48 L226,72 M254,53 L268,78" '
            'fill="none" stroke="#B4E6FF" stroke-width="1.1" opacity="0.52" stroke-linecap="round"/>'
            '<path d="M254,18 L242,48 L254,53 L236,92 L244,95 L228,124" '
            'fill="none" stroke="#7FE6FF" stroke-width="6.5" opacity="0.16" stroke-linecap="round"/>'
        )

        # Distant Chicago skyline silhouette on far right horizon with warm sodium-vapor pinpoints
        skyline_pts = [
            (640, 278), (640, 256), (656, 256), (656, 242), (674, 242), (674, 260),
            (690, 260), (690, 224), (702, 224), (702, 210), (706, 210), (706, 198),
            (709, 198), (709, 210), (715, 210), (715, 224), (724, 224), (724, 252),
            (742, 252), (742, 232), (762, 232), (762, 248), (784, 248), (784, 218),
            (798, 218), (798, 244), (824, 244), (824, 236), (846, 236), (846, 254),
            (884, 254), (884, 240), (908, 240), (908, 258), (960, 258), (960, 290), (640, 290),
        ]
        sky_d = "M" + " L".join(f"{x},{y}" for x, y in skyline_pts) + " Z"
        uzak.append(f'<path d="{sky_d}" fill="#0C1726" opacity="0.82"/>')
        # Distant skyline pinpoint lights
        for sx in range(650, 945, 11):
            sy = rng.randint(232, 266)
            if rng.random() < 0.65:
                c_dot = "#F5B862" if rng.random() < 0.72 else "#9ED4F0"
                uzak.append(f'<rect x="{sx}" y="{sy}" width="2" height="2" fill="{c_dot}" opacity="0.45"/>')

        # Distant atmospheric rain veil
        for _ in range(55):
            rx = rng.randint(0, 960)
            ry = rng.randint(0, 280)
            rl = rng.randint(18, 36)
            uzak.append(
                f'<line x1="{rx}" y1="{ry}" x2="{rx - int(rl * 0.28)}" y2="{ry + rl}" '
                'stroke="#7EB2D4" stroke-width="0.7" opacity="0.18"/>'
            )

        uzak.append("</g>")
        parts.append("".join(uzak))

    # ── LAYER 2: orta (Gothic Fox River Fortress, Twin Watchtowers, Lit Cellblocks, Wet Yard) ──
    if _katman_aktif(katmanlar, "orta"):
        orta: list[str] = ['<g id="p01-orta">']

        # 0) Distant secondary background watchtowers (adds massive penitentiary scale)
        for dtx in (296, 664):
            orta.append(
                f'<path d="M{dtx - 15},256 L{dtx - 11},138 L{dtx + 11},138 L{dtx + 15},256 Z" fill="#141F2E" stroke="{INK}" stroke-width="1.2"/>'
                f'<rect x="{dtx - 17}" y="122" width="34" height="16" fill="#182434" stroke="{INK}" stroke-width="1"/>'
                f'<rect x="{dtx - 12}" y="125" width="24" height="8" fill="#8CD8F0" opacity="0.28"/>'
                f'<path d="M{dtx - 20},122 L{dtx},104 L{dtx + 20},122 Z" fill="#101824" stroke="{INK}" stroke-width="1"/>'
                f'<circle cx="{dtx}" cy="100" r="4" fill="url(#{p}_red_beacon)"/>'
            )

        # 1) Background Gothic Admin Spire & Multi-Story Cellblocks rising behind perimeter wall
        # Central Gothic bell/admin spire
        orta.append(
            f'<path d="M432,268 L432,148 L452,148 L458,108 L480,68 L502,108 L508,148 L528,148 L528,268 Z" '
            f'fill="url(#{p}_stone_dark)" stroke="{INK}" stroke-width="1.8"/>'
            # Spire lancet windows
            '<path d="M474,132 L474,112 Q480,104 486,112 L486,132 Z" fill="#F4BE64" opacity="0.65"/>'
            '<path d="M460,176 L460,156 Q465,150 470,156 L470,176 Z" fill="#8CD8EC" opacity="0.42"/>'
            '<path d="M490,176 L490,156 Q495,150 500,156 L500,176 Z" fill="#F4BE64" opacity="0.58"/>'
            # Lightning rod & red beacon on central spire
            '<line x1="480" y1="68" x2="480" y2="48" stroke="#6E8299" stroke-width="1.5"/>'
            f'<circle cx="480" cy="48" r="7" fill="url(#{p}_red_beacon)"/>'
            '<circle cx="480" cy="48" r="2" fill="#FFD2D8"/>'
        )

        # Left & Right Multi-Story Cellblock Wings (A-Block & B-Block)
        cellblocks = [
            (182, 168, 242, 148),  # Left Cellblock A
            (536, 168, 242, 148),  # Right Cellblock B
        ]
        for bx, by, bw, bh in cellblocks:
            orta.append(
                f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" fill="url(#{p}_stone_dark)" stroke="{INK}" stroke-width="1.8"/>'
                # Roof parapet battlements
                f'<rect x="{bx - 4}" y="{by - 8}" width="{bw + 8}" height="10" fill="#253242" stroke="{INK}" stroke-width="1.2"/>'
            )
            # Stone roof merlons
            for mx in range(bx, bx + bw - 12, 22):
                orta.append(f'<rect x="{mx}" y="{by - 14}" width="12" height="7" fill="#2B394B" stroke="{INK}" stroke-width="1"/>')

            # 4 tiers of barred cellblock windows (mix of warm amber, cold fluorescent & dark cells)
            for row in range(4):
                wy = by + 16 + row * 28
                for col in range(9):
                    wx = bx + 14 + col * 24
                    r_val = rng.random()
                    if r_val < 0.42:
                        w_col = "#F5BA5D"
                        w_op = rng.uniform(0.68, 0.96)
                    elif r_val < 0.68:
                        w_col = "#84D3E8"
                        w_op = rng.uniform(0.45, 0.80)
                    else:
                        w_col = "#0E1722"
                        w_op = 0.92
                    orta.append(
                        f'<rect x="{wx}" y="{wy}" width="14" height="17" rx="1" fill="{w_col}" opacity="{w_op:.2f}" stroke="#0C121A" stroke-width="1"/>'
                    )
                    # Tiny vertical prison bars inside lit windows
                    if w_col != "#0E1722":
                        orta.append(
                            f'<line x1="{wx + 4.5}" y1="{wy}" x2="{wx + 4.5}" y2="{wy + 17}" stroke="#121821" stroke-width="0.9"/>'
                            f'<line x1="{wx + 9.5}" y1="{wy}" x2="{wx + 9.5}" y2="{wy + 17}" stroke="#121821" stroke-width="0.9"/>'
                        )

        # 2) Main Perimeter Stone Fortress Walls (Left, Right & Central Gatehouse Bastion)
        # Left & Right high stone walls
        orta.append(
            f'<rect x="0" y="252" width="382" height="156" fill="url(#{p}_stone_mid)" stroke="{INK}" stroke-width="2"/>'
            f'<rect x="578" y="252" width="382" height="156" fill="url(#{p}_stone_mid)" stroke="{INK}" stroke-width="2"/>'
            # Stone coping cap along top of walls
            f'<rect x="0" y="246" width="382" height="9" fill="#3B4D62" stroke="{INK}" stroke-width="1.4"/>'
            f'<rect x="578" y="246" width="382" height="9" fill="#3B4D62" stroke="{INK}" stroke-width="1.4"/>'
        )

        # Stone masonry coursing & buttresses on perimeter walls
        for wall_x0, wall_x1 in [(0, 382), (578, 960)]:
            for wy in range(268, 404, 18):
                orta.append(f'<line x1="{wall_x0}" y1="{wy}" x2="{wall_x1}" y2="{wy}" stroke="#141C27" stroke-width="1" opacity="0.65"/>')
                off = 16 if (wy // 18) % 2 == 0 else 0
                for wx in range(wall_x0 + off, wall_x1, 34):
                    orta.append(f'<line x1="{wx}" y1="{wy}" x2="{wx}" y2="{wy + 18}" stroke="#141C27" stroke-width="0.9" opacity="0.52"/>')
            # Heavy vertical stone buttresses
            for bx in range(wall_x0 + 48, wall_x1 - 24, 92):
                orta.append(
                    f'<rect x="{bx}" y="255" width="16" height="153" fill="#233040" stroke="{INK}" stroke-width="1.2"/>'
                    f'<line x1="{bx + 2}" y1="256" x2="{bx + 2}" y2="406" stroke="#465A72" stroke-width="1" opacity="0.45"/>'
                )

        # Concertina razor wire coils along top of both perimeter walls
        for wx0, wx1 in [(4, 376), (582, 956)]:
            # Angled support posts
            for px in range(wx0 + 14, wx1, 36):
                orta.append(f'<line x1="{px}" y1="246" x2="{px - 6}" y2="225" stroke="#4D6178" stroke-width="1.6"/>')
            # Coiled loops
            d_wire = []
            for cx in range(wx0 + 8, wx1 - 6, 13):
                d_wire.append(f"M{cx},244 C{cx - 6},224 {cx + 14},224 {cx + 8},244")
            orta.append(f'<path d="{" ".join(d_wire)}" fill="none" stroke="#7E97B3" stroke-width="1.2" opacity="0.82"/>')
            orta.append(f'<line x1="{wx0}" y1="231" x2="{wx1}" y2="231" stroke="#6B839E" stroke-width="0.9" opacity="0.65"/>')

        # 3) Central Stone Gatehouse & Heavy Iron Gate
        orta.append(
            # Flanking gatehouse turrets
            f'<rect x="372" y="210" width="34" height="198" fill="url(#{p}_tower_l)" stroke="{INK}" stroke-width="2"/>'
            f'<rect x="554" y="210" width="34" height="198" fill="url(#{p}_tower_r)" stroke="{INK}" stroke-width="2"/>'
            # Main gatehouse lintel block
            f'<rect x="404" y="220" width="152" height="188" fill="url(#{p}_stone_mid)" stroke="{INK}" stroke-width="2"/>'
            # Gothic crenellations on gatehouse top
            f'<path d="M368,210 L368,198 L382,198 L382,206 L396,206 L396,198 L410,198 L410,214 '
            f'L550,214 L550,198 L564,198 L564,206 L578,206 L578,198 L592,198 L592,210 Z" '
            f'fill="#2D3C4E" stroke="{INK}" stroke-width="1.6"/>'
            # Engraved stone plaque: FOX RIVER STATE PENITENTIARY (with crisp overhead sign wash light)
            f'<rect x="410" y="230" width="140" height="36" rx="2" fill="#131D29" stroke="#627E9B" stroke-width="1.3"/>'
            f'<rect x="410" y="230" width="140" height="36" rx="2" fill="url(#{p}_plaque_wash)"/>'
            # Twin small gooseneck sign lamps above plaque
            '<line x1="442" y1="224" x2="442" y2="230" stroke="#7A94AE" stroke-width="1.4"/>'
            '<circle cx="442" cy="230" r="2.2" fill="#E6F8FF"/>'
            '<line x1="518" y1="224" x2="518" y2="230" stroke="#7A94AE" stroke-width="1.4"/>'
            '<circle cx="518" cy="230" r="2.2" fill="#E6F8FF"/>'
            '<text x="480" y="246" text-anchor="middle" font-family="Georgia, Times New Roman, serif" '
            'font-weight="bold" font-size="12.5" letter-spacing="1.8" fill="#F2F8FF">FOX RIVER</text>'
            '<text x="480" y="259" text-anchor="middle" font-family="DejaVu Sans, Arial, sans-serif" '
            'font-weight="bold" font-size="6.6" letter-spacing="1.5" fill="#A6C4DF">STATE PENITENTIARY · EST. 1858</text>'
            # Deep arched iron gate opening
            f'<path d="M424,408 L424,302 Q480,276 536,302 L536,408 Z" fill="#090E15" stroke="{INK}" stroke-width="2.2"/>'
            # Heavy steel gate doors (closed)
            f'<rect x="428" y="304" width="51" height="104" fill="url(#{p}_gate_steel)" stroke="{INK}" stroke-width="1.4"/>'
            f'<rect x="481" y="304" width="51" height="104" fill="url(#{p}_gate_steel)" stroke="{INK}" stroke-width="1.4"/>'
        )
        # Steel vertical bars & cross braces on main gate
        for gx in range(435, 530, 9):
            orta.append(f'<line x1="{gx}" y1="305" x2="{gx}" y2="407" stroke="#0C121A" stroke-width="1.6"/>')
        orta.append(
            '<line x1="428" y1="342" x2="532" y2="342" stroke="#394B5F" stroke-width="3.2"/>'
            '<line x1="428" y1="378" x2="532" y2="378" stroke="#394B5F" stroke-width="3.2"/>'
            # Warm amber gatehouse entry lamps
            f'<circle cx="404" cy="294" r="14" fill="url(#{p}_lamp_amber)"/>'
            '<circle cx="404" cy="294" r="3.2" fill="#FFF7DE"/>'
            f'<circle cx="556" cy="294" r="14" fill="url(#{p}_lamp_amber)"/>'
            '<circle cx="556" cy="294" r="3.2" fill="#FFF7DE"/>'
        )

        # 4) Twin Towering Stone Watchtowers (Left at x=126, Right at x=834)
        for side, tx, tgrad in [("L", 126, f"{p}_tower_l"), ("R", 834, f"{p}_tower_r")]:
            orta.append(
                # Tapered heavy stone tower shaft
                f'<path d="M{tx - 38},412 L{tx - 28},166 L{tx + 28},166 L{tx + 38},412 Z" '
                f'fill="url(#{tgrad})" stroke="{INK}" stroke-width="2.2"/>'
                # Observation deck overhang & railing
                f'<rect x="{tx - 44}" y="158" width="88" height="12" rx="1" fill="#324357" stroke="{INK}" stroke-width="1.8"/>'
                f'<rect x="{tx - 48}" y="144" width="96" height="14" fill="none" stroke="#6B839C" stroke-width="1.4"/>'
            )
            # Deck railing vertical pickets
            for rx in range(tx - 44, tx + 46, 10):
                orta.append(f'<line x1="{rx}" y1="144" x2="{rx}" y2="158" stroke="#536880" stroke-width="1.1"/>')
            # Lit observation glass cab + Guard Silhouette inside
            cab_fill = "#D9F4FF" if side == "L" else "#FFE8B8"
            orta.append(
                f'<rect x="{tx - 32}" y="114" width="64" height="44" fill="#182330" stroke="{INK}" stroke-width="1.8"/>'
                f'<rect x="{tx - 28}" y="120" width="56" height="28" fill="{cab_fill}" opacity="0.62"/>'
                # Guard silhouette (head + shoulders + rifle slant)
                f'<circle cx="{tx}" cy="131" r="4.6" fill="#0B111A"/>'
                f'<path d="M{tx - 10},148 Q{tx - 8},137 {tx},137 Q{tx + 8},137 {tx + 10},148 Z" fill="#0B111A"/>'
                f'<line x1="{tx - 8}" y1="146" x2="{tx + 12}" y2="128" stroke="#0B111A" stroke-width="2"/>'
                # Window mullions over cab
                f'<line x1="{tx - 10}" y1="120" x2="{tx - 10}" y2="148" stroke="{INK}" stroke-width="1.6"/>'
                f'<line x1="{tx + 10}" y1="120" x2="{tx + 10}" y2="148" stroke="{INK}" stroke-width="1.6"/>'
                # Pyramidal Gothic stone/slate roof + antenna + red aircraft beacon
                f'<path d="M{tx - 42},116 L{tx},74 L{tx + 42},116 Z" fill="#1A2431" stroke="{INK}" stroke-width="2"/>'
                f'<path d="M{tx - 38},114 L{tx},78 L{tx + 6},114 Z" fill="#2E3E52" opacity="0.55"/>'
                f'<line x1="{tx}" y1="74" x2="{tx}" y2="48" stroke="#7A92AD" stroke-width="1.6"/>'
                f'<circle cx="{tx}" cy="48" r="9" fill="url(#{p}_red_beacon)"/>'
                f'<circle cx="{tx}" cy="48" r="2.2" fill="#FFD6DC"/>'
            )
            # Stone coursing lines on tower shaft
            for sy in range(186, 400, 22):
                orta.append(f'<line x1="{tx - 32}" y1="{sy}" x2="{tx + 32}" y2="{sy}" stroke="#121A24" stroke-width="1" opacity="0.58"/>')
            # Narrow slit windows on tower shaft
            for sy in (216, 274, 332):
                orta.append(
                    f'<rect x="{tx - 4}" y="{sy}" width="8" height="20" rx="2" fill="#F4C26B" opacity="0.52" stroke="{INK}" stroke-width="1"/>'
                )

        # 5) Wet Rain-Slicked Prison Yard Ground & Shimmering Reflections
        orta.append(f'<rect x="0" y="406" width="960" height="134" fill="url(#{p}_yard)"/>')
        # Subtle asphalt perspective lanes & wet puddle reflections
        orta.append(
            '<line x1="0" y1="408" x2="960" y2="408" stroke="#364C64" stroke-width="1.6" opacity="0.65"/>'
            # Reflected amber gatehouse lamp streaks on wet ground
            '<ellipse cx="404" cy="456" rx="18" ry="38" fill="#F4BA58" opacity="0.14"/>'
            '<ellipse cx="556" cy="456" rx="18" ry="38" fill="#F4BA58" opacity="0.14"/>'
            # Reflected cool searchlight sheen in puddles
            '<ellipse cx="290" cy="472" rx="88" ry="18" fill="#7FE6FF" opacity="0.12"/>'
            '<ellipse cx="670" cy="486" rx="96" ry="20" fill="#F8C86E" opacity="0.12"/>'
            '<ellipse cx="480" cy="494" rx="132" ry="24" fill="#9EDFFF" opacity="0.11"/>'
        )
        # Horizontal wet-ripple shimmer lines
        for _ in range(28):
            rx = rng.randint(40, 920)
            ry = rng.randint(416, 532)
            rw = rng.randint(18, 66)
            rc = "#8CD6F8" if rng.random() < 0.58 else "#F5C56F"
            orta.append(f'<line x1="{rx}" y1="{ry}" x2="{rx + rw}" y2="{ry}" stroke="{rc}" stroke-width="1" opacity="0.18"/>')

        orta.append("</g>")
        parts.append("".join(orta))

    # ── LAYER 3: sahne (Sweeping Volumetric Searchlights, Chain-Link Fence, Intense Rain) ──
    if _katman_aktif(katmanlar, "sahne"):
        sahne: list[str] = ['<g id="p01-sahne">']

        # Sweeping dual-tone volumetric searchlight cones anchored to tower decks
        # Left tower (162, 152) -> Cold icy-white main sweep down-right + secondary sky sweep
        sahne.append(
            f'<polygon points="162,150 618,494 422,520 154,158" fill="url(#{p}_beam_cool)"/>'
            f'<polygon points="154,146 530,10 648,32 162,154" fill="url(#{p}_beam_cool_up)" opacity="0.65"/>'
            # Right tower (798, 152) -> Warm amber main sweep down-left + secondary sky sweep
            f'<polygon points="798,150 318,488 504,522 806,158" fill="url(#{p}_beam_amber)"/>'
            f'<polygon points="806,146 392,8 282,36 798,154" fill="url(#{p}_beam_amber_up)" opacity="0.62"/>'
            # Ground illumination pools where beams intersect the wet yard
            '<ellipse cx="496" cy="496" rx="116" ry="22" fill="#B6ECFF" opacity="0.20"/>'
            '<ellipse cx="422" cy="498" rx="108" ry="20" fill="#FFD98E" opacity="0.18"/>'
            # Blazing searchlight lamp housings + swivel mounts on tower decks
            f'<circle cx="160" cy="152" r="26" fill="url(#{p}_lamp_cool)"/>'
            '<g transform="translate(157, 152) rotate(32)">'
            f'<rect x="-7" y="-5" width="11" height="10" rx="2" fill="#1C2836" stroke="{INK}" stroke-width="1.2"/>'
            '<ellipse cx="4" cy="0" rx="3.2" ry="5.2" fill="#FFFFFF"/>'
            '</g>'
            f'<circle cx="800" cy="152" r="26" fill="url(#{p}_lamp_amber)"/>'
            '<g transform="translate(803, 152) rotate(-32)">'
            f'<rect x="-4" y="-5" width="11" height="10" rx="2" fill="#1C2836" stroke="{INK}" stroke-width="1.2"/>'
            '<ellipse cx="-4" cy="0" rx="3.2" ry="5.2" fill="#FFF9E6"/>'
            '</g>'
        )

        # Perimeter chain-link fence silhouettes framing left and right mid-foreground (strict SVG clipPath)
        fence_segs = [(0, 148, f"{p}_fence_l"), (812, 960, f"{p}_fence_r")]
        for fx0, fx1, clip_id in fence_segs:
            # Top & mid steel rails
            sahne.append(
                f'<line x1="{fx0}" y1="312" x2="{fx1}" y2="312" stroke="#18222F" stroke-width="3.2"/>'
                f'<line x1="{fx0}" y1="428" x2="{fx1}" y2="428" stroke="#18222F" stroke-width="2.4"/>'
            )
            # Vertical fence posts
            for px in (fx0 + 18, fx1 - 18):
                sahne.append(f'<line x1="{px}" y1="296" x2="{px}" y2="540" stroke="#141D28" stroke-width="5"/>')
            # Diagonal diamond mesh cleanly clipped by SVG <clipPath>
            mesh_paths = []
            for mx in range(fx0 - 60, fx1 + 60, 16):
                mesh_paths.append(f"M{mx},312 L{mx + 56},540")
                mesh_paths.append(f"M{mx + 56},312 L{mx},540")
            sahne.append(
                f'<g clip-path="url(#{clip_id})">'
                f'<path d="{" ".join(mesh_paths)}" fill="none" stroke="#364B63" stroke-width="1.0" opacity="0.52"/>'
                '</g>'
            )

        # Heavy cinematic diagonal rain streaks (brighter inside searchlight cones)
        for _ in range(150):
            rx = rng.randint(-20, 980)
            ry = rng.randint(-20, 520)
            rl = rng.randint(24, 52)
            # Check if near central beam crossing for brighter specular rain highlight
            in_beam = (180 < rx < 780) and (150 < ry < 500)
            col = "#D8F4FF" if (in_beam and rng.random() < 0.45) else "#8AC2E3"
            op = rng.uniform(0.32, 0.62) if in_beam else rng.uniform(0.14, 0.30)
            sw = 1.3 if in_beam else 0.9
            sahne.append(
                f'<line x1="{rx}" y1="{ry}" x2="{rx - int(rl * 0.30)}" y2="{ry + rl}" '
                f'stroke="{col}" stroke-width="{sw}" opacity="{op:.2f}" stroke-linecap="round"/>'
            )

        # Rain splash micro-arcs on wet yard & wall ledges
        for _ in range(26):
            sx = rng.randint(60, 900)
            sy = rng.randint(422, 530)
            sahne.append(
                f'<ellipse cx="{sx}" cy="{sy}" rx="{rng.randint(3, 7)}" ry="1.4" '
                'fill="none" stroke="#A6E0FF" stroke-width="0.9" opacity="0.34"/>'
            )

        sahne.append("</g>")
        parts.append("".join(sahne))

    # ── LAYER 4: plan (#7FE6FF Multi-Layer Architectural CAD X-Ray Blueprint) ──
    if _katman_aktif(katmanlar, "plan"):
        plan: list[str] = ['<g id="p01-plan">']

        # X-Ray blueprint cutout panels over left wall, underground yard tunnel & right infirmary wing
        plan.append(
            # Left X-Ray section (Cell Block -> Pipe Shaft)
            f'<rect x="176" y="264" width="192" height="134" fill="url(#{p}_xray_fill)" stroke="{PLAN}" stroke-width="1.3" opacity="0.88"/>'
            # Right X-Ray section (Infirmary Wall & Outer Perimeter)
            f'<rect x="592" y="264" width="192" height="134" fill="url(#{p}_xray_fill)" stroke="{PLAN}" stroke-width="1.3" opacity="0.88"/>'
            # Underground yard utility tunnel X-Ray strip
            f'<path d="M294,408 L666,408 L718,472 L242,472 Z" fill="#061D30" fill-opacity="0.56" stroke="{PLAN}" stroke-width="1.2" stroke-dasharray="6,4" opacity="0.85"/>'
        )

        # Architectural blueprint micro-grid inside left & right X-Ray boxes
        grid_lines = []
        for gx0, gx1 in [(176, 368), (592, 784)]:
            for x in range(gx0 + 16, gx1, 16):
                grid_lines.append(f"M{x},264 L{x},398")
            for y in range(280, 398, 16):
                grid_lines.append(f"M{gx0},{y} L{gx1},{y}")
        plan.append(f'<path d="{" ".join(grid_lines)}" fill="none" stroke="{PLAN}" stroke-width="0.5" opacity="0.24"/>')

        # Detailed CAD structural internals:
        # Left box: Cell A-40 floor plan + sink bolt + vertical/horizontal pipe shaft
        plan.append(
            f'<g stroke="{PLAN}" fill="none" opacity="0.86">'
            # Cell A-40 structural bay
            '<rect x="192" y="282" width="62" height="44" stroke-width="1.2"/>'
            '<line x1="204" y1="282" x2="204" y2="326" stroke-width="0.8" stroke-dasharray="3,2"/>'
            '<circle cx="242" cy="304" r="5" stroke-width="1.2"/>'
            # Pipe shaft vertical riser & elbow conduit
            '<path d="M254,304 L298,304 L298,398" stroke-width="1.4"/>'
            '<path d="M254,312 L290,312 L290,398" stroke-width="1.4"/>'
            # Valve flange cross-marks on pipe
            '<line x1="286" y1="336" x2="302" y2="336" stroke-width="1.3"/>'
            '<line x1="286" y1="364" x2="302" y2="364" stroke-width="1.3"/>'
            # Structural wall section hatching on right box (Infirmary & Outer Wall)
            '<rect x="614" y="286" width="84" height="58" stroke-width="1.2"/>'
            '<line x1="656" y1="286" x2="656" y2="344" stroke-width="0.9" stroke-dasharray="3,2"/>'
            '<path d="M698,314 L758,314 L758,368" stroke-width="1.4"/>'
            # Target exit ring at 04 WALL
            '<circle cx="758" cy="314" r="11" stroke-width="1.2" stroke-dasharray="4,2"/>'
            '<circle cx="758" cy="314" r="18" stroke-width="0.7" opacity="0.55"/>'
            # Underground tunnel perspective ribs
            '<line x1="340" y1="408" x2="314" y2="472" stroke-width="0.8" opacity="0.5"/>'
            '<line x1="480" y1="408" x2="480" y2="472" stroke-width="0.8" opacity="0.5"/>'
            '<line x1="620" y1="408" x2="646" y2="472" stroke-width="0.8" opacity="0.5"/>'
            '</g>'
        )

        # GLOWING DASHED ESCAPE ROUTE connecting 01 CELL -> 02 PIPE -> 03 TUNNEL -> 04 WALL
        route_d = "M224,304 L294,304 L294,440 L634,440 L634,314 L758,314"
        plan.append(
            f'<path d="{route_d}" fill="none" stroke="{PLAN}" stroke-width="6.5" opacity="0.18" stroke-linejoin="round"/>'
            f'<path d="{route_d}" fill="none" stroke="{PLAN_CORE}" stroke-width="2.2" stroke-dasharray="8,5" stroke-linejoin="round"/>'
            # Directional arrowheads along the escape route
            f'<path d="M448,434 L460,440 L448,446" fill="none" stroke="{PLAN_CORE}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="M538,434 L550,440 L538,446" fill="none" stroke="{PLAN_CORE}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="M718,308 L730,314 L718,320" fill="none" stroke="{PLAN_CORE}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
        )

        # 4 Numbered Blueprint Nodes + Crisp Technical Callout Badges
        nodes = [
            (224, 304, 186, 276, "01 · CELL"),
            (294, 356, 308, 352, "02 · PIPE"),
            (480, 440, 434, 464, "03 · TUNNEL"),
            (758, 314, 704, 276, "04 · WALL"),
        ]
        for nx, ny, lx, ly, label in nodes:
            plan.append(
                f'<circle cx="{nx}" cy="{ny}" r="7.5" fill="#071B2C" stroke="{PLAN}" stroke-width="1.6"/>'
                f'<circle cx="{nx}" cy="{ny}" r="3.0" fill="{PLAN_CORE}"/>'
                f'<rect x="{lx - 4}" y="{ly - 11}" width="76" height="15" rx="2" fill="#061826" fill-opacity="0.88" stroke="{PLAN}" stroke-width="0.9"/>'
                f'<text x="{lx + 34}" y="{ly}" text-anchor="middle" font-family="DejaVu Sans Mono, Consolas, monospace" '
                f'font-weight="bold" font-size="8.2" letter-spacing="0.6" fill="{PLAN_CORE}">{label}</text>'
            )

        # Architectural elevation & dimension callout lines across the fortress
        plan.append(
            f'<g stroke="{PLAN}" fill="none" opacity="0.58">'
            '<line x1="126" y1="62" x2="126" y2="38" stroke-width="0.9" stroke-dasharray="2,2"/>'
            '<line x1="834" y1="62" x2="834" y2="38" stroke-width="0.9" stroke-dasharray="2,2"/>'
            '<line x1="126" y1="42" x2="340" y2="42" stroke-width="0.9"/>'
            '<line x1="620" y1="42" x2="834" y2="42" stroke-width="0.9"/>'
            '</g>'
            '<rect x="348" y="31" width="264" height="22" rx="2" fill="#061726" fill-opacity="0.82" stroke="#7FE6FF" stroke-width="1"/>'
            f'<text x="480" y="45" text-anchor="middle" font-family="DejaVu Sans Mono, Consolas, monospace" '
            f'font-weight="bold" font-size="9.5" letter-spacing="1.6" fill="{PLAN_CORE}">FOX RIVER · STRUCTURAL PLAN // BY HEART</text>'
        )

        plan.append("</g>")
        parts.append("".join(plan))

    # ── LAYER 5: onplan (Foreground Dark Razor-Wire Framing + Corner Technical HUD + Vignette) ──
    if _katman_aktif(katmanlar, "onplan"):
        onplan: list[str] = ['<g id="p01-onplan">']

        # Cinematic dark vignette
        onplan.append(f'<rect x="0" y="0" width="960" height="540" fill="url(#{p}_vig)"/>')

        # Foreground out-of-focus / dark razor-wire framing strands in top-left & top-right corners
        onplan.append(
            '<path d="M-10,58 Q88,34 196,12" fill="none" stroke="#080D14" stroke-width="4.2" opacity="0.82"/>'
            '<path d="M-10,82 Q76,62 164,40" fill="none" stroke="#080D14" stroke-width="2.6" opacity="0.72"/>'
            '<path d="M970,58 Q872,34 764,12" fill="none" stroke="#080D14" stroke-width="4.2" opacity="0.82"/>'
            '<path d="M970,82 Q884,62 796,40" fill="none" stroke="#080D14" stroke-width="2.6" opacity="0.72"/>'
            # Barbs along foreground wire
            '<path d="M44,44 L54,54 M54,44 L44,54 M114,28 L124,38 M124,28 L114,38" fill="none" stroke="#16212E" stroke-width="2.4" opacity="0.8"/>'
            '<path d="M906,44 L916,54 M916,44 L906,54 M836,28 L846,38 M846,28 L836,38" fill="none" stroke="#16212E" stroke-width="2.4" opacity="0.8"/>'
        )

        # Crisp four-corner #7FE6FF technical HUD brackets & micro telemetry
        onplan.append(
            f'<g stroke="{PLAN}" fill="none" stroke-width="1.6" opacity="0.72">'
            '<path d="M18,42 L18,18 L44,18"/>'
            '<path d="M916,18 L942,18 L942,42"/>'
            '<path d="M18,498 L18,522 L44,522"/>'
            '<path d="M916,522 L942,522 L942,498"/>'
            '</g>'
            f'<text x="26" y="514" font-family="DejaVu Sans Mono, Consolas, monospace" font-size="8.2" letter-spacing="1.0" fill="{PLAN}" opacity="0.78">SECTOR 01 · MAX SECURITY · WALL EL +14.2M</text>'
            f'<text x="934" y="514" text-anchor="end" font-family="DejaVu Sans Mono, Consolas, monospace" font-size="8.2" letter-spacing="1.0" fill="{PLAN}" opacity="0.78">ESCAPE ROUTE: 4 NODES LOCKED</text>'
        )

        onplan.append("</g>")
        parts.append("".join(onplan))

    return defs, "".join(parts)


# =============================================================================
# SCENE P04: DARK CLOSET FLOOR & 11YO SNEAKERS ("AGE 11")
# =============================================================================
def set_p04_depo_zemin(
    katmanlar: set[str] | list[str] | None = None,
) -> tuple[str, str]:
    """Atmospheric dark wooden storage closet floor with golden under-door light spill
    and high-detail worn 11-year-old sneakers (cream vulcanized rubber soles, laced canvas,
    dark denim jeans cuffs & realistic contact shadows) standing at the edge of the light.
    - uzak:   Deep dark timber closet backdrop & ceiling rafters
    - orta:   Splintered dark wooden walls, dusty stacked crates, heavy wooden closet door
              with rusty iron bolt lock & perspective floorboards
    - sahne:  Blazing golden light beam spilling from under the door onto wooden planks +
              high-detail worn child's sneakers, indigo denim cuffs & layered contact shadows
    - plan:   Floating golden dust motes in the light cone + subtle cyan observation micro-marks
    - onplan: Foreground dark crate silhouette framing & cinematic vignette
    """
    rng = random.Random(404)
    p = _uid("p04")

    defs = f"""
    <linearGradient id="{p}_bg_wall" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#060A0F"/>
      <stop offset="55%" stop-color="#0E151E"/>
      <stop offset="100%" stop-color="#171B20"/>
    </linearGradient>
    <linearGradient id="{p}_side_wood_l" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#090D12"/>
      <stop offset="68%" stop-color="#161C24"/>
      <stop offset="100%" stop-color="#22262B"/>
    </linearGradient>
    <linearGradient id="{p}_side_wood_r" x1="1" y1="0" x2="0" y2="0">
      <stop offset="0%" stop-color="#090D12"/>
      <stop offset="68%" stop-color="#161C24"/>
      <stop offset="100%" stop-color="#22262B"/>
    </linearGradient>
    <linearGradient id="{p}_door_wood" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#1C1919"/>
      <stop offset="64%" stop-color="#28211E"/>
      <stop offset="92%" stop-color="#3E2D1E"/>
      <stop offset="100%" stop-color="#6B4A27"/>
    </linearGradient>
    <linearGradient id="{p}_floor_base" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#241D18"/>
      <stop offset="45%" stop-color="#171413"/>
      <stop offset="100%" stop-color="#0B0B0D"/>
    </linearGradient>
    <linearGradient id="{p}_gold_spill" x1="0.5" y1="0" x2="0.5" y2="1">
      <stop offset="0%" stop-color="#FFFBE8" stop-opacity="0.98"/>
      <stop offset="10%" stop-color="#FFE394" stop-opacity="0.88"/>
      <stop offset="38%" stop-color="#F2B957" stop-opacity="0.52"/>
      <stop offset="76%" stop-color="#B87426" stop-opacity="0.18"/>
      <stop offset="100%" stop-color="#5E3610" stop-opacity="0.0"/>
    </linearGradient>
    <linearGradient id="{p}_gold_cone" x1="0.5" y1="0" x2="0.5" y2="1">
      <stop offset="0%" stop-color="#FFF4C8" stop-opacity="0.54"/>
      <stop offset="36%" stop-color="#F7C264" stop-opacity="0.20"/>
      <stop offset="100%" stop-color="#C87E2A" stop-opacity="0.0"/>
    </linearGradient>
    <radialGradient id="{p}_door_bloom" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0%" stop-color="#FFFDF0" stop-opacity="0.95"/>
      <stop offset="35%" stop-color="#FFD97D" stop-opacity="0.52"/>
      <stop offset="100%" stop-color="#E59836" stop-opacity="0.0"/>
    </radialGradient>
    <linearGradient id="{p}_crate_dark" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#26201C"/>
      <stop offset="55%" stop-color="#191615"/>
      <stop offset="100%" stop-color="#0E0D0E"/>
    </linearGradient>
    <linearGradient id="{p}_rust_iron" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#6B442C"/>
      <stop offset="45%" stop-color="#3E2A22"/>
      <stop offset="100%" stop-color="#1E1919"/>
    </linearGradient>
    <linearGradient id="{p}_denim" x1="0" y1="0.85" x2="0.9" y2="0.05">
      <stop offset="0%" stop-color="#283C5A"/>
      <stop offset="32%" stop-color="#1E2E46"/>
      <stop offset="68%" stop-color="#111A28"/>
      <stop offset="100%" stop-color="#070B11"/>
    </linearGradient>
    <linearGradient id="{p}_denim_back" x1="0" y1="0.9" x2="0.9" y2="0.05">
      <stop offset="0%" stop-color="#1D2C42"/>
      <stop offset="42%" stop-color="#121C2B"/>
      <stop offset="100%" stop-color="#06090E"/>
    </linearGradient>
    <linearGradient id="{p}_denim_cuff" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#283A54"/>
      <stop offset="45%" stop-color="#3F5878"/>
      <stop offset="100%" stop-color="#1A2638"/>
    </linearGradient>
    <linearGradient id="{p}_canvas" x1="0" y1="0" x2="0.8" y2="1">
      <stop offset="0%" stop-color="#344354"/>
      <stop offset="52%" stop-color="#222C38"/>
      <stop offset="100%" stop-color="#141A22"/>
    </linearGradient>
    <linearGradient id="{p}_rubber" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#EFE7D6"/>
      <stop offset="48%" stop-color="#DDD1B8"/>
      <stop offset="100%" stop-color="#AFA084"/>
    </linearGradient>
    <linearGradient id="{p}_rubber_toe" x1="0.2" y1="0" x2="0.8" y2="1">
      <stop offset="0%" stop-color="#F7F0E0"/>
      <stop offset="58%" stop-color="#DCD0B6"/>
      <stop offset="100%" stop-color="#9E8F75"/>
    </linearGradient>
    <radialGradient id="{p}_vig" cx="0.5" cy="0.54" r="0.68">
      <stop offset="42%" stop-color="#000000" stop-opacity="0.0"/>
      <stop offset="82%" stop-color="#05070B" stop-opacity="0.62"/>
      <stop offset="100%" stop-color="#030508" stop-opacity="0.90"/>
    </radialGradient>
    """

    parts: list[str] = []

    # ── LAYER 1: uzak (Dark splintered timber back wall & rafters) ──
    if _katman_aktif(katmanlar, "uzak"):
        uzak: list[str] = ['<g id="p04-uzak">']
        uzak.append(f'<rect x="0" y="0" width="960" height="540" fill="url(#{p}_bg_wall)"/>')
        # Back vertical plank grooves
        for x in range(210, 760, 28):
            uzak.append(f'<line x1="{x}" y1="0" x2="{x}" y2="302" stroke="#080C12" stroke-width="1.6"/>')
            uzak.append(f'<line x1="{x + 2}" y1="0" x2="{x + 2}" y2="302" stroke="#242E3B" stroke-width="0.7" opacity="0.34"/>')
        # Overhead dark timber rafter beam
        uzak.append(
            f'<rect x="0" y="0" width="960" height="36" fill="#090D13" stroke="{INK}" stroke-width="1.5"/>'
            '<line x1="0" y1="36" x2="960" y2="36" stroke="#263140" stroke-width="1" opacity="0.45"/>'
        )
        uzak.append("</g>")
        parts.append("".join(uzak))

    # ── LAYER 2: orta (Perspective Closet Walls, Heavy Door + Rusty Bolt, Dusty Crates, Floorboards) ──
    if _katman_aktif(katmanlar, "orta"):
        orta: list[str] = ['<g id="p04-orta">']

        # Perspective left & right dark timber walls
        orta.append(
            f'<polygon points="0,0 226,48 226,296 0,432" fill="url(#{p}_side_wood_l)" stroke="{INK}" stroke-width="2"/>'
            f'<polygon points="960,0 734,48 734,296 960,432" fill="url(#{p}_side_wood_r)" stroke="{INK}" stroke-width="2"/>'
        )
        # Vertical splintered planks on side walls
        for t in (0.16, 0.34, 0.52, 0.70, 0.86):
            lx = int(226 * t)
            ly0 = int(48 * t)
            ly1 = int(432 - (432 - 296) * t)
            orta.append(f'<line x1="{lx}" y1="{ly0}" x2="{lx}" y2="{ly1}" stroke="#070A0F" stroke-width="1.8"/>')
            rx = int(960 - 226 * t)
            orta.append(f'<line x1="{rx}" y1="{ly0}" x2="{rx}" y2="{ly1}" stroke="#070A0F" stroke-width="1.8"/>')

        # Perspective wooden floor base (y=296 to y=540)
        orta.append(f'<polygon points="0,432 226,296 734,296 960,432 960,540 0,540" fill="url(#{p}_floor_base)"/>')

        # Perspective floorboard plank seams radiating from the closet door vanishing zone
        vp_x, vp_y = 480, 148
        for fx_bot in range(-280, 1260, 76):
            # Intersect ray (vp_x, vp_y) -> (fx_bot, 540) with y=296
            t_top = (296 - vp_y) / (540 - vp_y)
            fx_top = vp_x + (fx_bot - vp_x) * t_top
            orta.append(
                f'<line x1="{fx_top:.1f}" y1="296" x2="{fx_bot}" y2="540" stroke="#090A0D" stroke-width="2.0"/>'
                f'<line x1="{fx_top + 1.5:.1f}" y1="296" x2="{fx_bot + 2}" y2="540" stroke="#362A20" stroke-width="0.9" opacity="0.45"/>'
            )
        # Cross butt-joints & subtle wood knots/grain cracks on floorboards
        for fy in (328, 368, 418, 476):
            for _ in range(4):
                jx = rng.randint(150, 810)
                orta.append(f'<line x1="{jx}" y1="{fy}" x2="{jx + rng.randint(36, 62)}" y2="{fy}" stroke="#0B0B0E" stroke-width="1.4" opacity="0.72"/>')
        # Subtle floorboard grain cracks
        for _ in range(18):
            gx = rng.randint(180, 780)
            gy = rng.randint(310, 515)
            dx = (gx - 480) * 0.14
            orta.append(
                f'<path d="M{gx},{gy} Q{gx + dx * 0.5:.1f},{gy + 16} {gx + dx:.1f},{gy + 34}" '
                'fill="none" stroke="#2D2219" stroke-width="1.0" opacity="0.42"/>'
            )

        # HEAVY WOODEN CLOSET DOOR (center: x=362..598, y=56..292 — leaving bright 6px gap at bottom!)
        orta.append(
            # Heavy wooden doorframe casing
            f'<rect x="346" y="42" width="268" height="254" fill="#13161B" stroke="{INK}" stroke-width="2.2"/>'
            # Thin golden light bleed around top & side door gaps
            '<rect x="360" y="54" width="240" height="240" fill="none" stroke="#F6C56B" stroke-width="1.3" opacity="0.34"/>'
            # Solid timber door slab (ends at y=289 for blazing under-door light slit)
            f'<rect x="362" y="56" width="236" height="233" fill="url(#{p}_door_wood)" stroke="{INK}" stroke-width="2"/>'
        )
        # Vertical heavy door planks + nail studs
        for dx in range(392, 596, 30):
            orta.append(f'<line x1="{dx}" y1="56" x2="{dx}" y2="289" stroke="#110E0D" stroke-width="1.8"/>')
        # Horizontal braced crossbars & diagonal Z-brace on door
        orta.append(
            f'<rect x="364" y="88" width="232" height="22" fill="#231D1A" stroke="{INK}" stroke-width="1.6"/>'
            f'<rect x="364" y="232" width="232" height="24" fill="#28201B" stroke="{INK}" stroke-width="1.6"/>'
            f'<polygon points="374,232 564,110 584,110 394,232" fill="#211B18" stroke="{INK}" stroke-width="1.4"/>'
            # Heavy iron strap hinges on left edge
            f'<rect x="352" y="92" width="46" height="14" rx="2" fill="url(#{p}_rust_iron)" stroke="{INK}" stroke-width="1.4"/>'
            f'<rect x="352" y="236" width="46" height="14" rx="2" fill="url(#{p}_rust_iron)" stroke="{INK}" stroke-width="1.4"/>'
            '<circle cx="364" cy="99" r="2.2" fill="#111010"/><circle cx="386" cy="99" r="2.2" fill="#111010"/>'
            '<circle cx="364" cy="243" r="2.2" fill="#111010"/><circle cx="386" cy="243" r="2.2" fill="#111010"/>'
        )

        # RUSTY HEAVY IRON SLIDE BOLT LOCK & PADLOCK on right side of closet door (x=554, y=184)
        orta.append(
            f'<g transform="translate(550, 176)">'
            f'<rect x="0" y="0" width="54" height="24" rx="2" fill="url(#{p}_rust_iron)" stroke="{INK}" stroke-width="1.5"/>'
            # Steel slide bar pushed into frame staple
            f'<rect x="6" y="7" width="56" height="9" rx="3" fill="#4E392E" stroke="{INK}" stroke-width="1.3"/>'
            '<line x1="8" y1="9" x2="58" y2="9" stroke="#9E7354" stroke-width="1.1" opacity="0.6"/>'
            # Bolt handle knob
            f'<circle cx="18" cy="11.5" r="5.5" fill="#63402C" stroke="{INK}" stroke-width="1.4"/>'
            # Rusty staple & hanging heavy padlock
            f'<rect x="44" y="4" width="10" height="16" rx="2" fill="#2C221E" stroke="{INK}" stroke-width="1.2"/>'
            '<path d="M46,18 C46,28 54,28 54,18" fill="none" stroke="#6E5242" stroke-width="2.4"/>'
            f'<rect x="42" y="24" width="16" height="18" rx="3" fill="url(#{p}_rust_iron)" stroke="{INK}" stroke-width="1.4"/>'
            '<circle cx="50" cy="32" r="2" fill="#0B0A0A"/>'
            '<line x1="50" y1="33" x2="50" y2="38" stroke="#0B0A0A" stroke-width="1.6"/>'
            '</g>'
        )

        # DUSTY STACKED WOODEN CRATES (Left side & Right side, catching warm rim light)
        # Left stacked crates
        orta.append(
            # Lower large crate
            f'<polygon points="48,374 238,374 268,342 268,246 86,246 48,274" fill="url(#{p}_crate_dark)" stroke="{INK}" stroke-width="2"/>'
            f'<rect x="48" y="274" width="190" height="100" fill="#171516" stroke="{INK}" stroke-width="1.8"/>'
            # Crate horizontal slats & diagonal brace
            '<line x1="48" y1="308" x2="238" y2="308" stroke="#0D0C0D" stroke-width="2"/>'
            '<line x1="48" y1="342" x2="238" y2="342" stroke="#0D0C0D" stroke-width="2"/>'
            '<line x1="54" y1="280" x2="232" y2="368" stroke="#241F1C" stroke-width="4" opacity="0.65"/>'
            # Golden rim light catching inner edge of left crate
            '<line x1="238" y1="274" x2="238" y2="374" stroke="#E9B25A" stroke-width="2.0" opacity="0.62"/>'
            '<line x1="238" y1="274" x2="268" y2="246" stroke="#E9B25A" stroke-width="1.2" opacity="0.40"/>'
            # Upper smaller wooden box perched on top
            f'<polygon points="88,266 226,266 250,242 250,180 118,180 88,200" fill="url(#{p}_crate_dark)" stroke="{INK}" stroke-width="1.8"/>'
            f'<rect x="88" y="200" width="138" height="66" fill="#1D1918" stroke="{INK}" stroke-width="1.6"/>'
            '<line x1="226" y1="200" x2="226" y2="266" stroke="#D9A350" stroke-width="1.5" opacity="0.48"/>'
        )
        # Right stacked crate + wall shelf
        orta.append(
            f'<polygon points="724,380 908,380 908,266 868,242 694,242 694,344" fill="url(#{p}_crate_dark)" stroke="{INK}" stroke-width="2"/>'
            f'<rect x="724" y="266" width="184" height="114" fill="#151416" stroke="{INK}" stroke-width="1.8"/>'
            '<line x1="724" y1="304" x2="908" y2="304" stroke="#0B0B0D" stroke-width="2"/>'
            '<line x1="724" y1="342" x2="908" y2="342" stroke="#0B0B0D" stroke-width="2"/>'
            # Golden rim light catching inner edge of right crate
            '<line x1="724" y1="266" x2="724" y2="380" stroke="#E9B25A" stroke-width="2.0" opacity="0.60"/>'
            '<line x1="694" y1="242" x2="694" y2="344" stroke="#E9B25A" stroke-width="1.5" opacity="0.45"/>'
            # High dark wooden shelf on right wall with dusty jars/boxes
            f'<polygon points="756,162 936,136 936,152 756,174" fill="#1B191B" stroke="{INK}" stroke-width="1.6"/>'
            f'<rect x="786" y="128" width="32" height="34" rx="2" fill="#14181E" stroke="{INK}" stroke-width="1.4"/>'
            f'<rect x="832" y="114" width="44" height="42" rx="2" fill="#1C1A1C" stroke="{INK}" stroke-width="1.4"/>'
        )

        # Delicate cobweb in upper-left door corner
        orta.append(
            '<path d="M226,48 L296,62 M226,48 L280,98 M226,48 L254,122 '
            'M250,53 Q246,72 238,84 M272,58 Q264,84 246,102" '
            'fill="none" stroke="#6E7C8C" stroke-width="0.7" opacity="0.28"/>'
        )

        orta.append("</g>")
        parts.append("".join(orta))

    # ── LAYER 3: sahne (Blazing Golden Under-Door Light Spill + High-Detail 11yo Sneakers & Denim Cuffs) ──
    if _katman_aktif(katmanlar, "sahne"):
        sahne: list[str] = ['<g id="p04-sahne">']

        # 1) Blazing Under-Door Light Slit & Golden Floor Light Carpet
        sahne.append(
            # Soft wide bloom around door threshold
            f'<ellipse cx="480" cy="296" rx="196" ry="38" fill="url(#{p}_door_bloom)"/>'
            # Golden light carpet spilling across the wooden floorboards
            f'<polygon points="358,292 602,292 786,540 174,540" fill="url(#{p}_gold_spill)"/>'
            # Volumetric god-ray light shafts angled through the dusty air
            f'<polygon points="366,292 436,292 314,540 198,540" fill="url(#{p}_gold_cone)" opacity="0.52"/>'
            f'<polygon points="452,292 528,292 562,540 416,540" fill="url(#{p}_gold_cone)" opacity="0.62"/>'
            f'<polygon points="544,292 596,292 752,540 644,540" fill="url(#{p}_gold_cone)" opacity="0.48"/>'
            # Blazing bright white-gold light slit directly under the door
            '<rect x="360" y="288" width="240" height="8" rx="3" fill="#FFFDF2"/>'
            '<rect x="356" y="286" width="248" height="12" rx="5" fill="#FFE696" opacity="0.58"/>'
        )

        # Illuminated floorboard highlight streaks inside the golden beam
        for bx0, bx1 in [(386, 286), (434, 384), (482, 484), (530, 586), (576, 684)]:
            sahne.append(
                f'<line x1="{bx0}" y1="296" x2="{bx1}" y2="540" stroke="#FFE9A8" stroke-width="1.3" opacity="0.22"/>'
            )

        # 2) HIGH-DETAIL WORN 11YO CHILD'S SNEAKERS + DARK INDIGO DENIM LEGS + CONTACT SHADOWS
        # Child sitting tucked in the dark right shadow of the closet, knees drawn up slightly,
        # denim legs fading naturally into the dark right-side shadow (NO floating cut-off edges!),
        # worn sneakers resting right at the edge of the golden under-door light pool.
        # Unified inside p04-sahne (R4-PARALLAX compliant).
        sahne.append('<g id="p04-sneakers-11yo">')

        # A) Realistic layered contact shadows + long cast shadows stretching down-right away from door light
        sahne.append(
            '<ellipse cx="584" cy="496" rx="64" ry="19" fill="#040507" opacity="0.68" transform="rotate(8 584 496)"/>'
            '<ellipse cx="678" cy="482" rx="58" ry="17" fill="#040507" opacity="0.70" transform="rotate(13 678 482)"/>'
            # Tight ambient-occlusion contact shadows directly underneath both rubber soles
            '<path d="M494,474 C510,488 574,492 618,482 C628,478 628,468 616,464 L506,462 Z" fill="#030406" opacity="0.92"/>'
            '<path d="M604,454 C618,470 676,478 716,468 C726,464 726,454 712,448 L616,442 Z" fill="#030406" opacity="0.92"/>'
        )

        # B) BACK / RIGHT LEG & SNEAKER (tucked slightly behind & to the right, distinct slim child jeans leg)
        sahne.append(
            '<g id="p04-shoe-right">'
            # Slim bent child's right shin & knee curving cleanly into the dark right-side shadow
            f'<path d="M652,412 L688,334 C698,314 720,308 746,316 L846,356 L836,412 L746,368 L716,414 Z" '
            f'fill="url(#{p}_denim_back)" stroke="#0A0E14" stroke-width="1.6" stroke-linejoin="round"/>'
            # Knee & shin crease folds + warm golden rim highlight on front shin edge
            '<path d="M680,356 Q708,354 734,366 M706,326 Q734,332 762,348" fill="none" stroke="#080C12" stroke-width="1.8" opacity="0.72"/>'
            '<path d="M654,408 L689,335 C696,321 709,314 724,314" fill="none" stroke="#E5B25C" stroke-width="1.7" opacity="0.48" stroke-linecap="round"/>'
            # Rolled/hemmed denim cuff with ochre double-stitching
            f'<path d="M644,406 C666,416 706,416 724,404 L722,422 C704,432 664,432 642,422 Z" fill="url(#{p}_denim_cuff)" stroke="{INK_WARM}" stroke-width="2"/>'
            '<path d="M647,416 C668,425 702,425 720,415" fill="none" stroke="#C48F46" stroke-width="1.2" stroke-dasharray="4,2" opacity="0.85"/>'
            # Canvas sneaker upper body
            f'<path d="M648,416 C638,428 626,438 614,446 C608,450 610,462 624,466 L718,462 C726,458 726,440 720,422 Z" '
            f'fill="url(#{p}_canvas)" stroke="{INK_WARM}" stroke-width="2.2" stroke-linejoin="round"/>'
            '<path d="M694,424 C700,438 702,450 698,458" fill="none" stroke="#6E8299" stroke-width="1.1" stroke-dasharray="3,2" opacity="0.65"/>'
            '<path d="M644,426 C656,436 664,448 666,456" fill="none" stroke="#6E8299" stroke-width="1.1" stroke-dasharray="3,2" opacity="0.62"/>'
            # Vintage ankle patch
            '<circle cx="684" cy="438" r="7.5" fill="#DDD2BC" stroke="#1E2530" stroke-width="1.2" opacity="0.85"/>'
            '<circle cx="684" cy="438" r="3.2" fill="#2A3A4E" opacity="0.8"/>'
            # Cream rubber toe cap
            f'<path d="M612,448 C614,436 632,432 644,438 C652,442 652,456 642,460 L614,458 Z" '
            f'fill="url(#{p}_rubber_toe)" stroke="{INK_WARM}" stroke-width="1.8"/>'
            '<path d="M618,442 C626,438 636,438 642,442" fill="none" stroke="#FFF9E6" stroke-width="1.5" opacity="0.78"/>'
            # Vulcanized cream rubber midsole + black foxing stripe + scuffs
            f'<path d="M612,452 C640,460 692,460 724,450 L724,464 C692,474 638,474 612,464 Z" '
            f'fill="url(#{p}_rubber)" stroke="{INK_WARM}" stroke-width="2"/>'
            '<path d="M613,457 C640,465 692,465 723,455" fill="none" stroke="#22252A" stroke-width="1.6" opacity="0.85"/>'
            '<path d="M666,466 L682,464 M632,462 L644,464" fill="none" stroke="#7A6D58" stroke-width="1.4" opacity="0.58"/>'
            # Eyelets + crisscrossed laces + loose bow
            '<circle cx="644" cy="435" r="1.8" fill="#B5C0CC"/><circle cx="651" cy="429" r="1.8" fill="#B5C0CC"/><circle cx="658" cy="423" r="1.8" fill="#B5C0CC"/>'
            '<path d="M638,438 L652,432 M644,432 L658,426 M650,426 L664,420" fill="none" stroke="#EFE6D2" stroke-width="2.1" stroke-linecap="round"/>'
            '<path d="M648,428 C636,426 632,434 642,438 M648,428 C636,438 634,448 638,454" fill="none" stroke="#E6DAC2" stroke-width="1.5" stroke-linecap="round"/>'
            '<path d="M614,448 C624,436 640,428 650,418" fill="none" stroke="#FFE196" stroke-width="1.6" opacity="0.72" stroke-linecap="round"/>'
            '</g>'
        )

        # C) FRONT / LEFT LEG & SNEAKER (distinct slim child jeans leg + knee, never obscuring right shoe!)
        sahne.append(
            '<g id="p04-shoe-left">'
            # Slim child's left shin rising cleanly to bent knee, then thigh receding to dark right shadow
            f'<path d="M532,424 L568,334 C578,312 602,306 630,316 L764,378 L748,438 L636,374 L608,424 Z" '
            f'fill="url(#{p}_denim)" stroke="#0B1018" stroke-width="1.9" stroke-linejoin="round"/>'
            # Natural denim fabric folds at bent knee & inner crease
            '<path d="M562,368 Q594,364 624,376 M588,332 Q620,336 654,354 M636,374 L668,392" '
            'fill="none" stroke="#0C1320" stroke-width="2.0" opacity="0.74" stroke-linecap="round"/>'
            # Subtle denim outseam double-stitching along shin
            '<path d="M558,420 L586,342" fill="none" stroke="#4D688C" stroke-width="1.0" stroke-dasharray="3,2" opacity="0.52"/>'
            # Bright golden door-light rim highlight hugging the front shin & knee curve
            '<path d="M534,420 L569,336 C576,320 590,312 610,312" fill="none" stroke="#FFD985" stroke-width="2.5" opacity="0.80" stroke-linecap="round"/>'
            # Slightly frayed rolled denim cuff + ochre stitching
            f'<path d="M526,420 C550,430 594,430 616,418 L614,438 C592,448 548,448 524,436 Z" fill="url(#{p}_denim_cuff)" stroke="{INK_WARM}" stroke-width="2.1"/>'
            '<path d="M530,431 C552,440 590,440 611,430" fill="none" stroke="#D19A4E" stroke-width="1.3" stroke-dasharray="4,2" opacity="0.9"/>'
            # Canvas sneaker main body (classic worn high-top silhouette)
            f'<path d="M532,432 C520,444 506,454 494,462 C488,468 492,480 506,484 L610,480 C620,474 620,454 612,436 Z" '
            f'fill="url(#{p}_canvas)" stroke="{INK_WARM}" stroke-width="2.3" stroke-linejoin="round"/>'
            # Canvas panel double-stitch lines & subtle wear creases
            '<path d="M582,440 C590,454 592,466 588,474" fill="none" stroke="#7A8FA6" stroke-width="1.1" stroke-dasharray="3,2" opacity="0.70"/>'
            '<path d="M530,442 C544,452 552,464 554,474" fill="none" stroke="#7A8FA6" stroke-width="1.1" stroke-dasharray="3,2" opacity="0.68"/>'
            # Vintage round canvas ankle patch
            '<circle cx="574" cy="454" r="8.5" fill="#E3D8C2" stroke="#1C232E" stroke-width="1.3" opacity="0.9"/>'
            '<circle cx="574" cy="454" r="3.6" fill="#2A3B52" opacity="0.82"/>'
            # Cream vulcanized rubber toe cap (brightly kissed by golden under-door light!)
            f'<path d="M492,464 C494,450 514,446 528,452 C538,458 538,472 526,478 L494,476 Z" '
            f'fill="url(#{p}_rubber_toe)" stroke="{INK_WARM}" stroke-width="1.9"/>'
            # Toe cap bright golden specular highlight + tiny bumper ridges
            '<path d="M498,458 C508,452 520,452 526,457" fill="none" stroke="#FFFBEB" stroke-width="1.8" opacity="0.88"/>'
            '<path d="M496,468 L496,474 M501,469 L501,475 M506,470 L506,476" fill="none" stroke="#9B8D75" stroke-width="1.0" opacity="0.65"/>'
            # Thick cream vulcanized rubber sole + dark foxing stripe + worn scuffs
            f'<path d="M492,470 C524,479 580,479 616,468 L616,484 C580,495 522,495 492,484 Z" '
            f'fill="url(#{p}_rubber)" stroke="{INK_WARM}" stroke-width="2.1"/>'
            '<path d="M494,476 C524,485 580,485 614,474" fill="none" stroke="#1E2126" stroke-width="1.8" opacity="0.88"/>'
            # Subtle dirt wear & sole tread edge notches
            '<path d="M544,484 L564,482 M510,481 L524,483 M586,480 L600,478" fill="none" stroke="#7D6E57" stroke-width="1.5" opacity="0.62"/>'
            # Metal lace eyelets
            '<circle cx="528" cy="451" r="2.0" fill="#C4CED9"/><circle cx="535" cy="445" r="2.0" fill="#C4CED9"/>'
            '<circle cx="543" cy="439" r="2.0" fill="#C4CED9"/><circle cx="551" cy="434" r="2.0" fill="#C4CED9"/>'
            # Crisscrossed cream shoelaces + bow knot & dangling lace tips with aglets
            '<path d="M521,454 L537,448 M528,448 L544,442 M536,442 L552,436 M543,436 L558,431" '
            'fill="none" stroke="#F4ECDA" stroke-width="2.3" stroke-linecap="round"/>'
            '<path d="M542,436 C528,430 522,440 534,444 M542,436 C550,426 560,432 550,440" '
            'fill="none" stroke="#EFE5CE" stroke-width="1.9" stroke-linecap="round"/>'
            '<path d="M538,440 C526,450 520,460 522,470 M542,440 C536,454 540,464 544,472" '
            'fill="none" stroke="#E5D9C0" stroke-width="1.7" stroke-linecap="round"/>'
            '<line x1="522" y1="468" x2="522" y2="473" stroke="#363A42" stroke-width="2.0" stroke-linecap="round"/>'
            '<line x1="543" y1="470" x2="545" y2="475" stroke="#363A42" stroke-width="2.0" stroke-linecap="round"/>'
            # Strong golden under-door rim light hugging left contour of front sneaker
            '<path d="M494,462 C504,450 522,442 534,432" fill="none" stroke="#FFEAAB" stroke-width="2.0" opacity="0.86" stroke-linecap="round"/>'
            '</g>'
        )

        sahne.append("</g>")  # end sneakers-11yo
        sahne.append("</g>")
        parts.append("".join(sahne))

    # ── LAYER 4: plan (Floating Golden Dust Motes + Subtle Cyan Observation Micro-Marks) ──
    if _katman_aktif(katmanlar, "plan"):
        plan: list[str] = ['<g id="p04-plan">']

        # Floating golden dust motes drifting inside the volumetric light cone
        for _ in range(56):
            dy = rng.uniform(298, 526)
            # Spread widens linearly from door gap (360..600) down to bottom (185..775)
            frac = (dy - 296) / (540 - 296)
            x_min = 362 - frac * 175
            x_max = 598 + frac * 175
            dx = rng.uniform(x_min, x_max)
            r_dot = rng.uniform(0.9, 2.6)
            op = rng.uniform(0.28, 0.85)
            col = "#FFF8DD" if r_dot > 1.8 else "#F8CA72"
            plan.append(f'<circle cx="{dx:.1f}" cy="{dy:.1f}" r="{r_dot:.1f}" fill="{col}" opacity="{op:.2f}"/>')
            if r_dot > 2.0:
                plan.append(f'<circle cx="{dx:.1f}" cy="{dy:.1f}" r="{r_dot * 2.5:.1f}" fill="#F8CA72" opacity="0.16"/>')

        # Subtle #7FE6FF cyan observation micro-marks (11yo Michael studying the lock & door gap)
        plan.append(
            f'<g stroke="{PLAN}" fill="none" opacity="0.54">'
            # Fine callout bracket around the rusty iron bolt lock
            '<rect x="544" y="170" width="70" height="54" rx="2" stroke-width="1.0" stroke-dasharray="4,3"/>'
            '<path d="M614,186 L646,168 L724,168" stroke-width="0.9"/>'
            # Fine measurement tick on under-door light gap
            '<path d="M352,286 L342,286 L342,298 L352,298" stroke-width="1.0"/>'
            '<path d="M342,292 L292,292" stroke-width="0.9" stroke-dasharray="3,2"/>'
            '</g>'
            '<rect x="646" y="154" width="102" height="14" rx="2" fill="#071624" fill-opacity="0.78" stroke="#7FE6FF" stroke-width="0.8" opacity="0.75"/>'
            f'<text x="697" y="164" text-anchor="middle" font-family="DejaVu Sans Mono, Consolas, monospace" font-size="7.6" fill="{PLAN_CORE}" opacity="0.82">IRON BOLT · 14MM</text>'
            '<rect x="206" y="284" width="84" height="14" rx="2" fill="#071624" fill-opacity="0.78" stroke="#7FE6FF" stroke-width="0.8" opacity="0.75"/>'
            f'<text x="248" y="294" text-anchor="middle" font-family="DejaVu Sans Mono, Consolas, monospace" font-size="7.6" fill="{PLAN_CORE}" opacity="0.82">DOOR GAP · 18MM</text>'
        )

        plan.append("</g>")
        parts.append("".join(plan))

    # ── LAYER 5: onplan (Foreground Dark Crate Silhouette Framing + Vignette) ──
    if _katman_aktif(katmanlar, "onplan"):
        onplan: list[str] = ['<g id="p04-onplan">']

        # Close-up dark foreground storage crates framing bottom-left & bottom-right corners
        onplan.append(
            f'<polygon points="-10,550 -10,364 114,418 148,550" fill="#080A0E" stroke="#181C22" stroke-width="1.6"/>'
            '<line x1="114" y1="418" x2="148" y2="550" stroke="#C89342" stroke-width="1.4" opacity="0.28"/>'
            f'<polygon points="970,550 970,356 844,412 814,550" fill="#080A0E" stroke="#181C22" stroke-width="1.6"/>'
            '<line x1="844" y1="412" x2="814" y2="550" stroke="#C89342" stroke-width="1.4" opacity="0.26"/>'
        )
        # Cinematic vignette
        onplan.append(f'<rect x="0" y="0" width="960" height="540" fill="url(#{p}_vig)"/>')

        # Subtle top-left chapter stamp
        onplan.append(
            f'<g stroke="{PLAN}" fill="none" stroke-width="1.3" opacity="0.52">'
            '<path d="M18,38 L18,18 L38,18"/>'
            '<path d="M922,522 L942,522 L942,502"/>'
            '</g>'
            '<text x="28" y="34" font-family="DejaVu Sans Mono, Consolas, monospace" font-weight="bold" '
            'font-size="8.6" letter-spacing="1.4" fill="#F4C770" opacity="0.72">PROLOGUE · AGE 11 · CLOSET FLOOR</text>'
        )

        onplan.append("</g>")
        parts.append("".join(onplan))

    return defs, "".join(parts)


# =============================================================================
# SVG VALIDATION & RENDERING HELPERS
# =============================================================================
def _check_paths_fill_none(svg_text: str) -> list[str]:
    """Verify every stroked <path> explicitly specifies fill=... (none or color)."""
    bad = []
    for m in re.finditer(r"<path\b[^>]*>", svg_text):
        tag = m.group(0)
        if "stroke=" in tag and "fill=" not in tag:
            bad.append(tag[:110])
    return bad


def render_scene_png(scene_fn, width: int = 1920, height: int = 1080) -> Image.Image:
    defs, body = scene_fn()
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {W_SCENE} {H_SCENE}">'
        f"<defs>{defs}</defs>{body}</svg>"
    )
    bad = _check_paths_fill_none(svg)
    if bad:
        raise ValueError(f"Stroked <path> without fill attribute detected: {bad[0]}")
    png_bytes = resvg_py.svg_to_bytes(svg_string=svg)
    return Image.open(io.BytesIO(png_bytes)).convert("RGBA")


def _load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = (
        [
            "C:/Windows/Fonts/segoeuib.ttf",
            "C:/Windows/Fonts/arialbd.ttf",
            "C:/Windows/Fonts/calibrib.ttf",
        ]
        if bold
        else [
            "C:/Windows/Fonts/segoeui.ttf",
            "C:/Windows/Fonts/arial.ttf",
            "C:/Windows/Fonts/calibri.ttf",
        ]
    )
    for fp in candidates:
        if Path(fp).exists():
            return ImageFont.truetype(fp, size=size)
    return ImageFont.load_default()


def _draw_card_bg(w: int, h: int) -> Image.Image:
    img = Image.new("RGBA", (w, h), "#080F19")
    draw = ImageDraw.Draw(img)
    for y in range(0, h, 32):
        draw.line((0, y, w, y), fill="#0D1826", width=1)
    for x in range(0, w, 32):
        draw.line((x, 0, x, h), fill="#0D1826", width=1)
    return img


def _draw_panel_box(draw: ImageDraw.ImageDraw, xy: tuple[int, int, int, int]) -> None:
    draw.rounded_rectangle(xy, radius=8, fill="#0D1724", outline="#24384E", width=1)


def _draw_swatches(draw: ImageDraw.ImageDraw, x: int, y: int, colors: list[str], size: int = 20, gap: int = 6) -> None:
    cx = x
    for c in colors:
        draw.rounded_rectangle((cx, y, cx + size, y + size), radius=3, fill=c, outline="#3B536D", width=1)
        cx += size + gap


# =============================================================================
# CARD GENERATOR (1280x720 MAIN SET CARD + 1280x720 R13 200% ZOOM QC CARD)
# =============================================================================
def uret_kartlar(versiyon: str = "v1") -> tuple[Path, Path]:
    img_p01 = render_scene_png(set_p01_fox_river_gece, 1920, 1080)
    img_p04 = render_scene_png(set_p04_depo_zemin, 1920, 1080)

    f_title = _load_font(20, bold=True)
    f_sub = _load_font(11, bold=False)
    f_card_t = _load_font(14, bold=True)
    f_card_s = _load_font(11, bold=False)
    f_small = _load_font(10, bold=True)

    # =========================================================================
    # OUTPUT 1: MAIN PROLOGUE SET SHEET (1280 x 720, 100% ENGLISH)
    # =========================================================================
    canvas = _draw_card_bg(1280, 720)
    draw = ImageDraw.Draw(canvas)

    draw.text((24, 12), "MICHAEL SCOFIELD · PROLOGUE HIGH-DETAIL OPENING & CLOSET SETS", fill="#EBF4FC", font=f_title)
    draw.text(
        (24, 38),
        "STYLE B+A HYBRID (CINEMATIC 2D + CYAN BLUEPRINT VISION)  ·  SCENES P01 & P04  ·  5-LAYER PARALLAX",
        fill="#7E97B0",
        font=f_sub,
    )
    top_swatches = [
        ("#142740", "STORM"),
        ("#F8C86E", "AMBER"),
        ("#7FE6FF", "CAD PLAN"),
        ("#263854", "DENIM"),
        ("#DDD1B8", "RUBBER"),
    ]
    sx_top = 816
    for col, lbl in top_swatches:
        draw.rounded_rectangle((sx_top, 18, sx_top + 14, 32), radius=3, fill=col, outline="#3B536D", width=1)
        draw.text((sx_top + 19, 19), lbl, fill="#9BB2C8", font=f_small)
        sx_top += 88
    draw.line((24, 58, 1256, 58), fill="#213247", width=1)

    # --- TOP WIDE PANEL: P01 EPIC FOX RIVER NIGHT OPENING HOOK ---
    _draw_panel_box(draw, (22, 68, 1256, 384))
    t_p01 = img_p01.resize((528, 297), Image.Resampling.LANCZOS)
    canvas.paste(t_p01, (34, 78), t_p01)
    draw.rectangle((34, 78, 34 + 528, 78 + 297), outline="#33506E", width=1)

    rx = 582
    draw.text((rx, 78), "01 · P01 FOX RIVER NIGHT OPENING HOOK", fill="#7FE6FF", font=f_card_t)
    draw.text((rx, 98), "Hero Hook: \"FOX RIVER\" / \"BY HEART\" · High Visual Activity", fill="#9CB6CE", font=f_card_s)
    draw.text((rx, 122), "PALETTE (STORM STEEL, DUAL SEARCHLIGHTS & CYAN X-RAY)", fill="#7FE6FF", font=f_small)
    _draw_swatches(draw, rx, 138, ["#091527", "#283444", "#F8C86E", "#FF3B4E", "#7FE6FF", "#E2FCFF"], size=20, gap=6)

    draw.text((rx, 172), "KEY ELEMENTS", fill="#9BB2C8", font=f_small)
    p01_items = [
        "• Towering Gothic Fox River fortress, twin watchtowers & guard silhouettes",
        "• Multi-story lit cellblocks, concertina razor wire & wet yard reflections",
        "• Sweeping dual-tone volumetric searchlights (icy white + warm amber)",
        "• Layered diagonal rain, distant lightning & Chicago horizon glow",
        "• #7FE6FF X-Ray CAD overlay: 01 CELL -> 02 PIPE -> 03 TUNNEL -> 04 WALL",
    ]
    for idx, line in enumerate(p01_items):
        draw.text((rx, 190 + idx * 20), line, fill="#DCE7F2", font=f_card_s)

    draw.text((rx, 300), "KEY LIGHTING", fill="#9BB2C8", font=f_small)
    draw.text((rx, 316), "Moonlit storm + cross-sweeping amber/icy searchlights", fill="#F6C367", font=f_card_s)
    draw.text((rx, 342), "PARALLAX LAYERS (5)", fill="#9BB2C8", font=f_small)
    draw.text((rx, 358), "p01-uzak · p01-orta · p01-sahne · p01-plan · p01-onplan", fill="#8AA3BC", font=f_small)

    # --- BOTTOM WIDE PANEL: P04 DARK CLOSET FLOOR & 11YO SNEAKERS ---
    _draw_panel_box(draw, (22, 396, 1256, 706))
    t_p04 = img_p04.resize((528, 297), Image.Resampling.LANCZOS)
    canvas.paste(t_p04, (34, 403), t_p04)
    draw.rectangle((34, 403, 34 + 528, 403 + 297), outline="#4C4133", width=1)

    draw.text((rx, 406), "02 · P04 DARK CLOSET FLOOR & 11YO SNEAKERS", fill="#F6C86E", font=f_card_t)
    draw.text((rx, 426), "Childhood Origin: \"AGE 11\" · Golden Under-Door Light Spill", fill="#B5A184", font=f_card_s)
    draw.text((rx, 450), "PALETTE (DARK TIMBER, GOLDEN SPILL, INDIGO DENIM & RUBBER)", fill="#7FE6FF", font=f_small)
    _draw_swatches(draw, rx, 466, ["#0E151E", "#28211E", "#F8C86E", "#263854", "#DDD1B8", "#7FE6FF"], size=20, gap=6)

    draw.text((rx, 500), "KEY ELEMENTS", fill="#9BB2C8", font=f_small)
    p04_items = [
        "• Splintered dark timber closet walls, dusty crates & rusty iron bolt lock",
        "• Blazing golden light beam spilling onto perspective wooden floorboards",
        "• High-detail worn 11yo canvas sneakers (cream rubber soles, eyelets, laces)",
        "• Indigo denim cuffs + realistic double-layer contact & cast shadows",
        "• Floating golden dust motes + subtle cyan observation micro-marks",
    ]
    for idx, line in enumerate(p04_items):
        draw.text((rx, 518 + idx * 20), line, fill="#DCE7F2", font=f_card_s)

    draw.text((rx, 626), "R4-PARALLAX & ENGINE COMPLIANCE", fill="#9BB2C8", font=f_small)
    draw.text((rx, 642), "Unified p04-sahne footwear/denim/shadows · 100% fill='none' stroked paths", fill="#9EC5DE", font=f_card_s)
    draw.text((rx, 668), "PARALLAX LAYERS (5)", fill="#9BB2C8", font=f_small)
    draw.text((rx, 684), "p04-uzak · p04-orta · p04-sahne · p04-plan · p04-onplan", fill="#8AA3BC", font=f_small)

    out_main = OUT_DIR / f"p_set_prolog_{versiyon}.png"
    canvas.convert("RGB").save(out_main, quality=95)

    # =========================================================================
    # OUTPUT 2: R13 200% ZOOM QUALITY CONTROL CARD (1280 x 720 — 4 PANELS)
    # =========================================================================
    r13 = _draw_card_bg(1280, 720)
    d13 = ImageDraw.Draw(r13)
    d13.text((24, 13), "R13 · 200% ZOOM QUALITY CONTROL (PROLOGUE OPENING & CLOSET)", fill="#EBF4FC", font=f_title)
    d13.text(
        (24, 37),
        "1:1 PIXEL CROPS FROM 1920×1080 SOURCE  ·  TOWERS, X-RAY CAD BLUEPRINT, RUSTY BOLT & 11YO SNEAKERS",
        fill="#7E97B0",
        font=f_sub,
    )
    d13.line((24, 55, 1256, 55), fill="#213247", width=1)

    cw, ch = 600, 264
    crops = [
        (
            img_p01,
            (320, 320),
            "1 · P01 LEFT WATCHTOWER, GUARD & SEARCHLIGHT (200%)",
            "Stone masonry, guard silhouette, swivel spotlight, razor wire & icy beam",
            (22, 66),
        ),
        (
            img_p01,
            (920, 565),
            "2 · P01 FOX RIVER GATE & CYAN CAD X-RAY ROUTE (200%)",
            "Lit stone plaque, iron gate, 01 CELL -> 02 PIPE -> 03 TUNNEL -> 04 WALL",
            (652, 66),
        ),
        (
            img_p04,
            (1220, 420),
            "3 · P04 CLOSET DOOR, RUSTY IRON BOLT & LIGHT SLIT (200%)",
            "Heavy timber door, rusty padlock bolt, IRON BOLT 14MM mark & golden bloom",
            (22, 392),
        ),
        (
            img_p04,
            (1210, 860),
            "4 · P04 11YO WORN SNEAKERS, DENIM LEGS & SHADOWS (200%)",
            "Cream vulcanized soles, laced canvas, bent denim knees, golden rim & dust",
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

    out_r13 = OUT_DIR / "p_set_prolog_r13.png"
    r13.convert("RGB").save(out_r13, quality=95)
    print(f"Saved:\n  - {out_main}\n  - {out_r13}")
    return out_main, out_r13


if __name__ == "__main__":
    uret_kartlar("v1")
