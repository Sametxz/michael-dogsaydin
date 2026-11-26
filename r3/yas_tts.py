import subprocess, wave, json, numpy as np
LINES = ["Onu kimseye bırakmıyorsun. Kendin taşıyorsun.",
         "Her sabah dua ettiği yere. Şelalenin başına.",
         "Haçını toprağa sen saplıyorsun.",
         "Sana tanrılarını sorgulatan tek adamdı.",
         "Ve onu, kendi tanrılarının adamı öldürdü."]
out = []
for i, t in enumerate(LINES):
    f = f"yas_ses/l{i}.wav"
    subprocess.run(['python3','-m','piper','-m','/home/claude/voices/tr_TR-dfki-medium.onnx','-f',f,'--length-scale','0.97','--sentence-silence','0.35'], input=t.encode(), check=True, capture_output=True)
    w = wave.open(f); sr = w.getframerate(); a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    nz = np.where(np.abs(a) > 0.02)[0]; a = a[max(0, nz[0] - 400): nz[-1] + 1200]
    # sona yakın en güçlü vurgunun konumu (saplıyorsun için)
    np.save(f"yas_ses/l{i}.npy", a); out.append(dict(i=i, text=t, dur=len(a) / sr, sr=sr))
json.dump(out, open("yas_ses/durs.json", "w"), ensure_ascii=False, indent=1)
for o in out: print(round(o["dur"], 2), o["text"])
