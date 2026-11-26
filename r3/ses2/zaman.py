"""Bölüm zaman haritası → ses2/zaman.json. Her bölüm: video dosyası + parçalar (ofset, süre, ses olayları, çekimler)."""
import subprocess, json, os, soundfile as sf
R = "/home/claude/r3"; H = f"{R}/ses2"
def dur(p): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p], capture_output=True, text=True).stdout)
def betik(path, pat, plan, pre=""):
    out = subprocess.run(["python3", f"{H}/cikar.py", path, pat, plan] + ([pre] if pre else []), capture_output=True, text=True)
    line = [l for l in out.stdout.splitlines() if l.startswith("{")]
    if not line: raise RuntimeError(path + plan + out.stderr[-800:])
    return json.loads(line[-1])
def kopru(k):
    S = f"{R}/tahta/ses"; n = len([f for f in os.listdir(S) if f.startswith(k + "_") and f.endswith(".wav")]); t = 0.6; v = []
    for i in range(n): v.append([f"{S}/{k}_{i}.wav", t]); t += sf.info(f"{S}/{k}_{i}.wav").duration + 0.35
    return {"voice": v, "shots": [[k, 0.0, t + 1.05, k]], "bolum": "kopru"}
def yas():
    S = [0, 8.6, 12.2, 20.2, 25.8]; VST = [0.5, 4.8, S[1] + 0.4, S[2] + 0.6, S[2] + 3.7, S[3] + 0.4, S[3] + 2.9]
    return {"voice": [[f"{R}/yas_ses/d{i}.wav", t] for i, t in enumerate(VST)], "shots": [["yas", 0.0, 30.8, "yas"]], "bolum": "III"}
B = f"{R}/bati"; T = f"{R}/tahta/out"
BOLUM = {
 "prolog": (f"{R}/prolog/out/prolog_v1.mp4", [("prolog", f"{R}/prolog/out/prolog_v1.mp4", lambda: betik(f"{B}/anim_prolog.py", "p{i:02d}.wav", "PA"))]),
 "I": (f"{R}/bati/out/bolum1_bati_v3.mp4", [("pa", f"{R}/bati/out/pa.mp4", lambda: betik(f"{B}/anim1.py", "a{i:02d}.wav", "PA")),
        ("K0", f"{T}/K0.mp4", lambda: kopru("K0")), ("pb", f"{R}/bati/out/pb.mp4", lambda: betik(f"{B}/anim1.py", "a{i:02d}.wav", "PB"))]),
 "II": (f"{R}/bedel/out/bolum2_bedel_v2.mp4", [("K1", f"{T}/K1.mp4", lambda: kopru("K1")), ("p6", f"{R}/bedel/out/p6.mp4", lambda: betik(f"{R}/bedel/anim2b.py", "b{i:02d}.wav", "P6")),
        ("K2", f"{T}/K2.mp4", lambda: kopru("K2")), ("p8", f"{R}/bedel/out/p8.mp4", lambda: betik(f"{R}/bedel/anim2b.py", "b{i:02d}.wav", "P8")),
        ("K3", f"{T}/K3.mp4", lambda: kopru("K3")), ("veda", f"{R}/veda2/out/lagertha_vedasi_v4.mp4", lambda: betik(f"{R}/veda2/anim7.py", "v{i:02d}.wav", "SHOTS", "veda_")),
        ("K4", f"{T}/K4.mp4", lambda: kopru("K4")), ("ivar", f"{R}/ivar2/out/ivar_nehir_v5.mp4", lambda: betik(f"{R}/ivar2/anim3.py", "n{i:02d}.wav", "SHOTS", "ivar_")),
        ("K5", f"{T}/K5.mp4", lambda: kopru("K5")), ("p10", f"{R}/bedel/out/p10.mp4", lambda: betik(f"{R}/bedel/anim2b.py", "b{i:02d}.wav", "P10"))]),
 "III": (f"{R}/kesis/out/bolum3_kesis_v2.mp4", [("K6", f"{T}/K6.mp4", lambda: kopru("K6")), ("parcaA", f"{R}/kesis/out/parcaA.mp4", lambda: betik(f"{R}/kesis/anim3k.py", "k{i:02d}.wav", "PART_A")),
        ("yas", f"{R}/anim4/yas_sahnesi_v5.mp4", yas), ("parcaC", f"{R}/kesis/out/parcaC.mp4", lambda: betik(f"{R}/kesis/anim3k.py", "k{i:02d}.wav", "PART_C"))]),
 "IV": (f"{R}/paris/out/bolum4_paris_v1.mp4", [("K7", f"{T}/K7.mp4", lambda: kopru("K7")), ("pa", f"{R}/paris/out/pa.mp4", lambda: betik(f"{B}/anim_paris.py", "r{i:02d}.wav", "PA")),
        ("K8", f"{T}/K8.mp4", lambda: kopru("K8")), ("pb", f"{R}/paris/out/pb.mp4", lambda: betik(f"{B}/anim_paris.py", "r{i:02d}.wav", "PB"))]),
 "V": (f"{R}/kayip/out/bolum5_kayip_v1.mp4", [("kayip", f"{R}/kayip/out/bolum5_kayip_v1.mp4", lambda: betik(f"{B}/anim_kayip.py", "v{i:02d}.wav", "PA"))]),
 "VI": (f"{R}/son/out/bolum6_son_v1.mp4", [("son", f"{R}/son/out/bolum6_son_v1.mp4", lambda: betik(f"{B}/anim_son.py", "s{i:02d}.wav", "PA"))]),
}
if __name__ == "__main__":
    Z = {}
    for b, (vid, parts) in BOLUM.items():
        off = 0.0; P = []
        for name, mp4, f in parts:
            d = dur(mp4); x = f(); x.update(name=name, offset=off, dur=d, mp4=mp4); P.append(x); off += d
        Z[b] = {"video": vid, "dur": dur(vid), "sum": off, "parts": P}; print(b, round(Z[b]["dur"], 2), round(off, 2), flush=True)
    json.dump(Z, open(f"{H}/zaman.json", "w"), indent=1)
