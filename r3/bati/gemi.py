"""Floki'nin gemisi: tek kaynak (R8). Bindirme kaplamalı uzun gemi, ejder başı, kıvrık kıç, kalkan sırası, kürekler,
çizgili kare yelken. built (0–1) inşaat aşaması: omurga + postalar → alttan üste bindirme kaplamalar → küpeşte, kalkan ve direk.
"""
import math, random
INK = "#1A1410"
N = 48

def _x(u): return -540 + 1100 * u
def _K(u): return 70 * math.sin(math.pi * u) ** 0.55              # omurga (orta derin)
def _G(u): return -60 - 150 * abs(2 * u - 1) ** 3.2               # küpeşte (uçlarda yükselir)

def _line(f, u0=0.0, u1=1.0, n=N):
    return [(_x(u0 + (u1 - u0) * k / n), f(u0 + (u1 - u0) * k / n)) for k in range(n + 1)]

def _pts(p): return " ".join(f"{x:.1f},{y:.1f}" for x, y in p)

def dragon_head(x, y, s=1.0, col="#5A4632"):
    """Oyma ejder pruvası v3 (kurul: ağır, tehditkâr, Oseberg/Gokstad): kalın konik boyun bloğu, büyük kafa (alın çıkıntısı, geniş kıvrık burun,
    blok çene, aralık ağızda 4 kalın düzensiz diş, dişlerin üstüne kıvrılan dudak), derin kaş kemeri altında oyma badem göz, kıvrık yele,
    yanlarda örgü oyması, damar + yeşil-gri patina. Dil yok, çizgi film gözü yok."""
    dk = "#2E2216"; hl = "#8A7458"; pat = "#5E6A52"
    o = [f'<g transform="translate({x},{y}) scale({s})">']
    neck = "M-40,170 C-34,40 -30,-90 10,-236 L74,-246 C56,-176 48,-40 46,170 Z"   # gövdeye kadar inen, üste incelen blok
    o.append(f'<path d="{neck}" fill="{col}" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>')
    o.append(f'<path d="{neck}" fill="{pat}" opacity="0.28"/>')
    for k in range(7):   # damar
        o.append(f'<path d="M{-30+k*10},160 C{-22+k*9},-90 {-14+k*10},-170 {16+k*8},-236" stroke="{dk}" stroke-width="2" fill="none" opacity="0.45"/>')
    for k in range(4):   # yan yüzde örgü oyması (iç içe iki şerit)
        yy = -40 - k * 48; xo = 4 + k * 5
        o.append(f'<path d="M{xo-24},{yy} q24,-28 48,0 q-24,28 -48,0 Z" fill="none" stroke="{dk}" stroke-width="5"/>'
                 f'<path d="M{xo-24},{yy-20} q24,28 48,0" fill="none" stroke="{dk}" stroke-width="4"/>')
    for k in range(6):   # arka kenarda kıvrık yele
        yy = -60 - k * 34; xx = -34 + k * 7
        o.append(f'<path d="M{xx},{yy} q-40,-4 -44,-34 q10,14 26,8 q-8,-10 -2,-20 q8,22 26,22 Z" fill="{col}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>')
    o.append('<g transform="translate(40,-250) rotate(-10)">')   # kafa (yukarı dönük)
    o.append(f'<path d="M40,30 L196,22 L186,52 L60,58 Z" fill="#160C06"/>')   # ağız içi
    o.append(f'<path d="M-30,40 Q60,64 200,48 Q214,62 196,82 Q100,96 -20,80 Z" fill="{col}" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>')   # blok alt çene
    o.append(f'<path d="M-30,40 Q60,64 200,48 Q214,62 196,82 Q100,96 -20,80 Z" fill="{pat}" opacity="0.25"/><path d="M-10,72 Q90,82 190,70" stroke="{dk}" stroke-width="3" fill="none"/>')
    for tx, h in ((70, 26), (112, 20), (150, 24), (182, 18)):   # 4 kalın düzensiz diş
        o.append(f'<path d="M{tx},24 l7,{h} l9,-{h+2} Z" fill="#D8CCAE" stroke="{INK}" stroke-width="3"/><path d="M{tx+16},56 l6,-{h-6} l8,{h-8} Z" fill="#D8CCAE" stroke="{INK}" stroke-width="3"/>')
    o.append(f'<path d="M-40,20 Q-44,-46 20,-70 Q70,-88 130,-60 Q190,-50 222,-28 Q246,-10 236,12 Q226,26 200,24 Q190,34 170,28 L40,32 Q0,44 -40,20 Z" fill="{col}" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>')   # kafa
    o.append(f'<path d="M-40,20 Q-44,-46 20,-70 Q70,-88 130,-60 Q190,-50 222,-28 Q246,-10 236,12 Q226,26 200,24 Q190,34 170,28 L40,32 Q0,44 -40,20 Z" fill="{pat}" opacity="0.25"/>')
    o.append(f'<path d="M196,22 Q214,30 210,44 Q196,40 190,30" fill="{col}" stroke="{INK}" stroke-width="5"/>')   # dişlerin üstüne kıvrılan dudak
    o.append(f'<path d="M206,-18 q18,-4 22,10 q-4,12 -18,8" fill="{dk}" stroke="{INK}" stroke-width="3"/>')   # burun deliği
    o.append(f'<path d="M8,-52 Q60,-96 120,-62" stroke="{INK}" stroke-width="16" fill="none" stroke-linecap="round"/><path d="M12,-54 Q60,-92 116,-62" stroke="{hl}" stroke-width="6" fill="none"/>')   # kaş kemeri
    o.append(f'<path d="M30,-40 Q62,-58 96,-42 Q62,-28 30,-40 Z" fill="#120A06" stroke="{INK}" stroke-width="4"/><path d="M50,-42 Q62,-48 76,-42" stroke="#7A6A4A" stroke-width="3" fill="none"/>')   # derin oyma göz
    o.append(f'<path d="M110,-34 Q160,-30 214,-14 M96,-6 Q150,-2 206,6 M-10,0 q20,-26 44,-8 q10,18 -10,22 q-12,-2 -8,-12" stroke="{dk}" stroke-width="4" fill="none"/>')   # oyma çizgiler + yanak sarmalı
    o.append(f'<path d="M-36,-10 Q-60,-60 -40,-104 Q-20,-130 0,-110 Q-16,-104 -18,-86 Q-10,-70 6,-74" fill="none" stroke="{INK}" stroke-width="18" stroke-linecap="round"/>'
             f'<path d="M-36,-10 Q-60,-60 -40,-104 Q-20,-130 0,-110 Q-16,-104 -18,-86 Q-10,-70 6,-74" fill="none" stroke="{col}" stroke-width="9" stroke-linecap="round"/>')   # geriye kıvrık tepe
    o.append(f'<path d="M20,-68 Q80,-88 140,-60" stroke="{hl}" stroke-width="3" fill="none" opacity="0.7"/>')
    o.append('</g></g>'); return "".join(o)

def stern_curl(x, y, s=1.0, col="#7A5232"):
    return (f'<g transform="translate({x},{y}) scale({s})"><path d="M0,0 Q-40,-80 -20,-160 Q0,-220 -60,-230 Q-110,-226 -100,-184 Q-90,-160 -66,-170 Q-60,-196 -78,-196" fill="none" stroke="{INK}" stroke-width="26" stroke-linecap="round"/>'
            f'<path d="M0,0 Q-40,-80 -20,-160 Q0,-220 -60,-230 Q-110,-226 -100,-184 Q-90,-160 -66,-170 Q-60,-196 -78,-196" fill="none" stroke="{col}" stroke-width="15" stroke-linecap="round"/></g>')

STRAKE_C = ["#5A3A20", "#6A4428", "#74502E", "#6A4428", "#7A5634", "#6E4A2A", "#7E5A36"]

def hull(built=1.0, shields=True, oars=True, wet=False):
    """Gövde (merkez 0,0; uzunluk ~1160). built<1: kaplamalar alttan kısmen, postalar açıkta."""
    o = []; ns = 7; nb = int(round(built * ns))
    # postalar (çıplak iskelet; kaplananların arkasında da görünür)
    for k in range(1, 18):
        u = k / 18; x = _x(u)
        o.append(f'<path d="M{x:.0f},{_K(u):.0f} Q{x+6:.0f},{(_K(u)+_G(u))/2:.0f} {x:.0f},{_G(u):.0f}" stroke="{INK}" stroke-width="15" fill="none"/>'
                 f'<path d="M{x:.0f},{_K(u):.0f} Q{x+6:.0f},{(_K(u)+_G(u))/2:.0f} {x:.0f},{_G(u):.0f}" stroke="#9A6A3A" stroke-width="8" fill="none"/>')
    # bindirme kaplama bantları (alttan üste)
    for i in range(nb):
        f0 = lambda u, i=i: _K(u) + (_G(u) - _K(u)) * i / ns
        f1 = lambda u, i=i: _K(u) + (_G(u) - _K(u)) * (i + 1) / ns
        top = _line(f1); bot = _line(f0)[::-1]
        o.append(f'<polygon points="{_pts(top + bot)}" fill="{STRAKE_C[i % 7]}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>')
        sh = _line(lambda u, i=i: f1(u) + 5)
        o.append(f'<polyline points="{_pts(sh)}" fill="none" stroke="#000" stroke-width="5" opacity="0.28"/>')   # bindirme gölgesi
        for k in range(3, N, 4):   # perçin
            x, y = _line(lambda u, i=i: f1(u) + 9)[k]; o.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="2.6" fill="#2A1A10"/>')
        if wet: o.append(f'<polyline points="{_pts(_line(lambda u, i=i: f1(u) + 2))}" fill="none" stroke="#C8DCE8" stroke-width="2" opacity="0.25"/>')
    # omurga ve uç postaları
    o.append(f'<polyline points="{_pts(_line(_K))}" fill="none" stroke="{INK}" stroke-width="22" stroke-linecap="round"/><polyline points="{_pts(_line(_K))}" fill="none" stroke="#4A2E18" stroke-width="13" stroke-linecap="round"/>')
    o.append(f'<path d="M{_x(1):.0f},{_K(1):.0f} Q{_x(1)+60:.0f},-60 {_x(1)+50:.0f},{_G(1)-20:.0f}" stroke="{INK}" stroke-width="46" fill="none"/><path d="M{_x(1):.0f},{_K(1):.0f} Q{_x(1)+60:.0f},-60 {_x(1)+50:.0f},{_G(1)-20:.0f}" stroke="#5A4632" stroke-width="34" fill="none"/>')
    o.append(f'<path d="M{_x(0):.0f},{_K(0):.0f} Q{_x(0)-50:.0f},-60 {_x(0)-40:.0f},{_G(0)-10:.0f}" stroke="{INK}" stroke-width="26" fill="none"/><path d="M{_x(0):.0f},{_K(0):.0f} Q{_x(0)-50:.0f},-60 {_x(0)-40:.0f},{_G(0)-10:.0f}" stroke="#7A5232" stroke-width="16" fill="none"/>')
    o.append(dragon_head(_x(1) + 50, _G(1) - 14, 1.0)); o.append(stern_curl(_x(0) - 40, _G(0) - 6, 1.0))
    if built >= 0.99:   # küpeşte, kürek delikleri, kalkanlar, kürekler
        o.append(f'<polyline points="{_pts(_line(_G))}" fill="none" stroke="{INK}" stroke-width="18"/><polyline points="{_pts(_line(_G))}" fill="none" stroke="#9A6E40" stroke-width="10"/>')
        if oars:
            for k in range(2, 16):
                u = k / 17; x = _x(u); y = _G(u) + 24
                o.append(f'<path d="M{x:.0f},{y:.0f} L{x-70:.0f},{y+210:.0f}" stroke="{INK}" stroke-width="11"/><path d="M{x:.0f},{y:.0f} L{x-70:.0f},{y+210:.0f}" stroke="#B88A52" stroke-width="5"/>'
                         f'<path d="M{x-62:.0f},{y+186:.0f} l-20,40 l12,4 l18,-38 Z" fill="#B88A52" stroke="{INK}" stroke-width="4"/>')
        if shields:
            r = random.Random(3); cols = [("#B8322A", "#E8D8B0"), ("#E8D8B0", "#2E4A5E"), ("#2E4A5E", "#C9A25A"), ("#3A5A34", "#E8D8B0"), ("#C9A25A", "#8A2A22")]
            for k in range(1, 18):
                u = 0.06 + 0.88 * k / 18; x = _x(u); y = _G(u) + 6; c1, c2 = cols[k % 5]
                o.append(f'<g transform="translate({x:.0f},{y:.0f})"><circle r="27" fill="{c1}" stroke="{INK}" stroke-width="5"/>'
                         + (f'<path d="M0,-27 V27 M-27,0 H27" stroke="{c2}" stroke-width="7"/>' if k % 2 else f'<path d="M0,-27 A27,27 0 0,1 0,27 Z" fill="{c2}"/>')
                         + f'<circle r="27" fill="none" stroke="{INK}" stroke-width="5"/><circle r="7" fill="#A8A8A0" stroke="{INK}" stroke-width="3"/></g>')
    return "".join(o)

def mast_sail(billow=1.0, reefed=False):
    o = [f'<path d="M20,-60 L20,-640" stroke="{INK}" stroke-width="26"/><path d="M20,-60 L20,-640" stroke="#6A4428" stroke-width="15"/>',
         f'<path d="M20,-640 L{_x(1)+60:.0f},{_G(1)-60:.0f} M20,-640 L{_x(0)-30:.0f},{_G(0)-30:.0f} M20,-600 L-200,-90 M20,-600 L240,-100" stroke="#3A2A1A" stroke-width="4"/>']
    if reefed:
        o.append(f'<path d="M-250,-560 L290,-560" stroke="{INK}" stroke-width="40" stroke-linecap="round"/><path d="M-250,-560 L290,-560" stroke="#C8B8A0" stroke-width="28" stroke-linecap="round"/>'
                 + "".join(f'<path d="M{x},-576 V-544" stroke="#B8322A" stroke-width="16"/>' for x in range(-220, 280, 70)))
        return "".join(o)
    top = -580; bot = -170; L, R = -270, 310; b = 60 * billow
    stripes = 8; w = (R - L) / stripes
    for k in range(stripes):
        x0 = L + k * w; x1 = x0 + w
        o.append(f'<path d="M{x0:.0f},{top} L{x1:.0f},{top} L{x1 + b*0.4:.0f},{bot + b*(0.6 - abs(k+1-stripes/2)/stripes):.0f} Q{(x0+x1)/2 + b*0.4:.0f},{bot + b:.0f} {x0 + b*0.4:.0f},{bot + b*(0.6 - abs(k-stripes/2)/stripes):.0f} Z" fill="{"#B8322A" if k % 2 == 0 else "#E8DCC0"}"/>')
    o.append(f'<path d="M{L},{top} L{R},{top} L{R + b*0.4:.0f},{bot + b*0.1:.0f} Q{(L+R)/2 + b*0.4:.0f},{bot + b*1.2:.0f} {L + b*0.4:.0f},{bot + b*0.1:.0f} Z" fill="none" stroke="{INK}" stroke-width="8"/>')
    o.append(f'<path d="M{L-30},{top} L{R+30},{top}" stroke="{INK}" stroke-width="20" stroke-linecap="round"/><path d="M{L-30},{top} L{R+30},{top}" stroke="#7A5232" stroke-width="11" stroke-linecap="round"/>')
    o.append(f'<path d="M{L+40},{top+40} Q{(L+R)/2},{top+60} {R-40},{top+40}" stroke="#000" stroke-width="10" fill="none" opacity="0.12"/>')
    return "".join(o)

def longship(x, y, s=1.0, sail=True, billow=1.0, reefed=False, built=1.0, oars=True, shields=True, wet=False):
    return (f'<g transform="translate({x},{y}) scale({s})">' + (mast_sail(billow, reefed) if (sail and built >= 0.99) else "")
            + hull(built, shields, oars, wet) + '</g>')

def scaffold(x, y, s=1.0):
    """İnşaat iskelesi: sehpalar, payandalar, iskele tahtası, kalas yığını, katran kazanı, aletler, ip."""
    o = [f'<g transform="translate({x},{y}) scale({s})">']
    for xx in (-420, -150, 120, 390):   # gövde altı sehpalar + yan payandalar
        o.append(f'<path d="M{xx-60},170 L{xx},70 L{xx+60},170" stroke="{INK}" stroke-width="18" fill="none"/><path d="M{xx-60},170 L{xx},70 L{xx+60},170" stroke="#5A3A20" stroke-width="10" fill="none"/>')
        o.append(f'<path d="M{xx+20},-20 L{xx+120},170" stroke="{INK}" stroke-width="14"/><path d="M{xx+20},-20 L{xx+120},170" stroke="#6A4428" stroke-width="7"/>')
    o.append(f'<path d="M-560,-130 L560,-130" stroke="{INK}" stroke-width="10"/>')   # iskele ipi
    o.append(f'<rect x="-640" y="-10" width="20" height="180" fill="#5A3A20" stroke="{INK}" stroke-width="5"/><rect x="620" y="-60" width="20" height="230" fill="#5A3A20" stroke="{INK}" stroke-width="5"/>')
    for k in range(5):   # kalas yığını
        o.append(f'<rect x="{-760+k*6}" y="{140-k*16}" width="300" height="16" rx="4" fill="{STRAKE_C[k]}" stroke="{INK}" stroke-width="4"/>')
    o.append(f'<g transform="translate(620,140)"><path d="M-40,0 Q-46,-60 0,-64 Q46,-60 40,0 Z" fill="#2A2420" stroke="{INK}" stroke-width="6"/>'
             f'<path d="M-50,26 L-30,-6 M50,26 L30,-6" stroke="{INK}" stroke-width="8"/><path d="M-36,22 Q0,-10 36,22" fill="#E8742A" stroke="{INK}" stroke-width="3"/>'
             f'<path d="M-6,-66 q-14,-30 6,-50 q16,-20 0,-44" stroke="#9A9A9A" stroke-width="6" fill="none" opacity="0.6"/></g>')   # katran kazanı
    for (xx, yy, rot) in ((-380, 150, -20), (-300, 160, 30)):   # keser ve burgu
        o.append(f'<g transform="translate({xx},{yy}) rotate({rot})"><rect x="-6" y="-70" width="12" height="80" fill="#5A3A20" stroke="{INK}" stroke-width="4"/><path d="M-6,-70 Q-40,-80 -36,-48 L-6,-52 Z" fill="#A8B0B8" stroke="{INK}" stroke-width="4"/></g>')
    r = random.Random(4)
    for k in range(70): o.append(f'<path d="M{r.uniform(-700,700):.0f},{r.uniform(150,200):.0f} q8,-8 18,0" stroke="#D8B884" stroke-width="4" fill="none"/>')   # talaş
    o.append('</g>'); return "".join(o)
