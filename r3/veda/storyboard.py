import sys; sys.path[:0] = ['/home/claude/r3', '/home/claude/r2']
from art3 import *
import art2, subprocess, random
INK_ = "#1A1410"
LAG = dict(RAGNAR3, female=True, hair="#D2AC5C", skin="#F2CDAA", iris="#5E8CA8", tunic="#3B5A66", trim="#C9D2D6", cloak="#6A5236",
           fur_collar="#C8BCA6", scratch=True, brow_k=0.5, armring=False, brow_c="#8A6A3A",
           clasp='<g transform="translate(0,-440)"><circle r="16" fill="#C9D2D6" stroke="#1A1410" stroke-width="4"/><path d="M-8,0 L8,0 M0,-8 L0,8" stroke="#1A1410" stroke-width="3"/></g>')
ASL = dict(LAG, hair="#E6D6A8", skin="#F3D2B0", iris="#6A7A9A", tunic="#5B3A6E", trim="#E2B23A", cloak="#2E2A44", scratch=False, brow_c="#A88E5A", crown=False,
           clasp='<g transform="translate(0,-440)"><circle r="14" fill="#E2B23A" stroke="#1A1410" stroke-width="4"/></g>')
BJ = dict(RAGNAR3, beardless=True, hair="#8A6A42", skin="#F2CDAA", iris="#4C7EA6", tunic="#4A5A6A", trim="#C9A25A", cloak="#5A4632", armring=True, clasp="")
RG = RAGNAR_UC
def belly(x, y, s):  # hamilelik karnı (önden)
    return f'<g transform="translate({x},{y}) scale({s})"><path d="M-60,-300 Q-96,-220 -60,-150 L60,-150 Q96,-220 60,-300 Z" fill="{ASL["tunic"]}" stroke="{INK_}" stroke-width="5"/><path d="M-30,-280 Q-50,-220 -30,-170" stroke="{shade(ASL["tunic"],1.3)}" stroke-width="6" fill="none" opacity="0.6"/></g>'
def cold(op=0.35):
    return f'<rect width="960" height="540" fill="#24384E" opacity="{op}" style="mix-blend-mode:multiply"/>'
def bands():
    return '<rect width="960" height="48" fill="#000"/><rect y="492" width="960" height="48" fill="#000"/>'
def blur_def(i, sd):
    return f'<defs><filter id="b{i}" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="{sd}"/></filter></defs>'
def sky(c1="#6E8296", c2="#B8C4CE"):
    return f'<defs><linearGradient id="sk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient></defs><rect width="960" height="540" fill="url(#sk)"/>'
def longhouse(x, y, w, h):
    o = f'<path d="M{x-20},{y} L{x+w/2},{y-h*0.7} L{x+w+20},{y} Z" fill="#5A4636" stroke="{INK_}" stroke-width="4"/>'
    o += "".join(f'<path d="M{x+k*18},{y-4} L{x+w/2},{y-h*0.66}" stroke="#4A3828" stroke-width="3"/>' for k in range(int(w / 18)))
    o += f'<rect x="{x}" y="{y}" width="{w}" height="{h*0.55}" fill="#6E5A44" stroke="{INK_}" stroke-width="4"/>'
    o += "".join(f'<path d="M{x+k*22},{y} L{x+k*22},{y+h*0.55}" stroke="#5A4836" stroke-width="3"/>' for k in range(1, int(w / 22)))
    return o
def cart(x, y, s, flip=1):
    return (f'<g transform="translate({x},{y}) scale({s*flip},{s})">'
            f'<rect x="-120" y="-90" width="240" height="70" fill="#7A5A3A" stroke="{INK_}" stroke-width="5"/><path d="M-120,-60 L120,-60" stroke="#5A4028" stroke-width="4"/>'
            f'<rect x="-100" y="-150" width="90" height="60" fill="#8A6A4A" stroke="{INK_}" stroke-width="4"/><rect x="0" y="-130" width="70" height="40" fill="#6A4A30" stroke="{INK_}" stroke-width="4"/>'
            + "".join(f'<g transform="translate({wx},-10)"><circle r="42" fill="#5A4028" stroke="{INK_}" stroke-width="5"/><circle r="8" fill="#3A2A1A"/>' + "".join(f'<path d="M0,0 L{42*math.cos(a):.0f},{42*math.sin(a):.0f}" stroke="{INK_}" stroke-width="3"/>' for a in [k*math.pi/4 for k in range(8)]) + '</g>' for wx in (-70, 70))
            + f'<path d="M120,-60 L230,-40" stroke="#5A4028" stroke-width="6"/>'
            f'<g transform="translate(300,-20)"><path d="M-80,-60 Q-90,-110 -30,-110 L40,-110 Q70,-150 90,-170 L120,-150 Q110,-120 80,-90 L70,-50 Q60,-30 40,-40 L-60,-40 Z" fill="#6A4A34" stroke="{INK_}" stroke-width="5"/>'
            f'<path d="M-60,-45 L-70,20 M-30,-45 L-24,20 M30,-45 L36,20 M55,-50 L64,20" stroke="#5A3A24" stroke-width="12" stroke-linecap="round"/><path d="M95,-165 L80,-120" stroke="#3A2A1A" stroke-width="6"/></g></g>')
def mud(y):
    r = random.Random(3)
    return f'<rect y="{y}" width="960" height="{540-y}" fill="#5C4A36"/>' + "".join(f'<ellipse cx="{r.uniform(0,960):.0f}" cy="{r.uniform(y+10,540):.0f}" rx="{r.uniform(20,60):.0f}" ry="{r.uniform(4,9):.0f}" fill="#7A6A56" opacity="0.5"/>' for _ in range(24))
def fig(spec, x, y, s, view="3q", expr="neutral", facing=1, pose="stand", hands=("open", "fist")):
    if pose == "stand":
        return f'<g transform="translate({x},{y}) scale({s})">{figure(spec, view, "stand", expr, facing=facing, hands=hands)}</g>'
    return f'<g transform="translate({x},{y}) scale({s})">{figure(spec, "front", pose, expr, facing=facing, hands=hands)}</g>'
def head(spec, x, y, s, view="3q", expr="neutral", flip=1, look=None):
    return f'<g transform="translate({x},{y}) scale({s*flip},{s})">{head3(spec, view, expr, look)}</g>'

F = []
# 1 · Avlu: Aslaug kapıda, ön planda Lagertha profili (bulanıktan nete)
o = sky() + longhouse(80, 300, 520, 300) + f'<rect x="250" y="330" width="90" height="135" fill="#2A2018" stroke="{INK_}" stroke-width="4"/>' + mud(440)
o += fig(ASL, 300, 470, 0.36, "front", "neutral") + belly(300, 470, 0.36)
o += blur_def(1, 0) + f'<g filter="url(#b1)">' + head(LAG, 760, 300, 2.0, "side", "cold", flip=-1) + f'<path d="M640,470 Q700,420 900,440 L960,540 L600,540 Z" fill="{LAG["tunic"]}" stroke="{INK_}" stroke-width="5"/></g>'
o += cold(0.3) + bands()
F.append((o, "1 · Avlu (5 sn)", "Bir gün kapına bir kadın geliyor. Karnında senin çocuğun.", "Sabit plan. \"çocuğun\" kelimesinde netlik kapıdaki Aslaug'dan ön plandaki Lagertha'ya kayar. Duygu: şok."))
# 2 · Ev içi: Lagertha sandığa eşya koyuyor; eşikte Ragnar sırtı (omuz üstü)
o = '<rect width="960" height="540" fill="#2E241C"/>' + f'<rect x="0" y="380" width="960" height="160" fill="#3E3024"/>'
o += '<rect x="560" y="110" width="150" height="270" fill="#9AB0C4" opacity="0.55"/>'  # kapıdan gelen ışık
o += '<ellipse cx="420" cy="400" rx="80" ry="22" fill="#5A4636" stroke="#1A1410" stroke-width="4"/><path d="M370,395 Q420,250 470,395 Z" fill="#F2A54A" opacity="0.9"/><path d="M395,395 Q420,300 445,395 Z" fill="#FFE08A"/>'
o += f'<rect x="200" y="330" width="150" height="90" fill="#6E5034" stroke="{INK_}" stroke-width="5"/><path d="M200,330 L350,330 L340,300 L210,300 Z" fill="#5A4028" stroke="{INK_}" stroke-width="4"/>'
o += fig(LAG, 300, 440, 0.4, "3q", "cold", facing=-1, hands=("grip", "grip"))
o += f'<g opacity="0.95">{fig(RG, 830, 640, 0.75, "back", "neutral")}</g>'
o += cold(0.25) + bands()
F.append((o, "2 · Ev içi (6 sn)", "İkisi de kalsın istiyorsun. Ama Lagertha paylaşmaz.", "Ragnar'ın omzu üstünden. \"paylaşmaz\" kelimesinde ocak ateşi söner, kapıdan gelen ışık şeridi daralır. Duygu: soğuk kopuş."))
# 3a · Yol: araba uzaklaşıyor, Bjorn babasının yanında
o = sky("#7A8A98", "#C2CCD4") + f'<path d="M0,330 Q300,300 960,320 L960,540 L0,540 Z" fill="#4E5E4C"/>' + mud(400)
o += f'<path d="M585,370 Q590,320 610,315 Q630,320 635,370 Z" fill="{LAG["cloak"]}" stroke="{INK_}" stroke-width="3"/>' + cart(640, 420, 0.55) + f'<path d="M585,372 Q590,326 610,320 Q630,326 635,372 Z" fill="{LAG["cloak"]}" stroke="{INK_}" stroke-width="3"/>' + head(LAG, 610, 304, 0.3, "back", "neutral")
o += fig(RG, 170, 500, 0.5, "3q", "grief") + fig(BJ, 255, 500, 0.32, "3q", "grief")
o += cold(0.3) + bands()
F.append((o, "3a · Yol, ilk karar (3 sn)", "Oğlun önce seni seçiyor.", "Geniş plan. Bjorn babasının yanında, araba uzaklaşıyor. Duygu: kırılgan sevinç, sonra boşluk."))
# 3b · Bjorn koşuyor; Lagertha'nın eli halkalı bileği kavrıyor
o = sky("#7A8A98", "#C2CCD4") + f'<path d="M0,330 Q300,300 960,320 L960,540 L0,540 Z" fill="#4E5E4C"/>' + mud(380)
o += f'<path d="M370,400 Q370,280 420,262 Q470,280 470,400 Z" fill="{LAG["tunic"]}" stroke="{INK_}" stroke-width="5"/>'
o += cart(520, 470, 0.9)
o += f'<path d="M400,300 Q350,350 320,338" stroke="{LAG["tunic"]}" stroke-width="30" fill="none" stroke-linecap="round"/><path d="M400,300 Q350,350 320,338" stroke="{INK_}" stroke-width="34" fill="none" stroke-linecap="round" opacity="0" />'
o += fig(BJ, 220, 520, 0.36, "front", "determined", pose="reach")
o += f'<circle cx="318" cy="338" r="36" fill="none" stroke="#FFE08A" stroke-width="5" opacity="0.9"/><text x="318" y="292" font-family="Alegreya SC" font-size="20" text-anchor="middle" fill="#FFE08A">halka</text>'
o += head(LAG, 420, 215, 0.55, "3q", "tender", flip=-1) + f'<circle cx="320" cy="338" r="15" fill="{LAG["skin"]}" stroke="{INK_}" stroke-width="4"/>'
o += cold(0.28) + bands()
F.append((o, "3b · Yol, ikinci karar (5 sn)", "Sonra annesinin arabasının peşinden koşuyor.", "Alçak açı, takip. \"koşuyor\" kelimesinde Lagertha'nın eli Bjorn'un halkalı bileğini kavrar (kol halkası #1 eşlemesi). Duygu: umut + acı."))
# 4 · Yakın: Ragnar Bjorn'un başını öpüyor
o = sky("#6A7A8A", "#9AAAB8") + f'<rect y="380" width="960" height="160" fill="#4A5646"/>'
o += head(BJ, 420, 400, 1.3, "3q", "grief", flip=-1, look=-0.3) + head(RG, 520, 210, 1.5, "3q", "grief_closed" if "grief_closed" in EXP else "grief", flip=-1)
o += f'<path d="M300,540 Q340,470 470,470 Q560,480 600,540 Z" fill="{BJ["tunic"]}" stroke="{INK_}" stroke-width="5"/>'
o += cold(0.3) + bands()
F.append((o, "4 · Yakın plan (6 sn)", "Kal diyorsun. Yetmiyor. Oğlunun başını öpüyorsun.", "Çok yavaş yakınlaşma. \"öpüyorsun\" kelimesinde Ragnar'ın gözleri kapanır, müzik tek notaya iner. Duygu: kayıp."))
# 5 · Yol ayrımı (yukarıdan)
o = '<rect width="960" height="540" fill="#4E5E4C"/>' + f'<path d="M430,540 L470,330 L330,48 L400,48 L520,300 L760,48 L840,48 L560,330 L560,540 Z" fill="#6A5A46" stroke="{INK_}" stroke-width="4"/>'
o += "".join(f'<path d="M{x},{y} l-8,-24 l16,0 Z" fill="#2E3E32"/>' for x, y in [(random.Random(k).uniform(0, 960), random.Random(k + 99).uniform(60, 540)) for k in range(70)] if not (300 < x < 860 and y < 330) and not (400 < x < 600))
o += cart(370, 120, 0.22, flip=-1) + fig(RG, 505, 470, 0.17, "back", "neutral")
o += cold(0.32) + bands()
F.append((o, "5 · Yol ayrımı (5 sn)", "Araba gidiyor. Ve yol, ikiye ayrılıyor.", "Kamera yükselerek geri çekilir. \"gidiyor\"da araba kadrajdan çıkar, \"ayrılıyor\"da iki yol açılır. Vuruş 20'de aynı kompozisyon yankılanır. Duygu: yalnızlık."))

# sayfa
CW, CH = 960, 540; GAP = 40; TXT = 170
Wt = 2 * CW + 3 * GAP; Ht = 140 + 3 * (CH + TXT + GAP) + 20
o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{Wt}" height="{Ht}"><rect width="{Wt}" height="{Ht}" fill="#EDE2CC"/>',
     '<text x="40" y="95" font-family="Pirata One" font-size="72" fill="#2A1D14">Lagertha vedası · küçük kareler v1 (≈30 sn, 6 kare)</text>']
for i, (svg, title, line, note) in enumerate(F):
    x = GAP + (i % 2) * (CW + GAP); y = 140 + (i // 2) * (CH + TXT + GAP)
    o.append(f'<svg x="{x}" y="{y}" width="{CW}" height="{CH}" viewBox="0 0 960 540" overflow="hidden"><rect width="960" height="540" fill="#000"/>{svg}</svg>')
    o.append(f'<rect x="{x}" y="{y}" width="{CW}" height="{CH}" fill="none" stroke="#2A1D14" stroke-width="4"/>')
    o.append(f'<text x="{x}" y="{y+CH+44}" font-family="Alegreya SC" font-weight="bold" font-size="34" fill="#2A1D14">{title}</text>')
    o.append(f'<text x="{x}" y="{y+CH+86}" font-family="Alegreya" font-style="italic" font-size="30" fill="#5A2A1A">“{line}”</text>')
    words = note.split(); lines = [""]
    for w in words:
        if len(lines[-1]) + len(w) > 78: lines.append("")
        lines[-1] += w + " "
    for k, l in enumerate(lines[:3]):
        o.append(f'<text x="{x}" y="{y+CH+124+k*32}" font-family="Alegreya" font-size="25" fill="#2A1D14">{l.replace("&","&amp;")}</text>')
o.append('</svg>')
open('/home/claude/r3/veda/sb.svg', 'w').write("".join(o))
subprocess.run(['rsvg-convert', '/home/claude/r3/veda/sb.svg', '-w', '2000', '-o', '/home/claude/r3/veda/veda_kucuk_kareler_v1.png'], check=True)
print("ok")
