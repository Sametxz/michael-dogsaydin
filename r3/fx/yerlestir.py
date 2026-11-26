"""Ateş işaretlerini karedeki gerçek alevlere oturtur (ajan koordinatları 960 px tahmini).
Kamera matrisi efekt kancasında yakalanır; ekrandaki alev pikselleri kare uzayına geri çevrilir.
fire / light_flicker / embers: en yakın alev öbeğine taşınır, ölçek öbek boyuna göre; 260 px içinde alev yoksa fire silinir.
python3 yerlestir.py <animatik.py>  → isaretler.json güncellenir, rapor yazdırılır"""
import sys, os, json, importlib.util, numpy as np
path = sys.argv[1]; d0 = os.path.dirname(path); sys.path[:0] = [d0]; os.chdir(d0)
spec = importlib.util.spec_from_file_location("anim", path); A = importlib.util.module_from_spec(spec); sys.argv = ["x"]; spec.loader.exec_module(A)
import skia
from scipy import ndimage
FX = A.FX; B = FX.BOLUM[0]; M = [None]
FX.uygula = lambda c, k, t, st: M.__setitem__(0, c.getTotalMatrix())
A.FX.sarsinti = lambda *a: (0.0, 0.0)
IS = "/home/claude/r3/fx/isaretler.json"; data = json.load(open(IS))
ent = {e["cekim"]: e for e in data if e["bolum"] == B}
surf = skia.Surface(1920, 1080); c = surf.getCanvas()
import re as _re
_PL = [n for n in dir(A) if _re.fullmatch(r"P[A-Z0-9_]*|PLAN", n) and isinstance(getattr(A, n), list) and getattr(A, n) and isinstance(getattr(A, n)[0], tuple)]
SH = [A.timeline(getattr(A, n))[0] for n in sorted(_PL, key=lambda n: (len(n), n))] if hasattr(A, "timeline") else [A.SHOTS]
for shots in SH:
    for k, d, st, _ in shots:
        e = ent.get(A._fxk(k))
        if not e or not any(f["tur"] in ("fire", "light_flicker", "embers") for f in e["fx"]): continue
        c.clear(skia.ColorBLACK); A.compose(c, k, d * 0.5, d, st)
        px = np.frombuffer(surf.makeImageSnapshot().tobytes(), np.uint8).reshape(1080, 1920, 4)
        b_, g_, r_ = px[..., 0].astype(int), px[..., 1].astype(int), px[..., 2].astype(int)
        sat = (r_ - b_) / np.maximum(r_, 1)
        mask = (r_ > 165) & (sat > 0.62) & (g_ < 0.95 * r_)   # renk derecelendirmesinden bağımsız: doygun turuncu
        mask = ndimage.binary_opening(mask, structure=np.ones((5, 5)))   # ince kontur ışıklarını (rim) at
        lab, n = ndimage.label(ndimage.binary_dilation(mask, iterations=3))
        inv = M[0]; ok = inv.invert(inv) if False else None
        Mi = skia.Matrix(); M[0].invert(Mi)
        blobs = []
        for sl in ndimage.find_objects(lab):
            ys, xs = sl; h = ys.stop - ys.start; w = xs.stop - xs.start
            if h * w < 300: continue
            c1 = mask[sl] & (g_[sl] > 0.76 * r_[sl]) & (r_[sl] > 185)        # sarı çekirdek
            c2 = mask[sl] & (g_[sl] < 0.6 * r_[sl])                           # koyu turuncu dil (altın tokada yok)
            if c2.sum() < 40: continue
            core = c1 if c1.sum() >= 15 else c2
            cy_, cx_ = np.nonzero(core); bx_ = xs.start + cx_.mean(); by_ = ys.start + np.percentile(cy_, 92); ch = cy_.max() - cy_.min() + 1
            sc = M[0].getScaleX(); p = Mi.mapXY(bx_, by_)
            blobs.append((p.x(), p.y(), ch * 1.6 / sc, (cx_.max() - cx_.min() + 1) * 1.4 / sc))
            if os.environ.get("DBG"): print("  öbek", k, round(p.x()), round(p.y()), int(core.sum()), (xs.start, ys.start, xs.stop, ys.stop))
        yeni = []
        for f in e["fx"]:
            if f["tur"] in ("fire", "light_flicker", "embers"):
                if "alan" in f: fx_, fy_ = (f["alan"][0] + f["alan"][2]) / 2, f["alan"][3]
                else: fx_, fy_ = f.get("x", 960), f.get("y", 540)
                best = max(blobs, key=lambda b: (b[2] * b[3]) ** 0.5 / (((b[0] - fx_) ** 2 + (b[1] - fy_) ** 2) ** 0.5 + 150), default=None)
                dist = ((best[0] - fx_) ** 2 + (best[1] - fy_) ** 2) ** 0.5 if best else 1e9
                if dist > 560:
                    if f["tur"] == "fire": print(B, k, "fire SİLİNDİ (yakında alev yok)", round(dist)); continue
                    yeni.append(f); continue
                bx, by, bh, bw = best
                if f["tur"] == "fire": f.update(x=round(bx), y=round(by), olcek=round(max(0.25, min(2.4, min(bh, bw * 1.3) / 95)), 2))
                elif f["tur"] == "light_flicker": f.update(x=round(bx), y=round(by - bh / 2), r=round(max(120, bh * 3)))
                else: f["alan"] = [round(bx - bw), round(by - bh * 4), round(bx + bw), round(by - bh * 0.3)]
                print(B, k, f["tur"], "→", round(bx), round(by), "öbek", round(bh), "uzaklık", round(dist))
            yeni.append(f)
        e["fx"] = yeni
json.dump(data, open(IS, "w"), ensure_ascii=False, indent=1); print("ok", B)
