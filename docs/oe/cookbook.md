# Olden Era Template Cookbook — building a `.rmg.json` from scratch

A practical, parameter-driven how-to for authoring new Olden Era random-map templates, including
porting legacy **Heroes 3 (HotA)** tournament templates. This is the *recipe* book; for the exact
field semantics see the spec [`rmg-format.md`](rmg-format.md), and for lookup data
see [`../../lib/`](../../lib) and [`../../data/`](../../data).

> **The deliverable.** A template is two files sharing a basename: `Name.rmg.json` (+ `Name.png`
> preview). Deploy to
> Deploy path: see [`../install.md`](../install.md).

---

## Contents

1. [The 7-step recipe](#1-the-7-step-recipe)
2. [Parameter tables (size, players, economy, guards)](#2-parameter-tables)
3. [Pick a topology + a base to clone](#3-pick-a-topology--a-base-to-clone)
4. [Building the zone graph](#4-building-the-zone-graph)
5. [Wiring economy & content](#5-wiring-economy--content)
6. [Rules, bans, bonuses](#6-rules-bans-bonuses)
7. [Validate, preview, deploy](#7-validate-preview-deploy)
8. [Recipes by scenario](#8-recipes-by-scenario)
9. [Porting Heroes 3 tournament templates](#9-porting-heroes-3-tournament-templates)
10. [Pitfalls & checklist](#10-pitfalls--checklist)
11. [Reference index](#11-reference-index)

---

## 1. The 7-step recipe

1. **Choose parameters** — players (2–8), map size, topology, FFA vs teams, isolation, win
   condition. → [§2](#2-parameter-tables)
2. **Pick the closest existing template as a base** and copy it — never start from a blank file.
   → [§3](#3-pick-a-topology--a-base-to-clone)
3. **Edit identity** — `name`, `description`, `displayWinCondition`, `sizeX`/`sizeZ`.
4. **Reshape the zone graph** — zones (spawns + neutrals) and connections; enforce isolation if
   wanted. → [§4](#4-building-the-zone-graph)
5. **Set economy & content** — per-zone `…Value`/`…ValuePerArea`, content pools, mandatory packs,
   count limits. → [§5](#5-wiring-economy--content)
6. **Set rules** — `gameRules`, win condition flags, bonuses, bans, value overrides.
   → [§6](#6-rules-bans-bonuses)
7. **Validate → preview → deploy.** → [§7](#7-validate-preview-deploy)

Golden rule: **clone-and-mutate**. Every official template is a working, engine-validated fixture in
[`../../templates/official/`](../../templates/official); start from the one nearest your target.

---

## 2. Parameter tables

### 2.1 Map size

OE map is square (`sizeX == sizeZ`). Official sizes: `64,80,96,112,128,144,160,176,192,208,240`
(experimental to 512). Rough capacity and the H3 size code it corresponds to in the ports:

| OE px | H3 size code | Typical zones | Typical players | Example OE templates |
|------:|---|---:|---|---|
| 64–96 | S / M (`M-U`, 200%) | 4–8 | 2 | Blitz, Sprint, `h3-port/2sm2c(2)`, `Skirmish(M)` |
| 112–128 | M / L | 8–14 | 2–4 | Kerberos (128) |
| 144–160 | L (`L±U`) | 14–18 | 2–8 | Diamond (144), Mini-Nostalgia (144), Jebus Cross (160), Anarchy (160) |
| 176–208 | XL (`XL±U`) | 20–30 | 4–8 | Spider (208), `h3-port/Nostalgia/6lm10a/8mm6a/8xm12a` (208) |
| 240 | max / G | up to 32 | 8 | OctoJebus (240), Full Hire |

> H3 size letters: S=36, M=72, L=108, XL=144, H=180, XH=216, G=252 tiles; `+U` = two levels
> (underground), `-U` = single level. OE has one level, so the ports map H3 size → an OE px bucket
> (M→96, L→144/160, XL→208) rather than 1:1 tiles.
> **Hard cap: 32 total zones** (so max neutrals = `32 − players`). Warn if a zone's area
> (`px² / zones`) drops below ~1024 tiles — zones get cramped.

### 2.2 Player count → topology

| Players | Good topologies | Notes |
|---|---|---|
| 2 | Jebus hub (2 spawns + center), Chain, mirrored | Classic 1v1; PG-gated center treasure. |
| 3–4 | Ring, Diamond, Hub | Even spacing; ring keeps adjacency fair. |
| 6 | Ring, Spider, Kerberos-style connectors | |
| 8 | Hub (OctoJebus), Ring, Web, Balanced concentric | 8 spawns + neutral buffer. |
| 2v2 / teams | Mirror with ally zones **not** directly linked (`mt_TeamJebus`) | Use ownership + isolation. |

### 2.3 Economy scaling

Per-zone budgets have a flat `…Value` and an area-scaled `…ValuePerArea` (per channel: guarded /
unguarded / resources). When resizing a base template, **scale per-area budgets by ≈ `(newPx/oldPx)²`**
(the generator uses `contentScale = clamp(sqrt(zoneArea/6400), 0.5, 2.5)`, `zoneArea = px²/zones`).
Object gold values (so a budget ≈ N objects) are in [`../../data/generator_config.json`](../../data/generator_config.json):
`random_item_common` 3500 · `rare` 7000 · `epic` 14000 · `legendary` 28000 · `random_hire_1` 4000…

Neutral-tier guard profiles (from [`../../lib/generator_constants.json`](../../lib/generator_constants.json)):

| Tier | layout | guardMultiplier | pools | primary city guard |
|---|---|---:|---|---:|
| Low | `zone_layout_sides` | 1.1 | t2 | 4 000 |
| Medium | `zone_layout_treasure_zone` | 1.4 | t3 | 8 000 |
| High | `zone_layout_treasure_zone` | 1.8 | t4/t5 | 16 000 |

### 2.4 Border / pathfinder guards (the gateway to a zone)

Connection `guardValue` gates movement between zones. OE generator bases (× `BorderGuardStrength%`):

| Edge | OE base | H3 "PG" reference (from official `.h3t`) |
|---|---:|---|
| Player ↔ Player | 30 000 | Jebus Cross 45 000; mt_* 45 000 |
| Player ↔ Neutral low/med/high | 15 000 / 20 000 / 25 000 | 2sm2c 12 500–20 000; Kerberos 12 000–25 000 |
| Portal | 25 000 | — |
| Center super-treasure | 50 000–70 000 (OctoJebus 70 000, Jebus center 55 555–66 666) | Clash of Dragons up to 180 000 |

> H3 PG values per official template are tabulated in
> [`../../h3/layouts/official/README.md`](../../h3/layouts/official/README.md). OE
> tends to guard a little harder than H3; tune for parity if porting competitively.

---

## 3. Pick a topology + a base to clone

| You want… | Clone this base | Why |
|---|---|---|
| 2-player Jebus (hub + guarded center) | `Jebus Cross.rmg.json` / `Jebus Cross Classic` | 5 zones, center super-treasure, 2 spawns. |
| 8-player isolated FFA | `OctoJebus.rmg.json` | 8 spawns each linked **only** to neutral `Center`. |
| 8-player diamond/symmetric | `Diamond.rmg.json` / `Mini-Nostalgia` | 16/15 zones, even spawns. |
| 6–8 player spider/branched | `Spider.rmg.json` | 24 zones, XL. |
| Chaos / encounter-holes | `Anarchy.rmg.json` | `encounterHoles:true`, anarchy pools, value overrides. |
| Connector-web 6p | `Kerberos.rmg.json` | spawn + connector zones. |
| Fast 1v1 small | `Blitz` / `Sprint` | M-size, lean. |

Copy the file, rename to `YourName.rmg.json`, then edit. The 56 bases live in
[`../../templates/official/`](../../templates/official); the 20 H3 tournament scaffolds in
[`../../templates/h3-port/`](../../templates/h3-port).

---

## 4. Building the zone graph

A variant is `{ orientation, zones[], connections[] }`. (Full field semantics: spec
[§2.6–2.8](rmg-format.md#26-zone-object-graph-node).)

**Zones** — one per player spawn (`mainObjects[0]` = `{ "type":"Spawn", "spawn":"PlayerN" }`) plus
neutral zones. Naming convention: `Spawn-A…H`, `Center`, `Treasure-N`, `Side-X`, `Connector-N`.

**Connections** — `from`/`to` are zone **names**; `connectionType` is the key lever:

- `Direct` / `Default` — a real, guarded passage (set `guardValue`).
- `Portal` — teleport link (`portalPlacementRules{From,To}`).
- `Proximity` — **spacing hint only, not a path** (`length`).

**Isolation (FFA "no rush" / teams):** ensure **no `Direct`/`Default`/`Portal` connects two zones
hosting *different* players.** Route every spawn only to neutral zones (the OctoJebus pattern). Same
player's alternate-spawn zones and `Proximity` rival edges are fine. The validator enforces this.

**Roads** connect *references inside a zone* (`MainObject` index, `Connection` name, `Crossroads`),
typed `Stone`/`Dirt`. Remember `mainObjects` are indexed positionally — don't reorder.

---

## 5. Wiring economy & content

Per zone set the three budget channels and point at content pools:

```jsonc
"guardedContentValue": 750000, "guardedContentValuePerArea": 10000,   // scale per-area by (px/160)^2
"unguardedContentValue": 250000, "unguardedContentValuePerArea": 0,
"resourcesValue": 300000, "resourcesValuePerArea": 0,
"guardedContentPool":   ["template_pool_<tpl>_guarded_start_zone"],
"unguardedContentPool": ["template_pool_<tpl>_unguarded_start_zone"],
"resourcesContentPool": ["content_pool_general_resources_start_zone_rich"],
"mandatoryContent":  ["mandatory_content_spawn"],   // defined INLINE (see below)
"contentCountLimits":["content_limits_spawn"]        // defined INLINE
```

- **Pools** are *external* SIDs resolved from [`../../data/content_pools/`](../../data/content_pools)
  (e.g. `template_anarchy_pools.json`, `template_octojebus_pools.json`, tiered `random_pools/`).
  Reuse a base template's pool family, or point at `content_pool_default_*`.
- **`mandatoryContent` / `contentCountLimits`** are defined **inline** in your file (top-level arrays)
  and referenced by name. Use the generator's sensible **default caps** as a starting point:
  [`../../lib/content_count_limit_defaults.json`](../../lib/content_count_limit_defaults.json)
  (e.g. `market` 1, `pandora_box` 4, `point_of_balance` 3, `university` 2).
- **Placement `rules`** position mandatory objects by distance band — use
  [`../../lib/distance_presets.json`](../../lib/distance_presets.json): NextTo 0.05–0.10,
  Near 0.10–0.25, Medium 0.25–0.50, Far 0.50–0.75, VeryFar 0.75–0.90, against `Road`/`MainObject ["0"]`/`Crossroads`.
- **Object & variant meanings:** [`../../lib/content_ids.json`](../../lib/content_ids.json)
  (SID→name) and [`../../lib/variant_mappings.json`](../../lib/variant_mappings.json)
  (`pandora_box` 0–27, `dragon_utopia` 0–3, `monty_hall` 0–3).
- **Tier philosophy:** only **High** neutral zones spawn dragon utopias / unstable ruins / research
  labs; **Low** zones stay lean. Castle-less zones strip near-castle (`MainObject`) rules.

---

## 6. Rules, bans, bonuses

```jsonc
"gameRules": {
  "heroCountMin": 5, "heroCountMax": 10, "heroCountIncrement": 1, "heroHireBan": false,
  "encounterHoles": false,           // true → Anarchy chaos mechanic
  "winConditions": { "classic": true, "desertion": true, "desertionDay": 3, "desertionValue": 3000,
                     "heroLighting": true, "heroLightingDay": 1, "lostStartHero": false }
}
```

- **Win condition** — set `displayWinCondition` + matching flags ([spec §VI](rmg-format.md#part-vi--value-catalogs)):
  `win_condition_1` Standard · `win_condition_3` Lost Starting City (`lostStartCity`) ·
  `win_condition_5` Hold City (`cityHold`+`cityHoldDays`) · `win_condition_6` Tournament (2P).
- **Bonuses** (`gameRules.bonuses`) — starting gold/spells/items: `add_bonus_res ["gold","10000"]`,
  `receiverSide:-1`, `receiverFilter:"start_hero"|"all_heroes"`.
- **`globalBans`** — `{ "items":[…], "magics":[…], "heroes":[…], "skills":[…] }`; ID catalogs in
  [`../../lib/bannable_items.json`](../../lib/bannable_items.json) (152),
  `bannable_magics.json`, `spells.json` (78).
- **`valueOverrides`** — globally retune POI guards (Anarchy uses 7: `point_of_balance` 7500,
  `the_gorge`/`boreal_call`/`jousting_range`/`petrified_memorial`/`unforgotten_grave`/`ritual_pyre` 6000).

---

## 7. Validate, preview, deploy

```bash
# General structural validator — use this for any template:
python tools/validate_rmg.py "templates/official/Your Name.rmg.json"
# Anarchy 8P/240 isolated-spawn checker only:
python tools/validate_template.py "templates/max8/Octo Anarchy.rmg.json"
```

- Fix until PASS. Known-good targets: exactly N `Player1..N` spawns, no rival-spawn `Direct` link,
  every `layout`/`mandatoryContent`/`contentCountLimits` reference resolves, `sizeX==sizeZ`.
- **PNG preview** — the game shows `Name.png` (parchment node-graph: numbered player discs, bronze/
  silver/gold neutral tiers, gold/blue connection lines — see [spec Part III](rmg-format.md#part-iii--reading-the-png-preview)).
  Generate via the Template Editor, or ship a placeholder.
- **Deploy** — see [`../install.md`](../install.md). Confirm zones/guards/isolation in-game after deploy.

---

## 8. Recipes by scenario

### A. N-player FFA at size X
Clone the size/player match from [§2.1](#21-map-size)/[§3](#3-pick-a-topology--a-base-to-clone) →
set `sizeX/sizeZ` → ensure N `Spawn-*` zones with `Player1..N` → scale per-area budgets by
`(X/oldPx)²` → validate.

### B. 2-player Jebus (hub + guarded center)
Clone `Jebus Cross.rmg.json`. Keep 5 zones (Center + 2 spawns + 2 sides). Center holds a
super-treasure city; gate `Spawn→Center` at 45 000–66 666. `win_condition_5` (hold center) optional.

### C. 8-player isolated (no-rush FFA / teams)
Clone `OctoJebus.rmg.json`. 8 `Spawn-*` each `Direct`-linked **only** to neutral `Center`; rival
spawns share no real edge. For 2v2, own ally zones and keep allies unlinked (`mt_TeamJebus`).

### D. Anarchy-style chaos
Clone `Anarchy.rmg.json`. Set `gameRules.encounterHoles:true`; add per-zone
`encounterHolesSettings:{affectedEncounters:0.66,twoHoleEncounters:0.66}`; copy the 7
`valueOverrides`; use `content_pool_anarchy_*` ([`../../data/content_pools/template_anarchy_pools.json`](../../data/content_pools/template_anarchy_pools.json)).

### E. Port an H3 tournament template
See [§9](#9-porting-heroes-3-tournament-templates).

---

## 9. Porting Heroes 3 tournament templates

The repo already contains a full H3 (HotA) cross-reference and 20 working scaffolds. To port:

1. **Find the H3 target** in [`../h3/matrix.md`](../h3/matrix.md)
2. **Read the H3 topology** in [`../../h3/layouts/official/`](../../h3/layouts/official/) (`*.topology.json`) and [`../../h3/layouts/official/README.md`](../../h3/layouts/official/README.md)
3. **Start from the scaffold** if one exists in [`../../templates/h3-port/`](../../templates/h3-port)
   (20 templates, all pass structural validation) — these already carry the H3 name, size, and
   description key; you hand-tune the zone graph to match the parsed `.h3t` topology.
4. **Tune to H3 parity** — set connection `guardValue` to the H3 PG (e.g. Jebus Cross 45 000), match
   zone richness, and apply per-zone object bans from h3hota where relevant.
5. **Mind the gaps** in [`../h3/tier1-audit.md`](../h3/tier1-audit.md):
   guards harder, adds extra connection lanes, and simplifies large H3 maps (e.g. Kerberos 33→13
   zones, Anarchy 12→5 variants). Decide faithful vs. OE-native.

**H3 size → OE px** (used by the ports): `M-U`≈96, `L±U`≈144/160, `XL±U`≈208.

**Tooling:** see [`../../tools/README.md`](../../tools/README.md). Official `.h3t` packs: [`../../h3/sources/official/`](../../h3/sources/official/); catalog: [`../h3/catalog.md`](../h3/catalog.md).

> Verified direct ports: **Diamond, Mini-Nostalgia, Spider** (topology/size align). Partial:
> **Jebus Cross** (OE harder PG + cityHold), **Kerberos** (smaller), **Anarchy** (5 vs 12 variants).

---

## 10. Pitfalls & checklist

- **Don't start blank** — clone a base; the engine schema is a superset few tools fully model.
- **Don't reorder `mainObjects`** — roads/biomes/rules reference them by index.
- **`Proximity` is not a path** — it only spaces zones; use `Direct` for real routes.
- **Isolation means *different* players** — same-player alt-spawn links and `Proximity` rival edges
  are allowed.
- **Inline vs external** — `mandatoryContent`/`contentCountLimits` are inline; pools/lists/layouts
  are external SIDs (`data/`). A typo'd inline reference fails validation; a typo'd pool SID does
  not (it's resolved at runtime) — spell against a known-good template.
- **Apply per-zone tuning to *every* variant.**
- **Ship the PNG.** A template with no preview shows blank/`?` in the picker.
- **Known typos to avoid** (present in some shipped files): `content_limits_spaws`, missing
  `content_limits_supertreasures` / `mandatory_content_yellow` — run `python tools/validate_rmg.py templates/` to catch these.

**Final checklist:** parses (BOM/trailing-comma tolerant) · `sizeX==sizeZ` & accepted · N spawns
`Player1..N` · isolation honored (if intended) · all inline refs resolve · per-area economy scaled ·
rules + win condition consistent · validator PASS · PNG present.

---

## 11. Reference index

See [`../README.md`](../README.md) for the full documentation map.
