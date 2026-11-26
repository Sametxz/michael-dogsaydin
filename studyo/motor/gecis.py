"""Anlamsal geçişler + Film (çekimleri birleştirip mp4 yazar).

Kural: çekimler arası geçiş, iki çekimi ANLAMCA bağlar. Siyaha kararma yalnızca bölüm sonunda kullanılır.
Bir geçiş, A çekiminin son `sure` saniyesi ile B çekiminin ilk `sure` saniyesinin üst üste bindiği aralıkta çizilir.

Katalog (ayrıntı ve hangi durumda hangisi: docs/02_DINAMIK_ANLATIM.md §3):
  Kes()                         sert kesme (ritim, şok, ses vuruşu ile)
  Maske("pencere", boyut=(w,h)) A'daki öğenin içinden B'ye girilir (pencere, kapı, göz, ayna, kalkan, ateşin ağzı)
  ZoomIcinden("gozler")         A'da bir noktaya dalıp B'nin içinden çıkılır (anı, rüya, iç ses)
  NesneTasi("halka","halka",ciz)Nesne A'dan B'ye uçar/taşınır; zemin değişir, nesne sürer (kimlik nesnesi, mektup, sikke)
  Eslesme("ay","kalkan")        Biçim eşleşmesi: A'daki biçim B'deki benzer biçime oturur (ay → kalkan, göz → güneş)
  OnPlanSil(ciz_perde)          Ön planda geçen bir şey (direk, yelken, kalabalık) ekranı siler, arkasında sahne değişir
  Savurma(yon=1)                Hızlı kamera savurması + hareket bulanıklığı (eylem, kovalama, zaman atlaması)
  Karart(renk)                  yalnızca bölüm sonu / büyük zaman atlaması
"""
import math, os, subprocess
import skia
from sahne import W, H, FPS, SAMP, ease, clamp, hexcol, ekran_konumu


def _img(cekim, t, surf):
    c = surf.getCanvas(); cekim.render(c, t); return surf.makeImageSnapshot()

def _ciz_olcekli(c, img, merkez, s, a=1.0, blur=0.0):
    p = skia.Paint(); p.setAlphaf(clamp(a))
    if blur > 0.3: p.setImageFilter(skia.ImageFilters.Blur(blur, blur))
    c.save(); c.translate(*merkez); c.scale(s, s); c.translate(-merkez[0], -merkez[1]); c.drawImage(img, 0, 0, SAMP, p); c.restore()

def _konum(cekim, ad, t):
    o = cekim.oge(ad); kam = cekim.kamera(t); z = 1 + (kam["z"] - 1) * o.derinlik
    return ekran_konumu(o, t, kam), z * o.donusum(t)["s"]


class Gecis:
    sure = 0.0
    def ciz(self, c, A, B, ia, ib, ta, tb, u): raise NotImplementedError

class Kes(Gecis):
    sure = 0.0

class Karart(Gecis):
    def __init__(self, sure=0.8, renk="#000000"): self.sure, self.renk = sure, renk
    def ciz(self, c, A, B, ia, ib, ta, tb, u):
        c.drawImage(ia if u < 0.5 else ib, 0, 0)
        p = skia.Paint(Color4f=hexcol(self.renk, 1 - abs(u - 0.5) * 2)); c.drawRect(skia.Rect(0, 0, W, H), p)

class Maske(Gecis):
    """A'daki öğenin (pencere/kapı/göz) biçimi büyüyerek ekranı kaplar; içinde B görünür. A aynı anda o noktaya dalar."""
    def __init__(self, oge, boyut=(160, 200), sekil="dikdortgen", sure=1.1, yaricap=10):
        self.oge, self.boyut, self.sekil, self.sure, self.r = oge, boyut, sekil, sure, yaricap
    def ciz(self, c, A, B, ia, ib, ta, tb, u):
        (px, py), sc = _konum(A, self.oge, ta); q = ease("in", u) if u < 0.6 else ease("io", u)
        dal = 1 + 5.0 * ease("in", u)                                   # A pencereye dalar
        _ciz_olcekli(c, ia, (px, py), dal, blur=6 * u)
        w0, h0 = self.boyut[0] * sc * dal, self.boyut[1] * sc * dal
        k = max(W / w0, H / h0) * 1.25
        w, h = w0 * (1 + (k - 1) * q) if k > 1 else w0, h0 * (1 + (k - 1) * q) if k > 1 else h0
        cx, cy = px + (W / 2 - px) * q, py + (H / 2 - py) * q
        path = skia.Path()
        if self.sekil == "daire": path.addCircle(cx, cy, max(w, h) / 2)
        else: path.addRRect(skia.RRect.MakeRectXY(skia.Rect(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), self.r, self.r))
        c.save(); c.clipPath(path, doAntiAlias=True)
        _ciz_olcekli(c, ib, (W / 2, H / 2), 1.35 - 0.35 * ease("out", u))   # B içeriden yerine oturur
        c.restore()
        ic = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=10 * (1 - u), Color4f=hexcol("#FFE0A0", 0.6 * (1 - u)))
        c.drawPath(path, ic)                                              # çerçevenin ışığı geçişte söner

class ZoomIcinden(Gecis):
    """A'nın bir noktasına (öğe ya da (x,y)) hızla dalınır; beyaz/renkli bir nefesle B açılır ve geri yerine oturur."""
    def __init__(self, hedef, sure=0.9, renk="#FFF4DC"): self.hedef, self.sure, self.renk = hedef, sure, renk
    def ciz(self, c, A, B, ia, ib, ta, tb, u):
        p = self.hedef if isinstance(self.hedef, tuple) else _konum(A, self.hedef, ta)[0]
        if u < 0.5:
            _ciz_olcekli(c, ia, p, 1 + 9 * ease("in", u * 2), blur=18 * u)
        else:
            _ciz_olcekli(c, ib, (W / 2, H / 2), 1.6 - 0.6 * ease("out", (u - 0.5) * 2), blur=14 * (1 - u))
        f = skia.Paint(Color4f=hexcol(self.renk, max(0, 1 - abs(u - 0.5) * 4) * 0.9)); c.drawRect(skia.Rect(0, 0, W, H), f)

class NesneTasi(Gecis):
    """Nesne A'daki yerinden B'deki yerine kavisle uçar; altta A kayarak çıkar, B kayarak gelir.
    ciz_nesne(c, ilerleme) nesneyi (0,0) çapasına çizer. A ve B'deki öğeler geçiş boyunca gizlenir (çift nesne olmaz: R6)."""
    def __init__(self, oge_a, oge_b, ciz_nesne, sure=1.2, kavis=-260):
        self.oa, self.ob, self.cn, self.sure, self.kavis = oge_a, oge_b, ciz_nesne, sure, kavis
    def ciz(self, c, A, B, ia, ib, ta, tb, u):
        (ax, ay), sa = _konum(A, self.oa, ta); (bx, by), sb = _konum(B, self.ob, tb + self.sure * (1 - u))
        q = ease("io", u); yon = 1 if bx >= ax else -1
        _ciz_olcekli(c, ia, (W / 2 - yon * W * 0.35 * q, H / 2), 1.0, a=1 - q)
        c.save(); c.translate(yon * W * 0.25 * (1 - q), 0); _ciz_olcekli(c, ib, (W / 2, H / 2), 1.0, a=q); c.restore()
        x = ax + (bx - ax) * q; y = ay + (by - ay) * q + self.kavis * math.sin(math.pi * q); s = sa + (sb - sa) * q
        c.save(); c.translate(x, y); c.rotate(yon * 360 * q * 0.15); c.scale(s, s); self.cn(c, u); c.restore()
    def gizle(self): return (self.oa, self.ob)

class Eslesme(Gecis):
    """Biçim eşleşmesi: A'daki öğe B'deki öğenin konum ve ölçeğine kayar, bu sırada A → B çözülür."""
    def __init__(self, oge_a, oge_b, sure=0.9): self.oa, self.ob, self.sure = oge_a, oge_b, sure
    def ciz(self, c, A, B, ia, ib, ta, tb, u):
        (ax, ay), sa = _konum(A, self.oa, ta); (bx, by), sb = _konum(B, self.ob, tb); q = ease("io", u)
        k = 1 + (sb / max(sa, 1e-6) - 1) * q
        c.save(); c.translate((bx - ax) * q, (by - ay) * q); _ciz_olcekli(c, ia, (ax, ay), k, a=1 - q); c.restore()
        k2 = (sa / max(sb, 1e-6)) + (1 - sa / max(sb, 1e-6)) * q
        c.save(); c.translate((ax - bx) * (1 - q), (ay - by) * (1 - q)); _ciz_olcekli(c, ib, (bx, by), k2, a=q); c.restore()

class OnPlanSil(Gecis):
    """Ön planda bir şey (direk, yelken, kalabalık, duman) ekranı soldan sağa geçer; geçtiği yerin arkasında B vardır.
    ciz_perde(c, u) → perdeyi çizer ve sınırın x'ini döndürür (sınırın solunda B, sağında A)."""
    def __init__(self, ciz_perde, sure=0.8): self.cp, self.sure = ciz_perde, sure
    def ciz(self, c, A, B, ia, ib, ta, tb, u):
        x = -300 + (W + 600) * ease("io", u)
        c.drawImage(ia, 0, 0)
        c.save(); c.clipRect(skia.Rect(0, 0, clamp(x, 0, W), H)); c.drawImage(ib, 0, 0); c.restore()
        c.save(); c.translate(x, 0); self.cp(c, u); c.restore()

class Savurma(Gecis):
    def __init__(self, yon=1, sure=0.45): self.yon, self.sure = yon, sure
    def ciz(self, c, A, B, ia, ib, ta, tb, u):
        q = ease("io", u); dx = -self.yon * W * q; n = 7
        for i in range(n):   # hareket bulanıklığı: kaydırılmış kopyalar
            o = (i - n / 2) * 30 * math.sin(math.pi * u)
            p = skia.Paint(); p.setAlphaf(1 / n * 1.6)
            c.drawImage(ia, dx + o, 0, SAMP, p); c.drawImage(ib, dx + self.yon * W + o, 0, SAMP, p)


# ───────── Film
class Writer:
    def __init__(self, path, crf=18):
        self.p = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                                   "-c:v", "libx264", "-preset", "veryfast", "-crf", str(crf), "-pix_fmt", "yuv420p", path], stdin=subprocess.PIPE)
        self.info = skia.ImageInfo.Make(W, H, skia.kRGBA_8888_ColorType, skia.kPremul_AlphaType); self.buf = bytearray(W * H * 4)
    def write(self, surf): surf.readPixels(self.info, self.buf, W * 4); self.p.stdin.write(self.buf)
    def close(self):
        self.p.stdin.close()
        if self.p.wait() != 0: raise RuntimeError("ffmpeg hata verdi")


class Film:
    """Film([ck1, Maske("pencere"), ck2, NesneTasi(...), ck3]) — çekim ve geçişler sırayla."""
    def __init__(self, dizi):
        self.cekimler, self.gecisler = [], []          # gecisler[i] = i. çekimden sonraki geçiş
        for x in dizi:
            if isinstance(x, Gecis): self.gecisler[-1] = x
            else: self.cekimler.append(x); self.gecisler.append(Kes())
        self.gecisler[-1] = Kes()
        for i, ck in enumerate(self.cekimler):
            giren = self.gecisler[i - 1].sure if i else 0.0
            if ck.sure < giren + self.gecisler[i].sure + 0.3:
                raise ValueError(f"{ck.ad}: süre ({ck.sure}) giriş+çıkış geçişlerine yetmiyor")
        self.bas = [0.0]
        for ck, g in zip(self.cekimler, self.gecisler): self.bas.append(self.bas[-1] + ck.sure - g.sure)
        self.sure = self.bas[-1]

    def zaman_cizelgesi(self):
        """Ses miksi için: [(çekim adı, film başlangıcı, süre)] — anlatım satırları çekim içi zamana göre buraya oturur."""
        return [(ck.ad, b, ck.sure) for ck, b in zip(self.cekimler, self.bas)]

    def kare(self, c, t, sa, sb):
        """Film zamanı t'deki kareyi c'ye çizer."""
        for i, ck in enumerate(self.cekimler):
            t0 = self.bas[i]; g = self.gecisler[i]; son = t0 + ck.sure
            if t < t0 or t >= son: continue
            if g.sure > 0 and i + 1 < len(self.cekimler) and t >= son - g.sure:
                B = self.cekimler[i + 1]; ta, tb = t - t0, t - self.bas[i + 1]; u = (t - (son - g.sure)) / g.sure
                gizli = g.gizle() if hasattr(g, "gizle") else ()
                kayit = []
                for ad, C in zip(gizli, (ck, B)):
                    o = C.oge(ad); kayit.append((o, o.a)); o.a = lambda t, _a=o.a: 0.0
                ia, ib = _img(ck, ta, sa), _img(B, tb, sb)
                for o, a in kayit: o.a = a
                c.clear(skia.ColorBLACK); g.ciz(c, ck, B, ia, ib, ta, tb, u); return
            if i > 0 and t < t0 + self.gecisler[i - 1].sure: continue   # önceki geçiş çiziyor
            ck.render(c, t - t0); return

    def render(self, yol, crf=18):
        surf = skia.Surface(W, H); sa, sb = skia.Surface(W, H), skia.Surface(W, H); c = surf.getCanvas()
        tmp = yol[:-4] + "_tmp.mp4"; wr = Writer(tmp, crf)
        for f in range(int(round(self.sure * FPS))):
            t = f / FPS
            # geçiş aralığı önceki çekimin döngüsünde yakalanır; değilse sıradaki çekim çizer
            self.kare(c, t, sa, sb); wr.write(surf)
        wr.close(); os.replace(tmp, yol); return yol

    def onizle(self, zamanlar, klasor, olcek=0.5):
        """Seçili anların PNG'si (kontakt/kurul için). olcek=0.5 → 960 px."""
        os.makedirs(klasor, exist_ok=True); surf = skia.Surface(W, H); sa, sb = skia.Surface(W, H), skia.Surface(W, H); out = []
        for t in zamanlar:
            self.kare(surf.getCanvas(), t, sa, sb); img = surf.makeImageSnapshot()
            if olcek != 1: img = img.resize(int(W * olcek), int(H * olcek))
            p = f"{klasor}/t{t:06.2f}.png"; img.save(p); out.append(p)
        return out
