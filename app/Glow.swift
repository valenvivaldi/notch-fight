import AppKit
import QuartzCore

// The light a clip spills around the panel (config "glow": "soft" / "strong"; off by default): a halo that
// hugs the panel's shape, out to its sides and below it, a short way, in the colour of the frame on
// screen (build.py writes one colour per frame, clips/<clip>/glow), eased from frame to frame. It is the
// shadow of a panel-shaped path, in a window of its own under the panel that takes no clicks. It fades in
// once the panel is down and out before it goes up.
final class Glow {
    let win: NSPanel
    let halo = CALayer()
    var color = SIMD3<Double>(0, 0, 0)
    var strength: Double = 0.55
    static let reach: CGFloat = 16                                  // pt the light spreads beyond the panel

    init() {
        win = NSPanel(contentRect: .zero, styleMask: [.borderless, .nonactivatingPanel], backing: .buffered, defer: true)
        win.level = .screenSaver
        win.backgroundColor = .clear
        win.isOpaque = false
        win.hasShadow = false
        win.ignoresMouseEvents = true
        win.collectionBehavior = [.canJoinAllSpaces, .stationary, .fullScreenAuxiliary, .ignoresCycle]
        let v = NSView(); v.wantsLayer = true; v.layer!.addSublayer(halo); win.contentView = v
        halo.shadowOffset = .zero
        halo.shadowOpacity = 0
        halo.actions = ["shadowColor": NSNull(), "shadowPath": NSNull(), "bounds": NSNull(), "position": NSNull()]
    }

    /// Strength for a config value: "soft" (or true), "strong"; nil when off.
    static func strength(_ cfg: Any?) -> Double? {
        switch cfg {
        case let s as String where s == "strong": return 0.95
        case let s as String where s == "soft": return 0.55
        case let b as Bool where b: return 0.55
        default: return nil
        }
    }

    /// Lays it under `panel` around `body` (screen coordinates: the panel's area, from the top of the
    /// screen down to its rounded bottom), `corner` the bottom corners' radius.
    func place(below panel: NSWindow, around body: NSRect, corner: CGFloat) {
        let m = Self.reach * 2.5                                    // room for the blur to fade out
        win.setFrame(NSRect(x: body.minX - m, y: body.minY - m, width: body.width + 2 * m, height: body.height + m), display: false)
        halo.frame = CGRect(x: 0, y: 0, width: body.width + 2 * m, height: body.height + m)
        let shape = CGMutablePath()                                 // rounded at the bottom, square at the top edge
        let r = CGRect(x: m, y: m, width: body.width, height: body.height + corner)
        shape.addRoundedRect(in: r, cornerWidth: corner, cornerHeight: corner)
        halo.shadowPath = shape
        halo.shadowRadius = Self.reach
        win.order(.below, relativeTo: panel.windowNumber)
    }

    func fade(to opacity: Float, duration: Double, done: (() -> Void)? = nil) {
        let target = opacity * Float(strength)
        CATransaction.begin()
        CATransaction.setCompletionBlock(done)
        let a = CABasicAnimation(keyPath: "shadowOpacity")
        a.fromValue = halo.presentation()?.shadowOpacity ?? halo.shadowOpacity; a.toValue = target; a.duration = duration
        halo.add(a, forKey: "fade"); halo.shadowOpacity = target
        CATransaction.commit()
    }

    /// One step towards this frame's colour; called every frame while the panel is out.
    func step(toward c: SIMD3<Double>?) {
        if let c { color += (c - color) * 0.15 }
        CATransaction.begin(); CATransaction.setDisableActions(true)
        halo.shadowColor = NSColor(srgbRed: color.x, green: color.y, blue: color.z, alpha: 1).cgColor
        CATransaction.commit()
    }

    static func load(_ dir: URL) -> [SIMD3<Double>] {
        let raw = (try? String(contentsOf: dir.appendingPathComponent("glow"), encoding: .utf8)) ?? ""
        return raw.split(separator: "\n").compactMap { line in
            guard line.count == 6, let v = UInt32(line, radix: 16) else { return nil }
            return SIMD3(Double(v >> 16 & 255), Double(v >> 8 & 255), Double(v & 255)) / 255
        }
    }
}
