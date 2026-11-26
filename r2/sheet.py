import sys, subprocess
from PIL import Image
ids = sys.argv[2:]; frac = float(sys.argv[1])
subprocess.run(["python3","render.py","prev"]+[f"{i}:{frac}" for i in ids], check=True)
ims=[Image.open(f"prev/{i}_{int(frac*100)}.png").convert("RGB").resize((640,360)) for i in ids]
cols=3; rows=(len(ims)+cols-1)//cols
s=Image.new("RGB",(640*cols,360*rows))
for k,im in enumerate(ims): s.paste(im,((k%cols)*640,(k//cols)*360))
s.save("prev/sheet.png")
