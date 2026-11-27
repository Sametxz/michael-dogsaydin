"""V3 (Bölüm I: Chicago Structural Engineer, Fox River Blueprint & Death Row Front Page).

Style B+A Hybrid (Cinematic 2D + Cyan Blueprint Vision) — 5-layer parallax-ready scenes (960x540):
  - set_108_chicago_ofis(katmanlar=None)   -> (defs_str, body_str)
  - set_109_taslak_masasi(katmanlar=None)  -> (defs_str, body_str)
  - set_110_idam_manset(katmanlar=None)    -> (defs_str, body_str)

All on-screen text is in ENGLISH. All stroked <path> elements explicitly set fill="none".
Uses locked assets K.turna (v4) and K.lincoln_kafa (v1) from karakter.py without modifying it.
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
INK_WARM = "#1C1410"
PLAN = "#7FE6FF"
PLAN_CORE = "#DDFBFF"
RED_ALERT = "#E63244"

_UID = 0


def _uid(prefix: str = "b1") -> str:
    global _UID
    _UID += 1
    return f"{prefix}_{_UID}"


def _katman_aktif(katmanlar: set[str] | list[str] | None, ad: str) -> bool:
    return katmanlar is None or ad in katmanlar


# =============================================================================
# SCENE 1.08: CHICAGO STRUCTURAL ENGINEERING OFFICE ("STRUCTURAL ENGINEER")
# =============================================================================
def set_108_chicago_ofis(
    katmanlar: set[str] | list[str] | None = None,
) -> tuple[str, str]:
    """Modern glass-walled Chicago structural engineering office at twilight.
    Foreground architect desk + steaming coffee + walnut wall with gold-framed Loyola diploma;
    huge window opens to twilight Chicago skyline (Willis Tower twin antennas, Hancock X-bracing,
    bascule river bridge, warm windows) dissolving on the right into live #7FE6FF CAD wireframe.
    """
    rng = random.Random(108)
    p = _uid("s108")

    defs = f"""
    <linearGradient id="{p}_sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#070E1C"/>
      <stop offset="38%" stop-color="#11223B"/>
      <stop offset="72%" stop-color="#223754"/>
      <stop offset="90%" stop-color="#4B4657"/>
      <stop offset="100%" stop-color="#7B5647"/>
    </linearGradient>
    <radialGradient id="{p}_horizon_glow" cx="0.62" cy="0.72" r="0.48">
      <stop offset="0%" stop-color="#E89A5C" stop-opacity="0.42"/>
      <stop offset="45%" stop-color="#8A5258" stop-opacity="0.18"/>
      <stop offset="100%" stop-color="#0E1B30" stop-opacity="0.0"/>
    </radialGradient>
    <linearGradient id="{p}_river" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#0D192B"/>
      <stop offset="50%" stop-color="#13263E"/>
      <stop offset="100%" stop-color="#09121F"/>
    </linearGradient>
    <linearGradient id="{p}_wood_wall" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#1A120D"/>
      <stop offset="48%" stop-color="#2E1E15"/>
      <stop offset="82%" stop-color="#3C271B"/>
      <stop offset="100%" stop-color="#241710"/>
    </linearGradient>
    <linearGradient id="{p}_gold_frame" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F8DF96"/>
      <stop offset="32%" stop-color="#B88839"/>
      <stop offset="68%" stop-color="#E7C26B"/>
      <stop offset="100%" stop-color="#7C561F"/>
    </linearGradient>
    <linearGradient id="{p}_parchment" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#F7F0DE"/>
      <stop offset="100%" stop-color="#E2D5B8"/>
    </linearGradient>
    <linearGradient id="{p}_desk_top" x1="0" y1="0" x2="0.8" y2="1">
      <stop offset="0%" stop-color="#3B271B"/>
      <stop offset="45%" stop-color="#281A12"/>
      <stop offset="100%" stop-color="#17100C"/>
    </linearGradient>
    <linearGradient id="{p}_desk_edge" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#5E3E2A"/>
      <stop offset="50%" stop-color="#3B271B"/>
      <stop offset="100%" stop-color="#1C130E"/>
    </linearGradient>
    <radialGradient id="{p}_lamp_pool" cx="0.28" cy="0.84" r="0.34">
      <stop offset="0%" stop-color="#FFD98B" stop-opacity="0.46"/>
      <stop offset="48%" stop-color="#E0943E" stop-opacity="0.18"/>
      <stop offset="100%" stop-color="#E0943E" stop-opacity="0.0"/>
    </radialGradient>
    <radialGradient id="{p}_sconce_glow" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0%" stop-color="#FFE6A8" stop-opacity="0.62"/>
      <stop offset="45%" stop-color="#D98B3B" stop-opacity="0.20"/>
      <stop offset="100%" stop-color="#D98B3B" stop-opacity="0.0"/>
    </radialGradient>
    <linearGradient id="{p}_glass_glare" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#BCEBFF" stop-opacity="0.10"/>
      <stop offset="50%" stop-color="#BCEBFF" stop-opacity="0.02"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0.0"/>
    </linearGradient>
    <linearGradient id="{p}_cad_fade" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#7FE6FF" stop-opacity="0.0"/>
      <stop offset="35%" stop-color="#7FE6FF" stop-opacity="0.14"/>
      <stop offset="100%" stop-color="#7FE6FF" stop-opacity="0.34"/>
    </linearGradient>
    <radialGradient id="{p}_vignette" cx="0.52" cy="0.48" r="0.66">
      <stop offset="58%" stop-color="#000000" stop-opacity="0.0"/>
      <stop offset="100%" stop-color="#03060C" stop-opacity="0.68"/>
    </radialGradient>
    <filter id="{p}_glow_cyan" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="2.4" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="{p}_glow_warm" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="3.5" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <clipPath id="{p}_win_clip">
      <rect x="252" y="28" width="686" height="366"/>
    </clipPath>
    """

    parts: list[str] = []

    # -------------------------------------------------------------------------
    # LAYER 1: UZAK — Chicago Twilight Skyline, Clouds, River & Bascule Bridge
    # -------------------------------------------------------------------------
    if _katman_aktif(katmanlar, "uzak"):
        u: list[str] = ['<g id="s108-uzak">']
        u.append(f'<rect x="0" y="0" width="960" height="540" fill="#080F1A"/>')
        u.append(f'<g clip-path="url(#{p}_win_clip)">')
        # Sky & twilight glow
        u.append(f'<rect x="252" y="28" width="686" height="310" fill="url(#{p}_sky)"/>')
        u.append(f'<rect x="252" y="28" width="686" height="310" fill="url(#{p}_horizon_glow)"/>')

        # Layered twilight clouds
        cloud_specs = [
            (280, 96, 150, 22, "#1C304E", 0.55),
            (460, 74, 190, 26, "#253A59", 0.48),
            (690, 92, 175, 24, "#1C2E4A", 0.52),
            (370, 142, 210, 18, "#4A4359", 0.40),
            (620, 148, 220, 20, "#5B4A59", 0.36),
            (790, 126, 150, 16, "#324461", 0.45),
        ]
        for cx, cy, rx, ry, col, op in cloud_specs:
            u.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{col}" opacity="{op}"/>')
            u.append(f'<ellipse cx="{cx+28}" cy="{cy+5}" rx="{rx*0.68:.1f}" ry="{ry*0.65:.1f}" fill="#D98E5C" opacity="{op*0.24:.2f}"/>')

        # Subtle stars in upper sky
        for _ in range(28):
            sx = rng.uniform(265, 925)
            sy = rng.uniform(36, 128)
            sr = rng.uniform(0.6, 1.3)
            u.append(f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="{sr:.1f}" fill="#DDF0FF" opacity="{rng.uniform(0.25,0.7):.2f}"/>')

        # Far background skyline silhouettes (depth layer)
        far_bldgs = [
            (265, 195, 38, 125, "#0D1A2D"),
            (308, 172, 34, 148, "#0F1E33"),
            (346, 208, 42, 112, "#0C182A"),
            (412, 164, 36, 156, "#102036"),
            (518, 180, 44, 140, "#0E1C30"),
            (566, 156, 38, 164, "#112239"),
            (652, 174, 40, 146, "#0E1C31"),
            (758, 186, 46, 134, "#0D1A2E"),
            (858, 168, 48, 152, "#0D1A2D"),
        ]
        for bx, by, bw, bh, bc in far_bldgs:
            u.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" fill="{bc}"/>')
            # Tiny warm far windows
            for wy in range(by + 10, by + bh - 12, 11):
                for wx in range(bx + 5, bx + bw - 6, 8):
                    if rng.random() < 0.38:
                        wc = rng.choice(["#F4C97A", "#9AC8E8", "#FFE6B0"])
                        u.append(f'<rect x="{wx}" y="{wy}" width="3.5" height="4.5" fill="{wc}" opacity="{rng.uniform(0.25,0.65):.2f}"/>')

        # --- HERO SKYSCRAPER 1: WILLIS TOWER (stepped 9-tube icon + twin antennas) ---
        # Stepped profile: base x=370..456, mid-step 380..448, upper 392..444, crown 402..434
        u.append('<polygon points="370,320 370,188 380,188 380,142 392,142 392,106 404,106 404,88 434,88 434,116 446,116 446,158 456,158 456,320" fill="#111F33" stroke="#080F1A" stroke-width="1.3"/>')
        # Sunlit left-edge highlight + vertical tube seams
        u.append('<path d="M370,188 L370,320 M380,142 L380,320 M392,106 L392,320 M404,88 L404,320 M419,88 L419,320 M434,88 L434,320 M446,116 L446,320" fill="none" stroke="#1E3452" stroke-width="1.0" opacity="0.75"/>')
        u.append('<path d="M404,88 L434,88 M392,106 L404,106 M434,116 L446,116" fill="none" stroke="#6E8EB0" stroke-width="1.0" opacity="0.55"/>')
        # Twin Willis Tower antennas
        u.append('<path d="M411,88 L411,42 M427,88 L427,42" fill="none" stroke="#C5DCF0" stroke-width="1.8"/>')
        u.append('<path d="M411,64 L411,38 M427,64 L427,38" fill="none" stroke="#EBF6FF" stroke-width="1.0"/>')
        u.append('<circle cx="411" cy="38" r="2.2" fill="#FF4B55" filter="url(#%s_glow_warm)"/>' % p)
        u.append('<circle cx="427" cy="38" r="2.2" fill="#FF4B55" filter="url(#%s_glow_warm)"/>' % p)
        # Willis Tower lit office bands
        for wy in range(96, 310, 9):
            x_min = 406 if wy < 106 else (394 if wy < 142 else (382 if wy < 188 else 373))
            x_max = 431 if wy < 116 else (443 if wy < 158 else 452)
            for wx in range(x_min, x_max, 6):
                if rng.random() < 0.48:
                    wc = rng.choice(["#FFD98A", "#FFF1C4", "#A9D8F5", "#F0B65E"])
                    u.append(f'<rect x="{wx}" y="{wy}" width="3.6" height="4.2" fill="{wc}" opacity="{rng.uniform(0.35,0.88):.2f}"/>')

        # --- HERO SKYSCRAPER 2: ART DECO STEPPED TOWER (left-mid, warm spire) ---
        u.append('<polygon points="282,320 282,192 294,192 294,166 306,166 306,144 326,144 326,166 338,166 338,192 350,192 350,320" fill="#16263D" stroke="#09101C" stroke-width="1.2"/>')
        u.append('<polygon points="309,144 316,118 323,144" fill="#233958" stroke="#09101C" stroke-width="1.0"/>')
        u.append('<path d="M316,118 L316,102" fill="none" stroke="#F4C97A" stroke-width="1.2"/>')
        for wy in range(154, 312, 10):
            xl = 309 if wy < 166 else (297 if wy < 192 else 286)
            xr = 323 if wy < 166 else (335 if wy < 192 else 346)
            for wx in range(xl, xr, 7):
                if rng.random() < 0.55:
                    u.append(f'<rect x="{wx}" y="{wy}" width="4" height="5" fill="{rng.choice(["#FFDA8E","#F2B45C","#D5EEFF"])}" opacity="{rng.uniform(0.4,0.85):.2f}"/>')

        # --- HERO SKYSCRAPER 3: MID-CENTER GLASS TOWER (transitioning into CAD!) ---
        u.append('<polygon points="484,320 484,132 518,116 544,132 544,320" fill="#14253C" stroke="#08101C" stroke-width="1.2"/>')
        u.append('<polygon points="518,116 544,132 544,320 518,320" fill="#0F1D31"/>')
        for wy in range(138, 312, 10):
            for wx in range(489, 538, 8):
                if rng.random() < 0.52:
                    wc = "#7FE6FF" if wx > 518 and rng.random() < 0.45 else rng.choice(["#FFE2A2", "#A8DCFA"])
                    u.append(f'<rect x="{wx}" y="{wy}" width="4.5" height="4.8" fill="{wc}" opacity="{rng.uniform(0.35,0.85):.2f}"/>')

        # --- HERO SKYSCRAPER 4: JOHN HANCOCK-INSPIRED TAPERED X-BRACED TOWER (solid left -> CAD right!) ---
        u.append('<polygon points="602,320 618,96 668,96 684,320" fill="#101E32" opacity="0.88" stroke="#08101A" stroke-width="1.2"/>')
        # Partial CAD dissolution mask tint on right side of skyline
        u.append(f'<rect x="590" y="34" width="348" height="290" fill="url(#{p}_cad_fade)"/>')
        # Solid lower-left windows on Hancock tower
        for wy in range(112, 312, 11):
            t_y = (wy - 96) / 224.0
            xl = int(618 - t_y * 15) + 4
            xr = int(668 + t_y * 15) - 24  # right half dissolves to CAD
            for wx in range(xl, xr, 7):
                if rng.random() < 0.50:
                    u.append(f'<rect x="{wx}" y="{wy}" width="3.8" height="4.5" fill="{rng.choice(["#FFD98A","#9AD5F5"])}" opacity="{rng.uniform(0.35,0.82):.2f}"/>')
        # Twin antennas on Hancock
        u.append('<path d="M630,96 L630,52 M656,96 L656,52" fill="none" stroke="#7FE6FF" stroke-width="1.6" opacity="0.9"/>')

        # --- RIGHT SKYSCRAPERS: HALF-SOLID / HALF-CAD WIREFRAME ---
        u.append('<polygon points="712,320 712,148 742,134 776,148 776,320" fill="#0D1D33" opacity="0.62"/>')
        u.append('<polygon points="802,320 802,118 854,118 854,320" fill="#0C1A2E" opacity="0.48"/>')
        u.append('<polygon points="872,320 872,162 918,162 918,320" fill="#0A1628" opacity="0.38"/>')

        # --- CHICAGO RIVER & REFLECTIONS ---
        u.append(f'<rect x="252" y="318" width="686" height="76" fill="url(#{p}_river)"/>')
        # Vertical city light shimmer on water
        for _ in range(95):
            rx = rng.uniform(260, 926)
            ry = rng.uniform(323, 386)
            rw = rng.uniform(6, 26)
            rc = "#7FE6FF" if rx > 610 and rng.random() < 0.65 else rng.choice(["#FFD78A", "#F2A852", "#9AD8F8"])
            u.append(f'<rect x="{rx:.1f}" y="{ry:.1f}" width="{rw:.1f}" height="1.6" rx="0.8" fill="{rc}" opacity="{rng.uniform(0.18,0.62):.2f}"/>')

        # --- CHICAGO BASCULE RIVER BRIDGE (Steel Truss Arch + Stone Piers + Lamps) ---
        # Stone bridge piers
        u.append('<rect x="336" y="310" width="22" height="36" fill="#1B283A" stroke="#091019" stroke-width="1.2"/>')
        u.append('<rect x="556" y="310" width="22" height="36" fill="#1B283A" stroke="#091019" stroke-width="1.2"/>')
        u.append('<rect x="772" y="310" width="22" height="36" fill="#15253A" stroke="#091019" stroke-width="1.2"/>')
        # Bridge roadway deck
        u.append('<rect x="252" y="324" width="686" height="8" fill="#162233" stroke="#080E17" stroke-width="1.0"/>')
        # Steel truss arches across main span (358..556) and right span (578..772)
        for sx0, sx1, is_cad in [(358, 556, False), (578, 772, True)]:
            sc = "#7FE6FF" if is_cad else "#243750"
            op = "0.82" if is_cad else "0.95"
            mid = (sx0 + sx1) * 0.5
            u.append(f'<path d="M{sx0},324 Q{mid:.0f},292 {sx1},324" fill="none" stroke="{sc}" stroke-width="2.4" opacity="{op}"/>')
            u.append(f'<path d="M{sx0},324 L{sx1},324" fill="none" stroke="{sc}" stroke-width="1.8" opacity="{op}"/>')
            steps = 8
            for i in range(steps):
                t0 = i / steps
                t1 = (i + 1) / steps
                x0 = sx0 + (sx1 - sx0) * t0
                x1 = sx0 + (sx1 - sx0) * t1
                y0 = 324 - 16 * 4 * t0 * (1 - t0)
                y1 = 324 - 16 * 4 * t1 * (1 - t1)
                u.append(f'<path d="M{x0:.1f},324 L{x0:.1f},{y0:.1f} L{x1:.1f},324 M{x0:.1f},324 L{x1:.1f},{y1:.1f}" fill="none" stroke="{sc}" stroke-width="1.1" opacity="{op}"/>')
        # Bridge warm street lamps
        for lx in (310, 396, 456, 516, 616, 680, 744):
            u.append(f'<path d="M{lx},324 L{lx},311" fill="none" stroke="#364C66" stroke-width="1.2"/>')
            u.append(f'<circle cx="{lx}" cy="310" r="2.2" fill="#FFE6A3"/>')
            u.append(f'<circle cx="{lx}" cy="310" r="7" fill="#F2B256" opacity="0.22"/>')

        u.append('</g>')  # end win_clip
        u.append('</g>')
        parts.append("\n".join(u))

    # -------------------------------------------------------------------------
    # LAYER 2: ORTA — Walnut Office Wall, Gold-Framed Loyola Diploma, Curtain Wall
    # -------------------------------------------------------------------------
    if _katman_aktif(katmanlar, "orta"):
        o: list[str] = ['<g id="s108-orta">']
        # Ceiling & upper beam
        o.append(f'<rect x="0" y="0" width="960" height="32" fill="#0C131E" stroke="{INK}" stroke-width="1.5"/>')
        # Recessed ceiling spotlights
        for sx in (360, 560, 760):
            o.append(f'<ellipse cx="{sx}" cy="18" rx="16" ry="4" fill="#1D2B3D"/>')
            o.append(f'<ellipse cx="{sx}" cy="18" rx="9" ry="2.2" fill="#FFE3A8" opacity="0.85"/>')
            o.append(f'<polygon points="{sx-10},20 {sx+10},20 {sx+44},118 {sx-44},118" fill="#FFE3A8" opacity="0.045"/>')

        # Glass curtain wall steel mullions (framing the Chicago skyline)
        o.append(f'<rect x="248" y="28" width="694" height="368" fill="none" stroke="#182332" stroke-width="8"/>')
        for mx in (478, 708):
            o.append(f'<rect x="{mx}" y="28" width="11" height="368" fill="#121B28" stroke="{INK}" stroke-width="1.2"/>')
            o.append(f'<path d="M{mx+2},30 L{mx+2},394" fill="none" stroke="#354B66" stroke-width="1.0" opacity="0.55"/>')
        # Horizontal transom bar
        o.append(f'<rect x="252" y="282" width="686" height="7" fill="#121B28" stroke="{INK}" stroke-width="1.0"/>')
        o.append('<path d="M254,284 L936,284" fill="none" stroke="#39526F" stroke-width="0.9" opacity="0.5"/>')
        # Subtle glass reflection bands
        o.append(f'<polygon points="285,32 342,32 276,278 256,278" fill="url(#{p}_glass_glare)"/>')
        o.append(f'<polygon points="512,32 558,32 496,278 486,278" fill="url(#{p}_glass_glare)"/>')
        o.append(f'<polygon points="755,32 820,32 740,278 716,278" fill="url(#{p}_glass_glare)"/>')
        # Right structural column
        o.append(f'<rect x="936" y="0" width="24" height="540" fill="#101824" stroke="{INK}" stroke-width="1.5"/>')

        # --- LEFT WALNUT WOOD WALL (x=0..252) ---
        o.append(f'<rect x="0" y="28" width="252" height="390" fill="url(#{p}_wood_wall)" stroke="{INK}" stroke-width="1.8"/>')
        # Vertical architectural walnut slats + grain
        for wx in range(28, 252, 32):
            o.append(f'<path d="M{wx},28 L{wx},416" fill="none" stroke="#130C08" stroke-width="1.5"/>')
            o.append(f'<path d="M{wx+2},28 L{wx+2},416" fill="none" stroke="#4D3322" stroke-width="0.8" opacity="0.55"/>')
            for g_i in range(2):
                gx = wx - 16 + g_i * 9
                o.append(f'<path d="M{gx},34 Q{gx+4},190 {gx-3},408" fill="none" stroke="#492F1F" stroke-width="0.8" opacity="0.38"/>')

        # Warm wall sconce light above diploma
        o.append(f'<ellipse cx="126" cy="136" rx="115" ry="92" fill="url(#{p}_sconce_glow)"/>')
        # Brass picture light fixture above diploma
        o.append(f'<rect x="86" y="54" width="80" height="8" rx="3" fill="url(#{p}_gold_frame)" stroke="{INK_WARM}" stroke-width="1.1"/>')
        o.append(f'<path d="M106,54 L106,42 L146,42 L146,54" fill="none" stroke="#A67A34" stroke-width="2.2"/>')
        o.append('<rect x="92" y="61" width="68" height="2.4" fill="#FFF3C8" opacity="0.9"/>')

        # --- GOLD-FRAMED DIPLOMA: LOYOLA UNIVERSITY · STRUCTURAL ENGINEERING ---
        # Drop shadow
        o.append('<rect x="34" y="80" width="188" height="142" rx="3" fill="#080504" opacity="0.55"/>')
        # Outer gold frame
        o.append(f'<rect x="28" y="74" width="188" height="142" rx="3" fill="url(#{p}_gold_frame)" stroke="{INK_WARM}" stroke-width="1.8"/>')
        # Inner dark mat board
        o.append('<rect x="38" y="84" width="168" height="122" fill="#1C2736" stroke="#6E4E1E" stroke-width="1.2"/>')
        # Inner gold trim + parchment certificate
        o.append(f'<rect x="46" y="92" width="152" height="106" fill="url(#{p}_parchment)" stroke="#C69A48" stroke-width="1.2"/>')
        o.append('<rect x="50" y="96" width="144" height="98" fill="none" stroke="#8C6D3B" stroke-width="0.7" stroke-dasharray="3,2"/>')
        # University crest emblem at top
        o.append('<circle cx="122" cy="107" r="6.5" fill="#7D2428" stroke="#C59843" stroke-width="1.0"/>')
        o.append('<path d="M119,107 L122,103 L125,107 L122,111 Z" fill="#F2D27E"/>')
        # English Diploma Typography
        o.append('<text x="122" y="124" text-anchor="middle" font-family="Georgia,serif" font-size="10.2" font-weight="bold" fill="#1E1812" letter-spacing="0.8">LOYOLA UNIVERSITY</text>')
        o.append('<text x="122" y="134" text-anchor="middle" font-family="Georgia,serif" font-size="6.4" fill="#5A4732" letter-spacing="1.4">CHICAGO · ILLINOIS</text>')
        o.append('<path d="M68,139 L176,139" fill="none" stroke="#B28C48" stroke-width="0.8"/>')
        o.append('<text x="122" y="150" text-anchor="middle" font-family="Georgia,serif" font-size="7.2" font-style="italic" fill="#463726">Bachelor of Science in</text>')
        o.append('<text x="122" y="163" text-anchor="middle" font-family="Arial,sans-serif" font-size="8.6" font-weight="bold" fill="#162336" letter-spacing="0.5">STRUCTURAL ENGINEERING</text>')
        o.append('<text x="122" y="174" text-anchor="middle" font-family="Georgia,serif" font-size="6.2" fill="#5C4934">MAGNA CUM LAUDE · HONORS</text>')
        # Signature lines + gold/crimson embossed seal
        o.append('<path d="M62,186 L98,186 M142,186 L180,186" fill="none" stroke="#6E5B45" stroke-width="0.7"/>')
        o.append('<path d="M66,184 Q78,179 92,184 M148,184 Q162,178 174,183" fill="none" stroke="#2D3D52" stroke-width="0.8"/>')
        # Seal + ribbons
        o.append('<polygon points="118,187 114,198 120,195" fill="#8C2328"/>')
        o.append('<polygon points="126,187 130,198 124,195" fill="#A82D32"/>')
        o.append('<circle cx="122" cy="185" r="7.2" fill="#D4A646" stroke="#8C631E" stroke-width="1.0"/>')
        o.append('<circle cx="122" cy="185" r="4.6" fill="none" stroke="#FFF0B8" stroke-width="0.7"/>')
        # Subtle glass sheen over diploma
        o.append('<polygon points="46,92 82,92 56,198 46,198" fill="#FFFFFF" opacity="0.14"/>')

        # Bookshelf / structural binders cleanly below diploma (shelf at y=306, no overlap!)
        o.append(f'<rect x="18" y="306" width="212" height="10" fill="#1D120C" stroke="{INK_WARM}" stroke-width="1.2"/>')
        o.append('<path d="M19,307 L229,307" fill="none" stroke="#6E4B32" stroke-width="1.0" opacity="0.6"/>')
        binders = [
            (26, 28, 56, "#1E3A56", "STEEL"),
            (56, 22, 52, "#4B2A23", "AISC"),
            (80, 24, 58, "#263B4D", "CAD-4"),
            (106, 18, 48, "#3B3124", "LOAD"),
            (126, 26, 55, "#193047", "IL-08"),
            (154, 22, 50, "#523523", "CODE"),
        ]
        for bx, bw, bh, bc, lbl in binders:
            by = 306 - bh
            o.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="1.5" fill="{bc}" stroke="{INK_WARM}" stroke-width="1.1"/>')
            o.append(f'<rect x="{bx+3}" y="{by+10}" width="{bw-6}" height="10" fill="#E6DAC2" opacity="0.82"/>')
            o.append(f'<text x="{bx+bw/2:.1f}" y="{by+17.5:.1f}" text-anchor="middle" font-family="Arial,sans-serif" font-size="5.2" font-weight="bold" fill="#18202B">{lbl}</text>')
        # Small structural truss desktop model on right end of shelf
        o.append('<path d="M186,306 L196,274 L206,306 L216,274 L224,306 M186,290 L224,290 M196,274 L216,274" fill="none" stroke="#9EC4DC" stroke-width="1.2" opacity="0.85"/>')

        o.append('</g>')
        parts.append("\n".join(o))

    # -------------------------------------------------------------------------
    # LAYER 3: SAHNE — Foreground Architect Desk, Coffee, Lamp, CAD Monitor, Plans
    # -------------------------------------------------------------------------
    if _katman_aktif(katmanlar, "sahne"):
        s: list[str] = ['<g id="s108-sahne">']
        # Perspective modern walnut & glass architect desk
        s.append(f'<polygon points="0,394 960,378 960,540 0,540" fill="url(#{p}_desk_top)" stroke="{INK_WARM}" stroke-width="2.0"/>')
        s.append(f'<polygon points="0,394 960,378 960,388 0,404" fill="url(#{p}_desk_edge)"/>')
        # Wood grain across desk
        for gy in (420, 448, 476, 506, 528):
            s.append(f'<path d="M0,{gy} Q320,{gy-8} 640,{gy-4} T960,{gy-12}" fill="none" stroke="#4D3322" stroke-width="1.1" opacity="0.42"/>')
        # Warm desk lamp light pool
        s.append(f'<ellipse cx="265" cy="452" rx="260" ry="86" fill="url(#{p}_lamp_pool)"/>')

        # --- ARCHITECT DESK LAMP (left foreground) ---
        s.append(f'<ellipse cx="86" cy="458" rx="34" ry="12" fill="#14181F" stroke="{INK}" stroke-width="1.5"/>')
        s.append('<ellipse cx="86" cy="455" rx="28" ry="8" fill="#2A3340"/>')
        s.append('<path d="M84,452 L56,374 L126,326" fill="none" stroke="#303B4A" stroke-width="5.5" stroke-linecap="round" stroke-linejoin="round"/>')
        s.append('<path d="M84,452 L56,374 L126,326" fill="none" stroke="#7A8FA6" stroke-width="1.4" opacity="0.6" stroke-linecap="round"/>')
        s.append('<circle cx="56" cy="374" r="5" fill="#C69A48" stroke="#18120D" stroke-width="1.1"/>')
        # Lamp shade
        s.append(f'<polygon points="112,318 148,314 166,342 108,348" fill="#1F2B38" stroke="{INK}" stroke-width="1.5"/>')
        s.append('<ellipse cx="137" cy="345" rx="27" ry="6.5" fill="#FFF1C2" opacity="0.92"/>')
        s.append(f'<polygon points="110,348 164,342 295,488 78,488" fill="#FFD98B" opacity="0.11"/>')

        # --- OPEN TECHNICAL SKETCHBOOK + RULER + BLUEPRINT ROLLS (center-left) ---
        # Rolled blueprints behind sketchbook
        for ry, rx0, rx1 in [(404, 212, 396), (414, 224, 412)]:
            s.append(f'<rect x="{rx0}" y="{ry}" width="{rx1-rx0}" height="15" rx="6" fill="#1A446E" stroke="{INK}" stroke-width="1.3"/>')
            s.append(f'<ellipse cx="{rx0+3}" cy="{ry+7.5}" rx="4.5" ry="7.2" fill="#DDF5FF" stroke="{INK}" stroke-width="1.1"/>')
            s.append(f'<ellipse cx="{rx0+3}" cy="{ry+7.5}" rx="2.0" ry="3.4" fill="#112E4D"/>')
            s.append(f'<path d="M{rx0+12},{ry+4} L{rx1-8},{ry+4}" fill="none" stroke="#7FE6FF" stroke-width="0.9" opacity="0.55"/>')

        # Open engineering sketchbook
        s.append('<polygon points="205,436 458,426 488,518 176,528" fill="#EAE2D0" stroke="#1D1712" stroke-width="1.5"/>')
        s.append('<path d="M332,431 L332,523" fill="none" stroke="#8C7E6B" stroke-width="1.6"/>')
        # Blueprint sketch lines inside notebook
        s.append('<path d="M218,454 L314,450 L314,504 L212,508 Z M218,454 L314,504 M314,450 L212,508" fill="none" stroke="#1E5280" stroke-width="1.1" opacity="0.82"/>')
        s.append('<path d="M348,448 L446,444 M348,460 L432,456 M348,474 L452,470 M354,492 L438,488" fill="none" stroke="#364D66" stroke-width="1.0" opacity="0.72"/>')
        # Metallic scale ruler
        s.append('<polygon points="366,488 534,478 538,494 370,504" fill="#C4CED8" stroke="#18202A" stroke-width="1.2"/>')
        for tx in range(378, 528, 12):
            s.append(f'<path d="M{tx},488 L{tx+1},494" fill="none" stroke="#223040" stroke-width="0.9"/>')

        # --- STEAMING CERAMIC COFFEE MUG (center-right foreground) ---
        s.append('<ellipse cx="596" cy="482" rx="34" ry="11" fill="#0A0705" opacity="0.52"/>')
        # Coaster
        s.append('<ellipse cx="592" cy="479" rx="31" ry="10" fill="#4E3422" stroke="#1A110B" stroke-width="1.2"/>')
        # Mug handle
        s.append('<path d="M614,442 C632,442 632,468 612,469" fill="none" stroke="#D5DCE4" stroke-width="4.8" stroke-linecap="round"/>')
        s.append('<path d="M614,442 C632,442 632,468 612,469" fill="none" stroke="#1A2029" stroke-width="1.2" stroke-linecap="round"/>')
        # Mug body
        s.append('<path d="M566,434 L570,474 C570,481 614,481 614,474 L618,434 Z" fill="#DFE5EC" stroke="#18202A" stroke-width="1.5"/>')
        s.append('<path d="M568,438 L571,472 C571,477 586,478 586,474 L584,438 Z" fill="#FFFFFF" opacity="0.38"/>')
        # Dark coffee surface inside rim
        s.append('<ellipse cx="592" cy="434" rx="26" ry="7.2" fill="#EEF3F7" stroke="#18202A" stroke-width="1.3"/>')
        s.append('<ellipse cx="592" cy="435" rx="22" ry="5.2" fill="#2A170D"/>')
        s.append('<path d="M578,434 Q592,431 606,434" fill="none" stroke="#8C5B38" stroke-width="1.1" opacity="0.7"/>')
        # Delicate rising steam wisps
        s.append('<path d="M584,424 C578,412 590,402 584,388" fill="none" stroke="#E8F3FF" stroke-width="1.6" opacity="0.32" stroke-linecap="round"/>')
        s.append('<path d="M598,422 C605,408 594,398 602,382" fill="none" stroke="#E8F3FF" stroke-width="1.4" opacity="0.28" stroke-linecap="round"/>')

        # --- CAD MONITOR / WORKSTATION EDGE (right side of desk) ---
        # Monitor stand
        s.append('<polygon points="782,456 846,456 856,474 772,474" fill="#1C2532" stroke="#0C1118" stroke-width="1.3"/>')
        s.append('<rect x="806" y="424" width="16" height="36" fill="#243040" stroke="#0C1118" stroke-width="1.2"/>')
        # Monitor bezel (slightly angled)
        s.append(f'<polygon points="698,328 928,312 932,442 702,452" fill="#141C27" stroke="{INK}" stroke-width="2.0"/>')
        s.append('<polygon points="708,337 920,322 923,432 711,442" fill="#081626"/>')
        # Live CAD structural truss diagram on screen
        s.append('<path d="M724,420 L724,352 L904,340 L904,412 Z" fill="none" stroke="#7FE6FF" stroke-width="1.2" opacity="0.85"/>')
        s.append('<path d="M724,386 L904,376 M768,349 L768,418 M814,346 L814,416 M860,343 L860,414" fill="none" stroke="#7FE6FF" stroke-width="0.9" opacity="0.6"/>')
        s.append('<path d="M724,420 L768,349 L814,416 L860,343 L904,412" fill="none" stroke="#DDFBFF" stroke-width="1.4" opacity="0.92"/>')
        s.append('<text x="724" y="346" font-family="Consolas,monospace" font-size="8.2" fill="#7FE6FF" font-weight="bold">STRUCTURAL CAD · TRUSS 07</text>')
        s.append('<text x="724" y="432" font-family="Consolas,monospace" font-size="7.2" fill="#8CCAE0">LOAD: 420 kN · SAFETY: 1.85</text>')
        # Keyboard edge
        s.append('<polygon points="664,484 892,470 912,510 676,524" fill="#1A222E" stroke="#0B1017" stroke-width="1.4"/>')
        for ky in (492, 502, 512):
            s.append(f'<path d="M678,{ky} L894,{ky-13}" fill="none" stroke="#36465B" stroke-width="3.2" stroke-dasharray="10,4"/>')

        s.append('</g>')
        parts.append("\n".join(s))

    # -------------------------------------------------------------------------
    # LAYER 4: PLAN — Live #7FE6FF CAD Wireframe Dissolve Over Chicago Skyline
    # -------------------------------------------------------------------------
    if _katman_aktif(katmanlar, "plan"):
        pl: list[str] = ['<g id="s108-plan">']
        pl.append(f'<g clip-path="url(#{p}_win_clip)">')
        # John Hancock X-bracing CAD overlay (right half & upper structure)
        pl.append(f'<polygon points="602,320 618,96 668,96 684,320" fill="none" stroke="{PLAN}" stroke-width="1.5" opacity="0.88" filter="url(#{p}_glow_cyan)"/>')
        tiers = [(96, 140), (140, 186), (186, 232), (232, 278), (278, 320)]
        for y0, y1 in tiers:
            t0 = (y0 - 96) / 224.0
            t1 = (y1 - 96) / 224.0
            xl0, xr0 = 618 - t0 * 16, 668 + t0 * 16
            xl1, xr1 = 618 - t1 * 16, 668 + t1 * 16
            pl.append(f'<path d="M{xl0:.1f},{y0} L{xr0:.1f},{y0} M{xl0:.1f},{y0} L{xr1:.1f},{y1} M{xr0:.1f},{y0} L{xl1:.1f},{y1}" fill="none" stroke="{PLAN}" stroke-width="1.2" opacity="0.82"/>')

        # Right skyscrapers pure CAD steel lattice
        cad_towers = [
            (712, 148, 64, 172, 6),
            (802, 118, 52, 202, 7),
            (872, 162, 46, 158, 5),
        ]
        for tx, ty, tw, th, floors in cad_towers:
            pl.append(f'<rect x="{tx}" y="{ty}" width="{tw}" height="{th}" fill="none" stroke="{PLAN}" stroke-width="1.35" opacity="0.85"/>')
            pl.append(f'<path d="M{tx+tw/2:.1f},{ty} L{tx+tw/2:.1f},{ty+th}" fill="none" stroke="{PLAN}" stroke-width="0.9" opacity="0.6"/>')
            step_h = th / floors
            for fi in range(floors):
                fy0 = ty + fi * step_h
                fy1 = fy0 + step_h
                pl.append(f'<path d="M{tx},{fy0:.1f} L{tx+tw},{fy0:.1f} M{tx},{fy0:.1f} L{tx+tw},{fy1:.1f}" fill="none" stroke="{PLAN}" stroke-width="0.85" opacity="0.58"/>')
        # Roof spire CAD triangle on 712 tower
        pl.append(f'<path d="M712,148 L744,126 L776,148 M744,126 L744,98" fill="none" stroke="{PLAN_CORE}" stroke-width="1.2" opacity="0.9"/>')

        # CAD dimension lines, structural callouts & stress nodes
        pl.append(f'<path d="M618,76 L668,76 M618,70 L618,86 M668,70 L668,86" fill="none" stroke="{PLAN}" stroke-width="1.0" opacity="0.8"/>')
        pl.append(f'<path d="M584,96 L584,320 M578,96 L592,96 M578,320 L592,320" fill="none" stroke="{PLAN}" stroke-width="0.9" stroke-dasharray="4,3" opacity="0.72"/>')
        pl.append(f'<text x="580" y="210" text-anchor="end" font-family="Consolas,monospace" font-size="8.5" fill="{PLAN}" opacity="0.92">EL +344m</text>')
        pl.append(f'<text x="643" y="71" text-anchor="middle" font-family="Consolas,monospace" font-size="8.2" fill="{PLAN_CORE}" font-weight="bold">GRID B-4</text>')
        pl.append(f'<text x="828" y="109" text-anchor="middle" font-family="Consolas,monospace" font-size="8.0" fill="{PLAN}">F = 420 kN</text>')
        pl.append(f'<path d="M430,52 L456,52" fill="none" stroke="{PLAN}" stroke-width="0.9" opacity="0.8"/>')
        pl.append(f'<text x="460" y="55" font-family="Consolas,monospace" font-size="8.0" fill="{PLAN}" opacity="0.88">EL +442m · WILLIS</text>')
        # Highlight nodes
        for nx, ny in [(618, 96), (668, 96), (643, 186), (744, 126), (802, 118), (854, 118)]:
            pl.append(f'<circle cx="{nx}" cy="{ny}" r="3.4" fill="none" stroke="{PLAN_CORE}" stroke-width="1.2"/>')
            pl.append(f'<circle cx="{nx}" cy="{ny}" r="1.4" fill="{PLAN_CORE}"/>')

        pl.append('</g>')
        pl.append('</g>')
        parts.append("\n".join(pl))

    # -------------------------------------------------------------------------
    # LAYER 5: ONPLAN — Vignette, Dust Motes & Subtle Technical Corner Tag
    # -------------------------------------------------------------------------
    if _katman_aktif(katmanlar, "onplan"):
        op_l: list[str] = ['<g id="s108-onplan">']
        # Warm floating dust motes near lamp
        for _ in range(18):
            dx = rng.uniform(75, 340)
            dy = rng.uniform(290, 485)
            op_l.append(f'<circle cx="{dx:.1f}" cy="{dy:.1f}" r="{rng.uniform(0.8,1.8):.1f}" fill="#FFE7B0" opacity="{rng.uniform(0.18,0.48):.2f}"/>')
        # Vignette
        op_l.append(f'<rect x="0" y="0" width="960" height="540" fill="url(#{p}_vignette)"/>')
        # Subtle HUD corner stamp (English)
        op_l.append(f'<path d="M24,514 L24,522 L38,522 M936,514 L936,522 L922,522" fill="none" stroke="{PLAN}" stroke-width="1.2" opacity="0.55"/>')
        op_l.append(f'<text x="46" y="522" font-family="Consolas,monospace" font-size="9.5" fill="{PLAN}" opacity="0.72" letter-spacing="1.4">CHICAGO · STRUCTURAL ENGINEER</text>')
        op_l.append('</g>')
        parts.append("\n".join(op_l))

    return defs, "\n".join(parts)


# =============================================================================
# SCENE 1.09: ARCHITECT'S DRAFTING TABLE ("FOX RIVER")
# =============================================================================
def set_109_taslak_masasi(
    katmanlar: set[str] | list[str] | None = None,
) -> tuple[str, str]:
    """Top-down angled architect's drafting table bathed in warm amber lamp light.
    Rich wood grain surface, sticky notes, T-square, brass compass, drafting pens,
    coffee cup ring, and centerpiece multi-wing FOX RIVER STATE PENITENTIARY blueprint
    with locked Origami Crane v4 (K.turna) resting in the heart of the plan.
    """
    rng = random.Random(109)
    p = _uid("s109")

    defs = f"""
    <linearGradient id="{p}_wood_bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#4A3222"/>
      <stop offset="42%" stop-color="#362317"/>
      <stop offset="80%" stop-color="#251810"/>
      <stop offset="100%" stop-color="#170F0A"/>
    </linearGradient>
    <linearGradient id="{p}_bp_paper" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#134570"/>
      <stop offset="48%" stop-color="#0E365B"/>
      <stop offset="100%" stop-color="#092440"/>
    </linearGradient>
    <linearGradient id="{p}_bp_fold" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#000000" stop-opacity="0.0"/>
      <stop offset="48%" stop-color="#04101D" stop-opacity="0.34"/>
      <stop offset="52%" stop-color="#7FE6FF" stop-opacity="0.16"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.0"/>
    </linearGradient>
    <radialGradient id="{p}_amber_lamp" cx="0.34" cy="0.32" r="0.62">
      <stop offset="0%" stop-color="#FFE6A8" stop-opacity="0.40"/>
      <stop offset="36%" stop-color="#F0A948" stop-opacity="0.19"/>
      <stop offset="72%" stop-color="#B86B22" stop-opacity="0.06"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.0"/>
    </radialGradient>
    <linearGradient id="{p}_brass" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FCE4A0"/>
      <stop offset="45%" stop-color="#C2903A"/>
      <stop offset="100%" stop-color="#6F4C19"/>
    </linearGradient>
    <linearGradient id="{p}_steel" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#E5EDF5"/>
      <stop offset="50%" stop-color="#9EB0C2"/>
      <stop offset="100%" stop-color="#58697B"/>
    </linearGradient>
    <radialGradient id="{p}_vignette" cx="0.48" cy="0.48" r="0.66">
      <stop offset="56%" stop-color="#000000" stop-opacity="0.0"/>
      <stop offset="100%" stop-color="#060403" stop-opacity="0.72"/>
    </radialGradient>
    <filter id="{p}_glow_cyan" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="2.5" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="{p}_shadow_soft" x="-15%" y="-15%" width="130%" height="130%">
      <feGaussianBlur stdDeviation="4.0" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    """

    parts: list[str] = []

    # -------------------------------------------------------------------------
    # LAYER 1: UZAK — Wood-Grained Architect Drafting Table Surface
    # -------------------------------------------------------------------------
    if _katman_aktif(katmanlar, "uzak"):
        u: list[str] = ['<g id="s109-uzak">']
        u.append(f'<rect x="0" y="0" width="960" height="540" fill="url(#{p}_wood_bg)"/>')
        # Horizontal drafting table wood planks & rich grain
        plank_ys = [0, 74, 152, 234, 316, 398, 474, 540]
        for i in range(len(plank_ys) - 1):
            y0, y1 = plank_ys[i], plank_ys[i + 1]
            tint = ["#3D281B", "#312015", "#432D1E", "#2C1C12"][i % 4]
            u.append(f'<rect x="0" y="{y0}" width="960" height="{y1-y0}" fill="{tint}" opacity="0.38"/>')
            u.append(f'<path d="M0,{y1} L960,{y1}" fill="none" stroke="#160E09" stroke-width="1.8"/>')
            u.append(f'<path d="M0,{y1+2} L960,{y1+2}" fill="none" stroke="#5A3D29" stroke-width="0.8" opacity="0.45"/>')
            # Grain curves
            for g in range(4):
                gy = y0 + 12 + g * 16 + rng.uniform(-3, 3)
                u.append(
                    f'<path d="M0,{gy:.1f} C240,{gy+rng.uniform(-7,7):.1f} 620,{gy+rng.uniform(-7,7):.1f} 960,{gy+rng.uniform(-4,4):.1f}" '
                    f'fill="none" stroke="#5C3E2A" stroke-width="0.9" opacity="0.32"/>'
                )
        # Coffee cup ring stain on top-right wood surface
        u.append('<g transform="translate(868,82)">')
        u.append('<circle cx="0" cy="0" r="28" fill="none" stroke="#1C0F08" stroke-width="3.2" opacity="0.42"/>')
        u.append('<circle cx="1.5" cy="1" r="26.5" fill="none" stroke="#3D2212" stroke-width="1.4" opacity="0.35"/>')
        u.append('<circle cx="18" cy="24" r="3.2" fill="#23130A" opacity="0.35"/>')
        u.append('</g>')
        u.append('</g>')
        parts.append("\n".join(u))

    # -------------------------------------------------------------------------
    # LAYER 2: ORTA — Sticky Notes, T-Square, Set Square, Secondary Sketches
    # -------------------------------------------------------------------------
    if _katman_aktif(katmanlar, "orta"):
        o: list[str] = ['<g id="s109-orta">']
        # Left pinned yellow/cream engineering note cards
        notes = [
            (28, 128, -5.5, "#EFE2B4", "GUARD SHIFT", "02:15 AM · 14 MIN"),
            (22, 232, 3.2, "#E6D8AE", "PIPE SHAFT", "18\" CAST IRON"),
            (30, 344, -2.8, "#F2E6BE", "INFIRMARY", "WINDOW BARS"),
        ]
        for nx, ny, rot, ncol, h1, h2 in notes:
            o.append(f'<g transform="translate({nx},{ny}) rotate({rot})">')
            o.append('<rect x="3" y="4" width="114" height="74" rx="2" fill="#0B0705" opacity="0.48"/>')
            o.append(f'<rect x="0" y="0" width="114" height="74" rx="2" fill="{ncol}" stroke="#8C7B5A" stroke-width="1.0"/>')
            o.append('<rect x="42" y="-6" width="30" height="12" fill="#D5C8A6" opacity="0.72" stroke="#8C7E63" stroke-width="0.6"/>')
            o.append(f'<text x="10" y="24" font-family="Consolas,monospace" font-size="9.2" font-weight="bold" fill="#221A12">{h1}</text>')
            o.append('<path d="M10,30 L102,30" fill="none" stroke="#B59E76" stroke-width="0.9"/>')
            o.append(f'<text x="10" y="46" font-family="Consolas,monospace" font-size="8.0" fill="#4B3828">{h2}</text>')
            o.append('<path d="M10,56 L84,56 M10,64 L66,64" fill="none" stroke="#8C7B63" stroke-width="1.0" opacity="0.65"/>')
            o.append('</g>')

        # Right side small structural sketch card + brass paperclip
        o.append('<g transform="translate(822,162) rotate(4.2)">')
        o.append('<rect x="4" y="5" width="112" height="128" fill="#090604" opacity="0.5"/>')
        o.append('<rect x="0" y="0" width="112" height="128" fill="#E8DFC8" stroke="#7A6D57" stroke-width="1.1"/>')
        o.append('<text x="10" y="18" font-family="Consolas,monospace" font-size="8.2" font-weight="bold" fill="#1C2E42">HEX BOLT #7</text>')
        # Small technical bolt sketch
        o.append('<polygon points="56,34 74,44 74,64 56,74 38,64 38,44" fill="none" stroke="#1E4B72" stroke-width="1.4"/>')
        o.append('<circle cx="56" cy="54" r="10" fill="none" stroke="#1E4B72" stroke-width="1.1"/>')
        o.append('<path d="M24,54 L88,54 M56,26 L56,82" fill="none" stroke="#4D7FA8" stroke-width="0.7" stroke-dasharray="3,2"/>')
        o.append('<text x="10" y="98" font-family="Consolas,monospace" font-size="7.4" fill="#3A4B5C">SINK ANCHOR</text>')
        o.append('<text x="10" y="112" font-family="Consolas,monospace" font-size="7.4" fill="#8C2B2B">CRITICAL NODE</text>')
        o.append('</g>')

        # Wooden + Steel T-Square along bottom edge
        o.append('<g transform="translate(0,488)">')
        o.append('<rect x="0" y="5" width="760" height="24" fill="#080503" opacity="0.55"/>')
        # T-head on left
        o.append('<rect x="12" y="-34" width="28" height="84" rx="3" fill="#2B1B11" stroke="#0F0906" stroke-width="1.4"/>')
        o.append('<circle cx="26" cy="14" r="3.2" fill="#C69A48"/>')
        # Steel blade
        o.append(f'<rect x="40" y="2" width="714" height="24" fill="url(#{p}_steel)" stroke="{INK}" stroke-width="1.3"/>')
        for tx in range(56, 744, 16):
            h_tick = 9 if (tx - 56) % 64 == 0 else 5
            o.append(f'<path d="M{tx},2 L{tx},{2+h_tick}" fill="none" stroke="#1B2530" stroke-width="0.9"/>')
        o.append('<text x="640" y="20" font-family="Consolas,monospace" font-size="8.0" fill="#1E2B38" font-weight="bold">ARCHITECTURAL SCALE 1:250</text>')
        o.append('</g>')

        o.append('</g>')
        parts.append("\n".join(o))

    # -------------------------------------------------------------------------
    # LAYER 3: SAHNE — FOX RIVER STATE PENITENTIARY Blueprint + Compass + Pens + Crane v4
    # -------------------------------------------------------------------------
    if _katman_aktif(katmanlar, "sahne"):
        s: list[str] = ['<g id="s109-sahne">']

        # --- MAIN BLUEPRINT SHEET (x=154..806, y=46..470) ---
        s.append('<rect x="160" y="53" width="654" height="422" rx="2" fill="#060403" opacity="0.62"/>')
        s.append(f'<rect x="154" y="46" width="654" height="422" rx="2" fill="url(#{p}_bp_paper)" stroke="#091C30" stroke-width="1.8"/>')
        # Outer white technical border & double frame
        s.append('<rect x="166" y="58" width="630" height="398" fill="none" stroke="#A8E8FF" stroke-width="1.4" opacity="0.82"/>')
        s.append('<rect x="171" y="63" width="620" height="388" fill="none" stroke="#7FE6FF" stroke-width="0.7" opacity="0.52"/>')

        # Blueprint architectural coordinate grid
        for gx in range(210, 785, 48):
            s.append(f'<path d="M{gx},64 L{gx},450" fill="none" stroke="#5BBCE0" stroke-width="0.5" opacity="0.22"/>')
        for gy in range(96, 445, 44):
            s.append(f'<path d="M172,{gy} L790,{gy}" fill="none" stroke="#5BBCE0" stroke-width="0.5" opacity="0.22"/>')
        # Grid labels (A-F, 1-5)
        for idx, gl in enumerate(["A", "B", "C", "D", "E", "F"]):
            gx = 210 + idx * 96
            s.append(f'<circle cx="{gx}" cy="74" r="6.5" fill="none" stroke="#7FE6FF" stroke-width="0.8" opacity="0.65"/>')
            s.append(f'<text x="{gx}" y="77" text-anchor="middle" font-family="Consolas,monospace" font-size="7.5" fill="#A8ECFF">{gl}</text>')

        # --- ARCHITECTURAL FLOOR PLAN: FOX RIVER STATE PENITENTIARY ---
        # Outer Perimeter Security Wall + Corner Watchtowers (TOWER 1..4)
        s.append('<rect x="196" y="96" width="568" height="296" fill="none" stroke="#DDFBFF" stroke-width="2.4" opacity="0.88"/>')
        s.append('<rect x="202" y="102" width="556" height="284" fill="none" stroke="#7FE6FF" stroke-width="0.9" stroke-dasharray="6,4" opacity="0.55"/>')
        for tx, ty, tlbl in [(196, 96, "T-1"), (764, 96, "T-2"), (196, 392, "T-3"), (764, 392, "T-4")]:
            s.append(f'<rect x="{tx-10}" y="{ty-10}" width="20" height="20" fill="#0B2E4F" stroke="#DDFBFF" stroke-width="1.5"/>')
            s.append(f'<path d="M{tx-10},{ty-10} L{tx+10},{ty+10} M{tx+10},{ty-10} L{tx-10},{ty+10}" fill="none" stroke="#7FE6FF" stroke-width="0.7" opacity="0.7"/>')
            s.append(f'<text x="{tx}" y="{ty-14 if ty<200 else ty+21}" text-anchor="middle" font-family="Consolas,monospace" font-size="7.5" fill="#A8ECFF">{tlbl}</text>')

        # WING A (Left cellblock — detailed cells + central corridor)
        s.append('<rect x="218" y="122" width="144" height="236" fill="#0A2946" stroke="#C5F4FF" stroke-width="1.8"/>')
        s.append('<rect x="266" y="122" width="48" height="236" fill="#0E385E" stroke="#7FE6FF" stroke-width="1.0"/>')
        for cy in range(138, 348, 22):
            s.append(f'<path d="M218,{cy} L266,{cy} M314,{cy} L362,{cy}" fill="none" stroke="#8FE4FF" stroke-width="0.9" opacity="0.75"/>')
            # Tiny cell doors (swing arcs)
            s.append(f'<path d="M266,{cy+6} Q273,{cy+6} 273,{cy+13}" fill="none" stroke="#7FE6FF" stroke-width="0.7" opacity="0.65"/>')
            s.append(f'<path d="M314,{cy+6} Q307,{cy+6} 307,{cy+13}" fill="none" stroke="#7FE6FF" stroke-width="0.7" opacity="0.65"/>')
        s.append('<text x="290" y="116" text-anchor="middle" font-family="Consolas,monospace" font-size="10.5" font-weight="bold" fill="#E3FCFF" letter-spacing="1.2">WING A</text>')
        s.append('<text x="290" y="372" text-anchor="middle" font-family="Consolas,monospace" font-size="7.5" fill="#8CDDF5">CELL BLOCK 40</text>')

        # CENTRAL YARD (center — open courtyard + guard booth + underground tunnel lines)
        s.append('<rect x="386" y="130" width="188" height="220" fill="#08243E" stroke="#8CE4FF" stroke-width="1.4" stroke-dasharray="5,3"/>')
        s.append('<circle cx="480" cy="240" r="56" fill="none" stroke="#7FE6FF" stroke-width="1.0" opacity="0.5"/>')
        s.append('<circle cx="480" cy="240" r="76" fill="none" stroke="#7FE6FF" stroke-width="0.7" stroke-dasharray="3,3" opacity="0.4"/>')
        s.append('<text x="480" y="148" text-anchor="middle" font-family="Consolas,monospace" font-size="10.5" font-weight="bold" fill="#DDFBFF" letter-spacing="1.5">YARD</text>')
        # Sub-ground PIPES network across yard & wing A
        s.append('<path d="M290,260 L404,260 L404,316 L602,316 L602,226 L654,226" fill="none" stroke="#7FE6FF" stroke-width="2.0" stroke-dasharray="7,4" opacity="0.75"/>')
        s.append('<text x="518" y="336" text-anchor="middle" font-family="Consolas,monospace" font-size="9.2" font-weight="bold" fill="#7FE6FF" letter-spacing="1.1">PIPES · SUB-LEVEL B2</text>')

        # INFIRMARY (Right wing — exam rooms, corridor, exterior wall window)
        s.append('<rect x="598" y="122" width="144" height="146" fill="#0B2E4E" stroke="#C5F4FF" stroke-width="1.8"/>')
        s.append('<path d="M598,176 L742,176 M652,122 L652,268 M702,176 L702,268" fill="none" stroke="#8FE4FF" stroke-width="1.0" opacity="0.8"/>')
        # Medical cross symbol
        s.append('<path d="M624,142 L624,158 M616,150 L632,150" fill="none" stroke="#DDFBFF" stroke-width="2.2"/>')
        s.append('<text x="670" y="116" text-anchor="middle" font-family="Consolas,monospace" font-size="10.5" font-weight="bold" fill="#E3FCFF" letter-spacing="1.2">INFIRMARY</text>')
        # Admin / Gatehouse below Infirmary
        s.append('<rect x="598" y="286" width="144" height="72" fill="#092744" stroke="#8CE4FF" stroke-width="1.3"/>')
        s.append('<path d="M648,286 L648,358 M696,286 L696,358" fill="none" stroke="#7FE6FF" stroke-width="0.9" opacity="0.7"/>')
        s.append('<text x="670" y="326" text-anchor="middle" font-family="Consolas,monospace" font-size="8.2" fill="#9EE6FC">GATEHOUSE · ADMIN</text>')

        # Blueprint Title Block (bottom band inside frame)
        s.append('<rect x="171" y="406" width="620" height="45" fill="#08213A" stroke="#A8E8FF" stroke-width="1.2"/>')
        s.append('<path d="M562,406 L562,451 M692,406 L692,451" fill="none" stroke="#7FE6FF" stroke-width="1.0"/>')
        s.append('<text x="186" y="427" font-family="Arial,sans-serif" font-size="13.5" font-weight="bold" fill="#EBFBFF" letter-spacing="1.1">FOX RIVER STATE PENITENTIARY</text>')
        s.append('<text x="186" y="443" font-family="Consolas,monospace" font-size="8.6" fill="#7FE6FF" letter-spacing="0.9">RENOVATION BLUEPRINT · STRUCTURAL &amp; UTILITY PLAN · REV 4B</text>')
        s.append('<text x="574" y="424" font-family="Consolas,monospace" font-size="7.6" fill="#9CDDF2">ENGINEER: M. SCOFIELD</text>')
        s.append('<text x="574" y="439" font-family="Consolas,monospace" font-size="7.6" fill="#9CDDF2">JOLIET, ILLINOIS</text>')
        s.append('<text x="741" y="425" text-anchor="middle" font-family="Consolas,monospace" font-size="8.2" font-weight="bold" fill="#DDFBFF">SCALE 1:250</text>')
        s.append('<text x="741" y="440" text-anchor="middle" font-family="Consolas,monospace" font-size="7.4" fill="#7FE6FF">SHEET 04 OF 12</text>')

        # Subtle vertical fold crease across center of blueprint
        s.append(f'<rect x="466" y="46" width="28" height="422" fill="url(#{p}_bp_fold)"/>')

        # Corner brass paperweights & masking tape strips holding the blueprint
        for tx, ty, rot in [(156, 48, -36), (804, 48, 38), (156, 466, 35)]:
            s.append(f'<g transform="translate({tx},{ty}) rotate({rot})">')
            s.append('<rect x="-24" y="-8" width="48" height="16" fill="#DFD1AC" opacity="0.78" stroke="#9C8B67" stroke-width="0.7"/>')
            s.append('</g>')
        # Heavy cylindrical brass paperweight (bottom-right corner)
        s.append('<circle cx="792" cy="454" r="21" fill="#070504" opacity="0.52"/>')
        s.append(f'<circle cx="788" cy="450" r="19" fill="url(#{p}_brass)" stroke="{INK_WARM}" stroke-width="1.4"/>')
        s.append('<circle cx="788" cy="450" r="12" fill="none" stroke="#FFF1C2" stroke-width="1.0" opacity="0.65"/>')

        # --- BRASS ARCHITECTURAL COMPASS (top-right on blueprint edge) ---
        s.append('<g transform="translate(724,132) rotate(28)">')
        # Shadow
        s.append('<path d="M4,6 L-26,114 M4,6 L34,112" fill="none" stroke="#050C15" stroke-width="6" opacity="0.45" stroke-linecap="round"/>')
        # Compass legs (brass)
        s.append(f'<path d="M0,0 L-28,108" fill="none" stroke="url(#{p}_brass)" stroke-width="5.2" stroke-linecap="round"/>')
        s.append(f'<path d="M0,0 L30,106" fill="none" stroke="url(#{p}_brass)" stroke-width="5.2" stroke-linecap="round"/>')
        # Steel needle tips
        s.append('<path d="M-28,108 L-31,122 M30,106 L33,120" fill="none" stroke="#E2ECF5" stroke-width="2.0" stroke-linecap="round"/>')
        # Adjustment crossbar & wheel
        s.append('<path d="M-16,58 L18,58" fill="none" stroke="#D5A64E" stroke-width="2.6"/>')
        s.append('<circle cx="1" cy="58" r="5.5" fill="#F2D27E" stroke="#4D3512" stroke-width="1.1"/>')
        # Top hinge & handle
        s.append(f'<circle cx="0" cy="0" r="8.5" fill="url(#{p}_brass)" stroke="{INK_WARM}" stroke-width="1.3"/>')
        s.append('<rect x="-2.5" y="-20" width="5" height="14" rx="2" fill="#C7963E" stroke="#36240B" stroke-width="1.0"/>')
        s.append('</g>')

        # --- TECHNICAL DRAFTING PENS (right side of desk) ---
        for px, py, rot, pcol, trim in [(854, 344, -14, "#1C232D", "#C89B45"), (886, 356, -8, "#25415E", "#DCE6F0"), (914, 368, -20, "#7C242A", "#E5C272")]:
            s.append(f'<g transform="translate({px},{py}) rotate({rot})">')
            s.append('<rect x="3" y="4" width="11" height="132" rx="4" fill="#070503" opacity="0.48"/>')
            s.append(f'<rect x="0" y="0" width="10" height="122" rx="3" fill="{pcol}" stroke="{INK}" stroke-width="1.1"/>')
            s.append(f'<rect x="0" y="24" width="10" height="6" fill="{trim}"/>')
            s.append(f'<polygon points="0,122 10,122 5,136" fill="{trim}" stroke="{INK}" stroke-width="0.9"/>')
            s.append('<path d="M5,136 L5,142" fill="none" stroke="#11161D" stroke-width="1.2"/>')
            s.append('</g>')

        # --- LOCKED ORIGAMI CRANE v4 (K.turna) AT THE HEART OF THE FOX RIVER PLAN ---
        s.append('<g transform="translate(480,236) rotate(-8)">')
        s.append('<ellipse cx="6" cy="36" rx="54" ry="15" fill="#04101D" opacity="0.52"/>')
        s.append(K.turna(s=0.52, isik=0.78, kanat=0.05, kagit="#F8F1E1", golge=True))
        s.append('</g>')

        s.append('</g>')
        parts.append("\n".join(s))

    # -------------------------------------------------------------------------
    # LAYER 4: PLAN — Glowing #7FE6FF Escape Route Overlay on Blueprint
    # -------------------------------------------------------------------------
    if _katman_aktif(katmanlar, "plan"):
        pl: list[str] = ['<g id="s109-plan">']
        # Highlighted cyan escape vector: WING A -> PIPES -> INFIRMARY -> EXTERIOR WALL
        pl.append(
            f'<path d="M290,260 L404,260 L404,316 L602,316 L602,226 L742,226 L782,226" '
            f'fill="none" stroke="{PLAN}" stroke-width="3.2" opacity="0.92" filter="url(#{p}_glow_cyan)"/>'
        )
        pl.append(
            f'<path d="M290,260 L404,260 L404,316 L602,316 L602,226 L742,226 L782,226" '
            f'fill="none" stroke="{PLAN_CORE}" stroke-width="1.2" stroke-dasharray="8,5" opacity="0.95"/>'
        )
        # Route nodes & callouts (positioned cleanly without overlapping grid lines)
        nodes = [
            (290, 260, 290, 246, "01 · CELL 40"),
            (404, 316, 404, 302, "02 · PIPE ACCESS"),
            (602, 226, 652, 212, "03 · INFIRMARY"),
            (764, 226, 764, 212, "EXIT"),
        ]
        for nx, ny, lx, ly, lbl in nodes:
            pl.append(f'<circle cx="{nx}" cy="{ny}" r="6.5" fill="none" stroke="{PLAN}" stroke-width="1.6" filter="url(#{p}_glow_cyan)"/>')
            pl.append(f'<circle cx="{nx}" cy="{ny}" r="2.5" fill="{PLAN_CORE}"/>')
            pl.append(f'<text x="{lx}" y="{ly}" text-anchor="middle" font-family="Consolas,monospace" font-size="8.0" font-weight="bold" fill="{PLAN_CORE}">{lbl}</text>')
        # Target reticle around the Crane
        pl.append(f'<circle cx="480" cy="240" r="64" fill="none" stroke="{PLAN}" stroke-width="0.9" stroke-dasharray="6,6" opacity="0.55"/>')
        pl.append('</g>')
        parts.append("\n".join(pl))

    # -------------------------------------------------------------------------
    # LAYER 5: ONPLAN — Articulated Architect Desk Lamp Head, Amber Pool & Vignette
    # -------------------------------------------------------------------------
    if _katman_aktif(katmanlar, "onplan"):
        op_l: list[str] = ['<g id="s109-onplan">']
        # Warm amber lamp light pool across table & blueprint
        op_l.append(f'<rect x="0" y="0" width="960" height="540" fill="url(#{p}_amber_lamp)"/>')
        # Articulated desk lamp arm & shade entering from top-left corner
        op_l.append('<path d="M-12,32 L78,66 L128,44" fill="none" stroke="#181F29" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>')
        op_l.append('<path d="M-12,32 L78,66 L128,44" fill="none" stroke="#5D6F82" stroke-width="2.2" opacity="0.6" stroke-linecap="round"/>')
        op_l.append('<circle cx="78" cy="66" r="7.5" fill="#C5963E" stroke="#14100C" stroke-width="1.4"/>')
        # Vintage green/brass banker-architect lamp shade
        op_l.append(f'<path d="M108,22 C136,12 174,26 184,56 L138,88 C114,72 100,46 108,22 Z" fill="#183A32" stroke="{INK}" stroke-width="1.8"/>')
        op_l.append('<path d="M138,88 L184,56" fill="none" stroke="#FFF2C4" stroke-width="3.2" opacity="0.95"/>')
        op_l.append('<polygon points="138,88 184,56 385,220 215,285" fill="#FFE29A" opacity="0.10"/>')
        # Vignette
        op_l.append(f'<rect x="0" y="0" width="960" height="540" fill="url(#{p}_vignette)"/>')
        op_l.append('</g>')
        parts.append("\n".join(op_l))

    return defs, "\n".join(parts)


# =============================================================================
# SCENE 1.10: DEATH ROW FRONT PAGE ("DEATH ROW")
# =============================================================================
def set_110_idam_manset(
    katmanlar: set[str] | list[str] | None = None,
) -> tuple[str, str]:
    """Same Fox River drafting table shifted into cold-steel & crimson tension lighting.
    Dramatic prison-bar shadows slash across the blueprint and a slightly crumpled
    THE CHICAGO CHRONICLE front page slammed onto the desk:
    DEATH ROW / LINCOLN BURROWS SENTENCED TO DIE — FOX RIVER
    featuring locked Lincoln v1 (K.lincoln_kafa('front', 'odak', boyun=True)),
    coffee stain, red tension glow, and subtle cyan blueprint pulse underneath.
    """
    rng = random.Random(110)
    p = _uid("s110")

    defs = f"""
    <linearGradient id="{p}_dark_wood" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#1A1514"/>
      <stop offset="55%" stop-color="#101218"/>
      <stop offset="100%" stop-color="#080A0F"/>
    </linearGradient>
    <linearGradient id="{p}_bp_dark" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0B2742"/>
      <stop offset="100%" stop-color="#061628"/>
    </linearGradient>
    <linearGradient id="{p}_newsprint" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ECE4D2"/>
      <stop offset="48%" stop-color="#DED5C0"/>
      <stop offset="100%" stop-color="#C8BEAA"/>
    </linearGradient>
    <linearGradient id="{p}_crease_h" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#000000" stop-opacity="0.0"/>
      <stop offset="46%" stop-color="#221C14" stop-opacity="0.26"/>
      <stop offset="53%" stop-color="#FFFDF5" stop-opacity="0.34"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.0"/>
    </linearGradient>
    <linearGradient id="{p}_photo_bg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#2F3B46"/>
      <stop offset="100%" stop-color="#192129"/>
    </linearGradient>
    <radialGradient id="{p}_red_glow" cx="0.86" cy="0.16" r="0.54">
      <stop offset="0%" stop-color="#FF2E43" stop-opacity="0.46"/>
      <stop offset="42%" stop-color="#B81628" stop-opacity="0.18"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.0"/>
    </radialGradient>
    <radialGradient id="{p}_cold_key" cx="0.32" cy="0.42" r="0.55">
      <stop offset="0%" stop-color="#B8DCFF" stop-opacity="0.18"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.0"/>
    </radialGradient>
    <radialGradient id="{p}_vignette" cx="0.5" cy="0.5" r="0.64">
      <stop offset="52%" stop-color="#000000" stop-opacity="0.0"/>
      <stop offset="100%" stop-color="#040508" stop-opacity="0.78"/>
    </radialGradient>
    <filter id="{p}_glow_red" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="4.0" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="{p}_glow_cyan" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="2.4" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <clipPath id="{p}_lincoln_clip">
      <rect x="0" y="0" width="166" height="194"/>
    </clipPath>
    """

    parts: list[str] = []

    # -------------------------------------------------------------------------
    # LAYER 1: UZAK — Darkened Drafting Table & Fox River Blueprint Underneath
    # -------------------------------------------------------------------------
    if _katman_aktif(katmanlar, "uzak"):
        u: list[str] = ['<g id="s110-uzak">']
        u.append(f'<rect x="0" y="0" width="960" height="540" fill="url(#{p}_dark_wood)"/>')
        # Subtle dark wood planks
        for py in range(68, 540, 78):
            u.append(f'<path d="M0,{py} L960,{py}" fill="none" stroke="#06080C" stroke-width="1.6"/>')
            u.append(f'<path d="M0,{py+2} L960,{py+2}" fill="none" stroke="#252832" stroke-width="0.7" opacity="0.4"/>')

        # Fox River Blueprint visible underneath the slammed newspaper (visual continuity with 1.09!)
        u.append(f'<rect x="74" y="34" width="812" height="474" fill="url(#{p}_bp_dark)" stroke="#05101D" stroke-width="1.8"/>')
        u.append('<rect x="88" y="48" width="784" height="446" fill="none" stroke="#4FA6CC" stroke-width="1.2" opacity="0.55"/>')
        # Grid & partial architectural lines peeking out around newspaper
        for gx in range(130, 860, 56):
            u.append(f'<path d="M{gx},48 L{gx},494" fill="none" stroke="#3F8EB2" stroke-width="0.6" opacity="0.22"/>')
        for gy in range(88, 480, 52):
            u.append(f'<path d="M88,{gy} L872,{gy}" fill="none" stroke="#3F8EB2" stroke-width="0.6" opacity="0.22"/>')
        # Left peeking Wing A cells
        u.append('<rect x="108" y="88" width="124" height="296" fill="none" stroke="#7FE6FF" stroke-width="1.4" opacity="0.45"/>')
        for cy in range(112, 376, 26):
            u.append(f'<path d="M108,{cy} L164,{cy}" fill="none" stroke="#7FE6FF" stroke-width="0.9" opacity="0.38"/>')
        u.append('<text x="118" y="78" font-family="Consolas,monospace" font-size="10.0" fill="#7FE6FF" opacity="0.62">FOX RIVER · WING A</text>')
        # Right peeking Infirmary & Pipes
        u.append('<rect x="734" y="96" width="118" height="214" fill="none" stroke="#7FE6FF" stroke-width="1.4" opacity="0.45"/>')
        u.append('<text x="744" y="86" font-family="Consolas,monospace" font-size="9.5" fill="#7FE6FF" opacity="0.62">INFIRMARY</text>')
        u.append('<text x="108" y="476" font-family="Consolas,monospace" font-size="9.2" fill="#7FE6FF" opacity="0.58">FOX RIVER STATE PENITENTIARY · REV 4B</text>')

        # Brass compass pushed aside on upper-left edge
        u.append('<g transform="translate(124,412) rotate(-52)" opacity="0.82">')
        u.append('<path d="M0,0 L-16,74 M0,0 L18,72" fill="none" stroke="#9E7634" stroke-width="4.2" stroke-linecap="round"/>')
        u.append('<circle cx="0" cy="0" r="6" fill="#B88B3E"/>')
        u.append('</g>')
        u.append('</g>')
        parts.append("\n".join(u))

    # -------------------------------------------------------------------------
    # LAYER 2: ORTA — Slammed Crumpled Chicago Newspaper Front Page + Lincoln v1
    # -------------------------------------------------------------------------
    if _katman_aktif(katmanlar, "orta"):
        o: list[str] = ['<g id="s110-orta">']
        # Newspaper group tilted slightly (-3.2 deg) for raw dramatic impact
        o.append('<g transform="translate(482,272) rotate(-3.2) translate(-298,-238)">')
        # Deep impact shadow + stacked underneath pages
        o.append('<rect x="10" y="13" width="596" height="476" rx="2" fill="#030407" opacity="0.72"/>')
        o.append('<polygon points="4,8 602,2 606,478 8,482" fill="#B6AD9B" stroke="#4D463B" stroke-width="1.0"/>')
        o.append('<polygon points="-3,4 598,0 601,474 2,477" fill="#CFC6B3" stroke="#5A5245" stroke-width="1.0"/>')

        # Main front page sheet (slightly uneven crumpled corner at bottom-right)
        o.append(f'<polygon points="0,0 596,0 596,448 564,474 0,474" fill="url(#{p}_newsprint)" stroke="#3D362D" stroke-width="1.5"/>')
        # Curled dog-ear flap at bottom-right
        o.append('<polygon points="564,474 568,446 596,448" fill="#B9AF9B" stroke="#5E5548" stroke-width="1.0"/>')

        # Subtle newsprint paper grain flecks
        for _ in range(95):
            fx = rng.uniform(12, 584)
            fy = rng.uniform(12, 462)
            o.append(f'<circle cx="{fx:.1f}" cy="{fy:.1f}" r="{rng.uniform(0.5,1.2):.1f}" fill="#7A7060" opacity="{rng.uniform(0.12,0.28):.2f}"/>')

        # --- MASTHEAD: THE CHICAGO CHRONICLE ---
        o.append('<path d="M22,22 L574,22" fill="none" stroke="#181512" stroke-width="2.6"/>')
        o.append('<text x="298" y="54" text-anchor="middle" font-family="Georgia,Times New Roman,serif" font-size="31" font-weight="bold" fill="#15120F" letter-spacing="2.2">THE CHICAGO CHRONICLE</text>')
        o.append('<path d="M22,63 L574,63" fill="none" stroke="#181512" stroke-width="1.4"/>')
        o.append('<text x="26" y="75" font-family="Arial,sans-serif" font-size="8.2" font-weight="bold" fill="#3A332B">VOL. CXIV · NO. 284</text>')
        o.append('<text x="298" y="75" text-anchor="middle" font-family="Georgia,serif" font-size="8.4" font-style="italic" fill="#3A332B">ILLINOIS FINAL EDITION · CRIME &amp; JUSTICE</text>')
        o.append('<text x="570" y="75" text-anchor="end" font-family="Arial,sans-serif" font-size="8.2" font-weight="bold" fill="#3A332B">50¢</text>')
        o.append('<path d="M22,81 L574,81" fill="none" stroke="#181512" stroke-width="2.2"/>')

        # --- GIANT BANNER HEADLINE: DEATH ROW ---
        o.append('<rect x="22" y="88" width="552" height="72" fill="#141210"/>')
        o.append('<text x="298" y="146" text-anchor="middle" font-family="Impact,Arial Black,sans-serif" font-size="60" font-weight="900" fill="#F2EBD9" letter-spacing="7.5">DEATH ROW</text>')
        # Subheadline bar
        o.append('<rect x="22" y="164" width="552" height="24" fill="#8C1C24"/>')
        o.append('<text x="298" y="180" text-anchor="middle" font-family="Arial,sans-serif" font-size="13.2" font-weight="bold" fill="#FAF4E6" letter-spacing="1.4">LINCOLN BURROWS SENTENCED TO DIE — FOX RIVER</text>')
        o.append('<path d="M22,194 L574,194" fill="none" stroke="#221D18" stroke-width="1.2"/>')

        # --- LEFT COLUMN: FRAMED MUGSHOT PHOTO WITH LOCKED LINCOLN v1 ---
        o.append('<rect x="24" y="204" width="174" height="222" fill="#1B1916" stroke="#12100E" stroke-width="1.4"/>')
        o.append(f'<g transform="translate(28,208)" clip-path="url(#{p}_lincoln_clip)">')
        # Prison height chart background behind Lincoln
        o.append(f'<rect x="0" y="0" width="166" height="194" fill="url(#{p}_photo_bg)"/>')
        for hy in range(24, 190, 22):
            o.append(f'<path d="M0,{hy} L166,{hy}" fill="none" stroke="#6E7F8F" stroke-width="0.7" opacity="0.42"/>')
        o.append('<text x="8" y="20" font-family="Consolas,monospace" font-size="8.0" fill="#9BB0C2" opacity="0.75">6\'1"</text>')
        o.append('<text x="8" y="64" font-family="Consolas,monospace" font-size="8.0" fill="#9BB0C2" opacity="0.75">5\'10"</text>')
        # Prison blue shirt shoulders + inmate number #79238
        o.append('<path d="M14,196 L36,154 L130,154 L152,196 Z" fill="#5D7D9E" stroke="#171C22" stroke-width="1.8"/>')
        o.append('<path d="M62,154 L83,178 L104,154 Z" fill="#E5E1D8" stroke="#171C22" stroke-width="1.3"/>')
        o.append('<text x="48" y="182" font-family="Consolas,monospace" font-size="9.5" font-weight="bold" fill="#1C2836">79238</text>')
        # LOCKED LINCOLN v1 HEAD (front, odak, boyun=True)
        o.append('<g transform="translate(83,92) scale(0.62)">')
        o.append(K.lincoln_kafa("front", "odak", boyun=True))
        o.append('</g>')
        # Subtle newsprint halftone wash over photo
        o.append('<rect x="0" y="0" width="166" height="194" fill="#D5CBB8" opacity="0.16"/>')
        o.append('</g>')
        # Photo caption
        o.append('<text x="111" y="416" text-anchor="middle" font-family="Arial,sans-serif" font-size="8.2" font-weight="bold" fill="#E5DEC8" letter-spacing="0.6">L. BURROWS · INMATE #79238</text>')
        o.append('<text x="111" y="438" text-anchor="middle" font-family="Georgia,serif" font-size="7.6" font-style="italic" fill="#3B342C">Fox River Maximum Security Transfer</text>')

        # --- RIGHT COLUMNS: AUTHENTIC ENGLISH ARTICLE LAYOUT ---
        o.append('<path d="M210,204 L210,456 M392,204 L392,456" fill="none" stroke="#4D453B" stroke-width="0.9"/>')

        # Column 2 (x=220..382)
        o.append('<text x="220" y="217" font-family="Georgia,serif" font-size="11.2" font-weight="bold" fill="#181410">FINAL APPEAL DENIED</text>')
        o.append('<text x="220" y="230" font-family="Georgia,serif" font-size="11.2" font-weight="bold" fill="#181410">BY ILLINOIS COURT</text>')
        o.append('<text x="220" y="242" font-family="Arial,sans-serif" font-size="7.2" font-weight="bold" fill="#5A5044">BY CHRONICLE METRO DESK</text>')
        col2_lines = [
            "CHICAGO — State Supreme",
            "Court justices rejected the",
            "final stay of execution for",
            "Lincoln Burrows late Friday.",
            "",
            "Prosecutors cited surveillance",
            "records from the parking",
            "garage shooting, while the",
            "defense maintains the evidence",
            "was fabricated to frame him.",
            "",
            "Burrows has been transferred",
            "to Fox River State Penitentiary",
            "pending the May 11 date.",
        ]
        for idx, txt in enumerate(col2_lines):
            if txt:
                o.append(f'<text x="220" y="{258 + idx*13.2:.1f}" font-family="Georgia,serif" font-size="8.4" fill="#2A241E">{txt}</text>')

        # Column 3 (x=402..570)
        o.append('<text x="402" y="217" font-family="Georgia,serif" font-size="10.8" font-weight="bold" fill="#181410">FOX RIVER SECURITY</text>')
        o.append('<text x="402" y="230" font-family="Georgia,serif" font-size="10.8" font-weight="bold" fill="#181410">ON HIGH ALERT</text>')
        col3_lines = [
            "JOLIET — Warden Pope",
            "confirmed maximum security",
            "protocols across Wing A and",
            "Death Row ahead of next",
            "month's scheduled execution.",
            "",
            "\"No inmate has ever escaped",
            "Fox River,\" officials stated.",
        ]
        for idx, txt in enumerate(col3_lines):
            if txt:
                o.append(f'<text x="402" y="{248 + idx*13.2:.1f}" font-family="Georgia,serif" font-size="8.4" fill="#2A241E">{txt}</text>')

        # Boxed sidebar in Column 3
        o.append('<rect x="402" y="358" width="166" height="86" fill="#D4C9B3" stroke="#362F27" stroke-width="1.1"/>')
        o.append('<rect x="402" y="358" width="166" height="18" fill="#231E19"/>')
        o.append('<text x="485" y="370" text-anchor="middle" font-family="Arial,sans-serif" font-size="8.2" font-weight="bold" fill="#F0E8D4">EXECUTION SCHEDULE</text>')
        o.append('<text x="412" y="392" font-family="Consolas,monospace" font-size="8.4" font-weight="bold" fill="#7D1820">DATE: MAY 11 · 00:01 AM</text>')
        o.append('<text x="412" y="407" font-family="Consolas,monospace" font-size="8.0" fill="#241E18">FACILITY: FOX RIVER</text>')
        o.append('<text x="412" y="421" font-family="Consolas,monospace" font-size="8.0" fill="#241E18">CELL: DEATH ROW #79238</text>')
        o.append('<text x="412" y="435" font-family="Consolas,monospace" font-size="8.0" fill="#241E18">STATUS: NO STAY GRANTED</text>')

        # Red hand-drawn marker circle around MAY 11 date!
        o.append('<ellipse cx="478" cy="389" rx="58" ry="12" fill="none" stroke="#B81D29" stroke-width="2.2" opacity="0.82"/>')

        # Coffee stain ring on lower-right corner of newspaper
        o.append('<g transform="translate(526,422)">')
        o.append('<circle cx="0" cy="0" r="34" fill="#8C592C" opacity="0.14"/>')
        o.append('<circle cx="0" cy="0" r="34" fill="none" stroke="#6B3E1B" stroke-width="3.4" opacity="0.38"/>')
        o.append('<circle cx="2" cy="1" r="31.5" fill="none" stroke="#4D2910" stroke-width="1.2" opacity="0.32"/>')
        o.append('<circle cx="-26" cy="28" r="3.2" fill="#6B3E1B" opacity="0.32"/>')
        o.append('</g>')

        # Subtle paper fold crease across lower third (avoids Lincoln's eyes) + corner crumple lines
        o.append(f'<rect x="0" y="344" width="596" height="16" fill="url(#{p}_crease_h)" opacity="0.72"/>')
        o.append('<path d="M510,0 L562,64 M0,418 L48,474" fill="none" stroke="#9C9280" stroke-width="1.0" opacity="0.35"/>')
        o.append('<path d="M512,0 L564,64 M2,418 L50,474" fill="none" stroke="#FFFBF0" stroke-width="0.8" opacity="0.35"/>')

        o.append('</g>')  # end rotated newspaper
        o.append('</g>')
        parts.append("\n".join(o))

    # -------------------------------------------------------------------------
    # LAYER 3: SAHNE — Red Marking Pen Slammed Beside Newspaper
    # -------------------------------------------------------------------------
    if _katman_aktif(katmanlar, "sahne"):
        s: list[str] = ['<g id="s110-sahne">']
        # Red grease/marking pen on right edge of blueprint
        s.append('<g transform="translate(838,342) rotate(18)">')
        s.append('<rect x="4" y="5" width="12" height="146" rx="4" fill="#040508" opacity="0.62"/>')
        s.append('<rect x="0" y="0" width="11" height="134" rx="3" fill="#8E1C26" stroke="#18080A" stroke-width="1.2"/>')
        s.append('<rect x="0" y="28" width="11" height="7" fill="#D5A852"/>')
        s.append('<polygon points="0,134 11,134 5.5,150" fill="#DFCEB0" stroke="#18080A" stroke-width="1.0"/>')
        s.append('<polygon points="3.5,144 7.5,144 5.5,150" fill="#B81D29"/>')
        s.append('</g>')
        s.append('</g>')
        parts.append("\n".join(s))

    # -------------------------------------------------------------------------
    # LAYER 4: PLAN — Subtle Cyan Blueprint Pulse Underneath + Crimson Target Reticle
    # -------------------------------------------------------------------------
    if _katman_aktif(katmanlar, "plan"):
        pl: list[str] = ['<g id="s110-plan">']
        # Cyan escape line still glowing faintly from under the newspaper edges
        pl.append(
            f'<path d="M126,244 L182,244 M784,218 L856,218 L856,164" '
            f'fill="none" stroke="{PLAN}" stroke-width="2.6" opacity="0.72" filter="url(#{p}_glow_cyan)"/>'
        )
        pl.append(f'<circle cx="126" cy="244" r="5" fill="none" stroke="{PLAN}" stroke-width="1.4" opacity="0.75"/>')
        pl.append(f'<circle cx="856" cy="164" r="5" fill="none" stroke="{PLAN}" stroke-width="1.4" opacity="0.75"/>')
        # Subtle red tension corner brackets framing the headline zone
        pl.append(f'<path d="M162,48 L162,36 L184,36 M796,492 L796,504 L774,504" fill="none" stroke="{RED_ALERT}" stroke-width="1.8" opacity="0.75"/>')
        pl.append('</g>')
        parts.append("\n".join(pl))

    # -------------------------------------------------------------------------
    # LAYER 5: ONPLAN — Dramatic Prison Bar Shadows + Crimson Tension Glow + Vignette
    # -------------------------------------------------------------------------
    if _katman_aktif(katmanlar, "onplan"):
        op_l: list[str] = ['<g id="s110-onplan">']
        # Cold directional key light across center
        op_l.append(f'<rect x="0" y="0" width="960" height="540" fill="url(#{p}_cold_key)"/>')
        # Dramatic diagonal prison-bar shadows slashing across BOTH blueprint and newspaper
        op_l.append('<g opacity="0.44">')
        for bx in range(-120, 1020, 118):
            op_l.append(f'<polygon points="{bx},0 {bx+34},0 {bx-146},540 {bx-180},540" fill="#04070D"/>')
        # Horizontal crossbar shadow
        op_l.append('<polygon points="0,152 960,82 960,104 0,174" fill="#04070D" opacity="0.78"/>')
        op_l.append('<polygon points="0,398 960,328 960,348 0,418" fill="#04070D" opacity="0.72"/>')
        op_l.append('</g>')
        # Crimson high-tension corner glow (top-right)
        op_l.append(f'<rect x="0" y="0" width="960" height="540" fill="url(#{p}_red_glow)"/>')
        # Subtle red edge flare
        op_l.append(f'<circle cx="882" cy="64" r="46" fill="#FF3246" opacity="0.18" filter="url(#{p}_glow_red)"/>')
        # Deep cinematic vignette
        op_l.append(f'<rect x="0" y="0" width="960" height="540" fill="url(#{p}_vignette)"/>')
        op_l.append('</g>')
        parts.append("\n".join(op_l))

    return defs, "\n".join(parts)


# =============================================================================
# RENDERING & PRESENTATION CARDS (1280x720 SET CARD + R13 200% ZOOM CARD)
# =============================================================================
def _render_scene_pil(scene_fn, width: int = 1920, height: int = 1080) -> Image.Image:
    defs, body = scene_fn()
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {W_SCENE} {H_SCENE}">'
        f"<defs>{defs}</defs>"
        f"{body}"
        f"</svg>"
    )
    png_bytes = resvg_py.svg_to_bytes(svg_string=svg)
    return Image.open(io.BytesIO(png_bytes)).convert("RGBA")


def _load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
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
    draw: ImageDraw.ImageDraw, x: int, y: int, colors: list[str], size: int = 16, gap: int = 6
) -> None:
    for i, hex_c in enumerate(colors):
        cx = x + i * (size + gap)
        draw.rounded_rectangle((cx, y, cx + size, y + size), radius=3, fill=hex_c, outline="#384D66", width=1)


def uret_kartlar(versiyon: str = "v1") -> tuple[Path, Path]:
    print("Rendering 3 Act I scenes at 1920x1080...")
    img_108 = _render_scene_pil(set_108_chicago_ofis, 1920, 1080)
    img_109 = _render_scene_pil(set_109_taslak_masasi, 1920, 1080)
    img_110 = _render_scene_pil(set_110_idam_manset, 1920, 1080)

    # =========================================================================
    # OUTPUT 1: SET PRESENTATION CARD (1280 x 720 — ALL ENGLISH)
    # =========================================================================
    canvas = _draw_card_bg(1280, 720)
    draw = ImageDraw.Draw(canvas)

    f_title = _load_font(20, bold=True)
    f_sub = _load_font(12, bold=False)
    f_card_t = _load_font(13, bold=True)
    f_card_s = _load_font(11, bold=False)
    f_small = _load_font(10, bold=False)

    draw.text((24, 14), "MICHAEL SCOFIELD  ·  ACT I ENGINEERING & FOX RIVER SET", fill="#EBF3FA", font=f_title)
    draw.text(
        (24, 39),
        "STYLE B+A HYBRID (CINEMATIC 2D + CYAN BLUEPRINT VISION)  ·  SCENES 1.08 – 1.10",
        fill="#7E97B0",
        font=f_sub,
    )
    top_swatches = [
        ("#11223B", "CHICAGO"),
        ("#F2C46D", "AMBER"),
        ("#0E365B", "BLUEPRINT"),
        ("#E63244", "TENSION"),
        ("#7FE6FF", "CAD PLAN"),
    ]
    sx_top = 816
    for col, lbl in top_swatches:
        draw.rounded_rectangle((sx_top, 18, sx_top + 14, 32), radius=3, fill=col, outline="#3B536D", width=1)
        draw.text((sx_top + 19, 19), lbl, fill="#9BB2C8", font=f_small)
        sx_top += 88
    draw.line((24, 58, 1256, 58), fill="#213247", width=1)

    # --- TOP-LEFT PANEL: 1.08 CHICAGO OFFICE ---
    _draw_panel_box(draw, (22, 68, 630, 366))
    t108 = img_108.resize((448, 252), Image.Resampling.LANCZOS)
    canvas.paste(t108, (34, 98), t108)
    draw.rectangle((34, 98, 34 + 448, 98 + 252), outline="#2E455E", width=1)
    draw.text((34, 76), "01 · 1.08 CHICAGO OFFICE", fill="#7FE6FF", font=f_card_t)
    draw.text((228, 78), "Title Card: \"STRUCTURAL ENGINEER\"", fill="#8AA3BC", font=f_card_s)
    ix = 492
    draw.text((ix, 98), "PALETTE", fill="#7FE6FF", font=f_small)
    _draw_swatches(draw, ix, 114, ["#0B172B", "#3C271B", "#E8C26B", "#7B5647", "#7FE6FF"], size=18, gap=5)
    draw.text((ix, 146), "KEY ELEMENTS", fill="#9BB2C8", font=f_small)
    for k_i, item in enumerate(
        [
            "• Loyola Univ. Diploma",
            "• Willis & Hancock CAD",
            "• Chicago River Bridge",
            "• Architect Desk & Mug",
            "• Live #7FE6FF Wireframe",
        ]
    ):
        draw.text((ix, 164 + k_i * 19), item, fill="#D5E2EE", font=f_card_s)
    draw.text((ix, 272), "KEY LIGHTING", fill="#9BB2C8", font=f_small)
    draw.text((ix, 288), "Twilight + warm desk lamp", fill="#F6C367", font=f_card_s)
    draw.text((ix, 314), "LAYERS (5)", fill="#9BB2C8", font=f_small)
    draw.text((ix, 330), "uzak · orta · sahne\nplan · onplan", fill="#8AA3BC", font=f_small)

    # --- TOP-RIGHT PANEL: 1.09 ARCHITECT'S DRAFTING TABLE ---
    _draw_panel_box(draw, (648, 68, 1256, 366))
    t109 = img_109.resize((448, 252), Image.Resampling.LANCZOS)
    canvas.paste(t109, (660, 98), t109)
    draw.rectangle((660, 98, 660 + 448, 98 + 252), outline="#2E455E", width=1)
    draw.text((660, 76), "02 · 1.09 DRAFTING TABLE", fill="#F6C367", font=f_card_t)
    draw.text((854, 78), "Title Card: \"FOX RIVER\"", fill="#8AA3BC", font=f_card_s)
    ix2 = 1118
    draw.text((ix2, 98), "PALETTE", fill="#7FE6FF", font=f_small)
    _draw_swatches(draw, ix2, 114, ["#362317", "#0E365B", "#F0A948", "#E6D8AE", "#7FE6FF"], size=18, gap=5)
    draw.text((ix2, 146), "KEY ELEMENTS", fill="#9BB2C8", font=f_small)
    for k_i, item in enumerate(
        [
            "• Fox River Blueprint",
            "• Wing A / Infirmary / Yard",
            "• Locked Crane v4 Center",
            "• Brass Compass & T-Sq",
            "• Warm Amber Lamp Pool",
        ]
    ):
        draw.text((ix2, 164 + k_i * 19), item, fill="#D5E2EE", font=f_card_s)
    draw.text((ix2, 272), "KEY LIGHTING", fill="#9BB2C8", font=f_small)
    draw.text((ix2, 288), "Warm amber architect lamp", fill="#F6C367", font=f_card_s)
    draw.text((ix2, 314), "LAYERS (5)", fill="#9BB2C8", font=f_small)
    draw.text((ix2, 330), "uzak · orta · sahne\nplan · onplan", fill="#8AA3BC", font=f_small)

    # --- BOTTOM WIDE PANEL: 1.10 DEATH ROW FRONT PAGE ---
    _draw_panel_box(draw, (22, 378, 1256, 704))
    t110 = img_110.resize((512, 288), Image.Resampling.LANCZOS)
    canvas.paste(t110, (34, 404), t110)
    draw.rectangle((34, 404, 34 + 512, 404 + 288), outline="#5C2830", width=1)
    draw.text((34, 384), "03 · 1.10 DEATH ROW FRONT PAGE", fill="#FF5A68", font=f_card_t)
    draw.text((284, 386), "Title Card: \"DEATH ROW\" · Dramatic Bars & Crimson Tension", fill="#B88E92", font=f_card_s)

    rx = 564
    draw.text((rx, 404), "PALETTE (CRIMSON & COLD STEEL CONTRAST)", fill="#FF7A85", font=f_small)
    _draw_swatches(draw, rx, 422, ["#080A0F", "#0B2742", "#DED5C0", "#8C1C24", "#FF3246", "#7FE6FF"], size=22, gap=7)
    draw.text((rx, 458), "KEY ELEMENTS", fill="#9BB2C8", font=f_small)
    for k_i, item in enumerate(
        [
            "• THE CHICAGO CHRONICLE front page slammed on plan",
            "• Bold DEATH ROW banner & Fox River subheadline",
            "• Locked Lincoln v1 mugshot (#79238) in left column",
            "• Diagonal prison-bar shadows + coffee ring & red glow",
        ]
    ):
        draw.text((rx, 476 + k_i * 21), item, fill="#E3ECF5", font=f_card_s)
    draw.text((rx, 572), "DRAMATIC SHIFT", fill="#9BB2C8", font=f_small)
    draw.text(
        (rx, 590),
        "Continuity with 1.09's Fox River blueprint underneath,\n"
        "slashed by harsh prison-bar shadows and crimson alert\n"
        "lighting as the May 11 execution deadline hits.",
        fill="#D4C2C4",
        font=f_card_s,
    )
    draw.text((rx, 650), "LAYERS (5)", fill="#9BB2C8", font=f_small)
    draw.text((rx, 666), "s110-uzak · s110-orta · s110-sahne · s110-plan · s110-onplan", fill="#8AA3BC", font=f_small)

    draw.line((880, 404, 880, 692), fill="#233447", width=1)
    tx = 898
    draw.text((tx, 404), "ACT I VISUAL ARC & ENGINE SPEC", fill="#7FE6FF", font=f_card_t)
    notes = [
        (
            "1.08 -> 1.09 -> 1.10 PROGRESSION",
            "Moves from Michael's brilliant structural mind in\n"
            "Chicago, down onto his Fox River drafting table,\n"
            "to the harsh reality of Lincoln's Death Row headline.",
        ),
        (
            "LOCKED ASSET INTEGRATION",
            "Embeds locked Origami Crane v4 (K.turna) in 1.09\n"
            "and locked Lincoln Burrows v1 (K.lincoln_kafa)\n"
            "inside the authentic Chicago Chronicle front page.",
        ),
        (
            "PARALLAX & CLEAN SVG SPEC",
            "Each function returns pure (defs, body) at 960x540\n"
            "with 5 named <g> depth layers and fill='none' on\n"
            "every stroked <path> for seamless camera rig use.",
        ),
    ]
    ny = 432
    for heading, body_txt in notes:
        draw.text((tx, ny), heading, fill="#F6C367" if "PROGRESSION" in heading else "#9EC5DE", font=f_small)
        draw.text((tx, ny + 16), body_txt, fill="#C5D5E4", font=f_card_s)
        ny += 86

    out_main = OUT_DIR / f"b1_set_muhendis_{versiyon}.png"
    canvas.convert("RGB").save(out_main, quality=95)

    # =========================================================================
    # OUTPUT 2: R13 200% ZOOM QUALITY CONTROL CARD (1280 x 720 — 4 PANELS)
    # =========================================================================
    r13 = _draw_card_bg(1280, 720)
    d13 = ImageDraw.Draw(r13)
    d13.text((24, 13), "R13 · 200% ZOOM QUALITY CONTROL (ACT I ENGINEERING SET)", fill="#EBF3FA", font=f_title)
    d13.text(
        (24, 37),
        "1:1 PIXEL CROPS FROM 1920×1080 SOURCE  ·  TEXTURE, TYPOGRAPHY, LIGHTING & ASSET FIDELITY",
        fill="#7E97B0",
        font=f_sub,
    )
    d13.line((24, 55, 1256, 55), fill="#213247", width=1)

    cw, ch = 600, 264
    crops = [
        (
            img_108,
            (1320, 520),
            "1 · 1.08 CHICAGO CAD SKYSCRAPERS & RIVER BRIDGE (200%)",
            "Hancock X-bracing dissolving to #7FE6FF CAD wireframe + steel truss river bridge",
            (22, 66),
        ),
        (
            img_109,
            (1130, 470),
            "2 · 1.09 FOX RIVER BLUEPRINT, CRANE v4 & COMPASS (200%)",
            "Multi-wing penitentiary plan, glowing escape route, K.turna v4 & brass compass",
            (652, 66),
        ),
        (
            img_110,
            (700, 675),
            "3 · 1.10 DEATH ROW NEWSPAPER & LINCOLN v1 PHOTO (200%)",
            "THE CHICAGO CHRONICLE headline, K.lincoln_kafa v1 mugshot (#79238) & bar shadows",
            (22, 392),
        ),
        (
            img_108,
            (260, 315),
            "4 · 1.08 LOYOLA DIPLOMA, WOOD PANEL & BOOKSHELF (200%)",
            "Gold-framed Structural Engineering diploma, walnut grain, binders & truss model",
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

    out_r13 = OUT_DIR / "b1_set_muhendis_r13.png"
    r13.convert("RGB").save(out_r13, quality=95)
    print(f"Saved:\n  - {out_main}\n  - {out_r13}")
    return out_main, out_r13


if __name__ == "__main__":
    uret_kartlar("v1")
