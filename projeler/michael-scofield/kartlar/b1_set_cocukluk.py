"""V1 (Chapter I Childhood & Lock Scenes Visual Artist) — Style B + A Hybrid.

Isolated module producing 3 high-detail 5-layer (960x540) cinematic 2D SVG sets:
  - set_101_kapi(katmanlar=None, plan_gorusu=True)          -> (defs_svg, body_svg)
  - set_102_mutfak(katmanlar=None, plan_gorusu=True)        -> (defs_svg, body_svg)
  - set_103_islahevi_kilit(katmanlar=None, plan_gorusu=True)-> (defs_svg, body_svg)

All on-screen text is in English. Every stroked <path> explicitly sets fill="none".
"""
from __future__ import annotations

import io
import math
import random
from pathlib import Path
import resvg_py
from PIL import Image, ImageDraw, ImageFont

OUT_DIR = Path(__file__).resolve().parent
W_SCENE, H_SCENE = 960, 540

# Style B + A Hybrid Constants
INK = "#12171E"
INK_WARM = "#1B130E"
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
# 1.01 — FAMILY FRONT DOOR (BURROWS -> SCOFIELD)
# =============================================================================
def set_101_kapi(katmanlar: set[str] | list[str] | None = None,
                 plan_gorusu: bool = True) -> tuple[str, str]:
    """1980s suburban entryway: carved oak door, rainy night streetlamp,
    departing father's long-coat shadow, warm foyer, brass SCOFIELD nameplate."""
    rng = random.Random(1011)
    p = _uid("kapi")

    defs = f"""
    <linearGradient id="{p}_night_sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#060D19"/>
      <stop offset="52%" stop-color="#0E1D33"/>
      <stop offset="100%" stop-color="#192D46"/>
    </linearGradient>
    <radialGradient id="{p}_lamp_halo" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0%" stop-color="#FFF5D6" stop-opacity="0.95"/>
      <stop offset="22%" stop-color="#FFD07B" stop-opacity="0.55"/>
      <stop offset="58%" stop-color="#5E8DB8" stop-opacity="0.22"/>
      <stop offset="100%" stop-color="#0E1D33" stop-opacity="0.0"/>
    </radialGradient>
    <linearGradient id="{p}_foyer_wall" x1="0" y1="0" x2="1" y2="0.6">
      <stop offset="0%" stop-color="#221914"/>
      <stop offset="48%" stop-color="#3D2B1F"/>
      <stop offset="100%" stop-color="#241913"/>
    </linearGradient>
    <linearGradient id="{p}_foyer_glow" x1="0.82" y1="0.18" x2="0.25" y2="0.88">
      <stop offset="0%" stop-color="#FFCA75" stop-opacity="0.46"/>
      <stop offset="45%" stop-color="#D98B38" stop-opacity="0.18"/>
      <stop offset="100%" stop-color="#2B1C12" stop-opacity="0.0"/>
    </linearGradient>
    <linearGradient id="{p}_wainscot" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#4A3222"/>
      <stop offset="50%" stop-color="#362317"/>
      <stop offset="100%" stop-color="#22150E"/>
    </linearGradient>
    <linearGradient id="{p}_door_oak" x1="0" y1="0" x2="1" y2="0.15">
      <stop offset="0%" stop-color="#4E311E"/>
      <stop offset="38%" stop-color="#6B442A"/>
      <stop offset="76%" stop-color="#51321E"/>
      <stop offset="100%" stop-color="#321E12"/>
    </linearGradient>
    <linearGradient id="{p}_door_panel" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#3B2315"/>
      <stop offset="55%" stop-color="#593722"/>
      <stop offset="100%" stop-color="#2F1B10"/>
    </linearGradient>
    <linearGradient id="{p}_door_edge" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#6A92B5"/>
      <stop offset="30%" stop-color="#4B3423"/>
      <stop offset="100%" stop-color="#23160E"/>
    </linearGradient>
    <linearGradient id="{p}_glass_frost" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#3B6182" stop-opacity="0.82"/>
      <stop offset="50%" stop-color="#233F5C" stop-opacity="0.72"/>
      <stop offset="100%" stop-color="#132539" stop-opacity="0.88"/>
    </linearGradient>
    <linearGradient id="{p}_brass" x1="0" y1="0" x2="1" y2="0.85">
      <stop offset="0%" stop-color="#8C6324"/>
      <stop offset="22%" stop-color="#E5B95C"/>
      <stop offset="46%" stop-color="#FFF0B2"/>
      <stop offset="68%" stop-color="#D49E3D"/>
      <stop offset="88%" stop-color="#9A6E24"/>
      <stop offset="100%" stop-color="#6B4A16"/>
    </linearGradient>
    <linearGradient id="{p}_brass_bevel" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#FFF4C8"/>
      <stop offset="50%" stop-color="#C69034"/>
      <stop offset="100%" stop-color="#5C3D12"/>
    </linearGradient>
    <linearGradient id="{p}_parquet" x1="0.3" y1="0" x2="0.7" y2="1">
      <stop offset="0%" stop-color="#251913"/>
      <stop offset="35%" stop-color="#3C291D"/>
      <stop offset="72%" stop-color="#2A1C14"/>
      <stop offset="100%" stop-color="#17100C"/>
    </linearGradient>
    <linearGradient id="{p}_wet_reflect" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#76B0D9" stop-opacity="0.42"/>
      <stop offset="55%" stop-color="#456E94" stop-opacity="0.22"/>
      <stop offset="100%" stop-color="#1A2C42" stop-opacity="0.0"/>
    </linearGradient>
    <linearGradient id="{p}_warm_floor" x1="1" y1="0" x2="0.2" y2="1">
      <stop offset="0%" stop-color="#FFCA72" stop-opacity="0.36"/>
      <stop offset="55%" stop-color="#C97D2E" stop-opacity="0.14"/>
      <stop offset="100%" stop-color="#2A1B12" stop-opacity="0.0"/>
    </linearGradient>
    <radialGradient id="{p}_vignette" cx="0.52" cy="0.48" r="0.65">
      <stop offset="56%" stop-color="#000000" stop-opacity="0.0"/>
      <stop offset="100%" stop-color="#05080E" stop-opacity="0.72"/>
    </radialGradient>
    <filter id="{p}_glow_warm" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="5.0" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="{p}_glow_cyan" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="2.5" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    """

    parts: list[str] = []

    # --- LAYER 1: UZAK (Rainy night street, streetlamp halo, departing father silhouette) ---
    if _katman_aktif(katmanlar, "uzak"):
        u: list[str] = ['<g id="kapi-uzak">']
        u.append('<rect x="0" y="0" width="960" height="540" fill="#13100E"/>')
        # Rainy night exterior visible through open doorway (x=175..410, y=54..415)
        u.append(f'<rect x="175" y="54" width="235" height="365" fill="url(#{p}_night_sky)"/>')
        # Distant suburban gable roof silhouettes & bare trees
        u.append('<polygon points="175,265 210,224 252,265 252,328 175,328" fill="#0B1525"/>')
        u.append('<polygon points="262,258 312,216 368,258 368,328 262,328" fill="#0A1322"/>')
        # Tiny warm distant neighbor windows
        u.append('<rect x="206" y="274" width="12" height="16" fill="#C98D3E" opacity="0.55"/>')
        u.append('<rect x="304" y="268" width="14" height="18" fill="#B8823A" opacity="0.42"/>')
        # Bare tree branches against night sky
        u.append('<path d="M188,248 Q206,192 228,158 M206,204 Q226,184 242,172 M355,244 Q336,184 316,142" fill="none" stroke="#08101C" stroke-width="3.0"/>')
        # Streetlamp post & glowing halo
        u.append('<rect x="268" y="138" width="6" height="196" fill="#0E1724"/>')
        u.append('<path d="M271,142 Q276,124 296,126" fill="none" stroke="#0E1724" stroke-width="4.2"/>')
        u.append(f'<ellipse cx="298" cy="134" rx="76" ry="72" fill="url(#{p}_lamp_halo)"/>')
        u.append(f'<ellipse cx="298" cy="134" rx="11" ry="8" fill="#FFF8DC" filter="url(#{p}_glow_warm)"/>')
        # Wet street asphalt & porch steps
        u.append('<rect x="175" y="326" width="235" height="92" fill="#0C1726"/>')
        # Wet streetlamp reflections on asphalt
        for wy, ww, op in [(336, 42, 0.42), (348, 56, 0.34), (362, 70, 0.25), (378, 82, 0.18)]:
            u.append(f'<ellipse cx="298" cy="{wy}" rx="{ww}" ry="3.2" fill="#FFD98B" opacity="{op}"/>')
        # Porch railing & steps
        u.append('<rect x="175" y="378" width="235" height="40" fill="#172434" stroke="#0A111B" stroke-width="1.4"/>')
        u.append('<path d="M175,388 L410,388 M175,402 L410,402" fill="none" stroke="#4D7194" stroke-width="1.0" opacity="0.45"/>')

        # *** FATHER'S DRAMATIC LONG-COAT SILHOUETTE STEPPING INTO THE RAIN ***
        # Backlit rim around coat & briefcase
        u.append('<g id="father-silhouette">')
        # Long cast shadow reaching back across the porch toward the foyer!
        u.append('<polygon points="244,376 286,376 346,435 198,435" fill="#04080F" opacity="0.72"/>')
        # Legs / striding boots
        u.append('<polygon points="246,342 260,342 252,380 238,380" fill="#070D16"/>')
        u.append('<polygon points="268,340 282,340 294,378 278,378" fill="#070D16"/>')
        # Long trench coat body billowing slightly in rain
        u.append('<path d="M242,232 L288,232 L302,350 L232,348 Z" fill="#080F1A" stroke="#04070C" stroke-width="1.4"/>')
        # Turned-up collar & head (back/3-quarter view walking away)
        u.append('<path d="M248,232 L254,218 L278,218 L284,232 Z" fill="#0C1524"/>')
        u.append('<ellipse cx="266" cy="204" rx="12.5" ry="15.5" fill="#09111D"/>')
        # Briefcase in right hand
        u.append('<rect x="294" y="294" width="26" height="19" rx="2" fill="#070D16" stroke="#365370" stroke-width="0.9"/>')
        u.append('<path d="M302,294 L302,289 L312,289 L312,294" fill="none" stroke="#2D4660" stroke-width="1.4"/>')
        # Dramatic cold-gold streetlamp rim-light on coat shoulder & head!
        u.append('<path d="M276,193 Q281,204 277,218 L289,232 L301,342" fill="none" stroke="#BFE2FF" stroke-width="1.8" opacity="0.78"/>')
        u.append('<path d="M266,189 Q276,190 278,200" fill="none" stroke="#FFE9B5" stroke-width="1.5" opacity="0.75"/>')
        u.append('</g>')

        # Diagonal exterior rain streaks
        for _ in range(52):
            rx = rng.uniform(178, 406)
            ry = rng.uniform(58, 392)
            rlen = rng.uniform(14, 34)
            u.append(
                f'<path d="M{rx:.1f},{ry:.1f} L{rx-rlen*0.24:.1f},{ry+rlen:.1f}" '
                f'fill="none" stroke="#9AC7EC" stroke-width="{rng.uniform(0.6,1.2):.1f}" opacity="{rng.uniform(0.18,0.48):.2f}"/>'
            )
        u.append('</g>')
        parts.append("\n".join(u))

    # --- LAYER 2: ORTA (1980s Foyer: wainscoting, wallpaper, family photo, coat rack, parquet floor) ---
    if _katman_aktif(katmanlar, "orta"):
        o: list[str] = ['<g id="kapi-orta">']
        # Left foyer wall (x=0..180) and Right foyer wall (x=408..960)
        o.append(f'<rect x="0" y="0" width="180" height="422" fill="url(#{p}_foyer_wall)"/>')
        o.append(f'<rect x="408" y="0" width="552" height="422" fill="url(#{p}_foyer_wall)"/>')
        # Top lintel wall above doorway
        o.append('<rect x="176" y="0" width="236" height="58" fill="#2A1E17"/>')

        # Subtle 1980s vertical striped wallpaper texture (upper walls, y=0..278)
        for wx in range(10, 174, 18):
            o.append(f'<rect x="{wx}" y="0" width="6" height="278" fill="#4A3527" opacity="0.28"/>')
        for wx in range(420, 956, 20):
            o.append(f'<rect x="{wx}" y="0" width="7" height="278" fill="#4E3829" opacity="0.26"/>')

        # Lower wood wainscoting + chair rail (y=278..420)
        o.append(f'<rect x="0" y="278" width="176" height="144" fill="url(#{p}_wainscot)" stroke="{INK_WARM}" stroke-width="1.4"/>')
        o.append(f'<rect x="412" y="278" width="548" height="144" fill="url(#{p}_wainscot)" stroke="{INK_WARM}" stroke-width="1.4"/>')
        # Chair rail molding
        o.append('<rect x="0" y="274" width="176" height="8" fill="#5A3D29" stroke="#1E130C" stroke-width="1.2"/>')
        o.append('<rect x="412" y="274" width="548" height="8" fill="#5A3D29" stroke="#1E130C" stroke-width="1.2"/>')
        # Wainscoting recessed panels
        for px in (18, 96):
            o.append(f'<rect x="{px}" y="294" width="62" height="106" fill="#2B1C13" stroke="#533724" stroke-width="1.2"/>')
        for px in (698, 784, 870):
            o.append(f'<rect x="{px}" y="294" width="68" height="106" fill="#2B1C13" stroke="#533724" stroke-width="1.2"/>')

        # Warm foyer glow wash over right wall
        o.append(f'<rect x="412" y="0" width="548" height="422" fill="url(#{p}_foyer_glow)"/>')

        # *** RIGHT WALL: FRAMED FAMILY PHOTOGRAPH (slightly tilted) & BRASS SCONCE ***
        # Warm brass wall sconce (x=882, y=132)
        o.append(f'<ellipse cx="882" cy="136" rx="95" ry="95" fill="url(#{p}_lamp_halo)" opacity="0.48"/>')
        o.append('<rect x="875" y="138" width="14" height="28" rx="3" fill="#B88838" stroke="#1E140B" stroke-width="1.2"/>')
        o.append('<polygon points="866,112 898,112 892,140 872,140" fill="#FFE7A8" stroke="#7A551D" stroke-width="1.3"/>')
        o.append('<ellipse cx="882" cy="124" rx="8" ry="10" fill="#FFFDF0" opacity="0.88"/>')

        # Framed family photo (x=724..832, y=118..220)
        o.append('<g transform="rotate(-1.8 778 169)">')
        o.append('<rect x="728" y="122" width="108" height="100" rx="2" fill="#0B0705" opacity="0.52"/>')
        o.append(f'<rect x="722" y="116" width="108" height="100" rx="2" fill="#5A3A23" stroke="{INK_WARM}" stroke-width="2.0"/>')
        o.append('<rect x="731" y="125" width="90" height="82" fill="#D8C8AE" stroke="#362214" stroke-width="1.2"/>')
        # Sepia family photo content (mother + 2 boys silhouettes)
        o.append('<rect x="737" y="131" width="78" height="70" fill="#6E5B48"/>')
        o.append('<ellipse cx="776" cy="154" rx="9" ry="11" fill="#3B2E24"/>')  # mother head
        o.append('<path d="M758,201 Q762,172 776,170 Q790,172 794,201 Z" fill="#32261E"/>')
        o.append('<ellipse cx="754" cy="166" rx="7" ry="8.5" fill="#2E231B"/>')  # older boy
        o.append('<path d="M742,201 Q746,179 754,178 Q762,179 765,201 Z" fill="#281E17"/>')
        o.append('<ellipse cx="797" cy="171" rx="6.5" ry="7.8" fill="#2E231B"/>')  # young Michael
        o.append('<path d="M787,201 Q790,183 797,182 Q804,183 807,201 Z" fill="#261D16"/>')
        # Glass diagonal glare
        o.append('<polygon points="737,131 768,131 737,168" fill="#FFF4D6" opacity="0.16"/>')
        o.append('</g>')

        # Right side small entryway console table (x=742..938, y=312..424)
        o.append('<polygon points="748,418 938,418 952,438 732,438" fill="#0B0705" opacity="0.65"/>')
        o.append(f'<rect x="742" y="312" width="194" height="14" rx="2" fill="#593822" stroke="{INK_WARM}" stroke-width="1.5"/>')
        o.append(f'<rect x="752" y="326" width="174" height="24" fill="#3F2718" stroke="{INK_WARM}" stroke-width="1.4"/>')
        o.append('<circle cx="839" cy="338" r="3.5" fill="#D4A042" stroke="#1F150B" stroke-width="1.0"/>')
        o.append(f'<rect x="756" y="350" width="10" height="72" fill="#3A2416" stroke="{INK_WARM}" stroke-width="1.3"/>')
        o.append(f'<rect x="912" y="350" width="10" height="72" fill="#3A2416" stroke="{INK_WARM}" stroke-width="1.3"/>')
        # Mail envelopes & brass key dish on console
        o.append('<polygon points="774,306 814,303 822,312 780,312" fill="#E8DCC4" stroke="#4F4030" stroke-width="1.0"/>')
        o.append('<ellipse cx="868" cy="310" rx="18" ry="4.5" fill="#B58332" stroke="#2D1E0B" stroke-width="1.1"/>')

        # *** LEFT SIDE: COAT RACK & UMBRELLA STAND (x=18..155) ***
        # Wooden coat rack pole & hooks
        o.append(f'<rect x="76" y="96" width="12" height="328" fill="#3C2618" stroke="{INK_WARM}" stroke-width="1.6"/>')
        o.append('<path d="M52,424 L82,398 L112,424" fill="none" stroke="#3C2618" stroke-width="8" stroke-linecap="round"/>')
        o.append('<path d="M82,118 Q62,112 56,126 M82,126 Q104,118 112,132" fill="none" stroke="#9C7434" stroke-width="3.2" stroke-linecap="round"/>')
        # Hanging navy rain jacket on coat rack
        o.append(f'<path d="M56,126 Q38,144 30,248 L66,262 L76,222 L74,132 Z" fill="#1C2A3B" stroke="{INK}" stroke-width="1.5"/>')
        o.append('<path d="M44,158 Q40,204 42,248 M58,154 Q56,204 54,254" fill="none" stroke="#101924" stroke-width="1.3" opacity="0.7"/>')
        # Umbrella stand + dark folded umbrella
        o.append(f'<polygon points="104,332 146,332 140,424 110,424" fill="#462F1E" stroke="{INK_WARM}" stroke-width="1.5"/>')
        o.append('<rect x="102" y="330" width="46" height="7" rx="2" fill="#B58435" stroke="#25180B" stroke-width="1.2"/>')
        o.append('<path d="M126,332 L134,264 Q136,248 148,252 Q154,256 150,264" fill="none" stroke="#6E4A24" stroke-width="4.2" stroke-linecap="round"/>')
        o.append('<polygon points="118,332 132,272 138,274 134,332" fill="#18222E" stroke="#0C1118" stroke-width="1.2"/>')

        # *** HARDWOOD PARQUET FLOOR (y=418..540) ***
        o.append(f'<polygon points="0,418 960,418 960,540 0,540" fill="url(#{p}_parquet)"/>')
        # Perspective parquet floor planks
        for fx in range(-140, 1140, 58):
            top_x = 390 + (fx - 390) * 0.56
            o.append(f'<path d="M{top_x:.1f},418 L{fx:.1f},540" fill="none" stroke="#140D09" stroke-width="1.4" opacity="0.78"/>')
            o.append(f'<path d="M{top_x+2:.1f},418 L{fx+2:.1f},540" fill="none" stroke="#5A3E2B" stroke-width="0.7" opacity="0.32"/>')
        for fy in (440, 468, 502):
            o.append(f'<path d="M0,{fy} L960,{fy}" fill="none" stroke="#160E0A" stroke-width="1.0" opacity="0.52"/>')
        # Cold wet-night reflection spilling onto floor from open door
        o.append(f'<polygon points="175,418 408,418 358,540 96,540" fill="url(#{p}_wet_reflect)"/>')
        # Warm foyer light pool on right floor
        o.append(f'<polygon points="480,418 960,418 960,540 380,540" fill="url(#{p}_warm_floor)"/>')
        # Entryway woven doormat
        o.append('<polygon points="196,432 396,432 374,486 164,486" fill="#3B2B1E" stroke="#1B120C" stroke-width="1.5"/>')
        o.append('<polygon points="204,438 388,438 370,480 174,480" fill="none" stroke="#6E5238" stroke-width="1.2" stroke-dasharray="4,3"/>')

        # Heavy wooden door jamb & molding frame around doorway
        o.append(f'<rect x="164" y="42" width="16" height="380" fill="#4C3220" stroke="{INK_WARM}" stroke-width="1.6"/>')
        o.append(f'<rect x="164" y="42" width="256" height="16" fill="#523623" stroke="{INK_WARM}" stroke-width="1.6"/>')
        o.append(f'<rect x="404" y="42" width="16" height="380" fill="#3E281A" stroke="{INK_WARM}" stroke-width="1.6"/>')
        # Threshold brass weatherstrip
        o.append('<rect x="176" y="415" width="232" height="6" fill="#A67C37" stroke="#261A0D" stroke-width="1.0"/>')

        o.append('</g>')
        parts.append("\n".join(o))

    # --- LAYER 3: SAHNE (Carved Oak Front Door + HERO Brass SCOFIELD Nameplate) ---
    if _katman_aktif(katmanlar, "sahne"):
        s: list[str] = ['<g id="kapi-sahne">']
        # Door swung inward to the right-center (x=392..674, y=48..452)
        # Floor contact shadow under open door (R9)
        s.append('<polygon points="392,420 676,450 658,476 384,434" fill="#070504" opacity="0.78"/>')
        # Beveled door thickness edge catching cool blue night light
        s.append(f'<polygon points="392,54 410,50 410,432 392,422" fill="url(#{p}_door_edge)" stroke="{INK_WARM}" stroke-width="1.6"/>')
        s.append('<path d="M394,56 L394,420" fill="none" stroke="#9AC8ED" stroke-width="1.4" opacity="0.65"/>')

        # Main carved wooden door face
        s.append(f'<polygon points="410,50 672,26 672,456 410,432" fill="url(#{p}_door_oak)" stroke="{INK_WARM}" stroke-width="2.2"/>')

        # Wood grain vertical fibers across door stiles + subtle wood knots
        for gx in range(420, 666, 16):
            t = (gx - 410) / 262.0
            y_top = 50 - t * 24
            y_bot = 432 + t * 24
            s.append(
                f'<path d="M{gx},{y_top+6:.1f} Q{gx+rng.uniform(-3,3):.1f},{(y_top+y_bot)/2:.1f} {gx+rng.uniform(-2,2):.1f},{y_bot-6:.1f}" '
                f'fill="none" stroke="#2D1B10" stroke-width="0.9" opacity="0.45"/>'
            )
        for kx_d, ky_d in [(434, 146), (648, 224), (538, 342)]:
            s.append(f'<ellipse cx="{kx_d}" cy="{ky_d}" rx="3.0" ry="7.2" fill="#2A190E" stroke="#6E462B" stroke-width="0.7" opacity="0.58"/>')

        # Upper frosted glass decorative window pane (2x2 mullions)
        s.append('<polygon points="444,76 636,60 636,164 444,174" fill="#2A190F" stroke="#180E08" stroke-width="1.8"/>')
        s.append(f'<polygon points="452,82 628,68 628,158 452,167" fill="url(#{p}_glass_frost)" stroke="#1E130B" stroke-width="1.3"/>')
        # Window mullions
        s.append('<path d="M540,74 L540,162 M452,124 L628,113" fill="none" stroke="#4D301D" stroke-width="6.5"/>')
        s.append('<path d="M540,74 L540,162 M452,124 L628,113" fill="none" stroke="#1C1009" stroke-width="1.4"/>')
        # Glass specular streaks & raindrop glints
        s.append('<path d="M464,154 L516,84 M556,148 L602,82" fill="none" stroke="#B6DCFA" stroke-width="2.2" opacity="0.24"/>')
        for _ in range(14):
            dx = rng.uniform(458, 622)
            dy = rng.uniform(76, 156)
            s.append(f'<circle cx="{dx:.1f}" cy="{dy:.1f}" r="{rng.uniform(1.1,2.2):.1f}" fill="#CBE6FF" opacity="0.45"/>')

        # Carved lower recessed wood panels (2 side-by-side beveled panels)
        # Left lower panel
        s.append(f'<polygon points="444,274 528,274 528,408 444,402" fill="url(#{p}_door_panel)" stroke="{INK_WARM}" stroke-width="1.7"/>')
        s.append('<polygon points="454,284 518,284 518,396 454,392" fill="#462B19" stroke="#754D31" stroke-width="1.2"/>')
        # Right lower panel
        s.append(f'<polygon points="548,274 636,274 636,416 548,410" fill="url(#{p}_door_panel)" stroke="{INK_WARM}" stroke-width="1.7"/>')
        s.append('<polygon points="558,284 626,284 626,404 558,399" fill="#462B19" stroke="#754D31" stroke-width="1.2"/>')
        # Panel bevel highlights catching warm foyer light
        s.append('<path d="M454,284 L518,284 L518,396 M558,284 L626,284 L626,404" fill="none" stroke="#9B6A42" stroke-width="1.1" opacity="0.58"/>')

        # Heavy brass hinges on right door edge
        for hy in (96, 368):
            s.append(f'<rect x="662" y="{hy}" width="16" height="44" rx="2" fill="url(#{p}_brass)" stroke="{INK_WARM}" stroke-width="1.4"/>')
            s.append(f'<circle cx="670" cy="{hy+10}" r="2.2" fill="#4A3210"/>')
            s.append(f'<circle cx="670" cy="{hy+34}" r="2.2" fill="#4A3210"/>')

        # Antique brass mortise lockset & doorknob (left edge of door)
        s.append(f'<rect x="414" y="252" width="22" height="72" rx="3" fill="url(#{p}_brass)" stroke="{INK_WARM}" stroke-width="1.4"/>')
        s.append('<circle cx="425" cy="268" r="5.5" fill="#7D581F" stroke="#241708" stroke-width="1.1"/>')  # deadbolt
        s.append('<path d="M425,264 L425,272" fill="none" stroke="#1E1308" stroke-width="1.8"/>')
        # Round brass doorknob with specular highlight
        s.append(f'<circle cx="425" cy="298" r="11.5" fill="url(#{p}_brass)" stroke="{INK_WARM}" stroke-width="1.5"/>')
        s.append('<ellipse cx="422" cy="294" rx="4.2" ry="3.0" fill="#FFF7D4" opacity="0.82"/>')

        # *** HERO FOCAL DETAIL: TEXTURED BRASS NAMEPLATE (BURROWS -> SCOFIELD) ***
        # Drop shadow on carved oak middle rail
        s.append('<rect x="462" y="196" width="164" height="58" rx="4" fill="#180D07" opacity="0.68"/>')
        # Outer beveled brass frame
        s.append(f'<rect x="458" y="191" width="164" height="58" rx="4" fill="url(#{p}_brass_bevel)" stroke="{INK_WARM}" stroke-width="1.8"/>')
        # Inner brushed brass face
        s.append(f'<rect x="464" y="197" width="152" height="46" rx="2.5" fill="url(#{p}_brass)" stroke="#634214" stroke-width="1.1"/>')
        # Fine horizontal brushed-metal texture lines & wear scratches
        for by_l in range(201, 242, 4):
            s.append(f'<path d="M466,{by_l} L614,{by_l}" fill="none" stroke="#FFF6CE" stroke-width="0.45" opacity="0.28"/>')
        s.append('<path d="M482,204 L518,214 M576,232 L606,225" fill="none" stroke="#6E4A18" stroke-width="0.7" opacity="0.42"/>')
        # 4 slotted brass corner screws
        for sx, sy in [(471, 204), (609, 204), (471, 236), (609, 236)]:
            s.append(f'<circle cx="{sx}" cy="{sy}" r="3.4" fill="#B88630" stroke="#36220B" stroke-width="1.0"/>')
            s.append(f'<path d="M{sx-2.2},{sy-1.2} L{sx+2.2},{sy+1.2}" fill="none" stroke="#2D1C09" stroke-width="1.0"/>')
        # Faint ghostly/scratched-out previous engraving "BURROWS" above
        s.append('<text x="540" y="211" text-anchor="middle" fill="#6E4B19" font-family="Georgia,serif" font-size="9.5" letter-spacing="3.5" opacity="0.48">BURROWS</text>')
        s.append('<path d="M500,208 L580,208" fill="none" stroke="#5A3C12" stroke-width="0.9" opacity="0.52"/>')
        # Bold crisp engraved "SCOFIELD"
        s.append('<text x="540" y="232" text-anchor="middle" fill="#2A1A08" font-family="Georgia,serif" font-size="22" font-weight="bold" letter-spacing="2.8">SCOFIELD</text>')
        s.append('<text x="539.3" y="231.2" text-anchor="middle" fill="#FFF2BC" font-family="Georgia,serif" font-size="22" font-weight="bold" letter-spacing="2.8" opacity="0.28">SCOFIELD</text>')
        # Subtle #7FE6FF blueprint edge spark on top-right corner of brass plate!
        s.append(f'<path d="M604,191 L622,191 L622,209" fill="none" stroke="{PLAN}" stroke-width="1.7" filter="url(#{p}_glow_cyan)"/>')
        s.append(f'<circle cx="622" cy="191" r="2.6" fill="{PLAN_CORE}" filter="url(#{p}_glow_cyan)"/>')

        s.append('</g>')
        parts.append("\n".join(s))

    # --- LAYER 4: PLAN GÖRÜŞÜ (#7FE6FF Blueprint Analysis) ---
    if plan_gorusu and _katman_aktif(katmanlar, "plan"):
        pl: list[str] = [f'<g id="kapi-plan" filter="url(#{p}_glow_cyan)" opacity="0.86">']
        # Blueprint bracket around brass SCOFIELD plate (callout placed cleanly below photo)
        pl.append(f'<path d="M452,185 L628,185 L628,255 L452,255 Z" fill="none" stroke="{PLAN}" stroke-width="1.1" stroke-dasharray="6,4" opacity="0.72"/>')
        pl.append(f'<path d="M628,236 L688,236 L688,258 L710,258" fill="none" stroke="{PLAN}" stroke-width="1.1"/>')
        pl.append(f'<circle cx="628" cy="236" r="4.2" fill="none" stroke="{PLAN}" stroke-width="1.2"/>')
        pl.append(f'<circle cx="628" cy="236" r="1.6" fill="{PLAN_CORE}"/>')
        pl.append(f'<text x="716" y="255" fill="{PLAN}" font-family="Consolas,monospace" font-size="10.5" font-weight="bold">01 · SCOFIELD</text>')
        pl.append(f'<text x="716" y="268" fill="{PLAN_CORE}" font-family="Consolas,monospace" font-size="8.5" opacity="0.82">NAMEPLATE REPLACED</text>')
        # Blueprint arc at door threshold opening
        pl.append(f'<path d="M180,420 L392,420" fill="none" stroke="{PLAN}" stroke-width="1.0" stroke-dasharray="4,3" opacity="0.7"/>')
        pl.append(f'<path d="M294,420 Q340,398 392,418" fill="none" stroke="{PLAN}" stroke-width="1.0" opacity="0.62"/>')
        pl.append(f'<circle cx="294" cy="420" r="3.6" fill="none" stroke="{PLAN}" stroke-width="1.2"/>')
        pl.append(f'<text x="206" y="410" fill="{PLAN}" font-family="Consolas,monospace" font-size="9.5" font-weight="bold">02 · THRESHOLD</text>')
        pl.append('</g>')
        parts.append("\n".join(pl))

    # --- LAYER 5: ÖN PLAN (Interior warm dust motes, drifting rain mist, vignette) ---
    if _katman_aktif(katmanlar, "onplan"):
        f: list[str] = ['<g id="kapi-onplan">']
        for _ in range(24):
            dx = rng.uniform(430, 930)
            dy = rng.uniform(55, 480)
            dr = rng.uniform(0.9, 2.2)
            f.append(f'<circle cx="{dx:.1f}" cy="{dy:.1f}" r="{dr:.1f}" fill="#FFE9B5" opacity="{rng.uniform(0.18,0.52):.2f}"/>')
        # Subtle dark foreground edge framing
        f.append('<polygon points="0,0 32,0 16,540 0,540" fill="#080605" opacity="0.62"/>')
        f.append(f'<rect x="0" y="0" width="960" height="540" fill="url(#{p}_vignette)"/>')
        f.append('</g>')
        parts.append("\n".join(f))

    return defs, "\n".join(parts)


# =============================================================================
# 1.02 — RAINY KITCHEN (AGE 11)
# =============================================================================
def set_102_mutfak(katmanlar: set[str] | list[str] | None = None,
                   plan_gorusu: bool = True) -> tuple[str, str]:
    """Warm-to-cold rainy 1980s kitchen: ceramic tile backsplash, wood cabinets,
    gingham curtains, rainy window with two brothers' reflection & cyan '?',
    foreground wooden table with two ceramic mugs, kettle, newspaper, chair."""
    rng = random.Random(1022)
    p = _uid("mutfak")

    defs = f"""
    <linearGradient id="{p}_storm_sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#0A1422"/>
      <stop offset="55%" stop-color="#182C42"/>
      <stop offset="100%" stop-color="#28425C"/>
    </linearGradient>
    <linearGradient id="{p}_wall_warm" x1="0.5" y1="0" x2="0.5" y2="1">
      <stop offset="0%" stop-color="#2D231B"/>
      <stop offset="50%" stop-color="#3E3024"/>
      <stop offset="100%" stop-color="#251D17"/>
    </linearGradient>
    <linearGradient id="{p}_cab_wood" x1="0" y1="0" x2="1" y2="0.2">
      <stop offset="0%" stop-color="#3C2618"/>
      <stop offset="50%" stop-color="#563824"/>
      <stop offset="100%" stop-color="#311E13"/>
    </linearGradient>
    <linearGradient id="{p}_table_top" x1="0.5" y1="0" x2="0.5" y2="1">
      <stop offset="0%" stop-color="#533926"/>
      <stop offset="42%" stop-color="#432C1D"/>
      <stop offset="100%" stop-color="#261810"/>
    </linearGradient>
    <linearGradient id="{p}_window_wash" x1="0.5" y1="0" x2="0.5" y2="1">
      <stop offset="0%" stop-color="#7BB6DC" stop-opacity="0.34"/>
      <stop offset="60%" stop-color="#4A7A9E" stop-opacity="0.14"/>
      <stop offset="100%" stop-color="#1E3447" stop-opacity="0.0"/>
    </linearGradient>
    <radialGradient id="{p}_lamp_warm" cx="0.5" cy="0.05" r="0.65">
      <stop offset="0%" stop-color="#FFD485" stop-opacity="0.45"/>
      <stop offset="45%" stop-color="#C8823B" stop-opacity="0.16"/>
      <stop offset="100%" stop-color="#2A1E15" stop-opacity="0.0"/>
    </radialGradient>
    <linearGradient id="{p}_mug_cold" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#243445"/>
      <stop offset="38%" stop-color="#455F78"/>
      <stop offset="72%" stop-color="#2E4257"/>
      <stop offset="100%" stop-color="#182430"/>
    </linearGradient>
    <linearGradient id="{p}_mug_warm" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#9A8870"/>
      <stop offset="35%" stop-color="#E6D9C3"/>
      <stop offset="72%" stop-color="#BFA98B"/>
      <stop offset="100%" stop-color="#6E5D49"/>
    </linearGradient>
    <linearGradient id="{p}_kettle" x1="0" y1="0" x2="1" y2="0.2">
      <stop offset="0%" stop-color="#2C3A45"/>
      <stop offset="30%" stop-color="#7992A3"/>
      <stop offset="52%" stop-color="#C2D5E0"/>
      <stop offset="78%" stop-color="#4A5D6B"/>
      <stop offset="100%" stop-color="#1F2A33"/>
    </linearGradient>
    <linearGradient id="{p}_curtain" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#5E352B"/>
      <stop offset="45%" stop-color="#8A5242"/>
      <stop offset="100%" stop-color="#4A2920"/>
    </linearGradient>
    <radialGradient id="{p}_vignette" cx="0.5" cy="0.48" r="0.66">
      <stop offset="56%" stop-color="#000000" stop-opacity="0.0"/>
      <stop offset="100%" stop-color="#05080D" stop-opacity="0.72"/>
    </radialGradient>
    <filter id="{p}_glow_cyan" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="2.6" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    """

    parts: list[str] = []

    # --- LAYER 1: UZAK (Stormy rainy night outside the kitchen window) ---
    if _katman_aktif(katmanlar, "uzak"):
        u: list[str] = ['<g id="mutfak-uzak">']
        u.append(f'<rect x="0" y="0" width="960" height="540" fill="url(#{p}_wall_warm)"/>')
        # Window exterior opening (x=256..704, y=44..298)
        u.append(f'<rect x="256" y="44" width="448" height="254" fill="url(#{p}_storm_sky)"/>')
        # Storm clouds
        u.append('<ellipse cx="360" cy="88" rx="110" ry="26" fill="#0E1B2B" opacity="0.65"/>')
        u.append('<ellipse cx="590" cy="78" rx="135" ry="30" fill="#0D1928" opacity="0.62"/>')
        # Dark wind-swept trees & backyard fence silhouette
        u.append('<path d="M256,298 L256,184 Q286,154 318,176 Q344,126 382,162 Q404,190 422,228 L422,298 Z" fill="#0A141F"/>')
        u.append('<path d="M548,298 L556,204 Q588,144 634,154 Q670,132 704,174 L704,298 Z" fill="#09121C"/>')
        # Distant neighbor roofline & warm lit window
        u.append('<polygon points="410,256 472,224 536,256 536,298 410,298" fill="#0E1A28"/>')
        u.append('<rect x="464" y="264" width="16" height="14" fill="#D49A48" opacity="0.58"/>')
        # Backyard picket fence posts
        for fx in range(264, 704, 22):
            u.append(f'<rect x="{fx}" y="274" width="5" height="24" fill="#132233"/>')
        u.append('<path d="M256,282 L704,282" fill="none" stroke="#132233" stroke-width="3.2"/>')
        # Heavy exterior rain streaks
        for _ in range(78):
            rx = rng.uniform(260, 700)
            ry = rng.uniform(48, 286)
            rlen = rng.uniform(16, 36)
            u.append(
                f'<path d="M{rx:.1f},{ry:.1f} L{rx-rlen*0.26:.1f},{ry+rlen:.1f}" '
                f'fill="none" stroke="#8EBCE0" stroke-width="{rng.uniform(0.6,1.25):.1f}" opacity="{rng.uniform(0.18,0.48):.2f}"/>'
            )
        u.append('</g>')
        parts.append("\n".join(u))

    # --- LAYER 2: ORTA (Ceramic tile wall, wood cabinets, hanging skillet/mugs, curtains, glass reflection) ---
    if _katman_aktif(katmanlar, "orta"):
        o: list[str] = ['<g id="mutfak-orta">']
        # Ceramic tile backsplash (y=218..368, skipping window opening x=246..714, y<302!)
        o.append('<rect x="0" y="218" width="246" height="150" fill="#463D34"/>')
        o.append('<rect x="714" y="218" width="246" height="150" fill="#463D34"/>')
        o.append('<rect x="246" y="302" width="468" height="66" fill="#463D34"/>')
        tile_w, tile_h = 32, 24
        for ty in range(218, 368, tile_h):
            for tx in range(0, 960, tile_w):
                if 246 <= tx < 714 and ty < 302:
                    continue  # window area stays completely clear!
                tone = rng.choice(["#595248", "#625A4F", "#514A41", "#686055", "#565047"])
                o.append(f'<rect x="{tx+1}" y="{ty+1}" width="{tile_w-2}" height="{tile_h-2}" fill="{tone}" opacity="0.88"/>')
                o.append(f'<path d="M{tx+2},{ty+2} L{tx+tile_w-2},{ty+2}" fill="none" stroke="#8C8376" stroke-width="0.7" opacity="0.42"/>')
            if ty < 302:
                o.append(f'<path d="M0,{ty} L246,{ty} M714,{ty} L960,{ty}" fill="none" stroke="#26211C" stroke-width="1.2"/>')
            else:
                o.append(f'<path d="M0,{ty} L960,{ty}" fill="none" stroke="#26211C" stroke-width="1.2"/>')
        for tx in range(0, 960, tile_w):
            if 246 < tx < 714:
                o.append(f'<path d="M{tx},302 L{tx},368" fill="none" stroke="#26211C" stroke-width="1.1"/>')
            else:
                o.append(f'<path d="M{tx},218 L{tx},368" fill="none" stroke="#26211C" stroke-width="1.1"/>')

        # Upper wooden cabinets (left: x=0..226, right: x=734..960)
        for cx0, cw in [(0, 224), (736, 224)]:
            o.append(f'<rect x="{cx0}" y="0" width="{cw}" height="216" fill="url(#{p}_cab_wood)" stroke="{INK_WARM}" stroke-width="1.8"/>')
            # Two cabinet doors per side
            dw = (cw - 24) // 2
            for di in range(2):
                dx = cx0 + 8 + di * (dw + 8)
                o.append(f'<rect x="{dx}" y="12" width="{dw}" height="192" fill="#4A301F" stroke="#21140C" stroke-width="1.5"/>')
                o.append(f'<rect x="{dx+10}" y="24" width="{dw-20}" height="168" fill="#3D2618" stroke="#6E4930" stroke-width="1.1"/>')
                # Brass cabinet knob
                kx = dx + dw - 14 if di == 0 else dx + 14
                o.append(f'<circle cx="{kx}" cy="176" r="4.2" fill="#C9963E" stroke="#24160A" stroke-width="1.0"/>')

        # Hanging peg rail with cast-iron skillet & ceramic cups (left backsplash)
        o.append('<rect x="18" y="236" width="196" height="10" rx="2" fill="#4B311F" stroke="#1E120B" stroke-width="1.3"/>')
        # Hanging cast-iron skillet
        o.append('<path d="M58,244 L58,278" fill="none" stroke="#1F242A" stroke-width="5.5" stroke-linecap="round"/>')
        o.append('<circle cx="58" cy="306" r="28" fill="#1D2229" stroke="#0D1014" stroke-width="1.8"/>')
        o.append('<circle cx="58" cy="306" r="21" fill="#2A313B" stroke="#4D5866" stroke-width="1.0"/>')
        o.append('<path d="M44,296 Q58,286 72,296" fill="none" stroke="#768799" stroke-width="1.2" opacity="0.5"/>')
        # Hanging mugs on pegs
        for mx, mcol in [(126, "#7A4638"), (174, "#4A6678")]:
            o.append(f'<circle cx="{mx}" cy="241" r="2.8" fill="#B88738"/>')
            o.append(f'<path d="M{mx},244 Q{mx+8},254 {mx},262" fill="none" stroke="{mcol}" stroke-width="3.0"/>')
            o.append(f'<rect x="{mx-11}" y="256" width="22" height="24" rx="3" fill="{mcol}" stroke="{INK_WARM}" stroke-width="1.3"/>')

        # Right countertop items: spice jars & folded dish towel
        o.append('<rect x="0" y="346" width="960" height="24" fill="#3B2B20" stroke="#1C130D" stroke-width="1.5"/>')
        for jx, jh, jcol in [(768, 34, "#A65336"), (796, 28, "#C99846"), (822, 32, "#5E7855")]:
            o.append(f'<rect x="{jx}" y="{346-jh}" width="20" height="{jh}" rx="3" fill="{jcol}" stroke="{INK_WARM}" stroke-width="1.2" opacity="0.88"/>')
            o.append(f'<rect x="{jx+2}" y="{342-jh}" width="16" height="6" rx="1" fill="#8C6B48" stroke="#24190E" stroke-width="1.0"/>')
        # Dish towel draped on right
        o.append('<polygon points="878,346 932,346 938,408 872,404" fill="#C4B69E" stroke="#362C22" stroke-width="1.4"/>')
        o.append('<path d="M876,368 L934,368 M875,384 L936,384" fill="none" stroke="#8C483A" stroke-width="2.2" opacity="0.72"/>')

        # *** WINDOW GLASS REFLECTION: TWO BROTHERS (AGE 15 & AGE 11) + CYAN '?' ***
        o.append('<g id="window-reflection">')
        # Translucent cool-warm glass reflection tint
        o.append('<rect x="256" y="44" width="448" height="254" fill="#1C354D" opacity="0.22"/>')
        # Older brother (Age 15 Lincoln) — taller, broader shoulders, protective slight lean (left-center of glass)
        o.append('<path d="M362,298 Q364,230 388,214 L436,214 Q462,230 468,298 Z" fill="#9BC4E2" opacity="0.24"/>')
        o.append('<ellipse cx="412" cy="176" rx="23" ry="29" fill="#9BC4E2" opacity="0.26"/>')
        o.append('<path d="M390,164 Q412,144 434,164" fill="none" stroke="#CBE7FF" stroke-width="2.2" opacity="0.32"/>')
        # Younger brother (Age 11 Michael) — smaller, sharp attentive posture, closer to glass (right-center)
        o.append('<path d="M494,298 Q496,246 516,234 L554,234 Q574,246 578,298 Z" fill="#B2D8F2" opacity="0.28"/>')
        o.append('<ellipse cx="535" cy="202" rx="18.5" ry="23.5" fill="#B2D8F2" opacity="0.30"/>')
        # Subtle focused eyes/brow glint in reflection
        o.append('<path d="M524,199 L532,199 M539,199 L547,199" fill="none" stroke="#E0F4FF" stroke-width="1.3" opacity="0.36"/>')
        # Diagonal glass specular reflection bands
        o.append('<polygon points="274,44 334,44 256,164 256,104" fill="#C4E4FA" opacity="0.12"/>')
        o.append('<polygon points="564,44 612,44 472,298 424,298" fill="#C4E4FA" opacity="0.09"/>')
        # Raindrops clinging to windowpane
        for _ in range(28):
            dx = rng.uniform(264, 696)
            dy = rng.uniform(52, 290)
            o.append(f'<circle cx="{dx:.1f}" cy="{dy:.1f}" r="{rng.uniform(1.0,2.3):.1f}" fill="#D6EEFF" opacity="0.44"/>')
        o.append('</g>')

        # Window wooden frame & mullions (2x3 panes)
        o.append(f'<rect x="246" y="34" width="468" height="272" fill="none" stroke="#4D3321" stroke-width="14"/>')
        o.append(f'<rect x="240" y="28" width="480" height="284" fill="none" stroke="{INK_WARM}" stroke-width="2.0"/>')
        o.append('<path d="M480,40 L480,300 M254,170 L706,170" fill="none" stroke="#462E1E" stroke-width="8.5"/>')
        o.append('<path d="M480,40 L480,300 M254,170 L706,170" fill="none" stroke="#1E130B" stroke-width="1.5"/>')
        # Window sill
        o.append(f'<rect x="234" y="302" width="492" height="14" rx="2" fill="#593B26" stroke="{INK_WARM}" stroke-width="1.6"/>')

        # *** GINGHAM / CHECKERED CURTAINS (Pötikare) ***
        # Curtain rod
        o.append('<rect x="224" y="22" width="512" height="6" rx="3" fill="#2A1D14" stroke="#0E0906" stroke-width="1.2"/>')
        # Left & right draped curtain panels + top valance
        o.append(f'<path d="M236,28 L334,28 Q312,135 282,216 L296,298 L232,298 Z" fill="url(#{p}_curtain)" stroke="{INK_WARM}" stroke-width="1.6"/>')
        o.append(f'<path d="M724,28 L626,28 Q648,135 678,216 L664,298 L728,298 Z" fill="url(#{p}_curtain)" stroke="{INK_WARM}" stroke-width="1.6"/>')
        o.append(f'<path d="M232,28 L728,28 L724,70 Q640,56 560,72 Q480,56 400,72 Q320,56 236,70 Z" fill="url(#{p}_curtain)" stroke="{INK_WARM}" stroke-width="1.6"/>')
        # Checkered gingham weave lines on curtains
        for gx in range(242, 326, 14):
            o.append(f'<path d="M{gx},30 L{gx-6},296" fill="none" stroke="#D8C4AE" stroke-width="1.5" opacity="0.28"/>')
        for gx in range(636, 722, 14):
            o.append(f'<path d="M{gx},30 L{gx+6},296" fill="none" stroke="#D8C4AE" stroke-width="1.5" opacity="0.28"/>')
        for gy in range(42, 290, 16):
            o.append(f'<path d="M236,{gy} L316,{gy}" fill="none" stroke="#D8C4AE" stroke-width="1.4" opacity="0.26"/>')
            o.append(f'<path d="M644,{gy} L724,{gy}" fill="none" stroke="#D8C4AE" stroke-width="1.4" opacity="0.26"/>')

        # Ambient warm-to-cold light washes
        o.append(f'<rect x="0" y="0" width="960" height="368" fill="url(#{p}_lamp_warm)"/>')
        o.append(f'<polygon points="256,306 704,306 820,540 140,540" fill="url(#{p}_window_wash)"/>')

        o.append('</g>')
        parts.append("\n".join(o))

    # --- LAYER 3: SAHNE (Wooden kitchen table, 2 ceramic mugs, kettle, newspaper, chair back) ---
    if _katman_aktif(katmanlar, "sahne"):
        s: list[str] = ['<g id="mutfak-sahne">']
        # Foreground oak kitchen table (y=366..540)
        s.append(f'<polygon points="0,382 140,362 820,362 960,382 960,540 0,540" fill="url(#{p}_table_top)" stroke="{INK_WARM}" stroke-width="2.0"/>')
        # Table plank perspective seams & wood grain
        for tx in (210, 360, 510, 660, 800):
            top_x = 480 + (tx - 480) * 0.72
            s.append(f'<path d="M{top_x:.1f},362 L{tx:.1f},540" fill="none" stroke="#22140C" stroke-width="1.2" opacity="0.58"/>')
        for gy in (392, 428, 468, 512):
            s.append(f'<path d="M40,{gy} Q480,{gy-4} 920,{gy}" fill="none" stroke="#6B4A32" stroke-width="0.9" opacity="0.26"/>')
        # Cool rainy window reflection across middle of tabletop
        s.append(f'<polygon points="270,364 690,364 756,540 204,540" fill="url(#{p}_window_wash)" opacity="0.85"/>')

        # === 1) FOLDED 1980s NEWSPAPER (Left-center on table) ===
        s.append('<polygon points="168,452 332,438 358,504 188,522" fill="#0E0906" opacity="0.52"/>')
        s.append('<polygon points="164,446 326,432 350,496 184,514" fill="#CFC4AE" stroke="#362E24" stroke-width="1.4"/>')
        s.append('<polygon points="172,442 322,429 342,488 190,504" fill="#DDD3BE" stroke="#4F4437" stroke-width="1.1"/>')
        s.append('<text x="248" y="452" text-anchor="middle" fill="#2A241E" font-family="Georgia,serif" font-size="9.5" font-weight="bold" transform="rotate(-5 248 452)">DAILY CHRONICLE</text>')
        for ny in (462, 470, 478, 486):
            s.append(f'<path d="M192,{ny} L262,{ny-6} M272,{ny-7} L326,{ny-11}" fill="none" stroke="#5A5145" stroke-width="1.3" opacity="0.65"/>')

        # === 2) ENAMELED METAL KETTLE (Center-right on table) ===
        # Contact shadow (R9)
        s.append('<ellipse cx="642" cy="442" rx="54" ry="13" fill="#0A0604" opacity="0.68"/>')
        # Kettle spout
        s.append(f'<path d="M598,412 Q574,404 568,378 L582,374 Q588,392 606,396 Z" fill="url(#{p}_kettle)" stroke="{INK}" stroke-width="1.5"/>')
        # Kettle domed body
        s.append(f'<path d="M594,436 Q592,380 642,376 Q692,380 690,436 Z" fill="url(#{p}_kettle)" stroke="{INK}" stroke-width="1.7"/>')
        # Kettle lid & wooden knob
        s.append('<ellipse cx="642" cy="378" rx="28" ry="7" fill="#9BB2C2" stroke="#18222B" stroke-width="1.3"/>')
        s.append('<circle cx="642" cy="369" r="6" fill="#3B2416" stroke="#140C07" stroke-width="1.2"/>')
        # Arched handle
        s.append('<path d="M602,388 Q642,326 682,388" fill="none" stroke="#1A2229" stroke-width="6.5" stroke-linecap="round"/>')
        s.append('<path d="M602,388 Q642,326 682,388" fill="none" stroke="#5C7080" stroke-width="2.0" stroke-linecap="round"/>')
        # Specular highlight on kettle
        s.append('<path d="M624,388 Q620,410 624,430" fill="none" stroke="#EAF6FF" stroke-width="2.4" opacity="0.62"/>')

        # === 3) TWO DETAILED CERAMIC MUGS (Hero foreground table props) ===
        # Left Mug — COLD / UNTOUCHED (dark slate-blue ceramic, no steam)
        s.append('<ellipse cx="424" cy="480" rx="34" ry="9" fill="#090604" opacity="0.72"/>')
        # Handle
        s.append('<path d="M394,432 Q374,434 374,452 Q374,468 394,468" fill="none" stroke="#31465C" stroke-width="6.5" stroke-linecap="round"/>')
        s.append('<path d="M394,432 Q374,434 374,452 Q374,468 394,468" fill="none" stroke="#111922" stroke-width="1.5"/>')
        # Mug cylinder
        s.append(f'<path d="M394,422 L454,422 L451,476 Q424,484 397,476 Z" fill="url(#{p}_mug_cold)" stroke="{INK}" stroke-width="1.7"/>')
        s.append('<ellipse cx="424" cy="422" rx="30" ry="7.5" fill="#5D7B96" stroke="#131C26" stroke-width="1.4"/>')
        s.append('<ellipse cx="424" cy="424" rx="24" ry="5.2" fill="#1D1612"/>')  # cold dark tea/coffee
        s.append('<path d="M408,430 L408,470" fill="none" stroke="#A6CCE8" stroke-width="2.0" opacity="0.48"/>')
        # Subtle cold air ring (steam gone)
        s.append('<path d="M416,406 Q424,400 432,406" fill="none" stroke="#8EBCE0" stroke-width="0.9" stroke-dasharray="3,3" opacity="0.32"/>')

        # Right Mug — FADING WARMTH (cream ceramic with thin dying wisp of steam + teaspoon)
        s.append('<ellipse cx="526" cy="488" rx="35" ry="9.5" fill="#090604" opacity="0.72"/>')
        # Teaspoon resting beside mug
        s.append('<path d="M558,494 L596,488" fill="none" stroke="#8FA3B0" stroke-width="2.4" stroke-linecap="round"/>')
        s.append('<ellipse cx="602" cy="487" rx="9" ry="4" fill="#B6C8D4" stroke="#2D3942" stroke-width="1.0"/>')
        # Handle
        s.append('<path d="M556,438 Q576,440 576,458 Q576,474 556,474" fill="none" stroke="#C4B094" stroke-width="6.5" stroke-linecap="round"/>')
        s.append('<path d="M556,438 Q576,440 576,458 Q576,474 556,474" fill="none" stroke="#261E16" stroke-width="1.5"/>')
        # Mug cylinder
        s.append(f'<path d="M496,428 L556,428 L553,484 Q526,492 499,484 Z" fill="url(#{p}_mug_warm)" stroke="{INK_WARM}" stroke-width="1.7"/>')
        s.append('<ellipse cx="526" cy="428" rx="30" ry="7.5" fill="#EFE4D2" stroke="#3B3025" stroke-width="1.4"/>')
        s.append('<ellipse cx="526" cy="430" rx="24" ry="5.2" fill="#3B2416"/>')
        s.append('<path d="M510,436 L510,478" fill="none" stroke="#FFF9ED" stroke-width="2.2" opacity="0.62"/>')
        # Thin dying wisp of steam rising toward the cold window
        s.append('<path d="M524,422 Q516,400 528,382 Q536,368 524,352" fill="none" stroke="#DCEBF5" stroke-width="1.8" opacity="0.34"/>')
        s.append('<path d="M532,420 Q540,404 532,388" fill="none" stroke="#DCEBF5" stroke-width="1.1" opacity="0.22"/>')

        # === 4) WOODEN SPINDLE-BACK KITCHEN CHAIR (Foreground left) ===
        s.append(f'<path d="M18,540 L48,376 Q86,366 138,378 L112,540" fill="none" stroke="#362216" stroke-width="12" stroke-linejoin="round"/>')
        s.append(f'<path d="M18,540 L48,376 Q86,366 138,378 L112,540" fill="none" stroke="{INK_WARM}" stroke-width="2.0" stroke-linejoin="round"/>')
        for sx_c in (56, 78, 100):
            s.append(f'<path d="M{sx_c},376 L{sx_c-14},540" fill="none" stroke="#472E1E" stroke-width="6.5"/>')
            s.append(f'<path d="M{sx_c},376 L{sx_c-14},540" fill="none" stroke="{INK_WARM}" stroke-width="1.2"/>')
        # Subtle warm rim on chair top rail
        s.append('<path d="M52,374 Q88,366 134,376" fill="none" stroke="#8C6242" stroke-width="1.6" opacity="0.62"/>')

        s.append('</g>')
        parts.append("\n".join(s))

    # --- LAYER 4: PLAN GÖRÜŞÜ (#7FE6FF Blueprint '?' & AGE 11) ---
    if plan_gorusu and _katman_aktif(katmanlar, "plan"):
        pl: list[str] = [f'<g id="mutfak-plan" filter="url(#{p}_glow_cyan)" opacity="0.88">']
        # Crisp cyan '?' mark beside the 11-year-old's reflection in the rainy glass
        pl.append(f'<circle cx="578" cy="186" r="21" fill="none" stroke="{PLAN}" stroke-width="1.2" stroke-dasharray="5,3"/>')
        pl.append(f'<text x="578" y="196" text-anchor="middle" fill="{PLAN_CORE}" font-family="Consolas,monospace" font-size="28" font-weight="bold">?</text>')
        # Blueprint callout line to AGE 11 tag
        pl.append(f'<path d="M599,186 L646,186 L646,154" fill="none" stroke="{PLAN}" stroke-width="1.15"/>')
        pl.append(f'<circle cx="599" cy="186" r="3.2" fill="{PLAN_CORE}"/>')
        pl.append(f'<text x="614" y="146" fill="{PLAN}" font-family="Consolas,monospace" font-size="11" font-weight="bold">AGE 11</text>')
        # Subtle reflection bracket linking both brothers
        pl.append(f'<path d="M366,142 L366,132 L578,132 L578,142" fill="none" stroke="{PLAN}" stroke-width="0.95" opacity="0.65"/>')
        pl.append(f'<text x="472" y="126" text-anchor="middle" fill="{PLAN}" font-family="Consolas,monospace" font-size="9.5">01 · BROTHERS REFLECTION</text>')
        # Cold mug temperature / stillness indicator
        pl.append(f'<path d="M424,400 L424,378 L368,378" fill="none" stroke="{PLAN}" stroke-width="0.95" stroke-dasharray="4,3" opacity="0.7"/>')
        pl.append(f'<text x="292" y="374" fill="{PLAN}" font-family="Consolas,monospace" font-size="9.5">02 · COLD MUG</text>')
        pl.append('</g>')
        parts.append("\n".join(pl))

    # --- LAYER 5: ÖN PLAN (Foreground right chair edge, dust motes, vignette) ---
    if _katman_aktif(katmanlar, "onplan"):
        f: list[str] = ['<g id="mutfak-onplan">']
        for _ in range(22):
            dx = rng.uniform(180, 780)
            dy = rng.uniform(70, 470)
            dr = rng.uniform(0.9, 2.0)
            f.append(f'<circle cx="{dx:.1f}" cy="{dy:.1f}" r="{dr:.1f}" fill="#DCEEFB" opacity="{rng.uniform(0.16,0.45):.2f}"/>')
        # Dark foreground corner silhouette (right chair back edge)
        f.append('<polygon points="882,540 912,418 960,404 960,540" fill="#0B0705" opacity="0.82"/>')
        f.append(f'<rect x="0" y="0" width="960" height="540" fill="url(#{p}_vignette)"/>')
        f.append('</g>')
        parts.append("\n".join(f))

    return defs, "\n".join(parts)


# =============================================================================
# 1.03 — JUVENILE HALL & FOSTER CLOSET LOCK (JUVENILE HALL / LOCKED)
# =============================================================================
def set_103_islahevi_kilit(katmanlar: set[str] | list[str] | None = None,
                           plan_gorusu: bool = True) -> tuple[str, str]:
    """High-detail dramatic split-depth set:
    Left half: Rainy cold Juvenile Hall corridor, wet tile reflections, wire-caged
    fluorescent lamp, peeling paint/brick, heavy riveted steel bars + 15yo Lincoln rim-lit silhouette.
    Right half (angled foreground): Splintered dark foster closet door, bare bulb on wire,
    rusted strap hinges, HERO heavy forged iron slide bolt & padlock hasp (LOCKED)."""
    rng = random.Random(1033)
    p = _uid("kilit")

    defs = f"""
    <linearGradient id="{p}_jh_wall" x1="0" y1="0" x2="1" y2="0.6">
      <stop offset="0%" stop-color="#142229"/>
      <stop offset="52%" stop-color="#22363E"/>
      <stop offset="100%" stop-color="#111D23"/>
    </linearGradient>
    <linearGradient id="{p}_jh_floor" x1="0.5" y1="0" x2="0.5" y2="1">
      <stop offset="0%" stop-color="#273D45"/>
      <stop offset="48%" stop-color="#19282E"/>
      <stop offset="100%" stop-color="#0D161A"/>
    </linearGradient>
    <linearGradient id="{p}_fluor_cone" x1="0.5" y1="0" x2="0.5" y2="1">
      <stop offset="0%" stop-color="#C8F2EC" stop-opacity="0.55"/>
      <stop offset="35%" stop-color="#76B0B0" stop-opacity="0.22"/>
      <stop offset="100%" stop-color="#1A2E34" stop-opacity="0.0"/>
    </linearGradient>
    <linearGradient id="{p}_bar_steel" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#1B252B"/>
      <stop offset="28%" stop-color="#5A6E78"/>
      <stop offset="52%" stop-color="#8FA6B0"/>
      <stop offset="80%" stop-color="#303E47"/>
      <stop offset="100%" stop-color="#141B20"/>
    </linearGradient>
    <linearGradient id="{p}_closet_wood" x1="0" y1="0" x2="1" y2="0.2">
      <stop offset="0%" stop-color="#1A1512"/>
      <stop offset="35%" stop-color="#2E2017"/>
      <stop offset="72%" stop-color="#3F2B1D"/>
      <stop offset="100%" stop-color="#1F150E"/>
    </linearGradient>
    <radialGradient id="{p}_bulb_glow" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0%" stop-color="#FFF7D6" stop-opacity="0.98"/>
      <stop offset="18%" stop-color="#FFD075" stop-opacity="0.62"/>
      <stop offset="55%" stop-color="#C27428" stop-opacity="0.22"/>
      <stop offset="100%" stop-color="#26160B" stop-opacity="0.0"/>
    </radialGradient>
    <linearGradient id="{p}_iron_plate" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#3E4952"/>
      <stop offset="35%" stop-color="#2A323A"/>
      <stop offset="72%" stop-color="#1D2329"/>
      <stop offset="100%" stop-color="#382B22"/>
    </linearGradient>
    <linearGradient id="{p}_bolt_cyl" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#A8BAC4"/>
      <stop offset="24%" stop-color="#6E7F8A"/>
      <stop offset="62%" stop-color="#2E3840"/>
      <stop offset="88%" stop-color="#4A3E35"/>
      <stop offset="100%" stop-color="#1B2126"/>
    </linearGradient>
    <linearGradient id="{p}_padlock_body" x1="0" y1="0" x2="1" y2="0.8">
      <stop offset="0%" stop-color="#4C5863"/>
      <stop offset="26%" stop-color="#333C45"/>
      <stop offset="68%" stop-color="#22282F"/>
      <stop offset="100%" stop-color="#453325"/>
    </linearGradient>
    <linearGradient id="{p}_shackle" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#4A5A66"/>
      <stop offset="35%" stop-color="#C8DAE6"/>
      <stop offset="65%" stop-color="#6E8290"/>
      <stop offset="100%" stop-color="#2A353D"/>
    </linearGradient>
    <linearGradient id="{p}_rust" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#5E3520"/>
      <stop offset="50%" stop-color="#7D4325"/>
      <stop offset="100%" stop-color="#3A2116"/>
    </linearGradient>
    <radialGradient id="{p}_vignette" cx="0.5" cy="0.5" r="0.68">
      <stop offset="56%" stop-color="#000000" stop-opacity="0.0"/>
      <stop offset="100%" stop-color="#04070B" stop-opacity="0.72"/>
    </radialGradient>
    <filter id="{p}_glow_warm" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="5.5" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="{p}_glow_cyan" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="2.6" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    """

    parts: list[str] = []

    # --- LAYER 1: UZAK (Left Half: Juvenile Hall Corridor, Wet Tile Floor, Peeling Paint/Brick, Caged Lamp) ---
    if _katman_aktif(katmanlar, "uzak"):
        u: list[str] = ['<g id="kilit-uzak">']
        u.append('<rect x="0" y="0" width="960" height="540" fill="#0E171C"/>')

        # Left half institutional corridor perspective (x=0..480)
        u.append(f'<polygon points="0,0 480,0 382,92 98,92" fill="#101B21"/>')  # ceiling
        u.append(f'<rect x="98" y="92" width="284" height="292" fill="url(#{p}_jh_wall)"/>')  # back wall
        u.append(f'<polygon points="0,0 98,92 98,384 0,486" fill="#17272E" stroke="{INK}" stroke-width="1.5"/>')  # left wall
        u.append(f'<polygon points="480,0 382,92 382,384 480,486" fill="#122026"/>')  # right corridor wall
        u.append(f'<polygon points="0,486 98,384 382,384 480,486 480,540 0,540" fill="url(#{p}_jh_floor)"/>')  # floor

        # Exposed brick patches & peeling institutional paint on left & back walls
        u.append('<polygon points="16,138 78,166 74,254 12,240" fill="#3B2B26" opacity="0.62"/>')
        for by_b in range(152, 246, 14):
            u.append(f'<path d="M14,{by_b} L76,{by_b+14}" fill="none" stroke="#1C1412" stroke-width="1.2"/>')
        # Peeling paint curls
        u.append('<path d="M14,142 Q44,148 76,166 Q66,184 74,254" fill="none" stroke="#5E7B82" stroke-width="1.4" opacity="0.58"/>')
        # Back wall concrete block lines & damp stains
        for r_y in range(92, 384, 24):
            u.append(f'<path d="M98,{r_y} L382,{r_y}" fill="none" stroke="#0E181D" stroke-width="1.1" opacity="0.65"/>')
            off = 22 if (r_y // 24) % 2 else 0
            for c_x in range(98 + off, 382, 44):
                u.append(f'<path d="M{c_x},{r_y} L{c_x},{min(384,r_y+24)}" fill="none" stroke="#0E181D" stroke-width="1.0" opacity="0.55"/>')
        # Damp water streaks running down institutional wall
        for wx in (132, 214, 318):
            u.append(f'<path d="M{wx},96 L{wx+2},198 M{wx+6},114 L{wx+4},176" fill="none" stroke="#0D161A" stroke-width="2.2" opacity="0.45"/>')
        # Conduit pipes along upper left wall
        u.append('<path d="M0,48 L98,122 L382,122" fill="none" stroke="#394E57" stroke-width="4.2"/>')
        u.append('<path d="M0,58 L98,132 L382,132" fill="none" stroke="#283840" stroke-width="3.0"/>')
        # Institutional wall stencil: JUVENILE HALL (positioned cleanly above upper bar beam)
        u.append('<rect x="148" y="88" width="184" height="22" fill="#132128" opacity="0.82"/>')
        u.append('<text x="240" y="103" text-anchor="middle" fill="#A2C4CC" font-family="Consolas,monospace" font-size="13" font-weight="bold" letter-spacing="2.0" opacity="0.9">JUVENILE HALL</text>')

        # *** WIRE-CAGED CEILING FLUORESCENT LAMP ***
        u.append('<polygon points="154,38 326,38 334,54 146,54" fill="#23333A" stroke="#0C1317" stroke-width="1.5"/>')
        u.append(f'<rect x="160" y="44" width="160" height="8" rx="3" fill="#E4FAF5" filter="url(#{p}_glow_cyan)"/>')
        # Wire safety cage over fluorescent tube
        u.append('<rect x="152" y="40" width="176" height="18" rx="3" fill="none" stroke="#182329" stroke-width="1.6"/>')
        for cx_w in range(166, 324, 16):
            u.append(f'<path d="M{cx_w},40 L{cx_w},58" fill="none" stroke="#182329" stroke-width="1.2"/>')
        # Cold volumetric light cone spilling down corridor
        u.append(f'<polygon points="148,56 332,56 446,420 34,420" fill="url(#{p}_fluor_cone)"/>')

        # *** WET INSTITUTIONAL TILE FLOOR WITH REFLECTIONS ***
        for fx in range(-40, 520, 52):
            top_x = 240 + (fx - 240) * 0.52
            u.append(f'<path d="M{top_x:.1f},384 L{fx:.1f},540" fill="none" stroke="#0C1418" stroke-width="1.2" opacity="0.72"/>')
        for fy in (406, 434, 468, 508):
            u.append(f'<path d="M0,{fy} L480,{fy}" fill="none" stroke="#0C1418" stroke-width="1.1" opacity="0.65"/>')
        # Wet floor glossy light reflections of the fluorescent lamp & bars
        u.append('<polygon points="172,386 308,386 362,538 118,538" fill="#8CC5C8" opacity="0.16"/>')
        u.append('<ellipse cx="240" cy="444" rx="76" ry="18" fill="#B6E6E2" opacity="0.14"/>')
        u.append('<ellipse cx="222" cy="496" rx="92" ry="16" fill="#9BD1D4" opacity="0.12"/>')

        u.append('</g>')
        parts.append("\n".join(u))

    # --- LAYER 2: ORTA (15-Year-Old Lincoln Rim-Lit Silhouette + Heavy Riveted Steel Bars) ---
    if _katman_aktif(katmanlar, "orta"):
        o: list[str] = ['<g id="kilit-orta">']
        # *** 15-YEAR-OLD LINCOLN SILHOUETTE BEHIND THE BARS (framed cleanly between bars 184 & 254!) ***
        o.append('<g id="lincoln-15-silhouette">')
        # Contact shadow on wet floor
        o.append('<ellipse cx="224" cy="416" rx="54" ry="11" fill="#050A0D" opacity="0.78"/>')
        # Dark institutional cell/shadow behind Lincoln
        o.append('<rect x="128" y="164" width="224" height="226" fill="#0B1318" opacity="0.52"/>')
        # Broad adolescent shoulders, institutional hoodie/jacket
        o.append('<path d="M162,414 L170,282 Q176,252 202,246 L248,246 Q274,252 280,282 L288,414 Z" fill="#0D161C" stroke="#070C10" stroke-width="1.6"/>')
        # Neck & slightly bowed head positioned clearly in gap between steel bars
        o.append('<rect x="213" y="232" width="22" height="18" fill="#0D161C"/>')
        o.append('<ellipse cx="224" cy="210" rx="20.5" ry="26" fill="#0D161C"/>')
        o.append('<path d="M206,202 Q224,180 242,202" fill="#15222B"/>')
        # Right forearm & hand reaching across to grip steel bar at x=324
        o.append('<path d="M268,280 Q294,298 320,296 L322,312 Q290,318 262,298 Z" fill="#121D24"/>')
        # Intense cold cyan-white rim lighting on head, jawline, shoulders & arm
        o.append('<path d="M206,192 Q224,179 242,192" fill="none" stroke="#C8F4F8" stroke-width="2.4" opacity="0.88"/>')
        o.append('<path d="M204,208 Q205,224 214,232 M244,208 Q243,224 234,232" fill="none" stroke="#8ACBD6" stroke-width="1.4" opacity="0.68"/>')
        o.append('<path d="M174,262 Q186,248 208,246 M242,246 Q264,248 276,262" fill="none" stroke="#A6E2EA" stroke-width="2.2" opacity="0.82"/>')
        o.append('<path d="M170,284 L164,380" fill="none" stroke="#76B5C2" stroke-width="1.5" opacity="0.58"/>')
        o.append('</g>')

        # *** HEAVY RIVETED STEEL BARS (Left Half, x=0..465) ***
        # Horizontal riveted cross-beams (top, mid, bottom)
        for hy in (118, 258, 396):
            o.append(f'<rect x="0" y="{hy}" width="472" height="22" fill="#233038" stroke="{INK}" stroke-width="1.8"/>')
            o.append(f'<path d="M0,{hy+2} L472,{hy+2}" fill="none" stroke="#85A0AD" stroke-width="1.3" opacity="0.62"/>')
            # Rivets along cross-beam
            for rx_r in range(28, 460, 54):
                o.append(f'<circle cx="{rx_r}" cy="{hy+11}" r="3.4" fill="#4E626E" stroke="#10171C" stroke-width="1.1"/>')
                o.append(f'<circle cx="{rx_r-1}" cy="{hy+10}" r="1.1" fill="#A6C2CF" opacity="0.72"/>')

        # Heavy vertical steel bars
        bar_xs = [44, 114, 184, 254, 324, 394]
        for bx in bar_xs:
            # Bar cast shadow on wet floor
            o.append(f'<polygon points="{bx},418 {bx+16},418 {bx-28},540 {bx-48},540" fill="#060B0E" opacity="0.45"/>')
            # Steel bar cylinder
            o.append(f'<rect x="{bx}" y="0" width="16" height="540" fill="url(#{p}_bar_steel)" stroke="{INK}" stroke-width="1.7"/>')
            # Specular highlight edge
            o.append(f'<path d="M{bx+6},0 L{bx+6},540" fill="none" stroke="#C4DCE6" stroke-width="1.4" opacity="0.55"/>')
            # Rust streak near cross-beam joints
            o.append(f'<rect x="{bx+1}" y="256" width="14" height="28" fill="#5A331E" opacity="0.28"/>')

        # Lincoln's fingers curled around bar at x=324, y=296..316 (dramatic storytelling touch!)
        for fy_f in (296, 302, 308, 314):
            o.append(f'<rect x="322" y="{fy_f}" width="18" height="5.2" rx="2.4" fill="#18242B" stroke="#7EB8C4" stroke-width="0.9"/>')

        o.append('</g>')
        parts.append("\n".join(o))

    # --- LAYER 3: SAHNE (Right Half Angled Foreground: Foster Closet Door, Bare Bulb, Rusted Hinges, HERO Iron Bolt & Padlock) ---
    if _katman_aktif(katmanlar, "sahne"):
        s: list[str] = ['<g id="kilit-sahne">']

        # Dramatic angled foreground doorframe edge separating Juvenile Hall (left) & Closet Door (right)
        # Drop shadow cast onto left corridor
        s.append('<polygon points="444,0 478,0 462,540 426,540" fill="#05090D" opacity="0.72"/>')
        # Heavy weathered wooden jamb (x=456..518)
        s.append(f'<polygon points="466,0 526,0 512,540 448,540" fill="#2A1D15" stroke="{INK_WARM}" stroke-width="2.2"/>')
        # Cold rim-light from left corridor hitting the left bevel of the closet doorframe!
        s.append('<path d="M466,0 L448,540" fill="none" stroke="#8BC8D6" stroke-width="2.4" opacity="0.65"/>')

        # *** WEATHERED, SPLINTERED DARK WOODEN CLOSET DOOR (x=512..960) ***
        s.append(f'<polygon points="526,0 960,0 960,540 512,540" fill="url(#{p}_closet_wood)"/>')
        # Vertical weathered wood planks with deep gaps, knots & splinters
        plank_edges = [526, 610, 698, 788, 878, 960]
        for i in range(len(plank_edges) - 1):
            x0, x1 = plank_edges[i], plank_edges[i + 1]
            dx_bot = -14 if i == 0 else -8
            tone = ["#241811", "#322217", "#2A1C13", "#382519", "#211610"][i % 5]
            s.append(f'<polygon points="{x0},0 {x1},0 {x1+dx_bot},540 {x0+dx_bot},540" fill="{tone}" opacity="0.58"/>')
            # Deep plank seam
            s.append(f'<path d="M{x0},0 L{x0+dx_bot},540" fill="none" stroke="#0C0805" stroke-width="2.8"/>')
            s.append(f'<path d="M{x0+2},0 L{x0+dx_bot+2},540" fill="none" stroke="#5C402B" stroke-width="0.9" opacity="0.45"/>')
            # Organic wood grain curves & splinter lines
            for _ in range(5):
                gx = rng.uniform(x0 + 8, x1 - 8)
                s.append(
                    f'<path d="M{gx:.1f},10 C{gx+rng.uniform(-6,6):.1f},180 {gx+rng.uniform(-6,6):.1f},360 {gx+dx_bot:.1f},535" '
                    f'fill="none" stroke="#18100A" stroke-width="{rng.uniform(0.8,1.5):.1f}" opacity="0.58"/>'
                )
        # Wood knots & rough gouge scratches near the lock area
        for kx, ky in [(568, 168), (656, 396), (748, 148), (836, 442), (618, 472)]:
            s.append(f'<ellipse cx="{kx}" cy="{ky}" rx="5.5" ry="12" fill="#170E09" stroke="#4D3422" stroke-width="1.0" opacity="0.72"/>')
            s.append(f'<ellipse cx="{kx}" cy="{ky}" rx="2.2" ry="5" fill="#0B0704" opacity="0.8"/>')
        # Deep wood splinters/cracks around bolt mounting zone
        s.append('<path d="M542,226 L568,244 L556,272 M716,322 L734,358 L722,388 M638,184 L644,218" fill="none" stroke="#0C0704" stroke-width="1.8"/>')
        s.append('<path d="M544,226 L570,244 M718,322 L736,358" fill="none" stroke="#6E4C32" stroke-width="0.9" opacity="0.58"/>')

        # *** BARE INCANDESCENT BULB & CORD (Upper Right — Warm Key Light!) ***
        s.append(f'<ellipse cx="836" cy="96" rx="195" ry="175" fill="url(#{p}_bulb_glow)"/>')
        # Braided wire coming down from ceiling
        s.append('<path d="M836,0 L836,54" fill="none" stroke="#18120E" stroke-width="3.2"/>')
        # Brass/Bakelite socket & pull chain
        s.append(f'<rect x="826" y="52" width="20" height="22" rx="3" fill="#4A3828" stroke="{INK_WARM}" stroke-width="1.4"/>')
        s.append('<path d="M846,66 L856,118" fill="none" stroke="#8C7348" stroke-width="1.2" stroke-dasharray="2,2"/>')
        s.append('<circle cx="856" cy="121" r="2.6" fill="#C9A258"/>')
        # Glowing glass bulb + filament
        s.append(f'<path d="M828,74 Q820,94 836,104 Q852,94 844,74 Z" fill="#FFF7D6" stroke="#D9A34A" stroke-width="1.2" filter="url(#{p}_glow_warm)"/>')
        s.append('<path d="M832,82 L836,92 L840,82" fill="none" stroke="#FFAA33" stroke-width="1.2"/>')

        # *** RUSTED HEAVY STRAP HINGES (Far Right Edge) ***
        for hy_h in (138, 412):
            s.append(f'<polygon points="866,{hy_h} 960,{hy_h-6} 960,{hy_h+38} 866,{hy_h+32}" fill="url(#{p}_rust)" stroke="{INK_WARM}" stroke-width="1.8"/>')
            s.append(f'<path d="M868,{hy_h+2} L958,{hy_h-4}" fill="none" stroke="#C47846" stroke-width="1.1" opacity="0.55"/>')
            for hx_b in (884, 916, 944):
                s.append(f'<circle cx="{hx_b}" cy="{hy_h+16}" r="4.5" fill="#2A1D17" stroke="#120B08" stroke-width="1.2"/>')
                s.append(f'<path d="M{hx_b-3},{hy_h+16} L{hx_b+3},{hy_h+16}" fill="none" stroke="#8C5332" stroke-width="1.0"/>')

        # =====================================================================
        # *** HERO CENTERPIECE: HEAVY FORGED IRON SLIDE BOLT & PADLOCK HASP ***
        # =====================================================================
        s.append('<g id="hero-iron-lock">')
        # Deep cast shadow on splintered wood below hardware (R9)
        s.append('<rect x="488" y="218" width="336" height="94" rx="5" fill="#090503" opacity="0.72"/>')
        s.append('<path d="M622,302 L726,302 L718,414 L630,414 Z" fill="#090503" opacity="0.68"/>')

        # 1) Left Keeper Plate mounted on doorframe jamb (x=478..542, y=206..298)
        s.append(f'<rect x="478" y="206" width="64" height="92" rx="3" fill="url(#{p}_iron_plate)" stroke="{INK}" stroke-width="2.0"/>')
        # Cold left rim + warm right rim on keeper plate
        s.append('<path d="M479,208 L479,296" fill="none" stroke="#8ACAE0" stroke-width="1.6" opacity="0.72"/>')
        s.append('<path d="M482,208 L540,208" fill="none" stroke="#E0A55A" stroke-width="1.2" opacity="0.6"/>')
        # Keeper staple loop
        s.append(f'<rect x="496" y="232" width="28" height="40" rx="4" fill="#1D242B" stroke="{INK}" stroke-width="1.8"/>')
        s.append('<rect x="502" y="238" width="16" height="28" rx="2" fill="#0B0F14"/>')

        # 2) Main Heavy Forged Iron Bolt Baseplate on door (x=554..816, y=206..298)
        s.append(f'<rect x="554" y="206" width="262" height="92" rx="4" fill="url(#{p}_iron_plate)" stroke="{INK}" stroke-width="2.2"/>')
        # Beveled inner recess & metallic wear scratches
        s.append('<rect x="562" y="214" width="246" height="76" rx="2" fill="none" stroke="#536370" stroke-width="1.0" opacity="0.52"/>')
        s.append('<path d="M558,208 L812,208" fill="none" stroke="#F5C072" stroke-width="1.6" opacity="0.68"/>')  # warm bulb top specular!
        # Scratches, hammer pits & rust drips on baseplate + wood below bolts
        s.append('<path d="M582,226 L618,232 M742,276 L792,268 M698,222 L724,228 M624,282 L652,276" fill="none" stroke="#9BB0BF" stroke-width="0.95" opacity="0.48"/>')
        s.append('<ellipse cx="786" cy="282" rx="14" ry="6" fill="#6E3B20" opacity="0.48"/>')
        s.append('<ellipse cx="578" cy="284" rx="12" ry="5" fill="#63351D" opacity="0.45"/>')
        # Rust streaks dripping from iron plate onto splintered wood below
        for rx_d, rlen_d in [(492, 42), (572, 54), (798, 46)]:
            s.append(f'<path d="M{rx_d},298 L{rx_d+1},{298+rlen_d}" fill="none" stroke="#5E3019" stroke-width="3.2" opacity="0.48"/>')
            s.append(f'<path d="M{rx_d+3},298 L{rx_d+2},{298+rlen_d*0.65:.0f}" fill="none" stroke="#783D1F" stroke-width="1.4" opacity="0.42"/>')

        # 6 Heavy Slotted/Hex Bolt Heads securing the plates
        bolt_pts = [(492, 220), (492, 284), (572, 222), (572, 282), (798, 222), (798, 282)]
        for bx_h, by_h in bolt_pts:
            hex_p = " ".join(
                f"{bx_h + 7.5*math.cos(math.radians(a)):.1f},{by_h + 7.5*math.sin(math.radians(a)):.1f}"
                for a in range(0, 360, 60)
            )
            s.append(f'<polygon points="{hex_p}" fill="#4A5863" stroke="{INK}" stroke-width="1.5"/>')
            s.append(f'<circle cx="{bx_h}" cy="{by_h}" r="3.4" fill="#232B32"/>')
            s.append(f'<path d="M{bx_h-3},{by_h-2} L{bx_h+3},{by_h+2}" fill="none" stroke="#A6BBC9" stroke-width="1.1"/>')

        # 3) Heavy Cylindrical Steel Slide-Bolt Bar pushed firmly into keeper!
        s.append(f'<rect x="498" y="241" width="286" height="22" rx="6" fill="url(#{p}_bolt_cyl)" stroke="{INK}" stroke-width="2.0"/>')
        # Bright metallic specular streak along top of slide-bolt
        s.append('<path d="M504,245 L778,245" fill="none" stroke="#E8F4FA" stroke-width="2.2" opacity="0.72"/>')
        s.append('<path d="M504,259 L778,259" fill="none" stroke="#E09F4B" stroke-width="1.2" opacity="0.48"/>')
        # Forged guide straps holding the bolt bar
        for gx_s in (588, 728):
            s.append(f'<rect x="{gx_s}" y="230" width="26" height="44" rx="3" fill="#2B343D" stroke="{INK}" stroke-width="1.8"/>')
            s.append(f'<path d="M{gx_s+3},233 L{gx_s+23},233" fill="none" stroke="#F0BD72" stroke-width="1.3" opacity="0.65"/>')
        # Heavy bolt handle knob (right side)
        s.append(f'<rect x="764" y="226" width="18" height="52" rx="6" fill="url(#{p}_bolt_cyl)" stroke="{INK}" stroke-width="1.8"/>')
        s.append('<circle cx="773" cy="274" r="11" fill="#5A6C78" stroke="#11171C" stroke-width="1.7"/>')
        s.append('<circle cx="770" cy="270" r="3.8" fill="#FFF0C8" opacity="0.72"/>')

        # 4) Padlock Hasp Loop + HEAVY FORGED IRON PADLOCK (LOCKED)
        # Hasp staple ring protruding downward from bolt center
        s.append(f'<path d="M648,262 L648,294 Q666,306 684,294 L684,262" fill="none" stroke="#11171C" stroke-width="10" stroke-linecap="round"/>')
        s.append(f'<path d="M648,262 L648,294 Q666,306 684,294 L684,262" fill="none" stroke="#6E8290" stroke-width="5.2" stroke-linecap="round"/>')

        # Hardened steel padlock shackle
        s.append(f'<path d="M636,334 L636,294 A30,28 0 0,1 696,294 L696,334" fill="none" stroke="{INK}" stroke-width="15" stroke-linecap="round"/>')
        s.append(f'<path d="M636,334 L636,294 A30,28 0 0,1 696,294 L696,334" fill="none" stroke="url(#{p}_shackle)" stroke-width="10.5" stroke-linecap="round"/>')
        # Specular shine arc on shackle
        s.append('<path d="M642,292 A24,22 0 0,1 686,282" fill="none" stroke="#F2FBFF" stroke-width="2.0" opacity="0.78"/>')

        # Cast-iron padlock body (x=618..714, y=326..410)
        s.append(f'<rect x="618" y="326" width="96" height="84" rx="10" fill="url(#{p}_padlock_body)" stroke="{INK}" stroke-width="2.2"/>')
        # Laminated steel/rivet horizontal band lines + wear scratches
        for ly_p in (342, 358, 374, 390):
            s.append(f'<path d="M620,{ly_p} L712,{ly_p}" fill="none" stroke="#161C22" stroke-width="1.3" opacity="0.78"/>')
            s.append(f'<path d="M622,{ly_p+1.5} L710,{ly_p+1.5}" fill="none" stroke="#6B7E8C" stroke-width="0.7" opacity="0.38"/>')
        # Warm right rim + cold left rim on padlock body
        s.append('<path d="M621,334 L621,402" fill="none" stroke="#7EC4DC" stroke-width="1.8" opacity="0.65"/>')
        s.append('<path d="M711,334 L711,402" fill="none" stroke="#F0B562" stroke-width="1.8" opacity="0.72"/>')
        # Brass keyhole escutcheon plate in center of padlock
        s.append('<circle cx="666" cy="368" r="14" fill="#9E7636" stroke="#1E150A" stroke-width="1.5"/>')
        s.append('<circle cx="666" cy="364" r="4.5" fill="#0B0E12"/>')
        s.append('<polygon points="663,366 669,366 671,378 661,378" fill="#0B0E12"/>')
        # Embossed word "LOCKED" on padlock bottom band
        s.append('<text x="666" y="402" text-anchor="middle" fill="#A8BCC9" font-family="Consolas,monospace" font-size="9.5" font-weight="bold" letter-spacing="2.2" opacity="0.82">LOCKED</text>')
        s.append('</g>')

        s.append('</g>')
        parts.append("\n".join(s))

    # --- LAYER 4: PLAN GÖRÜŞÜ (#7FE6FF Blueprint Analysis bridging both halves) ---
    if plan_gorusu and _katman_aktif(katmanlar, "plan"):
        pl: list[str] = [f'<g id="kilit-plan" filter="url(#{p}_glow_cyan)" opacity="0.86">']
        # Left Juvenile Hall bar spacing readout & crisp cyan tag
        pl.append(f'<text x="72" y="102" fill="{PLAN}" font-family="Consolas,monospace" font-size="10.5" font-weight="bold">JUVENILE HALL</text>')
        pl.append(f'<path d="M184,162 L254,162 M184,156 L184,168 M254,156 L254,168" fill="none" stroke="{PLAN}" stroke-width="1.1"/>')
        pl.append(f'<text x="219" y="153" text-anchor="middle" fill="{PLAN}" font-family="Consolas,monospace" font-size="9.5" font-weight="bold">01 · BARS</text>')

        # Right heavy iron bolt & padlock mechanical blueprint overlay
        pl.append(f'<path d="M472,200 L822,200 L822,304 L722,304 L722,418 L610,418 L610,304 L472,304 Z" fill="none" stroke="{PLAN}" stroke-width="1.15" stroke-dasharray="6,4" opacity="0.72"/>')
        # Bolt throw & keyhole callouts
        pl.append(f'<circle cx="510" cy="252" r="6" fill="none" stroke="{PLAN}" stroke-width="1.3"/>')
        pl.append(f'<circle cx="510" cy="252" r="2" fill="{PLAN_CORE}"/>')
        pl.append(f'<path d="M510,246 L510,174 L616,174" fill="none" stroke="{PLAN}" stroke-width="1.1"/>')
        pl.append(f'<text x="622" y="177" fill="{PLAN}" font-family="Consolas,monospace" font-size="10.5" font-weight="bold">02 · IRON BOLT</text>')

        pl.append(f'<circle cx="666" cy="368" r="19" fill="none" stroke="{PLAN}" stroke-width="1.15" stroke-dasharray="4,3"/>')
        pl.append(f'<path d="M685,368 L758,368 L758,396" fill="none" stroke="{PLAN}" stroke-width="1.1"/>')
        pl.append(f'<text x="764" y="399" fill="{PLAN}" font-family="Consolas,monospace" font-size="10.5" font-weight="bold">03 · LOCKED</text>')
        pl.append('</g>')
        parts.append("\n".join(pl))

    # --- LAYER 5: ÖN PLAN (Warm dust motes in bulb light, cold mist on left, vignette) ---
    if _katman_aktif(katmanlar, "onplan"):
        f: list[str] = ['<g id="kilit-onplan">']
        # Warm dust motes floating in bare bulb cone (right half)
        for _ in range(28):
            dx = rng.uniform(530, 940)
            dy = rng.uniform(40, 480)
            dr = rng.uniform(0.9, 2.3)
            f.append(f'<circle cx="{dx:.1f}" cy="{dy:.1f}" r="{dr:.1f}" fill="#FFE9B5" opacity="{rng.uniform(0.20,0.60):.2f}"/>')
        # Cold damp air particles on left corridor
        for _ in range(18):
            dx = rng.uniform(20, 440)
            dy = rng.uniform(60, 480)
            dr = rng.uniform(0.9, 2.0)
            f.append(f'<circle cx="{dx:.1f}" cy="{dy:.1f}" r="{dr:.1f}" fill="#BCEBF0" opacity="{rng.uniform(0.14,0.38):.2f}"/>')
        f.append(f'<rect x="0" y="0" width="960" height="540" fill="url(#{p}_vignette)"/>')
        f.append('</g>')
        parts.append("\n".join(f))

    return defs, "\n".join(parts)


# =============================================================================
# RENDER & PRESENTATION CARDS (1280x720 Set Card + 1280x720 R13 200% Crop Card)
# =============================================================================
def _render_scene_pil(scene_fn, width: int = 1920, height: int = 1080,
                      plan_gorusu: bool = True) -> Image.Image:
    defs, body = scene_fn(plan_gorusu=plan_gorusu)
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {W_SCENE} {H_SCENE}">'
        f'<defs>{defs}</defs>'
        f'{body}'
        f'</svg>'
    )
    png_bytes = resvg_py.svg_to_bytes(svg_string=svg)
    return Image.open(io.BytesIO(png_bytes)).convert("RGBA")


def _load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = (
        ["C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf"]
        if bold else
        ["C:/Windows/Fonts/segoeui.ttf", "C:/Windows/Fonts/arial.ttf"]
    )
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def _draw_card_bg(w: int = 1280, h: int = 720) -> Image.Image:
    svg = f"""
    <svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
      <defs>
        <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0%" stop-color="#091019"/>
          <stop offset="55%" stop-color="#0F1824"/>
          <stop offset="100%" stop-color="#0A121C"/>
        </linearGradient>
      </defs>
      <rect width="{w}" height="{h}" fill="url(#bg)"/>
      <g stroke="#1C2B3D" stroke-width="1" opacity="0.28">
        {"".join(f'<line x1="{x}" y1="0" x2="{x}" y2="{h}"/>' for x in range(0, w, 64))}
        {"".join(f'<line x1="0" y1="{y}" x2="{w}" y2="{y}"/>' for y in range(0, h, 64))}
      </g>
    </svg>
    """
    return Image.open(io.BytesIO(resvg_py.svg_to_bytes(svg_string=svg))).convert("RGBA")


def _draw_panel_box(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int],
                    radius: int = 10, fill=(17, 26, 39, 235), outline=(42, 62, 86, 255)) -> None:
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=1)


def _draw_swatches(draw: ImageDraw.ImageDraw, x: int, y: int, colors: list[str],
                   size: int = 16, gap: int = 6) -> None:
    for i, hex_c in enumerate(colors):
        cx = x + i * (size + gap)
        draw.rounded_rectangle((cx, y, cx + size, y + size), radius=3, fill=hex_c, outline="#384D66", width=1)


def uret_kartlar(versiyon: str = "v1") -> tuple[Path, Path]:
    print("Rendering 3 Chapter I childhood & lock sets at 1920x1080...")
    img_101 = _render_scene_pil(set_101_kapi, 1920, 1080)
    img_102 = _render_scene_pil(set_102_mutfak, 1920, 1080)
    img_103 = _render_scene_pil(set_103_islahevi_kilit, 1920, 1080)

    # =========================================================================
    # OUTPUT 1: SET PRESENTATION CARD (1280 x 720, ALL ENGLISH)
    # =========================================================================
    canvas = _draw_card_bg(1280, 720)
    draw = ImageDraw.Draw(canvas)

    f_title = _load_font(20, bold=True)
    f_sub = _load_font(12, bold=False)
    f_card_t = _load_font(13, bold=True)
    f_card_s = _load_font(11, bold=False)
    f_small = _load_font(10, bold=False)

    # Top header bar
    draw.text((24, 14), "MICHAEL SCOFIELD  ·  CHAPTER I CHILDHOOD & LOCK SETS", fill="#EBF3FA", font=f_title)
    draw.text((24, 39), "STYLE B+A HYBRID (CINEMATIC 2D + CYAN BLUEPRINT VISION)  ·  SCENES 1.01 – 1.03",
              fill="#7E97B0", font=f_sub)
    top_swatches = [("#4E311E", "OAK"), ("#E5B95C", "BRASS"), ("#28425C", "RAIN"),
                    ("#22363E", "HALL"), ("#7FE6FF", "PLAN")]
    sx_top = 874
    for col, lbl in top_swatches:
        draw.rounded_rectangle((sx_top, 18, sx_top + 14, 32), radius=3, fill=col, outline="#3B536D", width=1)
        draw.text((sx_top + 19, 19), lbl, fill="#9BB2C8", font=f_small)
        sx_top += 76
    draw.line((24, 58, 1256, 58), fill="#213247", width=1)

    # --- TOP LEFT: 1.01 FAMILY FRONT DOOR ---
    _draw_panel_box(draw, (22, 68, 630, 366))
    t101 = img_101.resize((448, 252), Image.Resampling.LANCZOS)
    canvas.paste(t101, (34, 98), t101)
    draw.rectangle((34, 98, 34 + 448, 98 + 252), outline="#3E3228", width=1)
    draw.text((34, 76), "1.01 · FAMILY FRONT DOOR", fill="#E5B95C", font=f_card_t)
    draw.text((228, 78), "BURROWS → SCOFIELD · Rainy 1980s Entryway", fill="#8AA3BC", font=f_card_s)
    ix = 492
    draw.text((ix, 98), "PALETTE", fill="#7FE6FF", font=f_small)
    _draw_swatches(draw, ix, 114, ["#0E1D33", "#4E311E", "#E5B95C", "#FFCA75", "#7FE6FF"], size=18, gap=5)
    draw.text((ix, 146), "KEY DETAILS", fill="#9BB2C8", font=f_small)
    for k_i, item in enumerate([
        "• Carved oak door + glass",
        "• Brass SCOFIELD plate",
        "• Father's coat silhouette",
        "• Framed family photo",
        "• Parquet wet reflections",
    ]):
        draw.text((ix, 164 + k_i * 19), item, fill="#D5E2EE", font=f_card_s)
    draw.text((ix, 272), "KEY LIGHT", fill="#9BB2C8", font=f_small)
    draw.text((ix, 288), "Warm foyer vs. streetlamp", fill="#F6C367", font=f_card_s)
    draw.text((ix, 314), "LAYERS (5)", fill="#9BB2C8", font=f_small)
    draw.text((ix, 330), "far · mid · scene\nplan · foreground", fill="#8AA3BC", font=f_small)

    # --- TOP RIGHT: 1.02 RAINY KITCHEN ---
    _draw_panel_box(draw, (648, 68, 1256, 366))
    t102 = img_102.resize((448, 252), Image.Resampling.LANCZOS)
    canvas.paste(t102, (660, 98), t102)
    draw.rectangle((660, 98, 660 + 448, 98 + 252), outline="#2E455E", width=1)
    draw.text((660, 76), "1.02 · RAINY KITCHEN", fill="#7FE6FF", font=f_card_t)
    draw.text((832, 78), "AGE 11 · Warm-to-Cold Glass Reflection", fill="#8AA3BC", font=f_card_s)
    ix2 = 1118
    draw.text((ix2, 98), "PALETTE", fill="#7FE6FF", font=f_small)
    _draw_swatches(draw, ix2, 114, ["#182C42", "#563824", "#8A5242", "#E6D9C3", "#7FE6FF"], size=18, gap=5)
    draw.text((ix2, 146), "KEY DETAILS", fill="#9BB2C8", font=f_small)
    for k_i, item in enumerate([
        "• Ceramic tile & cabinets",
        "• Gingham curtains & rain",
        "• Brothers' reflection + '?'",
        "• Cold & warm ceramic mugs",
        "• Kettle, paper & chair",
    ]):
        draw.text((ix2, 164 + k_i * 19), item, fill="#D5E2EE", font=f_card_s)
    draw.text((ix2, 272), "KEY LIGHT", fill="#9BB2C8", font=f_small)
    draw.text((ix2, 288), "Storm twilight + lamp", fill="#9BD1E8", font=f_card_s)
    draw.text((ix2, 314), "LAYERS (5)", fill="#9BB2C8", font=f_small)
    draw.text((ix2, 330), "far · mid · scene\nplan · foreground", fill="#8AA3BC", font=f_small)

    # --- BOTTOM FEATURE PANEL: 1.03 JUVENILE HALL & FOSTER CLOSET LOCK ---
    _draw_panel_box(draw, (22, 378, 1256, 704))
    t103 = img_103.resize((512, 288), Image.Resampling.LANCZOS)
    canvas.paste(t103, (34, 404), t103)
    draw.rectangle((34, 404, 34 + 512, 404 + 288), outline="#4E3F31", width=1)
    draw.text((34, 384), "1.03 · JUVENILE HALL & FOSTER CLOSET LOCK", fill="#F6C367", font=f_card_t)
    draw.text((366, 386), "JUVENILE HALL / LOCKED · Split-Depth Hero Set", fill="#96AEC6", font=f_card_s)

    rx = 564
    draw.text((rx, 404), "PALETTE (COLD INSTITUTIONAL VS. WARM BULB)", fill="#E8C89B", font=f_small)
    _draw_swatches(draw, rx, 422, ["#142229", "#22363E", "#8FA6B0", "#3F2B1D", "#FFD075", "#7FE6FF"], size=22, gap=7)
    draw.text((rx, 458), "HERO DETAILS (6+)", fill="#9BB2C8", font=f_small)
    for k_i, item in enumerate([
        "• Wet Juvenile Hall tile reflections & caged fluorescent",
        "• Peeling paint, exposed brick & riveted steel bars",
        "• 15-year-old Lincoln rim-lit silhouette gripping bar",
        "• Splintered dark foster closet door + rusted hinges",
        "• Bare hanging bulb casting warm-vs-cold rim contrast",
        "• Forged iron slide bolt & padlock hasp (LOCKED)",
    ]):
        draw.text((rx, 476 + k_i * 19), item, fill="#E3ECF5", font=f_card_s)
    draw.text((rx, 602), "LIGHTING & TENSION", fill="#9BB2C8", font=f_small)
    draw.text((rx, 618), "Zero violence depicted — tension is carried purely\nthrough texture, cold steel bars, splintered oak,\nand specular rim lighting on the heavy iron lock.",
              fill="#D4C2AB", font=f_card_s)

    draw.line((896, 404, 896, 692), fill="#233447", width=1)
    tx = 914
    draw.text((tx, 404), "CHAPTER I VISUAL ARCHITECTURE", fill="#7FE6FF", font=f_card_t)
    notes = [
        ("TEXTURE-FIRST WORLD",
         "Zero flat-color fills: every wood plank, ceramic\ntile, concrete block, brass plate, and forged\niron bolt carries grain, wear, and rim light."),
        ("ENGLISH ON-SCREEN TEXT",
         "All diegetic signs and blueprint overlays are\nrendered in crisp English (SCOFIELD, AGE 11,\nJUVENILE HALL, LOCKED)."),
        ("5-LAYER PARALLAX READY",
         "Each 960×540 function returns (defs, body)\nwith 5 isolated <g> depth layers for direct\nintegration into the animation engine."),
    ]
    ny = 432
    for heading, body_txt in notes:
        draw.text((tx, ny), heading, fill="#F6C367" if "TEXTURE" in heading else "#9EC5DE", font=f_small)
        draw.text((tx, ny + 16), body_txt, fill="#C5D5E4", font=f_card_s)
        ny += 86

    out_main = OUT_DIR / f"b1_set_cocukluk_{versiyon}.png"
    canvas.convert("RGB").save(out_main, quality=95)

    # =========================================================================
    # OUTPUT 2: R13 200% ZOOM CROP CARD (1280 x 720 — 4 PANELS, ALL ENGLISH)
    # =========================================================================
    r13 = _draw_card_bg(1280, 720)
    d13 = ImageDraw.Draw(r13)
    d13.text((24, 13), "R13 · 200% ZOOM QUALITY INSPECTION (CHAPTER I CHILDHOOD & LOCK SETS)", fill="#EBF3FA", font=f_title)
    d13.text((24, 37), "1:1 PIXEL CROPS FROM 1920×1080 RENDERS  ·  TEXTURE, SPECULAR LIGHT, CONTACT SHADOWS & BLUEPRINT DETAIL",
             fill="#7E97B0", font=f_sub)
    d13.line((24, 55, 1256, 55), fill="#213247", width=1)

    cw, ch = 600, 264
    crops = [
        (img_101, (1080, 442), "1 · 1.01 BRASS NAMEPLATE & CARVED OAK DOOR (200%)",
         "Engraved SCOFIELD plate, ghosted BURROWS, brass screws, wood grain & cyan glint", (22, 66)),
        (img_102, (1010, 865), "2 · 1.02 KITCHEN CERAMIC MUGS, KETTLE & TABLE (200%)",
         "Cold vs. warm ceramic mugs, fading steam, kettle speculars, newspaper & wood grain", (652, 66)),
        (img_103, (460, 495), "3 · 1.03 JUVENILE HALL CORRIDOR & STEEL BARS (200%)",
         "Riveted steel bars, 15yo Lincoln rim-lit silhouette & hand grip, peeling brick wall", (22, 392)),
        (img_103, (1315, 650), "4 · 1.03 HEAVY IRON BOLT, PADLOCK & SPLINTERED WOOD (200%)",
         "Forged iron bolt, LOCKED padlock shackle, hex bolts, rust drips & warm/cold rims", (652, 392)),
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

    out_r13 = OUT_DIR / "b1_set_cocukluk_r13.png"
    r13.convert("RGB").save(out_r13, quality=95)
    print(f"Saved:\n  - {out_main}\n  - {out_r13}")
    return out_main, out_r13


if __name__ == "__main__":
    uret_kartlar("v1")
