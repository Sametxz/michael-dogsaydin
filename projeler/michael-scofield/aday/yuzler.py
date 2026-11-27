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
_src = _src.replace("        eh = ew * 0.72\n", "        ew = ew * sp.get('goz_k', 1.0); eh = ew * sp.get('goz_h', 0.72)\n")
_src = _src.replace("ince=uz))", "ince=uz or sp.get('female', False), olcek=sp.get('kas_k', 1.0)))")
# kadın: yumuşak, yuvarlak çene; kazınmış saç kapağı yerine saç ayrı çizilir
_src = _src.replace('    cid = _uid("f"); bid = _uid("b"); sid = _uid("s")\n',
    '    if sp.get("female"): face = _yumusak_cene(face, view); cap = "M0,0 Z"\n    cid = _uid("f"); bid = _uid("b"); sid = _uid("s")\n', 1)
_src = _src.replace("    lk = 0.25 if look is None else look\n", "    lk = 0.25 if look is None else look\n    lu = max(0.0, lu - sp.get('kapak_ac', 0.0))\n", 1)
assert "kapak_ac" in _src
_ns = dict(vars(Y))
exec(compile(_src, "yuzler<kafa>", "exec"), _ns)
_kafa_param = _ns["_kafa_param"]

def _yumusak_cene(face, view):
    if view == "front":
        return face.replace("L38,80 C32,85 26,88 18,89 L-18,89 C-26,88 -32,85 -38,80", "C44,76 24,92 0,92 C-24,92 -44,76 -50,64")
    if view == "3q":
        return face.replace("L40,89 L8,91", "C44,84 28,93 14,92 C10,92 9,91 8,91")
    if view == "side":   # kadın profili: yumuşak alın, küçük kalkık burun, dolgun dudak, yuvarlak çene
        return ("M-66,-40 C-70,-98 -26,-116 10,-112 C44,-108 62,-88 62,-50 L63,-26 C66,-14 71,-2 77,9 "
                "C81,15 80,20 74,22 C70,23 70,26 72,30 C75,33 74,37 70,39 C74,43 73,48 68,51 "
                "C68,60 64,70 54,78 C40,86 24,88 4,84 C-20,72 -46,48 -60,20 C-66,6 -68,-14 -66,-40 Z")
    return face
_ns["_yumusak_cene"] = _yumusak_cene

def _kadin_sac(view, hair, arka):
    """Omuza dökülen dalgalı saç, yandan ayrık perçem. arka=True: başın arkasındaki kütle."""
    hd = shade(hair, 0.78); hl = shade(hair, 1.45)
    if arka:
        d = {"front": "M-80,-44 C-110,20 -96,70 -106,110 C-100,150 -70,170 -48,150 C-40,136 -44,124 -40,116 L40,116 C44,124 40,136 48,150 C70,170 100,150 106,110 C96,70 110,20 80,-44 Z",
             "3q": "M-74,-44 C-110,20 -100,70 -110,112 C-104,152 -76,172 -52,154 C-40,142 -44,128 -40,118 C-20,128 0,120 6,100 L-40,-40 Z",
             "side": "M-76,-54 C-114,10 -104,70 -112,116 C-106,156 -76,176 -50,158 C-34,144 -30,126 -34,112 C-22,90 -14,40 -20,-60 Z"}[view]
        dalga = {"front": "M-86,0 C-96,40 -84,70 -96,104 M-70,30 C-78,70 -68,100 -76,140 M86,0 C96,40 84,70 96,104 M70,30 C78,70 68,100 76,140",
                 "3q": "M-82,0 C-94,40 -84,70 -96,106 M-64,30 C-72,70 -62,104 -70,144",
                 "side": "M-84,-10 C-96,40 -86,74 -98,110 M-62,20 C-72,64 -60,100 -66,146"}[view]
        uzak = ('<path d="M58,-70 C98,-10 96,70 84,128 C74,146 58,130 64,100 C70,60 70,0 50,-60 Z" '
                f'fill="{shade(hd,0.85)}" stroke="{INK}" stroke-width="4.5" stroke-linejoin="round"/>') if view == "3q" else ""
        return (uzak + f'<path d="{d}" fill="{hd}" stroke="{INK}" stroke-width="4.5" stroke-linejoin="round"/>'
                f'<path d="{dalga}" stroke="{shade(hd,0.72)}" stroke-width="3" fill="none" opacity="0.8" stroke-linecap="round"/>'
                f'<path d="M-90,-10 C-98,30 -90,60 -98,90" stroke="{hl}" stroke-width="5" fill="none" opacity="0.35" stroke-linecap="round"/>')
    d = {"front": "M-66,-20 C-74,-100 -30,-124 6,-122 C46,-120 72,-98 66,-24 C60,-66 42,-86 16,-92 C0,-74 -28,-62 -58,-56 C-62,-40 -64,-28 -66,-20 Z",
         "3q": "M-62,-16 C-72,-106 -14,-126 22,-122 C62,-118 84,-90 78,-30 C70,-68 54,-88 30,-94 C12,-74 -18,-62 -46,-58 C-54,-44 -58,-28 -62,-16 Z",
         "side": "M-72,10 C-84,-90 -30,-128 14,-122 C50,-116 68,-94 64,-62 C50,-82 30,-90 12,-88 C2,-80 -4,-70 -6,-56 C-8,-40 -14,-20 -24,-6 C-34,4 -54,10 -72,10 Z"}[view]
    side_lock = {"front": "M66,-34 C84,10 80,72 68,116 C62,104 66,44 62,-16 Z",
                 "3q": "", "side": ""}[view]
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
        dud = (f'<ellipse cx="{mx}" cy="{my+6}" rx="{11 if view!="side" else 4}" ry="4.5" fill="{sp.get("dudak","#C77566")}" opacity="0.7"/>'
               + "".join(f'<ellipse cx="{x}" cy="{y}" rx="15" ry="8" fill="#E8907A" opacity="0.22"/>' for x, y in {"front": [(-36, 30), (36, 30)], "3q": [(-6, 30), (58, 28)], "side": [(38, 28)]}[view]))
        kir = "".join(f'<path d="M{x},{y} l{5 if x > 0 and view == "front" else -5},-5 M{x + (-4 if x > 0 and view == "front" else 4)},{y-3} l{3 if x > 0 and view == "front" else -3},-6" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>'
                      for x, y in {"front": [(44, -9), (-44, -9)], "3q": [(-12, -8)], "side": [(38, -8)]}[view])
        body = _kadin_sac(view, sp["hair"], True) + body + dud + kir + _kadin_sac(view, sp["hair"], False)
    if sp.get("yas_cizgi") and view != "side":
        cx = 0 if view == "front" else 30
        body += (f'<path d="M{cx-22},-58 q22,-6 44,0 M{cx-14},-50 q14,-4 28,0" stroke="{sp["skin_dk"]}" stroke-width="2" fill="none" opacity="0.45"/>'
                 f'<path d="M{cx+18 if view=="front" else 54},38 q6,10 4,20" stroke="{sp["skin_dk"]}" stroke-width="2.2" fill="none" opacity="0.4"/>')
    en = sp.get("en", 1.0)
    return f'<g transform="scale({en},1)">{body}</g>' if en != 1.0 else body
