# Kalite standardı (Ragnar çıtası + dinamik anlatım)

Bu belge kısa ve uygulanabilir özettir. Ayrıntılı ölçütler, puanlama ve eşikler Ragnar'da olgunlaştı: `ragnar_kaynak/GORSEL_STANDART.md` (v1.1 + R9–R13). Yeni projede o metin **aynen geçerlidir**, bu belge onun üstüne dinamik anlatım ölçütlerini ekler.

## 1. Çıta
- **Görsel:** "Temiz, gölgeli, sinematik 2D." Referans kareler `studyo/referans/`:
  - `kahraman_kare_hero_v4.jpg`: yakın plan, yönlü ışık, tek sıcak vurgu, etkileşim kompoziti.
  - `toren_cenaze_d3.jpg`: tören ihtişamı, gece ışığı, kalabalık.
  - `firtina_gemi_e4.jpg`: atmosfer ve kahraman nesne.
  - `holmgang_e7.jpg`: kalabalık çemberi, derinlik.
- **Hareket:** Her çekim yaşar (D2), her cümle görünür (D1), çekimler akar (D4–D5).
- **Duygu:** Yedi kanal (`03_DUYGU_DILI.md`).

## 2. Kesin red listesi (kare ya da video YETERSİZ)
| Kod | Kural |
|---|---|
| R1 | Oyuncu benzerliği ya da dizideki imza karakter tasarımının kopyası |
| R2 | Duygu ile ifade çelişiyor (acı anında gülümseme) |
| R3 | Kimlik sızıntısı (bir karakterin yarası, dövmesi başka karakterde) |
| R4 | Kopuk ya da havada uzuv, boyunsuz kafa |
| R5 | Döndürülmüş sprite ile sahte poz (ayakta figürü yatırmak) |
| R6 | Çift nesne (aynı nesne aynı anda iki yerde; geçişlerde de) |
| R7 | Pozlama hatası (L p95 < 0,15) |
| R8 | Kimlik öğesi elle yeniden çizilmiş (yalnızca tek kaynaktan çağrılır) |
| R9 | Zemin nesnenin üstüne çıkmış, temas gölgesi yok |
| R10 | Çizgi film sevimliliği (yuvarlak parlak göz, çubuk bacak, kutu ev) |
| R11 | Model dışı uydurma gövde |
| R12 | Kalabalık, tören ya da kahraman nesne cılız (ihtişam eksik) |
| R13 | Ana nesne %200 kırpmada vasat görünüyor (pruva, silah, taç) |
| **R14 (yeni)** | Ekranda 3 sn'den uzun hiçbir şeyin olmadığı aralık (D3) |
| **R15 (yeni)** | Anlatılan cümlenin ekranda karşılığı yok ya da 0,3 sn'den fazla gecikiyor (D1) |
| **R16 (yeni)** | Bölüm sonu dışında siyaha kararma (D4) |
| **R17 (yeni)** | Geçişte titreme, atlama, yön kırılması ya da göz noktasının sıçraması |

## 3. Her kare için zorunlu kalite kuralları (Ragnar Bölüm I v3'ten)
1. **En az 4 derinlik katmanı:** uzak, orta, sahne, ön plan çerçevesi. Atmosfer (sis, duman, toz, kar) katmanlar arasındadır. Yeni motorda bu katmanlar **ayrı Oge**'lerdir, böylece paralaks çalışır.
2. **Düz renk alan yok:** Her büyük yüzey dokulu (`r3/tex.py`), gökyüzü degrade ve bulut katmanlı.
3. **Işık kararıyla başla:** Kaynağı belli tek anahtar ışık; gölge tarafı, rim ışığı, temas gölgesi.
4. **6–12 anlamlı ayrıntı**, hepsi hikâyeye hizmet eder.
5. **Gövde her zaman modelden** gelir; kimlik öğeleri tek kaynaktan çağrılır.
6. Asimetrik kimlik işaretli karakter **aynalanmaz**, kompozisyon ters kurulur.
7. **Ara kare küçümsenmez:** 2 sn görünen insert de ana sahnenin çıtasını taşır.
8. **R13:** Her karenin en önemli 2 nesnesinin %200 kırpması alınır ve kontrol edilir.
9. **Öz değerlendirme döngüsü:** En az 2 tur, en fazla 4. Vasat kare teslim edilmez.

## 4. Video denetimi (F4d ve F6)
- Ses kapalı izleme: her 3 sn'de bir olay var mı (R14)?
- Ses açık izleme: her cümle görünür mü, kilit gecikmesi ≤ 0,3 sn mi (R15)?
- Geçiş listesi: her geçişin bağı okunuyor mu, R17 var mı?
- Whisper anlaşılabilirlik testi: miks, kuru sesle ±%3 içinde.
- Ses dengesi: konuşma arka plandan 10–13 dB yukarıda, −16 LUFS.

## 5. Kontrol görselleri
- `kontakt_960.png`: bütün anahtar kareler + geçiş orta kareleri.
- `kontrol_kucuk.png`: 1/8 boyut (siluet ve göz yolu).
- R13 kırpmaları.
- Blok animatik ve tam animatik için `ffmpeg -ss` ile her geçişin ortasından kare.
