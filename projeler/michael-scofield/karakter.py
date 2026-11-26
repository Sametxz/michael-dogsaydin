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

def turna(s=1.0, isik=0.0, kanat=0.0, kagit="#F7F3EA", golge=True):
    """Kâğıt turna TEK KAYNAK (v3.1, gerçekçi origami). Merkez (0,0) gövde ortası, sağa bakar.
    Elmas gövde, ince yukarı boyun ve kuyruk sivrileri, aşağı katlı baş, V açısıyla kalkan iki geniş
    üçgen kanat (her biri kat iziyle ışık/gölge yüzeyine bölünür), hafif kâğıt dokusu.
    isik: 0..1 sabah ışığı; kanat: -1..1 kanat çırpma (V açılır/kapanır)."""
    L = kagit; M = shade(kagit, 0.91); D = shade(kagit, 0.80); DD = shade(kagit, 0.68)
    lw = 2.4 / max(s, 0.3) ** 0.6; crease = shade(kagit, 0.58)
    def pg(pts, fill):
        d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + " Z"
        return f'<path d="{d}" fill="{fill}" stroke="{INK}" stroke-width="{lw:.2f}" stroke-linejoin="round"/>'
    def ln(a, b, w=1.1, op=0.75):
        return f'<path d="M{a[0]:.1f},{a[1]:.1f} L{b[0]:.1f},{b[1]:.1f}" stroke="{crease}" stroke-width="{w/max(s,0.3)**0.5:.2f}" opacity="{op}"/>'
    sp = 22 * kanat                                 # V açıklığı
    fa = (-44 - sp, -112 + 46 * kanat)         # uzak kanat ucu
    na = (54 + sp, -120 + 50 * kanat)          # yakın kanat ucu
    o = [f'<g transform="scale({s})">'] + ([f'<ellipse cx="4" cy="48" rx="88" ry="9" fill="#000" opacity="0.22"/>'] if golge else [])
    # uzak kanat: iki yüz
    fm = (-4, -8)
    o += [pg([(-38, 2), fa, fm], DD), pg([fm, fa, (30, -6)], D)]
    # kuyruk
    o += [pg([(-24, 0), (-106, -60), (-36, 12)], M), pg([(-24, 0), (-106, -60), (-14, -6)], L)]
    # gövde elması (ışık sol üstten)
    o += [pg([(-46, 6), (0, -12), (0, 36)], L), pg([(0, -12), (46, 6), (0, 36)], M),
          pg([(-46, 6), (0, 36), (-10, 42)], D), pg([(0, 36), (46, 6), (10, 42)], DD)]
    # boyun + baş
    o += [pg([(24, 0), (98, -72), (36, 12)], D), pg([(24, 0), (98, -72), (14, -6)], M),
          pg([(98, -72), (94, -64), (116, -54)], L), pg([(94, -64), (116, -54), (104, -52)], D)]
    # yakın kanat: iki yüz (ışık + gölge), kat izi
    nm = (8, -10)
    o += [pg([(-30, 6), na, nm], M), pg([nm, na, (42, 2)], L), ln(nm, na)]
    # kat izleri
    o += [ln((0, -12), (0, 36)), ln((-14, -6), (-106, -60), 0.9, 0.5), ln((14, -6), (98, -72), 0.9, 0.5), ln(fm, fa, 0.9, 0.5)]
    # kâğıt dokusu: çok ince lifler (yalnız büyük ölçekte)
    if False:
        r = random.Random(7)
        for _ in range(26):
            x, y = r.uniform(-30, 40), r.uniform(-90, 30)
            o.append(f'<path d="M{x:.0f},{y:.0f} l{r.uniform(4,10):.0f},{r.uniform(-3,3):.0f}" stroke="{D}" stroke-width="0.6" opacity="0.5"/>')
    # kenar ışığı ve sabah ışığı
    hl = "#FFF8DC"
    o.append(f'<path d="M-30,6 L{na[0]:.0f},{na[1]:.0f} M24,0 L98,-72 M-24,0 L-106,-60 M-46,6 L0,-12" stroke="{hl}" stroke-width="{(1.2+1.6*isik)/max(s,0.3)**0.5:.2f}" opacity="{0.4+0.4*isik:.2f}" stroke-linecap="round"/>')
    if isik > 0 and golge: o.append(f'<ellipse cx="10" cy="-40" rx="120" ry="90" fill="#FFE9B0" opacity="{0.10*isik:.2f}"/>')
    o.append('</g>')
    return "".join(o)

# ───────────────────────── v2: iskeletli, pozlanabilir figür ─────────────────────────
def _uc(x, y, a, L):
    """(x,y) noktasından dikeyden a derece (sağa +) L uzunlukta aşağı doğru uç."""
    r = math.radians(a); return x + L * math.sin(r), y + L * math.cos(r)

def _seg(a, b, w, c):
    return (f'<path d="M{a[0]:.1f},{a[1]:.1f} L{b[0]:.1f},{b[1]:.1f}" stroke="{INK}" stroke-width="{w+9:.1f}" stroke-linecap="round"/>'
            f'<path d="M{a[0]:.1f},{a[1]:.1f} L{b[0]:.1f},{b[1]:.1f}" stroke="{c}" stroke-width="{w:.1f}" stroke-linecap="round"/>')

POZ_DUR = dict(govde=3, bas=0, kol_on=(8, -6), kol_arka=(-6, 10), bacak_on=(4, 0), bacak_arka=(-6, 6), el_on="relax", el_arka="relax")

def figur2(spec, ifade="odak", poz=None, plan=False, numara_goster=True, el_on_ek=""):
    """Pozlanabilir 3/4 figür, sağa bakar, yer y=0. poz alanları (derece):
    govde: gövde eğimi (öne +); bas: baş eğimi; kol_on/kol_arka: (omuz, dirsek) dikeyden, öne +;
    bacak_on/bacak_arka: (kalça, diz bükümü); el_on/el_arka: relax|open|fist|grip|point.
    el_on_ek: yakın elin içine çizilecek SVG ('HX','HY' yer tutucu)."""
    p = dict(POZ_DUR); p.update(poz or {})
    child = spec.get("child"); s = 0.76 if child else 1.0; br = 1.18 if spec.get("broad") else 1.0
    sk = spec["skin"]; sh = spec["shirt"]; sd = spec["shirt_d"]
    TH, SN = 118 * s, 112 * s            # uyluk, baldır
    UA, FA = 112 * s, 104 * s            # üst kol, ön kol
    TOR = 200 * s                        # pelvis→omuz
    # pelvis yüksekliği: en alçak ayak yere değsin
    def ayak_y(t, k):
        kx, ky = _uc(0, 0, t, TH); ax, ay = _uc(kx, ky, t - k, SN); return ay
    hip_y = -max(ayak_y(*p["bacak_on"]), ayak_y(*p["bacak_arka"])) - 26 * s
    hip = (0, hip_y)
    g = math.radians(p["govde"])
    def tw(lx, ly):  # gövde yerelinden dünyaya (pelvis merkezli, yukarı -y)
        return hip[0] + lx * math.cos(g) - ly * math.sin(g), hip[1] + lx * math.sin(g) + ly * math.cos(g)
    sh_on, sh_ark = tw(64 * br * s, -TOR + 14 * s), tw(-60 * br * s, -TOR + 18 * s)
    neck = tw(8 * s, -TOR - 10 * s)
    o = [f'<ellipse cx="0" cy="4" rx="{110*br*s:.0f}" ry="16" fill="#000" opacity="0.25"/>']
    def bacak(side, t, k, ton):
        hx, hy = tw(side * 26 * br * s, 0)
        kx, ky = _uc(hx, hy, t, TH); ax, ay = _uc(kx, ky, t - k, SN)
        out = _seg((hx, hy), (kx, ky), 60 * s, ton) + _seg((kx, ky), (ax, ay), 54 * s, ton)
        out += (f'<path d="M{ax-26*s:.0f},{ay-10:.0f} L{ax+30*s:.0f},{ay-10:.0f} Q{ax+54*s:.0f},{ay+2:.0f} {ax+50*s:.0f},{ay+22:.0f} L{ax-28*s:.0f},{ay+22:.0f} Z" '
                f'fill="{spec["shoe"]}" stroke="{INK}" stroke-width="4.5" stroke-linejoin="round" transform="rotate({max(-25, min(25, (t-k)*0.5)):.0f} {ax:.0f} {ay:.0f})"/>')
        return out
    def kol(sp, oa, da, w, renk, ten, el, ek=""):
        ex, ey = _uc(*sp, oa, UA); wx, wy = _uc(ex, ey, oa + da, FA)
        out = _seg((ex, ey), (wx, wy), w * 0.8, ten)
        if not child and not spec.get("female"):
            out += f'<g transform="translate({ex:.1f},{ey:.1f}) rotate({-(oa+da):.1f})">{dovme_onkol(w*0.8, FA, plan)}</g>'
        out += _seg(sp, (ex, ey), w, renk)
        if not child:
            out += (f'<ellipse cx="{ex:.1f}" cy="{ey:.1f}" rx="{w*0.62:.1f}" ry="{w*0.42:.1f}" fill="{shade(renk,0.85)}" stroke="{INK}" stroke-width="4" '
                    f'transform="rotate({90-(oa+da):.1f} {ex:.1f} {ey:.1f})"/>')
        hx, hy = _uc(wx, wy, oa + da, 14 * s)
        if el == "relax":
            out += f'<g transform="rotate({180-(oa+da):.1f} {hx:.1f} {hy:.1f})">{hand3(hx, hy, 20*s, ten, "open", -1)}</g>'
        else:
            out += f'<g transform="rotate({-(oa+da)*0.6:.1f} {hx:.1f} {hy:.1f})">{hand3(hx, hy, 20*s, ten, el, 1)}</g>'
        if ek: out += ek.replace("HX", f"{hx:.1f}").replace("HY", f"{hy:.1f}")
        return out
    # arka katmanlar
    o.append(bacak(-1, *p["bacak_arka"], shade(spec["pants"], 0.82)))
    o.append(kol(sh_ark, *p["kol_arka"], 40 * s * br, sd, shade(sk, 0.88), p["el_arka"]))
    o.append(bacak(1, *p["bacak_on"], spec["pants"]))
    # gövde: V biçimli, yerel koordinatta çizilip döndürülür
    W1, W2 = 72 * br * s, 50 * br * s
    torso = (f"M{-W1:.0f},{-TOR+10*s:.0f} Q{-W1-8:.0f},{-TOR*0.6:.0f} {-W2:.0f},{-TOR*0.2:.0f} L{-W2-4:.0f},{20*s:.0f} "
             f"Q0,{34*s:.0f} {W2+6:.0f},{18*s:.0f} L{W2+2:.0f},{-TOR*0.2:.0f} Q{W1+10:.0f},{-TOR*0.6:.0f} {W1:.0f},{-TOR+10*s:.0f} "
             f"Q0,{-TOR-16*s:.0f} {-W1:.0f},{-TOR+10*s:.0f} Z")
    tid = f"v{abs(hash((sh, s, br, p['govde']))) % 10**7}"
    inner = [f'<rect x="{W2-6:.0f}" y="{-TOR-40:.0f}" width="80" height="{TOR+90:.0f}" fill="{sd}"/>',
             f'<path d="M{-W1+10:.0f},{-TOR+30:.0f} Q{-W2+10:.0f},{-TOR*0.4:.0f} {-W2+6:.0f},0" stroke="#FFFFFF" stroke-width="9" fill="none" opacity="0.16"/>']
    if spec.get("stripes"):
        for k in range(9): inner.append(f'<rect x="-200" y="{-TOR+20*s+k*28*s:.0f}" width="400" height="{10*s:.0f}" fill="{spec["stripes"]}" opacity="0.9"/>')
    elif not spec.get("female"):
        inner.append(f'<path d="M-6,{-TOR-6:.0f} L14,{-TOR+44*s:.0f} L34,{-TOR-6:.0f}" fill="{spec["under"]}" stroke="{INK}" stroke-width="3"/>'
                     f'<path d="M-14,{-TOR-2:.0f} L2,{-TOR+32*s:.0f} L14,{-TOR+8*s:.0f} M42,{-TOR-2:.0f} L26,{-TOR+32*s:.0f} L14,{-TOR+8*s:.0f}" fill="{shade(sh,1.08)}" stroke="{INK}" stroke-width="3"/>'
                     + "".join(f'<circle cx="16" cy="{-TOR+58*s+k*42*s:.0f}" r="3.5" fill="#E8E4DA" stroke="{INK}" stroke-width="1.5"/>' for k in range(4))
                     + f'<rect x="{-W1+16:.0f}" y="{-TOR+52*s:.0f}" width="40" height="34" rx="3" fill="none" stroke="{INK}" stroke-width="2.6"/>')
        if numara_goster:
            inner.append(f'<text x="{-W1+14:.0f}" y="{-TOR+44*s:.0f}" font-family="DejaVu Sans Mono" font-weight="bold" font-size="14" fill="#F0ECE2">94941</text>')
    o.append(f'<g transform="translate({hip[0]:.1f},{hip[1]:.1f}) rotate({p["govde"]})">'
             f'<defs><clipPath id="{tid}"><path d="{torso}"/></clipPath></defs><path d="{torso}" fill="{sh}"/>'
             f'<g clip-path="url(#{tid})">{"".join(inner)}</g><path d="{torso}" fill="none" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/></g>')
    # boyun + baş
    hx, hy = _uc(*neck, 180 + p["govde"] * 0.3 + p["bas"] * 0.3, 70 * s)
    o.append(_seg(neck, (neck[0] + (hx - neck[0]) * 0.5, neck[1] + (hy - neck[1]) * 0.5), 44 * s, shade(sk, 0.84)))
    o.append(f'<g transform="translate({hx:.1f},{hy:.1f}) rotate({p["govde"]*0.4 + p["bas"]:.1f}) scale({0.62*s*(1.05 if child else 1):.3f})">{kafa(spec, "3q", ifade)}</g>')
    o.append(kol(sh_on, *p["kol_on"], 42 * s * br, sh, sk, p["el_on"], el_on_ek))
    return "".join(o)

POZLAR = {
    "dur":        POZ_DUR,
    "bak_1":      dict(bas=-4),
    "bak_2":      dict(bas=6, govde=4),
    "bak_3":      dict(bas=10, govde=6, kol_on=(14, -10)),
    "dokun_1":    dict(govde=6, kol_on=(30, -20), el_on="relax"),
    "dokun_2":    dict(govde=10, kol_on=(70, -30), el_on="open"),
    "dokun_3":    dict(govde=14, kol_on=(100, -12), el_on="open", bacak_on=(14, 10)),
    "yuru_1":     dict(govde=6, kol_on=(-18, 14), kol_arka=(22, 18), bacak_on=(22, 4), bacak_arka=(-18, 14)),
    "yuru_2":     dict(govde=6, kol_on=(2, 10), kol_arka=(0, 10), bacak_on=(2, 0), bacak_arka=(-4, 30)),
    "yuru_3":     dict(govde=6, kol_on=(22, 18), kol_arka=(-18, 14), bacak_on=(-18, 14), bacak_arka=(22, 4)),
    "kos_1":      dict(govde=16, bas=-4, kol_on=(-36, 70), kol_arka=(40, 60), bacak_on=(40, 22), bacak_arka=(-38, 70), el_on="fist", el_arka="fist"),
    "kos_2":      dict(govde=14, bas=-4, kol_on=(4, 76), kol_arka=(-4, 76), bacak_on=(4, 8), bacak_arka=(16, 96), el_on="fist", el_arka="fist"),
    "kos_3":      dict(govde=16, bas=-4, kol_on=(40, 60), kol_arka=(-36, 70), bacak_on=(-38, 70), bacak_arka=(40, 22), el_on="fist", el_arka="fist"),
    "uzat_1":     dict(govde=2, kol_on=(10, 60), el_on="grip"),
    "uzat_2":     dict(govde=6, kol_on=(40, 40), el_on="open"),
    "uzat_3":     dict(govde=10, kol_on=(76, 6), el_on="open", bas=4),
}
