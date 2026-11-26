from art2 import *
items = [
 (RAGNAR_CHILD, "child", "happy", ("toy_sword",), "wave"),
 (RAGNAR_TEEN, "teen", "surprised", (), "stand"),
 (RAGNAR, "adult", "smug", ("spear",), "spear"),
 (RAGNAR_LOD, "adult", "determined", ("shield","spear"), "spear"),
 (RAGNAR_OLD, "adult", "cold", (), "cross"),
 (SIGURD_HRING, "adult", "happy", ("cup",), "stand"),
 (LAGERTHA, "adult", "determined", ("shield","sword"), "shield"),
 (THORA, "adult", "happy", (), "stand"),
 (KRAKA, "adult", "smug", ("onion",), "stand"),
 (CHARLES, "adult", "sad", (), "shrug"),
 (AELLA, "adult", "cold", (), "point"),
 (SIGURD_SNAKE, "adult", "angry", ("knife",), "grip"),
]
W=4200; H=1500
s=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}"><rect width="{W}" height="{H}" fill="#E9DCC0"/>']
for i,(sp,age,ex,pr,po) in enumerate(items):
    x = 180 + (i%6)*680; y = 680 if i<6 else 1440
    s.append(f'<g transform="translate({x},{y}) scale(1.0)">{character(sp,age,po,ex,props=pr)}</g>')
s.append('</svg>')
open('lineup.svg','w').write("".join(s))
