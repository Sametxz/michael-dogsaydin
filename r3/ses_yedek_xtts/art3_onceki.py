"""v3 karakter modeli: 1:3,5 oran, çok görünümlü kafa (front/3q/side/back), tel dokulu saç-sakal,
katmanlı ifadeler, el şekilleri. Ragnar'ın özgün imzası: şakak örgüleri + yüzük boncuklar, çatallı örgülü sakal,
kaşta ince yara, gümüş kuzgun pelerin tokası."""
import math, random, sys
sys.path.insert(0, "/home/claude/r2")
import art2
from art2 import INK, shade, limb, character, BODY

LINE = 4.5
BROW_C = ["#2C1E12"]
STERN = [7]

def strands(path_pts, n, color, width=2.2, jitter=6, seed=1, alpha=0.55):
    """Bir kılavuz eğri boyunca tel tel çizgiler (saç/sakal dokusu)."""
    r = random.Random(seed); out = []
    for i in range(n):
        ox, oy = r.uniform(-jitter, jitter), r.uniform(-jitter * 0.4, jitter * 0.4)
        pts = [(x + ox + r.uniform(-2, 2), y + oy) for x, y in path_pts]
        d = f"M{pts[0][0]:.1f},{pts[0][1]:.1f} " + " ".join(f"Q{pts[k][0]:.1f},{pts[k][1]:.1f} {(pts[k][0]+pts[k+1][0])/2:.1f},{(pts[k][1]+pts[k+1][1])/2:.1f}" for k in range(1, len(pts) - 1)) + f" L{pts[-1][0]:.1f},{pts[-1][1]:.1f}"
        out.append(f'<path d="{d}" stroke="{color}" stroke-width="{width}" fill="none" opacity="{alpha}" stroke-linecap="round"/>')
    return "".join(out)

BEAD_C = ["#D9A93A", "#F6E2A0"]
def bead(x, y, s=1.0):
    return f'<rect x="{x-9*s:.1f}" y="{y-6*s:.1f}" width="{18*s:.1f}" height="{12*s:.1f}" rx="{4*s:.1f}" fill="{BEAD_C[0]}" stroke="{INK}" stroke-width="3"/><path d="M{x-6*s:.1f},{y-2*s:.1f} h{12*s:.1f}" stroke="{BEAD_C[1]}" stroke-width="2"/>'

def braid(x0, y0, x1, y1, w, color, beads=(), seed=1):
    n = max(3, int(math.hypot(x1 - x0, y1 - y0) / (w * 0.9))); o = []
    for i in range(n):
        t = (i + 0.5) / n; x = x0 + (x1 - x0) * t; y = y0 + (y1 - y0) * t
        o.append(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{w*0.55:.1f}" ry="{w*0.62:.1f}" fill="{color}" stroke="{INK}" stroke-width="3" transform="rotate({(-25 if i%2 else 25)} {x:.1f} {y:.1f})"/>')
    for b in beads:
        x = x0 + (x1 - x0) * b; y = y0 + (y1 - y0) * b; o.append(bead(x, y, w / 16))
    return "".join(o)

# ─────────── yüz ifadeleri: (kaş_iç, kaş_dış, üst_kapak, alt_kapak, ağız, ekstra)
EXP = {
    "neutral":    (0, 0, 0.15, 0.0, "flat", ""),
    "determined": (8, -4, 0.30, 0.10, "firm", ""),
    "smug":       (0, -6, 0.42, 0.05, "smirk", ""),
    "curious":    (-10, -6, 0.05, 0.0, "open_s", ""),
    "angry":      (14, -6, 0.32, 0.12, "snarl", ""),
    "grief":      (-14, 8, 0.45, 0.10, "tremble", "tear"),
    "crying":     (-16, 10, 0.62, 0.15, "sob", "tears"),
    "pain":       (12, -4, 0.70, 0.20, "grit", ""),
    "laugh":      (-6, -8, 0.55, 0.25, "laugh", ""),
    "awe":        (-12, -12, 0.0, 0.0, "open_o", ""),
    "cold":       (4, 2, 0.48, 0.12, "flat", ""),
    "tender":     (-8, 4, 0.35, 0.05, "soft_smile", ""),
    "sleepy":     (0, 2, 0.95, 0.0, "flat", ""),
}

def _eye(cx, cy, w, h, lid_up, lid_low, iris, look=0.25, skin="#EEC6A2", far=False):
    o = []
    clip = f"e{abs(hash((cx, cy, w, h, lid_up))) % 10**8}"
    shape = f"M{cx-w},{cy} Q{cx-w*0.4},{cy-h*1.15} {cx+w*0.2},{cy-h*1.0} Q{cx+w*0.9},{cy-h*0.6} {cx+w},{cy+h*0.05} Q{cx+w*0.2},{cy+h*0.95} {cx-w},{cy} Z"
    o.append(f'<defs><clipPath id="{clip}"><path d="{shape}"/></clipPath></defs>')
    o.append(f'<path d="{shape}" fill="#FBF6EE"/>')
    ir = h * 0.95
    ix = cx + look * w * 0.45
    o.append(f'<g clip-path="url(#{clip})"><circle cx="{ix:.1f}" cy="{cy:.1f}" r="{ir:.1f}" fill="{iris}"/><circle cx="{ix:.1f}" cy="{cy:.1f}" r="{ir*0.55:.1f}" fill="{shade(iris,0.55)}"/>'
             f'<circle cx="{ix:.1f}" cy="{cy:.1f}" r="{ir*0.38:.1f}" fill="#120C08"/><circle cx="{ix-ir*0.35:.1f}" cy="{cy-ir*0.38:.1f}" r="{ir*0.22:.1f}" fill="#fff"/>'
             f'<rect x="{cx-w-4}" y="{cy-h*1.4}" width="{w*2+8}" height="{h*2.4*lid_up:.1f}" fill="{skin}"/>'
             f'<rect x="{cx-w-4}" y="{cy+h*1.1 - h*2.0*lid_low:.1f}" width="{w*2+8}" height="{h*2.0*lid_low+2:.1f}" fill="{skin}"/></g>')
    ly = cy - h * 1.2 + h * 2.4 * lid_up
    o.append(f'<path d="M{cx-w-2},{max(cy-h*0.1, ly) if lid_up>0.2 else cy:.1f} Q{cx},{ly - (0 if lid_up>0.2 else h*0.9):.1f} {cx+w+2},{(cy if lid_up<=0.2 else ly):.1f}" stroke="{INK}" stroke-width="{LINE+0.5}" fill="none" stroke-linecap="round"/>')
    o.append(f'<path d="M{cx-w*0.6},{cy+h*0.85} Q{cx},{cy+h*1.05} {cx+w*0.7},{cy+h*0.7}" stroke="{shade(skin,0.72)}" stroke-width="2.5" fill="none"/>')
    return "".join(o)

def _brow(cx, cy, w, inner, outer, color, toward=1, thick=9):
    """Kama biçimli, kalın, alçak kaş. toward: iç ucun yönü (-1/1)."""
    inner = inner * 1.6 + STERN[0]; outer = outer * 1.6
    xi, xo = cx - toward * w * 1.0, cx + toward * w * 1.25
    yi = cy - 15 - inner; yo = cy - 17 - outer
    t = thick * 2.3
    # konik kalın şerit: iç uç kalın, dış uç ince; hafif kemer
    import math as _m
    dx, dy = xo - xi, yo - yi; L = _m.hypot(dx, dy) or 1; nx, ny = dy / L, -dx / L
    if ny > 0: nx, ny = -nx, -ny
    mx, my_ = (xi + xo) / 2 + nx * t * 0.35, (yi + yo) / 2 + ny * t * 0.35
    ti, to = t * 0.62, t * 0.22
    pts = [(xi + nx * ti, yi + ny * ti), (mx + nx * t * 0.5, my_ + ny * t * 0.5), (xo + nx * to, yo + ny * to),
           (xo - nx * to * 0.6, yo - ny * to * 0.6), (mx - nx * t * 0.35, my_ - ny * t * 0.35), (xi - nx * ti * 0.7, yi - ny * ti * 0.7)]
    d = (f"M{pts[0][0]:.1f},{pts[0][1]:.1f} Q{pts[1][0]:.1f},{pts[1][1]:.1f} {pts[2][0]:.1f},{pts[2][1]:.1f} "
         f"L{pts[3][0]:.1f},{pts[3][1]:.1f} Q{pts[4][0]:.1f},{pts[4][1]:.1f} {pts[5][0]:.1f},{pts[5][1]:.1f} Z")
    hair_ = "".join(f'<path d="M{xi + (xo-xi)*k:.1f},{yi + (yo-yi)*k + t*0.3:.1f} l{toward*6:.1f},{-t*0.7:.1f}" stroke="{shade(BROW_C[0],1.4)}" stroke-width="1.6" opacity="0.6"/>' for k in (0.15, 0.35, 0.55, 0.75))
    return f'<path d="{d}" fill="{BROW_C[0]}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>{hair_}'

def _mouth(mx, my, w, kind, skin):
    lip = shade(skin, 0.72)
    m = {
        "flat": f'<path d="M{mx-w},{my} Q{mx},{my+3} {mx+w},{my-1}" stroke="{INK}" stroke-width="{LINE}" fill="none" stroke-linecap="round"/>',
        "firm": f'<path d="M{mx-w},{my+1} L{mx+w},{my-1}" stroke="{INK}" stroke-width="{LINE+1}" stroke-linecap="round"/>',
        "smirk": f'<path d="M{mx-w},{my+2} Q{mx+w*0.2},{my+6} {mx+w*1.1},{my-7}" stroke="{INK}" stroke-width="{LINE}" fill="none" stroke-linecap="round"/>',
        "open_s": f'<ellipse cx="{mx}" cy="{my+2}" rx="{w*0.45}" ry="{w*0.35}" fill="#5A2018" stroke="{INK}" stroke-width="3.5"/>',
        "open_o": f'<ellipse cx="{mx}" cy="{my+4}" rx="{w*0.55}" ry="{w*0.6}" fill="#5A2018" stroke="{INK}" stroke-width="3.5"/>',
        "snarl": f'<path d="M{mx-w},{my+4} Q{mx},{my-6} {mx+w},{my+4} Q{mx},{my+10} {mx-w},{my+4} Z" fill="#5A2018" stroke="{INK}" stroke-width="3.5"/><path d="M{mx-w*0.7},{my+1} H{mx+w*0.7}" stroke="#fff" stroke-width="4"/>',
        "tremble": f'<path d="M{mx-w},{my+5} Q{mx-w*0.5},{my-1} {mx},{my+2} Q{mx+w*0.5},{my-1} {mx+w},{my+5}" stroke="{INK}" stroke-width="{LINE}" fill="none" stroke-linecap="round"/><path d="M{mx-w*0.5},{my+11} Q{mx},{my+15} {mx+w*0.5},{my+11}" stroke="{lip}" stroke-width="3" fill="none"/>',
        "tremble2": f'<path d="M{mx-w},{my+4} Q{mx-w*0.5},{my+1} {mx},{my+3} Q{mx+w*0.5},{my} {mx+w},{my+6}" stroke="{INK}" stroke-width="{LINE}" fill="none" stroke-linecap="round"/><path d="M{mx-w*0.55},{my+12} Q{mx},{my+17} {mx+w*0.5},{my+12}" stroke="{lip}" stroke-width="3" fill="none"/>',
        "sob": f'<path d="M{mx-w},{my+6} Q{mx},{my-4} {mx+w},{my+6} Q{mx},{my+14} {mx-w},{my+6} Z" fill="#5A2018" stroke="{INK}" stroke-width="3.5"/>',
        "grit": f'<rect x="{mx-w}" y="{my-5}" width="{w*2}" height="12" rx="5" fill="#F4EEE2" stroke="{INK}" stroke-width="3.5"/><path d="M{mx-w*0.4},{my-5} v12 M{mx+w*0.3},{my-5} v12" stroke="{INK}" stroke-width="2"/>',
        "laugh": f'<path d="M{mx-w*1.1},{my-3} Q{mx},{my+24} {mx+w*1.1},{my-3} Z" fill="#5A2018" stroke="{INK}" stroke-width="3.5" stroke-linejoin="round"/><path d="M{mx-w*0.8},{my} H{mx+w*0.8}" stroke="#fff" stroke-width="5"/>',
        "soft_smile": f'<path d="M{mx-w},{my-2} Q{mx},{my+8} {mx+w},{my-3}" stroke="{INK}" stroke-width="{LINE}" fill="none" stroke-linecap="round"/>',
    }[kind]
    return m

def head3(spec, view="3q", expr="neutral", look=None):
    """Kafa merkezi (0,0). Görünüş sağa bakar (gerekirse dışarıda scale(-1,1))."""
    skin = spec.get("skin", "#EEC6A2"); sh = shade(skin, 0.84); hair = spec.get("hair", "#A9783E"); hd = shade(hair, 0.72); hl = shade(hair, 1.3)
    beard = spec.get("beard_c", shade(hair, 0.9)); iris = spec.get("iris", "#7E9A8A")
    bi, bo, lu, ll, mk, extra = EXP[expr]
    _bc = BROW_C[0]; BROW_C[0] = spec.get("brow_c", _bc)
    BEAD_C[:] = spec.get("bead_c", ("#D9A93A", "#F6E2A0"))   # sahne vurgusu başka yerdeyse boncuk desatüre edilir
    o = []; late = []
    if view == "back" and spec.get("undercut"):
        stub = spec.get("stubble", "#B8A88A")
        o.append(f'<ellipse cx="0" cy="-10" rx="84" ry="100" fill="{skin}" stroke="{INK}" stroke-width="{LINE+1}"/>')
        o.append(f'<ellipse cx="0" cy="-10" rx="80" ry="96" fill="{stub}" opacity="0.5"/>')
        o.append(f'<ellipse cx="-84" cy="10" rx="13" ry="20" fill="{skin}" stroke="{INK}" stroke-width="{LINE}"/><ellipse cx="84" cy="10" rx="13" ry="20" fill="{skin}" stroke="{INK}" stroke-width="{LINE}"/>')
        if not spec.get("shaved"): o.append(f'<path d="M-36,-104 Q0,-116 36,-104 L24,10 L-24,10 Z" fill="{hair}" stroke="{INK}" stroke-width="{LINE}"/>' + strands([(0, -108), (0, -40), (0, 6)], 6, hd, 2.4, 14, 40, 0.7))
        if not (spec.get("shaved") or spec.get("nobraid")): o.append(braid(0, 0, 0, 170, 26, hair, (0.4, 0.85), 41))
        BROW_C[0] = _bc; return "".join(o)
    if view == "back":
        o.append(f'<path d="M-86,-20 Q-92,-104 0,-108 Q92,-104 86,-20 Q90,60 60,120 L-60,120 Q-90,60 -86,-20 Z" fill="{hair}" stroke="{INK}" stroke-width="{LINE+1}"/>')
        o.append(strands([(-60, -90), (-70, 0), (-50, 110)], 10, hd, 3, 30, 3) + strands([(40, -96), (60, 0), (40, 112)], 10, hd, 3, 30, 4) + strands([(0, -104), (0, 0), (0, 110)], 8, hl, 2.5, 24, 5, 0.5))
        o.append(f'<path d="M-40,40 Q0,60 40,40" stroke="#6B4A2A" stroke-width="12" fill="none"/>')  # deri bağ
        o.append(braid(-74, 0, -84, 120, 18, hair, (0.35, 0.8), 2) + braid(74, 0, 84, 120, 18, hair, (0.35, 0.8), 3))
        BROW_C[0] = _bc; return "".join(o)
    UC = spec.get("undercut", False); FEM = spec.get("female", False); NB = FEM or spec.get("beardless", False)
    # arka saç kütlesi (omuzlara)
    if UC:
        if spec.get("nobraid") or spec.get("shaved"): pass
        elif view == "3q": o.append(braid(-56, -84, -96, 90, 24, hair, (0.45, 0.85), 34))
        elif view == "side": o.append(braid(-70, -78, -104, 100, 24, hair, (0.45, 0.85), 37))
    elif FEM:
        if view == "front":
            o.append(f'<path d="M-92,-40 Q-106,50 -96,100 L96,100 Q106,50 92,-40 Z" fill="{hd}" stroke="{INK}" stroke-width="{LINE}"/>')
            o.append(strands([(-84, 0), (-96, 60), (-90, 96)], 6, shade(hd, 0.8), 2.5, 10, 71, 0.6) + strands([(84, 0), (96, 60), (90, 96)], 6, shade(hd, 0.8), 2.5, 10, 72, 0.6))
        elif view == "3q":
            if spec.get("loose"):   # Aslaug: dalgalı, omuzlardan aşağı dökülen açık saç
                o.append(f'<path d="M-90,-50 Q-136,40 -118,150 Q-134,230 -106,300 Q-70,330 -24,300 Q-44,220 -32,140 Q-44,60 -30,-50 Z" fill="{hd}" stroke="{INK}" stroke-width="{LINE}"/>')
                o.append(strands([(-96, 0), (-122, 120), (-100, 290)], 7, shade(hd, 0.78), 2.6, 12, 75, 0.7) + strands([(-60, 40), (-70, 160), (-50, 280)], 5, shade(hair, 1.12), 2.4, 10, 76, 0.6))
            else:
                o.append(f'<path d="M-88,-40 Q-112,60 -98,150 L-30,156 Q-40,80 -30,-40 Z" fill="{hd}" stroke="{INK}" stroke-width="{LINE}"/>')
                if spec.get("long_braid", True): o.append(braid(-60, -60, -88, 300, 22, hair, (0.5, 0.88), 73))
        else:
            o.append(f'<path d="M-90,-50 Q-124,90 -104,250 L-20,256 Q-40,100 -30,-50 Z" fill="{hd}" stroke="{INK}" stroke-width="{LINE}"/>')
            if spec.get("long_braid", True): o.append(braid(-72, -60, -96, 250, 22, hair, (0.5, 0.88), 74))
    elif spec.get("short_hair"):
        pass

    elif view == "front":
        o.append(f'<path d="M-90,-30 Q-104,80 -78,150 L78,150 Q104,80 90,-30 Z" fill="{hd}" stroke="{INK}" stroke-width="{LINE}"/>')
    elif view == "3q":
        o.append(f'<path d="M-86,-30 Q-106,60 -92,140 L-40,150 Q-50,60 -40,-40 Z" fill="{hd}" stroke="{INK}" stroke-width="{LINE}"/>')
    else:
        o.append(f'<path d="M-88,-40 Q-112,60 -100,150 L-50,150 Q-46,60 -40,-40 Z" fill="{hd}" stroke="{INK}" stroke-width="{LINE}"/>')
    if not UC: o.append(strands([(-80, -20), (-92, 60), (-80, 140)], 7, shade(hd, 0.8), 2.5, 10, 7, 0.6))
    # yüz konturu
    if view == "front":
        face = "M-80,-12 Q-82,-94 0,-96 Q82,-94 80,-12 L78,30 L62,66 L34,88 Q0,100 -34,88 L-62,66 L-78,30 Z"; fx = 0
        ears = [(-80, 4), (80, 4)]
    elif view == "3q":
        face = "M-70,-12 Q-72,-94 6,-96 Q84,-92 84,-10 L84,24 L74,48 L56,78 L28,96 L2,96 Q-40,88 -60,64 Q-72,32 -70,-12 Z"; fx = 20
        ears = [(-62, 6)]
    else:
        face = "M-78,-12 Q-80,-94 0,-96 Q62,-94 72,-34 L74,-8 L96,24 L76,32 Q78,46 72,56 L74,64 L66,80 L54,94 L18,96 Q-14,92 -34,72 Q-62,58 -78,-12 Z"; fx = 44
        ears = [(-14, 6)]
    if FEM:
        face = {"front": "M-76,-12 Q-78,-94 0,-96 Q78,-94 76,-12 L72,30 Q62,68 30,88 Q0,98 -30,88 Q-62,68 -72,30 Z",
                "3q": "M-68,-12 Q-70,-94 6,-96 Q82,-92 80,-10 L78,24 Q72,54 52,78 Q28,96 2,94 Q-38,86 -58,62 Q-70,32 -68,-12 Z",
                "side": "M-78,-12 Q-80,-94 0,-96 Q62,-94 70,-34 L72,-8 L88,22 L72,30 Q74,42 70,50 Q74,58 68,66 Q60,84 40,92 L18,94 Q-14,90 -34,72 Q-62,58 -78,-12 Z"}[view]
    for ex_, ey_ in ears:
        o.append(f'<ellipse cx="{ex_}" cy="{ey_}" rx="15" ry="22" fill="{skin}" stroke="{INK}" stroke-width="{LINE}"/><path d="M{ex_-4},{ey_-8} q8,6 0,16" stroke="{sh}" stroke-width="4" fill="none"/>')
    cid = f"f{abs(hash((view, expr, skin))) % 10**8}"
    o.append(f'<defs><clipPath id="{cid}"><path d="{face}"/></clipPath></defs><path d="{face}" fill="{skin}"/>')
    # cel gölge + elmacık
    if spec.get("light_left") and view == "3q":
        # yönlü ışık sol üstten: uzak yanak gölgede + çekirdek gölge şekilleri (kurul L5/L6)
        o.append(f'<g clip-path="url(#{cid})"><path d="M56,-100 Q74,-20 62,40 Q54,80 30,110 L140,110 L140,-100 Z" fill="{sh}" opacity="0.9"/>'
                 f'<path d="M-40,-14 Q-14,-26 12,-14 Q-14,6 -40,-14 Z M24,-16 Q46,-26 66,-12 Q46,6 24,-16 Z" fill="{sh}" opacity="0.55"/>'   # göz çukurları
                 f'<path d="M50,-6 Q64,14 62,40 Q54,44 46,40 Q54,18 50,-6 Z" fill="{shade(sh, 0.85)}" opacity="0.7"/>'                     # burnun gölge yanı
                 f'<path d="M-58,38 Q-30,54 -4,46 Q-30,64 -58,52 Z M40,44 Q58,52 70,44 Q60,62 40,56 Z" fill="{sh}" opacity="0.45"/>'      # elmacık altı
                 f'<path d="M-70,-90 Q-40,-70 -50,-20" stroke="#FFF6EA" stroke-width="10" fill="none" opacity="0.18"/></g>')              # ışık tarafı yumuşak parlaklık
    else:
        o.append(f'<g clip-path="url(#{cid})"><path d="{'M40,-100 Q70,0 50,110 L140,110 L140,-100 Z' if view=='front' else 'M-90,-100 Q-40,0 -60,110 L-140,110 L-140,-100 Z'}" fill="{sh}" opacity="0.85"/>'
                 + ("" if spec.get("no_blush") else f'<ellipse cx="{fx+28}" cy="22" rx="18" ry="9" fill="#D98A74" opacity="0.30"/><ellipse cx="{fx-30 if view=="front" else fx-38}" cy="22" rx="16" ry="8" fill="#D98A74" opacity="0.22"/>') + '</g>')
    o.append(f'<path d="{face}" fill="none" stroke="{INK}" stroke-width="{LINE+1}" stroke-linejoin="round"/>')
    hard = shade(skin, 0.62)
    cxs = {"front": (-32, 32), "3q": (-14, 42), "side": (44,)}[view]
    for ecx in cxs:
        o.append(f'<path d="M{ecx-18},{-30} Q{ecx},{-38} {ecx+18},{-30}" stroke="{shade(skin,0.78)}" stroke-width="7" fill="none" opacity="0.7"/>')  # kaş kemiği
        o.append(f'<path d="M{ecx-12},{12} Q{ecx},{17} {ecx+12},{11}" stroke="{hard}" stroke-width="2.4" fill="none" opacity="0.8"/>')  # göz altı
    chk = {"front": [(-58, 18, -46, 44), (58, 18, 46, 44)], "3q": [(70, 14, 60, 44), (-50, 18, -44, 40)], "side": [(40, 20, 30, 46)]}[view]
    for x0, y0, x1, y1 in ([] if (FEM or spec.get("smooth")) else chk):
        o.append(f'<path d="M{x0},{y0} L{x1},{y1}" stroke="{hard}" stroke-width="3" stroke-linecap="round" opacity="0.75"/>')  # elmacık hattı
    fxc = {"front": 0, "3q": 18, "side": 30}[view]
    if not FEM: o.append(f'<path d="M{fxc-16},{-62} q16,-5 32,0 M{fxc-10},{-52} q10,-3 20,0" stroke="{hard}" stroke-width="2.4" fill="none" opacity="0.55" stroke-linecap="round"/>')  # alın kırışığı

    # gözler + kaşlar
    lk = 0.25 if look is None else look
    if view == "front":
        for s_ in (-1, 1):
            o.append(_eye(s_ * 32, -6, 17, 9, lu, ll, iris, lk, skin))
            late.append(_brow(s_ * 32, -6, 17, bi, bo, hd, toward=-s_ if s_ < 0 else -1, thick=9*spec.get("brow_k",1)) if False else "")
        late.append(_brow(-32, -6, 17, bi, bo, hd, toward=1, thick=9*spec.get("brow_k",1))); late.append(_brow(32, -6, 17, bi, bo, hd, toward=-1, thick=9*spec.get("brow_k",1)))
        nose = f'<path d="M-2,4 Q-6,26 -8,30 Q2,36 12,30" stroke="{shade(skin,0.6)}" stroke-width="4" fill="none" stroke-linecap="round"/>'
        mx, my, mw = 0, 52, 15
    elif view == "3q":
        o.append(_eye(-14, -6, 12, 8, lu, ll, iris, lk, skin))
        o.append(_eye(42, -6, 17, 9, lu, ll, iris, lk, skin))
        late.append(_brow(-14, -6, 12, bi * 0.8, bo, hd, toward=1, thick=8*spec.get("brow_k",1))); late.append(_brow(42, -6, 17, bi, bo, hd, toward=-1, thick=9*spec.get("brow_k",1)))
        nose = f'<path d="M20,-2 L34,26 Q30,34 18,32" stroke="{INK}" stroke-width="4" fill="{sh}" stroke-linejoin="round"/>'
        if spec.get("nose2"):  # hacimli burun: köprü, gölge yanı, kanat, ışık çizgisi
            nose = (f'<path d="M12,-6 Q22,10 32,26 Q34,34 24,35 Q16,36 12,32 Q8,14 12,-6 Z" fill="{shade(sh,0.88)}" opacity="0.75"/>'
                    f'<path d="M20,-2 Q28,12 36,26 Q38,33 28,34 Q22,35 19,32" stroke="{INK}" stroke-width="4" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
                    f'<path d="M15,32 Q9,26 15,20" stroke="{INK}" stroke-width="3" fill="none" stroke-linecap="round"/>'
                    f'<path d="M25,6 Q31,15 34,22" stroke="#FFF2E2" stroke-width="2.5" fill="none" opacity="0.55" stroke-linecap="round"/>')
        mx, my, mw = 26, 54, 13
    else:
        o.append(_eye(44, -6, 13, 8, lu, ll, iris, 0.6 if look is None else look, skin))
        late.append(_brow(44, -6, 14, bi, bo, hd, toward=-1, thick=9*spec.get("brow_k",1)))
        nose = ""
        mx, my, mw = 60, 54, 8
    o.append(nose)
    if not NB:
        # sakal (çatallı, örgülü)
        i0 = len(o)
        bx = {"front": 0, "3q": 12, "side": 26}[view]
        jag = "".join(f" L{bx + x:.0f},{y:.0f}" for x, y in ((62, 150), (50, 176), (40, 168), (30, 204), (18, 190), (8, 226), (-4, 200), (-16, 222), (-26, 188), (-38, 200), (-46, 166), (-58, 176), (-66, 146)))
        beard_path = (f"M{bx-80},{26} Q{bx-90},{80} {bx-76},{120}" + "" + f" L{bx-66},{146}" + "".join(f" L{bx + x:.0f},{y:.0f}" for x, y in ((-58, 176), (-46, 166), (-38, 200), (-26, 188), (-16, 222), (-4, 200), (8, 226), (18, 190), (30, 204), (40, 168), (50, 176), (62, 150)))
                      + f" L{bx+76},{120} Q{bx+90},{80} {bx+80},{26} Q{bx+68},{60} {bx+44},{74} Q{bx+20},{86} {bx},{86} Q{bx-20},{86} {bx-44},{74} Q{bx-68},{60} {bx-80},{26} Z")
        if view == "side":
            beard_path = ("M-30,16 Q-40,96 -16,152 L-6,196 L6,178 L16,218 L28,188 L40,210 L52,172 L64,182 L74,146 "
                          "Q90,104 80,62 Q68,78 50,80 Q28,82 8,72 Q-14,52 -30,16 Z")
        bcid = f"bd{abs(hash((view, bx))) % 10**7}"
        o.append(f'<defs><clipPath id="{bcid}"><path d="{beard_path}"/></clipPath></defs>')
        o.append(f'<path d="{beard_path}" fill="{beard}" stroke="{INK}" stroke-width="{LINE+0.5}" stroke-linejoin="round"/><g clip-path="url(#{bcid})">')
        o.append(f'<path d="M{bx+40},{80} Q{bx+70},{120} {bx+46},{176}" stroke="{shade(beard,0.72)}" stroke-width="22" fill="none" opacity="0.7"/>')
        for k in range(5):
            x0 = bx - 64 + k * 32
            o.append(strands([(x0, 60), (x0 + (k - 2) * 3, 130), (x0 + (k - 2) * 6, 210)], 6, shade(beard, 0.68), 2.4, 10, 50 + k, 0.75))
        o.append(strands([(bx - 20, 90), (bx - 10, 140), (bx - 4, 200)], 5, shade(beard, 1.3), 2, 10, 60, 0.6))
        o.append('</g>')
        if spec.get("beard_braid", True): o.append(braid(bx + 2, 176, bx + 4, 262, 18, beard, (0.4, 0.8), 61) if view != "side" else braid(30, 186, 36, 268, 18, beard, (0.4, 0.8), 61))
        # yanak/şakak sakal geçişi
        if view != "side":
            o.append(f'<path d="M{bx-80},{26} Q{bx-84},{0} {bx-78},{-24}" stroke="{beard}" stroke-width="12" fill="none" stroke-linecap="round"/>')
        if view == "front":
            o.append(f'<path d="M{bx+80},{26} Q{bx+84},{0} {bx+78},{-24}" stroke="{beard}" stroke-width="12" fill="none" stroke-linecap="round"/>')
        bk, bw = spec.get("beard_len", 1.0), spec.get("beard_w", 1.0)
        if bk < 1 or bw < 1:
            cxb = bx if view != "side" else 26
            o[i0:] = [f'<g transform="translate({cxb*(1-bw):.1f},{26*(1-bk):.1f}) scale({bw},{bk})">'] + o[i0:] + ['</g>']
        # bıyık
        o.append(f'<path d="M{mx},{my-10} Q{mx-28},{my-20} {mx-40},{my} Q{mx-46},{my+18} {mx-40},{my+26} Q{mx-30},{my+4} {mx},{my-2} Q{mx+30},{my+4} {mx+40},{my+26} Q{mx+46},{my+18} {mx+40},{my} Q{mx+28},{my-20} {mx},{my-10} Z" fill="{shade(beard,0.8)}" stroke="{INK}" stroke-width="3.5"/>')
    if FEM:
        my -= 6
        o.append(f'<ellipse cx="{mx}" cy="{my+17}" rx="{mw*0.85:.1f}" ry="4.5" fill="#C9786A" opacity="0.75"/>')
        eyes_o = {"front": [(-32 - 17, -6, -1), (32 + 17, -6, 1)], "3q": [(-14 - 12, -6, -1), (42 + 17, -6, 1)], "side": [(44 + 13, -6, 1)]}[view]
        for ex_, ey_, sd in eyes_o:
            late.append(f'<path d="M{ex_ - 4*sd},{ey_-3} l{7*sd},-7 M{ex_ - 9*sd},{ey_-6} l{5*sd},-8" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>')
    o.append(_mouth(mx, my + 12, mw, mk, skin))
    # gözyaşı
    if extra in ("tear", "tears"):
        ex0 = 42 if view != "front" else 32
        o.append(f'<path d="M{ex0+4},8 Q{ex0+10},30 {ex0+6},46" stroke="#BFE2FF" stroke-width="5" fill="none" stroke-linecap="round" opacity="0.9"/><ellipse cx="{ex0+6}" cy="50" rx="5" ry="7" fill="#BFE2FF" stroke="#5A8AB0" stroke-width="2"/>')
        if extra == "tears" and view == "front":
            o.append(f'<path d="M-36,8 Q-42,30 -38,46" stroke="#BFE2FF" stroke-width="5" fill="none" opacity="0.9"/>')
    if expr == "pain":
        o.append(f'<path d="M{fx+60},-60 Q{fx+70},-44 {fx+62},-34 Q{fx+52},-44 {fx+60},-60 Z" fill="#CFEAFF" stroke="#5A8AB0" stroke-width="2"/>')
    if expr == "cold":
        o.append(f'<ellipse cx="{fx+34 if view!="side" else 88}" cy="30" rx="10" ry="7" fill="#D66A60" opacity="0.5"/>')
    # yara (yakın kaş)
    sx_ = {"front": 32, "3q": 42, "side": 44}[view]
    if FEM and spec.get("scratch"):
        sc = {"front": (44, 8), "3q": (52, 10), "side": (40, 14)}[view]
        o.append(f'<path d="M{sc[0]-6},{sc[1]-8} L{sc[0]+8},{sc[1]+10} M{sc[0]+2},{sc[1]-10} L{sc[0]+12},{sc[1]+2}" stroke="#B0605A" stroke-width="1.8" stroke-linecap="round" opacity="0.85"/>')
    if not FEM and spec.get("face_scar", True): o.append(f'<path d="M{sx_+8},-48 L{sx_+2},-20 M{sx_},8 L{sx_-8},40" stroke="#9A5A50" stroke-width="4.5" stroke-linecap="round" opacity="0.8"/><path d="M{sx_+8},-48 L{sx_+2},-20 M{sx_},8 L{sx_-8},40" stroke="#E8B8A8" stroke-width="1.6" stroke-linecap="round"/>')
    # ön saç
    if UC:
        stub = spec.get("stubble", "#B8A88A")
        # kazınmış yanlar: kafa üstü konturu içinde gölgeli kirli sakal dokusu
        scalp = {"front": "M-82,-36 Q-84,-100 0,-104 Q84,-100 82,-36 Q60,-66 0,-70 Q-60,-66 -82,-36 Z",
                 "3q": "M-74,-36 Q-82,-104 8,-106 Q88,-100 84,-38 Q64,-68 10,-72 Q-40,-68 -74,-36 Z",
                 "side": "M-80,-24 Q-84,-104 6,-106 Q66,-104 70,-60 Q40,-72 0,-68 Q-50,-60 -80,-24 Z"}[view]
        o.append(f'<path d="{scalp}" fill="{stub}" opacity="0.55"/>')
        scar_ = {"front": (36, -66, 80, -58), "3q": (-26, -68, -72, -60), "side": (-12, -60, -66, -52)}[view]
        x0_, y0_, x1_, y1_ = scar_
        mxs, mys = (x0_ + x1_) / 2, (y0_ + y1_) / 2 - 3
        d_ = f"M{x0_},{y0_} Q{mxs},{mys} {x1_},{y1_}"
        o.append(f'<path d="{d_}" stroke="#2E1C12" stroke-width="9" fill="none" stroke-linecap="round"/>'    # sürekli, koyu kahve-siyah iz
                 f'<path d="{d_}" stroke="#4A2E1E" stroke-width="4.5" fill="none" stroke-linecap="round"/>'
                 f'<path d="{d_}" stroke="#7A5040" stroke-width="1.4" fill="none" stroke-linecap="round" opacity="0.6" transform="translate(0,-2)"/>')
        o.append(f'<path d="{scalp}" fill="url(#dots)" opacity="0.5"/><defs><pattern id="dots" width="7" height="7" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.1" fill="{shade(stub,0.55)}"/></pattern></defs>')
        tie = "#5A3A22"
        if spec.get("shaved"):
            pass
        elif view == "front":
            strip = "M-38,-36 Q-50,-104 0,-122 Q50,-104 38,-36 Q20,-58 0,-60 Q-20,-58 -38,-36 Z"
            o.append(f'<path d="{strip}" fill="{hair}" stroke="{INK}" stroke-width="{LINE+0.5}" stroke-linejoin="round"/>')
            o.append(strands([(-30, -40), (-26, -96), (-6, -118)], 7, hd, 2.4, 6, 31, 0.75) + strands([(30, -40), (26, -96), (6, -118)], 7, hd, 2.4, 6, 32, 0.75) + strands([(-8, -60), (0, -100), (6, -118)], 4, hl, 3, 4, 33, 0.7))
        elif view == "3q":
            strip = "M48,-40 Q66,-96 20,-120 Q-30,-130 -62,-96 L-50,-80 Q-24,-96 4,-86 Q30,-76 48,-40 Z"
            o.append(f'<path d="{strip}" fill="{hair}" stroke="{INK}" stroke-width="{LINE+0.5}" stroke-linejoin="round"/>')
            o.append(strands([(44, -44), (34, -100), (-20, -118)], 8, hd, 2.4, 6, 35, 0.75) + strands([(20, -60), (10, -104), (-50, -100)], 5, hl, 2.6, 5, 36, 0.7))
            if not spec.get("nobraid"): o.append(f'<rect x="-70" y="-100" width="26" height="22" rx="6" fill="{tie}" stroke="{INK}" stroke-width="3.5" transform="rotate(-30 -57 -89)"/>')
        else:
            strip = "M66,-50 Q62,-104 12,-120 Q-48,-122 -74,-90 L-64,-74 Q-30,-92 6,-86 Q42,-78 66,-50 Z"
            o.append(f'<path d="{strip}" fill="{hair}" stroke="{INK}" stroke-width="{LINE+0.5}" stroke-linejoin="round"/>')
            o.append(strands([(60, -56), (24, -108), (-50, -104)], 8, hd, 2.4, 6, 38, 0.75) + strands([(30, -92), (-10, -110), (-60, -94)], 5, hl, 2.6, 5, 39, 0.7))
            if not spec.get("nobraid"): o.append(f'<rect x="-84" y="-94" width="26" height="22" rx="6" fill="{tie}" stroke="{INK}" stroke-width="3.5" transform="rotate(-40 -71 -83)"/>')
    elif view == "front":
        cap = "M-84,-10 Q-92,-110 0,-114 Q92,-110 84,-10 Q70,-60 30,-70 Q0,-62 -30,-70 Q-70,-60 -84,-10 Z"
        o.append(f'<path d="{cap}" fill="{hair}" stroke="{INK}" stroke-width="{LINE+0.5}" stroke-linejoin="round"/>')
        o.append(strands([(-70, -40), (-40, -96), (10, -108)], 8, hd, 2.5, 10, 21, 0.7) + strands([(70, -40), (40, -96), (-10, -108)], 8, hd, 2.5, 10, 22, 0.7) + strands([(-30, -100), (0, -110), (30, -100)], 5, hl, 3, 6, 23, 0.7))
        if spec.get("side_braids", True): o.append(braid(-86, -10, -92, 90, 15, hair, (0.45, 0.85), 6) + braid(86, -10, 92, 90, 15, hair, (0.45, 0.85), 7))
    elif view == "3q":
        cap = "M-78,-10 Q-90,-112 8,-116 Q90,-108 86,-14 Q74,-62 36,-72 Q4,-64 -24,-70 Q-60,-62 -78,-10 Z"
        o.append(f'<path d="{cap}" fill="{hair}" stroke="{INK}" stroke-width="{LINE+0.5}" stroke-linejoin="round"/>')
        o.append(strands([(70, -40), (40, -96), (-20, -110)], 9, hd, 2.5, 10, 24, 0.7) + strands([(-60, -50), (-40, -100), (0, -112)], 6, hd, 2.5, 8, 25, 0.6) + strands([(0, -104), (30, -108), (60, -96)], 5, hl, 3, 6, 26, 0.7))
        if spec.get("side_braids", True): o.append(braid(84, -14, 88, 82, 14, hair, (0.45, 0.85), 8))
    else:
        cap = "M-80,-10 Q-86,-112 6,-116 Q66,-110 70,-40 Q50,-74 10,-74 Q-40,-66 -80,-10 Z"
        o.append(f'<path d="{cap}" fill="{hair}" stroke="{INK}" stroke-width="{LINE+0.5}" stroke-linejoin="round"/>')
        if not spec.get("side_braids", True):  # örgüsüz uzun saç: kulak arkası ense saçla kapanır
            o.append(f'<path d="M-84,-30 Q-86,-96 -20,-104 Q-30,-60 -34,-30 Q-38,30 -60,96 L-96,96 Q-100,30 -84,-30 Z" fill="{hair}" stroke="{INK}" stroke-width="{LINE}" stroke-linejoin="round"/>')
        o.append(strands([(60, -50), (20, -100), (-60, -90)], 9, hd, 2.5, 10, 27, 0.7) + strands([(30, -106), (-20, -110), (-70, -80)], 5, hl, 3, 6, 28, 0.7))
        if spec.get("side_braids", True): o.append(braid(-6, -8, -2, 86, 14, hair, (0.45, 0.85), 9))
    if FEM and view == "3q" and spec.get("loose"):
        # öne düşen dalgalı tutam (uzak yanakta) + ince altın taç bandı + şakakta minik örgü
        late.append(f'<path d="M78,-40 Q104,40 96,140 Q92,210 70,250 Q58,236 62,200 Q78,120 66,-10 Z" fill="{hair}" stroke="{INK}" stroke-width="{LINE}" stroke-linejoin="round"/>'
                    + strands([(80, -20), (96, 80), (74, 230)], 4, shade(hair, 0.8), 2.2, 8, 77, 0.7))
        late.append(braid(-70, -40, -78, 60, 11, shade(hair, 1.08), (0.5,), 78))
        if spec.get("circlet", True):
            late.append(f'<path d="M-76,-60 Q0,-92 86,-62" stroke="{INK}" stroke-width="9" fill="none"/><path d="M-76,-60 Q0,-92 86,-62" stroke="#D8B04A" stroke-width="5" fill="none"/>'
                        f'<circle cx="10" cy="-80" r="7" fill="#3A6A5A" stroke="{INK}" stroke-width="2.5"/>')
    if FEM and view != "back" and spec.get("crown", True):
        cr = {"front": [(-82, -52, -10, -104), (-10, -104, 82, -52)], "3q": [(-74, -52, 0, -106), (0, -106, 84, -60)], "side": [(-82, -50, -10, -106), (-10, -106, 60, -78)]}[view]
        for k, (a0, b0, a1, b1) in enumerate(cr): o.append(braid(a0, b0, a1, b1, 15, hl, (), 80 + k))
    if spec.get("old") and view != "back":
        fx0 = {"front": 0, "3q": 10, "side": 20}[view]
        late.append(f'<path d="M{fx0-30},-62 q30,-8 60,0 M{fx0-24},-50 q24,-6 48,0" stroke="#8A6A56" stroke-width="2.5" fill="none" opacity="0.8"/>'
                    f'<path d="M{fx0-30},18 q-8,22 -2,42 M{fx0+34},18 q8,22 2,42" stroke="#8A6A56" stroke-width="3" fill="none" opacity="0.8"/>'
                    f'<path d="M{fx0-50},50 q8,22 26,30 M{fx0+54},50 q-8,22 -26,30" stroke="#8A6A56" stroke-width="2.5" fill="none" opacity="0.7"/>')
    res = "".join(o) + "".join(late) + spec.get("_head_extra", ""); BROW_C[0] = _bc
    return res

def hand3(x, y, r, skin, shape="open", side=1):
    """side: -1 sol, +1 sağ el. r ≈ avuç yarıçapı."""
    o = [f'<g transform="translate({x:.1f},{y:.1f}) scale({side},1)">']
    sk = skin; d = shade(skin, 0.8)
    if shape == "fist":
        o.append(f'<rect x="{-r}" y="{-r*0.9}" width="{r*2}" height="{r*1.8}" rx="{r*0.7}" fill="{sk}" stroke="{INK}" stroke-width="4"/>'
                 + "".join(f'<path d="M{-r*0.6+i*r*0.42},{-r*0.9} v{r*0.6}" stroke="{d}" stroke-width="3"/>' for i in range(4))
                 + f'<path d="M{-r},{r*0.1} Q{-r*0.2},{-r*0.2} {r*0.3},{r*0.2}" stroke="{INK}" stroke-width="3.5" fill="none"/>')
    elif shape == "grip":
        o.append(f'<path d="M{-r},{-r*0.5} Q{-r*1.1},{r*0.9} 0,{r} Q{r*1.1},{r*0.9} {r},{-r*0.3} L{r*0.5},{-r*0.6} L{r*0.2},{r*0.2} L{-r*0.1},{-r*0.5} L{-r*0.4},{r*0.2} L{-r*0.6},{-r*0.6} Z" fill="{sk}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>')
    elif shape == "point":
        o.append(f'<rect x="{-r}" y="{-r*0.7}" width="{r*1.7}" height="{r*1.5}" rx="{r*0.6}" fill="{sk}" stroke="{INK}" stroke-width="4"/>'
                 f'<rect x="{r*0.3}" y="{-r*0.55}" width="{r*1.6}" height="{r*0.55}" rx="{r*0.27}" fill="{sk}" stroke="{INK}" stroke-width="4"/>')
    else:  # open
        o.append(f'<path d="M{-r*0.8},{-r*0.6} Q{-r},{r*0.7} 0,{r*0.8} Q{r},{r*0.7} {r*0.8},{-r*0.5} Z" fill="{sk}" stroke="{INK}" stroke-width="4"/>')
        for i, (fx_, fl) in enumerate(((-0.62, 1.0), (-0.2, 1.18), (0.22, 1.12), (0.6, 0.92))):
            o.append(f'<rect x="{fx_*r - r*0.17:.1f}" y="{-r*0.6 - r*fl:.1f}" width="{r*0.34:.1f}" height="{r*fl+r*0.2:.1f}" rx="{r*0.17:.1f}" fill="{sk}" stroke="{INK}" stroke-width="3.5"/>')
        o.append(f'<path d="M{-r*0.8},{-r*0.1} Q{-r*1.4},{-r*0.4} {-r*1.3},{-r*0.9}" stroke="{INK}" stroke-width="{r*0.4+7}" stroke-linecap="round" fill="none"/><path d="M{-r*0.8},{-r*0.1} Q{-r*1.4},{-r*0.4} {-r*1.3},{-r*0.9}" stroke="{sk}" stroke-width="{r*0.4}" stroke-linecap="round" fill="none"/>')
    o.append('</g>')
    return "".join(o)

art2.HAND3 = hand3

RAVEN_CLASP = (f'<g transform="translate(-70,-430)"><circle r="34" fill="#C8CDD2" stroke="{INK}" stroke-width="5"/><circle r="27" fill="none" stroke="#9AA2AA" stroke-width="3"/>'
               f'<path d="M-24,10 Q-30,-6 -14,-12 Q-4,-22 10,-14 L28,-18 L14,-6 Q16,8 4,14 L-6,10 L-22,22 Z" fill="#1E2328" stroke="#1E2328" stroke-width="2" stroke-linejoin="round"/>'
               f'<path d="M-14,-4 Q-2,-2 6,6" stroke="#5A6470" stroke-width="2.5" fill="none"/><circle cx="8" cy="-10" r="2.6" fill="#fff"/></g>')

RAGNAR_UC = None
RAGNAR3 = dict(art2.RAGNAR_LOD, hair="#C2AD80", beard_c="#AE9466", skin="#EEC6A2", iris="#6E8FA0", tunic="#3E4A42", trim="#B8322A",
               cloak="#26344A", fur_collar="#8A8272", pants="#3A3A34", fur="#5E4A34", belt="#3A2418", _v3=True)

def figure(spec, view="3q", pose="stand", expr="neutral", facing=1, props=(), hands=("open", "open"), look=None):
    """Tam figür, ayak (0,0). view: front|3q|side|back."""
    if view in ("3q", "side") and pose == "stand":
        return f'<g transform="scale({facing},1)">{body_turn(spec, view, expr, hands, look)}</g>'

    sp = dict(spec); sp["_nohead"] = True; sp["hand_shape"] = hands
    B = BODY["tall"]; hy = B["head_cy"]
    hsvg = f'<g transform="translate({6 if view=="3q" else 10 if view=="side" else 0},{hy}) scale({B["head_r"]/80:.3f})">{head3(spec, view, expr, look)}</g>'
    clasp = spec.get("clasp", RAVEN_CLASP) if view in ("front", "3q") else ""
    sp["_head_svg"] = hsvg + clasp
    sx = {"front": 1.0, "3q": 0.88, "side": 0.62, "back": 1.0}[view]
    if view == "back":
        sp["_head_svg"] = f'<g transform="translate(0,{hy}) scale({B["head_r"]/80:.3f})">{head3(spec, "back", expr)}</g>'
    body = character(sp, "tall", pose, expr if expr in art2.EXPR else "neutral", facing=1, props=props)
    if view == "back":
        # sırtta pelerin tüm gövdeyi örter
        cl = spec.get("cloak", "#2A3E58")
        body += (f'<path d="M-110,-460 Q-150,-220 -130,-10 L130,-10 Q150,-220 110,-460 Q0,-480 -110,-460 Z" fill="{cl}" stroke="{INK}" stroke-width="5"/>'
                 f'<path d="M40,-450 Q70,-230 60,-20" stroke="{shade(cl,0.75)}" stroke-width="34" fill="none" opacity="0.8"/>' + sp["_head_svg"]
                 + f'<g transform="translate(96,-432)"><circle r="20" fill="#C8CDD2" stroke="{INK}" stroke-width="4"/></g>')
    inner = body if view != "side" else body
    return f'<g transform="scale({facing},1)"><g transform="scale({sx},1)">{inner}</g></g>' if view != "3q" else f'<g transform="scale({facing},1)">{_widen_head(body, sx)}</g>'

def _widen_head(body, sx):
    return f'<g transform="scale({sx},1)">{body}</g>'


def body_turn(spec, view, expr="neutral", hands=("open", "fist"), look=None, lean=0):
    """Ayakta, gerçek 3/4 ve profil gövde (sağa bakar). Ayak (0,0)."""
    B = BODY["tall"]; skin = spec.get("skin", "#EEC6A2"); tunic = spec["tunic"]; trim = spec.get("trim", "#B8322A")
    cloak = spec.get("cloak"); fur = spec.get("fur", "#5E4A34"); boots = "#2E2016"; td = shade(tunic, 0.78)
    hy = B["head_cy"]; shy = B["shoulder_y"]; hip = B["hip_y"]
    o = [f'<ellipse cx="0" cy="4" rx="120" ry="18" fill="#000" opacity="0.18"/>']
    if view == "3q":
        nx, fx_ = 52, -58           # yakın/uzak omuz x
        cx_off = 8
        torso = f"M{fx_-6},{shy-6} Q{fx_-14},{(shy+hip)/2} {fx_-2},{hip} L{fx_-12},{hip+60} Q10,{hip+76} {nx+18},{hip+56} L{nx+6},{hip} Q{nx+16},{(shy+hip)/2} {nx+8},{shy-6} Q0,{shy-20} {fx_-6},{shy-6} Z"
        buckle_x = 16; legs = [(-26, -6, 4), (30, 8, 0)]
    else:
        nx, fx_ = 30, -40
        cx_off = 18
        torso = f"M{fx_},{shy-4} Q{fx_-18},{(shy+hip)/2} {fx_+2},{hip} L{fx_-6},{hip+60} Q0,{hip+72} {nx+26},{hip+54} L{nx+16},{hip} Q{nx+34},{shy+70} {nx+20},{shy-4} Q0,{shy-16} {fx_},{shy-4} Z"
        buckle_x = nx + 8; legs = [(-8, -10, 6), (12, 12, -4)]
    # pelerin arkada
    if cloak:
        o.append(f'<path d="M{fx_-14},{shy-10} Q{fx_-70},{hip} {fx_-60},-14 L{nx-10},-14 Q{nx-20},{hip} {nx-30},{shy} Z" fill="{cloak}" stroke="{INK}" stroke-width="5"/>')
    # uzak kol (arkada)
    fa = [(fx_ + 6, shy + 14), (fx_ - 10, shy + 110), (fx_ + 60, shy + 160)] if spec.get("_carry_svg") else [(fx_ + 6, shy + 14), (fx_ - 10, shy + 120), (fx_ + 4, shy + 228)]
    o.append(limb(fa, 34, shade(tunic, 0.7)))
    o.append(hand3(fa[-1][0], fa[-1][1], 19, shade(skin, 0.9), hands[0], 1))
    # bacaklar (kıllı pantolon) + çizme
    KN = spec.get("_kneel", 0)          # diz çökme: gövde KN kadar iner, bacaklar katlanır (model gövdesi korunur)
    kneel_legs = []
    for lx, ang, dy in legs:
        if KN:
            hx_, hy_ = lx, hip + 30 + KN; kx_, ky_ = lx + 92, -26; fx2, fy2 = lx - 70, -16
            kneel_legs.append(art2.fur_leg(hx_, hy_, kx_, ky_, 56, fur) + art2.fur_leg(kx_, ky_, fx2, fy2, 50, fur)
                              + f'<path d="M{fx2+10},{fy2-20} L{fx2-60},{fy2-24} Q{fx2-76},{fy2-6} {fx2-62},{fy2+14} L{fx2+10},{fy2+14} Z" fill="{boots}" stroke="{INK}" stroke-width="4.5" stroke-linejoin="round"/>')
            continue
        x0, y0 = lx, hip + 30; x1, y1 = lx + ang, -20 + dy
        o.append(art2.fur_leg(x0, y0, x1, y1, 54, fur))
        o.append(f'<path d="M{x1-26},{y1-6} L{x1+22},{y1-6} Q{x1+50},{y1+6} {x1+46},{y1+22} L{x1-28},{y1+22} Z" fill="{boots}" stroke="{INK}" stroke-width="4.5" stroke-linejoin="round"/>')
    # gövde
    cid = f"bt{view}"
    o.append(f'<defs><clipPath id="{cid}"><path d="{torso}"/></clipPath></defs><path d="{torso}" fill="{tunic}"/>')
    o.append(f'<g clip-path="url(#{cid})"><rect x="{nx-30}" y="{shy-40}" width="120" height="600" fill="{td}"/>'
             f'<path d="M{fx_-20},{hip+50} Q0,{hip+66} {nx+30},{hip+46}" stroke="{trim}" stroke-width="12" fill="none"/>'
             f'<path d="M{cx_off-12},{shy-8} L{cx_off+4},{shy+40} L{cx_off+18},{shy-8}" stroke="{trim}" stroke-width="7" fill="none"/></g>')
    o.append(f'<path d="{torso}" fill="none" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>')
    o.append(f'<path d="M{fx_-4},{hip-6} Q0,{hip+4} {nx+12},{hip-8}" stroke="#3A2418" stroke-width="18" fill="none"/><path d="M{fx_-4},{hip-6} Q0,{hip+4} {nx+12},{hip-8}" stroke="{INK}" stroke-width="3" fill="none" opacity="0.6"/>')
    o.append(f'<rect x="{buckle_x-12}" y="{hip-16}" width="24" height="22" rx="4" fill="#D8A93A" stroke="{INK}" stroke-width="3.5"/>')
    # kürk yaka
    for i in range(7):
        t = i / 6; x = fx_ - 18 + (nx + 30 - (fx_ - 18)) * t; y = shy - 6 + 8 * math.sin(t * math.pi)
        o.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="22" fill="{spec.get("fur_collar","#8A8272")}" stroke="{INK}" stroke-width="4"/>')
    # boyun + kafa
    o.append(f'<rect x="{cx_off-22}" y="{hy+70}" width="44" height="{shy-hy-60}" fill="{shade(skin,0.85)}" stroke="{INK}" stroke-width="4"/>')
    o.append(f'<g transform="translate({cx_off},{hy}) scale({B["head_r"]/80:.3f})">{head3(spec, view, expr, look)}</g>')
    if view == "3q": o.append(spec.get("clasp", RAVEN_CLASP).replace("translate(-70,-430)", "translate(-34,-430)").replace("translate(0,-440)", "translate(-34,-430)"))
    if spec.get("_body_extra"): o.append(spec["_body_extra"])   # gövde önü eklentisi (karın, kılıç kemeri), kolun altında
    # yakın kol (önde); kucak pozunda kol göğsün önünden karşıya kıvrılır ve bebek kolların arasındadır
    if spec.get("_arm_up"):
        na = [(nx, shy + 16), (nx + 74, shy - 70), (nx + 112, shy - 186)]
    elif spec.get("_carry_svg"):
        o.append(spec["_carry_svg"])
        na = [(nx, shy + 16), (nx + 30, shy + 118), (fx_ - 4, shy + 132)]
        hands = (hands[0], "grip")
    else:
        na = [(nx, shy + 16), (nx + 22, shy + 122), (nx + 10, shy + 230)]
    if spec.get("_arm_up") and not spec.get("_carry_svg"): pass
    if spec.get("_noarm"):   # yakın kol sahnede ayrı nesne olarak çiziliyor (ör. kalkık kol + seax)
        return "".join(o)
    o.append(limb(na, 38, tunic))
    if spec.get("armring", True): o.append(f'<circle cx="{(na[1][0]+na[2][0])/2:.0f}" cy="{(na[1][1]+na[2][1])/2:.0f}" r="23" fill="none" stroke="#D9A93A" stroke-width="8"/>')
    o.append(hand3(na[-1][0], na[-1][1], 21, skin, hands[1], 1))
    if not spec.get("female") and spec.get("knot", True): o.append(knot_mark(na[-1][0], na[-1][1] - 2, 0.55))
    if spec.get("_hand_extra"): o.append(spec["_hand_extra"].replace("HX", f"{na[-1][0]}").replace("HY", f"{na[-1][1]}"))
    if KN:
        cid2 = f"kn{KN}"
        return ("".join(kneel_legs) + f'<defs><clipPath id="{cid2}"><rect x="-400" y="-1200" width="800" height="{1200 - 20}"/></clipPath></defs>'
                f'<g clip-path="url(#{cid2})"><g transform="translate(0,{KN})">' + "".join(o) + '</g></g>')
    return "".join(o)

def knot_mark(x, y, s=1.0, c="#2E4A5E"):
    """Düğüm (valknut benzeri değil, üç halkalı özgün düğüm) — el sırtı / önkol deseni."""
    return (f'<g transform="translate({x:.1f},{y:.1f}) scale({s})" opacity="0.85">'
            + "".join(f'<circle cx="{10*math.cos(a):.1f}" cy="{10*math.sin(a):.1f}" r="9" fill="none" stroke="{c}" stroke-width="3"/>' for a in (-1.57, 0.52, 2.62))
            + '</g>')

def forearm_band(c="#2E4A5E"):
    """Ragnar önkol düğüm bandı — TEK KAYNAK (R8). Yerel: forearm_detail koordinatı, 11° eğik."""
    o = [f'<g transform="rotate(11)"><rect x="20" y="-18" width="110" height="46" rx="14" fill="none" stroke="{c}" stroke-width="3" opacity="0.8"/>']
    for k in range(5):
        o.append(f'<path d="M{30+k*20},{-10+k*4} q10,14 0,28 q-10,-14 0,-28" stroke="{c}" stroke-width="3" fill="none" opacity="0.85"/>')
    return "".join(o) + "</g>"

def forearm_detail():
    """Model sayfası için: sıvanmış kol, önkolda düğüm bandı + el sırtı sembolü."""
    skin = "#EEC6A2"
    o = [limb([(0, 0), (150, 30)], 64, skin)]
    o.append(forearm_band())
    o.append(limb([(-40, -6), (0, 0)], 72, "#3E4A42"))
    o.append(hand3(190, 40, 28, skin, "fist", 1))
    o.append(knot_mark(186, 34, 0.9))
    return "".join(o)

RAGNAR_UC = dict(RAGNAR3, undercut=True, hair="#5C3F27", beard_c="#5A3E28", stubble="#6E5A46", iris="#6A8CA0")
