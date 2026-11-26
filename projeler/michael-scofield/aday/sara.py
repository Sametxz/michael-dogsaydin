"""Dr. Sara Tancredi kafa/yüz tasarımı (karakter.kafa ile aynı imza, drop-in).
Michael'ın onaylı stilinde (2 ton sıcak cel, temiz çizgi, canlı badem göz, koyu kontur, ışık sol üstten)
ama ayrı çizilmiş KADIN yüz yapısı: yumuşak çene, ince çene ucu, yumuşak elmacık, açık badem göz + kirpik,
ince kavisli kaş, küçük burun, dolgun renkli dudak, sıcak yanak. Saç: hacimli, dalgalı, omuza dökülen,
yandan ayrık; uzun tutamlar YÜZÜN ARKASINDA çizilir (yüz tam görünür), önde yalnız alın üstü perçem.
Hiçbir gerçek kişinin yüzü örnek alınmadı; stilize özgün yüz.
Kullanım: python3 sara.py  ->  sara_kart.png (1280x720)
"""
import subprocess, sys
from pathlib import Path
P = Path(__file__).resolve().parent; PROJ = P.parent; REPO = PROJ.parents[1]
sys.path[:0] = [str(P), str(PROJ), str(REPO / "r3"), str(REPO / "r2")]
from art2 import shade
import karakter as K
import yetiskin as Y

INK = Y.INK; PLAN = Y.PLAN; _uid = Y._uid
SARA_Y = dict(K.SARA, skin="#EDB896", skin_sh="#D2967A", skin_dk="#B07560", skin_hl="#FFE4CC",
              hair="#8E3A26", brow="#6A2A1C", iris="#8CBF84", iris_d="#2F4D31", dudak="#C8655A")

# ifade: kaş_iç (yukarı +), kaş_dış, üst_kapak, alt_kapak, ağız, ekstra
IFADE = {
    "odak":    (1, 2, 0.06, 0.06, "hafif", ""),
    "kararli": (-6, 1, 0.22, 0.16, "siki", ""),
    "yas":     (10, -5, 0.28, 0.04, "tremble", "tear"),
    "korku":   (12, 8, 0.0, 0.0, "acik", ""),
    "sefkat":  (6, 3, 0.10, 0.20, "gulus", ""),
    "ofke":    (-10, 5, 0.24, 0.20, "ofke", ""),
    "plan":    (1, 2, 0.08, 0.06, "hafif", "plan"),
    "neutral": (0, 1, 0.12, 0.06, "duz", ""),
}

# ───────────── geometri (kafa birimi; merkez 0,0; saç üstü ~-124, çene ~93) ─────────────
FACE = {
    "front": ("M-57,-40 C-59,-96 -30,-112 0,-112 C30,-112 59,-96 57,-40 C59,-14 59,8 55,28 "
              "C51,50 42,70 28,82 C19,88 9,91 0,91 C-9,91 -19,88 -28,82 C-42,70 -51,50 -55,28 "
              "C-59,8 -59,-14 -57,-40 Z"),
    "3q":    ("M-57,-40 C-61,-98 -18,-114 14,-112 C50,-110 71,-88 71,-46 L70,-28 C75,-18 76,-6 71,4 "
              "C71,22 67,38 60,54 C53,68 42,82 28,89 C20,93 12,93 6,90 C-8,84 -21,74 -31,62 "
              "C-45,46 -55,22 -57,-40 Z"),
    "side":  ("M-64,-40 C-68,-98 -24,-116 12,-112 C46,-108 61,-86 61,-54 C62,-40 62,-30 63,-22 "
              "C65,-12 70,-2 76,8 C79,13 79,18 75,20 C72,21 70,22 70,24 C72,26 73,29 72,32 "
              "C71,34 70,35 69,36 C71,38 72,41 70,44 C67,46 65,48 66,52 C69,61 67,72 58,79 "
              "C48,86 32,88 16,86 C0,82 -10,76 -20,66 C-40,46 -56,28 -60,10 C-64,-6 -66,-20 -64,-40 Z"),
}
# (x, y, yarı genişlik, uzak, ayna)  ayna: dış köşe solda -> göz aynalanır
EYES = {"front": [(-25, -5, 20.0, False, True), (25, -5, 20.0, False, False)],
        "3q":    [(7, -6, 20.5, False, True), (55, -7, 13.0, True, False)],
        "side":  [(50, -6, 11.0, True, True)]}
MOUTH = {"front": (0, 55, 13.5), "3q": (33, 55, 12.0), "side": None}
NOSE = {"front": (0, 31), "3q": (43, 29), "side": None}
BLUSH = {"front": [(-37, 27), (37, 27)], "3q": [(-12, 27), (60, 24)], "side": [(32, 24)]}
GOLGE = {"front": "M36,-120 C58,-80 56,-30 56,8 C54,40 44,64 22,98 L120,120 L120,-120 Z",
         "3q":    "M52,-120 C66,-80 62,-40 64,-14 C64,16 58,50 36,98 L130,120 L130,-120 Z",
         "side":  "M-60,14 C-40,44 -14,62 14,78 L-80,120 Z"}

# saç: tutam = (yol, arka gölge kayması dx) yüzün ARKASINDA; on = alın üstü perçem / kafatası (önde)
_LF = ("M-52,-80 C-82,-60 -92,-20 -88,14 C-85,40 -98,60 -100,90 C-102,116 -90,132 -98,156 C-86,154 -80,148 -76,142 "
       "C-74,154 -66,162 -54,166 C-60,152 -58,136 -50,126 C-44,112 -50,94 -46,74 C-42,54 -50,20 -50,-20 Z")
_LFD = ("M-84,-20 C-88,20 -80,40 -92,84 C-96,110 -86,128 -92,146 M-66,30 C-70,60 -62,84 -68,120 C-70,136 -66,146 -62,156")
SAC = {
 "front": dict(
    tutam=[(_LF, -10, False), (_LF, -10, True)],
    dalga=[_LFD, "AYNA"],
    on="M-62,26 C-78,2 -88,-36 -84,-72 C-78,-114 -40,-136 4,-134 C50,-132 88,-110 86,-70 C88,-36 78,0 62,26 "
       "C61,4 61,-20 60,-40 C58,-62 50,-80 26,-92 C10,-72 -16,-62 -40,-58 C-52,-54 -58,-46 -59,-36 C-60,-16 -61,4 -62,26 Z",
    parlak="M-50,-96 C-32,-116 -4,-122 20,-116", parlak2="M38,-110 C52,-102 62,-88 66,-70",
    on_dalga="M16,-104 C-4,-84 -28,-72 -52,-66 M40,-108 C54,-94 62,-72 64,-50 M-20,-122 C-46,-114 -66,-94 -72,-60 C-76,-30 -72,-6 -66,14 M60,-118 C76,-104 82,-80 80,-50"),
 "3q": dict(
    tutam=[("M-50,-84 C-90,-64 -100,-20 -96,16 C-92,44 -106,64 -108,94 C-110,120 -98,138 -106,162 C-94,160 -88,154 -84,148 "
            "C-82,160 -74,168 -62,172 C-68,158 -66,142 -58,132 C-50,116 -50,96 -40,76 C-30,60 -40,20 -40,-20 Z", -12, False),
           ("M62,-70 C86,-44 94,-6 90,30 C88,58 98,80 94,108 C92,128 84,140 76,146 C80,132 76,120 68,112 "
            "C60,96 62,72 58,50 Z", 8, False)],
    dalga=["M-86,-20 C-90,20 -84,40 -96,86 C-100,112 -90,130 -96,150 M-66,30 C-68,60 -60,84 -70,122 C-72,138 -68,150 -64,160",
           "M84,10 C86,40 82,66 90,96"],
    on="M-62,30 C-80,6 -90,-36 -86,-74 C-80,-114 -24,-138 20,-134 C64,-130 96,-104 92,-70 C92,-48 86,-34 77,-20 "
       "C75,-34 74,-44 73,-50 C70,-72 60,-86 40,-94 C22,-74 -4,-64 -28,-60 C-44,-56 -55,-46 -58,-34 C-60,-14 -60,8 -62,30 Z",
    parlak="M-44,-100 C-24,-120 6,-126 32,-120", parlak2="M54,-112 C68,-102 78,-88 80,-70",
    on_dalga="M30,-106 C10,-86 -16,-74 -44,-68 M56,-110 C68,-96 76,-76 78,-56 M-10,-126 C-40,-120 -66,-98 -74,-64 C-78,-34 -74,-6 -66,18 M74,-112 C86,-96 88,-74 84,-48"),
 "side": dict(
    tutam=[],
    dalga=[],
    on="M57,-90 C68,-106 42,-134 -10,-133 C-50,-131 -70,-114 -76,-92 C-98,-62 -98,-12 -96,22 C-94,50 -106,70 -106,98 C-106,124 -94,140 -102,164 "
       "C-90,162 -84,156 -80,150 C-78,162 -70,170 -58,174 C-64,160 -62,144 -54,134 C-46,120 -44,104 -36,88 "
       "C-28,72 -24,52 -22,30 C-20,10 -20,-6 -16,-18 C-8,-28 2,-38 10,-50 C22,-68 38,-80 57,-90 Z",
    parlak="M-56,-98 C-30,-118 6,-122 34,-114", parlak2="M-88,-30 C-92,0 -88,22 -90,44",
    on_dalga="M44,-110 C10,-116 -32,-106 -60,-72 M30,-90 C10,-80 -6,-64 -14,-44 "
             "M-84,-40 C-90,0 -84,30 -96,70 C-102,100 -90,126 -96,150 M-60,10 C-60,46 -54,80 -66,120 C-70,140 -64,152 -60,164"),
}


# ───────────── parçalar ─────────────
def _ayna(cx, inner, ayna):
    return f'<g transform="translate({2*cx:.1f},0) scale(-1,1)">{inner}</g>' if ayna else inner

def _goz(ex, ey, ew, uz, ayna, lu, ll, lk, sp, plan):
    eh = ew * (0.8 if not uz else 0.84)
    look = -lk if ayna else lk
    body = Y._goz(ex, ey, ew, eh, lu, ll, sp["iris"], sp["iris_d"], look, sp["skin"], uzak=uz, plan=plan, olcek=0.95)
    ly = ey - eh * 1.05 + 2.0 * eh * lu
    # kirpik çizgisi (dışa doğru kalınlaşan) + dış köşede 2 zarif kirpik
    lw = 3.2 if uz else 4.2
    body += (f'<path d="M{ex-ew*0.2:.1f},{ly+eh*0.05:.1f} Q{ex+ew*0.55:.1f},{ly-eh*0.05+eh*0.35*lu:.1f} {ex+ew+2:.1f},{ey-eh*0.12:.1f} '
             f'L{ex+ew+7:.1f},{ey-eh*0.55:.1f} Q{ex+ew*0.5:.1f},{ly-eh*0.38+eh*0.3*lu:.1f} {ex-ew*0.3:.1f},{ly-eh*0.05:.1f} Z" fill="{INK}"/>')
    return _ayna(ex, body, ayna), eh

def _goz_profil(ex, ey, lu, ll, sp, plan):
    """Profil göz: arka köşe sivri, ön kısım açık; iris yarım elips, kirpik öne-yukarı."""
    cid = _uid("gp"); top = ey - 9 + 14 * lu; bot = ey + 6 - 8 * ll
    shape = f"M{ex-11},{ey} C{ex-4},{top-1} {ex+4},{top-1} {ex+9},{top+2} C{ex+10},{ey} {ex+9},{bot-2} {ex+6},{bot} C{ex},{bot+1} {ex-6},{ey+3} {ex-11},{ey} Z"
    ir = sp["iris"] if not plan else PLAN
    return (f'<defs><clipPath id="{cid}"><path d="{shape}"/></clipPath></defs><path d="{shape}" fill="#F6F1EA"/>'
            f'<g clip-path="url(#{cid})"><ellipse cx="{ex+5}" cy="{ey-1}" rx="5" ry="7.5" fill="{ir}" stroke="{sp["iris_d"]}" stroke-width="1.6"/>'
            f'<ellipse cx="{ex+6.5}" cy="{ey-1}" rx="2" ry="3.6" fill="#0E0B09"/><circle cx="{ex+4}" cy="{ey-4}" r="1.6" fill="#FFF"/></g>'
            f'<path d="M{ex-12},{ey+0.5} C{ex-4},{top-2} {ex+4},{top-2} {ex+9},{top+1.5} L{ex+14},{top-4} L{ex+8},{top-2.5} C{ex+2},{top-5} {ex-6},{top-4} {ex-12},{ey+0.5} Z" fill="{INK}" stroke="{INK}" stroke-width="1.6" stroke-linejoin="round"/>'
            f'<path d="M{ex-9},{ey+2} C{ex-3},{bot+2} {ex+2},{bot+2} {ex+6},{bot+0.5}" stroke="{shade(sp["skin"],0.66)}" stroke-width="1.6" fill="none" opacity="0.7"/>'
            f'<path d="M{ex-8},{top-6} C{ex-2},{top-10} {ex+4},{top-9} {ex+8},{top-5}" stroke="{shade(sp["skin"],0.66)}" stroke-width="1.5" fill="none" opacity="0.45"/>')

def _kas(ex, ey, ew, ic, dis, color, ayna, uz):
    """İnce, kavisli kaş: iç uç yumuşak kalın, tepe dış 2/3'te, dış uç incelir. Ayna olmadan iç uç solda."""
    xi, xo = ex - ew * 0.95, ex + ew * 1.15
    yi, yo = ey - ic, ey + 3 - dis
    xp, yp = ex + ew * 0.45, min(yi, yo) - 6 - (dis - ic) * 0.15
    t = 4.6 if not uz else 3.6
    d = (f"M{xi:.1f},{yi+t*0.5:.1f} C{xi+ew*0.3:.1f},{yi-t*0.6:.1f} {xp-ew*0.3:.1f},{yp-t*0.5:.1f} {xp:.1f},{yp-t*0.45:.1f} "
         f"Q{xo-ew*0.2:.1f},{yp:.1f} {xo:.1f},{yo:.1f} "
         f"Q{xo-ew*0.3:.1f},{yp+t*0.9:.1f} {xp:.1f},{yp+t*0.55:.1f} C{xp-ew*0.4:.1f},{yp+t*0.6:.1f} {xi+ew*0.3:.1f},{yi+t*1.2:.1f} {xi:.1f},{yi+t*0.5:.1f} Z")
    return _ayna(ex, f'<path d="{d}" fill="{color}" stroke="{INK}" stroke-width="1.4" stroke-linejoin="round"/>', ayna)

def _burun(x, y, view, sk):
    dk = shade(sk, 0.68)
    if view == "front":
        return (f'<path d="M{x+4},{y-26} C{x+5},{y-16} {x+7},{y-8} {x+7},{y-3}" stroke="{dk}" stroke-width="2" fill="none" opacity="0.5" stroke-linecap="round"/>'
                f'<path d="M{x-6},{y+1} C{x-3},{y+4} {x+3},{y+4} {x+6},{y+1}" stroke="{INK}" stroke-width="2.8" fill="none" stroke-linecap="round"/>'
                f'<path d="M{x+9},{y-4} C{x+11},{y-1} {x+10},{y+1} {x+7},{y+2}" stroke="{dk}" stroke-width="2" fill="none" stroke-linecap="round"/>'
                f'<path d="M{x-9},{y-4} C{x-11},{y-1} {x-10},{y+1} {x-7},{y+2}" stroke="{dk}" stroke-width="1.8" fill="none" stroke-linecap="round" opacity="0.6"/>')
    # 3/4: kısa, hafif kalkık uç; sırt çizgisi göz altından başlar
    return (f'<path d="M{x-6},{y-24} C{x-3},{y-14} {x+1},{y-7} {x+4},{y-2} C{x+6},{y+2} {x+3},{y+5} {x-3},{y+4}" '
            f'stroke="{INK}" stroke-width="2.9" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="M{x-12},{y+1} C{x-13},{y+3.5} {x-11},{y+5} {x-8},{y+4.6}" stroke="{dk}" stroke-width="2" fill="none" stroke-linecap="round" opacity="0.8"/>')

def _dudak(mx, my, w, kind, sp, view):
    """Dolgun, renkli dudak; ağız çizgisi ifadeye göre. cl/cr köşe y, cm orta kontrol."""
    lip = sp.get("dudak", "#C8655A"); lipd = shade(lip, 0.8); dk = shade(sp["skin"], 0.66)
    asym = 0.85 if view == "3q" else 1.0           # 3/4'te uzak yarı daha dar
    L, R = mx - w, mx + w * asym
    cfg = {"hafif": (-1.5, 2.5, -2.5), "duz": (0.5, 1.5, 0.5), "siki": (2.5, 0, 2.5), "tremble": (3, 1, 3),
           "gulus": (-4, 6, -5), "ofke": (3, -0.5, 3)}
    o = []
    if kind == "acik":
        o.append(f'<path d="M{L+3:.1f},{my:.1f} Q{mx:.1f},{my-6:.1f} {R-3:.1f},{my:.1f} Q{mx:.1f},{my+16:.1f} {L+3:.1f},{my:.1f} Z" fill="{lip}" stroke="{INK}" stroke-width="2.6" stroke-linejoin="round"/>'
                 f'<path d="M{L+7:.1f},{my+1:.1f} Q{mx:.1f},{my-2:.1f} {R-7:.1f},{my+1:.1f} Q{mx:.1f},{my+10:.1f} {L+7:.1f},{my+1:.1f} Z" fill="#3E1A14"/>')
        return "".join(o)
    cl, cm, cr = cfg.get(kind, cfg["hafif"])
    yl, yr = my + cl, my + cr
    sk = 1.0 if kind != "siki" else 0.6               # sıkı ağızda dudak incelir
    # alt dudak
    o.append(f'<path d="M{L+1:.1f},{yl:.1f} Q{mx:.1f},{my+cm*0.5+11*sk:.1f} {R-1:.1f},{yr:.1f} Q{mx:.1f},{my+cm:.1f} {L+1:.1f},{yl:.1f} Z" fill="{lip}"/>')
    # üst dudak (kupid yayı)
    o.append(f'<path d="M{L:.1f},{yl:.1f} Q{mx-w*0.45:.1f},{my-5*sk+cm*0.3:.1f} {mx-w*0.22:.1f},{my-4.5*sk+cm*0.3:.1f} '
             f'Q{mx:.1f},{my-2.5*sk+cm*0.3:.1f} {mx+w*0.22*asym:.1f},{my-4.5*sk+cm*0.3:.1f} Q{mx+w*0.45*asym:.1f},{my-5*sk+cm*0.3:.1f} {R:.1f},{yr:.1f} '
             f'Q{mx:.1f},{my+cm:.1f} {L:.1f},{yl:.1f} Z" fill="{lipd}"/>')
    o.append(f'<ellipse cx="{mx+1:.1f}" cy="{my+cm*0.5+5*sk:.1f}" rx="{w*0.32:.1f}" ry="1.8" fill="#FFFFFF" opacity="0.35"/>')
    if kind == "tremble":
        o.append(f'<path d="M{L:.1f},{yl:.1f} Q{mx-w*0.45:.1f},{my-2:.1f} {mx:.1f},{my+1.5:.1f} Q{mx+w*0.45:.1f},{my-2:.1f} {R:.1f},{yr:.1f}" stroke="{INK}" stroke-width="2.8" fill="none" stroke-linecap="round"/>')
    else:
        o.append(f'<path d="M{L-1:.1f},{yl:.1f} Q{mx:.1f},{my+cm:.1f} {R+1:.1f},{yr:.1f}" stroke="{INK}" stroke-width="2.8" fill="none" stroke-linecap="round"/>')
    if kind in ("gulus", "hafif"):   # gülümseme kıvrımı (yanak)
        a = 0.6 if kind == "gulus" else 0.35
        o.append(f'<path d="M{L-3:.1f},{yl-4:.1f} q-2.5,2.5 0,5 M{R+3:.1f},{yr-5:.1f} q3,2.5 0.5,6" stroke="{dk}" stroke-width="1.7" fill="none" opacity="{a}" stroke-linecap="round"/>')
    return "".join(o)

def _kulak_yan(ex, ey, sk, sh):
    return (f'<path d="M{ex+2},{ey-20} C{ex-14},{ey-24} {ex-18},{ey+2} {ex-11},{ey+18} C{ex-7},{ey+25} {ex-1},{ey+24} {ex+1},{ey+16} Z" '
            f'fill="{sk}" stroke="{INK}" stroke-width="3.6" stroke-linejoin="round"/>'
            f'<path d="M{ex-4},{ey-11} C{ex-10},{ey-11} {ex-11},{ey+5} {ex-6},{ey+11}" stroke="{sh}" stroke-width="2.6" fill="none"/>'
            f'<circle cx="{ex-6}" cy="{ey+21}" r="2.2" fill="#E9E4D8" stroke="{INK}" stroke-width="1.2"/>')   # küçük inci küpe


# ───────────── kafa ─────────────
def kafa(spec=None, view="3q", ifade="odak", look=None):
    """Kafa merkezi (0,0): saç üstü ~-126, çene ~93, saç ucu ~170. view: front|3q|side. Sağa bakar."""
    sp = dict(SARA_Y)
    if spec:
        for k in ("shirt", "shirt_d", "under", "pants", "shoe"):
            if k in spec: sp[k] = spec[k]
    sk, sh, dk, hl, hair = sp["skin"], sp["skin_sh"], sp["skin_dk"], sp["skin_hl"], sp["hair"]
    hd = shade(hair, 0.72); hm = shade(hair, 0.86); hli = shade(hair, 1.55)
    bi, bo, lu, ll, mk, extra = IFADE.get(ifade, IFADE["odak"])
    lk = (0.0 if view == "front" else 0.25) if look is None else look
    face = FACE[view]; S = SAC[view]
    cid = _uid("sf"); bid = _uid("sb"); sid = _uid("ss"); hid = _uid("sh")
    o = [f'<defs><clipPath id="{cid}"><path d="{face}"/></clipPath><clipPath id="{hid}"><path d="{S["on"]}"/></clipPath>'
         f'<filter id="{bid}" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="2.2"/></filter>'
         f'<filter id="{sid}" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="4.5"/></filter></defs>']
    late = []
    # 1) uzun saç: koyu arka kopya + tutam + dalga çizgileri; hepsi yüzün ARKASINDA (yüz tam görünür)
    def _ay(x, m): return f'<g transform="scale(-1,1)">{x}</g>' if m else x
    for t, dx, m in S["tutam"]:
        o.append(_ay(f'<path d="{t}" transform="translate({dx},5)" fill="{hd}" stroke="{INK}" stroke-width="4.5" stroke-linejoin="round"/>', m))
    for t, dx, m in S["tutam"]:
        o.append(_ay(f'<path d="{t}" fill="{hm}" stroke="{INK}" stroke-width="4.5" stroke-linejoin="round"/>', m))
    tid = _uid("st")
    o.append(f'<defs><clipPath id="{tid}">' + "".join(f'<path d="{t}"' + (' transform="scale(-1,1)"' if m else '') + '/>' for t, dx, m in S["tutam"]) + '</clipPath></defs><g clip-path="url(#' + tid + ')">')
    for i, dl in enumerate(S["dalga"]):
        d = S["dalga"][i-1] if dl == "AYNA" else dl
        o.append(_ay(f'<path d="{d}" stroke="{hd}" stroke-width="2.6" fill="none" opacity="0.85" stroke-linecap="round"/>'
                     f'<path d="{d}" transform="translate(6,-8)" stroke="{hli}" stroke-width="3.4" fill="none" opacity="0.32" stroke-linecap="round"/>', dl == "AYNA"))
    o.append('</g>')
    if view == "side":   # yan profilde arka kütle: koyu kopya
        o.append(f'<path d="{S["on"]}" transform="translate(-10,6)" fill="{hd}" stroke="{INK}" stroke-width="4.5" stroke-linejoin="round"/>')
    # 2) yüz + 2 ton cel gölge
    o.append(f'<path d="{face}" fill="{sk}"/>')
    g = [f'<path d="{GOLGE[view]}" fill="{sh}"/>',
         f'<path d="M-90,{84 if view!="side" else 78} C-20,104 40,104 120,64 L120,140 L-90,140 Z" fill="{sh}"/>',
         f'<path d="{S["on"]}" transform="translate(4,8)" fill="{sh}" opacity="0.85"/>',      # perçemin alına düşen gölgesi
         f'<ellipse cx="-24" cy="-22" rx="40" ry="56" fill="{hl}" opacity="0.22" filter="url(#{bid})"/>']
    for bx, by in BLUSH[view]:
        g.append(f'<ellipse cx="{bx}" cy="{by}" rx="15" ry="8.5" fill="#EE8A78" opacity="0.32" filter="url(#{bid})"/>')
    elm = {"front": [(-40, 14), (40, 14)], "3q": [(-26, 12), (62, 10)], "side": [(26, 10)]}[view]
    for ex_, ey_ in elm:   # yumuşak elmacık ışığı (yükseltisi)
        g.append(f'<ellipse cx="{ex_}" cy="{ey_}" rx="14" ry="5" fill="{hl}" opacity="0.35" transform="rotate(-18 {ex_} {ey_})" filter="url(#{bid})"/>')
    for ex, ey, ew, uz, ay in EYES[view]:
        g.append(f'<ellipse cx="{ex+1}" cy="{ey-8}" rx="{ew*1.25:.1f}" ry="{ew*0.6:.1f}" fill="{dk}" opacity="0.10" filter="url(#{bid})"/>')
    o.append(f'<g clip-path="url(#{cid})">{"".join(g)}</g>')
    o.append(f'<path d="{face}" fill="none" stroke="{INK}" stroke-width="4.6" stroke-linejoin="round"/>')
    # 3) gözler + kaşlar
    plan = extra == "plan"
    for k, (ex, ey, ew, uz, ay) in enumerate(EYES[view]):
        if view == "side": eye, eh = _goz_profil(ex, ey, lu, ll, sp, plan), 10.0
        else: eye, eh = _goz(ex, ey, ew, uz, ay, lu, ll, lk, sp, plan)
        o.append(eye)
        bw = ew * (0.85 if uz else 1.0)
        late.append(_kas(ex, ey - eh * 1.9 - 3, bw, bi, bo, sp["brow"], ay, uz))
    if ifade in ("kararli", "ofke", "yas", "korku") and view != "side":
        cx_ = 0 if view == "front" else 31
        late.append(f'<path d="M{cx_-2},-30 q-1,6 0,9 M{cx_+3},-29 q1,5 0,8" stroke="{dk}" stroke-width="1.6" fill="none" opacity="0.5" stroke-linecap="round"/>')
    # 4) burun + dudak
    if NOSE[view]: o.append(_burun(*NOSE[view], view, sk))
    if MOUTH[view]:
        o.append(_dudak(*MOUTH[view], mk, sp, view))
        mx, my, _ = MOUTH[view]
        late.append(f'<path d="M{mx-6},{my+24} C{mx-2},{my+26} {mx+4},{my+26} {mx+8},{my+24}" stroke="{dk}" stroke-width="1.8" fill="none" opacity="0.25"/>')
    else:   # profil: dudak rengi konturun içinde, kısa ağız çizgisi ifadeye göre
        lip = sp.get("dudak"); lipd = shade(lip, 0.8)
        o.append(f'<g clip-path="url(#{cid})"><path d="M62,25 C66,26 69,25 72,28 C73,31 72,34 69,36 C66,36 64,35 62,34 Z" fill="{lipd}" opacity="0.45"/>'
                 f'<path d="M62,37 C65,37 68,36 71,39 C72,42 70,44 68,45 C65,45 63,44 62,42 Z" fill="{lip}" opacity="0.45"/></g>')
        mline = {"gulus": "M69,36 C66,36 63,35 61,32", "hafif": "M69,36 C66,36 64,35 62,34", "siki": "M71,36 C67,37 64,37 62,38",
                 "ofke": "M71,36 C67,37 64,38 62,39", "tremble": "M71,36 C68,35 65,37 62,37", "duz": "M71,36 L62,36"}.get(mk, "M71,36 L62,36")
        if mk == "acik":
            o.append('<path d="M71,35 C67,34 63,36 62,38 C64,40 68,40 72,39 Z" fill="#3E1A14" stroke="#15110E" stroke-width="1.8"/>')
        else:
            o.append(f'<path d="{mline}" stroke="{INK}" stroke-width="2.6" fill="none" stroke-linecap="round"/>')
        o.append(f'<path d="M77,15 C75,17 73,17 71,15" stroke="{dk}" stroke-width="1.8" fill="none" stroke-linecap="round"/>')   # burun kanadı
    # 5) ön saç: perçem / kafatası (yalnız saç çizgisinin üstü; yan profilde kafatasının arkası)
    o.append(f'<path d="{S["on"]}" fill="{hair}" stroke="{INK}" stroke-width="4.5" stroke-linejoin="round"/>')
    o.append(f'<g clip-path="url(#{hid})">'
             f'<path d="{S["on_dalga"]}" stroke="{hd}" stroke-width="2.6" fill="none" opacity="0.75" stroke-linecap="round"/>'
             f'<path d="{S["parlak"]}" stroke="{hli}" stroke-width="9" fill="none" opacity="0.55" stroke-linecap="round" filter="url(#{bid})"/>'
             f'<path d="{S["parlak"]}" stroke="#FFD8C0" stroke-width="2.4" fill="none" opacity="0.5" stroke-linecap="round"/>'
             f'<path d="{S["parlak2"]}" stroke="{hli}" stroke-width="5" fill="none" opacity="0.35" stroke-linecap="round"/></g>')
    if view == "side":
        o.append(_kulak_yan(-12, 0, sk, sh))
    if extra == "tear":
        ex, ey, ew, _, _ = EYES[view][0]
        o.append(f'<path d="M{ex+2},{ey+14} C{ex+5},{ey+25} {ex+1},{ey+33} {ex+2},{ey+40}" stroke="#CDEBFF" stroke-width="3.2" fill="none" stroke-linecap="round" opacity="0.9"/>'
                 f'<ellipse cx="{ex+2}" cy="{ey+44}" rx="3.4" ry="4.8" fill="#CDEBFF" stroke="#5A8AB0" stroke-width="1.5"/>')
    return "".join(o) + "".join(late)

def kafa_drop(sp, v="3q", i="odak", l=None, _eski=None):
    return kafa(sp, v, i, l) if sp.get("female") else (_eski or K.kafa)(sp, v, i, l)

def figur(ifade="sefkat", **kw):
    eski = K.kafa; K.kafa = lambda sp, v="3q", i="odak", l=None: kafa_drop(sp, v, i, l, eski)
    try: return K.figur2(K.SARA, ifade, **kw)
    finally: K.kafa = eski


# ─────────────── kart ───────────────
W, H = 1280, 720
def et(x, y, t, s=14, c="#D8DEE4", a="middle"):
    return f'<text x="{x}" y="{y}" font-family="DejaVu Sans" font-size="{s}" fill="{c}" text-anchor="{a}">{t}</text>'
def g(x, y, sc, inner):
    return f'<g transform="translate({x},{y}) scale({sc})">{inner}</g>'

def kart():
    import yuzler
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
         '<defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2E3944"/><stop offset="1" stop-color="#171D23"/></linearGradient>'
         '<radialGradient id="spot" cx="0.5" cy="0.4" r="0.6"><stop offset="0" stop-color="#FFE2B8" stop-opacity="0.22"/><stop offset="1" stop-color="#FFE2B8" stop-opacity="0"/></radialGradient></defs>',
         f'<rect width="{W}" height="{H}" fill="url(#bg)"/><ellipse cx="150" cy="420" rx="180" ry="320" fill="url(#spot)"/>',
         et(24, 32, "SARA TANCREDİ · yüz ve saç adayı (sara.py)", 18, "#FFFFFF", "start")]
    o.append(g(150, 690, 1.0, figur("sefkat")))
    o.append(et(150, 712, "tam figür (yeni kafa, şefkat)"))
    for x, v, ad in ((390, "front", "önden"), (530, "3q", "3/4"), (670, "side", "yandan")):
        o.append(g(x, 120, 0.46, kafa(SARA_Y, v, "odak")))
        o.append(et(x, 215, ad, 13))
    for i, (e, ad) in enumerate((("odak", "odak"), ("sefkat", "şefkat"), ("kararli", "kararlı"), ("yas", "yas"), ("korku", "korku"), ("ofke", "öfke"))):
        x = 390 + (i % 3) * 140; y = 300 + (i // 3) * 180
        o.append(g(x, y, 0.5, kafa(SARA_Y, "3q", e)))
        o.append(et(x, y + 100, ad, 13))
    # önce / sonra
    o.append(f'<rect x="790" y="48" width="470" height="300" rx="10" fill="#0F1418" opacity="0.5"/>')
    o.append(g(905, 170, 0.78, yuzler.kafa(K.SARA, "3q", "sefkat")))
    o.append(g(1145, 170, 0.78, kafa(SARA_Y, "3q", "sefkat")))
    o.append(et(905, 340, "ÖNCE (yuzler.py)", 14, "#E8A890"))
    o.append(et(1145, 340, "SONRA (sara.py)", 14, "#9FE0B0"))
    # stil uyumu
    o.append(g(880, 445, 0.5, K.kafa(K.MICHAEL, "3q", "odak")))
    o.append(g(990, 445, 0.5, kafa(SARA_Y, "3q", "sefkat")))
    o.append(g(1100, 445, 0.5, kafa(SARA_Y, "front", "sefkat")))
    o.append(g(1205, 445, 0.5, kafa(SARA_Y, "side", "sefkat")))
    o.append(et(1040, 545, "stil uyumu: Michael · Sara 3/4 · önden · yandan", 12))
    o.append(et(1040, 572, "küçük boy (~70 px yüz): odak · şefkat · kararlı · yas · korku · öfke", 12))
    for i, e in enumerate(("odak", "sefkat", "kararli", "yas", "korku", "ofke")):
        o.append(g(860 + i * 72, 625, 0.32, kafa(SARA_Y, "3q", e)))
    o.append('</svg>')
    return "".join(o)

if __name__ == "__main__":
    svg = Path("/tmp") / "sara_kart.svg"; svg.write_text(kart())
    subprocess.run(["rsvg-convert", "-w", str(W), "-o", str(P / "sara_kart.png"), str(svg)], check=True)
    print("tamam")
