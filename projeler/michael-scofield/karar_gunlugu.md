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
