"""Ivar sahnesi v2 · mekân ve nesne kartları (hero_v4 çıtası).

Mekânlar 1920x1080 kare koordinatında çizilir. Her mekânda en az 3 kimlik öğesi bulunur (§9).
- longhouse(): gece, ocak ışığında Viking uzun evi. Kimlik öğeleri: taş çevreli ocak, oymalı
  direkler, çatı kirişleri, duvardaki kalkanlar, kürklü yatak sekisi, kapı.
- riverbank(): şafakta sisli nehir kıyısı. Kimlik öğeleri: akan su, sazlık, çakıl ve taşlar,
  kuru ağaç, karşı kıyıdaki orman, sis.
- seax(): Ragnar'ın bıçağı. Oluklu tek ağızlı ağız, kemik sap, deri sargı, pirinç bilezik.
"""
import sys, math, random, subprocess
sys.path[:0] = ["/home/claude/r3", "/home/claude/r2"]
import tex
from art3 import knot_mark
INK = "#1A1410"
R = random.Random
W, H = 1920, 1080


def _defs():
    return ("<defs>" + tex.TEX["ahsap"] + tex.TEX["tas"] + tex.TEX["kurk"] + tex.TEX["metal"] + tex.TEX["deri"]
            + tex.scaled("ahsap", 0.5)[0] + tex.scaled("tas", 0.6)[0]
            + '<radialGradient id="fire" cx="0.5" cy="0.62" r="0.6"><stop offset="0" stop-color="#FFB25A" stop-opacity="0.85"/><stop offset="0.35" stop-color="#E0702A" stop-opacity="0.45"/><stop offset="1" stop-color="#2A1408" stop-opacity="0"/></radialGradient>'
            + '<linearGradient id="smoke" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5A4A40" stop-opacity="0.55"/><stop offset="1" stop-color="#5A4A40" stop-opacity="0"/></linearGradient>'
            + '<linearGradient id="floor" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2A2016"/><stop offset="1" stop-color="#4A3A2A"/></linearGradient>'
            + '<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8FA4B8"/><stop offset="1" stop-color="#C8D4DE"/></linearGradient>'
            + '<linearGradient id="water" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9AAEC0"/><stop offset="1" stop-color="#4E6478"/></linearGradient>'
            + '<linearGradient id="blade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#E6ECF0"/><stop offset="0.45" stop-color="#A8B4BE"/><stop offset="1" stop-color="#5E6A74"/></linearGradient>'
            + "</defs>")


# ------------------------------------------------------------------ uzun ev (gece)
VP = (980, 470)   # kaçış noktası

def _post(x, y0, y1, w, k):
    """Oymalı direk: ahşap damar, düğüm oyması, taban taşı, gölge yüzü."""
    o = [f'<g filter="url(#t_ahsap)"><rect x="{x-w/2}" y="{y0}" width="{w}" height="{y1-y0}" fill="#5A4430"/></g>',
         f'<rect x="{x+w*0.12}" y="{y0}" width="{w*0.38}" height="{y1-y0}" fill="#1E140C" opacity="0.45"/>',
         f'<rect x="{x-w/2}" y="{y0}" width="{w}" height="{y1-y0}" fill="none" stroke="{INK}" stroke-width="{max(3, w*0.08):.1f}"/>']
    for j in range(3):  # oyma bantları
        yy = y0 + (y1 - y0) * (0.25 + j * 0.22)
        o.append(f'<path d="M{x-w*0.4},{yy} q{w*0.2},{-w*0.25} {w*0.4},0 q{w*0.2},{w*0.25} {w*0.4},0" stroke="#2A1C10" stroke-width="{max(2, w*0.06):.1f}" fill="none"/>')
    o.append(f'<ellipse cx="{x}" cy="{y1}" rx="{w*0.75}" ry="{w*0.22}" fill="#4A4440" stroke="{INK}" stroke-width="3"/>')
    return "".join(o)

def _shield(x, y, r, c1, c2):
    o = [f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c1}" stroke="{INK}" stroke-width="5"/>']
    for a in range(0, 360, 90):
        o.append(f'<path d="M{x},{y} L{x+r*math.cos(math.radians(a)):.0f},{y+r*math.sin(math.radians(a)):.0f} A{r},{r} 0 0 1 {x+r*math.cos(math.radians(a+45)):.0f},{y+r*math.sin(math.radians(a+45)):.0f} Z" fill="{c2}"/>')
    o.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="#6A6A6A" stroke-width="{r*0.12:.0f}"/><circle cx="{x}" cy="{y}" r="{r*0.22:.0f}" fill="#8A8A86" stroke="{INK}" stroke-width="3" filter="url(#t_metal)"/>')
    return "".join(o)

def longhouse(fire=1.0):
    o = [_defs(), f'<rect width="{W}" height="{H}" fill="#140E0A"/>']
    # arka duvar (dikey tahtalar) + kapı
    bx0, bx1, by0, by1 = 640, 1320, 300, 640
    o.append(f'<g filter="url(#t_ahsap_s50)">' + "".join(f'<rect x="{x}" y="{by0}" width="34" height="{by1-by0}" fill="{["#3A2C1E","#34271A","#402F20"][i%3]}"/>' for i, x in enumerate(range(bx0, bx1, 34))) + '</g>')
    o.append(f'<rect x="{bx0}" y="{by0}" width="{bx1-bx0}" height="{by1-by0}" fill="none" stroke="{INK}" stroke-width="4"/>')
    o.append(f'<path d="M1110,640 L1110,430 Q1150,396 1190,430 L1190,640 Z" fill="#22344E" stroke="{INK}" stroke-width="6"/>'   # kapı aralığı: dışarıda gece mavisi
             f'<path d="M1124,640 L1124,440 Q1150,418 1176,440 L1176,640" fill="none" stroke="#3A5A7E" stroke-width="3" opacity="0.6"/>')
    # yan duvarlar (perspektif tahta şeritleri)
    for side in (-1, 1):
        xe = 0 if side < 0 else W; xb = bx0 if side < 0 else bx1
        o.append(f'<path d="M{xe},120 L{xb},{by0} L{xb},{by1} L{xe},{H} Z" fill="#2C2117"/>')
        for k in range(1, 9):
            t_ = k / 9; x = xe + (xb - xe) * t_
            o.append(f'<path d="M{x:.0f},{120+(by0-120)*t_:.0f} L{x:.0f},{H+(by1-H)*t_:.0f}" stroke="#1A120C" stroke-width="{6-4*t_:.1f}"/>')
        o.append(f'<g filter="url(#t_ahsap)"><path d="M{xe},120 L{xb},{by0} L{xb},{by1} L{xe},{H} Z" fill="#3A2C1E" opacity="0.35"/></g>')
    # zemin (sıkıştırılmış toprak + saman)
    o.append(f'<path d="M0,{H} L{bx0},{by1} L{bx1},{by1} L{W},{H} Z" fill="url(#floor)"/>')
    o.append("".join(f'<path d="M{x:.0f},{y:.0f} l{R(k).uniform(-14,14):.0f},{R(k+1).uniform(-3,3):.0f}" stroke="#7A6440" stroke-width="2" opacity="0.5"/>' for k, (x, y) in enumerate([(R(k).uniform(200, 1700), R(k + 7).uniform(700, 1060)) for k in range(140)])))
    # çatı: karanlık + kirişler (kaçış noktasına)
    o.append(f'<path d="M0,0 L{W},0 L{W},120 L{bx1},{by0} L{bx0},{by0} L0,120 Z" fill="#0E0A07"/>')
    for k in range(-5, 6):
        x0 = 980 + k * 260
        o.append(f'<path d="M{x0},0 L{980 + k*44},{by0}" stroke="#2A1E14" stroke-width="{22 - abs(k)*1.2:.0f}" stroke-linecap="round"/>'
                 f'<path d="M{x0},0 L{980 + k*44},{by0}" stroke="#4A3826" stroke-width="5" opacity="0.6"/>')
    for j, y in enumerate((60, 170, 250)):   # enine kirişler
        t_ = y / by0; xa = 0 + (bx0) * t_; xb_ = W + (bx1 - W) * t_
        o.append(f'<rect x="{xa:.0f}" y="{y}" width="{xb_-xa:.0f}" height="{26-j*6}" fill="#3A2A1C" stroke="{INK}" stroke-width="4"/>')
    # duvar kalkanları (sol duvar) + asılı balta/av
    o.append(_shield(250, 430, 70, "#7A2A22", "#C8B080") + _shield(430, 450, 54, "#2A4A6A", "#C8B080") + _shield(540, 470, 40, "#5A5A2A", "#D0C090"))
    o.append(f'<path d="M1540,380 l60,-40 M1600,340 q20,30 -6,50 q-20,-10 6,-50" stroke="{INK}" stroke-width="7" fill="#8A8A86"/>')
    # kürklü yatak sekisi: sağ duvar boyunca, perspektifte (üst yüz + ön yüz)
    top = "M1350,592 L1920,772 L1920,866 L1286,652 Z"; front = "M1286,652 L1920,866 L1920,968 L1286,722 Z"
    o.append(f'<g filter="url(#t_ahsap)"><path d="{front}" fill="#3E2E20"/></g><path d="{front}" fill="none" stroke="{INK}" stroke-width="6"/>')
    o.append(f'<g filter="url(#t_kurk)"><path d="M1340,580 Q1500,600 1930,750 L1930,880 Q1560,760 1276,664 Q1290,620 1340,580 Z" fill="#8A7A62"/></g>'
             f'<path d="M1340,580 Q1500,600 1930,750 L1930,880 Q1560,760 1276,664 Q1290,620 1340,580 Z" fill="none" stroke="{INK}" stroke-width="5"/>')
    o.append("".join(f'<path d="M{1300+k*44},{664+k*15} q10,16 0,30" stroke="#5A4A38" stroke-width="4" fill="none"/>' for k, _ in enumerate(range(14))))
    # direkler: ön çift büyük, arka çift küçük (perspektif)
    for (x, y0, y1, w) in ((300, 0, 1080, 70), (1640, 0, 1080, 70), (560, 140, 770, 40), (1400, 140, 770, 40), (760, 250, 660, 24), (1200, 250, 660, 24)):
        o.append(_post(x, y0, y1, w, 0))
    # ocak: taş halka + kütükler + ateş (zeminde, merkez-alt)
    hx, hy = 960, 860
    o.append(f'<ellipse cx="{hx}" cy="{hy}" rx="250" ry="70" fill="#1A120C"/>')
    for k in range(18):
        a = k / 18 * 2 * math.pi; x = hx + 250 * math.cos(a); y = hy + 70 * math.sin(a)
        rr = R(k + 3); rx_ = rr.uniform(26, 36) * (0.75 + 0.25 * math.sin(a)); ry_ = rx_ * 0.6
        o.append(f'<g filter="url(#t_tas_s60)"><ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{rx_:.0f}" ry="{ry_:.0f}" fill="#6A625A"/></g>'
                 f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{rx_:.0f}" ry="{ry_:.0f}" fill="none" stroke="{INK}" stroke-width="4"/>'
                 f'<path d="M{x-rx_*0.6:.0f},{y-ry_*0.5:.0f} q{rx_*0.6:.0f},{-ry_*0.6:.0f} {rx_*1.2:.0f},0" stroke="#E0A060" stroke-width="3" fill="none" opacity="{0.25+0.5*max(0,-math.sin(a)):.2f}"/>')
    o.append(f'<path d="M{hx-150},{hy+10} L{hx+140},{hy-20}" stroke="#2A1A10" stroke-width="30" stroke-linecap="round"/><path d="M{hx-120},{hy-24} L{hx+150},{hy+16}" stroke="#3A2414" stroke-width="26" stroke-linecap="round"/>')
    o.append(f'<path d="M{hx-130},{hy+6} L{hx+120},{hy-18}" stroke="#E06A24" stroke-width="6" opacity="0.8" stroke-linecap="round"/>')
    if fire:
        o.append(f'<ellipse cx="{hx}" cy="{hy-120}" rx="{520*fire:.0f}" ry="{360*fire:.0f}" fill="url(#fire)"/>')
        for k in range(5):  # alevler
            x = hx - 90 + k * 45; hgt = 90 + 50 * math.sin(k * 1.7)
            o.append(f'<path d="M{x-26},{hy-6} Q{x-30},{hy-hgt*0.6:.0f} {x+4},{hy-hgt:.0f} Q{x+8},{hy-hgt*0.55:.0f} {x+28},{hy-6} Z" fill="#F08A2A" opacity="0.9"/>'
                     f'<path d="M{x-12},{hy-6} Q{x-12},{hy-hgt*0.4:.0f} {x+4},{hy-hgt*0.66:.0f} Q{x+6},{hy-hgt*0.35:.0f} {x+14},{hy-6} Z" fill="#FFD27A"/>')
        o.append(f'<path d="M{hx-80},{hy-160} Q{hx-20},{hy-420} {hx+40},{hy-560} L{hx+160},{hy-560} Q{hx+60},{hy-400} {hx+80},{hy-160} Z" fill="url(#smoke)"/>')
    o.append(f'<defs><radialGradient id="night" cx="{hx/W:.2f}" cy="{(hy-80)/H:.2f}" r="0.75"><stop offset="0.15" stop-color="#05030A" stop-opacity="0"/><stop offset="0.7" stop-color="#05030A" stop-opacity="0.55"/><stop offset="1" stop-color="#05030A" stop-opacity="0.85"/></radialGradient></defs>'
             f'<rect width="{W}" height="{H}" fill="url(#night)"/>')
    return "".join(o)


# ------------------------------------------------------------------ nehir kıyısı (şafak)
def riverbank():
    o = [_defs(), f'<rect width="{W}" height="{H}" fill="url(#sky)"/>']
    # uzak orman (3 katman, sise gömülü, sırtlara oturan)
    for layer, (y, col_, hgt, n) in enumerate(((430, "#8296A8", 170, 34), (470, "#6A7E90", 220, 26), (510, "#52667A", 260, 18))):
        o.append(f'<path d="M0,{y} Q480,{y-30} 960,{y-10} Q1440,{y+10} 1920,{y-20} L1920,{y+80} L0,{y+80} Z" fill="{col_}"/>')
        for k in range(n):
            rr = R(layer * 100 + k); x = rr.uniform(0, W); hh = rr.uniform(0.6, 1.0) * hgt; ww = 6 + layer * 4
            o.append(f'<path d="M{x:.0f},{y+20} L{x:.0f},{y-hh:.0f}" stroke="{col_}" stroke-width="{ww}" stroke-linecap="round"/>')
            for b in range(3):
                by = y - hh * (0.45 + b * 0.16); s_ = 1 if (k + b) % 2 else -1
                o.append(f'<path d="M{x:.0f},{by:.0f} l{s_*hh*0.16:.0f},{-hh*0.12:.0f}" stroke="{col_}" stroke-width="{ww*0.5:.0f}" stroke-linecap="round"/>')
        o.append(f'<rect x="0" y="{y-hgt}" width="{W}" height="{hgt+80}" fill="#C8D4DE" opacity="{0.28 - layer*0.06:.2f}"/>')
    # nehir: akan su + yansıma + akıntı çizgileri + karşı kıyı çakılları
    o.append(f'<path d="M0,560 Q600,540 1100,556 Q1500,568 1920,548 L1920,720 Q1300,760 700,740 Q300,730 0,760 Z" fill="url(#water)"/>')
    o.append("".join(f'<path d="M{x:.0f},{y:.0f} q{R(k).uniform(30,70):.0f},-4 {R(k+5).uniform(80,180):.0f},0" stroke="#E2EAF0" stroke-width="{R(k+2).uniform(2,4):.1f}" fill="none" opacity="0.65" stroke-linecap="round"/>'
                      for k, (x, y) in enumerate([(R(k).uniform(-50, 1900), R(k + 11).uniform(572, 735)) for k in range(46)])))
    o.append(f'<path d="M0,560 Q600,540 1100,556 Q1500,568 1920,548" stroke="#3E4C58" stroke-width="10" fill="none"/>')
    # ön kıyı: çamurlu toprak, çakıl, taşlar, sazlık, kuru ağaç
    o.append(f'<path d="M0,770 Q300,730 700,750 Q1300,780 1920,730 L1920,{H} L0,{H} Z" fill="#4A4A40"/>')
    o.append(f'<g filter="url(#t_tas_s60)"><path d="M0,770 Q300,730 700,750 Q1300,780 1920,730 L1920,{H} L0,{H} Z" fill="#5A5A50" opacity="0.6"/></g>')
    o.append(f'<path d="M0,770 Q300,730 700,750 Q1300,780 1920,730" stroke="#2E3430" stroke-width="12" fill="none"/>'
             f'<path d="M0,786 Q300,746 700,766 Q1300,796 1920,746" stroke="#7A8A8A" stroke-width="4" fill="none" opacity="0.6"/>')   # ıslak kenar parlaklığı
    for k in range(60):   # çakıllar
        rr = R(k + 900); x = rr.uniform(0, W); y = rr.uniform(800, 1060); r = rr.uniform(6, 18) * (0.6 + (y - 780) / 500)
        o.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r:.0f}" ry="{r*0.6:.0f}" fill="{["#6E706A","#7E7E76","#5E605A"][k%3]}" stroke="{INK}" stroke-width="2.5"/>')
    for (x, y, r) in ((240, 900, 70), (1720, 940, 90), (1460, 1010, 50)):   # büyük taşlar
        o.append(f'<g filter="url(#t_tas)"><ellipse cx="{x}" cy="{y}" rx="{r*1.3:.0f}" ry="{r*0.7:.0f}" fill="#62686E"/></g>'
                 f'<ellipse cx="{x}" cy="{y}" rx="{r*1.3:.0f}" ry="{r*0.7:.0f}" fill="none" stroke="{INK}" stroke-width="6"/>'
                 f'<path d="M{x-r},{y-r*0.3:.0f} Q{x},{y-r*0.75:.0f} {x+r},{y-r*0.35:.0f}" stroke="#A6B2BE" stroke-width="5" fill="none" opacity="0.7"/>'
                 f'<path d="M{x-r*1.2:.0f},{y+r*0.3:.0f} Q{x},{y+r*0.75:.0f} {x+r*1.2:.0f},{y+r*0.3:.0f}" stroke="#3E5A3A" stroke-width="8" fill="none" opacity="0.65"/>')
    for k in range(40):   # sazlık (sol ve sağ uçta)
        rr = R(k + 300); x = rr.uniform(0, 380) if k < 24 else rr.uniform(1560, 1920); y = rr.uniform(740, 800); hh = rr.uniform(80, 170); bend = rr.uniform(-30, 30)
        o.append(f'<path d="M{x:.0f},{y:.0f} q{bend*0.3:.0f},{-hh*0.5:.0f} {bend:.0f},{-hh:.0f}" stroke="#6A7050" stroke-width="{rr.uniform(3,6):.1f}" fill="none" stroke-linecap="round"/>')
        if k % 4 == 0: o.append(f'<ellipse cx="{x+bend:.0f}" cy="{y-hh:.0f}" rx="5" ry="14" fill="#5A4A34" transform="rotate({bend*0.6:.0f} {x+bend:.0f} {y-hh:.0f})"/>')
    # kuru ağaç (sol, kıyıda): gövde + çatallı dallar
    o.append(f'<g filter="url(#t_ahsap)"><path d="M110,800 Q130,600 100,420 Q90,300 140,180 L170,190 Q130,320 150,430 Q180,610 170,800 Z" fill="#3A3430"/></g>'
             f'<path d="M110,800 Q130,600 100,420 Q90,300 140,180 L170,190 Q130,320 150,430 Q180,610 170,800 Z" fill="none" stroke="{INK}" stroke-width="7"/>'
             f'<path d="M120,420 Q220,360 300,250 M140,300 Q60,230 30,140 M150,520 Q260,500 330,440 M128,240 Q190,160 250,120" stroke="#3A3430" stroke-width="14" fill="none" stroke-linecap="round"/>'
             f'<path d="M120,420 Q220,360 300,250 M140,300 Q60,230 30,140 M150,520 Q260,500 330,440 M128,240 Q190,160 250,120" stroke="{INK}" stroke-width="3" fill="none" stroke-linecap="round" opacity="0.6"/>')
    # alçak sis şeritleri (nehrin üstünde)
    o.append("".join(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="26" fill="#E6ECF0" opacity="0.32"/>' for (x, y, rx) in ((400, 600, 420), (1200, 620, 520), (1700, 590, 300), (800, 700, 380))))
    return "".join(o)


# ------------------------------------------------------------------ bıçak (seax)
def seax():
    """Yerel: sap kökü (0,0), ağız +x yönünde, uç ≈ (520,-10)."""
    o = [f'<path d="M0,-26 L380,-30 Q470,-26 524,-8 Q470,8 380,14 L0,16 Z" fill="url(#blade)" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>',
         f'<path d="M30,-12 L360,-14" stroke="#6A7680" stroke-width="5"/><path d="M30,-17 L360,-19" stroke="#F4F8FA" stroke-width="2" opacity="0.8"/>',   # oluk
         f'<path d="M380,-30 Q470,-26 524,-8" stroke="#FFFFFF" stroke-width="3" fill="none" opacity="0.8"/>',                                         # sırt ışığı
         f'<rect x="-24" y="-32" width="24" height="52" rx="5" fill="#B08A3A" stroke="{INK}" stroke-width="5" filter="url(#t_metal)"/>',                   # pirinç bilezik
         f'<path d="M-24,-22 L-170,-26 Q-196,-6 -170,14 L-24,12 Z" fill="#E2D6BC" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>']               # kemik sap
    for k in range(6):  # deri sargı
        x = -40 - k * 22
        o.append(f'<path d="M{x},-23 L{x-12},12" stroke="#5A3A22" stroke-width="10"/><path d="M{x},-23 L{x-12},12" stroke="{INK}" stroke-width="2" opacity="0.6"/>')
    o.append(f'<circle cx="-182" cy="-6" r="12" fill="#B08A3A" stroke="{INK}" stroke-width="4"/>')   # topuz
    return "".join(o)


def card(out="/home/claude/r3/ivar2/mekan_karti_v1.png"):
    CW, CH = 2400, 1700
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{CW}" height="{CH}">{_defs()}<rect width="{CW}" height="{CH}" fill="#EDE2CC"/>',
         '<text x="40" y="70" font-family="Pirata One" font-size="56" fill="#2A1D14">Ivar sahnesi · mekân ve nesne kartı v1 (uzun ev gece, nehir kıyısı şafak, seax)</text>']
    lab = lambda x, y, t: f'<text x="{x}" y="{y}" font-family="Alegreya SC" font-size="26" fill="#2A1D14">{t}</text>'
    o.append('<defs><clipPath id="cp"><rect width="1920" height="1080"/></clipPath></defs>')
    o.append(f'<g transform="translate(40,100) scale(0.6)"><g clip-path="url(#cp)">{longhouse()}</g></g>' + lab(40, 780, "uzun ev · ocak, oymalı direkler, kirişler, kalkanlar, kürklü seki, kapı aralığı"))
    o.append(f'<g transform="translate(1210,100) scale(0.6)"><g clip-path="url(#cp)">{riverbank()}</g></g>' + lab(1210, 780, "nehir kıyısı · akan su, sis, sazlık, çakıl/taş, kuru ağaç, katmanlı orman"))
    o.append(f'<g transform="translate(400,1060) scale(1.6)">{seax()}</g>' + lab(140, 1180, "seax · oluklu ağız, pirinç bilezik, deri sargı, kemik sap (1,6×)"))
    o.append(f'<g transform="translate(1500,1060) scale(0.5)">{seax()}</g>' + lab(1300, 1130, "kare ölçeği (0,5×)"))
    o.append('</svg>')
    open("/home/claude/r3/ivar2/mekan_karti.svg", "w").write("".join(o))
    subprocess.run(["rsvg-convert", "/home/claude/r3/ivar2/mekan_karti.svg", "-w", str(CW), "-o", out], check=True)


if __name__ == "__main__":
    card(); print("ok")
