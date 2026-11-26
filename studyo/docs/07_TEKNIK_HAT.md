# Teknik hat

## 0. Kurulum (yeni ortam)
```bash
bash scripts/setup.sh                 # sistem paketleri (rsvg, ffmpeg), python paketleri, fontlar, r2/r3 bağlantıları
mkdir -p /home/claude/.secrets && chmod 700 /home/claude/.secrets
# Kullanıcıdan ElevenLabs anahtarlarını iste; dosyaya yaz, chmod 600. ASLA repoya yazma.
#   /home/claude/.secrets/elevenlabs_key   (TTS + SFX)
#   /home/claude/.secrets/elevenlabs_key2  (müzik izni olan)
cd studyo/motor && python3 ornek/demo.py onizle   # motor testi (10 PNG)
```
XTTS modeli yalnızca eski yerel ses hattı için gerekir. ElevenLabs kullanılıyorsa `setup.sh` içindeki XTTS indirmesi atlanabilir.

## 1. Yeni sahne motoru: `studyo/motor/`
| Dosya | Görev |
|---|---|
| `sahne.py` | `Iz` (anahtar kareli iz), `Oge` (katman, derinlik, giriş/çıkış, ikincil hareket, eylemler), `Kamera` (x/y/zoom, sarsıntı), `Cekim` (sahne grafiği + kelime kilidi `ck.k("kelime")`), `svg_sprite` (SVG → PNG önbellek) |
| `duygu.py` | `Duygu("yas")` kalıpları: renk matrisi + ışık degradesi + vinyet; `.gecis("huzur", t0, sure)` çekim içi duygu dönüşümü |
| `gecis.py` | Anlamsal geçişler (`Maske`, `NesneTasi`, `Eslesme`, `ZoomIcinden`, `OnPlanSil`, `Savurma`, `Kes`, `Karart`) + `Film` (render, önizleme, zaman çizelgesi) |
| `kelime.py` | faster-whisper ile kelime zamanları (önbellekli) |
| `dokum_kontrol.py` | Sahne dökümünü D1–D10 kurallarına göre denetler |
| `ornek/demo.py` | Çalışan örnek: pencere → iç mekân → halka uçuşu → fırtına |

**Performans:** 1920×1080 çizimde geçiş karesi 2 çekim render eder. Demo 11 sn için ~2 dk sürdü. Tam bölüm (~90 sn) yaklaşık 15–20 dk sürer. Önizleme için `Film.onizle()` kullanılır, tam render bölüm onaylanınca yapılır.

**Önbellek:** `motor/.cache/` (SVG sprite PNG'leri, git dışında). `STUDYO_CACHE` ortam değişkeniyle değiştirilebilir.

### Çekim yazma kalıbı
```python
from sahne import *; from duygu import Duygu; from gecis import *; from kelime import zamanlar
kw = zamanlar("ses/2.04.wav", bas=0.3)                       # satır çekimin 0.3. saniyesinde başlıyor
ck = Cekim("2.04", sure=kw[-1][2] + 0.8, kelimeler=kw, duygu=Duygu("huzur").gecis("yas", t0=..., sure=1.5))
ck.ekle(Oge("gok", ciz_gok, derinlik=0.05),
        Oge("ragnar", ciz_ragnar, x=820, y=900, derinlik=1, ikincil=[("nefes", 1)],
            eylemler=[(ck.k("dönüyor"), 0.5, lambda p: dict(rot=-4 * p))]),
        Oge("kuzgun", ciz_kuzgun, x=1300, y=300, derinlik=0.9, giris=("dus", ck.k("kuzgun", -0.1), 0.7)),
        Oge("on_plan_dal", ciz_dal, x=200, y=200, derinlik=1.4, blur=4, ikincil=[("salin", 1)]))
ck.kamera = Kamera(x=Iz([(0, 900), (ck.sure, 1000)]), z=Iz([(0, 1.0), (ck.sure, 1.1, "io")]))
```

## 2. Karakterler
- Ragnar'ın karakter sistemi `r3/art3.py`: `head3(spec, view, expr, look)`, `figure(...)`, `body_turn(...)`, `hand3(...)`, dokular `r3/tex.py`. Spec bayrakları ve ifade tablosu `docs/PIPELINE.md`'de.
- Yeni motorda bir art3 karakteri `svg_sprite(svg, w, h, ax, ay)` ile sprite olur ve bir `Oge`'nin `ciz` fonksiyonunda `draw_sprite` ile çizilir.
- **Yeni gereksinim, F3'te yapılacak:** D2 karakter eylemleri için karakter **eklemli** kurulmalıdır. Önerilen yapı `projeler/<ad>/karakter.py` içinde, her parça ayrı sprite ve kendi pivotuyla:
  - gövde (nefes ölçeği)
  - baş (dönüş ±8°, ifade varyantları önceden render: `neutral`, `joy`, `grief`, `anger`, `fear`, `resolve`)
  - göz kapağı (kırpma), ağız (konuşma yok, ama nefes ve iç çekme)
  - üst kol / ön kol / el (her biri pivotlu, `hand3` şekilleri: `relax`, `fist`, `grip`, `open`)
  - pelerin / saç (ikincil salınım)
  Bu yapı `Oge` içinde alt öğeler olarak kurulur (`ciz` içinde parçalar sırayla `c.save/rotate/restore` ile çizilir). İlk iş: model kartıyla birlikte bir "eylem kartı" (5 eylem × 3 kare) hazırlanıp onaya sunulur.
- Ragnar'ın efekt kütüphanesi `r3/fx/efekt.py` (ateş, kıvılcım, duman, kuzgun, ok, mızrak, flaş, ışık titreşimi, yağmur, kar, toz) yeni motorda bir `Oge`'nin `ciz` fonksiyonundan çağrılabilir: `lambda c, t, o: FX.fire(c, t, 0, 0, 0)`.

## 3. Sahne dökümü ve plan
- Döküm: `projeler/<ad>/dokum/bolum_X.json` (şema: `sablonlar/sahne_dokumu.schema.md`, örnek: `sablonlar/sahne_dokumu_ornek.json`).
- Kullanıcıya örgü sunumu, dökümden üretilen tablo ile yapılır (md ya da plan artifact'ı). Ragnar'ın plan sayfası örnek: `r3/plan/index.html`.

## 4. Seslendirme
- **ElevenLabs** (Ragnar'ın son hâli): ses "George" (`JBFqnCBsd6RMkjVDRZzb`), model `eleven_v3`, `language_code: "tr"`. Yardımcı: `tts/el.py` (`tts()`, `sfx()`), anahtar `/home/claude/.secrets/elevenlabs_key`.
  `python3 tts/el.py isler.json` → `[{"text", "out", "voice", "lang"}]` her satır ayrı wav (24 kHz mono).
- Satır başına bir dosya. Özel isimler fonetik yazılır. Sonra `motor/kelime.py` ile kelime zamanları alınır.
- Yedek yerel hat: XTTS-v2 "Damien Black" (`tts/gen.py`, `tts/takes.py`: 4 deneme + Whisper seçimi).

## 5. Müzik, efekt, miks (`r3/ses2/`)
- `muzik.py`: Eleven Music kompozisyon planı. Bölüm başına bir parça, `sections` duygu dönüşlerinde çekim başlangıçlarına hizalı, `respect_sections_durations`. GLOBAL ve NEG stil listeleri (vokalsiz, anlatıma yer bırakan). Anahtar 2. Aynı anda en fazla 2 istek.
- `kutuphane.json` + `lib/`: ElevenLabs SFX (11 kredi/sn). Ambiyans `amb_*`, nokta efekt `sp_*`.
- `miks.py`: AMB/SPOT/HUSH/FIRTINA tabloları. Konuşma satırı RMS −19 dB. Müzik EQ (2,5 kHz −5 dB, 1,2 kHz −2,5 dB), konuşma altında ~−8 dB. Ambiyans %55, nokta efektleri %50 kısılır. Çıkış −16 LUFS. Görüntüye `-c:v copy` ile eklenir.
- Yeni projede `miks.py`, `Film.zaman_cizelgesi()` çıktısını kullanacak biçimde uyarlanır: anlatım satırları çekim başlangıcı + satır ofsetiyle yerleşir. **J-cut:** Bir sonraki çekimin ortam sesi geçişten 0,4 sn önce başlar.
- Kontrol: `tts/asr.py mix.wav`. Mikste anlaşılabilirlik kuru sesle ±%3 içinde olmalı.

## 6. Montaj ve yayın
- `r3/final/birlestir.py`: bölümleri birleştirir (`RES`, `CRF` ortam değişkenleri), 1080p usta dosya.
- `r3/final/yayin.py`: anlatım satırlarının gerçek başlangıçlarına kilitli 8 dil SRT (en fazla 2 satır × 42 karakter), `bolumler.json`.
- `r3/final/yayin.md`: başlık, açıklama, bölümler, etiketler, YouTube çok dilli ses ve altyazı adımları (şablon: `sablonlar/yayin_sablonu.md`).
- `r3/kapak/kapak.py`: 8 dilde kapak (1280×720 JPG + 2560 PNG). Arapça için Noto Kufi Arabic (`fonts/`).

## 7. Dosya ve klasör kuralları
- Yeni projenin kodu `projeler/<slug>/` altında durur ve **göreli yol** kullanır (`Path(__file__).parent`). Ragnar'daki `/home/claude/r3` mutlak yolları yeni kodda kullanılmaz.
- Büyük çıktılar (mp4, wav, 2560 png) `.gitignore`'a eklenir. Onaylı kareler ve kontakt sayfaları repoya girer.
- Her render geçici adla yazılır ve ffmpeg başarıyla bitince yeniden adlandırılır.
