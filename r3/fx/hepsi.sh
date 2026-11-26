cd /home/claude/r3/fx
for a in bati/anim_son.py bati/anim_prolog.py bati/anim1.py bedel/anim2b.py veda2/anim7.py ivar2/anim3.py kesis/anim3k.py bati/anim_paris.py bati/anim_kayip.py; do
  timeout 900 python3 yerlestir.py /home/claude/r3/$a 2>&1 | grep -v "^ok$"
  timeout 900 python3 fx_kontakt.py /home/claude/r3/$a 2>&1 | tail -1
done
echo BITTI
