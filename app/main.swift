import AppKit
import QuartzCore

// Drops a black pixel-art fight from under the MacBook notch while Claude works; click it to retract.
// Resident (the default, config "resident"): the app stays up, hidden, between prompts, and shows itself
// when a Claude session starts working (a marker appears in sessions/, written by notch-hook.sh). Hidden it
// runs no timers and holds no frames. With "resident": false it quits when it retracts, as it used to.
// It only becomes the key window if one of its views needs the keyboard (none does: becomesKeyOnlyIfNeeded),
// so whatever you're typing in keeps the keyboard when it drops in; clicks still reach it.
final class NotchPanel: NSPanel {
    override var canBecomeKey: Bool { true }
    override var canBecomeMain: Bool { false }
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
    var queue: [(name: String?, frames: [CGImage])] = []   // name: a clip (nil: a transition half)
    var theme = ""
    // Shuffle bag: forced clips first, then every other clip in random order; no clip repeats until all
    // have played, then a new round starts. The round outlives the app: state.json keeps what has played.
    var remaining: [String] = []
    lazy var state = State()
    var shownSince = Date()                            // visible time not yet added to the stats
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
    let overlap: CGFloat = 10
    var fillet: CGFloat { CGFloat(cfgNumber("fillet") ?? 0) }
    // stretch: fill the real notch width with the art (true) or keep square pixels, centred (false). Config: "stretch".
    var stretch: Bool { (config["stretch"] as? Bool) ?? true }
    // scale: grow the panel below the notch, keeping the art's proportions and staying centred. Config: "scale".
    var scale: CGFloat { max(1, CGFloat(cfgNumber("scale") ?? 1)) }
    var bodyW: CGFloat { notchW * scale }   // panel body (the art area); the notch-wide stem rises into the notch
    var bodyH: CGFloat { clipH * scale }

    // ~/.config/notch-fight/config.json, read again each time the panel shows. Keys: "first", "fillet",
    // "stretch", "scale", "widthTweak", "click", "delay", "resident", "newClips"/"enabled"/"disabled" (which
    // clips play; see activeClips). NOTCH_FIGHT_CONFIG overrides the path (tests/dev: only seen when the
    // binary is run directly, `open` does not pass the environment).
    var config: [String: Any] = Gate.loadConfig()
    func cfgNumber(_ key: String) -> Double? { (config[key] as? NSNumber)?.doubleValue }
    lazy var resident = !preview && ((config["resident"] as? Bool) ?? true)
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
        win = NotchPanel(contentRect: .zero, styleMask: [.borderless, .nonactivatingPanel], backing: .buffered, defer: true)
        win.level = .screenSaver
        win.backgroundColor = .clear
        win.isOpaque = false
        win.hasShadow = false
        win.collectionBehavior = [.canJoinAllSpaces, .stationary, .fullScreenAuxiliary, .ignoresCycle]
        win.becomesKeyOnlyIfNeeded = true                            // never takes the keyboard from what you're typing in

        let v = ClickView(frame: .zero)
        // Config "click": "close" (default) closes on a click; "next" skips to the next clip, a double click closes.
        v.onClick = { [weak self] count in
            guard let self, self.phase == .shown else { return }
            if (self.config["click"] as? String) == "next" && count < 2 { self.idx = self.current.count }   // past the end: tick picks the next
            else { self.dismiss() }
        }
        v.wantsLayer = true
        root = v.layer!
        root.backgroundColor = NSColor.black.cgColor
        root.mask = shape
        root.addSublayer(content)
        for layer in [art, alertLayer, badgeLayer] {
            layer.magnificationFilter = .nearest
            layer.actions = ["contents": NSNull()]
            content.addSublayer(layer)
        }
        crtMask.backgroundColor = NSColor.white.cgColor
        crtLine.backgroundColor = NSColor.white.cgColor; crtLine.isHidden = true
        for l in [content, crtMask, crtLine] { l.actions = ["bounds": NSNull(), "position": NSNull(), "opacity": NSNull(), "hidden": NSNull()] }
        root.addSublayer(crtLine)
        v.autoresizingMask = [.width, .height]
        win.contentView = v

        if preview {                                                 // tell a resident copy to step aside meanwhile
            try? "\(getpid())".write(to: Self.previewFile, atomically: true, encoding: .utf8)
            pokeOthers(); show(); return
        }
        if !resident {                                               // the old way: launched to show, quits when it retracts
            if case (false, let why) = Gate.check() { NSLog("NotchFight: not showing (\(why))"); NSApp.terminate(nil); return }
            show(); if phase != .shown { NSApp.terminate(nil); return }
            watchSessions()
            return
        }
        // Resident: wake on a change in sessions/ (a prompt starts or ends) and on SIGUSR1 (`nf pause` /
        // `resume`, the Stop hook, a preview starting or ending). No polling while nobody is working.
        let fm = FileManager.default
        try? fm.createDirectory(at: Self.sessionsDir, withIntermediateDirectories: true)
        let fd = open(Self.sessionsDir.path, O_EVTONLY)
        if fd >= 0 {
            dirWatch = DispatchSource.makeFileSystemObjectSource(fileDescriptor: fd, eventMask: [.write, .rename, .delete], queue: .main)
            dirWatch?.setEventHandler { [weak self] in self?.evaluate() }
            dirWatch?.setCancelHandler { Darwin.close(fd) }
            dirWatch?.resume()
        }
        evaluate()
    }

    // Over the clip: the "needs you" alert while a session waits for you (a permission prompt, a question;
    // the marker says "waiting"), and the badge with how many sessions work when more than one does.
    // Both from overlays/ (src/overlays.py), loaded while the panel is out.
    let alertLayer = CALayer(), badgeLayer = CALayer()
    var alertFrames: [CGImage] = [], countFrames: [CGImage] = []
    var alertIdx = 0
    var waitingNow = false, sessionCount = 0
    var waitingSeen: Set<String> = []                   // sessions already counted as waiting (stats)

    func noteSessions(_ live: [Session]) {
        let waiting = Set(live.filter(\.waiting).map(\.name))
        let new = waiting.subtracting(waitingSeen)
        if !new.isEmpty && !preview { for _ in new { state.countWait() }; state.save() }
        waitingSeen = waiting
        if !waiting.isEmpty != waitingNow { alertIdx = 0; trace(waiting.isEmpty ? "alert off" : "alert on") }   // from its first frame
        if live.count != sessionCount { trace("sessions \(live.count)") }
        waitingNow = !waiting.isEmpty; sessionCount = live.count
        badgeLayer.contents = sessionCount >= 2 && !countFrames.isEmpty ? countFrames[min(sessionCount, countFrames.count + 1) - 2] : nil
    }

    enum Phase { case hidden, shown, hiding }
    var phase = Phase.hidden
    var dirWatch: DispatchSourceFileSystemObject?
    var pollTimer: Timer?, delayTimer: Timer?
    var dismissedAt: Date?                              // a click hid it: back on the next prompt, not before
    var launchArgsUsed = false                          // --first from the command line: the first show only

    // Resident: should the panel be out right now? Asked whenever something may have changed. Shows it when a
    // live session started (or prompted again) after the last dismissal, has worked at least "delay"
    // seconds, the gate is open and no preview is playing; hides it otherwise. While anyone is working it
    // also asks every 5 s (the gate's clock-driven rules, dead PIDs, the delay running out).
    func evaluate() {
        guard resident else { return }
        config = Gate.loadConfig()
        let live = liveSessions()
        noteSessions(live)
        pollTimer?.invalidate(); pollTimer = nil; delayTimer?.invalidate(); delayTimer = nil
        if live.isEmpty { dismissedAt = nil; hide("no session working"); return }
        pollTimer = Timer.scheduledTimer(withTimeInterval: 5, repeats: false) { [weak self] _ in self?.evaluate() }
        // a session waiting for you counts even after a click, and skips the delay
        let fresh = live.filter { $0.waiting || dismissedAt == nil || $0.date > dismissedAt! }
        if fresh.isEmpty { hide("dismissed"); return }
        if case (false, let why) = Gate.check() { hide(why); return }
        if previewRunning() { hide("a preview is playing"); return }
        if phase == .shown { return }
        let wait = waitingNow ? 0 : (cfgNumber("delay") ?? 0) - Date().timeIntervalSince(fresh.map(\.date).min()!)
        if wait > 0 {
            delayTimer = Timer.scheduledTimer(withTimeInterval: wait, repeats: false) { [weak self] _ in self?.evaluate() }
            return
        }
        if phase == .hidden { show() }                               // .hiding: evaluated again once hidden
    }

    // A preview (`nf preview`: a second copy with --only) leaves its PID in .preview while it plays and
    // pokes the other copies when it starts and ends.
    static var previewFile: URL { Gate.stateDir.appendingPathComponent(".preview") }
    func previewRunning() -> Bool {
        guard let raw = try? String(contentsOf: Self.previewFile, encoding: .utf8),
              let pid = pid_t(raw.trimmingCharacters(in: .whitespacesAndNewlines)), pid != getpid() else { return false }
        return kill(pid, 0) == 0 || errno == EPERM
    }
    func pokeOthers() {
        for other in NSRunningApplication.runningApplications(withBundleIdentifier: Bundle.main.bundleIdentifier ?? "")
            where other.processIdentifier != getpid() { kill(other.processIdentifier, SIGUSR1) }
    }

    // The panel drops in: config re-read, the notch measured (the screen may have changed), the forced clips
    // and the rotation planned, frames loaded for the first clip.
    func show() {
        config = Gate.loadConfig()
        screen = NSScreen.screens.first { $0.auxiliaryTopLeftArea != nil } ?? NSScreen.main!
        let f = screen.frame
        notchMidX = f.midX
        if let l = screen.auxiliaryTopLeftArea, let r = screen.auxiliaryTopRightArea {
            // The notch is not always centred on the screen: anchor to its real edges.
            notchW = r.minX - l.maxX
            notchMidX = (l.maxX + r.minX) / 2
            notchH = screen.safeAreaInsets.top
            notchW += CGFloat(cfgNumber("widthTweak") ?? Double(Self.notchWidthTweak[Self.hwModel] ?? 0))
        }
        theme = ""; visitCount = 0; idx = 0; current = []; queue = []
        for name in planSelection() { enqueue(name) }
        launchArgsUsed = true
        if allowed.isEmpty && queue.isEmpty {
            NSLog("NotchFight: no clips active (see ./clips.sh); not showing the panel"); return
        }
        content.mask = nil; crtLine.isHidden = true                  // whatever an interrupted CRT effect left
        content.frame = CGRect(x: fillet, y: 0, width: bodyW, height: bodyH)
        art.frame = content.bounds
        // Art is authored at a fixed W×H canvas (185×64, MacBookPro18,3's notch width) with effects
        // drawn edge-to-edge. `notchW` varies per Mac (e.g. 209pt on a MacBook Air M2), so `.resizeAspect`
        // would center the unscaled art and leave dead black margins instead of reaching the real notch
        // edges. `.resize` stretches horizontally only — clipH always equals the art's native height, so
        // the vertical scale factor is always 1 and no content is ever cropped.
        // Config "stretch": false keeps the art at its native width, centred (the black margins blend in).
        art.contentsGravity = stretch ? .resize : .resizeAspect
        art.contentsScale = screen.backingScaleFactor
        for layer in [alertLayer, badgeLayer] {                      // drawn over the clip, the same way
            layer.frame = art.frame; layer.contentsGravity = art.contentsGravity; layer.contentsScale = art.contentsScale
        }
        let res = Bundle.main.resourceURL!.appendingPathComponent("overlays")
        alertFrames = Self.loadFrames(res.appendingPathComponent("wait"), alpha: true)
        countFrames = Self.loadFrames(res.appendingPathComponent("count"), alpha: true)
        if !preview { noteSessions(liveSessions()) }
        glowColors = [:]
        glowStrength = Glow.strength(config["glow"])
        win.setFrame(rect(height: 0), display: false)
        phase = .shown; trace("shown")
        shownSince = Date()
        tick()
        updateMask()
        win.orderFrontRegardless()
        playTimer?.invalidate()
        playTimer = Timer.scheduledTimer(withTimeInterval: 1.0 / 20.0, repeats: true) { [weak self] _ in self?.tick() }
        dropIn { [weak self] in self?.glowIn() }
    }

    // Config "entrance": how the panel comes out and goes back. "spring" (default): it drops and settles
    // with a little wobble; "bounce": it falls and bounces off the bottom; "crt": it drops dark and the
    // picture switches on like an old TV (a bright line that opens up), and off the same way.
    var entrance: String { (config["entrance"] as? String) ?? "spring" }
    let content = CALayer()                             // the clip and its overlays (masked by the CRT effect)
    let crtMask = CALayer(), crtLine = CALayer()

    func dropIn(done: @escaping () -> Void) {
        switch entrance {
        case "bounce": animate(to: bodyH, duration: 0.75, curve: .bounce, done: done)
        case "crt":
            setCRT(open: 0, line: 0)
            animate(to: bodyH, duration: 0.18, curve: .smooth) { [weak self] in
                guard let self else { return }
                self.run(0.38, { p in                               // the line spreads, then the picture opens
                    if p < 0.35 { self.setCRT(open: 0, line: p / 0.35) } else { self.setCRT(open: (p - 0.35) / 0.65, line: 1) }
                }) { self.content.mask = nil; self.crtLine.isHidden = true; done() }
            }
        default: animate(to: bodyH, duration: 0.55, curve: .spring, done: done)
        }
    }

    func goUp(done: @escaping () -> Void) {
        glowOut()
        if entrance == "crt" {
            run(0.3, { [weak self] p in                             // the picture closes to a line, the line to a dot
                guard let self else { return }
                if p < 0.6 { self.setCRT(open: 1 - p / 0.6, line: 1) } else { self.setCRT(open: 0, line: 1 - (p - 0.6) / 0.4) }
            }) { [weak self] in
                self?.crtLine.isHidden = true
                self?.animate(to: 0, duration: 0.18, curve: .smooth, done: done)
            }
        } else { animate(to: 0, duration: 0.3, curve: .smooth, done: done) }
    }

    /// open: 0 (a line) .. 1 (the whole picture); line: how much of the width the bright line covers.
    func setCRT(open: Double, line: Double) {
        let b = content.bounds, mid = b.height / 2
        let h = max(2, b.height * CGFloat(open * open)), w = b.width * CGFloat(line)
        content.mask = crtMask
        crtMask.frame = open > 0 ? CGRect(x: 0, y: mid - h / 2, width: b.width, height: h) : .zero
        crtLine.isHidden = line <= 0
        crtLine.frame = CGRect(x: content.frame.minX + (b.width - w) / 2, y: mid - 1, width: w, height: 2)
        crtLine.opacity = Float(1 - open)
    }

    // The glow around the panel (Glow.swift), when the config asks for it.
    var glow: Glow?
    var glowStrength: Double?
    var glowColors: [String: [SIMD3<Double>]] = [:]     // clip -> one colour per frame
    var currentName: String?
    func glowIn() {
        guard phase == .shown, let strength = glowStrength else { return }
        let g = glow ?? Glow(); glow = g; g.strength = strength
        let f = screen.frame                                        // the panel, from the screen's top edge down
        g.place(below: win, around: NSRect(x: notchMidX - bodyW / 2, y: f.maxY - notchH - bodyH, width: bodyW, height: notchH + bodyH),
                corner: min(corner, bodyH / 2))
        if let n = currentName, let c = glowColors[n], idx > 0, idx - 1 < c.count { g.color = c[idx - 1] }
        g.step(toward: nil)
        g.win.orderFrontRegardless(); g.win.order(.below, relativeTo: win.windowNumber)
        g.fade(to: 1, duration: 0.4)
    }
    func glowOut() {
        guard let g = glow, g.win.isVisible else { return }
        g.fade(to: 0, duration: 0.15) { g.win.orderOut(nil) }
    }

    // The panel retracts into the notch. Resident: it then lets go of every frame and waits, hidden;
    // otherwise the app quits.
    func hide(_ why: String) {
        guard phase == .shown else { return }
        NSLog("NotchFight: hiding (\(why))")
        phase = .hiding
        saveState()
        goUp { [weak self] in
            guard let self else { return }
            if !self.resident { NSApp.terminate(nil); return }
            self.playTimer?.invalidate(); self.playTimer = nil
            self.win.orderOut(nil)
            self.art.contents = nil; self.alertLayer.contents = nil; self.badgeLayer.contents = nil
            self.current = []; self.queue = []; self.cache = [:]; self.cacheOrder = []
            self.alertFrames = []; self.countFrames = []; self.glowColors = [:]
            self.phase = .hidden; self.trace("hidden")
            self.evaluate()                                          // a prompt may have come in meanwhile
        }
    }

    // NOTCH_FIGHT_TRACE=<file>: one line per change: "shown" / "hidden", "alert on" / "alert off",
    // "sessions <n>" (tests/test_resident.py).
    let tracePath = ProcessInfo.processInfo.environment["NOTCH_FIGHT_TRACE"]
    func trace(_ what: String) {
        guard let tracePath, let h = FileHandle(forWritingAtPath: tracePath) ?? {
            FileManager.default.createFile(atPath: tracePath, contents: nil); return FileHandle(forWritingAtPath: tracePath) }() else { return }
        h.seekToEndOfFile(); h.write((what + "\n").data(using: .utf8)!); try? h.close()
    }

    // A click: back into the notch until the next prompt.
    func dismiss() {
        if resident { dismissedAt = Date(); evaluate() } else { close() }
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
        if !theme.isEmpty && t != theme {
            nextStyle = pickStyle()
            keys += transKeys(from: theme, to: t, style: nextStyle!).map { ("t:" + $0, transDirs[$0]) }
        }
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
        let args = CommandLine.arguments                             // (the command line: the first show only)
        if !launchArgsUsed, let i = args.firstIndex(of: "--first"), i + 1 < args.count { return split(args[i + 1]) }
        if !launchArgsUsed, let env = ProcessInfo.processInfo.environment["NOTCH_FIGHT_FIRST"], !env.isEmpty { return split(env) }
        let json = config
        if let one = json["first"] as? String { return split(one) }
        return (json["first"] as? [String]) ?? []
    }

    static func subdirs(_ root: URL) -> [String: URL] {
        let names = (try? FileManager.default.contentsOfDirectory(atPath: root.path)) ?? []
        return Dictionary(uniqueKeysWithValues: names.filter { !$0.hasPrefix(".") }.map { ($0, root.appendingPathComponent($0)) })
    }

    // A folder's frames: its frames.png cut into `count` frames (a grid, row by row, as build.py packs
    // it), decoded once into memory so every frame is a cheap crop; an older build's NNN.png otherwise.
    static func loadFrames(_ dir: URL, alpha: Bool = false) -> [CGImage] {
        let raw = (try? String(contentsOf: dir.appendingPathComponent("count"), encoding: .utf8)) ?? ""
        if let n = Int(raw.trimmingCharacters(in: .whitespacesAndNewlines)), n > 0,
           let src = CGImageSourceCreateWithURL(dir.appendingPathComponent("frames.png") as CFURL, nil),
           let packed = CGImageSourceCreateImageAtIndex(src, 0, nil) {
            let sheet = decoded(packed, alpha: alpha) ?? packed
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
    static func decoded(_ img: CGImage, alpha: Bool = false) -> CGImage? {
        let space = img.colorSpace ?? CGColorSpace(name: CGColorSpace.sRGB)!
        guard let ctx = CGContext(data: nil, width: img.width, height: img.height, bitsPerComponent: 8, bytesPerRow: 0,
                                  space: space, bitmapInfo: (alpha ? CGImageAlphaInfo.premultipliedLast : .noneSkipLast).rawValue) else { return nil }
        ctx.draw(img, in: CGRect(x: 0, y: 0, width: img.width, height: img.height))
        return ctx.makeImage()
    }

    // `nf preview` (--only): just the forced clips, once, then close; no rotation, no gate, no sessions.
    let preview = CommandLine.arguments.contains("--only")

    // Gate.check() (Gate.swift) decides whether the panel may show: paused, quiet hours, screen sharing.
    // In-process, so asking costs next to nothing.

    // Loads the clip list, works out the rotation (allowed) and resolves the forced clips, which play
    // first, in order, even when not active. Shared by the launch and by --print-selection.
    func planSelection() -> [String] {
        let res = Bundle.main.resourceURL!
        clipDirs = Self.subdirs(res.appendingPathComponent("clips"))
        transDirs = Self.subdirs(res.appendingPathComponent("transitions"))
        allowed = preview ? [] : activeClips()
        remaining = allowed
        if !preview {                                                // carry on with the last launch's round
            let done = Set(state.played), left = allowed.filter { !done.contains($0) }
            if left.isEmpty { state.played = [] } else { remaining = left }
            lastPlayed = state.lastClip
        }
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
        let cfg = config, all = Array(clipDirs.keys)
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
        if remaining.isEmpty { remaining = allowed; state.played = [] }  // new round
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
        if !theme.isEmpty && t != theme {                             // this theme closes, the next one opens
            for tk in transKeys(from: theme, to: t, style: nextStyle ?? pickStyle()) {
                if let tr = frames("t:" + tk, transDirs[tk]) { queue.append((nil, tr)) }
            }
        }
        nextStyle = nil
        picked(name)
        queue.append((name, clipFrames))
    }

    // Transitions (src/transitions.py): each theme has halves in several styles, <theme>__out / __in for its
    // first (the iris, or the theme's own) and <theme>__out__<style> for the rest. Config "transitions":
    // "mix" (default) picks one at random on each change; a style's name always uses that one. A theme
    // without that style plays its first.
    var nextStyle: String?                              // the style prepareNext loaded for the coming change
    func pickStyle() -> String {
        let want = (config["transitions"] as? String) ?? "mix"
        if want != "mix" { return want }
        return ([""] + otherStyles()).randomElement()!                 // "": the first style
    }
    func otherStyles() -> [String] {
        Set(transDirs.keys.compactMap { k in k.range(of: "__out__").map { String(k[$0.upperBound...]) } }).sorted()
    }
    func transKeys(from: String, to: String, style: String) -> [String] {
        ["\(from)__out", "\(to)__in"].map { base in
            let k = style.isEmpty ? base : "\(base)__\(style)"
            return transDirs[k] != nil ? k : base
        }
    }

    // The rotation's bookkeeping once a clip is chosen (it is queued, not yet playing).
    func picked(_ name: String) {
        let t = themeOf(name)
        visitCount = (t == theme) ? visitCount + 1 : 1
        theme = t; lastPlayed = name
        remaining.removeAll { $0 == name }
    }

    // A clip starts playing: it counts as played this round, in state.json too (a queued clip that never
    // played, because the panel closed first, stays in the round for the next launch).
    func started(_ name: String) {
        if preview { return }
        if !state.played.contains(name) { state.played.append(name) }
        state.lastClip = name
        state.countPlay(name)
        saveState()
    }

    func saveState() {
        if preview { return }
        let secs = Int(Date().timeIntervalSince(shownSince))         // whole seconds; the rest waits for the next save
        state.addShown(secs); shownSince += Double(secs)
        state.save()
    }

    func tick() {
        if idx >= current.count {
            if preparing && queue.isEmpty { return }                  // the next one is nearly ready: hold this frame
            if queue.isEmpty, let next = pickNext() { enqueue(next) }
            guard !queue.isEmpty else { close(); return }             // a preview's clips are done
            let item = queue.removeFirst(); current = item.frames; idx = 0; currentName = item.name
            if let name = item.name {
                started(name)
                if glowStrength != nil, glowColors[name] == nil, let dir = clipDirs[name] { glowColors[name] = Glow.load(dir) }
            }
            prepareNext()
        }
        art.contents = current[idx]
        idx += 1
        alertLayer.contents = waitingNow && !alertFrames.isEmpty ? alertFrames[alertIdx % alertFrames.count] : nil
        alertIdx += 1
        if let g = glow, g.win.isVisible {                          // transitions: no colours, it keeps the last
            let c = currentName.flatMap { glowColors[$0] }
            g.step(toward: c.flatMap { idx - 1 < $0.count ? $0[idx - 1] : nil })
        }
    }

    // Manual 60 fps animation (window frames don't take spring timing reliably): step(p), p from 0 to 1.
    func run(_ duration: Double, _ step: @escaping (Double) -> Void, done: (() -> Void)? = nil) {
        animTimer?.invalidate()
        let t0 = CACurrentMediaTime()
        animTimer = Timer.scheduledTimer(withTimeInterval: 1.0 / 60.0, repeats: true) { t in
            let p = min(1, (CACurrentMediaTime() - t0) / duration)
            CATransaction.begin(); CATransaction.setDisableActions(true); step(p); CATransaction.commit()
            if p >= 1 { t.invalidate(); done?() }
        }
    }

    enum Curve { case spring, smooth, bounce }
    static func ease(_ c: Curve, _ p: Double) -> Double {
        if p >= 1 { return 1 }
        switch c {
        case .spring: return 1 - exp(-6 * p) * cos(9 * p)
        case .smooth: return p * p * (3 - 2 * p)
        case .bounce:                                               // falls, then smaller and smaller bounces
            let n = 7.5625, d = 2.75
            if p < 1 / d { return n * p * p }
            if p < 2 / d { let q = p - 1.5 / d; return n * q * q + 0.75 }
            if p < 2.5 / d { let q = p - 2.25 / d; return n * q * q + 0.9375 }
            let q = p - 2.625 / d; return n * q * q + 0.984375
        }
    }

    // The panel's height, animated.
    func animate(to target: CGFloat, duration: Double, curve: Curve, done: (() -> Void)? = nil) {
        let start = win.frame.height - overlap
        run(duration, { [weak self] p in
            guard let self else { return }
            self.win.setFrame(self.rect(height: max(0, start + (target - start) * CGFloat(Self.ease(curve, p)))), display: true)
            self.updateMask()
        }, done: done)
    }

    // ~/.config/notch-fight/sessions/<id> holds the PID of each working Claude session (written by
    // scripts/notch-hook.sh on each prompt, so its date is when that prompt started). Markers of dead PIDs
    // are pruned (a closed terminal never fires Stop). Returns the live markers' dates.
    static var sessionsDir: URL { Gate.stateDir.appendingPathComponent("sessions") }   // (moves with NOTCH_FIGHT_CONFIG: tests)
    // A marker reads "<pid>" or "<pid> waiting" (the hook's `wait`: a permission prompt is up).
    struct Session { let name: String; let date: Date; let waiting: Bool }
    func liveSessions() -> [Session] {
        let fm = FileManager.default
        let files = (try? fm.contentsOfDirectory(at: Self.sessionsDir, includingPropertiesForKeys: [.contentModificationDateKey])) ?? []
        var live: [Session] = []
        for f in files where !f.lastPathComponent.hasPrefix(".") {
            let words = ((try? String(contentsOf: f, encoding: .utf8)) ?? "").split(whereSeparator: \.isWhitespace)
            let m = (try? f.resourceValues(forKeys: [.contentModificationDateKey]))?.contentModificationDate ?? .distantPast
            let s = Session(name: f.lastPathComponent, date: m, waiting: words.dropFirst().contains("waiting"))
            if let pid = words.first.flatMap({ pid_t($0) }) {
                if kill(pid, 0) == 0 || errno == EPERM { live.append(s) } else { try? fm.removeItem(at: f) }
            } else {   // no PID recorded: trust the marker for 2 h, like notch-hook.sh
                if Date().timeIntervalSince(m) < 7200 { live.append(s) } else { try? fm.removeItem(at: f) }
            }
        }
        return live
    }

    // Not resident: every 3 s, retract and quit once every session is gone. Launches without any marker
    // (manual `open --args --first ...`) are left alone; the gate is asked too.
    var sawSession = false
    func watchSessions() {
        Timer.scheduledTimer(withTimeInterval: 3, repeats: true) { [weak self] _ in self?.recheck() }
    }
    func recheck() {
        if preview { return }
        if resident { evaluate(); return }
        if case (false, let why) = Gate.check() { NSLog("NotchFight: hiding (\(why))"); close(); return }
        let live = liveSessions(); noteSessions(live)
        if !live.isEmpty { sawSession = true } else if sawSession { close() }
    }
    // SIGUSR1 (the Stop hook, `nf pause`): look again now. Not resident, with nobody working: retract and quit.
    func poke() {
        if preview { return }
        if resident { evaluate(); return }
        if case (false, let why) = Gate.check() { NSLog("NotchFight: hiding (\(why))"); close(); return }
        if liveSessions().isEmpty { close() }
    }

    // Retract and quit (SIGTERM, a preview that is over, the old non-resident way).
    var closing = false
    func close() {
        if closing { return }; closing = true
        saveState()
        if preview { try? FileManager.default.removeItem(at: Self.previewFile); pokeOthers() }
        if phase != .shown { NSApp.terminate(nil); return }
        phase = .hiding
        goUp { NSApp.terminate(nil) }
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
    print("transition styles: \((["first"] + p.otherStyles()).joined(separator: ", "))")
    print("panel: \(p.allowed.isEmpty && forced.isEmpty ? "hidden (no clips active)" : "shown")")
    exit(0)
}

// --print-rotation N: play N clips without showing anything (the rotation and state.json as for real,
// no frames loaded) and print them, one "played: <clip>" per line. For tests of the round across launches.
if let i = CommandLine.arguments.firstIndex(of: "--print-rotation"), i + 1 < CommandLine.arguments.count,
   let n = Int(CommandLine.arguments[i + 1]) {
    let p = App(), forced = p.planSelection()
    // As in the app: each clip starts before the next is picked (prepareNext runs once one starts).
    var order = Array(forced.prefix(n))
    for name in order { p.picked(name); p.started(name) }
    while order.count < n, let next = p.pickNext() { p.picked(next); p.started(next); order.append(next) }
    for name in order { print("played: \(name)") }
    exit(0)
}

// --gate: Gate.check() as `nf gate` prints it (exit 0: may show, 1: may not). NOTCH_FIGHT_NOW (epoch
// seconds) fixes "now", for tests/test_app_gate.py.
if CommandLine.arguments.contains("--gate") {
    let now = Double(ProcessInfo.processInfo.environment["NOTCH_FIGHT_NOW"] ?? "").map { Date(timeIntervalSince1970: $0) } ?? Date()
    let (ok, why) = Gate.check(now: now)
    print(why); exit(ok ? 0 : 1)
}

let app = NSApplication.shared
let d = App()
app.delegate = d
app.setActivationPolicy(.accessory)
// SIGTERM (pkill, `nf resident off`, build.sh) retracts into the notch before quitting. SIGUSR1 (the Stop
// hook, `nf pause` / `resume`): look at the sessions and the gate again now.
signal(SIGTERM, SIG_IGN); signal(SIGUSR1, SIG_IGN)
let term = DispatchSource.makeSignalSource(signal: SIGTERM, queue: .main)
term.setEventHandler { d.close() }
term.resume()
let usr1 = DispatchSource.makeSignalSource(signal: SIGUSR1, queue: .main)
usr1.setEventHandler { d.poke() }
usr1.resume()
app.run()
