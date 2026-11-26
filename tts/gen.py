import sys, torch, json, numpy as np, soundfile as sf
from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import Xtts
torch.set_num_threads(2)
cfg = XttsConfig(); cfg.load_json("config.json")
m = Xtts.init_from_config(cfg); m.load_checkpoint(cfg, checkpoint_dir=".", use_deepspeed=False); m.eval()
spk = torch.load("speakers_xtts.pth")
jobs = json.load(open(sys.argv[1]))
for j in jobs:
    g, e = spk[j["speaker"]]["gpt_cond_latent"], spk[j["speaker"]]["speaker_embedding"]
    out = m.inference(j["text"], "tr", g, e, temperature=j.get("temp", 0.7), speed=j.get("speed", 0.9), repetition_penalty=5.0, enable_text_splitting=False)
    sf.write(j["out"], np.array(out["wav"]), 24000); print("wrote", j["out"], len(out["wav"]) / 24000, flush=True)
