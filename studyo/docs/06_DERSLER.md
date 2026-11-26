# Ragnar projesinden kalıcı dersler

Kaynak: `ragnar_kaynak/karar_gunlugu_ragnar.md` (48 tur), `ragnar_kaynak/DERSLER.md` (kurul). Yeni projede her oturumun başında bu dosya okunur.

## 1. Kullanıcı tercihleri
- **Dinamik anlatım (26.11.2026, en güncel):** Her cümle ekranda yaşanır, sahneler anlamsal geçişlerle akar, duygu görsel öğelerle taşınır → `02_DINAMIK_ANLATIM.md`, `03_DUYGU_DILI.md`.
- **"Vasat tasarımlar kabul edilemez."** Ara kare, insert ve geçiş karesi dahil her kare onaydan geçer.
- **Önce örgü:** Görsel üretimden önce cümle cümle örgü ve süre sunulur.
- **Anlatım açıklayıcı ve net olmalı:** Hiç izlememiş biri anlamalı. Kim, nerede, neden; kavram ilk geçtiğinde açıklanır.
- **Sözlü kancalar zayıf:** "Aklında tut" türü sinyal cümleleri sevilmedi. Ekim, görüntü ve motifle yapılır.
- **Mekânlar dolu ama abartısız**, nesne ve dokuca zengin.
- **İhtişam:** Ordular kalabalık ve çeşitli, törenler süslü, kahraman nesneleri görkemli. Siluet ve gölge yerine gerçek model kullanılır.
- **Sert iklim tonu:** Sevimli ya da çizgi film görünümlü hayvan ve nesne kullanılmaz.
- **Kadın savaşçı** "kadın = küçük" varsayımıyla çizilmez. Rol fiziği belirler.
- **Nesneler zemine oturur:** Kazık toprağa girer, ağaç kökle oturur, yapıştırılmış görünmez.
- **Ses:** Konuşma her zaman net. Müzik ve efekt sesi bastırmaz. Viking teması gibi döneme uygun müzik istenir. Ambiyans yetersiz kalmamalı.
- **Kullanıcı küçük karedeki belirsiz öğeyi kendi yorumuyla okuyabilir.** Yorum güçlüyse benimsenir.
- **Kullanıcının önceki açık istekleri**, öneriler çelişse bile seçenek olarak sunulur.
- **Karar verici ajan** kullanıcıya sorulmadan "onay" veremez. Görsel yeterliliği kullanıcı belirler.

## 2. Değişmez sınırlar
- Oyuncuya benzeyen yüz çizilmez. Dizideki imza karakter tasarımı birebir kopyalanmaz. Kimlik; isim kartı, aksesuar, yara izi, renk, silah ve hikâye nesneleriyle taşınır. Kullanıcı ısrar etse bile yalnızca kopya kısmı reddedilir, genel öğelere izin verilir.
- Dizinin müziği, ekran görüntüsü ve gerçek kişi fotoğrafı kullanılmaz.
- Kan ve vahşet gösterilmez. Hassas sahnelerde intihar yöntemi gösterilmez. Yılan gibi ürkütücü öğeler gölgeyle verilir.
- API anahtarları yalnızca `/home/claude/.secrets/` altında durur (chmod 600). Repoya, loga ve commit'e girmez. İş bitince kullanıcıya iptal etmesi hatırlatılır.

## 3. Hikâye ve anlatım
- Bir kare en fazla 1–2 cümle taşır. Her yeni bilgi yeni bir görüntüyle gelir: harita, insert, isim kartı.
- Telaffuzu zor özel isimler anlatımda genel adla, ekranda özel adla verilir (TTS için fonetik yazım).
- Diziye sadakat: olaylar sezon ve bölümle doğrulanır. Sanatsal eklemeler (ölümdeki kuzgunlar gibi) açıkça işaretlenir.
- Mizah yalnızca hafif bölümlerde kullanılır. Trajik vuruşlarda espri yoktur.
- Ajan denetimi satırları numara sırasıyla okuyabilir. Mantık bulguları her zaman animatik PLAN sırasına göre doğrulanır.

## 4. Görsel üretim
- **Hız kaliteyi sessizce yer.** Kısa yol, en pahalı revizyonu doğurur.
- **Brif netliği ajan sayısından önemlidir.** Kare başına 6–12 somut ayrıntı listesi + referans kare kıyası.
- **Kimlik öğesi tek kaynaktan** çağrılır (dövme, yara, broş, halka). Türetilen karakterde ana karakterin kimlik bayrakları açıkça kapatılır.
- Asimetrik kimlikli kafa `scale(-1)` ile çevrilmez.
- Yüz çizgileri yalnız çıplak cilt bölgesine düşer. Kaşlar en son katmandır.
- Malzeme önce değer yapısıyla (öz, orta, specular) ve geometriyle kurulur, gürültü dokusu en son eklenir.
- Nesne kartı nötr pozda değil, **sahnedeki eylem pozunda ve etkileşim kompozitinde** değerlendirilir.
- Bebek ve çocuk için ayrı oran tablosu: en geniş yer yanak, kısa kol, parmak avucun ön yüzünde.
- Sıra dağ kadrajın içinde bitiyorsa etekle başlar.
- Doğal nesneler (ağaç, kaya) düzensiz doku ve konik dallanmayla çizilir; kalıp segmentler tahta şerit gibi durur.
- Bir eylemi anlatan karede eylemin iki ucu da görünür: kimden kaçılıyor, kime yetişiliyor.
- Tanrı ve efsane figürleri ölçek ve kompozisyonla büyütülür (minik dünya, alt açı, ışık).
- Küçük boyutta (168 px) gözleri kapalı gülüş öfke gibi okunur.

## 5. Teknik
- Kare kare render edilen sprite'ın içeriği zamandan bağımsız olmalı. Hareket transform ile verilir. (Yeni motorda öğelerin `ciz` fonksiyonu t alabilir, ama sprite önbelleği SVG içeriğine göre anahtarlandığı için zamanla değişen SVG her karede yeni PNG üretir. Zamanla değişen şeyler skia ile çizilir ya da transform ile verilir.)
- Ham karelerin PNG'sinde alfa olabilir. Animatikte RGB'ye düzleştirilir.
- Import sırasında dosya yazan modüller paralel render'da çakışır. Bu betikler aynı anda çalıştırılmaz.
- Betiğe takma adla modül eklerken var olan adlar kontrol edilir (`YAS` çakışması).
- Efekt koordinatları kareden **ölçülür**, kontakt sayfasından tahmin edilmez. Alevi sarı-beyaz çekirdek belirler, rim ışığı alev değildir.
- Kontakt sayfası skia ile okunurken BGRA/RGBA sırası kontrol edilir.
- Yardımcı betikler dosya sayarak satır sayısı çıkarmaz (yalnız `.wav`).
- Kuzgunlar üstten görünüşle ve uçuş yönüne dönük çizilir.

## 6. Ses
- Her cümle ayrı üretilir. Kelime zamanları Whisper `word_timestamps` ile alınır, görsel olaylar bunlara kilitlenir.
- Geniş bantlı efektler (gök gürültüsü, fırtına) satır aralarına konur ve konuşma altında kısılır. Ragnar'da bir satır fırtına altında yanlış duyuldu.
- Miks sonrası Whisper anlaşılabilirlik testi zorunludur.
- ElevenLabs: TTS ve SFX için anahtar 1, müzik izni olan anahtar 2. Music API'de aynı anda en fazla 2 istek.
- Müzik vokalsiz olmalı. Whisper'ın müzikte "konuşma" bulması halüsinasyondur, ama yine de dinlenir.

## 7. Süreç ve maliyet
- Bir kurul turu (3 ajan) yaklaşık 750 bin token harcadı. Tek ajan + kontakt sayfası aynı kaliteyi verdi.
- Uzun bağlam pahalıdır. Her bölüm sonunda `OTURUM_DEVRI.md` güncellenir ve gerekirse yeni oturuma geçilir.
- Yayın sonrası yerelleştirme: 8 dil SRT + çevrilmiş başlık/açıklama + dil başına kapak. Dublaj isteğe bağlıdır (yaklaşık 85 bin kredi).
