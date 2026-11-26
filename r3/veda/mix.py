import numpy as np, soundfile as sf, wave
SR = 24000; S = [0, 5.0, 10.8, 13.8, 18.0, 24.0]; TOT = 29.8; N = int(TOT * SR)
rng = np.random.default_rng(7); t = np.arange(N) / SR
def lp(x, k): k = max(1, int(k)); return np.convolve(x, np.ones(k) / k, mode="same").astype(np.float32)
def env(pts): xs, ys = zip(*pts); return np.interp(t, xs, ys).astype(np.float32)
def put(buf, a, st):
    k = int(st * SR); e = min(N, k + len(a)); buf[k:e] += a[:e - k]
voice = np.zeros(N, np.float32)
VST = [0.5, 2.7, S[1] + 0.5, S[1] + 2.6, S[2] + 0.4, S[3] + 0.3, S[4] + 0.5, S[4] + 3.0, S[5] + 0.5, S[5] + 2.0]
for i, st in enumerate(VST):
    a, _ = sf.read(f"v{i}.wav", dtype="float32"); put(voice, a / np.abs(a).max() * 0.8, st)
vact = np.clip(lp((np.abs(voice) > 0.02).astype(np.float32), 0.35 * SR) * 3, 0, 1)
sfx = np.zeros(N, np.float32)
# rüzgâr
wind = lp(rng.standard_normal(N).astype(np.float32), 90) * 1.8 * (0.6 + 0.4 * np.sin(2 * np.pi * t / 4.7)) * env([(0, 0.0), (0.5, 0.25), (S[1], 0.25), (S[1] + 0.2, 0.06), (S[2], 0.06), (S[2] + 0.2, 0.25), (S[5], 0.3), (TOT, 0.2)])
# ateş çıtırtısı + sönme
fire = np.zeros(N, np.float32); out = S[1] + 4.0
for k in rng.uniform(S[1], out + 0.3, 120):
    n = int(0.02 * SR); x = np.arange(n) / SR; put(fire, (rng.standard_normal(n) * np.exp(-x * 300) * rng.uniform(0.05, 0.25)).astype(np.float32), k)
fire += lp(rng.standard_normal(N).astype(np.float32), 30) * 0.15 * ((t > S[1]) & (t < out + 0.3))
n = int(1.2 * SR); x = np.arange(n) / SR; put(sfx, (lp(rng.standard_normal(n).astype(np.float32), 3) * np.exp(-x * 3) * 0.12), out)  # sönme tıslaması
n = int(0.4 * SR); x = np.arange(n) / SR; put(sfx, (np.sin(2 * np.pi * (80 * np.exp(-x * 8) + 50) * x) * np.exp(-x * 12) * 0.5).astype(np.float32), out + 0.35)  # kapak
# nal + tekerlek (3a, 3b)
for st, en, rate, amp in ((S[2], S[3], 2.2, 0.18), (S[3], S[4] - 0.2, 2.8, 0.28), (S[5], S[5] + 1.5, 2.2, 0.08)):
    tt = st
    while tt < en:
        for o_ in (0, 0.11):
            n = int(0.05 * SR); x = np.arange(n) / SR; put(sfx, (np.sin(2 * np.pi * 420 * x) * np.exp(-x * 90) * amp + rng.standard_normal(n) * np.exp(-x * 120) * amp * 0.4).astype(np.float32), tt + o_)
        tt += 1 / rate
    a, b = int(st * SR), int(en * SR); sfx[a:b] += lp(rng.standard_normal(b - a).astype(np.float32), 60) * amp * 1.6
# Bjorn adımları (3b)
tt = S[3] + 0.1
while tt < S[3] + 2.6:
    n = int(0.06 * SR); x = np.arange(n) / SR; put(sfx, (lp(rng.standard_normal(n).astype(np.float32), 4) * np.exp(-x * 60) * 0.25), tt); tt += 1 / 3.2
# tutuş tınısı
for f in (1174.66, 1760.0):
    n = int(1.3 * SR); x = np.arange(n) / SR; put(sfx, (np.sin(2 * np.pi * f * x) * np.exp(-x * 3.5) * 0.05).astype(np.float32), S[3] + 2.56)
# müzik
def bowed(f, dur, amp):
    n = int(dur * SR); tt = np.arange(n) / SR
    ph = 2 * np.pi * np.cumsum(f * (1 + 0.005 * np.sin(2 * np.pi * 5 * tt))) / SR
    y = sum(np.sin(k * ph) / k ** 1.3 for k in range(1, 8)) * 0.5
    return (y * np.minimum(1, tt / 1.0) * np.minimum(1, (dur - tt) / 1.2) * amp).astype(np.float32)
def ks(f, dur=2.0, amp=0.1):
    n = int(dur * SR); L = int(SR / f); buf = rng.uniform(-1, 1, L).astype(np.float32); o = np.zeros(n, np.float32)
    for k in range(n): o[k] = buf[k % L]; buf[k % L] = 0.996 * 0.5 * (buf[k % L] + buf[(k + 1) % L])
    return o * amp
music = np.zeros(N, np.float32)
D = 73.42; music += (0.06 * np.sin(2 * np.pi * D * t) + 0.035 * np.sin(2 * np.pi * D * 1.5 * t)) * env([(0, 0), (1.5, 1), (S[4] + 3.6, 1), (S[4] + 4.0, 0.3), (TOT - 1, 0.6), (TOT, 0)])
for st, f, d_ in ((0.3, 146.83, 5.0), (5.0, 116.54, 5.6), (10.6, 130.81, 3.4), (13.8, 146.83, 4.2), (18.0, 116.54, 3.9), (S[4] + 3.84, 220.0, 6.0), (S[5] + 2.2, 174.61, 3.6)):
    put(music, bowed(f, d_, 0.05), st)
cache = {}; mel = [293.66, 349.23, 329.63, 293.66, 261.63, 293.66, 220.0, 246.94]
pos, k = 0.6, 0
while pos < S[4] + 3.5:
    if not (S[1] + 4.0 < pos < S[2]):
        f = mel[k % len(mel)]; cache.setdefault(f, ks(f)); put(music, cache[f], pos)
    pos += 0.62; k += 1
put(music, ks(146.83, 3.0, 0.12), S[5] + 3.38)
music *= (1 - 0.45 * vact)
outm = voice + (wind * 0.5 + fire * 0.6 + sfx * 0.8) * (1 - 0.5 * vact) + music * 0.9
outm[-int(1.0 * SR):] *= np.linspace(1, 0, int(1.0 * SR))
outm = np.clip(outm / np.abs(outm).max() * 0.9, -1, 1)
sf.write("mix.wav", outm, SR); print("ok")
