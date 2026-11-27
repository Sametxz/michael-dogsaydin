# Kurul dersleri (Michael Scofield)

Her kurul turu sonunda 1–3 genellenebilir ders eklenir. Kalıcı olanlar `studyo/docs/06_DERSLER.md`'ye taşınır.

## Tur 7 · 26.11.2026 · A-Y & A-Ç v2 Model Kartları
- **Paralel yaş/varyant üretimi:** Aynı karakterin farklı yaşlarını paralel çizen ajanlar, ortak kontur kalınlığı, göz oranı ve yüz gölge düzlemi şablonunu kilitlemeden üretime çıkmamalıdır.
- **Çocuk karakterde R10 sınırı:** Yaş farkı yuvarlak/parlak çizgi film gözleriyle değil; baş-gövde oranı, yumuşak çene hattı ve saç formuyla verilir.
- **R13 kapsamı:** %200 kırpma kartlarına yüz/boyun dışında karakterin ana kimlik öğesi (ör. özgün önkol dövmesi) de bir panel olarak eklenmelidir.
- **Kısa kazınmış saç (buzzcut):** Düz koyu dolgu yerine şakak fade'i + ince stipple dokusu kullanıldığında karakter portresi R13 %200 kırpmasında ciddi kalite sıçraması yapar.

## Tur 9 · 26.11.2026 · Lincoln (A-L) & Sara (A-S) v1 Model Kartları
- **Ortak kilit şablonun gücü:** A-Y v3'ün kontur, göz kapağı ve düzlem gölge kuralları referans alındığında, yeni karakterler ilk turda (v1) sıfır stil kopukluğuyla çıkabiliyor.
- **Uzun saçta R13 detayı:** Uzun/orta boy saç uçları küt tüp şeklinde bitirilmemeli; %200 kırpmada hafif inceltme (*taper*) ile organik form korunmalıdır.

## Tur 10 · 26.11.2026 · Sara v2 & Ana Mekânlar v1
- **Sıcak-soğuk mekân ayrımı:** Aynı yapı içindeki güven mekânını (Revir) tehdit mekânından (Hücre) keskin palet değişimiyle (amber-krem vs. soğuk yeşil-mavi) ayırmak duyguyu diyalogsuz taşır.
- **Çekicilik vs. R10 sınırı:** Kadın karakterde sıcaklık ve zarafet gözleri büyüterek değil; yumuşak dudak/elmacık tonu, zarif kirpik hattı ve doğal inceltilmiş (*tapered*) saç formuyla sağlanır.

## Tur 17 · 26.11.2026 · Bölüm I Yüksek Detay İngilizce Sahne Setleri (V1 · V2 · V3)
- **Çoklu sahne ajanı bütünlüğü:** Ortak 5 katman mimarisi, sıcak-soğuk ışık kuralı ve kilitli F3 varlık çağrıları (Turna v4, Lincoln v1) baştan brife bağlandığında 3 paralel görsel ajan tek elden çıkmış gibi bütünlüklü sahne setleri üretebiliyor.

## Tur 20+ · 26.11.2026 · R4-PARALAKS (Kritik Kesin Red)
- **Karakter bütünlüğü tek katmanda kalır:** Bir karakterin başı, gövdesi ve elleri farklı derinlik (`orta`/`sahne`/`onplan`) katmanlarına bölünürse statik kartta kusursuz görünse bile animatikte kamera hareketi/zoom anında kafa bedenden, el koldan kopar! Tüm karakter anatomisi tek derinlik katmanında tutulur; Görsel Kurul her animatik kontaktında bunu 1. öncelikle denetler.

## R4-ANATOMİ — Kilitli F3 Oranları, Yaka-Üstü-Boyun & Kesintisiz Kol (26.11.2026)
- **Sorun:** Sahne setlerinde `K.*_kafa(..., boyun=True)` çağrılıp altına özel gövde çizildiğinde (a) boyun alt kenarı yakanın üstünde kalarak kafa bedenin dışındaymış gibi göründü, (b) el yordamıyla çizilen omuzlar kilitli F3 modellerine kıyasla şişkin/kubbe kaldı, (c) `2.02` gibi sahnelerde masadaki önkol omuzdan kopuk çizildi.
- **Zorunlu Kural:**
  1. **Collar-Over-Neck Z-Order:** SVG çizim sırası her zaman `[Gövde/Omuzlar] → [K.*_kafa(..., boyun=True)] → [Gömlek/Ceket Yaka Kanatları + Kravat]` olur; boyun tabanı asla yakanın üstünde bırakılmaz.
  2. **Kilitli F3 Omuz Oranları:** Michael `~2,1×–2,3×` kafa genişliği, Lincoln `~2,3×–2,5×`, Sara `~1,9×–2,1×`; net omuz dikişi, şişkin kubbe omuz yasak.
  3. **Kesintisiz Kol Zinciri:** Masada/camda/prop üzerinde görünen her el/önkol omuz → üst kol → dirsek → önkol → bilek → el şeklinde kesintisiz gövdeye bağlı olmalıdır.
  4. **Görsel Kurul (G)** her set ve animatik denetiminde bu 3 maddeyi %200 kırpmalarda doğrudan kontrol etmeden onay veremez.

## R18-HAREKET — Slayt Gösterisi YASAK, Gerçek Sahne İçi Eylem (27.11.2026)
- **Sorun:** Yalnızca kamera kaydırması + ok/HUD taramasıyla ilerleyen statik sahneler slayt gösterisi hissi veriyor; izleyici eylemin sahne içinde canlı gerçekleştiğini görmeli.
- **Zorunlu Kural (Tüm gelecek bölümler ve tüm ajanlar için otonom standart):**
  1. **Hareketli Nesneleri Ayrı Katmanda Üret:** Her sahnede anlatımın ana eylemini taşıyan nesne/karakterler (sökülen cıvata + kayan tuvalet, inen/kalkan şalter kolu + titreşen telefon, kabloda kayan kaçaklar + tarayan projektörler, havalanan uçak + koşan karakterler, açılan kapı vb.) ayrı SVG katmanları olarak dışa aktarılır ki blok animatiğinde fiziksel olarak hareket edebilsinler.
  2. **Işık & Atmosfer Eyleme Tepki Verir:** Şalter çekildiğinde, kıvılcım çaktığında, alarm yandığında veya masa lambası açıldığında tüm sahnenin ışığı, gölgesi ve atmosferi o anla birlikte canlı olarak değişir.
  3. **Karakter Ayırt Ediciliği (Michael vs. Lincoln) & Detaylı Dövme:** Aynı karede yer alan karakterlerin yüz/çene/omuz siluetleri ilk bakışta ayrışmalı (Michael daha ince keskin çeneli, Lincoln daha geniş çeneli/yapılı). Dövme çizgileri asla kaba düz çubuklar olmamalı; kilitli **A-Sırt v1** kalitesinde ince gotik kemer, ikiz turna ve mimari telkari içermelidir.
  4. **Kutu Taşması Sıfır Tolerans:** Hiçbir HUD/damga/etiket metni kendi kutusunun dışına tek piksel bile taşamaz.
  5. **İki Kol Kontrolü:** Kadrajda gövdesi görünen her karakterin iki kolu da anatomik olarak doğru ve eksiksiz görünür (eksik kol kesinlikle yasak).
