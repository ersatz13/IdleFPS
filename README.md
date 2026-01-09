This is an idle game that plays a First Person Shooter game in the background while you work.
features ample stat tracking and level progression built-in. 
How to play
1. select play
2. select create new
3. build your character and give it a name
4. select default loadout and gamemode
5. select quickstart
6. now you are playing

you can now view the player profile and inspect results in summaries

you will now be earning xp, leveling up weapons, earning camos, and achievements while the game runs.  

UI / Tabs
- Added a dedicated Loadout tab; Start/Play now routes to Loadout, and loading a profile can open the Loadout tab.
- Loadout tab now guards against missing profile and shows a message when no profile is loaded.
- Profile view refresh callback saved; Save Loadout returns to Profile tab and refreshes view.
- All tabs auto-refresh when selected (Profile, Loadout, Options, Achievements, History, Match).
- Match tab reopens the match/lobby view when a session is active.

History
- Match History now shows the last 50 matches in a scrollable list.

Debug / Options
- Debug controls are hidden unless the user types "doritos" while Options is open.
- Debug listener now uses global key binding and focuses the Options window.
- Debug listener now expires after 10 seconds if the password is not entered.

Match / Profile Behavior
- Stopped any running match session when a new profile is loaded to prevent mixed profile status updates.
- Nukes now end matches in live play only; offline progression is unaffected.

Ribbons
- Ribbons now use per-achievement unique palettes (deterministic) with 5 vertical color sections.
- Ribbon text color changed to black.
- Ribbon palette tuned to more earthy, subdued tones.

Versioning
- Title updated to Idle FPS version 0.0.8.7.
