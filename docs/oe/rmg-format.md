# Heroes of Might & Magic: Olden Era — `.rmg.json` Template Format

**The single comprehensive reference** for the Olden Era random-map-generator template format:
the JSON data model, the PNG preview, how templates are generated, the external content contract,
and the full value catalogs.

**Sources.** Reverse-engineered and cross-checked against (a) the 56 official templates in
[`templates/official/`](../templates/official) (+ their `.png` previews), and (b) the Olden Era Template
Generator (a C# WPF app), whose knowledge has been **drained and preserved in this repo** — the
generator project itself has been removed. The durable resources now live at:

- [`data/`](../data) — the bundled engine data that templates reference by SID (content
  pools, content lists, zone layouts, 641 encounter templates, the object value table, biome assets).
- [`lib/`](../lib) — structured catalogs extracted from the generator's C# source
  (object SID→name maps, value catalogs, variant meanings, placement presets, default caps,
  constants), indexed by [`lib/README.md`](../lib/README.md).

Structural invariants are machine-checkable via [`../tools/validate_rmg.py`](../tools/validate_rmg.py).
Anarchy 8-player / 240px isolated-spawn rules: [`../tools/validate_template.py`](../tools/validate_template.py).

---

## Contents

- [Part I — Orientation](#part-i--orientation)
- [Part II — JSON data model](#part-ii--json-data-model)
- [Part III — Reading the PNG preview](#part-iii--reading-the-png-preview)
- [Part IV — How templates are generated](#part-iv--how-templates-are-generated)
- [Part V — External content contract & resources](#part-v--external-content-contract--resources)
- [Part VI — Value catalogs](#part-vi--value-catalogs)
- [Part VII — Authoring & validation checklist](#part-vii--authoring--validation-checklist)
- [Appendix — source pointers](#appendix--source-file-pointers)

---

# Part I — Orientation

## What a template is

An `.rmg.json` file is a **random-map-generator template**, not a finished map. It defines a **zone
graph** (zones = nodes, connections = edges) plus rules. The game's RMG re-randomizes terrain,
biomes, object placement, and content **within** that graph every match, so one template yields a
different map each game. A complete, shippable template is **two files** that share a basename:

- `Name.rmg.json` — the template.
- `Name.png` — a preview image (the game displays it in the template picker). See [Part III](#part-iii--reading-the-png-preview).

## ⚠️ Two schema levels — engine superset vs. generator subset

There are effectively two versions of this schema:

- **Engine schema (superset).** What the game actually reads. Hand-authored official templates use a
  richer field set than any tool models. **This document specifies the engine schema.**
- **Generator round-trip model (subset).** The `Models/Unfrozen/*.cs` classes the Template Generator
  reads/writes. It emits **valid** templates but **cannot represent** several engine fields — loading
  an official template into the editor and re-saving would silently drop them.

Fields confirmed in official templates but **absent from the generator model** (drop on round-trip):

| Engine-only field | Uses | Location |
|---|---|---|
| `contentCountLimits[].limits[].variant` | 2092 | count-limit entry |
| `connections[].guardRandomization` | 166 | connection |
| `contentCountLimits[].limits[].includeLists` | 163 | count-limit entry |
| `mainObjects[].factions` (plural) | 90 | main object |
| `mainObjects[].guardRandomization` | 61 | main object |
| `mandatoryContent[].content[].designatedEncounter` | 41 | content item |
| `contentCountLimits[].limits[].content` | 39 | count-limit entry |
| `zone.randomHireInitialUnitIncrement` / `…EnableWeeklyUnitIncrement` | 34 / 34 | zone |
| `mandatoryContent[].content[].owner` | 8 | content item |
| `mandatoryContent[].content[].road` | 6 | content item |
| `mainObjects[].enableWeeklyUnitIncrement` / `initialUnitIncrement` | 4 / 4 | main object |
| `globalBans.heroes` / `globalBans.skills` | 2 / 1 | global bans |
| `mainObjects[].isKeyObject` | 2 | main object |
| `mandatoryContent[].content[].guardValue` | 1 | content item |

Conversely, the generator model declares a few fields no shipped template uses:
`zoneLayouts[].minLakeArea`, `contentCountLimits[].playerMin` / `playerMax`.

## File conventions

| Aspect | Notes |
|---|---|
| Extension | `.rmg.json` (+ sidecar `.png`) |
| Encoding | UTF-8; some files carry a BOM (parse with `utf-8-sig`) |
| Strictness | Mostly strict JSON, but several files have **trailing commas** / leading whitespace before `{`. Use a tolerant parser (strip `,` before `}`/`]`). |
| Formatting | Tab-indented, hand-edited, inconsistent between files. Match the surrounding file when editing. |
| `*Sid` fields | A **SID** is a string ID resolved against the game's content database. SIDs are **not** defined in the template (see [Part V](#part-v--external-content-contract--resources)). |
| Object indexing | `mainObjects` are referenced positionally (`"0"`, `"1"`). Reordering them silently breaks roads, biomes, and rules. |

---

# Part II — JSON data model

## 2.1 Top-level object

| Key | Req. | Type | Notes |
|---|---|---|---|
| `name` | ✅ | string | Template display name. |
| `gameMode` | ✅ | enum | `"Classic"` (36/56) or `"SingleHero"` (20/56). |
| `description` | ✅ | string | Localization key, e.g. `templates_description_anarchy`. |
| `displayWinCondition` | ✅ | string | Win-condition ID, e.g. `win_condition_1` (see [§6](#part-vi--value-catalogs)). |
| `sizeX`, `sizeZ` | ✅ | int | Square (`sizeX == sizeZ`). Range 64–240 official; experimental to 512. |
| `gameRules` | ✅ | object | [§2.2](#22-gamerules). |
| `valueOverrides` | 26/56 | array | [§2.3](#23-valueoverrides--globalbans). |
| `globalBans` | 18/56 | object | [§2.3](#23-valueoverrides--globalbans). |
| `variants` | ✅ | array | One or more layouts; engine picks one per match. [§2.4](#24-variants). |
| `zoneLayouts` | ✅ | array | Named terrain presets referenced by zones. [§2.9](#29-zonelayouts). |
| `mandatoryContent` | ✅ | array | Named content packs referenced by zones. [§2.10](#210-mandatorycontent--the-placement-rule-system). |
| `contentCountLimits` | ✅ | array | Named cap-sets referenced by zones. [§2.11](#211-contentcountlimits). |
| `contentPools` | ✅ | array | **Always empty `[]`** in shipped templates ([§2.12](#212-contentpools--contentlists)). |
| `contentLists` | ✅ | array | **Always empty `[]`** in shipped templates. |
| `orientation` | 1/56 | object | Rare top-level orientation (`OctoJebus`). [§2.5](#25-orientation--border). |
| `border` | 1/56 | object | Rare map-edge band (`OctoJebus`). [§2.5](#25-orientation--border). |

## 2.2 `gameRules`

```jsonc
"gameRules": {
  "heroCountMin": 5, "heroCountMax": 10, "heroCountIncrement": 1,  // commonly 5/10/1
  "heroHireBan": false,
  "encounterHoles": true,        // enable the "encounter hole" battle mechanic (Anarchy signature)
  "tournamentRules": false,      // optional
  "factionLawsExpModifier": 1.0, // optional; clamp [0.25, 2.0]
  "astrologyExpModifier": 1.0,   // optional; clamp [0.25, 2.0]
  "bonuses": [ … ],              // optional (22/56), see below
  "winConditions": { … }         // required
}
```

### `winConditions`

| Key | Coverage | Meaning |
|---|---|---|
| `classic` | 56 | Standard "defeat all". |
| `desertion` + `desertionDay` + `desertionValue` | 56 | Lose if army value < `desertionValue` after `desertionDay`. |
| `heroLighting` + `heroLightingDay` | 56 | Hero-lighting rule from day N. |
| `lostStartHero` | 56 | Lose on losing the start hero. |
| `lostStartCity` (+ `lostStartCityDay`) | 50 | Lose on losing the start city. |
| `cityHold` + `cityHoldDays` | 13 | Hold-a-city victory. |
| `tournament*` (5 keys) | 5 | Tournament scoring (`tournamentDays`, `tournamentAnnounceDays`, `tournamentPointsToWin`, `tournamentSaveArmy`). |
| `gladiatorArena*` (6 keys) + `championSelectRule` | 8 | Arena mode. |

### `bonuses` (start-game bonuses)

```jsonc
{ "sid": "add_bonus_res", "receiverSide": -1, "receiverFilter": "start_hero",
  "parameters": ["gold", "10000"] }
```

`receiverSide: -1` = all players. `receiverFilter`: `start_hero` | `all_heroes`. SIDs:
`add_bonus_res`, `add_bonus_hero_spell`, `add_bonus_hero_stat`, `add_bonus_hero_unit_multipler`,
`add_bonus_hero_item`. Note some editor presets expand to **two** entries — e.g. a *free* spell adds
a companion `add_bonus_hero_stat` with `["magicCostSidSet", <spell>, "-999", "0"]` to zero its cost.

## 2.3 `valueOverrides` & `globalBans`

**`valueOverrides`** — globally override an object's guard strength (`variant: -1` = all variants):

```jsonc
"valueOverrides": [ { "sid": "point_of_balance", "variant": -1, "guardValue": 7500 } ]
```

**`globalBans`** — an **object** keyed by category, each an array of banned SIDs:

```jsonc
"globalBans": {
  "items":  ["voodoosh_doll_artifact", "flag_of_truce_artifact"],   // artifact SIDs
  "magics": ["neutral_magic_town_portal"],                          // spell SIDs
  "heroes": ["demon_hero_3", "dungeon_hero_10"],                    // engine-only
  "skills": ["skill_logistic", "skill_siege"]                       // engine-only
}
```

The generator models only `items`/`magics`; `heroes`/`skills` are engine-only. ID catalogs live in
`KnownValues.BannableItems` / `BannableMagics` (see [§6](#part-vi--value-catalogs)).

## 2.4 `variants`

Array of independent layouts; the engine picks one per match (52/56 ship one; a few ship 3 or 5).

```jsonc
{ "orientation": { "mode": "MinimalBoundingSquare", … },  // see §2.5
  "zones": [ … ],          // graph nodes — §2.6
  "connections": [ … ] }   // graph edges — §2.8
```

> **Per-zone tuning must be applied to *every* variant**, not just the first.

## 2.5 `orientation` & `border`

`orientation` can appear at the top level (rare) or per variant (normal):

```jsonc
"orientation": {
  "mode": "MinimalBoundingSquare",   // MinimalBoundingSquare (43) | BoundingCircle (12) | None (11)
  "zeroAngleZone": "Spawn-A",        // radial modes: anchor + angle spread
  "baseAngleMin": 45, "baseAngleMax": 45,
  "randomAngleAmplitude": 360, "randomAngleStep": 90
}
```

`border` — map-edge band of obstacles / water (only `OctoJebus`):

```jsonc
"border": { "cornerRadius": 0.0, "obstaclesWidth": 3,
  "obstaclesNoise": [ { "amp": 1, "freq": 12 } ],
  "waterWidth": 0, "waterNoise": [ { "amp": 1, "freq": 12 } ], "waterType": "water grass" }
```

## 2.6 Zone object (graph node)

Every zone carries the full core block (902 zones across the 56 templates share the first ~21 keys):

```jsonc
{
  "name": "Spawn-A",                 // unique within variant; referenced by connections/roads
  "size": 1.0,                       // relative area weight
  "layout": "zone_layout_spawns",    // → zoneLayouts[].name (§2.9)

  // guard model
  "guardCutoffValue": 1500, "guardRandomization": 0.05,
  "guardMultiplier": 1.6,            // 716/902 — scales rolled guard strength
  "guardWeeklyIncrement": 0.20,
  "guardReactionDistribution": [2,2,1,1,0,0],   // 6-bucket reaction-tier weights

  // content pools (SIDs resolved engine-side, Part V)
  "guardedContentPool":   ["template_pool_…_guarded_start_zone"],
  "unguardedContentPool": ["template_pool_…_unguarded_start_zone"],
  "resourcesContentPool": ["content_pool_general_resources_start_zone_rich"],

  // named packs (resolved INLINE in this file)
  "mandatoryContent":  ["mandatory_content_spawn"],    // → §2.10
  "contentCountLimits":["content_limits_spawn"],        // → §2.11

  // economy: flat budget + per-area budget, per channel
  "guardedContentValue": 750000,   "guardedContentValuePerArea": 10000,
  "unguardedContentValue": 250000, "unguardedContentValuePerArea": 0,
  "resourcesValue": 300000,        "resourcesValuePerArea": 0,

  // objects, biomes, roads
  "mainObjects": [ … ],            // §2.7
  "zoneBiome":        { "type": "MatchMainObject", "args": ["0"] },
  "contentBiome":     { "type": "MatchMainObject", "args": ["0"] },
  "metaObjectsBiome": { "type": "MatchMainObject", "args": ["0"] },
  "roads": [ … ],                  // §2.8

  // optional
  "crossroadsPosition": 0,                 // 418/902
  "diplomacyModifier": -0.5,               // 313/902 — neutral-join bias (-0.5 or -0.25)
  "encounterHolesSettings": { "affectedEncounters": 0.66, "twoHoleEncounters": 0.66 },  // 163/902
  "randomHireInitialUnitIncrement": …,     // 34/902 — engine-only
  "randomHireEnableWeeklyUnitIncrement": … // 34/902 — engine-only
}
```

**Economy model.** Three channels — guarded / unguarded / resources — each budgeted by a flat
`…Value` plus an area-scaled `…ValuePerArea`. The RMG fills the zone until budgets are met. On larger
maps the per-area term dominates → scale it by ≈ `(newSize / oldSize)²`.

**Biome selectors** (`zoneBiome` / `contentBiome` / `metaObjectsBiome`) — `{ "type", "args" }`:

| `type` | Meaning |
|---|---|
| `MatchMainObject` | Inherit from a main object by index, `args: ["0"]`. |
| `MatchZone` | Inherit from another named zone, `args: ["Spawn-A"]`. |
| `FromList` | Pick from an explicit biome list, `args: ["Sand"]`; `[]` = any. |
| `Match` | Match a main object with an extra zone argument (rare). |

## 2.7 `mainObjects`

Anchor objects the zone is built around. Order matters (positional indexing).

```jsonc
{
  "type": "Spawn",                        // City | Spawn | AbandonedOutpost | None | GladiatorArena
  "spawn": "Player1",                     // required for Spawn: Player1..Player8
  "owner": "Player2",                     // optional pre-owned object (39 uses)
  "placement": "Uniform",                 // Uniform | Center | Connection | NearZone
  "placementArgs": ["true", "0.7", "3"],  // stringified; see table
  "faction": { "type": "Match", "args": ["0"] },   // single faction selector
  "factions": [],                         // optional plural list (90 uses, engine-only)
  "buildingsConstructionSid": "poor_buildings_construction",
  "guardChance": 1.0, "guardValue": 3000, "guardWeeklyIncrement": 0.20,
  "guardRandomization": 0.05,             // engine-only on main objects
  "removeGuardIfHasOwner": true,
  "isKeyObject": true,                    // engine-only, rare
  "holdCityWinCon": true                  // ties object to a hold-city win condition
}
```

| `type` | Count | Meaning |
|---|---|---|
| `City` | 614 | Town/castle. |
| `Spawn` | 220 | Player start; carries `spawn`. |
| `AbandonedOutpost` | 40 | Neutral guarded outpost. |
| `None` / `GladiatorArena` | 2 / 1 | Placeholder / arena-mode object. |

**`placement` / `placementArgs`** (args are strings):

| `placement` | `placementArgs` | Reading |
|---|---|---|
| `Uniform` | `["<edgeAvoid bool>","<radialBias −1..1>","<count/spread>"]` e.g. `["true","0.7","3"]` | Scatter; bias toward center (+) or edge (−). `[]` also valid. |
| `Center` | `["true","1","3"]` or `[]` | Near zone center. |
| `Connection` | `["<ConnectionName>"]` | At a named connection (gateway). |
| `NearZone` | `["<ZoneName>"]` | Near another zone. |

**`faction` / `factions`** — `{ "type", "args" }`: `None` (503, neutral), `Match` (250, match another
object's faction e.g. `args:["0"]`), `FromList` (124, `args:[]` = any).

## 2.8 `roads` & connections

A zone's **`roads`** lay segments between **references** inside that zone:

```jsonc
"roads": [ { "type": "Stone",                       // Stone (1897) | Dirt (92) | omitted
             "from": { "type": "MainObject", "args": ["0"] },
             "to":   { "type": "Connection", "args": ["Center-A-Main"] } } ]
```

Reference `{ "type", "args" }` resolves to: `MainObject` (by index), `Connection` (by name),
`Crossroads` (zone crossroads), `MandatoryContent` (a placed mandatory object).

**`connections`** are the graph edges; `from`/`to` are **zone names**:

```jsonc
{
  "name": "Center-A-Main",
  "from": "Center", "to": "Spawn-A",
  "connectionType": "Direct",  // Direct | Default | Portal | Proximity | GladiatorArena
  "guardValue": 70000, "guardWeeklyIncrement": 0.20,
  "guardEscape": false,        // 604 — bypassable?
  "guardRandomization": 0.05,  // 166 — engine-only
  "guardZone": "Center",       // 200 — which zone's pools size the guard
  "guardMatchGroup": "g1",     // 40 — share guard rolls across a group
  "simTurnSquad": true,        // 430 — simultaneous-turn squad gateway
  "road": true,                // build a road across (true 694 / false 223)
  "gatePlacement": "Center",   // 190
  "length": 0.94,              // Proximity only — relative spacing, NOT a path
  "portalPlacementRulesFrom": [ … ], "portalPlacementRulesTo": [ … ]  // Portal only
}
```

| `connectionType` | Count | Meaning |
|---|---|---|
| `Direct` | 730 | Real walkable, usually guarded passage. |
| `Default` | 382 | Standard passage (engine default). |
| `Portal` | 168 | Teleport link; placement via `portalPlacementRules{From,To}` (placement-rule grammar, §2.10). |
| `Proximity` | 111 | **Not a path** — sets only relative spacing (`length`) for the layout solver. |
| `GladiatorArena` | 2 | Arena-mode link. |

> **Isolation rule.** To keep players isolated, ensure **no `Direct`/`Default`/`Portal` connection
> links two zones hosting *different* players.** `Proximity` edges between rival spawns are fine
> (spacing only); linking two zones hosting the *same* player (alternate-spawn candidates) is fine.

## 2.9 `zoneLayouts`

Named terrain/obstacle presets referenced by `zone.layout`:

```jsonc
{ "name": "zone_layout_spawns",
  "obstaclesFill": 0.24, "obstaclesFillVoid": 0.24, "lakesFill": 0.3,
  "minLakeArea": 64,                 // optional (generator model; unused by shipped templates)
  "elevationClusterScale": 0.16,
  "elevationModes": [ { "weight": 2, "minElevatedFraction": 0.2, "maxElevatedFraction": 0.4 }, … ],
  "roadClusterArea": 160,
  "guardedEncounterResourceFractions": { "countBounds": [], "fractions": [0.5] },
  "ambientPickupDistribution": { "repulsion": 1.0, "noise": 0.3, "roadAttraction": 0.5,
                                 "obstacleAttraction": 0.0, "groupSizeWeights": [4,1,1] } }
```

The engine's default layout definitions (with extra `…Dencity` / `…SizeDistribution` fields) ship in
`data/zone_layouts/` — see [Part V](#part-v--external-content-contract--resources).

## 2.10 `mandatoryContent` & the placement-rule system

Named packs whose objects **must** be placed in any zone referencing them via `zone.mandatoryContent`:

```jsonc
{ "name": "mandatory_content_spawn", "content": [ <content item>, … ] }
```

**Content item:**

```jsonc
{
  "sid": "mine_gold",            // object to place (or use includeLists)
  "variant": 1,                  // specific variant; -1 = any (see VariantMapping, Part V)
  "includeLists": ["content_list_building_random_hires"],  // pull from a list instead of sid
  "isMine": true, "isGuarded": false,
  "soloEncounter": true,         // place as a standalone encounter
  "designatedEncounter": false,  // engine-only
  "owner": "Player2",            // engine-only
  "guardValue": …, "road": …,    // engine-only
  "rules": [ <placement rule>, … ]
}
```

**Placement-rule grammar** (also used by `portalPlacementRules*`) — scores candidate positions:

```jsonc
{ "type": "Road", "args": [], "targetMin": 0.1, "targetMax": 0.2, "weight": 1 }
```

| Field | Meaning |
|---|---|
| `type` | What to measure relative to: `Road` (734), `MainObject` (361), `Crossroads` (270), `Sid` (250), `Connection` (17). |
| `args` | Target selector, e.g. `["0"]` (main-object index), `["mine_wood"]` (SID). |
| `targetMin`/`targetMax` | Desired normalized-distance band (0..1). See `DistancePresets` ([Part V](#34-placement-rule-helpers)). |
| `weight` | Relative importance when combining rules. |

## 2.11 `contentCountLimits`

Named cap-sets referenced by `zone.contentCountLimits`:

```jsonc
{ "name": "content_limits_spawn",
  "playerMin": 2, "playerMax": 8,           // optional range gate (generator model; unused by shipped)
  "limits": [
    { "sid": "prison", "variant": -1, "maxCount": 4 },          // variant: engine-only
    { "sid": "arena", "maxCount": 1 },
    { "includeLists": ["basic_content_list_building_guarded_units_banks"],  // engine-only
      "content": [ { "sid": "dragon_utopia" } ], "maxCount": 12 } ] }        // content: engine-only
```

The generator model holds only `sid` + `maxCount`; `variant`, `includeLists`, `content` are engine-only.

## 2.12 `contentPools` / `contentLists`

Both top-level arrays are **empty `[]`** in all 56 shipped templates. The pool/list SIDs zones
reference (`content_pool_anarchy_*`, `basic_content_list_*`) are defined in the **game content
database**, bundled in [`data/`](../data) — see [Part V](#part-v--external-content-contract--resources).
The empty arrays are override hooks: a template *could* inline pools/lists here, but the official set
does not.

---

# Part III — Reading the PNG preview

Each template ships a sidecar `Name.png` (the game's template-picker thumbnail). Two formats exist
in the wild: ~**665×664** (official game thumbnails) and **700×700** (the generator's output). The
official previews are **parchment-styled schematic node-graphs**, not pictorial maps:

- **Numbered disc** = a player spawn zone; the number is the player slot (1–8). `OctoJebus` shows
  discs 1–8 in a ring around a central node → its JSON (8 spawns → `Center`).
- **Smaller coloured discs** around the players = neutral zones. Tier colour by zone `layout`:
  - `zone_layout_sides` → **bronze** (low), `zone_layout_treasure_zone` → **silver** (medium/high),
    `zone_layout_center` → **gold** (top), Hub → blue-grey.
  - Player/spawn zones render **green**.
- **Lines** = connections, drawn beneath zones: Direct/Default/Gladiator → thick **gold**;
  Portal → semi-transparent **blue**; Proximity → not drawn (spacing only).
- Some special templates ship a **"?" placeholder** instead (e.g. `Anarchy.png`).

**Layout algorithm** (`TemplatePreviewPngWriter.Render`, 700×700): zones are ordered from
`orientation.zeroAngleZone`; structured topologies (Ring/Chain/Hub/SharedWeb) use a ring layout;
Random/Balanced use the generator's in-memory position/ring stamps (`GeneratorPosition`/`GeneratorRing`,
both `[JsonIgnore]` — never in the JSON) with a Fruchterman–Reingold spring embedder. Tournament
two-cluster layouts render only the first cluster.

---

# Part IV — How templates are generated

The generator is the pure function `RmgTemplate Generate(GeneratorSettings)`, always emitting **one
variant**, structurally modelled on **Jebus Cross Classic**.

**Pipeline:** plan neutral zones (6 tier counters → letters/quality/castles) → pick hold-city neutral
(BFS equidistance) → compute tuning (content scale, density, guards) → build variant by topology →
attach layouts / mandatory content / rules / bans / overrides.

**Topologies** (`MapTopology`):

| Topology | UI label | Shape |
|---|---|---|
| `Default` | Ring | Closed ring; adjacent `Ring-{A}-{B}` Direct edges. |
| `Chain` | Chain | Linear, no wrap; `Chain-{A}-{B}`. |
| `HubAndSpoke` | Hub | Central `Hub` + spoke `Hub-{x}` Direct + outer `Pseudo-{A}-{B}` Proximity hints. |
| `SharedWeb` | Shared Web | Player→neutral spokes (`Web-…`) + neutral ring (`NRing-…`). |
| `Random` | Random | **Delaunay** edges (Bowyer–Watson) from random positions (`Rnd-{A}-{B}`). |
| `Balanced` | Balanced | 7 concentric quality rings (radii 0.42→0.03) + tier-aware connectivity. |

Tournament override for 2P fully isolates two clusters until the tournament starts. **Isolate player
zones** skips player↔player edges and runs `EnsurePlayerZonesConnected`. **Random portals** builds a
derangement (each zone → a non-adjacent target), one outgoing portal per zone, capped at
`MaxPortalConnections`.

**Scaling** (`GenerationTuning`):

```text
referenceArea = 160² / 4 = 6400 ;  zoneArea = mapSize² / totalZones
contentScale  = clamp(sqrt(zoneArea / referenceArea), 0.5, 2.5)
structure values     = base × contentScale × (StructureDensity% / 100)
per-area structure   = base × sqrt(contentScale) × (StructureDensity% / 100)
resources            = base × contentScale × (ResourceDensity% / 200)
main-object guards   = base × (NeutralStackStrength% / 100)
connection guards    = borderBase × (BorderGuardStrength% / 100)
```

**Border guard bases** (× BorderGuardStrength%): Player↔Player 30 000; Player↔Neutral
15 000/20 000/25 000 (low/med/high); Portal 25 000. Direct connections: `guardEscape:false`,
`simTurnSquad:true`, `guardWeeklyIncrement:0.15`.

**Limits:** max 32 zones total (max neutrals = 32 − players); players 2–8; default guard
randomization 0.05.

**Validation** — hard errors: empty name, `heroMin>heroMax`, zones over cap (10 simple / 32 advanced),
City-Hold without neutrals (non-hub), isolation without neutrals, tournament ≠ 2 players, tournament
with odd tier count. Warnings: default name, zone area < 1024 tiles, experimental size > 240, >10
zones with >1 castle, border guard > 100%.

> Full pipeline detail (tier ranks, gap ordering, hold-city BFS, connectivity repair, tournament
> mirroring) was specified by the generator's test suite (`TemplateGeneratorTests.cs`), distilled here.

---

# Part V — External content contract & resources

Zone `*ContentPool`, `includeLists`, and `layout` SIDs resolve to definitions **outside** the
template. That engine data is bundled in [`data/`](../data):

| Path | Files | Defines | Referenced by |
|---|---|---|---|
| `content_pools/` | 50 | `content_pool_*` / `template_pool_*` | zone `*ContentPool` |
| `content_lists/` | 17 | `basic_content_list_*` / `content_list_*` | pool / mandatory / count-limit `includeLists` |
| `zone_layouts/` | 1 | `zone_layout_*` | zone `layout` |
| `encounter_templates/` | 641 | `rmg_*` grid stamps | engine RMG (guarded encounters, holes) |
| `generator_config.json` | 1 | `metaObjects[]` — SID → gold `value` (+ `guardValue`), type, args | the value economy (below) |
| `generator_stats_config.json` | 1 | `statSids[]` — objects counted as "stats" | distribution |
| `generator_environment_assets.json` | 1 | `biomes[]` → tilesets → obstacle/pool asset SIDs | what biome names resolve to |

**Content pool** — weighted groups pulling from lists, optionally value-tiered:

```jsonc
{ "name": "content_pool_anarchy_rich_guarded_start_zone",
  "valueDistribution": { "priceBounds": [3999,6999,12999,20000], "weights": [5,11,16,8,4] },
  "groups": [
    { "weight": 50000, "includeLists": ["basic_content_list_pickup_random_items"],
      "content": [ { "sid": "random_item_legendary", "weight": 50 } ] },  // inline weight override; 0 = suppress
  ], "bans": [] }
```
Key files: `default_content_pools.json`, `basic_pools_*`, per-template `template_*_pools.json`
(incl. `template_anarchy_pools.json`, `template_octojebus_pools.json`), and tiered
`random_pools/…_t0..t5` (+ `classic_version/`).

**Content list** — flat weighted bag, optional biome gate:

```jsonc
{ "name": "basic_content_list_rare_resources",
  "content": [ { "sid": "resource_crystals", "weight": 50 },
               { "sid": "resource_gemstones", "weight": 100, "biome": "Grass" } ] }
```
Files: `basic_content_lists.json` (core), `basic_content_lists_variants_table.json` (per-tier),
`generator_content_lists.json`, `custom_content_lists_*` (per template).

**Zone layout** (`zone_layouts/default_zone_layouts.json`) — engine defaults; superset of the inline
template layout, adding `guardedEncounterDencity` [sic], `guardedEncounterSizeDistribution` (7-bucket),
`unguardedEncounter*`, `ambientPickupDensity`.

**Encounter template** (`encounter_templates/rmg_*.json`) — a grid stamp the RMG places for a guarded
encounter: `width`/`height`, `guards`, `buildings` (`interaction`, `position`), `pickups`,
`entrances`, **`holeTiles`** (→ encounter holes), `tileContents` (row-major grid codes). Naming:
`rmg_<makeup>_<a_b>_[pickups_]encounter_<W>x<H>_<n>`. Never hand-edited.

**Object value economy** (`generator_config.json`). The `metaObjects[]` table sets each placeable
SID's gold value — the unit the zone `…ContentValue` budgets are spent in. Examples:
`random_item_common` 3500 · `random_item_rare` 7000 · `random_item_epic` 14000 ·
`random_item_legendary` 28000 · `random_hire_1` 4000 (guard 4000) … rising by tier. So a zone's
`guardedContentValue` ÷ object values ≈ how many objects it will hold.

## Extracted catalogs ([`lib/`](../lib))

The generator's curated C# lookup tables were extracted to JSON (see
[`lib/README.md`](../lib/README.md)):

- **`content_ids.json`** (120) / **`include_list_ids.json`** (36) — SID ↔ display-name maps. Records
  gotchas like `the_gorge` → "Carrion Pile", themed mine names, `altar_of_magic_1..4` → magic-school shrines.
- **`variant_mappings.json`** — the `variant` integer meanings:
  - `pandora_box` 0–27 (0–3 Gold, 4–7 Exp, 8–14 Units, 15–18 All-Stats, 19–22 Magic-School, 23–27 Spells T1–T5).
  - `dragon_utopia` 0–3 = Small/Medium/Large/Maximum guard. `monty_hall` 0–3 = Common/Rare/Epic/Legendary.
- <a id="34-placement-rule-helpers"></a>**`distance_presets.json`** — placement-rule distance bands:

  | Band | Min–Max | | Band | Min–Max |
  |---|---|---|---|---|
  | NextTo | 0.05–0.10 | | Far | 0.50–0.75 |
  | Near | 0.10–0.25 | | VeryFar | 0.75–0.90 |
  | Medium | 0.25–0.50 | | | |

  (Rule helpers: `RoadDistance`/`TownDistance`(MainObject `["0"]`)/`CrossroadsDistance`(band, weight);
  `RemoteFoothold(castleCount)` = the canonical spawn-zone foothold item.)
- **`content_count_limit_defaults.json`** (45) — the default per-SID `maxCount` caps the generator
  applies to neutral zones (e.g. `market` 1, `pandora_box` 4, `point_of_balance` 3, `black_tower` 0).
- **`generator_constants.json`** — scaling formula, density multipliers, border-guard bases, balanced
  ring radii, tier ranks, and the neutral-quality profiles below.
- **`known_values.json`**, **`bannable_items.json`** (152), **`bannable_magics.json`** (5),
  **`spells.json`** (78) — the enum/ban/spell catalogs (see [Part VI](#part-vi--value-catalogs)).

**Zone-tier content philosophy** (`ZoneContentManager`, captured in `generator_constants.json`):
spawn/player → t2 pools + guaranteed starter mines + footholds; **Low** neutral → `zone_layout_sides`,
guardMult 1.1, t2 pools, lean (no utopias); **Medium** → `zone_layout_treasure_zone`, guardMult 1.4,
t3, banks + pandoras; **High** → `zone_layout_treasure_zone`, guardMult 1.8, t4/t5, the **only** tier
that spawns dragon utopias / unstable ruins / research labs. Castle-less zones strip `MainObject`
(near-castle) placement rules.

## Other resources

- [`templates/official/AnarchySmall.rmg.json`](../templates/official/AnarchySmall.rmg.json) — a smaller Anarchy variant
  not in the main official set (bundled extra variant).
- **Deployment.** The game loads templates from
Deploy path: see [`../install.md`](../install.md).
  (default library `C:\Program Files (x86)\Steam`). Ship `Name.rmg.json` **+** `Name.png`.

## Reference resolution map

```
zone.layout            → zone_layouts/*.json (or inline zoneLayouts)
zone.*ContentPool      → content_pools/*.json
   pool.includeLists   → content_lists/*.json
      list.sid         → ContentIds / engine object
zone.mandatoryContent  → INLINE in template
zone.contentCountLimits→ INLINE in template
*.sid + variant        → VariantMapping / engine
guarded encounters     → encounter_templates/rmg_*.json (engine-selected)
```

---

# Part VI — Value catalogs

Authoritative allowed-value lists from `KnownValues.cs` (broader than what the 56 templates use).

**Enums:**

| Field | Values |
|---|---|
| `gameMode` | `Classic`, `SingleHero` |
| `orientation.mode` | `MinimalBoundingSquare`, `BoundingCircle`, `None` |
| `mainObject.type` | `City`, `Spawn`, `AbandonedOutpost`, `None`, `GladiatorArena` |
| `mainObject.placement` | `Uniform`, `Center`, `Connection`, `NearZone` |
| `mainObject.spawn` | `Player1` … `Player8` |
| `faction.type` / biome `.type` | `None`, `Match`, `FromList`, `MatchMainObject`, `MatchZone` |
| `connectionType` | `Direct`, `Default`, `Portal`, `Proximity`, `GladiatorArena` |
| road `.type` | `Stone`, `Dirt` (or omitted) |
| reference / rule `.type` | `MainObject`, `Connection`, `Crossroads`, `MandatoryContent`; rules add `Road`, `Sid` |
| `gatePlacement` | `Center` |
| `diplomacyModifier` | `-0.5`, `-0.25` |
| `guardReactionDistribution` | 6-int array; common `[1,1,4,4,2,1]`, `[3,2,0,0,0,0]`, `[2,2,1,1,0,0]`, `[120,60,20,10,4,0]` |
| `bonus.receiverFilter` | `start_hero`, `all_heroes` |
| `winConditions.championSelectRule` | `StartHero` |
| `border.waterType` | `water grass` |

**Win conditions** (`displayWinCondition`): `win_condition_1` Standard (classic only) ·
`win_condition_3` Lost Starting City (`lostStartCity`) · `win_condition_5` Hold City (`cityHold`) ·
`win_condition_6` Tournament (`tournament`, 2P). `win_condition_4` (Gladiator Arena) defined but
commented out.

**Map sizes:** official `64,80,96,112,128,144,160,176,192,208,240`; experimental `256…512` step 16.

**`zone.layout` (full set):** `zone_layout_ai_spawn`, `_back`, `_center`, `_center_zone`, `_leaf`,
`_player_spawn`, `_second_spawn`, `_side_spawn_zone`, `_side_zone`, `_sides`, `_spawn`, `_spawns`,
`_start_zone`, `_supertreasure_zone`, `_treasure`, `_treasure_zone`, `_treasures`, `_wincondition_zone`.

**`buildingsConstructionSid`:** `default`, `extra_poor`/`poor`/`medium`/`rich`/`extra_rich`/`ultra_rich`,
`army`/`siege`, `arcade`/`massacre`/`chosen_one` (several with `_up_1..3`) — all `_buildings_construction`.

**`bonus.sid`:** `add_bonus_hero_item`, `add_bonus_hero_spell`, `add_bonus_hero_stat`,
`add_bonus_hero_unit_multipler`, `add_bonus_res`.

**Object/encounter SIDs** (`valueOverrides`, pools, mandatory content; ≈70 in `KnownValues.ObjectSids`):
`dragon_utopia`, `unstable_ruins`, `point_of_balance`, `boreal_call`, `jousting_range`,
`petrified_memorial`, `the_gorge`, `unforgotten_grave`, `ritual_pyre`, `pandora_box`, `prison`,
`arena`, `university`, `market`, `tavern`, `stables`, `watchtower`,
`mine_{gold,ore,wood,crystals,mercury,gemstones}`, `alchemy_lab`,
`random_item_{common,rare,epic,legendary}`, `random_hire_1..7`, `remote_foothold`, …

**Ban catalogs:** `KnownValues.BannableItems` (artifacts grouped Movement/Diplomacy/Combat/Magic/Misc/Set),
`BannableMagics` (spells), `KnownSpells` (full learnable library: id, name, school, tier) — the ID
source for `globalBans` and spell/town-portal bonuses.

---

# Part VII — Authoring & validation checklist

A complete template = `Name.rmg.json` + `Name.png`. Verify (see
[`../tools/validate_rmg.py`](../tools/validate_rmg.py)):

- [ ] Parses as JSON (tolerate trailing commas / BOM).
- [ ] `sizeX == sizeZ`; size is an accepted value.
- [ ] All required top-level keys present (incl. empty `contentPools`/`contentLists`).
- [ ] `gameRules` + `winConditions` complete; `displayWinCondition` matches the flags set.
- [ ] Each variant has `zones` and `connections`.
- [ ] Spawns are exactly `Player1`…`PlayerN` for an N-player template; no unintended duplicates.
- [ ] **Isolation (if intended):** no `Direct`/`Default`/`Portal` connection links zones hosting
      *different* players.
- [ ] Every `zone.layout` resolves (inline `zoneLayouts` or engine default); every `mandatoryContent`
      / `contentCountLimits` reference resolves to a pack defined **inline** in the same file.
- [ ] Connection `from`/`to` and all road/rule references name real zones/objects/connections.
- [ ] Per-zone tuning applied across **all** variants.
- [ ] Pretty-printed to match repo formatting; PNG sidecar present.

> Pool/list/building SIDs and localization keys reference **external** game data and can't be verified
> from the template alone — spell them against a known-good template or the [`data/`](../data) catalogs.

---

# Appendix — source file pointers

The generator project has been removed; its durable knowledge lives in this repo. (Original C#
locations are noted in parentheses for provenance.)

| Topic | Location in this repo |
|---|---|
| Official templates (+ PNG previews) | [`templates/official/`](../templates/official) |
| Bundled extra template | [`templates/official/AnarchySmall.rmg.json`](../templates/official/AnarchySmall.rmg.json) |
| Value/ban/spell catalogs | [`lib/known_values.json`](../lib/known_values.json), `bannable_items.json`, `bannable_magics.json`, `spells.json` *(from `Models/Unfrozen/KnownValues.cs`)* |
| Object SID/name maps | [`lib/content_ids.json`](../lib/content_ids.json), `include_list_ids.json` *(from `SidMapping.cs`)* |
| Variant meanings, presets, caps, constants | [`lib/`](../lib) `variant_mappings.json`, `distance_presets.json`, `content_count_limit_defaults.json`, `generator_constants.json` |
| External content data | [`data/`](../data) `{content_pools,content_lists,zone_layouts,encounter_templates}/` + `generator_config.json`, `generator_stats_config.json`, `generator_environment_assets.json` |
| Catalog index | [`lib/README.md`](../lib/README.md) |
| Structural validator | [`tools/validate_rmg.py`](../tools/validate_rmg.py) |
| Anarchy 8P/240 validator | [`tools/validate_template.py`](../tools/validate_template.py) |
| JSON model / pipeline / preview / tests | documented in this file (Parts II–IV) *(from `Models/Unfrozen/*.cs`, `Services/TemplateGenerator.cs`, `TemplatePreviewPngWriter.cs`, `…Tests/TemplateGeneratorTests.cs`)* |
