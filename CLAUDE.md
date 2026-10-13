# Notch Fight — rules for agents

## Setup requests ("install this", "set it up", "remove it")
- Install: run `./install.sh` from the repo root. It checks requirements (macOS, `swiftc`,
  `python3`, Pillow — auto-installed), builds, and registers the hooks in `$CLAUDE_CONFIG_DIR/settings.json` (default `~/.claude`; several dirs via `NOTCH_FIGHT_CLAUDE_DIRS=~/.claude-work:~/.claude-personal`)
  pointing at this checkout. Idempotent; backs up settings.json. Report its output to the user.
- If the user has Vorssaint (a notch app with a wider bar), `install.sh` sets `"scale": 1.5` in
  `~/.config/notch-fight/config.json` unless a scale is already set; mention it in the report.
- If `swiftc` is missing, tell the user to run `xcode-select --install` (interactive, needs them).
- Not macOS: say the app is macOS-only; the generator still runs (`mkdir -p build && cd build && python3 ../src/build.py`).
- Uninstall: `./uninstall.sh` (`--purge` also removes `build/` and `~/.config/notch-fight`).
- Never hand-edit the hooks: `scripts/hooks.py` owns them (it matches entries mentioning `NotchFight` or `notch-hook.sh`).
- Showing / hiding clips ("hide the Maki clip", "only new clips I pick"): use `./clips.sh list | enable |
  disable <clip|theme> | mode enabled|disabled`, never edit the config by hand. The checklist (`./clips.sh`
  with no args) needs a real terminal: tell the user to run it themselves.
- Pausing it, quiet hours, hiding it while screen sharing, previewing a clip: `./nf pause <time> | resume |
  quiet HH:MM-HH:MM [weekdays] | share hide|show | delay <N>s | click close|next | menu on|off | preview <clip|theme> | status` (`nf` once installed).
  `nf pause` with no time is an interactive menu: give the time instead.
- Hooks added mid-session may need `/hooks` opened once to reload — tell the user.
- Clips inside Claude Code ("show it in the terminal", no notch): the mod in `mod/` (README "Inside Claude
  Code"): `claude --plugin-dir <repo>/mod`. Pixel-perfect only in kitty/Ghostty; elsewhere (Orca included) it draws cells: suggest `display: octant` + `rows: 16` with a font that has the octants (Cascadia Mono 2404.23+), else `sextant` (README "Inside Claude Code").

## Adding content ("add a One Piece fight", "add a clip to DBZ")
- New theme = new file `src/themes/<id>.py`, started with `nf new-theme` (see README "Adding a clip"); new
  clip in an existing theme = new `clip_<name>` + entry in that file's `CLIPS`. Hand both to the
  `theme-maker` agent (see "Who does what" below) and review what it brings.
- Then `ONLY=<theme> GIFS=1 ./build.sh` (only that theme, its transitions and its GIF, on top of the
  last build; a plain `./build.sh` rebuilds everything), look at `build/sheet_<theme>_<clip>.png` to
  check the frames, and commit the source + `media/clips/<theme>__*.gif`.
- If the clip is niche (a football club, a brand, an in-joke), ask whether it should ship off by default:
  `DEFAULT_OFF = True` in the theme, or `clip(..., off=True)` for one clip (README "Adding a clip").

## Who does what (models)
Cheap models do the volume, the main session decides and reviews. Delegate with the project agents in
`.claude/agents/`, which pin their model:
- **New themes and clips** from an idea → `theme-maker` (Haiku 5.5). A whole theme costs well under a
  dollar. Several ideas → several theme-makers in parallel, one worktree each.
- **Refactors across themes** (onto engine code, pixel-identical) and **scripts with a clear spec** →
  `theme-refactor` (Sonnet 5.5).
- **The main session** (whatever model it runs): designing an engine API or the toolkit, the Swift app,
  anything that needs judgment across the codebase; and **reviewing and integrating** what the agents bring.

Each agent works in its own worktree: `git worktree add -b <branch> ../nf-wt-<name> HEAD` (the Agent tool's
`isolation: "worktree"` only works when the session was started inside this repo). Integrating:
- read the report, then look yourself: `nf check <theme>`, and `python3 scripts/sheet.py <theme> <clip>
  [frames]` for the beats it calls weak; send it back with specific fixes if a beat doesn't read;
- `git cherry-pick` its commit, then `python3 tests/test_snapshots.py --update` (a new theme: only "N new";
  a refactor: nothing may change), `FIRST=<theme>__<clip> ONLY=<theme> GIFS=1 ./build.sh`, and commit the
  snapshot and the GIF; remove the worktree and its branch.

Long sessions cost mostly in re-read context, not in the model: start a fresh session for each new batch
of work rather than piling everything into one.

## Rules

- **Claude is always the protagonist** of every clip.
- **Every clip starts and ends on its theme's neutral pose** (the loop keyframe), so the
  theme-to-theme transitions line up; a new theme needs its own neutral pose (transitions are automatic).
- **After creating a clip, make it play first** so the dev sees it immediately.
  `./build.sh` does this automatically for any clip that was not in the previous build
  (writes `~/.config/notch-fight/config.json` → `{"first": ["<theme>__<clip>", ...]}`; several new
  clips are all queued, in order). If the clip was already generated by a manual run it is
  not "new" for the build — then force it: `FIRST=<theme>__<clip>[,...] ./build.sh`. Tell the dev which clip was set first.
- Regenerate previews with `GIFS=1 ./build.sh` and commit `media/clips/*.gif` with the change.
- Builds must stay reproducible: seed randomness with `zlib.crc32`, never `hash()`.
- **Sub-themes** (same franchise, different loop keyframe — e.g. `naruto-edo` under Naruto) are their
  own theme: id `<franchise>-<sub>`, file `src/themes/<franchise>_<sub>.py`. They may import sprites and
  helpers from the sibling theme module (`from themes.nrt import NARU`) instead of moving them to engine.
- **One file per theme** in `src/themes/`. Theme-specific sprites, colours (`PAL.update`) and effects
  (`@fx('name')`) live in that file; only move something to `src/engine/` when a second theme needs it.
  Effect names are global — registering one twice fails loudly.
- A refactor that should not change visuals must keep the rendered frames pixel-identical:
  `tests/test_snapshots.py` checks every clip against `tests/snapshots.txt` and names the ones that
  changed. When a change is meant (a new clip, a better sprite), record it with
  `python3 tests/test_snapshots.py --update` and commit `tests/snapshots.txt` with it.
- Every clip's frame N must be its frame 0 (`tests/test_loops.py`): whatever moves in the neutral pose
  needs a period that divides the clip's length. Use `engine/loop.py` (`loop.frame`, `loop.wave`,
  `loop.period`, `loop.rng`) and the ambient effects in `engine/ambient.py` rather than raw `f`.
- To look at frames while making a clip: `python3 scripts/sheet.py <theme> [clip] [frames]` (no build).
- Build people with `figure(spec, pose)` (`engine/people.py`) and its `POSES`, adding a theme's own poses
  and small painters for what's particular to a character, rather than a new pose-builder per theme.
- Start a new theme with `nf new-theme <id> [--sub-of <theme>] [--people] [--2.5d] [--no-fight]`: it writes a
  skeleton that already loops, passes `nf check` and uses the toolkit below, adds its README row, and shows
  the sheet; then fill in its TODOs.
- For depth (2.5D: a court, a pitch, a dance floor), use a `Stage` (`engine/stage25.py`): `proj`, `place`
  (far figures smaller / faded), `shadow`, `back_to_front`, `quad` / `line` on the floor, `arc` and `ring`
  for paths, rather than a projection of the theme's own.
- Before calling a theme done, run `nf check <theme>`: it must report nothing new. Time text with
  `engine/director.py` (`hold`, `cue`) and lay it out with `text_block` / `closeup` rather than by hand.
