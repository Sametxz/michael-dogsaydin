# Görsel standart (kurul ortak metni, v1.1, 19.11.2026)

*v1.1 değişiklikleri (nesne kartı v1 incelemesi, tekrar eden dersler): R8 eklendi, §9'a N7 ve kart içeriği eklendi, eşikler R1–R8 olarak güncellendi.*

Kaynak: `kurul/benchmark/pano.md` (G1, G2, G3 ve tartışmalar). Referans: yas v5 **sahne kuruluşu** bakımından. Çizim kalitesinde çıta Born in Lore "Kratos": illüstrasyon kalitesinde 2D, güçlü yakın planlar, ifadeli yüzler.
**[A]** = otomatik ölçülür (`kurul/olcum.py` ya da render kontrolü). Diğer maddeler görsel incelemeyle işaretlenir.

## 1. Kesin red (puandan bağımsız, kare YETERSİZ)
- R1. CLAUDE.md sınırı: oyuncu benzerliği ya da dizideki Ragnar tasarımının kopyası.
- R2. Duygu ile ifade çelişiyor (ör. acı anında gülümseme) ve bu bilinçli çelişki S2'de yazılı değil.
- R3. Kimlik sızıntısı: bir karakterin işareti (yara izi, kırışık, kaş kalıbı) başka bir karakterde.
- R4. Kopuk ya da havada uzuv, kafa veya nesne. Boyunsuz kafa. **[A]** `assert_attached()`, ebeveyn eklemden ≤ 6 px.
- R5. Sprite döndürme izi (ör. ayakta figürün −90° döndürülüp "yatan" yapılması).
- R6. Çift nesne: aynı nesne aynı anda iki yerde.
- R7. Pozlama hatası: L p95 < 0,15 **[A]**.
- R8. Kimlik öğesi elle yeniden çizilmiş: dövme, düğüm, yara izi, broş, kol halkası ve haç yalnızca model kaynağından (`art3` / `props.py`) çağrılır. Kaynaktan farklı bir biçim varsa kare ya da nesne reddedilir. *(Tekrar eden ders: Tur 17 sızması, `veda_21.8` yarası, nesne kartı v1'deki ⊕ dövme.)*

## 2. Sahne düzeyi ölçütler (S)
- **S1 · Kahraman kare.** Her sahnede, duygu vuruşunu taşıyan en az bir yakın plan bulunur. Yüz kadraj yüksekliğinin ≥ %35'i **[A: yüz kutusu ölçümü]**, ¾ ya da önden, iki göz okunur. Kahraman kare kelime kilidine bağlanır.
- **S2 · Duygu cümlesi.** Sahne başlamadan önce şu cümle yazılır: "Seyirci X hisseder çünkü Y'nin yüzünde ya da bedeninde Z'yi görür." Kahraman kare bu cümleyi gösterir.
- **S3 · Ölçek kademesi.** En az 3 plan ölçeği (geniş, orta, yakın) bulunur. Doruk ya yakın planda ya da odağı figürde olan bir siluet/yalnızlık planında verilir. Geniş planda yüzdelik alt sınır yoktur, ama figür siluetle okunur ve göz yolu figüre gider.
- **S4 · Sessiz okuma.** Ses kapalıyken kahraman kare gösterilir ve "ne hissediyor?" sorusuna doğru duygu adı verilir. Yanıt anlatıcıya gerek duymaz.
- **S5 · Renk planı.** Sahnenin tek cümlelik bir renk planı ve tek bir vurgu rengi olur. Tek grade uygulanır. Ortalama doygunluk sahne içinde ±0,06 bandında kalır **[A]**.
- **S6 · Çıta (kahraman kare).** Yüzde iki tonlu form gölgesi, kenar ya da ortam ışığı ve duyguyla değişen kas çizgileri (alın, burun-dudak, göz altı) bulunur. Kare tek başına küçük resim (thumbnail) olabilecek güçtedir. Yüz `head3` parametrelerinden türetilir ve dönüş şeridiyle karşılaştırılır.
- **S7 · Süreklilik.** Duygu nesnesi (höyük, kol halkası, haç) sahnenin her ilgili karesinde görünür. Kimlik nesnelerinin ölçüsü sabittir (kol halkası = önkol × 1,25) **[A]**.

## 3. Kare düzeyi ölçütler

### 3a. Karakter (C) · G1
- C1 · Eylem pozu: Poz o anki fiili sessiz anlatır. "Kollar yanda, dik duruş" yalnızca bilinçli bekleme anında kullanılır.
- C2 · Bağlantı ve temas: Tutulan nesneyi el gerçekten kavrar. Sevgi, ayrılık ve şiddet anlarında temas noktası görünür (dudak alına, el bileğe).
- C3 · Eller: Varsayılan el `relax`, `fist` ya da `grip`. Gerekçesiz açık avuç yoktur. Yakın planda eldiven ikonu el kullanılmaz.
- C4 · Ölçek: Karakterler arası oran `SCALE` tablosuna ±%5 uyar **[A]**. Bebek, yetişkin kafa boyunun ≤ 1,6 katıdır.
- C5 · Kimlik: Karakter bağlamsız tanınır. Ragnar'da en az 3 kimlik öğesi görünür. Çocuk yüzünde yaşlılık çizgisi yoktur.
- C6 · Görünüm tutarlılığı: Önden, ¾, profil ve arka görünüm aynı kaş ve saç kütlesini taşır. Önplanda kullanılan arka görünüm model sayfasında onaylıdır.
- C7 · Çizgi: Aynı ölçekte kontur kalınlığı eşittir. Maske ya da kesim hatası yoktur (taşa gömülü beden gibi).

### 3b. Kompozisyon, ışık, renk (L) · G2
- L1 · Yerleşim: Odak üçte bir çizgisinde ya da bilinçli simetride. Ufuk kadrajı ortadan bölmez. Ana figür kenara < %8 yapışmaz.
- L2 · Açı: Anahtar karelerden en az biri dümdüz yandan değildir. Aynı yatay hatta 3'ten fazla öğe dizilmez.
- L3 · Derinlik: En az 5 katman ve atmosferik ayrım bulunur. Ön plan öğesi figürü kesmez.
- L4 · Doluluk: Düz, dokusuz alan kadrajın ≤ %35'idir **[A]**. Tekrar eden damgalarda boyut, ton ve aralık değişkenliği ≥ ±%15'tir.
- L5 · Işık kaynağı: Kaynağı belli tek bir anahtar ışık vardır.
- L6 · Işık figüre değer: Işık ve gölge yanı arasındaki fark ≥ 0,12 L **[A: figür maskesi]**. Arka planla ayrışma yoksa rim ışığı kullanılır.
- L7 · Zemin bağı: Her figür ve nesnenin yer ya da temas gölgesi vardır. Nesneler zemine "girer".
- L8 · Değer aralığı: L p95 − p5 ≥ 0,35 **[A]**. Kasıtlı karanlık karede p95 ≥ 0,30 olur ve odak çevresinden ≥ 0,15 L daha parlaktır.
- L9 · Göz yolu: Merkez–kenar parlaklık farkı ≥ 0 **[A]**. En yüksek kontrast odaktadır.
- L10 · Duygu vurgusu: Vurgu rengi odakta bulunur ve başka yerde tekrarlanmaz. Duyguya hizmet eden bir atmosfer efekti ≥ 2 katmanda görünür.

### 3c. Duygu ve ifade (E) · G3
- E1 · Üç bölge: Kaş, göz ve ağız aynı duyguyu söyler.
- E2 · Ayırt edici yüz: Aynı karede iki karakter aynı ifade şablonunu ya da aynı gözyaşını taşımaz. Kalabalıkta yüz, poz, boy ve ton değişkenleri bakımından en az 3 farklılık bulunur (klon yok).
- E3 · Fiziksel ipucu: Duygu gözyaşı, ıslaklık, titreme, kızarık göz kenarı, nefes gibi en az bir izle desteklenir.
- E4 · Göz yönü: Gözbebeği bir hedefe bakar. Kapalı göz yalnızca öpme, dua, ölüm gibi bilinçli anlarda kullanılır ve sahnenin ≤ %40'ında görülür.
- E5 · Sevimlilik süzgeci: Trajik sahnede pembe yanak lekesi, emoji ağız ya da "top" bebek kullanılmaz.

## 4. Puanlama ve eşik
- Her üye kendi alanında kareye 0–3 puan verir. 3 = Born in Lore çıtası, 2 = uygun ve küçük not, 1 = revize gerekir, 0 = işlevsiz. Toplam en fazla 9.
- **Kare SON ÇIKTIYA UYGUN:** R1–R8 yok **ve** her üyenin puanı ≥ 2 **ve** toplam ≥ 6. Kahraman karede toplam ≥ 7 ve G3 ≥ 2.
- **Kare YETERSİZ:** Bu koşullardan biri sağlanmıyorsa. Karar, ölçüt kodlarıyla yazılır (ör. `ivar_19.5: S1, C2, E5`).
- **Sahne UYGUN:** Kahraman kare UYGUN, S1–S7'nin tamamı evet ve karelerin ≥ %80'i UYGUN.
- Üyeler arasında ≥ 2 puan fark varsa gerekçe panoya yazılır. Uzlaşma yoksa düşük puan geçerli olur.

## 5. Kullanıcıya gitme koşulları
1. Her sahne sonunda kareler + kurul tablosu (puanlar, karar, ölçüt kodları) her durumda gider. Kurul ya da ana ajan kendi başına "onaylandı" demez.
2. YETERSİZ her kare için kurul 1–2 somut iyileştirme seçeneği önerir. Hangisinin uygulanacağını **kullanıcı seçer**.
3. Aşağıdaki durumlarda hemen kullanıcıya sorulur: uzlaşma yoksa; kare ya da çekim eklemek veya çıkarmak gerekiyorsa; genel bir stil değişikliği gerekiyorsa; yeni bir model sayfası gerekiyorsa; bir öneri CLAUDE.md sınırına yaklaşıyorsa.
4. Aynı kare 2 revizyon turundan sonra hâlâ YETERSİZ ise sorun sistem düzeyindedir (kukla ya da yüz motoru). Kullanıcıdan sistem kararı istenir.

## 6. Ham kare paketi (`kurul/<sahne>/`)
- `kare_<t>.png`: Anahtar kareler, 1920×1080, son çıktı kalitesinde. Kahraman kare adında `_KAHRAMAN` eki bulunur.
- `sahne.md`: S2 duygu cümlesi, S5 renk planı, kare listesi (zaman, kelime kilidi, plan ölçeği).
- `cast_strip.png`: Sahnedeki karakter kafaları aynı ölçekte, model sayfası kafasının yanında. Kahraman yüz için dönüş şeridi (0°, 45°, 90°, 180°).
- `olcum.csv` **[A]**: kare başına L p5/p95, merkez–kenar farkı, düz alan %, ortalama doygunluk, yüz kutusu yüksekliği %, `assert_attached` ve `SCALE` uyarıları.
- `kontrol_gri.png`: Bütün karelerin gri tonlu kontak tabakası (değer okuması).
- `kontrol_kucuk.png`: Bütün kareler 1/8 boyutta (240×135): siluet, göz yolu ve küçük resim testi.
- `kontrol_derinlik.png` (isteğe bağlı): Katmanlar ayrı renge boyanmış derinlik haritası.
- `pano.md`: G1, G2 ve G3 bölümleri, tartışma ve kurul tablosu.

## 7. Mevcut 5 sahnenin kurul kararı (19.11.2026)

| Sahne | Karar | En kritik 2 eksik |
|---|---|---|
| Yas (Athelstan'ın gömülmesi) v5 | YETERSİZ (kuruluş referansı) | S6: yüz düz maske, form gölgesi ve kas yok, pembe yanak lekesi (E5). R4: `yas_21.5` kopuk kılıç kolu, `yas_24.8` boyunsuz kafa. |
| Lagertha vedası v2 | YETERSİZ | R2: `veda_3`, `veda_8` ve `veda_16.5`'te ayrılık anında gülümseyen Lagertha. R3 + C2: `veda_21.8`'de Bjorn'da Ragnar'ın yarası, temas ve kol yok. |
| Athelstan'ın ölümü | YETERSİZ | S1: Floki'nin çatışması hiç yakın planda değil (`olum_12` uzak ve tam aydınlık). R7 + L6: `olum_23.5` neredeyse siyah, mum ışığı figürlere değmiyor (`olum_7`). |
| Ivar, nehir kıyısı | YETERSİZ | S1: Ragnar'ın yüzü sahnede hiç yakın plana girmiyor, doruk `ivar_14` geniş planda, `ivar_19.5` tüp kol. E5 + C4: emoji/top bebek ve ölçek hataları (`ivar_8`, `ivar_14`). |
| Paris'te sahte ölüm | YETERSİZ | S1 + E1: doruk `paris_16.3` uzak planda ve sırıtış yok. Şok yüzü `paris_18.9` gözleri kapalı, öfke gibi okunuyor. R5 + E2: `paris_3.4` döndürülmüş sprite, `paris_14` 6 klon taşıyıcı. |

## 8. Kullanıcıya gidecek yön kararları
1. **Kahraman kare yüzü:** Her sahnenin kahraman karesindeki yüz illüstrasyon kalitesinde ayrıca çizilsin mi? Yüz `head3` parametrelerinden türetilecek; form gölgesi, kas çizgileri, göz akı ve gözbebeği yönü eklenecek. Kukla şablonu geniş ve orta planlarda kalacak. *(Kurul önerisi: evet. Önce tek bir test karesi hazırlansın: `ivar_19.5` yerine Ragnar'ın ¾ yakın planı.)*
2. **Poz sistemi:** Genel `figure()` yerine sahneye özel poz fonksiyonlarına (yatma, yığılma, sarılma, kucaklama, nesne verme, dua) ve ortak `compose()` / `key_light` hattına geçilsin mi? Bu stil ve iş yükü bakımından genel bir değişiklik.
3. **Yeni model sayfaları:** Bebek, arka görünüm (Ragnar ve Lagertha), Paris'teki S3 tıraşlı Ragnar ve karakter başına ayrışan yüz kalıpları önce onaya gitsin mi?
4. **Kapsam:** Dört zayıf sahne (ve yasın R4 düzeltmeleri) baştan mı çizilecek, yoksa yalnızca YETERSİZ kareler mi düzeltilecek? Sahne renk planları G2 (d)4'teki gibi mi uygulanacak?

## 9. Nesne düzeyi değerlendirme (kullanıcı kuralı, 19.11.2026 15:06)
Kullanıcı: "Üretilecek her nesne kendi içinde değerlendirilsin. Örneğin kale çizilecekse tutarlı ve güzel dokulu bir kale mi, sahneyle uyumlu mu? Aynı şekilde el, kol ve bebek."
- Her sahnenin **önemli nesneleri** (karakter parçası, bebek, el, kol, silah, araç, yapı, mekân öğesi) kareye girmeden önce **nesne kartı** olarak tek başına çizilir: `kurul/<sahne>/nesneler/<ad>.png`. Kartta ön görünüm, sahnede kullanılacak açı, yakın detay ve ölçek çubuğu bulunur.
- Kurul her nesneyi şu ölçütlerle puanlar (0–3):
  - **N1 · Okunurluk:** Siluet ve küçük boy (1/8) kontrolünde nesne adıyla tanınıyor mu? (Kale "kale" diye, bebek "bebek" diye okunmalı.)
  - **N2 · Yapısal tutarlılık:** Parçalar birbirine bağlı ve mantıklı mı? Oranlar doğru mu? (El ve parmak sayısı, kolun omza bağlanması, surun burç–mazgal–kapı düzeni.)
  - **N3 · Doku ve malzeme:** Malzeme okunuyor mu (taş, ahşap, yün, deri, metal)? `r3/tex.py` dokuları ve ışık tarafı/gölge tarafı var mı?
  - **N4 · Ayrıntı yoğunluğu:** Nesne düz bir şekil mi, yoksa ikincil ayrıntılar var mı (kıvrım, dikiş, çatlak, perçin, tutam)?
  - **N5 · Sahne uyumu:** Renk planı, ışık yönü, çizgi kalınlığı ve stil sahneyle aynı mı? Ölçek komşu nesnelere göre doğru mu?
  - **N6 · Model tutarlılığı:** Aynı nesne başka sahnede de görünüyorsa (kol halkası, haç, Bjorn'un kalkanı) aynı mı?
  - **N7 · Eylem ve duygu uygunluğu (v1.1):** Nesne, sahnede yapacağı eylemin pozunda ve taşıyacağı ifadede de çizilmiş mi? Örneğin temas anı için gevşek ve parmağını sunan el (işaret eden el değil), kahraman an için bebeğin uyanık ve bakan yüzü. Nesne, trajik sahnede "oyuncak" etkisi bırakmıyor mu (plastik parlama, pembe leke, top kafa; E5)? *(Tekrar eden ders: kukla pozları, uyuyan ya da gülümseyen yüzler, işaret eden el.)*
- **Kart içeriği (v1.1, zorunlu):** (a) ön görünüm, (b) sahnede kullanılacak açı, (c) yakın detay, (d) **eylem pozu ve ifade varyantları** (N7), (e) etkileşen nesnelerle **ortak ölçek çubuğu**, (f) sahne arka planı ve grade'i üstünde **sahne önizlemesi**, (g) 1/8 okunurluk.
- **Nesne geçme eşiği:** N1–N6'nın her birinde ≥2 ve toplam ≥13/18, **ayrıca N7 ≥2** (ayrı kapı). R8 varsa nesne geçmez. Üyelerin puanları farklıysa her N için en düşük puan alınır. Geçemeyen nesne kareye girmez.
- Mekânlar "nesne seti" olarak değerlendirilir: mekânı tanımlayan en az 3 kimlik öğesi (ör. kale: sur + burç + kapı + mazgal + sancak; kilise: sütun + kemer + sunak + vitray/mum) olmadan mekân kartı geçmez.

## 10. Kendini eğiten kurul
- Her revizyondan sonra kurul üyeleri `kurul/DERSLER.md` dosyasına kendi alanında kısa, genellenebilir bir ders ekler: "Hata → neden → bundan sonra kontrol edeceğim madde".
- Her incelemeye başlamadan önce üyeler `DERSLER.md` ve bu standardı yeniden okur. Tekrarlayan dersler standarda yeni bir ölçüt olarak eklenir (standart sürümü artar: v1.1, v1.2…).
- Kullanıcının her talimatı `DERSLER.md` içinde "Kullanıcı" etiketiyle ayrıca kaydedilir. Kullanıcı talimatı ile kurul görüşü çelişirse kullanıcı talimatı geçerlidir.

### §8 ek · Kullanıcı kararları (19.11.2026 ~15:40)
- **Çıta:** "Temiz, gölgeli, sinematik 2D". Boyalı yüz dokusu hedef dışı.
- **Referans kare:** `test_ivar/hero_v4.png`. Kahraman karelerin ölçüsü budur:
  - Model yönü korunur, kafa aynalanmaz.
  - Işık yönlüdür; çekirdek gölge, ışık tarafında rim ve arka plandan koyulaştırma kullanılır.
  - Karede tek sıcak vurgu olur.
  - Duygu, bir etkileşim kompozitiyle taşınır (ör. bebeğin parmağı kavraması).
  - Ön plan, orta plan ve uzak plan katmanları bulunur.

### R9 · Katman sırası ve zemin teması (kullanıcı uyarısı, 19.11.2026 20:51)
Zemin, üstünde duran her nesneden (ev, araba, karakter, taş) **önce** çizilir. Hiçbir zemin öğesi (kar, çamur, su birikintisi) bir nesnenin tabanını örtemez.
Kurul her karede şunları ayrıca kontrol eder:
- Nesnenin taban çizgisi zemine oturuyor mu?
- Zemin, nesnenin üstüne çıkmış mı?
- Temas gölgesi var mı?
Bu kurallardan biri çiğnenirse kare **kesin red** alır.

### R10 · Ton ve iklim uyumu (kullanıcı, 19.11.2026 20:51)
Vikings sert iklimli bir dizi. Nesneler "çocuk çizgi filmi" sevimliliğinde çizilmez:
- Hayvanlar gerçekçi oranlı ve soluk/koyu renkli çizilir; kışlık kaba tüy, çamur ve yorgunluk gösterilir.
- Göz büyük ve parlak çizilmez.
- Ahşap ve demir yıpranmış görünür.
- Zemin gerçekçi doku ve ton kırılımıyla çizilir (donmuş çamur, kirli kar).

### R11 · Gövde her zaman modelden gelir (kullanıcı, 19.11.2026 22:30)
Diz çökme, kalkık kol, siluet ve gölge dahil hiçbir karakter gövdesi elle ya da eski kukla (`puppet`) parçalarıyla çizilmez. Hepsi `art3.figure` model gövdesinden üretilir. Kullanılabilecek bayraklar: `_kneel`, `_arm_up` + `_hand_extra`, `_carry_svg`, `_body_extra`, `_noarm`. Siluet ve gölge de bu gövdenin boyanmış hâlidir.
Kurul her karede şunu kontrol eder: "Bu gövde ve gölge, karakterin model hatlarıyla aynı mı?" Aynı değilse kare kesin red alır.

### R12 · Sahne yapılandırması: kalabalık, tören, kahraman nesnesi (kullanıcı, 19.11.2026 23:20)
1. **Ordu ve kalabalık:** 2–3 temel modelden rastgele türetilir (`bedel/kalabalik.py: soldier_spec`). Saç, sakal, giysi, miğfer, kalkan deseni ve silah değişir. Kalabalık 3 derinlik sırasıyla kurulur: uzakta küçük ve havada solmuş, önde büyük ve net. Sancak ve mızrak ormanı bulunur. "Birkaç kişi" ordu yerine geçmez.
2. **Tören ve ritüel sahneleri** (cenaze, taç giyme, kurban): dizideki biçim araştırılır. Sahnede en az 5 tören öğesi olur. Örnek, cenaze yığını: kafes kütük, oymalı köşe direkleri, kalkanlar, çiçek ve otlar, kefen ve örtü, mezar eşyaları, meşaleli halk.
3. **Kahraman nesneleri** görkemli çizilir: Ragnar'ın süslü sakallı baltası (`KL.BEARD_AXE`), işlemeli kabzalar. Sıradan bir kılıç kahramanın elinde durmaz.
4. **Siluet ve gölge yerine gerçek modeller** kullanılır. Karanlık sahnede model gövdesi ışık ve gölgeyle (`rim` + `shade_side`) aydınlatılır, düz siyaha boyanmaz.
5. Kurul her bölümde şunu sorar: "Bu kare dizideki aynı anın ihtişamına ve dolulukuna yaklaşıyor mu?"

## R13 · Ana nesne yakın kontrolü (20.11.2026; kullanıcı: "geminin başı çok komik duruyor")
Kontakt sayfası 960 px olduğundan küçük ama kritik ayrıntıları (pruva, silah, taht, taç, haç) seçemez. Her ana nesne için 1920 px karenin üstünden en az %200 büyütülmüş, yalnızca nesneyi içeren bir kırpma hazırlanır. Kurul bu kırpmayı ayrıca imzalar. Sorulacak sorular: gerçekçi mi, dizideki gibi görkemli ve tehditkâr mı, çizgi film gibi mi okunuyor (yuvarlak göz, ince dil, sivri tek tip diş, yılan gibi ince boyun)?
