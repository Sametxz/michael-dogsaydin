"""Prosedürel doku kütüphanesi (SVG filtreleri, rsvg destekli).

Kullanım: svg parçasının başına `defs()` eklenir, şekle filter="url(#t_yun)" verilir.
Her doku kendi kaynağının rengini korur, üstüne yapı (lif, damar, taş) ekler.
"""

def _mul(fid, turb, extra=""):
    # gürültüyü alfa maskesine çevirip kaynağı çarparak doku katar
    return (f'<filter id="{fid}" x="-5%" y="-5%" width="110%" height="110%" color-interpolation-filters="sRGB">'
            f'{turb}<feColorMatrix in="n" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -1.4 1.15" result="a"/>'
            f'<feComposite in="SourceGraphic" in2="a" operator="in" result="t"/><feBlend in="SourceGraphic" in2="t" mode="multiply" result="b"/>'
            f'<feComposite in="b" in2="SourceGraphic" operator="in"/>{extra}</filter>')

def _lit(fid, freq, oct_, seed, scale, light="#E8E2D6", az=225, el=50):
    # kabartmalı (yönlü ışıklı) doku: taş, ahşap, deri
    return (f'<filter id="{fid}" x="-5%" y="-5%" width="110%" height="110%" color-interpolation-filters="sRGB">'
            f'<feTurbulence type="fractalNoise" baseFrequency="{freq}" numOctaves="{oct_}" seed="{seed}" result="n"/>'
            f'<feDiffuseLighting in="n" lighting-color="{light}" surfaceScale="{scale}" result="l"><feDistantLight azimuth="{az}" elevation="{el}"/></feDiffuseLighting>'
            f'<feBlend in="SourceGraphic" in2="l" mode="multiply" result="b"/><feComposite in="b" in2="SourceGraphic" operator="in"/></filter>')

TEX = {
    "yun":   _mul("t_yun", '<feTurbulence type="fractalNoise" baseFrequency="0.55 0.18" numOctaves="3" seed="4" result="n"/>'),
    "orgu":  _mul("t_orgu", '<feTurbulence type="turbulence" baseFrequency="0.22 0.5" numOctaves="2" seed="7" result="n"/>'),
    "keten": _mul("t_keten", '<feTurbulence type="fractalNoise" baseFrequency="0.9 0.9" numOctaves="2" seed="3" result="n"/>'),
    "deri":  _lit("t_deri", "0.08", 4, 5, 1.4, "#EDE4D6"),
    "ahsap": _lit("t_ahsap", "0.012 0.22", 4, 9, 2.2, "#EEE2CE", az=200, el=55),
    "tas":   _lit("t_tas", "0.035", 5, 2, 3.0, "#E2DCD0"),
    "kurk":  _mul("t_kurk", '<feTurbulence type="fractalNoise" baseFrequency="0.08 0.6" numOctaves="4" seed="11" result="n"/>'),
    "cilt":  _mul("t_cilt", '<feTurbulence type="fractalNoise" baseFrequency="1.2" numOctaves="1" seed="21" result="n"/>'),
    "metal": _lit("t_metal", "0.02 0.3", 2, 13, 1.2, "#FFF4D8", az=240, el=60),
    "sakal": _mul("t_sakal", '<feTurbulence type="fractalNoise" baseFrequency="0.05 0.9" numOctaves="3" seed="17" result="n"/>'),
}

def defs(*names):
    names = names or tuple(TEX)
    return "<defs>" + "".join(TEX[n] for n in names) + "</defs>"

def f(name):
    return f'filter="url(#t_{name})"'

# ---- v1.1 (kurul nesne kartı v1 düzeltmeleri) ----
import re as _re
def scaled(name, s):
    """Ölçekten bağımsız doku: nesne ekranda s kat büyütülecekse baseFrequency/s (G2 #1)."""
    src = TEX[name]; fid = f"t_{name}_s{int(round(s*100))}"
    def fx(m):
        vals = " ".join(f"{float(v)/s:.4f}" for v in m.group(1).split())
        return f'baseFrequency="{vals}"'
    return _re.sub(r'baseFrequency="([^"]+)"', fx, src).replace(f'id="t_{name}"', f'id="{fid}"'), fid

def form(fid="t_form", blur=18, scale=9, az=225, el=55, gain=1.12):
    """Hacim (yastık) gölgesi: alfa maskesinden yönlü ışık. Düz dolguyu yuvarlaklaştırır (G2 #2)."""
    return (f'<filter id="{fid}" x="-5%" y="-5%" width="110%" height="110%" color-interpolation-filters="sRGB">'
            f'<feGaussianBlur in="SourceAlpha" stdDeviation="{blur}" result="b"/>'
            f'<feDiffuseLighting in="b" lighting-color="#FFFFFF" surfaceScale="{scale}" result="l"><feDistantLight azimuth="{az}" elevation="{el}"/></feDiffuseLighting>'
            f'<feComponentTransfer in="l" result="l2"><feFuncR type="linear" slope="{gain}"/><feFuncG type="linear" slope="{gain}"/><feFuncB type="linear" slope="{gain*1.03:.3f}"/></feComponentTransfer>'
            f'<feBlend in="SourceGraphic" in2="l2" mode="multiply" result="m"/><feComposite in="m" in2="SourceGraphic" operator="in"/></filter>')

def knit_pattern(pid="p_knit", col="#000000", a=0.22, w=14, h=12, rot=-18, s=1.0):
    """Örgü ilmek sıraları (V darbeleri) — gürültü yerine geometri (G2 #3)."""
    return (f'<pattern id="{pid}" width="{w}" height="{h}" patternUnits="userSpaceOnUse" patternTransform="rotate({rot}) scale({s})">'
            f'<path d="M1,1 L{w/2},{h-2} L{w-1},1" fill="none" stroke="{col}" stroke-opacity="{a}" stroke-width="2.2" stroke-linecap="round"/>'
            f'<path d="M3,0 L{w/2},{h-5}" fill="none" stroke="#FFFFFF" stroke-opacity="{a*0.45:.3f}" stroke-width="1.2"/></pattern>')
