"""Ragnar v2 — özgün karakter ve dekor kütüphanesi (SVG üretir).
Işık soldan-üstten gelir; gölge sağ/alt tarafa düşer (cel shading).
"""
import math, itertools

INK = "#2A1D14"
_uid = itertools.count()
def uid(p="u"): return f"{p}{next(_uid)}"

def shade(hexc, f):
    """f<1 koyulaştır, f>1 açıklaştır."""
    h = hexc.lstrip('#'); r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    if f < 1: r, g, b = int(r*f), int(g*f), int(b*f*1.04)
    else:
        k = f - 1; r, g, b = int(r+(255-r)*k), int(g+(255-g)*k), int(b+(255-b)*k)
    clamp = lambda v: max(0, min(255, v))
    return f"#{clamp(r):02x}{clamp(g):02x}{clamp(b):02x}"

def P(*pts): return " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)

def limb(pts, w, color, outline=INK, ow=5, shadow=True):
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    s = (f'<path d="{d}" fill="none" stroke="{outline}" stroke-width="{w+ow*2}" stroke-linecap="round" stroke-linejoin="round"/>'
         f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>')
    if shadow:
        # alt kenar boyunca ince gölge
        s += f'<path d="{d}" fill="none" stroke="{shade(color,0.78)}" stroke-width="{w*0.35:.1f}" stroke-linecap="round" stroke-linejoin="round" transform="translate({w*0.22:.1f},{w*0.12:.1f})" opacity="0.8"/>'
    return s

def polar(x, y, length, ang_deg):
    a = math.radians(ang_deg)
    return x + length * math.sin(a), y + length * math.cos(a)

# ═══════════════════════════════════════════ KARAKTER
BODY = {
    "child": dict(head_r=78, head_cy=-268, shoulder_y=-176, sx=40, hip_y=-96, torso_w=96, leg=96, au=56, al=52, hand=15, limbw=26, legw=30, neck=0),
    "teen":  dict(head_r=70, head_cy=-392, shoulder_y=-302, sx=52, hip_y=-170, torso_w=118, leg=168, au=86, al=82, hand=16, limbw=30, legw=36, neck=8),
    "tall": dict(head_r=82, head_cy=-560, shoulder_y=-452, sx=84, hip_y=-240, torso_w=178, leg=240, au=128, al=120, hand=22, limbw=40, legw=48, neck=14),
    "adult": dict(head_r=76, head_cy=-468, shoulder_y=-370, sx=72, hip_y=-200, torso_w=156, leg=200, au=100, al=96, hand=19, limbw=38, legw=46, neck=10),
}

POSES_OLD = {  # (sol omuz, sol dirsek, sağ omuz, sağ dirsek) açıları; 0 = aşağı, + = dışa/ileri
    "stand":      (14, 6, 14, 6),
    "hips":       (38, 120, 38, 120),
    "arms_up":    (160, -10, 160, -10),
    "one_up":     (14, 6, 165, -5),
    "point":      (14, 6, 95, 0),
    "cross":      (30, 105, 30, 105),
    "hold_front": (40, 60, 40, 60),
    "spear":      (25, 55, 75, 20),
    "thrust":     (60, 30, 92, 0),
    "shield":     (80, 10, 30, 70),
    "shrug":      (55, 115, 55, 115),
    "wave":       (14, 6, 150, 30),
    "sit":        (35, 60, 35, 60),
    "sleep":      (30, 80, 30, 80),
    "count":      (55, 95, 50, 100),
    "grip":       (40, 80, 40, 80),
}

# El hedefleri: (sol_el, sağ_el) — omuza göre, kol boyu birimiyle; x+ = dışarı, y+ = aşağı
POSES = {
    "stand": ((0.22, 0.95), (0.22, 0.95)), "hips": ((-0.02, 0.62), (-0.02, 0.62)), "arms_up": ((0.4, -0.88), (0.4, -0.88)),
    "one_up": ((0.22, 0.95), (0.18, -0.95)), "point": ((0.22, 0.95), (0.98, -0.08)), "cross": ((-0.62, 0.42), (-0.55, 0.36)),
    "hold_front": ((-0.12, 0.6), (-0.12, 0.6)), "spear": ((0.22, 0.95), (0.32, 0.5)), "thrust": ((0.15, 0.55), (0.97, 0.08)),
    "shield": ((0.5, 0.45), (0.32, 0.5)), "shrug": ((0.62, -0.05), (0.62, -0.05)), "wave": ((0.22, 0.95), (0.62, -0.72)),
    "sit": ((0.05, 0.62), (0.05, 0.62)), "sleep": ((-0.2, 0.55), (-0.2, 0.55)), "count": ((-0.3, 0.55), (-0.15, 0.5)),
    "grip": ((0.25, 0.6), (0.25, 0.6)), "reach": ((0.22, 0.95), (0.9, 0.3)), "give": ((0.7, 0.25), (0.7, 0.25)),
    "bound": ((-0.25, 0.5), (-0.25, 0.5)), "fist_up": ((0.22, 0.95), (0.25, -0.95)),
}
def ik(S, T, a, b, bend_out=True, side=1):
    dx, dy = T[0]-S[0], T[1]-S[1]; d = max(1e-3, min(math.hypot(dx, dy), a+b-0.5))
    base = math.atan2(dy, dx)
    cosA = max(-1, min(1, (a*a + d*d - b*b) / (2*a*d))); A = math.acos(cosA)
    sgn = (1 if side > 0 else -1) * (-1 if bend_out else 1)
    ang = base + sgn * A
    E = (S[0] + a*math.cos(ang), S[1] + a*math.sin(ang))
    H = (S[0] + d*math.cos(base), S[1] + d*math.sin(base))
    return E, H

EXPR = ["neutral", "happy", "smug", "angry", "sad", "surprised", "sleepy", "determined", "smitten", "pain", "cold"]

def eyes(ex, ey, expr, r=13, iris="#4A6E8A", snake=False, look=0.0):
    out = []
    closed = expr in ("sleepy",)
    for sx in (-1, 1):
        cx = ex * sx
        if closed:
            out.append(f'<path d="M{cx-r},{ey} Q{cx},{ey+r*0.7} {cx+r},{ey}" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>')
            continue
        ry = r * (1.15 if expr in ("surprised",) else 0.62 if expr in ("smug", "cold") else 0.95)
        out.append(f'<ellipse cx="{cx}" cy="{ey}" rx="{r}" ry="{ry:.1f}" fill="#FFFDF7" stroke="{INK}" stroke-width="4"/>')
        ir = r * 0.62
        ix = cx + look * r * 0.35
        out.append(f'<circle cx="{ix:.1f}" cy="{ey+1}" r="{min(ir, ry*0.95):.1f}" fill="{iris}"/>')
        out.append(f'<circle cx="{ix:.1f}" cy="{ey+1}" r="{ir*0.5:.1f}" fill="{INK}"/>')
        if snake and sx == 1:
            out.append(f'<circle cx="{ix:.1f}" cy="{ey+1}" r="{ir*0.78:.1f}" fill="none" stroke="#7FB04A" stroke-width="3"/>')
            out.append(f'<path d="M{ix+ir*0.78:.1f},{ey+1} l5,-3 l-1,5 z" fill="#7FB04A"/>')
        out.append(f'<circle cx="{ix-ir*0.35:.1f}" cy="{ey-ir*0.35:.1f}" r="{ir*0.28:.1f}" fill="#fff"/>')
        # üst göz kapağı
        lid = {"smug": 0.35, "cold": 0.4, "sad": 0.25, "determined": 0.25, "angry": 0.3, "smitten": 0.3, "pain": 0.45}.get(expr, 0)
        if lid:
            out.append(f'<path d="M{cx-r-1},{ey-ry} L{cx+r+1},{ey-ry} L{cx+r+1},{ey-ry+2*ry*lid} Q{cx},{ey-ry+2*ry*lid+3} {cx-r-1},{ey-ry+2*ry*lid} Z" fill="{SKIN_CUR[0]}" stroke="none"/>')
            out.append(f'<path d="M{cx-r-1},{ey-ry+2*ry*lid} Q{cx},{ey-ry+2*ry*lid+3} {cx+r+1},{ey-ry+2*ry*lid}" stroke="{INK}" stroke-width="4" fill="none"/>')
        else:
            out.append(f'<path d="M{cx-r-2},{ey-ry*0.55} Q{cx},{ey-ry*1.35} {cx+r+2},{ey-ry*0.55}" stroke="{INK}" stroke-width="4.5" fill="none" stroke-linecap="round"/>')
    return "".join(out)

SKIN_CUR = ["#F0C49C"]

def brows(ex, ey, expr, color, thick=7):
    b = {
        "neutral": ((-8, -2), (8, -4)), "happy": ((-8, -6), (8, -6)), "smug": ((-8, 0), (8, -8)),
        "angry": ((-10, -10), (8, 4)), "sad": ((-8, 4), (8, -8)), "surprised": ((-8, -12), (8, -12)),
        "sleepy": ((-8, 0), (8, 0)), "determined": ((-10, -6), (8, 2)), "smitten": ((-8, -2), (8, -8)),
        "pain": ((-8, 4), (8, -6)), "cold": ((-8, -2), (8, 0)),
    }[expr]
    out = []
    for sx in (-1, 1):
        cx = ex * sx
        (x1, y1), (x2, y2) = b
        if sx == -1: x1, x2 = -x1, -x2
        y0 = ey - 26
        out.append(f'<path d="M{cx + x1*1.6:.1f},{y0 + (y1 if sx==1 else y2):.1f} Q{cx},{y0 - 6 + (y1+y2)/2:.1f} {cx + x2*1.6:.1f},{y0 + (y2 if sx==1 else y1):.1f}" stroke="{color}" stroke-width="{thick}" stroke-linecap="round" fill="none"/>')
    return "".join(out)

def mouth(my, expr, beard=False):
    m = {
        "neutral": f'<path d="M-12,{my} Q0,{my+3} 12,{my}" stroke="{INK}" stroke-width="4.5" fill="none" stroke-linecap="round"/>',
        "happy": f'<path d="M-18,{my-3} Q0,{my+20} 18,{my-3} Z" fill="#7A2E24" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/><path d="M-12,{my+1} Q0,{my+5} 12,{my+1}" stroke="#fff" stroke-width="4" fill="none"/>',
        "smug": f'<path d="M-14,{my+2} Q2,{my+8} 16,{my-6}" stroke="{INK}" stroke-width="4.5" fill="none" stroke-linecap="round"/>',
        "angry": f'<path d="M-16,{my+6} Q0,{my-6} 16,{my+6}" stroke="{INK}" stroke-width="5" fill="none" stroke-linecap="round"/>',
        "sad": f'<path d="M-14,{my+6} Q0,{my-4} 14,{my+6}" stroke="{INK}" stroke-width="4.5" fill="none" stroke-linecap="round"/>',
        "surprised": f'<ellipse cx="0" cy="{my+4}" rx="9" ry="12" fill="#7A2E24" stroke="{INK}" stroke-width="4"/>',
        "sleepy": f'<ellipse cx="2" cy="{my+2}" rx="6" ry="5" fill="#7A2E24" stroke="{INK}" stroke-width="3.5"/>',
        "determined": f'<path d="M-14,{my+2} L14,{my}" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>',
        "smitten": f'<path d="M-14,{my-2} Q0,{my+12} 14,{my-2}" stroke="{INK}" stroke-width="4.5" fill="none" stroke-linecap="round"/>',
        "pain": f'<path d="M-16,{my+4} L-8,{my} L0,{my+4} L8,{my} L16,{my+4}" stroke="{INK}" stroke-width="4" fill="none" stroke-linejoin="round"/>',
        "cold": f'<path d="M-12,{my+1} L12,{my+1}" stroke="{INK}" stroke-width="4.5" stroke-linecap="round"/>',
    }[expr]
    return m

def hair_back(style, color, r, cy):
    c = color; d = shade(c, 0.78)
    if style == "long":      # omuzlara dökülen
        return f'<path d="M{-r*1.08},{cy-r*0.3} Q{-r*1.25},{cy+r*1.6} {-r*0.85},{cy+r*2.1} L{r*0.85},{cy+r*2.1} Q{r*1.25},{cy+r*1.6} {r*1.08},{cy-r*0.3} Z" fill="{d}" stroke="{INK}" stroke-width="5"/>'
    if style == "flow":      # rüzgârda dalgalanan (Lagertha)
        return (f'<path d="M{-r*1.0},{cy-r*0.5} Q{-r*1.7},{cy+r*0.9} {-r*2.4},{cy+r*1.7} Q{-r*1.6},{cy+r*1.5} {-r*1.9},{cy+r*2.3} '
                f'Q{-r*0.9},{cy+r*1.7} {-r*0.4},{cy+r*1.6} L{r*0.9},{cy+r*1.2} Q{r*1.25},{cy+r*0.4} {r*1.05},{cy-r*0.4} Z" fill="{c}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
                f'<path d="M{-r*1.3},{cy+r*0.6} Q{-r*1.8},{cy+r*1.2} {-r*2.1},{cy+r*1.8}" stroke="{d}" stroke-width="5" fill="none"/>')
    if style == "ankle":     # ayak bileğine kadar (Kráka)
        return (f'<path d="M{-r*1.05},{cy-r*0.3} Q{-r*1.5},{cy+r*3} {-r*1.25},{cy+r*5.9} L{r*1.25},{cy+r*5.9} Q{r*1.5},{cy+r*3} {r*1.05},{cy-r*0.3} Z" fill="{c}" stroke="{INK}" stroke-width="5"/>'
                + "".join(f'<path d="M{x*r:.0f},{cy+r*1.2} Q{x*r*1.1:.0f},{cy+r*4} {x*r*0.95:.0f},{cy+r*5.7}" stroke="{d}" stroke-width="4" fill="none"/>' for x in (-0.9, -0.45, 0.45, 0.9)))
    if style == "tied":      # arkaya bağlı + yan örgü (Ragnar)
        return f'<path d="M{-r*0.95},{cy-r*0.2} Q{-r*1.1},{cy+r*1.0} {-r*0.7},{cy+r*1.4} L{r*0.7},{cy+r*1.4} Q{r*1.1},{cy+r*1.0} {r*0.95},{cy-r*0.2} Z" fill="{d}" stroke="{INK}" stroke-width="5"/>'
    return ""

def hair_front(style, color, r, cy):
    c = color; l = shade(c, 1.25)
    top = cy - r
    if style in ("long", "flow", "ankle"):
        s = (f'<path d="M{-r*1.02},{cy+r*0.2} Q{-r*1.12},{top-r*0.05} {-r*0.2},{top-r*0.08} Q{r*0.9},{top-r*0.02} {r*1.04},{cy+r*0.15} '
             f'Q{r*0.75},{cy-r*0.55} {r*0.1},{cy-r*0.62} Q{-r*0.6},{cy-r*0.5} {-r*1.02},{cy+r*0.2} Z" fill="{c}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>')
        s += f'<path d="M{-r*0.5},{top+r*0.12} Q{-r*0.1},{top+r*0.02} {r*0.3},{top+r*0.12}" stroke="{l}" stroke-width="6" fill="none" stroke-linecap="round"/>'
        return s
    if style == "tied":
        s = (f'<path d="M{-r*1.0},{cy-r*0.05} Q{-r*1.05},{top-r*0.06} {0},{top-r*0.1} Q{r*1.05},{top-r*0.06} {r*1.0},{cy-r*0.05} '
             f'Q{r*0.6},{cy-r*0.58} {0},{cy-r*0.6} Q{-r*0.6},{cy-r*0.58} {-r*1.0},{cy-r*0.05} Z" fill="{c}" stroke="{INK}" stroke-width="5"/>')
        s += f'<path d="M{-r*0.6},{top+r*0.16} Q0,{top+r*0.0} {r*0.6},{top+r*0.16}" stroke="{l}" stroke-width="6" fill="none" stroke-linecap="round"/>'
        # sağ yan örgü
        for k in range(4):
            s += f'<ellipse cx="{r*1.02}" cy="{cy+r*0.05+k*r*0.32:.0f}" rx="{r*0.15:.0f}" ry="{r*0.19:.0f}" fill="{c}" stroke="{INK}" stroke-width="3.5"/>'
        return s
    if style == "tousled":
        pts = []
        for i in range(11):
            a = math.pi + i * math.pi / 10
            rr = r * (1.12 if i % 2 else 0.98)
            pts.append((rr * math.cos(a), cy + rr * math.sin(a) * 0.95))
        s = f'<path d="M{-r*1.02},{cy+r*0.1} L' + " L".join(f"{x:.0f},{y:.0f}" for x, y in pts) + f' L{r*1.02},{cy+r*0.1} Q{r*0.5},{cy-r*0.55} 0,{cy-r*0.5} Q{-r*0.5},{cy-r*0.55} {-r*1.02},{cy+r*0.1} Z" fill="{c}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
        s += f'<path d="M{-r*0.4},{top+r*0.15} q{r*0.3},{-r*0.1} {r*0.6},0" stroke="{l}" stroke-width="6" fill="none" stroke-linecap="round"/>'
        return s
    if style == "bald":
        return f'<path d="M{-r*0.5},{top+r*0.18} Q{-r*0.2},{top+r*0.05} {r*0.1},{top+r*0.12}" stroke="#fff" stroke-width="8" opacity="0.7" fill="none" stroke-linecap="round"/>' \
               f'<path d="M{-r*1.02},{cy-r*0.05} Q{-r*1.1},{cy+r*0.35} {-r*0.9},{cy+r*0.5} L{-r*0.85},{cy} Z M{r*1.02},{cy-r*0.05} Q{r*1.1},{cy+r*0.35} {r*0.9},{cy+r*0.5} L{r*0.85},{cy} Z" fill="{c}" stroke="{INK}" stroke-width="4"/>'
    if style == "short":
        return (f'<path d="M{-r*1.0},{cy} Q{-r*1.05},{top-r*0.08} 0,{top-r*0.1} Q{r*1.05},{top-r*0.08} {r*1.0},{cy} '
                f'Q{r*0.7},{cy-r*0.5} {r*0.2},{cy-r*0.55} L0,{cy-r*0.4} L{-r*0.2},{cy-r*0.56} Q{-r*0.7},{cy-r*0.5} {-r*1.0},{cy} Z" fill="{c}" stroke="{INK}" stroke-width="5"/>'
                f'<path d="M{-r*0.5},{top+r*0.15} Q0,{top+r*0.02} {r*0.5},{top+r*0.15}" stroke="{l}" stroke-width="6" fill="none" stroke-linecap="round"/>')
    if style == "braidcrown":   # Thora: başa sarılı örgü
        s = hair_front("short", c, r, cy)
        for k in range(9):
            a = math.pi + k * math.pi / 8
            s += f'<ellipse cx="{r*0.98*math.cos(a):.0f}" cy="{cy - r*0.2 + r*0.85*math.sin(a):.0f}" rx="{r*0.17:.0f}" ry="{r*0.13:.0f}" fill="{c}" stroke="{INK}" stroke-width="3.5"/>'
        return s
    if style == "hood":
        return (f'<path d="M{-r*1.25},{cy+r*0.9} Q{-r*1.35},{top-r*0.35} 0,{top-r*0.4} Q{r*1.35},{top-r*0.35} {r*1.25},{cy+r*0.9} '
                f'L{r*0.95},{cy+r*0.6} Q{r*0.95},{cy-r*0.75} 0,{cy-r*0.8} Q{-r*0.95},{cy-r*0.75} {-r*0.95},{cy+r*0.6} Z" fill="{c}" stroke="{INK}" stroke-width="5"/>')
    return ""

def beard_svg(style, color, r, cy, beads="#E2B23A"):
    if style == "none": return ""
    c = color; d = shade(c, 0.8); l = shade(c, 1.2)
    jaw = cy + r * 0.25
    if style == "stubble":
        return f'<path d="M{-r*0.8},{jaw} Q0,{cy+r*1.12} {r*0.8},{jaw}" fill="{c}" opacity="0.35"/>'
    L = {"short": 0.55, "full": 0.95, "long": 1.55, "braids": 1.2, "white_long": 1.9, "neat": 0.5}[style]
    s = (f'<path d="M{-r*0.92},{cy-r*0.05} Q{-r*0.95},{jaw+r*L*0.6} {-r*0.35},{jaw+r*L} Q0,{jaw+r*L*1.15} {r*0.35},{jaw+r*L} '
         f'Q{r*0.95},{jaw+r*L*0.6} {r*0.92},{cy-r*0.05} Q{r*0.55},{cy+r*0.35} 0,{cy+r*0.42} Q{-r*0.55},{cy+r*0.35} {-r*0.92},{cy-r*0.05} Z" '
         f'fill="{c}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>')
    s += f'<path d="M{r*0.35},{jaw+r*L*0.2} Q{r*0.5},{jaw+r*L*0.6} {r*0.2},{jaw+r*L*0.95}" stroke="{d}" stroke-width="6" fill="none" stroke-linecap="round"/>'
    s += f'<path d="M{-r*0.45},{jaw+r*0.1} Q{-r*0.55},{jaw+r*L*0.5} {-r*0.3},{jaw+r*L*0.8}" stroke="{l}" stroke-width="5" fill="none" stroke-linecap="round" opacity="0.8"/>'
    if style in ("braids", "white_long"):
        for bx in (-0.22, 0.22):
            y0 = jaw + r * L * 0.85
            for k in range(3):
                s += f'<ellipse cx="{bx*r:.0f}" cy="{y0 + k*r*0.2:.0f}" rx="{r*0.11:.0f}" ry="{r*0.13:.0f}" fill="{c}" stroke="{INK}" stroke-width="3"/>'
            s += f'<rect x="{bx*r - r*0.13:.0f}" y="{y0 + r*0.62:.0f}" width="{r*0.26:.0f}" height="{r*0.14:.0f}" rx="4" fill="{beads}" stroke="{INK}" stroke-width="3"/>'
            s += f'<rect x="{bx*r - r*0.13:.0f}" y="{y0 + r*0.12:.0f}" width="{r*0.26:.0f}" height="{r*0.12:.0f}" rx="4" fill="{beads}" stroke="{INK}" stroke-width="3"/>'
    # bıyık
    s += (f'<path d="M0,{cy+r*0.38} Q{-r*0.35},{cy+r*0.25} {-r*0.62},{cy+r*0.55} Q{-r*0.3},{cy+r*0.52} 0,{cy+r*0.48} '
          f'Q{r*0.3},{cy+r*0.52} {r*0.62},{cy+r*0.55} Q{r*0.35},{cy+r*0.25} 0,{cy+r*0.38} Z" fill="{d}" stroke="{INK}" stroke-width="3.5"/>')
    return s

def head(spec, r, cy, expr):
    skin = spec.get("skin", "#F0C49C"); SKIN_CUR[0] = skin
    sh = shade(skin, 0.86)
    hairc = spec.get("hair", "#C99A4E")
    out = [hair_back(spec.get("hair_style", "short"), hairc, r, cy) if spec.get("_hb_inline") else ""]
    # kulaklar
    for sx in (-1, 1):
        out.append(f'<ellipse cx="{sx*r*0.98:.0f}" cy="{cy+r*0.08:.0f}" rx="{r*0.17:.0f}" ry="{r*0.24:.0f}" fill="{skin}" stroke="{INK}" stroke-width="4"/>')
    # yüz (hafif köşeli çene erkek için)
    jaw = spec.get("jaw", 1.0)
    face = (f'M{-r},{cy-r*0.1} Q{-r},{cy-r*1.02} 0,{cy-r*1.02} Q{r},{cy-r*1.02} {r},{cy-r*0.1} '
            f'Q{r*0.98*jaw},{cy+r*0.75} 0,{cy+r*0.98} Q{-r*0.98*jaw},{cy+r*0.75} {-r},{cy-r*0.1} Z')
    cid = uid("fc")
    out.append(f'<defs><clipPath id="{cid}"><path d="{face}"/></clipPath></defs>')
    out.append(f'<path d="{face}" fill="{skin}" stroke="{INK}" stroke-width="5"/>')
    out.append(f'<g clip-path="url(#{cid})"><ellipse cx="{r*0.95:.0f}" cy="{cy+r*0.2:.0f}" rx="{r*0.55:.0f}" ry="{r*1.3:.0f}" fill="{sh}" opacity="0.8"/></g>')
    out.append(f'<path d="{face}" fill="none" stroke="{INK}" stroke-width="5"/>')
    ex, ey = r * 0.40, cy - r * 0.02
    out.append(eyes(ex, ey, expr, r=r*0.2, iris=spec.get("iris", "#4A6E8A"), snake=spec.get("snake_eye", False), look=spec.get("look", 0)))
    out.append(brows(ex, ey, expr, shade(hairc, 0.75) if spec.get("hair_style") != "bald" else "#8a6a4a", thick=r*0.11))
    # burun
    out.append(f'<path d="M{-r*0.02},{cy+r*0.12} Q{r*0.14},{cy+r*0.3} {-r*0.04},{cy+r*0.36}" stroke="{shade(skin,0.62)}" stroke-width="4.5" fill="none" stroke-linecap="round"/>')
    # yanaklar
    if spec.get("blush", True):
        for sx in (-1, 1):
            out.append(f'<ellipse cx="{sx*r*0.6:.0f}" cy="{cy+r*0.33:.0f}" rx="{r*0.17:.0f}" ry="{r*0.09:.0f}" fill="#E07F6A" opacity="0.35"/>')
    bstyle = spec.get("beard", "none")
    my = cy + r * 0.62
    if bstyle not in ("none", "stubble"):
        out.append(beard_svg(bstyle, spec.get("beard_c", hairc), r, cy))
        out.append(mouth(my + r*0.02, expr))
    else:
        out.append(beard_svg(bstyle, spec.get("beard_c", hairc), r, cy))
        out.append(mouth(my, expr))
    if spec.get("scar"):
        out.append(f'<path d="M{-ex-r*0.1:.0f},{ey-r*0.45:.0f} l{r*0.22:.0f},{r*0.7:.0f}" stroke="#A8483E" stroke-width="5" stroke-linecap="round"/>')
    out.append(hair_front(spec.get("hair_style", "short"), hairc, r, cy))
    if spec.get("crown"):
        out.append(crown(0, cy - r*0.82, r/60*0.95, big=spec.get("crown_big", False)))
    if spec.get("circlet"):
        out.append(f'<path d="M{-r*0.98},{cy-r*0.45} Q0,{cy-r*0.72} {r*0.98},{cy-r*0.45}" stroke="#E2B23A" stroke-width="8" fill="none"/><circle cx="0" cy="{cy-r*0.6:.0f}" r="7" fill="#C0392B" stroke="{INK}" stroke-width="3"/>')
    if spec.get("helmet"):
        out.append(f'<path d="M{-r*1.04},{cy-r*0.25} Q{-r*1.0},{cy-r*1.2} 0,{cy-r*1.22} Q{r*1.0},{cy-r*1.2} {r*1.04},{cy-r*0.25} Z" fill="#8F9AA3" stroke="{INK}" stroke-width="5"/>'
                   f'<rect x="-7" y="{cy-r*0.4:.0f}" width="14" height="{r*0.62:.0f}" fill="#8F9AA3" stroke="{INK}" stroke-width="4"/>'
                   f'<path d="M{-r*0.5},{cy-r*0.95} Q0,{cy-r*1.1} {r*0.5},{cy-r*0.95}" stroke="#C8D0D6" stroke-width="6" fill="none"/>')
    return "".join(out)

def crown(x, y, s=1.0, big=False):
    k = 1.35 if big else 1.0
    return (f'<g transform="translate({x},{y}) scale({s*k:.3f}) rotate({8 if big else 0})"><path d="M-58,0 L-62,-48 L-32,-22 L0,-60 L32,-22 L62,-48 L58,0 Z" '
            f'fill="#E8B93A" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/><path d="M-58,0 L58,0 L56,10 L-56,10 Z" fill="#C99A2E" stroke="{INK}" stroke-width="4"/>'
            f'<circle cx="0" cy="-16" r="8" fill="#B8322A" stroke="{INK}" stroke-width="3"/><circle cx="-36" cy="-10" r="5" fill="#3E6FA8" stroke="{INK}" stroke-width="2.5"/><circle cx="36" cy="-10" r="5" fill="#3E6FA8" stroke="{INK}" stroke-width="2.5"/></g>')

def hand(x, y, r, skin, fist=False):
    return (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{skin}" stroke="{INK}" stroke-width="4"/>'
            + ("" if fist else f'<ellipse cx="{x - r*0.65:.1f}" cy="{y - r*0.35:.1f}" rx="{r*0.38:.1f}" ry="{r*0.5:.1f}" fill="{skin}" stroke="{INK}" stroke-width="3.5"/>'))

def fur_leg(x0, y0, x1, y1, w, color):
    """Kıllı pantolon bacağı: tırtıklı kontur + tutamlar."""
    ang = math.atan2(y1 - y0, x1 - x0); nx, ny = -math.sin(ang), math.cos(ang)
    L = math.hypot(x1 - x0, y1 - y0); n = int(L / 16)
    left, right = [], []
    for i in range(n + 1):
        t = i / n; cx, cy = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
        j = (7 if i % 2 else -2)
        left.append((cx + nx * (w/2 + j), cy + ny * (w/2 + j)))
        right.append((cx - nx * (w/2 + j), cy - ny * (w/2 + j)))
    pts = left + right[::-1]
    s = f'<polygon points="{P(*pts)}" fill="{color}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
    for i in range(1, n):
        t = i / n; cx, cy = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
        off = (i % 3 - 1) * w * 0.22
        s += f'<path d="M{cx + nx*off:.1f},{cy + ny*off:.1f} l{-4 + (i%2)*8},10" stroke="{shade(color,1.3)}" stroke-width="4" stroke-linecap="round"/>'
        s += f'<path d="M{cx - nx*(off+6):.1f},{cy - ny*(off+6):.1f} l{3},9" stroke="{shade(color,0.7)}" stroke-width="4" stroke-linecap="round"/>'
    return s

def character(spec, age="adult", pose="stand", expr="neutral", facing=1, props=(), stride=0, extra_front="", extra_back=""):
    """Ayak tabanı ortası (0,0). Döndürülen SVG <g>."""
    B = BODY[age]; skin = spec.get("skin", "#F0C49C"); SKIN_CUR[0] = skin
    r, hcy, shy, sx, hy = B["head_r"], B["head_cy"], B["shoulder_y"], B["sx"], B["hip_y"]
    tw, lw, aw = B["torso_w"], B["legw"], B["limbw"]
    tunic = spec.get("tunic", "#8E3B2E"); trim = spec.get("trim", "#E2B23A")
    pants = spec.get("pants", "#5B4636"); boots = spec.get("boots", "#4A3424")
    out = [f'<g transform="scale({facing},1)">']
    out.append(f'<ellipse cx="0" cy="4" rx="{tw*0.75:.0f}" ry="{tw*0.12:.0f}" fill="#000" opacity="0.18"/>')
    out.append(extra_back)
    if not spec.get("_nohead"): out.append(hair_back(spec.get("hair_style", "short"), spec.get("hair", "#C99A4E"), r, hcy))
    # pelerin
    cloak = spec.get("cloak")
    if cloak:
        cl = shade(cloak, 0.8)
        out.append(f'<path d="M{-sx-8},{shy-6} Q{-sx-48},{hy+20} {-sx-40},{-12} L{sx+40},{-12} Q{sx+48},{hy+20} {sx+8},{shy-6} Z" fill="{cloak}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>')
        out.append(f'<path d="M{sx+10},{shy+30} Q{sx+38},{hy+30} {sx+30},{-18}" stroke="{cl}" stroke-width="16" fill="none" opacity="0.8"/>')
    # bacaklar
    ang = pose_legs = stride
    if pose == "sit":
        kx = tw * 0.42
        for s_ in (-1, 1):
            out.append(limb([(s_*tw*0.22, hy+10), (s_*tw*0.22 + 6, hy + 10 + 4), (s_*tw*0.26, hy + B["leg"]*0.62)], lw, pants))
        lx = [(-tw*0.26, hy + B["leg"]*0.62), (tw*0.26, hy + B["leg"]*0.62)]
        foot_y = hy + B["leg"]*0.62
    else:
        feet = []
        for s_ in (-1, 1):
            a = s_ * (6 + stride)
            x0, y0 = s_ * tw * 0.2, hy + 6
            x1, y1 = polar(x0, y0, B["leg"] - 18, a)
            feet.append((x1, y1))
            if spec.get("hairy"):
                out.append(fur_leg(x0, y0, x1, y1 - 6, lw + 10, spec.get("fur", "#6B4A2E")))
            else:
                out.append(limb([(x0, y0), (x1, y1 - 4)], lw, pants))
            # çizme
            out.append(f'<path d="M{x1 - lw*0.55:.1f},{y1-22:.1f} L{x1 + lw*0.5:.1f},{y1-22:.1f} L{x1 + lw*0.55 + 14*s_*0 + 10:.1f},{y1:.1f} L{x1 - lw*0.6:.1f},{y1:.1f} Z" fill="{boots}" stroke="{INK}" stroke-width="4.5" stroke-linejoin="round"/>')
            if not spec.get("hairy"):
                out.append(f'<path d="M{x1 - lw*0.5:.1f},{y1-34:.1f} l{lw:.0f},-8 M{x1 - lw*0.5:.1f},{y1-48:.1f} l{lw:.0f},-8" stroke="{shade(pants,0.7)}" stroke-width="3"/>')
    # gövde (tunik)
    top = shy - 8; waist = hy + 4; hem = hy + (B["leg"] * (0.35 if spec.get("dress") else 0.2))
    if spec.get("dress"): hem = -14
    torso = (f'M{-tw/2+4},{top} Q{-tw/2-4},{(top+waist)/2} {-tw/2+2},{waist} L{-tw/2-10},{hem} '
             f'Q0,{hem+10} {tw/2+10},{hem} L{tw/2-2},{waist} Q{tw/2+4},{(top+waist)/2} {tw/2-4},{top} Q0,{top-10} {-tw/2+4},{top} Z')
    cid = uid("tc")
    out.append(f'<defs><clipPath id="{cid}"><path d="{torso}"/></clipPath></defs>')
    out.append(f'<path d="{torso}" fill="{tunic}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>')
    out.append(f'<g clip-path="url(#{cid})"><rect x="{tw*0.18:.0f}" y="{top-20}" width="{tw}" height="{hem-top+40}" fill="{shade(tunic,0.8)}"/>'
               f'<path d="M{-tw/2-12},{hem-8} Q0,{hem+2} {tw/2+12},{hem-8}" stroke="{trim}" stroke-width="10" fill="none"/>'
               f'<path d="M-14,{top} L0,{top+34} L14,{top}" stroke="{trim}" stroke-width="7" fill="none"/>'
               f'{spec.get("chest","")}</g>')
    out.append(f'<path d="{torso}" fill="none" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>')
    if spec.get("armor"):
        out.append(f'<path d="M{-tw/2+8},{top+16} L{tw/2-8},{top+16} L{tw/2-4},{waist-6} L{-tw/2+4},{waist-6} Z" fill="{spec["armor"]}" stroke="{INK}" stroke-width="4.5"/>'
                   + "".join(f'<path d="M{-tw/2+8},{top+16+k*18} L{tw/2-8},{top+16+k*18}" stroke="{shade(spec["armor"],0.75)}" stroke-width="3"/>' for k in range(1, 6)))
    # kemer
    out.append(f'<rect x="{-tw/2-2}" y="{waist-10}" width="{tw+4}" height="16" rx="3" fill="{spec.get("belt","#4A3020")}" stroke="{INK}" stroke-width="4"/>'
               f'<rect x="-11" y="{waist-13}" width="22" height="22" rx="4" fill="#D8A93A" stroke="{INK}" stroke-width="3.5"/>')
    # kürk yaka
    if spec.get("fur_collar"):
        fc = spec["fur_collar"]
        for i in range(9):
            t = i / 8; xx = -tw*0.62 + tw*1.24*t; yy = top - 4 + 8*math.sin(t*math.pi)
            out.append(f'<circle cx="{xx:.0f}" cy="{yy:.0f}" r="{tw*0.12:.0f}" fill="{fc}" stroke="{INK}" stroke-width="4"/>')
        for i in range(9):
            t = i / 8; xx = -tw*0.62 + tw*1.24*t; yy = top - 4 + 8*math.sin(t*math.pi)
            out.append(f'<circle cx="{xx-3:.0f}" cy="{yy-3:.0f}" r="{tw*0.06:.0f}" fill="{shade(fc,1.25)}"/>')
    # kollar
    tl, tr = POSES.get(pose, POSES["stand"])
    hands = []
    sleeve = spec.get("sleeve", tunic)
    Lr = B["au"] + B["al"]
    for s_, tg in ((-1, tl), (1, tr)):
        x0, y0 = s_ * (tw/2 - 10), shy + 10
        T = (x0 + s_ * tg[0] * Lr, y0 + tg[1] * Lr)
        c1 = ik((x0, y0), T, B["au"], B["al"], bend_out=True, side=s_)
        c2 = ik((x0, y0), T, B["au"], B["al"], bend_out=False, side=s_)
        if pose in ("arms_up", "wave", "one_up", "fist_up", "shrug", "hips"):
            pick = c1 if abs(c1[0][0]) >= abs(c2[0][0]) else c2
        else:
            pick = c1 if c1[0][1] >= c2[0][1] else c2
        (ex_, ey_), (hx, hy_) = pick
        out.append(limb([(x0, y0), (ex_, ey_), (hx, hy_)], aw, sleeve))
        if spec.get("armring") and s_ == 1:
            mx, my = (ex_ + hx) / 2, (ey_ + hy_) / 2
            out.append(f'<circle cx="{mx:.0f}" cy="{my:.0f}" r="{aw*0.62:.0f}" fill="none" stroke="#E2B23A" stroke-width="7"/>')
        hands.append((hx, hy_))
    # boyun + kafa
    out.append(f'<rect x="-{r*0.28:.0f}" y="{hcy + r*0.7:.0f}" width="{r*0.56:.0f}" height="{shy - hcy - r*0.6 + 6:.0f}" fill="{shade(skin,0.86)}" stroke="{INK}" stroke-width="4"/>')
    if not spec.get("_nohead"): out.append(head(spec, r, hcy, expr))
    else: out.append(spec.get("_head_svg", ""))
    # eldekiler
    for name in props:
        out.append(PROPS[name](hands, B, spec))
    hs = spec.get("hand_shape", ("open", "open"))
    for k_, (hx, hy_) in enumerate(hands):
        out.append(HAND3(hx, hy_, B["hand"], skin, hs[k_], -1 if k_ == 0 else 1) if "HAND3" in globals() and spec.get("_v3") else hand(hx, hy_, B["hand"], skin))
    out.append(extra_front)
    out.append('</g>')
    return "".join(out)

# ─────────── el aksesuarları (hands[0]=sol, hands[1]=sağ)
def _spear(h, B, spec, ang=-8, length=None):
    (lx, ly), (rx, ry) = h; L = length or B["leg"] * 2.4
    x0, y0 = rx - 10, ry + L * 0.25
    x1, y1 = rx + 30, ry - L * 0.75
    return (f'<path d="M{x0:.0f},{y0:.0f} L{x1:.0f},{y1:.0f}" stroke="{INK}" stroke-width="15" stroke-linecap="round"/>'
            f'<path d="M{x0:.0f},{y0:.0f} L{x1:.0f},{y1:.0f}" stroke="#8C5E34" stroke-width="7" stroke-linecap="round"/>'
            f'<g transform="translate({x1:.0f},{y1:.0f}) rotate({math.degrees(math.atan2(x1-x0, y0-y1)):.1f})"><path d="M0,-58 L14,-12 L6,6 L-6,6 L-14,-12 Z" fill="#C3CCD3" stroke="{INK}" stroke-width="4.5" stroke-linejoin="round"/><path d="M0,-50 L0,0" stroke="#fff" stroke-width="3" opacity="0.6"/></g>')

def _spear_thrust(h, B, spec):
    (lx, ly), (rx, ry) = h
    x0, y0 = rx - 160, ry + 10; x1, y1 = rx + 230, ry - 18
    return (f'<path d="M{x0:.0f},{y0:.0f} L{x1:.0f},{y1:.0f}" stroke="{INK}" stroke-width="15" stroke-linecap="round"/>'
            f'<path d="M{x0:.0f},{y0:.0f} L{x1:.0f},{y1:.0f}" stroke="#8C5E34" stroke-width="7" stroke-linecap="round"/>'
            f'<g transform="translate({x1:.0f},{y1:.0f}) rotate(86)"><path d="M0,-58 L14,-12 L6,6 L-6,6 L-14,-12 Z" fill="#C3CCD3" stroke="{INK}" stroke-width="4.5" stroke-linejoin="round"/></g>')

def _round_shield(h, B, spec, color=None, rim="#9AA4AC"):
    (lx, ly), _ = h; c = color or spec.get("shield", "#B8322A"); R = B["leg"] * 0.36
    return (f'<g transform="translate({lx - 6:.0f},{ly - 4:.0f})"><circle r="{R:.0f}" fill="{c}" stroke="{INK}" stroke-width="5"/>'
            f'<circle r="{R*0.86:.0f}" fill="none" stroke="{rim}" stroke-width="7"/>'
            f'<path d="M0,{-R*0.86:.0f} V{R*0.86:.0f} M{-R*0.86:.0f},0 H{R*0.86:.0f}" stroke="{shade(c,1.35)}" stroke-width="9"/>'
            f'<circle r="{R*0.2:.0f}" fill="#B9C2C9" stroke="{INK}" stroke-width="4"/><path d="M{-R*0.5:.0f},{-R*0.5:.0f} A{R*0.7:.0f},{R*0.7:.0f} 0 0 1 {R*0.3:.0f},{-R*0.62:.0f}" stroke="#fff" stroke-width="5" opacity="0.5" fill="none"/></g>')

def _sword(h, B, spec):
    _, (rx, ry) = h
    return (f'<g transform="translate({rx:.0f},{ry:.0f}) rotate(-25)"><rect x="-5" y="-170" width="10" height="160" rx="3" fill="#C3CCD3" stroke="{INK}" stroke-width="4"/>'
            f'<rect x="-22" y="-14" width="44" height="10" rx="3" fill="#8C6A2E" stroke="{INK}" stroke-width="4"/><rect x="-5" y="-4" width="10" height="28" fill="#5A3B22" stroke="{INK}" stroke-width="3.5"/></g>')

def _toy_sword(h, B, spec):
    _, (rx, ry) = h
    return (f'<g transform="translate({rx:.0f},{ry:.0f}) rotate(-35)"><rect x="-6" y="-92" width="12" height="86" rx="4" fill="#C49A62" stroke="{INK}" stroke-width="4"/>'
            f'<rect x="-18" y="-10" width="36" height="9" rx="3" fill="#8C6A3E" stroke="{INK}" stroke-width="3.5"/></g>')

def _cup(h, B, spec):
    _, (rx, ry) = h
    return f'<g transform="translate({rx+4:.0f},{ry-14:.0f})"><path d="M-16,-20 L16,-20 L12,14 L-12,14 Z" fill="#C9A15A" stroke="{INK}" stroke-width="4"/><ellipse cx="0" cy="-20" rx="16" ry="5" fill="#7A2E24" stroke="{INK}" stroke-width="3"/></g>'

def _onion(h, B, spec):
    _, (rx, ry) = h
    return f'<g transform="translate({rx+2:.0f},{ry-16:.0f})"><path d="M0,-18 Q16,0 0,16 Q-16,0 0,-18 Z" fill="#E9D7C0" stroke="{INK}" stroke-width="3.5"/><path d="M0,-18 l-3,-12 M0,-18 l4,-12" stroke="#6E9C4F" stroke-width="4"/></g>'

def _coin(h, B, spec):
    _, (rx, ry) = h
    return f'<circle cx="{rx+8:.0f}" cy="{ry-14:.0f}" r="13" fill="#E2B23A" stroke="{INK}" stroke-width="3.5"/><circle cx="{rx+8:.0f}" cy="{ry-14:.0f}" r="7" fill="none" stroke="#B88A2A" stroke-width="2.5"/>'

def _chess(h, B, spec):
    _, (rx, ry) = h
    return f'<g transform="translate({rx:.0f},{ry-12:.0f})"><path d="M-9,10 L9,10 L6,-6 Q10,-14 0,-20 Q-10,-14 -6,-6 Z" fill="#E9E1D0" stroke="{INK}" stroke-width="3.5"/><path d="M-6,4 l3,-3 M2,-2 l4,-4" stroke="#8A2A20" stroke-width="2.5"/></g>'

def _knife(h, B, spec):
    _, (rx, ry) = h
    return f'<g transform="translate({rx:.0f},{ry:.0f}) rotate(-60)"><path d="M-4,-6 L4,-6 L3,-54 L-2,-60 Z" fill="#C3CCD3" stroke="{INK}" stroke-width="3.5"/><rect x="-5" y="-6" width="10" height="26" rx="3" fill="#5A3B22" stroke="{INK}" stroke-width="3"/></g>'

def _scroll(h, B, spec):
    _, (rx, ry) = h
    return f'<g transform="translate({rx+10:.0f},{ry-30:.0f}) rotate(-12)"><rect x="-26" y="-40" width="52" height="80" fill="#EBD9AE" stroke="{INK}" stroke-width="4"/><rect x="-32" y="-46" width="64" height="12" rx="6" fill="#C9A86E" stroke="{INK}" stroke-width="4"/><rect x="-32" y="36" width="64" height="12" rx="6" fill="#C9A86E" stroke="{INK}" stroke-width="4"/></g>'

PROPS = dict(spear=_spear, thrust=_spear_thrust, shield=_round_shield, sword=_sword, toy_sword=_toy_sword, cup=_cup,
             onion=_onion, coin=_coin, chess=_chess, knife=_knife, scroll=_scroll)

# ═══════════════════════════════════════════ KARAKTER KADROSU
RAGNAR = dict(hair="#C99A4E", hair_style="tied", beard="braids", beard_c="#B9853F", tunic="#8E3B2E", trim="#E2B23A",
              cloak="#2F4C6E", fur_collar="#9A8F80", pants="#5B4636", iris="#4C7EA6", jaw=1.05, armring=True)
RAGNAR_LOD = dict(RAGNAR, hairy=True, fur="#6B4A2E")
RAGNAR_OLD = dict(RAGNAR_LOD, hair="#D9D3C7", beard_c="#E6E1D6", beard="white_long", iris="#4C7EA6")
RAGNAR_CHILD = dict(hair="#E2BE6A", hair_style="tousled", tunic="#3E6A8A", trim="#E2B23A", pants="#6A5240", iris="#4C7EA6")
RAGNAR_TEEN = dict(hair="#D9B060", hair_style="tousled", beard="stubble", beard_c="#C9A050", tunic="#3E6A8A", cloak="#7A2E2A",
                   fur_collar="#A89B88", iris="#4C7EA6", crown=True, crown_big=True)
SIGURD_HRING = dict(hair="#E9E4DA", hair_style="long", beard="white_long", beard_c="#F2EEE6", tunic="#6B2E3A", trim="#E2B23A",
                    cloak="#8A1F24", fur_collar="#C8BFAF", iris="#6A7F8E", circlet=True, armring=True)
LAGERTHA = dict(hair="#EFD37A", hair_style="flow", beard="none", tunic="#3B6B6B", trim="#C9D2D6", armor="#7F8C93",
                iris="#3E7A6E", skin="#F3CDA6", shield="#E9E4D6", jaw=0.9)
THORA = dict(hair="#B5532E", hair_style="braidcrown", tunic="#4E7A4A", trim="#E9D6A0", dress=True, iris="#5A7A3E", jaw=0.88, skin="#F6D3B0")
KRAKA = dict(hair="#2C2420", hair_style="ankle", tunic="#7A6A58", trim="#A8977E", dress=True, iris="#5A4A3E", jaw=0.88, skin="#F1CCA6")
ASLAUG = dict(KRAKA, tunic="#5B3A6E", trim="#E2B23A", circlet=True, cloak="#2E2A44")
HERRAUD = dict(hair="#8A6A4A", hair_style="short", beard="full", beard_c="#7A5A3A", tunic="#5B3A78", cloak="#3A2A5A", fur_collar="#B8A890", jaw=1.15, circlet=True)
IVAR = dict(hair="#2E2A26", hair_style="short", beard="stubble", beard_c="#2E2A26", tunic="#2F4A3A", iris="#5FA3C9", jaw=0.95)
BJORN = dict(hair="#8A6A42", hair_style="tied", beard="full", beard_c="#7A5A36", tunic="#4A4E56", armor="#9AA5AD", iris="#4C7EA6", jaw=1.1)
HVITSERK = dict(hair="#E3D3A8", hair_style="short", beard="short", beard_c="#D6C394", tunic="#ECE6D6", trim="#9A8F80", iris="#4C7EA6")
SIGURD_SNAKE = dict(hair="#B9853F", hair_style="short", beard="short", beard_c="#A9753A", tunic="#6E3A2E", iris="#5A8A4A", snake_eye=True)
CHARLES = dict(hair="#7A5A3A", hair_style="bald", beard="neat", beard_c="#6A4A2E", tunic="#2E4E8A", trim="#E2B23A", cloak="#3A5FA8",
               fur_collar="#EDE6D6", crown=True, jaw=1.0)
AELLA = dict(hair="#4E3A2A", hair_style="short", beard="neat", beard_c="#4E3A2A", tunic="#7A1E22", trim="#E2B23A", cloak="#5A1418",
             fur_collar="#CFC5B4", crown=True, iris="#6A7A8A", jaw=1.0)
SCHOLAR = dict(hair="#9A9088", hair_style="bald", beard="full", beard_c="#B8B0A8", tunic="#3A3A4A", trim="#8A8A9A", jaw=1.0)
WARRIOR = dict(hair="#6A4E36", hair_style="short", beard="full", beard_c="#5A4030", tunic="#5A4A3A", helmet=True)
WOMAN_WARRIOR = dict(hair="#C9A060", hair_style="long", tunic="#5A5048", armor="#7F8C93", helmet=True, jaw=0.9, skin="#F3CDA6")
SAXON = dict(hair="#5A4030", hair_style="short", beard="short", beard_c="#4A3020", tunic="#8A2A2A", helmet=True)
MONKISH = dict(hair="#6B4A30", hair_style="short", beard="none", tunic="#6E5844")
BAKER = dict(hair="#7A5A3A", hair_style="short", beard="full", beard_c="#6A4A2E", tunic="#7A6A4A", jaw=1.05)

# ═══════════════════════════════════════════ YARATIKLAR
def baby(expr="sleepy"):
    sk = "#F2CAA2"; SKIN_CUR[0] = sk
    s = (f'<path d="M-120,0 Q-130,-150 0,-170 Q130,-150 120,0 Q60,30 0,30 Q-60,30 -120,0 Z" fill="#9A8F80" stroke="{INK}" stroke-width="5"/>'
         + "".join(f'<circle cx="{-110+i*27}" cy="{-150+abs(i-4)*10}" r="18" fill="#B5AB9C" stroke="{INK}" stroke-width="4"/>' for i in range(9))
         + f'<path d="M-90,-10 Q-95,-110 0,-118 Q95,-110 90,-10 Z" fill="#C9B79A" stroke="{INK}" stroke-width="5"/>'
         + f'<path d="M-60,-40 Q0,-10 60,-40" stroke="#A8977E" stroke-width="5" fill="none"/>')
    s += f'<g transform="translate(0,-115)">' + head(dict(hair="#F0D79A", hair_style="none", skin=sk, blush=True), 62, 0, expr)
    s += f'<path d="M-6,-60 q6,-14 12,-4" stroke="{INK}" stroke-width="4" fill="#F0D79A"/></g>'
    return s

def bear():
    c = "#5E4330"; d = shade(c, 0.75)
    return (f'<path d="M-150,0 Q-170,-160 -60,-200 Q40,-230 120,-170 Q170,-120 150,0 Z" fill="{c}" stroke="{INK}" stroke-width="6"/>'
            f'<path d="M60,-150 Q150,-150 150,0 L100,0 Q110,-90 60,-120 Z" fill="{d}"/>'
            f'<circle cx="80" cy="-230" r="70" fill="{c}" stroke="{INK}" stroke-width="6"/>'
            f'<circle cx="40" cy="-290" r="22" fill="{c}" stroke="{INK}" stroke-width="5"/><circle cx="122" cy="-288" r="22" fill="{c}" stroke="{INK}" stroke-width="5"/>'
            f'<ellipse cx="96" cy="-210" rx="34" ry="24" fill="#B89070" stroke="{INK}" stroke-width="4"/><ellipse cx="104" cy="-220" rx="12" ry="8" fill="{INK}"/>'
            f'<circle cx="60" cy="-246" r="7" fill="{INK}"/><circle cx="108" cy="-250" r="7" fill="{INK}"/>'
            f'<path d="M48,-262 l20,6 M100,-266 l20,-4" stroke="{INK}" stroke-width="5"/>'
            f'<path d="M84,-196 Q96,-188 110,-196" stroke="{INK}" stroke-width="4" fill="#fff"/>')

def hound():
    c = "#8A7A68"
    return (f'<path d="M-110,-40 Q-100,-110 0,-110 Q80,-110 100,-70 L100,-40 Q40,-30 -110,-40 Z" fill="{c}" stroke="{INK}" stroke-width="5"/>'
            + "".join(f'<rect x="{x}" y="-50" width="20" height="50" rx="8" fill="{c}" stroke="{INK}" stroke-width="4.5"/>' for x in (-95, -60, 40, 74))
            + f'<path d="M-110,-90 Q-160,-120 -150,-150" stroke="{INK}" stroke-width="14" fill="none" stroke-linecap="round"/><path d="M-110,-90 Q-160,-120 -150,-150" stroke="{c}" stroke-width="6" fill="none" stroke-linecap="round"/>'
            f'<path d="M80,-100 Q90,-170 140,-170 Q190,-160 190,-130 Q170,-110 120,-100 Z" fill="{c}" stroke="{INK}" stroke-width="5"/>'
            f'<path d="M120,-168 l-14,-30 l26,16 Z" fill="{shade(c,0.8)}" stroke="{INK}" stroke-width="4"/><circle cx="150" cy="-148" r="6" fill="{INK}"/>'
            f'<path d="M168,-122 l14,6 l6,-8 Z" fill="#fff" stroke="{INK}" stroke-width="2.5"/><circle cx="188" cy="-136" r="7" fill="{INK}"/>')

def dog_small():
    c = "#B88A5A"
    return (f'<path d="M-60,-24 Q-60,-70 0,-70 Q50,-70 56,-40 L56,-24 Z" fill="{c}" stroke="{INK}" stroke-width="5"/>'
            + "".join(f'<rect x="{x}" y="-30" width="14" height="30" rx="6" fill="{c}" stroke="{INK}" stroke-width="4"/>' for x in (-52, -30, 22, 40))
            + f'<circle cx="64" cy="-78" r="30" fill="{c}" stroke="{INK}" stroke-width="5"/><path d="M48,-100 q-18,10 -12,40" fill="{shade(c,0.75)}" stroke="{INK}" stroke-width="4"/>'
            f'<circle cx="74" cy="-82" r="5" fill="{INK}"/><ellipse cx="92" cy="-72" rx="7" ry="5" fill="{INK}"/><path d="M-60,-50 q-20,-20 -10,-40" stroke="{INK}" stroke-width="10" fill="none" stroke-linecap="round"/><path d="M-60,-50 q-20,-20 -10,-40" stroke="{c}" stroke-width="4" fill="none" stroke-linecap="round"/>')

def serpent_body(points, w=60, c="#5E8A3A", belly="#C9D28A", spots=True):
    d = "M" + " ".join(f"{x:.0f},{y:.0f}" for x, y in points[:1]) + " " + " ".join(
        f"Q{points[i][0]:.0f},{points[i][1]:.0f} {(points[i][0]+points[i+1][0])/2:.0f},{(points[i][1]+points[i+1][1])/2:.0f}" for i in range(1, len(points)-1)) \
        + f" L{points[-1][0]:.0f},{points[-1][1]:.0f}"
    s = (f'<path d="{d}" stroke="{INK}" stroke-width="{w+12}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
         f'<path d="{d}" stroke="{c}" stroke-width="{w}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
         f'<path d="{d}" stroke="{belly}" stroke-width="{w*0.28:.0f}" fill="none" stroke-linecap="round" transform="translate(0,{w*0.22:.0f})" opacity="0.9"/>')
    if spots:
        s += f'<path d="{d}" stroke="{shade(c,0.7)}" stroke-width="{w*0.3:.0f}" fill="none" stroke-dasharray="{w*0.35:.0f} {w*0.9:.0f}" stroke-linecap="round" transform="translate(0,{-w*0.12:.0f})"/>'
    return s

def serpent_head(x, y, s=1.0, rot=0, c="#5E8A3A", mouth_open=False, cute=False):
    jaw = (f'<path d="M10,20 Q80,40 120,10 L110,30 Q60,60 0,40 Z" fill="{shade(c,0.85)}" stroke="{INK}" stroke-width="5"/>'
           f'<path d="M30,26 l8,14 l6,-12 M70,28 l8,14 l6,-12" fill="#fff" stroke="{INK}" stroke-width="2.5"/>' if mouth_open else "")
    eye_r = 22 if cute else 13
    return (f'<g transform="translate({x},{y}) rotate({rot}) scale({s})">{jaw}'
            f'<path d="M-40,0 Q-40,-50 20,-56 Q100,-58 130,-10 Q120,{10 if not mouth_open else -4} 60,{14 if not mouth_open else 4} Q0,24 -40,0 Z" fill="{c}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
            f'<path d="M0,-40 Q60,-50 110,-24" stroke="{shade(c,1.3)}" stroke-width="7" fill="none" stroke-linecap="round"/>'
            f'<circle cx="40" cy="-26" r="{eye_r}" fill="#F2E35B" stroke="{INK}" stroke-width="4"/>'
            f'<ellipse cx="{44 if not cute else 42}" cy="-26" rx="{4 if not cute else 9}" ry="{eye_r*0.75:.0f}" fill="{INK}"/>'
            + (f'<circle cx="36" cy="-32" r="5" fill="#fff"/>' if cute else
               f'<path d="M22,-46 L60,-36" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>')
            + f'<circle cx="118" cy="-16" r="3" fill="{INK}"/>'
            + (f'<path d="M126,-6 l26,4 l6,-8 M152,-2 l8,6" stroke="#C0392B" stroke-width="4" fill="none" stroke-linecap="round"/>' if not cute else "")
            + '</g>')

def ox_hide(w=360, h=260, c="#B07A4A"):
    return (f'<path d="M{-w/2},{-h/2+30} Q{-w/2-30},0 {-w/2},{h/2-20} Q0,{h/2+20} {w/2},{h/2-30} Q{w/2+40},0 {w/2},{-h/2+20} Q0,{-h/2-30} {-w/2},{-h/2+30} Z" '
            f'fill="{c}" stroke="{INK}" stroke-width="6"/>'
            + "".join(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{shade(c,0.7)}" opacity="0.6"/>' for x, y, rx, ry in ((-60, -30, 50, 30), (70, 40, 40, 26), (20, -70, 30, 18))))
