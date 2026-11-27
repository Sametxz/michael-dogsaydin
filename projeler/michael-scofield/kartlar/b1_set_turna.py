"""V2 (Act I — Crane, High School & $90K Diner Scene Artist) — Style B + A Hybrid.

Isolated module producing 3 richly detailed, 5-layer (960x540) cinematic 2D sets:
  - set_105_sabah_yatak(katmanlar=None)  -> (defs_svg, body_svg)  [Morning Bedside · I'M HERE]
  - set_106_lise_origami(katmanlar=None) -> (defs_svg, body_svg)  [High School Craft Desk · HIGH SCHOOL]
  - set_107_lokanta_cek(katmanlar=None)  -> (defs_svg, body_svg)  [Night Diner & $90,000 Sacrifice · AGE 18]

Each scene uses 5 named <g> depth layers: uzak, orta, sahne, plan, onplan.
Locked character/prop sources imported read-only from karakter.py:
  - K.turna(...)
  - K.lincoln_kafa(...)
All on-screen text and presentation cards are in ENGLISH.
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
INK_WARM = "#211711"
PLAN = "#7FE6FF"
PLAN_CORE = "#E0FBFF"

_UID = 0


def _uid(prefix: str = "b1") -> str:
    global _UID
    _UID += 1
    return f"{prefix}_{_UID}"


def _katman_aktif(katmanlar: set[str] | list[str] | None, ad: str) -> bool:
    return katmanlar is None or ad in katmanlar


# =============================================================================
# 1.05 · MORNING BEDSIDE ("I'M HERE")
# =============================================================================
def set_105_sabah_yatak(katmanlar: set[str] | list[str] | None = None) -> tuple[str, str]:
    """Sun-drenched morning bedroom: wooden slatted headboard, wrinkled cotton sheets,
    quilted blanket, warm bedside lamp, vintage alarm clock, Venetian blinds casting
    diagonal golden sunbeams & dust motes onto the locked Turna v4 like a jewel."""
    rng = random.Random(105)
    p = _uid("s105")

    defs = f"""
    <linearGradient id="{p}_wall" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#3E2E22"/>
      <stop offset="45%" stop-color="#6B513A"/>
      <stop offset="78%" stop-color="#A88259"/>
      <stop offset="100%" stop-color="#D9AE76"/>
    </linearGradient>
    <linearGradient id="{p}_win_sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#FFF9DF"/>
      <stop offset="55%" stop-color="#FFE09A"/>
      <stop offset="100%" stop-color="#F2B45E"/>
    </linearGradient>
    <linearGradient id="{p}_wood_head" x1="0" y1="0" x2="1" y2="0.4">
      <stop offset="0%" stop-color="#3A2214"/>
      <stop offset="52%" stop-color="#5B3720"/>
      <stop offset="88%" stop-color="#7B4C2D"/>
      <stop offset="100%" stop-color="#9A663F"/>
    </linearGradient>
    <linearGradient id="{p}_wood_night" x1="0" y1="0" x2="1" y2="0.2">
      <stop offset="0%" stop-color="#432717"/>
      <stop offset="55%" stop-color="#643D24"/>
      <stop offset="100%" stop-color="#875534"/>
    </linearGradient>
    <linearGradient id="{p}_sheet_base" x1="0.1" y1="0" x2="0.85" y2="1">
      <stop offset="0%" stop-color="#D5C2A8"/>
      <stop offset="35%" stop-color="#EFE2CA"/>
      <stop offset="68%" stop-color="#FFF5DE"/>
      <stop offset="100%" stop-color="#DFC6A2"/>
    </linearGradient>
    <linearGradient id="{p}_pillow" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#C8B49B"/>
      <stop offset="52%" stop-color="#EFE3CE"/>
      <stop offset="100%" stop-color="#FFF8E8"/>
    </linearGradient>
    <linearGradient id="{p}_quilt" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#293A4D"/>
      <stop offset="55%" stop-color="#3B536D"/>
      <stop offset="100%" stop-color="#56728E"/>
    </linearGradient>
    <linearGradient id="{p}_lamp_shade" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#FFEBB8"/>
      <stop offset="60%" stop-color="#F6C36E"/>
      <stop offset="100%" stop-color="#D98D3B"/>
    </linearGradient>
    <radialGradient id="{p}_lamp_glow" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0%" stop-color="#FFE6A3" stop-opacity="0.72"/>
      <stop offset="48%" stop-color="#F2AA49" stop-opacity="0.26"/>
      <stop offset="100%" stop-color="#D9822B" stop-opacity="0.0"/>
    </radialGradient>
    <linearGradient id="{p}_beam" x1="1" y1="0" x2="0.15" y2="1">
      <stop offset="0%" stop-color="#FFF6D1" stop-opacity="0.56"/>
      <stop offset="42%" stop-color="#FFE196" stop-opacity="0.28"/>
      <stop offset="82%" stop-color="#F7C268" stop-opacity="0.10"/>
      <stop offset="100%" stop-color="#E5A243" stop-opacity="0.0"/>
    </linearGradient>
    <radialGradient id="{p}_crane_halo" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0%" stop-color="#FFF9DC" stop-opacity="0.88"/>
      <stop offset="38%" stop-color="#FFDF8E" stop-opacity="0.42"/>
      <stop offset="100%" stop-color="#F2AE4B" stop-opacity="0.0"/>
    </radialGradient>
    <radialGradient id="{p}_vignette" cx="0.54" cy="0.55" r="0.68">
      <stop offset="52%" stop-color="#000000" stop-opacity="0.0"/>
      <stop offset="100%" stop-color="#1A1008" stop-opacity="0.62"/>
    </radialGradient>
    <filter id="{p}_glow_warm" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="5.5" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="{p}_glow_soft" x="-25%" y="-25%" width="150%" height="150%">
      <feGaussianBlur stdDeviation="2.6" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    """

    parts: list[str] = []

    # --- LAYER 1: UZAK (Textured wallpaper, framed sketch, Venetian blind window) ---
    if _katman_aktif(katmanlar, "uzak"):
        u: list[str] = ['<g id="s105-uzak">']
        u.append(f'<rect x="0" y="0" width="960" height="540" fill="url(#{p}_wall)"/>')
        # Subtle vintage vertical wallpaper stripes + plaster micro-texture
        for wx in range(18, 960, 32):
            u.append(f'<rect x="{wx}" y="0" width="12" height="390" fill="#2A1D14" opacity="0.10"/>')
            u.append(f'<path d="M{wx+6},0 L{wx+6},390" fill="none" stroke="#FFE7BE" stroke-width="0.6" opacity="0.12"/>')
        # Wainscoting & wooden baseboard trim
        u.append(f'<rect x="0" y="346" width="960" height="12" fill="#4A2E1B" stroke="{INK_WARM}" stroke-width="1.4"/>')
        u.append(f'<rect x="0" y="358" width="960" height="44" fill="#362113"/>')
        # Framed childhood pencil sketch on left wall
        u.append(f'<rect x="292" y="64" width="114" height="90" rx="2" fill="#3E2516" stroke="{INK_WARM}" stroke-width="1.8"/>')
        u.append('<rect x="300" y="72" width="98" height="74" fill="#EFE4CC" stroke="#5A3A23" stroke-width="1.0"/>')
        # Mini bird/cloud sketch inside frame
        u.append('<path d="M312,126 Q346,112 386,124" fill="none" stroke="#8C7B66" stroke-width="1.1"/>')
        u.append('<path d="M334,102 L349,92 L364,104 L349,108 Z" fill="#C9BCA4" stroke="#5D4E3E" stroke-width="0.9"/>')
        u.append('<path d="M324,86 Q336,80 346,86 M358,84 Q368,78 378,84" fill="none" stroke="#9B8A74" stroke-width="1.0"/>')

        # Right-side tall bedroom window with golden morning sky + Venetian blinds
        wx0, wy0, ww, wh = 636, 18, 286, 304
        # Outer sun bloom around window
        u.append(f'<rect x="{wx0-18}" y="{wy0-12}" width="{ww+36}" height="{wh+24}" fill="#FFE8A8" opacity="0.16" filter="url(#{p}_glow_warm)"/>')
        u.append(f'<rect x="{wx0}" y="{wy0}" width="{ww}" height="{wh}" fill="url(#{p}_win_sky)"/>')
        # Distant blurred tree canopy silhouettes outside window
        u.append('<path d="M636,248 Q690,192 752,226 Q810,174 876,214 Q902,196 922,222 L922,322 L636,322 Z" fill="#D2954B" opacity="0.42"/>')
        u.append('<path d="M636,282 Q710,248 794,268 Q856,244 922,272 L922,322 L636,322 Z" fill="#A66B30" opacity="0.38"/>')

        # Venetian blinds slats (angled slats letting bright golden bands through)
        slat_y = wy0 + 14
        idx = 0
        while slat_y < wy0 + wh - 10:
            # Tilted slat shadow + bright top edge
            u.append(f'<rect x="{wx0+4}" y="{slat_y:.1f}" width="{ww-8}" height="9.2" fill="#4A3322" opacity="0.88"/>')
            u.append(f'<path d="M{wx0+4},{slat_y:.1f} L{wx0+ww-4},{slat_y:.1f}" fill="none" stroke="#FFF4D2" stroke-width="1.5" opacity="0.85"/>')
            # Thin sunlit gap glow
            u.append(f'<rect x="{wx0+4}" y="{slat_y+9.2:.1f}" width="{ww-8}" height="4.8" fill="#FFF9DC" opacity="0.72"/>')
            slat_y += 17.5
            idx += 1
        # Vertical blind ladder cords
        for cx_cord in (wx0 + 54, wx0 + ww - 54):
            u.append(f'<path d="M{cx_cord},{wy0+8} L{cx_cord},{wy0+wh-8}" fill="none" stroke="#302016" stroke-width="1.5" opacity="0.75"/>')
        # Pull cord with wooden tassel
        u.append(f'<path d="M{wx0+ww-22},{wy0+14} L{wx0+ww-22},{wy0+236}" fill="none" stroke="#4D3523" stroke-width="1.6"/>')
        u.append(f'<polygon points="{wx0+ww-26},{wy0+236} {wx0+ww-18},{wy0+236} {wx0+ww-16},{wy0+250} {wx0+ww-28},{wy0+250}" fill="#7C502E" stroke="{INK_WARM}" stroke-width="1.2"/>')

        # Heavy wooden window casing & sill
        u.append(f'<rect x="{wx0-12}" y="{wy0-12}" width="{ww+24}" height="14" fill="#4D2E1B" stroke="{INK_WARM}" stroke-width="1.6"/>')
        u.append(f'<rect x="{wx0-12}" y="{wy0}" width="14" height="{wh}" fill="#5A3620" stroke="{INK_WARM}" stroke-width="1.6"/>')
        u.append(f'<rect x="{wx0+ww-2}" y="{wy0}" width="14" height="{wh}" fill="#462917" stroke="{INK_WARM}" stroke-width="1.6"/>')
        u.append(f'<rect x="{wx0-20}" y="{wy0+wh-2}" width="{ww+40}" height="18" rx="2" fill="#7D4F2E" stroke="{INK_WARM}" stroke-width="1.8"/>')
        u.append(f'<path d="M{wx0-18},{wy0+wh+1} L{wx0+ww+18},{wy0+wh+1}" fill="none" stroke="#FFE5A8" stroke-width="1.8" opacity="0.78"/>')

        # Soft translucent left curtain edge catching morning light
        u.append(f'<path d="M612,12 Q646,120 628,236 Q616,300 634,358 L586,358 Q598,220 584,12 Z" fill="#F2E2C4" opacity="0.34" stroke="#D2B68E" stroke-width="1.0"/>')
        u.append('<path d="M604,16 Q622,140 608,354 M618,16 Q638,150 622,354" fill="none" stroke="#FFF6DE" stroke-width="1.1" opacity="0.45"/>')

        # Diagonal sunlit blind-slat bands projected across the back wall
        for b_i in range(6):
            by = 48 + b_i * 44
            u.append(
                f'<polygon points="624,{by} 624,{by+18} 368,{by+142} 368,{by+124}" '
                f'fill="#FFE9AD" opacity="0.16"/>'
            )
        u.append('</g>')
        parts.append("".join(u))

    # --- LAYER 2: ORTA (Wooden slatted headboard, nightstand, warm lamp, vintage alarm clock) ---
    if _katman_aktif(katmanlar, "orta"):
        m: list[str] = ['<g id="s105-orta">']
        # Wooden bed headboard on left-back (perspective angled)
        # Main posts
        m.append(f'<rect x="26" y="88" width="28" height="292" rx="3" fill="url(#{p}_wood_head)" stroke="{INK_WARM}" stroke-width="2.0"/>')
        m.append(f'<ellipse cx="40" cy="84" rx="18" ry="12" fill="#7B4C2D" stroke="{INK_WARM}" stroke-width="1.8"/>')
        m.append(f'<rect x="386" y="138" width="24" height="222" rx="3" fill="url(#{p}_wood_head)" stroke="{INK_WARM}" stroke-width="1.9"/>')
        m.append(f'<ellipse cx="398" cy="134" rx="15" ry="10" fill="#8C5936" stroke="{INK_WARM}" stroke-width="1.7"/>')
        # Top curved headboard rail
        m.append(f'<path d="M48,118 Q224,96 392,158 L392,188 Q224,132 48,152 Z" fill="url(#{p}_wood_head)" stroke="{INK_WARM}" stroke-width="1.9"/>')
        m.append('<path d="M52,121 Q224,100 388,160" fill="none" stroke="#D89F68" stroke-width="1.5" opacity="0.65"/>')
        # Vertical wooden slats/spindles
        for sx in (82, 124, 166, 208, 250, 292, 334, 368):
            t_ratio = (sx - 48) / 344.0
            sy_top = 140 + t_ratio * 34
            m.append(f'<rect x="{sx}" y="{sy_top:.1f}" width="16" height="196" fill="#5C3821" stroke="{INK_WARM}" stroke-width="1.4"/>')
            m.append(f'<path d="M{sx+13},{sy_top+4:.1f} L{sx+13},{sy_top+185:.1f}" fill="none" stroke="#A67047" stroke-width="1.1" opacity="0.55"/>')
        # Headboard wood grain lines
        for gx in (34, 44, 394):
            m.append(f'<path d="M{gx},108 Q{gx+3},210 {gx-2},348" fill="none" stroke="#28160C" stroke-width="0.9" opacity="0.55"/>')

        # Nightstand (wooden cabinet to the right of headboard, near window)
        nx0, ny0 = 442, 246
        # Nightstand top overhang
        m.append(f'<polygon points="{nx0-10},{ny0} {nx0+142},{ny0-16} {nx0+184},{ny0+8} {nx0+28},{ny0+26}" fill="#855433" stroke="{INK_WARM}" stroke-width="1.8"/>')
        m.append(f'<path d="M{nx0-8},{ny0+1} L{nx0+140},{ny0-15}" fill="none" stroke="#F0BE82" stroke-width="1.4" opacity="0.7"/>')
        # Front body & side panel
        m.append(f'<polygon points="{nx0},{ny0+24} {nx0+136},{ny0+10} {nx0+136},{ny0+142} {nx0},{ny0+156}" fill="url(#{p}_wood_night)" stroke="{INK_WARM}" stroke-width="1.8"/>')
        m.append(f'<polygon points="{nx0+136},{ny0+10} {nx0+176},{ny0+8} {nx0+176},{ny0+130} {nx0+136},{ny0+142}" fill="#4A2C1A" stroke="{INK_WARM}" stroke-width="1.6"/>')
        # Two drawers with brass knobs
        for dy_off in (16, 76):
            m.append(f'<polygon points="{nx0+12},{ny0+24+dy_off} {nx0+124},{ny0+12+dy_off} {nx0+124},{ny0+60+dy_off} {nx0+12},{ny0+72+dy_off}" fill="#6F4428" stroke="{INK_WARM}" stroke-width="1.4"/>')
            m.append(f'<circle cx="{nx0+68}" cy="{ny0+42+dy_off}" r="4.8" fill="#D9A34E" stroke="{INK_WARM}" stroke-width="1.2"/>')
            m.append(f'<circle cx="{nx0+66.5}" cy="{ny0+40.5+dy_off}" r="1.5" fill="#FFF3C4"/>')

        # Stacked books on nightstand
        m.append(f'<polygon points="{nx0+98},{ny0+2} {nx0+164},{ny0-4} {nx0+170},{ny0+6} {nx0+104},{ny0+12}" fill="#324B61" stroke="{INK_WARM}" stroke-width="1.3"/>')
        m.append(f'<polygon points="{nx0+102},{ny0-7} {nx0+160},{ny0-12} {nx0+165},{ny0-3} {nx0+107},{ny0+2}" fill="#8B3B2E" stroke="{INK_WARM}" stroke-width="1.3"/>')

        # Warm bedside lamp (left side of nightstand)
        lx, ly = 486, 246
        m.append(f'<ellipse cx="{lx}" cy="{ly-64}" rx="74" ry="64" fill="url(#{p}_lamp_glow)"/>')
        # Brass base + stem
        m.append(f'<ellipse cx="{lx}" cy="{ly+2}" rx="22" ry="7.5" fill="#C48F44" stroke="{INK_WARM}" stroke-width="1.5"/>')
        m.append(f'<path d="M{lx-7},{ly} L{lx-4},{ly-38} L{lx+4},{ly-38} L{lx+7},{ly} Z" fill="#D49E4F" stroke="{INK_WARM}" stroke-width="1.4"/>')
        m.append(f'<path d="M{lx-2},{ly-4} L{lx-1},{ly-36}" fill="none" stroke="#FFF1C2" stroke-width="1.2" opacity="0.7"/>')
        # Fabric lampshade
        m.append(f'<polygon points="{lx-22},{ly-92} {lx+22},{ly-92} {lx+38},{ly-36} {lx-38},{ly-36}" fill="url(#{p}_lamp_shade)" stroke="{INK_WARM}" stroke-width="1.7" stroke-linejoin="round"/>')
        # Subtle fabric ribbing on lampshade
        for rx_l in (-22, -11, 0, 11, 22):
            m.append(f'<path d="M{lx+rx_l*0.6:.1f},{ly-90} L{lx+rx_l:.1f},{ly-38}" fill="none" stroke="#B7722B" stroke-width="0.8" opacity="0.45"/>')
        # Warm bulb glow rim under shade
        m.append(f'<ellipse cx="{lx}" cy="{ly-36}" rx="34" ry="5.5" fill="#FFF4CC" opacity="0.78"/>')

        # Vintage twin-bell alarm clock (center-right of nightstand)
        cx_clk, cy_clk = 556, 232
        # Feet
        m.append(f'<path d="M{cx_clk-11},{cy_clk+14} L{cx_clk-15},{cy_clk+20} M{cx_clk+11},{cy_clk+14} L{cx_clk+15},{cy_clk+20}" fill="none" stroke="{INK_WARM}" stroke-width="2.4" stroke-linecap="round"/>')
        # Twin brass bells
        m.append(f'<circle cx="{cx_clk-12}" cy="{cy_clk-14}" r="7.5" fill="#C99649" stroke="{INK_WARM}" stroke-width="1.4"/>')
        m.append(f'<circle cx="{cx_clk+12}" cy="{cy_clk-14}" r="7.5" fill="#C99649" stroke="{INK_WARM}" stroke-width="1.4"/>')
        m.append(f'<path d="M{cx_clk},{cy_clk-16} L{cx_clk},{cy_clk-22}" fill="none" stroke="{INK_WARM}" stroke-width="2.0"/>')
        # Clock casing & cream dial
        m.append(f'<circle cx="{cx_clk}" cy="{cy_clk}" r="16.5" fill="#4E5B5E" stroke="{INK_WARM}" stroke-width="1.8"/>')
        m.append(f'<circle cx="{cx_clk}" cy="{cy_clk}" r="12.8" fill="#FAF2DE" stroke="#363B3D" stroke-width="1.0"/>')
        # Hour ticks & hands (07:15)
        for ang in range(0, 360, 30):
            rad = math.radians(ang)
            m.append(f'<path d="M{cx_clk+9.5*math.cos(rad):.1f},{cy_clk+9.5*math.sin(rad):.1f} L{cx_clk+11.5*math.cos(rad):.1f},{cy_clk+11.5*math.sin(rad):.1f}" fill="none" stroke="#2A2420" stroke-width="0.9"/>')
        m.append(f'<path d="M{cx_clk},{cy_clk} L{cx_clk-6.5},{cy_clk+4.5}" fill="none" stroke="#1E1A18" stroke-width="1.9" stroke-linecap="round"/>')
        m.append(f'<path d="M{cx_clk},{cy_clk} L{cx_clk+9.2},{cy_clk}" fill="none" stroke="#1E1A18" stroke-width="1.4" stroke-linecap="round"/>')
        m.append(f'<circle cx="{cx_clk}" cy="{cy_clk}" r="1.8" fill="#B5382B"/>')
        m.append('</g>')
        parts.append("".join(m))

    # --- LAYER 3: SAHNE (Wrinkled cotton sheets, pillow, quilted blanket, locked Turna v4) ---
    if _katman_aktif(katmanlar, "sahne"):
        s: list[str] = ['<g id="s105-sahne">']
        # Bed mattress & sheet plane sweeping from left headboard to bottom-right foreground
        s.append(f'<polygon points="0,336 392,292 960,368 960,540 0,540" fill="url(#{p}_sheet_base)" stroke="{INK_WARM}" stroke-width="2.0"/>')

        # Fluffy pillow propped against headboard (left-mid)
        s.append(
            f'<path d="M46,274 Q165,244 294,264 Q340,278 334,324 Q282,354 170,358 Q74,356 32,326 Q24,296 46,274 Z" '
            f'fill="url(#{p}_pillow)" stroke="{INK_WARM}" stroke-width="1.9" stroke-linejoin="round"/>'
        )
        # Pillow folds, seam piping & warm indentation shadow
        s.append('<path d="M62,314 Q162,336 278,322 Q314,316 326,304" fill="none" stroke="#B79E82" stroke-width="2.2" opacity="0.65"/>')
        s.append('<path d="M92,286 Q178,298 256,288" fill="none" stroke="#C5AD91" stroke-width="1.6" opacity="0.55"/>')
        s.append('<path d="M120,264 Q212,256 286,272" fill="none" stroke="#FFFDF5" stroke-width="2.0" opacity="0.72"/>')

        # Rich organic cotton sheet wrinkles (multiple shaded & lit fabric ridges)
        wrinkle_shadows = [
            "M180,366 Q340,342 520,378 Q660,404 820,388 L820,406 Q645,422 500,394 Q332,360 180,384 Z",
            "M280,420 Q445,392 618,434 Q748,464 930,444 L930,468 Q736,486 596,452 Q435,414 280,442 Z",
            "M410,322 Q536,306 672,336 Q786,358 910,350 L910,364 Q778,370 658,348 Q530,320 410,336 Z",
            "M330,478 Q510,456 694,496 Q816,522 958,504 L958,528 Q806,540 676,514 Q502,478 330,498 Z",
        ]
        for wpath in wrinkle_shadows:
            s.append(f'<path d="{wpath}" fill="#C7AC8A" opacity="0.46"/>')
        # Crisp sunlit fabric crease highlights
        wrinkle_hl = [
            "M204,362 Q350,338 524,372 Q666,398 830,382",
            "M296,416 Q452,388 622,428 Q752,458 936,438",
            "M422,318 Q544,302 680,330 Q790,352 918,344",
            "M352,472 Q522,450 700,490 Q820,516 956,498",
        ]
        for hpath in wrinkle_hl:
            s.append(f'<path d="{hpath}" fill="none" stroke="#FFFDF4" stroke-width="2.0" opacity="0.72" stroke-linecap="round"/>')
        # Subtle cotton weave cross-hatching in sunlit zone
        for wy in range(326, 520, 14):
            s.append(f'<path d="M260,{wy} Q540,{wy-8} 940,{wy+12}" fill="none" stroke="#9D8365" stroke-width="0.55" opacity="0.22"/>')

        # Folded quilted blanket bundled on the left-bottom corner
        s.append(
            f'<path d="M0,342 Q128,334 246,374 Q326,404 358,468 Q372,504 352,540 L0,540 Z" '
            f'fill="url(#{p}_quilt)" stroke="{INK_WARM}" stroke-width="2.1" stroke-linejoin="round"/>'
        )
        # Folded top cuff of blanket (warm terracotta lining)
        s.append(
            f'<path d="M0,342 Q126,332 246,374 Q264,394 242,414 Q134,376 0,386 Z" '
            f'fill="#9A4E38" stroke="{INK_WARM}" stroke-width="1.7" stroke-linejoin="round"/>'
        )
        # Diamond quilted stitching lines on blanket
        for qx in range(-60, 340, 38):
            s.append(f'<path d="M{qx},386 L{qx+140},540" fill="none" stroke="#1E2D3D" stroke-width="1.0" opacity="0.55"/>')
            s.append(f'<path d="M{qx+140},386 L{qx},540" fill="none" stroke="#7594B3" stroke-width="0.9" opacity="0.38"/>')
        # Blanket sunlit rim fold
        s.append('<path d="M10,346 Q126,338 240,376" fill="none" stroke="#F4C58C" stroke-width="2.0" opacity="0.72"/>')

        # Venetian blind golden sunlight bands draped across the wrinkled bedsheets
        for sb in range(5):
            sy0 = 318 + sb * 46
            s.append(
                f'<polygon points="960,{sy0-44} 960,{sy0-20} 290,{sy0+66} 290,{sy0+42}" '
                f'fill="#FFE9A3" opacity="0.24"/>'
            )

        # === LOCKED TURNA V4 AS A JEWEL IN THE CENTER OF THE SUNBEAM ===
        # Warm halo + soft radial fabric depression folds & cast shadow on crumpled cotton sheet
        crane_x, crane_y = 548, 378
        s.append(f'<ellipse cx="{crane_x}" cy="{crane_y+6}" rx="164" ry="90" fill="url(#{p}_crane_halo)"/>')
        s.append(
            f'<path d="M{crane_x-96},{crane_y+42} Q{crane_x-30},{crane_y+56} {crane_x+38},{crane_y+62} '
            f'M{crane_x-70},{crane_y+72} Q{crane_x+12},{crane_y+64} {crane_x+108},{crane_y+48}" '
            f'fill="none" stroke="#B69872" stroke-width="1.6" opacity="0.52"/>'
        )
        s.append(
            f'<path d="M{crane_x-88},{crane_y+38} Q{crane_x-22},{crane_y+50} {crane_x+42},{crane_y+56}" '
            f'fill="none" stroke="#FFFDF4" stroke-width="1.4" opacity="0.72"/>'
        )
        s.append(f'<ellipse cx="{crane_x-18}" cy="{crane_y+58}" rx="86" ry="18" fill="#5A3E24" opacity="0.34"/>')
        s.append(f'<ellipse cx="{crane_x-10}" cy="{crane_y+54}" rx="54" ry="10" fill="#3D2614" opacity="0.38"/>')
        # Locked K.turna(1.0, isik=0.8) placed in exact spotlight
        s.append(
            f'<g transform="translate({crane_x},{crane_y}) rotate(-4)">'
            f'{K.turna(1.0, isik=0.8, kanat=0.08, kagit="#FFF8EB", golge=False)}'
            f'</g>'
        )
        # Subtle jewel-like specular sparkle on crane wing crest
        s.append(
            f'<g transform="translate({crane_x+4},{crane_y-16})" filter="url(#{p}_glow_soft)">'
            f'<path d="M-12,0 L12,0 M0,-12 L0,12 M-6,-6 L6,6 M-6,6 L6,-6" fill="none" stroke="#FFFDF2" stroke-width="1.4" opacity="0.88"/>'
            f'<circle cx="0" cy="0" r="2.6" fill="#FFFFFF"/>'
            f'</g>'
        )
        s.append('</g>')
        parts.append("".join(s))

    # --- LAYER 4: PLAN (Subtle Style B+A cyan geometric echo & English caption) ---
    if _katman_aktif(katmanlar, "plan"):
        pl: list[str] = ['<g id="s105-plan" opacity="0.88">']
        # Whisper-thin cyan origami fold ratio arc around crane
        pl.append(
            f'<path d="M432,374 A122,74 0 0,1 668,362" fill="none" stroke="{PLAN}" '
            f'stroke-width="1.2" stroke-dasharray="5 4" opacity="0.65"/>'
        )
        pl.append(
            f'<path d="M548,302 L548,266 L662,266" fill="none" stroke="{PLAN}" stroke-width="1.2" opacity="0.82"/>'
        )
        pl.append(f'<circle cx="548" cy="302" r="3.2" fill="{PLAN_CORE}" stroke="{PLAN}" stroke-width="1.2"/>')
        pl.append(f'<rect x="664" y="255" width="154" height="20" rx="3" fill="#141C24" opacity="0.72" stroke="{PLAN}" stroke-width="0.9"/>')
        pl.append(
            f'<text x="673" y="269" font-family="DejaVu Sans Mono, Consolas, monospace" '
            f'font-size="10.5" font-weight="bold" fill="{PLAN_CORE}" letter-spacing="1.0">I\'M HERE · CRANE 01</text>'
        )
        pl.append('</g>')
        parts.append("".join(pl))

    # --- LAYER 5: ONPLAN (Diagonal golden sunbeams, floating dust motes, warm vignette) ---
    if _katman_aktif(katmanlar, "onplan"):
        op: list[str] = ['<g id="s105-onplan">']
        # Volumetric diagonal golden sunbeams pouring from window toward crane
        beams = [
            "646,38 920,18 690,540 310,540",
            "660,112 920,96 810,540 430,540",
            "642,190 920,174 960,490 540,540",
        ]
        for bpts in beams:
            op.append(f'<polygon points="{bpts}" fill="url(#{p}_beam)"/>')

        # Floating illuminated dust motes in the sunbeams
        for _ in range(62):
            dx = rng.uniform(330, 910)
            dy = rng.uniform(52, 490)
            # Keep motes mostly inside the diagonal light cone
            if dy < (920 - dx) * 0.42 - 40:
                continue
            r = rng.uniform(1.0, 3.1)
            al = rng.uniform(0.28, 0.85)
            col = rng.choice(["#FFFBE2", "#FFE9A8", "#FFF3C4"])
            op.append(f'<circle cx="{dx:.1f}" cy="{dy:.1f}" r="{r:.1f}" fill="{col}" opacity="{al:.2f}"/>')

        # Subtle warm cinematic vignette
        op.append(f'<rect x="0" y="0" width="960" height="540" fill="url(#{p}_vignette)"/>')
        op.append('</g>')
        parts.append("".join(op))

    return defs, "".join(parts)


# =============================================================================
# 1.06 · HIGH SCHOOL CRAFT DESK ("HIGH SCHOOL")
# =============================================================================
def set_106_lise_origami(katmanlar: set[str] | list[str] | None = None) -> tuple[str, str]:
    """1990s High School art & drafting classroom: chalk-drawn blackboard, tall sunlit
    classroom windows, lockers/cabinets, wood-grained scratched student desk with metal
    ruler, scissors, pencil, open origami diagram (FOLD 01 -> 02 -> 03), square papers,
    and 5 locked Turna v4 cranes soaring in sequence toward the sunbeam."""
    rng = random.Random(106)
    p = _uid("s106")

    defs = f"""
    <linearGradient id="{p}_wall" x1="0" y1="0" x2="1" y2="0.4">
      <stop offset="0%" stop-color="#27323A"/>
      <stop offset="48%" stop-color="#3E4C54"/>
      <stop offset="82%" stop-color="#6B6D62"/>
      <stop offset="100%" stop-color="#A89A78"/>
    </linearGradient>
    <linearGradient id="{p}_board" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#192B24"/>
      <stop offset="55%" stop-color="#21382F"/>
      <stop offset="100%" stop-color="#1A2C25"/>
    </linearGradient>
    <linearGradient id="{p}_win_out" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#FFFBE6"/>
      <stop offset="52%" stop-color="#FFE6A8"/>
      <stop offset="100%" stop-color="#D8BA85"/>
    </linearGradient>
    <linearGradient id="{p}_desk_wood" x1="0" y1="0" x2="1" y2="0.6">
      <stop offset="0%" stop-color="#5B3B24"/>
      <stop offset="35%" stop-color="#7D5232"/>
      <stop offset="72%" stop-color="#A36E44"/>
      <stop offset="100%" stop-color="#C9915E"/>
    </linearGradient>
    <linearGradient id="{p}_desk_edge" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#3B2516"/>
      <stop offset="60%" stop-color="#5A3922"/>
      <stop offset="100%" stop-color="#764C2E"/>
    </linearGradient>
    <linearGradient id="{p}_steel" x1="0" y1="0" x2="1" y2="0.3">
      <stop offset="0%" stop-color="#8B96A1"/>
      <stop offset="42%" stop-color="#DCE4EC"/>
      <stop offset="65%" stop-color="#A5B1BC"/>
      <stop offset="100%" stop-color="#E7EEF5"/>
    </linearGradient>
    <linearGradient id="{p}_sunbeam" x1="1" y1="0" x2="0.1" y2="1">
      <stop offset="0%" stop-color="#FFF9DC" stop-opacity="0.52"/>
      <stop offset="48%" stop-color="#FFE5A0" stop-opacity="0.24"/>
      <stop offset="100%" stop-color="#E8B866" stop-opacity="0.0"/>
    </linearGradient>
    <radialGradient id="{p}_vignette" cx="0.52" cy="0.5" r="0.68">
      <stop offset="56%" stop-color="#000000" stop-opacity="0.0"/>
      <stop offset="100%" stop-color="#0F1418" stop-opacity="0.58"/>
    </radialGradient>
    <filter id="{p}_glow_sun" x="-25%" y="-25%" width="150%" height="150%">
      <feGaussianBlur stdDeviation="4.5" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    """

    parts: list[str] = []

    # --- LAYER 1: UZAK (Chalkboard, tall classroom windows, art lockers, room sign) ---
    if _katman_aktif(katmanlar, "uzak"):
        u: list[str] = ['<g id="s106-uzak">']
        u.append(f'<rect x="0" y="0" width="960" height="540" fill="url(#{p}_wall)"/>')
        # Subtle cinderblock classroom wall grid
        for by in range(28, 340, 28):
            u.append(f'<path d="M0,{by} L640,{by}" fill="none" stroke="#1E272E" stroke-width="0.7" opacity="0.28"/>')
        # Classroom room plaque above board
        u.append(f'<rect x="28" y="18" width="218" height="22" rx="2" fill="#232D34" stroke="{INK}" stroke-width="1.3"/>')
        u.append('<text x="38" y="33" font-family="DejaVu Sans, Arial, sans-serif" font-size="10.5" font-weight="bold" fill="#DCE5EC" letter-spacing="0.9">ART &amp; DRAFTING · ROOM 204</text>')

        # Chalkboard with wooden frame (left-center background)
        bx, by, bw, bh = 28, 52, 412, 198
        u.append(f'<rect x="{bx-8}" y="{by-8}" width="{bw+16}" height="{bh+16}" rx="2" fill="#634229" stroke="{INK}" stroke-width="1.8"/>')
        u.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" fill="url(#{p}_board)" stroke="#131F1B" stroke-width="1.4"/>')
        # Chalk dust smudges
        u.append('<ellipse cx="145" cy="146" rx="86" ry="42" fill="#D4E3DC" opacity="0.06"/>')
        u.append('<ellipse cx="322" cy="138" rx="92" ry="52" fill="#D4E3DC" opacity="0.07"/>')
        # Chalk drawings & English annotations on blackboard
        u.append('<text x="46" y="78" font-family="DejaVu Sans Mono, monospace" font-size="11.5" font-weight="bold" fill="#DCECE4" opacity="0.85">GEOMETRY &amp; FOLDS</text>')
        u.append('<path d="M46,84 L182,84" fill="none" stroke="#DCECE4" stroke-width="1.0" opacity="0.6"/>')
        # Geometric origami crease square diagram on chalkboard
        u.append('<rect x="52" y="102" width="76" height="76" fill="none" stroke="#DCECE4" stroke-width="1.3" opacity="0.78"/>')
        u.append('<path d="M52,102 L128,178 M128,102 L52,178 M90,102 L90,178 M52,140 L128,140" fill="none" stroke="#DCECE4" stroke-width="0.9" stroke-dasharray="4 3" opacity="0.65"/>')
        u.append('<text x="138" y="124" font-family="DejaVu Sans Mono, monospace" font-size="9.5" fill="#CFE2D8" opacity="0.78">45° AXIS</text>')
        u.append('<text x="138" y="142" font-family="DejaVu Sans Mono, monospace" font-size="9.5" fill="#CFE2D8" opacity="0.72">SYMMETRY</text>')
        # Isometric truss / bridge sketch on right half of chalkboard
        u.append('<path d="M236,164 L274,112 L312,164 L350,112 L388,164 Z" fill="none" stroke="#DCECE4" stroke-width="1.2" opacity="0.75"/>')
        u.append('<path d="M274,112 L350,112 M274,112 L274,164 M312,112 L312,164 M350,112 L350,164" fill="none" stroke="#DCECE4" stroke-width="0.9" opacity="0.58"/>')
        u.append('<text x="242" y="96" font-family="DejaVu Sans Mono, monospace" font-size="9.5" fill="#CFE2D8" opacity="0.72">LOAD PATH · HIGH SCHOOL</text>')
        # Chalk tray with chalk sticks & felt eraser
        u.append(f'<rect x="{bx-10}" y="{by+bh+4}" width="{bw+20}" height="12" fill="#7D5434" stroke="{INK}" stroke-width="1.5"/>')
        u.append(f'<rect x="78" y="{by+bh-1}" width="32" height="7" rx="1" fill="#2A2624" stroke="{INK}" stroke-width="1.0"/>')
        u.append(f'<rect x="132" y="{by+bh+1}" width="22" height="4" rx="1" fill="#F2EFE6"/>')
        u.append(f'<rect x="162" y="{by+bh+1}" width="16" height="4" rx="1" fill="#F5DF98"/>')

        # Metal classroom supply lockers between chalkboard & windows (x=462..588)
        for li in range(3):
            lx = 466 + li * 40
            u.append(f'<rect x="{lx}" y="68" width="38" height="238" fill="#465864" stroke="{INK}" stroke-width="1.5"/>')
            u.append(f'<rect x="{lx+4}" y="74" width="30" height="226" fill="#526673" stroke="#303E47" stroke-width="0.9"/>')
            # Locker vents
            for vy in (86, 93, 100, 107):
                u.append(f'<path d="M{lx+10},{vy} L{lx+28},{vy}" fill="none" stroke="#222D34" stroke-width="1.5"/>')
            # Handle
            u.append(f'<rect x="{lx+26}" y="168" width="4" height="18" rx="1" fill="#A9B7C2" stroke="{INK}" stroke-width="0.8"/>')

        # Wall clock above lockers
        u.append(f'<circle cx="525" cy="34" r="18" fill="#293238" stroke="{INK}" stroke-width="1.6"/>')
        u.append('<circle cx="525" cy="34" r="14.5" fill="#F4EFE2"/>')
        u.append('<path d="M525,34 L532,27 M525,34 L525,22" fill="none" stroke="#1E1C1A" stroke-width="1.6" stroke-linecap="round"/>')

        # Tall sunlit classroom windows on right wall (x=616..950)
        for wi in range(2):
            wx = 620 + wi * 166
            u.append(f'<rect x="{wx-8}" y="12" width="158" height="278" fill="#FFF3C8" opacity="0.22" filter="url(#{p}_glow_sun)"/>')
            u.append(f'<rect x="{wx}" y="18" width="144" height="266" fill="url(#{p}_win_out)" stroke="#3D464C" stroke-width="4"/>')
            # Distant trees / campus building outside
            u.append(f'<path d="M{wx},228 Q{wx+44},182 {wx+92},208 Q{wx+124},190 {wx+144},214 L{wx+144},284 L{wx},284 Z" fill="#A39972" opacity="0.48"/>')
            # Window mullions (3x2 grid)
            u.append(f'<path d="M{wx+72},18 L{wx+72},284 M{wx},106 L{wx+144},106 M{wx},194 L{wx+144},194" fill="none" stroke="#4D575E" stroke-width="3.2"/>')
            u.append(f'<path d="M{wx+74},18 L{wx+74},284" fill="none" stroke="#FFFBE4" stroke-width="1.0" opacity="0.65"/>')
        # Window sill
        u.append(f'<rect x="606" y="284" width="354" height="14" fill="#6F5138" stroke="{INK}" stroke-width="1.6"/>')
        u.append('</g>')
        parts.append("".join(u))

    # --- LAYER 2: ORTA (Background student desks, pinboard, classroom floor) ---
    if _katman_aktif(katmanlar, "orta"):
        m: list[str] = ['<g id="s106-orta">']
        # Classroom linoleum floor visible between back wall and foreground desk
        m.append('<rect x="0" y="298" width="960" height="84" fill="#3A3D3B"/>')
        # Distant classroom desks & stools (depth cues)
        for dx_bg in (56, 254, 456):
            m.append(f'<rect x="{dx_bg}" y="302" width="136" height="12" rx="1" fill="#6B4A31" stroke="{INK}" stroke-width="1.4"/>')
            m.append(f'<path d="M{dx_bg+14},314 L{dx_bg+10},368 M{dx_bg+122},314 L{dx_bg+126},368" fill="none" stroke="#262D33" stroke-width="3.2"/>')
            # Stool
            m.append(f'<ellipse cx="{dx_bg+68}" cy="336" rx="22" ry="6" fill="#593F2A" stroke="{INK}" stroke-width="1.3"/>')
            m.append(f'<path d="M{dx_bg+56},341 L{dx_bg+52},374 M{dx_bg+80},341 L{dx_bg+84},374" fill="none" stroke="#22282E" stroke-width="2.6"/>')
        # Paper rolls cup on window sill
        m.append(f'<rect x="646" y="256" width="22" height="28" rx="2" fill="#7D5C3E" stroke="{INK}" stroke-width="1.3"/>')
        m.append(f'<polygon points="649,256 654,234 660,234 657,256" fill="#F2EAD7" stroke="{INK}" stroke-width="1.0"/>')
        m.append(f'<polygon points="658,256 664,238 669,240 665,256" fill="#DCE9F2" stroke="{INK}" stroke-width="1.0"/>')
        m.append('</g>')
        parts.append("".join(m))

    # --- LAYER 3: SAHNE (Detailed wood-grained desk, diagram, tools, 5 soaring Turna v4) ---
    if _katman_aktif(katmanlar, "sahne"):
        s: list[str] = ['<g id="s106-sahne">']
        # Perspective wooden craft desk filling foreground (y=342..540)
        s.append(f'<polygon points="0,368 122,334 960,348 960,540 0,540" fill="url(#{p}_desk_wood)" stroke="{INK}" stroke-width="2.2"/>')
        # Front beveled desk lip
        s.append(f'<rect x="0" y="518" width="960" height="22" fill="url(#{p}_desk_edge)" stroke="{INK}" stroke-width="1.8"/>')
        s.append('<path d="M0,518 L960,518" fill="none" stroke="#E4B37E" stroke-width="1.4" opacity="0.65"/>')

        # Plank seams, organic wood grain, knots & old student desk scratches (NO flat brown box!)
        for py_seam in (384, 434, 482):
            s.append(f'<path d="M0,{py_seam+8} L960,{py_seam-4}" fill="none" stroke="#3F2717" stroke-width="1.4" opacity="0.65"/>')
            s.append(f'<path d="M0,{py_seam+9.5} L960,{py_seam-2.5}" fill="none" stroke="#D5A06C" stroke-width="0.7" opacity="0.35"/>')
        for _ in range(28):
            gy = rng.uniform(346, 512)
            gx0 = rng.uniform(0, 260)
            gx1 = rng.uniform(520, 960)
            amp = rng.uniform(-7, 7)
            s.append(
                f'<path d="M{gx0:.1f},{gy:.1f} Q{(gx0+gx1)*0.5:.1f},{gy+amp:.1f} {gx1:.1f},{gy-2:.1f}" '
                f'fill="none" stroke="#4D2E1B" stroke-width="{rng.uniform(0.6,1.3):.1f}" opacity="{rng.uniform(0.24,0.48):.2f}"/>'
            )
        # Wood knots
        for kx, ky in [(142, 408), (748, 456), (862, 396)]:
            s.append(f'<ellipse cx="{kx}" cy="{ky}" rx="12" ry="4.5" fill="none" stroke="#452A18" stroke-width="1.1" opacity="0.58"/>')
            s.append(f'<ellipse cx="{kx}" cy="{ky}" rx="4.5" ry="1.8" fill="#3B2314" opacity="0.55"/>')
        # Subtle compass/knife scratches on desk surface
        s.append('<path d="M62,462 L114,474 M74,476 L108,456 M812,488 L854,496" fill="none" stroke="#E0B484" stroke-width="0.8" opacity="0.38"/>')

        # Sunlight reflection pool on right side of desk
        s.append('<polygon points="480,342 960,348 960,518 396,518" fill="#FFE6A3" opacity="0.16"/>')

        # --- DESK PROP 1: Open Origami Folding Diagram Sheet (left-center) ---
        s.append(
            f'<g transform="translate(278,434) rotate(-5)">'
            # Drop shadow
            f'<polygon points="-132,-62 138,-56 146,66 -124,72" fill="#2A180D" opacity="0.35"/>'
            # Cream drafting sheet with slightly curled bottom-right corner
            f'<path d="M-136,-66 L134,-60 L140,46 L122,64 L-128,68 Z" fill="#F6EEDB" stroke="{INK}" stroke-width="1.6"/>'
            f'<polygon points="140,46 122,64 120,46" fill="#D9CCB0" stroke="{INK}" stroke-width="1.1"/>'
            # Diagram header
            f'<text x="-120" y="-44" font-family="DejaVu Sans Mono, monospace" font-size="10.5" font-weight="bold" fill="#253545">FOLD 01 → 02 → 03</text>'
            f'<text x="34" y="-44" font-family="DejaVu Sans Mono, monospace" font-size="8.5" fill="#5A6A78">CRANE STUDY</text>'
            f'<path d="M-120,-38 L120,-35" fill="none" stroke="#7A8A96" stroke-width="0.9"/>'
            # Step 01: Square with diagonal fold lines
            f'<rect x="-116" y="-26" width="54" height="54" fill="#FFFDF6" stroke="#364A5C" stroke-width="1.2"/>'
            f'<path d="M-116,-26 L-62,28 M-62,-26 L-116,28" fill="none" stroke="#2D7B9E" stroke-width="1.0" stroke-dasharray="3 2"/>'
            f'<text x="-100" y="42" font-family="DejaVu Sans Mono, monospace" font-size="8" fill="#3A4A58">01 BASE</text>'
            # Arrow 1->2
            f'<path d="M-54,1 L-36,1 M-41,-3 L-36,1 L-41,5" fill="none" stroke="#364A5C" stroke-width="1.2"/>'
            # Step 02: Diamond kite fold
            f'<polygon points="-2, -26 24,2 -2,30 -28,2" fill="#EFE7D2" stroke="#364A5C" stroke-width="1.2"/>'
            f'<path d="M-2,-26 L-2,30 M-28,2 L24,2" fill="none" stroke="#2D7B9E" stroke-width="1.0" stroke-dasharray="3 2"/>'
            f'<text x="-19" y="42" font-family="DejaVu Sans Mono, monospace" font-size="8" fill="#3A4A58">02 KITE</text>'
            # Arrow 2->3
            f'<path d="M32,1 L50,1 M45,-3 L50,1 L45,5" fill="none" stroke="#364A5C" stroke-width="1.2"/>'
            # Step 03: Wing lift silhouette
            f'<polygon points="62,14 86,-22 114,14 86,26" fill="#E3D9C1" stroke="#364A5C" stroke-width="1.2"/>'
            f'<path d="M86,-22 L86,26 M62,14 L114,14" fill="none" stroke="#2D7B9E" stroke-width="1.0" stroke-dasharray="3 2"/>'
            f'<path d="M74,-6 Q86,-20 98,-6" fill="none" stroke="#C94A38" stroke-width="1.1"/>'
            f'<text x="66" y="42" font-family="DejaVu Sans Mono, monospace" font-size="8" fill="#3A4A58">03 WINGS</text>'
            f'</g>'
        )

        # --- DESK PROP 2: Stacked & half-folded square origami papers (right-center) ---
        # Stack of colored squares
        s.append(f'<polygon points="502,438 594,432 606,496 510,504" fill="#2A180D" opacity="0.28"/>')
        s.append(f'<polygon points="498,434 588,428 600,492 506,498" fill="#C9DDEB" stroke="{INK}" stroke-width="1.4"/>')
        s.append(f'<polygon points="508,424 596,422 606,484 514,488" fill="#F8E7B9" stroke="{INK}" stroke-width="1.4"/>')
        s.append(f'<polygon points="518,414 606,416 614,476 522,476" fill="#FAF4E6" stroke="{INK}" stroke-width="1.5"/>')
        # Diagonal valley crease on top sheet
        s.append('<path d="M518,414 L614,476 M606,416 L522,476" fill="none" stroke="#B7A98E" stroke-width="1.0" stroke-dasharray="4 3"/>')
        # Half-folded triangular paper beside the stack
        s.append(f'<polygon points="640,452 722,436 692,494" fill="#FAF3E2" stroke="{INK}" stroke-width="1.5"/>')
        s.append(f'<polygon points="640,452 722,436 672,462" fill="#E4D7BE" stroke="{INK}" stroke-width="1.2"/>')

        # --- DESK PROP 3: Stainless Steel Ruler (front-center) ---
        s.append(
            f'<g transform="translate(468,496) rotate(-2.5)">'
            f'<rect x="-148" y="-10" width="296" height="24" rx="1.5" fill="#2A180D" opacity="0.32" transform="translate(3,4)"/>'
            f'<rect x="-148" y="-12" width="296" height="24" rx="1.5" fill="url(#{p}_steel)" stroke="{INK}" stroke-width="1.5"/>'
            f'<path d="M-146,-10 L146,-10" fill="none" stroke="#FFFFFF" stroke-width="1.0" opacity="0.78"/>'
        )
        # Ruler tick marks & numbers
        ticks: list[str] = []
        for ti in range(37):
            tx = -136 + ti * 7.5
            th = 9.0 if ti % 4 == 0 else (6.0 if ti % 2 == 0 else 3.5)
            ticks.append(f'<path d="M{tx:.1f},-12 L{tx:.1f},{-12+th:.1f}" fill="none" stroke="#222B33" stroke-width="0.9"/>')
            if ti % 4 == 0 and ti // 4 > 0 and ti // 4 <= 8:
                ticks.append(f'<text x="{tx-2.5:.1f}" y="6" font-family="DejaVu Sans Mono, monospace" font-size="7.5" font-weight="bold" fill="#222B33">{ti//4}</text>')
        ticks.append('<text x="118" y="6" font-family="DejaVu Sans Mono, monospace" font-size="7" fill="#222B33">IN</text></g>')
        s.append("".join(ticks))

        # --- DESK PROP 4: Metal Craft Scissors (left foreground) ---
        s.append(
            f'<g transform="translate(88,434) rotate(28)">'
            # Shadow
            f'<path d="M-42,-4 L54,-12 L52,-4 L-42,6 Z M-42,4 L54,14 L52,20 L-42,10 Z" fill="#24150C" opacity="0.32" transform="translate(3,5)"/>'
            # Steel blades
            f'<polygon points="-14,-2 62,-10 56,-1 -14,5" fill="#CFD8E0" stroke="{INK}" stroke-width="1.3"/>'
            f'<polygon points="-14,4 60,12 52,18 -14,10" fill="#A9B5C0" stroke="{INK}" stroke-width="1.3"/>'
            # Pivot screw
            f'<circle cx="4" cy="4" r="3.0" fill="#5D6973" stroke="{INK}" stroke-width="1.0"/>'
            # Dark ergonomic handle loops
            f'<ellipse cx="-32" cy="-7" rx="19" ry="10" fill="none" stroke="#22262B" stroke-width="5.2"/>'
            f'<ellipse cx="-32" cy="-7" rx="19" ry="10" fill="none" stroke="#4D555E" stroke-width="1.2"/>'
            f'<ellipse cx="-30" cy="14" rx="21" ry="11" fill="none" stroke="#22262B" stroke-width="5.2"/>'
            f'<ellipse cx="-30" cy="14" rx="21" ry="11" fill="none" stroke="#4D555E" stroke-width="1.2"/>'
            f'</g>'
        )

        # --- DESK PROP 5: Yellow #2 Pencil + Drafting Triangle (right foreground) ---
        s.append(
            f'<g transform="translate(776,472) rotate(-18)">'
            f'<rect x="-66" y="-4" width="124" height="9" fill="#26160C" opacity="0.30" transform="translate(3,4)"/>'
            # Yellow body
            f'<rect x="-66" y="-5" width="108" height="9" fill="#E8B93C" stroke="{INK}" stroke-width="1.3"/>'
            f'<path d="M-66,-2 L42,-2" fill="none" stroke="#FCE08B" stroke-width="1.4"/>'
            f'<path d="M-66,1.5 L42,1.5" fill="none" stroke="#B6871E" stroke-width="1.2"/>'
            # Metal ferrule + pink eraser
            f'<rect x="-78" y="-5" width="12" height="9" fill="#BFC7CE" stroke="{INK}" stroke-width="1.2"/>'
            f'<rect x="-88" y="-4.5" width="10" height="8" rx="2" fill="#D98383" stroke="{INK}" stroke-width="1.2"/>'
            # Sharpened wood tip + graphite
            f'<polygon points="42,-5 62,-0.5 42,4" fill="#E5C094" stroke="{INK}" stroke-width="1.2"/>'
            f'<polygon points="54,-2.2 62,-0.5 54,1.2" fill="#23262A"/>'
            f'</g>'
        )
        # Clear acrylic 30-60 drafting triangle (far right)
        s.append(
            f'<polygon points="818,376 934,432 824,442" fill="#D9F0F7" opacity="0.28" stroke="#89B4C4" stroke-width="1.4"/>'
            f'<polygon points="842,398 892,424 844,428" fill="#8C5D39" opacity="0.38" stroke="#89B4C4" stroke-width="1.0"/>'
        )

        # === 5 LOCKED TURNA V4 CRANES SOARING IN SEQUENCE TOWARD THE SUNBEAM ===
        # S-curve ascent from the desk surface (x=470, y=384) up toward sunlit right window (x=834, y=104)
        crane_specs = [
            # (x, y, scale, rot_deg, wing_flap, light, has_shadow)
            (462, 384, 0.48, -10, -0.15, 0.35, True),
            (558, 326, 0.52, -18, 0.42, 0.55, False),
            (652, 258, 0.58, -22, -0.10, 0.72, False),
            (748, 184, 0.54, -24, 0.58, 0.86, False),
            (844, 114, 0.44, -20, 0.18, 0.95, False),
        ]
        for cx_c, cy_c, sc_c, rot_c, wing_c, isik_c, sh_c in crane_specs:
            if sh_c:
                s.append(f'<ellipse cx="{cx_c+6}" cy="{cy_c+32}" rx="42" ry="9" fill="#3A2212" opacity="0.34"/>')
            s.append(
                f'<g transform="translate({cx_c},{cy_c}) rotate({rot_c})">'
                f'{K.turna(sc_c, isik=isik_c, kanat=wing_c, kagit="#FAF4E6", golge=False)}'
                f'</g>'
            )
        s.append('</g>')
        parts.append("".join(s))

    # --- LAYER 4: PLAN (Cyan flight trajectory arc & technical callouts) ---
    if _katman_aktif(katmanlar, "plan"):
        pl: list[str] = ['<g id="s106-plan" opacity="0.82">']
        # Sweeping cyan dashed trajectory linking all 5 cranes
        pl.append(
            f'<path d="M462,384 Q566,328 652,258 T856,104" fill="none" stroke="{PLAN}" '
            f'stroke-width="1.4" stroke-dasharray="6 4" opacity="0.72"/>'
        )
        for tx_p, ty_p in [(462, 384), (652, 258), (844, 114)]:
            pl.append(f'<circle cx="{tx_p}" cy="{ty_p}" r="3.4" fill="none" stroke="{PLAN}" stroke-width="1.2"/>')
        pl.append(f'<path d="M652,258 L652,216 L608,216" fill="none" stroke="{PLAN}" stroke-width="1.2" opacity="0.82"/>')
        pl.append(f'<rect x="434" y="205" width="174" height="20" rx="3" fill="#101A22" opacity="0.76" stroke="{PLAN}" stroke-width="0.9"/>')
        pl.append(
            f'<text x="444" y="219" font-family="DejaVu Sans Mono, monospace" font-size="10.2" '
            f'font-weight="bold" fill="{PLAN_CORE}" letter-spacing="0.9">HIGH SCHOOL · 5 CRANES</text>'
        )
        pl.append('</g>')
        parts.append("".join(pl))

    # --- LAYER 5: ONPLAN (Golden afternoon sunbeams from windows, chalk/paper dust motes, vignette) ---
    if _katman_aktif(katmanlar, "onplan"):
        op: list[str] = ['<g id="s106-onplan">']
        op.append(f'<polygon points="620,26 958,18 746,540 330,540" fill="url(#{p}_sunbeam)"/>')
        op.append(f'<polygon points="784,26 960,120 960,540 564,540" fill="url(#{p}_sunbeam)" opacity="0.75"/>')
        for _ in range(48):
            dx = rng.uniform(390, 945)
            dy = rng.uniform(36, 480)
            r = rng.uniform(0.9, 2.6)
            op.append(f'<circle cx="{dx:.1f}" cy="{dy:.1f}" r="{r:.1f}" fill="#FFF7D6" opacity="{rng.uniform(0.24,0.75):.2f}"/>')
        op.append(f'<rect x="0" y="0" width="960" height="540" fill="url(#{p}_vignette)"/>')
        op.append('</g>')
        parts.append("".join(op))

    return defs, "".join(parts)


# =============================================================================
# 1.07 · NIGHT DINER & $90,000 SACRIFICE ("AGE 18" / "$90,000")
# =============================================================================
def set_107_lokanta_cek(katmanlar: set[str] | list[str] | None = None) -> tuple[str, str]:
    """Night Chicago diner: burgundy leather booth, hanging warm amber glass pendant lamp,
    steaming coffee mugs, chrome napkin dispenser, ketchup bottle, open manila envelope &
    realistic $90,000 bank check (PAY TO MICHAEL SCOFIELD), locked Lincoln v1 on the left
    in a broad-shouldered jacket with warm protective gaze; outside the rain-streaked neon
    window, two trench-coated loan sharks waiting by a dark sedan's red taillights."""
    rng = random.Random(107)
    p = _uid("s107")

    defs = f"""
    <linearGradient id="{p}_night_sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#050912"/>
      <stop offset="55%" stop-color="#0C1524"/>
      <stop offset="100%" stop-color="#172130"/>
    </linearGradient>
    <radialGradient id="{p}_taillight_glow" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0%" stop-color="#FF3B3B" stop-opacity="0.95"/>
      <stop offset="35%" stop-color="#D91B24" stop-opacity="0.48"/>
      <stop offset="100%" stop-color="#7A0B12" stop-opacity="0.0"/>
    </radialGradient>
    <radialGradient id="{p}_neon_cyan" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0%" stop-color="#6EE8FF" stop-opacity="0.52"/>
      <stop offset="100%" stop-color="#1A6A82" stop-opacity="0.0"/>
    </radialGradient>
    <linearGradient id="{p}_booth_red" x1="0" y1="0" x2="1" y2="0.4">
      <stop offset="0%" stop-color="#3E1117"/>
      <stop offset="48%" stop-color="#6D1E28"/>
      <stop offset="85%" stop-color="#8A2835"/>
      <stop offset="100%" stop-color="#53171F"/>
    </linearGradient>
    <linearGradient id="{p}_table_top" x1="0.2" y1="0" x2="0.8" y2="1">
      <stop offset="0%" stop-color="#8F7D69"/>
      <stop offset="45%" stop-color="#C9B79D"/>
      <stop offset="82%" stop-color="#E5D5B8"/>
      <stop offset="100%" stop-color="#A89379"/>
    </linearGradient>
    <linearGradient id="{p}_jacket" x1="0" y1="0" x2="1" y2="0.3">
      <stop offset="0%" stop-color="#201A17"/>
      <stop offset="58%" stop-color="#372B24"/>
      <stop offset="92%" stop-color="#5A4232"/>
      <stop offset="100%" stop-color="#7A573B"/>
    </linearGradient>
    <linearGradient id="{p}_amber_lamp" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#B96523"/>
      <stop offset="45%" stop-color="#F2AE4B"/>
      <stop offset="82%" stop-color="#FFE39C"/>
      <stop offset="100%" stop-color="#FFF7DC"/>
    </linearGradient>
    <radialGradient id="{p}_lamp_cone" cx="0.5" cy="0.08" r="0.72">
      <stop offset="0%" stop-color="#FFE49E" stop-opacity="0.55"/>
      <stop offset="38%" stop-color="#F0A746" stop-opacity="0.22"/>
      <stop offset="100%" stop-color="#B5651D" stop-opacity="0.0"/>
    </radialGradient>
    <linearGradient id="{p}_check_bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#EAF2E5"/>
      <stop offset="55%" stop-color="#F4F8EC"/>
      <stop offset="100%" stop-color="#DCE7D5"/>
    </linearGradient>
    <radialGradient id="{p}_vignette" cx="0.5" cy="0.52" r="0.68">
      <stop offset="52%" stop-color="#000000" stop-opacity="0.0"/>
      <stop offset="100%" stop-color="#06080D" stop-opacity="0.70"/>
    </radialGradient>
    <filter id="{p}_glow_red" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="5.0" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="{p}_glow_amber" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="4.5" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    """

    parts: list[str] = []

    # --- LAYER 1: UZAK (Rainy Chicago night street outside diner window, sedan taillights, 2 loan sharks) ---
    if _katman_aktif(katmanlar, "uzak"):
        u: list[str] = ['<g id="s107-uzak">']
        # Night street sky + wet asphalt
        u.append(f'<rect x="0" y="0" width="960" height="540" fill="url(#{p}_night_sky)"/>')
        # Distant Chicago skyline buildings across the wet street
        bldgs = [
            (280, 48, 86, 178), (370, 72, 74, 154), (448, 36, 98, 190),
            (552, 66, 82, 160), (640, 28, 112, 198), (758, 58, 92, 168), (854, 42, 98, 184),
        ]
        for bx, by, bw, bh in bldgs:
            u.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" fill="#0D1522" stroke="#182538" stroke-width="1"/>')
            # Lit distant apartment windows
            for wy in range(by + 16, by + bh - 26, 22):
                for wx in range(bx + 10, bx + bw - 14, 18):
                    if rng.random() < 0.34:
                        col_w = rng.choice(["#E6B86A", "#9AC8E0", "#F2D28B"])
                        u.append(f'<rect x="{wx}" y="{wy}" width="8" height="11" fill="{col_w}" opacity="{rng.uniform(0.28,0.65):.2f}"/>')

        # Streetlamp glow & wet asphalt road (y=218..330)
        u.append('<rect x="260" y="218" width="690" height="122" fill="#0B111B"/>')
        u.append('<path d="M260,224 L950,224" fill="none" stroke="#243347" stroke-width="2"/>')

        # Exterior neon diner sign reflection in upper-right window
        u.append(f'<ellipse cx="838" cy="72" rx="88" ry="34" fill="url(#{p}_neon_cyan)"/>')
        u.append(f'<rect x="762" y="52" width="144" height="36" rx="5" fill="#0A1320" opacity="0.72" stroke="#FF4A5A" stroke-width="2.0" filter="url(#{p}_glow_red)"/>')
        u.append('<text x="774" y="75" font-family="DejaVu Sans, Arial, sans-serif" font-size="14" font-weight="bold" fill="#8CF0FF" letter-spacing="1.6">OPEN 24H</text>')

        # === DARK 1990s SEDAN WITH GLOWING RED TAILLIGHTS (x=548..886) ===
        # Red taillight ambient spill on wet asphalt
        u.append(f'<ellipse cx="642" cy="256" rx="110" ry="44" fill="url(#{p}_taillight_glow)"/>')
        u.append(f'<ellipse cx="776" cy="256" rx="100" ry="40" fill="url(#{p}_taillight_glow)"/>')
        # Sedan body (rear 3/4 view parked along curb)
        u.append(
            f'<path d="M566,248 L584,204 Q612,172 668,170 L772,172 Q824,174 848,206 L878,224 '
            f'L880,264 L562,266 Z" fill="#121822" stroke="#06090F" stroke-width="2.0" stroke-linejoin="round"/>'
        )
        # Rear windshield with cold rain reflection
        u.append('<polygon points="602,202 630,178 776,178 806,204" fill="#1E2C3E" stroke="#0A0F17" stroke-width="1.4"/>')
        u.append('<path d="M622,198 L652,182 M672,198 L704,182" fill="none" stroke="#5E85A8" stroke-width="1.3" opacity="0.45"/>')
        # Trunk deck & bumper
        u.append('<path d="M578,212 L848,214" fill="none" stroke="#3B4D66" stroke-width="1.4" opacity="0.6"/>')
        u.append('<rect x="560" y="248" width="320" height="14" rx="2" fill="#0B1018" stroke="#222E40" stroke-width="1.1"/>')
        # Wheels
        u.append('<ellipse cx="606" cy="268" rx="22" ry="15" fill="#06090E" stroke="#243040" stroke-width="1.5"/>')
        u.append('<ellipse cx="826" cy="268" rx="22" ry="15" fill="#06090E" stroke="#243040" stroke-width="1.5"/>')
        # Blazing red taillight bars
        u.append(f'<rect x="580" y="220" width="54" height="14" rx="2" fill="#FF2932" filter="url(#{p}_glow_red)"/>')
        u.append('<rect x="586" y="224" width="42" height="6" rx="1" fill="#FFD2C8"/>')
        u.append(f'<rect x="752" y="220" width="54" height="14" rx="2" fill="#FF2932" filter="url(#{p}_glow_red)"/>')
        u.append('<rect x="758" y="224" width="42" height="6" rx="1" fill="#FFD2C8"/>')
        # Wet asphalt red reflections underneath car
        for ry_r in range(282, 326, 9):
            u.append(f'<path d="M576,{ry_r} L650,{ry_r} M742,{ry_r+2} L814,{ry_r+2}" fill="none" stroke="#FF3038" stroke-width="2.4" opacity="{0.52 - (ry_r-282)*0.008:.2f}"/>')

        # === TWO TRENCH-COATED LOAN SHARKS STANDING BEFORE RED TAILLIGHTS ===
        # Loan Shark 1 (left, taller, sculpted trenchcoat shoulders, fedora brim, upturned collar)
        u.append(
            f'<g transform="translate(650,144)">'
            # Head & sculpted fedora silhouette
            f'<path d="M-12,18 Q-14,4 0,3 Q14,4 12,18 Q9,29 0,30 Q-9,29 -12,18 Z" fill="#0B0F17" stroke="#36141A" stroke-width="1.1"/>'
            f'<path d="M-24,11 Q0,4 24,11 L15,3 Q0,-5 -15,3 Z" fill="#070A10" stroke="#2A1218" stroke-width="0.9"/>'
            # Sculpted trenchcoat shoulders, upturned collar, draped lapels & pocket hand
            f'<path d="M-14,30 Q-28,34 -38,48 Q-44,96 -42,162 L40,162 Q42,96 34,48 Q26,34 14,30 Q0,38 -14,30 Z" '
            f'fill="#0B0F18" stroke="#1E141A" stroke-width="1.4" stroke-linejoin="round"/>'
            # Trenchcoat collar & lapel seam
            f'<path d="M-14,30 L-22,48 L-6,62 L0,52 L6,62 L22,48 L14,30" fill="none" stroke="#2B3444" stroke-width="1.4" opacity="0.72"/>'
            f'<path d="M0,52 L0,156" fill="none" stroke="#1E2634" stroke-width="1.3" opacity="0.65"/>'
            # Red taillight rim highlight on curved shoulder & coat edge
            f'<path d="M-36,48 Q-42,98 -41,158 M32,48 Q38,98 39,158" fill="none" stroke="#FF3A42" stroke-width="2.0" opacity="0.78"/>'
            # Cigarette ember & faint smoke wisp
            f'<circle cx="-18" cy="76" r="2.6" fill="#FF6B2B" filter="url(#{p}_glow_red)"/>'
            f'<path d="M-18,72 Q-22,60 -15,50" fill="none" stroke="#8FA8BE" stroke-width="1.0" opacity="0.38"/>'
            f'</g>'
        )
        # Loan Shark 2 (right, stockier, heavy wool overcoat, crossed arms, red rim light)
        u.append(
            f'<g transform="translate(726,154)">'
            f'<path d="M-12,16 Q-14,2 0,1 Q14,2 12,16 Q10,27 0,28 Q-10,27 -12,16 Z" fill="#0B0F17" stroke="#38141A" stroke-width="1.1"/>'
            # Broad sloped overcoat shoulders & tapered body
            f'<path d="M-16,28 Q-32,34 -40,48 Q-44,94 -38,152 L38,152 Q44,94 40,48 Q32,34 16,28 Q0,36 -16,28 Z" '
            f'fill="#0A0E16" stroke="#1E141A" stroke-width="1.4" stroke-linejoin="round"/>'
            # Coat collar & crossed arms silhouette
            f'<path d="M-15,29 L-20,44 L0,54 L20,44 L15,29" fill="none" stroke="#2B3444" stroke-width="1.3" opacity="0.68"/>'
            f'<path d="M-32,74 Q0,86 32,72 M-28,84 Q0,94 28,82" fill="none" stroke="#2D3848" stroke-width="2.0" opacity="0.7"/>'
            # Red taillight rim highlight
            f'<path d="M38,48 Q42,96 37,148 M-38,48 Q-42,96 -37,148" fill="none" stroke="#FF3A42" stroke-width="1.9" opacity="0.74"/>'
            f'</g>'
        )

        # Slanted falling rain streaks outside the window
        for _ in range(72):
            rx_r = rng.uniform(270, 945)
            ry_r = rng.uniform(22, 316)
            rlen = rng.uniform(14, 30)
            u.append(f'<path d="M{rx_r:.1f},{ry_r:.1f} L{rx_r-4.5:.1f},{ry_r+rlen:.1f}" fill="none" stroke="#9AC2DF" stroke-width="0.85" opacity="{rng.uniform(0.18,0.44):.2f}"/>')
        u.append('</g>')
        parts.append("".join(u))

    # --- LAYER 2: ORTA (Diner window frame, rain droplets on glass, burgundy booth, locked Lincoln v1) ---
    if _katman_aktif(katmanlar, "orta"):
        m: list[str] = ['<g id="s107-orta">']
        # Diner interior wall framing the big window (left solid wood wainscot + top valence)
        m.append(f'<rect x="0" y="0" width="268" height="540" fill="#211612"/>')
        m.append(f'<rect x="0" y="0" width="960" height="32" fill="#1C120E"/>')
        m.append(f'<rect x="938" y="0" width="22" height="540" fill="#1E1410"/>')
        # Warm wood paneling lines on left interior wall
        for px_w in range(22, 260, 38):
            m.append(f'<path d="M{px_w},32 L{px_w},350" fill="none" stroke="#36241B" stroke-width="1.3"/>')
        # Small vintage diner wall sconce on far left
        m.append(f'<ellipse cx="52" cy="116" rx="46" ry="38" fill="#F2AA49" opacity="0.22"/>')
        m.append(f'<polygon points="40,104 64,104 60,126 44,126" fill="#F5C36E" stroke="{INK_WARM}" stroke-width="1.4"/>')
        m.append(f'<rect x="49" y="126" width="6" height="12" fill="#8C6235" stroke="{INK_WARM}" stroke-width="1.1"/>')

        # Chrome & dark wood window frame + center vertical mullion
        m.append(f'<rect x="266" y="30" width="674" height="302" fill="none" stroke="#3B2A20" stroke-width="10"/>')
        m.append(f'<rect x="270" y="34" width="666" height="294" fill="none" stroke="#9AA5AE" stroke-width="2.2"/>')
        m.append(f'<rect x="536" y="34" width="8" height="294" fill="#3B2A20" stroke="{INK}" stroke-width="1.2"/>')
        m.append('<path d="M539,34 L539,328" fill="none" stroke="#A6B1BA" stroke-width="1.0" opacity="0.7"/>')

        # Glass rain droplets, vertical trickle trails & subtle interior amber reflection
        m.append('<polygon points="274,38 446,38 356,326 274,326" fill="#FFE0A3" opacity="0.06"/>')
        for _ in range(44):
            gx = rng.uniform(284, 926)
            gy = rng.uniform(44, 316)
            gr = rng.uniform(1.2, 3.2)
            m.append(f'<ellipse cx="{gx:.1f}" cy="{gy:.1f}" rx="{gr*0.75:.1f}" ry="{gr:.1f}" fill="#C8E4F8" opacity="{rng.uniform(0.28,0.68):.2f}"/>')
            if rng.random() < 0.35:
                m.append(f'<path d="M{gx:.1f},{gy:.1f} L{gx+rng.uniform(-1,1):.1f},{gy+rng.uniform(14,42):.1f}" fill="none" stroke="#A8CCE6" stroke-width="0.9" opacity="0.32"/>')

        # === BURGUNDY LEATHER BOOTH (left-side seat behind Lincoln + right booth back) ===
        # Left booth backrest (tufted vertical vinyl pleats)
        m.append(f'<rect x="8" y="198" width="186" height="248" rx="14" fill="url(#{p}_booth_red)" stroke="{INK_WARM}" stroke-width="2.2"/>')
        for bpx in (46, 86, 126, 162):
            m.append(f'<path d="M{bpx},204 L{bpx},424" fill="none" stroke="#2D0A10" stroke-width="2.2"/>')
            m.append(f'<path d="M{bpx+4},208 L{bpx+4},420" fill="none" stroke="#B54958" stroke-width="1.2" opacity="0.48"/>')
        # Top leather roll highlight
        m.append('<path d="M22,206 L180,206" fill="none" stroke="#D16B79" stroke-width="2.2" opacity="0.55" stroke-linecap="round"/>')
        # Opposite right-side booth edge peeking into right border
        m.append(f'<rect x="876" y="218" width="84" height="220" rx="12" fill="url(#{p}_booth_red)" stroke="{INK_WARM}" stroke-width="2.0"/>')
        m.append('<path d="M908,224 L908,424" fill="none" stroke="#2D0A10" stroke-width="2.0"/>')

        # === LOCKED LINCOLN V1 SEATED ON LEFT (R4-ANATOMY: ~2.35x head width, Collar-Over-Neck Z-Order) ===
        # Head at (216, 172) scale 0.68 -> head width ~94px; athletic shoulders ~218px (x=106..324)
        m.append(
            f'<g id="s107-lincoln">'
            # 1) BASE TORSO + CONTINUOUS ARMS (behind neck/head)
            # Far (right) arm descending continuously from right shoulder seam to table edge
            f'<path d="M276,256 L306,268 Q322,276 322,304 L318,376 L278,376 L274,306 Z" '
            f'fill="#3D2E25" stroke="{INK_WARM}" stroke-width="2.1" stroke-linejoin="round"/>'
            # Main athletic jacket torso (clean sloped shoulders, NO puffed dome)
            f'<path d="M126,262 L176,246 L252,248 L294,264 L290,384 L122,402 Z" '
            f'fill="url(#{p}_jacket)" stroke="{INK_WARM}" stroke-width="2.1" stroke-linejoin="round"/>'
            # Near (left) arm descending continuously from left shoulder seam down to table
            f'<path d="M134,260 L108,274 Q94,284 92,314 L88,412 L134,404 L138,318 Z" '
            f'fill="#2A211C" stroke="{INK_WARM}" stroke-width="2.1" stroke-linejoin="round"/>'
            # Clean tailored shoulder seam lines (matching al_lincoln_v1.png)
            f'<path d="M134,262 Q138,296 135,332" fill="none" stroke="{INK_WARM}" stroke-width="1.6" opacity="0.78"/>'
            f'<path d="M286,262 Q284,296 286,330" fill="none" stroke="{INK_WARM}" stroke-width="1.6" opacity="0.78"/>'
            # Warm amber rim highlight along right shoulder & sleeve
            f'<path d="M286,262 L308,271 Q320,280 319,324" fill="none" stroke="#F4B76A" stroke-width="2.2" opacity="0.70" stroke-linecap="round"/>'
            f'<path d="M104,278 Q94,294 93,332" fill="none" stroke="#C98D52" stroke-width="1.5" opacity="0.38" stroke-linecap="round"/>'
            # Inner collar backing cavity behind neck
            f'<path d="M174,244 L214,306 L252,246 Z" fill="#182028"/>'
            # 2) LOCKED LINCOLN V1 HEAD + NECK (middle Z-layer)
            f'<g transform="translate(216,172) scale(0.68)">'
            f'{K.lincoln_kafa(view="3q", ifade="koruyucu", look=0.32, boyun=True)}'
            f'</g>'
            # Subtle warm amber rim highlight on Lincoln's cheekbone/jaw
            f'<path d="M254,146 Q266,182 248,218" fill="none" stroke="#FFCE85" stroke-width="2.0" opacity="0.46" stroke-linecap="round"/>'
            # 3) COLLAR-OVER-NECK Z-ORDER (drawn OVER lower neck edge so neck seats cleanly inside collar!)
            # Inner white undershirt scoop + dark henley/crew neckline overlapping neck base (y=248..274)
            f'<path d="M180,248 Q214,274 246,250 L242,282 Q214,302 184,280 Z" '
            f'fill="#E8E3D8" stroke="{INK_WARM}" stroke-width="1.5" stroke-linejoin="round"/>'
            f'<path d="M180,256 Q214,284 246,258 L244,324 L214,344 L182,324 Z" '
            f'fill="#222B36" stroke="{INK_WARM}" stroke-width="1.6" stroke-linejoin="round"/>'
            # Left jacket collar & lapel wing overlapping left neck/trapezius edge
            f'<path d="M178,242 L154,282 L182,322 L212,334 L196,294 L182,254 Z" '
            f'fill="#46352B" stroke="{INK_WARM}" stroke-width="1.8" stroke-linejoin="round"/>'
            f'<path d="M162,282 L188,314" fill="none" stroke="#8C674B" stroke-width="0.9" stroke-dasharray="3 2" opacity="0.55"/>'
            # Right jacket collar & lapel wing overlapping right neck/trapezius edge
            f'<path d="M248,244 L274,282 L244,322 L214,334 L232,294 L244,256 Z" '
            f'fill="#5A4233" stroke="{INK_WARM}" stroke-width="1.8" stroke-linejoin="round"/>'
            f'<path d="M266,282 L238,314" fill="none" stroke="#A67D5B" stroke-width="0.9" stroke-dasharray="3 2" opacity="0.60"/>'
            # Center jacket front closure seam
            f'<path d="M213,334 L213,388" fill="none" stroke="{INK_WARM}" stroke-width="1.8"/>'
            # Jacket chest pocket & subtle fabric folds
            f'<path d="M146,322 L176,322 L176,348 L146,348 Z" fill="none" stroke="#221914" stroke-width="1.3" opacity="0.72"/>'
            f'<path d="M112,336 Q122,344 132,338 M290,328 Q302,336 314,332" fill="none" stroke="#1E1713" stroke-width="1.3" opacity="0.62"/>'
            f'</g>'
        )
        m.append('</g>')
        parts.append("".join(m))

    # --- LAYER 3: SAHNE (Diner Formica table, manila envelope, $90,000 check, steaming mugs, ketchup, napkin holder) ---
    if _katman_aktif(katmanlar, "sahne"):
        s: list[str] = ['<g id="s107-sahne">']
        # Perspective Formica diner table with chrome trim
        s.append(f'<polygon points="0,412 184,362 960,370 960,540 0,540" fill="url(#{p}_table_top)" stroke="{INK_WARM}" stroke-width="2.2"/>')
        # Subtle Formica boomerang/speckle texture
        for _ in range(32):
            fx = rng.uniform(40, 920)
            fy = rng.uniform(376, 528)
            s.append(f'<circle cx="{fx:.1f}" cy="{fy:.1f}" r="{rng.uniform(0.8,1.8):.1f}" fill="#7A6752" opacity="0.22"/>')
        # Warm overhead lamp pool directly illuminating the $90,000 check
        s.append('<ellipse cx="520" cy="444" rx="260" ry="72" fill="#FFF0C2" opacity="0.28"/>')

        # --- TABLE PROP 1: Open Manila Envelope (center-left, next to Lincoln's hand) ---
        s.append(
            f'<g transform="translate(364,458) rotate(-8)">'
            f'<polygon points="-86,-36 88,-32 94,42 -82,46" fill="#2A1B10" opacity="0.34" transform="translate(4,5)"/>'
            f'<polygon points="-86,-36 88,-32 94,42 -82,46" fill="#C99E65" stroke="{INK_WARM}" stroke-width="1.6"/>'
            # Open triangular flap on right
            f'<polygon points="88,-32 126,6 94,42" fill="#B68A52" stroke="{INK_WARM}" stroke-width="1.4"/>'
            f'<path d="M-76,-22 L72,-19" fill="none" stroke="#9B723F" stroke-width="1.0" opacity="0.65"/>'
            f'<text x="-66" y="10" font-family="DejaVu Sans, Arial, sans-serif" font-size="11" font-style="italic" font-weight="bold" fill="#4A331E" opacity="0.78">MICHAEL</text>'
            f'</g>'
        )

        # --- TABLE PROP 2: Realistic Bank Check ($90,000 · PAY TO MICHAEL SCOFIELD) ---
        s.append(
            f'<g transform="translate(556,458) rotate(3.2)">'
            # Cast shadow
            f'<rect x="-132" y="-50" width="268" height="104" rx="2" fill="#23160D" opacity="0.38" transform="translate(4,6)"/>'
            # Check paper base
            f'<rect x="-134" y="-52" width="268" height="104" rx="2" fill="url(#{p}_check_bg)" stroke="{INK_WARM}" stroke-width="1.7"/>'
            # Decorative security inner border
            f'<rect x="-126" y="-44" width="252" height="88" fill="none" stroke="#6E8C75" stroke-width="1.0" stroke-dasharray="2 1"/>'
            # Subtle guilloche horizontal watermark lines
            f'<path d="M-120,-18 L120,-18 M-120,6 L120,6 M-120,24 L120,24" fill="none" stroke="#9BB5A0" stroke-width="0.6" opacity="0.55"/>'
            # Bank header & Check Number
            f'<text x="-118" y="-30" font-family="DejaVu Sans, Arial, sans-serif" font-size="8.5" font-weight="bold" fill="#2E4A36" letter-spacing="0.8">CHICAGO TRUST BANK</text>'
            f'<text x="72" y="-30" font-family="DejaVu Sans Mono, monospace" font-size="8.5" fill="#445A4A">NO. 0418</text>'
            # PAY TO line
            f'<text x="-118" y="-12" font-family="DejaVu Sans, Arial, sans-serif" font-size="7.5" fill="#4F6856">PAY TO THE ORDER OF</text>'
            f'<text x="-118" y="3" font-family="DejaVu Sans, Arial, sans-serif" font-size="11.5" font-weight="bold" fill="#182433" letter-spacing="0.4">MICHAEL SCOFIELD</text>'
            f'<path d="M-118,6 L34,6" fill="none" stroke="#4D6654" stroke-width="0.9"/>'
            # Highlighted $90,000.00 amount box
            f'<rect x="44" y="-14" width="76" height="22" rx="1.5" fill="#FFFDF5" stroke="#2D4A36" stroke-width="1.3"/>'
            f'<text x="50" y="1.5" font-family="DejaVu Sans Mono, monospace" font-size="12.5" font-weight="bold" fill="#132218">$90,000</text>'
            # Written amount & signature
            f'<text x="-118" y="21" font-family="DejaVu Sans, Arial, sans-serif" font-size="8.2" font-weight="bold" fill="#25364A">NINETY THOUSAND DOLLARS</text>'
            f'<path d="M36,24 L118,24" fill="none" stroke="#4D6654" stroke-width="0.9"/>'
            # Signature scribble (Lincoln Burrows)
            f'<path d="M44,21 Q56,12 64,20 Q74,10 86,21 Q98,15 112,20" fill="none" stroke="#1E2C42" stroke-width="1.5" stroke-linecap="round"/>'
            # MICR routing numbers at bottom
            f'<text x="-114" y="38" font-family="DejaVu Sans Mono, monospace" font-size="8" fill="#3B4D42" letter-spacing="1.4">|:071000288|:  0090418||</text>'
            f'</g>'
        )

        # --- TABLE PROP 3: Two Steaming Ceramic Coffee Mugs ---
        mugs = [(296, 396, 0.88), (746, 464, 1.05)]
        for mx_m, my_m, ms_m in mugs:
            s.append(
                f'<g transform="translate({mx_m},{my_m}) scale({ms_m:.2f})">'
                f'<ellipse cx="4" cy="24" rx="28" ry="9" fill="#2A1C12" opacity="0.34"/>'
                # Handle
                f'<path d="M22,-8 Q36,-8 36,6 Q36,18 20,16" fill="none" stroke="#EFE6D4" stroke-width="5.5" stroke-linecap="round"/>'
                f'<path d="M22,-8 Q36,-8 36,6 Q36,18 20,16" fill="none" stroke="{INK_WARM}" stroke-width="1.6"/>'
                # Ceramic body
                f'<path d="M-22,-16 L-20,18 Q0,27 20,18 L22,-16 Z" fill="#EFE7D6" stroke="{INK_WARM}" stroke-width="1.7"/>'
                f'<path d="M-14,-12 L-13,16" fill="none" stroke="#FFFFFF" stroke-width="3.2" opacity="0.55"/>'
                # Rim & hot dark coffee
                f'<ellipse cx="0" cy="-16" rx="22" ry="7.5" fill="#F7F0E2" stroke="{INK_WARM}" stroke-width="1.5"/>'
                f'<ellipse cx="0" cy="-15.5" rx="18" ry="5.5" fill="#2B160B"/>'
                f'<path d="M-10,-16 Q0,-19 10,-16" fill="none" stroke="#9C6B43" stroke-width="1.1" opacity="0.65"/>'
                # Rising curling steam wisps
                f'<path d="M-6,-24 Q-12,-40 -4,-54 Q2,-66 -6,-78" fill="none" stroke="#FFF6E2" stroke-width="2.0" opacity="0.48" stroke-linecap="round"/>'
                f'<path d="M6,-22 Q14,-38 6,-52 Q0,-64 8,-74" fill="none" stroke="#FFF6E2" stroke-width="1.6" opacity="0.38" stroke-linecap="round"/>'
                f'</g>'
            )

        # --- TABLE PROP 4: Classic Diner Ketchup Bottle, Chrome Napkin Dispenser & Salt/Pepper (right) ---
        # Chrome napkin dispenser (x=822, y=386)
        s.append(
            f'<g transform="translate(822,386)">'
            f'<polygon points="-24,18 26,18 32,26 -18,26" fill="#22170F" opacity="0.35"/>'
            f'<rect x="-22" y="-34" width="44" height="54" rx="4" fill="#9AA5AE" stroke="{INK_WARM}" stroke-width="1.6"/>'
            f'<rect x="-15" y="-26" width="30" height="38" rx="2" fill="#DCE4EC" stroke="#5A6670" stroke-width="1.0"/>'
            f'<rect x="-11" y="-22" width="22" height="30" fill="#FAF6EC"/>'
            f'<path d="M-18,-30 L-18,14" fill="none" stroke="#FFFFFF" stroke-width="1.8" opacity="0.72"/>'
            f'</g>'
        )
        # Glass Ketchup Bottle (x=762, y=378)
        s.append(
            f'<g transform="translate(762,378)">'
            f'<ellipse cx="2" cy="30" rx="16" ry="5" fill="#22170F" opacity="0.35"/>'
            f'<path d="M-6,-42 L6,-42 L8,-16 L14,-4 L13,26 Q0,31 -13,26 L-14,-4 L-8,-16 Z" fill="#A61D22" stroke="{INK_WARM}" stroke-width="1.6"/>'
            f'<rect x="-7" y="-48" width="14" height="8" rx="1.5" fill="#F2ECE0" stroke="{INK_WARM}" stroke-width="1.3"/>'
            # Cream label
            f'<rect x="-11" y="-2" width="22" height="19" rx="1.5" fill="#F6EED9" stroke="#7A2124" stroke-width="1.0"/>'
            f'<text x="-9" y="10" font-family="DejaVu Sans, Arial, sans-serif" font-size="5.2" font-weight="bold" fill="#8C1D22">KETCHUP</text>'
            # Glass specular highlight
            f'<path d="M-8,-2 L-8,22" fill="none" stroke="#FF8A8E" stroke-width="2.0" opacity="0.62"/>'
            f'</g>'
        )
        # Salt & pepper shakers beside napkin dispenser
        for sx_sp, cap_col, body_col in [(868, "#C8D0D8", "#F4EFE4"), (892, "#C8D0D8", "#4A433D")]:
            s.append(f'<rect x="{sx_sp-7}" y="394" width="14" height="22" rx="3" fill="{body_col}" stroke="{INK_WARM}" stroke-width="1.3"/>')
            s.append(f'<ellipse cx="{sx_sp}" cy="394" rx="6.5" ry="4" fill="{cap_col}" stroke="{INK_WARM}" stroke-width="1.2"/>')

        s.append('</g>')
        parts.append("".join(s))

    # --- LAYER 4: PLAN (Subtle Style B+A cyan link from $90,000 check to loan sharks outside) ---
    if _katman_aktif(katmanlar, "plan"):
        pl: list[str] = ['<g id="s107-plan" opacity="0.80">']
        # Dashed analytical link connecting $90,000 check to loan sharks outside
        pl.append(
            f'<path d="M622,448 L674,398 L674,256" fill="none" stroke="{PLAN}" '
            f'stroke-width="1.2" stroke-dasharray="5 4" opacity="0.72"/>'
        )
        pl.append(f'<circle cx="622" cy="448" r="3.4" fill="{PLAN_CORE}" stroke="{PLAN}" stroke-width="1.2"/>')
        pl.append(f'<rect x="606" y="138" width="164" height="142" rx="4" fill="none" stroke="{PLAN}" stroke-width="1.0" stroke-dasharray="6 4" opacity="0.54"/>')
        pl.append(f'<rect x="606" y="116" width="114" height="19" rx="3" fill="#0B141E" opacity="0.82" stroke="{PLAN}" stroke-width="0.9"/>')
        pl.append(
            f'<text x="614" y="129" font-family="DejaVu Sans Mono, monospace" font-size="10" '
            f'font-weight="bold" fill="{PLAN_CORE}" letter-spacing="1.0">DEBT · $90,000</text>'
        )
        pl.append('</g>')
        parts.append("".join(pl))

    # --- LAYER 5: ONPLAN (Hanging warm amber diner glass lamp, soft radial light glow, vignette) ---
    if _katman_aktif(katmanlar, "onplan"):
        op: list[str] = ['<g id="s107-onplan">']
        # Soft blurred warm amber cone descending from ceiling pendant lamp (no hard polygon edge!)
        op.append(f'<ellipse cx="515" cy="285" rx="235" ry="220" fill="url(#{p}_lamp_cone)" opacity="0.72"/>')
        op.append(f'<polygon points="452,96 578,96 720,540 310,540" fill="url(#{p}_lamp_cone)" opacity="0.38" filter="url(#{p}_glow_amber)"/>')
        # Brass chain + hanging amber stained-glass pendant lamp at top-center
        op.append(f'<path d="M515,0 L515,38" fill="none" stroke="#8C6233" stroke-width="4.0"/>')
        op.append(f'<rect x="503" y="34" width="24" height="12" rx="2" fill="#A6743B" stroke="{INK_WARM}" stroke-width="1.5"/>')
        op.append(
            f'<path d="M446,96 Q456,46 515,44 Q574,46 584,96 Z" '
            f'fill="url(#{p}_amber_lamp)" stroke="{INK_WARM}" stroke-width="2.0" filter="url(#{p}_glow_amber)"/>'
        )
        # Fluted stained-glass ribs on pendant shade
        for rx_sh in (474, 496, 515, 534, 556):
            op.append(f'<path d="M515,44 Q{rx_sh},70 {rx_sh},96" fill="none" stroke="#6E3B15" stroke-width="1.3" opacity="0.65"/>')
        op.append(f'<path d="M444,96 L586,96" fill="none" stroke="#5A2F10" stroke-width="3.2"/>')
        # Warm bulb core glow at bottom rim
        op.append('<ellipse cx="515" cy="96" rx="52" ry="7" fill="#FFF8DC" opacity="0.85"/>')

        # Cinematic vignette
        op.append(f'<rect x="0" y="0" width="960" height="540" fill="url(#{p}_vignette)"/>')
        op.append('</g>')
        parts.append("".join(op))

    return defs, "".join(parts)


# =============================================================================
# RENDERING & PRESENTATION CARDS (ALL ENGLISH LABELS)
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
    # Subtle blueprint grid
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
    img_105 = _render_scene(set_105_sabah_yatak, scale=2.0)  # 1920x1080
    img_106 = _render_scene(set_106_lise_origami, scale=2.0)
    img_107 = _render_scene(set_107_lokanta_cek, scale=2.0)

    f_title = _load_font(20, bold=True)
    f_sub = _load_font(12, bold=False)
    f_card_t = _load_font(13, bold=True)
    f_card_s = _load_font(11, bold=False)
    f_small = _load_font(10, bold=False)

    # =========================================================================
    # OUTPUT 1: SET PRESENTATION CARD (1280 x 720 — ALL ENGLISH)
    # =========================================================================
    canvas = _draw_card_bg(1280, 720)
    draw = ImageDraw.Draw(canvas)

    draw.text((24, 14), "MICHAEL SCOFIELD  ·  ACT I SCENE SETS (1.05 – 1.07)", fill="#EBF3FA", font=f_title)
    draw.text((24, 39), "STYLE B+A HYBRID (CINEMATIC 2D + CYAN PLAN VISION)  ·  5-LAYER PARALLAX SETS (960×540)",
              fill="#7E97B0", font=f_sub)
    top_swatches = [("#FFE196", "SUN"), ("#5B3720", "WOOD"), ("#21382F", "CLASS"),
                    ("#6D1E28", "DINER"), ("#7FE6FF", "PLAN")]
    sx_top = 876
    for col, lbl in top_swatches:
        draw.rounded_rectangle((sx_top, 18, sx_top + 14, 32), radius=3, fill=col, outline="#3B536D", width=1)
        draw.text((sx_top + 19, 19), lbl, fill="#9BB2C8", font=f_small)
        sx_top += 76
    draw.line((24, 58, 1256, 58), fill="#213247", width=1)

    # --- TOP-LEFT: 1.05 MORNING BEDSIDE ---
    _draw_panel_box(draw, (22, 68, 630, 366))
    t105 = img_105.resize((448, 252), Image.Resampling.LANCZOS)
    canvas.paste(t105, (34, 98), t105)
    draw.rectangle((34, 98, 34 + 448, 98 + 252), outline="#5A4632", width=1)
    draw.text((34, 76), "1.05 · MORNING BEDSIDE", fill="#F6C367", font=f_card_t)
    draw.text((222, 78), "Act I · \"I'M HERE\"", fill="#9DB0C4", font=f_card_s)
    ix = 492
    draw.text((ix, 98), "PALETTE", fill="#7FE6FF", font=f_small)
    _draw_swatches(draw, ix, 114, ["#4D2E1B", "#EFE2CA", "#3B536D", "#FFE09A", "#7FE6FF"], size=18, gap=5)
    draw.text((ix, 146), "KEY ELEMENTS", fill="#9BB2C8", font=f_small)
    for k_i, item in enumerate([
        "• Slatted wood headboard",
        "• Wrinkled cotton sheets",
        "• Bedside lamp & alarm",
        "• Venetian blind beams",
        "• Locked Turna v4 jewel",
    ]):
        draw.text((ix, 164 + k_i * 19), item, fill="#D5E2EE", font=f_card_s)
    draw.text((ix, 272), "KEY LIGHT", fill="#9BB2C8", font=f_small)
    draw.text((ix, 288), "Golden morning sunbeams", fill="#F6C367", font=f_card_s)
    draw.text((ix, 314), "LAYERS (5)", fill="#9BB2C8", font=f_small)
    draw.text((ix, 330), "uzak · orta · sahne\nplan · onplan", fill="#8AA3BC", font=f_small)

    # --- TOP-RIGHT: 1.06 HIGH SCHOOL CRAFT DESK ---
    _draw_panel_box(draw, (648, 68, 1256, 366))
    t106 = img_106.resize((448, 252), Image.Resampling.LANCZOS)
    canvas.paste(t106, (660, 98), t106)
    draw.rectangle((660, 98, 660 + 448, 98 + 252), outline="#3E5466", width=1)
    draw.text((660, 76), "1.06 · HIGH SCHOOL CRAFT DESK", fill="#7FE6FF", font=f_card_t)
    draw.text((886, 78), "Act I · \"HIGH SCHOOL\"", fill="#9DB0C4", font=f_card_s)
    ix2 = 1118
    draw.text((ix2, 98), "PALETTE", fill="#7FE6FF", font=f_small)
    _draw_swatches(draw, ix2, 114, ["#21382F", "#526673", "#8B5C36", "#FFE6A8", "#7FE6FF"], size=18, gap=5)
    draw.text((ix2, 146), "KEY ELEMENTS", fill="#9BB2C8", font=f_small)
    for k_i, item in enumerate([
        "• Chalk-drawn blackboard",
        "• Sunlit tall windows",
        "• Scratched wood desk",
        "• Diagram, ruler, scissors",
        "• 5 soaring Turna v4",
    ]):
        draw.text((ix2, 164 + k_i * 19), item, fill="#D5E2EE", font=f_card_s)
    draw.text((ix2, 272), "KEY LIGHT", fill="#9BB2C8", font=f_small)
    draw.text((ix2, 288), "Warm afternoon window", fill="#F6D07C", font=f_card_s)
    draw.text((ix2, 314), "LAYERS (5)", fill="#9BB2C8", font=f_small)
    draw.text((ix2, 330), "uzak · orta · sahne\nplan · onplan", fill="#8AA3BC", font=f_small)

    # --- BOTTOM WIDE PANEL: 1.07 NIGHT DINER & $90,000 SACRIFICE ---
    _draw_panel_box(draw, (22, 378, 1256, 704))
    t107 = img_107.resize((512, 288), Image.Resampling.LANCZOS)
    canvas.paste(t107, (34, 404), t107)
    draw.rectangle((34, 404, 34 + 512, 404 + 288), outline="#6A333D", width=1)
    draw.text((34, 384), "1.07 · NIGHT DINER & $90,000 SACRIFICE", fill="#F2AE57", font=f_card_t)
    draw.text((314, 386), "Act I · \"AGE 18\" / \"$90,000\"", fill="#A69788", font=f_card_s)

    rx = 564
    draw.text((rx, 404), "PALETTE (WARM DINER VS. RAINY NIGHT)", fill="#F2AE57", font=f_small)
    _draw_swatches(draw, rx, 422, ["#0C1524", "#6D1E28", "#FF2932", "#F2AE4B", "#EAF2E5", "#7FE6FF"], size=22, gap=7)
    draw.text((rx, 458), "KEY ELEMENTS (5)", fill="#9BB2C8", font=f_small)
    for k_i, item in enumerate([
        "• Burgundy tufted leather booth & Formica table",
        "• Warm amber glass pendant lamp & steaming mugs",
        "• Open envelope & realistic $90,000 bank check",
        "• Locked Lincoln v1 in broad jacket (warm gaze)",
        "• Rainy neon window, sedan taillights & 2 loan sharks",
    ]):
        draw.text((rx, 476 + k_i * 21), item, fill="#E3ECF5", font=f_card_s)
    draw.text((rx, 588), "LIGHTING & DRAMATIC CONTRAST", fill="#9BB2C8", font=f_small)
    draw.text((rx, 606), "Warm amber interior refuge around Lincoln's sacrifice\ncontrasted against cold rain and crimson taillights\nof the loan sharks waiting outside.",
              fill="#D4C2AB", font=f_card_s)
    draw.text((rx, 666), "LAYERS: s107-uzak · s107-orta · s107-sahne · s107-plan · s107-onplan",
              fill="#8AA3BC", font=f_small)

    draw.line((886, 404, 886, 692), fill="#233447", width=1)
    tx = 904
    draw.text((tx, 404), "VISUAL ARC & LOCKED ASSETS", fill="#7FE6FF", font=f_card_t)
    notes = [
        ("LOCKED PROPS & CHARACTERS",
         "Imports K.turna() v4 and K.lincoln_kafa()\ndirectly from karakter.py (read-only).\nLincoln's forearm stays tattoo-free (R3)."),
        ("RICH TEXTURE & ACTIVITY",
         "Every flat box replaced with layered wood\ngrain, fabric folds, chalk sketches, tools,\nsteaming coffee and rain-streaked glass."),
        ("ENGLISH-ONLY SCREEN TEXT",
         "All diegetic props (FOLD 01->02->03,\nPAY TO MICHAEL SCOFIELD, $90,000,\nOPEN 24H) and cards strictly in English."),
    ]
    ny = 434
    for heading, body_txt in notes:
        draw.text((tx, ny), heading, fill="#F6C367" if "LOCKED" in heading else "#9EC5DE", font=f_small)
        draw.text((tx, ny + 16), body_txt, fill="#C5D5E4", font=f_card_s)
        ny += 86

    out_main = OUT_DIR / f"b1_set_turna_{versiyon}.png"
    canvas.convert("RGB").save(out_main, quality=95)

    # =========================================================================
    # OUTPUT 2: R13 200% CROP QUALITY AUDIT CARD (1280 x 720 — 4 PANELS)
    # =========================================================================
    r13 = _draw_card_bg(1280, 720)
    d13 = ImageDraw.Draw(r13)
    d13.text((24, 13), "R13 · 200% ZOOM QUALITY AUDIT (ACT I: 1.05 – 1.07 SETS)", fill="#EBF3FA", font=f_title)
    d13.text((24, 37), "1:1 PIXEL CROPS FROM 1920×1080 RENDERS  ·  FABRIC, WOOD GRAIN, CHECK DETAIL, LINCOLN & RAINY WINDOW",
             fill="#7E97B0", font=f_sub)
    d13.line((24, 55, 1256, 55), fill="#213247", width=1)

    cw, ch = 600, 264
    crops = [
        (img_105, (1096, 710), "1 · 1.05 COTTON SHEETS + LOCKED TURNA V4 (200%)",
         "Wrinkled cotton creases, quilt edge, golden sunbeams & jewel crane", (22, 66)),
        (img_106, (680, 860), "2 · 1.06 HIGH SCHOOL ORIGAMI DESK & TOOLS (200%)",
         "Wood grain, FOLD 01 -> 02 -> 03 diagram, steel ruler, square papers", (652, 66)),
        (img_107, None, "3 · 1.07 LOCKED LINCOLN V1 + $90,000 BANK CHECK (200%)",
         "Split 1:1 crop: Lincoln v1 warm protective gaze (left) & $90,000 check (right)", (22, 392)),
        (img_107, (1395, 420), "4 · 1.07 RAINY WINDOW + LOAN SHARKS & SEDAN (200%)",
         "Rain droplets on glass, red taillights & 2 sculpted trenchcoat figures", (652, 392)),
    ]

    for src_img, center, title, sub, (bx, by) in crops:
        _draw_panel_box(d13, (bx, by, bx + 606, by + 314))
        if center is None:
            # Split 1:1 200% crop: Left 216px Lincoln v1 portrait + Right 380px $90,000 check
            lw_s, rw_s = 236, cw - 240
            lx0 = max(0, min(src_img.width - lw_s, 434 - lw_s // 2))
            ly0 = max(0, min(src_img.height - ch, 442 - ch // 2))
            p_linc = src_img.crop((lx0, ly0, lx0 + lw_s, ly0 + ch))

            rx0 = max(0, min(src_img.width - rw_s, 1175 - rw_s // 2))
            ry0 = max(0, min(src_img.height - ch, 916 - ch // 2))
            p_chk = src_img.crop((rx0, ry0, rx0 + rw_s, ry0 + ch))

            r13.paste(p_linc, (bx + 3, by + 44), p_linc)
            r13.paste(p_chk, (bx + 3 + lw_s + 4, by + 44), p_chk)
            d13.line((bx + 3 + lw_s + 2, by + 44, bx + 3 + lw_s + 2, by + 44 + ch), fill="#7FE6FF", width=2)
        else:
            cx, cy = center
            x0 = max(0, min(src_img.width - cw, cx - cw // 2))
            y0 = max(0, min(src_img.height - ch, cy - ch // 2))
            patch = src_img.crop((x0, y0, x0 + cw, y0 + ch))
            r13.paste(patch, (bx + 3, by + 44), patch)
        d13.rectangle((bx + 3, by + 44, bx + 3 + cw, by + 44 + ch), outline="#2F465E", width=1)
        d13.text((bx + 12, by + 8), title, fill="#7FE6FF", font=f_card_t)
        d13.text((bx + 12, by + 25), sub, fill="#96AEC6", font=f_small)

    out_r13 = OUT_DIR / "b1_set_turna_r13.png"
    r13.convert("RGB").save(out_r13, quality=95)
    print(f"Saved:\n  - {out_main}\n  - {out_r13}")
    return out_main, out_r13


if __name__ == "__main__":
    uret_kartlar("v1")
