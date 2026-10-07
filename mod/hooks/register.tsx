// Notch Fight inside Claude Code: while a turn runs, the band above the prompt plays the clips the
// notch app plays (same build/clips, same config.json selection, theme-to-theme transitions).
// display "image" shows the real PNG frames (kitty graphics protocol: kitty, Ghostty) and falls back
// to "raster" where the terminal draws the Image's alt; "raster" packs each frame into coloured
// quadrant-block cells, 2x2 pixels each (scripts/mod_cells.py), which every terminal shows;
// "sextant" packs sextant cells, 2x3 pixels each: 50% more rows, for terminals whose renderer or
// font draws U+1FB00..1FB3B (kitty, Ghostty, WezTerm, xterm.js's WebGL renderer: VS Code, Orca).
// "octant" packs octant cells, 2x4 pixels each (Unicode 16, U+1CD00..1CDE5): twice raster's rows,
// where the terminal draws them (kitty, Ghostty, WezTerm; xterm.js not yet: boxes in Orca, VS Code).
// A Raster only takes BMP characters, so sextant and octant frames are drawn as coloured Text runs,
// one row each, redrawn by bumping the `tick` atom.
// The clip sits at the right end of the band.
import { atom, read, update } from 'claude-code'
import type { EngineInterface, Register } from 'claude-code'

import type { Mode } from '../types'

const isPlaying = atom({ plugin: 'notch-fight', key: 'isPlaying' } as const, false)
const mode = atom({ plugin: 'notch-fight', key: 'mode' } as const, 'image' as Mode)
const tickNo = atom({ plugin: 'notch-fight', key: 'tick' } as const, 0)

const FPS = 20
const MAX_PER_VISIT = 2                   // clips in one theme before moving on, like the app
const KEY = 'clip'

type Item = { name: string; dir: string; count: number }
type Run = { text: string; fg: string; bg: string }
type Config = { newClips?: string; enabled?: string[]; disabled?: string[]; first?: string | string[] }

const themeOf = (name: string) => name.split('_')[0]
const pad = (n: number) => String(n).padStart(3, '0')

// ---- playback state (module variables: a reload starts over) ----
let rows = 10
let columns = 58
let repo = ''
let root = ''
let site: string | undefined                            // the band's requestId, once it drew us
let allowed: string[] = []
let remaining: string[] = []
let forced: string[] = []
let theme = ''
let last = ''
let visits = 0
let queue: Item[] = []
let item: Item | null = null
let frame = 0
let png = ''                                            // the frame on screen, image mode
let cells = ''                                          // the frame on screen, cell modes
let packDir = ''                                        // the current item's cell frames: chunks of PER frames
let packed: Uint8Array | null = null                    // the chunk in memory
let chunk = -1
let runs: Run[][] = []                                  // the frame on screen, sextant mode: one list a row
let timer: { cancel(): void } | null = null
let isBusy = false
let hasWarned = false

async function load($: EngineInterface) {
  const home = (await $.env.get('HOME')) ?? ''
  root = repo
  for (const up of ['/..', '/../..']) {                   // this plugin is mod/ in the checkout
    if (!root && (await $.fs.exists(`${$.plugin.root}${up}/src/build.py`))) root = `${$.plugin.root}${up}`
  }
  if (!root) throw new Error('cannot find the notch-fight checkout: set the "repo" option')
  const all = (await $.fs.list(`${root}/build/clips`)).filter(d => d.kind === 'dir' && !d.name.startsWith('.')).map(d => d.name)
  let cfg: Config = {}
  try { cfg = JSON.parse(await $.fs.read(`${home}/.config/notch-fight/config.json`)) } catch { /* no config: defaults */ }
  const enabled = new Set(cfg.enabled ?? []), disabled = new Set(cfg.disabled ?? [])
  const off = new Set<string>()
  for (const c of all) if (await $.fs.exists(`${root}/build/clips/${c}/.default-off`)) off.add(c)
  allowed = cfg.newClips === 'disabled' ? all.filter(c => enabled.has(c))
    : all.filter(c => (off.has(c) ? enabled.has(c) : !disabled.has(c)))
  remaining = [...allowed]
  const first = typeof cfg.first === 'string' ? cfg.first.split(',') : cfg.first ?? []
  forced = first.map(n => n.trim()).filter(Boolean).map(n => (all.includes(n) ? n : pickOf(all.filter(c => themeOf(c) === n))))
    .filter((n): n is string => !!n)
}

const pickOf = (list: string[]) => (list.length ? list[Math.floor(Math.random() * list.length)] : undefined)

function pickNext(): string | undefined {
  if (remaining.length === 0) remaining = [...allowed]
  if (remaining.length === 0) return undefined
  let pool = remaining.filter(c => c !== last)
  if (pool.length === 0) pool = remaining
  const same = pool.filter(c => themeOf(c) === theme), other = pool.filter(c => themeOf(c) !== theme)
  if (same.length && (visits < MAX_PER_VISIT || other.length === 0)) return pickOf(same)
  return pickOf(other.length ? other : same)
}

// A clip's or transition's frames: build.py packs them into frames.png and writes how many in count
// (an older build left them loose, as NNN.png)
async function itemOf($: EngineInterface, dir: string, name: string): Promise<Item | null> {
  try {
    const count = (await $.fs.exists(`${dir}/count`)) ? parseInt(await $.fs.read(`${dir}/count`), 10) || 0
      : (await $.fs.list(dir)).filter(f => /^\d{3}\.png$/.test(f.name)).length
    return count ? { name, dir, count } : null
  } catch { return null }
}

// The image mode sends each frame as a PNG: a packed clip is unpacked once into build/mod/<name>.png/
// (scripts/frames.py, which skips it when that's up to date), loose frames are used as they are.
let pngsFor = '', pngsDir = ''
async function pngDir($: EngineInterface, it: Item): Promise<string> {
  if (pngsFor === it.dir) return pngsDir
  let out = it.dir
  if (await $.fs.exists(`${it.dir}/count`)) {
    out = `${root}/build/mod/${it.name}.png`
    const r = await $.process.run(['python3', `${root}/scripts/frames.py`, 'unpack', it.dir, out], { timeoutMs: 120000 })
    if (r.exitCode !== 0) throw new Error(`frames.py: ${r.stderr.slice(0, 200)}`)
  }
  pngsFor = it.dir; pngsDir = out
  return out
}

async function enqueue($: EngineInterface, name: string) {
  const t = themeOf(name)
  if (theme && t !== theme) {                             // the iris closes on this theme, opens on the next
    for (const half of [`${theme}__out`, `${t}__in`]) {
      const tr = await itemOf($, `${root}/build/transitions/${half}`, `t_${half}`)
      if (tr) queue.push(tr)
    }
  }
  const clip = await itemOf($, `${root}/build/clips/${name}`, name)
  if (clip) queue.push(clip)
  visits = t === theme ? visits + 1 : 1
  theme = t; last = name
  remaining = remaining.filter(c => c !== name)
}

const isCells = (m: Mode) => m !== 'image'
const isText = (m: Mode) => m === 'sextant' || m === 'octant'

// $.fs.read takes files up to 4 MB, so mod_cells.py writes a pack as chunks of whole frames
const CHUNK_BYTES = 3_000_000                           // the same number as scripts/mod_cells.py
const perChunk = () => Math.max(1, Math.floor(CHUNK_BYTES / (columns * rows * 9)))

async function loadPacked($: EngineInterface, it: Item, m: Mode) {
  const glyphs = isText(m) ? m : 'quad'
  const out = `${root}/build/mod/${it.name}.${columns}x${rows}.${glyphs}`
  const src = await $.fs.stat((await $.fs.exists(`${it.dir}/frames.png`)) ? `${it.dir}/frames.png` : `${it.dir}/000.png`)
  const have = (await $.fs.exists(`${out}/000.cells`)) && (await $.fs.stat(`${out}/000.cells`)).mtimeMs >= src.mtimeMs
  if (!have) {
    const r = await $.process.run(['python3', `${root}/scripts/mod_cells.py`, it.dir, String(columns), String(rows), out, glyphs], { timeoutMs: 120000 })
    if (r.exitCode !== 0) throw new Error(`mod_cells.py: ${r.stderr.slice(0, 200)}`)
  }
  packDir = out; packed = null; chunk = -1
}

// Frame i's first byte in `packed`, reading its chunk first when another one is in memory.
async function frameAt($: EngineInterface, i: number) {
  const per = perChunk(), c = Math.floor(i / per)
  if (c !== chunk || !packed) {
    packed = Uint8Array.fromBase64((await $.fs.read(`${packDir}/${String(c).padStart(3, '0')}.cells`, { as: 'bytes' })).base64)
    chunk = c
  }
  return (i - c * per) * columns * rows * 9
}

function cellsOf(start: number) {
  const n = columns * rows, p = packed!, words = new Uint32Array(n * 3)
  for (let k = 0, b = start; k < n; k++, b += 9) {     // a block character, its fg, its bg
    words[k * 3] = p[b] | (p[b + 1] << 8) | (p[b + 2] << 16)
    words[k * 3 + 1] = (p[b + 3] << 16) | (p[b + 4] << 8) | p[b + 5]
    words[k * 3 + 2] = (p[b + 6] << 16) | (p[b + 7] << 8) | p[b + 8]
  }
  return new Uint8Array(words.buffer).toBase64()
}

const hex = (p: Uint8Array, b: number) => '#' + ((p[b] << 16) | (p[b + 1] << 8) | p[b + 2]).toString(16).padStart(6, '0')

// Frame i as rows of runs: neighbouring cells that share both colours make one Text.
function runsOf(start: number): Run[][] {
  const p = packed!, out: Run[][] = []
  for (let y = 0, b = start; y < rows; y++) {
    const row: Run[] = []
    for (let x = 0; x < columns; x++, b += 9) {
      const ch = String.fromCodePoint(p[b] | (p[b + 1] << 8) | (p[b + 2] << 16)), fg = hex(p, b + 3), bg = hex(p, b + 6)
      const last = row[row.length - 1]
      if (last && last.bg === bg && (last.fg === fg || ch === ' ')) last.text += ch
      else row.push({ text: ch, fg, bg })
    }
    out.push(row)
  }
  return out
}

// One frame: move to the next item when this one is done, read the frame, swap it into the band.
async function tick($: EngineInterface) {
  if (isBusy) return                                     // a slow read or a cell pack: skip, never pile up
  isBusy = true
  try {
    const m = await read($, mode)
    if (!item || frame >= item.count) {
      if (!queue.length) {
        const name = forced.shift() ?? pickNext()
        if (!name) return
        await enqueue($, name)
      }
      item = queue.shift() ?? null; frame = 0
      if (!item) return
      if (isCells(m)) await loadPacked($, item, m)
    }
    if (isText(m)) {
      if (!packDir) await loadPacked($, item, m)
      runs = runsOf(await frameAt($, frame))
      await update($, tickNo, n => n + 1)                 // redraws the band
    } else if (isCells(m)) {
      if (!packDir) await loadPacked($, item, m)
      cells = cellsOf(await frameAt($, frame))
      if (site) await $.ui.blit({ requestId: site, key: KEY, cells })
    } else {
      png = (await $.fs.read(`${await pngDir($, item)}/${pad(frame)}.png`, { as: 'bytes' })).base64
      if (site) {
        const r = await $.ui.blit({ requestId: site, key: KEY, source: { png } })
        if (r.deny && /alt|placeholder|cannot/i.test(r.deny)) {     // this terminal shows no pictures
          if (!hasWarned) { hasWarned = true; $.ui.toast('Notch Fight: no inline images in this terminal, drawing cells instead') }
          await loadPacked($, item, 'raster'); cells = cellsOf(await frameAt($, frame))
          await update($, mode, () => 'raster')
        }
      }
    }
    frame += 1
  } finally { isBusy = false }
}


export const register: Register = (on, options) => {
  if (options.enabled === false) return                    // turned off in /config: no hooks at all
  rows = Math.max(4, Math.min(24, Math.round(Number(options.rows) || 10)))
  columns = Math.round((rows * 2 * 185) / 64)             // the clip is 185x64; a cell is twice as tall as wide
  repo = String(options.repo || '')

  on('session.start', async ($, e, next) => {
    const display = String(options.display)
    await update($, mode, (): Mode => (display === 'raster' || display === 'sextant' || display === 'octant' ? display : 'image'))
    await update($, isPlaying, () => false)
    return next(e)
  })

  on('turn.start', async ($, e, next) => {
    try {
      if (!root) await load($)
      if (allowed.length || forced.length) {
        await tick($)                                      // the first frame, before the band draws
        await update($, isPlaying, () => true)
        timer?.cancel()
        timer = $.clock.every(1000 / FPS, () => { void tick($).catch(err => $.ui.log(`notch-fight: ${err}`)) })
      }
    } catch (err) { $.ui.log(`notch-fight: ${err}`) }
    return next(e)
  })

  on('turn.complete', async ($, e, next) => {
    timer?.cancel(); timer = null
    await update($, isPlaying, () => false)
    return next(e)
  })

  on('ui.render', { component: 'AbovePrompt' }, async ($, e, next) => {
    if (e.surface !== 'terminal' || !(await read($, isPlaying)) || e.props.hasSurvey || e.props.bodyColumns < columns) return next(e)
    const m = await read($, mode)
    if (isText(m)) {
      await read($, tickNo)                               // subscribes: every frame redraws
      if (!runs.length) return next(e)
      const { Box, Text } = $.ui.resolve(e)
      return (
        <Box width={e.props.bodyColumns} justifyContent="flex-end">
          <Box flexDirection="column" width={columns}>
            {runs.map((row, y) => (
              <Text key={`r${y}`} wrap="truncate">
                {row.map((r, x) => <Text key={`c${x}`} color={r.fg} backgroundColor={r.bg}>{r.text}</Text>)}
              </Text>
            ))}
          </Box>
        </Box>
      )
    }
    if (m === 'image' ? !png : !cells) return next(e)
    site = e.requestId
    const { Box, Image, Raster } = $.ui.resolve(e)
    return (
      <Box width={e.props.bodyColumns} justifyContent="flex-end">
        {m === 'image'
          ? <Image key={KEY} source={{ png }} columns={columns} rows={rows} alt="Notch Fight (this terminal shows no images)" />
          : <Raster key={KEY} columns={columns} rows={rows} cells={cells} />}
      </Box>
    )
  })
}
