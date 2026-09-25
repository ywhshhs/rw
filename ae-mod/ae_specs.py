"""AE unit spec table — single source of truth for all roster + codename units.
Each spec: (codename/display, tier, chassis, cost, hp, shield, armour, speed, role, weapons, extras)
Weapons format: dict(turret sprite type, projectiles...) — generated into full INIs."""
from ae_sprites import *

T2_FACTORY, T3_FACTORY, EXP_FACTORY = "landFactory", "landFactory", "aeExperimentalFactory"

SPECS = []
def U(name, tier, chassis, cost, hp, role, weapons=None, shield=0, armour=0, speed=0.9,
      radius=None, extra="", factory=T2_FACTORY, accent="steel"):
    SPECS.append(dict(name=name, tier=tier, chassis=chassis, cost=cost, hp=hp, role=role,
                      weapons=weapons or {}, shield=shield, armour=armour, speed=speed,
                      radius=radius or max(6,int(hp**0.5)), extra=extra,
                      factory=factory, accent=accent))

# ============ BATCH 2 — T2 (roster 6 + codename 6) ============
U("Ankylo",2,"tracked",1400,700,"heavy tank", weapons=dict(gun=(55,(4,"large_gun_fire1"),150,1.6)), armour=4, speed=0.6, radius=13, accent="steel")
U("Lobber",2,"artillery",1200,150,"ballistic artillery", weapons=dict(mortar=(55,30,320)), speed=0.7, radius=11, accent="olive")
U("Bramble",2,"aa_pod",900,140,"AA platform", weapons=dict(missiles_air=(30,0.7,180)), shield=50, speed=1.0, radius=10, accent="steel")
U("Mantis",3-1,"tracked",1300,260,"tank hunter", weapons=dict(gun=(90,(6,"missile_fire"),170,1.8)), speed=1.0, radius=11, extra="dies to swarms", accent="olive")
U("Axolotl",2,"medic",1100,260,"tracked healer", shield=100, speed=0.7, radius=11, accent="white")
U("Kestrel",2,"hover",1500,200,"multi-role missiles", weapons=dict(missiles_both=(35,0.9,200)), speed=1.1, radius=11, accent="steel")
# codename T2 units
U("R2-01 Hound",2,"tracked",800,160,"flame runner", weapons=dict(flame=(4,110,140)), speed=1.3, radius=10, accent="red")
U("A2-02 Viper",2,"wheeled",900,200,"mine layer", weapons=dict(gun=(10,(2,"gun_fire"),90,0.5)), speed=1.1, radius=10, extra="lays mines")
U("S2-03 Mule",2,"wheeled",600,300,"transport (4 slots)", speed=0.8, radius=12, extra="maxTransportingUnits 4")
U("H2-04 Skate",2,"hover",1000,140,"hover missile cart", weapons=dict(missiles_both=(20,0.8,160)), shield=40, speed=1.4, radius=10, accent="steel")
U("D2-05 Picker",2,"biped",350,120,"walker scout", speed=1.8, radius=8, extra="sight 32", accent="tan")
U("S2-06 Owl",2,"wheeled",700,150,"mobile radar", speed=0.7, radius=10, extra="sight 40", accent="white")
U("R2-07 Ferry",2,"hover",800,280,"amphibious transport", speed=0.9, radius=12, extra="maxTransportingUnits 4, sight 24", accent="white")
U("A2-08 Scrapper",2,"wheeled",700,190,"armed salvager", weapons=dict(gun=(8,(2,"gun_fire"),100,0.5)), speed=0.8, radius=10, extra="reclaim", accent="tan")
U("D2-09 Ricochet",2,"tracked",600,110,"dodge skirmisher", weapons=dict(gun=(12,(2,"tank_firing"),100,0.6)), shield=80, speed=1.6, radius=9, accent="steel")

# ============ BATCH 3 — T3 (roster 5 + codename 6) ============
U("Bedrock",3,"heavy_tracked",4200,2000,"super-heavy", weapons=dict(gun=(100,(4,"large_gun_fire1"),190,2.5)), armour=10, speed=0.45, radius=16, factory=T3_FACTORY, accent="dark")
U("Avalanche",3,"artillery",4000,300,"heavy artillery", weapons=dict(mortar=(120,60,420)), speed=0.5, radius=14, factory=T3_FACTORY, accent="dark")
U("Turtle",3,"shield_anchor",3500,800,"defense anchor", shield=400, speed=0.5, radius=14, extra="repairs allies", factory=T3_FACTORY, accent="dark")
U("Hailstorm",3,"aa_battery",3200,400,"heavy AA", weapons=dict(missiles_air=(40,0.6,260)), speed=0.6, radius=12, factory=T3_FACTORY, accent="dark")
U("Stampede",3,"crawler",6000,1600,"experimental breacher", weapons=dict(gun=(150,(4,"large_gun_fire1"),200,3.0), mgs=True), armour=8, speed=0.4, radius=18, factory=T3_FACTORY, accent="dark")
U("H3-01 Lance",3,"tracked",2200,260,"railgun sniper", weapons=dict(beam=(70,240,1.5)), speed=0.8, radius=11, factory=T3_FACTORY, accent="dark")
U("A3-02 Wick",3,"biped",1800,500,"flame walker", weapons=dict(flame=(6,130,150)), armour=3, speed=0.7, radius=12, factory=T3_FACTORY, accent="red")
U("D3-03 Horn",3,"artillery",2000,220,"counter-battery", weapons=dict(mortar=(45,25,380)), speed=0.55, radius=11, factory=T3_FACTORY, accent="olive")
U("S3-04 Puffer",3,"medic",1600,350,"shield-bus healer", shield=250, speed=0.6, radius=12, extra="repairs allies", factory=T3_FACTORY, accent="white")
U("H3-05 Scatter",3,"artillery",2400,180,"cluster artillery", weapons=dict(mortar=(50,35,300,{"shrapnel":6})), speed=0.55, radius=12, factory=T3_FACTORY, accent="olive")
U("R3-06 Newt",3,"hover",400,140,"amphibious scout", speed=1.9, radius=8, extra="sight 36", factory=T3_FACTORY, accent="tan")
U("H3-07 Needle",3,"tracked",2600,240,"beam sniper", weapons=dict(beam=(90,280,1.6)), speed=0.75, radius=11, factory=T3_FACTORY, accent="dark")
U("D3-08 Hedgehog",3,"biped",2300,520,"AA walker", weapons=dict(lightning_air=(25,170,0.5)), armour=4, speed=0.65, radius=12, factory=T3_FACTORY, accent="dark")
U("S3-09 Hearth",3,"crawler",1700,600,"repair station", speed=0.5, radius=13, extra="repairs allies fast", factory=T3_FACTORY, accent="white")

# ============ BATCH 4 — T4 experimental (E-series) ============
U("E4-01 Widow",4,"spider",2800,700,"spider tank", weapons=dict(gun=(60,(4,"large_gun_fire1"),170,1.4), mgs=True), armour=6, speed=0.9, radius=13, factory=EXP_FACTORY, accent="purple")
U("E4-02 Tortoise",4,"crawler",3200,900,"siege crawler", weapons=dict(mortar=(80,50,420,{"arc_high":True})), armour=8, speed=0.35, radius=16, factory=EXP_FACTORY, accent="purple")
U("E4-03 Tesla",4,"tracked",3000,400,"chain lightning tank", weapons=dict(beam=(90,200,0.8,{"lightning":True})), speed=0.8, radius=11, factory=EXP_FACTORY, accent="purple")
U("E4-04 Doomsday",4,"nuke_silo",8000,500,"nuke launcher", weapons=dict(nuke=True), speed=0, radius=18, factory=EXP_FACTORY, accent="purple", extra="isBuilding? no - mobile, slow")
U("E4-05 Phase",4,"hover",2400,300,"blink tank", weapons=dict(gun=(25,(3,"plasma_fire2"),130,0.8)), speed=1.3, radius=10, extra="teleport action", factory=EXP_FACTORY, accent="purple")
U("E4-06 Foundry",4,"crawler",4000,800,"mobile factory", weapons=dict(mgs=True), speed=0.45, radius=15, factory=EXP_FACTORY, accent="purple", extra="builds Hornet+Thorn")
U("E4-07 Rail",4,"artillery",5000,300,"mass driver", weapons=dict(beam=(120,520,4.0)), speed=0.4, radius=13, factory=EXP_FACTORY, accent="purple")
U("E4-08 Leech",4,"tracked",2800,500,"vampiric crawler", weapons=dict(gun=(35,(4,"tank_firing"),140,0.9)), speed=0.7, radius=11, extra="high regen", factory=EXP_FACTORY, accent="purple")

# ============ BATCH 5 — T5 experimental (X-series) ============
U("X5-01 Omega",5,"heavy_tracked",9000,1800,"omega tank", weapons=dict(gun=(120,(4,"large_gun_fire1"),200,2.0), mgs=True), armour=12, speed=0.55, radius=18, factory=EXP_FACTORY, accent="gold")
U("X5-02 Storm",5,"crawler",7000,600,"lightning fortress", weapons=dict(beam=(70,220,0.6,{"lightning":True,"multi":4})), armour=6, speed=0.45, radius=16, factory=EXP_FACTORY, accent="gold")
U("X5-03 Bastion",5,"shield_anchor",8000,1200,"shield citadel", shield=600, speed=0.3, radius=16, extra="repairs allies", factory=EXP_FACTORY, accent="gold")
U("X5-04 Clock",5,"nuke_silo",10000,400,"doomsday clock", weapons=dict(nuke=True), speed=0, radius=15, factory=EXP_FACTORY, accent="gold", extra="suprise: explodes once")
U("X5-05 Titan",5,"titan",12000,2200,"apex walker", weapons=dict(gun=(150,(4,"large_gun_fire1"),220,2.6), mgs=True), armour=14, speed=0.35, radius=20, factory=EXP_FACTORY, accent="gold", extra="maxTransportingUnits 4")
U("X5-06 Hive",5,"crawler",9500,1000,"mothership crawler", weapons=dict(mgs=True), speed=0.4, radius=17, factory=EXP_FACTORY, accent="gold", extra="maxTransportingUnits 6")
U("X5-07 Null",5,"tracked",6500,500,"EMP tank", weapons=dict(beam=(10,190,1.2,{"emp":True})), speed=0.75, radius=11, factory=EXP_FACTORY, accent="gold", extra="hullDamageMultiplier 0 - shield killer")
U("X5-08 Singularity",5,"titan",15000,2000,"the final unit", weapons=dict(gun=(180,(4,"large_gun_fire1"),230,2.2), mgs=True, missiles_air=(30,0.8,200)), armour=14, speed=0.3, radius=22, factory=EXP_FACTORY, accent="gold", extra="nukeOnDeath")

# ---- spawned-only units (not in any build menu) ----
MINE = dict(name="Mine", tier=2, chassis="hover", cost=0, hp=25, role="proximity mine",
            weapons=dict(melee=(300,10)), shield=0, armour=0, speed=0.0, radius=5,
            extra="melee mine - spawned by Viper only", factory="NONE", accent="red")
SPECS.append(MINE)
