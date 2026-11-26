---
name: dinamik-sahne
description: "Anlatımlı 2D animasyonda bir bölümü cümle=eylem ilkesiyle sahne dökümüne çevirir ve studyo/motor ile render eder: kelimeye kilitli girişler, paralaks katmanları, anlamsal geçişler (pencere, nesne taşıma, biçim eşleşmesi), duygu grade'i ve D1–D10 denetimi."
---

# Dinamik sahne: cümleden hareketli çekime

Bir anlatım bölümünü, söylenen her şeyin ekranda yaşandığı ve çekimlerin birbirine anlamca aktığı bir animasyona çevirir. Motor ve belgeler `Sametxz/michael-dogsaydin` (önceki: `Sametxz/ragnar-dogsaydin`) reposunun `studyo/` klasöründedir.

## Ne zaman kullanılır
- Bir bölümün anlatım metni hazırsa ve sahne dökümü, blok animatik ya da tam render yapılacaksa.
- Kullanıcı "statik kaldı", "anlatıldı ama yaşanmadı", "geçişler kopuk" dediğinde.

## Adımlar
1. **Cümlelere böl.** Her cümle ≤ 12 kelime olmalı. Çekim başına en çok 2 cümle.
2. **Her cümleye dört cevap yaz:** ne görünür (somut), hangi kelimede, nasıl girer ya da ne yapar, sonrakine neyle akar. Dökümü `dokum/bolum_X.json` olarak yaz (şema: `studyo/sablonlar/sahne_dokumu.schema.md`).
3. **Duyguyu yerleştir:** çekim başına `duygu` + `duygu_tasiyici`. Dönüşüm varsa kelimesini yaz (`studyo/docs/03_DUYGU_DILI.md`).
4. **Geçişleri seç** (`studyo/docs/02_DINAMIK_ANLATIM.md §3`). Anlamsal oran ≥ %60 olmalı, kararma yalnız bölüm sonunda. Her geçişin bağ cümlesini yaz.
5. **Denetle:** `cd studyo/motor && python3 dokum_kontrol.py <döküm>`. Bütün ✗ hataları düzelt.
6. **Örgü tablosu** (`sablonlar/orgu_sunum_sablonu.md`) kullanıcıya gider. Onay gelmeden çizim yapılmaz.
7. **Blok animatik:** kaba şekillerle `Cekim`/`Oge` kur, gerçek ya da tahmini zamanlarla `Film.render()` (960 px'e küçült). Kullanıcıya gönder.
8. **Son kalite:** Öğeleri gerçek çizimlerle değiştir (yapı aynı kalır). Anahtar kareler + geçiş orta kareleri → öz değerlendirme → kurul → kullanıcı.
9. **Ses ve kilit:** TTS → `kelime.zamanlar(wav, bas)` → `Cekim(kelimeler=…)`. `ck.k("kelime")` bulunamazsa hata verir; sessiz kayma olmaz.
10. **Tam render ve denetim:** Sessiz izlemede ölü süre olmamalı. Sesli izlemede her cümle görünmeli (≤ 0,3 sn gecikme). Geçiş orta karelerine bakılır.

## Motor hızlı başvuru
```python
from sahne import *; from duygu import Duygu; from gecis import *
ck = Cekim("2.04", 4.5, kelimeler=kw, duygu=Duygu("huzur").gecis("yas", t0=2.0, sure=1.5))
ck.ekle(Oge("gok", ciz_gok, derinlik=0.05),
        Oge("pencere", ciz_pencere, x=1080, y=770, giris=("parla", ck.k("pencere", -0.1), 0.7), ikincil=[("alev", .4)]),
        Oge("dal", ciz_dal, derinlik=1.4, blur=4, ikincil=[("salin", 1)]))
ck.kamera = Kamera(x=Iz([(0, 900), (4.5, 1070, "io")]), z=Iz([(0, 1.0), (4.5, 1.2, "in")]), sarsinti=[(ck.k("savaş"), .6, 14)])
Film([ck, Maske("pencere", boyut=(160, 160)), ck2, NesneTasi("halka", "halka", ciz_halka), ck3]).render("out/bolum.mp4")
```
- Giriş türleri: `pop dus kay_sol kay_sag yuksel belir parla ciz buyu`.
- İkincil hareketler: `nefes salin titre suz alev`.
- Eylem: `eylemler=[(t0, sure, lambda p: dict(rot=-6*p, dy=-20*p))]`.
- Çalışan örnek: `studyo/motor/ornek/demo.py`.

## Tuzaklar
- `ciz` içinde saydamlığı yeniden uygulama: `Oge` katmanı zaten uyguluyor.
- Tam ekran efekt öğesi (flaş, sis) arkada kalmasın diye yüksek derinlik verilir (≥ 1,3).
- Çekim süresi, giriş ve çıkış geçişlerinin toplamından en az 0,3 sn uzun olmalıdır (`Film` kontrol eder).
- Zamanla değişen SVG her karede yeni PNG üretir. Hareket transform ile, değişen ayrıntı skia ile çizilir.
- `NesneTasi` sırasında kaynak ve hedef öğe gizlenir (R6). Başka bir kopya kalmadığını kontrol et.
