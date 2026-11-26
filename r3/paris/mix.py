import numpy as np, soundfile as sf, json
SR = 24000; CUE = json.load(open("cues.json")); D = CUE["d"]; S = [sum(D[:i]) for i in range(len(D))]; TOT = sum(D); N = int(TOT * SR)
rng = np.random.default_rng(16); t = np.arange(N) / SR
def lp(x, k): k = max(1, int(k)); return np.convolve(x, np.ones(k) / k, mode="same").astype(np.float32)
def env(pts): xs, ys = zip(*pts); return np.interp(t, xs, ys).astype(np.float32)
def put(buf, a, st):
    k = int(st * SR); e = min(N, k + len(a)); buf[k:e] += a[:e - k]
voice = np.zeros(N, np.float32)
for i, (sh, st) in enumerate(CUE["vst"]):
    a, _ = sf.read(f"ses/p{i}.wav", dtype="float32"); put(voice, a / np.abs(a).max() * 0.8, S[sh] + st)
vact = np.clip(lp((np.abs(voice) > 0.02).astype(np.float32), 0.35 * SR) * 3, 0, 1)
K = S[3] + CUE["kalk"]; P = S[3] + CUE["program"]
sfx = np.zeros(N, np.float32)
camp = lp(rng.standard_normal(N).astype(np.float32), 120) * 1.5 * env([(0, 0.3), (S[1], 0.3), (S[1] + 0.01, 0), (TOT, 0)])
crowd = lp(rng.standard_normal(N).astype(np.float32), 30) * env([(0, 0), (S[2], 0), (S[2] + 0.3, 0.12), (S[3], 0.08), (K, 0.05), (K + 0.05, 0), (S[4], 0), (S[4] + CUE["acil"], 0.05), (S[4] + CUE["acil"] + 0.6, 0.3), (TOT, 0.15)])
n = int(0.5 * SR); x = np.arange(n) / SR
put(sfx, (lp(rng.standard_normal(n).astype(np.float32), 4) * np.exp(-x * 9) * 0.35), S[0] + CUE["olmeye"] - 0.1)  # su
for k in range(3):  # tabutta metal şıngırtısı
    n = int(0.25 * SR); x = np.arange(n) / SR; put(sfx, ((np.sin(2 * np.pi * 2300 * x) + np.sin(2 * np.pi * 3450 * x)) * np.exp(-x * 30) * 0.06).astype(np.float32), S[2] + CUE["silah"] + k * 0.09)
tt = S[2]
while tt < S[3] - 0.1:  # ağır adımlar
    n = int(0.08 * SR); x = np.arange(n) / SR; put(sfx, (np.sin(2 * np.pi * 60 * x) * np.exp(-x * 40) * 0.25).astype(np.float32), tt); tt += 0.55
n = int(0.7 * SR); x = np.arange(n) / SR
put(sfx, (np.sin(2 * np.pi * (90 * np.exp(-x * 5) + 40) * x) * np.exp(-x * 6) * 0.6 + lp(rng.standard_normal(n).astype(np.float32), 3) * np.exp(-x * 10) * 0.3).astype(np.float32), K)  # kapak patlar
n = int(0.6 * SR); x = np.arange(n) / SR; put(sfx, (np.sin(2 * np.pi * 1600 * x) * np.exp(-x * 4) * 0.05).astype(np.float32), K + 0.6)  # kılıç
n = int(1.6 * SR); x = np.arange(n) / SR
put(sfx, (lp(rng.standard_normal(n).astype(np.float32), 50) * np.minimum(1, x / 0.6) * np.exp(-np.maximum(0, x - 0.8) * 2) * 0.8), S[4] + CUE["acil"] - 0.1)  # kapı gıcırtısı/gürültü
n = int(0.5 * SR); x = np.arange(n) / SR; put(sfx, (np.sin(2 * np.pi * 70 * x) * np.exp(-x * 10) * 0.3).astype(np.float32), S[4] + CUE["yigil"])  # yığılma
def bowed(f, dur, amp):
    n = int(dur * SR); tt_ = np.arange(n) / SR; ph = 2 * np.pi * np.cumsum(f * (1 + 0.005 * np.sin(2 * np.pi * 5 * tt_))) / SR
    y = sum(np.sin(k * ph) / k ** 1.3 for k in range(1, 8)) * 0.5
    return (y * np.minimum(1, tt_ / 0.4) * np.minimum(1, (dur - tt_) / 0.6) * amp).astype(np.float32)
def pluck(f, amp=0.08):
    n = int(0.5 * SR); x = np.arange(n) / SR; return (np.sin(2 * np.pi * f * x) * np.exp(-x * 9) * amp).astype(np.float32)
music = np.zeros(N, np.float32)
# kurnaz pizzicato (1-3), kalkışta zafer akoru, "programa"da 0.8 sn sessizlik, kapılarda kahramanca, yığılmada iner
notes = [146.83, 174.61, 220.0, 196.0, 174.61, 164.81, 146.83, 130.81]; pos, k = 0.3, 0
while pos < K - 0.2:
    if not (S[1] + CUE["duyuyor"] < pos < S[1] + CUE["duyuyor"] + 0.8): put(music, pluck(notes[k % 8]), pos)
    pos += 0.36; k += 1
for f in (146.83, 220.0, 293.66): put(music, bowed(f, P - K - 0.05, 0.05), K)
for f in (174.61, 220.0, 261.63): put(music, bowed(f, S[4] + CUE["yigil"] - (P + 0.8), 0.05), P + 0.8)
put(music, bowed(110.0, TOT - (S[4] + CUE["yigil"]), 0.06), S[4] + CUE["yigil"])
music *= (1 - 0.45 * vact)
out = voice + (camp * 0.4 + crowd * 0.6 + sfx) * (1 - 0.5 * vact) + music
quiet = ((t > P + 0.05) & (t < P + 0.8)); out[quiet] = voice[quiet]
out[-int(0.8 * SR):] *= np.linspace(1, 0, int(0.8 * SR))
out = np.clip(out / np.abs(out).max() * 0.9, -1, 1)
sf.write("mix.wav", out, SR); print("ok", TOT)
