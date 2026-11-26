import sys, math, random, subprocess
sys.path[:0] = ['/home/claude/r3', '/home/claude/r2', '/home/claude/r3/veda', '/home/claude/r3/floki']
from art3 import *
import puppet
from storyboard import fig, head, cold, bands, INK_
exec(open('/home/claude/r3/floki/model_af.py').read().split("W_, H_ = 3000")[0].split("import subprocess")[1])  # ATH, FLO, CROSS_S, AXE
def kneel_back(spec, x, y, s):
    return f'<g transform="translate({x},{y}) scale({s})">{puppet.back_kneel_uc(spec).__dict__.get("svg","")}</g>'
F = []
# 1 · Şafak, liman: suya giriyor, ışık hüzmesi
o = ('<defs><linearGradient id="d1" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8A9AB0"/><stop offset="0.6" stop-color="#E8C8A0"/></linearGradient></defs><rect width="960" height="540" fill="url(#d1)"/>'
     '<path d="M0,330 L960,330 L960,540 L0,540 Z" fill="#5A7088"/>' + "".join(f'<path d="M{random.Random(k).uniform(0,960):.0f},{340+k*9} q20,-5 40,0" stroke="#B8C8D8" stroke-width="3" fill="none" opacity="0.6"/>' for k in range(20))
     + '<path d="M40,330 L330,330 L330,345 L40,345 Z" fill="#5A4430" stroke="#1A1410" stroke-width="3"/>' + "".join(f'<rect x="{x}" y="345" width="8" height="50" fill="#4A3826"/>' for x in (60, 140, 220, 300))
     + '<path d="M600,0 L700,0 L640,420 L560,420 Z" fill="#FFF2C8" opacity="0.45"/>')
o += f'<g>{fig(ATH, 600, 470, 0.32, "front", "awe", pose="arms_up")}</g><rect x="540" y="400" width="140" height="140" fill="#5A7088" opacity="0.85"/>'
o += cold(0.1) + bands()
F.append((o, "1 · Liman, şafak (5 sn)", "Dostun bir sabah ışığı görüyor. Eski tanrısına geri dönüyor.", "Geniş plan, ışığa doğru yükselen kamera. \"ışığı\"nda hüzme ona değer, kollarını açar. Duygu: arınma."))
# 2 · Kulübe, gece: tahta haç önünde diz çökmüş
o = '<rect width="960" height="540" fill="#1E1812"/><rect y="400" width="960" height="140" fill="#2E241A"/>' + "".join(f'<rect x="{x}" y="40" width="44" height="360" fill="{["#2A2018","#30251B"][i%2]}"/>' for i, x in enumerate(range(0, 960, 44)))
o += '<g transform="translate(560,240)"><rect x="-10" y="-120" width="20" height="200" fill="#5A4430" stroke="#1A1410" stroke-width="4"/><rect x="-60" y="-80" width="120" height="18" fill="#5A4430" stroke="#1A1410" stroke-width="4"/></g>'
o += '<rect x="640" y="360" width="12" height="40" fill="#E8DCC0"/><path d="M646,360 q-8,-14 0,-26 q8,12 0,26 Z" fill="#FFD27A"/><circle cx="646" cy="345" r="80" fill="#FFB050" opacity="0.18"/>'
o += f'<g transform="translate(470,470) scale(0.42)"><g transform="scale(1)">{puppet.head3(ATH, "back", "neutral") if False else ""}</g></g>'
o += fig(ATH, 470, 480, 0.45, "back", "neutral")
o += bands()
F.append((o, "2 · Kulübe, gece (6 sn)", "O gece yalnız, dua ediyor.", "Sırtına doğru yavaş yaklaşma. \"yalnız\"da mum alevi dikleşip durulur. Duygu: huzur."))
# 3 · Kapı aralanıyor, Floki
o = '<rect width="960" height="540" fill="#1E1812"/><rect y="400" width="960" height="140" fill="#2E241A"/>'
o += '<rect x="560" y="120" width="180" height="290" fill="#6A86A8" opacity="0.8"/><path d="M560,120 L520,140 L520,420 L560,410 Z" fill="#3A2C20" stroke="#1A1410" stroke-width="4"/>'
o += f'<g opacity="0.95">{fig(FLO, 660, 410, 0.4, "front", "cold")}</g>' + f'<g transform="translate(660,410) scale(0.4)">{AXE}</g>'
o += '<path d="M660,410 L360,520 L760,540 Z" fill="#6A86A8" opacity="0.2"/>'
o += f'<g filter="url(#bb)"><defs><filter id="bb"><feGaussianBlur stdDeviation="3"/></filter></defs>{fig(ATH, 200, 640, 0.7, "back", "neutral")}</g>'
o += bands()
F.append((o, "3 · Kapı (5 sn)", "Kapı açılıyor. Gelen, geminizi yapan adam.", "Athelstan'ın omzu üstünden, kapı net. \"Kapı\"da gıcırtı, mum yatar; ay ışığı içeri dolar. Floki yüzüyle görünür. Duygu: tehdit."))
# 4 · Yakın plan: gülümseme, duvarda yükselen balta gölgesi
o = '<rect width="960" height="540" fill="#2A2018"/><circle cx="480" cy="300" r="300" fill="#FFB050" opacity="0.12"/>'
o += '<g transform="translate(700,170) rotate(-30)" opacity="0.55"><rect x="-8" y="-20" width="16" height="260" fill="#0E0A08"/><path d="M8,-20 Q90,-40 96,50 Q50,40 8,60 Z" fill="#0E0A08"/></g>'
o += head(ATH, 420, 300, 1.6, "3q", "tender")
o += bands()
F.append((o, "4 · Yakın plan (4 sn)", "Dostun korkmuyor. Gülümsüyor.", "Sabit. Duvarda balta gölgesi yükselir; \"Gülümsüyor\"da beyaz flaş, ses tamamen kesilir, 1 sn siyah. Duygu: teslimiyet."))
# 5 · Siyah, yerde haç, ilk damla
o = '<rect width="960" height="540" fill="#0A0807"/><ellipse cx="480" cy="300" rx="160" ry="60" fill="#2A2018" opacity="0.7"/>'
o += f'<g transform="translate(480,300) scale(2.4)">{CROSS_S.replace("translate(0,-400)", "translate(0,0)")}</g>'
o += '<path d="M560,180 q-6,14 0,20 q6,-6 0,-20 Z" fill="#BFD8EC"/><circle cx="560" cy="250" r="12" fill="none" stroke="#BFD8EC" stroke-width="2" opacity="0.6"/>'
o += bands()
F.append((o, "5 · Tepeden, yerde haç (5 sn)", "Sen o gece orada değilsin. Onu kurtaramıyorsun.", "Sabit, tepeden. \"kurtaramıyorsun\"da yağmur başlar, ses yükselir ve doğrudan gömme sahnesine (yağmurda taşıma) bağlanır. Duygu: boşluk."))
CW, CH, GAP, TXT = 960, 540, 40, 170
Wt = 2 * CW + 3 * GAP; Ht = 140 + 3 * (CH + TXT + GAP) + 20
o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{Wt}" height="{Ht}"><rect width="{Wt}" height="{Ht}" fill="#EDE2CC"/>',
     '<text x="40" y="95" font-family="Pirata One" font-size="72" fill="#2A1D14">Athelstan\'ın ölümü · küçük kareler v1 (≈25 sn, 5 kare)</text>']
for i, (svg, title, line, note) in enumerate(F):
    x = GAP + (i % 2) * (CW + GAP); y = 140 + (i // 2) * (CH + TXT + GAP)
    o.append(f'<svg x="{x}" y="{y}" width="{CW}" height="{CH}" viewBox="0 0 960 540" overflow="hidden"><rect width="960" height="540" fill="#000"/>{svg}</svg><rect x="{x}" y="{y}" width="{CW}" height="{CH}" fill="none" stroke="#2A1D14" stroke-width="4"/>')
    o.append(f'<text x="{x}" y="{y+CH+44}" font-family="Alegreya SC" font-weight="bold" font-size="34" fill="#2A1D14">{title}</text><text x="{x}" y="{y+CH+86}" font-family="Alegreya" font-style="italic" font-size="30" fill="#5A2A1A">“{line}”</text>')
    words = note.split(); lines = [""]
    for w in words:
        if len(lines[-1]) + len(w) > 78: lines.append("")
        lines[-1] += w + " "
    for k, l in enumerate(lines[:3]): o.append(f'<text x="{x}" y="{y+CH+124+k*32}" font-family="Alegreya" font-size="25" fill="#2A1D14">{l}</text>')
o.append('</svg>')
open('sb.svg', 'w').write("".join(o))
subprocess.run(['rsvg-convert', 'sb.svg', '-w', '2000', '-o', 'athelstan_olum_kucuk_kareler_v1.png'], check=True); print("ok")
