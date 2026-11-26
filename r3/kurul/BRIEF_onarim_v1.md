# BRIEF: Denetim onarımları v1 (20.11.2026), tek görsel ajan

Önce oku: `CLAUDE.md`, `kurul/BRIEF_SABLON.md`, `kurul/BRIEF_bolum1_v3.md` (zorunlu kalite kuralları 1–9), `kurul/GORSEL_STANDART.md` (R8–R13), `kurul/DERSLER.md`, `kurul/denetim_v1.md`.
Kullanıcı onayladı: (A) yükselişte kahramanlık, (B) mantık boşlukları, (C) ifade ve jest notları. Her kare kullanıcıya **taslak** olarak gidecek; onaylı kare dosyalarının üstüne yazma.

## Çalışma biçimi (kredi tasarrufu)
- Bütçe: en fazla ~45 araç çağrısı. Her kare için öz değerlendirme yapılır: R13 ≥%200 kırpma, en az 2 tur.
- Yeni kareler **varyant** fonksiyonu olarak yazılır: `bati/onarim_v1.py` içinde `FR = {"d8": d8v, ...}`. Gerekirse var olan modülden import edip üstüne kur; onaylı fonksiyonları değiştirme.
- Ragnar yaş evresi zorunlu: `import ragnar_yas as YAS` ile kare çiziminden önce `YAS.uygula(YAS.RGn)`. Evre tablosu `ragnar_yas.EVRE`: Prolog ve I için RG1; II, III ve IV'ün ilk Paris'i için RG2 (kral kürkü, `_king`); p18 ve V için RG3; VI için RG4.
- Model gövdeleri (art3 `full`, `fig_bust`, `figure`) kullanılır. Profil görünüş yok, uydurulmaz. Asimetrik karakterler aynalanmaz.
- Hassas sınırlar: kan ve şiddet yok; yılanlar yalnızca gölge ya da siluet; ölüm sahnesinde yara yok. Oyuncu benzerliği ve dizideki Ragnar kafa dövmesi kombinasyonu yok.
- Çıktılar: `kurul/onarim_v1/<id>.png` (1920×1080) ve `kurul/onarim_v1/kontakt_960.png` (önce/sonra yan yana; eski kare `bati/out*`, `son/out`, `kesis/` vb. çıktılardan ya da FR çağrısından alınır). Son raporda kare başına bir satır: neyi değiştirdin, öz değerlendirme puanın.

## (A) Yükselişte kahramanlık
1. **d8** (II, `bedel/kareler4.py`): satır "Artık bir kralsın". Ragnar tahtta minik ve taçsız. Yeni karede alçak açı kullan: Ragnar (RG2, kral kürkü) kadrajın büyük kısmını doldursun, başında taç (altın bant, sade; dizideki taç kopyalanmaz), arkada salon, meşale ve diz çökmüş halk. Altın ışık vurgusu ver.
2. **e8** (I, `bati/kareler5.py` e8): "halkla paylaşmak". Şu an yalnız 3 adam var. Kalabalık (R12: 2–3 model, gerçek modeller) Ragnar'ın dağıttığı altın kol halkalarını, kâseyi ve gümüşü alıyor; yüzler sevinçli.
3. **f10** (I): "Jarl düşüyor". Jarl Haraldson'ın öne yığılma anı (kan yok; balta Ragnar'ın elinde aşağıda). Ragnar ayakta, kalabalık şaşkın.

## (B) Mantık boşlukları
4. **k21b** (V, `bati/v5_kayip.py`): "Fırtına filonu yutuyor". Şu an sakin gün batımı var. Gerekenler: fırtına gökyüzü, dev dalgalar, devrilen ya da batan 2–3 uzun gemi (`gemi.py` tek kaynak), şimşek. Efekt katmanı yağmur, flaş ve sarsıntıyı ayrıca ekleyecek; karede bunlar için boş alan bırak.
5. **b4** (III, `kesis/kareler3.py`): "Dostun yerde yatıyor". Kadrajda yalnız haç var. Kadraj kenarında Athelstan'ın yatan bedeni olacak, sakin, örtülü, yarası görünmeyecek. Ragnar diz çökmüş, haçı yerden alıyor (haç geçişinin anı). Haç modeli `athelstan` haçıyla aynı (R8).
6. **k26b / k26c** (VI, `bati/v6_son.py`): "Yılanlarla dolu çukur". Çukurun dibinde ışık huzmesinde kıvrılan yılan **gölgeleri** olacak (gövde çizilmez, ağız ya da diş yok). k26c'de Ragnar çukurun içinde, omzu ve göğsü görünüyor, RG4.
7. **Güneş taşı sürekliliği** (I): e4 ya da f7'ye bağlanan kısa bir insert karesi: Ragnar'ın eli, güneş taşı (e2'deki modelin aynısı, R8), bulutlu gökte taşın içinde yön veren ışık noktası. Adı `e4i`.

## (C) İfade ve jest notları (yalnızca ifade ya da el değişimi; kompozisyona dokunma)
Her notu önce o çekimin anlatım satırıyla karşılaştır (`anlatim/master_tr.json` ve animatik PLAN). Satırla çelişen ya da diziye uymayan notu atla ve nedenini yaz. Örneğin e4'teki "Ragnar dua eder" notu şüpheli: Ragnar fırtınada dua etmez, Floki güler.
- I e4: Floki başını geriye atıp kahkaha atıyor.
- I e6: "Onu öldürmüyorsun". Balta iner, bakış yumuşar.
- II d2: "Ve mum sönüyor". Ragnar'ın gözü kapanır, gözyaşı iner.
- II d7: "Ama sen daha iyi yalan söylüyorsun". Ragnar'ın yüzünde öfke yerine sinsi yarım gülümseme.
- II veda_2: Lagertha'nın gözleri kısık, çenesi sert; Aslaug elini karnına koyuyor.
- II ivar_4: "Yapamıyorsun". Yüz gevşer, gözyaşı iner (RG2; alın kırışıklıklarını azalt).
- III b2: Athelstan'ın gözleri kapalı, hafif tebessüm, haçı kavrıyor.
- III b4: madde 5 ile birleşik.
- IV p16a: haritaya sinsi bakış.
- IV p17: "Biliyorum". Ragnar gözlerini kısar, Floki bakışını kaçırır.
- V k19c: oğullar bakışlarını kaçırır.
- VI k23b: Ivar gözlerini kısar, ağzı yamuk gülümser.
- VI k26c: "Gelecekler". Hafif gülümseme, gözlerinde parıltı.
İfade adları `art3.EXP` / `art2.EXPR` içinde. Gözyaşı için var olan `grief` ifadesine bak.

## Kalite çıtası
Referans: `kurul/test_ivar/hero_v4.png` ve onaylı v3 kareleri. Her karede en az 4 derinlik katmanı olacak, düz renk alan olmayacak, belirgin ışık olacak, 6–12 anlamlı ayrıntı bulunacak. Vasat kare kabul edilmez.
