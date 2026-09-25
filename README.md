# Rusted Warfare Mods

## Mini Tank (Test Mod)
A tiny T1 tank — **buildable from the starter base (Command Center) and every builder**.

📥 **Download the mod:** [`MiniTank.rwmod`](MiniTank.rwmod) → then in-game: **Mods → Import → enable**

### How to install (mobile)
1. Download `MiniTank.rwmod` (tap the file above, then **View raw** / download button)
2. Open Rusted Warfare → **Mods** → **Import** → pick the downloaded file
3. Enable the mod, start a Skirmish
4. Select your **Command Center** → Mini Tank is slot 2 (or any builder → end of build menu)

### Source (edit me)
| File | What it is |
|---|---|
| `source/mod-info.txt` | Mod metadata (title/author/version) |
| `source/units/mini_tank/miniTank.ini` | Unit definition — stats, build links, turret, projectile |
| `source/units/mini_tank/miniTank.png` | Body sprite (2 frames, 16×20 each) |
| `source/units/mini_tank/miniTank_turret.png` | Turret sprite (10×20, points up) |
| `source/units/mini_tank/miniTank_dead.png` | Wreck sprite |
| `sprite_preview_6x.png` | Zoomed preview of the sprites |

### Modding quick notes
- `.rwmod` = plain ZIP of the mod folder (mod-info.txt must be at the zip root)
- Only `#` works as INI comments — `//` gets parsed as a key and spams errors
- Green pixels `(0,148,0)` on sprites become the player's team color
- `builtFrom_1_name: commandCenter` on a unit adds it to that building's production menu
- `builtFrom_N_forceNano: true` makes builders nano-construct units on the ground
