"""Sahne 7 v2 mekânları: büyük salon (hükümdar koltuğu), Kattegat dış mekân (sabah), eşek arabası.
Kimlik öğeleri — salon: kürsü üstünde oymalı yüksek koltuk, sancaklar, kalkan dizisi, uzun ocak, mangallar, direkler.
Kattegat: çimen damlı evler, iskele ve fiyort, çit, çamurlu yol, duman. Araba: tahta tekerlek, sandıklar, eşek ve koşum.
"""
import sys, math, random
sys.path[:0] = ["/home/claude/r3", "/home/claude/r2", "/home/claude/r3/ivar2"]
import places as P
import tex
INK = "#1A1410"; W, H = 1920, 1080; R = random.Random

def high_seat(x, y, s=1.0):
    return (f'<g transform="translate({x},{y}) scale({s})">'
            f'<path d="M-260,0 L-240,-70 L240,-70 L260,0 Z" fill="#3A2C1E" stroke="{INK}" stroke-width="8"/>'                        # kürsü
            f'<path d="M-250,-70 L-230,-120 L230,-120 L250,-70 Z" fill="#4A3826" stroke="{INK}" stroke-width="7"/>'
            f'<g filter="url(#t_ahsap)"><path d="M-150,-120 L-150,-470 Q0,-560 150,-470 L150,-120 Z" fill="#5A4430"/></g>'
            f'<path d="M-150,-120 L-150,-470 Q0,-560 150,-470 L150,-120 Z" fill="none" stroke="{INK}" stroke-width="8"/>'
            f'<path d="M-110,-150 L-110,-440 Q0,-500 110,-440 L110,-150 Z" fill="#6E2A22" stroke="{INK}" stroke-width="5"/>'             # kırmızı arka
            + "".join(f'<path d="M-100,{-200-k*70} q100,-30 200,0" stroke="#C9A25A" stroke-width="5" fill="none" opacity="0.8"/>' for k in range(4))
            + "".join(f'<rect x="{sx-26}" y="-560" width="52" height="450" fill="#5A4430" stroke="{INK}" stroke-width="7"/>'
                      f'<path d="M{sx},-556 q{36*g},-70 {8*g},-110 q{-30*g},-20 {-44*g},12 q{24*g},8 {20*g},30" fill="#5A4430" stroke="{INK}" stroke-width="7"/>'
                      f'<circle cx="{sx+8*g}" cy="-640" r="7" fill="#C9A25A" stroke="{INK}" stroke-width="3"/>' for sx, g in ((-176, -1), (176, 1)))
            + f'<g filter="url(#t_kurk)"><path d="M-140,-240 Q0,-280 140,-240 L150,-160 Q0,-140 -150,-160 Z" fill="#C8BCA6"/></g>'
            f'<path d="M-140,-240 Q0,-280 140,-240 L150,-160 Q0,-140 -150,-160 Z" fill="none" stroke="{INK}" stroke-width="6"/></g>')

def banner(x, y, h, c1, c2):
    return (f'<path d="M{x-40},{y} L{x+40},{y} L{x+40},{y+h} L{x},{y+h-40} L{x-40},{y+h} Z" fill="{c1}" stroke="{INK}" stroke-width="5"/>'
            f'<path d="M{x-22},{y+40} l22,30 l22,-30 M{x-22},{y+90} l22,30 l22,-30" stroke="{c2}" stroke-width="6" fill="none"/>'
            f'<path d="M{x-56},{y} L{x+56},{y}" stroke="#4A3826" stroke-width="10" stroke-linecap="round"/>')

def brazier(x, y, s=1.0):
    return (f'<g transform="translate({x},{y}) scale({s})"><path d="M-30,0 L-14,-80 M30,0 L14,-80 M0,0 L0,-80" stroke="#2A2A2A" stroke-width="8"/>'
            f'<path d="M-46,-80 L46,-80 L34,-110 L-34,-110 Z" fill="#3A3A3A" stroke="{INK}" stroke-width="5"/>'
            f'<path d="M-30,-110 Q-20,-170 0,-190 Q10,-150 30,-110 Z" fill="#F08A2A"/><path d="M-12,-110 Q-6,-150 4,-160 Q8,-130 14,-110 Z" fill="#FFD27A"/></g>')

def greathall(fire=1.0):
    """Kral/jarl salonu: uzun evin iskeleti + kürsüde hükümdar koltuğu + sancaklar + mangallar."""
    o = P.longhouse(fire)
    o += banner(780, 320, 230, "#2F4C6E", "#D8C8A0") + banner(1140, 320, 230, "#6E2A22", "#C9A25A")
    o += high_seat(960, 650, 0.62)
    o += brazier(700, 700, 0.8) + brazier(1220, 700, 0.8)
    return o

def turf_house(x, y, w, h, flip=1):
    rr = R(int(x))
    return (f'<g transform="translate({x},{y}) scale({flip},1)">'
            f'<g filter="url(#t_ahsap)"><rect x="{-w/2}" y="{-h}" width="{w}" height="{h}" fill="#5A4430"/></g>'
            f'<rect x="{-w/2}" y="{-h}" width="{w}" height="{h}" fill="none" stroke="{INK}" stroke-width="6"/>'
            + "".join(f'<path d="M{-w/2 + k*w/8:.0f},{-h} L{-w/2 + k*w/8:.0f},0" stroke="#3A2C1E" stroke-width="3"/>' for k in range(1, 8))
            + f'<path d="M{-w/2-30},{-h+6} Q0,{-h-h*0.9:.0f} {w/2+30},{-h+6} Z" fill="#5E6E44" stroke="{INK}" stroke-width="6"/>'
            + "".join(f'<path d="M{rr.uniform(-w/2, w/2):.0f},{-h - rr.uniform(10, h*0.6):.0f} q4,-12 10,-16" stroke="#7E8E5A" stroke-width="4" fill="none"/>' for _ in range(18))
            + f'<rect x="{-w*0.08:.0f}" y="{-h*0.62:.0f}" width="{w*0.16:.0f}" height="{h*0.62:.0f}" fill="#2A1E14" stroke="{INK}" stroke-width="5"/></g>')

def kattegat(snow=True):
    o = ["<defs>" + tex.TEX["ahsap"] + tex.TEX["tas"] + tex.TEX["kurk"] + tex.TEX["metal"] + "</defs>",
         '<defs><linearGradient id="ksky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7E94AA"/><stop offset="1" stop-color="#C8D2DC"/></linearGradient></defs>',
         f'<rect width="{W}" height="{H}" fill="url(#ksky)"/>']
    # uzak dağlar + fiyort
    o.append('<path d="M0,470 L180,330 L330,420 L520,280 L720,430 L900,350 L1100,440 L1320,300 L1520,420 L1720,320 L1920,420 L1920,560 L0,560 Z" fill="#6E8094"/>')
    o.append('<path d="M0,470 L180,330 L230,370 L300,360 M520,280 L580,330 L640,320 M1320,300 L1380,350 M1720,320 L1770,360" stroke="#E6ECF2" stroke-width="10" fill="none" stroke-linejoin="round"/>')
    o.append('<rect x="0" y="540" width="1920" height="70" fill="#8AA0B4"/>' + "".join(f'<path d="M{R(k).uniform(0,1900):.0f},{R(k+3).uniform(550,600):.0f} h{R(k+5).uniform(30,90):.0f}" stroke="#D6E0EA" stroke-width="2.5" opacity="0.7"/>' for k in range(24)))
    # iskele + uzak gemi
    o.append('<path d="M1380,600 L1700,590" stroke="#3A2C1E" stroke-width="14"/>' + "".join(f'<path d="M{x},596 L{x},640" stroke="#3A2C1E" stroke-width="8"/>' for x in range(1400, 1700, 50)))
    o.append('<path d="M1500,560 Q1600,590 1700,560 L1690,548 L1510,548 Z" fill="#4A3826" stroke="#1A1410" stroke-width="4"/><path d="M1600,548 L1600,470" stroke="#3A2C1E" stroke-width="6"/>')
    # evler (çimen dam), çit, duman
    for (x, y, w_, h_, f_) in ((250, 640, 360, 150, 1), (700, 620, 300, 120, -1), (1180, 630, 280, 110, 1), (1850, 660, 340, 160, -1)):
        o.append(turf_house(x, y, w_, h_, f_))
        o.append(f'<path d="M{x+20},{y-h_*1.6:.0f} q-20,-60 10,-120 q30,-60 0,-120" stroke="#B8C2CC" stroke-width="22" fill="none" opacity="0.35" stroke-linecap="round"/>')
    # zemin: çamurlu yol + karlı kenarlar
    o.append(f'<path d="M0,640 Q600,610 1920,650 L1920,{H} L0,{H} Z" fill="#5E5040"/>')
    o.append(f'<g filter="url(#t_tas)"><path d="M0,640 Q600,610 1920,650 L1920,{H} L0,{H} Z" fill="#6E604C" opacity="0.5"/></g>')
    o.append(f'<path d="M700,{H} Q900,800 1100,660 L1300,660 Q1300,820 1500,{H} Z" fill="#7A6A52" opacity="0.8"/>')        # yol
    if snow:
        o.append(f'<path d="M0,650 Q300,630 620,660 Q500,760 0,800 Z" fill="#E6ECF2" opacity="0.85"/><path d="M1500,670 Q1700,650 1920,660 L1920,820 Q1700,780 1560,760 Z" fill="#E6ECF2" opacity="0.85"/>')
    o.append("".join(f'<path d="M{x},{720 + (x % 3) * 4} L{x},{640 + (x % 3) * 4}" stroke="#4A3826" stroke-width="8"/>' for x in range(40, 600, 46))
             + '<path d="M40,668 L600,668 M40,700 L600,700" stroke="#4A3826" stroke-width="6"/>')
    return "".join(o)

def donkey_cart(x, y, s=1.0, trunks=True, flip=1):
    """Eşek arabası: yan görünüş, eşek sağda (yol yönü). Yerel: arabanın tabanı (0,0)."""
    sp = (f'<g transform="translate({x},{y}) scale({s*flip},{s})">'
          f'<g filter="url(#t_ahsap)"><path d="M-220,-140 L180,-140 L170,-60 L-210,-60 Z" fill="#7A5A3A"/></g>'
          f'<path d="M-220,-140 L180,-140 L170,-60 L-210,-60 Z" fill="none" stroke="{INK}" stroke-width="7"/>'
          + "".join(f'<path d="M{-210 + k*48},-140 L{-206 + k*48},-60" stroke="#5A4028" stroke-width="4"/>' for k in range(1, 8)))
    if trunks:
        sp += (f'<g filter="url(#t_ahsap)"><rect x="-190" y="-250" width="150" height="110" rx="10" fill="#6A4A30"/><rect x="-20" y="-220" width="130" height="80" rx="8" fill="#5A3E28"/></g>'
               f'<rect x="-190" y="-250" width="150" height="110" rx="10" fill="none" stroke="{INK}" stroke-width="6"/><rect x="-20" y="-220" width="130" height="80" rx="8" fill="none" stroke="{INK}" stroke-width="6"/>'
               f'<path d="M-190,-200 L-40,-200 M-20,-182 L110,-182" stroke="#8A8A86" stroke-width="8"/><rect x="-124" y="-214" width="18" height="24" fill="#B08A3A" stroke="{INK}" stroke-width="3"/>'
               f'<g filter="url(#t_kurk)"><path d="M-40,-150 Q30,-190 120,-150 L110,-140 L-30,-140 Z" fill="#8A7A62"/></g>')
    for wx in (-130, 100):   # tekerlekler
        sp += (f'<g transform="translate({wx},-40)"><circle r="62" fill="none" stroke="{INK}" stroke-width="20"/><circle r="62" fill="none" stroke="#5A4028" stroke-width="12"/>'
               + "".join(f'<path d="M0,0 L{58*math.cos(a):.0f},{58*math.sin(a):.0f}" stroke="#4A3420" stroke-width="7"/>' for a in [k * math.pi / 4 for k in range(8)])
               + f'<circle r="14" fill="#3A2A1A" stroke="{INK}" stroke-width="4"/></g>')
    # oklar + eşek
    sp += (f'<path d="M170,-110 L330,-130" stroke="{INK}" stroke-width="12" stroke-linecap="round"/><path d="M170,-110 L330,-130" stroke="#6A4A30" stroke-width="7" stroke-linecap="round"/>'
           f'<g transform="translate(420,-20)">'
           f'<path d="M-110,-150 Q-120,-210 -40,-214 L70,-210 Q110,-208 120,-170 L118,-120 Q100,-90 60,-96 L-80,-96 Q-112,-100 -110,-150 Z" fill="#7E7468" stroke="{INK}" stroke-width="6"/>'   # gövde
           f'<path d="M-90,-100 L-96,0 M-60,-98 L-54,0 M60,-100 L66,0 M90,-104 L100,0" stroke="{INK}" stroke-width="30" stroke-linecap="round"/><path d="M-90,-100 L-96,0 M-60,-98 L-54,0 M60,-100 L66,0 M90,-104 L100,0" stroke="#6E6458" stroke-width="20" stroke-linecap="round"/>'
           f'<path d="M100,-180 Q140,-250 170,-260 Q210,-266 222,-232 Q230,-200 200,-196 Q170,-196 150,-160 Z" fill="#7E7468" stroke="{INK}" stroke-width="6"/>'    # boyun + baş
           f'<path d="M168,-258 L156,-318 L178,-268 M186,-262 L190,-322 L198,-264" fill="#7E7468" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'  # uzun kulaklar
           f'<ellipse cx="214" cy="-214" rx="16" ry="14" fill="#B8AEA0" stroke="{INK}" stroke-width="4"/><circle cx="188" cy="-238" r="5" fill="{INK}"/>'
           f'<path d="M130,-200 Q160,-220 180,-232" stroke="#4A3E34" stroke-width="10" fill="none"/>'                                                       # yele
           f'<path d="M-112,-150 Q-140,-140 -136,-100" stroke="#4A3E34" stroke-width="8" fill="none" stroke-linecap="round"/>'                              # kuyruk
           f'<path d="M-20,-214 L-10,-96 M20,-212 L30,-96" stroke="#5A3A24" stroke-width="10"/><path d="M140,-190 Q170,-170 200,-200" stroke="#5A3A24" stroke-width="7" fill="none"/></g></g>')
    return sp

CART_DEFS = "<defs>" + tex.TEX["ahsap"] + tex.TEX["kurk"] + "</defs>"
