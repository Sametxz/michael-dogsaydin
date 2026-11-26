"""Sahne 7 nesneleri v2 (kullanıcı 19.11 20:36: "eşek, araba, evler, yol ve zemin yetersiz; çizim tarzımıza göre modellensin").
Çizim dili hero_v5 ile aynı: kalın mürekkep kontur, form ışığı (tex.form), malzeme dokusu (tex), tek yönlü ışık (sol üst),
gölge tarafı soğuk. Her nesne kendi kartında değerlendirilir (§9 N1–N7).
- donkey(): yan görünüş, sağa bakar. Kimlik: uzun kulak (iç açık), açık renkli burun ve göbek, sırtta koyu çizgi ve omuzda haç, püsküllü kuyruk, dik kısa yele, koşum.
- cart(): tahta yataklı iki tekerlekli araba, demir bantlı sandıklar, ip bağlar, kürk bohça, oklar.
- longhouse_ext(): çimen damlı uzun ev (3/4): taş temel, dikey tahta duvar, oymalı alın tahtaları, kapı, damda kar ve duman.
- ground(): çamurlu yol (tekerlek izleri, su birikintisi), tahta yürüme yolu, taşlar, ot öbekleri, yumuşak kenarlı kar.
"""
import sys, math, random, subprocess
sys.path[:0] = ["/home/claude/r3", "/home/claude/r2"]
import tex
INK = "#1A1410"; R = random.Random

def defs(s=1.0):
    return ("<defs>" + tex.scaled("ahsap", s)[0] + tex.scaled("kurk", s)[0] + tex.scaled("tas", s)[0] + tex.scaled("deri", s)[0] + tex.TEX["metal"]
            + tex.form("f_form", blur=14 * s, scale=8, az=225) + tex.form("f_form_s", blur=6 * s, scale=6, az=225)
            + '<linearGradient id="g_coat" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9A8E80"/><stop offset="0.7" stop-color="#7E7366"/><stop offset="1" stop-color="#C8BEB0"/></linearGradient>'
            + '<linearGradient id="g_snow" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F4F8FB"/><stop offset="1" stop-color="#C8D6E4"/></linearGradient>'
            + '<linearGradient id="g_mud" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5E5040"/><stop offset="1" stop-color="#4A3E30"/></linearGradient>'
            + '<linearGradient id="g_pud" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#B8C8D8"/><stop offset="1" stop-color="#7E94AA"/></linearGradient>'
            + "</defs>")

def T(n, s=1.0): return f'filter="url(#{tex.scaled(n, s)[1]})"'

def _leg(pts, w0, w1, col, hoof="#2A2420"):
    d = "M" + " L".join(f"{x},{y}" for x, y in pts)
    o = []
    for (x0, y0), (x1, y1), ww in zip(pts, pts[1:], [w0, (w0 + w1) / 2, w1]):
        o.append(f'<path d="M{x0},{y0} L{x1},{y1}" stroke="{INK}" stroke-width="{ww+9}" stroke-linecap="round"/>')
    for (x0, y0), (x1, y1), ww in zip(pts, pts[1:], [w0, (w0 + w1) / 2, w1]):
        o.append(f'<path d="M{x0},{y0} L{x1},{y1}" stroke="{col}" stroke-width="{ww}" stroke-linecap="round"/>')
    hx, hy = pts[-1]
    o.append(f'<path d="M{hx-13},{hy-16} L{hx+13},{hy-16} L{hx+16},{hy} L{hx-15},{hy} Z" fill="{hoof}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
             f'<path d="M{hx-11},{hy-22} q11,5 22,0" stroke="#E2DAD0" stroke-width="4" fill="none" opacity="0.6"/>')   # bukağılık açık kıl
    return "".join(o)

def donkey(s=1.0, harness=True):
    """Yerel: zemin y=0, gövde ortası x≈0, sağa bakar. Cidago yüksekliği ≈ 235."""
    far = "#6A6056"; near = "url(#g_coat)"
    o = [f'<g filter="url(#f_form)">']
    o.append(_leg([(-118, -120), (-136, -58), (-122, 0)], 30, 16, far) + _leg([(78, -120), (84, -58), (86, 0)], 26, 16, far))   # uzak bacaklar
    body = ("M118,-196 Q104,-236 52,-238 Q-30,-232 -110,-232 Q-170,-234 -192,-196 Q-206,-150 -176,-118 Q-150,-98 -110,-100 "
            "Q-40,-92 40,-100 Q92,-102 118,-128 Q132,-160 118,-196 Z")
    o.append(f'<path d="{body}" fill="{near}" {T("kurk", s)}/>')
    neck = "M48,-234 Q86,-282 132,-322 Q152,-338 172,-330 Q178,-300 166,-268 Q150,-232 132,-192 Q122,-170 116,-150 Q98,-190 48,-234 Z"
    o.append(f'<path d="{neck}" fill="#8E8276" {T("kurk", s)}/>')
    head = ("M150,-330 Q170,-350 196,-338 Q232,-316 264,-270 Q280,-246 266,-228 Q252,-216 228,-222 Q206,-226 190,-246 Q172,-262 158,-282 Q144,-304 150,-330 Z")
    o.append(f'<path d="{head}" fill="#8E8276" {T("kurk", s)}/>')
    o.append('</g>')
    o.append(f'<path d="{body}" fill="none" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
             f'<path d="{neck}" fill="none" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>')
    # açık renkli göbek + koyu sırt çizgisi + omuz haçı (eşek kimliği)
    o.append(f'<path d="M-150,-112 Q-60,-96 60,-104 Q90,-106 110,-124" stroke="#D2C8BA" stroke-width="20" fill="none" stroke-linecap="round" opacity="0.85"/>')
    o.append(f'<path d="M150,-322 Q100,-280 52,-238 Q-40,-232 -150,-232 Q-182,-224 -192,-200" stroke="#3E362E" stroke-width="9" fill="none" stroke-linecap="round"/>'
             f'<path d="M66,-236 Q74,-200 70,-160" stroke="#3E362E" stroke-width="8" fill="none" stroke-linecap="round"/>')
    # dik kısa yele
    mane = "".join(f'<path d="M{150 - k*12:.0f},{-322 + k*11:.0f} l{-6 - (k % 2) * 3},{-22 + (k % 2) * 4}" stroke="#3E362E" stroke-width="7" stroke-linecap="round"/>' for k in range(9))
    o.append(mane)
    # kulaklar (uzun, iç açık)
    for (bx, by, tx, ty, c_) in ((156, -328, 116, -430, "#6E645A"), (170, -332, 146, -440, "#8E8276")):
        o.append(f'<path d="M{bx-10},{by} Q{tx-14},{(by+ty)/2:.0f} {tx},{ty} Q{tx+18},{(by+ty)/2:.0f} {bx+12},{by+4} Z" fill="{c_}" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
                 f'<path d="M{bx-2},{by-8} Q{tx-2},{(by+ty)/2:.0f} {tx+3},{ty+18}" stroke="#D8C8BC" stroke-width="7" fill="none" stroke-linecap="round"/>'
                 f'<path d="M{tx-4},{ty+4} q6,-6 10,2" stroke="#2A2420" stroke-width="6" fill="none"/>')
    o.append(f'<path d="{head}" fill="none" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>')
    # burun (açık, büyük), ağız, burun deliği, göz (beyaz halkalı)
    o.append(f'<path d="M232,-292 Q268,-262 270,-238 Q262,-218 232,-222 Q212,-228 204,-250 Q214,-280 232,-292 Z" fill="#D6CEC2" stroke="{INK}" stroke-width="5"/>'
             f'<path d="M250,-262 q8,4 10,12" stroke="{INK}" stroke-width="5" fill="none" stroke-linecap="round"/>'
             f'<path d="M236,-226 q14,4 26,-2" stroke="{INK}" stroke-width="4" fill="none"/>')
    o.append(f'<ellipse cx="190" cy="-306" rx="15" ry="12" fill="#E8E0D6" stroke="{INK}" stroke-width="3.5"/><ellipse cx="192" cy="-305" rx="8" ry="8" fill="#241C16"/><circle cx="189" cy="-308" r="2.6" fill="#FFFFFF"/>'
             f'<path d="M176,-316 q14,-8 28,0" stroke="{INK}" stroke-width="4" fill="none" stroke-linecap="round"/>')
    # kuyruk
    o.append(f'<path d="M-188,-214 Q-216,-160 -206,-112" stroke="{INK}" stroke-width="15" fill="none" stroke-linecap="round"/><path d="M-188,-214 Q-216,-160 -206,-112" stroke="#7E7366" stroke-width="8" fill="none" stroke-linecap="round"/>'
             f'<path d="M-206,-120 q-14,18 -6,42 q8,-8 14,0 q4,-24 -8,-42 Z" fill="#3E362E" stroke="{INK}" stroke-width="4"/>')
    # yakın bacaklar (dizler, bukağı, toynak)
    o.append(_leg([(-150, -128), (-170, -60), (-152, 0)], 40, 18, "#8A7E72") + _leg([(98, -124), (104, -60), (106, 0)], 30, 17, "#8A7E72"))
    o.append(f'<path d="M-180,-150 Q-168,-120 -150,-104" stroke="#6A6056" stroke-width="5" fill="none" opacity="0.7"/>')   # uyluk kıvrımı
    if harness:   # deri koşum: gerdanlık, göğüs kayışı, sırt kayışı
        o.append(f'<path d="M108,-150 Q126,-196 112,-238 Q96,-252 80,-236 Q96,-200 88,-150 Z" fill="#5A3A22" stroke="{INK}" stroke-width="5" {T("deri", s)}/>'
                 f'<path d="M100,-170 Q20,-160 -60,-170" stroke="{INK}" stroke-width="13" fill="none"/><path d="M100,-170 Q20,-160 -60,-170" stroke="#6A4A2C" stroke-width="8" fill="none"/>'
                 f'<path d="M20,-236 Q24,-170 14,-102" stroke="{INK}" stroke-width="13" fill="none"/><path d="M20,-236 Q24,-170 14,-102" stroke="#6A4A2C" stroke-width="8" fill="none"/>'
                 f'<circle cx="104" cy="-172" r="8" fill="#B08A3A" stroke="{INK}" stroke-width="3"/><circle cx="18" cy="-170" r="7" fill="#B08A3A" stroke="{INK}" stroke-width="3"/>'
                 f'<path d="M212,-300 Q238,-286 262,-262 M200,-246 Q220,-262 236,-290" stroke="#5A3A22" stroke-width="6" fill="none"/>')   # yular
    o.append(f'<ellipse cx="-30" cy="4" rx="230" ry="16" fill="#000" opacity="0.18"/>')
    return f'<g transform="scale({s})">' + "".join(o) + '</g>'

def wheel(cx, cy, r, hub="#3A2A1A"):
    o = [f'<g transform="translate({cx},{cy})">',
         f'<circle r="{r}" fill="none" stroke="{INK}" stroke-width="{r*0.32+8:.0f}"/>',
         f'<circle r="{r}" fill="none" stroke="#6A4A30" stroke-width="{r*0.32:.0f}" {T("ahsap")}/>',
         f'<circle r="{r+r*0.16:.0f}" fill="none" stroke="#5A5A58" stroke-width="5"/>']                     # demir şerit
    for k in range(10):
        a = k * math.pi / 5
        o.append(f'<path d="M{r*0.18*math.cos(a):.0f},{r*0.18*math.sin(a):.0f} L{r*0.86*math.cos(a):.0f},{r*0.86*math.sin(a):.0f}" stroke="{INK}" stroke-width="{r*0.13+5:.0f}" stroke-linecap="round"/>'
                 f'<path d="M{r*0.18*math.cos(a):.0f},{r*0.18*math.sin(a):.0f} L{r*0.86*math.cos(a):.0f},{r*0.86*math.sin(a):.0f}" stroke="#7A5A3A" stroke-width="{r*0.13:.0f}" stroke-linecap="round"/>')
    o.append(f'<circle r="{r*0.24:.0f}" fill="{hub}" stroke="{INK}" stroke-width="5"/><circle r="{r*0.09:.0f}" fill="#8A8A86" stroke="{INK}" stroke-width="3"/>'
             f'<path d="M{-r*0.7:.0f},{-r*0.55:.0f} A{r},{r} 0 0 1 {r*0.2:.0f},{-r*0.98:.0f}" stroke="#A8865E" stroke-width="5" fill="none" opacity="0.7"/></g>')
    return "".join(o)

def cart(trunks=True):
    """Yerel: zemin y=0, yatak merkezi x≈0, oklar sağa (+x)."""
    o = [f'<ellipse cx="0" cy="4" rx="250" ry="16" fill="#000" opacity="0.2"/>']
    o.append(wheel(-120, -78, 78, "#2E2218"))                                    # uzak tekerlek (arkada, kısmen)
    bed = "M-250,-196 L170,-196 L176,-150 L-244,-150 Z"
    side = "M-246,-150 L172,-150 L166,-108 L-238,-108 Z"
    o.append(f'<g filter="url(#f_form_s)"><path d="{bed}" fill="#8A6A48" {T("ahsap")}/><path d="{side}" fill="#6A4E34" {T("ahsap")}/></g>'
             f'<path d="{bed}" fill="none" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/><path d="{side}" fill="none" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>')
    o.append("".join(f'<path d="M{x},-150 L{x-2},-108" stroke="#4A3420" stroke-width="5"/>' for x in range(-200, 170, 52))
             + "".join(f'<rect x="{x-7}" y="-152" width="14" height="46" fill="#5A5A58" stroke="{INK}" stroke-width="3" {T("metal")}/><circle cx="{x}" cy="-140" r="3" fill="#2A2A2A"/><circle cx="{x}" cy="-118" r="3" fill="#2A2A2A"/>' for x in (-226, 150)))
    # yan parmaklık (direkler + üst kiriş)
    o.append("".join(f'<path d="M{x},-196 L{x},-250" stroke="{INK}" stroke-width="16"/><path d="M{x},-196 L{x},-250" stroke="#7A5A3A" stroke-width="9"/>' for x in (-236, -110, 20, 150))
             + f'<path d="M-244,-246 L158,-246" stroke="{INK}" stroke-width="16" stroke-linecap="round"/><path d="M-244,-246 L158,-246" stroke="#8A6A48" stroke-width="9" stroke-linecap="round"/>')
    if trunks:
        for (x, y, w_, h_, c_) in ((-220, -300, 170, 110, "#6A4A30"), (-36, -282, 140, 90, "#5A3E28")):
            o.append(f'<g filter="url(#f_form_s)"><rect x="{x}" y="{y}" width="{w_}" height="{h_}" rx="10" fill="{c_}" {T("ahsap")}/></g>'
                     f'<rect x="{x}" y="{y}" width="{w_}" height="{h_}" rx="10" fill="none" stroke="{INK}" stroke-width="6"/>'
                     f'<path d="M{x},{y+24} Q{x+w_/2},{y+10} {x+w_},{y+24}" stroke="{INK}" stroke-width="5" fill="none"/>'
                     + "".join(f'<rect x="{x+w_*f_-8:.0f}" y="{y}" width="16" height="{h_}" fill="#5A5A58" stroke="{INK}" stroke-width="3" {T("metal")}/>' for f_ in (0.18, 0.82))
                     + f'<rect x="{x+w_/2-12:.0f}" y="{y+30}" width="24" height="28" rx="3" fill="#B08A3A" stroke="{INK}" stroke-width="3"/>')
        o.append(f'<g filter="url(#f_form_s)"><path d="M110,-196 Q120,-270 170,-262 Q206,-250 196,-196 Z" fill="#9A8A70" {T("kurk")}/></g>'
                 f'<path d="M110,-196 Q120,-270 170,-262 Q206,-250 196,-196 Z" fill="none" stroke="{INK}" stroke-width="5"/>')   # kürk bohça
        o.append(f'<path d="M-230,-300 Q-140,-330 -60,-250 M-30,-282 Q40,-300 104,-240" stroke="#C8B08A" stroke-width="6" fill="none"/>'
                 f'<path d="M-230,-300 Q-140,-330 -60,-250 M-30,-282 Q40,-300 104,-240" stroke="{INK}" stroke-width="2" fill="none" opacity="0.6"/>')   # ip bağlar
    # oklar (koşum kolları) — eşeğin gerdanlığına
    o.append(f'<path d="M150,-160 L360,-172" stroke="{INK}" stroke-width="18" stroke-linecap="round"/><path d="M150,-160 L360,-172" stroke="#7A5A3A" stroke-width="10" stroke-linecap="round"/>')
    o.append(wheel(70, -78, 78))                                                     # yakın tekerlek
    return "".join(o)

def donkey_cart(x, y, s=1.0):
    return f'<g transform="translate({x},{y}) scale({s})"><g transform="translate(-160,0)">{cart()}</g><g transform="translate(330,0) scale(0.9)">{donkey()}</g></g>'

def longhouse_ext(x, y, w=520, h=150, s=1.0, snow=True, smoke=True):
    """3/4 görünüş: sol uçta alın, sağa uzanan yan duvar. Yerel: zemin (0,0) = alın köşesi."""
    gw = w * 0.36
    o = [f'<g transform="translate({x},{y}) scale({s})">', f'<ellipse cx="{w*0.4:.0f}" cy="6" rx="{w*0.62:.0f}" ry="18" fill="#000" opacity="0.2"/>']
    # taş temel
    o.append("".join(f'<g filter="url(#f_form_s)"><ellipse cx="{xx:.0f}" cy="-10" rx="{R(int(xx)).uniform(16, 26):.0f}" ry="12" fill="#6E6A64" {T("tas")}/></g><ellipse cx="{xx:.0f}" cy="-10" rx="{R(int(xx)).uniform(16, 26):.0f}" ry="12" fill="none" stroke="{INK}" stroke-width="3"/>' for xx in [i * 34 - gw for i in range(int((w + gw) / 34) + 1)]))
    # alın duvarı (beşgen) ve yan duvar
    gable = f"M{-gw:.0f},-18 L{-gw:.0f},{-h} L{-gw/2:.0f},{-h*1.9:.0f} L0,{-h} L0,-18 Z"
    side = f"M0,-18 L0,{-h} L{w},{-h+18} L{w},-4 Z"
    o.append(f'<g filter="url(#f_form)"><path d="{gable}" fill="#7A5A3C" {T("ahsap")}/><path d="{side}" fill="#5E4630" {T("ahsap")}/></g>')
    o.append("".join(f'<path d="M{-gw + k*gw/7:.0f},-18 L{-gw + k*gw/7:.0f},{-h - (h*0.9) * (1 - abs(2*k/7 - 1)):.0f}" stroke="#4A3420" stroke-width="3"/>' for k in range(1, 7))
             + "".join(f'<path d="M{k*w/10:.0f},{-18 + k*1.4:.0f} L{k*w/10:.0f},{-h + k*1.8:.0f}" stroke="#3A2A1A" stroke-width="3"/>' for k in range(1, 10)))
    o.append(f'<path d="{gable}" fill="none" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/><path d="{side}" fill="none" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>')
    # kapı (yan duvarda) + pencere aralığı
    dx = w * 0.42
    o.append(f'<path d="M{dx-34:.0f},-14 L{dx-34:.0f},{-h*0.7:.0f} Q{dx:.0f},{-h*0.86:.0f} {dx+34:.0f},{-h*0.7:.0f} L{dx+34:.0f},-12 Z" fill="#241A12" stroke="{INK}" stroke-width="6"/>'
             f'<path d="M{dx-42:.0f},-12 L{dx-42:.0f},{-h*0.72:.0f} Q{dx:.0f},{-h*0.92:.0f} {dx+42:.0f},{-h*0.72:.0f} L{dx+42:.0f},-10" fill="none" stroke="#8A6A48" stroke-width="9"/>'
             f'<rect x="{w*0.75:.0f}" y="{-h*0.66:.0f}" width="34" height="22" fill="#FFB060" stroke="{INK}" stroke-width="4" opacity="0.9"/>')
    # çimen dam (kalın, kavisli), sırtta kar, saçak altı gölgesi
    roof = (f"M{-gw-30:.0f},{-h+10} L{-gw/2:.0f},{-h*1.96:.0f} Q{w*0.4:.0f},{-h*2.15:.0f} {w+30},{-h*1.7:.0f} "
            f"Q{w+52},{-h*1.3:.0f} {w+26},{-h+28} Q{w*0.5:.0f},{-h+6} 0,{-h-10} Z")
    o.append(f'<path d="M0,{-h-4} Q{w*0.5:.0f},{-h+12} {w+20},{-h+30}" stroke="#1A120C" stroke-width="16" fill="none" opacity="0.6"/>')
    o.append(f'<g filter="url(#f_form)"><path d="{roof}" fill="#5E6E44" {T("kurk", 0.7)}/></g><path d="{roof}" fill="none" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>')
    o.append("".join(f'<path d="M{R(k).uniform(-gw, w):.0f},{-h*R(k+1).uniform(1.1, 1.9):.0f} q{R(k+2).uniform(-6, 6):.0f},-14 {R(k+3).uniform(-4, 10):.0f},-22" stroke="#8A9A62" stroke-width="4" fill="none" stroke-linecap="round"/>' for k in range(int(w / 9))))
    o.append(f'<path d="M{-gw-30:.0f},{-h+10} L{-gw/2:.0f},{-h*1.96:.0f} L0,{-h-10}" fill="none" stroke="#4A3420" stroke-width="12"/>')                 # alın tahtaları
    o.append(f'<path d="M{-gw/2-6:.0f},{-h*1.96:.0f} q-22,-30 -6,-56 q10,-6 14,6 M{-gw/2+6:.0f},{-h*1.96:.0f} q22,-30 6,-56 q-10,-6 -14,6" stroke="{INK}" stroke-width="12" fill="none" stroke-linecap="round"/>'
             f'<path d="M{-gw/2-6:.0f},{-h*1.96:.0f} q-22,-30 -6,-56 q10,-6 14,6 M{-gw/2+6:.0f},{-h*1.96:.0f} q22,-30 6,-56 q-10,-6 -14,6" stroke="#6A4A30" stroke-width="6" fill="none" stroke-linecap="round"/>')   # çapraz oymalı başlar
    if snow:
        o.append(f'<path d="M{-gw/2:.0f},{-h*1.96:.0f} Q{w*0.4:.0f},{-h*2.15:.0f} {w+30},{-h*1.7:.0f} Q{w*0.5:.0f},{-h*1.86:.0f} {-gw/2+30:.0f},{-h*1.82:.0f} Z" fill="url(#g_snow)" stroke="{INK}" stroke-width="4"/>')
    if smoke:
        o.append(f'<path d="M{w*0.45:.0f},{-h*2.1:.0f} q-30,-60 10,-120 q40,-60 0,-130" stroke="#C8D2DC" stroke-width="26" fill="none" opacity="0.35" stroke-linecap="round"/>')
    o.append('</g>')
    return "".join(o)

def ground(W=1920, H=1080, y0=640, road=True):
    o = [f'<path d="M0,{y0} Q600,{y0-30} {W},{y0+10} L{W},{H} L0,{H} Z" fill="url(#g_mud)"/>',
         f'<g filter="url(#f_form)"><path d="M0,{y0} Q600,{y0-30} {W},{y0+10} L{W},{H} L0,{H} Z" fill="#6A5A46" opacity="0.45" {T("tas", 0.6)}/></g>']
    if road:
        rd = f"M{W*0.36:.0f},{H} Q{W*0.46:.0f},{y0+150} {W*0.58:.0f},{y0+16} L{W*0.66:.0f},{y0+16} Q{W*0.68:.0f},{y0+160} {W*0.80:.0f},{H} Z"
        o.append(f'<path d="{rd}" fill="#7A6850"/><path d="{rd}" fill="none" stroke="#3E3226" stroke-width="5" opacity="0.7"/>')
        for off in (0.40, 0.70):   # tekerlek izleri
            o.append(f'<path d="M{W*(0.36 + off*0.44):.0f},{H} Q{W*(0.46 + off*0.22):.0f},{y0+150} {W*(0.58 + off*0.08):.0f},{y0+18}" stroke="#4A3C2C" stroke-width="10" fill="none" opacity="0.8"/>'
                     f'<path d="M{W*(0.36 + off*0.44)+10:.0f},{H} Q{W*(0.46 + off*0.22)+8:.0f},{y0+150} {W*(0.58 + off*0.08)+2:.0f},{y0+18}" stroke="#9A8668" stroke-width="3" fill="none" opacity="0.6"/>')
        for (px, py, rx) in ((W*0.52, y0+230, 70), (W*0.66, y0+330, 90), (W*0.58, y0+90, 40)):   # su birikintileri
            o.append(f'<ellipse cx="{px:.0f}" cy="{py:.0f}" rx="{rx}" ry="{rx*0.22:.0f}" fill="url(#g_pud)" stroke="#3E3226" stroke-width="4"/>'
                     f'<path d="M{px-rx*0.5:.0f},{py-rx*0.05:.0f} h{rx*0.6:.0f}" stroke="#F0F6FA" stroke-width="3" opacity="0.8"/>')
    # tahta yürüme yolu (sol ön)
    o.append("".join(f'<g filter="url(#f_form_s)"><path d="M{60+k*70},{y0+70+k*6} l64,0 l-6,26 l-64,0 Z" fill="#7A5A3C" {T("ahsap")}/></g><path d="M{60+k*70},{y0+70+k*6} l64,0 l-6,26 l-64,0 Z" fill="none" stroke="{INK}" stroke-width="4"/>' for k in range(7)))
    # taşlar + ot öbekleri
    for k in range(18):
        r_ = R(k + 400); x = r_.uniform(0, W); y = r_.uniform(y0 + 40, H - 40); rr = r_.uniform(10, 26) * (0.6 + (y - y0) / 600)
        o.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{rr:.0f}" ry="{rr*0.6:.0f}" fill="#8E8A82"/><ellipse cx="{x:.0f}" cy="{y+rr*0.15:.0f}" rx="{rr*0.85:.0f}" ry="{rr*0.35:.0f}" fill="#6A665E" opacity="0.6"/><ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{rr:.0f}" ry="{rr*0.6:.0f}" fill="none" stroke="{INK}" stroke-width="3.5"/>'
                 f'<path d="M{x-rr*0.6:.0f},{y-rr*0.2:.0f} q{rr*0.6:.0f},{-rr*0.5:.0f} {rr*1.1:.0f},{-rr*0.1:.0f}" stroke="#B8B4AC" stroke-width="3" fill="none"/>')
    for k in range(40):
        r_ = R(k + 700); x = r_.uniform(0, W); y = r_.uniform(y0 + 10, H)
        if W * 0.38 < x < W * 0.78 and y > y0 + 60: continue
        o.append("".join(f'<path d="M{x + j*5:.0f},{y:.0f} q{(j-1)*4},-10 {(j-1)*7},-{16 + j*3}" stroke="#7A8A52" stroke-width="3.5" fill="none" stroke-linecap="round"/>' for j in range(3)))
    # kar: yumuşak kenarlı yamalar (gölge kenarı soğuk mavi)
    for (cx, cy, rx, ry) in ((220, y0 + 40, 300, 50), (1720, y0 + 60, 260, 60), (980, y0 + 250, 140, 26)):
        o.append(f'<path d="M{cx-rx},{cy} Q{cx-rx*0.6:.0f},{cy-ry} {cx},{cy-ry*0.8:.0f} Q{cx+rx*0.7:.0f},{cy-ry*1.1:.0f} {cx+rx},{cy} Q{cx+rx*0.4:.0f},{cy+ry*0.7:.0f} {cx-rx*0.2:.0f},{cy+ry*0.5:.0f} Q{cx-rx*0.8:.0f},{cy+ry*0.6:.0f} {cx-rx},{cy} Z" fill="url(#g_snow)" stroke="#8AA0B6" stroke-width="4"/>')
    return "".join(o)

def kattegat2(W=1920, H=1080):
    """Kattegat dış mekânı v2: gökyüzü, karlı dağlar, fiyort, iskele ve gemi, uzun evler, çit, zemin."""
    import places7 as P7
    sky = P7.kattegat(snow=False)
    i = sky.index('<path d="M0,640 Q600,610')            # eski evleri ve zemini at, gökyüzü/dağ/fiyort/iskele kalsın
    head = sky[:i]
    head = head.split('<g transform="translate(250,640)')[0]
    o = [defs(), head]
    o.append(longhouse_ext(120, 650, 420, 120, 0.8) + longhouse_ext(860, 620, 360, 100, 0.62, smoke=True) + longhouse_ext(1420, 640, 380, 110, 0.7))
    o.append(ground(W, H, 640))
    # örgü çit (sol)
    o.append("".join(f'<path d="M{x},{760 + (x % 3) * 3} L{x},{690 + (x % 3) * 3}" stroke="{INK}" stroke-width="12" stroke-linecap="round"/><path d="M{x},{760 + (x % 3) * 3} L{x},{690 + (x % 3) * 3}" stroke="#5A4430" stroke-width="7" stroke-linecap="round"/>' for x in range(30, 420, 40))
             + "".join(f'<path d="M20,{y} Q220,{y-8} 430,{y}" stroke="{INK}" stroke-width="9" fill="none"/><path d="M20,{y} Q220,{y-8} 430,{y}" stroke="#7A5A3C" stroke-width="5" fill="none"/>' for y in (712, 732, 752)))
    return "".join(o)

def card(out="/home/claude/r3/veda2/nesne_karti7_v2.png"):
    CW, CH = 2400, 1500
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{CW}" height="{CH}">{defs()}<rect width="{CW}" height="{CH}" fill="#EDE2CC"/>',
         '<text x="40" y="70" font-family="Pirata One" font-size="54" fill="#2A1D14">Sahne 7 · nesne kartı v2: eşek, araba, uzun ev (dış), zemin</text>']
    lab = lambda x, y, t: f'<text x="{x}" y="{y}" font-family="Alegreya SC" font-size="26" fill="#2A1D14">{t}</text>'
    o.append(f'<g transform="translate(700,640)">{donkey_cart(0, 0, 1.0)}</g>' + lab(80, 700, "eşek arabası · tahta yatak, demir bantlı sandıklar, ip, kürk bohça · eşek: uzun kulak, açık burun, sırt çizgisi ve omuz haçı, koşum"))
    o.append(f'<g transform="translate(1700,620) scale(0.5)">{donkey()}</g>' + lab(1620, 700, "eşek · kare ölçeği (0,5×)"))
    o.append(f'<g transform="translate(250,1180)">{longhouse_ext(0, 0, 520, 150, 1.0)}</g>' + lab(80, 1240, "uzun ev (dış, 3/4) · taş temel, tahta duvar, çimen dam, kar, oymalı alın, kapı, duman"))
    o.append(f'<svg x="1180" y="760" width="1180" height="560" viewBox="0 520 1920 560">{ground()}</svg>' + lab(1180, 1350, "zemin · çamurlu yol, tekerlek izi, su birikintisi, tahta yol, taş, ot, kar"))
    o.append('</svg>')
    open("/home/claude/r3/veda2/nesne_karti7.svg", "w").write("".join(o))
    subprocess.run(["rsvg-convert", "/home/claude/r3/veda2/nesne_karti7.svg", "-w", str(CW), "-o", out], check=True)

if __name__ == "__main__":
    card(); print("ok")


# ======================================================================= v3 (kullanıcı 19.11 20:45)
# Dizideki Kattegat: dik dağların arasındaki koyu bir gölün (fiyort) kıyısında, ahşap ve sazdan
# evlerden oluşan köy; iskelede uzun gemiler. Sazdan (saman) dik çatılar, kalın saçaklar, ahşap duvarlar.
def thatch_house(x, y, s=1.0, gw=260, L=360, h=110, rh=230, door=True, smoke=True, snow=0.0, light=True):
    """Sazdan çatılı uzun ev, 3/4 perspektif: alın cephesi kameraya dönük, yan duvar sağa ve geriye kaçar.
    Yerel: alın cephesinin sol alt köşesi (0,0)."""
    k = 0.80; dy = -L * 0.16
    A = (gw / 2, -h - rh); BA = (gw / 2 + L, dy - (h + rh) * k)
    FRt = (gw, -h); BRt = (gw + L, dy - h * k); BR = (gw + L, dy)
    ov = gw * 0.16
    o = [f'<g transform="translate({x},{y}) scale({s})">',
         f'<ellipse cx="{gw/2 + L*0.5:.0f}" cy="6" rx="{(gw + L)*0.62:.0f}" ry="{22}" fill="#000" opacity="0.22"/>']
    side = f"M{gw},0 L{BR[0]:.0f},{BR[1]:.0f} L{BRt[0]:.0f},{BRt[1]:.0f} L{FRt[0]},{FRt[1]} Z"
    front = f"M0,0 L{gw},0 L{gw},{-h} L0,{-h} Z"
    o.append(f'<g filter="url(#f_form)"><path d="{side}" fill="#4E3A28" {T("ahsap", 0.8)}/><path d="{front}" fill="#6E5236" {T("ahsap", 0.8)}/></g>')
    o.append("".join(f'<path d="M{gw + L*t:.0f},{dy*t:.0f} L{gw + L*t:.0f},{dy*t - h*(1 - (1 - k)*t):.0f}" stroke="#2E2216" stroke-width="{4 - 2*t:.1f}"/>' for t in [i / 9 for i in range(1, 9)]))
    o.append("".join(f'<path d="M{gw*i/8:.0f},0 L{gw*i/8:.0f},{-h}" stroke="#4A3622" stroke-width="3"/>' for i in range(1, 8)))
    o.append(f'<path d="M0,0 L{gw},0 L{BR[0]:.0f},{BR[1]:.0f}" stroke="#5E5A54" stroke-width="18" fill="none" stroke-linecap="round"/>')   # taş temel
    o.append(f'<path d="{side}" fill="none" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/><path d="{front}" fill="none" stroke="{INK}" stroke-width="6"/>')
    # köşe direkleri
    o.append(f'<path d="M0,0 L0,{-h} M{gw},0 L{gw},{-h}" stroke="{INK}" stroke-width="16"/><path d="M0,0 L0,{-h} M{gw},0 L{gw},{-h}" stroke="#3E2C1C" stroke-width="10"/>')
    if door:
        dw = gw * 0.26
        o.append(f'<path d="M{gw/2-dw/2:.0f},0 L{gw/2-dw/2:.0f},{-h*0.78:.0f} L{gw/2+dw/2:.0f},{-h*0.78:.0f} L{gw/2+dw/2:.0f},0 Z" fill="#1E140C" stroke="{INK}" stroke-width="6"/>'
                 f'<path d="M{gw/2-dw/2-8:.0f},0 L{gw/2-dw/2-8:.0f},{-h*0.84:.0f} L{gw/2+dw/2+8:.0f},{-h*0.84:.0f} L{gw/2+dw/2+8:.0f},0" fill="none" stroke="#7A5A3C" stroke-width="10"/>')
        if light: o.append(f'<path d="M{gw/2-dw/2+6:.0f},-4 L{gw/2-dw/2+6:.0f},{-h*0.7:.0f} L{gw/2:.0f},{-h*0.7:.0f} L{gw/2:.0f},-4 Z" fill="#FFB060" opacity="0.55"/>')
    # alın üçgeni (tahta) — saz çatının altında
    o.append(f'<path d="M0,{-h} L{gw},{-h} L{A[0]:.0f},{A[1]:.0f} Z" fill="#5E4630" {T("ahsap", 0.8)}/><path d="M0,{-h} L{gw},{-h} L{A[0]:.0f},{A[1]:.0f} Z" fill="none" stroke="{INK}" stroke-width="5"/>')
    o.append("".join(f'<path d="M{gw*i/6:.0f},{-h} L{gw*i/6:.0f},{-h - rh*(1 - abs(2*i/6 - 1)):.0f}" stroke="#3A2A1A" stroke-width="3"/>' for i in range(1, 6)))
    # saz çatı: yan yüz (büyük) + alın saçağı (kalın kenar)
    roof_side = (f"M{A[0]:.0f},{A[1]-8:.0f} L{BA[0]:.0f},{BA[1]-6:.0f} L{BRt[0]+ov*0.8:.0f},{BRt[1]+ov*0.5:.0f} L{FRt[0]+ov:.0f},{FRt[1]+ov*0.6:.0f} Z")
    o.append(f'<g filter="url(#f_form)"><path d="{roof_side}" fill="#A88450"/></g>')
    rr = R(int(x * 7 + y))
    for i in range(int(L / 7)):        # saz demetleri: saçaktan sırta paralel çizgiler
        t = rr.uniform(0, 1); u = rr.uniform(0.15, 1.0)
        ex_ = FRt[0] + ov + (BRt[0] + ov * 0.8 - FRt[0] - ov) * t; ey_ = FRt[1] + ov * 0.6 + (BRt[1] + ov * 0.5 - FRt[1] - ov * 0.6) * t
        rx_ = A[0] + (BA[0] - A[0]) * t; ry_ = A[1] + (BA[1] - A[1]) * t
        o.append(f'<path d="M{ex_:.0f},{ey_:.0f} L{ex_ + (rx_ - ex_)*u:.0f},{ey_ + (ry_ - ey_)*u:.0f}" stroke="{["#7E6034", "#C8A46A", "#8E6E3E"][i % 3]}" stroke-width="{rr.uniform(2, 4):.1f}" opacity="0.8"/>')
    o.append(f'<path d="{roof_side}" fill="none" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>')
    eave = (f"M{-ov:.0f},{-h+ov*0.6:.0f} L{A[0]:.0f},{A[1]-14:.0f} L{gw+ov:.0f},{-h+ov*0.6:.0f} L{gw+ov*0.6:.0f},{-h+ov*1.3:.0f} L{A[0]:.0f},{A[1]+20:.0f} L{-ov*0.6:.0f},{-h+ov*1.3:.0f} Z")
    o.append(f'<path d="{eave}" fill="#8A6A3C" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>')
    o.append("".join(f'<path d="M{-ov + (A[0] + ov)*t:.0f},{-h + ov*0.6 + (A[1] - 14 + h - ov*0.6)*t:.0f} l{6},{14}" stroke="#5E4426" stroke-width="3"/>' for t in [i / 14 for i in range(1, 14)])
             + "".join(f'<path d="M{A[0] + (gw + ov - A[0])*t:.0f},{A[1] - 14 + (-h + ov*0.6 - A[1] + 14)*t:.0f} l{-6},{14}" stroke="#5E4426" stroke-width="3"/>' for t in [i / 14 for i in range(1, 14)]))
    o.append(f'<path d="M{A[0]:.0f},{A[1]-12:.0f} L{BA[0]:.0f},{BA[1]-8:.0f}" stroke="{INK}" stroke-width="16" stroke-linecap="round"/><path d="M{A[0]:.0f},{A[1]-12:.0f} L{BA[0]:.0f},{BA[1]-8:.0f}" stroke="#5E6E44" stroke-width="9" stroke-linecap="round"/>')   # sırtta çimen
    o.append(f'<path d="M{A[0]-8:.0f},{A[1]-12:.0f} q-30,-40 -10,-74 q14,-8 18,8 M{A[0]+8:.0f},{A[1]-12:.0f} q30,-40 10,-74 q-14,-8 -18,8" stroke="{INK}" stroke-width="13" fill="none" stroke-linecap="round"/>'
             f'<path d="M{A[0]-8:.0f},{A[1]-12:.0f} q-30,-40 -10,-74 q14,-8 18,8 M{A[0]+8:.0f},{A[1]-12:.0f} q30,-40 10,-74 q-14,-8 -18,8" stroke="#6A4A30" stroke-width="7" fill="none" stroke-linecap="round"/>')   # oymalı başlar
    if snow:
        o.append(f'<path d="M{A[0]:.0f},{A[1]-10:.0f} L{BA[0]:.0f},{BA[1]-8:.0f} L{BA[0]+L*0.05:.0f},{BA[1] + (BRt[1]-BA[1])*0.35*snow:.0f} L{A[0]+gw*0.3:.0f},{A[1] + (FRt[1]-A[1])*0.35*snow:.0f} Z" fill="url(#g_snow)" stroke="{INK}" stroke-width="4" opacity="0.95"/>')
    if smoke:
        sx, sy = (A[0] + BA[0]) / 2, (A[1] + BA[1]) / 2 - 10
        o.append(f'<path d="M{sx:.0f},{sy:.0f} q-30,-70 10,-140 q40,-70 -10,-160" stroke="#C8D2DC" stroke-width="30" fill="none" opacity="0.32" stroke-linecap="round"/>')
    o.append('</g>')
    return "".join(o)

def longship(x, y, s=1.0, flip=1):
    o = [f'<g transform="translate({x},{y}) scale({s*flip},{s})">',
         f'<path d="M-260,-40 Q-200,20 0,24 Q200,20 260,-40 Q240,-10 0,-6 Q-240,-10 -260,-40 Z" fill="#3E2C1C" stroke="{INK}" stroke-width="6"/>',
         f'<path d="M-250,-36 Q0,-4 250,-36" stroke="#6A4A30" stroke-width="5" fill="none"/>',
         "".join(f'<circle cx="{-180 + k*40}" cy="-16" r="13" fill="{["#8E3B2E", "#D8C8A0", "#2F4C6E"][k % 3]}" stroke="{INK}" stroke-width="3"/>' for k in range(10)),
         f'<path d="M260,-40 Q300,-90 286,-140 Q276,-170 300,-176 Q316,-160 300,-150" stroke="{INK}" stroke-width="14" fill="none" stroke-linecap="round"/><path d="M260,-40 Q300,-90 286,-140 Q276,-170 300,-176 Q316,-160 300,-150" stroke="#3E2C1C" stroke-width="8" fill="none" stroke-linecap="round"/>',
         f'<path d="M-260,-40 Q-290,-90 -280,-130" stroke="{INK}" stroke-width="12" fill="none" stroke-linecap="round"/>',
         f'<path d="M0,-20 L0,-250" stroke="{INK}" stroke-width="10"/><path d="M-120,-200 L120,-200" stroke="{INK}" stroke-width="8"/>',
         f'<path d="M-110,-198 Q0,-176 110,-198 L104,-180 Q0,-160 -104,-180 Z" fill="#B8302A" stroke="{INK}" stroke-width="4"/>',
         '</g>']
    return "".join(o)

def kattegat3(W=1920, H=1080, horizon=560):
    """Kattegat v3: koyu göl-fiyort, dik ve karlı dağlar, kıyı boyunca sazdan evler, iskelede gemiler, kıyıya inen patika."""
    o = [defs(),
         '<defs><linearGradient id="k3sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6E8298"/><stop offset="1" stop-color="#C2CCD6"/></linearGradient>'
         '<linearGradient id="k3lake" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5A6E80"/><stop offset="1" stop-color="#2E3E4C"/></linearGradient>'
         '<linearGradient id="k3m1" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7A8A98"/><stop offset="1" stop-color="#5E6E7C"/></linearGradient>'
         '<linearGradient id="k3m2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4E5A4C"/><stop offset="1" stop-color="#36402E"/></linearGradient></defs>',
         f'<rect width="{W}" height="{H}" fill="url(#k3sky)"/>']
    # uzak dağlar (soluk) + yakın dik yamaçlar (koyu, kayalık, karlı tepeler) → gölü çevreler
    o.append(f'<path d="M0,{horizon} L0,300 L220,180 L420,300 L640,150 L860,280 L1100,170 L1320,290 L1560,160 L1760,260 L1920,200 L1920,{horizon} Z" fill="url(#k3m1)"/>')
    o.append(f'<path d="M640,150 L700,200 L760,190 M1100,170 L1150,215 M1560,160 L1620,210 L1680,200 M220,180 L270,220" stroke="#E8EEF4" stroke-width="12" fill="none" stroke-linejoin="round"/>')
    o.append(f'<rect x="0" y="{horizon-120}" width="{W}" height="120" fill="#C8D2DC" opacity="0.35"/>')
    o.append(f'<path d="M0,{horizon+10} L0,260 Q120,250 240,330 Q360,420 520,470 L640,{horizon+10} Z" fill="url(#k3m2)"/>'
             f'<path d="M1920,{horizon+10} L1920,240 Q1780,250 1660,330 Q1520,430 1360,480 L1240,{horizon+10} Z" fill="url(#k3m2)"/>')
    o.append("".join(f'<path d="M{x0:.0f},{y0:.0f} l{R(k).uniform(-20,20):.0f},{R(k+1).uniform(30,70):.0f}" stroke="#2A3224" stroke-width="5" opacity="0.6"/>' for k, (x0, y0) in enumerate([(R(k).uniform(40, 560), R(k + 9).uniform(300, 520)) for k in range(16)] + [(R(k).uniform(1360, 1900), R(k + 9).uniform(300, 520)) for k in range(16, 32)])))
    o.append(f'<path d="M0,260 Q120,250 240,330 M1920,240 Q1780,250 1660,330" stroke="#E8EEF4" stroke-width="14" fill="none" opacity="0.8"/>')
    # göl
    o.append(f'<rect x="0" y="{horizon}" width="{W}" height="140" fill="url(#k3lake)"/>')
    o.append("".join(f'<path d="M{R(k).uniform(0,W):.0f},{R(k+3).uniform(horizon+8, horizon+130):.0f} h{R(k+5).uniform(30,110):.0f}" stroke="#A8BACA" stroke-width="2.5" opacity="0.6"/>' for k in range(30)))
    o.append(f'<path d="M500,{horizon+30} q200,-6 420,0" stroke="#C8D6E2" stroke-width="18" opacity="0.25"/>')   # dağın yansıması/sis
    # iskele + gemiler
    o.append(f'<path d="M1180,{horizon+92} L1560,{horizon+70}" stroke="{INK}" stroke-width="20"/><path d="M1180,{horizon+92} L1560,{horizon+70}" stroke="#5A4430" stroke-width="12"/>'
             + "".join(f'<path d="M{x},{horizon + 92 - (x-1180)*0.058:.0f} L{x},{horizon + 130 - (x-1180)*0.058:.0f}" stroke="{INK}" stroke-width="9"/>' for x in range(1200, 1560, 60)))
    o.append(longship(1420, horizon + 110, 0.42) + longship(1700, horizon + 96, 0.34, -1) + longship(900, horizon + 60, 0.22))
    # kıyı şeridi (açık kum/çakıl)
    o.append(f'<path d="M0,{horizon+140} Q500,{horizon+120} 960,{horizon+132} Q1400,{horizon+142} {W},{horizon+120} L{W},{horizon+160} L0,{horizon+170} Z" fill="#B8AE98"/>')
    # evler: kıyı boyunca, derinliğe göre ölçek (arkadakiler önce)
    o.append(thatch_house(150, horizon + 150, 0.42, snow=0.6) + thatch_house(1500, horizon + 150, 0.40, snow=0.6, smoke=False)
             + thatch_house(560, horizon + 175, 0.55, snow=0.5) + thatch_house(1220, horizon + 190, 0.60, snow=0.5, light=False))
    o.append(f'<rect x="0" y="{horizon+100}" width="{W}" height="90" fill="#C8D2DC" opacity="0.18"/>')    # ara sis
    o.append(ground(W, H, horizon + 175))
    return "".join(o)


# ======================================================================= v4 (kullanıcı 19.11 20:51)
# Zemin evlerin üstüne çıkıyordu (katman sırası hatası). Zemin artık nesnelerden ÖNCE çizilir ve
# gerçekçi: donmuş çamur, ton kırılımları, tekerlek izi oyukları, buzlu su birikintisi, kirli kar, saman.
MUD_DEFS = ('<defs>'
            '<filter id="mudn" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="0.006 0.022" numOctaves="4" seed="3"/>'
            '<feColorMatrix type="matrix" values="0 0 0 0 0.16  0 0 0 0 0.13  0 0 0 0 0.10  0 0 0 -2.2 1.35"/></filter>'
            '<filter id="mudl" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="0.01 0.04" numOctaves="3" seed="11"/>'
            '<feColorMatrix type="matrix" values="0 0 0 0 0.62  0 0 0 0 0.58  0 0 0 0 0.52  0 0 0 -2.6 1.25"/></filter>'
            '<filter id="grain" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="0.35" numOctaves="2" seed="5"/>'
            '<feColorMatrix type="matrix" values="0 0 0 0 0.1  0 0 0 0 0.08  0 0 0 0 0.06  0 0 0 -1.4 0.75"/></filter>'
            '<linearGradient id="g_mud2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5E584E"/><stop offset="0.3" stop-color="#4E463C"/><stop offset="1" stop-color="#3A3229"/></linearGradient>'
            '<linearGradient id="g_dsnow" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#DCE2E6"/><stop offset="1" stop-color="#A8B0B4"/></linearGradient>'
            '<linearGradient id="g_ice" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#8A9CAC"/><stop offset="0.5" stop-color="#4E5E6C"/><stop offset="1" stop-color="#6E7E8C"/></linearGradient>'
            '</defs>')

def ground2(W=1920, H=1080, y0=700, seed=1):
    gp = f"M0,{y0} Q{W*0.3:.0f},{y0-14} {W*0.5:.0f},{y0-6} Q{W*0.75:.0f},{y0+2} {W},{y0-10} L{W},{H} L0,{H} Z"
    o = [MUD_DEFS, f'<clipPath id="gclip{seed}"><path d="{gp}"/></clipPath>',
         f'<path d="{gp}" fill="url(#g_mud2)"/>',
         f'<g clip-path="url(#gclip{seed})"><rect width="{W}" height="{H}" filter="url(#mudn)"/><rect width="{W}" height="{H}" filter="url(#mudl)" opacity="0.55"/>'
         f'<rect width="{W}" height="{H}" filter="url(#grain)" opacity="0.6"/>']
    # kirli kar: kenarlarda, çamurla karışık; içine çamur benekleri
    rr = R(seed)
    for (cx, cy, rx, ry) in ((W*0.08, y0+40, W*0.16, 34), (W*0.93, y0+50, W*0.14, 40), (W*0.24, H-60, W*0.18, 60), (W*0.88, H-40, W*0.15, 50)):
        pts = []
        for i in range(14):
            a = i / 14 * 2 * math.pi; k_ = rr.uniform(0.75, 1.15)
            pts.append((cx + rx * k_ * math.cos(a), cy + ry * k_ * math.sin(a)))
        d = "M" + " ".join(f"{x:.0f},{y:.0f}" for x, y in pts) + " Z"
        o.append(f'<path d="{d}" fill="url(#g_dsnow)" opacity="0.92"/><path d="{d}" fill="none" stroke="#6E6A60" stroke-width="5" opacity="0.6"/>')
        o.append("".join(f'<ellipse cx="{cx + rr.uniform(-rx, rx)*0.8:.0f}" cy="{cy + rr.uniform(-ry, ry)*0.6:.0f}" rx="{rr.uniform(4, 14):.0f}" ry="{rr.uniform(2, 5):.0f}" fill="#5A5044" opacity="0.6"/>' for _ in range(16)))
    # patika: daha koyu, ıslak çamur; tekerlek izi oyukları (gölge + ışıklı kenar)
    rd = f"M{W*0.30:.0f},{H} Q{W*0.44:.0f},{y0+170} {W*0.57:.0f},{y0+4} L{W*0.65:.0f},{y0+4} Q{W*0.70:.0f},{y0+180} {W*0.84:.0f},{H} Z"
    o.append(f'<path d="{rd}" fill="#2E2820" opacity="0.55"/>')
    for off in (0.32, 0.68):
        xa, xb, xc = W*(0.30 + off*0.54), W*(0.44 + off*0.26), W*(0.57 + off*0.08)
        o.append(f'<path d="M{xa:.0f},{H} Q{xb:.0f},{y0+170} {xc:.0f},{y0+6}" stroke="#1E1A14" stroke-width="22" fill="none" opacity="0.75"/>'
                 f'<path d="M{xa+14:.0f},{H} Q{xb+10:.0f},{y0+170} {xc+3:.0f},{y0+6}" stroke="#8A8274" stroke-width="4" fill="none" opacity="0.55"/>')
    # buzlu su birikintileri (koyu yansıma + buz kenarı)
    for (px, py, rx) in ((W*0.50, y0+180, 90), (W*0.70, y0+300, 120), (W*0.60, y0+60, 46)):
        o.append(f'<ellipse cx="{px:.0f}" cy="{py:.0f}" rx="{rx}" ry="{rx*0.2:.0f}" fill="url(#g_ice)" stroke="#2A241C" stroke-width="4"/>'
                 f'<path d="M{px-rx*0.7:.0f},{py-rx*0.04:.0f} q{rx*0.3:.0f},{-rx*0.05:.0f} {rx*0.7:.0f},0 M{px+rx*0.1:.0f},{py+rx*0.06:.0f} l{rx*0.3:.0f},{-rx*0.03:.0f}" stroke="#D8E2EA" stroke-width="3" fill="none" opacity="0.75"/>')
    # yarı gömülü taşlar (toprakla aynı tonda, üst kenarı ışıklı)
    for k in range(26):
        r_ = R(k + 900 + seed); x = r_.uniform(0, W); y = r_.uniform(y0 + 30, H - 20); s_ = r_.uniform(8, 22) * (0.5 + (y - y0) / 500)
        o.append(f'<path d="M{x-s_:.0f},{y:.0f} Q{x-s_*0.8:.0f},{y-s_*0.7:.0f} {x:.0f},{y-s_*0.75:.0f} Q{x+s_*0.9:.0f},{y-s_*0.6:.0f} {x+s_:.0f},{y:.0f} Z" fill="#6E685E" stroke="#2A241C" stroke-width="3"/>'
                 f'<path d="M{x-s_*0.6:.0f},{y-s_*0.55:.0f} Q{x:.0f},{y-s_*0.85:.0f} {x+s_*0.6:.0f},{y-s_*0.5:.0f}" stroke="#A8A296" stroke-width="2.5" fill="none"/>')
    # saman ve kuru ot (dağınık), çiğnenmiş kenarlar
    for k in range(90):
        r_ = R(k + 1500 + seed); x = r_.uniform(0, W); y = r_.uniform(y0 + 10, H); a = r_.uniform(-0.6, 0.6); l = r_.uniform(8, 20)
        o.append(f'<path d="M{x:.0f},{y:.0f} l{l*math.cos(a):.0f},{l*math.sin(a):.0f}" stroke="{["#8A7A50", "#6E6040", "#A08C5A"][k % 3]}" stroke-width="2" opacity="0.8"/>')
    for k in range(30):
        r_ = R(k + 2000 + seed); x = r_.uniform(0, W); y = r_.uniform(y0 + 5, H)
        if W * 0.30 < x < W * 0.84 and y > y0 + 40: continue
        o.append("".join(f'<path d="M{x + j*4:.0f},{y:.0f} q{(j-1)*3},-9 {(j-1)*6},-{12 + j*3}" stroke="#6E6A48" stroke-width="3" fill="none" stroke-linecap="round"/>' for j in range(3)))
    o.append('</g>')
    o.append(f'<path d="M0,{y0} Q{W*0.3:.0f},{y0-14} {W*0.5:.0f},{y0-6} Q{W*0.75:.0f},{y0+2} {W},{y0-10}" stroke="#2A241C" stroke-width="4" fill="none" opacity="0.6"/>')
    return "".join(o)

def kattegat4(W=1920, H=1080, horizon=560):
    """kattegat3 + doğru katman sırası (zemin → evler) + gerçekçi zemin."""
    src = kattegat3(W, H, horizon)
    houses_at = src.index('<g transform="translate(150,')
    sky_lake = src[:houses_at]
    rest = src[houses_at:]
    houses = rest[:rest.index('<rect x="0" y="' + str(horizon + 100) + '"')]
    return sky_lake + ground2(W, H, horizon + 150) + houses + f'<rect x="0" y="{horizon+100}" width="{W}" height="70" fill="#C8D2DC" opacity="0.12"/>'

# ---- sert iklim eşeği: kışlık uzun tüy, koyu ve soluk renkler, gerçekçi oran, yorgun baş duruşu, çamurlu bacaklar
def donkey_rough(s=1.0, harness=True, head_drop=14):
    coat, coat_d, belly, mud = "#5E564C", "#3E3830", "#8E8678", "#3A3024"
    o = [f'<g filter="url(#f_form)">']
    def leg(pts, w0, w1, col):
        out = _leg(pts, w0, w1, col, hoof="#1E1A16")
        (x1, y1), (x2, y2) = pts[-2], pts[-1]   # alt bacakta çamur
        return out + f'<path d="M{(x1+x2)/2:.0f},{(y1+y2)/2:.0f} L{x2},{y2-14}" stroke="{mud}" stroke-width="{w1+2}" stroke-linecap="round" opacity="0.85"/>'
    o.append(leg([(-120, -122), (-140, -60), (-126, 0)], 34, 18, coat_d) + leg([(80, -124), (84, -60), (88, 0)], 30, 18, coat_d))
    body = ("M122,-200 Q110,-246 52,-248 Q-40,-244 -116,-240 Q-180,-240 -200,-196 Q-214,-146 -182,-112 Q-150,-92 -110,-96 "
            "Q-40,-86 44,-96 Q98,-98 122,-126 Q138,-162 122,-200 Z")
    o.append(f'<path d="{body}" fill="{coat}" {T("kurk", s)}/>')
    neck = "M44,-244 Q90,-278 136,-300 Q160,-310 176,-296 Q180,-262 166,-232 Q150,-198 136,-170 Q126,-150 120,-134 Q100,-190 44,-244 Z"
    o.append(f'<path d="{neck}" fill="{coat}" {T("kurk", s)}/>')
    o.append('</g>')
    # baş: büyük, uzun, hafif aşağı eğik (yorgun)
    o.append(f'<g transform="rotate({head_drop} 160 -300)">')
    head = "M148,-312 Q172,-334 202,-322 Q244,-298 278,-246 Q292,-218 274,-198 Q256,-184 228,-192 Q204,-198 186,-222 Q166,-244 152,-266 Q136,-290 148,-312 Z"
    o.append(f'<g filter="url(#f_form)"><path d="{head}" fill="{coat}" {T("kurk", s)}/></g><path d="{head}" fill="none" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>')
    o.append(f'<path d="M238,-268 Q276,-232 278,-210 Q270,-190 240,-194 Q218,-200 210,-224 Q220,-254 238,-268 Z" fill="{belly}" stroke="{INK}" stroke-width="4" opacity="0.95"/>'
             f'<path d="M258,-236 q6,4 8,10" stroke="{INK}" stroke-width="4" fill="none" stroke-linecap="round"/><path d="M244,-198 q14,3 24,-2" stroke="{INK}" stroke-width="3.5" fill="none"/>')
    o.append(f'<path d="M184,-286 q12,-6 24,2 q-10,8 -24,-2 Z" fill="#14100C" stroke="{INK}" stroke-width="2.5"/><path d="M182,-292 q14,-8 30,0" stroke="{coat_d}" stroke-width="5" fill="none" stroke-linecap="round"/>')   # küçük, çökük göz
    for (bx, by, tx, ty, c_) in ((154, -312, 112, -398, coat_d), (168, -316, 150, -408, coat)):   # kulaklar (biraz yana yatık)
        o.append(f'<path d="M{bx-10},{by} Q{tx-12},{(by+ty)/2:.0f} {tx},{ty} Q{tx+16},{(by+ty)/2:.0f} {bx+12},{by+4} Z" fill="{c_}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
                 f'<path d="M{bx-2},{by-8} Q{tx},{(by+ty)/2:.0f} {tx+3},{ty+18}" stroke="#7E766A" stroke-width="5" fill="none" stroke-linecap="round"/>'
                 f'<path d="M{tx-3},{ty+2} q6,-4 9,3" stroke="#14100C" stroke-width="5" fill="none"/>')
    if harness:
        o.append(f'<path d="M206,-296 Q236,-280 262,-252 M196,-236 Q216,-252 232,-282" stroke="#3A2614" stroke-width="7" fill="none"/>')
    o.append('</g>')
    o.append(f'<path d="{body}" fill="none" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/><path d="{neck}" fill="none" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>')
    # kışlık tüy: kontur boyunca kısa kaba tüy darbeleri + karın altında sarkan tüy
    rr = R(77)
    for k in range(70):
        t = k / 70; x = -196 + 316 * t; y = -110 + 10 * math.sin(t * 6)
        o.append(f'<path d="M{x:.0f},{y:.0f} l{rr.uniform(-3, 3):.0f},{rr.uniform(8, 16):.0f}" stroke="{coat_d}" stroke-width="3" stroke-linecap="round"/>')
    for k in range(60):
        x = rr.uniform(-180, 110); y = rr.uniform(-236, -120)
        o.append(f'<path d="M{x:.0f},{y:.0f} l{rr.uniform(-4, 4):.0f},{rr.uniform(6, 12):.0f}" stroke="{["#4A443A", "#7A7266"][k % 2]}" stroke-width="2.5" opacity="0.7" stroke-linecap="round"/>')
    o.append(f'<path d="M-150,-112 Q-60,-98 60,-104 Q92,-108 110,-124" stroke="{belly}" stroke-width="12" fill="none" stroke-linecap="round" opacity="0.5"/>')
    o.append(f'<path d="M150,-304 Q100,-276 48,-246 Q-40,-240 -156,-238 Q-188,-230 -198,-206" stroke="#2A241E" stroke-width="8" fill="none" stroke-linecap="round"/>'
             f'<path d="M66,-246 Q74,-206 70,-166" stroke="#2A241E" stroke-width="7" fill="none" stroke-linecap="round"/>')
    o.append("".join(f'<path d="M{150 - k*12:.0f},{-304 + k*7:.0f} l{-8 - (k % 2) * 4},{-18 + (k % 3) * 5}" stroke="#2A241E" stroke-width="7" stroke-linecap="round"/>' for k in range(9)))   # dağınık yele
    o.append(f'<path d="M-196,-216 Q-222,-160 -212,-110" stroke="{INK}" stroke-width="14" fill="none" stroke-linecap="round"/><path d="M-196,-216 Q-222,-160 -212,-110" stroke="{coat}" stroke-width="7" fill="none" stroke-linecap="round"/>'
             f'<path d="M-212,-118 q-14,20 -4,46 q8,-8 14,0 q4,-26 -10,-46 Z" fill="#2A241E" stroke="{INK}" stroke-width="4"/>')
    o.append(leg([(-156, -128), (-176, -60), (-158, 0)], 44, 20, coat) + leg([(100, -126), (106, -60), (108, 0)], 34, 19, coat))
    if harness:   # yıpranmış deri koşum + kaba keçe semer
        o.append(f'<path d="M-40,-246 Q20,-262 70,-244 L64,-206 Q10,-222 -36,-212 Z" fill="#4A4036" stroke="{INK}" stroke-width="5" {T("kurk", s)}/>'
                 f'<path d="M112,-152 Q130,-200 116,-242 Q100,-256 84,-240 Q100,-204 92,-152 Z" fill="#3E2A18" stroke="{INK}" stroke-width="5" {T("deri", s)}/>'
                 f'<path d="M104,-172 Q20,-162 -60,-172" stroke="{INK}" stroke-width="12" fill="none"/><path d="M104,-172 Q20,-162 -60,-172" stroke="#4A3220" stroke-width="7" fill="none"/>'
                 f'<path d="M16,-214 Q20,-160 12,-100" stroke="{INK}" stroke-width="12" fill="none"/><path d="M16,-214 Q20,-160 12,-100" stroke="#4A3220" stroke-width="7" fill="none"/>'
                 f'<circle cx="106" cy="-174" r="7" fill="#6E6A60" stroke="{INK}" stroke-width="3"/>')
    o.append(f'<ellipse cx="-30" cy="4" rx="230" ry="16" fill="#000" opacity="0.25"/>')
    return f'<g transform="scale({s})">' + "".join(o) + '</g>'

def cart_rough(trunks=True):
    """Yıpranmış ağır yük arabası: koyu, eğri tahtalar, çamurlu tekerlekler, aşınmış demir."""
    src = cart(trunks)
    src = (src.replace("#8A6A48", "#5E4A36").replace("#6A4E34", "#4A3A2A").replace("#7A5A3A", "#4E3C2A")
              .replace("#6A4A30", "#4A3828").replace("#5A3E28", "#3E3022").replace("#9A8A70", "#6E6252")
              .replace("#B08A3A", "#7A6A4A").replace("#5A5A58", "#4A4644").replace("#A8865E", "#6E5A44").replace("#C8B08A", "#8A7A5E"))
    mud = "".join(f'<path d="M{cx-60},{-30} Q{cx},{-4} {cx+60},{-30}" stroke="#3A3024" stroke-width="18" fill="none" opacity="0.8" stroke-linecap="round"/>' for cx in (-120, 70))
    return src + mud

def donkey_cart_rough(x, y, s=1.0):
    return f'<g transform="translate({x},{y}) scale({s})"><g transform="translate(-160,0)">{cart_rough()}</g><g transform="translate(330,0) scale(0.92)">{donkey_rough()}</g></g>'
