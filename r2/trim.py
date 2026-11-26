import json, wave, numpy as np, glob
out = {}
D = json.load(open('line_durs.json'))
for sid, durs in D.items():
    nd = []
    for i in range(len(durs)):
        f = f'audio/{sid}_{i}.wav'; w = wave.open(f); sr = w.getframerate()
        a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16)
        env = np.abs(a) > 500
        idx = np.where(env)[0]
        s, e = max(0, idx[0] - int(0.02*sr)), min(len(a), idx[-1] + int(0.06*sr))
        a = a[s:e]
        o = wave.open(f'audio/{sid}_{i}.t.wav','wb'); o.setnchannels(1); o.setsampwidth(2); o.setframerate(sr); o.writeframes(a.tobytes()); o.close()
        nd.append(len(a)/sr)
    out[sid] = nd
json.dump(out, open('line_durs.json','w'))
print(round(sum(sum(v) for v in out.values()),1), sr)
