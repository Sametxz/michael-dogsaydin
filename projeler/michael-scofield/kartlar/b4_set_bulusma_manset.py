"""V11 (Act IV — Motel Reunion, Father's Watch & Conspiracy Headlines Artist) — Style B + A Hybrid.

Isolated, side-effect-free module producing 3 richly detailed, R18-HAREKET animated-layer (960x540)
cinematic 2D sets:
  - set_404_motel_bulusma(katmanlar=None) -> (defs_svg, body_svg)
      [Motel Reunion & Bandage · STILL HERE | Layers: uzak, orta, sahne, bandaj_sar, plan, onplan]
  - set_405_baba_saati(katmanlar=None)    -> (defs_svg, body_svg)
      [The Father's Watch · FATHER (ZERO VIOLENCE) | Layers: uzak, orta, baba_golge, dusen_saat, sahne, plan, onplan]
  - set_406_manset_af(katmanlar=None)     -> (defs_svg, body_svg)
      [Conspiracy Headlines & Vanishing Pardon · REVOKED | Layers: uzak, orta, sahne, af_imza, gazete_1, damga_revoked, plan, onplan]

Rules enforced:
  - 100% ENGLISH on-screen diegetic text, HUD badges, neon signage, newspapers, pardon & presentation cards.
  - ZERO box overflow (every HUD badge & stamp has >= 16px horizontal padding on both sides).
  - ZERO violence / blood (4.04 uses clean white gauze bandage; 4.05 has only warm sunset shadow, empty chair & watch).
  - R4-ANATOMI & R4-PARALAKS: Collar-Over-Neck Z-order, locked F3 slender shoulders, BOTH ARMS complete from
    shoulder to hand, Michael v3 + Sara v2 + table strictly inside single `sahne` layer.
  - A2 Shape-Match Alignment: 4.05 brass pocket watch center = (480, 310), 4.06 circular newspaper seal = (480, 310).
  - Read-only import of karakter.py (`K.michael_kafa`, `K.sara_kafa`).
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

INK = "#161414"
INK_WARM = "#21150F"
PLAN = "#7FE6FF"
PLAN_CORE = "#E0FBFF"

_UID = 0


def _uid(prefix: str = "b4") -> str:
    global _UID
    _UID += 1
    return f"{prefix}_{_UID}"


def _katman_aktif(katmanlar: set[str] | list[str] | None, ad: str) -> bool:
    return katmanlar is None or ad in katmanlar


def _hud_badge(x: float, y: float, w: float, text: str, dot_color: str = PLAN_CORE) -> str:
    """Clean Style B+A cyan CAD HUD badge with generous >= 18px horizontal padding."""
    h = 36.0
    cx = x + w / 2.0
    return (
        f'<g id="hud-{_uid("b")}">'
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="3" '
        f'fill="#07121C" fill-opacity="0.92" stroke="{PLAN}" stroke-width="1.5"/>'
        f'<path d="M{x+6:.1f},{y+5:.1f} L{x+16:.1f},{y+5:.1f} '
        f'M{x+w-16:.1f},{y+h-5:.1f} L{x+w-6:.1f},{y+h-5:.1f}" '
        f'fill="none" stroke="{PLAN}" stroke-width="1.2" opacity="0.82"/>'
        f'<circle cx="{x+15:.1f}" cy="{y+h/2:.1f}" r="3.4" fill="{dot_color}"/>'
        f'<text x="{cx+7:.1f}" y="{y+23.0:.1f}" text-anchor="middle" '
        f'font-family="DejaVu Sans Mono, monospace" font-size="13.0" font-weight="bold" '
        f'fill="{PLAN_CORE}" letter-spacing="0.9">{text}</text>'
        f'</g>'
    )


# =============================================================================
# 4.04 · MOTEL REUNION & BANDAGE ("STILL HERE")
# =============================================================================
def set_404_motel_bulusma(katmanlar: set[str] | list[str] | None = None) -> tuple[str, str]:
    """Rainy night motel room lit by warm red-amber MOTEL neon outside the window
    and a warm table lamp. Locked Michael v3 (left, dark civilian jacket/shirt)
    and locked Sara v2 (right, olive-khaki jacket) sit across the wooden table in
    the single `sahne` layer (R4-PARALAKS) with Collar-Over-Neck and BOTH ARMS
    complete; Sara wraps a clean white gauze bandage (ZERO BLOOD) around Michael's
    wrist. Separate `bandaj_sar` layer enables live wrapping in the animatic."""
    rng = random.Random(404)
    p = _uid("s404")

    defs = f"""
    <linearGradient id="{p}_night_sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#090D16"/>
      <stop offset="55%" stop-color="#141926"/>
      <stop offset="100%" stop-color="#22171A"/>
    </linearGradient>
    <radialGradient id="{p}_neon_glow" cx="0.5" cy="0.5" r="0.55">
      <stop offset="0%" stop-color="#FF5B42" stop-opacity="0.72"/>
      <stop offset="48%" stop-color="#E63C2E" stop-opacity="0.30"/>
      <stop offset="100%" stop-color="#8C1A18" stop-opacity="0.0"/>
    </radialGradient>
    <linearGradient id="{p}_wall_room" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#1C191F"/>
      <stop offset="48%" stop-color="#292226"/>
      <stop offset="100%" stop-color="#1B1516"/>
    </linearGradient>
    <radialGradient id="{p}_lamp_pool" cx="0.5" cy="0.45" r="0.58">
      <stop offset="0%" stop-color="#FFE09C" stop-opacity="0.56"/>
      <stop offset="45%" stop-color="#E59846" stop-opacity="0.22"/>
      <stop offset="100%" stop-color="#8C481A" stop-opacity="0.0"/>
    </radialGradient>
    <linearGradient id="{p}_table_wood" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#6B4830"/>
      <stop offset="38%" stop-color="#4F3321"/>
      <stop offset="100%" stop-color="#2C1B12"/>
    </linearGradient>
    <linearGradient id="{p}_m_jacket" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#36414D"/>
      <stop offset="55%" stop-color="#252E38"/>
      <stop offset="100%" stop-color="#181E25"/>
    </linearGradient>
    <linearGradient id="{p}_m_shirt" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#637E96"/>
      <stop offset="100%" stop-color="#41586E"/>
    </linearGradient>
    <linearGradient id="{p}_s_jacket" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#6A7454"/>
      <stop offset="55%" stop-color="#4F583E"/>
      <stop offset="100%" stop-color="#353C2A"/>
    </linearGradient>
    <radialGradient id="{p}_vignette" cx="0.50" cy="0.48" r="0.72">
      <stop offset="48%" stop-color="#000000" stop-opacity="0.0"/>
      <stop offset="100%" stop-color="#070508" stop-opacity="0.72"/>
    </radialGradient>
    <filter id="{p}_glow_neon" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="3.4" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="{p}_glow_cyan" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="2.4" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    """

    parts: list[str] = []

    # -------------------------------------------------------------------------
    # LAYER 1: UZAK (Rainy night outside + glowing red-amber MOTEL neon sign)
    # -------------------------------------------------------------------------
    if _katman_aktif(katmanlar, "uzak"):
        u: list[str] = ['<g id="s404-uzak">']
        # Window opening sits at x=306..654, y=38..264 (centered behind table)
        u.append(f'<rect x="0" y="0" width="960" height="540" fill="url(#{p}_night_sky)"/>')
        # Distant motel wing & wet asphalt lot
        u.append('<rect x="290" y="182" width="380" height="90" fill="#11131C"/>')
        u.append('<rect x="332" y="196" width="38" height="26" fill="#E89D4A" opacity="0.24"/>')
        u.append('<rect x="412" y="196" width="38" height="26" fill="#7089A4" opacity="0.16"/>')
        u.append('<rect x="572" y="196" width="42" height="26" fill="#E89D4A" opacity="0.20"/>')
        # Red-amber neon halo bleeding into rainy night air
        u.append(f'<ellipse cx="480" cy="112" rx="185" ry="96" fill="url(#{p}_neon_glow)"/>')

        # Exterior MOTEL neon sign mounted on steel pylon outside window
        u.append(f'<rect x="386" y="76" width="188" height="62" rx="6" fill="#170E11" stroke="#3D2629" stroke-width="2.2"/>')
        u.append(f'<rect x="392" y="82" width="176" height="50" rx="4" fill="none" stroke="#FF6B4A" stroke-width="2.2" filter="url(#{p}_glow_neon)"/>')
        u.append(
            f'<text x="480" y="118" text-anchor="middle" font-family="DejaVu Sans, sans-serif" '
            f'font-size="31" font-weight="bold" fill="#FFB07C" stroke="#FF4B36" stroke-width="1.0" '
            f'letter-spacing="4.2" filter="url(#{p}_glow_neon)">MOTEL</text>'
        )
        # Small amber VACANCY sub-bar
        u.append(f'<rect x="424" y="140" width="112" height="20" rx="3" fill="#180F11" stroke="#442A24" stroke-width="1.4"/>')
        u.append(
            f'<text x="480" y="154" text-anchor="middle" font-family="DejaVu Sans Mono, monospace" '
            f'font-size="10.2" font-weight="bold" fill="#FFD384" letter-spacing="2.2">VACANCY</text>'
        )

        # Diagonal rain streaks & water droplets on the motel windowpane
        for _ in range(44):
            rx = rng.uniform(312, 648)
            ry = rng.uniform(44, 254)
            rlen = rng.uniform(12, 30)
            u.append(
                f'<path d="M{rx:.1f},{ry:.1f} L{rx-rlen*0.24:.1f},{ry+rlen:.1f}" '
                f'fill="none" stroke="#FFC4A6" stroke-width="1.1" opacity="{rng.uniform(0.16, 0.42):.2f}" stroke-linecap="round"/>'
            )
        for _ in range(28):
            dx = rng.uniform(314, 646)
            dy = rng.uniform(48, 256)
            u.append(f'<circle cx="{dx:.1f}" cy="{dy:.1f}" r="{rng.uniform(1.1, 2.3):.1f}" fill="#FFCFB0" opacity="{rng.uniform(0.18, 0.44):.2f}"/>')

        u.append('</g>')
        parts.append("".join(u))

    # -------------------------------------------------------------------------
    # LAYER 2: ORTA (Motel room walls, window frame/blinds, warm table lamp)
    # -------------------------------------------------------------------------
    if _katman_aktif(katmanlar, "orta"):
        m: list[str] = ['<g id="s404-orta">']
        # Wall surrounding the window cutout (window is x=306..654, y=38..264)
        m.append(f'<path d="M0,0 H960 V540 H0 Z M306,38 V264 H654 V38 Z" fill="url(#{p}_wall_room)" fill-rule="evenodd"/>')
        # Subtle vintage motel wallpaper vertical stripes
        for wx in range(18, 960, 34):
            if 302 <= wx <= 658:
                m.append(f'<path d="M{wx},0 L{wx},38 M{wx},264 L{wx},370" fill="none" stroke="#362C30" stroke-width="1.0" opacity="0.45"/>')
            else:
                m.append(f'<path d="M{wx},0 L{wx},370" fill="none" stroke="#362C30" stroke-width="1.0" opacity="0.45"/>')
        # Lower wood wainscot paneling
        m.append(f'<rect x="0" y="330" width="960" height="210" fill="#2A1D19" stroke="{INK_WARM}" stroke-width="1.5"/>')
        m.append(f'<rect x="0" y="324" width="960" height="8" fill="#463026" stroke="{INK_WARM}" stroke-width="1.3"/>')

        # Window wooden frame, partially pulled Venetian blinds & sill
        m.append(f'<rect x="300" y="32" width="360" height="238" fill="none" stroke="#3F2B23" stroke-width="12"/>')
        m.append(f'<rect x="306" y="38" width="348" height="226" fill="none" stroke="{INK_WARM}" stroke-width="2.0"/>')
        # Partially lowered top blinds slats (only top 26px so MOTEL neon stays unobstructed!)
        for by in (42, 50, 58):
            m.append(f'<rect x="308" y="{by}" width="344" height="4.5" fill="#4B3B34" stroke="{INK_WARM}" stroke-width="0.9"/>')
        # Window sill with red-amber neon reflection
        m.append(f'<rect x="292" y="264" width="376" height="12" rx="2" fill="#4E352A" stroke="{INK_WARM}" stroke-width="1.6"/>')
        m.append('<path d="M308,266 L652,266" fill="none" stroke="#FF8D68" stroke-width="1.8" opacity="0.58"/>')

        # Left motel room vintage framed landscape print
        m.append(f'<rect x="52" y="76" width="136" height="98" rx="2" fill="#3B2920" stroke="{INK_WARM}" stroke-width="1.8"/>')
        m.append('<rect x="62" y="86" width="116" height="78" fill="#252B33"/>')
        m.append('<path d="M62,140 L98,114 L132,134 L162,118 L178,136 L178,164 L62,164 Z" fill="#1A1E24"/>')

        # Right-side warm vintage motel table lamp on nightstand (x=832, y=156..324)
        m.append(f'<ellipse cx="834" cy="212" rx="185" ry="155" fill="url(#{p}_lamp_pool)"/>')
        m.append(f'<path d="M800,156 L868,156 L882,226 L786,226 Z" fill="#F2C87B" stroke="{INK_WARM}" stroke-width="1.8" stroke-linejoin="round"/>')
        m.append('<path d="M804,160 L864,160 L875,222 L793,222 Z" fill="#FFE6A8" opacity="0.52"/>')
        m.append(f'<rect x="828" y="226" width="12" height="58" fill="#6E4E34" stroke="{INK_WARM}" stroke-width="1.5"/>')
        m.append(f'<ellipse cx="834" cy="288" rx="30" ry="9" fill="#523724" stroke="{INK_WARM}" stroke-width="1.6"/>')
        # Warm light spill from window neon across upper walls
        m.append(f'<ellipse cx="480" cy="200" rx="280" ry="165" fill="url(#{p}_neon_glow)" opacity="0.32"/>')

        m.append('</g>')
        parts.append("".join(m))

    # -------------------------------------------------------------------------
    # LAYER 3: SAHNE (R4-PARALAKS LOCKED: Michael v3 + Sara v2 + motel table
    # ALL strictly inside this single `sahne` layer! Collar-Over-Neck & 2 ARMS EACH)
    # -------------------------------------------------------------------------
    if _katman_aktif(katmanlar, "sahne"):
        s: list[str] = ['<g id="s404-sahne">']

        # === 1. WOODEN MOTEL TABLE (back edge behind hands, front fills bottom) ===
        s.append(f'<polygon points="88,374 872,374 960,540 0,540" fill="url(#{p}_table_wood)" stroke="{INK_WARM}" stroke-width="2.2"/>')
        s.append('<path d="M96,378 L864,378" fill="none" stroke="#C88B58" stroke-width="1.8" opacity="0.56"/>')
        # Subtle warm wood grain lines
        for ty in (406, 444, 486, 520):
            s.append(f'<path d="M{60-(ty-400)*0.2:.0f},{ty} Q480,{ty+5} {900+(ty-400)*0.2:.0f},{ty-2}" fill="none" stroke="#2A1910" stroke-width="1.1" opacity="0.38"/>')
        # Warm table lamp & neon sheen on table surface
        s.append('<ellipse cx="505" cy="432" rx="195" ry="44" fill="#FFD794" opacity="0.14"/>')
        # Clean white medical gauze roll & small metal first-aid tin on right side of table (ZERO BLOOD)
        s.append(f'<g id="s404-firstaid-props">'
                 f'<ellipse cx="644" cy="456" rx="22" ry="11" fill="#F4F1E8" stroke="{INK}" stroke-width="1.5"/>'
                 f'<rect x="622" y="438" width="44" height="18" fill="#EAE6DC" stroke="{INK}" stroke-width="1.4"/>'
                 f'<ellipse cx="644" cy="438" rx="22" ry="10" fill="#FAF8F2" stroke="{INK}" stroke-width="1.4"/>'
                 f'<ellipse cx="644" cy="438" rx="9" ry="4" fill="#CFC9BC" stroke="{INK}" stroke-width="1.0"/>'
                 f'<rect x="688" y="446" width="66" height="30" rx="4" fill="#D9D5CC" stroke="{INK}" stroke-width="1.5"/>'
                 f'<rect x="716" y="453" width="10" height="16" fill="#3D6B7E"/>'
                 f'<rect x="713" y="456" width="16" height="10" fill="#3D6B7E"/>'
                 f'</g>')

        # =====================================================================
        # 2. LOCKED MICHAEL V3 (Left side, facing RIGHT toward Sara)
        #    F3 slender shoulders (~2.1x head_w), Collar-Over-Neck, BOTH ARMS!
        # =====================================================================
        s.append('<g id="s404-michael">')
        # Michael's FAR (RIGHT) ARM extending from right shoulder (340,294) to wrist resting on table (455..512, 396..414)
        # Sleeve rolled slightly above wrist, showing forearm & clean hand palm-up for bandaging
        s.append(
            f'<g id="s404-m-arm-right">'
            # Upper arm & elbow in dark jacket sleeve
            f'<path d="M326,288 L352,298 Q384,334 406,368 L382,386 Q356,356 322,326 Z" '
            f'fill="#222A33" stroke="{INK}" stroke-width="2.1" stroke-linejoin="round"/>'
            # Rolled cuff at elbow/mid-forearm
            f'<path d="M380,384 L406,366 L414,376 L388,394 Z" fill="#3A4754" stroke="{INK}" stroke-width="1.6" stroke-linejoin="round"/>'
            # Forearm extending cleanly onto table toward Sara
            f'<path d="M392,390 L412,374 L498,396 L494,418 L404,404 Z" '
            f'fill="#D9A988" stroke="{INK}" stroke-width="2.0" stroke-linejoin="round"/>'
            # Subtle original architectural forearm tattoo lines peeking out above wrist
            f'<path d="M416,384 L448,392 M422,392 L452,399 M430,386 L426,401 M442,389 L439,404" '
            f'fill="none" stroke="#2D3E4C" stroke-width="1.05" opacity="0.58"/>'
            # Relaxed right hand resting palm-up on table (x=496..534, y=394..420)
            f'<path d="M494,396 Q516,392 532,399 Q538,404 530,411 Q524,418 506,418 L492,416 Z" '
            f'fill="#D9A988" stroke="{INK}" stroke-width="1.8" stroke-linejoin="round"/>'
            f'<path d="M510,404 L528,404 M510,410 L525,410" fill="none" stroke="#A67658" stroke-width="1.1"/>'
            f'</g>'
        )

        # Michael's slender civilian torso (dark jacket over slate-blue shirt & cream undershirt)
        s.append(
            f'<path d="M222,296 L264,276 L326,278 L348,298 L354,432 L212,432 Z" '
            f'fill="url(#{p}_m_jacket)" stroke="{INK}" stroke-width="2.2" stroke-linejoin="round"/>'
        )
        # Inner slate-blue civilian shirt & cream crewneck undershirt
        s.append(f'<path d="M270,276 L316,278 L322,424 L274,424 Z" fill="url(#{p}_m_shirt)" stroke="{INK}" stroke-width="1.7"/>')
        s.append(f'<path d="M276,276 Q294,306 310,278 Z" fill="#E6E1D6" stroke="{INK}" stroke-width="1.4"/>')
        # Shirt placket & buttons
        s.append(f'<path d="M298,294 L302,422" fill="none" stroke="{INK}" stroke-width="1.3"/>')
        for by_m in (316, 344, 372, 400):
            s.append(f'<circle cx="299" cy="{by_m}" r="2.2" fill="#DCE2E8" stroke="{INK}" stroke-width="0.9"/>')

        # Michael's NEAR (LEFT) ARM — complete & continuous from left shoulder (222,296) -> elbow (188,386) -> hand on table (318,432)
        s.append(
            f'<g id="s404-m-arm-left">'
            f'<path d="M222,296 L194,314 Q174,364 186,406 Q194,426 220,432 L308,438 L312,414 L228,404 Q212,384 224,336 L236,306 Z" '
            f'fill="#2A333E" stroke="{INK}" stroke-width="2.2" stroke-linejoin="round"/>'
            # Jacket cuff
            f'<path d="M298,412 L314,414 L310,438 L294,436 Z" fill="#3B4755" stroke="{INK}" stroke-width="1.5"/>'
            # Left hand resting calmly on the wooden table
            f'<path d="M312,414 Q336,412 350,420 Q356,428 346,436 Q332,442 308,438 Z" '
            f'fill="#D9A988" stroke="{INK}" stroke-width="1.8" stroke-linejoin="round"/>'
            f'<path d="M326,423 L346,424 M324,430 L343,431" fill="none" stroke="#A67658" stroke-width="1.1"/>'
            f'</g>'
        )

        # Warm neon-amber rim highlight along Michael's shoulder & sleeve
        s.append('<path d="M200,312 L224,296 L262,278" fill="none" stroke="#FF9C72" stroke-width="2.0" opacity="0.58" stroke-linecap="round"/>')

        # Locked K.michael_kafa (view="3q", ifade="sefkat", boyun=True)
        # Neck base sits at y = 186 + 134*0.76 = 288
        s.append(
            f'<g transform="translate(294,186) scale(0.76)">'
            f'{K.michael_kafa(view="3q", ifade="sefkat", look=0.35, boyun=True)}'
            f'</g>'
        )

        # COLLAR-OVER-NECK Z-ORDER: Structured jacket collar & shirt collar lapels cleanly OVER neck base!
        s.append(
            f'<path d="M254,274 L240,304 L274,332 L278,286 L264,274 Z" '
            f'fill="#343F4C" stroke="{INK}" stroke-width="1.9" stroke-linejoin="round"/>'
        )
        s.append(
            f'<path d="M318,274 L334,296 L316,328 L310,286 Z" '
            f'fill="#26303B" stroke="{INK}" stroke-width="1.9" stroke-linejoin="round"/>'
        )
        s.append(
            f'<path d="M266,274 L286,306 L296,294 L274,274 Z" '
            f'fill="#637E96" stroke="{INK}" stroke-width="1.6" stroke-linejoin="round"/>'
        )
        s.append(
            f'<path d="M314,274 L300,304 L296,294 L308,274 Z" '
            f'fill="#4C667E" stroke="{INK}" stroke-width="1.6" stroke-linejoin="round"/>'
        )
        s.append('</g>')

        # =====================================================================
        # 3. LOCKED SARA V2 (Right side, mirrored to face LEFT toward Michael)
        #    F3 slender shoulders (~1.95x head_w), Collar-Over-Neck, BOTH ARMS!
        # =====================================================================
        s.append('<g id="s404-sara">')
        # Sara's FAR (LEFT) ARM extending continuously from left shoulder (614,298) down to gently cradle Michael's wrist (500,414)
        s.append(
            f'<g id="s404-s-arm-left">'
            f'<path d="M626,298 L602,308 Q574,348 548,390 L566,408 Q594,376 626,336 Z" '
            f'fill="#3E4631" stroke="{INK}" stroke-width="2.1" stroke-linejoin="round"/>'
            # Forearm & slender left hand cradling Michael's wrist from below
            f'<path d="M554,390 L520,404 L512,422 L564,410 Z" '
            f'fill="#D9AF92" stroke="{INK}" stroke-width="1.8" stroke-linejoin="round"/>'
            f'<path d="M522,406 Q502,408 496,418 Q498,427 516,426 L530,420 Z" '
            f'fill="#E8C1A6" stroke="{INK}" stroke-width="1.7" stroke-linejoin="round"/>'
            f'</g>'
        )

        # Sara's slender civilian torso (olive-khaki jacket over soft cream knit top)
        s.append(
            f'<path d="M614,298 L644,282 L696,282 L734,302 L742,438 L612,438 Z" '
            f'fill="url(#{p}_s_jacket)" stroke="{INK}" stroke-width="2.2" stroke-linejoin="round"/>'
        )
        # Soft cream-ivory knit top V-opening (clean scoop neckline below neck base)
        s.append(f'<path d="M648,284 L668,364 L688,284 Z" fill="#EAE4D7" stroke="{INK}" stroke-width="1.5"/>')
        # Jacket center seam
        s.append(f'<path d="M668,364 L668,438" fill="none" stroke="{INK}" stroke-width="1.5"/>')

        # Sara's NEAR (RIGHT) ARM — complete & continuous from right shoulder (734,302) -> elbow (754,386) -> hand wrapping bandage (532,390)
        s.append(
            f'<g id="s404-s-arm-right">'
            f'<path d="M734,302 L756,320 Q768,368 754,404 Q744,424 716,422 L578,408 L582,384 L710,394 Q728,376 722,334 L714,310 Z" '
            f'fill="#5D6749" stroke="{INK}" stroke-width="2.2" stroke-linejoin="round"/>'
            # Rolled olive sleeve cuff
            f'<path d="M578,382 L594,384 L590,410 L574,408 Z" fill="#464E37" stroke="{INK}" stroke-width="1.5"/>'
            # Slender wrist & right hand delicately holding/wrapping the clean white bandage
            f'<path d="M580,386 L544,382 Q522,380 518,392 Q520,404 542,406 L576,406 Z" '
            f'fill="#E8C1A6" stroke="{INK}" stroke-width="1.8" stroke-linejoin="round"/>'
            f'<path d="M540,390 L524,391 M540,397 L526,398" fill="none" stroke="#B88B6E" stroke-width="1.1"/>'
            f'</g>'
        )

        # Warm lamp highlight along Sara's right shoulder
        s.append('<path d="M700,284 L734,302 L754,318" fill="none" stroke="#FFE1A2" stroke-width="2.1" opacity="0.65" stroke-linecap="round"/>')

        # Locked K.sara_kafa (view="3q", ifade="sefkat", boyun=True), mirrored to face LEFT toward Michael!
        # Neck base sits at y = 198 + 134*0.74 = 297
        s.append(
            f'<g transform="translate(668,198) scale(-0.74, 0.74)">'
            f'{K.sara_kafa(view="3q", ifade="sefkat", look=0.30, boyun=True)}'
            f'</g>'
        )

        # COLLAR-OVER-NECK Z-ORDER: Cream knit neckline rim & olive jacket collar lapels cleanly OVER neck base!
        s.append(f'<path d="M652,292 Q670,305 688,292 L685,302 Q670,313 655,302 Z" fill="#EAE4D7" stroke="{INK}" stroke-width="1.4" stroke-linejoin="round"/>')
        s.append(
            f'<path d="M642,282 L624,312 L658,342 L666,330 L648,284 Z" '
            f'fill="#555E43" stroke="{INK}" stroke-width="1.8" stroke-linejoin="round"/>'
        )
        s.append(
            f'<path d="M694,282 L714,312 L680,342 L672,330 L688,284 Z" '
            f'fill="#6A7454" stroke="{INK}" stroke-width="1.8" stroke-linejoin="round"/>'
        )
        s.append('</g>')

        s.append('</g>')
        parts.append("".join(s))

    # -------------------------------------------------------------------------
    # LAYER 4: BANDAJ_SAR (R18-HAREKET animated clean white bandage wrap — ZERO BLOOD!)
    # -------------------------------------------------------------------------
    if _katman_aktif(katmanlar, "bandaj_sar"):
        b: list[str] = ['<g id="s404-bandaj_sar">']
        # Clean white layered cotton gauze wrapping Michael's wrist (x=456..500, y=388..420)
        b.append(
            f'<path d="M456,386 L496,394 L492,420 L452,412 Z" '
            f'fill="#FAF8F3" stroke="{INK}" stroke-width="1.9" stroke-linejoin="round"/>'
        )
        # Overlapping crisp diagonal bandage folds (pure clean white & soft warm-grey shadow)
        b.append(f'<path d="M464,387 L458,413 M476,389 L470,416 M488,392 L482,418" fill="none" stroke="#C8C2B6" stroke-width="1.5"/>')
        b.append(f'<path d="M460,396 L494,403" fill="none" stroke="#DED9CE" stroke-width="2.2" opacity="0.72"/>')
        # Active unrolling white gauze ribbon leading cleanly into Sara's right fingers (x=488..532)
        b.append(
            f'<path d="M484,394 Q506,388 526,390 L524,401 Q504,400 482,406 Z" '
            f'fill="#FFFFFF" stroke="{INK}" stroke-width="1.5" stroke-linejoin="round"/>'
        )
        b.append('<path d="M490,398 Q508,394 522,395" fill="none" stroke="#D4CFC4" stroke-width="1.0"/>')
        b.append('</g>')
        parts.append("".join(b))

    # -------------------------------------------------------------------------
    # LAYER 5: PLAN (Cyan CAD overlay: RENDEZVOUS · STILL HERE)
    # -------------------------------------------------------------------------
    if _katman_aktif(katmanlar, "plan"):
        pl: list[str] = ['<g id="s404-plan" opacity="0.92">']
        # Subtle cyan CAD target reticle around the gentle bandage-wrapping gesture
        pl.append(
            f'<circle cx="486" cy="404" r="46" fill="none" stroke="{PLAN}" '
            f'stroke-width="1.3" stroke-dasharray="6 5" opacity="0.62" filter="url(#{p}_glow_cyan)"/>'
        )
        pl.append(
            f'<path d="M432,404 L444,404 M528,404 L540,404 M486,350 L486,362 M486,446 L486,458" '
            f'fill="none" stroke="{PLAN_CORE}" stroke-width="1.3" opacity="0.72"/>'
        )
        # Top-right HUD badge (244px wide for "RENDEZVOUS · STILL HERE" -> >22px padding each side!)
        pl.append(_hud_badge(694, 20, 246, "RENDEZVOUS · STILL HERE"))
        pl.append('</g>')
        parts.append("".join(pl))

    # -------------------------------------------------------------------------
    # LAYER 6: ONPLAN (Warm neon dust motes & cinematic night vignette)
    # -------------------------------------------------------------------------
    if _katman_aktif(katmanlar, "onplan"):
        op: list[str] = ['<g id="s404-onplan">']
        for _ in range(22):
            dx = rng.uniform(40, 920)
            dy = rng.uniform(50, 490)
            dr = rng.uniform(0.9, 2.0)
            col = "#FFB588" if dx < 540 else "#FFE4A6"
            op.append(f'<circle cx="{dx:.1f}" cy="{dy:.1f}" r="{dr:.1f}" fill="{col}" opacity="{rng.uniform(0.18, 0.44):.2f}"/>')
        op.append(f'<rect x="0" y="0" width="960" height="540" fill="url(#{p}_vignette)"/>')
        op.append('</g>')
        parts.append("".join(op))

    return defs, "".join(parts)


# =============================================================================
# 4.05 · THE FATHER'S WATCH ("06:14 · ONLY HIS WATCH" · ZERO VIOLENCE)
# =============================================================================
def set_405_baba_saati(katmanlar: set[str] | list[str] | None = None) -> tuple[str, str]:
    """Golden-dusty New Mexico desert sunset veranda with a wooden table and two
    wooden chairs. ZERO VIOLENCE / ZERO BLOOD / ZERO WEAPONS.
    R18-HAREKET layers:
      - `baba_golge`: Warm sunset shadow silhouette of Father & Michael side by side
        (fades in animatic to leave the empty wooden chair).
      - `dusen_saat`: Falling brass pocket watch with thin chain & cracked glass
        stopped at 06:14, centered at EXACTLY (480, 310) for A2 Shape-Match with 4.06!"""
    rng = random.Random(405)
    p = _uid("s405")

    defs = f"""
    <linearGradient id="{p}_sky_nm" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#2A1A22"/>
      <stop offset="30%" stop-color="#763A2B"/>
      <stop offset="62%" stop-color="#D47B3E"/>
      <stop offset="88%" stop-color="#F5BD6B"/>
      <stop offset="100%" stop-color="#FCE09A"/>
    </linearGradient>
    <radialGradient id="{p}_sun_glow" cx="0.50" cy="0.50" r="0.52">
      <stop offset="0%" stop-color="#FFF5C8" stop-opacity="0.95"/>
      <stop offset="32%" stop-color="#FFCA70" stop-opacity="0.58"/>
      <stop offset="72%" stop-color="#E58038" stop-opacity="0.18"/>
      <stop offset="100%" stop-color="#B04B24" stop-opacity="0.0"/>
    </radialGradient>
    <linearGradient id="{p}_porch_floor" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#734A2D"/>
      <stop offset="45%" stop-color="#56351F"/>
      <stop offset="100%" stop-color="#2F1C10"/>
    </linearGradient>
    <linearGradient id="{p}_wood_beam" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#2D1A10"/>
      <stop offset="50%" stop-color="#4A2D1C"/>
      <stop offset="100%" stop-color="#23140C"/>
    </linearGradient>
    <linearGradient id="{p}_brass" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FCE29C"/>
      <stop offset="32%" stop-color="#D8A448"/>
      <stop offset="70%" stop-color="#9A6B22"/>
      <stop offset="100%" stop-color="#5C3C12"/>
    </linearGradient>
    <radialGradient id="{p}_watch_dial" cx="0.44" cy="0.40" r="0.60">
      <stop offset="0%" stop-color="#FFFBF0"/>
      <stop offset="72%" stop-color="#EFE4C8"/>
      <stop offset="100%" stop-color="#D2C099"/>
    </radialGradient>
    <linearGradient id="{p}_sun_beam" x1="0.2" y1="0" x2="0.8" y2="1">
      <stop offset="0%" stop-color="#FFE8A6" stop-opacity="0.24"/>
      <stop offset="65%" stop-color="#F2A950" stop-opacity="0.06"/>
      <stop offset="100%" stop-color="#D4742E" stop-opacity="0.0"/>
    </linearGradient>
    <radialGradient id="{p}_vignette" cx="0.50" cy="0.50" r="0.72">
      <stop offset="48%" stop-color="#000000" stop-opacity="0.0"/>
      <stop offset="100%" stop-color="#140A06" stop-opacity="0.68"/>
    </radialGradient>
    <filter id="{p}_glow_cyan" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="2.4" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="{p}_shadow_soft" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="2.2" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    """

    parts: list[str] = []

    # -------------------------------------------------------------------------
    # LAYER 1: UZAK (Golden-dusty New Mexico desert sunset horizon & mesas)
    # -------------------------------------------------------------------------
    if _katman_aktif(katmanlar, "uzak"):
        u: list[str] = ['<g id="s405-uzak">']
        u.append(f'<rect x="0" y="0" width="960" height="318" fill="url(#{p}_sky_nm)"/>')
        # Low New Mexico sun & golden atmospheric bloom
        u.append(f'<ellipse cx="480" cy="212" rx="280" ry="145" fill="url(#{p}_sun_glow)"/>')
        u.append('<circle cx="480" cy="216" r="34" fill="#FFF4C6" opacity="0.90"/>')

        # Distant hazy desert mesas (layered silhouettes)
        u.append(
            '<path d="M0,254 L78,244 L108,214 L214,214 L244,242 L348,246 L382,226 L444,226 L468,248 '
            'L580,248 L612,218 L734,218 L764,244 L858,236 L902,216 L960,216 L960,318 L0,318 Z" '
            'fill="#7A3E2B" opacity="0.72"/>'
        )
        u.append(
            '<path d="M0,278 L142,268 L178,254 L276,256 L328,274 L628,274 L694,254 L810,256 L866,272 L960,268 L960,318 L0,318 Z" '
            'fill="#54291E" opacity="0.88"/>'
        )
        # Golden horizon rim
        u.append('<path d="M0,278 L960,276" fill="none" stroke="#F8C676" stroke-width="1.4" opacity="0.42"/>')
        u.append('</g>')
        parts.append("".join(u))

    # -------------------------------------------------------------------------
    # LAYER 2: ORTA (Wooden veranda, porch railing, wooden table & EMPTY CHAIR)
    # -------------------------------------------------------------------------
    if _katman_aktif(katmanlar, "orta"):
        m: list[str] = ['<g id="s405-orta">']
        # Porch roof eaves at top & rustic wooden veranda posts
        m.append(f'<rect x="0" y="0" width="960" height="36" fill="#23140D" stroke="{INK_WARM}" stroke-width="1.8"/>')
        m.append(f'<rect x="0" y="34" width="960" height="8" fill="#462B1A" stroke="{INK_WARM}" stroke-width="1.2"/>')
        # Left & right veranda support posts
        m.append(f'<rect x="52" y="36" width="32" height="304" fill="url(#{p}_wood_beam)" stroke="{INK_WARM}" stroke-width="2.0"/>')
        m.append(f'<rect x="876" y="36" width="32" height="304" fill="url(#{p}_wood_beam)" stroke="{INK_WARM}" stroke-width="2.0"/>')
        # Horizontal porch rail & balusters
        m.append(f'<rect x="84" y="236" width="792" height="10" fill="#4A2D1C" stroke="{INK_WARM}" stroke-width="1.6"/>')
        m.append(f'<rect x="84" y="294" width="792" height="8" fill="#3B2315" stroke="{INK_WARM}" stroke-width="1.4"/>')
        for bx in range(118, 868, 42):
            m.append(f'<rect x="{bx}" y="246" width="8" height="48" fill="#3A2215" stroke="{INK_WARM}" stroke-width="1.1"/>')

        # Sunlit wooden veranda floor planks
        m.append(f'<rect x="0" y="302" width="960" height="238" fill="url(#{p}_porch_floor)"/>')
        for fy in (326, 356, 392, 434, 482):
            m.append(f'<path d="M0,{fy} L960,{fy}" fill="none" stroke="#26150C" stroke-width="1.5" opacity="0.65"/>')
        # Warm sunset light strip across floor
        m.append('<polygon points="180,302 780,302 890,540 70,540" fill="#F5B460" opacity="0.16"/>')

        # === LEFT WOODEN CHAIR (Michael's chair, slightly angled) ===
        m.append(
            f'<g id="s405-chair-left">'
            # Backrest posts & slats
            f'<rect x="176" y="198" width="12" height="186" rx="2" fill="#4D2F1C" stroke="{INK_WARM}" stroke-width="1.8"/>'
            f'<rect x="268" y="206" width="12" height="174" rx="2" fill="#3F2616" stroke="{INK_WARM}" stroke-width="1.8"/>'
            f'<rect x="186" y="208" width="84" height="18" fill="#5D3A24" stroke="{INK_WARM}" stroke-width="1.5"/>'
            f'<rect x="186" y="236" width="84" height="14" fill="#53331F" stroke="{INK_WARM}" stroke-width="1.4"/>'
            # Seat & front legs
            f'<polygon points="172,306 286,306 298,324 184,324" fill="#6E462B" stroke="{INK_WARM}" stroke-width="1.8"/>'
            f'<rect x="184" y="324" width="12" height="82" fill="#4A2D1B" stroke="{INK_WARM}" stroke-width="1.6"/>'
            f'<rect x="282" y="324" width="12" height="82" fill="#3C2314" stroke="{INK_WARM}" stroke-width="1.6"/>'
            f'</g>'
        )

        # === RIGHT EMPTY WOODEN CHAIR (Father's chair — poignant centerpiece!) ===
        m.append(
            f'<g id="s405-chair-empty">'
            f'<rect x="680" y="204" width="12" height="178" rx="2" fill="#3F2616" stroke="{INK_WARM}" stroke-width="1.8"/>'
            f'<rect x="772" y="196" width="12" height="188" rx="2" fill="#553420" stroke="{INK_WARM}" stroke-width="1.8"/>'
            f'<rect x="690" y="206" width="84" height="18" fill="#684128" stroke="{INK_WARM}" stroke-width="1.5"/>'
            f'<rect x="690" y="234" width="84" height="14" fill="#5B3822" stroke="{INK_WARM}" stroke-width="1.4"/>'
            # Empty sunlit seat
            f'<polygon points="674,306 788,306 776,324 662,324" fill="#7C5032" stroke="{INK_WARM}" stroke-width="1.8"/>'
            f'<path d="M676,308 L784,308" fill="none" stroke="#F8C87A" stroke-width="1.6" opacity="0.62"/>'
            f'<rect x="664" y="324" width="12" height="82" fill="#3E2515" stroke="{INK_WARM}" stroke-width="1.6"/>'
            f'<rect x="762" y="324" width="12" height="82" fill="#4D2F1C" stroke="{INK_WARM}" stroke-width="1.6"/>'
            f'</g>'
        )

        # === CENTER WOODEN VERANDA TABLE ===
        m.append(
            f'<g id="s405-table">'
            f'<polygon points="334,296 626,296 654,322 306,322" fill="#7A4E30" stroke="{INK_WARM}" stroke-width="2.0"/>'
            f'<rect x="306" y="322" width="348" height="14" fill="#4E301D" stroke="{INK_WARM}" stroke-width="1.8"/>'
            f'<rect x="328" y="336" width="16" height="94" fill="#3D2415" stroke="{INK_WARM}" stroke-width="1.7"/>'
            f'<rect x="616" y="336" width="16" height="94" fill="#3D2415" stroke="{INK_WARM}" stroke-width="1.7"/>'
            f'<path d="M338,298 L622,298" fill="none" stroke="#FAD082" stroke-width="1.8" opacity="0.64"/>'
            f'</g>'
        )

        m.append('</g>')
        parts.append("".join(m))

    # -------------------------------------------------------------------------
    # LAYER 3: BABA_GOLGE (R18-HAREKET animated warm sunset shadow silhouettes
    # of Father & Michael side by side — fades in animatic leaving empty chair!)
    # -------------------------------------------------------------------------
    if _katman_aktif(katmanlar, "baba_golge"):
        bg: list[str] = ['<g id="s405-baba_golge" opacity="0.62">']
        # Long warm sunset shadow cast across the wooden veranda floor by the two figures
        bg.append(
            '<path d="M210,418 Q242,390 296,406 L342,468 L170,486 Z" fill="#2A140A" opacity="0.46"/>'
            '<path d="M686,416 Q724,386 774,404 L824,474 L636,488 Z" fill="#2A140A" opacity="0.46"/>'
        )
        # Soft backlit warm-sepia silhouette of Michael (left chair) & Father (right chair)
        # Strictly peaceful, warm memory silhouettes (ZERO weapons, ZERO violence)
        bg.append(
            f'<g filter="url(#{p}_shadow_soft)">'
            # Michael's warm backlit silhouette on left chair
            f'<path d="M222,194 Q224,166 244,164 Q264,166 264,194 Q264,214 252,222 L252,232 '
            f'L286,244 Q298,266 296,306 L196,306 Q192,262 206,242 L232,232 L232,220 Q222,212 222,194 Z" '
            f'fill="#3D1F12" opacity="0.54"/>'
            # Father's warm backlit silhouette on right chair (slightly broader, older posture)
            f'<path d="M694,186 Q696,156 718,154 Q740,156 740,186 Q740,208 728,218 L728,228 '
            f'L766,242 Q780,266 776,306 L666,306 Q664,264 678,242 L706,228 L706,216 Q694,206 694,186 Z" '
            f'fill="#3D1F12" opacity="0.58"/>'
            # Warm golden rim outline tracing the Father's memory silhouette
            f'<path d="M694,186 Q696,156 718,154 Q740,156 740,186" fill="none" stroke="#FFD68A" stroke-width="2.0" opacity="0.65"/>'
            f'</g>'
        )
        bg.append('</g>')
        parts.append("".join(bg))

    # -------------------------------------------------------------------------
    # LAYER 4: SAHNE (Foreground porch frame subtle shadow anchoring depth)
    # -------------------------------------------------------------------------
    if _katman_aktif(katmanlar, "sahne"):
        s: list[str] = ['<g id="s405-sahne">']
        # Subtle warm drop-shadow cast beneath the falling pocket watch on the table/floor below
        s.append('<ellipse cx="480" cy="404" rx="46" ry="10" fill="#1A0E07" opacity="0.34"/>')
        s.append('</g>')
        parts.append("".join(s))

    # -------------------------------------------------------------------------
    # LAYER 5: DUSEN_SAAT (R18-HAREKET animated falling brass pocket watch!
    # CENTERED EXACTLY AT (480, 310) for A2 Shape-Match with 4.06 newspaper seal!)
    # -------------------------------------------------------------------------
    if _katman_aktif(katmanlar, "dusen_saat"):
        w: list[str] = ['<g id="s405-dusen_saat">']
        cx, cy = 480.0, 310.0

        # Delicate brass watch chain trailing upward & swaying gently as it falls
        chain_pts = [
            (480, 240), (476, 224), (482, 206), (492, 188),
            (496, 168), (488, 148), (476, 128), (472, 106),
            (478, 84), (490, 62), (496, 38), (492, 14),
        ]
        for i in range(len(chain_pts) - 1):
            x1, y1 = chain_pts[i]
            x2, y2 = chain_pts[i + 1]
            mx, my = (x1 + x2) / 2.0, (y1 + y2) / 2.0
            ang = math.degrees(math.atan2(y2 - y1, x2 - x1))
            w.append(
                f'<ellipse cx="{mx:.1f}" cy="{my:.1f}" rx="7.5" ry="3.4" '
                f'transform="rotate({ang:.1f} {mx:.1f} {my:.1f})" '
                f'fill="none" stroke="#E8BE68" stroke-width="2.4"/>'
            )
            w.append(
                f'<ellipse cx="{mx:.1f}" cy="{my:.1f}" rx="7.5" ry="3.4" '
                f'transform="rotate({ang:.1f} {mx:.1f} {my:.1f})" '
                f'fill="none" stroke="{INK_WARM}" stroke-width="0.9" opacity="0.72"/>'
            )

        # Pocket watch bow (top ring) & fluted winding crown
        w.append(f'<circle cx="{cx:.1f}" cy="{cy-66:.1f}" r="11" fill="none" stroke="#D8A64C" stroke-width="3.4"/>')
        w.append(f'<circle cx="{cx:.1f}" cy="{cy-66:.1f}" r="11" fill="none" stroke="{INK_WARM}" stroke-width="1.2"/>')
        w.append(f'<rect x="{cx-9:.1f}" y="{cy-62:.1f}" width="18" height="12" rx="3" fill="url(#{p}_brass)" stroke="{INK_WARM}" stroke-width="1.6"/>')
        w.append(f'<rect x="{cx-6:.1f}" y="{cy-52:.1f}" width="12" height="7" fill="#B58330" stroke="{INK_WARM}" stroke-width="1.3"/>')

        # Outer brass case (r=56) & inner stepped bezel (r=48)
        w.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="56" fill="url(#{p}_brass)" stroke="{INK_WARM}" stroke-width="2.4"/>')
        w.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="51" fill="none" stroke="#FCE3A2" stroke-width="1.4" opacity="0.72"/>')
        w.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="47" fill="url(#{p}_watch_dial)" stroke="{INK_WARM}" stroke-width="1.8"/>')
        w.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="42" fill="none" stroke="#B69F78" stroke-width="0.9"/>')

        # 12 hour tick marks around dial
        for h_idx in range(12):
            ang_rad = math.radians(h_idx * 30 - 90)
            r_in = 37.5 if h_idx % 3 == 0 else 39.0
            r_out = 43.0
            tx1, ty1 = cx + r_in * math.cos(ang_rad), cy + r_in * math.sin(ang_rad)
            tx2, ty2 = cx + r_out * math.cos(ang_rad), cy + r_out * math.sin(ang_rad)
            sw_t = 2.0 if h_idx % 3 == 0 else 1.2
            w.append(f'<path d="M{tx1:.1f},{ty1:.1f} L{tx2:.1f},{ty2:.1f}" fill="none" stroke="#2C2117" stroke-width="{sw_t}"/>')

        # Crisp vintage dial numerals (12, 3, 6, 9 — cleanly inset from ticks!)
        w.append(f'<text x="{cx:.1f}" y="{cy-22.5:.1f}" text-anchor="middle" font-family="Georgia, serif" font-size="10.8" font-weight="bold" fill="#2A1E15">12</text>')
        w.append(f'<text x="{cx+27.5:.1f}" y="{cy+4:.1f}" text-anchor="middle" font-family="Georgia, serif" font-size="10.8" font-weight="bold" fill="#2A1E15">3</text>')
        w.append(f'<text x="{cx:.1f}" y="{cy+31.5:.1f}" text-anchor="middle" font-family="Georgia, serif" font-size="10.8" font-weight="bold" fill="#2A1E15">6</text>')
        w.append(f'<text x="{cx-27.5:.1f}" y="{cy+4:.1f}" text-anchor="middle" font-family="Georgia, serif" font-size="10.8" font-weight="bold" fill="#2A1E15">9</text>')

        # Hands STOPPED EXACTLY AT 06:14
        # Hour hand: 6 + 14/60 = 6.233 -> 187° from 12 o'clock (pointing down & slightly left)
        hr_ang = math.radians(187 - 90)
        hx, hy = cx + 21.0 * math.cos(hr_ang), cy + 21.0 * math.sin(hr_ang)
        w.append(f'<path d="M{cx:.1f},{cy:.1f} L{hx:.1f},{hy:.1f}" fill="none" stroke="#1D1612" stroke-width="3.2" stroke-linecap="round"/>')
        # Minute hand: 14 * 6 = 84° from 12 o'clock (pointing right & slightly above 3)
        mn_ang = math.radians(84 - 90)
        mx_h, my_h = cx + 30.5 * math.cos(mn_ang), cy + 30.5 * math.sin(mn_ang)
        w.append(f'<path d="M{cx:.1f},{cy:.1f} L{mx_h:.1f},{my_h:.1f}" fill="none" stroke="#1D1612" stroke-width="2.1" stroke-linecap="round"/>')
        # Fine stopped seconds hand & brass center pin
        w.append(f'<path d="M{cx:.1f},{cy:.1f} L{cx-18:.1f},{cy-14:.1f}" fill="none" stroke="#8C2E22" stroke-width="1.1" stroke-linecap="round"/>')
        w.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="4.0" fill="#D8A448" stroke="{INK_WARM}" stroke-width="1.3"/>')

        # Delicate CRACKED GLASS fracture lines radiating from impact point (494, 294) + specular glare
        w.append(
            f'<path d="M494,294 L466,274 M494,294 L522,298 M494,294 L478,324 L452,338 '
            f'M494,294 L512,330 M478,324 L496,352 M494,294 L488,266" '
            f'fill="none" stroke="#FFFFFF" stroke-width="1.3" opacity="0.82" stroke-linecap="round"/>'
        )
        w.append(
            f'<path d="M495,295 L467,275 M495,295 L479,325 L453,339 M495,295 L513,331" '
            f'fill="none" stroke="#4F4438" stroke-width="0.85" opacity="0.55"/>'
        )
        # Subtle curved crystal specular glint
        w.append('<path d="M446,292 Q458,270 482,268" fill="none" stroke="#FFFFFF" stroke-width="3.0" opacity="0.42" stroke-linecap="round"/>')

        w.append('</g>')
        parts.append("".join(w))

    # -------------------------------------------------------------------------
    # LAYER 6: PLAN (A2 Shape-Match cyan reticle at (480,310) + HUD badge)
    # -------------------------------------------------------------------------
    if _katman_aktif(katmanlar, "plan"):
        pl: list[str] = ['<g id="s405-plan" opacity="0.92">']
        # A2 Shape-Match concentric cyan CAD ring centered at EXACTLY (480, 310)
        pl.append(
            f'<circle cx="480" cy="310" r="66" fill="none" stroke="{PLAN}" '
            f'stroke-width="1.5" stroke-dasharray="8 6" opacity="0.74" filter="url(#{p}_glow_cyan)"/>'
        )
        pl.append(
            f'<path d="M406,310 L418,310 M542,310 L554,310 M480,236 L480,248 M480,372 L480,384" '
            f'fill="none" stroke="{PLAN_CORE}" stroke-width="1.4" opacity="0.82"/>'
        )
        # Top-right HUD badge (244px wide for "06:14 · ONLY HIS WATCH" -> >22px padding each side!)
        pl.append(_hud_badge(694, 20, 246, "06:14 · ONLY HIS WATCH", dot_color="#FFD278"))
        pl.append('</g>')
        parts.append("".join(pl))

    # -------------------------------------------------------------------------
    # LAYER 7: ONPLAN (Golden desert sunbeams, dust motes & warm sunset vignette)
    # -------------------------------------------------------------------------
    if _katman_aktif(katmanlar, "onplan"):
        op: list[str] = ['<g id="s405-onplan">']
        op.append(f'<polygon points="220,0 740,0 920,540 40,540" fill="url(#{p}_sun_beam)"/>')
        for _ in range(30):
            dx = rng.uniform(40, 920)
            dy = rng.uniform(50, 500)
            dr = rng.uniform(0.9, 2.2)
            op.append(f'<circle cx="{dx:.1f}" cy="{dy:.1f}" r="{dr:.1f}" fill="#FFE8A8" opacity="{rng.uniform(0.22, 0.56):.2f}"/>')
        op.append(f'<rect x="0" y="0" width="960" height="540" fill="url(#{p}_vignette)"/>')
        op.append('</g>')
        parts.append("".join(op))

    return defs, "".join(parts)


# =============================================================================
# 4.06 · CONSPIRACY HEADLINES & VANISHING PARDON ("REVOKED")
# =============================================================================
def set_406_manset_af(katmanlar: set[str] | list[str] | None = None) -> tuple[str, str]:
    """Dark mahogany desk with official US Presidential Pardon document for
    BURROWS, LINCOLN. R18-HAREKET animated layers:
      - `af_imza`: Golden fountain-pen signature (erases/vanishes in animatic).
      - `gazete_1`: THE CHICAGO CHRONICLE · STEADMAN ALIVE! with circular front-page
        seal centered at EXACTLY (480, 310) for A2 Shape-Match with 4.05 pocket watch!
      - `damga_revoked`: Heavy crimson-red PARDON REVOKED rubber stamp slammed onto pardon."""
    rng = random.Random(406)
    p = _uid("s406")

    defs = f"""
    <linearGradient id="{p}_mahogany" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#3E2017"/>
      <stop offset="48%" stop-color="#2B140E"/>
      <stop offset="100%" stop-color="#170A07"/>
    </linearGradient>
    <radialGradient id="{p}_desk_lamp" cx="0.28" cy="0.24" r="0.68">
      <stop offset="0%" stop-color="#FFE4A6" stop-opacity="0.34"/>
      <stop offset="48%" stop-color="#D99648" stop-opacity="0.12"/>
      <stop offset="100%" stop-color="#542810" stop-opacity="0.0"/>
    </radialGradient>
    <linearGradient id="{p}_parchment" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FCF7EA"/>
      <stop offset="55%" stop-color="#F1E5CB"/>
      <stop offset="100%" stop-color="#DECBA5"/>
    </linearGradient>
    <linearGradient id="{p}_newsprint" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ECE7DB"/>
      <stop offset="58%" stop-color="#DDD6C5"/>
      <stop offset="100%" stop-color="#C6BDA9"/>
    </linearGradient>
    <linearGradient id="{p}_gold_seal" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FCE49C"/>
      <stop offset="48%" stop-color="#D6A33E"/>
      <stop offset="100%" stop-color="#8C6018"/>
    </linearGradient>
    <radialGradient id="{p}_vignette" cx="0.50" cy="0.50" r="0.72">
      <stop offset="48%" stop-color="#000000" stop-opacity="0.0"/>
      <stop offset="100%" stop-color="#090404" stop-opacity="0.72"/>
    </radialGradient>
    <filter id="{p}_glow_cyan" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="2.4" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    """

    parts: list[str] = []

    # -------------------------------------------------------------------------
    # LAYER 1: UZAK (Deep dark executive office backdrop)
    # -------------------------------------------------------------------------
    if _katman_aktif(katmanlar, "uzak"):
        u: list[str] = ['<g id="s406-uzak">']
        u.append('<rect x="0" y="0" width="960" height="540" fill="#120908"/>')
        u.append('</g>')
        parts.append("".join(u))

    # -------------------------------------------------------------------------
    # LAYER 2: ORTA (Polished mahogany desk surface, warm lamp pool & fountain pen)
    # -------------------------------------------------------------------------
    if _katman_aktif(katmanlar, "orta"):
        m: list[str] = ['<g id="s406-orta">']
        m.append(f'<rect x="0" y="0" width="960" height="540" fill="url(#{p}_mahogany)"/>')
        # Subtle mahogany wood grain lines
        for gy in range(24, 540, 26):
            m.append(
                f'<path d="M0,{gy} Q320,{gy+rng.uniform(-5,5):.1f} 640,{gy+rng.uniform(-5,5):.1f} T960,{gy}" '
                f'fill="none" stroke="#4F2A1E" stroke-width="1.3" opacity="0.34"/>'
            )
        # Warm executive desk lamp pool from upper-left
        m.append(f'<rect x="0" y="0" width="960" height="540" fill="url(#{p}_desk_lamp)"/>')
        # Polished brass & black fountain pen resting at bottom-left of desk
        m.append(
            f'<g transform="translate(154,504) rotate(-8)">'
            f'<rect x="-92" y="-6" width="144" height="12" rx="5" fill="#1B1E24" stroke="{INK}" stroke-width="1.5"/>'
            f'<rect x="-20" y="-6.5" width="12" height="13" fill="url(#{p}_gold_seal)" stroke="{INK}" stroke-width="1.0"/>'
            f'<polygon points="52,-5 82,0 52,5" fill="url(#{p}_gold_seal)" stroke="{INK}" stroke-width="1.2"/>'
            f'<path d="M66,0 L82,0" fill="none" stroke="{INK}" stroke-width="1.0"/>'
            f'</g>'
        )
        m.append('</g>')
        parts.append("".join(m))

    # -------------------------------------------------------------------------
    # LAYER 3: SAHNE (Official US Presidential Pardon Parchment for Lincoln Burrows)
    # -------------------------------------------------------------------------
    if _katman_aktif(katmanlar, "sahne"):
        s: list[str] = ['<g id="s406-sahne">']
        s.append('<g id="s406-pardon" transform="translate(244,266) rotate(-2.4)">')
        # Soft drop shadow on mahogany desk
        s.append('<rect x="-180" y="-208" width="368" height="422" rx="3" fill="#0B0403" opacity="0.52"/>')
        # Cream-ivory parchment sheet
        s.append(f'<rect x="-186" y="-214" width="368" height="422" rx="2" fill="url(#{p}_parchment)" stroke="{INK_WARM}" stroke-width="2.0"/>')
        # Ornate double official border (navy & gold)
        s.append('<rect x="-172" y="-200" width="340" height="394" fill="none" stroke="#1E3048" stroke-width="2.0"/>')
        s.append('<rect x="-166" y="-194" width="328" height="382" fill="none" stroke="#B68B38" stroke-width="1.1"/>')

        # Top executive eagle/shield emblem (stylized geometric 2D heraldry)
        s.append('<circle cx="-2" cy="-164" r="18" fill="none" stroke="#1E3048" stroke-width="1.6"/>')
        s.append('<circle cx="-2" cy="-164" r="14" fill="#E8D7B2" stroke="#B68B38" stroke-width="1.1"/>')
        s.append('<path d="M-12,-165 L-2,-173 L8,-165 L4,-156 L-8,-156 Z" fill="#1E3048"/>')

        # 100% English official pardon typography (generous margins inside 328px inner border!)
        s.append(
            '<text x="-2" y="-130" text-anchor="middle" font-family="Georgia, serif" '
            'font-size="9.5" font-weight="bold" fill="#2A3A4E" letter-spacing="1.8">UNITED STATES OF AMERICA</text>'
        )
        s.append(
            '<text x="-2" y="-104" text-anchor="middle" font-family="Georgia, serif" '
            'font-size="20.5" font-weight="bold" fill="#182332" letter-spacing="1.4">PRESIDENTIAL PARDON</text>'
        )
        s.append('<path d="M-136,-92 L132,-92" fill="none" stroke="#B68B38" stroke-width="1.5"/>')

        # Subject & Case lines
        s.append(
            '<text x="-2" y="-68" text-anchor="middle" font-family="DejaVu Sans Mono, monospace" '
            'font-size="11.5" font-weight="bold" fill="#1B222C" letter-spacing="0.8">RECIPIENT: BURROWS, LINCOLN</text>'
        )
        s.append(
            '<text x="-2" y="-48" text-anchor="middle" font-family="DejaVu Sans Mono, monospace" '
            'font-size="9.0" fill="#463E34" letter-spacing="0.6">EXECUTIVE CLEMENCY · FULL &amp; UNCONDITIONAL</text>'
        )

        # Formal legal body lines (clean readable typographic bars)
        for ly_i, lw_i in enumerate([270, 286, 260, 282, 240, 274, 210]):
            yy = -24 + ly_i * 15
            s.append(f'<path d="M-144,{yy} L{-144+lw_i},{yy}" fill="none" stroke="#6E6254" stroke-width="1.7" opacity="0.68"/>')

        # Bottom-left embossed gold foil seal & crimson ribbon
        s.append('<polygon points="-122,144 -132,184 -116,174 -106,184 -110,144" fill="#8C1D22" stroke="#3D0C0F" stroke-width="1.1"/>')
        s.append(f'<circle cx="-116" cy="136" r="24" fill="url(#{p}_gold_seal)" stroke="#6B4712" stroke-width="1.6"/>')
        s.append('<circle cx="-116" cy="136" r="18" fill="none" stroke="#FFF2C2" stroke-width="1.0" stroke-dasharray="3 2"/>')
        s.append('<text x="-116" y="139" text-anchor="middle" font-family="Georgia, serif" font-size="7.5" font-weight="bold" fill="#4A300A">SEAL</text>')

        # Bottom-right signature baseline
        s.append('<path d="M-32,148 L142,148" fill="none" stroke="#2C241E" stroke-width="1.4"/>')
        s.append(
            '<text x="55" y="164" text-anchor="middle" font-family="DejaVu Sans Mono, monospace" '
            'font-size="8.2" fill="#4E453B" letter-spacing="0.9">PRESIDENT OF THE UNITED STATES</text>'
        )
        s.append('</g>')
        s.append('</g>')
        parts.append("".join(s))

    # -------------------------------------------------------------------------
    # LAYER 4: AF_IMZA (R18-HAREKET animated golden fountain-pen signature!
    # Physically erases/vanishes in the animatic!)
    # -------------------------------------------------------------------------
    if _katman_aktif(katmanlar, "af_imza"):
        sig: list[str] = ['<g id="s406-af_imza">']
        sig.append('<g transform="translate(244,266) rotate(-2.4)">')
        # Subtle warm shadow beneath cursive gold signature
        sig.append(
            '<path d="M-22,142 C-14,116 4,110 8,136 C12,150 24,118 36,126 C44,132 42,144 54,138 '
            'C66,132 76,112 86,134 C92,146 106,124 118,136 C126,142 134,132 140,136" '
            'fill="none" stroke="#6E4910" stroke-width="3.4" stroke-linecap="round" opacity="0.55"/>'
        )
        # Main shimmering golden-ink cursive signature
        sig.append(
            '<path d="M-22,140 C-14,114 4,108 8,134 C12,148 24,116 36,124 C44,130 42,142 54,136 '
            'C66,130 76,110 86,132 C92,144 106,122 118,134 C126,140 134,130 140,134" '
            'fill="none" stroke="#E8B948" stroke-width="2.6" stroke-linecap="round"/>'
        )
        # Elegant golden flourish underline
        sig.append(
            '<path d="M-16,145 Q56,139 132,143" fill="none" stroke="#F8D97C" stroke-width="1.4" stroke-linecap="round" opacity="0.88"/>'
        )
        sig.append('</g>')
        sig.append('</g>')
        parts.append("".join(sig))

    # -------------------------------------------------------------------------
    # LAYER 5: GAZETE_1 (R18-HAREKET animated spinning broadsheet newspaper!
    # Circular front-page seal centered at EXACTLY (480, 310) for A2 Shape-Match!)
    # -------------------------------------------------------------------------
    if _katman_aktif(katmanlar, "gazete_1"):
        g1: list[str] = ['<g id="s406-gazete_1">']
        # Newspaper positioned on right-center desk (x=408..922, y=72..486)
        # Rotated +3.2 deg around (665, 280), while placing the circular seal at EXACTLY (480, 310)!
        g1.append('<g transform="translate(664,280) rotate(3.2)">')
        # Drop shadow on desk
        g1.append('<rect x="-242" y="-196" width="496" height="404" rx="2" fill="#090403" opacity="0.54"/>')
        # Folded newsprint broadsheet
        g1.append(f'<rect x="-248" y="-202" width="496" height="404" rx="2" fill="url(#{p}_newsprint)" stroke="{INK}" stroke-width="2.0"/>')
        # Top newspaper masthead rules & title
        g1.append('<path d="M-230,-184 L230,-184 M-230,-142 L230,-142" fill="none" stroke="#1E1B18" stroke-width="2.2"/>')
        g1.append('<path d="M-230,-137 L230,-137" fill="none" stroke="#1E1B18" stroke-width="0.9"/>')
        g1.append(
            '<text x="0" y="-154" text-anchor="middle" font-family="Georgia, serif" '
            'font-size="25.5" font-weight="bold" fill="#171412" letter-spacing="1.6">THE CHICAGO CHRONICLE</text>'
        )
        g1.append(
            '<text x="-226" y="-124" font-family="DejaVu Sans Mono, monospace" font-size="8.0" fill="#464038">SPECIAL EDITION · CHICAGO, IL</text>'
        )
        g1.append(
            '<text x="226" y="-124" text-anchor="end" font-family="DejaVu Sans Mono, monospace" font-size="8.0" fill="#464038">FINAL · 50 CENTS</text>'
        )
        g1.append('<path d="M-230,-118 L230,-118" fill="none" stroke="#363029" stroke-width="1.1"/>')

        # HUGE BOLD FRONT-PAGE HEADLINE: "STEADMAN ALIVE!" (generous margins inside 460px!)
        g1.append(
            '<text x="0" y="-76" text-anchor="middle" font-family="DejaVu Sans, sans-serif" '
            'font-size="40.0" font-weight="bold" fill="#14110F" letter-spacing="1.2">STEADMAN ALIVE!</text>'
        )
        g1.append(
            '<text x="0" y="-52" text-anchor="middle" font-family="Georgia, serif" '
            'font-size="12.5" font-weight="bold" fill="#7A1D1D" letter-spacing="0.9">CONSPIRACY SHOCKS NATION · PARDON IN DOUBT</text>'
        )
        g1.append('<path d="M-230,-42 L230,-42" fill="none" stroke="#2A2520" stroke-width="1.3"/>')

        # Right-side stylized halftone news photograph box (Capitol / courthouse silhouette)
        g1.append('<rect x="-66" y="-28" width="296" height="128" fill="#2A2D32" stroke="#1E1B18" stroke-width="1.5"/>')
        # Stylized Capitol dome silhouette in newsprint B&W halftone
        g1.append('<path d="M-66,100 L-66,64 L22,64 L44,34 Q82,-4 120,34 L142,64 L230,64 L230,100 Z" fill="#52575E"/>')
        g1.append('<path d="M78,12 L86,12 L84,-10 L80,-10 Z" fill="#70767E"/>')
        g1.append('<rect x="-66" y="78" width="296" height="22" fill="#1E2024"/>')
        g1.append(
            '<text x="82" y="114" text-anchor="middle" font-family="DejaVu Sans Mono, monospace" '
            'font-size="7.8" fill="#3B352E">FEDERAL INVESTIGATION LAUNCHED IN WASHINGTON</text>'
        )

        # Newsprint article text columns below photograph & left column
        for col_x, col_w, y_start, n_lines in [(-228, 146, 102, 7), (-66, 138, 128, 5), (86, 142, 128, 5)]:
            for li in range(n_lines):
                yy = y_start + li * 11
                w_line = col_w if li < n_lines - 1 else col_w * 0.68
                g1.append(f'<path d="M{col_x},{yy} L{col_x+w_line:.0f},{yy}" fill="none" stroke="#4D473F" stroke-width="2.1" opacity="0.72"/>')
        g1.append('</g>')

        # === CIRCULAR FRONT-PAGE NEWSPAPER SEAL CENTERED AT EXACTLY (480, 310)! ===
        # Radius 54 matches the 4.05 brass pocket watch (r=56) at (480, 310) for seamless A2 Shape-Match!
        scx, scy = 480.0, 310.0
        g1.append(f'<g id="s406-newspaper-seal">')
        g1.append(f'<circle cx="{scx:.1f}" cy="{scy:.1f}" r="54" fill="#F2EBD9" stroke="#181512" stroke-width="3.0"/>')
        g1.append(f'<circle cx="{scx:.1f}" cy="{scy:.1f}" r="47" fill="none" stroke="#8C1D22" stroke-width="2.0" stroke-dasharray="6 3"/>')
        g1.append(f'<circle cx="{scx:.1f}" cy="{scy:.1f}" r="38" fill="#1C222B" stroke="#181512" stroke-width="1.4"/>')
        g1.append(
            f'<text x="{scx:.1f}" y="{scy-12:.1f}" text-anchor="middle" font-family="DejaVu Sans Mono, monospace" '
            f'font-size="8.4" font-weight="bold" fill="#F4C768" letter-spacing="1.0">BREAKING</text>'
        )
        g1.append(f'<path d="M{scx-26:.1f},{scy-4:.1f} L{scx+26:.1f},{scy-4:.1f}" fill="none" stroke="#F4C768" stroke-width="1.0"/>')
        g1.append(
            f'<text x="{scx:.1f}" y="{scy+9:.1f}" text-anchor="middle" font-family="Georgia, serif" '
            f'font-size="11.0" font-weight="bold" fill="#FAF6EC" letter-spacing="0.8">SPECIAL</text>'
        )
        g1.append(
            f'<text x="{scx:.1f}" y="{scy+22:.1f}" text-anchor="middle" font-family="DejaVu Sans Mono, monospace" '
            f'font-size="8.2" font-weight="bold" fill="#E87266" letter-spacing="1.0">EDITION</text>'
        )
        g1.append('</g>')

        g1.append('</g>')
        parts.append("".join(g1))

    # -------------------------------------------------------------------------
    # LAYER 6: DAMGA_REVOKED (R18-HAREKET animated red rubber stamp!)
    # Generous >= 20px padding on both sides -> ZERO box overflow!
    # -------------------------------------------------------------------------
    if _katman_aktif(katmanlar, "damga_revoked"):
        st: list[str] = ['<g id="s406-damga_revoked">']
        st.append('<g transform="translate(242,294) rotate(-13)">')
        # Outer & inner distressed crimson rubber stamp frame (width=286, height=68)
        st.append('<rect x="-143" y="-34" width="286" height="68" rx="5" fill="#B81D24" fill-opacity="0.14" stroke="#B81D24" stroke-width="4.4"/>')
        st.append('<rect x="-135" y="-26" width="270" height="52" rx="3" fill="none" stroke="#C8222A" stroke-width="1.6"/>')
        # Bold centered PARDON REVOKED stencil text (~224px wide inside 270px inner box -> 23px padding each side!)
        st.append(
            '<text x="0" y="9" text-anchor="middle" font-family="DejaVu Sans, sans-serif" '
            'font-size="23.5" font-weight="bold" fill="#B81D24" letter-spacing="1.8">PARDON REVOKED</text>'
        )
        # Authentic rubber-stamp ink speckles
        for _ in range(18):
            sx = rng.uniform(-132, 132)
            sy = rng.uniform(-26, 26)
            st.append(f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="{rng.uniform(0.8, 1.8):.1f}" fill="#F1E5CB" opacity="0.46"/>')
        st.append('</g>')
        st.append('</g>')
        parts.append("".join(st))

    # -------------------------------------------------------------------------
    # LAYER 7: PLAN (A2 Shape-Match cyan reticle at (480,310) + HUD badge)
    # -------------------------------------------------------------------------
    if _katman_aktif(katmanlar, "plan"):
        pl: list[str] = ['<g id="s406-plan" opacity="0.92">']
        # A2 Shape-Match concentric cyan CAD ring centered at EXACTLY (480, 310)
        pl.append(
            f'<circle cx="480" cy="310" r="66" fill="none" stroke="{PLAN}" '
            f'stroke-width="1.5" stroke-dasharray="8 6" opacity="0.72" filter="url(#{p}_glow_cyan)"/>'
        )
        pl.append(
            f'<path d="M406,310 L418,310 M542,310 L554,310 M480,236 L480,248 M480,372 L480,384" '
            f'fill="none" stroke="{PLAN_CORE}" stroke-width="1.4" opacity="0.80"/>'
        )
        # Top-right HUD badge (208px wide for "STATUS · REVOKED" -> >24px padding each side!)
        pl.append(_hud_badge(732, 20, 208, "STATUS · REVOKED", dot_color="#FF5B5B"))
        pl.append('</g>')
        parts.append("".join(pl))

    # -------------------------------------------------------------------------
    # LAYER 8: ONPLAN (Warm lamp dust motes & noir mahogany vignette)
    # -------------------------------------------------------------------------
    if _katman_aktif(katmanlar, "onplan"):
        op: list[str] = ['<g id="s406-onplan">']
        for _ in range(18):
            dx = rng.uniform(40, 920)
            dy = rng.uniform(50, 490)
            dr = rng.uniform(0.8, 1.8)
            op.append(f'<circle cx="{dx:.1f}" cy="{dy:.1f}" r="{dr:.1f}" fill="#FFE4A8" opacity="{rng.uniform(0.16, 0.38):.2f}"/>')
        op.append(f'<rect x="0" y="0" width="960" height="540" fill="url(#{p}_vignette)"/>')
        op.append('</g>')
        parts.append("".join(op))

    return defs, "".join(parts)


# =============================================================================
# RENDERING, AUDIT & PRESENTATION CARDS (1280×720 + R13 200% ZOOM AUDIT)
# =============================================================================
def _render_scene_png(fn, scale: int = 2, katmanlar=None) -> Image.Image:
    defs_s, body_s = fn(katmanlar=katmanlar)
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W_SCENE*scale}" height="{H_SCENE*scale}" '
        f'viewBox="0 0 {W_SCENE} {H_SCENE}">'
        f'<defs>{defs_s}</defs>{body_s}</svg>'
    )
    png_bytes = resvg_py.svg_to_bytes(svg_string=svg)
    return Image.open(io.BytesIO(png_bytes)).convert("RGBA")


def _audit_svg_integrity() -> dict[str, int]:
    """Automated check: verify every stroke-only <path> has fill='none' and all
    R18-HAREKET layers render cleanly individually AND with katmanlar=None."""
    checks = [
        ("4.04", set_404_motel_bulusma, ["uzak", "orta", "sahne", "bandaj_sar", "plan", "onplan"]),
        ("4.05", set_405_baba_saati, ["uzak", "orta", "baba_golge", "dusen_saat", "sahne", "plan", "onplan"]),
        ("4.06", set_406_manset_af, ["uzak", "orta", "sahne", "af_imza", "gazete_1", "damga_revoked", "plan", "onplan"]),
    ]
    missing_fill_none = 0
    layers_ok = 0
    for code, fn, layer_list in checks:
        defs_s, body_s = fn(katmanlar=None)
        # Check for <path> with stroke= but without fill=
        for m in re.finditer(r'<path\b[^>]*>', body_s):
            tag = m.group(0)
            if 'stroke=' in tag and 'fill=' not in tag:
                missing_fill_none += 1
        # Verify each individual layer renders cleanly via resvg_py
        for lyr in layer_list:
            img_l = _render_scene_png(fn, scale=1, katmanlar={lyr})
            assert img_l.size == (W_SCENE, H_SCENE), f"{code}:{lyr} size mismatch"
            layers_ok += 1
    return {"missing_fill_none": missing_fill_none, "layers_verified": layers_ok}


def _load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = (
        ["C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf", "C:/Windows/Fonts/DejaVuSans-Bold.ttf"]
        if bold
        else ["C:/Windows/Fonts/segoeui.ttf", "C:/Windows/Fonts/arial.ttf", "C:/Windows/Fonts/DejaVuSans.ttf"]
    )
    for fp in candidates:
        if Path(fp).exists():
            return ImageFont.truetype(fp, size)
    return ImageFont.load_default()


def _draw_card_bg(w: int, h: int) -> Image.Image:
    img = Image.new("RGBA", (w, h), "#0B111A")
    d = ImageDraw.Draw(img)
    for gx in range(0, w, 32):
        d.line((gx, 0, gx, h), fill="#121C29", width=1)
    for gy in range(0, h, 32):
        d.line((0, gy, w, gy), fill="#121C29", width=1)
    return img


def _draw_panel_box(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int]) -> None:
    draw.rounded_rectangle(box, radius=8, fill="#101824", outline="#233447", width=1)


def _draw_swatches(draw: ImageDraw.ImageDraw, x: int, y: int, colors: list[str], size: int = 18, gap: int = 6) -> None:
    for i, c in enumerate(colors):
        sx = x + i * (size + gap)
        draw.rounded_rectangle((sx, y, sx + size, y + size), radius=3, fill=c, outline="#3B536D", width=1)


def uret_kartlar(versiyon: str = "v1") -> tuple[Path, Path]:
    audit = _audit_svg_integrity()
    print(f"SVG Audit: {audit}")
    assert audit["missing_fill_none"] == 0, f"Found {audit['missing_fill_none']} stroke paths missing fill='none'!"

    img_404 = _render_scene_png(set_404_motel_bulusma, scale=2)
    img_405 = _render_scene_png(set_405_baba_saati, scale=2)
    img_406 = _render_scene_png(set_406_manset_af, scale=2)

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

    draw.text((24, 11), "MICHAEL SCOFIELD  ·  ACT IV SCENE SETS (4.04 – 4.06)", fill="#EBF3FA", font=f_title)
    draw.text((24, 35), "STYLE B+A HYBRID (CINEMATIC 2D + CYAN PLAN VISION)  ·  R18-HAREKET LIVE LAYERS (960×540)  ·  ZERO VIOLENCE",
              fill="#7E97B0", font=f_sub)
    top_swatches = [("#FF5B42", "MOTEL"), ("#4F583E", "SARA"), ("#D8A448", "WATCH"),
                    ("#B81D24", "STAMP"), ("#7FE6FF", "PLAN")]
    sx_top = 860
    for col, lbl in top_swatches:
        draw.rounded_rectangle((sx_top, 15, sx_top + 13, 28), radius=3, fill=col, outline="#3B536D", width=1)
        draw.text((sx_top + 18, 15), lbl, fill="#9BB2C8", font=f_small)
        sx_top += 80
    draw.line((24, 52, 1256, 52), fill="#213247", width=1)

    rows = [
        (
            60, img_404, "#FF8A6B", "#6B3830",
            "4.04 · MOTEL REUNION & BANDAGE", "Act IV · \"STILL HERE\"",
            ["#1C191F", "#FF5B42", "#252E38", "#4F583E", "#FAF8F3", "#7FE6FF"],
            [
                "• Rainy night window with glowing red-amber MOTEL neon",
                "• Locked Michael v3 (left) & Sara v2 (right) in single sahne",
                "• R4-ANATOMI: Collar-Over-Neck, slender F3 shoulders, 2 arms",
                "• Clean white gauze wrap (ZERO BLOOD) on live bandaj_sar",
                "• Top-right HUD badge: RENDEZVOUS · STILL HERE",
            ],
            "R4-ANATOMI & R18-HAREKET",
            "Michael v3 + Sara v2 + table live in single\n`s404-sahne` layer (zero parallax drift).\nSeparate `bandaj_sar` wraps live in animatic.",
            "LAYERS: uzak · orta · sahne · bandaj_sar · plan · onplan",
        ),
        (
            278, img_405, "#F6C367", "#7A4E30",
            "4.05 · THE FATHER'S WATCH", "Act IV · \"FATHER\" (ZERO VIOLENCE)",
            ["#D47B3E", "#F5BD6B", "#56351F", "#D8A448", "#EFE4C8", "#7FE6FF"],
            [
                "• Golden New Mexico desert sunset veranda & empty wood chair",
                "• Live `baba_golge` warm memory silhouette (fades to empty)",
                "• Live `dusen_saat` brass pocket watch & chain at (480, 310)",
                "• Cracked crystal dial stopped at 06:14 (ZERO weapons/blood)",
                "• A2 Shape-Match cyan reticle synced with 4.06 seal",
            ],
            "ZERO VIOLENCE · A2 MATCH",
            "Strictly zero weapons, blood, or violence.\nPocket watch centered at (480, 310) aligns\n1:1 with 4.06 spinning newspaper seal.",
            "LAYERS: uzak · orta · baba_golge · dusen_saat · sahne · plan · onplan",
        ),
        (
            496, img_406, "#E87266", "#6E352B",
            "4.06 · HEADLINES & VANISHING PARDON", "Act IV · \"REVOKED\"",
            ["#2B140E", "#F1E5CB", "#E8B948", "#DDD6C5", "#B81D24", "#7FE6FF"],
            [
                "• Dark mahogany desk with Presidential Pardon (BURROWS, L.)",
                "• Live `af_imza` golden signature (vanishes in animatic)",
                "• Live `gazete_1` THE CHICAGO CHRONICLE · STEADMAN ALIVE!",
                "• Circular newspaper seal centered at (480, 310) (A2 match)",
                "• Live `damga_revoked` red PARDON REVOKED rubber stamp",
            ],
            "R18-HAREKET LIVE PROPS",
            "100% English diegetic newsprint, pardon &\nstamp with >= 20px inner padding (zero box\noverflow). 3 independent animated layers.",
            "LAYERS: uzak · orta · sahne · af_imza · gazete_1 · damga_revoked · plan · onplan",
        ),
    ]

    for y0, img_s, tcol, bcol, title, sub, sw, bullets, rhead, rbody, lyr_txt in rows:
        _draw_panel_box(draw, (22, y0, 1258, y0 + 210))
        thumb = img_s.resize((320, 180), Image.Resampling.LANCZOS)
        canvas.paste(thumb, (32, y0 + 22), thumb)
        draw.rectangle((32, y0 + 22, 352, y0 + 202), outline=bcol, width=1)
        draw.text((32, y0 + 4), title, fill=tcol, font=f_card_t)
        title_w = draw.textlength(title, font=f_card_t)
        draw.text((int(32 + title_w + 14), y0 + 6), sub, fill="#9DB0C4", font=f_small)

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

    out_main = OUT_DIR / f"b4_set_bulusma_manset_{versiyon}.png"
    canvas.convert("RGB").save(out_main, quality=95)

    # =========================================================================
    # OUTPUT 2: R13 200% CROP QUALITY AUDIT CARD (1280 x 720 — 4 PANELS)
    # =========================================================================
    r13 = _draw_card_bg(1280, 720)
    d13 = ImageDraw.Draw(r13)
    d13.text((24, 13), "R13 · 200% ZOOM QUALITY AUDIT (ACT IV: 4.04 – 4.06 SETS)", fill="#EBF3FA", font=f_title)
    d13.text((24, 37), "1:1 PIXEL CROPS FROM 1920×1080 RENDERS  ·  R4-ANATOMI (NECK/COLLAR & 2 ARMS), 06:14 WATCH & REVOKED HEADLINES",
             fill="#7E97B0", font=f_sub)
    d13.line((24, 55, 1256, 55), fill="#213247", width=1)

    cw, ch = 600, 264
    crops = [
        (img_404, (670, 680), "1 · 4.04 MICHAEL V3 COLLAR-OVER-NECK & BOTH ARMS + BANDAGE (200%)",
         "Slender F3 shoulders, dark jacket collar over neck, 2 complete arms & white gauze", (22, 66)),
        (img_404, (1250, 680), "2 · 4.04 SARA V2 COLLAR-OVER-NECK & BOTH ARMS BANDAGING (200%)",
         "Olive jacket collar over neck, clean scoop top, both arms wrapping clean gauze", (652, 66)),
        (img_405, (960, 620), "3 · 4.05 BRASS POCKET WATCH 06:14 & CRACKED GLASS AT (480,310) (200%)",
         "Exact 06:14 hands, delicate chain, hairline crystal crack & A2 cyan reticle", (22, 392)),
        (img_406, None, "4 · 4.06 PARDON REVOKED (L) · STEADMAN ALIVE! & SEAL (R) (200%)",
         "Split 1:1 200% audit: PARDON REVOKED + gold signature (L) | STEADMAN ALIVE! (R)", (652, 392)),
    ]

    for src_img, center, title, sub, (bx, by) in crops:
        _draw_panel_box(d13, (bx, by, bx + 606, by + 314))
        if center is None:
            pw = 298
            for idx_p, (pcx, pcy) in enumerate([(484, 620), (1280, 415)]):
                px0 = max(0, min(src_img.width - pw, pcx - pw // 2))
                py0 = max(0, min(src_img.height - ch, pcy - ch // 2))
                p_img = src_img.crop((px0, py0, px0 + pw, py0 + ch))
                r13.paste(p_img, (bx + 3 + idx_p * (pw + 4), by + 44), p_img)
                if idx_p == 1:
                    d13.line((bx + 3 + pw + 2, by + 44, bx + 3 + pw + 2, by + 44 + ch), fill="#7FE6FF", width=2)
        else:
            cx_p, cy_p = center
            x0 = max(0, min(src_img.width - cw, cx_p - cw // 2))
            y0 = max(0, min(src_img.height - ch, cy_p - ch // 2))
            patch = src_img.crop((x0, y0, x0 + cw, y0 + ch))
            r13.paste(patch, (bx + 3, by + 44), patch)
        d13.rectangle((bx + 3, by + 44, bx + 3 + cw, by + 44 + ch), outline="#2F465E", width=1)
        d13.text((bx + 12, by + 8), title, fill="#7FE6FF", font=f_card_t)
        d13.text((bx + 12, by + 25), sub, fill="#96AEC6", font=f_small)

    out_r13 = OUT_DIR / "b4_set_bulusma_manset_r13.png"
    r13.convert("RGB").save(out_r13, quality=95)
    print(f"Saved:\n  - {out_main}\n  - {out_r13}")
    return out_main, out_r13


if __name__ == "__main__":
    uret_kartlar("v1")
