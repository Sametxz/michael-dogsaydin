# Sahne 7, Lagertha'nın vedası: kurul raporu (tek ajan, 960 px kontakt)

Çıta: hero_v5 (temiz, gölgeli, sinematik 2D; arkaplan sis ve bokeh, güçlü kontur, rim ışığı, duygu yüzde okunuyor).
Puanlar 0-3: K = karakter ve tutarlılık, I = ışık, kompozisyon, mekân, D = duygu.

## Kare 1: Aslaug kapıda, Ragnar ocak başında
K 2, I 2, D 1
- Ragnar yüzü şaşkın değil, "yan bakan, hafif tedirgin"; ağız açık "o" biçiminde ve sakal içinde okunmuyor. Bakış Aslaug'a değil boşluğa gidiyor.
- Aslaug'ın yüzü sakin gülümsüyor, hamile karnı ve mor giysi iyi okunuyor ama gece/kar kapısı ışığı ona rim veriyor, ocak ışığı vermiyor.
- Düzeltme 1: Ragnar'ın `pupil_dx` değerini Aslaug'a (sağa, kapıya) çevir, kaşları yukarı ve içe al (`brow_raise=0.8`), ağzı kapat, hafif açık dudak çizgisi kullan.
- Düzeltme 2: Aslaug'a ocaktan sıcak turuncu alt rim ekle (`rim(color=warm, side=left, a=0.5)`), ifadeyi daha kararlı yap (gülümsemeyi yarıya indir, çene yukarı).

## Kare 2: Lagertha yakın plan, Ragnar odak dışı
K 2, I 3, D 2
- Lagertha'nın yüzü öfke/küskünlük okutuyor ama kaşlar çok keskin, "kızgın karikatür"; hedef hüzünlü kararlılık. Sırtı dönük değil, yüz kameraya dönük (brifle uyumsuz): bu karede kafa 3/4 sağa bakıyor, omuz kameraya.
- Ragnar odak dışı bokeh ile derinlik çok iyi, çıtaya yakın. Yalvaran ifade okunuyor.
- Düzeltme 1: Lagertha kaşlarını `brow_angle` 0.5'e indir, alt göz kapağını gevşet, göze nemli parlama (`tear_gloss`) ekle; kafayı sağa 15 derece çevirip sırtı Ragnar'a daha belirgin ver (omuz örtüşmesi).
- Düzeltme 2: Sıyrık izi kontrastını biraz artır (şu an kaşa karışıyor).

## Kare 3: Geniş plan, Bjorn ortada
K 2, I 2, D 2
- Üç karakter ölçekçe tutarlı, mekân dolu ve okunur. Bjorn'ün ortada kalması kompozisyonla iyi anlatılıyor. Ancak karakterler küçük ve yüz ifadeleri 960 px'de kayboluyor.
- Ocak ışığı Bjorn'ü aydınlatıyor, Lagertha kapıda mavi, bölünme anlatısı güzel ama Ragnar'ın yüzü düz, ışık geçişi yok.
- Düzeltme 1: Kamerayı %15 yakınlaştır (`crop=(0.05,0.1,0.95,0.95)`) ya da karakterleri %20 büyüt; Bjorn'e çift taraflı ışık (sol sıcak, sağ soğuk) ver.
- Düzeltme 2: Zemine karakter gölgeleri ve ocak yansıması ekle (ayaklar şu an kesik/yüzer).

## Kare 4: Lagertha ve Bjorn kara çıkıyor, ön planda Ragnar silueti
K 2, I 3, D 3
- Bu kare çıtaya en yakın: ters ışık, kapı çerçevesi, kar, silüet. Duygu sözsüz okunuyor.
- Ragnar silüeti çok koyu, hatları kaybolmuş; sadece kafa ve omuz bir blok.
- Düzeltme 1: Silüete ince soğuk rim ışığı (`rim(color=cold, a=0.35)`) ve omuzda kuzgun broşun seçilmesi için hafif parıltı ekle.
- Düzeltme 2: İki figürün yürüyüş izi (kar üzerinde ayak izi) ve biraz daha uzak ölçek; şu an kapıda "dikilmiş" duruyorlar.

## Kare 5: Ragnar eşikte yalnız, arkada Aslaug tahtta
K 2, I 2, D 2
- Yüz hero_v5'e yakın ve yorgun ifade iyi. Fakat ifade yas değil "can sıkkınlığı" okunuyor (yarı kapalı göz, düz ağız). Aslaug kafa büyüklüğünde, bulanık, neredeyse görünmüyor; tahtta oturduğu anlaşılmıyor.
- Ocak sönüyor fikri zayıf: alev hâlâ canlı.
- Düzeltme 1: Ağız köşelerini aşağı (`mouth_curve=-0.6`), kaşları iç uçtan yukarı kaldır, bir damla yaş ekle (hero_v5'teki gibi); yüzü kapıya doğru değil boşluğa bakır.
- Düzeltme 2: Ocak alev boyutunu %40 küçült, kor ağırlıklı yap; Aslaug'ı tahta oturur boy ve taht çizimiyle belirgin yap (ya da yüzünü gizle) ve ışığı soğuk tut.

## Genel
Kareler arası tutarlılık iyi (kıyafet, broş, halka, mekân). Ana eksik: yüz ifadeleri hero_v5 kadar duygu taşımıyor (kare 1, 5), kare 3 küçük, zemin gölgeleri yok.

Ortalama: K 2.0, I 2.4, D 2.0.

## KARAR: YETERSİZ
Kare 2 ve 4 neredeyse yeterli. Kare 1, 3, 5 yukarıdaki düzeltmelerle yeniden render edilmeli.
