import sys; sys.path[:0] = ['/home/claude/r3', '/home/claude/r2']
from art3 import *
import subprocess
INK_ = "#1A1410"
CROSS_S = '<g transform="translate(0,-400)"><path d="M-30,-60 Q0,-20 30,-60" stroke="#6A4A30" stroke-width="3" fill="none"/><g transform="translate(0,-18)"><rect x="-5" y="-6" width="10" height="34" fill="#4A3424" stroke="#1A1410" stroke-width="3"/><rect x="-14" y="2" width="28" height="9" fill="#4A3424" stroke="#1A1410" stroke-width="3"/><path d="M9,4 l4,3" stroke="#C8B89A" stroke-width="2"/></g></g>'
ATH = dict(RAGNAR3, hair="#7A5636", beard_c="#7A5636", beard_len=0.42, beard_w=0.86, iris="#6A8A5A", skin="#F0CCA8",
           tunic="#7A6A54", trim="#9A8A70", cloak="#4A3E32", fur_collar="#8A7A62", armring=False, clasp=CROSS_S, brow_c="#5A3E26", brow_k=0.7, face_scar=False, knot=False, beard_braid=False, side_braids=False)
FLO = dict(RAGNAR3, hair="#3E3024", beard_c="#3E3024", beard_len=0.62, beard_w=0.55, iris="#8AB4C8", skin="#E6C09A",
           tunic="#4E4A3A", trim="#7A6A4A", cloak="#2E3230", fur_collar="#6A6052", armring=False, clasp="", brow_c="#2A2018", brow_k=0.85, face_scar=False, knot=False, beard_braid=True)
AXE = ('<g transform="translate(70,-250) rotate(12)"><rect x="-6" y="-170" width="12" height="230" rx="4" fill="#6A5038" stroke="#1A1410" stroke-width="4"/>'
       '<path d="M6,-168 Q60,-180 66,-120 Q40,-128 6,-112 Z" fill="#A8B0B8" stroke="#1A1410" stroke-width="4"/><path d="M50,-160 Q58,-140 56,-124" stroke="#E8EEF2" stroke-width="3" fill="none"/></g>')
W_, H_ = 3000, 2000
o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W_}" height="{H_}"><rect width="{W_}" height="{H_}" fill="#EDE2CC"/>',
     '<text x="60" y="90" font-family="Pirata One" font-size="80" fill="#2A1D14">Athelstan &amp; Floki · model sayfası v2 (özgün tasarım)</text>']
for i, (v, lab) in enumerate([("front", "ÖN"), ("3q", "3/4"), ("side", "PROFİL")]):
    x = 220 + i * 330
    o.append(f'<g transform="translate({x},900) scale(0.95)">{figure(ATH, v, "stand", "neutral", hands=("open", "open"))}</g>')
    o.append(f'<text x="{x}" y="960" font-family="Alegreya SC" font-weight="bold" font-size="36" text-anchor="middle">{lab}</text>')
o.append('<text x="550" y="1030" font-family="Alegreya SC" font-weight="bold" font-size="34" text-anchor="middle" fill="#5A2A1A">ATHELSTAN · S3, Viking tuniği, kısa sakal, boynunda çentikli koyu haç</text>')
for i, (v, lab) in enumerate([("front", "ÖN"), ("3q", "3/4"), ("side", "PROFİL")]):
    x = 1300 + i * 330
    o.append(f'<g transform="translate({x},900) scale(0.88,0.97)">{figure(FLO, v, "stand", "smug", hands=("open", "grip"))}</g>')
    if v == "3q": o.append(f'<g transform="translate({x},900) scale(0.88,0.97)">{AXE}</g>')
    o.append(f'<text x="{x}" y="960" font-family="Alegreya SC" font-weight="bold" font-size="36" text-anchor="middle">{lab}</text>')
o.append('<text x="1630" y="1080" font-family="Alegreya SC" font-weight="bold" font-size="44" text-anchor="middle" fill="#5A2A1A">FLOKI · sıska gemici, keçi sakalı, gemici baltası</text>')
for k, e in enumerate(["neutral", "tender", "grief", "awe"]):
    cx = 2500 + (k % 2) * 260; cy = 260 + (k // 2) * 330
    o.append(f'<g transform="translate({cx},{cy}) scale(0.9)">{head3(ATH, "3q", e)}</g><text x="{cx}" y="{cy+170}" font-family="Alegreya SC" font-size="28" text-anchor="middle">Athelstan · {e}</text>')
for k, e in enumerate(["smug", "cold", "angry", "laugh"]):
    cx = 2500 + (k % 2) * 260; cy = 1000 + (k // 2) * 330
    o.append(f'<g transform="translate({cx},{cy}) scale(0.9)">{head3(FLO, "3q", e)}</g><text x="{cx}" y="{cy+170}" font-family="Alegreya SC" font-size="28" text-anchor="middle">Floki · {e}</text>')
# yakın planlar + haç detayı + boy
o.append(f'<g transform="translate(400,1540) scale(1.5)">{head3(ATH, "3q", "tender")}</g><text x="400" y="1960" font-family="Alegreya SC" font-weight="bold" font-size="32" text-anchor="middle">Athelstan · son an (gülümseme)</text>')
o.append(f'<g transform="translate(950,1540) scale(1.5,1.5)">{head3(FLO, "side", "cold")}</g><text x="950" y="1960" font-family="Alegreya SC" font-weight="bold" font-size="32" text-anchor="middle">Floki · profil</text>')
o.append(f'<g transform="translate(1450,1650) scale(4)">{CROSS_S.replace("translate(0,-400)", "translate(0,0)")}</g><text x="1450" y="1960" font-family="Alegreya SC" font-weight="bold" font-size="32" text-anchor="middle">haç: koyu ahşap, sağ kolda çentik</text>')
for j, (sp, sc, lab) in enumerate(((RAGNAR_UC, (1, 1), "Ragnar"), (ATH, (0.97, 0.95), "Athelstan"), (FLO, (0.86, 1.0), "Floki"))):
    x = 1900 + j * 190
    o.append(f'<g transform="translate({x},1900) scale({0.55*sc[0]},{0.55*sc[1]})">{figure(sp, "3q", "stand", "neutral")}</g><text x="{x}" y="1950" font-family="Alegreya SC" font-size="26" text-anchor="middle">{lab}</text>')
o.append('</svg>')
open('model_af.svg', 'w').write("".join(o))
subprocess.run(['rsvg-convert', 'model_af.svg', '-w', '1800', '-o', 'athelstan_floki_v2.png'], check=True); print("ok")
