# Brief: Tüm film denetimi ve efekt işaret listesi (20.11.2026)
Kullanıcının isteği:
- Her bölümün kareleri gözden geçirilecek.
- Anlatım efektlerle desteklenecek: ateş, kuzgun uçuşu, mızraklar, ifade ve jestler.
- Ragnar yükseliş döneminde kahraman görünmeli; düşüşte zayıflamış ve yaşlanmış olmalı.
- Her sahnenin "olması gerektiği gibi görünüp görünmediği" mantık analiziyle denetlenecek.

## Girdiler
- Anlatım (sıra ve satır metinleri): `/home/claude/r3/anlatim/master_tr.json`. `out` yolu hangi bölüme ait olduğunu gösterir.
- Bölüm kontakt sayfaları (çekim sırasıyla):
  - prolog: `prolog/kontakt_prolog_960.png` (p1a…p3c)
  - Bölüm I: `bati/v3/kontakt_v3_960.png` (f1–f10) ve `bati/kontakt5_960.png` (e1–e8)
  - Bölüm II: `bedel/kontakt4_960.png` (d1–d8), `veda2/kontakt2_960.png` (sahne 7), `ivar2/kontakt_960.png` (sahne 9)
  - Bölüm III: `kesis/kontakt3_960.png` (a1–c1)
  - Bölüm IV: `paris/kontakt_paris_960.png`
  - Bölüm V: `kayip/kontakt_kayip_960.png`
  - Bölüm VI: `son/kontakt_son_960.png`

  Tüm yollar `/home/claude/r3/` altındadır.
- Çekim ve satır eşleşmesi: animatik betiklerindeki PLAN/PA/PB listeleri (`bati/anim1.py`, `anim_prolog.py`, `anim_paris.py`, `anim_kayip.py`, `anim_son.py`, `bedel/anim2b.py`, `kesis/anim3k.py`). Her öğe `("çekim_id", [(satır_no, boşluk)], kuyruk)` biçimindedir.
- Ragnar'ın yaş evreleri: `/home/claude/r3/ragnar_yas.py` ve `kurul/model_ragnar_yas.png`. Evreler: 1 çiftçi, 2 jarl/kral, 3 düşüş, 4 son.
- Standart: `kurul/GORSEL_STANDART.md` ve `kurul/DERSLER.md` → KÖK NEDEN ANALİZİ.

## Yapılacaklar
1. **Mantık ve süreklilik analizi.** Her çekim için şu sorular sorulur:
   - Anlatılan şey gösteriliyor mu?
   - Karakter doğru yerde ve doğru yaşta mı? Ragnar'ın evresi doğru mu?
   - Nesne sürekliliği tutuyor mu (kol halkaları, Athelstan'ın haçı, güneş taşı, taç, kuzgun broş)?
   - Zaman mantığı doğru mu (gece/gündüz, mevsim)?
   - Dizi akışıyla çelişen bir şey var mı?
   - Sahnede eksik olan ne?
2. **Efekt işaretleri.** Her çekime en fazla 3 efekt önerilir, yalnızca hikâyeyi güçlendirenler. Kullanılabilecek efekt türleri:
   - `fire` (x,y,ölçek): titreyen alev + ışık
   - `embers` (alan): uçuşan kıvılcım
   - `smoke` (alan): sürüklenen duman
   - `ravens` (yol: başlangıç→bitiş, adet): uçan kuzgunlar
   - `arrows` (kaynak→hedef, adet): ok yağmuru
   - `spear` (kaynak→hedef): atılan mızrak
   - `shake` (şiddet, süre): kamera sarsıntısı
   - `flash` (renk): ani ışık
   - `light_flicker`: mum/meşale titreşimi
   - `rain`, `snow`, `dust`
   - `push` (kamera yavaş itme yönü)

   Zamanlama satıra bağlanır: `"at": "L<satır_no>+<saniye>"` ya da `"at": "S+<saniye>"` (çekim başından itibaren). Koordinatlar 1920×1080 kare üzerindedir; kontakt sayfasındaki 960 px'lik görüntüden kabaca tahmin et (ikiyle çarp).
3. **Oyunculuk notları.** Sahnenin duygusunu taşıyan çekimler için ifade ve jest önerilir. Örnekler: `"Biliyorum"`da Ragnar'ın gözleri kısılır; "Kimse istemiyor"da oğullar bakışlarını kaçırır. Bunlar sonraki aşamada yalnızca seçilmiş karelere uygulanacak; en fazla 12 tane, en etkili olanlar.
4. **Ragnar evresi.** Her çekimde olması gereken evre (1–4) belirtilir ve şu anki kareyle uyuşmayanlar işaretlenir.

## Çıktılar
- `/home/claude/r3/kurul/denetim_v1.md`: Türkçe ve kısa. Önce en önemli 15 sorunu önem sırasıyla yaz (çekim, sorun, önerilen düzeltme). Ardından bölüm bölüm birer satırlık genel not ekle.
- `/home/claude/r3/fx/isaretler.json`:
  ```
  [{"bolum": "...", "cekim": "...", "evre": 1-4, "evre_uyumsuz": bool, "fx": [...], "oyunculuk": "...", "sorun": "..."}]
  ```
  `fx` alanı, işaret ve efekt tanımlarının listesidir.

**Bütçe:** yaklaşık 30 araç çağrısı. Kontakt sayfalarını bir kez oku; tek tek kare okuma yalnızca şüpheli 5 kare için.
