# Kurul dersleri (kendini eğitme günlüğü)

Biçim: `- [Üye/Kullanıcı · tarih · sahne] Hata → neden → bundan sonra kontrol edilecek madde`

- [Kullanıcı · 19.11 · genel] Sahneler görsel olarak zayıf, duygu yok → kukla şablonu, yüzsüz doruklar, düz mekânlar → her sahnede kahraman kare ve sahneye özel poz.
- [Kullanıcı · 19.11 · genel] Mekânlarda öğeler eksik (Paris'te kale olduğu bile belirsiz) → mekân kimlik öğeleri yok, doku yok → her mekân nesne seti kartıyla, en az 3 kimlik öğesi ve dokuyla (§9).
- [Kullanıcı · 19.11 · genel] Her nesne kendi içinde değerlendirilsin (kale, el, kol, bebek) → nesne kartı + N1–N6 (§9).
- [Kullanıcı · 19.11 · Ivar] Bebeğin görünümü iyileştirilsin → bebek "emoji daire" → bebek nesne kartı: bebek oranları (büyük kafa, tombul yanak, küçük burun), dokulu yün kundak, görünen el.
- [G1 · 19.11 · test_ivar] Elsiz, gövdeye bağlı olmayan kol → poz parçası tek başına çizilmiş → her uzuv omza/gövdeye bağlanır, ucunda el olur (R4).
- [G1 · 19.11 · test_ivar] Kırışık kazınmış kafa derisine düştü → yüz çizgileri bölge sınırı bilmiyor → yüz çizgileri yalnız çıplak cilt bölgesine (R1).
- [G2 · 19.11 · test_ivar] Form gölgesi düz perde → doğrusal degrade → çekirdek gölge şekilleri (kaş altı, burun, elmacık, sakal altı).
- [G2 · 19.11 · test_ivar nesne] Altın halka ahşap gibi, yün kundak kot gibi okundu → malzeme yalnız gürültüyle taklit edildi, değer yapısı (öz, orta, specular) ve malzeme geometrisi (ilmek, blok, tahta) yok → her malzemede önce değer yapısı ve geometri, gürültü en son ve düşük kontrastla; kartta 1× ve 1/8 doku kontrolü.
- [G2 · 19.11 · test_ivar nesne] Nesne sıcak kâğıtta güzel, sahnede kayboluyor (halka zeytine döndü) → kart grade'siz değerlendirildi → her nesne kartında sahne arka planı ve grade önizlemesi; vurgu nesnesi grade'den sonra çizilir ya da grade dışında tutulur.
- [G1 · 19.11 · test_ivar nesne] Kimlik dövmesi model sayfasından farklı (⊕) çizildi → nesne kartı model fonksiyonunu çağırmak yerine yeniden çizdi → kimlik öğeleri (knot_mark, kol halkası, broş, haç) yalnızca tek kaynaktan (`art3`/`props.py`) çağrılır; kartta model sayfasıyla yan yana kontrol edilir (N6).
- [G1 · 19.11 · test_ivar nesne] Bebek yetişkin kuralıyla çizildi (alın geniş, ince uzun kol, parmaklar yumruğun üstünde) ve sevimlilik izleri (pembe yanak, parlama) kaldı → yaş oranı tablosu yok → bebek/çocuk için oran kontrolü: en geniş yer yanak, kol ≤ 0,8 kafa yarıçapı, parmaklar avucun ön yüzünde; trajik sahnede E5 süzgeci nesne kartında da uygulanır.
- [G3 · 19.11 · test_ivar/nesneler] Bebek uyuyor, Ragnar'ın eli işaret ediyor; nesneler tek başına düzgün ama temas anına hizmet etmiyor → nesne kartı nesneyi "nötr pozda" çiziyor, sahnedeki eylemi ve ifadeyi değil → her kartta sahnedeki eylem pozu, ifade varyantı ve etkileşen nesneyle ortak ölçek bulunur (standart v1.1, N7).
- [G3 · 19.11 · test_ivar/nesneler] Önkol dövmesi ⊕ olarak uydurulmuş (model: üç halkalı düğüm). Bu, Tur 17 sızması ve veda_21.8 yarasından sonra **üçüncü** kimlik hatası → kimlik öğeleri parça parça elle yeniden çiziliyor → kimlik öğesi yalnızca model kaynağından çağrılır; incelemede kaynakla yan yana karşılaştırılır (standart v1.1, R8).
- [G2 · 19.11 · test_ivar nesne v2] Form ışığı kola uygulandı, ele uygulanmadı; gölgeler sıcak kaldı → düzeltme nesne listesi yerine 'ana parça' üzerinden uygulandı → her alt parçada (el, parmak, kıvrım) ışık–gölge ölçümü yapılır ve soğuk sahnede gölge rengi ortamdan alınır.
- [G3 · 19.11 · test_ivar/nesneler v2] İşe yarayan: nesneler tek tek değil, **etkileşim anının kompoziti** olarak çizildi (kavrama kartı, ortak ölçek çubuğu, sahne önizlemesi). Duygu cümlesi ses olmadan okundu ve v1'deki 7 ve 10 puan 12 ve 13'e çıktı → bundan sonra her sahnede duygu vuruşunu taşıyan nesneler önce birlikte, kahraman anın kompozitinde ve grade altında kurula gelir. Tek başına güzel nesne yeterli değildir.
- [Kullanıcı · 19.11 15:15 · test_ivar/nesneler] Nesne kartı v2: ortak ölçek, kavrama kompoziti ve sahne önizlemesi kullanıcıya yeterli geldi ("Yeterli, devam"). Kurul puanı eşiğin 1 puan altında olsa da kullanıcı onayı geçerli → kalan düzeltmeler bekletilmez, bir sonraki üretime (hero v2) taşınır. Kullanıcının yeterlilik çıtası, kurulun nesne eşiğinden biraz daha esnek: kurul bu farkı engel olarak değil iş listesi olarak sunsun.
- [G3 (G1 alanı) · 19.11 · test_ivar hero v2] Kafa `scale(-1)` ile aynalandı; yara izi ve örgü öbür tarafa geçti → asimetrik kimlik işaretleri geometriyle birlikte çevrildi → yön değiştirmek için `facing` parametresi kullanılır, kimlik işaretleri model tarafında kalır; incelemede yara ve örgü tarafı model sayfasıyla karşılaştırılır.

- **[Kullanıcı, 19.11 ~15:40]** Hero v3 onaylandı, 4 küçük madde düzeltilip v4'e geçildi. Çıta "temiz, gölgeli, sinematik 2D" olarak belirlendi. Kurulun 7/9 eşiği kullanıcıyla uyumlu çıktı.
- **[Uygulayıcı]** Asimetrik kimlik işaretli bir kahramanı çevirmek gerekiyorsa kafa aynalanmaz, kompozisyon ters kurulur. Işık da ona göre taşınır.
- **[Kullanıcı, 19.11 akşam]** Yakın planda bile karakter gövdesi model gövdesinden (`art3.figure`) gelir; uydurma gövde kullanılmaz. Yan karakter, başka bir karakterin renk değişikliği olamaz: Aslaug, Lagertha'dan saç biçimi, renk ve aksesuarla ayrışmalı.
- **[Kullanıcı, 19.11 20:51 · KURULA UYARI]** Kattegat v3'te zemin evlerin üstüne çıktı ve kurul bunu yakalayamadı. Artık her incelemede R9 (katman sırası ve zemin teması) ayrı bir madde olarak kontrol edilecek. R10 eklendi: sert iklim tonu; sevimli ya da çizgi film görünümlü hayvan ve nesne kullanılmaz.
- **[Kullanıcı, 19.11 23:20 · KURULA ÖĞRETİ]**
  - Savaş sahnesinde ordular ihtişamlı olmalı; rastgele türetilmiş çok sayıda model kullanılır.
  - Lagertha'nın ateşi yaktığı cenaze yığını dizideki gibi süslü ve görkemli olmalı.
  - Ragnar'ın elinde sıradan kılıç değil, görkemli bir Viking baltası olmalı.
  - Gölge ve siluet yerine gerçek modeller kullanılır.
  - Hepsi R12'ye yazıldı. Kurul ve uygulayıcı her bölümün başında R8–R12'yi kontrol listesi olarak okur.

## Bölüm I (20.11): öz değerlendirme turu
- Gemi tek kaynaktan gelir (`bati/gemi.py`): inşaat aşaması `built` ile verilir, aynı gemi fırtınada tamamlanmış hâliyle görünür. Kahraman nesneler dizideki ihtişamla çizilir: bindirme kaplama, ejder başı, çizgili yelken, kalkan sırası, kürekler.
- Kurul ikinci turda ham hataların yanı sıra "kaliteyi artıracak detay" da arar: ışık hüzmesinin hedefe düşmesi, rim ışığı, köpük ve serpinti, yangın, duman, kıvılcım, yere düşmüş nesneler.
- Keşiş gibi uzun giysili karakterlerde model gövdesinin üstüne cübbe katmanı eklenir (R11 korunur).

## Anlatım öz değerlendirmesi (20.11; kullanıcı: "anlatımlar çok daha açıklayıcı ve net olmalı")
- Her bölümün anlatımı, seslendirmeden önce hikâye ajanından geçer. Ajan dört şeye bakar: (1) dizi doğruluğu, belirsiz noktalar web'de teyit edilir; (2) "hiç izlememiş biri anlar mı" 1–5 puanı, 4'ün altındaki satır yeniden yazılır; (3) 12 kelimeyi aşan cümle bölünür; (4) kim, nerede, neden soruları cevaplanmış mı.
- Ünvan ve kavramlar ilk geçtiklerinde tek cümleyle açıklanır (jarl, holmgang, güneş taşı). Her olayın nedeni söylenir ("çünkü yasağını çiğnedin").

## KÖK NEDEN ANALİZİ: neden vasat kareler geçti? (20.11.2026, kullanıcı v3'ü "harika" buldu)
Ajanlara: her yeni sahnede bu listeyi oku.

1. **Ara kare küçümsendi.** Ek görüntü ve geçiş kareleri "kısa süre görünecek" diye yer tutucu gibi çizildi (kutu kulübe, çubuk bacaklı keçi, düz duvar). Doğrusu: ekranda 2 saniye kalan kare de ana sahnenin çıtasını taşır.
2. **Ölçek yanılgısı.** 960 px kontakt sayfası küçük nesneyi (pruva, el, hayvan) gizledi. Çözüm: R13 kırpması (%200).
3. **Kendi işini notlamak.** Üreten kişi kendi karesini "yeterli" saydı. Kurul da genel sorular sordu ve referans kareyle yan yana karşılaştırma yapmadı. Doğrusu: her kare referansla (`hero_v4`, `d3`, `e4`, `e7`, `v3/kontakt_v3_960.png`) yan yana konur ve "bu kare referansın yanında zayıf mı?" diye sorulur.
4. **Brif belirsizdi.** "Fakir köy" yazıp bırakmak düz şekiller doğurdu. v3'ü başarılı yapan şey, her kare için 6–12 somut ayrıntının önceden listelenmesi oldu (yamalı saz, cılız tavuk, çamurda ayak izi...). Yeni brif şablonu: `BRIEF_SABLON.md`.
5. **Süreç kısaltıldı.** Hız uğruna kullanıcı onayı atlandı ve animatik erken üretildi. Kural: taslak → kullanıcı → ancak sonra ses ve video.
6. **Katman ve derinlik düşünülmedi.** Tek düzlemde çizilen kareler ölü durdu. v3'te en az 4 katman vardı: ön plan çerçevesi, atmosfer, orta plan, arka plan.
7. **Işık sonradan eklendi.** Işık kaynağı baştan seçilmeyince düz renkli kareler çıktı. v3'te her kare bir ışık kararıyla başladı: bulut yırtığı, meşale, pencere hüzmesi, ay.
8. **Anlatım içeriden yazıldı.** Diziyi bilen biri için kısa satırlar yazıldı. Doğrusu: hiç izlememiş biri için kim, nerede, neden; kavramlar ilk geçtikleri yerde açıklanır.
9. **Ses görüntüyü bastırdı.** Gök gürültüsü bir satırı yuttu. Whisper testi zorunlu; geniş bantlı efektler satır aralarına konur.
10. **Önceki hatalar** (zemin evlerin üstünde, uydurma gövde, silüet, aynalanmış kimlik) aynı kökten çıktı: kontrol listesi yerine göze güvenmek. Liste: `GORSEL_STANDART.md` R8–R13 + `BRIEF_bolum1_v3.md`.
