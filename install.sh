#!/usr/bin/env bash
# Installs Notch Fight: checks requirements, builds the app, registers the Claude Code hooks.
# Safe to re-run (hooks are replaced, never duplicated; settings.json is backed up).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
ok(){ printf '  \033[32m✓\033[0m %s\n' "$1"; }
fail(){ printf '  \033[31m✗\033[0m %s\n' "$1"; exit 1; }

echo "Checking requirements"
[[ "$(uname)" == "Darwin" ]] || fail "macOS only (the app uses AppKit + the notch API). The generator in src/ runs anywhere."
ok "macOS $(sw_vers -productVersion)"
command -v swiftc >/dev/null || fail "swiftc not found — run: xcode-select --install"
ok "swiftc"
command -v python3 >/dev/null || fail "python3 not found"
ok "python3 $(python3 -c 'import sys;print(".".join(map(str,sys.version_info[:2])))')"
if ! python3 -c "import PIL" 2>/dev/null; then
  echo "  … installing Pillow (python3 -m pip install --user pillow)"
  python3 -m pip install --user --quiet pillow || fail "could not install Pillow"
fi
ok "Pillow"
command -v ffmpeg >/dev/null && ok "ffmpeg (only needed for GIF previews)" || echo "  - ffmpeg not found (optional, only for GIFS=1 ./build.sh)"
python3 - <<'PY' || echo "  - no notch detected on this Mac: the panel will hang from the top centre instead"
import subprocess,sys
out=subprocess.run(["system_profiler","SPDisplaysDataType"],capture_output=True,text=True).stdout
sys.exit(0 if "Liquid Retina XDR" in out or "Built-in Liquid Retina" in out else 1)
PY

echo "Building"
FIRST=none "$ROOT/build.sh" | tail -1

# Vorssaint draws its own wider bar around the notch: a 1.5x panel matches it better.
# Applied only when the user has not chosen a scale yet.
if [[ -d /Applications/Vorssaint.app || -d "$HOME/Applications/Vorssaint.app" ]] || pgrep -xq Vorssaint; then
  python3 - "$HOME/.config/notch-fight/config.json" <<'PY'
import json, os, sys
path = sys.argv[1]; os.makedirs(os.path.dirname(path), exist_ok=True)
cfg = json.load(open(path)) if os.path.exists(path) else {}
if 'scale' in cfg:
    print(f"  - Vorssaint detected; keeping your scale {cfg['scale']}")
else:
    cfg['scale'] = 1.5
    open(path, 'w').write(json.dumps(cfg, indent=2) + '\n')
    print("  ✓ Vorssaint detected: panel scale set to 1.5 (change \"scale\" in ~/.config/notch-fight/config.json)")
PY
fi

echo "Registering Claude Code hooks"
python3 "$ROOT/scripts/hooks.py" install "$ROOT/build/NotchFight.app"

echo "Linking the nf command"
BIN="$HOME/.local/bin"; mkdir -p "$BIN"
if [[ -L "$BIN/nf" && "$(readlink "$BIN/nf")" == "$ROOT/nf" ]] || [[ ! -e "$BIN/nf" ]]; then
  ln -sfn "$ROOT/nf" "$BIN/nf"; ok "nf -> $BIN/nf (nf help)"
  case ":$PATH:" in *":$BIN:"*) ;; *) echo "  - $BIN is not in your PATH: add  export PATH=\"\$HOME/.local/bin:\$PATH\"  to your shell profile";; esac
else
  echo "  - $BIN/nf already exists and is not ours: left alone (run $ROOT/nf directly)"
fi

# The menu bar icon (pause, preview, settings without a terminal): offered, never forced.
if [[ -t 0 && -t 1 ]]; then
  read -r -p "Add a menu bar icon (pause, preview, settings)? [y/N] " ans
  [[ "$ans" =~ ^[yY] ]] && "$ROOT/nf" menu on
else
  echo "  - for a menu bar icon: nf menu on"
fi

# Which clips play: offer the checklist when a person is at the terminal (never when scripted).
if [[ -t 0 && -t 1 ]]; then
  read -r -p "Choose which clips to show now? [y/N] " ans
  [[ "$ans" =~ ^[yY] ]] && "$ROOT/nf" clips
else
  echo "  - to choose which clips play: nf clips (in a terminal)"
fi

cat <<MSG

Done. Send any prompt to Claude Code and the fight drops out of the notch;
it retracts when Claude finishes. Click it to dismiss until your next prompt.
The app then stays up, hidden, between prompts (nf resident on: also at login; off: not at all).
If it does not appear in an already-open Claude Code session, open /hooks once (reloads config).
Choose clips: ./clips.sh   Uninstall: ./uninstall.sh
MSG
