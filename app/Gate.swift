import Foundation
import Darwin

// Whether the panel may show right now: paused, quiet hours, screen sharing. The same rules as `gate()` in
// scripts/nf.py, which the command line and the Claude Code hook still use; tests/test_app_gate.py keeps the
// two in step. Compiled into the app and the menu, so neither runs Python to ask (they did, every few
// seconds). Reads config.json and paused fresh on every call: `nf quiet` or `nf pause` apply at once.
enum Gate {
    // ~/.config/notch-fight/config.json; NOTCH_FIGHT_CONFIG moves it, and the files next to it (tests/dev).
    static let configURL: URL = {
        let env = ProcessInfo.processInfo.environment["NOTCH_FIGHT_CONFIG"] ?? ""
        return env.isEmpty ? FileManager.default.homeDirectoryForCurrentUser.appendingPathComponent(".config/notch-fight/config.json")
                           : URL(fileURLWithPath: env)
    }()
    static var stateDir: URL { configURL.deletingLastPathComponent() }
    static var pausedURL: URL { stateDir.appendingPathComponent("paused") }

    // Zoom starts CptHost to share; screencaptureui is macOS's own capture (Cmd-Shift-5). nf.py's SHARE_PROCESSES.
    static let shareProcesses = ["CptHost", "screencaptureui"]

    static func loadConfig() -> [String: Any] {
        guard let data = try? Data(contentsOf: configURL),
              let json = try? JSONSerialization.jsonObject(with: data) as? [String: Any] else { return [:] }
        return json
    }

    /// (may show, why). `now` is for tests: NOTCH_FIGHT_NOW (epoch seconds) when run with --gate.
    static func check(now: Date = Date()) -> (Bool, String) {
        let cfg = loadConfig()
        if let until = pausedUntil(now) {
            return (false, until == .infinity ? "paused until resumed" : "paused until \(hhmm(Date(timeIntervalSince1970: until)))")
        }
        if let q = cfg["quiet"] as? [String: Any], inQuiet(q, now) {
            let f = q["from"] as? String ?? "", t = q["to"] as? String ?? ""
            return (false, "quiet hours (\(f)-\(t)\((q["days"] as? String) == "weekdays" ? ", weekdays" : ""))")
        }
        if (cfg["pauseOnShare"] as? Bool) ?? true, let who = sharing(cfg) { return (false, "screen sharing (\(who))") }
        return (true, "showing")
    }

    /// nil: not paused; .infinity: until resumed; else the epoch it ends. An expired pause file is removed.
    static func pausedUntil(_ now: Date) -> Double? {
        guard let data = try? Data(contentsOf: pausedURL),
              let json = try? JSONSerialization.jsonObject(with: data) as? [String: Any] else { return nil }
        guard let until = (json["until"] as? NSNumber)?.doubleValue else { return .infinity }
        if until <= now.timeIntervalSince1970 { try? FileManager.default.removeItem(at: pausedURL); return nil }
        return until
    }

    /// Inside the quiet window {"from","to","days"}? Wraps past midnight; with "weekdays" the window belongs
    /// to the day it starts on (Friday night yes, Saturday night no).
    static func inQuiet(_ q: [String: Any], _ now: Date) -> Bool {
        func mins(_ s: Any?) -> Int? {
            let p = ((s as? String) ?? "").split(separator: ":").compactMap { Int($0) }
            return p.count == 2 ? p[0] * 60 + p[1] : nil
        }
        guard let start = mins(q["from"]), let end = mins(q["to"]), start != end else { return false }
        let cal = Calendar.current, c = cal.dateComponents([.hour, .minute, .weekday], from: now)
        let m = c.hour! * 60 + c.minute!
        let weekdays = (q["days"] as? String) == "weekdays"
        func workday(_ d: Date) -> Bool { let w = cal.component(.weekday, from: d); return w != 1 && w != 7 }   // 1 = Sunday
        if start < end { return start <= m && m < end && (!weekdays || workday(now)) }
        if m >= start { return !weekdays || workday(now) }                                               // tonight
        if m < end { return !weekdays || workday(cal.date(byAdding: .day, value: -1, to: now)!) }        // since last night
        return false
    }

    /// A running screen-sharing / recording process from the list ("shareProcesses" in config.json), or nil.
    static func sharing(_ cfg: [String: Any]) -> String? {
        let wanted = (cfg["shareProcesses"] as? [String]) ?? shareProcesses
        if wanted.isEmpty { return nil }
        let running = processNames()
        return wanted.first { running.contains($0) }
    }

    /// The names of all running processes (what `pgrep -x` matches), without spawning anything.
    static func processNames() -> Set<String> {
        var pids = [pid_t](repeating: 0, count: Int(proc_listallpids(nil, 0)) + 64)
        let n = Int(proc_listallpids(&pids, Int32(pids.count * MemoryLayout<pid_t>.size)))
        var names = Set<String>(), buf = [CChar](repeating: 0, count: 256)
        for pid in pids.prefix(max(0, n)) where pid > 0 {
            if proc_name(pid, &buf, UInt32(buf.count)) > 0 { names.insert(String(cString: buf)) }
        }
        return names
    }

    static func hhmm(_ d: Date) -> String {
        let f = DateFormatter(); f.dateFormat = "HH:mm"; return f.string(from: d)
    }
}
