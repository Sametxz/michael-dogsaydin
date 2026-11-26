"""Sahne 7 · Lagertha'nın vedası, animatik v3 (örgü v2, onaylı ham kareler, 19.11 20:56).
Yalnızca anlatıcı (Damien). Hafif canlandırma (kareler2.py içindeki live/blink + eylemler):
Aslaug salona yürür; "kabul ediyor"da başını eğer; Lagertha kemerini bağlar; öpücük; araba ilerler,
Bjorn koşup yetişir ve annesinin yanına oturur; "göz kulak"ta Ragnar başını sallar; köz söner.
python3 anim7.py prev | python3 anim7.py → out/lagertha_vedasi_v4.mp4
"""
import sys, math, os, subprocess
sys.path[:0] = ["/home/claude/r3", "/home/claude/r2", "/home/claude/r3/veda2"]
import numpy as np, soundfile as sf, skia
from engine import *
from fx import *
import kareler2 as K
OUT = "/home/claude/r3/veda2/out"; os.makedirs(OUT, exist_ok=True); SES = "/home/claude/r3/veda2/ses"; SR = 24000
dur = lambda i: sf.info(f"{SES}/v{i:02d}.wav").duration
PLAN = [(1, [(0, 0.4), (1, 0.3), (2, 0.35)], 0.5),
        (2, [(3, 0.4), (4, 0.45)], 0.7),
        (3, [(5, 0.4), (6, 0.45)], 0.6),
        (4, [(7, 0.4)], 1.2),
        (5, [(8, 0.3), (9, 0.3), (10, 0.3)], 1.8),
        (6, [(11, 0.6), (12, 0.7)], 2.8)]
SHOTS = []; VST = []; t0 = 0.0
for k, lines, tail in PLAN:
    t = 0.0; st = {}
    for i, gap in lines:
        t += gap; st[i] = t; VST.append((i, t0 + t)); t += dur(i)
    d = t + tail; SHOTS.append((k, d, st, t0)); t0 += d
TOT = t0

def cues(k, st):
    if k == 2: return {"kabul": st[4] + 0.1}
    if k == 5: return {"kos": st[8], "onay": st[10] + 1.2}
    if k == 6: return {"kur": st[11] + 0.1, "kayip": st[12] + 0.2}
    return {}

CAM = {1: (1.0, 1.06, (960, 540), (1100, 560)), 2: (1.0, 1.05, (960, 540), (900, 520)), 3: (1.0, 1.05, (960, 560), (1040, 560)),
       4: (1.02, 1.10, (900, 520), (880, 480)), 5: (1.0, 1.04, (960, 560), (1060, 560)), 6: (1.0, 1.10, (1080, 480), (1180, 440))}
# --- efekt katmanı + Ragnar yaş evresi (fx/efekt.py, ragnar_yas.py) ---
sys.path[:0] = ["/home/claude/r3", "/home/claude/r3/fx"]
import ragnar_yas as YAS, efekt as FX
FX.BOLUM[0] = "II"
def _evre(k): return {}.get(k, YAS.RG2)
def _fxk(k): return f"veda_{k}"

def compose(c, k, t, d, st):
    YAS.uygula(_evre(k))
    K.T[0] = t; K.DUR[0] = d; K.CUE2.clear(); K.CUE2.update(cues(k, st))
    img = K.FR2[k]().makeImageSnapshot()
    z0, z1, a, b = CAM[k]; q = t / d; q = q * q * (3 - 2 * q); z = z0 + (z1 - z0) * q
    cx = a[0] + (b[0] - a[0]) * q; cy = a[1] + (b[1] - a[1]) * q
    hw, hh = W / (2 * z), (H - 140) / (2 * z); cx = min(max(cx, hw), W - hw); cy = min(max(cy, 70 + hh), H - 70 - hh)
    _sx, _sy = FX.sarsinti(_fxk(k), t, st); c.save(); c.translate(W / 2 + _sx, H / 2 + _sy); c.scale(z, z); c.translate(-cx, -cy); c.drawImage(img, 0, 0); FX.uygula(c, _fxk(k), t, st); c.restore()
    letterbox(c, 1.0, 70)

def mix():
    N = int(TOT * SR); tt = np.arange(N) / SR; rng = np.random.default_rng(7)
    lp = lambda x, n: np.convolve(x, np.ones(max(1, int(n))) / max(1, int(n)), mode="same").astype(np.float32)
    def put(buf, a, s): i = int(s * SR); e = min(N, i + len(a)); buf[i:e] += a[:e - i]
    def env(pts): xs, ys = zip(*pts); return np.interp(tt, xs, ys).astype(np.float32)
    voice = np.zeros(N, np.float32)
    for i, s in VST:
        a, _ = sf.read(f"{SES}/v{i:02d}.wav", dtype="float32"); put(voice, a / (np.abs(a).max() + 1e-6) * 0.8, s)
    S = {k: t0 for k, d, st, t0 in SHOTS}; E = {k: t0 + d for k, d, st, t0 in SHOTS}; ST = {k: st for k, d, st, t0 in SHOTS}
    vact = np.clip(lp((np.abs(voice) > 0.02).astype(np.float32), 0.35 * SR) * 3, 0, 1); duck = 1 - 0.55 * vact
    inside = env([(0, 1), (E[2] - 0.3, 1), (E[2] + 0.2, 0), (S[6] - 0.2, 0), (S[6] + 0.3, 0.6), (TOT, 0.3)])
    fire = lp(rng.standard_normal(N).astype(np.float32), 40) * 0.5 * (1 + 0.6 * lp((rng.standard_normal(N) > 2.2).astype(np.float32), 200)) * inside
    crowd = lp(rng.standard_normal(N).astype(np.float32), 400) * 0.8 * env([(0, 0.6), (S[1] + 2.0, 0.6), (S[1] + 3.0, 0.0), (TOT, 0)])   # salon uğultusu → susar
    wind0 = (lp(rng.standard_normal(N).astype(np.float32), 30) - lp(rng.standard_normal(N).astype(np.float32), 400)) * env([(0, 0), (S[3] - 0.2, 0), (S[3] + 0.5, 0.35), (E[5], 0.35), (E[5] + 0.4, 0.1), (TOT, 0.12)])
    wind = wind0 * env([(0, 1), (S[6] + ST[6][12] + 2.1, 1), (S[6] + ST[6][12] + 2.5, 0), (TOT, 0)])   # kapı kapanınca rüzgâr kesilir
    sfx = np.zeros(N, np.float32)
    def tone(f, d_, decay, amp): n = int(d_ * SR); x = np.arange(n) / SR; return (np.sin(2 * np.pi * f * x) * np.exp(-x * decay) * amp).astype(np.float32)
    for k_ in range(int((E[5] - S[5]) / 0.55)):   # araba tekerleği gıcırtısı + toynak
        tk = S[5] + 0.3 + k_ * 0.55; put(sfx, tone(380 + 40 * math.sin(k_), 0.18, 18, 0.03), tk); put(sfx, lp(rng.standard_normal(int(0.05 * SR)).astype(np.float32), 3) * 0.08, tk + 0.27)
    def bowed(f, d_, amp):
        n = int(d_ * SR); x = np.arange(n) / SR; ph = 2 * np.pi * np.cumsum(f * (1 + 0.005 * np.sin(2 * np.pi * 5 * x))) / SR
        y = sum(np.sin(j * ph) / j ** 1.3 for j in range(1, 8)) * 0.5
        return (y * np.minimum(1, x / 1.2) * np.minimum(1, (d_ - x) / 1.5) * amp).astype(np.float32)
    music = np.zeros(N, np.float32)
    put(music, bowed(110.0, E[2] - 0.5, 0.045), 0.5)              # La: salon, gerilim
    put(music, bowed(130.8, E[4] - S[3], 0.05), S[3])             # Do: veda
    put(music, bowed(98.0, TOT - S[5], 0.055), S[5])              # Sol: gidiş ve yalnızlık
    music *= env([(0, 1), (S[6] + ST[6][12], 1), (S[6] + ST[6][12] + 1.2, 0.25), (TOT, 0.0)])            # müzik çekilir
    put(music, bowed(73.4, TOT - (S[6] + ST[6][12]), 0.06), S[6] + ST[6][12])                      # tek, derin ton: yalnızlık
    put(sfx, lp(rng.standard_normal(int(0.4 * SR)).astype(np.float32), 30) * np.exp(-np.arange(int(0.4 * SR)) / SR * 6) * 0.5, S[6] + ST[6][12] + 2.2)   # kapı kapanır
    out = voice + duck * (fire * 0.10 + crowd * 0.25 + wind * 0.35 + music) + sfx
    out *= np.minimum(1, (TOT - tt) / 1.5)
    sf.write(f"{OUT}/mix7_raw.wav", out / (np.abs(out).max() + 1e-6) * 0.9, SR)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", f"{OUT}/mix7_raw.wav", "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "48000", f"{OUT}/mix7.wav"], check=True)
    os.remove(f"{OUT}/mix7_raw.wav")

def render(preview=False):
    surf = skia.Surface(W, H); c = surf.getCanvas()
    if preview:
        from PIL import Image
        pics = []
        for k, d, st, _ in SHOTS:
            for frac in (0.25, 0.85):
                c.clear(skia.ColorBLACK); compose(c, k, frac * d, d, st); p = f"{OUT}/q{k}_{int(frac*100)}.png"
                surf.makeImageSnapshot().save(p, skia.kPNG); pics.append(p)
        sheet = Image.new("RGB", (960 * 2 + 30, 560 * 6 + 10), "#EDE2CC")
        for i, p in enumerate(pics): sheet.paste(Image.open(p).convert("RGB").resize((960, 540)), (10 + (i % 2) * 970, 10 + (i // 2) * 560))
        sheet.save(f"{OUT}/onizleme7_960.png"); [os.remove(p) for p in pics]; print("sure", round(TOT, 2)); return
    mix()
    tmp = f"{OUT}/veda_tmp.mp4"; wr = Writer(tmp); dip = 6
    for si, (k, d, st, _) in enumerate(SHOTS):
        n = int(round(d * FPS))
        for f in range(n):
            t = f / FPS; c.clear(skia.ColorBLACK); compose(c, k, t, d, st)
            if si > 0 and f < dip: fill(c, "#000", 1 - f / dip)
            if si < len(SHOTS) - 1 and f >= n - dip: fill(c, "#000", (f - (n - dip)) / dip)
            if si == len(SHOTS) - 1 and f >= n - 24: fill(c, "#000", (f - (n - 24)) / 24)
            wr.write(surf)
    wr.close()
    out = f"{OUT}/lagertha_vedasi_v4.mp4"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", tmp, "-i", f"{OUT}/mix7.wav", "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", out + ".tmp.mp4"], check=True)
    os.replace(out + ".tmp.mp4", out); os.remove(tmp); print(out, round(TOT, 2))

if __name__ == "__main__":
    render(len(sys.argv) > 1 and sys.argv[1] == "prev")
