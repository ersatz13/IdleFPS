This is an idle game that plays a First Person Shooter game in the background while you work.
features ample stat tracking and level progression built-in. 
How to play
1. select play
2. select create new
3. build your character and give it a name
4. select default loadout and gamemode
5. select quickstart
6. now you are playing

Idle FPS Change List (session summary)

UI / Tabs
- Added a dedicated Loadout tab; Start/Play now routes to Loadout, and loading a profile can open the Loadout tab.
- Loadout tab now guards against missing profile and shows a message when no profile is loaded.
- Profile view refresh callback saved; Save Loadout returns to Profile tab and refreshes view.
- All tabs auto-refresh when selected (Profile, Loadout, Options, Achievements, History, Match).
- Match tab reopens the match/lobby view when a session is active.
- Added a Leaderboard tab with top 100 gamertags and player rank section.

History
- Match History now shows the last 50 matches in a scrollable list.

Debug / Options
- Debug controls are hidden unless the user types "doritos" while Options is open.
- Debug listener now uses global key binding and focuses the Options window.
- Debug listener now expires after 10 seconds if the password is not entered.

Match / Profile Behavior
- Stopped any running match session when a new profile is loaded to prevent mixed profile status updates.
- Nukes now end matches in live play only; offline progression is unaffected.
- Offline progression can now exceed 25 kill streaks (cap removed for offline only).

Ribbons
- Ribbons now use per-achievement unique palettes (deterministic) with 5 vertical color sections.
- Ribbon text color changed to black.
- Ribbon palette tuned to more earthy, subdued tones.

Leaderboard
- Generated 100 deterministic gamertags (English/Spanish/Japanese/Russian + humorous variants, mixed case, symbols).
- #1 score set to 16,420,069 with tight 1.0?1.2% decay for top 10 and 1?2% for ranks 11?100.
- Leaderboard rows show rank label (Prestige/Master of War), time played, and XP.
- Player footer shows rank, XP, kills, and prestige/master label plus time.
- Leaderboard time now follows XP pacing rules (8 hours per prestige cycle, 4 hours per master level).
- Master of War 1000 animated name styling applied to any top?100 entry at that level.
- Leaderboard simulates offline progression for top 100 with a "reticulating splines" loading screen.
- Top?100 simulation runs at half XP rate; player earns full rate only when currently in top 100.
- Leaderboard refreshes after match end when active.
- Rank progression is weighted to climb quickly from 440,000 to 200,000.

Progression
- XP table tuned: LEVEL_XP_BASE=50, LEVEL_XP_STEP=25, MASTER_LEVEL_XP=20000.

Match View
- Enemy visuals changed to red stick figures.
- Player character replaced by a single tall, narrow gun silhouette.
- Kill feed moved to the bottom-left.
- Minimap experiment added then removed.

Versioning
- Title updated to Idle FPS version 0.0.8.7.
