"""F3 eylem kartı v1: 5 eylem × 3 anahtar kare (bak, dokun, yürü, koş, turna uzat). 1280x720."""
import subprocess, sys
from pathlib import Path
P = Path(__file__).resolve().parent; sys.path.insert(0, str(P.parent))
import karakter as K
W, H = 1280, 720
EYLEM = [("bak", "dönüp bakar", ["odak", "odak", "plan"]), ("dokun", "duvara dokunur", ["odak", "kararli", "plan"]),
         ("yuru", "yürür", ["odak"] * 3), ("kos", "koşar (kaçış)", ["kararli"] * 3), ("uzat", "turna uzatır", ["sefkat"] * 3)]
def svg():
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
         '<defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2E3944"/><stop offset="1" stop-color="#171D23"/></linearGradient></defs>',
         f'<rect width="{W}" height="{H}" fill="url(#bg)"/>',
         '<text x="24" y="34" font-family="DejaVu Sans" font-size="18" fill="#fff">MICHAEL · eylem kartı v1 (5 eylem × 3 anahtar kare)</text>']
    for c, (ad, et, ifs) in enumerate(EYLEM):
        x0 = 30 + c * 250
        o.append(f'<text x="{x0+110}" y="70" font-family="DejaVu Sans" font-size="15" fill="#D8DEE4" text-anchor="middle">{et}</text>')
        for r in range(3):
            y = 290 + r * 210 if False else 0
        for k in range(3):
            pz = K.POZLAR[f"{ad}_{k+1}"]
            ek = ""
            if ad == "uzat":
                ek = f'<g transform="translate(HX,HY) translate(10,-30) scale(0.45)">{K.turna(1.0, isik=0.3*k, golge=False)}</g>'
            fig = K.figur2(K.MICHAEL, ifs[k], pz, plan=(ifs[k] == "plan"), el_on_ek=ek)
            o.append(f'<g transform="translate({x0 + 40 + k*70},{690}) scale(0.62)" opacity="{0.45 if k < 2 else 1}">{fig}</g>' if False else
                     f'<g transform="translate({x0 + 110},{250 + k*0}) " ></g>')
        # üç kareyi alt alta değil yan yana küçük ölçekte: kare k → satır k
        for k in range(3):
            pz = K.POZLAR[f"{ad}_{k+1}"]
            ek = f'<g transform="translate(HX,HY) translate(6,-34) scale(0.5)">{K.turna(1.0, isik=0.3*k, golge=False)}</g>' if ad == "uzat" else ""
            fig = K.figur2(K.MICHAEL, ifs[k], pz, plan=(ifs[k] == "plan"), el_on_ek=ek)
            yy = 280 + k * 205
            o.append(f'<rect x="{x0}" y="{yy-196}" width="230" height="200" rx="8" fill="#000" opacity="0.18"/>')
            o.append(f'<g transform="translate({x0+100},{yy}) scale(0.32)">{fig}</g>')
            o.append(f'<text x="{x0+8}" y="{yy-178}" font-family="DejaVu Sans Mono" font-size="12" fill="#7FE6FF">{k+1}</text>')
    o.append('</svg>'); return "".join(o)
if __name__ == "__main__":
    f = P / "eylem_michael_v1.svg"; f.write_text(svg())
    subprocess.run(["rsvg-convert", "-w", str(W), "-o", str(P / "eylem_michael_v1.png"), str(f)], check=True); f.unlink(); print("tamam")
