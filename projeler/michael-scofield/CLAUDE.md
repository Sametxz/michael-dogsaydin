# CLAUDE.md: "Michael Scofield Olarak Doğsaydın?" projesi

Yeni bir oturumda bu dosyayı **ilk** oku. Ardından şunları oku: `OTURUM_DEVRI.md`, `karar_gunlugu.md` (son 3 tur), `studyo/docs/02_DINAMIK_ANLATIM.md`, `studyo/docs/03_DUYGU_DILI.md`, `studyo/docs/06_DERSLER.md`.

## Ne yapıyoruz
Born in Lore formatında, ikinci tekil şahısla anlatılan ~9 dakikalık Türkçe 2D animasyon (prolog + 6 bölüm). Konu: Michael Scofield'ın **Prison Break dizisindeki** hayatı (S1–S4 + The Final Break). S5 (2017) kapsam dışı. Kişisel, ticari değil.

## En önemli kural: dinamik anlatım (kullanıcı, 26.11.2026)
> Her söylenen cümle ekranda hayata geçsin. Cümlenin öğesi o anda ekrana gelsin ve mümkün olduğunca hareketli olsun. Sahneler arası anlamsal geçişler olsun (ör. öğe pencerede belirsin, sonraki sahne pencereden devam etsin). Duygular görsel öğelerle aktarılsın.
→ D1–D10 (`studyo/docs/02`), duygu kanalları (`studyo/docs/03`), denetçi `studyo/motor/dokum_kontrol.py`.

## Çalışma kuralları
1. Önce örgü: görsel üretimden önce cümle cümle örgü + süre kullanıcıya gider.
2. Hareket taslağı (blok animatik) onaylanmadan son kalite kare çizilmez.
3. Katı denetim: hiçbir yeni kare (insert ve geçiş karesi dahil) kullanıcı onayı olmadan animatiğe, sese ya da videoya girmez. Sıra: öz değerlendirme (≥ 2 tur, R13) → kurul (tek ajan) → kullanıcı.
4. Ses ve video onaydan sonra üretilir.
5. Kararlar AskUserQuestion ile sorulur, önerilen seçenek ilk sırada.
6. Kredi tasarrufu: bölüm başına en fazla 2 ajan çağrısı. Ara kontroller 960 px'de yapılır.
7. Her tur sonunda `karar_gunlugu.md`'ye kayıt + **Ders** eklenir. Commit + push `main` dalına yapılır.

## Değişmez sınırlar
- Oyuncuya (Wentworth Miller) ya da diğer oyunculara benzeyen yüz çizilmez.
- **Bu karaktere özgü kopya yasağı:** Dizideki gerçek dövme sanat eserinin (üst gövde ve kolları kaplayan, şeytan/melek figürlü, belirli kompozisyonlu "Fox River planı" dövmesi) birebir ya da tanınır kopyası çizilmez. Dövme hikâyenin merkezi olduğu için **özgün** bir tasarımla verilir: gizli plan çizgilerinin süslemeye gömüldüğü, kendi motiflerimizle kurulan bir desen. Dövme + kısa kazınmış saç + mavi hapishane gömleği üçlüsü, oyuncu yüzü olmadan kullanılabilir (genel öğeler). F3'te ayrıntılı sınır netleştirilecek.
- Dizinin müziği, logosu, ekran görüntüsü ve gerçek kişi fotoğrafı kullanılmaz. Kan ve vahşet gösterilmez (ör. parmak kesme, işkence sahneleri yalnızca ima, ışık ve sesle).
- API anahtarları yalnızca `/home/claude/.secrets/` altında durur, asla repoya girmez.

## Kullanıcı tercihleri
(`studyo/docs/06_DERSLER.md §1` geçerli; bu projeye özgü yeni tercihler buraya eklenir)
- Anlatıcı: George değil, yeni bir ElevenLabs sesi (örnek dinletilerek seçilecek). **Şimdilik yerel TTS** (XTTS, kredi harcamaz) kullanılır; her şey hazır olunca ses ElevenLabs'ten alınır (kullanıcı, 26.11.2026 15:53).
- **Taslaklar düşük çözünürlükte** (960 px ya da daha düşük) üretilir; **içerik ve çizim kalitesi her zaman tam çıtadadır** (kullanıcı düzeltmesi, 26.11.2026 16:07: "düşük kalite = çözünürlük, içerik kalitesi yüksek olsun"). Tam çözünürlük yalnızca tamamlanmış, yayına hazır video için yapılır. Amaç token ve kredi tasarrufu.
- **Bütün karar aşamalarında kullanıcıya sorulur** (karar verici ajan kullanılmaz).
- Anlatım sıkıcı olmamalı: sürekli akan, geçişli, dinamik; neredeyse her cümle sahnede karşılık bulur.
- **Ragnar stiline bağlı kalınmaz** (kullanıcı, 26.11.2026 16:08): görsel dil konuya (hapishane, plan, kaçış) ve yeni akışa göre seçilir. Öncelik: daha dinamik ve hareketli sahneler, her cümle ekranda yaşanır, akış yüksek, **ekranda tutuculuk (izleyiciyi tutma) artırılır**.
- **Görsel dil: B + A hibrit** (16:20): sinematik 2D dünya + Michael'ın 'plan görüşü' (camgöbeği plan çizgileri; aynı zamanda geçiş aracı). Tutuculuk: geri sayım sayacı, kinetik kilit kelimeler, görsel açık döngüler (`omurga.md §8`). Stil testi: `stil/stil_kontakt.png`.

## Teknik
`studyo/docs/07_TEKNIK_HAT.md`. Motor `studyo/motor/`, karakter sistemi `r3/art3.py`, ses `tts/el.py` + `r3/ses2/`, yayın `r3/final/`, kapak `r3/kapak/`. Kod göreli yol kullanır:
```python
from pathlib import Path; import sys
P = Path(__file__).resolve().parent; REPO = P.parents[1]
sys.path[:0] = [str(REPO / "studyo/motor"), str(REPO / "r3"), str(REPO / "r2")]
```

## Sıradaki iş
`OTURUM_DEVRI.md` → "Açık işler".
