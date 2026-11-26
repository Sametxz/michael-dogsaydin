"""I · Batı bölüm animatiği: Sahne 1–4 (e1–e6) → K0 tahta → Sahne 5 (e7–e8). Efektler: şimşek flaşı + gök gürültüsü, sis, yangın,
"düşüyor"da beyaz flaş + kalkan darbesi, "jarl sensin"de tezahürat, halka parıltısı. python3 anim1.py prev | python3 anim1.py → out/bolum1_bati_v1.mp4
"""
import sys, math, os, subprocess
sys.path[:0] = ["/home/claude/r3", "/home/claude/r2", "/home/claude/r3/kesis", "/home/claude/r3/bedel", "/home/claude/r3/bati"]
import numpy as np, soundfile as sf, skia
from engine import *
from fx import *
import kareler5 as K
import kareler6 as K6
FR = {**K.FR5, **K6.FR6}
import v3_b, v3_prolog, v6_son
FR.update(v3_b.FRB); FR.update(v3_prolog.FR); FR.update(v6_son.FR)
ALIAS = {"e1b": "e1", "e5h": "e5", "e5r": "e5"}
OUT = "/home/claude/r3/son/out"; os.makedirs(OUT, exist_ok=True); SES = "/home/claude/r3/son/ses"; SR = 24000
K7 = "/home/claude/r3/tahta/out/K7.mp4"; K8 = "/home/claude/r3/tahta/out/K8.mp4"
dur = lambda i: sf.info(f"{SES}/s{i:02d}.wav").duration
PA = [("k22a", [(0, 0.5)], 0.3), ("k22b", [(1, 0.3)], 0.4), ("k22c", [(2, 0.3)], 1.2), ("k23a", [(3, 0.4)], 0.2), ("k23b", [(4, 0.2)], 1.0),
      ("k24", [(5, 0.4)], 1.4), ("k25a", [(6, 0.3)], 0.6), ("k25b", [(7, 0.3)], 1.0), ("k26a", [(8, 0.4)], 0.8), ("k26b", [(9, 0.3)], 1.2),
      ("k26c", [(10, 0.5)], 1.4), ("k26d", [(11, 0.5)], 2.0), ("f1", [(12, 0.5)], 0.0), ("p1b", [], 1.2), ("k27b", [(13, 0.3)], 1.0), ("k27c", [(14, 0.6)], 4.0)]
PB = []
def timeline(plan):
    shots, vst, t0 = [], [], 0.0
    for k, lines, tail in plan:
        t = 0.0; st = {}
        for i, gap in lines:
            t += gap; st[i] = t; vst.append((i, t0 + t)); t += dur(i)
        d = t + tail; shots.append((k, d, st, t0)); t0 += d
    return shots, vst, t0

def cues(k, st): return {}
CAM = {"e1": (1.0, 1.06, (960, 540), (860, 520)), "e2": (1.0, 1.08, (960, 540), (1000, 480)), "e3": (1.0, 1.05, (960, 560), (1000, 560)),
       "e4": (1.04, 1.0, (1000, 520), (960, 540)), "e5": (1.0, 1.06, (960, 540), (1100, 520)), "e6": (1.0, 1.10, (960, 560), (1000, 500)),
       "e7": (1.0, 1.08, (960, 600), (960, 560)), "e8": (1.0, 1.08, (960, 560), (900, 480))}
# --- onaylı onarım kareleri v1 (kurul/BRIEF_onarim_v1.md, kullanıcı onayı 20.11.2026) ---
sys.path[:0] = ["/home/claude/r3/bati", "/home/claude/r3/bedel", "/home/claude/r3/kesis", "/home/claude/r3", "/home/claude/r2"]
import onarim_v1 as ON
FR.update(k26b=ON.FR["k26b"], k26c=ON.FR["k26c"], k23b=ON.FR["k23bc"])

# --- efekt katmanı + Ragnar yaş evresi (fx/efekt.py, ragnar_yas.py) ---
sys.path[:0] = ["/home/claude/r3", "/home/claude/r3/fx"]
import ragnar_yas as YAS, efekt as FX
FX.BOLUM[0] = "VI"
def _evre(k): return {"f1": YAS.RG1, "p1b": YAS.RG2}.get(k, YAS.RG4)
def _fxk(k): return k

def compose(c, k, t, d, st):
    YAS.uygula(_evre(k))
    K.T[0] = t; K.DUR[0] = d; K.CUE2.clear(); K.CUE2.update(cues(k, st))
    img = FR[ALIAS.get(k, k)]().makeImageSnapshot()
    z0, z1, a, b = CAM.get(ALIAS.get(k, k), (1.0, 1.06, (960, 540), (960, 520))); q = t / d; q = q * q * (3 - 2 * q); z = z0 + (z1 - z0) * q
    cx = a[0] + (b[0] - a[0]) * q; cy = a[1] + (b[1] - a[1]) * q
    hw, hh = W / (2 * z), (H - 140) / (2 * z); cx = min(max(cx, hw), W - hw); cy = min(max(cy, 70 + hh), H - 70 - hh)
    _sx, _sy = FX.sarsinti(_fxk(k), t, st); c.save(); c.translate(W / 2 + _sx, H / 2 + _sy); c.scale(z, z); c.translate(-cx, -cy); c.drawImage(img, 0, 0); FX.uygula(c, _fxk(k), t, st); c.restore()
    if k == "k26d":   # ışık açılır
        fill(c, "#FFF2D0", 0.18 * min(1.0, t / 1.5))

def mix(shots, vst, tot, path, part):
    N = int(tot * SR); tt = np.arange(N) / SR; rng = np.random.default_rng(3)
    lp = lambda x, n: np.convolve(x, np.ones(max(1, int(n))) / max(1, int(n)), mode="same").astype(np.float32)
    def put(buf, a, s): i = int(s * SR); e = min(N, i + len(a)); buf[i:e] += a[:e - i]
    def env(pts): xs, ys = zip(*pts); return np.interp(tt, xs, ys).astype(np.float32)
    voice = np.zeros(N, np.float32)
    for i, s in vst:
        a, _ = sf.read(f"{SES}/s{i:02d}.wav", dtype="float32"); put(voice, a / (np.abs(a).max() + 1e-6) * 0.8, s)
    S = {k: t0 for k, d, st, t0 in shots}; E = {k: t0 + d for k, d, st, t0 in shots}; ST = {k: st for k, d, st, t0 in shots}
    vact = np.clip(lp((np.abs(voice) > 0.02).astype(np.float32), 0.35 * SR) * 3, 0, 1); duck = 1 - 0.55 * vact
    def bowed(f, d_, amp):
        n = int(d_ * SR); x = np.arange(n) / SR; ph = 2 * np.pi * np.cumsum(f * (1 + 0.005 * np.sin(2 * np.pi * 5 * x))) / SR
        y = sum(np.sin(j * ph) / j ** 1.3 for j in range(1, 8)) * 0.5
        return (y * np.minimum(1, x / 1.2) * np.minimum(1, (d_ - x) / 1.5) * amp).astype(np.float32)
    music = np.zeros(N, np.float32); amb = np.zeros(N, np.float32); sfx = np.zeros(N, np.float32)
    ST = {k: st for k, d, st, t0 in shots}
    rng2 = np.random.default_rng(5)
    if part == "A":
        rain = lp(rng.standard_normal(N).astype(np.float32), 6) * env([(0, 0.7), (S["k22b"], 0.0), (S["k25a"], 0.8), (S["k26a"], 0.0), (tot, 0.0)])
        fire = lp(rng.standard_normal(N).astype(np.float32), 40) * 0.4 * env([(0, 0), (S["k22b"], 1.0), (S["k23a"], 0.2), (S["k25a"], 0.0), (S["k26a"], 0.6), (S["k26b"], 0.0), (tot, 0.0)])
        wind = lp(rng.standard_normal(N).astype(np.float32), 25) * env([(0, 0.2), (S["k26c"], 0.2), (S["k26d"], 0.6), (S["k27b"], 0.8), (tot, 0.5)])
        n = int(1.0 * SR); x = np.arange(n) / SR
        caw = (np.sin(2 * np.pi * (700 - 300 * x[:int(0.25 * SR)]) * x[:int(0.25 * SR)]) * np.exp(-x[:int(0.25 * SR)] * 6) * 0.15).astype(np.float32)
        for dt in (0.6, 1.4): put(sfx, caw, S["k26d"] + dt)
        put(sfx, caw, E["k27c"] - 2.0)
        chime = (np.sin(2 * np.pi * 1320 * x) * np.exp(-x * 3) * 0.06).astype(np.float32); put(sfx, chime, S["k24"] + ST["k24"][5] + 1.0)   # haç parıltısı
        clank = (np.sin(2 * np.pi * 220 * x) * np.exp(-x * 10) * 0.25).astype(np.float32); put(sfx, clank, S["k25a"] + 0.2)   # kafes
        h0 = S["k26b"] + ST["k26b"][9] + 1.6
        hush = env([(0, 1), (h0, 1), (h0 + 0.2, 0.1), (S["k26c"] + 0.3, 0.1), (S["k26c"] + 1.0, 1), (tot, 1)])
        put(music, bowed(98.0, S["k25a"], 0.045), 0.0); put(music, bowed(73.4, S["k26d"] - S["k25a"], 0.055), S["k25a"])
        put(music, bowed(110.0, S["k27b"] - S["k26d"], 0.05), S["k26d"]); put(music, bowed(130.8, tot - S["k27b"], 0.06), S["k27b"])
        out = voice + duck * (rain * 0.12 + fire * 0.1 + wind * 0.3 + music) * hush + sfx
    out *= np.minimum(1, (tot - tt) / 1.0) * np.minimum(1, tt / 0.3)
    sf.write(path + ".raw.wav", out / (np.abs(out).max() + 1e-6) * 0.9, SR)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", path + ".raw.wav", "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "48000", "-ac", "2", path], check=True)
    os.remove(path + ".raw.wav")

def render_part(plan, name, part):
    shots, vst, tot = timeline(plan)
    mix(shots, vst, tot, f"{OUT}/{name}.wav", part)
    surf = skia.Surface(W, H); c = surf.getCanvas(); tmp = f"{OUT}/{name}_tmp.mp4"; wr = Writer(tmp); dip = 6
    for si, (k, d, st, _) in enumerate(shots):
        n = int(round(d * FPS))
        for f in range(n):
            t = f / FPS; c.clear(skia.ColorBLACK); compose(c, k, t, d, st)
            if si > 0 and f < dip: fill(c, "#000", 1 - f / dip)
            if si < len(shots) - 1 and f >= n - dip: fill(c, "#000", (f - (n - dip)) / dip)
            if si == len(shots) - 1 and f >= n - 18: fill(c, "#000", (f - (n - 18)) / 18)
            wr.write(surf)
    wr.close()
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", tmp, "-i", f"{OUT}/{name}.wav", "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", f"{OUT}/{name}.mp4"], check=True)
    os.remove(tmp); return tot

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    ta = render_part(PA, "bolum6_son_v1", "A"); print(f"{OUT}/bolum6_son_v1.mp4", ta)
