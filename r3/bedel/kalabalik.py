"""Kalabalık ve ordu üretici + kahraman silahları + cenaze ateşi (kullanıcı 19.11 23:20).
- soldier(seed, ...): 3 temel modelden (BJ, BORG, ROLLO) rastgele türetme. Saç/sakal/giysi rengi, miğfer, kalkan deseni, mızrak ya da balta.
  Her biri model gövdesi (R11); sprite önbelleği sınırlı tutulur (VAR_N varyant).
- army(c, ...): derinlik sıraları (uzakta küçük ve soluk, önde büyük ve net), sancaklar, mızrak ormanı.
- BEARD_AXE: Ragnar'ın süslü sakallı baltası (düğüm işlemeli ağız, gümüş kakma, deri sargı).
- pyre_grand(): dizideki gibi görkemli cenaze yığını (çapraz kütük kafes, oymalı köşe direkleri ve ejder başları,
  çevresinde kalkanlar, otlar ve çiçekler, üstte kefenli beden ve mavi örtü, mezar eşyaları).
"""
import random, math
from art3 import figure
INK = "#1A1410"
HELMET = ('<path d="M-82,-30 Q-84,-120 0,-124 Q84,-120 82,-30 Z" fill="#7A7E84" stroke="#1A1410" stroke-width="6"/>'
          '<path d="M-82,-38 L82,-38" stroke="#5A5E64" stroke-width="12"/><path d="M0,-124 L0,-36" stroke="#5A5E64" stroke-width="10"/>'
          '<rect x="-7" y="-40" width="14" height="44" fill="#6A6E74" stroke="#1A1410" stroke-width="4"/>')
def shield_svg(c1, c2, boss="#8A8A86", style=0):
    pat = {0: f'<path d="M0,-150 L0,150 M-150,0 L150,0" stroke="{c2}" stroke-width="40"/>',
           1: "".join(f'<path d="M0,0 L{150*math.cos(a):.0f},{150*math.sin(a):.0f} A150,150 0 0 1 {150*math.cos(a+0.785):.0f},{150*math.sin(a+0.785):.0f} Z" fill="{c2}"/>' for a in [k * 1.571 for k in range(4)]),
           2: f'<circle r="96" fill="none" stroke="{c2}" stroke-width="34"/>'}[style]
    return (f'<g transform="translate(70,-330) scale(0.62)"><circle r="150" fill="{c1}" stroke="#1A1410" stroke-width="10"/>{pat}'
            f'<circle r="150" fill="none" stroke="#5A5A58" stroke-width="12"/><circle r="34" fill="{boss}" stroke="#1A1410" stroke-width="6"/></g>')
SPEAR = ('<g transform="translate(HX,HY)"><path d="M0,120 L0,-420" stroke="#1A1410" stroke-width="14" stroke-linecap="round"/><path d="M0,120 L0,-420" stroke="#6A5038" stroke-width="8"/>'
         '<path d="M0,-470 L14,-420 L0,-404 L-14,-420 Z" fill="#B8C0C8" stroke="#1A1410" stroke-width="4"/></g>')
TORCH2 = ('<g transform="translate(HX,HY)"><path d="M0,30 L-10,-120" stroke="#1A1410" stroke-width="18" stroke-linecap="round"/><path d="M0,30 L-10,-120" stroke="#5A4028" stroke-width="10" stroke-linecap="round"/>'
          '<path d="M-30,-120 Q-20,-200 -6,-230 Q8,-190 16,-120 Z" fill="#F08A2A" stroke="#1A1410" stroke-width="3"/><path d="M-16,-124 Q-10,-170 -4,-186 Q4,-160 6,-124 Z" fill="#FFD27A"/></g>')
BEARD_AXE = ('<g transform="translate(HX,HY)">'
             '<path d="M8,60 L-40,-300" stroke="#1A1410" stroke-width="22" stroke-linecap="round"/><path d="M8,60 L-40,-300" stroke="#5A3E26" stroke-width="13" stroke-linecap="round"/>'
             + "".join(f'<path d="M{-2 - k*4.6:.0f},{-6 - k*34} l14,8" stroke="#2A1A10" stroke-width="5"/>' for k in range(4))                     # deri sargı
             + '<path d="M-40,-290 Q40,-330 70,-250 Q66,-190 30,-150 Q10,-190 -30,-210 Z" fill="#A8B0B8" stroke="#1A1410" stroke-width="7" stroke-linejoin="round"/>'   # sakallı ağız
             '<path d="M70,-250 Q66,-190 30,-150" stroke="#F0F4F8" stroke-width="5" fill="none"/>'                                                    # keskin kenar parıltısı
             '<path d="M-20,-264 Q14,-280 30,-246 Q20,-214 -8,-222" stroke="#C9A25A" stroke-width="4" fill="none"/>'                                 # altın kakma
             '<path d="M-6,-252 q10,-8 18,2 q-6,12 -16,6 Z" fill="none" stroke="#5A5E64" stroke-width="3"/>'                                         # düğüm işleme
             '<path d="M-48,-300 L-28,-296 L-34,-210 L-52,-214 Z" fill="#7A7E84" stroke="#1A1410" stroke-width="5"/></g>')                          # dil (langet)

BASES = None
def _bases():
    global BASES
    if BASES is None:
        import sys; sys.path[:0] = ["/home/claude/r3/bedel", "/home/claude/r3/veda2"]
        from modeller import ROLLO, BORG
        from kareler import BJv
        BASES = [BJv, BORG, ROLLO]
    return BASES

HAIR = ["#3A2A1E", "#6A4A2E", "#8A6A42", "#A0582E", "#C8A060", "#5A4A3A", "#B8B0A0"]
TUN = ["#4A5A6A", "#5A2E24", "#4A5A34", "#5A4A3A", "#3E4A42", "#6A5A3A", "#3A3E5A"]
SH = [("#8E3B2E", "#D8C8A0"), ("#2F4C6E", "#D8C8A0"), ("#5A6A3A", "#C9A25A"), ("#3A3A38", "#B8302A"), ("#C8B080", "#4A3A2A")]
def soldier_spec(seed, side="ragnar", weapon="spear", torch=False):
    r = random.Random(seed); b = dict(_bases()[seed % 3]); h = r.choice(HAIR)
    sp = dict(b, hair=h, beard_c=h, tunic=r.choice(TUN), cloak=r.choice(["#3A2C20", "#2E3230", "#4A3E32", "#3A3048"]), armring=r.random() < 0.4,
              face_scar=False, knot=False, clasp="", beardless=False, beard_len=r.uniform(0.4, 0.85), no_blush=True)
    if r.random() < 0.55: sp["_head_extra"] = HELMET
    c1, c2 = SH[(seed + (0 if side == "ragnar" else 2)) % len(SH)] if side == "ragnar" else (("#4A5A2A", "#C9A25A") if seed % 2 else ("#5A6A34", "#2A3A1A"))
    if not torch: sp["_body_extra"] = shield_svg(c1, c2, style=seed % 3)
    sp["_arm_up"] = torch or r.random() < 0.3          # çoğu mızrağı yanında dik tutar, bir kısmı kaldırır
    sp["_hand_extra"] = TORCH2 if torch else (SPEAR if weapon == "spear" else BEARD_AXE.replace("#C9A25A", "#8A7A5A"))
    return sp

def pyre_grand(x, y, s=1.0, body=True):
    """Görkemli cenaze yığını. Yerel: taban ortası (0,0)."""
    o = [f'<g transform="translate({x},{y}) scale({s})">', '<ellipse cx="0" cy="10" rx="420" ry="40" fill="#000" opacity="0.35"/>']
    for k in range(7):   # çapraz kütük kafes (kat kat, uçlar dışarı taşar)
        yy = -k * 46; wv = 360 - k * 18
        if k % 2 == 0:
            o.append(f'<g filter="url(#t_ahsap)"><rect x="{-wv}" y="{yy-38}" width="{2*wv}" height="38" rx="18" fill="#5A4430"/></g><rect x="{-wv}" y="{yy-38}" width="{2*wv}" height="38" rx="18" fill="none" stroke="{INK}" stroke-width="5"/>'
                     + "".join(f'<circle cx="{sx*(wv-14)}" cy="{yy-19}" r="15" fill="#8A6A48" stroke="{INK}" stroke-width="4"/><circle cx="{sx*(wv-14)}" cy="{yy-19}" r="6" fill="none" stroke="#5A4028" stroke-width="2"/>' for sx in (-1, 1)))
        else:
            o.append("".join(f'<g filter="url(#t_ahsap)"><ellipse cx="{xx}" cy="{yy-19}" rx="26" ry="22" fill="#6A5038"/></g><ellipse cx="{xx}" cy="{yy-19}" rx="26" ry="22" fill="none" stroke="{INK}" stroke-width="4"/><circle cx="{xx}" cy="{yy-19}" r="9" fill="none" stroke="#4A3420" stroke-width="2"/>' for xx in range(-wv + 30, wv - 10, 70)))
    top = -7 * 46
    for sx in (-1, 1):   # oymalı köşe direkleri + ejder başları + sancak
        px = sx * 380
        o.append(f'<g filter="url(#t_ahsap)"><rect x="{px-18}" y="{top-200}" width="36" height="{-top+200}" fill="#4A3826"/></g><rect x="{px-18}" y="{top-200}" width="36" height="{-top+200}" fill="none" stroke="{INK}" stroke-width="6"/>'
                 + "".join(f'<path d="M{px-14},{yy} q14,-12 28,0 q-14,12 -28,0" stroke="#2A1C10" stroke-width="4" fill="none"/>' for yy in range(top - 170, 0, 60))
                 + f'<path d="M{px},{top-200} q{sx*40},-50 {sx*10},-90 q{-sx*30},-10 {-sx*40},20 q{sx*20},10 {sx*16},30" fill="#4A3826" stroke="{INK}" stroke-width="6"/><circle cx="{px+sx*8}" cy="{top-276}" r="5" fill="#C9A25A"/>'
                 + f'<path d="M{px},{top-120} L{px + sx*110},{top-110} L{px + sx*90},{top-80} L{px + sx*110},{top-50} L{px},{top-60} Z" fill="#8E2A22" stroke="{INK}" stroke-width="4"/>')
    for k, (xx, c1, c2) in enumerate(((-300, "#8E3B2E", "#D8C8A0"), (-170, "#2F4C6E", "#D8C8A0"), (170, "#5A6A3A", "#C9A25A"), (300, "#3A3A38", "#B8302A"))):   # dayalı kalkanlar
        o.append(f'<g transform="translate({xx},-70) rotate({(-1)**k * 8})"><circle r="70" fill="{c1}" stroke="{INK}" stroke-width="6"/><path d="M0,-70 L0,70 M-70,0 L70,0" stroke="{c2}" stroke-width="18"/><circle r="70" fill="none" stroke="#5A5A58" stroke-width="7"/><circle r="16" fill="#8A8A86" stroke="{INK}" stroke-width="4"/></g>')
    o.append("".join(f'<path d="M{xx},{top} q{(-1)**k*10},-28 {(-1)**k*4},-44" stroke="#6E7A4A" stroke-width="6" fill="none"/><circle cx="{xx + (-1)**k*4}" cy="{top-46}" r="9" fill="{["#E8D8A0", "#D8A8B8", "#F0F0E8"][k % 3]}" stroke="{INK}" stroke-width="3"/>' for k, xx in enumerate(range(-240, 260, 40))))   # ot ve çiçekler
    if body:   # sedye + kefenli beden + mavi örtü + mezar eşyaları
        o.append(f'<path d="M-230,{top-6} L230,{top-6} L216,{top+14} L-216,{top+14} Z" fill="#7A5A3C" stroke="{INK}" stroke-width="6"/>'
                 f'<path d="M-200,{top-8} Q-200,{top-70} -120,{top-74} L170,{top-60} Q206,{top-40} 196,{top-8} Z" fill="#E8E0D0" stroke="{INK}" stroke-width="6"/>'
                 f'<path d="M-60,{top-70} L160,{top-58} Q190,{top-40} 186,{top-10} L-60,{top-10} Z" fill="#4A6A8A" stroke="{INK}" stroke-width="5"/>'
                 + "".join(f'<path d="M{xx},{top-66} l0,56" stroke="#C9A25A" stroke-width="4"/>' for xx in range(-40, 170, 40))
                 + f'<circle cx="-150" cy="{top-62}" r="34" fill="#E0C070" stroke="{INK}" stroke-width="5"/>'                     # saç (başın üstü kefenin içinde)
                 f'<path d="M100,{top-64} q14,-26 30,-8" stroke="#B8A070" stroke-width="6" fill="none"/>'                           # tarak
                 f'<path d="M30,{top-70} q-6,-24 10,-30 q16,6 10,30 Z" fill="#D8A8B8" stroke="{INK}" stroke-width="3"/>')            # çiçek demeti
    o.append('</g>')
    return "".join(o)
