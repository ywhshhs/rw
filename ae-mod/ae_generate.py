"""AE unit generator v2 — spec table -> full INIs + sprites. No fragile f-strings."""
import os, re
from ae_sprites import generate_body, generate_turret
from PIL import Image

WP_KEYS = ("gun","mortar","missiles_air","missiles_both","beam","flame")

def weapon_range_cycle(wp):
    for k in ("gun","mortar","missiles_air","missiles_both","beam","flame"):
        if k in wp and isinstance(wp[k], tuple) and len(wp[k]) >= 3:
            w = wp[k]
            return w[2], (w[3] if len(w) > 3 else 1.0)
    return 0, 1.0

def make_wreck(body, path):
    wreck_img = Image.new('RGBA', (body.width, body.height), (0,0,0,0))
    bb = body.load()
    for yy in range(body.height):
        for xx in range(body.width):
            p = bb[xx,yy]
            if p[3] > 0:
                wreck_img.putpixel((xx,yy), (30,33,38,255) if (xx+yy)%4 else (12,12,12,255))
    wreck_img.save(path)

def unit_id(name):
    import re as _re
    uid = _re.sub(r'[^A-Za-z0-9]+','_', name).strip('_')
    if name.startswith(("R2","A2","S2","H2","D2","H3","D3","S3","R3","E4","X5")):
        return "ae_" + uid
    return "ae" + uid[0].upper() + uid[1:] if not uid.startswith("ae") else uid

def gen_one(sp, base="units"):
    name = sp["name"]
    uid = unit_id(name)
    folder = os.path.join(base, uid.lower())
    os.makedirs(folder, exist_ok=True)

    # ---- sprites ----
    w = max(16, sp["radius"]*2+2)
    h = max(18, sp["radius"]*2+6)
    if sp["chassis"] in ("heavy_tracked","crawler","titan","nuke_silo"):
        h = max(24, sp["radius"]*2+8)
    body = generate_body(sp["chassis"], w, h, sp["accent"])
    body.save(os.path.join(folder, uid + ".png"))
    make_wreck(body, os.path.join(folder, uid + "_dead.png"))

    wp = sp["weapons"]
    turret_kind = None
    for k in ("gun","mortar","missiles_air","missiles_both","beam","flame"):
        if k in wp: turret_kind = {"missiles_air":"missiles","missiles_both":"missiles"}.get(k,k); break
    has_turret = turret_kind and sp["chassis"] not in ("medic","shield_anchor")
    if has_turret:
        t = generate_turret(turret_kind, sp["accent"], w=12+sp["radius"]//2, h=20)
        t.save(os.path.join(folder, uid + "_turret.png"))
    # rocket sprite for missile units (copy from mini aa pack or draw fresh)
    if any("missile" in k for k in wp):
        from ae_sprites import px as _px
        r = Image.new('RGBA',(5,13),(0,0,0,0))
        HULL_L=(87,95,108,255); HULL_D=(43,47,53,255); OUTLINE=(25,27,31,255); GREEN=(0,148,0,255)
        RED=(200,60,40,255); RED_L=(255,130,70,255)
        r.putpixel((2,0),RED_L); r.putpixel((1,1),RED); r.putpixel((2,1),RED_L); r.putpixel((3,1),RED)
        for y in range(2,9):
            r.putpixel((1,y),HULL_L); r.putpixel((2,y),HULL_L); r.putpixel((3,y),HULL_D)
        for y in (5,6): r.putpixel((2,y),GREEN)
        r.putpixel((1,9),HULL_D); r.putpixel((3,9),HULL_D); r.putpixel((0,10),OUTLINE); r.putpixel((4,10),OUTLINE)
        for x in (1,2,3): r.putpixel((x,10),HULL_D); r.putpixel((x,11),HULL_D)
        r.save(os.path.join(folder, "rocket.png"))

    # ---- INI ----
    rng, cyc = weapon_range_cycle(wp)
    if "melee" in wp: rng = wp["melee"][1]; cyc = 0.5
    mass = int(sp["hp"]*12 + sp["cost"])
    pos_map = {2:"15.%d", 3:"16.%d", 4:"17.%d", 5:"18.%d"}
    pos = pos_map[sp["tier"]] % ((int(sp["cost"])%9)+1)
    L = []
    A = L.append
    A(f"# {name} - AE {sp['role']}")
    A("[core]")
    A(f"name: {uid}")
    A("class: CustomUnitMetadata")
    A(f"price: {sp['cost']}")
    A(f"maxHp: {sp['hp']}")
    A(f"mass: {mass}")
    A(f"techLevel: {min(3, sp['tier'])}")
    A(f"buildSpeed: {max(2, int(sp['cost']**0.5/8))}s")
    A(f"radius: {sp['radius']}")
    A(f"displayRadius: {sp['radius']}")
    A("isBio: false")
    A("availableInDemo: true")
    if sp["shield"]:
        A(f"maxShield: {sp['shield']}"); A("shieldRegen: 0.15")
    if sp["armour"]:
        A(f"armour: {sp['armour']}"); A(f"armourMinDamageToKeep: {max(2,sp['armour']//2)}")
    if "regen" in sp["extra"]: A("selfRegenRate: 0.08")
    m = re.search(r'sight (\d+)', sp["extra"])
    if m: A(f"fogOfWarSightRange: {m.group(1)}")
    m = re.search(r'maxTransportingUnits (\d+)', sp["extra"])
    if m:
        A(f"maxTransportingUnits: {m.group(1)}")
        A("transportUnitsRequireMovementType: LAND" + (", WATER" if "amphibious" in sp["role"] else ""))
    if "repairs allies" in sp["extra"] or sp["role"]=="tracked healer" or "repair" in sp["role"]:
        A("canRepairUnits: true"); A("nanoRepairSpeed: 0.3"); A("nanoRange: 85")
    if "builds Hornet" in sp["extra"]:
        A("isBuilder: true"); A("nanoBuildSpeed: 2")
    if "reclaim" in sp["extra"]:
        A("nanoUnbuildSpeed: 1.5"); A("nanoRange: 75")
    A(f"displayText: {name}")
    desc = "-" + sp["role"].replace(", ", "\\n-")
    A(f"displayDescription: {desc}")
    A("")
    if sp["factory"] != "NONE":
        A(f"builtFrom_1_name: {sp['factory']}")
        A(f"builtFrom_1_pos: {pos}")
    A("")
    if "reclaim" in sp["extra"]:
        A("[canBuild_1]"); A("name: reclaim"); A("pos: -1"); A("")
    if "builds Hornet" in sp["extra"]:
        A("[canBuild_1]"); A("name: aeHornet"); A("pos: 1"); A("forceNano: true"); A("")
        A("[canBuild_2]"); A("name: aeThorn"); A("pos: 2"); A("forceNano: true"); A("")

    A("[graphics]")
    A("total_frames: 1")
    A(f"image: {uid}.png")
    A(f"image_wreak: {uid}_dead.png")
    A(f"image_turret: {uid + '_turret.png' if has_turret else 'NONE'}")
    A("image_shadow: AUTO")
    A("shadowOffsetX: 1"); A("shadowOffsetY: 1")
    if sp["chassis"] != "hover": A("dustEffect: true")
    A("teamColoringMode: pureGreen")
    A("")

    air_ok = ("missiles_air" in wp) or ("missiles_both" in wp) or (sp["role"]=="AA platform") or ("AA walker" in sp["role"]) or ("heavy AA" in sp["role"]) or ("AA battery" in sp["role"])
    land_only = "missiles_air" in wp
    A("[attack]")
    if "melee" in wp: A("isMelee: true")
    A(f"canAttack: {str(bool(wp)).lower()}")
    A(f"canAttackFlyingUnits: {str(air_ok).lower()}")
    A(f"canAttackLandUnits: {str(bool(wp and not land_only)).lower()}")
    A("canAttackUnderwaterUnits: false")
    A(f"turretSize: {max(5, sp['radius']-3)}")
    A(f"turretTurnSpeed: {4 if sp['tier']<4 else 5}")
    A(f"maxAttackRange: {rng}")
    A(f"shootDelay: {cyc}s")
    A("aimOffsetSpread: 0.25")
    A("")

    if wp:
        A("[turret_1]"); A("x: 0"); A("y: 0"); A("projectile: 1"); A("canShoot: true")
        A(f"turnSpeed: {4 if sp['tier']<4 else 5}"); A("recoilOffset: -2")
        def snd(s, v=0.25): A(f"shoot_sound: {s}"); A(f"shoot_sound_vol: {v}")
        if "gun" in wp:
            d, (frame, sound), r, c = wp["gun"]
            snd(sound)
            A("shoot_flame: small"); A("shoot_light: #FFEECCCC"); A("")
            A("[projectile_1]")
            A(f"directDamage: {d}"); A("life: 70"); A("speed: 6"); A(f"frame: {frame}"); A("drawSize: 1")
        if "mortar" in wp:
            mo = wp["mortar"]; d, area, r = mo[0], mo[1], mo[2]
            snd("cannon_firing", 0.3); A("")
            A("[projectile_1]")
            A("directDamage: 15"); A(f"areaDamage: {d}"); A(f"areaRadius: {area}")
            A("life: 90"); A("speed: 4"); A("ballistic: true"); A("ballistic_height: 30")
            A("frame: 3"); A("drawSize: 1"); A("trailEffect: true")
            if len(mo)>3 and isinstance(mo[3], dict) and mo[3].get("shrapnel"):
                A(f"spawnProjectilesOnEndOfLife: shrap*{mo[3]['shrapnel']}(offsetRandomXY=25)")
                A("")
                A("[projectile_shrap]"); A("directDamage: 10"); A("life: 25"); A("speed: 3"); A("frame: 1"); A("drawSize: 0.7")
        if "missiles_air" in wp or "missiles_both" in wp:
            key = "missiles_air" if "missiles_air" in wp else "missiles_both"
            d, c, r = wp[key]
            snd("missile_fire", 0.2); A("")
            A("[projectile_1]")
            A(f"directDamage: {d}"); A("life: 70"); A("speed: 1.5"); A("targetSpeed: 7")
            A("image: rocket.png"); A("trailEffect: true")
        if "beam" in wp:
            b = wp["beam"]; d, r, c = b[0], b[1], b[2]
            opts = b[3] if len(b)>3 else {}
            lightning = opts.get("lightning"); emp = opts.get("emp")
            if lightning:
                snd("lighting_burst", 0.3); A("shoot_flame: CUSTOM:sparks2*3"); A("shoot_light: #FFcceeee")
                A("chargeEffectImage: SHARED:lighting_charge.png")
            else:
                snd("plasma_fire2", 0.25)
            A("")
            A("[projectile_1]")
            A(f"directDamage: {d}"); A("life: 25"); A("instant: true")
            if lightning: A("lightingEffect: true")
            if emp: A("hullDamageMultiplier: 0"); A("shieldDamage: 60")
            A("frame: 0"); A("drawSize: 1.2")
        if "melee" in wp:
            d, mrng = wp["melee"]
            A("")
            A("[projectile_1]")
            A(f"directDamage: {d}"); A("life: 10"); A("speed: 5"); A("frame: 0"); A("drawSize: 0.5")
        if "flame" in wp:
            d, r, c = wp["flame"]
            snd("firing3", 0.2); A("")
            A("[projectile_1]")
            A(f"directDamage: {d}"); A("areaDamage: 4"); A("areaRadius: 12"); A("life: 25"); A("speed: 7"); A("speedSpread: 1"); A("frame: 3"); A("drawSize: 1.5")
        if wp.get("mgs"):
            A("")
            A("[turret_2]"); A("x: -6"); A("y: 5"); A("attachedTo: 1"); A("slave: true"); A("invisible: true")
            A("projectile: 2"); A("turnSpeed: 8"); A("delay: 0.2s"); A("limitingRange: 140")
            A("canAttackFlyingUnits: true"); A("canAttackLandUnits: true"); A("canAttackUnderwaterUnits: false")
            A("shoot_sound: gun_fire"); A("shoot_sound_vol: 0.1")
            A("")
            A("[projectile_2]"); A("directDamage: 8"); A("life: 40"); A("speed: 9"); A("frame: 0"); A("drawSize: 0.8")
            A("")
            A("[turret_3]"); A("x: 6"); A("y: 5"); A("attachedTo: 1"); A("slave: true"); A("invisible: true")
            A("projectile: 2"); A("turnSpeed: 8"); A("delay: 0.2s"); A("limitingRange: 140")
            A("canAttackFlyingUnits: true"); A("canAttackLandUnits: true"); A("canAttackUnderwaterUnits: false")
            A("shoot_sound: gun_fire"); A("shoot_sound_vol: 0.1")
        if "lays mines" in sp["extra"]:
            A("")
            A("[action_layMine]")
            A("text: Lay Mine")
            A("buildSpeed: 2s")
            A("pos: 1")
            A("spawnUnits: aeMine(offsetRandomXY=40, spawnChance=1)")
            A("addActionCooldownTime: 4s")
            A("displayType: action")
    if wp.get("nuke"):
            A("")
            A("[turret_silo]"); A("x: 0"); A("y: 0"); A("canShoot: false")
            A("")
            A("[turret_siloTop]"); A("attachedTo: silo"); A("slave: true"); A("invisible: true")
            A("projectile: nukeProjectile"); A("shoot_sound: nuke_launch"); A("shoot_sound_vol: 0.5")
            A("shoot_flame: CUSTOM:sparks2*3, CUSTOM:lightSlowFade")
            A("")
            A("[projectile_nukeProjectile]")
            A("tags: nuke"); A("directDamage: 120"); A("life: 99999"); A("speed: 0.1")
            A("targetSpeed: 2.7"); A("targetSpeedAcceleration: 0.02"); A("largeHitEffect: true")
            A("ballistic: true"); A("ballistic_delaymove_height: 80"); A("ballistic_height: 110")
            A("frame: 0"); A("drawType: 1"); A("targetGround: true"); A("areaDamage: 5000")
            A("areaHitAirAndLandAtSameTime: true"); A("alwaysVisibleInFog: true"); A("areaRadius: 220")
            A("areaExpandTime: 75"); A("shouldRevealFog: true"); A("nukeWeapon: true")
            A("")
            A("[effect_lightSlowFade]")
            A("image: light_50.png"); A("life: 40"); A("fadeOut: true"); A("attachedToUnit: true")
            A("color: #ffddaa"); A("scaleFrom: 0.7"); A("scaleTo: 0.7"); A("alpha: 0.5"); A("drawUnderUnits: true")
            # copy light_50.png into this unit folder
            src = "units/mini_mammoth/light_50.png"
            if os.path.exists(src):
                from shutil import copyfile
                copyfile(src, os.path.join(folder, "light_50.png"))
    A("")
    A("[movement]")
    A(f"movementType: {'HOVER' if sp['chassis']=='hover' else 'LAND'}")
    A(f"moveSpeed: {sp['speed']}")
    A("moveAccelerationSpeed: 0.06"); A("moveDecelerationSpeed: 0.15")
    A(f"maxTurnSpeed: {max(2, 6 - sp['radius']//3)}"); A("turnAcceleration: 0.25")
    A("moveSlidingMode: false"); A("moveIgnoringBody: false")
    A("")
    A("[ai]"); A("useAsBuilder: false")

    with open(os.path.join(folder, uid + ".ini"), "w") as f:
        f.write("\n".join(L) + "\n")
    print("generated", uid, f"({name})")

def gen_units(specs, base="units"):
    for sp in specs: gen_one(sp, base)
