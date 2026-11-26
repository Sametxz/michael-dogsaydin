import json, sys, math, os
import skia
sys.path.insert(0, "/home/claude/r2")
from script import SHOTS
from engine import *
import scenes_a as A
try:
    import scenes_b as B
except ImportError:
    B = None

LD = json.load(open("/home/claude/r2/line_durs.json"))

def gap_after(line):
    return 0.12 if line.rstrip()[-1:] in ",:;" else 0.28

class X:
    pass

def timeline():
    tl = []; t0 = 0.0
    for s in SHOTS:
        lead = 0.35 if s["id"] == "H1" else (0.25 if s.get("dark") else 0.12)
        cues, ends = [], []; tt = lead
        for i, line in enumerate(s["lines"]):
            cues.append(tt); d = LD[s["id"]][i]; ends.append(tt + d)
            tt += d + gap_after(line)
        tail = 0.35 + (0.45 if s.get("dark") else 0) + (2.2 if s["id"] == "F4" else 0)
        dur = round((tt - gap_after(s["lines"][-1]) + tail) * FPS) / FPS
        tl.append(dict(shot=s, start=t0, dur=dur, cues=cues, ends=ends))
        t0 += dur
    return tl

CH_NAMES = {"I": ("I", "Hring'in Oğlu"), "II": ("II", "Kalkan Kızı"), "III": ("III", "Kıllı Pantolon"), "IV": ("IV", "Kráka"),
            "V": ("V", "Paris"), "VI": ("VI", "İki Gemi"), "VII": ("VII", "Çukur"), "VIII": ("VIII", "Yavrular")}

def scene_fn(name):
    for mod in (A, B):
        if mod and hasattr(mod, name): return getattr(mod, name)
    raise KeyError(name)

SCENE_MAP = {"saga_stone": "saga_stone", "cradle": "cradle", "tapestry": "tapestry", "hearth": "hearth_scene", "growup": "growup",
             "map_crumble": "map_crumble", "teen_throne": "teen_throne", "frost_banner": "frost_banner", "army_women": "army_women",
             "lagertha_hero": "lagertha_hero", "lagertha_house": "lagertha_house", "lagertha_after": "lagertha_after", "ox_hide": "ox_hide_scene"}

def draw_shot(c, item, t, first_of_ch):
    s = item["shot"]; x = X(); x.t = t; x.dur = item["dur"]; x.shot = s
    cues = item["cues"]; x.c = lambda i: cues[min(i, len(cues) - 1)]
    x.idx = lambda: max([i for i, q in enumerate(cues) if q <= t] or [0])
    fn = scene_fn(SCENE_MAP.get(s["scene"], s["scene"]))
    fn(c, x)
    if s.get("src"):
        a = fade(t, 0.15, 0.3)
        draw(c, source_tag(s["src"]), W - 34, 30, 1.0, a=a)
    if first_of_ch and s["ch"] in CH_NAMES:
        a = fade(t, 0.1, 0.35) * (1 - fade(t, 2.6, 0.4))
        if a > 0:
            num, name = CH_NAMES[s["ch"]]
            draw(c, chapter_title(num, name), 0, H - 20 + 30 * (1 - ease_out(lin(t, 0.1, 0.6))), 1.0, a=a)

def render(out, only=None, preview=None):
    tl = timeline(); surf = skia.Surface(W, H); c = surf.getCanvas()
    seen = set(); firsts = set()
    for it in tl:
        ch = it["shot"]["ch"]
        if ch not in seen: seen.add(ch); firsts.add(it["shot"]["id"])
    if preview:
        for sid, frac in preview:
            it = next(i for i in tl if i["shot"]["id"] == sid)
            c.clear(skia.ColorBLACK); draw_shot(c, it, frac * it["dur"], sid in firsts)
            surf.makeImageSnapshot().save(f"/home/claude/r2/prev/{sid}_{int(frac*100)}.png", skia.kPNG)
        return
    wr = Writer(out); prev = None
    for it in tl:
        if only and it["shot"]["id"] not in only: continue
        n = int(round(it["dur"] * FPS)); xf = 6 if it["shot"].get("xf") else 0
        for f in range(n):
            t = f / FPS
            c.clear(skia.ColorBLACK); draw_shot(c, it, t, it["shot"]["id"] in firsts)
            wr.write(surf)
        print(it["shot"]["id"], round(it["dur"], 2), flush=True)
    wr.close()

if __name__ == "__main__":
    os.makedirs("/home/claude/r2/prev", exist_ok=True)
    if sys.argv[1] == "tl":
        tl = timeline(); print(round(sum(i["dur"] for i in tl), 1)); json.dump([(i["shot"]["id"], i["start"], i["dur"], i["cues"], i["ends"]) for i in tl], open("/home/claude/r2/timeline.json", "w"))
    elif sys.argv[1] == "prev":
        pv = [(a.split(":")[0], float(a.split(":")[1])) for a in sys.argv[2:]]
        render(None, preview=pv)
    elif sys.argv[1] == "render":
        only = sys.argv[3].split(",") if len(sys.argv) > 3 else None
        render(sys.argv[2], only=only)
