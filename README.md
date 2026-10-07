# Notch Fight

Pixel-art anime fights that drop out of the MacBook Pro notch while Claude Code is working.
Claude (the orange asterisk mascot) is always the protagonist.

![DBZ Cell Games](media/clips/dbz__cellgames.gif)

## Install

Requirements: **macOS** (ideally a MacBook with a notch), Xcode Command Line Tools (`swiftc`),
`python3`. Pillow is installed automatically if missing; `ffmpeg` is optional (GIF previews).

```bash
git clone <this repo> && cd notch-fight
./install.sh        # checks requirements, builds, registers the Claude Code hooks (idempotent)
./uninstall.sh      # removes the hooks and stops the app (--purge also deletes build/ + config)
nf clips            # choose which clips play (see "Choosing clips"); install.sh links `nf` into ~/.local/bin
nf pause 1h         # and the rest of the controls (see "The nf command")
# several Claude profiles? NOTCH_FIGHT_CLAUDE_DIRS=~/.claude-work:~/.claude-personal ./install.sh (same for uninstall)
```

Or just ask Claude Code in this repo: *"install this"* — `CLAUDE.md` tells it what to do.

**Platforms:** the app is macOS-only (Swift/AppKit + the notch API). The clip generator
(`src/`, Python + Pillow) runs anywhere. On a Mac without a notch the panel hangs from the top
centre with the default 185 pt width. A Linux port would only need a new player (e.g. a GTK
always-on-top borderless window) reading the same `build/clips` PNGs.

## How it works

- `NotchFight.app` hangs a black panel from the notch's bottom edge (width = notch width,
  detected at runtime via `NSScreen.auxiliaryTopLeftArea/RightArea`) and plays the clips.
- The app is **resident** (the default): it stays up, hidden, between prompts, and drops the panel as
  soon as a session starts working (about 75 ms from the prompt, against ~300 ms when it had to start
  each time). Hidden it holds no frames and runs no timers: ~13 MB and 0 % CPU. `nf resident on` also
  starts it at login; `nf resident off` goes back to starting it on each prompt and quitting after.
- Clicking the panel retracts it until your next prompt. `SIGTERM` (`pkill -x NotchFight`) retracts it
  and quits.
- Claude Code hooks in `$CLAUDE_CONFIG_DIR/settings.json` (default `~/.claude`; for several profiles: `NOTCH_FIGHT_CLAUDE_DIRS=~/.claude-work:~/.claude-personal ./install.sh`) drive it:
  - `UserPromptSubmit` → `scripts/notch-hook.sh start` (marks the session as working; starts the app
    if it is not up)
  - `Stop` / `StopFailure` / `SessionEnd` → `scripts/notch-hook.sh stop` (removes the mark; `SIGUSR1`
    tells the app to look again: resident, it hides; otherwise it retracts and quits)
  - `Notification` (`permission_prompt`, `elicitation_dialog`, `elicitation_url_dialog`, `agent_needs_input`)
    → `scripts/notch-hook.sh wait`: Claude is waiting for you. The mark gets ` waiting` and the panel
    shows a **NEEDS YOU** alert over the clip (the edge pulses in Claude's orange), right away even with a
    delay and even after a click.
  - `PostToolUse` / `PostToolUseFailure` / `ElicitationResult` (and the `elicitation_complete` /
    `elicitation_response` notifications) → `scripts/notch-hook.sh work`: the alert comes off once the
    tool ran or the question was answered. It does nothing unless the session was waiting (plain bash,
    no Python: it runs after every tool call).
  - To see which hooks fire: `touch ~/.config/notch-fight/hook.log` and each call is noted there (mode,
    event, notification type, tool); delete the file to stop.
- Several sessions can work at once (even across profiles): each one leaves a marker in
  `~/.config/notch-fight/sessions/` with its `claude` PID (rewritten on each prompt), and the panel
  retracts only when the last one stops. The resident app watches that folder, so it reacts at once.
  With more than one working, a small badge in the bottom right corner says how many (`✱3`). The app also drops markers of dead PIDs (e.g. a closed terminal never fires
  `Stop`). An interrupted turn (Esc) doesn't fire `Stop` either: the panel stays until that
  session's next turn ends, or click it.

## Themes and loop keyframes

Each theme has its own neutral pose (the "loop keyframe"). Every clip of a theme starts and
ends on it. Switching theme plays a
pre-rendered asterisk-iris transition: the iris closes on the theme being left (`transitions/<from>__out`)
and opens on the next one (`transitions/<to>__in`), two halves per theme rather than one per pair.

| Theme | Claude as | Opponent | Clips |
|---|---|---|---|
| `dbz` | Claude (goes Super Saiyan) | Perfect Cell, on the Cell Games ring | cellgames |
| `ygo` | Yugi-style duelist (D-D-D-DUEL and Heart of the Cards close-ups, Dark Magician card reveal, Mirror Force) | Kaiba + Blue-Eyes White Dragon hologram, in the Kaiba Corp stadium (life points 8000 to 0) | duel |
| `kny` | Tanjiro-style swordsman (Water Breathing dragon and Hinokami Kagura close-ups) | Akaza (kanji-eye close-up), on the Mugen Train roof; beheaded, crumbles to ash | breath |
| `jjk` | Gojo at the Shibuya crossing on 10.31 (Infinity stops Dismantle and the lunge — MUGEN, blindfold-off SIX EYES close-up, Blue, Red, HOLLOW PURPLE close-up erases the street) | Sukuna (Dismantle slashes, blown into the 109 tower, reforms from cursed motes) | infinity |
| `fn` | Jonesy with a pickaxe (cranks 90s to high ground, wood-edit shotgun close-up — 200 HEADSHOT, #1 VICTORY ROYALE crown card, default dance) | Geno, on the island (Tilted Towers skyline, Battle Bus overhead, the storm wall closing in; AR, rocket, eliminated into cubes) | royale |
| `pkm` | Claude in Ash's cap on a GBA battle screen (FIGHT menu, HP/EXP boxes; Quick Attack, Shadow Ball — SUPER EFFECTIVE close-up, levels up, YOU WIN!, Poke Ball GO! close-up) | Mewtwo on the far platform (Psychic warps the screen, faints, a wild one appears) | psychic |
| `snk` | Survey Corps scout (ODM gear) | a grinning Titan in Trost (red roofs, church spire, the Wall; grin + crossed-blades close-ups, SHINZOU WO SASAGEYO!, nape slash, steam) | survey |
| `nrt` | Naruto in the Hidden Leaf under the Hokage faces (hand-seal close-up, shadow clones, leaps the Great Fireball, Rasengan close-up) | Madara (gunbai swats the clones, Sharingan close-up, Katon) | shadowclone |
| `naruto-edo` | Naruto on the Fourth Great Ninja War battlefield (clones, Rasengan, Sage Mode close-up, Rasenshuriken wind dome) | Kabuto + Edo Tensei'd Codex, OpenCode, Grok (coffin close-up, paper-dust regeneration) | edotensei |
| `naruto-shikamaru` | Shikamaru in the Nara clan forest: hops the scythe, the thinking-pose close-up (WHAT A DRAG...), Kagemane catches Hidan mid-run and he copies every move, Asuma's lighter in close-up (FOR ASUMA.), the tags go up: CHECKMATE. | Hidan (FOR JASHIN!, I CANT MOVE!, climbs out of the pit: I AM IMMORTAL!) | kagemane |
| `naruto-zabuza` | Kakashi (Sharingan close-up, copied jutsu) | Zabuza on the lake (Water Dragons clash, Great Waterfall) | waterdragon |
| `naruto-lee` | Rock Lee in the Chunin Exam hall: Konoha Senpu, the leg weights in close-up (LEE! TAKE THEM OFF!, DOSUN!), too fast for the sand, the Eight Gates close-up (KAIMON! KYUMON! SEIMON!), Kage Buyo and the bandage drill: OMOTE RENGE! | Gaara (the sand shield rises by itself, sand stream, sand armour flakes off, gathers back from a heap of sand) | lotus |
| `dbz-buu` | Claude, then Clodex (fusion dance with Codex, FU-SION-HA! close-up, goes blue for the Final Kamehameha) on the Supreme Kai's world | Kid Buu (grin close-up, planet-destroying ball, regenerates) | fusion |
| `jjk-sukuna` | Gojo in ruined Shibuya under a red moon (hand-sign close-up with one Six Eye, Unlimited Void swallows the shrine, four Black Flashes) | Sukuna (grin close-up with four eyes, Malevolent Shrine, Dismantle + Cleave storm) | domain |
| `jjk-toji` | Toji (Inventory curse, Inverted Spear of Heaven, SORCERER KILLER close-up) | young Gojo: the spear shatters his Infinity | sakahoko |
| `jjk-maki` | Maki, awakened (glasses crack close-up, afterimage cuts) | the Zen'in clan, then her father Ogi | zenin |
| `hxh` | Gon (fishing rod, adult form close-up) | Neferpitou (Terpsichora) | jajanken |
| `fma` | Colonel Mustang (glove snap close-up, flame alchemy) | Envy (disguised as Claude, burned to his true form) | flame |
| `dbz-jiren` | Claude in Ultra Instinct (silver-eyes close-up, dodges everything, instant hits from everywhere) at the Tournament of Power | Jiren (red glare close-up, knocked off the arena) | ultra |
| `dbz-freezer` | Claude as Goku with Codex on planet Namek (Codex lifted and blown into light, CODEX...! FREEZEEER!!! rage close-up, storm and lightning, first SUPER SAIYAN close-up, Kamehameha) | Freezer, final form (smug close-up closing his hand, Death Beams, Death Ball; Porunga revives Codex) | namek |
| `mk` | Claudepion (Scorpion: spear, Toasty fatality) | Sub-Zero, with the arcade HUD | fatality |
| `apex` | a Legend with jump pack and grapple (kill-leader banner close-up) | Wraith (Into the Void, Dimensional Rift) | champion |
| `cs` | Counter-Terrorist (AWP scope close-up, defuse) | Phoenix Terrorist, with the 1.6 HUD | defuse |
| `hl` | Gordon Freeman in the HEV suit (crowbar, Gravity Gun) | headcrabs + a Combine soldier (G-Man close-up) | lambda |
| `rm` | Rick with the portal gun | a Cromulon (SHOW ME WHAT YOU GOT!) | schwifty |
| `inv` | Invincible (Mark) | Omni-Man: the train, then PIENSA CLAUDE! (close-up) and the beatdown | train |
| `sf` | Ryu (Hadouken, Shoryuken, Shinku Hadouken close-up) | M. Bison, with the SF2 HUD | hadouken |
| `mario` | Mario (? blocks, Super Star close-up, the axe) | Bowser on the castle bridge | castle |
| `mc` | Steve (pillar, bow, diamond sword) | a Creeper (close-up) and the Ender Dragon | enderdragon |
| `ds` | a Sun knight (roll, Estus, PRAISE THE SUN, fake YOU DIED) | Malenia | felled |
| `sw` | a Jedi | Darth Vader (I AM YOUR FATHER close-up) | father |
| `matrix` | Neo (bullet time, NO.) | Agent Smith and his clones | bullettime |
| `term` | the T-800 (red HUD close-up) | the T-1000 (frozen and shattered) | judgment |
| `bb` | Heisenberg (SAY MY NAME: CLAUDENBERG) | Tuco | saymyname |
| `snk-colosal` | Survey Corps scout (ODM gear) | the Colossal Titan behind the Wall (eye close-up) | colossal |
| `jojo` | Jotaro-style Stand user (ORA ORA barrage, moves in stopped time) | DIO and The World (ZA WARUDO, clock close-up) | theworld |
| `jojo-golden` | Giorno at the Colosseum at night (sub-theme of `jojo`): golden curls and braid, pink suit with the ladybug brooch, Gold Experience; hit while time is erased without ever seeing it, the Arrow pierces his Stand in close-up (GOLD EXPERIENCE REQUIEM), RETURN TO ZERO., MUDA MUDA MUDA with damage numbers, the last MUDA!, ARRIVEDERCI. | Diavolo and King Crimson (KING CRIMSON!, TIME HAS BEEN ERASED! with a red glitch and afterimages; blown away, he never reaches death: falls, and falls again, the loop restarting) | requiem |
| `jojo-diamond` | Josuke (sub-theme of `jojo`) with Crazy Diamond in a Morioh street at dusk: MY NAME IS YOSHIKAGE KIRA..., Killer Queen's coin goes CLICK and BOOM, Sheer Heart Attack rolls in (LOOK HERE!) and gets punched into the wall, the hair gets mocked: the rage close-up (WHAT DID YOU SAY ABOUT MY HAIR?!), DORARARARA, Crazy Diamond repairs the wall and the blood drops fly back into Kira as bullets | Yoshikage Kira and Killer Queen | kira |
| `jojo-stone` | Jolyne (sub-theme of `jojo`) in the Green Dolphin Street prison yard at night (searchlight, the wall, the sea, the fence): Whitesnake pulls a DISC out of her head and she falls asleep, she unravels into string and a thread pulls the disc back, the tattooed arm in close-up coming undone into taut strings (STONE FREE!); MADE IN HEAVEN: time accelerates (sun and moon race across the sky, day and night flicker, shadows spin), she weaves a string net and Pucci flies right into it: CAUGHT!, ORA ORA ORA, YARE YARE DAWA. | Enrico Pucci, with Whitesnake and Made in Heaven (a blur hitting from everywhere, slammed into the fence) | heaven |
| `etendo` | Claude the brand designer | the old Etendo logo (grabbed, spun, morphed into the new star in a close-up — NEW ETENDO!) | rebrand |
| `sl` | Sung Jinwoo, the Shadow Monarch (twin daggers, ARISE! close-up, shadow army) | Igris the Blood-Red Knight, extracted as a shadow (System windows) | arise |
| `memes` | Claude on a vaporwave stage (hug, uppercut, blast, deal-with-it shades) | a meme boss rush: Forever Alone, Tung Tung Tung Sahur, then the FINAL BOSS "6 7" (close-up, weighing-gesture attacks) | bossrush |
| `ben10` | Ben Tennyson with the Omnitrix (HERO TIME close-up, Heatblast, Four Arms, XLR8, the watch times out, Diamondhead) | Vilgax in the desert at night | hero |
| `ppg` | the fourth Powerpuff Girl over Townsville at dusk (big shiny eyes, flies on an orange streak, flying punch; Blossom, Bubbles and Buttercup dive in and hit one after another, POW! into orbit, AND SO, ONCE AGAIN, THE DAY IS SAVED!) | Mojo Jojo with a ray gun (I, MOJO JOJO, SHALL DESTROY YOU!, shoots Claude out of the sky, crashes back down: CURSE YOU, POWERPUFF CLAUDE!) | townsville |
| `dexter` | Dexter in CLAUDE'S LABORATORY (glasses, lab coat, purple gloves; DEE DEE! GET OUT OF MY LABORATORY!, pulls the lever and the mech drops around him, stomps and fires lasers; comes out of the smoke black with soot: DEE DEEEE!) | Dee Dee (OOOH! WHAT DOES THIS BUTTON DO?, pirouettes through every shot, presses the big red button: SELF DESTRUCT, KABOOM!) | lab |
| `samuraijack` | Jack in the desert at sunset with Aku's city on the horizon (LONG AGO, IN A DISTANT LAND..., Genndy-style split screen as the robots creep in, eyes and katana-gleam close-up, one cut and the robots slide apart leaking black oil, leaps the giant hand and takes a finger off, sheathes slowly: CLICK.) | Aku (HA HA HA!, three beetle robots, ENOUGH! and turns into a giant hand, dissolves in smoke: CURSE YOU, SAMURAI!) | aku |
| `foster` | the new imaginary friend in Foster's grand hall, no fight (staircase, gilt portraits, chandelier, red carpet): BET YOU CANT BEAT THIS!, a paddle-ball contest with counters while Eduardo (NO ME GUSTA!), Coco (lays a plastic egg: COCO! COCO!) and Wilt (SORRY! SORRY!) go by; Bloo's string snaps, the ball ricochets round the hall and smashes the vase (CRASH!); Mr. Herriman's monocle in close-up (MASTER CLAUDE! RULE 37!); wins 99 TO 98, Frankie sweeps up with a SIGH... and puts out a new vase | Bloo (HE DID IT!, NO FAIR!, REMATCH!) | bloo |
| `simuladores` | the fifth simulador in a dark suit and dark glasses, on a Buenos Aires street at night with the team's van: no fight, an operation (the client wrings his hands: ME ESTAFARON..., UN NUEVO CASO card, the plan on the whiteboard name by name with every arrow into CODEX, Ravenna turns inspector in a puff of smoke, Lamponne with his toolcase, a three-panel montage: CONFIE EN MI, FIRME ACA, ERA TODO SIMULADO; the handshake in close-up: GRACIAS, MUCHACHOS; the five walk in slow motion; the CUESTIONARIO DE SATISFACCION, every box ticked) | Codex, the crook with the briefcase of money (QUE TAL, AMIGO?) | operativo |
| `jakelong` | Jake Long, the American Dragon, on the Chinatown rooftops of New York at night (black hair with green tips, red jacket; ollies the first staff blast on his skateboard, the DRAGON UP! close-up as the fire runs up his body into the red dragon, flies through the blasts and breathes fire; Fu Dog on the pagoda roof: YO, JAKE! LOOK OUT!, burns his way out of the Huntsclan net, a tail-whip: WHAM!, lands back as Jake: HAHA, DRAGON!) | the Huntsman, with the bone mask and the green-blast staff (THE DRAGON WILL BE MINE!, HOLD STILL, DRAGON!, GOT YOU!; whipped into the sky, drops back dizzy) | dragon |
| `spongebob` | SpongeBob at the grill outside the Krusty Krab under Bikini Bottom's flower clouds (I'M READY! I'M READY!, flips Krabby Patties, hops the robot's claw without leaving the grill and flips patties into it: SPLAT!; Squidward at the door: UGH., Mr. Krabs bursts out: MONEY! MONEY! MONEY!; the ORDER UP! close-up with the spatula and shining eyes; one last patty into the cockpit, a bubble wipe and the 2000 YEARS LATER... title card) | Plankton in his giant robot (THE FORMULA WILL BE MINE!, HEH HEH HEH!, falls apart and flies back to the Chum Bucket: I'LL GET YOU NEXT TIME!, trudges back: SIGH...) | krabby |
| `dannyphantom` | Danny Fenton in Amity Park at night, Fenton Works and the green portal swirling at its door (the ghost sense's blue wisp, the GOIN' GHOST! close-up: two white rings sweep him into the black-and-white jumpsuit, white hair, green eyes; floats, goes intangible and the missiles fly right through: MISSED ME!, a green ecto-blast, the Ghostly Wail close-up: AAAAAAA! shockwaves fill the screen; the Fenton Thermos vortex: GOTCHA!, the rings take him back to human) | Skulker, the armoured ghost hunter with the flaming mohawk and the shoulder launcher (I'LL HAVE YOUR PELT, WHELP!; pops the thermos lid and reforms: I'LL BE BACK, WHELP!) | ghost |
| `cyberpunk` | V in the Samurai jacket inside the Maelstrom plant in Watson (red neon, rain on the windows, Night City through a blown-out wall): the scan tags him THREAT: EXTREME, the SHORT CIRCUIT quickhack fries him in a glitch, SANDEVISTAN slows the world and V leaves colour trails landing three mantis-blade cuts (3X CRIT!), leaps the arm cannon's shot; Johnny Silverhand flickers in like a broken hologram in close-up (WAKE UP, SAMURAI. WE HAVE A CITY TO BURN.), one shot of the Malorian: BANG!, FLATLINED. | Royce, the Maelstrom boss (red optics, jaw mask, powered exoskeleton with an arm cannon: YOU'RE DEAD, CHOOM!) | nightcity |
| `cyberpunk-edgerunners` | David Martinez (sub-theme of `cyberpunk`) in the Arasaka plaza at night, rain and neon under a huge moon: the yellow ambulance jacket, the green streak, the Sandevistan down his spine; SANDEVISTAN: the world goes green and slow, the bullets hang in the air and he walks between them trailing afterimages; Lucy fades out of her optical camo and hacks the tower (BREACH PROTOCOL, the drones drop: I GOT YOU, DAVID.); the arm gets crushed (CRUNCH, the red CYBERPSYCHOSIS glitch, red eyes), the Militech cyberskeleton closes on him plate by plate in close-up (I'M GONNA GET TO THE TOP), the brawl to the edge (AAAAARGH!); Lucy on the Moon in close-up, the Earth in the sky: I WANT TO GO TO THE MOON. | Adam Smasher (opens fire, HEH., the crushing grip, pushed to the edge of the plaza) | moon |
| `sonic` | Claude as a blue hedgehog in Green Hill (rings, spin dash, loop-de-loop, ring loss, 7 Chaos Emeralds, SUPER CLAUDE) | Dr. Eggman in the Egg Mobile with the wrecking ball (GOT THROUGH ACT 1 tally) | greenhill |
| `tetris` | Claude in an ushanka (punches and kicks the falling pieces into place, FINALLY! I-piece close-up, TETRIS!) | the falling tetrominoes on an NES/Game Boy playfield in front of the Kremlin (4-line clear, Game Boy rocket ending) | tetris |
| `clippy` | Claude on a Windows 98 desktop (clicks NO, punches error dialogs, END TASK, bends him straight into the Recycle Bin) | Clippy in a DEATH MATCH (NEED HELP? spam, grows huge, turns into a bicycle/bell/question mark, crazy-eyes close-up) | deathmatch |
| `predator` | an 80s jungle commando (laser triple-dot, thermal-vision close-up, mud camouflage, log trap) | the Predator (decloaks, unmasks with a RAAARGH!, wrist self-destruct and mushroom blast) | hunt |
| `alien` | a warrant-officer survivor with a pulse rifle, then in the yellow power loader (motion-tracker and inner-jaw close-ups, GET AWAY FROM HER!) | the Xenomorph (acid blood that eats the deck, blown out of the airlock) | nostromo |
| `avp` | Claude caught between them in the Antarctic pyramid (WHOEVER WINS... WE LOSE., clan-mark close-up, alien-head shield + spear, back-to-back close-up) | a Xenomorph, the Predator and the Queen (buried under the collapsing pyramid) | pyramid |
| `gta` | CJ on Grove Street (AH SHIT HERE WE GO AGAIN..., wanted stars, handbrake donut, MISSION PASSED!) | a low-poly 3D police cruiser (flat-shaded software renderer: chase, barrel roll, explosion) | grove |
| `simpsons` | a Sector 7G worker (D'OH!, stomps the uranium rod back in, MMM... ROSQUILLAS) | Mr. Burns and his hounds in the nuclear plant (EXCELENTE... close-up) | meltdown |
| `portal` | the test subject with the Portal Gun in an Aperture test chamber (drops through blue/orange portals, turns the turret fire back through them, shoots a portal at the MOON; THIS WAS A TRIUMPH card, the cake is a lie) | GLaDOS on her ceiling arm (turrets, neurotoxin, yellow-to-red eye close-up — YOU MONSTER; her cores pop off, Wheatley babbles, SPAAACE!; sucked out into space) | triumph |
| `amongus` | an orange crewmate with Codex in The Skeld cafeteria (fix-wiring close-up, spots Codex venting ?!, lights out, DEAD BODY REPORTED, CODEX VENTED! meeting, VICTORY) | Codex, the impostor (I WAS IN ELECTRICAL, sweating close-up, voted off: CODEX WAS THE IMPOSTOR.) | impostor |
| `pvz` | Crazy Dave with a saucepan on his head, on his front lawn (grabs suns, plants a wall-nut, lobs a cherry bomb: KABOOM; rides the lawn mower over THE ZOMBIES ATE YOUR BRAINS!; BECAUSE IM CRAAAZY! close-up, YOU GOT A NEW PLANT! card) | a wave of zombies (arm and head shot off, conehead, buckethead; CHOMP wall-nut close-up), then Codex as Dr. Zomboss on the Zombot (> RM -RF LAWN, hurls an imp; blown off the screen) | lastwave |
| `meshi` | Laios (sword, I WONDER HOW IT TASTES... close-up) | the Red Dragon, then Senshi cooks it: DRAGON STEW | dragonstew |
| `terraria` | the Terrarian: Terra Blade beams, or a staff + whip with a Stardust Dragon | the Eye of Cthulhu (servants, phase 2 close-up, coins) | melee, summoner |
| `mist` | Vin, Mistborn (mistcloak, Steel Pushes on coins, ATIUM close-up with her future shadows) | a Steel Inquisitor in Luthadel's mists and ash (she Pulls the spike from his back); off by default | inquisitor |
| `mist-kelsier` | Kelsier, the Survivor of Hathsin, in Fountain Square under the red sun (sub-theme of `mist`, off by default): hops the axe, Steel-Pushes coins, a pewter punch; the spear, and the smile in close-up (THERES ALWAYS ANOTHER SECRET); the skaa raise their hands, the mists roll in and he stands up out of them | a Steel Inquisitor, then the Lord Ruler | survivor |
| `deadpool` | Deadpool (katanas, the arm pops off and a tiny one grows back, talks to us in yellow boxes and knocks on the notch, MAXIMUM EFFORT close-up); `notchverse`: a TVA door into the other themes (steals Madara's gunbai, tells the Cyclops he is NOBODY, OH NO. close-up before Cell's Kamehameha, comes home charred: WORTH IT.); `webcam`: finds the MacBook camera (fisheye close-up: HI MOM!), pushes the panel's edges, waits on Claude (STILL THINKING?) and dozes off as the panel closes (HEY! NOT YET!); `review`: reads Claude's PR on Etendo_schema_forge out loud, judges the Etendo rebrand in close-up, stamps it LGTM and merges it with a katana | Wolverine in the Void (SNIKT, takes the chimichanga: BUB.); Madara, Polyphemus, Cell | bub, notchverse, webcam, review |
| `spidey` | Miles Morales, on twos with magenta/cyan rim light (camouflage split into comic panels, A LEAP OF FAITH close-up, the city turns upside down with streaking lights, THWIP, webs, venom blast ZZAKT!) | the Prowler in Brooklyn (webbed to a wall, police lights) | leap |
| `xmen-nightcrawler` | Nightcrawler (X-Men '97) on a New York rooftop at dusk: BAMF out of the crossfire, pops up behind each drone in a puff of indigo smoke, the yellow-eyed grin in close-up (BAMF!), teleports the last one into the sky (AUF WIEDERSEHEN!) | four Sentinel drones (MUTANT DETECTED) | bamf |
| `xmen-gambit` | Gambit (X-Men '97) in the French Quarter at night: a charged card for each drone (BONJOUR MES AMIS), vaults the giant hand on his staff, the ace of spades in close-up (CHARGED), blows the Sentinel apart and walks out of the smoke (DEALER WINS.) | three Sentinel drones, then a giant Sentinel (SURRENDER MUTANT) | charged |
| `coraline` | Coraline in stop-motion (the little door and the tunnel, NO., the seeing stone close-up with the ghost children's eyes, the escape with the cat, the button key: CLICK.) | the Other Mother: WE ONLY WANT YOU TO STAY., then her spider form with needle fingers | buttons |
| `odyssey` | Odysseus in a Corinthian helmet in the Cyclops' cave (Homer, book 9): gives him wine, the MY NAME IS NOBODY close-up, the olive stake heated in the fire and driven into the eye (close-up, TSSSS), rides out under the ram | Polyphemus (WHO ARE YOU?, MORE WINE!, NOBODY IS HURTING ME!; the other Cyclopes: NOBODY? THEN HUSH!) | nobody |
| `dnd` | A wizard (pointed hat, starry robe, beard, crystal staff), the DM narrating in parchment boxes: `nat20` (ROLL INITIATIVE, Shield against the eye rays, the d20 close-up lands NAT 20!, Fireball: CRITICAL HIT!) and `nat1` (the d20 lands NAT 1., the fireball comes down on his own hat: CRITICAL FAIL, PRESTIDIGITATION to clean up) | a Beholder (crashes and dreams another Beholder; laughs at the NAT 1) | nat20, nat1 |
| `ghibli-totoro` | Satsuki at the bus stop in the rain, no fight (fireflies, the lamp, lends Totoro the spare umbrella, grin close-up, the Catbus's headlight eyes, a bundle of acorns) | Totoro and the Catbus | busstop |
| `phm` | Ryland Grace in the Hail Mary's lab, no fight: `rocky` (the Blip-A, the xenonite tunnel, chords that become AMAZE AMAZE AMAZE, FIST MY BUMP close-up) and `astrophage` (the star dims, the bench, Taumoeba under the microscope, IT WORKS!); off by default | Rocky, a friend; Astrophage, the problem | rocky, astrophage |
| `arg` | the albiceleste number 10 in the 2022 World Cup final (Dibu's leg on Kolo Muani at 123 in close-up, PENALES with the TV scoreboard, GOL, Montiel's last penalty, CAMPEONES DEL MUNDO, the Cup and the third star) | France | final |
| `arg-86` | Diego at the Azteca, 1986 (sub-theme of `arg`), with the TV scoreboard: `mano` (the one-two with Valdano, Hodge's loop, up against the taller Shilton, the fist in close-up, the English round the referee, LA MANO DE DIOS) and `siglo` (the spin in his own half, the camera following his run past a slide, two lunges and the keeper, Butcher from behind; TA TA TA TA, GOLAZO, BARRILETE COSMICO, DE QUE PLANETA VINISTE) | England | mano, siglo |
| `arg-mate` | No fight: a ronda de mate in a patio under the parra, the flag with the Sol de Mayo on the wall: the first one for the cebador (EL PRIMERO ES DEL CEBADOR), the mate going round with facturas (RRRP), the yerba in close-up until ESTA LAVADO, a GRACIAS, the golden hour | three friends | ronda |
| `arg-colapinto` | Franco Colapinto, number 43, in the dark-blue Williams: the five red lights (AND AWAY WE GO!), four cars passed as the TV tower takes COL from P12 to P8, team radio (GOOD JOB FRANCO. P8. POINTS.), the chequered flag, the helmet in close-up with the stands in its visor (VAMOS FRANCO), a lap of honour under the flags | the rest of the grid | debut |
| `arg-alejo` | No fight: Carlitox from Alejo y Valentina (LocoArts), green hair everywhere, on the couch next to Alejo with Valentina by, the TV and the CUADRITO: MIRA COMO REVOLEO LAS PATAS, the legs spin from the hip like a fan; close-up: HOLA, VENGO A REVOLEAR LAS PATAS! | Alejo and Valentina, watching | patas |
| `arg-alejo-flotar` | No fight: Carlitox on the series' other set (the orange wall, the brown curtain, the green floor): HOLA, VENGO A FLOTAR, and he floats off, comes back and slips behind the curtain | nobody | flotar |
| `arg-cordoba` | No fight, a cuarteto dance in Córdoba: coloured lights sweeping the floor, the CUAR - TE - TO sign lighting up to the beat, La Mona Jiménez on the stage (the curly mane, bare-chested), the ronda going round in 2.5D (the far side smaller, everyone sorted by depth); Claude at the bar in Belgrano's sky blue with the 2.25 l Coca bottle cut in half (the waist, the five-lobed foot): ice, fernet to a third, then the Coca; close-up: nearly full, the Coca still pouring, the foam swelling over the ice to the brim, FERNET CON COCA, RICASO CULIAO; up it goes, into the ronda (ARRIBA CORDOBA!), down in one (AHH!), back to the bar | nobody | fernet |
| `cai` | Independiente, the Rojo (red shirt, blue shorts), in the clasico de Avellaneda at the Libertadores de America: past three Racing defenders (OLE!: a nutmeg, a lob, a feint), the strike in close-up, top corner (GOL DEL ROJO, red flares), the trophy cabinet in close-up as the seven Libertadores light up: REY DE COPAS | Racing | clasico |
| `eternauta` | Juan Salvo in the home-made insulated suit (El Eternauta), on a street in Vicente Lopez under the deadly snowfall: the bullets spark off the shell (PAC! PAC! PAC!), a Mano at its console in close-up driving the beetles, Favalli, Lucas and Polsky come out of the snow and fire together (FUEGO!), four visors in close-up: NADIE SE SALVA SOLO | a cascarudo, the giant beetle (the snow buries it) | nevada |
| `thebear` | Carmy (The Bear) at the pass, the blue LED clock and its EVERY SECOND COUNTS plaque over the line: the printer spits tickets (ORDERS IN!), the brigade's YES CHEF!, a pan in flames, BEHIND!, a smashed plate, the clock racing through a whole day; the clock and the plaque in close-up, glowing with every second; the last plate with the tweezers (HANDS!) and the quiet after | the dinner service (Sydney, Marcus, Tina and Richie on the line) | service |
| `lol` | Quinn and Valor (League of Legends) in a lane of Summoner's Rift: bolts, damage numbers and gold, Harrier's mark; Q, Blinding Assault (Valor dives); Valor's eye in close-up (DEMACIA!); E, Vault; R, Behind Enemy Lines over the turret (TURRET DESTROYED); VICTORY | a red minion wave and the enemy turret | valor |
| `lol-yasuo` | No fight: Yasuo (League of Legends) at sunset in Ionia, on a rock under a cherry tree, playing the bamboo flute, the notes drifting off as petals; eyes closed in the wind in close-up (DEATH IS LIKE THE WIND. ALWAYS BY MY SIDE.); a bird lands on his katana, a sip of sake | nobody | flute |
| `thisisfine` | No fight: the This Is Fine dog (KC Green's Gunshow) in his bowler hat, sipping coffee at the kitchen table while the fire climbs the walls and the pictures turn into BUILD FAILED, PROD IS DOWN and DEPLOY FRIDAY; the calm smile in close-up (THIS IS FINE.), IM OKAY WITH THE EVENTS THAT ARE UNFOLDING CURRENTLY., then the smoke clears | the fire | fine |
| `wednesday` | No fight, as in the meme's panel: Captain Haddock a bit worse for wear (hair everywhere, red nose) slumped over the bar with a pint, in Herge's clear line: WHAT A WEEK, HUH? / CAPTAIN, IT'S WEDNESDAY; his bleary face in close-up (the eyes pop: BLISTERING BARNACLES!), Snowy sniffing the beer | Tintin and Snowy | wednesday |
| `memento` | Leonard Shelby, and the film's structure as the clip: colour running backwards (the polaroid un-develops, the casing flies back into the gun), black and white forwards (the motel phone: REMEMBER SAMMY JANKIS.), the chest tattoo in close-up (JOHN G. RAPED AND MURDERED MY WIFE), Teddy's polaroid (DON'T BELIEVE HIS LIES), and the end meets the start: a polaroid develops and the colour comes back | John G., whoever he is | polaroids |
| `skyrim` | The Dragonborn in the horned iron helmet, at night in the snowy mountains under the aurora, the compass and the combat bars as in the game: a dragon lands on the watchtower and breathes fire (YOL TOOR SHUL) onto his shield; the close-up FUS... RO... DAH!; the shout throws it off the tower, it burns to bone and its soul streams into him (DRAGON SOUL ABSORBED). `awake`, no fight: the screen goes black and the eyes open on the cart to Helgen, hands tied, Ralof across from him (close-up: HEY, YOU. YOU'RE FINALLY AWAKE.), YOU WERE TRYING TO CROSS THE BORDER, RIGHT?, Lokir's DAMN YOU STORMCLOAKS., the gate of HELGEN | a dragon | fusrodah, awake |
| `haikyuu` | In 2.5D (the court in perspective, everyone sorted by depth with a shadow, the net a see-through plane, the ball with its height and shadow): Hinata in Karasuno's black kit, the FLY banner, KRS 20-19 SRZ. Shiratorizawa serves, Nishinoya digs, Kageyama sets while Hinata runs in on the diagonal and leaps eyes shut (Tendou has already guessed wrong); the close-up from behind him in the air, the 10 on his back, the block below not reaching, THE VIEW FROM THE TOP; the spike over Ushijima's hands, crow feathers, 21-19, OI, I'M HERE! | Shiratorizawa (Ushijima, Tendou) | quick |
| `fightclub` | The Narrator (white shirt, loosened tie, a black eye) in the basement of Lou's Tavern, the bulb swinging over the ring of men: THE FIRST RULE OF FIGHT CLUB IS... (the rest crossed out); bare knuckles with Tyler (red leather jacket, shades), the blood landing on the concrete; the close-up: the bloody grin, the Paper Street soap, I AM JACK'S SMIRKING REVENGE.; Tyler flickers and is gone, he's hitting himself; the towers coming down outside the window, WHERE IS MY MIND?. `firstrule`, for laughs and no blood: cardboard rules drop from the ceiling and cross themselves out the moment he reads them aloud (BZZT!; RULE 2 is RULE 1 again), RULE 8 points at him (...ME?); Tyler: HIT ME AS HARD AS YOU CAN, and it's the ear (OW! IN THE EAR, MAN?); a cartoon brawl cloud; the dust clears and he's alone, punching himself — close-up: WHY AM I HITTING MYSELF?; Tyler, there all along or not: FIRST RULE. | Tyler Durden (himself) | rules, firstrule |
| `arcane` | Jinx (the blue braids to her boots, pink eyes, cloud tattoos, striped trousers) with Fishbones, the shark-faced launcher, in Zaun under golden Piltover, her pink graffiti on the walls: Vi walks in with the Atlas gauntlets, POWDER...; the voices, pink scribbles round her head; a rocket on the gauntlets, Vi charges, a wind-up monkey bomb, every blast lights the graffiti up; the close-up in the scribbles, I AM JINX; the last rocket to the Council's tower, a pink blast with drawn clouds, and Vi just watches, then goes | Vi, her sister | sisters |
| `basterds` | Lt. Aldo Raine (olive jacket, slicked hair and moustache, the rope scar, the Bowie knife) in the French woods by the old stone tunnel, a German sergeant and a private on their knees: TELL ME WHERE YOUR BOYS ARE. / I RESPECTFULLY REFUSE, SIR. / DONNY!; out of the dark, the bat on the stone, TOC... TOC... TOC!; the close-up: the Bear Jew comes out of the black, THE BEAR JEW; one swing (a white cut, CRACK), the Basterds whoop; Aldo crouches by the private: THIS JUST MIGHT BE MY MASTERPIECE. | the Nazis | bear |
| `basterds-cinema` | The premiere at Le Gamaar (its own set, no fight): Shosanna in the red dress at the end of the aisle while Stolz der Nation plays to a full house (the sniper in his bell tower, the grain, the projector's beam over the rows of caps); she slips out — CHAPTER FIVE: REVENGE OF THE GIANT FACE — the reel cuts and her face comes up on the screen: THIS IS THE FACE OF JEWISH VENGEANCE.; the nitrate catches behind it, the fire climbs the curtains; close-up: her face thrown onto the smoke, laughing; the screen is gone, the house in flames | the premiere's audience | cinema |
| `hp` | Harry (round glasses, the scar, the Gryffindor scarf) in the graveyard at Little Hangleton: leaning headstones, the yew, the statue of Death with its scythe, mist on the ground. Voldemort rises out of the mist; EXPELLIARMUS! against AVADA KEDAVRA!, the red beam and the green lock, the bead of light sliding between them, the golden cage rising over both; the close-up inside the cage, PRIORI INCANTATEM, the shades of the dead coming out of the wand; Harry pushes the bead home, the link breaks and he runs for the cup — the Portkey — and he's gone | Voldemort | priori |

Playback (each time the panel shows): forced clips first, then every other clip in random order — no clip
repeats until all of them have played, then a new round starts. Clips are grouped up to 2 per
theme visit to keep transitions few.

## Forcing the first clip

Useful to test a new clip or to show one off. Value is a clip (`<theme>__<clip>`, e.g.
`fn__royale`), a whole theme (e.g. `ygo`), or a comma-separated list / JSON array of them,
played in order. After the forced clips, playback continues normally.

```bash
open -g build/NotchFight.app --args --first fn__royale     # one-off
open -g build/NotchFight.app --args --first pkm__psychic,snk__survey
NOTCH_FIGHT_FIRST=jjk ./build/NotchFight.app/Contents/MacOS/NotchFight
```

Or persistently (also applies to the Claude Code hook launches):

```bash
mkdir -p ~/.config/notch-fight && cp config.example.json ~/.config/notch-fight/config.json
```

Priority: `--first` arg > `NOTCH_FIGHT_FIRST` env > config file. An unknown name is logged
(with the list of valid names) and ignored. Clip names = folder names under `build/clips/`.

## The nf command

`install.sh` links `nf` into `~/.local/bin` (it leaves an existing `nf` that isn't ours alone), so it
works from any folder:

```bash
nf clips [...]              # which clips play: the checklist, list, enable, disable, mode (= ./clips.sh)
nf pause                    # a menu: 15 min, 30 min, 1 h, 4 h, 8 h, until resumed, or N minutes
nf pause 45m                # or straight away: 15m, 1h, 1h30m, 90 (minutes), forever
nf resume                   # show it again (right away if a Claude session is working)
nf status                   # paused?, quiet hours, screen sharing, clips, scale, hooks, sessions, app
nf preview odyssey          # play a clip or a whole theme in the notch now, then close (no focus change)
nf quiet 22:00-08:00        # never show it in that window (add `weekdays` for Monday to Friday; `off`)
nf share hide|show          # while sharing the screen: hide the panel (default) or keep showing it
nf delay 10s                # only show it once Claude has worked that long (quick answers stay quiet; `off`)
nf click next               # a click skips to the next clip, a double click closes it (`close`: the default)
nf menu on                  # a menu bar icon with all of the above (and "Choose clips…"); starts at login; `off`
nf resident on|off          # keep the app up, hidden, between prompts (the default; `on` adds login) or not
```

Whether the panel may show follows one set of rules, `nf gate` (`scripts/nf.py`). The resident app asks
when a session starts, every 5 s while anyone is working, and when `nf pause` / `resume` poke it
(`SIGUSR1`), so a pause, quiet hours or a screen share hides a panel that is already out, and it comes
back when they end if Claude is still working. Not resident, the hook asks before opening it. Sessions keep being tracked meanwhile. The pause lives
in `~/.config/notch-fight/paused`; quiet hours and `pauseOnShare` in `config.json`. The app and the menu
ask their own copy of those rules (`app/Gate.swift`, no Python every few seconds); `tests/test_app_gate.py`
keeps it answering exactly like `nf gate`.

The rotation outlives the app: `~/.config/notch-fight/state.json` keeps the clips already played this
round, so the next launch carries on with it instead of starting over, and no clip repeats until all have
played. It also counts plays per clip and the time the panel was up each day.

With a delay, the panel shows only once a session has been working that long: the resident app times it
from the date of the session's marker (written on each prompt); not resident, the hook hands the prompt
to a detached sleeper. `nf preview` plays in a second copy of the app; the resident one steps aside
while it runs (the preview leaves its PID in `~/.config/notch-fight/.preview` and pokes it). The menu bar icon is a
separate tiny app (`build/NotchFightMenu.app`, a LaunchAgent once on): a sparkle when the panel may
show, a pause sign when it is hidden, and every item just runs `nf`.

Screen sharing is detected by process: Zoom runs `CptHost` while sharing and macOS runs
`screencaptureui` while recording. A share from a browser tab (Meet, Teams on the web) looks like any
other tab from outside, so it isn't caught: list your own process names in `"shareProcesses"` in
`config.json`, or `nf pause` for the call.

## Choosing clips

```bash
./clips.sh                         # checklist (in a real terminal): space toggles, m mode, enter saves
./clips.sh list                    # on/off per clip
./clips.sh disable jjk-sukuna       # a clip (<theme>__<clip>) or a whole theme
./clips.sh enable sw__father
./clips.sh mode disabled           # what happens to NEW clips; the current selection is kept
```

Two modes, stored in `~/.config/notch-fight/config.json` (`install.sh` offers the checklist too):

| `newClips` | List | New clips |
|---|---|---|
| `"enabled"` (default) | `"disabled": [...]`: everything plays except these | play until you turn them off |
| `"disabled"` | `"enabled": [...]`: only these play | ignored until you turn them on |

- Clips forced with `first` (or `--first`) still play once at launch, even when turned off. The
  checklist shows them; `f` clears the list (`./build.sh` puts each new clip there).
- Enabling a theme in `"disabled"` mode enables the clips it has now, not ones added later.
- Some clips ship **off by default** (niche ones, see "Adding a clip"): they are listed as
  `(off by default)` and only play once you turn them on. In `"enabled"` mode those go in an
  `"enabled"` list next to `"disabled"`.
- With nothing selected the panel does not show at all. Changes apply the next time the panel shows.
- `NOTCH_FIGHT_CONFIG=/path/config.json` points the app and `clips.sh` at another config (tests and
  dev only: the app sees it when its binary is run directly, not through `open`).
- To check what would play without opening the panel:
  `build/NotchFight.app/Contents/MacOS/NotchFight --print-selection` (the active count, forced clips, and
  whether the panel would show).
- Tests: `python3 -m unittest discover tests` (the app tests need `./build.sh`). They use `--print-selection`,
  so no panel shows and the focused window keeps focus. `NOTCH_FIGHT_TEST_PANEL=1` adds real launches
  (in the background with `open -g`: the panel shows, focus stays) and `tests/test_resident.py`, which
  runs a resident copy against a temporary config folder and follows it through `NOTCH_FIGHT_TRACE`.

## Inside Claude Code (mod)

`mod/` is a Claude Code mod (a plugin of function hooks) that plays the same clips in the band
above the prompt while Claude works, at the right end, and hides them when the turn ends. It reads
`build/clips` and `build/transitions` from this checkout (run `./build.sh` first) and honours the
same `config.json` selection as the app. Terminal only: the desktop app's Code tab has no pixel
elements for mods.

```bash
claude --plugin-dir ~/Workspace/notch-fight/mod      # one session
```

To load it in every session, add the folder to `CLAUDE_CODE_PLUGIN_DIRS` in the `env` block of
`~/.claude/settings.json` (`{"env": {"CLAUDE_CODE_PLUGIN_DIRS": "~/Workspace/notch-fight/mod"}}`).
Options (`/config` → `notch-fight`):

| Option | Default | Effect |
|---|---|---|
| `enabled` | `true` | Off: the mod plays nothing (the band never shows); turn it back on from the same menu. |
| `display` | `image` | `image`: the real PNG frames. `raster`: coloured quadrant blocks (2x2 pixels a cell), any terminal. `sextant`: coloured sextant blocks (2x3 pixels a cell, 50% more detail than `raster`). `octant`: coloured octant blocks (2x4 pixels a cell, twice `raster`'s rows). |
| `rows` | `14` | Height in terminal rows (4 to 24); the width follows the clip (81 columns at 14, 93 at 16, 121 at 21). Native 185x64: `octant` at 16 rows, `sextant` at 21. |
| `repo` | the checkout `mod/` is in | Where `build/clips` lives. |

`image` needs a terminal that draws kitty graphics **Unicode placeholders** (`U=1`), which is what
Claude Code uses for a mod's `Image`: **kitty** and **Ghostty** do. Anywhere else the mod falls
back to `raster` by itself (a toast says so). **Orca** (any version so far, 1.4.218 included) only
gets the cell modes: its "Inline Images" setting (1.4.206+) uses xterm.js's image addon, whose kitty
support has no Unicode placeholders yet ([xterm.js#6198](https://github.com/xtermjs/xterm.js/pull/6198)
adds them).

Where `image` does not work, pick a cell mode, sharpest first:

1. **`octant`** (recommended), with **16 rows**: the clips at their native 185x64. It draws the
   Unicode 16 octants (U+1CD00–1CDE5), which kitty, Ghostty and WezTerm draw themselves; anywhere
   else (Orca, VS Code: xterm.js does not draw them yet) **the terminal font must have them**, or
   they show as boxes. **Cascadia Mono** 2404.23+ does: `brew install --cask font-cascadia-mono`,
   pick it as the terminal font (Orca: "Tipografía del terminal" → "Familia de fuentes"), and
   restart the terminal app after installing a font. An older Cascadia Code has no octants.
2. **`sextant`**: no font needed in kitty, Ghostty, WezTerm and xterm.js's WebGL renderer (Orca,
   VS Code), which draw U+1FB00–1FB3B themselves. 21 rows reach the native resolution.
3. **`raster`**: quadrant blocks, any terminal and any font.

The cell modes pack each clip once with `scripts/mod_cells.py` (about one second for `raster`, two
for `sextant`, five for `octant`) into `build/mod/`.

## Panel shape

The panel takes its size and position from the real notch of each Mac. Its looks can be tuned in
`~/.config/notch-fight/config.json` (defaults shown; `./build.sh` only rewrites `"first"`):

| Key | Default | Effect |
|---|---|---|
| `fillet` | `0` | Concave flare (pt) where the panel meets the notch. `8` gives the rounded "grows out of the notch" look; on some Macs it sticks out as a ledge. |
| `stretch` | `true` | Stretch the art to the notch width. `false` keeps square pixels, centred at 185pt (the black margins blend in). |
| `scale` | `1` | Make the panel bigger than the notch (e.g. `1.5`), keeping the art's proportions and staying centred under it. `install.sh` sets `1.5` when Vorssaint is installed (its bar is wider than the notch), unless you already chose a scale. |
| `widthTweak` | per model | Width correction (pt) when the panel overhangs by a hair. Built-in: `Mac14,2` → `-1`. |
| `entrance` | `"spring"` | How it comes out and goes back: `"spring"` drops and settles with a wobble; `"bounce"` falls and bounces off the bottom; `"crt"` drops dark and switches on like an old TV (a bright line that opens up), and off the same way. |
| `transitions` | `"mix"` | Between themes: a random style each time (`"mix"`), or always one of `"iris"`, `"dissolve"`, `"wipe"`, `"crt"`. A theme can have its own (the cinema's curtain). |
| `glow` | off | `"soft"` or `"strong"`: a halo of the clip's light hugs the panel (its sides and below it, ~16 pt), in the colour of the frame on screen. |

```json
{ "fillet": 8, "stretch": false, "entrance": "crt", "glow": "soft" }
```

Transitions are built per theme (`src/transitions.py`): the half that closes a theme and the half that
opens the next meet at black, so any two go together. Each theme has `transitions/<theme>__out` / `__in`
(the iris, also what the Claude Code mod plays) and `<theme>__out__<style>` for the other styles; a
theme module can set `TRANSITION = '<style>'` to have only its own. The glow's colours come from the
build too: `clips/<clip>/glow`, one `rrggbb` per frame: the hue from the scene's vivid pixels (not
Claude's own orange, which is in every clip), the brightness from how lit the scene is.

## Layout

```
src/
├── engine/            # shared by every theme
│   ├── core.py        # canvas constants, sprite drawing (auto outline + aura), sparks, orbs, easing
│   ├── palette.py     # one char per colour for sprite grids (themes add their own)
│   ├── claude.py      # Claude's base sprites + tools to dress him up / derive poses
│   ├── text.py        # 3x5 pixel font (accents, Ñ, ¡ ¿)
│   ├── fx.py          # effect registry (@fx('name')) + effects used by several themes
│   ├── logos.py       # pixel logos of other coding agents (Codex, OpenCode, Grok) + stick body
│   ├── people.py      # people from a body spec and a pose (figure, POSES), far-away copies, the speech bubble
│   ├── loop.py        # time that loops: the clip's length, wrapped frames, periods that divide it
│   ├── ambient.py     # rain, snow, ash, embers, fireflies, fog, torch, stars, flashes (they loop on their own)
│   ├── director.py    # text: how long it stays up, wrapping, the biggest that fits; a close-up template
│   └── render.py      # scene/actor model, backgrounds, render(), callout(), clip()
├── themes/            # one file per theme: sprites, its own effects, its clips, CLIPS = [...]
│   ├── dbz.py  ygo.py  kny.py  jjk.py  fn.py  pkm.py  snk.py  nrt.py  hxh.py  fma.py  mk.py  jojo.py  apex.py  cs.py  hl.py  rm.py  inv.py  phm.py  arg.py  odyssey.py  dnd.py  eternauta.py  cai.py  thebear.py  lol.py  thisisfine.py  wednesday.py  memento.py  skyrim.py  haikyuu.py  fightclub.py  arcane.py  basterds.py  basterds_cinema.py  hp.py  meshi.py  terraria.py  mist.py  deadpool.py  spidey.py  coraline.py
│   ├── sf.py  mario.py  mc.py  ds.py  sw.py  matrix.py  term.py  bb.py
│   ├── naruto_edo.py  naruto_zabuza.py  dbz_buu.py  dbz_jiren.py  jjk_sukuna.py  ghibli_totoro.py  snk_colosal.py  arg_86.py  naruto_shikamaru.py  mist_kelsier.py  xmen_nightcrawler.py  xmen_gambit.py  arg_mate.py  arg_colapinto.py  naruto_lee.py  lol_yasuo.py  jjk_toji.py  jjk_maki.py  arg_alejo.py  arg_alejo_flotar.py  arg_cordoba.py   # sub-themes
│   └── __init__.py    # auto-discovers every theme module
├── transitions.py     # transitions between themes: iris, dissolve, wipe, crt, and themes' own (curtain)
├── overlays.py        # drawn over any clip: the NEEDS YOU alert, the sessions badge (transparent frames)
├── build.py           # entry point used by build.sh
└── legacy/single_clip.py   # the original standalone 10 s clip (--black for the notch version)
app/main.swift, app/Info.plist   # the notch app
app/Gate.swift                   # may the panel show (pause, quiet hours, sharing): app + menu, like `nf gate`
app/State.swift                  # state.json: the rotation's round across launches, play counts, waits
app/Glow.swift                   # the light a clip spills below the panel (config "glow")
app/menu.swift                   # the menu bar icon (nf menu on)
mod/                             # the Claude Code mod (band above the prompt)
media/                           # rendered previews
```

## Build

```bash
./build.sh           # frames + app into build/
GIFS=1 ./build.sh    # also refresh media/clips/*.gif
ONLY=sonic GIFS=1 ./build.sh      # just one theme (or theme__clip, comma-separated) on top of the last build
JOBS=4 ./build.sh    # clips render in parallel, one per core by default (JOBS=1: one at a time)
```

Each clip (and transition) folder holds its frames packed into one image, `frames.png` (a 10-column
grid, row by row), and `count`; `scripts/frames.py` reads them back (the GIFs, the Claude Code mod, which
unpacks a clip into `build/mod/` for its image mode). The app is updated in place: just the packs that
changed are copied into it, and the Swift is recompiled only when `app/*.swift` changes. As a clip
starts, the app picks the next one and decodes its pack in the background, keeping only the last few in
memory.

Canvas is 185×64 art pixels = 185×64 pt on a 14" MacBook Pro (1 art px = 2 device px).

## Adding a clip

See `CLAUDE.md` for the rules (a new clip is auto-set to play first).

- **New clip in an existing theme:** add a `clip_<name>(f)` returning a scene to that theme's file
  and append `clip('<name>', <frames>, clip_<name>)` to its `CLIPS`. It must start and end on the
  theme's neutral pose.
- **New theme:** create `src/themes/<id>.py` with `from engine import *`, `THEME = '<id>'`,
  `register_bg(THEME, ...)`, its sprites/effects (`@fx('name')`) and `CLIPS`. Nothing else to
  touch: themes are auto-discovered and transitions to/from it are generated.
- **Off by default:** for a clip most people may not want (a football club, a brand), ship it off so
  users opt in: `DEFAULT_OFF = True` in the theme file turns off all its clips, and
  `clip('<name>', <frames>, clip_<name>, off=True)` (or `off=False` to override the theme) does it per clip.
  `build.py` marks them in the build (`build/clips/<clip>/.default-off`); the app and `./clips.sh` read it.
  `./build.sh` still puts a new clip first, so you see it while you make it.
- **Look at it while you make it:** `python3 scripts/sheet.py <theme> [clip] [frames]` renders a contact
  sheet straight from the code (no build), each frame numbered: `0,40,80`, `0-200/20`, or `end` (the
  last frames and frame 0, to check the loop closes). It goes to `build/sheets/`.
- **Text:** the 3x5 font has A-Z, 0-9, accents and Ñ (Á É Í Ó Ú Ü Ñ), ¡ ¿ and `! ? . , : ; ' " - + = / ( ) < > _ * # % &`;
  lower case draws as upper case. A test fails if a clip writes a character it lacks.
- **Things that keep moving** (rain, a torch, a swaying cloak) must be back where they started at frame
  N. The engine knows each clip's length: `loop.frame(f)` for anything random per frame, `loop.wave(f, p)`
  / `loop.phase(f, p)` / `loop.period(p)` for smooth motion (periods that divide the clip), `loop.rng(f)`.
  Ready-made ambient effects that already do: `rain`, `snow`, `ash`, `embers`, `fireflies`, `fog`,
  `torch`, `stars`, `flashes` (options in a dict: `s['under'].append(('rain', {'dens': 0.7}))`).
- **People:** `figure(spec, pose)` (`engine/people.py`) paints a person from a body spec (proportions,
  hair, clothes colours, boots, fists, and small painters for the rest: a tie, a number, glasses, a scar)
  and a pose (elbows, hands, lean, legs: stand, stance, lunge, reel, run, jump, kneel, crouch...). `POSES`
  has the common ones (guard, jab, hook, hurt, cheer, point, walk, run, jump, kneel, crouch);
  `figure_point()` finds a hand or the head on screen (to hang a sword, a bat, a wand on it). The six
  themes with posed people (haikyuu, fightclub, arcane, basterds, arg-cordoba, hp) are built this way.
- **Text, the easy way** (`engine/director.py`): `hold(txt)` is how many frames a line needs (0.5 s + 0.2 s
  a word, at least 1 s), `cue(f, start, txt)` whether it's up; `text_block(im, txt, box)` draws it as
  big as fits in a box, wrapped into even lines; the `caption` effect does the same; and
  `closeup(t, f, bg, draw, txt)` makes a close-up frame (background, your drawing, the text, zoom lines).
- **Check it:** `nf check <theme>` (or `python3 scripts/check.py <theme>`) renders the theme and lists
  what breaks the rules: loops, characters the font lacks, lines too short to read, text cut off by the
  edge. `tests/test_check.py` runs it on every theme and fails on any problem that isn't already in
  `tests/check_baseline.txt` (fix one, drop its line).
- **Snapshots:** `tests/snapshots.txt` keeps a hash of every clip; the tests say which clips changed. When
  a change is meant (a new clip, a better sprite), record it: `python3 tests/test_snapshots.py --update`.
