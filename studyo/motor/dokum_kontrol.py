"""Sahne dökümü denetçisi: dinamik anlatım kurallarını (D1–D10) otomatik kontrol eder.

    python3 dokum_kontrol.py ../sablonlar/sahne_dokumu_ornek.json

Döküm biçimi: sablonlar/sahne_dokumu.schema.md. Hata (✗) varsa döküm kullanıcıya gönderilmez, önce düzeltilir.
Uyarı (⚠) kullanıcı sunumunda gerekçesiyle belirtilir.
"""
import json, math, re, sys
from duygu import KALIP

ANLAMSAL = {"maske", "zoom_icinden", "nesne_tasi", "eslesme", "on_plan_sil", "savurma"}
GIRISLER = {"pop", "dus", "kay_sol", "kay_sag", "yuksel", "belir", "parla", "ciz", "buyu", "eylem"}

def cumleler(metin): return [c.strip() for c in re.split(r"(?<=[.!?…])\s+", metin.strip()) if c.strip()]
def kelimeler(c): return re.findall(r"[\wçğıöşüÇĞİÖŞÜâîû']+", c.lower())

def denetle(dokum):
    hatalar, uyarilar = [], []
    H = lambda k, m: hatalar.append(f"✗ {k} · {m}"); U = lambda k, m: uyarilar.append(f"⚠ {k} · {m}")
    tum = [(b, ck) for b in dokum["bolumler"] for ck in b["cekimler"]]
    gecis_say = anlamsal = 0; plan_seri = []
    for bi, bol in enumerate(dokum["bolumler"]):
        cks = bol["cekimler"]
        for ci, ck in enumerate(cks):
            k = ck["id"]; ogeler = ck.get("ogeler", []); son_cekim = ci == len(cks) - 1
            # D1 cümle → görsel karşılık
            for c in cumleler(ck.get("anlatim", "")):
                kw = set(kelimeler(c))
                if not any(o.get("kelime", "").lower() in kw or any(o.get("kelime", "").lower() in w for w in kw) for o in ogeler if o.get("kelime")):
                    H(k, f"D1 cümlenin ekranda karşılığı yok: «{c}» (bu cümleden bir kelimeye kilitli öğe ekle)")
                if len(kelimeler(c)) > 12: U(k, f"D8 cümle 12 kelimeden uzun ({len(kelimeler(c))}): «{c}»")
            # D2 hareket: giriş + kamera + ikincil
            if not any(o.get("giris") in GIRISLER for o in ogeler): H(k, "D2 sahneye giren ya da eylem yapan öğe yok")
            if not ck.get("kamera"): H(k, "D2 kamera hareketi yazılmamış")
            if not ck.get("ikincil"): U(k, "D2 ikincil (yaşam) hareketi yazılmamış: nefes, salınım, duman, su…")
            # D3 durağanlık: her ~3 sn'de bir olay
            sure = float(ck.get("sure_tahmini", 0)); olay = sum(1 for o in ogeler if o.get("kelime")) + len(ck.get("eylemler", []))
            if sure and olay < math.ceil(sure / 3.0): H(k, f"D3 {sure:.1f} sn için {olay} olay; en az {math.ceil(sure / 3)} gerekli")
            # D4/D5 geçiş
            g = ck.get("gecis_sonraki", {}); tur = g.get("tur", "kes")
            if not (bi == len(dokum["bolumler"]) - 1 and son_cekim):
                gecis_say += 1; anlamsal += tur in ANLAMSAL
                if tur == "karart" and not son_cekim: H(k, "D4 siyaha kararma yalnızca bölüm sonunda")
                if tur in ANLAMSAL and not g.get("bag"): H(k, f"D5 {tur} geçişinin anlam bağı yazılmamış (A'daki ne → B'deki ne)")
                if tur in ("maske", "nesne_tasi", "eslesme", "zoom_icinden"):
                    adlar = {o["ad"] for o in ogeler}
                    if g.get("oge_a") not in adlar: H(k, f"D5 {tur}: oge_a «{g.get('oge_a')}» bu çekimin öğelerinde yok")
                    nxt = cks[ci + 1] if not son_cekim else dokum["bolumler"][bi + 1]["cekimler"][0]
                    if tur in ("nesne_tasi", "eslesme") and g.get("oge_b") not in {o["ad"] for o in nxt.get("ogeler", [])}:
                        H(k, f"D5 {tur}: oge_b «{g.get('oge_b')}» sonraki çekimde ({nxt['id']}) yok")
                if tur == "kes" and not g.get("gerekce"): U(k, "D4 sert kesmenin gerekçesi yok (şok/ritim/ses vuruşu?)")
            # D6 duygu
            if ck.get("duygu") not in KALIP: H(k, f"D6 duygu «{ck.get('duygu')}» tanımsız ({', '.join(KALIP)})")
            if not ck.get("duygu_tasiyici"): H(k, "D6 duyguyu taşıyan görsel öğe yazılmamış (yüz, el, nesne, ışık, hava)")
            # D7 plan çeşitliliği
            plan_seri.append(ck.get("plan", "?"))
            if len(plan_seri) >= 4 and len(set(plan_seri[-4:])) == 1: U(k, f"D7 art arda 4 çekim aynı plan ölçeğinde ({plan_seri[-1]})")
            # D9 ses
            if ck.get("vurucu") and not (ck.get("ses", {}).get("efekt") and ck.get("vfx")): H(k, "D9 vurucu cümle görsel efekt + ses efekti ister")
        # D10 bölüm sonu
    if gecis_say and anlamsal / gecis_say < 0.6: H("genel", f"D4 anlamsal geçiş oranı %{100 * anlamsal / gecis_say:.0f} (< %60)")
    return hatalar, uyarilar, (anlamsal, gecis_say)

if __name__ == "__main__":
    d = json.load(open(sys.argv[1])); h, u, (a, g) = denetle(d)
    n = sum(len(b["cekimler"]) for b in d["bolumler"]); sure = sum(float(c.get("sure_tahmini", 0)) for b in d["bolumler"] for c in b["cekimler"])
    print(f"{n} çekim · ~{sure:.0f} sn · anlamsal geçiş {a}/{g}")
    for x in h + u: print(x)
    print("SONUÇ:", "GEÇTİ" if not h else f"{len(h)} hata — düzelt")
    sys.exit(1 if h else 0)
