# Dinamik anlatım: söylenen her şey ekranda yaşanır

Bu belge, Ragnar videosundan sonra kullanıcının verdiği üç geri bildirimi, ölçülebilir ve denetlenebilir kurallara çevirir. Yeni videonun **en önemli belgesi** budur. Her bölüm örgüsü, sahne dökümü ve kurul incelemesi bu kurallara göre yapılır.

## 0. Kullanıcının geri bildirimi (26.11.2026, birebir)

> 1. Çok story telling şeklinde kaldı ve hikaye dinamik anlatılmadı. Her sahnede her söylenen cümlenin hayata geçtiği daha hareketli bir senaryo istiyorum.
> 2. Her söylenen cümlede ekrana o cümlenin öğesi gelmedi. Çoğu mümkün mertebe hareketli olmalı. Sahneler arası anlamsal geçişler olmalı. Örneğin o an söylenen öğe evin penceresinde belirsin, sonra gelecek sahne pencereden devam etsin. Akıcı ve dinamik bir anlatım sunsun.
> 3. Sahnelerde duygular ve hissiyat aktarılsın, bunun için görsel öğelerden faydalanılsın.

### Ragnar'da neden böyle oldu (kök neden)
| Belirti | Kod/süreçteki nedeni |
|---|---|
| "Hikâye anlatılıyor, yaşanmıyor" | Her çekim **tek bir düzleştirilmiş kareydi** (`FR[k]().makeImageSnapshot()`), üstüne yavaş zoom (Ken Burns) eklendi. Kare içinde hiçbir şey olmuyordu. |
| Cümlenin öğesi ekrana gelmedi | Plan birimi "kare"ydi. Bir kare 1–3 cümle taşıdı, cümleler ise kareye uyduruldu. Kelime kilidi yalnızca birkaç vurgu anındaydı. |
| Geçişler kopuk | Her çekim arasında 6 karelik **siyaha kararma** vardı (`dip = 6`). Anlamsal bağ hiç kurulmadı. |
| Duygu zayıf | Duygu çoğunlukla yüz ifadesine ve sabit grade'e bırakıldı. Işık, hava, renk ve kamera duyguyla birlikte **değişmedi**. |

**Yeni ilke:** Planlama birimi kare değil **cümle**dir. Her cümle bir eylemdir. Çekim, durağan bir resim değil bir **sahne grafiğidir**. Öğeler katman katman yaşar, kelime gelince girer ve hareket eder. Çekimler birbirine bir nesne, biçim ya da hareket üzerinden **akar**.

---

## 1. Altın kurallar (D1–D10)

`motor/dokum_kontrol.py` bu kuralların ölçülebilir olanlarını otomatik denetler. ✗ hata varsa döküm kullanıcıya gitmez.

| Kod | Kural | Ölçüt |
|---|---|---|
| **D1 · Cümle = görüntü** | Anlatımdaki her cümlenin ekranda somut bir karşılığı vardır: nesne, eylem, yer, kişi ya da sembol. Bu karşılık cümledeki bir **kelimeye kilitlenir**. | Her cümlede ≥ 1 kelime kilidi. Kilitli öğe kelimenin başlangıcından en çok 0,15 sn önce girer, en geç 0,1 sn sonra. |
| **D2 · Her çekim hareket eder** | Her çekimde üç tür hareket bulunur: (a) sahneye **giren ya da eylem yapan** en az bir öğe, (b) bir **kamera** hareketi, (c) sürekli **ikincil** yaşam hareketi (nefes, salınım, duman, su, saç, pelerin, alev, toz). | (a) ve (b) zorunlu, (c) uyarı. |
| **D3 · Ölü süre yok** | Ekranda hiçbir şey olmadan 3 saniye geçmez. | Çekim süresi / 3 ≤ olay sayısı. Ses kapalı izlenince "bu 3 sn'de ne oldu?" sorusunun bir cevabı olmalı. |
| **D4 · Geçişler anlamlıdır** | Çekimler arasındaki geçişlerin **≥ %60'ı anlamsal** olur (§3). Sert kesme yalnızca bilinçli bir şok, ritim ya da ses vuruşunda kullanılır. **Siyaha kararma yalnızca bölüm sonunda** kullanılır. | Oran otomatik ölçülür. |
| **D5 · Geçişin bir bağı vardır** | Her anlamsal geçişte "A'daki **ne**, B'deki **ne**ye bağlanıyor ve **neden**" bir cümleyle yazılır. Geçişte kullanılan öğe A'da (ve gerekiyorsa B'de) bulunur. | `bag`, `oge_a` ve `oge_b` kontrol edilir. |
| **D6 · Duygu görünür** | Her çekimin bir duygusu (`duygu`) ve onu taşıyan bir görsel öğesi (`duygu_tasiyici`) vardır. Duygu bir çekimin içinde değişiyorsa ışık, renk ve kamera da o anda değişir. | `03_DUYGU_DILI.md` kalıpları. |
| **D7 · Plan çeşitliliği** | Art arda 4 çekim aynı plan ölçeğinde olmaz. Duygu dorukları yakın planda ya da bilinçli bir yalnızlık planında verilir. | Uyarı. |
| **D8 · Kısa cümle** | Bir cümle en fazla 12 kelimedir. Bir çekimde en fazla 2 cümle bulunur. | Uyarı. |
| **D9 · Vurucu an** | Vurucu cümle (bölümün can alıcı cümlesi) görsel bir efektle (flaş, sarsıntı, ışık patlaması, ağır çekim) ve bir ses olayıyla birlikte gelir. | `vurucu: true` → `vfx` ve `ses.efekt` zorunlu. |
| **D10 · Süreklilik** | Bir nesne iki çekime yayılıyorsa (taşıma, eşleşme) aynı anda iki yerde görünmez (R6). Kimlik nesnesi her yerde aynı kaynaktan çizilir. | Motor, `NesneTasi` sırasında kaynak ve hedef öğeyi gizler. |

---

## 2. Cümleden çekime: yazım yöntemi

Her cümle için senarist şu dört soruyu yanıtlar ve yanıtları sahne dökümüne yazar:

1. **Ne görünür?** Cümlenin ekrandaki karşılığı. Soyut cümle somutlaştırılır:
   - "Zengin oluyorsun" → sandığa altın dökülür, sikkeler sayılır.
   - "Herkes sana güveniyor" → kalabalığın başları sana döner, biri kılıcını önüne koyar.
   - "Yıllar geçiyor" → aynı pencerede mevsim değişir, kar düşer, çiçek açar, çocuk boyu uzar.
2. **Hangi kelimede?** Kilit kelime çoğunlukla cümlenin adı ya da fiilidir. Öğe o kelimenin başında girer.
3. **Nasıl girer ya da ne yapar?** Hareket sözlüğünden (§4) bir giriş seçilir. Eylem ise karakterin yaptığı küçük hareket olur: dön, kaldır, uzat, düş, kırp.
4. **Bir sonraki cümleye nasıl akar?** Bu cümlenin son görüntüsü, bir sonraki cümlenin ilk görüntüsüne hangi öğe üzerinden bağlanır?

### Örnek: anlatıdan sahne dökümüne
Anlatım: *"Bir gece babanın halkası pencerede parlıyor. Yıllar sonra aynı halka savaşa gidiyor."*

| Cümle | Görünen | Kilit | Giriş ya da eylem | Kamera | Akış |
|---|---|---|---|---|---|
| "Bir gece babanın halkası pencerede parlıyor." | Gece, çiftlik evi. Pencerede halka mum ışığında parlıyor. | "pencerede" → ışık, "parlıyor" → halka | Işık `parla`, halka `parla` + ışık patlaması | Pencereye doğru yavaş itme | **Maske:** pencereden içeri |
| (iç mekân, aynı cümlenin devamı ya da sessiz 1 sn) | Masada halka, mum | — | Halka hafifçe döner | Halkaya itme | **Nesne taşıma:** halka uçar |
| "Yıllar sonra aynı halka savaşa gidiyor." | Fırtınalı kıyı, halka bir savaşçının koluna oturur | "halka" → kola oturur, "savaşa" → şimşek | `eylem`, şimşek `belir` | Geri çekilme + sarsıntı | — |

Bu örnek `motor/ornek/demo.py` ve `sablonlar/sahne_dokumu_ornek.json` olarak çalışır.

---

## 3. Anlamsal geçiş kataloğu (`motor/gecis.py`)

Her geçiş iki çekimi bir **öğe**, bir **biçim** ya da bir **hareket** üzerinden bağlar. Seçim tablosu:

| Geçiş | Motor | Ne zaman | Örnek |
|---|---|---|---|
| **Maske (içinden geçiş)** | `Maske("pencere", boyut, sekil)` | Dışarıdan içeriye, bir mekândan iç dünyaya, bir çerçeveden sahneye geçerken. Öğe A'da bir açıklıktır. | Pencere → iç mekân. Kapı → salon. Göz bebeği → anı. Kalkanın içi → savaş. Ateşin ağzı → cehennem/rüya. Mektup zarfı → mektubun dünyası. |
| **Nesne taşıma** | `NesneTasi("halka", "halka", ciz)` | Bir nesne hikâyede yer ya da zaman değiştiriyorsa: kimlik nesnesi, miras, mektup, sikke, silah. | Halka masadan savaş alanına. Taç bir kafadan ötekine. Ok yaydan hedefe ve hedefin olduğu sahneye. |
| **Biçim eşleşmesi** | `Eslesme("ay", "kalkan")` | Benzer biçimli iki öğe zaman ya da yer atlamasını bağlar. | Ay → yuvarlak kalkan. Göz → güneş. Bebek eli → yetişkin eli (aynı hareket). Mum alevi → yanan köy. |
| **Zoom içinden** | `ZoomIcinden("goz")` | Anıya, rüyaya, düşünceye ya da kehanete girerken; bir şeyin "içine" bakılırken. | Gözün içine dalış → çocukluk anısı. Kehanet kemiklerine dalış → gelecek. |
| **Ön plan silme** | `OnPlanSil(ciz_perde)` | Akış içinde yer değişirken, hareket sürerken. | Önden geçen direk, yelken, at, kalabalık, duman perdesi. Arkasından yeni sahne çıkar. |
| **Savurma** | `Savurma(yon)` | Hız, kovalama, ani karar, kısa zaman atlaması. | Kılıç savrulur, kamera da onunla savrulur ve yeni savaşa düşer. |
| **Sert kesme** | `Kes()` | Şok, sessizlik, ses vuruşuyla eşleşen kesme. Gerekçesi yazılır. | Ölüm haberi. Darbe sesinde siyah çerçeve. |
| **Kararma** | `Karart()` | **Yalnızca** bölüm sonu ya da büyük zaman atlaması. | Bölüm başlığından önce. |

**Geçiş tasarlarken sorulacak sorular:** A'nın son görüntüsünde göz nerede? B'nin ilk görüntüsünde göz nerede olmalı? İkisi aynı noktaya düşüyorsa geçiş akıcı olur. Bir geçiş 0,6–1,3 saniye sürer. Hareket yönü korunur: soldan sağa akan bir hikâye, sağa doğru geçişle devam eder.

**Ses de geçer:** Ses kesme noktasından 0,3–0,5 sn önce başlar (J-cut). Örneğin pencereden girmeden önce içerideki ateşin çıtırtısı duyulur.

---

## 4. Hareket sözlüğü

### Giriş kalıpları (`sahne._giris`)
`pop` (taşarak büyür) · `dus` (düşer ve seker) · `kay_sol` / `kay_sag` · `yuksel` (aşağıdan yükselir) · `belir` (saydamlıktan) · `parla` (yanar, ışık patlaması) · `ciz` (soldan sağa çizilir: harita, yol, yazı, kan izi yerine iz) · `buyu` (küçükten büyür).

### İkincil yaşam hareketi (`sahne.ikincil`)
`nefes` (bütün karakterler) · `salin` (bitki, pelerin, asılı nesne) · `titre` (korku, soğuk, öfke) · `suz` (havada asılı ay, kuş, toz) · `alev` (mum, meşale, ateş).

### Karakter eylemleri
Kelimeye kilitli küçük eylemler `Oge.eylemler` ile verilir: baş çevirme, el kaldırma, nesne uzatma, diz çökme, yumruk sıkma, göz kırpma, gözyaşı düşmesi. Ragnar'daki `ivar2/frames.py: live()` fikri burada her öğeye genelleştirildi.
**Kural:** Bir karakter konuşulduğu sırada ekrandaysa kımıldar. Hiçbir karakter "fotoğraf" gibi durmaz.

### Kamera dili
| Hareket | Anlamı |
|---|---|
| Yavaş itme (push-in) | Önem, içe dönüş, karar anı |
| Geri çekilme (pull-out) | Yalnızlık, ölçeğin ortaya çıkışı, kayıp |
| Yukarı tilt | Umut, güç, tanrısal olan |
| Aşağı tilt | Çöküş, yenilgi |
| Yana takip | Yolculuk, akış |
| Sarsıntı | Darbe, deprem, öfke, şok |
| Eğik kadraj | Huzursuzluk, delilik |
| Sabit | Gerilim (bir şeyin olmasını beklemek) ya da yas |

**Paralaks:** Her çekim en az 4 derinlik katmanıyla kurulur: gök 0.05, uzak 0.3, orta 0.6–0.8, ana düzlem 1, ön plan 1.3–1.5. Kamera kaydığında bu katmanlar farklı hızda kayar ve düz bir kare "2,5 boyutlu" görünür.

---

## 5. Bölüm ritmi
- Hafif bölümler hızlıdır: çekim 2,5–4 sn, geçişlerin çoğu nesne taşıma ve savurma.
- Trajik anlar yavaştır: çekim 4–7 sn, ama yine de ölü süre olmaz. Hareket küçülür (nefes, gözyaşı, yağmur, mum söner) ama durmaz. Geçişler biçim eşleşmesi ya da sert kesme olur, sonra sessizlik gelir.
- Her bölüm görsel bir **motifle** açılır ve kapanır (aynı pencere, aynı halka, aynı ağaç). Böylece bölümler birbirine bağlanır.

## 6. Denetim (her bölümde)
1. `python3 motor/dokum_kontrol.py projeler/<ad>/dokum/bolum_X.json` → GEÇTİ olmalı.
2. Animatik sessiz izlenir. Her 3 saniyede bir "ne oldu?" sorusunun cevabı not edilir. Cevabı olmayan aralık D3 ihlalidir.
3. Animatik sesli izlenir. Her cümlede "söylenen şey o anda ekranda mı?" diye bakılır. Gecikme 0,3 sn'yi aşıyorsa kilit düzeltilir.
4. Geçiş listesi çıkarılır: her geçişin bağ cümlesi okunur. Bağ zorlama görünüyorsa geçiş değiştirilir.
