import sys; sys.path[:0] = ['/home/claude/r3', '/home/claude/r2']
from art3 import *
INK_ = "#1A1410"
EXP["fakedead"] = (0, 0, 1.0, 0.0, "open_s", "")
EXP["sly"] = (-6, 8, 0.0, 0.0, "smirk", "")
CROSS_CL = '<g transform="translate(0,-430)"><path d="M-30,-40 Q0,0 30,-40" stroke="#6A4A30" stroke-width="3" fill="none"/><g transform="translate(0,0)"><rect x="-5" y="-6" width="10" height="34" fill="#4A3424" stroke="#1A1410" stroke-width="3"/><rect x="-14" y="2" width="28" height="9" fill="#4A3424" stroke="#1A1410" stroke-width="3"/><path d="M9,4 l4,3" stroke="#C8B89A" stroke-width="2"/></g></g>'
RAG3 = dict(RAGNAR_UC, shaved=True, skin="#E6C3A2", clasp=CROSS_CL)
RAG3D = dict(RAG3, skin="#CFC3A6")
BJA = dict(RAGNAR3, hair="#7E5E3A", beard_c="#7E5E3A", beard_len=0.72, beard_w=0.92, iris="#4C7EA6", skin="#F0C9A4", tunic="#6A4A30", trim="#9A8A5A",
           cloak="#5A4632", fur_collar="#8A7A62", face_scar=False, knot=False, beard_braid=False, armring=True, clasp="", brow_c="#4A3220")
BISH = dict(RAGNAR3, hair="#D8D4CC", beardless=True, short_hair=True, old=True, iris="#7A8A9A", skin="#EACAAE", tunic="#E8E2D4", trim="#C9A25A", cloak="#B8923A", fur_collar="#E8E2D4",
            face_scar=False, knot=False, armring=False, side_braids=False, brow_c="#B8B4AC", clasp='<g transform="translate(0,-440)"><rect x="-5" y="-14" width="10" height="34" fill="#E2B23A" stroke="#1A1410" stroke-width="3"/><rect x="-13" y="-6" width="26" height="9" fill="#E2B23A" stroke="#1A1410" stroke-width="3"/></g>')
FRANK = dict(RAGNAR3, hair="#5A4A3A", beard_c="#5A4A3A", beard_len=0.35, beard_w=0.8, iris="#6A6A5A", skin="#E8C29C", tunic="#4A5A72", trim="#C9C2B0", cloak="#3A4456",
             fur_collar="#4A5A72", face_scar=False, knot=False, beard_braid=False, armring=False, side_braids=False, clasp="", brow_c="#3A2E22")
GIS = dict(RAGNAR3, female=True, side_braids=False, long_braid=False, hair="#3A2A20", skin="#F6D8BE", iris="#5A7A6A", tunic="#7A2E3A", trim="#E2B23A", cloak="#4A2030", fur_collar="#E8E0D0",
           scratch=False, crown=False, brow_k=0.5, brow_c="#2A1E16", armring=False, clasp='<g transform="translate(0,-440)"><circle r="12" fill="#E2B23A" stroke="#1A1410" stroke-width="3"/></g>')
HY = -560
MITRE = f'<g transform="translate(0,{HY-70})"><path d="M-62,10 L-50,-110 Q0,-150 50,-110 L62,10 Z" fill="#F2ECDE" stroke="{INK_}" stroke-width="6"/><path d="M0,-140 L0,10 M-56,-30 L56,-30" stroke="#C9A25A" stroke-width="10"/><path d="M-62,10 L62,10" stroke="#C9A25A" stroke-width="12"/></g>'
HELM = f'<g transform="translate(0,{HY-30})"><path d="M-84,10 Q-88,-90 0,-104 Q88,-90 84,10 Z" fill="#8A9298" stroke="{INK_}" stroke-width="6"/><path d="M0,-104 L0,10" stroke="#5A6268" stroke-width="6"/><rect x="-7" y="6" width="14" height="70" fill="#8A9298" stroke="{INK_}" stroke-width="4"/><path d="M-84,10 L84,10" stroke="#5A6268" stroke-width="10"/></g>'
CIRCLET = f'<g transform="translate(0,{HY-56})"><path d="M-74,8 Q0,-12 74,8" stroke="#E2B23A" stroke-width="9" fill="none"/><circle cx="0" cy="-4" r="8" fill="#C83A4A" stroke="{INK_}" stroke-width="3"/></g>'
ROBE_B = f'<path d="M-92,-250 L-104,0 L104,0 L92,-250 Z" fill="#E8E2D4" stroke="{INK_}" stroke-width="6"/><path d="M-20,-250 L-24,0 M20,-250 L24,0" stroke="#C9A25A" stroke-width="10"/><path d="M-104,-6 L104,-6" stroke="#C9A25A" stroke-width="8"/>'
ROBE_G = f'<path d="M-90,-250 Q-118,-80 -116,0 L116,0 Q118,-80 90,-250 Z" fill="#7A2E3A" stroke="{INK_}" stroke-width="6"/><path d="M-116,-8 L116,-8" stroke="#E2B23A" stroke-width="8"/>'
BJ_EXTRA = ('<g transform="translate(-60,-330)"><circle r="110" fill="#8A3A2A" stroke="#1A1410" stroke-width="7"/><path d="M0,-110 L0,110 M-110,0 L110,0" stroke="#D8C8A0" stroke-width="12"/><circle r="22" fill="#9AA2AA" stroke="#1A1410" stroke-width="5"/></g>',
            '<g transform="translate(70,-250) rotate(-20)"><rect x="-6" y="0" width="12" height="190" fill="#AAB2BA" stroke="#1A1410" stroke-width="4"/><rect x="-26" y="-8" width="52" height="10" fill="#5A4430" stroke="#1A1410" stroke-width="3"/><rect x="-6" y="-46" width="12" height="40" fill="#4A3424" stroke="#1A1410" stroke-width="3"/></g>')
GIS_EXTRA = '<path d="M-60,-510 Q-90,-430 -84,-380 L-60,-390 Z M60,-510 Q90,-430 84,-380 L60,-390 Z" fill="#3A2A20" stroke="#1A1410" stroke-width="4"/><path d="M-50,-440 Q0,-420 50,-440" stroke="#E2B23A" stroke-width="6" fill="none"/>'
BANNER = '<g transform="translate(140,-40)"><rect x="-5" y="-700" width="10" height="740" fill="#6A5038" stroke="#1A1410" stroke-width="3"/><path d="M5,-690 L170,-690 L150,-620 L170,-550 L5,-550 Z" fill="#B8322A" stroke="#1A1410" stroke-width="4"/><path d="M40,-650 l30,30 l-30,30 l-30,-30 Z" fill="#E2B23A" stroke="#1A1410" stroke-width="3"/></g>'
MAIL = '<g fill="#9AA2AA" stroke="#1A1410" stroke-width="4"><path d="M-100,-440 L-128,-250 L-96,-250 L-80,-420 Z M100,-440 L128,-250 L96,-250 L80,-420 Z"/><path d="M-60,-470 Q0,-440 60,-470 L56,-440 Q0,-420 -56,-440 Z"/></g>'
KITE = '<g transform="translate(-110,-260)"><path d="M0,-130 Q70,-120 70,-40 Q60,60 0,150 Q-60,60 -70,-40 Q-70,-120 0,-130 Z" fill="#3A4E6E" stroke="#1A1410" stroke-width="6"/><path d="M0,-120 L0,140 M-60,-50 L60,-50" stroke="#C9C2B0" stroke-width="8"/></g>'
CARRY = dict(RAGNAR3, hair="#6A4A30", beard_c="#6A4A30", beard_len=0.8, beard_w=0.9, face_scar=False, knot=False, beard_braid=False, armring=False, clasp="", tunic="#5A5240", cloak="#4A4234", fur_collar="#5A5240", side_braids=False)
CARRY2 = dict(CARRY, hair="#B89A5A", beard_c="#B89A5A", tunic="#4A5448", beard_len=0.5)
CROZIER = '<g transform="translate(110,-40)"><rect x="-6" y="-560" width="12" height="620" fill="#C9A25A" stroke="#1A1410" stroke-width="4"/><path d="M0,-560 Q-50,-610 -10,-640 Q30,-650 30,-610 Q30,-590 10,-590" stroke="#C9A25A" stroke-width="14" fill="none"/></g>'
SPEAR = '<g transform="translate(100,-20)"><rect x="-5" y="-640" width="10" height="680" fill="#6A5038" stroke="#1A1410" stroke-width="3"/><path d="M0,-700 L14,-640 L-14,-640 Z" fill="#AAB2BA" stroke="#1A1410" stroke-width="3"/></g>'
def sheet():
    import subprocess
    W_, H_ = 3300, 1920
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W_}" height="{H_}"><rect width="{W_}" height="{H_}" fill="#EDE2CC"/>',
         '<text x="60" y="90" font-family="Pirata One" font-size="80" fill="#2A1D14">Paris kadrosu · model sayfası v2 (özgün tasarım)</text>']
    items = [(RAG3D, "front", "fakedead", (1.0, 1.0), "", "Ragnar · S3, tıraşlı, solgun"), (RAG3, "3q", "sly", (1.0, 1.0), "", ""),
             (BJA, "front", "determined", (1.12, 1.08), BJ_EXTRA[1], "Bjorn · %108 boy, deri tunik, kalkan, kılıç"), (BJA, "3q", "neutral", (1.12, 1.08), BJ_EXTRA[0] + BJ_EXTRA[1], ""),
             (BISH, "front", "neutral", (0.95, 0.95), ROBE_B + MITRE + CROZIER, "Piskopos"), (FRANK, "front", "cold", (1.0, 1.0), MAIL + HELM + KITE + SPEAR, "Frank askeri"),
             (GIS, "front", "cold", (0.94, 0.94), ROBE_G + GIS_EXTRA + CIRCLET + BANNER, "Prenses Gisla"), (CARRY, "front", "neutral", (1.0, 1.0), "", "Taşıyıcılar"), (CARRY2, "3q", "neutral", (1.0, 1.0), "", "")]
    for i, (sp, v, e, sc, extra, lab) in enumerate(items):
        x = 200 + i * 345
        o.append(f'<g transform="translate({x},1000) scale({0.82*sc[0]},{0.82*sc[1]})">{figure(sp, v, "stand", e)}{extra}</g>')
        if lab: o.append(f'<text x="{x + (170 if i in (0, 2, 7) else 0)}" y="1080" font-family="Alegreya SC" font-weight="bold" font-size="30" text-anchor="middle" fill="#5A2A1A">{lab}</text>')
    for k, (sp, e, lab) in enumerate([(RAG3D, "fakedead", "Ragnar ölü taklidi"), (RAG3, "sly", "Ragnar kalkış"), (BJA, "grief", "Bjorn endişe"), (BISH, "awe", "Piskopos şok"), (GIS, "angry", "Gisla öfke")]):
        cx = 330 + k * 620
        o.append(f'<g transform="translate({cx},1400) scale(1.2)">{head3(sp, "3q", e)}</g><text x="{cx}" y="1870" font-family="Alegreya SC" font-size="30" text-anchor="middle">{lab}</text>')
    o.append('</svg>')
    open('models.svg', 'w').write("".join(o))
    subprocess.run(['rsvg-convert', 'models.svg', '-w', '2000', '-o', 'paris_kadro_v2.png'], check=True)
if __name__ == "__main__": sheet(); print("ok")
