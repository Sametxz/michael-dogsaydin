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

## Tur 7 · 26.11.2026 16:32–16:46 · F3 Michael Yetişkin (A-Y) + 11 Yaş (A-Ç) v2 + Görsel Kurul
- Kullanıcı kuralı: **GitHub yalnızca read-only** tutulur; tüm geliştirmeler lokalde kalır (`git push` yapılmaz).
- Yapılanlar: A-Y (`kartlar/ay_yetiskin.py` → `ay_yetiskin_v2.png`, `ay_yetiskin_r13.png`) ve A-Ç (`kartlar/ac_cocuk.py` → `ac_cocuk_v2.png`, `ac_cocuk_r13.png`) izole dosyalarda paralel 3'er tur öz değerlendirme ile üretildi; ardından bağımsız Görsel Kurul (`gorsel-kurul`) denetimi yapıldı.
- Kurul özeti:
  - **A-Y Yetişkin v2:** **SON ÇIKTIYA UYGUN** (G1 3/3, G2 3/3, G3 3/3, D2 2/3, R1–R13 geçer). İsteğe bağlı küçük cila: saçta ince stipple dokusu ve R13 #3 sol kaş taşması.
  - **A-Ç 11 Yaş v2:** **YETERSİZ (R10, G1)** (G1 1/3, G2 2/3, G3 2/3, D2 2/3). Prolog depo ışığı güçlü, R3/R4 temiz; ancak gözler fazla yuvarlak/parlak (R10 riski), konturlar A-Y'den kalın ve yüz düzlem gölgeleri eksik (G1 stil kopukluğu), kollar hafif uzun.
- Ders: Aynı karakterin yaş varyantları paralel üretilirken önce ortak stil şablonu (kontur kalınlığı, göz oranı, yüz düzlem gölgelemesi) kilitlenir; çocuk karakterde yaş farkı büyük yuvarlak gözlerle değil anatomi ve oranla verilir.
- Bekleyen karar: A-Y v2 onayı + A-Ç'nin A-Y stiline hizalanıp yeniden kurula çıkması.

## Tur 8 · 26.11.2026 16:47–16:56 · F3 Michael Yetişkin (A-Y) + 11 Yaş (A-Ç) v3 + Görsel Kurul
- Kullanıcı geri bildirimi: Yetişkin Michael'ın yüzü orijinal Scofield arketipine daha yakın olmalı.
- Yapılanlar (R1 sınırları içinde, lokal):
  - **A-Y v3** (`ay_yetiskin_v3.png`, `ay_yetiskin_r13_v3.png`): 1–2 numara kazınmış buzzcut (şakak fade + stipple), ağır kapaklı buz-mavisi/gri-yeşil gözler (`#7EB6BE`), doğal üst/alt dudak hacmi, temiz sakal gölgesi; R13 #3 kaş taşması temizlendi ve #5 önkol dövmesi %200 paneli eklendi.
  - **A-Ç v3** (`ac_cocuk_v3.png`, `ac_cocuk_r13_v3.png`): R10 yuvarlak çizgi film gözü kaldırıldı, A-Y kontur kalınlığı ve yumuşatılmış yüz düzlem gölgelerine hizalandı, tam boy kol oranı ve dirsek kırığı düzeltildi.
- Kurul sonucu: Hem **A-Y v3** hem **A-Ç v3** tüm alanlarda **3/3** (G1, G2, G3, D2; R1–R13 geçer) alarak **SON ÇIKTIYA UYGUN** bulundu.
- Ders: Oyuncu yüzü kopyalamadan karakter tanınırlığını en çok artıran öğeler kask gibi olmayan gerçekçi saç silueti (fade+stipple buzzcut), göz kapağı/iris dili ve dudak hacmidir.
- Bekleyen karar: A-Y v3 ve A-Ç v3 kullanıcı onayı → onaylanırsa `karakter.py` entegrasyonu ve F3'ün kalan kartları (Lincoln, Sara, mekânlar).

## Tur 9 · 26.11.2026 16:56–17:10 · Michael v3 Entegrasyonu + Lincoln (A-L) & Sara (A-S) v1 + Görsel Kurul
- Karar (Tur 8): A-Y v3 ve A-Ç v3 **onaylı, kilitlendi** → `karakter.py`'ye entegre edildi (`michael_kafa`, `michael_figur`, `michael_dovme_onkol`, `michael_cocuk_kafa`, `michael_cocuk_figur`).
- Yapılanlar (lokal): Kilitli v3 stil şablonuyla **A-L (Lincoln Burrows)** (`al_lincoln.py` → `al_lincoln_v1.png`, `al_lincoln_r13.png`) ve **A-S (Sara Tancredi)** (`as_sara.py` → `as_sara_v1.png`, `as_sara_r13.png`) paralel üretildi, ardından bağımsız **Görsel Kurul (`gorsel-kurul`)** denetimi yapıldı.
- Kurul sonucu: Hem **Lincoln v1** hem **Sara v1** tüm alanlarda **3/3** (G1, G2, G3, D2; R1–R13 geçer) alarak **SON ÇIKTIYA UYGUN** bulundu. (Sara için isteğe bağlı ufak not: saç uçları hafif inceltilebilir, yakın plan el sahne üretiminde daha anatomik eklemlenir.)
- Ders: Önceki turdan çıkarılan "ortak kilit şablon" dersi anında meyve verdi — iki yeni ana karakter ilk turda sıfır stil kopukluğuyla kuruldan tam puan aldı.
- Bekleyen karar: Lincoln v1 ve Sara v1 kullanıcı onayı → onaylanırsa `karakter.py` entegrasyonu ve F3 mekân kartları (veya F4 Prolog örgüsü).

## Tur 10 · 26.11.2026 17:11–17:22 · Lincoln Entegrasyonu + Sara v2 + F3 Ana Mekânlar v1 + Görsel Kurul
- Karar (Tur 9): Lincoln v1 **onaylı, kilitlendi** → `karakter.py`'ye entegre edildi (`lincoln_kafa`, `lincoln_figur`). Sara için "biraz daha sevimli ve çekici" revizyonu istendi.
- Yapılanlar (lokal):
  - **A-S Sara v2** (`as_sara_v2.png`, `as_sara_r13_v2.png`): Daha narin yüz/çene oranları, sıcak gül-şeftali dudak tonu, zarif kirpik hattı, uçları incelen (*tapered*) dalgalı saçlar ve anatomik anahtar eli.
  - **A-M Ana Mekânlar v1** (`am_mekanlar.py` → `am_mekanlar_v1.png`, `am_mekanlar_r13.png`): 3 temel mekân (Karanlık Depo, Fox River Hücresi, Fox River Revir), her biri `studyo/motor/` paralaksına hazır 5 katmanlı (`uzak/orta/sahne/plan/onplan`), Stil B + A hibrit.
- Kurul sonucu: Hem **Sara v2** hem **Ana Mekânlar v1** tüm alanlarda **3/3** (G1, G2, G3, D2; R1–R13 geçer) alarak **SON ÇIKTIYA UYGUN** bulundu.
- Ders: Kadın karakterde çekicilik/sıcaklık R10 sınırına kaymadan yumuşak dudak/elmacık tonu ve tapered saçla; mekânda güven/tehdit duygusu ise sıcak-soğuk palet kontrastıyla (Revir vs. Hücre) taşınır.
- Bekleyen karar: Sara v2 ve 3 Ana Mekân kartı onayı → onaylanırsa F3 tamamlanıp F4a Prolog + Bölüm I örgüsüne geçilir.

## Tur 11 · 26.11.2026 17:24–17:27 · F3 Kilitlendi + F4a Prolog Dökümü Doğrulandı
- Karar (Tur 10): Sara v2 ve 3 Ana Mekân kartı **onaylı, kilitlendi** → `karakter.py`'ye entegre edildi (`sara_kafa`, `sara_figur`, `mekan_depo`, `mekan_hucre`, `mekan_revir`). **F3 ✅ tamamlandı.**
- Yapılanlar (lokal): Kullanıcının verdiği Prolog örgüsü v1 ("Kapının altındaki ışık", P.01–P.05 + P.06 başlık kartı) `dokum/prolog.json` ve `orgu/prolog_orgu.md` olarak kaydedildi.
- Otomatik denetim: `dokum_kontrol.py` → **6 çekim · ~24 sn · anlamsal geçiş 5/5 (%100) · 0 hata, 0 uyarı → GEÇTİ**.
- Ders: Örgüden JSON dökümüne geçişte her cümlenin kilit kelimesi, `duygu_donusum` anı ve `oge_a/oge_b` geçiş bağları birebir şemaya oturtulunca `dokum_kontrol.py` ilk seferde sıfır uyarıyla geçer.
- Bekleyen karar: F4b Prolog blok animatiğine (960 px hareket taslağı) geçilsin mi, yoksa önce A1+A2 denetimi / Bölüm I örgüsü mü yapılsın?

## Tur 12 · 26.11.2026 17:28–17:56 · F4b Prolog Blok Animatiği (960 px) + A1/A2 & Görsel Kurul Denetimi
- Yapılanlar (lokal):
  - `studyo/motor/sahne.py` (`resvg_py` fallback) ve `gecis.py` (`imageio-ffmpeg` fallback + `STUDYO_FAST=1` taslak hızlandırma + `ZoomIcinden` tepe flaş opaklığı `%90 → %45`) Windows uyumlu hâle getirildi.
  - `blok/prolog_blok.py` → `blok/prolog_blok_960.mp4` (960×540, 20 fps, 20.4 sn, 6 çekim, 5/5 anlamsal geçiş) ve `blok/prolog_kontakt_960.png` (12 kare: 6 çekim + 5 geçiş orta karesi + vurucu an) üretildi.
- Alt ajan denetimi: Hem **A1+A2 (`hikaye-ve-sahne`)** hem **Görsel Kurul (`gorsel-kurul`)** denetiminden geçirildi. Yakalanan 4 bulgu (P.03 kesik boyun + yazı çakışması, P.04 11 yaş yüzen kafa/R4, P.05 lore dışı erken turna, Geçiş 1 & 4 flaş opaklığı/R17 + kontakt Türkçe font) anında v2'ye işlendi.
- Ders: F4b taslak animatiklerde `ZoomIcinden` tepe flaşı %45 bandında tutulduğunda ve `STUDYO_FAST=1` ile ağır CPU blur'ı kapatıldığında hem geçiş köprüsü okunur kalır hem taslak render süresi ciddi ölçüde kısalır.
- Bekleyen karar: F4b Prolog blok animatiği kullanıcı onayı → onaylanırsa F4c Prolog ham kareleri (son kalite) veya Bölüm I örgüsü.

## Tur 13 · 26.11.2026 18:28–18:48 · A-Sırt v1 (Anatomik Sırt & 5 Katmanlı Dövme) + Yüksek Tempolu Prolog F4b v3
- Kullanıcı yönlendirmesi (18:28): Vücut daha iyi modellenmeli, sırt dövmesi çok daha detaylı olmalı; sahneler 3. şahıstan ağır sinema filmi gibi değil, her cümle/kelime ekranda anlık render oluyor gibi yüksek tempolu ve aktif akmalı. (`CLAUDE.md`'ye kalıcı kural olarak işlendi.)
- Yapılanlar (lokal):
  - **A-Sırt v1** (`kartlar/as_sirt_dovme.py` → `sirt_dovme_v1.png`, `sirt_dovme_r13.png`): Trapez/deltoid/omurga anatomisi, A-Y v3 uyumlu buzzcut + 5 katmanlı özgün tam sırt dövmesi (gotik kemer + ikiz origami turna + gizli `#7FE6FF` kat planı). **Görsel Kurul: 3/3 SON ÇIKTIYA UYGUN.** `karakter.py`'ye (`michael_sirt_dovme`) entegre edildi.
  - **Prolog F4b v3** (`blok/prolog_blok.py` → `prolog_kontakt_v3_960.png`, `prolog_blok_v3_960.mp4`, 16.7 sn): Canlı CAD lazer tarama, seri patlayan `01–04` düğümleri, `FOX RIVER` / `EZBERE` / `KİLİT · 94941` / `HARİTA` / `11 YAŞ` kinetik damgaları, yeni A-Sırt v1 entegrasyonu ve 5/5 anlamsal geçiş.
- Alt ajan doğrulaması (v3):
  - **A1+A2 (`hikaye-ve-sahne`):** **F4b AKIŞA UYGUN** (tüm önceki bulgular çözüldü, D1–D10 ve yüksek tempo doğrulandı).
  - **Görsel Kurul (`gorsel-kurul`):** **F4b UYGUN** (tüm R4, tipografi, R17 geçiş ve Türkçe font bulguları çözüldü).
- Ders: "Canlı kelime-kelime render" temposu (lazer tarama + seri 0.14–0.18 sn aralıklı düğüm patlamaları + kinetik damgalar + 0.55–0.70 sn keskin anlamsal geçişler) ağır sinematik hissi tamamen kırıp ekranda tutuculuğu dramatik biçimde artırıyor.
- Bekleyen karar: A-Sırt v1 ve Prolog F4b v3 kullanıcı onayı → onaylanırsa F4c/F4d Prolog tam yapım (veya Bölüm I örgüsü).

## Tur 14 · 26.11.2026 18:50–18:59 · Prolog v3.1 Saniye-Saniye MP4 Denetimi & 3 Cerrahi Düzeltme
- Yapılanlar (lokal): Gerçek render edilmiş `prolog_blok_v3_960.mp4`'den 1 fps 16 ardışık karelik film şeridi (`prolog_v3_filmstrip.png`) çıkarılıp hem **A1+A2** hem **Görsel Kurul** denetimine sokuldu.
- Yakalanan ve anında giderilen 3 kusur (t=10.5s–14.5s):
  1. `t=10.5s`: Siyah oval ayakkabı uçları → krem tabanlı, bağcıklı çocuk spor ayakkabısı + koyu kot paçası + temas gölgesi.
  2. `t=11.5s`: Yukarı tilt sırasında kapı ışığı ve `11 YAŞ` damgası temizce sönerek alt kadrajdan çıktı; çocuk gövdesi alt kenara tam oturdu.
  3. `t=12.5–14.5s`: P.05'teki sert beyaz şerit + siyah glitch kutusu kaldırıldı → onaylı `am_mekanlar_v1` yumuşak altın ışık huzmesi + yumuşak kenarlı yürüyen gölge + çakışmasız `03·TOZ`/`04·IŞIK` yerleşimi.
- Ders: Kontakt sayfası seçili 12 anı gösterir; ancak gerçek MP4'ten 1 fps ardışık şerit çıkarmak ara saniyelerdeki çakışmaları ve geçiş artefaktlarını (ör. `t=10.5s–12.5s`) kusursuz yakalar.
- Bekleyen karar: Temiz v3.1 Prolog F4b onayı → F4c Prolog son kalite + yerel sesli animatik veya Bölüm I örgüsü.

## Tur 15 · 26.11.2026 19:01–19:06 · Prolog F4b Kilitlendi + F4a Bölüm I ("Turna") Örgüsü & A1+A2 Denetimi
- Karar (Tur 14): Prolog F4b v3.1 **onaylı, kilitlendi**.
- Yapılanlar (lokal): Bölüm I ("Turna", #1–#8, 10 çekim, ~46.8 sn, 9/9 anlamsal geçiş) `dokum/bolum_1.json` ve `orgu/bolum_1_orgu.md` olarak yüksek tempolu canlı akış kuralıyla yazıldı.
- Denetim: `dokum_kontrol.py` **GEÇTİ** (0 hata, 0 uyarı) → **A1+A2 (`hikaye-ve-sahne`)** tüm 10 çekime **5/5 anlaşılırlık** ve tam dizi doğruluğu verdi; yakaladığı 2 nokta (`1.09→1.10` geçişinin `zoom_icinden` yapılması ve `1.09` öğe sırasının konuşma sırasına alınması) anında düzeltildi ve `dokum_kontrol.py` yeniden **GEÇTİ**.
- Ders: JSON dökümünde `kelime` alanı her zaman tek kelime kökü olarak yazılır (çok kelimeli ifadeler D1 eşleşmesinde düşer); geçiş bağları sonraki çekimin ilk anıyla çelişmeyecek şekilde A1+A2 denetimiyle doğrulanır.
- Bekleyen karar: Bölüm I ("Turna") örgüsü onayı → F4b Bölüm I blok animatiğine geçiş.

## Tur 16 · 26.11.2026 19:11–19:27 · F4b Bölüm I ("Turna") Blok Animatiği v2 + A1/A2 & Görsel Kurul Denetimi
- Yapılanlar (lokal): `blok/bolum1_blok.py` → `blok/bolum1_kontakt_960.png` (16 kare: 10 çekim + 6 kritik geçiş orta karesi) ve `blok/bolum1_blok_960.mp4` (960×540, 33.85 sn, 9/9 anlamsal geçiş) yüksek tempolu canlı akışla üretildi.
- Alt ajan denetimi (**A1+A2** + **Görsel Kurul**): Yakalanan 3 bulgu (`1.03` R7 aşırı karanlık, `1.04` A1 lore-dışı erken turna, `1.07` `18 YAŞ` alın çakışması + Lincoln omuz/tefeci silueti) anında v2'ye işlenip yeniden render edildi.
- Ders: Paylaşılan mekân modülleri (`am_mekanlar.py`) kronolojiye göre değişen motif nesneleri (ör. karanlık depo zeminindeki turna) içerdiğinde, erken sahnelerde yalnızca arka/orta katmanlar çağrılarak lore tutarlılığı korunur.
- Bekleyen karar: Bölüm I F4b v2 kullanıcı onayı → Bölüm II ("Haritayı giymek") F4a örgüsüne geçiş veya Prolog+Bölüm I yerel sesli animatik.

## Tur 17 · 26.11.2026 20:04–20:18 · Ham Video İngilizce Kararı + 3 Paralel Görsel Ajanla Bölüm I Yüksek Detay Setleri (V1, V2, V3)
- Kullanıcı kararları (20:04): (1) Ham video ve tüm ekran yazıları **İngilizce** üretilecek, yerelleştirme sonradan YouTube'da yapılacak; (2) Yalın/boş geometrik bloklar kesinlikle kaldırılacak, 3 görsel ajan çağrılarak yüksek görsel aktivite ve bütünlük sağlanacak. (`CLAUDE.md`'ye işlendi.)
- Yapılanlar (lokal): 3 paralel görsel ajan 9 sahneyi 5 katmanlı (`960×540`) yüksek detaylı İngilizce illüstrasyonlar olarak üretti:
  - **V1** (`b1_set_cocukluk.py` → `b1_set_cocukluk_v1.png`, `r13`): `1.01` Family Front Door (`SCOFIELD`), `1.02` Rainy Kitchen (`AGE 11` & `?`), `1.03` Juvenile Hall & Foster Closet Lock (`JUVENILE HALL` / `LOCKED`).
  - **V2** (`b1_set_turna.py` → `b1_set_turna_v1.png`, `r13`): `1.05` Morning Bedside (`I'M HERE` + Turna v4), `1.06` High School Craft Desk (`FOLD 01→03` + 5 Turna v4), `1.07` Night Diner (`$90,000` check + Lincoln v1 + sedan & 2 loan sharks).
  - **V3** (`b1_set_muhendis.py` → `b1_set_muhendis_v1.png`, `r13`): `1.08` Chicago Office (Loyola diploma + Willis/Hancock CAD), `1.09` Drafting Table (`FOX RIVER` blueprint + Turna v4), `1.10` `THE CHICAGO CHRONICLE · DEATH ROW` + Lincoln v1.
- Denetimler: **Görsel Kurul (`gorsel-kurul`)** her 3 sete de tüm alanlarda **3/3 (SON ÇIKTIYA UYGUN)** verdi; **A1+A2 (`hikaye-ve-sahne`)** ise **BÖLÜM I F4b ENTEGRASYONUNA HAZIR** onayı verdi.
- Ders: Ortak 5 katman mimarisi, sıcak-soğuk ışık kuralı ve kilitli F3 varlık çağrıları baştan brife bağlandığında 3 paralel görsel ajan tek elden çıkmış gibi bütünlüklü yüksek kaliteli sahne setleri üretebiliyor.
- Bekleyen karar: Bu 9 yüksek detaylı İngilizce sahne setini onaylayıp Bölüm I F4b v3 İngilizce animatiğine (ve ardından Prolog'u da İngilizceye) entegre edelim mi?

## Tur 18 · 26.11.2026 20:24–20:44 · Act I ("The Crane") F4b v3 EN (5 Katmanlı Paralaks + V1·V2·V3) Tamamlandı
- Yapılanlar (lokal): `blok/bolum1_blok_en.py` → `blok/bolum1_v3_en_kontakt_960.png` (16 kare) ve `blok/bolum1_v3_en_960.mp4` (960×540, 33.15 sn, 530 kare, 9/9 anlamsal geçiş) %100 İngilizce, 5 katmanlı paralaks (`uzak/orta/sahne/plan/onplan`) ve kelimeye kilitli canlı CAD lazer taramalarıyla üretildi.
- Denetimler:
  - **A1+A2 (`hikaye-ve-sahne`):** **F4b v3 EN AKIŞA UYGUN** (önceki tüm bulgular çözüldü, 9/9 geçiş ve İngilizce senkron tam puan).
  - **Görsel Kurul (`gorsel-kurul`):** **F4b v3 EN UYGUN** (R1–R17 tamamen temiz; yalnızca F4c için ufak not: `1.07` çeki alt altyazı bandından ~10–15 px yukarı çekilebilir).
- Ders: Onaylı 5 katmanlı SVG setlerini doğrudan önbellekli `svg_sprite` olarak ayrı `Oge` derinlik katmanlarına ayırmak ve `plan` katmanını canlı CAD taramasıyla açmak, hem tam illüstrasyon kalitesi hem gerçek 2,5D paralaks hareketi sağlıyor.
- Bekleyen karar: Act I F4b v3 EN kullanıcı onayı → Prolog'un İngilizce+zengin görsel uyarlaması mı, yoksa Act II ("Wearing the Map") örgüsü + 3 görsel ajan setleri mi?

## Tur 19 · 26.11.2026 21:03–21:17 · Act I 1.04 Düzeltmesi + Prolog EN + Act II ("Wearing the Map") 7 Yüksek Detaylı Set (V4·V5·V6)
- Karar (Tur 18): Act I F4b v3 EN **onaylı, kilitlendi** (`1.04` çocuk gövdesi karartısı gerçek çizgili kazaklı kilitli 11 yaş Michael v3 figürüne geçirildi).
- Yapılanlar (lokal):
  - **Prolog EN:** `blok/prolog_blok_en.py` → `blok/prolog_en_kontakt_960.png` (%100 İngilizce yazılar + P.04 gerçek çizgili kazaklı 11 yaş figürü).
  - **Act II ("Wearing the Map") F4a:** `dokum/bolum_2_en.json` + `orgu/bolum_2_en_orgu.md` (7 çekim, ~33 sn, 6/6 anlamsal geçiş) → `dokum_kontrol.py` **GEÇTİ** + **A1+A2** **ACT II F4a ONAYLI** (A1 lore düzeltmesiyle `28 → 30 gün` / `EXECUTION IN 30 DAYS` hizalandı).
  - **3 Paralel Görsel Ajan (V4, V5, V6):** 7 yüksek detaylı 5 katmanlı İngilizce sahne seti (`b2_set_mahkeme_v1.png`, `b2_set_plan_dovme_v1.png`, `b2_set_banka_kapi_v1.png` + R13 kırpmaları) üretildi.
- Denetim: **Görsel Kurul (`gorsel-kurul`)** her 3 sete de tüm alanlarda **3/3 (SON ÇIKTIYA UYGUN)** verdi (Act I ile tam stil bütünlüğü, kronolojik dövme sürekliliği kusursuz).
- Ders: Kronolojik süreklilik (1.10 `MAY 11` ↔ 2.07 `EXECUTION IN 30 DAYS`; 2.02 dövmesiz → 2.04 dövme yapımı → 2.07 ışıklı önkol) A1+A2 ve Görsel Kurul çapraz kontrolüyle hatasız kilitleniyor.
- Bekleyen karar: Prolog EN + Act II 7 yüksek detaylı set onayı → Act II F4b 5 katmanlı İngilizce blok animatiğine (MP4) geçiş.

## Tur 20 · 26.11.2026 21:27–21:42 · Act II ("Wearing the Map") F4b EN (5 Katmanlı Paralaks + V4·V5·V6) Tamamlandı
- Yapılanlar (lokal): `blok/bolum2_blok_en.py` → `blok/bolum2_en_kontakt_960.png` (12 kare) ve `blok/bolum2_en_960.mp4` (960×540, 25.55 sn, 409 kare, 6/6 anlamsal geçiş) %100 İngilizce, 5 katmanlı paralaks ve canlı CAD taramalarıyla üretildi.
- Denetimler:
  - **A1+A2 (`hikaye-ve-sahne`):** **ACT II F4b EN AKIŞA UYGUN** (`DATE: APR 11` + `30 DAYS` lore uyumu ve 6/6 geçiş tam puan).
  - **Görsel Kurul (`gorsel-kurul`):** **ACT II F4b EN UYGUN** (R1–R17 tamamen temiz; F4c için ufak not: `2.07` `EXECUTION IN 30 DAYS` kutusu zoom'da ~15 px sola, `2.01` `GUILTY?` etiketi hafif sağa alınacak).
- Ders: 5 katmanlı setlerle `Eslesme` (duvar planı → A-Sırt dövmesi) ve `Maske` (kırmızı damga → Fox River kapıları) geçişleri 25 saniyelik bir bölümde bile çok yüksek sinematik etki ve akıcılık yaratıyor.
- Bekleyen karar: Act II F4b EN kullanıcı onayı → Act III ("Fox River") İngilizce örgüsü + 3 görsel ajan setlerine geçiş mi, yoksa Prolog + Act I + Act II'yi birleştirip ilk İngilizce yerel sesli önizleme mi?

### Tur 21 — Birleşik Prolog+Act I+Act II Çift Denetim & Act III ("Fox River") 10 Sahne Seti (V7·V8·V9)
- **V-Prolog + R4-PARALAKS Birleşimi:** Yükseltilmiş `prolog_en_960.mp4` (`set_p01_fox_river_gece` ikiz kule/projektör/yağmur/CAD X-ray + `set_p04_depo_zemin`), R4-PARALAKS düzeltmeli `bolum1_v3_en_960.mp4` ve `bolum2_en_960.mp4` tek 75.4 sn videoda birleştirildi: `blok/prolog_act1_act2_en_960.mp4` + 16 karelik denetim şeridi `blok/birlesik_denetim_960.png`.
- **Birleşik Çapraz Denetim:** Hem **Görsel Kurul (G)** (`BİRLEŞİK PROLOG+ACT I+ACT II KURUL ONAYLI`, 16/16 R4-temiz) hem **A1+A2** (`BİRLEŞİK PROLOG+ACT I+ACT II A1+A2 ONAYLI`) onayladı.
- **Act III ("Fox River") F4a + 3 Paralel Görsel Sanatçı (V7·V8·V9):**
  - `dokum/bolum_3_en.json` + `orgu/bolum_3_en_orgu.md` (10 çekim, 9/9 anlamsal geçiş, `dokum_kontrol.py` 0 hata, A1+A2 onaylı).
  - **V7 (`3.01–3.03`):** `kartlar/b3_set_ziyaret_revir.py` → `b3_set_ziyaret_revir_v1.png` + `r13.png` (ilk turda Kurul ONAYLI).
  - **V8 (`3.04–3.06`):** `kartlar/b3_set_duvar_idam.py` → `b3_set_duvar_idam_v1.png` + `r13.png` (Kurul geri bildirimi üzerine `3.05` Michael kol/gövde anatomisi yumuşatıldı → Kurul ONAYLI).
  - **V9 (`3.07–3.10`):** `kartlar/b3_set_yanik_kacis.py` → `b3_set_yanik_kacis_v1.png` + `r13.png` (Kurul R8 yakalaması üzerine `3.10` FBI kanıt fotoğrafına kilitli A-Sırt v1 gömüldü → Kurul ONAYLI).
- **Çapraz Denetim Sonucu:** Act III 10/10 sahne hem **Görsel Kurul (G)** (`ACT III SETLERİ 3/3 ONAYLI`) hem **A1+A2** (`ACT III SETLERİ A1+A2 ONAYLI`) çift onaylı.
- **Bekleyen karar:** Birleşik `Prolog + Act I + Act II` + Act III set kartları kullanıcı onayı → **Act III F4b EN 5-katman blok animatiği** (`blok/bolum3_blok_en.py`).

### Tur 22 — R4-ANATOMİ Kalıcı Düzeltmesi & Act III ("Fox River") F4b EN Blok Animatiği (43.60 sn)
- **R4-ANATOMİ Kuralı & 4 Paralel Sanatçı Düzeltmesi:** Kullanıcının `2.01` ve `2.02` ekran görüntülerinde yakaladığı yaka-üstü-boyun, kubbe omuz ve kopuk kol hataları için `kurul/DERSLER.md`'ye kalıcı **R4-ANATOMİ** kuralı eklendi; **V4 (`2.01–2.02`)**, **V2 (`1.07`)**, **V6 (`2.05`)**, **V7 (`3.01–3.03`)** düzeltilip Görsel Kurul `R4-ANATOMİ 4/4 TEMİZ` onayını aldı; birleşik `prolog_act1_act2_en_960.mp4` yeniden render edilip kullanıcı tarafından onaylandı.
- **Act III ("Fox River") F4b EN (`blok/bolum3_blok_en.py`):** 10 çekim (`3.01–3.10`), 43.60 sn, 9/9 anlamsal geçiş, R4-PARALAKS + R4-ANATOMİ kilitli 5-katman blok animatiği kuruldu.
- **Çapraz Denetim & Anlık Düzeltme:** İlk kontakt denetiminde hem **Görsel Kurul (G)** hem **A1+A2** 7 sahnedeki tekrarlı kinetik damgaları ve `3.01 / 3.06 / 3.08` sağ üst HUD kenar kırpılmasını yakaladı → çift damgalar temizlendi, kamera zoom'u güvenli kadraja çekildi → yeniden render edildi:
  - `blok/bolum3_en_kontakt_960.png` (12 kare)
  - `blok/bolum3_en_960.mp4` (43.60 sn, 960×540 @ 16fps)
  - Son karar: **Görsel Kurul (`ACT III F4b EN KURUL ONAYLI`)** + **A1+A2 (`ACT III F4b EN A1+A2 ONAYLI`)**.
- **Bekleyen karar:** Act III F4b EN kullanıcı onayı → kilitle ve **Act IV ("On the Run")** F4a EN örgüsü + 3 paralel görsel ajan setlerine geçiş.

### Tur 23 — R18-HAREKET Kalıcı Standardı, Act III F4b v2 EN (Gerçek Sahne İçi Hareket) & GitHub Senkronizasyonu
- **Kalıcı Kurallar (`kurul/DERSLER.md` + `CLAUDE.md`):** `R18-HAREKET` (slayt gösterisi yasak — hareketli nesneler ayrı katmanda fiziksel hareket eder, ışık/atmosfer eyleme tepki verir, sıfır kutu taşması, iki kol tam) ve `R4-AYIRT EDİCİLİK` kalıcı olarak işlendi.
- **Michael v3 (`kartlar/ay_yetiskin.py`):** Yüz konturu ~%8 inceltilerek Lincoln'dan ilk bakışta ayrışması sağlandı; önkol dövmesi (`dovme_onkol_yetiskin`) A-Sırt v1 kalitesinde gotik telkari/gölgeli forma yükseltildi.
- **Act III Set Revizyonları (V7·V8·V9):**
  - **V7 (`3.01–3.02`):** `3.01` göğüs/önkol dövmesi gotik telkariye yükseltildi; `3.02` John Abruzzi, Fernando Sucre ve Charles Westmoreland stilize 2D karakter tanınırlığı güçlendirildi.
  - **V8 (`3.04–3.06`):** `3.04` ayrılabilir `duvar_oyuk / tuvalet / civata` katmanları; `3.05` ince Michael + Collar-Over-Neck + Sara'nın iki kolu da eksiksiz; `3.06` ayrılabilir `salter_kol` + `telefon_ahize` katmanları.
  - **V9 (`3.08–3.10`):** `3.08` `DOOR UNLOCKED · TONIGHT` sıfır kutu taşması + `kapi_isik`; `3.09` ayrılabilir `kacanlar / projektor_1 / projektor_2 / alarm`; `3.10` ayrılabilir `ucak / kosucular / fbi_kutu` + ıslak pist atmosferi.
- **Act III F4b v2 EN (`blok/bolum3_blok_en.py` · 43.60 sn):** Tüm hareketli katmanlar fiziksel sahne içi eylemle canlandırıldı → **Görsel Kurul (`ACT III F4b v2 EN KURUL ONAYLI`)** & **A1+A2 (`ACT III F4b v2 EN A1+A2 ONAYLI`)**.
- **GitHub Senkronizasyonu:** Kullanıcının yeni talimatıyla tüm değişiklikler, iş planları, kurallar, setler ve animatikler GitHub'a commit & push ediliyor.

### Tur 24 — Act III Kilitlendi & Act IV ("On the Run") F4a EN + 3 Paralel R18-HAREKET Seti (V10·V11·V12)
- **Act III F4b v2 EN:** Kullanıcı onayıyla kilitlendi.
- **Act IV ("On the Run") F4a EN:** `dokum/bolum_4_en.json` + `orgu/bolum_4_en_orgu.md` (8 çekim `4.01–4.08`, ~38.4 sn, 7/7 anlamsal geçiş, `dokum_kontrol.py` GEÇTİ, A1+A2 `ACT IV F4a ONAYLI`).
- **3 Paralel R18-HAREKET Görsel Sanatçısı (İlk Turda Sıfır Hata · 3/3 Kurul + A1+A2 Çift Onaylı):**
  - **V10 (`4.01–4.03`):** `kartlar/b4_set_takip_turna.py` → `v1.png` + `r13.png` (Mahone FBI masası + A-Sırt v1 + `kirmizi_ip/harita_igne`, otoyol + uçan `kart_1/2/3` `MICHAEL CRANE`, Sara'nın çantasında açılan Turna v4 `turna_kapali/turna_acik`).
  - **V11 (`4.04–4.06`):** `kartlar/b4_set_bulusma_manset.py` → `v1.png` + `r13.png` (Motel buluşması Michael v3 + Sara v2 2 tam kol + kansız `bandaj_sar`, şiddetsiz baba saati `06:14` `(480,310)`, `STEADMAN ALIVE!` + silinen `af_imza` + `PARDON REVOKED`).
  - **V12 (`4.07–4.08`):** `kartlar/b4_set_panama_sona.py` → `v1.png` + `r13.png` (Panama `CHRISTINA ROSE` teknesi + `tuzak_halka`, Sona kavurucu çöl + kilitli Michael v3 + çarparak kapanan `kapi_sol/kapi_sag` + Act V `NO GUARDS INSIDE`).
- **GitHub:** Act IV F4a + V10·V11·V12 setleri ve güncel günlükler `origin/main`'e commit & push edildi.
- **Bekleyen karar:** Act IV setlerinin kullanıcı onayı → **Act IV F4b EN canlı-hareketli blok animatiği** (`blok/bolum4_blok_en.py`).

### Tur 25 — Act IV ("On the Run") `4.01` 5 Parmaklı El Revizyonu & F4b EN Canlı-Hareketli Blok Animatiği (35.00 sn)
- **V10 (`4.01`) Kullanıcı Revizyonu:** `harita_igne` FBI eli zarif, anatomik 5 parmaklı sinematik 2D insan eli olarak yeniden çizildi ve R13 #2'de doğrulandı.
- **Act IV ("On the Run") F4b EN (`blok/bolum4_blok_en.py` · 35.00 sn):** 8 çekim (`4.01–4.08`), 7/7 anlamsal geçiş, tüm sahnelerde gerçek R18-HAREKET sahne içi eylem (`4.01` gerilen kırmızı ipler + hamle yapan FBI eli, `4.02` 3 uçan sahte kimlik, `4.03` açılan Turna v4 → `GILA NM` şifresi, `4.04` canlı sarılan kansız bandaj, `4.05` eriyen baba silueti + düşen `06:14` cep saati, `4.06` dönen `STEADMAN ALIVE!` + silinen af imzası + çarpan `PARDON REVOKED`, `4.07` dalgada sallanan `CHRISTINA ROSE` + kapanan Şirket tuzağı, `4.08` çarparak kapanan paslı Sona kapıları + 4px yarık).
- **Çapraz Denetim & Anlık Düzeltme:** Kurul ve A1+A2 `4.02`, `4.03b`, `4.07`, `4.08b` sağ-alt HUD kutularının alt altyazı bandıyla çakıştığını yakaladı → `plan` katmanları yukarı çekilip yeniden render edildi → **Görsel Kurul (`ACT IV F4b EN KURUL ONAYLI`)** + **A1+A2 (`ACT IV F4b EN A1+A2 ONAYLI`)**.
- **GitHub:** Tüm Act IV F4b EN çıktıları (`bolum4_blok_en.py`, `bolum4_en_kontakt_960.png`, güncel V10 kartları ve günlükler) `origin/main`'e commit & push edildi.
- **Bekleyen karar:** Act IV F4b EN kullanıcı onayı → kilitle ve **Act V ("Sona & Scylla")** F4a EN örgüsü + 3 paralel R18-HAREKET görsel ajan setlerine geçiş.

### Tur 26 — R19-CANLI-DÜNYA Kalıcı Standardı & Act IV F4b v2 EN Dinamik Karakter Anlatımı (35.00 sn)
- **Kalıcı Kural (`kurul/DERSLER.md` + `CLAUDE.md`):** `R19-CANLI-DÜNYA` (donuk manken yasak, her 1,2–1,5 sn'de bir görsel vuruş, ses kapalıyken bile ekrandan okunan hikâye, 2 aşamalı dinamik kamera koreografisi) eklendi.
- **Act IV F4b v2 EN (`blok/bolum4_blok_en.py` · 35.00 sn):** Tüm 8 çekim çoklu görsel vuruş, canlı karakter hareketi (nefes alan/eğilen Michael & Sara, Sona'ya yürüyen Michael), yaşayan çevre (akan 3B yol şeritleri, çalışan silecek, tarayan polis projektörü, gölge dalgası, seken `06:14` saat, dumanla silinen imza) ve 2 aşamalı dinamik kamerayla yenilendi → **Görsel Kurul (`ACT IV F4b v2 EN KURUL ONAYLI`)** + **A1+A2 (`ACT IV F4b v2 EN A1+A2 ONAYLI`)**.
- **GitHub:** `R19-CANLI-DÜNYA` kuralları ve Act IV F4b v2 EN çıktıları `origin/main`'e commit & push edildi.
- **Bekleyen karar:** Act IV F4b v2 EN kullanıcı onayı → kilitle ve **Act V ("Sona & Scylla")** aşamasına geçiş.
