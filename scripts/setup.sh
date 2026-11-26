#!/usr/bin/env bash
# Yeni bir ortamda stüdyoyu çalışır hale getirir.
# Kullanım: bash scripts/setup.sh            (repo kökünden)
#           XTTS=1 bash scripts/setup.sh     (eski yerel ses hattı da gerekiyorsa)
set -euo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"
BASE=/home/claude
mkdir -p "$BASE"

echo "== sistem paketleri"
if command -v apt-get >/dev/null; then
  (apt-get install -y librsvg2-bin ffmpeg >/dev/null 2>&1 || sudo apt-get install -y librsvg2-bin ffmpeg) || echo "apt kurulumu atlandı"
fi

echo "== python paketleri"
pip install --break-system-packages -q torch torchaudio --index-url https://download.pytorch.org/whl/cpu
pip install --break-system-packages -q -r "$REPO/requirements.txt"

echo "== fontlar"
mkdir -p ~/.fonts && cp "$REPO"/fonts/*.ttf ~/.fonts/ && fc-cache -f >/dev/null

echo "== Ragnar kod kütüphanesi yolları (eski kod /home/claude/r2, /home/claude/r3 mutlak yollarını kullanır)"
for d in r2 r3; do
  if [ -e "$BASE/$d" ] && [ ! -L "$BASE/$d" ]; then mv "$BASE/$d" "$BASE/${d}_eski_$(date +%s)"; fi
  ln -sfn "$REPO/$d" "$BASE/$d"
done

echo "== gizli anahtar klasörü"
mkdir -p "$BASE/.secrets" && chmod 700 "$BASE/.secrets"

if [ "${XTTS:-0}" = "1" ]; then
  echo "== XTTS-v2 modeli (~2 GB, yalnız yedek yerel ses hattı)"
  mkdir -p "$BASE/xtts"
  for f in config.json model.pth dvae.pth mel_stats.pth speakers_xtts.pth vocab.json; do
    [ -s "$BASE/xtts/$f" ] || curl -sSfL -o "$BASE/xtts/$f" "https://huggingface.co/coqui/XTTS-v2/resolve/main/$f"
  done
  for f in gen.py takes.py asr.py; do ln -sfn "$REPO/tts/$f" "$BASE/xtts/$f"; done
fi

echo "Hazır. Motor testi: cd $REPO/studyo/motor && python3 ornek/demo.py onizle"
