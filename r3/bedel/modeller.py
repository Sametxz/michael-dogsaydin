"""II · Bedel: yeni karakter model kartı (özgün tasarım, oyuncu benzerliği aranmaz). Gövde: art3.figure (R11)."""
import sys, subprocess
sys.path[:0] = ["/home/claude/r3", "/home/claude/r2", "/home/claude/r3/veda"]
from art3 import figure, head3, RAGNAR3, EXP
from storyboard import LAG
INK = "#1A1410"
GOLD_BAND = '<path d="M-78,-58 Q0,-92 84,-62" stroke="#1A1410" stroke-width="12" fill="none"/><path d="M-78,-58 Q0,-92 84,-62" stroke="#D8B04A" stroke-width="7" fill="none"/>' + "".join(f'<circle cx="{x}" cy="{y}" r="5" fill="#8E2A22" stroke="#1A1410" stroke-width="2"/>' for x, y in ((-40, -76), (6, -84), (50, -78)))
ROLLO = dict(RAGNAR3, hair="#3A2A1E", beard_c="#3A2A1E", beard_len=0.85, beard_w=1.0, iris="#5A6A7A", skin="#E2B894", tunic="#5A2E24", trim="#8A6A3A",
             cloak="#3A2C20", fur_collar="#6A5844", armring=True, clasp="", brow_c="#2A1E14", brow_k=1.0, face_scar=False, knot=False, beard_braid=False, side_braids=True, no_blush=True, jaw=1.15)
HORIK = dict(RAGNAR3, hair="#B8B0A0", beard_c="#C8C0B0", beard_len=0.7, beard_w=0.9, iris="#7A8A9A", skin="#E8C4A4", tunic="#2E3E5E", trim="#D8B04A",
             cloak="#1E2A40", fur_collar="#E6E0D6", armring=True, clasp="", brow_c="#A8A090", brow_k=0.8, face_scar=False, knot=False, old=True, beard_braid=True, no_blush=True, _head_extra=GOLD_BAND)
BORG = dict(RAGNAR3, hair="#A0582E", beard_c="#A0582E", beard_len=0.6, beard_w=0.8, iris="#6A8A6A", skin="#EEC6A4", tunic="#4A5A34", trim="#9A8A5A",
            cloak="#5A4A30", fur_collar="#8A7A5A", armring=True, clasp="", brow_c="#7A3E1E", brow_k=0.8, face_scar=False, knot=False, beard_braid=True, no_blush=True)
GYDA = dict(LAG, hair="#E0C070", skin="#F6D8BC", iris="#5E8CA8", tunic="#6A8A9A", cloak="#7A6A4E", scratch=False, smooth=True, no_blush=False, brow_k=0.5,
            loose=True, circlet=False, crown=False, long_braid=False, side_braids=False, clasp='<g transform="translate(-34,-430)"><circle r="10" fill="#B8C8D0" stroke="#1A1410" stroke-width="3"/></g>')
CAST = [("Rollo", ROLLO, 1.06, "ağabey · iri, koyu, gür sakal"),
        ("Kral Horik", HORIK, 1.0, "yaşlı kral · gümüş saç, taç bandı"),
        ("Jarl Borg", BORG, 1.0, "jarl · kızıl, örgülü sakal"),
        ("Gyda", GYDA, 0.62, "kızı · ~10 yaş, açık sarı saç")]
def card(out="/home/claude/r3/bedel/model_karti_v1.png"):
    W_, H_ = 2600, 1500
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W_}" height="{H_}"><rect width="{W_}" height="{H_}" fill="#EDE2CC"/>',
         '<text x="40" y="70" font-family="Pirata One" font-size="56" fill="#2A1D14">II · Bedel · yeni karakterler (model kartı v1) · Ragnar ölçek için</text>']
    from art3 import RAGNAR_UC
    o.append(f'<g transform="translate(200,1250) scale(0.95)">{figure(RAGNAR_UC, "3q", "stand", "neutral")}</g><text x="200" y="1320" text-anchor="middle" font-family="Alegreya SC" font-size="30" fill="#2A1D14">Ragnar (ölçek)</text>')
    for i, (n, sp, sc, note) in enumerate(CAST):
        x = 620 + i * 520
        o.append(f'<g transform="translate({x},1250) scale({0.95*sc})">{figure(sp, "3q", "stand", "neutral")}</g>')
        o.append(f'<g transform="translate({x},330) scale(1.5)">{head3(sp, "3q", "neutral")}</g>')
        o.append(f'<text x="{x}" y="1320" text-anchor="middle" font-family="Pirata One" font-size="44" fill="#2A1D14">{n}</text>'
                 f'<text x="{x}" y="1380" text-anchor="middle" font-family="Alegreya" font-size="22" fill="#2A1D14">{note}</text>')
    o.append('</svg>')
    open("/home/claude/r3/bedel/model_karti.svg", "w").write("".join(o))
    subprocess.run(["rsvg-convert", "/home/claude/r3/bedel/model_karti.svg", "-w", str(W_), "-o", out], check=True)
if __name__ == "__main__":
    card(); print("ok")
