# İş planı: yeni karakter videosu

Biçim: Born in Lore ("X olarak doğsaydın?"), ikinci tekil şahıs, Türkçe, 8–10 dk, 2D animasyon. Kişisel, ticari değil.
Ragnar'dan farkı: **dinamik anlatım** (`02_DINAMIK_ANLATIM.md`) ve **duygu dili** (`03_DUYGU_DILI.md`) baştan zorunlu. Kalite çıtası Ragnar'ın son hâlidir (`05_KALITE_STANDARDI.md`).

## Değişmeyen çalışma kuralları (kullanıcının Ragnar'da koyduğu kurallar, aynen geçerli)
1. **Önce örgü:** Görsel üretimden önce her bölümün örgüsü kullanıcıya gider: cümle cümle görüntü, kilit kelime, hareket, geçiş, duygu ve süre. Kullanıcı düzeltir ya da onaylar.
2. **Katı denetim:** Hiçbir yeni kare kullanıcı onayı olmadan animatiğe, sese ya da videoya girmez. Bu kural ek görüntüler (insert) ve geçiş kareleri için de geçerlidir. Sıra: üreten ajanın öz değerlendirmesi (en az 2 tur, R13 kırpması dahil) → bağımsız kurul → kullanıcı.
3. **Ses ve video onaydan sonra** üretilir.
4. **Nakış gibi:** Bölüm bölüm ilerlenir. Takılınan yerde AskUserQuestion ile seçenekli soru sorulur, önerilen seçenek ilk sıradadır, kullanıcının önceki açık istekleri her zaman bir seçenek olarak sunulur.
5. **Kredi tasarrufu:** Kurul sahne başına tek ajanla ve tek kontakt sayfasıyla toplanır. Ara kontroller 960 px'de yapılır. Kullanıcıya sahne başına bir sunum gider.
6. **Her tur sonunda** `karar_gunlugu.md` dosyasına bir tur kaydı ve **Ders** satırı eklenir. Kalıcı dersler `studyo/docs/06_DERSLER.md`'ye taşınır.
7. Commit ve push her anlamlı adımda `main` dalına yapılır. Gizli anahtarlar asla repoya girmez.

---

## Aşamalar ve kapılar

### F0 · Başlangıç (1 oturum)
- Kullanıcıya tek AskUserQuestion: karakter ve dizi, kapsam (sezonlar), hedef süre, anlatıcı sesi (varsayılan ElevenLabs "George", Türkçe), altyazı ve dublaj dilleri.
- `projeler/<slug>/` klasörü `sablonlar/proje_iskeleti.md`'ye göre kurulur. `CLAUDE.md` şablondan doldurulur.
- **Kapı:** Kullanıcı kapsamı onaylar.

### F1 · Araştırma → `lore_bible.md`
- Hikâye ajanı (A1) diziyi sezon ve bölüm bazında tarar. Her olayın kaynağı yazılır, emin olunmayan yer ⚠️ ile işaretlenir.
- Karakterin **görsel kimlik kataloğu** çıkarılır: kostüm, renk, silah, aksesuar, mekânlar. Oyuncu yüzü ya da imza tasarım kopyalanmaz (`06_DERSLER §Sınırlar`).
- **Kapı:** Yok. Sonuç F2 ile birlikte sunulur.

### F2 · Omurga, bölümler, motifler → `omurga.md` + plan artifact'ı
- Tek cümlelik tema, duygusal çapa, 6 bölüm + prolog, bölüm süreleri.
- **Ekim-biçim defteri** (3–5 ekim) ve **görsel motif listesi**. Motif, bölümleri bağlayan ve geçişlerde taşınan nesne ya da biçimdir (Ragnar'da kol halkası, haç, kuzgun). Her motifin hangi geçişlerde kullanılacağı yazılır.
- **Duygu eğrisi:** Bölüm bölüm duygu grafiği (huzur → merak → zafer → ... → yas). Renk planı bu eğriden çıkar.
- **Kapı:** Kullanıcı omurgayı onaylar ya da düzeltir.

### F3 · Model ve mekân kartları
- Ana karakterler (yaş evreleriyle), kimlik nesneleri, ana mekân setleri (her mekânda ≥ 3 kimlik öğesi).
- Karakterler motorun SVG sprite sistemiyle çizilir (Ragnar'daki `art3` yaklaşımı). Bu kez **eklemli** hazırlanırlar: baş, gövde, kollar, el ve ağız/göz ayrı katmanlardadır, böylece D2 karakter eylemleri yapılabilir (`07_TEKNIK_HAT §2`).
- Öz değerlendirme → kurul (G-tek) → kullanıcı.
- **Kapı:** Kullanıcı model ve mekân kartlarını onaylar.

### F4 · Bölüm döngüsü (her bölüm için tekrar)
**F4a · Örgü ve sahne dökümü**
- Anlatım metni + `dokum/bolum_X.json` (şema: `sablonlar/sahne_dokumu.schema.md`).
- `motor/dokum_kontrol.py` → GEÇTİ.
- Hikâye ajanı (A1) metni denetler: dizi doğruluğu, "hiç izlememiş biri anlar mı" 1–5 puanı, 12 kelime sınırı.
- Sahne yönetmeni ajanı (A2) dinamikleri denetler: her cümlenin görüntüsü, geçiş bağları, duygu kanalları, ölü süre.
- Kullanıcıya **örgü sunumu** gider: okunabilir tablo (cümle | görünen | kilit | hareket | geçiş | duygu | süre) + 1–3 karar sorusu.
- **Kapı:** Kullanıcı örgüyü onaylar.

**F4b · Hareket taslağı (yeni adım)**
- Son çizim yapılmadan önce bölümün **blok animatiği** çıkarılır: kaba şekiller ve yer tutucu öğeler, gerçek zamanlama (geçici TTS ya da tahmini süre), bütün geçişler ve kelime kilitleri, 960 px.
- Amaç akışı, ritmi ve geçişleri ucuza onaylatmaktır. Görsel kalite bu adımda sorulmaz.
- **Kapı:** Kullanıcı akışı onaylar ya da "şu geçiş olmadı" der.

**F4c · Ham kareler (son kalite)**
- Her çekimin anahtar kareleri ve **her geçişin orta karesi** son kalitede, 1920 px.
- Öz değerlendirme (≥ 2 tur, R13 kırpması) → kurul (tek ajan, kontakt sayfası) → kullanıcı sunumu.
- **Kapı:** Kullanıcı kareleri onaylar.

**F4d · Ses ve animatik**
- TTS (satır satır) → kelime zamanları (`motor/kelime.py`) → çekim süreleri sese göre ayarlanır → tam render.
- Kurul videoyu hareketiyle denetler (D1–D10 + R kuralları), ardından kullanıcıya gider.
- **Kapı:** Kullanıcı bölüm animatiğini onaylar.

### F5 · Ses tasarımı (bütün bölümler bitince)
- Bölüm müzikleri (Eleven Music, vokalsiz, duygu eğrisine göre), SFX kütüphanesi, ortam sesleri.
- Miks: konuşma öncelikli (`07_TEKNIK_HAT §5`). J-cut geçişler. Whisper ile anlaşılabilirlik testi.

### F6 · Montaj ve master
- Bölümler birleştirilir. 1080p usta dosya, −16 LUFS. Bölüm zaman damgaları.
- Son kontrol: 10 rastgele an + bütün bölüm geçişleri + kahraman kareler.

### F7 · Yayın paketi
- 8 dilde SRT, başlık ve açıklama, bölümler, etiketler (`sablonlar/yayin_sablonu.md`).
- Kapak görselleri (8 dil, CTR ajanı + sanat yönetmeni ajanı, 168 ve 320 px kontrolü).
- İsteğe bağlı dublaj: dil başına ses parçası (kredi onayı alınır).

---

## Her bölümde kullanıcıya giden sunumun biçimi
1. Kısa durum cümlesi.
2. Dosya: örgü tablosu, blok animatik, kontakt sayfası ya da animatik.
3. Kurul özeti: 3–5 madde, ölçüt kodlarıyla.
4. AskUserQuestion: 1–3 somut karar, önerilen seçenek ilk sırada.
