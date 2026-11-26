"""Bölüm I v3 · Ajan C: karakter / hikâye kareleri f6, f7, f9, f10 (brief: kurul/BRIEF_bolum1_v3.md).
python3 v3_c.py [f6 f7 f9 f10] → bati/v3/<id>.png (+ <id>_crop1/2.png R13 kırpmaları)
"""
import sys
sys.path.insert(0, "/home/claude/r3/bati")
from kareler6 import *
import tex
OUT3 = "/home/claude/r3/bati/v3"
R_ = random.Random

TORCH_B = ('<g transform="translate(HX,HY)"><path d="M4,40 L-12,-150" stroke="#1A1410" stroke-width="22" stroke-linecap="round"/><path d="M4,40 L-12,-150" stroke="#5A4028" stroke-width="12" stroke-linecap="round"/>'
           '<path d="M-30,-150 Q-34,-196 -14,-206 Q8,-206 10,-160 Q4,-146 -30,-150 Z" fill="#2A2018" stroke="#1A1410" stroke-width="5"/>'   # katranlı bez sargı
           '<path d="M-28,-170 q18,-6 36,2 M-28,-186 q18,-6 34,2" stroke="#4A3A2A" stroke-width="4" fill="none"/>'
           '<path d="M-36,-196 Q-70,-270 -40,-330 Q-34,-290 -18,-286 Q-30,-340 6,-390 Q2,-330 22,-300 Q30,-340 44,-350 Q52,-270 14,-200 Z" fill="#E8641E" stroke="#1A1410" stroke-width="4" stroke-linejoin="round"/>'
           '<path d="M-24,-200 Q-44,-250 -24,-290 Q-16,-262 -4,-258 Q-10,-300 8,-330 Q8,-280 22,-262 Q28,-240 6,-200 Z" fill="#F8A23A"/>'
           '<path d="M-12,-204 Q-20,-236 -8,-256 Q0,-236 6,-232 Q10,-218 2,-204 Z" fill="#FFE6A0"/></g>')

TEXD = tex.defs("ahsap", "tas", "deri", "kurk", "yun", "metal")

def gradient(id_, stops, x2=0, y2=1):
    return (f'<linearGradient id="{id_}" x1="0" y1="0" x2="{x2}" y2="{y2}">' + "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops) + '</linearGradient>')

def ridge(pts, fill_, stroke="#0A0E14", sw=4):
    d = "M" + " ".join(f"{x:.0f},{y:.0f}" for x, y in pts) + " Z"
    return f'<path d="{d}" fill="{fill_}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"/>'

def ridge_pts(seed, x0, x1, base, top, amp, it=6):
    """Tepe–boyun dizisi + küçük pürüz. top: en yüksek tepe, amp: tepe yükseklik değişkenliği."""
    r = R_(seed); pts = []; x = x0
    while x < x1:
        pts.append((x, top + r.uniform(0, amp)))                      # tepe
        x += r.uniform(110, 260); pts.append((x, top + amp + r.uniform(30, (base - top - amp) * 0.75)))   # boyun
        x += r.uniform(110, 260)
    pts.append((x1 + 200, base - 40))
    d = 26
    for _ in range(it):
        np_ = []
        for (ax, ay), (bx, by) in zip(pts, pts[1:]):
            np_ += [(ax, ay), ((ax + bx) / 2 + r.uniform(-0.08, 0.08) * (bx - ax), (ay + by) / 2 + r.uniform(-d, d))]
        np_.append(pts[-1]); pts = np_; d *= 0.6
    return [(x, min(base - 6, y)) for x, y in pts]

def mountain_range(seed, x0, x1, base, top, amp, body, lit, snow=None, light=1, snow_y=None, stroke="#0A0E14", cid="m", taper=0):
    """Sıra dağ (orta nokta kaydırma sırtı): gövde + ışık tarafı yüzleri + pürüzlü kar örtüsü.
    taper > 0: sol uç dikey kesilmez, taper px boyunca suya/zemine doğru alçalan bir etekle başlar."""
    r = R_(seed + 50); P = ridge_pts(seed, x0, x1, base, top, amp)
    if taper:
        (ax, ay) = P[0]; P = [(ax - taper + taper * f, base - (base - ay) * (f ** 1.6) + 6 * math.sin(f * 9)) for f in [i / 14 for i in range(14)]] + P; x0 = ax - taper
    d = "M" + " ".join(f"{x:.0f},{y:.0f}" for x, y in P) + f" L{x1},{base} L{x0},{base} Z"
    o = [f'<defs><clipPath id="{cid}{seed}"><path d="{d}"/></clipPath></defs><path d="{d}" fill="{body}"/>', f'<g clip-path="url(#{cid}{seed})">']
    peaks = [i for i in range(2, len(P) - 2) if P[i][1] == min(p[1] for p in P[max(0, i - 7):i + 8]) and P[i][1] < base - (base - top) * 0.25]
    for i in peaks:   # ışık tarafı yüzü (tepeden aşağı inen sırt)
        px, py = P[i]; w = r.uniform(120, 240)
        o.append(f'<path d="M{px:.0f},{py:.0f} L{px + light*w*2.4:.0f},{base} L{px + light*w*0.3:.0f},{base} Q{px + light*w*0.2:.0f},{(py+base)/2:.0f} {px:.0f},{py:.0f} Z" fill="{lit}"/>')
    if snow:
        sy = snow_y if snow_y is not None else top + (base - top) * 0.45
        low = []
        ph = r.uniform(0, 6)
        for x, y in P:
            dd = 30 + 14 * math.sin(x * 0.021 + ph) + 7 * math.sin(x * 0.063 + 2 * ph) + r.uniform(-3, 3)
            low.append((x, y if y > sy else min(y + dd, sy + 10 * math.sin(x * 0.03 + ph))))
        sd = "M" + " ".join(f"{x:.0f},{y:.0f}" for x, y in P) + " L" + " ".join(f"{x:.0f},{y:.0f}" for x, y in low[::-1]) + " Z"
        o.append(f'<path d="{sd}" fill="{snow}" opacity="0.9"/>')
        for i in peaks:   # kar kanalları (yüzün ışık tarafında, tepeden süzülen)
            px, py = P[i]
            for j in range(1):
                gx = px + light * r.uniform(4, 40); o.append(f'<path d="M{px:.0f},{py+4:.0f} Q{gx:.0f},{py + 30 + j*10:.0f} {gx + light*r.uniform(10,40):.0f},{py + r.uniform(50, 110):.0f}" stroke="{snow}" stroke-width="{r.uniform(2,3.5):.1f}" fill="none" opacity="0.3" stroke-linecap="round"/>')
    o.append('</g>')
    o.append('<path d="M' + " ".join(f"{x:.0f},{y:.0f}" for x, y in P) + f'" stroke="{stroke}" stroke-width="3" fill="none" stroke-linejoin="round"/>')
    return "".join(o)

def cloud_band(seed, n, x0, x1, y0, y1, body, lit, a=1.0, lit_dy=-6, rx=(120, 320), ry=(18, 46)):
    r = R_(seed); o = []
    for k in range(n):
        x = r.uniform(x0, x1); y = r.uniform(y0, y1); w_ = r.uniform(*rx); h_ = r.uniform(*ry)
        o.append(f'<ellipse cx="{x:.0f}" cy="{y+lit_dy:.0f}" rx="{w_:.0f}" ry="{h_:.0f}" fill="{lit}" opacity="{a*0.9:.2f}"/>'
                 f'<ellipse cx="{x+8:.0f}" cy="{y:.0f}" rx="{w_*0.98:.0f}" ry="{h_*0.92:.0f}" fill="{body}" opacity="{a:.2f}"/>')
    return "".join(o)

def pebbles(seed, n, x0, x1, y0, y1, cols=("#3A3A3C", "#4A4642", "#2E3034", "#55504A"), hl="#9AB0C4", wet=True, grow=1.0):
    r = R_(seed); o = []
    items = sorted([(r.uniform(y0, y1), r.uniform(x0, x1)) for _ in range(n)])
    for y, x in items:
        d = (y - y0) / max(1, (y1 - y0)); s = (4 + 22 * d) * grow * r.uniform(0.6, 1.3); c_ = r.choice(cols)
        o.append(f'<ellipse cx="{x:.0f}" cy="{y+s*0.25:.0f}" rx="{s*1.15:.1f}" ry="{s*0.35:.1f}" fill="#000" opacity="0.35"/>'
                 f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{s:.1f}" ry="{s*0.62:.1f}" fill="{c_}" stroke="#0E0E10" stroke-width="{1+d*2.2:.1f}"/>')
        if r.random() < 0.8:
            o.append(f'<path d="M{x-s*0.5:.0f},{y-s*0.32:.0f} Q{x+s*0.1:.0f},{y-s*0.62:.0f} {x+s*0.6:.0f},{y-s*0.28:.0f}" stroke="{hl}" stroke-width="{1+d*2:.1f}" fill="none" opacity="{0.45 + 0.4*wet*r.random():.2f}"/>')
    return "".join(o)

def gull(x, y, s=1.0, flap=0.0, col_="#E8ECEE", dark="#2A2E34", rot=0):
    """Martı: gövde, kıvrık kanat (dirsek), siyah kanat ucu, sarı gaga."""
    up = -26 - 18 * flap
    return (f'<g transform="translate({x:.0f},{y:.0f}) rotate({rot}) scale({s})">'
            f'<path d="M-6,0 Q-40,{up*0.6:.0f} -66,{up:.0f} Q-80,{up+4:.0f} -96,{up+14:.0f} Q-60,{up*0.2:.0f} -8,8 Z" fill="{col_}" stroke="{dark}" stroke-width="3" stroke-linejoin="round"/>'
            f'<path d="M-66,{up:.0f} Q-80,{up+4:.0f} -96,{up+14:.0f} Q-82,{up+12:.0f} -72,{up+8:.0f} Z" fill="{dark}"/>'
            f'<path d="M6,0 Q40,{up*0.6:.0f} 62,{up+2:.0f} Q78,{up+6:.0f} 92,{up+16:.0f} Q58,{up*0.2:.0f} 8,8 Z" fill="{col_}" stroke="{dark}" stroke-width="3" stroke-linejoin="round"/>'
            f'<path d="M62,{up+2:.0f} Q78,{up+6:.0f} 92,{up+16:.0f} Q78,{up+14:.0f} 68,{up+10:.0f} Z" fill="{dark}"/>'
            f'<path d="M-22,6 Q0,-6 26,2 Q34,6 26,12 Q0,16 -22,6 Z" fill="{col_}" stroke="{dark}" stroke-width="3"/>'
            f'<path d="M26,4 l12,3 l-12,3 Z" fill="#D8A83A"/><circle cx="20" cy="5" r="1.6" fill="{dark}"/></g>')

def crop2x(img_path, box, out):
    """R13: 1920 karede kutuyu %200 büyüt."""
    from PIL import Image
    im = Image.open(img_path).convert("RGB"); x, y, w, h = box
    im.crop((x, y, x + w, y + h)).resize((w * 2, h * 2), Image.LANCZOS).save(out)

def soft_shadow(c, x, y, rx, ry, a=0.4, blur=10):
    p = skia.Paint(AntiAlias=True, Color4f=col("#000", a), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, blur))
    c.drawOval(skia.Rect(x - rx, y - ry, x + rx, y + ry), p)

def breath(c, x, y, s=1.0, a=0.35, d=1):
    """Soğukta nefes buharı: ağızdan çıkan, genişleyip sönen yumuşak bulut (normal karışım)."""
    for k in range(6):
        r = (8 + k * 7) * s; cx = x + d * (10 + k * 15) * s; cy = y - k * 4 * s
        c.drawOval(skia.Rect(cx - r * 1.3, cy - r * 0.8, cx + r * 1.3, cy + r * 0.8),
                   skia.Paint(AntiAlias=True, Color4f=col("#F2F6FA", a * (1 - k / 7)), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 4 + k * 2)))

# =============================================================== f6 · gece, gizli kalkış
def f6_sky():
    r = R_(6); o = ['<defs>' + gradient("s6", [(0, "#060B14"), (0.55, "#13233A"), (1, "#2A4462")]) + '</defs>', '<rect width="1920" height="600" fill="url(#s6)"/>']
    for k in range(160):
        x, y = r.uniform(0, 1920), r.uniform(60, 430); o.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r.uniform(0.8, 2.2):.1f}" fill="#DCE8F4" opacity="{r.uniform(0.25, 0.85):.2f}"/>')
    o.append('<circle cx="1490" cy="185" r="58" fill="#E6EEF4"/><circle cx="1474" cy="172" r="12" fill="#C8D4DE" opacity="0.6"/><circle cx="1508" cy="204" r="8" fill="#C8D4DE" opacity="0.5"/><circle cx="1500" cy="160" r="6" fill="#C8D4DE" opacity="0.5"/>')
    return "".join(o)

def f6_clouds():
    return (cloud_band(61, 9, 900, 1920, 230, 290, "#1A2A40", "#8AA4C0", 0.8, lit_dy=-8, rx=(140, 300), ry=(10, 22))
            + cloud_band(62, 7, 0, 900, 120, 200, "#142236", "#4A6280", 0.7, lit_dy=-6, rx=(160, 340), ry=(12, 26))
            + cloud_band(64, 4, 1300, 1700, 205, 225, "#22344C", "#B8CCE0", 0.6, lit_dy=-6, rx=(60, 130), ry=(6, 10)))

def f6_bg():
    o = [TEXD, '<defs>' + gradient("s6", [(0, "#060B14"), (0.55, "#13233A"), (1, "#2A4462")])
         + gradient("w6", [(0, "#1C3048"), (0.4, "#101C2C"), (1, "#070C14")])
         + gradient("sh6", [(0, "#2E2E30"), (1, "#141416")]) + '</defs>',
         ]
    r = R_(6)
    # uzak dağlar (ay sağda: sağ yüzler ışıklı) + yakın koyu sırt
    o.append(mountain_range(7, -40, 1960, 562, 290, 90, "#1A2A3C", "#2A4058", snow="#8EA6BE", light=1, snow_y=380))
    o.append(mountain_range(8, -40, 980, 572, 410, 50, "#0E1824", "#1A2C40", snow="#5E7690", light=1, snow_y=455))
    o.append('<path d="M1500,560 L1620,500 L1760,520 L1920,470 L1920,566 Z" fill="#0C1520" stroke="#06090E" stroke-width="3"/>')
    for k in range(22):   # karşı kıyıda çam sırası
        x = 1520 + k * 18 + r.uniform(-4, 4); h = r.uniform(26, 48); b = 560 - (x - 1500) * 0.12
        o.append(f'<path d="M{x:.0f},{b-h:.0f} L{x+9:.0f},{b:.0f} L{x-9:.0f},{b:.0f} Z" fill="#08101A"/>')
    o.append(cloud_band(65, 12, -100, 2000, 470, 540, "#3A5068", "#4A6280", 0.22, rx=(200, 420), ry=(16, 30)))   # dağ eteği sisi
    # su
    o.append('<rect y="556" width="1920" height="524" fill="url(#w6)"/>')
    o.append('<path d="M0,560 H1920" stroke="#3C5674" stroke-width="3" opacity="0.7"/>')
    for k in range(70):   # dalga çizgileri (uzakta sık, yakında seyrek)
        y = 566 + (k / 70) ** 1.6 * 300; x = r.uniform(-100, 1900); w_ = 40 + (y - 560) * 0.9
        o.append(f'<path d="M{x:.0f},{y:.0f} q{w_/2:.0f},-{2+(y-560)*0.02:.1f} {w_:.0f},0" stroke="#3A5470" stroke-width="{1+(y-560)*0.008:.1f}" fill="none" opacity="0.55"/>')
    for k in range(90):   # ay parıltısı yolu
        y = 566 + (k / 90) ** 1.3 * 280; spread = 20 + (y - 560) * 0.5; x = 1490 + r.gauss(0, spread * 0.5); w_ = r.uniform(10, 26) + (y - 560) * 0.12
        o.append(f'<path d="M{x-w_/2:.0f},{y:.0f} h{w_:.0f}" stroke="#DCE8F2" stroke-width="{1.5+(y-560)*0.01:.1f}" stroke-linecap="round" opacity="{r.uniform(0.35, 0.9):.2f}"/>')
    # su üstü sis
    o.append(cloud_band(63, 10, -100, 2000, 540, 590, "#5A7290", "#7A92AE", 0.18, rx=(240, 480), ry=(14, 26)))
    return "".join(o)

def f6_shore():
    """Ön plan çakıllı kıyı (ıslak), kıyı çizgisi köpüğü, yosun, iskele kazığı, halat kangalı, ayak izleri."""
    r = R_(16); o = [TEXD]
    edge = "M0,800 Q300,790 600,830 Q900,872 1200,900 Q1600,930 1920,940 L1920,1080 L0,1080 Z"
    o.append('<defs>' + gradient("sh6b", [(0, "#2C2E32"), (0.5, "#1C1E22"), (1, "#0E0F12")]) + f'<clipPath id="shc"><path d="{edge}"/></clipPath></defs>')
    o.append(f'<path d="{edge}" fill="url(#sh6b)"/>')
    o.append(f'<g clip-path="url(#shc)"><rect width="1920" height="1080" filter="url(#t_tas)" fill="#3A3A3E" opacity="0.5"/>')
    o.append(pebbles(160, 520, -20, 1940, 790, 1090, grow=1.1))
    # ıslak şerit (ay yansıması) kıyı boyunca
    o.append('<path d="M0,806 Q300,796 600,836 Q900,878 1200,906 Q1600,936 1920,946" stroke="#8EA6BE" stroke-width="10" fill="none" opacity="0.28"/>')
    for k in range(9):   # yosun/kelp şeritleri
        x = r.uniform(200, 1700); y = 820 + (x / 1920) * 110 + r.uniform(0, 30)
        o.append(f'<path d="M{x:.0f},{y:.0f} q30,-8 60,4 q30,10 64,-2" stroke="#1E2A1A" stroke-width="7" fill="none" stroke-linecap="round"/><path d="M{x+6:.0f},{y-3:.0f} q30,-8 56,3" stroke="#4A5A3A" stroke-width="2" fill="none" opacity="0.7"/>')
    for k in range(6):   # ayak izleri: kıyıdan gemiye
        x = 380 + k * 70; y = 900 - k * 14
        o.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="16" ry="6" fill="#0A0B0D" opacity="0.6"/><path d="M{x-14:.0f},{y-3:.0f} q14,-5 28,0" stroke="#6E8298" stroke-width="2" fill="none" opacity="0.5"/>')
    o.append('</g>')
    # köpük: kıyı çizgisi boyunca kırık beyaz şerit
    for k in range(40):
        t_ = k / 40; x = t_ * 1920; y = 800 + 140 * t_ ** 1.1 - 6
        o.append(f'<path d="M{x:.0f},{y:.0f} q{r.uniform(10,30):.0f},-4 {r.uniform(30,60):.0f},1" stroke="#C8D8E6" stroke-width="{r.uniform(2,5):.1f}" fill="none" opacity="{r.uniform(0.3,0.75):.2f}" stroke-linecap="round"/>')
    # iskele kazığı (zemine giren) + gemiye giden halat
    o.append('<path d="M640,930 L652,760 L684,760 L690,936 Z" fill="#3A2A1C" stroke="#0A0806" stroke-width="5" filter="url(#t_ahsap)"/>'
             '<path d="M640,930 L652,760 L684,760 L690,936 Z" fill="none" stroke="#0A0806" stroke-width="5"/>'
             '<path d="M666,760 L684,760 L690,936 L668,934 Z" fill="#000" opacity="0.4"/>'
             '<ellipse cx="664" cy="934" rx="40" ry="9" fill="#000" opacity="0.5"/>'
             '<path d="M648,790 Q668,800 688,790 M648,806 Q668,816 688,806" stroke="#8A7A5A" stroke-width="6" fill="none"/>')
    o.append('<path d="M684,796 Q760,840 840,800" stroke="#0A0806" stroke-width="8" fill="none"/><path d="M684,796 Q760,840 840,800" stroke="#9A8A62" stroke-width="4" fill="none" stroke-dasharray="6 4"/>')
    # halat kangalı (Ragnar'ın ayağı yanında)
    for k in range(5):
        o.append(f'<ellipse cx="560" cy="{1000-k*7}" rx="{78-k*8}" ry="{22-k*1.6:.0f}" fill="none" stroke="#0A0806" stroke-width="12"/><ellipse cx="560" cy="{1000-k*7}" rx="{78-k*8}" ry="{22-k*1.6:.0f}" fill="none" stroke="#8A7650" stroke-width="7" stroke-dasharray="8 3"/>')
    o.append('<path d="M630,996 Q700,1010 760,1060" stroke="#0A0806" stroke-width="12" fill="none"/><path d="M630,996 Q700,1010 760,1060" stroke="#8A7650" stroke-width="7" fill="none" stroke-dasharray="8 3"/>')
    # kıyıda bekleyen sandık + kalkan (gizli yük)
    o.append('<g transform="translate(1720,960)"><ellipse cx="0" cy="10" rx="120" ry="16" fill="#000" opacity="0.5"/>'
             '<rect x="-100" y="-80" width="200" height="90" rx="6" fill="#4A3020" filter="url(#t_ahsap)"/><rect x="-100" y="-80" width="200" height="90" rx="6" fill="none" stroke="#0A0806" stroke-width="6"/>'
             '<path d="M-100,-80 Q0,-130 100,-80" fill="#5A3A24" stroke="#0A0806" stroke-width="6"/><path d="M-60,-104 V10 M60,-104 V10" stroke="#5A5E64" stroke-width="10"/>'
             '<path d="M-100,-40 H100" stroke="#5A5E64" stroke-width="7"/><path d="M100,-80 Q20,-126 -40,-118" stroke="#9AB0C8" stroke-width="3" fill="none" opacity="0.6"/></g>')
    return "".join(o)

def f6():
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    draw(c, svg_sprite(f6_sky()), 0, 0, 1.0)
    glow(c, 1490, 185, 300, "#9EB8D6", 0.30); glow(c, 1490, 185, 110, "#E6F0FA", 0.4)
    draw(c, blurred(svg_sprite(f6_clouds()), 4), 0, 0, 1.0)
    draw(c, svg_sprite(f6_bg()), 0, 0, 1.0)
    # gemi: kıç kıyıda sığlıkta, pruva açığa dönük; yelken sarılı; mürettebat küpeşte arkasında
    sx, sy, ss = 1170, 700, 0.74
    draw(c, svg_sprite(f'<g transform="translate({sx},{sy}) scale({ss})">{G.mast_sail(1.0, reefed=True)}</g>'), 0, 0, 1.0)
    for k, (x, ph) in enumerate(((930, 0.1), (1060, 0.7), (1220, 0.4), (1330, 0.9))):   # küreğe geçen mürettebat (gövde arkasında)
        sp = full(dict(KL.soldier_spec(90 + k, "ragnar"), _arm_up=False, _hand_extra="", _body_extra=""), "determined" if k % 2 else "neutral", 0.9, facing=1, look=0.5)
        c.save(); c.clipRect(skia.Rect(0, 0, W, 700))
        rim(c, sp, x, 790, 0.40, "#9EBAD8", dx=3, dy=-1, a=0.5); draw(c, sp, x, 790, 0.40); c.restore()
    FL = full(dict(FLOv, _arm_up=True, _hand_extra=""), ex("laugh", IF.blink_at(0.5)), 0.9, facing=1, look=0.7)
    rim(c, FL, 1470, 676, 0.5, "#BFD6F0", dx=4, dy=-2, a=0.8); draw(c, FL, 1470, 676, 0.5)
    hull = G.hull(1.0, shields=True, oars=False, wet=True)
    oars = "".join(f'<path d="M{x},{-70 - (k%2)*6} L{x + 300},{-150 - (k%3)*10}" stroke="{INK}" stroke-width="13"/><path d="M{x},{-70 - (k%2)*6} L{x + 300},{-150 - (k%3)*10}" stroke="#B88A52" stroke-width="6"/>' for k, x in enumerate(range(-380, 260, 120)))   # içeri çekilmiş kürekler, eğik yığın
    draw(c, svg_sprite(f'<g transform="translate({sx},{sy}) scale({ss})">{oars}{hull}</g>'), 0, 0, 1.0)
    # gövdeye ay ışığı: üst kaplama parıltısı
    glow(c, 1450, 610, 220, "#9EB8D6", 0.12)
    # gövdenin su altı: yansıma + su örtüsü
    wr = skia.Paint(AntiAlias=True, Color4f=col("#0C1828", 0.72)); c.drawRect(skia.Rect(740, 735, 1660, 790), wr)
    rr = R_(66)
    for k in range(40):
        y = 738 + rr.uniform(0, 48); x = rr.uniform(760, 1640)
        c.drawLine(x, y, x + rr.uniform(20, 70), y, skia.Paint(AntiAlias=True, Color4f=col("#8EA8C4", rr.uniform(0.15, 0.5)), StrokeWidth=2))
    # iten mürettebat: kıç direğinde, dize kadar suda, öne eğik
    for k, (x, y, rot, ph) in enumerate(((612, 792, 28, 1.1), (560, 806, 29, 0.3))):
        sp = full(dict(KL.soldier_spec(110 + k * 3, "ragnar"), _arm_up=True, _hand_extra="", _body_extra=""), "angry", 0.9, facing=1, look=0.6)
        c.save(); c.translate(x, y); c.rotate(rot); c.translate(-x, -y)
        rim(c, sp, x, y, 0.45, "#BFD6F0", dx=4, dy=-2, a=0.6); draw(c, sp, x, y, 0.45); shade_side(c, sp, x, y, 0.5, x - 140, x + 40, "#060A12")
        c.restore()
        c.drawOval(skia.Rect(x - 60, y - 54, x + 60, y - 34), skia.Paint(AntiAlias=True, Color4f=col("#0E1A2A", 0.88)))   # su yüzü (dizler)
        c.drawRect(skia.Rect(x - 70, y - 44, x + 70, y + 10), skia.Paint(AntiAlias=True, Color4f=col("#0E1A2A", 0.88)))
        for j in range(3):
            c.drawOval(skia.Rect(x - 40 - j * 20, y - 50 - j * 3, x + 40 + j * 20, y - 38 + j * 3), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=2, Color4f=col("#C8DCEE", 0.5 - j * 0.12)))
    draw(c, svg_sprite(f6_shore()), 0, 0, 1.0)
    # Ragnar: ön plan solda, meşale kalkık, söndürmek üzere (su kovası yanında)
    RGt = full(dict(RG, _arm_up=True, _hand_extra=TORCH_B), ex("determined", IF.blink_at(0.2)), 1.0, facing=1, look=0.7)
    rx_, ry_ = 300, 1112
    soft_shadow(c, rx_, ry_ - 30, 160, 20, 0.6)
    with live(c, rx_, ry_, phase=0.2, breathe=0.006):
        rim(c, RGt, rx_, ry_, 1.0, "#BFD6F0", dx=6, dy=-2, a=0.55); rim(c, RGt, rx_, ry_, 1.0, "#FFB070", dx=4, dy=-5, a=0.7)
        draw(c, RGt, rx_, ry_, 1.0); shade_side(c, RGt, rx_, ry_, 0.6, rx_ + 240, rx_ - 200, "#05080E")
    # meşale ışığı: sıcak tek nokta
    tx, ty = 455, 250
    glow(c, tx, ty, 420, "#FF8A2A", 0.22); glow(c, tx, ty, 140, "#FFC070", 0.45); bloom_spot(c, tx - 6, ty - 40, 60, "#FFE6A8", 0.5)
    for j in range(26):   # kıvılcım
        q = R_(j); c.drawCircle(tx + q.uniform(-50, 60), ty - 60 - q.uniform(0, 200), q.uniform(1.5, 3.2), skia.Paint(AntiAlias=True, Color4f=col("#FFC070", q.uniform(0.4, 0.9))))
    breath(c, rx_ + 70, 610, 0.9, 0.3)
    glow(c, 470, 930, 260, "#FF9A40", 0.10)
    for j in range(14):   # meşalenin sudaki sıcak yansıması
        q = R_(j + 300); y = 790 + q.uniform(-14, 10); x = 470 + q.gauss(0, 30)
        c.drawLine(x, y, x + q.uniform(10, 30), y, skia.Paint(AntiAlias=True, StrokeWidth=2.5, Color4f=col("#FFB060", q.uniform(0.3, 0.7))))
    # ön plan çerçeve: bulanık kaya + kıyı otu (sağ alt / sol alt)
    fg = ('<path d="M1580,1080 Q1600,960 1700,930 Q1820,900 1920,940 L1920,1080 Z" fill="#0A0C10"/>'
          + "".join(f'<path d="M{x},{1080} q{(k%3-1)*10},-60 {(k%5-2)*14},-{90+k%4*30}" stroke="#141A12" stroke-width="7" fill="none"/>' for k, x in enumerate(range(0, 200, 12))))
    draw(c, blurred(svg_sprite(fg), 7), 0, 0, 1.0)
    card_at(c, "GECE", 860, 150, "Jarl'dan gizli")
    fill(c, "#0A1424", 0.12); finish(c, cold=True); return s

# =============================================================== f7 · pruvadan: sisten çıkan Lindisfarne
def f7_sky():
    r = R_(70); o = ['<defs>' + gradient("s7", [(0, "#5E7088"), (0.45, "#9AA6B4"), (0.8, "#E2CFB6"), (1, "#F2DCC0")]) + '</defs>', '<rect width="1920" height="620" fill="url(#s7)"/>']
    o.append('<circle cx="430" cy="330" r="64" fill="#FFF2DA" opacity="0.95"/>')
    return "".join(o)

def f7_clouds():
    return (cloud_band(71, 10, -100, 2000, 110, 220, "#7E8A9C", "#E8D4BC", 0.75, lit_dy=8, rx=(200, 420), ry=(20, 46))
            + cloud_band(72, 8, -100, 2000, 250, 330, "#A8AEB8", "#F4DEC2", 0.6, lit_dy=7, rx=(160, 360), ry=(12, 26)))

def monastery_isle():
    """Lindisfarne: katmanlı kireçtaşı yarı, çimen üst, taş kilise (nef, yuvarlak kemer, çan kulesi), keşiş hücreleri, taş çit; gelgit düzlüğü."""
    r = R_(77); o = [TEXD]
    # uzak anakara (sağda, puslu)
    o.append('<path d="M1180,560 Q1400,520 1600,530 Q1800,515 1960,525 L1960,566 L1180,566 Z" fill="#A8AEB4" opacity="0.8"/>')
    o.append('<path d="M1300,548 Q1500,532 1700,540 L1700,566 L1300,566 Z" fill="#9AA2AA" opacity="0.7"/>')
    # gelgit kumu (adanın önünde, ıslak yansıma)
    o.append('<path d="M240,566 Q520,548 900,552 Q1200,556 1420,566 Q1100,584 700,586 Q400,584 240,566 Z" fill="#C8B898" opacity="0.85"/>'
             '<path d="M300,572 Q600,566 900,568 Q1150,570 1350,574" stroke="#F4E6CC" stroke-width="3" fill="none" opacity="0.7"/>')
    # ana kaya kütlesi: yüksek yar (sol yüz güneşli), sağda tepe (Heugh)
    edge = "M260,568 L292,536 Q322,500 380,486 L430,468 Q470,440 520,434 L600,430 Q660,404 760,398 L940,392 Q1010,388 1060,400 L1100,392 Q1150,360 1200,368 L1236,392 Q1270,436 1292,500 L1318,568"
    top = edge + " Z"
    o.append(f'<defs><clipPath id="isl"><path d="{top}"/></clipPath>' + gradient("rk7", [(0, "#9A9284"), (0.5, "#7A746A"), (1, "#56524C")]) + '</defs>')
    o.append(f'<path d="{top}" fill="url(#rk7)"/>')
    o.append('<g clip-path="url(#isl)">')
    o.append(f'<rect x="250" y="350" width="1080" height="230" fill="#7A746A" filter="url(#t_tas)" opacity="0.7"/>')
    for k in range(13):   # katmanlar (strata) — hafif eğimli
        y = 440 + k * 10 + r.uniform(-3, 3)
        o.append(f'<path d="M250,{y+10:.0f} Q700,{y-4:.0f} 1330,{y-8:.0f}" stroke="#3E3A34" stroke-width="{1.6 + k*0.18:.1f}" fill="none" opacity="0.75"/>')
        o.append(f'<path d="M250,{y+13:.0f} Q700,{y-1:.0f} 1330,{y-5:.0f}" stroke="#D8CCB4" stroke-width="1.2" fill="none" opacity="0.35"/>')
    for k in range(70):   # düşey eklemler + çatlaklar
        x = r.uniform(280, 1300); y = r.uniform(430, 560); o.append(f'<path d="M{x:.0f},{y:.0f} l{r.uniform(-3,3):.0f},{r.uniform(8,20):.0f}" stroke="#34302A" stroke-width="2.5" opacity="0.75"/>')
    o.append('<path d="M1150,360 L1330,568 L1180,568 Q1190,470 1150,420 Z" fill="#2E3038" opacity="0.38"/>')   # gölge yüzü
    o.append('<path d="M260,568 L292,536 Q322,500 380,486 L430,468 L470,568 Z" fill="#FFE2B8" opacity="0.22"/>')   # güneşe bakan yüz
    o.append('<path d="M250,548 Q700,536 1330,552 L1330,580 L250,580 Z" fill="#33331E" opacity="0.9"/>')   # deniz otu bandı
    o.append(f'<path d="{edge}" stroke="#5E6E44" stroke-width="30" fill="none"/><path d="{edge}" stroke="#7E8C58" stroke-width="10" fill="none" transform="translate(0,-6)"/>')   # çimen örtüsü
    o.append('</g>')
    o.append(f'<path d="{edge}" stroke="#2A3020" stroke-width="3" fill="none"/>')
    for k in range(70):
        x = r.uniform(300, 1280); y = 400 + abs(x - 860) * 0.05 + r.uniform(-4, 10); o.append(f'<path d="M{x:.0f},{y:.0f} l{r.uniform(-3,3):.0f},-7" stroke="#6E7E4A" stroke-width="2"/>')
    for k in range(14):   # su kenarında kaya blokları
        x = r.uniform(270, 1320); w_ = r.uniform(18, 46); y = 568
        o.append(f'<path d="M{x:.0f},{y} L{x+4:.0f},{y-w_*0.5:.0f} L{x+w_*0.5:.0f},{y-w_*0.7:.0f} L{x+w_:.0f},{y-w_*0.35:.0f} L{x+w_+4:.0f},{y} Z" fill="#5E5A52" stroke="#1A1410" stroke-width="2.5"/>'
                 f'<path d="M{x+w_*0.5:.0f},{y-w_*0.7:.0f} L{x+w_:.0f},{y-w_*0.35:.0f} L{x+w_+4:.0f},{y} L{x+w_*0.55:.0f},{y} Z" fill="#000" opacity="0.25"/>')
    # taş çit (çevirme duvarı)
    o.append('<path d="M470,442 Q620,428 760,410 L940,402 Q1020,400 1090,410" stroke="#2A2620" stroke-width="12" fill="none"/><path d="M470,442 Q620,428 760,410 L940,402 Q1020,400 1090,410" stroke="#B0A894" stroke-width="7" fill="none" stroke-dasharray="10 3"/>')
    # keşiş hücreleri (saz damlı, sol)
    for (x, y, w) in ((520, 436, 70), (604, 428, 58)):
        o.append(f'<rect x="{x}" y="{y-34}" width="{w}" height="34" fill="#9A9284" stroke="#2A2620" stroke-width="3"/><path d="M{x-8},{y-30} L{x+w/2},{y-62} L{x+w+8},{y-30} Z" fill="#8A7A52" stroke="#2A2620" stroke-width="3"/>'
                 f'<path d="M{x+w/2},{y-62} L{x+w+8},{y-30} L{x+w/2},{y-30} Z" fill="#000" opacity="0.18"/><rect x="{x+w*0.4:.0f}" y="{y-20}" width="12" height="20" fill="#2A2420"/>')
    o.append('<path d="M640,364 q-10,-30 6,-50 q14,-24 -4,-50" stroke="#C8C4BC" stroke-width="10" fill="none" opacity="0.45" stroke-linecap="round"/>')   # ocak dumanı
    # kilise: nef + kemerli pencereler + çan kulesi + haç
    o.append('<g transform="translate(860,400) scale(0.8)">')
    o.append('<rect x="-180" y="-120" width="300" height="120" fill="#B0A898" filter="url(#t_tas)"/><rect x="-180" y="-120" width="300" height="120" fill="none" stroke="#1A1410" stroke-width="4"/>')
    for yy in range(-112, 0, 16):
        for xx in range(-180 + (yy // 16 % 2) * 14, 120, 28): o.append(f'<rect x="{xx}" y="{yy}" width="28" height="16" fill="none" stroke="#7E7668" stroke-width="1.2"/>')
    o.append('<path d="M-196,-112 L-30,-196 L136,-112 Z" fill="#5A4E40" stroke="#1A1410" stroke-width="4"/>')
    for k in range(1, 7):   # kayrak sıraları (saçağa paralel)
        y_ = -112 - k * 12; w_ = (y_ + 196) / 84 * 166; o.append(f'<path d="M{-30-w_:.0f},{y_} H{-30+w_:.0f}" stroke="#3E3428" stroke-width="2"/>')
        for j in range(int(w_ // 14)): o.append(f'<path d="M{-30-w_+j*28+(k%2)*14:.0f},{y_} v-12" stroke="#3E3428" stroke-width="1.2" opacity="0.7"/>')
    o.append('<path d="M-30,-196 L136,-112 L60,-112 Z" fill="#000" opacity="0.2"/>')
    for xx in (-150, -96, -42, 12, 66):
        o.append(f'<path d="M{xx},-30 V-70 Q{xx+12},-86 {xx+24},-70 V-30 Z" fill="#2A2830" stroke="#1A1410" stroke-width="3"/><path d="M{xx+12},-30 V-78" stroke="#6A6A72" stroke-width="2"/>')
    o.append('<path d="M-60,0 V-54 Q-40,-76 -20,-54 V0 Z" fill="#4A3020" stroke="#1A1410" stroke-width="3"/>')
    o.append('<path d="M120,-120 L190,-120 L190,0 L120,0 Z" fill="#000" opacity="0.12"/>')   # nefin gölge cephesi
    # çan kulesi
    o.append('<rect x="120" y="-250" width="74" height="250" fill="#A8A090" filter="url(#t_tas)"/><rect x="120" y="-250" width="74" height="250" fill="none" stroke="#1A1410" stroke-width="4"/>')
    o.append('<rect x="160" y="-250" width="34" height="250" fill="#000" opacity="0.16"/>')
    for yy in range(-244, 0, 16): o.append(f'<path d="M120,{yy} H194" stroke="#7E7668" stroke-width="1.2"/>')
    o.append('<path d="M138,-200 V-226 Q157,-246 176,-226 V-200 Z" fill="#1E1C22" stroke="#1A1410" stroke-width="3"/><path d="M148,-206 Q157,-226 166,-206 Z" fill="#B8963A" stroke="#1A1410" stroke-width="2"/>')   # çan
    o.append('<path d="M112,-250 L157,-300 L202,-250 Z" fill="#5A4E40" stroke="#1A1410" stroke-width="4"/>')
    o.append('<path d="M157,-300 V-344 M141,-328 H173" stroke="#1A1410" stroke-width="9"/><path d="M157,-300 V-344 M141,-328 H173" stroke="#D8B860" stroke-width="4"/>')
    o.append('<path d="M-30,-196 V-226 M-42,-214 H-18" stroke="#1A1410" stroke-width="7"/><path d="M-30,-196 V-226 M-42,-214 H-18" stroke="#C8C0B0" stroke-width="3"/>')
    o.append('</g>')
    # sağda ayrı kaya kulesi (stack) + köpük
    o.append('<path d="M1300,566 L1312,500 L1340,470 L1372,476 L1390,520 L1400,566 Z" fill="#6A665E" stroke="#1A1410" stroke-width="3"/><path d="M1340,470 L1372,476 L1390,520 L1400,566 L1364,566 Z" fill="#3E3C40" opacity="0.5"/>'
             + "".join(f'<path d="M1306,{490+k*12} H1396" stroke="#4A463E" stroke-width="2" opacity="0.6"/>' for k in range(6)))
    for k in range(30):   # kayalara vuran köpük
        x = r.uniform(280, 1420); o.append(f'<path d="M{x:.0f},{566 + r.uniform(-3, 4):.0f} q{r.uniform(6,16):.0f},-{r.uniform(3,8):.0f} {r.uniform(16,34):.0f},0" stroke="#F4F6F4" stroke-width="{r.uniform(2,4):.1f}" fill="none" opacity="0.8"/>')
    return "".join(o)

def f7_sea():
    r = R_(78); o = ['<defs>' + gradient("w7", [(0, "#8A98A4"), (0.25, "#5E7282"), (1, "#24343E")]) + '</defs>', '<rect y="560" width="1920" height="520" fill="url(#w7)"/>']
    for k in range(110):   # dalga sırtları: uzakta ince, yakında kalın; açık sırt + koyu çukur
        y = 566 + (k / 110) ** 1.7 * 470; x = r.uniform(-150, 1900); w_ = 30 + (y - 560) * 1.0
        sw = 1 + (y - 560) * 0.012
        o.append(f'<path d="M{x:.0f},{y:.0f} q{w_*0.25:.0f},-{2+(y-560)*0.03:.1f} {w_*0.5:.0f},0 q{w_*0.25:.0f},{1+(y-560)*0.02:.1f} {w_*0.5:.0f},0" stroke="#1E2C36" stroke-width="{sw:.1f}" fill="none" opacity="0.55"/>'
                 f'<path d="M{x+w_*0.1:.0f},{y-2-(y-560)*0.02:.0f} q{w_*0.2:.0f},-{1+(y-560)*0.02:.1f} {w_*0.4:.0f},0" stroke="#C8D2D8" stroke-width="{sw*0.7:.1f}" fill="none" opacity="0.4"/>')
    for k in range(120):   # güneş parıltısı yolu (güneş solda)
        y = 566 + (k / 120) ** 1.4 * 420; spread = 16 + (y - 560) * 0.55; x = 430 + (y - 560) * 0.35 + r.gauss(0, spread * 0.5); w_ = r.uniform(8, 22) + (y - 560) * 0.1
        o.append(f'<path d="M{x-w_/2:.0f},{y:.0f} h{w_:.0f}" stroke="#FFF0D4" stroke-width="{1.5+(y-560)*0.012:.1f}" stroke-linecap="round" opacity="{r.uniform(0.35, 0.9):.2f}"/>')
    return "".join(o)

def fleet():
    o = []
    for (x, y, s_, a) in ((150, 650, 0.30, 0.8), (1700, 600, 0.13, 0.5)):
        o.append(f'<g transform="translate({x},{y}) scale({s_})">{G.mast_sail(1.3)}{G.hull(1.0, shields=True, oars=True)}</g>')
    return "".join(o)

def f7_fg():
    """Ön plan: kendi gemimizin küpeştesi (kaplama dokusu, kalkanlar, halat) ve pruva."""
    o = [TEXD]
    gun = "M-20,1080 L-20,890 Q500,850 1100,910 Q1300,936 1440,1000 L1480,1080 Z"
    o.append(f'<path d="{gun}" fill="#5A3E26" filter="url(#t_ahsap)"/><path d="{gun}" fill="none" stroke="{INK}" stroke-width="10"/>')
    for k in range(5):
        o.append(f'<path d="M-20,{910+k*36} Q500,{872+k*38} 1100,{932+k*34} Q1300,{958+k*30} 1450,{1020+k*24}" stroke="#2E1E12" stroke-width="5" fill="none"/>'
                 f'<path d="M-20,{916+k*36} Q500,{878+k*38} 1100,{938+k*34}" stroke="#8A6A46" stroke-width="2" fill="none" opacity="0.5"/>')
        for j in range(14):
            x = 40 + j * 100; o.append(f'<circle cx="{x}" cy="{904 + k*37 - x*0.03 + (x/1100)**2*40:.0f}" r="3.5" fill="#2A1A10"/>')
    o.append('<path d="M-20,890 Q500,850 1100,910 Q1300,936 1440,1000" stroke="#1A1410" stroke-width="22" fill="none"/><path d="M-20,886 Q500,846 1100,906 Q1300,932 1440,996" stroke="#9A7448" stroke-width="10" fill="none"/>')
    o.append('<path d="M-20,882 Q500,842 1100,902" stroke="#F4D8B0" stroke-width="3" fill="none" opacity="0.6"/>')   # güneşli kenar
    cols = [("#8E3B2E", "#D8C8A0"), ("#2F4C6E", "#D8C8A0"), ("#5A6A3A", "#C9A25A"), ("#C8B080", "#4A3A2A")]
    for k, x in enumerate((90, 330, 570, 810)):   # küpeşte kalkanları (yarısı kadraj altında)
        y = 900 + (x / 1100) ** 2 * 30 - x * 0.03 + 70; c1, c2 = cols[k]
        o.append(f'<g transform="translate({x},{y:.0f}) scale(0.95)">' + KL.shield_svg(c1, c2, style=k % 3).replace('translate(70,-330) scale(0.62)', 'translate(0,0) scale(0.75)') + '</g>')
    # halat: küpeşteden pruvaya
    o.append('<path d="M1000,912 Q1200,880 1390,780" stroke="#1A1410" stroke-width="9" fill="none"/><path d="M1000,912 Q1200,880 1390,780" stroke="#B8A070" stroke-width="5" fill="none" stroke-dasharray="7 3"/>')
    return "".join(o)

def f7():
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    draw(c, svg_sprite(f7_sky()), 0, 0, 1.0)
    glow(c, 430, 330, 520, "#FFD8A0", 0.35); glow(c, 430, 330, 160, "#FFF4E0", 0.5)
    draw(c, blurred(svg_sprite(f7_clouds()), 5), 0, 0, 1.0)
    rays(c, 430, 330, 20, 1100, 70, 9, "#FFE8C0", 0.10, t or 0.0)
    draw(c, svg_sprite(f7_sea()), 0, 0, 1.0)
    draw(c, svg_sprite(monastery_isle()), 0, 0, 1.0)
    fl_ = blurred(svg_sprite(fleet()), 1.2); draw(c, fl_, 0, 0, 1.0); draw(c, tinted(fl_, "#C4C8CC"), 0, 0, 1.0, a=0.3)
    fog_ = cloud_band(73, 14, -100, 2000, 548, 610, "#E4E2DC", "#F6EADA", 0.32, rx=(220, 480), ry=(14, 30)) + cloud_band(74, 8, 200, 1500, 470, 520, "#E8E4DC", "#F6EADA", 0.22, rx=(160, 360), ry=(10, 20))
    draw(c, blurred(svg_sprite(fog_), 8), 0, 0, 1.0)
    glow(c, 520, 470, 380, "#FFD8A8", 0.12)
    # martılar (yakından uzağa, kanat açıları farklı)
    birds = "".join(gull(x, y, s_, f_, rot=r_) for x, y, s_, f_, r_ in ((1180, 300, 0.55, 0.2, -6), (1330, 250, 0.4, 1.0, 4), (1060, 250, 0.3, 0.5, 0), (1400, 330, 0.26, 0.8, -8), (740, 230, 0.22, 0.1, 6)))
    draw(c, svg_sprite(birds), 0, 0, 1.0)
    # küçük keşişler (habersiz, sabah işi): model gövdesi + cübbe
    for k, (x, y, f_) in enumerate(((680, 432, 1), (1060, 402, -1))):
        sp = full(monk(k * 3 + 1), "neutral", 0.9, facing=f_); draw(c, sp, x, y, 0.06); draw(c, robe(0.9, f_), x, y, 0.06)
    # ön plan: küpeşte + pruva (onaylı ejder başı) — güneşe karşı, gölgede ve hafif alan derinliği
    fgs = svg_sprite(f7_fg()); fb = blurred(fgs, 4); draw(c, fb, 0, 0, 1.0); draw(c, tinted(fb, "#1A1E26"), 0, 0, 1.0, a=0.5)
    draw(c, svg_sprite(f'<g transform="translate(1500,1120) scale(2.2)">{G.dragon_head(0, 0, 1.0)}</g>'), 0, 0, 1.0)
    glow(c, 1560, 560, 260, "#FFD8A8", 0.10)
    # pruva köpüğü ve serpinti (ön planda)
    r = R_(79)
    for k in range(70):
        x = 1560 + r.gauss(0, 120); y = 900 + r.uniform(-260, 160); rr = r.uniform(2, 9)
        c.drawCircle(x, y, rr, skia.Paint(AntiAlias=True, Color4f=col("#F2F6F8", r.uniform(0.35, 0.85))))
    draw(c, blurred(svg_sprite(gull(260, 190, 1.6, 0.4, rot=-10)), 6), 0, 0, 1.0)   # ön planda bulanık martı
    for k in range(10):   # objektife sıçramış damlalar
        x, y, rr = r.uniform(1300, 1900), r.uniform(150, 900), r.uniform(10, 26)
        c.drawCircle(x, y, rr, skia.Paint(AntiAlias=True, Color4f=col("#F4F8FA", 0.12), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 4)))
    card_at(c, "İNGİLTERE", 1250, 140, "Lindisfarne · 793")
    finish(c, cold=True, warm=0.10); return s

# =============================================================== f9 · Floki, Jarl'ın salonunda meydan okumayı iletir
SIGGYc = dict(ASLv, hair="#E2CC96", brow_c="#A88E5A", iris="#6A8AA0", tunic="#5A2436", trim="#C9A25A", cloak="#2A1E26", fur_collar="#D8D0C2", skin="#F2D4BA")

def hearth(x, y, s=1.0):
    """Uzun ocak: taş çerçeve, kor yatağı, kütükler, alevler (yerel taban ortası)."""
    r = R_(91); o = [TEXD, f'<g transform="translate({x},{y}) scale({s})">', '<ellipse cx="0" cy="18" rx="420" ry="46" fill="#000" opacity="0.45"/>']
    o.append('<path d="M-400,0 Q-410,-40 -360,-52 L360,-52 Q410,-40 400,0 Q0,30 -400,0 Z" fill="#1E1410"/>')
    o.append('<path d="M-360,-40 L360,-40 L340,-8 L-340,-8 Z" fill="#E0641E" opacity="0.9"/><path d="M-320,-34 L320,-34 L300,-14 L-300,-14 Z" fill="#FFB050" opacity="0.8"/>')   # kor
    for k in range(9):   # kütükler
        xx = -300 + k * 75; o.append(f'<g transform="translate({xx},-30) rotate({r.uniform(-12,12):.0f})"><rect x="-60" y="-12" width="120" height="24" rx="11" fill="#3A2416" stroke="#0A0604" stroke-width="4"/><path d="M-50,-4 H50" stroke="#FF8A2A" stroke-width="3" opacity="0.7"/></g>')
    for k in range(26):   # çevre taşları (ön yüzleri ateş ışığında)
        a = k / 26; xx = -410 + a * 820; yy = 4 + 22 * math.sin(a * math.pi); w_ = r.uniform(30, 44)
        o.append(f'<path d="M{xx-w_/2:.0f},{yy+10:.0f} Q{xx-w_/2:.0f},{yy-16:.0f} {xx:.0f},{yy-18:.0f} Q{xx+w_/2:.0f},{yy-16:.0f} {xx+w_/2:.0f},{yy+10:.0f} Z" fill="#5A4E46" stroke="#0A0604" stroke-width="3"/>'
                 f'<path d="M{xx-w_/3:.0f},{yy-12:.0f} Q{xx:.0f},{yy-20:.0f} {xx+w_/3:.0f},{yy-12:.0f}" stroke="#FFAA60" stroke-width="3" fill="none" opacity="0.7"/>')
    o.append('</g>'); return "".join(o)

def flames(c, x0, x1, base, h, t, seed=0, a=1.0, soft=True):
    if soft:   # yumuşak alev halesi (bulanık katman)
        c.saveLayer(None, skia.Paint(ImageFilter=skia.ImageFilters.Blur(14, 14)))
        flames(c, x0 - 20, x1 + 20, base, h * 1.25, t, seed + 50, a * 0.8, soft=False); c.restore()
    for layer, (colr, sc_, a_) in enumerate((("#C8401A", 1.0, 0.85), ("#F08A2A", 0.72, 0.9), ("#FFD27A", 0.42, 0.95))):
        n = int((x1 - x0) / 34)
        for j in range(n):
            r_ = R_(j * 7 + layer + seed); fl = 0.75 + 0.25 * math.sin((t or 0) * (7 + j % 3) + j * 1.9)
            x = x0 + (j + 0.5) * (x1 - x0) / n + r_.uniform(-12, 12); hh = h * (0.35 + 0.8 * r_.random() ** 1.6) * fl * sc_ * (0.55 + 0.45 * math.sin(math.pi * (j + 0.5) / n)); w_ = 24 * sc_ + 6
            p = skia.Path(); p.moveTo(x - w_, base); p.cubicTo(x - w_, base - hh * 0.5, x - w_ * 0.2, base - hh * 0.7, x + 6 * math.sin((t or 0) * 5 + j), base - hh)
            p.cubicTo(x + w_ * 0.3, base - hh * 0.65, x + w_, base - hh * 0.45, x + w_, base); p.close()
            c.drawPath(p, skia.Paint(Color4f=col(colr, a_ * a), AntiAlias=True))

def hall_fg_left():
    """Ön plan oymalı direk + asılı kürk (bulanık)."""
    o = [TEXD, '<path d="M0,0 L170,0 L170,1080 L0,1080 Z" fill="#2A1C12" filter="url(#t_ahsap)"/><path d="M170,0 L170,1080" stroke="#0A0604" stroke-width="10"/>']
    for k in range(7):
        y = 100 + k * 140; o.append(f'<path d="M30,{y} q50,-40 100,0 q-50,40 -100,0 Z M50,{y-30} q30,60 60,0" stroke="#0E0804" stroke-width="7" fill="none"/>')
    o.append('<path d="M130,0 L170,0 L170,1080 L130,1080 Z" fill="#FF9A50" opacity="0.18"/>')
    return "".join(o)

def hall_fg_right():
    """Sağ ön plan: masa ucu, içki boynuzu, tahta kâse, ekmek; arkada asılı kalkan."""
    o = [TEXD, '<path d="M1560,1080 L1600,860 L1920,830 L1920,1080 Z" fill="#3A2818" filter="url(#t_ahsap)"/><path d="M1600,860 L1920,830" stroke="#0A0604" stroke-width="10"/><path d="M1600,868 L1920,838" stroke="#C88A50" stroke-width="4" opacity="0.6"/>']
    o.append('<g transform="translate(1700,840) rotate(-14)"><path d="M-60,0 Q-40,-50 40,-60 L52,-44 Q-10,-34 -40,8 Z" fill="#D8C8A0" stroke="#0A0604" stroke-width="5"/><path d="M36,-58 l16,14" stroke="#B08A3A" stroke-width="8"/></g>')
    o.append('<g transform="translate(1830,826)"><path d="M-50,0 Q0,40 50,0 Z" fill="#6A4428" stroke="#0A0604" stroke-width="5"/><ellipse cx="0" cy="0" rx="50" ry="10" fill="#4A2A18" stroke="#0A0604" stroke-width="4"/></g>')
    o.append('<g transform="translate(1640,850)"><ellipse rx="44" ry="20" fill="#B88A52" stroke="#0A0604" stroke-width="5"/><path d="M-30,-6 q30,-14 60,0" stroke="#7A5A32" stroke-width="3" fill="none"/></g>')
    return "".join(o)

def hall_floor():
    """Salon zemini: sıkıştırılmış toprak, saman/hasır, kürsü önünde ayı postu, ayak izleri."""
    r = R_(95); o = [TEXD, '<defs>' + gradient("fl9", [(0, "#4A3A2A"), (1, "#2A1E14")]) + '</defs>']
    o.append('<path d="M0,1080 L300,800 L1620,800 L1920,1080 Z" fill="url(#fl9)" opacity="0.55"/>')
    for k in range(260):
        y = r.uniform(810, 1070); x = r.uniform(300 - (y - 800) * 1.1, 1620 + (y - 800) * 1.1); a = r.uniform(-0.5, 0.5); l = 6 + (y - 800) * 0.06
        o.append(f'<path d="M{x:.0f},{y:.0f} l{l*math.cos(a):.0f},{l*math.sin(a):.0f}" stroke="{r.choice(["#A08A5A", "#7A6440", "#C0A870"])}" stroke-width="{1.5 + (y-800)*0.006:.1f}" opacity="0.65"/>')
    # ayı postu (kürsü önü)
    o.append('<g transform="translate(1080,905)"><path d="M-170,0 Q-200,-30 -150,-46 Q-120,-70 -60,-60 Q0,-80 60,-62 Q130,-72 160,-44 Q210,-24 180,4 Q200,30 150,40 Q80,56 0,50 Q-90,58 -150,40 Q-200,30 -170,0 Z" fill="#4A3424" filter="url(#t_kurk)"/>'
             '<path d="M-170,0 Q-200,-30 -150,-46 Q-120,-70 -60,-60 Q0,-80 60,-62 Q130,-72 160,-44 Q210,-24 180,4 Q200,30 150,40 Q80,56 0,50 Q-90,58 -150,40 Q-200,30 -170,0 Z" fill="none" stroke="#0E0804" stroke-width="5"/>'
             '<path d="M-140,-40 Q0,-66 140,-40" stroke="#C8783A" stroke-width="3" fill="none" opacity="0.5"/></g>')
    return "".join(o)

def f9():
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    draw(c, blurred(place(P7.greathall(0.9)), 2), 0, 0, 1.0)
    draw(c, blurred(svg_sprite(hall_floor()), 1), 0, 0, 1.0)
    rays(c, 820, -40, 98, 1000, 10, 4, "#BFD4F0", 0.10, t or 0.0)   # duman deliğinden soğuk ışık
    # arka sıralar: saray halkı (model gövdeleri, rastgele), iki yanda
    army(c, "ragnar", [(800, 0.50, 6, 0.10)], t, seed0=92, facing=1, x0=180, x1=620)
    army(c, "ragnar", [(800, 0.50, 6, 0.10)], t, seed0=93, facing=-1, x0=1320, x1=1760)
    # muhafızlar kürsünün iki yanında
    for k, (x, f_) in enumerate(((760, 1), (1300, -1))):
        sp = full(dict(KL.soldier_spec(130 + k, "ragnar"), _arm_up=False), "cold", 0.9, facing=f_, look=0.5 * f_)
        rim(c, sp, x, 870, 0.66, "#FFB070", dx=-4 * f_, dy=-2, a=0.5); draw(c, sp, x, 870, 0.66); shade_side(c, sp, x, 870, 0.35, x + 120 * f_, x - 120 * f_, "#140A06")
    # Siggy benzeri jarl karısı: Haraldson'un arkasında, endişeli
    SG = full(SIGGYc, ex("worry", IF.blink_at(1.1)), 0.9, facing=-1, look=-0.6)
    rim(c, SG, 1200, 880, 0.74, "#FFB070", dx=-4, dy=-2, a=0.6); draw(c, SG, 1200, 880, 0.74); shade_side(c, SG, 1200, 880, 0.4, 1080, 1300, "#140A06")
    # Jarl Haraldson: kürsü önünde ayakta, soğuk öfke
    HS = full(HARALD, ex("angry", IF.blink_at(0.6)), 1.0, facing=-1, look=-0.7)
    soft_shadow(c, 1040, 920, 130, 18, 0.5)
    with live(c, 1040, 930, phase=0.6, breathe=0.005):
        rim(c, HS, 1040, 930, 0.86, "#FFC080", dx=-6, dy=-3, a=0.85); draw(c, HS, 1040, 930, 0.86); shade_side(c, HS, 1040, 930, 0.45, 920, 1180, "#140A06")
    card_at(c, "JARL HARALDSON", 1290, 150)
    # ocak: ortada, kahramanlar arasında
    draw(c, svg_sprite(hearth(840, 975, 0.78)), 0, 0, 1.0)
    flames(c, 600, 1080, 953, 160, t, seed=3)
    glow(c, 840, 900, 560, "#FF7A2A", 0.30); glow(c, 840, 950, 240, "#FFC070", 0.35)
    for j in range(46):
        q = (((t or 0) * 0.3 + j / 46) % 1.0); rq = R_(j + 500)
        c.drawCircle(840 + rq.uniform(-240, 240) + 30 * math.sin(q * 6 + j), 960 - 760 * q, 3.2 * (1 - q) + 0.8, skia.Paint(Color4f=col("#FFC070", 0.9 * (1 - q)), AntiAlias=True))
    draw(c, blurred(place(cloud_band(94, 8, 400, 1200, 300, 760, "#5A4A40", "#7A6656", 0.18, rx=(80, 200), ry=(40, 90))), 14), 0, 0, 1.0)   # ocak dumanı
    # Floki: ön planda solda, Ragnar'ın kol halkasını Jarl'a uzatıyor (meydan okuma nişanı)
    FL = full(dict(FLOv, _arm_up=True, _hand_extra=RING_UP), ex("smug", IF.blink_at(0.5)), 1.0, facing=1, look=0.8)
    fx_, fy_ = 380, 1090
    soft_shadow(c, fx_, fy_ - 24, 150, 20, 0.55)
    with live(c, fx_, fy_, phase=0.5, breathe=0.006):
        rim(c, FL, fx_, fy_, 1.05, "#FFB070", dx=7, dy=-3, a=0.9); rim(c, FL, fx_, fy_, 1.05, "#9EB8D8", dx=-5, dy=-4, a=0.45)
        draw(c, FL, fx_, fy_, 1.05); shade_side(c, FL, fx_, fy_, 0.5, fx_ + 160, fx_ - 220, "#0E0806")
    hx, hy = 600, 395   # halka
    bloom_spot(c, hx, hy, 70, "#FFE6A0", 0.55); glow(c, hx, hy, 160, "#FFC860", 0.22)
    # ön plan çerçeve
    draw(c, blurred(svg_sprite(hall_fg_left()), 6), 0, 0, 1.0)
    draw(c, blurred(svg_sprite(hall_fg_right()), 5), 0, 0, 1.0)
    card_at(c, "FLOKİ", 420, 150, "Ragnar'ın meydan okuması")
    finish(c, cold=False, warm=0.06); return s

# =============================================================== f10 · Jarl düşüyor (holmgang sonrası, alçak açı)
AXE_DOWN = KL.BEARD_AXE.replace('translate(HX,HY)', 'translate(HX,HY) scale(-1,1) rotate(196)')

def f10_bg():
    r = R_(100); o = [TEXD, '<defs>' + gradient("s10", [(0, "#4E5A68"), (0.5, "#7E8A96"), (1, "#B4BEC6")]) + '</defs>', '<rect width="1920" height="760" fill="url(#s10)"/>']
    o.append(mountain_range(101, -40, 1960, 640, 330, 110, "#5A6672", "#7A8692", snow="#D8E0E6", light=-1, snow_y=430, stroke="#3A4450", cid="m10"))
    o.append(mountain_range(103, -40, 1960, 660, 470, 60, "#3E4A40", "#56624E", snow="#B8C2C6", light=-1, snow_y=500, stroke="#28302A", cid="n10"))
    # fiyort ve uzak evler (kar kaplı saz damlar)
    o.append('<rect y="600" width="1920" height="80" fill="#5E7080"/><path d="M0,604 H1920" stroke="#9AAAB8" stroke-width="3" opacity="0.6"/>')
    for k, (x, w_) in enumerate(((180, 160), (420, 120), (1500, 180), (1760, 130))):
        o.append(f'<g transform="translate({x},650)"><rect x="{-w_/2}" y="-40" width="{w_}" height="40" fill="#4A3A2C"/><path d="M{-w_/2-14},-36 Q0,-96 {w_/2+14},-36 Z" fill="#E2E8EC" stroke="#3A3A3A" stroke-width="3"/>'
                 f'<path d="M0,-90 q-12,-30 6,-50 q14,-20 -2,-46" stroke="#C8CED2" stroke-width="10" fill="none" opacity="0.5"/></g>')
    # karlı arena zemini (çiğnenmiş, ayak izi, sürüklenme izi)
    o.append('<defs>' + gradient("g10", [(0, "#C8D2DA"), (0.4, "#DDE4EA"), (1, "#B4C0CA")]) + '</defs>')
    o.append('<path d="M0,690 Q960,668 1920,690 L1920,1080 L0,1080 Z" fill="url(#g10)"/>')
    o.append('<path d="M200,1080 Q600,760 960,750 Q1340,760 1720,1080 Z" fill="#A8B0B6" opacity="0.45"/>')   # çiğnenmiş, kirli kar
    for k in range(26):   # kar sırtları ve mavi gölgeli kümeler (rüzgâr savruğu)
        x = r.uniform(-100, 1900); y = r.uniform(700, 1060); w_ = r.uniform(80, 240) * (0.5 + (y - 690) / 400); h_ = w_ * 0.12
        o.append(f'<path d="M{x-w_:.0f},{y:.0f} Q{x:.0f},{y-h_*2:.0f} {x+w_:.0f},{y:.0f} Z" fill="#EEF3F6"/><path d="M{x-w_*0.2:.0f},{y-h_*0.9:.0f} Q{x+w_*0.5:.0f},{y-h_*0.6:.0f} {x+w_:.0f},{y:.0f}" stroke="#8E9EB0" stroke-width="{2+h_*0.15:.1f}" fill="none" opacity="0.6"/>')
    for k in range(120):   # kar grenleri
        x = r.uniform(0, 1920); y = r.uniform(700, 1080); o.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r.uniform(1,2.5):.1f}" fill="#8E9AA6" opacity="0.5"/>')
    for k in range(70):
        x = r.uniform(250, 1700); y = r.uniform(760, 1060); s_ = 0.5 + (y - 740) / 400
        o.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{14*s_:.0f}" ry="{5*s_:.0f}" fill="#7E8890" opacity="0.55"/><path d="M{x-12*s_:.0f},{y-3*s_:.0f} q{12*s_:.0f},-{5*s_:.0f} {24*s_:.0f},0" stroke="#F4F8FA" stroke-width="2" fill="none" opacity="0.7"/>')
    for k in range(40):   # çamur lekeleri
        x = r.uniform(300, 1650); y = r.uniform(780, 1060); o.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r.uniform(10,40):.0f}" ry="{r.uniform(3,9):.0f}" fill="#5E5448" opacity="{r.uniform(0.2,0.45):.2f}"/>')
    o.append('<path d="M1260,1040 Q1180,960 1120,900" stroke="#6E7880" stroke-width="18" fill="none" opacity="0.4" stroke-linecap="round"/>')   # diz sürüklenme izi
    # holmgang alanını belirleyen fındık dalı kazıklar (zemine giren)
    for x, y in ((420, 900), (1500, 905), (560, 770), (1360, 772)):
        sc = 0.6 + (y - 760) / 300
        o.append(f'<g transform="translate({x},{y}) scale({sc:.2f})"><ellipse cx="0" cy="2" rx="22" ry="6" fill="#4A5058" opacity="0.6"/><path d="M-6,0 L-4,-110 L6,-110 L8,0 Z" fill="#5A4030" stroke="#1A1410" stroke-width="4"/><path d="M-4,-110 L1,-124 L6,-110" fill="#7A5A40" stroke="#1A1410" stroke-width="3"/><path d="M-8,-6 Q1,6 10,-6" fill="#E8EEF2"/></g>')
    return "".join(o)

def f10_fg():
    """Ön plan: kalkan duvarının arkadan görünen kenarları + mızrak sapları (bulanık)."""
    o = []
    cols = [("#8E3B2E", "#D8C8A0"), ("#2F4C6E", "#C9A25A"), ("#5A6A3A", "#D8C8A0"), ("#3A3A38", "#B8302A")]
    for k, (x, y, sc) in enumerate(((60, 1040, 1.9), (300, 1100, 1.6), (1640, 1100, 1.6), (1880, 1040, 1.9))):
        c1, c2 = cols[k]
        o.append(f'<g transform="translate({x},{y}) scale({sc})">' + KL.shield_svg(c1, c2, style=k % 3).replace('translate(70,-330) scale(0.62)', 'translate(0,0) scale(0.75)') + '</g>')
    for x, a in ((170, -6), (1770, 7)):
        o.append(f'<path d="M{x},1080 L{x + a*60},40" stroke="#1A1410" stroke-width="22"/><path d="M{x},1080 L{x + a*60},40" stroke="#6A5038" stroke-width="12"/>')
    return "".join(o)

def f10():
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    c.save(); c.translate(960, 540); c.rotate(-2.2); c.scale(1.06, 1.06); c.translate(-960, -580)   # hafif eğik kadraj (gerilim)
    bgs = f10_bg(); i_ = bgs.index('<g transform="translate(180,650)">') if '<g transform="translate(180,650)">' in bgs else None
    draw(c, svg_sprite(bgs), 0, 0, 1.0)
    clouds = (cloud_band(104, 14, -200, 2100, 90, 330, "#5E6A78", "#8A96A2", 0.9, lit_dy=10, rx=(220, 460), ry=(40, 90))
              + cloud_band(105, 10, -200, 2100, 300, 470, "#9AA4AE", "#C4CCD2", 0.55, lit_dy=6, rx=(200, 420), ry=(14, 30)))
    draw(c, blurred(svg_sprite(clouds), 12), 0, 0, 1.0)
    glow(c, 560, 110, 300, "#F4EEDC", 0.25)   # bulut yarığı
    rays(c, 560, 90, 72, 1000, 30, 8, "#F4F0E0", 0.06, t or 0.0)
    # kalkan çemberi: üç derinlik sırası (model gövdeleri), iki yarı merkeze bakar
    army(c, "ragnar", [(700, 0.36, 10, 0.12), (740, 0.46, 8, 0.06)], t, seed0=111, facing=1, x0=-40, x1=860)
    army(c, "ragnar", [(700, 0.36, 10, 0.12), (740, 0.46, 8, 0.06)], t, seed0=112, facing=-1, x0=1060, x1=1960)
    fill(c, "#C8D2DC", 0.06)
    # Lagertha ve Bjorn kalabalığın önünde (sol), Rollo (sağ)
    for sp, x, y, f_, sc, e in ((LAGv, 250, 800, 1, 0.58, "determined"), (dict(BJv, _scale_child=True), 350, 808, 1, 0.50, "awe"), (ROLLO, 1690, 800, -1, 0.60, "coldv")):
        d_ = full(sp, e, 0.9, facing=f_, look=0.6 * f_); rim(c, d_, x, y, sc, "#E8F0F8", dx=-3, dy=-2, a=0.5); draw(c, d_, x, y, sc)
    glow(c, 760, 960, 420, "#F6F0E0", 0.10)   # Ragnar'ın üstüne düşen ışık havuzu
    # Haraldson: dizleri üstünde, başı eğik
    HS = full(dict(HARALD, _kneel=150, _carry_svg="<g/>"), ex("shame_r", IF.blink_at(0.6)), 1.0, facing=-1, look=-0.5)
    hx_, hy_ = 1240, 990
    soft_shadow(c, hx_ - 20, hy_ - 6, 170, 20, 0.45)
    with live(c, hx_, hy_, phase=0.6, breathe=0.008):
        rim(c, HS, hx_, hy_, 0.95, "#F2F6FA", dx=-6, dy=-4, a=0.8); draw(c, HS, hx_, hy_, 0.95); shade_side(c, HS, hx_, hy_, 0.5, hx_ - 120, hx_ + 200, "#1A2430")
    breath(c, hx_ - 62, 686, 0.9, 0.6, d=-1)
    # düşen kılıç: karda yarı gömülü, soğuk parıltı
    sw = ('<g transform="translate(950,958) rotate(-7) scale(0.85)"><ellipse cx="0" cy="12" rx="190" ry="14" fill="#6E7880" opacity="0.5"/>'
          '<path d="M-170,4 L120,-4 L150,2 L120,8 L-170,10 Z" fill="#C8D2DA" stroke="#1A1410" stroke-width="5"/><path d="M-160,2 L120,-2" stroke="#F4F8FC" stroke-width="2"/><path d="M-150,6 L120,6" stroke="#7A8690" stroke-width="2"/>'
          '<rect x="-196" y="-26" width="16" height="64" rx="4" fill="#8A7A5A" stroke="#1A1410" stroke-width="4"/><rect x="-250" y="-4" width="56" height="16" rx="5" fill="#4A2A1A" stroke="#1A1410" stroke-width="4"/><circle cx="-258" cy="4" r="11" fill="#C9A25A" stroke="#1A1410" stroke-width="4"/>'
          '<path d="M-60,12 q30,-10 60,2 q30,8 70,-2" stroke="#F4F8FA" stroke-width="7" fill="none"/></g>')   # üstüne düşen kar
    draw(c, svg_sprite(sw), 0, 0, 1.0); bloom_spot(c, 1050, 945, 30, "#FFFFFF", 0.6)
    # Ragnar: ayakta, balta aşağıda, Jarl'a bakar
    RGs = full(dict(RG, _arm_up=False, _hand_extra=AXE_DOWN), ex("coldv", IF.blink_at(0.2)), 1.0, facing=1, look=0.6)
    rx_, ry_ = 690, 1000
    soft_shadow(c, rx_ + 30, ry_ - 30, 190, 22, 0.5)
    with live(c, rx_, ry_, phase=0.2, breathe=0.006):
        rim(c, RGs, rx_, ry_, 0.98, "#FFF4DC", dx=-6, dy=-4, a=0.6); draw(c, RGs, rx_, ry_, 0.98); shade_side(c, RGs, rx_, ry_, 0.45, rx_ - 150, rx_ + 260, "#1A2430")
    breath(c, rx_ + 40, 516, 0.9, 0.6)
    glow(c, 560, 260, 380, "#FFF2D8", 0.10)
    snowfall(c, t, (0, 70, W, H - 70), 140, seed=10)
    c.restore()
    draw(c, blurred(svg_sprite(f10_fg()), 8), 0, 0, 1.0)
    for j in range(24):   # ön plan iri kar taneleri (bulanık)
        q = R_(j + 700); c.drawCircle(q.uniform(0, W), q.uniform(80, H - 80), q.uniform(5, 11), skia.Paint(AntiAlias=True, Color4f=col("#FFFFFF", 0.5), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 4)))
    fill(c, "#C8D2DC", 0.05); finish(c, cold=True); return s

FR = {"f6": f6, "f7": f7, "f9": f9, "f10": f10}

CROPS = {"f6": [(150, 90, 440, 560), (500, 450, 560, 400)], "f7": [(640, 110, 520, 470), (1260, 250, 600, 520)], "f9": [(230, 300, 480, 360), (900, 330, 480, 400)], "f10": [(440, 200, 520, 460), (980, 380, 520, 640)]}

if __name__ == "__main__":
    ids = sys.argv[1:] or list(FR)
    for i in ids:
        T[0] = None; p = f"{OUT3}/{i}.png"
        FR[i]().makeImageSnapshot().save(p, skia.kPNG); print("kare", i)
        for k, b in enumerate(CROPS.get(i, []), 1): crop2x(p, b, f"{OUT3}/{i}_crop{k}.png")
