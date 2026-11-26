import numpy as np, soundfile as sf, json
SR = 24000; CUE = json.load(open("cues.json")); D = CUE["d"]; S = [sum(D[:i]) for i in range(len(D))]; TOT = sum(D); N = int(TOT * SR)
rng = np.random.default_rng(12); t = np.arange(N) / SR
def lp(x, k): k = max(1, int(k)); return np.convolve(x, np.ones(k) / k, mode="same").astype(np.float32)
def env(pts): xs, ys = zip(*pts); return np.interp(t, xs, ys).astype(np.float32)
def put(buf, a, st):
    k = int(st * SR); e = min(N, k + len(a)); buf[k:e] += a[:e - k]
voice = np.zeros(N, np.float32)
for i, (sh, st) in enumerate(CUE["vst"]):
    a, _ = sf.read(f"ses/f{i}.wav", dtype="float32"); put(voice, a / np.abs(a).max() * 0.8, S[sh] + st)
vact = np.clip(lp((np.abs(voice) > 0.02).astype(np.float32), 0.35 * SR) * 3, 0, 1)
G = S[3] + CUE["gulumsuyor"]; K = S[4] + CUE["kurtaramiyorsun"]
silent = ((t > G) & (t < G + 1.1)).astype(np.float32)
sfx = np.zeros(N, np.float32)
# 1 liman: dalga + martı benzeri tını yok, ışık anında koro tonu
waves = lp(rng.standard_normal(N).astype(np.float32), 200) * 3 * (0.6 + 0.4 * np.sin(2 * np.pi * t / 3.1)) * env([(0, 0.25), (S[1] - 0.2, 0.25), (S[1], 0.0), (TOT, 0)])
def pad(f0, dur, amp):
    n = int(dur * SR); tt = np.arange(n) / SR
    y = sum(np.sin(2 * np.pi * f0 * m * tt + m) / (1 + k) for k, m in enumerate((1, 1.5, 2, 2.5, 3)))
    return (y * np.minimum(1, tt / 0.8) * np.minimum(1, (dur - tt) / 1.0) * amp).astype(np.float32)
put(sfx, pad(220.0, 3.4, 0.05), S[0] + CUE["isik"] - 0.1)
# 2 kulübe: mum çıtırtısı, iç ortam
room = lp(rng.standard_normal(N).astype(np.float32), 400) * 1.5 * (((t > S[1]) & (t < G)).astype(np.float32))
for k in rng.uniform(S[1], G, 40):
    n = int(0.015 * SR); x = np.arange(n) / SR; put(sfx, (rng.standard_normal(n) * np.exp(-x * 400) * 0.06).astype(np.float32), k)
# 3 kapı gıcırtısı + rüzgâr
kp = S[2] + CUE["kapi"]; n = int(0.9 * SR); x = np.arange(n) / SR
put(sfx, (np.sin(2 * np.pi * (300 + 140 * np.sin(2 * np.pi * 3 * x)) * x) * np.exp(-x * 2.5) * 0.08 * (1 + 0.5 * np.sin(2 * np.pi * 40 * x))).astype(np.float32), kp)
wind = lp(rng.standard_normal(N).astype(np.float32), 80) * 2.0 * env([(0, 0), (kp, 0), (kp + 0.3, 0.3), (S[3], 0.12), (G, 0.12), (G + 0.01, 0), (TOT, 0)])
# 4 gerilim: alçak drone yükselir, flaşta her şey kesilir
drone = (np.sin(2 * np.pi * 55 * t) * 0.12 + np.sin(2 * np.pi * 58.3 * t) * 0.08) * env([(0, 0), (S[2], 0), (S[3], 0.6), (G, 1.0), (G + 0.01, 0), (TOT, 0)])
# 5 yağmur: K'dan sonra
rain = (lp(rng.standard_normal(N).astype(np.float32), 3) - lp(rng.standard_normal(N).astype(np.float32), 40) * 0.5) * env([(0, 0), (K - 0.1, 0), (K + 0.8, 0.22), (TOT, 0.3)])
# müzik: sıcak lir (1-2), kesilir; sonda yağmurla tek yaylı
def ks(f, dur=2.2, amp=0.09):
    n = int(dur * SR); L = int(SR / f); buf = rng.uniform(-1, 1, L).astype(np.float32); o = np.zeros(n, np.float32)
    for k in range(n): o[k] = buf[k % L]; buf[k % L] = 0.996 * 0.5 * (buf[k % L] + buf[(k + 1) % L])
    return o * amp
music = np.zeros(N, np.float32); mel = [293.66, 369.99, 440.0, 369.99, 329.63, 293.66, 246.94, 293.66]; cache = {}
pos, k = 0.4, 0
while pos < S[2] + 0.2:
    f = mel[k % 8]; cache.setdefault(f, ks(f)); put(music, cache[f], pos); pos += 0.7; k += 1
put(music, pad(146.83, TOT - (S[4] + 0.6), 0.04), S[4] + 0.6)
music *= (1 - 0.45 * vact)
out = voice + (waves * 0.5 + room * 0.4 + wind * 0.5 + rain * 0.5 + sfx) * (1 - 0.5 * vact) + drone * 0.7 + music
out *= (1 - silent * (1 - (voice != 0)))   # flaş sonrası sessizlik (anlatım dışı)
out[-int(0.6 * SR):] *= np.linspace(1, 0.4, int(0.6 * SR))
out = np.clip(out / np.abs(out).max() * 0.9, -1, 1)
sf.write("mix.wav", out, SR); print("ok", TOT)
