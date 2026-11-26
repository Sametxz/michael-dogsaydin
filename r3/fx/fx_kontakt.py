"""Efekt yerleşim denetimi: bir bölüm animatiğinin her çekimini, efektlerin etkin olduğu anda çizer → fx/kontrol/<bölüm>.png
python3 fx_kontakt.py <animatik.py yolu>"""
import sys, os, importlib.util
path = sys.argv[1]; d0 = os.path.dirname(path); sys.path[:0] = [d0]; os.chdir(d0)
spec = importlib.util.spec_from_file_location("anim", path); A = importlib.util.module_from_spec(spec); sys.argv = ["x"]; spec.loader.exec_module(A)
import skia
from PIL import Image, ImageDraw
FX = A.FX; ad = FX.BOLUM[0]; OUT = "/home/claude/r3/fx/kontrol"; os.makedirs(OUT, exist_ok=True)
import re as _re
_PL = [n for n in dir(A) if _re.fullmatch(r"P[A-Z0-9_]*|PLAN", n) and isinstance(getattr(A, n), list) and getattr(A, n) and isinstance(getattr(A, n)[0], tuple)]
SH = [A.timeline(getattr(A, n))[0] for n in sorted(_PL, key=lambda n: (len(n), n))] if hasattr(A, "timeline") else [A.SHOTS]
surf = skia.Surface(1920, 1080); c = surf.getCanvas(); thumbs = []
for shots in SH:
    for k, d, st, _ in shots:
        cl = FX.cues().get(A._fxk(k), [])
        ts = [FX.zaman(e.get("at"), st) for e in cl if e.get("tur") not in ("push", "shake")]
        t = min(d * 0.95, (max(ts) + 0.7) if ts else d * 0.6)
        c.clear(skia.ColorBLACK); A.compose(c, k, t, d, st)
        im = Image.frombytes("RGBA", (1920, 1080), surf.makeImageSnapshot().tobytes(), "raw", "BGRA").convert("RGB").resize((640, 360))
        ImageDraw.Draw(im).text((8, 6), f"{A._fxk(k)}  t={t:.1f}  " + ",".join(e.get("tur") for e in cl), fill="#FFFF60")
        thumbs.append(im); print(k, flush=True)
cols = 3; rows = (len(thumbs) + cols - 1) // cols
sheet = Image.new("RGB", (cols * 650 + 10, rows * 370 + 10), "#222")
for i, im in enumerate(thumbs): sheet.paste(im, (10 + (i % cols) * 650, 10 + (i // cols) * 370))
sheet.save(f"{OUT}/{ad}.png"); print("ok", ad)
