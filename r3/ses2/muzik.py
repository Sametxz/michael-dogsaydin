"""Eleven Music: bölüm başına bir enstrümantal parça; bölümler duygu dönüşlerinde değişir (çekim başlangıçlarına hizalı).
Anlatım altına yazılır: orta frekanslar sade, ritim seyrek, vokal yok. python3 muzik.py [bölüm...]"""
import json, sys, os, requests, subprocess
H = "/home/claude/r3/ses2"; KEY = open("/home/claude/.secrets/elevenlabs_key2").read().strip()
Z = json.load(open(f"{H}/zaman.json")); os.makedirs(f"{H}/muzik", exist_ok=True)
GLOBAL = ["instrumental", "cinematic underscore", "Nordic folk", "Viking era", "tagelharpa", "kraviklyre lyre", "frame drum", "deep low drones",
          "sparse arrangement", "warm low end", "leaves space for narration", "slow tempo"]
NEG = ["vocals", "lyrics", "singing", "choir words", "electronic", "synth pop", "modern drum kit", "electric guitar", "rap", "busy melody"]
# (başlangıç çekimi ya da parça adı, bölüm adı, yerel stiller)
PLAN = {
 "prolog": [("e5h", "Ember", ["ominous low drone", "distant fire", "tension"]), ("p1a", "Legend", ["mythic", "rising", "slow frame drum heartbeat", "hopeful horn-like drone"]),
            ("p2a", "Hearth tale", ["intimate", "soft lyre", "warm", "storytelling"]), ("p2b", "Odin", ["awe", "huge low drone swell", "divine", "slow timpani-like frame drum rolls"]),
            ("p2c", "Belief", ["soft lyre returns", "tender"]), ("p3a", "Arm ring", ["proud", "gentle build", "warm strings of tagelharpa"]), ("p3c", "Promise", ["resolve", "open fifths", "gentle ending"])],
 "I": [("e5h", "Ember", ["ominous", "short"]), ("f1", "Farmer", ["pastoral", "fjord morning", "solo lyre melody", "calm"]), ("e1", "Jarl", ["stern", "low drone", "restrained"]),
       ("f3", "Poor villages", ["light wry tone", "plucked lyre"]), ("f4", "Open sea", ["uncertain", "wind-like drone", "searching"]), ("f5", "Sun stone", ["wonder", "shimmering", "discovery"]),
       ("e3", "Floki's ship", ["craft", "rhythmic woodwork pulse", "playful"]), ("f6", "Departure", ["adventure", "rowing rhythm frame drum", "building"]),
       ("e4", "Storm", ["dramatic", "pounding drums", "tension", "low strings"]), ("f7", "Land sighted", ["awe", "release", "wide"]), ("f8", "Monastery", ["eerie calm", "hollow drones"]),
       ("e5r", "Raid", ["brutal", "war drums", "short burst"]), ("e6", "Athelstan", ["quiet", "curious", "soft lyre", "rain mood"]),
       ("K0", "Jarl's greed", ["tension", "dark low drone", "slow menace"]), ("f9", "Challenge", ["rising tension", "drum heartbeat", "duel"]),
       ("f10", "Fall", ["impact", "sudden silence then low swell"]), ("e8", "New Jarl", ["triumphant", "proud", "horn-like drones", "warm resolution"])],
 "II": [("K1", "Bargain", ["neutral", "low pulse"]), ("d1", "Plague", ["grief", "sparse", "fragile lyre", "mourning"]), ("d3", "Pyre", ["sorrowful", "slow", "ritual drum soft"]),
        ("K2", "Betrayal", ["dark tension", "brooding"]), ("d4", "Brother", ["conflict", "war drums distant", "heavy"]), ("d5", "Mercy", ["anguish", "release"]),
        ("K3", "Spared", ["uneasy calm"]), ("veda_1", "Aslaug", ["mysterious", "seductive soft drone"]), ("veda_3", "Farewell", ["heartbreak", "slow lament", "tagelharpa solo"]),
        ("K4", "Four years", ["time passing", "steady", "growing power"]), ("ivar_1", "Ivar", ["tender", "fragile", "aching", "very soft"]), ("ivar_4", "Little hand", ["heartbreaking", "almost silent", "single sustained notes"]),
        ("ivar_5", "Prophecy", ["ominous", "low swell", "fate"]), ("K5", "Horik", ["intrigue", "plucked tension"]), ("d6", "Lies", ["cunning", "dark pulse"]), ("d8", "King", ["triumphant", "regal", "full drums", "horn-like swell"])],
 "III": [("K6", "Wessex", ["new land", "stately"]), ("a1", "Friendship", ["warm", "gentle lyre", "two voices intertwining"]), ("a2", "Light in water", ["luminous", "spiritual", "soft"]),
         ("b1", "Floki", ["threat", "dark drone", "tension rising"]), ("b3", "Death", ["stark", "single low hit then silence-like drone"]), ("b4", "Aftermath", ["grief", "shock", "quiet"]),
         ("yas", "Burial", ["deep mourning", "slow lament", "tagelharpa", "rain mood", "reverent"]), ("c1", "Pause", ["soft reflective", "gentle ending"])],
 "IV": [("K7", "Paris", ["anticipation", "curious"]), ("p15b", "Walls", ["epic", "massive", "war drums", "siege"]), ("p15d", "Wounded", ["pain", "slowing", "low"]),
        ("p16a", "Ruse", ["cunning", "sly plucked lyre", "playful tension"]), ("p16b1", "False death", ["solemn fake funeral", "hollow"]), ("p1c", "Rise", ["sudden surge", "drums kick in"]),
        ("p16e", "Paris falls", ["triumphant battle", "full war drums", "horns"]), ("p17", "I know", ["cold", "quiet", "betrayal known"]), ("p18a", "Drug", ["decay", "woozy drone", "unsettling"]),
        ("K8", "Rollo", ["bitter", "brooding"]), ("p18c", "Return", ["dark", "heavy", "defeat looming"])],
 "V": [("k19a", "Return", ["desolate", "cold wind-like drone", "lonely"]), ("k19c", "No heirs", ["bitter", "sparse"]), ("k19d", "Ivar", ["faint warmth", "fragile"]),
       ("k20a", "The tree", ["despair", "very sparse", "low sustained"]), ("k20b", "Ravens", ["fate", "eerie", "gods watching"]), ("k21a", "Last voyage", ["grim resolve"]),
       ("k21b", "Storm", ["chaos", "pounding drums", "dark"])],
 "VI": [("k22a", "Ecbert", ["old friends", "melancholic", "warm and sad"]), ("k23a", "The plan", ["secret", "quiet resolve"]), ("k24", "The cross", ["tender", "legacy", "soft"]),
        ("k25a", "Cage", ["grim", "slow march", "dark"]), ("k26a", "Ella", ["defiance", "tense drone"]), ("k26b", "The pit", ["dread", "very low", "sparse"]),
        ("k26c", "They will come", ["defiant", "rising", "fate"]), ("k26d", "Two ravens", ["release", "transcendent", "swelling drones"]),
        ("f1", "Farmer to king", ["epic reflective", "full", "lyre theme returns", "horn-like swell"]), ("k27c", "Question", ["open", "resolve", "gentle fade ending"])]}

def starts(b):
    s = {}
    for p in Z[b]["parts"]:
        s.setdefault(p["name"], p["offset"])
        for k, t0, d, fk in p["shots"]: s.setdefault(fk, p["offset"] + t0)
    return s

def plan(b):
    S = starts(b); tot = Z[b]["dur"]; P = PLAN[b]; secs = []
    for i, (k, nm, st) in enumerate(P):
        a = S[k] if i else 0.0; e = S[P[i + 1][0]] if i + 1 < len(P) else tot
        secs.append([nm, st, e - a])
    m = []   # 4 sn'den kısa bölümleri öncekine kat
    for s in secs:
        if m and s[2] < 4.0: m[-1][2] += s[2]
        else: m.append(s)
    if len(m) > 1 and m[0][2] < 4.0: m[1][2] += m[0][2]; m.pop(0)
    return {"positive_global_styles": GLOBAL, "negative_global_styles": NEG,
            "sections": [{"section_name": n, "positive_local_styles": st, "negative_local_styles": [], "duration_ms": int(round(d * 1000)), "lines": []} for n, st, d in m]}

def compose(b):
    cp = plan(b); json.dump(cp, open(f"{H}/muzik/{b}_plan.json", "w"), indent=1)
    r = requests.post("https://api.elevenlabs.io/v1/music?output_format=mp3_44100_192", headers={"xi-api-key": KEY},
                      json={"composition_plan": cp, "respect_sections_durations": True}, timeout=600)
    if r.status_code != 200: raise RuntimeError(b + " " + r.text[:400])
    mp = f"{H}/muzik/{b}.mp3"; open(mp, "wb").write(r.content)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", mp, "-ar", "48000", "-ac", "2", f"{H}/muzik/{b}.wav"], check=True)
    d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", mp], capture_output=True, text=True).stdout)
    return b, round(d, 2), round(Z[b]["dur"], 2), len(cp["sections"])

if __name__ == "__main__":
    bs = sys.argv[1:] or list(PLAN)
    if bs == ["plan"]:
        for b in PLAN: p = plan(b); print(b, len(p["sections"]), [s["duration_ms"] for s in p["sections"]])
        sys.exit()
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(2) as ex:
        for x in ex.map(compose, bs): print(*x, flush=True)
