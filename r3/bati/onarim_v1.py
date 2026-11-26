"""Denetim onarımları v1 (20.11.2026) · taslak varyantlar. Onaylı kare fonksiyonlarına DOKUNULMAZ:
yeni kareler burada yazılır; küçük ifade/jest notları onaylı fonksiyonun kaynağından türetilen yeni adlı kopya ile yapılır (_turet).
python3 onarim_v1.py [id ...] → kurul/onarim_v1/<id>.png (+ _crop1/_crop2) ve kontakt_960.png
"""
import sys, os, math, random, inspect
sys.path[:0] = ["/home/claude/r3/bati", "/home/claude/r3", "/home/claude/r2", "/home/claude/r3/ivar2", "/home/claude/r3/veda2", "/home/claude/r3/bedel", "/home/claude/r3/kesis"]
import v6_son as VS
from v6_son import *                       # kareler6/5/4/3 + v3_a/b/c + v4_paris + v5_kayip yardımcıları
import v5_kayip as VK, v3_c as VC, v3_b as VB, v3_a as VA, v4_paris as VP
import kareler4 as K4, kareler5 as K5, kareler3 as K3
import ragnar_yas as YAS
import gemi as G
OUTS = "/home/claude/r3/kurul/onarim_v1"; os.makedirs(OUTS, exist_ok=True)
INK = "#1A1410"

# ------------------------------------------------------------------ ortak: yeni ifadeler (art3.EXP'ye eklenir, var olanlar değişmez)
EXP["closed_tear"] = (-16, 8, 0.96, 0.14, "tremble2", "tear")      # d2: göz kapanır, gözyaşı
EXP["sly_half"] = (4, -4, 0.46, 0.08, "smirk", "")                 # d7: sinsi yarım gülümseme
EXP["soften"] = (-8, 5, 0.36, 0.04, "flat", "")                    # e6: bakış yumuşar
EXP["squint_smirk"] = (12, -4, 0.58, 0.10, "smirk", "")            # k23b: Ivar gözlerini kısar, yamuk gülümser
EXP["gelecek"] = (-6, 2, 0.34, 0.06, "soft_smile", "")             # k26c: hafif gülümseme
EXP["regal"] = (6, -3, 0.30, 0.08, "firm", "")                     # d8: kral bakışı
EXP["joy"] = (-8, -6, 0.30, 0.10, "laugh", "")                     # e8: sevinçli halk
EXP["shock"] = (-12, -10, 0.0, 0.0, "open_o", "")                  # f10: şaşkın kalabalık

MARK = '<g transform="translate(HX,HY)"><circle r="7" fill="#FF00FF"/></g>'
def hand_at(spec, maker):
    """Model gövdesinde elin (HX,HY) sprite çapasına göre konumunu ölçer: el ekine macenta işaret koyup piksel arar."""
    import numpy as np
    sp = maker(dict(spec, _hand_extra=MARK)); s = skia.Surface(3000, 3000); c = s.getCanvas(); c.clear(skia.ColorTRANSPARENT)
    draw(c, sp, 1500, 1500, 1.0); a = s.makeImageSnapshot().toarray()
    m = (a[..., 0] > 240) & (a[..., 1] < 30) & (a[..., 2] > 240) if a.shape[-1] == 4 else None
    ys, xs = np.nonzero(m)
    return (float(xs.mean()) - 1500, float(ys.mean()) - 1500) if len(xs) else (0.0, 0.0)

# ------------------------------------------------------------------ kimlik ve nesne kaynakları (R8)
CROWN_RG = ('<g>'   # sade altın bant: dizideki taç kopyalanmaz; alın kavisinde, alçak beş diş, üç kehribar
            '<path d="M-88,-54 L-80,-80 L-66,-70 L-46,-88 L-24,-76 L0,-96 L24,-77 L48,-89 L68,-72 L84,-82 L88,-58 Q0,-88 -88,-54 Z" fill="#C9962E" stroke="#1A1410" stroke-width="6" stroke-linejoin="round"/>'
            '<path d="M-88,-52 Q0,-88 90,-56" stroke="#1A1410" stroke-width="22" fill="none"/><path d="M-88,-52 Q0,-88 90,-56" stroke="#D8A63A" stroke-width="15" fill="none"/>'
            '<path d="M-84,-58 Q0,-92 86,-62" stroke="#FFE7A0" stroke-width="3" fill="none" opacity="0.9"/>'
            '<path d="M-80,-46 Q0,-78 84,-50" stroke="#7A5418" stroke-width="3" fill="none" opacity="0.8"/>'
            + "".join(f'<path d="M{x-6},{y-4} q6,-6 12,0 q-6,6 -12,0" stroke="#7A5418" stroke-width="2" fill="none"/>' for x, y in ((-64, -62), (-30, -72), (30, -73), (62, -65)))
            + "".join(f'<circle cx="{x}" cy="{y}" r="{r_}" fill="#C8641E" stroke="#1A1410" stroke-width="3"/><circle cx="{x-2}" cy="{y-2}" r="{r_*0.35:.1f}" fill="#FFD8A0"/>' for x, y, r_ in ((-46, -66, 7), (0, -76, 9), (46, -67, 7)))
            + '<path d="M-44,-84 L-40,-76 M2,-92 L2,-82 M48,-86 L46,-78" stroke="#FFE7A0" stroke-width="3"/></g>')
ATH_CROSS = VS.CROSS_A.replace('<g transform="translate(0,-436)">', '<g>')   # Athelstan'ın tahta haçı (k24 ile aynı model)
def cross_held(s=2.0, rot=0):
    """Haç elde: kordon parmaktan sarkar (CROSS_A geometrisi, ölçekli)."""
    return (f'<g transform="translate(HX,HY) rotate({rot}) scale({s})"><path d="M0,-6 Q-10,-30 0,-46 Q10,-30 0,-6" stroke="#5A4026" stroke-width="2.4" fill="none"/>'
            f'<g transform="translate(0,6) scale(1.35)"><rect x="-5" y="-6" width="10" height="36" rx="2" fill="#5A3E26" stroke="#1A1410" stroke-width="3"/><rect x="-15" y="3" width="30" height="9" rx="2" fill="#5A3E26" stroke="#1A1410" stroke-width="3"/>'
            '<path d="M-2,-2 V26 M-11,7 H11" stroke="#9A7A52" stroke-width="1.6" opacity="0.8"/><path d="M3,-4 V24" stroke="#2E1E10" stroke-width="1.4" opacity="0.7"/></g></g>')
SILVER = ('<g transform="translate(HX,HY)"><path d="M-46,-6 Q0,26 46,-6 L40,-20 Q0,2 -40,-20 Z" fill="#B8BEC4" stroke="#1A1410" stroke-width="5"/>'
          '<ellipse cx="0" cy="-20" rx="42" ry="10" fill="#E6EAEE" stroke="#1A1410" stroke-width="4"/><path d="M-26,-22 q26,-8 52,0" stroke="#FFFFFF" stroke-width="3" fill="none"/>'
          + "".join(f'<circle cx="{x}" cy="{y}" r="7" fill="#D8DCE0" stroke="#1A1410" stroke-width="2"/>' for x, y in ((-14, -26), (4, -30), (18, -24))) + '</g>')   # gümüş kâse, içi sikke
COINS = ('<g transform="translate(HX,HY)">' + "".join(f'<ellipse cx="{x}" cy="{y}" rx="12" ry="5" fill="#D4D8DC" stroke="#1A1410" stroke-width="2.5"/>' for x, y in ((0, 0), (2, -6), (-2, -12), (1, -18))) + '</g>')

def crop2x_(p, box, out):
    from PIL import Image
    im = Image.open(p).crop(box); im.resize((im.width * 2, im.height * 2), Image.LANCZOS).save(out)

def throne_back(cx, y0, w=820, h=760):
    """Oymalı yüksek koltuk sırtı: iki dikme, kuzgun başlı tepelik, örgü desenli pano, kırmızı kumaş."""
    o = [TEXD]
    o.append(f'<path d="M{cx-w/2+60},{y0+h} L{cx-w/2+80},{y0+80} Q{cx},{y0+10} {cx+w/2-80},{y0+80} L{cx+w/2-60},{y0+h} Z" fill="#5A3A22" stroke="{INK}" stroke-width="8" filter="url(#t_ahsap)"/>')
    o.append(f'<path d="M{cx-w/2+130},{y0+h} L{cx-w/2+140},{y0+140} Q{cx},{y0+80} {cx+w/2-140},{y0+140} L{cx+w/2-130},{y0+h} Z" fill="#7A1E1C" stroke="{INK}" stroke-width="6"/>')
    for k in range(9): o.append(f'<path d="M{cx-w/2+150+k*((w-300)/8):.0f},{y0+150+abs(k-4)*6} L{cx-w/2+150+k*((w-300)/8)+8:.0f},{y0+h}" stroke="#4E1210" stroke-width="5" opacity="0.6"/>')
    o.append(VA.braid(cx - w / 2 + 110, y0 + 92, w - 220, 40, "#B8862E", "#5A3A12", 16, 9))
    for sx in (-1, 1):
        x = cx + sx * (w / 2 - 40)
        o.append(f'<rect x="{x-38}" y="{y0+40}" width="76" height="{h}" fill="#6A4428" stroke="{INK}" stroke-width="8" filter="url(#t_ahsap)"/>')
        o.append(VA.braid(x - 26, y0 + 120, 52, h - 140, "#9A6A3A", "#3A2412", 6, 22).replace('<path', '<path opacity="0.7"'))
        o.append(f'<path d="M{x+sx*22},{y0+44} L{x-sx*10},{y0+44} Q{x-sx*30},{y0-30} {x+sx*2},{y0-78} Q{x+sx*40},{y0-100} {x+sx*56},{y0-70} L{x+sx*92},{y0-64} L{x+sx*58},{y0-48} Q{x+sx*40},{y0-36} {x+sx*34},{y0-10} Z" fill="#5A3A22" stroke="{INK}" stroke-width="7" stroke-linejoin="round" filter="url(#t_ahsap)"/>'
                 f'<circle cx="{x+sx*30}" cy="{y0-62}" r="7" fill="#E2B448" stroke="{INK}" stroke-width="3"/><path d="M{x+sx*4},{y0-60} Q{x+sx*20},{y0-30} {x+sx*10},{y0+20}" stroke="#2A1A10" stroke-width="4" fill="none"/>')   # kuzgun başı
    return "".join(o)

def sprite_h(sp):
    import numpy as np
    s_ = skia.Surface(3000, 3000); c_ = s_.getCanvas(); c_.clear(skia.ColorTRANSPARENT); draw(c_, sp, 1500, 2500, 1.0)
    a = s_.makeImageSnapshot().toarray(); ys = np.nonzero(a[..., 3] > 20)[0]; return float(ys.max() - ys.min()) if len(ys) else 900.0

# ================================================================== (A) d8 · "Artık bir kralsın": alçak açı, taç, diz çöken salon
def d8():
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    draw(c, blurred(place(P7.greathall(1.0)), 5), -300, -120, 1.32)
    c.drawRect(skia.Rect(0, 0, W, H), skia.Paint(Color4f=col("#06030A", 0.35)))
    rays(c, 960, -60, 90, 1100, 40, 9, "#FFE2A0", 0.10, 0.0 if t is None else t)        # duman deliğinden altın hüzme
    for x in (230, 1690):                                                               # iki yanda meşale direği (orta plan)
        draw(c, svg_sprite(f'<g transform="translate({x},330)">{K4.TORCH.replace("translate(HX,HY)", "translate(0,0) scale(1.3)")}</g>'
                           f'<path d="M{x-6},360 L{x-10},1080" stroke="{INK}" stroke-width="30"/><path d="M{x-6},360 L{x-10},1080" stroke="#4A3020" stroke-width="18"/>'), 0, 0, 1.0)
        glow(c, x - 10, 60, 280, "#FF9A3A", 0.45); bloom_spot(c, x - 12, 70, 50, "#FFE6A0", 0.7)
    # orta plan: iki yanda diz çökmüş halk (gerçek modeller, ortaya bakar), uzak sıra küçük ve soluk
    for k, (x, y, f_, sc, a_) in enumerate(((300, 880, 1, 0.50, 0.75), (430, 900, 1, 0.55, 0.85), (1500, 900, -1, 0.55, 0.85), (1630, 880, -1, 0.50, 0.75),
                                            (180, 940, 1, 0.66, 1.0), (1760, 940, -1, 0.66, 1.0))):
        sp = full(dict(KL.soldier_spec(30 + k, "ragnar") if k % 3 else VK.civ(80 + k, "woman" if k == 3 else "man"), _kneel=130, _arm_up=False, _hand_extra="", _body_extra=""),
                  "awe", 0.85, facing=f_, look=0.5 * f_)
        rim(c, sp, x, y, sc, "#FFC070", dx=4 * -f_, dy=-4, a=0.7); draw(c, sp, x, y, sc); shade_side(c, sp, x, y, 0.5, 960, x, "#120A06")
    draw(c, svg_sprite(throne_back(960, 210)), 0, 0, 1.0)                              # koltuk sırtı
    glow(c, 960, 380, 520, "#FFD27A", 0.30)                                             # başın arkasında altın hale
    rg = dict(RG, _head_extra=CROWN_RG)
    b = fig_bust(rg, ex("regal", IF.blink_at(0.3)), 0.1, 2.15, hands=("fist", "fist"))
    with live(c, 960, 1080, phase=0.3, breathe=0.004):
        rim(c, b, 960, 400, 1.0, "#FFD08A", dx=6, dy=-6, a=0.9); draw(c, b, 960, 400, 1.0); shade_side(c, b, 960, 400, 0.45, 1260, 760, "#1A0C06")
    # koltuk kolçakları (oturduğu okunsun): kuzgun başlı uçlar
    arm = lambda x, sx: (f'<path d="M{x-90},1080 L{x-80},900 L{x+80},880 Q{x+sx*120},860 {x+sx*130},900 L{x+sx*110},930 L{x+80},930 L{x+90},1080 Z" fill="#5A3A22" stroke="{INK}" stroke-width="8" filter="url(#t_ahsap)"/>'
                         f'<path d="M{x-80},905 L{x+80},885" stroke="#C9962E" stroke-width="6"/><circle cx="{x+sx*104}" cy="{898}" r="6" fill="#E2B448" stroke="{INK}" stroke-width="2"/>')
    draw(c, svg_sprite(TEXD + arm(560, -1) + arm(1360, 1)), 0, 0, 1.0)
    bloom_spot(c, 960, 318, 150, "#FFE6A8", 0.30)                                      # taçta altın vurgu
    for k in range(60): q = R_(k + 880); c.drawCircle(q.uniform(200, 1700), q.uniform(80, 800), q.uniform(1.5, 3.5), skia.Paint(AntiAlias=True, Color4f=col("#FFC060", q.uniform(0.3, 0.8))))   # kıvılcım
    # ön plan: arkadan görünen diz çökmüş iki kişi (bulanık, kadrajı çerçeveler)
    fg = skia.Surface(W, H); fc = fg.getCanvas(); fc.clear(skia.ColorTRANSPARENT)
    for k, (x, sc) in enumerate(((150, 1.25), (1790, 1.25))):
        sp = full(dict(KL.soldier_spec(41 + k, "ragnar"), _kneel=130, _arm_up=False, _hand_extra="", _body_extra=""), "neutral", 0.85, facing=1 if k == 0 else -1, view="back")
        draw(fc, sp, x, 1260, sc); shade_side(fc, sp, x, 1260, 0.65, x, 960, "#0A0604")
    c.drawImage(fg.makeImageSnapshot(), 0, 0, skia.SamplingOptions(), skia.Paint(ImageFilter=skia.ImageFilters.Blur(7, 7)))
    card_at(c, "KRAL RAGNAR", 960, 120, "Kattegat ve ötesi", 0.85)
    finish(c, cold=False, warm=0.06); return s

# ================================================================== (A) e8 · halkla paylaşmak: kalabalık altın, kâse, gümüş alıyor
def e8():
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    draw(c, blurred(place(P7.greathall(0.7)), 4), -120, -60, 1.12)
    rays(c, 820, -40, 80, 1000, 26, 7, "#FFE0B0", 0.07, t or 0.0)
    # uzak sıra (küçük, solmuş), orta sıra, ön sıra: sevinçli halk
    rows = [(760, 0.46, ((1180, "man"), (1320, "woman"), (1460, "old"), (1600, "man"), (1740, "woman"), (1860, "man"), (300, "man"), (170, "woman")), 0.55),
            (850, 0.62, ((1120, "woman"), (1300, "man"), (1490, "hood"), (1680, "man"), (1840, "kid")), 0.8)]
    for y, sc, ppl, a_ in rows:
        for k, (x, kind) in enumerate(ppl):
            sp = dict(VK.civ(int(x) + int(y), kind)); up = (k % 2 == 0)
            if up: sp.update(_arm_up=True, _hand_extra=[RING_UP, SILVER, COINS][k % 3])
            f_ = -1 if x > 960 else 1
            d_ = full(sp, ex(["joy", "laugh", "tender", "awe"][k % 4], IF.blink_at(k * 0.7)), 0.9, facing=f_, look=-0.5 * f_)
            soft_shadow(c, x, y - 4, 110 * sc, 12 * sc, 0.35); rim(c, d_, x, y, sc, "#FFB070", dx=-4 * f_, dy=-3, a=0.6); draw(c, d_, x, y, sc)
            shade_side(c, d_, x, y, 0.3 + 0.3 * (1 - a_), x, x + 200 * f_, "#140A06")
    fill(c, "#2A1408", 0.08)
    draw(c, svg_sprite(f'<g transform="translate(1000,975) scale(1.15)">{RING_CHEST}</g>'), 0, 0, 1.0)   # açık sandık (halka #2)
    for x_ in (950, 1010, 1070, 1120): bloom_spot(c, x_, 890, 30, "#FFE6A0", 0.6)
    RGs = full(dict(RG, _arm_up=True, _hand_extra=RING_UP), ex("tender", IF.blink_at(0.2)), 1.0, facing=1, look=0.5)
    soft_shadow(c, 700, 1000, 170, 20, 0.5)
    with live(c, 700, 1010, phase=0.2, breathe=0.006):
        rim(c, RGs, 700, 1010, 1.0, "#FFC880", dx=5, dy=-4, a=0.75); draw(c, RGs, 700, 1010, 1.0); shade_side(c, RGs, 700, 1010, 0.45, 860, 520, "#140A06")
    # ön sıra: halka için uzanan iki kişi (büyük, net), kâseyi tutan kadın
    for k, (x, kind, extra, e) in enumerate(((1210, "man", RING_UP, "joy"), (1440, "woman", SILVER, "laugh"), (1700, "smith", COINS, "joy"))):
        sp = dict(VK.civ(900 + k, kind), _arm_up=True, _hand_extra=extra)
        d_ = full(sp, ex(e, IF.blink_at(k * 0.5 + 0.3)), 0.9, facing=-1, look=-0.6)
        soft_shadow(c, x, 1050, 150, 16, 0.45); rim(c, d_, x, 1060, 0.86, "#FFC070", dx=4, dy=-4, a=0.75); draw(c, d_, x, 1060, 0.86); shade_side(c, d_, x, 1060, 0.4, x, x + 220, "#120806")
    bloom_spot(c, 640, 330, 110, "#FFE6A0", 0.5); glow(c, 980, 1000, 560, "#FF8A3A", 0.22)
    for k in range(40): q = R_(k + 811); c.drawCircle(q.uniform(500, 1500), q.uniform(200, 900), q.uniform(1.5, 3), skia.Paint(AntiAlias=True, Color4f=col("#FFD070", q.uniform(0.3, 0.8))))
    # ön plan: masa kenarı, boynuz kadeh, gümüş yığını (bulanık)
    fgs = (TEXD + '<path d="M-20,1080 L-20,990 Q300,960 520,1000 L560,1080 Z" fill="#4A3020" stroke="#1A1410" stroke-width="8" filter="url(#t_ahsap)"/>'
           + K4.HORN_UP.replace("translate(HX,HY)", "translate(330,980) rotate(70) scale(1.2)")
           + "".join(f'<ellipse cx="{120+k*22}" cy="{985-(k%3)*8}" rx="16" ry="6" fill="#D4D8DC" stroke="#1A1410" stroke-width="3"/>' for k in range(7)))
    draw(c, blurred(svg_sprite(fgs), 6), 0, 0, 1.0)
    card_at(c, "JARL RAGNAR", 700, 150, "ganimeti halkla paylaşır", 0.85)
    finish(c, cold=False, warm=0.06); return s

# ================================================================== (A) f10 · Jarl düşüyor: öne yığılma, kalabalık şaşkın
def f10():
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    c.save(); c.translate(960, 540); c.rotate(-2.2); c.scale(1.06, 1.06); c.translate(-960, -580)
    draw(c, svg_sprite(VC.f10_bg()), 0, 0, 1.0)
    clouds = (cloud_band(104, 14, -200, 2100, 90, 330, "#5E6A78", "#8A96A2", 0.9, lit_dy=10, rx=(220, 460), ry=(40, 90))
              + cloud_band(105, 10, -200, 2100, 300, 470, "#9AA4AE", "#C4CCD2", 0.55, lit_dy=6, rx=(200, 420), ry=(14, 30)))
    draw(c, blurred(svg_sprite(clouds), 12), 0, 0, 1.0)
    glow(c, 560, 110, 300, "#F4EEDC", 0.25); rays(c, 560, 90, 72, 1000, 30, 8, "#F4F0E0", 0.06, t or 0.0)
    army(c, "ragnar", [(700, 0.36, 10, 0.12), (740, 0.46, 8, 0.06)], t, seed0=111, facing=1, x0=-40, x1=860)
    army(c, "ragnar", [(700, 0.36, 10, 0.12), (740, 0.46, 8, 0.06)], t, seed0=112, facing=-1, x0=1060, x1=1960)
    fill(c, "#C8D2DC", 0.06)
    # ön sıra kalabalık: şaşkın (ağız açık), Lagertha, Bjorn, Rollo + iki köylü
    for sp, x, y, f_, sc, e in ((LAGv, 250, 800, 1, 0.58, "shock"), (dict(BJv, _scale_child=True), 350, 808, 1, 0.50, "shock"), (KL.soldier_spec(171, "ragnar"), 1560, 806, -1, 0.56, "shock"),
                                (ROLLO, 1690, 800, -1, 0.60, "awe"), (KL.soldier_spec(172, "ragnar"), 140, 806, 1, 0.55, "awe")):
        d_ = full(sp, e, 0.9, facing=f_, look=0.7 * f_); rim(c, d_, x, y, sc, "#E8F0F8", dx=-3, dy=-2, a=0.5); draw(c, d_, x, y, sc)
    glow(c, 760, 960, 420, "#F6F0E0", 0.10)
    # Haraldson: dizlerinden öne yığılıyor (diz noktası etrafında döner; yüz karın üstünde, kan yok)
    HS = full(dict(HARALD, _kneel=150, _carry_svg="<g/>"), ex("pain", True), 1.0, facing=-1, look=-0.5)
    kx, ky = 1300, 1000
    soft_shadow(c, kx - 200, ky - 4, 300, 26, 0.5)
    c.save(); c.translate(kx, ky); c.rotate(-58); c.translate(-kx, -ky)
    rim(c, HS, kx, ky, 0.95, "#F2F6FA", dx=-6, dy=-4, a=0.8); draw(c, HS, kx, ky, 0.95); shade_side(c, HS, kx, ky, 0.55, kx - 100, kx + 260, "#1A2430")
    c.restore()
    draw(c, blurred(svg_sprite('<path d="M960,1000 Q1000,972 1060,978 Q1120,970 1160,996 Z" fill="#EEF3F6" opacity="0.85"/><path d="M970,996 Q1060,984 1150,994" stroke="#8E9EB0" stroke-width="3" fill="none" opacity="0.6"/>'), 2), 0, 0, 1.0)   # yığılmanın kardaki izi
    for k in range(26): q = R_(k + 1010); c.drawCircle(1040 + q.uniform(-60, 160), 940 + q.uniform(-50, 30), q.uniform(2, 6), skia.Paint(AntiAlias=True, Color4f=col("#F4F8FA", q.uniform(0.5, 0.9))))   # kar serpintisi
    sw = ('<g transform="translate(1560,1010) rotate(-170) scale(0.75)"><ellipse cx="0" cy="-12" rx="190" ry="14" fill="#6E7880" opacity="0.5"/>'
          '<path d="M-170,4 L120,-4 L150,2 L120,8 L-170,10 Z" fill="#C8D2DA" stroke="#1A1410" stroke-width="5"/><path d="M-160,2 L120,-2" stroke="#F4F8FC" stroke-width="2"/>'
          '<rect x="-196" y="-26" width="16" height="64" rx="4" fill="#8A7A5A" stroke="#1A1410" stroke-width="4"/><rect x="-250" y="-4" width="56" height="16" rx="5" fill="#4A2A1A" stroke="#1A1410" stroke-width="4"/><circle cx="-258" cy="4" r="11" fill="#C9A25A" stroke="#1A1410" stroke-width="4"/></g>')
    draw(c, svg_sprite(sw), 0, 0, 1.0)                                                 # elinden düşen kılıç (arkasında)
    RGs = full(dict(RG, _arm_up=False, _hand_extra=VC.AXE_DOWN), ex("coldv", IF.blink_at(0.2)), 1.0, facing=1, look=0.7)
    rx_, ry_ = 640, 1000
    soft_shadow(c, rx_ + 30, ry_ - 30, 190, 22, 0.5)
    with live(c, rx_, ry_, phase=0.2, breathe=0.006):
        rim(c, RGs, rx_, ry_, 1.02, "#FFF4DC", dx=-6, dy=-4, a=0.6); draw(c, RGs, rx_, ry_, 1.02); shade_side(c, RGs, rx_, ry_, 0.45, rx_ - 150, rx_ + 260, "#1A2430")
    VC.breath(c, rx_ + 40, 506, 0.9, 0.6)
    snowfall(c, t, (0, 70, W, H - 70), 140, seed=10)
    c.restore()
    draw(c, blurred(svg_sprite(VC.f10_fg()), 8), 0, 0, 1.0)
    for j in range(24):
        q = R_(j + 700); c.drawCircle(q.uniform(0, W), q.uniform(80, H - 80), q.uniform(5, 11), skia.Paint(AntiAlias=True, Color4f=col("#FFFFFF", 0.5), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 4)))
    fill(c, "#C8D2DC", 0.05); finish(c, cold=True); return s

# ================================================================== (B) k21b · fırtına filoyu yutuyor
def ship(x, y, s, rot, sail=True, mast_rot=0, sink=0.0, cid="sh"):
    """gemi.py tek kaynak: gövde + direk/yelken; sink: su çizgisinin altında kalan kısım kırpılır (y ekseninde yerel)."""
    m = (f'<g transform="rotate({mast_rot} 20 -60)">{G.mast_sail(1.6)}</g>' if sail else "")
    return f'<g transform="translate({x},{y}) rotate({rot}) scale({s})">{m}{G.hull(1.0, wet=True)}</g>'

def k21b():
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    sky = (VB.DEFS() + '<defs>' + gradient("s21s", [(0, "#0E1218"), (0.45, "#2A3440"), (0.8, "#46525C"), (1, "#5E6870")]) + '</defs><rect width="1920" height="760" fill="url(#s21s)"/>')
    draw(c, svg_sprite(sky), 0, 0, 1.0)
    draw(c, blurred(svg_sprite(cloud_band(2151, 16, -200, 2100, 20, 300, "#14181E", "#4A5662", 0.98, lit_dy=-8, rx=(260, 560), ry=(50, 110))
                               + cloud_band(2152, 12, -200, 2100, 260, 470, "#262E36", "#56626C", 0.85, lit_dy=-6, rx=(220, 480), ry=(30, 60))), 4), 0, 0, 1.0)
    # şimşek: bulut içinde çatallı, zemine iner (efekt katmanı flaşı ayrıca ekler)
    r = R_(2153); pts = [(1240, 120)]
    while pts[-1][1] < 600: pts.append((pts[-1][0] + r.uniform(-50, 40), pts[-1][1] + r.uniform(40, 80)))
    d = "M" + " L".join(f"{x:.0f},{y:.0f}" for x, y in pts); br = "M" + " L".join(f"{x:.0f},{y:.0f}" for x, y in [pts[3], (pts[3][0] + 70, pts[3][1] + 60), (pts[3][0] + 100, pts[3][1] + 140)])
    glow(c, 1240, 300, 520, "#BFD8FF", 0.30)
    draw(c, blurred(svg_sprite(f'<path d="{d}" stroke="#DCE8FF" stroke-width="22" fill="none"/><path d="{br}" stroke="#DCE8FF" stroke-width="14" fill="none"/>'), 10), 0, 0, 1.0)
    draw(c, svg_sprite(f'<path d="{d}" stroke="#FFFFFF" stroke-width="6" fill="none" stroke-linejoin="round"/><path d="{br}" stroke="#F4F8FF" stroke-width="3.5" fill="none"/>'), 0, 0, 1.0)
    # uzak deniz ve uzak batan gemi (küçük, solmuş): yalnız pruva ve direk dışarıda
    sea = [VB.DEFS(), '<defs>' + gradient("s21w", [(0, "#3A4A54"), (1, "#121C22")]) + '</defs><path d="M0,600 ' + " ".join(f"Q{x+60},{560 + 20*math.sin(x*0.03)} {x+120},600" for x in range(0, 1920, 120)) + ' L1920,1080 L0,1080 Z" fill="url(#s21w)"/>']
    for k in range(70): x = r.uniform(0, 1920); y = r.uniform(600, 760); sea.append(f'<path d="M{x:.0f},{y:.0f} q{r.uniform(20,40):.0f},-{r.uniform(6,14):.0f} {r.uniform(50,90):.0f},0" stroke="#A8BCC6" stroke-width="2.5" fill="none" opacity="{r.uniform(0.3,0.7):.2f}"/>')
    draw(c, svg_sprite("".join(sea)), 0, 0, 1.0)
    far = svg_sprite(f'<defs><clipPath id="cf"><rect x="0" y="0" width="1920" height="650"/></clipPath></defs><g clip-path="url(#cf)">{ship(330, 690, 0.42, -52, mast_rot=14)}</g>')
    draw(c, blurred(far, 1.5), 0, 0, 1.0, a=0.8); fill(c, "#3A4A58", 0.10)
    draw(c, svg_sprite(VB.big_wave(-100, 760, 1100, 300, seed=2154)), 0, 0, 1.0)                  # orta dalga sırtı (sol)
    # orta plan: devrilen gemi (direk kırık, omurga havada, dalga üstünde)
    mid = svg_sprite(f'<defs><clipPath id="cm"><rect x="0" y="0" width="1920" height="780"/></clipPath></defs><g clip-path="url(#cm)">{ship(1420, 720, 0.55, 152, sail=True, mast_rot=-30)}</g>')
    draw(c, mid, 0, 0, 1.0)
    draw(c, svg_sprite(VB.big_wave(900, 820, 1120, 240, seed=2155)), 0, 0, 1.0)
    # ön-orta: pruvası göğe kalkmış, kıçtan batan gemi; tayfa tutunuyor (model gövdeleri, küçük)
    c.save(); c.translate(820, 830); c.rotate(-36); c.translate(-820, -830)
    draw(c, svg_sprite(f'<g transform="translate(820,830) scale(0.78)">{G.mast_sail(1.9)}</g>'), 0, 0, 1.0)
    for k, x in enumerate((640, 760, 900, 1020)):
        sp = full(dict(KL.soldier_spec(2160 + k, "ragnar"), _arm_up=(k % 2 == 0), _hand_extra=""), "pain", 0.9, facing=1 if k % 2 else -1, look=0.3)
        draw(c, sp, x, 820, 0.36)
    draw(c, svg_sprite(f'<g transform="translate(820,830) scale(0.78)">{G.hull(1.0, wet=True)}</g>'), 0, 0, 1.0)
    c.restore()
    draw(c, svg_sprite(VB.DEFS() + VB.big_wave(-120, 900, 900, 400, seed=2157)), 0, 0, 1.0)            # kıçı yutan dalga
    # ön plan: dev dalga, köpük, kopan kürek ve kalkan (kadrajı çerçeveler); sağ üstte yağmur ve flaş için açık gök
    draw(c, svg_sprite(VB.DEFS() + VB.big_wave(-200, 1010, 2400, 260, seed=2156)), 0, 0, 1.0)
    fgx = (VP.broken_shield(1500, 1000, 0.8, "#8E1E22", "#E8D8B0", rot=24) + '<path d="M180,1040 L560,930" stroke="#1A1410" stroke-width="22" stroke-linecap="round"/><path d="M180,1040 L560,930" stroke="#8A6A46" stroke-width="13"/>')
    draw(c, blurred(svg_sprite(fgx), 3), 0, 0, 1.0)
    glow(c, 1240, 620, 600, "#9AC0E0", 0.14); fill(c, "#8AA4C0", 0.06)
    finish(c, cold=True); return s

# ================================================================== (B) b4 · dostun yerde yatıyor: haç Ragnar'a geçer
def b4():
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    draw(c, blurred(place(K3.P.longhouse(0.15) + K3.house_dressing() + K3.altar()), 5), 0, 0, 1.0)
    c.drawRect(skia.Rect(0, 0, W, H), skia.Paint(Color4f=col("#05060C", 0.42)))
    VA.beam(c, 1180, -40, 160, 1150, 1000, 620, "#DCE8F4", 0.22, 26)                 # duman deliğinden soğuk hüzme: bedenin üstüne düşer
    floor = (TEXD + '<path d="M0,880 L1920,880 L1920,1080 L0,1080 Z" fill="#2E241A" filter="url(#t_ahsap)"/>'
             + "".join(f'<path d="M0,{900+k*40} L1920,{896+k*42}" stroke="#1A120C" stroke-width="4" opacity="0.6"/>' for k in range(5))
             + "".join(f'<path d="M{x},{y} q12,-6 26,0" stroke="#B8A880" stroke-width="3" fill="none" opacity="0.6"/>' for x, y in ((300, 1020), (420, 960), (860, 1050), (1600, 940))))   # saman
    draw(c, svg_sprite(floor), 0, 0, 1.0)
    # Athelstan: kadraj kenarında yatıyor, başı sola; keten örtü göğse kadar, yüz sakin, gözler kapalı, yara görünmez
    AT = full(ATHv, ex("peace", True), 1.0, facing=1, look=0.0)
    hgt = 716 / 1.05 * 1.3; X, Y = 960 + hgt, 850                                     # baş ~x=1060+; ayaklar kadraj dışı
    soft_shadow(c, 1500, 1030, 640, 30, 0.6)
    c.save(); c.translate(X, Y); c.rotate(-90)
    rim(c, AT, 0, 0, 1.3, "#E8F0F8", dx=0, dy=-6, a=0.7); draw(c, AT, 0, 0, 1.3)
    c.restore()
    sh0 = 960 + 0.27 * hgt
    shroud = (TEXD + f'<g transform="translate({sh0 - 1170:.0f},0)"><path d="M1170,1030 Q1150,860 1230,700 Q1500,680 2400,700 L2400,1080 L1160,1080 Z" fill="#B8AA90" stroke="#1A1410" stroke-width="7" filter="url(#t_keten)"/>'
              + "".join(f'<path d="M{1240+k*80},{706+(k%2)*8} q24,120 8,330" stroke="#7A6C56" stroke-width="3" fill="none" opacity="0.8"/>' for k in range(9))
              + '<path d="M1230,720 Q1600,690 2400,710" stroke="#E8DCC0" stroke-width="6" fill="none" opacity="0.7"/>'
              + '<path d="M1172,1020 Q1150,860 1232,702" stroke="#5A4E40" stroke-width="12" fill="none"/></g>')
    draw(c, svg_sprite(shroud), 0, 0, 1.0)
    # Ragnar diz çökmüş, haçı yerden alıyor (sol el aşağıda, kordon sarkar)
    RK = fig_bust(dict(RG, _arm_up=True, _hand_extra=cross_held(1.5, 0)), ex("broken", IF.blink_at(0.6)), 0.7, 1.9)   # diz çökmüş (alçak kadraj), yerden aldığı haça bakar
    with live(c, 560, 1080, phase=0.6, breathe=0.008):
        rim(c, RK, 560, 470, 1.0, "#CFE4FF", dx=6, dy=-4, a=0.85); draw(c, RK, 560, 470, 1.0); shade_side(c, RK, 560, 470, 0.55, 300, 820, "#060810")
    bloom_spot(c, 1080, 860, 110, "#E8F0F8", 0.22)
    for k in range(40): q = R_(k + 404); c.drawCircle(q.uniform(1150, 1500), q.uniform(60, 900), q.uniform(1, 2.6), skia.Paint(AntiAlias=True, Color4f=col("#E8F0F8", q.uniform(0.2, 0.6))))   # hüzmede toz
    # ön plan: bulanık sandık ve mum (sol alt)
    draw(c, blurred(svg_sprite(TEXD + '<path d="M-20,1080 L-20,880 L230,880 L260,1080 Z" fill="#3A2818" stroke="#1A1410" stroke-width="8" filter="url(#t_ahsap)"/>' + VA.drip_candle(140, 880, 120, 26, lit=True, seed=4)), 7), 0, 0, 1.0)
    glow(c, 140, 740, 200, "#FFB060", 0.35)
    finish(c, cold=True); grade(c, "#8AA6C8", 0.12, "multiply"); letterbox(c, 1.0, 70); return s

# ================================================================== (B) k26b / k26c · yılan gölgeleri
def snake_shadows2(c, seed, n, box, a=0.85, lit=None):
    """Işık havuzuna düşen kıvrık yılan GÖLGELERİ: iki ucu incelen gövdesiz şerit; baş, ağız, diş yok."""
    r = R_(seed); x0, y0, x1, y1 = box; o = []
    for k in range(n):
        x = r.uniform(x0, x1); y = r.uniform(y0, y1); L = r.uniform(260, 420); amp = r.uniform(26, 46); ph = r.uniform(0, 6); rot = r.uniform(-20, 20); w0 = r.uniform(30, 44); turns = r.uniform(0.9, 1.4)
        pts = [(x + L * q - L / 2, y + amp * math.sin(ph + q * math.pi * 2 * turns) * (0.6 + 0.4 * q)) for q in [i / 40 for i in range(41)]]
        seg = "".join(f'<path d="M{pts[i][0]:.0f},{pts[i][1]:.0f} L{pts[i+1][0]:.0f},{pts[i+1][1]:.0f}" stroke-width="{w0 * math.sin(math.pi * (0.06 + 0.88 * i / 40)):.1f}"/>' for i in range(40))
        o.append(f'<g transform="rotate({rot:.0f} {x:.0f} {y:.0f})" stroke="#040606" stroke-linecap="round" fill="none" opacity="0.92">{seg}</g>')
    draw(c, blurred(svg_sprite("".join(o)), 7), 0, 0, 1.0, a=a)

def pit_pool(c, cx, cy, rx, ry, col_="#E8D8B0", a=0.55):
    """Çukur tabanında hüzmenin düştüğü ışık havuzu (yılan gölgeleri bunun üstüne düşer)."""
    draw(c, blurred(svg_sprite(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{col_}"/>'), 40), 0, 0, 1.0, a=a)

def _turet(mod, fname, newname, repls, inject=None):
    """Onaylı fonksiyonun kaynağından yeni adla kopya türetir (dosya değişmez). repls: [(eski, yeni)] tam metin eşleşmesi zorunlu."""
    fn = mod.FR[fname] if hasattr(mod, "FR") and fname in mod.FR else getattr(mod, fname)
    src = inspect.getsource(fn); src = src.replace(f"def {fname}(", f"def {newname}(", 1)
    for a, b in repls:
        assert a in src, f"{fname}: bulunamadı → {a[:60]}"; src = src.replace(a, b)
    for k, v in (inject or {}).items(): mod.__dict__[k] = v
    exec(compile(src, f"<{newname}>", "exec"), mod.__dict__); return mod.__dict__[newname]

def _k26b_pit(c):
    VA.beam(c, 1240, 420, 220, 1200, 960, 520, "#FFD8A0", 0.20, 30)
    pit_pool(c, 1200, 950, 460, 80, "#E0CC9A", 0.8)
    snake_shadows2(c, 2624, 5, (900, 915, 1500, 985), 0.9)
VS_k26b = _turet(VS, "k26b", "k26b_onarim", [('snake_shadows(c, 2624, 12, (700, 880, 1700, 1020), 0.9, "#8AAA80")', '_k26b_pit(c)')], {"_k26b_pit": _k26b_pit})

def k26c():
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]
    draw(c, blurred(svg_sprite(pit_walls(2631)), 2.4), 0, 0, 1.0); fill(c, "#0A0806", 0.30)
    # üstte çukurun ağzı: yağmurlu gri gök, taş dudak, aşağı bakan iki meşale
    mouth = (TEXD + '<ellipse cx="1000" cy="-60" rx="760" ry="250" fill="#5A6470"/><ellipse cx="1000" cy="-80" rx="700" ry="200" fill="#7A8692"/>'
             + "".join(f'<ellipse cx="{1000 + 770*math.cos(a):.0f}" cy="{-60 + 255*math.sin(a):.0f}" rx="{R_(int(a*100)).uniform(40,70):.0f}" ry="22" fill="#4A4238" stroke="#1A1410" stroke-width="4" filter="url(#t_tas)"/>' for a in [math.pi * k / 24 for k in range(0, 25)]))
    draw(c, blurred(svg_sprite(mouth), 3), 0, 0, 1.0)
    for x in (560, 1450): VS.torch(c, x, 120, t, 1.0); glow(c, x, 120, 220, "#FF9A40", 0.35)
    VA.beam(c, 1040, -40, 520, 980, 1080, 980, "#FFF4D8", 0.30, 26); glow(c, 1000, 360, 620, "#FFE8C0", 0.30)
    pit_pool(c, 980, 1010, 760, 130, "#E0CC9A", 0.7)
    snake_shadows2(c, 2633, 3, (200, 960, 640, 1040), 0.85); snake_shadows2(c, 2634, 3, (1320, 960, 1760, 1040), 0.85)
    # Ragnar (RG4): çukurun içinde, omuz ve göğüs görünür, başı ışığa kalkık
    b = ragnar_bust(c, VS.RGO, "gelecek", 1000, 470, 2.0, look=0.4, rimc="#FFF0D0", shx=(760, 1040), shc="#0A0806", rot=-6, phase=1.0)
    snake_shadows2(c, 2635, 2, (760, 940, 1240, 1000), 0.7)                                   # göğsün önünden geçen gölgeler
    bloom_spot(c, 1040, 380, 140, "#FFF4DC", 0.20)
    for k in range(70): q = R_(k + 2632); c.drawCircle(q.uniform(600, 1400), q.uniform(80, 900), q.uniform(1, 3), skia.Paint(AntiAlias=True, Color4f=col("#FFF4DC", q.uniform(0.15, 0.6))))
    rain(c, 2636, 260, box=(500, 0, 1500, 700), ang=6, a=(0.08, 0.2), L=(30, 60))
    vign(c, 0.52, 0.45, 0.66, 0.9, "#030202", 0.42)
    finish(c, cold=False, warm=0.05); return s

# ================================================================== (B) e4i · güneş taşı insert: elde taş, bulutlu gök, yön veren ışık noktası
def e4i():
    s = skia.Surface(W, H); c = s.getCanvas(); t = T[0]; tt = t or 0
    sky = (VB.DEFS() + '<defs>' + gradient("s4i", [(0, "#3E4A58"), (0.5, "#6E7C88"), (1, "#9AA6AE")]) + '</defs><rect width="1920" height="1080" fill="url(#s4i)"/>')
    draw(c, svg_sprite(sky), 0, 0, 1.0)
    draw(c, blurred(svg_sprite(cloud_band(4411, 16, -200, 2100, 0, 420, "#3A4450", "#8A98A4", 0.95, lit_dy=-8, rx=(240, 520), ry=(40, 90))
                               + cloud_band(4412, 12, -200, 2100, 360, 620, "#5A6672", "#A8B4BC", 0.8, lit_dy=-6, rx=(220, 460), ry=(20, 50))), 5), 0, 0, 1.0)
    glow(c, 1560, 210, 220, "#F4ECD0", 0.18)                                                    # bulut ardında gizli güneş: gözle görünmez
    sea = (VB.DEFS() + '<defs>' + gradient("s4w", [(0, "#4A5A64"), (1, "#1A262E")]) + '</defs><path d="M0,690 L1920,670 L1920,1080 L0,1080 Z" fill="url(#s4w)"/>'
           + VB.big_wave(1000, 760, 900, 120, seed=4413))
    draw(c, blurred(svg_sprite(sea), 3), 0, 0, 1.0)
    # orta plan: geminin küpeştesi, kalkan sırası ve halat (gemi.py kalkan rengi)
    rail = (TEXD + '<path d="M-20,880 Q900,820 1940,860 L1940,1080 L-20,1080 Z" fill="#5A3E26" stroke="#1A1410" stroke-width="8" filter="url(#t_ahsap)"/>'
            + "".join(f'<path d="M-20,{900+k*36} Q900,{840+k*36} 1940,{880+k*36}" stroke="#2A1A10" stroke-width="5" fill="none"/>' for k in range(5))
            + "".join(f'<circle cx="{x+1}" cy="{y+1}" r="5" fill="#2A2A2A"/>' for x, y in ((200, 900), (520, 880), (1300, 880), (1600, 890)))
            + "".join(f'<g transform="translate({x},{1180 + 0.00006*(x-900)**2:.0f}) scale(0.62)">{KL.shield_svg(a, b, style=k % 3).replace("translate(70,-330) scale(0.62)", "translate(0,0)")}</g>'
                      for k, (x, a, b) in enumerate(((1200, "#8E3B2E", "#D8C8A0"), (1420, "#2F4C6E", "#C9A25A"), (1640, "#5A6A3A", "#D8C8A0"), (1860, "#8E3B2E", "#D8C8A0"))))
            + '<path d="M1100,700 Q1300,820 1500,860" stroke="#3A2A1A" stroke-width="8" fill="none"/>')
    draw(c, blurred(svg_sprite(rail), 2), 0, 0, 1.0)
    # Ragnar (RG1) yakın: taşı göğe kaldırmış (e2'deki SUNSTONE, aynı model), kadrajda kol ve el baskın
    st = f'<g transform="translate(HX,HY) translate(0,-34) scale(0.8)">{SUNSTONE}</g>'
    b = fig_bust(dict(RG, _arm_up=True, _hand_extra=st), ex("determined", IF.blink_at(0.3)), 0.8, 3.0)
    hx, hy = hand_at(dict(RG, _arm_up=True), lambda sp: fig_bust(sp, "determined", 0.8, 3.0))
    bx, by = 1180 - hx, 420 - hy                                                             # taş ~ (1180,420)
    with live(c, bx, by + 600, phase=0.3, breathe=0.004):
        rim(c, b, bx, by, 1.0, "#E8F0F8", dx=8, dy=-6, a=0.7); draw(c, b, bx, by, 1.0); shade_side(c, b, bx, by, 0.5, bx + 300, bx - 300, "#0E1620")
    # taşın içinde yön veren ışık noktası + gizli güneşe giden ince çizgi
    sx, sy = 1180, 420 - 40
    rays(c, sx, sy, -24, 420, 6, 3, "#FFF2C8", 0.18, tt)
    bloom_spot(c, sx, sy, 60, "#FFF2C8", 0.55); bloom_spot(c, sx, sy, 16, "#FFFFFF", 1.0)
    for k in range(30): q = R_(k + 4414); c.drawCircle(sx + q.uniform(-80, 80), sy + q.uniform(-70, 70), q.uniform(1, 3), skia.Paint(AntiAlias=True, Color4f=col("#FFF6D8", q.uniform(0.3, 0.8))))
    draw(c, place("".join(f'<path d="M{R_(k).uniform(0,W):.0f},{R_(k+99).uniform(0,H):.0f} l-8,30" stroke="#D8E4EC" stroke-width="2" opacity="0.4"/>' for k in range(120))), 0, 0, 1.0)   # ince serpinti
    card_at(c, "GÜNEŞ TAŞI", 1180, 140, "bulutlu günde güneşi bulur", 0.8)
    finish(c, cold=True); return s

# ================================================================== (C) ifade ve jest notları: onaylı kaynaktan ifade değişimi
def _c_variants():
    out = {}
    out["d2"] = _turet(K4, "d2", "d2_c", [('ex("broken", IF.blink_at(0.5))', '"closed_tear"')])
    out["d7"] = _turet(K4, "d7", "d7_c", [('RGf = full(RG, "fierce", 1.0, look=0.6)', 'RGf = full(RG, "sly_half", 1.0, look=0.5)')])
    out["e6"] = _turet(K5, "e6", "e6_c", [('ex("curious", IF.blink_at(0.2)), 0.6, 1.7)', 'ex("soften", IF.blink_at(0.2)), 0.7, 1.7)')])
    out["e4"] = _turet(K5, "e4", "e4_c", [('ex("pray", IF.blink_at(0.2))', 'ex("determined", IF.blink_at(0.2))'), ('ex("laugh", IF.blink_at(0.5)), 0.6, facing=1, look=0.8)', 'ex("laugh", IF.blink_at(0.5)), 0.6, facing=1, look=-0.6)')])
    out["k23b"] = _turet(VS, "k23b", "k23b_c", [('ex("fierce", IF.blink_at(4.0))', 'ex("squint_smirk", IF.blink_at(4.0))')])
    return out
CV = _c_variants()

FR = {"d8": d8, "e8": e8, "f10": f10, "k21b": k21b, "b4": b4, "k26b": VS_k26b, "k26c": k26c, "e4i": e4i,
      "d2c": CV["d2"], "d7c": CV["d7"], "e6c": CV["e6"], "e4c": CV["e4"], "k23bc": CV["k23b"]}
EVRE = {"d8": YAS.RG2, "e8": YAS.RG1, "f10": YAS.RG1, "k21b": YAS.RG3, "b4": YAS.RG2, "k26b": YAS.RG4, "k26c": YAS.RG4, "e4i": YAS.RG1,
        "d2c": YAS.RG2, "d7c": YAS.RG2, "e6c": YAS.RG1, "e4c": YAS.RG1, "k23bc": YAS.RG4}
ONCE = {"d8": "bedel/d8.png", "e8": "bati/e8.png", "f10": "bati/v3/f10.png", "k21b": "kayip/k21b.png", "b4": "kesis/b4.png", "k26b": "son/k26b.png", "k26c": "son/k26c.png",
        "e4i": "bati/e2.png", "d2c": "bedel/d2.png", "d7c": "bedel/d7.png", "e6c": "bati/e6.png", "e4c": "bati/e4.png", "k23bc": "son/k23b.png"}
CROPS = {"d8": [(640, 120, 1280, 480), (420, 760, 1500, 1080)], "e8": [(480, 120, 1000, 560), (1050, 560, 1850, 1060)], "f10": [(940, 700, 1500, 1060), (440, 380, 900, 1060)],
         "k21b": [(440, 300, 1260, 900), (1060, 420, 1860, 860)], "b4": [(560, 520, 1160, 1060), (1100, 760, 1920, 1080)], "k26b": [(800, 820, 1600, 1040), (180, 120, 700, 700)],
         "k26c": [(700, 160, 1300, 760), (100, 900, 900, 1080)], "e4i": [(900, 160, 1460, 640), (600, 400, 1300, 1000)]}

def contact(ids, name):
    from PIL import Image, ImageDraw
    cw, ch = 960, 540; sheet = Image.new("RGB", (cw * 2 + 30, (ch + 40) * len(ids) + 10), "#EDE2CC"); d = ImageDraw.Draw(sheet)
    for k, i in enumerate(ids):
        y = 10 + k * (ch + 40); d.text((14, y), f"{i} · ÖNCE ({ONCE[i]})", fill="#1A1410"); d.text((cw + 24, y), f"{i} · SONRA (taslak)", fill="#1A1410")
        sheet.paste(Image.open(f"/home/claude/r3/{ONCE[i]}").convert("RGB").resize((cw, ch)), (10, y + 22))
        sheet.paste(Image.open(f"{OUTS}/{i}.png").convert("RGB").resize((cw, ch)), (cw + 20, y + 22))
    sheet.save(f"{OUTS}/{name}")

if __name__ == "__main__":
    ids = sys.argv[1:] or list(FR)
    for i in ids:
        YAS.uygula(EVRE[i]); T[0] = None; p = f"{OUTS}/{i}.png"
        FR[i]().makeImageSnapshot().save(p, skia.kPNG); print("kare", i, flush=True)
        for k, b in enumerate(CROPS.get(i, []), 1): crop2x_(p, b, f"{OUTS}/{i}_crop{k}.png")
