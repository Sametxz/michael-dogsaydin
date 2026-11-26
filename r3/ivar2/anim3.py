"""Ivar sahnesi v3 · zengin anlatım + hafif canlandırma (kullanıcı 19.11 19:07).
Anlatıcı yalnız (Damien), 16 cümle. Karakterler: göz kırpma, nefes, salınım + eylemler
(gözlerini kaçırma, kapıya yürüme, bıçağı kaldırıp titretme, kolun titremesi, sise karışıp kaybolma).
python3 anim3.py prev | python3 anim3.py → out/ivar_nehir_v5.mp4
"""
import sys, math, random, json, os, subprocess
sys.path[:0] = ["/home/claude/r3", "/home/claude/r2", "/home/claude/r3/veda", "/home/claude/r3/kurul/test_ivar", "/home/claude/r3/ivar2"]
import numpy as np, soundfile as sf, skia
from engine import *
from fx import *
import frames as F
import hero3 as HR
OUT = "/home/claude/r3/ivar2/out"; SES = "/home/claude/r3/ivar2/ses"; SR = 24000
dur = lambda i: sf.info(f"{SES}/n{i:02d}.wav").duration
# çekim: (kare, [(cümle, önündeki boşluk)], kuyruk)
# v5 (kullanıcı 19.11 19:54): bıçak yok. Annesinin koynundan alıp ormana götürüyorsun, parmağın kadar olduğu için
# kıyamıyorsun, ormanda bırakıyorsun, annesi buluyor.
PLAN = [(1, [(0, 0.4), (2, 0.3)], 0.5),
        (2, [(5, 0.4), (16, 0.35)], 0.6),
        (4, [(9, 0.4), (17, 0.5), (18, 0.9)], 1.0),
        (5, [(12, 0.4), (13, 0.6), (14, 0.5)], 1.4)]
SHOTS = []; VST = []; t0 = 0.0
for k, lines, tail in PLAN:
    t = 0.0; st = {}
    for i, gap in lines:
        t += gap; st[i] = t; VST.append((i, t0 + t)); t += dur(i)
    d = t + tail; SHOTS.append((k, d, st, t0)); t0 += d
TOT = t0

def cues(k, st):
    if k == 1: return {"kacir": st[2] + 3.2}
    if k == 3: return {"kaldir": st[7] + 0.35}
    return {}

def shot_surface(k, t, d, st):
    if k == 4:
        HR.LIVE[0] = True; return HR.frame(t)
    F.T[0] = t; F.DUR[0] = d; F.CUE2.clear(); F.CUE2.update(cues(k, st))
    return F.FR[k]()

CAM = {1: (1.0, 1.06, (960, 540), (1080, 600)), 2: (1.0, 1.07, (980, 540), (1060, 540)), 3: (1.02, 1.08, (960, 560), (960, 520)),
       4: (1.0, 1.07, (900, 640), (960, 640)), 5: (1.10, 1.0, (1100, 560), (960, 540))}
# --- efekt katmanı + Ragnar yaş evresi (fx/efekt.py, ragnar_yas.py) ---
sys.path[:0] = ["/home/claude/r3", "/home/claude/r3/fx"]
import ragnar_yas as YAS, efekt as FX
FX.BOLUM[0] = "II"
def _evre(k): return {}.get(k, YAS.RG2)
def _fxk(k): return f"ivar_{k}"

def compose(c, k, t, d, st):
    YAS.uygula(_evre(k))
    img = shot_surface(k, t, d, st).makeImageSnapshot()
    z0, z1, a, b = CAM[k]; q = t / d; q = q * q * (3 - 2 * q); z = z0 + (z1 - z0) * q
    cx = a[0] + (b[0] - a[0]) * q; cy = a[1] + (b[1] - a[1]) * q
    hw, hh = W / (2 * z), (H - 140) / (2 * z); cx = min(max(cx, hw), W - hw); cy = min(max(cy, 70 + hh), H - 70 - hh)
    _sx, _sy = FX.sarsinti(_fxk(k), t, st); c.save(); c.translate(W / 2 + _sx, H / 2 + _sy); c.scale(z, z); c.translate(-cx, -cy); c.drawImage(img, 0, 0); FX.uygula(c, _fxk(k), t, st); c.restore()
    letterbox(c, 1.0, 70)

# ------------------------------------------------------------------ ses
def mix():
    N = int(TOT * SR); tt = np.arange(N) / SR; rng = np.random.default_rng(3)
    lp = lambda x, n: np.convolve(x, np.ones(max(1, int(n))) / max(1, int(n)), mode="same").astype(np.float32)
    def put(buf, a, s): i = int(s * SR); e = min(N, i + len(a)); buf[i:e] += a[:e - i]
    voice = np.zeros(N, np.float32)
    for i, s in VST:
        a, _ = sf.read(f"{SES}/n{i:02d}.wav", dtype="float32"); put(voice, a / (np.abs(a).max() + 1e-6) * 0.8, s)
    S = {k: t0 for k, d, st, t0 in SHOTS}; E = {k: t0 + d for k, d, st, t0 in SHOTS}
    def env(pts): xs, ys = zip(*pts); return np.interp(tt, xs, ys).astype(np.float32)
    vact = np.clip(lp((np.abs(voice) > 0.02).astype(np.float32), 0.35 * SR) * 3, 0, 1); duck = 1 - 0.55 * vact
    fire = lp(rng.standard_normal(N).astype(np.float32), 40) * 0.5 * (1 + 0.6 * lp(rng.standard_normal(N).astype(np.float32) > 2.2, 200)) * env([(0, 1), (E[1] - 0.3, 1), (E[1] + 0.3, 0.25), (E[2], 0.0), (TOT, 0)])
    river = (lp(rng.standard_normal(N).astype(np.float32), 6) - lp(rng.standard_normal(N).astype(np.float32), 60) * 0.5) * env(
        [(0, 0), (S[4] - 0.2, 0), (S[4] + 0.6, 0.12), (S[5], 0.1), (S[5] + 1, 0.16), (TOT, 0.1)])
    ST = {k: st for k, d, st, t0 in SHOTS}
    sfx = np.zeros(N, np.float32)
    def tone(f, d_, decay, amp): n = int(d_ * SR); x = np.arange(n) / SR; return (np.sin(2 * np.pi * f * x) * np.exp(-x * decay) * amp).astype(np.float32)
    put(sfx, tone(70, 0.5, 10, 0.25), S[2] + ST[2][5] + 4.4)                               # kapı
    put(sfx, (tone(520, 0.6, 5, 0.03) * (1 + 0.3 * np.sin(2 * np.pi * 5 * np.arange(int(0.6 * SR)) / SR))).astype(np.float32), S[4] + ST[4][9] + 1.6)  # bebeğin sesi
    def bowed(f, d_, amp):
        n = int(d_ * SR); x = np.arange(n) / SR; ph = 2 * np.pi * np.cumsum(f * (1 + 0.005 * np.sin(2 * np.pi * 5 * x))) / SR
        y = sum(np.sin(j * ph) / j ** 1.3 for j in range(1, 8)) * 0.5
        return (y * np.minimum(1, x / 1.2) * np.minimum(1, (d_ - x) / 1.5) * amp).astype(np.float32)
    music = np.zeros(N, np.float32)
    music += 0.05 * np.sin(2 * np.pi * 65.41 * tt) * env([(0, 0), (1, 1), (S[4] + ST[4][18], 1), (S[4] + ST[4][18] + 0.05, 0), (S[5], 0), (S[5] + 1, 0.8), (TOT, 0)])
    put(music, bowed(130.8, E[2] - 1.0, 0.05), 1.0)                 # Do: ev
    put(music, bowed(155.6, E[4] - S[4], 0.05), S[4])               # Mi bemol: orman, kıyamama
    put(music, bowed(196.0, TOT - S[5] - 0.2, 0.06), S[5] + 0.2)    # Sol: kurtuluş
    put(music, bowed(261.6, TOT - (S[5] + ST[5][14]), 0.04), S[5] + ST[5][14])   # "Kemiksiz Ivar": yükselen ton
    out = voice + duck * (fire * 0.12 + river * 0.5 + music) + sfx
    out *= np.minimum(1, (TOT - tt) / 1.5)
    sf.write(f"{OUT}/mix_v5_raw.wav", out / (np.abs(out).max() + 1e-6) * 0.9, SR)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", f"{OUT}/mix_v5_raw.wav", "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "48000", f"{OUT}/mix_v5.wav"], check=True)

def render(preview=False):
    surf = skia.Surface(W, H); c = surf.getCanvas()
    if preview:
        from PIL import Image
        pics = []
        for k, d, st, _ in SHOTS:
            for frac in (0.2, 0.8):
                c.clear(skia.ColorBLACK); compose(c, k, frac * d, d, st); p = f"{OUT}/q{k}_{int(frac*100)}.png"
                surf.makeImageSnapshot().save(p, skia.kPNG); pics.append(p)
        sheet = Image.new("RGB", (960 * 2 + 30, 560 * 5 + 10), "#EDE2CC")
        for i, p in enumerate(pics): sheet.paste(Image.open(p).convert("RGB").resize((960, 540)), (10 + (i % 2) * 970, 10 + (i // 2) * 560))
        sheet.save(f"{OUT}/onizleme_v3_960.png"); [os.remove(p) for p in pics]; print("sure", round(TOT, 2)); return
    mix()
    tmp = f"{OUT}/ivar_v5_tmp.mp4"; wr = Writer(tmp); dip = 6
    for si, (k, d, st, _) in enumerate(SHOTS):
        n = int(round(d * FPS))
        for f in range(n):
            t = f / FPS; c.clear(skia.ColorBLACK); compose(c, k, t, d, st)
            if si > 0 and f < dip: fill(c, "#000", 1 - f / dip)
            if si < len(SHOTS) - 1 and f >= n - dip: fill(c, "#000", (f - (n - dip)) / dip)
            if si == len(SHOTS) - 1 and f >= n - 24: fill(c, "#000", (f - (n - 30)) / 30)
            wr.write(surf)
    wr.close()
    out = f"{OUT}/ivar_nehir_v5.mp4"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", tmp, "-i", f"{OUT}/mix_v5.wav", "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", out + ".tmp.mp4"], check=True)
    os.replace(out + ".tmp.mp4", out); os.remove(tmp); print(out, round(TOT, 2))

if __name__ == "__main__":
    render(len(sys.argv) > 1 and sys.argv[1] == "prev")
