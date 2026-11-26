"""Dinamik sahne motoru: katmanlı çekim, hareket izleri, kelime kilidi, kamera ve paralaks.

Ragnar projesindeki sorun: her çekim tek bir düzleştirilmiş kareydi (`makeImageSnapshot`) + yavaş zoom + siyaha kararma.
Burada çekim bir SAHNE GRAFİĞİDİR: her öğe kendi katmanında, kendi derinliğinde ve kendi hareket iziyle yaşar;
anlatıdaki kelime geldiğinde öğe sahneye GİRER ya da EYLEM yapar; çekimden çekime anlamsal geçişle (gecis.py) akılır.

Temel kavramlar
- Iz        : anahtar kareli sayı/demet izi. Iz([(0, 0), (1.2, 300, "out")])
- Oge       : çizilen her şey (karakter, nesne, ışık, efekt). derinlik: 0 = sonsuz uzak, 1 = ana düzlem, >1 ön plan.
- Cekim     : öğeler + kamera + kelime zamanları + duygu (grade). render(c, t)
- Film      : çekimler + aralarındaki geçişler → mp4 (gecis.py içindeki Film)

Kullanım özeti (bkz. ornek/demo.py):
    ck = Cekim("ev_dis", sure=4.0, kelimeler=[("pencerede", 1.1, 1.6)])
    ck.ekle(Oge("gok", ciz_gok, derinlik=0.05))
    ck.ekle(Oge("isik", ciz_isik, derinlik=1, giris=("parla", ck.k("pencerede"))))
    ck.kamera = Kamera(zoom=Iz([(0, 1.0), (4, 1.12, "io")]), x=Iz([(0, 960), (4, 1010)]))
"""
import math, os, hashlib, subprocess, re
import skia

W, H, FPS = 1920, 1080, 30
CACHE = os.environ.get("STUDYO_CACHE", os.path.join(os.path.dirname(__file__), ".cache"))
os.makedirs(CACHE, exist_ok=True)
SAMP = skia.SamplingOptions(skia.FilterMode.kLinear, skia.MipmapMode.kLinear)

# ───────── eğriler
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def lin(t, t0, t1): return clamp((t - t0) / max(1e-6, t1 - t0))
EASE = {
    "lin": lambda p: p,
    "io": lambda p: p * p * (3 - 2 * p),
    "out": lambda p: 1 - (1 - p) ** 3,
    "in": lambda p: p ** 3,
    "back": lambda p: 1 + 2.70158 * (p - 1) ** 3 + 1.70158 * (p - 1) ** 2,          # hafif taşma
    "bounce": lambda p: 1 - abs(math.cos(p * math.pi * 2.5)) * (1 - p) ** 2,          # düşüp sekme
    "expo": lambda p: 1 - 2 ** (-10 * p) if p < 1 else 1.0,
}
def ease(name, p): return EASE[name](clamp(p))

def hexcol(h, a=1.0):
    h = h.lstrip("#"); r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    return skia.Color4f(r, g, b, a)
def paint(h, a=1.0, **kw): return skia.Paint(AntiAlias=True, Color4f=hexcol(h, a), **kw)


class Iz:
    """Anahtar kareli iz. kare: (t, değer[, eğri]). Değer sayı ya da demet olabilir. Eğri, o kareye VARIŞ eğrisidir."""
    def __init__(self, kareler):
        if not isinstance(kareler, (list, tuple)) or not kareler or not isinstance(kareler[0], (list, tuple)):
            kareler = [(0, kareler)]
        self.k = sorted([(k[0], k[1], k[2] if len(k) > 2 else "io") for k in kareler], key=lambda k: k[0])
    def __call__(self, t):
        k = self.k
        if t <= k[0][0]: return k[0][1]
        for (t0, v0, _), (t1, v1, e) in zip(k, k[1:]):
            if t <= t1:
                p = ease(e, (t - t0) / max(1e-6, t1 - t0))
                if isinstance(v0, (tuple, list)): return tuple(a + (b - a) * p for a, b in zip(v0, v1))
                return v0 + (v1 - v0) * p
        return k[-1][1]
def sabit(v): return Iz([(0, v)])


# ───────── sprite (SVG → PNG önbellek; art3 gibi SVG üreten modellerle uyumlu)
class Sprite:
    def __init__(self, img, w, h, ax, ay, ss): self.img, self.w, self.h, self.ax, self.ay, self.ss = img, w, h, ax, ay, ss
_mem = {}
def svg_sprite(body, w, h, ax=None, ay=None, ss=1.0, defs=""):
    norm = re.sub(r'((?:id="|url\(#))([A-Za-z_]+?)(\d+)', r'\1\2#', body)
    key = hashlib.md5(f"{w}x{h}@{ss}|{defs}|{norm}".encode()).hexdigest()
    if key in _mem: return _mem[key]
    png = f"{CACHE}/{key}.png"
    if not os.path.exists(png):
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{int(w * ss)}" height="{int(h * ss)}" viewBox="0 0 {w} {h}">{defs}{body}</svg>')
        subprocess.run(["rsvg-convert", "-o", png + ".tmp"], input=svg.encode(), check=True); os.replace(png + ".tmp", png)
    sp = Sprite(skia.Image.open(png).makeRasterImage(), w, h, w / 2 if ax is None else ax, h / 2 if ay is None else ay, ss)
    _mem[key] = sp; return sp

def draw_sprite(c, sp, a=1.0):
    """Sprite'ı (0,0) çapasına çizer; konum/ölçek Oge dönüşümünden gelir."""
    p = None
    if a < 0.999: p = skia.Paint(); p.setAlphaf(clamp(a))
    c.save(); c.scale(1 / sp.ss, 1 / sp.ss); c.drawImage(sp.img, -sp.ax * sp.ss, -sp.ay * sp.ss, SAMP, p); c.restore()


# ───────── giriş/çıkış ve ikincil hareket kalıpları
# Her kalıp (ilerleme p ∈ [0,1]) → dönüşüm değişiklikleri sözlüğü döndürür. Kelime zamanında başlar.
def _giris(tur, p):
    if tur == "pop":     s = ease("back", p); return dict(s=max(0.0, s), a=clamp(p * 3))
    if tur == "dus":     return dict(dy=-(1 - ease("bounce", p)) * 420, a=clamp(p * 4))
    if tur == "kay_sol": return dict(dx=-(1 - ease("out", p)) * 900, a=clamp(p * 2))
    if tur == "kay_sag": return dict(dx=(1 - ease("out", p)) * 900, a=clamp(p * 2))
    if tur == "yuksel":  return dict(dy=(1 - ease("out", p)) * 260, a=ease("out", p))
    if tur == "belir":   return dict(a=ease("io", p))
    if tur == "parla":   return dict(a=ease("out", p), parlama=math.sin(p * math.pi) * 0.9)
    if tur == "ciz":     return dict(kirp=ease("io", p))                       # soldan sağa çizilerek açılır (harita, yol, yazı)
    if tur == "buyu":    return dict(s=0.2 + 0.8 * ease("out", p), a=clamp(p * 2))
    raise ValueError(tur)

def ikincil(tur, t, guc=1.0, faz=0.0):
    """Sürekli yaşam hareketi: hiçbir öğe tamamen donuk kalmaz."""
    if tur == "nefes":   return dict(sy=1 + 0.008 * guc * math.sin(2 * math.pi * 0.25 * t + faz))
    if tur == "salin":   return dict(rot=1.2 * guc * math.sin(2 * math.pi * 0.35 * t + faz))
    if tur == "titre":   return dict(dx=1.5 * guc * math.sin(53 * t + faz), dy=1.5 * guc * math.cos(47 * t + faz))
    if tur == "suz":     return dict(dy=6 * guc * math.sin(2 * math.pi * 0.2 * t + faz))
    if tur == "alev":    return dict(sy=1 + 0.06 * guc * math.sin(17 * t + faz) * math.sin(5 * t), a=0.85 + 0.15 * math.sin(11 * t + faz))
    return {}


class Oge:
    """Sahnede çizilen tek bir şey.
    ciz(c, t, o) → öğeyi yerel (0,0) çapasına çizer. o = bu Oge (o.durum sözlüğü ile eylem durumları okunur).
    derinlik: paralaks katsayısı (0 uzak gök, 0.3 dağ, 0.7 orta plan, 1 ana düzlem, 1.3+ ön plan çerçevesi).
    x,y,s,rot,a: Iz ya da sabit. giris=(tur, t0, sure). cikis=(tur, t0, sure). ikincil=[(tur, guc)].
    eylemler: [(t0, sure, fonksiyon(p) → dönüşüm sözlüğü)] — kelimeye kilitli küçük eylemler (sapla, kaldır, dön).
    """
    def __init__(self, ad, ciz, x=W / 2, y=H / 2, s=1.0, rot=0.0, a=1.0, derinlik=1.0, giris=None, cikis=None, ikincil=(), eylemler=(), blur=0.0):
        self.ad, self.ciz, self.derinlik = ad, ciz, derinlik
        sar = lambda v: v if isinstance(v, Iz) else sabit(v)
        self.x, self.y, self.s, self.rot, self.a, self.blur = map(sar, (x, y, s, rot, a, blur))
        self.giris, self.cikis, self.ikincil, self.eylemler = giris, cikis, list(ikincil), list(eylemler)
        self.durum = {}

    def donusum(self, t):
        d = dict(x=self.x(t), y=self.y(t), s=self.s(t), rot=self.rot(t), a=self.a(t), dx=0, dy=0, sy=1.0, parlama=0.0, kirp=1.0, gorunur=True)
        def birles(m):
            for k, v in m.items():
                if k in ("s", "a", "sy", "kirp"): d[k] *= v
                elif k in ("dx", "dy", "rot", "parlama"): d[k] += v
        if self.giris:
            tur, t0, sure = (self.giris + (0.45,))[:3]
            if t < t0: d["gorunur"] = False
            else: birles(_giris(tur, (t - t0) / sure))
        if self.cikis:
            tur, t0, sure = (self.cikis + (0.4,))[:3]
            if t >= t0:
                g = _giris(tur, 1 - (t - t0) / sure)
                if t - t0 >= sure: d["gorunur"] = False
                birles(g)
        for i, (tur, guc) in enumerate(self.ikincil): birles(ikincil(tur, t, guc, faz=i * 1.7 + len(self.ad)))
        for t0, sure, f in self.eylemler:
            if t >= t0: birles(f(clamp((t - t0) / sure)))
        return d

    def render(self, c, t, kam):
        d = self.donusum(t)
        if not d["gorunur"] or d["a"] <= 0.003 or d["s"] <= 0.001: return
        # paralaks: kamera kayması ve zoom derinlikle ölçeklenir
        z = 1 + (kam["z"] - 1) * self.derinlik
        ox = (kam["x"] - W / 2) * self.derinlik; oy = (kam["y"] - H / 2) * self.derinlik
        c.save()
        c.translate(W / 2, H / 2); c.scale(z, z); c.translate(-W / 2 - ox, -H / 2 - oy)
        c.translate(d["x"] + d["dx"], d["y"] + d["dy"])
        if d["rot"]: c.rotate(d["rot"])
        c.scale(d["s"], d["s"] * d["sy"])
        lay = None
        if d["a"] < 0.999 or self.blur(t) > 0.05:
            lp = skia.Paint(); lp.setAlphaf(clamp(d["a"]))
            if self.blur(t) > 0.05: lp.setImageFilter(skia.ImageFilters.Blur(self.blur(t), self.blur(t)))
            lay = c.saveLayer(None, lp)
        if d["kirp"] < 0.999: c.clipRect(skia.Rect(-4000, -4000, -4000 + 8000 * d["kirp"], 4000))
        self.durum.update(d)
        self.ciz(c, t, self)
        if lay is not None: c.restore()
        c.restore()
        if d["parlama"] > 0.01:   # kelime anında ışık patlaması: öğenin ekrandaki konumunda
            sx, sy = ekran_konumu(self, t, kam)
            g = skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeRadial((sx, sy), 260 * z * d["s"], [hexcol("#FFE6A8", 0.55 * d["parlama"]), hexcol("#FFE6A8", 0)]),
                           BlendMode=skia.BlendMode.kScreen)
            c.drawCircle(sx, sy, 260 * z * d["s"], g)

def ekran_konumu(o, t, kam):
    """Öğenin çapasının ekran koordinatı (geçişler bunu kullanır: 'pencereden geç', 'nesneyi taşı')."""
    d = o.donusum(t); z = 1 + (kam["z"] - 1) * o.derinlik
    ox = (kam["x"] - W / 2) * o.derinlik; oy = (kam["y"] - H / 2) * o.derinlik
    px, py = d["x"] + d["dx"] - ox, d["y"] + d["dy"] - oy
    return W / 2 + (px - W / 2) * z, H / 2 + (py - H / 2) * z


class Kamera:
    """x,y: kameranın baktığı nokta (ana düzlem koordinatı), z: zoom. sarsinti: [(t0, sure, guc)]."""
    def __init__(self, x=W / 2, y=H / 2, z=1.0, sarsinti=()):
        sar = lambda v: v if isinstance(v, Iz) else sabit(v)
        self.x, self.y, self.z = sar(x), sar(y), sar(z); self.sarsinti = list(sarsinti)
    def __call__(self, t):
        x, y = self.x(t), self.y(t)
        for t0, sure, guc in self.sarsinti:
            if t0 <= t < t0 + sure:
                k = guc * (1 - (t - t0) / sure); x += k * math.sin(71 * t); y += k * math.cos(59 * t)
        return dict(x=x, y=y, z=self.z(t))


class Cekim:
    """Bir çekim = bir sahne grafiği. kelimeler: [(kelime, başlangıç, bitiş)] (çekim başına göre, ASR'den)."""
    def __init__(self, ad, sure, kelimeler=(), duygu=None, arka="#000000"):
        self.ad, self.sure, self.kelimeler, self.duygu, self.arka = ad, sure, list(kelimeler), duygu, arka
        self.ogeler, self.kamera, self.ust = [], Kamera(), []   # ust: kamera dışı katman (altyazı, isim kartı, vinyet)

    def ekle(self, *ogeler):
        for o in ogeler: self.ogeler.append(o)
        self.ogeler.sort(key=lambda o: o.derinlik); return self
    def oge(self, ad): return next(o for o in self.ogeler if o.ad == ad)

    def k(self, kelime, ofset=0.0, kacinci=1):
        """Kelime kilidi: kelimenin (kısmi eşleşme, küçük harf) başlangıç zamanı + ofset. Bulamazsa hata verir — sessiz kayma yok."""
        kelime = kelime.lower(); n = 0
        for w, a, b in self.kelimeler:
            if kelime in w.lower().strip(".,!?;:\"'"):
                n += 1
                if n == kacinci: return a + ofset
        raise KeyError(f"{self.ad}: '{kelime}' kelimesi zaman listesinde yok")

    def render(self, c, t):
        c.clear(hexcol(self.arka)); kam = self.kamera(t)
        lay = None
        if self.duygu:
            p = skia.Paint(); p.setColorFilter(self.duygu.filtre(t)); lay = c.saveLayer(None, p)
        for o in self.ogeler: o.render(c, t, kam)
        if lay is not None: c.restore()
        if self.duygu: self.duygu.uygula(c, t)
        for f in self.ust: f(c, t)
