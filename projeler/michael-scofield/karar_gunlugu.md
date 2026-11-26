# Karar günlüğü: Michael Scofield Olarak Doğsaydın?

Her tur sonunda bir kayıt eklenir. **Ders** satırı zorunludur. Tekrarlayan dersler `studyo/docs/06_DERSLER.md`'ye taşınır.

## Tur 1 · 26.11.2026 15:44–16:00 · F0 Başlangıç
- Sunulan: ortam kurulumu, yeni ana repo `Sametxz/michael-dogsaydin`, F0 soru seti.
- Sorulan kararlar ve yanıtlar:
  - Karakter → Michael Scofield (Prison Break).
  - Kapsam → S1–S4 + The Final Break; çocukluk ekimleri, Fox River, kaçış, Sona… (S5 / Ogygia kapsam dışı).
  - Süre → ~9 dk (prolog + 6 bölüm).
  - Anlatıcı → George değil, **farklı bir ElevenLabs sesi**; örnekler dinletilip seçilecek.
- Yapılanlar: Ragnar stüdyo paketi ve kod kütüphanesi yeni repoya taşındı, motor demo ile sınandı, proje iskeleti kuruldu.
- Ders: Kullanıcı yeni projede yeni bir ses istiyor → Ragnar tercihleri varsayılan değil, başlangıç önerisidir → her yeni projede ses, renk ve ton gibi "kimlik" kararları yeniden sorulur.

## Tur 2 · 26.11.2026 15:53–16:40 · F1 Araştırma + F2 Omurga taslağı
- Kullanıcı talimatı (15:53): ses şimdilik yerel TTS, ElevenLabs en sonda; olay tablosu sezon/bölüm bazında; anlatım sürekli akışlı, geçişli, dinamik, neredeyse her cümle sahnede; bütün karar aşamalarında sor; taslaklar düşük kalitede, tam kalite yalnızca yayına hazır videoda.
- Sunulan: `lore_bible.md` (57 olay, S1–S4 + Final Break, ✅/⚠️ işaretli), `omurga.md` v1 (tema, çapa, 3 imge yankısı, motif-geçiş haritası, prolog + 6 bölüm, duygu eğrisi, kesim listesi).
- Kontrol: Wikipedia S1E16 özeti cinayeti Michael'a yüklüyor (yanlış, Lincoln'e kurulan tuzak); depo sahnesinin yaşı 11+ olmalı (anne "öldükten" sonra koruyucu aile) → prolog düzeltildi.
- Ders: İkincil özetler küçük ama kritik hatalar taşıyabilir → her olay en az iki kaynakla ya da bölüm özetiyle çapraz kontrol edilir; yaş ve sıra bilgisi kronolojiden türetilerek denetlenir.
- Sorulan kararlar ve yanıtlar:
  - Bölüm yapısı (V = Sona + Scylla, 1:35) → **bu yapı kalsın**.
  - Prolog kancası ("On bir yaşındasın. Karanlıktasın…") → **uygun**.
  - Sara'nın kutusu (S3E3) → **kapalı kutu + sembol** (yağmur, titreyen eller, solan renk).
  - Michael'ın ölümü → **kıvılcım + sönen ışık**, sandalye kıvılcımıyla eşleşme; Sara kapıdan geçer.
- Ders: Kullanıcı dört önerinin dördünü de kabul etti → omurgada imge yankısı ve duygu eğrisi baştan net verilince karar hızlanıyor → F3 ve örgülerde de her soruyu bir imgeye bağlayarak sun.

## Tur 3 · 26.11.2026 16:07–16:25 · F3 stil testi
- Kullanıcı: "düşük kalite = çözünürlük; içerik kalitesi yüksek olsun" (16:07). "Ragnar tarzına bağlı kalma; konuya ve yeni akışa odaklan; daha dinamik, her cümle ekranda, akış yüksek, ekranda tutuculuk artırılmalı" (16:08).
- Sunulan: `stil/stil_kontakt.png` — aynı an (sırttaki planın duvara akışı) üç stilde: A mavi plan, B sinematik 2D, C noir. Özgün dövme ilk kez çizildi (kapı kemeri, iki turna, sütunlar; gizli plan çizgileri).
- Öz değerlendirme: 1. tur kafa yumurta gibi, kol yok, harita kafanın arkasında → 2. tur Michael sol üçte bir, harita sağ duvarda, deltoid ve kol kıvrımı, saç dokusu → 3. tur akış yayları öne alındı, sırttan başlatıldı.
- Kararlar: Stil → **B + A hibrit**. Tutuculuk → **geri sayım sayacı, kinetik kilit kelimeler, görsel açık döngüler** (ilerleme çubuğu seçilmedi).
- Ders: Kullanıcı "düşük kalite" derken çözünürlüğü kastediyordu → belirsiz kalite talimatlarında çözünürlük ile içerik ayrımı en baştan sorulur ya da varsayılan "içerik tam, çözünürlük düşük" alınır. Stil kararı tek bir ortak an üzerinden sunulunca hızlı çıktı.

## Tur 4 · 26.11.2026 16:25–16:50 · F3 Michael model kartı v1
- Sunulan: `kartlar/model_michael_v1.png` — yetişkin tam figür (mavi gömlek, 94941, sıvalı kollar, önkol dövmesi), 3 görünüş, 6 ifade (odak, kararlı, yas, korku, şefkat, plan görüşü), önkol dövmesi kapalı/ışıklı, kâğıt turna (+ kanat çırpma pozu), 11 yaş figür ve baş.
- Teknik: Ragnar'ın `head3` fonksiyonu her erkek karaktere Ragnar'ın yarasını ekliyordu (R3 sızıntı riski) → projeye özel eklemli `karakter.py` yazıldı (kafa, kol, figür, dövme ve turna tek kaynak).
- Öz değerlendirme: 1. tur nokta gözler, turna uçağa benziyor, diken saçlı çocuk, numara kolun altında → 2. tur büyük gözler, yeni turna, yuvarlak tutamlı saç, numara sol göğüste → 3. tur turna kanatları genişletildi, sarkan eller parmak aşağı, etiket çakışması giderildi.
- Ders: Ödünç alınan karakter fonksiyonları başka karakterin kimlik öğelerini varsayılan olarak taşıyabilir → yeni projede kimlik bayrakları varsayılan "kapalı" olan yeni modül yazılır.

## Tur 5 · 26.11.2026 16:50–17:15 · F3 beden dinamiği, eylem kartı, turna v3
- Kararlar (Tur 4 sorusu): model kartı → **yön doğru, beden dinamikleşsin**; turna ve dövme → **uygun**. Kullanıcı ardından (16:18): **"turnayı iyileştir, daha belirgin ve gerçekçi olmalı."**
- Yapılanlar: `karakter.py` → `figur2()` iskeletli, pozlanabilir figür (gövde eğimi, baş, omuz/dirsek, kalça/diz; pelvis yüksekliği ayağa göre otomatik). `POZLAR`: bak, dokun, yürü, koş, turna uzat (her biri 3 anahtar kare). `kartlar/eylem_michael_v1.png`.
- Turna v3.1: elmas gövde, ince boyun ve kuyruk sivrileri, aşağı katlı baş, V açısıyla kalkan geniş üçgen kanatlar (kat iziyle ışık/gölge yüzeyi), sabit kontur kalınlığı, kanat çırpma parametresi, elde tutulurken gölge/hale kapalı. `kartlar/turna_v3.png` (+ R13 kırpması, 120/60/32 px okunurluk).
- Öz değerlendirme: turna 1. tur kanatlar şerit gibi, taç görünümü, kirli doku → 2. tur geniş üçgen kanatlar, hafif doku → 3. tur liflerin taşması ve kalın sabah ışığı giderildi. Eylem kartı: koşu orta karesi çökük → yeniden kuruldu; elde turnanın gölgesi kaldırıldı.
- Ders: Origami gibi gerçek nesnelerde siluet önce doğru kurulmalı (kanat = gövde sırtından çıkan geniş üçgen); doku ve ışık ancak siluet okunduktan sonra eklenir. Küçük boyut (32 px) kontrolü siluet hatasını hemen gösterir.

## Tur 6 · 26.11.2026 17:15–17:35 · Turna v4, Michael yüz tipi v2
- Kullanıcı: turna "ilk bakışta kâğıttan turna olduğu daha anlaşılır olsun"; Michael "başrole biraz daha benzet, benzerlikten çok uzak kalmış".
- Sınır: oyuncunun yüzü kopyalanmaz (değişmez sınır). Yalnız karakterin genel imza özellikleri güçlendirildi: daha uzun ve köşeli yüz (face_len 1.2, jaw 0.9), elmacık ve çene hatları, dar odaklı açık gözler, düz alçak kaşlar, belirgin sakal gölgesi, koyu kısa kazınmış saç.
- Turna v4: klasik origami fotoğrafı açısı (hafif üstten 3/4), kanatlar iki yana geniş açık, belirgin katlı baş/gaga, ince boyun ve kuyruk. Hata: kenar ışığı yolunda `fill="none"` yoktu → SVG siyah doldurdu (v3'teki gri lekeler de buydu) → düzeltildi.
- Ders: SVG'de çizgi olarak düşünülen her `path`'e `fill="none"` yazılır; yoksa açık yollar siyah dolgu üretir. Nesne tanınırlığında açı siluetten önemlidir: nesnenin en çok fotoğraflandığı açı seçilir.
- Kararlar: Turna v4 → **onaylı, kilitlendi**. Michael → kullanıcı: "benzerlik için 2 ajan çalışsın, hem küçüklüğü hem yetişkin hâli iyileştirilsin, optimal sonuç çıksın, denetçilerden geçsin" → A-Y (yetişkin) ve A-Ç (11 yaş) üretici ajanlar paralel, ardından bağımsız denetçi (D).

## Tur 7 · 26.11.2026 16:26–17:20 · Michael ajan turu (A-Y, A-Ç, denetçi D)
- Kullanıcı (16:26) oyuncunun iki fotoğrafını "referans görseller" olarak gönderdi → **kullanılmadı**: gerçek kişi fotoğrafından yüz çizmek değişmez sınır; fotoğraflar repoya ve ajanlara verilmedi. Yakınlık yalnız genel imza özellikleriyle.
- A-Y (yetişkin) v3 → D denetimi: tanınırlık 2/3, çocuk 1,5/3, süreklilik 1/3. Kullanıcı (16:34): "tip benzemiş ama yüz sempatik, çekici durmuyor" → A-Y v4 (yüz %8 kısa, köşeli çene, çizgi gürültüsü yok, catchlight'lı canlı gözler, sıcak 2 ton ten, odak'ta hafif sıcaklık), A-Ç v3 (yetişkinin renk/göz/kaş/burun şablonu ortak, dağınık perçem, tek parça kol).
- D yeniden denetim: tanınırlık Y 2/3, Ç 2/3; çekicilik Y 2/3, Ç 2,5/3; süreklilik 2,5/3; R1–R13 yok; karar ikisi de "küçük düzeltmeyle uygun". Kalan: sakal gölgesi (imza) hafifçe geri, çocuk sağ kol birleşimi, yetişkinde çene köşesi + hafif elmacık, saç dokusu biraz koyu.
- Ders: Tanınırlık ile çekicilik ayrı eksenlerdir; tip özellikleri (çizgi, sakal noktası, sert gölge) eklendikçe çekicilik düşebilir → iki ekseni ayrı puanla, imza öğeyi en az görsel gürültüyle ver.

## Tur 8 · 26.11.2026 17:20–17:45 · Michael kilit ve entegrasyon
- Kararlar: yüzler → **son rötuşlarla kilitle**; sakal → **yumuşak, hafif ton (noktasız)**.
- Son rötuş: yetişkin v5 (noktasız yumuşak sakal tonu, çene köşesine hafif açı, çok hafif elmacık gölgesi, koyu ve ince saç dokusu); çocuk v3.1 (kol-omuz tek kontur, önden saç yanları kavisli).
- Entegrasyon: `karakter.kafa` artık yönlendirici → `_tip="michael"` yetişkin `aday/yetiskin.py`, çocuk `aday/cocuk.py`; diğer karakterler `kafa_temel`. `figur2` çocuk Michael'ı `cocuk.figur`'a yollar, yetişkinde boyun kısaltma ofseti uygular. `MICHAEL_COCUK` sadeleştirildi (renkler tek kaynak). Kartlar: `kartlar/model_michael_v2.png` (kilitli), `aday/sureklilik.png`.
- Hatalar: (1) `yetiskin` modülü hem `aday.yetiskin` hem `yetiskin` adıyla iki kez yüklendi → iki ayrı kimlik sayacı → SVG `id` çakışması → uzak göz beyaz leke. Çözüm: tek modül adı. (2) Eski çocuk tanımındaki renkler yeni tanımın üstüne yazıldı (kahverengi saç) → tanım sadeleştirildi.
- Ders: Sayaçla kimlik üreten modül tek adla içe aktarılmalı; her birleşik SVG'de tekrarlayan `id` taraması yapılır (`re.findall(r'id="..."')`). Onaylı tasarım tek kaynaktan okunur, eski tanım kalıntıları silinir.
- Kullanıcı (Tur 9 sorusu): "Sara daha sıcak, çekici ve yan profilini iyileştir"; sıra → **prolog örgüsü + blok animatik** (mekânlar ondan önce).
- Sara v2: kadın profili (yumuşak alın, küçük kalkık burun, dolgun dudak, yuvarlak çene), yanda saç kafatasını sarar, perçem yukarı, gözler büyük ve açık (goz_k 1.14, goz_h 0.86, kapak_ac 0.12), hacimli dalgalı saç + parlama, sıcak yanak tonu, belirgin dudak, kalın kirpik; varsayılan görünüşler "şefkat". `kartlar/model_yan_v2.png`.
- Ders: Aynı yüz sistemini kadın karaktere taşırken profil (side) ayrı çizilmeli; genişlik ölçeği yetmez.

## Tur 10 · 26.11.2026 18:10–18:35 · F4a prolog örgüsü v1 + Sara v3
- Sunulan: `dokum/prolog.json` (5 çekim, ~21 sn + 3 sn başlık, anlamsal geçiş 4/4, dokum_kontrol GEÇTİ) ve `orgu/prolog_v1.md`.
- Kullanıcı: örgü sorusuna cevap yerine "Sara'nın vücudu hâlâ kadın vücudu gibi olmamış; yüzü yarım, yüzü tam yap; çekici, sevecen durmalı". Ses sorusu yanıtsız → varsayım: blok animatikte yerel XTTS.
- Sara v3: yüzü örten saç tutamları kaldırıldı/dışarı alındı (3/4'te uzak saç yüzün arkasında), `figur2` kadın bedeni (omuz ×0.8, bel 40, kalça 60, önlük kalçanın altına iner, kol ×0.78, bacak ×0.7, alçak topuklu sivri ayakkabı), açık önlük + bele oturan bluz.
- Prolog örgüsü onayı bekliyor.
- Ders: Kadın karakterde yalnız yüzü değiştirmek yetmez; omuz-bel-kalça oranı ve kıyafet kesimi silüeti belirler. Saç tutamı yüzün iç konturunu kesmemeli (yarım yüz algısı).

## Tur 11 · 26.11.2026 18:35–19:20 · F4b prolog blok animatiği v1 + Sara ajan turu
- Kararlar: Sara → **yüz yeniden ajanlarla**; prolog örgüsü v1 → **onaylı, blok animatiğe geç**. Ses sorusu yanıtsız → varsayım: yerel XTTS (Damien Black, geçici).
- Sara: tasarım ajanı `aday/sara.py` (kadın yüzü ayrı çizim, büyük açık badem göz + kirpik, ince kavisli kaş, küçük burun, dolgun kupid yaylı dudak, sıcak yanak; saç yüzün arkasında, yalnız perçem/şakak önde; kadın profili; 4 öz değerlendirme turu). `karakter.kafa`: `_tip="yan"` + female → sara.kafa. Kart: `kartlar/model_yan_v3.png`.
- Prolog blok animatiği: `prolog.py` → `out/prolog_blok_960.mp4` (23,8 sn, git dışı), kontakt `kurul/prolog_blok_kontakt_v1.png`. 5 çekim + başlık; geçişler: ZoomIcinden (plan noktası → hücre), OnPlanSil (parmaklık), Eslesme (plan çizgisi → kapı aralığı ışığı), ZoomIcinden (çocuğun yüzü), Maske (kapı aralığı → başlık). Kinetik kelimeler EZBERE, HARİTA; "Ama"da ışık söner + sarsıntı.
- Teknik sorunlar: (1) transformers 5.x XTTS'i bozuyor → 4.57.6 sabitlendi (requirements). (2) faster-whisper ↔ av uyumsuz → `kelime.py` sesi soundfile + resample ile okuyor. (3) XTTS uydurma kuyrukları → satır son kelimede kesiliyor; "Karanlıktasın mı ya" → satır yeniden üretildi. (4) Whisper yazım farkları (hapishaniyi, ez verebilirdin) → kilit fonksiyonu aday listesi + yedek sıra. (5) Kafa sprite'ları tuval merkezine çevrilmemişti → translate eklendi.
- Ders: Kelime kilidi aday kökler listesiyle yazılır (ASR yazım farkları); her TTS satırı Whisper'la doğrulanır ve son kelimede kesilir; sprite'a çevrilen her SVG, çapa noktasına göre tuval merkezine çevrilir ve ilk kontakt sayfasında konumu kontrol edilir.
