"""Bölüm ses miksi v2: anlatım + Eleven Music + ElevenLabs ortam ve vurgu sesleri → videoya -c:v copy ile yeni ses.
Kurallar: konuşma her zaman net (müzik konuşma altında ~-8 dB ve 1,5–4 kHz bandı yumuşatılmış; ortam %55 kısılır),
sessizlik anları korunur, sonda -16 LUFS.  python3 miks.py [bölüm...]  →  <bölüm video>_ses2.mp4"""
import json, sys, os, subprocess, numpy as np, soundfile as sf
from scipy.signal import resample_poly, lfilter
H = "/home/claude/r3/ses2"; SR = 48000; LIB = f"{H}/lib"
Z = json.load(open(f"{H}/zaman.json"))
CUE = {}
for e in json.load(open("/home/claude/r3/fx/isaretler.json")): CUE[(e["bolum"], e["cekim"])] = e["fx"]

# ---------------------------------------------------------------- çekim → ortam (anahtar, kazanç)
AMB = {
 "prolog": dict(e5h=("city_burning", 1.0), p1a=("village", 0.9), p1b=("hall_crowd", 0.8), p1c=("church", 1.0), p1d=("shore", 0.9), p2a=("longhouse", 1.0),
                p2b=("snow_wind", 0.9), p2c=("longhouse", 1.0), p3a=("village", 0.9), p3b=("hall_crowd", 0.9), p3c=("shore", 0.9)),
 "I": dict(e5h=("city_burning", 1.0), f1=("village", 1.0), e1=("hall_crowd", 0.8), f2=("longhouse", 0.9), f3=("village", 0.8), e1b=("hall_crowd", 0.8), f4=("sea_storm", 0.75),
           f5=("longhouse", 0.9), e2=("longhouse", 0.9), e3=("shore", 1.0), f6=("shore", 0.9), e4=("sea_storm", 0.85), e4i=("sea_storm", 1.0), f7=("sea_rowing", 1.0),
           f8=("church", 1.0), e5r=("city_burning", 1.1), e6=("rain_light", 1.0), K0=("longhouse", 0.6), f9=("hall_crowd", 1.0), e7=("snow_wind", 1.0), f10=("snow_wind", 1.0), e8=("hall_crowd", 1.0)),
 "II": dict(K1=("longhouse", 0.6), d1=("longhouse", 0.8), d2=("longhouse", 0.7), d3=("shore", 0.9), K2=("longhouse", 0.6), d4=("battle", 0.9), d5=("snow_wind", 1.0), K3=("longhouse", 0.6),
            veda_1=("hall_crowd", 0.8), veda_2=("longhouse", 0.9), veda_3=("snow_wind", 1.0), veda_4=("snow_wind", 1.0), veda_5=("snow_wind", 1.0), veda_6=("snow_wind", 0.9),
            K4=("longhouse", 0.6), ivar_1=("longhouse", 0.8), ivar_2=("forest_mist", 1.0), ivar_4=("forest_mist", 0.8), ivar_5=("forest_mist", 1.0), K5=("longhouse", 0.6),
            d6=("longhouse", 0.9), d7=("longhouse", 0.9), d8=("hall_crowd", 1.0)),
 "III": dict(K6=("longhouse", 0.6), a1=("longhouse", 1.0), a2=("forest_mist", 1.0), b1=("longhouse", 0.8), b2=("forest_mist", 0.8), b3=("longhouse", 0.7), b4=("longhouse", 0.6),
             yas=("rain_light", 1.0), c1=("snow_wind", 0.8)),
 "IV": dict(K7=("longhouse", 0.6), p15b=("sea_rowing", 1.0), p15c=("siege", 1.1), p15d=("siege", 1.0), p15e=("siege", 0.8), p16a=("longhouse", 0.8), p16b1=("church", 1.0),
            p16b2=("church", 1.0), p16c=("rain_light", 0.8), p1c=("church", 1.0), p16e=("city_burning", 1.1), p17=("sea_rowing", 1.0), p18a=("longhouse", 0.8), K8=("longhouse", 0.6),
            p18c=("siege", 1.0), p18d=("battle", 1.0)),
 "V": dict(k19a=("shore", 1.0), k19b=("hall_crowd", 0.7), k19c=("hall_crowd", 0.6), k19d=("longhouse", 0.8), k20a=("forest_mist", 0.9), k20b=("forest_mist", 0.9),
           k21a=("shore", 1.0), k21b=("sea_storm", 0.8)),
 "VI": dict(k22a=("rain_heavy", 1.0), k22b=("longhouse", 1.0), k22c=("longhouse", 0.9), k23a=("shore", 1.0), k23b=("longhouse", 0.8), k24=("village", 0.9), k25a=("rain_heavy", 1.0),
            k25b=("forest_mist", 1.0), k26a=("church", 0.9), k26b=("pit", 1.0), k26c=("pit", 1.0), k26d=("pit", 0.8), f1=("village", 1.0), p1b=("hall_crowd", 0.8),
            k27b=("sea_rowing", 1.0), k27c=("shore", 1.0))}
# elle vurgular: (çekim, çekim içi sn, ses, kazanç)
SPOT = {
 "prolog": [("p1c", 1.6, "sp_drums_hit", 0.6), ("p2b", 0.4, "sp_horn1", 0.5), ("p3b", 0.5, "sp_crowd_cheer", 0.45)],
 "I": [("e5h", 0.0, "sp_fire_flare", 0.6), ("f6", 0.3, "sp_horn2", 0.5), ("e4", 0.5, "sp_waves_crash", 0.7), ("f7", 1.5, "sp_horn1", 0.35), ("e5r", 0.1, "sp_cheer_battle", 0.6),
       ("f9", 0.3, "sp_crowd_cheer", 0.4), ("e7", 0.2, "sp_axe_shield", 0.7), ("f10", 0.2, "sp_sword_clash", 0.7), ("f10", 0.8, "sp_body_snow", 0.9), ("f10", 1.1, "sp_crowd_gasp", 0.6),
       ("e8", 4.5, "sp_gold", 0.8), ("e8", 5.6, "sp_crowd_cheer", 0.5)],
 "II": [("d3", 0.3, "sp_fire_flare", 0.6), ("d4", 0.2, "sp_horn1", 0.45), ("d5", 0.5, "sp_axe_shield", 0.5), ("veda_1", 0.2, "sp_door", 0.5), ("veda_5", 0.5, "sp_steps_wood", 0.0),
        ("ivar_4", 0.4, "sp_heartbeat", 0.7), ("d7", 0.6, "sp_drums_hit", 0.4), ("d8", 0.2, "sp_horn1", 0.55), ("d8", 1.4, "sp_crowd_cheer", 0.5)],
 "III": [("b3", 0.6, "sp_drums_hit", 0.6), ("b4", 0.8, "sp_cross_chime", 0.5), ("c1", 0.3, "sp_raven1", 0.4)],
 "IV": [("p15b", 0.3, "sp_horn1", 0.5), ("p15c", 0.4, "sp_cheer_battle", 0.5), ("p16b1", 0.8, "sp_steps_wood", 0.35), ("p1c", 1.2, "sp_door", 0.6), ("p1c", 2.2, "sp_drums_hit", 0.5),
        ("p16e", 0.1, "sp_cheer_battle", 0.7), ("p18c", 0.4, "sp_horn2", 0.4)],
 "V": [("k21b", 0.3, "sp_waves_crash", 0.5)],
 "VI": [("k22a", 0.6, "sp_door", 0.45), ("k24", 2.6, "sp_cross_chime", 0.5), ("k25a", 0.2, "sp_cage", 0.8), ("k25a", 1.0, "sp_chain", 0.5), ("k26c", 4.4, "sp_heartbeat", 0.5),
        ("f1", 0.2, "sp_horn2", 0.4), ("k27b", 0.5, "sp_horn1", 0.45)]}
# sessizlik: (çekim, başlangıç sn, süre sn, müzik/ortam çarpanı)
HUSH = {"II": [("d2", 4.2, 3.6, 0.15), ("ivar_4", 2.0, 5.5, 0.35)], "III": [("b3", 1.2, 4.0, 0.25), ("b4", 0.0, 4.2, 0.4)],
        "VI": [("k26b", 2.2, 1.8, 0.2), ("k26c", 0.0, 1.0, 0.3)], "V": [("k20a", 1.0, 6.0, 0.45)]}
FIRTINA = {"f4", "e4", "e4i", "k21b", "k22a", "k25a", "e6", "p15d"}   # flaş = gök gürültüsü

_C = {}
def load(name, mono=False):
    if name not in _C:
        a, sr = sf.read(name if name.startswith("/") else f"{LIB}/{name}.wav", dtype="float32", always_2d=True)
        if sr != SR: a = resample_poly(a, SR, sr, axis=0).astype(np.float32)
        if a.shape[1] == 1: a = np.repeat(a, 2, 1)
        _C[name] = a
    return _C[name]
def rms_db(x): return 20 * np.log10(np.sqrt((x ** 2).mean()) + 1e-9)
def gain_to(x, db): return x * 10 ** ((db - rms_db(x)) / 20)
def loop(a, n, xf=SR):   # çapraz geçişli döngü
    out = np.zeros((n, 2), np.float32); L = len(a) - xf; i = 0; r = np.linspace(0, 1, xf, dtype=np.float32)[:, None]
    while i < n:
        seg = a.copy(); seg[:xf] *= r if i else 1; seg[-xf:] *= 1 - r
        e = min(n, i + len(seg)); out[i:e] += seg[:e - i]; i += L
    return out
def smooth(x, n):
    n = max(1, int(n)); return np.convolve(x, np.ones(n) / n, mode="same").astype(np.float32)
def peaking(x, f0, db, q=0.9):   # RBJ tepe süzgeci
    A = 10 ** (db / 40); w = 2 * np.pi * f0 / SR; al = np.sin(w) / (2 * q)
    b = [1 + al * A, -2 * np.cos(w), 1 - al * A]; a = [1 + al / A, -2 * np.cos(w), 1 - al / A]
    return lfilter(np.array(b) / a[0], np.array(a) / a[0], x, axis=0).astype(np.float32)

def miks(b):
    z = Z[b]; N = int(z["dur"] * SR) + 1; t = np.arange(N) / SR
    voice = np.zeros((N, 2), np.float32); amb = np.zeros((N, 2), np.float32); spot = np.zeros((N, 2), np.float32)
    def put(buf, a, s, g=1.0):
        i = int(s * SR); e = min(N, i + len(a))
        if i < N and e > i: buf[i:e] += a[:e - i] * g
    shots = []   # (fk, mutlak başlangıç, süre)
    for p in z["parts"]:
        for w, s in p["voice"]:
            a = load(w); put(voice, np.clip(gain_to(a, -19.0), -0.95, 0.95), p["offset"] + s)
        for k, t0, d, fk in p["shots"]: shots.append((fk, p["offset"] + t0, d))
    # ortam: çekim başına döngü, 0,6 sn çapraz geçiş
    for fk, s, d in shots:
        key, g = AMB[b].get(fk, ("longhouse", 0.5)); a = gain_to(load(f"amb_{key}"), -27.0)
        n = int((d + 1.2) * SR); seg = loop(a, n); f = np.ones(n, np.float32); x = int(0.6 * SR)
        f[:x] = np.linspace(0, 1, x); f[-x:] = np.linspace(1, 0, x); put(amb, seg * f[:, None], max(0, s - 0.6), g)
    # vurgular: işaretlerden + elle
    S0 = {fk: s for fk, s, d in shots}; bol = None if b == "prolog" else b
    for fk, s, d in shots:
        for c in CUE.get(("prolog" if b == "prolog" else b, fk), []):
            from_ = c.get("at", "S+0"); off = float(str(from_).split("+")[-1] or 0)
            if str(from_).startswith("L"): off += 0.0   # satır başına göre: çekim başına yakın kabul
            tur = c.get("tur"); at = s + off
            if tur == "ravens": put(spot, gain_to(load("sp_raven2" if c.get("adet", 2) > 1 else "sp_raven1"), -26), at + 0.3, 1.0)
            elif tur == "arrows": put(spot, gain_to(load("sp_arrow_volley"), -22), at, 1.0)
            elif tur == "spear": put(spot, gain_to(load("sp_spear"), -22), at, 1.0)
            elif tur == "flash": put(spot, gain_to(load("sp_thunder1" if fk in FIRTINA else "sp_drums_hit"), -22 if fk in FIRTINA else -28), at, 1.0)
            elif tur == "shake" and fk in FIRTINA: put(spot, gain_to(load("sp_thunder2"), -26), at, 1.0)
    for fk, off, nm, g in SPOT.get(b, []):
        if fk in S0 and g > 0: put(spot, gain_to(load(nm), -20), S0[fk] + off, g)
    # müzik: 1,5–4 kHz yumuşatma + konuşma altında kısma
    mu = load(f"{H}/muzik/{b}.wav")[:N]; mu = np.pad(mu, ((0, N - len(mu)), (0, 0)))
    mu = peaking(peaking(mu, 2500, -5.0, 0.7), 1200, -2.5, 1.0); mu = gain_to(mu, -25.5)
    vact = np.clip(smooth((np.abs(voice[:, 0]) > 0.015).astype(np.float32), 0.4 * SR) * 3, 0, 1)
    vact = smooth(vact, 0.25 * SR)
    hush = np.ones(N, np.float32)
    for fk, a0, d, m in HUSH.get(b, []):
        if fk in S0:
            s = S0[fk] + a0; hush *= np.interp(t, [0, s, s + 0.4, s + d, s + d + 0.8, t[-1] + 1], [1, 1, m, m, 1, 1]).astype(np.float32)
    mus = mu * ((1 - 0.6 * vact) * hush)[:, None]; am = amb * ((1 - 0.55 * vact) * hush)[:, None]
    out = voice + mus + am + spot * (1 - 0.5 * vact)[:, None]
    fade = np.minimum(1, t / 0.4) * np.minimum(1, (t[-1] - t) / 1.2); out *= fade[:, None].astype(np.float32)
    raw = f"{H}/out/{b}_raw.wav"; os.makedirs(f"{H}/out", exist_ok=True)
    sf.write(raw, np.clip(out / max(1.0, np.abs(out).max() / 0.95), -1, 1), SR)
    # kontrol: konuşma anlarında anlatım/arka plan oranı
    m = vact > 0.9; bg = mus + am + spot * (1 - 0.5 * vact)[:, None]
    print(b, "konuşma-arka plan farkı dB", round(rms_db(voice[m]) - rms_db(bg[m]), 1), "| boşlukta müzik dB", round(rms_db(mus[vact < 0.05]), 1), flush=True)
    wav = f"{H}/out/{b}.wav"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", raw, "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "48000", "-ac", "2", wav], check=True); os.remove(raw)
    vid = z["video"]; out_v = vid.replace(".mp4", "_ses2.mp4")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", vid, "-i", wav, "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", out_v + ".tmp.mp4"], check=True)
    os.replace(out_v + ".tmp.mp4", out_v); return out_v

if __name__ == "__main__":
    for b in (sys.argv[1:] or list(Z)): print(miks(b))
