# CLAUDE.md: "<KARAKTER> Olarak Doğsaydın?" projesi

Yeni bir oturumda bu dosyayı **ilk** oku. Ardından şunları oku: `OTURUM_DEVRI.md`, `karar_gunlugu.md` (son 3 tur), `studyo/docs/02_DINAMIK_ANLATIM.md`, `studyo/docs/03_DUYGU_DILI.md`, `studyo/docs/06_DERSLER.md`.

## Ne yapıyoruz
Born in Lore formatında, ikinci tekil şahısla anlatılan <SÜRE> dakikalık Türkçe 2D animasyon. Konu: <KARAKTER>'in **<DİZİ> dizisindeki** hayatı (<SEZONLAR>). Kişisel, ticari değil.

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
- Oyuncuya benzeyen yüz çizilmez. Dizideki imza karakter tasarımı kopyalanmaz. <BU KARAKTERE ÖZGÜ YASAK KOMBİNASYON>.
- Dizinin müziği, ekran görüntüsü ve gerçek kişi fotoğrafı kullanılmaz. Kan ve vahşet gösterilmez.
- API anahtarları yalnızca `/home/claude/.secrets/` altında durur, asla repoya girmez.

## Kullanıcı tercihleri
(`studyo/docs/06_DERSLER.md §1` geçerli; bu projeye özgü yeni tercihler buraya eklenir)

## Teknik
`studyo/docs/07_TEKNIK_HAT.md`. Motor `studyo/motor/`, karakter sistemi `r3/art3.py`, ses `tts/el.py` + `r3/ses2/`, yayın `r3/final/`, kapak `r3/kapak/`.

## Sıradaki iş
`OTURUM_DEVRI.md` → "Açık işler".
