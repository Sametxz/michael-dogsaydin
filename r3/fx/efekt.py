"""Efekt kütüphanesi: onaylı kareler değişmez, üstüne zamana bağlı hareket katmanı eklenir.
Animatik compose() içinde, kamera dönüşümü açıkken çağrılır:  FX.uygula(c, cekim_id, t, st)   (st: {satır_no: başlangıç saniyesi})
Sarsıntı için compose başında:  dx, dy = FX.sarsinti(cekim_id, t, st)

İşaretler: /home/claude/r3/fx/isaretler.json → [{"cekim": "f4", "fx": [{"tur": "ravens", "at": "L5+0.4", ...}, ...]}, ...]
Türler ve parametreler (koordinatlar 1920×1080 kare uzayında):
  fire        x, y, olcek=1, sure=∞           titreyen alev dili + sıcak ışık
  embers      alan=[x0,y0,x1,y1], adet=40      yükselen kıvılcımlar
  smoke       alan=[...], adet=10              yavaş yükselen duman
  ravens      yol=[[x0,y0],[x1,y1]], adet=2, sure=4, olcek=1   kanat çırparak uçan kuzgunlar (onaylı v3_b.raven)
  arrows      kaynak=[x,y], hedef=[x,y], adet=12, sure=1.2     kavisli ok yağmuru
  spear       kaynak=[x,y], hedef=[x,y], sure=0.7              atılan mızrak
  shake       siddet=12, sure=0.5                              kamera sarsıntısı (sarsinti() ile)
  flash       renk="#FFFFFF", sure=0.3, guc=0.8                ani ışık
  light_flicker x, y, r=400, renk="#FFB060"                    mum/meşale ışık titreşimi
  rain / snow / dust   adet                                    tüm kare
"""
import json, math, os, random, sys
import skia
sys.path[:0] = ["/home/claude/r3/bati", "/home/claude/r3", "/home/claude/r2"]
from engine import col, sprite, draw
W, H = 1920, 1080
ISARET = "/home/claude/r3/fx/isaretler.json"
_CUES = None; _SPR = {}
BOLUM = [None]   # animatik betiği kendi bölümünü yazar: FX.BOLUM[0] = "VI"  (aynı çekim kimliği iki bölümde geçebiliyor)

def cues():
    """{çekim: [efekt...]}: yalnız bu bölümün işaretleri; bölüm yazılmamışsa hepsi."""
    global _CUES
    if _CUES is None:
        _CUES = {}
        if os.path.exists(ISARET):
            for e in json.load(open(ISARET)):
                if BOLUM[0] is None or e.get("bolum") == BOLUM[0]:
                    _CUES.setdefault(e.get("cekim"), []).extend(e.get("fx", []))
    return _CUES

def zaman(at, st):
    """'L5+0.4' → 5. satırın başı + 0.4 sn; 'S+1.2' → çekim başı + 1.2 sn."""
    at = str(at or "S+0").replace(" ", "")
    base, _, off = at.partition("+"); off = float(off or 0)
    if base.startswith("L"):
        n = int(base[1:]); return st.get(n, 0.0) + off
    return off

def _p(col_hex, a): return skia.Paint(AntiAlias=True, Color4f=col(col_hex, max(0.0, min(1.0, a))))

# ---------------------------------------------------------------- efektler
def fire(c, t, t0, x, y, olcek=1.0, sure=None, **_):
    if t < t0 or (sure and t > t0 + sure): return
    g = min(1.0, (t - t0) / 0.4); o = olcek
    c.drawCircle(x, y - 40 * o, 190 * o, skia.Paint(Color4f=col("#FF8A30", 0.22 * g * (0.85 + 0.15 * math.sin(t * 9))),
                 MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 70 * o), BlendMode=skia.BlendMode.kScreen))
    # üç katman: dış kızıl, orta turuncu, iç sarı çekirdek; her dil ayrı fazda
    for katman, (renk, hs, ws, a, bl) in enumerate([("#C23A12", 1.0, 1.0, 0.9, 3), ("#F07A2A", 0.78, 0.75, 0.9, 2.5), ("#FFD27A", 0.5, 0.45, 0.95, 2)]):
        for k in range(6):
            ph = t * (6.5 + k * 0.9) + k * 2.1 + katman; h = (105 + 34 * math.sin(ph) + 12 * math.sin(ph * 2.3)) * o * hs * g * (1 - abs(k - 2.5) * 0.12)
            w = 22 * o * ws; dx = (k - 2.5) * 13 * o * ws; sway = 9 * o * math.sin(ph * 1.4)
            p = skia.Path(); p.moveTo(x + dx - w, y); p.cubicTo(x + dx - w, y - h * 0.5, x + dx + sway - w * 0.2, y - h * 0.75, x + dx + sway, y - h)
            p.cubicTo(x + dx + sway + w * 0.2, y - h * 0.75, x + dx + w, y - h * 0.5, x + dx + w, y); p.close()
            c.drawPath(p, skia.Paint(AntiAlias=True, Color4f=col(renk, a), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, bl * o)))
    c.drawOval(skia.Rect(x - 50 * o, y - 10 * o, x + 50 * o, y + 8 * o), _p("#FFC870", 0.25 * g))

def embers(c, t, t0, alan=(0, 600, 1920, 1080), adet=40, **_):
    if t < t0: return
    x0, y0, x1, y1 = alan; r = random.Random(11)
    for i in range(int(adet)):
        sx, sp, ph = r.uniform(x0, x1), r.uniform(40, 120), r.uniform(0, 10)
        life = ((t - t0) * sp / (y1 - y0 + 1) + ph) % 1.0
        x = sx + 20 * math.sin(t * 2 + ph); y = y1 - life * (y1 - y0)
        c.drawCircle(x, y, 2.4 * (1 - life) + 0.8, _p("#FFB040", (1 - life) * 0.9))

def smoke(c, t, t0, alan=(0, 300, 1920, 900), adet=10, **_):
    if t < t0: return
    x0, y0, x1, y1 = alan; r = random.Random(5); g = min(1.0, (t - t0) / 1.5)
    for i in range(int(adet)):
        sx, ph, rad = r.uniform(x0, x1), r.uniform(0, 1), r.uniform(60, 160)
        life = ((t - t0) * 0.08 + ph) % 1.0
        c.drawCircle(sx + 40 * math.sin(t * 0.3 + i), y1 - life * (y1 - y0), rad * (0.6 + life),
                     skia.Paint(Color4f=col("#8A8A90", 0.18 * g * math.sin(math.pi * life)), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 30)))

def _raven_sprite(olcek):
    key = ("raven", round(olcek, 2))
    if key not in _SPR:
        import v3_b
        svg = v3_b.raven(160, 120, olcek, 1, "fly", 1)
        _SPR[key] = sprite(svg, 320, 240, 160, 120, 1.0)
    return _SPR[key]

def ravens(c, t, t0, yol=((-100, 300), (2000, 200)), adet=2, sure=4.0, olcek=0.45, kaynak=None, hedef=None, **_):
    """Kareye ait kuzgunlar gibi üstten görünüş: uçuş yönüne döner, kanat açıklığı çırpınır (k26d ile aynı dil)."""
    if kaynak and hedef: yol = (kaynak, hedef)
    if t < t0 or t > t0 + sure + 1.0: return
    (xa, ya), (xb, yb) = yol; sp = _raven_sprite(min(olcek, 0.7))
    for i in range(int(adet)):
        q = (t - t0 - i * 0.35) / sure
        if not 0 <= q <= 1: continue
        def pos(q): return (xa + (xb - xa) * q + i * 70, ya + (yb - ya) * q - 60 * math.sin(math.pi * q) + i * 40 + 12 * math.sin(q * 9 + i))
        x, y = pos(q); x2, y2 = pos(min(1, q + 0.01) if q < 1 else q); x1_, y1_ = pos(max(0, q - 0.01))
        rot = math.degrees(math.atan2(y2 - y1_, x2 - x1_)) + 90
        flap = 0.62 + 0.38 * abs(math.sin((t - t0) * (5.5 + i * 0.8) + i * 1.9)); s_i = 1.0 - 0.14 * i
        draw(c, sp, x, y, s_i, rot=rot, sx=flap * s_i, sy=s_i)

def _bez(p0, p1, q, lift):
    (x0, y0), (x1, y1) = p0, p1; mx, my = (x0 + x1) / 2, min(y0, y1) - lift
    return ((1 - q) ** 2 * x0 + 2 * (1 - q) * q * mx + q * q * x1, (1 - q) ** 2 * y0 + 2 * (1 - q) * q * my + q * q * y1)

def _shaft(c, x, y, ang, L, w, colr="#5A4028", tip="#B8C0C8"):
    c.save(); c.translate(x, y); c.rotate(math.degrees(ang))
    c.drawLine(-L, 0, 0, 0, skia.Paint(AntiAlias=True, Color4f=col("#1A1410"), StrokeWidth=w + 3, StrokeCap=skia.Paint.kRound_Cap))
    c.drawLine(-L, 0, 0, 0, skia.Paint(AntiAlias=True, Color4f=col(colr), StrokeWidth=w, StrokeCap=skia.Paint.kRound_Cap))
    tri = skia.Path(); tri.moveTo(10 + w, 0); tri.lineTo(-6, -w - 3); tri.lineTo(-6, w + 3); tri.close(); c.drawPath(tri, _p(tip, 1))
    c.restore()

def arrows(c, t, t0, kaynak=(200, 900), hedef=(1500, 700), adet=12, sure=1.2, **_):
    if t < t0 or t > t0 + sure + 0.6: return
    r = random.Random(7)
    for i in range(int(adet)):
        d0 = r.uniform(0, 0.5); q = (t - t0 - d0) / sure
        if not 0 <= q <= 1: continue
        p0 = (kaynak[0] + r.uniform(-120, 120), kaynak[1] + r.uniform(-40, 40)); p1 = (hedef[0] + r.uniform(-200, 200), hedef[1] + r.uniform(-60, 60))
        x, y = _bez(p0, p1, q, 260); x2, y2 = _bez(p0, p1, min(1, q + 0.02), 260)
        _shaft(c, x, y, math.atan2(y2 - y, x2 - x), 46, 3)

def spear(c, t, t0, kaynak=(300, 700), hedef=(1400, 650), sure=0.7, **_):
    if t < t0: return
    q = min(1.0, (t - t0) / sure); x, y = _bez(kaynak, hedef, q, 140); x2, y2 = _bez(kaynak, hedef, min(1, q + 0.02), 140)
    ang = math.atan2(y2 - y, x2 - x) if q < 1 else math.atan2(hedef[1] - _bez(kaynak, hedef, 0.97, 140)[1], hedef[0] - _bez(kaynak, hedef, 0.97, 140)[0])
    _shaft(c, x, y, ang, 150, 6)

def flash(c, t, t0, renk="#FFFFFF", sure=0.3, guc=0.8, **_):
    if t0 <= t <= t0 + sure:
        c.drawRect(skia.Rect(-200, -200, W + 200, H + 200), _p(renk, guc * (1 - (t - t0) / sure)))

def light_flicker(c, t, t0, x=960, y=540, r=400, renk="#FFB060", **_):
    if t < t0: return
    a = 0.10 + 0.06 * math.sin(t * 11) + 0.04 * math.sin(t * 23 + 1)
    c.drawCircle(x, y, r, skia.Paint(Color4f=col(renk, a), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, r * 0.3), BlendMode=skia.BlendMode.kScreen))

def _parcacik(c, t, adet, hiz, uzun, renk, a, seed, ruzgar=0.0):
    r = random.Random(seed)
    for i in range(int(adet)):
        x0, ph = r.uniform(-100, W + 100), r.uniform(0, 1)
        q = (t * hiz / H + ph) % 1.0; y = q * (H + 100) - 50; x = x0 + ruzgar * q * 200 + (15 * math.sin(t + i) if uzun == 0 else 0)
        if uzun: c.drawLine(x, y, x - 8, y + uzun, skia.Paint(AntiAlias=True, Color4f=col(renk, a), StrokeWidth=1.6))
        else: c.drawCircle(x, y, r.uniform(1.5, 3.5), _p(renk, a))

def rain(c, t, t0, adet=220, **_):
    if t >= t0: _parcacik(c, t, adet, 1600, 34, "#B8C8D8", 0.45, 3, 0.2)
def snow(c, t, t0, adet=120, **_):
    if t >= t0: _parcacik(c, t, adet, 70, 0, "#F2F6FA", 0.8, 4)
def dust(c, t, t0, adet=60, **_):
    if t >= t0: _parcacik(c, t, adet, 25, 0, "#E8D8B0", 0.35, 5)

FX = {"fire": fire, "embers": embers, "smoke": smoke, "ravens": ravens, "arrows": arrows, "spear": spear, "flash": flash,
      "light_flicker": light_flicker, "rain": rain, "snow": snow, "dust": dust}

def uygula(c, cekim, t, st):
    for e in cues().get(cekim, []):
        f = FX.get(e.get("tur"))
        if f:
            prm = {k: v for k, v in e.items() if k not in ("tur", "at")}
            try: f(c, t, zaman(e.get("at"), st), **prm)
            except Exception as ex: print("fx hata", cekim, e.get("tur"), ex)

def sarsinti(cekim, t, st):
    dx = dy = 0.0
    for e in cues().get(cekim, []):
        if e.get("tur") == "shake":
            t0 = zaman(e.get("at"), st); s = e.get("sure", 0.5); g = e.get("siddet", 12)
            if t0 <= t <= t0 + s:
                k = 1 - (t - t0) / s; dx += g * k * math.sin(t * 90); dy += g * k * math.cos(t * 77)
    return dx, dy
