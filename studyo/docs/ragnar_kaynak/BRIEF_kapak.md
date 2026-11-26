# BRIEF: YouTube kapağı denetimi ve iyileştirme (21.11.2026)

Kullanıcı isteği: "2 alt agent daha ekle görseli denetleyip iyileştirsinler; YouTube için en optimal hale getirsinler, tıklanmayı arttıracak ve görsel açıdan kusursuz görünen. Eklemeleri de onlar tespit etsin, iyileştirme önersin."

Taslak: `kapak/kapak_tr.jpg` (1280×720) ve `kapak/kapak_tr_2560.png` (tam çözünürlük). Kod: `kapak/kapak.py` (sol(): çiftçi aile, sag(): yaşlı kral, ayrac(), yazi()).
Kullanıcının tarifi: solda çiftçi Ragnar, Lagertha ve çocuklarıyla mutlu ve huzurlu; sağda yaşlı Ragnar bitkin, yaşanmışlıklarla dolu; arkasında kuzgunlar ve ağaç (detay serbest). Metin solda "Her şeyi olan bir çiftçiden", sağda "Hiçbir şeyi olmayan krala". Referans: sol-sağ zıtlık kapakları (bebek ve yanan bina). Birebir kopyalanmaz, kendi tarzımız korunur.
8 dil çıkacak (tr, en, es, pt-BR, de, fr, ar, ru): metin kutusu uzun dillere (ru, de) de sığmalı; Arapça sağdan sola yazılır.

## Sınırlar (CLAUDE.md)
- Oyuncu benzerliği yok. Dizideki Ragnar kafa deseni kombinasyonu yok. Model gövdeleri (art3 `full`) ve yaş evreleri (`ragnar_yas`: RG1 çiftçi, RG4 son) kullanılır.
- Profil yüz uydurulmaz, asimetrik karakter aynalanmaz. Kan yok.
- Çıta: en az 4 derinlik katmanı, düz renk alan yok, belirgin ışık, R13 (≥%200 kırpma ile kusur arama).

## Ajan 1: Tıklanma (CTR) stratejisti
- Kapağı YouTube'un gerçek gösterim boyutlarında incele: 1280×720, 320×180 (ana sayfa), 168×94 (öneriler, mobil). Sağ altta 13:18 gibi bir süre rozeti kapatır, o köşeyi hesaba kat.
- Sorular: Metin en küçük boyutta okunuyor mu? Sol/sağ zıtlığı ilk bakışta anlaşılıyor mu? Odak yüzler yeterince büyük mü? Duygu (sevinç / yıkım) okunuyor mu? Göz hangi sırayla dolaşıyor? Renk zıtlığı yeterli mi? Gereksiz kalabalık var mı?
- Somut öneriler yaz: ne büyüyecek, ne çıkacak, ne eklenecek (ör. "kral" okuması için taç, "her şey" için altın parıltısı vb.). Gerekçe olarak bilinen kapak ilkelerini kullan.
- Çıktı: `kurul/kapak_ctr.md` (en fazla 12 madde, önem sırasıyla, her biri uygulanabilir talimat). Kod değiştirme.

## Ajan 2: Sanat yönetmeni / görsel kalite
- 2560 PNG üzerinde R13 kırpmalarıyla kusur ara: kesik sprite, yamuk kenar, yanlış yerleşim (kuzgun omza oturuyor mu?), boş ya da düz alanlar, ışık tutarlılığı, ayracın kalitesi, metin konturu.
- Kompozisyon önerileri yaz.
- İkinci aşama: Ajan 1'in raporu ile kendi bulgularını birleştir. Bunları `kapak/kapak.py` dosyasına uygula. Yaşlı Ragnar için şimdilik gözyaşlı yüz varsayılıyor; değiştirmeyi önerirsen gerekçeni yaz. TR ve RU kapaklarını üret, en uzun metin olan RU taşmamalı. 2 tur öz değerlendirme yap. Önce/sonra karşılaştırması `kapak/kontakt_kapak.png` dosyasına: 1280 ve 320 boyut yan yana.
- Çıktı: `kurul/kapak_gorsel.md` (bulgular + yapılanlar).
