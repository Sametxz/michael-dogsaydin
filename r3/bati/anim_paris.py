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
import v3_a, v3_b, v3_c, v3_prolog, v4_paris
FR.update(v3_a.FR); FR.update(v3_b.FRB); FR.update(v3_c.FR); FR.update(v3_prolog.FR); FR.update(v4_paris.FR)
ALIAS = {"e1b": "e1", "e5h": "e5", "e5r": "e5"}
OUT = "/home/claude/r3/paris/out"; os.makedirs(OUT, exist_ok=True); SES = "/home/claude/r3/paris/ses"; SR = 24000
K7 = "/home/claude/r3/tahta/out/K7.mp4"; K8 = "/home/claude/r3/tahta/out/K8.mp4"
dur = lambda i: sf.info(f"{SES}/r{i:02d}.wav").duration
PA = [("p15b", [(1, 0.4)], 0.4), ("p15c", [(2, 0.3)], 0.6), ("p15d", [(3, 0.3)], 0.2), ("p15e", [], 1.0), ("p16a", [(4, 0.4)], 0.4),
      ("p16b1", [(5, 0.3)], 0.2), ("p16b2", [], 1.4), ("p16c", [(6, 0.4)], 0.3), ("p1c", [(7, 0.3)], 0.4), ("p16e", [(8, 0.3)], 1.0),
      ("p17", [(9, 0.6)], 2.0), ("p18a", [(10, 0.4)], 0.8)]
PB = [("p18c", [(12, 0.4)], 0.4), ("p18d", [(13, 0.4)], 2.6)]
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
FX.BOLUM[0] = "IV"
def _evre(k): return {"p18a": YAS.RG3, "p18c": YAS.RG3, "p18d": YAS.RG3}.get(k, YAS.RG2)
def _fxk(k): return k

def compose(c, k, t, d, st):
    YAS.uygula(_evre(k))
    K.T[0] = t; K.DUR[0] = d; K.CUE2.clear(); K.CUE2.update(cues(k, st))
    img = FR[ALIAS.get(k, k)]().makeImageSnapshot()
    z0, z1, a, b = CAM.get(ALIAS.get(k, k), (1.0, 1.06, (960, 540), (960, 520))); q = t / d; q = q * q * (3 - 2 * q); z = z0 + (z1 - z0) * q
    cx = a[0] + (b[0] - a[0]) * q; cy = a[1] + (b[1] - a[1]) * q
    hw, hh = W / (2 * z), (H - 140) / (2 * z); cx = min(max(cx, hw), W - hw); cy = min(max(cy, 70 + hh), H - 70 - hh)
    _sx, _sy = FX.sarsinti(_fxk(k), t, st); c.save(); c.translate(W / 2 + _sx, H / 2 + _sy); c.scale(z, z); c.translate(-cx, -cy); c.drawImage(img, 0, 0); FX.uygula(c, _fxk(k), t, st); c.restore()
    if k == "p16e":   # kapı açılınca ışık patlaması
        fill(c, "#FFF2D0", 0.6 * max(0.0, 1 - t / 0.35))
    if k == "p18d":   # alev titreşimi
        fill(c, "#FF6A2A", 0.05 + 0.04 * math.sin(t * 15))

def mix(shots, vst, tot, path, part):
    N = int(tot * SR); tt = np.arange(N) / SR; rng = np.random.default_rng(3)
    lp = lambda x, n: np.convolve(x, np.ones(max(1, int(n))) / max(1, int(n)), mode="same").astype(np.float32)
    def put(buf, a, s): i = int(s * SR); e = min(N, i + len(a)); buf[i:e] += a[:e - i]
    def env(pts): xs, ys = zip(*pts); return np.interp(tt, xs, ys).astype(np.float32)
    voice = np.zeros(N, np.float32)
    for i, s in vst:
        a, _ = sf.read(f"{SES}/r{i:02d}.wav", dtype="float32"); put(voice, a / (np.abs(a).max() + 1e-6) * 0.8, s)
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
        wind = lp(rng.standard_normal(N).astype(np.float32), 25) * env([(0, 0.5), (S["p15c"], 0.2), (S["p15e"], 0.0), (S["p16b1"], 0.4), (S["p16b2"], 0.0), (S["p16c"], 0.4), (S["p1c"], 0.0), (S["p17"], 0.7), (S["p18a"], 0.0), (tot, 0.0)])
        fire = lp(rng.standard_normal(N).astype(np.float32), 40) * 0.5 * env([(0, 0), (S["p15c"], 1.0), (S["p15d"], 0.3), (S["p16a"], 0.4), (S["p16b1"], 0.0), (S["p16e"], 1.6), (S["p17"], 0.0), (tot, 0.0)])
        n = int(0.5 * SR); x = np.arange(n) / SR
        thud = (np.sin(2 * np.pi * 60 * x) * np.exp(-x * 8) * 0.6).astype(np.float32)
        for dt in (0.3, 1.1, 1.9): put(sfx, thud * 0.6, S["p15c"] + dt)
        put(sfx, thud, S["p15d"] + ST["p15d"][3] + 1.5)
        put(sfx, thud * 1.2, S["p16e"] + 0.05)
        roar = lp(rng2.standard_normal(N).astype(np.float32), 90) * 1.2 * env([(0, 0), (S["p16e"], 0), (S["p16e"] + 0.3, 1.0), (E["p16e"] - 0.3, 0.8), (E["p16e"], 0), (tot, 0)])
        k0 = S["p17"] + ST["p17"][9] + 2.6
        hush = env([(0, 1), (k0, 1), (k0 + 0.1, 0.0), (S["p18a"], 0.0), (S["p18a"] + 0.4, 1), (tot, 1)])
        put(music, bowed(98.0, S["p16a"], 0.045), 0.0); put(music, bowed(110.0, S["p17"] - S["p16a"], 0.05), S["p16a"]); put(music, bowed(87.3, tot - S["p17"], 0.05), S["p17"])
        out = voice + duck * (wind * 0.3 + fire * 0.12 + roar * 0.35 + music) * hush + sfx
    else:
        fire = lp(rng.standard_normal(N).astype(np.float32), 40) * 0.6 * env([(0, 0.2), (S["p18d"], 1.4), (tot, 1.0)])
        put(music, bowed(82.4, tot, 0.06), 0.0)
        out = voice + duck * (fire * 0.15 + music) + sfx
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
    ta = render_part(PA, "pa", "A"); tb = render_part(PB, "pb", "B")
    out = f"{OUT}/bolum4_paris_v1.mp4"; ins = [K7, f"{OUT}/pa.mp4", K8, f"{OUT}/pb.mp4"]
    fc = "".join(f"[{i}:v]scale=1920:1080,fps=30,format=yuv420p,setsar=1[v{i}];[{i}:a]aresample=48000,aformat=channel_layouts=stereo[a{i}];" for i in range(4))
    fc += "".join(f"[v{i}][a{i}]" for i in range(4)) + "concat=n=4:v=1:a=1[v][a]"
    cmd = ["ffmpeg", "-y", "-v", "error"] + sum([["-i", p] for p in ins], []) + ["-filter_complex", fc, "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-c:a", "aac", "-b:a", "192k", out + ".tmp.mp4"]
    subprocess.run(cmd, check=True); os.replace(out + ".tmp.mp4", out); print(out, ta, tb)
