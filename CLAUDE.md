# CLAUDE.md: michael-dogsaydin stüdyosu

Bu repo, "X Olarak Doğsaydın?" (Born in Lore formatı) videolarının **yeni ana reposudur**. Ragnar projesinden (`Sametxz/ragnar-dogsaydin`, tamamlandı) stüdyo paketi, motor ve kod kütüphanesi buraya taşındı (26.11.2026). Geliştirme bu repodan sürer.

## Yeni oturumda okuma sırası
1. `docs/OTURUM_DEVRI.md` (nerede kaldık, açık işler)
2. `studyo/BASLA.md` ve oradaki okuma sırası (`studyo/docs/02` → `03` → `01` → `06`)
3. Aktif proje varsa `projeler/<slug>/CLAUDE.md`, `OTURUM_DEVRI.md`, `karar_gunlugu.md` (son 3 tur)

## En önemli kural: dinamik anlatım (kullanıcı, 26.11.2026)
Her söylenen cümle ekranda hayata geçer, öğesi o kelimede gelir ve hareket eder. Sahneler anlamsal geçişlerle akar (ör. öğe pencerede belirir, sonraki sahne pencereden devam eder). Duygu görsel öğelerle taşınır. → `studyo/docs/02_DINAMIK_ANLATIM.md` (D1–D10), `03_DUYGU_DILI.md`, denetçi `studyo/motor/dokum_kontrol.py`.

## Çalışma kuralları (Ragnar'dan aynen geçerli)
- Önce örgü → blok animatik → ham kareler → animatik. Her kapıda kullanıcı onayı.
- Hiçbir yeni kare (insert ve geçiş karesi dahil) kullanıcı onayı olmadan animatiğe, sese ya da videoya girmez. Görsel yeterliliği kullanıcı belirler.
- Kararlar AskUserQuestion ile, önerilen seçenek ilk sırada; kullanıcının önceki açık istekleri her zaman seçenek olarak sunulur.
- Kredi tasarrufu: bölüm başına en fazla 2 ajan çağrısı, ara kontroller 960 px.
- Her tur sonunda karar günlüğüne kayıt + **Ders**; commit + push `main` dalına.

## Değişmez sınırlar
- Oyuncuya benzeyen yüz çizilmez; dizideki imza karakter tasarımı kopyalanmaz.
- Dizinin müziği, ekran görüntüsü, gerçek kişi fotoğrafı kullanılmaz. Kan ve vahşet gösterilmez.
- API anahtarları yalnızca `/home/claude/.secrets/` altında (chmod 600); repoya, loga, commit'e girmez. İş bitince kullanıcıya iptal etmesi hatırlatılır.

## Repo haritası
```
studyo/        başlangıç paketi: docs/, motor/ (dinamik sahne motoru), sablonlar/, skills/, referans/
projeler/      her video kendi klasöründe (F0'da kurulur)
r2/ r3/        Ragnar kod kütüphanesi (yalnız kod; medya ragnar-dogsaydin reposunda)
               karakter r3/art3.py · doku r3/tex.py · efekt r3/fx/efekt.py · ses r3/ses2/ · yayın r3/final/ · kapak r3/kapak/
tts/           ElevenLabs (el.py) ve yedek XTTS betikleri
docs/ragnar/   Ragnar'ın PIPELINE, AJANLAR ve oturum devri belgeleri
fonts/  skills/  scripts/setup.sh
```
Eski r2/r3 kodu `/home/claude/r2`, `/home/claude/r3` mutlak yollarını kullanır; `setup.sh` bu yolları repoya bağlar. Yeni kod `projeler/<slug>/` altında **göreli yol** kullanır.

## Kurulum
`bash scripts/setup.sh` → ElevenLabs anahtarları `/home/claude/.secrets/elevenlabs_key` (TTS+SFX) ve `elevenlabs_key2` (müzik) → `cd studyo/motor && python3 ornek/demo.py onizle`.
