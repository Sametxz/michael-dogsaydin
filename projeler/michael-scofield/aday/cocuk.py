"""11 yaşındaki Michael: kafa + figür adayı (v2).
Sözleşme karakter.kafa ile aynı: kafa(spec, view, ifade, look), merkez (0,0), yükseklik ~220, sağa bakar.
Yetişkinle süreklilik anahtarları: aynı iris rengi, aynı DÜZ kaş biçimi (keskin kaş), aynı saç çizgisi
(alında yetişkin buzz kesiminin sınırıyla aynı yay), aynı kulak, aynı köşeli 3/4 burun (kısaltılmış), aynı düz ağız.
Çocuk oranları: büyük kafatası/alın, göz hattı aşağıda, yuvarlak yanak, kısa burun, küçük yumuşak çene, ince boyun.
Sevimlilik abartısı yok: göz ancak %10 büyük, ağır üst kapak (yetişkinin sakin bakışı), pembe yanak yok,
göz altında hafif yorgunluk gölgesi (koruyucu aile, uykusuzluk).
Hiçbir gerçek kişiye benzetilmez.
Çalıştır: python3 cocuk.py  ->  cocuk_kart.svg/png
"""
import math, random, sys, subprocess
from pathlib import Path
A = Path(__file__).resolve().parent; PRJ = A.parent; REPO = PRJ.parents[1]
sys.path[:0] = [str(A), str(PRJ), str(REPO / "r3"), str(REPO / "r2")]
import karakter as K
from art2 import shade
from art3 import _eye, _mouth, hand3

INK = K.INK; PLAN = K.PLAN

import yetiskin as Y

# ── spec: renkler YETİŞKİNDEN (Y.MICHAEL_Y); tek fark saçın uzunluğu ve kıyafet
_YS = Y.MICHAEL_Y
MICHAEL_COCUK_V2 = dict(K.MICHAEL, child=True, keskin=False, buzz=False,
                        skin=_YS["skin"], skin_sh=_YS["skin_sh"], skin_dk=_YS["skin_dk"], skin_hl=_YS["skin_hl"],
                        hair=_YS["hair"], brow=_YS["brow"], iris=_YS["iris"], iris_d=_YS["iris_d"],
                        shirt="#9A5A48", shirt_d="#7A4334", shirt_hl="#B9735D",   # soluk, büyük gelen tişört (Lincoln'ün eskisi)
                        pants="#3E4B5E", pants_d="#323D4D", shoe="#3A332E", sole="#CFC6B6")

# ifade (yetişkinle aynı sözleşme): kaş_iç (yukarı +), kaş_dış, üst_kapak, alt_kapak, ağız, ekstra
# varsayılan "odak": sakin, meraklı, hafif hüzünlü (iç kaş çok hafif kalkık)
IFADE_C = {
    "odak":    (3, 0, 0.14, 0.06, "duz", ""),
    "plan":    (-2, 2, 0.14, 0.08, "duz", "plan"),
    "korku":   (12, 8, 0.0, 0.0, "open_s", "korku"),
    "sefkat":  (6, 2, 0.16, 0.24, "yarim", ""),
    "yas":     (11, -4, 0.26, 0.04, "tremble", "tear"),
    "kararli": (-8, 2, 0.24, 0.16, "siki", ""),
    "ofke":    (-11, 3, 0.26, 0.20, "siki", ""),
    "neutral": (0, 0, 0.14, 0.06, "duz", ""),
}

# geometri: yetişkin v4 yüzünün çocuk hâli (büyük kafatası, göz hattı ~10 aşağıda, dolgun yanak, kısa burun, yumuşak çene)
GEO = {
    "front": dict(
        face=("M-66,-40 C-68,-100 -34,-116 0,-116 C34,-116 68,-100 66,-40 C68,-10 66,18 60,38 "
              "C54,58 42,74 24,82 C14,86 -14,86 -24,82 C-42,74 -54,58 -60,38 C-66,18 -68,-10 -66,-40 Z"),
        ears=[(-66, 4, -1), (66, 4, 1)], eyes=[(-26, 2, 18, False), (26, 2, 18, False)],
        nose=(0, 32), mouth=(0, 54, 12),
        hair=("M-64,-22 C-71,-30 -75,-42 -72,-54 C-78,-102 -36,-126 0,-126 C38,-126 78,-102 72,-54 "
              "C75,-42 71,-30 64,-22 C62,-34 60,-46 54,-56 C52,-60 51,-62 50,-64 "
              "C52,-56 50,-50 45,-45 C42,-56 33,-64 22,-68 C24,-58 20,-51 13,-46 C10,-57 3,-64 -6,-68 "
              "C-5,-58 -9,-51 -16,-46 C-20,-57 -28,-64 -37,-66 C-36,-57 -40,-51 -45,-47 C-49,-55 -54,-58 -56,-54 "
              "C-60,-46 -62,-34 -64,-22 Z"),
        hshade="M36,-140 C76,-100 80,-60 70,-20 L130,-20 L130,-140 Z",
        golge="M38,-120 C62,-80 62,-30 62,6 C60,36 50,60 28,92 L120,120 L120,-120 Z",
        strands=["M64,-22 C64,-40 62,-56 56,-70", "M-64,-22 C-66,-40 -66,-56 -62,-70", "M45,-45 C42,-58 36,-70 26,-80", "M13,-46 C10,-58 4,-70 -6,-80", "M-16,-46 C-20,-58 -26,-68 -34,-76", "M-45,-47 C-48,-58 -52,-66 -58,-72"]),
    "3q": dict(
        face=("M-62,-40 C-66,-100 -20,-116 14,-114 C54,-112 78,-88 78,-44 C80,-24 84,-2 80,18 "
              "C78,36 70,54 58,66 C48,76 36,83 22,85 C10,86 -2,83 -12,77 C-30,66 -46,50 -54,30 "
              "C-60,14 -62,-8 -62,-40 Z"),
        ears=[(-58, 6, -1)], eyes=[(6, 2, 18, False), (58, 1, 12, True)],
        nose=(42, 32), mouth=(32, 54, 12),
        hair=("M-66,-24 C-76,-96 -30,-126 16,-124 C58,-122 84,-96 80,-54 C82,-48 84,-44 86,-40 "
              "C81,-40 77,-42 74,-44 C74,-52 70,-60 64,-64 C64,-56 61,-50 56,-45 C54,-56 48,-64 40,-68 "
              "C40,-58 35,-52 28,-47 C26,-59 18,-67 8,-70 C6,-60 1,-54 -5,-50 C-7,-60 -14,-66 -23,-67 "
              "C-24,-58 -28,-52 -34,-47 C-38,-52 -41,-48 -42,-40 L-42,-24 C-46,-14 -52,-8 -58,-8 Z"),
        hshade="M46,-140 C84,-104 92,-70 82,-36 L130,-36 L130,-140 Z",
        golge="M52,-120 C70,-80 66,-40 68,-12 C70,18 62,50 40,96 L130,120 L130,-120 Z",
        strands=["M56,-45 C54,-58 48,-70 38,-80", "M28,-47 C25,-60 18,-72 8,-82", "M-5,-50 C-8,-62 -14,-72 -22,-82", "M-34,-47 C-38,-58 -42,-66 -48,-72"]),
    "side": dict(
        face=("M-70,-40 C-74,-100 -28,-118 10,-114 C44,-110 62,-90 64,-52 L65,-28 C68,-20 68,-12 66,-6 "
              "C70,2 76,10 80,16 C79,22 74,24 70,24 C72,29 72,33 70,36 L68,41 L70,46 C70,51 68,54 66,56 "
              "C70,63 70,71 66,77 C58,86 44,88 30,86 C14,84 2,80 -8,72 C-26,58 -50,42 -62,20 C-68,6 -72,-14 -70,-40 Z"),
        ears=[(-16, 4, -1)], eyes=[(50, 0, 11, True)],
        nose=None, mouth=(62, 43, 4),
        hair=("M-76,-22 C-82,-100 -30,-126 12,-124 C52,-120 72,-100 70,-62 C70,-54 68,-48 64,-43 "
              "C62,-53 58,-59 50,-63 C50,-55 46,-49 40,-45 C38,-57 30,-65 20,-69 C10,-67 2,-61 -2,-53 "
              "L0,-20 L-8,-18 C-14,-10 -28,-8 -40,-6 C-44,-2 -48,2 -52,6 C-54,0 -56,-2 -60,-2 C-64,4 -68,10 -72,12 C-74,4 -75,-8 -76,-22 Z"),
        hshade="M-90,-60 C-84,-20 -70,0 -50,10 L-90,20 Z",
        golge="M-62,16 C-40,44 -14,64 10,80 L-80,120 Z",
        strands=["M64,-43 C62,-58 54,-70 42,-80", "M40,-45 C36,-58 28,-68 16,-76", "M-52,6 C-54,-10 -56,-24 -62,-36"]),
}


def kafa(spec=None, view="3q", ifade="odak", look=None):
    """11 yaş Michael. Merkez (0,0), yükseklik ~215 (saç üstü -130, çene ~86). view: front|3q|side. Sağa bakar.
    Yetişkin v4 (yetiskin.kafa) ile aynı göz/kaş/burun/ağız yardımcıları ve aynı 2 tonlu sıcak cel gölge."""
    sp = dict(MICHAEL_COCUK_V2); sp.update(spec or {})
    for k_ in ("skin_sh", "skin_dk", "skin_hl", "iris_d"):
        sp.setdefault(k_, MICHAEL_COCUK_V2[k_])
    sk = sp["skin"]; sh = sp["skin_sh"]; dk = sp["skin_dk"]; hl = sp["skin_hl"]; hair = sp["hair"]
    bi, bo, lu, ll, mk, extra = IFADE_C.get(ifade, IFADE_C["odak"])
    lk = 0.25 if look is None else look
    G = GEO[view]; face = G["face"]
    o = []; late = []
    cid = Y._uid("cf"); bid = Y._uid("cb"); hid = Y._uid("ch")
    o.append(f'<defs><clipPath id="{cid}"><path d="{face}"/></clipPath><clipPath id="{hid}"><path d="{G["hair"]}"/></clipPath>'
             f'<filter id="{bid}" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="2.4"/></filter></defs>')
    kul = []
    for ex, ey, s_ in G["ears"]:   # yetişkinle aynı kulak biçimi
        kul.append(f'<path d="M{ex+s_*4},{ey-22} C{ex+s_*19},{ey-25} {ex+s_*21},{ey+4} {ex+s_*13},{ey+21} C{ex+s_*9},{ey+28} {ex+s_*2},{ey+27} {ex},{ey+19} Z" '
                   f'fill="{sk}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
                   f'<path d="M{ex+s_*7},{ey-12} C{ex+s_*14},{ey-12} {ex+s_*14},{ey+7} {ex+s_*8},{ey+13}" stroke="{sh}" stroke-width="3" fill="none"/>')
    if view != "side": o += kul
    o.append(f'<path d="{face}" fill="{sk}"/>')
    # 2 tonlu sıcak cel gölge (yetişkinle aynı yaklaşım), sakal gölgesi yok; yanak dolgunluğu = yumuşak ışık, pembe yok
    g = [f'<path d="{G["golge"]}" fill="{sh}"/>',
         f'<path d="M-90,{80 if view!="side" else 78} C-20,100 40,100 120,60 L120,140 L-90,140 Z" fill="{sh}"/>',
         f'<ellipse cx="-28" cy="-46" rx="44" ry="40" fill="{hl}" opacity="0.22" filter="url(#{bid})"/>',
         f'<path d="M-90,-58 C-30,-40 30,-40 120,-62 L120,-140 L-90,-140 Z" fill="{sh}" opacity="0.45" filter="url(#{bid})"/>']  # perçem gölgesi alında
    if view == "3q":
        g.append(f'<ellipse cx="-18" cy="40" rx="20" ry="12" fill="{hl}" opacity="0.14" filter="url(#{bid})"/>'
                 f'<path d="M-62,-30 C-54,-10 -52,10 -54,30 L-70,30 Z" fill="{sh}" opacity="0.5"/>')
    elif view == "front":
        g.append(f'<ellipse cx="-36" cy="38" rx="16" ry="10" fill="{hl}" opacity="0.14" filter="url(#{bid})"/>')
    for ex, ey, ew, uz in G["eyes"]:   # çok hafif göz çukuru
        g.append(f'<ellipse cx="{ex+1}" cy="{ey-10}" rx="{ew*1.3:.1f}" ry="{ew*0.6:.1f}" fill="{dk}" opacity="0.08" filter="url(#{bid})"/>')
    o.append(f'<g clip-path="url(#{cid})">{"".join(g)}</g>')
    o.append(f'<path d="{face}" fill="none" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>')
    # saç: dağınık perçem; iç kenarı yetişkinin alın hattını izler, uçlar alına düşer
    hh = [f'<path d="{G["hshade"]}" fill="#000" opacity="0.28"/>',
          f'<path d="M-46,-104 C-14,-122 26,-120 56,-106" stroke="{shade(hair,3.4)}" stroke-width="6" fill="none" opacity="0.16" filter="url(#{bid})"/>']
    hh.insert(0, f'<ellipse cx="-14" cy="-108" rx="46" ry="14" fill="{shade(hair,2.6)}" opacity="0.2" filter="url(#{bid})"/>')
    hh += [f'<path d="{st}" stroke="#000" stroke-width="2.2" fill="none" stroke-linecap="round" opacity="0.45"/>' for st in G["strands"]]
    hh += [f'<path d="{st}" transform="translate(-5,-1)" stroke="{shade(hair,3.0)}" stroke-width="1.6" fill="none" stroke-linecap="round" opacity="0.28"/>' for st in G["strands"]]
    o.append(f'<path d="{G["hair"]}" fill="{hair}"/><g clip-path="url(#{hid})">{"".join(hh)}</g>'
             f'<path d="{G["hair"]}" fill="none" stroke="{INK}" stroke-width="4.2" stroke-linejoin="round"/>')
    if view == "side": o += kul
    # gözler: yetişkinin badem gözü, cocuk=True; ×1.1 ölçek, %15 daha açık
    plan = extra == "plan"
    for k, (ex, ey, ew, uz) in enumerate(G["eyes"]):
        w = ew * 1.1; eh = ew * 0.72 * 1.15
        o.append(Y._goz(ex, ey, w, eh, lu, ll, sp["iris"], sp["iris_d"], lk, sk, uzak=uz, cocuk=True))
        ix = ex + lk * w * 0.4; ir = eh * 1.05
        if extra == "korku":   # gözbebeği küçülür (iris büyük görünür, bakış donuk)
            o.append(f'<circle cx="{ix:.1f}" cy="{ey+0.5:.1f}" r="{ir*0.4:.1f}" fill="{sp["iris"]}"/>'
                     f'<circle cx="{ix:.1f}" cy="{ey+0.5:.1f}" r="{ir*0.2:.1f}" fill="#0E0B09"/>'
                     f'<circle cx="{ix-ir*0.36:.1f}" cy="{ey-ir*0.3:.1f}" r="{max(1.4, ir*0.22):.1f}" fill="#FFFFFF"/>')
        if plan:   # yetişkinle aynı plan yansıması
            late.append(f'<circle cx="{ix:.1f}" cy="{ey+0.5:.1f}" r="{eh*0.9:.1f}" fill="{PLAN}" opacity="0.6"/>'
                        f'<path d="M{ix-eh*0.6:.1f},{ey+eh*0.1:.1f} h{eh*0.45:.1f} v{-eh*0.45:.1f} h{eh*0.5:.1f}" stroke="#E8FCFF" stroke-width="1.5" fill="none" opacity="0.95"/>'
                        f'<circle cx="{ix-eh*0.32:.1f}" cy="{ey-eh*0.28:.1f}" r="{max(1.5,eh*0.26):.1f}" fill="#FFFFFF"/>')
        if view == "front": yon = 1 if ex < 0 else -1
        elif view == "3q": yon = 1 if k == 0 else -1
        else: yon = 1
        late.append(Y._kas(ex, ey - eh * 1.6, ew * (0.85 if uz else 1.0), bi, bo, sp["brow"], yon, ince=uz, olcek=0.8))
    if G["nose"]: o.append(Y._burun(*G["nose"], view=view, skin=sk, cocuk=True))
    mx, my, mw = G["mouth"]
    if view == "side":   # yandan: kontura dayanan kısa, düz dudak çizgisi (kanca yok)
        o.append(f'<path d="M{mx-7},{my+0.5} L{mx+5},{my-0.5}" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>'
                 + (f'<path d="M{mx-7},{my-1} l-2,-3" stroke="{dk}" stroke-width="1.8" stroke-linecap="round" opacity="0.6"/>' if mk == "yarim" else "")
                 + (f'<ellipse cx="{mx-1}" cy="{my+2}" rx="3" ry="4" fill="#3E1A14" stroke="{INK}" stroke-width="2"/>' if mk == "open_s" else ""))
    else:
        o.append(Y._agiz(mx, my, mw, mk, sk))
    if extra == "korku":   # ter damlası (şakak)
        tx = {"front": 50, "3q": 70, "side": 40}[view]
        late.append(f'<path d="M{tx},-30 q-5,10 0,14 q5,-4 0,-14 Z" fill="#DDEFFF" stroke="#6E93B3" stroke-width="1.6" opacity="0.9"/>')
    if extra == "tear":
        ex, ey, ew, _ = G["eyes"][0]
        o.append(f'<path d="M{ex+4},{ey+17} C{ex+7},{ey+28} {ex+3},{ey+36} {ex+4},{ey+44}" stroke="#CDEBFF" stroke-width="3.5" fill="none" stroke-linecap="round" opacity="0.9"/>'
                 f'<ellipse cx="{ex+4}" cy="{ey+48}" rx="3.6" ry="5" fill="#CDEBFF" stroke="#5A8AB0" stroke-width="1.6"/>')
    return "".join(o) + "".join(late)


# ───────────────────────── figür: ince 11 yaş, büyük gelen soluk tişört ─────────────────────────
_uc = K._uc; _seg = K._seg
POZ_DUR = dict(govde=2, bas=0, kol_on=(6, -4), kol_arka=(-14, 10), bacak_on=(3, 0), bacak_arka=(-5, 5), el_on="relax", el_arka="relax")
POZ_KORKU = dict(govde=-4, bas=-6, kol_on=(-10, 120), kol_arka=(-14, 110), bacak_on=(2, 0), bacak_arka=(-4, 4), el_on="fist", el_arka="fist")


def figur(spec=MICHAEL_COCUK_V2, ifade="odak", poz=None, plan=False):
    """11 yaş Michael, ayakta 3/4, sağa bakar, yer y=0. Boy ~ 450 (yetişkin figür2 ~ 560 → oran 0.8).
    Kafa/boy ≈ 1/3.4 (yetişkin 1/4.1): çocukta baş görece büyük, uzuvlar ince, boyun ince."""
    p = dict(POZ_DUR); p.update(poz or {})
    sk = spec["skin"]; sh = spec["shirt"]; sd = spec["shirt_d"]
    TH, SN = 86, 84; UA, FA = 66, 60; TOR = 136
    def ayak_y(t, k):
        kx, ky = _uc(0, 0, t, TH); ax, ay = _uc(kx, ky, t - k, SN); return ay
    hip = (0, -max(ayak_y(*p["bacak_on"]), ayak_y(*p["bacak_arka"])) - 20)
    g = math.radians(p["govde"])
    def tw(lx, ly):
        return hip[0] + lx * math.cos(g) - ly * math.sin(g), hip[1] + lx * math.sin(g) + ly * math.cos(g)
    sh_on, sh_ark = tw(30, -TOR + 20), tw(-34, -TOR + 24)
    neck = tw(6, -TOR - 4)
    o = [f'<ellipse cx="0" cy="4" rx="78" ry="12" fill="#000" opacity="0.25"/>']
    def bacak(side, t, k, ton, on):
        hx, hy = tw(side * 18, 0)
        kx, ky = _uc(hx, hy, t, TH); ax, ay = _uc(kx, ky, t - k, SN)
        out = _seg((hx, hy), (kx, ky), 34, ton) + _seg((kx, ky), (ax, ay), 30, ton)
        if on:  # dizde yama (eskimiş kot)
            out += (f'<rect x="{kx-11:.1f}" y="{ky-10:.1f}" width="22" height="20" rx="3" fill="{shade(ton,1.18)}" stroke="{INK}" stroke-width="2.2" '
                    f'transform="rotate({-(t)*0.6:.0f} {kx:.1f} {ky:.1f})"/>'
                    f'<path d="M{kx-8:.1f},{ky-6:.1f} l3,0 m3,0 l3,0 m3,0 l3,0" stroke="{shade(ton,1.6)}" stroke-width="1.4"/>')
        # paça kıvrımı + eski spor ayakkabı (beyaz taban)
        out += (f'<g transform="rotate({max(-25, min(25, (t-k)*0.5)):.0f} {ax:.0f} {ay:.0f})">'
                f'<path d="M{ax-17:.0f},{ay-9:.0f} L{ax+16:.0f},{ay-9:.0f} Q{ax+36:.0f},{ay-2:.0f} {ax+36:.0f},{ay+12:.0f} L{ax-19:.0f},{ay+12:.0f} Z" fill="{spec["shoe"]}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
                f'<path d="M{ax-19:.0f},{ay+12:.0f} L{ax+36:.0f},{ay+12:.0f} L{ax+35:.0f},{ay+19:.0f} L{ax-19:.0f},{ay+19:.0f} Z" fill="{spec["sole"]}" stroke="{INK}" stroke-width="3.4" stroke-linejoin="round"/>'
                f'<path d="M{ax+2:.0f},{ay-6:.0f} l6,6 m2,-6 l6,6" stroke="{spec["sole"]}" stroke-width="1.6" opacity="0.7"/></g>'
                f'<path d="M{ax-17:.0f},{ay-20:.0f} L{ax+17:.0f},{ay-20:.0f}" stroke="{INK}" stroke-width="3" opacity="0.8"/>')
        return out
    def kol(sp, oa, da, ten, el, renk, yan):
        """yan: gövdenin bu omuza göre yönü (+1 sağda, -1 solda). Kol ve omuz tek parça: kumaş gövdeye taşar,
        gövde tarafında kontur yok; büyük tişörtün düşük omuz dikişi üst kolda."""
        ex, ey = _uc(*sp, oa, UA); wx, wy = _uc(ex, ey, oa + da, FA)
        out = _seg(sp, (ex, ey), 24, ten) + _seg((ex, ey), (wx, wy), 21, ten)
        Ls = UA * 0.72; i = yan   # iç taraf (gövde) yönü, yerel x
        fill = (f"M{i*34},-20 C{i*10},-22 {-i*18},-16 {-i*25},-2 C{-i*28},{Ls*0.45:.0f} {-i*27},{Ls*0.8:.0f} {-i*25},{Ls:.0f} "
                f"Q0,{Ls+7:.0f} {i*24},{Ls-2:.0f} C{i*24},{Ls*0.7:.0f} {i*22},{Ls*0.4:.0f} {i*30},{Ls*0.25:.0f} L{i*40},{Ls*0.1:.0f} Z")
        # tek kontur: omuz üstü → dış yan → etek; gövde tarafında (iç yan) kontur YOK, yalnız ince koltuk kıvrımı
        dis = (f"M{i*30},-21 C{i*10},-22 {-i*18},-16 {-i*25},-2 C{-i*28},{Ls*0.45:.0f} {-i*27},{Ls*0.8:.0f} {-i*25},{Ls:.0f} "
               f"Q0,{Ls+7:.0f} {i*22},{Ls-2:.0f}")
        out += (f'<g transform="translate({sp[0]:.1f},{sp[1]:.1f}) rotate({-oa:.1f})">'
                f'<path d="{fill}" fill="{renk}"/>'
                f'<path d="{dis}" fill="none" stroke="{INK}" stroke-width="4" stroke-linejoin="round" stroke-linecap="round"/>'
                f'<path d="M{-i*24},{Ls*0.3:.0f} Q{-i*4},{Ls*0.36:.0f} {i*10},{Ls*0.3:.0f}" stroke="{shade(renk,0.72)}" stroke-width="1.5" fill="none" stroke-dasharray="3 3" stroke-linecap="round"/>'
                f'<path d="M{i*22},{Ls-2:.0f} C{i*24},{Ls-10:.0f} {i*23},{Ls-16:.0f} {i*26},{Ls-22:.0f}" stroke="{shade(renk,0.62)}" stroke-width="2.4" fill="none" stroke-linecap="round"/>'
                f'<path d="M{-i*18},{Ls-3:.0f} Q0,{Ls+2:.0f} {i*19},{Ls-5:.0f}" stroke="{shade(renk,0.72)}" stroke-width="3" fill="none"/>'
                f'<path d="M{i*14},{Ls*0.45:.0f} Q{i*8},{Ls*0.7:.0f} {i*12},{Ls-6:.0f}" stroke="{shade(renk,0.8)}" stroke-width="2.5" fill="none" opacity="0.8"/></g>')
        hx, hy = _uc(wx, wy, oa + da, 10)
        if el == "relax":
            out += f'<g transform="rotate({180-(oa+da):.1f} {hx:.1f} {hy:.1f})">{hand3(hx, hy, 16, ten, "open", -1)}</g>'
        else:
            out += f'<g transform="rotate({-(oa+da)*0.6:.1f} {hx:.1f} {hy:.1f})">{hand3(hx, hy, 16, ten, el, 1)}</g>'
        return out
    o.append(bacak(-1, *p["bacak_arka"], spec["pants_d"], False))
    o.append(kol(sh_ark, *p["kol_arka"], shade(sk, 0.86), p["el_arka"], sd, 1))
    o.append(bacak(1, *p["bacak_on"], spec["pants"], True))
    # gövde: dar omuzlu çocuk gövdesi, tişört kalçanın altına sarkar, etek ucu dalgalı
    W1, W2 = 44, 46
    torso = (f"M{-W1:.0f},{-TOR+12:.0f} Q{-W1-6:.0f},{-TOR*0.55:.0f} {-W2:.0f},{-TOR*0.15:.0f} L{-W2-4:.0f},{30:.0f} "
             f"Q{-20:.0f},{38:.0f} 0,{33:.0f} Q20,{40:.0f} {W2+6:.0f},{28:.0f} L{W2+2:.0f},{-TOR*0.15:.0f} Q{W1+8:.0f},{-TOR*0.55:.0f} {W1:.0f},{-TOR+12:.0f} "
             f"Q0,{-TOR-10:.0f} {-W1:.0f},{-TOR+12:.0f} Z")
    tid = f"cv{abs(hash((sh, p['govde']))) % 10**7}"
    inner = [f'<rect x="{W2-16:.0f}" y="{-TOR-40:.0f}" width="80" height="{TOR+90:.0f}" fill="{sd}"/>',
             # bol kumaş kırışıkları
             f'<path d="M{-W2+8},{-TOR*0.3:.0f} Q-6,{-TOR*0.18:.0f} 14,{-TOR*0.32:.0f} M{-W2+4},{10} Q-10,{-2} 10,{14} M8,{-TOR*0.62:.0f} Q20,{-TOR*0.5:.0f} 30,{-TOR*0.64:.0f}" '
             f'stroke="{shade(sh,0.78)}" stroke-width="3" fill="none" opacity="0.8" stroke-linecap="round"/>',
             # solmuş iki şerit (v1 çizgili tişörtün izi), yer yer silinmiş
             f'<g opacity="0.35"><rect x="-80" y="{-TOR*0.62:.0f}" width="160" height="7" fill="{spec["shirt_hl"]}"/>'
             f'<rect x="-80" y="{-TOR*0.62+14:.0f}" width="160" height="7" fill="{spec["shirt_hl"]}"/>'
             f'<path d="M-20,{-TOR*0.64:.0f} l10,26 M18,{-TOR*0.64:.0f} l-6,26" stroke="{sh}" stroke-width="6"/></g>',
             # etek ucunda küçük yırtık
             f'<path d="M{W2-14},34 l4,-10 l5,9" fill="{shade(sh,0.45)}" stroke="{INK}" stroke-width="1.6"/>',
             f'<path d="M{-W1+8:.0f},{-TOR+26:.0f} Q{-W2+6:.0f},{-TOR*0.45:.0f} {-W2+6:.0f},0" stroke="#FFFFFF" stroke-width="8" fill="none" opacity="0.13"/>']
    o.append(f'<g transform="translate({hip[0]:.1f},{hip[1]:.1f}) rotate({p["govde"]})">'
             f'<defs><clipPath id="{tid}"><path d="{torso}"/></clipPath></defs><path d="{torso}" fill="{sh}"/>'
             f'<g clip-path="url(#{tid})">{"".join(inner)}</g><path d="{torso}" fill="none" stroke="{INK}" stroke-width="4.5" stroke-linejoin="round"/></g>')
    # baş + ince boyun + gerilmiş yaka (boyun gövdenin üstünde, yaka boynun üstünde)
    hx, hy = _uc(*neck, 180 + p["govde"] * 0.3 + p["bas"] * 0.3, 60)
    o.append(_seg((neck[0], neck[1] + 6), (neck[0] + (hx - neck[0]) * 0.55, neck[1] + (hy - neck[1]) * 0.55), 22, shade(sk, 0.82)))
    nx_, ny_ = tw(6, -TOR + 4)
    o.append(f'<g transform="translate({nx_:.1f},{ny_:.1f}) rotate({p["govde"]})">'
             f'<path d="M-22,-10 Q-20,18 2,22 Q24,18 26,-10 Z" fill="{shade(sk,0.8)}"/>'
             f'<path d="M-22,-10 Q-20,18 2,22 Q24,18 26,-10" stroke="{INK}" stroke-width="10" fill="none" stroke-linecap="round"/>'
             f'<path d="M-22,-10 Q-20,18 2,22 Q24,18 26,-10" stroke="{shade(sh,0.88)}" stroke-width="4" fill="none" stroke-linecap="round"/></g>')
    o.append(f'<g transform="translate({hx:.1f},{hy:.1f}) rotate({p["govde"]*0.4 + p["bas"]:.1f}) scale(0.6)">{kafa(spec, "3q", ifade)}</g>')
    o.append(kol(sh_on, *p["kol_on"], sk, p["el_on"], sh, -1))
    return "".join(o)


# ───────────────────────── kart ─────────────────────────
def kart(out=A / "cocuk_kart"):
    S = MICHAEL_COCUK_V2
    o = ['<rect width="1280" height="720" fill="#252B33"/>',
         '<radialGradient id="gl" cx="0.5" cy="0.45" r="0.6"><stop offset="0" stop-color="#3A424C"/><stop offset="1" stop-color="#252B33"/></radialGradient>',
         '<ellipse cx="150" cy="420" rx="150" ry="290" fill="url(#gl)"/>']
    def t(x, y, s, size=14, c="#D8D2C6", anchor="middle", w="normal"):
        o.append(f'<text x="{x}" y="{y}" font-family="DejaVu Sans" font-size="{size}" font-weight="{w}" fill="{c}" text-anchor="{anchor}">{s}</text>')
    t(24, 34, "MICHAEL · 11 yaş · çocuk kafası v3 (yetişkin v4 sistemiyle)", 20, "#F0EBE2", "start")
    # tam figür
    o.append(f'<g transform="translate(150,676)">{figur(S, "odak")}</g>')
    t(150, 706, "tam figür · büyük gelen soluk tişört")
    # 3 görünüş
    for i, v in enumerate(("front", "3q", "side")):
        x = 360 + i * 150
        o.append(f'<g transform="translate({x},150) scale(0.5)">{kafa(S, v, "odak")}</g>')
        t(x, 222, {"front": "önden", "3q": "3/4", "side": "yandan"}[v])
    # 5 ifade
    for i, (f, ad) in enumerate((("korku", "korku"), ("odak", "odak"), ("plan", "plan görüşü"), ("sefkat", "şefkat"), ("yas", "yas"))):
        x = 330 + i * 118
        o.append(f'<g transform="translate({x},330) scale(0.42)">{kafa(S, "3q", f)}</g>')
        t(x, 392, ad, 13, PLAN if f == "plan" else "#D8D2C6")
    # önce / sonra
    o.append('<rect x="300" y="420" width="300" height="270" rx="10" fill="#1E232A"/>')
    o.append(f'<g transform="translate(380,550) scale(0.62)">{K.kafa(K.MICHAEL_COCUK, "3q", "odak")}</g>')
    o.append(f'<g transform="translate(520,550) scale(0.62)">{kafa(S, "3q", "odak")}</g>')
    t(380, 640, "önce (v1)"); t(520, 640, "sonra (v3)", 14, "#F0EBE2", w="bold")
    t(450, 676, "aynı göz/kaş/burun sistemi · dağınık perçem · büyük alın", 11, "#A9A296")
    # süreklilik: aynı kişi mi?
    o.append('<rect x="630" y="420" width="400" height="270" rx="10" fill="#1E232A"/>')
    o.append(f'<g transform="translate(730,550) scale(0.62)">{kafa(S, "3q", "odak")}</g>')
    o.append(f'<g transform="translate(925,545) scale(0.7)">{Y.kafa(Y.MICHAEL_Y, "3q", "odak")}</g>')
    t(730, 640, "11 yaş"); t(925, 640, "yetişkin (Fox River)")
    t(830, 676, "aynı iris · aynı düz kaş · aynı saç çizgisi · aynı kulak · aynı burun", 11, "#A9A296")
    # yetişkin figür ile boy oranı
    o.append(f'<g transform="translate(1185,676) scale(0.74)">{Y.figur(K.MICHAEL, "odak", numara_goster=True)}</g>')
    o.append(f'<g transform="translate(1100,676) scale(0.74)">{figur(S, "odak")}</g>')
    t(1160, 706, "boy: 11 yaş / yetişkin ≈ 0.8", 11, "#A9A296")
    # 168 px okunurluk kontrolü (küçük boyda ifade)
    for i, f in enumerate(("korku", "plan", "sefkat", "yas")):
        x = 905 + i * 92
        o.append(f'<g transform="translate({x},150) scale(0.38)">{kafa(S, "3q", f)}</g>')
    t(1043, 222, "küçük boy (~84 px kafa) okunurluk", 11, "#A9A296")
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720" viewBox="0 0 1280 720">{"".join(o)}</svg>'
    sv = f"/tmp/{Path(str(out)).name}.svg"; Path(sv).write_text(svg)
    subprocess.run(["rsvg-convert", "-w", "1280", "-o", f"{out}.png", sv], check=True)
    return f"{out}.png"


def buyuk(out=A / "cocuk_buyuk"):
    """İnceleme için büyük kafa sayfası (öz değerlendirme)."""
    S = MICHAEL_COCUK_V2; o = ['<rect width="1280" height="720" fill="#252B33"/>']
    for i, v in enumerate(("front", "3q", "side")):
        o.append(f'<g transform="translate({200+i*300},190)">{kafa(S, v, "odak")}</g>')
    for i, f in enumerate(("korku", "odak", "plan", "sefkat", "yas")):
        o.append(f'<g transform="translate({140+i*250},530) scale(0.85)">{kafa(S, "3q", f)}</g>')
    o.append(f'<g transform="translate(1130,190) scale(0.9)">{Y.kafa(Y.MICHAEL_Y, "3q", "odak")}</g>')
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720">{"".join(o)}</svg>'
    sv = f"/tmp/{Path(str(out)).name}.svg"; Path(sv).write_text(svg)
    subprocess.run(["rsvg-convert", "-w", "1280", "-o", f"{out}.png", sv], check=True)
    return f"{out}.png"


def kucuk(out=A / "cocuk_168"):
    """168 px kafa yüksekliğinde ifade okunurluk kontrolü (sahnede yakın plan değil, orta plan boyu)."""
    S = MICHAEL_COCUK_V2; o = ['<rect width="960" height="220" fill="#1B1F25"/>']
    for i, f in enumerate(("korku", "odak", "plan", "sefkat", "yas")):
        o.append(f'<g transform="translate({96+i*192},116) scale(0.76)">{kafa(S, "3q", f)}</g>')
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="960" height="220">{"".join(o)}</svg>'
    sv = f"/tmp/{Path(str(out)).name}.svg"; Path(sv).write_text(svg)
    subprocess.run(["rsvg-convert", "-w", "960", "-o", f"{out}.png", sv], check=True)
    return f"{out}.png"


def sureklilik(out=A / "sureklilik"):
    """Üst sıra 11 yaş, alt sıra yetişkin v4: aynı görünüş/ifade çiftleri."""
    S = MICHAEL_COCUK_V2
    o = ['<rect width="1280" height="720" fill="#252B33"/>',
         '<text x="24" y="36" font-family="DejaVu Sans" font-size="20" fill="#F0EBE2">Süreklilik · üst: 11 yaş (cocuk.kafa) · alt: yetişkin v4 (yetiskin.kafa)</text>']
    for i, (v, f, ad) in enumerate((("3q", "odak", "3/4 · odak"), ("front", "odak", "önden · odak"), ("3q", "korku", "3/4 · korku"),
                                     ("3q", "sefkat", "3/4 · şefkat"), ("3q", "yas", "3/4 · yas"))):
        x = 140 + i * 250
        o.append(f'<g transform="translate({x},205) scale(1.0)">{kafa(S, v, f)}</g>')
        o.append(f'<g transform="translate({x},505) scale(1.0)">{Y.kafa(Y.MICHAEL_Y, v, f)}</g>')
        o.append(f'<text x="{x}" y="700" font-family="DejaVu Sans" font-size="16" fill="#D8D2C6" text-anchor="middle">{ad}</text>')
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720">{"".join(o)}</svg>'
    sv = f"/tmp/{Path(str(out)).name}.svg"; Path(sv).write_text(svg)
    subprocess.run(["rsvg-convert", "-w", "1280", "-o", f"{out}.png", sv], check=True)
    return f"{out}.png"


if __name__ == "__main__":
    print(buyuk()); print(kucuk()); print(kart()); print(sureklilik())
