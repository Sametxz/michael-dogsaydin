# Teknik hat

## Dizinler
| Yol | İçerik |
|---|---|
| `r2/` | Çekirdek motor ve ilk tam video (v2). `engine.py`: sprite/çizim/easing/parçacık/Writer, `art2.py`: art2 karakter sistemi (BODY, POSES, IK kollar), `bg.py`: arka plan parçaları, `scenes_a.py`/`scenes_b.py`/`render.py`/`script.py`/`audio2.py`/`tts2.py`: v2 videosu, `SKILL_v2.md`: önerilen skill güncellemesi |
| `r3/` | İnteraktif mod çalışmaları. `art3.py`: çok görünüşlü kafa ve vücut (head3, body_turn, figure, hand3), `fx.py`: efektler, `stylefr.py`: şelale ortamı ve orman, `puppet.py`: kukla parçaları, `anim1-4.py`: yas sahnesi v1–v4, `model_sheet_v*.py` ve `model_lagertha_v1.py`: model sayfaları, `yas_tts.py`/`yas_mix.py`: yas sahnesi sesi, `veda/`: Lagertha vedası (storyboard.py, anim.py, mix.py) |
| `r3/karar_gunlugu.md` | Her turun kararları ve dersleri (**her turda güncelle**) |
| `r3/hikaye_taslak_v1.md`, `v2.md` | Hikâye omurgası (v2 güncel) |
| `tts/` | XTTS üretimi (`gen.py`, `takes.py`: çoklu deneme + Whisper seçimi), `asr.py` (anlaşılabilirlik testi), örnek sesler |
| `skills/` | Kullanıcının skill'leri: born-as-character-video, video-making |
| `fonts/` | Kullanılan fontlar (Pirata One, Alegreya, Cormorant Garamond, Luckiest Guy…) |

`r3/engine.py`, `art2.py`, `bg.py` ve `scenes_a.py`, `../r2/` içindeki dosyalara bağlantıdır.

## Render
- 1920×1080, 30 fps. SVG parçaları `rsvg-convert` ile PNG'ye çevrilir ve md5 önbelleğine alınır. Her kare skia-python ile birleştirilir. Ham RGBA tek bir ffmpeg sürecine (libx264 veryfast crf18) aktarılır. Kare başına ~85 ms.
- Sahne fonksiyonu imzası `shot(c, t, d)` şeklindedir. Kamera `with_cam` veya `cam(z, cx, cy)` ile yönetilir, kenarlar sıkıştırılır (clamp). Çekimler arası geçiş 6–8 karelik siyaha karartmadır.
- Önizleme: `python3 animX.py prev` birkaç tam boy kare üretir. Tam render: `python3 animX.py full`.

## Karakter sistemi (art3)
- `head3(spec, view, expr, look)`: view değerleri front/3q/side/back. `EXP[expr] = (brow_inner, brow_outer, lid_up, lid_low, mouth, extra)`. **Kaşta negatif inner değeri iç ucu yukarı kaldırır (yas).**
- Spec bayrakları:
  - `undercut`, `nobraid`, `shaved`
  - `female`: sakal yok, yumuşak çene, kirpik, dudak, taç örgü
  - `beardless`, `scratch`
  - `brow_k`: kaş kalınlığı, `brow_c`: kaş rengi
  - `armring`, `clasp`
- Specler: `RAGNAR_UC` (art3), `puppet.WET` (ıslak), `veda/storyboard.py` içinde `LAG`, `ASL`, `BJ`.
- Kukla: `puppet.py` parçaları pivot etrafında çizer (yürüyüş, diz çökme, haç saplama, büst, sırttan siluet).

## Efektler (fx.py + engine)
tinted (kenar ışığı), blurred (derinlik), grade, gradient_grade, Rain (+splashes), fog, light_shaft, bloom_spot, letterbox, vignette, glow, rays, Particles (ember/snow/dust/rain).

## Ses
1. Her cümle ayrı üretilir: `tts/takes.py <jobs.json> 4`. Konuşmacı Damien Black, dil tr, hız 0.92. Her cümleden 4 deneme alınır, Whisper ile metin benzerliği ölçülür, en iyisi seçilir ve son kelimede kesilir (uydurma kuyruğu temizlenir).
2. Özel isimler fonetik yazılır ("Lagertha" → "Lagerta").
3. Kelime zaman damgaları faster-whisper `word_timestamps=True` ile alınır. Görsel olaylar bu zamanlara kilitlenir.
4. Miks numpy ile yapılır (`yas_mix.py`, `veda/mix.py`). Ses efektleri ve müzik sentezlenir (bowed yaylı, Karplus-Strong lir). Konuşma sırasında ducking uygulanır. Ardından `loudnorm I=-16`.
5. Kontrol: `python3 tts/asr.py mix.wav` çıktısı metni doğru vermeli.

## Lisans notları
- XTTS-v2 modeli Coqui Public Model License altındadır ve ticari olmayan kullanıma izin verir. Proje kişisel olduğu için uygundur.
- Piper tr_TR-dfki-medium sesi yalnızca eski v2 videosunda kullanıldı.
