# Görsel kurul süreci (kullanıcı kuralı, 19.11.2026 14:36)

Kullanıcının talimatı:
> "Atelstan'ın gömüldüğü sahneyi de sen yaptın, çok daha başarılıydı. 3 görsel agent birbiriyle iletişim halinde olsun. Son video çıkartmadan önce ham kareler oluşturulsun. Seslendirme ve video oluşturma onaydan sonraya bırakılsın. Görsellik tam ve tutarlı olmalı. Agentlar son çıktıya uygun mu değerlendirmeli. Yetersiz kareler oluşturulursa benim talimatlarımla iyileştirilecek."

## Akış
1. **Ham kareler.** Ana ajan sahnenin anahtar karelerini tam çözünürlükte (1920×1080), son çıktıdaki kalitesiyle üretir. Ses ve video yapılmaz. Kareler `r3/kurul/<sahne>/` altına konur.
2. **Bağımsız inceleme.** Üç görsel ajan kareleri ayrı ayrı inceler ve görüşünü `kurul/<sahne>/pano.md` dosyasına kendi başlığı altında yazar.
3. **Tartışma.** Her ajan diğer ikisinin yazdıklarını okur, katılır ya da itiraz eder. Ortak bir karara varılır: kare başına **SON ÇIKTIYA UYGUN** ya da **YETERSİZ**, ölçüte dayalı gerekçeyle.
4. **Kullanıcıya sunum.** Ana ajan kareleri ve kurul kararını kullanıcıya gönderir. Yetersiz kareler **kullanıcının talimatlarıyla** iyileştirilir. Ana ajan kendi başına "yeterli" kararı vermez.
5. **Onaydan sonra üretim.** Kullanıcı kareleri onaylayınca seslendirme, animasyon ve video üretilir. Ardından kurul videoyu hareketiyle tekrar denetler.

## Kurul üyeleri
- **G1 · Karakter ve tutarlılık:** Model sayfalarına uyum, oran, kostüm, sahneler arası tutarlılık, poz ve beden dili, çizim kalitesi.
- **G2 · Kompozisyon, ışık ve renk:** Kadraj, ölçek, derinlik katmanları, ışık yönü ve karakter üstündeki ışık, renk planı, atmosfer efektleri, mekânın doluluğu.
- **G3 · Duygu, oyunculuk ve son çıktı uygunluğu:** Karenin duyguyu taşıyıp taşımadığı, ifade ve poz oyunculuğu, okunurluk. Born in Lore çıtasına ve yas sahnesi v5'e göre "son çıktıya uygun mu" kararını verir. Panoyu da bu üye toplar.

## Ölçüt kaynağı
`kurul/GORSEL_STANDART.md` (kurulun ilk görevi bu dosyayı yazmak). Referans: yas sahnesi v5, kullanıcının "daha başarılı" dediği sahne.

## Kredi tasarrufu modu (kullanıcı, 19.11.2026 18:50)
Görsel dil oturdu, artık amaç aynı kaliteyi daha az krediyle sürdürmek. Bir kurul turu (3 ajan) yaklaşık 750 bin token harcıyor.
1. **Kurul sahne başına bir kez toplanır, nesne başına toplanmaz.** Tek bir ajan (G3 koordinatör) bir sahnenin bütün ham karelerini tek kontakt sayfası üzerinden değerlendirir; G1/G2/G3 alanları bu tek raporda yer alır. Küçük düzeltmeler kurula gönderilmez.
2. **Ayrı nesne kartı yalnızca yeni ana nesnede yapılır** (yeni karakter, kimlik nesnesi, mekân). Mekân kartı ham karelerle aynı tura birleştirilebilir.
3. **Kontrol görselleri küçük tutulur.** Uygulayıcı ara kontrolleri 960 px kontakt sayfasında yapar; tam çözünürlük yalnızca kullanıcıya gönderilen karelerde kullanılır.
4. **Kullanıcıya sahne başına bir sunum yapılır:** kontakt sayfası ve 1–2 soru. Kare kare onay alınmaz.
5. **Uzun bağlam pahalıdır.** Her sahne bitince `OTURUM_DEVRI.md` güncellenir ve yeni oturuma geçmek önerilir.
