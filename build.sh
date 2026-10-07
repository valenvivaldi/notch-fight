#!/usr/bin/env bash
# Generates every clip + transition frame and builds NotchFight.app into build/.
# ONLY=<theme|theme__clip>[,...] ./build.sh re-renders just those clips (and their themes' transitions)
# on top of the last build; GIFS=1 then refreshes only their previews.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
OUT="$ROOT/build"; APP="$OUT/NotchFight.app"
mkdir -p "$OUT"
before="$(ls "$OUT/clips" 2>/dev/null || true)"
(cd "$OUT" && python3 "$ROOT/src/build.py")

# Rule: a newly created clip plays FIRST so the dev sees it right away.
# All new clips are queued first, in order. FIRST=a__x,b__y ./build.sh forces a list; FIRST=none skips.
new="$(comm -13 <(echo "$before" | sort) <(ls "$OUT/clips" | sort) | paste -sd, -)"
[[ -z "$before" ]] && new=""          # first build ever: everything is "new", pick nothing
FIRST="${FIRST:-$new}"
if [[ -n "$FIRST" && "$FIRST" != "none" ]]; then
  mkdir -p "$HOME/.config/notch-fight"
  # update only "first": the panel-shape keys (fillet, stretch, widthTweak) are the user's
  python3 - "$FIRST" "$HOME/.config/notch-fight/config.json" <<'PY'
import json, sys, os
names, path = sys.argv[1].split(','), sys.argv[2]
cfg = json.load(open(path)) if os.path.exists(path) else {}
cfg['first'] = names
open(path, 'w').write(json.dumps(cfg, indent=2) + '\n')
PY
  echo "First clip set to $FIRST (~/.config/notch-fight/config.json)"
fi

# The app is updated in place, not rebuilt: rsync copies each folder's frames.png + count (and the
# .default-off marks) that changed, and drops what's gone (the loose NNN.png of an older build too). The Swift is compiled only when its source is newer than the binary.
mkdir -p "$APP/Contents/MacOS" "$APP/Contents/Resources"
cp "$ROOT/app/Info.plist" "$APP/Contents/"
for d in clips transitions overlays; do
  rsync -a --delete --delete-excluded --include='*/' --include='frames.png' --include='count' --include='.default-off' \
    --exclude='*' "$OUT/$d/" "$APP/Contents/Resources/$d/"
done
# stale <binary> <sources...>: missing, or older than one of its sources (only then is the Swift compiled)
stale() { local bin="$1"; shift; [[ -x "$bin" ]] || return 0; for s in "$@"; do [[ "$s" -nt "$bin" ]] && return 0; done; return 1; }
# pin the deployment target: some toolchains default to a macOS newer than the running one (LaunchServices error -10825)
swift() { swiftc -O -target "$(uname -m)-apple-macos13.0" "$@"; }
SRC=("$ROOT/app/main.swift" "$ROOT/app/Gate.swift" "$ROOT/app/State.swift")
stale "$APP/Contents/MacOS/NotchFight" "${SRC[@]}" && swift "${SRC[@]}" -o "$APP/Contents/MacOS/NotchFight"
codesign -s - --force "$APP" >/dev/null 2>&1
# a resident app that is up picks up the new build: it retracts and quits, and starts again (hidden, or
# straight back out with the new clips first if a Claude session is working)
if pgrep -x NotchFight >/dev/null && python3 -c 'import sys; sys.path.insert(0, sys.argv[1]); import nf; sys.exit(not nf.resident())' "$ROOT/scripts"; then
  pkill -x NotchFight; for _ in $(seq 40); do pgrep -x NotchFight >/dev/null || break; sleep 0.1; done
  # LaunchServices can still be letting go of the old one (error -600): try again for a moment
  for _ in 1 2 3 4 5; do open -g "$APP" 2>/dev/null && break; sleep 0.5; done || echo "Could not restart the app: open -g $APP"
fi

# the menu bar icon (nf menu on): a tiny separate app, so it can stay up while the panel comes and goes
MENU="$OUT/NotchFightMenu.app"
mkdir -p "$MENU/Contents/MacOS"
cp "$ROOT/app/MenuInfo.plist" "$MENU/Contents/Info.plist"
MSRC=("$ROOT/app/menu.swift" "$ROOT/app/Gate.swift")   # -parse-as-library: menu.swift has an @main
if stale "$MENU/Contents/MacOS/NotchFightMenu" "${MSRC[@]}"; then
  swift -parse-as-library "${MSRC[@]}" -o "$MENU/Contents/MacOS/NotchFightMenu"
  codesign -s - --force "$MENU" >/dev/null 2>&1
fi

if [[ "${GIFS:-0}" == "1" ]]; then   # GIFS=1 ./build.sh refreshes media/clips previews
  tmp="$(mktemp -d)"
  while read -r n; do [[ -z "$n" ]] && continue; d="$tmp/$n"          # only the clips this run rendered
    python3 "$ROOT/scripts/frames.py" unpack "$OUT/clips/$n" "$d"
    ffmpeg -y -loglevel error -framerate 20 -i "$d/%03d.png" \
      -vf "scale=iw*2:ih*2:flags=neighbor,split[a][b];[a]palettegen=max_colors=128[p];[b][p]paletteuse=dither=none" \
      -loop 0 "$ROOT/media/clips/$n.gif"
  done < "$OUT/.built"
  rm -rf "$tmp"
fi
echo "Built $APP"
