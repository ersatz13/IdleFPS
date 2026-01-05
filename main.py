import json
import random
import time
import tkinter as tk
import tkinter.font as tkfont
from tkinter import ttk
try:
    import pystray
    from PIL import Image, ImageDraw
except Exception:
    pystray = None
    Image = None
    ImageDraw = None
from pathlib import Path

# Core configuration for saves and attribute setup.
DEFAULT_SAVE_FILE = Path("user_save.json")
LAST_PROFILE_FILE = Path("last_profile.txt")
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
    "Overpass",
    "Highrise",
    "Favela",
    "Scrapyard",
    "Wasteland",
    "Shipment",
    "Skidrow",
    "Estate",
    "Invasion",
    "Crossfire",
    "Backlot",
    "Vacant",
)
ENEMY_POOL = ("Rusher", "Camper", "BK randy")
WEAPON_CATEGORIES = {
    "Assault Rifle": ("Ak-47", "M4A1", "FAMAS", "G36C", "Kilo 141", "SCAR-H"),
    "SMG": ("MP5", "P90", "Uzi", "Vector", "PP-Bizon", "MP7"),
    "Sniper Rifle": ("Kar98k", "HDR", "AX-50", "Dragunov", "SP-R 208", "Intervention"),
    "Pistol": ("M9", "Glock 18", "Desert Eagle", "P226", "1911", "MP-443"),
    "Rocket Launcher": ("RPG-7", "Strela-P", "JOKR", "PILA", "Panzerfaust", "AT4"),
}
WEAPON_POOL = tuple(weapon for weapons in WEAPON_CATEGORIES.values() for weapon in weapons)
TEAM_DEATHMATCH_KILL_CAP = 150
DOMINATION_SCORE_CAP = 600
FREE_FOR_ALL_KILL_CAP = 30
PLAYER_TEAM_SIZE = 5
ENEMY_TEAM_SIZE = 6
AI_SKILL_RANGE = (0.6, 1.4)
AI_KILL_RATE = 0.08
THEME = {
    "bg": "#0f141b",
    "panel": "#141c26",
    "panel_edge": "#1c2733",
    "text": "#d6e2f0",
    "muted": "#9fb0c3",
    "accent": "#7fc7ff",
    "button": "#1f2a36",
    "button_hover": "#2a3947",
    "primary": "#2b6cb0",
    "primary_hover": "#3a7cc4",
    "danger": "#7a3b3b",
}
WEAPON_ACHIEVEMENT_BASE = 100
TEAMMATE_NAME_POOL = (
    "Falcon",
    "Ghost",
    "Viper",
    "Reaper",
    "Nova",
    "Rogue",
    "Saber",
    "Blaze",
    "Echo",
    "Ranger",
    "Havoc",
    "Atlas",
    "Striker",
    "Bishop",
    "Cipher",
    "Raven",
    "Titan",
    "Pulse",
    "Arrow",
    "Kodiak",
    "Tracer",
    "Lancer",
    "Onyx",
    "Phantom",
    "Comet",
    "Sledge",
    "Tempest",
    "Vector",
    "Maverick",
    "Glitch",
    "Blitz",
    "Specter",
    "Nebula",
    "Raptor",
    "Vanguard",
    "Nomad",
)
ENEMY_NAME_POOL = (
    "Wraith",
    "Marauder",
    "Riot",
    "Vandal",
    "Drake",
    "Mantis",
    "Nightfall",
    "Shade",
    "Widow",
    "Grim",
    "Harpy",
    "Grudge",
    "Rage",
    "Banshee",
    "Scorch",
    "Specter",
    "Hollow",
    "Venom",
    "Raptor",
    "Reckon",
    "Havoc",
    "Blight",
    "Ruin",
    "Vortex",
    "Shatter",
    "Onyx",
    "Grimace",
    "Karma",
    "Razor",
    "Grit",
    "Prowler",
    "Talon",
    "Cinder",
    "Fury",
    "Rancor",
    "Cipher",
)
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
    (1000, "Singularity"),
]
CAMO_ORDER = ["None"] + [name for _, name in CAMO_UNLOCKS]
CAMO_RANK = {name: idx for idx, name in enumerate(CAMO_ORDER)}
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
    "Singularity": "#ffffff",
}
ROMAN_NUMERALS = ("I", "II", "III", "IV", "V", "VI", "VII", "VIII")
ACHIEVEMENT_GROWTH = 1.5
KILL_ACHIEVEMENT_GROWTH = 2.0
BASE_ACHIEVEMENTS = [
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
    ("UAV_25", "Recon Specialist", "UAV_calls", 25, 200, "Call in 25 UAVs."),
    ("airstrike_25", "Fire Support", "airstrike_calls", 25, 200, "Call in 25 airstrikes."),
    ("heli_25", "Air Cav", "helicopter_calls", 25, 300, "Call in 25 helicopters."),
    ("nuke_1", "Nuclear Option", "nuke_victories", 1, 500, "Earn 1 nuclear victory."),
    ("nuke_10", "Fallout", "nuke_victories", 10, 2000, "Earn 10 nuclear victories."),
    ("matches_100", "Career Soldier", "games_played", 100, 300, "Play 100 matches."),
    ("matches_1000", "Lifelong Warrior", "games_played", 1000, 1500, "Play 1,000 matches."),
    ("playtime_24h", "Veteran", "play_time_seconds", 24 * 3600, 400, "Accumulate 24 hours played."),
]


def weapon_achievement_id(weapon_name):
    # Normalize weapon names into consistent achievement ids.
    cleaned = "".join(ch.lower() if ch.isalnum() else "_" for ch in weapon_name).strip("_")
    return f"weapon_kills_{cleaned}"


WEAPON_ACHIEVEMENTS = [
    (
        weapon_achievement_id(weapon),
        f"{weapon} Warpath",
        f"weapon_kills:{weapon}",
        WEAPON_ACHIEVEMENT_BASE,
        50,
        f"Reach {WEAPON_ACHIEVEMENT_BASE} kills with {weapon}.",
    )
    for weapon in WEAPON_POOL
]


def expand_achievements(base_achievements, levels=8):
    # Build multi-level achievements with non-linear growth per tier.
    expanded = []
    for ach_id, name, key, threshold, reward_xp, description in base_achievements:
        prev_threshold = None
        prev_reward = None
        for level in range(1, levels + 1):
            level_id = ach_id if level == 1 else f"{ach_id}_l{level}"
            level_name = name if level == 1 else f"{name} Tier {ROMAN_NUMERALS[level - 1]}"
            if key == "kills" or key.startswith("weapon_kills:"):
                tier_growth = KILL_ACHIEVEMENT_GROWTH
            else:
                tier_growth = ACHIEVEMENT_GROWTH
            growth = tier_growth ** (level - 1)
            level_threshold = int(round(threshold * growth))
            level_reward = int(round(reward_xp * growth))
            if level == levels and prev_threshold is not None and prev_reward is not None:
                level_threshold = prev_threshold * 4
                level_reward = prev_reward * 4
            level_description = f"{description} (Level {level} of {levels})"
            expanded.append((level_id, level_name, key, level_threshold, level_reward, level_description))
            prev_threshold = level_threshold
            prev_reward = level_reward
    return expanded


ACHIEVEMENTS = expand_achievements(BASE_ACHIEVEMENTS + WEAPON_ACHIEVEMENTS)
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


def master_level_progress_with_cap(xp_total, level_cap):
    # Master prestige uses a flat XP requirement per level.
    xp_total = max(0, int(xp_total))
    level = min(level_cap, 1 + xp_total // 1_000_000)
    remaining = xp_total % 1_000_000
    threshold = 1_000_000
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
    level = int(stats.get("level", 1))

    while True:
        if master:
            threshold = 1_000_000
            if xp < threshold or master_level >= MASTER_MAX_LEVEL:
                break
            xp -= threshold
            master_level = min(MASTER_MAX_LEVEL, master_level + 1)
            continue

        threshold = level_threshold(level)
        if xp < threshold:
            break
        xp -= threshold
        if level < BASE_MAX_LEVEL:
            level += 1
            continue
        if not prestige_unlocked:
            prestige_unlocked = True
            prestige = 1
            level = 1
            continue
        if prestige < PRESTIGE_MAX:
            prestige += 1
            level = 1
            continue
        master = True
        master_level = 1
        continue

    stats["xp"] = xp
    stats["level"] = level
    stats["prestige"] = prestige
    stats["prestige_unlocked"] = prestige_unlocked
    stats["master_prestige"] = master
    stats["master_level"] = master_level


def progress_state(stats, xp_gain=0):
    # Preview progress without mutating stats.
    snapshot = {
        "xp": int(stats.get("xp", 0)),
        "prestige": int(stats.get("prestige", 0)),
        "prestige_unlocked": bool(stats.get("prestige_unlocked", False)),
        "master_prestige": bool(stats.get("master_prestige", False)),
        "master_level": int(stats.get("master_level", 1)),
        "level": int(stats.get("level", 1)),
    }
    apply_xp_and_progress(snapshot, xp_gain)
    if snapshot.get("master_prestige"):
        return {
            "level": int(snapshot.get("level", 1)),
            "xp_into": int(snapshot.get("xp", 0)),
            "xp_needed": 1_000_000,
            "prestige": int(snapshot.get("prestige", 0)),
            "master": True,
            "master_level": int(snapshot.get("master_level", 1)),
        }
    level = int(snapshot.get("level", 1))
    return {
        "level": level,
        "xp_into": int(snapshot.get("xp", 0)),
        "xp_needed": level_threshold(level),
        "prestige": int(snapshot.get("prestige", 0)),
        "master": False,
        "master_level": int(snapshot.get("master_level", 1)),
        "prestige_unlocked": bool(snapshot.get("prestige_unlocked", False)),
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

def weapon_category(weapon_name):
    # Map a weapon to its configured category.
    for category, weapons in WEAPON_CATEGORIES.items():
        if weapon_name in weapons:
            return category
    return None


def rank_color(name):
    # Resolve a rank name to a display color.
    return RANK_COLORS.get(name, "#5b5b5b")


def get_total_play_time(timer_state):
    # Combine stored elapsed time with current session runtime.
    elapsed = timer_state.get("elapsed", 0)
    if timer_state.get("running"):
        elapsed += int(time.monotonic() - timer_state.get("start", time.monotonic()))
    return elapsed


def clear_frame(frame):
    # Remove all children from a container frame.
    for widget in frame.winfo_children():
        widget.destroy()


NOTIFY_CALLBACK = None


def notify(message):
    # Send an in-window notification when available.
    if NOTIFY_CALLBACK:
        NOTIFY_CALLBACK(message)


def calculate_rates(attributes):
    # Derive kills/deaths rates from player attributes.
    total = sum(attributes.values())
    max_total = ATTRIBUTE_MAX * len(ATTRIBUTES)
    skill = total / max_total if max_total else 0.0
    kills_per_min = 2 + 7 * skill
    deaths_per_min = 6 - 5 * skill
    return kills_per_min / 60.0, deaths_per_min / 60.0


def build_match_rosters(player_name):
    # Create simulated teammate and enemy rosters with randomized skills.
    teammates = []
    teammate_count = max(1, PLAYER_TEAM_SIZE) - 1
    teammate_names = list(TEAMMATE_NAME_POOL)
    random.shuffle(teammate_names)
    for idx in range(1, teammate_count + 1):
        name = teammate_names.pop() if teammate_names else f"Teammate {idx}"
        teammates.append(
            {
                "name": name,
                "skill": random.uniform(*AI_SKILL_RANGE),
                "kills": 0,
                "deaths": 0,
                "is_player": False,
            }
        )
    enemies = []
    enemy_names = list(ENEMY_NAME_POOL)
    random.shuffle(enemy_names)
    for idx in range(1, max(1, ENEMY_TEAM_SIZE) + 1):
        name = enemy_names.pop() if enemy_names else f"Enemy {idx}"
        enemies.append(
            {
                "name": name,
                "skill": random.uniform(*AI_SKILL_RANGE),
                "kills": 0,
                "deaths": 0,
                "is_player": False,
            }
        )
    player_entry = {
        "name": player_name,
        "skill": 1.0,
        "kills": 0,
        "deaths": 0,
        "is_player": True,
    }
    return [player_entry] + teammates, enemies, player_entry


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
    if key.startswith("weapon_kills:"):
        weapon_name = key.split(":", 1)[1]
        weapons = stats.get("weapons", {})
        weapon_stats = weapons.get(weapon_name, {})
        return int(weapon_stats.get("kills", 0))
    if key == "xp_total":
        return int(stats.get("lifetime_xp", stats.get("xp", 0)))
    if key == "play_time_seconds":
        return int(profile["player"].get("play_time_seconds", 0))
    return int(stats.get(key, 0))


def achievement_base_and_level(achievement_id):
    # Split a level-suffixed achievement id into base id and level.
    parts = achievement_id.rsplit("_l", 1)
    if len(parts) == 2 and parts[1].isdigit():
        return parts[0], int(parts[1])
    return achievement_id, 1


def check_achievements(profile):
    # Award new achievements and return bonus XP gained.
    stats = ensure_stats(profile)
    earned = stats.setdefault("achievements", {})
    bonus_xp = 0
    grouped = {}
    for entry in ACHIEVEMENTS:
        base_id, level = achievement_base_and_level(entry[0])
        grouped.setdefault(base_id, []).append((level, entry))
    for base_id, levels in grouped.items():
        levels.sort(key=lambda item: item[0])
        next_entry = None
        for _, entry in levels:
            if not earned.get(entry[0]):
                next_entry = entry
                break
        if not next_entry:
            continue
        ach_id, name, key, threshold, reward_xp, description = next_entry
        value = achievement_value(profile, key)
        if value >= threshold:
            earned[ach_id] = True
            bonus_xp += reward_xp
    return bonus_xp


def ensure_stats(profile):
    # Ensure the profile stats dict contains required keys.
    stats = profile["player"].setdefault(
        "stats",
        {
            "games_played": 0,
            "game_modes_played": {},
            "game_mode_wins": {},
            "game_mode_losses": {},
            "maps_played": {},
            "kills": 0,
            "deaths": 0,
            "wins": 0,
            "losses": 0,
            "longest_kill_streak": 0,
            "headshots": 0,
            "xp": 0,
            "lifetime_xp": 0,
            "level": 1,
            "prestige_unlocked": False,
            "prestige": 0,
            "master_prestige": False,
            "master_level": 1,
            "weapons": {},
            "UAV_calls": 0,
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
            "match_history": [],
        },
    )
    if "lifetime_xp" not in stats:
        stats["lifetime_xp"] = int(stats.get("xp", 0))
    return stats


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
    UAV_calls = 0
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
                UAV_calls += 1
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
    mode_wins = stats.setdefault("game_mode_wins", {})
    mode_losses = stats.setdefault("game_mode_losses", {})

    maps = stats.setdefault("maps_played", {})
    for _ in range(completed_matches):
        name = random.choice(MAP_POOL)
        maps[name] = int(maps.get(name, 0)) + 1
        # Simulate match outcomes per completed offline match.
        skill = sum(attributes.values()) / (ATTRIBUTE_MAX * len(ATTRIBUTES)) if attributes else 0.5
        win_chance = 0.45 + 0.4 * skill
        if random.random() < win_chance:
            stats["wins"] = int(stats.get("wins", 0)) + 1
            mode_wins[mode] = int(mode_wins.get(mode, 0)) + 1
        else:
            stats["losses"] = int(stats.get("losses", 0)) + 1
            mode_losses[mode] = int(mode_losses.get(mode, 0)) + 1

    stats["UAV_calls"] = int(stats.get("UAV_calls", 0)) + UAV_calls
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
    stats["lifetime_xp"] = int(stats.get("lifetime_xp", 0)) + int(xp_gain)
    apply_xp_and_progress(stats, xp_gain)
    bonus = check_achievements(profile)
    if bonus:
        stats["lifetime_xp"] = int(stats.get("lifetime_xp", 0)) + int(bonus)
        apply_xp_and_progress(stats, bonus)

    weapons = stats.setdefault("weapons", {})
    weapon_stats = weapons.setdefault(
        weapon,
        {"xp": 0, "level": 1, "headshots": 0, "camo": "None", "kills": 0},
    )
    weapon_stats["xp"] = int(weapon_stats.get("xp", 0)) + xp_gain + headshots * 5
    weapon_stats["level"] = level_progress(weapon_stats["xp"])[0]
    weapon_stats["headshots"] = int(weapon_stats.get("headshots", 0)) + headshots
    weapon_stats["kills"] = int(weapon_stats.get("kills", 0)) + kills
    weapon_stats["camo"] = get_camo_for_headshots(profile, weapon, weapon_stats["headshots"])
    refresh_all_weapon_camos(profile)

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
    stats["lifetime_xp"] = int(stats.get("lifetime_xp", 0)) + int(xp_gain)
    apply_xp_and_progress(stats, xp_gain)


def base_camo_for_headshots(headshot_count):
    # Resolve the highest camo unlocked for the given headshot count.
    camo = "None"
    for requirement, name in CAMO_UNLOCKS:
        if headshot_count >= requirement:
            camo = name
    return camo


def camo_rank(name):
    # Convert camo names into an ordered rank value.
    return CAMO_RANK.get(name, 0)


def cap_camo(camo_name, max_name):
    # Clamp a camo name to a maximum allowed tier.
    if camo_rank(camo_name) > camo_rank(max_name):
        return max_name
    return camo_name


def category_lower_camos_complete(profile, category):
    # Check if every weapon in a category has unlocked all lower camos.
    stats = ensure_stats(profile)
    weapons = stats.get("weapons", {})
    for weapon in WEAPON_CATEGORIES.get(category, ()):
        headshots = int(weapons.get(weapon, {}).get("headshots", 0))
        if camo_rank(base_camo_for_headshots(headshots)) < camo_rank("Obsidian"):
            return False
    return True


def category_has_camo_at_least(profile, category, camo_name):
    # See if any weapon in the category has reached the requested camo tier.
    stats = ensure_stats(profile)
    weapons = stats.get("weapons", {})
    for weapon in WEAPON_CATEGORIES.get(category, ()):
        headshots = int(weapons.get(weapon, {}).get("headshots", 0))
        if camo_rank(base_camo_for_headshots(headshots)) >= camo_rank(camo_name):
            return True
    return False


def all_categories_have_camo_at_least(profile, camo_name):
    # Require at least one weapon per category at the camo tier or higher.
    for category in WEAPON_CATEGORIES:
        if not category_has_camo_at_least(profile, category, camo_name):
            return False
    return True


def all_weapons_have_camo_at_least(profile, camo_name):
    # Require every weapon to reach the camo tier or higher.
    stats = ensure_stats(profile)
    weapons = stats.get("weapons", {})
    for weapon in WEAPON_POOL:
        headshots = int(weapons.get(weapon, {}).get("headshots", 0))
        if camo_rank(base_camo_for_headshots(headshots)) < camo_rank(camo_name):
            return False
    return True


def refresh_all_weapon_camos(profile):
    # Re-evaluate camo gates across every weapon.
    stats = ensure_stats(profile)
    weapons = stats.get("weapons", {})
    for weapon_name, weapon_stats in weapons.items():
        headshots = int(weapon_stats.get("headshots", 0))
        weapon_stats["camo"] = get_camo_for_headshots(profile, weapon_name, headshots)


def get_camo_for_headshots(profile, weapon_name, headshot_count):
    # Resolve the highest camo unlocked, respecting category gates.
    camo = base_camo_for_headshots(headshot_count)
    category = weapon_category(weapon_name)

    if camo in ("Gold", "Platinum", "Diamond", "Singularity") and category:
        if not category_lower_camos_complete(profile, category):
            return cap_camo(camo, "Obsidian")

    if camo in ("Platinum", "Diamond", "Singularity"):
        if not all_categories_have_camo_at_least(profile, "Gold"):
            return "Gold"

    if camo in ("Diamond", "Singularity"):
        if not all_weapons_have_camo_at_least(profile, "Platinum"):
            return "Platinum"

    if camo == "Singularity":
        if not all_weapons_have_camo_at_least(profile, "Diamond"):
            return "Diamond"

    return camo


def award_weapon_xp(loaded_profile, weapon_name, xp_gain, headshots=0, kills=0):
    # Track per-weapon progression and camo unlocks.
    stats = loaded_profile["player"].setdefault("stats", {})
    weapons = stats.setdefault("weapons", {})
    weapon = weapons.setdefault(
        weapon_name,
        {"xp": 0, "level": 1, "headshots": 0, "camo": "None", "kills": 0},
    )
    weapon["xp"] = int(weapon.get("xp", 0)) + int(xp_gain)
    weapon["level"] = level_progress(weapon["xp"])[0]
    weapon["headshots"] = int(weapon.get("headshots", 0)) + int(headshots)
    weapon["kills"] = int(weapon.get("kills", 0)) + int(kills)
    weapon["camo"] = get_camo_for_headshots(loaded_profile, weapon_name, weapon["headshots"])
    refresh_all_weapon_camos(loaded_profile)


def trigger_nuke(session_state, stats, now, schedule_end, force=False):
    # Trigger a nuclear victory and end the match shortly after.
    if "nuke" in session_state.get("reward_flags", set()) and not force and not session_state.get("pending_nuke"):
        return
    session_state["streak_rewards"]["nuke"] = now
    session_state["reward_flags"].add("nuke")
    session_state["nuke_until"] = now + 3
    session_state["kills"] += 6
    session_state["xp_bonus"] += 6 * 10
    team_kills = session_state.get("team_kills")
    if team_kills:
        team_kills["player"] += 6
    if session_state.get("player_entry"):
        session_state["player_entry"]["kills"] += 6
    game_mode = session_state.get("game_mode")
    if game_mode == "Free for all":
        roster = session_state.get("teams", {}).get("player_team", [])
        targets = [entry for entry in roster if not entry.get("is_player")]
    else:
        targets = session_state.get("teams", {}).get("enemy_team", [])
    for _ in range(6):
        if targets:
            random.choice(targets)["deaths"] += 1
    session_state["end_time"] = session_state["nuke_until"]
    schedule_end(int((session_state["nuke_until"] - now) * 1000))


def close_nuke_prompt(session_state):
    # Close the nuke prompt if it's open.
    prompt = session_state.get("nuke_prompt_frame")
    if prompt:
        prompt.pack_forget()
    session_state["nuke_prompt_payload"] = None


def show_nuke_prompt(root, session_state, stats, schedule_end):
    # Prompt the player to accept a nuclear victory without pausing the match.
    if session_state.get("nuke_prompt_payload") is not None:
        return
    session_state["nuke_prompt_payload"] = (stats, schedule_end)
    prompt = session_state.get("nuke_prompt_frame")
    if prompt:
        prompt.pack(fill="x", padx=12, pady=(12, 6))


def start_doomguy_animation(root, session_state):
    # Create a small animated scene while a game is running.
    canvas = session_state.get("match_canvas")
    if canvas is None:
        container = session_state.get("match_container")
        if container is None:
            return
        canvas = tk.Canvas(container, width=320, height=240, bg="#101820", highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        session_state["match_canvas"] = canvas
    session_state["anim_canvas"] = canvas
    session_state["anim_frame"] = 0
    session_state["enemy_hitboxes"] = []

    def on_click(event):
        if session_state.get("phase") != "playing":
            return
        now = time.monotonic()
        if now < session_state.get("respawn_until", 0):
            return
        if now < session_state.get("click_lock_until", 0):
            return
        hitboxes = session_state.get("enemy_hitboxes", [])
        for idx, (x, y, r) in enumerate(hitboxes):
            if (event.x - x) ** 2 + (event.y - y) ** 2 <= r ** 2:
                handler = session_state.get("apply_player_kill")
                attributes = session_state.get("attributes", {})
                if handler:
                    effects = compute_attribute_effects(attributes, session_state.get("options"))
                    handler(1, [idx], effects, now)
                    session_state["enemy_hitboxes"] = []
                    session_state["click_lock_until"] = now + 0.25
                break

    canvas.bind("<Button-1>", on_click)

    def draw_scene():
        if session_state.get("phase") != "playing" or session_state.get("anim_canvas") is None:
            return
        frame = session_state.get("anim_frame", 0)
        canvas.delete("all")
        scorebar_height = 24
        offset_y = scorebar_height
        team_scores = session_state.get("team_scores", {"player": 0, "enemy": 0})

        canvas.create_rectangle(0, 0, 320, scorebar_height, fill="#151c28", outline="")
        if session_state.get("game_mode") == "Free for all":
            left_label = "You"
            right_label = "Leader"
        else:
            left_label = "Your Team"
            right_label = "Enemy"
        canvas.create_text(
            8,
            scorebar_height // 2,
            text=f"{left_label}: {int(team_scores.get('player', 0))}",
            fill="#c9d4e2",
            font=("Segoe UI", 9),
            anchor="w",
        )
        canvas.create_text(
            312,
            scorebar_height // 2,
            text=f"{right_label}: {int(team_scores.get('enemy', 0))}",
            fill="#f0b1b1",
            font=("Segoe UI", 9),
            anchor="e",
        )
        if session_state.get("game_mode") == "Domination":
            control_points = session_state.get("control_points", [])
            colors = {"player": "#6bd98a", "enemy": "#f07070", None: "#5b5b5b"}
            labels = ["A", "B", "C"]
            start_x = 130
            for idx, label in enumerate(labels):
                point = control_points[idx] if idx < len(control_points) else {"owner": None}
                owner = point.get("owner")
                x = start_x + idx * 24
                canvas.create_oval(x, 6, x + 10, 16, fill=colors.get(owner, "#5b5b5b"), outline="")
                canvas.create_text(x + 5, 18, text=label, fill="#c9d4e2", font=("Segoe UI", 7))

        # Simple pseudo-3D corridor.
        canvas.create_rectangle(0, offset_y, 320, offset_y + 80, fill="#1a2636", outline="")
        canvas.create_polygon(
            0,
            offset_y + 80,
            320,
            offset_y + 80,
            260,
            offset_y + 200,
            60,
            offset_y + 200,
            fill="#0d131a",
            outline="",
        )
        for i in range(6):
            offset = (frame * 6 + i * 40) % 240
            left = 60 + offset * 0.3
            right = 260 - offset * 0.3
            y = offset_y + 80 + offset * 0.5
            canvas.create_line(left, y, right, y, fill="#243447")

        # Enemies to pick from (always visible).
        positions = [
            (60, offset_y + 130),
            (160, offset_y + 130),
            (260, offset_y + 130),
            (80, offset_y + 160),
            (160, offset_y + 170),
            (240, offset_y + 160),
        ]
        enemies = session_state.get("encounter_enemies", [])
        last_kill_time = session_state.get("last_kill_time", 0)
        flash_hit = time.monotonic() - last_kill_time < 0.6
        hit_indices = set(session_state.get("last_kill_indices", [])) if flash_hit else set()

        hitboxes = []
        for idx, name in enumerate(enemies):
            ex, ey = positions[idx % len(positions)]
            hitboxes.append((ex, ey, 10))
            # Enemy with shadow and highlight for depth.
            canvas.create_oval(ex - 8, ey + 6, ex + 8, ey + 10, fill="#1a1212", outline="")
            canvas.create_oval(ex - 10, ey - 10, ex + 10, ey + 10, fill="#8b2d2d", outline="")
            canvas.create_oval(ex - 6, ey - 8, ex + 2, ey, fill="#a94343", outline="")
            if idx in hit_indices:
                canvas.create_oval(ex - 16, ey - 16, ex + 16, ey + 16, outline="#f0d24b", width=2)
                canvas.create_line(ex - 6, ey, ex - 2, ey, fill="#f0d24b", width=2)
                canvas.create_line(ex + 2, ey, ex + 6, ey, fill="#f0d24b", width=2)
                canvas.create_line(ex, ey - 6, ex, ey - 2, fill="#f0d24b", width=2)
                canvas.create_line(ex, ey + 2, ex, ey + 6, fill="#f0d24b", width=2)
            canvas.create_text(ex, ey + 16, text=name, fill="#c0c0c0", font=("Segoe UI", 7))
        session_state["enemy_hitboxes"] = hitboxes

        # Doomguy stick figure with a simple walk cycle.
        respawn_until = session_state.get("respawn_until", 0)
        if time.monotonic() >= respawn_until:
            bob = 2 if frame % 10 < 5 else 0
            x = 160 + (frame % 40 - 20) * 0.6
            y = offset_y + 120 + bob
            # Ground shadow.
            canvas.create_oval(x - 12, y + 26, x + 12, y + 32, fill="#0f1118", outline="")
            # Head with highlight.
            canvas.create_oval(x - 8, y - 18, x + 8, y - 2, fill="#c89b6d", outline="")
            canvas.create_oval(x - 6, y - 16, x - 1, y - 9, fill="#deb894", outline="")
            # Torso with shading.
            canvas.create_line(x, y - 2, x, y + 20, fill="#c95738", width=4)
            canvas.create_line(x + 2, y - 2, x + 2, y + 20, fill="#a7462f", width=2)
            # Legs with depth.
            leg_offset = 6 if frame % 10 < 5 else -6
            canvas.create_line(x, y + 20, x - 6, y + 36 + leg_offset, fill="#7b3f2a", width=3)
            canvas.create_line(x, y + 20, x + 6, y + 36 - leg_offset, fill="#5f2e1f", width=3)
            # Arms with slight highlight.
            canvas.create_line(x - 10, y + 6, x + 10, y + 10, fill="#c95738", width=3)
            canvas.create_line(x - 10, y + 7, x + 10, y + 11, fill="#b14c35", width=1)

        # Kill feedback.
        if time.monotonic() - last_kill_time < 1.0:
            kill_count = session_state.get("last_kill_count", 1)
            label = "Eliminated enemy!" if kill_count == 1 else f"Eliminated {kill_count} enemies!"
            canvas.create_text(160, offset_y + 20, text=label, fill="#f0d24b", font=("Segoe UI", 10))

        # Death/respawn feedback.
        if time.monotonic() < respawn_until:
            seconds_left = max(1, int(respawn_until - time.monotonic()))
            canvas.create_text(
                160,
                offset_y + 40,
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
            canvas.create_text(
                10,
                offset_y + 12 + idx * 12,
                text=text,
                fill="#d5e3f0",
                font=("Segoe UI", 8),
                anchor="w",
            )

        # Streak rewards visuals.
        now = time.monotonic()
        rewards = session_state.get("streak_rewards", {})

        nuke_until = session_state.get("nuke_until", 0)
        if now < nuke_until:
            radius = 30 + (1 - (nuke_until - now) / 3.0) * 120
            canvas.create_oval(
                160 - radius,
                offset_y + 100 - radius,
                160 + radius,
                offset_y + 100 + radius,
                fill="#f4b33a",
                outline="",
            )
            canvas.create_oval(
                160 - radius * 1.1,
                offset_y + 100 - radius * 1.1,
                160 + radius * 1.1,
                offset_y + 100 + radius * 1.1,
                outline="#ffd37a",
                width=2,
            )
            canvas.create_oval(
                160 - radius * 0.7,
                offset_y + 100 - radius * 0.7,
                160 + radius * 0.7,
                offset_y + 100 + radius * 0.7,
                fill="#ff6b3a",
                outline="",
            )
            canvas.create_text(160, offset_y + 100, text="NUCLEAR VICTORY", fill="#ffffff", font=("Segoe UI", 12))

        UAV_start = rewards.get("UAV")
        if UAV_start:
            elapsed = now - UAV_start
            if elapsed <= 3.0:
                pulse = int(elapsed // 1.0)
                progress = (elapsed % 1.0) / 1.0
                radius = 20 + progress * 90
                alpha = int(255 * (1 - progress))
                color = f"#{alpha:02x}ff{alpha:02x}"
                canvas.create_oval(
                    160 - radius,
                    offset_y + 100 - radius,
                    160 + radius,
                    offset_y + 100 + radius,
                    outline=color,
                    width=2,
                )
                canvas.create_oval(
                    160 - radius * 0.7,
                    offset_y + 100 - radius * 0.7,
                    160 + radius * 0.7,
                    offset_y + 100 + radius * 0.7,
                    outline="#7fc7ff",
                    width=1,
                )
                canvas.create_text(160, offset_y + 70, text="UAV Sweep", fill="#9ad1ff", font=("Segoe UI", 9))
            else:
                session_state["streak_rewards"]["UAV"] = None

        air_start = rewards.get("airstrike")
        if air_start:
            elapsed = now - air_start
            if elapsed <= 3.0:
                x = -40 + (elapsed / 3.0) * 400
                y = offset_y + 30
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
                canvas.create_polygon(
                    x - 10,
                    y + 8,
                    x + 8,
                    y + 12,
                    x - 10,
                    y + 16,
                    fill="#8da0b0",
                    outline="",
                )
                canvas.create_text(160, offset_y + 55, text="Airstrike inbound", fill="#f4c542", font=("Segoe UI", 9))
            else:
                session_state["streak_rewards"]["airstrike"] = None

        heli_start = rewards.get("helicopter")
        if heli_start:
            elapsed = now - heli_start
            if elapsed <= 8.0:
                x = 30 + (elapsed / 8.0) * 240
                y = offset_y + 40
                canvas.create_rectangle(x, y, x + 40, y + 14, fill="#6b8c8e", outline="")
                canvas.create_rectangle(x, y + 8, x + 40, y + 14, fill="#4f6a6b", outline="")
                canvas.create_rectangle(x + 10, y - 8, x + 30, y, fill="#6b8c8e", outline="")
                rotor_offset = 6 if int(elapsed * 10) % 2 == 0 else -6
                canvas.create_line(x + 20 - 14, y - 10, x + 20 + 14, y - 10, fill="#d0d7de", width=2)
                canvas.create_line(x + 20, y - 10 - rotor_offset, x + 20, y - 10 + rotor_offset, fill="#d0d7de", width=2)
                canvas.create_oval(x - 6, y + 6, x + 6, y + 16, fill="#263338", outline="")
                canvas.create_text(160, offset_y + 75, text="Helicopter support", fill="#8ef5b3", font=("Segoe UI", 9))
            else:
                session_state["streak_rewards"]["helicopter"] = None

        session_state["anim_frame"] = frame + 1
        session_state["anim_after_id"] = root.after(80, draw_scene)

    draw_scene()


def start_lobby_view(root, session_state, wait_seconds):
    # Show a lobby roster that fills in over the waiting period.
    canvas = session_state.get("match_canvas")
    if canvas is None:
        container = session_state.get("match_container")
        if container is None:
            return
        canvas = tk.Canvas(container, width=320, height=240, bg="#101820", highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        session_state["match_canvas"] = canvas
    session_state["anim_canvas"] = canvas
    session_state["anim_frame"] = 0
    session_state["lobby_start"] = time.monotonic()
    session_state["lobby_duration"] = max(1, int(wait_seconds))
    roster = session_state.get("next_match_roster", {})
    fill_order = []
    for entry in roster.get("player_team", []):
        fill_order.append(("player", entry.get("name", "Unknown")))
    for entry in roster.get("enemy_team", []):
        fill_order.append(("enemy", entry.get("name", "Unknown")))
    random.shuffle(fill_order)
    session_state["lobby_fill_order"] = fill_order

    def draw_lobby():
        if session_state.get("phase") != "waiting" or session_state.get("anim_canvas") is None:
            return
        canvas.delete("all")
        now = time.monotonic()
        elapsed = now - session_state.get("lobby_start", now)
        duration = max(1, session_state.get("lobby_duration", 1))
        progress = min(1.0, elapsed / duration)

        roster = session_state.get("next_match_roster", {})
        player_team = roster.get("player_team", [])
        enemy_team = roster.get("enemy_team", [])
        total_players = len(player_team) + len(enemy_team)
        visible_count = int(round(total_players * progress))
        fill_order = session_state.get("lobby_fill_order", [])
        visible_entries = fill_order[:visible_count]
        player_names = [name for team, name in visible_entries if team == "player"]
        enemy_names = [name for team, name in visible_entries if team == "enemy"]

        canvas.create_text(160, 16, text="Loading Lobby...", fill="#c9d4e2", font=("Segoe UI", 11))
        canvas.create_text(
            160,
            36,
            text=f"{int(progress * 100)}% Ready",
            fill="#7fc7ff",
            font=("Segoe UI", 9),
        )
        canvas.create_line(12, 48, 308, 48, fill="#243447")

        left_x = 20
        right_x = 180
        y_start = 60
        line_height = 18
        canvas.create_text(left_x, y_start - 14, text="Your Team", fill="#6bd98a", anchor="w", font=("Segoe UI", 9))
        for idx, name in enumerate(player_names):
            canvas.create_text(left_x, y_start + idx * line_height, text=name, fill="#c9d4e2", anchor="w")

        canvas.create_text(
            right_x,
            y_start - 14,
            text="Enemy Team",
            fill="#f07070",
            anchor="w",
            font=("Segoe UI", 9),
        )
        for e_idx, name in enumerate(enemy_names):
            canvas.create_text(right_x, y_start + e_idx * line_height, text=name, fill="#c9d4e2", anchor="w")

        session_state["anim_after_id"] = root.after(200, draw_lobby)

    draw_lobby()


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
    session_state["after_id"] = None
    session_state["ticker_id"] = None
    session_state["anim_after_id"] = None
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
    session_state["anim_canvas"] = None
    session_state["anim_frame"] = 0
    session_state["phase"] = "waiting"
    wait_seconds = random.randint(12, 55)
    if loaded_profile:
        player_name = loaded_profile["player"].get("gamertag", "Player")
        player_team, enemy_team, player_entry = build_match_rosters(player_name)
        session_state["next_match_roster"] = {
            "player_team": player_team,
            "enemy_team": enemy_team,
            "player_entry": player_entry,
        }
    start_lobby_view(root, session_state, wait_seconds)
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
    if game_mode == "Domination":
        duration_seconds = 14 * 60
    else:
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
    anim_after_id = session_state.get("anim_after_id")
    if anim_after_id:
        root.after_cancel(anim_after_id)
        session_state["anim_after_id"] = None
    session_state["anim_canvas"] = None
    session_state["anim_frame"] = 0

    session_state["player_name"] = loaded_profile["player"].get("gamertag", "Player")
    next_roster = session_state.pop("next_match_roster", None)
    if next_roster:
        player_team = next_roster.get("player_team", [])
        enemy_team = next_roster.get("enemy_team", [])
        player_entry = next_roster.get("player_entry")
    else:
        player_team, enemy_team, player_entry = build_match_rosters(session_state["player_name"])
    if game_mode == "Free for all":
        combined = player_team + enemy_team
        player_team = combined
        enemy_team = []
    session_state["teams"] = {"player_team": player_team, "enemy_team": enemy_team}
    session_state["player_entry"] = player_entry
    session_state["team_kills"] = {"player": 0, "enemy": 0}
    session_state["team_scores"] = {"player": 0.0, "enemy": 0.0}
    session_state["game_mode"] = game_mode
    if game_mode == "Domination":
        session_state["control_points"] = [
            {"name": "A", "owner": None, "owner_name": None},
            {"name": "B", "owner": None, "owner_name": None},
            {"name": "C", "owner": None, "owner_name": None},
        ]
        session_state["last_point_tick"] = time.monotonic()
        session_state["next_capture_time"] = time.monotonic() + random.randint(3, 7)
    else:
        session_state["control_points"] = []
    session_state["options"] = loaded_profile["player"].get("options", {})
    session_state["streak_rewards"] = {"UAV": None, "airstrike": None, "helicopter": None, "nuke": None}
    session_state["reward_flags"] = set()
    session_state["xp_bonus"] = 0
    session_state["UAV_bonus_until"] = 0.0
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
        "UAV": {},
        "airstrike": {},
        "helicopter": {},
        "nuke": {},
        "score": {},
    }
    session_state["totals"] = {
        "kills": 0,
        "deaths": 0,
        "headshots": 0,
        "UAV": 0,
        "airstrike": 0,
        "helicopter": 0,
        "nuke": 0,
        "score": 0,
    }
    session_state["encounter_enemies"] = random.choices(ENEMY_POOL, k=random.randint(1, 6))
    session_state["encounter_last_update"] = time.monotonic()
    session_state["weapon_name"] = defaults.get("weapon", "Ak-47")
    session_state["attributes"] = attributes
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
        summary = {
            "mode": defaults.get("game_mode", "Team death match"),
            "map": map_name,
            "weapon": session_state.get("weapon_name", WEAPON_POOL[0]),
            "kills": session_state["kills"],
            "deaths": session_state["deaths"],
            "headshots": session_state.get("headshots", 0),
            "longest_streak": session_state["longest_streak"],
            "xp_bonus": session_state.get("xp_bonus", 0),
        }
        summary["team_scores"] = {
            "player": int(session_state.get("team_scores", {}).get("player", 0)),
            "enemy": int(session_state.get("team_scores", {}).get("enemy", 0)),
        }
        teams = session_state.get("teams", {})
        summary["scoreboard"] = {
            "player_team": [
                {"name": entry.get("name"), "kills": entry.get("kills", 0), "deaths": entry.get("deaths", 0)}
                for entry in teams.get("player_team", [])
            ],
            "enemy_team": [
                {"name": entry.get("name"), "kills": entry.get("kills", 0), "deaths": entry.get("deaths", 0)}
                for entry in teams.get("enemy_team", [])
            ],
        }
        if game_mode == "Free for all":
            player_entry = session_state.get("player_entry")
            all_players = summary["scoreboard"]["player_team"]
            best_entry = max(all_players, key=lambda entry: entry.get("kills", 0), default=None)
            best_kills = best_entry.get("kills", 0) if best_entry else 0
            player_kills = player_entry.get("kills", 0) if player_entry else 0
            summary["team_scores"] = {"player": best_kills, "enemy": 0}
            summary["scoreboard"]["enemy_team"] = []
            summary["result"] = "Win" if player_kills >= best_kills else "Loss"
            summary["winner_name"] = best_entry.get("name") if best_entry else "Unknown"
        else:
            summary["result"] = (
                "Win" if summary["team_scores"].get("player", 0) >= summary["team_scores"].get("enemy", 0) else "Loss"
            )
        base_xp_gain = compute_xp_gain(
            session_state["kills"],
            session_state.get("headshots", 0),
            True,
        )
        bonus_xp = summary["xp_bonus"]
        win_multiplier = 2 if summary["result"] == "Win" else 1
        xp_gain = (base_xp_gain + bonus_xp) * win_multiplier
        summary["xp_gain"] = base_xp_gain
        summary["xp_total"] = xp_gain
        add_kill_death_stats(
            loaded_profile,
            session_state["kills"],
            session_state["deaths"],
            session_state.get("headshots", 0),
        )
        match_stats = ensure_stats(loaded_profile)
        if summary["result"] == "Win":
            match_stats["wins"] = int(match_stats.get("wins", 0)) + 1
            mode_wins = match_stats.setdefault("game_mode_wins", {})
            mode_wins[game_mode] = int(mode_wins.get(game_mode, 0)) + 1
        else:
            match_stats["losses"] = int(match_stats.get("losses", 0)) + 1
            mode_losses = match_stats.setdefault("game_mode_losses", {})
            mode_losses[game_mode] = int(mode_losses.get(game_mode, 0)) + 1
        award_xp(
            loaded_profile,
            xp_gain,
        )
        award_weapon_xp(
            loaded_profile,
            session_state.get("weapon_name", "Ak-47"),
            (base_xp_gain + bonus_xp) * win_multiplier + session_state.get("headshots", 0) * 5,
            session_state.get("headshots", 0),
            session_state.get("kills", 0),
        )
        bonus = check_achievements(loaded_profile)
        if bonus:
            award_xp(loaded_profile, bonus)
        loaded_profile["player"]["stats"].update({"longest_kill_streak": session_state["longest_streak"]})
        stats = ensure_stats(loaded_profile)
        history = stats.setdefault("match_history", [])
        history.insert(0, summary)
        del history[10:]
        save_profile_data(loaded_profile, save_path)
        refresh = session_state.get("ribbon_refresh_callback")
        if refresh:
            refresh()
        profile_refresh = session_state.get("profile_refresh_callback")
        if profile_refresh:
            profile_refresh()
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
        open_match_summary(summary, session_state)

    def schedule_end(delay_ms):
        if session_state.get("after_id"):
            root.after_cancel(session_state["after_id"])
        session_state["after_id"] = root.after(delay_ms, end_match)

    def apply_player_kill(kill_count, kill_indices, effects, now):
        if kill_indices:
            kill_count = len(kill_indices)
        if kill_count <= 0:
            return
        encounter = session_state.get("encounter_enemies", [])
        session_state["kills"] += kill_count
        session_state["totals"]["kills"] += kill_count
        session_state["current_streak"] += kill_count
        session_state["team_kills"]["player"] += kill_count
        if session_state.get("player_entry"):
            session_state["player_entry"]["kills"] += kill_count
        if game_mode == "Free for all":
            roster = session_state.get("teams", {}).get("player_team", [])
            targets = [entry for entry in roster if not entry.get("is_player")]
        else:
            targets = session_state.get("teams", {}).get("enemy_team", [])
        for _ in range(kill_count):
            if targets:
                random.choice(targets)["deaths"] += 1
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
        if now < session_state.get("UAV_bonus_until", 0):
            session_state["xp_bonus"] += kill_count * 5
            minute = int((now - session_state["match_start"]) // 60)
            bonus = kill_count * 5
            session_state["timeline"]["score"][minute] = session_state["timeline"]["score"].get(minute, 0) + bonus
            session_state["totals"]["score"] += bonus
        session_state["encounter_enemies"] = random.choices(ENEMY_POOL, k=random.randint(1, 6))
        session_state["encounter_last_update"] = now
        if session_state["current_streak"] >= 3 and "UAV" not in session_state["reward_flags"]:
            session_state["streak_rewards"]["UAV"] = now
            session_state["reward_flags"].add("UAV")
            session_state["UAV_bonus_until"] = now + 12
            stats["UAV_calls"] = int(stats.get("UAV_calls", 0)) + 1
            session_state["totals"]["UAV"] += 1
            minute = int((now - session_state["match_start"]) // 60)
            session_state["timeline"]["UAV"][minute] = session_state["timeline"]["UAV"].get(minute, 0) + 1
        if session_state["current_streak"] >= 5 and "airstrike" not in session_state["reward_flags"]:
            session_state["streak_rewards"]["airstrike"] = now
            session_state["reward_flags"].add("airstrike")
            air_kills = random.randint(0, 6)
            session_state["kills"] += air_kills
            session_state["totals"]["kills"] += air_kills
            session_state["team_kills"]["player"] += air_kills
            if session_state.get("player_entry"):
                session_state["player_entry"]["kills"] += air_kills
            if game_mode == "Free for all":
                roster = session_state.get("teams", {}).get("player_team", [])
                targets = [entry for entry in roster if not entry.get("is_player")]
            else:
                targets = session_state.get("teams", {}).get("enemy_team", [])
            for _ in range(air_kills):
                if targets:
                    random.choice(targets)["deaths"] += 1
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
            session_state["team_kills"]["player"] += extra_kills
            if session_state.get("player_entry"):
                session_state["player_entry"]["kills"] += extra_kills
            if game_mode == "Free for all":
                roster = session_state.get("teams", {}).get("player_team", [])
                targets = [entry for entry in roster if not entry.get("is_player")]
            else:
                targets = session_state.get("teams", {}).get("enemy_team", [])
            for _ in range(extra_kills):
                if targets:
                    random.choice(targets)["deaths"] += 1
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

    session_state["apply_player_kill"] = apply_player_kill

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

        player_team = session_state.get("teams", {}).get("player_team", [])
        enemy_team = session_state.get("teams", {}).get("enemy_team", [])
        if game_mode == "Free for all":
            for bot in player_team:
                if bot.get("is_player"):
                    continue
                if random.random() < AI_KILL_RATE * bot.get("skill", 1.0):
                    targets = [entry for entry in player_team if entry is not bot]
                    if not targets:
                        continue
                    victim = random.choice(targets)
                    bot["kills"] += 1
                    victim["deaths"] += 1
        else:
            for teammate in player_team[1:]:
                if random.random() < AI_KILL_RATE * teammate.get("skill", 1.0):
                    teammate["kills"] += 1
                    if enemy_team:
                        random.choice(enemy_team)["deaths"] += 1
                    session_state["team_kills"]["player"] += 1
            for enemy in enemy_team:
                if random.random() < AI_KILL_RATE * enemy.get("skill", 1.0):
                    enemy["kills"] += 1
                    if player_team[1:]:
                        random.choice(player_team[1:])["deaths"] += 1
                    session_state["team_kills"]["enemy"] += 1

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

        team_kills = session_state.get("team_kills", {})
        if (
            game_mode == "Team death match"
            and max(team_kills.get("player", 0), team_kills.get("enemy", 0)) >= TEAM_DEATHMATCH_KILL_CAP
        ):
            schedule_end(0)
            return
        if game_mode == "Free for all":
            roster = session_state.get("teams", {}).get("player_team", [])
            best_kills = max((entry.get("kills", 0) for entry in roster), default=0)
            if best_kills >= FREE_FOR_ALL_KILL_CAP:
                schedule_end(0)
                return
        if game_mode == "Domination":
            control_points = session_state.get("control_points", [])
            next_capture = session_state.get("next_capture_time", now)
            if now >= next_capture:
                point = random.choice(control_points)
                team_choice = random.choice(["player", "enemy"])
                roster = session_state.get("teams", {}).get(
                    "player_team" if team_choice == "player" else "enemy_team",
                    [],
                )
                owner = random.choice(roster)["name"] if roster else "Unknown"
                point["owner"] = team_choice
                point["owner_name"] = owner
                session_state["next_capture_time"] = now + random.randint(3, 7)

            last_tick = session_state.get("last_point_tick", now)
            delta = max(0.0, now - last_tick)
            player_control = sum(1 for point in control_points if point.get("owner") == "player")
            enemy_control = sum(1 for point in control_points if point.get("owner") == "enemy")
            player_score = session_state["team_scores"]["player"] + delta * player_control
            enemy_score = session_state["team_scores"]["enemy"] + delta * enemy_control
            session_state["team_scores"]["player"] = max(session_state["team_scores"]["player"], player_score)
            session_state["team_scores"]["enemy"] = max(session_state["team_scores"]["enemy"], enemy_score)
            session_state["last_point_tick"] = now
            if max(session_state["team_scores"]["player"], session_state["team_scores"]["enemy"]) >= DOMINATION_SCORE_CAP:
                schedule_end(0)
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
            apply_player_kill(kill_count, kill_indices, effects, now)

        if now - session_state["death_minute_start"] >= 60:
            session_state["death_minute_start"] = now
            session_state["deaths_in_minute"] = 0

        if session_state["deaths_in_minute"] < 20 and random.random() < deaths_rate:
            session_state["deaths"] += 1
            session_state["totals"]["deaths"] += 1
            session_state["deaths_in_minute"] += 1
            session_state["team_kills"]["enemy"] += 1
            if session_state.get("player_entry"):
                session_state["player_entry"]["deaths"] += 1
            enemy_team = session_state.get("teams", {}).get("enemy_team", [])
            if enemy_team:
                random.choice(enemy_team)["kills"] += 1
            session_state["current_streak"] = 0
            session_state["respawn_until"] = now + effects["respawn_seconds"]
            session_state["reward_flags"].clear()
            session_state["UAV_bonus_until"] = 0.0
            minute = int((now - session_state["match_start"]) // 60)
            session_state["timeline"]["deaths"][minute] = session_state["timeline"]["deaths"].get(minute, 0) + 1

        if game_mode == "Team death match":
            session_state["team_scores"]["player"] = session_state["team_kills"]["player"]
            session_state["team_scores"]["enemy"] = session_state["team_kills"]["enemy"]
        elif game_mode == "Free for all":
            roster = session_state.get("teams", {}).get("player_team", [])
            best_kills = max((entry.get("kills", 0) for entry in roster), default=0)
            player_entry = session_state.get("player_entry")
            player_kills = player_entry.get("kills", 0) if player_entry else 0
            session_state["team_scores"]["player"] = player_kills
            session_state["team_scores"]["enemy"] = best_kills
        team_scores = session_state.get("team_scores", {})
        kd_var.set(
            "Kills: {kills} | Deaths: {deaths} | Streak: {streak} | Longest: {longest} | "
            "Team {team} - {enemy}".format(
                kills=session_state["kills"],
                deaths=session_state["deaths"],
                streak=session_state["current_streak"],
                longest=session_state["longest_streak"],
                team=int(team_scores.get("player", 0)),
                enemy=int(team_scores.get("enemy", 0)),
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


def on_start(parent):
    # Open the profile setup flow.
    notify("Create a new profile to get started.")
    open_profile_window(parent)


def on_options(parent, loaded_profile, save_path, session_state):
    # Allow players to override attribute-driven effects.
    clear_frame(parent)
    if not loaded_profile or not save_path:
        notify("Load a player profile to edit options.")
        tk.Label(
            parent,
            text="Load a player profile to edit options.",
            font=("Segoe UI", 10),
            bg=THEME["bg"],
            fg=THEME["muted"],
        ).pack(padx=24, pady=24)
        return

    attributes = loaded_profile["player"].get("attributes", {})
    base_effects = compute_attribute_effects(attributes)
    options = loaded_profile["player"].get("options", {})

    window = parent

    header = tk.Label(window, text="Attribute Effects (Overrides)", font=("Segoe UI", 11), bg=THEME["bg"], fg=THEME["text"])
    header.pack(padx=24, pady=(18, 6))

    hint = tk.Label(window, text="Adjust values to override the attribute defaults.", font=("Segoe UI", 9), bg=THEME["bg"], fg=THEME["muted"])
    hint.pack(padx=24, pady=(0, 10))

    accuracy_var = tk.DoubleVar(value=options.get("accuracy", base_effects["accuracy"]) * 100)
    move_var = tk.DoubleVar(value=options.get("movement_speed", base_effects["movement_speed"]))
    respawn_var = tk.DoubleVar(value=options.get("respawn_seconds", base_effects["respawn_seconds"]))
    headshot_var = tk.DoubleVar(value=options.get("headshot_rate", base_effects["headshot_rate"]) * 100)
    offline_var = tk.BooleanVar(value=bool(options.get("offline_progression", False)))
    offline_confirmed = {"accepted": offline_var.get()}

    def add_slider(label_text, var, from_, to, resolution, unit):
        row = tk.Frame(window, bg=THEME["bg"])
        row.pack(fill="x", padx=24, pady=4)
        label = tk.Label(row, text=label_text, width=16, anchor="w", bg=THEME["bg"], fg=THEME["text"])
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
        scale.configure(bg=THEME["bg"], fg=THEME["text"], highlightthickness=0, troughcolor=THEME["panel"])
        scale.pack(side="right")
        if unit:
            scale.configure(label=unit)

    add_slider("Accuracy %", accuracy_var, 50, 110, 1, None)
    add_slider("Move Speed", move_var, 0.7, 1.3, 0.01, "x")
    add_slider("Respawn", respawn_var, 1.5, 4.0, 0.1, "s")
    add_slider("Headshot %", headshot_var, 5, 40, 1, None)

    def on_offline_toggle():
        if offline_var.get() and not offline_confirmed["accepted"]:
            notify("Offline progression can make achievements and level progression fall out of sync.")
            offline_confirmed["accepted"] = True

    def on_save():
        loaded_profile["player"]["options"] = {
            "accuracy": accuracy_var.get() / 100.0,
            "movement_speed": move_var.get(),
            "respawn_seconds": respawn_var.get(),
            "headshot_rate": headshot_var.get() / 100.0,
            "offline_progression": offline_var.get(),
        }
        session_state["options"] = loaded_profile["player"]["options"]
        save_profile_data(loaded_profile, save_path)
        notify("Options saved.")
        on_options(parent, loaded_profile, save_path, session_state)

    offline_row = tk.Frame(window, bg=THEME["bg"])
    offline_row.pack(fill="x", padx=24, pady=(8, 0))
    offline_toggle = tk.Checkbutton(
        offline_row,
        text="Enable offline progression",
        variable=offline_var,
        command=on_offline_toggle,
        bg=THEME["bg"],
        fg=THEME["text"],
        selectcolor=THEME["panel"],
        activebackground=THEME["bg"],
        activeforeground=THEME["text"],
    )
    offline_toggle.pack(side="left")

    debug_header = tk.Label(window, text="Debug Controls", font=("Segoe UI", 10), bg=THEME["bg"], fg=THEME["accent"])
    debug_header.pack(padx=24, pady=(14, 6))

    def on_end_match():
        if session_state.get("phase") != "playing":
            notify("No active match to end.")
            return
        end_match = session_state.get("end_match")
        if not end_match:
            notify("Match end handler is not available yet.")
            return
        end_match()

    end_match_button = tk.Button(window, text="End Current Match", width=20, command=on_end_match)
    end_match_button.configure(bg=THEME["button"], fg=THEME["text"], activebackground=THEME["button_hover"])
    end_match_button.pack(padx=24, pady=(0, 10))

    save_button = tk.Button(window, text="Save Options", width=18, command=on_save)
    save_button.configure(bg=THEME["primary"], fg="#f5f7fb", activebackground=THEME["primary_hover"])
    save_button.pack(padx=24, pady=(12, 18))

    debug_container = tk.Frame(window, bg=THEME["bg"], height=32)
    debug_container.pack(padx=24, pady=(0, 16), fill="x")
    debug_text = tk.Label(debug_container, text="Singularity debug text", font=("Segoe UI", 10), bg=THEME["bg"])
    debug_text.place(relx=0.5, y=8, anchor="n")

    debug_anim = {"index": 0}
    debug_colors = ["#ff5f6d", "#ffc371", "#7dffb8", "#7fc7ff", "#c77dff"]
    debug_offsets = [0, 1, 2, 3, 4, 3, 2, 1]

    def animate_debug_text():
        if not debug_text.winfo_exists():
            return
        color = debug_colors[debug_anim["index"] % len(debug_colors)]
        offset = debug_offsets[debug_anim["index"] % len(debug_offsets)]
        debug_anim["index"] += 1
        jitter = 1 if debug_anim["index"] % 2 == 0 else 3
        debug_text.configure(fg=color, padx=jitter)
        debug_text.place_configure(y=8 + offset)
        window.after(250, animate_debug_text)

    animate_debug_text()

    master_container = tk.Frame(window, bg=THEME["bg"], height=34)
    master_container.pack(padx=24, pady=(0, 16), fill="x")
    master_font = tkfont.Font(family="Segoe UI", size=10)
    master_canvas = tk.Canvas(master_container, height=20, bg=THEME["bg"], highlightthickness=0)
    master_canvas.pack()
    master_text = "Master Prestige 1000"
    base_y = 10
    master_items = []
    cursor_x = 0
    for ch in master_text:
        width = master_font.measure(ch)
        x_pos = cursor_x + width / 2
        item = master_canvas.create_text(x_pos, base_y, text=ch, font=master_font, fill=THEME["text"])
        master_items.append({"item": item, "char": ch, "x": x_pos})
        cursor_x += width
    master_canvas.configure(width=max(180, int(cursor_x)))

    master_state = {"index": 0, "frame": 0}
    master_spin = ["-", "\\", "|", "/"]
    master_colors = ["#ff5f6d", "#ffc371", "#7dffb8", "#7fc7ff", "#c77dff"]

    def animate_master_debug():
        if not master_canvas.winfo_exists():
            return
        color = master_colors[master_state["frame"] % len(master_colors)]
        for entry in master_items:
            master_canvas.itemconfig(entry["item"], fill=color, text=entry["char"])
            master_canvas.coords(entry["item"], entry["x"], base_y)
        if master_items:
            letter_index = master_state["index"] % len(master_items)
            for _ in range(len(master_items)):
                if master_items[letter_index]["char"] != " ":
                    break
                letter_index = (letter_index + 1) % len(master_items)
            spin_char = master_spin[master_state["frame"] % len(master_spin)]
            offset = 3 if master_state["frame"] % 2 == 0 else -3
            entry = master_items[letter_index]
            master_canvas.itemconfig(entry["item"], text=spin_char)
            master_canvas.coords(entry["item"], entry["x"], base_y + offset)
        master_state["frame"] += 1
        if master_state["frame"] % len(master_spin) == 0:
            master_state["index"] += 1
        window.after(120, animate_master_debug)

    animate_master_debug()




def open_match_summary(summary, session_state):
    # Show match summaries in a persistent tabbed view (max 10 tabs).
    notebook = session_state.get("summary_notebook")
    if notebook is None:
        container = session_state.get("summary_container")
        if container is None:
            return
        placeholder = session_state.get("summaries_placeholder")
        if placeholder:
            placeholder.destroy()
            session_state["summaries_placeholder"] = None
        notebook = ttk.Notebook(container)
        notebook.pack(fill="both", expand=True, padx=8, pady=8)
        session_state["summary_notebook"] = notebook
        session_state["summary_tabs"] = []

    tabs = session_state.get("summary_tabs", [])
    if len(tabs) >= 10:
        oldest = tabs.pop(0)
        notebook.forget(oldest)
        oldest.destroy()

    frame = tk.Frame(notebook)
    tab_title = f"{summary.get('mode', 'Match')} {len(tabs) + 1}"
    notebook.add(frame, text=tab_title)
    tabs.append(frame)
    session_state["summary_tabs"] = tabs

    header = tk.Label(frame, text="Match Complete", font=("Segoe UI", 12))
    header.pack(pady=(12, 10))

    rows = [
        ("Mode", summary["mode"]),
        ("Map", summary["map"]),
        ("Weapon", summary["weapon"]),
        ("Result", summary.get("result", "Win")),
        ("Winner", summary.get("winner_name", "N/A")),
        ("Kills", summary["kills"]),
        ("Deaths", summary["deaths"]),
        ("Headshots", summary["headshots"]),
        ("XP Gained", summary["xp_gain"]),
        ("Bonus XP", summary["xp_bonus"]),
        ("Total XP", summary["xp_total"]),
        ("Longest Streak", summary["longest_streak"]),
    ]

    for label_text, value_text in rows:
        row = tk.Frame(frame)
        row.pack(fill="x", pady=2, padx=12)
        label = tk.Label(row, text=f"{label_text}:", width=14, anchor="w")
        label.pack(side="left")
        value = tk.Label(row, text=str(value_text), anchor="w")
        value.pack(side="left")

    team_scores = summary.get("team_scores", {"player": 0, "enemy": 0})
    score_label = "Points" if summary.get("mode") == "Domination" else "Kills"
    scoreboard = summary.get("scoreboard", {})
    player_team = scoreboard.get("player_team", [])
    enemy_team = scoreboard.get("enemy_team", [])
    if player_team or enemy_team:
        divider = tk.Label(frame, text="Team Rankings", font=("Segoe UI", 10))
        divider.pack(pady=(10, 6))

        def sorted_team(team):
            return sorted(team, key=lambda entry: (-entry.get("kills", 0), entry.get("deaths", 0)))

        team_a = tk.Label(
            frame,
            text=f"Your Team ({team_scores.get('player', 0)} {score_label})",
            font=("Segoe UI", 9, "bold"),
            anchor="w",
        )
        team_a.pack(fill="x", padx=12)
        for entry in sorted_team(player_team):
            line = f"{entry.get('name')} - K {entry.get('kills', 0)} D {entry.get('deaths', 0)}"
            tk.Label(frame, text=line, font=("Segoe UI", 9), anchor="w").pack(fill="x", padx=12)

        if enemy_team:
            team_b = tk.Label(
                frame,
                text=f"Enemy Team ({team_scores.get('enemy', 0)} {score_label})",
                font=("Segoe UI", 9, "bold"),
                anchor="w",
            )
            team_b.pack(fill="x", pady=(6, 0), padx=12)
            for entry in sorted_team(enemy_team):
                line = f"{entry.get('name')} - K {entry.get('kills', 0)} D {entry.get('deaths', 0)}"
                tk.Label(frame, text=line, font=("Segoe UI", 9), anchor="w").pack(fill="x", padx=12)

    notebook.select(frame)


def open_match_history(parent, loaded_profile):
    # Show the last 10 match summaries.
    clear_frame(parent)
    if not loaded_profile:
        tk.Label(parent, text="Load a player profile to view match history.", font=("Segoe UI", 10)).pack(
            padx=24, pady=24
        )
        return

    stats = ensure_stats(loaded_profile)
    history = stats.get("match_history", [])

    window = parent
    frame = tk.Frame(window)
    frame.pack(padx=16, pady=16, fill="both", expand=True)

    header = tk.Label(frame, text="Last 10 Matches", font=("Segoe UI", 12))
    header.pack(pady=(0, 10))

    if not history:
        empty = tk.Label(frame, text="No matches recorded yet.", font=("Segoe UI", 10))
        empty.pack()
        return

    for entry in history[:10]:
        row = tk.Frame(frame)
        row.pack(fill="x", pady=2)
        text = (
            f"{entry.get('mode', 'TDM')} | {entry.get('map', 'Unknown')} | "
            f"K {entry.get('kills', 0)} D {entry.get('deaths', 0)} HS {entry.get('headshots', 0)} | "
            f"XP {entry.get('xp_total', 0)}"
        )
        label = tk.Label(row, text=text, anchor="w", font=("Segoe UI", 9))
        label.pack(side="left")


def open_achievements_window(parent, loaded_profile):
    # Display achievements with progress bars.
    clear_frame(parent)
    if not loaded_profile:
        tk.Label(
            parent,
            text="Load a player profile to view achievements.",
            font=("Segoe UI", 10),
            bg=THEME["bg"],
            fg=THEME["muted"],
        ).pack(padx=24, pady=24)
        return

    stats = ensure_stats(loaded_profile)
    earned = stats.setdefault("achievements", {})

    window = parent

    tooltip_label = tk.Label(window, text="", font=("Segoe UI", 9), bg=THEME["bg"], fg=THEME["muted"])
    tooltip_label.pack(padx=16, pady=(0, 8))

    def show_tooltip(_widget, text):
        tooltip_label.configure(text=text)

    def hide_tooltip(*_):
        tooltip_label.configure(text="")

    header = tk.Label(window, text="Achievement Board", font=("Segoe UI", 11, "bold"), bg=THEME["bg"], fg=THEME["text"])
    header.pack(padx=16, pady=(16, 6))

    filter_row = tk.Frame(window, bg=THEME["bg"])
    filter_row.pack(padx=16, pady=(0, 10), fill="x")
    weapon_only_var = tk.BooleanVar(value=False)

    filter_label = tk.Label(filter_row, text="Filter:", font=("Segoe UI", 9), bg=THEME["bg"], fg=THEME["muted"])
    filter_label.pack(side="left")

    weapon_toggle = tk.Checkbutton(
        filter_row,
        text="Weapon achievements only",
        variable=weapon_only_var,
        bg=THEME["bg"],
        fg=THEME["text"],
        selectcolor=THEME["panel"],
        activebackground=THEME["bg"],
        activeforeground=THEME["text"],
        command=lambda: draw_achievements(),
    )
    weapon_toggle.pack(side="left", padx=8)

    list_body = tk.Frame(window, bg=THEME["bg"])
    list_body.pack(padx=16, pady=(0, 16), fill="both", expand=True)
    canvas = tk.Canvas(list_body, bg=THEME["bg"], highlightthickness=0)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar = tk.Scrollbar(list_body, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scrollbar.set)
    frame = tk.Frame(canvas, bg=THEME["bg"])
    canvas.create_window((0, 0), window=frame, anchor="nw", tags="content")
    def update_scrollregion(_event=None):
        canvas.configure(scrollregion=canvas.bbox("all"))

    frame.bind("<Configure>", update_scrollregion)

    def on_canvas_configure(event):
        canvas.itemconfigure("content", width=event.width)

    canvas.bind("<Configure>", on_canvas_configure)

    def is_weapon_entry(entry):
        return entry[2].startswith("weapon_kills:")

    def draw_achievements():
        for widget in frame.winfo_children():
            widget.destroy()

        grouped = {}
        for entry in ACHIEVEMENTS:
            if weapon_only_var.get() and not is_weapon_entry(entry):
                continue
            base_id, level = achievement_base_and_level(entry[0])
            grouped.setdefault(base_id, []).append((level, entry))

        if not grouped:
            empty = tk.Label(frame, text="No achievements to display.", font=("Segoe UI", 9), bg=THEME["bg"], fg=THEME["muted"])
            empty.pack()
            return

        for base_id, levels in grouped.items():
            levels.sort(key=lambda item: item[0])
            current = levels[-1][1]
            for _, entry in levels:
                if not earned.get(entry[0]):
                    current = entry
                    break
            ach_id, name, key, threshold, reward_xp, description = current
            value = achievement_value(loaded_profile, key)
            done = bool(earned.get(ach_id))
            display_value = min(value, threshold)
            ratio = 1.0 if threshold == 0 else min(1.0, display_value / threshold)

            title = tk.Label(
                frame,
                text=f"{name} (+{reward_xp} XP)",
                font=("Segoe UI", 10),
                fg="#f4c542" if done else "#7a7a7a",
                bg=THEME["bg"],
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

    draw_achievements()

def open_profile_window(parent, on_saved=None):
    # Profile creation panel for attribute distribution and gamertag entry.
    clear_frame(parent)
    window = parent
    window.configure(bg=THEME["bg"])
    window.configure(bg=THEME["bg"])

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
            notify("You must spend all 30 points.")
            return
        gamertag = gamertag_var.get().strip()
        if not gamertag:
            notify("Please enter your gamertag.")
            return
        profile = {
            "gamertag": gamertag,
            "attributes": values,
            "play_time_seconds": 0,
            "last_saved": int(time.time()),
            "stats": {
            "games_played": 0,
            "game_modes_played": {},
            "game_mode_wins": {},
            "game_mode_losses": {},
            "maps_played": {},
            "kills": 0,
            "deaths": 0,
            "wins": 0,
            "losses": 0,
            "longest_kill_streak": 0,
            "headshots": 0,
            "xp": 0,
            "lifetime_xp": 0,
                "level": 1,
                "prestige_unlocked": False,
                "prestige": 0,
                "master_prestige": False,
                "master_level": 1,
                "weapons": {},
                "UAV_calls": 0,
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
                "match_history": [],
            },
        }
        save_player_profile(profile)
        notify("Your profile has been saved.")
        if on_saved:
            on_saved(profile)
        else:
            clear_frame(window)

    gamertag_var.trace_add("write", on_gamertag_change)
    save_button.configure(command=on_save)



def view_player_profile(parent, loaded_profile, timer_state):
    # Show a read-only view of the currently loaded profile.
    clear_frame(parent)
    if not loaded_profile:
        tk.Label(
            parent,
            text="Load a player profile first.",
            font=("Segoe UI", 10),
            bg=THEME["bg"],
            fg=THEME["text"],
        ).pack(padx=24, pady=24)
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
    xp_total = int(stats.get("lifetime_xp", stats.get("xp", 0)))
    progress = progress_state(stats)
    level = progress["level"]
    xp_into = progress["xp_into"]
    xp_needed = progress["xp_needed"]
    rank = rank_display_from_progress(progress)

    window = parent
    label_style = {"bg": THEME["bg"], "fg": THEME["text"]}
    diamond_swatches = []
    singularity_swatches = []
    singularity_labels = []
    diamond_after_id = {"id": None, "index": 0}

    def stop_diamond_animation():
        if diamond_after_id["id"]:
            window.after_cancel(diamond_after_id["id"])
            diamond_after_id["id"] = None

    title = tk.Label(window, text=f"Gamertag: {gamertag}", font=("Segoe UI", 11), **label_style)
    title.pack(padx=24, pady=(18, 10))

    time_label = tk.Label(
        window,
        text=f"Time Played: {format_duration(total_time)}",
        font=("Segoe UI", 10),
        **label_style,
    )
    time_label.pack(padx=24, pady=(0, 8))

    level_label = tk.Label(
        window,
        text=f"Level: {level} ({xp_into}/{xp_needed} XP)",
        font=("Segoe UI", 10),
        **label_style,
    )
    level_label.pack(padx=24, pady=(0, 8))

    rank_row = tk.Frame(window, bg=THEME["bg"])
    rank_row.pack(padx=24, pady=(0, 8), fill="x")
    rank_swatch = tk.Canvas(rank_row, width=12, height=12, highlightthickness=0, bg=THEME["bg"])
    rank_swatch.create_rectangle(1, 1, 11, 11, fill=rank_color(rank), outline="#1a1a1a")
    rank_swatch.pack(side="left", padx=(0, 6))
    if rank == "Master of War 1000":
        rank_font = tkfont.Font(family="Segoe UI", size=10)
        rank_canvas = tk.Canvas(rank_row, height=20, bg=THEME["bg"], highlightthickness=0)
        rank_canvas.pack(side="left")
        rank_text = f"Rank: {rank}"
        base_y = 10
        items = []
        cursor_x = 0
        for ch in rank_text:
            width = rank_font.measure(ch)
            x_pos = cursor_x + width / 2
            item = rank_canvas.create_text(x_pos, base_y, text=ch, font=rank_font, fill=THEME["text"])
            items.append({"item": item, "char": ch, "x": x_pos})
            cursor_x += width
        rank_canvas.configure(width=max(160, int(cursor_x)))

        spin_state = {"index": 0, "frame": 0}
        spin_frames = ["-", "\\", "|", "/"]
        rainbow_colors = ["#ff5f6d", "#ffc371", "#7dffb8", "#7fc7ff", "#c77dff"]

        def animate_master_rank():
            if not rank_canvas.winfo_exists():
                return
            color = rainbow_colors[spin_state["frame"] % len(rainbow_colors)]
            for entry in items:
                rank_canvas.itemconfig(entry["item"], fill=color, text=entry["char"])
                rank_canvas.coords(entry["item"], entry["x"], base_y)
            if items:
                letter_index = spin_state["index"] % len(items)
                for _ in range(len(items)):
                    if items[letter_index]["char"] != " ":
                        break
                    letter_index = (letter_index + 1) % len(items)
                spin_char = spin_frames[spin_state["frame"] % len(spin_frames)]
                offset = 3 if spin_state["frame"] % 2 == 0 else -3
                entry = items[letter_index]
                rank_canvas.itemconfig(entry["item"], text=spin_char)
                rank_canvas.coords(entry["item"], entry["x"], base_y + offset)
            spin_state["frame"] += 1
            if spin_state["frame"] % len(spin_frames) == 0:
                spin_state["index"] += 1
            diamond_after_id["id"] = window.after(120, animate_master_rank)

        animate_master_rank()
    else:
        rank_label = tk.Label(rank_row, text=f"Rank: {rank}", font=("Segoe UI", 10), **label_style)
        rank_label.pack(side="left")

    total_xp_label = tk.Label(window, text=f"Total XP: {xp_total}", font=("Segoe UI", 10), **label_style)
    total_xp_label.pack(padx=24, pady=(0, 8))

    wins = int(stats.get("wins", 0))
    losses = int(stats.get("losses", 0))
    kd_label = tk.Label(
        window,
        text=f"Kills: {kills} | Deaths: {deaths} | K/D Ratio: {kd_ratio:.2f}",
        font=("Segoe UI", 10),
        **label_style,
    )
    kd_label.pack(padx=24, pady=(0, 6))

    wl_label = tk.Label(
        window,
        text=f"Wins: {wins} | Losses: {losses}",
        font=("Segoe UI", 10),
        **label_style,
    )
    wl_label.pack(padx=24, pady=(0, 8))

    streak_label = tk.Label(
        window,
        text=f"Longest Kill Streak: {longest_streak}",
        font=("Segoe UI", 10),
        **label_style,
    )
    streak_label.pack(padx=24, pady=(0, 8))

    headshot_label = tk.Label(window, text=f"Headshots: {headshots}", font=("Segoe UI", 10), **label_style)
    headshot_label.pack(padx=24, pady=(0, 8))

    UAV_calls = int(stats.get("UAV_calls", 0))
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
            f"UAVs: {UAV_calls} | Airstrikes: {airstrike_calls} "
            f"(Kills {airstrike_kills}) | Helicopters: {helicopter_calls} "
            f"(Kills {helicopter_kills}) | Nukes: {nuke_victories}"
        ),
        font=("Segoe UI", 10),
        **label_style,
    )
    rewards_label.pack(padx=24, pady=(0, 8))

    mode_wins = stats.get("game_mode_wins", {})
    mode_losses = stats.get("game_mode_losses", {})
    if mode_wins or mode_losses:
        mode_header = tk.Label(window, text="Mode Record", font=("Segoe UI", 10), **label_style)
        mode_header.pack(padx=24, pady=(4, 6))
        for mode_name in sorted(set(mode_wins) | set(mode_losses)):
            wins_value = int(mode_wins.get(mode_name, 0))
            losses_value = int(mode_losses.get(mode_name, 0))
            row = tk.Frame(window, bg=THEME["bg"])
            row.pack(fill="x", padx=24, pady=1)
            label = tk.Label(row, text=mode_name, width=16, anchor="w", **label_style)
            label.pack(side="left")
            value = tk.Label(row, text=f"W {wins_value} / L {losses_value}", anchor="e", **label_style)
            value.pack(side="right")

    multikill_label = tk.Label(
        window,
        text=(
            f"Double: {double_kills} | Triple: {triple_kills} | Quad: {quad_kills} | "
            f"Monster: {monster_kills} | Team: {team_kills}"
        ),
        font=("Segoe UI", 10),
        **label_style,
    )
    multikill_label.pack(padx=24, pady=(0, 8))

    weapons = stats.get("weapons", {})
    if weapons:
        weapon_header = tk.Label(window, text="Weapon Progression", font=("Segoe UI", 10), **label_style)
        weapon_header.pack(padx=24, pady=(4, 6))
        for weapon_name in sorted(weapons):
            weapon_stats = weapons[weapon_name]
            weapon_xp = int(weapon_stats.get("xp", 0))
            weapon_level, weapon_into, weapon_needed = level_progress(weapon_xp)
            weapon_headshots = int(weapon_stats.get("headshots", 0))
            weapon_camo = weapon_stats.get("camo", "None")
            row = tk.Frame(window, bg=THEME["bg"])
            row.pack(fill="x", padx=24, pady=1)
            label = tk.Label(row, text=weapon_name, width=14, anchor="w", **label_style)
            label.pack(side="left")
            swatch = tk.Canvas(row, width=12, height=12, highlightthickness=0, bg=THEME["bg"])
            swatch.create_rectangle(1, 1, 11, 11, fill=camo_color(weapon_camo), outline="#1a1a1a")
            swatch.pack(side="left", padx=(4, 6))
            if weapon_camo == "Diamond":
                diamond_swatches.append(swatch)
            if weapon_camo == "Singularity":
                singularity_swatches.append(swatch)
            value = tk.Label(
                row,
                text=f"Lv {weapon_level} ({weapon_into}/{weapon_needed}) | HS {weapon_headshots} | {weapon_camo}",
                anchor="e",
                **label_style,
            )
            value.pack(side="right")
            if weapon_camo == "Singularity":
                singularity_labels.extend([label, value])

    def animate_diamond():
        alive_diamond = [swatch for swatch in diamond_swatches if swatch.winfo_exists()]
        alive_singularity = [swatch for swatch in singularity_swatches if swatch.winfo_exists()]
        alive_labels = [label for label in singularity_labels if label.winfo_exists()]
        if not alive_diamond and not alive_singularity and not alive_labels:
            return
        diamond_colors = ["#7fc7ff", "#bfe9ff", "#5aaef2", "#e7f7ff"]
        singularity_colors = ["#ff5f6d", "#ffc371", "#7dffb8", "#7fc7ff", "#c77dff"]
        diamond_color = diamond_colors[diamond_after_id["index"] % len(diamond_colors)]
        singularity_color = singularity_colors[diamond_after_id["index"] % len(singularity_colors)]
        diamond_after_id["index"] += 1
        for swatch in alive_diamond:
            swatch.delete("all")
            swatch.create_rectangle(1, 1, 11, 11, fill=diamond_color, outline="#1a1a1a")
        for swatch in alive_singularity:
            swatch.delete("all")
            swatch.create_rectangle(1, 1, 11, 11, fill=singularity_color, outline="#1a1a1a")
        if alive_labels:
            jitter = 1 if diamond_after_id["index"] % 2 == 0 else 3
            for label in alive_labels:
                label.configure(fg=singularity_color, padx=jitter)
        diamond_after_id["id"] = window.after(250, animate_diamond)

    animate_diamond()

    def on_close():
        stop_diamond_animation()

    attrs_frame = tk.Frame(window, bg=THEME["bg"])
    attrs_frame.pack(padx=24, pady=(0, 18))

    for name in ATTRIBUTES:
        value = attributes.get(name, 0)
        row = tk.Frame(attrs_frame, bg=THEME["bg"])
        row.pack(fill="x", pady=2)
        label = tk.Label(row, text=name, width=18, anchor="w", **label_style)
        label.pack(side="left")
        number = tk.Label(row, text=str(value), width=4, anchor="e", **label_style)
        number.pack(side="right")


def open_game_setup_window(
    parent,
    loaded_profile,
    save_path,
    session_state,
    status_var,
    timer_var,
    map_var,
    kd_var,
    xp_var,
    timer_state=None,
):
    # Allow the player to pick default weapon and game mode for this profile.
    clear_frame(parent)
    player = loaded_profile["player"]
    defaults = player.get("defaults", {})

    window = parent

    header = tk.Label(window, text="Select default loadout and mode.", font=("Segoe UI", 11))
    header.pack(padx=24, pady=(18, 12))

    default_weapon = defaults.get("weapon", WEAPON_POOL[0])
    default_category = next(
        (category for category, weapons in WEAPON_CATEGORIES.items() if default_weapon in weapons),
        next(iter(WEAPON_CATEGORIES)),
    )

    category_frame = tk.Frame(window)
    category_frame.pack(padx=24, pady=(0, 8))

    category_label = tk.Label(category_frame, text="Category:", width=18, anchor="w")
    category_label.pack(side="left")

    category_var = tk.StringVar(value=default_category)
    category_menu = tk.OptionMenu(category_frame, category_var, *WEAPON_CATEGORIES.keys())
    category_menu.config(width=18)
    category_menu.pack(side="right")

    weapon_frame = tk.Frame(window)
    weapon_frame.pack(padx=24, pady=(0, 8))

    weapon_label = tk.Label(weapon_frame, text="Weapon:", width=18, anchor="w")
    weapon_label.pack(side="left")

    initial_weapon = default_weapon
    if initial_weapon not in WEAPON_CATEGORIES.get(default_category, ()):
        initial_weapon = WEAPON_CATEGORIES[default_category][0]
    weapon_var = tk.StringVar(value=initial_weapon)
    weapon_menu = tk.OptionMenu(weapon_frame, weapon_var, *WEAPON_CATEGORIES[default_category])
    weapon_menu.config(width=18)
    weapon_menu.pack(side="right")

    def refresh_weapon_menu(*_):
        category = category_var.get()
        menu = weapon_menu["menu"]
        menu.delete(0, "end")
        for weapon in WEAPON_CATEGORIES.get(category, ()):
            menu.add_command(label=weapon, command=lambda value=weapon: weapon_var.set(value))
        if weapon_var.get() not in WEAPON_CATEGORIES.get(category, ()):
            weapon_var.set(WEAPON_CATEGORIES[category][0])

    category_var.trace_add("write", refresh_weapon_menu)

    mode_frame = tk.Frame(window)
    mode_frame.pack(padx=24, pady=(0, 12))

    mode_label = tk.Label(mode_frame, text="Game Mode:", width=18, anchor="w")
    mode_label.pack(side="left")

    mode_var = tk.StringVar(value=defaults.get("game_mode", "Team death match"))
    mode_menu = tk.OptionMenu(mode_frame, mode_var, "Team death match", "Domination", "Free for all")
    mode_menu.config(width=18)
    mode_menu.pack(side="right")

    def persist_defaults():
        player["defaults"] = {
            "weapon": weapon_var.get(),
            "game_mode": mode_var.get(),
        }
        save_profile_data(loaded_profile, save_path)

    def on_quick_start():
        persist_defaults()
        start_game_session(
            parent.winfo_toplevel(),
            session_state,
            status_var,
            timer_var,
            map_var,
            kd_var,
            xp_var,
            loaded_profile,
            save_path,
        )
        clear_frame(window)

    def on_save():
        persist_defaults()
        notify("Loadout saved.")
        if timer_state is not None:
            view_player_profile(window, loaded_profile, timer_state)

    quick_button = tk.Button(window, text="Quick Start", width=22, command=on_quick_start)
    quick_button.pack(pady=(6, 6))
    save_button = tk.Button(window, text="Save Loadout", width=22, command=on_save)
    save_button.pack(pady=(0, 18))


def main():
    # Build the main menu window.
    root = tk.Tk()
    root.title("Idle FPS")
    root.configure(bg=THEME["bg"])

    notify_var = tk.StringVar(value="")
    notify_label = tk.Label(
        root,
        textvariable=notify_var,
        font=("Segoe UI", 9),
        bg=THEME["panel"],
        fg=THEME["accent"],
        anchor="w",
    )
    notify_label.pack(fill="x", padx=12, pady=(8, 4))

    def set_notify(message):
        notify_var.set(message)
        if message:
            root.after(4000, lambda: notify_var.set(""))

    global NOTIFY_CALLBACK
    NOTIFY_CALLBACK = set_notify

    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True, padx=12, pady=(0, 12))

    tabs = {
        "home": tk.Frame(notebook, bg=THEME["bg"]),
        "profile": tk.Frame(notebook, bg=THEME["bg"]),
        "options": tk.Frame(notebook, bg=THEME["bg"]),
        "achievements": tk.Frame(notebook, bg=THEME["bg"]),
        "history": tk.Frame(notebook, bg=THEME["bg"]),
        "summaries": tk.Frame(notebook, bg=THEME["bg"]),
        "match": tk.Frame(notebook, bg=THEME["bg"]),
    }
    notebook.add(tabs["home"], text="Home")
    notebook.add(tabs["profile"], text="Profile")
    notebook.add(tabs["options"], text="Options")
    notebook.add(tabs["achievements"], text="Achievements")
    notebook.add(tabs["history"], text="History")
    notebook.add(tabs["summaries"], text="Summaries")
    notebook.add(tabs["match"], text="Match")

    def show_tab(key):
        notebook.select(tabs[key])
        session_state["current_tab"] = key

    def on_tab_changed(event):
        selected = event.widget.select()
        if selected == str(tabs["options"]):
            session_state["current_tab"] = "options"
            on_options(tabs["options"], loaded_profile["data"], loaded_profile["path"], session_state)
        elif selected == str(tabs["achievements"]):
            session_state["current_tab"] = "achievements"
            open_achievements_window(tabs["achievements"], loaded_profile["data"])
        elif selected == str(tabs["profile"]):
            session_state["current_tab"] = "profile"
        elif selected == str(tabs["home"]):
            session_state["current_tab"] = "home"
        elif selected == str(tabs["history"]):
            session_state["current_tab"] = "history"
        elif selected == str(tabs["summaries"]):
            session_state["current_tab"] = "summaries"
        elif selected == str(tabs["match"]):
            session_state["current_tab"] = "match"

    notebook.bind("<<NotebookTabChanged>>", on_tab_changed)

    title_label = tk.Label(
        tabs["home"],
        text="Idle FPS version 0.0.8.1 by ErsatzRealizm",
        font=("Segoe UI", 16, "bold"),
        bg=THEME["bg"],
        fg=THEME["text"],
    )
    title_label.pack(padx=24, pady=(22, 12))

    actions_frame = tk.Frame(tabs["home"], bg=THEME["panel"], highlightbackground=THEME["panel_edge"], highlightthickness=1)
    actions_frame.pack(padx=24, pady=(0, 14), fill="both", expand=True)
    actions_header = tk.Label(
        actions_frame,
        text="Actions",
        font=("Segoe UI", 10, "bold"),
        bg=THEME["panel"],
        fg=THEME["accent"],
    )
    actions_header.pack(anchor="w", padx=14, pady=(10, 6))

    menu_frame = tk.Frame(actions_frame, bg=THEME["panel"])
    menu_frame.pack(padx=14, pady=(0, 12), fill="both", expand=True)

    def style_button(button, primary=False, danger=False):
        bg = THEME["primary"] if primary else THEME["button"]
        hover = THEME["primary_hover"] if primary else THEME["button_hover"]
        fg = "#f5f7fb"
        if danger:
            bg = THEME["danger"]
            hover = "#8a4a4a"
        button.configure(
            bg=bg,
            fg=fg,
            activebackground=hover,
            activeforeground=fg,
            relief="flat",
            highlightthickness=0,
        )

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
        "UAV_bonus_until": 0.0,
        "nuke_until": 0.0,
        "nuke_prompt": None,
        "pending_nuke": False,
        "match_start": 0.0,
        "timeline": {},
        "totals": {},
    }
    session_state["match_view_closed_callback"] = lambda: None
    session_state["match_view_opened_callback"] = lambda: None
    session_state["ribbon_refresh_callback"] = lambda: None
    session_state["profile_refresh_callback"] = lambda: None
    session_state["current_tab"] = "home"
    session_state["summary_container"] = tabs["summaries"]
    session_state["summary_notebook"] = None
    session_state["summary_tabs"] = []
    session_state["match_container"] = tabs["match"]
    session_state["match_canvas"] = None
    session_state["nuke_prompt_payload"] = None

    summaries_placeholder = tk.Label(
        tabs["summaries"],
        text="Match summaries will appear here.",
        font=("Segoe UI", 10),
        bg=THEME["bg"],
        fg=THEME["muted"],
    )
    summaries_placeholder.pack(pady=24)
    session_state["summaries_placeholder"] = summaries_placeholder

    match_prompt = tk.Frame(tabs["match"], bg=THEME["panel"])
    match_prompt.pack(fill="x", padx=12, pady=(12, 6))
    match_prompt_label = tk.Label(
        match_prompt,
        text="Nuclear victory ready. Accept and end the match?",
        font=("Segoe UI", 10),
        bg=THEME["panel"],
        fg=THEME["text"],
    )
    match_prompt_label.pack(side="left", padx=8)
    match_prompt.pack_forget()

    def accept_nuke():
        payload = session_state.get("nuke_prompt_payload")
        if payload:
            stats, schedule_end = payload
            trigger_nuke(session_state, stats, time.monotonic(), schedule_end, force=True)
        close_nuke_prompt(session_state)

    def decline_nuke():
        close_nuke_prompt(session_state)
        session_state["pending_nuke"] = False

    accept_nuke_button = tk.Button(match_prompt, text="Accept", width=10, command=accept_nuke)
    style_button(accept_nuke_button, primary=True)
    accept_nuke_button.pack(side="right", padx=6)

    decline_nuke_button = tk.Button(match_prompt, text="Decline", width=10, command=decline_nuke)
    style_button(decline_nuke_button)
    decline_nuke_button.pack(side="right", padx=6)

    session_state["nuke_prompt_frame"] = match_prompt

    profile_frame = tk.Frame(tabs["profile"], bg=THEME["bg"])
    profile_frame.pack(fill="both", expand=True, padx=16, pady=16)

    profile_sidebar = tk.Frame(profile_frame, bg=THEME["panel"], highlightbackground=THEME["panel_edge"], highlightthickness=1)
    profile_sidebar.pack(side="left", fill="y", padx=(0, 12))

    profile_list_label = tk.Label(profile_sidebar, text="Profiles", font=("Segoe UI", 10, "bold"), bg=THEME["panel"], fg=THEME["accent"])
    profile_list_label.pack(anchor="w", padx=10, pady=(10, 6))

    profile_list = tk.Listbox(profile_sidebar, height=12, width=24)
    profile_list.pack(padx=10, pady=(0, 10))

    profile_buttons = tk.Frame(profile_sidebar, bg=THEME["panel"])
    profile_buttons.pack(padx=10, pady=(0, 10), fill="x")

    profile_content = tk.Frame(profile_frame, bg=THEME["bg"])
    profile_content.pack(side="left", fill="both", expand=True)
    profile_view_state = {"active": False}

    def show_profile_view():
        profile_view_state["active"] = True
        view_player_profile(profile_content, loaded_profile["data"], timer_state)

    def refresh_profile_list():
        profile_list.delete(0, "end")
        for path in sorted(Path(".").glob("*.json")):
            profile_list.insert("end", path.name)

    def load_profile_from_path(path, show_loadout=True):
        session_status_var.set("Loading profile...")
        try:
            data = json.loads(Path(path).read_text(encoding="ascii"))
            gamertag = data["player"]["gamertag"]
        except (OSError, json.JSONDecodeError, KeyError, TypeError):
            notify("Selected file is not a valid profile.")
            return
        try:
            LAST_PROFILE_FILE.write_text(str(path), encoding="ascii")
        except OSError:
            pass
        last_saved = int(data["player"].get("last_saved", time.time()))
        offline_seconds = int(time.time()) - last_saved
        offline_enabled = bool(data["player"].get("options", {}).get("offline_progression", False))
        if offline_enabled and offline_seconds >= 60:
            apply_offline_progress(data, offline_seconds)
            save_profile_data(data, Path(path))
        loaded_profile["data"] = data
        loaded_profile["path"] = Path(path)
        playing_as_var.set(f"Playing as: {gamertag}")
        timer_state["elapsed"] = int(data["player"].get("play_time_seconds", 0))
        timer_state["start"] = time.monotonic()
        timer_state["running"] = True
        start_button.configure(text="Play")
        refresh_profile_button.configure(state="normal")
        update_ribbon_display()
        session_state["running"] = True
        session_status_var.set("Connecting to lobby...")
        root.after(
            1200,
            lambda: start_lobby_wait(
                root,
                session_state,
                session_status_var,
                session_timer_var,
                session_map_var,
                session_kd_var,
                session_xp_var,
                data,
                loaded_profile["path"],
            ),
        )
        if show_loadout:
            profile_view_state["active"] = False
            show_tab("profile")
            profile_view_state["active"] = False
            open_game_setup_window(
                profile_content,
                loaded_profile["data"],
                loaded_profile["path"],
                session_state,
                session_status_var,
                session_timer_var,
                session_map_var,
                session_kd_var,
                session_xp_var,
                timer_state,
            )
        else:
            show_profile_view()
        notify(f"Welcome back, {gamertag}.")

    def load_selected_profile():
        selection = profile_list.curselection()
        if not selection:
            notify("Select a profile to load.")
            return
        filename = profile_list.get(selection[0])
        load_profile_from_path(filename)

    load_profile_button = tk.Button(profile_buttons, text="Load Selected", command=load_selected_profile)
    style_button(load_profile_button)
    load_profile_button.pack(fill="x", pady=(0, 6))

    def start_profile_create():
        def on_saved(profile):
            refresh_profile_list()
            save_path = Path(f"{sanitize_filename(profile.get('gamertag', 'player'))}.json")
            if save_path.exists():
                load_profile_from_path(save_path, show_loadout=True)
            else:
                show_profile_view()
        profile_view_state["active"] = False
        open_profile_window(profile_content, on_saved)

    create_profile_button = tk.Button(profile_buttons, text="Create New", command=start_profile_create)
    style_button(create_profile_button)
    create_profile_button.pack(fill="x")

    refresh_profile_button = tk.Button(profile_buttons, text="Refresh Stats", command=show_profile_view)
    style_button(refresh_profile_button)
    refresh_profile_button.pack(fill="x", pady=(6, 0))
    refresh_profile_button.configure(state="disabled")

    def auto_load_last_profile():
        if loaded_profile["data"] or not LAST_PROFILE_FILE.exists():
            return
        last_path = LAST_PROFILE_FILE.read_text(encoding="ascii").strip()
        if not last_path:
            return
        path = Path(last_path)
        if path.exists():
            load_profile_from_path(path, show_loadout=True)

    refresh_profile_list()
    show_profile_view()
    root.after(200, auto_load_last_profile)
    tray_state = {"icon": None}

    def show_window():
        root.deiconify()
        root.lift()
        root.focus_force()

    def create_tray_icon():
        if tray_state["icon"] or pystray is None or Image is None:
            return
        image = Image.new("RGB", (64, 64), "#1f2a36")
        draw = ImageDraw.Draw(image)
        draw.rectangle((8, 8, 56, 56), outline="#7fc7ff", width=3)
        draw.line((32, 14, 32, 50), fill="#d6e2f0", width=2)
        draw.line((14, 32, 50, 32), fill="#d6e2f0", width=2)

        def on_show(icon, _item):
            icon.stop()
            tray_state["icon"] = None
            root.after(0, show_window)

        def on_exit_tray(icon, _item):
            icon.stop()
            tray_state["icon"] = None
            root.after(0, on_exit)

        icon = pystray.Icon(
            "IdleFPS",
            image,
            "Idle FPS",
            menu=pystray.Menu(
                pystray.MenuItem("Show", on_show),
                pystray.MenuItem("Exit", on_exit_tray),
            ),
        )
        tray_state["icon"] = icon
        icon.run_detached()

    def hide_to_tray():
        root.withdraw()
        create_tray_icon()

    def on_start_click():
        if loaded_profile["data"] and loaded_profile["path"]:
            show_tab("profile")
            open_game_setup_window(
                profile_content,
                loaded_profile["data"],
                loaded_profile["path"],
                session_state,
                session_status_var,
                session_timer_var,
                session_map_var,
                session_kd_var,
                session_xp_var,
                timer_state,
            )
            return
        show_tab("profile")
        refresh_profile_list()
        notify("Select a profile to play or create a new one.")

    start_button = tk.Button(menu_frame, text="Play", width=16, command=on_start_click)
    style_button(start_button, primary=True)
    start_button.pack(pady=4)

    def on_view_profile():
        show_tab("profile")
        show_profile_view()

    view_button = tk.Button(
        menu_frame,
        text="View Player Profile",
        width=16,
        command=on_view_profile,
    )
    style_button(view_button)
    view_button.pack(pady=4)

    options_button = tk.Button(
        menu_frame,
        text="Options",
        width=16,
        command=lambda: (show_tab("options"), on_options(tabs["options"], loaded_profile["data"], loaded_profile["path"], session_state)),
    )
    style_button(options_button)
    options_button.pack(pady=4)

    def update_match_view_label():
        match_view_button.configure(text="Match / Lobby View")

    def on_toggle_match_view():
        show_tab("match")
        if session_state.get("phase") == "playing":
            start_doomguy_animation(root, session_state)
        elif session_state.get("phase") == "waiting":
            start_lobby_view(root, session_state, session_state.get("lobby_duration", 12))
        else:
            notify("Start a match to open the match view.")

    match_view_button = tk.Button(menu_frame, text="Match / Lobby View", width=16, command=on_toggle_match_view)
    style_button(match_view_button)
    match_view_button.pack(pady=4)
    session_state["match_view_closed_callback"] = update_match_view_label
    session_state["match_view_opened_callback"] = update_match_view_label


    achievements_button = tk.Button(
        menu_frame,
        text="Achievements",
        width=16,
        command=lambda: (show_tab("achievements"), open_achievements_window(tabs["achievements"], loaded_profile["data"])),
    )
    style_button(achievements_button)
    achievements_button.pack(pady=4)

    history_button = tk.Button(
        menu_frame,
        text="Match History",
        width=16,
        command=lambda: (show_tab("history"), open_match_history(tabs["history"], loaded_profile["data"])),
    )
    style_button(history_button)
    history_button.pack(pady=4)

    def on_about():
        notify("Vibe coded by Jdog 1/2/2026. Use as inspiration to make a better Idle FPS game.")

    about_button = tk.Button(menu_frame, text="About", width=16, command=on_about)
    style_button(about_button)
    about_button.pack(pady=4)

    def on_exit():
        icon = tray_state.get("icon")
        if icon:
            icon.stop()
            tray_state["icon"] = None
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
                session_state.get("kills", 0),
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
        refresh_profile_button.configure(state="disabled")
        if loaded_profile["data"] and loaded_profile["path"]:
            total_time = get_total_play_time(timer_state)
            loaded_profile["data"]["player"]["play_time_seconds"] = total_time
            save_profile_data(loaded_profile["data"], loaded_profile["path"])
        root.destroy()

    exit_button = tk.Button(menu_frame, text="Exit", width=16, command=on_exit)
    style_button(exit_button, danger=True)
    exit_button.pack(pady=4)

    status_frame = tk.Frame(tabs["home"], bg=THEME["panel"], highlightbackground=THEME["panel_edge"], highlightthickness=1)
    status_frame.pack(padx=24, pady=(0, 14), fill="both", expand=True)
    status_header = tk.Label(
        status_frame,
        text="Match Status",
        font=("Segoe UI", 10, "bold"),
        bg=THEME["panel"],
        fg=THEME["accent"],
    )
    status_header.pack(anchor="w", padx=14, pady=(10, 6))

    status_body = tk.Frame(status_frame, bg=THEME["panel"])
    status_body.pack(padx=14, pady=(0, 12), fill="both", expand=True)

    playing_as_label = tk.Label(status_body, textvariable=playing_as_var, font=("Segoe UI", 10), bg=THEME["panel"], fg=THEME["text"])
    playing_as_label.pack(anchor="w", pady=2)

    session_status_label = tk.Label(status_body, textvariable=session_status_var, font=("Segoe UI", 10), bg=THEME["panel"], fg=THEME["text"])
    session_status_label.pack(anchor="w", pady=2)

    session_timer_label = tk.Label(status_body, textvariable=session_timer_var, font=("Segoe UI", 10), bg=THEME["panel"], fg=THEME["text"])
    session_timer_label.pack(anchor="w", pady=2)

    session_map_label = tk.Label(status_body, textvariable=session_map_var, font=("Segoe UI", 10), bg=THEME["panel"], fg=THEME["text"])
    session_map_label.pack(anchor="w", pady=2)

    session_kd_label = tk.Label(status_body, textvariable=session_kd_var, font=("Segoe UI", 10), bg=THEME["panel"], fg=THEME["text"])
    session_kd_label.pack(anchor="w", pady=2)

    session_xp_label = tk.Label(status_body, textvariable=session_xp_var, font=("Segoe UI", 10), bg=THEME["panel"], fg=THEME["text"])
    session_xp_label.pack(anchor="w", pady=2)

    ribbons_frame = tk.Frame(tabs["home"], bg=THEME["panel"], highlightbackground=THEME["panel_edge"], highlightthickness=1)
    ribbons_frame.pack(padx=24, pady=(0, 14), fill="both", expand=True)
    ribbons_header = tk.Label(
        ribbons_frame,
        text="Achievement Ribbons",
        font=("Segoe UI", 10, "bold"),
        bg=THEME["panel"],
        fg=THEME["accent"],
    )
    ribbons_header.pack(anchor="w", padx=14, pady=(10, 6))

    ribbons_canvas = tk.Canvas(ribbons_frame, width=420, height=90, bg="#121821", highlightthickness=0)
    ribbons_canvas.pack(padx=14, pady=(0, 8), fill="both", expand=True)

    ribbon_page = {"index": 0}

    def on_prev_ribbons():
        ribbon_page["index"] = max(0, ribbon_page["index"] - 1)
        update_ribbon_display()

    def on_next_ribbons():
        ribbon_page["index"] += 1
        update_ribbon_display()

    ribbon_controls = tk.Frame(ribbons_frame, bg=THEME["panel"])
    ribbon_controls.pack(padx=14, pady=(0, 12))
    prev_ribbon_button = tk.Button(ribbon_controls, text="Prev", width=8, command=on_prev_ribbons)
    style_button(prev_ribbon_button)
    prev_ribbon_button.pack(side="left", padx=6)
    ribbon_page_label = tk.Label(ribbon_controls, text="Page 0/0", font=("Segoe UI", 9), bg=THEME["panel"], fg=THEME["muted"])
    ribbon_page_label.pack(side="left", padx=6)
    next_ribbon_button = tk.Button(ribbon_controls, text="Next", width=8, command=on_next_ribbons)
    style_button(next_ribbon_button)
    next_ribbon_button.pack(side="left", padx=6)

    def update_ribbon_display():
        ribbons_canvas.delete("all")
        if not loaded_profile["data"]:
            ribbons_canvas.create_text(
                210,
                45,
                text="Load a profile to display earned ribbons.",
                fill="#7a7a7a",
                font=("Segoe UI", 9),
            )
            ribbon_page_label.configure(text="Page 0/0")
            prev_ribbon_button.configure(state="disabled")
            next_ribbon_button.configure(state="disabled")
            return
        stats = ensure_stats(loaded_profile["data"])
        earned = stats.get("achievements", {})
        grouped = {}
        for entry in ACHIEVEMENTS:
            if not earned.get(entry[0]):
                continue
            base_id, level = achievement_base_and_level(entry[0])
            current = grouped.get(base_id)
            if current is None or level > current[0]:
                grouped[base_id] = (level, entry)
        earned_entries = [entry for _, entry in grouped.values()]
        if not earned_entries:
            ribbons_canvas.create_text(
                210,
                45,
                text="No ribbons earned yet.",
                fill="#7a7a7a",
                font=("Segoe UI", 9),
            )
            ribbon_page_label.configure(text="Page 0/0")
            prev_ribbon_button.configure(state="disabled")
            next_ribbon_button.configure(state="disabled")
            return
        per_page = 6
        total_pages = max(1, (len(earned_entries) + per_page - 1) // per_page)
        ribbon_page["index"] = max(0, min(ribbon_page["index"], total_pages - 1))
        start_index = ribbon_page["index"] * per_page
        show_entries = earned_entries[start_index : start_index + per_page]
        ribbon_page_label.configure(text=f"Page {ribbon_page['index'] + 1}/{total_pages}")
        prev_ribbon_button.configure(state="normal" if ribbon_page["index"] > 0 else "disabled")
        next_ribbon_button.configure(state="normal" if ribbon_page["index"] < total_pages - 1 else "disabled")
        ribbon_width = 200
        ribbon_height = 26
        padding_x = 10
        padding_y = 8
        default_stripes = ["#3c6e9b", "#5d9c59", "#b88b3c", "#8c3c5d"]
        category_stripes = {
            "Assault Rifle": ["#5d9c59", "#8b6f2a", "#3c6e9b", "#6f8b2a"],
            "SMG": ["#6a8cc9", "#4b6fb3", "#8cc96a", "#c9a26a"],
            "Sniper Rifle": ["#7a7f8c", "#9aa1b0", "#4a5363", "#b0b7c6"],
            "Pistol": ["#8b5a3c", "#c9a26a", "#6b4a3b", "#b07a4a"],
            "Rocket Launcher": ["#8c3c5d", "#c95a3c", "#b84a4a", "#f0b14b"],
        }
        for idx, (_, name, key, _, _, _) in enumerate(show_entries):
            row = idx // 2
            col = idx % 2
            x0 = padding_x + col * (ribbon_width + padding_x)
            y0 = padding_y + row * (ribbon_height + padding_y)
            stripe_colors = default_stripes
            if isinstance(key, str) and key.startswith("weapon_kills:"):
                weapon_name = key.split("weapon_kills:", 1)[1]
                category = next(
                    (cat for cat, weapons in WEAPON_CATEGORIES.items() if weapon_name in weapons),
                    None,
                )
                if category and category in category_stripes:
                    stripe_colors = category_stripes[category]
            for stripe in range(4):
                sx0 = x0 + stripe * (ribbon_width // 4)
                sx1 = sx0 + (ribbon_width // 4)
                ribbons_canvas.create_rectangle(sx0, y0, sx1, y0 + ribbon_height, fill=stripe_colors[stripe], outline="")
            ribbons_canvas.create_rectangle(x0, y0, x0 + ribbon_width, y0 + ribbon_height, outline="#1a1a1a")
            ribbons_canvas.create_text(
                x0 + ribbon_width / 2,
                y0 + ribbon_height / 2,
                text=name,
                fill="#f2f2f2",
                font=("Segoe UI", 8, "bold"),
            )

    session_state["ribbon_refresh_callback"] = update_ribbon_display
    session_state["profile_refresh_callback"] = lambda: (
        show_profile_view() if session_state.get("current_tab") == "profile" else None
    )

    root.resizable(True, True)
    def on_close_request():
        if pystray and Image and ImageDraw:
            hide_to_tray()
        else:
            on_exit()

    root.protocol("WM_DELETE_WINDOW", on_close_request)
    root.mainloop()


if __name__ == "__main__":
    main()
