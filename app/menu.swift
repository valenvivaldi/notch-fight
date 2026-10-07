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

        let preview = NSMenu()
        for t in run(["_themes"]).1.split(separator: "\n").map(String.init) where !t.isEmpty {
            add(preview, t, #selector(act(_:)), ["preview", t])
        }
        sub(menu, "Preview", preview)
        menu.addItem(.separator())

        let hide = (cfg["pauseOnShare"] as? Bool) ?? true
        let share = NSMenu()
        add(share, "Hide the panel", #selector(act(_:)), ["share", "hide"], on: hide)
        add(share, "Keep showing it", #selector(act(_:)), ["share", "show"], on: !hide)
        sub(menu, "While sharing the screen", share)

        let next = (cfg["click"] as? String) == "next"
        let click = NSMenu()
        add(click, "Closes it", #selector(act(_:)), ["click", "close"], on: !next)
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
        let app = NSApplication.shared
        app.delegate = menu
        app.setActivationPolicy(.accessory)
        app.run()
    }
}
