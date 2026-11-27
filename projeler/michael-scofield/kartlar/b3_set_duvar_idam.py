"""V8 (Act III: Cell Wall Allen Bolt, Riot Air Vent Rescue & Execution Night Red Phone).

Style B+A Hybrid (Cinematic 2D + Cyan Blueprint Vision) — 5-layer parallax-ready scenes (960x540):
  - set_304_duvar_civata(katmanlar=None) -> (defs_str, body_str)
  - set_305_isyan_kanal(katmanlar=None)  -> (defs_str, body_str)
  - set_306_idam_telefon(katmanlar=None) -> (defs_str, body_str)

Rules enforced:
  - 100% ENGLISH on-screen typography.
  - Every stroked <path> explicitly sets fill="none" (unless an intentional filled closed shape).
  - R4-PARALAKS: All character anatomy (head, neck, torso, arms, hands) + directly contacted
    objects live inside the single `sahne` depth layer so parallax shifts never detach limbs.
  - NON-VIOLENT BOUNDARY: Scene 3.06 contains ZERO blood, gore, or electric-chair close-up;
    tension is conveyed via cold corridor shadows, distant Lincoln silhouette, shorted blue
    cable spark, frozen hand on the breaker switch, and ringing red court phone.
  - Side-effect-free module; imports locked Michael v3 & Sara v2 from karakter.py without editing it.
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
INK_CHAR = "#1A1513"
PLAN = "#7FE6FF"
PLAN_CORE = "#E4FCFF"
RED_ALERT = "#E63244"
RED_PHONE = "#E52432"
FIRE_ORANGE = "#FF6A24"
FIRE_GOLD = "#FFB948"

_UID = 0


def _uid(prefix: str = "b3") -> str:
    global _UID
    _UID += 1
    return f"{prefix}_{_UID}"


def _katman_aktif(katmanlar: set[str] | list[str] | None, ad: str) -> bool:
    return katmanlar is None or ad in katmanlar


def _days_hud(
    x: float,
    y: float,
    days_text: str,
    accent: str = RED_ALERT,
    sub_text: str = "FOX RIVER · COUNTDOWN",
) -> str:
    """Crisp top-right countdown HUD badge matching Act II-III visual language."""
    return (
        f'<g transform="translate({x:.1f},{y:.1f})">'
        f'<rect x="0" y="0" width="214" height="52" rx="5" fill="#08101A" fill-opacity="0.90" '
        f'stroke="{accent}" stroke-width="1.6"/>'
        f'<rect x="0" y="0" width="5" height="52" rx="2" fill="{accent}"/>'
        f'<circle cx="17" cy="14" r="3.4" fill="{accent}"/>'
        f'<text x="27" y="18" font-family="Consolas, DejaVu Sans Mono, monospace" font-size="9.5" '
        f'font-weight="bold" fill="#9CB6CC" letter-spacing="0.9">{sub_text}</text>'
        f'<text x="16" y="42" font-family="Segoe UI, Arial, sans-serif" font-size="21" '
        f'font-weight="bold" fill="#F2F8FC" letter-spacing="1.1">{days_text}</text>'
        f'</g>'
    )


# =============================================================================
# SCENE 3.04: ALLEN BOLT & HIDDEN HEART (DAYS LEFT: 14)
# =============================================================================
def set_304_duvar_civata(
    katmanlar: set[str] | list[str] | None = None,
    tuvalet_dx: float = 0.0,
) -> tuple[str, str]:
    """Fox River cell wall with R18-HAREKET animation-ready layers:
      - `uzak`       : Clean concrete cell wall, ceiling fluorescent, bunk, bar shadows
      - `orta`       : Floor baseboard & subtle wall cracks
      - `duvar_oyuk` : Concrete breach + deep maintenance pipes aligned directly behind toilet
      - `tuvalet`    : Fox River stainless-steel toilet/sink unit (at tuvalet_dx=0.0 fully covers
                       `duvar_oyuk`; slides left via tuvalet_dx or layer transform to reveal shaft)
      - `civata`     : Hero rotating bright hexagonal Allen bolt (#11121147)
      - `plan`       : #7FE6FF cyan CAD underground pipe network + DAYS LEFT: 14 HUD
      - `onplan`     : Foreground prison bar edge, dust motes & vignette
    When `katmanlar=None`, all layers render in proper depth order.
    """
    rng = random.Random(304)
    p = _uid("s304")

    # Breach polygon aligned directly behind the default (tuvalet_dx=0) steel toilet unit (x: 424..724, y: 168..406)
    breach_d = (
        "M436,180 L492,168 L576,164 L668,174 L718,196 L728,266 L720,350 "
        "L694,400 L602,408 L496,402 L438,376 L424,284 Z"
    )
    breach_in = (
        "M450,192 L500,182 L576,178 L658,188 L704,208 L712,270 L704,342 "
        "L682,388 L598,394 L504,388 L452,364 L440,284 Z"
    )

    defs = f"""
    <linearGradient id="{p}_wall" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#1A252B"/>
      <stop offset="38%" stop-color="#27363E"/>
      <stop offset="82%" stop-color="#1E2A31"/>
      <stop offset="100%" stop-color="#11191E"/>
    </linearGradient>
    <linearGradient id="{p}_floor" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#1B242A"/>
      <stop offset="55%" stop-color="#141C21"/>
      <stop offset="100%" stop-color="#0B1014"/>
    </linearGradient>
    <radialGradient id="{p}_fluor" cx="0.34" cy="0.06" r="0.64">
      <stop offset="0%" stop-color="#C8F2FF" stop-opacity="0.34"/>
      <stop offset="42%" stop-color="#76AFC0" stop-opacity="0.14"/>
      <stop offset="100%" stop-color="#1A252B" stop-opacity="0.0"/>
    </radialGradient>
    <radialGradient id="{p}_shaft_deep" cx="0.54" cy="0.50" r="0.62">
      <stop offset="0%" stop-color="#0C202B"/>
      <stop offset="52%" stop-color="#060D13"/>
      <stop offset="100%" stop-color="#020508"/>
    </radialGradient>
    <linearGradient id="{p}_pipe_rust" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#1A2226"/>
      <stop offset="28%" stop-color="#4B5B63"/>
      <stop offset="54%" stop-color="#6B7E87"/>
      <stop offset="82%" stop-color="#333E44"/>
      <stop offset="100%" stop-color="#12181C"/>
    </linearGradient>
    <linearGradient id="{p}_pipe_h" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#192126"/>
      <stop offset="30%" stop-color="#5B6E78"/>
      <stop offset="52%" stop-color="#7A909B"/>
      <stop offset="84%" stop-color="#2D373D"/>
      <stop offset="100%" stop-color="#101518"/>
    </linearGradient>
    <linearGradient id="{p}_steel" x1="0" y1="0" x2="1" y2="0.15">
      <stop offset="0%" stop-color="#52626C"/>
      <stop offset="24%" stop-color="#A8BBC6"/>
      <stop offset="48%" stop-color="#D3E2EB"/>
      <stop offset="76%" stop-color="#738793"/>
      <stop offset="100%" stop-color="#35424A"/>
    </linearGradient>
    <linearGradient id="{p}_steel_dark" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#879BA7"/>
      <stop offset="50%" stop-color="#4E5F69"/>
      <stop offset="100%" stop-color="#273138"/>
    </linearGradient>
    <linearGradient id="{p}_bolt_metal" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F6FCFF"/>
      <stop offset="26%" stop-color="#B9D3E0"/>
      <stop offset="58%" stop-color="#6A8594"/>
      <stop offset="84%" stop-color="#3C4E59"/>
      <stop offset="100%" stop-color="#1D272E"/>
    </linearGradient>
    <linearGradient id="{p}_bolt_thread" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#28353D"/>
      <stop offset="30%" stop-color="#9EB8C7"/>
      <stop offset="55%" stop-color="#E4F4FC"/>
      <stop offset="82%" stop-color="#526875"/>
      <stop offset="100%" stop-color="#1A2329"/>
    </linearGradient>
    <radialGradient id="{p}_cyan_glow" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0%" stop-color="{PLAN}" stop-opacity="0.46"/>
      <stop offset="55%" stop-color="{PLAN}" stop-opacity="0.14"/>
      <stop offset="100%" stop-color="{PLAN}" stop-opacity="0.0"/>
    </radialGradient>
    <radialGradient id="{p}_vig" cx="0.5" cy="0.48" r="0.68">
      <stop offset="52%" stop-color="#000000" stop-opacity="0.0"/>
      <stop offset="100%" stop-color="#03070B" stop-opacity="0.72"/>
    </radialGradient>
    <clipPath id="{p}_breach_clip">
      <path d="{breach_d}"/>
    </clipPath>
    """

    parts: list[str] = []

    # ── LAYER 1: uzak (Clean Fox River cell concrete wall, fluorescent, bar shadows, bunk) ──
    if _katman_aktif(katmanlar, "uzak"):
        uzak: list[str] = ['<g id="s304-uzak">']
        uzak.append(f'<rect x="0" y="0" width="960" height="432" fill="url(#{p}_wall)"/>')
        uzak.append(f'<rect x="0" y="424" width="960" height="116" fill="url(#{p}_floor)"/>')
        uzak.append(f'<rect x="0" y="0" width="960" height="432" fill="url(#{p}_fluor)"/>')

        # Concrete masonry blocks
        block_lines: list[str] = []
        for row, y in enumerate(range(36, 430, 44)):
            block_lines.append(f'<line x1="0" y1="{y}" x2="960" y2="{y}" stroke="#121B20" stroke-width="1.4" opacity="0.72"/>')
            offset = 42 if row % 2 else 0
            for x in range(offset, 960, 84):
                block_lines.append(f'<line x1="{x}" y1="{y}" x2="{x}" y2="{y + 44}" stroke="#121B20" stroke-width="1.2" opacity="0.62"/>')
        uzak.append("".join(block_lines))

        # Fluorescent ceiling fixture
        uzak.append('<rect x="242" y="14" width="212" height="10" rx="3" fill="#2A3A42" stroke="#10181D" stroke-width="1.6"/>')
        uzak.append('<rect x="252" y="17" width="192" height="5" rx="2" fill="#DDF8FF"/>')

        # Diagonal prison bar shadow bands cast across wall
        uzak.append(
            '<g opacity="0.24" fill="#060B0F">'
            '<polygon points="48,0 82,0 18,432 -16,432"/>'
            '<polygon points="154,0 188,0 124,432 90,432"/>'
            '<polygon points="260,0 294,0 230,432 196,432"/>'
            '<polygon points="366,0 400,0 336,432 302,432"/>'
            '<polygon points="472,0 506,0 442,432 408,432"/>'
            '</g>'
        )

        # Cell bunk silhouette on far left for spatial continuity
        uzak.append('<rect x="18" y="114" width="12" height="328" fill="#172228" stroke="#0C1317" stroke-width="1.8"/>')
        uzak.append('<rect x="0" y="168" width="112" height="16" fill="#23313A" stroke="#0C1317" stroke-width="1.6"/>')
        uzak.append('<rect x="0" y="314" width="118" height="18" fill="#23313A" stroke="#0C1317" stroke-width="1.6"/>')
        uzak.append('<path d="M0,152 L106,152 L106,168 L0,168 Z" fill="#3B4D57" stroke="#0C1317" stroke-width="1.4"/>')
        uzak.append('<path d="M0,298 L112,298 L112,314 L0,314 Z" fill="#3B4D57" stroke="#0C1317" stroke-width="1.4"/>')
        uzak.append("</g>")
        parts.append("".join(uzak))

    # ── LAYER 2: orta (Floor baseboard & concrete wall shelf detail) ──
    if _katman_aktif(katmanlar, "orta"):
        orta: list[str] = ['<g id="s304-orta">']
        orta.append(f'<line x1="0" y1="428" x2="960" y2="428" stroke="{INK}" stroke-width="2.2"/>')
        # Small steel cell wall shelf on far right
        orta.append(f'<rect x="772" y="182" width="116" height="10" rx="2" fill="#3B4E59" stroke="{INK}" stroke-width="1.8"/>')
        orta.append(f'<polygon points="784,192 798,192 784,218" fill="#28363E" stroke="{INK}" stroke-width="1.4"/>')
        orta.append(f'<polygon points="876,192 862,192 876,218" fill="#28363E" stroke="{INK}" stroke-width="1.4"/>')
        orta.append("</g>")
        parts.append("".join(orta))

    # ── LAYER 3A (R18-HAREKET): duvar_oyuk (Concrete breach + deep maintenance pipes behind toilet) ──
    if _katman_aktif(katmanlar, "duvar_oyuk"):
        oyuk: list[str] = ['<g id="s304-duvar-oyuk">']
        oyuk.append(f'<path d="{breach_d}" fill="url(#{p}_shaft_deep)"/>')
        oyuk.append(f'<g clip-path="url(#{p}_breach_clip)">')
        # Receding tunnel perspective ribs
        for k in range(5):
            inset = k * 21
            rx = 454 + inset * 1.12
            ry = 186 + inset * 0.78
            rw = max(42, 246 - inset * 2.10)
            rh = max(38, 198 - inset * 1.72)
            oyuk.append(
                f'<rect x="{rx:.1f}" y="{ry:.1f}" width="{rw:.1f}" height="{rh:.1f}" rx="4" '
                f'fill="none" stroke="#162936" stroke-width="{2.3 - k * 0.3:.1f}" opacity="{0.75 - k * 0.11:.2f}"/>'
            )
        # Subtle cyan underground glow at vanishing point
        oyuk.append(f'<ellipse cx="584" cy="286" rx="104" ry="78" fill="url(#{p}_cyan_glow)"/>')

        # Heavy dark vertical & horizontal maintenance pipes receding into shaft
        oyuk.append(f'<rect x="568" y="156" width="20" height="260" fill="url(#{p}_pipe_rust)" stroke="{INK}" stroke-width="1.6" opacity="0.74"/>')
        oyuk.append(f'<rect x="614" y="156" width="16" height="260" fill="url(#{p}_pipe_rust)" stroke="{INK}" stroke-width="1.4" opacity="0.64"/>')
        # Mid-depth horizontal steam conduit + flange bolts
        oyuk.append(f'<rect x="420" y="246" width="320" height="24" fill="url(#{p}_pipe_h)" stroke="{INK}" stroke-width="1.8"/>')
        for fx in (476, 558, 650):
            oyuk.append(f'<rect x="{fx}" y="241" width="10" height="34" rx="2" fill="#526570" stroke="{INK}" stroke-width="1.4"/>')
        # Foreground vertical main pipe inside shaft
        oyuk.append(f'<rect x="498" y="154" width="34" height="264" fill="url(#{p}_pipe_rust)" stroke="{INK}" stroke-width="2.0"/>')
        oyuk.append(f'<rect x="492" y="210" width="46" height="11" rx="2" fill="#465761" stroke="{INK}" stroke-width="1.6"/>')
        oyuk.append(f'<rect x="492" y="332" width="46" height="11" rx="2" fill="#465761" stroke="{INK}" stroke-width="1.6"/>')
        # Curved pipe running deep into lower tunnel
        oyuk.append(f'<path d="M674,166 L674,316 Q674,344 646,344 L424,344" fill="none" stroke="{INK}" stroke-width="24" stroke-linecap="round"/>')
        oyuk.append(f'<path d="M674,166 L674,316 Q674,344 646,344 L424,344" fill="none" stroke="#4D606B" stroke-width="19" stroke-linecap="round"/>')
        oyuk.append(f'<path d="M670,166 L670,314 Q670,339 646,339 L424,339" fill="none" stroke="#859FA9" stroke-width="4.5" stroke-linecap="round" opacity="0.55"/>')
        # Red-rust valve wheel
        oyuk.append('<circle cx="634" cy="258" r="20" fill="none" stroke="#7A3229" stroke-width="5.0"/>')
        oyuk.append(f'<circle cx="634" cy="258" r="20" fill="none" stroke="{INK}" stroke-width="1.6"/>')
        oyuk.append('<path d="M616,258 L652,258 M634,240 L634,276" fill="none" stroke="#61251E" stroke-width="3.2"/>')
        oyuk.append(f'<circle cx="634" cy="258" r="4.8" fill="#9A4538" stroke="{INK}" stroke-width="1.4"/>')
        oyuk.append("</g>")

        # 3D Concrete bevel rim around the breach
        oyuk.append(
            f'<path d="{breach_d} {breach_in}" '
            'fill="#3E5059" fill-rule="evenodd" stroke="#10181D" stroke-width="2.2" stroke-linejoin="round"/>'
        )
        # Cut steel rebar stubs poking out of concrete edge
        oyuk.append(
            '<path d="M430,236 L460,238" fill="none" stroke="#6E7E87" stroke-width="4.0" stroke-linecap="round"/>'
            '<path d="M718,284 L688,280" fill="none" stroke="#6E7E87" stroke-width="4.0" stroke-linecap="round"/>'
            '<path d="M566,166 L568,194" fill="none" stroke="#6E7E87" stroke-width="3.6" stroke-linecap="round"/>'
            '<path d="M604,404 L602,378" fill="none" stroke="#6E7E87" stroke-width="3.6" stroke-linecap="round"/>'
        )
        # Concrete rubble chunks on floor directly beneath breach
        for _ in range(14):
            rx = rng.uniform(434, 718)
            ry = rng.uniform(422, 460)
            rw = rng.uniform(6, 17)
            rh = rng.uniform(4, 10)
            oyuk.append(
                f'<polygon points="{rx:.1f},{ry:.1f} {rx+rw*0.6:.1f},{ry-rh:.1f} '
                f'{rx+rw:.1f},{ry-rh*0.2:.1f} {rx+rw*0.8:.1f},{ry+rh*0.5:.1f}" '
                f'fill="#3D4E57" stroke="{INK}" stroke-width="1.1"/>'
            )
        oyuk.append("</g>")
        parts.append("".join(oyuk))

    # ── LAYER 3B (R18-HAREKET): tuvalet (Stainless-steel unit; at tuvalet_dx=0 FULLY covers breach) ──
    if _katman_aktif(katmanlar, "tuvalet"):
        tuv: list[str] = [f'<g id="s304-tuvalet" transform="translate({tuvalet_dx:.1f}, 0)">']
        # Ground contact shadow moving with the steel toilet unit
        tuv.append('<ellipse cx="574" cy="450" rx="164" ry="20" fill="#05090D" opacity="0.72"/>')

        # Fox River stainless-steel combo sink/toilet unit (x: 404..744, y: 152..442 -> 100% covers breach at dx=0!)
        tuv.append('<g transform="translate(404, 152)">')
        # Back-side flange (depth thickness)
        tuv.append(f'<polygon points="318,14 342,4 342,276 318,288" fill="url(#{p}_steel_dark)" stroke="{INK}" stroke-width="2.0" stroke-linejoin="round"/>')
        # Main brushed stainless body (wide enough to completely seal the wall breach at dx=0)
        tuv.append(f'<path d="M10,16 L318,14 L318,288 L26,290 L10,272 Z" fill="url(#{p}_steel)" stroke="{INK}" stroke-width="2.2" stroke-linejoin="round"/>')
        # Top basin deck
        tuv.append(f'<polygon points="4,16 322,14 342,4 32,6" fill="#B6CAD6" stroke="{INK}" stroke-width="2.0" stroke-linejoin="round"/>')
        # Recessed oval sink basin
        tuv.append(f'<ellipse cx="168" cy="12" rx="74" ry="8.5" fill="#516570" stroke="{INK}" stroke-width="1.6"/>')
        tuv.append('<ellipse cx="168" cy="13" rx="56" ry="5" fill="#2E3B42"/>')
        # Push-button faucet spout
        tuv.append(f'<path d="M162,8 L162,-8 Q162,-18 178,-18 L190,-18 L190,-10 L172,-10 L172,8 Z" fill="#D5E5EE" stroke="{INK}" stroke-width="1.7"/>')
        # Integrated stainless toilet bowl protruding forward
        tuv.append(f'<path d="M84,132 L248,132 L236,226 Q226,262 166,264 Q106,262 96,226 Z" fill="url(#{p}_steel)" stroke="{INK}" stroke-width="2.2"/>')
        tuv.append(f'<ellipse cx="166" cy="132" rx="84" ry="23" fill="#CEE0EA" stroke="{INK}" stroke-width="2.2"/>')
        tuv.append(f'<ellipse cx="166" cy="132" rx="60" ry="15" fill="#465863" stroke="{INK}" stroke-width="1.6"/>')
        tuv.append('<ellipse cx="166" cy="136" rx="42" ry="8" fill="#1F2B32"/>')
        # Specular metallic vertical highlights + 4 corner Allen bolt mounting holes
        tuv.append('<rect x="34" y="30" width="16" height="240" fill="#FFFFFF" opacity="0.22"/>')
        tuv.append('<rect x="276" y="30" width="10" height="240" fill="#223038" opacity="0.24"/>')
        for bx, by in ((28, 34), (298, 34), (28, 266), (298, 266)):
            tuv.append(f'<circle cx="{bx}" cy="{by}" r="6.5" fill="#182228" stroke="{INK}" stroke-width="1.6"/>')
            tuv.append(f'<circle cx="{bx}" cy="{by}" r="3.0" fill="#6D8694"/>')
        tuv.append("</g>")
        tuv.append("</g>")
        parts.append("".join(tuv))

    # ── LAYER 3C (R18-HAREKET): civata (Hero rotating hexagonal Allen bolt #11121147) ──
    if _katman_aktif(katmanlar, "civata"):
        civ: list[str] = ['<g id="s304-civata">']
        civ.append('<g transform="translate(432, 412) rotate(-14)">')
        # Soft cyan/white halo behind hero bolt
        civ.append(f'<ellipse cx="0" cy="0" rx="108" ry="64" fill="url(#{p}_cyan_glow)"/>')
        # Threaded bolt shank extending right-upward
        civ.append(f'<rect x="18" y="-17" width="96" height="34" rx="4" fill="url(#{p}_bolt_thread)" stroke="{INK}" stroke-width="2.2"/>')
        # Smooth machined collar band where serial #11121147 is laser-engraved
        civ.append('<rect x="20" y="-15.5" width="46" height="31" fill="#C7DCE8" opacity="0.88"/>')
        civ.append('<line x1="66" y1="-16" x2="66" y2="16" stroke="#2A3A44" stroke-width="1.6"/>')
        # Helical thread grooves starting cleanly after engraved shoulder
        for tx in range(70, 108, 7):
            civ.append(f'<path d="M{tx},-16 L{tx + 3.5},16" fill="none" stroke="#223038" stroke-width="2.1"/>')
            civ.append(f'<path d="M{tx + 1.8},-15 L{tx + 5.2},15" fill="none" stroke="#EFFAFF" stroke-width="1.0" opacity="0.70"/>')
        # Washer collar
        civ.append(f'<ellipse cx="18" cy="0" rx="11" ry="30" fill="#7D98A8" stroke="{INK}" stroke-width="2.0"/>')
        # Hexagonal Bolt Head (3D faceted bright steel)
        civ.append(
            f'<polygon points="-54,-34 10,-38 22,0 10,38 -54,34 -68,0" '
            f'fill="url(#{p}_bolt_metal)" stroke="{INK}" stroke-width="2.4" stroke-linejoin="round"/>'
        )
        # Front hex face
        civ.append(
            f'<polygon points="-46,-26 -6,-26 10,0 -6,26 -46,26 -60,0" '
            f'fill="#D9EEF8" stroke="{INK}" stroke-width="1.8" stroke-linejoin="round"/>'
        )
        # Recessed hexagonal Allen socket in center
        civ.append(
            f'<polygon points="-36,-14 -16,-14 -6,0 -16,14 -36,14 -46,0" '
            f'fill="#1B2830" stroke="{INK}" stroke-width="1.8" stroke-linejoin="round"/>'
        )
        civ.append(
            '<polygon points="-32,-10 -18,-10 -11,0 -18,10 -32,10 -39,0" '
            'fill="#0B1217" stroke="#536F7E" stroke-width="1.0"/>'
        )
        # Specular gleam star on top-left bevel
        civ.append('<path d="M-46,-26 L-36,-26 M-41,-31 L-41,-21" fill="none" stroke="#FFFFFF" stroke-width="2.2" stroke-linecap="round"/>')
        # Crisp serial stamp engraved on clean machined shoulder
        civ.append(
            '<text x="29" y="3.5" font-family="Consolas, DejaVu Sans Mono, monospace" font-size="7.6" '
            'font-weight="bold" fill="#101A22" letter-spacing="0.1">11121147</text>'
        )
        # Rotation motion arcs around bolt head
        civ.append(
            f'<path d="M-76,-34 A56,56 0 0,1 -20,-54" fill="none" stroke="{PLAN}" stroke-width="2.2" '
            f'stroke-dasharray="6,4" stroke-linecap="round"/>'
        )
        civ.append(f'<polygon points="-14,-54 -25,-60 -23,-48" fill="{PLAN}"/>')
        civ.append(
            f'<path d="M-76,34 A56,56 0 0,0 -20,54" fill="none" stroke="{PLAN}" stroke-width="2.2" '
            f'stroke-dasharray="6,4" stroke-linecap="round"/>'
        )
        civ.append(f'<polygon points="-80,28 -83,40 -71,36" fill="{PLAN}"/>')
        civ.append("</g>")
        civ.append("</g>")
        parts.append("".join(civ))

    # ── LAYER 3 (legacy compat): sahne (subtle non-duplicating floor anchor when requested alone) ──
    if katmanlar is not None and "sahne" in katmanlar:
        parts.append('<g id="s304-sahne"><line x1="120" y1="452" x2="840" y2="452" stroke="#0C141A" stroke-width="1.4" opacity="0.45"/></g>')

    # ── LAYER 4: plan (#7FE6FF Cyan CAD Underground Pipe Network + Callouts + DAYS LEFT: 14) ──
    if _katman_aktif(katmanlar, "plan"):
        plan_el: list[str] = ['<g id="s304-plan">']
        # Cyan CAD blueprint wireframe aligned directly to the hidden breach behind the toilet
        plan_el.append(
            f'<g fill="none" stroke="{PLAN}" stroke-linecap="round" stroke-linejoin="round">'
            f'<path d="M448,202 L538,202 L592,258 L592,356 L696,356" stroke-width="2.2" opacity="0.88"/>'
            f'<path d="M515,174 L515,386 L662,386" stroke-width="1.8" stroke-dasharray="6,4" opacity="0.78"/>'
            f'<path d="M438,258 L704,258" stroke-width="2.0" opacity="0.85"/>'
            f'<path d="M592,258 L674,258 L674,334 L732,334" stroke-width="1.6" stroke-dasharray="4,4" opacity="0.76"/>'
            f'<circle cx="592" cy="258" r="22" stroke-width="1.5" stroke-dasharray="5,3" opacity="0.86"/>'
            f'<circle cx="592" cy="258" r="7" stroke-width="1.8"/>'
            f'</g>'
        )
        # Glowing CAD nodes
        for nx, ny in ((515, 202), (592, 258), (592, 356), (674, 334), (515, 386)):
            plan_el.append(f'<circle cx="{nx}" cy="{ny}" r="3.6" fill="{PLAN_CORE}" stroke="{PLAN}" stroke-width="1.2"/>')

        # Underground shaft CAD labels
        plan_el.append(
            f'<g font-family="Consolas, DejaVu Sans Mono, monospace" fill="{PLAN}">'
            f'<rect x="466" y="106" width="214" height="24" rx="3" fill="#07131D" fill-opacity="0.84" stroke="{PLAN}" stroke-width="1.1"/>'
            f'<text x="476" y="122" font-size="10.5" font-weight="bold" letter-spacing="0.8">PIPE SHAFT A · HIDDEN HEART</text>'
            f'<path d="M572,130 L572,174" fill="none" stroke="{PLAN}" stroke-width="1.2" stroke-dasharray="3,3"/>'
            f'<text x="606" y="246" font-size="9.5" fill="{PLAN_CORE}">INFIRMARY MAIN</text>'
            f'<text x="606" y="349" font-size="9.0" opacity="0.88">SUB-TUNNEL -14FT</text>'
            f'</g>'
        )

        # Hero Allen Bolt CAD callout badge
        plan_el.append(
            f'<g>'
            f'<path d="M462,456 L512,486 L534,486" fill="none" stroke="{PLAN}" stroke-width="1.6"/>'
            f'<circle cx="462" cy="456" r="3.5" fill="{PLAN_CORE}"/>'
            f'<rect x="534" y="464" width="248" height="46" rx="4" fill="#07131D" fill-opacity="0.90" stroke="{PLAN}" stroke-width="1.4"/>'
            f'<text x="546" y="483" font-family="Consolas, DejaVu Sans Mono, monospace" font-size="13" '
            f'font-weight="bold" fill="{PLAN_CORE}" letter-spacing="0.8">HEX BOLT #11121147</text>'
            f'<text x="546" y="500" font-family="Consolas, DejaVu Sans Mono, monospace" font-size="9.5" '
            f'fill="{PLAN}" letter-spacing="0.5">SCHWEITZER ALLEN · WALL BREACH OPEN</text>'
            f'</g>'
        )

        # Top-right Countdown HUD
        plan_el.append(_days_hud(728, 18, "DAYS LEFT: 14", accent=RED_ALERT, sub_text="EXECUTION COUNTDOWN"))
        plan_el.append("</g>")
        parts.append("".join(plan_el))

    # ── LAYER 5: onplan (Foreground cell bar edge, floating concrete dust & vignette) ──
    if _katman_aktif(katmanlar, "onplan"):
        onplan: list[str] = ['<g id="s304-onplan">']
        # Dark out-of-focus foreground prison bar on far right framing the cell
        onplan.append('<rect x="912" y="0" width="20" height="540" fill="#070C10" opacity="0.82"/>')
        onplan.append('<rect x="916" y="0" width="3" height="540" fill="#2A3E4A" opacity="0.35"/>')
        # Subtle concrete dust motes suspended in fluorescent beam
        for _ in range(36):
            dx = rng.uniform(120, 860)
            dy = rng.uniform(50, 480)
            dr = rng.uniform(0.9, 2.3)
            onplan.append(f'<circle cx="{dx:.1f}" cy="{dy:.1f}" r="{dr:.1f}" fill="#D6F4FF" opacity="{rng.uniform(0.14, 0.42):.2f}"/>')
        onplan.append(f'<rect x="0" y="0" width="960" height="540" fill="url(#{p}_vig)"/>')
        onplan.append("</g>")
        parts.append("".join(onplan))

    return defs, "".join(parts)


# =============================================================================
# SCENE 3.05: RIOT AIR VENT RESCUE (DAYS LEFT: 9)
# =============================================================================
def set_305_isyan_kanal(
    katmanlar: set[str] | list[str] | None = None,
) -> tuple[str, str]:
    """Below: fiery orange-red riot corridor with heat haze and wall thermometer
    spiking to 104°F · RIOT. Above: opened galvanized steel air vent where locked
    Michael v3 reaches down and pulls locked Sara v2 up by the hand.
    R4-PARALAKS STRICT: Both characters (heads, necks, torsos, arms, clasping hands)
    and the vent lip they contact are drawn inside the single `s305-sahne` layer.
    """
    rng = random.Random(305)
    p = _uid("s305")

    defs = f"""
    <linearGradient id="{p}_riot_bg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#141C24"/>
      <stop offset="34%" stop-color="#2D1B1A"/>
      <stop offset="68%" stop-color="#7A2616"/>
      <stop offset="100%" stop-color="#D94B1C"/>
    </linearGradient>
    <radialGradient id="{p}_fire_glow" cx="0.50" cy="0.96" r="0.68">
      <stop offset="0%" stop-color="#FFE082" stop-opacity="0.88"/>
      <stop offset="32%" stop-color="#FF6A24" stop-opacity="0.62"/>
      <stop offset="68%" stop-color="#A82014" stop-opacity="0.28"/>
      <stop offset="100%" stop-color="#220A08" stop-opacity="0.0"/>
    </radialGradient>
    <linearGradient id="{p}_ceil" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#0D141C"/>
      <stop offset="65%" stop-color="#1A2530"/>
      <stop offset="100%" stop-color="#2B2120"/>
    </linearGradient>
    <linearGradient id="{p}_duct_steel" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#263440"/>
      <stop offset="28%" stop-color="#4A5E6E"/>
      <stop offset="52%" stop-color="#6A8194"/>
      <stop offset="78%" stop-color="#364654"/>
      <stop offset="100%" stop-color="#1A242D"/>
    </linearGradient>
    <linearGradient id="{p}_duct_in" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#070E15"/>
      <stop offset="60%" stop-color="#13212E"/>
      <stop offset="100%" stop-color="#203242"/>
    </linearGradient>
    <linearGradient id="{p}_wall_side" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#261816"/>
      <stop offset="60%" stop-color="#47231A"/>
      <stop offset="100%" stop-color="#6B2E1C"/>
    </linearGradient>
    <linearGradient id="{p}_mercury" x1="0" y1="1" x2="0" y2="0">
      <stop offset="0%" stop-color="#B0121E"/>
      <stop offset="55%" stop-color="#FF2A32"/>
      <stop offset="100%" stop-color="#FF8C42"/>
    </linearGradient>
    <linearGradient id="{p}_m_shirt" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#7D9FC1"/>
      <stop offset="52%" stop-color="#5B7B9C"/>
      <stop offset="100%" stop-color="#374E67"/>
    </linearGradient>
    <linearGradient id="{p}_s_coat" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F7F3EC"/>
      <stop offset="55%" stop-color="#DDD6CA"/>
      <stop offset="100%" stop-color="#A89A8D"/>
    </linearGradient>
    <radialGradient id="{p}_hand_rim" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0%" stop-color="#FFE4A8" stop-opacity="0.48"/>
      <stop offset="55%" stop-color="#FF7D3B" stop-opacity="0.16"/>
      <stop offset="100%" stop-color="#FF7D3B" stop-opacity="0.0"/>
    </radialGradient>
    <radialGradient id="{p}_vig" cx="0.5" cy="0.46" r="0.70">
      <stop offset="54%" stop-color="#000000" stop-opacity="0.0"/>
      <stop offset="100%" stop-color="#070405" stop-opacity="0.72"/>
    </radialGradient>
    <clipPath id="{p}_m_forearm_clip">
      <path d="M491,188 L524,192 L506,262 L482,258 Z"/>
    </clipPath>
    """

    parts: list[str] = []

    # ── LAYER 1: uzak (Fiery riot corridor below + ceiling depth + smoke haze) ──
    if _katman_aktif(katmanlar, "uzak"):
        uzak: list[str] = ['<g id="s305-uzak">']
        uzak.append(f'<rect x="0" y="0" width="960" height="540" fill="url(#{p}_riot_bg)"/>')
        uzak.append(f'<rect x="0" y="0" width="960" height="178" fill="url(#{p}_ceil)"/>')
        uzak.append(f'<rect x="0" y="160" width="960" height="380" fill="url(#{p}_fire_glow)"/>')

        # Receding cellblock tier railings in fiery distance
        uzak.append(
            '<g stroke="#2C0F0B" stroke-width="2.4" opacity="0.65">'
            '<line x1="160" y1="312" x2="800" y2="312"/>'
            '<line x1="190" y1="366" x2="770" y2="366"/>'
            '<line x1="140" y1="430" x2="820" y2="430"/>'
            '</g>'
        )
        # Vertical distant cellblock bars silhouetted against fire glow
        bars = []
        for bx in range(180, 790, 34):
            bars.append(f'<line x1="{bx}" y1="250" x2="{bx}" y2="540" stroke="#240C09" stroke-width="3.2" opacity="0.52"/>')
        uzak.append("".join(bars))

        # Stylized rising fire tongues & heat smoke plumes at bottom (non-violent atmospheric glow)
        uzak.append(
            '<path d="M0,540 L0,468 Q92,430 168,466 Q244,410 332,456 Q418,392 496,446 '
            'Q588,396 668,452 Q756,412 848,460 Q912,434 960,464 L960,540 Z" '
            'fill="#FF7D2E" opacity="0.45"/>'
        )
        uzak.append(
            '<path d="M0,540 L0,492 Q120,464 220,496 Q340,452 464,488 Q592,448 724,492 '
            'Q844,462 960,496 L960,540 Z" fill="#FFD166" opacity="0.42"/>'
        )
        # Rising smoke billows
        for sx, sy, sr, op in (
            (190, 396, 78, 0.24),
            (310, 342, 68, 0.18),
            (690, 384, 84, 0.24),
            (790, 320, 64, 0.18),
        ):
            uzak.append(f'<circle cx="{sx}" cy="{sy}" r="{sr}" fill="#1E0E0D" opacity="{op}"/>')
        uzak.append("</g>")
        parts.append("".join(uzak))

    # ── LAYER 2: orta (Corridor walls, glowing 104°F · RIOT thermometer, ceiling duct housing) ──
    if _katman_aktif(katmanlar, "orta"):
        orta: list[str] = ['<g id="s305-orta">']
        # Left & right corridor side walls framing the shaft
        orta.append(f'<polygon points="0,148 214,214 214,540 0,540" fill="url(#{p}_wall_side)" stroke="{INK}" stroke-width="2.2"/>')
        orta.append(f'<polygon points="960,148 756,214 756,540 960,540" fill="url(#{p}_wall_side)" stroke="{INK}" stroke-width="2.2"/>')

        # Ceiling concrete soffit & upper structural beam
        orta.append(f'<polygon points="0,0 960,0 960,152 756,214 214,214 0,152" fill="url(#{p}_ceil)" stroke="{INK}" stroke-width="2.0"/>')
        # Recessed overhead steel air-vent duct housing (back & interior)
        orta.append(f'<polygon points="264,0 696,0 676,174 284,174" fill="url(#{p}_duct_in)" stroke="{INK}" stroke-width="2.4"/>')
        # Interior duct ribs
        for dy in (34, 78, 124):
            orta.append(f'<line x1="276" y1="{dy}" x2="684" y2="{dy}" stroke="#283C4D" stroke-width="1.8" opacity="0.72"/>')
        # Hinged metal vent grille swung open to the left
        orta.append(
            f'<polygon points="284,172 162,216 146,184 268,144" '
            f'fill="url(#{p}_duct_steel)" stroke="{INK}" stroke-width="2.2" stroke-linejoin="round"/>'
        )
        for g_i in range(5):
            gx1 = 176 + g_i * 20
            gy1 = 204 - g_i * 7
            orta.append(f'<line x1="{gx1}" y1="{gy1}" x2="{gx1 - 12}" y2="{gy1 - 24}" stroke="#121B22" stroke-width="2.0"/>')

        # ── WALL THERMOMETER ON LEFT WALL (104°F · RIOT) ──
        orta.append('<g transform="translate(56, 232)">')
        # Glowing red heat halo around thermometer
        orta.append('<ellipse cx="44" cy="112" rx="68" ry="118" fill="#FF3824" opacity="0.22"/>')
        # Metal thermometer backplate
        orta.append(f'<rect x="10" y="6" width="68" height="202" rx="12" fill="#2A1E1E" stroke="{INK}" stroke-width="2.4"/>')
        orta.append('<rect x="16" y="12" width="56" height="190" rx="8" fill="#D9D4C8" stroke="#5A4A44" stroke-width="1.4"/>')
        # Scale tick marks & labels
        for t_i, ty in enumerate(range(30, 166, 15)):
            is_hot = ty <= 60
            tw = 13 if t_i % 2 == 0 else 8
            col = "#C81D25" if is_hot else "#383533"
            orta.append(f'<line x1="50" y1="{ty}" x2="{50 + tw}" y2="{ty}" stroke="{col}" stroke-width="1.8"/>')
        orta.append('<text x="20" y="34" font-family="Consolas, monospace" font-size="9" font-weight="bold" fill="#C81D25">110</text>')
        orta.append('<text x="20" y="64" font-family="Consolas, monospace" font-size="9" font-weight="bold" fill="#C81D25">100</text>')
        orta.append('<text x="24" y="94" font-family="Consolas, monospace" font-size="8.5" fill="#423E3B">90</text>')
        orta.append('<text x="24" y="124" font-family="Consolas, monospace" font-size="8.5" fill="#423E3B">80</text>')
        orta.append('<text x="24" y="154" font-family="Consolas, monospace" font-size="8.5" fill="#423E3B">70</text>')
        # Glass tube & maxed-out glowing red mercury column
        orta.append(f'<rect x="38" y="22" width="10" height="148" rx="5" fill="#ECEAE4" stroke="#4D4845" stroke-width="1.4"/>')
        orta.append(f'<rect x="40" y="32" width="6" height="142" rx="3" fill="url(#{p}_mercury)"/>')
        # Mercury bulb at bottom
        orta.append(f'<circle cx="43" cy="178" r="14" fill="url(#{p}_mercury)" stroke="{INK}" stroke-width="1.8"/>')
        orta.append('<circle cx="39" cy="173" r="4" fill="#FFD4B8" opacity="0.72"/>')
        # Crisp callout badge next to thermometer: 104°F · RIOT
        orta.append(
            f'<rect x="2" y="216" width="136" height="32" rx="4" fill="#180808" fill-opacity="0.92" '
            f'stroke="#FF442E" stroke-width="1.6"/>'
            f'<text x="12" y="237" font-family="Segoe UI, Arial, sans-serif" font-size="15" '
            f'font-weight="bold" fill="#FF7348" letter-spacing="0.8">104°F · RIOT</text>'
        )
        orta.append("</g>")
        orta.append("</g>")
        parts.append("".join(orta))

    # ── LAYER 3: sahne (R4-PARALAKS CLEAN: Locked Michael v3 + Locked Sara v2 + Vent Lip) ──
    if _katman_aktif(katmanlar, "sahne"):
        sahne: list[str] = ['<g id="s305-sahne">']

        # Highlight glow behind the clasping hands
        sahne.append(f'<ellipse cx="486" cy="276" rx="84" ry="62" fill="url(#{p}_hand_rim)"/>')

        # ── 1) MICHAEL v3 (Slim athletic ay_yetiskin_v3 proportions + Collar-Over-Neck) ──
        # Bracing left arm (slim athletic shoulder -> bicep -> elbow -> forearm gripping vent rim)
        sahne.append(
            f'<path d="M418,124 C396,128 374,138 362,152 C354,160 354,168 358,174 '
            f'L382,174 C384,166 388,160 396,155 C408,150 418,148 428,146 Z" '
            f'fill="url(#{p}_m_shirt)" stroke="{INK_CHAR}" stroke-width="2.0" stroke-linejoin="round"/>'
        )
        # Subtle sleeve shading & elbow crease on left bracing arm
        sahne.append(
            '<path d="M372,155 C386,150 404,145 424,142 L427,147 C408,151 394,154 386,160 C382,164 380,169 379,174 L368,174 C369,166 370,160 372,155 Z" '
            'fill="#2F445B" opacity="0.54"/>'
            '<path d="M368,144 C382,135 398,129 416,126" fill="none" stroke="#99B9D6" stroke-width="1.8" opacity="0.45" stroke-linecap="round"/>'
        )
        # Rolled left sleeve cuff (hand drawn AFTER vent front lip so fingers physically grip the steel edge)
        sahne.append(
            f'<path d="M356,162 C365,160 375,160 384,163 L382,170 C374,168 364,168 356,170 Z" '
            f'fill="#7A9CBE" stroke="{INK_CHAR}" stroke-width="1.6" stroke-linejoin="round"/>'
        )

        # Slim athletic torso leaning forward out of duct (shoulder width ~98px matching ay_yetiskin_v3)
        sahne.append(
            f'<path d="M416,122 C426,112 442,108 462,108 C482,108 498,113 508,124 '
            f'C513,134 512,150 506,166 C492,173 474,175 456,174 C438,173 424,168 416,158 '
            f'C412,146 412,132 416,122 Z" '
            f'fill="url(#{p}_m_shirt)" stroke="{INK_CHAR}" stroke-width="2.1" stroke-linejoin="round"/>'
        )
        # Athletic chest shading, subtle fabric folds & warm lower riot bounce light
        sahne.append(
            '<path d="M418,154 C434,164 456,168 486,166 C498,165 505,160 508,154 '
            'C506,166 490,174 456,174 C436,173 422,167 417,158 Z" fill="#2A3E54" opacity="0.56"/>'
            '<path d="M424,136 C436,144 448,149 458,151 M498,136 C488,144 478,149 468,152" '
            'fill="none" stroke="#2A3E54" stroke-width="1.4" opacity="0.62" stroke-linecap="round"/>'
            '<path d="M426,166 C448,172 480,172 498,164" fill="none" stroke="#FF8F4A" stroke-width="2.0" opacity="0.46" stroke-linecap="round"/>'
        )

        # Locked Michael v3 Head (drawn BEFORE front collar so Collar-Over-Neck seals the neck seamlessly!)
        sahne.append(
            f'<g transform="translate(460, 88) rotate(11) scale(0.43)">'
            f'{K.michael_kafa("3q", ifade="kararli", look=0.35, boyun=True)}'
            f'</g>'
        )

        # COLLAR-OVER-NECK: White undershirt V-neck & Fox River blue shirt collar cleanly covering neck base
        sahne.append(
            f'<path d="M442,122 Q460,132 478,123 L460,147 Z" fill="#EEEAE1" stroke="{INK_CHAR}" stroke-width="1.5" stroke-linejoin="round"/>'
            f'<path d="M435,118 C439,131 446,142 456,151 L460,143 L444,122 Z" '
            f'fill="#6F90B2" stroke="{INK_CHAR}" stroke-width="1.6" stroke-linejoin="round"/>'
            f'<path d="M487,120 C481,133 474,143 464,151 L460,143 L476,123 Z" '
            f'fill="#5C7D9E" stroke="{INK_CHAR}" stroke-width="1.6" stroke-linejoin="round"/>'
            f'<line x1="460" y1="145" x2="459" y2="173" stroke="#253648" stroke-width="1.4"/>'
            f'<circle cx="460" cy="158" r="1.8" fill="#E8E4DA" stroke="{INK_CHAR}" stroke-width="0.9"/>'
            # Fox River chest pocket & crisp 94941 stamp (zero overlap with collar)
            f'<path d="M420,151 L443,153 L442,164 Q431,165 419,161 Z" fill="none" stroke="#283B50" stroke-width="1.2" opacity="0.78"/>'
            f'<text x="418" y="148" font-family="Consolas, monospace" font-size="7.6" '
            f'font-weight="bold" fill="#E8E4DA" opacity="0.95">94941</text>'
        )

        # Michael's reaching right arm (slim athletic deltoid/bicep + rolled sleeve + tattooed forearm)
        sahne.append(
            f'<path d="M496,120 C510,122 522,128 524,142 C526,156 523,170 519,184 '
            f'L492,180 C492,164 493,148 494,134 C495,128 495,123 496,120 Z" '
            f'fill="url(#{p}_m_shirt)" stroke="{INK_CHAR}" stroke-width="2.0" stroke-linejoin="round"/>'
        )
        # Soft sleeve shading & elbow crease on right reaching arm
        sahne.append(
            '<path d="M512,128 C520,142 520,162 515,182 L506,181 C510,162 511,144 506,128 Z" fill="#2E4359" opacity="0.46"/>'
            '<path d="M497,148 C506,152 514,152 521,149 M495,164 C504,167 512,167 519,165" '
            'fill="none" stroke="#243547" stroke-width="1.3" opacity="0.62" stroke-linecap="round"/>'
        )
        # Rolled cuff
        sahne.append(
            f'<path d="M489,175 C501,176 512,178 523,181 L521,191 C510,189 499,187 487,185 Z" '
            f'fill="#7D9FC1" stroke="{INK_CHAR}" stroke-width="1.7" stroke-linejoin="round"/>'
        )
        # Exposed athletic forearm with locked K.michael_dovme_onkol architectural tattoo (R1 compliant)
        sahne.append(
            f'<path d="M491,188 L520,192 L505,260 L484,257 Z" '
            f'fill="#D5A687" stroke="{INK_CHAR}" stroke-width="2.0" stroke-linejoin="round"/>'
        )
        sahne.append(
            f'<g clip-path="url(#{p}_m_forearm_clip)">'
            f'<path d="M512,190 L522,192 L507,260 L499,259 Z" fill="#BC8A6B" opacity="0.62"/>'
            f'<g transform="translate(502, 190) rotate(10)" opacity="0.88">'
            f'{K.michael_dovme_onkol(w=28, h=68, plan=False)}'
            f'</g>'
            f'</g>'
        )
        sahne.append(
            f'<path d="M491,188 L520,192 L505,260 L484,257 Z" '
            f'fill="none" stroke="{INK_CHAR}" stroke-width="2.0" stroke-linejoin="round"/>'
        )

        # ── 2) SARA v2 (BOTH ARMS COMPLETE & ANATOMICAL + Collar-Over-Neck!) ──
        # Sara's dark trousers & lower coat hem
        sahne.append(
            f'<path d="M438,464 L464,464 L468,540 L430,540 Z" fill="#252E3A" stroke="{INK_CHAR}" stroke-width="2.0"/>'
            f'<path d="M478,464 L506,464 L516,540 L482,540 Z" fill="#1D252F" stroke="{INK_CHAR}" stroke-width="2.0"/>'
        )
        # Sara's slim white doctor coat body
        sahne.append(
            f'<path d="M434,372 Q472,360 508,374 L524,474 Q472,486 422,474 Z" '
            f'fill="url(#{p}_s_coat)" stroke="{INK_CHAR}" stroke-width="2.1" stroke-linejoin="round"/>'
        )
        # Warm orange rim light on Sara's coat from riot fire below
        sahne.append(
            '<path d="M426,470 Q472,482 518,471" fill="none" stroke="#FF8A42" stroke-width="3.4" opacity="0.68"/>'
        )
        # Coat pockets & front vertical seam
        sahne.append(
            f'<path d="M434,436 L456,436 L455,462 L433,462 Z M488,436 L510,436 L512,462 L489,462 Z" '
            f'fill="none" stroke="#8C857A" stroke-width="1.3" opacity="0.8"/>'
        )

        # SARA'S COMPLETE LEFT ARM (Shoulder -> upper coat sleeve -> bent elbow -> lower sleeve -> wrist -> 5-fingered hand!)
        sahne.append(
            f'<path d="M436,374 C418,382 400,400 392,418 C388,428 392,442 404,458 '
            f'L422,450 C414,438 412,430 415,422 C422,410 432,400 442,394 Z" '
            f'fill="url(#{p}_s_coat)" stroke="{INK_CHAR}" stroke-width="2.0" stroke-linejoin="round"/>'
        )
        # Soft sleeve fold & elbow crease on Sara's left arm
        sahne.append(
            '<path d="M396,424 C404,422 411,422 416,426 M402,438 C409,436 415,436 419,439" '
            'fill="none" stroke="#8E867B" stroke-width="1.3" opacity="0.75" stroke-linecap="round"/>'
        )
        # Sara's left wrist & complete anatomical 5-fingered balancing hand
        sahne.append(
            f'<g stroke="{INK_CHAR}" stroke-width="1.65" stroke-linejoin="round" stroke-linecap="round">'
            f'<path d="M405,457 L421,450 L427,464 C429,470 424,475 416,474 L407,469 Z" fill="#E8C1A6"/>'
            # Thumb (inner right side)
            f'<path d="M423,456 C431,458 434,465 429,469 C426,471 423,468 423,464" fill="#E8C1A6"/>'
            # Four tapered fingers balancing outward
            f'<path d="M419,472 L423,484 C424,487 420,488 418,485 L414,473" fill="#E8C1A6"/>'
            f'<path d="M414,472 L416,486 C417,489 412,490 411,486 L409,472" fill="#E8C1A6"/>'
            f'<path d="M409,470 L409,483 C409,486 405,486 405,483 L405,469" fill="#E8C1A6"/>'
            f'<path d="M405,467 L403,477 C402,480 399,479 399,476 L402,464" fill="#D5A687"/>'
            f'</g>'
        )

        # SARA'S RIGHT ARM (reaching naturally upward to clasp Michael's hand)
        sahne.append(
            f'<path d="M498,374 C516,356 518,334 514,316 L496,314 C495,336 490,352 480,368 Z" '
            f'fill="url(#{p}_s_coat)" stroke="{INK_CHAR}" stroke-width="2.0" stroke-linejoin="round"/>'
        )
        sahne.append(
            f'<path d="M496,316 L512,318 C510,296 506,282 501,274 L488,274 C492,288 494,302 496,316 Z" '
            f'fill="#E8C1A6" stroke="{INK_CHAR}" stroke-width="1.9" stroke-linejoin="round"/>'
        )

        # Locked Sara v2 Head (drawn BEFORE front collar/stethoscope so Collar-Over-Neck seals cleanly!)
        sahne.append(
            f'<g transform="translate(468, 336) rotate(-7) scale(0.41)">'
            f'{K.sara_kafa("3q", ifade="endise", look=-0.22, boyun=True)}'
            f'</g>'
        )

        # COLLAR-OVER-NECK FOR SARA: Petrol-blue scrub V-neck + crisp white coat lapels + stethoscope
        sahne.append(
            f'<path d="M454,368 Q471,376 488,368 L472,414 Z" fill="#4E6B7B" stroke="{INK_CHAR}" stroke-width="1.5" stroke-linejoin="round"/>'
            f'<path d="M444,368 L455,368 L466,418 L454,412 Z" fill="#F6F3EC" stroke="{INK_CHAR}" stroke-width="1.5" stroke-linejoin="round"/>'
            f'<path d="M498,368 L487,368 L477,418 L489,412 Z" fill="#E8E3D8" stroke="{INK_CHAR}" stroke-width="1.5" stroke-linejoin="round"/>'
            f'<path d="M466,418 L465,474 M477,418 L482,474" fill="none" stroke="{INK_CHAR}" stroke-width="1.6" stroke-linecap="round"/>'
            f'<path d="M450,369 Q445,404 455,426 M492,369 Q498,402 490,422" '
            f'fill="none" stroke="#232A30" stroke-width="3.0" stroke-linecap="round"/>'
            f'<circle cx="455" cy="430" r="5.2" fill="#C4CED6" stroke="{INK_CHAR}" stroke-width="1.4"/>'
        )

        # ── 3) ANATOMICAL CLASPING HANDS (Rescue wrist-grip: Michael & Sara locking hands) ──
        sahne.append(
            f'<g stroke="{INK_CHAR}" stroke-width="1.75" stroke-linejoin="round" stroke-linecap="round">'
            # Sara's palm & thumb gripping the upper side of Michael's wrist
            f'<path d="M487,276 Q478,262 484,248 Q490,242 496,248 L504,264 L503,278 Z" fill="#E8C1A6"/>'
            # Sara's fingers wrapping over Michael's wrist (tapered natural fingers)
            f'<path d="M482,254 Q494,250 504,255 Q506,260 496,261 L483,260 Z" fill="#F2D2BC"/>'
            f'<path d="M483,261 Q495,258 505,262 Q506,267 496,268 L484,267 Z" fill="#E8C1A6"/>'
            # Michael's hand wrapping downward around Sara's wrist/palm
            f'<path d="M482,256 Q478,270 484,284 Q494,292 505,284 Q510,274 507,262 Z" fill="#D5A687"/>'
            # Michael's three visible curled fingers locking firmly around Sara's wrist
            f'<path d="M484,266 Q495,264 506,268 Q507,273 496,274 L484,272 Z" fill="#DDA989"/>'
            f'<path d="M484,273 Q495,271 505,275 Q506,280 495,281 L484,279 Z" fill="#D5A687"/>'
            f'<path d="M486,280 Q494,279 503,282 Q503,287 494,287 L486,285 Z" fill="#C49375"/>'
            # Michael's thumb counter-locking on left edge
            f'<path d="M482,258 Q476,265 480,275 Q485,277 487,270 Z" fill="#C49375"/>'
            f'</g>'
        )

        # ── 4) VENT FRONT LIP (Contacted by Michael's torso & bracing hand — same sahne layer!) ──
        sahne.append(
            f'<path d="M266,166 L410,166 L410,180 L266,180 Z '
            f'M534,166 L694,166 L694,180 L534,180 Z" '
            f'fill="url(#{p}_duct_steel)" stroke="{INK}" stroke-width="2.2" stroke-linejoin="round"/>'
        )
        # Rivets along steel vent flange
        for rx in (284, 326, 368, 560, 608, 656):
            sahne.append(f'<circle cx="{rx}" cy="173" r="2.4" fill="#A2BACB" stroke="{INK}" stroke-width="0.9"/>')
        # Michael's left hand physically wrapping OVER the steel vent lip (same sahne layer!)
        sahne.append(
            f'<g stroke="{INK_CHAR}" stroke-width="1.7" stroke-linejoin="round">'
            f'<path d="M355,167 C352,174 354,182 361,184 L381,183 C387,181 388,173 382,167 C374,165 363,165 355,167 Z" fill="#D5A687"/>'
            f'<path d="M361,174 L361,183 M368,174 L368,183 M375,174 L375,182" fill="none" stroke="#7A503B" stroke-width="1.15"/>'
            f'</g>'
        )

        sahne.append("</g>")
        parts.append("".join(sahne))

    # ── LAYER 4: plan (Cyan CAD air-vent extraction path + DAYS LEFT: 9 HUD) ──
    if _katman_aktif(katmanlar, "plan"):
        plan_el: list[str] = ['<g id="s305-plan">']
        # Blueprint duct extraction route (cleanly routed beside Michael's arm, never cutting across it)
        plan_el.append(
            f'<g fill="none" stroke="{PLAN}" stroke-linecap="round" stroke-linejoin="round">'
            f'<path d="M294,158 L294,54 L668,54 L668,158" stroke-width="1.5" stroke-dasharray="6,4" opacity="0.68"/>'
            f'<path d="M532,268 L566,268 L566,136 L618,54 L668,54" stroke-width="2.0" opacity="0.86"/>'
            f'<circle cx="494" cy="268" r="32" stroke-width="1.4" stroke-dasharray="5,4" opacity="0.72"/>'
            f'</g>'
        )
        plan_el.append(f'<polygon points="676,54 662,48 662,60" fill="{PLAN}"/>')
        plan_el.append(
            f'<rect x="26" y="20" width="234" height="38" rx="4" fill="#07121C" fill-opacity="0.88" '
            f'stroke="{PLAN}" stroke-width="1.3"/>'
            f'<text x="36" y="36" font-family="Consolas, DejaVu Sans Mono, monospace" font-size="10.5" '
            f'font-weight="bold" fill="{PLAN_CORE}" letter-spacing="0.7">VENT SHAFT B-04 · EXTRACTION</text>'
            f'<text x="36" y="50" font-family="Consolas, DejaVu Sans Mono, monospace" font-size="9" '
            f'fill="{PLAN}">CLEAR RIOT FLOOR -> INFIRMARY ROOF</text>'
        )
        plan_el.append(_days_hud(728, 18, "DAYS LEFT: 9", accent=FIRE_ORANGE, sub_text="FOX RIVER · LOCKDOWN"))
        plan_el.append("</g>")
        parts.append("".join(plan_el))

    # ── LAYER 5: onplan (Rising embers, sparks, heat haze & cinematic vignette) ──
    if _katman_aktif(katmanlar, "onplan"):
        onplan: list[str] = ['<g id="s305-onplan">']
        # Rising glowing embers from the riot corridor below
        for _ in range(44):
            ex = rng.uniform(30, 930)
            ey = rng.uniform(220, 534)
            er = rng.uniform(1.1, 3.0)
            col = FIRE_GOLD if rng.random() > 0.45 else FIRE_ORANGE
            onplan.append(f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="{er:.1f}" fill="{col}" opacity="{rng.uniform(0.35, 0.85):.2f}"/>')
        # Subtle heat shimmer wave lines near bottom
        onplan.append(
            '<path d="M180,492 Q240,478 300,492 T420,492 M560,484 Q620,470 680,484 T800,484" '
            'fill="none" stroke="#FFB948" stroke-width="1.6" opacity="0.28"/>'
        )
        onplan.append(f'<rect x="0" y="0" width="960" height="540" fill="url(#{p}_vig)"/>')
        onplan.append("</g>")
        parts.append("".join(onplan))

    return defs, "".join(parts)


# =============================================================================
# SCENE 3.06: EXECUTION NIGHT & RED PHONE (DAYS LEFT: 00 -> +14 DAYS)
# =============================================================================
def set_306_idam_telefon(
    katmanlar: set[str] | list[str] | None = None,
) -> tuple[str, str]:
    """Ice-cold blue-grey death row corridor (ZERO blood/violence/chair close-up).
    Far background: distant Lincoln silhouette walking slowly in dim backlit mist.
    Lower center: shorted blue electrical cable spark dying out.
    Front right: hand frozen on the heavy wall breaker switch.
    Front left: bright red court phone ringing with radiating sound waves
    ('STAY GRANTED · +14 DAYS') and top-right HUD 'DAYS LEFT: 00 -> +14 DAYS'.
    R4-PARALAKS STRICT: Frozen hand + arm + breaker lever AND red phone + receiver
    all live inside the single `s306-sahne` layer.
    """
    rng = random.Random(306)
    p = _uid("s306")

    defs = f"""
    <linearGradient id="{p}_ice_bg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#070E17"/>
      <stop offset="48%" stop-color="#111E2D"/>
      <stop offset="100%" stop-color="#0A131E"/>
    </linearGradient>
    <radialGradient id="{p}_door_mist" cx="0.50" cy="0.45" r="0.34">
      <stop offset="0%" stop-color="#B6DEF5" stop-opacity="0.54"/>
      <stop offset="42%" stop-color="#487394" stop-opacity="0.24"/>
      <stop offset="100%" stop-color="#0B1520" stop-opacity="0.0"/>
    </radialGradient>
    <linearGradient id="{p}_wall_l" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#152332"/>
      <stop offset="70%" stop-color="#1E3042"/>
      <stop offset="100%" stop-color="#0F1B27"/>
    </linearGradient>
    <linearGradient id="{p}_wall_r" x1="1" y1="0" x2="0" y2="0">
      <stop offset="0%" stop-color="#142230"/>
      <stop offset="70%" stop-color="#1D2F40"/>
      <stop offset="100%" stop-color="#0E1924"/>
    </linearGradient>
    <linearGradient id="{p}_floor_ice" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#0D1824"/>
      <stop offset="45%" stop-color="#172838"/>
      <stop offset="100%" stop-color="#081018"/>
    </linearGradient>
    <radialGradient id="{p}_spark_glow" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.95"/>
      <stop offset="28%" stop-color="#7FE6FF" stop-opacity="0.72"/>
      <stop offset="68%" stop-color="#227BFF" stop-opacity="0.22"/>
      <stop offset="100%" stop-color="#0A1B33" stop-opacity="0.0"/>
    </radialGradient>
    <radialGradient id="{p}_red_glow" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0%" stop-color="#FF3244" stop-opacity="0.55"/>
      <stop offset="52%" stop-color="#C81828" stop-opacity="0.18"/>
      <stop offset="100%" stop-color="#14080A" stop-opacity="0.0"/>
    </radialGradient>
    <linearGradient id="{p}_phone_body" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FF4A56"/>
      <stop offset="38%" stop-color="#D91E2C"/>
      <stop offset="78%" stop-color="#9E111C"/>
      <stop offset="100%" stop-color="#5E080F"/>
    </linearGradient>
    <linearGradient id="{p}_breaker_box" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#4A5C6B"/>
      <stop offset="50%" stop-color="#2E3C47"/>
      <stop offset="100%" stop-color="#1A232B"/>
    </linearGradient>
    <linearGradient id="{p}_hand_cold" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#DFC4B2"/>
      <stop offset="55%" stop-color="#B99884"/>
      <stop offset="100%" stop-color="#7E6254"/>
    </linearGradient>
    <radialGradient id="{p}_vig" cx="0.5" cy="0.48" r="0.68">
      <stop offset="52%" stop-color="#000000" stop-opacity="0.0"/>
      <stop offset="100%" stop-color="#03070D" stop-opacity="0.74"/>
    </radialGradient>
    """

    parts: list[str] = []

    # ── LAYER 1: uzak (Ice-cold corridor perspective + distant backlit Lincoln silhouette) ──
    if _katman_aktif(katmanlar, "uzak"):
        uzak: list[str] = ['<g id="s306-uzak">']
        uzak.append(f'<rect x="0" y="0" width="960" height="540" fill="url(#{p}_ice_bg)"/>')
        # Corridor perspective floor & ceiling
        uzak.append(f'<polygon points="354,322 606,322 960,540 0,540" fill="url(#{p}_floor_ice)"/>')
        uzak.append('<polygon points="354,158 606,158 960,0 0,0" fill="#0B1520"/>')
        # Receding cold fluorescent ceiling strips
        for fy, fw, fh, op in ((150, 128, 4, 0.82), (118, 178, 5, 0.68), (74, 246, 6, 0.56), (22, 340, 8, 0.45)):
            uzak.append(f'<rect x="{480 - fw / 2:.1f}" y="{fy}" width="{fw}" height="{fh}" rx="2" fill="#C9ECFF" opacity="{op}"/>')

        # Back corridor backlit steel gate & cold mist
        uzak.append(f'<rect x="354" y="158" width="252" height="164" fill="#182C3E" stroke="{INK}" stroke-width="2.0"/>')
        uzak.append(f'<ellipse cx="480" cy="246" rx="164" ry="118" fill="url(#{p}_door_mist)"/>')
        # Gate vertical bars at far end
        for gx in range(374, 594, 18):
            uzak.append(f'<line x1="{gx}" y1="158" x2="{gx}" y2="322" stroke="#0C1722" stroke-width="2.2" opacity="0.65"/>')

        # Distant walking Lincoln silhouette (broad shoulders, calm solemn walk in dim mist)
        uzak.append('<g opacity="0.88">')
        # Subtle escort guard silhouettes further back on left & right
        uzak.append(
            '<path d="M424,234 Q424,222 432,222 Q440,222 440,234 L444,264 L440,316 L434,316 L432,282 L428,316 L422,316 L420,264 Z" '
            'fill="#122130" opacity="0.58"/>'
        )
        uzak.append(
            '<path d="M520,234 Q520,222 528,222 Q536,222 536,234 L540,264 L536,316 L530,316 L528,282 L524,316 L518,316 L516,264 Z" '
            'fill="#122130" opacity="0.58"/>'
        )
        # Lincoln center silhouette (broad shoulders, buzzcut head, walking stride)
        uzak.append(
            '<path d="M471,218 Q471,202 480,202 Q489,202 489,218 L488,224 '
            'L502,230 Q506,236 504,264 L498,274 L494,324 L485,324 L481,284 '
            'L475,324 L466,324 L462,272 L456,264 Q454,236 458,230 L472,224 Z" '
            'fill="#09121B"/>'
        )
        # Soft cold rim light along Lincoln's shoulders
        uzak.append(
            '<path d="M458,230 L472,224 Q480,202 488,224 L502,230" '
            'fill="none" stroke="#8AC2DF" stroke-width="1.3" opacity="0.55"/>'
        )
        # Wet corridor floor reflection of Lincoln & backlight
        uzak.append('<ellipse cx="480" cy="356" rx="68" ry="22" fill="#70A8CC" opacity="0.16"/>')
        uzak.append('<polygon points="468,324 492,324 498,378 462,378" fill="#060D14" opacity="0.42"/>')
        uzak.append("</g>")
        uzak.append("</g>")
        parts.append("".join(uzak))

    # ── LAYER 2: orta (Left & right steel/concrete walls, floor conduit & breaker box housing) ──
    if _katman_aktif(katmanlar, "orta"):
        orta: list[str] = ['<g id="s306-orta">']
        # Left & right corridor side walls
        orta.append(f'<polygon points="0,0 354,158 354,322 0,540" fill="url(#{p}_wall_l)" stroke="{INK}" stroke-width="2.2"/>')
        orta.append(f'<polygon points="960,0 606,158 606,322 960,540" fill="url(#{p}_wall_r)" stroke="{INK}" stroke-width="2.2"/>')

        # Perspective wall seam lines
        for sy_l, sy_r in ((120, 200), (240, 240), (360, 282)):
            orta.append(f'<line x1="0" y1="{sy_l}" x2="354" y2="{sy_r}" stroke="#0D1722" stroke-width="1.4" opacity="0.62"/>')
            orta.append(f'<line x1="960" y1="{sy_l}" x2="606" y2="{sy_r}" stroke="#0D1722" stroke-width="1.4" opacity="0.62"/>')

        # Floor electrical conduit pipe leading from right breaker wall to shorted spark point
        orta.append(
            f'<path d="M960,468 L628,468 Q562,468 532,452 L486,438" '
            f'fill="none" stroke="{INK}" stroke-width="13" stroke-linecap="round"/>'
        )
        orta.append(
            '<path d="M960,468 L628,468 Q562,468 532,452 L486,438" '
            'fill="none" stroke="#374C5E" stroke-width="8.5" stroke-linecap="round"/>'
        )
        # Exposed frayed copper/blue power cable emerging from conduit
        orta.append(
            '<path d="M488,438 Q464,432 454,446 M484,442 Q468,454 452,456" '
            'fill="none" stroke="#1E3548" stroke-width="3.6" stroke-linecap="round"/>'
        )

        # Left wall shelf/mount for the Red Court Telephone
        orta.append(
            f'<polygon points="18,376 268,366 286,396 18,412" '
            f'fill="#22313F" stroke="{INK}" stroke-width="2.2" stroke-linejoin="round"/>'
        )
        orta.append(
            f'<polygon points="18,412 286,396 286,416 18,434" '
            f'fill="#121C26" stroke="{INK}" stroke-width="2.0" stroke-linejoin="round"/>'
        )
        # Wall plaque on lower shelf front edge (clear of coiled cord & ringing waves)
        orta.append(
            f'<rect x="76" y="406" width="166" height="22" rx="3" fill="#182430" stroke="#4D667B" stroke-width="1.3"/>'
            f'<text x="86" y="420" font-family="Consolas, DejaVu Sans Mono, monospace" font-size="9.5" '
            f'font-weight="bold" fill="#D9E8F5" letter-spacing="0.8">GOVERNOR · COURT LINE</text>'
        )

        # Right wall heavy steel breaker box (housing backplate)
        orta.append(
            f'<rect x="668" y="154" width="212" height="252" rx="6" '
            f'fill="url(#{p}_breaker_box)" stroke="{INK}" stroke-width="2.4"/>'
        )
        orta.append(
            f'<rect x="682" y="168" width="184" height="224" rx="4" '
            f'fill="#1C262F" stroke="#4F6373" stroke-width="1.4"/>'
        )
        # Warning header plate on breaker box
        orta.append(
            '<rect x="698" y="180" width="152" height="26" rx="2" fill="#B58A28" stroke="#11161D" stroke-width="1.4"/>'
            '<text x="708" y="197" font-family="Consolas, monospace" font-size="11" font-weight="bold" fill="#11161D">HIGH VOLTAGE · MAIN</text>'
        )
        # Status LEDs on breaker box (one red OFF, one flickering blue FAULT)
        orta.append(f'<circle cx="718" cy="226" r="6" fill="#47161B" stroke="{INK}" stroke-width="1.4"/>')
        orta.append(f'<circle cx="746" cy="226" r="6" fill="{PLAN}" stroke="{INK}" stroke-width="1.4"/>')
        orta.append('<text x="760" y="230" font-family="Consolas, monospace" font-size="9.5" fill="#9BB6CC">GRID FAULT</text>')
        orta.append("</g>")
        parts.append("".join(orta))

    # ── LAYER 3: sahne (Static foreground scene: Spark + Red Phone Base + Breaker Slot) ──
    if _katman_aktif(katmanlar, "sahne"):
        sahne: list[str] = ['<g id="s306-sahne">']

        # ── 1) SHORTED BLUE ELECTRICAL SPARK (Lower center, dying out) ──
        sahne.append(f'<ellipse cx="458" cy="448" rx="92" ry="52" fill="url(#{p}_spark_glow)"/>')
        # Jagged electric blue-white arc bolts
        sahne.append(
            '<path d="M454,446 L442,424 L452,418 L438,396 '
            'M458,448 L478,426 L470,418 L492,402 '
            'M456,450 L432,456 L422,468 '
            'M460,452 L486,460 L498,476" '
            'fill="none" stroke="#7FE6FF" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>'
        )
        sahne.append(
            '<path d="M454,446 L446,430 M458,448 L474,432 M456,450 L440,456" '
            'fill="none" stroke="#FFFFFF" stroke-width="1.5" stroke-linecap="round"/>'
        )
        sahne.append('<circle cx="456" cy="448" r="7" fill="#FFFFFF"/>')
        # Thin wispy smoke curling up from dying short circuit
        sahne.append(
            '<path d="M456,434 Q444,410 460,388 Q472,368 456,348" '
            'fill="none" stroke="#9AC2DB" stroke-width="3.2" opacity="0.28" stroke-linecap="round"/>'
        )

        # ── 2) BRIGHT RED COURT PHONE BASE (Front left; handset separated into `telefon_ahize`) ──
        sahne.append('<g transform="translate(46, 256)">')
        sahne.append(f'<ellipse cx="106" cy="78" rx="134" ry="96" fill="url(#{p}_red_glow)"/>')
        # Coiled red phone cord
        sahne.append(
            '<path d="M22,94 Q6,112 18,128 Q30,144 18,160 Q8,176 28,186" '
            f'fill="none" stroke="{INK}" stroke-width="8" stroke-linecap="round"/>'
        )
        sahne.append(
            '<path d="M22,94 Q6,112 18,128 Q30,144 18,160 Q8,176 28,186" '
            'fill="none" stroke="#C81826" stroke-width="4.4" stroke-linecap="round"/>'
        )
        # Main retro red telephone base
        sahne.append(
            f'<path d="M36,68 L178,68 L196,136 L18,136 Z" '
            f'fill="url(#{p}_phone_body)" stroke="{INK}" stroke-width="2.4" stroke-linejoin="round"/>'
        )
        # Specular glossy red highlight on base
        sahne.append('<path d="M48,76 L166,76 L172,92 L42,92 Z" fill="#FF7E88" opacity="0.34"/>')
        # Cradle prongs
        sahne.append(
            f'<rect x="64" y="48" width="14" height="22" rx="3" fill="#B51420" stroke="{INK}" stroke-width="1.8"/>'
            f'<rect x="136" y="48" width="14" height="22" rx="3" fill="#B51420" stroke="{INK}" stroke-width="1.8"/>'
        )
        # Center rotary/direct dial plate (glossy ivory/chrome)
        sahne.append(f'<circle cx="107" cy="108" r="22" fill="#E8EEF2" stroke="{INK}" stroke-width="2.0"/>')
        sahne.append('<circle cx="107" cy="108" r="14" fill="#B81622" stroke="#11161D" stroke-width="1.2"/>')
        sahne.append('<text x="95" y="111" font-family="Consolas, monospace" font-size="8" font-weight="bold" fill="#FFFFFF">STAY</text>')
        # Radiating ringing sound waves around red phone
        for rad, op, sw in ((88, 0.92, 2.8), (110, 0.66, 2.2), (132, 0.38, 1.6)):
            sahne.append(
                f'<path d="M{107 - rad * 0.72:.1f},{46 - rad * 0.62:.1f} A{rad},{rad} 0 0,1 {107 + rad * 0.72:.1f},{46 - rad * 0.62:.1f}" '
                f'fill="none" stroke="#FF5A66" stroke-width="{sw}" opacity="{op}" stroke-linecap="round"/>'
            )
            sahne.append(
                f'<path d="M{107 + rad * 0.86:.1f},{24:.1f} A{rad},{rad} 0 0,1 {107 + rad * 0.92:.1f},{88:.1f}" '
                f'fill="none" stroke="{PLAN}" stroke-width="{sw * 0.85:.1f}" opacity="{op * 0.85:.2f}" stroke-linecap="round"/>'
            )
        sahne.append("</g>")

        # ── 3) WALL BREAKER SLOT HOUSING (Lever & hand separated into `salter_kol`) ──
        sahne.append(f'<rect x="726" y="254" width="96" height="118" rx="6" fill="#101820" stroke="#4D6273" stroke-width="1.8"/>')
        sahne.append('<rect x="762" y="268" width="24" height="90" rx="4" fill="#060A0F" stroke="#2D3E4C" stroke-width="1.4"/>')
        sahne.append("</g>")
        parts.append("".join(sahne))

    # ── LAYER 3A (R18-HAREKET): telefon_ahize (Vibrating/bouncing red handset) ──
    if _katman_aktif(katmanlar, "telefon_ahize"):
        ahize: list[str] = ['<g id="s306-telefon-ahize">']
        ahize.append('<g transform="translate(153, 302) rotate(-4)">')
        ahize.append(
            f'<path d="M-86,12 Q-92,-16 -54,-18 L54,-18 Q92,-16 86,12 L74,24 Q58,28 50,14 L46,0 L-46,0 L-50,14 Q-58,28 -74,24 Z" '
            f'fill="url(#{p}_phone_body)" stroke="{INK}" stroke-width="2.4" stroke-linejoin="round"/>'
        )
        ahize.append('<path d="M-56,-11 L56,-11" fill="none" stroke="#FF9BA3" stroke-width="3.2" stroke-linecap="round" opacity="0.68"/>')
        ahize.append("</g>")
        ahize.append("</g>")
        parts.append("".join(ahize))

    # ── LAYER 3B (R18-HAREKET + R4-PARALAKS): salter_kol (Red breaker lever + frozen hand as 1 atomic unit) ──
    if _katman_aktif(katmanlar, "salter_kol"):
        salter: list[str] = ['<g id="s306-salter-kol">']
        # Lever shaft & red insulated T-handle
        salter.append(f'<rect x="766" y="276" width="16" height="44" rx="3" fill="#8EA2B2" stroke="{INK}" stroke-width="1.8"/>')
        salter.append(f'<rect x="734" y="266" width="80" height="22" rx="6" fill="#C42530" stroke="{INK}" stroke-width="2.2"/>')
        salter.append('<line x1="744" y1="272" x2="804" y2="272" stroke="#FF8C94" stroke-width="2.2" opacity="0.58"/>')

        # Officer forearm entering from bottom-right + hand frozen on the breaker handle
        salter.append(
            f'<path d="M960,418 L854,328 L820,368 L918,486 L960,486 Z" '
            f'fill="#1A2533" stroke="{INK_CHAR}" stroke-width="2.3" stroke-linejoin="round"/>'
        )
        salter.append(
            f'<path d="M854,328 L842,318 L810,356 L820,368 Z" '
            f'fill="#C7D4E0" stroke="{INK_CHAR}" stroke-width="1.8" stroke-linejoin="round"/>'
        )
        salter.append(
            f'<path d="M744,284 Q736,294 744,304 Q756,312 770,308 L774,292 Z" '
            f'fill="#A68572" stroke="{INK_CHAR}" stroke-width="1.9" stroke-linejoin="round"/>'
        )
        salter.append(
            f'<path d="M842,318 L816,288 Q806,274 790,272 L750,274 Q742,278 746,290 '
            f'L762,312 Q778,328 796,336 L810,356 Z" '
            f'fill="url(#{p}_hand_cold)" stroke="{INK_CHAR}" stroke-width="2.2" stroke-linejoin="round"/>'
        )
        salter.append(
            '<path d="M764,294 L792,314 M778,292 L804,310 M792,290 L814,306" '
            'fill="none" stroke="#8C6D5D" stroke-width="1.3" opacity="0.58" stroke-linecap="round"/>'
        )
        finger_specs = [
            (745, 261, 13.5, 24),
            (759, 259, 14.0, 26),
            (774, 260, 13.5, 25),
            (788, 263, 12.5, 22),
        ]
        for fx, fy, fw, fh in finger_specs:
            salter.append(
                f'<path d="M{fx},{fy + fh} L{fx},{fy + 6} Q{fx + fw / 2:.1f},{fy - 1} {fx + fw:.1f},{fy + 6} '
                f'L{fx + fw:.1f},{fy + fh} Q{fx + fw / 2:.1f},{fy + fh + 3} {fx},{fy + fh} Z" '
                f'fill="url(#{p}_hand_cold)" stroke="{INK_CHAR}" stroke-width="1.9" stroke-linejoin="round"/>'
            )
            salter.append(
                f'<path d="M{fx + 3},{fy + 11} Q{fx + fw / 2:.1f},{fy + 9.5} {fx + fw - 3:.1f},{fy + 11}" '
                f'fill="none" stroke="#7A5C4E" stroke-width="1.2" stroke-linecap="round"/>'
            )
            salter.append(
                f'<path d="M{fx + 3.5},{fy + 19} Q{fx + fw / 2:.1f},{fy + 18} {fx + fw - 3.5:.1f},{fy + 19}" '
                f'fill="none" stroke="#8F7060" stroke-width="1.0" opacity="0.7" stroke-linecap="round"/>'
            )
        salter.append("</g>")
        parts.append("".join(salter))

    # ── LAYER 4: plan (STAY GRANTED · +14 DAYS callout, CAD fault line, DAYS LEFT: 00 -> +14 DAYS) ──
    if _katman_aktif(katmanlar, "plan"):
        plan_el: list[str] = ['<g id="s306-plan">']

        # Dramatic STAY GRANTED · +14 DAYS callout above the ringing red phone
        plan_el.append(
            f'<g transform="translate(26, 134)">'
            f'<rect x="0" y="0" width="292" height="58" rx="5" fill="#18080C" fill-opacity="0.92" '
            f'stroke="#FF4655" stroke-width="1.8"/>'
            f'<rect x="0" y="0" width="6" height="58" rx="2" fill="#FF3244"/>'
            f'<circle cx="20" cy="18" r="4" fill="#FF3244"/>'
            f'<text x="32" y="22" font-family="Consolas, DejaVu Sans Mono, monospace" font-size="10.5" '
            f'font-weight="bold" fill="#FF9AA2" letter-spacing="0.9">COURT DIRECT LINE · RINGING</text>'
            f'<text x="16" y="46" font-family="Segoe UI, Arial, sans-serif" font-size="19" '
            f'font-weight="bold" fill="#FFFFFF" letter-spacing="0.9">STAY GRANTED · +14 DAYS</text>'
            f'</g>'
        )
        # Leader line from STAY GRANTED badge to ringing phone
        plan_el.append('<path d="M152,192 L152,262" fill="none" stroke="#FF5A66" stroke-width="1.6" stroke-dasharray="4,3"/>')

        # Cyan CAD circuit line linking shorted spark to frozen breaker switch
        plan_el.append(
            f'<path d="M462,448 L544,448 L646,356 L724,356" '
            f'fill="none" stroke="{PLAN}" stroke-width="1.7" stroke-dasharray="5,4" opacity="0.86"/>'
            f'<circle cx="462" cy="448" r="18" fill="none" stroke="{PLAN}" stroke-width="1.4" stroke-dasharray="4,3" opacity="0.80"/>'
            f'<rect x="366" y="484" width="234" height="32" rx="4" fill="#07121C" fill-opacity="0.88" stroke="{PLAN}" stroke-width="1.2"/>'
            f'<text x="378" y="504" font-family="Consolas, DejaVu Sans Mono, monospace" font-size="10.5" '
            f'font-weight="bold" fill="{PLAN_CORE}" letter-spacing="0.6">POWER SHORTED · SWITCH HALTED</text>'
        )

        # Top-right HUD: DAYS LEFT: 00 -> +14 DAYS
        plan_el.append(
            f'<g transform="translate(626, 18)">'
            f'<rect x="0" y="0" width="316" height="58" rx="5" fill="#08101A" fill-opacity="0.92" '
            f'stroke="{PLAN}" stroke-width="1.7"/>'
            f'<rect x="0" y="0" width="5" height="58" rx="2" fill="{PLAN}"/>'
            f'<text x="16" y="18" font-family="Consolas, DejaVu Sans Mono, monospace" font-size="9.5" '
            f'font-weight="bold" fill="#9CB6CC" letter-spacing="0.9">EXECUTION NIGHT · STAY ORDER</text>'
            # Struck-through DAYS LEFT: 00
            f'<text x="16" y="44" font-family="Segoe UI, Arial, sans-serif" font-size="18" '
            f'font-weight="bold" fill="#E65260" opacity="0.85">DAYS LEFT: 00</text>'
            f'<line x1="14" y1="38" x2="146" y2="38" stroke="#FF3B4D" stroke-width="2.4"/>'
            # Cyan arrow -> +14 DAYS
            f'<path d="M156,38 L182,38 M176,32 L183,38 L176,44" fill="none" stroke="{PLAN}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<rect x="192" y="22" width="112" height="28" rx="4" fill="#0E2A3A" stroke="{PLAN}" stroke-width="1.4"/>'
            f'<text x="202" y="42" font-family="Segoe UI, Arial, sans-serif" font-size="18" '
            f'font-weight="bold" fill="{PLAN_CORE}" letter-spacing="0.8">+14 DAYS</text>'
            f'</g>'
        )

        plan_el.append("</g>")
        parts.append("".join(plan_el))

    # ── LAYER 5: onplan (Cold corridor air motes, spark particles & vignette) ──
    if _katman_aktif(katmanlar, "onplan"):
        onplan: list[str] = ['<g id="s306-onplan">']
        # Tiny bright blue sparks flying from the short circuit
        for _ in range(18):
            ang = rng.uniform(-math.pi, 0.25)
            dist = rng.uniform(16, 86)
            sx = 456 + math.cos(ang) * dist
            sy = 448 + math.sin(ang) * dist * 0.72
            onplan.append(
                f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="{rng.uniform(1.0, 2.4):.1f}" '
                f'fill="#B8F3FF" opacity="{rng.uniform(0.45, 0.92):.2f}"/>'
            )
        # Faint cold dust motes in corridor light
        for _ in range(28):
            dx = rng.uniform(80, 880)
            dy = rng.uniform(40, 480)
            onplan.append(f'<circle cx="{dx:.1f}" cy="{dy:.1f}" r="{rng.uniform(0.8, 1.8):.1f}" fill="#B8DDF2" opacity="{rng.uniform(0.10, 0.28):.2f}"/>')
        onplan.append(f'<rect x="0" y="0" width="960" height="540" fill="url(#{p}_vig)"/>')
        onplan.append("</g>")
        parts.append("".join(onplan))

    return defs, "".join(parts)


# =============================================================================
# RENDERING & PRESENTATION CARD BUILDERS (1280x720 SET + R13 200% CROPS)
# =============================================================================
def _sahne_svg(fn, w: int = 1920, h: int = 1080, katmanlar=None) -> str:
    defs, body = fn(katmanlar)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {W_SCENE} {H_SCENE}">'
        f"<defs>{defs}</defs>{body}</svg>"
    )


def _render_scene_pil(fn, w: int = 1920, h: int = 1080, katmanlar=None) -> Image.Image:
    svg_str = _sahne_svg(fn, w=w, h=h, katmanlar=katmanlar)
    png_bytes = resvg_py.svg_to_bytes(svg_string=svg_str)
    return Image.open(io.BytesIO(png_bytes)).convert("RGBA")


def _load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/calibrib.ttf" if bold else "C:/Windows/Fonts/calibri.ttf",
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
          <stop offset="0%" stop-color="#0A121E"/>
          <stop offset="50%" stop-color="#101A29"/>
          <stop offset="100%" stop-color="#070D16"/>
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
    print("Rendering 3 Act III scenes (3.04, 3.05, 3.06) at 1920x1080...")
    img_304 = _render_scene_pil(lambda k: set_304_duvar_civata(k, tuvalet_dx=-295.0), 1920, 1080)
    img_305 = _render_scene_pil(set_305_isyan_kanal, 1920, 1080)
    img_306 = _render_scene_pil(set_306_idam_telefon, 1920, 1080)

    # =========================================================================
    # OUTPUT 1: SET PRESENTATION CARD (1280 x 720 — 100% ENGLISH)
    # =========================================================================
    canvas = _draw_card_bg(1280, 720)
    draw = ImageDraw.Draw(canvas)

    f_title = _load_font(20, bold=True)
    f_sub = _load_font(12, bold=False)
    f_card_t = _load_font(13, bold=True)
    f_card_s = _load_font(11, bold=False)
    f_small = _load_font(10, bold=False)

    draw.text((24, 14), "MICHAEL SCOFIELD  ·  ACT III CELL WALL, RIOT RESCUE & EXECUTION NIGHT", fill="#EBF3FA", font=f_title)
    draw.text(
        (24, 39),
        "STYLE B+A HYBRID (CINEMATIC 2D + CYAN BLUEPRINT VISION)  ·  SCENES 3.04 – 3.06",
        fill="#7E97B0",
        font=f_sub,
    )
    top_swatches = [
        ("#384B53", "CELL"),
        ("#FF6A24", "RIOT"),
        ("#1D2F40", "ICE HALL"),
        ("#E52432", "RED LINE"),
        ("#7FE6FF", "CAD PLAN"),
    ]
    sx_top = 808
    for col, lbl in top_swatches:
        draw.rounded_rectangle((sx_top, 18, sx_top + 14, 32), radius=3, fill=col, outline="#3B536D", width=1)
        draw.text((sx_top + 19, 19), lbl, fill="#9BB2C8", font=f_small)
        sx_top += 90
    draw.line((24, 58, 1256, 58), fill="#213247", width=1)

    # --- TOP-LEFT PANEL: 3.04 ALLEN BOLT & HIDDEN HEART ---
    _draw_panel_box(draw, (22, 68, 630, 366))
    t304 = img_304.resize((448, 252), Image.Resampling.LANCZOS)
    canvas.paste(t304, (34, 98), t304)
    draw.rectangle((34, 98, 34 + 448, 98 + 252), outline="#2E455E", width=1)
    draw.text((34, 76), "01 · 3.04 ALLEN BOLT & HIDDEN HEART", fill="#7FE6FF", font=f_card_t)
    draw.text((314, 78), "DAYS LEFT: 14 · Wall Breach", fill="#8AA3BC", font=f_card_s)
    ix = 492
    draw.text((ix, 98), "PALETTE", fill="#7FE6FF", font=f_small)
    _draw_swatches(draw, ix, 114, ["#1C262B", "#4B5B63", "#C4DAE6", "#E63244", "#7FE6FF"], size=18, gap=5)
    draw.text((ix, 146), "KEY ELEMENTS", fill="#9BB2C8", font=f_small)
    for k_i, item in enumerate(
        [
            "• Pulled-Out Steel Sink",
            "• Hex Bolt #11121147",
            "• Concrete Wall Breach",
            "• Underground Pipe Shaft",
            "• Cyan CAD Network",
        ]
    ):
        draw.text((ix, 164 + k_i * 19), item, fill="#D5E2EE", font=f_card_s)
    draw.text((ix, 272), "KEY LIGHTING", fill="#9BB2C8", font=f_small)
    draw.text((ix, 288), "Cold fluorescent + cyan", fill="#8AE6FF", font=f_card_s)
    draw.text((ix, 314), "LAYERS (5)", fill="#9BB2C8", font=f_small)
    draw.text((ix, 330), "uzak · orta · sahne\nplan · onplan", fill="#8AA3BC", font=f_small)

    # --- TOP-RIGHT PANEL: 3.05 RIOT AIR VENT RESCUE ---
    _draw_panel_box(draw, (648, 68, 1256, 366))
    t305 = img_305.resize((448, 252), Image.Resampling.LANCZOS)
    canvas.paste(t305, (660, 98), t305)
    draw.rectangle((660, 98, 660 + 448, 98 + 252), outline="#2E455E", width=1)
    draw.text((660, 76), "02 · 3.05 RIOT AIR VENT RESCUE", fill="#FF8C42", font=f_card_t)
    draw.text((906, 78), "DAYS LEFT: 9 · 104°F RIOT", fill="#D99878", font=f_card_s)
    ix2 = 1118
    draw.text((ix2, 98), "PALETTE", fill="#7FE6FF", font=f_small)
    _draw_swatches(draw, ix2, 114, ["#1B2630", "#7A2616", "#FF6A24", "#EDEAE2", "#7FE6FF"], size=18, gap=5)
    draw.text((ix2, 146), "KEY ELEMENTS", fill="#9BB2C8", font=f_small)
    for k_i, item in enumerate(
        [
            "• 104°F Wall Thermometer",
            "• Locked Michael v3 Pull",
            "• Locked Sara v2 Rescue",
            "• Opened Steel Air Vent",
            "• R4 Single-Layer Clean",
        ]
    ):
        draw.text((ix2, 164 + k_i * 19), item, fill="#D5E2EE", font=f_card_s)
    draw.text((ix2, 272), "KEY LIGHTING", fill="#9BB2C8", font=f_small)
    draw.text((ix2, 288), "Fire glow vs steel duct", fill="#FF9852", font=f_card_s)
    draw.text((ix2, 314), "LAYERS (5)", fill="#9BB2C8", font=f_small)
    draw.text((ix2, 330), "uzak · orta · sahne\nplan · onplan", fill="#8AA3BC", font=f_small)

    # --- BOTTOM WIDE PANEL: 3.06 EXECUTION NIGHT & RED PHONE ---
    _draw_panel_box(draw, (22, 378, 1256, 704))
    t306 = img_306.resize((512, 288), Image.Resampling.LANCZOS)
    canvas.paste(t306, (34, 404), t306)
    draw.rectangle((34, 404, 34 + 512, 404 + 288), outline="#35516E", width=1)
    draw.text((34, 384), "03 · 3.06 EXECUTION NIGHT & RED PHONE", fill="#FF6B78", font=f_card_t)
    draw.text((322, 386), "DAYS LEFT: 00 -> +14 DAYS · Zero Violence", fill="#9AC6DF", font=f_card_s)

    rx = 564
    draw.text((rx, 404), "PALETTE (ICE CORRIDOR, SHORT SPARK & RED COURT PHONE)", fill="#7FE6FF", font=f_small)
    _draw_swatches(draw, rx, 422, ["#070E17", "#1D2F40", "#E52432", "#7FE6FF", "#E4FCFF"], size=22, gap=7)
    draw.text((rx, 458), "KEY ELEMENTS", fill="#9BB2C8", font=f_small)
    for k_i, item in enumerate(
        [
            "• Ice-cold corridor & distant backlit Lincoln silhouette",
            "• Dying blue short-circuit cable spark on corridor floor",
            "• Hand frozen on wall breaker lever (single sahne layer)",
            "• Ringing Red Court Phone: STAY GRANTED · +14 DAYS",
        ]
    ):
        draw.text((rx, 476 + k_i * 21), item, fill="#E3ECF5", font=f_card_s)
    draw.text((rx, 572), "SUSPENSE & BOUNDARY", fill="#9BB2C8", font=f_small)
    draw.text(
        (rx, 590),
        "Zero blood, gore, or chair close-up. Maximum tension\n"
        "built through cold mist, shorted grid spark, frozen\n"
        "hand on the switch, and the ringing red stay phone.",
        fill="#C9D8E6",
        font=f_card_s,
    )
    draw.text((rx, 650), "LAYERS (5)", fill="#9BB2C8", font=f_small)
    draw.text((rx, 666), "s306-uzak · s306-orta · s306-sahne · s306-plan · s306-onplan", fill="#8AA3BC", font=f_small)

    draw.line((880, 404, 880, 692), fill="#233447", width=1)
    tx = 898
    draw.text((tx, 404), "ACT III ARC & R4-PARALAKS SPEC", fill="#7FE6FF", font=f_card_t)
    notes = [
        (
            "3.04 -> 3.05 -> 3.06 PROGRESSION",
            "From breaking behind the cell wall (14 days) through\n"
            "rescuing Sara in the 104°F riot (9 days) to the\n"
            "eleventh-hour stay of execution (00 -> +14 days).",
        ),
        (
            "R4-PARALAKS STRICT COMPLIANCE",
            "All character heads, torsos, limbs & contacted\n"
            "props (Michael+Sara+vent lip; hand+breaker lever)\n"
            "stay locked in the single `sahne` depth layer.",
        ),
        (
            "LOCKED ASSETS & CLEAN SVG",
            "Embeds K.michael_kafa (v3) & K.sara_kafa (v2)\n"
            "without touching karakter.py. 100% English text\n"
            "and explicit fill='none' on all stroked paths.",
        ),
    ]
    ny = 432
    for heading, body_txt in notes:
        draw.text((tx, ny), heading, fill="#F6C367" if "PROGRESSION" in heading else "#9EC5DE", font=f_small)
        draw.text((tx, ny + 16), body_txt, fill="#C5D5E4", font=f_card_s)
        ny += 86

    out_main = OUT_DIR / f"b3_set_duvar_idam_{versiyon}.png"
    canvas.convert("RGB").save(out_main, quality=95)

    # =========================================================================
    # OUTPUT 2: R13 200% ZOOM QUALITY CONTROL CARD (1280 x 720 — 4 PANELS)
    # =========================================================================
    r13 = _draw_card_bg(1280, 720)
    d13 = ImageDraw.Draw(r13)
    d13.text((24, 13), "R13 · 200% ZOOM QUALITY CONTROL (ACT III WALL, RIOT & EXECUTION NIGHT)", fill="#EBF3FA", font=f_title)
    d13.text(
        (24, 37),
        "1:1 PIXEL CROPS FROM 1920×1080 SOURCE  ·  BOLT, LOCKED MICHAEL+SARA, RED PHONE & BREAKER HAND",
        fill="#7E97B0",
        font=f_sub,
    )
    d13.line((24, 55, 1256, 55), fill="#213247", width=1)

    cw, ch = 600, 264
    crops = [
        (
            img_304,
            (960, 740),
            "1 · 3.04 SLIDING TOILET, WALL BREACH & HEX BOLT (200%)",
            "R18 layers: `duvar_oyuk` behind `tuvalet` (dx=0 sealed, dx=-295 open) + `civata`",
            (22, 66),
        ),
        (
            img_305,
            (920, 270),
            "2 · 3.05 SLIM MICHAEL v3 + COLLAR-OVER-NECK (200%)",
            "Athletic ay_yetiskin_v3 torso, seamless collar-over-neck & bracing left arm",
            (652, 66),
        ),
        (
            img_305,
            (920, 770),
            "3 · 3.05 SARA v2 BOTH ARMS COMPLETE + RESCUE GRIP (200%)",
            "Right arm clasping Michael's wrist + complete left arm & 5-fingered hand",
            (22, 392),
        ),
        (
            img_306,
            (1520, 620),
            "4 · 3.06 R18 `salter_kol` BREAKER LEVER & HAND (200%)",
            "Separated `salter_kol` & `telefon_ahize` layers ready for live animation",
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

    out_r13 = OUT_DIR / "b3_set_duvar_idam_r13.png"
    r13.convert("RGB").save(out_r13, quality=95)
    print(f"Saved:\n  - {out_main}\n  - {out_r13}")
    return out_main, out_r13


if __name__ == "__main__":
    uret_kartlar("v1")
