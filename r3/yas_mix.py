import numpy as np, json, wave
SR = 24000; S = [0, 8.6, 12.2, 20.2, 25.8]; TOT = 30.8; N = int(TOT * SR)
rng = np.random.default_rng(5); t = np.arange(N) / SR
def lp(x, k):  # basit hareketli ortalama alçak geçiren
    k = max(1, int(k)); return np.convolve(x, np.ones(k) / k, mode="same").astype(np.float32)
def env_pts(pts):  # [(zaman, değer)] doğrusal zarf
    xs, ys = zip(*pts); return np.interp(t, xs, ys).astype(np.float32)
voice = np.zeros(N, np.float32)
import soundfile as sf
VST = [0.5, 4.8, S[1] + 0.4, S[2] + 0.6, S[2] + 3.7, S[3] + 0.4, S[3] + 2.9]
for i, st in enumerate(VST):
    a, _ = sf.read(f"yas_ses/d{i}.wav", dtype="float32"); a = a / np.abs(a).max() * 0.8
    k = int(st * SR); voice[k:k + len(a)] += a
vact = lp((np.abs(voice) > 0.02).astype(np.float32), 0.35 * SR); vact = np.clip(vact * 3, 0, 1)
# yağmur: geniş bant + damla tıkırtıları
wn = rng.standard_normal(N).astype(np.float32)
rain = lp(wn, 3) - lp(wn, 40) * 0.6
drops = np.zeros(N, np.float32)
for k in rng.integers(0, N - 400, 900):
    n = 300; x = np.arange(n) / SR; drops[k:k + n] += (np.sin(2 * np.pi * rng.uniform(1800, 4200) * x) * np.exp(-x * 300) * rng.uniform(0.05, 0.25)).astype(np.float32)
rain_e = env_pts([(0, 0), (0.6, 0.20), (S[1], 0.20), (S[1] + 1.62, 0.20), (S[1] + 1.8, 0.13), (S[2], 0.13), (S[2] + 0.3, 0.08), (S[4], 0.08), (S[4] + 3, 0.035), (TOT, 0)])
rain_close = lp(rain, 6)  # yakın planda boğuk
mix_r = (np.where((t > S[2]) & (t < S[4]), rain_close * 1.4, rain) * rain_e + drops * rain_e * 1.2) * (1 - 0.6 * vact)
# şelale uğultusu + rüzgâr
fall = lp(wn[::-1].copy(), 25) * env_pts([(0, 0), (1, 0.07), (S[2], 0.05), (S[4], 0.04), (TOT, 0)]) * (1 - 0.5 * vact)
wind = lp(rng.standard_normal(N).astype(np.float32), 120) * (0.6 + 0.4 * np.sin(2 * np.pi * t / 5.3)) * 1.6 * env_pts([(0, 0.2), (S[4], 0.25), (TOT, 0)]) * (1 - 0.5 * vact)
# çamur darbesi
sfx = np.zeros(N, np.float32); imp = S[1] + 1.5
n = int(0.6 * SR); x = np.arange(n) / SR; a = int(imp * SR)
sfx[a:a + n] += (np.sin(2 * np.pi * (62 * np.exp(-x * 6) + 30) * x) * np.exp(-x * 7) * 0.7).astype(np.float32)
sfx[a:a + n] += lp(rng.standard_normal(n).astype(np.float32), 8) * np.exp(-x * 9).astype(np.float32) * 0.5
# bıçak (örgü kesimi), tıraş hışırtısı, kolye tınısı
cut = S[3] + 1.26; n = int(0.25 * SR); x = np.arange(n) / SR; a = int(cut * SR)
sfx[a:a + n] += (rng.standard_normal(n) * np.exp(-x * 25) * 0.25).astype(np.float32)
a, b = int((S[3] + 1.45) * SR), int((S[3] + 2.75) * SR)
scr = rng.standard_normal(b - a).astype(np.float32); scr = scr - lp(scr, 6); sfx[a:b] += scr * 0.05 * (0.6 + 0.4 * np.sin(np.linspace(0, 26, b - a)) ** 2)
for f in (1567.98, 2349.3):
    n = int(1.4 * SR); x = np.arange(n) / SR; a = int((S[3] + 4.02) * SR); sfx[a:a + n] += (np.sin(2 * np.pi * f * x) * np.exp(-x * 3.5) * 0.05).astype(np.float32)
# müzik: D minör yaylı + bas drone; siluette kabarma, isimde lir arpeji
def bowed(f, dur, amp):
    n = int(dur * SR); tt = np.arange(n) / SR
    ph = 2 * np.pi * np.cumsum(f * (1 + 0.005 * np.sin(2 * np.pi * 5 * tt))) / SR
    y = sum(np.sin(k * ph) / k ** 1.3 for k in range(1, 8)) * 0.5
    return (y * np.minimum(1, tt / 1.2) * np.minimum(1, (dur - tt) / 1.5) * amp).astype(np.float32)
music = np.zeros(N, np.float32)
D = 73.42; music += ((0.07 * np.sin(2 * np.pi * D * t) + 0.04 * np.sin(2 * np.pi * D * 1.5 * t)) * env_pts([(0, 0), (2, 1), (TOT - 1.5, 1), (TOT, 0)])).astype(np.float32)
for st, f, d_, am in [(0.5, 146.83, 5.0, 0.05), (4.8, 116.54, 4.6, 0.05), (9.0, 110.0, 3.8, 0.05), (12.4, 146.83, 4.2, 0.045), (16.0, 130.81, 4.6, 0.045),
                      (20.2, 116.54, 3.4, 0.045), (23.2, 110.0, 3.0, 0.05), (S[4] - 0.3, 174.61, 5.3, 0.075), (S[4] - 0.3, 220.0, 5.3, 0.05), (S[4] + 1.6, 293.66, 3.4, 0.04)]:
    y = bowed(f, d_, am); k = int(st * SR); music[k:k + len(y)] += y[:N - k]
def ks(f, dur=2.2, amp=0.11):
    n = int(dur * SR); L = int(SR / f); buf = rng.uniform(-1, 1, L).astype(np.float32); out = np.zeros(n, np.float32)
    for k in range(n):
        out[k] = buf[k % L]; buf[k % L] = 0.997 * 0.5 * (buf[k % L] + buf[(k + 1) % L])
    return out * amp
for j, f in enumerate((293.66, 349.23, 440.0, 587.33)):
    y = ks(f); k = int((S[4] + 2.0 + j * 0.32) * SR); music[k:k + len(y)] += y[:N - k]
music *= (1 - 0.45 * vact)
out = voice * 1.0 + mix_r * 0.22 + fall * 0.7 + wind * 0.4 + sfx + music * 0.9
out[-int(0.8 * SR):] *= np.linspace(1, 0, int(0.8 * SR))
out = np.clip(out / max(1e-6, np.abs(out).max()) * 0.9, -1, 1)
w = wave.open("yas_ses/mix.wav", "wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out * 32767).astype(np.int16).tobytes()); w.close()
print("ok", TOT)
