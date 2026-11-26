# Duygu dili: hissiyat görsel öğelerle taşınır

Kullanıcı geri bildirimi 3: *"Sahnelerde duygular ve hissiyat aktarılsın, bunun için görsel öğelerden faydalanılsın."*

Duygu yalnızca yüzle taşınmaz. Bir sahnenin duygusu **yedi kanaldan** birlikte verilir. Bir kanal duyguyu söylemiyorsa en azından ona karşı çıkmamalıdır.

## 1. Yedi kanal
| Kanal | Ne kullanılır |
|---|---|
| **Yüz ve beden** | Kaş, göz, ağız aynı duyguyu söyler (E1). Beden dili: omuz düşük ya da dik, el yumruk ya da gevşek, mesafe yakın ya da uzak. Gözyaşı, titreme, nefes görünür (E3). |
| **Işık** | Kaynağı belli tek anahtar ışık. Sıcak ya da soğuk, sert ya da yumuşak, yüksek ya da alçak. Duygu değişince ışık **sahnede değişir**: mum söner, bulut güneşi kapatır, ateş harlanır. |
| **Renk (grade)** | `motor/duygu.py` kalıbı: doygunluk, sıcaklık, parlaklık, kontrast, vinyet. Tek vurgu rengi odakta durur. |
| **Hava ve atmosfer** | Yağmur, kar, sis, rüzgâr, toz, kül, ateş böceği. Hava duyguyla değişir ("içindeki fırtına" gerçek fırtınaya dönüşür). |
| **Kamera ve kadraj** | Mesafe (yakınlık = içtenlik), açı (alt açı = güç, üst açı = küçüklük), boşluk (figürün çevresindeki boş alan = yalnızlık), hareket (`02 §4`). |
| **Sembol nesne** | Duygu bir nesneye yüklenir ve nesnenin durumu değişir: çiçek solar, mum söner, halka çıkarılır, kapı kapanır, kuzgun konar. |
| **Ses** | Müzik kipi, sessizlik (HUSH), tek bir enstrüman, ortam sesinin çekilmesi. Duygu doruğunda ses azalır, artmaz. |

## 2. Duygu kalıpları (`motor/duygu.py: KALIP`)
| Duygu | Işık ve renk | Kamera | Atmosfer | Sembol önerileri |
|---|---|---|---|---|
| huzur | Sıcak altın, yumuşak, yüksek doygunluk | Yavaş kayma, geniş | Toz zerreleri, polen | Ocak, buğday, çocuk gülüşü |
| mutluluk | Parlak amber, yumuşak gölge | Hafif yukarı kalkış | Işık zerreleri | Uçuşan saç, kucaklaşma |
| merak | Nötr, serin vurgu | Odağa yavaş itme | İnce sis | Ufuk, harita, kapı aralığı |
| gerilim | Soğuk, yüksek kontrast, karanlık köşeler | Çok yavaş itme, alçak açı | Sis, uçan kül | Gölgede bekleyen figür, gerilen ip |
| korku | Mavi-gri, sert gölge | Ani zoom, eğik kadraj | Yağmur, şimşek | Titreyen mum, açılan kapı |
| öfke | Kırmızı-turuncu, sert | Sert kesme, sarsıntı | Kıvılcım, duman | Yumruk, kırılan nesne, ateş |
| zafer | Altın, yüksek ışık | Alt açı, büyüyen geri çekilme | Kıvılcım, sancak | Kaldırılan silah, taç |
| yas | Doygunluk ≈ %50, soğuk, ağır vinyet | Durağan ya da çok yavaş geri çekilme, boş alan | Yağmur ya da kar, düşen yaprak | Boş sandalye, sönen mum, yere bırakılan nesne |
| yalnızlık | Soğuk, düşük doygunluk | Geniş planda küçük figür | Kar, sis | Tek ağaç, boş yol |
| umut | Karanlıktan ışığa | Yukarı tilt | Işık hüzmesi | Doğan güneş, yeşeren filiz |
| yorgunluk | Soluk, toprak tonu | Ağır, gecikmeli takip | Toz, duman | Düşen omuz, bırakılan silah |

## 3. Duygu dönüşümü (çekim içinde)
Duygunun **değiştiği an** sahnenin en güçlü anıdır. Bu an kelimeye kilitlenir ve bütün kanallar aynı anda döner:
```python
ck.duygu = Duygu("huzur").gecis("yas", t0=ck.k("öldü"), sure=1.5)
```
Örnek: Çocuklarla oynayan bir baba (huzur). "Ama hastalık geliyor" cümlesinde bulut güneşi kapatır, renk solar, rüzgâr çıkar, çocuğun elindeki çiçek düşer, kamera geri çekilir ve müzik tek bir notaya iner.

## 4. Duygu cümlesi (her sahnede zorunlu, S2'nin genişlemiş hâli)
> Seyirci **X** hisseder, çünkü **[yüz/beden]**'de **Y**'yi, **[ışık/renk/hava]**'da **Z**'yi ve **[sembol nesne]**'nin **W** olduğunu görür.

Sessiz okuma testi (S4): Ses kapalıyken kahraman kare ve duygu dönüşüm anı izletilir. Duygu adı anlatıcı olmadan doğru söylenebilmelidir.

## 5. Yasaklar
- Trajik sahnede sevimlilik izleri kullanılmaz: pembe yanak, emoji ağız, top bebek (E5).
- Kan ve vahşet gösterilmez. Acı; ışık, sembol ve yüzle anlatılır.
- Duygu doruğunda ses yükseltilmez: ortam sesi çekilir, anlatım tek başına kalır.
- Gözü kapalı gülüş küçük boyutta öfke gibi okunur. Gözler açık çizilir.
