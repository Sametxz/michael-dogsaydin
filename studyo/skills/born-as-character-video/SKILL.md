---
name: born-as-character-video
description: "\"X olarak doğsaydın?\" (Born in Lore) tarzında, ikinci tekil şahıs anlatımlı, bir dizi/oyun/tarih karakterinin bütün hayatını anlatan dinamik 2D animasyon video üretir: kaynak harmanı, omurga, cümle=eylem sahne dökümü, anlamsal geçişler, duygu dili, kodla çizim, ses, montaj, 8 dilli yayın paketi."
---

# "X Olarak Doğsaydın?" — dinamik anlatı videosu (v3)

Bir oyun, dizi, mitoloji ya da tarih karakterinin bütün hayatını, izleyiciyi o karakterin yerine koyarak ("sen") anlatan videoyu uçtan uca üretir. Referans: Born in Lore, "What If You Were Born as Kratos?" (8:06). v3, Ragnar videosu bittikten sonra kullanıcının şu isteğiyle yazıldı:

> Söylenen her cümle ekranda hayata geçsin. Cümlenin öğesi o anda gelsin ve hareketli olsun. Sahneler anlamsal geçişlerle akmalı (ör. öğe pencerede belirir, sonraki sahne pencereden devam eder). Duygu görsel öğelerle aktarılsın.

**Repo varsa** (`Sametxz/michael-dogsaydin` (önceki: `Sametxz/ragnar-dogsaydin`)): `studyo/BASLA.md` ile başla. Ayrıntılı kurallar `studyo/docs/`, çalışan motor `studyo/motor/`, şablonlar `studyo/sablonlar/` altında; bu skill onların özetidir.

**Temel ilke:** Bu formatta kalite üç şeyden gelir.
1. **Anlatı:** kısa, kuru, ikinci tekil şahıs cümleler ve imgelerle kapanan bir yay.
2. **Yaşanan anlatım:** Her cümle ekranda bir nesneye ya da eyleme dönüşür, **tam o kelimede** belirir ve hareket eder. Çekimler birbirine bir nesne, biçim ya da açıklık üzerinden akar.
3. **Duygu:** Duygu yüzün yanında ışık, renk, hava, kamera, sembol nesne ve sesle taşınır.

Ragnar'daki hata: Her çekim düzleştirilmiş tek bir kare + yavaş zoom + siyaha kararmaydı. Planlama birimi cümle değil kareydi. Bu yüzden hikâye anlatıldı ama yaşanmadı.

---

## 0. Düşünce biçimi (her kararda)
1. **Sen mi, o mu?** Her cümle "…yapıyorsun" diye kurulur, asla "X şunu yaptı" diye değil.
2. **Bu cümle ekranda ne olarak yaşanıyor, hangi kelimede?** Cevabı yoksa cümle zayıftır ya da sahne eksiktir. Örnek: "15 yaşında kralsın" → ayakları yere değmeyen çocuk, gözüne kayan koca taç. Taç "kralsın" kelimesinde kafaya düşer.
3. **Bu çekim sonrakine neyle akıyor?** Bir nesne, biçim, açıklık ya da hareket. Siyaha kararma yalnızca bölüm sonunda kullanılır.
4. **Duygu hangi kanallardan geliyor?** Yüz/beden, ışık, renk, hava, kamera, sembol nesne, ses. En az dördü aynı şeyi söyler.
5. **Son 3 saniyede ekranda ne oldu?** Cevap "hiçbir şey" ise çekim ölüdür.
6. **Hangi imge geri dönecek?** "Bunu aklında tut" gibi sözlü işaretler zayıftır, kullanılmaz. Ekim imgeyle yapılır.
7. **Son espriden beri kaç saniye geçti?** Hafif bölümde 10–15 sn, trajik anda 10 sn'den fazla şakasız.
8. **İzlemeyen biri anlar mı?** Kim, nerede, neden sorularını yanıtla. Kavram ilk geçtiği yerde açıklanır.

## 1. Değişmez kurallar
- Oyuncuya benzeyen yüz, dizideki imza karakter tasarımının kopyası ve logolar çizilmez. Kimlik aksesuar, renk, silah, yara izi ve hikâye nesneleriyle taşınır. Kullanıcı ısrar ederse yalnızca kopya kısmı reddedilir.
- Kaynak eserin müziği, ekran görüntüsü ve gerçek kişi fotoğrafı kullanılmaz. Kan ve vahşet gösterilmez.
- API anahtarları yalnızca `/home/claude/.secrets/` altında durur (chmod 600). Repoya ya da loga girmez.
- **Kullanıcı onay kapıları:** örgü → blok animatik → ham kareler → animatik. Hiçbir kare (insert ve geçiş karesi dahil) onaysız ses ya da videoya girmez. Görsel yeterliliği kullanıcı belirler.

## 2. Akış
| Aşama | Çıktı | Kapı |
|---|---|---|
| F0 Başlangıç | Tek soru seti: karakter + kaynak, sezonlar, süre (varsayılan 8–9 dk), ses, diller | kullanıcı |
| F1 Kaynak harmanı | `lore_bible.md` (§3) | — |
| F2 Omurga | Tema, çapa, prolog + 6 bölüm, imge yankıları, motifler, duygu eğrisi (§4) | kullanıcı |
| F3 Model ve mekân | Eklemli karakter kartları (yaş evreleri, ifade ve eylem varyantları), kimlik nesneleri, mekân setleri | kurul → kullanıcı |
| F4a Örgü | Anlatım + `dokum/bolum_X.json` → `dokum_kontrol.py` GEÇTİ → A1 + A2 ajanları → tablo sunumu | kullanıcı |
| F4b Blok animatik | Kaba şekillerle gerçek zamanlama, bütün geçişler ve kilitler, 960 px | kullanıcı |
| F4c Ham kareler | Anahtar kareler + geçiş orta kareleri, son kalite, öz değerlendirme en az 2 tur | kurul → kullanıcı |
| F4d Animatik | TTS → kelime zamanları → tam render | kurul → kullanıcı |
| F5 Ses | Bölüm müzikleri, SFX, konuşma öncelikli miks, Whisper testi | — |
| F6 Master | 1080p, −16 LUFS, bölüm damgaları | kullanıcı |
| F7 Yayın | 8 dil SRT, başlık ve açıklama, kapaklar, isteğe bağlı dublaj | kullanıcı |

Her tur sonunda karar günlüğüne bir kayıt ve **Ders** satırı eklenir. Kurul sahne başına tek ajanla toplanır (kredi tasarrufu).

## 3. Kaynak harmanı → `lore_bible.md`
Hafızadan yazma. WebSearch ile tara, her olayı doğrula (dizi ise sezon ve bölüm ver, emin olunmayanı ⚠️ ile işaretle). Çocukluk genelde az belgelenir: ebeveynin efsanesini, doğum koşullarını ve ilk sınavı topla.

Tablo: `# | yaş | olay | kaynak | doğrulandı | duygusal ağırlık | görsel nesne/eylem fikri | imge potansiyeli | geçiş fikri`

Ara:
- **Lakap ya da isim kökeni:** genelde en güçlü gag ve imge.
- **Tekrar eden imgeler:** hayvan, kıyafet, silah, yemin, kehanet.
- **Kaynak çelişkileri:** gizleme, gag yap.
- **Sayılar:** ekranda makbuz, harita ya da tabela olarak.
- **Ölüm ve mirasçıların tepkisi.**

## 4. Omurga → `omurga.md`
- Tek cümlelik tema + duygusal çapa (karakterin başta istediği şey).
- **İmge yankısı tablosu (3 adet):** `imge | 1. görünüş | 2. görünüş | final anlamı | final cümlesi`. Örnek (Ragnar): kol halkası, Athelstan'ın haçı, kuzgunlar.
- **Görsel motifler ve geçiş haritası:** Motif nesne bölümleri bağlar ve geçişlerde taşınır (halka masadan savaşa uçar, pencere bölüm açılışlarında tekrar eder).
- **Duygu eğrisi:** bölüm bölüm duygu; renk planı bu eğriden çıkar.
- Kesim listesi; 1–2 tanesi "Uzun hikâye." gag'ine dönüşür. **Bookend:** açılıştaki obje finalde geri döner.

## 5. Senaryo
- İkinci tekil şahıs, şimdiki/geniş zaman. Cümle ≤ 12 kelime. Çekim başına en çok 2 cümle. Her cümle ayrı seslendirilir.
- Yapı (oransal): Prolog %8–10 · Çocukluk %12 · Gençlik/ilk zafer %15 · İsim kökeni %12 · Kayıp + yeni hayat %15 · Zirve %12 · Düşüş %13 · Miras %8 · Final %5. Yorum çağrısı ilk büyük kayıptan hemen sonra (%37–45).
- **Kanca:** "[Karakter] olarak doğsaydın, [epik 1]. [Epik 2]. Ve tarihe [absürt 3] ile geçerdin. Ama şu an? [Savunmasız başlangıç]."
- **Ses tonu:** Üçlü ritim + kırılma, retorik soru ile dönüş, kuru ve şefkatli alay. Ünlem yağmuru yok.
- **Mizah araç kutusu** (hafif bölümlerde en az iki; aynı teknik arka arkaya kullanılmaz; her esprinin bir görsel karşılığı olur):

| Teknik | Kalıp | Örnek |
|---|---|---|
| Hafife alma | Dev olay + minik yorum | "Bir krallığı yakıp yıkıyorsun. Kötü bir salı." |
| Modern deyim | Mitolojik olay + günlük kalıp | "Sözleşmenin küçük yazılarını hep oku." |
| Ters köşe tekrar | Niyet + aynı kelimelerle sonuç | "Savaşı önlemek için uğraşıyorsun. Savaşı başlatıyorsun." |
| Fiziksel özellik takıntısı | Ciddi sıralama + saçma özellik | "Yenilmez, korkunç ve çok ama çok kel." |
| Resmî lakap | Lakabı gerçek bilgi gibi sunmak | "Kral Kel Charles savaşmıyor. Ödüyor." |
| Atlama | Uzun yan hikâyeyi tek kelimeyle geçmek | "Uzun hikâye." |
| Sayıyı somutlaştırma | Rakam → fiziksel karşılık | "Yedi bin livre. Yaklaşık iki buçuk ton." |
| İnatçı döngü | Tekrar eden olay | "Yine öldün. Yine kalktın." |

- **Trajik anlar:** kurulum → görsel an → tek cümlelik gerçek → şakasız sessizlik. Hareket küçülür ama durmaz (nefes, gözyaşı, mum söner).
- **Final:** dönüşüm → çapaya dönüş → üçlü özet (bookend açılır) → izleyiciye karar sorusu.
- Özel isimler TTS için fonetik yazılır, ekranda doğru yazımla verilir.
- **Öz eleştiri** (her madde ≥ 4/5 olana dek, en fazla 3 tur): kanca, sen-dili, her cümlenin ekran karşılığı, imge yankıları, espri aralığı, trajik anlar, cümle uzunluğu, süre, sesli okuma, kaynak doğruluğu.

## 6. Dinamik anlatım (D1–D10)
| | Kural |
|---|---|
| D1 | Her cümlenin ekranda kelimeye kilitli bir karşılığı vardır (kelime başı −0,15 / +0,1 sn) |
| D2 | Her çekimde: giren ya da eylem yapan öğe + kamera hareketi + ikincil yaşam hareketi (nefes, salınım, duman, su, pelerin) |
| D3 | 3 sn'den uzun olaysız aralık yoktur |
| D4 | Geçişlerin ≥ %60'ı anlamsaldır. Kararma yalnız bölüm sonunda. Sert kesmenin gerekçesi yazılır |
| D5 | Her anlamsal geçişin bağı yazılır: A'daki ne → B'deki ne, neden |
| D6 | Her çekimin duygusu ve duygu taşıyıcısı vardır. Duygu dönüşümü kelimeye kilitlenir, bütün kanallar birlikte döner |
| D7 | Art arda 4 çekim aynı plan ölçeğinde olmaz |
| D8 | Cümle ≤ 12 kelime |
| D9 | Vurucu cümle = görsel efekt + ses olayı |
| D10 | Geçişte bir nesne aynı anda iki yerde görünmez. Kimlik nesnesi tek kaynaktan çizilir |

**Cümle → çekim:** Her cümle için dört cevap yazılır: ne görünür (soyut cümleyi somutlaştır: "zengin oluyorsun" → sandığa altın dökülür), hangi kelimede, nasıl girer ya da ne yapar, sonrakine neyle akar.

**Geçiş kataloğu:**

| Geçiş | Ne yapar | Örnek |
|---|---|---|
| Maske | Bir açıklığın içinden yeni sahneye girilir | Pencere, kapı, göz, kalkan, zarf |
| Nesne taşıma | Nesne A'dan B'ye uçar, zemin değişir | Kimlik nesnesi, mektup, sikke, ok |
| Biçim eşleşmesi | Benzer biçimler üst üste oturur | Ay → kalkan, mum → yanan köy, bebek eli → yetişkin eli |
| Zoom içinden | Bir noktaya dalış | Göze dalış → anı, kehanete dalış |
| Ön plan silme | Önden geçen şey sahneyi değiştirir | Direk, yelken, kalabalık, duman |
| Savurma | Hızlı kamera savrulması | Hız, kovalama |
| Sert kesme | Ani kesme | Şok, ses vuruşu |
| Kararma | Siyaha kararma | Yalnızca bölüm sonu |

Göz noktası A'nın sonunda ve B'nin başında aynı yere düşer. Hareket yönü korunur. Ses kesmeden 0,3–0,5 sn önce gelir (J-cut).

**Hareket sözlüğü:**
- **Giriş:** pop, düş ve sek, kay, yüksel, belir, parla (ışık patlaması), çiz (harita, rota), büyü.
- **İkincil:** nefes, salınım, titreme, süzülme, alev.
- **Karakter eylemleri:** baş çevirme, el kaldırma, uzatma, diz çökme, yumruk, göz kırpma, gözyaşı.
- **Kamera:**

| Hareket | Anlamı |
|---|---|
| İtme | önem |
| Geri çekilme | yalnızlık, kayıp |
| Yukarı tilt | umut, güç |
| Sarsıntı | darbe |
| Eğik açı | huzursuzluk |
| Sabit | gerilim ya da yas |

- **Paralaks:** en az 4 derinlik katmanı (gök 0,05 · uzak 0,3 · orta 0,7 · ana 1 · ön plan 1,4).

## 7. Duygu dili
Duygu yedi kanaldan taşınır: yüz/beden · ışık · renk (grade) · hava/atmosfer · kamera/kadraj · sembol nesne · ses.

| Duygu | Görsel kalıp |
|---|---|
| huzur | sıcak altın, yavaş kayma, toz zerreleri |
| gerilim | soğuk, yüksek kontrast, çok yavaş itme, sis |
| korku | mavi-gri, ani zoom, eğik |
| öfke | kırmızı-turuncu, sarsıntı, kıvılcım |
| zafer | altın, alt açı |
| yas | doygunluk ≈ %50, ağır vinyet, durağan ya da geri çekilme, yağmur/kar, boş alan |
| umut | karanlıktan ışığa, yukarı tilt |

**Duygu cümlesi** her sahnede yazılır: "Seyirci X hisseder çünkü yüzde Y'yi, ışıkta Z'yi ve [nesne]'nin W olduğunu görür."

Kurallar:
- Sessiz okuma testi uygulanır.
- Duygu doruğunda ses azalır.
- Trajik sahnede pembe yanak ya da emoji ağız gibi sevimlilik izi kullanılmaz.
- Görsel stil karakterle büyür: çocukluk sıcak, yetişkinlik epik (kenar ışığı, kızıl gök), son soğuk ve sade.

## 8. Görsel kalite ve yoğunluk
**Çıta:** temiz, gölgeli, sinematik 2D.

**Kesin red:**
- R1 benzerlik ya da kopya
- R2 duygu ile ifade çelişkisi
- R3 kimlik sızıntısı
- R4 kopuk uzuv
- R5 döndürülmüş sprite
- R6 çift nesne
- R7 pozlama hatası
- R8 elle yeniden çizilmiş kimlik öğesi
- R9 zemin ya da temas hatası
- R10 çizgi film sevimliliği
- R11 uydurma gövde
- R12 cılız kalabalık, tören ya da kahraman nesne
- R13 %200 kırpmada vasat görünen nesne
- R14 ölü süre
- R15 cümlenin ekranda görünmemesi
- R16 bölüm içinde kararma
- R17 geçişte sıçrama

**Her kare için:**
- En az 4 katman (her biri ayrı öğe).
- Düz renk alan yok.
- Işık kararıyla başlanır: rim, gölge tarafı, temas gölgesi.
- 6–12 anlamlı ayrıntı.
- Gövde ve kimlik öğeleri model kaynağından gelir.
- Asimetrik karakter aynalanmaz.
- Ara kare ve geçiş karesi de çıtayı taşır.

**Öz değerlendirme döngüsü:** render → Read ile bak → 1–5 puan → 4'ün altını düzelt. En az 2, en çok 4 tur.

**Diegetik grafik öğeleri** (bilgiyi ekranda nesneye çevir, kelimeye kilitle):
- Sözleşme, taş tablet, yapılacaklar listesi.
- Makbuz + "ÖDENDİ" damgası.
- Harita + çizilen rota.
- Portre çerçevesi + pirinç plaka.
- Aile ağacı.
- Tabela.
- Oyun çubukları (ÜN: sen ↓ oğullar ↑).
- Bölünmüş ekran.
- Etiket + el çizimi ok (tırmanan etiketler).
- Konuşma balonu ("ADIN?" / ". . .").

**Diğer görsel kurallar:**
- **Ölçek = güç:** tanrılar ve krallar dev, çocuk minik.
- **Tipografi:** Cinzel ya da Pirata One (epik), Luckiest Guy (gag), Caveat Brush (not), Alegreya (parşömen). Türkçe glifleri kontrol et (ş ğ ı İ).
- **Ekrana gömülü altyazı yok** (SRT ayrı verilir). Bölüm başında sinematik başlık kullanılır.

## 9. Karakter tasarımı (özgün, kodla)
- Arketip + kaynak metindeki ayırt edici öğeler kullanılır. Korunan tasarım kopyalanmaz.
- **Oranlar:** yetişkin ≈ 4,5 kafa, genç ≈ 3,5, çocuk ≈ 2,4, bebek kundakta. Kadın savaşçı rolünün fiziğiyle çizilir.
- **Yüz:** göz akı, iris, bebek ve parlama. Göz kapağı ifadeye göre değişir. Kaş en son katmandır.
- **İfade seti:** neutral, joy, grief, anger, fear, resolve, smug, surprised, pain.
- **Eklemli rig (v3):** baş, gövde, üst kol, ön kol, el, göz kapağı, pelerin ve saç ayrı parçalardır, her biri kendi pivotuyla. Kelimeye kilitli eylemler bu sayede yapılır. Eller relax, fist, grip ve open şekillerini alır.
- **Katman sırası:** gölge → arka saç → pelerin → bacaklar → gövde → zırh → kollar → boyun/kafa → eldeki obje → eller.
- **Kadro testi:** Bütün karakterler tek tabakada aynı ölçekte çizilir. Yaşlanma parametrik spec'ten türetilir. Kimlik bayrakları türetilen karakterde kapatılır.

## 10. Kelimeye kilitli zamanlama
1. Her cümle ayrı bir TTS dosyasıdır. Kelime zamanları faster-whisper (`word_timestamps`) ile alınır.
2. Görüntü sese göre zamanlanır: çekim süresi = satırların gerçek süresi + boşluklar.
3. Her giriş, eylem, kamera vuruşu ve ses efekti bir kelimeye bağlanır (`ck.k("kelime", ofset)`). Kelime bulunamazsa hata verilir, sessiz kayma olmaz.

## 11. Render mimarisi
- Her öğe bir kez `rsvg-convert` ile PNG sprite olur (md5 önbelleği). Kareler skia-python ile birleştirilir, ham RGBA tek bir ffmpeg sürecine borulanır (1080p30, libx264 veryfast crf 18). Her kareyi tam SVG olarak rasterize etmek yasaktır.
- **v3 motoru** (`studyo/motor/`):
  - `Cekim`: sahne grafiği ve kelime kilidi.
  - `Oge`: derinlik/paralaks, giriş/çıkış, ikincil hareket, eylemler.
  - `Kamera`: x/y/zoom ve sarsıntı.
  - `Duygu`: renk matrisi, ışık degradesi, vinyet, çekim içi dönüşüm.
  - Geçişler: `Maske`, `NesneTasi`, `Eslesme`, `ZoomIcinden`, `OnPlanSil`, `Savurma`, `Kes`, `Karart`.
  - `Film.render()` / `onizle()` / `zaman_cizelgesi()`.
  - `dokum_kontrol.py`: D1–D10 denetimi.
  - Örnek: `ornek/demo.py`.
- Canlı efektler skia ile çizilir: vinyet, parlama, ışık hüzmesi, parçacıklar (kor, kar, toz, yağmur), el çizimi ok, şimşek ve flaş.
- Doku (`feTurbulence`) sprite'a pişirilir. Zamanla değişen ayrıntı skia ile çizilir, sprite içi zamandan bağımsızdır.
- Önce önizleme tabakası (960 px) hazırlanır, tam render bölüm onaylanınca yapılır. Geçici adla yazılır, başarıda yeniden adlandırılır.

## 12. Ses
- **TTS:** ElevenLabs "George", `eleven_v3`, `language_code: tr`, satır başına bir dosya. Yedek: XTTS-v2 ya da Piper (`tr_TR-dfki-medium`). Telaffuz sözlüğü tutulur.
- **Müzik:** Eleven Music. Vokalsiz, anlatıma yer bırakan, döneme uygun. Bölümler duygu dönüşlerine hizalanır. Ayrı müzik izinli anahtar gerekebilir. Aynı anda en fazla 2 istek gönderilir.
- **SFX:** ElevenLabs Sound Effects kütüphanesi (ambiyans + nokta efekt), kelimeye bağlı.
- **Miks:**
  - Konuşma satırı RMS −19 dB.
  - Müzik konuşma altında ~−8 dB, 2,5 kHz bandında −5 dB EQ.
  - Ambiyans %55, nokta efektler %50 kısılır.
  - Duygu doruklarında sessizlik.
  - Geniş bantlı efektler satır aralarına konur.
  - Çıkış −16 LUFS.
  - Whisper anlaşılabilirlik testi zorunlu.

## 13. Ajanlar (değerlendirir, üretmez)
- **A1 · Hikâye:** dizi doğruluğu, "hiç izlememiş biri anlar mı" puanı (1–5), 12 kelime sınırı, ekim-biçim takibi.
- **A2 · Sahne yönetmeni:**
  - D1–D10 denetimi.
  - Cümleden görüntüye somutluk.
  - Geçiş bağları.
  - Yedi duygu kanalı.
  - Ölü süre.
  - En güçlü ve en zayıf 3 an.
- **G · Görsel kurul (tek ajan):** R1–R17, 0–3 puan, referans kareyle yan yana karşılaştırma, DERSLER satırı.
- **K1 · CTR + K2 · Sanat yönetmeni:** kapaklar.

## 14. Yayın paketi
- **Başlık:** `{Karakter} Olarak Doğsaydın? | {Seri}`. 8 dilde başlık ve açıklama.
- **Açıklama:**
  - İkinci tekil şahısla kanca.
  - Anahtar isimler.
  - Kapanış sorusu + "sırada kim?"
  - Bölüm zaman damgaları.
  - Kaynaklar.
  - "Tüm çizimler, animasyon ve müzik özgündür" + resmî olmayan hayran çalışması beyanı.
  - 3 hashtag.
- **SRT:** satır başlangıcına kilitli, 2 satır × 42 karakter. Espriler işlevine göre çevrilir.
- **Kapak:** önce/sonra düzeni, kısa büyük metin, 8 dil. 168 ve 320 px'te okunurluk test edilir. Küçük boyutta gözler açık çizilir.
- **İsteğe bağlı dublaj:** dil başına ses parçası, video uzunluğunda.

## 15. Son kontrol
- [ ] Her olay kaynakla doğrulandı
- [ ] `dokum_kontrol.py` her bölümde GEÇTİ
- [ ] Sessiz izlemede ölü süre yok, sesli izlemede her cümle görünüyor
- [ ] Anlamsal geçiş ≥ %60, kararma yalnızca bölüm sonlarında
- [ ] Her sahnenin duygu cümlesi var ve sessiz okuma testini geçiyor
- [ ] İmge yankıları ve bookend finalde kapanıyor, "aklında tut" tipi sözlü işaret yok
- [ ] Tanınır resmî tasarım, oyuncu yüzü, logo ya da kaynak eser müziği yok
- [ ] Onaylar karar günlüğünde kayıtlı
- [ ] Ses: Whisper testi, −16 LUFS
- [ ] Teslim: master + SRT + yayın paketi + kapaklar. Bir satırda sıradaki karakter önerisi
