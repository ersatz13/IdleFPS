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


def sanitize_filename(name):
    # Keep save filenames safe and predictable on disk.
    safe = "".join(ch for ch in name if ch.isalnum() or ch in (" ", "-", "_")).strip()
    return safe or "player"


def save_profile_data(data, save_path):
    # Write the full profile payload to a specific path.
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
    kills_per_min = 8 + 22 * skill
    deaths_per_min = 14 - 10 * skill
    return kills_per_min / 60.0, deaths_per_min / 60.0


def add_kill_death_stats(loaded_profile, kills, deaths, headshots=0):
    # Accumulate kills, deaths, and headshots into the profile stats.
    stats = loaded_profile["player"].setdefault(
        "stats",
        {
            "games_played": 0,
            "game_modes_played": {},
            "maps_played": {},
            "kills": 0,
            "deaths": 0,
            "longest_kill_streak": 0,
            "headshots": 0,
        },
    )
    stats["kills"] = int(stats.get("kills", 0)) + int(kills)
    stats["deaths"] = int(stats.get("deaths", 0)) + int(deaths)
    stats["headshots"] = int(stats.get("headshots", 0)) + int(headshots)


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

        session_state["anim_frame"] = frame + 1
        session_state["anim_after_id"] = root.after(80, draw_scene)

    draw_scene()


def stop_game_session(root, session_state, status_var, timer_var, map_var, kd_var):
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
    status_var.set("Not in game")
    timer_var.set("")
    map_var.set("")
    kd_var.set("")


def start_lobby_wait(root, session_state, status_var, timer_var, map_var, kd_var, loaded_profile, save_path):
    # Wait a short random buffer before starting the next game.
    if not session_state.get("running"):
        return
    status_var.set("Waiting for a lobby...")
    timer_var.set("")
    map_var.set("")
    kd_var.set("")
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
            loaded_profile,
            save_path,
        ),
    )


def start_game_session(root, session_state, status_var, timer_var, map_var, kd_var, loaded_profile, save_path):
    # Start a timed game session based on the profile's defaults.
    if not loaded_profile or not save_path:
        return
    defaults = loaded_profile["player"].get("defaults")
    if not defaults or "game_mode" not in defaults:
        status_var.set("Not in game")
        timer_var.set("")
        map_var.set("")
        kd_var.set("")
        return

    game_mode = defaults["game_mode"]
    map_name = random.choice(MAP_POOL)
    attributes = loaded_profile["player"].get("attributes", {})
    duration_seconds = random.randint(8, 13) * 60
    session_state["running"] = True
    session_state["phase"] = "playing"
    session_state["end_time"] = time.monotonic() + duration_seconds
    stats = loaded_profile["player"].setdefault(
        "stats",
        {
            "games_played": 0,
            "game_modes_played": {},
            "maps_played": {},
            "kills": 0,
            "deaths": 0,
            "longest_kill_streak": 0,
            "headshots": 0,
        },
    )
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
    session_state["kill_feed"] = []
    session_state["player_name"] = loaded_profile["player"].get("gamertag", "Player")
    session_state["encounter_enemies"] = random.choices(ENEMY_POOL, k=random.randint(1, 6))
    session_state["encounter_last_update"] = time.monotonic()
    status_var.set(f"Playing {game_mode}")
    map_var.set(f"Now playing on map {map_name}")
    start_doomguy_animation(root, session_state)
    stats["games_played"] = int(stats.get("games_played", 0)) + 1
    modes = stats.setdefault("game_modes_played", {})
    modes[game_mode] = int(modes.get(game_mode, 0)) + 1
    maps = stats.setdefault("maps_played", {})
    maps[map_name] = int(maps.get(map_name, 0)) + 1
    save_profile_data(loaded_profile, save_path)

    def tick():
        if not session_state.get("running") or session_state.get("phase") != "playing":
            return
        now = time.monotonic()
        remaining = max(0, int(session_state["end_time"] - now))
        timer_var.set(f"In-game timer: {format_duration(remaining)}")
        if now < session_state.get("respawn_until", 0):
            kd_var.set(
                "Kills: {kills} | Deaths: {deaths} | Streak: {streak} | Longest: {longest}".format(
                    kills=session_state["kills"],
                    deaths=session_state["deaths"],
                    streak=session_state["current_streak"],
                    longest=session_state["longest_streak"],
                )
            )
            session_state["ticker_id"] = root.after(1000, tick)
            return
        kills_rate, deaths_rate = calculate_rates(attributes)
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
            session_state["current_streak"] += kill_count
            if session_state["current_streak"] > session_state["longest_streak"]:
                session_state["longest_streak"] = session_state["current_streak"]
            session_state["last_kill_time"] = now
            session_state["last_kill_indices"] = kill_indices
            session_state["last_kill_count"] = kill_count
            player_name = session_state.get("player_name", "Player")
            killed_names = [encounter[i] for i in kill_indices] if kill_indices else ["enemy"] * kill_count
            for enemy_name in killed_names:
                headshot = random.random() < 0.22
                if headshot:
                    session_state["headshots"] += 1
                suffix = " (Headshot)" if headshot else ""
                session_state["kill_feed"].append((now, f"{player_name} eliminated {enemy_name}{suffix}"))
            session_state["encounter_enemies"] = random.choices(ENEMY_POOL, k=random.randint(1, 6))
            session_state["encounter_last_update"] = now

        if now - session_state["death_minute_start"] >= 60:
            session_state["death_minute_start"] = now
            session_state["deaths_in_minute"] = 0

        if session_state["deaths_in_minute"] < 20 and random.random() < deaths_rate:
            session_state["deaths"] += 1
            session_state["deaths_in_minute"] += 1
            session_state["current_streak"] = 0
            session_state["respawn_until"] = now + 3

        kd_var.set(
            "Kills: {kills} | Deaths: {deaths} | Streak: {streak} | Longest: {longest}".format(
                kills=session_state["kills"],
                deaths=session_state["deaths"],
                streak=session_state["current_streak"],
                longest=session_state["longest_streak"],
            )
        )
        session_state["ticker_id"] = root.after(1000, tick)

    tick()

    session_state["after_id"] = root.after(
        duration_seconds * 1000,
        lambda: (
            add_kill_death_stats(loaded_profile, session_state["kills"], session_state["deaths"]),
            loaded_profile["player"]["stats"].update({"longest_kill_streak": session_state["longest_streak"]}),
            save_profile_data(loaded_profile, save_path),
            start_lobby_wait(
                root,
                session_state,
                status_var,
                timer_var,
                map_var,
                kd_var,
                loaded_profile,
                save_path,
            ),
        ),
    )


def on_start(root):
    # Confirm start and open the profile setup flow.
    if messagebox.askyesno("Start Game", "Would you like to start the game?"):
        open_profile_window(root)


def on_options():
    # Placeholder for a future options screen.
    pass


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
        profile = {"gamertag": gamertag, "attributes": values, "play_time_seconds": 0}
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

    window = tk.Toplevel(root)
    window.title("Player Profile")
    window.resizable(False, False)

    title = tk.Label(window, text=f"Gamertag: {gamertag}", font=("Segoe UI", 11))
    title.pack(padx=24, pady=(18, 10))

    time_label = tk.Label(window, text=f"Time Played: {format_duration(total_time)}", font=("Segoe UI", 10))
    time_label.pack(padx=24, pady=(0, 8))

    kd_label = tk.Label(
        window,
        text=f"Kills: {kills} | Deaths: {deaths} | K/D Ratio: {kd_ratio:.2f}",
        font=("Segoe UI", 10),
    )
    kd_label.pack(padx=24, pady=(0, 8))

    streak_label = tk.Label(window, text=f"Longest Kill Streak: {longest_streak}", font=("Segoe UI", 10))
    streak_label.pack(padx=24, pady=(0, 8))

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


def open_game_setup_window(root, loaded_profile, save_path, session_state, status_var, timer_var, map_var, kd_var):
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

    weapon_var = tk.StringVar(value=defaults.get("weapon", "Ak-47"))
    weapon_menu = tk.OptionMenu(weapon_frame, weapon_var, "Ak-47")
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
        start_game_session(root, session_state, status_var, timer_var, map_var, kd_var, loaded_profile, save_path)
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
            start_game_session(
                root,
                session_state,
                session_status_var,
                session_timer_var,
                session_map_var,
                session_kd_var,
                data,
                path,
            )

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

    options_button = tk.Button(menu_frame, text="Options", width=16, command=on_options)
    options_button.pack(pady=4)

    def on_about():
        messagebox.showinfo(
            "About",
            "Vibe coded by Jdog 1/2/2026.\nUse as inspiration to make a better Idle FPS game.",
        )

    about_button = tk.Button(menu_frame, text="About", width=16, command=on_about)
    about_button.pack(pady=4)

    def on_exit():
        if loaded_profile["data"] and loaded_profile["path"] and session_state.get("phase") == "playing":
            add_kill_death_stats(loaded_profile["data"], session_state.get("kills", 0), session_state.get("deaths", 0))
            loaded_profile["data"]["player"]["stats"].update(
                {"longest_kill_streak": session_state.get("longest_streak", 0)}
            )
        stop_game_session(root, session_state, session_status_var, session_timer_var, session_map_var, session_kd_var)
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

    root.resizable(False, False)
    root.protocol("WM_DELETE_WINDOW", on_exit)
    root.mainloop()


if __name__ == "__main__":
    main()
