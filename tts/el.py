"""ElevenLabs TTS yardımcısı (anahtar: /home/claude/.secrets/elevenlabs_key; repoya girmez).
el.py <json> : [{"text","out","voice","model"(ops),"lang"(ops),"stability"(ops)}] → mp3 indirir, wav 24k mono'ya çevirir.
"""
import json, sys, os, subprocess, time, urllib.request
KEY = open("/home/claude/.secrets/elevenlabs_key").read().strip()
VOICES = {"george": "JBFqnCBsd6RMkjVDRZzb", "brian": "nPczCjzI2devNBz1zQrb", "bill": "pqHfZKP75CvOlQylNhV4", "adam": "pNInz6obpgDQGcFmaJgB", "daniel": "onwK4e9ZLuTAKqWW03F9"}

def tts(text, out, voice="george", model="eleven_v3", lang=None, stability=0.5, style=None, retries=3):
    vid = VOICES.get(voice, voice)
    body = {"text": text, "model_id": model, "voice_settings": {"stability": stability, "similarity_boost": 0.8}}
    if style is not None: body["voice_settings"]["style"] = style
    if lang: body["language_code"] = lang
    req = urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{vid}?output_format=mp3_44100_128",
                                 data=json.dumps(body).encode(), headers={"xi-api-key": KEY, "Content-Type": "application/json", "Accept": "audio/mpeg"})
    for a in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=120) as r: data = r.read()
            break
        except urllib.error.HTTPError as e:
            msg = e.read().decode()[:300]
            if a == retries - 1: raise RuntimeError(f"{e.code} {msg}")
            time.sleep(3)
    mp3 = out[:-4] + ".mp3"; open(mp3, "wb").write(data)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", mp3, "-ar", "24000", "-ac", "1", out], check=True)
    return out

if __name__ == "__main__":
    for d in json.load(open(sys.argv[1])):
        os.makedirs(os.path.dirname(d["out"]), exist_ok=True)
        tts(d["text"], d["out"], d.get("voice", "george"), d.get("model", "eleven_v3"), d.get("lang"), d.get("stability", 0.5), d.get("style"))
        print("ok", d["out"], len(d["text"]))

def sfx(text, out, seconds=None, influence=0.45, retries=3):
    """ElevenLabs Sound Effects → wav 48k stereo. 11 kredi/sn (süre verilince)."""
    import requests, subprocess, time, os
    body = {"text": text, "prompt_influence": influence}
    if seconds: body["duration_seconds"] = float(seconds)
    for k in range(retries):
        r = requests.post("https://api.elevenlabs.io/v1/sound-generation?output_format=mp3_44100_128", headers={"xi-api-key": KEY}, json=body, timeout=180)
        if r.status_code == 200:
            mp = out.rsplit(".", 1)[0] + ".mp3"; open(mp, "wb").write(r.content)
            subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", mp, "-ar", "48000", "-ac", "2", out], check=True); return out
        print("sfx hata", r.status_code, r.text[:200]); time.sleep(3 * (k + 1))
    raise RuntimeError(out)
