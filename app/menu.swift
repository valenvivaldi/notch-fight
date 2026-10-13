import AppKit

// Notch Fight's menu bar icon (`nf menu on`): pause / resume, preview a theme, and the settings, without
// a terminal. Every action runs `nf` (scripts/nf.py next to the build), which stays the one place that
// knows how; the menu is rebuilt each time it opens, so it always shows the current state. Only the
// gate, asked every 15 s and on every open, runs in-process (Gate.swift) instead of through Python.
final class Menu: NSObject, NSApplicationDelegate, NSMenuDelegate {
    var item: NSStatusItem!
    let root = Bundle.main.bundleURL.deletingLastPathComponent().deletingLastPathComponent()
    var nf: String { root.appendingPathComponent("scripts/nf.py").path }

    func applicationDidFinishLaunching(_ n: Notification) {
        item = NSStatusBar.system.statusItem(withLength: NSStatusItem.squareLength)
        let menu = NSMenu(); menu.delegate = self; item.menu = menu
        refreshIcon()
        Timer.scheduledTimer(withTimeInterval: 15, repeats: true) { [weak self] _ in self?.refreshIcon() }
    }

    @discardableResult
    func run(_ args: [String]) -> (Int32, String) {
        let p = Process(), out = Pipe()
        p.executableURL = URL(fileURLWithPath: "/usr/bin/env"); p.arguments = ["python3", nf] + args
        p.standardOutput = out; p.standardError = out
        guard (try? p.run()) != nil else { return (1, "") }
        let data = out.fileHandleForReading.readDataToEndOfFile(); p.waitUntilExit()
        return (p.terminationStatus, String(data: data, encoding: .utf8)?.trimmingCharacters(in: .whitespacesAndNewlines) ?? "")
    }

    var config: [String: Any] { Gate.loadConfig() }

    // The icon: a sparkle when the panel may show, a pause sign when it is hidden (paused, quiet, sharing).
    func refreshIcon() {
        DispatchQueue.global(qos: .utility).async {
            let (ok, why) = Gate.check()
            DispatchQueue.main.async {
                let name = ok ? "sparkle" : "pause.circle"
                let img = NSImage(systemSymbolName: name, accessibilityDescription: "Notch Fight")
                img?.isTemplate = true
                self.item.button?.image = img
                self.item.button?.toolTip = ok ? "Notch Fight" : "Notch Fight: \(why)"
            }
        }
    }

    func menuNeedsUpdate(_ menu: NSMenu) {
        menu.removeAllItems()
        let cfg = config
        let (ok, why) = Gate.check()
        add(menu, ok ? "Notch Fight: on" : "Notch Fight: \(why)", nil)

        let pause = NSMenu()
        for (label, arg) in [("15 minutes", "15m"), ("30 minutes", "30m"), ("1 hour", "1h"), ("4 hours", "4h"),
                             ("8 hours", "8h"), ("Until I resume", "forever")] {
            add(pause, label, #selector(act(_:)), ["pause", arg])
        }
        sub(menu, "Pause", pause)
        let paused = FileManager.default.fileExists(atPath: Gate.pausedURL.path)
        add(menu, "Resume", paused ? #selector(act(_:)) : nil, ["resume"])
        menu.addItem(.separator())

        // one nf call for the themes (on / off / some) and the stats
        let data = (try? JSONSerialization.jsonObject(with: Data(run(["_menu"]).1.utf8))) as? [String: Any] ?? [:]
        let themes = (data["themes"] as? [[String]] ?? []).filter { $0.count == 2 }.map { (name: $0[0], state: $0[1]) }

        let preview = NSMenu()
        grouped(preview, themes) { m, fr, members in
            if members.count == 1 { self.add(m, members[0].name, #selector(self.act(_:)), ["preview", members[0].name]); return }
            let sm = NSMenu()
            for t in members { self.add(sm, t.name, #selector(self.act(_:)), ["preview", t.name]) }
            self.sub(m, fr, sm)
        }
        sub(menu, "Preview", preview)
        sub(menu, "Themes", themesMenu(themes))
        let stats = NSMenu()
        for line in data["stats"] as? [String] ?? [] { add(stats, line, nil) }
        stats.addItem(.separator())
        add(stats, "Reset the stats…", #selector(resetStats))
        sub(menu, "Stats", stats)
        menu.addItem(.separator())

        let hide = (cfg["pauseOnShare"] as? Bool) ?? true
        let share = NSMenu()
        add(share, "Hide the panel", #selector(act(_:)), ["share", "hide"], on: hide)
        add(share, "Keep showing it", #selector(act(_:)), ["share", "show"], on: !hide)
        sub(menu, "While sharing the screen", share)

        let next = (cfg["click"] as? String) == "next"
        let click = NSMenu()
        add(click, "Hides it (until the next prompt)", #selector(act(_:)), ["click", "close"], on: !next)
        add(click, "Skips to the next clip (double click closes)", #selector(act(_:)), ["click", "next"], on: next)
        sub(menu, "A click on the panel", click)

        let d = (cfg["delay"] as? NSNumber)?.intValue ?? 0
        let delay = NSMenu()
        for (label, secs) in [("Off", 0), ("5 seconds", 5), ("10 seconds", 10), ("30 seconds", 30), ("1 minute", 60)] {
            add(delay, label, #selector(act(_:)), ["delay", secs == 0 ? "off" : "\(secs)s"], on: d == secs)
        }
        sub(menu, "Show after Claude works for", delay)

        if let q = cfg["quiet"] as? [String: Any], let f = q["from"] as? String, let t = q["to"] as? String {
            add(menu, "Quiet hours: \(f)-\(t)\((q["days"] as? String) == "weekdays" ? ", weekdays" : "")", nil)
            add(menu, "Turn quiet hours off", #selector(act(_:)), ["quiet", "off"])
        } else {
            add(menu, "Quiet hours: off (nf quiet 22:00-08:00)", nil)
        }
        menu.addItem(.separator())
        add(menu, "Choose clips…", #selector(chooseClips))
        add(menu, "Remove this icon", #selector(act(_:)), ["menu", "off"])
        add(menu, "Quit", #selector(NSApplication.terminate(_:)), target: NSApp)
    }

    func add(_ m: NSMenu, _ title: String, _ action: Selector?, _ args: [String] = [], on: Bool = false, target: AnyObject? = nil) {
        let i = NSMenuItem(title: title, action: action, keyEquivalent: "")
        i.target = target ?? self; i.representedObject = args; i.state = on ? .on : .off
        if action == nil { i.isEnabled = false }
        m.addItem(i)
    }
    func sub(_ m: NSMenu, _ title: String, _ s: NSMenu) {
        let i = NSMenuItem(title: title, action: nil, keyEquivalent: ""); i.submenu = s; m.addItem(i)
    }

    @objc func act(_ sender: NSMenuItem) {
        guard let args = sender.representedObject as? [String] else { return }
        DispatchQueue.global(qos: .userInitiated).async {
            self.run(args)
            DispatchQueue.main.async { self.refreshIcon() }
        }
    }

    // Which themes play: a check per theme (a dash when only some of its clips are on); a click turns it on
    // or, when it is on, off. Themes of one franchise (dbz, dbz-buu, ...) share a submenu, and the
    // franchises are split alphabetically into a few groups, so the list never runs off the screen.
    func themesMenu(_ themes: [(name: String, state: String)]) -> NSMenu {
        let m = NSMenu()
        let names = themes.map(\.name)
        add(m, "Turn them all on", #selector(act(_:)), ["clips", "all", "on"])
        add(m, "Turn them all off", #selector(act(_:)), ["clips", "all", "off"])
        add(m, "Back to the defaults", #selector(act(_:)), ["clips", "defaults"])
        let arg = names.filter { $0 == "arg" || $0.hasPrefix("arg-") }
        if !arg.isEmpty { add(m, "Only the Argentine ones", #selector(act(_:)), ["clips", "only"] + arg) }
        m.addItem(.separator())
        grouped(m, themes) { g, fr, members in
                if members.count == 1 { self.themeItem(g, members[0].name, [members[0].name], members[0].state); return }
                let all = members.map(\.state)
                let s = all.allSatisfy { $0 == "on" } ? "on" : all.allSatisfy { $0 == "off" } ? "off" : "some"
                let sm = NSMenu()
                self.themeItem(sm, "All of \(fr)", members.map(\.name), s)
                sm.addItem(.separator())
                for t in members { self.themeItem(sm, t.name, [t.name], t.state) }
                let i = NSMenuItem(title: fr, action: nil, keyEquivalent: ""); i.submenu = sm; i.state = self.mark(s); g.addItem(i)
        }
        return m
    }

    // Themes by franchise (the name before the first "-": dbz, dbz-buu, ...), the franchises split
    // alphabetically into about six submenus ("A–C", ...); `item` adds one franchise to its submenu.
    func grouped(_ m: NSMenu, _ themes: [(name: String, state: String)],
                 _ item: (NSMenu, String, [(name: String, state: String)]) -> Void) {
        let franchise = { (t: String) in String(t.split(separator: "-").first ?? Substring(t)) }
        var groups: [(String, [(name: String, state: String)])] = []
        for t in themes {
            if let i = groups.firstIndex(where: { $0.0 == franchise(t.name) }) { groups[i].1.append(t) } else { groups.append((franchise(t.name), [t])) }
        }
        let size = max(8, Int((Double(groups.count) / 6).rounded(.up)))
        for start in stride(from: 0, to: groups.count, by: size) {
            let chunk = Array(groups[start..<min(start + size, groups.count)])
            let g = NSMenu()
            for (fr, members) in chunk { item(g, fr, members) }
            let first = chunk.first!.0.prefix(1).uppercased(), last = chunk.last!.0.prefix(1).uppercased()
            sub(m, first == last ? first : "\(first)–\(last)", g)
        }
    }
    func mark(_ state: String) -> NSControl.StateValue { state == "on" ? .on : state == "some" ? .mixed : .off }
    func themeItem(_ m: NSMenu, _ title: String, _ names: [String], _ state: String) {
        add(m, title, #selector(act(_:)), ["clips", state == "on" ? "disable" : "enable"] + names)
        m.items.last?.state = mark(state)
    }

    @objc func resetStats() {
        NSApp.activate(ignoringOtherApps: true)
        let a = NSAlert()
        a.messageText = "Reset the stats?"
        a.informativeText = "Plays, panel time and waits go back to zero. Which clips have played this round is kept."
        a.addButton(withTitle: "Reset"); a.addButton(withTitle: "Cancel")
        if a.runModal() == .alertFirstButtonReturn { run(["stats", "reset"]) }
    }

    // The checklist needs a real terminal: open one running `nf clips`.
    @objc func chooseClips() {
        let script = FileManager.default.temporaryDirectory.appendingPathComponent("notch-fight-clips.command")
        let body = "#!/bin/bash\nexec python3 '\(nf)' clips\n"
        try? body.write(to: script, atomically: true, encoding: .utf8)
        chmod(script.path, 0o755)
        NSWorkspace.shared.open(script)
    }
}

// Built together with Gate.swift (-parse-as-library), so the entry point is explicit.
@main enum MenuMain {
    static let menu = Menu()
    static func main() {
        // --print-menu: build the menu as when it opens and print it as a tree (✓ on, – some), then exit.
        // For tests and checks: NOTCH_FIGHT_CONFIG points it at another config.
        if CommandLine.arguments.contains("--print-menu") {
            let m = NSMenu(); menu.menuNeedsUpdate(m)
            func dump(_ m: NSMenu, _ depth: Int) {
                for i in m.items {
                    if i.isSeparatorItem { print(String(repeating: "  ", count: depth) + "---"); continue }
                    let mark = i.state == .on ? "✓ " : i.state == .mixed ? "– " : ""
                    print(String(repeating: "  ", count: depth) + mark + i.title + (i.isEnabled || i.submenu != nil ? "" : " (label)"))
                    if let s = i.submenu { dump(s, depth + 1) }
                }
            }
            dump(m, 0); exit(0)
        }
        let app = NSApplication.shared
        app.delegate = menu
        app.setActivationPolicy(.accessory)
        app.run()
    }
}
