"""Model gövdeli yakın plan: art3.figure (body_turn) gövdesi + başı, büst kadrajında.
Kullanıcı 19.11 akşam: "vücutlar referans çizimlerdeki gibi olsun". Uydurma gövde yok.
fig_bust(spec, expr, look, hs, flip=False, carry=None, noarm=False)
  hs: ekrandaki baş ölçeği (head3 birimi; hero_v4 = 2.75). Yerel çapa: baş merkezi (700,520).
  carry: figür yerel koordinatında kolların arasına çizilecek SVG (bebek). flip yalnız asimetrik kimliği olmayanlara.
"""
import sys
sys.path[:0] = ["/home/claude/r3", "/home/claude/r2", "/home/claude/r3/kurul/test_ivar"]
from engine import sprite
from art3 import figure, BODY
import assets as A

def baby_in_arms(k, awake=False, cry=False, leg_out=False, s=0.34):
    """Kucaktaki bebek (figür yerel): baş uzak omuz tarafında, kundak yakın kolun üstünde."""
    lw = 5.0 / (s * k)
    return f'{A.defs(s * k)}<g transform="translate(-34,-430) scale({s}) rotate(-12)">{A.baby(awake=awake, cry=cry, leg_out=leg_out, s=s * k, lw=lw)}</g>'

def fig_bust(spec, expr, look, hs, flip=False, carry=None, noarm=False, w=1400, h=1600, hands=("open", "fist")):
    k = hs * 80 / BODY["tall"]["head_r"]
    sp = dict(spec)
    if carry: sp["_carry_svg"] = carry
    if noarm: sp["_noarm"] = True
    g = figure(sp, "3q", "stand", expr, hands=hands, look=look)
    hx, hy = 8, BODY["tall"]["head_cy"]
    sx = -k if flip else k
    tx = 700 - sx * hx; ty = 520 - k * hy
    defs = A.defs(1.0) if carry else ""
    return sprite(f'{defs}<g transform="translate({tx:.1f},{ty:.1f}) scale({sx:.4f},{k:.4f})">{g}</g>', w, h, ax=700, ay=520, ss=1.0)
