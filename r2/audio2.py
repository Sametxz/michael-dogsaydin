import json, wave, numpy as np, sys
sys.path.insert(0, "/home/claude/r2")
from script import SHOTS
SR = 22050
TL = json.load(open("/home/claude/r2/timeline.json"))
total = TL[-1][1] + TL[-1][2]; N = int(total * SR) + SR
bymap = {s["id"]: s for s in SHOTS}
rng = np.random.default_rng(3)

def rd(f):
    w = wave.open(f); a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768; return a

voice = np.zeros(N, np.float32); sfx = np.zeros(N, np.float32)
for sid, st, dur, cues, ends in TL:
    for i, q in enumerate(cues):
        a = rd(f"/home/claude/r2/audio/{sid}_{i}.t.wav"); k = int((st + q) * SR); voice[k:k+len(a)] += a

# ───── bölüm yoğunlukları (zaman → profil)
MOOD = {"Prolog": "myst", "I": "warm", "II": "battle", "III": "adv", "IV": "light", "V": "play", "VI": "tense", "VII": "dark", "VIII": "war", "Son": "warm"}
OVR = {"K1": "somber", "K2": "somber", "CTA": "warm", "D3": "dark", "D4": "silent", "D5": "dark", "D6": "dark", "R1": "tense", "F4": "end"}
PROF = {  # drone, drum, lyre, bowed
    "myst": (0.9, 0.35, 0.3, 0.6), "warm": (0.7, 0.2, 1.0, 0.3), "battle": (0.8, 1.0, 0.2, 0.7), "adv": (0.7, 0.75, 0.8, 0.4),
    "light": (0.6, 0.35, 0.9, 0.2), "play": (0.5, 0.5, 1.0, 0.1), "tense": (0.9, 0.55, 0.2, 0.8), "dark": (1.0, 0.25, 0.0, 0.9),
    "war": (0.9, 1.0, 0.3, 0.8), "somber": (0.8, 0.0, 0.25, 0.7), "silent": (0.15, 0.0, 0.0, 0.2), "end": (0.8, 0.3, 1.0, 0.5)}
env = {k: np.zeros(N, np.float32) for k in ("drone", "drum", "lyre", "bowed")}
for sid, st, dur, cues, ends in TL:
    s = bymap[sid]; m = OVR.get(sid, MOOD[s["ch"]]); p = PROF[m]
    a, b = int(st * SR), int((st + dur) * SR)
    for key, v in zip(("drone", "drum", "lyre", "bowed"), p): env[key][a:b] = v
K = int(1.2 * SR); ker = np.ones(K) / K
for k in env: env[k] = np.convolve(env[k], ker, mode="same").astype(np.float32)

t = np.arange(N) / SR
D = 73.42  # D2
drone = (0.09*np.sin(2*np.pi*D*t) + 0.06*np.sin(2*np.pi*D*1.5*t) + 0.035*np.sin(2*np.pi*D*2*t*1.001)) * (0.8 + 0.2*np.sin(2*np.pi*t/9))
# yaylı (testere + yumuşatma + vibrato)
def bowed_note(f, dur):
    n = int(dur * SR); tt = np.arange(n) / SR
    ph = 2*np.pi*np.cumsum(f * (1 + 0.006*np.sin(2*np.pi*5.2*tt))) / SR
    x = sum(np.sin(k*ph) / k for k in range(1, 9)) * 0.5
    e = np.minimum(1, tt / 0.6) * np.minimum(1, (dur - tt) / 0.8)
    return (x * e).astype(np.float32)
bowed = np.zeros(N, np.float32)
prog = [146.83, 130.81, 116.54, 130.81, 146.83, 174.61, 164.81, 146.83]   # D C Bb C D F E D
pos = 0.0; i = 0
while pos < total:
    d = 4.2; f = prog[i % len(prog)]; a = int(pos * SR); nt = bowed_note(f, d)
    end = min(N, a + len(nt)); bowed[a:end] += nt[:end - a] * 0.07; pos += 3.6; i += 1
# davul
drum = np.zeros(N, np.float32); bpm = 88; beat = 60 / bpm
def hit(t0, amp, f0=90):
    n = int(0.45 * SR); x = np.arange(n) / SR
    h = np.sin(2*np.pi*(f0*np.exp(-x*7) + 42)*x) * np.exp(-x*8) * amp
    h += rng.standard_normal(n) * np.exp(-x*40) * amp * 0.25
    a = int(t0 * SR); e = min(N, a + n); drum[a:e] += h[:e - a].astype(np.float32)
pattern = [(0, 1.0), (1.5, 0.5), (2, 0.8), (3, 0.45), (3.5, 0.6)]
bar = 0
while bar * 4 * beat < total:
    for off, amp in pattern: hit(bar * 4 * beat + off * beat, amp * 0.55)
    bar += 1
# lir (Karplus-Strong)
def ks(f, dur=1.8, amp=0.12):
    n = int(dur * SR); L = int(SR / f); buf = rng.uniform(-1, 1, L).astype(np.float32); out = np.zeros(n, np.float32)
    for k in range(n):
        out[k] = buf[k % L]; buf[k % L] = 0.996 * 0.5 * (buf[k % L] + buf[(k + 1) % L])
    return out * amp
scale = [293.66, 329.63, 349.23, 392.0, 440.0, 523.25, 587.33]  # D dorian-ish
motif = [0, 2, 4, 3, 2, 0, 1, 2, 4, 6, 5, 4, 2, 3, 1, 0]
lyre = np.zeros(N, np.float32); cache = {}
step = beat; k = 0; pos = 0.0
while pos < total:
    if (k % 8) not in (3, 7) or rng.random() < 0.3:
        f = scale[motif[k % len(motif)]] * (0.5 if (k // 16) % 2 else 1.0)
        if f not in cache: cache[f] = ks(f)
        nt = cache[f]; a = int(pos * SR); e = min(N, a + len(nt)); lyre[a:e] += nt[:e - a]
    pos += step; k += 1
music = drone * env["drone"] + drum * env["drum"] + lyre * env["lyre"] + bowed * env["bowed"]
fi = int(1.0 * SR); music[:fi] *= np.linspace(0, 1, fi)
fo = int(3.0 * SR); music[-fo:] *= np.linspace(1, 0, fo)

# ───── SFX
def at(sid, cue=None, off=0.0):
    for s, st, dur, cues, ends in TL:
        if s == sid: return st + (cues[cue] if cue is not None else 0) + off
def whoosh(t0, amp=0.25):
    n = int(0.6 * SR); x = np.arange(n) / SR; noise = rng.standard_normal(n).astype(np.float32)
    k = int(0.004 * SR); sm = np.convolve(noise, np.ones(k) / k, mode="same")
    e = np.sin(np.pi * x / 0.6) ** 2; a = int(t0 * SR); sfx[a:a+n] += (sm * e * amp)[:max(0, min(n, N - a))]
def thud(t0, amp=0.6):
    n = int(0.5 * SR); x = np.arange(n) / SR; h = np.sin(2*np.pi*(70*np.exp(-x*5) + 35)*x) * np.exp(-x*7) * amp
    a = int(t0 * SR); sfx[a:a+n] += h.astype(np.float32)[:max(0, min(n, N - a))]
def chime(t0, amp=0.12):
    for f in (880, 1320, 1760):
        n = int(1.2 * SR); x = np.arange(n) / SR; a = int(t0 * SR); sfx[a:a+n] += (np.sin(2*np.pi*f*x) * np.exp(-x*3) * amp / 3).astype(np.float32)[:max(0, min(n, N - a))]
for sid in ("C1", "L1", "T1", "K1", "P1", "E1", "D1", "R1"): whoosh(at(sid) - 0.15)
thud(at("L5", None, 0.35)); thud(at("T6", 1)); thud(at("P3", 0, 1.0), 0.5); thud(at("R3", 3), 0.5); thud(at("C1", 2, 1.0), 0.5)
chime(at("T7", 2)); chime(at("K9", 3, 0.8)); chime(at("E4", 0, 0.5)); chime(at("H1", 1)); chime(at("H2", 0)); chime(at("H3", 1))

def save(f, a):
    a = np.clip(a, -1, 1); w = wave.open(f, "wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((a * 32767).astype(np.int16).tobytes()); w.close()
save("/home/claude/r2/voice.wav", voice); save("/home/claude/r2/music.wav", music * 0.9); save("/home/claude/r2/sfx.wav", sfx)
print(round(total, 2))
