"""III · Keşiş bölüm animatiği: Sahne 11 + 12 (yeni) → Sahne 13 (yas sahnesi v5, hazır) → Sahne 14 (yorum çağrısı).
Efektler: ocak titreşimi, nehirde ışık huzmesinin büyümesi, Floki'nin kapıdan adımı, baltanın gölgesi, beyaz flaş + sesin
tamamen kesilmesi, Ragnar'ın çöküşü, kar ve yazı kartı. python3 anim3k.py prev | python3 anim3k.py → out/bolum3_kesis_v1.mp4
"""
import sys, math, os, subprocess
sys.path[:0] = ["/home/claude/r3", "/home/claude/r2", "/home/claude/r3/kesis"]
import numpy as np, soundfile as sf, skia
from engine import *
from fx import *
import kareler3 as K
OUT = "/home/claude/r3/kesis/out"; os.makedirs(OUT, exist_ok=True); SES = "/home/claude/r3/kesis/ses"; SR = 24000
YAS = "/home/claude/r3/anim4/yas_sahnesi_v5.mp4"
dur = lambda i: sf.info(f"{SES}/k{i:02d}.wav").duration
PART_A = [("a1", [(0, 0.5), (1, 0.35), (2, 0.4)], 0.6), ("a2", [(3, 0.5), (4, 0.4)], 0.8),
          ("b1", [(5, 0.5)], 1.0), ("b2", [(6, 0.6)], 1.2), ("b3", [(7, 2.0)], 1.0), ("b4", [(8, 0.6)], 1.8)]
PART_C = [("c1", [(9, 0.6), (10, 0.3)], 1.2)]

def timeline(plan):
    shots, vst, t0 = [], [], 0.0
    for k, lines, tail in plan:
        t = 0.0; st = {}
        for i, gap in lines:
            t += gap; st[i] = t; vst.append((i, t0 + t)); t += dur(i)
        d = t + tail; shots.append((k, d, st, t0)); t0 += d
    return shots, vst, t0

def cues(k, st):
    return {"cok": st[8] + 1.2} if k == "b4" else {}
CAM = {"a1": (1.0, 1.06, (960, 540), (900, 560)), "a2": (1.0, 1.08, (980, 520), (980, 470)), "b1": (1.0, 1.06, (960, 540), (1100, 560)),
       "b2": (1.0, 1.10, (900, 500), (900, 460)), "b3": (1.0, 1.0, (960, 540), (960, 540)), "b4": (1.0, 1.08, (900, 540), (760, 520)), "c1": (1.0, 1.05, (960, 560), (960, 520))}

# --- onaylı onarım kareleri v1 (kurul/BRIEF_onarim_v1.md, kullanıcı onayı 20.11.2026) ---
sys.path[:0] = ["/home/claude/r3/bati", "/home/claude/r3/bedel", "/home/claude/r3/kesis", "/home/claude/r3", "/home/claude/r2"]
import onarim_v1 as ON
K.FR3.update(b4=ON.FR["b4"])

# --- efekt katmanı + Ragnar yaş evresi (fx/efekt.py, ragnar_yas.py) ---
sys.path[:0] = ["/home/claude/r3", "/home/claude/r3/fx"]
import ragnar_yas as RYAS, efekt as FX
FX.BOLUM[0] = "III"
def _evre(k): return {}.get(k, RYAS.RG2)
def _fxk(k): return k

def compose(c, k, t, d, st):
    RYAS.uygula(_evre(k))
    K.T[0] = t; K.DUR[0] = d; K.CUE2.clear(); K.CUE2.update(cues(k, st))
    img = K.FR3[k]().makeImageSnapshot()
    z0, z1, a, b = CAM[k]; q = t / d; q = q * q * (3 - 2 * q); z = z0 + (z1 - z0) * q
    cx = a[0] + (b[0] - a[0]) * q; cy = a[1] + (b[1] - a[1]) * q
    hw, hh = W / (2 * z), (H - 140) / (2 * z); cx = min(max(cx, hw), W - hw); cy = min(max(cy, 70 + hh), H - 70 - hh)
    _sx, _sy = FX.sarsinti(_fxk(k), t, st); c.save(); c.translate(W / 2 + _sx, H / 2 + _sy); c.scale(z, z); c.translate(-cx, -cy); c.drawImage(img, 0, 0); FX.uygula(c, _fxk(k), t, st); c.restore()
    if k == "b3":   # beyaz flaş: ilk 0,35 sn tam beyaz, sonra siluetler belirir
        fill(c, "#FFFFFF", max(0.0, 1 - t / 0.5))
    if k == "a2":   # ışık huzmesi büyür
        bloom_spot(c, 1000, 300, 300 + 200 * q, "#FFF4D8", 0.15 * q)
    letterbox(c, 1.0, 70)

def mix(shots, vst, tot, path, part):
    N = int(tot * SR); tt = np.arange(N) / SR; rng = np.random.default_rng(3)
    lp = lambda x, n: np.convolve(x, np.ones(max(1, int(n))) / max(1, int(n)), mode="same").astype(np.float32)
    def put(buf, a, s): i = int(s * SR); e = min(N, i + len(a)); buf[i:e] += a[:e - i]
    def env(pts): xs, ys = zip(*pts); return np.interp(tt, xs, ys).astype(np.float32)
    voice = np.zeros(N, np.float32)
    for i, s in vst:
        a, _ = sf.read(f"{SES}/k{i:02d}.wav", dtype="float32"); put(voice, a / (np.abs(a).max() + 1e-6) * 0.8, s)
    S = {k: t0 for k, d, st, t0 in shots}; E = {k: t0 + d for k, d, st, t0 in shots}; ST = {k: st for k, d, st, t0 in shots}
    vact = np.clip(lp((np.abs(voice) > 0.02).astype(np.float32), 0.35 * SR) * 3, 0, 1); duck = 1 - 0.55 * vact
    def bowed(f, d_, amp):
        n = int(d_ * SR); x = np.arange(n) / SR; ph = 2 * np.pi * np.cumsum(f * (1 + 0.005 * np.sin(2 * np.pi * 5 * x))) / SR
        y = sum(np.sin(j * ph) / j ** 1.3 for j in range(1, 8)) * 0.5
        return (y * np.minimum(1, x / 1.2) * np.minimum(1, (d_ - x) / 1.5) * amp).astype(np.float32)
    music = np.zeros(N, np.float32); amb = np.zeros(N, np.float32); sfx = np.zeros(N, np.float32)
    if part == "A":
        fire = lp(rng.standard_normal(N).astype(np.float32), 40) * 0.5 * env([(0, 1), (E["a1"], 1), (E["a1"] + 0.3, 0), (S["b1"], 0), (S["b1"] + 0.3, 0.6), (E["b2"], 0.6), (E["b2"], 0), (S["b4"], 0), (S["b4"] + 0.3, 0.4), (tot, 0.3)])
        river = (lp(rng.standard_normal(N).astype(np.float32), 6) - lp(rng.standard_normal(N).astype(np.float32), 60) * 0.5) * env([(0, 0), (S["a2"], 0), (S["a2"] + 0.3, 0.16), (E["a2"], 0.16), (E["a2"] + 0.2, 0), (tot, 0)])
        amb = fire * 0.1 + river * 0.5
        put(music, bowed(146.8, E["a2"] - 0.6, 0.045), 0.6)                         # Re: yakınlık
        put(music, bowed(220.0, E["a2"] - S["a2"], 0.03), S["a2"])                  # ışık: üst ses
        put(music, bowed(103.8, S["b3"] - S["b1"], 0.055), S["b1"])                 # Sol diyez: gerilim
        put(music, bowed(87.3, tot - S["b4"], 0.05), S["b4"] + 0.4)                 # Fa: yas
        n = int(0.5 * SR); x = np.arange(n) / SR
        put(sfx, (lp(rng.standard_normal(n).astype(np.float32), 2) * np.exp(-x * 30) * 0.5).astype(np.float32), S["b3"])   # darbe (çok kısa)
        silence = env([(0, 1), (S["b3"] - 0.02, 1), (S["b3"], 0), (S["b3"] + ST["b3"][7] - 0.1, 0), (S["b3"] + ST["b3"][7] + 0.8, 1), (tot, 1)])   # flaşta ses tamamen kesilir
        put(sfx, (np.sin(2 * np.pi * 1400 * x) * np.exp(-x * 4) * 0.02).astype(np.float32), S["b3"] + 0.05)                 # kulak çınlaması
        out = voice + (duck * (amb + music)) * silence + sfx
    else:
        wind = lp(rng.standard_normal(N).astype(np.float32), 30) * 0.4
        put(music, bowed(87.3, tot - 0.2, 0.04), 0.2)
        out = voice + duck * (wind * 0.4 + music)
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
            if k != "b3" and si > 0 and f < dip: fill(c, "#000", 1 - f / dip)
            if shots[min(si + 1, len(shots) - 1)][0] != "b3" and si < len(shots) - 1 and f >= n - dip: fill(c, "#000", (f - (n - dip)) / dip)
            if si == len(shots) - 1 and f >= n - 18: fill(c, "#000", (f - (n - 18)) / 18)
            wr.write(surf)
    wr.close()
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", tmp, "-i", f"{OUT}/{name}.wav", "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", f"{OUT}/{name}.mp4"], check=True)
    os.remove(tmp); return tot

def preview():
    from PIL import Image
    pics = []; surf = skia.Surface(W, H); c = surf.getCanvas()
    for plan in (PART_A, PART_C):
        shots, _, _ = timeline(plan)
        for k, d, st, _ in shots:
            c.clear(skia.ColorBLACK); compose(c, k, 0.7 * d, d, st); p = f"{OUT}/q_{k}.png"; surf.makeImageSnapshot().save(p, skia.kPNG); pics.append(p)
    sheet = Image.new("RGB", (960 * 2 + 30, 560 * 4 + 10), "#EDE2CC")
    for i, p in enumerate(pics): sheet.paste(Image.open(p).convert("RGB").resize((960, 540)), (10 + (i % 2) * 970, 10 + (i // 2) * 560))
    sheet.save(f"{OUT}/onizleme_960.png"); [os.remove(p) for p in pics]
    print("A", round(timeline(PART_A)[2], 2), "C", round(timeline(PART_C)[2], 2))

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "prev": preview(); sys.exit()
    ta = render_part(PART_A, "parcaA", "A"); tc = render_part(PART_C, "parcaC", "C")
    out = f"{OUT}/bolum3_kesis_v1.mp4"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", f"{OUT}/parcaA.mp4", "-i", YAS, "-i", f"{OUT}/parcaC.mp4", "-filter_complex",
                    "[0:v]scale=1920:1080,fps=30,format=yuv420p[v0];[1:v]scale=1920:1080,fps=30,format=yuv420p[v1];[2:v]scale=1920:1080,fps=30,format=yuv420p[v2];"
                    "[0:a]aresample=48000,aformat=channel_layouts=stereo[a0];[1:a]aresample=48000,aformat=channel_layouts=stereo[a1];[2:a]aresample=48000,aformat=channel_layouts=stereo[a2];"
                    "[v0][a0][v1][a1][v2][a2]concat=n=3:v=1:a=1[v][a]", "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-c:a", "aac", "-b:a", "192k", out + ".tmp.mp4"], check=True)
    os.replace(out + ".tmp.mp4", out); print(out, round(ta, 2), "+ 30.8 +", round(tc, 2))
