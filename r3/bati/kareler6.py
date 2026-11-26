"""I · Batı: çekim listesi v2'nin yeni kareleri f1–f10 (her cümleye bir görsel vuruş). Ortak yardımcılar kareler5'ten gelir.
python3 kareler6.py [f1..f10] → bati/<id>.png, kontakt6_960.png
"""
import sys
sys.path.insert(0, "/home/claude/r3/bati")
from kareler5 import *

def field_svg():
    r = random.Random(12); o = []
    o.append('<path d="M0,760 Q600,700 1100,730 Q1500,750 1920,720 L1920,1080 L0,1080 Z" fill="#5A4A36" stroke="#2A1E14" stroke-width="6"/>')
    for k in range(16):   # karık
        y = 770 + k * 20; o.append(f'<path d="M0,{y} Q700,{y-30-k*2} 1920,{y-10}" stroke="#3E3022" stroke-width="{3+k*0.4:.1f}" fill="none"/>')
    for k in range(60): o.append(f'<ellipse cx="{r.uniform(0,1920):.0f}" cy="{r.uniform(780,1060):.0f}" rx="{r.uniform(10,40):.0f}" ry="{r.uniform(3,8):.0f}" fill="#E8EEF2" opacity="0.7"/>')
    o.append('<path d="M150,760 L150,690 M110,700 L190,700" stroke="#3A2A1A" stroke-width="8"/>')
    return "".join(o)

ARD = ('<g transform="translate(HX,HY)"><path d="M0,0 L140,180" stroke="#1A1410" stroke-width="16" stroke-linecap="round"/><path d="M0,0 L140,180" stroke="#6A4428" stroke-width="9" stroke-linecap="round"/>'
       '<path d="M120,170 L260,200 L250,214 L118,190 Z" fill="#5A3A20" stroke="#1A1410" stroke-width="5"/><path d="M250,200 L290,212" stroke="#8A8A82" stroke-width="10"/></g>')

def f1():   # Kattegat fiyordu, tarlada Ragnar (kanca kartları)
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    draw(c, place(O7.kattegat4()), 0, 0, 1.0)
    draw(c, svg_sprite(field_svg()), 0, 0, 1.0)
    RGs = full(dict(RG, _arm_up=False, _carry_svg=ARD.replace("translate(HX,HY)", "translate(30,-300)")), ex("determined", IF.blink_at(0.2)), 0.95, facing=1, look=-0.6)
    with live(c, 760, 1020, phase=0.2, breathe=0.005):
        draw(c, RGs, 760, 1020, 1.0); shade_side(c, RGs, 760, 1020, 0.35, 600, 900, "#1A2430")
    card_at(c, "KATTEGAT · 793", 1400, 160)
    card_at(c, "RAGNAR", 760, 300, "çiftçi (henüz)")
    snowfall(c, t, (0, 70, W, H - 70), 60); finish(c, cold=True); return s

def f2():   # duvardaki deri harita yakın: doğuya kırmızı oklar, gemi ikonları
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    wall = "".join(f'<rect x="{x}" y="0" width="160" height="1080" fill="{"#4A3020" if (x//160)%2 else "#432C1C"}" stroke="#1A0E06" stroke-width="5"/>' for x in range(0, 1920, 160))
    ships = "".join(f'<g transform="translate({x},{y}) scale(0.18)">{G.longship(0, 0, 1.0, sail=True, oars=False)}</g>' for x, y in ((1180, 520), (1330, 640), (1250, 760)))
    draw(c, svg_sprite(wall + hide_map(960, 560, 3.6) + ships), 0, 0, 1.0)
    card_at(c, "DOĞU", 1560, 200, "Rus toprakları")
    glow(c, 960, 540, 700, "#FF9A50", 0.12); finish(c, cold=False, warm=0.06); return s

def mud_hut(x, y, s=1.0, collapsed=False):
    roof = (f'<path d="M-130,-60 L0,-170 L130,-60 Z" fill="#7A6A44" stroke="{INK}" stroke-width="7"/>' if not collapsed else
            f'<path d="M-130,-60 L-40,-90 L10,-40 L60,-110 L130,-60 Z" fill="#7A6A44" stroke="{INK}" stroke-width="7"/><path d="M-20,-60 l40,-30 M30,-50 l30,-40" stroke="#5A4A2A" stroke-width="6"/>')
    return (f'<g transform="translate({x},{y}) scale({s})"><path d="M-110,0 L-110,-70 L110,-70 L110,0 Z" fill="#6A5A40" stroke="{INK}" stroke-width="7"/>'
            f'<path d="M-30,0 L-30,-50 L20,-50 L20,0" fill="#2A2018" stroke="{INK}" stroke-width="5"/>{roof}'
            + "".join(f'<path d="M{-100+k*30},-{20+(k%3)*12} l18,4" stroke="#4A3A28" stroke-width="4"/>' for k in range(7)) + '</g>')

GOAT = ('<g><ellipse cx="0" cy="0" rx="62" ry="30" fill="#B8B0A0" stroke="#1A1410" stroke-width="6"/>' + "".join(f'<path d="M{x},20 L{x+4},80" stroke="#1A1410" stroke-width="8"/>' for x in (-40, -20, 24, 44)) +
        '<path d="M50,-14 L84,-48 L104,-30 L80,-6 Z" fill="#B8B0A0" stroke="#1A1410" stroke-width="5"/><path d="M84,-48 Q80,-80 60,-84 M92,-44 Q100,-76 84,-88" stroke="#5A4A3A" stroke-width="6" fill="none"/>'
        '<path d="M100,-26 l6,20" stroke="#E8E0D0" stroke-width="5"/><circle cx="90" cy="-36" r="4" fill="#1A1410"/>' + "".join(f'<path d="M{-50+k*14},-24 l2,12" stroke="#7A7268" stroke-width="3"/>' for k in range(8)) + '</g>')

def f3():   # şaka: doğuda fakir köyler (çamur, sıska keçi, boş sandık); ikinci kulübenin çatısı çökmüş
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    sky = '<rect width="1920" height="1080" fill="#8E949A"/><rect y="560" width="1920" height="520" fill="#5E5A48"/>'
    draw(c, svg_sprite(sky + O7.ground2(W, H, 620, seed=21) + mud_hut(560, 820, 2.4) + mud_hut(1360, 790, 2.1, collapsed=True)
                       + f'<g transform="translate(960,900) scale(2.0)">{GOAT}</g><g transform="translate(1560,900)">{RING_CHEST.replace("<ellipse", "<ellipse opacity=\'0\'")}</g>'
                       + "".join(f'<path d="M{x},{y} q30,-10 60,0" stroke="#3A3022" stroke-width="5" fill="none"/>' for x, y in ((300, 900), (820, 980), (1400, 960)))), 0, 0, 1.0)
    card_at(c, "DOĞU", 960, 160, "fakir köy · biraz daha fakir köy")
    fill(c, "#B0B4B0", 0.08); finish(c, cold=True); return s

def f4():   # açık deniz: sis, boş ufuk, minik kayık; harita ve pusula yok
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    o = ['<defs><linearGradient id="fg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9AA6B0"/><stop offset="1" stop-color="#C8CED2"/></linearGradient></defs>',
         '<rect width="1920" height="600" fill="url(#fg)"/><rect y="560" width="1920" height="520" fill="#4E606C"/>']
    for k in range(30):
        y = 600 + k * 16; o.append(f'<path d="M0,{y} ' + " ".join(f"Q{x+60},{y-6-k*0.4:.0f} {x+120},{y}" for x in range(0, 1920, 120)) + f'" stroke="#3A4A56" stroke-width="{2+k*0.15:.1f}" fill="none" opacity="0.6"/>')
    for k in range(12): r = random.Random(k); o.append(f'<ellipse cx="{r.uniform(0,1920):.0f}" cy="{r.uniform(480,640):.0f}" rx="{r.uniform(200,500):.0f}" ry="{r.uniform(20,50):.0f}" fill="#E0E4E6" opacity="0.4"/>')
    o.append(f'<g transform="translate(960,620) scale(0.16)">{G.longship(0, 0, 1.0, sail=True, oars=False)}</g>')
    for x, ic in ((760, '<rect x="-50" y="-36" width="100" height="72" fill="#E2CFA2" stroke="#1A1410" stroke-width="5"/><path d="M-30,-10 Q0,-30 30,0 Q0,20 -30,10" stroke="#8A2A22" stroke-width="4" fill="none"/>'),
                  (1160, '<circle r="44" fill="#C8B488" stroke="#1A1410" stroke-width="5"/><path d="M0,-34 L10,0 L0,34 L-10,0 Z" fill="#8A2A22" stroke="#1A1410" stroke-width="3"/>')):
        o.append(f'<g transform="translate({x},260)">{ic}<path d="M-56,-56 L56,56 M56,-56 L-56,56" stroke="#B8322A" stroke-width="14" stroke-linecap="round"/></g>')
    draw(c, svg_sprite("".join(o)), 0, 0, 1.0)
    card_at(c, "BATI", 960, 420, "açık deniz")
    finish(c, cold=True); return s

def f5():   # insert: pelerinli gezginin eli iki aleti uzatır
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    draw(c, blurred(place(IPL.longhouse(0.5)), 9), 0, 0, 1.0); fill(c, "#0A0E16", 0.4)
    o = [f'<rect x="0" y="700" width="1920" height="380" fill="#4A3020" stroke="{INK}" stroke-width="8"/>' + "".join(f'<path d="M0,{730+k*40} H1920" stroke="#3A2414" stroke-width="3"/>' for k in range(9))]
    o.append(f'<path d="M1920,380 Q1500,420 1240,560 L1260,700 Q1560,620 1920,640 Z" fill="#3A3028" stroke="{INK}" stroke-width="8"/>'   # pelerin kolu
             + "".join(f'<path d="M{1300+k*60},{560-k*14} q10,40 0,80" stroke="#2A221C" stroke-width="4" fill="none"/>' for k in range(10)))
    o.append(f'<path d="M1270,540 Q1170,530 1090,580 Q1040,620 1060,660 Q1080,690 1150,680 L1170,700 Q1230,710 1280,700 Z" fill="#D8B494" stroke="{INK}" stroke-width="8"/>'
             f'<path d="M1090,600 q-30,10 -40,30 M1100,640 q-40,10 -50,30 M1130,670 q-30,14 -36,34" stroke="{INK}" stroke-width="22" stroke-linecap="round" fill="none"/><path d="M1090,600 q-30,10 -40,30 M1100,640 q-40,10 -50,30 M1130,670 q-30,14 -36,34" stroke="#D8B494" stroke-width="13" stroke-linecap="round" fill="none"/>'
             f'<path d="M1150,560 q20,10 50,4 M1140,600 q30,8 60,0" stroke="#A88A6A" stroke-width="3" fill="none"/>')   # yaşlı, damarlı el
    o.append(f'<g transform="translate(860,760) scale(1.5)">{SUNBOARD}</g><g transform="translate(1010,610) scale(1.6)">{SUNSTONE}</g>')
    o.append(candles_svg(420, 760))
    draw(c, svg_sprite("".join(o)), 0, 0, 1.0)
    bloom_spot(c, 420, 640, 160, "#FFB060", 0.45); bloom_spot(c, 1010, 610, 110, "#FFF2C8", 0.4)
    card_at(c, "GEZGİN", 1560, 300, "güneş tahtası + güneş taşı", 0.9)
    finish(c, cold=True, warm=0.08); return s

def f6():   # gece, gizli kalkış: kıyıdan itilen gemi, meşale söner
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    o = ['<rect width="1920" height="1080" fill="#0E1620"/><circle cx="1500" cy="200" r="70" fill="#D8E2EA"/><circle cx="1500" cy="200" r="140" fill="#D8E2EA" opacity="0.08"/>',
         '<path d="M0,560 Q500,520 1000,560 L1920,540 L1920,1080 L0,1080 Z" fill="#1A2A36"/>']
    o.append(f'<g transform="translate(1100,640) scale(0.8)">{G.longship(0, 0, 1.0, sail=True, reefed=True, oars=True, shields=True)}</g>')
    o.append('<path d="M0,820 Q600,760 900,800 Q1200,840 1920,800 L1920,1080 L0,1080 Z" fill="#2A2A22" stroke="#0A0A08" stroke-width="5"/>')   # kıyı
    draw(c, svg_sprite("".join(o)), 0, 0, 1.0)
    for k, x in enumerate((1460, 1600)):
        sp = full(dict(KL.soldier_spec(70 + k, "ragnar"), _arm_up=False, _hand_extra=""), "pain", 0.85, facing=1, look=0.6)
        draw(c, tinted(sp, "#1A2A3A") if False else sp, x, 900, 0.7)
    RGt = full(dict(RG, _arm_up=True, _hand_extra=TORCH), ex("determined", IF.blink_at(0.2)), 0.9, facing=1, look=0.6)
    draw(c, RGt, 420, 1020, 1.0); shade_side(c, RGt, 420, 1020, 0.55, 250, 700, "#060A10")
    fill(c, "#0A1220", 0.25); glow(c, 420, 300, 200, "#FF9A3A", 0.25)
    card_at(c, "GECE", 960, 160, "Jarl'dan gizli")
    finish(c, cold=True); return s

def f7():   # pruvadan bakış: sisten çıkan kayalık ada ve manastır
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    o = ['<rect width="1920" height="1080" fill="#A8B2BA"/>', '<rect y="560" width="1920" height="520" fill="#5E7280"/>',
         '<path d="M500,560 L640,420 L820,400 L900,330 L1180,340 L1260,420 L1420,440 L1520,560 Z" fill="#4E5A4A" stroke="#2A3020" stroke-width="6"/>']
    o.append('<g transform="translate(1020,360) scale(0.35)"><rect x="-320" y="-220" width="560" height="220" fill="#8A8478" stroke="#1A1410" stroke-width="12"/><path d="M-350,-210 L-40,-360 L270,-210 Z" fill="#4A3E32" stroke="#1A1410" stroke-width="12"/>'
             '<rect x="240" y="-420" width="150" height="420" fill="#7E786C" stroke="#1A1410" stroke-width="12"/><path d="M226,-420 L315,-520 L404,-420 Z" fill="#4A3E32" stroke="#1A1410" stroke-width="12"/>'
             '<path d="M315,-520 V-610 M285,-580 H345" stroke="#D8B04A" stroke-width="16"/></g>')
    for k in range(18): r = random.Random(k + 40); o.append(f'<ellipse cx="{r.uniform(0,1920):.0f}" cy="{r.uniform(420,620):.0f}" rx="{r.uniform(200,500):.0f}" ry="{r.uniform(20,60):.0f}" fill="#E4E8EA" opacity="{r.uniform(0.25,0.5):.2f}"/>')
    for k in range(24):
        y = 640 + k * 18; o.append(f'<path d="M0,{y} ' + " ".join(f"Q{x+60},{y-8} {x+120},{y}" for x in range(0, 1920, 120)) + f'" stroke="#3A4E5A" stroke-width="3" fill="none" opacity="0.6"/>')
    o.append(f'<g transform="translate(1500,1120) scale(2.2)">{G.dragon_head(0, 0, 1.0)}</g>')   # pruva ön planda
    o.append(f'<path d="M0,1080 L0,900 Q600,860 1360,960 L1500,1080 Z" fill="#5A4632" stroke="{INK}" stroke-width="10"/>' + "".join(f'<path d="M0,{920+k*36} Q600,{880+k*36} 1380,{980+k*30}" stroke="#3E2E1E" stroke-width="5" fill="none"/>' for k in range(4)))
    draw(c, svg_sprite("".join(o)), 0, 0, 1.0)
    card_at(c, "İNGİLTERE", 960, 160, "Lindisfarne")
    finish(c, cold=True); return s

def f8():   # insert: sunak, altın haç, kadeh, mücevherli kitap
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    o = ['<rect width="1920" height="1080" fill="#3A3630"/>'] + [f'<rect x="{x}" y="{y}" width="120" height="60" fill="none" stroke="#2A2620" stroke-width="4"/>' for y in range(0, 700, 60) for x in range(-60 + (y // 60 % 2) * 60, 1920, 120)]
    o.append('<path d="M860,0 V420 Q960,320 1060,420 V0 Z" fill="#8A9AA8" opacity="0.55"/>')   # pencere ışığı
    o.append(f'<rect x="300" y="680" width="1320" height="400" fill="#7A746A" stroke="{INK}" stroke-width="10"/><rect x="260" y="640" width="1400" height="60" fill="#E8E0CC" stroke="{INK}" stroke-width="8"/>'
             f'<path d="M700,640 V1080 M1220,640 V1080" stroke="#B8322A" stroke-width="40"/>')
    o.append(f'<g transform="translate(960,630)"><rect x="-14" y="-380" width="28" height="380" fill="#D8B04A" stroke="{INK}" stroke-width="7"/><rect x="-120" y="-300" width="240" height="28" fill="#D8B04A" stroke="{INK}" stroke-width="7"/>'
             + "".join(f'<circle cx="{x}" cy="{y}" r="12" fill="{c_}" stroke="{INK}" stroke-width="4"/>' for x, y, c_ in ((0, -286, "#8E2A22"), (-100, -286, "#2E4A9E"), (100, -286, "#2E4A9E"), (0, -360, "#2E8A4E"), (0, -180, "#8E2A22"))) + '</g>')
    o.append(f'<g transform="translate(640,630)"><path d="M-60,-160 Q-60,-80 0,-60 Q60,-80 60,-160 Z" fill="#D8B04A" stroke="{INK}" stroke-width="7"/><rect x="-10" y="-62" width="20" height="44" fill="#D8B04A" stroke="{INK}" stroke-width="6"/><ellipse cx="0" cy="-12" rx="60" ry="14" fill="#D8B04A" stroke="{INK}" stroke-width="6"/></g>')
    o.append(f'<g transform="translate(1300,600) rotate(-6)"><rect x="-150" y="-40" width="300" height="70" rx="6" fill="#6A1E1E" stroke="{INK}" stroke-width="7"/><rect x="-130" y="-30" width="260" height="20" fill="#D8B04A" stroke="{INK}" stroke-width="4"/>'
             + "".join(f'<circle cx="{-100+k*50}" cy="-20" r="7" fill="#2E8A9E" stroke="{INK}" stroke-width="3"/>' for k in range(5)) + '</g>')
    draw(c, svg_sprite("".join(o)), 0, 0, 1.0)
    for x, y in ((960, 300), (640, 500), (1300, 580)): bloom_spot(c, x, y, 90, "#FFE6A0", 0.45)
    card_at(c, "ALTIN · GÜMÜŞ", 960, 140, "silah yok")
    finish(c, cold=False, warm=0.05); return s

def f9():   # Floki, Jarl'ın salonunda meydan okumayı iletiyor
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    draw(c, blurred(place(P7.greathall(0.8)), 4), 0, 0, 1.0)
    army(c, "ragnar", [(860, 0.55, 10, 0.12)], t, seed0=81, facing=-1, x0=200, x1=1800)
    FL = full(dict(FLOv, _arm_up=True, _hand_extra=""), ex("smug", IF.blink_at(0.5)), 1.0, facing=1, look=0.6)
    HS = full(HARALD, ex("cold", IF.blink_at(0.6)), 1.0, facing=-1, look=-0.6)
    rim(c, FL, 640, 1040, 1.0, "#FFB070", dx=4, dy=0, a=0.6); draw(c, FL, 640, 1040, 1.0)
    rim(c, HS, 1300, 1040, 1.0, "#FFB070", dx=-4, dy=0, a=0.6); draw(c, HS, 1300, 1040, 1.0)
    draw(c, thought('<text x="0" y="16" font-family="Georgia" font-weight="bold" font-size="46" fill="#8A2A22" text-anchor="middle">HOLMGANG</text>', 340, 150), 820, 220, 0.9)
    card_at(c, "FLOKİ", 640, 330, "Ragnar'ın mesajı")
    glow(c, 960, 1000, 520, "#FF8A3A", 0.18); finish(c, cold=False, warm=0.05); return s

def f10():   # Jarl düşüyor: dizlerinin üstünde, kılıcı yerde; Ragnar ayakta; kar
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    draw(c, blurred(place(O7.kattegat4()), 7), 0, 0, 1.0)
    draw(c, svg_sprite(shield_ring(960, 860, 900, 260, front=False)), 0, 0, 1.0)
    HS = full(dict(HARALD, _kneel=130), ex("pain", IF.blink_at(0.6)), 1.0, facing=-1, look=-0.8)
    draw(c, HS, 1220, 1020, 1.0); shade_side(c, HS, 1220, 1020, 0.4, 1100, 1400, "#1A2430")
    draw(c, svg_sprite('<g transform="translate(1000,1000) rotate(80)"><path d="M0,0 L-14,-260" stroke="#1A1410" stroke-width="18" stroke-linecap="round"/><path d="M-2,-30 L-14,-260" stroke="#C8D0D8" stroke-width="10"/><path d="M-36,-24 L32,-30" stroke="#1A1410" stroke-width="14"/></g>'), 0, 0, 1.0)
    RGs = full(dict(RG, _arm_up=False, _carry_svg=""), ex("cold", IF.blink_at(0.2)), 1.0, facing=1, look=0.6)
    draw(c, RGs, 640, 1040, 1.0); shade_side(c, RGs, 640, 1040, 0.4, 500, 800, "#1A2430")
    snowfall(c, t, (0, 70, W, H - 70), 80); fill(c, "#C8D2DC", 0.06); finish(c, cold=True); return s

FR6 = {"f1": f1, "f2": f2, "f3": f3, "f4": f4, "f5": f5, "f6": f6, "f7": f7, "f8": f8, "f9": f9, "f10": f10}

def contact6(ids=tuple(FR6)):
    from PIL import Image
    sheet = Image.new("RGB", (960 * 2 + 30, 560 * 5 + 10), "#EDE2CC")
    for k, i in enumerate(ids): sheet.paste(Image.open(f"{OUT}/{i}.png").convert("RGB").resize((960, 540)), (10 + (k % 2) * 970, 10 + (k // 2) * 560))
    sheet.save(f"{OUT}/kontakt6_960.png")

if __name__ == "__main__":
    ids = sys.argv[1:] or list(FR6)
    for i in ids:
        T[0] = None; FR6[i]().makeImageSnapshot().save(f"{OUT}/{i}.png", skia.kPNG); print("kare", i)
    contact6()
