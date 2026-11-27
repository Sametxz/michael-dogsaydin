"""V12 (Act IV: Panama Harbor & Christina Rose Trap + Sona's Iron Gate — Act V Open Loop).

Style B+A Hybrid (Cinematic 2D + Cyan/Red Blueprint CAD Vision) — R18-HAREKET live-layer scenes (960x540):
  - set_407_panama_tekne(katmanlar=None) -> (defs_str, body_str)
  - set_408_sona_kapisi(katmanlar=None)  -> (defs_str, body_str)

Rules enforced:
  - 100% ENGLISH on-screen typography (zero box overflow, >=16px horizontal padding).
  - Every stroked <path> explicitly sets fill="none" (unless an intentional filled closed shape).
  - R4-PARALAKS: Locked full-body Michael v3 (`K.michael_figur`) lives inside the single `sahne` layer.
  - R18-HAREKET: Separate animated layers (`tekne`, `sis_katman`, `tuzak_halka`, `kapi_sol`, `kapi_sag`).
  - Side-effect-free module; read-only import of `karakter as K` without modifying it.
"""
from __future__ import annotations

import io
import math
import random
import re
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
INK_WARM = "#1E1813"
PLAN = "#7FE6FF"
PLAN_CORE = "#E4FCFF"
RED_TRAP = "#E03E3E"
RED_GLOW = "#FF5462"
BLUE_POLICE = "#2F86FF"

_UID = 0


def _uid(prefix: str = "b4") -> str:
    global _UID
    _UID += 1
    return f"{prefix}_{_UID}"


def _katman_aktif(katmanlar: set[str] | list[str] | None, ad: str) -> bool:
    return katmanlar is None or ad in katmanlar


# =============================================================================
# SCENE 4.07: PANAMA HARBOR & THE TRAP (CHRISTINA ROSE)
# =============================================================================
def set_407_panama_tekne(
    katmanlar: set[str] | list[str] | None = None,
) -> tuple[str, str]:
    """Dawn misty emerald-blue Panama harbor with R18-HAREKET live layers:
      - `uzak`        : Dawn misty Panama sky, glowing low sun, distant Panama City skyline
      - `orta`        : Emerald-blue harbor water, reflections, far pier, approaching police patrol lights
      - `tekne`       : Elegant white sailing yacht `CHRISTINA ROSE` (bobs/drifts in animatic)
      - `sis_katman`  : Semi-transparent drifting harbor mist banks
      - `sahne`       : Foreground wooden pier planks, bollards, coiled mooring rope
      - `tuzak_halka` : Red Company/CAD closing trap rings + `COMPANY TRAP · PANAMA` HUD
      - `plan`        : Cyan `#7FE6FF` CAD harbor grid, `PANAMA CITY` & `VESSEL` callouts
      - `onplan`      : Foreground sea-mist edge, floating motes & cinematic vignette
    """
    rng = random.Random(407)
    p = _uid("s407")

    defs = f"""
    <linearGradient id="{p}_sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#0E2534"/>
      <stop offset="34%" stop-color="#1D4456"/>
      <stop offset="68%" stop-color="#4B7B86"/>
      <stop offset="90%" stop-color="#9AC0B8"/>
      <stop offset="100%" stop-color="#CBE0CE"/>
    </linearGradient>
    <radialGradient id="{p}_sun" cx="0.68" cy="0.39" r="0.34">
      <stop offset="0%" stop-color="#FFF4D4" stop-opacity="0.92"/>
      <stop offset="28%" stop-color="#F2D7A4" stop-opacity="0.46"/>
      <stop offset="65%" stop-color="#7EB5B3" stop-opacity="0.16"/>
      <stop offset="100%" stop-color="#1D4456" stop-opacity="0.0"/>
    </radialGradient>
    <linearGradient id="{p}_water" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#1B5662"/>
      <stop offset="26%" stop-color="#134552"/>
      <stop offset="65%" stop-color="#0C2E3B"/>
      <stop offset="100%" stop-color="#061A24"/>
    </linearGradient>
    <linearGradient id="{p}_hull" x1="0.1" y1="0" x2="0.85" y2="1">
      <stop offset="0%" stop-color="#F7FAFC"/>
      <stop offset="52%" stop-color="#E1EBF0"/>
      <stop offset="100%" stop-color="#B0C4CE"/>
    </linearGradient>
    <linearGradient id="{p}_hull_sh" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#C2D4DD"/>
      <stop offset="100%" stop-color="#7B96A4"/>
    </linearGradient>
    <linearGradient id="{p}_sail" x1="0" y1="0" x2="1" y2="0.8">
      <stop offset="0%" stop-color="#FCFDFD"/>
      <stop offset="65%" stop-color="#DDE8ED"/>
      <stop offset="100%" stop-color="#B7CBD4"/>
    </linearGradient>
    <linearGradient id="{p}_wood" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#533D2E"/>
      <stop offset="55%" stop-color="#3A291E"/>
      <stop offset="100%" stop-color="#221710"/>
    </linearGradient>
    <linearGradient id="{p}_wood_top" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#6B513E"/>
      <stop offset="50%" stop-color="#553F2F"/>
      <stop offset="100%" stop-color="#3B2B20"/>
    </linearGradient>
    <radialGradient id="{p}_pol_r" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0%" stop-color="#FF384A" stop-opacity="0.95"/>
      <stop offset="40%" stop-color="#E03E3E" stop-opacity="0.40"/>
      <stop offset="100%" stop-color="#E03E3E" stop-opacity="0.0"/>
    </radialGradient>
    <radialGradient id="{p}_pol_b" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0%" stop-color="#45A2FF" stop-opacity="0.95"/>
      <stop offset="40%" stop-color="#2F86FF" stop-opacity="0.40"/>
      <stop offset="100%" stop-color="#2F86FF" stop-opacity="0.0"/>
    </radialGradient>
    <linearGradient id="{p}_mist" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#CBE4E2" stop-opacity="0.0"/>
      <stop offset="45%" stop-color="#CFE7E5" stop-opacity="0.34"/>
      <stop offset="100%" stop-color="#9FC7CA" stop-opacity="0.0"/>
    </linearGradient>
    <radialGradient id="{p}_vig" cx="0.5" cy="0.48" r="0.68">
      <stop offset="58%" stop-color="#051018" stop-opacity="0.0"/>
      <stop offset="100%" stop-color="#040C12" stop-opacity="0.62"/>
    </radialGradient>
    """

    parts: list[str] = []

    # ── 1. UZAK: Dawn misty Panama sky + distant skyline ─────────────────────
    if _katman_aktif(katmanlar, "uzak"):
        u: list[str] = []
        u.append(f'<rect x="0" y="0" width="{W_SCENE}" height="248" fill="url(#{p}_sky)"/>')
        u.append(f'<rect x="0" y="0" width="{W_SCENE}" height="260" fill="url(#{p}_sun)"/>')

        # Soft dawn cloud strata
        u.append(
            '<path d="M-20,94 Q140,76 290,92 Q430,104 590,82 Q760,64 980,88 L980,126 L-20,126 Z" '
            'fill="#D9EAE4" opacity="0.16"/>'
            '<path d="M-20,148 Q190,130 380,146 Q620,160 980,132 L980,176 L-20,176 Z" '
            'fill="#E4F0E8" opacity="0.18"/>'
        )
        # Dawn sun disc diffused through mist
        u.append(
            '<circle cx="654" cy="186" r="26" fill="#FFF7DF" opacity="0.72"/>'
            '<circle cx="654" cy="186" r="46" fill="#F6DEA9" opacity="0.22"/>'
        )

        # Distant Panama hills / causeway headland
        u.append(
            '<path d="M0,226 Q110,204 210,214 Q320,222 440,218 L440,248 L0,248 Z" fill="#1F4554" opacity="0.68"/>'
            '<path d="M580,224 Q710,200 840,210 Q910,216 960,208 L960,248 L580,248 Z" fill="#1E4250" opacity="0.62"/>'
        )

        # Distant misty Panama City high-rise skyline silhouettes
        skyscrapers = [
            (62, 174, 24, 68),
            (90, 152, 22, 90),
            (116, 134, 26, 108),
            (146, 160, 20, 82),
            (172, 122, 24, 120),  # iconic tapered Panama tower
            (200, 146, 28, 96),
            (234, 166, 22, 76),
            (262, 142, 20, 100),
            (288, 176, 30, 66),
            (326, 158, 24, 84),
            (356, 182, 26, 60),
            (694, 178, 22, 64),
            (722, 158, 26, 84),
            (754, 144, 22, 98),
            (782, 168, 28, 74),
            (818, 180, 24, 62),
            (850, 164, 20, 78),
        ]
        for bx, by, bw, bh in skyscrapers:
            u.append(
                f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" fill="#234A59" opacity="0.62"/>'
            )
            # Subtle lit skyscraper windows
            for wy in range(by + 10, 226, 11):
                if rng.random() < 0.42:
                    wx = bx + 4 + rng.randint(0, max(1, bw - 12))
                    u.append(
                        f'<rect x="{wx}" y="{wy}" width="4" height="2" fill="#DCEFE8" opacity="0.34"/>'
                    )
        # Signature curved sail-tower silhouette (Panama skyline flavor)
        u.append(
            '<path d="M174,242 L176,120 Q188,106 196,122 L198,242 Z" fill="#1D3F4E" opacity="0.72"/>'
            '<path d="M186,112 L186,98" fill="none" stroke="#2D5A6B" stroke-width="1.5" opacity="0.7"/>'
        )
        # Distant harbor cranes on far right
        u.append(
            '<path d="M884,238 L890,188 L904,188 L908,238 M880,192 L932,174 M904,188 L924,196" '
            'fill="none" stroke="#244856" stroke-width="1.8" opacity="0.62"/>'
        )
        # Horizon atmospheric haze seam
        u.append('<rect x="0" y="220" width="960" height="32" fill="#A6CCC8" opacity="0.28"/>')
        parts.append(f'<g id="s407-uzak">{"".join(u)}</g>')

    # ── 2. ORTA: Emerald-blue harbor water, far dock & approaching police patrol ─
    if _katman_aktif(katmanlar, "orta"):
        m: list[str] = []
        m.append(f'<rect x="0" y="242" width="{W_SCENE}" height="298" fill="url(#{p}_water)"/>')

        # Sun reflection column on emerald water
        for i in range(18):
            ry = 248 + i * 14
            rw = 56 + i * 7 + rng.randint(-8, 10)
            rx = 654 - rw * 0.5 + rng.randint(-10, 10)
            op = max(0.06, 0.42 - i * 0.018)
            m.append(
                f'<rect x="{rx:.1f}" y="{ry}" width="{rw:.1f}" height="3.2" rx="1.6" '
                f'fill="#E8F1D5" opacity="{op:.2f}"/>'
            )

        # Horizontal emerald-teal wave shimmer lines across harbor
        for i in range(44):
            wy = rng.uniform(248, 520)
            wx = rng.uniform(10, 880)
            wl = rng.uniform(26, 110) * (0.55 + (wy - 242) / 420.0)
            col = "#59A9B0" if i % 3 else "#8CD4D2"
            op = rng.uniform(0.10, 0.28)
            m.append(
                f'<path d="M{wx:.1f},{wy:.1f} Q{wx + wl * 0.5:.1f},{wy - 1.8:.1f} {wx + wl:.1f},{wy:.1f}" '
                f'fill="none" stroke="{col}" stroke-width="1.3" opacity="{op:.2f}" stroke-linecap="round"/>'
            )

        # Distant waterfront seawall & approaching Panama Police Patrol cruisers (left waterfront)
        m.append(
            '<path d="M0,240 L374,240 L356,262 L0,262 Z" fill="#182C38" stroke="#0D1A22" stroke-width="1.4"/>'
            '<path d="M0,256 L360,256" fill="none" stroke="#456E7E" stroke-width="1.1" opacity="0.5"/>'
        )
        # Distant harbor dock pilings (mid-left)
        for px in (46, 98, 152, 206, 260, 314):
            m.append(
                f'<rect x="{px}" y="248" width="7" height="30" fill="#211B16" stroke="{INK}" stroke-width="1.0"/>'
                f'<rect x="{px + 1}" y="278" width="5" height="22" fill="#0B1E28" opacity="0.55"/>'
            )

        # Three approaching police patrol cruisers along waterfront with red-blue lightbar flares
        patrol_cars = [(58, 240, 0.78), (126, 241, 1.0), (232, 243, 0.90)]
        for cx, cy, sc in patrol_cars:
            m.append(
                f'<g transform="translate({cx},{cy}) scale({sc:.2f})">'
                f'<path d="M-24,8 L-20,-2 L-8,-8 L10,-8 L20,-1 L26,2 L26,8 Z" '
                f'fill="#101A24" stroke="#080D12" stroke-width="1.2"/>'
                f'<rect x="-7" y="-11" width="6" height="3.2" rx="1" fill="#FF384A"/>'
                f'<rect x="1" y="-11" width="6" height="3.2" rx="1" fill="#45A2FF"/>'
                f'<circle cx="-4" cy="-9" r="28" fill="url(#{p}_pol_r)"/>'
                f'<circle cx="4" cy="-9" r="28" fill="url(#{p}_pol_b)"/>'
                f'<circle cx="23" cy="4" r="3.4" fill="#FFF2C2" opacity="0.92"/>'
                f'</g>'
            )
            # Red & blue shimmer streaks on the emerald harbor water below patrol cars
            for k in range(7):
                ry = 264 + k * 10
                m.append(
                    f'<rect x="{cx - 18 - k * 2}" y="{ry}" width="{16 + k * 3}" height="2.6" rx="1.3" '
                    f'fill="#FF3F50" opacity="{0.46 - k * 0.055:.2f}"/>'
                    f'<rect x="{cx + 2}" y="{ry + 3}" width="{16 + k * 3}" height="2.6" rx="1.3" '
                    f'fill="#3D9BFF" opacity="{0.46 - k * 0.055:.2f}"/>'
                )

        # Midground timber jetty extending from right toward the yacht
        m.append(
            '<path d="M746,356 L960,342 L960,368 L746,374 Z" fill="#3B2B20" stroke="#14100D" stroke-width="1.6"/>'
        )
        for jx in (756, 804, 854, 906, 948):
            m.append(
                f'<rect x="{jx}" y="340" width="11" height="58" rx="2" fill="url(#{p}_wood)" stroke="{INK}" stroke-width="1.5"/>'
                f'<ellipse cx="{jx + 5.5}" cy="340" rx="5.5" ry="2.4" fill="#6E5440" stroke="{INK}" stroke-width="1.1"/>'
            )

        parts.append(f'<g id="s407-orta">{"".join(m)}</g>')

    # ── 3. TEKNE: Hero Sailing Yacht "CHRISTINA ROSE" (R18-HAREKET layer) ───
    if _katman_aktif(katmanlar, "tekne"):
        t: list[str] = []
        # Soft reflection & water contact ripples directly under the hull
        t.append(
            '<ellipse cx="520" cy="396" rx="196" ry="18" fill="#071B24" opacity="0.62"/>'
            '<path d="M332,394 Q426,406 520,398 Q616,406 710,392" fill="none" stroke="#8AD8D8" stroke-width="2.0" opacity="0.52" stroke-linecap="round"/>'
            '<path d="M366,406 Q460,416 560,409 Q634,414 688,404" fill="none" stroke="#62B6BE" stroke-width="1.5" opacity="0.38" stroke-linecap="round"/>'
            '<path d="M402,418 Q514,426 646,416" fill="none" stroke="#D9EFEF" stroke-width="1.1" opacity="0.26" stroke-linecap="round"/>'
        )

        # Tall mast, spreaders, forestay, backstay & shrouds
        t.append(
            '<path d="M518,322 L512,68" fill="none" stroke="#DCE7EE" stroke-width="5.2" stroke-linecap="round"/>'
            f'<path d="M518,322 L512,68" fill="none" stroke="{INK}" stroke-width="1.3" stroke-linecap="round"/>'
            # Masthead spreaders
            '<path d="M492,148 L534,148 M496,214 L532,214" fill="none" stroke="#C8D9E2" stroke-width="2.4" stroke-linecap="round"/>'
            # Rigging cables (forestay to bow, backstay to stern, shrouds)
            '<path d="M512,72 L322,334 M512,72 L696,336 M513,148 L470,334 M513,148 L562,334 '
            'M514,214 L486,334 M514,214 L548,334" '
            'fill="none" stroke="#B7CDD8" stroke-width="1.25" opacity="0.78"/>'
            # Masthead wind vane & anchor light
            '<path d="M512,68 L512,56 M506,62 L522,60" fill="none" stroke="#E8F4FA" stroke-width="1.5"/>'
            '<circle cx="512" cy="56" r="2.6" fill="#FFF3C4"/>'
        )

        # Partially-reefed / billowing white mainsail & furled jib
        t.append(
            # Soft mainsail billow behind mast (ready to sail at dawn)
            f'<path d="M516,86 Q574,174 636,294 L518,302 Z" fill="url(#{p}_sail)" opacity="0.94" '
            f'stroke="{INK}" stroke-width="1.8" stroke-linejoin="round"/>'
            # Sail battens & wind creases
            '<path d="M516,136 Q550,140 572,144 M517,192 Q562,198 598,202 M518,248 Q576,254 618,256" '
            'fill="none" stroke="#9AB4C2" stroke-width="1.3" opacity="0.72"/>'
            '<path d="M542,142 Q568,210 596,292" fill="none" stroke="#FFFFFF" stroke-width="3.2" opacity="0.34" stroke-linecap="round"/>'
            # Furled jib along forestay
            '<path d="M511,76 L332,330 L342,330 L513,84 Z" fill="#EAF2F6" stroke="#243844" stroke-width="1.2"/>'
            # Horizontal boom & reefed sail fold
            '<path d="M515,302 L648,296" fill="none" stroke="#CFDCE4" stroke-width="5.0" stroke-linecap="round"/>'
            f'<path d="M515,302 L648,296" fill="none" stroke="{INK}" stroke-width="1.3" stroke-linecap="round"/>'
            '<path d="M518,296 Q580,286 644,292 L642,300 L518,304 Z" fill="#F0F6F8" stroke="#2A3E4A" stroke-width="1.1"/>'
        )

        # Cabin superstructure, teak deck rail & warm portholes
        t.append(
            f'<path d="M412,334 L438,314 L578,312 L606,334 Z" fill="#EDF4F7" stroke="{INK}" stroke-width="2.0" stroke-linejoin="round"/>'
            '<path d="M438,314 L578,312 L584,320 L432,322 Z" fill="#FFFFFF" opacity="0.75"/>'
            # Tinted cabin windows with faint warm cabin glow
            '<path d="M446,321 L478,320 L476,329 L440,329 Z" fill="#234152" stroke="#111C24" stroke-width="1.2"/>'
            '<path d="M488,320 L534,319 L534,328 L488,329 Z" fill="#27495C" stroke="#111C24" stroke-width="1.2"/>'
            '<path d="M544,319 L576,319 L580,328 L544,328 Z" fill="#D9B46A" opacity="0.62" stroke="#111C24" stroke-width="1.2"/>'
            # Stainless bow pulpit & lifelines
            '<path d="M322,334 L334,316 L354,322 M334,316 L418,326 L608,326 L692,320 L696,336" '
            'fill="none" stroke="#D2E2EA" stroke-width="1.5" stroke-linejoin="round"/>'
            # Teak deck sheer strip
            '<path d="M318,334 Q508,346 698,334 L696,340 Q508,352 322,340 Z" fill="#7D5436" stroke="#1C140E" stroke-width="1.2"/>'
        )

        # Main sculpted white yacht hull
        hull_d = (
            "M318,336 Q508,348 698,336 L688,376 Q664,394 522,396 Q388,396 356,374 Z"
        )
        t.append(
            f'<path d="{hull_d}" fill="url(#{p}_hull)" stroke="{INK}" stroke-width="2.4" stroke-linejoin="round"/>'
            # Lower hull shadow & deep navy-teal waterline stripe
            f'<path d="M342,366 Q508,378 690,364 L686,378 Q664,394 522,396 Q390,396 356,374 Z" '
            f'fill="url(#{p}_hull_sh)" opacity="0.88"/>'
            '<path d="M332,354 Q508,366 694,352" fill="none" stroke="#1B556B" stroke-width="3.6"/>'
            '<path d="M336,360 Q508,372 692,358" fill="none" stroke="#C99A4E" stroke-width="1.4" opacity="0.88"/>'
            # Hull waterline boot-top stripe (dark teal-red)
            '<path d="M352,374 Q508,386 686,374 L682,383 Q512,395 360,382 Z" fill="#173847"/>'
            # Crisp top specular highlight along hull sheer
            '<path d="M330,342 Q508,354 690,342" fill="none" stroke="#FFFFFF" stroke-width="2.2" opacity="0.72"/>'
        )

        # Hull lettering: "CHRISTINA ROSE" — crisp, centered, high-contrast navy on white hull
        t.append(
            '<g transform="translate(508, 353) rotate(-0.8)">'
            '<text x="0" y="0" text-anchor="middle" font-family="Georgia, Times New Roman, serif" '
            'font-size="13.5" font-weight="bold" fill="#10293B" letter-spacing="2.4">CHRISTINA ROSE</text>'
            '</g>'
        )

        parts.append(f'<g id="s407-tekne">{"".join(t)}</g>')

    # ── 4. SIS_KATMAN: Semi-transparent drifting harbor mist (R18-HAREKET) ──
    if _katman_aktif(katmanlar, "sis_katman"):
        s: list[str] = []
        s.append(f'<rect x="-40" y="196" width="1040" height="106" fill="url(#{p}_mist)"/>')
        mist_banks = [
            (150, 268, 220, 26, 0.24),
            (460, 250, 270, 24, 0.20),
            (790, 264, 240, 28, 0.24),
            (290, 326, 230, 22, 0.16),
            (720, 336, 250, 24, 0.16),
            (120, 412, 240, 22, 0.12),
        ]
        for mx, my, rx, ry, op in mist_banks:
            s.append(f'<ellipse cx="{mx}" cy="{my}" rx="{rx}" ry="{ry}" fill="#D6ECEB" opacity="{op:.2f}"/>')
        parts.append(f'<g id="s407-sis_katman">{"".join(s)}</g>')

    # ── 5. SAHNE: Foreground wooden dock planks, bollards & mooring ropes ────
    if _katman_aktif(katmanlar, "sahne"):
        f: list[str] = []
        # Diagonal weathered timber dock deck (bottom-left foreground)
        f.append(
            f'<path d="M0,418 L346,456 L422,540 L0,540 Z" fill="url(#{p}_wood)" stroke="{INK}" stroke-width="2.4" stroke-linejoin="round"/>'
            f'<path d="M0,418 L346,456 L342,468 L0,432 Z" fill="url(#{p}_wood_top)" stroke="{INK}" stroke-width="1.6"/>'
        )
        # Individual plank seams & wood grain
        plank_lines = [
            (0, 444, 358, 480),
            (0, 466, 376, 504),
            (0, 492, 396, 530),
            (0, 518, 360, 540),
        ]
        for x1, y1, x2, y2 in plank_lines:
            f.append(
                f'<path d="M{x1},{y1} L{x2},{y2}" fill="none" stroke="#18100B" stroke-width="2.0" opacity="0.85"/>'
                f'<path d="M{x1},{y1 + 2} L{x2},{y2 + 2}" fill="none" stroke="#6E5340" stroke-width="1.0" opacity="0.35"/>'
            )

        # Heavy foreground timber piling / dock bollard (left)
        f.append(
            f'<path d="M48,370 L98,370 L102,516 L44,516 Z" fill="url(#{p}_wood)" stroke="{INK}" stroke-width="2.4" stroke-linejoin="round"/>'
            f'<ellipse cx="73" cy="370" rx="25" ry="7.5" fill="#705541" stroke="{INK}" stroke-width="2.0"/>'
            '<ellipse cx="73" cy="370" rx="16" ry="4.4" fill="none" stroke="#3D2B1F" stroke-width="1.2" opacity="0.7"/>'
            # Vertical wood grain cracks on piling
            '<path d="M60,384 L58,504 M78,386 L80,508 M89,382 L90,486" fill="none" stroke="#221710" stroke-width="1.3" opacity="0.72"/>'
        )

        # Second smaller dock piling & cast-iron mooring cleat (mid-foreground)
        f.append(
            f'<path d="M276,416 L310,416 L312,482 L274,482 Z" fill="url(#{p}_wood)" stroke="{INK}" stroke-width="2.1"/>'
            f'<ellipse cx="293" cy="416" rx="17" ry="5.5" fill="#6D533F" stroke="{INK}" stroke-width="1.8"/>'
            # Cast iron cleat on pier edge
            f'<path d="M188,452 L222,456 L218,464 L184,460 Z" fill="#2A333B" stroke="{INK}" stroke-width="1.5"/>'
            f'<path d="M196,450 L214,452 L212,445 L198,444 Z" fill="#3B4752" stroke="{INK}" stroke-width="1.4"/>'
        )

        # Thick hemp mooring rope wrapped around the piling and trailing toward the yacht bow
        for k in range(4):
            ry = 412 + k * 7.5
            f.append(
                f'<path d="M44,{ry:.1f} Q73,{ry + 8:.1f} 102,{ry:.1f}" '
                f'fill="none" stroke="#A68B64" stroke-width="5.6" stroke-linecap="round"/>'
                f'<path d="M44,{ry:.1f} Q73,{ry + 8:.1f} 102,{ry:.1f}" '
                f'fill="none" stroke="#2B1F14" stroke-width="1.2" stroke-linecap="round"/>'
            )
        # Sweeping mooring line from foreground piling to boat bow
        f.append(
            '<path d="M98,424 Q210,456 322,340" fill="none" stroke="#1B130C" stroke-width="5.4" stroke-linecap="round"/>'
            '<path d="M98,424 Q210,456 322,340" fill="none" stroke="#B6996E" stroke-width="3.2" stroke-linecap="round"/>'
            # Coiled rope resting on pier planks
            '<ellipse cx="144" cy="498" rx="34" ry="11" fill="none" stroke="#9C805A" stroke-width="5.0"/>'
            '<ellipse cx="144" cy="498" rx="23" ry="7.2" fill="none" stroke="#B5986E" stroke-width="4.2"/>'
            '<ellipse cx="144" cy="498" rx="13" ry="4.0" fill="none" stroke="#8C714D" stroke-width="3.4"/>'
        )

        parts.append(f'<g id="s407-sahne">{"".join(f)}</g>')

    # ── 6. TUZAK_HALKA: Red Company/CAD Closing Trap Rings + Alert HUD ──────
    if _katman_aktif(katmanlar, "tuzak_halka"):
        tr: list[str] = []
        # Concentric red tactical trap ellipses tightening around Christina Rose & pier
        cx, cy = 516, 368
        tr.append(
            f'<ellipse cx="{cx}" cy="{cy}" rx="284" ry="84" fill="none" stroke="{RED_TRAP}" stroke-width="1.8" '
            f'stroke-dasharray="14 8" opacity="0.72"/>'
            f'<ellipse cx="{cx}" cy="{cy}" rx="234" ry="68" fill="none" stroke="{RED_GLOW}" stroke-width="2.2" '
            f'opacity="0.88"/>'
            f'<ellipse cx="{cx}" cy="{cy}" rx="184" ry="52" fill="none" stroke="{RED_TRAP}" stroke-width="1.3" '
            f'stroke-dasharray="6 6" opacity="0.65"/>'
        )
        # 4 inward-pointing red trap convergence chevrons on outer ellipse diagonals (never overlapping boom)
        arrows = [
            (256, 304, 286, 318),  # top-left inward
            (776, 304, 746, 318),  # top-right inward
            (256, 434, 286, 420),  # bottom-left inward
            (776, 434, 746, 420),  # bottom-right inward
        ]
        for x1, y1, x2, y2 in arrows:
            dx, dy = x2 - x1, y2 - y1
            ang = math.atan2(dy, dx)
            ah1 = (x2 - 9 * math.cos(ang - 0.52), y2 - 9 * math.sin(ang - 0.52))
            ah2 = (x2 - 9 * math.cos(ang + 0.52), y2 - 9 * math.sin(ang + 0.52))
            tr.append(
                f'<path d="M{x1},{y1} L{x2},{y2}" fill="none" stroke="{RED_GLOW}" stroke-width="2.4" stroke-linecap="round"/>'
                f'<path d="M{ah1[0]:.1f},{ah1[1]:.1f} L{x2},{y2} L{ah2[0]:.1f},{ah2[1]:.1f}" '
                f'fill="none" stroke="{RED_GLOW}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>'
            )

        # Tactical red vector lines linking waterfront police patrol to yacht trap ring
        tr.append(
            f'<path d="M126,246 L316,326 M228,248 L368,318" fill="none" stroke="{RED_TRAP}" '
            f'stroke-width="1.3" stroke-dasharray="5 5" opacity="0.72"/>'
            f'<circle cx="126" cy="246" r="5.5" fill="none" stroke="{RED_GLOW}" stroke-width="1.5"/>'
            f'<circle cx="228" cy="248" r="5.0" fill="none" stroke="{RED_GLOW}" stroke-width="1.5"/>'
        )

        # Zero-overflow Red Company Trap HUD (top-right: width=278px, >=26px padding both sides)
        hx, hy, hw, hh = 658, 20, 278, 56
        tr.append(
            f'<g transform="translate({hx},{hy})">'
            f'<rect x="0" y="0" width="{hw}" height="{hh}" rx="5" fill="#14090D" fill-opacity="0.90" '
            f'stroke="{RED_TRAP}" stroke-width="1.7"/>'
            f'<rect x="0" y="0" width="5" height="{hh}" rx="2" fill="{RED_TRAP}"/>'
            f'<circle cx="20" cy="17" r="3.6" fill="{RED_GLOW}"/>'
            f'<text x="31" y="21" font-family="Consolas, DejaVu Sans Mono, monospace" font-size="9.5" '
            f'font-weight="bold" fill="#F2A4AA" letter-spacing="0.9">ALERT · PERIMETER LOCK</text>'
            f'<text x="142" y="44" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif" font-size="15" '
            f'font-weight="bold" fill="#FFF2F3" letter-spacing="1.1">COMPANY TRAP · PANAMA</text>'
            f'</g>'
        )

        parts.append(f'<g id="s407-tuzak_halka">{"".join(tr)}</g>')

    # ── 7. PLAN: Cyan #7FE6FF CAD Harbor Grid & Vessel Callouts ─────────────
    if _katman_aktif(katmanlar, "plan"):
        pl: list[str] = []
        # Subtle cyan CAD horizon ruler & corner registration brackets
        pl.append(
            f'<path d="M18,242 L68,242 M892,242 L942,242" fill="none" stroke="{PLAN}" stroke-width="1.1" opacity="0.55"/>'
            f'<path d="M18,18 L40,18 M18,18 L18,40 M942,522 L920,522 M942,522 L942,500" '
            f'fill="none" stroke="{PLAN}" stroke-width="1.4" opacity="0.72"/>'
        )
        # Top-left clean CAD Location Tag: "PANAMA CITY · HARBOR SECTOR" (width=266, >=24px padding)
        pl.append(
            '<g transform="translate(24, 20)">'
            f'<rect x="0" y="0" width="266" height="32" rx="4" fill="#071520" fill-opacity="0.86" '
            f'stroke="{PLAN}" stroke-width="1.3"/>'
            f'<rect x="0" y="0" width="4" height="32" rx="1.5" fill="{PLAN}"/>'
            '<text x="135" y="20" text-anchor="middle" font-family="Consolas, DejaVu Sans Mono, monospace" '
            f'font-size="10.5" font-weight="bold" fill="{PLAN_CORE}" letter-spacing="1.0">PANAMA CITY · HARBOR SECTOR</text>'
            '</g>'
        )
        # Bottom-right CAD Vessel Callout leader line to Christina Rose (width=224, >=24px padding)
        pl.append(
            f'<path d="M626,386 L676,472 L706,472" fill="none" stroke="{PLAN}" stroke-width="1.3" opacity="0.85"/>'
            f'<circle cx="626" cy="386" r="3.4" fill="{PLAN}"/>'
            '<g transform="translate(706, 456)">'
            f'<rect x="0" y="0" width="224" height="32" rx="4" fill="#071520" fill-opacity="0.88" '
            f'stroke="{PLAN}" stroke-width="1.3"/>'
            '<text x="112" y="20" text-anchor="middle" font-family="Consolas, DejaVu Sans Mono, monospace" '
            f'font-size="10" font-weight="bold" fill="{PLAN_CORE}" letter-spacing="0.9">VESSEL · CHRISTINA ROSE</text>'
            '</g>'
        )

        parts.append(f'<g id="s407-plan">{"".join(pl)}</g>')

    # ── 8. ONPLAN: Foreground mist motes & vignette ──────────────────────────
    if _katman_aktif(katmanlar, "onplan"):
        op_l: list[str] = []
        for _ in range(26):
            dx = rng.uniform(20, 940)
            dy = rng.uniform(30, 510)
            dr = rng.uniform(0.9, 2.2)
            op = rng.uniform(0.14, 0.36)
            op_l.append(f'<circle cx="{dx:.1f}" cy="{dy:.1f}" r="{dr:.1f}" fill="#DFF5F4" opacity="{op:.2f}"/>')
        op_l.append(f'<rect x="0" y="0" width="{W_SCENE}" height="{H_SCENE}" fill="url(#{p}_vig)"/>')
        parts.append(f'<g id="s407-onplan">{"".join(op_l)}</g>')

    return defs, "".join(parts)


# =============================================================================
# SCENE 4.08: SONA'S IRON GATE (ACT V OPEN LOOP — NO GUARDS INSIDE)
# =============================================================================
def _draw_sona_gate_leaf(side: str, p: str) -> str:
    """Massive rusted iron Sona prison gate leaf (width=496px, y=120..540).
    - `side == "left"`  : x = -140 .. 356  (inner edge x=356; slides +122px to x=478 when slammed shut)
    - `side == "right"` : x =  604 .. 1100 (inner edge x=604; slides -122px to x=482 when slammed shut)
    """
    is_left = side == "left"
    x0 = -140 if is_left else 604
    w = 496
    x1 = x0 + w
    y0, y1 = 120, 540
    h = y1 - y0
    inner_x = x1 if is_left else x0

    g: list[str] = []

    # Outer heavy steel frame
    g.append(
        f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" fill="url(#{p}_iron)" '
        f'stroke="{INK_WARM}" stroke-width="3.2"/>'
    )

    # Upper rusted prison grating window band (y=142..246)
    grate_x = x0 + 28
    grate_w = w - 56
    g.append(
        f'<rect x="{grate_x}" y="144" width="{grate_w}" height="104" fill="#1C1410" fill-opacity="0.58" '
        f'stroke="#231914" stroke-width="2.4"/>'
    )
    # Heavy vertical iron bars inside grating
    for bx in range(grate_x + 20, grate_x + grate_w - 8, 26):
        g.append(
            f'<rect x="{bx}" y="144" width="6.5" height="104" fill="#3B2A22" stroke="{INK_WARM}" stroke-width="1.2"/>'
            f'<path d="M{bx + 1.5},146 L{bx + 1.5},246" fill="none" stroke="#7A5640" stroke-width="1.1" opacity="0.55"/>'
        )
    # Horizontal cross-bar through grating
    g.append(
        f'<rect x="{grate_x}" y="191" width="{grate_w}" height="10" fill="#463126" stroke="{INK_WARM}" stroke-width="1.6"/>'
    )

    # Lower solid riveted steel armor panels (y=266..522)
    panel_w = (w - 64) // 2
    for pi in range(2):
        px = x0 + 24 + pi * (panel_w + 16)
        g.append(
            f'<rect x="{px}" y="268" width="{panel_w}" height="248" fill="url(#{p}_iron_panel)" '
            f'stroke="#241914" stroke-width="2.2"/>'
            # Diagonal heavy steel X-bracing
            f'<path d="M{px + 6},274 L{px + panel_w - 6},510 M{px + panel_w - 6},274 L{px + 6},510" '
            f'fill="none" stroke="#2D1F18" stroke-width="9.0" opacity="0.52"/>'
            f'<path d="M{px + 6},274 L{px + panel_w - 6},510 M{px + panel_w - 6},274 L{px + 6},510" '
            f'fill="none" stroke="#5E402E" stroke-width="3.6" opacity="0.55"/>'
        )

    # Corrosion / rust drip streaks & peeling oxidized patches
    rust_rng = random.Random(4081 if is_left else 4082)
    for _ in range(18):
        rx = rust_rng.uniform(x0 + 18, x1 - 36)
        ry = rust_rng.uniform(252, 480)
        rw = rust_rng.uniform(14, 48)
        rh = rust_rng.uniform(10, 32)
        op = rust_rng.uniform(0.22, 0.46)
        col = "#7B3A1D" if rust_rng.random() < 0.6 else "#542716"
        g.append(f'<ellipse cx="{rx:.1f}" cy="{ry:.1f}" rx="{rw * 0.5:.1f}" ry="{rh * 0.5:.1f}" fill="{col}" opacity="{op:.2f}"/>')
    for _ in range(14):
        sx = rust_rng.uniform(x0 + 22, x1 - 22)
        sy = rust_rng.uniform(140, 340)
        sh = rust_rng.uniform(35, 110)
        g.append(
            f'<path d="M{sx:.1f},{sy:.1f} L{sx:.1f},{sy + sh:.1f}" fill="none" '
            f'stroke="#6C331A" stroke-width="{rust_rng.uniform(1.4, 3.2):.1f}" opacity="0.38" stroke-linecap="round"/>'
        )

    # Heavy horizontal steel locking beams (top, mid, bottom)
    for by in (122, 248, 384, 518):
        g.append(
            f'<rect x="{x0}" y="{by}" width="{w}" height="18" fill="#3B2B23" stroke="{INK_WARM}" stroke-width="1.8"/>'
            f'<path d="M{x0 + 4},{by + 3} L{x1 - 4},{by + 3}" fill="none" stroke="#8C674E" stroke-width="1.3" opacity="0.45"/>'
        )
        # Steel rivets along beam
        for rvx in range(x0 + 18, x1 - 12, 34):
            g.append(
                f'<circle cx="{rvx}" cy="{by + 9}" r="3.0" fill="#231813" stroke="#7A5944" stroke-width="0.8"/>'
            )

    # Inner vertical locking flange + sunlit rim highlight on the meeting edge
    flange_x = x1 - 22 if is_left else x0
    rim_x = x1 - 2 if is_left else x0 + 2
    g.append(
        f'<rect x="{flange_x}" y="{y0}" width="22" height="{h}" fill="#2E211B" stroke="{INK_WARM}" stroke-width="2.0"/>'
        f'<path d="M{rim_x},{y0 + 2} L{rim_x},{y1 - 2}" fill="none" stroke="#F4D393" stroke-width="2.6" opacity="0.78"/>'
    )
    # Heavy slide-bolt latch hardware near center meeting edge (y=360..404)
    if is_left:
        g.append(
            f'<rect x="{inner_x - 56}" y="366" width="52" height="24" rx="3" fill="#2A1F19" stroke="{INK_WARM}" stroke-width="1.8"/>'
            f'<rect x="{inner_x - 42}" y="373" width="44" height="10" rx="2" fill="#5D4435" stroke="{INK_WARM}" stroke-width="1.4"/>'
            f'<circle cx="{inner_x - 44}" cy="378" r="5" fill="#7D5C48" stroke="{INK_WARM}" stroke-width="1.3"/>'
        )
    else:
        g.append(
            f'<rect x="{inner_x + 4}" y="366" width="52" height="24" rx="3" fill="#2A1F19" stroke="{INK_WARM}" stroke-width="1.8"/>'
            f'<rect x="{inner_x + 8}" y="372" width="16" height="12" rx="2" fill="#17100D" stroke="#6E523F" stroke-width="1.2"/>'
            f'<path d="M{inner_x + 28},386 Q{inner_x + 36},412 {inner_x + 24},428" fill="none" stroke="#574135" stroke-width="4.2" stroke-linecap="round"/>'
        )

    return "".join(g)


def set_408_sona_kapisi(
    katmanlar: set[str] | list[str] | None = None,
) -> tuple[str, str]:
    """Scorching yellow-gray Sona Prison Iron Gate (Act V Open Loop) with R18-HAREKET layers:
      - `uzak`     : Scorching yellow-gray Panama desert sky, blazing sun, distant hills
      - `orta`     : Sona concrete fortress walls, barbed-wire watchtowers, `SONA` arch, cracked desert ground
      - `sahne`    : Locked full-body Michael v3 (`K.michael_figur("kararli", plan=False, numara_goster=False)`)
      - `kapi_sol` : Massive rusted iron left gate leaf (slides right to slam shut in animatic)
      - `kapi_sag` : Massive rusted iron right gate leaf (slides left to slam shut in animatic)
      - `plan`     : `ACT V · SONA · NO GUARDS INSIDE` clean CAD HUD + gate-closing vectors
      - `onplan`   : Desert dust clouds, heat-shimmer wisps & sun glare vignette
    """
    rng = random.Random(408)
    p = _uid("s408")

    defs = f"""
    <linearGradient id="{p}_sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#8C836B"/>
      <stop offset="35%" stop-color="#B9AC88"/>
      <stop offset="72%" stop-color="#DDD0A6"/>
      <stop offset="100%" stop-color="#EFE4BE"/>
    </linearGradient>
    <radialGradient id="{p}_sun" cx="0.50" cy="0.36" r="0.44">
      <stop offset="0%" stop-color="#FFFDF0" stop-opacity="0.96"/>
      <stop offset="22%" stop-color="#FCE9B2" stop-opacity="0.62"/>
      <stop offset="58%" stop-color="#D8BE82" stop-opacity="0.22"/>
      <stop offset="100%" stop-color="#B9AC88" stop-opacity="0.0"/>
    </radialGradient>
    <linearGradient id="{p}_concrete" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#8A8272"/>
      <stop offset="45%" stop-color="#756E60"/>
      <stop offset="100%" stop-color="#524C41"/>
    </linearGradient>
    <linearGradient id="{p}_concrete_dk" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#615B4F"/>
      <stop offset="100%" stop-color="#3E3931"/>
    </linearGradient>
    <linearGradient id="{p}_ground" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#C8B486"/>
      <stop offset="45%" stop-color="#AE986C"/>
      <stop offset="100%" stop-color="#7E6B49"/>
    </linearGradient>
    <linearGradient id="{p}_iron" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#543D30"/>
      <stop offset="42%" stop-color="#422F25"/>
      <stop offset="78%" stop-color="#35251D"/>
      <stop offset="100%" stop-color="#271B15"/>
    </linearGradient>
    <linearGradient id="{p}_iron_panel" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#4E382C"/>
      <stop offset="55%" stop-color="#3D2B22"/>
      <stop offset="100%" stop-color="#2D1F18"/>
    </linearGradient>
    <radialGradient id="{p}_dust_glow" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0%" stop-color="#EBD9AC" stop-opacity="0.34"/>
      <stop offset="100%" stop-color="#C8B282" stop-opacity="0.0"/>
    </radialGradient>
    <radialGradient id="{p}_vig" cx="0.5" cy="0.48" r="0.68">
      <stop offset="55%" stop-color="#1E170F" stop-opacity="0.0"/>
      <stop offset="100%" stop-color="#17100A" stop-opacity="0.58"/>
    </radialGradient>
    """

    parts: list[str] = []

    # ── 1. UZAK: Scorching yellow-gray desert sky & blazing sun ─────────────
    if _katman_aktif(katmanlar, "uzak"):
        u: list[str] = []
        u.append(f'<rect x="0" y="0" width="{W_SCENE}" height="390" fill="url(#{p}_sky)"/>')
        u.append(f'<rect x="0" y="0" width="{W_SCENE}" height="390" fill="url(#{p}_sun)"/>')
        # Blazing sun core right behind the Sona archway gap
        u.append(
            '<circle cx="480" cy="186" r="34" fill="#FFFDF4" opacity="0.90"/>'
            '<circle cx="480" cy="186" r="76" fill="#FAE6B0" opacity="0.28"/>'
        )
        # Parched heat-haze horizontal bands
        u.append(
            '<rect x="0" y="218" width="960" height="22" fill="#F2E4BE" opacity="0.24"/>'
            '<rect x="0" y="274" width="960" height="30" fill="#E6D3A3" opacity="0.22"/>'
        )
        # Distant dry Panamanian hills & hazy interior prison blocks visible through gateway
        u.append(
            '<path d="M0,336 Q160,302 320,318 Q480,330 640,314 Q800,300 960,326 L960,390 L0,390 Z" '
            'fill="#9A8C6C" opacity="0.65"/>'
            # Distant weathered Sona inner yard cellblock silhouette
            '<rect x="360" y="278" width="240" height="92" fill="#8B7E64" opacity="0.52"/>'
            '<rect x="386" y="294" width="18" height="26" fill="#5D5340" opacity="0.45"/>'
            '<rect x="424" y="294" width="18" height="26" fill="#5D5340" opacity="0.45"/>'
            '<rect x="518" y="294" width="18" height="26" fill="#5D5340" opacity="0.45"/>'
            '<rect x="556" y="294" width="18" height="26" fill="#5D5340" opacity="0.45"/>'
        )
        parts.append(f'<g id="s408-uzak">{"".join(u)}</g>')

    # ── 2. ORTA: Sona concrete walls, barbed-wire towers, arch & cracked earth ─
    if _katman_aktif(katmanlar, "orta"):
        m: list[str] = []

        # Cracked parched desert ground (y=366..540)
        m.append(f'<rect x="0" y="366" width="{W_SCENE}" height="174" fill="url(#{p}_ground)"/>')
        # Perspective dirt track leading through the Sona gate
        m.append(
            '<path d="M356,366 L604,366 L760,540 L200,540 Z" fill="#BCA67A" opacity="0.62"/>'
            '<path d="M402,366 L558,366 L640,540 L320,540 Z" fill="#CEBA8E" opacity="0.38"/>'
        )
        # Deep dry desert mud/earth fissures & cracks (prominent around doorway & foreground)
        cracks = [
            "M180,454 L236,466 L268,494 L318,504",
            "M236,466 L216,498 L194,524",
            "M358,488 L412,502 L448,530",
            "M412,502 L444,486 L486,494 L526,518 L572,534",
            "M444,514 L468,526 L496,518",
            "M530,504 L576,490 L628,512 L682,506",
            "M576,490 L594,462 L636,450",
            "M664,474 L722,492 L774,484",
            "M392,418 L434,426 L460,444",
            "M516,422 L552,434 L574,424",
            "M372,458 L416,468 L442,456",
            "M524,466 L558,476 L588,464",
        ]
        for cd in cracks:
            m.append(f'<path d="{cd}" fill="none" stroke="#4D3D26" stroke-width="1.9" opacity="0.78" stroke-linecap="round"/>')
            m.append(f'<path d="{cd}" fill="none" stroke="#EFE0B8" stroke-width="0.8" opacity="0.38" transform="translate(1,1)"/>')
        # Small desert stones & pebbles
        for _ in range(36):
            sx = rng.uniform(40, 920)
            sy = rng.uniform(376, 532)
            sr = rng.uniform(1.4, 4.0)
            m.append(f'<ellipse cx="{sx:.1f}" cy="{sy:.1f}" rx="{sr:.1f}" ry="{sr * 0.55:.1f}" fill="#6B5A3E" opacity="0.58"/>')

        # Left & Right perimeter guard watchtowers (behind main concrete walls)
        for tx in (68, 818):
            m.append(
                f'<rect x="{tx}" y="38" width="74" height="84" fill="url(#{p}_concrete_dk)" stroke="{INK_WARM}" stroke-width="2.0"/>'
                f'<path d="M{tx - 10},38 L{tx + 84},38 L{tx + 76},24 L{tx - 2},24 Z" fill="#464036" stroke="{INK_WARM}" stroke-width="1.8"/>'
                f'<rect x="{tx + 10}" y="52" width="54" height="22" fill="#231F1A" stroke="{INK_WARM}" stroke-width="1.4"/>'
                f'<path d="M{tx + 28},52 L{tx + 28},74 M{tx + 46},52 L{tx + 46},74" fill="none" stroke="#575044" stroke-width="1.4"/>'
            )

        # Massive Sona Concrete Walls (left & right pillars + heavy top gateway lintel)
        m.append(
            # Left concrete wall bastion
            f'<rect x="0" y="92" width="218" height="310" fill="url(#{p}_concrete)" stroke="{INK_WARM}" stroke-width="2.4"/>'
            # Right concrete wall bastion
            f'<rect x="742" y="92" width="218" height="310" fill="url(#{p}_concrete)" stroke="{INK_WARM}" stroke-width="2.4"/>'
            # Heavy central gateway lintel / concrete arch header spanning x=186..774, y=22..126
            f'<path d="M182,126 L182,22 L778,22 L778,126 L732,126 L732,118 L228,118 L228,126 Z" '
            f'fill="url(#{p}_concrete)" stroke="{INK_WARM}" stroke-width="2.6" stroke-linejoin="round"/>'
            # Deep inner arch shadow underside
            '<rect x="224" y="114" width="512" height="12" fill="#2B251D" opacity="0.78"/>'
            # Concrete column jambs framing the iron gate opening
            f'<rect x="192" y="124" width="44" height="288" fill="url(#{p}_concrete_dk)" stroke="{INK_WARM}" stroke-width="2.2"/>'
            f'<rect x="724" y="124" width="44" height="288" fill="url(#{p}_concrete_dk)" stroke="{INK_WARM}" stroke-width="2.2"/>'
        )

        # Concrete weathering streaks, bullet-pock scars & expansion joints
        for cx in (64, 146, 214, 746, 824, 902):
            m.append(f'<path d="M{cx},94 L{cx},398" fill="none" stroke="#3F3A31" stroke-width="1.3" opacity="0.48"/>')
        for _ in range(16):
            wx = rng.uniform(194, 766)
            wy = rng.uniform(26, 114)
            wh = rng.uniform(16, 46)
            m.append(f'<path d="M{wx:.1f},{wy:.1f} L{wx:.1f},{wy + wh:.1f}" fill="none" stroke="#474136" stroke-width="2.0" opacity="0.28"/>')

        # Coiled razor / barbed wire along top of concrete walls
        for start_x, end_x, wy in [(0, 182, 86), (778, 960, 86), (186, 774, 16)]:
            # Angled fence posts
            for px in range(start_x + 12, end_x, 44):
                m.append(f'<path d="M{px},{wy + 6} L{px - 6},{wy - 12}" fill="none" stroke="#2D2720" stroke-width="2.0"/>')
            # Coiled concertina wire loops
            for wx in range(start_x + 4, end_x - 4, 16):
                m.append(
                    f'<ellipse cx="{wx}" cy="{wy - 2}" rx="8.5" ry="6.5" fill="none" '
                    f'stroke="#2B241E" stroke-width="1.2" opacity="0.82"/>'
                )

        # Weathered Sona concrete header plaque: "PENITENCIARÍA FEDERAL DE SONA" + bold "SONA"
        # Plaque spans x=244..716 (width=472px) — massive padding on both sides, zero overflow!
        m.append(
            f'<rect x="244" y="34" width="472" height="74" rx="3" fill="#4B4439" stroke="#29241D" stroke-width="2.2"/>'
            '<rect x="250" y="40" width="460" height="62" rx="2" fill="none" stroke="#756C5C" stroke-width="1.1" opacity="0.72"/>'
            # Top sub-header
            '<text x="480" y="61" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif" '
            'font-size="13.5" font-weight="bold" fill="#DDD2B8" letter-spacing="1.8">PENITENCIARÍA FEDERAL DE SONA</text>'
            # Bold weathered SONA lettering
            '<text x="480" y="94" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif" '
            'font-size="30" font-weight="bold" fill="#F2E6C8" letter-spacing="10">SONA</text>'
            # Subtle grime / crack across concrete sign
            '<path d="M312,36 L326,64 L318,98 M640,38 L632,74 L646,104" fill="none" stroke="#2E2921" stroke-width="1.4" opacity="0.55"/>'
        )

        parts.append(f'<g id="s408-orta">{"".join(m)}</g>')

    # ── 3. SAHNE: Locked Full-Body Michael v3 (Single R4-PARALAKS Layer) ────
    if _katman_aktif(katmanlar, "sahne"):
        sh: list[str] = []
        # Ground cast shadow on the scorching cracked desert floor (sun behind/overhead)
        sh.append(
            '<ellipse cx="480" cy="492" rx="56" ry="11.5" fill="#3C2F1C" opacity="0.64"/>'
            '<path d="M444,491 L516,491 L542,532 L418,532 Z" fill="#3D301D" opacity="0.30"/>'
        )
        # Locked Michael v3 full-body figure (slim F3 proportions, both arms complete, no Fox River number)
        michael_svg = K.michael_figur("kararli", plan=False, numara_goster=False)
        sh.append(f'<g transform="translate(480, 491) scale(0.495)">{michael_svg}</g>')
        parts.append(f'<g id="s408-sahne">{"".join(sh)}</g>')

    # ── 4. KAPI_SOL: Massive Rusted Iron Left Gate Leaf (R18-HAREKET) ───────
    if _katman_aktif(katmanlar, "kapi_sol"):
        parts.append(f'<g id="s408-kapi_sol">{_draw_sona_gate_leaf("left", p)}</g>')

    # ── 5. KAPI_SAG: Massive Rusted Iron Right Gate Leaf (R18-HAREKET) ──────
    if _katman_aktif(katmanlar, "kapi_sag"):
        parts.append(f'<g id="s408-kapi_sag">{_draw_sona_gate_leaf("right", p)}</g>')

    # ── 6. PLAN: Act V CAD HUD ("ACT V · SONA · NO GUARDS INSIDE") ──────────
    if _katman_aktif(katmanlar, "plan"):
        pl: list[str] = []
        # Subtle cyan CAD gate-closing vector indicators on left & right gate inner edges
        pl.append(
            # Left gate closing arrow (->)
            f'<path d="M312,308 L348,308 M339,301 L348,308 L339,315" fill="none" stroke="{PLAN}" '
            f'stroke-width="2.0" opacity="0.82" stroke-linecap="round" stroke-linejoin="round"/>'
            # Right gate closing arrow (<-)
            f'<path d="M648,308 L612,308 M621,301 L612,308 L621,315" fill="none" stroke="{PLAN}" '
            f'stroke-width="2.0" opacity="0.82" stroke-linecap="round" stroke-linejoin="round"/>'
            # Center seam alignment hairlines
            f'<path d="M480,132 L480,174 M480,498 L480,526" fill="none" stroke="{PLAN}" '
            f'stroke-width="1.2" stroke-dasharray="4 4" opacity="0.64"/>'
            # Corner CAD brackets
            f'<path d="M18,18 L38,18 M18,18 L18,38 M942,522 L922,522 M942,522 L942,502" '
            f'fill="none" stroke="{PLAN}" stroke-width="1.4" opacity="0.72"/>'
        )

        # Bottom-right clean CAD HUD: "ACT V · SONA · NO GUARDS INSIDE"
        # Box width=290px, text ~232px -> ~29px horizontal padding each side! Zero overflow!
        bx, by, bw, bh = 646, 464, 290, 54
        pl.append(
            f'<g transform="translate({bx},{by})">'
            f'<rect x="0" y="0" width="{bw}" height="{bh}" rx="5" fill="#120E0B" fill-opacity="0.90" '
            f'stroke="{RED_TRAP}" stroke-width="1.6"/>'
            f'<rect x="0" y="0" width="5" height="{bh}" rx="2" fill="{RED_TRAP}"/>'
            f'<circle cx="20" cy="17" r="3.4" fill="{RED_GLOW}"/>'
            '<text x="31" y="20.5" font-family="Consolas, DejaVu Sans Mono, monospace" font-size="9.0" '
            f'font-weight="bold" fill="{PLAN}" letter-spacing="0.7">OPEN LOOP · MAXIMUM CONTAINMENT</text>'
            '<text x="147" y="42.5" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif" font-size="12.5" '
            'font-weight="bold" fill="#FFF3E0" letter-spacing="0.7">ACT V · SONA · NO GUARDS INSIDE</text>'
            '</g>'
        )

        # Bottom-left small CAD tag: "GATE STATUS · CLOSING" (width=206px, >=26px padding)
        pl.append(
            '<g transform="translate(24, 486)">'
            f'<rect x="0" y="0" width="206" height="32" rx="4" fill="#120E0B" fill-opacity="0.88" '
            f'stroke="{PLAN}" stroke-width="1.3"/>'
            f'<rect x="0" y="0" width="4" height="32" rx="1.5" fill="{PLAN}"/>'
            '<text x="105" y="20" text-anchor="middle" font-family="Consolas, DejaVu Sans Mono, monospace" '
            f'font-size="10" font-weight="bold" fill="{PLAN_CORE}" letter-spacing="0.9">GATE STATUS · CLOSING</text>'
            '</g>'
        )

        parts.append(f'<g id="s408-plan">{"".join(pl)}</g>')

    # ── 7. ONPLAN: Desert dust clouds, heat shimmer & sun vignette ──────────
    if _katman_aktif(katmanlar, "onplan"):
        op_l: list[str] = []
        # Drifting low desert dust plumes
        for dx, dy, rx, ry in [(160, 492, 170, 34), (480, 514, 210, 30), (810, 488, 165, 36)]:
            op_l.append(f'<ellipse cx="{dx}" cy="{dy}" rx="{rx}" ry="{ry}" fill="url(#{p}_dust_glow)"/>')
        # Heat-shimmer refraction wisps in the sunlit central gap
        for hy in (188, 224, 266, 314, 360):
            op_l.append(
                f'<path d="M388,{hy} Q434,{hy - 5} 480,{hy} Q526,{hy + 5} 572,{hy}" '
                f'fill="none" stroke="#FFF4D0" stroke-width="1.4" opacity="0.22" stroke-linecap="round"/>'
            )
        # Floating desert dust motes
        for _ in range(30):
            mx = rng.uniform(24, 936)
            my = rng.uniform(34, 520)
            mr = rng.uniform(0.9, 2.3)
            op = rng.uniform(0.16, 0.42)
            op_l.append(f'<circle cx="{mx:.1f}" cy="{my:.1f}" r="{mr:.1f}" fill="#F6E5BD" opacity="{op:.2f}"/>')
        op_l.append(f'<rect x="0" y="0" width="{W_SCENE}" height="{H_SCENE}" fill="url(#{p}_vig)"/>')
        parts.append(f'<g id="s408-onplan">{"".join(op_l)}</g>')

    return defs, "".join(parts)


# =============================================================================
# RENDER & AUDIT HELPERS (1920x1080 -> 1280x720 v1 + R13 200% QC)
# =============================================================================
def _render_svg(defs: str, body: str, width: int = 1920, height: int = 1080) -> Image.Image:
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W_SCENE} {H_SCENE}" '
        f'width="{width}" height="{height}">'
        f'<defs>{defs}</defs>{body}</svg>'
    )
    png_bytes = resvg_py.svg_to_bytes(svg)
    return Image.open(io.BytesIO(png_bytes)).convert("RGBA")


def _audit_fill_none(svg_body: str, label: str) -> int:
    """Count any <path ... stroke=...> that lacks an explicit fill= attribute."""
    bad = 0
    for m in re.finditer(r"<path\b[^>]*>", svg_body):
        tag = m.group(0)
        if "stroke=" in tag and "fill=" not in tag:
            bad += 1
    if bad:
        print(f"[AUDIT WARN] {label}: {bad} stroked <path> missing fill=")
    return bad


def _load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = (
        ["C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf"]
        if bold
        else ["C:/Windows/Fonts/segoeui.ttf", "C:/Windows/Fonts/arial.ttf"]
    )
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def _draw_card_bg(w: int, h: int) -> Image.Image:
    img = Image.new("RGBA", (w, h), (9, 15, 22, 255))
    draw = ImageDraw.Draw(img)
    for y in range(h):
        t = y / max(1, h - 1)
        c = (int(8 + 6 * t), int(14 + 8 * t), int(21 + 10 * t), 255)
        draw.line((0, y, w, y), fill=c)
    return img


def _draw_panel_box(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int]) -> None:
    draw.rounded_rectangle(box, radius=8, fill=(13, 21, 31, 255), outline=(34, 52, 72, 255), width=1)


def _draw_swatches(draw: ImageDraw.ImageDraw, x: int, y: int, colors: list[str], size: int = 20, gap: int = 6) -> None:
    for i, col in enumerate(colors):
        sx = x + i * (size + gap)
        draw.rounded_rectangle((sx, y, sx + size, y + size), radius=3, fill=col, outline=(220, 234, 245, 180), width=1)


def _verify_all_layers() -> None:
    """Verify each individual layer + full render for both scenes and audit fill='none'."""
    scenes = [
        (
            "set_407_panama_tekne",
            set_407_panama_tekne,
            ["uzak", "orta", "tekne", "sis_katman", "sahne", "tuzak_halka", "plan", "onplan"],
        ),
        (
            "set_408_sona_kapisi",
            set_408_sona_kapisi,
            ["uzak", "orta", "sahne", "kapi_sol", "kapi_sag", "plan", "onplan"],
        ),
    ]
    total_bad = 0
    for name, fn, layers in scenes:
        d_all, b_all = fn(None)
        total_bad += _audit_fill_none(b_all, f"{name}(None)")
        _render_svg(d_all, b_all, 480, 270)
        for lyr in layers:
            dl, bl = fn({lyr})
            assert f'id="s{name[4:7]}-{lyr}"' in bl, f"Missing layer id for {name}:{lyr}"
            total_bad += _audit_fill_none(bl, f"{name}({lyr})")
            _render_svg(dl, bl, 480, 270)
    assert total_bad == 0, f"Found {total_bad} stroked <path> elements without fill=!"
    print(f"[AUDIT OK] Both scenes + all 15 individual layers rendered cleanly; fill='none' missing = {total_bad}.")


def uret_kartlar(versiyon: str = "v1") -> tuple[Path, Path]:
    _verify_all_layers()

    d407, b407 = set_407_panama_tekne(None)
    d408, b408 = set_408_sona_kapisi(None)

    img_407 = _render_svg(d407, b407, 1920, 1080)
    img_408 = _render_svg(d408, b408, 1920, 1080)

    # Also render a slammed-shut preview of Sona gates (shifting kapi_sol +122, kapi_sag -122)
    b408_closed = (
        b408.replace('<g id="s408-kapi_sol">', '<g id="s408-kapi_sol" transform="translate(122,0)">')
        .replace('<g id="s408-kapi_sag">', '<g id="s408-kapi_sag" transform="translate(-122,0)">')
    )
    img_408_closed = _render_svg(d408, b408_closed, 960, 540)

    f_title = _load_font(19, bold=True)
    f_sub = _load_font(11, bold=False)
    f_card_t = _load_font(13, bold=True)
    f_card_s = _load_font(11, bold=False)
    f_small = _load_font(10, bold=True)

    # =========================================================================
    # OUTPUT 1: PRESENTATION SHEET (1280 x 720)
    # =========================================================================
    canvas = _draw_card_bg(1280, 720)
    draw = ImageDraw.Draw(canvas)

    draw.text((24, 13), "V12 · ACT IV PANAMA HARBOR (CHRISTINA ROSE) & SONA'S IRON GATE", fill="#EBF4FA", font=f_title)
    draw.text(
        (24, 37),
        "STYLE B+A HYBRID  ·  R18-HAREKET LIVE LAYERS  ·  LOCKED MICHAEL v3  ·  100% ENGLISH ZERO-OVERFLOW HUD",
        fill="#7E97B0",
        font=f_sub,
    )
    draw.line((24, 55, 1256, 55), fill="#213247", width=1)

    # --- LEFT PANEL: 4.07 PANAMA HARBOR & THE TRAP ---
    _draw_panel_box(draw, (22, 66, 634, 534))
    t407 = img_407.resize((588, 331), Image.Resampling.LANCZOS)
    canvas.paste(t407, (34, 96), t407)
    draw.rectangle((34, 96, 34 + 588, 96 + 331), outline="#2F4A62", width=1)
    draw.text((34, 74), "01 · 4.07 PANAMA HARBOR & THE TRAP", fill="#7FE6FF", font=f_card_t)
    draw.text((438, 76), "CHRISTINA ROSE · COMPANY TRAP", fill="#F2949C", font=f_card_s)

    draw.text((34, 438), "PALETTE", fill="#7FE6FF", font=f_small)
    _draw_swatches(draw, 34, 454, ["#0E2534", "#1B5662", "#E1EBF0", "#E03E3E", "#7FE6FF"], size=20, gap=6)
    draw.text((178, 438), "R18-HAREKET LAYERS (8)", fill="#9BB2C8", font=f_small)
    draw.text(
        (178, 454),
        "uzak · orta · tekne (live bob/drift) · sis_katman (mist drift)\n"
        "sahne (pier/ropes) · tuzak_halka (closing red rings) · plan · onplan",
        fill="#CFE0EE",
        font=f_card_s,
    )
    draw.text((34, 492), "HIGHLIGHTS", fill="#9BB2C8", font=f_small)
    draw.text(
        (34, 507),
        "Dawn misty Panama skyline, emerald water reflections, police lightbars & CHRISTINA ROSE.",
        fill="#BFD2E2",
        font=f_card_s,
    )

    # --- RIGHT PANEL: 4.08 SONA'S IRON GATE ---
    _draw_panel_box(draw, (646, 66, 1258, 534))
    t408 = img_408.resize((588, 331), Image.Resampling.LANCZOS)
    canvas.paste(t408, (658, 96), t408)
    draw.rectangle((658, 96, 658 + 588, 96 + 331), outline="#4C4334", width=1)
    draw.text((658, 74), "02 · 4.08 SONA'S IRON GATE (ACT V OPEN LOOP)", fill="#F6C876", font=f_card_t)
    draw.text((1068, 76), "SONA · NO GUARDS INSIDE", fill="#E8B982", font=f_card_s)

    draw.text((658, 438), "PALETTE", fill="#F6C876", font=f_small)
    _draw_swatches(draw, 658, 454, ["#B9AC88", "#756E60", "#422F25", "#E03E3E", "#7FE6FF"], size=20, gap=6)
    draw.text((802, 438), "R18-HAREKET LAYERS (7)", fill="#9BB2C8", font=f_small)
    draw.text(
        (802, 454),
        "uzak (desert sky) · orta (Sona arch/cracks) · sahne (Michael v3)\n"
        "kapi_sol (+122px) · kapi_sag (-122px) · plan · onplan",
        fill="#CFE0EE",
        font=f_card_s,
    )
    draw.text((658, 492), "LOCKED MICHAEL v3", fill="#9BB2C8", font=f_small)
    draw.text(
        (658, 507),
        "K.michael_figur('kararli', plan=False, numara_goster=False) centered in single `sahne` layer.",
        fill="#BFD2E2",
        font=f_card_s,
    )

    # --- BOTTOM STRIP: R18 GATE SLAM PROOF + SPECS ---
    _draw_panel_box(draw, (22, 546, 1258, 706))
    t408_c = img_408_closed.resize((256, 144), Image.Resampling.LANCZOS)
    canvas.paste(t408_c, (34, 554), t408_c)
    draw.rectangle((34, 554, 34 + 256, 554 + 144), outline="#5C4936", width=1)
    draw.text((306, 558), "R18-HAREKET GATE SLAM VERIFICATION (kapi_sol +122px / kapi_sag -122px)", fill="#F6C876", font=f_card_t)
    draw.text(
        (306, 580),
        "Left preview demonstrates live animatic gate-slam state: both massive rusted iron leaves\n"
        "converge from half-open framing to slam shut, leaving a 4px scorching sunlit slit at x=480\n"
        "with zero exposed edge gaps. All 15 layers verified individually and in full composite.",
        fill="#C9D8E6",
        font=f_card_s,
    )
    draw.text(
        (306, 650),
        "COMPLIANCE: 100% English Typography  ·  Zero Box Overflow (>=24px pad)  ·  fill='none' missing = 0  ·  karakter.py read-only",
        fill="#7FE6FF",
        font=f_small,
    )

    out_main = OUT_DIR / f"b4_set_panama_sona_{versiyon}.png"
    canvas.convert("RGB").save(out_main, quality=95)

    # =========================================================================
    # OUTPUT 2: R13 200% ZOOM QUALITY CONTROL CARD (1280 x 720 — 4 PANELS)
    # =========================================================================
    r13 = _draw_card_bg(1280, 720)
    d13 = ImageDraw.Draw(r13)
    d13.text((24, 13), "R13 · 200% ZOOM QUALITY CONTROL (PANAMA HARBOR & SONA'S IRON GATE)", fill="#EBF4FA", font=f_title)
    d13.text(
        (24, 37),
        "1:1 PIXEL CROPS FROM 1920×1080 SOURCE  ·  CHRISTINA ROSE, COMPANY TRAP, SONA ARCH + MICHAEL v3 & IRON GATE HUD",
        fill="#7E97B0",
        font=f_sub,
    )
    d13.line((24, 55, 1256, 55), fill="#213247", width=1)

    cw, ch = 600, 264
    crops = [
        (
            img_407,
            (1030, 700),
            "1 · 4.07 CHRISTINA ROSE YACHT HULL & RIGGING (200%)",
            "Crisp hull lettering, teak sheer, cabin portholes & emerald harbor reflections",
            (22, 66),
        ),
        (
            img_407,
            (1590, 120),
            "2 · 4.07 COMPANY TRAP · PANAMA HUD (200%)",
            "Zero-overflow red alert badge (>=26px padding) + dawn Panama horizon",
            (652, 66),
        ),
        (
            img_408,
            (960, 196),
            "3 · 4.08 SONA ARCH SIGNAGE & RAZOR WIRE (200%)",
            "Weathered PENITENCIARÍA FEDERAL DE SONA header + concrete jambs & barbed wire",
            (22, 392),
        ),
        (
            img_408,
            (1582, 955),
            "4 · 4.08 RUSTED IRON GATE & NO GUARDS INSIDE HUD (200%)",
            "Riveted rusted `kapi_sag` texture + complete ACT V CAD box (>=28px pad each side)",
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

    out_r13 = OUT_DIR / "b4_set_panama_sona_r13.png"
    r13.convert("RGB").save(out_r13, quality=95)
    print(f"Saved:\n  - {out_main}\n  - {out_r13}")
    return out_main, out_r13


if __name__ == "__main__":
    uret_kartlar("v1")
