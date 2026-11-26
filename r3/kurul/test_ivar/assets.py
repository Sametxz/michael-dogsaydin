"""Nesne kartları v2: bebek Ivar (kundak) ve Ragnar'ın kolu, eli ve kol halkası.

v1'den sonra kurulun (G1, G2, G3) düzeltmeleri uygulandı:
- Bebek yüzü en geniş yanakta; pembe leke, plastik parlama ve kirpik çıkarıldı.
- Kundakta örgü ilmekleri, sarma kanadı, ayak çıkıntısı ve hacim gölgesi var. leg_out varyantı eklendi.
- Kol halkası arka ve ön yay olarak iki katmanlı, üç tonlu altın. Dövme art3.knot_mark ile çiziliyor.
- Bilekte basamak yok, tırnaklar eklendi. Dokular ölçekten bağımsız (tex.scaled). Form ışığı tex.form ile veriliyor.
"""
import sys, subprocess, math
sys.path[:0] = ["/home/claude/r3", "/home/claude/r2"]
import tex
from art3 import knot_mark, forearm_band
INK = "#1A1410"
SKIN_B = "#F2D0B2"; SKIN_B2 = "#DDA88A"; SKIN_B3 = "#C98A70"
BLANKET = "#4A5870"; BLANKET_L = "#62728C"; BLANKET_D = "#2C3646"; KNIT = "#B49C6C"; KNIT_D = "#6A5838"
RAG_SKIN = "#E8C29C"; RAG_SKIN2 = "#B98864"; TUNIC = "#3E4A42"
BABY_REL = 0.75          # bebek, kola göre bu ölçekte (kafa ≈ 0,66 × el uzunluğu)
FIST = (-178, -14)       # bebek yerel koordinatında yumruk merkezi (hand="grip"/"up")


def defs(s=1.0, az=225):
    """Nesnelerin kullandığı tüm filtreler. s = nesnenin ekrandaki toplam ölçeği."""
    out = []
    for n in ("orgu", "keten", "cilt"):
        out.append(tex.scaled(n, s)[0])
    out.append(tex.form("t_form", blur=16 * s, scale=8, az=az))
    out.append(tex.form("t_form_s", blur=7 * s, scale=6, az=az))
    out.append(tex.form("t_form_h", blur=22 * s, scale=14, az=az, el=40, gain=1.25))
    out.append(tex.knit_pattern("p_knit", "#0E1520", 0.32, 16 * s, 13 * s, -20))
    out.append(tex.knit_pattern("p_knit2", "#0E1520", 0.28, 16 * s, 13 * s, 35))
    out.append(f'<linearGradient id="g_blk" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{BLANKET_L}"/><stop offset="0.55" stop-color="{BLANKET}"/><stop offset="1" stop-color="{BLANKET_D}"/></linearGradient>')
    out.append(f'<radialGradient id="g_red" cx="0.5" cy="0.45" r="0.5"><stop offset="0" stop-color="#E07A6A" stop-opacity="0.38"/><stop offset="1" stop-color="#E07A6A" stop-opacity="0"/></radialGradient>')
    out.append('<radialGradient id="g_bloom" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#FFF8EE" stop-opacity="0.2"/><stop offset="1" stop-color="#FFF8EE" stop-opacity="0"/></radialGradient>')
    return "<defs>" + "".join(out) + "</defs>"


def T(name, s):
    return f'filter="url(#{tex.scaled(name, s)[1]})"'


def _knit_fill(d, sw=None, pat="p_knit"):
    """Kumaş: degrade dolgu + ilmek deseni + kontur."""
    return (f'<path d="{d}" fill="url(#g_blk)"/>'
            f'<path d="{d}" fill="url(#{pat})"/>'
            f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{sw}" stroke-linejoin="round"/>')


# ------------------------------------------------------------------ bebek
FACE = ("M0,-118 C-58,-120 -98,-84 -102,-34 C-114,18 -110,62 -80,88 "
        "C-50,110 30,112 70,90 C108,66 114,14 102,-38 C92,-86 56,-118 0,-118 Z")

def baby(cry=False, hand="rest", leg_out=False, s=1.0, lw=7, awake=False):
    """Kundaklı bebek, ¾. Yerel: baş merkezi (0,0), kafa uzunluğu ≈ 230.

    hand: "rest" (el kundakta), "up" (kalkık, açık yumruk), "grip" (parmak kavrıyor; ön parmaklar
    baby_grip_front() ile parmağın ÜSTÜNE ayrıca çizilir). s: ekran ölçeği (doku/form için).
    lw: kontur kalınlığı ekran pikselinde sabit kalsın diye çağıran LW/scale verir.
    """
    o = []
    # 1) kundak gövdesi (başın arkasından sağ alta), alt katman
    body = ("M-150,30 Q-196,170 -70,252 Q100,332 300,262 Q372,236 402,176 "
            "Q430,110 392,62 Q340,8 240,-4 Q120,-16 30,50 Z")
    o.append(f'<g filter="url(#t_form)">{_knit_fill(body, lw)}</g>')
    # ayak çıkıntısı (uçta, kundak içinde topuk şişkinliği)
    o.append(f'<path d="M352,214 Q404,226 420,190 Q430,150 398,126" fill="none" stroke="{INK}" stroke-width="{lw*0.8}" stroke-linecap="round"/>')
    # sarma kanadı: kapüşondan sağ alta çapraz, kendi konturu
    flap = "M-120,60 Q20,40 170,96 Q300,150 384,214 Q300,284 150,270 Q20,250 -60,200 Q-110,150 -120,60 Z"
    o.append(f'<g filter="url(#t_form_s)">{_knit_fill(flap, lw, "p_knit2")}</g>')
    # kıvrımlar: gölge (multiply) + sırt (ışık tarafı) çifti
    for d in ("M-70,170 Q40,214 190,206", "M10,120 Q120,150 250,150", "M150,40 Q240,70 330,80"):
        o.append(f'<path d="{d}" stroke="{BLANKET_D}" stroke-width="{lw}" fill="none" stroke-linecap="round" opacity="0.9"/>')
        o.append(f'<path d="{d}" stroke="{BLANKET_L}" stroke-width="{lw*0.55}" fill="none" stroke-linecap="round" transform="translate(-4,-8)" opacity="0.9"/>')
    # Aslaug'un örgü şeridi: sarma kanadının kenarı boyunca (sabit motif: örgü + çapraz şerit)
    o.append(f'<path d="M-112,70 Q20,52 168,106 Q296,158 376,218" stroke="{KNIT}" stroke-width="18" fill="none" {T("orgu", s)}/>')
    o.append(f'<path d="M-112,70 Q20,52 168,106 Q296,158 376,218" stroke="{KNIT_D}" stroke-width="18" fill="none" stroke-dasharray="4 12" opacity="0.65"/>')
    if leg_out:  # ivar_2.3: kundağın ucundan çıkan ince, içe dönük bacak
        o.append(f'<path d="M372,236 Q420,282 404,330 Q396,352 368,350" fill="none" stroke="{INK}" stroke-width="{30+lw*2}" stroke-linecap="round"/>'
                 f'<path d="M372,236 Q420,282 404,330 Q396,352 368,350" fill="none" stroke="{SKIN_B}" stroke-width="30" stroke-linecap="round"/>'
                 f'<path d="M352,346 q-30,4 -36,-14 q10,-16 40,-8" fill="{SKIN_B}" stroke="{INK}" stroke-width="{lw*0.8}" stroke-linejoin="round"/>'
                 f'<path d="M398,300 q-10,8 -20,4" stroke="{SKIN_B2}" stroke-width="3.5" fill="none"/>')
    # 2) kapüşon (başın arkası): yüzü saran, yüzden 25–45 px taşan
    hood = "M-150,60 Q-210,-120 -60,-186 Q90,-222 168,-104 Q206,-30 164,64 Q110,108 40,112 Q-70,118 -150,60 Z"
    o.append(f'<g filter="url(#t_form)">{_knit_fill(hood, lw)}</g>')
    # kapüşonun iç gölgesi (yüzün arkasındaki boşluk)
    o.append(f'<path d="M-118,20 Q-140,-96 -30,-138 Q90,-160 132,-60 Q146,-10 128,40" fill="{BLANKET_D}" stroke="none" opacity="0.85"/>')
    # 3) yüz: form ışıklı, en geniş yanakta
    o.append(f'<g filter="url(#t_form)"><path d="{FACE}" fill="{SKIN_B}"/></g>')
    o.append(f'<ellipse cx="-34" cy="-58" rx="70" ry="44" fill="url(#g_bloom)"/>')     # yumuşak alın ışığı (a ≤ 0,2)
    if cry:
        o.append('<ellipse cx="-6" cy="4" rx="96" ry="62" fill="url(#g_red)"/>')
    o.append(f'<path d="{FACE}" fill="none" stroke="{INK}" stroke-width="{lw}"/>')
    o.append(f'<path d="M-34,92 Q-6,104 24,90" stroke="{SKIN_B2}" stroke-width="4" fill="none" stroke-linecap="round"/>')  # çene boğumu
    o.append(f'<path d="M-56,-110 q10,-14 24,-6 M-16,-114 q8,-16 22,-4" stroke="#8A6A42" stroke-width="4" fill="none" stroke-linecap="round"/>')  # ince saç
    if cry:
        o.append(f'<path d="M-30,-60 q10,-8 22,-2 M8,-62 q12,-6 22,2" stroke="{SKIN_B3}" stroke-width="3.5" fill="none" stroke-linecap="round"/>')  # iç uçları kalkık alın
        o.append(f'<path d="M-70,-14 Q-52,-2 -34,-12 M14,-12 Q32,-2 50,-14" stroke="{INK}" stroke-width="5.5" fill="none" stroke-linecap="round"/>'
                 f'<path d="M-72,-20 q-8,-4 -12,-10 M-72,-8 q-10,2 -14,0 M52,-20 q8,-4 12,-10 M52,-8 q10,2 14,0 M-64,-24 Q-50,-30 -36,-22 M18,-22 Q32,-30 46,-24" stroke="{SKIN_B3}" stroke-width="3" fill="none" stroke-linecap="round"/>')  # sıkılmış kapak + kırışık
        o.append(f'<path d="M-22,48 Q0,42 22,48 Q24,68 12,78 Q0,82 -12,78 Q-24,68 -22,48 Z" fill="#5A2026" stroke="{INK}" stroke-width="4.5" stroke-linejoin="round"/>'
                 f'<path d="M-10,72 q10,-4 20,0" stroke="#A85058" stroke-width="4" fill="none"/>')  # kare-yamuk ağız
        o.append('<path d="M-74,4 q-6,22 -2,40 q6,8 10,0 q2,-16 -8,-40 Z" fill="#CFE4F2" stroke="#6C8AA0" stroke-width="2.5" opacity="0.9"/>')  # tek gözyaşı
    elif awake:  # Ragnar'a (sol üste) bakan, açık iri gözler; ağız hafif aralık
        for ex in (-50, 30):
            o.append(f'<ellipse cx="{ex}" cy="-10" rx="15" ry="17" fill="#F6F2EE" stroke="{INK}" stroke-width="3.5"/>'
                     f'<ellipse cx="{ex-5}" cy="-14" rx="11" ry="12" fill="#3A4A5C"/><circle cx="{ex-8}" cy="-19" r="4" fill="#FFFFFF"/>'
                     f'<path d="M{ex-16},-30 q16,-8 32,0" stroke="{SKIN_B2}" stroke-width="3" fill="none" stroke-linecap="round"/>')
        o.append(f'<ellipse cx="-2" cy="60" rx="9" ry="8" fill="#6A3238" stroke="{INK}" stroke-width="3.5"/><path d="M-6,64 q4,2 8,0" stroke="#B0606A" stroke-width="2.5" fill="none"/>')  # hayretle yarı açık
    else:
        o.append(f'<path d="M-66,-12 q16,10 32,0 M14,-12 q16,10 32,0" stroke="{INK}" stroke-width="5" fill="none" stroke-linecap="round"/>')
        o.append(f'<path d="M-66,-24 q16,-6 32,0 M14,-24 q16,-6 32,0" stroke="{SKIN_B2}" stroke-width="3" fill="none" stroke-linecap="round"/>')  # şişkin kapak kıvrımı
        o.append(f'<path d="M-18,56 Q-4,62 10,56" stroke="{INK}" stroke-width="4.5" fill="none" stroke-linecap="round"/>')
    o.append(f'<path d="M-10,14 Q-2,30 12,22" stroke="{SKIN_B3}" stroke-width="4.5" fill="none" stroke-linecap="round"/>')  # minik burun
    # 4) Aslaug'un örgü kenar bandı: yüz çevresinde, yüz konturunu hafifçe örter
    band = "M-124,40 Q-150,-40 -118,-96 Q-84,-140 -30,-140 Q20,-150 70,-128 Q128,-100 138,-40 Q148,10 128,56"
    o.append(f'<path d="{band}" stroke="{INK}" stroke-width="{15+lw}" fill="none" stroke-linecap="round"/>'
             f'<path d="{band}" stroke="{KNIT}" stroke-width="15" fill="none" stroke-linecap="round" {T("orgu", s)}/>'
             f'<path d="{band}" stroke="{KNIT_D}" stroke-width="15" fill="none" stroke-dasharray="3 9" opacity="0.6"/>'
             f'<path d="{band}" stroke="#F0D79A" stroke-width="4" fill="none" transform="translate(-3,-6)" opacity="0.55"/>')
    # 5) el
    if hand in ("up", "grip"):
        fx, fy = FIST
        arm_d = f"M-118,64 Q-150,40 {fx+14},{fy+26}"
        o.append(f'<path d="{arm_d}" stroke="{INK}" stroke-width="{62+lw*2}" fill="none" stroke-linecap="round"/>'
                 f'<path d="{arm_d}" stroke="{SKIN_B}" stroke-width="62" fill="none" stroke-linecap="round"/>'
                 f'<path d="M-112,82 Q-150,62 {fx+24},{fy+46}" stroke="{SKIN_B2}" stroke-width="12" fill="none" stroke-linecap="round" opacity="0.7"/>')
        o.append(f'<path d="M-140,30 q14,-6 22,8 M-158,8 q12,-4 20,8" stroke="{SKIN_B2}" stroke-width="4" fill="none" stroke-linecap="round"/>')  # iki bilek boğumu
        # kundak ağzı (kol, kanadın altından çıkıyor)
        o.append(f'<path d="M-140,92 Q-120,40 -86,58" stroke="{BLANKET_D}" stroke-width="{lw+6}" fill="none" stroke-linecap="round"/>')
        if hand == "up":
            o.append(_fist(fx, fy, lw, closed=True))
        else:
            o.append(f'<g transform="translate({fx},{fy})"><ellipse rx="44" ry="38" fill="{SKIN_B2}" stroke="{INK}" stroke-width="{lw}"/>'
                     f'<path d="M-30,20 q-20,-4 -18,-26 q12,-6 22,8" fill="{SKIN_B}" stroke="{INK}" stroke-width="{lw*0.75}"/></g>')  # avuç (parmağın arkası)
    o.append('<g/>')
    return "".join(o)


def _fist(x, y, lw, closed=True):
    """Bebek yumruğu: 4 kısa parmak yumruğun ÖN yüzünde, başparmak içe kıvrık."""
    o = [f'<g transform="translate({x},{y}) rotate(-20)">',
         f'<ellipse rx="42" ry="36" fill="{SKIN_B}" stroke="{INK}" stroke-width="{lw}"/><path d="M-30,24 Q0,40 34,18" stroke="{SKIN_B2}" stroke-width="8" fill="none" opacity="0.7"/>']
    for k in range(4):
        cx = -24 + k * 15
        o.append(f'<path d="M{cx-7},-14 q7,-12 14,0 q2,12 -7,16 q-9,-4 -7,-16 Z" fill="{SKIN_B}" stroke="{INK}" stroke-width="{lw*0.6}"/>')
    o.append(f'<path d="M-36,10 q4,-16 22,-12" stroke="{INK}" stroke-width="{lw*0.6}" fill="none" stroke-linecap="round"/>')  # içe kıvrık başparmak
    o.append('</g>')
    return "".join(o)


def baby_grip_front(lw=7):
    """Kavrayan minik parmaklar: Ragnar'ın parmağının ÜSTÜNE çizilir (bebek yerel koordinatı)."""
    fx, fy = FIST
    o = [f'<g transform="translate({fx},{fy})">']
    for k in range(4):
        cx = -30 + k * 18
        o.append(f'<path d="M{cx-8},-34 Q{cx-10},-4 {cx-4},22 Q{cx+4},30 {cx+9},20 Q{cx+10},-6 {cx+8},-34 Z" fill="{SKIN_B}" stroke="{INK}" stroke-width="{lw*0.65}" stroke-linejoin="round"/>'
                 f'<path d="M{cx-4},4 q5,3 10,0" stroke="{SKIN_B2}" stroke-width="2.5" fill="none"/>')
    o.append(f'<path d="M-46,-30 Q-58,-10 -44,8" stroke="{SKIN_B2}" stroke-width="5" fill="none" stroke-linecap="round" opacity="0.8"/>')  # yumruk kenarı gölgesi
    o.append('</g>')
    return "".join(o)


# ------------------------------------------------------------------ Ragnar'ın kolu
RING = (330, -36, 34, 72)   # merkez x, y, rx, ry (dış yükseklik ≈ 1,25 × önkol kalınlığı)

def _ring_arc(back, lw):
    cx, cy, rx, ry = RING
    d = f"M0,{-ry} A{rx},{ry} 0 0 1 0,{ry}" if back else f"M0,{ry} A{rx},{ry} 0 0 1 0,{-ry}"
    o = [f'<g transform="translate({cx},{cy})">']
    k = 0.62 if back else 1.0
    def sh(hexc):
        r, g, b = (int(hexc[i:i + 2], 16) for i in (1, 3, 5))
        return "#%02X%02X%02X" % (int(r * k), int(g * k), int(b * k))
    o.append(f'<path d="{d}" stroke="{INK}" stroke-width="{26+lw*1.4}" fill="none" stroke-linecap="round"/>')
    o.append(f'<path d="{d}" stroke="{sh("#6A4A12")}" stroke-width="26" fill="none" stroke-linecap="round"/>')   # koyu öz
    o.append(f'<path d="{d}" stroke="{sh("#C9952E")}" stroke-width="15" fill="none" stroke-linecap="round" transform="translate(-2,-2)"/>')  # orta
    if not back:
        # burgu: eğimli spiral bantlar (koyu + parlak çift)
        for j in range(1, 12):
            a = math.pi / 2 + j * math.pi / 12
            x, y = rx * math.cos(a), ry * math.sin(a)
            o.append(f'<path d="M{x-9:.1f},{y-10:.1f} l16,14" stroke="#5A3C0C" stroke-width="5" stroke-linecap="round"/>'
                     f'<path d="M{x-4:.1f},{y-14:.1f} l14,12" stroke="#F2CF7A" stroke-width="3" stroke-linecap="round" opacity="0.9"/>')
        o.append(f'<path d="M{-rx*0.55:.0f},{-ry*0.86:.0f} Q{-rx-4},{-ry*0.3:.0f} {-rx-2},{ry*0.05:.0f}" stroke="#FFF2C0" stroke-width="6" fill="none" stroke-linecap="round"/>')   # keskin specular
        o.append(f'<path d="M{-rx+2},{ry*0.35:.0f} Q{-rx+4},{ry*0.75:.0f} {-rx*0.4:.0f},{ry*0.93:.0f}" stroke="#9EB6CC" stroke-width="4" fill="none" stroke-linecap="round" opacity="0.85"/>')  # soğuk ortam yansıması
    o.append('</g>')
    return "".join(o)


def arm(index_out=True, s=1.0, lw=7, sleeve=True):
    """Ragnar'ın sol önkolu ve eli. Yerel: dirsek (0,0), bilek ≈ (460,-36), işaret ucu ≈ (722,-46)."""
    o = []
    if sleeve:
        sl = "M-260,-60 Q-80,-120 120,-112 L132,34 Q-60,42 -260,112 Z"
        o.append(f'<g filter="url(#t_form)"><path d="{sl}" fill="{TUNIC}" {T("keten", s)}/></g><path d="{sl}" fill="none" stroke="{INK}" stroke-width="{lw}"/>')
        o.append(f'<path d="M-220,-30 Q-80,-70 100,-82 M-200,40 Q-60,12 110,2" stroke="#232B26" stroke-width="6" fill="none" opacity="0.8"/>'
                 f'<path d="M-214,-40 Q-80,-80 96,-92" stroke="#58665C" stroke-width="3" fill="none" opacity="0.8"/>')
    o.append(_ring_arc(True, lw))                                  # halkanın arka yayı (kolun arkasında)
    # --- el (önkoldan önce: bilek basamağı oluşmasın)
    palm = "M430,-90 Q520,-114 584,-86 Q624,-56 606,-4 Q566,38 470,26 Q440,20 430,10 Z"
    o.append(f'<g filter="url(#t_form_h)"><path d="{palm}" fill="{RAG_SKIN}" {T("cilt", s)}/></g><path d="{palm}" fill="none" stroke="{INK}" stroke-width="{lw}"/>')
    for (y0, ln, wd) in ((-22, 74, 26), (4, 66, 24), (28, 54, 21)):   # kıvrık parmaklar: konik, iki boğumlu, yuvarlak uçlu
        a = (588, y0 + 6); b = (596 + ln * 0.62, y0 + 2); tip = (596 + ln * 0.78, y0 + 26)
        seg1 = f"M{a[0]},{a[1]} Q{b[0]-10:.0f},{y0-2} {b[0]:.0f},{b[1]+4}"
        seg2 = f"M{b[0]:.0f},{b[1]+4} Q{b[0]+16:.0f},{y0+10} {tip[0]:.0f},{tip[1]}"
        for d_, w_ in ((seg1, wd), (seg2, wd * 0.82)):
            o.append(f'<path d="{d_}" stroke="{INK}" stroke-width="{w_+lw*1.7:.1f}" fill="none" stroke-linecap="round"/>')
        for d_, w_ in ((seg1, wd), (seg2, wd * 0.82)):
            o.append(f'<path d="{d_}" stroke="{RAG_SKIN}" stroke-width="{w_:.1f}" fill="none" stroke-linecap="round"/>')
        o.append(f'<path d="M{b[0]-4:.0f},{b[1]-6:.0f} q6,6 4,14" stroke="{RAG_SKIN2}" stroke-width="2.5" fill="none" opacity="0.8"/>'   # boğum kıvrımı
                 f'<path d="M{tip[0]-12:.0f},{tip[1]+2} q8,6 14,-2" stroke="#C8A088" stroke-width="5" fill="none" stroke-linecap="round"/>'  # tırnak
                 f'<path d="M{a[0]+6},{a[1]+wd*0.35:.0f} Q{b[0]:.0f},{b[1]+wd*0.5:.0f} {tip[0]-6:.0f},{tip[1]+wd*0.3:.0f}" stroke="{RAG_SKIN2}" stroke-width="5" fill="none" opacity="0.45" stroke-linecap="round"/>')  # alt gölge
    if index_out:
        ix = "M588,-66 Q646,-74 690,-56 Q722,-44 724,-22 Q718,-8 702,-14 Q690,-30 660,-34 Q626,-34 594,-32 Z"
        o.append(f'<g filter="url(#t_form_s)"><path d="{ix}" fill="{RAG_SKIN}"/></g><path d="{ix}" fill="none" stroke="{INK}" stroke-width="{lw}" stroke-linejoin="round"/>')
        o.append(f'<path d="M704,-46 Q720,-40 720,-26 Q710,-28 702,-36 Z" fill="#E6C2AC" stroke="#9A7258" stroke-width="2.5"/>')  # işaret tırnağı
        o.append(f'<path d="M640,-64 q2,14 0,28 M668,-62 q2,12 0,24" stroke="{RAG_SKIN2}" stroke-width="3" fill="none" opacity="0.8"/>')  # eklem kıvrımları
    thumb = "M486,-92 Q546,-140 604,-118 Q616,-98 584,-84 Q540,-80 504,-74 Z"
    o.append(f'<path d="{thumb}" fill="{RAG_SKIN}" stroke="{INK}" stroke-width="{lw*0.9}" stroke-linejoin="round"/>'
             f'<path d="M590,-122 q12,4 10,16" stroke="#C8A088" stroke-width="5" fill="none" stroke-linecap="round"/>')
    o.append(f'<path d="M500,-60 q30,-6 64,0" stroke="{RAG_SKIN2}" stroke-width="3.5" fill="none" opacity="0.8"/>')  # el sırtı tendonu
    o.append(knot_mark(516, -28, 1.3))                             # el sırtı düğümü (kimlik)
    # --- önkol: dolgu konturSUZ, üst ve alt kontur ayrı (bilekte çizgi yok)
    fa = "M110,-104 Q300,-114 456,-84 Q470,-40 462,10 Q300,40 112,38 Z"
    o.append(f'<g filter="url(#t_form)"><path d="{fa}" fill="{RAG_SKIN}" {T("cilt", s)}/></g>')
    o.append(f'<path d="M110,-104 Q300,-114 456,-84" fill="none" stroke="{INK}" stroke-width="{lw}" stroke-linecap="round"/>'
             f'<path d="M462,10 Q300,40 112,38" fill="none" stroke="{INK}" stroke-width="{lw}" stroke-linecap="round"/>')
    o.append(f'<path d="M444,-82 Q450,-50 438,-20" stroke="{RAG_SKIN2}" stroke-width="3" fill="none" opacity="0.6"/>')  # bilek kemiği
    o.append("".join(f'<path d="M{150+k*22},{-74+(k%3)*12} l10,-4" stroke="#8A6A4A" stroke-width="2.4" opacity="0.6"/>' for k in range(12)))  # kıl
    # önkol düğüm bandı: art3.forearm_band (tek kaynak, R8); kol eksenine göre -11° düzeltme
    o.append(f'<g transform="translate(150,-66) scale(1.5) rotate(-13)" opacity="0.9">{forearm_band()}</g>')
    # manşet (kolun üstünde)
    if sleeve:
        o.append(f'<path d="M104,-122 Q136,-40 116,44" stroke="{INK}" stroke-width="{24+lw}" fill="none" stroke-linecap="round"/><path d="M104,-122 Q136,-40 116,44" stroke="#2E3A33" stroke-width="24" fill="none" stroke-linecap="round"/>')
    o.append(_ring_arc(False, lw))                                 # halkanın ön yayı
    return "".join(o)


def grip_composite(lw=7):
    """Bebeğin eli Ragnar'ın işaret parmağını kavrıyor. Katman: bebek+avuç → Ragnar parmağı → bebeğin parmakları."""
    tx, ty = 700 - BABY_REL * FIST[0], -30 - BABY_REL * FIST[1]
    bl = lw / BABY_REL
    return (f'<g transform="translate({tx:.0f},{ty:.0f}) scale({BABY_REL})">{baby(hand="grip", s=BABY_REL, lw=bl, awake=True)}</g>'
            + arm(lw=lw)
            + f'<g transform="translate({tx:.0f},{ty:.0f}) scale({BABY_REL})">{baby_grip_front(bl)}</g>')


# ------------------------------------------------------------------ kart
def card(path_png="nesneler/nesne_karti_v2.png"):
    W_, H_ = 2800, 1900
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W_}" height="{H_}">{defs(1.0)}<rect width="{W_}" height="{H_}" fill="#EDE2CC"/>',
         '<text x="40" y="76" font-family="Pirata One" font-size="60" fill="#2A1D14">Nesne kartı v2 · bebek Ivar ve Ragnar\'ın kolu, eli, halkası (kurul düzeltmeleri)</text>']
    lab = lambda x, y, t: f'<text x="{x}" y="{y}" font-family="Alegreya SC" font-size="28" text-anchor="middle" fill="#2A1D14">{t}</text>'
    # üst sıra: bebek ifadeleri (aynı ölçek, BABY_REL)
    for i, (kw, t) in enumerate(((dict(), "sakin (ana)"), (dict(cry=True, hand="up"), "ağlayan"), (dict(leg_out=True), "ivar_2.3 · sakat bacak"), (dict(awake=True, hand="up"), "uyanık, Ragnar\'a bakan"))):
        x = 260 + i * 560
        o.append(f'<g transform="translate({x},330) scale({BABY_REL})">{baby(s=BABY_REL, lw=7/BABY_REL, **kw)}</g>' + lab(x + 110, 640, t))
    o.append(f'<g transform="translate(2560,1500) scale(0.125)">{baby()}</g>' + lab(2580, 1600, "1/8"))
    # alt sıra: kol (1,0) ve kavrama kompoziti, aynı ölçek
    o.append(f'<g transform="translate(330,960)">{arm()}</g>' + lab(560, 1110, "Ragnar · sol önkol, el, düğüm dövmesi, iki katmanlı burgulu halka"))
    o.append(f'<g transform="translate(330,1500)">{grip_composite()}</g>' + lab(900, 1860, "kavrama: bebeğin parmakları Ragnar\'ın işaret parmağını sarıyor (aynı ölçek)"))
    # ölçek çubuğu: Ragnar el uzunluğu (bilek→işaret ucu = 262) ve bebek kafa uzunluğu
    o.append('<g transform="translate(1180,1180)" font-family="Alegreya SC" font-size="24" fill="#2A1D14">'
             '<rect width="262" height="10" fill="#2A1D14"/><text y="40">el uzunluğu (262)</text>'
             f'<rect y="60" width="{230*BABY_REL:.0f}" height="10" fill="#7A5A28"/><text y="100">bebek kafası ({230*BABY_REL:.0f}) = 0,66 × el</text></g>')
    o.append(lab(2120, 1250, "sahne önizlemesi (Ivar sisi + grade)"))
    o.append('</svg>')
    open('nesneler/kart_v2.svg', 'w').write("".join(o))
    subprocess.run(['rsvg-convert', 'nesneler/kart_v2.svg', '-w', str(W_), '-o', path_png], check=True)


def scene_preview(path_png="nesneler/sahne_onizleme_v2.png"):
    """Aynı nesneler Ivar sahnesinin sisli arka planı ve grade'i altında (G2 #5)."""
    sys.path[:0] = ["/home/claude/r3/veda", "/home/claude/r3/ivar"]
    import skia
    from engine import sprite, draw, W, H
    from engine import vignette
    from fx import blurred, fog, gradient_grade, grade, bloom_spot
    import ivar.anim as IA
    sc = 1.2
    svg = f'{defs(sc)}<g transform="translate(300,220)">{grip_composite(lw=7/sc)}</g>'
    sp = sprite(svg, 1500, 600, ax=0, ay=0, ss=1.0)
    surf = skia.Surface(W, H); c = surf.getCanvas(); c.clear(skia.ColorBLACK)
    for L_ in (IA.FOG_FAR, IA.MID, IA.NEAR): draw(c, blurred(L_, 14), W / 2, H / 2 + 120, 1.1)
    fog(c, 1.2, 700, "#DDE4EA", 0.5, seed=2, speed=14)
    bloom_spot(c, 420, 220, 520, "#E8F0F6", 0.35)
    draw(c, sp, 20, 300, sc)
    gradient_grade(c, "#2A4A6E", "#1A2A3A", 0.35, "soft"); grade(c, "#9EB6CC", 0.18, "multiply")
    vignette(c, 0.75)
    surf.makeImageSnapshot().save(path_png, skia.kPNG)



def build():
    from PIL import Image
    card(); scene_preview()
    cd = Image.open("nesneler/nesne_karti_v2.png").convert("RGB"); pv = Image.open("nesneler/sahne_onizleme_v2.png").convert("RGB")
    pv = pv.resize((1000, 562)); cd.paste(pv, (1620, 660)); cd.save("nesneler/nesne_karti_v2.png")


if __name__ == "__main__":
    build(); print("ok")
