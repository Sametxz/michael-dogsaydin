# Kahraman kare testi · ivar hero_v1

## G2

**Puan: 2 / 3.** Kare son çıktıya uygun, ama kahraman kare çıtasının (3) altında. Eski ivar_19.5'e göre büyük sıçrama var. Kalan sorunlar parametre düzeyinde.

**[A] ölçümleri** (letterbox dışı alan; `hero_v1` / eski `ivar_19.5` / `yas_16`):
| Madde | hero_v1 | eski 19.5 | yas_16 | Eşik | Sonuç |
|---|---|---|---|---|---|
| R7 L p95 | 0,64 | 0,64 | 0,59 | ≥ 0,15 | ✔ |
| L8 değer aralığı (p95 − p5) | **0,55** | 0,46 | 0,42 | ≥ 0,35 | ✔ |
| L4 düz alan (64 px blok, σ < 0,012) | **%6** | %23 | %19 | ≤ %35 | ✔ |
| L9 merkez − kenar | +0,03 | +0,07 | +0,05 | ≥ 0 | ✔ (sınırda) |
| L6 ışık − gölge yanı (yanak / alın) | **0,11 / 0,10** | – | – | ≥ 0,12 | ✘ (az farkla) |
| S5 doygunluk | 0,23 | 0,24 | 0,23 | ±0,06 | ✔ (yas ile aynı plan) |
| S1 yüz kutusu (alın–çene) | ~%59 | – | – | ≥ %35 | ✔ |

**Doğru olanlar:** Orman 3 katman, bulanık ve sisli; arka planda düz alan neredeyse yok. Soğuk tek renk planı yas sahnesiyle aynı. Yüz kadrajın sağ üçte birinde, ¾ açıdan. Başta kenar ışığı var. Form gölgesi ilk kez figürün üstünde.

**Sorunlar:**
- Anahtar ışık "sol üst" olarak tanımlı, ama arka plan solda ve sağda aynı parlaklıkta (0,51 / 0,51). `bloom_spot(420,220)` okunmuyor, ışığın yönü yalnızca yüzdeki zayıf degradeden çıkıyor.
- Yüz arka plandan karanlık (yüz merkezi 0,45, arka plan 0,51). Göz yüze konturla gidiyor, ışıkla gitmiyor.
- Gölge, bütün sprite'a uygulanmış doğrusal bir perde gibi. Kaş altında, burnun gölge yanında ve sakalın boyna düştüğü yerde çekirdek gölge yok.
- Rim ışığı sağdaki gölge tarafında da (sakal kenarı) aynı güçte. Bu, tek ışık kaynağı fikriyle çelişiyor.
- Halkadaki sıcak vurgu grade içinde kaybolmuş (halka bölgesi L 0,30, renk zeytin ve kahverengi). Halkanın içi koyu bir "lomboz" gibi okunuyor.
- Bebeğin eli kadrajın alt kenarında, letterbox'a kesilmiş ve neredeyse görünmüyor. Sahnenin duygu nesnesi kaybolmuş.
- Ön plandaki dal sağ üstte letterbox'ın altında kalıyor. Zerreler ve nefes buharı 1080p'de seçilmiyor. Bu yüzden 5. derinlik katmanı (L3) fiilen yok.

**Düzeltmeler (en fazla 5):**
1. **Işığı yönlü yap ve yüzü odak yap (L5, L6, L9).** Bloom kaynağını sol üstte kadraja sok (`bloom_spot(260,120,700,a=0.55)`) ve yüze vuran soğuk bir `light_shaft` ekle. Sağ yarıya `gradient_grade` ile −0,08 L koyulaştırma uygula. Hedef: yüz merkezi ≥ arka plan + 0,05; ışık ile gölge yanı arasındaki fark ≥ 0,15.
2. **Form gölgesini şekle bağla (L6, S6).** Doğrusal perdenin (`a=0.45`) yerine iki katman kullan. Ilk katman, mevcut degradenin `a=0.6` olan hâli. Ikinci katman, `head_svg` içine çizilen çekirdek gölge şekilleri: kaş altı, burnun sağ yanı, elmacık altı, sakalın boyna düşen gölgesi (`multiply`, %40). Rim ışığını gölge tarafında `a ≤ 0,3`'e indir ya da yalnızca sol ve üst kontura uygula.
3. **Halkayı tek sıcak vurgu yap (L10).** Halkayı ve bebeğin elini grade'den sonra çiz ya da grade'i maskeyle bunların dışına uygula. Halkaya `#FFC860` bloom (a 0,45) ve parlak bir specular yay ekle. Halkanın içini düz koyu yeşil yerine kolun devamı olarak doldur.
4. **Bebeğin elini kadraja al (L1, S2).** Kol ve eli 120–160 px yukarı taşı: eli Ragnar'ın parmağını kavrar hâlde, letterbox'ın en az 80 px üstünde konumla. Kolun düz bej dikdörtgenine hacim ver: üst kenarda ışık, alt kenarda gölge şeridi. Bu kare, sahnenin "yapamıyorsun" sebebini göstermeli.
5. **Ön plan katmanını görünür kıl (L3, L10).** Dalı kadrajın içine, sağ kenarda 200–350 px yüksekliğe indir (bulanıklık 18 kalsın). Zerreleri büyüt (4–8 px), sayısını 60'a çıkar ve bir kısmını ön planda bulanık çiz. Nefes buharı ancak `a ≥ 0,35` ile okunur.

## G3

*`hero_v1.png` incelendi. Karşılaştırma: `eski_ivar_19.5.png` ve `referans_yas_16.png`. Ölçüt: GORSEL_STANDART v1. Ölçüm (letterbox dışı): L p5 0,10 / p95 0,64 (aralık 0,55), merkez–kenar −0,04, S 0,23. Yüzde ışık alan yan 0,59, gölge yan 0,47 (fark 0,12).*

**Puan (G3): 2 / 3.** Kesin red: R2, R3, R5, R6, R7 yok. **R4 sınırda** (aşağıda madde 5).

**İyi olanlar**
- **S1 karşılanıyor, hem de güçlü.** Yüz kadraj yüksekliğinin ~%65'i, ¾ görünüm, iki göz okunuyor. Eski karede (`ivar_19.5`) sahnenin doruğunda Ragnar'ın yüzü hiç yoktu. Bu, sahnenin en büyük eksiğini kapatıyor.
- **E1 tutarlı.** İç kaş uçları kalkık, kapaklar yarı düşük, ağız köşeleri aşağıda, alt dudak titrek. Üç bölge aynı duyguyu söylüyor. Sessiz okumada (S4) "acı / kırılmış" doğru okunuyor.
- **E4 iyi.** Gözbebekleri aşağı ve sola, bebeğin eline ve halkaya bakıyor. Bakış, karedeki tek sıcak vurguya (halka) yön veriyor. Yas_16'dan daha iyi oyunculuk; orada bakış boşluğa gidiyordu.
- **E3 var.** Gözyaşı, kaş arası çatık çizgileri, burun-dudak gerilimi ve alın kırışığı ilk kez duyguyla birlikte kullanılmış.
- **Atmosfer duyguyu destekliyor** (D5/S5): soğuk sis, bulanık orman, tek sıcak vurgu halkada.

**Duyguyu zayıflatanlar (dürüst)**
1. **Gözyaşı yara izinin üstünde.** Damla, sağ yanaktaki pembe yaranın hemen yanından iniyor ve ikisi tek bir çizgi gibi okunuyor. Tur 11–12'de alınan "gözyaşı yaradan ayrı" dersine aykırı. Gözyaşı sol göze alınmalı.
2. **Bağlam okunmuyor.** Bebeğin eli kadrajın alt kenarında, letterbox'a kesilmiş birkaç piksel. Bıçak yok. Kare tek başına "üzgün adam" anlatıyor, "**çocuğunu öldüremeyen baba**" anlatmıyor. S2'deki duygu cümlesi (vazgeçiş ve çaresizlik) için bebeğin parmakları halkayı ya da Ragnar'ın parmağını kavramalı ve görünür olmalı (dizideki an da bu).
3. **Kaşlar siyah kama blokları.** Duyguyu doğru yöne çeviriyorlar, ama kalınlıkları ve düz siyahlıkları maskeyi "kızgın / ağır" yöne çekiyor. Yas yüzünde (Tur 12) kullanılan ince kaş (`brow_k` 0,68) burada da kullanılmalı.
4. **E5 ihlali.** Pembe yanak lekeleri trajik kahraman karede hâlâ duruyor.
5. **Kol kimin? (R4 sınırda, C2).** Halkalı kol kadrajın sol kenarından giriyor, oysa omuz x≈700'de. Bu kol Ragnar'ın bedenine bağlanmıyor ve yabancı bir kol gibi okunuyor. Önkolun ucu (el) parmaksız, düz bir silindirle bitiyor. Halka yine yüz kadar dikkat çekiyor.
6. **S6 çıtası karşılanmıyor.** Form gölgesi var ama tek, düz bir gradyan (fark yalnızca 0,12). Elmacık, göz çukuru ve burun altı gibi hacim bölgeleri yok. Burun tek "ㄱ" çizgisi. Kırışıklar ince ve kahverengi "çizik" gibi duruyor, kas gibi değil. Nefes buharı neredeyse görünmüyor.

**Born in Lore çıtasına göre:** Eski kareye göre büyük sıçrama, yas_16'ya göre bir adım ileri (ışık, DOF, bakış). Ama hâlâ **düz vektör kukla yüzü**. Kratos videosundaki boyalı hacim, fırça dokusu, anatomik göz kapağı ve dudak yok. Bu kare "doğru oyunculuk, eksik çizim".

**G3 önerileri (öncelik sırasıyla):** (a) bebeğin eli halkayı ya da Ragnar'ın parmağını kavrasın ve kadrajın alt üçte birinde net görünsün; (b) gözyaşı sol göze; (c) ince ıslak kaş ve pembe lekelerin kaldırılması; (d) kol Ragnar'ın omzundan gelsin, el görünür parmaklarla; (e) yüze 3 bölgeli hacim gölgesi (göz çukuru, elmacık altı, burun altı) ve belirgin bir burun kanadı.

## G1

**Puan: 1/3 (YETERSİZ). Kafa tek başına 2 alırdı; ön plandaki kol ve bebek eli kareyi düşürüyor.**

**Kesin red kontrolü**
- **R4: VAR.** Ön plandaki önkol (`ARM`) kadrajın ortasında düz bir kesikle bitiyor; ucunda el yok (bkz. yaklaşık x 700, y 930). Kol sol kenardan Ragnar'ın göğsüne doğru uzanıyor, yani kimin kolu olduğu ve hangi omza bağlandığı okunmuyor. Bebeğin kolu ve eli neredeyse tamamen letterbox'ın altında kalıyor (`BABYH` y ≈ 1020 > 1010). Görünen yalnızca birkaç piksellik parmak. Anlatılan "halkalı kol + bebeğin eli" teması karede yok (C2).
- **R1: RİSK (henüz red değil).** "Endişe kırışığı" ve "kaş arası çatık" çizgileri (`head_svg`, y −52…−76 × 3,3) alına değil, **kazınmış ve noktalı kafa derisi bölgesine** düşüyor (yaklaşık x 1090–1200, y 170–260). Kahverengi çizgiler kazınmış yan + tepe saç kütlesinin üstünde kafa derisi deseni gibi okunuyor. Bu da yasaklı "kafa derisi deseni + kazınmış yan + tepe örgü" kombinasyonuna yaklaşıyor.
- R2, R3, R5, R6 ve R7 yok.

**C ölçütleri:** C1 ✓ (baş eğik, bakış aşağıda, eyleme bağlı). C2 ✗ (temas noktası görünmüyor). C3 ✗ (yakın planda el yok ya da kesik). C4: bebek değerlendirilemiyor. C5 ✓ (yara izi, boncuklu örgü, undercut ve kol halkası görünüyor). C6 ~ (kafa kütlesi ve saç perçemi yas_16 ile tutarlı, ama kaşlar model v11 ve yas_16'ya göre çok daha kalın, dolgulu siyah takozlar). C7 ~ (kontur kalınlığı tutarlı; ancak kenar ışığı gölge tarafı dahil tüm kafanın çevresinde beyaz bir hale gibi duruyor ve çıkartma etkisi veriyor). S7 ✗: kol halkasının dış çapı ≈ 218 px, önkol kalınlığı ≈ 112 px. Oran ≈ 1,95; kural × 1,25.

**Düzeltmeler (en fazla 5)**
1. **Kırışıklar alına taşınsın:** Endişe ve çatık çizgileri kaş ile saç çizgisi arasındaki çıplak alına alınsın (kafa biriminde y −30…−45). Kazınmış ve noktalı bölgede hiçbir çizgi kalmasın (R1 riski kapanır).
2. **Kaşlar modele dönsün:** `HS = 3.3` ölçeği kaş dolgusunu takoza çeviriyor. Kaş kalınlığı model v11 ve yas_16 oranında tutulsun (tarama çizgili, dolgu yarı ton). İç uçların yukarı kalkık şekli korunsun.
3. **Gözyaşı ile yara izi ayrılsın:** Gözyaşı şu an burun kanadının yanından, yara iziyle çakışarak iniyor ve "burun akıyor" gibi okunuyor. Gözyaşı yakın gözün alt kapağının orta ya da dış köşesinden başlasın, yara izinden ≥ 20 px uzakta dursun, yarı saydam olsun ve üstünde parlak bir nokta taşısın.
4. **Ön plan teması yeniden kurulsun:** Ragnar'ın kendi omzundan gelen ve gövdeyle yönü uyumlu bir önkol çizilsin. Ucunda parmakları görünen gevşek bir el (`relax` ya da `grip`) olsun. Bebeğin minik eli Ragnar'ın parmağını kavrasın ve temas noktası letterbox'ın üstünde, y ≤ 940'ta kalsın. Kol halkası, kolun içinden geçtiği perspektifli bir elips olsun (iç kısmı dolgusuz). Çapı = önkol × 1,25.
5. **Kenar ışığı yalnızca ışık tarafında olsun:** `rim` yalnızca sol üst kenara ve maskeyle uygulansın; sağ ve alt gölge tarafında hale kalmasın. Ardından kafa, model v11'in ¾ kafası ve yas_16 ile yan yana konup karşılaştırılsın (C6, dönüş şeridi).

## Kurul kararı

**Karar: YETERSİZ** (kahraman kare). Puanlar: **G1 1 · G2 2 · G3 2**, toplam 5/9. Eşik: her üyede ≥ 2 ve kahraman karede toplam ≥ 7. Kesin red: **R4 var** (elsiz önkol, kimin olduğu belirsiz kol, letterbox altında kalan bebek eli). **R1 riski var** (kırışıklar kazınmış kafa derisinin üstüne düşüyor).
**Yön doğru:** S1 (yüz ~%60), E1 ve E4 (bakış halkaya ve bebeğe gidiyor), değer aralığı ve atmosfer eski kareye göre açıkça daha iyi. Sorunlar sistemde değil, parametrelerde. Aynı kare v2 ile düzeltilebilir.

**Birleştirilmiş düzeltmeler (v2):**
1. **Temas ve bağlam (R4, C2, C3, S2, L1):** Ragnar'ın kendi omzundan gelen, gövdeyle yönü uyumlu bir önkol çizilsin. Ucunda parmakları görünen gevşek bir el olsun. Bebeğin eli bu parmağı kavrasın ve temas noktası y ≤ 940'ta net görünsün. Kol halkası perspektifli bir elips olsun ve çapı önkol × 1,25 (S7).
2. **Kafa derisi temiz (R1):** Endişe ve çatık çizgileri yalnızca çıplak alına konsun. Kazınmış ve noktalı bölgede hiç çizgi kalmasın.
3. **Yüz yeniden ayarlansın (C6, E5, E1):** Kaşlar model v11 / yas_16 kalınlığında, ıslak ince tarama ile çizilsin. İç uçların kalkık şekli korunsun. Pembe yanak lekeleri kaldırılsın.
4. **Gözyaşı (E3):** Gözyaşı yakın gözün alt kapağından başlasın, yara izinden ≥ 20 px uzakta dursun, yarı saydam olsun ve parlak bir noktası olsun. "Burun akıyor" gibi okunmasın.
5. **Yönlü ışık ve hacim (L5, L6, L9, S6):** Kaynak sol üstte görünür olsun ve yüze vuran soğuk bir huzme eklensin. Doğrusal perdenin yerine çekirdek gölge şekilleri gelsin (kaş altı, göz çukuru, burnun gölge yanı, elmacık altı, sakalın boyna düştüğü yer). Hedef: ışık ile gölge yanı arasındaki fark ≥ 0,15, yüz merkezi arka plandan ≥ 0,05 daha parlak. Rim ışığı yalnızca ışık tarafında olsun ve bir burun kanadı çizilsin.
6. **Tek sıcak vurgu ve ön plan (L3, L10):** Halka ve bebeğin eli grade'den sonra çizilsin, halkada sıcak bir bloom ve specular parlama olsun. Ön plandaki dal kadraja girsin. Zerreler büyütülsün, nefes buharı a ≥ 0,35 ile görünür olsun.

**Kullanıcıya sorulacak:** v2'de kurul bu altı düzeltmeyi uygulayıp yeniden puanlayabilir; bu adım için yeni bir yön kararı gerekmiyor. Ama aşağıdaki tavan değerlendirmesi göz önüne alınınca bir soru var: **Çıta, "Born in Lore'a yakın, temiz ve gölgeli 2D vektör" olarak mı tanımlansın, yoksa kahraman karelerde hattın dışından (elle çizilmiş ya da boyanmış) yüz katmanı mı kullanılsın?** Kurulun önerisi: v2 sonucunu görmeden karar verilmesin. v2, bu hattın üst sınırına yakın bir örnek olacak.

### Tavan değerlendirmesi (dürüst)

Bu hat, SVG parçalarından kurulan parametrik bir kukla (`head3`) ve Skia efektlerinden oluşuyor. Düzeltmelerle varabileceği yerler:
- **Çıtaya yaklaşabilir (~%80–90):** kompozisyon, ölçek kademesi, ışık yönü, rim ve huzme, atmosfer (sis, yağmur, toz), derinlik bulanıklığı, renk planı, kurgu ve kelime kilitli efektler. Bunlar G2'nin alanı ve yas sahnesi bunun yapılabildiğini gösterdi.
- **Kısmen yaklaşabilir (~%60–70):** oyunculuk (bakış, kaş-göz-ağız uyumu, eylem pozları, temas). İfade parametreleri ve sahneye özel poz fonksiyonlarıyla belirgin biçimde iyileşir. Ama her yeni poz el ile kodlanmış bir geometri demek; iş yükü yüksek, çeşitlilik sınırlı.
- **Tavanın altında kalır (~%40–50):** Born in Lore'un boyalı illüstrasyon dokusu. Anatomik göz kapağı ve dudak, fırça izi, yüz yüzeyinde yumuşak geçişli hacim, gerçek el ve parmak anatomisi. Vektör primitiflerle bu "temiz düz 2D + katmanlı gölge" düzeyinde kalır. Kratos videosundaki boyalı yüz kalitesine kod parametreleriyle ulaşmak gerçekçi değil.
- **Sonuç:** Düzeltilmiş hat "iyi yapılmış, gölgeli, sinematik vektör 2D" seviyesine ulaşabilir. Kullanıcının "çizimler aşırı kötü" eleştirisinin büyük kısmı (yüzsüz doruklar, kukla pozları, düz arka planlar, klonlar) bu seviyede giderilir. Ama Born in Lore ile birebir eşitlik beklenmemeli. Bu beklenti kullanıcıyla **v2 sunulurken açıkça konuşulmalı.**

## Kurul · hero v2

*G3 koordinatör olarak üç alanı birlikte değerlendirdi (G1 ve G2'ye mesaj gönderilemiyor). Önce standart v1.1 ve DERSLER.md okundu. İncelenen dosyalar: `hero_v2.png`, `hero_v2_gri.png`, `hero_v2_1_8.png`, `hero2.py`.*

### Puanlar
| Alan | Puan | Gerekçe (kısa) |
|---|---|---|
| G1 · karakter ve tutarlılık | **2** | R1 yok (kırışıklar yalnızca alında, kazınmış bölgede yalnızca kirli sakal noktaları var). R8 yok (bant `forearm_band()`'dan geliyor). Kaşlar modele dönmüş, pembe lekeler kalkmış. Kol gövdeden gelip kadraj altından çıkıyor (R4 kapandı). El gevşek ve parmağını sunuyor (C1–C3 ✓). **Ama kafa `scale(-HS)` ile aynalandığı için asimetrik kimlik işaretleri yer değiştirmiş** (C6): yara izi ve örgü artık öbür tarafta. Model sayfası, yas_16 ve ivar_14 ile süreklilik bozuluyor. El sırtındaki düğüm avuç tarafında görünüyor olabilir; açı belirsiz. |
| G2 · kompozisyon, ışık, renk | **2** | Kompozisyon belirgin biçimde iyileşmiş: köşegen göz yolu (yüz → bakış → el → bebek), ön planda höyük, sağ üstte dal, değer aralığı 0,57. **Ama hero_v1'in ışık hedefleri tutmamış:** yanakta ışık ile gölge yanı farkı 0,06 (hedef ≥ 0,15), yüz arka plandan ayrışmıyor, sıcak vurgu tek değil (aşağıdaki tablo). Rim ışığı gölge tarafında da beyaz bir hale yapıyor. Höyüğün yeşili soğuk planın dışında kalıyor. |
| G3 · duygu ve son çıktı | **2** (güçlü) | Ses olmadan okunuyor (S4 ✓): Ragnar çocuğa bakıyor, bebek parmağını tutuyor, gözyaşı ve titreyen dudak var. Ölçek karşıtlığı (minik bebek, dev baba) kırılganlığı veriyor. Gözyaşı yaradan ayrı. 1/8'de bile hikâye okunuyor (thumbnail ✓). Projenin bugüne kadarki en güçlü duygu karesi. Çıtanın (3) altında kalma nedenleri: yüz hâlâ düz bir maske (burun tek çizgi, yanakta "çizgi" gibi duran gölge bantları), bebeğin gülümsemesi S2'de bilinçli zıtlık olarak yazılmamış. |
| **Toplam** | **6/9** | Kahraman kare eşiği: her alanda ≥ 2 ✓, toplam ≥ 7 ✗ |

### Ölçüm tablosu (letterbox dışı; [A])
| Ölçüt | hero_v1 | **hero_v2** | Hedef | Sonuç |
|---|---|---|---|---|
| R7 L p95 | 0,64 | 0,67 | ≥ 0,15 | ✔ |
| L8 değer aralığı | 0,55 | **0,57** | ≥ 0,35 | ✔ |
| L9 merkez − kenar | −0,04 | −0,02 | ≥ 0 | ✘ (az farkla) |
| L6 yüz ışık − gölge yanı (yanak) | 0,12 | **0,06** | ≥ 0,15 (v1 kararı) | ✘ geriledi |
| Yüz merkezi − arka plan | −0,06 | **0,52 − (0,50…0,55) ≈ 0** | ≥ +0,05 | ✘ |
| S5 ortalama doygunluk | 0,23 | 0,23 | yas ile ±0,06 | ✔ |
| L10 sıcak vurgu tekliği (sıcak px) | – | halka ≈ 2.800 px · **saç boncukları ≈ 2.200 px** · kapüşon kenarı < 50 | tek odak | ✘ boncuklar halkayla yarışıyor |
| S1 yüz yüksekliği | ~%60 | ~%55 | ≥ %35 | ✔ |
| Gri ton | – | Bebek ve el okunuyor. Yüz sis ile aynı orta gride karışıyor, sakal tek kara kütle. | değer ayrımı | ~ |
| 1/8 | – | Yüz, bebek, el ve halka okunuyor. Halka tek sıcak nokta değil (boncuklar da parlıyor). | okunur | ✔ |

### Karar: **YETERSİZ (eşiğin 1 puan altında, düzeltme parametre düzeyinde)**
Yön doğru ve kare büyük ölçüde oturdu. Sorunlar sistemde değil, ayarlarda. v3 tek turda kahraman kare eşiğine (≥ 7) çıkabilir. Hikâye, oyunculuk ve kompozisyon için yeni bir karar gerekmiyor.

### Kalan düzeltmeler (en fazla 6, öncelik sırasıyla)
1. **Aynalama kimliği bozmasın (C6).** `head3`'e `facing="right"` parametresi eklensin. Geometri aynalansın, ama yara izi, örgü ve boncuk tarafı model sayfasındaki tarafta kalsın. Ya da yara ve örgü aynalamadan sonra ayrı katmanda çizilsin. Kural standarda ve DERSLER.md'ye girsin: asimetrik kimlik işaretli karakterler `scale(-1)` ile çevrilmez.
2. **Yüzü ışıkla odak yap (L6, L9, yüz − arka plan).** Sol üstteki anahtar ışık yüze vursun. Gölge tarafına `#3A4A6A` multiply uygulansın (ışık–gölge farkı ≥ 0,15). Yüzün arkasındaki sis 0,06 L koyulaştırılsın ya da yüze yumuşak bir key bloom eklensin (yüz merkezi arka plandan ≥ 0,05 parlak). Yanaktaki dikey "çizgi" gölge bantları yumuşak çekirdek gölge şekillerine dönüşsün.
3. **Rim ışığı yalnızca ışık tarafında olsun.** Rim, sol ve üst konturda maskeyle uygulansın. Sağdaki sakal ve kafa kenarındaki beyaz hale ile bebeğin sağ kenarındaki hale kalksın (çıkartma etkisi).
4. **Tek sıcak vurgu (L10).** Saç boncukları desatüre edilsin: koyu bronz, S ≤ 0,35, specular yok. Böylece sıcak altın yalnızca halkada kalır. Bebeğin kapüşon kenarı da bir ton soğutulsun.
5. **Mekân: nehir kıyısı (kullanıcı: "mekânlarda öğeler eksik").** Höyüğün yeşili soğuk plana çekilsin (desatüre, sisli). Bebeğin altına taşlar ve ıslak çakıl konsun. Arka planda, bebeğin arkasından geçen soluk bir nehir şeridi olsun, sisle karışan su parıltısıyla. Bebeğin altında temas gölgesi (AO) olsun. Kahverengi dal düz bir çubuk değil, dokulu bir kök ya da dal olsun.
6. **Yüz ve bebek ifadesinin ince ayarı (S6, S2).** Burun tek "ㄱ" çizgisi yerine burun kanadı ve burun altı gölgesiyle çizilsin. El sırtındaki düğüm, elin görünen sırt yüzüne yerleştirilsin. Bebeğin gülümsemesi, hayretle bakan yarı açık küçük bir ağıza dönüşsün. Ya da `sahne.md`'deki S2 cümlesine bilinçli zıtlık olarak yazılsın ("bebek gülümser, baba kırılır").

### Kullanıcıya sunum için önerilen tavan cümlesi
> "Bu kare, kod tabanlı çizim hattının nereye varabildiğini gösteriyor: hikâye, oyunculuk ve ışık Born in Lore düzeyine yaklaşabiliyor; boyalı illüstrasyon yüzü ve fırça dokusu ise bu hattın tavanının üstünde kalıyor, bu yüzden hedefimiz 'temiz, gölgeli, sinematik 2D'."

## Kurul · hero v3

*G3 koordinatör olarak üç alanı değerlendirdi. Standart v1.1. İncelenenler: `hero_v3.png`, `hero_v3_gri.png`, `hero_v3_1_8.png`.*

| Alan | v2 | **v3** | Gerekçe |
|---|---|---|---|
| G1 · karakter | 2 | **2** | Aynalama kalktı. Yara izi sağ tarafta, örgü ve boncuklar solda, model ve yas_16 ile aynı (C6 ✓). Gözyaşı sol gözde, yaradan ayrı. R1 ve R8 temiz, kol gövdeden geliyor (R4 ✓). Kalan: Ragnar'ın parmakları hâlâ tahta gibi düz bloklar, eklem tümsekleri yok. |
| G2 · ışık ve kompozisyon | 2 | **2** | Işık yönü artık okunuyor: başın arkası koyu, yüz kenarı aydınlık. Sisli nehir ve karşı kıyı mekânı kuruyor. Halka baskın sıcak vurgu. Hedefin altında kalanlar: ışık–gölge farkı ve ön plan taşları (aşağıdaki tablo). |
| G3 · duygu ve son çıktı | 2 | **3** | Duygu ve oyunculuk çıtada. Baba bebeğe, bebek hayretle babaya bakıyor. Küçük el dev parmağı tutuyor, gözyaşı ve nefes buharı var. "Yapamıyorsun" ses olmadan okunuyor. 1/8 boyda thumbnail gibi çalışıyor. Bu 3, oyunculuk ve okunurluk için; boyalı yüz dokusu (S6) tavan notunda. |
| **Toplam** | 6 | **7/9** | Kahraman kare eşiği: her alan ≥ 2 ✓, toplam ≥ 7 ✓ |

| Ölçüm [A] | v2 | **v3** | Hedef | |
|---|---|---|---|---|
| L8 değer aralığı | 0,57 | **0,58** | ≥ 0,35 | ✔ |
| L9 merkez − kenar | −0,02 | **+0,04** | ≥ 0 | ✔ |
| L6 ışık − gölge yanı (şakak / üst yanak / alt yanak) | 0,06 | **0,10 / 0,10 / 0,05** | ≥ 0,15 | ✘ (iyileşti) |
| Yüz − arka plan (başın arkası) | ≈ 0 | **0,46 − 0,25 = +0,21** (sol); sağda rim ışığıyla ayrışıyor | ≥ +0,05 | ✔ |
| L10 sıcak vurgu | halka ~%56, boncuklar ~%44 | **halka ~%83**, kapüşon kenarı ~%16, boncuklar ≈ 0 | tek odak | ✔ |
| S5 doygunluk | 0,23 | 0,25 | ±0,06 | ✔ |
| Gri ton ve 1/8 | yüz sise karışıyordu | yüz, bebek, el ve halka ayrışıyor | okunur | ✔ |

### Karar: **SON ÇIKTIYA UYGUN (kurul görüşü), kullanıcı onayına sunulur.**
Kahraman kare eşiğini geçiyor. Aşağıdaki 4 madde kareyi engellemiyor; final render'da ya da sahnenin öteki karelerinde uygulanabilir.

**Kalan maddeler (engelleyici değil):**
1. **Form ışığı:** Alt yanakta ve çenede ışık–gölge farkı 0,05. Çekirdek gölge (sol yanak altı, sakalın yüze düştüğü yer) koyulaştırılsın, hedef ≥ 0,15.
2. **Ragnar'ın eli:** Parmaklara eklem tümseği ve boğum kıvrımı eklensin. Kıvrık parmaklar işaretten serçeye kademeli kıvrılsın. Tahta blok görünümü kalksın.
3. **Ön plan kıyısı:** Taşlar düz koyu lekeler, kök düz bir çubuk. Taşlara ıslak parlaklık ve doku (`tas`, yosun) verilsin, kökün uçları sivrilsin ve kıyıya gömülsün. Höyük yosununa sise doğru açılan bir değer degradesi eklensin.
4. **Kapüşon kenarı:** Bebeğin altın kenarı bir ton soğutulsun (sıcak piksellerin %16'sı). Halka tek sıcak nokta olarak kalsın.

**Tavan notu (kullanıcıya):** Oyunculuk, kompozisyon ve ışık bu karede Born in Lore çizgisine yaklaştı. Yüzün boyalı hacmi ve fırça dokusu, kod tabanlı vektör hattının tavanında kalıyor.
