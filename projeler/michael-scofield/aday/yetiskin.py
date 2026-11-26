"""Yetişkin Michael kafa/yüz tasarımı ADAYI v4 (karakter.kafa ile aynı imza, drop-in).
Hedef: tipi koruyan (kazınmış koyu saç, açık yeşil-mavi göz, düz güçlü kaş, köşeli çene) ama
çekici, sempatik, karizmatik bir animasyon başrol yüzü (~30 yaş, sağlıklı, temiz).
Hiçbir gerçek kişinin yüzü örnek alınmadı; stilize özgün yüz.
Paylaşılan yardımcılar (çocuk tasarımı da kullanır): _goz(...), _burun(...), _kas(...).
Kullanım: python3 yetiskin.py [sürüm]  ->  yetiskin_kart.png (1280x720)
"""
import base64, subprocess, sys
from pathlib import Path
P = Path(__file__).resolve().parent; PROJ = P.parent; REPO = PROJ.parents[1]
sys.path[:0] = [str(PROJ), str(REPO / "r3"), str(REPO / "r2")]
from art2 import shade
import karakter as K

_ESKI_KAFA = K.kafa
INK = "#15110E"; PLAN = "#7FE6FF"
# sıcak, sağlıklı ten; gölge tonu griye değil sıcak kahveye kayar (2 ton cel)
MICHAEL_Y = dict(K.MICHAEL, skin="#E2AB86", skin_sh="#C4876A", skin_dk="#A86A52", skin_hl="#FFD9B8",
                 hair="#1F1A16", brow="#1F1A16", iris="#8FCFC4", iris_d="#2C5754")
BOYUN_KISALT = 22   # figürde boyun ~%10 kısa: kafa, boyna göre bu kadar (kafa birimi) aşağı oturur

# ifade: kaş_iç (yukarı +), kaş_dış, üst_kapak (0 açık..1 kapalı), alt_kapak, ağız, ekstra
IFADE = {
    "odak":    (-1, 1, 0.20, 0.10, "emin", ""),
    "kararli": (-11, 2, 0.30, 0.20, "siki", ""),
    "yas":     (10, -5, 0.32, 0.04, "tremble", "tear"),
    "korku":   (12, 7, 0.0, 0.0, "open_s", ""),
    "sefkat":  (5, 2, 0.22, 0.24, "yarim", ""),
    "ofke":    (-13, 4, 0.30, 0.22, "siki", ""),
    "plan":    (-2, 2, 0.16, 0.08, "emin", "plan"),
    "neutral": (0, 0, 0.18, 0.06, "duz", ""),
}

_ID = [0]
def _uid(p):
    _ID[0] += 1; return f"{p}{_ID[0]}"


# ───────────── paylaşılan yardımcılar (modül düzeyi, parametreli) ─────────────
def _goz(cx, cy, w, h, lu=0.2, ll=0.1, iris="#8FCFC4", iris_d="#2C5754", look=0.25, skin="#E2AB86",
         uzak=False, plan=False, olcek=1.0, cocuk=False):
    """Canlı badem göz. (cx,cy) göz merkezi, w yarı genişlik, h yarı yükseklik.
    lu/ll: üst/alt kapak kapanma (0 açık..1 kapalı); look: -1..1 bakış; uzak: 3/4'te uzak göz (ince çizgi);
    olcek: çizgi kalınlık ölçeği; cocuk=True: daha yuvarlak göz, büyük iris, ince kapak, kıvrım çizgisi yok."""
    o = []; cid = _uid("g"); dk = shade(skin, 0.66); lw = (3.0 if uzak else 3.8) * olcek
    yuv = 1.15 if cocuk else 1.0
    shape = (f"M{cx-w:.1f},{cy+h*0.1:.1f} C{cx-w*0.6:.1f},{cy-h*1.1*yuv:.1f} {cx+w*0.45:.1f},{cy-h*1.15*yuv:.1f} {cx+w:.1f},{cy-h*0.05:.1f} "
             f"C{cx+w*0.55:.1f},{cy+h*0.95*yuv:.1f} {cx-w*0.5:.1f},{cy+h*0.95*yuv:.1f} {cx-w:.1f},{cy+h*0.1:.1f} Z")
    ly = cy - h * 1.05 + 2.0 * h * lu
    lo = cy + h * 0.85 - 1.6 * h * ll
    ix = cx + look * w * 0.4; ir = h * (1.05 if cocuk else 0.95)
    o.append(f'<defs><clipPath id="{cid}"><path d="{shape}"/></clipPath></defs><path d="{shape}" fill="#F6F1EA"/>')
    o.append(f'<g clip-path="url(#{cid})">'
             f'<path d="M{cx-w-2:.1f},{cy-h:.1f} H{cx+w+2:.1f} V{cy-h*0.35:.1f} Q{cx:.1f},{cy-h*0.1:.1f} {cx-w-2:.1f},{cy-h*0.35:.1f} Z" fill="#D9CFC4" opacity="0.7"/>'
             f'<circle cx="{ix:.1f}" cy="{cy+0.5:.1f}" r="{ir:.1f}" fill="{PLAN if plan else iris}"/>'
             f'<circle cx="{ix+ir*0.15:.1f}" cy="{cy+ir*0.35:.1f}" r="{ir*0.6:.1f}" fill="#FFFFFF" opacity="0.22"/>'
             f'<circle cx="{ix:.1f}" cy="{cy+0.5:.1f}" r="{ir:.1f}" fill="none" stroke="{iris_d}" stroke-width="{max(1.2, ir*0.2):.1f}"/>'
             f'<circle cx="{ix:.1f}" cy="{cy+0.5:.1f}" r="{ir*0.38:.1f}" fill="#0E0B09"/>'
             f'<circle cx="{ix-ir*0.36:.1f}" cy="{cy-ir*0.3:.1f}" r="{max(1.6, ir*0.3):.1f}" fill="#FFFFFF"/>'
             f'<circle cx="{ix+ir*0.42:.1f}" cy="{cy+ir*0.38:.1f}" r="{max(0.8, ir*0.12):.1f}" fill="#FFFFFF" opacity="0.85"/>'
             # üst kapak (ten), alt kapak (ten)
             f'<path d="M{cx-w-4:.1f},{cy+h*0.1:.1f} Q{cx:.1f},{ly-h*0.3:.1f} {cx+w+4:.1f},{cy-h*0.05:.1f} L{cx+w+4:.1f},{cy-h*3:.1f} L{cx-w-4:.1f},{cy-h*3:.1f} Z" fill="{skin}"/>'
             f'<path d="M{cx-w-4:.1f},{cy+h*2:.1f} L{cx-w-4:.1f},{cy+h*0.1:.1f} Q{cx:.1f},{lo+h*0.3:.1f} {cx+w+4:.1f},{cy-h*0.05:.1f} L{cx+w+4:.1f},{cy+h*2:.1f} Z" fill="{skin}"/>'
             f'</g>')
    # üst kapak çizgisi: dış köşede kirpik vurgusu
    o.append(f'<path d="M{cx-w-1:.1f},{cy+h*0.15:.1f} Q{cx:.1f},{ly-h*0.3:.1f} {cx+w+1:.1f},{cy-h*0.05:.1f} l{3*olcek:.1f},{-1*olcek:.1f}" stroke="{INK}" stroke-width="{lw:.1f}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
    o.append(f'<path d="M{cx-w*0.5:.1f},{lo+h*0.2:.1f} Q{cx:.1f},{lo+h*0.42:.1f} {cx+w*0.7:.1f},{lo+h*0.08:.1f}" stroke="{dk}" stroke-width="{1.8*olcek:.1f}" fill="none" opacity="0.7"/>')
    if not cocuk:  # ince kapak kıvrımı
        o.append(f'<path d="M{cx-w*0.6:.1f},{cy-h*1.35:.1f} Q{cx:.1f},{cy-h*1.7:.1f} {cx+w*0.85:.1f},{cy-h*1.15:.1f}" stroke="{dk}" stroke-width="{1.8*olcek:.1f}" fill="none" opacity="0.45"/>')
    return "".join(o)

def _kas(cx, cy, w, ic, dis, color, yon, ince=False, olcek=1.0):
    """Düz, güçlü kaş: iç uç kalın, dış uç incelir. yon: iç ucun x yönü (-1 sol, +1 sağ). ic/dis: yukarı +."""
    xi, xo = cx + yon * w * 0.95, cx - yon * w * 1.15
    yi, yo = cy - 3 - ic, cy - 5 - dis
    t = (7.8 if not ince else 6.0) * olcek
    d = (f"M{xi:.1f},{yi-t*0.55:.1f} Q{(xi+xo)/2:.1f},{(yi+yo)/2-t*0.85:.1f} {xo:.1f},{yo-t*0.15:.1f} "
         f"L{xo-yon*2:.1f},{yo+t*0.25:.1f} Q{(xi+xo)/2:.1f},{(yi+yo)/2+t*0.15:.1f} {xi:.1f},{yi+t*0.5:.1f} Z")
    return f'<path d="{d}" fill="{color}" stroke="{INK}" stroke-width="{2*olcek:.1f}" stroke-linejoin="round"/>'

def _burun(x, y, view="3q", skin="#E2AB86", olcek=1.0, cocuk=False):
    """Sade burun. (x,y) burun ucu. 3q: çizgi göz iç köşesi altından başlar, kısa ve düzgün.
    front: belirgin ama sade alt kısım + hafif sırt gölgesi. cocuk=True: daha kısa ve yuvarlak."""
    s = olcek * (0.75 if cocuk else 1.0); dk = shade(skin, 0.66)
    if view == "3q":
        return (f'<path d="M{x-6*s:.1f},{y-30*s:.1f} C{x-3*s:.1f},{y-18*s:.1f} {x+1*s:.1f},{y-8*s:.1f} {x+4*s:.1f},{y-2*s:.1f} '
                f'C{x+5*s:.1f},{y+3*s:.1f} {x+1*s:.1f},{y+6*s:.1f} {x-5*s:.1f},{y+5*s:.1f}" stroke="{INK}" stroke-width="{3.4*olcek:.1f}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
                f'<path d="M{x-14*s:.1f},{y+1*s:.1f} C{x-15*s:.1f},{y+4*s:.1f} {x-12*s:.1f},{y+6*s:.1f} {x-9*s:.1f},{y+5.5*s:.1f}" stroke="{dk}" stroke-width="{2.2*olcek:.1f}" fill="none" stroke-linecap="round" opacity="0.8"/>')
    if view == "front":
        return (f'<path d="M{x+5*s:.1f},{y-34*s:.1f} C{x+6*s:.1f},{y-20*s:.1f} {x+8*s:.1f},{y-10*s:.1f} {x+9*s:.1f},{y-4*s:.1f}" stroke="{dk}" stroke-width="{2.4*olcek:.1f}" fill="none" opacity="0.55" stroke-linecap="round"/>'
                f'<path d="M{x-7*s:.1f},{y+1*s:.1f} C{x-3*s:.1f},{y+5*s:.1f} {x+3*s:.1f},{y+5*s:.1f} {x+7*s:.1f},{y+1*s:.1f}" stroke="{INK}" stroke-width="{3.2*olcek:.1f}" fill="none" stroke-linecap="round"/>'
                f'<path d="M{x+12*s:.1f},{y-5*s:.1f} C{x+14*s:.1f},{y-1*s:.1f} {x+12*s:.1f},{y+2*s:.1f} {x+8*s:.1f},{y+2*s:.1f}" stroke="{dk}" stroke-width="{2.4*olcek:.1f}" fill="none" stroke-linecap="round"/>'
                f'<path d="M{x-12*s:.1f},{y-5*s:.1f} C{x-14*s:.1f},{y-1*s:.1f} {x-12*s:.1f},{y+2*s:.1f} {x-8*s:.1f},{y+2*s:.1f}" stroke="{dk}" stroke-width="{2*olcek:.1f}" fill="none" stroke-linecap="round" opacity="0.6"/>')
    return ""   # yandan: burun konturun parçası

def _agiz(mx, my, w, kind, sk):
    lip = shade(sk, 0.74); dk = shade(sk, 0.66); o = []
    if kind == "emin":      # kendinden emin sıcaklık: sağ köşe çok hafif kalkık
        o.append(f'<path d="M{mx-w:.1f},{my+1:.1f} Q{mx:.1f},{my+3.5:.1f} {mx+w:.1f},{my-1.5:.1f}" stroke="{INK}" stroke-width="3.3" fill="none" stroke-linecap="round"/>'
                 f'<path d="M{mx+w+1:.1f},{my-4:.1f} q2,2 0.5,5" stroke="{dk}" stroke-width="1.8" fill="none" opacity="0.6"/>')
    elif kind == "duz":
        o.append(f'<path d="M{mx-w:.1f},{my+1:.1f} Q{mx:.1f},{my+2:.1f} {mx+w:.1f},{my+0.5:.1f}" stroke="{INK}" stroke-width="3.3" fill="none" stroke-linecap="round"/>')
    elif kind == "siki":    # sıkı, köşeler hafif aşağı
        o.append(f'<path d="M{mx-w*0.95:.1f},{my+4:.1f} Q{mx:.1f},{my-0.5:.1f} {mx+w*0.95:.1f},{my+4:.1f}" stroke="{INK}" stroke-width="3.8" fill="none" stroke-linecap="round"/>'
                 f'<path d="M{mx-w-2:.1f},{my+3:.1f} l-1.5,4 M{mx+w+2:.1f},{my+3:.1f} l1.5,4" stroke="{dk}" stroke-width="1.8" opacity="0.6" stroke-linecap="round"/>')
    elif kind == "tremble":
        o.append(f'<path d="M{mx-w:.1f},{my+4:.1f} Q{mx-w*0.45:.1f},{my-1:.1f} {mx:.1f},{my+1.5:.1f} Q{mx+w*0.45:.1f},{my-1:.1f} {mx+w:.1f},{my+4:.1f}" stroke="{INK}" stroke-width="3.3" fill="none" stroke-linecap="round"/>')
    elif kind == "open_s":
        o.append(f'<path d="M{mx-w*0.6:.1f},{my:.1f} Q{mx:.1f},{my-4:.1f} {mx+w*0.6:.1f},{my:.1f} Q{mx:.1f},{my+12:.1f} {mx-w*0.6:.1f},{my:.1f} Z" fill="#3E1A14" stroke="{INK}" stroke-width="3"/>')
    elif kind == "yarim":   # net, sıcak yarım gülümseme
        o.append(f'<path d="M{mx-w*1.05:.1f},{my-1:.1f} Q{mx-w*0.1:.1f},{my+8:.1f} {mx+w*1.1:.1f},{my-5:.1f}" stroke="{INK}" stroke-width="3.4" fill="none" stroke-linecap="round"/>'
                 f'<path d="M{mx-w*1.2:.1f},{my-4:.1f} q-2,2 0,4 M{mx+w*1.2:.1f},{my-9:.1f} q3,3 1,7" stroke="{dk}" stroke-width="1.8" fill="none" opacity="0.65" stroke-linecap="round"/>')
    o.append(f'<path d="M{mx-w*0.5:.1f},{my+9:.1f} Q{mx:.1f},{my+11.5:.1f} {mx+w*0.5:.1f},{my+9:.1f}" stroke="{lip}" stroke-width="2.8" fill="none" stroke-linecap="round" opacity="0.75"/>')
    return "".join(o)


# ───────────── kafa ─────────────
def kafa(spec=None, view="3q", ifade="odak", look=None):
    """Kafa merkezi (0,0), yükseklik ~205 (saç üstü -116, çene ~90). view: front|3q|side. Sağa bakar."""
    if spec is not None and (spec.get("child") or spec.get("female") or spec.get("broad")):
        return _ESKI_KAFA(spec, view, ifade, look)   # yalnız yetişkin Michael bu yüzü alır
    sp = dict(MICHAEL_Y)
    sk = sp["skin"]; sh = sp["skin_sh"]; dk = sp["skin_dk"]; hl = sp["skin_hl"]; hair = sp["hair"]
    bi, bo, lu, ll, mk, extra = IFADE.get(ifade, IFADE["odak"])
    lk = 0.25 if look is None else look
    o = []; late = []
    if view == "front":
        face = ("M-60,-40 C-64,-96 -32,-112 0,-112 C32,-112 64,-96 60,-40 C62,-16 62,4 59,24 "
                "C57,42 54,56 47,68 C42,78 32,86 20,88 L-20,88 C-32,86 -42,78 -47,68 C-54,56 -57,42 -59,24 "
                "C-62,4 -62,-16 -60,-40 Z")
        ears = [(-60, -4, -1), (60, -4, 1)]
        eyes = [(-25, -8, 17, False), (25, -8, 17, False)]
        nose = (0, 30); mx, my, mw = 0, 52, 15
        cap = ("M-61,-34 C-66,-98 -32,-116 0,-116 C32,-116 66,-98 61,-34 L56,-34 C55,-52 52,-62 44,-68 "
               "C34,-72 22,-74 12,-73 C6,-76 -6,-76 -12,-73 C-22,-74 -34,-72 -44,-68 C-52,-62 -55,-52 -56,-34 Z")
        golge = "M32,-120 C56,-80 54,-30 56,10 C55,40 48,62 30,92 L120,120 L120,-120 Z"
        sakal = "M-58,26 C-54,50 -46,70 -30,82 L-20,88 L20,88 L30,82 C46,70 54,50 58,26 C54,52 44,64 30,70 C18,64 8,64 0,64 C-8,64 -18,64 -30,70 C-44,64 -54,52 -58,26 Z"
    elif view == "3q":
        face = ("M-60,-40 C-64,-98 -20,-114 14,-112 C52,-110 76,-86 76,-42 L74,-24 C80,-14 80,-2 74,6 "
                "C74,22 70,38 64,52 C58,66 52,76 44,84 L40,89 L6,91 C-6,89 -20,79 -34,64 "
                "C-46,50 -58,28 -60,-40 Z")
        ears = [(-54, -2, -1)]
        eyes = [(6, -8, 17.5, False), (56, -9, 11.5, True)]
        nose = (42, 28); mx, my, mw = 34, 52, 14
        cap = ("M-61,-30 C-66,-100 -20,-118 14,-116 C54,-114 80,-90 77,-40 L72,-42 C68,-58 60,-66 50,-70 "
               "C36,-76 20,-78 6,-76 C-10,-74 -24,-70 -32,-62 C-40,-52 -42,-40 -40,-24 C-44,-14 -50,-8 -56,-8 Z")
        golge = "M50,-120 C66,-80 62,-40 64,-14 C66,14 60,50 40,96 L130,120 L130,-120 Z"
        sakal = "M-36,40 C-24,64 -10,80 6,91 L40,89 C56,76 68,56 74,28 C66,54 56,66 46,70 C38,64 30,64 24,64 C16,64 8,66 2,72 C-14,66 -28,56 -36,40 Z"
    else:  # side
        face = ("M-66,-40 C-70,-98 -26,-116 10,-112 C44,-108 62,-88 63,-50 L64,-28 C68,-22 68,-16 64,-10 "
                "C70,0 80,10 86,18 C84,24 78,26 72,26 C74,30 75,34 73,37 L70,42 L73,47 C72,51 70,53 68,55 "
                "C72,62 73,70 72,78 L70,84 L48,88 C30,88 14,86 2,82 L-8,72 C-24,56 -46,40 -60,20 C-66,6 -68,-14 -66,-40 Z")
        ears = [(-16, -2, -1)]
        eyes = [(50, -8, 11, True)]
        nose = None; mx, my, mw = 66, 42, 5
        cap = ("M-67,-30 C-72,-100 -26,-120 10,-116 C46,-112 64,-92 66,-62 L58,-64 C48,-74 34,-78 18,-76 "
               "C4,-74 -2,-68 -4,-56 L-2,-22 L-10,-20 C-14,-12 -26,-10 -40,-10 C-50,-10 -58,-8 -63,-6 Z")
        golge = "M-62,16 C-40,44 -14,64 10,80 L-80,120 Z"
        sakal = "M-4,40 C10,60 28,76 50,86 L70,84 C72,74 70,62 68,56 C60,58 52,58 46,60 C30,56 12,50 -4,40 Z"
    cid = _uid("f"); bid = _uid("b")
    o.append(f'<defs><clipPath id="{cid}"><path d="{face}"/></clipPath>'
             f'<filter id="{bid}" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="2.2"/></filter></defs>')
    kul = []
    for ex, ey, s in ears:
        kul.append(f'<path d="M{ex+s*4},{ey-22} C{ex+s*19},{ey-25} {ex+s*21},{ey+4} {ex+s*13},{ey+21} C{ex+s*9},{ey+28} {ex+s*2},{ey+27} {ex},{ey+19} Z" '
                   f'fill="{sk}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
                   f'<path d="M{ex+s*7},{ey-12} C{ex+s*14},{ey-12} {ex+s*14},{ey+7} {ex+s*8},{ey+13}" stroke="{sh}" stroke-width="3" fill="none"/>')
    if view != "side": o += kul
    o.append(f'<path d="{face}" fill="{sk}"/>')
    # 2 tonlu cel gölge + sıcak ışık; sakal gölgesi yumuşak düz ton
    g = [f'<path d="{golge}" fill="{sh}"/>',
         f'<path d="M-90,{84 if view!="side" else 80} C-20,104 40,104 120,64 L120,140 L-90,140 Z" fill="{sh}"/>',
         f'<path d="{sakal}" fill="{hair}" opacity="0.13" filter="url(#{bid})"/>',
         f'<ellipse cx="-30" cy="-30" rx="40" ry="60" fill="{hl}" opacity="0.18" filter="url(#{bid})"/>']
    if view == "3q":
        g.append(f'<path d="M-60,-30 C-50,-10 -48,10 -52,30 L-66,30 Z" fill="{sh}" opacity="0.6"/>')
    for ex, ey, ew, uz in eyes:   # hafif göz çukuru
        g.append(f'<ellipse cx="{ex+1}" cy="{ey-9}" rx="{ew*1.3:.1f}" ry="{ew*0.7:.1f}" fill="{dk}" opacity="0.12" filter="url(#{bid})"/>')
    o.append(f'<g clip-path="url(#{cid})">{"".join(g)}</g>')
    # saç: temiz şekil + ince doku
    hid = _uid("h")
    o.append(f'<defs><clipPath id="{hid}"><path d="{cap}"/></clipPath></defs>')
    o.append(f'<g clip-path="url(#{cid})"><path d="{cap}" fill="{hair}" opacity="0.92" filter="url(#{bid})"/></g>')
    hh = []
    for k in range(9):   # ince yön dokusu: tepe ışığına paralel kısa çizgiler
        y = -108 + k * 9
        hh.append(f'<path d="M-50,{y} C-10,{y-10} 30,{y-8} 70,{y+4}" stroke="{shade(hair,2.0)}" stroke-width="1" fill="none" opacity="0.22" stroke-dasharray="2 5"/>')
    hh.append(f'<path d="M-44,-100 C-14,-114 26,-112 54,-98" stroke="{shade(hair,3.4)}" stroke-width="8" fill="none" opacity="0.22" filter="url(#{bid})"/>')
    hh.append(f'<path d="M36,-120 C70,-90 80,-60 70,-20 L120,-20 L120,-120 Z" fill="#000" opacity="0.22"/>')
    o.append(f'<g clip-path="url(#{cid})"><g clip-path="url(#{hid})">{"".join(hh)}</g></g>')
    o.append(f'<path d="{face}" fill="none" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>')
    if view == "side": o += kul
    # gözler + kaşlar
    plan = extra == "plan"
    for k, (ex, ey, ew, uz) in enumerate(eyes):
        eh = ew * 0.72
        o.append(_goz(ex, ey, ew, eh, lu, ll, sp["iris"], sp["iris_d"], lk, sk, uzak=uz))
        if plan:
            ix = ex + lk * ew * 0.4
            late.append(f'<circle cx="{ix:.1f}" cy="{ey+0.5:.1f}" r="{eh*0.9:.1f}" fill="{PLAN}" opacity="0.6"/>'
                        f'<path d="M{ix-eh*0.6:.1f},{ey+eh*0.1:.1f} h{eh*0.45:.1f} v{-eh*0.45:.1f} h{eh*0.5:.1f}" stroke="#E8FCFF" stroke-width="1.5" fill="none" opacity="0.95"/>'
                        f'<circle cx="{ix-eh*0.32:.1f}" cy="{ey-eh*0.28:.1f}" r="{max(1.5,eh*0.26):.1f}" fill="#FFFFFF"/>')
        if view == "front": yon = 1 if ex < 0 else -1
        elif view == "3q": yon = 1 if k == 0 else -1
        else: yon = 1
        late.append(_kas(ex, ey - eh * 1.75, ew * (0.85 if uz else 1.0), bi, bo, sp["brow"], yon, ince=uz))
    # kaş arası çizgi yalnız gergin ifadelerde
    cx_ = {"front": 0, "3q": 31, "side": None}[view]
    if cx_ is not None and ifade in ("kararli", "ofke", "yas", "korku"):
        late.append(f'<path d="M{cx_-3},-32 q-1,7 0,11 M{cx_+4},-31 q1,6 0,9" stroke="{dk}" stroke-width="2" fill="none" opacity="0.6" stroke-linecap="round"/>')
    if nose: o.append(_burun(*nose, view=view, skin=sk))
    o.append(_agiz(mx, my, mw, mk, sk))
    if view != "side":   # çene altı tek hafif çizgi (≤%25)
        late.append(f'<path d="M{mx-6},{my+22} C{mx-2},{my+25} {mx+4},{my+25} {mx+8},{my+22}" stroke="{dk}" stroke-width="2" fill="none" opacity="0.25"/>')
    if extra == "tear":
        ex, ey, ew, _ = eyes[0]
        o.append(f'<path d="M{ex+4},{ey+15} C{ex+7},{ey+26} {ex+3},{ey+34} {ex+4},{ey+42}" stroke="#CDEBFF" stroke-width="3.5" fill="none" stroke-linecap="round" opacity="0.9"/>'
                 f'<ellipse cx="{ex+4}" cy="{ey+46}" rx="3.6" ry="5" fill="#CDEBFF" stroke="#5A8AB0" stroke-width="1.6"/>')
    return "".join(o) + "".join(late)

def kafa_figur(spec=None, view="3q", ifade="odak", look=None):
    """figur2 içinde kullanmak için: boyun ~%10 kısa görünsün diye kafa boyna BOYUN_KISALT kadar iner."""
    return f'<g transform="translate(0,{BOYUN_KISALT})">{kafa(spec, view, ifade, look)}</g>'

def figur(spec=None, ifade="odak", **kw):
    """Yeni kafayla tam figür (karakter.figur2 değiştirilmeden)."""
    eski = K.kafa; K.kafa = kafa_figur
    try: return K.figur2(spec or K.MICHAEL, ifade, **kw)
    finally: K.kafa = eski


# ─────────────── kart ───────────────
W, H = 1280, 720
def et(x, y, t, s=14, c="#D8DEE4", a="middle"):
    return f'<text x="{x}" y="{y}" font-family="DejaVu Sans" font-size="{s}" fill="{c}" text-anchor="{a}">{t}</text>'
def g(x, y, sc, inner):
    return f'<g transform="translate({x},{y}) scale({sc})">{inner}</g>'

def kart(surum="v4"):
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
         '<defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2E3944"/><stop offset="1" stop-color="#171D23"/></linearGradient>'
         '<radialGradient id="spot" cx="0.5" cy="0.4" r="0.6"><stop offset="0" stop-color="#FFE2B8" stop-opacity="0.22"/><stop offset="1" stop-color="#FFE2B8" stop-opacity="0"/></radialGradient></defs>',
         f'<rect width="{W}" height="{H}" fill="url(#bg)"/><ellipse cx="170" cy="420" rx="190" ry="320" fill="url(#spot)"/>',
         et(24, 32, f"MICHAEL (yetişkin) · yüz adayı {surum}", 18, "#FFFFFF", "start")]
    o.append(g(170, 690, 1.0, figur(K.MICHAEL, "odak")))
    o.append(et(170, 712, "tam figür (yeni kafa, boyun -%10)"))
    for x, v, ad in ((420, "front", "önden"), (560, "3q", "3/4"), (700, "side", "yandan")):
        o.append(g(x, 136, 0.5, kafa(MICHAEL_Y, v, "odak")))
        o.append(et(x, 214, ad, 13))
    for i, (e, ad) in enumerate((("odak", "odak"), ("kararli", "kararlı"), ("yas", "yas"), ("korku", "korku"), ("sefkat", "şefkat"), ("plan", "plan görüşü"))):
        x = 390 + (i % 3) * 140; y = 330 + (i // 3) * 190
        o.append(g(x, y, 0.62, kafa(MICHAEL_Y, "3q", e)))
        o.append(et(x, y + 92, ad, 13, PLAN if e == "plan" else "#D8DEE4"))
    # önce (v3, kaydedilmiş görüntü) / sonra
    o.append(f'<rect x="820" y="60" width="440" height="420" rx="10" fill="#0F1418" opacity="0.5"/>')
    v3 = P / "yetiskin_v3_3q.png"
    if v3.exists():
        b64 = base64.b64encode(v3.read_bytes()).decode()
        o.append(f'<image x="{930-126}" y="{250-136}" width="252" height="273" xlink:href="data:image/png;base64,{b64}"/>')
    o.append(g(1150, 250, 1.05, kafa(MICHAEL_Y, "3q", "odak")))
    o.append(et(930, 400, "ÖNCE (v3)", 15, "#E8A890"))
    o.append(et(1150, 400, f"SONRA ({surum})", 15, "#9FE0B0"))
    o.append(et(1040, 510, "küçük ölçek (~70 px kafa): odak · kararlı · yas · korku · şefkat · plan", 12))
    for i, e in enumerate(("odak", "kararli", "yas", "korku", "sefkat", "plan")):
        o.append(g(860 + i * 70, 580, 0.32, kafa(MICHAEL_Y, "3q", e)))
    o.append('</svg>')
    return "".join(o)

if __name__ == "__main__":
    surum = sys.argv[1] if len(sys.argv) > 1 else "v4"
    svg = Path("/tmp") / "yetiskin_kart.svg"; svg.write_text(kart(surum))
    subprocess.run(["rsvg-convert", "-w", str(W), "-o", str(P / "yetiskin_kart.png"), str(svg)], check=True)
    print("tamam")
