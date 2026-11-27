"""Prolog EN (yükseltilmiş V-Prolog) + Act I EN (R4-PARALAKS) + Act II EN (R4-PARALAKS)
birleşik 960×540 İngilizce önizleme videosu ve 16 karelik birleşik denetim şeridi üreticisi."""
import os, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg

P = Path(__file__).resolve().parent
REPO = P.parents[2]
sys.path.insert(0, str(P))

import prolog_blok_en as PR
import bolum1_blok_en as B1
import bolum2_blok_en as B2

if __name__ == "__main__":
    os.environ["STUDYO_FAST"] = "1"
    # 1) Prolog EN (upgraded V-Prolog!)
    fp = PR.build_film()
    p_mp4 = P / "prolog_en_960.mp4"
    print(f"[1/3] Prolog EN render ({fp.sure:.2f}s)...", flush=True)
    B1.render_taslak_960(fp, p_mp4, fps=16, crf=24)

    # 2) Act I EN (R4-PARALAKS fixed!)
    f1 = B1.build_film()
    b1_mp4 = P / "bolum1_v3_en_960.mp4"
    print(f"[2/3] Act I EN render ({f1.sure:.2f}s)...", flush=True)
    B1.render_taslak_960(f1, b1_mp4, fps=16, crf=24)

    # 3) Act II EN (R4-PARALAKS fixed!)
    f2 = B2.build_film()
    b2_mp4 = P / "bolum2_en_960.mp4"
    print(f"[3/3] Act II EN render ({f2.sure:.2f}s)...", flush=True)
    B2.render_taslak_960(f2, b2_mp4, fps=16, crf=24)

    # 4) Seamless ffmpeg concat -> prolog_act1_act2_en_960.mp4
    lst = P / "concat_list.txt"
    lst.write_text(f"file '{p_mp4.name}'\nfile '{b1_mp4.name}'\nfile '{b2_mp4.name}'\n", encoding="utf-8")
    merged = P / "prolog_act1_act2_en_960.mp4"
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    subprocess.run([ff, "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(merged)], check=True)
    lst.unlink()
    print("MERGED MP4 OK:", merged, flush=True)

    # 5) 16-frame unified overview filmstrip across the full ~75.4s merged video
    out_dir = P / "birlesik_kareler"
    out_dir.mkdir(exist_ok=True)
    total_s = fp.sure + f1.sure + f2.sure
    fps_sample = 16.0 / max(total_s, 1.0)
    subprocess.run([ff, "-y", "-v", "error", "-i", str(merged), "-vf", f"fps={fps_sample:.4f}", str(out_dir / "u%02d.png")], check=True)
    frames = sorted(out_dir.glob("u*.png"))[:16]
    cols, rows, tw, th, pad, top = 4, 4, 420, 236, 12, 50
    sheet = Image.new("RGB", (cols*tw+(cols+1)*pad, top+rows*(th+24)+pad), (10, 14, 22))
    draw = ImageDraw.Draw(sheet)
    ft = ImageFont.truetype(str(REPO / "fonts/AlegreyaSC-Bold.ttf"), 20)
    fl = ImageFont.truetype(str(REPO / "fonts/Alegreya.ttf"), 14)
    draw.text((pad, 14), f"UNIFIED MASTER PREVIEW: PROLOGUE + ACT I + ACT II (EN · {total_s:.1f}s · 16 FRAMES)", fill=(127,230,255), font=ft)
    for i, fp_im in enumerate(frames):
        r, c = divmod(i, cols); x, y = pad + c*(tw+pad), top + r*(th+24)
        sheet.paste(Image.open(fp_im).convert("RGB").resize((tw, th), Image.Resampling.LANCZOS), (x, y))
        draw.rectangle([x, y, x+tw, y+th], outline=(55, 85, 110), width=2)
        t_est = (i + 0.5) / fps_sample
        sec = "PROLOG" if t_est < fp.sure else ("ACT I" if t_est < fp.sure + f1.sure else "ACT II")
        draw.text((x+4, y+th+3), f"{sec} · t={t_est:.1f}s ({fp_im.name})", fill=(220,230,240), font=fl)
    out_png = P / "birlesik_denetim_960.png"
    sheet.save(out_png)
    print("UNIFIED FILMSTRIP OK:", out_png, flush=True)
