"""Tek animatik betiğinden zaman çizelgesi çıkarır (ayrı süreçte çalışır): ses olayları + çekimler → JSON (stdout).
python3 cikar.py <betik.py> <ses_kalıbı> <plan_adı|SHOTS> [fxön_ek]"""
import sys, os, json, importlib.util, io, contextlib
path, pat, plan = sys.argv[1:4]; pre = sys.argv[4] if len(sys.argv) > 4 else ""
d0 = os.path.dirname(path); sys.path[:0] = [d0]; os.chdir(d0); sys.argv = ["x"]
src = open(path).read().split('if __name__ == "__main__":')[0]
g = {"__name__": "cikar", "__file__": path}
with contextlib.redirect_stdout(io.StringIO()): exec(compile(src, path, "exec"), g)
SES = g["SES"]
if plan == "SHOTS": shots, vst = g["SHOTS"], g["VST"]
else: shots, vst = g["timeline"](g[plan])[:2]
voice = [[f"{SES}/" + pat.format(i=i), t] for i, t in vst]
print(json.dumps({"voice": voice, "shots": [[k if isinstance(k, str) else str(k), t0, d, (pre + str(k)) if pre else str(k)] for k, d, st, t0 in shots],
                  "bolum": g["FX"].BOLUM[0] if "FX" in g else None}))
