"""Michael Scofield projesi karakter sistemi (stil B: sinematik 2D).
Eklemli yapı: baş, gövde, üst kol, ön kol, el ayrı parçalardır; her parça kendi pivotunda döner.
Kimlik öğeleri TEK KAYNAK: dovme_onkol(), turna(), numara().
Yüzler özgündür; hiçbir oyuncuya benzetilmez.
"""
import math, random, sys
from pathlib import Path
P = Path(__file__).resolve().parent; REPO = P.parents[1]
sys.path[:0] = [str(REPO / "r3"), str(REPO / "r2")]
from art2 import shade
from art3 import _eye, _mouth, hand3

INK = "#15110E"
PLAN = "#7FE6FF"

# ── karakter özellikleri (yalnız genel öğeler; oyuncu benzerliği yok)
MICHAEL = dict(skin="#D9A988", hair="#2B2420", iris="#7C9A8E", brow="#2B2420", jaw=1.0, face_len=1.08,
               shirt="#6F8FB0", shirt_d="#55728F", under="#ECE8DE", pants="#2E3A4A", shoe="#2A2420", buzz=True)
MICHAEL_COCUK = dict(MICHAEL, child=True, hair="#3A302A", shirt="#B8563E", shirt_d="#93412F", pants="#3C4A5C",
                     stripes="#E9D9B8", buzz=False)
LINCOLN = dict(skin="#C99C7C", hair="#3A322C", iris="#6F7F88", brow="#2A2420", jaw=1.22, face_len=1.0,
               shirt="#6F8FB0", shirt_d="#55728F", under="#ECE8DE", pants="#2E3A4A", shoe="#2A2420", buzz=True, broad=True)
SARA = dict(skin="#E8BFA2", hair="#7A2E22", iris="#6A8A6E", brow="#5A241A", jaw=0.9, face_len=1.02, female=True,
            shirt="#F2F0EA", shirt_d="#CFCBC0", under="#5E7A8A", pants="#3A4250", shoe="#2A2420", buzz=False)

# ifade: (kaş_iç, kaş_dış, üst_kapak, alt_kapak, ağız, ekstra)
IFADE = {
    "odak":     (6, 0, 0.32, 0.12, "flat", ""),       # varsayılan: sakin, gözler hafif kısık
    "kararli":  (10, -4, 0.36, 0.16, "firm", ""),
    "yas":      (-12, 6, 0.48, 0.10, "tremble", "tear"),
    "korku":    (-10, -10, 0.0, 0.0, "open_s", ""),
    "sefkat":   (-6, 2, 0.34, 0.08, "soft_smile", ""),
    "ofke":     (14, -6, 0.34, 0.14, "firm", ""),
    "plan":     (4, -2, 0.28, 0.10, "flat", "plan"),  # plan görüşü: gözde camgöbeği yansıma
    "neutral":  (0, 0, 0.15, 0.0, "flat", ""),
}

def _brow(cx, cy, w, inner, outer, color, toward, thick=6.0):
    """İnce, düz, modern kaş (Ragnar'ın kama kaşı değil)."""
    xi, xo = cx - toward * w * 0.95, cx + toward * w * 1.2
    yi, yo = cy - 17 - inner * 1.3, cy - 18 - outer * 1.3
    mx, my = (xi + xo) / 2, min(yi, yo) - 4
    return (f'<path d="M{xi:.1f},{yi:.1f} Q{mx:.1f},{my:.1f} {xo:.1f},{yo:.1f}" stroke="{color}" stroke-width="{thick}" '
            f'fill="none" stroke-linecap="round"/>')

def kafa(spec, view="3q", ifade="odak", look=None):
    """Kafa merkezi (0,0), yükseklik ~220. view: front|3q|side. Sağa bakar."""
    sk = spec["skin"]; sh = shade(sk, 0.82); dk = shade(sk, 0.66); hair = spec["hair"]
    child = spec.get("child"); fem = spec.get("female")
    L = spec.get("face_len", 1.0) * (0.9 if child else 1.0); J = spec.get("jaw", 1.0) * (0.85 if child else 1.0)
    bi, bo, lu, ll, mk, extra = IFADE[ifade]
    o = []; late = []
    yb = 92 * L  # çene alt
    if view == "front":
        face = (f"M-74,-20 Q-76,-98 0,-100 Q76,-98 74,-20 L{70*J:.0f},{30*L:.0f} Q{60*J:.0f},{70*L:.0f} {26*J:.0f},{yb-6:.0f} "
                f"Q0,{yb+4:.0f} {-26*J:.0f},{yb-6:.0f} Q{-60*J:.0f},{70*L:.0f} {-70*J:.0f},{30*L:.0f} Z")
        ears = [(-76, 4), (76, 4)]; eyes = [(-31, -4, 18), (31, -4, 18)]; fx = 0
    elif view == "3q":
        face = (f"M-66,-20 Q-70,-98 8,-100 Q80,-96 80,-18 L80,{18*L:.0f} L{74*J:.0f},{44*L:.0f} Q{62*J:.0f},{78*L:.0f} {30*J:.0f},{yb:.0f} "
                f"Q4,{yb+4:.0f} -18,{yb-8:.0f} Q-56,{64*L:.0f} -64,{24*L:.0f} Z")
        ears = [(-58, 6)]; eyes = [(-12, -4, 13), (42, -4, 18)]; fx = 20
    else:
        face = (f"M-72,-20 Q-76,-98 4,-100 Q64,-96 70,-36 L72,-10 L90,{20*L:.0f} L74,{28*L:.0f} Q76,{44*L:.0f} 70,{54*L:.0f} "
                f"L70,{64*L:.0f} Q{64*J:.0f},{84*L:.0f} {40*J:.0f},{yb:.0f} L10,{yb+2:.0f} Q-24,{yb-8:.0f} -40,{66*L:.0f} Q-66,{40*L:.0f} -72,-20 Z")
        ears = [(-8, 8)]; eyes = [(48, -4, 14)]; fx = 40
    # boyun gölgesi + kulaklar
    for ex, ey in ears:
        o.append(f'<ellipse cx="{ex}" cy="{ey}" rx="13" ry="20" fill="{sk}" stroke="{INK}" stroke-width="4"/>'
                 f'<path d="M{ex-3},{ey-8} q7,6 0,15" stroke="{dk}" stroke-width="3" fill="none"/>')
    if fem:  # arka saç kütlesi (omuza dalgalı)
        o.insert(0, f'<path d="M-92,-40 Q-120,60 -96,150 Q-60,170 -30,140 Q-40,60 -20,-60 Z" fill="{shade(hair,0.8)}" stroke="{INK}" stroke-width="4"/>')
    cid = f"k{abs(hash((view, ifade, sk, L, J))) % 10**8}"
    o.append(f'<defs><clipPath id="{cid}"><path d="{face}"/></clipPath></defs><path d="{face}" fill="{sk}"/>')
    # cel gölge (ışık sol üstten): uzak taraf + elmacık altı + çene altı
    o.append(f'<g clip-path="url(#{cid})">'
             f'<path d="M{50 if view!="side" else 20},-110 Q{82 if view!="side" else 40},0 {60 if view!="side" else 30},120 L160,120 L160,-110 Z" fill="{sh}" opacity="0.85"/>'
             f'<path d="M-80,{yb-24:.0f} Q0,{yb+6:.0f} 90,{yb-30:.0f} L90,140 L-80,140 Z" fill="{dk}" opacity="0.35"/>'
             f'<path d="M{fx-50},34 Q{fx-30},48 {fx-10},42" stroke="{sh}" stroke-width="7" fill="none" opacity="0.6"/>'
             f'<path d="M-70,-90 Q-46,-60 -54,-10" stroke="#FFF2E4" stroke-width="10" fill="none" opacity="0.18"/></g>')
    o.append(f'<path d="{face}" fill="none" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>')
    # saç
    if spec.get("buzz"):
        cap = {"front": "M-75,-10 Q-80,-104 0,-108 Q80,-104 75,-10 L70,-14 Q64,-50 40,-58 Q0,-66 -40,-58 Q-64,-50 -70,-14 Z",
               "3q": "M-67,-20 Q-76,-104 10,-108 Q84,-102 80,-30 Q74,-52 50,-58 Q14,-66 -22,-56 Q-50,-46 -56,6 L-62,6 Z",
               "side": "M-73,-20 Q-80,-104 4,-108 Q62,-104 66,-50 Q40,-70 0,-70 Q-36,-64 -40,-14 Q-56,10 -73,-20 Z"}[view]
        o.append(f'<path d="{cap}" fill="{hair}" opacity="0.92" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>')
        r = random.Random(3)
        for _ in range(70):
            x, y = r.uniform(-64, 70), r.uniform(-100, -58)
            o.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="1.2" fill="{shade(hair,1.6)}" opacity="0.5"/>')
        o.append(f'<path d="M-30,-98 Q10,-106 50,-94" stroke="{shade(hair,2.2)}" stroke-width="5" fill="none" opacity="0.35"/>')
    elif fem:
        late.append(f'<path d="M-72,-20 Q-84,-112 10,-114 Q96,-108 86,-10 Q70,-70 30,-72 Q40,-40 70,-10 Q20,-30 6,-74 Q-30,-60 -50,10 Q-70,-6 -72,-20 Z" '
                    f'fill="{hair}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
                    f'<path d="M-40,-90 Q0,-104 40,-96" stroke="{shade(hair,1.5)}" stroke-width="6" fill="none" opacity="0.5"/>')
    else:  # çocuk: kısa, dağınık
        late.append(f'<path d="M-72,-16 Q-84,-110 6,-114 Q92,-108 84,-20 Q78,-46 62,-44 Q58,-62 40,-56 Q30,-70 12,-62 Q0,-72 -14,-60 Q-30,-68 -40,-54 Q-58,-56 -60,-30 Z" '
                    f'fill="{hair}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
                    f'<path d="M-40,-94 Q0,-106 44,-96" stroke="{shade(hair,1.7)}" stroke-width="6" fill="none" opacity="0.4"/>')
    # gözler + kaşlar
    lk = 0.3 if look is None else look
    eh = 11.5 if not child else 13.5
    for k, (ex, ey, ew) in enumerate(eyes):
        o.append(_eye(ex, ey, ew * (1.1 if child else 1), eh * (ew / 18), lu, ll, spec["iris"], lk, sk))
        o.append(f'<path d="M{ex-ew*0.9:.1f},{ey-eh*1.55:.1f} Q{ex:.1f},{ey-eh*2.0:.1f} {ex+ew*0.9:.1f},{ey-eh*1.45:.1f}" stroke="{dk}" stroke-width="2" fill="none" opacity="0.55"/>')
        tw = 1 if k == len(eyes) - 1 else -1
        if view == "front": tw = 1 if ex > 0 else -1
        late.append(_brow(ex, ey, ew, bi, bo, spec["brow"], -tw if view == "front" else (-1 if k == len(eyes)-1 else 1),
                          thick=4.5 if fem else (5 if child else 6.5)))
        if extra == "plan":
            late.append(f'<circle cx="{ex + lk*ew*0.45 + 3:.1f}" cy="{ey-2}" r="{eh*0.45:.1f}" fill="{PLAN}" opacity="0.85"/>'
                        f'<path d="M{ex-ew},{ey+eh*1.2} h{ew*2}" stroke="{PLAN}" stroke-width="1.5" opacity="0.5"/>')
        if fem:
            late.append(f'<path d="M{ex+ew*0.8},{ey-eh*0.6} l6,-6 M{ex+ew*0.45},{ey-eh*0.95} l4,-7" stroke="{INK}" stroke-width="2.6" stroke-linecap="round"/>')
    # burun, ağız, ayrıntı
    if view == "front":
        o.append(f'<path d="M-2,2 Q-8,26 -8,32 Q2,38 12,32" stroke="{dk}" stroke-width="3.5" fill="none" stroke-linecap="round"/>'); mx = 0
    elif view == "3q":
        o.append(f'<path d="M22,-2 L36,28 Q32,36 20,34" stroke="{INK}" stroke-width="3.8" fill="{sh}" stroke-linejoin="round"/>'); mx = 28
    else:
        mx = 62
    my = 58 * L if not child else 52
    mw = 15 if view == "front" else (13 if view == "3q" else 8)
    if fem: o.append(f'<ellipse cx="{mx}" cy="{my+5:.0f}" rx="{mw*0.8:.1f}" ry="4" fill="#C2786A" opacity="0.7"/>')
    o.append(_mouth(mx, my, mw, mk, sk))
    if not child and not fem:  # yetişkin erkek: çene hattında hafif sakal gölgesi, düşünce çizgisi
        o.append(f'<g clip-path="url(#{cid})"><path d="M-70,{40*L:.0f} Q0,{yb+30:.0f} 90,{40*L:.0f} L90,{yb+20:.0f} L-70,{yb+20:.0f} Z" fill="{hair}" opacity="0.12"/></g>')
        cxb = {"front": 0, "3q": 18, "side": 36}[view]
        late.append(f'<path d="M{cxb+2},-30 v10" stroke="{dk}" stroke-width="2.4" stroke-linecap="round" opacity="0.7"/>')
    if extra == "tear":
        ex = eyes[-1][0]
        o.append(f'<path d="M{ex+2},10 Q{ex+8},30 {ex+4},44" stroke="#BFE2FF" stroke-width="4.5" fill="none" stroke-linecap="round"/>'
                 f'<ellipse cx="{ex+4}" cy="48" rx="4.5" ry="6.5" fill="#BFE2FF" stroke="#5A8AB0" stroke-width="2"/>')
    return "".join(o) + "".join(late)

def dovme_onkol(w=60, h=150, plan=False):
    """Önkol dövmesi TEK KAYNAK: kemer + turna kanadı + gizli plan çizgisi. Yerel: önkol ekseni dikey, üst (0,0)."""
    t = "#2E3A48"; o = []
    o.append(f'<path d="M{-w*0.3},{h*0.9} V{h*0.35} Q0,{h*0.12} {w*0.3},{h*0.35} V{h*0.9}" fill="none" stroke="{t}" stroke-width="2.4" opacity="0.85"/>')
    o.append(f'<path d="M{-w*0.34},{h*0.22} L0,{h*0.08} L{w*0.34},{h*0.22} L0,{h*0.3} Z" fill="none" stroke="{t}" stroke-width="2.2" opacity="0.85"/>')
    for k in range(4):
        o.append(f'<circle cx="{-w*0.36}" cy="{h*(0.45+k*0.12):.0f}" r="2.6" fill="none" stroke="{t}" stroke-width="1.6" opacity="0.8"/>')
    o.append(f'<path d="M{-w*0.15},{h*0.85} V{h*0.55} H{w*0.12} V{h*0.4}" fill="none" stroke="{PLAN if plan else t}" '
             f'stroke-width="{2.6 if plan else 1.6}" opacity="{1 if plan else 0.55}"/>')
    return "".join(o)

def kol(pts, w, renk, ten, cuff_t=None, dovme=False, plan=False):
    """Eklemli kol: omuz→dirsek→bilek. cuff_t: gömlek kolunun bittiği oran (sıvalı kol)."""
    (x0, y0), (x1, y1), (x2, y2) = pts
    o = []
    def seg(a, b, ww, c):
        return (f'<path d="M{a[0]:.1f},{a[1]:.1f} L{b[0]:.1f},{b[1]:.1f}" stroke="{INK}" stroke-width="{ww+9}" stroke-linecap="round"/>'
                f'<path d="M{a[0]:.1f},{a[1]:.1f} L{b[0]:.1f},{b[1]:.1f}" stroke="{c}" stroke-width="{ww}" stroke-linecap="round"/>')
    o.append(seg((x1, y1), (x2, y2), w * 0.82, ten))
    if dovme:
        ang = math.degrees(math.atan2(y2 - y1, x2 - x1)) - 90
        ln = math.hypot(x2 - x1, y2 - y1)
        o.append(f'<g transform="translate({x1:.1f},{y1:.1f}) rotate({ang:.1f})">{dovme_onkol(w*0.8, ln, plan)}</g>')
    o.append(seg((x0, y0), (x1, y1), w, renk))
    if cuff_t is not None:   # sıvanmış manşet dirsekte
        o.append(f'<ellipse cx="{x1:.1f}" cy="{y1:.1f}" rx="{w*0.62:.1f}" ry="{w*0.42:.1f}" fill="{shade(renk,0.85)}" stroke="{INK}" stroke-width="4" '
                 f'transform="rotate({math.degrees(math.atan2(y2-y1, x2-x1)):.1f} {x1:.1f} {y1:.1f})"/>')
    return "".join(o)

def figur(spec, ifade="odak", kol_sol=None, kol_sag=None, eller=("relax", "relax"), plan=False, numara_goster=True):
    """Ayakta 3/4 figür, ayak ortası (0,0), boy ~ 560 (yetişkin) / 420 (çocuk). Sağa bakar."""
    child = spec.get("child"); s = 0.76 if child else 1.0; br = 1.18 if spec.get("broad") else 1.0
    sk = spec["skin"]; sh = spec["shirt"]; sd = spec["shirt_d"]
    hy = -480 * s; shy = -390 * s; hip = -215 * s
    o = [f'<ellipse cx="0" cy="4" rx="{110*br*s:.0f}" ry="16" fill="#000" opacity="0.25"/>']
    # bacaklar + ayakkabı
    for lx, fx2 in ((-34 * br, -40), (30 * br, 44)):
        o.append(f'<path d="M{lx*s:.0f},{hip+10} L{fx2*s:.0f},-22" stroke="{INK}" stroke-width="{62*s+9:.0f}" stroke-linecap="round"/>'
                 f'<path d="M{lx*s:.0f},{hip+10} L{fx2*s:.0f},-22" stroke="{spec["pants"]}" stroke-width="{62*s:.0f}" stroke-linecap="round"/>')
        o.append(f'<path d="M{fx2*s-28:.0f},-30 L{fx2*s+30:.0f},-30 Q{fx2*s+56:.0f},-20 {fx2*s+52:.0f},2 L{fx2*s-30:.0f},2 Z" fill="{spec["shoe"]}" stroke="{INK}" stroke-width="4.5" stroke-linejoin="round"/>')
    o.append(f'<path d="M{-30*br*s:.0f},{hip+40} L{-36*br*s:.0f},-40" stroke="{shade(spec["pants"],0.75)}" stroke-width="10" opacity="0.6"/>')
    # uzak kol (arkada)
    nx, fx_ = 70 * br * s, -66 * br * s
    ks = kol_sol or [(fx_ + 6, shy + 20), (fx_ - 12, shy + 130 * s), (fx_ + 4, shy + 230 * s)]
    o.append(kol(ks, 40 * s * br, sd, shade(sk, 0.88), cuff_t=0.5 if not child else None, dovme=not child and not spec.get("female"), plan=plan))
    o.append(f'<g transform="rotate(180 {ks[2][0]:.1f} {ks[2][1]+8:.1f})">' + hand3(ks[2][0], ks[2][1] + 8, 19 * s, shade(sk, 0.88), eller[0], -1) + '</g>' if eller[0] == "relax" else hand3(ks[2][0], ks[2][1], 19 * s, shade(sk, 0.88), eller[0], 1))
    # gövde (gömlek)
    torso = (f"M{fx_-6:.0f},{shy-4:.0f} Q{fx_-16:.0f},{(shy+hip)/2:.0f} {fx_+2:.0f},{hip:.0f} L{fx_-4:.0f},{hip+34*s:.0f} "
             f"Q0,{hip+46*s:.0f} {nx+8:.0f},{hip+30*s:.0f} L{nx+4:.0f},{hip:.0f} Q{nx+14:.0f},{(shy+hip)/2:.0f} {nx+6:.0f},{shy-4:.0f} "
             f"Q0,{shy-24*s:.0f} {fx_-6:.0f},{shy-4:.0f} Z")
    tid = f"t{abs(hash((sh, s, br))) % 10**7}"
    o.append(f'<defs><clipPath id="{tid}"><path d="{torso}"/></clipPath></defs><path d="{torso}" fill="{sh}"/>')
    inner = [f'<rect x="{nx-26:.0f}" y="{shy-40:.0f}" width="120" height="600" fill="{sd}"/>']
    if spec.get("stripes"):
        for k in range(8):
            inner.append(f'<rect x="-200" y="{shy+14+k*30*s:.0f}" width="400" height="{11*s:.0f}" fill="{spec["stripes"]}" opacity="0.9"/>')
    elif spec.get("female"):  # doktor önlüğü: yaka, cep, stetoskop
        inner.append(f'<path d="M-10,{shy-6:.0f} L10,{shy+120*s:.0f} L30,{shy-6:.0f}" fill="{spec["under"]}" stroke="{INK}" stroke-width="3"/>'
                     f'<rect x="{fx_+18:.0f}" y="{shy+90:.0f}" width="34" height="30" fill="none" stroke="{INK}" stroke-width="3"/>'
                     f'<path d="M-6,{shy+4:.0f} Q-40,{shy+90:.0f} -6,{shy+130:.0f} M26,{shy+4:.0f} Q50,{shy+80:.0f} 30,{shy+120:.0f}" stroke="#3A3F46" stroke-width="5" fill="none"/>'
                     f'<circle cx="-6" cy="{shy+134:.0f}" r="9" fill="#C8CDD2" stroke="{INK}" stroke-width="3"/>')
    else:  # hapishane gömleği: yaka, düğmeler, cep, numara
        inner.append(f'<path d="M-14,{shy-8:.0f} L8,{shy+44:.0f} L30,{shy-8:.0f}" fill="{spec["under"]}" stroke="{INK}" stroke-width="3"/>'
                     f'<path d="M-20,{shy-6:.0f} L-6,{shy+30:.0f} L8,{shy+6:.0f} M36,{shy-6:.0f} L22,{shy+30:.0f} L8,{shy+6:.0f}" fill="{shade(sh,1.08)}" stroke="{INK}" stroke-width="3"/>'
                     + "".join(f'<circle cx="{8+k*1.2:.0f}" cy="{shy+60+k*44:.0f}" r="3.5" fill="#E8E4DA" stroke="{INK}" stroke-width="1.5"/>' for k in range(4))
                     + f'<rect x="{fx_+24:.0f}" y="{shy+50:.0f}" width="44" height="38" rx="3" fill="none" stroke="{INK}" stroke-width="2.6"/>')
        if numara_goster:
            inner.append(f'<text x="{fx_+20:.0f}" y="{shy+42:.0f}" font-family="DejaVu Sans Mono" font-weight="bold" font-size="15" fill="#F0ECE2">94941</text>')
    inner.append(f'<path d="M{fx_+6:.0f},{shy+20:.0f} Q{fx_+30:.0f},{(shy+hip)/2:.0f} {fx_+12:.0f},{hip:.0f}" stroke="#FFFFFF" stroke-width="8" fill="none" opacity="0.18"/>')
    o.append(f'<g clip-path="url(#{tid})">{"".join(inner)}</g><path d="{torso}" fill="none" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>')
    # boyun + baş
    o.append(f'<path d="M-22,{hy+80*s:.0f} L-20,{shy-6:.0f} L36,{shy-6:.0f} L34,{hy+80*s:.0f} Z" fill="{shade(sk,0.84)}" stroke="{INK}" stroke-width="4"/>')
    o.append(f'<g transform="translate(8,{hy:.0f}) scale({0.62*s*(1.05 if child else 1):.3f})">{kafa(spec, "3q", ifade)}</g>')
    # yakın kol (önde)
    ka = kol_sag or [(nx, shy + 18), (nx + 24 * s, shy + 132 * s), (nx + 12, shy + 236 * s)]
    o.append(kol(ka, 42 * s * br, sh, sk, cuff_t=0.5 if not child else None, dovme=not child and not spec.get("female"), plan=plan))
    o.append(f'<g transform="rotate(180 {ka[2][0]:.1f} {ka[2][1]+8:.1f})">' + hand3(ka[2][0], ka[2][1] + 8, 20 * s, sk, eller[1], -1) + '</g>' if eller[1] == "relax" else hand3(ka[2][0], ka[2][1], 20 * s, sk, eller[1], 1))
    return "".join(o)

def turna(s=1.0, isik=0.0, kanat=0.0):
    """Kâğıt turna TEK KAYNAK. Merkez (0,0) gövde ortası. kanat: -1..1 kanat çırpma (animasyon)."""
    p0, p1, p2 = "#F6F2E8", "#DCD5C6", "#B9B09E"
    ky = -86 - 30 * kanat
    return (f'<g transform="scale({s})">'
            f'<ellipse cx="0" cy="44" rx="78" ry="9" fill="#000" opacity="0.2"/>'
            f'<path d="M-26,-6 L-36,{ky*0.95:.0f} L16,-12 Z" fill="{p2}" stroke="{INK}" stroke-width="3.2" stroke-linejoin="round"/>'      # uzak kanat
            f'<path d="M-46,4 L0,-14 L46,4 L0,30 Z" fill="{p1}" stroke="{INK}" stroke-width="3.2" stroke-linejoin="round"/>'              # gövde elması
            f'<path d="M-46,4 L0,-14 L0,30 Z" fill="{p0}" stroke="{INK}" stroke-width="3.2" stroke-linejoin="round"/>'
            f'<path d="M-30,6 L-82,-48 L-74,-50 L-22,-2 Z" fill="{p0}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'          # kuyruk
            f'<path d="M30,6 L76,-56 L92,-52 L84,-46 L80,-48 L24,-2 Z" fill="{p1}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'  # boyun + baş
            f'<path d="M-20,-4 L44,{ky:.0f} L26,-6 Z" fill="{p0}" stroke="{INK}" stroke-width="3.2" stroke-linejoin="round"/>'              # yakın kanat
            f'<path d="M-18,-6 L44,{ky:.0f}" stroke="#FFF7D8" stroke-width="{2+5*isik:.1f}" opacity="{0.25+0.65*isik:.2f}"/>'
            f'<path d="M0,-14 L0,30" stroke="{p2}" stroke-width="2" opacity="0.8"/>'
            f'</g>')
