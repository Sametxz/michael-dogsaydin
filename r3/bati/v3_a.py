"""Bölüm I v3, görsel ajan A: iç mekân / nesne insertleri f2, f5, f8.
python3 v3_a.py [f2 f5 f8] → bati/v3/<id>.png (+ <id>_crop1.png, <id>_crop2.png: 1920 üzerinden %200 R13 kırpması)
Ortak dosyalara yazmaz; kareler6 yardımcılarını içe aktarır.
"""
import sys, os, math, random
sys.path.insert(0, "/home/claude/r3/bati")
from kareler6 import *
import tex
from fx import light_shaft, fog
from engine import Particles

OUTV = "/home/claude/r3/bati/v3"; os.makedirs(OUTV, exist_ok=True)
TDEFS = tex.defs("ahsap", "tas", "deri", "metal", "kurk", "keten", "yun")

# ------------------------------------------------------------------ ortak SVG yardımcıları
def beam(c, x0, y0, w0, x1, y1, w1, color="#F2F6F8", a=0.3, blur=8):
    """Keskin kenarlı ışık huzmesi (Tanrı ışını): üstte yoğun, altta söner."""
    dx, dy = x1 - x0, y1 - y0; L = math.hypot(dx, dy); nx, ny = -dy / L, dx / L
    p = skia.Path(); p.moveTo(x0 + nx * w0 / 2, y0 + ny * w0 / 2); p.lineTo(x1 + nx * w1 / 2, y1 + ny * w1 / 2)
    p.lineTo(x1 - nx * w1 / 2, y1 - ny * w1 / 2); p.lineTo(x0 - nx * w0 / 2, y0 - ny * w0 / 2); p.close()
    sh = skia.GradientShader.MakeLinear([(x0, y0), (x1, y1)], [col(color, a).toColor(), col(color, a * 0.55).toColor(), col(color, 0).toColor()], [0, 0.6, 1])
    c.drawPath(p, skia.Paint(Shader=sh, BlendMode=skia.BlendMode.kScreen, AntiAlias=True, MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, blur)))

def jit_poly(pts, r, k):
    rr = random.Random(k)
    return "M" + " L".join(f"{x + rr.uniform(-r, r):.0f},{y + rr.uniform(-r, r):.0f}" for x, y in pts) + " Z"

GRAD = ('<defs>'
        '<linearGradient id="gold" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFF0B0"/><stop offset="0.3" stop-color="#E8B84E"/><stop offset="0.7" stop-color="#A8741E"/><stop offset="1" stop-color="#5E3C0E"/></linearGradient>'
        '<linearGradient id="goldv" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFE9A0"/><stop offset="0.45" stop-color="#D9A440"/><stop offset="1" stop-color="#7A5214"/></linearGradient>'
        '<linearGradient id="goldh" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#FFE9A0"/><stop offset="0.4" stop-color="#D9A440"/><stop offset="1" stop-color="#6E4810"/></linearGradient>'
        '<linearGradient id="silv" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#F2F6F8"/><stop offset="0.35" stop-color="#B8C0C6"/><stop offset="0.75" stop-color="#6E767E"/><stop offset="1" stop-color="#3E444A"/></linearGradient>'
        '<radialGradient id="gem_r" cx="0.35" cy="0.35" r="0.7"><stop offset="0" stop-color="#FF9A8A"/><stop offset="0.4" stop-color="#B0201A"/><stop offset="1" stop-color="#4A0806"/></radialGradient>'
        '<radialGradient id="gem_b" cx="0.35" cy="0.35" r="0.7"><stop offset="0" stop-color="#A8D0FF"/><stop offset="0.4" stop-color="#2A4E9E"/><stop offset="1" stop-color="#0E1A40"/></radialGradient>'
        '<radialGradient id="gem_g" cx="0.35" cy="0.35" r="0.7"><stop offset="0" stop-color="#B8F0C0"/><stop offset="0.4" stop-color="#2A8A4A"/><stop offset="1" stop-color="#0A3018"/></radialGradient>'
        '<radialGradient id="gem_a" cx="0.35" cy="0.35" r="0.7"><stop offset="0" stop-color="#FFE6A0"/><stop offset="0.4" stop-color="#D88A20"/><stop offset="1" stop-color="#6A3006"/></radialGradient>'
        '<radialGradient id="soft" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#000" stop-opacity="0.55"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>'
        '</defs>')

def gem(x, y, r, kind="r"):
    return (f'<circle cx="{x}" cy="{y}" r="{r+3}" fill="#5A3A10" stroke="{INK}" stroke-width="3"/>'
            f'<circle cx="{x}" cy="{y}" r="{r}" fill="url(#gem_{kind})" stroke="{INK}" stroke-width="2.5"/>'
            f'<ellipse cx="{x-r*0.35:.1f}" cy="{y-r*0.4:.1f}" rx="{r*0.28:.1f}" ry="{r*0.18:.1f}" fill="#FFFFFF" opacity="0.85"/>')

def braid(x, y, w, h, light, dark, n=None, sw=None):
    """İki iplikli Insular örgü şeridi (yatay)."""
    n = n or max(2, int(w / (h * 1.4))); sw = sw or h * 0.32; step = w / n; o = []
    for ph in (0, math.pi):
        d = f"M{x},{y + h/2 + h*0.36*math.sin(ph):.1f}"
        for k in range(1, n * 8 + 1):
            xx = x + k * step / 8; yy = y + h / 2 + h * 0.36 * math.sin(ph + k * math.pi / 4)
            d += f" L{xx:.1f},{yy:.1f}"
        o.append((d, ph))
    s = ""
    for d, ph in o: s += f'<path d="{d}" stroke="{dark}" stroke-width="{sw+5:.1f}" fill="none" stroke-linejoin="round"/>'
    for d, ph in o: s += f'<path d="{d}" stroke="{light}" stroke-width="{sw:.1f}" fill="none" stroke-linejoin="round"/>'
    # üstten geçişler: her yarım dalgada bir ipliği yeniden çiz (alt-üst etkisi)
    for k in range(n * 2):
        cx = x + (k + 0.5) * step / 2
        s += f'<rect x="{cx - step*0.12:.1f}" y="{y + h*0.3:.1f}" width="{step*0.24:.1f}" height="{h*0.4:.1f}" fill="{light}" opacity="0"/>'
    return s

def drip_candle(x, y, hgt=150, w=30, lit=True, seed=1):
    r = random.Random(seed); o = [f'<g transform="translate({x},{y})">']
    o.append(f'<path d="M{-w/2},0 L{-w/2},{-hgt} Q0,{-hgt-8} {w/2},{-hgt} L{w/2},0 Z" fill="#E6D8B8" stroke="{INK}" stroke-width="4"/>')
    o.append(f'<path d="M{w*0.12},{-hgt+4} L{w*0.12},-4 L{w/2-2},-4 L{w/2-2},{-hgt+2} Z" fill="#B8A684" opacity="0.7"/>')   # gölge yanı
    for k in range(3):   # damlayan mum
        dx = r.uniform(-w/2 + 3, w/2 - 3); L = r.uniform(18, 60)
        o.append(f'<path d="M{dx-4:.0f},{-hgt+2} Q{dx-5:.0f},{-hgt+L:.0f} {dx:.0f},{-hgt+L+8:.0f} Q{dx+5:.0f},{-hgt+L:.0f} {dx+4:.0f},{-hgt+2} Z" fill="#F2E8CE" stroke="{INK}" stroke-width="2.5"/>')
    o.append(f'<path d="M-1,{-hgt-4} L1,{-hgt-18}" stroke="{INK}" stroke-width="3"/>')
    if lit:
        o.append(f'<path d="M0,{-hgt-62} Q14,{-hgt-30} 9,{-hgt-14} Q0,{-hgt-6} -9,{-hgt-14} Q-14,{-hgt-30} 0,{-hgt-62} Z" fill="#FFB648" stroke="#7A3A0A" stroke-width="2.5"/>'
                 f'<path d="M0,{-hgt-44} Q7,{-hgt-26} 4,{-hgt-16} Q0,{-hgt-12} -4,{-hgt-16} Q-7,{-hgt-26} 0,{-hgt-44} Z" fill="#FFF4C8"/>')
    o.append('</g>')
    return "".join(o)

def candlestick(x, y, hgt=150, seed=1):
    """Pirinç şamdan + damlayan mum. (x,y): taban."""
    o = [f'<g transform="translate({x},{y})"><ellipse cx="6" cy="4" rx="64" ry="14" fill="#000" opacity="0.35"/>'
         f'<path d="M-56,0 Q-50,-24 -14,-30 L-10,-110 Q-28,-118 -12,-128 L-8,-170 L-36,-178 L36,-178 L8,-170 L12,-128 Q28,-118 10,-110 L14,-30 Q50,-24 56,0 Z" fill="url(#goldv)" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
         f'<path d="M4,-30 L6,-110 M4,-128 L6,-168" stroke="#6E4810" stroke-width="5" opacity="0.7"/><path d="M-6,-34 L-6,-104" stroke="#FFF2C0" stroke-width="3" opacity="0.8"/>'
         f'<path d="M-44,-6 Q-30,-22 0,-24" stroke="#FFF2C0" stroke-width="3" fill="none" opacity="0.7"/></g>']
    o.append(drip_candle(x, y - 176, hgt, 30, True, seed))
    return "".join(o)


# ================================================================== f8 · Lindisfarne sunağı
def stone_wall(x0, y0, x1, y1, seed=3, wash=0.5, row=(70, 110), wd=(110, 240), base="#2E2820"):
    r = random.Random(seed); o = [f'<rect x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}" fill="{base}"/>', '<g filter="url(#t_tas)">']
    pal = ["#6E665A", "#7A7062", "#62594C", "#80776A", "#706658", "#5C5448"]
    y = y0
    while y < y1:
        h = r.uniform(*row); x = x0 - r.uniform(0, 120)
        while x < x1:
            w = r.uniform(*wd)
            pts = [(x + 5, y + 5), (x + w * 0.5, y + 3), (x + w - 5, y + 5), (x + w - 3, y + h * 0.5), (x + w - 5, y + h - 4), (x + w * 0.5, y + h - 3), (x + 5, y + h - 5), (x + 3, y + h * 0.5)]
            o.append(f'<path d="{jit_poly(pts, 5, r.random()*1e6)}" fill="{r.choice(pal)}" stroke="#241E18" stroke-width="3" stroke-linejoin="round"/>')
            x += w
        y += h
    o.append('</g>')
    # kireç badana: düzensiz, yer yer dökülmüş
    for k in range(9):
        cx, cy = r.uniform(x0, x1), r.uniform(y0, y1); rx_, ry_ = r.uniform(160, 420), r.uniform(90, 220)
        pts = [(cx + rx_ * math.cos(a) * r.uniform(0.7, 1.15), cy + ry_ * math.sin(a) * r.uniform(0.7, 1.15)) for a in [i * math.pi / 7 for i in range(14)]]
        o.append(f'<path d="{jit_poly(pts, 8, k)}" fill="#D8D0BE" opacity="{wash * r.uniform(0.35, 0.7):.2f}"/>')
    return "".join(o)

def insular_cross(x, y, s=1.0):
    """Mücevherli altın sunak haçı (Insular): halka, genişleyen kol uçları, örgü paneller, kabaşon taşlar, basamaklı kaide. (x,y) kaide altı."""
    o = [f'<g transform="translate({x},{y}) scale({s})">']
    o.append('<ellipse cx="30" cy="4" rx="150" ry="20" fill="url(#soft)"/>')
    # kaide (basamaklı)
    o.append(f'<path d="M-110,0 L-96,-36 L96,-36 L110,0 Z" fill="url(#goldh)" stroke="{INK}" stroke-width="6"/><path d="M-72,-36 L-60,-70 L60,-70 L72,-36 Z" fill="url(#goldh)" stroke="{INK}" stroke-width="6"/>')
    o.append(braid(-86, -32, 172, 24, "#F2CC6A", "#6E4810", 6, 6))
    for gx in (-40, 0, 40): o.append(gem(gx, -53, 9, "r" if gx == 0 else "b"))
    # halka (arkada)
    cy = -330
    o.append(f'<circle cx="0" cy="{cy}" r="118" fill="none" stroke="{INK}" stroke-width="40"/><circle cx="0" cy="{cy}" r="118" fill="none" stroke="url(#gold)" stroke-width="30"/>'
             f'<circle cx="0" cy="{cy}" r="118" fill="none" stroke="#7A5214" stroke-width="3" stroke-dasharray="6 10"/>')
    # gövde ve kollar (genişleyen uçlar)
    arm = "M-26,-70 L-26,{a} L-46,{b} L-46,{c} L-26,{d}".format(a=-250, b=-262, c=-300, d=-310)
    shape = ("M-24,-70 L-24,-268 L-150,-286 L-176,-306 L-176,-354 L-150,-374 L-24,-390 L-34,-520 L-50,-546 L50,-546 L34,-520 L24,-390 "
             "L150,-374 L176,-354 L176,-306 L150,-286 L24,-268 L24,-70 Z")
    o.append(f'<path d="{shape}" fill="#000" opacity="0.35" transform="translate(14,10)"/>')
    o.append(f'<path d="{shape}" fill="url(#gold)" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>')
    o.append(f'<path d="{shape}" fill="none" stroke="#FFF2C0" stroke-width="3" opacity="0.6" transform="translate(-3,-3)"/>')
    # örgü panelleri (gövde dikey, kollar yatay)
    o.append(f'<g transform="translate(-14,-90) rotate(-90)">{braid(0, 0, 160, 28, "#F6D47A", "#7A5214", 5, 7)}</g>')
    o.append(f'<g transform="translate(-14,-400) rotate(-90)">{braid(0, 0, 110, 28, "#F6D47A", "#7A5214", 4, 7)}</g>')
    o.append(braid(-150, -344, 100, 28, "#F6D47A", "#7A5214", 4, 7) + braid(50, -344, 100, 28, "#F6D47A", "#7A5214", 4, 7))
    # merkez kabarık disk + taşlar
    o.append(f'<circle cx="0" cy="{cy}" r="46" fill="url(#goldv)" stroke="{INK}" stroke-width="6"/><circle cx="0" cy="{cy}" r="34" fill="none" stroke="#7A5214" stroke-width="3" stroke-dasharray="4 5"/>')
    o.append(gem(0, cy, 24, "r"))
    for gx, gy, k in ((-160, cy, "b"), (160, cy, "b"), (0, -528, "g"), (0, -150, "a"), (0, -210, "b")):
        o.append(gem(gx, gy, 13, k))
    for ang in range(0, 360, 45):   # halka üstünde perçin taşlar
        a = math.radians(ang + 22.5); o.append(gem(118 * math.cos(a), cy + 118 * math.sin(a), 7, "a"))
    o.append('</g>')
    return "".join(o)

def chalice(x, y, s=1.0):
    o = [f'<g transform="translate({x},{y}) scale({s})"><ellipse cx="20" cy="2" rx="96" ry="14" fill="url(#soft)"/>']
    o.append(f'<path d="M-70,0 Q-66,-26 -18,-36 L-14,-90 Q-38,-100 -14,-112 L-12,-120 L12,-120 L14,-112 Q38,-100 14,-90 L18,-36 Q66,-26 70,0 Z" fill="url(#silv)" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>')
    o.append(f'<path d="M-30,-104 Q0,-116 30,-104" stroke="#D9A440" stroke-width="8" fill="none"/>' + gem(0, -101, 8, "b"))   # düğüm
    o.append(f'<path d="M-98,-250 Q-104,-150 -40,-128 Q0,-118 40,-128 Q104,-150 98,-250 Z" fill="url(#silv)" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>')
    o.append(f'<ellipse cx="0" cy="-250" rx="98" ry="18" fill="#3A3028" stroke="{INK}" stroke-width="6"/><ellipse cx="0" cy="-247" rx="84" ry="11" fill="#5A1A14"/>')   # şarap
    o.append(f'<path d="M-100,-226 Q0,-206 100,-226 L98,-196 Q0,-176 -98,-196 Z" fill="url(#goldh)" stroke="{INK}" stroke-width="4"/>')   # altın bant
    o.append(braid(-90, -218, 180, 18, "#F6D47A", "#6E4810", 7, 5))
    for k, gx in enumerate((-70, -24, 24, 70)): o.append(gem(gx, -150, 9, "rbga"[k]))
    o.append(f'<path d="M-82,-236 Q-84,-170 -48,-140" stroke="#FFFFFF" stroke-width="7" fill="none" opacity="0.75" stroke-linecap="round"/>')
    o.append('</g>')
    return "".join(o)

def gospel(x, y, s=1.0):
    """Açık İncil (Lindisfarne üslubu): sol sayfa halı sayfası, sağ sayfa büyük süslü baş harf + kırmızı nokta bezeme; kırmızı yastıkta."""
    r = random.Random(5); o = [f'<g transform="translate({x},{y}) scale({s})"><ellipse cx="20" cy="6" rx="200" ry="22" fill="url(#soft)"/>']
    o.append(f'<path d="M-200,0 Q-210,-50 -170,-62 L170,-62 Q210,-50 200,0 Q0,18 -200,0 Z" fill="#7A1E18" stroke="{INK}" stroke-width="6" filter="url(#t_yun)"/>'
             f'<path d="M-180,-14 Q0,0 180,-14" stroke="#D9A440" stroke-width="5" fill="none"/>')   # yastık
    # kapak (koyu deri, altın köşe)
    o.append(f'<path d="M-186,-56 L-176,-196 L0,-176 L176,-196 L186,-56 L0,-40 Z" fill="#4A1E10" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>')
    L = "M-172,-66 L-164,-196 Q-80,-206 -4,-184 L-4,-52 Q-90,-70 -172,-66 Z"
    R = "M172,-66 L164,-196 Q80,-206 4,-184 L4,-52 Q90,-70 172,-66 Z"
    o.append(f'<path d="{L}" fill="#EADCB6" stroke="{INK}" stroke-width="5"/><path d="{R}" fill="#F0E4C2" stroke="{INK}" stroke-width="5"/>')
    o.append('<path d="M-4,-184 L-4,-52 L4,-52 L4,-184 Z" fill="#A89070"/><path d="M-30,-180 Q-14,-110 -18,-56" stroke="#B8A27A" stroke-width="10" fill="none" opacity="0.6"/>')
    # sol: halı sayfası (haç biçimli, renkli örgü)
    o.append('<g transform="translate(-86,-126) skewY(4)">'
             '<rect x="-64" y="-56" width="128" height="104" fill="#2E4A3A" stroke="#1A1410" stroke-width="3"/>'
             '<path d="M-14,-56 V48 M14,-56 V48 M-64,-12 H64 M-64,8 H64" stroke="#C8962E" stroke-width="5"/>'
             '<rect x="-14" y="-12" width="28" height="20" fill="#B0281E"/>')
    for k in range(4):   # triskele sarmalları (göz gibi okunmasın: açık sarmal, nokta yok)
        qx, qy = (-40 if k % 2 == 0 else 40), (-34 if k < 2 else 28)
        o.append(f'<circle cx="{qx}" cy="{qy}" r="15" fill="#B0281E" stroke="#D9A440" stroke-width="3"/>')
        for j in range(3):
            a = math.radians(j * 120 + k * 30); ex_, ey_ = qx + 11 * math.cos(a), qy + 11 * math.sin(a); a2 = a + 2.2
            o.append(f'<path d="M{qx},{qy} Q{qx + 14*math.cos(a+0.9):.1f},{qy + 14*math.sin(a+0.9):.1f} {ex_:.1f},{ey_:.1f} Q{qx + 6*math.cos(a2):.1f},{qy + 6*math.sin(a2):.1f} {qx + 4*math.cos(a+0.6):.1f},{qy + 4*math.sin(a+0.6):.1f}" stroke="#F2D27A" stroke-width="2.6" fill="none"/>')
    o.append('</g>')
    # sağ: büyük baş harf + metin satırları
    o.append('<g transform="translate(86,-126) skewY(-4)">'
             '<path d="M-66,-58 L-66,42 M-46,42 L-46,-58 L-16,42 L-16,-58" stroke="#1A1410" stroke-width="13" fill="none" stroke-linejoin="round"/>'
             '<path d="M-66,-58 L-66,42 M-46,42 L-46,-58 L-16,42 L-16,-58" stroke="#3A5AA0" stroke-width="7" fill="none" stroke-linejoin="round"/>'
             '<path d="M-66,-58 Q-80,-74 -90,-60 M-16,42 Q-4,58 6,44" stroke="#C8962E" stroke-width="4" fill="none"/>'
             '<path d="M-66,-20 L-66,4 M-46,-30 L-36,0" stroke="#B0281E" stroke-width="3"/>')
    for k in range(26):
        a = k / 26 * 2 * math.pi; o.append(f'<circle cx="{-40 + 34*math.cos(a):.0f}" cy="{-8 + 54*math.sin(a):.0f}" r="2.2" fill="#B0281E"/>')
    for k in range(8):
        L_ = 56 if k < 6 else 0; x0 = 0
        o.append(f'<path d="M{x0},{-46 + k*12} H{x0 + L_ + r.uniform(-8, 6):.0f}" stroke="#3A2A1E" stroke-width="3.5" stroke-dasharray="{r.randint(6,12)} 3 {r.randint(4,9)} 3"/>')
    o.append('<path d="M-60,50 H60" stroke="#B0281E" stroke-width="3" stroke-dasharray="10 3"/></g>')
    o.append('</g>')
    return "".join(o)

def reliquary(x, y, s=1.0):
    """Ev biçimli kutsal emanet kutusu (Monymusk tipi): ahşap gövde, bronz-altın levhalar, sırt kirişi ve hayvan başı uçlar."""
    o = [f'<g transform="translate({x},{y}) scale({s})"><ellipse cx="18" cy="4" rx="140" ry="16" fill="url(#soft)"/>']
    o.append(f'<path d="M-120,0 L-120,-110 L120,-110 L120,0 Z" fill="#5A3A22" stroke="{INK}" stroke-width="6" filter="url(#t_ahsap)"/>')
    o.append(f'<path d="M-126,-110 L-96,-190 L96,-190 L126,-110 Z" fill="#4E3220" stroke="{INK}" stroke-width="6" filter="url(#t_ahsap)"/>')
    o.append(f'<path d="M-104,-188 L104,-188 L104,-206 L-104,-206 Z" fill="url(#goldh)" stroke="{INK}" stroke-width="5"/>'
             f'<path d="M-104,-198 Q-136,-214 -128,-238 Q-110,-226 -104,-206 Z M104,-198 Q136,-214 128,-238 Q110,-226 104,-206 Z" fill="url(#goldv)" stroke="{INK}" stroke-width="5"/>')
    for px in (-96, -32, 32, 96):
        o.append(f'<rect x="{px-24}" y="-96" width="48" height="74" rx="4" fill="url(#gold)" stroke="{INK}" stroke-width="4"/>' + gem(px, -60, 9, "r" if px in (-32, 32) else "a"))
    o.append(braid(-112, -176, 224, 22, "#E8C060", "#5A3A10", 9, 6))
    o.append(f'<path d="M-120,-12 H120" stroke="#C8962E" stroke-width="6"/><path d="M60,-110 L60,0 L120,0 L120,-110 Z" fill="#000" opacity="0.28"/>')
    o.append('</g>')
    return "".join(o)

def paten(x, y, s=1.0):
    return (f'<g transform="translate({x},{y}) scale({s}) rotate(-8)"><ellipse cx="10" cy="4" rx="110" ry="104" fill="#000" opacity="0.3"/>'
            f'<ellipse rx="110" ry="104" fill="url(#silv)" stroke="{INK}" stroke-width="6"/><ellipse rx="82" ry="76" fill="none" stroke="#5E666E" stroke-width="4"/>'
            f'<ellipse rx="96" ry="90" fill="none" stroke="#E8EEF2" stroke-width="2" stroke-dasharray="3 6"/>'
            f'<path d="M-14,-40 L14,-40 L14,-14 L40,-14 L40,14 L14,14 L14,40 L-14,40 L-14,14 L-40,14 L-40,-14 L-14,-14 Z" fill="none" stroke="#5E666E" stroke-width="4"/>'
            f'<path d="M-80,-40 Q-70,-80 -30,-94" stroke="#FFFFFF" stroke-width="8" fill="none" opacity="0.7" stroke-linecap="round"/></g>')

def altar_cloth(x0, x1, y0, y1):
    """Keten örtü: üstte kıvrım, önde sarkan, Celtic düğüm nakışlı alt bordür, ortada nakış madalyon, saçaklı kenar."""
    r = random.Random(8); o = []
    w = x1 - x0; hem = f"M{x0},{y0} L{x1},{y0} L{x1+10},{y1}"
    for k in range(24, -1, -1):
        xx = x1 + 10 - k * (w + 20) / 24; hem += f" Q{xx + (w+20)/48:.0f},{y1 + 14 + r.uniform(-3,3):.0f} {xx:.0f},{y1}" if k < 24 else ""
    hem += f" L{x0-10},{y1} Z"
    o.append(f'<path d="{hem}" fill="#E4DCC8" stroke="{INK}" stroke-width="6" filter="url(#t_keten)"/>')
    for k in range(14):   # dikey kıvrımlar
        xx = x0 + 40 + k * (w - 80) / 13 + r.uniform(-12, 12)
        o.append(f'<path d="M{xx:.0f},{y0+30} Q{xx + r.uniform(-14,14):.0f},{(y0+y1)/2:.0f} {xx + r.uniform(-8,8):.0f},{y1-6}" stroke="#A89C84" stroke-width="{r.uniform(5,10):.0f}" fill="none" opacity="0.55" stroke-linecap="round"/>')
    o.append(f'<path d="M{x0},{y0+6} L{x1},{y0+6}" stroke="#FFFFFF" stroke-width="5" opacity="0.6"/>')
    by = y1 - 70   # nakış bordürü
    o.append(f'<rect x="{x0}" y="{by}" width="{w}" height="46" fill="#7A1E18" stroke="{INK}" stroke-width="3"/>' + braid(x0 + 6, by + 6, w - 12, 34, "#E2B04A", "#3A0A06", int(w / 46), 9))
    o.append(f'<path d="M{x0},{by-8} H{x1} M{x0},{by+54} H{x1}" stroke="#C8962E" stroke-width="4" stroke-dasharray="14 6"/>')
    cx = (x0 + x1) / 2; my = y0 + 70   # madalyon: halkalı haç nakışı
    o.append(f'<circle cx="{cx}" cy="{my}" r="44" fill="#7A1E18" stroke="#C8962E" stroke-width="6"/><circle cx="{cx}" cy="{my}" r="26" fill="none" stroke="#E2B04A" stroke-width="5"/>'
             f'<path d="M{cx},{my-38} V{my+38} M{cx-38},{my} H{cx+38}" stroke="#E2B04A" stroke-width="9"/>')
    for k in range(int(w / 14)):   # saçak
        xx = x0 - 6 + k * 14; o.append(f'<path d="M{xx},{y1+6} l{r.uniform(-3,3):.0f},{r.uniform(12,22):.0f}" stroke="#C8BEA6" stroke-width="3"/>')
    return "".join(o)

def censer_svg(x, y):
    o = [f'<path d="M{x},70 L{x},{y-80}" stroke="#2A2018" stroke-width="5" stroke-dasharray="10 4"/>'
         f'<path d="M{x-8},70 L{x-30},{y-50} M{x+8},70 L{x+30},{y-50}" stroke="#2A2018" stroke-width="3" opacity="0.8"/>'
         f'<g transform="translate({x},{y})"><path d="M-44,-50 Q-50,-10 -26,10 L26,10 Q50,-10 44,-50 Z" fill="url(#goldv)" stroke="{INK}" stroke-width="5"/>'
         f'<path d="M-44,-50 Q0,-120 44,-50 Z" fill="url(#gold)" stroke="{INK}" stroke-width="5"/>'
         + "".join(f'<circle cx="{-24 + k*12}" cy="{-66 + abs(k-2)*6}" r="4" fill="#2A1A0A"/>' for k in range(5))
         + f'<path d="M-16,10 L-20,26 L20,26 L16,10" fill="#8A6020" stroke="{INK}" stroke-width="4"/>{gem(0, -24, 7, "r")}</g>']
    return "".join(o)

def smoke_svg(x, y, h, seed=1, a=0.35, w=40):
    r = random.Random(seed); d = f"M{x},{y}"; xx = x
    for k in range(10):
        nx = xx + r.uniform(-w, w); ny = y - (k + 1) * h / 10; d += f" Q{xx + r.uniform(-w, w):.0f},{ny + h/20:.0f} {nx:.0f},{ny:.0f}"; xx = nx
    return f'<path d="{d}" stroke="#D8D4CC" stroke-width="{r.uniform(10,18):.0f}" fill="none" opacity="{a}" stroke-linecap="round"/>'

def f8():
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0] or 0.0
    # --- 1 arka duvar: kaba taş + kireç badana, yuvarlak kemerli pencere (derin şev), boyalı örgü friz
    o = [GRAD, TDEFS, stone_wall(0, 0, 1920, 1080, seed=31, wash=0.55)]
    wx, wy, ww, wh = 470, 185, 170, 290
    o.append(f'<path d="M{wx-70},{wy+wh+30} L{wx-70},{wy+40} Q{wx+ww/2},{wy-130} {wx+ww+70},{wy+40} L{wx+ww+70},{wy+wh+30} Z" fill="#9A9284" stroke="#241E18" stroke-width="5" filter="url(#t_tas)"/>')   # şev
    for k in range(11):   # kemer taşları
        a0 = math.pi + k * math.pi / 11; a1 = a0 + math.pi / 11; cx, cy = wx + ww / 2, wy + 60
        p = [(cx + 170 * math.cos(a0), cy + 190 * math.sin(a0)), (cx + 170 * math.cos(a1), cy + 190 * math.sin(a1)), (cx + 118 * math.cos(a1), cy + 140 * math.sin(a1)), (cx + 118 * math.cos(a0), cy + 140 * math.sin(a0))]
        o.append(f'<path d="{jit_poly(p, 2, k+50)}" fill="{["#8A8274", "#7A7264"][k%2]}" stroke="#241E18" stroke-width="4"/>')
    o.append(f'<defs><linearGradient id="sky8" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9FB4C4"/><stop offset="0.7" stop-color="#E4ECF0"/><stop offset="1" stop-color="#C8D4DA"/></linearGradient></defs>'
             f'<path d="M{wx},{wy+wh} L{wx},{wy+60} Q{wx+ww/2},{wy-40} {wx+ww},{wy+60} L{wx+ww},{wy+wh} Z" fill="url(#sky8)" stroke="#241E18" stroke-width="6"/>'
             f'<ellipse cx="{wx+60}" cy="{wy+90}" rx="70" ry="18" fill="#F4F8FA" opacity="0.8"/><ellipse cx="{wx+120}" cy="{wy+150}" rx="60" ry="12" fill="#F4F8FA" opacity="0.6"/>'
             f'<path d="M{wx+ww},{wy+wh} L{wx+ww},{wy+60} Q{wx+ww-20},{wy+10} {wx+ww/2},{wy+0} L{wx+ww+60},{wy+wh+30} Z" fill="#7A7468" opacity="0.6"/>'   # şev gölgesi
             f'<path d="M{wx+20},{wy+wh-60} Q{wx+70},{wy+wh-110} {wx+ww-10},{wy+wh-70} L{wx+ww},{wy+wh} L{wx},{wy+wh} Z" fill="#9AAAB4" opacity="0.7"/>')   # dışarıda deniz ufku
    o.append(f'<path d="M{wx-80},{wy+wh+30} L{wx+ww+80},{wy+wh+30} L{wx+ww+70},{wy+wh+52} L{wx-70},{wy+wh+52} Z" fill="#8A8274" stroke="#241E18" stroke-width="5"/>')   # denizlik
    # friz: kırmızı aşı boyası bant + sarı örgü (duvarda boyalı)
    o.append(f'<rect x="0" y="512" width="1920" height="56" fill="#8A3A24" opacity="0.85"/><rect x="0" y="508" width="1920" height="64" fill="none" stroke="#2A1A10" stroke-width="3"/>'
             + braid(0, 518, 1920, 44, "#D8B060", "#4A1A0C", 44, 10).replace('<path', '<path opacity="0.85"'))
    # sağ: orta planda kemer ayağı (sütun) + nişte asılı kandil
    o.append(f'<path d="M1640,0 L1640,1080 L1920,1080 L1920,0 Z" fill="#3A332A"/>' + stone_wall(1660, 0, 1920, 1080, seed=7, wash=0.4, row=(90, 120), wd=(90, 140), base="#2A241C"))
    o.append('<path d="M1660,0 L1660,1080" stroke="#14100C" stroke-width="10"/><path d="M1660,0 L1700,0 L1700,1080 L1660,1080 Z" fill="#000" opacity="0.35"/>')
    draw(c, svg_sprite("".join(o)), 0, 0, 1.0)
    fill(c, "#0E0C10", 0.18)
    # pencere ışığı + toz (atmosfer katman 1)
    # değer yapısı: köşeler karanlık, sunak merkezi aydınlık
    sh = skia.GradientShader.MakeRadial((1000, 600), 1150, [col("#000000", 0).toColor(), col("#000000", 0).toColor(), col("#05060A", 0.62).toColor()], [0, 0.42, 1])
    c.drawRect(skia.Rect(0, 0, W, H), skia.Paint(Shader=sh))
    bloom_spot(c, wx + ww / 2, wy + 150, 200, "#E8F2FA", 0.35)

    # --- 2 sunak + nesneler
    o = [GRAD, TDEFS]
    o.append(f'<path d="M360,1080 L380,700 L1540,700 L1560,1080 Z" fill="#6A6254" stroke="{INK}" stroke-width="8" filter="url(#t_tas)"/>')   # sunak gövdesi
    for k in range(6):   # oyma kemerli arkatlar (ön yüz)
        ax = 430 + k * 180
        o.append(f'<path d="M{ax},1080 L{ax},930 Q{ax+70},850 {ax+140},930 L{ax+140},1080" fill="#4E473C" stroke="{INK}" stroke-width="5"/><path d="M{ax+10},1080 L{ax+10},934 Q{ax+70},866 {ax+130},934" stroke="#8A8272" stroke-width="3" fill="none"/>')
    o.append(f'<path d="M330,640 L1590,640 L1600,700 L320,700 Z" fill="#7E7666" stroke="{INK}" stroke-width="7" filter="url(#t_tas)"/>')   # üst tabla
    o.append(altar_cloth(380, 1540, 640, 870))
    # nesneler (sol → sağ): şamdan, İncil, haç, kadeh+patén, emanet kutusu, şamdan
    o.append(candlestick(420, 652, 120, 3))
    o.append(gospel(650, 650, 1.05))
    o.append(paten(1215, 560, 0.9))
    o.append(insular_cross(950, 655, 0.92))
    o.append(chalice(1140, 662, 0.92))
    o.append(reliquary(1380, 662, 0.9))
    o.append(candlestick(1560, 652, 140, 4))
    # gümüş sikkeler / küçük tabak (sunağın önünde)
    for k, (cx, cy) in enumerate(((800, 672), (826, 676), (850, 670), (1270, 676), (1296, 672))):
        o.append(f'<ellipse cx="{cx}" cy="{cy}" rx="16" ry="6" fill="url(#silv)" stroke="{INK}" stroke-width="3"/>')
    draw(c, svg_sprite("".join(o)), 0, 0, 1.0)
    # pencere ışığı nesnelerin sol-üstünde: altın parıltıları
    bloom_spot(c, 960, 700, 420, "#FFF4DC", 0.22)
    for x, y, r_, a in ((950, 355, 150, 0.35), (420, 456, 110, 0.55), (1560, 436, 110, 0.55), (1100, 470, 80, 0.25), (650, 520, 120, 0.18)):
        bloom_spot(c, x, y, r_, "#FFE2A0", a)
    glow(c, 420, 456, 60, "#FFB040", 0.35); glow(c, 1560, 436, 60, "#FFB040", 0.35)
    # Tanrı ışınları: pencereden sunağa çapraz (toz taşıyan, belirgin)
    for (x0_, y0_, w0, x1_, y1_, w1, a, bl) in ((wx + 40, wy + 120, 40, 820, 760, 110, 0.30, 6), (wx + 90, wy + 100, 50, 980, 720, 150, 0.36, 6),
                                             (wx + 140, wy + 140, 30, 1130, 700, 90, 0.26, 5), (wx + 85, wy + 120, 150, 950, 760, 520, 0.14, 30)):
        beam(c, x0_, y0_, w0, x1_, y1_, w1, "#EEF4F8", a, bl)

    # --- 3 tütsü (orta-ön plan) ve dumanı (atmosfer katman 2)
    sm = "".join(smoke_svg(1700 + k * 14, 470, 460, seed=k + 3, a=0.22, w=70).replace('stroke-width="', 'stroke-width="2') for k in range(5))
    sm += "".join(smoke_svg(x, 300, 240, seed=k + 20, a=0.18, w=22) for k, x in enumerate((420, 1560)))
    draw(c, blurred(svg_sprite(sm), 9), 0, 0, 1.0)
    draw(c, svg_sprite(GRAD + TDEFS + censer_svg(1720, 520)), 0, 0, 1.0)
    fog(c, t, 300, "#C8CCD0", 0.05, n=4, seed=8, h=160)
    Particles("dust", 260, seed=8, area=(520, 280, 1200, 820), color="#FFF8E8", size=(2.5, 5.5), speed=10).draw(c, t, 1.0)
    # --- 4 ön plan: bulanık büyük mum (sol) + taş sütun (sağ kenar)
    fg = (GRAD + drip_candle(170, 806, 300, 96, True, 9).replace('#E6D8B8', '#6A5238').replace('#F2E8CE', '#7A6040').replace('#B8A684', '#3A2A1A')
          + '<path d="M60,1080 L90,820 L250,820 L280,1080 Z" fill="#1A1410"/><path d="M80,830 L260,830 L250,800 L90,800 Z" fill="#2A2018"/>' + '<path d="M1830,0 L1920,0 L1920,1080 L1810,1080 Q1790,600 1830,0 Z" fill="#1E1A14"/>')
    draw(c, blurred(svg_sprite(fg), 14), 0, 0, 1.0)
    glow(c, 170, 470, 200, "#FFA040", 0.4); bloom_spot(c, 170, 480, 300, "#FFC070", 0.22)
    sh = skia.GradientShader.MakeLinear([(0, 860), (0, 1010)], [col("#000000", 0).toColor(), col("#08060A", 0.55).toColor()])
    c.drawRect(skia.Rect(0, 860, W, 1010), skia.Paint(Shader=sh))   # zemine doğru karanlık
    card_at(c, "ALTIN · GÜMÜŞ", 1290, 150, "silah yok")
    grade(c, "#FFB060", 0.04, "screen")
    finish(c, cold=False, warm=0.03); return s



# ================================================================== f2 · Jarl'ın deri haritası
RUNES = "ᚠᚢᚦᚬᚱᚴᚼᚾᛁᛅᛋᛏᛒᛘᛚᛦ"

def plank_wall(x0, x1, y0, y1, seed=2):
    r = random.Random(seed); o = ['<g filter="url(#t_ahsap)">']; x = x0
    while x < x1:
        w = r.uniform(90, 150); cc = r.choice(["#4A3222", "#43301F", "#503726", "#3E2C1C"])
        o.append(f'<rect x="{x:.0f}" y="{y0}" width="{w:.0f}" height="{y1-y0}" fill="{cc}" stroke="#160E08" stroke-width="5"/>'); x += w
    o.append('</g>')
    for k in range(40):   # budak, çatlak, çivi
        xx, yy = r.uniform(x0, x1), r.uniform(y0, y1)
        kind = r.random()
        if kind < 0.3: o.append(f'<ellipse cx="{xx:.0f}" cy="{yy:.0f}" rx="9" ry="16" fill="#2A1C10" opacity="0.7"/><ellipse cx="{xx:.0f}" cy="{yy:.0f}" rx="18" ry="30" fill="none" stroke="#2A1C10" stroke-width="3" opacity="0.5"/>')
        elif kind < 0.7: o.append(f'<path d="M{xx:.0f},{yy:.0f} q{r.uniform(-6,6):.0f},{r.uniform(40,90):.0f} {r.uniform(-4,4):.0f},{r.uniform(90,180):.0f}" stroke="#1E140A" stroke-width="2.5" fill="none" opacity="0.7"/>')
        else: o.append(f'<circle cx="{xx:.0f}" cy="{yy:.0f}" r="5" fill="#1A120A"/><circle cx="{xx-1:.0f}" cy="{yy-1:.0f}" r="2" fill="#6A5A4A"/>')
    return "".join(o)

def carved_post(x, w, y0=0, y1=1080, seed=1):
    o = [f'<rect x="{x}" y="{y0}" width="{w}" height="{y1-y0}" fill="#5A3E26" stroke="{INK}" stroke-width="7" filter="url(#t_ahsap)"/>']
    o.append(f'<g transform="translate({x + w/2 - 26},{y0 + 40}) rotate(90)">' + braid(0, -26, y1 - y0 - 80, 52, "#7A5634", "#2A1A0C", None, 13) + '</g>')
    o.append(f'<rect x="{x + w*0.62:.0f}" y="{y0}" width="{w*0.38:.0f}" height="{y1-y0}" fill="#000" opacity="0.35"/>')
    o.append(f'<path d="M{x+6},{y0} V{y1}" stroke="#A07850" stroke-width="4" opacity="0.6"/>')
    return "".join(o)

def hide_shape(cx, cy, w, h, seed=4):
    """Hayvan postu: dört bacak uzantısı + boyun; düzensiz kenar."""
    r = random.Random(seed); hw, hh = w / 2, h / 2
    pts = [(-0.10, -1.0), (0.0, -1.06), (0.12, -1.0), (0.55, -0.92), (0.80, -0.96), (1.02, -1.08), (1.0, -0.80), (0.94, -0.45), (0.98, 0.0), (0.94, 0.45),
           (1.0, 0.80), (1.04, 1.06), (0.80, 0.96), (0.50, 0.92), (0.0, 0.98), (-0.50, 0.92), (-0.80, 0.96), (-1.04, 1.08), (-1.0, 0.80), (-0.94, 0.45),
           (-0.98, 0.0), (-0.94, -0.45), (-1.0, -0.80), (-1.02, -1.06), (-0.80, -0.96), (-0.55, -0.92)]
    P = [(cx + hw * px + r.uniform(-10, 10), cy + hh * py + r.uniform(-8, 8)) for px, py in pts]
    d = f"M{P[0][0]:.0f},{P[0][1]:.0f}"
    for i in range(len(P)):
        a, b = P[i], P[(i + 1) % len(P)]; m = ((a[0] + b[0]) / 2 + r.uniform(-12, 12), (a[1] + b[1]) / 2 + r.uniform(-12, 12))
        d += f" Q{m[0]:.0f},{m[1]:.0f} {b[0]:.0f},{b[1]:.0f}"
    return d + " Z", P

def ink_ship(x, y, s=1.0, rot=0):
    """Boyalı gemi simgesi: hilal gövde, ejder pruva, kıvrık kıç, kırmızı çizgili kare yelken, kürek çizgileri."""
    return (f'<g transform="translate({x},{y}) rotate({rot}) scale({s})">'
            f'<path d="M-60,0 Q0,26 60,0 Q72,-8 74,-30 Q86,-40 80,-48 Q70,-44 66,-34 Q62,-12 54,-6 L-54,-6 Q-64,-14 -66,-34 Q-72,-46 -80,-40 Q-74,-24 -60,0 Z" fill="#2A1A10"/>'
            + "".join(f'<path d="M{-40 + k*14},4 l-6,14" stroke="#2A1A10" stroke-width="3"/>' for k in range(6))
            + f'<path d="M0,-6 V-74" stroke="#2A1A10" stroke-width="4"/><path d="M-30,-70 L30,-70 L34,-20 L-34,-20 Z" fill="#E6D2A8" stroke="#2A1A10" stroke-width="3.5"/>'
            + "".join(f'<path d="M{-22 + k*15},-69 L{-25 + k*17},-21" stroke="#A8261C" stroke-width="7"/>' for k in range(4))
            + f'<circle cx="77" cy="-46" r="2.5" fill="#E6D2A8"/></g>')

def red_arrow(d, w=26):
    """Fırçayla boyanmış kırmızı ok (pürüzlü kenar, iki tonlu)."""
    return (f'<path d="{d}" stroke="#5A0E08" stroke-width="{w+8}" fill="none" stroke-linecap="round" opacity="0.55"/>'
            f'<path d="{d}" stroke="#B8261A" stroke-width="{w}" fill="none" stroke-linecap="round"/>'
            f'<path d="{d}" stroke="#7A140C" stroke-width="{w*0.25:.0f}" fill="none" stroke-linecap="round" stroke-dasharray="3 9 2 14" opacity="0.5" transform="translate(0,{w*0.28:.0f})"/>')

def arrow_head(x, y, ang, s=1.0):
    return (f'<g transform="translate({x},{y}) rotate({ang}) scale({s})"><path d="M-20,-34 L46,0 L-20,34 L-6,0 Z" fill="#B8261A" stroke="#5A0E08" stroke-width="5" stroke-linejoin="round"/>'
            f'<path d="M-10,-20 L30,0" stroke="#E0503A" stroke-width="5" opacity="0.7"/></g>')

def seax(x, y, ang=35, s=1.0):
    """Posta saplanmış seax: kalın sırtlı bıçağın yarısı derinin içinde; yarıktan çıkan bıçak, pirinç bilezik, deri sargılı sap, küçük topuz."""
    return (f'<g transform="translate({x},{y}) rotate({ang}) scale({s})">'
            f'<path d="M-6,-10 L6,-18 L8,16 L-6,12 Z" fill="#1A0E06"/>'                         # yarık
            f'<path d="M0,-8 L74,-18 L74,14 L0,8 Q-4,0 0,-8 Z" fill="url(#silv)" stroke="{INK}" stroke-width="4"/>'
            f'<path d="M4,-6 L72,-15" stroke="#F2F6F8" stroke-width="3"/><path d="M6,5 L72,10" stroke="#4A5058" stroke-width="3"/>'
            f'<rect x="72" y="-20" width="16" height="38" rx="3" fill="url(#goldv)" stroke="{INK}" stroke-width="4"/>'
            f'<path d="M88,-16 Q140,-20 196,-15 L198,15 Q140,20 88,16 Z" fill="#5A3A22" stroke="{INK}" stroke-width="5"/>'
            + "".join(f'<path d="M{100 + k*16},-17 L{108 + k*16},17" stroke="#2E1C0E" stroke-width="4"/>' for k in range(6))
            + f'<rect x="194" y="-19" width="16" height="38" rx="6" fill="url(#goldv)" stroke="{INK}" stroke-width="4"/>'
            + f'<path d="M94,-9 Q140,-13 190,-10" stroke="#A07850" stroke-width="4" fill="none" opacity="0.8"/></g>')

def f2():
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0] or 0.0
    cx, cy, hw, hh = 1000, 560, 1120, 760
    hp, P = hide_shape(cx, cy, hw, hh, seed=6)
    # --- 1 arka duvar + oyma direkler + asılı eşyalar
    o = [GRAD, TDEFS, plank_wall(0, 1920, 0, 1080, seed=12)]
    o.append('<path d="M0,0 H1920 V90 H0 Z" fill="#20160E" stroke="#0E0804" stroke-width="5"/>')   # kiriş
    o.append(f'<ellipse cx="160" cy="120" rx="260" ry="200" fill="#0E0804" opacity="0.55"/>')     # meşale isi
    o.append(carved_post(1760, 120, 0, 1080, 3))
    # sağ duvarda: yuvarlak kalkan (yarısı direk arkasında) + asılı balta + boynuz
    o.append(f'<g transform="translate(1690,300)"><circle r="150" fill="#2E4A5E" stroke="{INK}" stroke-width="8" filter="url(#t_ahsap)"/>'
             + "".join(f'<path d="M0,0 L{150*math.cos(a):.0f},{150*math.sin(a):.0f}" stroke="#D8C8A0" stroke-width="22"/>' for a in [k*math.pi/2 + 0.4 for k in range(4)])
             + f'<circle r="150" fill="none" stroke="#6A6A66" stroke-width="10"/><circle r="40" fill="url(#silv)" stroke="{INK}" stroke-width="6"/></g>')
    o.append(f'<g transform="translate(1700,620) rotate(-12)"><path d="M0,0 L0,360" stroke="{INK}" stroke-width="22" stroke-linecap="round"/><path d="M0,0 L0,360" stroke="#7A5232" stroke-width="13" stroke-linecap="round"/>'
             f'<path d="M-6,20 Q-90,0 -120,-30 Q-140,40 -110,110 Q-70,70 -6,64 Z" fill="url(#silv)" stroke="{INK}" stroke-width="6"/><path d="M-112,-24 Q-130,40 -104,104" stroke="#F2F6F8" stroke-width="5" fill="none"/></g>')
    o.append(f'<path d="M1650,600 L1660,560 L1745,560 L1752,600" stroke="#1A120A" stroke-width="10" fill="none"/>')   # askı çivisi
    # sol: kürk post (duvarda asılı, meşalenin altında)
    o.append(f'<path d="M30,560 Q120,520 230,560 Q250,700 220,860 Q240,960 200,1080 L40,1080 Q10,900 30,760 Z" fill="#5A4632" stroke="{INK}" stroke-width="7" filter="url(#t_kurk)"/>'
             + "".join(f'<path d="M{random.Random(k).uniform(50,210):.0f},{random.Random(k+7).uniform(580,1060):.0f} q{random.Random(k+3).uniform(-8,8):.0f},22 0,40" stroke="#3A2A1A" stroke-width="4" fill="none"/>' for k in range(40)))
    draw(c, svg_sprite("".join(o)), 0, 0, 1.0)
    # --- 2 çerçeve sırıkları + postun duvara düşen gölgesi (ışık soldan: gölge sağa-aşağı)
    o = [GRAD, TDEFS, f'<path d="{hp}" fill="#000" opacity="0.6" transform="translate(34,22)"/>']
    draw(c, blurred(svg_sprite("".join(o)), 16), 0, 0, 1.0)
    fx0, fx1, fy0, fy1 = cx - hw / 2 - 70, cx + hw / 2 + 70, cy - hh / 2 - 70, cy + hh / 2 + 70
    o = [GRAD, TDEFS]
    poles = [(fx0 - 20, fy0, fx1 + 20, fy0 + 6), (fx0 - 10, fy1, fx1 + 26, fy1 - 4), (fx0, fy0 - 30, fx0 + 4, fy1 + 30), (fx1, fy0 - 26, fx1 - 6, fy1 + 34)]
    for (a, b, c2, d2) in poles:
        o.append(f'<path d="M{a:.0f},{b:.0f} L{c2:.0f},{d2:.0f}" stroke="{INK}" stroke-width="34" stroke-linecap="round"/><path d="M{a:.0f},{b:.0f} L{c2:.0f},{d2:.0f}" stroke="#6A4A2C" stroke-width="24" stroke-linecap="round"/>'
                 f'<path d="M{a:.0f},{b-5:.0f} L{c2:.0f},{d2-5:.0f}" stroke="#9A7448" stroke-width="5" opacity="0.7"/>')
    for (lx, ly) in ((fx0, fy0), (fx1, fy0), (fx0, fy1), (fx1, fy1)):   # köşe bağları
        o.append(f'<path d="M{lx-20:.0f},{ly-16:.0f} L{lx+20:.0f},{ly+16:.0f} M{lx-20:.0f},{ly-4:.0f} L{lx+20:.0f},{ly+26:.0f} M{lx+20:.0f},{ly-16:.0f} L{lx-20:.0f},{ly+16:.0f}" stroke="#2A1A0C" stroke-width="8"/>'
                 f'<path d="M{lx-20:.0f},{ly-16:.0f} L{lx+20:.0f},{ly+16:.0f} M{lx+20:.0f},{ly-16:.0f} L{lx-20:.0f},{ly+16:.0f}" stroke="#A88A5A" stroke-width="4"/>')
    # kenar delikleri → sırığa deri bağcık
    for i in range(0, len(P)):
        px, py = P[i]; qx = min(max(px, fx0), fx1); qy = min(max(py, fy0), fy1)
        if abs(px - cx) / (hw / 2) > abs(py - cy) / (hh / 2): qx = fx0 if px < cx else fx1; qy = py
        else: qy = fy0 if py < cy else fy1; qx = px
        hx, hy = px + (cx - px) * 0.035, py + (cy - py) * 0.05
        o.append(f'<path d="M{hx:.0f},{hy:.0f} L{qx:.0f},{qy:.0f}" stroke="{INK}" stroke-width="9"/><path d="M{hx:.0f},{hy:.0f} L{qx:.0f},{qy:.0f}" stroke="#A88458" stroke-width="5"/>')
    # --- 3 post (deri) + harita
    o.append(f'<defs><clipPath id="hc"><path d="{hp}"/></clipPath>'
             f'<linearGradient id="rake" x1="0" y1="0" x2="1" y2="0.3"><stop offset="0" stop-color="#FFE2B0" stop-opacity="0.35"/><stop offset="0.45" stop-color="#FFE2B0" stop-opacity="0"/><stop offset="0.75" stop-color="#000" stop-opacity="0.18"/><stop offset="1" stop-color="#000" stop-opacity="0.5"/></linearGradient></defs>')
    o.append(f'<path d="{hp}" fill="#C9A676" stroke="{INK}" stroke-width="9" filter="url(#t_deri)"/>')
    m = ['<g clip-path="url(#hc)">']
    r = random.Random(33)
    for k in range(14):   # lekeler, yanık izi, kırışıklar
        m.append(f'<ellipse cx="{r.uniform(cx-hw/2, cx+hw/2):.0f}" cy="{r.uniform(cy-hh/2, cy+hh/2):.0f}" rx="{r.uniform(30,120):.0f}" ry="{r.uniform(20,70):.0f}" fill="#7A5A34" opacity="{r.uniform(0.08,0.2):.2f}"/>')
    for k in range(10):
        x0_ = r.uniform(cx - hw/2, cx + hw/2); y0_ = r.uniform(cy - hh/2, cy + hh/2)
        m.append(f'<path d="M{x0_:.0f},{y0_:.0f} q{r.uniform(-60,60):.0f},{r.uniform(-20,20):.0f} {r.uniform(-140,140):.0f},{r.uniform(-30,30):.0f}" stroke="#8A6A44" stroke-width="3" fill="none" opacity="0.5"/>')
    m.append(f'<path d="{hp}" fill="none" stroke="#6A4420" stroke-width="40" opacity="0.35"/>')   # kenar koyulaşması (kurumuş deri)
    # deniz: tüm postun içi soluk mavi-gri yıkama (karalar deri renginde kalır)
    m.append(f'<rect x="300" y="100" width="1400" height="900" fill="#4E6E80" opacity="0.48"/>')
    def coast(pts, seed, fillc):
        rr = random.Random(seed); d = f"M{pts[0][0]},{pts[0][1]}"
        for i in range(1, len(pts)):
            a_, b_ = pts[i - 1], pts[i]; mx_ = (a_[0] + b_[0]) / 2 + rr.uniform(-16, 16); my_ = (a_[1] + b_[1]) / 2 + rr.uniform(-16, 16)
            d += f" Q{mx_:.0f},{my_:.0f} {b_[0]},{b_[1]}"
        d += " Z"
        return (f'<path d="{d}" fill="{fillc}" stroke="#3A2414" stroke-width="5" stroke-linejoin="round" filter="url(#t_deri)"/>'
                f'<path d="{d}" fill="none" stroke="#5E7E8C" stroke-width="18" opacity="0.25" transform="translate(4,4)"/>')
    # İskandinavya yarımadası (sol üst → aşağı), Jutland (sol alt), güney kıyı (alt), doğu kara (sağ)
    m.append(coast([(380, 120), (860, 120), (840, 230), (800, 300), (830, 380), (770, 470), (740, 560), (700, 640), (640, 690), (600, 660), (560, 600), (520, 520), (470, 470), (380, 430)], 1, "#C9A676"))
    m.append(coast([(380, 1000), (380, 760), (450, 720), (520, 740), (540, 820), (600, 870), (700, 900), (860, 880), (1000, 900), (1120, 870), (1240, 900), (1700, 900), (1700, 1000)], 2, "#C4A070"))
    m.append(coast([(1700, 120), (1180, 120), (1150, 220), (1210, 290), (1330, 300), (1420, 330), (1330, 360), (1220, 380), (1190, 470), (1230, 560), (1180, 650), (1220, 740), (1260, 820), (1300, 880), (1700, 880)], 3, "#C6A272"))
    m.append(coast([(940, 600), (990, 570), (1020, 610), (1000, 680), (960, 700), (930, 660)], 4, "#C4A070"))   # Gotland
    m.append(coast([(830, 780), (870, 765), (885, 800), (850, 815)], 5, "#C4A070"))                             # Bornholm
    for k in range(16):   # kıyı tarama (deniz tarafı)
        yy = 230 + k * 28; xx = 830 - (yy - 230) * 0.45 + 20 * math.sin(k)
        m.append(f'<path d="M{xx:.0f},{yy} l24,4" stroke="#3A2414" stroke-width="3" opacity="0.7"/>')
    for (mx, my) in ((470, 200), (560, 180), (640, 230), (520, 290), (610, 330), (700, 300), (560, 400), (660, 430), (630, 520)):
        m.append(f'<path d="M{mx-24},{my+14} L{mx},{my-20} L{mx+24},{my+14}" stroke="#3A2414" stroke-width="5" fill="none" stroke-linejoin="round"/><path d="M{mx},{my-20} L{mx+9},{my+14}" stroke="#3A2414" stroke-width="3"/>')
    m.append(f'<g transform="translate(640,640)"><path d="M-30,0 L-30,-22 Q0,-40 30,-22 L30,0 Z" fill="#7A3A1E" stroke="#2A1A10" stroke-width="4"/><path d="M-30,-22 L-40,-32 M30,-22 L40,-32" stroke="#2A1A10" stroke-width="4"/></g>'
             f'<text x="520" y="600" font-family="DejaVu Sans" font-size="28" fill="#2A1A10">ᚴᛅᛏᛁᚴᛅᛏ</text>')
    for k in range(3):   # doğu nehirleri
        y0_ = 450 + k * 160; d = f"M1240,{y0_}"
        for j in range(1, 8): d += f" Q{1240 + j*44 - 22},{y0_ + (16 if j % 2 else -16) - j*10} {1240 + j*44},{y0_ - j*12}"
        m.append(f'<path d="{d}" stroke="#4E6A7A" stroke-width="6" fill="none"/>')
    for k in range(20):
        tx, ty = r.uniform(1290, 1560), r.uniform(150, 860)
        if 300 < ty < 380 and tx < 1430: continue
        m.append(f'<path d="M{tx:.0f},{ty+14:.0f} L{tx:.0f},{ty:.0f} M{tx-11:.0f},{ty+7:.0f} L{tx:.0f},{ty-9:.0f} L{tx+11:.0f},{ty+7:.0f}" stroke="#3E4A2A" stroke-width="4" fill="none"/>')
    for (vx, vy) in ((1250, 420), (1265, 600), (1300, 790)):   # hedef köyler
        m.append(f'<g transform="translate({vx},{vy})"><path d="M-20,0 L-20,-14 L0,-30 L20,-14 L20,0 Z" fill="#7A3A1E" stroke="#2A1A10" stroke-width="4"/><path d="M28,0 L28,-10 L42,-22 L56,-10 L56,0 Z" fill="#7A3A1E" stroke="#2A1A10" stroke-width="4"/></g>')
    # rün bordürü (deniz üstünde, üst/alt kenar boyunca)
    for (yy, seed_) in ((180, 1), (960, 2)):
        rr = random.Random(seed_); txt = "".join(rr.choice(RUNES) for _ in range(40))
        m.append(f'<text x="880" y="{yy}" font-family="DejaVu Sans" font-size="24" fill="#3A2414" opacity="0.75" letter-spacing="3">{txt[:22]}</text>')
    # KIRMIZI AKIN OKLARI: Kattegat → doğu köyleri
    for (d, hx, hy, ang) in (("M680,610 Q880,380 1200,415", 1204, 414, 4), ("M690,650 Q950,560 1215,592", 1218, 592, 8), ("M680,690 Q900,860 1250,780", 1254, 778, -14)):
        m.append(red_arrow(d, 22) + arrow_head(hx, hy, ang, 0.95))
    for (x, y, rot) in ((905, 470, -14), (975, 560, 4), (1010, 820, -6)):
        m.append(ink_ship(x, y, 0.85, rot))
    # ışık: soldan sürten (sıcak), sağ taraf gölgede
    m.append(f'<rect x="300" y="120" width="1400" height="880" fill="url(#rake)"/>')
    m.append('</g>')
    o.append("".join(m))
    o.append(f'<path d="{hp}" fill="none" stroke="#F2D8A8" stroke-width="3" opacity="0.5" transform="translate(-3,-3)"/>')
    for i in range(len(P)):   # kenar dikiş delikleri + yırtık
        px, py = P[i]; hx, hy = px + (cx - px) * 0.035, py + (cy - py) * 0.05
        o.append(f'<circle cx="{hx:.0f}" cy="{hy:.0f}" r="7" fill="#2A1A0C" stroke="#8A6A44" stroke-width="2"/>')
    o.append(seax(cx - hw / 2 + 170, cy - hh / 2 + 120, 210, 1.1))
    draw(c, svg_sprite("".join(o)), 0, 0, 1.0)
    # bıçak gölgesi (sağa-aşağı)
    draw(c, blurred(svg_sprite(f'<g opacity="0.55">{seax(cx - hw / 2 + 200, cy - hh / 2 + 150, 214, 1.1).replace("url(#silv)", "#000").replace("url(#goldv)", "#000").replace("#D8CCB0", "#000").replace("#FFFFFF", "#000")}</g>'), 5), 0, 0, 1.0)
    # --- 4 ön plan: meşale (anahtar ışık) + bulanık direk + duman
    draw(c, blurred(svg_sprite('<path d="M0,0 L70,0 L90,1080 L0,1080 Z" fill="#1A120A"/><path d="M0,820 Q160,800 260,860 L300,1080 L0,1080 Z" fill="#3A2A1A"/>'), 14), 0, 0, 1.0)
    fg = (GRAD + TDEFS + f'<g transform="translate(150,330)"><path d="M-60,40 L20,10 M-60,70 L20,40" stroke="#1A1410" stroke-width="12"/>'
          f'<path d="M0,120 L30,-40" stroke="{INK}" stroke-width="40" stroke-linecap="round"/><path d="M0,120 L30,-40" stroke="#5A3A20" stroke-width="28" stroke-linecap="round"/>'
          f'<path d="M6,118 L34,-36" stroke="#8A6040" stroke-width="6" opacity="0.7"/>'
          f'<path d="M14,-20 L50,-12 L60,-58 L26,-66 Z" fill="#3A2614" stroke="{INK}" stroke-width="5"/><path d="M18,-34 L54,-26 M22,-50 L58,-42" stroke="#1A0E06" stroke-width="4"/>'
          f'<path d="M-4,40 L44,52" stroke="#1A1410" stroke-width="14" stroke-linecap="round"/><path d="M-4,40 L44,52" stroke="#4A4A4A" stroke-width="6" stroke-linecap="round"/></g>')
    draw(c, svg_sprite(fg), 0, 0, 1.0)
    flame = ('<g transform="translate(186,270)"><path d="M0,40 Q-50,0 -30,-60 Q-20,-100 0,-150 Q10,-100 30,-80 Q60,-30 40,20 Q24,46 0,40 Z" fill="#E86A1E"/>'
             '<path d="M0,34 Q-30,0 -16,-40 Q-6,-70 4,-100 Q14,-60 26,-40 Q40,0 22,26 Z" fill="#FFB43A"/><path d="M4,26 Q-12,0 -2,-24 Q6,-44 10,-56 Q20,-20 18,10 Z" fill="#FFF0B0"/></g>')
    draw(c, svg_sprite(flame), 0, 0, 1.0)
    sm = "".join(smoke_svg(190 + k * 10, 130, 300, seed=k + 60, a=0.25, w=70).replace('stroke="#D8D4CC"', 'stroke="#4A3E36"').replace('stroke-width="', 'stroke-width="3') for k in range(4))
    draw(c, blurred(svg_sprite(sm), 12), 0, 0, 1.0)
    glow(c, 190, 220, 520, "#FF9A40", 0.45); bloom_spot(c, 190, 220, 160, "#FFE0A0", 0.6)
    Particles("ember", 26, seed=4, area=(120, 80, 360, 260), color="#FFB050", size=(2, 4), speed=30).draw(c, 1.3, 1.0)
    # sağ üst + alt köşeler karanlık (değer yapısı: ışık soldan sağa söner)
    sh = skia.GradientShader.MakeLinear([(200, 0), (1920, 300)], [col("#000000", 0).toColor(), col("#000000", 0.05).toColor(), col("#05030A", 0.5).toColor()], [0, 0.45, 1])
    c.drawRect(skia.Rect(0, 0, W, H), skia.Paint(Shader=sh))
    card_at(c, "DOĞU", 1690, 150, "Rus toprakları")
    finish(c, cold=False, warm=0.05); return s


# ================================================================== f5 · gezginin eli: güneş tahtası + güneş taşı
SKO = "#D6AE88"; SKO2 = "#A87A58"; SKO3 = "#7A5236"

def old_hand():
    """Gezginin yaşlı sağ eli, avuç yukarı ve kameraya dönük, parmaklar sola (sunma jesti). Yerel: bilek (0,0).
    Avuç çizgileri, parmak boğum kırışıkları, parmak yastıkları, bilekte damar, yaşlılık lekesi, bronz yüzük, deri bileklik."""
    o = []
    # parmaklar (hafif aralık, uçlar kameraya kıvrık): (taban y, uzunluk, kalınlık, eğim)
    F = ((-46, 110, 30, -12), (-15, 126, 31, -3), (16, 116, 29, 5), (44, 88, 25, 13))
    for k, (fy, ln, wd, tilt) in enumerate(F):
        x0 = -150; xm = x0 - ln * 0.58; ym = fy + tilt * 0.6; x1 = x0 - ln; y1 = fy + tilt - 6
        d1 = f"M{x0},{fy} Q{(x0+xm)/2:.0f},{fy + tilt*0.25 + 3:.0f} {xm:.0f},{ym:.0f}"
        d2 = f"M{xm:.0f},{ym:.0f} Q{(xm+x1)/2 - 4:.0f},{ym + 4:.0f} {x1:.0f},{y1:.0f}"
        for d_, w_ in ((d1, wd), (d2, wd * 0.8)): o.append(f'<path d="{d_}" stroke="{INK}" stroke-width="{w_+12:.0f}" fill="none" stroke-linecap="round"/>')
        for d_, w_ in ((d1, wd), (d2, wd * 0.8)): o.append(f'<path d="{d_}" stroke="{SKO}" stroke-width="{w_:.0f}" fill="none" stroke-linecap="round"/>')
        o.append(f'<path d="M{x0},{fy + wd*0.32:.0f} Q{xm:.0f},{ym + wd*0.3:.0f} {x1+8:.0f},{y1 + wd*0.24:.0f}" stroke="{SKO2}" stroke-width="{wd*0.28:.0f}" fill="none" stroke-linecap="round" opacity="0.85"/>')   # alt gölge
        o.append(f'<path d="M{x0-6},{fy - wd*0.26:.0f} Q{xm:.0f},{ym - wd*0.3:.0f} {x1+14:.0f},{y1 - wd*0.22:.0f}" stroke="#F2D4B4" stroke-width="4" fill="none" stroke-linecap="round" opacity="0.8"/>')   # üst ışık
        for (bx, by, ww) in ((x0 - ln * 0.30, fy + tilt * 0.3, wd), (xm - 2, ym, wd * 0.9), (x0 - ln * 0.82, fy + tilt * 0.85 - 4, wd * 0.8)):   # boğum kırışıkları
            o.append(f'<path d="M{bx+3:.0f},{by - ww*0.4:.0f} q-5,{ww*0.4:.0f} 0,{ww*0.8:.0f}" stroke="{SKO3}" stroke-width="3" fill="none"/>'
                     f'<path d="M{bx-4:.0f},{by - ww*0.26:.0f} q-4,{ww*0.26:.0f} 0,{ww*0.52:.0f}" stroke="{SKO3}" stroke-width="2" fill="none" opacity="0.6"/>')
        o.append(f'<ellipse cx="{x1+5:.0f}" cy="{y1-1:.0f}" rx="{wd*0.34:.0f}" ry="{wd*0.27:.0f}" fill="#EACAA8"/>')   # parmak ucu yastığı
        o.append(f'<path d="M{x1-wd*0.3:.0f},{y1 - wd*0.3:.0f} q-6,{wd*0.3:.0f} 0,{wd*0.6:.0f}" stroke="#6A5038" stroke-width="5" fill="none" stroke-linecap="round"/>')   # kirli tırnak kenarı
    # bronz yüzük (yüzük parmağı)
    o.append(f'<path d="M-196,{16-17} q-6,17 0,34" stroke="{INK}" stroke-width="13" fill="none"/><path d="M-196,{16-17} q-6,17 0,34" stroke="#C8923A" stroke-width="7" fill="none"/><path d="M-198,6 q-3,8 0,14" stroke="#F2C878" stroke-width="3" fill="none"/>')
    # avuç
    palm = "M14,-58 Q-60,-70 -150,-64 Q-176,-40 -172,0 Q-176,40 -156,62 Q-80,74 14,58 Q30,0 14,-58 Z"
    o.append(f'<defs><radialGradient id="palmg" cx="0.42" cy="0.45" r="0.62"><stop offset="0" stop-color="#E6C29C"/><stop offset="0.7" stop-color="{SKO}"/><stop offset="1" stop-color="#B08260"/></radialGradient></defs>'
             f'<path d="{palm}" fill="url(#palmg)" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>')
    o.append(f'<path d="M-150,-30 Q-110,-14 -60,-36 M-160,8 Q-110,-2 -40,10 M-70,-58 Q-110,-10 -60,52" stroke="{SKO3}" stroke-width="3.5" fill="none" opacity="0.85"/>')   # kalp, akıl, hayat çizgileri
    o.append(f'<path d="M-150,-46 q20,6 40,-2 M-140,44 q30,10 70,4 M-20,30 q-14,10 -30,12" stroke="{SKO3}" stroke-width="2.5" fill="none" opacity="0.6"/>')
    o.append(f'<path d="M-40,-44 Q-10,-10 -24,40" stroke="#B88A64" stroke-width="18" fill="none" opacity="0.45" stroke-linecap="round"/>')   # tenar tümseği gölgesi
    o.append(f'<path d="M-160,-40 Q-168,0 -150,40" stroke="#F0D0B0" stroke-width="6" fill="none" opacity="0.6" stroke-linecap="round"/>')   # ışık kenarı (sol)
    # başparmak (üstte, sola-yukarı)
    th = "M-10,-50 Q-50,-96 -110,-112 Q-140,-118 -146,-100 Q-146,-84 -124,-78 Q-80,-68 -60,-50 Z"
    o.append(f'<path d="{th}" fill="{SKO}" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/><path d="M-20,-58 Q-70,-96 -120,-108" stroke="#F2D4B4" stroke-width="5" fill="none" opacity="0.7"/>'
             f'<path d="M-90,-102 q-4,10 2,20 M-80,-98 q-3,8 1,16" stroke="{SKO3}" stroke-width="3" fill="none"/><ellipse cx="-132" cy="-98" rx="11" ry="9" fill="#E8C4A0"/>'
             f'<path d="M-30,-56 Q-60,-70 -90,-86" stroke="#B88A64" stroke-width="6" fill="none" opacity="0.6"/>')
    # bilek: damarlar + yaşlılık lekeleri + deri bileklik
    o.append(f'<path d="M6,-40 Q-20,-20 -40,-30 M4,-4 q-20,-6 -36,6 M8,30 Q-14,28 -30,40" stroke="#7A8AA8" stroke-width="4.5" fill="none" opacity="0.55"/>')
    for (sx, sy, sr) in ((-110, 34, 5), (-128, 50, 3.5), (-60, 46, 4), (-20, -30, 3)): o.append(f'<circle cx="{sx}" cy="{sy}" r="{sr}" fill="#9A6A48" opacity="0.55"/>')
    o.append(f'<path d="M14,-62 Q32,0 14,62" stroke="{INK}" stroke-width="34" fill="none"/><path d="M14,-62 Q32,0 14,62" stroke="#4A2E1A" stroke-width="24" fill="none"/>'
             f'<path d="M16,-56 Q32,0 16,56" stroke="#8A6240" stroke-width="4" fill="none" stroke-dasharray="7 6"/>')
    return "".join(o)

def sleeve():
    """Kaba yün yen: kıvrımlar, yama, püsküllü manşet. Yerel: bilek (0,0), sağ kenara uzanır."""
    r = random.Random(5)
    sl = "M22,-78 Q200,-120 520,-160 L520,180 Q220,120 24,74 Q6,0 22,-78 Z"
    o = [f'<g filter="url(#t_form)"><path d="{sl}" fill="#3E3428" filter="url(#t_yun)"/></g><path d="{sl}" fill="none" stroke="{INK}" stroke-width="8"/>']
    for k in range(9): o.append(f'<path d="M{40 + k*50},{-70 - k*8} Q{60 + k*52},{0} {40 + k*50},{70 + k*10}" stroke="#211A12" stroke-width="{r.uniform(4,8):.0f}" fill="none" opacity="0.7"/>')
    for k in range(18):   # püskül
        y = -72 + k * 8.4; o.append(f'<path d="M{24 - abs(math.sin(k))*4:.0f},{y:.0f} l{-r.uniform(10,24):.0f},{r.uniform(-4,6):.0f}" stroke="#2A2218" stroke-width="4" stroke-linecap="round"/>')
    o.append(f'<path d="M10,-64 Q200,-104 520,-144" stroke="#7A6A50" stroke-width="5" fill="none" opacity="0.6"/>')   # üst ışık kenarı
    return "".join(o)

def sunstone2(s=1.0):
    """İzlanda spatı (kalsit) eşkenar dörtyüzlü: yarı saydam, fasetli, içinde çift kırılma çizgisi."""
    return (f'<g transform="scale({s})"><ellipse cx="-4" cy="42" rx="62" ry="14" fill="#5A3020" opacity="0.45"/>'
            f'<path d="M-56,14 L-6,-50 L66,-30 L18,36 Z" fill="#F6F0DC" fill-opacity="0.6" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
            f'<path d="M-6,-50 L66,-30 L78,-12 L6,-32 Z" fill="#FFFFFF" fill-opacity="0.8" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
            f'<path d="M66,-30 L78,-12 L30,54 L18,36 Z" fill="#B8A884" fill-opacity="0.75" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
            f'<path d="M-56,14 L18,36 L30,54 L-44,32 Z" fill="#C8BC98" fill-opacity="0.8" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
            f'<path d="M-30,0 L30,10 M-26,8 L34,18" stroke="#8A6A3A" stroke-width="3" opacity="0.6"/>'      # çift görüntü
            f'<path d="M-36,-20 L-16,-44" stroke="#FFFFFF" stroke-width="6" stroke-linecap="round"/><path d="M-4,-40 L44,-32" stroke="#FFFFFF" stroke-width="3" opacity="0.9"/>'
            f'<path d="M10,-20 L22,-6 L8,6 Z" fill="#FFF6D8" opacity="0.6"/></g>')

def bowl_board(cx, cy):
    """Su dolu oyma tahta çanak; içinde yüzen güneş tahtası (sólskuggafjöl): halkalar, kenar çentikleri, ortada mil."""
    o = [f'<ellipse cx="{cx+40}" cy="{cy+70}" rx="320" ry="60" fill="url(#soft)"/>']
    o.append(f'<path d="M{cx-290},{cy} Q{cx-280},{cy+110} {cx},{cy+120} Q{cx+280},{cy+110} {cx+290},{cy} Z" fill="#6A4628" stroke="{INK}" stroke-width="8" filter="url(#t_ahsap)"/>')
    o.append(f'<path d="M{cx-250},{cy+40} Q{cx},{cy+96} {cx+250},{cy+40}" stroke="#4A2E18" stroke-width="16" fill="none" opacity="0.6"/>' + braid(cx - 220, cy + 30, 440, 30, "#8A6240", "#3A2412", 12, 8).replace('<path', '<path opacity="0.55"'))
    o.append(f'<path d="M{cx+120},{cy+20} Q{cx+250},{cy+40} {cx+280},{cy+10} L{cx+290},{cy} Q{cx+280},{cy+110} {cx},{cy+120} Q{cx+200},{cy+90} {cx+120},{cy+20} Z" fill="#000" opacity="0.3"/>')
    o.append(f'<ellipse cx="{cx}" cy="{cy}" rx="290" ry="84" fill="#7A5432" stroke="{INK}" stroke-width="8"/>')   # ağız
    o.append(f'<ellipse cx="{cx}" cy="{cy+6}" rx="262" ry="70" fill="#2E4450" stroke="#3A2414" stroke-width="5"/>')   # su
    o.append(f'<ellipse cx="{cx-120}" cy="{cy-14}" rx="70" ry="10" fill="#FFD9A0" opacity="0.55"/>')   # mum yansıması
    for k in range(3): o.append(f'<ellipse cx="{cx}" cy="{cy+8}" rx="{214 + k*18}" ry="{58 + k*4}" fill="none" stroke="#6A8A9A" stroke-width="2.5" opacity="{0.5 - k*0.12:.2f}"/>')
    # yüzen disk
    dx, dy = cx + 10, cy + 2
    o.append(f'<ellipse cx="{dx}" cy="{dy+12}" rx="182" ry="50" fill="#5A3A1E" stroke="{INK}" stroke-width="6"/>'
             f'<ellipse cx="{dx}" cy="{dy}" rx="182" ry="50" fill="#B07E48" stroke="{INK}" stroke-width="6" filter="url(#t_ahsap)"/>')
    for rr in (150, 110, 70, 34): o.append(f'<ellipse cx="{dx}" cy="{dy}" rx="{rr}" ry="{rr*0.275:.1f}" fill="none" stroke="#5A3A1E" stroke-width="3"/>')
    for k in range(32):
        a = k * math.pi / 16; L = 14 if k % 4 == 0 else 7
        o.append(f'<path d="M{dx + 168*math.cos(a):.1f},{dy + 46*math.sin(a):.1f} L{dx + (168-L)*math.cos(a):.1f},{dy + (46-L*0.27)*math.sin(a):.1f}" stroke="#4A2E16" stroke-width="3"/>')
    o.append(f'<path d="M{dx-20},{dy-6} Q{dx+30},{dy-26} {dx+80},{dy-30}" stroke="#4A2E16" stroke-width="2.5" fill="none" stroke-dasharray="5 5"/>')   # gnomon eğrisi
    o.append(f'<path d="M{dx},{dy} L{dx+150},{dy+18}" stroke="#2A1608" stroke-width="9" opacity="0.55" stroke-linecap="round"/>')   # milin gölgesi (ışık soldan)
    o.append(f'<path d="M{dx-5},{dy+2} L{dx-5},{dy-104} L{dx+5},{dy-108} L{dx+5},{dy+2} Z" fill="#8A5A30" stroke="{INK}" stroke-width="4"/><circle cx="{dx}" cy="{dy-108}" r="8" fill="#D8B04A" stroke="{INK}" stroke-width="3"/>')
    o.append(f'<path d="M{dx-150},{dy-10} Q{dx-60},{dy-40} {dx+60},{dy-38}" stroke="#E8C08A" stroke-width="4" fill="none" opacity="0.6"/>')
    return "".join(o)

def coins_pouch(x, y):
    r = random.Random(9)
    o = [f'<ellipse cx="{x+30}" cy="{y+40}" rx="130" ry="26" fill="url(#soft)"/>',
         f'<path d="M{x-90},{y+30} Q{x-120},{y-20} {x-40},{y-52} L{x-30},{y-64} Q{x-10},{y-60} {x+6},{y-64} L{x+14},{y-52} Q{x+80},{y-20} {x+50},{y+32} Q{x-20},{y+46} {x-90},{y+30} Z" fill="#6A4428" stroke="{INK}" stroke-width="6" filter="url(#t_deri)"/>',
         f'<path d="M{x-44},{y-62} L{x-56},{y-96} L{x-36},{y-80} L{x-24},{y-104} L{x-12},{y-80} L{x+4},{y-102} L{x+8},{y-78} L{x+26},{y-94} L{x+10},{y-62} Z" fill="#7A5232" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>',
         f'<path d="M{x-46},{y-60} Q{x-14},{y-48} {x+16},{y-60}" stroke="#2A1A0C" stroke-width="8" fill="none"/><path d="M{x+12},{y-58} q34,10 46,40 M{x+12},{y-58} q20,18 18,46" stroke="#3A2414" stroke-width="5" fill="none"/>'
         f'<path d="M{x-70},{y} Q{x-80},{y-30} {x-44},{y-46}" stroke="#9A7050" stroke-width="5" fill="none" opacity="0.7"/>']
    for k in range(9):
        cx_, cy_ = x + 60 + r.uniform(0, 130), y + 10 + r.uniform(-10, 34)
        o.append(f'<ellipse cx="{cx_:.0f}" cy="{cy_:.0f}" rx="22" ry="8" fill="url(#silv)" stroke="{INK}" stroke-width="3"/><ellipse cx="{cx_:.0f}" cy="{cy_:.0f}" rx="13" ry="4" fill="none" stroke="#5E666E" stroke-width="2" stroke-dasharray="2 3"/>')
    o.append(f'<path d="M{x+190},{y+24} l30,-6 l6,10 l-30,8 Z" fill="url(#silv)" stroke="{INK}" stroke-width="3"/>')   # kesik gümüş
    return "".join(o)

def carved_cup(x, y):
    return (f'<g transform="translate({x},{y})"><ellipse cx="14" cy="4" rx="80" ry="14" fill="url(#soft)"/>'
            f'<path d="M-60,-130 L-50,0 Q0,10 50,0 L60,-130 Z" fill="#7A5232" stroke="{INK}" stroke-width="6" filter="url(#t_ahsap)"/>'
            f'<ellipse cx="0" cy="-130" rx="60" ry="14" fill="#3A2414" stroke="{INK}" stroke-width="5"/>'
            + braid(-56, -110, 112, 30, "#A07850", "#3A2412", 4, 7) +
            f'<path d="M20,-120 L22,-8 L50,-4 L58,-124 Z" fill="#000" opacity="0.3"/><path d="M-50,-122 L-42,-6" stroke="#C89A68" stroke-width="5" opacity="0.7"/></g>')

def table_knife(x, y, ang=-18):
    return (f'<g transform="translate({x},{y}) rotate({ang})"><path d="M-110,14 L130,14" stroke="#000" stroke-width="16" opacity="0.3"/>'
            f'<path d="M-120,0 L0,-8 L0,8 L-110,10 Z" fill="url(#silv)" stroke="{INK}" stroke-width="4"/><rect x="0" y="-11" width="14" height="22" fill="url(#goldv)" stroke="{INK}" stroke-width="3"/>'
            f'<path d="M14,-10 L130,-12 Q140,0 130,12 L14,10 Z" fill="#D8CCB0" stroke="{INK}" stroke-width="4"/></g>')

def f5():
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0] or 0.0
    # --- 1 uzak: uzun ev (bulanık), ocak parıltısı
    draw(c, blurred(place(IPL.longhouse(1.0)), 10), 0, -60, 1.0); fill(c, "#0A0806", 0.3)
    glow(c, 1300, 420, 500, "#FF7A30", 0.12)
    # --- 2 masa yüzeyi (perspektifte tahtalar) + arka eşyalar
    o = [GRAD, TDEFS]
    o.append(f'<path d="M-40,620 L1960,620 L1960,1080 L-40,1080 Z" fill="#5A3C24" stroke="{INK}" stroke-width="6" filter="url(#t_ahsap)"/>')
    vx, vy = 960, -900
    for k in range(-8, 9):
        xb = 960 + k * 260; xt = vx + (xb - vx) * (620 - vy) / (1080 - vy)
        o.append(f'<path d="M{xt:.0f},620 L{xb:.0f},1080" stroke="#24160C" stroke-width="5"/><path d="M{xt+6:.0f},620 L{xb+8:.0f},1080" stroke="#8A6440" stroke-width="2" opacity="0.5"/>')
    o.append('<path d="M-40,612 L1960,612 L1960,632 L-40,632 Z" fill="#3A2614" stroke="#160E06" stroke-width="4"/>')
    for k in range(8):   # çizik, leke
        r = random.Random(k + 70); x_, y_ = r.uniform(100, 1800), r.uniform(700, 1050)
        o.append(f'<path d="M{x_:.0f},{y_:.0f} l{r.uniform(30,90):.0f},{r.uniform(-8,8):.0f}" stroke="#2A1A0C" stroke-width="2.5" opacity="0.6"/><ellipse cx="{x_+40:.0f}" cy="{y_+30:.0f}" rx="{r.uniform(20,50):.0f}" ry="{r.uniform(6,12):.0f}" fill="#2A1A0C" opacity="0.18"/>')
    # sol arka: kürk örtü + oyma kupa + mum öbeği (anahtar ışık)
    o.append(f'<path d="M-40,560 Q160,540 330,600 Q360,640 320,700 Q200,720 80,700 Q0,690 -40,700 Z" fill="#6A5640" stroke="{INK}" stroke-width="6" filter="url(#t_kurk)"/>'
             + "".join(f'<path d="M{random.Random(k).uniform(-20,320):.0f},{random.Random(k+5).uniform(570,690):.0f} q6,14 0,26" stroke="#3E3022" stroke-width="4" fill="none"/>' for k in range(30)))
    o.append(carved_cup(250, 712))
    o.append(f'<ellipse cx="470" cy="706" rx="110" ry="22" fill="#2A2420" stroke="{INK}" stroke-width="5"/><ellipse cx="470" cy="700" rx="96" ry="16" fill="#4A4440"/>')   # demir tabak
    o.append(drip_candle(430, 704, 170, 34, True, 11) + drip_candle(500, 708, 110, 30, True, 12) + drip_candle(462, 712, 60, 28, False, 13))
    o.append(bowl_board(860, 790))
    o.append(coins_pouch(330, 930))
    o.append(table_knife(1420, 960, -14))
    draw(c, svg_sprite("".join(o)), 0, 0, 1.0)
    # mum ışığı: anahtar (sol), masaya sıcak havuz
    for x, y in ((430, 470), (500, 532)): glow(c, x, y, 120, "#FFB050", 0.55); bloom_spot(c, x, y, 70, "#FFF2C8", 0.7)
    bloom_spot(c, 600, 780, 600, "#FFB060", 0.20)
    # --- 3 gezginin eli + yen + taş; masaya düşen gölge
    hx, hy, hs = 1450, 600, 1.6
    draw(c, blurred(svg_sprite(f'<ellipse cx="{hx-160}" cy="{hy+230}" rx="300" ry="36" fill="#000" opacity="0.5"/>'), 18), 0, 0, 1.0)
    hand = (GRAD + TDEFS + tex.scaled("cilt", 1.0)[0] + f'<g transform="translate({hx},{hy}) scale({hs},{hs*0.78:.3f})">{sleeve()}{old_hand()}'
            f'<g transform="translate(-92,-28) rotate(-6) scale(1,1.2)">{sunstone2(0.85)}</g></g>')
    sp = svg_sprite(hand)
    rim(c, sp, 0, 0, 1.0, "#FFC080", dx=-4, dy=-3, a=0.7)
    draw(c, sp, 0, 0, 1.0)
    c.saveLayer(None, None); draw(c, tinted(sp, "#140A06"), 0, 0, 1.0)   # gölge yanı: ışık soldan (mum), sağa doğru koyulaşır
    g = skia.GradientShader.MakeLinear([(1150, 0), (1750, 0)], [col("#000000", 0).toColor(), col("#000000", 0.55).toColor()])
    pp = skia.Paint(Shader=g); pp.setBlendMode(skia.BlendMode.kDstIn); c.drawRect(skia.Rect(0, 0, W, H), pp); c.restore()
    # taştan kırılan ışık: masadaki güneş tahtasına ince huzme + kenarda tayf
    stx, sty = hx - 92 * hs, hy - 40 * hs * 0.78
    bloom_spot(c, stx - 10, sty - 10, 80, "#FFF0D0", 0.35); glow(c, stx - 10, sty - 14, 34, "#FFFFFF", 0.35)
    beam(c, stx - 30, sty + 10, 10, 900, 760, 44, "#FFF4D0", 0.38, 3)
    for k, cc in enumerate(("#FF6A5A", "#FFD24A", "#6AE0A0", "#6A9AFF")):
        beam(c, stx - 26 + k * 3, sty + 16, 4, 936 + k * 10, 772 + k * 3, 10, cc, 0.32, 2)
    bloom_spot(c, 905, 762, 70, "#FFF6D8", 0.6)
    rays(c, stx - 10, sty - 14, 200, 90, 360, 8, "#FFFFFF", 0.07, t)
    Particles("dust", 70, seed=21, area=(600, 300, 1400, 760), color="#FFE8C0", size=(1.5, 3.5), speed=8).draw(c, t, 0.8)
    # --- 4 ön plan: bulanık kürk (sol alt) + boynuz kupası (sağ alt)
    fg = (GRAD + TDEFS + '<path d="M-40,1080 L-40,900 Q120,860 300,940 Q380,1000 360,1080 Z" fill="#4A3A2A"/>'
          + '<g transform="translate(1720,1060)"><path d="M-70,0 Q-90,-150 0,-260 Q60,-320 120,-300 Q130,-280 110,-270 Q40,-250 20,-160 Q10,-80 50,0 Z" fill="#7A6A4A" stroke="#1A1410" stroke-width="9"/>'
          + '<path d="M-74,-30 Q-10,-50 54,-30" stroke="#B8823A" stroke-width="20"/><path d="M-80,-90 Q-20,-110 34,-96" stroke="#B8823A" stroke-width="10"/><path d="M110,-298 l18,-4 l-6,26 Z" fill="#B8823A"/></g>')
    draw(c, blurred(svg_sprite(fg), 9), 0, 0, 1.0)
    sh = skia.GradientShader.MakeRadial((760, 640), 1250, [col("#000000", 0).toColor(), col("#000000", 0).toColor(), col("#05030A", 0.6).toColor()], [0, 0.45, 1])
    c.drawRect(skia.Rect(0, 0, W, H), skia.Paint(Shader=sh))
    card_at(c, "GEZGİN", 1500, 200, "güneş tahtası + güneş taşı", 0.9)
    finish(c, cold=False, warm=0.06); return s

FR = {"f2": f2, "f5": f5, "f8": f8}

CROPS = {"f8": [(950, 400), (700, 560)], "f2": [(1000, 560), (560, 360)], "f5": [(1250, 560), (860, 760)]}   # id → [(cx, cy), (cx, cy)]  (1920 kare üzerinde %200: 960×540 kutu)

def crop(img_path, cx, cy, out):
    from PIL import Image
    im = Image.open(img_path); x0 = max(0, min(W - 960, cx - 480)); y0 = max(0, min(H - 540, cy - 270))
    im.crop((x0, y0, x0 + 960, y0 + 540)).resize((1920, 1080), Image.LANCZOS).save(out)

if __name__ == "__main__":
    ids = sys.argv[1:] or list(FR)
    for i in ids:
        T[0] = None; p = f"{OUTV}/{i}.png"; FR[i]().makeImageSnapshot().save(p, skia.kPNG); print("kare", i)
        for k, (cx, cy) in enumerate(CROPS.get(i, []), 1): crop(p, cx, cy, f"{OUTV}/{i}_crop{k}.png")
