import Foundation

// What the app remembers between launches, in state.json next to config.json (written atomically):
//   "rotation": {"played": [...], "lastClip": "..."}   the clips already played this round, so a new launch
//                                                     carries on with the round instead of starting another;
//   "stats":    {"plays": {clip: n}, "shown": {"YYYY-MM-DD": seconds}, "waits": {"YYYY-MM-DD": n}}
//               for the menu's stats, later.
// Keys it does not know are kept as they are.
final class State {
    let url: URL
    var json: [String: Any]

    init(url: URL = Gate.stateDir.appendingPathComponent("state.json")) {
        self.url = url
        json = (try? Data(contentsOf: url)).flatMap { try? JSONSerialization.jsonObject(with: $0) as? [String: Any] } ?? [:]
    }

    private var rotation: [String: Any] {
        get { json["rotation"] as? [String: Any] ?? [:] }
        set { json["rotation"] = newValue }
    }
    private var stats: [String: Any] {
        get { json["stats"] as? [String: Any] ?? [:] }
        set { json["stats"] = newValue }
    }

    var played: [String] {
        get { rotation["played"] as? [String] ?? [] }
        set { rotation["played"] = newValue }
    }
    var lastClip: String {
        get { rotation["lastClip"] as? String ?? "" }
        set { rotation["lastClip"] = newValue }
    }

    func countPlay(_ clip: String) {
        var plays = stats["plays"] as? [String: Int] ?? [:]
        plays[clip, default: 0] += 1
        stats["plays"] = plays
    }

    func addShown(_ seconds: Int, on day: Date = Date()) {
        guard seconds > 0 else { return }
        let f = DateFormatter(); f.dateFormat = "yyyy-MM-dd"
        var shown = stats["shown"] as? [String: Int] ?? [:]
        shown[f.string(from: day), default: 0] += seconds
        stats["shown"] = shown
    }

    // Times a session stopped to wait for you (a permission prompt, a question), per day.
    func countWait(on day: Date = Date()) {
        let f = DateFormatter(); f.dateFormat = "yyyy-MM-dd"
        var waits = stats["waits"] as? [String: Int] ?? [:]
        waits[f.string(from: day), default: 0] += 1
        stats["waits"] = waits
    }

    func save() {
        guard let data = try? JSONSerialization.data(withJSONObject: json, options: [.prettyPrinted, .sortedKeys]) else { return }
        try? FileManager.default.createDirectory(at: url.deletingLastPathComponent(), withIntermediateDirectories: true)
        try? data.write(to: url, options: .atomic)
    }
}
