"""Yaş evresi denemesi: modül global'ini (RG/RGO) evreye çevirip kareleri yeniden çizer, önce/sonra kontakt sayfası çıkarır.
python3 yas_test.py <modül> <attr=EVRE,...> <çekim...>   örn: v6_son RGO=RG4 k22a k23a"""
import sys, os
sys.path[:0] = ["/home/claude/r3/bati", "/home/claude/r3", "/home/claude/r2", "/home/claude/r3/ivar2", "/home/claude/r3/veda2", "/home/claude/r3/bedel", "/home/claude/r3/kesis", "/home/claude/r3/tahta"]
import importlib, skia, ragnar_yas as Y
from PIL import Image
mod = importlib.import_module(sys.argv[1]); sets = dict(a.split("=") for a in sys.argv[2].split(","))
for a, ev in sets.items():
    for m in list(sys.modules.values()):
        if getattr(m, "__file__", "") and "/home/claude/r3" in m.__file__ and hasattr(m, a) and m.__name__ not in ("ragnar_yas", "frames"):
            setattr(m, a, getattr(Y, ev))
OUT = f"/home/claude/r3/yas/{sys.argv[1]}"; os.makedirs(OUT, exist_ok=True)
import frames
ids = sys.argv[3:]
for i in ids:
    frames.T[0] = None
    mod.FR[i]().makeImageSnapshot().save(f"{OUT}/{i}.png", skia.kPNG); print("kare", i, flush=True)
sheet = Image.new("RGB", (960 * 2 + 30, 560 * ((len(ids) + 1) // 2) + 10), "#EDE2CC")
for k, i in enumerate(ids): sheet.paste(Image.open(f"{OUT}/{i}.png").convert("RGB").resize((960, 540)), (10 + (k % 2) * 970, 10 + (k // 2) * 560))
sheet.save(f"{OUT}/kontakt.png"); print("ok")
