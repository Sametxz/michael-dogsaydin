import sys, math, random
sys.path[:0] = ['/home/claude/r3', '/home/claude/r2', '/home/claude/r3/veda']
from art3 import *
import puppet
from storyboard import ASL, RG, fig, head, cold, bands, INK_
ASL2 = dict(ASL, tunic="#4A3A5E")
BLANKET = "#3E4A5A"; KNIT = "#C9A25A"
def baby(x, y, s, foot=False, hand=False, cry=False):
    """Yün battaniyeye sarılı bebek (Aslaug'un örgü deseni kenarda)."""
    o = f'<g transform="translate({x},{y}) scale({s})">'
    o += f'<path d="M-70,0 Q-80,-50 -30,-60 L50,-56 Q86,-40 76,0 Q60,34 0,36 Q-56,34 -70,0 Z" fill="{BLANKET}" stroke="{INK_}" stroke-width="5"/>'
    o += "".join(f'<path d="M{-56+k*14},-48 l7,8 l7,-8" stroke="{KNIT}" stroke-width="3" fill="none"/>' for k in range(8))
    o += f'<circle cx="-40" cy="-30" r="26" fill="#F2CDAA" stroke="{INK_}" stroke-width="4"/><path d="M-62,-44 Q-40,-66 -18,-46 Q-40,-56 -62,-44 Z" fill="#8A6A42"/>'
    o += (f'<path d="M-50,-30 q5,-4 10,0 M-36,-30 q5,-4 10,0" stroke="{INK_}" stroke-width="2.5" fill="none"/><ellipse cx="-38" cy="-18" rx="6" ry="4" fill="#B8605A"/>' if cry
          else f'<path d="M-50,-30 q5,3 10,0 M-36,-30 q5,3 10,0" stroke="{INK_}" stroke-width="2.5" fill="none"/><path d="M-42,-18 q4,2 8,0" stroke="{INK_}" stroke-width="2" fill="none"/>')
    if foot: o += (f'<path d="M66,6 Q86,10 92,26 Q94,36 88,40" stroke="{INK_}" stroke-width="11" fill="none" stroke-linecap="round"/><path d="M66,6 Q86,10 92,26 Q94,36 88,40" stroke="#F2CDAA" stroke-width="7" fill="none" stroke-linecap="round"/>'
                   f'<path d="M88,40 q-4,8 -14,6 q-6,-2 -2,-8 q6,-2 16,2 Z" fill="#F2CDAA" stroke="{INK_}" stroke-width="2.5"/>')
    if hand: o += f'<circle cx="-6" cy="-58" r="9" fill="#F2CDAA" stroke="{INK_}" stroke-width="3"/>'
    return o + '</g>'
def knife(x, y, s, rot=0):
    return (f'<g transform="translate({x},{y}) rotate({rot}) scale({s})"><path d="M-5,0 L-8,-90 Q0,-104 8,-90 L5,0 Z" fill="#C8D0D8" stroke="{INK_}" stroke-width="3"/>'
            f'<rect x="-12" y="0" width="24" height="7" fill="#6A5038" stroke="{INK_}" stroke-width="2"/><rect x="-6" y="7" width="12" height="40" rx="3" fill="#4A3424" stroke="{INK_}" stroke-width="2"/></g>')
def river_svg(fog=0.5):
    r = random.Random(4); o = '<defs><linearGradient id="rv" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8A98A8"/><stop offset="1" stop-color="#C8D0D6"/></linearGradient></defs><rect width="960" height="540" fill="url(#rv)"/>'
    for row, (by, hh, c) in enumerate(((300, 150, "#6A7682"), (330, 210, "#56626C"))):
        for k in range(26 - row * 8):
            x = r.uniform(-20, 980); h = r.uniform(hh * 0.7, hh); w = r.uniform(8, 16)
            o += f'<rect x="{x:.0f}" y="{by-h:.0f}" width="{w:.0f}" height="{h+8:.0f}" fill="{c}"/><path d="M{x+w/2:.0f},{by-h*0.7:.0f} l{r.choice([-1,1])*r.uniform(16,30):.0f},{-r.uniform(14,30):.0f}" stroke="{c}" stroke-width="4"/>'
        o += f'<path d="M-20,{by} Q480,{by-10} 980,{by+4} L980,{by+20} L-20,{by+20} Z" fill="{c}"/>'
    o += '<path d="M0,370 Q480,350 960,372 L960,430 Q480,412 0,436 Z" fill="#7A90A2"/>' + "".join(f'<path d="M{r.uniform(0,940):.0f},{r.uniform(380,420):.0f} q14,-4 28,0" stroke="#C8D8E4" stroke-width="2" fill="none" opacity="0.7"/>' for _ in range(18))
    o += '<path d="M0,420 Q480,400 960,426 L960,540 L0,540 Z" fill="#5A5248"/>' + "".join(f'<ellipse cx="{r.uniform(0,960):.0f}" cy="{r.uniform(440,540):.0f}" rx="{r.uniform(10,30):.0f}" ry="{r.uniform(6,12):.0f}" fill="{r.choice(["#7A7268","#8A8278","#6A6258"])}" stroke="#3A342C" stroke-width="2"/>' for _ in range(40))
    o += f'<rect width="960" height="540" fill="#D8E0E6" opacity="{fog*0.35}"/>'
    return o
