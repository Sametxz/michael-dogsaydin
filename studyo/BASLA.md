# BAŞLA: yeni karakter videosu (yeni oturumun giriş noktası)

Bu klasör, "Ragnar Lothbrok Olarak Doğsaydın?" projesinden (tamamlandı, 26.11.2026) çıkan bilgiyle hazırlanmış **başlangıç paketidir**. Yeni oturumda repo bağlanınca önce bu dosyayı oku.

## 1. Okuma sırası (zorunlu)
1. `studyo/BASLA.md` (bu dosya)
2. `studyo/docs/02_DINAMIK_ANLATIM.md`: **kullanıcının yeni video için en önemli isteği**
3. `studyo/docs/03_DUYGU_DILI.md`
4. `studyo/docs/01_IS_PLANI.md`: aşamalar ve onay kapıları
5. `studyo/docs/06_DERSLER.md`: Ragnar'dan kalıcı dersler, kullanıcı tercihleri, sınırlar
6. `studyo/docs/04_AJANLAR.md`, `05_KALITE_STANDARDI.md`, `07_TEKNIK_HAT.md`: ihtiyaç oldukça
7. Skill'ler: `studyo/skills/born-as-character-video/SKILL.md` (v3), `studyo/skills/dinamik-sahne/SKILL.md`

## 2. Kullanıcının yeni video için istediği (26.11.2026, birebir)
> 1. Çok story telling şeklinde kaldı ve hikaye dinamik anlatılmadı. Her sahnede her söylenen cümlenin hayata geçtiği daha hareketli bir senaryo istiyorum.
> 2. Her söylenen cümlede ekrana o cümlenin öğesi gelmedi. Çoğu mümkün mertebe hareketli olmalı, sahneler arası anlamsal geçişler olmalı. Örneğin o an söylenen öğe evin penceresinde belirsin, sonra gelecek sahne pencereden devam etsin. Akıcı ve dinamik bir anlatım sunsun.
> 3. Sahnelerde duygular ve hissiyat aktarılsın, bunun için görsel öğelerden faydalanılsın.

Bu üç madde `02` ve `03` belgelerinde D1–D10 kurallarına, geçiş kataloğuna ve duygu kanallarına çevrildi. `motor/dokum_kontrol.py` bunları otomatik denetler.

## 3. İlk oturumda yapılacaklar
1. Ortamı kur: `bash scripts/setup.sh`. ElevenLabs anahtarlarını kullanıcıdan iste ve `/home/claude/.secrets/` altına yaz (asla repoya değil). Motoru sına: `cd studyo/motor && python3 ornek/demo.py onizle`.
2. **F0 soruları** (tek AskUserQuestion): Hangi karakter ve dizi? Hangi sezonlar? Hedef süre (önerilen 9 dk)? Anlatıcı (önerilen ElevenLabs George)?
3. `projeler/<slug>/` iskeletini kur (`sablonlar/proje_iskeleti.md`). `CLAUDE.md`'yi `sablonlar/CLAUDE_proje_sablonu.md`'den doldur. Karaktere özgü "kopyalanmayacak imza tasarımı" sınırını araştırıp yaz.
4. F1 araştırması ve F2 omurgası: motif listesi ve duygu eğrisiyle birlikte. Kullanıcıya sun.
5. Her tur sonunda `karar_gunlugu.md` ve `OTURUM_DEVRI.md` güncellenir, commit ve push yapılır.

## 4. Klasör haritası
```
studyo/
├── BASLA.md                     ← buradasın
├── docs/
│   ├── 01_IS_PLANI.md           aşamalar F0–F7, onay kapıları, sunum biçimi
│   ├── 02_DINAMIK_ANLATIM.md    D1–D10, cümle→çekim yöntemi, geçiş kataloğu, hareket sözlüğü
│   ├── 03_DUYGU_DILI.md         7 duygu kanalı, duygu kalıpları, çekim içi duygu dönüşümü
│   ├── 04_AJANLAR.md            A1 hikâye, A2 sahne yönetmeni (yeni), G kurul, K1/K2 kapak + brief'ler
│   ├── 05_KALITE_STANDARDI.md   R1–R17, kare kuralları, video denetimi
│   ├── 06_DERSLER.md            Ragnar'dan kalıcı dersler ve kullanıcı tercihleri
│   ├── 07_TEKNIK_HAT.md         kurulum, motor, karakter, ses, miks, yayın
│   └── ragnar_kaynak/           Ragnar'ın tam standart, ders, brief, yayın ve karar günlüğü metinleri
├── motor/                       YENİ dinamik sahne motoru (çalışır, demo ile sınandı)
│   ├── sahne.py  duygu.py  gecis.py  kelime.py  dokum_kontrol.py
│   └── ornek/demo.py            pencere → iç mekân → halka uçuşu → fırtına (çıktı: `ornek/out/`, git dışı)
├── sablonlar/                   döküm şeması + örnek, örgü sunumu, brief, proje iskeleti, CLAUDE.md, devir, günlük, yayın
├── skills/                      born-as-character-video v3, dinamik-sahne, video-making
└── referans/                    Ragnar'dan kalite çıtası kareleri (küçültülmüş) + kapak
```
Ragnar'ın yeniden kullanılabilir kodu repoda olduğu yerde durur: `r3/art3.py` (karakter), `r3/tex.py` (doku), `r3/fx/efekt.py` (efektler), `r3/ses2/` (müzik, SFX, miks), `r3/final/` (birleştirme, SRT), `r3/kapak/` (kapak), `tts/el.py` (ElevenLabs).

## 5. Ragnar projesinde açık kalanlar (yeni projeyi engellemez)
- 7 dilde dublaj (yaklaşık 85 bin kredi) kullanıcı onayı bekliyor.
- e4 satırı: "Sen dua ediyorsun" → "Sen dümene sarılıyorsun" önerisi karar bekliyor.
- Kullanıcıya ElevenLabs anahtarlarını iş bitince iptal etmesi hatırlatılacak.
