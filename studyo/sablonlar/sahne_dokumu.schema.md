# Sahne dökümü şeması (`dokum/bolum_X.json`)

Bir bölümün çekim çekim, cümle cümle dökümü. `motor/dokum_kontrol.py` bu alanları denetler. Örnek: `sahne_dokumu_ornek.json`.

```jsonc
{
  "proje": "slug",
  "bolumler": [{
    "ad": "II · Bedel",
    "cekimler": [{
      "id": "2.04",                       // bölüm.sıra
      "anlatim": "En fazla 2 cümle. Her biri ≤ 12 kelime.",
      "sure_tahmini": 4.5,                // sn; TTS sonrası gerçek süreyle güncellenir
      "plan": "genis | orta | yakin | detay",
      "duygu": "huzur",                   // motor/duygu.py KALIP anahtarı
      "duygu_donusum": {"hedef": "yas", "kelime": "öldü"},          // isteğe bağlı: çekim içi dönüşüm
      "duygu_tasiyici": "Hangi görsel öğe duyguyu taşıyor (yüz, el, ışık, hava, sembol nesne)",
      "ogeler": [                         // her cümleden en az biri kelimeye kilitli (D1)
        {"ad": "kuzgun", "kelime": "kuzgun", "giris": "dus", "eylem": "dala konar, başını çevirir"},
        {"ad": "ragnar", "kelime": "dönüyor", "giris": "eylem", "eylem": "başını kuzguna çevirir, kaşları çatılır"}
      ],
      "eylemler": ["isteğe bağlı: kelimeye bağlı olmayan ek olaylar"],
      "kamera": "yavaş itme yüze, 1.0 → 1.12",
      "ikincil": ["pelerin rüzgârda", "nefes", "kar"],
      "katmanlar": ["gök 0.05", "dağ 0.3", "orman 0.7", "ana 1.0", "ön plan dal 1.4"],
      "vurucu": false,                    // true ise vfx + ses.efekt zorunlu (D9)
      "vfx": "flaş / sarsıntı / ışık patlaması / ağır çekim",
      "gecis_sonraki": {
        "tur": "maske | nesne_tasi | eslesme | zoom_icinden | on_plan_sil | savurma | kes | karart",
        "oge_a": "bu çekimdeki öğe adı",   // maske, nesne_tasi, eslesme, zoom_icinden için
        "oge_b": "sonraki çekimdeki öğe",  // nesne_tasi, eslesme için
        "bag": "A'daki ne → B'deki ne, neden",
        "gerekce": "kes için: şok / ritim / ses vuruşu"
      },
      "ses": {"ambiyans": "rüzgâr, uzak dalga", "efekt": ["kanat çırpışı 'kuzgun'"], "muzik": "isteğe bağlı not"}
    }]
  }]
}
```

## Yazım notları
- `ogeler[].kelime`: Cümledeki kelimenin kökü yeterlidir ("kuzgun" → "kuzgunlar" eşleşir). Motor `ck.k()` aynı kısmi eşleşmeyi kullanır.
- `giris`: `pop, dus, kay_sol, kay_sag, yuksel, belir, parla, ciz, buyu` ya da `eylem` (öğe zaten sahnede, kelimede bir şey yapıyor).
- Sessiz çekim (anlatımsız, geçiş nefesi) için `anlatim: ""` yazılır. D1 uygulanmaz, D2–D3 uygulanır.
- Bölümün son çekiminde `gecis_sonraki.tur` genellikle `karart` olur, ya da sonraki bölümün motifine bağlanan anlamsal bir geçiş.
