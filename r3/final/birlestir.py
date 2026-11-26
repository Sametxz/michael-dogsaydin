"""Tam Türkçe önizleme: bölüm animatiklerini sırayla 720p olarak birleştirir.
python3 birlestir.py [çıktı_adı]"""
import subprocess, sys, os
R = "/home/claude/r3"
EK = "_ses2"
PARCA = [(f"{R}/prolog/out/prolog_v1.mp4", 0.0), (f"{R}/bati/out/bolum1_bati_v3.mp4", 0.55), (f"{R}/bedel/out/bolum2_bedel_v2.mp4", 0.0),
         (f"{R}/kesis/out/bolum3_kesis_v2.mp4", 0.0), (f"{R}/paris/out/bolum4_paris_v1.mp4", 0.0), (f"{R}/kayip/out/bolum5_kayip_v1.mp4", 0.0),
         (f"{R}/son/out/bolum6_son_v1.mp4", 0.0)]
out = f"{R}/final/{sys.argv[1] if len(sys.argv) > 1 else 'onizleme_tr_720_v2.mp4'}"
ins = sum([(["-ss", str(ss)] if ss else []) + ["-i", p.replace(".mp4", EK + ".mp4") if os.path.exists(p.replace(".mp4", EK + ".mp4")) else p] for p, ss in PARCA], [])
n = len(PARCA)
RES = os.environ.get("RES", "1280:720"); CRF = os.environ.get("CRF", "23")
fc = "".join(f"[{i}:v]scale={RES},fps=30,format=yuv420p,setsar=1[v{i}];[{i}:a]aresample=48000,aformat=channel_layouts=stereo[a{i}];" for i in range(n))
fc += "".join(f"[v{i}][a{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=1[v][a]"
subprocess.run(["ffmpeg", "-y", "-v", "error"] + ins + ["-filter_complex", fc, "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "veryfast",
                "-crf", CRF, "-c:a", "aac", "-b:a", "192k" if RES.startswith("1920") else "160k", "-movflags", "+faststart", out + ".tmp.mp4"], check=True)
os.replace(out + ".tmp.mp4", out)
d = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", out], capture_output=True, text=True).stdout.strip()
print(out, d)
