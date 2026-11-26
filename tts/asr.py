import sys, glob, soundfile as sf, numpy as np
from scipy.signal import resample_poly
from faster_whisper import WhisperModel
m = WhisperModel('small', device='cpu', compute_type='int8')
for f in sys.argv[1:]:
    a, sr = sf.read(f, dtype='float32')
    if a.ndim > 1: a = a.mean(1)
    a = resample_poly(a, 16000, sr).astype(np.float32)
    seg, _ = m.transcribe(a, language='tr'); print(f, '|', ' '.join(s.text for s in seg), flush=True)
