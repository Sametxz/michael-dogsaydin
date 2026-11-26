"""Yan karakter yüzleri (Lincoln, Sara, ...) — Michael yüz sisteminin (yetiskin.py v5) parametreli hâli.
Aynı stil (2 ton sıcak cel, temiz çizgi, canlı badem göz), farklı kişi: genişlik, göz, kaş, sakal, saç, çene.
Hiçbir gerçek kişinin yüzü örnek alınmadı.
spec alanları: skin/skin_sh/skin_dk/skin_hl, hair, brow, iris, iris_d, en (yüz genişliği), goz_k, kas_k,
sakal (0..1 opaklık), female (yumuşak çene + uzun dalgalı saç), dudak (dudak rengi), sac_stil.
"""
import inspect, re, sys
from pathlib import Path
P = Path(__file__).resolve().parent
if str(P) not in sys.path: sys.path.insert(0, str(P))
import yetiskin as Y
from art2 import shade

INK = Y.INK

# ── yetiskin.kafa kaynağından parametreli kopya üret (tek yüz sistemi, iki yerde elle bakım yok)
_src = inspect.getsource(Y.kafa)
_src = _src.replace("def kafa(", "def _kafa_param(", 1)
_src = re.sub(r"    if spec is not None and \(spec\.get\(\"child\"\).*?\n        return _ESKI_KAFA\(spec, view, ifade, look\).*?\n", "", _src, flags=re.S)
_src = _src.replace("    sp = dict(MICHAEL_Y)\n", "    sp = dict(MICHAEL_Y); sp.update(spec or {})\n", 1)
_src = _src.replace('fill="{hair}" opacity="0.28" filter="url(#{sid})"', 'fill="{hair}" opacity="{sp.get(\'sakal\', 0.28):.2f}" filter="url(#{sid})"')
_src = _src.replace('fill="{hair}" opacity="0.14" filter="url(#{sid})"', 'fill="{hair}" opacity="{sp.get(\'sakal\', 0.28)*0.5:.2f}" filter="url(#{sid})"')
_src = _src.replace("        eh = ew * 0.72\n", "        ew = ew * sp.get('goz_k', 1.0); eh = ew * 0.72\n")
_src = _src.replace("ince=uz))", "ince=uz or sp.get('female', False), olcek=sp.get('kas_k', 1.0)))")
# kadın: yumuşak, yuvarlak çene; kazınmış saç kapağı yerine saç ayrı çizilir
_src = _src.replace('    cid = _uid("f"); bid = _uid("b"); sid = _uid("s")\n',
    '    if sp.get("female"): face = _yumusak_cene(face, view); cap = "M0,0 Z"\n    cid = _uid("f"); bid = _uid("b"); sid = _uid("s")\n', 1)
_ns = dict(vars(Y))
exec(compile(_src, "yuzler<kafa>", "exec"), _ns)
_kafa_param = _ns["_kafa_param"]

def _yumusak_cene(face, view):
    if view == "front":
        return face.replace("L38,80 C32,85 26,88 18,89 L-18,89 C-26,88 -32,85 -38,80", "C44,76 24,92 0,92 C-24,92 -44,76 -50,64")
    if view == "3q":
        return face.replace("L40,89 L8,91", "C44,84 28,93 14,92 C10,92 9,91 8,91")
    return face
_ns["_yumusak_cene"] = _yumusak_cene

def _kadin_sac(view, hair, arka):
    """Omuza dökülen dalgalı saç, yandan ayrık perçem. arka=True: başın arkasındaki kütle."""
    hd = shade(hair, 0.78); hl = shade(hair, 1.45)
    if arka:
        d = {"front": "M-74,-40 C-96,30 -92,110 -70,150 C-50,166 -30,150 -40,120 L40,120 C30,150 50,166 70,150 C92,110 96,30 74,-40 Z",
             "3q": "M-70,-40 C-98,30 -96,110 -78,152 C-58,170 -34,156 -40,120 C-20,130 0,120 6,100 L-40,-40 Z",
             "side": "M-74,-50 C-104,20 -100,110 -80,156 C-58,172 -30,160 -34,124 C-20,96 -14,40 -20,-60 Z"}[view]
        return (f'<path d="{d}" fill="{hd}" stroke="{INK}" stroke-width="4.5" stroke-linejoin="round"/>'
                f'<path d="M-70,0 C-82,60 -76,110 -62,140" stroke="{shade(hd,0.8)}" stroke-width="3" fill="none" opacity="0.7"/>')
    d = {"front": "M-66,-20 C-74,-100 -30,-122 6,-120 C46,-118 72,-96 66,-24 C60,-60 40,-78 14,-82 C-2,-60 -30,-46 -58,-40 C-62,-30 -64,-24 -66,-20 Z",
         "3q": "M-62,-16 C-72,-104 -14,-124 22,-120 C62,-116 84,-88 78,-30 C70,-62 52,-80 28,-84 C10,-60 -20,-46 -46,-44 C-54,-36 -58,-26 -62,-16 Z",
         "side": "M-70,-20 C-76,-104 -20,-124 16,-118 C50,-112 68,-90 66,-60 C50,-76 30,-82 10,-80 C-6,-70 -14,-56 -20,-40 C-30,-30 -50,-24 -70,-20 Z"}[view]
    side_lock = {"front": "M58,-40 C74,10 70,70 58,110 C52,100 54,40 50,-20 Z",
                 "3q": "M70,-40 C88,10 84,74 70,112 C62,100 66,40 62,-24 Z",
                 "side": ""}[view]
    o = [f'<path d="{d}" fill="{hair}" stroke="{INK}" stroke-width="4.5" stroke-linejoin="round"/>']
    if side_lock: o.append(f'<path d="{side_lock}" fill="{hair}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>')
    o.append(f'<path d="M-30,-104 C0,-118 34,-112 56,-94" stroke="{hl}" stroke-width="7" fill="none" opacity="0.45" stroke-linecap="round"/>'
             f'<path d="M-10,-86 C10,-96 30,-94 46,-84 M-40,-70 C-20,-84 0,-88 20,-86" stroke="{hd}" stroke-width="2.2" fill="none" opacity="0.7"/>')
    return "".join(o)

def kafa(spec, view="3q", ifade="odak", look=None):
    """karakter.kafa ile aynı sözleşme. Merkez (0,0), sağa bakar."""
    sp = dict(spec)
    body = _kafa_param(sp, view, ifade, look)
    if sp.get("female"):
        # dudak rengi (hafif) ve kirpik vurgusu
        mx, my = {"front": (0, 52), "3q": (34, 52), "side": (66, 42)}[view]
        dud = f'<ellipse cx="{mx}" cy="{my+5}" rx="{11 if view!="side" else 4}" ry="4" fill="{sp.get("dudak","#C77566")}" opacity="0.55"/>'
        kir = "".join(f'<path d="M{x},{y} l{5 if x > 0 and view == "front" else -5},-5 M{x + (-4 if x > 0 and view == "front" else 4)},{y-3} l{3 if x > 0 and view == "front" else -3},-6" stroke="{INK}" stroke-width="2.4" stroke-linecap="round"/>'
                      for x, y in {"front": [(44, -9), (-44, -9)], "3q": [(-12, -8)], "side": [(38, -8)]}[view])
        body = _kadin_sac(view, sp["hair"], True) + body + dud + kir + _kadin_sac(view, sp["hair"], False)
    if sp.get("yas_cizgi") and view != "side":
        cx = 0 if view == "front" else 30
        body += (f'<path d="M{cx-22},-58 q22,-6 44,0 M{cx-14},-50 q14,-4 28,0" stroke="{sp["skin_dk"]}" stroke-width="2" fill="none" opacity="0.45"/>'
                 f'<path d="M{cx+18 if view=="front" else 54},38 q6,10 4,20" stroke="{sp["skin_dk"]}" stroke-width="2.2" fill="none" opacity="0.4"/>')
    en = sp.get("en", 1.0)
    return f'<g transform="scale({en},1)">{body}</g>' if en != 1.0 else body
