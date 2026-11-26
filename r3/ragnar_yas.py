"""Ragnar'ın yaş evreleri: tek kaynak (R8). Yükseliş döneminde kahraman, düşüşte zayıflayan ve yaşlanan Ragnar.
Kimlik öğeleri her evrede korunur: kuzgun broş, yara izi, sakal örgüsü, önkol düğüm dövmesi, undercut + örgü (dizi kombinasyonu değil).
Kullanım: from ragnar_yas import EVRE, RG_EVRE
"""
import sys
sys.path[:0] = ["/home/claude/r3", "/home/claude/r2", "/home/claude/r3/ivar2", "/home/claude/r3/veda", "/home/claude/r3/veda2", "/home/claude/r3/kesis", "/home/claude/r3/bedel", "/home/claude/r3/floki", "/home/claude/r3/kurul/test_ivar"]
from frames import RG

# 1 · Çiftçi ve yükseliş (Prolog, Bölüm I): genç, koyu saç, canlı ten, dik duruş
RG1 = dict(RG)
# 2 · Jarl ve kral (Bölüm II–III, IV ilk kuşatma): olgun, şakaklarda ilk griler, kraliyet kürkü
RG2 = dict(RG, hair="#56402C", beard_c="#5E4A36", stubble="#6E5E4C", fur_collar="#8A7458", _king=True, mantle_fur="#7A6650",
           tunic="#2E4038", trim="#C8962E", cloak="#5A1E1E")
# 3 · Düşüş (IV ikinci Paris ve bağımlılık, Bölüm V): kırlaşmış saç ve sakal, solgun, yorgun; yaşlanma çizgileri
RG3 = dict(RG, hair="#6A5038", beard_c="#7A6650", stubble="#7A6A58", skin="#E2BE9C", old=True, _thin=0.94, _stoop=3, cloak="#3A2E2A", fur_collar="#6E6458")
# 4 · Son (Bölüm VI): ağarmış sakal, gri saç, çökmüş yüz, solgun ten, koyu pelerin
RG4 = dict(RG, hair="#8A7A68", beard_c="#A89C8A", stubble="#9A8E80", skin="#DCB898", brow_c="#7A6A5A", old=True, cloak="#2A3040", _thin=0.88, _stoop=7, tunic="#38403A")

EVRE = {"prolog": RG1, "bati": RG1, "bedel": RG2, "veda2": RG2, "ivar2": RG2, "kesis": RG2, "yas": RG2,
        "paris_15_17": RG2, "paris_18": RG3, "kayip": RG3, "son": RG4}

_SON = [None]
def uygula(spec):
    """Yüklü bütün r3 kare modüllerinde Ragnar'ı (RG / RGO) bu evreye çevirir. Kare fonksiyonları global'i çizim anında okuduğu için
    onaylı kare dosyalarına dokunmadan evre değişir. Animatik betiğinde bölüm başında ya da çekim başına çağrılır."""
    if _SON[0] is spec: return
    _SON[0] = spec
    for m in list(sys.modules.values()):
        f = getattr(m, "__file__", "") or ""
        if "/home/claude/r3" not in f or m.__name__ in ("ragnar_yas", "__main__") and not hasattr(m, "FR"): continue
        for a in ("RG", "RGO"):
            if hasattr(m, a) and isinstance(getattr(m, a), dict): setattr(m, a, spec)

if __name__ == "__main__":   # yaş evreleri model kartı → kurul/model_ragnar_yas.png
    import skia
    from kareler import full
    from engine import draw
    sys.path.insert(0, "/home/claude/r3/bati"); from kareler5 import card_at, finish
    W, H = 1920, 1080; s = skia.Surface(W, H); c = s.getCanvas(); c.clear(skia.Color(0xEE, 0xE4, 0xCC))
    for i, (sp, ad, alt, ex_) in enumerate([(RG1, "1 · ÇİFTÇİ", "Prolog, I", "determined"), (RG2, "2 · JARL ve KRAL", "II–IV (ilk Paris)", "determined"),
                                            (RG3, "3 · DÜŞÜŞ", "IV sonu, V", "grief"), (RG4, "4 · SON", "VI", "cold")]):
        x = 300 + i * 440; f = full(sp, ex_, 1.15, facing=1, look=0.3); draw(c, f, x, 960, 1.0); card_at(c, ad, x, 120, alt)
    c.drawLine(80, 962, 1840, 962, skia.Paint(Color=skia.Color(60, 40, 20), StrokeWidth=4))
    s.makeImageSnapshot().save("/home/claude/r3/kurul/model_ragnar_yas.png", skia.kPNG); print("ok")
