import json, subprocess, re, sys, wave
sys.path.insert(0,'.')
from script import SHOTS, TTS_FIX
out = {}
for s in SHOTS:
    durs = []
    for i, line in enumerate(s['lines']):
        t = line
        for k, v in TTS_FIX.items(): t = t.replace(k, v)
        f = f"audio/{s['id']}_{i}.wav"
        subprocess.run(['python3','-m','piper','-m','/home/claude/voices/tr_TR-dfki-medium.onnx','-f',f,
                        '--length-scale','0.86','--sentence-silence','0.0'], input=t.encode(), check=True, capture_output=True)
        w = wave.open(f); durs.append(w.getnframes()/w.getframerate())
    out[s['id']] = durs
json.dump(out, open('line_durs.json','w'), indent=0)
tot = sum(sum(v) for v in out.values()); print('speech total', round(tot,1), 'lines', sum(len(v) for v in out.values()))
