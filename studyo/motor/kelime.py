"""Kelime kilidi: anlatım sesinden kelime zamanları çıkarır ve çekimlere dağıtır.

    python3 kelime.py ses/1.01.wav            → kelime zamanlarını yazdırır
    from kelime import zamanlar
    ck = Cekim("1.01", sure, kelimeler=zamanlar("ses/1.01.wav", bas=0.4))   # satır çekim içinde 0.4 sn'de başlıyorsa

Kurallar (docs/02 §2): her cümlede en az bir öğe o cümlenin bir kelimesine kilitlenir. Kilit kelimenin
BAŞLANGICINA konur; giriş animasyonu −0.1 sn erken başlarsa göz kelimeyle aynı anda yakalar.
"""
import json, os, sys

_model = None
def zamanlar(wav, bas=0.0, dil="tr", model="small"):
    """[(kelime, başlangıç, bitiş)] — bas: satırın çekim içindeki başlangıç ofseti. Sonuç wav yanında .kelime.json olarak önbelleğe alınır."""
    onb = wav + ".kelime.json"
    if os.path.exists(onb) and os.path.getmtime(onb) > os.path.getmtime(wav):
        ws = json.load(open(onb))
    else:
        global _model
        from faster_whisper import WhisperModel
        if _model is None: _model = WhisperModel(model, device="cpu", compute_type="int8")
        import numpy as np, soundfile as sf
        from scipy.signal import resample_poly
        y, sr = sf.read(wav, dtype="float32")
        if y.ndim > 1: y = y.mean(axis=1)
        if sr != 16000: y = resample_poly(y, 16000, sr).astype("float32")   # av/ffmpeg sürüm bağımlılığı olmadan
        segs, _ = _model.transcribe(y, language=dil, word_timestamps=True, beam_size=5)
        ws = [(w.word.strip(), round(w.start, 3), round(w.end, 3)) for s in segs for w in s.words]
        json.dump(ws, open(onb, "w"), ensure_ascii=False)
    return [(w, a + bas, b + bas) for w, a, b in ws]

if __name__ == "__main__":
    for w, a, b in zamanlar(sys.argv[1]): print(f"{a:6.2f} {b:6.2f}  {w}")
