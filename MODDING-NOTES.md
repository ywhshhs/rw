# 📝 RUSTED WARFARE MODDING NOTES — everything learned making the Mini Tank
*If this repo ever breaks, this file recreates it from scratch. Last updated: Mini Tank v1.0.0*

---

## 1. WHAT A MOD IS (the 30-second version)

A mod = **a ZIP file named `whatever.rwmod`** containing:

```
MyMod.rwmod  (ZIP — mod-info.txt MUST be at the zip root)
├── mod-info.txt                      ← required metadata
├── units/                            ← one .ini + sprite PNGs per unit
│   └── my_unit/
│       ├── myUnit.ini
│       ├── myUnit.png                ← body sprite (frames side-by-side)
│       ├── myUnit_turret.png         ← optional turret sprite
│       └── myUnit_dead.png           ← optional wreck
├── maps/                             ← optional .tmx maps (Tiled, 20px tiles)
└── music/                            ← optional .ogg music
```

**Install:** Mods → Import (accepts `.rwmod`/`.zip`/`.tmx`) → enable → play.
**Manual:** drop the file in `/sdcard/rustedWarfare/units/` (Android).

---

## 2. mod-info.txt (copy-paste template)

```ini
[mod]
title: My Mod
description: What it does
author: ywhshhs
version: 1.0.0
tags: units
# optional: minVersion: 1.15p9   (game won't load mod on older versions)
# 1.16 extras: id:, requiredMods:, requiredModsMessage:, [music] section
```

---

## 3. INI RULES / GOTCHAS (burn these in)

| Rule | Detail |
|---|---|
| **Comments are `#` ONLY** | `//` gets parsed as a KEY and throws `key '[core]// blah' was not used` errors. The official reference only ever uses `#`. |
| mod-info.txt required | At the ZIP ROOT. Game errors: *"No 'mod-info.txt' file found in this directory"* |
| `name:` = internal ID | Other code references this. `displayText:` is the pretty label |
| `class: CustomUnitMetadata` | Required for custom units |
| frames are horizontal | `total_frames: N` → PNG is N frames side-by-side in ONE strip. Frame index starts at **0** |
| Body sprites face **UP** | Confirmed from vanilla artillery/tank sprites (barrel at top). Turrets also point up |
| Turret pivot = **image center** | Vanilla 10×40 turret: drum centered at image center, barrel up, empty padding below |
| Team color = green pixels | `(0,148,0)` (vanilla's exact green). `teamColoringMode: pureGreen` = green pixels → player color |
| Colors | `#RRGGBB` or `#AARRGGBB` |
| Max 30 turrets | per unit. `leg_N`/`arm_N` numbers only |
| `overrideAndReplace: vanillaName` | replaces a vanilla unit instead of adding new |
| `availableInDemo: true` | lets demo players use it |
| Keys are case-insensitive | `NONE` / `AUTO` are magic image values |
| Section inheritance | `[turret_2 : turret_1]` |
| `all-units.template` | file in mod root applied to ALL units (e.g. `strictLevel:1`, `autoTriggerCheckRate:every8Frames` for perf) |

**Build speed format:** `buildSpeed: 5s` (seconds) — old format was fraction-per-frame (`0.0020`), both work.

---

## 4. THE BUILD-LINK SYSTEM (how our tank is buildable)

Build menus are defined on the BUILDER side (`canBuild_N_name`) — but you can't edit vanilla units.
Solution: `builtFrom_*` **on the new unit's side** = "canBuild in reverse":

```ini
builtFrom_1_name: commandCenter      ← starter base PRODUCES it (like builders)
builtFrom_1_pos: 2                   ← slot in its menu

builtFrom_2_name: builder            ← any vanilla builder can make it...
builtFrom_2_pos: 15.1                ← end of menu (avoid clobbering vanilla slots)
builtFrom_2_forceNano: true          ← ...nano-constructed on the ground (designed
                                        for units: "Build as if this is a building")
```

- Comma lists work: `builtFrom_2_name: builder, builderShip, combatEngineer`
- Vanilla **internal names** (from game translations file): `commandCenter, builder, builderShip, combatEngineer, mechEngineer, fabricatorT1/T2/T3, landFactory, airFactory, seaFactory, mechFactory/T2, experimentalLandFactory, tank, heavyTank, extractor/T2/T3, turret/T2/T3, laserDefence, repairBay, outpostT1/T2, mammothTank, plasmaTank, laserTank, missileTank, tankDestroyer, heavyArtillery, heavyHoverTank, hoverTank, hovercraft, scout, helicopter, gunShip, lightGunship, bomber, interceptor, heavyInterceptor, amphibiousJet, attackSubmarine, heavySub, lightSub, nautilusSubmarine, battleShip, heavyBattleship, missileShip, heavyMissileShip, heavyAAShip, aaBeamGunship, airShip, missileAirship, gunBoat, dropship, experimentalCarrier/Dropship/Gunship/HoverTank/Spider, modularSpider (+_antiair/_artillery/_blink/etc), mechArtillery/mechBunker/mechFlame/mechGun/mechLaser/mechLightning/mechMinigun/mechMissile, fireBee, ladybug, spyDrone, fogRevealer, supplyDepot, AntiNukeLaucher, NukeLaucher, wall_v, spreadingFire, creditsCrates, crystalResource`
  (note the game's typos: `NukeLaucher`, `laserDefence`)

---

## 5. THE MINI TANK RECIPE (exact recipe, recreate anytime)

**Sprites** (PIL, vanilla palette lifted from `tank.png` in the APK):
| Color | RGB | Use |
|---|---|---|
| Track | (17,17,0) + link (40,40,10) | dark yellow-black, alternating rows for 2-frame animation |
| Hull | (69,74,84) / light (87,95,108) / dark (43,47,53) | bluish grays |
| Outline | (25,27,31) | 1px definition |
| **Team green** | (0,148,0) | hull patch + drum ring → becomes player color |

- `miniTank.png` = 32×20 (two 16×20 frames, tracks shift 1px between frames)
- `miniTank_turret.png` = 10×20 (barrel 2px wide × 10px, drum 6×7 centered at (4.5,10) = image center)
- `miniTank_dead.png` = 16×20 darkened silhouette + scorch speckle (no green)
- Shadow: don't draw one — `image_shadow: AUTO`

**miniTank.ini** (full, with the gotchas fixed):
```ini
[core]
name: miniTank
class: CustomUnitMetadata
price: 250
maxHp: 150
mass: 1500
techLevel: 1
buildSpeed: 5s
radius: 9
displayRadius: 10
isBio: false
availableInDemo: true
displayText: Mini Tank
displayDescription: -A tiny test tank\n-Built from the starter base and any builder

builtFrom_1_name: commandCenter
builtFrom_1_pos: 2
builtFrom_2_name: builder
builtFrom_2_pos: 15.1
builtFrom_2_forceNano: true
builtFrom_3_name: builderShip
builtFrom_3_pos: 15.1
builtFrom_3_forceNano: true
builtFrom_4_name: combatEngineer
builtFrom_4_pos: 15.1
builtFrom_4_forceNano: true
builtFrom_5_name: mechEngineer
builtFrom_5_pos: 15.1
builtFrom_5_forceNano: true
builtFrom_6_name: fabricatorT1
builtFrom_6_pos: 15.1
builtFrom_6_forceNano: true
builtFrom_7_name: fabricatorT2
builtFrom_7_pos: 15.1
builtFrom_7_forceNano: true
builtFrom_8_name: fabricatorT3
builtFrom_8_pos: 15.1
builtFrom_8_forceNano: true

[graphics]
total_frames: 2
image: miniTank.png
image_wreak: miniTank_dead.png
image_turret: miniTank_turret.png
image_shadow: AUTO
shadowOffsetX: 1
shadowOffsetY: 1
animation_idle_start: 0
animation_idle_end: 1
animation_idle_speed: 1
animation_moving_start: 0
animation_moving_end: 1
animation_moving_speed: 3
dustEffect: true
teamColoringMode: pureGreen

[attack]
canAttack: true
canAttackFlyingUnits: false
canAttackLandUnits: true
canAttackUnderwaterUnits: false
turretSize: 7
turretTurnSpeed: 5
maxAttackRange: 120
shootDelay: 60

[turret_1]
x: 0
y: 0
projectile: 1
turnSpeed: 5
turnSpeedAcceleration: 1.0
shoot_sound: tank_firing
shoot_sound_vol: 0.25
shoot_flame: small
shoot_light: #FFEECCCC
canShoot: true
recoilOffset: -2

[projectile_1]
directDamage: 20
life: 60
speed: 5
frame: 1
drawSize: 1

[movement]
movementType: LAND
moveSpeed: 1.2
moveAccelerationSpeed: 0.08
moveDecelerationSpeed: 0.2
maxTurnSpeed: 4.5
turnAcceleration: 0.25
moveSlidingMode: false
moveIgnoringBody: false

[ai]
useAsBuilder: false
```

**Package:** `zip -r MiniTank.rwmod mod-info.txt units` (from inside the mod folder).

---

## 6. BALANCE CHEAT SHEET (vanilla baselines)

| Unit | Price | HP | Dmg | Range | Speed | Role |
|---|---|---|---|---|---|---|
| Tank (T1) | 350 | 210 | 25 | 130 | 1.1 | bread & butter |
| Heavy Tank (T2) | ~1800 | ~1300 | ~60 | 145 | 0.7 | frontline |
| Mech Artillery (T2) | ~1200 | ~240 | ~64 AoE | ~330 | 0.6 | siege |
| Scout | 250 | 90 | none | — | 2.2 | recon |
| Turret T1 | 500 | 900 | 22 | 165 | — | defense |
| **Mini Tank (ours)** | **250** | **150** | **20** | **120** | **1.2** | cheap swarm/early raid — weaker than Tank 1v1 but faster + cheaper |

**Balance rules of thumb:** cost ∝ (HP × DPS × range × speed); artillery should die to any 2 units that reach it; builders/support units = unarmed or very weak; T2 = ~3-5× T1 cost for ~3× power.

**Built-in sounds** (use anywhere): `attack, move, click, missile_fire, missile_hit, unit_explode, building_explode, tank_firing, cannon_firing, gun_fire, lighting_burst, plasma_fire, plasma_fire2, firing3, firing4, large_gun_fire1/2, bug_die, bug_attack, interface_error, nuke_explode, nuke_launch, laser_deflect, laser_deflect2, message` — or put custom `.ogg/.wav` in the mod and use the filename.

**Logic system (1.15+):** `autoTrigger: if self.hp(lessThan=50)`, `and/or/not`, `==, !=, >, <`, arithmetic `+ - * / %`, `${}` dynamic text: `text: HP %{self.hp}`. Functions: `rnd()`, `distance()`, `min/max`, `sin/cos`, `int()`, `str()`, `select()`, `debug()` etc. 1.16 adds `otherwiseTriggerAction` (else), `vec2/vec3`, `abs`, `coalesce`, dynamic damage.

---

## 7. TOOLBOX & REFERENCES

| Resource | Where |
|---|---|
| Official Unit Modding Reference (1.16, Q3 2026) | in the local workspace: `Rusted_Warfare_Unit_Modding_Reference_Q3_2026.pdf` + extracted `.txt` (48pp, every key version-stamped) |
| Full research guide | local workspace: `rusted-warfare-modding-research.md` |
| This repo's mod source | `source/` |
| Mobile editors | Rust Assistant (Cold-Mint, Android), RW Mod Editor (CLRedfield, Android+Win — ships a dual-faction example mod) |
| Maps on mobile | NotTiled (Tiled-compatible, 20px tiles, Base64 gzip layer format) |
| Official refs | corrodinggames.com/rusted_warfare → "Modding reference" Google Sheets |
| Community | discord.gg/rustedwarfare, r/rustedwarfare, Steam Workshop (browse top mods' INIs = best learning) |
| Game's own example | `assets/builtin_mods/mega_builders/` inside the APK/game folder |

**Debug flow when a unit breaks:** in-game error text names the bad key → check section placement → check `#` comments → check required fields (name/maxHp/price/mass/radius + image + canAttack×4 + movementType) → delete + re-import mod (cache!) → restart match.

---

## 8. REPAIR DRONE (mod #2 — recipe + what it teaches)

Design goals from the user: **NOT buildable from starter base**, **T1 army factory only**, **50 HP shield**.

Key differences vs Mini Tank:
- `builtFrom_1_name: landFactory` ONLY (no commandCenter entry → not from starter base; no other builders)
- Shield: `maxShield: 50` + `shieldRegen: 0.15` (per-frame; ~5.5s to refill 50 from 0 at 9/sec... 0.15×60fps=9/s)
- Repair: `canRepairUnits: true` + `nanoRepairSpeed: 0.25` (vanilla default 0.2) + `nanoRange: 70` (default 85)
- **NO [attack] section at all** = truly unarmed, no attack cursor
- `movementType: HOVER` + `targetHeight: 1.5` + `targetHeightDrift: 0.8` + `moveSlidingMode: true` = hovering bob, crosses land+water
- `canRepairBuildings` NOT set (would need `isBuilder: true` for buildings — drone repairs units only, balanced)
- Sprite: 12×12 rounded dome, blinking green team light (2 frames), 4 thruster pads
- AI: `useAsBuilder: false` so AI doesn't treat it as a builder

---

## 9. BALANCE PATCH: Mini Tank v1.1.0 (the first nerf!)

**Playtest data:** ~5k credits of mini tanks overwhelmed 3 artillery + 4 scouts.
**Root cause identified:** the stats were fine-ish (weaker than vanilla tank 1v1) — the problem was **AVAILABILITY**: `builtFrom: commandCenter` meant infinite early spam without investing in a factory.

**Changes:**
| Stat | v1.0 | v1.1 |
|---|---|---|
| Built from | commandCenter + ALL builders + fabricators | **landFactory only** |
| maxHp | 150 | **130** |
| directDamage | 20 | **15** |
| price | 250 | 250 (kept) |

**LESSON (balance design):** *availability is a balancing lever, often stronger than stats.* A unit that's slightly weak per-unit but free from the start will always warp games. Gate anything spammable behind a production building. Same reason the Repair Drone was designed T1-factory-only from day one.

**Nerf checklist for OP units:** 1) restrict builtFrom to the "correct" factory, 2) cut damage (slows kills → enemy gets value), 3) cut HP (dies to counter-attack), 4) raise price LAST (feels bad, changes AI evaluation of every unit).

---

## 10. PATHING PATCH: Mini Tank v1.2.0 ("why is it humping the crystal?")

**User bug report:** mini tanks keep running into resource spots and trees, getting stuck ~1s.

**ROOT CAUSE (neat fact):** trees and resource crystals are **neutral UNITS in RW** (see vanilla name list: `tree`, `crystalResource`), not map tiles. With `softCollisionOnAll: 0` (vanilla tank default) the mini tank hard-collides with them and grinds to a stop against their collision radius.

**Fix applied:**
| Key | Before | After | Why |
|---|---|---|---|
| `softCollisionOnAll` | 0 (absent) | **5** | soft collision = slide around neutral units/obstacles instead of dead-stop (helicopters use 18 to push through swarms) |
| `maxTurnSpeed` | 4.5 | **6** | tighter cornering around blocked tiles |
| `turnAcceleration` | 0.25 | **0.4** | faster direction recovery when bumped |
| `moveAccelerationSpeed` | 0.08 | **0.1** | quicker get-away after a stop |

**LESSON:** in RW, "obstacles" are mostly other units (neutral trees/crystals count). Any unit that feels "sticky" needs softCollisionOnAll + turn tuning. Big soft values = swarm overlap (use 15+ for ant-like units), small (3-6) = just slide assistance.

---

## 11. PACKAGING LESSON: ship multi-unit mods as ONE .rwmod

Installing N separate .rwmods is tedious (N imports + N toggles). A single mod can hold unlimited units — just add more folders under `units/`:

```
TinyArmy.rwmod
├── mod-info.txt          (one metadata file for the whole pack)
└── units/
    ├── mini_tank/        (miniTank.ini + PNGs)
    └── repair_drone/     (repairDrone.ini + PNGs)
```

Repo now ships `TinyArmy.rwmod` (Mini Tank v1.2 + Repair Drone) as the single install; individual mods were removed to avoid version drift.

---

## 12. GOTCHA #1 STRIKE: `[attack]` is REQUIRED — even for unarmed units

**Bug:** repair drone errored in-game: *"could not find canAttack in configuration file in section: attack"*.
**Cause:** I omitted the whole `[attack]` section thinking "no section = no weapon". Wrong — the official reference START table lists `[attack] canAttack/canAttackFlyingUnits/canAttackLandUnits/canAttackUnderwaterUnits` as REQUIRED CODE for EVERY unit.
**Fix:** every unit gets the section; disarming is a VALUE choice:
```ini
[attack]
canAttack: false
canAttackFlyingUnits: false
canAttackLandUnits: false
canAttackUnderwaterUnits: false
```
**Rule:** required fields can have their values changed but never be omitted. `false` disarms; missing section = load error.

---

## 13. THE CACHING TRAP (learned the hard way — 3 identical downloads)

**User-confirmed behavior:** if the newly downloaded `.rwmod` has the SAME NAME as one already installed, the game (and/or the browser downloading it) keeps the **cached old copy** — your fix never actually loads, and the error repeats no matter how many times you re-download.

**Why it happens (two caches stack):**
1. **Browser cache** — same URL/filename → same stale bytes on Android download
2. **Game mod identity** — the mod's file/folder name in `rustedWarfare/units/` is its identity; a re-import with the same name doesn't cleanly replace the old broken copy

**The fix ritual (when pushing an update for a mod that errors):**
1. Fix the INI → rebuild
2. **Rename the file** (`TinyArmy.rwmod` → `TinyArmy_v2.rwmod`) and bump `version:` (and optionally show it in `title:` so you can SEE which copy the Mods list has)
3. Delete ALL old mod entries in the in-game Mods menu (old packs, old single-unit mods — any that contain the same units)
4. Import the fresh file, enable, start a NEW match (mods load at match start, not in the menu)

**Rule of thumb:** *changing the file is not enough if the name is the same — rename to bust every cache layer.*

---

## 14. SPRITE LESSON: support units need MORE detail, not less

Mini tank = perfect with minimal detail (vehicles read well from simple shapes). Support/tech units (repair drone) look "plain" without mechanical storytelling. Drone v2 detail checklist:
- **Quad-rotor layout**: 4 corner pods + translucent diagonal rotor blades (alpha ~170) alternating A/B per frame = spin animation
- **Color storytelling**: orange welding tip at the rear (universal "repair tool" color, doesn't clash with team green), tip heats brighter on frame 2 (welding sparkle)
- **Hull detail**: top-left light source highlight + bottom-right shade, vent grilles, panel lines
- Team light still center (blinking 2×2 → reads as "heart")
- Wreck: missing one rotor pod + cracked hull + scorch = instantly readable as "this drone died"
- Green px count is small (8) on purpose: only the core light is team colored

---

## 15. BUG ZAPPER (mod #3 — T2 AA, user-specced)

**Design by committee (user tuned my spec):** speed 1.3→**0.9** (cheap+fast AA would ruin early air — mass-producible chasers are broken), 125 HP, 50 shield, **3 rockets × 25 dmg every 0.75s** air-only.

**New mechanics introduced:**
- `shootDelay: 0.75s` — accepts SECONDS directly (or frames: `45`)
- **3 rockets at once**: center `[projectile_1]` uses `spawnProjectileOnCreate: flakRocket(offsetX=-6, recursionLimit=0), flakRocket(offsetX=6, recursionLimit=0)` — spawns 2 named child projectiles at launch. Children need their own `[projectile_flakRocket]` section with same `directDamage: 25`. `recursionLimit: 0` stops chain-spawning.
- **Air-only**: `[attack] canAttack: true + canAttackFlyingUnits: true + canAttackLandUnits/UnderwaterUnits: false`
- Sprite storytelling: 3 visible rocket tubes in the turret image = telegraphs the 3-rocket volley; radar dish sweep animated via BODY frames (frame 0 dish-left, frame 1 dish-right) since turret-frame animation keys weren't confirmed — body frames are the reliable animation channel.
- Pack structure: just add another folder `units/bug_zapper/` — same mod, zero extra install cost.

---

## 16. MINI AA (final name) + SPRITE QoD UPGRADE

- Renamed bugZapper → **miniAA** (internal name, display text, files, folder) — always rename ALL layers: `name:` (what other units/logic reference), `displayText:` (UI), file names, folder name. Renaming after packaging = rebuild zip.
- Sprite detail upgrade technique: **mirror-drawing** (draw left half, mirror to right) keeps tanks symmetric while doubling detail cheaply. More tones = smoother read: added HULL_L2/HULL_D2 for 5-tone shading.
- Detail added: 4px tracks with dark edge guides, 3-tone sloped glacis, side panel seams, rear engine grilles (slats), exhaust pipes, 4px radar dish with sweep + mesh ring, pod bolts, tube rims + dark bores, gradient rocket tips, hatch hinge, side armor skirts.
- **Wreck storytelling**: miniAA_dead has EMPTY tubes (rockets spent at death) vs loaded rockets in alive sprite. Missing/team-colored pixels = 0 on wreck.
- **Packaging gotcha (almost shipped it): preview PNGs must NOT be inside units/ folders** — anything in the zip loads as mod content; keep previews at pack root or outside.

---

## 17. GOTCHA: the spawn-keys are PLURAL — `spawnProjectilesOnCreate`

**Error:** `key '[projectile_]spawnProjectileOnCreate' was not used` — the SINGULAR form is not a real key (the spreadsheet's truncated example columns spell it singular in places; the full example block is the truth):
```
[projectile_main]
spawnProjectilesOnExplode: shrapnel(offsetDir=90), shrapnel(offsetDir=-90)
[projectile_shrapnel]
turnSpeed: 0
spawnProjectilesOnEndOfLife: secondary*3(spawnChance=0.5)
```
**Real keys (plural Projectiles):** `spawnProjectilesOnCreate` (on launch), `spawnProjectilesOnExplode` (on impact), `spawnProjectilesOnEndOfLife` (when expiring — shrapnel/cluster munitions).
**Also learned:** named projectile sections `[projectile_flakRocket]` ARE valid (alongside indexed `[projectile_1]`); the game error prefixes the section FAMILY as `[projectile_]keyName` which looks confusing but just means "unknown key in a projectile section".

---

## 18. MULTI-ROCKET VOLLEYS: slaved turrets, not projectile spawning

**Bug:** spawnProjectilesOnCreate volley only showed 1 rocket, and it looked like a bullet (built-in `frame: 4`).
**Fix — the vanilla missileTank pattern (from the APK's own INI):**
1. **3 simultaneous rockets** = slaved invisible turrets, NOT projectile spawning:
```ini
[turret_1]   # master: aims the target, canShoot: false (never fires)
canShoot: false
shouldResetTurret: false
[turret_2]   # left pod: slaved to master aim, fires every volley
attachedTo: 1
slave: true
invisible: true
warmup: 2
projectile: 1
shoot_sound: missile_fire
[turret_3]   # right pod: copy turret_2, mirror x
copyFrom: 2
x: 5         # (overrides the copied -5)
```
2. **Rocket look** = custom projectile image + trail:
- `[projectile_1] image: rocket.png` ("Overrides drawType and frame") — draw the rocket pointing UP, game rotates it to travel direction
- `trailEffect: true` — smoke trail (this is what makes vanilla missiles read as missiles!)
- `speed: 1.5` + `targetSpeed: 7` — slow launch then accelerate = launch-ramp feel
- `frame: 4` was the vanilla missile tank's built-in frame, but custom image + trail is the reliable way to get rocket reads
3. Stagger trick from vanilla: `linkDelayWithTurret: 2` + different `warmup:` = sequential double-tap (vanilla missile tank fires 2 missiles 15 ticks apart). warmup equal = simultaneous volley.

---

## 19. MID + ENDGAME: Mini Mortar (T2) & Mini Mammoth (T3)

**Mini Mortar — 900cr T2 siege:** `ballistic: true` + `ballistic_height: 30` = lobbed arc shell, `areaDamage: 30 / areaRadius: 30` splash + small direct hit, 280 range, 2s reload, 160 HP, 0.7 speed. Sprite: fat mortar tube with dark bore + visible shell, rear baseplate. Balance anchor: vanilla artillery (1100cr/240hp/64dmg/330range) — mini mortar is weaker but cheaper and faster.

**Mini Mammoth — 3800cr T3 breacher:** `armour: 8` + `armourMinDamageToKeep: 5` (flat damage reduction; anti-MG armor), twin cannons 110dmg/190range/2.5s, **per-turret attack permissions**: MG pods ([turret_2]/[turret_3], slaved) have their OWN `canAttackFlyingUnits: true` + `delay: 0.2s` — main guns stay anti-ground while MGs buzz air. 1400 HP, 0.55 speed, 12k mass. Balance anchor: vanilla mammothTank (~4500cr, 2100hp, 180dmg) — mini mammoth strictly weaker 1v1 but MGs add anti-air utility.

**New mechanics used:**
- `ballistic: true` + `ballistic_height:` — lobbed arc projectiles (mortars/howitzers)
- `areaDamage` + `areaRadius` — splash (note: small directDamage ON TOP of splash)
- `armour` + `armourMinDamageToKeep` — flat damage reduction with a floor so it never goes immune
- **Per-turret canAttack overrides** — each [turret_N] can have its OWN attack permissions and `delay:` (independent fire cycle!) — this is how hybrid units work
- `shoot_flame: big` for heavy guns; `copyFrom` in turret sections works for MG pods too

---

## 20. 2.5D SPRITES + ARTILLERY SILHOUETTE (mortar redesign)

**Feedback:** mortar looked like the mammoth with fewer barrels; sprites felt flat.

**2.5D depth technique (the extrusion pass):** draw the unit's top-surface silhouette, then draw the SAME silhouette offset down-right (+3,+4) in a dark side-wall color, then the top surface on top. Result: the sprite looks like a slab with visible side walls = instant depth. Light source = top-left. Sides get outlined where the wall meets background. Worked as a reusable `extrude(im, silhouette, top_detail_fn, side_color, dx, dy)` helper applied to ALL ground units (mini tank 2px, AA 3px, mortar 4px, mammoth 5px = bigger unit, deeper walls).

**Artillery silhouette language (why the mortar no longer looks like a tank):**
- **Open carriage** — cross-members instead of full hull deck (you can almost see the ground between the beams)
- **Barrel overhangs the rear** (extends past the body — guns poke out both ends in top-down artillery)
- **Olive-drab palette** ((96,98,66) family) vs the blue-gray tank family — color codes the role
- Ammo crates on the rear plate, visible shell in the bore, wheeled beams instead of full tracks
- Turret = just the tube assembly with a loaded-shell pixel
- Mammoth got a **dozer blade** (wider front plate) to break the rectangle + 5px walls

---

## 21. GOTCHA: shoot_flame values — "big" doesn't exist

**Error:** `failed to find built-in or custom effect with the name: big`
**Valid built-in flames** (from vanilla unit INIs): `small`, `medium`, `large`, `shockwave`, `smoke`, `NONE` — plus `CUSTOM:<effectSectionName>` (and comma lists: `shockwave, smoke`).
**Also learned:** `shoot_flame` accepts multiple effects — `shoot_flame: large, CUSTOM:lightSlowFade` = muzzle flash + lingering light fade (nice for heavy cannons). Check vanilla usage (`grep shoot_flame assets/units/`) before inventing values.

---

## 22. GOTCHA: CUSTOM: effects are per-mod namespaces

**Error:** `failed to find custom effect with the name: lightSlowFade` — even though vanilla units use `shoot_flame: CUSTOM:lightSlowFade`, vanilla defines that effect in ITS OWN files. `CUSTOM:` only resolves effect sections **within your mod**.
**Fix:** copy the effect section into your unit INI and ship any images it needs:
```ini
shoot_flame: large, CUSTOM:lightSlowFade

[effect_lightSlowFade]
image: light_50.png        # copied from assets/units/shared/ into the mod
life: 40
fadeOut: true
attachedToUnit: true
color: #ffddaa             # vanilla uses cyan #63e6e8; warm tint matches cannons
scaleFrom: 0.7
scaleTo: 0.7
alpha: 0.5
drawUnderUnits: true
```
**Lesson:** every `[effect_NAME]` you reference with CUSTOM: must exist in your own files. Vanilla unit INIs each re-define their effects — that's the intended pattern, not duplication.

---

## 23. GOTCHA: copyFrom is FILE-level, not turret-level

**Error:** `could not find: y in configuration file under [turret_3]` — I copied the vanilla missileTank's `copyFrom: 2` shortcut, giving turret_3 only `x: 8` and assuming the rest (y, projectile, permissions) would be inherited. They weren't.
**The reference says it plainly:** `copyFrom: file(s) (ini)` — it pulls from FILES (e.g. `copyFrom: ROOT:defaultTanks.template, tankT1.ini`), not from sibling sections. Vanilla's turret_3 uses `copyFrom: 2` but ALSO re-declares its fields — don't trust that pattern.
**Safe fixes (either):**
1. Write the section out explicitly (what we did — verbose but bulletproof)
2. Documented section-to-section inheritance via the header: `[turret_3 : turret_2]` + only the overrides (e.g. `x: 8`)
**Rule:** shared logic between turrets = header inheritance or explicit fields; `copyFrom:` = files only.

---

## 24. GOTCHA: per-turret range is `limitingRange`, not maxAttackRange

**Error:** `key '[turret_2]maxAttackRange' was not used` — turret sections do NOT take maxAttackRange (that's [attack]-only, the unit-wide range).
**The right key:** `limitingRange: 140` — *"Make this turret have less range than the maxAttackRange. Do not apply this to all turrets, change maxAttackRange instead."* (1.13+). MGs = main gun range 190, capped to 140 via limitingRange.
**Related per-turret keys worth knowing:** `canAttackMaxAngle: 181` (fire without turning - missiles), `limitingAngle: 60` (fire arc sides), `clearTurretTargetAfterFiring` (multi-targeting).

---

## 25. AEA TECHNIQUE IMPORT (referencing the high-quality mod)

From studying AEA 1.4.8 (also in this repo) + vanilla missileTank:
1. **`idleSpin: 2`** — turrets can spin continuously. The Mini AA's radar dish is now a SEPARATE turret sprite ([turret_4], image: radarDish.png, canShoot: false, idleSpin: 2) = real spinning radar instead of a 2-frame fake sweep. Turret sections take their own `image:` ("overrides unit's main turret image").
2. **CUSTOM muzzle light-fade on every shooter** — shoot_flame: small, CUSTOM:lightSlowFade (effect defined per-file, images shipped in each unit folder).
3. **movementEffect: CUSTOM:trackDust / bigDust** — AEA's movementEffect pattern (their helis: CUSTOM:EkRotorwash) applied as track dust; richer than dustEffect: true (per-unit scale/color/offset).
4. **AEA sprite layering style** (for future units): multi-part sprites via [attachment_NAME] (attackjet: wings.png attachments) and [arm_N]/[leg_N] with image_end: (buzzard rotor blades). Moveable parts = separate images, not baked into the body.

---

## 26. GOTCHA: softCollisionOnAll is a [core] key, not [movement]

**Error:** `key '[movement]softCollisionOnAll' was not used` — I'd put it under [movement] (it FEELS like a movement property). It's a [core] section key ("creates a soft collision effect when touching other units"). Fixed in all 6 AE units (value preserved, moved after displayRadius).
**Meta-lesson:** when a "key was not used" error appears, first suspect SECTION placement — the key may be valid but belong elsewhere. [core] holds body/collision/economy keys; [movement] holds only movement keys.

---

## 27. CENTERED 2.5D + Beaver build fix (AE v0.3.0)

**Centered extrusion (fixes "walls peak out"):** the old pass drew top surface at 0,0 and walls at +dx,+dy — so the BODY sat up-left of image center and walls hung out bottom-right (game centers the IMAGE on the unit, not the body). Fix: canvas grows to W+2dx/H+2dy, top surface drawn at (dx,dy), walls at (2dx,2dy) → whole shape symmetric around canvas center = unit position. The reusable kit is `ae_sprites.py` (parametric, relative coords — regenerate any unit at any size; batch regenerate all units with one run).

**Size floor:** all AE units now ≥16px min dimension (Hornet 20×24, turret 16×20; Grasshopper 22×22 canvas; Boar 26×31).

**Beaver couldn't build** ("drives to spot, does nothing"): flat `canBuild_1_name:` keys + missing `nanoBuildSpeed`. Working builder pattern (from combat_engineer.ini): **section-form** `[canBuild_1] name: turret / pos: 1` + `nanoBuildSpeed: 2` + `[ai] useAsBuilder: true`. flat canBuild_*_name = display only.

---

## 28. AE MEGA-BUILD (v0.4.0): 46 new units, 5 tiers, Experimental Factory

**Architecture that made it possible:** spec-driven generation — `ae_specs.py` (46-unit table) + `ae_sprites.py` (parametric chassis/turret kit) + `ae_generate.py` (INI emitter). One table row = full unit (INI + sprites + wrecks). New unit = one spec line. QA sweep script: required fields, [attack]x4, // comments, image existence, projectile section refs — 0 errors across 50+ INIs.

**New mechanics verified + used:**
- **Nuke weapon** (from vanilla nuke_launcher.ini): tags: nuke (interceptable), nukeWeapon: true, areaDamage/areaRadius/areaExpandTime: 75 (expanding wave), ballistic_height: 110, targetGround, shouldRevealFog. Ammo pattern: [action] with price + addResources: ammo=1 + ai_isDisabled.
- **EMP**: hullDamageMultiplier: 0 + shieldDamage (vanilla comment in nuke INI confirms the EMP variant pattern).
- **Lightning weapon**: instant: true + lightingEffect: true + chargeEffectImage + shoot_flame: CUSTOM:sparks2*3.
- **Blink teleport** (vanilla blink.ini): [action] fireTurretXAtGround: dummyBlink + fireTurretXAtGround_withProjectile + [turret_dummyBlink] canShoot:false + [projectile_dummyBlink] teleportSource: true, instant: true, life: 99999. whenBuilding_cannotMove: true, addActionCooldownTime.
- **Melee/suicide**: isMeMine... isMelee: true in [attack] (AEA Nuclear Drone pattern) — mines as melee attackers.
- **Transports**: maxTransportingUnits, transportUnitsRequireMovementType.
- **Mobile factory**: [canBuild_N] sections with forceNano: true building UNITS (combat_engineer pattern: it builds heavyTanks with forceNano).
- **Cluster munitions**: spawnProjectilesOnEndOfLife: shrap*6(offsetRandomXY=25).
- **Anti-nuke interception**: interceptProjectiles_withTags: nuke (antiNuke silo pattern).
- **Codename system**: R/A/S/H/D series for T2/T3, E4-xx T4, X5-xx T5; techLevel capped at 3 in INI (min(3,tier)) since GUI only shows 3 colors; tiers 4/5 = price/factory gating.
