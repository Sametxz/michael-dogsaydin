# Brief: Bölüm V · Kayıp On Yıl ham kareleri
**Önce oku:** `/home/claude/r3/kurul/BRIEF_bolum1_v3.md` (zorunlu kalite kuralları 1–9), `/home/claude/r3/kurul/BRIEF_SABLON.md`, `/home/claude/r3/kurul/DERSLER.md` → "KÖK NEDEN ANALİZİ". Örgü: `/home/claude/r3/plan/orgu_bolum5_v1.md`.
**Çıta:** `/home/claude/r3/bati/v3/kontakt_v3_960.png` ve `/home/claude/r3/paris/kontakt_paris_960.png`. Teknikleri `v3_a.py`, `v3_b.py`, `v3_c.py` ve `v4_paris.py` dosyalarından yeniden kullan.
**Teknik:** Kod `/home/claude/r3/bati/v5_kayip.py` içinde (`from kareler6 import *`; gerekirse `import v3_b, v4_paris, gemi as G`). Çıktılar `/home/claude/r3/kayip/<id>.png`. Kontakt: `kayip/kontakt_kayip_960.png`. Dosya sonunda `FR = {...}` tanımlanır. Ortak dosyalara yazma; video, ses ve git yok.

**1. Önce model kartı** (`kayip/model_ogullar.png`): yetişkin dört oğul, Ragnar'ın yanında boy karşılaştırmasıyla. Tümü art3 model gövdesiyle çizilir ve özgün tasarımdır.
- **Ubbe:** sarımsı kumral saç, örgülü sakal, en olgunu; tahtadaki pul tasarımıyla uyumlu (`tahta/tahta.py` UBBE rengi).
- **Hvitserk:** açık sarı saç, genç ve kısa sakal.
- **Sigurd:** koyu saç; gözünde yılan işareti (yılan gözü), kimlik öğesi.
- **Ivar:** zeki, keskin bakışlı, mavi gözlü, sakalsız ya da çok az sakallı. Bacakları zayıf olduğu için oturur (`figure sit` ya da sedir) ya da koltuk değneğiyle durur.

Hiçbiri oyuncu benzerliği taşımaz. Var olan bir karakterin yalnızca rengi değiştirilmiş hâli olmamalı; saç biçimi, yüz, sakal ve kıyafet bakımından ayrışmalılar.

**2. Kareler** (örgüdeki 8 vuruş):
- `k19a`: alacakaranlıkta Kattegat girişinde kapüşonlu Ragnar, fısıldayan kalabalık.
- `k19b`: salonda dört oğul ve isim kartları.
- `k19c`: Ragnar tacı uzatıyor, oğullar başını çeviriyor.
- `k19d`: Ivar kollarını açmış; ışık yalnız ikisine düşüyor.
- `k20a`: sisli ormanda devasa yaşlı ağaç, altında küçük ve bükük Ragnar, dallarda kuzgunlar. Ölçekle büyüt: ağaç kadrajı doldurur.
- `k20b`: yakın plan, kopmuş ip ucunu gagalayan iki kuzgun; yerde gözleri açık, gökyüzüne bakan Ragnar.
- `k21a`: boş iskele, tek gemi, koltuk değnekli Ivar.
- `k21b`: sabah kıyısında enkaz arasında Ragnar ve Ivar.

**HASSAS:** `k20a` ve `k20b`'de intihar yöntemi gösterilmez. Boyunda ip yok, asılı beden yok, ilmek yok. Yalnızca dalda kopmuş ve sarkan bir ip ucu ile kuzgunlar görünür. Ton hüzünlü ve ölçülü, ürkütücü değil.

**Bütçe:** en fazla 2 öz değerlendirme turu ve yaklaşık 40 araç çağrısı. R13 kırpmaları: model kartı, `k19c`, `k20a`, `k20b`.
