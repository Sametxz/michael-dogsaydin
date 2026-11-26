import numpy as np, soundfile as sf, json
SR = 24000; CUE = json.load(open("cues.json")); D = CUE["d"]; S = [sum(D[:i]) for i in range(len(D))]; TOT = sum(D); N = int(TOT * SR)
rng = np.random.default_rng(9); t = np.arange(N) / SR
def lp(x, k): k = max(1, int(k)); return np.convolve(x, np.ones(k) / k, mode="same").astype(np.float32)
def env(pts): xs, ys = zip(*pts); return np.interp(t, xs, ys).astype(np.float32)
def put(buf, a, st):
    k = int(st * SR); e = min(N, k + len(a)); buf[k:e] += a[:e - k]
voice = np.zeros(N, np.float32)
for i, (sh, st) in enumerate(CUE["vst"]):
    a, _ = sf.read(f"ses/i{i}.wav", dtype="float32"); put(voice, a / np.abs(a).max() * 0.8, S[sh] + st)
vact = np.clip(lp((np.abs(voice) > 0.02).astype(np.float32), 0.35 * SR) * 3, 0, 1)
Y = S[3] + CUE["yapam"]
room = lp(rng.standard_normal(N).astype(np.float32), 300) * 1.4 * env([(0, 1), (S[2] - 0.1, 1), (S[2], 0), (TOT, 0)])
river = (lp(rng.standard_normal(N).astype(np.float32), 6) - lp(rng.standard_normal(N).astype(np.float32), 60) * 0.5) * env(
    [(0, 0), (S[2], 0), (S[2] + 0.3, 0.12), (S[2] + CUE["bicak"], 0.22), (Y, 0.26), (Y + 0.05, 0.0), (S[4] + 0.3, 0.0), (S[4] + 1.0, 0.1), (TOT, 0.08)])
sfx = np.zeros(N, np.float32)
n = int(0.5 * SR); x = np.arange(n) / SR; put(sfx, (np.sin(2 * np.pi * 70 * x) * np.exp(-x * 10) * 0.3).astype(np.float32), S[1] + CUE["aliyor"] + 0.9)  # kapı
for f in (2600, 3900):  # bıçak parıltısı
    n = int(0.6 * SR); x = np.arange(n) / SR; put(sfx, (np.sin(2 * np.pi * f * x) * np.exp(-x * 8) * 0.03).astype(np.float32), S[2] + CUE["bicak"])
n = int(0.3 * SR); x = np.arange(n) / SR; put(sfx, ((np.sin(2 * np.pi * 1800 * x) + 0.6 * np.sin(2 * np.pi * 2700 * x)) * np.exp(-x * 25) * 0.12).astype(np.float32), Y + 0.33)  # bıçak taşa düşer
n = int(0.5 * SR); x = np.arange(n) / SR; put(sfx, (np.sin(2 * np.pi * (520 + 80 * np.sin(2 * np.pi * 5 * x)) * x) * np.exp(-x * 5) * 0.035).astype(np.float32), Y + 1.0)  # bebeğin hafif sesi
tt = S[5]
while tt < S[5] + CUE["annesi"]:  # Aslaug'un koşusu
    n = int(0.06 * SR); x = np.arange(n) / SR; put(sfx, lp(rng.standard_normal(n).astype(np.float32), 4) * np.exp(-x * 60) * 0.25, tt); tt += 0.3
def bowed(f, dur, amp):
    n = int(dur * SR); tt_ = np.arange(n) / SR; ph = 2 * np.pi * np.cumsum(f * (1 + 0.005 * np.sin(2 * np.pi * 5 * tt_))) / SR
    y = sum(np.sin(k * ph) / k ** 1.3 for k in range(1, 8)) * 0.5
    return (y * np.minimum(1, tt_ / 1.0) * np.minimum(1, (dur - tt_) / 1.2) * amp).astype(np.float32)
music = np.zeros(N, np.float32)
music += (0.05 * np.sin(2 * np.pi * 65.41 * t)) * env([(0, 0), (1, 1), (Y, 1), (Y + 0.05, 0), (S[5], 0), (S[5] + 0.8, 0.8), (TOT, 0)])
for st, f, d_ in ((0.3, 130.81, 5.2), (5.4, 116.54, 7.0), (12.4, 123.47, 4.0), (S[5] + 0.6, 196.0, 3.4), (S[5] + 0.9, 261.63, 3.1)):
    put(music, bowed(f, d_, 0.05), st)
music *= (1 - 0.45 * vact)
out = voice + (room * 0.4 + river * 0.6 + sfx) * (1 - 0.5 * vact) + music
out[-int(0.8 * SR):] *= np.linspace(1, 0, int(0.8 * SR))
out = np.clip(out / np.abs(out).max() * 0.9, -1, 1)
sf.write("mix.wav", out, SR); print("ok", TOT)
