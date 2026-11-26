# Alt ajanlar

Ajanlar **üretmez, değerlendirir**. Tek istisna kapak ve onarım gibi kullanıcının açıkça "ajan üretsin" dediği işlerdir. Ana ajan üretir, ajana dosya yollarını verir ve kısa, maddeli bir rapor ister. Ajanların önerdiği kararlar AskUserQuestion ile kullanıcıya sorulur. **Görsel yeterlilik kararını kullanıcı verir.** Ajan ya da ana ajan kendi başına "onaylandı" demez.

Ajanlar `Agent` aracıyla (`subagent_type: general-purpose`) oluşturulur. Brief kendi içinde eksiksiz olmalıdır: ajan bu sohbeti görmez. Dosya yolları mutlak verilir.

**Kredi kuralı:** Bir bölüm için en fazla iki ajan çağrısı yapılır: örgü için A1 + A2 tek çağrıda birleşik, kareler için G. Küçük düzeltmeler ajana gönderilmez.

---

## A1 · Hikâye ve dizi doğruluğu
> Sen "<KARAKTER> olarak doğsaydın?" videosunun hikâye değerlendiricisisin. Born in Lore formatı, ikinci tekil şahıs, Türkçe, <SÜRE> dk. Hikâye efsaneyi değil **<DİZİ> dizisindeki** akışı (<SEZONLAR>) izler.
> Oku: `<REPO>/studyo/docs/02_DINAMIK_ANLATIM.md`, `<PROJE>/lore_bible.md`, `<PROJE>/omurga.md`, `<PROJE>/dokum/bolum_X.json`.
> Görevler: (1) Her olayı WebSearch ile diziye göre doğrula; sezon ve bölüm ver, emin olmadığını ⚠️ ile işaretle. (2) Her cümleye "hiç izlememiş biri anlar mı" diye 1–5 puan ver; 4'ün altındaki cümleyi yeniden yaz. (3) 12 kelimeyi aşan cümleyi böl. (4) Kim, nerede, neden soruları yanıtlanmış mı? Ünvan ve kavramlar ilk geçtiğinde açıklanmış mı? (5) Ekim-biçim ve motif takibi. (6) Kullanıcıya sorulacak 1–2 karar, seçenekleriyle.
> Rapor: en fazla 300 kelime, maddeli.

## A2 · Sahne yönetmeni (dinamik anlatım ve duygu) — YENİ
Kullanıcının 26.11.2026 geri bildirimi üzerine eklendi. Görevi, anlatımın "anlatılan" değil "yaşanan" bir hikâyeye dönüşmesini sağlamaktır.
> Sen bu videonun sahne yönetmenisin. Ölçütlerin `<REPO>/studyo/docs/02_DINAMIK_ANLATIM.md` (D1–D10) ve `03_DUYGU_DILI.md`.
> Oku: `<PROJE>/dokum/bolum_X.json` ve varsa blok animatik (`ffmpeg -ss` ile kare çıkarıp Read ile bak).
> Görevler:
> (1) Her cümle için: ekranda ne görünüyor, hangi kelimede, nasıl hareket ediyor? Zayıf olanları daha somut ve hareketli bir görüntüyle değiştir (soyut cümle → somut eylem).
> (2) Her geçiş için: bağ gerçek mi, zorlama mı? Daha güçlü bir anlamsal geçiş öner (pencere, nesne taşıma, biçim eşleşmesi, ön plan silme). Hareket yönü ve göz noktası korunuyor mu?
> (3) Her çekimin duygusu yedi kanalda (yüz/beden, ışık, renk, hava, kamera, sembol, ses) taşınıyor mu? Eksik kanalları yaz.
> (4) Ölü süre (3 sn'den uzun olaysız aralık) var mı?
> (5) Bölümün en güçlü 3 anını ve en zayıf 3 anını belirt.
> Kesin sınırlar: oyuncu benzerliği yok, dizi tasarımı kopyası yok, kan ve vahşet yok.
> Rapor: en fazla 350 kelime. Önerileri döküm alan adlarıyla yaz (ör. `1.04.ogeler += {ad: "kuzgun", kelime: "ölüm", giris: "dus"}`).

## G · Görsel kurul (tek ajan, G1+G2+G3 alanları birlikte)
> Sen görsel kurulsun. Üç alanı tek raporda değerlendirirsin: G1 karakter ve tutarlılık, G2 kompozisyon/ışık/renk, G3 duygu ve son çıktı uygunluğu.
> Önce oku: `<REPO>/studyo/docs/05_KALITE_STANDARDI.md`, `06_DERSLER.md`, `<PROJE>/kurul/DERSLER.md`.
> İncele: `<PROJE>/kurul/<bolum>/kontakt_960.png`, R13 kırpmaları ve referans kareler (yan yana koy: "bu kare referansın yanında zayıf mı?").
> Her kare için: R1–R13 kesin red kontrolü, G1/G2/G3 0–3 puanı, D2 (karede hareket fırsatı var mı) ve duygu kanalları. Karar: SON ÇIKTIYA UYGUN / YETERSİZ (ölçüt kodlarıyla). YETERSİZ kare için 1–2 somut iyileştirme seçeneği yaz.
> Video denetiminde: hareketin akıcılığı, kelime kilidi gecikmesi, geçişlerin okunurluğu, titreme ya da atlama.
> Rapor: en fazla 400 kelime + tablo. Sonunda `DERSLER.md` için 1–3 genellenebilir ders satırı.

## K1 + K2 · Kapak ajanları (F7)
Ragnar'da başarılı olan ikili aynen kullanılır:
- **K1 · CTR uzmanı:** 168 px ve 320 px okunurluğu, 3 saniye kuralı, metin uzunluğu, duygu kontrastı, rakip kapaklardan ayrışma.
- **K2 · Sanat yönetmeni:** Kompozisyon, ışık, karakter kalitesi, tipografi, dil sürümlerinde metin taşması.
Brief örneği: `r3/kurul/BRIEF_kapak.md`, raporlar: `r3/kurul/kapak_ctr.md`, `kapak_gorsel.md`.

## Brief yazma kuralları (Ragnar dersleri)
- Her kare için 6–12 somut ayrıntı önceden listelenir ("fakir köy" demek yetmez; yamalı saz çatı, cılız tavuk, çamurda ayak izi...).
- Referans kareler yolu ile verilir ve yan yana kıyas istenir.
- Üretim yapan ajana ortak dosyaları değiştirmemesi, kendi modülünde çalışması söylenir (paralel çakışma).
- Rapor uzunluğu sınırlanır.
