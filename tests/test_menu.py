"""The menu bar icon's menu (app/menu.swift), built as when it opens and printed with --print-menu against
a temporary config: the themes with their checks, grouped, the bulk actions, and the stats.
Skipped when there is no build or no Mac."""
import json, os, platform, subprocess, tempfile, unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
BIN = os.path.join(ROOT, 'build', 'NotchFightMenu.app', 'Contents', 'MacOS', 'NotchFightMenu')
CLIPS = os.path.join(ROOT, 'build', 'clips')
RUN = platform.system() == 'Darwin' and os.path.exists(BIN) and os.path.isdir(CLIPS)

def menu(cfg):
    d = tempfile.mkdtemp(); path = os.path.join(d, 'config.json'); json.dump(cfg, open(path, 'w'))
    env = dict(os.environ, NOTCH_FIGHT_CONFIG=path)
    return subprocess.run([BIN, '--print-menu'], env=env, capture_output=True, text=True, timeout=60).stdout.splitlines()

def section(lines, title):
    """The lines under a top-level item, up to the next top-level one."""
    i = lines.index(title); out = []
    for l in lines[i + 1:]:
        if not l.startswith('  '): break
        out.append(l)
    return out

@unittest.skipUnless(RUN, 'needs macOS and ./build.sh')
class Menu(unittest.TestCase):
    def setUp(self):
        self.themes = sorted({c.split('__')[0] for c in os.listdir(CLIPS) if not c.startswith('.')})

    def test_themes_are_grouped_and_checked(self):
        off = self.themes[0]
        lines = section(menu({'newClips': 'disabled', 'enabled': [c for c in os.listdir(CLIPS) if not c.startswith(off + '__')]}), 'Themes')
        groups = [l.strip() for l in lines if l.startswith('  ') and not l.startswith('    ') and ('–' in l or len(l.strip()) == 1)]
        self.assertTrue(3 <= len(groups) <= 8, groups)
        for action in ('Turn them all on', 'Turn them all off', 'Back to the defaults'): self.assertIn('  ' + action, lines)
        items = [l.strip() for l in lines]
        self.assertIn(off, items)                                  # unchecked
        self.assertNotIn('✓ ' + off, items)
        self.assertIn('✓ ' + self.themes[-1], items)

    def test_a_franchise_shares_a_submenu(self):
        lines = section(menu({}), 'Themes')
        if not any(t.startswith('dbz-') for t in self.themes): self.skipTest('needs dbz sub-themes')
        i = next(k for k, l in enumerate(lines) if l.strip().endswith(' dbz') or l.strip() == 'dbz')
        below = [l.strip() for l in lines[i + 1:i + 8]]
        self.assertTrue(any('All of dbz' in l for l in below), below)

    def test_stats_are_listed_with_a_reset(self):
        lines = [l.strip() for l in section(menu({}), 'Stats')]
        self.assertTrue(any(l.startswith('Panel up:') for l in lines), lines)
        self.assertIn('Reset the stats…', lines)

    def test_preview_is_grouped_too(self):
        lines = section(menu({}), 'Preview')
        self.assertLessEqual(len([l for l in lines if not l.startswith('    ')]), 8)

if __name__ == '__main__':
    unittest.main()
