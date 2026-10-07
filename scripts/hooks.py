"""Add/remove the Notch Fight hooks in <claude dir>/settings.json (idempotent, keeps a backup).

    python3 scripts/hooks.py install <path/to/NotchFight.app>
    python3 scripts/hooks.py uninstall

Claude dirs: $NOTCH_FIGHT_CLAUDE_DIRS (colon-separated, e.g. ~/.claude-work:~/.claude-personal),
else $CLAUDE_CONFIG_DIR, else ~/.claude.
"""
import json, os, shlex, shutil, sys, time

MARKS = ('NotchFight', 'notch-hook.sh')   # every hook command we own mentions one of these
# the Notification types that mean Claude is waiting for you (its "matcher")
WAIT_TYPES = 'permission_prompt|elicitation_dialog|elicitation_url_dialog|agent_needs_input'

def claude_dirs():
    raw = os.environ.get('NOTCH_FIGHT_CLAUDE_DIRS') or os.environ.get('CLAUDE_CONFIG_DIR') or '~/.claude'
    return [os.path.expanduser(d) for d in raw.split(':') if d]

def load(path):
    if not os.path.exists(path): return {}
    with open(path) as fh: return json.load(fh)

def strip(settings):
    """Remove every hook entry that references NotchFight; drop groups left empty."""
    hooks = settings.get('hooks', {})
    for event in list(hooks):
        groups = []
        for g in hooks[event]:
            kept = [h for h in g.get('hooks', []) if not any(m in h.get('command', '') for m in MARKS)]
            if kept: groups.append(dict(g, hooks=kept))
        if groups: hooks[event] = groups
        else: del hooks[event]
    return settings

def save(settings, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if os.path.exists(path):
        backup = f'{path}.bak-notchfight-{time.strftime("%Y%m%d-%H%M%S")}'
        shutil.copy2(path, backup); print(f'backup: {backup}')
    tmp = path + '.tmp'
    with open(tmp, 'w') as fh: json.dump(settings, fh, indent=2); fh.write('\n')
    os.replace(tmp, path)

def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ('install', 'uninstall'): sys.exit(__doc__)
    for d in claude_dirs(): apply(os.path.join(d, 'settings.json'))

def apply(path):
    settings = strip(load(path))
    if sys.argv[1] == 'install':
        app = os.path.abspath(sys.argv[2])
        hook = shlex.quote(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'notch-hook.sh'))
        start = f'{hook} start {shlex.quote(app)}'
        stop = f'{hook} stop'
        hooks = settings.setdefault('hooks', {})
        hooks.setdefault('UserPromptSubmit', []).append({'hooks': [{'type': 'command', 'command': start, 'timeout': 5}]})
        for ev in ('Stop', 'StopFailure', 'SessionEnd'):
            hooks.setdefault(ev, []).append({'hooks': [{'type': 'command', 'command': stop, 'timeout': 5}]})
        # Claude waits for you (a permission prompt, an MCP question): the "needs you" alert; it comes off
        # once a tool has run or the question is answered (`work` is a no-op unless the session waits)
        wait, work = f'{hook} wait {shlex.quote(app)}', f'{hook} work'
        hooks.setdefault('Notification', []).append({'matcher': WAIT_TYPES, 'hooks': [{'type': 'command', 'command': wait, 'timeout': 5}]})
        hooks['Notification'].append({'matcher': 'elicitation_complete|elicitation_response', 'hooks': [{'type': 'command', 'command': work, 'timeout': 5}]})
        for ev in ('PostToolUse', 'PostToolUseFailure', 'ElicitationResult'):
            hooks.setdefault(ev, []).append({'hooks': [{'type': 'command', 'command': work, 'timeout': 5}]})
        print(f'hooks installed in {path} -> {app}')
    else:
        print(f'hooks removed from {path}')
    save(settings, path)

if __name__ == '__main__':
    main()
