# Alt ajanlar

Kullanıcı iki değerlendirme ajanı istedi. Yeni bir oturumda bunları `Agent` aracıyla (subagent_type: general-purpose) aşağıdaki brieflerle yeniden oluştur. İlk oturumdaki kimlikler `a8fb2c1962174d24a` (hikâye) ve `a2140efd2aaa87f47` (görsel) idi. O kimlikler yeni oturumda geçerli değildir.

Ajanlar **üretmez, değerlendirir**. Ana ajan üretir, ajana dosya yollarını verir ve kısa, maddeli bir rapor ister. Raporun özü kullanıcıya iletilir. Ajanların önerdiği kararlar AskUserQuestion ile kullanıcıya sorulur.

---

## 1. Hikâye örgüsü değerlendiricisi

**Brief (oluştururken prompt olarak ver):**

> Sen "Ragnar Lothbrok olarak doğsaydın?" videosunun hikâye örgüsü değerlendiricisisin. Video Born in Lore formatında, ikinci tekil şahısla anlatılıyor ve 8–9 dakika sürüyor. Hikâye, efsaneyi değil **Vikings dizisindeki** akışı (S1–S4) izler. Başta ~20 saniyelik bir efsane prologu var.
> Kaynaklar: `/home/claude/r3/hikaye_taslak_v2.md`, `/home/claude/r3/karar_gunlugu.md`.
> Görevlerin:
> (1) Olayları diziye göre WebSearch ile doğrula. Sezon ve bölüm ver. Emin olmadığını ⚠️ ile işaretle.
> (2) Sahne dökümü hazırla. Her çekim için görsel, duygu, kamera ve **kelimeye kilitli eylem** belirt.
> (3) Anlatım metnini yaz. Türkçe, kısa cümleler, TTS'nin rahat okuyacağı kelimeler. Uzun özel isimlerden kaçın.
> (4) Ekim-biçim bağlantılarını takip et: kol halkası #1–#4, Athelstan'ın haçı, kuzgunlar, yol ayrımı yankısı.
> (5) Kullanıcıya sorulacak 1–2 kararı seçenekleriyle ver.
> Mizah kuralı: espri yalnızca P1, I. bölüm, 10 ve 16'da olur. Trajik vuruşlarda espri yoktur.

**Şu ana kadar verdiği önemli düzeltmeler:**
- Ivar'ı ormana Ragnar kendisi götürür.
- Haç Alfred'e verilir.
- Ölümde şelale görüntüsü yoktur.
- Ivar'a Ecbert'ten intikam alması söylenir.
- Kol halkası #3, oğulların reddidir.
- Ölümdeki kuzgunlar sanatsal bir eklemedir.
- Lagertha vedası (S2E1): Bjorn önce babasını seçer, sonra arabanın peşinden koşar. Ragnar oğlunun başını öper.

## 2. Görsel öğeler değerlendiricisi

**Brief:**

> Sen aynı videonun görsel değerlendiricisisin. Stil hibrit: sıcak konturlu 2D temel; dram sahnelerinde soğuk A tonu ve sinemaskop bandı; 3–4 doruk anında C siluet. Karakterler kodla çiziliyor (SVG → skia). Kullanıcı görsellerin yalnızca nesnelerle değil **efekt ve animasyonla** desteklenmesini, duyguların sahnede etkili işlenmesini istiyor.
> Sana verilen kareleri ve videoyu incele. Gerekirse `ffmpeg -ss` ile ek kare çıkar.
> Kısa ve maddeli rapor ver:
> (a) her çekimde duyguyu taşıyan ve taşımayan öğeler;
> (b) efekt ve animasyon eksikleri;
> (c) öncelik sırasıyla en kritik 5 düzeltme;
> (d) kullanıcıya sorulacak 2 tasarım kararı, seçenekleriyle.
> Oyuncu benzerliği ya da dizi tasarımı kopyası önermezsin.

**Şu ana kadar verdiği önemli düzeltmeler (yas sahnesi):**
- Siluet yeni modelle çizildi ve huzme figüre indirildi.
- Yas ifadesinde ince kaş ve hafif kapak kullanıldı. Gözyaşı yara izinden ayrıldı.
- Mezar höyüğü görünür hâle getirildi.
- Kefene ağırlık verildi.
- Profil gözü kapak olarak çizildi.
- Serif el yazısı kullanıldı.

## 3. Karar verici (kullanıcı adına onay/revize) — 18.11.2026 05:09'da eklendi

Kullanıcının isteği (birebir): "Benim yerime karar alıcı bir alt agent daha oluştur istenilen akış ve karakterlerin dizide ki hallerini anımsatması için gerekli onay/revizeleri gerçekleştirsin."

Bu ajan, akıştaki **kullanıcı onay noktalarını** üstlenir: model sayfası, küçük kareler ve animatik önizlemesi. Ana ajan taslağı ona verir. Ajan ONAY ya da somut REVİZE döndürür. Revizeler uygulanır ve gerekirse tekrar sorulur. Geri dönüşü zor bir karar varsa ajan "KULLANICIYA SOR:" satırı yazar, o zaman kullanıcıya sorulur. Bitmiş animatik her durumda kullanıcıya gönderilir. Kullanıcının kendi notları her zaman önceliklidir.
İlk oturumdaki kimlik: `a2c1ac3e832fdbed2`.

**Brief (özet, oluştururken tam metni ver):**
> Sen kullanıcı adına karar veren ajansın. Ölçütlerin: (1) akış Vikings dizisine (efsaneye değil) sadık mı, duygu taşınıyor mu; (2) karakterler dizideki hallerini anımsatıyor mu. Bunu yalnızca GENEL ipuçlarıyla değerlendir: kostüm, renk paleti, saç/sakal silüeti, aksesuar, silah, mekân, beden dili; (3) kullanıcının geçmiş geri bildirimleri (CLAUDE.md'deki tercihler).
> DEĞİŞMEZ SINIRLAR: Oyuncu yüzüne benzerlik istenmez. Dizideki imza tasarımlar birebir kopyalanmaz (Ragnar'ın kafa derisi dövmesi + kazınmış yan + tepe örgü; Floki'nin kalın göz sürmesi). Dizinin müziği veya ekran görüntüsü kullanılmaz.
> Önce CLAUDE.md, docs/OTURUM_DEVRI.md, r3/karar_gunlugu.md ve r3/hikaye_taslak_v2.md dosyalarını oku. Görselleri Read ile aç.
> Çıktı: "KARAR: ONAY | REVİZE", kare kare tek cümle, en fazla 6 somut revize maddesi, gerekiyorsa "KULLANICIYA SOR:".

**Verdiği ilk kararlar (madde 12):**
- Athelstan'ın diz çökme kuklası Ragnar kostümünü taşıyordu. Kukla parametreli yapıldı; kürk ve pelerin artık spec'ten geliyor.
- Kapı sahnesi gece rengine çekildi.
- Floki'nin gözleri açık ve tehditkâr çizildi.
- Yakın plana boyun, yaka ve haç eklendi; balta gölgesi duvara düşüyor.
- Haç yağmur altında değil, kulübe zemininde.
- Limanda ejder başlı uzun gemi var, uzakta çatılar.
- Profil başta kulak arkası saçla kapatıldı; açık kalınca "kazınmış yan" gibi okunuyordu.

## 4. Görsel kurul (G1, G2, G3) — 19.11.2026 14:36'da eklendi
Kullanıcı son dört sahneyi görsel olarak çok zayıf buldu. Üç görsel ajanın birbiriyle iletişim kurmasını ve son çıktı uygunluğunu değerlendirmesini istedi. Süreç: `r3/kurul/SUREC.md`. İletişim, ortak `pano.md` dosyası ve tur tur mesajlarla yürür.
- **G1 · Karakter ve tutarlılık:** Model uyumu, oran, poz ve beden dili, çizim kalitesi, sahneler arası tutarlılık.
- **G2 · Kompozisyon, ışık ve renk:** Kadraj, ölçek, derinlik, karakter üstünde ışık, renk planı, atmosfer, mekân doluluğu.
- **G3 · Duygu, oyunculuk ve son çıktı uygunluğu:** Duygu taşıma, ifade, kahraman kare; panoyu toplar ve SON ÇIKTIYA UYGUN / YETERSİZ kararını yazar.
İlk oturumdaki kimlikler: G1 `acfda76e7d76828c9`, G2 `a23e0608ff5c653be`, G3 `ae7543a5199bc859f`. Yeni oturumda bu rollerle yeniden kurulurlar; ilk görevleri `GORSEL_STANDART.md` dosyasını okumaktır.
