"""Ivar sahnesi v2 · animatik (kullanıcı onaylı ham kareler, 19.11 19:03).

Onaylı ham kareler değişmeden kullanılır. Üstüne kamera itişi ve canlı katmanlar eklenir: ateş titremesi,
köz, toz, sis, bıçak parıltısı, halka nabzı, ışığın açılması.
Ses: onaylı v1 anlatımı ve miksi (ivar/mix.wav, 27,6 sn), sözcük işaretleri ivar/cues.json'dan.
python3 anim.py prev  → out/p*.png (960 px kontakt) | python3 anim.py  → out/ivar_nehir_v2.mp4
"""
import sys, math, random, json, os, subprocess
sys.path[:0] = ["/home/claude/r3", "/home/claude/r2", "/home/claude/r3/veda"]
import skia
from engine import *
from fx import *
OUT = "/home/claude/r3/ivar2/out"; os.makedirs(OUT, exist_ok=True)
CUE = json.load(open("/home/claude/r3/ivar/cues.json")); D = CUE["d"]
def _flat(p):
    """Onaylı kontakt sayfasıyla aynı görünüm: alfa kanalı atılır (RGB)."""
    from PIL import Image
    q = f"{OUT}/flat_{os.path.basename(p)}"; Image.open(p).convert("RGB").save(q); return skia.Image.open(q)
IMG = {k: _flat(p) for k, p in {1: "/home/claude/r3/ivar2/kare_1.png", 2: "/home/claude/r3/ivar2/kare_2.png", 3: "/home/claude/r3/ivar2/kare_3.png",
                                           4: "/home/claude/r3/kurul/test_ivar/hero_v5.png", 5: "/home/claude/r3/ivar2/kare_5.png"}.items()}
GLINT = (1281, 140)
lin = lambda t, a, b: min(1.0, max(0.0, (t - a) / (b - a))) if b > a else float(t >= a)
ease = lambda q: q * q * (3 - 2 * q)

def plate(c, k, z, cx, cy, dx=0.0, dy=0.0):
    hw, hh = W / (2 * z), (H - 140) / (2 * z)        # görünür pencere resim içinde kalsın (letterbox hariç)
    cx = min(max(cx, hw), W - hw); cy = min(max(cy, 70 + hh), H - 70 - hh)
    c.save(); c.translate(W / 2 + dx, H / 2 + dy); c.scale(z, z); c.translate(-cx, -cy)
    c.drawImage(IMG[k], 0, 0); c.restore()

def toz(c, t, seed, col_="#E8EEF2", n=26, a=0.6, box=(0, 70, W, H - 70)):
    for j in range(n):
        r = random.Random(seed * 100 + j); x = box[0] + (r.uniform(0, 1) * (box[2] - box[0]) + t * r.uniform(-14, 14)) % (box[2] - box[0])
        y = box[1] + (r.uniform(0, 1) * (box[3] - box[1]) - t * r.uniform(4, 16)) % (box[3] - box[1])
        c.drawCircle(x, y, r.uniform(1.5, 3.5), skia.Paint(Color4f=col(col_, a * (0.5 + 0.5 * math.sin(t * 2 + j))), AntiAlias=True))

def kozler(c, t, x, y):
    glow(c, x, y, 360, "#FF7A30", 0.16 * (1 + 0.25 * math.sin(t * 9) + 0.15 * math.sin(t * 23)))
    for j in range(10):
        q = ((t * 0.45 + j / 10) % 1.0); r = random.Random(j)
        c.drawCircle(x + r.uniform(-140, 140) + 20 * math.sin(q * 6 + j), y - 320 * q, 3.2 * (1 - q), skia.Paint(Color4f=col("#FFB060", 0.85 * (1 - q)), AntiAlias=True))

def bars(c): letterbox(c, 1.0, 70)

# ------------------------------------------------------------------ çekimler
def s1(c, t, d):   # gece, ev · "bacakları"nda kamera kucağa iner
    B = CUE["bacak"]; q = ease(lin(t, B, B + 1.6))
    plate(c, 1, 1.0 + 0.03 * t / d + 0.22 * q, 960 + 380 * q, 540 + 230 * q)
    kozler(c, t, 960 - 380 * q * 1.2, 860 - 230 * q)
    bars(c)

def s2(c, t, d):   # şafak öncesi · kapıya doğru yavaş itiş, kapı ışığı nabız
    A = CUE["aliyor"]; q = ease(lin(t, 0, d))
    plate(c, 2, 1.0 + 0.08 * q, 1000 + 60 * q, 540)
    bloom_spot(c, 1420, 520, 380, "#B8D4F0", 0.08 + 0.06 * math.sin(t * 1.3) + 0.18 * lin(t, A - 0.4, A + 0.6))
    toz(c, t, 2, "#CFE2F6", 30, 0.5, (1150, 120, 1700, 1000))
    bars(c)

def s3(c, t, d):   # bıçak · alçak açı, hafif titreme, "bıçağı"nda soğuk parıltı
    K = CUE["bicak"]; sh = 2.5 * lin(t, K, K + 0.4) * (1 - lin(t, d - 0.6, d))
    plate(c, 3, 1.02 + 0.04 * t / d, 960, 560, sh * math.sin(t * 40), sh * math.cos(t * 33))
    g = lin(t, K - 0.1, K + 0.15) * (1 - 0.6 * lin(t, K + 0.3, K + 1.2))
    bloom_spot(c, *GLINT, 140, "#F4FAFF", 0.7 * g); rays(c, GLINT[0], GLINT[1], 8, "#F4FAFF", 0.25 * g, 260, t * 0.3) if False else None
    fog(c, t, 820, "#DDE4EA", 0.18, seed=3, speed=18)
    bars(c)

def s4(c, t, d):   # yapamıyorsun · çok yavaş itiş, "yapamıyorsun"da halka ve kavrama noktası ısınır
    Y = CUE["yapam"]; q = ease(lin(t, 0, d))
    plate(c, 4, 1.0 + 0.07 * q, 900 + 60 * q, 640)
    w = lin(t, Y, Y + 0.8)
    bloom_spot(c, 1022 - (1022 - 960) * 0.0, 800, 90, "#FFE4C0", 0.22 * w)
    bloom_spot(c, 747, 957, 110, "#FFD98A", 0.18 * w * (0.8 + 0.2 * math.sin(t * 3)))
    toz(c, t, 4, "#E8EEF2", 22, 0.45)
    bars(c)

def s5(c, t, d):   # kurtarma · geri çekilen kamera, sis akar, "annesi"nde ışık açılır
    A = D[4] + CUE["annesi"]; q = ease(lin(t, 0, d))
    plate(c, 5, 1.12 - 0.12 * q, 1060 + 40 * q, 560)
    fog(c, t, 700, "#DDE4EA", 0.22 + 0.1 * (1 - lin(t, A - 1, A + 1)), seed=7, speed=16)
    L = ease(lin(t, A - 0.2, A + 1.4))
    light_shaft(c, 1300, 320, 1300, 760, "#FFF4DC", 0.22 * L, t=t, y_top=-60, y_bot=1080)
    bloom_spot(c, 1300, 760, 260, "#FFE8C8", 0.22 * L)
    bars(c)

SHOTS = [(s1, D[0]), (s2, D[1]), (s3, D[2]), (s4, D[3]), (s5, D[4] + D[5])]

def render(preview=False):
    surf = skia.Surface(W, H); c = surf.getCanvas()
    if preview:
        from PIL import Image
        pics = []
        for i, (fn, d) in enumerate(SHOTS):
            for frac in (0.15, 0.85):
                c.clear(skia.ColorBLACK); fn(c, frac * d, d); p = f"{OUT}/p{i}_{int(frac*100)}.png"
                surf.makeImageSnapshot().save(p, skia.kPNG); pics.append(p)
        sheet = Image.new("RGB", (960 * 2 + 30, 560 * 5 + 10), "#EDE2CC")
        for k, p in enumerate(pics): sheet.paste(Image.open(p).resize((960, 540)), (10 + (k % 2) * 970, 10 + (k // 2) * 560))
        sheet.save(f"{OUT}/onizleme_960.png"); return
    tmp = f"{OUT}/ivar_v2_tmp.mp4"; wr = Writer(tmp); dip = 6
    for si, (fn, d) in enumerate(SHOTS):
        n = int(round(d * FPS))
        for f in range(n):
            t = f / FPS; c.clear(skia.ColorBLACK); fn(c, t, d)
            if si > 0 and f < dip: fill(c, "#000", 1 - f / dip)
            if si < len(SHOTS) - 1 and f >= n - dip: fill(c, "#000", (f - (n - dip)) / dip)
            if si == len(SHOTS) - 1 and f >= n - 24: fill(c, "#000", (f - (n - 24)) / 24)
            wr.write(surf)
    wr.close()
    out = f"{OUT}/ivar_nehir_v2.mp4"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", tmp, "-i", "/home/claude/r3/ivar/mix.wav", "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", out + ".tmp.mp4"], check=True)
    os.replace(out + ".tmp.mp4", out); os.remove(tmp); print(out)

if __name__ == "__main__":
    render(len(sys.argv) > 1 and sys.argv[1] == "prev")
