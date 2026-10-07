import AppKit
import QuartzCore

// Drops a black pixel-art fight from under the MacBook notch. Click it to retract and quit.
final class NotchPanel: NSPanel {
    override var canBecomeKey: Bool { true }
    override func constrainFrameRect(_ r: NSRect, to s: NSScreen?) -> NSRect { r }
}

final class App: NSObject, NSApplicationDelegate {
    var win: NotchPanel!
    let art = CALayer()
    // Clips are grouped by theme (dir name "<theme>__<clip>"). Clips of one theme share a
    // loop keyframe and chain seamlessly; switching theme plays transitions/<from>__out, then <to>__in.
    // Frames load lazily: only the directory names are read at launch. A clip's frames are read when
    // it is queued, from its frames.png (all of them packed in one image), decoded once and cut into
    // frames; only the last few clips stay in memory.
    var clipDirs: [String: URL] = [:]               // "<theme>__<clip>" -> frames directory
    var allowed: [String] = []                      // the clips in the rotation (config selection)
    var transDirs: [String: URL] = [:]              // "<theme>__out" / "<theme>__in" -> frames directory
    var cache: [String: [CGImage]] = [:]            // "c:<clip>" / "t:<transition>" -> frames
    var cacheOrder: [String] = []                   // oldest first: the cache keeps the last `cacheSize`
    let cacheSize = 6
    var queue: [[CGImage]] = []
    var theme = ""
    // Per-launch shuffle bag: forced clips first, then every other clip in random order;
    // no clip repeats until all have played, then a new round starts.
    var remaining: [String] = []
    var lastPlayed = ""
    var visitCount = 0                                 // clips played in the current theme visit
    let maxPerVisit = 2
    var current: [CGImage] = []
    var idx = 0
    var playTimer: Timer?
    var animTimer: Timer?
    let clipH: CGFloat = 64, corner: CGFloat = 12
    // overlap: rises into the notch to cover its rounded bottom corners.
    // fillet: concave flare where the panel meets the notch's bottom edge. 0 = panel is exactly
    // notch-wide (the flare showed up as a protruding ledge on some Macs). Config: "fillet".
    let overlap: CGFloat = 10, fillet: CGFloat = CGFloat(App.cfgNumber("fillet") ?? 0)
    // stretch: fill the real notch width with the art (true) or keep square pixels, centred (false). Config: "stretch".
    let stretch: Bool = (App.config["stretch"] as? Bool) ?? true
    // scale: grow the panel below the notch, keeping the art's proportions and staying centred. Config: "scale".
    let scale: CGFloat = max(1, CGFloat(App.cfgNumber("scale") ?? 1))
    var bodyW: CGFloat { notchW * scale }   // panel body (the art area); the notch-wide stem rises into the notch
    var bodyH: CGFloat { clipH * scale }

    // ~/.config/notch-fight/config.json, read once. Keys: "first", "fillet", "stretch", "scale", "widthTweak",
    // "newClips"/"enabled"/"disabled" (which clips play; see activeClips). NOTCH_FIGHT_CONFIG overrides the
    // path (tests/dev: only seen when the binary is run directly, `open` does not pass the environment).
    static let config: [String: Any] = {
        let env = ProcessInfo.processInfo.environment["NOTCH_FIGHT_CONFIG"] ?? ""
        let url = env.isEmpty ? FileManager.default.homeDirectoryForCurrentUser.appendingPathComponent(".config/notch-fight/config.json")
                              : URL(fileURLWithPath: env)
        guard let data = try? Data(contentsOf: url),
              let json = try? JSONSerialization.jsonObject(with: data) as? [String: Any] else { return [:] }
        return json
    }()
    static func cfgNumber(_ key: String) -> Double? { (config[key] as? NSNumber)?.doubleValue }
    let shape = CAShapeLayer()
    var root: CALayer!
    var notchW: CGFloat = 185, notchH: CGFloat = 32, notchMidX: CGFloat = 0, screen: NSScreen!

    // Per-model width correction (pt): the auxiliary areas can report a notch slightly wider than the
    // real one. Keyed by `hw.model`; add an entry when a Mac's panel visibly overhangs the notch.
    static let notchWidthTweak: [String: CGFloat] = ["Mac14,2": -1]
    static let hwModel: String = {
        var n = 0; sysctlbyname("hw.model", nil, &n, nil, 0)
        var b = [CChar](repeating: 0, count: n); sysctlbyname("hw.model", &b, &n, nil, 0)
        return String(cString: b)
    }()

    func applicationDidFinishLaunching(_ n: Notification) {
        screen = NSScreen.screens.first { $0.auxiliaryTopLeftArea != nil } ?? NSScreen.main!
        let f = screen.frame
        notchMidX = f.midX
        if let l = screen.auxiliaryTopLeftArea, let r = screen.auxiliaryTopRightArea {
            // The notch is not always centred on the screen: anchor to its real edges.
            notchW = r.minX - l.maxX
            notchMidX = (l.maxX + r.minX) / 2
            notchH = screen.safeAreaInsets.top
            notchW += CGFloat(Self.cfgNumber("widthTweak") ?? Double(Self.notchWidthTweak[Self.hwModel] ?? 0))
        }
        if !preview, let why = Self.gateClosed() {
            NSLog("NotchFight: not showing (\(why))"); NSApp.terminate(nil); return
        }
        for name in planSelection() { enqueue(name) }
        if allowed.isEmpty && queue.isEmpty {
            NSLog("NotchFight: no clips active (see ./clips.sh); not showing the panel"); NSApp.terminate(nil); return
        }
        win = NotchPanel(contentRect: rect(height: 0), styleMask: [.borderless, .nonactivatingPanel],
                         backing: .buffered, defer: false)
        win.level = .screenSaver
        win.backgroundColor = .clear
        win.isOpaque = false
        win.hasShadow = false
        win.collectionBehavior = [.canJoinAllSpaces, .stationary, .fullScreenAuxiliary, .ignoresCycle]

        let v = ClickView(frame: NSRect(origin: .zero, size: win.frame.size))
        // Config "click": "close" (default) closes on a click; "next" skips to the next clip, a double click closes.
        let skips = (Self.config["click"] as? String) == "next"
        v.onClick = { [weak self] count in
            guard let self else { return }
            if skips && count < 2 { self.idx = self.current.count } else { self.close() }   // idx past the end: tick picks the next
        }
        v.wantsLayer = true
        root = v.layer!
        root.backgroundColor = NSColor.black.cgColor
        root.mask = shape
        art.frame = CGRect(x: fillet, y: 0, width: bodyW, height: bodyH)
        // Art is authored at a fixed W×H canvas (185×64, MacBookPro18,3's notch width) with effects
        // drawn edge-to-edge. `notchW` varies per Mac (e.g. 209pt on a MacBook Air M2), so `.resizeAspect`
        // would center the unscaled art and leave dead black margins instead of reaching the real notch
        // edges. `.resize` stretches horizontally only — clipH always equals the art's native height, so
        // the vertical scale factor is always 1 and no content is ever cropped.
        // Config "stretch": false keeps the art at its native width, centred (the black margins blend in).
        art.contentsGravity = stretch ? .resize : .resizeAspect
        art.magnificationFilter = .nearest
        art.contentsScale = screen.backingScaleFactor
        art.actions = ["contents": NSNull()]
        root.addSublayer(art)
        v.autoresizingMask = [.width, .height]
        win.contentView = v
        tick()
        updateMask()
        win.orderFrontRegardless()

        playTimer = Timer.scheduledTimer(withTimeInterval: 1.0 / 20.0, repeats: true) { [weak self] _ in self?.tick() }
        watchSessions()
        Timer.scheduledTimer(withTimeInterval: 3, repeats: true) { [weak self] _ in self?.watchSessions() }
        if !preview { Timer.scheduledTimer(withTimeInterval: 5, repeats: true) { [weak self] _ in self?.watchGate() } }
        animate(to: bodyH, duration: 0.55, spring: true)
    }

    func frames(_ key: String, _ dir: URL?) -> [CGImage]? {
        if let c = cache[key] {
            cacheOrder.removeAll { $0 == key }; cacheOrder.append(key)
            return c.isEmpty ? nil : c
        }
        guard let dir else { return nil }
        let f = Self.loadFrames(dir); store(key, f)
        return f.isEmpty ? nil : f
    }

    func store(_ key: String, _ f: [CGImage]) {
        cache[key] = f; cacheOrder.removeAll { $0 == key }; cacheOrder.append(key)
        while cacheOrder.count > cacheSize { cache[cacheOrder.removeFirst()] = nil }   // (playing ones are held by the queue)
    }

    // As soon as a clip starts, pick the next one and decode its frames (and the transition halves, on a
    // change of theme) in the background, so the switch never waits on a PNG.
    var preparing = false
    func prepareNext() {
        guard queue.isEmpty, !preparing, let next = pickNext() else { return }
        let t = themeOf(next)
        var keys: [(String, URL?)] = [("c:" + next, clipDirs[next])]
        if !theme.isEmpty && t != theme { keys += [("t:\(theme)__out", transDirs["\(theme)__out"]), ("t:\(t)__in", transDirs["\(t)__in"])] }
        let todo = keys.filter { cache[$0.0] == nil }
        preparing = true
        DispatchQueue.global(qos: .userInitiated).async {
            let loaded = todo.compactMap { k, dir in dir.map { (k, Self.loadFrames($0)) } }
            DispatchQueue.main.async {
                for (k, f) in loaded { self.store(k, f) }
                self.preparing = false
                self.enqueue(next)                                   // from the cache now
            }
        }
    }

    func rect(height h: CGFloat) -> NSRect {
        let f = screen.frame
        // Hangs from the notch's bottom edge; never overlaps the notch itself.
        return NSRect(x: notchMidX - bodyW / 2 - fillet, y: f.maxY - notchH - h,
                      width: bodyW + 2 * fillet, height: h + overlap)
    }

    // Body = notch width with rounded bottom; top flares concavely into the notch edge.
    // When scaled up, the body is wider than the notch: its top corners round off convexly under the
    // menu bar and only a notch-wide stem rises into the notch.
    func updateMask() {
        let size = win.frame.size, h = size.height - overlap
        let cb = min(corner, h / 2), fr = min(fillet, h / 2)
        let l = fillet, r = fillet + bodyW, w = size.width
        let p = CGMutablePath()
        p.move(to: CGPoint(x: l + cb, y: 0))
        p.addLine(to: CGPoint(x: r - cb, y: 0))
        p.addQuadCurve(to: CGPoint(x: r, y: cb), control: CGPoint(x: r, y: 0))
        if scale > 1 {
            let sl = fillet + (bodyW - notchW) / 2, sr = sl + notchW, ct = min(corner, h / 2, (bodyW - notchW) / 2)
            p.addLine(to: CGPoint(x: r, y: h - ct))
            p.addQuadCurve(to: CGPoint(x: r - ct, y: h), control: CGPoint(x: r, y: h))
            p.addLine(to: CGPoint(x: sr, y: h))
            p.addLine(to: CGPoint(x: sr, y: size.height))
            p.addLine(to: CGPoint(x: sl, y: size.height))
            p.addLine(to: CGPoint(x: sl, y: h))
            p.addLine(to: CGPoint(x: l + ct, y: h))
            p.addQuadCurve(to: CGPoint(x: l, y: h - ct), control: CGPoint(x: l, y: h))
        } else {
            p.addLine(to: CGPoint(x: r, y: h - fr))
            p.addQuadCurve(to: CGPoint(x: r + fr, y: h), control: CGPoint(x: r, y: h))
            p.addLine(to: CGPoint(x: min(w, r + fr), y: h))
            p.addLine(to: CGPoint(x: r, y: h))
            p.addLine(to: CGPoint(x: r, y: size.height))
            p.addLine(to: CGPoint(x: l, y: size.height))
            p.addLine(to: CGPoint(x: l, y: h))
            p.addLine(to: CGPoint(x: l - fr, y: h))
            p.addQuadCurve(to: CGPoint(x: l, y: h - fr), control: CGPoint(x: l, y: h))
        }
        p.addLine(to: CGPoint(x: l, y: cb))
        p.addQuadCurve(to: CGPoint(x: l + cb, y: 0), control: CGPoint(x: l, y: 0))
        p.closeSubpath()
        CATransaction.begin(); CATransaction.setDisableActions(true)
        shape.frame = CGRect(origin: .zero, size: size); shape.path = p
        CATransaction.commit()
    }

    // First clip override, in priority order:
    //   1. open -g NotchFight.app --args --first <theme__clip|theme>[,<...>]
    //   2. NOTCH_FIGHT_FIRST env var (same comma-separated format)
    //   3. ~/.config/notch-fight/config.json  {"first": "<name>"} or {"first": ["<name>", ...]}
    func forcedFirst() -> [String] {
        func split(_ s: String) -> [String] { s.split(separator: ",").map { $0.trimmingCharacters(in: .whitespaces) }.filter { !$0.isEmpty } }
        let args = CommandLine.arguments
        if let i = args.firstIndex(of: "--first"), i + 1 < args.count { return split(args[i + 1]) }
        if let env = ProcessInfo.processInfo.environment["NOTCH_FIGHT_FIRST"], !env.isEmpty { return split(env) }
        let json = Self.config
        if let one = json["first"] as? String { return split(one) }
        return (json["first"] as? [String]) ?? []
    }

    static func subdirs(_ root: URL) -> [String: URL] {
        let names = (try? FileManager.default.contentsOfDirectory(atPath: root.path)) ?? []
        return Dictionary(uniqueKeysWithValues: names.filter { !$0.hasPrefix(".") }.map { ($0, root.appendingPathComponent($0)) })
    }

    // A folder's frames: its frames.png cut into `count` frames (a grid, row by row, as build.py packs
    // it), decoded once into memory so every frame is a cheap crop; an older build's NNN.png otherwise.
    static func loadFrames(_ dir: URL) -> [CGImage] {
        let raw = (try? String(contentsOf: dir.appendingPathComponent("count"), encoding: .utf8)) ?? ""
        if let n = Int(raw.trimmingCharacters(in: .whitespacesAndNewlines)), n > 0,
           let src = CGImageSourceCreateWithURL(dir.appendingPathComponent("frames.png") as CFURL, nil),
           let packed = CGImageSourceCreateImageAtIndex(src, 0, nil) {
            let sheet = decoded(packed) ?? packed
            let cols = min(sheetCols, n), rows = (n + cols - 1) / cols
            let w = sheet.width / cols, h = sheet.height / rows
            return (0..<n).compactMap { i in sheet.cropping(to: CGRect(x: (i % cols) * w, y: (i / cols) * h, width: w, height: h)) }
        }
        let files = ((try? FileManager.default.contentsOfDirectory(atPath: dir.path)) ?? []).filter { $0.hasSuffix(".png") }.sorted()
        return files.compactMap { f -> CGImage? in
            guard let src = CGImageSourceCreateWithURL(dir.appendingPathComponent(f) as CFURL, nil) else { return nil }
            return CGImageSourceCreateImageAtIndex(src, 0, nil)
        }
    }

    static let sheetCols = 10                       // build.py's SHEET_COLS

    /// The image drawn once into a bitmap: its crops then share that memory instead of decoding the PNG again.
    static func decoded(_ img: CGImage) -> CGImage? {
        let space = img.colorSpace ?? CGColorSpace(name: CGColorSpace.sRGB)!
        guard let ctx = CGContext(data: nil, width: img.width, height: img.height, bitsPerComponent: 8, bytesPerRow: 0,
                                  space: space, bitmapInfo: CGImageAlphaInfo.noneSkipLast.rawValue) else { return nil }
        ctx.draw(img, in: CGRect(x: 0, y: 0, width: img.width, height: img.height))
        return ctx.makeImage()
    }

    // `nf preview` (--only): just the forced clips, once, then close; no rotation, no gate, no sessions.
    let preview = CommandLine.arguments.contains("--only")

    // `nf gate` (scripts/nf.py) decides whether the panel may show: paused, quiet hours, screen sharing.
    // Asked at launch and every few seconds while up; the reason when it may not, nil when it may (or
    // when the script is missing: a copied app never hides itself for that).
    static func gateClosed() -> String? {
        let script = Bundle.main.bundleURL.deletingLastPathComponent().deletingLastPathComponent()
            .appendingPathComponent("scripts/nf.py")
        guard FileManager.default.fileExists(atPath: script.path) else { return nil }
        let p = Process(), out = Pipe()
        p.executableURL = URL(fileURLWithPath: "/usr/bin/env"); p.arguments = ["python3", script.path, "gate"]
        p.standardOutput = out; p.standardError = FileHandle.nullDevice
        guard (try? p.run()) != nil else { return nil }
        p.waitUntilExit()
        let why = String(data: out.fileHandleForReading.readDataToEndOfFile(), encoding: .utf8)?.trimmingCharacters(in: .whitespacesAndNewlines) ?? ""
        return p.terminationStatus == 0 ? nil : why
    }
    func watchGate() {
        DispatchQueue.global(qos: .utility).async {
            if let why = Self.gateClosed() { DispatchQueue.main.async { NSLog("NotchFight: hiding (\(why))"); self.close() } }
        }
    }

    // Loads the clip list, works out the rotation (allowed) and resolves the forced clips, which play
    // first, in order, even when not active. Shared by the launch and by --print-selection.
    func planSelection() -> [String] {
        let res = Bundle.main.resourceURL!
        clipDirs = Self.subdirs(res.appendingPathComponent("clips"))
        transDirs = Self.subdirs(res.appendingPathComponent("transitions"))
        allowed = preview ? [] : activeClips()
        remaining = allowed
        var forced: [String] = [], left = Set(remaining)
        for first in forcedFirst() {
            let name = clipDirs[first] != nil ? first
                : (left.filter { themeOf($0) == first }.randomElement() ?? clipDirs.keys.filter { themeOf($0) == first }.randomElement())
            guard let name else {
                NSLog("NotchFight: unknown first clip/theme '\(first)'. Known: \(clipDirs.keys.sorted())"); continue
            }
            forced.append(name); left.remove(name)
        }
        return forced
    }

    // The clips in the rotation. "newClips": "enabled" (default): all except "disabled", so new clips play;
    // "disabled": only "enabled", so new clips are ignored until added. Clips shipped off by default (a
    // .default-off marker from build.py) only play when listed in "enabled". Unknown names are logged.
    func activeClips() -> [String] {
        let cfg = Self.config, all = Array(clipDirs.keys)
        let optIn = (cfg["newClips"] as? String) == "disabled"
        let enabled = Set((cfg["enabled"] as? [String]) ?? []), disabled = Set((cfg["disabled"] as? [String]) ?? [])
        for (key, list) in [("enabled", enabled), ("disabled", optIn ? [] : disabled)] {
            for n in list.sorted() where clipDirs[n] == nil { NSLog("NotchFight: unknown clip '\(n)' in \"\(key)\"") }
        }
        let shippedOff = Set(all.filter { FileManager.default.fileExists(atPath: clipDirs[$0]!.appendingPathComponent(".default-off").path) })
        let active = optIn ? all.filter { enabled.contains($0) }
                           : all.filter { shippedOff.contains($0) ? enabled.contains($0) : !disabled.contains($0) }
        NSLog("NotchFight: \(active.count)/\(all.count) clips active (new clips \(optIn ? "disabled" : "enabled"), \(shippedOff.count) off by default)")
        return active
    }

    func themeOf(_ name: String) -> String { String(name.split(separator: "_", maxSplits: 1).first ?? "") }

    // Stay in the current theme for up to maxPerVisit clips, then move to another theme;
    // always drawing from the clips not yet played this round.
    func pickNext() -> String? {
        if remaining.isEmpty { remaining = allowed }                    // new round
        if remaining.isEmpty { return nil }
        var pool = remaining.filter { $0 != lastPlayed }
        if pool.isEmpty { pool = remaining }
        let same = pool.filter { themeOf($0) == theme }
        let other = pool.filter { themeOf($0) != theme }
        if !same.isEmpty && (visitCount < maxPerVisit || other.isEmpty) { return same.randomElement() }
        return (other.isEmpty ? same : other).randomElement()
    }

    func enqueue(_ name: String) {
        guard let clipFrames = frames("c:" + name, clipDirs[name]) else { return }
        let t = themeOf(name)
        if !theme.isEmpty && t != theme {                             // the iris closes on this theme, opens on the next
            for tk in ["\(theme)__out", "\(t)__in"] { if let tr = frames("t:" + tk, transDirs[tk]) { queue.append(tr) } }
        }
        visitCount = (t == theme) ? visitCount + 1 : 1
        theme = t; lastPlayed = name
        remaining.removeAll { $0 == name }
        queue.append(clipFrames)
    }

    func tick() {
        if idx >= current.count {
            if preparing && queue.isEmpty { return }                  // the next one is nearly ready: hold this frame
            if queue.isEmpty, let next = pickNext() { enqueue(next) }
            guard !queue.isEmpty else { close(); return }             // only forced clips, and they are done
            current = queue.removeFirst(); idx = 0
            prepareNext()
        }
        art.contents = current[idx]
        idx += 1
    }

    // Manual 60 fps frame animation: window frames don't take spring timing reliably.
    func animate(to target: CGFloat, duration: Double, spring: Bool, done: (() -> Void)? = nil) {
        animTimer?.invalidate()
        let start = win.frame.height - overlap, t0 = CACurrentMediaTime()
        animTimer = Timer.scheduledTimer(withTimeInterval: 1.0 / 60.0, repeats: true) { [weak self] t in
            guard let self else { return }
            let p = min(1, (CACurrentMediaTime() - t0) / duration)
            let e = spring ? 1 - exp(-6 * p) * cos(9 * p) : p * p * (3 - 2 * p)
            self.win.setFrame(self.rect(height: max(0, start + (target - start) * CGFloat(p >= 1 ? 1 : e))), display: true)
            self.updateMask()
            if p >= 1 { t.invalidate(); done?() }
        }
    }

    // Session watchdog: ~/.config/notch-fight/sessions/<id> holds the PID of each working Claude
    // session (written by scripts/notch-hook.sh). Markers of dead PIDs are pruned (a closed terminal
    // never fires Stop); once every session is gone the panel retracts. Launches without any marker
    // (manual `open --args --first ...`) are left alone.
    var sawSession = false
    func watchSessions() {
        if preview { return }
        let fm = FileManager.default
        let dir = fm.homeDirectoryForCurrentUser.appendingPathComponent(".config/notch-fight/sessions")
        let files = (try? fm.contentsOfDirectory(at: dir, includingPropertiesForKeys: [.contentModificationDateKey])) ?? []
        var alive = 0
        for f in files where !f.lastPathComponent.hasPrefix(".") {
            let raw = (try? String(contentsOf: f, encoding: .utf8))?.trimmingCharacters(in: .whitespacesAndNewlines) ?? ""
            if let pid = pid_t(raw) {
                if kill(pid, 0) == 0 || errno == EPERM { alive += 1 } else { try? fm.removeItem(at: f) }
            } else {   // no PID recorded: trust the marker for 2 h, like notch-hook.sh
                let m = (try? f.resourceValues(forKeys: [.contentModificationDateKey]))?.contentModificationDate ?? .distantPast
                if Date().timeIntervalSince(m) < 7200 { alive += 1 } else { try? fm.removeItem(at: f) }
            }
        }
        if alive > 0 { sawSession = true } else if sawSession { close() }
    }

    var closing = false
    func close() {
        if closing { return }; closing = true
        animate(to: 0, duration: 0.3, spring: false) { NSApp.terminate(nil) }
    }
}

final class ClickView: NSView {
    var onClick: ((Int) -> Void)?
    override func mouseDown(with e: NSEvent) { onClick?(e.clickCount) }
    override func acceptsFirstMouse(for e: NSEvent?) -> Bool { true }
}

// --print-selection: print what would play and exit before the app starts (no panel, no focus change).
// Used by the tests; also handy to check a config: ./build/NotchFight.app/Contents/MacOS/NotchFight --print-selection
if CommandLine.arguments.contains("--print-selection") {
    let p = App(), forced = p.planSelection()
    for n in forced { print("forced: \(n)") }
    print("panel: \(p.allowed.isEmpty && forced.isEmpty ? "hidden (no clips active)" : "shown")")
    exit(0)
}

let app = NSApplication.shared
let d = App()
app.delegate = d
app.setActivationPolicy(.accessory)
// SIGTERM (pkill, e.g. from a Claude Code Stop hook) retracts into the notch before quitting.
signal(SIGTERM, SIG_IGN)
let term = DispatchSource.makeSignalSource(signal: SIGTERM, queue: .main)
term.setEventHandler { d.close() }
term.resume()
app.run()
