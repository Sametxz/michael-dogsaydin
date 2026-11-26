import subprocess
from common import *
F = []
# 1 · Gece, ev: Aslaug kucağında bebek, battaniyeden ayak; Ragnar ayakta
o = '<rect width="960" height="540" fill="#241A12"/><rect y="400" width="960" height="140" fill="#30251A"/><circle cx="700" cy="380" r="260" fill="#FF9A40" opacity="0.10"/>'
o += fig(ASL2, 330, 470, 0.4, "3q", "grief", hands=("open", "open")) + baby(355, 330, 0.9, foot=True)
o += fig(RG, 660, 500, 0.48, "3q", "grief", facing=-1)
o += cold(0.2) + bands()
F.append((o, "1 · Gece, ev (5 sn)", "Oğlun doğuyor. Bacakları zayıf, kemikleri yumuşak.", "Ragnar'ın yüzüne yavaş yaklaşma. \"Bacakları\"nda kamera kısa bir an battaniyeden çıkan içe dönük küçük ayağa iner, sonra Ragnar'ın yüzüne döner. Duygu: korku."))
# 2 · Şafak öncesi: uyuyan Aslaug'un yanından bebeği alıyor
o = '<rect width="960" height="540" fill="#1A1410"/><rect y="400" width="960" height="140" fill="#241C14"/><rect x="760" y="120" width="110" height="280" fill="#3A5272"/>'
o += '<path d="M120,380 Q300,340 520,370 L520,400 L120,400 Z" fill="#5A4A3A"/><g transform="translate(260,368)"><ellipse rx="70" ry="20" fill="#6A5A70"/><circle cx="-60" cy="-12" r="18" fill="#F1CCA6"/><path d="M-78,-20 Q-60,-36 -40,-20" fill="#2E2420"/></g>'
o += f'<g opacity="0.92">{fig(RG, 620, 470, 0.46, "side", "cold")}</g>' + baby(680, 300, 0.7)
o += cold(0.35) + bands()
F.append((o, "2 · Şafak öncesi (4 sn)", "Böyle bir çocuk yaşayamaz, diye düşünüyorsun. Gece onu annesinin yanından alıyorsun.", "Kapıdan gelen mavi ışıkta siluet. \"alıyorsun\"da bebek kucağa geçer, kapı kapanır. Duygu: kararlılık."))
# 3 · Sisli nehir kıyısı: diz çökmüş Ragnar, bebek taşlarda, bıçak havada (dokunmaz)
o = river_svg(0.7) + baby(560, 470, 0.9, cry=True)
o += f'<g transform="translate(330,520) scale(0.55)">{figure(RG, "side", "stand", "grief")}</g>'.replace("scale(0.55)", "scale(0.55,0.42)")
o += knife(420, 250, 1.0, rot=10) + '<circle cx="424" cy="160" r="14" fill="#FFFFFF" opacity="0.8"/>'
o += cold(0.3) + bands()
F.append((o, "3 · Nehir kıyısı (6 sn)", "Nehrin kıyısında bıçağı kaldırıyorsun.", "Alçak açı, bıçağın arkasından. Bıçak havada kalır, bebeğe değmez. \"bıçağı\"nda ağızda soğuk bir parıltı, nehrin sesi yükselir. Duygu: dehşet."))
# 4 · Yakın plan: bebeğin eli kol halkasına dokunur, bıçak iner
o = '<rect width="960" height="540" fill="#8A98A4"/><rect width="960" height="540" fill="#C8D0D6" opacity="0.4"/>'
o += f'<path d="M960,140 Q700,200 520,300 L470,360 L520,400 L980,260 Z" fill="{RG["tunic"]}" stroke="{INK_}" stroke-width="6"/><path d="M520,300 L470,360" stroke="{INK_}" stroke-width="6"/>'
o += f'<circle cx="560" cy="330" r="46" fill="none" stroke="#D9A93A" stroke-width="16"/>' + baby(330, 470, 2.0, hand=False)
o += '<g transform="translate(470,300)"><ellipse rx="22" ry="16" fill="#F2CDAA" stroke="#1A1410" stroke-width="4" transform="rotate(-30)"/></g>'
o += '<path d="M380,370 Q440,350 500,330" stroke="#F2CDAA" stroke-width="16" fill="none" stroke-linecap="round"/><circle cx="512" cy="326" r="11" fill="#F2CDAA" stroke="#1A1410" stroke-width="3"/>'
o += knife(760, 470, 1.4, rot=120) + cold(0.25) + bands()
F.append((o, "4 · Yakın plan (5 sn)", "Yapamıyorsun.", "Sabit yakın plan. Bebeğin minik eli kol halkasına dokunur, bıçak titreyip iner. \"Yapamıyorsun\"da bıçak taşlara düşer, nehrin sesi kesilir. Duygu: kırılma."))
# 5 · Sisle uzaklaşan Ragnar; karşıdan Aslaug koşup bebeği alır
o = river_svg(0.9) + baby(470, 470, 0.6, cry=True)
o += f'<g opacity="0.55">{fig(RG, 140, 420, 0.32, "back", "neutral")}</g>' + fig(ASL2, 760, 480, 0.36, "front", "determined", pose="reach")
o += '<path d="M560,0 L700,0 L620,420 L520,420 Z" fill="#FFF2D8" opacity="0.25"/>' + cold(0.25) + bands()
F.append((o, "5 · Kurtarma (5 sn)", "Ama onu geri de götüremiyorsun. Oğlunu annesi buluyor.", "Kamera yükselerek geri çekilir. Ragnar sise karışır. \"annesi\"nde Aslaug bebeği kucağına alır, sisin içinden ışık açılır. Duygu: utanç, sonra kurtuluş."))
CW, CH, GAP, TXT = 960, 540, 40, 170
Wt = 2 * CW + 3 * GAP; Ht = 140 + 3 * (CH + TXT + GAP) + 20
o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{Wt}" height="{Ht}"><rect width="{Wt}" height="{Ht}" fill="#EDE2CC"/>',
     '<text x="40" y="95" font-family="Pirata One" font-size="72" fill="#2A1D14">Ivar nehir kıyısında · küçük kareler v1 (≈25 sn, 5 kare)</text>']
for i, (svg, title, line, note) in enumerate(F):
    x = GAP + (i % 2) * (CW + GAP); y = 140 + (i // 2) * (CH + TXT + GAP)
    o.append(f'<svg x="{x}" y="{y}" width="{CW}" height="{CH}" viewBox="0 0 960 540" overflow="hidden"><rect width="960" height="540" fill="#000"/>{svg}</svg><rect x="{x}" y="{y}" width="{CW}" height="{CH}" fill="none" stroke="#2A1D14" stroke-width="4"/>')
    o.append(f'<text x="{x}" y="{y+CH+44}" font-family="Alegreya SC" font-weight="bold" font-size="34" fill="#2A1D14">{title}</text><text x="{x}" y="{y+CH+86}" font-family="Alegreya" font-style="italic" font-size="28" fill="#5A2A1A">“{line}”</text>')
    words = note.split(); lines = [""]
    for w in words:
        if len(lines[-1]) + len(w) > 78: lines.append("")
        lines[-1] += w + " "
    for k, l in enumerate(lines[:3]): o.append(f'<text x="{x}" y="{y+CH+124+k*32}" font-family="Alegreya" font-size="25" fill="#2A1D14">{l}</text>')
o.append('</svg>')
open('sb.svg', 'w').write("".join(o))
subprocess.run(['rsvg-convert', 'sb.svg', '-w', '2000', '-o', 'ivar_kucuk_kareler_v1.png'], check=True); print("ok")
