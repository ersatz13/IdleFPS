import json
import random
import time
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path

# Core configuration for saves and attribute setup.
DEFAULT_SAVE_FILE = Path("user_save.json")
ATTRIBUTE_POINTS = 30
ATTRIBUTE_MAX = 10
ATTRIBUTES = (
    "Target Acquisition",
    "Movement",
    "Map Knowledge",
    "Clairvoyance",
    "Adaptability",
)
MAP_POOL = (
    "Terminal",
    "Crash",
    "Firing Range",
    "Raid",
    "Rust",
    "SixFlags",
    "Toys-R-Us",
    "Subway",
)
ENEMY_POOL = ("Rusher", "Camper", "BK randy")
WEAPON_POOL = ("Ak-47", "M4A1", "MP5", "FAMAS", "G36C", "P90")
CAMO_UNLOCKS = [
    (10, "Forest"),
    (25, "Digital"),
    (40, "Desert"),
    (55, "Arctic"),
    (70, "Urban"),
    (85, "Jungle"),
    (100, "Tiger"),
    (120, "Marble"),
    (140, "Nebula"),
    (160, "Crimson"),
    (180, "Obsidian"),
    (200, "Gold"),
    (230, "Platinum"),
    (260, "Diamond"),
]
MULTIKILL_BONUS = {
    2: ("double_kills", 20),
    3: ("triple_kills", 40),
    4: ("quad_kills", 60),
    5: ("monster_kills", 80),
    6: ("team_kills", 100),
}
PLAYER_RANKS = (
    "Recruit",
    "Cadet",
    "Private",
    "Corporal",
    "Sergeant",
    "Staff Sergeant",
    "Master Sergeant",
    "Sergeant Major",
    "Warrant Officer",
    "Lieutenant",
    "Captain",
    "Major",
    "Lieutenant Colonel",
    "Colonel",
    "Brigadier",
    "General",
    "Field Commander",
    "Commander",
    "Chief",
)
BASE_MAX_LEVEL = 55
PRESTIGE_MAX = 12
MASTER_MAX_LEVEL = 1000
CAMO_COLORS = {
    "None": "#3a3a3a",
    "Forest": "#2e5b2e",
    "Digital": "#3b4b5a",
    "Desert": "#b49a6a",
    "Arctic": "#d7e5f0",
    "Urban": "#6a6a6a",
    "Jungle": "#2f6b3f",
    "Tiger": "#b56b2a",
    "Marble": "#a9b0b8",
    "Nebula": "#5a4a7a",
    "Crimson": "#8e2d2d",
    "Obsidian": "#1a1a1a",
    "Gold": "#d4af37",
    "Platinum": "#c0c0c0",
    "Diamond": "#7fc7ff",
}
ACHIEVEMENTS = [
    ("kills_100", "Warpath I", "kills", 100, 50, "Reach 100 total kills."),
    ("kills_1000", "Warpath II", "kills", 1000, 200, "Reach 1,000 total kills."),
    ("kills_10000", "Apex Predator", "kills", 10000, 800, "Reach 10,000 total kills."),
    ("deaths_1000", "Walking Target", "deaths", 1000, 50, "Reach 1,000 total deaths."),
    ("deaths_5000", "Iron Will", "deaths", 5000, 200, "Reach 5,000 total deaths."),
    ("headshots_250", "Sharpshooter", "headshots", 250, 100, "Reach 250 total headshots."),
    ("headshots_2500", "Deadeye", "headshots", 2500, 400, "Reach 2,500 total headshots."),
    ("headshots_10000", "Surgical", "headshots", 10000, 1200, "Reach 10,000 total headshots."),
    ("streak_10", "Streaker", "longest_streak", 10, 150, "Achieve a 10 kill streak."),
    ("streak_25", "Unstoppable", "longest_streak", 25, 500, "Achieve a 25 kill streak."),
    ("multi_50", "Multi-kill Maniac", "multi_kills", 50, 250, "Earn 50 multikills total."),
    ("xp_10000", "Rising Star", "xp_total", 10000, 200, "Earn 10,000 total XP."),
    ("xp_100000", "Elite Operative", "xp_total", 100000, 800, "Earn 100,000 total XP."),
    ("xp_1000000", "Legend", "xp_total", 1000000, 3000, "Earn 1,000,000 total XP."),
    ("uap_25", "Recon Specialist", "uap_calls", 25, 200, "Call in 25 UAPs."),
    ("airstrike_25", "Fire Support", "airstrike_calls", 25, 200, "Call in 25 airstrikes."),
    ("heli_25", "Air Cav", "helicopter_calls", 25, 300, "Call in 25 helicopters."),
    ("nuke_1", "Nuclear Option", "nuke_victories", 1, 500, "Earn 1 nuclear victory."),
    ("nuke_10", "Fallout", "nuke_victories", 10, 2000, "Earn 10 nuclear victories."),
    ("matches_100", "Career Soldier", "games_played", 100, 300, "Play 100 matches."),
    ("matches_1000", "Lifelong Warrior", "games_played", 1000, 1500, "Play 1,000 matches."),
    ("playtime_24h", "Veteran", "play_time_seconds", 24 * 3600, 400, "Accumulate 24 hours played."),
]
RANK_COLORS = {
    "Recruit": "#5b5b5b",
    "Cadet": "#4a6a84",
    "Private": "#3b6b3b",
    "Corporal": "#4d7a4d",
    "Sergeant": "#7a6a3b",
    "Staff Sergeant": "#8a6b2e",
    "Master Sergeant": "#9a6b2e",
    "Sergeant Major": "#a8742f",
    "Warrant Officer": "#8a8a8a",
    "Lieutenant": "#3b4d7a",
    "Captain": "#4b3b7a",
    "Major": "#6b3b7a",
    "Lieutenant Colonel": "#7a3b5b",
    "Colonel": "#7a3b3b",
    "Brigadier": "#8a3b3b",
    "General": "#9a3b3b",
    "Field Commander": "#b04b4b",
    "Commander": "#c06b3b",
    "Chief": "#d4af37",
}


def sanitize_filename(name):
    # Keep save filenames safe and predictable on disk.
    safe = "".join(ch for ch in name if ch.isalnum() or ch in (" ", "-", "_")).strip()
    return safe or "player"


def save_profile_data(data, save_path):
    # Write the full profile payload to a specific path.
    if "player" in data:
        data["player"]["last_saved"] = int(time.time())
    save_path.write_text(json.dumps(data, indent=2) + "\n", encoding="ascii")


def save_player_profile(profile):
    # Persist the player profile to a gamertag-named JSON file.
    payload = {
        "version": "0.0.0.1",
        "player": profile,
    }
    gamertag = profile.get("gamertag", "")
    file_stem = sanitize_filename(gamertag)
    save_path = Path(f"{file_stem}.json")
    save_profile_data(payload, save_path)


def remaining_points(values):
    # Compute points still available from the fixed budget.
    return ATTRIBUTE_POINTS - sum(values)


def format_duration(total_seconds):
    # Display elapsed time in hours, minutes, and seconds.
    total_seconds = max(0, int(total_seconds))
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def level_threshold(level):
    # XP needed to advance from the given level.
    return 100 + (level - 1) * 50


def level_progress(xp_total):
    # Compute current level and progress toward the next level.
    level = 1
    remaining = max(0, int(xp_total))
    threshold = level_threshold(level)
    while remaining >= threshold:
        remaining -= threshold
        level += 1
        threshold = level_threshold(level)
    return level, remaining, threshold


def level_progress_with_cap(xp_total, level_cap):
    # Compute level progress with a maximum level cap.
    level = 1
    remaining = max(0, int(xp_total))
    threshold = level_threshold(level)
    while remaining >= threshold and level < level_cap:
        remaining -= threshold
        level += 1
        threshold = level_threshold(level)
    return level, remaining, threshold


def rank_for_level(level):
    # Map each rank name to a 3-level span.
    index = max(0, min((int(level) - 1) // 3, len(PLAYER_RANKS) - 1))
    return PLAYER_RANKS[index]


def apply_xp_and_progress(stats, xp_gain):
    # Apply XP and update level/prestige/master state.
    xp = int(stats.get("xp", 0)) + int(xp_gain)
    prestige = int(stats.get("prestige", 0))
    prestige_unlocked = bool(stats.get("prestige_unlocked", False))
    master = bool(stats.get("master_prestige", False))
    master_level = int(stats.get("master_level", 1))

    while True:
        if master:
            level, remaining, threshold = level_progress_with_cap(xp, MASTER_MAX_LEVEL)
            master_level = level
            xp = remaining
            break

        level, remaining, threshold = level_progress_with_cap(xp, BASE_MAX_LEVEL)
        if not prestige_unlocked:
            if level < BASE_MAX_LEVEL or remaining < threshold:
                stats["level"] = level
                xp = remaining
                break
            prestige_unlocked = True
            prestige = 1
            stats["prestige"] = prestige
            stats["level"] = 1
            xp = remaining - threshold
            continue

        if level < BASE_MAX_LEVEL:
            stats["level"] = level
            xp = remaining
            break

        if remaining >= threshold:
            remaining -= threshold
            if prestige < PRESTIGE_MAX:
                prestige += 1
                stats["prestige"] = prestige
                stats["level"] = 1
                xp = remaining
                continue
            master = True
            stats["master_prestige"] = True
            stats["master_level"] = 1
            xp = remaining
            continue

        stats["level"] = level
        xp = remaining
        break

    stats["xp"] = xp
    stats["prestige"] = prestige
    stats["prestige_unlocked"] = prestige_unlocked
    stats["master_prestige"] = master
    stats["master_level"] = master_level


def progress_state(stats, xp_gain=0):
    # Preview progress without mutating stats.
    xp = int(stats.get("xp", 0)) + int(xp_gain)
    prestige = int(stats.get("prestige", 0))
    prestige_unlocked = bool(stats.get("prestige_unlocked", False))
    master = bool(stats.get("master_prestige", False))
    master_level = int(stats.get("master_level", 1))

    while True:
        if master:
            level, remaining, threshold = level_progress_with_cap(xp, MASTER_MAX_LEVEL)
            master_level = level
            return {
                "level": level,
                "xp_into": remaining,
                "xp_needed": threshold,
                "prestige": prestige,
                "master": True,
                "master_level": master_level,
            }

        level, remaining, threshold = level_progress_with_cap(xp, BASE_MAX_LEVEL)
        if not prestige_unlocked:
            if level < BASE_MAX_LEVEL or remaining < threshold:
                return {
                    "level": level,
                    "xp_into": remaining,
                    "xp_needed": threshold,
                    "prestige": prestige,
                    "master": False,
                    "master_level": master_level,
                    "prestige_unlocked": False,
                }
            prestige_unlocked = True
            prestige = 1
            xp = remaining - threshold
            continue

        if level < BASE_MAX_LEVEL:
            return {
                "level": level,
                "xp_into": remaining,
                "xp_needed": threshold,
                "prestige": prestige,
                "master": False,
                "master_level": master_level,
                "prestige_unlocked": prestige_unlocked,
            }

        if remaining >= threshold:
            remaining -= threshold
            if prestige < PRESTIGE_MAX:
                prestige += 1
                xp = remaining
                continue
            master = True
            xp = remaining
            continue

        return {
            "level": level,
            "xp_into": remaining,
            "xp_needed": threshold,
            "prestige": prestige,
            "master": False,
            "master_level": master_level,
            "prestige_unlocked": prestige_unlocked,
        }


def rank_display_from_progress(progress):
    # Compose rank label based on a progress snapshot.
    if progress.get("master"):
        return f"Master of War {int(progress.get('master_level', 1))}"
    prestige = int(progress.get("prestige", 0))
    prefix = f"Prestige {prestige} " if prestige > 0 else ""
    return f"{prefix}{rank_for_level(progress.get('level', 1))}"


def camo_color(name):
    # Resolve a camo name to a display color.
    return CAMO_COLORS.get(name, CAMO_COLORS["None"])


def rank_color(name):
    # Resolve a rank name to a display color.
    return RANK_COLORS.get(name, "#5b5b5b")


def get_total_play_time(timer_state):
    # Combine stored elapsed time with current session runtime.
    elapsed = timer_state.get("elapsed", 0)
    if timer_state.get("running"):
        elapsed += int(time.monotonic() - timer_state.get("start", time.monotonic()))
    return elapsed


def calculate_rates(attributes):
    # Derive kills/deaths rates from player attributes.
    total = sum(attributes.values())
    max_total = ATTRIBUTE_MAX * len(ATTRIBUTES)
    skill = total / max_total if max_total else 0.0
    kills_per_min = 2 + 7 * skill
    deaths_per_min = 6 - 5 * skill
    return kills_per_min / 60.0, deaths_per_min / 60.0


def compute_attribute_effects(attributes, options=None):
    # Translate attributes into explicit gameplay effects, with optional overrides.
    target = int(attributes.get("Target Acquisition", 0))
    movement = int(attributes.get("Movement", 0))
    clairvoyance = int(attributes.get("Clairvoyance", 0))
    adaptability = int(attributes.get("Adaptability", 0))

    accuracy = 0.6 + 0.04 * target  # 60% - 100%
    movement_speed = 0.8 + 0.04 * movement  # 0.8x - 1.2x
    respawn_seconds = 3.5 - 0.15 * adaptability  # 3.5s - 2.0s
    headshot_rate = 0.12 + 0.01 * clairvoyance  # 12% - 22%

    effects = {
        "accuracy": accuracy,
        "movement_speed": movement_speed,
        "respawn_seconds": respawn_seconds,
        "headshot_rate": headshot_rate,
    }
    if options:
        effects["accuracy"] = float(options.get("accuracy", effects["accuracy"]))
        effects["movement_speed"] = float(options.get("movement_speed", effects["movement_speed"]))
        effects["respawn_seconds"] = float(options.get("respawn_seconds", effects["respawn_seconds"]))
        effects["headshot_rate"] = float(options.get("headshot_rate", effects["headshot_rate"]))
    return effects


def compute_xp_gain(kills, headshots, completed):
    # Reward XP for combat performance and match completion.
    xp = kills * 10 + headshots * 5
    if completed:
        xp += 50
    return xp


def achievement_value(profile, key):
    # Resolve a stat value for achievements.
    stats = ensure_stats(profile)
    if key == "multi_kills":
        return (
            int(stats.get("double_kills", 0))
            + int(stats.get("triple_kills", 0))
            + int(stats.get("quad_kills", 0))
            + int(stats.get("monster_kills", 0))
            + int(stats.get("team_kills", 0))
        )
    if key == "xp_total":
        return int(stats.get("xp", 0))
    if key == "play_time_seconds":
        return int(profile["player"].get("play_time_seconds", 0))
    return int(stats.get(key, 0))


def check_achievements(profile):
    # Award new achievements and return bonus XP gained.
    stats = ensure_stats(profile)
    earned = stats.setdefault("achievements", {})
    bonus_xp = 0
    for ach_id, name, key, threshold, reward_xp, description in ACHIEVEMENTS:
        value = achievement_value(profile, key)
        if not earned.get(ach_id) and value >= threshold:
            earned[ach_id] = True
            bonus_xp += reward_xp
    return bonus_xp


def ensure_stats(profile):
    # Ensure the profile stats dict contains required keys.
    return profile["player"].setdefault(
        "stats",
        {
            "games_played": 0,
            "game_modes_played": {},
            "maps_played": {},
            "kills": 0,
            "deaths": 0,
            "longest_kill_streak": 0,
            "headshots": 0,
            "xp": 0,
            "level": 1,
            "prestige_unlocked": False,
            "prestige": 0,
            "master_prestige": False,
            "master_level": 1,
            "weapons": {},
            "uap_calls": 0,
            "airstrike_calls": 0,
            "helicopter_calls": 0,
            "airstrike_kills": 0,
            "helicopter_kills": 0,
            "nuke_victories": 0,
            "double_kills": 0,
            "triple_kills": 0,
            "quad_kills": 0,
            "monster_kills": 0,
            "team_kills": 0,
            "achievements": {},
        },
    )


def apply_offline_progress(profile, offline_seconds):
    # Simulate offline gains based on average match cadence.
    if offline_seconds <= 0:
        return
    stats = ensure_stats(profile)
    attributes = profile["player"].get("attributes", {})
    options = profile["player"].get("options", {})
    defaults = profile["player"].get("defaults", {})
    weapon = defaults.get("weapon", WEAPON_POOL[0])
    mode = defaults.get("game_mode", "Team death match")

    avg_match_seconds = 10.5 * 60
    avg_lobby_seconds = 23.5
    cycle_seconds = avg_match_seconds + avg_lobby_seconds

    full_cycles = int(offline_seconds // cycle_seconds)
    remainder = offline_seconds - full_cycles * cycle_seconds
    completed_matches = full_cycles + (1 if remainder >= avg_match_seconds else 0)
    match_seconds = full_cycles * avg_match_seconds + min(remainder, avg_match_seconds)

    kills_rate, deaths_rate = calculate_rates(attributes)
    effects = compute_attribute_effects(attributes, options)
    kills_rate *= effects["accuracy"]
    deaths_rate *= max(0.5, 1.1 - (effects["movement_speed"] - 0.8))
    headshot_rate = effects["headshot_rate"]

    kills = int(match_seconds * kills_rate)
    deaths = int(match_seconds * deaths_rate)
    headshots = int(kills * headshot_rate)

    # Simulate streak rewards from offline matches.
    uap_calls = 0
    airstrike_calls = 0
    helicopter_calls = 0
    nuke_victories = 0
    double_kills = 0
    triple_kills = 0
    quad_kills = 0
    monster_kills = 0
    team_kills = 0
    airstrike_kills = 0
    helicopter_kills = 0
    nuke_kills = 0
    if completed_matches > 0:
        kills_per_match = kills / completed_matches
        for _ in range(completed_matches):
            if kills_per_match >= 3:
                uap_calls += 1
            if kills_per_match >= 5:
                airstrike_calls += 1
                airstrike_kills += random.randint(0, 6)
            if kills_per_match >= 7:
                helicopter_calls += 1
                helicopter_kills += random.randint(0, 22)
            if kills_per_match >= 25:
                nuke_victories += 1
                nuke_kills += 6

            if kills_per_match >= 2:
                double_kills += int(kills_per_match // 2)
            if kills_per_match >= 3:
                triple_kills += int(kills_per_match // 3)
            if kills_per_match >= 4:
                quad_kills += int(kills_per_match // 4)
            if kills_per_match >= 5:
                monster_kills += int(kills_per_match // 5)
            if kills_per_match >= 6:
                team_kills += int(kills_per_match // 6)

    kills += airstrike_kills + helicopter_kills + nuke_kills

    stats["kills"] = int(stats.get("kills", 0)) + kills
    stats["deaths"] = int(stats.get("deaths", 0)) + deaths
    stats["headshots"] = int(stats.get("headshots", 0)) + headshots
    stats["games_played"] = int(stats.get("games_played", 0)) + completed_matches

    modes = stats.setdefault("game_modes_played", {})
    modes[mode] = int(modes.get(mode, 0)) + completed_matches

    maps = stats.setdefault("maps_played", {})
    for _ in range(completed_matches):
        name = random.choice(MAP_POOL)
        maps[name] = int(maps.get(name, 0)) + 1

    stats["uap_calls"] = int(stats.get("uap_calls", 0)) + uap_calls
    stats["airstrike_calls"] = int(stats.get("airstrike_calls", 0)) + airstrike_calls
    stats["helicopter_calls"] = int(stats.get("helicopter_calls", 0)) + helicopter_calls
    stats["airstrike_kills"] = int(stats.get("airstrike_kills", 0)) + airstrike_kills
    stats["helicopter_kills"] = int(stats.get("helicopter_kills", 0)) + helicopter_kills
    stats["nuke_victories"] = int(stats.get("nuke_victories", 0)) + nuke_victories
    stats["double_kills"] = int(stats.get("double_kills", 0)) + double_kills
    stats["triple_kills"] = int(stats.get("triple_kills", 0)) + triple_kills
    stats["quad_kills"] = int(stats.get("quad_kills", 0)) + quad_kills
    stats["monster_kills"] = int(stats.get("monster_kills", 0)) + monster_kills
    stats["team_kills"] = int(stats.get("team_kills", 0)) + team_kills

    xp_gain = kills * 10 + headshots * 5 + completed_matches * 50
    apply_xp_and_progress(stats, xp_gain)
    bonus = check_achievements(profile)
    if bonus:
        apply_xp_and_progress(stats, bonus)

    weapons = stats.setdefault("weapons", {})
    weapon_stats = weapons.setdefault(weapon, {"xp": 0, "level": 1, "headshots": 0, "camo": "None"})
    weapon_stats["xp"] = int(weapon_stats.get("xp", 0)) + xp_gain + headshots * 5
    weapon_stats["level"] = level_progress(weapon_stats["xp"])[0]
    weapon_stats["headshots"] = int(weapon_stats.get("headshots", 0)) + headshots
    weapon_stats["camo"] = get_camo_for_headshots(weapon_stats["headshots"])

    profile["player"]["play_time_seconds"] = int(profile["player"].get("play_time_seconds", 0)) + int(offline_seconds)


def add_kill_death_stats(loaded_profile, kills, deaths, headshots=0):
    # Accumulate kills, deaths, and headshots into the profile stats.
    stats = ensure_stats(loaded_profile)
    stats["kills"] = int(stats.get("kills", 0)) + int(kills)
    stats["deaths"] = int(stats.get("deaths", 0)) + int(deaths)
    stats["headshots"] = int(stats.get("headshots", 0)) + int(headshots)


def award_xp(loaded_profile, xp_gain):
    # Apply XP gain and update the stored level.
    stats = ensure_stats(loaded_profile)
    apply_xp_and_progress(stats, xp_gain)


def get_camo_for_headshots(headshot_count):
    # Resolve the highest camo unlocked for the given headshot count.
    camo = "None"
    for requirement, name in CAMO_UNLOCKS:
        if headshot_count >= requirement:
            camo = name
    return camo


def award_weapon_xp(loaded_profile, weapon_name, xp_gain, headshots=0):
    # Track per-weapon progression and camo unlocks.
    stats = loaded_profile["player"].setdefault("stats", {})
    weapons = stats.setdefault("weapons", {})
    weapon = weapons.setdefault(weapon_name, {"xp": 0, "level": 1, "headshots": 0, "camo": "None"})
    weapon["xp"] = int(weapon.get("xp", 0)) + int(xp_gain)
    weapon["level"] = level_progress(weapon["xp"])[0]
    weapon["headshots"] = int(weapon.get("headshots", 0)) + int(headshots)
    weapon["camo"] = get_camo_for_headshots(weapon["headshots"])


def trigger_nuke(session_state, stats, now, schedule_end, force=False):
    # Trigger a nuclear victory and end the match shortly after.
    if "nuke" in session_state.get("reward_flags", set()) and not force and not session_state.get("pending_nuke"):
        return
    session_state["streak_rewards"]["nuke"] = now
    session_state["reward_flags"].add("nuke")
    session_state["nuke_until"] = now + 3
    session_state["kills"] += 6
    session_state["xp_bonus"] += 6 * 10
    session_state["end_time"] = session_state["nuke_until"]
    schedule_end(int((session_state["nuke_until"] - now) * 1000))


def close_nuke_prompt(session_state):
    # Close the nuke prompt if it's open.
    prompt = session_state.get("nuke_prompt")
    if prompt:
        prompt.destroy()
    session_state["nuke_prompt"] = None


def show_nuke_prompt(root, session_state, stats, schedule_end):
    # Prompt the player to accept a nuclear victory without pausing the match.
    if session_state.get("nuke_prompt"):
        return
    prompt = tk.Toplevel(root)
    prompt.title("Nuclear Victory")
    prompt.resizable(False, False)

    label = tk.Label(
        prompt,
        text="Nuclear victory ready. Accept and end the match?",
        font=("Segoe UI", 10),
    )
    label.pack(padx=20, pady=(16, 10))

    buttons = tk.Frame(prompt)
    buttons.pack(pady=(0, 16))

    def accept():
        close_nuke_prompt(session_state)
        trigger_nuke(session_state, stats, time.monotonic(), schedule_end, force=True)
        session_state["pending_nuke"] = False

    def decline():
        close_nuke_prompt(session_state)
        session_state["pending_nuke"] = False

    accept_button = tk.Button(buttons, text="Accept", width=10, command=accept)
    accept_button.pack(side="left", padx=6)

    decline_button = tk.Button(buttons, text="Decline", width=10, command=decline)
    decline_button.pack(side="left", padx=6)

    def on_close():
        decline()

    prompt.protocol("WM_DELETE_WINDOW", on_close)
    session_state["nuke_prompt"] = prompt


def start_doomguy_animation(root, session_state):
    # Create a small animated scene while a game is running.
    if session_state.get("anim_window"):
        return
    window = tk.Toplevel(root)
    window.title("Match View")
    window.resizable(False, False)

    canvas = tk.Canvas(window, width=320, height=200, bg="#101820", highlightthickness=0)
    canvas.pack()

    session_state["anim_window"] = window
    session_state["anim_canvas"] = canvas
    session_state["anim_frame"] = 0

    def on_close():
        anim_after_id = session_state.get("anim_after_id")
        if anim_after_id:
            root.after_cancel(anim_after_id)
            session_state["anim_after_id"] = None
        window.destroy()
        session_state["anim_window"] = None
        session_state["anim_canvas"] = None
        session_state["anim_frame"] = 0

    window.protocol("WM_DELETE_WINDOW", on_close)

    def draw_scene():
        if session_state.get("phase") != "playing" or session_state.get("anim_canvas") is None:
            return
        frame = session_state.get("anim_frame", 0)
        canvas.delete("all")

        # Simple pseudo-3D corridor.
        canvas.create_rectangle(0, 0, 320, 80, fill="#1a2636", outline="")
        canvas.create_polygon(0, 80, 320, 80, 260, 200, 60, 200, fill="#0d131a", outline="")
        for i in range(6):
            offset = (frame * 6 + i * 40) % 240
            left = 60 + offset * 0.3
            right = 260 - offset * 0.3
            y = 80 + offset * 0.5
            canvas.create_line(left, y, right, y, fill="#243447")

        # Enemies to pick from (always visible).
        positions = [(60, 130), (160, 130), (260, 130), (80, 160), (160, 170), (240, 160)]
        enemies = session_state.get("encounter_enemies", [])
        last_kill_time = session_state.get("last_kill_time", 0)
        flash_hit = time.monotonic() - last_kill_time < 0.6
        hit_indices = set(session_state.get("last_kill_indices", [])) if flash_hit else set()

        for idx, name in enumerate(enemies):
            ex, ey = positions[idx % len(positions)]
            canvas.create_oval(ex - 10, ey - 10, ex + 10, ey + 10, fill="#8b2d2d", outline="")
            if idx in hit_indices:
                canvas.create_oval(ex - 16, ey - 16, ex + 16, ey + 16, outline="#f0d24b", width=2)
                canvas.create_line(ex - 6, ey, ex - 2, ey, fill="#f0d24b", width=2)
                canvas.create_line(ex + 2, ey, ex + 6, ey, fill="#f0d24b", width=2)
                canvas.create_line(ex, ey - 6, ex, ey - 2, fill="#f0d24b", width=2)
                canvas.create_line(ex, ey + 2, ex, ey + 6, fill="#f0d24b", width=2)
            canvas.create_text(ex, ey + 16, text=name, fill="#c0c0c0", font=("Segoe UI", 7))

        # Doomguy stick figure with a simple walk cycle.
        respawn_until = session_state.get("respawn_until", 0)
        if time.monotonic() >= respawn_until:
            bob = 2 if frame % 10 < 5 else 0
            x = 160 + (frame % 40 - 20) * 0.6
            y = 120 + bob
            canvas.create_oval(x - 8, y - 18, x + 8, y - 2, fill="#c89b6d", outline="")
            canvas.create_line(x, y - 2, x, y + 20, fill="#c95738", width=3)
            leg_offset = 6 if frame % 10 < 5 else -6
            canvas.create_line(x, y + 20, x - 6, y + 36 + leg_offset, fill="#7b3f2a", width=3)
            canvas.create_line(x, y + 20, x + 6, y + 36 - leg_offset, fill="#7b3f2a", width=3)
            canvas.create_line(x - 10, y + 6, x + 10, y + 10, fill="#c95738", width=3)

        # Kill feedback.
        if time.monotonic() - last_kill_time < 1.0:
            kill_count = session_state.get("last_kill_count", 1)
            label = "Eliminated enemy!" if kill_count == 1 else f"Eliminated {kill_count} enemies!"
            canvas.create_text(160, 20, text=label, fill="#f0d24b", font=("Segoe UI", 10))

        # Death/respawn feedback.
        if time.monotonic() < respawn_until:
            seconds_left = max(1, int(respawn_until - time.monotonic()))
            canvas.create_text(
                160,
                40,
                text=f"Respawning in {seconds_left}...",
                fill="#ff6b6b",
                font=("Segoe UI", 10),
            )

        # Kill feed.
        feed = session_state.get("kill_feed", [])
        now = time.monotonic()
        feed = [(t, text) for t, text in feed if now - t < 6]
        session_state["kill_feed"] = feed
        for idx, (_, text) in enumerate(feed[-4:]):
            canvas.create_text(10, 12 + idx * 12, text=text, fill="#d5e3f0", font=("Segoe UI", 8), anchor="w")

        # Streak rewards visuals.
        now = time.monotonic()
        rewards = session_state.get("streak_rewards", {})

        nuke_until = session_state.get("nuke_until", 0)
        if now < nuke_until:
            radius = 30 + (1 - (nuke_until - now) / 3.0) * 120
            canvas.create_oval(160 - radius, 100 - radius, 160 + radius, 100 + radius, fill="#f4b33a", outline="")
            canvas.create_oval(
                160 - radius * 0.7,
                100 - radius * 0.7,
                160 + radius * 0.7,
                100 + radius * 0.7,
                fill="#ff6b3a",
                outline="",
            )
            canvas.create_text(160, 100, text="NUCLEAR VICTORY", fill="#ffffff", font=("Segoe UI", 12))

        uap_start = rewards.get("uap")
        if uap_start:
            elapsed = now - uap_start
            if elapsed <= 3.0:
                pulse = int(elapsed // 1.0)
                progress = (elapsed % 1.0) / 1.0
                radius = 20 + progress * 90
                alpha = int(255 * (1 - progress))
                color = f"#{alpha:02x}ff{alpha:02x}"
                canvas.create_oval(160 - radius, 100 - radius, 160 + radius, 100 + radius, outline=color, width=2)
                canvas.create_text(160, 70, text="UAP Sweep", fill="#9ad1ff", font=("Segoe UI", 9))
            else:
                session_state["streak_rewards"]["uap"] = None

        air_start = rewards.get("airstrike")
        if air_start:
            elapsed = now - air_start
            if elapsed <= 3.0:
                x = -40 + (elapsed / 3.0) * 400
                y = 30
                canvas.create_polygon(
                    x,
                    y,
                    x + 30,
                    y + 6,
                    x,
                    y + 12,
                    fill="#cfd8e3",
                    outline="",
                )
                canvas.create_text(160, 55, text="Airstrike inbound", fill="#f4c542", font=("Segoe UI", 9))
            else:
                session_state["streak_rewards"]["airstrike"] = None

        heli_start = rewards.get("helicopter")
        if heli_start:
            elapsed = now - heli_start
            if elapsed <= 8.0:
                x = 30 + (elapsed / 8.0) * 240
                y = 40
                canvas.create_rectangle(x, y, x + 40, y + 14, fill="#6b8c8e", outline="")
                canvas.create_rectangle(x + 10, y - 8, x + 30, y, fill="#6b8c8e", outline="")
                rotor_offset = 6 if int(elapsed * 10) % 2 == 0 else -6
                canvas.create_line(x + 20 - 14, y - 10, x + 20 + 14, y - 10, fill="#d0d7de", width=2)
                canvas.create_line(x + 20, y - 10 - rotor_offset, x + 20, y - 10 + rotor_offset, fill="#d0d7de", width=2)
                canvas.create_text(160, 75, text="Helicopter support", fill="#8ef5b3", font=("Segoe UI", 9))
            else:
                session_state["streak_rewards"]["helicopter"] = None

        session_state["anim_frame"] = frame + 1
        session_state["anim_after_id"] = root.after(80, draw_scene)

    draw_scene()


def stop_game_session(root, session_state, status_var, timer_var, map_var, kd_var, xp_var):
    # Cancel any scheduled match loop and clear the status.
    after_id = session_state.get("after_id")
    if after_id:
        root.after_cancel(after_id)
    ticker_id = session_state.get("ticker_id")
    if ticker_id:
        root.after_cancel(ticker_id)
    anim_after_id = session_state.get("anim_after_id")
    if anim_after_id:
        root.after_cancel(anim_after_id)
    anim_window = session_state.get("anim_window")
    if anim_window:
        anim_window.destroy()
    session_state["after_id"] = None
    session_state["ticker_id"] = None
    session_state["anim_after_id"] = None
    session_state["anim_window"] = None
    session_state["anim_canvas"] = None
    session_state["anim_frame"] = 0
    session_state["running"] = False
    session_state["phase"] = "idle"
    session_state["end_match"] = None
    session_state["schedule_end"] = None
    close_nuke_prompt(session_state)
    session_state["pending_nuke"] = False
    status_var.set("Not in game")
    timer_var.set("")
    map_var.set("")
    kd_var.set("")
    xp_var.set("")


def start_lobby_wait(root, session_state, status_var, timer_var, map_var, kd_var, xp_var, loaded_profile, save_path):
    # Wait a short random buffer before starting the next game.
    if not session_state.get("running"):
        return
    status_var.set("Waiting for a lobby...")
    timer_var.set("")
    map_var.set("")
    kd_var.set("")
    xp_var.set("")
    anim_after_id = session_state.get("anim_after_id")
    if anim_after_id:
        root.after_cancel(anim_after_id)
        session_state["anim_after_id"] = None
    if session_state.get("anim_window"):
        session_state["anim_window"].destroy()
        session_state["anim_window"] = None
        session_state["anim_canvas"] = None
        session_state["anim_frame"] = 0
    session_state["phase"] = "waiting"
    wait_seconds = random.randint(12, 35)
    session_state["after_id"] = root.after(
        wait_seconds * 1000,
        lambda: start_game_session(
            root,
            session_state,
            status_var,
            timer_var,
            map_var,
            kd_var,
            xp_var,
            loaded_profile,
            save_path,
        ),
    )


def start_game_session(root, session_state, status_var, timer_var, map_var, kd_var, xp_var, loaded_profile, save_path):
    # Start a timed game session based on the profile's defaults.
    if not loaded_profile or not save_path:
        return
    defaults = loaded_profile["player"].get("defaults")
    if not defaults or "game_mode" not in defaults:
        status_var.set("Not in game")
        timer_var.set("")
        map_var.set("")
        kd_var.set("")
        xp_var.set("")
        return

    game_mode = defaults["game_mode"]
    map_name = random.choice(MAP_POOL)
    attributes = loaded_profile["player"].get("attributes", {})
    duration_seconds = random.randint(8, 13) * 60
    session_state["running"] = True
    session_state["phase"] = "playing"
    session_state["end_time"] = time.monotonic() + duration_seconds
    stats = ensure_stats(loaded_profile)
    session_state["kills"] = 0
    session_state["deaths"] = 0
    session_state["headshots"] = 0
    session_state["current_streak"] = 0
    session_state["longest_streak"] = int(stats.get("longest_kill_streak", 0))
    session_state["death_minute_start"] = time.monotonic()
    session_state["deaths_in_minute"] = 0
    session_state["respawn_until"] = 0.0
    session_state["last_kill_time"] = 0.0
    session_state["last_kill_enemy"] = None
    session_state["last_kill_indices"] = []
    session_state["last_kill_count"] = 0
    session_state["headshots_in_last_kill"] = 0
    session_state["kill_feed"] = []
    session_state["player_name"] = loaded_profile["player"].get("gamertag", "Player")
    session_state["options"] = loaded_profile["player"].get("options", {})
    session_state["streak_rewards"] = {"uap": None, "airstrike": None, "helicopter": None, "nuke": None}
    session_state["reward_flags"] = set()
    session_state["xp_bonus"] = 0
    session_state["uap_bonus_until"] = 0.0
    session_state["nuke_until"] = 0.0
    session_state["end_match"] = None
    session_state["schedule_end"] = None
    session_state["nuke_prompt"] = None
    session_state["pending_nuke"] = False
    session_state["match_start"] = time.monotonic()
    session_state["timeline"] = {
        "kills": {},
        "deaths": {},
        "headshots": {},
        "uap": {},
        "airstrike": {},
        "helicopter": {},
        "nuke": {},
        "score": {},
    }
    session_state["totals"] = {
        "kills": 0,
        "deaths": 0,
        "headshots": 0,
        "uap": 0,
        "airstrike": 0,
        "helicopter": 0,
        "nuke": 0,
        "score": 0,
    }
    session_state["encounter_enemies"] = random.choices(ENEMY_POOL, k=random.randint(1, 6))
    session_state["encounter_last_update"] = time.monotonic()
    session_state["weapon_name"] = defaults.get("weapon", "Ak-47")
    status_var.set(f"Playing {game_mode}")
    map_var.set(f"Now playing on map {map_name}")
    start_doomguy_animation(root, session_state)
    stats["games_played"] = int(stats.get("games_played", 0)) + 1
    modes = stats.setdefault("game_modes_played", {})
    modes[game_mode] = int(modes.get(game_mode, 0)) + 1
    maps = stats.setdefault("maps_played", {})
    maps[map_name] = int(maps.get(map_name, 0)) + 1
    save_profile_data(loaded_profile, save_path)

    def end_match():
        close_nuke_prompt(session_state)
        session_state["pending_nuke"] = False
        add_kill_death_stats(
            loaded_profile,
            session_state["kills"],
            session_state["deaths"],
            session_state.get("headshots", 0),
        )
        award_xp(
            loaded_profile,
            compute_xp_gain(
                session_state["kills"],
                session_state.get("headshots", 0),
                True,
            ),
        )
        award_weapon_xp(
            loaded_profile,
            session_state.get("weapon_name", "Ak-47"),
            compute_xp_gain(
                session_state["kills"],
                session_state.get("headshots", 0),
                True,
            )
            + session_state.get("headshots", 0) * 5,
            session_state.get("headshots", 0),
        )
        award_xp(loaded_profile, session_state.get("xp_bonus", 0))
        award_weapon_xp(
            loaded_profile,
            session_state.get("weapon_name", "Ak-47"),
            session_state.get("xp_bonus", 0),
        )
        bonus = check_achievements(loaded_profile)
        if bonus:
            award_xp(loaded_profile, bonus)
        loaded_profile["player"]["stats"].update({"longest_kill_streak": session_state["longest_streak"]})
        save_profile_data(loaded_profile, save_path)
        start_lobby_wait(
            root,
            session_state,
            status_var,
            timer_var,
            map_var,
            kd_var,
            xp_var,
            loaded_profile,
            save_path,
        )

    def schedule_end(delay_ms):
        if session_state.get("after_id"):
            root.after_cancel(session_state["after_id"])
        session_state["after_id"] = root.after(delay_ms, end_match)

    def tick():
        if not session_state.get("running") or session_state.get("phase") != "playing":
            return
        now = time.monotonic()
        remaining = max(0, int(session_state["end_time"] - now))
        timer_var.set(f"In-game timer: {format_duration(remaining)}")
        if session_state.get("pending_nuke") and remaining <= 10 and schedule_end:
            close_nuke_prompt(session_state)
            trigger_nuke(session_state, stats, time.monotonic(), schedule_end, force=True)
            session_state["pending_nuke"] = False
        if now < session_state.get("nuke_until", 0):
            timer_var.set("Nuclear Victory")
            session_state["ticker_id"] = root.after(1000, tick)
            return

        if now < session_state.get("respawn_until", 0):
            kd_var.set(
                "Kills: {kills} | Deaths: {deaths} | Streak: {streak} | Longest: {longest}".format(
                    kills=session_state["kills"],
                    deaths=session_state["deaths"],
                    streak=session_state["current_streak"],
                    longest=session_state["longest_streak"],
                )
            )
            total_xp = stats.get("xp", 0) + compute_xp_gain(
                session_state["kills"],
                session_state.get("headshots", 0),
                False,
            ) + session_state.get("xp_bonus", 0)
            preview = progress_state(stats, total_xp - stats.get("xp", 0))
            level = preview["level"]
            xp_into = preview["xp_into"]
            xp_needed = preview["xp_needed"]
            rank = rank_display_from_progress(preview)
            xp_var.set(f"{rank} | Level {level} | XP {xp_into}/{xp_needed}")
            session_state["ticker_id"] = root.after(1000, tick)
            return
        kills_rate, deaths_rate = calculate_rates(attributes)
        effects = compute_attribute_effects(attributes, session_state.get("options"))
        kills_rate *= effects["accuracy"]
        deaths_rate *= max(0.5, 1.1 - (effects["movement_speed"] - 0.8))
        if random.random() < kills_rate:
            encounter = session_state.get("encounter_enemies", [])
            kill_count = 1
            kill_indices = []
            if encounter:
                if random.randint(1, len(encounter)) == 1:
                    kill_count = len(encounter)
                    kill_indices = list(range(len(encounter)))
                else:
                    kill_indices = [random.randrange(len(encounter))]
            session_state["kills"] += kill_count
            session_state["totals"]["kills"] += kill_count
            session_state["current_streak"] += kill_count
            if session_state["current_streak"] > session_state["longest_streak"]:
                session_state["longest_streak"] = session_state["current_streak"]
            session_state["last_kill_time"] = now
            session_state["last_kill_indices"] = kill_indices
            session_state["last_kill_count"] = kill_count
            player_name = session_state.get("player_name", "Player")
            killed_names = [encounter[i] for i in kill_indices] if kill_indices else ["enemy"] * kill_count
            headshots_in_kill = 0
            minute = int((now - session_state["match_start"]) // 60)
            session_state["timeline"]["kills"][minute] = session_state["timeline"]["kills"].get(minute, 0) + kill_count
            session_state["timeline"]["score"][minute] = session_state["timeline"]["score"].get(minute, 0) + kill_count * 10
            session_state["totals"]["score"] += kill_count * 10
            for enemy_name in killed_names:
                headshot = random.random() < effects["headshot_rate"]
                if headshot:
                    session_state["headshots"] += 1
                    session_state["totals"]["headshots"] += 1
                    headshots_in_kill += 1
                suffix = " (Headshot)" if headshot else ""
                session_state["kill_feed"].append((now, f"{player_name} eliminated {enemy_name}{suffix}"))
            session_state["headshots_in_last_kill"] = headshots_in_kill
            if headshots_in_kill:
                session_state["timeline"]["headshots"][minute] = (
                    session_state["timeline"]["headshots"].get(minute, 0) + headshots_in_kill
                )
                headshot_bonus = headshots_in_kill * 5
                session_state["timeline"]["score"][minute] = (
                    session_state["timeline"]["score"].get(minute, 0) + headshot_bonus
                )
                session_state["totals"]["score"] += headshot_bonus
            multikill = MULTIKILL_BONUS.get(kill_count)
            if multikill:
                key, bonus = multikill
                stats[key] = int(stats.get(key, 0)) + 1
                session_state["xp_bonus"] += bonus
                minute = int((now - session_state["match_start"]) // 60)
                session_state["timeline"]["score"][minute] = session_state["timeline"]["score"].get(minute, 0) + bonus
                session_state["totals"]["score"] += bonus
            if now < session_state.get("uap_bonus_until", 0):
                session_state["xp_bonus"] += kill_count * 5
                minute = int((now - session_state["match_start"]) // 60)
                bonus = kill_count * 5
                session_state["timeline"]["score"][minute] = session_state["timeline"]["score"].get(minute, 0) + bonus
                session_state["totals"]["score"] += bonus
            session_state["encounter_enemies"] = random.choices(ENEMY_POOL, k=random.randint(1, 6))
            session_state["encounter_last_update"] = now
            if session_state["current_streak"] >= 3 and "uap" not in session_state["reward_flags"]:
                session_state["streak_rewards"]["uap"] = now
                session_state["reward_flags"].add("uap")
                session_state["uap_bonus_until"] = now + 12
                stats["uap_calls"] = int(stats.get("uap_calls", 0)) + 1
                session_state["totals"]["uap"] += 1
                minute = int((now - session_state["match_start"]) // 60)
                session_state["timeline"]["uap"][minute] = session_state["timeline"]["uap"].get(minute, 0) + 1
            if session_state["current_streak"] >= 5 and "airstrike" not in session_state["reward_flags"]:
                session_state["streak_rewards"]["airstrike"] = now
                session_state["reward_flags"].add("airstrike")
                air_kills = random.randint(0, 6)
                session_state["kills"] += air_kills
                session_state["totals"]["kills"] += air_kills
                bonus = air_kills * 10
                session_state["xp_bonus"] += bonus
                minute = int((now - session_state["match_start"]) // 60)
                session_state["timeline"]["score"][minute] = session_state["timeline"]["score"].get(minute, 0) + bonus
                session_state["totals"]["score"] += bonus
                stats["airstrike_calls"] = int(stats.get("airstrike_calls", 0)) + 1
                stats["airstrike_kills"] = int(stats.get("airstrike_kills", 0)) + air_kills
                session_state["totals"]["airstrike"] += 1
                minute = int((now - session_state["match_start"]) // 60)
                session_state["timeline"]["airstrike"][minute] = (
                    session_state["timeline"]["airstrike"].get(minute, 0) + 1
                )
            if session_state["current_streak"] >= 7 and "helicopter" not in session_state["reward_flags"]:
                session_state["streak_rewards"]["helicopter"] = now
                session_state["reward_flags"].add("helicopter")
                extra_kills = random.randint(0, 22)
                session_state["kills"] += extra_kills
                session_state["totals"]["kills"] += extra_kills
                bonus = extra_kills * 10
                session_state["xp_bonus"] += bonus
                minute = int((now - session_state["match_start"]) // 60)
                session_state["timeline"]["score"][minute] = session_state["timeline"]["score"].get(minute, 0) + bonus
                session_state["totals"]["score"] += bonus
                stats["helicopter_calls"] = int(stats.get("helicopter_calls", 0)) + 1
                stats["helicopter_kills"] = int(stats.get("helicopter_kills", 0)) + extra_kills
                session_state["totals"]["helicopter"] += 1
                minute = int((now - session_state["match_start"]) // 60)
                session_state["timeline"]["helicopter"][minute] = (
                    session_state["timeline"]["helicopter"].get(minute, 0) + 1
                )
            if session_state["current_streak"] >= 25 and "nuke" not in session_state["reward_flags"]:
                session_state["reward_flags"].add("nuke")
                session_state["pending_nuke"] = True
                stats["nuke_victories"] = int(stats.get("nuke_victories", 0)) + 1
                session_state["totals"]["nuke"] += 1
                minute = int((now - session_state["match_start"]) // 60)
                session_state["timeline"]["nuke"][minute] = session_state["timeline"]["nuke"].get(minute, 0) + 1
                session_state["timeline"]["score"][minute] = session_state["timeline"]["score"].get(minute, 0) + 60
                session_state["totals"]["score"] += 60
                if schedule_end:
                    show_nuke_prompt(root, session_state, stats, schedule_end)

        if now - session_state["death_minute_start"] >= 60:
            session_state["death_minute_start"] = now
            session_state["deaths_in_minute"] = 0

        if session_state["deaths_in_minute"] < 20 and random.random() < deaths_rate:
            session_state["deaths"] += 1
            session_state["totals"]["deaths"] += 1
            session_state["deaths_in_minute"] += 1
            session_state["current_streak"] = 0
            session_state["respawn_until"] = now + effects["respawn_seconds"]
            session_state["reward_flags"].clear()
            session_state["uap_bonus_until"] = 0.0
            minute = int((now - session_state["match_start"]) // 60)
            session_state["timeline"]["deaths"][minute] = session_state["timeline"]["deaths"].get(minute, 0) + 1

        kd_var.set(
            "Kills: {kills} | Deaths: {deaths} | Streak: {streak} | Longest: {longest}".format(
                kills=session_state["kills"],
                deaths=session_state["deaths"],
                streak=session_state["current_streak"],
                longest=session_state["longest_streak"],
            )
        )
        minute = int((now - session_state["match_start"]) // 60)
        session_state["timeline"]["kills"][minute] = session_state["timeline"]["kills"].get(minute, 0) + 0
        session_state["timeline"]["headshots"][minute] = session_state["timeline"]["headshots"].get(minute, 0) + 0
        total_xp = stats.get("xp", 0) + compute_xp_gain(
            session_state["kills"],
            session_state.get("headshots", 0),
            False,
        ) + session_state.get("xp_bonus", 0)
        preview = progress_state(stats, total_xp - stats.get("xp", 0))
        level = preview["level"]
        xp_into = preview["xp_into"]
        xp_needed = preview["xp_needed"]
        rank = rank_display_from_progress(preview)
        xp_var.set(f"{rank} | Level {level} | XP {xp_into}/{xp_needed}")
        session_state["ticker_id"] = root.after(1000, tick)

    tick()

    session_state["end_match"] = end_match
    session_state["schedule_end"] = schedule_end
    schedule_end(duration_seconds * 1000)


def on_start(root):
    # Confirm start and open the profile setup flow.
    if messagebox.askyesno("Start Game", "Would you like to start the game?"):
        open_profile_window(root)


def on_options(root, loaded_profile, save_path, session_state):
    # Allow players to override attribute-driven effects.
    if not loaded_profile or not save_path:
        messagebox.showinfo("Options", "Load a player profile to edit options.")
        return

    attributes = loaded_profile["player"].get("attributes", {})
    base_effects = compute_attribute_effects(attributes)
    options = loaded_profile["player"].get("options", {})

    window = tk.Toplevel(root)
    window.title("Options")
    window.resizable(False, False)

    header = tk.Label(window, text="Attribute Effects (Overrides)", font=("Segoe UI", 11))
    header.pack(padx=24, pady=(18, 6))

    hint = tk.Label(window, text="Adjust values to override the attribute defaults.", font=("Segoe UI", 9))
    hint.pack(padx=24, pady=(0, 10))

    accuracy_var = tk.DoubleVar(value=options.get("accuracy", base_effects["accuracy"]) * 100)
    move_var = tk.DoubleVar(value=options.get("movement_speed", base_effects["movement_speed"]))
    respawn_var = tk.DoubleVar(value=options.get("respawn_seconds", base_effects["respawn_seconds"]))
    headshot_var = tk.DoubleVar(value=options.get("headshot_rate", base_effects["headshot_rate"]) * 100)

    def add_slider(label_text, var, from_, to, resolution, unit):
        row = tk.Frame(window)
        row.pack(fill="x", padx=24, pady=4)
        label = tk.Label(row, text=label_text, width=16, anchor="w")
        label.pack(side="left")
        scale = tk.Scale(
            row,
            from_=from_,
            to=to,
            resolution=resolution,
            orient="horizontal",
            length=200,
            showvalue=True,
            variable=var,
        )
        scale.pack(side="right")
        if unit:
            scale.configure(label=unit)

    add_slider("Accuracy %", accuracy_var, 50, 110, 1, None)
    add_slider("Move Speed", move_var, 0.7, 1.3, 0.01, "x")
    add_slider("Respawn", respawn_var, 1.5, 4.0, 0.1, "s")
    add_slider("Headshot %", headshot_var, 5, 40, 1, None)

    def on_save():
        loaded_profile["player"]["options"] = {
            "accuracy": accuracy_var.get() / 100.0,
            "movement_speed": move_var.get(),
            "respawn_seconds": respawn_var.get(),
            "headshot_rate": headshot_var.get() / 100.0,
        }
        session_state["options"] = loaded_profile["player"]["options"]
        save_profile_data(loaded_profile, save_path)
        window.destroy()

    window.protocol("WM_DELETE_WINDOW", window.destroy)


def open_stats_window(root, session_state):
    # Show simple graphs for the current match timeline.
    if not session_state or session_state.get("phase") != "playing":
        messagebox.showinfo("Stats", "Start a match to view live stats.")
        return

    window = tk.Toplevel(root)
    window.title("Match Stats")
    window.resizable(False, False)

    canvas = tk.Canvas(window, width=420, height=260, bg="#101820", highlightthickness=0)
    canvas.pack(padx=16, pady=16)

    def draw_series(series, color, origin_x, origin_y, width, height, label):
        max_minute = max(series.keys(), default=0)
        max_value = max(series.values(), default=1)
        bars = max_minute + 1
        bar_width = max(4, width // max(1, bars))
        canvas.create_text(origin_x, origin_y - 10, text=label, fill="#c9d4e2", anchor="w")
        for minute in range(bars):
            value = series.get(minute, 0)
            bar_height = 0 if max_value == 0 else int((value / max_value) * height)
            x0 = origin_x + minute * bar_width
            y0 = origin_y + height - bar_height
            x1 = x0 + bar_width - 2
            y1 = origin_y + height
            canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="")

    kills_series = session_state.get("timeline", {}).get("kills", {})
    deaths_series = session_state.get("timeline", {}).get("deaths", {})
    headshots_series = session_state.get("timeline", {}).get("headshots", {})
    score_series = session_state.get("timeline", {}).get("score", {})

    draw_series(kills_series, "#6bd98a", 20, 30, 180, 80, "Kills per minute")
    draw_series(deaths_series, "#f07070", 220, 30, 180, 80, "Deaths per minute")
    draw_series(headshots_series, "#7fc7ff", 20, 140, 180, 80, "Headshots per minute")
    draw_series(score_series, "#f4c542", 220, 140, 180, 80, "Score per minute")

    totals = session_state.get("totals", {})
    summary = (
        f"Kills: {totals.get('kills', 0)} | Deaths: {totals.get('deaths', 0)} | "
        f"Headshots: {totals.get('headshots', 0)} | UAP: {totals.get('uap', 0)} | "
        f"Airstrike: {totals.get('airstrike', 0)} | Helicopter: {totals.get('helicopter', 0)} | "
        f"Nuke: {totals.get('nuke', 0)} | Score: {totals.get('score', 0)}"
    )
    canvas.create_text(20, 235, text=summary, fill="#c9d4e2", anchor="w", font=("Segoe UI", 9))


def open_achievements_window(root, loaded_profile):
    # Display achievements with progress bars.
    if not loaded_profile:
        messagebox.showinfo("Achievements", "Load a player profile to view achievements.")
        return

    stats = ensure_stats(loaded_profile)
    earned = stats.setdefault("achievements", {})

    window = tk.Toplevel(root)
    window.title("Achievements")
    window.resizable(False, False)

    tooltip = {"window": None, "label": None}

    def show_tooltip(widget, text):
        if tooltip["window"]:
            tooltip["window"].destroy()
        tw = tk.Toplevel(window)
        tw.wm_overrideredirect(True)
        tw.attributes("-topmost", True)
        x = widget.winfo_rootx() + 10
        y = widget.winfo_rooty() + 20
        tw.geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=text, bg="#1b2230", fg="#c9d4e2", font=("Segoe UI", 9), padx=6, pady=4)
        label.pack()
        tooltip["window"] = tw
        tooltip["label"] = label

    def hide_tooltip(*_):
        if tooltip["window"]:
            tooltip["window"].destroy()
            tooltip["window"] = None
            tooltip["label"] = None

    frame = tk.Frame(window)
    frame.pack(padx=16, pady=16)

    for ach_id, name, key, threshold, reward_xp, description in ACHIEVEMENTS:
        value = achievement_value(loaded_profile, key)
        done = bool(earned.get(ach_id))
        display_value = min(value, threshold)
        ratio = 1.0 if threshold == 0 else min(1.0, display_value / threshold)

        title = tk.Label(
            frame,
            text=f"{name} (+{reward_xp} XP)",
            font=("Segoe UI", 10),
            fg="#f4c542" if done else "#7a7a7a",
            anchor="w",
        )
        title.pack(fill="x")
        title.bind("<Enter>", lambda e, text=description: show_tooltip(e.widget, text))
        title.bind("<Leave>", hide_tooltip)

        progress = tk.Canvas(frame, width=260, height=8, highlightthickness=0, bg="#1b2230")
        progress.pack(pady=(2, 8))
        fill_width = int(260 * ratio)
        color = "#6bd98a" if done else "#4a6a84"
        progress.create_rectangle(0, 0, fill_width, 8, fill=color, outline="")
        progress.create_text(
            130,
            4,
            text=f"{display_value}/{threshold}",
            fill="#c9d4e2",
            font=("Segoe UI", 8),
        )

def open_profile_window(root):
    # Profile creation dialog for attribute distribution and gamertag entry.
    window = tk.Toplevel(root)
    window.title("Player Profile")
    window.resizable(False, False)

    header = tk.Label(
        window,
        text="Distribute 30 attribute points (0-10 per attribute).",
        font=("Segoe UI", 11),
    )
    header.pack(padx=24, pady=(18, 6))

    remaining_var = tk.StringVar(value=f"Points remaining: {ATTRIBUTE_POINTS}")
    remaining_label = tk.Label(window, textvariable=remaining_var, font=("Segoe UI", 10))
    remaining_label.pack(padx=24, pady=(0, 12))

    scales_frame = tk.Frame(window)
    scales_frame.pack(padx=24, pady=(0, 12))

    # Track slider state for each attribute.
    attribute_vars = {}
    last_values = {}

    def on_scale_change(attribute_name, raw_value):
        # Enforce the total points budget by clamping changes.
        value = int(float(raw_value))
        total = sum(var.get() for var in attribute_vars.values())
        if total > ATTRIBUTE_POINTS:
            over = total - ATTRIBUTE_POINTS
            adjusted = max(0, value - over)
            attribute_vars[attribute_name].set(adjusted)
            last_values[attribute_name] = adjusted
        else:
            last_values[attribute_name] = value
        refresh_state()

    for name in ATTRIBUTES:
        row = tk.Frame(scales_frame)
        row.pack(fill="x", pady=4)

        label = tk.Label(row, text=name, width=18, anchor="w")
        label.pack(side="left")

        var = tk.IntVar(value=0)
        scale = tk.Scale(
            row,
            from_=0,
            to=ATTRIBUTE_MAX,
            orient="horizontal",
            length=220,
            showvalue=True,
            variable=var,
            command=lambda value, attr=name: on_scale_change(attr, value),
        )
        scale.pack(side="right")
        attribute_vars[name] = var
        last_values[name] = 0

    gamertag_frame = tk.Frame(window)
    gamertag_frame.pack(padx=24, pady=(6, 0))

    gamertag_label = tk.Label(gamertag_frame, text="Gamertag:", width=18, anchor="w")
    gamertag_label.pack(side="left")

    gamertag_var = tk.StringVar()
    gamertag_entry = tk.Entry(gamertag_frame, textvariable=gamertag_var, width=24, state="disabled")
    gamertag_entry.pack(side="right")

    save_button = tk.Button(window, text="Save Data", width=16, state="disabled")
    save_button.pack(pady=(10, 18))

    def refresh_state():
        # Enable the gamertag field and save button only when points are fully spent.
        values = [var.get() for var in attribute_vars.values()]
        remaining = remaining_points(values)
        remaining_var.set(f"Points remaining: {remaining}")

        if remaining == 0:
            if gamertag_entry["state"] == "disabled":
                gamertag_entry.configure(state="normal")
            gamertag_ready = bool(gamertag_var.get().strip())
            save_button.configure(state="normal" if gamertag_ready else "disabled")
        else:
            gamertag_entry.configure(state="disabled")
            save_button.configure(state="disabled")

    def on_gamertag_change(*_):
        # Re-check save readiness when the gamertag changes.
        refresh_state()

    def on_save():
        # Validate inputs and write the profile to disk.
        values = {name: var.get() for name, var in attribute_vars.items()}
        remaining = remaining_points(values.values())
        if remaining != 0:
            messagebox.showwarning("Points Remaining", "You must spend all 30 points.")
            return
        gamertag = gamertag_var.get().strip()
        if not gamertag:
            messagebox.showwarning("Missing Gamertag", "Please enter your gamertag.")
            return
        profile = {
            "gamertag": gamertag,
            "attributes": values,
            "play_time_seconds": 0,
            "last_saved": int(time.time()),
            "stats": {
                "games_played": 0,
                "game_modes_played": {},
                "maps_played": {},
                "kills": 0,
                "deaths": 0,
                "longest_kill_streak": 0,
                "headshots": 0,
                "xp": 0,
                "level": 1,
                "prestige_unlocked": False,
                "prestige": 0,
                "master_prestige": False,
                "master_level": 1,
                "weapons": {},
                "uap_calls": 0,
                "airstrike_calls": 0,
                "helicopter_calls": 0,
                "airstrike_kills": 0,
                "helicopter_kills": 0,
                "nuke_victories": 0,
                "double_kills": 0,
                "triple_kills": 0,
                "quad_kills": 0,
                "monster_kills": 0,
                "team_kills": 0,
                "achievements": {},
            },
        }
        save_player_profile(profile)
        messagebox.showinfo("Profile Saved", "Your profile has been saved.")
        window.destroy()

    gamertag_var.trace_add("write", on_gamertag_change)
    save_button.configure(command=on_save)


def load_player_profile(root, playing_as_var):
    # Load a saved profile from disk and return its contents and path.
    file_path = filedialog.askopenfilename(
        parent=root,
        title="Load Player Profile",
        filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
    )
    if not file_path:
        return None
    try:
        path = Path(file_path)
        data = json.loads(path.read_text(encoding="ascii"))
        gamertag = data["player"]["gamertag"]
    except (OSError, json.JSONDecodeError, KeyError, TypeError):
        messagebox.showerror("Load Failed", "Selected file is not a valid profile.")
        return None

    last_saved = int(data["player"].get("last_saved", time.time()))
    offline_seconds = int(time.time()) - last_saved
    if offline_seconds >= 60:
        apply_offline_progress(data, offline_seconds)
        save_profile_data(data, path)

    playing_as_var.set(f"Playing as: {gamertag}")
    return data, path


def view_player_profile(root, loaded_profile, timer_state):
    # Show a read-only view of the currently loaded profile.
    if not loaded_profile:
        messagebox.showinfo("No Profile Loaded", "Load a player profile first.")
        return
    player = loaded_profile["player"]
    gamertag = player["gamertag"]
    attributes = player["attributes"]
    total_time = get_total_play_time(timer_state)
    stats = player.get("stats", {})
    kills = int(stats.get("kills", 0))
    deaths = int(stats.get("deaths", 0))
    kd_ratio = kills if deaths == 0 else kills / deaths
    longest_streak = int(stats.get("longest_kill_streak", 0))
    headshots = int(stats.get("headshots", 0))
    xp_total = int(stats.get("xp", 0))
    progress = progress_state(stats)
    level = progress["level"]
    xp_into = progress["xp_into"]
    xp_needed = progress["xp_needed"]
    rank = rank_display_from_progress(progress)

    window = tk.Toplevel(root)
    window.title("Player Profile")
    window.resizable(False, False)
    diamond_swatches = []
    diamond_after_id = {"id": None, "index": 0}

    def stop_diamond_animation():
        if diamond_after_id["id"]:
            window.after_cancel(diamond_after_id["id"])
            diamond_after_id["id"] = None

    title = tk.Label(window, text=f"Gamertag: {gamertag}", font=("Segoe UI", 11))
    title.pack(padx=24, pady=(18, 10))

    time_label = tk.Label(window, text=f"Time Played: {format_duration(total_time)}", font=("Segoe UI", 10))
    time_label.pack(padx=24, pady=(0, 8))

    level_label = tk.Label(
        window,
        text=f"Level: {level} ({xp_into}/{xp_needed} XP)",
        font=("Segoe UI", 10),
    )
    level_label.pack(padx=24, pady=(0, 8))

    rank_row = tk.Frame(window)
    rank_row.pack(padx=24, pady=(0, 8), fill="x")
    rank_swatch = tk.Canvas(rank_row, width=12, height=12, highlightthickness=0)
    rank_swatch.create_rectangle(1, 1, 11, 11, fill=rank_color(rank), outline="#1a1a1a")
    rank_swatch.pack(side="left", padx=(0, 6))
    rank_label = tk.Label(rank_row, text=f"Rank: {rank}", font=("Segoe UI", 10))
    rank_label.pack(side="left")

    total_xp_label = tk.Label(window, text=f"Total XP: {xp_total}", font=("Segoe UI", 10))
    total_xp_label.pack(padx=24, pady=(0, 8))

    kd_label = tk.Label(
        window,
        text=f"Kills: {kills} | Deaths: {deaths} | K/D Ratio: {kd_ratio:.2f}",
        font=("Segoe UI", 10),
    )
    kd_label.pack(padx=24, pady=(0, 8))

    streak_label = tk.Label(window, text=f"Longest Kill Streak: {longest_streak}", font=("Segoe UI", 10))
    streak_label.pack(padx=24, pady=(0, 8))

    headshot_label = tk.Label(window, text=f"Headshots: {headshots}", font=("Segoe UI", 10))
    headshot_label.pack(padx=24, pady=(0, 8))

    uap_calls = int(stats.get("uap_calls", 0))
    airstrike_calls = int(stats.get("airstrike_calls", 0))
    helicopter_calls = int(stats.get("helicopter_calls", 0))
    airstrike_kills = int(stats.get("airstrike_kills", 0))
    helicopter_kills = int(stats.get("helicopter_kills", 0))
    nuke_victories = int(stats.get("nuke_victories", 0))
    double_kills = int(stats.get("double_kills", 0))
    triple_kills = int(stats.get("triple_kills", 0))
    quad_kills = int(stats.get("quad_kills", 0))
    monster_kills = int(stats.get("monster_kills", 0))
    team_kills = int(stats.get("team_kills", 0))

    rewards_label = tk.Label(
        window,
        text=(
            f"UAPs: {uap_calls} | Airstrikes: {airstrike_calls} "
            f"(Kills {airstrike_kills}) | Helicopters: {helicopter_calls} "
            f"(Kills {helicopter_kills}) | Nukes: {nuke_victories}"
        ),
        font=("Segoe UI", 10),
    )
    rewards_label.pack(padx=24, pady=(0, 8))

    multikill_label = tk.Label(
        window,
        text=(
            f"Double: {double_kills} | Triple: {triple_kills} | Quad: {quad_kills} | "
            f"Monster: {monster_kills} | Team: {team_kills}"
        ),
        font=("Segoe UI", 10),
    )
    multikill_label.pack(padx=24, pady=(0, 8))

    weapons = stats.get("weapons", {})
    if weapons:
        weapon_header = tk.Label(window, text="Weapon Progression", font=("Segoe UI", 10))
        weapon_header.pack(padx=24, pady=(4, 6))
        for weapon_name in sorted(weapons):
            weapon_stats = weapons[weapon_name]
            weapon_xp = int(weapon_stats.get("xp", 0))
            weapon_level, weapon_into, weapon_needed = level_progress(weapon_xp)
            weapon_headshots = int(weapon_stats.get("headshots", 0))
            weapon_camo = weapon_stats.get("camo", "None")
            row = tk.Frame(window)
            row.pack(fill="x", padx=24, pady=1)
            label = tk.Label(row, text=weapon_name, width=14, anchor="w")
            label.pack(side="left")
            swatch = tk.Canvas(row, width=12, height=12, highlightthickness=0)
            swatch.create_rectangle(1, 1, 11, 11, fill=camo_color(weapon_camo), outline="#1a1a1a")
            swatch.pack(side="left", padx=(4, 6))
            if weapon_camo == "Diamond":
                diamond_swatches.append(swatch)
            value = tk.Label(
                row,
                text=f"Lv {weapon_level} ({weapon_into}/{weapon_needed}) | HS {weapon_headshots} | {weapon_camo}",
                anchor="e",
            )
            value.pack(side="right")

    def animate_diamond():
        if not diamond_swatches:
            return
        colors = ["#7fc7ff", "#bfe9ff", "#5aaef2", "#e7f7ff"]
        color = colors[diamond_after_id["index"] % len(colors)]
        diamond_after_id["index"] += 1
        for swatch in diamond_swatches:
            swatch.delete("all")
            swatch.create_rectangle(1, 1, 11, 11, fill=color, outline="#1a1a1a")
        diamond_after_id["id"] = window.after(300, animate_diamond)

    animate_diamond()

    def on_close():
        stop_diamond_animation()
        window.destroy()

    window.protocol("WM_DELETE_WINDOW", on_close)

    attrs_frame = tk.Frame(window)
    attrs_frame.pack(padx=24, pady=(0, 18))

    for name in ATTRIBUTES:
        value = attributes.get(name, 0)
        row = tk.Frame(attrs_frame)
        row.pack(fill="x", pady=2)
        label = tk.Label(row, text=name, width=18, anchor="w")
        label.pack(side="left")
        number = tk.Label(row, text=str(value), width=4, anchor="e")
        number.pack(side="right")


def open_game_setup_window(
    root,
    loaded_profile,
    save_path,
    session_state,
    status_var,
    timer_var,
    map_var,
    kd_var,
    xp_var,
):
    # Allow the player to pick default weapon and game mode for this profile.
    player = loaded_profile["player"]
    defaults = player.get("defaults", {})

    window = tk.Toplevel(root)
    window.title("Game Setup")
    window.resizable(False, False)

    header = tk.Label(window, text="Select default loadout and mode.", font=("Segoe UI", 11))
    header.pack(padx=24, pady=(18, 12))

    weapon_frame = tk.Frame(window)
    weapon_frame.pack(padx=24, pady=(0, 8))

    weapon_label = tk.Label(weapon_frame, text="Weapon:", width=18, anchor="w")
    weapon_label.pack(side="left")

    weapon_var = tk.StringVar(value=defaults.get("weapon", WEAPON_POOL[0]))
    weapon_menu = tk.OptionMenu(weapon_frame, weapon_var, *WEAPON_POOL)
    weapon_menu.config(width=18)
    weapon_menu.pack(side="right")

    mode_frame = tk.Frame(window)
    mode_frame.pack(padx=24, pady=(0, 12))

    mode_label = tk.Label(mode_frame, text="Game Mode:", width=18, anchor="w")
    mode_label.pack(side="left")

    mode_var = tk.StringVar(value=defaults.get("game_mode", "Team death match"))
    mode_menu = tk.OptionMenu(mode_frame, mode_var, "Team death match")
    mode_menu.config(width=18)
    mode_menu.pack(side="right")

    def on_save():
        player["defaults"] = {
            "weapon": weapon_var.get(),
            "game_mode": mode_var.get(),
        }
        save_profile_data(loaded_profile, save_path)
        start_game_session(
            root,
            session_state,
            status_var,
            timer_var,
            map_var,
            kd_var,
            xp_var,
            loaded_profile,
            save_path,
        )
        window.destroy()

    save_button = tk.Button(window, text="Save and Close Window", width=22, command=on_save)
    save_button.pack(pady=(6, 18))


def main():
    # Build the main menu window.
    root = tk.Tk()
    root.title("Idle FPS")

    label = tk.Label(root, text="Idle FPS version 0.0.0.1", font=("Segoe UI", 16))
    label.pack(padx=24, pady=(24, 12))

    menu_frame = tk.Frame(root)
    menu_frame.pack(padx=24, pady=(0, 24))

    playing_as_var = tk.StringVar(value="Playing as: ")
    session_status_var = tk.StringVar(value="Not in game")
    session_timer_var = tk.StringVar(value="")
    session_map_var = tk.StringVar(value="")
    session_kd_var = tk.StringVar(value="")
    session_xp_var = tk.StringVar(value="")

    loaded_profile = {"data": None, "path": None}
    timer_state = {"elapsed": 0, "start": 0.0, "running": False}
    session_state = {
        "running": False,
        "phase": "idle",
        "after_id": None,
        "ticker_id": None,
        "end_time": 0.0,
        "anim_window": None,
        "anim_canvas": None,
        "anim_after_id": None,
        "anim_frame": 0,
        "respawn_until": 0.0,
        "last_kill_time": 0.0,
        "last_kill_enemy": None,
        "last_kill_indices": [],
        "last_kill_count": 0,
        "encounter_enemies": [],
        "encounter_last_update": 0.0,
        "headshots": 0,
        "kill_feed": [],
        "player_name": "Player",
        "xp_bonus": 0,
        "uap_bonus_until": 0.0,
        "nuke_until": 0.0,
        "nuke_prompt": None,
        "pending_nuke": False,
        "match_start": 0.0,
        "timeline": {},
        "totals": {},
    }

    def on_start_click():
        if loaded_profile["data"] and loaded_profile["path"]:
            open_game_setup_window(
                root,
                loaded_profile["data"],
                loaded_profile["path"],
                session_state,
                session_status_var,
                session_timer_var,
                session_map_var,
                session_kd_var,
                session_xp_var,
            )
            return
        on_start(root)

    start_button = tk.Button(menu_frame, text="Start", width=16, command=on_start_click)
    start_button.pack(pady=4)

    def on_load_profile():
        profile = load_player_profile(root, playing_as_var)
        if profile:
            data, path = profile
            loaded_profile["data"] = data
            loaded_profile["path"] = path
            timer_state["elapsed"] = int(data["player"].get("play_time_seconds", 0))
            timer_state["start"] = time.monotonic()
            timer_state["running"] = True
            view_button.pack(pady=4)
            start_button.configure(text="Loadout Options")
            start_game_session(
                root,
                session_state,
                session_status_var,
                session_timer_var,
                session_map_var,
                session_kd_var,
                session_xp_var,
                data,
                path,
            )
        elif loaded_profile["data"] is None:
            start_button.configure(text="Start")

    load_button = tk.Button(
        menu_frame,
        text="Load Player Profile",
        width=16,
        command=on_load_profile,
    )
    load_button.pack(pady=4)

    view_button = tk.Button(
        menu_frame,
        text="View Player Profile",
        width=16,
        command=lambda: view_player_profile(root, loaded_profile["data"], timer_state),
    )
    view_button.pack_forget()

    options_button = tk.Button(
        menu_frame,
        text="Options",
        width=16,
        command=lambda: on_options(root, loaded_profile["data"], loaded_profile["path"], session_state),
    )
    options_button.pack(pady=4)

    stats_button = tk.Button(
        menu_frame,
        text="Stats",
        width=16,
        command=lambda: open_stats_window(root, session_state),
    )
    stats_button.pack(pady=4)

    achievements_button = tk.Button(
        menu_frame,
        text="Achievements",
        width=16,
        command=lambda: open_achievements_window(root, loaded_profile["data"]),
    )
    achievements_button.pack(pady=4)

    def on_about():
        messagebox.showinfo(
            "About",
            "Vibe coded by Jdog 1/2/2026.\nUse as inspiration to make a better Idle FPS game.",
        )

    about_button = tk.Button(menu_frame, text="About", width=16, command=on_about)
    about_button.pack(pady=4)

    def on_exit():
        if loaded_profile["data"] and loaded_profile["path"] and session_state.get("phase") == "playing":
            add_kill_death_stats(
                loaded_profile["data"],
                session_state.get("kills", 0),
                session_state.get("deaths", 0),
                session_state.get("headshots", 0),
            )
            award_xp(
                loaded_profile["data"],
                compute_xp_gain(
                    session_state.get("kills", 0),
                    session_state.get("headshots", 0),
                    False,
                ),
            )
            award_weapon_xp(
                loaded_profile["data"],
                session_state.get("weapon_name", "Ak-47"),
                compute_xp_gain(
                    session_state.get("kills", 0),
                    session_state.get("headshots", 0),
                    False,
                )
                + session_state.get("headshots", 0) * 5,
                session_state.get("headshots", 0),
            )
            award_xp(loaded_profile["data"], session_state.get("xp_bonus", 0))
            award_weapon_xp(
                loaded_profile["data"],
                session_state.get("weapon_name", "Ak-47"),
                session_state.get("xp_bonus", 0),
            )
            bonus = check_achievements(loaded_profile["data"])
            if bonus:
                award_xp(loaded_profile["data"], bonus)
            loaded_profile["data"]["player"]["stats"].update(
                {"longest_kill_streak": session_state.get("longest_streak", 0)}
            )
        stop_game_session(
            root,
            session_state,
            session_status_var,
            session_timer_var,
            session_map_var,
            session_kd_var,
            session_xp_var,
        )
        if loaded_profile["data"] and loaded_profile["path"]:
            total_time = get_total_play_time(timer_state)
            loaded_profile["data"]["player"]["play_time_seconds"] = total_time
            save_profile_data(loaded_profile["data"], loaded_profile["path"])
        root.destroy()

    exit_button = tk.Button(menu_frame, text="Exit", width=16, command=on_exit)
    exit_button.pack(pady=4)

    playing_as_label = tk.Label(root, textvariable=playing_as_var, font=("Segoe UI", 10))
    playing_as_label.pack(padx=24, pady=(0, 6))

    session_status_label = tk.Label(root, textvariable=session_status_var, font=("Segoe UI", 10))
    session_status_label.pack(padx=24, pady=(0, 6))

    session_timer_label = tk.Label(root, textvariable=session_timer_var, font=("Segoe UI", 10))
    session_timer_label.pack(padx=24, pady=(0, 16))

    session_map_label = tk.Label(root, textvariable=session_map_var, font=("Segoe UI", 10))
    session_map_label.pack(padx=24, pady=(0, 16))

    session_kd_label = tk.Label(root, textvariable=session_kd_var, font=("Segoe UI", 10))
    session_kd_label.pack(padx=24, pady=(0, 16))

    session_xp_label = tk.Label(root, textvariable=session_xp_var, font=("Segoe UI", 10))
    session_xp_label.pack(padx=24, pady=(0, 16))

    root.resizable(False, False)
    root.protocol("WM_DELETE_WINDOW", on_exit)
    root.mainloop()


if __name__ == "__main__":
    main()
