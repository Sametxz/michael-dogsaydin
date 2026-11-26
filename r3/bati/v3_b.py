"""Bölüm I · v3 · ajan B: manzara / kuruluş kareleri f1, f3, f4 (BRIEF_bolum1_v3).
python3 v3_b.py [f1 f3 f4] → bati/v3/<id>.png (+ <id>_crop1/2.png, R13 kırpmaları)
Ortak dosyalara yazılmaz; yalnızca kareler6 içe aktarılır.
"""
import sys, math, random
sys.path.insert(0, "/home/claude/r3/bati")
from kareler6 import *
from fx import light_shaft, fog, gradient_grade, grade
import tex

OUTV = "/home/claude/r3/bati/v3"
R = random.Random

# ======================================================================= ortak defs
def DEFS():
    return (O7.defs() + "<defs>" + tex.scaled("ahsap", 0.8)[0] + tex.scaled("kurk", 0.5)[0] + tex.scaled("kurk", 0.3)[0] + tex.scaled("tas", 0.6)[0]
            + tex.scaled("ahsap", 0.5)[0] + tex.scaled("deri", 0.5)[0]
            + "".join(f'<filter id="b{k}" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="{k}"/></filter>' for k in (1, 2, 3, 4, 6, 8, 12, 18, 28))
            # genel yüzey gürültüsü (koyu benek) ve açık benek: kırpılmış dikdörtgenlere uygulanır
            + '<filter id="nz_d" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="0.012 0.03" numOctaves="4" seed="8"/>'
              '<feColorMatrix type="matrix" values="0 0 0 0 0.08  0 0 0 0 0.07  0 0 0 0 0.06  0 0 0 -2.4 1.3"/></filter>'
            + '<filter id="nz_l" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="0.02 0.06" numOctaves="3" seed="19"/>'
              '<feColorMatrix type="matrix" values="0 0 0 0 0.85  0 0 0 0 0.88  0 0 0 0 0.9  0 0 0 -2.8 1.2"/></filter>'
            + '<filter id="nz_f" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="0.4" numOctaves="2" seed="5"/>'
              '<feColorMatrix type="matrix" values="0 0 0 0 0.1  0 0 0 0 0.09  0 0 0 0 0.08  0 0 0 -1.6 0.85"/></filter>'
            + '<filter id="nz_sky" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="0.004 0.012" numOctaves="4" seed="31"/>'
              '<feColorMatrix type="matrix" values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 -2.2 1.05"/></filter>'
            + "</defs>")

def clipped(cid, shape_d, inner):
    return f'<clipPath id="{cid}"><path d="{shape_d}"/></clipPath><g clip-path="url(#{cid})">{inner}</g>'

def P(pts): return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)

def smooth(pts, closed=False):
    """Catmull-Rom → kübik Bezier (yumuşak organik kontur)."""
    n = len(pts); o = [f"M{pts[0][0]:.1f},{pts[0][1]:.1f}"]
    rng = range(n) if closed else range(n - 1)
    for i in rng:
        p0 = pts[(i - 1) % n] if (closed or i > 0) else pts[i]
        p1 = pts[i]; p2 = pts[(i + 1) % n]
        p3 = pts[(i + 2) % n] if (closed or i + 2 < n) else pts[(i + 1) % n]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        o.append(f"C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}")
    return " ".join(o) + (" Z" if closed else "")

# ======================================================================= gökyüzü ve bulut
def cloud(cx, cy, w, h, seed, base, lit, dark, light=(-1, -1), blur=3, rim=None, flat=0.28, a=1.0):
    """Hacimli bulut kütlesi v2: düzensiz boyutlu kabarcık öbekleri (sıra hâlinde değil), dikey değer gradyanı
    (ışık üstte, koyu taban), güneşe bakan kenarda ince sıcak rim, altta parçalı yırtık kenar."""
    r = R(seed); cs = []
    n = max(8, int(w / 34))
    for i in range(n):
        t = r.uniform(0, 1); prof = math.sin(math.pi * (0.05 + 0.9 * t)) ** 1.2
        rad = (h * 0.16 + h * 0.5 * prof) * r.uniform(0.55, 1.15)
        cs.append((cx - w / 2 + w * t, cy - h * 0.55 * prof * r.uniform(0.4, 1.0) + rad * 0.25, rad))
    for i in range(n // 3):   # tepe kümeleri
        t = r.uniform(0.25, 0.75); rad = h * r.uniform(0.22, 0.42)
        cs.append((cx - w / 2 + w * t, cy - h * 0.6 * math.sin(math.pi * t) - rad * 0.1, rad))
    cs.sort(key=lambda q: -q[2])
    cid = f"cl{seed}"; bottom = cy + h * flat
    circ = lambda dx, dy, k, col: "".join(f'<circle cx="{x+dx:.0f}" cy="{y+dy:.0f}" r="{rr*k:.0f}" fill="{col}"/>' for x, y, rr in cs)
    lx, ly = light; top = cy - h * 1.2
    tear = " ".join(f"L{cx - w/2 + w*i/14:.0f},{bottom + (r.uniform(-h*0.25, h*0.12) if 0 < i < 14 else 0):.0f}" for i in range(15))
    clipd = f"M{cx-w:.0f},{top-h:.0f} L{cx+w:.0f},{top-h:.0f} L{cx+w:.0f},{bottom:.0f} " + " ".join(reversed(tear.split(" "))).replace("L", "L") + f" L{cx-w:.0f},{bottom:.0f} Z"
    gid = f"cg{seed}"; sh_ = min(h * 0.075, 11); sx_, sy_ = -lx * sh_, -ly * sh_     # gövde, ışığın tersine kaydırılır → ışık tarafında rim hilali kalır
    o = [f'<defs><linearGradient id="{gid}" x1="0" y1="{top:.0f}" x2="0" y2="{bottom:.0f}" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="{lit}"/><stop offset="0.5" stop-color="{base}"/><stop offset="1" stop-color="{dark}"/></linearGradient></defs>',
         f'<g filter="url(#b{blur})" opacity="{a}"><clipPath id="{cid}"><path d="{clipd}"/></clipPath><g clip-path="url(#{cid})">',
         circ(0, 0, 1, rim or lit),
         f'<clipPath id="{cid}s">{circ(sx_, sy_, 1, "#000")}</clipPath><g clip-path="url(#{cid}s)">',
         circ(sx_, sy_, 1, f"url(#{gid})"),
         '<g filter="url(#b12)">' + "".join(f'<circle cx="{x+sx_-lx*rr*0.25:.0f}" cy="{y+sy_+rr*0.45:.0f}" r="{rr*0.8:.0f}" fill="{dark}" opacity="0.35"/>' for x, y, rr in cs[len(cs)//3:]) + '</g>',
         '</g></g></g>']
    return "".join(o)

def stratus(y, seed, col_top, col_bot, n=6, thick=60, a=0.9, blur=4, x0=-200, x1=2120):
    """Alçak katman bulutu: uzun yatay şeritler; üst kenar açık, alt kenar koyu ve yırtık (yağmur saçağı)."""
    r = R(seed); o = []
    for i in range(n):
        cx = r.uniform(x0, x1); w = r.uniform(500, 1100); hh = thick * r.uniform(0.6, 1.3); yy = y + r.uniform(-thick, thick)
        top = " ".join(f"Q{cx - w/2 + w*(k+0.5)/8:.0f},{yy - hh*0.5 - r.uniform(0, hh*0.6):.0f} {cx - w/2 + w*(k+1)/8:.0f},{yy - hh*0.4 + r.uniform(-6, 6):.0f}" for k in range(8))
        bot = " ".join(f"L{cx + w/2 - w*(k+1)/10:.0f},{yy + hh*0.3 + r.uniform(-4, 14):.0f}" for k in range(10))
        d = f"M{cx-w/2:.0f},{yy:.0f} {top} L{cx+w/2:.0f},{yy:.0f} {bot} Z"
        gid = f"st{seed}_{i}"
        o.append(f'<defs><linearGradient id="{gid}" x1="0" y1="{yy-hh:.0f}" x2="0" y2="{yy+hh*0.4:.0f}" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="{col_top}"/><stop offset="1" stop-color="{col_bot}"/></linearGradient></defs>'
                 f'<path d="{d}" fill="url(#{gid})" opacity="{a}"/>')
    return f'<g filter="url(#b{blur})">{"".join(o)}</g>'

def sky_grad(gid, stops):
    return (f'<defs><linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1">'
            + "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops) + '</linearGradient></defs>')

# ======================================================================= dağ, orman
def ridge(x0, x1, ctrl, seed, rough=0.22, depth=7):
    """Kontrol noktalarından orta-nokta kaydırmalı sırt çizgisi."""
    r = R(seed); pts = list(ctrl)
    for _ in range(depth):
        new = [pts[0]]
        for (ax, ay), (bx, by) in zip(pts, pts[1:]):
            d = abs(bx - ax); new += [((ax + bx) / 2 + r.uniform(-d * 0.08, d * 0.08), (ay + by) / 2 + r.uniform(-d * rough, d * rough) * 0.5), (bx, by)]
        pts = new
    return pts

def mountain(ctrl, base, seed, col, shade_c, snow_c="#E8EEF4", snow_sh="#9AAABC", snowline=None, strata="#000", rough=0.22, outline=None, sw=3):
    pts = ridge(ctrl[0][0], ctrl[-1][0], ctrl, seed, rough)
    body = P(pts) + f" L{pts[-1][0]:.0f},{base} L{pts[0][0]:.0f},{base} Z"
    cid = f"mt{seed}"; r = R(seed + 1)
    o = [f'<path d="{body}" fill="{col}"/>', f'<clipPath id="{cid}"><path d="{body}"/></clipPath><g clip-path="url(#{cid})">']
    # yüzey: düşük frekans leke + kaya damarları (ışık sol üstten → sağa bakan yüzler gölgede)
    o.append(f'<rect x="{pts[0][0]}" y="{min(p[1] for p in pts)-10:.0f}" width="{pts[-1][0]-pts[0][0]}" height="{base}" filter="url(#nz_d)" opacity="0.5"/>')
    # büyük yüz gölgeleri: her kontrol tepesinden sağ vadiye uzanan yüz gölgede (ışık sol üst); sırt çizgisi zikzak
    def near_i(x): return min(range(len(pts)), key=lambda i: abs(pts[i][0] - x))
    faces = []
    for k in range(1, len(ctrl) - 1):
        (px, py), (vx, vy) = ctrl[k], ctrl[k + 1]
        if not (py < ctrl[k - 1][1] and py < vy): continue
        i0, i1 = near_i(px), near_i(vx)
        drop = base - py; spur = []
        for q in range(9):
            u = q / 8; spur.append((px + drop * 0.28 * u + r.uniform(-14, 14) * (0 < q < 8), py + drop * u))
        face = pts[i0:i1 + 1] + [(vx + (base - vy) * 0.45, base)] + list(reversed(spur))
        o.append(f'<path d="{P(face)} Z" fill="{shade_c}" opacity="0.88"/>'); faces.append(P(face) + " Z")
        for g in range(4):   # yüz içinde ikincil sırtlar (açık) ve oluklar (koyu)
            u = r.uniform(0.25, 0.85); gx, gy = px + (vx - px) * u, py + (vy - py) * u + 6
            L = (base - gy) * r.uniform(0.3, 0.7)
            o.append(f'<path d="M{gx:.0f},{gy:.0f} q{L*0.12:.0f},{L*0.5:.0f} {L*0.3:.0f},{L:.0f}" stroke="{col}" stroke-width="{r.uniform(2,5):.1f}" fill="none" opacity="0.35"/>')
    if snowline is not None:
        sp = []; ph = r.uniform(0, 6)
        for i, (x, y) in enumerate(pts):
            d = max(0.0, snowline - y)
            wav = 0.55 + 0.3 * math.sin(x / 41 + ph) + 0.15 * math.sin(x / 13 + ph * 2)
            tongue = 22 * max(0.0, math.sin(x / 31 + ph)) ** 6 if d > 30 else 0      # oluklara inen kar dilleri
            sp.append((x, y + d * wav + tongue))
        snow = P(pts) + " " + smooth(list(reversed(sp))).replace("M", "L", 1) + " Z"
        o.append(f'<path d="{snow}" fill="{snow_c}"/>')
        o.append(f'<clipPath id="{cid}sn"><path d="{snow}"/></clipPath><g clip-path="url(#{cid}sn)">' + "".join(f'<path d="{fd}" fill="{snow_sh}"/>' for fd in faces) + '</g>')
    for k in range(int((pts[-1][0] - pts[0][0]) / 45)):   # yamaç eğimini izleyen kaya damarları (çapraz, seyrek)
        i = r.randrange(1, len(pts) - 1); x, yt = pts[i]
        sl = 1 if pts[i + 1][1] > pts[i - 1][1] else -1
        y0 = yt + r.uniform(20, 140); L = r.uniform(40, 140)
        o.append(f'<path d="M{x:.0f},{y0:.0f} q{sl*L*0.25:.0f},{L*0.5:.0f} {sl*L*0.55:.0f},{L:.0f}" stroke="{strata}" stroke-width="{r.uniform(1.5,3):.1f}" fill="none" opacity="0.1"/>')
    o.append('</g>')
    if outline: o.append(f'<path d="{P(pts)}" stroke="{outline}" stroke-width="{sw}" fill="none" stroke-linejoin="round" opacity="0.8"/>')
    return "".join(o), pts

def spruce(x, y, h, seed, col="#24382C", lit="#4E6A4A", dark="#14221A", ink=None, snow=0.0, sw=3):
    """Ladin: katmanlı sarkık dallar, ışık tarafı (sol) açık, sağ ve alt kenar koyu; gövde zemine girer."""
    r = R(seed); w = h * 0.36; o = []
    o.append(f'<path d="M{x-h*0.02:.1f},{y+2} L{x-h*0.012:.1f},{y-h*0.3:.1f} L{x+h*0.012:.1f},{y-h*0.3:.1f} L{x+h*0.022:.1f},{y+2} Z" fill="#2E2218"/>')
    tiers = int(7 + h / 40)
    for k in range(tiers):
        t = k / tiers; ty = y - h * 0.12 - (h * 0.86) * t; tw = w * (1 - t) ** 0.95 * r.uniform(0.85, 1.1) + h * 0.02
        th = h * 0.86 / tiers * 1.9
        left = (x - tw, ty + th * 0.18); right = (x + tw * r.uniform(0.85, 1.05), ty + th * 0.12)
        teeth = []
        nT = 5 + int(tw / 12)
        for i in range(nT + 1):
            u = i / nT; xx = right[0] + (left[0] - right[0]) * u
            teeth.append((xx, ty + th * 0.15 + (r.uniform(0, th * 0.22) if i % 2 else -th * 0.05)))
        d = f"M{x:.1f},{ty-th:.1f} Q{x+tw*0.45:.1f},{ty-th*0.55:.1f} {right[0]:.1f},{right[1]:.1f} " + " ".join(f"L{a:.1f},{b:.1f}" for a, b in teeth) + f" Q{x-tw*0.45:.1f},{ty-th*0.55:.1f} {x:.1f},{ty-th:.1f} Z"
        o.append(f'<path d="{d}" fill="{col}"' + (f' stroke="{ink}" stroke-width="{sw}" stroke-linejoin="round"' if ink else "") + '/>')
        o.append(f'<path d="M{x:.1f},{ty-th:.1f} Q{x-tw*0.45:.1f},{ty-th*0.55:.1f} {left[0]:.1f},{left[1]:.1f} L{x-tw*0.3:.1f},{ty+th*0.02:.1f} Q{x-tw*0.15:.1f},{ty-th*0.5:.1f} {x:.1f},{ty-th*0.85:.1f} Z" fill="{lit}" opacity="0.75"/>')
        o.append(f'<path d="M{right[0]:.1f},{right[1]:.1f} ' + " ".join(f"L{a:.1f},{b:.1f}" for a, b in teeth[:nT // 2 + 1]) + f'" stroke="{dark}" stroke-width="{max(1.5, h/90):.1f}" fill="none" opacity="0.8"/>')
        if snow and k % 2 == 0:
            o.append(f'<path d="M{x-tw*0.7:.1f},{ty-th*0.25:.1f} Q{x-tw*0.3:.1f},{ty-th*0.75:.1f} {x:.1f},{ty-th*0.9:.1f} Q{x-tw*0.1:.1f},{ty-th*0.55:.1f} {x-tw*0.65:.1f},{ty-th*0.12:.1f} Z" fill="#E8EEF2" opacity="{snow}"/>')
    return "".join(o)

def forest(x0, x1, yfn, hmin, hmax, n, seed, **kw):
    r = R(seed); items = []
    for k in range(n):
        x = r.uniform(x0, x1); items.append((yfn(x) + r.uniform(-6, 10), x, r.uniform(hmin, hmax), k))
    items.sort()
    return "".join(spruce(x, y, h, seed * 100 + k, **kw) for y, x, h, k in items)

def birch(x, y, h, seed, dead=True, lean=0.0, broken=True, sc=1.0, ink=INK):
    """Ölü huş: beyaz gövde, siyah yatay lentiseller, kırık tepe, çıplak dallar (ışık solda)."""
    r = R(seed); o = []
    w0 = h * 0.055 * sc; top = (x + lean * h, y - h)
    trunk = f"M{x-w0:.1f},{y+3} Q{x-w0*0.9+lean*h*0.4:.1f},{y-h*0.5:.1f} {top[0]-w0*0.45:.1f},{top[1]:.1f} L{top[0]+w0*0.1:.1f},{top[1]-h*0.03:.1f} L{top[0]+w0*0.5:.1f},{top[1]+h*0.02:.1f} Q{x+w0*0.9+lean*h*0.4:.1f},{y-h*0.5:.1f} {x+w0:.1f},{y+3} Z"
    # dallar (gövdeden önce, arkada kalanlar)
    for k in range(int(5 + h / 70)):
        t = r.uniform(0.35, 0.92); bx = x + lean * h * t; by = y - h * t; side = r.choice((-1, 1)); L = h * r.uniform(0.12, 0.3) * (1.2 - t)
        ang = math.radians(r.uniform(-70, -25)) if side > 0 else math.radians(r.uniform(-155, -110))
        ex_, ey_ = bx + L * math.cos(ang), by + L * math.sin(ang)
        bw = max(2.0, w0 * 0.35 * (1.1 - t))
        o.append(f'<path d="M{bx:.1f},{by:.1f} Q{(bx+ex_)/2+side*6:.1f},{(by+ey_)/2+4:.1f} {ex_:.1f},{ey_:.1f}" stroke="{ink}" stroke-width="{bw+3:.1f}" fill="none" stroke-linecap="round"/>'
                 f'<path d="M{bx:.1f},{by:.1f} Q{(bx+ex_)/2+side*6:.1f},{(by+ey_)/2+4:.1f} {ex_:.1f},{ey_:.1f}" stroke="#6A625A" stroke-width="{bw:.1f}" fill="none" stroke-linecap="round"/>')
        for j in range(3):   # ince sürgün
            u = r.uniform(0.4, 1.0); sx_, sy_ = bx + (ex_ - bx) * u, by + (ey_ - by) * u
            a2 = ang + r.uniform(-0.7, 0.7); l2 = L * r.uniform(0.2, 0.45)
            o.append(f'<path d="M{sx_:.1f},{sy_:.1f} l{l2*math.cos(a2):.1f},{l2*math.sin(a2):.1f}" stroke="#3A342E" stroke-width="{max(1.2,bw*0.45):.1f}" stroke-linecap="round"/>')
    o.append(f'<path d="{trunk}" fill="#D8D4C8" stroke="{ink}" stroke-width="{max(2.5, w0*0.22):.1f}" stroke-linejoin="round"/>')
    cid = f"bi{seed}"
    inner = (f'<rect x="{x-w0*3+min(0,lean*h)}" y="{top[1]-10:.0f}" width="{w0*6+abs(lean*h)}" height="{h+20}" fill="#000" opacity="0"/>'
             f'<path d="M{x+w0*0.2:.1f},{y} Q{x+w0*0.3+lean*h*0.4:.1f},{y-h*0.5:.1f} {top[0]+w0*0.2:.1f},{top[1]:.1f} L{top[0]+w0*1.2:.1f},{top[1]:.1f} L{x+w0*1.4+lean*h:.1f},{y} Z" fill="#7E8088" opacity="0.55"/>'
             f'<rect x="{x-w0*3+min(0,lean*h)}" y="{top[1]-10:.0f}" width="{w0*6+abs(lean*h)}" height="{h+20}" filter="url(#nz_d)" opacity="0.35"/>')
    for k in range(int(h / 16)):   # lentiseller: kısa, ince, düzensiz yatay çizikler (bir kenardan başlar)
        t = r.uniform(0.02, 0.98); cx = x + lean * h * t * 0.9; cy = y - h * t; ww = w0 * r.uniform(0.25, 0.8)
        st = cx + r.choice((-1, 1)) * w0 * r.uniform(0.3, 1.0) - ww / 2
        inner += f'<path d="M{st:.1f},{cy:.1f} q{ww/2:.1f},{r.uniform(-1.5,1.5):.1f} {ww:.1f},{r.uniform(-1,1):.1f}" stroke="#2A2622" stroke-width="{r.uniform(1.0, 2.0)*max(1,w0/14):.1f}" fill="none" stroke-linecap="round" opacity="0.85"/>'
    for k in range(int(h / 120) + 1):   # dal izi: koyu üçgen "göz" (chevron)
        t = r.uniform(0.25, 0.85); cx = x + lean * h * t + r.uniform(-w0 * 0.3, w0 * 0.3); cy = y - h * t
        inner += f'<path d="M{cx-w0*0.6:.1f},{cy-w0*0.2:.1f} Q{cx:.1f},{cy-w0*0.6:.1f} {cx+w0*0.6:.1f},{cy-w0*0.2:.1f} Q{cx:.1f},{cy+w0*0.15:.1f} {cx-w0*0.6:.1f},{cy-w0*0.2:.1f} Z" fill="#24201C" opacity="0.85"/>'
    o.append(clipped(cid, trunk, inner))
    o.append(f'<path d="M{top[0]-w0*0.45:.1f},{top[1]:.1f} L{top[0]-w0*0.1:.1f},{top[1]-h*0.05:.1f} L{top[0]+w0*0.15:.1f},{top[1]-h*0.01:.1f} L{top[0]+w0*0.35:.1f},{top[1]-h*0.045:.1f} L{top[0]+w0*0.5:.1f},{top[1]+h*0.02:.1f}" fill="#B8A88A" stroke="{ink}" stroke-width="{max(2,w0*0.18):.1f}" stroke-linejoin="round"/>')   # kırık uç
    o.append(f'<ellipse cx="{x+w0*0.6:.1f}" cy="{y+3:.1f}" rx="{w0*2.2:.1f}" ry="{w0*0.45:.1f}" fill="#000" opacity="0.3"/>')
    return "".join(o)

# ======================================================================= hayvanlar
def leg(pts, ws, col, hoof="#1E1A16", hw=None, ink=INK, cloven=True):
    """Eklemli bacak: her segment kendi kalınlığında, mürekkep alt katman; ucunda (çatal) toynak."""
    o = []
    for (x0, y0), (x1, y1), w in zip(pts, pts[1:], ws):
        o.append(f'<path d="M{x0},{y0} L{x1},{y1}" stroke="{ink}" stroke-width="{w+7}" stroke-linecap="round"/>')
    for (x0, y0), (x1, y1), w in zip(pts, pts[1:], ws):
        o.append(f'<path d="M{x0},{y0} L{x1},{y1}" stroke="{col}" stroke-width="{w}" stroke-linecap="round"/>')
    for (x0, y0) in pts[1:-1]:   # eklem şişliği
        o.append(f'<circle cx="{x0}" cy="{y0}" r="{ws[0]*0.36:.1f}" fill="{col}"/>')
    hx, hy = pts[-1]; hw = hw or ws[-1] * 1.25
    o.append(f'<path d="M{hx-hw*0.55:.1f},{hy-hw*0.75:.1f} L{hx+hw*0.45:.1f},{hy-hw*0.75:.1f} L{hx+hw*0.85:.1f},{hy} L{hx-hw*0.6:.1f},{hy} Z" fill="{hoof}" stroke="{ink}" stroke-width="3.5" stroke-linejoin="round"/>')
    if cloven: o.append(f'<path d="M{hx+hw*0.12:.1f},{hy-hw*0.5:.1f} L{hx+hw*0.2:.1f},{hy}" stroke="{ink}" stroke-width="2.5"/>')
    return "".join(o)

def oleg(pts, ws, col, hoof="#1E1A16", ink=INK, sw=4, cloven=True, bumps=()):
    """Organik bacak: eklem noktalarından tek parça, incelen dış hat (Catmull-Rom); bumps: eklemde öne/arkaya kemik çıkıntısı (i, taraf, büyüklük)."""
    n = len(pts); L, Rr = [], []
    for i, (x, y) in enumerate(pts):
        if i == 0: dx, dy = pts[1][0] - x, pts[1][1] - y
        elif i == n - 1: dx, dy = x - pts[i - 1][0], y - pts[i - 1][1]
        else: dx, dy = pts[i + 1][0] - pts[i - 1][0], pts[i + 1][1] - pts[i - 1][1]
        m = math.hypot(dx, dy) or 1; nx, ny = -dy / m, dx / m; w = ws[i] / 2
        bl = br = 0
        for (bi, side, k) in bumps:
            if bi == i: bl, br = (k, 0) if side > 0 else (0, k)
        L.append((x + nx * (w + bl), y + ny * (w + bl))); Rr.append((x - nx * (w + br), y - ny * (w + br)))
    d = smooth(L) + " L" + smooth(list(reversed(Rr)))[1:] + " Z"
    hx, hy = pts[-1]; hw = ws[-1] * 1.15
    o = [f'<path d="{d}" fill="{col}" stroke="{ink}" stroke-width="{sw}" stroke-linejoin="round"/>',
         f'<path d="M{hx-hw*0.6:.1f},{hy-hw*0.8:.1f} L{hx+hw*0.45:.1f},{hy-hw*0.8:.1f} L{hx+hw*0.9:.1f},{hy} L{hx-hw*0.65:.1f},{hy} Z" fill="{hoof}" stroke="{ink}" stroke-width="{sw*0.85:.1f}" stroke-linejoin="round"/>']
    if cloven: o.append(f'<path d="M{hx+hw*0.12:.1f},{hy-hw*0.5:.1f} L{hx+hw*0.2:.1f},{hy}" stroke="{ink}" stroke-width="{sw*0.6:.1f}"/>')
    return "".join(o)

def ox(x, y, s=1.0, col="#7A4A2C", dark="#4A2C1A", light="#A8744A", muzzle="#C8B49A", yoke=True, mud="#3A3024"):
    """Öküz, profil, sağa bakar, başı çekişte hafif aşağıda. Yerel zemin y=0. Kas ve kemik noktaları: cidago hörgücü,
    kalça kemiği, döş sarkığı (gerdan), dirsek, diz, topuk (arkaya), çatal toynak. Kısa öne kıvrık boynuz."""
    o = [f'<g transform="translate({x},{y}) scale({s})">',
         f'<ellipse cx="-20" cy="4" rx="300" ry="26" fill="#000" opacity="0.35" filter="url(#b6)"/>']
    far = dark
    o.append(leg([(78, -150), (92, -66), (86, -22), (82, 0)], [40, 24, 21], far, ink=INK))           # uzak ön (geride adım)
    o.append(leg([(-178, -170), (-228, -92), (-236, -24), (-240, 0)], [46, 25, 21], far, ink=INK))     # uzak arka
    body = ("M-250,-300 C-200,-318 0,-312 60,-318 C96,-326 120,-348 146,-340 C178,-330 206,-312 228,-298 "
            "C240,-302 254,-298 262,-286 C278,-262 296,-226 308,-200 C314,-188 320,-178 322,-166 C324,-150 318,-138 304,-136 "
            "C292,-134 282,-140 274,-146 C262,-156 248,-170 238,-182 C226,-196 214,-200 204,-196 "
            "C196,-170 192,-140 180,-118 C172,-106 160,-104 150,-110 L148,-100 C146,-84 142,-72 140,-62 L104,-64 "
            "C104,-98 100,-118 92,-130 C40,-124 -60,-124 -140,-138 C-160,-142 -176,-156 -182,-172 "
            "C-188,-140 -196,-112 -198,-88 L-236,-82 C-240,-130 -262,-196 -266,-248 C-268,-276 -264,-294 -250,-300 Z")
    o.append(f'<g filter="url(#f_form)"><path d="{body}" fill="{col}" {O7.T("kurk", 0.5)}/></g>')
    cid = f"ox{int(x)}"
    inner = (f'<path d="M-270,-200 C-150,-150 20,-140 160,-150 L200,-90 L-280,-60 Z" fill="{dark}" opacity="0.55"/>'           # gövde alt gölgesi
             f'<path d="M-250,-300 C-200,-322 0,-314 60,-320 C92,-326 116,-346 142,-338 L150,-300 C60,-290 -100,-290 -250,-280 Z" fill="{light}" opacity="0.55"/>'   # sırt ışığı
             f'<path d="M150,-338 C190,-322 222,-302 244,-286 C266,-258 300,-206 320,-176 L300,-172 C270,-214 240,-262 150,-310 Z" fill="{light}" opacity="0.45"/>'
             f'<path d="M290,-214 C300,-200 312,-186 324,-172 C328,-150 316,-134 300,-134 C286,-136 276,-144 268,-152 C276,-176 282,-196 290,-214 Z" fill="{muzzle}" opacity="0.95"/>'
             f'<path d="M204,-196 C196,-170 192,-140 180,-118 C172,-106 160,-104 150,-110 L160,-150 C176,-170 190,-186 204,-196 Z" fill="{dark}" opacity="0.5"/>'   # açık burun
             f'<path d="M236,-296 C260,-292 290,-240 306,-206" stroke="{light}" stroke-width="10" fill="none" opacity="0.6"/>')
    o.append(clipped(cid, body, inner))
    o.append(f'<path d="{body}" fill="none" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>')
    # anatomi çizgileri: kürek kemiği, kaburga izi, kalça kemiği, diz/dirsek kıvrımı, gerdan kıvrımları
    o.append(f'<path d="M140,-330 C120,-280 100,-220 100,-160" stroke="{dark}" stroke-width="5" fill="none" opacity="0.8"/>'
             f'<path d="M100,-170 C112,-176 126,-170 132,-158" stroke="{INK}" stroke-width="4" fill="none" opacity="0.7"/>'
             + "".join(f'<path d="M{-20 - k*34},{-262 + k*2} C{-26 - k*34},{-226} {-24 - k*34},{-196} {-14 - k*34},{-168}" stroke="{dark}" stroke-width="3" fill="none" opacity="0.45"/>' for k in range(4))
             + f'<path d="M-214,-300 C-200,-286 -196,-270 -206,-254" stroke="{INK}" stroke-width="4.5" fill="none" opacity="0.75"/>'
             f'<path d="M-190,-176 C-170,-200 -150,-230 -146,-262" stroke="{dark}" stroke-width="5" fill="none" opacity="0.7"/>'
             f'<path d="M200,-196 C196,-176 192,-156 184,-138 M206,-180 C200,-160 194,-146 186,-132" stroke="{dark}" stroke-width="3.5" fill="none" opacity="0.7"/>')
    # yakın bacaklar
    o.append(leg([(122, -66), (128, -24), (132, 0)], [27, 23], col, ink=INK))
    o.append(leg([(-218, -84), (-208, -24), (-204, 0)], [27, 23], col, ink=INK))
    o.append(f'<path d="M110,-40 L148,-38 L150,0 L112,0 Z" fill="{mud}" opacity="0.7"/><path d="M-226,-40 L-188,-40 L-186,0 L-224,0 Z" fill="{mud}" opacity="0.7"/>')   # çamurlu alt bacak
    # kuyruk: kuyruk başından kalçaya yaslanır, püskül diz hizasında
    o.append(f'<path d="M-252,-296 C-276,-260 -276,-190 -262,-120" stroke="{INK}" stroke-width="15" fill="none" stroke-linecap="round"/><path d="M-252,-296 C-276,-260 -276,-190 -262,-120" stroke="{col}" stroke-width="8" fill="none" stroke-linecap="round"/>'
             f'<path d="M-262,-126 C-276,-110 -276,-84 -266,-70 C-258,-86 -250,-100 -254,-124 Z" fill="#2A1A10" stroke="{INK}" stroke-width="4"/>'
             + "".join(f'<path d="M-262,-110 l{-6+k*4},{24+k%2*6}" stroke="#2A1A10" stroke-width="3"/>' for k in range(4)))
    # kulak (yatay, iç açık) + boynuz (kısa, öne-yukarı kıvrık; kökte halkalı)
    o.append(f'<path d="M236,-284 C216,-296 192,-300 176,-290 C190,-278 214,-272 240,-272 Z" fill="{col}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/><path d="M230,-282 C214,-288 198,-290 186,-288" stroke="#C89A7A" stroke-width="4" fill="none"/>')
    horn = "M244,-296 C250,-320 266,-338 290,-344 C298,-344 302,-338 296,-334 C278,-326 266,-312 260,-292 Z"
    o.append(f'<path d="{horn}" fill="#D8CCAE" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/><path d="M244,-300 C252,-318 266,-332 286,-340" stroke="#8A7A5A" stroke-width="3" fill="none"/>'
             f'<path d="M244,-298 l12,4 M247,-306 l11,5" stroke="#6A5A40" stroke-width="2.5"/><path d="M286,-344 l8,10" stroke="#3A3020" stroke-width="5" stroke-linecap="round"/>')
    o.append(f'<path d="M238,-292 C232,-304 230,-316 238,-326 C244,-314 250,-306 250,-294 Z" fill="#B8A88A" stroke="{INK}" stroke-width="4"/>')   # uzak boynuz kökü
    # göz (kaş çıkıntısı altında, badem; parlak nokta yok), burun deliği, ağız
    o.append(f'<path d="M248,-262 C256,-270 270,-268 274,-258" stroke="{INK}" stroke-width="5" fill="none"/>'
             f'<path d="M252,-256 C258,-262 268,-262 272,-254 C266,-249 258,-249 252,-256 Z" fill="#1A0E08"/><path d="M256,-255 l6,-2" stroke="#6A4A3A" stroke-width="1.5"/>'
             f'<path d="M318,-170 C322,-162 320,-154 312,-152" stroke="{INK}" stroke-width="5" fill="none"/>'
             f'<path d="M302,-142 C292,-142 284,-146 278,-150" stroke="{INK}" stroke-width="3.5" fill="none"/>'
             f'<path d="M321,-156 q4,8 -2,14" stroke="#9AB4C8" stroke-width="2.5" fill="none" opacity="0.8"/>'
             + "".join(f'<path d="M{226+k*8},{-190+k*2} l-2,10" stroke="{dark}" stroke-width="2.5"/>' for k in range(4)))   # burun ıslaklığı
    # gerdan sarkığı alt kenarda kıl
    o.append("".join(f'<path d="M{176 - k*6},{-128 + k*3} l-3,9" stroke="{dark}" stroke-width="2.5"/>' for k in range(5)))
    if yoke:   # cidago boyunduruğu: hörgücün önüne oturan kavisli tahta + boyun kayışı
        o.append(f'<path d="M150,-354 C178,-362 210,-346 218,-322 L206,-316 C196,-336 174,-346 152,-342 Z" fill="#6A4A2C" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
                 f'<path d="M210,-318 C218,-280 214,-236 204,-200" stroke="{INK}" stroke-width="13" fill="none"/><path d="M210,-318 C218,-280 214,-236 204,-200" stroke="#5A3A22" stroke-width="7" fill="none"/>'
                 f'<path d="M156,-346 C150,-300 160,-250 190,-206" stroke="#4A2E1A" stroke-width="7" fill="none" opacity="0.8"/>'
                 f'<circle cx="168" cy="-300" r="7" fill="#8A8A82" stroke="{INK}" stroke-width="3"/>')
    o.append('</g>')
    return "".join(o)

def sheep(x, y, s=1.0, seed=0, wool="#C8BCA6", face="#3A2E26", graze=True, flip=1):
    """Kuzey kısa kuyruklu koyunu: kirli yün kütlesi (kıvrık tutam kenarı), koyu yüz ve bacak, küçük boynuz."""
    r = R(seed); o = [f'<g transform="translate({x},{y}) scale({s*flip},{s})">', '<ellipse cx="0" cy="3" rx="70" ry="9" fill="#000" opacity="0.3"/>']
    o.append(leg([(-34, -40), (-38, -14), (-38, 0)], [9, 7], "#2A221C", hw=9, cloven=False) + leg([(30, -40), (34, -14), (34, 0)], [9, 7], "#2A221C", hw=9, cloven=False))
    pts = []
    for i in range(22):
        a = i / 22 * 2 * math.pi; rx, ry = 62, 34
        pts.append((rx * math.cos(a) * r.uniform(0.95, 1.08), -50 + ry * math.sin(a) * r.uniform(0.92, 1.1)))
    d = smooth(pts, closed=True)
    o.append(f'<path d="{d}" fill="{wool}" {O7.T("kurk", 0.3)}/><path d="{d}" fill="none" stroke="{INK}" stroke-width="4.5" stroke-dasharray="9 3" stroke-linejoin="round"/>')
    o.append(f'<path d="M-50,-34 Q0,-14 54,-34 L50,-24 Q0,-6 -50,-26 Z" fill="#6A5E4C" opacity="0.6"/><path d="M-40,-74 Q0,-86 40,-76" stroke="#ECE4D4" stroke-width="7" fill="none" opacity="0.7"/>')
    o.append("".join(f'<path d="M{r.uniform(-50,50):.0f},{r.uniform(-76,-30):.0f} q4,-4 8,0 q4,4 8,0" stroke="#8A7E6A" stroke-width="2" fill="none"/>' for _ in range(14)))
    hy = -26 if graze else -70
    o.append(leg([(-48, -36), (-44, -14), (-46, 0)], [10, 8], "#3A2E26", hw=10, cloven=False) + leg([(40, -36), (46, -14), (44, 0)], [10, 8], "#3A2E26", hw=10, cloven=False))
    o.append(f'<path d="M50,-62 Q70,{hy-14} 84,{hy-6} Q98,{hy+4} 92,{hy+16} Q80,{hy+22} 70,{hy+12} Q60,{hy-4} 46,-40 Z" fill="{face}" stroke="{INK}" stroke-width="4"/>'
             f'<path d="M66,{hy-12} q-12,-4 -16,6" stroke="{INK}" stroke-width="5" fill="none"/><path d="M68,{hy-14} q12,-12 2,-20 q-8,-2 -8,6" stroke="#8A7A5A" stroke-width="4" fill="none"/>'
             f'<circle cx="80" cy="{hy-2}" r="2.6" fill="#E8C870"/><path d="M48,-70 q10,-10 22,-6" stroke="{wool}" stroke-width="10" fill="none" stroke-linecap="round"/>')
    o.append(f'<path d="M-62,-56 q-12,6 -8,18" stroke="{INK}" stroke-width="9" stroke-linecap="round" fill="none"/><path d="M-62,-56 q-12,6 -8,18" stroke="{wool}" stroke-width="4" stroke-linecap="round" fill="none"/>')
    o.append('</g>'); return "".join(o)

def raven(x, y, s=1.0, flip=1, pose="perch", seed=0):
    """Kuzgun: kalın kavisli gaga, tüylü gırtlak (hackle), kama kuyruk, mor-mavi parıltı; profil, sağa bakar."""
    o = [f'<g transform="translate({x},{y}) scale({s*flip},{s})">']
    if pose == "perch":
        body = ("M-96,10 L-60,-6 C-40,-30 -10,-52 28,-58 C46,-62 62,-70 70,-84 C78,-98 96,-104 112,-98 C122,-94 128,-88 132,-82 "
                "C150,-80 172,-76 186,-70 C170,-66 150,-66 134,-68 C128,-58 118,-52 104,-50 C96,-40 92,-24 80,-12 C60,10 30,22 -10,22 C-40,22 -60,20 -96,10 Z")
        o.append(f'<path d="{body}" fill="#16141C"/>')
        o.append(f'<path d="M-30,-30 C10,-50 50,-48 76,-30 C60,-10 30,4 -20,4 Z" fill="#232032"/>')   # kanat
        o.append("".join(f'<path d="M{-40 + k*16},{-26 + k*2} C{-10 + k*14},{-34 + k*2} {20 + k*12},{-30 + k*3} {40 + k*8},{-20 + k*4}" stroke="#3E3A5A" stroke-width="2.5" fill="none" opacity="0.8"/>' for k in range(5)))
        o.append(f'<path d="M-90,8 L-140,22 L-150,12 L-136,6 L-148,0 L-96,0 Z" fill="#16141C" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>')   # kama kuyruk
        o.append(f'<path d="M-30,-44 C10,-62 50,-66 72,-86 C86,-100 104,-102 118,-96" stroke="#7A86B8" stroke-width="4" fill="none" opacity="0.75"/>'   # mavi-mor parıltı (ışık tarafı)
                 f'<path d="M-20,-38 C10,-52 40,-52 60,-60" stroke="#B8C4E8" stroke-width="2" fill="none" opacity="0.6"/>')
        o.append("".join(f'<path d="M{98 - k*5},{-52 + k*3} l{-4},{10}" stroke="#2C2838" stroke-width="3" stroke-linecap="round"/>' for k in range(6)))   # gırtlak tüyleri
        o.append(f'<path d="{body}" fill="none" stroke="{INK}" stroke-width="3.5" stroke-linejoin="round"/>')
        o.append(f'<path d="M132,-82 C150,-80 172,-76 186,-70 C170,-66 150,-66 134,-68" fill="#24222A" stroke="{INK}" stroke-width="3"/><path d="M138,-78 C156,-76 170,-74 182,-71" stroke="#5A5868" stroke-width="2" fill="none"/>')
        o.append(f'<path d="M118,-90 C122,-80 128,-76 134,-76" stroke="#2C2838" stroke-width="5" fill="none"/>')   # gaga kökü kılları
        o.append(f'<circle cx="114" cy="-86" r="4.2" fill="#0A0808"/><circle cx="115.5" cy="-87.5" r="1.4" fill="#8A8AA0"/>')
        o.append(leg([(40, 16), (46, 40)], [7], "#1A181E", hw=5, cloven=False))
        o.append(f'<path d="M30,44 l26,0 M40,44 l-8,6 M50,44 l10,6" stroke="#1A181E" stroke-width="5" stroke-linecap="round"/>')
    else:   # uçuş (alttan): geniş kanat, 5 parmaklı el tüyleri, kama kuyruk, öne uzanan baş ve kalın gaga
        r = R(seed); up = r.uniform(-0.4, 0.6)
        def wing(sg):
            tipx, tipy = sg * 150, -30 - up * 50
            fingers = " ".join(f"L{sg*(150 - k*9):.0f},{tipy + 6 + k*9 + (k%2)*6:.0f} L{sg*(140 - k*9):.0f},{tipy + 12 + k*9:.0f}" for k in range(5))
            return (f"M{sg*10},-14 C{sg*50},{-30-up*30:.0f} {sg*100},{tipy-6:.0f} {tipx},{tipy:.0f} {fingers} "
                    f"C{sg*90},{20+tipy*0.2:.0f} {sg*40},18 {sg*8},14 Z")
        o.append(f'<path d="{wing(-1)}" fill="#18161E" stroke="{INK}" stroke-width="2.5" stroke-linejoin="round"/><path d="{wing(1)}" fill="#18161E" stroke="{INK}" stroke-width="2.5" stroke-linejoin="round"/>')
        o.append(f'<path d="M-12,-10 C-14,-40 -8,-62 0,-70 C8,-62 14,-40 12,-10 L14,30 L22,62 L0,54 L-22,62 L-14,30 Z" fill="#141218" stroke="{INK}" stroke-width="2.5" stroke-linejoin="round"/>'
                 f'<path d="M-5,-70 L0,-90 L5,-70 Z" fill="#24222A" stroke="{INK}" stroke-width="2"/>'
                 f'<path d="M-60,-20 C-30,-26 -12,-20 -8,-10 M60,-20 C30,-26 12,-20 8,-10" stroke="#3E3A5A" stroke-width="2" fill="none"/>')
    o.append('</g>'); return "".join(o)

def gull(x, y, s=1.0, seed=0):
    r = R(seed); up = r.uniform(-0.5, 1); s2 = s * r.uniform(0.85, 1.1)
    return (f'<g transform="translate({x},{y}) scale({s2})"><path d="M0,0 C-14,{-10-up*8:.0f} -30,{-14-up*12:.0f} -52,{-6-up*10:.0f} C-34,{-6-up*4:.0f} -16,-2 0,4 C16,-2 34,{-6-up*4:.0f} 52,{-6-up*10:.0f} C30,{-14-up*12:.0f} 14,{-10-up*8:.0f} 0,0 Z" fill="#F2F2EE" stroke="#2A2A2E" stroke-width="2.2"/>'
            f'<path d="M-52,{-6-up*10:.0f} l10,1 M52,{-6-up*10:.0f} l-10,1" stroke="#1A1A1E" stroke-width="4" stroke-linecap="round"/><ellipse cx="0" cy="2" rx="5" ry="9" fill="#E8E8E4" stroke="#2A2A2E" stroke-width="1.8"/></g>')

# ======================================================================= tarım nesneleri
def hay_rack(x, y, L=420, s=1.0, seed=3):
    """Norveç tipi kurutma çiti (hesje): eğik direkler, yatay sırıklar, üstüne serili saman; üstü ışıklı, altı gölgede."""
    r = R(seed); o = [f'<g transform="translate({x},{y}) scale({s})">', f'<ellipse cx="{L/2}" cy="6" rx="{L*0.62:.0f}" ry="16" fill="#000" opacity="0.3" filter="url(#b4)"/>']
    posts = [i * L / 4 for i in range(5)]
    for px in posts:
        o.append(f'<path d="M{px},4 L{px+6},-210" stroke="{INK}" stroke-width="15" stroke-linecap="round"/><path d="M{px},4 L{px+6},-210" stroke="#5A4028" stroke-width="8" stroke-linecap="round"/>')
    hay = (f"M-14,-198 " + " ".join(f"Q{L*t+r.uniform(-10,10):.0f},{-214+r.uniform(-6,6):.0f} {L*(t+0.1):.0f},{-200+r.uniform(-4,4):.0f}" for t in [i / 10 for i in range(10)])
           + f" L{L+16},-70 " + " ".join(f"Q{L*(1-t)+r.uniform(-8,8):.0f},{-50+r.uniform(-10,14):.0f} {L*(1-t-0.1):.0f},{-62+r.uniform(-6,10):.0f}" for t in [i / 10 for i in range(10)]) + " Z")
    o.append(f'<path d="{hay}" fill="#A08A50"/>')
    cid = f"hay{seed}"
    inner = (f'<rect x="-30" y="-230" width="{L+60}" height="60" fill="#D8C080" opacity="0.65"/><rect x="-30" y="-110" width="{L+60}" height="80" fill="#4A3E24" opacity="0.55"/>'
             + "".join(f'<path d="M{r.uniform(-20,L+20):.0f},{r.uniform(-214,-50):.0f} l{r.uniform(-4,4):.0f},{r.uniform(14,34):.0f}" stroke="{r.choice(["#6A5A30", "#C8B070", "#8A7440", "#E2D094"])}" stroke-width="{r.uniform(1.5,3):.1f}"/>' for _ in range(int(L * 1.4)))
             + "".join(f'<path d="M-30,{yy} Q{L/2},{yy+r.uniform(-6,6):.0f} {L+30},{yy}" stroke="#5A4A26" stroke-width="3" fill="none" opacity="0.6"/>' for yy in (-160, -118, -80)))
    o.append(clipped(cid, hay, inner))
    o.append(f'<path d="{hay}" fill="none" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>')
    o.append("".join(f'<path d="M{r.uniform(0,L):.0f},{-60+r.uniform(-6,6):.0f} l{r.uniform(-6,6):.0f},{r.uniform(12,28):.0f}" stroke="#8A7440" stroke-width="2.5"/>' for _ in range(40)))   # sarkan saplar
    for px in posts:   # direk tepeleri saman üstünde
        o.append(f'<path d="M{px+5},-196 L{px+6},-222" stroke="{INK}" stroke-width="15" stroke-linecap="round"/><path d="M{px+5},-196 L{px+6},-222" stroke="#6A4C30" stroke-width="8" stroke-linecap="round"/>')
    o.append("".join(f'<path d="M{r.uniform(-20,L+30):.0f},{r.uniform(-2,10):.0f} l{r.uniform(-10,10):.0f},{r.uniform(-4,4):.0f}" stroke="#C8B070" stroke-width="2"/>' for _ in range(30)))   # yere dökülen saman
    o.append('</g>'); return "".join(o)

def stone_wall(pts, seed=5, h=46, moss=True, snow=0.0):
    """Kuru taş duvar: polyline boyunca iki-üç sıra yuvarlak taş; her taş dokulu, üstü ışıklı, altı koyu; arada yosun ve kar."""
    r = R(seed); o = []
    segs = []
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        L = math.hypot(bx - ax, by - ay); n = int(L / (h * 0.55))
        for i in range(n): t = (i + r.uniform(0, 0.3)) / n; segs.append((ax + (bx - ax) * t, ay + (by - ay) * t))
    sc = lambda yy: 0.6 + 0.4 * (yy - 600) / 400
    o.append("".join(f'<ellipse cx="{x:.0f}" cy="{y+4:.0f}" rx="{h*0.7*sc(y):.0f}" ry="{h*0.16*sc(y):.0f}" fill="#000" opacity="0.28"/>' for x, y in segs))
    for row in range(3):
        for k, (x, y) in enumerate(segs):
            if row == 2 and k % 3 == 0: continue
            q = sc(y); w = h * r.uniform(0.38, 0.6) * q; hh = h * r.uniform(0.26, 0.38) * q
            cx = x + r.uniform(-6, 6) + (row % 2) * w * 0.5; cy = y - row * h * 0.32 * q - hh * 0.5
            ptsS = [(cx + w * math.cos(a) * r.uniform(0.85, 1.1), cy + hh * math.sin(a) * r.uniform(0.85, 1.1)) for a in [i / 8 * 2 * math.pi for i in range(8)]]
            d = smooth(ptsS, closed=True); tone = r.choice(["#7E7A70", "#6E6A62", "#8A8478", "#76705E"])
            o.append(f'<path d="{d}" fill="{tone}" {O7.T("tas", 0.6)}/><path d="{d}" fill="none" stroke="{INK}" stroke-width="{3*q+1:.1f}"/>'
                     f'<path d="M{cx-w*0.7:.1f},{cy-hh*0.45:.1f} Q{cx-w*0.1:.1f},{cy-hh*1.0:.1f} {cx+w*0.6:.1f},{cy-hh*0.6:.1f}" stroke="#C8C2B4" stroke-width="{2.4*q+0.5:.1f}" fill="none" opacity="0.8"/>'
                     f'<path d="M{cx-w*0.6:.1f},{cy+hh*0.6:.1f} Q{cx:.1f},{cy+hh*1.0:.1f} {cx+w*0.8:.1f},{cy+hh*0.4:.1f}" stroke="#2E2A24" stroke-width="{3*q:.1f}" fill="none" opacity="0.6"/>')
            if moss and r.random() < 0.35: o.append(f'<path d="M{cx-w*0.5:.1f},{cy-hh*0.6:.1f} q{w*0.4:.1f},{-hh*0.4:.1f} {w*0.8:.1f},0" stroke="#5E6E3A" stroke-width="{4*q:.1f}" fill="none" stroke-linecap="round" opacity="0.85"/>')
            if snow and row == 2 and r.random() < snow: o.append(f'<path d="M{cx-w*0.6:.1f},{cy-hh*0.55:.1f} Q{cx:.1f},{cy-hh*1.15:.1f} {cx+w*0.6:.1f},{cy-hh*0.55:.1f} Z" fill="#E6ECF0" stroke="#8A96A0" stroke-width="1.5"/>')
    return "".join(o)

def post(x, y, h, w=22, seed=0, lean=0.0, ink=INK, col="#5A4430"):
    """Zemine giren direk: üstü kesik ve çatlak, alt tarafı çamurlu, zemin halkası."""
    r = R(seed); tx = x + lean * h
    d = f"M{x-w/2:.1f},{y+6} L{tx-w/2:.1f},{y-h:.1f} L{tx+w/2:.1f},{y-h-w*0.25:.1f} L{x+w/2:.1f},{y+6} Z"
    o = [f'<ellipse cx="{x+w*0.4:.1f}" cy="{y+4:.1f}" rx="{w*1.2:.1f}" ry="{w*0.28:.1f}" fill="#000" opacity="0.4"/>', f'<path d="{d}" fill="{col}" {O7.T("ahsap", 0.5)}/>']
    o.append(clipped(f"po{seed}", d, f'<rect x="{x}" y="{y-h-20:.0f}" width="{w}" height="{h+30}" fill="#1A1410" opacity="0.4"/>'
                     f'<rect x="{x-w}" y="{y-h*0.18:.0f}" width="{w*3}" height="{h*0.2+8:.0f}" fill="#2A2018" opacity="0.6"/>'
                     + "".join(f'<path d="M{x-w/2+w*r.uniform(0.15,0.85)+lean*h*0.5:.1f},{y-h*r.uniform(0.2,0.9):.1f} l{lean*20:.1f},{-h*r.uniform(0.1,0.3):.1f}" stroke="#2A1E14" stroke-width="2"/>' for _ in range(4))))
    o.append(f'<path d="{d}" fill="none" stroke="{ink}" stroke-width="4" stroke-linejoin="round"/>')
    o.append(f'<path d="M{tx-w/2:.1f},{y-h:.1f} L{tx+w/2:.1f},{y-h-w*0.25:.1f}" stroke="#9A8060" stroke-width="3"/>')
    o.append(f'<path d="M{x-w*0.9:.1f},{y+4} Q{x:.1f},{y-4} {x+w*0.9:.1f},{y+4}" stroke="#2A2018" stroke-width="4" fill="none"/>')
    return "".join(o)

def grass_tuft(x, y, h, seed, col="#8A8458", dark="#4E4A30", frost=0.0, n=9):
    r = R(seed); o = []
    for i in range(n):
        a = r.uniform(-0.7, 0.7); hh = h * r.uniform(0.5, 1.0); bx = x + r.uniform(-h * 0.2, h * 0.2)
        cxp = bx + math.sin(a) * hh * 0.5; ex_ = bx + math.sin(a) * hh * 1.1; ey_ = y - hh * math.cos(a * 0.6)
        o.append(f'<path d="M{bx:.1f},{y} Q{cxp:.1f},{y-hh*0.6:.1f} {ex_:.1f},{ey_:.1f}" stroke="{dark if i%3==0 else col}" stroke-width="{max(1.5,h/22):.1f}" fill="none" stroke-linecap="round"/>')
        if frost and r.random() < frost: o.append(f'<circle cx="{ex_:.1f}" cy="{ey_:.1f}" r="{max(1.2,h/30):.1f}" fill="#EEF4F8"/>')
    return "".join(o)


# ======================================================================= f1 · Kattegat 793, tarlada Ragnar
SUN = (330, 175)

def ard_beam(share, ox_xy, s, near=False):
    """Saban oku + tek hayvan koşumu: ok (beam) paydan kısa çapraz kola (palanga) çıkar; iki ip (iz) öküzün böğrü boyunca
    boyunduruğun halkasına gider. near=False: ok + uzak ip (öküzden önce); near=True: yakın ip (öküzün üstünde)."""
    sx, sy = share; ox_, oy = ox_xy
    tx, ty = ox_ - 300 * s, oy - 120 * s          # palanga (hokların arkasında)
    ring = (ox_ + 168 * s, oy - 300 * s)
    if not near:
        o = [f'<path d="M{sx},{sy-8} Q{(sx+tx)/2:.0f},{sy-30:.0f} {tx},{ty}" stroke="{INK}" stroke-width="20" fill="none" stroke-linecap="round"/>'
             f'<path d="M{sx},{sy-8} Q{(sx+tx)/2:.0f},{sy-30:.0f} {tx},{ty}" stroke="#7A5232" stroke-width="11" fill="none" stroke-linecap="round"/>'
             f'<path d="M{sx},{sy-12} Q{(sx+tx)/2:.0f},{sy-34:.0f} {tx},{ty-4}" stroke="#B88A5A" stroke-width="3" fill="none" opacity="0.8"/>',
             f'<path d="M{tx+4},{ty-40} L{tx-4},{ty+40}" stroke="{INK}" stroke-width="16" stroke-linecap="round"/><path d="M{tx+4},{ty-40} L{tx-4},{ty+40}" stroke="#6A4A2C" stroke-width="9" stroke-linecap="round"/>',
             f'<path d="M{tx-2},{ty+36} Q{ox_-60*s:.0f},{oy-80*s:.0f} {ring[0]-30*s:.0f},{ring[1]+90*s:.0f}" stroke="#2A2018" stroke-width="5" fill="none"/>']
    else:
        o = [f'<path d="M{tx+2},{ty-36} Q{ox_-80*s:.0f},{oy-160*s:.0f} {ring[0]:.0f},{ring[1]:.0f}" stroke="{INK}" stroke-width="9" fill="none"/>'
             f'<path d="M{tx+2},{ty-36} Q{ox_-80*s:.0f},{oy-160*s:.0f} {ring[0]:.0f},{ring[1]:.0f}" stroke="#A88A5E" stroke-width="4.5" fill="none"/>'
             + "".join(f'<path d="M{tx + (ring[0]-tx)*u:.0f},{ty-36 + (ring[1]-ty+36)*u + 30*math.sin(math.pi*u):.0f} l6,-4" stroke="#5A4630" stroke-width="2"/>' for u in [k / 14 for k in range(1, 14)])]
    return "".join(o)

def ard_body(sx, sy):
    """Ragnar'ın elinden toprağa inen sap ile taban; demir uç toprağa gömülü; önünde toprak ve kırağı fışkırması."""
    o = [f'<path d="M{sx-46},{sy-4} L{sx+40},{sy+4} L{sx+64},{sy+14} L{sx+30},{sy+18} L{sx-50},{sy+10} Z" fill="#5A3A20" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>',
         f'<path d="M{sx+40},{sy+4} L{sx+74},{sy+16} L{sx+38},{sy+20} Z" fill="#8A8E92" stroke="{INK}" stroke-width="4"/>']
    o.append("".join(f'<path d="M{sx+62+k*7},{sy+10} q{6+k*3},{-14-k*4} {14+k*5},{-10-k*2}" stroke="#3A2C1E" stroke-width="{7-k}" fill="none" stroke-linecap="round"/>' for k in range(4)))   # devrilen toprak
    o.append("".join(f'<circle cx="{sx+80+k*9}" cy="{sy-6-k*4+(k%2)*6}" r="{3.5-k*0.4:.1f}" fill="#3A2C1E"/>' for k in range(6)))
    return "".join(o)

def field_svg(y0=760):
    """Sürülmüş tarla: perspektifte yatay karıklar (uzakta sık, yakında seyrek), sırtlarda kırağı; Ragnar'ın şeridinin sağı sürülmemiş anız."""
    r = R(77); W_, H_ = W, H
    gp = f"M0,{y0} Q600,{y0-22} 1100,{y0-8} Q1500,{y0+4} {W_},{y0-14} L{W_},{H_} L0,{H_} Z"
    o = [f'<path d="{gp}" fill="#4A3A2A"/>']
    inner = [f'<rect width="{W_}" height="{H_}" filter="url(#nz_d)" opacity="0.6"/>', f'<rect width="{W_}" height="{H_}" filter="url(#nz_f)" opacity="0.5"/>']
    rows = []
    y = y0 + 6; k = 0
    while y < H_ + 40:
        sp = 7 + (y - y0) * 0.075; rows.append((y, sp)); y += sp; k += 1
    cur = 958   # Ragnar'ın şu anki karığı
    share_x = 752
    for i, (yy, sp) in enumerate(rows):
        bend = lambda x: yy + 10 * math.sin(x / 520 + i * 0.05) - (x / W_) * 6
        q = (yy - y0) / (H_ - y0)
        unpl_x = share_x if abs(yy - cur) < sp * 0.6 else (0 if yy > cur + sp * 0.4 else W_ + 10)
        # anız (sürülmemiş): soluk, kırağılı
        if yy > cur + sp * 0.4 or abs(yy - cur) < sp * 0.6:
            xs = 0 if yy > cur + sp * 0.4 else share_x
            inner.append(f'<path d="M{xs},{bend(xs)-sp/2:.1f} L{W_},{bend(W_)-sp/2:.1f} L{W_},{bend(W_)+sp/2+1:.1f} L{xs},{bend(xs)+sp/2+1:.1f} Z" fill="#6A6450"/>')
            for j in range(int(26 * (1 - 0.5 * q) * (W_ - xs) / W_)):
                x = r.uniform(xs, W_); h_ = 4 + q * 14
                inner.append(f'<path d="M{x:.0f},{bend(x)+sp*0.3:.0f} l{r.uniform(-2,2):.1f},{-h_:.1f}" stroke="{r.choice(["#A89A6A", "#8A7E58", "#C8BC94"])}" stroke-width="{1+q*1.5:.1f}"/>')
            inner.append("".join(f'<ellipse cx="{r.uniform(xs,W_):.0f}" cy="{bend(r.uniform(0,W_))+r.uniform(-sp/3,sp/3):.0f}" rx="{r.uniform(6,26)*(0.4+q):.0f}" ry="{r.uniform(2,5)*(0.4+q):.1f}" fill="#E4ECF2" opacity="0.75"/>' for _ in range(int(8 + 10 * q))))
            if abs(yy - cur) >= sp * 0.6: continue
        xe = share_x if abs(yy - cur) < sp * 0.6 else W_
        # karık: oluk (koyu, soğuk gölge) + sırt (ışık sol üstten → sırtın üstü açık, kırağı sırtta)
        pts = [(x, bend(x)) for x in range(0, int(xe) + 40, 40)]
        dd = "M" + " L".join(f"{x:.0f},{y_:.1f}" for x, y_ in pts)
        fresh = abs(yy - cur) < sp * 0.6
        inner.append(f'<path d="{dd}" stroke="{"#24180E" if fresh else "#2A2018"}" stroke-width="{sp*0.42:.1f}" fill="none" stroke-linecap="round"/>')
        inner.append(f'<path d="{dd}" transform="translate(0,{-sp*0.35:.1f})" stroke="{"#7A5C3E" if fresh else "#6E5E4A"}" stroke-width="{max(1.2, sp*0.22):.1f}" fill="none" opacity="0.9"/>')
        if not fresh:
            for j in range(int(30 * (0.3 + q))):
                x = r.uniform(0, xe); inner.append(f'<path d="M{x:.0f},{bend(x)-sp*0.38:.1f} l{r.uniform(8,40)*(0.3+q):.0f},{r.uniform(-1,1):.1f}" stroke="#DCE6EE" stroke-width="{1+q*2.5:.1f}" opacity="{r.uniform(0.45,0.85):.2f}" stroke-linecap="round"/>')
        else:   # taze, ıslak, kırağısız toprak, devrik kesek
            for j in range(26):
                x = r.uniform(0, xe - 30); inner.append(f'<path d="M{x:.0f},{bend(x)-sp*0.3:.1f} q6,-8 14,-2" stroke="#3A2A1C" stroke-width="5" fill="none"/>')
    # tarla taşları ve kesekler
    for k in range(40):
        x = r.uniform(0, W_); yy = r.uniform(y0 + 30, H_); q = (yy - y0) / (H_ - y0); sz = (4 + 18 * q) * r.uniform(0.6, 1.2)
        inner.append(f'<path d="M{x-sz:.0f},{yy:.0f} Q{x-sz*0.7:.0f},{yy-sz*0.8:.0f} {x:.0f},{yy-sz*0.8:.0f} Q{x+sz:.0f},{yy-sz*0.6:.0f} {x+sz:.0f},{yy:.0f} Z" fill="#5E584E" stroke="#1E1812" stroke-width="{1+q*2:.1f}"/>'
                     f'<path d="M{x-sz*0.5:.0f},{yy-sz*0.55:.0f} q{sz*0.5:.0f},{-sz*0.3:.0f} {sz:.0f},0" stroke="#D8E0E6" stroke-width="{1+q*2:.1f}" fill="none"/>')
    o.append(clipped("fld", gp, "".join(inner)))
    o.append(f'<path d="M0,{y0} Q600,{y0-22} 1100,{y0-8} Q1500,{y0+4} {W_},{y0-14}" stroke="#2A2018" stroke-width="4" fill="none"/>')
    return "".join(o)

def wattle_fence(x0, y0, x1, y1, h, seed=4):
    """Örme çit (wattle): direkler + aralarından geçen esnek dallar; uçta eğik direk."""
    r = R(seed); o = []; n = int(math.hypot(x1 - x0, y1 - y0) / (h * 0.5)) + 1
    ps = [(x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n) for i in range(n + 1)]
    for row in range(4):
        dy = -h * (0.2 + row * 0.2)
        d = "M" + " ".join(f"{x:.0f},{y+dy+(4 if (i+row)%2 else -4):.0f}" + (" Q" if False else " L") for i, (x, y) in enumerate(ps)).rstrip(" L")
        o.append(f'<path d="{d}" stroke="{INK}" stroke-width="{h*0.1+4:.1f}" fill="none" stroke-linejoin="round"/><path d="{d}" stroke="#7A6448" stroke-width="{h*0.1:.1f}" fill="none" stroke-linejoin="round"/>'
                 f'<path d="{d}" transform="translate(0,{-h*0.03:.1f})" stroke="#B49A70" stroke-width="{max(1,h*0.025):.1f}" fill="none" opacity="0.7"/>')
    for i, (x, y) in enumerate(ps):
        o.append(post(x, y, h * r.uniform(1.0, 1.15), w=max(6, h * 0.12), seed=seed * 50 + i, lean=r.uniform(-0.04, 0.04)))
    return "".join(o)

def smoke_col(x, y, h, seed, a=0.35, col="#D8DEE4", drift=1.0):
    r = R(seed); o = []
    for k in range(9):
        t = k / 8; cx = x + drift * (t ** 1.6) * h * 0.5 + r.uniform(-6, 6); cy = y - h * t; rr = 8 + 50 * t
        o.append(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{rr:.0f}" fill="{col}" opacity="{a*(1-t*0.75):.2f}"/>')
    return f'<g filter="url(#b8)">{"".join(o)}</g>'

def f1():
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    D = DEFS()
    # ---- 1 gökyüzü: soğuk sabah, güneş sol üstte bulut yırtığından
    o = [sky_grad("sk1", [(0, "#4E5E74"), (0.35, "#7A8CA2"), (0.62, "#C8C6BC"), (0.75, "#E2D2B4")]), f'<rect width="{W}" height="{H}" fill="url(#sk1)"/>',
         f'<rect width="{W}" height="700" filter="url(#nz_sky)" opacity="0.25"/>',
         f'<circle cx="{SUN[0]}" cy="{SUN[1]}" r="260" fill="#FFE8B8" opacity="0.55" filter="url(#b28)"/><circle cx="{SUN[0]}" cy="{SUN[1]}" r="110" fill="#FFF4D8" opacity="0.8" filter="url(#b18)"/><circle cx="{SUN[0]}" cy="{SUN[1]}" r="42" fill="#FFFBEE"/>']
    # bulut katmanları: uzak soluk, yakın koyu; güneşe bakan kenarlar altın
    for k, (cx, cy, w_, h_, a_) in enumerate([(1450, 250, 900, 150, 0.9), (900, 190, 700, 120, 0.85), (1750, 130, 700, 140, 0.9)]):
        o.append(cloud(cx, cy, w_, h_, 40 + k, "#9AA6B4", "#C8CED4", "#6E7A8A", blur=5, rim="#C8CED4", a=a_))
    for k, (cx, cy, w_, h_) in enumerate([(-60, 300, 420, 150), (760, 110, 640, 170), (1240, 120, 760, 170), (1880, 330, 520, 120), (160, 60, 700, 120)]):
        o.append(cloud(cx, cy, w_, h_, 50 + k, "#5E6A7C", "#8E98A6", "#3E4858", blur=4 if abs(cx - SUN[0]) < 500 else 7, rim="#F2D9A8" if abs(cx - SUN[0]) < 500 else "#76808E"))
    o.append(cloud(SUN[0] + 90, SUN[1] + 80, 380, 60, 61, "#8A8E98", "#E2D2B0", "#5A6474", blur=2, rim="#FFF0C8"))   # güneşin altındaki ince bulut
    draw(c, svg_sprite(D + "".join(o)), 0, 0, 1.0)
    # ---- 2 uzak dağlar (soluk, karlı) + orta dağlar + fiyort
    o = [D]
    far, _ = mountain([(-40, 470), (260, 330), (520, 410), (760, 300), (1000, 380), (1260, 290), (1520, 360), (1760, 300), (1980, 380)], 620, 11,
                      "#8A98A8", "#6E7C8E", "#E6ECF2", "#A8B6C6", snowline=380, strata="#4A5868", rough=0.28)
    o.append(far)
    o.append(f'<rect x="0" y="420" width="{W}" height="200" fill="#C8D0D8" opacity="0.45" filter="url(#b18)"/>')
    left, lp = mountain([(-60, 300), (120, 250), (330, 330), (520, 440), (700, 560), (820, 620)], 680, 21, "#4A5A52", "#2E3A36", "#DCE4EA", "#8E9EAE", snowline=330, strata="#1A2420", rough=0.2)
    right, rp = mountain([(1100, 640), (1260, 560), (1450, 440), (1640, 330), (1820, 270), (1990, 300)], 680, 22, "#46564E", "#2A3632", "#DCE4EA", "#8E9EAE", snowline=330, strata="#1A2420", rough=0.2)
    o.append(left + right)
    # yamaçta ladin ormanı (atmosferik: uzak soluk)
    o.append(forest(0, 760, lambda x: 470 + (x / 760) * 180, 34, 60, 70, 3, col="#33463C", lit="#55705E", dark="#1E2A24", snow=0.4))
    o.append(forest(1170, 1920, lambda x: 640 - (x - 1170) / 750 * 190, 34, 62, 70, 4, col="#2E4036", lit="#4E6A58", dark="#1A2620", snow=0.4))
    # fiyort suyu: gradyan, dağ yansıması, ışık şeridi, kırışıklar
    o.append(sky_grad("wat", [(0, "#8A9AA8"), (0.5, "#5E7080"), (1, "#3E4E5C")]) + f'<rect x="0" y="618" width="{W}" height="120" fill="url(#wat)"/>')
    o.append(f'<g opacity="0.35" filter="url(#b3)"><path d="{P([(x, 1236 - y) for x, y in lp])} L820,618 L-60,618 Z" fill="#2E3A36"/><path d="{P([(x, 1236 - y) for x, y in rp])} L1990,618 L1100,618 Z" fill="#2A3632"/></g>')
    o.append("".join(f'<path d="M{R(k).uniform(0,W):.0f},{R(k+7).uniform(624,730):.0f} h{R(k+3).uniform(20,120):.0f}" stroke="#C8D4DE" stroke-width="{R(k).uniform(1.5,3):.1f}" opacity="0.55"/>' for k in range(70)))
    o.append(f'<path d="M180,640 Q420,636 760,648" stroke="#F2E2BC" stroke-width="10" opacity="0.4" filter="url(#b4)"/>')   # güneş yansıması
    for (gx, gy, gs, fl) in ((880, 650, 0.09, 1), (1010, 662, 0.07, 1)):
        o.append(f'<g transform="translate({gx},{gy}) scale({gs*fl},{gs})">{G.longship(0, 0, 1.0, sail=True, oars=False)}</g>')
    draw(c, svg_sprite("".join(o)), 0, 0, 1.0)
    fog(c, 0, 600, "#DCE2E8", 0.5, n=7, seed=12, speed=0, h=60)
    # ---- 3 köy: kıyıda saz evler, iskele, duman; arkasında sis
    o = [D]
    o.append(f'<path d="M0,700 Q300,676 700,690 Q1100,700 1500,690 Q1760,684 {W},694 L{W},760 L0,770 Z" fill="#7A7462"/>')   # kıyı çayırı
    o.append(f'<path d="M0,700 Q300,676 700,690 Q1100,700 1500,690 Q1760,684 {W},694 L{W},706 Q1300,712 700,702 Q300,690 0,712 Z" fill="#B8B2A0"/>')   # çakıl şeridi
    o.append(f'<rect x="0" y="680" width="{W}" height="90" filter="url(#nz_d)" opacity="0.4"/>')
    o.append(f'<path d="M1300,700 L1560,672" stroke="{INK}" stroke-width="12"/><path d="M1300,700 L1560,672" stroke="#6A5440" stroke-width="7"/>' + "".join(f'<path d="M{x},{700-(x-1300)*0.108:.0f} v20" stroke="{INK}" stroke-width="5"/>' for x in range(1320, 1560, 40)))
    o.append(f'<g transform="translate(1480,668) scale(0.11)">{G.longship(0, 0, 1.0, sail=False, oars=False)}</g>')
    houses = sorted([(840, 704, 0.22), (980, 728, 0.34), (1240, 700, 0.20), (1390, 734, 0.36), (1620, 708, 0.24), (1700, 742, 0.30), (1130, 712, 0.24)], key=lambda q: q[1])
    for i, (hx, hy, hs) in enumerate(houses):
        o.append(smoke_col(hx + 180 * hs, hy - 330 * hs, 190, 300 + i, a=0.5, col="#E4E8EC", drift=1.4))
    for i, (hx, hy, hs) in enumerate(houses):
        o.append(O7.thatch_house(hx, hy, hs, snow=0.5, smoke=False, light=(i % 2 == 0)))
    o.append(wattle_fence(780, 744, 1180, 748, 26, seed=8) + wattle_fence(1260, 752, 1760, 758, 24, seed=9))
    draw(c, svg_sprite("".join(o)), 0, 0, 1.0)
    fog(c, 0, 700, "#E2E6EA", 0.28, n=6, seed=14, speed=0, h=40)
    # ---- 4 tarla, taş duvar, kurutma çiti, koyunlar
    o = [D, field_svg(762)]
    o.append(stone_wall([(-20, 790), (300, 772), (640, 768), (760, 772)], seed=7, h=48, snow=0.5))
    o.append(hay_rack(120, 800, L=330, s=0.85, seed=3))
    o.append(sheep(430, 812, 0.78, seed=1, graze=True) + sheep(1560, 806, 0.62, seed=2, graze=False, wool="#9A8A72", flip=-1) + sheep(1660, 812, 0.7, seed=3, graze=True, wool="#D2C8B4"))
    o.append(stone_wall([(1700, 800), (1950, 794)], seed=17, h=46, snow=0.4))
    draw(c, svg_sprite("".join(o)), 0, 0, 1.0)
    # ---- 5 Ragnar + saban + öküz
    RS = 0.62; rx, ry = 560, 968
    share = (752, 966); OX = (1150, 975); OXS = 0.86
    draw(c, svg_sprite(D + ard_beam((share[0] + 30, share[1] + 6), OX, OXS)), 0, 0, 1.0)
    OXs = svg_sprite(D + ox(*OX, OXS))
    rim(c, OXs, 0, 0, 1.0, "#FFE0B0", dx=-2, dy=-2, a=0.45)
    draw(c, OXs, 0, 0, 1.0)
    draw(c, svg_sprite(D + ard_beam((share[0] + 30, share[1] + 6), OX, OXS, near=True)), 0, 0, 1.0)
    handle_l = (f'<path d="M-40,-322 L{(share[0]-rx)/RS-30:.0f},{(share[1]-ry)/RS:.0f}" stroke="{INK}" stroke-width="22" stroke-linecap="round"/>'
                f'<path d="M-40,-322 L{(share[0]-rx)/RS-30:.0f},{(share[1]-ry)/RS:.0f}" stroke="#7A5232" stroke-width="12" stroke-linecap="round"/>'
                f'<path d="M-36,-318 L{(share[0]-rx)/RS-34:.0f},{(share[1]-ry)/RS-4:.0f}" stroke="#B08458" stroke-width="3" opacity="0.8"/>')
    RGs = full(dict(RG, _arm_up=False, _carry_svg=handle_l), ex("determined", IF.blink_at(0.2)), RS, facing=1, look=0.5)
    draw(c, svg_sprite(f'<ellipse cx="{rx+50}" cy="{ry+6}" rx="130" ry="16" fill="#000" opacity="0.45" filter="url(#b6)"/>' + D), 0, 0, 1.0)
    with live(c, rx, ry, phase=0.2, breathe=0.005):
        rim(c, RGs, rx, ry, 1.0, "#FFD8A0", dx=-4, dy=-3, a=0.75)
        draw(c, RGs, rx, ry, 1.0); shade_side(c, RGs, rx, ry, 0.42, rx - 100, rx + 160, "#1A2430")
    draw(c, svg_sprite(D + ard_body(*share)), 0, 0, 1.0)
    # ---- 6 ön plan: kuzgunlu çit direği (sol), donmuş ot (bulanık), uçan kuzgunlar
    o = [D, post(196, 1080, 300, w=40, seed=91, lean=0.02), raven(186, 1080 - 300 - 10 - 50 * 0.78, 0.78, seed=1)]
    o.append(grass_tuft(60, 1080, 120, 5, frost=0.5, n=14) + grass_tuft(250, 1085, 90, 6, frost=0.5, n=10))
    draw(c, svg_sprite("".join(o)), 0, 0, 1.0)
    fgb = svg_sprite(D + grass_tuft(1760, 1100, 200, 9, col="#6E6A48", dark="#3A3624", frost=0.6, n=22) + grass_tuft(1880, 1100, 160, 10, col="#6E6A48", dark="#3A3624", frost=0.6, n=16))
    draw(c, blurred(fgb, 6), 0, 0, 1.0)
    fgr = svg_sprite(D + stone_wall([(1560, 1075), (1980, 1035)], seed=33, h=170, snow=0.6))
    draw(c, blurred(fgr, 9), 0, 0, 1.0)
    draw(c, svg_sprite(D + raven(1010, 300, 0.26, pose="fly", seed=3) + raven(1090, 270, 0.2, pose="fly", seed=4)), 0, 0, 1.0)
    # ---- 7 ışık: bulut yırtığından hüzmeler tarlaya iner, sıcak/soğuk ayrımı
    for (xb, wb, a_) in ((560, 260, 0.22), (900, 200, 0.16), (300, 160, 0.14)):
        light_shaft(c, SUN[0] + 60, 60, xb, wb, "#FFE6B0", a_, t=0, y_top=SUN[1] + 40, y_bot=1000)
    bloom_spot(c, SUN[0], SUN[1], 260, "#FFE2A8", 0.35)
    glow(c, 620, 880, 380, "#FFC880", 0.10)
    gradient_grade(c, "#2A4A6E", "#2A2A3A", 0.22, "soft")
    grade(c, "#FFB070", 0.04, "screen")
    card_at(c, "KATTEGAT · 793", 1470, 150)
    card_at(c, "RAGNAR", 520, 485, "çiftçi (henüz)", 0.85)
    finish(c, cold=False); return s



# ======================================================================= f3 · doğuda fakir köyler (ciddi çizilmiş şaka)
def log_wall(x0, y0, x1, y1, h, n, seed, k_end=1.0, col="#5E4A34", ends=True, missing=()):
    """Kütük duvar: (x0,y0)-(x1,y1) alt kenar, h yükseklik (uzak uçta h*k_end). Her kütük ayrı ton, damar; aralarda yosun-çamur sıvası."""
    r = R(seed); o = []
    for i in range(n):
        if i in missing: continue
        ta, tb = i / n, (i + 1) / n
        ya0, ya1 = y0 - h * ta, y0 - h * tb; yb0, yb1 = y1 - h * k_end * ta, y1 - h * k_end * tb
        sag = r.uniform(-3, 4)
        d = f"M{x0},{ya0:.1f} Q{(x0+x1)/2:.0f},{(ya0+yb0)/2+sag:.1f} {x1},{yb0:.1f} L{x1},{yb1:.1f} Q{(x0+x1)/2:.0f},{(ya1+yb1)/2+sag:.1f} {x0},{ya1:.1f} Z"
        tone = r.choice([col, "#6A543A", "#54422E", "#4A3A28"])
        o.append(f'<path d="{d}" fill="{tone}" {O7.T("ahsap", 0.5)}/>'
                 f'<path d="M{x0},{ya1+2:.1f} Q{(x0+x1)/2:.0f},{(ya1+yb1)/2+sag+2:.1f} {x1},{yb1+2:.1f}" stroke="#A08A68" stroke-width="2.5" fill="none" opacity="0.7"/>'
                 f'<path d="M{x0},{ya0-1:.1f} Q{(x0+x1)/2:.0f},{(ya0+yb0)/2+sag-1:.1f} {x1},{yb0-1:.1f}" stroke="#2A2016" stroke-width="4" fill="none"/>')
        if r.random() < 0.5:
            u = r.uniform(0.1, 0.8)
            o.append(f'<path d="M{x0+(x1-x0)*u:.0f},{ya0+(yb0-ya0)*u-3:.1f} q{r.uniform(10,30):.0f},{-2:.0f} {r.uniform(30,60):.0f},0" stroke="#5E6A3A" stroke-width="4" fill="none" opacity="0.8"/>')   # yosun
        if ends:
            rr = h / n * 0.55; cy = (ya0 + ya1) / 2
            o.append(f'<circle cx="{x0-4}" cy="{cy:.1f}" r="{rr:.1f}" fill="#8A7050" stroke="{INK}" stroke-width="3"/><circle cx="{x0-4}" cy="{cy:.1f}" r="{rr*0.55:.1f}" fill="none" stroke="#5A4630" stroke-width="1.5"/>')
    o.append(f'<path d="M{x0},{y0} L{x1},{y1} L{x1},{y1-h*k_end:.0f} L{x0},{y0-h}" fill="none" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>')
    return "".join(o)

def poor_hut(x, y, s=1.0, seed=1, collapsed=False, smoke=True, gw=300, h=118, L=250, rh=150):
    """Doğu kulübesi: kütük duvar, sarkık ve yamalı saz çatı (iple bağlı yamalar, delik, çatıyı tutan sırıklar), eğri kapı + deri perde.
    collapsed=True: sırt ortadan kırık, saz içeri çökmüş, kırık mertekler dışarı fırlamış, yan duvarın üst kütükleri yerde."""
    r = R(seed); k = 0.84; dy = -L * 0.2
    FL, FR = (0, 0), (gw, 0); BR = (gw + L, dy)
    A = (gw / 2, -h - rh); BA = (gw / 2 + L, dy - (h + rh) * k)
    FRt = (gw, -h); BRt = (gw + L, dy - h * k)
    ov = 34
    o = [f'<g transform="translate({x},{y}) scale({s})">',
         f'<ellipse cx="{gw/2+L*0.5:.0f}" cy="10" rx="{(gw+L)*0.62:.0f}" ry="26" fill="#000" opacity="0.32" filter="url(#b6)"/>']
    # yan duvar
    o.append(log_wall(gw, 0, BR[0], BR[1], h, 6, seed + 1, k_end=k, col="#4A3A28", ends=False, missing=((4, 5) if collapsed else ())))
    o.append(f'<path d="M{gw},0 L{BR[0]},{BR[1]} L{BR[0]},{BR[1]-h*k:.0f} L{gw},{-h}" fill="#0E1A24" opacity="0.32"/>')   # yan gölgede
    # ön duvar
    o.append(log_wall(0, 0, gw, 0, h, 6, seed + 2, col="#5E4A34"))
    # alın üçgeni: aralıklı dikey tahtalar, arası karanlık
    gab = f"M0,{-h} L{gw},{-h} L{A[0]},{A[1]} Z"
    o.append(f'<path d="{gab}" fill="#140E08"/>')
    for i in range(7):
        u0, u1 = i / 7 + 0.012, (i + 1) / 7 - 0.012
        xa, xb = gw * u0, gw * u1
        top = lambda xx: -h - rh * (1 - abs(2 * xx / gw - 1))
        if collapsed and i in (5, 6): continue
        o.append(f'<path d="M{xa:.0f},{-h} L{xa:.0f},{top(xa):.0f} L{xb:.0f},{top(xb):.0f} L{xb:.0f},{-h} Z" fill="{r.choice(["#5A4630", "#4E3C28", "#66503A"])}" stroke="{INK}" stroke-width="2.5" {O7.T("ahsap", 0.5)}/>')
    o.append(f'<path d="{gab}" fill="none" stroke="{INK}" stroke-width="5"/>')
    # kapı: eğri, deri perde yarım açık; eşikte çamur
    dx0, dw, dh = gw * 0.36, gw * 0.3, h * 0.86
    o.append(f'<path d="M{dx0},2 L{dx0+4},{-dh} L{dx0+dw},{-dh-6} L{dx0+dw-2},2 Z" fill="#0A0604" stroke="{INK}" stroke-width="5"/>'
             f'<path d="M{dx0+6},{-dh+4} Q{dx0+dw*0.4:.0f},{-dh*0.5:.0f} {dx0+dw*0.18:.0f},0 L{dx0+4},0 Z" fill="#7A6448" stroke="{INK}" stroke-width="3.5"/>'
             f'<path d="M{dx0+10},{-dh+10} Q{dx0+dw*0.3:.0f},{-dh*0.5:.0f} {dx0+dw*0.14:.0f},-8" stroke="#5A4630" stroke-width="2" fill="none"/>'
             f'<path d="M{dx0-10},{-dh-14} L{dx0+dw+10},{-dh-20}" stroke="{INK}" stroke-width="14"/><path d="M{dx0-10},{-dh-14} L{dx0+dw+10},{-dh-20}" stroke="#6A5236" stroke-width="8"/>')
    # küçük pencere: içine paçavra tıkanmış
    o.append(f'<path d="M{gw*0.78:.0f},{-h*0.62:.0f} l34,-2 l1,26 l-34,2 Z" fill="#100A06" stroke="{INK}" stroke-width="4"/><path d="M{gw*0.79:.0f},{-h*0.56:.0f} q14,-10 30,4 q-10,10 -28,6 Z" fill="#8A7E66" stroke="{INK}" stroke-width="2.5"/>')
    # çatı (yan yüz): sarkık sırt, yırtık saçak
    sag = 190 if collapsed else 26
    mid = ((A[0] + BA[0]) / 2, (A[1] + BA[1]) / 2 + sag)
    eF = (FRt[0] + ov, FRt[1] + ov * 0.7); eB = (BRt[0] + ov * 0.7, BRt[1] + ov * 0.5)
    eM = ((eF[0] + eB[0]) / 2, (eF[1] + eB[1]) / 2 + (40 if collapsed else 10))
    rag = " ".join(f"L{eB[0] + (eF[0]-eB[0])*t:.0f},{eB[1] + (eF[1]-eB[1])*t + (eM[1]-(eF[1]+eB[1])/2)*math.sin(math.pi*t)*2 + r.uniform(-4, 12):.0f}" for t in [i / 16 for i in range(17)])
    roof = f"M{A[0]},{A[1]-6} Q{mid[0]:.0f},{mid[1]*2-(A[1]+BA[1])/2:.0f} {BA[0]:.0f},{BA[1]-4:.0f} L{eB[0]:.0f},{eB[1]:.0f} {rag} Z"
    o.append(f'<path d="{roof}" fill="#7E6A44"/>')
    def rp(u, v):   # çatı düzlemi: u boy (ön→arka), v saçaktan sırta
        ex_, ey_ = eF[0] + (eB[0] - eF[0]) * u, eF[1] + (eB[1] - eF[1]) * u + (eM[1] - (eF[1] + eB[1]) / 2) * math.sin(math.pi * u) * 2
        rx_, ry_ = A[0] + (BA[0] - A[0]) * u, A[1] + (BA[1] - A[1]) * u + sag * 2 * math.sin(math.pi * u) * (1 - 0.5 * 0)
        ry_ = A[1] + (BA[1] - A[1]) * u + (2 * sag) * u * (1 - u) * 2
        return ex_ + (rx_ - ex_) * v, ey_ + (ry_ - ey_) * v
    inner = [f'<rect x="-100" y="{A[1]-100:.0f}" width="{gw+L+200}" height="{h+rh+200}" filter="url(#nz_d)" opacity="0.5"/>']
    for i in range(int(L * 1.6)):   # saz lifleri: saçaktan sırta
        u = r.uniform(0, 1); v0 = r.uniform(0, 0.9); v1 = min(1, v0 + r.uniform(0.08, 0.25))
        (ax_, ay_), (bx_, by_) = rp(u, v0), rp(u + r.uniform(-0.02, 0.02), v1)
        inner.append(f'<path d="M{ax_:.0f},{ay_:.0f} L{bx_:.0f},{by_:.0f}" stroke="{r.choice(["#5A4A2C", "#9A8458", "#6E5A36", "#B09A6A"])}" stroke-width="{r.uniform(1.5,3.2):.1f}" opacity="0.85"/>')
    # yamalar: farklı tonda saz kareleri + çapraz ip
    for (u0, v0, du, dv, tone) in ((0.12, 0.25, 0.22, 0.3, "#A89060"), (0.55, 0.15, 0.2, 0.25, "#6A5A3A"), (0.38, 0.6, 0.18, 0.22, "#8E7A4E")):
        q = [rp(u0, v0), rp(u0 + du, v0 - 0.02), rp(u0 + du + 0.01, v0 + dv), rp(u0 - 0.01, v0 + dv + 0.02)]
        inner.append(f'<path d="{P(q)} Z" fill="{tone}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
                     + "".join(f'<path d="M{rp(u0+du*a_,v0)[0]:.0f},{rp(u0+du*a_,v0)[1]:.0f} L{rp(u0+du*a_+0.02,v0+dv)[0]:.0f},{rp(u0+du*a_+0.02,v0+dv)[1]:.0f}" stroke="#4A3A22" stroke-width="2" opacity="0.7"/>' for a_ in (0.2, 0.4, 0.6, 0.8))
                     + f'<path d="M{q[0][0]:.0f},{q[0][1]:.0f} L{q[2][0]:.0f},{q[2][1]:.0f} M{q[1][0]:.0f},{q[1][1]:.0f} L{q[3][0]:.0f},{q[3][1]:.0f}" stroke="#C8B48A" stroke-width="3"/>')
    if not collapsed:   # delik: karanlık iç, kenarı saçaklı; duman buradan
        hx_, hy_ = rp(0.72, 0.62)
        inner.append(f'<ellipse cx="{hx_:.0f}" cy="{hy_:.0f}" rx="26" ry="12" fill="#120C06" stroke="#5A4A2C" stroke-width="4" stroke-dasharray="4 3"/>')
    for i in range(int(L / 18)):   # yosun lekeleri
        u, v = r.uniform(0, 1), r.uniform(0, 0.5); px_, py_ = rp(u, v)
        inner.append(f'<ellipse cx="{px_:.0f}" cy="{py_:.0f}" rx="{r.uniform(8,22):.0f}" ry="{r.uniform(3,7):.0f}" fill="#4E5A30" opacity="0.6"/>')
    inner.append(f'<path d="M{eF[0]:.0f},{eF[1]:.0f} L{eB[0]:.0f},{eB[1]:.0f} L{eB[0]:.0f},{eB[1]+60:.0f} L{eF[0]:.0f},{eF[1]+60:.0f} Z" fill="#000" opacity="0"/>')
    inner.append(f'<path d="M{A[0]},{A[1]} L{BA[0]},{BA[1]} L{BA[0]},{BA[1]+40} L{A[0]},{A[1]+40} Z" fill="#C8B888" opacity="0.25"/>')   # sırtta ışık
    o.append(clipped(f"rf{seed}", roof, "".join(inner)))
    o.append(f'<path d="{roof}" fill="none" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>')
    o.append("".join(f'<path d="M{eB[0] + (eF[0]-eB[0])*t:.0f},{eB[1] + (eF[1]-eB[1])*t + (eM[1]-(eF[1]+eB[1])/2)*math.sin(math.pi*t)*2:.0f} l{r.uniform(-4,4):.0f},{r.uniform(14,34):.0f}" stroke="{r.choice(["#6E5A36", "#9A8458"])}" stroke-width="2.5"/>' for t in [i / 40 for i in range(41)]))   # sarkan saz uçları
    # çatıyı tutan sırıklar (bağlı)
    for u in ((0.2, 0.8) if not collapsed else (0.15,)):
        (ax_, ay_), (bx_, by_) = rp(u, -0.05), rp(u + 0.02, 1.02)
        o.append(f'<path d="M{ax_:.0f},{ay_:.0f} L{bx_:.0f},{by_-8:.0f}" stroke="{INK}" stroke-width="11" stroke-linecap="round"/><path d="M{ax_:.0f},{ay_:.0f} L{bx_:.0f},{by_-8:.0f}" stroke="#6A5236" stroke-width="5" stroke-linecap="round"/>')
    # alın saçağı (ön kenar kalın saz)
    eave = f"M{-ov},{-h+ov*0.7} L{A[0]},{A[1]-12} L{eF[0]:.0f},{eF[1]:.0f} L{eF[0]-8:.0f},{eF[1]+14:.0f} L{A[0]},{A[1]+18} L{-ov+8},{-h+ov*0.7+14} Z"
    o.append(f'<path d="{eave}" fill="#8A7448" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
             + "".join(f'<path d="M{-ov + (A[0]+ov)*t:.0f},{-h+ov*0.7 + (A[1]-12+h-ov*0.7)*t:.0f} l6,16" stroke="#5A4A2C" stroke-width="2.5"/>' for t in [i / 12 for i in range(1, 12)]))
    if collapsed:   # kırık mertekler sırtın çöktüğü yerden fırlar; yan duvarın kütükleri yerde
        for (u, ang, Lr) in ((0.45, -70, 120), (0.55, -40, 100), (0.62, -110, 80)):
            px_, py_ = rp(u, 0.92)
            ex_, ey_ = px_ + Lr * math.cos(math.radians(ang)), py_ + Lr * math.sin(math.radians(ang))
            o.append(f'<path d="M{px_:.0f},{py_:.0f} L{ex_:.0f},{ey_:.0f}" stroke="{INK}" stroke-width="14" stroke-linecap="round"/><path d="M{px_:.0f},{py_:.0f} L{ex_:.0f},{ey_:.0f}" stroke="#6E5638" stroke-width="7" stroke-linecap="round"/>'
                     f'<path d="M{ex_-6:.0f},{ey_:.0f} l6,-10 l4,8 l5,-6" stroke="#C8A878" stroke-width="3" fill="none"/>')
        for i, (lx, ly, la) in enumerate(((gw + 40, 46, 8), (gw + 140, 30, -12), (gw + 220, 54, 4))):
            o.append(f'<g transform="translate({lx},{ly}) rotate({la})"><rect x="-80" y="-11" width="160" height="22" rx="10" fill="#4E3C28" stroke="{INK}" stroke-width="4" {O7.T("ahsap", 0.5)}/>'
                     f'<ellipse cx="80" cy="0" rx="7" ry="11" fill="#8A7050" stroke="{INK}" stroke-width="3"/></g>')
    o.append('</g>')
    return "".join(o)

def goat(x, y, s=1.0, coat="#BEB4A0", dark="#5E5446", flip=1, straw=True):
    """Sıska keçi (profil, sağa bakar): belirgin omurga ve kalça kemiği, kaburga izleri, içe çekik karın; eklemli ince ama doğru bacaklar
    (ön: dirsek-diz-bilek; arka: diz-topuk arkaya), çatal toynak, sakal, geriye kıvrık boynuz, yatay göz bebeği. Ağzında çatıdan çektiği saz."""
    o = [f'<g transform="translate({x},{y}) scale({s*flip},{s})">', '<ellipse cx="-20" cy="4" rx="150" ry="14" fill="#000" opacity="0.38" filter="url(#b4)"/>']
    o.append(oleg([(28, -100), (36, -52), (32, -14), (34, 0)], [20, 10, 8, 8], dark, sw=3.5, bumps=((1, 1, 3),)))        # uzak ön
    o.append(oleg([(-84, -104), (-108, -62), (-96, -14), (-94, 0)], [24, 10, 8, 8], dark, sw=3.5, bumps=((1, -1, 4),)))    # uzak arka
    body = ("M-122,-150 C-112,-160 -98,-166 -86,-160 C-60,-152 0,-154 40,-160 C52,-166 62,-168 72,-162 "
            "C88,-170 104,-178 118,-184 C130,-188 146,-184 160,-176 C176,-168 190,-162 198,-154 C202,-148 198,-140 190,-140 "
            "C180,-140 170,-142 162,-144 C152,-146 144,-148 136,-150 C130,-148 124,-144 120,-138 "
            "C120,-126 118,-114 112,-106 C106,-116 104,-126 102,-134 C92,-128 80,-118 70,-108 C60,-100 54,-98 50,-94 L46,-82 L28,-84 "
            "C10,-96 -20,-102 -50,-106 C-62,-108 -70,-104 -76,-100 C-80,-90 -86,-76 -94,-62 L-118,-58 C-124,-80 -128,-110 -130,-130 C-130,-140 -128,-146 -122,-150 Z")
    o.append(f'<g filter="url(#f_form)"><path d="{body}" fill="{coat}" {O7.T("kurk", 0.3)}/></g>')
    inner = (f'<path d="M-140,-112 C-60,-100 20,-96 80,-110 L90,-60 L-150,-50 Z" fill="{dark}" opacity="0.35"/>'
             f'<path d="M-122,-152 C-90,-166 0,-158 72,-166 L72,-150 C0,-142 -90,-150 -122,-140 Z" fill="#E8E2D2" opacity="0.5"/>'
             f'<rect x="-200" y="-300" width="500" height="400" filter="url(#nz_d)" opacity="0.35"/>'
             f'<path d="M-140,-90 C-100,-96 -60,-100 -20,-100 L-20,-60 L-140,-60 Z" fill="#4A3E30" opacity="0.4"/>')   # çamur sıçramış karın
    o.append(clipped("gt", body, inner))
    o.append(f'<path d="{body}" fill="none" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>')
    # kemik ve kas: omurga dikenleri, kalça kemiği, kaburgalar, kürek kemiği
    o.append("".join(f'<path d="M{-80 + k*16},{-157 - (k%2)} l2,-4" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>' for k in range(9)))
    o.append(f'<path d="M-96,-158 C-90,-150 -92,-140 -100,-134" stroke="{INK}" stroke-width="3.5" fill="none"/>'
             + "".join(f'<path d="M{-30 + k*16},{-148} C{-36 + k*16},{-132} {-34 + k*16},{-118} {-24 + k*16},{-104}" stroke="{dark}" stroke-width="2.5" fill="none" opacity="0.75"/>' for k in range(4))
             + f'<path d="M58,-158 C50,-140 44,-118 46,-100" stroke="{dark}" stroke-width="3" fill="none" opacity="0.8"/>')
    o.append(oleg([(40, -104), (50, -56), (46, -14), (48, 0)], [24, 11, 9, 9], "#9C9486", sw=4, bumps=((1, 1, 3),)))          # yakın ön: dirsek → diz (öne çıkıntı) → bilek
    o.append(oleg([(-96, -100), (-118, -60), (-104, -14), (-102, 0)], [26, 11, 9, 9], "#9C9486", sw=4, bumps=((1, -1, 5),)))   # yakın arka: diz → topuk (arkaya) → bilek
    o.append("".join(f'<path d="M{bx-6},{-22+k*7} q6,3 12,0" stroke="#3A3024" stroke-width="3" fill="none"/>' for bx in (47, -103) for k in range(3)))   # bilekte çamur
    # kuyruk (kısa, kalkık)
    o.append(f'<path d="M-122,-150 C-132,-162 -138,-172 -134,-182 C-126,-174 -120,-164 -116,-154 Z" fill="{coat}" stroke="{INK}" stroke-width="3.5"/>')
    # boynuz: geriye kıvrık, halkalı
    horn = "M122,-184 C112,-206 92,-222 70,-224 C66,-222 66,-216 72,-214 C90,-210 104,-198 112,-180 Z"
    o.append(f'<path d="{horn}" fill="#8A7A60" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>' + "".join(f'<path d="M{110 - k*8},{-196 - k*4} l{-4},{8}" stroke="#4A3E2A" stroke-width="2"/>' for k in range(5)))
    # kulak: yana sarkık
    o.append(f'<path d="M114,-176 C100,-178 86,-170 80,-160 C94,-160 108,-164 118,-168 Z" fill="{coat}" stroke="{INK}" stroke-width="3.5"/><path d="M110,-172 C100,-172 92,-168 86,-163" stroke="#C8A08A" stroke-width="2.5" fill="none"/>')
    # göz: sarı iris, YATAY dikdörtgen göz bebeği (keçi), üst kapak ağır (bıkkın)
    o.append(f'<ellipse cx="140" cy="-170" rx="8" ry="6" fill="#D8B44A" stroke="{INK}" stroke-width="2.5"/><rect x="133" y="-172" width="14" height="4" rx="2" fill="#0A0806"/>'
             f'<path d="M131,-172 C136,-178 146,-178 149,-171" fill="{coat}" stroke="{INK}" stroke-width="3"/>')
    # burun deliği, ağız, sakal
    o.append(f'<path d="M192,-152 q4,-2 4,4" stroke="{INK}" stroke-width="3" fill="none"/><path d="M168,-144 q12,2 22,-2" stroke="{INK}" stroke-width="2.5" fill="none"/>'
             f'<path d="M122,-140 C120,-124 118,-110 110,-100 C116,-104 122,-112 126,-126 Z" fill="#8A806E" stroke="{INK}" stroke-width="3"/>')
    if straw:
        o.append("".join(f'<path d="M{176+k*3},{-144+k} q{30+k*6},{-12-k*3} {70+k*14},{-30-k*8}" stroke="{c_}" stroke-width="3" fill="none"/>' for k, c_ in enumerate(("#B09A6A", "#8A7448", "#C8B07A", "#9A8458"))))
    o.append('</g>'); return "".join(o)

def hen(x, y, s=1.0, flip=1):
    """Cılız tavuk, gagalarken: sivri kemikli göğüs, seyrek tüy, düşük ibik, ince pullu bacak."""
    return (f'<g transform="translate({x},{y}) scale({s*flip},{s})"><ellipse cx="0" cy="2" rx="40" ry="6" fill="#000" opacity="0.3"/>'
            f'<path d="M-6,-30 L-10,-6 L-16,0 M-10,-6 L-2,0 M6,-30 L8,-6 L14,0 M8,-6 L2,0" stroke="#B8943A" stroke-width="3.5" fill="none" stroke-linecap="round"/>'
            f'<path d="M-44,-62 C-40,-72 -30,-70 -26,-60 C-10,-64 10,-56 24,-42 C34,-34 40,-22 44,-12 C40,-14 34,-18 30,-22 C20,-26 0,-26 -14,-28 C-30,-30 -40,-40 -44,-62 Z" fill="#8A6A48" stroke="{INK}" stroke-width="3.5" {O7.T("kurk", 0.3)}/>'
            f'<path d="M-44,-62 L-58,-80 L-50,-60 L-62,-68 L-48,-52" fill="#3A2A1E" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
            f'<path d="M-20,-48 C-6,-52 8,-46 14,-38" stroke="#5A4430" stroke-width="2.5" fill="none"/><path d="M-30,-40 C-14,-42 0,-38 10,-32" stroke="#5A4430" stroke-width="2" fill="none"/>'
            f'<path d="M40,-12 C44,-8 48,-4 50,2 L44,4 C42,-2 38,-6 34,-10 Z" fill="#8A6A48" stroke="{INK}" stroke-width="3"/>'
            f'<path d="M48,0 l10,4 l-10,2 Z" fill="#C8A040" stroke="{INK}" stroke-width="2"/><path d="M42,-6 q4,-6 8,-2" fill="#A83A2A" stroke="{INK}" stroke-width="2"/><circle cx="44" cy="-2" r="1.6" fill="#0A0806"/></g>')

def sack(x, y, s=1.0, rot=0, empty=True, seed=0):
    r = R(seed)
    d = "M-50,0 C-56,-20 -48,-40 -40,-52 C-30,-60 -10,-58 0,-62 C14,-58 30,-62 40,-50 C50,-36 56,-16 52,0 Z" if not empty else "M-60,0 C-62,-10 -56,-20 -44,-24 C-30,-30 -10,-22 0,-28 C14,-22 34,-30 48,-20 C58,-12 62,-6 60,0 Z"
    return (f'<g transform="translate({x},{y}) rotate({rot}) scale({s})"><ellipse cx="4" cy="2" rx="66" ry="8" fill="#000" opacity="0.35"/>'
            f'<path d="{d}" fill="#A8946C" stroke="{INK}" stroke-width="4" {O7.T("keten", 1.0) if False else ""}/>'
            f'<path d="{d}" fill="none" stroke="#6E5E40" stroke-width="1.5" stroke-dasharray="2 4" transform="translate(0,-4) scale(0.92)"/>'
            + "".join(f'<path d="M{r.uniform(-40,40):.0f},{r.uniform(-20,-4):.0f} q{r.uniform(-8,8):.0f},{r.uniform(-8,-2):.0f} {r.uniform(10,22):.0f},{r.uniform(-2,4):.0f}" stroke="#6E5E40" stroke-width="2" fill="none"/>' for _ in range(5))
            + (f'<path d="M52,-18 C66,-30 76,-24 82,-30 L84,-20 C74,-14 64,-18 56,-8 Z" fill="#A8946C" stroke="{INK}" stroke-width="3"/>' if empty else "")
            + '</g>')

def puddle(cx, cy, rx, ry, seed, sky_top="#9EA4A0", sky_bot="#6E7470", reflect=""):
    r = R(seed); pts = [(cx + rx * math.cos(a) * r.uniform(0.8, 1.1), cy + ry * math.sin(a) * r.uniform(0.8, 1.15)) for a in [i / 12 * 2 * math.pi for i in range(12)]]
    d = smooth(pts, closed=True); gid = f"pd{seed}"
    return (f'<defs><linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{sky_bot}"/><stop offset="1" stop-color="{sky_top}"/></linearGradient></defs>'
            f'<path d="{d}" fill="#2A241C" transform="translate(0,3)"/><path d="{d}" fill="url(#{gid})"/>'
            + clipped(f"pc{seed}", d, reflect + "".join(f'<path d="M{cx - rx*0.7 + r.uniform(0, rx*1.2):.0f},{cy + r.uniform(-ry*0.5, ry*0.5):.0f} h{r.uniform(10, rx*0.5):.0f}" stroke="#D8DCD6" stroke-width="2" opacity="0.6"/>' for _ in range(5)))
            + f'<path d="{d}" fill="none" stroke="#3A3226" stroke-width="3.5"/>')

def footprints(pts, kind="boot", s=1.0, seed=0):
    r = R(seed); o = []
    for i, (x, y) in enumerate(pts):
        q = s * (0.5 + (y - 700) / 600)
        side = (-1) ** i
        if kind == "boot":
            o.append(f'<ellipse cx="{x + side*10*q:.0f}" cy="{y:.0f}" rx="{16*q:.1f}" ry="{7*q:.1f}" fill="#1E1810" opacity="0.9"/><ellipse cx="{x + side*10*q:.0f}" cy="{y-1:.0f}" rx="{12*q:.1f}" ry="{3.5*q:.1f}" fill="#6E7470" opacity="0.7"/>')
        else:   # keçi: çatal toynak izi
            o.append(f'<path d="M{x-4*q:.0f},{y:.0f} q{-3*q:.1f},{-6*q:.1f} 0,{-8*q:.1f} q{2*q:.1f},{4*q:.1f} 0,{8*q:.1f} Z M{x+3*q:.0f},{y:.0f} q{3*q:.1f},{-6*q:.1f} 0,{-8*q:.1f} q{-2*q:.1f},{4*q:.1f} 0,{8*q:.1f} Z" fill="#241C14"/>')
    return "".join(o)

def bog_ground(y0=740, seed=31):
    """Bataklık zemini: koyu ıslak çamur, düşük frekans leke, saz/ayak otu öbekleri, pamuk otu, gökyüzünü yansıtan su birikintileri, batmış kalaslar."""
    r = R(seed)
    gp = f"M0,{y0} Q500,{y0-16} 960,{y0-6} Q1400,{y0+4} {W},{y0-12} L{W},{H} L0,{H} Z"
    o = [f'<path d="{gp}" fill="#4A4232"/>']
    inner = [f'<rect width="{W}" height="{H}" filter="url(#mudn)"/>', f'<rect width="{W}" height="{H}" filter="url(#nz_d)" opacity="0.7"/>',
             f'<rect width="{W}" height="{H}" filter="url(#nz_f)" opacity="0.6"/>',
             f'<rect x="0" y="{y0}" width="{W}" height="80" fill="#6E6A58" opacity="0.5" filter="url(#b18)"/>']
    for k in range(18):   # ıslak koyu lekeler + açık kuru tümsekler
        x = r.uniform(0, W); y = r.uniform(y0 + 30, H); q = (y - y0) / (H - y0)
        inner.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{(60+200*q)*r.uniform(0.6,1.2):.0f}" ry="{(8+30*q)*r.uniform(0.6,1.2):.0f}" fill="{r.choice(["#2E281E", "#6A6450"])}" opacity="0.45" filter="url(#b8)"/>')
    o.append(clipped("bog", gp, "".join(inner)))
    o.append(f'<path d="M0,{y0} Q500,{y0-16} 960,{y0-6} Q1400,{y0+4} {W},{y0-12}" stroke="#2A241C" stroke-width="3" fill="none" opacity="0.6"/>')
    return "".join(o)

def sedge(x, y, h, seed, cotton=False, col="#7A7448", dark="#3E3A24"):
    r = R(seed); o = [f'<ellipse cx="{x}" cy="{y+2}" rx="{h*0.45:.0f}" ry="{h*0.1:.0f}" fill="#2A241A"/>']
    for i in range(int(14 + h / 6)):
        a = r.uniform(-1.0, 1.0); hh = h * r.uniform(0.5, 1.0); bx = x + r.uniform(-h * 0.3, h * 0.3)
        ex_, ey_ = bx + math.sin(a) * hh, y - hh * math.cos(a * 0.8)
        o.append(f'<path d="M{bx:.0f},{y} Q{bx + math.sin(a)*hh*0.3:.0f},{y-hh*0.7:.0f} {ex_:.0f},{ey_:.0f}" stroke="{r.choice([col, dark, "#9A8E5A", "#5E5A36"])}" stroke-width="{max(1.5, h/28):.1f}" fill="none" stroke-linecap="round"/>')
        if cotton and r.random() < 0.15:
            o.append(f'<circle cx="{ex_:.0f}" cy="{ey_-4:.0f}" r="{max(3, h/16):.1f}" fill="#E8E6DC" stroke="#8A8676" stroke-width="1.2"/>')
    return "".join(o)

def f3():
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    D = DEFS()
    # ---- 1 kapalı gök: alçak, katman katman, donuk; ufukta soluk ışık şeridi
    o = [D, sky_grad("sk3", [(0, "#5E625C"), (0.45, "#8A8C82"), (0.7, "#AEAC9C"), (0.78, "#B8B4A0")]), f'<rect width="{W}" height="{H}" fill="url(#sk3)"/>',
         f'<rect width="{W}" height="760" filter="url(#nz_sky)" opacity="0.18"/>']
    o.append(stratus(130, 71, "#82847A", "#3E4038", n=8, thick=80, blur=5) + stratus(260, 72, "#94948A", "#52544C", n=8, thick=60, blur=3)
             + stratus(390, 73, "#9C9A8E", "#6E6E64", n=8, thick=40, blur=3) + stratus(480, 74, "#A8A698", "#80806E", n=6, thick=26, blur=3))
    o.append("".join(f'<path d="M{x},{470 + (x*7)%40} l-30,140" stroke="#6E7068" stroke-width="26" opacity="0.18" filter="url(#b12)"/>' for x in range(1300, 1900, 50)))   # uzakta yağmur saçağı
    o.append(raven(1260, 250, 0.16, pose="fly", seed=8) + raven(1310, 232, 0.13, pose="fly", seed=9))
    draw(c, svg_sprite("".join(o)), 0, 0, 1.0)
    # ---- 2 uzak: sisli düz bataklık ufku, seyrek cılız ağaçlar, uzaktaki üçüncü yıkık kulübe
    o = [D, f'<path d="M0,600 Q400,588 900,596 Q1400,604 {W},590 L{W},760 L0,760 Z" fill="#7E7E6E"/>']
    for k in range(28):
        rr_ = R(500 + k); x = rr_.uniform(0, W); hh = rr_.uniform(40, 120)
        o.append(spruce(x, 600 + rr_.uniform(-4, 8), hh, 600 + k, col="#6A6E62", lit="#7E8274", dark="#5E6258") if k % 3 else birch(x, 604, hh * 1.3, 700 + k, sc=0.8, ink="#5E6056"))
    o.append(f'<rect width="{W}" height="{H}" fill="#9A9A8C" opacity="0.45"/>')
    o.append(f'<g opacity="0.6">{poor_hut(1600, 640, 0.42, seed=40, collapsed=True)}</g>')
    o.append(f'<g opacity="0.7">{poor_hut(130, 660, 0.36, seed=41)}</g>')
    draw(c, svg_sprite("".join(o)), 0, 0, 1.0)
    fog(c, 0, 600, "#C8C8BA", 0.6, n=8, seed=21, speed=0, h=70)
    # ---- 3 zemin + orta plan: iki kulübe, sundurma, çuvallar, çit
    o = [D, O7.MUD_DEFS, bog_ground(700)]
    o.append(puddle(1000, 960, 210, 34, 1, reflect=f'<path d="M900,940 l40,-30 l30,30 Z" fill="#4A4232" opacity="0.5"/>') + puddle(420, 870, 120, 18, 2) + puddle(1620, 880, 150, 22, 3) + puddle(760, 790, 80, 10, 4))
    o.append(footprints([(540 + i * 40, 1000 - i * 24) for i in range(9)], "boot", 1.6, 1) + footprints([(780 + i * 26, 880 - i * 10) + () for i in range(10)], "goat", 1.2, 2))
    for (bx, by, ba, bl) in ((640, 900, -4, 220), (860, 930, 6, 200), (1080, 900, -9, 180)):   # batmış kalas yolu
        o.append(f'<g transform="translate({bx},{by}) rotate({ba})"><rect x="{-bl/2}" y="-12" width="{bl}" height="24" rx="4" fill="#5A4834" stroke="{INK}" stroke-width="4" {O7.T("ahsap", 0.5)}/>'
                 f'<rect x="{-bl/2}" y="2" width="{bl}" height="10" fill="#3A3024" opacity="0.7"/><path d="M{-bl/2+10},-6 h{bl*0.6:.0f}" stroke="#8A7458" stroke-width="2"/></g>')
    # sol kulübe ("fakir"): sundurma + boş çuvallar + balık kurutma çubuğu
    o.append(f'<path d="M150,760 L176,620 M340,770 L330,640" stroke="{INK}" stroke-width="14" stroke-linecap="round"/><path d="M150,760 L176,620 M340,770 L330,640" stroke="#5A4630" stroke-width="7" stroke-linecap="round"/>'
             f'<path d="M140,620 L360,632 L420,588 L210,574 Z" fill="#6A5E46" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
             + "".join(f'<path d="M{150+k*22},{620+k*1.2:.0f} L{214+k*21},{575+k*1.4:.0f}" stroke="#4A3E2C" stroke-width="4"/>' for k in range(10)))
    o.append(sack(210, 770, 0.9, -4, True, 1) + sack(300, 780, 0.8, 6, True, 2))
    o.append(poor_hut(360, 790, 1.0, seed=11, collapsed=False))
    o.append(smoke_col(360 + 300 + 250 * 0.72 * 0.95 - 120, 600, 240, 77, a=0.4, col="#C8C8BC", drift=1.6))
    o.append(poor_hut(1150, 770, 0.95, seed=22, collapsed=True))
    # kırık çit: eğik kazıklar, sarkık dal; tersyüz çuval kazığa asılı
    for i, (px, py, ln) in enumerate(((1560, 830, 0.12), (1640, 834, -0.08), (1720, 840, 0.22), (1800, 846, -0.15), (1880, 852, 0.3))):
        o.append(post(px, py, 120 - i * 6, w=16, seed=300 + i, lean=ln))
    o.append(f'<path d="M1562,750 Q1600,780 1642,744 Q1680,770 1720,766" stroke="{INK}" stroke-width="8" fill="none"/><path d="M1562,750 Q1600,780 1642,744 Q1680,770 1720,766" stroke="#6A5A40" stroke-width="4" fill="none"/>')
    o.append(f'<g transform="translate(1806,744) rotate(-12)"><path d="M-10,0 C-30,10 -34,50 -24,80 C-6,90 16,88 26,76 C34,50 28,12 10,0 Z" fill="#A8946C" stroke="{INK}" stroke-width="4"/><path d="M-20,30 q14,8 36,0 M-18,56 q14,6 30,-2" stroke="#6E5E40" stroke-width="2" fill="none"/><path d="M-6,84 l4,14 l6,-12" stroke="#A8946C" stroke-width="4" fill="none"/></g>')
    # sağ orta planda ölü huş + üstünde karga
    o.append(birch(1700, 846, 440, 81, lean=-0.04, sc=1.0))
    o.append(raven(1680, 846 - 440 + 16 - 50 * 0.32, 0.32, flip=-1, seed=2))
    o.append(sedge(560, 860, 70, 1, cotton=True) + sedge(1340, 830, 60, 2, cotton=True) + sedge(1500, 950, 90, 3, cotton=True) + sedge(260, 900, 80, 4))
    # balık kurutma: iki çatal direk + sırık + iki minicik balık
    o.append(f'<path d="M560,870 L566,720 M690,876 L682,724" stroke="{INK}" stroke-width="12" stroke-linecap="round"/><path d="M560,870 L566,720 M690,876 L682,724" stroke="#5A4630" stroke-width="6" stroke-linecap="round"/>'
             f'<path d="M550,730 L700,734" stroke="{INK}" stroke-width="10" stroke-linecap="round"/><path d="M550,730 L700,734" stroke="#6A5236" stroke-width="5" stroke-linecap="round"/>'
             + "".join(f'<g transform="translate({x},736)"><path d="M0,0 v8" stroke="#4A3A28" stroke-width="2"/><path d="M0,8 C6,12 6,30 0,38 C-6,30 -6,12 0,8 Z M0,38 l-6,10 l12,0 Z" fill="#8A8A7E" stroke="{INK}" stroke-width="2.5"/><circle cx="0" cy="14" r="1.5" fill="#000"/></g>' for x in (606, 642)))
    o.append(hen(700, 905, 1.35, flip=-1))
    o.append(goat(905, 830, 1.15))
    draw(c, svg_sprite("".join(o)), 0, 0, 1.0)
    fog(c, 0, 760, "#C8C8BA", 0.22, n=6, seed=23, speed=0, h=40)
    # ---- 4 ön plan: büyük ölü huş (sol, keskin), bulanık saz öbekleri (alt köşeler)
    draw(c, blurred(svg_sprite(D + birch(60, 1100, 1000, 91, lean=0.03, sc=1.0) + sedge(170, 1090, 120, 7, cotton=True)), 2), 0, 0, 1.0)
    fgb = svg_sprite(D + sedge(1780, 1110, 230, 8, cotton=True) + sedge(1600, 1120, 170, 9) + post(1900, 1120, 380, w=40, seed=401, lean=-0.12))
    draw(c, blurred(fgb, 7), 0, 0, 1.0)
    # ---- ışık: donuk, sol üstten; ufukta soluk bant, figürlere yumuşak rim
    light_shaft(c, 300, 300, 600, 500, "#E8E4D0", 0.10, t=0, y_top=60, y_bot=1000)
    gradient_grade(c, "#5A6A50", "#3A3428", 0.25, "soft")
    grade(c, "#B8B49C", 0.10, "multiply")
    card_at(c, "DOĞU", 960, 120)
    card_at(c, "FAKİR KÖY", 520, 420, "", 0.62)
    card_at(c, "BİRAZ DAHA FAKİR KÖY", 1250, 420, "", 0.55)
    finish(c, cold=False); return s


# ======================================================================= f4 · açık deniz: ne harita ne pusula
HZ = 600

def sea_rows(seed=5, glint=(1120, 300)):
    """Katmanlı ölü dalga (swell): ufukta sık-soluk, yakında iri-koyu; tepelerde köpük başlığı, yüzlerde köpük dantelası,
    ışık lekesinde parıltı. Arkadan öne çizilir; her sıra alttaki sıraları örter."""
    r = R(seed); o = []; N = 22
    for i in range(N):
        q = (i / (N - 1)); y = HZ + 4 + (q ** 1.9) * 430
        lam = 40 + 380 * q ** 1.4; A = 2 + 46 * q ** 1.6; ph = r.uniform(0, 6.28); ph2 = r.uniform(0, 6.28)
        pts = []
        for x in range(-40, W + 60, max(6, int(lam / 14))):
            grp = 0.45 + 0.35 * math.sin(x / (lam * 3.3) + ph2) + 0.2 * math.sin(x / (lam * 1.7) + ph2 * 2.1)
            f = (1 - abs(math.sin(math.pi * x / lam + ph))) ** 1.6 + 0.25 * math.sin(x / (lam * 0.61) + ph * 1.7)
            pts.append((x, y - A * grp * f + A * 0.25))
        col = (int(0x7A - 0x52 * q), int(0x8C - 0x56 * q), int(0x98 - 0x52 * q))
        hexc = "#%02X%02X%02X" % col
        d = "M" + " L".join(f"{x},{yy:.1f}" for x, yy in pts) + f" L{W+60},{H+40} L-40,{H+40} Z"
        gid = f"sw{i}"
        o.append(f'<defs><linearGradient id="{gid}" x1="0" y1="{y-A:.0f}" x2="0" y2="{y+A*2+30:.0f}" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="{hexc}"/><stop offset="1" stop-color="#1A2A34"/></linearGradient></defs>')
        o.append(f'<path d="{d}" fill="url(#{gid})"/>')
        # tepe çizgisi (gökten ışık) + gölge kenarı
        crest = "M" + " L".join(f"{x},{yy:.1f}" for x, yy in pts)
        o.append(f'<path d="{crest}" stroke="#C8D6DE" stroke-width="{0.8 + 2.2*q:.1f}" fill="none" opacity="{0.18 + 0.3*q*q:.2f}"/>')
        if q > 0.3: o.append(f'<path d="{crest}" transform="translate(0,{3+6*q:.0f})" stroke="#0E1A22" stroke-width="{1+3*q:.1f}" fill="none" opacity="0.35"/>')
        # köpük başlıkları: tepelerde, düzensiz
        for j, (x, yy) in enumerate(pts[1:-1], 1):
            if pts[j - 1][1] > yy < pts[j + 1][1] and r.random() < 0.15 + 0.6 * q:
                fw = lam * r.uniform(0.08, 0.22); fh = 2 + A * 0.18
                o.append(f'<path d="M{x-fw:.0f},{yy+fh*0.6:.0f} Q{x-fw*0.4:.0f},{yy-fh:.0f} {x+fw*0.1:.0f},{yy-fh*0.3:.0f} Q{x+fw*0.6:.0f},{yy+fh*0.2:.0f} {x+fw:.0f},{yy+fh:.0f} Q{x:.0f},{yy+fh*0.5:.0f} {x-fw:.0f},{yy+fh*0.6:.0f} Z" fill="#E8F0F2" opacity="{0.55 + 0.4*q:.2f}"/>')
                if q > 0.45:   # köpük dantelası: tepeden yüz boyunca yatay-çapraz uzanan ince şeritler
                    for k in range(2):
                        lx = x + r.uniform(-fw, fw); ll = lam * r.uniform(0.2, 0.45); dyy = A * r.uniform(0.3, 0.9)
                        o.append(f'<path d="M{lx:.0f},{yy+fh+dyy*0.2:.0f} q{ll*0.5:.0f},{dyy*0.5:.0f} {ll:.0f},{dyy:.0f}" stroke="#D8E4EA" stroke-width="{1+q*1.2:.1f}" fill="none" opacity="0.35" stroke-dasharray="{6+q*10:.0f} {4+q*6:.0f}"/>')
        # ışık lekesinde parıltı
        gx, gw = glint
        if q < 0.55:
            for k in range(int(20 * (1 - q))):
                x = r.gauss(gx, gw * (0.4 + q)); yy = y - r.uniform(0, A)
                o.append(f'<path d="M{x:.0f},{yy:.0f} h{r.uniform(4, 14 + 30*q):.0f}" stroke="#FFF6DC" stroke-width="{1+q*2:.1f}" opacity="{r.uniform(0.5,0.95):.2f}"/>')
    return "".join(o)

def big_wave(x0, y0, w, h, seed=9):
    """Ön plan: kadrajı çerçeveleyen iri, koyu dalga sırtı; tepede yırtık köpük şeridi ve rüzgârla savrulan serpinti; içinden geçen camgöbeği ışık."""
    r = R(seed); o = []
    top = [(x0 + w * t, y0 - h * (math.sin(math.pi * min(1.0, t * 1.15)) ** 1.3) * (1 - 0.35 * t) + r.uniform(-4, 4)) for t in [i / 30 for i in range(31)]]
    d = "M" + " L".join(f"{x:.0f},{y:.0f}" for x, y in top) + f" L{x0+w},{H+40} L{x0},{H+40} Z"
    o.append(f'<defs><linearGradient id="bw{seed}" x1="0" y1="{y0-h}" x2="0" y2="{H}" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#2E4A56"/><stop offset="0.3" stop-color="#1A2E3A"/><stop offset="1" stop-color="#0A141A"/></linearGradient></defs>')
    o.append(f'<path d="{d}" fill="url(#bw{seed})"/>')
    o.append(clipped(f"bwc{seed}", d, f'<ellipse cx="{x0+w*0.45:.0f}" cy="{y0-h*0.45:.0f}" rx="{w*0.3:.0f}" ry="{h*0.25:.0f}" fill="#4E8A92" opacity="0.45" filter="url(#b18)"/>'
                                     + "".join(f'<path d="M{x0 + r.uniform(0, w*0.8):.0f},{y0 - r.uniform(-60, h*0.6):.0f} q{r.uniform(60,120):.0f},{r.uniform(-10,10):.0f} {r.uniform(140,260):.0f},{r.uniform(10,30):.0f}" stroke="#B8CCD2" stroke-width="{r.uniform(2,4):.1f}" fill="none" opacity="0.35" stroke-dasharray="14 8"/>' for _ in range(16))))
    foam = " ".join(f"L{x:.0f},{y + r.uniform(-6, 4):.0f}" for x, y in top[2:24])
    foam_b = " ".join(f"L{x:.0f},{y + 14 + r.uniform(0, 26):.0f}" for x, y in reversed(top[2:24]))
    o.append(f'<path d="M{top[2][0]:.0f},{top[2][1]:.0f} {foam} {foam_b} Z" fill="#DCE8EC" opacity="0.92"/>')
    for k in range(90):   # savrulan serpinti (rüzgâr sağa)
        i = r.randrange(3, 24); x, y = top[i][0] + r.uniform(0, 80), top[i][1] - r.uniform(5, 110)
        o.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r.uniform(1.5,6):.1f}" fill="#E6EEF0" opacity="{r.uniform(0.4,0.9):.2f}"/>')
    o.append(f'<g filter="url(#b8)">' + "".join(f'<ellipse cx="{top[i][0]+40:.0f}" cy="{top[i][1]-30:.0f}" rx="60" ry="18" fill="#E6EEF0" opacity="0.35"/>' for i in range(4, 22, 3)) + '</g>')
    return "".join(o)

def fg_swell(seed=9):
    """Ön plan: tüm genişlikte iri, koyu dalga sırtı (kadrajın altını çerçeveler); düzensiz tepeler, tepede yırtık köpük, savrulan serpinti."""
    r = R(seed); o = []
    pts = []
    for x in range(-40, W + 60, 20):
        f = (0.5 + 0.5 * math.cos(2 * math.pi * x / 1100 + 0.9)) ** 1.6 + 0.12 * math.sin(x / 90)
        pts.append((x, 1000 - 150 * f + r.uniform(-2, 2)))
    d = "M" + " L".join(f"{x},{y:.0f}" for x, y in pts) + f" L{W+60},{H+40} L-40,{H+40} Z"
    o.append(f'<defs><linearGradient id="fgs" x1="0" y1="860" x2="0" y2="{H}" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#22404C"/><stop offset="0.35" stop-color="#122028"/><stop offset="1" stop-color="#070E12"/></linearGradient></defs>')
    o.append(f'<path d="{d}" fill="url(#fgs)"/>')
    o.append(clipped("fgsc", d, "".join(f'<ellipse cx="{x:.0f}" cy="{y+40:.0f}" rx="120" ry="40" fill="#3E7A84" opacity="0.35" filter="url(#b12)"/>' for x, y in pts[::8] if y < 960)
                     + "".join(f'<path d="M{r.uniform(0,W):.0f},{r.uniform(940,1080):.0f} q{r.uniform(60,140):.0f},{r.uniform(-8,8):.0f} {r.uniform(160,300):.0f},{r.uniform(4,20):.0f}" stroke="#A8C0C8" stroke-width="{r.uniform(2,4):.1f}" fill="none" opacity="0.3" stroke-dasharray="16 9"/>' for _ in range(22))))
    for j in range(1, len(pts) - 1):
        x, y = pts[j]
        if pts[j - 1][1] >= y <= pts[j + 1][1] and y < 900:
            fw = 150 + (960 - y) * 0.9
            band = [(xx, yy) for xx, yy in pts if abs(xx - x) < fw]
            top = " ".join(f"L{xx:.0f},{yy - 3 + r.uniform(-4, 3):.0f}" for xx, yy in band)
            bot = " ".join(f"L{xx:.0f},{yy + 8 + r.uniform(0, 12) * (1 - abs(xx - x) / fw):.0f}" for xx, yy in reversed(band))
            o.append(f'<path d="M{band[0][0]:.0f},{band[0][1]:.0f} {top} {bot} Z" fill="#DCE8EC" opacity="0.9"/>')
            for k in range(3):   # tepeden yüze dökülen köpük
                sx = x + r.uniform(-fw * 0.6, fw * 0.6); sy = y + 10
                o.append(f'<path d="M{sx:.0f},{sy:.0f} q{r.uniform(10,40):.0f},{r.uniform(20,40):.0f} {r.uniform(30,80):.0f},{r.uniform(50,90):.0f}" stroke="#C8D8DE" stroke-width="{r.uniform(3,6):.1f}" fill="none" opacity="0.5" stroke-linecap="round"/>')
            for k in range(30):
                o.append(f'<circle cx="{x + r.uniform(-fw, fw*1.5):.0f}" cy="{y - r.uniform(4, 80):.0f}" r="{r.uniform(1.5, 5):.1f}" fill="#E6EEF0" opacity="{r.uniform(0.4, 0.9):.2f}"/>')
    return "".join(o)

def parchment(x, y, w, h, inner, seed, rot=-3):
    """Yırtık kenarlı parşömen parçası: eskimiş leke, kıvrık köşe, raptiye; içine mürekkep çizim; kırmızı fırça X."""
    r = R(seed); pts = []
    for i in range(10): pts.append((-w / 2 + w * i / 9, -h / 2 + r.uniform(-5, 5)))
    for i in range(1, 7): pts.append((w / 2 + r.uniform(-5, 5), -h / 2 + h * i / 6))
    for i in range(1, 10): pts.append((w / 2 - w * i / 9, h / 2 + r.uniform(-6, 6)))
    for i in range(1, 6): pts.append((-w / 2 + r.uniform(-5, 5), h / 2 - h * i / 6))
    d = P(pts) + " Z"
    xs = (f'<path d="M{-w*0.36:.0f},{-h*0.34:.0f} Q{-w*0.05:.0f},{-h*0.02:.0f} {w*0.38:.0f},{h*0.36:.0f}" stroke="#8E1E18" stroke-width="10" fill="none" stroke-linecap="round" opacity="0.85"/>'
          f'<path d="M{w*0.36:.0f},{-h*0.36:.0f} Q{w*0.02:.0f},{h*0.04:.0f} {-w*0.36:.0f},{h*0.34:.0f}" stroke="#8E1E18" stroke-width="8" fill="none" stroke-linecap="round" opacity="0.85"/>'
          f'<path d="M{-w*0.33:.0f},{-h*0.33:.0f} Q{-w*0.05:.0f},{-h*0.04:.0f} {w*0.3:.0f},{h*0.28:.0f}" stroke="#C8443A" stroke-width="4" fill="none" opacity="0.7"/>'
          + "".join(f'<circle cx="{w*0.38 + r.uniform(-6,8):.0f}" cy="{h*0.38 + r.uniform(-4,8):.0f}" r="{r.uniform(1.5,3.5):.1f}" fill="#8E1E18"/>' for _ in range(4)))
    return (f'<g transform="translate({x},{y}) rotate({rot})"><path d="{d}" fill="#000" opacity="0.45" transform="translate(8,10)" filter="url(#b6)"/>'
            f'<path d="{d}" fill="#E2CFA2"/>'
            + clipped(f"pa{seed}", d, f'<rect x="{-w}" y="{-h}" width="{w*2}" height="{h*2}" filter="url(#nz_d)" opacity="0.25"/><rect x="{-w}" y="{-h}" width="{w*2}" height="{h*2}" filter="url(#nz_f)" opacity="0.25"/><ellipse cx="{w*0.3:.0f}" cy="{h*0.25:.0f}" rx="{w*0.3:.0f}" ry="{h*0.2:.0f}" fill="#B8955A" opacity="0.35" filter="url(#b8)"/>'
                      f'<path d="M{-w/2},{-h/2} L{-w/2+26},{-h/2} L{-w/2},{-h/2+26} Z" fill="#B8A070"/>' + inner)
            + f'<path d="{d}" fill="none" stroke="#5A4026" stroke-width="3"/>' + xs
            + f'<circle cx="0" cy="{-h/2+6}" r="9" fill="#B8322A" stroke="{INK}" stroke-width="3"/><circle cx="-3" cy="{-h/2+3}" r="3" fill="#F0A090"/></g>')

MAP_INK = ('<g stroke="#2A1A0E" fill="none" stroke-linecap="round" stroke-linejoin="round">'
           '<path d="M70,-74 q-12,10 -6,22 q-14,6 -10,20 q-12,10 -4,22 q-10,12 2,24 q-6,14 6,22 L150,60 L150,-90 Z" stroke-width="3.5" fill="#C8B488"/>'           # İskandinav kıyısı (sağda)
           '<path d="M78,-50 l10,4 M72,-20 l12,2 M74,10 l10,-2" stroke-width="2"/>'
           '<path d="M-20,-60 q-30,10 -50,0 M-60,-40 q-20,8 -30,0" stroke-width="1.5" stroke-dasharray="3 4"/>'                    # boş batı
           '<text x="-48" y="12" font-family="Georgia" font-size="40" fill="#5A3E22" stroke="none" font-weight="bold">?</text>'
           '<path d="M-90,40 q10,-14 20,0 q10,14 20,0 q10,-14 20,0" stroke-width="3"/><path d="M-36,40 q8,-12 14,-4" stroke-width="3"/><circle cx="-26" cy="34" r="1.5" fill="#3A2A1A"/>'   # deniz yılanı
           '</g>')
COMPASS_INK = ('<g stroke="#3A2A1A" stroke-linejoin="round">'
               '<circle r="52" fill="none" stroke-width="2.5"/><circle r="44" fill="none" stroke-width="1.2"/>'
               + "".join(f'<path d="M0,0 L{48*math.cos(math.radians(a)):.0f},{48*math.sin(math.radians(a)):.0f}" stroke-width="1" />' for a in range(0, 360, 15))
               + '<path d="M0,-46 L9,0 L0,46 L-9,0 Z" fill="#E8D8B0" stroke-width="2.5"/><path d="M0,-46 L9,0 L-9,0 Z" fill="#8A2A22" stroke-width="2"/>'
               '<path d="M-46,0 L0,-8 L46,0 L0,8 Z" fill="#C8B488" stroke-width="2"/><circle r="5" fill="#3A2A1A"/>'
               '<text x="0" y="-56" font-family="Georgia" font-size="16" fill="#3A2A1A" stroke="none" text-anchor="middle" font-weight="bold">N</text></g>')

def f4():
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    D = DEFS(); GL = (1130, 280)
    # ---- 1 gök: koyu kümülüs kütleleri, ortada yırtık; yırtıktan hüzmeler denize iner
    o = [D, sky_grad("sk4", [(0, "#2E3A48"), (0.4, "#56667A"), (0.56, "#8E9AA4"), (0.62, "#B4BCC0")]), f'<rect width="{W}" height="{H}" fill="url(#sk4)"/>',
         f'<ellipse cx="{GL[0]}" cy="230" rx="300" ry="170" fill="#F2EAD2" opacity="0.7" filter="url(#b28)"/>',
         f'<rect width="{W}" height="{HZ}" filter="url(#nz_sky)" opacity="0.2"/>']
    # ufukta kule bulutlar (soluk, uzak)
    for k, (cx, cy, w_, h_) in enumerate([(260, 520, 700, 200), (760, 540, 500, 150), (1600, 520, 760, 220), (1950, 540, 400, 140)]):
        o.append(cloud(cx, cy, w_, h_, 80 + k, "#7E8A96", "#A8B2BA", "#5E6A78", blur=6, rim="#A8B2BA", a=0.95))
    # orta: büyük koyu kütleler, yırtığa bakan kenarlar gümüş-sıcak
    for k, (cx, cy, w_, h_, lit_side) in enumerate([(350, 260, 1000, 300, (1, -0.4)), (1750, 240, 900, 300, (-1, -0.4)), (620, 420, 700, 160, (1, -0.6)), (1560, 430, 600, 150, (-1, -0.6))]):
        o.append(cloud(cx, cy, w_, h_, 90 + k, "#4A5664", "#7A8696", "#283240", light=lit_side, blur=3, rim="#E6E0D0"))
    # üst: en koyu tavan
    for k, (cx, cy, w_, h_) in enumerate([(300, 60, 1100, 200), (1100, 30, 900, 170), (1800, 70, 900, 220)]):
        o.append(cloud(cx, cy, w_, h_, 95 + k, "#2E3846", "#46525E", "#1A222C", light=(0, 1), blur=4, rim="#6A7684", flat=0.45))
    draw(c, svg_sprite("".join(o)), 0, 0, 1.0)
    for (xt, xb, wb, a_) in ((GL[0] - 60, GL[0] - 140, 260, 0.20), (GL[0] + 40, GL[0] + 160, 200, 0.16), (GL[0] - 140, GL[0] - 420, 160, 0.12)):
        light_shaft(c, xt, 90, xb, wb, "#FFF0D0", a_ * 3.2, t=0, y_top=330, y_bot=HZ + 20)
    # ---- 2 deniz
    o = [D, f'<rect x="0" y="{HZ-2}" width="{W}" height="{H}" fill="#8A9AA4"/>', sea_rows(5, glint=(GL[0] - 60, 260)),
         f'<rect x="0" y="{HZ}" width="{W}" height="{H-HZ}" filter="url(#nz_d)" opacity="0.35"/>',
         '<g filter="url(#b18)">' + "".join(f'<ellipse cx="{R(k).uniform(0,W):.0f}" cy="{R(k+5).uniform(HZ+60,H):.0f}" rx="{R(k+9).uniform(200,500):.0f}" ry="{R(k+2).uniform(15,40):.0f}" fill="{["#0E1A22", "#9AB0BC"][k%2]}" opacity="0.22"/>' for k in range(14)) + '</g>']
    draw(c, svg_sprite("".join(o)), 0, 0, 1.0)
    fog(c, 0, HZ - 6, "#D8DEE0", 0.55, n=9, seed=31, speed=0, h=30)
    bloom_spot(c, GL[0] - 60, HZ + 30, 300, "#FFF2D4", 0.30)
    for (xt, xb, wb, a_) in ((GL[0] - 60, GL[0] - 160, 300, 0.10), (GL[0] + 40, GL[0] + 200, 220, 0.08)):
        light_shaft(c, xt, 120, xb, wb, "#FFF0D0", a_, t=0, y_top=240, y_bot=HZ + 140)
    # ---- 3 küçük gemi (batıya: sola), dümen suyu, martılar
    o = [D, f'<path d="M{GL[0]-10},{HZ+48} q80,6 200,2 M{GL[0]},{HZ+54} q90,8 220,6" stroke="#E8F0F2" stroke-width="2.5" fill="none" opacity="0.8"/>',
         f'<clipPath id="wl"><path d="M{GL[0]-200},{HZ-200} L{GL[0]+100},{HZ-200} L{GL[0]+100},{HZ+47} L{GL[0]-8},{HZ+47} q-15,-3 -30,0 q-15,3 -30,0 q-15,-3 -30,0 q-15,3 -30,0 L{GL[0]-200},{HZ+47} Z"/></clipPath>'
         f'<g clip-path="url(#wl)"><g transform="translate({GL[0]-60},{HZ+46}) scale(-0.068,0.068)">{G.longship(0, 0, 1.0, sail=True, oars=True, shields=True)}</g></g>',
         f'<path d="M{GL[0]-128},{HZ+47} q15,-3 30,0 q15,3 30,0 q15,-3 30,0 q15,3 30,0" stroke="#D8E4EA" stroke-width="2.2" fill="none" opacity="0.85"/>'
         f'<path d="M{GL[0]-100},{HZ+50} q30,3 70,0" stroke="#22323C" stroke-width="3" fill="none" opacity="0.5"/>',
         f'<path d="M{GL[0]-128},{HZ+44} q-8,-10 -18,-6 q6,4 4,10 Z" fill="#F2F6F8"/><circle cx="{GL[0]-140}" cy="{HZ+34}" r="2" fill="#F2F6F8"/><circle cx="{GL[0]-134}" cy="{HZ+30}" r="1.5" fill="#F2F6F8"/>']
    for k, (gx, gy, gs) in enumerate(((GL[0] - 200, HZ - 70, 0.22), (GL[0] + 80, HZ - 110, 0.18), (GL[0] - 40, HZ - 150, 0.15), (1500, 300, 0.4), (1590, 250, 0.32))):
        o.append(gull(gx, gy, gs, seed=k))
    draw(c, svg_sprite("".join(o)), 0, 0, 1.0)
    # ---- 4 ön plan: sol altta iri dalga sırtı + serpinti (bulanık), sağ üstte yakın martı (bulanık)
    fgw = svg_sprite(D + fg_swell(9))
    draw(c, blurred(fgw, 3), 0, 0, 1.0)
    draw(c, blurred(svg_sprite(D + gull(1440, 190, 1.0, seed=7)), 3), 0, 0, 1.0)
    # ---- ışık ve renk
    glow(c, GL[0] - 60, HZ, 500, "#FFE8C0", 0.10)
    gradient_grade(c, "#2A4A6E", "#10202C", 0.28, "soft")
    grade(c, "#9EB6CC", 0.10, "multiply")
    # ---- parşömen ekler (zarif, küçük): harita ve pusula, ikisi de kırmızı fırçayla çizik
    draw(c, svg_sprite(D + parchment(250, 205, 230, 165, MAP_INK, 1, rot=-4) + parchment(1670, 215, 190, 170, COMPASS_INK, 2, rot=3)), 0, 0, 1.0)
    card_at(c, "BATI", 960, 120, "açık deniz", 0.9)
    finish(c, cold=False); return s

FRB = {"f1": f1, "f3": f3, "f4": f4}

CROPS = {"f1": [(400, 520, 360, 200), (1060, 640, 400, 225)], "f3": [(860, 600, 400, 225), (1100, 480, 440, 248)], "f4": [(940, 560, 320, 180), (120, 110, 300, 190)]}   # (x, y, w, h) → %200 kırpma

def crops(i):
    from PIL import Image
    im = Image.open(f"{OUTV}/{i}.png").convert("RGB")
    for k, (x, y, w, h) in enumerate(CROPS.get(i, []), 1):
        im.crop((x, y, x + w, y + h)).resize((w * 2, h * 2), Image.LANCZOS).save(f"{OUTV}/{i}_crop{k}.png")

if __name__ == "__main__":
    import os; os.makedirs(OUTV, exist_ok=True)
    ids = sys.argv[1:] or list(FRB)
    for i in ids:
        T[0] = None; FRB[i]().makeImageSnapshot().save(f"{OUTV}/{i}.png", skia.kPNG); crops(i); print("kare", i)
