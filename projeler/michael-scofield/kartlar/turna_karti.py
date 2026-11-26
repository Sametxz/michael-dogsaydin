"""Turna nesne kartı v3: büyük çizim, %200 kırpma (R13), sabah ışığı, kanat çırpma, küçük boyut okunurluğu."""
import subprocess, sys
from pathlib import Path
P = Path(__file__).resolve().parent; sys.path.insert(0, str(P.parent))
import karakter as K
W, H = 1280, 720
def t(x, y, s, **k): return f'<g transform="translate({x},{y})">{K.turna(s, **k)}</g>'
o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
     '<defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2E3944"/><stop offset="1" stop-color="#171D23"/></linearGradient>'
     '<linearGradient id="sabah" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#F3D9A8"/><stop offset="1" stop-color="#B98A5A"/></linearGradient></defs>',
     f'<rect width="{W}" height="{H}" fill="url(#bg)"/>',
     '<text x="24" y="34" font-family="DejaVu Sans" font-size="18" fill="#fff">KÂĞIT TURNA · nesne kartı v3 (gerçekçi origami)</text>',
     t(300, 360, 2.6),
     '<text x="300" y="560" font-family="DejaVu Sans" font-size="14" fill="#D8DEE4" text-anchor="middle">ana çizim (nötr ışık)</text>',
     '<rect x="620" y="70" width="300" height="300" rx="10" fill="url(#sabah)"/>',
     '<path d="M620,330 H920 V370 H620 Z" fill="#E9E1D2"/><path d="M620,330 H920" stroke="#15110E" stroke-width="3"/>',
     t(770, 290, 1.4, isik=1.0),
     '<text x="770" y="392" font-family="DejaVu Sans" font-size="14" fill="#D8DEE4" text-anchor="middle">sabah ışığında, yatak başında</text>',
     t(1010, 300, 0.9, kanat=-0.3), t(1160, 300, 0.9, kanat=1.0),
     '<text x="1080" y="392" font-family="DejaVu Sans" font-size="14" fill="#D8DEE4" text-anchor="middle">kanat çırpma: açık / kalkık</text>',
     '<text x="780" y="470" font-family="DejaVu Sans" font-size="14" fill="#D8DEE4" text-anchor="middle">küçük boyut okunurluğu (120 / 60 / 32 px)</text>',
     t(680, 600, 0.55), t(830, 610, 0.28), t(930, 615, 0.15),
     '</svg>']
f = P / "turna_v3.svg"; f.write_text("".join(o))
subprocess.run(["rsvg-convert", "-w", str(W), "-o", str(P / "turna_v3.png"), str(f)], check=True); f.unlink()
# R13: %200 kırpma
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(P / "turna_v3.png"), "-vf", "crop=360:300:120:200,scale=720:600", str(P / "turna_v3_r13.png")], check=True)
print("tamam")
