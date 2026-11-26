"""F3 model kartı: Lincoln ve Sara (Michael ile aynı yüz sistemi). 1280x720 taslak çözünürlüğü."""
import subprocess, sys
from pathlib import Path
P = Path(__file__).resolve().parent; sys.path.insert(0, str(P.parent))
import karakter as K
W, H = 1280, 720
def et(x, y, t, s=14, c="#D8DEE4"): return f'<text x="{x}" y="{y}" font-family="DejaVu Sans" font-size="{s}" fill="{c}" text-anchor="middle">{t}</text>'
def g(x, y, sc, inner): return f'<g transform="translate({x},{y}) scale({sc})">{inner}</g>'
o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}">',
     '<defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2E3944"/><stop offset="1" stop-color="#171D23"/></linearGradient></defs>',
     f'<rect width="{W}" height="{H}" fill="url(#bg)"/>',
     '<text x="24" y="34" font-family="DejaVu Sans" font-size="18" fill="#fff">LINCOLN ve SARA · model kartı v1 (Michael yüz sistemi)</text>']
# Lincoln
o.append(g(150, 690, 0.95, K.figur2(K.LINCOLN, "kararli")))
o.append(et(150, 712, "Lincoln · ağabey (idam koğuşu)"))
for i, (v, e) in enumerate((("front", "odak"), ("3q", "odak"), ("side", "odak"))):
    o.append(g(340 + i * 110, 130, 0.48, K.kafa(K.LINCOLN, v, e)))
for i, e in enumerate(("kararli", "ofke", "yas", "sefkat")):
    o.append(g(340 + i * 92, 300, 0.4, K.kafa(K.LINCOLN, "3q", e))); o.append(et(340 + i * 92, 365, e, 12))
# kardeşler yan yana
o.append(g(430, 690, 0.5, K.figur2(K.LINCOLN, "sefkat")))
o.append(g(540, 690, 0.5, K.figur2(K.MICHAEL, "odak")))
o.append(g(640, 690, 0.5, K.figur2(K.SARA, "odak")))
o.append(et(535, 712, "boy ve yapı: Lincoln · Michael · Sara"))
# Sara
o.append(g(1140, 690, 0.95, K.figur2(K.SARA, "sefkat")))
o.append(et(1130, 712, "Sara · revir doktoru"))
for i, (v, e) in enumerate((("front", "odak"), ("3q", "odak"), ("side", "odak"))):
    o.append(g(760 + i * 110, 130, 0.48, K.kafa(K.SARA, v, e)))
for i, e in enumerate(("sefkat", "korku", "yas", "kararli")):
    o.append(g(760 + i * 92, 300, 0.4, K.kafa(K.SARA, "3q", e))); o.append(et(760 + i * 92, 365, e, 12))
# üçlü yüz yan yana (aile / farklılık)
for i, sp in enumerate((K.LINCOLN, K.MICHAEL, K.SARA)):
    o.append(g(790 + i * 110, 520, 0.5, K.kafa(sp, "3q", "odak")))
o.append(et(900, 600, "Lincoln · Michael · Sara (aynı stil, farklı kişi)", 13))
o.append('</svg>')
f = P / "model_yan_v1.svg"; f.write_text("".join(o))
subprocess.run(["rsvg-convert", "-w", str(W), "-o", str(P / "model_yan_v1.png"), str(f)], check=True); f.unlink(); print("tamam")
