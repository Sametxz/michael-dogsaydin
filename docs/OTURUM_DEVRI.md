# Oturum devri

## Son durum (26.11.2026, oturum 1)
**Yapılanlar**
1. `Sametxz/ragnar-dogsaydin` klonlandı; `studyo/BASLA.md` okuma sırası izlendi (02 → 03 → 01 → 06 → 04/05/07 → skill'ler ve şablonlar).
2. Ortam kuruldu: `scripts/setup.sh` çalıştı (ffmpeg/rsvg, Python paketleri, fontlar, r2/r3 bağlantıları). Ragnar reposunda fontlar Git LFS işaretçisi olarak geliyordu; gerçek fontlar çekilip bu repoya normal dosya olarak kondu.
3. Motor sınandı: `studyo/motor/ornek/demo.py onizle` 10 önizleme karesi üretti (pencere → iç mekân → halka uçuşu → fırtına).
4. Kullanıcının isteğiyle yeni ana repo kuruldu: `Sametxz/michael-dogsaydin`. Taşınanlar: `studyo/` (tamamı), `r2/` + `r3/` (yalnız kod: py/json/md/sh/svg), `tts/` (kod), `skills/`, `fonts/`, Ragnar `docs/` → `docs/ragnar/`. Medya (mp4/wav/png render çıktıları) taşınmadı; gerekirse ragnar-dogsaydin'den alınır.
5. `setup.sh` sadeleştirildi: Git LFS gerekmiyor, XTTS indirmesi isteğe bağlı (`XTTS=1`), `.secrets` klasörü oluşturuluyor. `.gitignore` tüm büyük medyayı dışarıda tutuyor.

**Kavranan konsept (özet)**
- Format: Born in Lore, "sen" anlatımı, 8–10 dk, Türkçe 2D animasyon, prolog + 6 bölüm.
- Ragnar'daki kusur: her çekim tek düz kare + Ken Burns + siyaha kararma → hikâye "anlatıldı, yaşanmadı".
- Yeni ilke: planlama birimi **cümle**. Her cümle kelimeye kilitli bir görüntü/eylem (D1), her çekim hareketli (D2), 3 sn ölü süre yok (D3), geçişlerin ≥ %60'ı anlamsal (maske, nesne taşıma, biçim eşleşmesi, zoom içinden, ön plan silme, savurma), siyaha kararma yalnız bölüm sonunda (D4–D5), duygu yedi kanalda (yüz/beden, ışık, renk, hava, kamera, sembol, ses) ve çekim içinde dönüşebilir (D6).
- Akış: F0 başlangıç → F1 lore_bible → F2 omurga + motifler + duygu eğrisi → F3 eklemli karakter/mekân kartları → F4 bölüm döngüsü (örgü → blok animatik → ham kareler → animatik) → F5 ses → F6 master → F7 yayın.

## Açık işler
1. **F0 soruları** (kullanıcıya soruldu): karakter ve dizi, sezon kapsamı, hedef süre, anlatıcı.
2. ElevenLabs anahtarlarını kullanıcıdan al → `/home/claude/.secrets/` (ses aşamasına kadar acil değil).
3. F0 cevabından sonra `projeler/<slug>/` iskeleti (`studyo/sablonlar/proje_iskeleti.md`) ve proje `CLAUDE.md`'si; karaktere özgü "kopyalanmayacak imza tasarımı" sınırı araştırılıp yazılacak.
4. F1 araştırma + F2 omurga (motif listesi ve duygu eğrisiyle) → kullanıcıya sunum.

## Ragnar projesinde açık kalanlar (yeni projeyi engellemez)
- 7 dilde dublaj (~85 bin kredi) kullanıcı onayı bekliyor.
- e4 satırı: "Sen dua ediyorsun" → "Sen dümene sarılıyorsun" önerisi karar bekliyor.
- ElevenLabs anahtarlarının iş bitince iptali hatırlatılacak.
