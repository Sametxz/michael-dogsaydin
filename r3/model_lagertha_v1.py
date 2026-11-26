import sys; sys.path.insert(0,'/home/claude/r3'); sys.path.insert(0,'/home/claude/r2')
from art3 import *
import subprocess
LAG = dict(RAGNAR3, female=True, hair="#D2AC5C", skin="#F2CDAA", iris="#5E8CA8", tunic="#3B5A66", trim="#C9D2D6", cloak="#6A5236",
           fur_collar="#C8BCA6", scratch=True, brow_k=0.5, armring=False, brow_c="#8A6A3A", clasp='<g transform="translate(0,-440)"><circle r="16" fill="#C9D2D6" stroke="#1A1410" stroke-width="4"/><path d="M-8,0 L8,0 M0,-8 L0,8" stroke="#1A1410" stroke-width="3"/></g>')
W_,H_=3000,2100
o=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W_}" height="{H_}"><rect width="{W_}" height="{H_}" fill="#EDE2CC"/>',
   '<text x="60" y="90" font-family="Pirata One" font-size="84" fill="#2A1D14">Lagertha · model sayfası v2 (savaşçı boyu, ince sıyrık)</text>']
for i,(v,lab) in enumerate([("front","ÖN"),("3q","3/4"),("side","PROFİL"),("back","ARKA")]):
    x=260+i*420
    o.append(f'<g transform="translate({x},900) scale(0.97)">{figure(LAG, v, "stand", "neutral", hands=("open","fist"))}</g>')
    o.append(f'<text x="{x}" y="960" font-family="Alegreya SC" font-weight="bold" font-size="40" text-anchor="middle" fill="#2A1D14">{lab}</text>')
ex=["neutral","determined","cold","tender","grief","crying","angry","smug"]
for k,e in enumerate(ex):
    cx=1980+(k%4)*250; cy=260+(k//4)*380
    o.append(f'<g transform="translate({cx},{cy}) scale(0.95)">{head3(LAG,"3q",e)}</g>')
    o.append(f'<text x="{cx}" y="{cy+270}" font-family="Alegreya SC" font-weight="bold" font-size="32" text-anchor="middle" fill="#2A1D14">{e}</text>')
# Ragnar ile yan yana boy karşılaştırması
o.append(f'<g transform="translate(2100,1960) scale(0.62)">{figure(RAGNAR_UC,"3q","stand","neutral")}</g>')
o.append(f'<g transform="translate(2360,1960) scale(0.60)">{figure(LAG,"3q","stand","determined",facing=-1)}</g>')
o.append('<text x="2230" y="2050" font-family="Alegreya SC" font-weight="bold" font-size="32" text-anchor="middle">boy karşılaştırma</text>')
o.append(f'<g transform="translate(700,1560) scale(1.8)">{head3(LAG,"3q","cold")}</g>')
o.append('<text x="700" y="2060" font-family="Alegreya SC" font-weight="bold" font-size="36" text-anchor="middle">yakın plan · soğuk karar</text>')
o.append(f'<g transform="translate(1450,1560) scale(1.8)">{head3(LAG,"side","grief")}</g>')
o.append('<text x="1450" y="2060" font-family="Alegreya SC" font-weight="bold" font-size="36" text-anchor="middle">profil · hüzün</text>')
o.append('</svg>')
open('model_l.svg','w').write("".join(o))
subprocess.run(['rsvg-convert','model_l.svg','-w','1800','-o','style/lagertha_v2.png'],check=True)
