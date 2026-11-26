import sys, random, subprocess
sys.path[:0] = ['/home/claude/r3', '/home/claude/r2', '/home/claude/r3/paris', '/home/claude/r3/veda']
from models import *
import importlib.util as _u; _s=_u.spec_from_file_location('vsb','/home/claude/r3/veda/storyboard.py'); _m=_u.module_from_spec(_s); _s.loader.exec_module(_m); cold, bands = _m.cold, _m.bands
exec(open('/home/claude/r3/floki/model_af.py').read().split("W_, H_ = 3000")[0].split("import subprocess")[1])
def F(spec, x, y, s, view="front", expr="neutral", extra="", facing=1):
    return f'<g transform="translate({x},{y}) scale({s*facing},{s})">{figure(spec, view, "stand", expr)}{extra}</g>'
def H(spec, x, y, s, view="3q", expr="neutral", flip=1):
    return f'<g transform="translate({x},{y}) scale({s*flip},{s})">{head3(spec, view, expr)}</g>'
WALLS = ('<rect width="960" height="540" fill="#9AA6B0"/><path d="M0,140 L960,110 L960,540 L0,540 Z" fill="#8A8478"/>'
         + "".join(f'<rect x="{x}" y="{100 - 30*(x%3==0)}" width="46" height="40" fill="#8A8478" stroke="#5A564E" stroke-width="3"/>' for x in range(0, 960, 70))
         + "".join(f'<path d="M{x},{y} h60" stroke="#6A665E" stroke-width="2"/>' for x in range(0, 960, 60) for y in range(170, 400, 40)))
COFFIN = '<g><path d="M-170,-40 L170,-50 L190,0 L170,40 L-170,30 L-190,0 Z" fill="#4A3424" stroke="#1A1410" stroke-width="5"/><path d="M-150,-10 q20,-12 40,0 q20,12 40,0 q20,-12 40,0 q20,12 40,0 q20,-12 40,0 q20,12 40,0" stroke="#7A5A3A" stroke-width="4" fill="none"/></g>'
Fr = []
# 1 · kamp: solgun Ragnar yatıyor, rahip başına su döküyor, arkada dev surlar
o = WALLS + '<path d="M0,420 L960,420 L960,540 L0,540 Z" fill="#6A6A4A"/><path d="M120,330 L330,330 L360,250 L90,250 Z" fill="#C8B898" stroke="#1A1410" stroke-width="4"/>'
o += f'<g transform="translate(470,430) rotate(-90) scale(0.36)">{figure(RAG3D, "front", "stand", "fakedead")}</g>'
o += F(BISH, 640, 470, 0.34, extra=ROBE_B) + '<path d="M600,300 q-20,10 -40,40" stroke="#9AC0E0" stroke-width="5" fill="none"/>'
o += cold(0.1) + bands()
Fr.append((o, "1 · Kamp (5 sn)", "Surları aşamıyorsun. O yüzden ölmeye karar veriyorsun.", "Yandan, surlar arka planda dev gibi. \"ölmeye\"de su başına değer, dudağının kenarı belli belirsiz kıvrılır. Duygu: kurnazlık."))
# 2 · tabutun içinden: Lagertha, Rollo yerine Bjorn?, Floki eğiliyor
o = '<rect width="960" height="540" fill="#0A0806"/><path d="M200,48 L760,48 L700,492 L260,492 Z" fill="#7A8A9A"/>'
o += H(FLO, 480, 330, 1.6, "front", "smug") + '<path d="M200,48 L260,492 L0,492 L0,48 Z M760,48 L700,492 L960,492 L960,48 Z" fill="#2A1E14"/>'
o += '<path d="M40,200 q60,-30 120,0 q-60,24 -120,0 Z" fill="#E6D8C0"/><circle cx="100" cy="200" r="16" fill="#6A8CA0"/><circle cx="100" cy="200" r="7" fill="#0A0806"/>' + bands()
Fr.append((o, "2 · Tabuttan bakış (6 sn)", "Herkes tabutuna veda etmeye geliyor. Sen her şeyi duyuyorsun.", "Ragnar'ın bakış açısı, kapak aralığı. Lagertha, Rollo, Floki sırayla eğilir; Floki homurdanır. \"duyuyorsun\"da köşede Ragnar'ın tek gözü aralanır. Duygu: kara mizah."))
# 3 · kapı: altı Viking tabutu taşıyor, Frank mızrakları
o = WALLS + '<rect x="330" y="160" width="300" height="300" fill="#2A2018" stroke="#1A1410" stroke-width="6"/><path d="M0,440 L960,440 L960,540 L0,540 Z" fill="#7A7060"/>'
for k, x in enumerate((90, 160, 800, 870)): o += F(FRANK, x, 500, 0.24, extra=MAIL + HELM + SPEAR)
for k, x in enumerate((380, 450, 520, 590)): o += F(CARRY if k % 2 else CARRY2, x, 510, 0.26, "3q")
o += f'<g transform="translate(485,330) scale(0.6)">{COFFIN}</g>' + cold(0.15) + bands()
Fr.append((o, "3 · Şehir kapısı (5 sn)", "Altı silahsız adam seni şehre taşıyor. Silahlar tabutta.", "Yüksek açı, ağır yürüyüş. \"Silahlar\"da tabuttan metal şıngırtısı, bir asker başını çevirir. Duygu: gerilim."))
# 4 · kilise: kapak patlar, Ragnar kalkar
o = '<rect width="960" height="540" fill="#3A3028"/>' + "".join(f'<rect x="{x}" y="40" width="60" height="420" fill="#4A4036" stroke="#2A2018" stroke-width="3"/><path d="M{x},40 Q{x+30},0 {x+60},40" fill="#4A4036"/>' for x in (60, 820))
o += '<path d="M400,0 L560,0 L620,440 L340,440 Z" fill="#FFE8B0" opacity="0.35"/><rect x="420" y="120" width="120" height="160" fill="#C9A25A" opacity="0.4"/>'
o += F(BISH, 720, 470, 0.36, extra=ROBE_B + MITRE + CROZIER) + f'<g transform="translate(480,430) scale(0.7)">{COFFIN}</g>'
o += '<g transform="translate(560,300) rotate(-35) scale(0.7)"><path d="M-170,-14 L170,-20 L180,10 L-170,14 Z" fill="#4A3424" stroke="#1A1410" stroke-width="5"/></g>'
o += F(RAG3, 470, 430, 0.36, "front", "sly", extra='<g transform="translate(90,-300) rotate(-30)"><rect x="-6" y="-200" width="12" height="200" fill="#AAB2BA" stroke="#1A1410" stroke-width="4"/></g>')
o += "".join(f'<circle cx="{480 + 160*__import__("math").cos(a)}" cy="{330 + 90*__import__("math").sin(a)}" r="10" fill="#E8D8B8" opacity="0.7"/>' for a in [k*0.6 for k in range(10)])
o += bands()
Fr.append((o, "4 · Kilise, doruk (6 sn)", "Kilisede ayağa kalkıyorsun. Rahipler bunu programa yazmamıştı.", "Hızlı yaklaşma, sarsıntı, ışıkta toz patlaması. \"kalkıyorsun\"da kapak patlar; \"programa\"da kısa sessizlik ve donmuş piskopos yüzü. Piskopos rehine, ölüm gösterilmez. Duygu: zafer."))
# 5 · kapılar açılır, Bjorn'un halkalı kolu tutar
o = WALLS + '<path d="M300,140 L660,140 L660,460 L300,460 Z" fill="#E8DCC0"/><path d="M300,140 L230,170 L230,470 L300,460 Z M660,140 L730,170 L730,470 L660,460 Z" fill="#4A3424" stroke="#1A1410" stroke-width="5"/>'
o += "".join(F(CARRY2 if k % 2 else CARRY, 360 + k * 70, 470 - (k % 2) * 8, 0.16, "front", "angry") for k in range(4))
o += F(BJA, 560, 520, 0.42, "3q", "grief", facing=-1, extra=BJ_EXTRA[1]) + f'<g transform="translate(450,500) rotate(-25) scale(0.38)">{figure(RAG3D, "3q", "stand", "fakedead")}</g>'
o += '<circle cx="520" cy="370" r="26" fill="none" stroke="#FFE08A" stroke-width="5"/>' + cold(0.1) + bands()
Fr.append((o, "5 · Kapılar (6 sn)", "Kapılar açılıyor. Ve sen oğlunun kollarına yığılıyorsun.", "Geniş plandan yakına. \"açılıyor\"da kanatlar ayrılır, Vikingler akın eder; \"yığılıyorsun\"da Bjorn'un halkalı kolu onu tutar. Duygu: zaferden kırılganlığa."))
CW, CH, GAP, TXT = 960, 540, 40, 170
Wt = 2 * CW + 3 * GAP; Ht = 140 + 3 * (CH + TXT + GAP) + 20
o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{Wt}" height="{Ht}"><rect width="{Wt}" height="{Ht}" fill="#EDE2CC"/>',
     '<text x="40" y="95" font-family="Pirata One" font-size="72" fill="#2A1D14">Paris\'te sahte ölüm · küçük kareler v1 (≈28 sn, 5 kare)</text>']
for i, (svg, title, line, note) in enumerate(Fr):
    x = GAP + (i % 2) * (CW + GAP); y = 140 + (i // 2) * (CH + TXT + GAP)
    o.append(f'<svg x="{x}" y="{y}" width="{CW}" height="{CH}" viewBox="0 0 960 540" overflow="hidden"><rect width="960" height="540" fill="#000"/>{svg}</svg><rect x="{x}" y="{y}" width="{CW}" height="{CH}" fill="none" stroke="#2A1D14" stroke-width="4"/>')
    o.append(f'<text x="{x}" y="{y+CH+44}" font-family="Alegreya SC" font-weight="bold" font-size="34" fill="#2A1D14">{title}</text><text x="{x}" y="{y+CH+86}" font-family="Alegreya" font-style="italic" font-size="28" fill="#5A2A1A">“{line}”</text>')
    words = note.split(); lines = [""]
    for w in words:
        if len(lines[-1]) + len(w) > 78: lines.append("")
        lines[-1] += w + " "
    for k, l in enumerate(lines[:3]): o.append(f'<text x="{x}" y="{y+CH+124+k*32}" font-family="Alegreya" font-size="25" fill="#2A1D14">{l}</text>')
o.append('</svg>')
open('sb.svg', 'w').write("".join(o))
subprocess.run(['rsvg-convert', 'sb.svg', '-w', '2000', '-o', 'paris_kucuk_kareler_v1.png'], check=True); print("ok")
