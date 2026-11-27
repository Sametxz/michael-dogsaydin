"""V5 (Act II: Conspiracy Planning Wall & Tattoo Parlor Set).

Style B+A Hybrid (Cinematic 2D + Cyan Blueprint Vision) — 5-layer parallax-ready scenes (960x540):
  - set_203_plan_duvari(katmanlar=None)     -> (defs_str, body_str)
  - set_204_dovme_studyosu(katmanlar=None)  -> (defs_str, body_str)

All on-screen text is 100% ENGLISH. All stroked <path> elements explicitly set fill="none".
Uses locked assets K.michael_sirt_dovme, K.lincoln_kafa, K.sara_kafa, K.turna from karakter.py
without modifying karakter.py.
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

INK = "#141110"
INK_WARM = "#211611"
PLAN = "#7FE6FF"
PLAN_CORE = "#E6FDFF"
PLAN_DIM = "#38A4C7"
RED_STRING = "#D92A38"
RED_BRIGHT = "#FF4D5A"
AMBER_LIGHT = "#FFD180"
AMBER_WARM = "#E59842"

_UID = 0


def _uid(prefix: str = "b2") -> str:
    global _UID
    _UID += 1
    return f"{prefix}_{_UID}"


def _katman_aktif(katmanlar: set[str] | list[str] | None, ad: str) -> bool:
    return katmanlar is None or ad in katmanlar


def _pushpin(x: float, y: float, color: str = "#D92A38") -> str:
    """Realistic angled pushpin with subtle cast shadow and specular dot."""
    return (
        f'<ellipse cx="{x+2.2:.1f}" cy="{y+3.2:.1f}" rx="4.2" ry="2.6" fill="#000000" opacity="0.45"/>'
        f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4.4" fill="{color}" stroke="#1A1210" stroke-width="1.1"/>'
        f'<circle cx="{x-1.2:.1f}" cy="{y-1.3:.1f}" r="1.4" fill="#FFFFFF" opacity="0.55"/>'
    )


def _red_string(x1: float, y1: float, x2: float, y2: float, sag: float = 14.0) -> str:
    """Gravity-sagged red investigation string with soft wall shadow."""
    mx = (x1 + x2) * 0.5
    my = (y1 + y2) * 0.5 + sag
    return (
        f'<path d="M{x1:.1f},{y1+2.5:.1f} Q{mx:.1f},{my+4.5:.1f} {x2:.1f},{y2+2.5:.1f}" '
        f'fill="none" stroke="#080404" stroke-width="2.2" opacity="0.40" stroke-linecap="round"/>'
        f'<path d="M{x1:.1f},{y1:.1f} Q{mx:.1f},{my:.1f} {x2:.1f},{y2:.1f}" '
        f'fill="none" stroke="{RED_STRING}" stroke-width="1.7" opacity="0.92" stroke-linecap="round"/>'
        f'<path d="M{x1:.1f},{y1-0.4:.1f} Q{mx:.1f},{my-0.5:.1f} {x2:.1f},{y2-0.4:.1f}" '
        f'fill="none" stroke="{RED_BRIGHT}" stroke-width="0.6" opacity="0.55" stroke-linecap="round"/>'
    )


def _postit(
    x: float,
    y: float,
    w: float,
    h: float,
    rot: float,
    title: str,
    lines: list[str],
    fill: str = "#F3DC78",
    pin_col: str = "#D92A38",
    extra_svg: str = "",
) -> str:
    """Slightly curled sticky note with cast shadow, pin, and crisp English text."""
    out = [f'<g transform="translate({x:.1f},{y:.1f}) rotate({rot:.1f})">']
    # Drop shadow
    out.append(
        f'<path d="M3,5 L{w+4:.1f},4 L{w+5:.1f},{h+5:.1f} Q{w*0.5:.1f},{h+7:.1f} 2,{h+4:.1f} Z" '
        f'fill="#060404" opacity="0.45"/>'
    )
    # Curled sticky paper
    out.append(
        f'<path d="M0,0 L{w:.1f},0 L{w+1:.1f},{h-2:.1f} Q{w*0.55:.1f},{h+2:.1f} -1,{h-1:.1f} Z" '
        f'fill="{fill}" stroke="#6B5A24" stroke-width="0.9"/>'
    )
    # Top adhesive darker strip
    out.append(f'<rect x="0.5" y="0.5" width="{w-1:.1f}" height="11" fill="#D9BC52" opacity="0.45"/>')
    # Title & lines
    out.append(
        f'<text x="{w*0.5:.1f}" y="21" text-anchor="middle" font-family="Arial,sans-serif" '
        f'font-size="9.2" font-weight="bold" fill="#231910" letter-spacing="0.4">{title}</text>'
    )
    out.append(
        f'<path d="M8,24.5 L{w-8:.1f},24.5" fill="none" stroke="#8C2A2A" stroke-width="0.9" opacity="0.7"/>'
    )
    for idx, ln in enumerate(lines):
        out.append(
            f'<text x="8" y="{36 + idx * 11.5:.1f}" font-family="Consolas,monospace" '
            f'font-size="7.4" font-weight="bold" fill="#2D2418">{ln}</text>'
        )
    if extra_svg:
        out.append(extra_svg)
    out.append(_pushpin(w * 0.5, 4.5, pin_col))
    out.append("</g>")
    return "".join(out)


# =============================================================================
# SCENE 2.03: CONSPIRACY PLANNING WALL ("1 YEAR" / "PRISON BREAK")
# =============================================================================
def set_203_plan_duvari(
    katmanlar: set[str] | list[str] | None = None,
) -> tuple[str, str]:
    """Dim brick apartment wall covered in Michael's 1-year Fox River escape conspiracy board:
    pinned blueprints, guard shift schedule, Lincoln & Sara & Fox River photos, red strings,
    yellow post-its (ALLEN BOLT, INFIRMARY, PIPES), cluttered foreground desk with sketches &
    steaming coffee mug, and a live glowing #7FE6FF escape route (01->02->03->04 · 1 YEAR).
    """
    rng = random.Random(203)
    p = _uid("s203")

    defs = f"""
    <linearGradient id="{p}_wall_grad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#19110E"/>
      <stop offset="45%" stop-color="#271A15"/>
      <stop offset="100%" stop-color="#120C0A"/>
    </linearGradient>
    <radialGradient id="{p}_lamp_warm" cx="0.49" cy="0.22" r="0.62">
      <stop offset="0%" stop-color="#FFD994" stop-opacity="0.34"/>
      <stop offset="42%" stop-color="#D6863A" stop-opacity="0.14"/>
      <stop offset="100%" stop-color="#090D16" stop-opacity="0.0"/>
    </radialGradient>
    <linearGradient id="{p}_cork" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#533824"/>
      <stop offset="50%" stop-color="#442D1C"/>
      <stop offset="100%" stop-color="#2E1E13"/>
    </linearGradient>
    <linearGradient id="{p}_bp_paper" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#12416C"/>
      <stop offset="55%" stop-color="#0C2F51"/>
      <stop offset="100%" stop-color="#082039"/>
    </linearGradient>
    <linearGradient id="{p}_paper_warm" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#EFE7D2"/>
      <stop offset="100%" stop-color="#D7CAAF"/>
    </linearGradient>
    <linearGradient id="{p}_desk_top" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#3A261A"/>
      <stop offset="45%" stop-color="#271911"/>
      <stop offset="100%" stop-color="#160F0B"/>
    </linearGradient>
    <linearGradient id="{p}_moon_edge" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#4F8AB8" stop-opacity="0.28"/>
      <stop offset="100%" stop-color="#4F8AB8" stop-opacity="0.0"/>
    </linearGradient>
    <linearGradient id="{p}_cone" x1="0.5" y1="0" x2="0.5" y2="1">
      <stop offset="0%" stop-color="#FFE4A8" stop-opacity="0.24"/>
      <stop offset="50%" stop-color="#E59B48" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="#E59B48" stop-opacity="0.0"/>
    </linearGradient>
    <radialGradient id="{p}_vignette" cx="0.50" cy="0.46" r="0.65">
      <stop offset="52%" stop-color="#000000" stop-opacity="0.0"/>
      <stop offset="100%" stop-color="#04070D" stop-opacity="0.72"/>
    </radialGradient>
    <filter id="{p}_glow_cyan" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="3.0" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="{p}_glow_soft" x="-25%" y="-25%" width="150%" height="150%">
      <feGaussianBlur stdDeviation="1.6" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <clipPath id="{p}_clip_lincoln"><rect x="0" y="0" width="84" height="94"/></clipPath>
    <clipPath id="{p}_clip_sara"><rect x="0" y="0" width="84" height="94"/></clipPath>
    <clipPath id="{p}_clip_prison"><rect x="0" y="0" width="114" height="76"/></clipPath>
    """

    parts: list[str] = []

    # -------------------------------------------------------------------------
    # LAYER 1: UZAK — Dim Chicago Brick Apartment Wall & Night Window Rim
    # -------------------------------------------------------------------------
    if _katman_aktif(katmanlar, "uzak"):
        u: list[str] = ['<g id="s203-uzak">']
        u.append(f'<rect x="0" y="0" width="960" height="540" fill="url(#{p}_wall_grad)"/>')
        # Brick masonry grid across entire apartment wall
        brick_w, brick_h = 46, 20
        brick_cols = ["#2C1B15", "#35211A", "#241612", "#3B251D", "#291914", "#1F130F"]
        for row in range(0, 24):
            by = row * brick_h
            offset = (brick_w // 2) if (row % 2 == 1) else 0
            for col in range(-1, 23):
                bx = col * brick_w + offset
                bc = rng.choice(brick_cols)
                u.append(
                    f'<rect x="{bx+1}" y="{by+1}" width="{brick_w-2}" height="{brick_h-2}" '
                    f'rx="1.2" fill="{bc}" opacity="{rng.uniform(0.68, 0.94):.2f}"/>'
                )
                # Occasional worn highlight on top brick edge
                if rng.random() < 0.28:
                    u.append(
                        f'<path d="M{bx+3},{by+2.5} L{bx+brick_w-5},{by+2.5}" '
                        f'fill="none" stroke="#5A392C" stroke-width="0.9" opacity="0.35"/>'
                    )
        # Mortar horizontal shadow grooves
        for row in range(0, 24):
            u.append(
                f'<path d="M0,{row*brick_h} L960,{row*brick_h}" fill="none" stroke="#0C0807" stroke-width="1.4" opacity="0.65"/>'
            )
        # Left cold moonlight spill from apartment window off-frame
        u.append(f'<rect x="0" y="0" width="170" height="440" fill="url(#{p}_moon_edge)"/>')
        # Exposed industrial conduit pipe on far left wall
        u.append('<rect x="14" y="0" width="8" height="440" fill="#1A2028" stroke="#0A0D12" stroke-width="1.2"/>')
        u.append('<path d="M16.5,0 L16.5,440" fill="none" stroke="#4D657A" stroke-width="1.1" opacity="0.45"/>')
        for cy in (75, 195, 315):
            u.append(f'<rect x="10" y="{cy}" width="16" height="6" rx="1.5" fill="#2A323C" stroke="#0A0D12" stroke-width="1"/>')
        # Warm overhead lamp wash on brick wall
        u.append(f'<rect x="0" y="0" width="960" height="450" fill="url(#{p}_lamp_warm)"/>')
        u.append("</g>")
        parts.append("".join(u))

    # -------------------------------------------------------------------------
    # LAYER 2: ORTA — Massive Conspiracy Board, Blueprints, Photos, Post-its & Red Strings
    # -------------------------------------------------------------------------
    if _katman_aktif(katmanlar, "orta"):
        m: list[str] = ['<g id="s203-orta">']

        # Large wooden-framed cork planning board spanning the brick wall
        m.append('<rect x="46" y="34" width="868" height="398" rx="4" fill="#070505" opacity="0.58"/>')
        m.append(f'<rect x="40" y="28" width="868" height="398" rx="3" fill="url(#{p}_cork)" stroke="#1C120B" stroke-width="6"/>')
        # Wooden outer frame bevel highlight
        m.append('<rect x="40" y="28" width="868" height="398" rx="3" fill="none" stroke="#6E4B30" stroke-width="1.6" opacity="0.65"/>')
        # Subtle cork texture speckles
        for _ in range(180):
            cx = rng.uniform(48, 900)
            cy = rng.uniform(36, 418)
            m.append(
                f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{rng.uniform(0.6,1.5):.1f}" '
                f'fill="{rng.choice(["#2A1B10","#6B492F","#1F130B"])}" opacity="0.32"/>'
            )

        # --- 1. TOP-LEFT: GUARD SHIFT SCHEDULE (CREAM PAPER) ---
        m.append('<g transform="translate(62,48) rotate(-2.2)">')
        m.append('<rect x="3" y="4" width="164" height="148" fill="#060404" opacity="0.45"/>')
        m.append(f'<rect x="0" y="0" width="164" height="148" fill="url(#{p}_paper_warm)" stroke="#4C4233" stroke-width="1.0"/>')
        m.append('<rect x="0" y="0" width="164" height="22" fill="#232B35"/>')
        m.append('<text x="82" y="14.5" text-anchor="middle" font-family="Arial,sans-serif" font-size="8.6" font-weight="bold" fill="#EFE7D2" letter-spacing="0.8">GUARD SHIFT SCHEDULE</text>')
        m.append('<text x="8" y="33" font-family="Consolas,monospace" font-size="7.0" font-weight="bold" fill="#3B3126">FOX RIVER · CELL BLOCK A</text>')
        m.append('<path d="M8,37 L156,37" fill="none" stroke="#6D6150" stroke-width="0.9"/>')
        shifts = [
            ("00:00", "TOWER 01", "BELLICK", False),
            ("01:30", "YARD PATROL", "GEARY", False),
            ("02:15", "INFIRMARY", "14 MIN GAP", True),
            ("02:30", "WING A COUNT", "STOLTE", False),
            ("03:00", "PIPE CHECK", "NONE", True),
            ("04:00", "WALL SWEEP", "ROTO-B", False),
        ]
        for idx, (tm, loc, note, alert) in enumerate(shifts):
            sy = 50 + idx * 15.5
            if alert:
                m.append(f'<rect x="6" y="{sy-9:.1f}" width="152" height="13" fill="#D92A38" opacity="0.16"/>')
            m.append(f'<text x="8" y="{sy:.1f}" font-family="Consolas,monospace" font-size="7.2" fill="#282018">{tm}</text>')
            m.append(f'<text x="42" y="{sy:.1f}" font-family="Consolas,monospace" font-size="7.2" fill="#282018">{loc}</text>')
            col_n = "#A61C26" if alert else "#4A4035"
            m.append(f'<text x="156" y="{sy:.1f}" text-anchor="end" font-family="Consolas,monospace" font-size="7.2" font-weight="bold" fill="{col_n}">{note}</text>')
            m.append(f'<path d="M8,{sy+3.5:.1f} L156,{sy+3.5:.1f}" fill="none" stroke="#BEB19B" stroke-width="0.6"/>')
        # Hand-drawn red oval around 02:15 14 MIN GAP
        m.append('<ellipse cx="82" cy="77" rx="74" ry="11" fill="none" stroke="#C8222E" stroke-width="1.6" opacity="0.88"/>')
        m.append(_pushpin(82, 5, "#D92A38"))
        m.append("</g>")

        # --- 2. CENTER: MASSIVE PINNED FOX RIVER ARCHITECTURAL BLUEPRINT ---
        m.append('<g transform="translate(246,56) rotate(0.7)">')
        m.append('<rect x="5" y="6" width="388" height="266" fill="#050404" opacity="0.52"/>')
        m.append(f'<rect x="0" y="0" width="388" height="266" fill="url(#{p}_bp_paper)" stroke="#92CBE8" stroke-width="1.2"/>')
        # Blueprint inner double border & grid
        m.append('<rect x="9" y="9" width="370" height="248" fill="none" stroke="#5CA8D1" stroke-width="1.0" opacity="0.85"/>')
        for gx in range(24, 376, 22):
            m.append(f'<path d="M{gx},10 L{gx},256" fill="none" stroke="#4D96BF" stroke-width="0.45" opacity="0.32"/>')
        for gy in range(24, 254, 22):
            m.append(f'<path d="M10,{gy} L378,{gy}" fill="none" stroke="#4D96BF" stroke-width="0.45" opacity="0.32"/>')

        # Blueprint title block (bottom)
        m.append('<rect x="14" y="220" width="360" height="32" fill="#07223B" stroke="#64B2DB" stroke-width="0.9"/>')
        m.append('<text x="22" y="234" font-family="Arial,sans-serif" font-size="10.2" font-weight="bold" fill="#DCF2FF" letter-spacing="1.0">FOX RIVER STATE PENITENTIARY</text>')
        m.append('<text x="22" y="246" font-family="Consolas,monospace" font-size="6.8" fill="#8BC4E0">ARCHITECTURAL &amp; UTILITY SUB-LEVEL PLAN · REV 4B · SCALE 1:250</text>')
        m.append('<text x="366" y="236" text-anchor="end" font-family="Consolas,monospace" font-size="7.4" font-weight="bold" fill="#7FE6FF">ENG: M. SCOFIELD</text>')
        m.append('<text x="366" y="246" text-anchor="end" font-family="Consolas,monospace" font-size="6.6" fill="#8BC4E0">JOLIET, ILLINOIS</text>')

        # Wing A Cell Block (left section of blueprint)
        m.append('<rect x="24" y="28" width="94" height="174" fill="#0A2B4A" stroke="#A6DCF7" stroke-width="1.3"/>')
        m.append('<text x="71" y="22" text-anchor="middle" font-family="Consolas,monospace" font-size="8.0" font-weight="bold" fill="#BCE8FF">CELL BLOCK A</text>')
        for cy in range(36, 194, 16):
            m.append(f'<rect x="30" y="{cy}" width="26" height="12" fill="none" stroke="#7CC0E3" stroke-width="0.8"/>')
            m.append(f'<rect x="86" y="{cy}" width="26" height="12" fill="none" stroke="#7CC0E3" stroke-width="0.8"/>')
        m.append('<rect x="30" y="100" width="26" height="12" fill="#7FE6FF" opacity="0.28" stroke="#7FE6FF" stroke-width="1.0"/>')
        m.append('<text x="71" y="109" text-anchor="middle" font-family="Consolas,monospace" font-size="6.2" fill="#7FE6FF">CELL 40</text>')

        # Central Yard & Pipe Sub-Level (middle section)
        m.append('<rect x="132" y="34" width="122" height="148" fill="#092744" stroke="#8CCAE8" stroke-width="1.1" stroke-dasharray="4,2"/>')
        m.append('<text x="193" y="27" text-anchor="middle" font-family="Consolas,monospace" font-size="8.0" font-weight="bold" fill="#BCE8FF">MAIN YARD / PIPES</text>')
        m.append('<circle cx="193" cy="108" r="34" fill="none" stroke="#78BCE0" stroke-width="0.9" stroke-dasharray="3,2"/>')
        m.append('<path d="M132,108 L254,108 M193,34 L193,182" fill="none" stroke="#5EA4CA" stroke-width="0.7" opacity="0.7"/>')
        # Sub-level cast iron pipe lines
        m.append('<path d="M56,106 L146,106 L146,158 L266,158 L266,86 L318,86" fill="none" stroke="#5AB0DB" stroke-width="2.2" opacity="0.7"/>')
        m.append('<text x="193" y="174" text-anchor="middle" font-family="Consolas,monospace" font-size="6.4" fill="#9ED7F2">SUB-LEVEL 18&quot; DRAIN</text>')

        # Infirmary & North Wall (right section)
        m.append('<rect x="268" y="28" width="96" height="124" fill="#0A2B4A" stroke="#A6DCF7" stroke-width="1.3"/>')
        m.append('<text x="316" y="22" text-anchor="middle" font-family="Consolas,monospace" font-size="8.0" font-weight="bold" fill="#BCE8FF">INFIRMARY</text>')
        # Medical cross & rooms
        m.append('<path d="M286,42 L286,54 M280,48 L292,48" fill="none" stroke="#7FE6FF" stroke-width="1.8"/>')
        m.append('<rect x="276" y="64" width="42" height="36" fill="none" stroke="#7CC0E3" stroke-width="0.8"/>')
        m.append('<rect x="322" y="64" width="34" height="78" fill="none" stroke="#7CC0E3" stroke-width="0.8"/>')
        m.append('<path d="M268,168 L372,168" fill="none" stroke="#FFB866" stroke-width="1.5" stroke-dasharray="5,3"/>')
        m.append('<text x="320" y="182" text-anchor="middle" font-family="Consolas,monospace" font-size="6.8" font-weight="bold" fill="#FFD180">NORTH WALL · 40FT</text>')

        # Masking tape corners + brass pushpins
        m.append('<polygon points="-6,12 18,-6 24,2 0,20" fill="#D8CCA8" opacity="0.78"/>')
        m.append('<polygon points="366,-6 394,14 388,22 360,2" fill="#D8CCA8" opacity="0.78"/>')
        m.append(_pushpin(18, 12, "#D92A38"))
        m.append(_pushpin(370, 12, "#D92A38"))
        m.append(_pushpin(18, 254, "#E5B44B"))
        m.append(_pushpin(370, 254, "#E5B44B"))
        m.append("</g>")

        # --- 3. SECONDARY STRUCTURAL DIAGRAM (BOTTOM-LEFT OF BOARD) ---
        m.append('<g transform="translate(68,218) rotate(1.8)">')
        m.append('<rect x="3" y="4" width="162" height="114" fill="#060404" opacity="0.45"/>')
        m.append(f'<rect x="0" y="0" width="162" height="114" fill="url(#{p}_paper_warm)" stroke="#4C4233" stroke-width="1.0"/>')
        m.append('<text x="8" y="14" font-family="Consolas,monospace" font-size="7.4" font-weight="bold" fill="#221C16">SINK BOLT · WALL STRESS</text>')
        m.append('<path d="M8,18 L154,18" fill="none" stroke="#5A4F42" stroke-width="0.8"/>')
        # Hooke's law / masonry load sketch
        m.append('<rect x="16" y="28" width="58" height="66" fill="none" stroke="#2D3B4A" stroke-width="1.1"/>')
        m.append('<path d="M16,44 L74,44 M16,60 L74,60 M16,76 L74,76 M36,28 L36,94 M54,28 L54,94" fill="none" stroke="#5E7387" stroke-width="0.7"/>')
        # Stress fracture red X
        m.append('<path d="M36,44 L54,76 M54,44 L36,76" fill="none" stroke="#C8222E" stroke-width="1.4"/>')
        m.append('<circle cx="45" cy="60" r="14" fill="none" stroke="#C8222E" stroke-width="1.1" stroke-dasharray="3,2"/>')
        # Hex bolt schematic on right
        pts_hex = " ".join(
            f"{118 + 18*math.cos(math.radians(60*i-30)):.1f},{58 + 18*math.sin(math.radians(60*i-30)):.1f}"
            for i in range(6)
        )
        m.append(f'<polygon points="{pts_hex}" fill="none" stroke="#1E2833" stroke-width="1.4"/>')
        m.append('<circle cx="118" cy="58" r="7.5" fill="none" stroke="#1E2833" stroke-width="1.1"/>')
        m.append('<text x="118" y="92" text-anchor="middle" font-family="Consolas,monospace" font-size="7.0" font-weight="bold" fill="#9E1D27">11121147</text>')
        m.append('<text x="118" y="103" text-anchor="middle" font-family="Consolas,monospace" font-size="6.2" fill="#3A3128">SCHWEITZER</text>')
        m.append(_pushpin(80, 5, "#E5B44B"))
        m.append("</g>")

        # --- 4. PINNED PHOTOS ON RIGHT SIDE (LINCOLN v1, SARA v2, FOX RIVER TOWER) ---
        # Photo A: Lincoln Burrows (top-right-inner)
        m.append('<g transform="translate(658,46) rotate(3.4)">')
        m.append('<rect x="4" y="5" width="96" height="122" fill="#050404" opacity="0.50"/>')
        m.append('<rect x="0" y="0" width="96" height="122" fill="#EFEBE0" stroke="#363029" stroke-width="1.0"/>')
        m.append(f'<g transform="translate(6,6)" clip-path="url(#{p}_clip_lincoln)">')
        m.append('<rect x="0" y="0" width="84" height="94" fill="#2C3846"/>')
        for hy in range(14, 92, 14):
            m.append(f'<path d="M0,{hy} L84,{hy}" fill="none" stroke="#5E7184" stroke-width="0.6" opacity="0.45"/>')
        # Blue prison shoulders
        m.append('<path d="M6,96 L20,74 L64,74 L78,96 Z" fill="#5A7A9A" stroke="#1A1513" stroke-width="1.2"/>')
        m.append('<path d="M32,74 L42,86 L52,74 Z" fill="#EAE6DC"/>')
        # LOCKED LINCOLN v1 HEAD
        m.append('<g transform="translate(42,46) scale(0.32)">')
        m.append(K.lincoln_kafa("front", "odak", boyun=True))
        m.append("</g>")
        m.append('<rect x="0" y="0" width="84" height="94" fill="#18222C" opacity="0.12"/>')
        m.append("</g>")
        m.append('<text x="48" y="110" text-anchor="middle" font-family="Arial,sans-serif" font-size="7.2" font-weight="bold" fill="#231D18">L. BURROWS · #79238</text>')
        m.append('<text x="48" y="118.5" text-anchor="middle" font-family="Consolas,monospace" font-size="6.0" font-weight="bold" fill="#A61C26">EXECUTION: MAY 11</text>')
        m.append(_pushpin(48, 4, "#D92A38"))
        m.append("</g>")

        # Photo B: Dr. Sara Tancredi (top-far-right)
        m.append('<g transform="translate(778,56) rotate(-3.2)">')
        m.append('<rect x="4" y="5" width="96" height="122" fill="#050404" opacity="0.50"/>')
        m.append('<rect x="0" y="0" width="96" height="122" fill="#EFEBE0" stroke="#363029" stroke-width="1.0"/>')
        m.append(f'<g transform="translate(6,6)" clip-path="url(#{p}_clip_sara)">')
        m.append('<rect x="0" y="0" width="84" height="94" fill="#32414D"/>')
        # Infirmary coat & scrub shoulders
        m.append('<path d="M8,96 L22,74 L62,74 L76,96 Z" fill="#EAE6DD" stroke="#1A1513" stroke-width="1.2"/>')
        m.append('<path d="M32,74 L42,90 L52,74 Z" fill="#4E6B7B"/>')
        # LOCKED SARA v2 HEAD
        m.append('<g transform="translate(40,46) scale(0.32)">')
        m.append(K.sara_kafa("3q", "odak", look=0.1, boyun=True))
        m.append("</g>")
        m.append('<rect x="0" y="0" width="84" height="94" fill="#1C262E" opacity="0.10"/>')
        m.append("</g>")
        m.append('<text x="48" y="110" text-anchor="middle" font-family="Arial,sans-serif" font-size="7.2" font-weight="bold" fill="#231D18">DR. S. TANCREDI</text>')
        m.append('<text x="48" y="118.5" text-anchor="middle" font-family="Consolas,monospace" font-size="6.0" fill="#2D4A5E">INFIRMARY KEY ACCESS</text>')
        m.append(_pushpin(48, 4, "#D92A38"))
        m.append("</g>")

        # Photo C: Fox River North Wall & Watchtower Surveillance Photo (mid-right)
        m.append('<g transform="translate(744,198) rotate(2.4)">')
        m.append('<rect x="4" y="5" width="126" height="104" fill="#050404" opacity="0.50"/>')
        m.append('<rect x="0" y="0" width="126" height="104" fill="#EAE5D8" stroke="#363029" stroke-width="1.0"/>')
        m.append(f'<g transform="translate(6,6)" clip-path="url(#{p}_clip_prison)">')
        m.append('<rect x="0" y="0" width="114" height="76" fill="#0F1B2B"/>')
        # Searchlight beam
        m.append('<polygon points="84,20 12,76 58,76" fill="#D5F1FF" opacity="0.22"/>')
        # Prison masonry wall
        m.append('<rect x="0" y="42" width="114" height="34" fill="#2C3540" stroke="#12171E" stroke-width="1.0"/>')
        # Watchtower
        m.append('<polygon points="74,42 78,16 96,16 100,42" fill="#1D2530" stroke="#0D1218" stroke-width="1.0"/>')
        m.append('<rect x="76" y="10" width="22" height="8" fill="#18202A" stroke="#0D1218" stroke-width="1.0"/>')
        m.append('<rect x="80" y="12" width="14" height="4" fill="#FFE6A3" opacity="0.85"/>')
        # Barbed wire top
        m.append('<path d="M0,40 Q12,35 24,40 T48,40 T72,40 T96,40 T114,40" fill="none" stroke="#899BAD" stroke-width="0.8"/>')
        m.append("</g>")
        m.append('<text x="63" y="92" text-anchor="middle" font-family="Arial,sans-serif" font-size="7.2" font-weight="bold" fill="#231D18">FOX RIVER · NORTH WALL</text>')
        m.append('<text x="63" y="100" text-anchor="middle" font-family="Consolas,monospace" font-size="5.8" fill="#8C2229">40FT DROP · SPOTLIGHT BLIND</text>')
        m.append(_pushpin(63, 4, "#D92A38"))
        m.append("</g>")

        # --- 5. YELLOW POST-IT NOTES (ALLEN BOLT, PIPES, INFIRMARY, 1 YEAR — CLEAN NON-OVERLAPPING) ---
        m.append(
            _postit(
                156, 334, 94, 76, -3.8,
                "ALLEN BOLT",
                ["SINK ANCHOR", "HEX 11121147", "FILE DOWN"],
                fill="#F5DF7B",
                pin_col="#D92A38",
            )
        )
        m.append(
            _postit(
                292, 336, 96, 74, 2.2,
                "PIPES",
                ["18\" CAST IRON", "CORRODED JOINT", "CHEM MIX"],
                fill="#F2D76D",
                pin_col="#E5B44B",
            )
        )
        m.append(
            _postit(
                434, 334, 96, 76, -2.6,
                "INFIRMARY",
                ["UNBARRED WIN", "02:15 SHIFT", "ROPE LINE"],
                fill="#F6E284",
                pin_col="#D92A38",
            )
        )
        m.append(
            _postit(
                560, 332, 82, 72, 3.2,
                "1 YEAR",
                ["EVERY LINE", "ON THE SKIN", "NO MISTAKES"],
                fill="#EFC86E",
                pin_col="#E5B44B",
            )
        )

        # --- 6. RED INVESTIGATION STRINGS CONNECTING PINS (CLEAR OF PORTRAIT FACES!) ---
        strings = [
            (144, 53, 264, 68, 11),    # Guard Shift -> Blueprint top-left
            (144, 53, 148, 223, 8),    # Guard Shift -> Sink Bolt Diagram
            (264, 68, 203, 338, 14),   # Blueprint top-left -> Allen Bolt Post-it
            (203, 338, 340, 340, 9),   # Allen Bolt -> Pipes Post-it
            (340, 340, 482, 338, 9),   # Pipes -> Infirmary Post-it
            (482, 338, 601, 336, 8),   # Infirmary -> 1 YEAR Post-it
            (616, 68, 706, 50, 8),     # Blueprint top-right -> Lincoln pin (top only)
            (706, 50, 826, 60, 10),    # Lincoln pin -> Sara pin (clear above faces)
            (826, 60, 886, 134, -8),   # Sara pin -> right border tack (clear of Sara's face)
            (886, 134, 807, 202, 10),  # Right border tack -> Fox River North Wall photo
            (616, 310, 807, 202, 14),  # Blueprint bottom-right -> North Wall photo
            (482, 338, 616, 310, 10),  # Infirmary Post-it -> Blueprint bottom-right
        ]
        for x1, y1, x2, y2, sag in strings:
            m.append(_red_string(x1, y1, x2, y2, sag))
        # Right border relay tack so string clears Sara's portrait completely
        m.append(_pushpin(886, 134, "#D92A38"))

        m.append("</g>")
        parts.append("".join(m))

    # -------------------------------------------------------------------------
    # LAYER 3: SAHNE — Cluttered Foreground Desk (Sketches, Mug, Origami Crane, Tools)
    # -------------------------------------------------------------------------
    if _katman_aktif(katmanlar, "sahne"):
        s: list[str] = ['<g id="s203-sahne">']

        # Foreground walnut desk surface
        s.append('<polygon points="0,428 960,428 960,540 0,540" fill="url(#%s_desk_top)"/>' % p)
        s.append('<path d="M0,428 L960,428" fill="none" stroke="#6B4730" stroke-width="2.2"/>')
        s.append('<path d="M0,430 L960,430" fill="none" stroke="#120B08" stroke-width="1.5"/>')
        # Subtle desk wood grain lines
        for gy in (448, 472, 498, 522):
            s.append(f'<path d="M0,{gy} Q480,{gy+4} 960,{gy-2}" fill="none" stroke="#1A100A" stroke-width="1.1" opacity="0.45"/>')

        # Left scattered architectural sketches on desk
        s.append('<g transform="translate(88,438) rotate(-4)">')
        s.append('<polygon points="10,4 226,0 248,76 0,82" fill="#060404" opacity="0.48"/>')
        s.append('<polygon points="6,0 222,-4 244,72 -4,78" fill="#E9E0C9" stroke="#5D5140" stroke-width="1.0"/>')
        # Tunnel cross-section sketch on paper
        s.append('<circle cx="72" cy="36" r="20" fill="none" stroke="#2B3D4E" stroke-width="1.2"/>')
        s.append('<path d="M44,36 L100,36 M72,12 L72,60" fill="none" stroke="#4D6880" stroke-width="0.7" stroke-dasharray="3,2"/>')
        s.append('<path d="M118,16 L210,16 M118,28 L198,28 M118,40 L206,40 M118,52 L176,52" fill="none" stroke="#3B352D" stroke-width="1.0" opacity="0.65"/>')
        s.append('<text x="118" y="12" font-family="Consolas,monospace" font-size="6.8" font-weight="bold" fill="#8C1E26">DRAINAGE TUNNEL SEC-B</text>')
        s.append("</g>")

        # Secondary overlapping blueprint roll on right side of desk
        s.append('<g transform="translate(556,442) rotate(3)">')
        s.append('<polygon points="8,5 218,10 232,78 -4,74" fill="#050404" opacity="0.45"/>')
        s.append('<polygon points="4,0 214,5 228,73 -8,69" fill="#0E3356" stroke="#7DC2E4" stroke-width="1.0"/>')
        s.append('<path d="M12,18 L200,22 M10,36 L204,40 M8,54 L196,58" fill="none" stroke="#7FE6FF" stroke-width="0.7" opacity="0.45"/>')
        s.append('<path d="M46,8 L42,66 M112,10 L108,68 M168,12 L164,70" fill="none" stroke="#7FE6FF" stroke-width="0.7" opacity="0.45"/>')
        s.append("</g>")

        # Steel ruler & red marker pen on desk center-left
        s.append('<g transform="translate(332,484) rotate(-8)">')
        s.append('<rect x="2" y="3" width="166" height="14" rx="1.5" fill="#050404" opacity="0.45"/>')
        s.append('<rect x="0" y="0" width="166" height="14" rx="1.5" fill="#9AA9B6" stroke="#222A32" stroke-width="1.0"/>')
        for tx in range(8, 160, 8):
            th = 6 if tx % 24 == 0 else 3.5
            s.append(f'<path d="M{tx},0 L{tx},{th}" fill="none" stroke="#1E252C" stroke-width="0.8"/>')
        s.append("</g>")
        # Red marker
        s.append('<g transform="translate(358,452) rotate(14)">')
        s.append('<rect x="0" y="0" width="76" height="8" rx="3" fill="#B82430" stroke="#1A1010" stroke-width="1.0"/>')
        s.append('<rect x="58" y="0.5" width="18" height="7" rx="1.5" fill="#232830"/>')
        s.append("</g>")

        # Small locked Origami Crane v4 resting on desk center
        s.append('<g transform="translate(486,472) rotate(-8)">')
        s.append(K.turna(s=0.30, isik=0.55, golge=True))
        s.append("</g>")

        # Steaming Coffee Mug (right-foreground) + coffee ring stain
        s.append('<ellipse cx="786" cy="496" rx="22" ry="8" fill="none" stroke="#4D2E18" stroke-width="2.0" opacity="0.55"/>')
        # Mug shadow
        s.append('<ellipse cx="838" cy="498" rx="30" ry="11" fill="#050404" opacity="0.55"/>')
        # Mug handle
        s.append('<path d="M858,458 C876,458 878,484 858,486" fill="none" stroke="#D8D2C5" stroke-width="6.5" stroke-linecap="round"/>')
        s.append('<path d="M858,458 C876,458 878,484 858,486" fill="none" stroke="#1C1816" stroke-width="1.4"/>')
        # Mug body
        s.append('<path d="M812,448 L860,448 L856,496 Q836,504 816,496 Z" fill="#DDD6C8" stroke="#1A1512" stroke-width="1.6"/>')
        s.append('<path d="M838,448 L860,448 L856,496 Q846,501 838,500 Z" fill="#AEA596" opacity="0.65"/>')
        # Coffee rim & dark brew
        s.append('<ellipse cx="836" cy="448" rx="24" ry="7.2" fill="#EAE4D8" stroke="#1A1512" stroke-width="1.3"/>')
        s.append('<ellipse cx="836" cy="449" rx="19.5" ry="5.0" fill="#2A170E"/>')
        s.append('<path d="M824,448 Q836,445 848,448" fill="none" stroke="#8C6245" stroke-width="1.0" opacity="0.55"/>')
        # Rising warm steam wisps
        s.append('<path d="M828,438 Q822,422 831,408 Q838,396 829,382" fill="none" stroke="#F4E8D4" stroke-width="2.0" opacity="0.30" stroke-linecap="round"/>')
        s.append('<path d="M842,436 Q850,420 841,404 Q835,392 845,376" fill="none" stroke="#F4E8D4" stroke-width="1.6" opacity="0.22" stroke-linecap="round"/>')

        s.append("</g>")
        parts.append("".join(s))

    # -------------------------------------------------------------------------
    # LAYER 4: PLAN — Live Glowing #7FE6FF Escape Route Overlay (01 -> 02 -> 03 -> 04 · 1 YEAR)
    # -------------------------------------------------------------------------
    if _katman_aktif(katmanlar, "plan"):
        pl: list[str] = ['<g id="s203-plan">']
        # Subtle cyan CAD coordinate frame over the whole board
        pl.append('<rect x="52" y="38" width="844" height="378" fill="none" stroke="#7FE6FF" stroke-width="0.8" stroke-dasharray="6,6" opacity="0.32"/>')

        # Main glowing escape vector path: 01 (Cell 40) -> 02 (Sub-level Pipes) -> 03 (Infirmary) -> 04 (North Wall)
        route_d = "M294,162 L386,162 L386,216 L512,216 L512,144 L564,144 L564,226 L680,226 L680,242 L802,242"
        # Outer glow
        pl.append(
            f'<path d="{route_d}" fill="none" stroke="{PLAN}" stroke-width="7.5" '
            f'opacity="0.24" stroke-linejoin="round" stroke-linecap="round" filter="url(#{p}_glow_cyan)"/>'
        )
        # Main glowing cyan line
        pl.append(
            f'<path d="{route_d}" fill="none" stroke="{PLAN}" stroke-width="2.8" '
            f'opacity="0.96" stroke-linejoin="round" stroke-linecap="round" filter="url(#{p}_glow_soft)"/>'
        )
        # White-cyan inner core
        pl.append(
            f'<path d="{route_d}" fill="none" stroke="{PLAN_CORE}" stroke-width="1.1" '
            f'opacity="0.92" stroke-linejoin="round" stroke-linecap="round"/>'
        )

        # Secondary dashed vector callouts to Guard Shift & North Wall (clear of portrait faces)
        pl.append(
            f'<path d="M144,126 L294,126 L294,162" fill="none" stroke="{PLAN}" stroke-width="1.1" stroke-dasharray="4,3" opacity="0.62"/>'
        )
        pl.append(
            f'<path d="M564,144 L644,144 L644,186 L802,186 L802,242" fill="none" stroke="{PLAN}" stroke-width="1.1" stroke-dasharray="4,3" opacity="0.58"/>'
        )

        # 4 Glowing Waypoint Nodes (01 -> 02 -> 03 -> 04)
        nodes = [
            (294, 162, "01", "CELL 40 · BOLT"),
            (448, 216, "02", "SUB-LEVEL PIPES"),
            (564, 144, "03", "INFIRMARY"),
            (802, 242, "04", "NORTH WALL"),
        ]
        for nx, ny, code, lbl in nodes:
            pl.append(f'<circle cx="{nx}" cy="{ny}" r="13" fill="{PLAN}" opacity="0.18" filter="url(#{p}_glow_cyan)"/>')
            pl.append(f'<circle cx="{nx}" cy="{ny}" r="8.5" fill="#071929" stroke="{PLAN}" stroke-width="2.0"/>')
            pl.append(f'<text x="{nx}" y="{ny+3.2:.1f}" text-anchor="middle" font-family="Consolas,monospace" font-size="8.2" font-weight="bold" fill="{PLAN_CORE}">{code}</text>')
            # Crisp dark pill tag under/above node
            ty = ny - 22 if code in ("01", "03") else ny + 18
            pl.append(f'<rect x="{nx-44}" y="{ty-9}" width="88" height="13" rx="2.5" fill="#071522" fill-opacity="0.86" stroke="{PLAN}" stroke-width="0.7"/>')
            pl.append(f'<text x="{nx}" y="{ty+0.5:.1f}" text-anchor="middle" font-family="Consolas,monospace" font-size="6.8" font-weight="bold" fill="{PLAN}">{lbl}</text>')

        # Top-right HUD Stamp: PRISON BREAK · 1 YEAR · 01 -> 04
        pl.append('<g transform="translate(650,362)">')
        pl.append('<rect x="0" y="0" width="238" height="44" rx="3" fill="#071624" fill-opacity="0.84" stroke="#7FE6FF" stroke-width="1.1"/>')
        pl.append('<path d="M8,16 L230,16" fill="none" stroke="#7FE6FF" stroke-width="0.6" opacity="0.45"/>')
        pl.append('<text x="10" y="12" font-family="Consolas,monospace" font-size="8.0" font-weight="bold" fill="#7FE6FF" letter-spacing="1.0">ESCAPE VECTOR · 01 → 02 → 03 → 04</text>')
        pl.append('<text x="10" y="31" font-family="Arial,sans-serif" font-size="11.5" font-weight="bold" fill="#E6FDFF" letter-spacing="1.6">1 YEAR · PRISON BREAK</text>')
        pl.append('<circle cx="222" cy="27" r="4" fill="#7FE6FF" filter="url(#%s_glow_soft)"/>' % p)
        pl.append("</g>")

        pl.append("</g>")
        parts.append("".join(pl))

    # -------------------------------------------------------------------------
    # LAYER 5: ONPLAN — Overhead Lamp Shade Edge, Warm Cone, Dust Motes & Vignette
    # -------------------------------------------------------------------------
    if _katman_aktif(katmanlar, "onplan"):
        op: list[str] = ['<g id="s203-onplan">']
        # Overhead warm tungsten light cone
        op.append(f'<polygon points="412,18 548,18 820,470 140,470" fill="url(#{p}_cone)"/>')
        # Industrial enamel lamp shade peeking at top-center
        op.append('<path d="M476,0 L484,0 L484,12 L476,12 Z" fill="#181C22"/>')
        op.append('<path d="M406,24 Q480,-2 554,24 L544,28 Q480,14 416,28 Z" fill="#1C242B" stroke="#0A0E12" stroke-width="1.6"/>')
        op.append('<ellipse cx="480" cy="24" rx="58" ry="6" fill="#FFE6A8" opacity="0.82"/>')
        # Floating dust motes caught in lamp beam
        for _ in range(36):
            dx = rng.uniform(180, 780)
            dy = rng.uniform(44, 420)
            dr = rng.uniform(0.7, 1.8)
            op.append(
                f'<circle cx="{dx:.1f}" cy="{dy:.1f}" r="{dr:.1f}" '
                f'fill="{rng.choice(["#FFE5A8","#BCEEFF"])}" opacity="{rng.uniform(0.16,0.45):.2f}"/>'
            )
        # Cinematic vignette
        op.append(f'<rect x="0" y="0" width="960" height="540" fill="url(#{p}_vignette)"/>')
        op.append("</g>")
        parts.append("".join(op))

    return defs, "".join(parts)


# =============================================================================
# SCENE 2.04: TATTOO PARLOR ("4 MONTHS" / "THE MAP")
# =============================================================================
def set_204_dovme_studyosu(
    katmanlar: set[str] | list[str] | None = None,
) -> tuple[str, str]:
    """Atmospheric night tattoo parlor: dim amber-neon backdrop, ink bottles on shelves,
    framed original gothic-architectural flash sketches; center features locked A-Sirt v1
    (K.michael_sirt_dovme(plan_glow=0.85)) anatomical back; gloved tattoo artist's hand
    reaches in from right holding a vibrating coil tattoo machine; glowing #7FE6FF blueprint
    lines rise off the Fox River plan sheet on the left workbench and flow directly onto
    Michael's tattooed back!
    """
    rng = random.Random(204)
    p = _uid("s204")

    # Fetch locked A-Sirt v1 (plan_glow=0.85)
    sirt_defs, sirt_body = K.michael_sirt_dovme(plan_glow=0.85)

    defs = f"""
    {sirt_defs}
    <linearGradient id="{p}_bg_wall" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#110E12"/>
      <stop offset="48%" stop-color="#1C1514"/>
      <stop offset="100%" stop-color="#0B090C"/>
    </linearGradient>
    <radialGradient id="{p}_amber_lamp" cx="0.22" cy="0.24" r="0.46">
      <stop offset="0%" stop-color="#FFCA70" stop-opacity="0.42"/>
      <stop offset="45%" stop-color="#D47D2A" stop-opacity="0.16"/>
      <stop offset="100%" stop-color="#140D0B" stop-opacity="0.0"/>
    </radialGradient>
    <radialGradient id="{p}_neon_red" cx="0.86" cy="0.20" r="0.34">
      <stop offset="0%" stop-color="#FF3B4E" stop-opacity="0.36"/>
      <stop offset="48%" stop-color="#A81E32" stop-opacity="0.14"/>
      <stop offset="100%" stop-color="#120B0E" stop-opacity="0.0"/>
    </radialGradient>
    <radialGradient id="{p}_cyan_back" cx="0.48" cy="0.56" r="0.36">
      <stop offset="0%" stop-color="#7FE6FF" stop-opacity="0.26"/>
      <stop offset="55%" stop-color="#2C92B8" stop-opacity="0.09"/>
      <stop offset="100%" stop-color="#08121D" stop-opacity="0.0"/>
    </radialGradient>
    <linearGradient id="{p}_steel" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#5B6774"/>
      <stop offset="50%" stop-color="#333C46"/>
      <stop offset="100%" stop-color="#1C2229"/>
    </linearGradient>
    <linearGradient id="{p}_brass" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F2D184"/>
      <stop offset="48%" stop-color="#B58335"/>
      <stop offset="100%" stop-color="#6B4716"/>
    </linearGradient>
    <linearGradient id="{p}_glove" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#2E3640"/>
      <stop offset="52%" stop-color="#1B2128"/>
      <stop offset="100%" stop-color="#0E1216"/>
    </linearGradient>
    <linearGradient id="{p}_bp_sheet" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#134573"/>
      <stop offset="100%" stop-color="#08233E"/>
    </linearGradient>
    <radialGradient id="{p}_vignette" cx="0.50" cy="0.48" r="0.65">
      <stop offset="52%" stop-color="#000000" stop-opacity="0.0"/>
      <stop offset="100%" stop-color="#030509" stop-opacity="0.72"/>
    </radialGradient>
    <filter id="{p}_glow_cyan" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="3.4" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="{p}_glow_warm" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="4.0" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    """

    parts: list[str] = []

    # -------------------------------------------------------------------------
    # LAYER 1: UZAK — Dim Parlor Wall, Night Neon Window & Framed Gothic Flash Art
    # -------------------------------------------------------------------------
    if _katman_aktif(katmanlar, "uzak"):
        u: list[str] = ['<g id="s204-uzak">']
        u.append(f'<rect x="0" y="0" width="960" height="540" fill="url(#{p}_bg_wall)"/>')

        # Dark timber wainscot paneling in lower half
        u.append('<rect x="0" y="310" width="960" height="230" fill="#140F0D"/>')
        u.append('<path d="M0,310 L960,310" fill="none" stroke="#36261E" stroke-width="3.0"/>')
        for px in range(20, 960, 76):
            u.append(f'<rect x="{px}" y="324" width="60" height="120" rx="2" fill="#100C0A" stroke="#241914" stroke-width="1.2"/>')

        # Right-upper frosted night street window with crimson-amber neon sign glow
        u.append('<rect x="742" y="24" width="194" height="176" rx="3" fill="#0B1018" stroke="#2A201D" stroke-width="5"/>')
        u.append('<path d="M839,24 L839,200 M742,112 L936,112" fill="none" stroke="#221A18" stroke-width="4"/>')
        # Soft blurred city lights outside
        u.append('<circle cx="786" cy="148" r="14" fill="#F2AE52" opacity="0.22"/>')
        u.append('<circle cx="888" cy="162" r="18" fill="#5CA8D4" opacity="0.18"/>')
        # Hanging neon sign inside window: "INK" / "TATTOO"
        u.append(
            f'<rect x="760" y="54" width="158" height="46" rx="6" fill="none" '
            f'stroke="#FF4A5C" stroke-width="2.2" opacity="0.82" filter="url(#{p}_glow_warm)"/>'
        )
        u.append(
            f'<text x="839" y="85" text-anchor="middle" font-family="Arial,sans-serif" '
            f'font-size="24" font-weight="bold" fill="#FF8C96" letter-spacing="5" '
            f'opacity="0.90" filter="url(#{p}_glow_warm)">TATTOO</text>'
        )

        # Framed Original Gothic-Architectural Flash Sketches on left-upper wall (R1 safe!)
        flash_frames = [
            (36, 36, 118, 134, "ARCH"),
            (172, 42, 108, 122, "CRANE"),
            (598, 34, 118, 130, "VAULT"),
        ]
        for fx, fy, fw, fh, kind in flash_frames:
            u.append(f'<rect x="{fx+4}" y="{fy+5}" width="{fw}" height="{fh}" fill="#050404" opacity="0.52"/>')
            u.append(f'<rect x="{fx}" y="{fy}" width="{fw}" height="{fh}" fill="#1E1714" stroke="#4D392C" stroke-width="3.5"/>')
            u.append(f'<rect x="{fx+8}" y="{fy+8}" width="{fw-16}" height="{fh-16}" fill="#DFD5BF" stroke="#6E5E49" stroke-width="0.9"/>')
            cx, cy = fx + fw * 0.5, fy + fh * 0.5
            if kind == "ARCH":
                # Pointed gothic cathedral window arch + rose medallion
                u.append(
                    f'<path d="M{cx-26:.1f},{fy+fh-18:.1f} L{cx-26:.1f},{cy-6:.1f} '
                    f'Q{cx-26:.1f},{cy-34:.1f} {cx:.1f},{fy+22:.1f} '
                    f'Q{cx+26:.1f},{cy-34:.1f} {cx+26:.1f},{cy-6:.1f} L{cx+26:.1f},{fy+fh-18:.1f} Z" '
                    f'fill="none" stroke="#222A33" stroke-width="1.6"/>'
                )
                u.append(f'<circle cx="{cx:.1f}" cy="{cy-14:.1f}" r="12" fill="none" stroke="#222A33" stroke-width="1.2"/>')
                u.append(f'<path d="M{cx:.1f},{fy+22:.1f} L{cx:.1f},{fy+fh-18:.1f} M{cx-26:.1f},{cy+6:.1f} L{cx+26:.1f},{cy+6:.1f}" fill="none" stroke="#3C4957" stroke-width="0.9"/>')
            elif kind == "CRANE":
                # Geometric origami crane flash study
                u.append(
                    f'<path d="M{cx-32:.1f},{cy-8:.1f} L{cx:.1f},{cy-22:.1f} L{cx+32:.1f},{cy-12:.1f} '
                    f'L{cx+6:.1f},{cy+10:.1f} L{cx:.1f},{cy+28:.1f} L{cx-10:.1f},{cy+8:.1f} Z" '
                    f'fill="none" stroke="#222A33" stroke-width="1.5" stroke-linejoin="round"/>'
                )
                u.append(
                    f'<path d="M{cx-32:.1f},{cy-8:.1f} L{cx+6:.1f},{cy+10:.1f} M{cx:.1f},{cy-22:.1f} L{cx:.1f},{cy+28:.1f}" '
                    f'fill="none" stroke="#4D5C6B" stroke-width="0.9"/>'
                )
            else:
                # Blueprint rosette & compass geometry
                u.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="30" fill="none" stroke="#222A33" stroke-width="1.4"/>')
                u.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="18" fill="none" stroke="#222A33" stroke-width="1.0" stroke-dasharray="3,2"/>')
                u.append(f'<path d="M{cx-34:.1f},{cy:.1f} L{cx+34:.1f},{cy:.1f} M{cx:.1f},{cy-34:.1f} L{cx:.1f},{cy+34:.1f}" fill="none" stroke="#3C4957" stroke-width="0.9"/>')

        # Ambient amber & neon washes
        u.append(f'<rect x="0" y="0" width="960" height="540" fill="url(#{p}_amber_lamp)"/>')
        u.append(f'<rect x="0" y="0" width="960" height="540" fill="url(#{p}_neon_red)"/>')
        u.append(f'<rect x="0" y="0" width="960" height="540" fill="url(#{p}_cyan_back)"/>')
        u.append("</g>")
        parts.append("".join(u))

    # -------------------------------------------------------------------------
    # LAYER 2: ORTA — Ink Bottle Shelf, Warm Sconce & Left Workbench with Blueprint
    # -------------------------------------------------------------------------
    if _katman_aktif(katmanlar, "orta"):
        m: list[str] = ['<g id="s204-orta">']

        # Warm vintage brass wall sconce (left-mid)
        m.append('<rect x="294" y="88" width="12" height="36" rx="3" fill="#4A3624" stroke="#18110C" stroke-width="1.2"/>')
        m.append('<path d="M306,102 L326,102 L326,118" fill="none" stroke="#B58335" stroke-width="3.0"/>')
        m.append('<polygon points="310,118 342,118 348,140 304,140" fill="#2A201A" stroke="#120D0A" stroke-width="1.4"/>')
        m.append(f'<ellipse cx="326" cy="140" rx="18" ry="5" fill="#FFE29A" filter="url(#{p}_glow_warm)"/>')

        # Wall shelf with rows of tattoo ink bottles (left & right-mid)
        # Left shelf
        m.append('<rect x="28" y="246" width="248" height="10" rx="2" fill="#2E1F16" stroke="#120C08" stroke-width="1.4"/>')
        m.append('<path d="M46,256 L46,274 M254,256 L254,274" fill="none" stroke="#1A120D" stroke-width="4.5"/>')
        ink_bottles = [
            (44, 34, "#151A22", "BLK"),
            (68, 30, "#1E2D3E", "BLU"),
            (90, 36, "#16191F", "SUMI"),
            (114, 28, "#6E1D24", "CRIM"),
            (136, 33, "#253A4A", "SLAT"),
            (160, 35, "#15181E", "LINER"),
            (186, 29, "#2A586E", "CYAN"),
            (210, 32, "#1A1F26", "SHAD"),
            (236, 36, "#2D363E", "GRN"),
        ]
        for bx, bh, col, lbl in ink_bottles:
            by = 246 - bh
            # Bottle body
            m.append(f'<rect x="{bx}" y="{by}" width="17" height="{bh}" rx="2.5" fill="{col}" stroke="#0B0D10" stroke-width="1.1"/>')
            # Tapered dropper nozzle cap
            m.append(f'<polygon points="{bx+4},{by} {bx+13},{by} {bx+10},{by-10} {bx+7},{by-10}" fill="#1E2329" stroke="#0B0D10" stroke-width="0.9"/>')
            # Paper label
            m.append(f'<rect x="{bx+2}" y="{by+9}" width="13" height="{bh-14}" fill="#E6DEC8" opacity="0.88"/>')
            m.append(f'<text x="{bx+8.5:.1f}" y="{by+18}" text-anchor="middle" font-family="Arial,sans-serif" font-size="4.4" font-weight="bold" fill="#181512">{lbl}</text>')
            # Glass specular highlight
            m.append(f'<path d="M{bx+3},{by+2} L{bx+3},{by+bh-3}" fill="none" stroke="#FFFFFF" stroke-width="1.1" opacity="0.32"/>')

        # Right-mid utility shelf (antiseptic spray + paper towel roll + ink caps)
        m.append('<rect x="744" y="256" width="194" height="10" rx="2" fill="#2E1F16" stroke="#120C08" stroke-width="1.4"/>')
        # Green soap spray bottle
        m.append('<rect x="768" y="206" width="26" height="50" rx="4" fill="#2E6B5E" stroke="#101816" stroke-width="1.2"/>')
        m.append('<path d="M776,206 L776,196 L792,196 L796,200" fill="none" stroke="#D8E0E6" stroke-width="2.4" stroke-linecap="round"/>')
        m.append('<rect x="772" y="218" width="18" height="22" fill="#E8E4D8" opacity="0.85"/>')
        # Paper towel roll
        m.append('<rect x="816" y="202" width="44" height="54" rx="5" fill="#DDD8CC" stroke="#221F1B" stroke-width="1.3"/>')
        m.append('<ellipse cx="838" cy="202" rx="22" ry="5" fill="#EDE9DF" stroke="#221F1B" stroke-width="1.1"/>')
        m.append('<ellipse cx="838" cy="202" rx="7" ry="2" fill="#5A4E42"/>')

        # --- LEFT WORKBENCH (STAINLESS STEEL) WITH FOX RIVER BLUEPRINT SHEET ---
        # Perspective tabletop on lower-left
        m.append(f'<polygon points="0,378 338,378 308,540 0,540" fill="url(#{p}_steel)" stroke="#12161C" stroke-width="2.0"/>')
        m.append('<path d="M0,380 L338,380" fill="none" stroke="#99AAB8" stroke-width="1.6" opacity="0.65"/>')

        # Open Fox River Architectural Plan Sheet resting on workbench
        m.append('<polygon points="22,396 292,392 266,514 4,518" fill="#060B12" opacity="0.55"/>')
        m.append(f'<polygon points="18,392 288,388 262,510 0,514" fill="url(#{p}_bp_sheet)" stroke="#7FE6FF" stroke-width="1.3"/>')
        # Perspective architectural floorplan lines on the sheet
        m.append('<polygon points="30,404 272,400 250,498 16,502" fill="none" stroke="#5EAED4" stroke-width="0.9" opacity="0.75"/>')
        # Grid & rooms on sheet
        m.append('<path d="M68,403 L56,501 M136,402 L126,500 M204,401 L194,499" fill="none" stroke="#7FE6FF" stroke-width="0.7" opacity="0.45"/>')
        m.append('<path d="M26,432 L264,428 M21,466 L257,462" fill="none" stroke="#7FE6FF" stroke-width="0.7" opacity="0.45"/>')
        # Glowing route already highlighted on the paper blueprint
        m.append(
            f'<path d="M46,482 L106,480 L114,448 L184,446 L192,418 L244,417" '
            f'fill="none" stroke="{PLAN}" stroke-width="2.4" filter="url(#{p}_glow_cyan)"/>'
        )
        m.append(
            f'<path d="M46,482 L106,480 L114,448 L184,446 L192,418 L244,417" '
            f'fill="none" stroke="{PLAN_CORE}" stroke-width="1.0"/>'
        )
        m.append('<text x="26" y="495" font-family="Consolas,monospace" font-size="7.5" font-weight="bold" fill="#9EEBFF">FOX RIVER · SEC A-B</text>')

        # Tiny ink caps & stencil pencil beside blueprint on workbench
        for ix, iy in ((284, 412), (298, 422), (288, 434)):
            m.append(f'<ellipse cx="{ix}" cy="{iy}" rx="7.5" ry="4.0" fill="#12161C" stroke="#8A9AA8" stroke-width="1.0"/>')
            m.append(f'<ellipse cx="{ix}" cy="{iy-0.5:.1f}" rx="5.0" ry="2.2" fill="#0B131C"/>')

        m.append("</g>")
        parts.append("".join(m))

    # -------------------------------------------------------------------------
    # LAYER 3: SAHNE — Locked A-Sirt v1 (plan_glow=0.85) + Gloved Tattoo Artist Hand & Coil Machine
    # -------------------------------------------------------------------------
    if _katman_aktif(katmanlar, "sahne"):
        s: list[str] = ['<g id="s204-sahne">']

        # Studio tattoo stool/chair backrest hint behind lower waist
        s.append('<rect x="360" y="492" width="230" height="48" rx="8" fill="#181518" stroke="#0A080A" stroke-width="2.0"/>')

        # --- HERO CENTER: LOCKED A-SIRT v1 (K.michael_sirt_dovme(plan_glow=0.85)) ---
        # Local coord of A-Sirt is 800x800 centered at (0,0); head top ~ -365, waist bottom ~ +390.
        # Scale 0.64 places head at y~50, shoulders at y~205, lower back at y~530 — heroic framing!
        s.append('<g transform="translate(474,284) scale(0.64)">')
        s.append(sirt_body)
        s.append("</g>")

        # --- RIGHT: GLOVED TATTOO ARTIST'S ARM, HAND & VIBRATING COIL TATTOO MACHINE ---
        # Needle tip touches Michael's upper-right scapula / gothic wing area around (546, 266)
        s.append('<g id="s204-artist-hand">')

        # Draped black power clip-cord hanging down from the coil machine
        s.append(
            '<path d="M686,294 C716,356 692,442 744,540" fill="none" stroke="#080A0D" stroke-width="6.5" stroke-linecap="round"/>'
        )
        s.append(
            '<path d="M686,294 C716,356 692,442 744,540" fill="none" stroke="#2D3742" stroke-width="2.2" stroke-linecap="round"/>'
        )

        # Artist's dark rolled-sleeve forearm entering from right edge
        s.append(
            '<path d="M960,218 L774,264 L792,356 L960,334 Z" fill="#181C22" stroke="#0A0C0F" stroke-width="2.2"/>'
        )
        s.append('<path d="M778,274 L958,232" fill="none" stroke="#36404C" stroke-width="2.4" opacity="0.55"/>')

        # Gloved wrist cuff (black nitrile glove)
        s.append(
            '<path d="M786,260 L740,268 L748,348 L798,350 Z" fill="url(#%s_glove)" stroke="#0A0D10" stroke-width="2.0"/>' % p
        )

        # --- TRADITIONAL COIL TATTOO MACHINE (held at ~-24 deg toward Michael's back) ---
        s.append('<g transform="translate(546,266) rotate(-18)">')
        # Needle tip & steel tube entering skin at (0,0)
        s.append('<path d="M0,0 L28,0" fill="none" stroke="#DCEAF4" stroke-width="1.6"/>')
        s.append('<rect x="18" y="-5" width="44" height="10" rx="2" fill="#8B99A6" stroke="#14181E" stroke-width="1.4"/>')
        # Textured steel grip barrel
        s.append('<rect x="40" y="-9.5" width="32" height="19" rx="3" fill="#4E5B66" stroke="#14181E" stroke-width="1.5"/>')
        for gx in range(44, 70, 5):
            s.append(f'<path d="M{gx},-9 L{gx},9" fill="none" stroke="#222930" stroke-width="1.1"/>')
        # Brass L-frame of coil machine + metallic highlight
        s.append(
            f'<path d="M72,-10 L132,-10 L138,24 L118,28 L114,6 L72,6 Z" '
            f'fill="url(#{p}_brass)" stroke="#1A140B" stroke-width="1.6" stroke-linejoin="round"/>'
        )
        s.append('<path d="M75,-7 L128,-7" fill="none" stroke="#FFF0BE" stroke-width="1.4" opacity="0.72"/>')
        # Clip-cord brass terminal lug on lower rear of frame
        s.append('<circle cx="128" cy="21" r="4.2" fill="#D4A44C" stroke="#1A140B" stroke-width="1.1"/>')
        # Twin electromagnetic copper/black coils
        s.append('<rect x="80" y="-36" width="18" height="26" rx="2.5" fill="#232B34" stroke="#0E1217" stroke-width="1.3"/>')
        s.append('<rect x="103" y="-36" width="18" height="26" rx="2.5" fill="#232B34" stroke="#0E1217" stroke-width="1.3"/>')
        # Copper coil windings
        for wy in range(-32, -12, 4):
            s.append(f'<path d="M81,{wy} L97,{wy} M104,{wy} L120,{wy}" fill="none" stroke="#C87E3C" stroke-width="1.2" opacity="0.82"/>')
        # Top armature bar & contact screw
        s.append('<path d="M62,-42 L126,-42" fill="none" stroke="#C5D2DC" stroke-width="3.2" stroke-linecap="round"/>')
        s.append('<rect x="122" y="-48" width="10" height="38" rx="1.5" fill="#B58335" stroke="#1A140B" stroke-width="1.2"/>')
        s.append('<circle cx="127" cy="-50" r="4" fill="#F2D184" stroke="#1A140B" stroke-width="1.1"/>')
        # Crisp vibration motion arcs around coils & needle tip
        s.append('<path d="M72,-48 Q100,-56 124,-48" fill="none" stroke="#7FE6FF" stroke-width="1.3" opacity="0.72" stroke-dasharray="3,2"/>')
        s.append('<path d="M3,-11 Q-6,0 3,11" fill="none" stroke="#E6FDFF" stroke-width="1.5" opacity="0.85"/>')
        s.append('<path d="M9,-16 Q-2,0 9,16" fill="none" stroke="#7FE6FF" stroke-width="1.1" opacity="0.62"/>')
        s.append("</g>")

        # Gloved fingers wrapping firmly over the steel grip & machine frame
        # Palm mass
        s.append(
            f'<path d="M754,264 Q710,248 672,262 Q646,274 644,304 Q656,338 700,348 Q738,354 762,338 Z" '
            f'fill="url(#{p}_glove)" stroke="#0A0D10" stroke-width="2.0"/>'
        )
        # Index finger pressing firmly along machine grip barrel
        s.append(
            f'<path d="M674,262 Q634,244 598,250 Q586,255 590,268 Q604,276 644,273 L672,276 Z" '
            f'fill="url(#{p}_glove)" stroke="#0A0D10" stroke-width="1.9"/>'
        )
        # Middle & ring fingers curled underneath grip
        s.append(
            f'<path d="M664,282 Q624,278 604,286 Q596,294 606,304 Q628,308 666,302 Z" '
            f'fill="url(#{p}_glove)" stroke="#0A0D10" stroke-width="1.8"/>'
        )
        s.append(
            f'<path d="M668,304 Q634,306 618,314 Q612,322 624,328 Q646,330 676,322 Z" '
            f'fill="url(#{p}_glove)" stroke="#0A0D10" stroke-width="1.8"/>'
        )
        # Stronger anatomical thumb stabilizing top of barrel
        s.append(
            f'<path d="M712,264 Q678,228 634,226 Q618,229 620,244 Q636,256 676,268 Z" '
            f'fill="url(#{p}_glove)" stroke="#0A0D10" stroke-width="1.8"/>'
        )
        # Crisp nitrile specular highlights on knuckles & glove folds
        s.append('<path d="M608,255 Q636,251 664,260" fill="none" stroke="#6F869B" stroke-width="1.4" opacity="0.55" stroke-linecap="round"/>')
        s.append('<path d="M636,238 Q664,240 688,256" fill="none" stroke="#859DB3" stroke-width="1.5" opacity="0.52" stroke-linecap="round"/>')
        s.append('<path d="M704,282 Q728,292 746,288" fill="none" stroke="#5D7082" stroke-width="1.3" opacity="0.45" stroke-linecap="round"/>')

        # Active needle contact spark / fresh glowing ink point on Michael's back
        s.append(f'<circle cx="546" cy="266" r="11" fill="{PLAN}" opacity="0.32" filter="url(#{p}_glow_cyan)"/>')
        s.append(f'<circle cx="546" cy="266" r="3.4" fill="{PLAN_CORE}"/>')

        s.append("</g>")
        s.append("</g>")
        parts.append("".join(s))

    # -------------------------------------------------------------------------
    # LAYER 4: PLAN — Blueprint-to-Back Flowing #7FE6FF Floorplan Stream & HUD
    # -------------------------------------------------------------------------
    if _katman_aktif(katmanlar, "plan"):
        pl: list[str] = ['<g id="s204-plan">']

        # Flowing cyan blueprint streams rising off the left Fox River plan sheet
        # directly into Michael's tattooed back nodes!
        flow_paths = [
            # Stream 1: Sheet lower-left -> Left shoulder crane / node 03
            ("M114,448 C156,374 252,368 382,344 C408,339 422,334 434,332", 2.4, 0.92, ""),
            # Stream 2: Sheet center -> Spine node 01 (top arch)
            ("M184,446 C224,336 318,242 474,234", 2.8, 0.96, ""),
            # Stream 3: Sheet upper-right -> Right scapula / active tattoo needle (546,266)
            ("M244,417 C296,356 382,306 546,266", 2.2, 0.88, "6,4"),
            # Stream 4: Sheet lower -> Lower back node 04
            ("M106,480 C196,472 304,458 468,448", 1.8, 0.78, "5,3"),
        ]
        for d_str, sw, op_val, dash in flow_paths:
            dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
            # Soft neon aura
            pl.append(
                f'<path d="{d_str}" fill="none" stroke="{PLAN}" stroke-width="{sw*2.8:.1f}" '
                f'opacity="{op_val*0.24:.2f}" filter="url(#{p}_glow_cyan)"/>'
            )
            # Main cyan architectural flow line
            pl.append(
                f'<path d="{d_str}" fill="none" stroke="{PLAN}" stroke-width="{sw:.1f}" '
                f'opacity="{op_val:.2f}"{dash_attr} stroke-linecap="round"/>'
            )
            # Inner core filament
            if not dash:
                pl.append(
                    f'<path d="{d_str}" fill="none" stroke="{PLAN_CORE}" stroke-width="0.9" '
                    f'opacity="0.88" stroke-linecap="round"/>'
                )

        # Floating architectural geometry ticks & mini-nodes along the rising stream
        floating_nodes = [
            (184, 446, "BP-01"),
            (244, 417, "BP-02"),
            (318, 308, "SYNC"),
            (378, 344, "WING-A"),
        ]
        for fx, fy, lbl in floating_nodes:
            pl.append(f'<circle cx="{fx}" cy="{fy}" r="4.2" fill="#071826" stroke="{PLAN}" stroke-width="1.4"/>')
            pl.append(f'<circle cx="{fx}" cy="{fy}" r="1.6" fill="{PLAN_CORE}"/>')
            pl.append(
                f'<text x="{fx+7}" y="{fy-5}" font-family="Consolas,monospace" font-size="6.8" '
                f'font-weight="bold" fill="{PLAN}" opacity="0.88">{lbl}</text>'
            )

        # Floating holographic floorplan mini-projection lifting off the sheet into mid-air
        pl.append('<g transform="translate(154,286) skewY(-10)" opacity="0.82">')
        pl.append('<rect x="0" y="0" width="94" height="58" fill="#071B2E" fill-opacity="0.42" stroke="#7FE6FF" stroke-width="1.0"/>')
        pl.append('<path d="M0,20 L94,20 M0,40 L94,40 M32,0 L32,58 M64,0 L64,58" fill="none" stroke="#7FE6FF" stroke-width="0.6" opacity="0.45"/>')
        pl.append('<path d="M12,48 L44,48 L44,24 L78,24 L78,10" fill="none" stroke="#E6FDFF" stroke-width="1.6" filter="url(#%s_glow_cyan)"/>' % p)
        pl.append('<circle cx="12" cy="48" r="2.5" fill="#7FE6FF"/><circle cx="78" cy="10" r="2.5" fill="#E6FDFF"/>')
        pl.append('<text x="4" y="10" font-family="Consolas,monospace" font-size="6.0" font-weight="bold" fill="#9EEBFF">WING A → INFIRMARY</text>')
        pl.append("</g>")

        # Subtle floating architectural crosshairs & elevation ticks behind Michael's shoulders
        pl.append('<circle cx="348" cy="186" r="24" fill="none" stroke="#7FE6FF" stroke-width="0.8" stroke-dasharray="3,3" opacity="0.45"/>')
        pl.append('<path d="M320,186 L376,186 M348,158 L348,214" fill="none" stroke="#7FE6FF" stroke-width="0.7" opacity="0.42"/>')

        # Bottom-right HUD Stamp: 4 MONTHS · THE MAP
        pl.append('<g transform="translate(698,468)">')
        pl.append('<rect x="0" y="0" width="236" height="46" rx="3" fill="#071522" fill-opacity="0.86" stroke="#7FE6FF" stroke-width="1.1"/>')
        pl.append('<path d="M8,17 L228,17" fill="none" stroke="#7FE6FF" stroke-width="0.6" opacity="0.45"/>')
        pl.append('<text x="10" y="13" font-family="Consolas,monospace" font-size="7.8" font-weight="bold" fill="#7FE6FF" letter-spacing="0.9">BLUEPRINT TRANSFER · ACTIVE</text>')
        pl.append('<text x="10" y="34" font-family="Arial,sans-serif" font-size="12.2" font-weight="bold" fill="#E6FDFF" letter-spacing="1.6">4 MONTHS · THE MAP</text>')
        pl.append('<circle cx="220" cy="30" r="4" fill="#7FE6FF" filter="url(#%s_glow_cyan)"/>' % p)
        pl.append("</g>")

        pl.append("</g>")
        parts.append("".join(pl))

    # -------------------------------------------------------------------------
    # LAYER 5: ONPLAN — Parlor Depth Framing, Warm/Cyan Floating Motes & Vignette
    # -------------------------------------------------------------------------
    if _katman_aktif(katmanlar, "onplan"):
        op: list[str] = ['<g id="s204-onplan">']
        # Subtle warm amber & cyan airborne motes
        for _ in range(34):
            dx = rng.uniform(40, 920)
            dy = rng.uniform(35, 500)
            dr = rng.uniform(0.7, 1.8)
            col = "#7FE6FF" if (220 < dx < 620 and 200 < dy < 470) else "#FFD48A"
            op.append(f'<circle cx="{dx:.1f}" cy="{dy:.1f}" r="{dr:.1f}" fill="{col}" opacity="{rng.uniform(0.16,0.44):.2f}"/>')
        # Cinematic vignette
        op.append(f'<rect x="0" y="0" width="960" height="540" fill="url(#{p}_vignette)"/>')
        op.append("</g>")
        parts.append("".join(op))

    return defs, "".join(parts)


# =============================================================================
# RENDERING & CARD GENERATION (1280x720 SET CARD + 1280x720 R13 200% QC CARD)
# =============================================================================
def _render_scene_pil(scene_fn, w: int = 1920, h: int = 1080) -> Image.Image:
    defs, body = scene_fn()
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {W_SCENE} {H_SCENE}">'
        f"<defs>{defs}</defs>{body}</svg>"
    )
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
            return ImageFont.truetype(fp, size)
    return ImageFont.load_default()


def _draw_card_bg(w: int, h: int) -> Image.Image:
    svg = f"""
    <svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
      <defs>
        <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0%" stop-color="#0B131F"/>
          <stop offset="50%" stop-color="#101A28"/>
          <stop offset="100%" stop-color="#080E17"/>
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
    draw: ImageDraw.ImageDraw, x: int, y: int, colors: list[str], size: int = 18, gap: int = 6
) -> None:
    for i, hex_c in enumerate(colors):
        cx = x + i * (size + gap)
        draw.rounded_rectangle((cx, y, cx + size, y + size), radius=3, fill=hex_c, outline="#384D66", width=1)


def uret_kartlar(versiyon: str = "v1") -> tuple[Path, Path]:
    print("Rendering 2 Act II scenes at 1920x1080...")
    img_203 = _render_scene_pil(set_203_plan_duvari, 1920, 1080)
    img_204 = _render_scene_pil(set_204_dovme_studyosu, 1920, 1080)

    # =========================================================================
    # OUTPUT 1: SET PRESENTATION CARD (1280 x 720 — 100% ENGLISH)
    # =========================================================================
    canvas = _draw_card_bg(1280, 720)
    draw = ImageDraw.Draw(canvas)

    f_title = _load_font(20, bold=True)
    f_sub = _load_font(12, bold=False)
    f_card_t = _load_font(14, bold=True)
    f_card_s = _load_font(11, bold=False)
    f_small = _load_font(10, bold=False)

    draw.text((24, 13), "MICHAEL SCOFIELD  ·  ACT II PLANNING WALL & TATTOO PARLOR SET", fill="#EBF3FA", font=f_title)
    draw.text(
        (24, 38),
        "STYLE B+A HYBRID (CINEMATIC 2D + CYAN BLUEPRINT VISION)  ·  SCENES 2.03 – 2.04",
        fill="#7E97B0",
        font=f_sub,
    )
    top_swatches = [
        ("#2B1B15", "BRICK"),
        ("#D92A38", "STRING"),
        ("#0C2F51", "PLAN"),
        ("#E59842", "AMBER"),
        ("#7FE6FF", "VISION"),
    ]
    sx_top = 832
    for col, lbl in top_swatches:
        draw.rounded_rectangle((sx_top, 18, sx_top + 14, 32), radius=3, fill=col, outline="#3B536D", width=1)
        draw.text((sx_top + 19, 19), lbl, fill="#9BB2C8", font=f_small)
        sx_top += 85
    draw.line((24, 57, 1256, 57), fill="#213247", width=1)

    # --- LEFT HERO PANEL: 2.03 CONSPIRACY PLANNING WALL ---
    _draw_panel_box(draw, (22, 68, 632, 698))
    t203 = img_203.resize((584, 329), Image.Resampling.LANCZOS)
    canvas.paste(t203, (35, 102), t203)
    draw.rectangle((35, 102, 35 + 584, 102 + 329), outline="#324B66", width=1)
    draw.text((35, 76), "01 · 2.03 CONSPIRACY PLANNING WALL", fill="#7FE6FF", font=f_card_t)
    draw.text((322, 79), "Title Card: \"1 YEAR\" · \"PRISON BREAK\"", fill="#9AB3CC", font=f_card_s)

    y_info = 446
    draw.text((36, y_info), "PALETTE", fill="#7FE6FF", font=f_small)
    _draw_swatches(draw, 36, y_info + 16, ["#271A15", "#0C2F51", "#D92A38", "#F5DF7B", "#FFD180", "#7FE6FF"], size=20, gap=6)

    draw.text((36, y_info + 52), "KEY ELEMENTS", fill="#9BB2C8", font=f_small)
    for idx, txt in enumerate(
        [
            "• Dim Chicago brick wall + massive cork conspiracy board",
            "• Pinned Fox River architectural blueprint & Guard Shift Schedule",
            "• Locked Lincoln v1 (#79238) & Sara v2 photos + North Wall shot",
            "• Red strings + post-its: ALLEN BOLT, INFIRMARY, PIPES, 1 YEAR",
            "• Desk with sketches, steaming mug, locked Crane v4 & live 01→04",
        ]
    ):
        draw.text((36, y_info + 70 + idx * 20), txt, fill="#D8E5F1", font=f_card_s)

    draw.line((36, y_info + 178, 618, y_info + 178), fill="#213347", width=1)
    draw.text((36, y_info + 188), "LIGHTING & LAYERS (5)", fill="#9BB2C8", font=f_small)
    draw.text(
        (36, y_info + 204),
        "Warm overhead tungsten cone vs. cold window rim + #7FE6FF vector glow",
        fill="#F6C367",
        font=f_card_s,
    )
    draw.text(
        (36, y_info + 222),
        "s203-uzak · s203-orta · s203-sahne · s203-plan · s203-onplan",
        fill="#829CB5",
        font=f_small,
    )

    # --- RIGHT HERO PANEL: 2.04 TATTOO PARLOR ---
    _draw_panel_box(draw, (648, 68, 1258, 698))
    t204 = img_204.resize((584, 329), Image.Resampling.LANCZOS)
    canvas.paste(t204, (661, 102), t204)
    draw.rectangle((661, 102, 661 + 584, 102 + 329), outline="#324B66", width=1)
    draw.text((661, 76), "02 · 2.04 TATTOO PARLOR", fill="#F6C367", font=f_card_t)
    draw.text((868, 79), "Title Card: \"4 MONTHS\" · \"THE MAP\"", fill="#9AB3CC", font=f_card_s)

    draw.text((662, y_info), "PALETTE", fill="#7FE6FF", font=f_small)
    _draw_swatches(draw, 662, y_info + 16, ["#161113", "#E59842", "#FF4A5C", "#D5A687", "#222E3B", "#7FE6FF"], size=20, gap=6)

    draw.text((662, y_info + 52), "KEY ELEMENTS", fill="#9BB2C8", font=f_small)
    for idx, txt in enumerate(
        [
            "• Atmospheric night parlor: amber sconce, neon sign & ink shelves",
            "• Framed original gothic-architectural & origami flash studies (R1)",
            "• Center: locked A-Sirt v1 (K.michael_sirt_dovme, plan_glow=0.85)",
            "• Black-gloved tattoo artist hand + vibrating brass coil machine",
            "• #7FE6FF blueprint lines flowing from workbench sheet onto back",
        ]
    ):
        draw.text((662, y_info + 70 + idx * 20), txt, fill="#D8E5F1", font=f_card_s)

    draw.line((662, y_info + 178, 1244, y_info + 178), fill="#213347", width=1)
    draw.text((662, y_info + 188), "LIGHTING & LAYERS (5)", fill="#9BB2C8", font=f_small)
    draw.text(
        (662, y_info + 204),
        "Amber lamp + crimson neon rim vs. glowing #7FE6FF blueprint transfer",
        fill="#F6C367",
        font=f_card_s,
    )
    draw.text(
        (662, y_info + 222),
        "s204-uzak · s204-orta · s204-sahne · s204-plan · s204-onplan",
        fill="#829CB5",
        font=f_small,
    )

    out_main = OUT_DIR / f"b2_set_plan_dovme_{versiyon}.png"
    canvas.convert("RGB").save(out_main, quality=95)

    # =========================================================================
    # OUTPUT 2: R13 200% ZOOM QUALITY CONTROL CARD (1280 x 720 — 4 PANELS)
    # =========================================================================
    r13 = _draw_card_bg(1280, 720)
    d13 = ImageDraw.Draw(r13)
    d13.text((24, 13), "R13 · 200% ZOOM QUALITY CONTROL (ACT II PLANNING WALL & TATTOO PARLOR)", fill="#EBF3FA", font=f_title)
    d13.text(
        (24, 37),
        "1:1 PIXEL CROPS FROM 1920×1080 SOURCE  ·  TYPOGRAPHY, LOCKED ASSETS, INK & GLOW FIDELITY",
        fill="#7E97B0",
        font=f_sub,
    )
    d13.line((24, 55, 1256, 55), fill="#213247", width=1)

    cw, ch = 600, 264
    crops = [
        (
            img_203,
            (690, 680),
            "1 · 2.03 FOX RIVER PLAN, POST-ITS & RED STRINGS (200%)",
            "Blueprint title block, ALLEN BOLT · PIPES · INFIRMARY post-its & red strings",
            (22, 66),
        ),
        (
            img_203,
            (1530, 250),
            "2 · 2.03 LOCKED LINCOLN v1 & SARA v2 PHOTOS + NORTH WALL (200%)",
            "Clean pinned polaroids (K.lincoln_kafa & K.sara_kafa) with unobstructed faces",
            (652, 66),
        ),
        (
            img_204,
            (1130, 560),
            "3 · 2.04 LOCKED A-SIRT v1 (0.85 GLOW) & COIL MACHINE (200%)",
            "Anatomical back tattoo glow, black nitrile glove, brass coils & needle spark",
            (22, 392),
        ),
        (
            img_204,
            (360, 540),
            "4 · 2.04 INK SHELF & BLUEPRINT-TO-BACK CYAN STREAM (200%)",
            "Ink bottles, floating WING A→INFIRMARY projection & #7FE6FF flow onto back",
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

    out_r13 = OUT_DIR / "b2_set_plan_dovme_r13.png"
    r13.convert("RGB").save(out_r13, quality=95)
    print(f"Saved:\n  - {out_main}\n  - {out_r13}")
    return out_main, out_r13


if __name__ == "__main__":
    uret_kartlar("v1")
