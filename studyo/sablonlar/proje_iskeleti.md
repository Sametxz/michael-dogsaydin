# Yeni proje iskeleti

F0'da bu yapı kurulur:

```
projeler/<slug>/
├── CLAUDE.md                 # sablonlar/CLAUDE_proje_sablonu.md'den doldurulur
├── OTURUM_DEVRI.md           # sablonlar/OTURUM_DEVRI_sablonu.md
├── karar_gunlugu.md          # sablonlar/karar_gunlugu_sablonu.md
├── lore_bible.md             # F1: kronolojik olay tablosu, sezon/bölüm kaynaklı
├── omurga.md                 # F2: tema, çapa, bölümler, ekim-biçim, motifler, duygu eğrisi
├── dokum/
│   └── bolum_<X>.json        # F4a: sahne dökümü (dokum_kontrol.py'den geçer)
├── orgu/
│   └── bolum_<X>_v<N>.md     # F4a: kullanıcıya giden örgü tablosu
├── karakter.py               # F3: eklemli karakterler (art3 tabanlı) + kimlik öğeleri (tek kaynak)
├── mekan.py                  # F3: mekân setleri (katmanlı öğe fabrikaları)
├── kareler/                  # F4c: çekim modülleri (her bölüm ayrı dosya)
├── bolum_<X>.py              # F4d: Cekim + Film tanımı, render
├── ses/                      # TTS satırları (wav git dışı, .kelime.json repoda)
├── kurul/
│   ├── DERSLER.md
│   └── <bolum>/              # kontakt_960.png, kırpmalar, pano/rapor
├── final/                    # usta video (git dışı), altyazı, yayin.md
└── kapak/
```

`.gitignore` eklentisi:
```
projeler/*/ses/*.wav
projeler/*/ses/*.mp3
projeler/*/out/
projeler/*/final/*.mp4
projeler/*/kapak/*_2560.png
```

Kod göreli yolla çalışır:
```python
from pathlib import Path; import sys
P = Path(__file__).resolve().parent; REPO = P.parents[1]
sys.path[:0] = [str(REPO / "studyo/motor"), str(REPO / "r3"), str(REPO / "r2")]
```
