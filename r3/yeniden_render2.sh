#!/bin/bash
# İki şerit (2 çekirdek). anim1 ve anim_paris köprülere (K0, K7, K8) bağlı → kopru.done beklenir.
rm -f /tmp/kopru.done
(
cd /home/claude/r3/tahta && python3 kopru.py 2>&1 | grep -v "^ok" ; touch /tmp/kopru.done
cd /home/claude/r3/veda2 && python3 anim7.py 2>&1 | grep -v "^ok" | tail -2
cd /home/claude/r3/ivar2 && python3 anim3.py 2>&1 | grep -v "^ok" | tail -2
cd /home/claude/r3/bedel && python3 anim2b.py 2>&1 | grep -v "^ok" | tail -2
cd /home/claude/r3/kesis && python3 anim3k.py 2>&1 | grep -v "^ok" | tail -2
cd /home/claude/r3/tahta && python3 montaj.py 2>&1 | tail -2
echo SERIT_A_BITTI
) > /tmp/seritA.log 2>&1 &
(
cd /home/claude/r3/bati && python3 anim_prolog.py 2>&1 | grep -v "^ok" | tail -1
cd /home/claude/r3/bati && python3 anim_kayip.py 2>&1 | grep -v "^ok" | tail -1
cd /home/claude/r3/bati && python3 anim_son.py 2>&1 | grep -v "^ok" | tail -1
until [ -f /tmp/kopru.done ]; do sleep 5; done
cd /home/claude/r3/bati && python3 anim1.py 2>&1 | grep -v "^ok" | tail -1
cd /home/claude/r3/bati && python3 anim_paris.py 2>&1 | grep -v "^ok" | tail -1
echo SERIT_B_BITTI
) > /tmp/seritB.log 2>&1 &
wait
