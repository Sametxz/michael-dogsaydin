# Brief: Bölüm I anlatı kareleri v3 (f1–f10): katı kalite denetimi

## Bağlam
2D animasyon video: "Ragnar Lothbrok Olarak Doğsaydın?" (Born in Lore formatı, Vikings dizisi S1). Kullanıcı f1–f10 karelerini "aşırı kötü, kesinlikle kabul edilemez" buldu. Örnek olarak f3 ve f8'i gösterdi:
- f3: Düz renkli kutu kulübeler, boş gri gökyüzü, çubuk bacaklı keçi, ölü kompozisyon.
- f8: Düz tuğla duvar, plastik görünümlü sunak, birkaç basit şekil.
Bu kareler videoda bir cümle boyunca (3–5 sn) ekranda kalıyor; ana sahneler kadar zengin olmalı.

## Çıta (referans kareler, mutlaka bak)
- `/home/claude/r3/kurul/test_ivar/hero_v4.png`: temiz, gölgeli, sinematik 2D (kahraman kare).
- `/home/claude/r3/bedel/d3.png`: süslü cenaze yığını, meşaleli köylüler, gece ışığı.
- `/home/claude/r3/bati/e4.png`: fırtınada uzun gemi.
- `/home/claude/r3/bati/e7.png`: holmgang kalkan çemberi.
- `/home/claude/r3/kesis/a1.png`, `b1.png`, `b2.png`.
- Standart: `/home/claude/r3/kurul/GORSEL_STANDART.md` (R8–R13). Dersler: `/home/claude/r3/kurul/DERSLER.md`.

## Zorunlu kalite kuralları
1. **Derinlik katmanları:** en az 4 katman olmalı: uzak arka plan, orta plan, sahne, ön plan. Ön plan objesi ya da bulanık bir öğe kadrajı çerçeveler. Atmosfer (sis, duman, toz, kar, yağmur) katmanlar arasına girer.
2. **Düz renk alan yok:** Her büyük yüzeyde doku olmalı. Tex filtreleri, ahşap damarı, taş derzi, saman lifi, çamur ve kar lekeleri kullanılabilir. Gökyüzü gradyan ve bulut katmanlarıyla çizilir. Mevcut doku yardımcıları: `tex.py`, `obj7.ground2`, `obj7.thatch_house`, `places7.greathall`, `ivar2/places.py` (longhouse, riverbank).
3. **Işık:** Belirgin bir ışık kaynağı ve yönü olmalı. Her ana nesnede gölge tarafı ve rim ışığı bulunur, yere temas gölgesi düşer (R9). Sıcak/soğuk ayrımı net olur.
4. **Zenginlik ama dağınıklık yok:** Her karede hikâyeyi anlatan 6 ile 12 arası anlamlı ayrıntı olur. Örnek, doğudaki fakir köy için: çökük ve yamalı saz çatılar, duman, sıska ama gerçekçi keçi, kuru çit, çamurda ayak izleri, boş tahıl çuvalı, cılız tavuk, eğik çit kazığı, donuk ışık.
5. **Karakterler yalnızca art3 model gövdeleriyle** (R11): `full()`, `fig_bust()`; gövde uydurmak yok, silüet yok (R12). Ragnar'ın kimliği (kuzgun broş, yara, örgüler) korunur. Asimetrik karakter aynalanmaz; gerekiyorsa kompozisyon değiştirilir.
6. **Hayvanlar ve nesneler çizgi film gibi olmamalı (R10, R13):** çubuk bacak, yuvarlak boş göz, kutu şekil yasak. Anatomi doğru olmalı, kalın ve ince çizgi ayrımı, gölge ve doku olmalı.
7. **Kartlar:** `card_at()` isim/bilgi kartı kalır ama kompozisyonun içine yerleşir; önemli bir şeyin üstüne binmez.
8. **R13 yakın kontrol:** Her karede en önemli 2 nesnenin 1920 px üzerinden %200 büyütülmüş kırpması alınır (`bati/v3/<id>_crop1.png`, `crop2.png`) ve göz kontrolünden geçer. Kırpmada vasat görünen bir şey varsa düzeltilir.
9. **Öz değerlendirme döngüsü:** Kare render edilir ve Read ile bakılır. Bu kural listesine göre 1–5 puanlanır. 4'ün altındaki her madde düzeltilir. En az 2 tur yapılır, en fazla 4. Vasat bir kare teslim edilmez.

## Teknik
- Kod `/home/claude/r3/bati/kareler6.py` içinde (f1–f10). Yardımcılar `kareler5.py` → `kareler4.py` → `kareler3.py` zincirinden gelir: `full`, `fig_bust`, `svg_sprite`, `place`, `blurred`, `draw`, `rim`, `shade_side`, `glow`, `bloom_spot`, `rays`, `snowfall`, `finish`, `live`, `ex`, `IF.blink_at`, `card_at`, `army`, `KL.soldier_spec`, `O7.*`, `P7.*`, `IPL.longhouse`, `G.*` (`gemi.py`). Karakter spec'leri: `RG` (Ragnar), `FLOv`, `HARALD`, `ATHv`, `LAGv`, `BJv`, `ROLLO`, `monk()`.
- **Kendi modülünde çalış:** `/home/claude/r3/bati/v3_<harf>.py` (`from kareler6 import *`). Fonksiyonları aynı adla yeniden tanımla (ör. `def f3(): ...`) ve dosyanın sonunda kendi `FR` sözlüğünü kur. Render: `python3 v3_<harf>.py` → `/home/claude/r3/bati/v3/<id>.png`. Statik kare için `T[0] = None`. `kareler5.py` ve `kareler6.py` dosyalarını DEĞİŞTİRME; ortak dosyalara yazma, böylece öteki ajanlarla çakışmazsın.
- Sprite önbelleği SVG içeriğine göre anahtarlanır; yeni SVG otomatik yeniden render edilir. Bir kare render'ı birkaç saniyeden bir dakikaya kadar sürer.
- Karede aynı anda en fazla 1920×1080 çizilir; letterbox `finish()` içinde.
- Video, ses, TTS ve git YOK. Yalnızca ham kare üretilir.

## Teslim
Kısa bir rapor (Türkçe, en fazla 200 kelime) yaz. Raporda her kare için yapılanlar ve son öz değerlendirme puanı yer alır. Ayrıca kullanıcının yine beğenmeyebileceği riskli noktalar dürüstçe belirtilir. Dosyalar: `bati/v3/<id>.png` ve kırpmalar.
