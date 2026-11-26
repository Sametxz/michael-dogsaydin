import sys, json, re, difflib, torch, numpy as np, soundfile as sf
from scipy.signal import resample_poly
from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import Xtts
from faster_whisper import WhisperModel
torch.set_num_threads(2)
cfg = XttsConfig(); cfg.load_json("config.json")
m = Xtts.init_from_config(cfg); m.load_checkpoint(cfg, checkpoint_dir=".", use_deepspeed=False); m.eval()
spk = torch.load("speakers_xtts.pth"); g, e = spk["Damien Black"]["gpt_cond_latent"], spk["Damien Black"]["speaker_embedding"]
asr = WhisperModel('small', device='cpu', compute_type='int8')
norm = lambda s: re.sub(r"[^a-zçğıöşü ]", "", s.lower().replace("I", "ı").replace("İ", "i")).split()
jobs = json.load(open(sys.argv[1])); NT = int(sys.argv[2]) if len(sys.argv) > 2 else 4
report = []
for j in jobs:
    want = norm(j["text"]); best = None
    for k in range(NT):
        torch.manual_seed(100 + k)
        out = m.inference(j["text"], "tr", g, e, temperature=[0.55, 0.65, 0.75, 0.6, 0.7, 0.5][k % 6], speed=j.get("speed", 0.92), repetition_penalty=5.0, enable_text_splitting=False)
        a = np.array(out["wav"], np.float32)
        a16 = resample_poly(a, 16000, 24000).astype(np.float32)
        segs, _ = asr.transcribe(a16, language="tr", word_timestamps=True)
        words = [w for s in segs for w in s.words]
        got = norm(" ".join(w.word for w in words))
        # beklenen son kelimeyle eşleşen ilk kelimede kes
        cut = None; acc = []
        for w in words:
            acc += norm(w.word)
            if len(acc) >= len(want) and difflib.SequenceMatcher(None, acc[-1], want[-1]).ratio() > 0.6:
                cut = w.end; break
        got_c = acc if cut else got
        score = difflib.SequenceMatcher(None, " ".join(got_c), " ".join(want)).ratio() - (0.0 if cut else 0.2)
        if cut: a = a[: int((cut + 0.25) * 24000)]
        print(j["out"], k, round(score, 3), " ".join(got), flush=True)
        if best is None or score > best[0]: best = (score, a, " ".join(got_c))
    a = best[1]; nz = np.where(np.abs(a) > 0.01)[0]; a = a[max(0, nz[0] - 600): nz[-1] + 3000]
    fade = 1200; a[-fade:] *= np.linspace(1, 0, fade)
    sf.write(j["out"], a, 24000); report.append((j["out"], round(best[0], 3), best[2], round(len(a) / 24000, 2)))
for r in report: print("BEST", *r)
