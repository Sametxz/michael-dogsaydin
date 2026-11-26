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
import v5_kayip
FR.update(v5_kayip.FR)
ALIAS = {"e1b": "e1", "e5h": "e5", "e5r": "e5"}
OUT = "/home/claude/r3/kayip/out"; os.makedirs(OUT, exist_ok=True); SES = "/home/claude/r3/kayip/ses"; SR = 24000
K7 = "/home/claude/r3/tahta/out/K7.mp4"; K8 = "/home/claude/r3/tahta/out/K8.mp4"
dur = lambda i: sf.info(f"{SES}/v{i:02d}.wav").duration
PA = [("k19a", [(0, 0.5)], 0.4), ("k19b", [(1, 0.3)], 0.4), ("k19c", [(2, 0.3)], 1.6), ("k19d", [(3, 0.3)], 1.0),
      ("k20a", [(4, 0.6)], 1.2), ("k20b", [(5, 0.4)], 1.6), ("k21a", [(6, 0.4)], 0.6), ("k21b", [(7, 0.4)], 2.4)]
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
FR.update(k21b=ON.FR["k21b"])

# --- efekt katmanı + Ragnar yaş evresi (fx/efekt.py, ragnar_yas.py) ---
sys.path[:0] = ["/home/claude/r3", "/home/claude/r3/fx"]
import ragnar_yas as YAS, efekt as FX
FX.BOLUM[0] = "V"
def _evre(k): return {}.get(k, YAS.RG3)
def _fxk(k): return k

def compose(c, k, t, d, st):
    YAS.uygula(_evre(k))
    K.T[0] = t; K.DUR[0] = d; K.CUE2.clear(); K.CUE2.update(cues(k, st))
    img = FR[ALIAS.get(k, k)]().makeImageSnapshot()
    z0, z1, a, b = CAM.get(ALIAS.get(k, k), (1.0, 1.06, (960, 540), (960, 520))); q = t / d; q = q * q * (3 - 2 * q); z = z0 + (z1 - z0) * q
    cx = a[0] + (b[0] - a[0]) * q; cy = a[1] + (b[1] - a[1]) * q
    hw, hh = W / (2 * z), (H - 140) / (2 * z); cx = min(max(cx, hw), W - hw); cy = min(max(cy, 70 + hh), H - 70 - hh)
    _sx, _sy = FX.sarsinti(_fxk(k), t, st); c.save(); c.translate(W / 2 + _sx, H / 2 + _sy); c.scale(z, z); c.translate(-cx, -cy); c.drawImage(img, 0, 0); FX.uygula(c, _fxk(k), t, st); c.restore()
    if k == "k21b":   # şafak ışığı açılır
        fill(c, "#FFF2D0", 0.25 * max(0.0, 1 - t / 1.2))

def mix(shots, vst, tot, path, part):
    N = int(tot * SR); tt = np.arange(N) / SR; rng = np.random.default_rng(3)
    lp = lambda x, n: np.convolve(x, np.ones(max(1, int(n))) / max(1, int(n)), mode="same").astype(np.float32)
    def put(buf, a, s): i = int(s * SR); e = min(N, i + len(a)); buf[i:e] += a[:e - i]
    def env(pts): xs, ys = zip(*pts); return np.interp(tt, xs, ys).astype(np.float32)
    voice = np.zeros(N, np.float32)
    for i, s in vst:
        a, _ = sf.read(f"{SES}/v{i:02d}.wav", dtype="float32"); put(voice, a / (np.abs(a).max() + 1e-6) * 0.8, s)
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
        wind = lp(rng.standard_normal(N).astype(np.float32), 25) * env([(0, 0.6), (S["k19b"], 0.0), (S["k20a"], 0.7), (S["k21a"], 0.5), (S["k21b"], 1.4), (S["k21b"] + 1.5, 0.3), (tot, 0.2)])
        fire = lp(rng.standard_normal(N).astype(np.float32), 40) * 0.4 * env([(0, 0), (S["k19b"], 1.0), (S["k20a"], 0.0), (tot, 0.0)])
        n = int(1.0 * SR); x = np.arange(n) / SR
        caw = (np.sin(2 * np.pi * (700 - 300 * x[:int(0.25 * SR)]) * x[:int(0.25 * SR)]) * np.exp(-x[:int(0.25 * SR)] * 6) * 0.15).astype(np.float32)
        for dt in (0.4, 1.3): put(sfx, caw, S["k20a"] + dt)
        for dt in (0.2, 0.9): put(sfx, caw, S["k20b"] + dt)
        h0 = S["k19c"] + ST["k19c"][2]
        hush = env([(0, 1), (h0 + 1.5, 1), (h0 + 1.7, 0.15), (S["k19d"], 0.15), (S["k19d"] + 0.3, 1), (tot, 1)])   # "kimse istemiyor"da sessizlik
        put(music, bowed(87.3, S["k20a"], 0.05), 0.0); put(music, bowed(73.4, S["k21a"] - S["k20a"], 0.055), S["k20a"]); put(music, bowed(82.4, tot - S["k21a"], 0.05), S["k21a"])
        out = voice + duck * (wind * 0.35 + fire * 0.1 + music) * hush + sfx
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
    ta = render_part(PA, "bolum5_kayip_v1", "A"); print(f"{OUT}/bolum5_kayip_v1.mp4", ta)
