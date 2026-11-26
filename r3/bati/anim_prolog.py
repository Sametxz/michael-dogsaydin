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
import v3_a, v3_b, v3_c, v3_prolog
FR.update(v3_a.FR); FR.update(v3_b.FRB); FR.update(v3_c.FR); FR.update(v3_prolog.FR)
ALIAS = {"e1b": "e1", "e5h": "e5", "e5r": "e5"}
OUT = "/home/claude/r3/prolog/out"; os.makedirs(OUT, exist_ok=True); SES = "/home/claude/r3/prolog/ses"; SR = 24000
K0 = "/home/claude/r3/tahta/out/K0.mp4"
dur = lambda i: sf.info(f"{SES}/p{i:02d}.wav").duration
PA = [("e5h", [], 0.5), ("p1a", [(0, 0.3)], 0.3), ("p1b", [(1, 0.2)], 0.3), ("p1c", [(2, 0.2)], 0.5), ("p1d", [(3, 0.3)], 1.0),
      ("p2a", [(4, 0.4)], 0.2), ("p2b", [(5, 0.2)], 0.4), ("p2c", [(6, 0.2)], 0.8), ("p3a", [(7, 0.4)], 0.2), ("p3b", [(8, 0.2)], 0.5), ("p3c", [(9, 0.3)], 2.4)]
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
# --- efekt katmanı + Ragnar yaş evresi (fx/efekt.py, ragnar_yas.py) ---
sys.path[:0] = ["/home/claude/r3", "/home/claude/r3/fx"]
import ragnar_yas as YAS, efekt as FX
FX.BOLUM[0] = "prolog"
def _evre(k): return {"p1b": YAS.RG2, "p1c": YAS.RG2}.get(k, YAS.RG1)
def _fxk(k): return k

def compose(c, k, t, d, st):
    YAS.uygula(_evre(k))
    K.T[0] = t; K.DUR[0] = d; K.CUE2.clear(); K.CUE2.update(cues(k, st))
    img = FR[ALIAS.get(k, k)]().makeImageSnapshot()
    z0, z1, a, b = CAM.get(ALIAS.get(k, k), (1.0, 1.06, (960, 540), (960, 520))); q = t / d; q = q * q * (3 - 2 * q); z = z0 + (z1 - z0) * q
    cx = a[0] + (b[0] - a[0]) * q; cy = a[1] + (b[1] - a[1]) * q
    hw, hh = W / (2 * z), (H - 140) / (2 * z); cx = min(max(cx, hw), W - hw); cy = min(max(cy, 70 + hh), H - 70 - hh)
    _sx, _sy = FX.sarsinti(_fxk(k), t, st); c.save(); c.translate(W / 2 + _sx, H / 2 + _sy); c.scale(z, z); c.translate(-cx, -cy); c.drawImage(img, 0, 0); FX.uygula(c, _fxk(k), t, st); c.restore()
    if k == "e4":   # şimşek flaşları
        for f0 in (0.2, d - 1.5): fill(c, "#DDEBFF", 0.7 * max(0.0, 1 - abs(t - f0) / 0.12))
    if k == "f10":   # "düşüyor": beyaz flaş
        fill(c, "#FFFFFF", 0.9 * max(0.0, 1 - t / 0.25))
    if k == "e5h":   # kanca: yanan manastırın tek karelik kırmızı flaşı
        fill(c, "#8A1A10", 0.35); fill(c, "#FFFFFF", 0.8 * max(0.0, 1 - t / 0.2))
    if k == "e5r":   # baskın: yangın titreşimi
        fill(c, "#FF6A2A", 0.06 + 0.04 * math.sin(t * 17))
    letterbox(c, 1.0, 70)

def mix(shots, vst, tot, path, part):
    N = int(tot * SR); tt = np.arange(N) / SR; rng = np.random.default_rng(3)
    lp = lambda x, n: np.convolve(x, np.ones(max(1, int(n))) / max(1, int(n)), mode="same").astype(np.float32)
    def put(buf, a, s): i = int(s * SR); e = min(N, i + len(a)); buf[i:e] += a[:e - i]
    def env(pts): xs, ys = zip(*pts); return np.interp(tt, xs, ys).astype(np.float32)
    voice = np.zeros(N, np.float32)
    for i, s in vst:
        a, _ = sf.read(f"{SES}/p{i:02d}.wav", dtype="float32"); put(voice, a / (np.abs(a).max() + 1e-6) * 0.8, s)
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
        fire = lp(rng.standard_normal(N).astype(np.float32), 40) * 0.4 * env([(0, 1.4), (S["p1a"], 0.0), (S["p1b"], 0.8), (S["p1c"], 0.2), (S["p1d"], 0.0), (S["p2a"], 1.0), (S["p3a"], 0.3), (S["p3b"], 0.5), (S["p3c"], 0.0), (tot, 0.0)])
        wind = lp(rng.standard_normal(N).astype(np.float32), 25) * env([(0, 0.2), (S["p1a"], 0.9), (S["p1b"], 0.1), (S["p1d"], 0.7), (S["p2a"], 0.0), (S["p3a"], 0.5), (S["p3b"], 0.1), (S["p3c"], 0.8), (tot, 0.6)])
        n = int(1.0 * SR); x = np.arange(n) / SR
        boom = (np.sin(2 * np.pi * 55 * x) * np.exp(-x * 5) * 0.6).astype(np.float32)
        for k_ in ("p1a", "p1b", "p1c"): put(sfx, boom, S[k_] + 0.05)   # kanca vuruşları
        n2 = int(1.4 * SR); x2 = np.arange(n2) / SR
        put(sfx, (lp(rng.standard_normal(n2).astype(np.float32), 30) * np.exp(-x2 * 2.5) * 0.5).astype(np.float32), S["p1c"] + ST["p1c"][2] + 1.2)   # kapak sürtünmesi
        chime = (np.sin(2 * np.pi * 1320 * x) * np.exp(-x * 3) * 0.06 + np.sin(2 * np.pi * 1980 * x) * np.exp(-x * 4) * 0.03).astype(np.float32)
        put(sfx, chime, S["p3b"] + ST["p3b"][8] + 0.8); put(sfx, chime * 0.6, S["p2c"] + 0.4)   # halka ve broş parıltısı
        put(music, bowed(98.0, S["p2a"], 0.05), 0.0); put(music, bowed(110.0, S["p3a"] - S["p2a"], 0.045), S["p2a"]); put(music, bowed(130.8, tot - S["p3a"], 0.05), S["p3a"])
        out = voice + duck * (fire * 0.12 + wind * 0.3 + music) + sfx
    else:
        crowd = lp(rng2.standard_normal(N).astype(np.float32), 120) * 1.4 * env([(0, 0.25), (S["f10"], 0.25), (S["f10"] + 0.1, 0.0), (S["e8"], 0.0), (S["e8"] + ST["e8"][19] + 0.4, 0.0), (S["e8"] + ST["e8"][19] + 0.8, 1.0), (tot - 1.0, 0.8), (tot, 0)])
        n = int(0.6 * SR); x = np.arange(n) / SR; put(sfx, (np.sin(2 * np.pi * 70 * x) * np.exp(-x * 9) * 0.6 + lp(rng.standard_normal(n).astype(np.float32), 3) * np.exp(-x * 20) * 0.3).astype(np.float32), S["f10"] + 0.05)   # kalkan darbesi
        n = int(1.0 * SR); x = np.arange(n) / SR; put(sfx, (np.sin(2 * np.pi * 1760 * x) * np.exp(-x * 4) * 0.05).astype(np.float32), S["e8"] + ST["e8"][20] + 0.6)   # halka parıltısı
        put(music, bowed(103.8, E["f10"], 0.05), 0.0); put(music, bowed(130.8, tot - S["e8"], 0.05), S["e8"])
        out = voice + duck * (crowd * 0.4 + music) + sfx
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
    os.makedirs(OUT, exist_ok=True); ta = render_part(PA, "prolog_v1", "A"); print(f"{OUT}/prolog_v1.mp4", ta)
