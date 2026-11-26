# Brief: <bölüm> ham kareleri v<N>

## Bağlam
Video: "<KARAKTER> olarak doğsaydın?" (Born in Lore, <DİZİ>). Bu bölüm: <1 cümle>. Kullanıcının son geri bildirimi: <...>.

## Çıta (mutlaka bak, yan yana kıyasla)
- `<REPO>/studyo/referans/kahraman_kare_hero_v4.jpg`, `toren_cenaze_d3.jpg`, `firtina_gemi_e4.jpg`, `holmgang_e7.jpg`
- Standart: `<REPO>/studyo/docs/05_KALITE_STANDARDI.md` (R1–R17). Dinamik: `02_DINAMIK_ANLATIM.md`. Duygu: `03_DUYGU_DILI.md`. Dersler: `06_DERSLER.md` + `<PROJE>/kurul/DERSLER.md`.

## Kare listesi
Her kare için:
- **<id> · <plan> · <duygu>** · Anlatım: "<…>"
  - Işık kararı: <kaynak, yön, sıcak/soğuk>
  - Katmanlar (ayrı Oge): gök / uzak / orta / ana / ön plan
  - 6–12 ayrıntı: 1) … 2) … 3) …
  - Kelimeye kilitli öğeler ve hareketleri: …
  - Geçiş: önceki çekimden nasıl girilir, sonrakine nasıl çıkılır? Geçiş orta karesi de çizilecek.
  - Duygu cümlesi: "Seyirci X hisseder çünkü …"

## Zorunlu kurallar (özet)
1. En az 4 derinlik katmanı, her biri ayrı öğe (paralaks için).
2. Düz renk alan yok. Doku ve degrade kullanılır.
3. Işık kararıyla başla: rim ışığı, gölge tarafı, temas gölgesi.
4. Karakterler yalnızca model kaynağından. Kimlik öğeleri tek kaynaktan.
5. Çizgi film sevimliliği yok (R10). R13: en önemli 2 nesnenin %200 kırpması.
6. Öz değerlendirme: en az 2, en fazla 4 tur. Her tur 1–5 puan, 4'ün altındaki madde düzeltilir.

## Teknik
- Kendi modülünde çalış: `<PROJE>/kareler/<bolum>_<harf>.py`. Ortak dosyaları değiştirme.
- Çıktı: `<PROJE>/kurul/<bolum>/<id>.png`, kırpmalar `<id>_crop1.png`, `<id>_crop2.png`.
- Video, ses, TTS ve git YOK.

## Teslim
Türkçe, en fazla 200 kelime: kare başına yapılanlar, son puan, kullanıcının beğenmeyebileceği riskli noktalar.
