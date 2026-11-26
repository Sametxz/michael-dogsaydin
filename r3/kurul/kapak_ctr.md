# Kapak CTR denetimi (Ajan 1, 21.11.2026)

İncelenen dosya: `kapak/kapak_tr.jpg`. Kapak 1280×720, 320×180 (sağ alta 9:12 süre rozeti eklenerek) ve 168×94 boyutlarında incelendi. 168 boyutundaki görüntü ayrıca 3 kat büyütülerek bakıldı.
Ölçülen ortalama parlaklık: sol yarı 152, sağ yarı 65. Bu değerlerle sol/sağ zıtlığı ilk bakışta okunuyor ve kapağın en güçlü yanı bu. Zayıf noktalar şunlar: duygular yanlış okunuyor (sol tarafta mutluluk yok), "kral" fikri görselde karşılanmıyor ve 168 px'de metin zor seçiliyor.

## Göz dolaşımı (mevcut durum)
Göz önce sol başlığa (en parlak ve en büyük öğe), sonra sol aileye (dört yüz dikkati bölüyor), ardından ayraca, sağ başlığa ve en son yaşlı yüze gidiyor. Olması gereken sıra farklı: önce iki büyük yüz (Ragnar ↔ yaşlı Ragnar), sonra iki anahtar kelime (HER ŞEY ↔ HİÇBİR ŞEY). Şu an sağdaki yüz son durak olduğu için duygusal vuruş geç geliyor.

## Öneriler (önem sırasıyla)

1. **Soldaki Ragnar'ın ifadesini mutluluğa çevir.** Gözler kapalı, kaşlar çatık ve ağız açık. 320 ve 168 px'de bu yüz gülümseme olarak değil, yüz buruşturma ya da öfke olarak okunuyor. Kızın ve Bjorn'un gözleri de kapalı ve sıkılmış görünüyor. Yapılacaklar: Ragnar ve Lagertha'da açık gözlü, kaşları kalkık, dişleri görünen geniş bir gülüş kullan. Çocuklarda da açık gözlü gülümseme olsun. Bu tür kapaklarda zıtlık iki net duygu üzerine kurulur. Sol yüzlerde sevinç okunmazsa "her şeyi olan" vaadi görselde karşılık bulmaz.

2. **Yaşlı Ragnar'ın başına bir taç ekle.** "Kral" kelimesi görselde hiçbir şekilde karşılanmıyor. Yaşlı adam bir dilenci ya da keşiş gibi de okunabilir. Önerim düz, demir veya kararmış altından basit bir Viking tacı. Taç hafifçe yana kaymış olsun ve kızıl kenar ışığı alsın. Dizideki tasarım kopyalanmamalı. Taç 168 px'de bile seçilen tek "statü" işareti olur ve "hiçbir şeyi olmayan kral" paradoksunu tek nesneyle anlatır.

3. **Yüzleri büyüt ve bacakları kadrajdan çıkar.** Soldaki figürler ekranın alt yarısının çoğunu bacak ve gövdeyle dolduruyor. Ragnar'ın yüzü 1280'de yaklaşık 140 px, 168'de yaklaşık 18 px. Önerim aileyi yaklaşık 1,3× büyütüp aşağı kaydırmak; kadraj bel hizasından kesilsin. Yaşlı Ragnar'ın başı da kadraj yüksekliğinin %40–45'ine çıkarılsın; şu an bu oran yaklaşık %30. Küçük boyutta tıklamayı yüz büyüklüğü belirler.

4. **Soldaki kalabalığı azalt: odakta iki yüz olsun.** Dört yüz eşit büyüklükte olunca küçük boyutta yüzler birbirine karışıyor. Önerim Ragnar ve Lagertha'yı öne ve büyük koymak, çocukları biraz daha küçük ve kısmen arkada (önlerinde ya da kucakta) göstermek. Ragnar'ın yüzü, sağdaki yaşlı yüzle aynı yükseklikte ve aynı boyutta olsun. Böylece iki yüz yatay bir eksende "ayna" oluşturur ve göz soldan sağa doğrudan atlar.

5. **Anahtar kelimeleri renkle ayır ve iki başlığın puntosunu eşitle.** Sağ başlık uzun olduğu için (19 karakter) otomatik olarak küçülüyor. Bu yüzden 168 px'de "HİÇBİR ŞEYİ OLMAYAN" okunmuyor, sol başlık ise daha baskın kalıyor. Önerim: "HER ŞEYİ" altın renginde (#FFD24A) ve en büyük puntoda, "HİÇBİR ŞEYİ" kor kırmızısında ve aynı puntoda olsun. Bağlaç satırları ("OLAN BİR ÇİFTÇİDEN", "OLMAYAN KRALA") %70 punto ile alt satıra insin. Satır düzeni: `HER ŞEYİ|olan bir çiftçiden`, `HİÇBİR ŞEYİ|olmayan krala`. Küçük boyutta yalnızca iki karşıt kelime okunacaktır, ama kapağın vaadini taşımaya bu yeter. Bu düzen RU ve DE gibi uzun dillerde de taşmayı önler, çünkü uzun kısım küçük satıra gider.

6. **Metin konturunu ve gölgesini 168 px için kalınlaştır.** Mevcut kontur (fs×0,24) 1280'de iyi, ama 168'de harfler birbirine yapışıyor ("ÇİFTÇİDEN" bulanık bir lekeye dönüyor). Önerim: konturu fs×0,30'a çıkar ve 6–8 px'lik koyu bir alt gölge ekle (drop shadow, ofset 0,+8). Sol başlığın arkasına, yarı saydam ve sıcak koyu bir bulut ya da hale koy. Krem renkli harfler açık gökte zayıf kalıyor; sol başlık bölgesinin parlaklığı 152, sapması 99, yani zemin harfi yer yer yutuyor.

7. **Sol tarafa "her şey" ışığı ekle: altın saat güneşi.** Sol gök soluk mavi-beyaz ve haki tonda; huzur var ama bolluk hissi yok. Önerim ailenin arkasında, sol üst ya da Lagertha'nın başının arkasında sıcak bir altın güneş haresi ve ışık hüzmeleri. Çimene altın tonu ver, birkaç ekin demeti, uçuşan parıltı ya da polen ekle. Sağdaki kızıl kor parçacıkları ile soldaki altın parıltılar birbirine karşılık versin. Renk sıcaklığındaki zıtlık (altın ↔ kızıl-siyah), parlaklık zıtlığını da güçlendirir.

8. **Yaşlı yüzde yıkımı güçlendir.** Gözyaşı 1280'de görünüyor, 320'de kayboluyor. Yüz "yorgun" okunuyor ama "yıkılmış" okunmuyor. Önerim: gözyaşını kalınlaştır ve uca beyaz bir parlama noktası koy. Yüzün etrafına koyu bir vinyet yap ki yüz, sağ yarının tek aydınlık noktası olsun. Göz altlarını ve yanakları biraz daha gölgele, ağız köşelerini daha fazla indir. Gözyaşlı yüzü korumayı öneriyorum: küçük boyutta "üzgün yaşlı kral" en hızlı okunan ve en merak uyandıran duygu.

9. **Kuzgunları az ama okunur yap.** Ağaçtaki 4–5 kuzgun 320 px'de birer siyah çizgi gibi görünüyor ve gürültü üretiyor. Omuzdaki kuzgun da saçla karışıyor. Önerim: ağaçta en fazla 2–3 kuzgun bırak, ama her biri 1,5–2× büyük olsun ve gökyüzüne karşı net bir silüet çizsin. Kanadı açık bir kuzgun yaşlı kralın başının üstünde ya da yakınında dursun ve kızıl kenar ışığı alsın. Omuzdaki kuzgun ya tamamen çıkarılsın ya da büyütülüp omzun dış kenarına, gökyüzüne karşı yerleştirilsin. Ölüm alameti tek ve net bir öğe olarak okunmalı.

10. **Gri broş dairelerini sadeleştir.** Ragnar'ın göğsündeki kuzgun broşu, yaşlı Ragnar'daki broş ve Lagertha'nın "+" işaretli düğmesi küçük boyutta arayüz simgesi gibi (oynat/ekle düğmesi) okunuyor. Kapak, YouTube arayüzü üzerinde gösterildiği için bu karışıklık izleyicinin gözünü yanlış yere çekiyor. Önerim: broşları %60 küçült ve metal ya da bronz tonuna çevir; gri-beyaz daire görüntüsü ortadan kalksın. Lagertha'daki "+" düğmesini sade bir tokaya dönüştür.

11. **Sağ alt köşeyi rozete bırak ve sağ alt yarıdaki boşluğu kullan.** 13:18 süre rozeti, sağ alttaki altın kol halkasının ve pelerinin üstüne düşüyor. Şu an orada önemli bir şey yok ama o bölge kuru (sağ alt bölgenin parlaklık sapması 38, düz ve koyu bir pelerin alanı). Önerim: kol halkasını kapağa sokma ya da sol tarafa al. Yaşlı kral büyütülünce (madde 3) bu bölge kendiliğinden göğüs ve sakalla dolar. Hiçbir metin ya da anahtar nesne sağ alt 200×110 px'lik alana (1280 ölçeğinde) konmamalı.

12. **Ayracı koru, ama ortadaki yarığı biraz incelt.** Yırtık ayraç zıtlığı iyi taşıyor ve 168 px'de bile görünüyor; değiştirmeye gerek yok. Kalın siyah çizgi soldaki Bjorn'un kolunu kesiyor. Önerim: siyah çizgiyi 22 px'ten 16 px'e indir ve sol taraftaki altın kenar ışığını biraz artır. Böylece "sıcaktan soğuğa geçiş" duygusu belirginleşir. Ayrıca ayracın en az 30 px yakınına hiçbir yüz gelmesin.

## Kısa sonuç
Önce şu dört maddeye öncelik ver: 1 (sevinç ifadesi), 2 (taç), 3 ve 4 (yüz büyüklüğü), 5 (anahtar kelime renkleri). Bu dört değişiklik kapağı küçük boyutta "mutlu çiftçi ↔ ağlayan kral" diye tek bakışta okunan bir hikâyeye dönüştürür. Diğer maddeler cila.
