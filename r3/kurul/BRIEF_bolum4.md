# Brief: Bölüm IV · Paris ham kareleri
**Önce oku:** `/home/claude/r3/kurul/BRIEF_bolum1_v3.md` (zorunlu kalite kuralları 1–9), `/home/claude/r3/kurul/BRIEF_SABLON.md`, `/home/claude/r3/kurul/DERSLER.md` → "KÖK NEDEN ANALİZİ".
**Çıta:** `/home/claude/r3/bati/v3/kontakt_v3_960.png` (kullanıcı: "harika"). Tekniklerini `/home/claude/r3/bati/v3_a.py`, `v3_b.py`, `v3_c.py` dosyalarından yeniden kullan. Yeni her kare onlarla yan yana konduğunda zayıf kalmamalı.
**Teknik:** Kod `/home/claude/r3/bati/v4_paris.py` içinde (`from kareler6 import *`, gerekirse `import v3_a, v3_b, v3_c, gemi as G`). Çıktılar `/home/claude/r3/paris/<id>.png`, kontakt `/home/claude/r3/paris/kontakt_paris_960.png`. Dosyanın sonunda `FR = {...}` olur. Ortak dosyalara yazılmaz; video, ses ve git yok.
**Karakterler:** `RG` (Ragnar; kimlik öğeleri korunur, aynalanmaz), `FLOv`, `ROLLO`, `ATHv`. Yeni olanlar:
- Frank muhafız: `KL.soldier_spec` türevi; konik nasal miğfer, zincir zırh, mavi/kırmızı tunik, uzun kalkan.
- Piskopos: cübbe katmanı `robe()` + mitre şapka + asa.
- Frank zırhlı Rollo: ROLLO + zincir zırh, Frank miğferi, kırmızı-altın pelerin.

Tümü model gövdesiyle çizilir (R11, R12); silüet yok.
**Ölçek:** Tanrı ya da şehir gibi büyük öğeler ölçekle büyütülür (minik insanlar, alt açı). Odin dersi: kostüm tek başına kudret vermez.
**Bütçe:** en fazla 2 öz değerlendirme turu, yaklaşık 40 araç çağrısı. R13 kırpması yalnızca en riskli 4 karede alınır: 15b, 16b, 16e, 17.

| id | Satır | Göster | Çekim / ışık | Ayrıntılar (öneri) |
|---|---|---|---|---|
| p15b | Nehrin ortasında bir ada. Etrafında aşılmaz taş surlar. | Sabah sisinde Seine, ada üstünde surlarla çevrili Paris: kuleler, çan kuleleri, köprüler; nehirde Viking filosu (G.longship, kademeli) | Çok geniş, hafif yüksek; soğuk sabah, sis, uzak altın ışık | Söğütler, kıyıda kamp ateşleri, kuşlar, sur üstünde minik muhafızlar, sancaklar |
| p15c | İlk saldırınızı surlar yutuyor. | Sur dibi: devrilen merdivenler, yukarıdan kaynar yağ ve oklar, kalkan duvarı arkasında Vikingler (gerçek modeller, sıralı) | Alt açı, orta; duman, turuncu yağ buharı | Düşen taşlar, kırık kalkanlar, ok yağmuru, sis |
| p15d | Sen de surdan düşüyorsun. | Ragnar surdan geriye düşüyor; elinden balta kayıyor (dramatik dinamik açı) | Tepeden aşağı ya da yan; gökyüzü ve sur kenarı | Taş parçaları, ok, pelerin dalgası |
| p15e | Yaralı, ateşler içinde. | Çadırda postlar üstünde ateşli Ragnar, ter, bandaj; başında endişeli Floki (ya da Bjorn) | Yakın; mum, soğuk dış ışık çadır aralığından | İlaç kâsesi, kanlı bez, kalkan, balta |
| p16a | Kapı açılmıyorsa, seni içeri taşımalarını sağlarsın. | Ragnar gözlerini açmış, sinsi bakış; yanında beliren plan çizimi (deri üstüne kömürle tabut ve kapı ok çizimi) | Yakın; mum ışığı | Kömür, deri parşömen, harita |
| p16b1 | Vaftiz oluyorsun. | Nehir kıyısında piskopos (cübbe, mitre) Ragnar'ı vaftiz ediyor; Frank soyluları, Vikingler izliyor | Orta; gri gökyüzü, ışık yarığı | Haç, buhurdan, sancaklar, nehir |
| p16b2 | Sonra ölüyorsun. Ya da öyle görünüyorsun. | Çadırda yas: Ragnar kefen içinde, gözleri kapalı; adamları başında. (Animasyonda bir göz kısa açılacak.) | Orta; mum | Ölü hediyeleri, kalkan, Floki'nin gizli sırıtışı |
| p16c | Adamların tabutunu şehre sokuyor. | Paris kapısında omuzlarda taşınan tabut, şüpheli Frank muhafızlar, rahipler | Orta; soğuk gün | Kapı demiri, zincir, mızraklar, kalabalık |
| p16e | Kapılar açılıyor. Paris düşüyor. | Kapı içeriden açılırken dışarıdan akan Viking seli; şehirde alevler | Geniş, kapıdan; ışık ve duman | Kırık sürgü, düşen muhafız, yangın |
| p17 | Dönüş yolunda Floki'ye tek kelime: Biliyorum. | Gemide yakın plan: Ragnar (fig_bust) ve Floki yüz yüze; Floki'nin yüzü donuyor; Ragnar'ın boynunda Athelstan'ın haçı | Yakın, iki kişilik; soğuk deniz ışığı | Halat, deniz serpintisi, gri ufuk |
| p18a | Doğudan gelen bir ilaç. | Karanlık odada titreyen el, küçük şişe, toz; solgun, terli Ragnar | Yakın ve insert; tek mum, yeşilimsi ton | Duman, dağınık yatak, boş kâse |
| p18c | Bu kez surların başında kardeşin var. | Sur üstünde Frank zırhlı Rollo ve Frank askerleri; aşağıda nehirde gemide Ragnar ona bakıyor | Alt açıdan Rollo (heybetli), yüksek açıdan Ragnar; ya da ikisi bir kadrajda | Sancaklar, mancınık, sis |
| p18d | Ve seni yeniyor. | Nehirde yanan Viking gemileri, gerilmiş zincir, geri çekilen Ragnar'ın gemisi | Geniş; alev ve duman, alacakaranlık | Batan direkler, alevli oklar, yansımalar |
