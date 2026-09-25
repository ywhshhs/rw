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
