"""II · Bedel bölüm animatiği (6 + [7 hazır] + 8 + [9 hazır] + 10). Türetildi: kesis/anim3k.py.
Efektler: mum söner + ses kesilir, yığın tutuşur, balta iner, hançer flaşı, "kral"da alkış kesilir + ışık daralır.
python3 anim2b.py prev | python3 anim2b.py → out/bolum2_bedel_v1.mp4
"""
import sys, math, os, subprocess
sys.path[:0] = ["/home/claude/r3", "/home/claude/r2", "/home/claude/r3/kesis", "/home/claude/r3/bedel"]
import numpy as np, soundfile as sf, skia
from engine import *
from fx import *
import kareler4 as K
OUT = "/home/claude/r3/bedel/out"; os.makedirs(OUT, exist_ok=True); SES = "/home/claude/r3/bedel/ses"; SR = 24000
VEDA = "/home/claude/r3/veda2/out/lagertha_vedasi_v4.mp4"; IVAR = "/home/claude/r3/ivar2/out/ivar_nehir_v5.mp4"
dur = lambda i: sf.info(f"{SES}/b{i:02d}.wav").duration
P6 = [("d1", [(0, 0.5), (1, 0.35)], 0.6), ("d2", [(2, 0.5), (3, 0.9)], 2.0), ("d3", [(4, 0.8), (5, 0.6)], 2.0)]
P8 = [("d4", [(6, 0.5)], 0.8), ("d5", [(7, 0.6), (8, 0.5)], 1.2)]
P10 = [("d6", [(9, 0.5), (10, 0.4)], 0.8), ("d7", [(11, 0.5)], 1.4), ("d8", [(12, 1.2)], 2.6)]
def timeline(plan):
    shots, vst, t0 = [], [], 0.0
    for k, lines, tail in plan:
        t = 0.0; st = {}
        for i, gap in lines:
            t += gap; st[i] = t; vst.append((i, t0 + t)); t += dur(i)
        d = t + tail; shots.append((k, d, st, t0)); t0 += d
    return shots, vst, t0

def cues(k, st):
    return {"d2": {"mum": st.get(3, 99) + 0.3}, "d3": {"yak": st.get(4, 99) + 0.2}, "d5": {"indir": st.get(8, 99)},
            "d7": {"flas": st.get(11, 99) + 0.3}, "d8": {"kral": st.get(12, 99) + 0.4}}.get(k, {})
CAM = {"d1": (1.0, 1.06, (960, 540), (900, 560)), "d2": (1.0, 1.10, (960, 540), (1000, 600)), "d3": (1.0, 1.05, (960, 560), (960, 520)),
       "d4": (1.0, 1.05, (960, 540), (1000, 520)), "d5": (1.04, 1.0, (1000, 600), (960, 540)), "d6": (1.0, 1.06, (960, 500), (960, 480)),
       "d7": (1.0, 1.08, (960, 560), (1000, 520)), "d8": (1.0, 1.10, (960, 560), (960, 480))}
# --- onaylı onarım kareleri v1 (kurul/BRIEF_onarim_v1.md, kullanıcı onayı 20.11.2026) ---
sys.path[:0] = ["/home/claude/r3/bati", "/home/claude/r3/bedel", "/home/claude/r3/kesis", "/home/claude/r3", "/home/claude/r2"]
import onarim_v1 as ON
K.FR4.update(d8=ON.FR["d8"], d2=ON.FR["d2c"], d7=ON.FR["d7c"])

# --- efekt katmanı + Ragnar yaş evresi (fx/efekt.py, ragnar_yas.py) ---
sys.path[:0] = ["/home/claude/r3", "/home/claude/r3/fx"]
import ragnar_yas as YAS, efekt as FX
FX.BOLUM[0] = "II"
def _evre(k): return {}.get(k, YAS.RG2)
def _fxk(k): return k

def compose(c, k, t, d, st):
    YAS.uygula(_evre(k))
    K.T[0] = t; K.DUR[0] = d; K.CUE2.clear(); K.CUE2.update(cues(k, st))
    img = K.FR4[k]().makeImageSnapshot()
    z0, z1, a, b = CAM[k]; q = t / d; q = q * q * (3 - 2 * q); z = z0 + (z1 - z0) * q
    cx = a[0] + (b[0] - a[0]) * q; cy = a[1] + (b[1] - a[1]) * q
    hw, hh = W / (2 * z), (H - 140) / (2 * z); cx = min(max(cx, hw), W - hw); cy = min(max(cy, 70 + hh), H - 70 - hh)
    _sx, _sy = FX.sarsinti(_fxk(k), t, st); c.save(); c.translate(W / 2 + _sx, H / 2 + _sy); c.scale(z, z); c.translate(-cx, -cy); c.drawImage(img, 0, 0); FX.uygula(c, _fxk(k), t, st); c.restore()
    if k == "d7":   # hançer flaşı
        f0 = st.get(11, 99) + 0.3; fill(c, "#FFFFFF", 0.85 * max(0.0, 1 - abs(t - f0) / 0.18))
    letterbox(c, 1.0, 70)

def mix(shots, vst, tot, path, part):
    N = int(tot * SR); tt = np.arange(N) / SR; rng = np.random.default_rng(3)
    lp = lambda x, n: np.convolve(x, np.ones(max(1, int(n))) / max(1, int(n)), mode="same").astype(np.float32)
    def put(buf, a, s): i = int(s * SR); e = min(N, i + len(a)); buf[i:e] += a[:e - i]
    def env(pts): xs, ys = zip(*pts); return np.interp(tt, xs, ys).astype(np.float32)
    voice = np.zeros(N, np.float32)
    for i, s in vst:
        a, _ = sf.read(f"{SES}/b{i:02d}.wav", dtype="float32"); put(voice, a / (np.abs(a).max() + 1e-6) * 0.8, s)
    S = {k: t0 for k, d, st, t0 in shots}; E = {k: t0 + d for k, d, st, t0 in shots}; ST = {k: st for k, d, st, t0 in shots}
    vact = np.clip(lp((np.abs(voice) > 0.02).astype(np.float32), 0.35 * SR) * 3, 0, 1); duck = 1 - 0.55 * vact
    def bowed(f, d_, amp):
        n = int(d_ * SR); x = np.arange(n) / SR; ph = 2 * np.pi * np.cumsum(f * (1 + 0.005 * np.sin(2 * np.pi * 5 * x))) / SR
        y = sum(np.sin(j * ph) / j ** 1.3 for j in range(1, 8)) * 0.5
        return (y * np.minimum(1, x / 1.2) * np.minimum(1, (d_ - x) / 1.5) * amp).astype(np.float32)
    music = np.zeros(N, np.float32); amb = np.zeros(N, np.float32); sfx = np.zeros(N, np.float32)
    ST = {k: st for k, d, st, t0 in shots}
    rng2 = np.random.default_rng(5)
    if part == "6":
        fire = lp(rng.standard_normal(N).astype(np.float32), 40) * 0.5 * env([(0, 0.3), (S["d3"], 0.3), (S["d3"] + ST["d3"][4] + 0.2, 0.3), (S["d3"] + ST["d3"][4] + 1.5, 1.4), (tot, 1.2)])
        cough = np.zeros(N, np.float32)
        for tc in (1.2, 3.4): put(cough, lp(rng.standard_normal(int(0.25 * SR)).astype(np.float32), 8) * np.exp(-np.arange(int(0.25 * SR)) / SR * 12) * 0.25, tc)
        put(music, bowed(110.0, E["d2"] - 0.5, 0.045), 0.5); put(music, bowed(98.0, tot - S["d3"], 0.05), S["d3"])
        m0 = S["d2"] + ST["d2"][3] + 0.3
        silence = env([(0, 1), (m0, 1), (m0 + 0.1, 0.0), (S["d3"] - 0.3, 0.0), (S["d3"] + 0.3, 1), (tot, 1)])   # mum sönünce müzik ve ortam kesilir
        out = voice + (duck * (fire * 0.12 + music)) * silence + cough
    elif part == "8":
        wind = lp(rng.standard_normal(N).astype(np.float32), 30) * 0.4
        drums = np.zeros(N, np.float32)
        for k_ in range(int(E["d4"] / 0.9)): put(drums, (np.sin(2 * np.pi * 55 * np.arange(int(0.3 * SR)) / SR) * np.exp(-np.arange(int(0.3 * SR)) / SR * 14) * 0.25).astype(np.float32), 0.3 + k_ * 0.9)
        n = int(0.4 * SR); x = np.arange(n) / SR; put(sfx, (np.sin(2 * np.pi * 900 * x) * np.exp(-x * 9) * 0.06).astype(np.float32), S["d5"] + 1.2)   # silah yere düşer
        put(music, bowed(103.8, E["d4"], 0.05), 0.0); put(music, bowed(87.3, tot - S["d5"], 0.05), S["d5"])
        out = voice + duck * (wind * 0.3 + drums + music) + sfx
    else:
        fire = lp(rng.standard_normal(N).astype(np.float32), 40) * 0.5
        k0 = S["d8"] + ST["d8"][12] + 0.4
        crowd = lp(rng2.standard_normal(N).astype(np.float32), 120) * 1.6 * env([(0, 0), (S["d8"] + 0.3, 0), (S["d8"] + 0.8, 1), (k0, 1), (k0 + 0.05, 0), (tot, 0)])   # alkış, "kral"da kesilir
        put(music, bowed(130.8, E["d6"], 0.04), 0.0); put(music, bowed(103.8, E["d7"] - S["d7"], 0.05), S["d7"])
        n = int(0.5 * SR); x = np.arange(n) / SR; put(sfx, lp(rng.standard_normal(n).astype(np.float32), 2) * np.exp(-x * 25) * 0.4, S["d7"] + ST["d7"][11] + 0.3)
        put(music, bowed(65.4, tot - k0, 0.06), k0)
        out = voice + duck * (fire * 0.1 + crowd * 0.4 + music) + sfx
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
    for plan in (P6, P8, P10):
        shots, _, _ = timeline(plan)
        for k, d, st, _ in shots:
            c.clear(skia.ColorBLACK); compose(c, k, 0.75 * d, d, st); p = f"{OUT}/q_{k}.png"; surf.makeImageSnapshot().save(p, skia.kPNG); pics.append(p)
    sheet = Image.new("RGB", (960 * 2 + 30, 560 * 4 + 10), "#EDE2CC")
    for i, p in enumerate(pics): sheet.paste(Image.open(p).convert("RGB").resize((960, 540)), (10 + (i % 2) * 970, 10 + (i // 2) * 560))
    sheet.save(f"{OUT}/onizleme_960.png"); [os.remove(p) for p in pics]
    print([round(timeline(p)[2], 2) for p in (P6, P8, P10)])

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "prev": preview(); sys.exit()
    t6 = render_part(P6, "p6", "6"); t8 = render_part(P8, "p8", "8"); t10 = render_part(P10, "p10", "10")
    out = f"{OUT}/bolum2_bedel_v1.mp4"; ins = [f"{OUT}/p6.mp4", VEDA, f"{OUT}/p8.mp4", IVAR, f"{OUT}/p10.mp4"]
    fc = "".join(f"[{i}:v]scale=1920:1080,fps=30,format=yuv420p,setsar=1[v{i}];[{i}:a]aresample=48000,aformat=channel_layouts=stereo[a{i}];" for i in range(5))
    fc += "".join(f"[v{i}][a{i}]" for i in range(5)) + "concat=n=5:v=1:a=1[v][a]"
    cmd = ["ffmpeg", "-y", "-v", "error"] + sum([["-i", p] for p in ins], []) + ["-filter_complex", fc, "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-c:a", "aac", "-b:a", "192k", out + ".tmp.mp4"]
    subprocess.run(cmd, check=True); os.replace(out + ".tmp.mp4", out); print(out, t6, t8, t10)
