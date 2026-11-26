import sys; sys.path.insert(0,'/home/claude/r3'); sys.path.insert(0,'/home/claude/r2')
from art3 import *
import subprocess
W_,H_=3000,2100
o=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W_}" height="{H_}"><rect width="{W_}" height="{H_}" fill="#EDE2CC"/>',
   '<text x="60" y="90" font-family="Pirata One" font-size="84" fill="#2A1D14">Ragnar · model sayfası v5 (özgün tasarım, kazınmış yanlar + örgü)</text>']
views=[("front","ÖN"),("3q","3/4"),("side","PROFİL"),("back","ARKA")]
for i,(v,lab) in enumerate(views):
    x=260+i*420
    o.append(f'<g transform="translate({x},900)">{figure(RAGNAR_UC, v, "stand", "neutral", hands=("open","fist"))}</g>')
    o.append(f'<text x="{x}" y="960" font-family="Alegreya SC" font-weight="bold" font-size="40" text-anchor="middle" fill="#2A1D14">{lab}</text>')
# ifadeler (3/4 kafalar)
ex=["neutral","determined","curious","smug","laugh","angry","grief","crying","pain","awe","cold","tender"]
for k,e in enumerate(ex):
    cx=1980+(k%4)*250; cy=230+(k//4)*360
    tilt={"grief":10,"crying":12,"tender":-8,"curious":-10,"smug":-5,"pain":6,"cold":0,"awe":-6,"laugh":-8,"angry":4}.get(e,0)
    lk={"curious":0.6,"smug":0.6,"cold":-0.1,"grief":-0.2,"crying":-0.2,"awe":0.0,"tender":0.4}.get(e,None)
    grade=""
    o.append(f'<g transform="translate({cx},{cy}) rotate({tilt}) scale(0.95)">{head3(RAGNAR_UC,"3q",e,lk)}{grade}</g>')
    o.append(f'<text x="{cx}" y="{cy+232}" font-family="Alegreya SC" font-weight="bold" font-size="32" text-anchor="middle" fill="#2A1D14">{e}</text>')
# eller
for k,hs in enumerate(["open","fist","grip","point"]):
    cx=300+k*300
    o.append(f'<g transform="translate({cx},1250) scale(2.6)">{hand3(0,0,22,"#EEC6A2",hs,1)}</g>')
    o.append(f'<text x="{cx}" y="1370" font-family="Alegreya SC" font-weight="bold" font-size="32" text-anchor="middle">{hs}</text>')
# büyük yakın plan: yas
o.append(f'<g transform="translate(2300,1560) scale(1.8)">{head3(RAGNAR_UC,"3q","grief")}</g>')
o.append('<text x="2300" y="2060" font-family="Alegreya SC" font-weight="bold" font-size="36" text-anchor="middle">yakın plan · yas</text>')
o.append(f'<g transform="translate(1500,1560) scale(1.8)">{head3(RAGNAR_UC,"side","determined")}</g>')
o.append('<text x="1500" y="2060" font-family="Alegreya SC" font-weight="bold" font-size="36" text-anchor="middle">profil · kararlı</text>')
o.append('</svg>')
open('model.svg','w').write("".join(o))
subprocess.run(['rsvg-convert','model.svg','-w','1800','-o','style/model_v5.png'],check=True)
