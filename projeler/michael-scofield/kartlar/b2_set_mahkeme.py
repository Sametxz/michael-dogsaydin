"""V4 (Act II — Courtroom Sentencing & Truth Letter Scene Artist) — Style B + A Hybrid.

Isolated, side-effect-free module producing 2 richly detailed, 5-layer (960x540) cinematic 2D sets:
  - set_201_mahkeme(katmanlar=None) -> (defs_svg, body_svg)  [Courtroom Sentencing · GUILTY? / DEATH SENTENCE]
  - set_202_mektup(katmanlar=None)  -> (defs_svg, body_svg)  [Apartment Truth Letter · $90,000 LOAN / FOR YOU]

Each scene uses 5 named <g> depth layers: uzak, orta, sahne, plan, onplan.
Locked character assets imported read-only from karakter.py:
  - K.lincoln_kafa(...)  [Lincoln v1]
  - K.michael_kafa(...)  [Michael v3]
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


def _uid(prefix: str = "b2") -> str:
    global _UID
    _UID += 1
    return f"{prefix}_{_UID}"


def _katman_aktif(katmanlar: set[str] | list[str] | None, ad: str) -> bool:
    return katmanlar is None or ad in katmanlar


# =============================================================================
# 2.01 · COURTROOM SENTENCING ("GUILTY?" / "DEATH SENTENCE")
# =============================================================================
def set_201_mahkeme(katmanlar: set[str] | list[str] | None = None) -> tuple[str, str]:
    """Mahogany courtroom interior under harsh cold overhead lighting and press
    camera flashes; handcuffed locked Lincoln v1 behind the wooden defendant rail
    on the right mid-ground; polished wooden gavel striking in the center foreground
    (GUILTY · DEATH PENALTY); locked Michael v3 in a dark suit with cold fury on the
    left foreground."""
    rng = random.Random(201)
    p = _uid("s201")

    defs = f"""
    <linearGradient id="{p}_wall_mahog" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#1E0E0A"/>
      <stop offset="35%" stop-color="#3A1C12"/>
      <stop offset="75%" stop-color="#4D2618"/>
      <stop offset="100%" stop-color="#28120B"/>
    </linearGradient>
    <linearGradient id="{p}_panel_wood" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#4B2517"/>
      <stop offset="50%" stop-color="#351910"/>
      <stop offset="100%" stop-color="#24100A"/>
    </linearGradient>
    <linearGradient id="{p}_cold_win" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#D7EEFA"/>
      <stop offset="55%" stop-color="#8EB4CE"/>
      <stop offset="100%" stop-color="#4B6A82"/>
    </linearGradient>
    <linearGradient id="{p}_rail_wood" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#8A4C2C"/>
      <stop offset="28%" stop-color="#5E2F1B"/>
      <stop offset="72%" stop-color="#3E1E11"/>
      <stop offset="100%" stop-color="#251008"/>
    </linearGradient>
    <linearGradient id="{p}_gavel_head" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#A86138"/>
      <stop offset="38%" stop-color="#6E351B"/>
      <stop offset="78%" stop-color="#451E0E"/>
      <stop offset="100%" stop-color="#281007"/>
    </linearGradient>
    <linearGradient id="{p}_brass" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FCE49C"/>
      <stop offset="45%" stop-color="#C89B45"/>
      <stop offset="100%" stop-color="#76531C"/>
    </linearGradient>
    <linearGradient id="{p}_suit_dark" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#273242"/>
      <stop offset="45%" stop-color="#19212C"/>
      <stop offset="100%" stop-color="#0E131A"/>
    </linearGradient>
    <linearGradient id="{p}_suit_linc" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#36404D"/>
      <stop offset="55%" stop-color="#232A33"/>
      <stop offset="100%" stop-color="#14181F"/>
    </linearGradient>
    <linearGradient id="{p}_cold_beam" x1="0.5" y1="0" x2="0.5" y2="1">
      <stop offset="0%" stop-color="#D8F2FF" stop-opacity="0.34"/>
      <stop offset="48%" stop-color="#96CBE8" stop-opacity="0.14"/>
      <stop offset="100%" stop-color="#5B91B8" stop-opacity="0.0"/>
    </linearGradient>
    <radialGradient id="{p}_flash_glow" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.96"/>
      <stop offset="28%" stop-color="#CBEFFF" stop-opacity="0.62"/>
      <stop offset="68%" stop-color="#78C2EE" stop-opacity="0.18"/>
      <stop offset="100%" stop-color="#4898D0" stop-opacity="0.0"/>
    </radialGradient>
    <radialGradient id="{p}_impact_glow" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0%" stop-color="#FFE7B3" stop-opacity="0.65"/>
      <stop offset="45%" stop-color="#D95338" stop-opacity="0.22"/>
      <stop offset="100%" stop-color="#8C1D14" stop-opacity="0.0"/>
    </radialGradient>
    <radialGradient id="{p}_vignette" cx="0.50" cy="0.48" r="0.68">
      <stop offset="48%" stop-color="#000000" stop-opacity="0.0"/>
      <stop offset="100%" stop-color="#0A0B10" stop-opacity="0.68"/>
    </radialGradient>
    <filter id="{p}_blur_soft" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="4.0" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="{p}_blur_flash" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="6.5" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    """

    parts: list[str] = []

    # -------------------------------------------------------------------------
    # LAYER 1: UZAK (Mahogany coffered wall, tall courtroom windows, State Seal,
    # Judge's bench silhouette, press gallery & blinding camera flashes)
    # -------------------------------------------------------------------------
    if _katman_aktif(katmanlar, "uzak"):
        u: list[str] = ['<g id="s201-uzak">']
        u.append(f'<rect x="0" y="0" width="960" height="540" fill="url(#{p}_wall_mahog)"/>')

        # Crown molding & dark coffered mahogany wall panels
        u.append(f'<rect x="0" y="0" width="960" height="24" fill="#1A0B07" stroke="{INK}" stroke-width="1.4"/>')
        u.append('<path d="M0,24 L960,24 M0,32 L960,32" fill="none" stroke="#6B3A23" stroke-width="1.2" opacity="0.55"/>')
        for px in range(20, 940, 118):
            u.append(f'<rect x="{px}" y="42" width="102" height="224" rx="2" fill="url(#{p}_panel_wood)" stroke="#1D0D08" stroke-width="1.6"/>')
            u.append(f'<rect x="{px+10}" y="52" width="82" height="204" fill="none" stroke="#683721" stroke-width="1.0" opacity="0.45"/>')
            # Subtle vertical mahogany wood grain inside each recessed panel
            for gx in (px + 26, px + 52, px + 76):
                u.append(f'<path d="M{gx},56 Q{gx+3},150 {gx-2},250" fill="none" stroke="#220E08" stroke-width="0.9" opacity="0.35"/>')

        # Two tall cold courtroom windows on left-back casting institutional light
        for wx in (44, 184):
            u.append(f'<rect x="{wx-6}" y="38" width="96" height="196" fill="#2A130B" stroke="{INK}" stroke-width="1.6"/>')
            u.append(f'<rect x="{wx}" y="44" width="84" height="184" fill="url(#{p}_cold_win)"/>')
            # Window muntin grid & faint venetian blinds
            for wy in range(56, 224, 14):
                u.append(f'<path d="M{wx},{wy} L{wx+84},{wy}" fill="none" stroke="#4D6A80" stroke-width="1.4" opacity="0.42"/>')
            u.append(f'<path d="M{wx+42},44 L{wx+42},228 M{wx},136 L{wx+84},136" fill="none" stroke="#2D160E" stroke-width="4.2"/>')
            u.append(f'<path d="M{wx+2},46 L{wx+82},46" fill="none" stroke="#E8F7FF" stroke-width="1.2" opacity="0.7"/>')

        # Grand Bronze State Seal & Scales of Justice above Judge's Bench (center)
        cx_s, cy_s = 478, 92
        u.append(f'<circle cx="{cx_s}" cy="{cy_s}" r="36" fill="url(#{p}_brass)" stroke="{INK_WARM}" stroke-width="1.8"/>')
        u.append(f'<circle cx="{cx_s}" cy="{cy_s}" r="30" fill="#3B1D12" stroke="#E5C068" stroke-width="1.2"/>')
        # Scales of Justice emblem inside seal
        u.append(f'<path d="M{cx_s},{cy_s-18} L{cx_s},{cy_s+16} M{cx_s-14},{cy_s+16} L{cx_s+14},{cy_s+16}" fill="none" stroke="#F6D884" stroke-width="2.0"/>')
        u.append(f'<path d="M{cx_s-20},{cy_s-8} L{cx_s+20},{cy_s-8}" fill="none" stroke="#F6D884" stroke-width="1.8"/>')
        u.append(f'<path d="M{cx_s-20},{cy_s-8} L{cx_s-25},{cy_s+4} L{cx_s-15},{cy_s+4} Z" fill="#E6C26A" stroke="#F6D884" stroke-width="0.8"/>')
        u.append(f'<path d="M{cx_s+20},{cy_s-8} L{cx_s+15},{cy_s+4} L{cx_s+25},{cy_s+4} Z" fill="#E6C26A" stroke="#F6D884" stroke-width="0.8"/>')
        u.append(f'<text x="{cx_s}" y="{cy_s+49}" text-anchor="middle" font-family="DejaVu Serif, Georgia, serif" font-size="8.5" font-weight="bold" fill="#C9A35B" letter-spacing="1.8" opacity="0.85">COOK COUNTY CIRCUIT COURT</text>')

        # Draped courtroom flags flanking the seal
        for fx, fcol in [(352, "#1A2B4C"), (604, "#5E1B20")]:
            u.append(f'<path d="M{fx},42 L{fx},218" fill="none" stroke="#9B7532" stroke-width="3.2"/>')
            u.append(f'<circle cx="{fx}" cy="38" r="4.5" fill="url(#{p}_brass)" stroke="{INK}" stroke-width="1.0"/>')
            u.append(f'<path d="M{fx-2},52 Q{fx-18},112 {fx-10},196 L{fx+16},196 Q{fx+18},120 {fx+6},52 Z" fill="{fcol}" stroke="{INK}" stroke-width="1.3" opacity="0.88"/>')
            u.append(f'<path d="M{fx-4},60 Q{fx-10},120 {fx-4},190 M{fx+6},60 Q{fx+10},120 {fx+6},190" fill="none" stroke="#D2B066" stroke-width="0.9" opacity="0.45"/>')

        # Judge's elevated mahogany bench & robed silhouette (center-back)
        # Robed judge torso & shadowed face
        u.append(f'<path d="M428,228 Q438,176 478,172 Q518,176 528,228 Z" fill="#12141A" stroke="{INK}" stroke-width="1.6"/>')
        u.append('<path d="M466,174 L478,196 L490,174 Z" fill="#D5DCE4" opacity="0.85"/>')
        u.append('<ellipse cx="478" cy="154" rx="14" ry="17" fill="#5E463B" stroke="#181210" stroke-width="1.3"/>')
        u.append('<path d="M464,148 Q478,132 492,148" fill="none" stroke="#9FA8B2" stroke-width="4.5" opacity="0.72" stroke-linecap="round"/>')
        # Bench mahogany front facade
        u.append(f'<rect x="336" y="218" width="286" height="82" fill="url(#{p}_rail_wood)" stroke="{INK}" stroke-width="1.8"/>')
        u.append(f'<rect x="328" y="212" width="302" height="10" rx="2" fill="#7D4325" stroke="{INK}" stroke-width="1.5"/>')
        u.append('<path d="M332,215 L626,215" fill="none" stroke="#CBE6F7" stroke-width="1.2" opacity="0.42"/>')
        for bpx in (358, 438, 518):
            u.append(f'<rect x="{bpx}" y="232" width="66" height="54" fill="#2E150C" stroke="#5E301B" stroke-width="1.1"/>')

        # Press Gallery in background right (silhouetted reporters & camera lenses)
        u.append(f'<rect x="640" y="196" width="320" height="104" fill="#170C09" opacity="0.86"/>')
        reporters = [(688, 178), (748, 170), (812, 176), (878, 168), (928, 180)]
        for rx_p, ry_p in reporters:
            # Head & shoulders silhouette
            u.append(f'<circle cx="{rx_p}" cy="{ry_p}" r="12" fill="#11151E" stroke="#364A5E" stroke-width="1.0"/>')
            u.append(f'<path d="M{rx_p-24},{ry_p+48} Q{rx_p-20},{ry_p+14} {rx_p},{ry_p+14} Q{rx_p+20},{ry_p+14} {rx_p+24},{ry_p+48} Z" fill="#10141C" stroke="#28384A" stroke-width="1.0"/>')
            # Raised DSLR camera silhouette
            u.append(f'<rect x="{rx_p-10}" y="{ry_p-2}" width="20" height="13" rx="2" fill="#1B222C" stroke="#64839E" stroke-width="1.0"/>')
            u.append(f'<circle cx="{rx_p}" cy="{ry_p+4}" r="4.5" fill="#2A3A4A" stroke="#A6D4F2" stroke-width="1.0"/>')

        # Press Camera Flash Bursts in background gallery (framing Lincoln cleanly, never behind his ear)
        flashes = [(644, 162, 46), (828, 164, 56), (924, 178, 34)]
        for fx_f, fy_f, fr in flashes:
            u.append(f'<circle cx="{fx_f}" cy="{fy_f}" r="{fr}" fill="url(#{p}_flash_glow)" filter="url(#{p}_blur_flash)"/>')
            # Sharp 4-point optical starburst spikes
            u.append(
                f'<path d="M{fx_f-fr*0.95},{fy_f} L{fx_f+fr*0.95},{fy_f} '
                f'M{fx_f},{fy_f-fr*0.85} L{fx_f},{fy_f+fr*0.85} '
                f'M{fx_f-fr*0.45},{fy_f-fr*0.45} L{fx_f+fr*0.45},{fy_f+fr*0.45} '
                f'M{fx_f+fr*0.45},{fy_f-fr*0.45} L{fx_f-fr*0.45},{fy_f+fr*0.45}" '
                f'fill="none" stroke="#F0FAFF" stroke-width="1.8" opacity="0.88" stroke-linecap="round"/>'
            )
            u.append(f'<circle cx="{fx_f}" cy="{fy_f}" r="5.5" fill="#FFFFFF"/>')

        u.append('</g>')
        parts.append("".join(u))

    # -------------------------------------------------------------------------
    # LAYER 2: ORTA (Handcuffed Locked Lincoln v1 behind mahogany defendant rail,
    # court bailiff behind him, legal binders & courtroom bar balusters)
    # -------------------------------------------------------------------------
    if _katman_aktif(katmanlar, "orta"):
        m: list[str] = ['<g id="s201-orta">']

        # Courtroom oak floor plane behind railing
        m.append('<rect x="0" y="294" width="960" height="246" fill="#21110B"/>')
        for fy in range(306, 540, 24):
            m.append(f'<path d="M0,{fy} L960,{fy}" fill="none" stroke="#361D13" stroke-width="1.0" opacity="0.45"/>')

        # Subtle uniformed Court Bailiff standing guard on far right behind Lincoln
        m.append(
            f'<g id="s201-bailiff" opacity="0.92">'
            f'<path d="M844,234 Q872,216 912,218 Q948,224 960,256 L960,398 L836,398 Z" '
            f'fill="#161F2D" stroke="{INK}" stroke-width="1.8"/>'
            # Crisp dark uniform collar & brass badge
            f'<path d="M882,218 L904,254 L924,218 Z" fill="#C4CED8" opacity="0.72"/>'
            f'<path d="M902,232 L908,266 L898,266 Z" fill="#10151E"/>'
            f'<polygon points="870,262 878,256 886,262 883,273 873,273" fill="url(#{p}_brass)" stroke="{INK}" stroke-width="1.0"/>'
            f'<ellipse cx="902" cy="184" rx="22" ry="26" fill="#7D5E4C" stroke="{INK}" stroke-width="1.6"/>'
            f'<path d="M880,174 Q902,152 924,174 L922,164 Q902,146 882,164 Z" fill="#1D1A18"/>'
            f'<path d="M848,236 Q874,220 906,220" fill="none" stroke="#9DD2F2" stroke-width="1.6" opacity="0.45"/>'
            f'</g>'
        )

        # === LOCKED LINCOLN V1 BEHIND DEFENDANT RAIL (right mid-ground, facing left) ===
        # Strict R4-ANATOMY: athletic 2.4x head-width shoulders (~190px) & collar-over-neck Z-order!
        m.append(
            f'<g id="s201-lincoln">'
            # 1. Back collar rim + structured athletic suit torso & sleeves (x=630..818, ~188px width)
            f'<path d="M694,244 Q724,234 754,244 L758,266 L690,266 Z" fill="#181F28" stroke="{INK}" stroke-width="1.6"/>'
            f'<path d="M636,348 L630,278 Q632,256 658,248 L694,242 L754,242 L790,248 Q816,256 818,278 L812,348 Z" '
            f'fill="url(#{p}_suit_linc)" stroke="{INK}" stroke-width="2.2" stroke-linejoin="round"/>'
            # Structured shoulder-to-sleeve seams & natural arm volume connecting down toward handcuffs
            f'<path d="M656,250 Q658,292 664,334 M792,250 Q790,292 784,334" fill="none" stroke="#11161D" stroke-width="1.8" opacity="0.72"/>'
            # Cold institutional top-rim highlight along Lincoln's structured shoulders
            f'<path d="M636,268 Q650,250 692,244 M756,244 Q798,250 812,268" fill="none" stroke="#B6E1FA" stroke-width="2.0" opacity="0.56" stroke-linecap="round"/>'
            # 2. Locked K.lincoln_kafa (view="3q", ifade="yas", boyun=True) — neck sits INSIDE collar!
            f'<g transform="translate(724,174) scale(-0.58,0.58)">'
            f'{K.lincoln_kafa(view="3q", ifade="yas", look=0.35, boyun=True)}'
            f'</g>'
            # 3. COLLAR-OVER-NECK (drawn ON TOP of neck bottom y≈258 so zero cut-off neck edge shows!)
            f'<path d="M696,246 L724,312 L752,246 Q724,258 696,246 Z" fill="#DCE4EC" stroke="{INK}" stroke-width="1.5"/>'
            # Shirt collar wings hugging throat
            f'<path d="M695,244 L708,270 L724,256 L700,240 Z" fill="#EDF2F7" stroke="{INK}" stroke-width="1.4" stroke-linejoin="round"/>'
            f'<path d="M753,244 L740,270 L724,256 L748,240 Z" fill="#CFD8E2" stroke="{INK}" stroke-width="1.4" stroke-linejoin="round"/>'
            # Dark courtroom tie knot & blade
            f'<polygon points="718,255 730,255 728,266 720,266" fill="#18202B" stroke="{INK}" stroke-width="1.2"/>'
            f'<polygon points="720,266 728,266 731,306 724,316 717,306" fill="#1E2733" stroke="{INK}" stroke-width="1.3"/>'
            # Tailored charcoal suit lapels wrapping cleanly over collar base
            f'<path d="M692,242 L674,284 L714,322 L724,310 L696,246 Z" fill="#2C3542" stroke="{INK}" stroke-width="1.6" stroke-linejoin="round"/>'
            f'<path d="M756,242 L774,284 L734,322 L724,310 L752,246 Z" fill="#1D242E" stroke="{INK}" stroke-width="1.6" stroke-linejoin="round"/>'
            f'</g>'
        )

        # === POLISHED MAHOGANY DEFENDANT RAILING (in front of Lincoln's lower torso) ===
        # Vertical turned balusters
        for bx in range(524, 956, 44):
            m.append(f'<rect x="{bx}" y="346" width="14" height="118" fill="url(#{p}_panel_wood)" stroke="{INK}" stroke-width="1.5"/>')
            m.append(f'<ellipse cx="{bx+7}" cy="376" rx="9" ry="7" fill="#63321C" stroke="{INK}" stroke-width="1.2"/>')
            m.append(f'<ellipse cx="{bx+7}" cy="422" rx="9" ry="7" fill="#522815" stroke="{INK}" stroke-width="1.2"/>')
            m.append(f'<path d="M{bx+4},350 L{bx+4},456" fill="none" stroke="#A66A46" stroke-width="1.1" opacity="0.42"/>')
        # Heavy lower wainscot base of rail
        m.append(f'<rect x="504" y="454" width="456" height="86" fill="#2A130B" stroke="{INK}" stroke-width="1.8"/>')
        # Top polished mahogany rail beam + brass corner post
        m.append(f'<rect x="502" y="330" width="458" height="22" rx="3" fill="url(#{p}_rail_wood)" stroke="{INK}" stroke-width="2.0"/>')
        m.append('<path d="M506,334 L956,334" fill="none" stroke="#C8E4F7" stroke-width="1.8" opacity="0.52"/>')
        # Newel post at x=506
        m.append(f'<rect x="492" y="316" width="32" height="224" rx="3" fill="url(#{p}_rail_wood)" stroke="{INK}" stroke-width="2.0"/>')
        m.append(f'<rect x="488" y="312" width="40" height="12" rx="2" fill="#7D4325" stroke="{INK}" stroke-width="1.6"/>')
        m.append('<path d="M498,328 L498,530" fill="none" stroke="#9B5B38" stroke-width="1.4" opacity="0.45"/>')

        # === LINCOLN'S HANDCUFFED WRISTS RESTING ON THE MAHOGANY RAIL (TATTOO-FREE per R3!) ===
        m.append(
            f'<g id="s201-handcuffs">'
            # Sleeve cuffs & hands gripping the mahogany rail
            f'<path d="M664,312 L688,334 L668,346 L644,328 Z" fill="#232B36" stroke="{INK}" stroke-width="1.6"/>'
            f'<path d="M768,312 L746,334 L766,346 L790,328 Z" fill="#1D242E" stroke="{INK}" stroke-width="1.6"/>'
            # Left & right hands (tattoo-free skin, tense knuckles)
            f'<path d="M684,328 Q702,324 708,338 Q704,352 686,350 L674,342 Z" fill="#C99C7C" stroke="{INK}" stroke-width="1.6"/>'
            f'<path d="M750,328 Q732,324 726,338 Q730,352 748,350 L760,342 Z" fill="#C99C7C" stroke="{INK}" stroke-width="1.6"/>'
            f'<path d="M694,335 L704,338 M693,341 L703,344 M740,335 L730,338 M741,341 L731,344" fill="none" stroke="#7A5038" stroke-width="1.1"/>'
            # Heavy steel handcuffs around both wrists + connecting steel chain links!
            f'<ellipse cx="682" cy="336" rx="11" ry="13" fill="none" stroke="#9EB0BE" stroke-width="4.2"/>'
            f'<ellipse cx="682" cy="336" rx="11" ry="13" fill="none" stroke="{INK}" stroke-width="1.2"/>'
            f'<ellipse cx="752" cy="336" rx="11" ry="13" fill="none" stroke="#9EB0BE" stroke-width="4.2"/>'
            f'<ellipse cx="752" cy="336" rx="11" ry="13" fill="none" stroke="{INK}" stroke-width="1.2"/>'
            # Glinting chain links sagging between cuffs
            f'<path d="M693,339 Q717,354 741,339" fill="none" stroke="#222C36" stroke-width="5.2" stroke-linecap="round"/>'
            f'<path d="M693,339 Q717,354 741,339" fill="none" stroke="#D2E4F2" stroke-width="2.4" stroke-dasharray="6 3" stroke-linecap="round"/>'
            # Specular steel glint on handcuffs
            f'<path d="M676,327 L685,325 M747,327 L756,325" fill="none" stroke="#FFFFFF" stroke-width="1.6" opacity="0.85" stroke-linecap="round"/>'
            f'</g>'
        )

        # Case file folder on defense table edge (far right bottom)
        m.append(
            f'<g transform="translate(838,448) rotate(-4)">'
            f'<rect x="-66" y="-22" width="132" height="58" rx="2" fill="#D8C39E" stroke="{INK}" stroke-width="1.5"/>'
            f'<rect x="-58" y="-14" width="116" height="42" fill="#F2E8D5" stroke="#9A8565" stroke-width="0.8"/>'
            f'<text x="-50" y="2" font-family="DejaVu Sans Mono, monospace" font-size="8" font-weight="bold" fill="#2A201A">STATE v. BURROWS</text>'
            f'<text x="-50" y="15" font-family="DejaVu Sans Mono, monospace" font-size="7" fill="#8C1D1D">CAPITAL SENTENCING</text>'
            f'</g>'
        )

        m.append('</g>')
        parts.append("".join(m))

    # -------------------------------------------------------------------------
    # LAYER 3: SAHNE (Left foreground: Locked Michael v3 in dark suit with cold
    # fury; Center foreground: Polished mahogany gavel mid-strike & GUILTY verdict)
    # -------------------------------------------------------------------------
    if _katman_aktif(katmanlar, "sahne"):
        s: list[str] = ['<g id="s201-sahne">']

        # === FOREGROUND POLISHED WOOD COURTROOM LEDGE / BENCH DESK (center-bottom) ===
        s.append(f'<polygon points="248,432 742,418 784,540 218,540" fill="url(#{p}_rail_wood)" stroke="{INK}" stroke-width="2.2"/>')
        s.append('<path d="M254,434 L738,420" fill="none" stroke="#C8E4F7" stroke-width="1.6" opacity="0.45"/>')
        for gy_t in (458, 488, 518):
            s.append(f'<path d="M242,{gy_t} Q490,{gy_t-8} 758,{gy_t}" fill="none" stroke="#240F08" stroke-width="1.1" opacity="0.42"/>')

        # === OFFICIAL COURT VERDICT SLIP ON THE FOREGROUND DESK (unobstructed right of gavel) ===
        s.append(
            f'<g transform="translate(604,478) rotate(-4)">'
            f'<polygon points="-98,-32 108,-32 114,42 -92,42" fill="#0B0706" opacity="0.42"/>'
            f'<rect x="-102" y="-36" width="206" height="72" rx="2" fill="#F2ECE0" stroke="{INK}" stroke-width="1.5"/>'
            f'<rect x="-95" y="-30" width="192" height="60" fill="none" stroke="#B6A892" stroke-width="0.9"/>'
            f'<text x="-86" y="-15" font-family="DejaVu Sans, Arial, sans-serif" font-size="7.5" font-weight="bold" fill="#3B322C" letter-spacing="1.2">CIRCUIT COURT · SENTENCE ORDER</text>'
            f'<path d="M-86,-9 L86,-9" fill="none" stroke="#7A6D5E" stroke-width="0.9"/>'
            f'<text x="-86" y="7" font-family="DejaVu Sans Mono, monospace" font-size="13.5" font-weight="bold" fill="#A6191E" letter-spacing="0.8">GUILTY</text>'
            f'<text x="-18" y="6" font-family="DejaVu Sans Mono, monospace" font-size="9.5" font-weight="bold" fill="#2A1F1B">· DEATH PENALTY</text>'
            f'<text x="-86" y="22" font-family="DejaVu Sans Mono, monospace" font-size="7.5" fill="#4C423B">DEFENDANT: BURROWS, LINCOLN</text>'
            f'</g>'
        )

        # === DRAMATIC FOREGROUND WOODEN GAVEL STRIKING SOUND BLOCK ===
        # Impact radial flash & kinetic shockwave arcs
        s.append(f'<ellipse cx="402" cy="466" rx="88" ry="42" fill="url(#{p}_impact_glow)"/>')
        for r_arc, op_a in [(44, 0.72), (66, 0.45), (86, 0.24)]:
            s.append(
                f'<path d="M{402-r_arc},458 Q402,{458-r_arc*0.42:.1f} {402+r_arc},458" '
                f'fill="none" stroke="#FFE9B5" stroke-width="1.8" opacity="{op_a}" stroke-dasharray="10 6" stroke-linecap="round"/>'
            )
        # Turned mahogany sound block (circular anvil)
        s.append(f'<ellipse cx="404" cy="492" rx="64" ry="17" fill="#140906" opacity="0.55"/>')
        s.append(f'<path d="M348,470 L348,486 Q404,506 460,486 L460,470 Z" fill="#3C1B0F" stroke="{INK}" stroke-width="2.0"/>')
        s.append(f'<ellipse cx="404" cy="470" rx="56" ry="14.5" fill="#6E351B" stroke="{INK}" stroke-width="2.0"/>')
        s.append(f'<ellipse cx="404" cy="469" rx="43" ry="10" fill="#8B4826" stroke="#3D1B0D" stroke-width="1.1"/>')
        s.append('<path d="M368,466 Q404,460 440,466" fill="none" stroke="#FFE4BA" stroke-width="1.6" opacity="0.62"/>')

        # Polished mahogany gavel mid-strike (angled down-left onto block!)
        s.append(
            f'<g transform="translate(400,434) rotate(-24)">'
            # Long turned wooden handle extending right-upward
            f'<path d="M22,-7 L166,-12 Q178,-12 178,0 Q178,12 166,12 L22,7 Z" '
            f'fill="url(#{p}_gavel_head)" stroke="{INK}" stroke-width="2.1" stroke-linejoin="round"/>'
            f'<path d="M34,-3 L162,-7" fill="none" stroke="#E8B88A" stroke-width="1.8" opacity="0.55" stroke-linecap="round"/>'
            # Brass collar around handle joint
            f'<rect x="14" y="-9" width="12" height="18" rx="1.5" fill="url(#{p}_brass)" stroke="{INK}" stroke-width="1.4"/>'
            # Heavy cylindrical mahogany gavel head
            f'<rect x="-26" y="-42" width="44" height="84" rx="8" fill="url(#{p}_gavel_head)" stroke="{INK}" stroke-width="2.3"/>'
            # Decorative turned brass bands on gavel head
            f'<rect x="-26" y="-28" width="44" height="7" fill="url(#{p}_brass)" stroke="{INK}" stroke-width="1.2"/>'
            f'<rect x="-26" y="21" width="44" height="7" fill="url(#{p}_brass)" stroke="{INK}" stroke-width="1.2"/>'
            # Specular highlight along polished wood head
            f'<path d="M-14,-36 L-14,36" fill="none" stroke="#FFE4C2" stroke-width="2.8" opacity="0.48" stroke-linecap="round"/>'
            # Strike impact white spark at bottom face of gavel head
            f'<ellipse cx="-4" cy="43" rx="18" ry="4" fill="#FFF7DC" opacity="0.88"/>'
            f'</g>'
        )

        # === LOCKED MICHAEL V3 IN LEFT FOREGROUND (dark suit, cold fury) ===
        # Strict R4-ANATOMY: lean 2.2x head-width shoulders (~240px: x=44..284) & collar-over-neck Z-order!
        s.append(
            f'<g id="s201-michael">'
            # 1. Back collar rim + tailored lean dark charcoal-navy courtroom suit torso & structured shoulders
            f'<path d="M126,282 Q166,270 206,282 L210,316 L122,316 Z" fill="#111720" stroke="{INK}" stroke-width="1.8"/>'
            f'<path d="M24,540 L40,330 Q44,298 78,290 L128,280 L204,280 L254,290 Q284,298 290,332 L302,540 Z" '
            f'fill="url(#{p}_suit_dark)" stroke="{INK}" stroke-width="2.4" stroke-linejoin="round"/>'
            # Clean tailored sleeve seams & chest pocket square
            f'<path d="M74,294 Q80,400 72,540 M256,294 Q252,400 260,540" fill="none" stroke="#0B0F15" stroke-width="2.2" opacity="0.74"/>'
            f'<polygon points="212,418 240,413 238,424 210,428" fill="#DCE6F0" stroke="{INK}" stroke-width="1.1"/>'
            # Crisp cold courtroom rim light along Michael's structured shoulders
            f'<path d="M44,322 Q50,298 82,290 L124,282 M208,282 L252,290 Q280,298 286,324" fill="none" stroke="#A6DCFA" stroke-width="2.2" opacity="0.60" stroke-linecap="round"/>'
            # 2. Locked K.michael_kafa (view="3q", ifade="ofke", boyun=True) — neck bottom y≈307 sits INSIDE collar!
            f'<g transform="translate(166,188) scale(0.84)">'
            f'{K.michael_kafa(view="3q", ifade="ofke", look=0.36, boyun=True)}'
            f'</g>'
            # 3. COLLAR-OVER-NECK (drawn ON TOP of neck bottom so zero cut-off neck edge shows!)
            # Crisp white collared dress shirt V
            f'<path d="M130,286 L166,404 L204,286 Q166,304 130,286 Z" fill="#EDF2F7" stroke="{INK}" stroke-width="1.7"/>'
            # Left & right dress shirt collar wings wrapping snugly around throat
            f'<path d="M128,282 L148,322 L166,302 L134,276 Z" fill="#F6F9FC" stroke="{INK}" stroke-width="1.6" stroke-linejoin="round"/>'
            f'<path d="M206,282 L184,322 L166,302 L198,276 Z" fill="#D5DFE8" stroke="{INK}" stroke-width="1.6" stroke-linejoin="round"/>'
            # Dark slate silk tie knot & blade
            f'<polygon points="157,300 175,300 172,316 160,316" fill="#131B26" stroke="{INK}" stroke-width="1.4"/>'
            f'<polygon points="160,316 172,316 177,390 166,410 155,390" fill="#192331" stroke="{INK}" stroke-width="1.5"/>'
            f'<path d="M163,320 L163,388" fill="none" stroke="#4D6682" stroke-width="1.3" opacity="0.55"/>'
            # Structured suit lapels with tailored notch wrapping cleanly over collar base
            f'<path d="M124,280 L94,350 L144,418 L166,406 L130,286 Z" fill="#222E3E" stroke="{INK}" stroke-width="2.0" stroke-linejoin="round"/>'
            f'<path d="M208,280 L238,350 L188,418 L166,406 L204,286 Z" fill="#18212D" stroke="{INK}" stroke-width="2.0" stroke-linejoin="round"/>'
            f'</g>'
        )

        s.append('</g>')
        parts.append("".join(s))

    # -------------------------------------------------------------------------
    # LAYER 4: PLAN (Subtle Style B+A cyan analytical sightline & verdict HUD)
    # -------------------------------------------------------------------------
    if _katman_aktif(katmanlar, "plan"):
        pl: list[str] = ['<g id="s201-plan" opacity="0.82">']
        # Sightline linking Michael's cold-fury eyes to Lincoln behind the rail
        pl.append(
            f'<path d="M222,184 L668,176" fill="none" stroke="{PLAN}" '
            f'stroke-width="1.1" stroke-dasharray="6 5" opacity="0.58"/>'
        )
        # Analytical bracket around Lincoln's handcuffs
        pl.append(
            f'<path d="M664,316 L664,306 L678,306 M770,316 L770,306 L756,306 '
            f'M664,358 L664,368 L678,368 M770,358 L770,368 L756,368" '
            f'fill="none" stroke="{PLAN}" stroke-width="1.3" opacity="0.72"/>'
        )
        # Clean monospace verdict tag above gavel impact
        pl.append(f'<rect x="312" y="346" width="174" height="22" rx="3" fill="#0B131C" opacity="0.84" stroke="{PLAN}" stroke-width="1.0"/>')
        pl.append(
            f'<text x="322" y="361" font-family="DejaVu Sans Mono, monospace" font-size="10.2" '
            f'font-weight="bold" fill="{PLAN_CORE}" letter-spacing="0.9">GUILTY · DEATH PENALTY</text>'
        )
        pl.append(f'<path d="M396,368 L396,408" fill="none" stroke="{PLAN}" stroke-width="1.1" stroke-dasharray="4 3" opacity="0.74"/>')
        pl.append(f'<circle cx="396" cy="408" r="3.2" fill="{PLAN_CORE}" stroke="{PLAN}" stroke-width="1.1"/>')
        pl.append('</g>')
        parts.append("".join(pl))

    # -------------------------------------------------------------------------
    # LAYER 5: ONPLAN (Cold overhead volumetric light cones, camera flash flare,
    # dust motes & cinematic vignette)
    # -------------------------------------------------------------------------
    if _katman_aktif(katmanlar, "onplan"):
        op: list[str] = ['<g id="s201-onplan">']
        # Soft blurred cold overhead courtroom light cones descending on Lincoln & gavel
        op.append(f'<polygon points="620,0 820,0 890,540 550,540" fill="url(#{p}_cold_beam)" opacity="0.85" filter="url(#{p}_blur_flash)"/>')
        op.append(f'<polygon points="340,0 510,0 590,540 270,540" fill="url(#{p}_cold_beam)" opacity="0.65" filter="url(#{p}_blur_flash)"/>')
        # Diagonal light shafts from tall left courtroom windows
        op.append(f'<polygon points="44,44 128,44 380,380 240,380" fill="#CBEAFF" opacity="0.07" filter="url(#{p}_blur_soft)"/>')
        # Subtle optical anamorphic streak from press camera flash
        op.append(f'<path d="M600,164 L960,164" fill="none" stroke="#E0F7FF" stroke-width="2.0" opacity="0.28" filter="url(#{p}_blur_soft)"/>')
        # Dust motes in cold top-light
        for _ in range(28):
            dx = rng.uniform(220, 880)
            dy = rng.uniform(40, 460)
            dr = rng.uniform(0.8, 1.9)
            op.append(f'<circle cx="{dx:.1f}" cy="{dy:.1f}" r="{dr:.1f}" fill="#DFF5FF" opacity="{rng.uniform(0.18, 0.45):.2f}"/>')
        # Cinematic vignette
        op.append(f'<rect x="0" y="0" width="960" height="540" fill="url(#{p}_vignette)"/>')
        op.append('</g>')
        parts.append("".join(op))

    return defs, "".join(parts)


# =============================================================================
# 2.02 · APARTMENT TRUTH LETTER ("$90,000 LOAN" / "FOR YOU")
# =============================================================================
def set_202_mektup(katmanlar: set[str] | list[str] | None = None) -> tuple[str, str]:
    """Rainy night apartment study desk: warm brass desk lamp illuminating an
    opened truth letter and a red-stamped '$90,000 LOAN — FOR MICHAEL'S TUITION'
    debt document; rain-streaked midnight window behind; locked Michael v3
    beside the desk in shock and remorse, with the very first #7FE6FF cyan spark
    igniting in his eyes."""
    rng = random.Random(202)
    p = _uid("s202")

    defs = f"""
    <linearGradient id="{p}_night_sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#060D1A"/>
      <stop offset="55%" stop-color="#0E1C30"/>
      <stop offset="100%" stop-color="#192D46"/>
    </linearGradient>
    <linearGradient id="{p}_room_wall" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#141C27"/>
      <stop offset="48%" stop-color="#1D222A"/>
      <stop offset="100%" stop-color="#282019"/>
    </linearGradient>
    <linearGradient id="{p}_desk_wood" x1="0" y1="0" x2="1" y2="0.4">
      <stop offset="0%" stop-color="#4A2B18"/>
      <stop offset="38%" stop-color="#6E4224"/>
      <stop offset="72%" stop-color="#4E2D18"/>
      <stop offset="100%" stop-color="#2A170D"/>
    </linearGradient>
    <linearGradient id="{p}_lamp_shade" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#24523B"/>
      <stop offset="58%" stop-color="#1B3E2D"/>
      <stop offset="100%" stop-color="#F6D186"/>
    </linearGradient>
    <linearGradient id="{p}_brass_lamp" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F7DF9A"/>
      <stop offset="50%" stop-color="#BE8E3D"/>
      <stop offset="100%" stop-color="#6B4A19"/>
    </linearGradient>
    <radialGradient id="{p}_lamp_pool" cx="0.5" cy="0.45" r="0.55">
      <stop offset="0%" stop-color="#FFE8A8" stop-opacity="0.74"/>
      <stop offset="42%" stop-color="#F2AA49" stop-opacity="0.30"/>
      <stop offset="78%" stop-color="#C97324" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="#8A4412" stop-opacity="0.0"/>
    </radialGradient>
    <linearGradient id="{p}_paper_letter" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFFDF5"/>
      <stop offset="58%" stop-color="#F2E7CE"/>
      <stop offset="100%" stop-color="#DAC8A7"/>
    </linearGradient>
    <linearGradient id="{p}_paper_doc" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FAF4E4"/>
      <stop offset="65%" stop-color="#E9DEC4"/>
      <stop offset="100%" stop-color="#D2C2A2"/>
    </linearGradient>
    <linearGradient id="{p}_shirt_dark" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#35465C"/>
      <stop offset="48%" stop-color="#222F40"/>
      <stop offset="100%" stop-color="#131B26"/>
    </linearGradient>
    <radialGradient id="{p}_cyan_spark" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="1.0"/>
      <stop offset="32%" stop-color="#7FE6FF" stop-opacity="0.92"/>
      <stop offset="70%" stop-color="#38B6E8" stop-opacity="0.32"/>
      <stop offset="100%" stop-color="#1E82B8" stop-opacity="0.0"/>
    </radialGradient>
    <radialGradient id="{p}_vignette" cx="0.46" cy="0.54" r="0.68">
      <stop offset="46%" stop-color="#000000" stop-opacity="0.0"/>
      <stop offset="100%" stop-color="#070B12" stop-opacity="0.70"/>
    </radialGradient>
    <filter id="{p}_glow_warm" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="5.5" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="{p}_glow_cyan" x="-60%" y="-60%" width="220%" height="220%">
      <feGaussianBlur stdDeviation="2.6" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    """

    parts: list[str] = []

    # -------------------------------------------------------------------------
    # LAYER 1: UZAK (Rainy midnight Chicago skyline outside window, dark apartment
    # wall, framed architectural bridge blueprint & bookshelf edge)
    # -------------------------------------------------------------------------
    if _katman_aktif(katmanlar, "uzak"):
        u: list[str] = ['<g id="s202-uzak">']
        u.append(f'<rect x="0" y="0" width="960" height="540" fill="url(#{p}_room_wall)"/>')

        # Subtle apartment plaster wall texture & baseboard
        for wx_s in range(470, 960, 42):
            u.append(f'<path d="M{wx_s},0 L{wx_s},360" fill="none" stroke="#0E131B" stroke-width="0.9" opacity="0.25"/>')

        # Tall rainy apartment window opening on left (x=36..442, y=22..326)
        wx0, wy0, ww, wh = 36, 22, 406, 304
        u.append(f'<rect x="{wx0}" y="{wy0}" width="{ww}" height="{wh}" fill="url(#{p}_night_sky)"/>')

        # Distant Chicago night skyline buildings & warm lit apartment windows
        bldgs = [
            (40, 148, 66, 178, "#09111E"),
            (102, 112, 74, 214, "#0C1626"),
            (172, 168, 58, 158, "#08101C"),
            (226, 94, 88, 232, "#0B1524"),
            (310, 136, 68, 190, "#091220"),
            (374, 158, 68, 168, "#070E19"),
        ]
        for bx, by, bw, bh, bcol in bldgs:
            u.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" fill="{bcol}"/>')
            for wy_b in range(by + 14, wy0 + wh - 18, 20):
                for wx_b in range(bx + 10, bx + bw - 12, 16):
                    if rng.random() < 0.34:
                        lcol = "#E8B96B" if rng.random() < 0.68 else "#7EBCE0"
                        u.append(f'<rect x="{wx_b}" y="{wy_b}" width="7" height="10" fill="{lcol}" opacity="{rng.uniform(0.28, 0.72):.2f}"/>')

        # Soft distant city streetlight bokeh circles through rainy night
        for bkx, bky, bkr, bkcol in [
            (94, 272, 12, "#F2B863"),
            (196, 286, 9, "#7FC8F2"),
            (288, 266, 14, "#F5B85B"),
            (364, 284, 10, "#E86852"),
        ]:
            u.append(f'<circle cx="{bkx}" cy="{bky}" r="{bkr}" fill="{bkcol}" opacity="0.22"/>')
            u.append(f'<circle cx="{bkx}" cy="{bky}" r="{bkr*0.42:.1f}" fill="{bkcol}" opacity="0.48"/>')

        # Slanted falling rain streaks outside the window
        for _ in range(78):
            rx_r = rng.uniform(wx0 + 6, wx0 + ww - 6)
            ry_r = rng.uniform(wy0 + 6, wy0 + wh - 24)
            rlen = rng.uniform(16, 34)
            u.append(
                f'<path d="M{rx_r:.1f},{ry_r:.1f} L{rx_r-5.5:.1f},{ry_r+rlen:.1f}" '
                f'fill="none" stroke="#9AC8EA" stroke-width="0.9" opacity="{rng.uniform(0.18, 0.46):.2f}"/>'
            )

        # Framed structural-engineering bridge blueprint on right apartment wall (foreshadowing!)
        u.append(f'<rect x="524" y="42" width="166" height="114" rx="2" fill="#2A1D16" stroke="{INK}" stroke-width="1.8"/>')
        u.append('<rect x="532" y="50" width="150" height="98" fill="#10253A" stroke="#3E617D" stroke-width="1.0"/>')
        # Fine blueprint truss drawing inside frame
        u.append('<path d="M544,122 L670,122 M556,122 L582,84 L608,122 L634,84 L660,122 M582,84 L634,84" fill="none" stroke="#7FE6FF" stroke-width="1.0" opacity="0.58"/>')
        u.append('<path d="M544,128 L670,128" fill="none" stroke="#7FE6FF" stroke-width="0.6" stroke-dasharray="3 2" opacity="0.42"/>')
        u.append('<text x="540" y="66" font-family="DejaVu Sans Mono, monospace" font-size="6.5" fill="#9EDCF2" opacity="0.65">STRUCTURAL TRUSS · REV 04</text>')

        # Dark wood bookshelf edge on far right wall
        u.append(f'<rect x="854" y="24" width="106" height="316" fill="#1F1510" stroke="{INK}" stroke-width="1.8"/>')
        for sy_b in (106, 192, 278):
            u.append(f'<rect x="860" y="{sy_b}" width="98" height="9" fill="#3B2518" stroke="{INK}" stroke-width="1.2"/>')
            # Stacked engineering books with varied heights & colors
            bx_bk = 866
            for bw_k, bh_k, bcol_k in [(14, 58, "#3B4F66"), (11, 50, "#6E2E26"), (16, 62, "#2A3C35"), (13, 54, "#5A452C"), (15, 60, "#243242")]:
                u.append(f'<rect x="{bx_bk}" y="{sy_b-bh_k}" width="{bw_k}" height="{bh_k}" fill="{bcol_k}" stroke="{INK}" stroke-width="1.1"/>')
                bx_bk += bw_k + 2

        u.append('</g>')
        parts.append("".join(u))

    # -------------------------------------------------------------------------
    # LAYER 2: ORTA (Rain-beaded apartment window frame & curtain; Locked
    # Michael v3 on right in shock/remorse with FIRST #7FE6FF CYAN SPARK in eyes!)
    # -------------------------------------------------------------------------
    if _katman_aktif(katmanlar, "orta"):
        m: list[str] = ['<g id="s202-orta">']

        wx0, wy0, ww, wh = 36, 22, 406, 304
        # Rain droplets & vertical trickle streaks on the apartment glass
        m.append('<polygon points="40,26 184,26 112,322 40,322" fill="#8DC8EE" opacity="0.06"/>')
        for _ in range(48):
            gx = rng.uniform(wx0 + 12, wx0 + ww - 12)
            gy = rng.uniform(wy0 + 12, wy0 + wh - 14)
            gr = rng.uniform(1.3, 3.3)
            m.append(f'<ellipse cx="{gx:.1f}" cy="{gy:.1f}" rx="{gr*0.72:.1f}" ry="{gr:.1f}" fill="#C8E8FF" opacity="{rng.uniform(0.30, 0.72):.2f}"/>')
            if rng.random() < 0.40:
                m.append(
                    f'<path d="M{gx:.1f},{gy:.1f} L{gx+rng.uniform(-1.2, 1.2):.1f},{gy+rng.uniform(16, 48):.1f}" '
                    f'fill="none" stroke="#A6D0EC" stroke-width="0.95" opacity="0.34"/>'
                )

        # Heavy dark wooden window casing, mullions & sill
        m.append(f'<rect x="{wx0-10}" y="{wy0-10}" width="{ww+20}" height="{wh+20}" fill="none" stroke="#2D1D15" stroke-width="12"/>')
        m.append(f'<rect x="{wx0}" y="{wy0}" width="{ww}" height="{wh}" fill="none" stroke="#16100D" stroke-width="2.2"/>')
        # Cross mullions (2x2 panes)
        m.append(f'<rect x="{wx0+ww//2-5}" y="{wy0}" width="10" height="{wh}" fill="#2B1C14" stroke="{INK}" stroke-width="1.4"/>')
        m.append(f'<rect x="{wx0}" y="{wy0+148}" width="{ww}" height="10" fill="#2B1C14" stroke="{INK}" stroke-width="1.4"/>')
        # Window sill catching cold rain reflection
        m.append(f'<rect x="{wx0-18}" y="{wy0+wh-2}" width="{ww+36}" height="16" rx="2" fill="#3C261A" stroke="{INK}" stroke-width="1.8"/>')
        m.append(f'<path d="M{wx0-14},{wy0+wh+1} L{wx0+ww+14},{wy0+wh+1}" fill="none" stroke="#9AC4E2" stroke-width="1.4" opacity="0.45"/>')

        # Heavy draped midnight-blue curtain on far left
        m.append(f'<path d="M0,0 L76,0 Q58,140 66,356 L0,356 Z" fill="#182330" stroke="{INK}" stroke-width="1.8"/>')
        m.append('<path d="M24,0 Q16,160 28,350 M48,0 Q38,150 52,350" fill="none" stroke="#0D141D" stroke-width="2.2" opacity="0.72"/>')
        m.append('<path d="M62,12 Q54,140 62,340" fill="none" stroke="#4D6E8C" stroke-width="1.4" opacity="0.35"/>')

        m.append('</g>')
        parts.append("".join(m))

    # -------------------------------------------------------------------------
    # LAYER 3: SAHNE (Single-layer R4-PARALAKS: Locked Michael v3 with lean F3
    # shoulders, collar-over-neck Z-order, first #7FE6FF cyan spark & continuous
    # shoulder->upper-arm->elbow->forearm->hand resting beside $90,000 LOAN doc;
    # walnut desk, brass/emerald lamp, opened letter & drafting tools)
    # -------------------------------------------------------------------------
    if _katman_aktif(katmanlar, "sahne"):
        s: list[str] = ['<g id="s202-sahne">']

        # === LOCKED MICHAEL V3 UPPER TORSO & HEAD (behind desk edge, SAME s202-sahne layer for R4-PARALAKS!) ===
        # Strict R4-ANATOMY: lean 2.2x head-width shoulders (~222px: x=614..836) & collar-over-neck Z-order!
        s.append(
            f'<g id="s202-michael-body">'
            # 1. Back collar rim + lean structured dark navy-slate button-down torso (x=614..836)
            f'<path d="M684,274 Q722,262 760,274 L764,306 L680,306 Z" fill="#17202C" stroke="{INK}" stroke-width="1.6"/>'
            f'<path d="M608,358 L616,304 Q620,282 652,276 L690,268 L754,268 L794,276 Q826,282 834,308 L846,374 L608,374 Z" '
            f'fill="url(#{p}_shirt_dark)" stroke="{INK}" stroke-width="2.2" stroke-linejoin="round"/>'
            # Natural shoulder seams & far-left sleeve dropping behind desk
            f'<path d="M648,278 Q642,318 640,356 M792,278 Q796,318 798,356" fill="none" stroke="#0E151E" stroke-width="1.8" opacity="0.72"/>'
            # Warm amber lamp rim light on Michael's left (lamp-facing) shoulder
            f'<path d="M618,308 Q624,284 654,276 L688,270" fill="none" stroke="#FFCE82" stroke-width="2.4" opacity="0.70" stroke-linecap="round"/>'
            # Cool rainy night rim light on Michael's right (window-opposite) shoulder
            f'<path d="M758,270 L794,276 Q824,284 832,308" fill="none" stroke="#7CB6DE" stroke-width="1.8" opacity="0.40" stroke-linecap="round"/>'
            # 2. Locked K.michael_kafa (view="3q", ifade="yas", boyun=True) — neck bottom y≈295 sits INSIDE collar!
            f'<g transform="translate(722,184) scale(-0.78,0.78)">'
            f'{K.michael_kafa(view="3q", ifade="yas", look=0.35, boyun=True)}'
            f'</g>'
            # 3. COLLAR-OVER-NECK (drawn ON TOP of neck bottom y≈295 so zero cut-off neck edge shows!)
            # Inner white tee neckline & chest placket
            f'<path d="M690,272 Q720,308 752,272 L746,304 Q720,334 696,304 Z" fill="#EAE6DC" stroke="{INK}" stroke-width="1.6"/>'
            f'<path d="M696,294 L716,356 L728,356 L746,294" fill="none" stroke="#121A24" stroke-width="1.4" opacity="0.65"/>'
            # Unbuttoned navy-slate shirt collar wings wrapping snugly around throat
            f'<path d="M686,268 L664,306 L702,324 L718,308 L692,270 Z" fill="#3D526B" stroke="{INK}" stroke-width="1.7" stroke-linejoin="round"/>'
            f'<path d="M756,268 L778,306 L740,324 L722,308 L750,270 Z" fill="#273649" stroke="{INK}" stroke-width="1.7" stroke-linejoin="round"/>'
            f'<circle cx="718" cy="336" r="2.5" fill="#C4CCD4" stroke="{INK}" stroke-width="1.0"/>'
            # === THE VERY FIRST #7FE6FF CYAN SPARK IGNITING DEAD-CENTER IN MICHAEL'S PUPILS ===
            f'<g id="s202-cyan-eye-spark" filter="url(#{p}_glow_cyan)">'
            f'<circle cx="689" cy="178" r="5.8" fill="url(#{p}_cyan_spark)"/>'
            f'<path d="M683,178 L695,178 M689,172 L689,184" fill="none" stroke="{PLAN_CORE}" stroke-width="1.15" opacity="0.95" stroke-linecap="round"/>'
            f'<circle cx="689" cy="178" r="1.8" fill="#FFFFFF"/>'
            f'<circle cx="727" cy="178" r="5.0" fill="url(#{p}_cyan_spark)"/>'
            f'<path d="M722,178 L732,178 M727,173 L727,183" fill="none" stroke="{PLAN_CORE}" stroke-width="1.0" opacity="0.90" stroke-linecap="round"/>'
            f'<circle cx="727" cy="178" r="1.5" fill="#FFFFFF"/>'
            f'</g>'
            f'</g>'
        )

        # Perspective walnut study desk surface (overlaps Michael's lower chest cleanly at y≈346)
        s.append(f'<polygon points="0,356 144,332 960,348 960,540 0,540" fill="url(#{p}_desk_wood)" stroke="{INK_WARM}" stroke-width="2.2"/>')
        # Rich wood grain lines across desk
        for gy_d in (368, 396, 432, 474, 514):
            s.append(f'<path d="M0,{gy_d} Q360,{gy_d-10} 960,{gy_d+6}" fill="none" stroke="#26140B" stroke-width="1.2" opacity="0.38"/>')
        # Warm golden specular lamp pool directly across the desk papers
        s.append(f'<ellipse cx="386" cy="436" rx="285" ry="96" fill="url(#{p}_lamp_pool)"/>')

        # === VINTAGE BRASS & EMERALD BANKER'S DESK LAMP (left side of desk) ===
        s.append(
            f'<g id="s202-lamp">'
            # Heavy circular brass base on desk
            f'<ellipse cx="122" cy="364" rx="48" ry="14" fill="#1A0E08" opacity="0.48"/>'
            f'<ellipse cx="122" cy="358" rx="44" ry="12" fill="url(#{p}_brass_lamp)" stroke="{INK_WARM}" stroke-width="1.8"/>'
            f'<ellipse cx="122" cy="354" rx="28" ry="7" fill="#D9AC54" stroke="{INK_WARM}" stroke-width="1.2"/>'
            # Curved articulated brass stem
            f'<path d="M122,350 Q108,266 138,214 Q158,184 198,196" fill="none" stroke="{INK_WARM}" stroke-width="11" stroke-linecap="round"/>'
            f'<path d="M122,350 Q108,266 138,214 Q158,184 198,196" fill="none" stroke="url(#{p}_brass_lamp)" stroke-width="6.8" stroke-linecap="round"/>'
            f'<circle cx="138" cy="214" r="6" fill="url(#{p}_brass_lamp)" stroke="{INK_WARM}" stroke-width="1.3"/>'
            # Iconic emerald-glass banker's shade angled down-right toward the papers
            f'<g transform="translate(206,204) rotate(18)">'
            f'<path d="M-46,24 Q-42,-16 0,-18 Q42,-16 46,24 Z" fill="url(#{p}_lamp_shade)" stroke="{INK_WARM}" stroke-width="2.0"/>'
            f'<path d="M-32,2 Q0,-10 32,2" fill="none" stroke="#58A87E" stroke-width="1.8" opacity="0.55" stroke-linecap="round"/>'
            # Glowing warm bulb opening underneath shade
            f'<ellipse cx="0" cy="24" rx="44" ry="9" fill="#FFF7D6" stroke="#8C6226" stroke-width="1.4" filter="url(#{p}_glow_warm)"/>'
            # Brass pull chain
            f'<path d="M-24,26 L-28,62" fill="none" stroke="#D9AC54" stroke-width="1.6"/>'
            f'<circle cx="-28" cy="64" r="3.2" fill="#F2D07A" stroke="{INK_WARM}" stroke-width="1.0"/>'
            f'</g>'
            f'</g>'
        )

        # === TORN ENVELOPE ON FAR LEFT DESK ===
        s.append(
            f'<g transform="translate(114,442) rotate(-14)">'
            f'<polygon points="-66,-30 68,-30 74,38 -60,38" fill="#1A0E07" opacity="0.38"/>'
            f'<path d="M-68,-32 L58,-32 L68,-14 L60,0 L68,16 L58,34 L-68,34 Z" fill="#C9A878" stroke="{INK_WARM}" stroke-width="1.6"/>'
            f'<path d="M-64,-28 L0,6 L58,-28" fill="none" stroke="#8B6B40" stroke-width="1.3"/>'
            f'<text x="-54" y="18" font-family="DejaVu Serif, Georgia, serif" font-size="9.5" font-style="italic" fill="#3B291B">To: Michael Scofield</text>'
            f'</g>'
        )

        # === PROP 1: OPENED HANDWRITTEN TRUTH LETTER (left-center foreground) ===
        s.append(
            f'<g transform="translate(274,446) rotate(-5)">'
            f'<polygon points="-96,-72 104,-72 110,78 -90,78" fill="#180D06" opacity="0.38"/>'
            f'<rect x="-100" y="-76" width="200" height="150" rx="2" fill="url(#{p}_paper_letter)" stroke="{INK_WARM}" stroke-width="1.6"/>'
            # Horizontal letter fold creases (trifold shadow bands)
            f'<path d="M-100,-24 L100,-24 M-100,26 L100,26" fill="none" stroke="#BFA988" stroke-width="1.2" opacity="0.72"/>'
            f'<rect x="-99" y="-24" width="198" height="8" fill="#C8B290" opacity="0.18"/>'
            f'<rect x="-99" y="26" width="198" height="8" fill="#C8B290" opacity="0.18"/>'
            # Neat handwritten letter lines (100% English!)
            f'<text x="-84" y="-52" font-family="DejaVu Serif, Georgia, serif" font-size="10.5" font-style="italic" font-weight="bold" fill="#2A1F18">Michael,</text>'
            f'<text x="-84" y="-34" font-family="DejaVu Serif, Georgia, serif" font-size="8.6" font-style="italic" fill="#3C2E24">There was never any insurance.</text>'
            f'<text x="-84" y="-12" font-family="DejaVu Serif, Georgia, serif" font-size="8.6" font-style="italic" fill="#3C2E24">Lincoln borrowed every dollar</text>'
            f'<text x="-84" y="4" font-family="DejaVu Serif, Georgia, serif" font-size="8.6" font-style="italic" fill="#3C2E24">so you could finish college.</text>'
            f'<text x="-84" y="20" font-family="DejaVu Serif, Georgia, serif" font-size="8.6" font-style="italic" fill="#3C2E24">He took the debt in silence...</text>'
            f'<text x="-84" y="46" font-family="DejaVu Serif, Georgia, serif" font-size="11.5" font-style="italic" font-weight="bold" fill="#8C1D1A">He did it FOR YOU.</text>'
            f'<path d="M-84,51 L34,51" fill="none" stroke="#8C1D1A" stroke-width="1.1" opacity="0.65"/>'
            f'</g>'
        )

        # === PROP 2: RED-STAMPED '$90,000 LOAN — FOR MICHAEL'S TUITION' DEBT DOCUMENT (hero foreground) ===
        s.append(
            f'<g transform="translate(506,448) rotate(3)">'
            # Soft drop shadow
            f'<polygon points="-132,-78 138,-78 144,82 -126,82" fill="#160B05" opacity="0.45"/>'
            # Cream bond paper sheet
            f'<rect x="-136" y="-82" width="272" height="158" rx="2" fill="url(#{p}_paper_doc)" stroke="{INK_WARM}" stroke-width="1.8"/>'
            f'<rect x="-128" y="-74" width="256" height="142" fill="none" stroke="#9C8B72" stroke-width="1.0"/>'
            # Header
            f'<text x="-118" y="-56" font-family="DejaVu Sans, Arial, sans-serif" font-size="8.5" font-weight="bold" fill="#2A241F" letter-spacing="1.2">PRIVATE DEBT INSTRUMENT · CHICAGO</text>'
            f'<path d="M-118,-49 L118,-49" fill="none" stroke="#4D4238" stroke-width="1.2"/>'
            # Loan particulars
            f'<text x="-118" y="-33" font-family="DejaVu Sans Mono, monospace" font-size="8.2" fill="#4A3F36">BORROWER: BURROWS, LINCOLN</text>'
            f'<text x="-118" y="-19" font-family="DejaVu Sans Mono, monospace" font-size="8.2" fill="#4A3F36">PRINCIPAL: $90,000.00 USD</text>'
            f'<path d="M-118,-10 L118,-10" fill="none" stroke="#B5A48B" stroke-width="0.8"/>'
            # Bold centerpiece red-bordered stamp box
            f'<g transform="translate(0,18) rotate(-4)">'
            f'<rect x="-116" y="-26" width="232" height="52" rx="3" fill="#B81D24" fill-opacity="0.09" stroke="#B81D24" stroke-width="2.4"/>'
            f'<rect x="-112" y="-22" width="224" height="44" rx="2" fill="none" stroke="#B81D24" stroke-width="0.9" stroke-dasharray="4 2"/>'
            f'<text x="0" y="-2" text-anchor="middle" font-family="DejaVu Sans Mono, monospace" font-size="17" font-weight="bold" fill="#B21A20" letter-spacing="1.0">$90,000 LOAN</text>'
            f'<text x="0" y="15" text-anchor="middle" font-family="DejaVu Sans, Arial, sans-serif" font-size="9.5" font-weight="bold" fill="#8C151A" letter-spacing="1.2">FOR MICHAEL&apos;S TUITION</text>'
            f'</g>'
            # Circular crimson notary/debt seal at bottom right
            f'<g transform="translate(96,52)">'
            f'<circle cx="0" cy="0" r="17" fill="#B21A20" fill-opacity="0.16" stroke="#B21A20" stroke-width="1.8"/>'
            f'<circle cx="0" cy="0" r="13" fill="none" stroke="#B21A20" stroke-width="0.8" stroke-dasharray="2 2"/>'
            f'<text x="0" y="3" text-anchor="middle" font-family="DejaVu Sans, Arial, sans-serif" font-size="6.2" font-weight="bold" fill="#9E161C">FOR YOU</text>'
            f'</g>'
            # Signature line at bottom left
            f'<path d="M-118,58 L46,58" fill="none" stroke="#5A4D42" stroke-width="0.9"/>'
            f'<path d="M-108,54 Q-86,44 -68,53 Q-50,59 -28,48 Q-12,45 10,54" fill="none" stroke="#223044" stroke-width="1.3" opacity="0.85"/>'
            f'</g>'
        )

        # === MICHAEL'S CONTINUOUS RIGHT ARM (SHOULDER -> UPPER ARM -> ELBOW -> FOREARM -> CLEAN HAND ON DESK) ===
        # Connected seamlessly from his right shoulder (x=794..834, y=282..308) down across the desk edge to the $90,000 loan!
        s.append(
            f'<g id="s202-michael-arm">'
            # Soft contact shadow under forearm & hand on the walnut desk
            f'<path d="M652,452 Q726,466 836,422 Q852,410 834,400 L666,436 Z" fill="#180D06" opacity="0.42"/>'
            # Continuous bent sleeve: right shoulder (792,282) -> upper arm -> bent elbow (840,398) -> forearm -> cuff (698,418..708,448)
            f'<path d="M792,280 Q826,286 836,314 L848,386 Q852,412 824,424 L710,450 L698,420 L794,386 L792,326 Z" '
            f'fill="url(#{p}_shirt_dark)" stroke="{INK}" stroke-width="2.2" stroke-linejoin="round"/>'
            # Elbow fold creases & shirt sleeve cuff seam
            f'<path d="M794,386 Q814,394 826,386 M792,374 Q808,382 818,376" fill="none" stroke="#101720" stroke-width="1.6" opacity="0.72" stroke-linecap="round"/>'
            f'<path d="M708,417 L718,448" fill="none" stroke="#101720" stroke-width="1.5"/>'
            f'<circle cx="716" cy="436" r="2.0" fill="#C4CCD4" stroke="{INK}" stroke-width="0.9"/>'
            # Warm desk-lamp highlight along forearm top edge & cool rim on outer upper arm
            f'<path d="M706,420 L794,388" fill="none" stroke="#FFD691" stroke-width="1.8" opacity="0.52" stroke-linecap="round"/>'
            f'<path d="M834,314 L846,386" fill="none" stroke="#7CB6DE" stroke-width="1.6" opacity="0.38" stroke-linecap="round"/>'
            # Pre-tattoo clean wrist & tense hand resting beside the $90,000 LOAN document
            f'<path d="M700,421 Q670,423 656,439 Q659,455 686,455 L709,448 Z" fill="#D5A687" stroke="{INK}" stroke-width="1.8" stroke-linejoin="round"/>'
            f'<path d="M663,436 L682,438 M662,444 L681,446 M668,450 L683,451" fill="none" stroke="#8C5C44" stroke-width="1.1"/>'
            f'<path d="M662,429 Q677,423 696,425" fill="none" stroke="#FFE0AA" stroke-width="1.6" opacity="0.58" stroke-linecap="round"/>'
            f'</g>'
        )

        # === ARCHITECTURAL DRAFTING PENCIL & STEEL COMPASS ON RIGHT DESK EDGE ===
        s.append(
            f'<g transform="translate(822,492) rotate(-18)">'
            f'<rect x="-56" y="-4" width="96" height="8" rx="1" fill="#D9A338" stroke="{INK_WARM}" stroke-width="1.3"/>'
            f'<polygon points="40,-4 54,0 40,4" fill="#E8CFA6" stroke="{INK_WARM}" stroke-width="1.2"/>'
            f'<polygon points="49,-1.5 54,0 49,1.5" fill="#1A1715"/>'
            f'<rect x="-66" y="-4" width="10" height="8" fill="#B85A5A" stroke="{INK_WARM}" stroke-width="1.2"/>'
            f'</g>'
        )

        s.append('</g>')
        parts.append("".join(s))

    # -------------------------------------------------------------------------
    # LAYER 4: PLAN (First electric #7FE6FF cyan spark arcing from $90,000 LOAN
    # document straight into Michael's eyes — the birth of Plan Vision!)
    # -------------------------------------------------------------------------
    if _katman_aktif(katmanlar, "plan"):
        pl: list[str] = ['<g id="s202-plan" opacity="0.86">']
        # Crisp analytical cyan line rising from the $90,000 LOAN stamp to Michael's cyan eye spark
        pl.append(
            f'<path d="M568,430 L626,374 L626,226 L690,182" fill="none" stroke="{PLAN}" '
            f'stroke-width="1.3" stroke-dasharray="6 4" opacity="0.78"/>'
        )
        pl.append(f'<circle cx="568" cy="430" r="3.5" fill="{PLAN_CORE}" stroke="{PLAN}" stroke-width="1.2"/>')
        pl.append(f'<circle cx="626" cy="226" r="2.8" fill="{PLAN_CORE}" stroke="{PLAN}" stroke-width="1.0"/>')
        # Delicate blueprint corner reticle around Michael's eye-line
        pl.append(
            f'<path d="M674,162 L666,162 L666,170 M750,162 L758,162 L758,170 '
            f'M674,196 L666,196 L666,188 M750,196 L758,196 L758,188" '
            f'fill="none" stroke="{PLAN}" stroke-width="1.1" opacity="0.70"/>'
        )
        # Monospace Plan Vision origin tag
        pl.append(f'<rect x="478" y="214" width="138" height="22" rx="3" fill="#09131E" opacity="0.84" stroke="{PLAN}" stroke-width="1.0"/>')
        pl.append(
            f'<text x="486" y="229" font-family="DejaVu Sans Mono, monospace" font-size="9.6" '
            f'font-weight="bold" fill="{PLAN_CORE}" letter-spacing="0.8">PLAN SPARK · FOR YOU</text>'
        )
        pl.append('</g>')
        parts.append("".join(pl))

    # -------------------------------------------------------------------------
    # LAYER 5: ONPLAN (Warm volumetric desk lamp cone, floating dust motes,
    # cold rain rim light & cinematic vignette)
    # -------------------------------------------------------------------------
    if _katman_aktif(katmanlar, "onplan"):
        op: list[str] = ['<g id="s202-onplan">']
        # Soft warm volumetric lamp cone spilling organically over letter & $90,000 loan document
        op.append(f'<ellipse cx="325" cy="390" rx="280" ry="185" fill="url(#{p}_lamp_pool)" opacity="0.44"/>')
        # Floating golden dust motes caught in the warm desk lamp beam
        for _ in range(30):
            dx = rng.uniform(130, 620)
            dy = rng.uniform(230, 510)
            dr = rng.uniform(0.8, 2.0)
            op.append(f'<circle cx="{dx:.1f}" cy="{dy:.1f}" r="{dr:.1f}" fill="#FFE9B5" opacity="{rng.uniform(0.22, 0.56):.2f}"/>')
        # Cinematic vignette
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


def _draw_swatches(draw: ImageDraw.ImageDraw, x: int, y: int, colors: list[str], size: int = 20, gap: int = 6) -> None:
    cx = x
    for col in colors:
        draw.rounded_rectangle((cx, y, cx + size, y + size), radius=3, fill=col, outline="#4B6682", width=1)
        cx += size + gap


def uret_kartlar(versiyon: str = "v1") -> tuple[Path, Path]:
    img_201 = _render_scene(set_201_mahkeme, scale=2.0)  # 1920x1080
    img_202 = _render_scene(set_202_mektup, scale=2.0)

    f_title = _load_font(20, bold=True)
    f_sub = _load_font(12, bold=False)
    f_card_t = _load_font(14, bold=True)
    f_card_s = _load_font(11, bold=False)
    f_small = _load_font(10, bold=False)

    # =========================================================================
    # OUTPUT 1: SET PRESENTATION CARD (1280 x 720 — 100% ENGLISH)
    # =========================================================================
    canvas = _draw_card_bg(1280, 720)
    draw = ImageDraw.Draw(canvas)

    draw.text((24, 14), "MICHAEL SCOFIELD  ·  ACT II SCENE SETS (2.01 – 2.02)", fill="#EBF3FA", font=f_title)
    draw.text((24, 39), "STYLE B+A HYBRID (CINEMATIC 2D + CYAN PLAN VISION)  ·  5-LAYER PARALLAX SETS (960×540)",
              fill="#7E97B0", font=f_sub)
    top_swatches = [("#4D2618", "COURT"), ("#CBEFFF", "FLASH"), ("#F2AA49", "LAMP"),
                    ("#B21A20", "STAMP"), ("#7FE6FF", "PLAN")]
    sx_top = 860
    for col, lbl in top_swatches:
        draw.rounded_rectangle((sx_top, 18, sx_top + 14, 32), radius=3, fill=col, outline="#3B536D", width=1)
        draw.text((sx_top + 19, 19), lbl, fill="#9BB2C8", font=f_small)
        sx_top += 80
    draw.line((24, 58, 1256, 58), fill="#213247", width=1)

    # --- TOP WIDE PANEL: 2.01 COURTROOM SENTENCING ---
    _draw_panel_box(draw, (22, 66, 1258, 382))
    t201 = img_201.resize((496, 279), Image.Resampling.LANCZOS)
    canvas.paste(t201, (34, 94), t201)
    draw.rectangle((34, 94, 34 + 496, 94 + 279), outline="#5B3829", width=1)
    draw.text((34, 72), "2.01 · COURTROOM SENTENCING", fill="#F2AE57", font=f_card_t)
    draw.text((274, 75), "Act II · \"GUILTY?\" / \"DEATH SENTENCE\"", fill="#9DB0C4", font=f_card_s)

    rx = 548
    draw.text((rx, 94), "PALETTE (MAHOGANY COURT VS. COLD FLASH)", fill="#F2AE57", font=f_small)
    _draw_swatches(draw, rx, 112, ["#3A1C12", "#8A4C2C", "#19212C", "#CBEFFF", "#A6191E", "#7FE6FF"], size=22, gap=7)
    draw.text((rx, 148), "KEY ELEMENTS (5)", fill="#9BB2C8", font=f_small)
    for k_i, item in enumerate([
        "• Coffered mahogany walls, State Seal & press flashes",
        "• Handcuffed locked Lincoln v1 behind mahogany rail",
        "• Polished wooden gavel strike & GUILTY verdict slip",
        "• Locked Michael v3 in dark suit (cold fury gaze)",
        "• Cold overhead cones + cyan analytical sightline",
    ]):
        draw.text((rx, 166 + k_i * 21), item, fill="#E3ECF5", font=f_card_s)
    draw.text((rx, 282), "LIGHTING & DRAMATIC TENSION", fill="#9BB2C8", font=f_small)
    draw.text((rx, 298), "Harsh institutional blue-white top-light and press flashes\nquarantine Lincoln behind the rail while Michael watches\nin cold, restrained fury from the left foreground.",
              fill="#C8D6E4", font=f_card_s)
    draw.text((rx, 354), "LAYERS: s201-uzak · s201-orta · s201-sahne · s201-plan · s201-onplan",
              fill="#8AA3BC", font=f_small)

    draw.line((894, 94, 894, 368), fill="#233447", width=1)
    tx = 912
    draw.text((tx, 94), "LOCKED ASSETS & CONTINUITY", fill="#7FE6FF", font=f_card_t)
    notes_201 = [
        ("LOCKED CHARACTERS",
         "Imports K.lincoln_kafa('3q','yas') v1\nand K.michael_kafa('3q','ofke') v3\nread-only from karakter.py."),
        ("R1 & R3 COMPLIANCE",
         "Original archetype faces only (R1).\nLincoln's handcuffed wrists & forearms\nremain strictly tattoo-free (R3)."),
        ("ENGLISH DIEGETIC PROPS",
         "GUILTY · DEATH PENALTY verdict slip,\nSTATE v. BURROWS folder, Cook County\nCircuit Court seal — 100% English."),
    ]
    ny = 122
    for heading, body_txt in notes_201:
        draw.text((tx, ny), heading, fill="#F6C367" if "LOCKED" in heading else "#9EC5DE", font=f_small)
        draw.text((tx, ny + 16), body_txt, fill="#C5D5E4", font=f_card_s)
        ny += 82

    # --- BOTTOM WIDE PANEL: 2.02 APARTMENT TRUTH LETTER ---
    _draw_panel_box(draw, (22, 392, 1258, 708))
    t202 = img_202.resize((496, 279), Image.Resampling.LANCZOS)
    canvas.paste(t202, (34, 420), t202)
    draw.rectangle((34, 420, 34 + 496, 420 + 279), outline="#3D5970", width=1)
    draw.text((34, 398), "2.02 · APARTMENT TRUTH LETTER", fill="#7FE6FF", font=f_card_t)
    draw.text((274, 401), "Act II · \"$90,000 LOAN\" / \"FOR YOU\"", fill="#9DB0C4", font=f_card_s)

    draw.text((rx, 420), "PALETTE (RAINY MIDNIGHT VS. WARM LAMP + SPARK)", fill="#7FE6FF", font=f_small)
    _draw_swatches(draw, rx, 438, ["#0B1524", "#1B3E2D", "#6E4224", "#FFE8A8", "#B21A20", "#7FE6FF"], size=22, gap=7)
    draw.text((rx, 474), "KEY ELEMENTS (5)", fill="#9BB2C8", font=f_small)
    for k_i, item in enumerate([
        "• Rain-streaked midnight window & Chicago skyline",
        "• Vintage brass & emerald banker's desk lamp glow",
        "• Opened handwritten letter ('He did it FOR YOU')",
        "• Red-stamped '$90,000 LOAN · FOR MICHAEL'S TUITION'",
        "• Locked Michael v3 (grief + first #7FE6FF eye spark)",
    ]):
        draw.text((rx, 492 + k_i * 21), item, fill="#E3ECF5", font=f_card_s)
    draw.text((rx, 608), "THE BIRTH OF PLAN VISION", fill="#9BB2C8", font=f_small)
    draw.text((rx, 624), "Warm desk-lamp amber illuminates Lincoln's hidden sacrifice\nwhile the very first #7FE6FF cyan spark ignites inside\nMichael's grieving eyes — turning guilt into the Plan.",
              fill="#D4C2AB", font=f_card_s)
    draw.text((rx, 680), "LAYERS: s202-uzak · s202-orta · s202-sahne · s202-plan · s202-onplan",
              fill="#8AA3BC", font=f_small)

    draw.line((894, 420, 894, 694), fill="#233447", width=1)
    draw.text((tx, 420), "STORY ARC & VISUAL DETAILS", fill="#7FE6FF", font=f_card_t)
    notes_202 = [
        ("PRE-TATTOO CONTINUITY",
         "Michael's hands & forearms on the desk\nare still clean here — right before\nthe blueprint tattoo is conceived."),
        ("ARCHITECTURAL FORESHADOW",
         "Framed structural bridge truss blueprint\non the wall & drafting pencil on desk\nground Michael's engineering mind."),
        ("WARM / COLD / CYAN TRIAD",
         "Cold midnight rain, warm banker's lamp,\nand the razor-sharp #7FE6FF cyan eye\nspark anchor the Style B+A hybrid."),
    ]
    ny = 448
    for heading, body_txt in notes_202:
        draw.text((tx, ny), heading, fill="#F6C367" if "CONTINUITY" in heading else "#9EC5DE", font=f_small)
        draw.text((tx, ny + 16), body_txt, fill="#C5D5E4", font=f_card_s)
        ny += 82

    out_main = OUT_DIR / f"b2_set_mahkeme_{versiyon}.png"
    canvas.convert("RGB").save(out_main, quality=95)

    # =========================================================================
    # OUTPUT 2: R13 200% CROP QUALITY AUDIT CARD (1280 x 720 — 4 PANELS)
    # =========================================================================
    r13 = _draw_card_bg(1280, 720)
    d13 = ImageDraw.Draw(r13)
    d13.text((24, 13), "R13 · 200% ZOOM QUALITY AUDIT (ACT II: 2.01 – 2.02 SETS)", fill="#EBF3FA", font=f_title)
    d13.text((24, 37), "1:1 PIXEL CROPS FROM 1920×1080 RENDERS  ·  MICHAEL V3, HANDCUFFED LINCOLN V1, GAVEL, $90K STAMP & CYAN SPARK",
             fill="#7E97B0", font=f_sub)
    d13.line((24, 55, 1256, 55), fill="#213247", width=1)

    cw, ch = 600, 264
    crops = [
        (img_201, (336, 510), "1 · 2.01 MICHAEL V3 COLLAR-OVER-NECK & LEAN SUIT (200%)",
         "Locked F3 ~2.2x shoulders, neck seated inside collar, tailored lapels", (22, 66)),
        (img_201, None, "2 · 2.01 LINCOLN V1 COLLAR-OVER-NECK + GAVEL & GUILTY (200%)",
         "Split 1:1 crop: Lincoln v1 ~2.4x shoulders/collar (L) & gavel strike (R)", (652, 66)),
        (img_202, (1440, 480), "3 · 2.02 MICHAEL V3 COLLAR-OVER-NECK + FIRST CYAN SPARK (200%)",
         "Neck seated cleanly inside shirt collar, grief + centered #7FE6FF spark", (22, 392)),
        (img_202, (1460, 770), "4 · 2.02 CONTINUOUS SHOULDER -> ELBOW -> HAND & $90K DOC (200%)",
         "Unbroken right arm from shoulder across desk edge to $90,000 LOAN doc", (652, 392)),
    ]

    for src_img, center, title, sub, (bx, by) in crops:
        _draw_panel_box(d13, (bx, by, bx + 606, by + 314))
        if center is None:
            # Split 1:1 200% crop: Left 280px Lincoln v1 head+collar+shoulders, Right 316px Gavel + GUILTY slip
            lw_s, rw_s = 280, cw - 284
            lx0 = max(0, min(src_img.width - lw_s, 1448 - lw_s // 2))
            ly0 = max(0, min(src_img.height - ch, 450 - ch // 2))
            p_left = src_img.crop((lx0, ly0, lx0 + lw_s, ly0 + ch))

            rx0 = max(0, min(src_img.width - rw_s, 1020 - rw_s // 2))
            ry0 = max(0, min(src_img.height - ch, 908 - ch // 2))
            p_right = src_img.crop((rx0, ry0, rx0 + rw_s, ry0 + ch))

            r13.paste(p_left, (bx + 3, by + 44), p_left)
            r13.paste(p_right, (bx + 3 + lw_s + 4, by + 44), p_right)
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

    out_r13 = OUT_DIR / "b2_set_mahkeme_r13.png"
    r13.convert("RGB").save(out_r13, quality=95)
    print(f"Saved:\n  - {out_main}\n  - {out_r13}")
    return out_main, out_r13


if __name__ == "__main__":
    uret_kartlar("v1")
