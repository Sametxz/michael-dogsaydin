"""Yayın paketi: bölüm zaman damgaları + 8 dilde SRT altyazı (satırlar anlatımın gerçek başlangıç saniyesine kilitli).
python3 yayin.py → final/altyazi/ragnar_<dil>.srt, final/bolumler.json"""
import json, os, re, soundfile as sf, textwrap
R = "/home/claude/r3"; Z = json.load(open(f"{R}/ses2/zaman.json"))
SIRA = ["prolog", "I", "II", "III", "IV", "V", "VI"]; KES = {"I": 0.55}   # birlestir.py ile aynı: Bölüm I başından 0,55 sn kırpılıyor
DILLER = ["tr", "en", "es", "pt-BR", "de", "fr", "ar", "ru"]

def olaylar():
    t0 = 0.0; ev = []; bol = []
    for b in SIRA:
        k = KES.get(b, 0.0); bol.append((b, t0))
        for p in Z[b]["parts"]:
            for w, s in p["voice"]:
                a = t0 + p["offset"] + s - k; ev.append((w, a, a + sf.info(w).duration))
        t0 += Z[b]["dur"] - k
    return ev, bol, t0

def ts(x):
    h, r = divmod(max(0.0, x), 3600); m, s = divmod(r, 60); return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{int(round((s - int(s)) * 1000)) % 1000:03d}"

def parcala(txt, ad=42):
    """Uzun satırı cümle sınırından bloklara böler; her blok en fazla 2 satır × 42 karakter."""
    cumle = re.split(r"(?<=[.!?…])\s+", txt.strip()); bloklar = []; cur = ""
    for c in cumle:
        if len(cur) + len(c) + 1 <= ad * 2: cur = (cur + " " + c).strip()
        else:
            if cur: bloklar.append(cur)
            while len(c) > ad * 2:
                kes = c.rfind(" ", 0, ad * 2); bloklar.append(c[:kes]); c = c[kes + 1:]
            cur = c
    if cur: bloklar.append(cur)
    return ["\n".join(textwrap.wrap(b, ad)) for b in bloklar]

if __name__ == "__main__":
    ev, bol, tot = olaylar(); os.makedirs(f"{R}/final/altyazi", exist_ok=True)
    for dil in DILLER:
        M = {x["out"]: x["text"] for x in json.load(open(f"{R}/anlatim/master_{dil}.json"))}
        M[f"{R}/tahta/ses/K7_0.wav"] = M[f"{R}/paris/ses/r00.wav"]; M[f"{R}/tahta/ses/K8_0.wav"] = M[f"{R}/paris/ses/r11.wav"]   # köprü kopyaları
        if dil == "tr":   # seslendirme için fonetik yazılan adlar → ekran kartlarındaki doğru yazım
            AD = {"Lodbrok": "Lothbrok", "Atelstan": "Athelstan", "Biyorn": "Bjorn", "Aslog": "Aslaug", "Lagerta": "Lagertha", "Ekbert": "Ecbert", "Gida": "Gyda", "Vitserk": "Hvitserk", "İvar": "Ivar"}
            M = {k: re.sub("|".join(AD), lambda m: AD[m.group(0)], v) for k, v in M.items()}
        out = []; n = 1
        for w, a, e in ev:
            bl = parcala(M[w]); L = sum(len(b) for b in bl)
            t = a
            for b in bl:   # blok süresi karakter payına göre
                d = (e - a) * len(b) / L; out.append(f"{n}\n{ts(t)} --> {ts(t + d)}\n{b}\n"); n += 1; t += d
        open(f"{R}/final/altyazi/ragnar_{dil}.srt", "w", encoding="utf-8").write("\n".join(out))
        print(dil, n - 1, "blok")
    json.dump({"bolumler": [[b, round(t, 2)] for b, t in bol], "toplam": round(tot, 2)}, open(f"{R}/final/bolumler.json", "w"))
    for b, t in bol: print(b, f"{int(t // 60)}:{int(t % 60):02d}")
    print("toplam", round(tot, 2))
