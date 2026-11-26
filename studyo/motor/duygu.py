"""Duygu → görsel dil. Her çekimin bir duygusu vardır; bu modül onu renk, ışık, doku ve kamera davranışına çevirir.

Duygu(ad) hazır kalıplardan biriyle kurulur, sonra istenirse alanlar değiştirilir:
    ck.duygu = Duygu("yas")                    # soğuk, doygunluğu düşük, ağır vinyet, yavaş kamera
    ck.duygu = Duygu("huzur").gecis("yas", t0=2.0, sure=1.5)   # çekim içinde duygu dönüşümü (mutluluk → kayıp)

Alanlar:
  doygunluk  0..1.4   sicaklik −1 (mavi) .. +1 (amber)   parlaklik 0.6..1.2   kontrast 0.8..1.3
  vinyet 0..1         ust_renk / alt_renk: dikey ışık degradesi (gökten/yerden gelen renk)
  kamera: önerilen kamera davranışı (belgeleme ve kurul kontrolü için; Kamera'yı otomatik değiştirmez)
  parcacik: önerilen atmosfer (kül, kar, toz, yağmur, ateş böceği)
"""
import math
import skia
from sahne import W, H, hexcol, clamp, ease

KALIP = {
    #  ad          doyg  sıcak  parlak kontr vinyet  üst renk (a)          alt renk (a)          kamera                          parçacık
    "huzur":    (1.05,  0.45, 1.04, 0.95, 0.25, ("#FFD9A0", 0.16), ("#5A3A1A", 0.10), "yavaş kayma, geniş plan, sabit ufuk", "toz zerreleri, polen"),
    "mutluluk": (1.18,  0.55, 1.08, 1.00, 0.18, ("#FFE2A8", 0.20), ("#7A4A20", 0.08), "hafif yukarı kalkış, yumuşak takip", "ışık zerreleri"),
    "merak":    (1.00,  0.10, 1.00, 1.05, 0.35, ("#BFD8FF", 0.10), ("#202838", 0.15), "yavaş itme (push-in) odağa", "toz, sis tülü"),
    "gerilim":  (0.80, -0.25, 0.92, 1.18, 0.55, ("#9FB4C8", 0.10), ("#0A0E14", 0.35), "çok yavaş itme, hafif el titremesi, alçak açı", "sis, uçuşan kül"),
    "korku":    (0.62, -0.45, 0.82, 1.25, 0.70, ("#6E88A8", 0.12), ("#000000", 0.45), "ani zoom, eğik kadraj, sarsıntı", "yağmur, şimşek"),
    "ofke":     (1.15,  0.35, 0.95, 1.28, 0.55, ("#FF7A3A", 0.18), ("#2A0800", 0.35), "sert kesme, yakın plan, sarsıntı", "kıvılcım, duman"),
    "zafer":    (1.20,  0.40, 1.10, 1.15, 0.30, ("#FFD070", 0.24), ("#3A2208", 0.12), "alt açı, geri çekilip büyüme", "kıvılcım, bayrak dalgası"),
    "yas":      (0.48, -0.40, 0.86, 0.92, 0.65, ("#AFC0D0", 0.12), ("#0C1218", 0.40), "durağan ya da çok yavaş geri çekilme, boşluk bırakan kadraj", "yağmur ya da kar, düşen yaprak"),
    "yalnizlik":(0.55, -0.30, 0.90, 0.95, 0.60, ("#C8D2DC", 0.10), ("#101418", 0.30), "geniş planda küçük figür, uzaklaşan kamera", "kar, sis"),
    "umut":     (0.95,  0.30, 1.02, 1.00, 0.35, ("#FFE8B8", 0.22), ("#182030", 0.20), "karanlıktan ışığa kayma, yukarı tilt", "ışık hüzmesi, toz"),
    "yorgunluk":(0.60,  0.05, 0.88, 0.90, 0.55, ("#D8C8A8", 0.10), ("#181410", 0.35), "ağır, gecikmeli takip; yarım saniye geç kalan kamera", "toz, duman"),
}

class Duygu:
    def __init__(self, ad="huzur"):
        self.ad = ad
        (self.doygunluk, self.sicaklik, self.parlaklik, self.kontrast, self.vinyet, self.ust, self.alt, self.kamera, self.parcacik) = KALIP[ad]
        self._hedef = None

    def gecis(self, hedef, t0, sure=1.2):
        """Çekim içinde duygu dönüşümü: t0'dan itibaren 'sure' saniyede hedef duyguya kayar."""
        self._hedef = (Duygu(hedef), t0, sure); return self

    def _degerler(self, t):
        v = dict(d=self.doygunluk, s=self.sicaklik, p=self.parlaklik, k=self.kontrast, vin=self.vinyet, ust=self.ust, alt=self.alt)
        if self._hedef:
            h, t0, sure = self._hedef; q = ease("io", (t - t0) / sure)
            if q > 0:
                for a, b in (("d", "doygunluk"), ("s", "sicaklik"), ("p", "parlaklik"), ("k", "kontrast"), ("vin", "vinyet")):
                    v[a] = v[a] + (getattr(h, b) - v[a]) * q
                v["ust"] = (h.ust[0], v["ust"][1] * (1 - q) + h.ust[1] * q) if q > 0.5 else (v["ust"][0], v["ust"][1] * (1 - q))
                v["alt"] = (h.alt[0], v["alt"][1] * (1 - q) + h.alt[1] * q) if q > 0.5 else (v["alt"][0], v["alt"][1] * (1 - q))
        return v

    def filtre(self, t):
        """Renk matrisi: doygunluk + sıcaklık + parlaklık + kontrast (sahnenin tamamına uygulanır)."""
        v = self._degerler(t); s, k, p, sc = v["d"], v["k"], v["p"], v["s"]
        lr, lg, lb = 0.2126, 0.7152, 0.0722
        sat = [lr * (1 - s) + s, lg * (1 - s), lb * (1 - s),
               lr * (1 - s), lg * (1 - s) + s, lb * (1 - s),
               lr * (1 - s), lg * (1 - s), lb * (1 - s) + s]
        r_, b_ = 1 + 0.10 * sc, 1 - 0.12 * sc
        off = 0.5 * (1 - k)
        m = []
        for row, mul in zip(range(3), (r_, 1.0, b_)):
            m += [sat[row * 3] * k * p * mul, sat[row * 3 + 1] * k * p * mul, sat[row * 3 + 2] * k * p * mul, 0, off]
        m += [0, 0, 0, 1, 0]
        return skia.ColorFilters.Matrix(m)

    def uygula(self, c, t):
        """Kamera dışı ışık katmanları: üst/alt degrade + vinyet (filtreden sonra çizilir)."""
        v = self._degerler(t)
        (uc, ua), (ac, aa) = v["ust"], v["alt"]
        g = skia.Paint(Shader=skia.GradientShader.MakeLinear([(0, 0), (0, H)], [hexcol(uc, ua), hexcol(uc, 0), hexcol(ac, 0), hexcol(ac, aa)], [0, 0.45, 0.6, 1]))
        c.drawRect(skia.Rect(0, 0, W, H), g)
        vin = skia.Paint(Shader=skia.GradientShader.MakeRadial((W / 2, H / 2), W * 0.62, [hexcol("#000000", 0), hexcol("#000000", 0), hexcol("#000000", clamp(v["vin"]))], [0, 0.55, 1]))
        c.drawRect(skia.Rect(0, 0, W, H), vin)
