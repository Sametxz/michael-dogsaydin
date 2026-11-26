---
name: born-as-character-video
description: "X olarak doğsaydın?" tarzı, ikinci tekil şahıs anlatımlı, bir karakterin çocukluktan ölüme tüm hayatını anlatan, görsel gag yoğun 2D animasyon video üretir: kaynak harmanı, senaryo, kelimeye kilitli sahne tasarımı, kodla çizim, seslendirme, müzik, montaj, yayın paketi.
---

# "X Olarak Doğsaydın?" — Anlatı + Görsel Gag Videosu

Bir oyun/film/mitoloji/tarih karakterinin bütün hayatını, izleyiciyi o karakterin yerine koyarak ("sen") anlatan videoyu uçtan uca üretir. Referans: Born in Lore — "What If You Were Born as Kratos?" (8:06).

**Temel ilke:** Bu formatta kalite iki şeyden gelir. (1) Anlatı: kısa, kuru, ikinci tekil şahıs cümleler ve imgelerle kapanan bir yay. (2) Görsel yoğunluk: anlatıdaki her şaka, sayı, isim ve kavram ekranda **bir nesneye** dönüşür ve **tam o kelimede** belirir. Animasyon hafif olabilir; illüstrasyon kalitesi ve gag yoğunluğu hafif olamaz.

---

## 0. Ajanın düşünce biçimi (her kararda)

1. **Sen mi, o mu?** Her cümle "…yapıyorsun". Asla "X şunu yaptı".
2. **Bu cümlenin ekrandaki nesnesi ne?** Cevabı yoksa cümle zayıf ya da sahne eksik. "15 yaşında kralsın" → ayakları yere değmeyen çocuk + kocaman, gözüne kayan taç.
3. **Hangi imge geri dönecek?** "Bunu aklında tut / bir kenara yaz" gibi sözlü işaretler **zayıftır, kullanma.** Ekimi imgeyle yap: aynı nesne/hayvan/kıyafet hayatın başında, ortasında ve sonunda farklı anlamla döner; anlatıcı bunu ancak finalde, tek ve yalın bir cümleyle bağlar.
4. **Son espriden beri kaç saniye?** Hafif bölümde 10–15 sn; trajik anda 10+ sn şakasız.
5. **Görsel stil karakterle büyüyor mu?** Çocukluk sıcak/sevimli, yetişkinlik epik (kenar ışığı, kızıl gökler, siluet ordular), son karanlık ve sade.

---

## 1. Kapsam (tek soru seti; cevap yoksa varsayılanlarla devam et ve söyle)

- Karakter + kaynak (oyun/dizi/saga/tarih). Birden çok kaynak varsa **harmanla** ve sahnelerde kaynak etiketi göster.
- Dil (varsayılan: kullanıcının dili), süre (varsayılan 5–8 dk; "kısa/test" = 2–3 dk).
- Ses: TTS anahtarı var mı? Yoksa çevrimdışı Piper (aşağıda) + kullanıcıya "gerçek ses en büyük kalite artışı" notu.
- Görev listesi: Kaynak taraması → Omurga/imge yankıları → Senaryo → Öz-eleştiri → Karakter kadrosu (lineup testi) → Sahneler (önizleme tabakaları) → Ses/müzik → Render → Kontrol → Yayın paketi.

---

## 2. Kaynak harmanı → `lore_bible.md`

Hafızadan yazma; WebSearch ile tara, her olayı doğrula. Çocukluk genelde ince belgelenir: **ebeveynin efsanesini** (ör. babanın meşhur savaşı), doğum koşullarını, ilk iddia edilen yaşı ve ilk sınavı topla.

Tablo: `# | yaş | olay | kaynak (saga/kronik/oyun/dizi) | doğrulandı | duygusal ağırlık | görsel nesne fikri | imge potansiyeli`

Ara:
- **Çocukluk/ebeveyn efsanesi** → açılışın sıcak sahneleri.
- **Lakap/isim kökeni** → genelde en güçlü gag + imge.
- **Tekrar eden imgeler** (hayvan, kıyafet, silah, yemin, kehanet) → final bağlantısı.
- **Kaynak çelişkileri** → gizleme, gag yap: "Saxo'ya göre bir de buz tutturuyorsun."
- **Tarihî sayılar** (yıl, gemi sayısı, fidye) → ekranda makbuz/harita/tabela.
- **Ölüm + mirasçıların tepkisi** → finalin ritmi.

---

## 3. Omurga → `spine.md`

- Tek cümle tema + duygusal çapa (karakterin başta istediği şey).
- **İmge yankısı tablosu (3 adet):** `imge | 1. görünüş | 2. görünüş | final anlamı | final cümlesi`
  Örnek (Ragnar): yılan → hediye yavru yılan / lakabını veren yılan / ölümü getiren yılanlar → "Hayatına bir yılanla başlamıştın. Adını sana bir yılan vermişti. Şimdi yılanlar seni geri alıyor." Kıyafet: kıllı pantolon korur → ipek gömlek korur → gömleği çıkarırlar.
- Kesim listesi; 1–2 tanesi "Uzun hikâye." gag'i olur.
- **Bookend:** açılıştaki diegetik obje (to-do listesi, saga taşı, sözleşme) finalde geri döner ve eksik kalan paneli açar.

---

## 4. Senaryo → `script.py` (çekim listesiyle birlikte)

Her çekim: `id, bölüm, sahne, kaynak etiketi, lines=[parçalar]`. **Her parça ayrı seslendirilir**; parçalar görsel açılımların tetikleyicisidir (bkz. §7). Parçayı virgül/iki nokta/nokta sınırında böl; bir parça = bir görsel olay.

Yapı (oransal): Prolog %8–10 (kanca + bebeklik) · Çocukluk %12 · Gençlik/ilk zafer %15 · İsim kökeni %12 · Kayıp + yeni hayat %15 · Zirve %12 · Düşüş %13 · Miras %8 · Final %5. Yorum çağrısı ilk büyük kaybın hemen ardından (%37–45).

**Kanca formülü:** "[Karakter] olarak doğsaydın, [epik 1]. [Epik 2]. Ve tarihe [beklenmedik/absürt 3] ile geçerdin. Ama şu an? [Savunmasız başlangıç]."

**Ses tonu:** 6–10 kelimelik cümleler; üçlü ritim + kırılma; retorik soru ile dönüş ("Ya sen?"); kuru, şefkatli alay. Gag araç kutusu: hafife alma ("Terfi hızlı."), modern deyim, ters köşe tekrar, "teknik olarak", resmî lakabı gerçek sanma ("Kel Charles" → ok + "KEL (resmî lakabı)"), "Uzun hikâye.", tekrar eden kalıp, sayıyı somutlaştırma ("Yaklaşık iki buçuk ton.").

**Mizah araç kutusu** (her hafif bölümde en az iki; aynı tekniği arka arkaya kullanma):

| Teknik | Kalıp | Örnek |
|---|---|---|
| Hafife alma | Dev olay + minik yorum | "Bir krallığı yakıp yıkıyorsun. Kötü bir salı." / "Terfi hızlı." |
| Modern deyim | Mitolojik olay + günlük kalıp | "Sözleşmenin küçük yazılarını hep oku." |
| Ters köşe tekrar | Niyet + aynı kelimelerle sonuç | "Savaşı önlemek için uğraşıyorsun. Savaşı başlatıyorsun." |
| Fiziksel özellik takıntısı | Ciddi sıralama + saçma özellik | "Yenilmez, korkunç ve çok ama çok kel." |
| Resmî lakap / teknik terim | Lakabı gerçek bilgi gibi sun | "Kral Kel Charles savaşmıyor. Ödüyor." |
| Atlama | Uzun yan hikâyeyi tek kelimeyle geç | "Uzun hikâye." |
| Sayıyı somutlaştır | Rakam → fiziksel karşılık | "Yedi bin livre. Yaklaşık iki buçuk ton." |
| Kaynak çelişkisi | Versiyon farkını gag yap | "Saxo'ya göre bir de buz tutturuyorsun." |
| İnatçı döngü | Tekrar eden olay | "Yine öldün. Yine kalktın." |

**Yorum çağrısı:** "Kısa bir ara. Sırada kim doğsun? Yorumlara yaz." (~4–7 sn, ilk büyük kayıptan hemen sonra; ekranda rün taşına kazınmış soru). Abone çağrısı yalnızca açıklamada.

**Trajik anlar:** kurulum → tek cümle gerçek → şakasız sessizlik; görsel sadeleşir (mum söner, gömlek karanlıkta kaybolur).

**Final:** dönüşüm → çapaya dönüş → üçlü özet (bookend panellerini açar) → absürt imge ("dünya seni hâlâ pantolonunla hatırlıyor") → izleyiciye karar sorusu.

**Öz-eleştiri (zorunlu, ≥4/5 olana kadar):** kanca · sen-dili · her cümlenin görsel nesnesi var mı · imge yankıları finalde kapanıyor mu · espri aralığı · trajik anlar şakasız mı · cümle uzunluğu · süre (Piper ~135 kelime/dk, length-scale 0.86) · sesli okuma akışı · kaynak doğruluğu.

---

## 5. Referansla kendini karşılaştırma listesi (görsel denetim)

Her önizleme tabakasında bu maddeleri say; eksik olanı düzelt:

1. **Diegetik grafik objeler:** sözleşme, taş tablet, to-do/çeklist, tarif kartı, makbuz + damga ("ÖDENDİ"), ilan parşömeni, harita + hareketli rota, portre çerçeveleri + pirinç plaka, aile ağacı, tabela ("Ragnarök'süz gün: 1.095"), HUD/oyun çubukları (ÜN: sen ↓ oğullar ↑), eşitlik/eşitsizlik (= ≠), bölünmüş ekran (tarihçiler tartışıyor | sen sayıyorsun).
2. **Etiket + el çizimi ok:** kelimeye kilitli; tırmanan etiketler ("MARKED → MARKED → VERY MARKED"); ikinci satırda alt not ("(resmî lakabı)", "(bizzat)").
3. **Ölçek = güç:** tanrılar/krallar dev, çocuk minik; taht çocuğa göre kocaman.
4. **Plan çeşitliliği:** geniş / orta / yakın / aşırı yakın (göz, el) / siluet; her 2–4 sn yeni görsel olay.
5. **Işık:** ışık hüzmeleri (god rays), parlama, ateş ışığı, kor/kar/toz parçacıkları, vinyet, kenar ışığı; mekâna göre palet.
6. **Stil evrimi:** çocuklukta sıcak iç mekân; yetişkinlikte epik gökyüzü + siluet ordu; sonda soğuk/karanlık.
7. **Tipografi:** epik başlık (Cinzel/Pirata One), gag etiketi (Luckiest Guy, kontur + gölge), el yazısı not (Caveat Brush), parşömen metni (Alegreya). Türkçe glif kontrolü yap (ş ğ ı İ).
8. **Ekrana gömülü altyazı YOK** (SRT ayrı verilir). Bölüm etiketi pili yok; bunun yerine bölüm başında sinematik başlık (alt-sol, 2.5 sn) ve sağ üstte **kaynak etiketi** ("GESTA DANORUM · IX").
9. **Konuşma balonları** alıntı/diyalog için ("ADIN?" / ". . .").
10. **Bookend** ve **imge yankısı** görsel olarak aynı çizimle döner.

---

## 6. Karakter tasarımı (özgün, kodla)

- **Özgünlük kuralı:** Kaynak eserin resmî tasarımlarını, oyuncu yüzlerini, logoları kopyalama. Efsane/tarih figürlerinde kaynak metindeki ayırt edici öğeleri kullan (Ragnar: kıllı pantolon, sakal örgüsünde "hring" yüzükleri). Korunan bir oyun/dizi karakterinin tanınır çizimini yapma; arketip + metin etiketiyle anlat.
- **Oranlar:** yetişkin ≈ 4.5 kafa (head_r 76, gövde genişliği 156, kalın uzuvlar 38/46 px); genç ≈ 3.5; çocuk ≈ 2.4; bebek kundakta.
- **Yüz:** göz akı + iris + bebek + parlama; göz kapağı ifadeye göre; kalın kaş; küçük burun; ifade seti: neutral, happy, smug, angry, sad, surprised, sleepy, determined, smitten, pain, cold.
- **Kollar IK ile:** pozu açı değil **el hedefi** ile tanımla (omuza göre, kol boyu birimi). İki çözümden dirseği aşağıda olanı seç; kol kaldırma pozlarında dışa büken çözümü. Pozlar: stand, hips, arms_up, one_up, point, cross, hold_front, spear, thrust, shield, shrug, wave, sit, count, grip, give, bound, fist_up.
- **Cel shading:** gövde/yüz şekli clipPath ile sağ tarafa koyu ton; uzuvlarda alt kenar gölge çizgisi; saç üstünde parlama çizgisi.
- **Katman sırası:** gölge → arka saç → pelerin → bacaklar → gövde → zırh/kemer/yaka → kollar → boyun/kafa → eldeki obje → eller. (Arka saç gövdeden ÖNCE çizilmeli; aksi hâlde uzun saç gövdeyi kaplar.)
- **Kadro testi:** sahnelere geçmeden önce tüm karakterleri tek tabakada çiz ve incele (oran, kol, saç, okunurluk).
- Portre çerçevesi içindeki karakter: `translate(cx, 140 + 468*s) scale(s)` ile kafa üstte kalır.

---

## 7. Kelimeye kilitli zamanlama

1. Her `lines` parçasını ayrı TTS dosyası yap, sessizliği kırp (eşik ~500/32768, +60 ms kuyruk).
2. Zaman çizelgesi: parça sonu `,:;` → 0.12 sn, `.?!` → 0.28 sn boşluk; çekim kuyruğu 0.35 sn (+0.45 karanlık), ilk çekimde 0.35 sn giriş.
3. Sahne fonksiyonu `x.c(i)` = i. parçanın başlangıcı. Her etiket/pop/kamera hareketi/ses efekti bir `x.c(i) + ofset`'e bağlanır.
4. Animasyon dili: `pop` (geri tepmeli ölçek, 0.32 sn), `fade`, `ease_io` kamera itme/kaydırma, nefes (dikey %1), sallanma, çarpma yıldızı + hız çizgileri + 0.18 sn beyaz flaş, ekran sarsıntısı (0.25 sn), parçacıklar, ışık hüzmesi.

---

## 8. Render mimarisi (hızlı ve kaliteli)

- **Asla her kareyi tam SVG olarak rasterize etme** (yavaş). Her öğe bir kez `rsvg-convert` ile PNG sprite olur (hash önbelleği), kareler **skia-python** ile birleştirilir (dönüşüm + alfa ~1–6 ms/öğe), ham RGBA tek ffmpeg sürecine borulanır. 1080p30'da ~85 ms/kare; 2 parçaya bölüp paralel render et, `concat -c copy` ile birleştir.
- Canlı efektler skia'da: radyal vinyet, `kPlus` parlama, ışık hüzmesi poligonları, parçacıklar (kor/kar/toz/yağmur), el çizimi ok (kuadratik eğri, kontur + iç renk, ok başı), çarpma yıldızı.
- **Kamera kıskacı:** zoom ≥1 iken görüş penceresini sahne sınırına kıstır (siyah kenar olmaz).
- Doku: SVG `feTurbulence` grain + parşömen lekeleri sprite'a pişirilir (karede maliyet yok).
- Fontlar: `~/.fonts` içine Google Fonts (github raw) indir, `fc-cache -f`.
- Önizleme tabakası: her bölümden 6–9 çekimi %80 noktasında çiz, 3 sütunlu tabakada incele, §5 listesiyle düzelt. Tam render'dan önce en az bir tam tur önizleme.

Çekirdek (özet):
```python
def sprite(body, w, h, ax=None, ay=None, ss=1.0, defs=""):  # md5 önbellek → rsvg → skia.Image.open(png).makeRasterImage()
def draw(c, sp, x, y, s=1, rot=0, a=1, sx=None, sy=None):  # save/translate/rotate/scale(s/ss)/drawImage(anchor)/restore
class cam:  # with cam(c, z, cx, cy): kıstırılmış dünya dönüşümü
def pop(t,t0,d=.32): return back(lin(t,t0,t0+d)) if t>=t0 else 0
Writer: ffmpeg -f rawvideo -pix_fmt rgba -s 1920x1080 -r 30 -i - -c:v libx264 -preset veryfast -crf 18 -pix_fmt yuv420p
```

---

## 9. Ses

- **TTS:** Kullanıcının servisi varsa onu kullan. Yoksa `pip install piper-tts` + HuggingFace `rhasspy/piper-voices` (Türkçe: `tr_TR-dfki-medium`), `--length-scale 0.86`. Telaffuz sözlüğü tut (Loðbrók→Lodbrok, Ælla→Ella, yıllar → yazıyla).
- **Müzik (özgün, sentez):** bölüm başına ruh hâli profili (dron, davul, lir, yaylı yoğunlukları), 1.2 sn yumuşatma; lir = Karplus-Strong, yaylı = vibratolu testere dalga, davul = üstel düşen sinüs + gürültü. Trajik anlarda davul ve lir 0'a.
- **SFX:** bölüm geçişinde whoosh, darbelerde thud, isim/lakap açılışında chime — hepsi `x.c(i)` zamanlarına bağlı.
- **Miks:** ses kompresör → müzik sidechain ile -18…-22 dB → `loudnorm I=-14 TP=-1.5`.

---

## 10. Kontrol

- Final videodan her bölümden 1 kare + trajik an + final = 8–10 kare tabakası; §5 listesiyle say.
- Süre, ses seviyesi (-14 LUFS), siyah kenar, taşan yazı, kırpılmış portre, yüzü örten obje kontrolü.

## 11. Yayın paketi → `publish.md`

- Küçük resim: bebek/çocuk hâli ile son hâl yan yana ("önce/sonra"), kısa büyük metin, özgün çizim.
- Çok dilli altyazı istenirse: espriler kelime kelime değil işlevine göre çevrilir; süreler korunur.


Başlık (`{Karakter} Olarak Doğsaydın? | {Seri}`), 2. tekil kanca açıklaması, anahtar isimler, kapanış sorusu + "sırada kim?", bölüm zaman damgaları (zaman çizelgesinden), kaynak listesi (saga/kronik/oyun), "tüm çizimler, animasyon ve müzik özgündür" + resmî olmayan hayran çalışması beyanı, 3 hashtag, ayrı SRT dosyaları (parça zamanlarından otomatik).

## 12. Son kontrol listesi

- [ ] Her olay kaynakla doğrulandı; kaynak etiketleri doğru sahnede
- [ ] Öz-eleştiri ≥4; "aklında tut" tipi sözlü işaret yok, imge yankıları finalde kapanıyor
- [ ] Her cümlenin ekranda bir nesnesi var; etiketler kelimeye kilitli
- [ ] §5 karşılaştırma listesi tabakalarda sayıldı
- [ ] Tanınır resmî tasarım, oyuncu yüzü, logo ya da kaynak eser müziği yok
- [ ] Siyah kenar, taşan yazı, kırpılmış portre, yüzü örten obje yok
- [ ] Süre hedefe uygun; -14 LUFS; bölüm damgaları zaman çizelgesinden
- [ ] Teslim: final.mp4 + SRT + publish.md; bir satırda sıradaki karakter önerisi
