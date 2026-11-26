"""F3 model kartı v1: Michael (yetişkin + 11 yaş), görünüşler, ifadeler, dövme ayrıntısı, turna.
Çıktı: model_michael_v1.png (1280x720, taslak çözünürlüğü). Kullanım: python3 model_michael.py
"""
import subprocess, sys
from pathlib import Path
P = Path(__file__).resolve().parent; sys.path.insert(0, str(P.parent))
import karakter as K

W, H = 1280, 720

def etiket(x, y, t, s=15, c="#D8DEE4", anchor="middle"):
    return f'<text x="{x}" y="{y}" font-family="DejaVu Sans" font-size="{s}" fill="{c}" text-anchor="{anchor}">{t}</text>'

def g(x, y, sc, inner):
    return f'<g transform="translate({x},{y}) scale({sc})">{inner}</g>'

def kart():
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
         '<defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2E3944"/><stop offset="1" stop-color="#171D23"/></linearGradient>'
         '<radialGradient id="spot" cx="0.5" cy="0.4" r="0.6"><stop offset="0" stop-color="#FFE2B8" stop-opacity="0.22"/><stop offset="1" stop-color="#FFE2B8" stop-opacity="0"/></radialGradient>'
         '<filter id="glow"><feGaussianBlur stdDeviation="3"/><feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>',
         f'<rect width="{W}" height="{H}" fill="url(#bg)"/>',
         f'<ellipse cx="190" cy="420" rx="200" ry="320" fill="url(#spot)"/>',
         etiket(24, 34, "MICHAEL · model kartı v1 (taslak çözünürlüğü)", 18, "#FFFFFF", "start")]
    # yetişkin tam figür
    o.append(g(190, 690, 1.0, K.figur(K.MICHAEL, "odak", eller=("relax", "relax"))))
    o.append(etiket(190, 712, "yetişkin · Fox River"))
    # görünüşler
    for x, v in ((440, "front"), (580, "3q"), (720, "side")):
        o.append(g(x, 140, 0.52, K.kafa(K.MICHAEL, v, "odak")))
        o.append(etiket(x, 222, {"front": "önden", "3q": "3/4", "side": "yandan"}[v], 13))
    # ifadeler
    for i, (e, ad) in enumerate((("odak", "odak"), ("kararli", "kararlı"), ("yas", "yas"), ("korku", "korku"), ("sefkat", "şefkat"), ("plan", "plan görüşü"))):
        x = 410 + i * 108
        o.append(g(x, 330, 0.42, K.kafa(K.MICHAEL, "3q", e)))
        o.append(etiket(x, 400, ad, 13, "#7FE6FF" if e == "plan" else "#D8DEE4"))
    # dövme: önkol ayrıntısı, kapalı ve ışıklı
    for x, pl, ad in ((520, False, "önkol dövmesi"), (700, True, "plan ışıklandığında")):
        kolsvg = K.kol([(0, -40), (0, 0), (0, 150)], 70, K.MICHAEL["shirt"], K.MICHAEL["skin"], cuff_t=0.5, dovme=True, plan=pl)
        o.append(g(x, 500, 0.85, kolsvg + K.hand3(0, 168, 26, K.MICHAEL["skin"], "fist", 1)))
        o.append(etiket(x, 712, ad, 13, "#7FE6FF" if pl else "#D8DEE4"))
    # turna
    o.append(g(880, 150, 1.0, K.turna(1.0, isik=0.6)))
    o.append(etiket(880, 222, "kâğıt turna (ana motif)", 13))
    o.append(g(880, 560, 0.7, K.turna(1.0, isik=0.0, kanat=0.8)))
    o.append(etiket(880, 600, "kanat çırpma pozu", 12))
    # çocuk
    o.append(g(1150, 690, 1.0, K.figur(K.MICHAEL_COCUK, "korku", eller=("relax", "relax"))))
    o.append(etiket(1150, 712, "11 yaş"))
    o.append(g(1150, 140, 0.5, K.kafa(K.MICHAEL_COCUK, "3q", "sefkat")))
    o.append('</svg>')
    return "".join(o)

if __name__ == "__main__":
    svg = P / "model_michael_v1.svg"; svg.write_text(kart())
    subprocess.run(["rsvg-convert", "-w", str(W), "-o", str(P / "model_michael_v1.png"), str(svg)], check=True)
    svg.unlink(); print("tamam")
