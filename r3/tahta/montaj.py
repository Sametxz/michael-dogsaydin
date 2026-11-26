"""Bölüm montajı, köprülerle birlikte (dizi sırası: 6 → 8 → 7).
II: K1 · 6 · K2 · 8 · K3 · 7 (veda) · K4 · 9 (Ivar) · K5 · 10   → bedel/out/bolum2_bedel_v2.mp4
III: K6 · bolum3_kesis_v1                                        → kesis/out/bolum3_kesis_v2.mp4
"""
import subprocess, os
K = "/home/claude/r3/tahta/out"; B = "/home/claude/r3/bedel/out"
II = [f"{K}/K1.mp4", f"{B}/p6.mp4", f"{K}/K2.mp4", f"{B}/p8.mp4", f"{K}/K3.mp4", "/home/claude/r3/veda2/out/lagertha_vedasi_v4.mp4",
      f"{K}/K4.mp4", "/home/claude/r3/ivar2/out/ivar_nehir_v5.mp4", f"{K}/K5.mp4", f"{B}/p10.mp4"]
III = [f"{K}/K6.mp4", "/home/claude/r3/kesis/out/bolum3_kesis_v1.mp4"]

def cat(ins, out):
    fc = "".join(f"[{i}:v]scale=1920:1080,fps=30,format=yuv420p,setsar=1[v{i}];[{i}:a]aresample=48000,aformat=channel_layouts=stereo[a{i}];" for i in range(len(ins)))
    fc += "".join(f"[v{i}][a{i}]" for i in range(len(ins))) + f"concat=n={len(ins)}:v=1:a=1[v][a]"
    cmd = ["ffmpeg", "-y", "-v", "error"] + sum([["-i", p] for p in ins], []) + ["-filter_complex", fc, "-map", "[v]", "-map", "[a]",
           "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-c:a", "aac", "-b:a", "192k", out + ".tmp.mp4"]
    subprocess.run(cmd, check=True); os.replace(out + ".tmp.mp4", out)
    d = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", out], capture_output=True, text=True).stdout.strip()
    print(out, d)

if __name__ == "__main__":
    cat(II, f"{B}/bolum2_bedel_v2.mp4"); cat(III, "/home/claude/r3/kesis/out/bolum3_kesis_v2.mp4")
