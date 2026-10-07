#!/usr/bin/env bash
# Claude Code hook: keeps NotchFight up while at least one Claude session is working.
#   notch-hook.sh start <path/to/NotchFight.app>   (UserPromptSubmit)
#   notch-hook.sh wait <path/to/NotchFight.app>    (Notification: a permission prompt or a question is up)
#   notch-hook.sh work                              (PostToolUse, PostToolUseFailure, ElicitationResult, ...)
#   notch-hook.sh stop                              (Stop, StopFailure, SessionEnd)
# Each working session leaves a marker in ~/.config/notch-fight/sessions/<session_id> holding the
# PID of its `claude` process, rewritten on each prompt (its date: when that prompt started), and
# " waiting" after it while Claude waits for you (`wait`; `work` takes it off once a tool ran, keeping
# the date). Stop removes it; the panel retracts only when no live marker is left. The resident app
# watches the folder and shows or hides itself; SIGUSR1 tells it (or a non-resident one, which then
# quits) to look again now. The app also prunes markers of dead PIDs (a closed terminal never fires Stop).
set -u
DIR="$HOME/.config/notch-fight/sessions"; LOCK="$HOME/.config/notch-fight/.lock"
mkdir -p "$DIR"

# The session id from the hook's JSON on stdin; plain bash (no Python): `work` runs after every tool call.
input="$(cat)"
sid=""
[[ "$input" =~ \"session_id\"[[:space:]]*:[[:space:]]*\"([A-Za-z0-9_-]+)\" ]] && sid="${BASH_REMATCH[1]}"
M="$DIR/$sid"

# Debugging: when ~/.config/notch-fight/hook.log exists, every call is noted there (mode, event, type).
LOG="$HOME/.config/notch-fight/hook.log"
if [[ -e "$LOG" ]]; then
  ev=""; nt=""; tool=""
  [[ "$input" =~ \"hook_event_name\"[[:space:]]*:[[:space:]]*\"([A-Za-z]+)\" ]] && ev="${BASH_REMATCH[1]}"
  [[ "$input" =~ \"notification_type\"[[:space:]]*:[[:space:]]*\"([a-z_]+)\" ]] && nt="${BASH_REMATCH[1]}"
  [[ "$input" =~ \"tool_name\"[[:space:]]*:[[:space:]]*\"([A-Za-z_]+)\" ]] && tool="${BASH_REMATCH[1]}"
  echo "$(date +%T) ${1:-?} $ev $nt $tool ${sid:0:8}" >> "$LOG"
fi

# Nothing to take off: the common case after a tool call, done before taking the lock.
if [[ "${1:-}" == work ]]; then
  [[ -n "$sid" && -f "$M" ]] && grep -q waiting "$M" 2>/dev/null || exit 0
fi

# The `claude` process that ran this hook: walk up the process tree.
claude_pid() {
  local p=$PPID
  while [[ -n "$p" && "$p" -gt 1 ]]; do
    [[ "$(basename "$(ps -o comm= -p "$p" 2>/dev/null)")" == claude ]] && { echo "$p"; return; }
    p="$(ps -o ppid= -p "$p" 2>/dev/null | tr -d ' ')"
  done
}

# mark <content> [keep-date]: write the marker next to it and rename it, so the app's folder watcher
# sees it (a rewrite in place it would not); keep-date keeps the prompt's start as its date.
mark() {
  echo "$1" > "$DIR/.$sid.tmp" || return
  [[ -n "${2:-}" && -f "$M" ]] && touch -r "$M" "$DIR/.$sid.tmp"
  mv -f "$DIR/.$sid.tmp" "$M"
}
pid_of_marker() { local w=""; read -r w _ < "$M" 2>/dev/null; echo "$w"; }

# Serialize start/stop so a stop can't kill the app right as another session starts it.
for _ in $(seq 50); do mkdir "$LOCK" 2>/dev/null && break; sleep 0.05; done
trap 'rmdir "$LOCK" 2>/dev/null' EXIT

case "${1:-}" in
  start)
    [[ -n "$sid" ]] && mark "$(claude_pid)"
    # nf starts the app if it is not up (resident: the app then decides by itself); not resident, nf
    # decides: paused, quiet hours or screen sharing keep it hidden (the marker stays); with a "delay" it
    # shows only if this session is still working by then
    python3 "$(dirname "$0")/nf.py" _show "$2" "$sid" >/dev/null 2>&1 || true
    ;;
  wait)
    [[ -n "$sid" ]] || exit 0
    pid="$(pid_of_marker)"; [[ -n "$pid" ]] || pid="$(claude_pid)"
    mark "$pid waiting" keep
    # it shows at once, delay or not (the gate still applies)
    python3 "$(dirname "$0")/nf.py" _wait "${2:-}" >/dev/null 2>&1 || true
    ;;
  work)
    mark "$(pid_of_marker)" keep
    ;;
  stop)
    [[ -n "$sid" ]] && rm -f "$M"
    for f in "$DIR"/*; do
      [[ -e "$f" ]] || continue
      pid=""; read -r pid _ < "$f" 2>/dev/null
      if [[ -n "$pid" ]] && kill -0 "$pid" 2>/dev/null; then exit 0; fi   # someone still working
      # no PID recorded (process tree lookup failed): trust the marker for 2 h
      if [[ -z "$pid" && -n "$(find "$f" -mmin -120 2>/dev/null)" ]]; then exit 0; fi
      rm -f "$f"
    done
    pkill -USR1 -x NotchFight >/dev/null 2>&1 || true   # resident: hides; otherwise: retracts and quits
    ;;
esac
exit 0
