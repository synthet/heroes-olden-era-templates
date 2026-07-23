# Max-Size 8-Player Co-op Template Set

17 templates, all **240×240** (max map size) and **8 players** (max), tuned for **2 human co-op +
6 FFA AI** with **classic win only** on every map. Seat humans on **Player1** and **Player2**
(maximally separated spawns; **Spawn-A** / **Spawn-E** on Hub, Ring Ladder, Double Ring, and Twin Isles;
**Spawn-1** / **Spawn-2** on Trident); Players 3–8 as AI. Each name reflects its **topology**.

**Balance reference:** [Matrix](Matrix.rmg.json) — flat role budgets, yellow/orange/red
connection guards (15k / 35k / 85k), rich spawn mandatory (hire 1–7 + market/tavern), wiki fairness
caps. Other templates keep their zone graphs but share that methodology via
`tools/max8/normalize_max8_to_matrix.py` (family-scaled).

```bash
python tools/max8/build_max8_neutral_packs.py   # themed location packs
python tools/max8/build_max8_bank_limits.py     # per-zone bank caps catalog
python tools/max8/normalize_max8_to_matrix.py   # Matrix economy + guards + spawn MC
python tools/max8/apply_max8_pacing_tweaks.py   # spawn profile sync + wiki caps (no budget trim)
python tools/max8/apply_max8_coop_classic.py    # classic win + co-op seats + PvE tuning
python tools/max8/apply_max8_ai_coop_ease.py    # mild AI spawn nerf + gate ×1.25 (run last)
# Full rebuild from official bases (includes normalize + Ring custom topology):
python tools/max8/rescale_max8_economy.py
# Ring fully-buffered flanks only:
python tools/max8/build_ring_buffered.py
# Bilateral hourglass 5→4→3→2→1←2←3←4←5 (HAND_PACKAGED):
python tools/max8/build_hourglass.py
# Trident: co-op shaft + three AI tines; Portal@150k (HAND_PACKAGED):
python tools/max8/build_trident.py
# Ring Ladder: 32-zone 3-regular circular ladder (HAND_PACKAGED):
python tools/max8/build_prism.py
# Double Ring: 32-zone 4-regular K4 necklace (HAND_PACKAGED):
python tools/max8/build_lattice.py
# Mesh typed mid prizes (HAND_PACKAGED):
python tools/max8/ring_neutral_diversity.py
```

Audit spawn/center economy bands: `python tools/max8/analyze_economy_density.py --matrix` (writes
[`../../content/catalogs/max8_macro_audit.json`](../../content/catalogs/max8_macro_audit.json)). Authoring metadata:
[`../../content/catalogs/max8_design_meta.json`](../../content/catalogs/max8_design_meta.json).
Fairness caps: [`../../content/catalogs/max8_wiki_fairness_caps.json`](../../content/catalogs/max8_wiki_fairness_caps.json).

After rewire, pools must stay on **Expanse engine SIDs** (never `content_pool_max8_*`). Fill roads
after topology edits: `python tools/max8/fill_max8_roads.py`. PNG previews:
`python tools/preview/render_preview.py content/templates/max8`.

All 17 **PASS** `python tools/validate/validate_rmg.py content/templates/max8`.

| Template | Base (size) | Topology |
|---|---|---|
| **Ring** | Diamond (144, rewired) | Fully buffered ring — every spawn CW+CCW flanks; typed prizes (Magic/Connector/Deep); hard AI exits (32 zones) |
| **Ring Ladder** | Ring (240, rewired) | Circular ladder Y16 — outer spawn/buffer + inner typed lean/rich ring (Might/Magic/Side/…) + spokes; every zone degree 3 (32 zones) |
| **Double Ring** | Ring (240, rewired) | 4-regular K4 necklace — Ring Ladder + sector diagonals; every zone degree 4 (32 zones) |
| **Mesh** | Diamond (144) | Dense bipartite mesh; typed mid prizes (Magic/Connector/Deep) (16 zones) |
| **Star** | Ikarus (160, rewired → hand) | Max-hop star: Spawn → Outer → Inner → `Center` (25 zones) |
| **Web** | Ikarus (160, deepened) | Dual-rim web: Treasure + Inner axes (25 zones) |
| **Twin Fans** | Boomerang (144, rewired) | Mirrored twin wings; Elbow-W/E gate `Center` (19 zones) |
| **Target Core** | Spider (208) | Concentric bullseye: 8 radial legs + treasure mid-ring + 4 Buffer gates into 4 SuperTreasure; Buffer ring (24 zones) |
| **Playoff Tree** | Expanse (192) | Playoff tree 8→4→2→1 + unpredictable random-pool Leaf-1..8 farm pockets (23 zones); steeper round guards |
| **Hub** | OctoJebus (240, rewired) | Dense equal-ray star: 8 identical Spawn→Inner seats + 7 diverse filler rays → fat `Center` (31 zones) |
| **Triple Hub** | hand lattice (240) | Three identical 3×3 blocks (hub-adjacent P1/P2) + unpredictable random-pool Gate-W/M/E + four magic schools; triangle Portals Gate↔Gate @ 150k (30 zones) |
| **Twin Wings** | Twin Fans (rewired) | Twin butterfly lobes; 4 mirrored random-pool interior zones; Portal Treasure-A↔G (150k) (24 zones) |
| **Twin Blocks** | Twin Fans (rewired) | Twin 4×4 blocks with typed mids (Might/Magic/Side/Outer/Connector); 4 random-pool interiors; Portal Treasure-A↔G (150k) (32 zones) |
| **Twin Loop** | Twin Fans (rewired) | Twin Loop racetrack: N/S Buffer gates → Hub → deep prize; dual Portals close the central loop @ 150k (24 zones) |
| **Matrix** | hand lattice (240) | 5×5 lattice — A-N home↔Spawn-N; B mid + Center; C magic schools; red Portals |
| **Hourglass** | hand lattice (240) | Bilateral hourglass 5→4→3→2→1←2←3←4←5 — 4 spawns + Rim gate per arc; guards rise 15k/35k/50k/85k into Final (29 zones) |
| **Trident** | hand lattice (240) | Co-op shaft Portal Gate-W↔E @150k; Buffer→Might→Magic spines; Deep shields meshed + Center; three AI tines on Might/Magic/Gate hosts (31 zones) |

All maps share the same co-op rules shell via `tools/max8/apply_max8_coop_classic.py` (classic win,
PvE guard multiplier 0.85, diplomacy −0.5, antipodal Player1/Player2 assignment), then
`tools/max8/apply_max8_ai_coop_ease.py`: AI (P3–P8) spawn budgets at **60–80%** of human (closer hop
to P1/P2 → leaner), near/mid/far AI mandatory kits (curios / low hires; fewer mines), and connection
`guardValue` **×1.25** (15k→18750, 35k→43750, 50k→62500, 85k→106250, 150k→187500). Re-run the ease pass after
any HAND_PACKAGED rebuild.

Twin-wing Twin Fans: `python tools/max8/build_wings.py` (also via `rework_max8_variants.py`). Regenerate Hub max-hop star:
`python tools/max8/build_hub_arms.py`. Star max-hop chains: `python tools/max8/build_star.py`. Web dual rims: `python tools/max8/build_web.py`. Twin Isles set (Twin Wings / Twin Blocks / Twin Loop):
`python tools/max8/build_twins_set.py`. Triple Hub: `python tools/max8/build_triad.py`.
Trident: `python tools/max8/build_trident.py`.
Ring Ladder circular ladder: `python tools/max8/build_prism.py`.
Double Ring 4-regular necklace: `python tools/max8/build_lattice.py`.
Mesh typed mid prizes: `python tools/max8/ring_neutral_diversity.py`.

**Diversity:** Distinct zone graphs across the max8 set. Topologies: ring, ring ladder (3-regular
ladder), double ring (4-regular K4 necklace), mesh, star, web,
twin fans, bullseye, playoff tree, spoke hub, triple hub,
twin-isle twin wings/twin blocks/twin loop, and the **Matrix** 5×5 lattice.

**Neutral content:** each mid-map neutral zone (Treasure, Buffer, Connector, SuperTreasure leg) gets a
**themed location** mandatory pack from [`../../content/catalogs/max8_neutral_packs.json`](../../content/catalogs/max8_neutral_packs.json).
Packs group objects into cohesive settings (ArcaneSanctuary, WarCamp, TradePost, MiningOutpost, HeroShrine)
with biome-matched banks, altars, dwellings, mines, weekly storages, and power-ups. Assignment is
biome-aware via `tools/max8/diversify_max8_neutrals.py`; peer zones stay value-balanced. Procedural fill must
reuse **engine-known** pool SIDs (Expanse / official families) — never invent `content_pool_max8_*`
(breaks MapGen; see `docs/LESSONS_LEARNED.md`). **Per-zone bank caps** (`maxCount: 1` per bank type)
come from [`../../content/catalogs/max8_bank_limits.json`](../../content/catalogs/max8_bank_limits.json). Center/hub zones get a themed
refresh; **Hub** uses the full official OctoJebus center grid via `centerOverrides`.
**Matrix** is hand-packaged (`tools/max8/build_matrix_map.py`) — A-N packs match Spawn-N biome/faction;
C-1..4 are Nightshade/Daylight/Primal/Arcane school packs. **Triple Hub** is hand-packaged
(`tools/max8/build_triad.py`) — three identical 3×3 blocks (30 zones); A-homes, Mid war camps,
Nightshade/Daylight/Primal/Arcane schools; Hub-W/M/E behind procedural random-pool Gate-W/M/E; triangle Portals
Gate↔Gate @ 150k. **Playoff Tree** is hand-packaged
(`tools/max8/build_bracket.py`) — playoff 8→4→2→1 plus unpredictable random-pool Leaf-1..8 farm pockets (23 zones). **Hub** is hand-packaged (`tools/max8/build_hub_arms.py`) —
dense equal-ray star (8 identical Spawn→Inner seats + 7 diverse Tip→Gate fillers → Center). **Star** is hand-packaged
(`tools/max8/build_star.py`) — Spawn → Outer → Inner → Center (25 zones) with Yellow/Orange/Red guards.
**Web** is hand-packaged (`tools/max8/build_web.py`) — Treasure-1..8 ring + Inner-1..8 axes rim; guards escalate inward Yellow/Orange/Scarlet/Red.
**Hourglass** is hand-packaged (`tools/max8/build_hourglass.py`) — Rim and Mid payloads are fully
procedural from official Expanse pools; WarCamp west / utility east Lows; ArcaneSanctuary Deeps;
Final center prize.
**Trident** is hand-packaged (`tools/max8/build_trident.py`) — co-op shaft with Portal@150k;
three AI tines off a Deep-shield core; maximizes hop distance from P1/P2 to each AI.
**Ring Ladder** is hand-packaged (`tools/max8/build_prism.py`) — 32-zone 3-regular circular ladder
(outer spawn/buffer + inner typed lean/rich ring + spokes); single `AbandonedOutpost` per neutral;
unique themed packs via `ring_neutral_diversity.py`.
**Double Ring** is hand-packaged (`tools/max8/build_lattice.py`) — Ring Ladder + sector diagonals
(Spawn↔rich typed, Buffer↔lean typed); every zone degree 4 (64 Direct).
**Mesh** is hand-packaged (`tools/max8/ring_neutral_diversity.py`) — bipartite mesh with typed
mid prizes and single outpost per neutral.
Do **not** run `diversify_max8_neutrals.py`, `rewire_max8_pools.py`, or
`normalize_max8_to_matrix.py` on Matrix / Playoff Tree / Hub / Ring / Triple Hub / Hourglass / Trident / Star / Web / Ring Ladder / Double Ring / Mesh (HAND_PACKAGED).
Near-dupe check: `python tools/max8/topology_fingerprint.py content/templates/max8`.

**Co-op fairness:** see [`../../docs/oe/coop-fairness-review.md`](../../docs/oe/coop-fairness-review.md).

## Player picker guide (macro tier + co-op)

All maps: **classic win**, **co-op tier A**. Ally Player1 + Player2; seat six AI on Player3–8.

| Template | Macro tier | Contact | Co-op seats |
|---|---|---|---|
| **Ring** | Lean | Slow | P1/P2 antipodal (auto) |
| **Ring Ladder** | Lean | Slow | P1/P2 on Spawn-A / Spawn-E |
| **Double Ring** | Lean | Medium | P1/P2 on Spawn-A / Spawn-E |
| **Mesh** | Standard | Medium | P1/P2 antipodal (auto) |
| **Star** | Lean | Slow | P1/P2 on Spawn-A / Spawn-E |
| **Web** | Lean | Slow | P1/P2 antipodal (auto) |
| **Twin Fans** | Dense | Medium | P1/P2 antipodal (auto) |
| **Target Core** | Dense | Medium | P1/P2 antipodal (auto) |
| **Playoff Tree** | Standard | Medium | P1/P2 on Spawn-1 / Spawn-8 |
| **Hub** | Standard | Slow | P1/P2 on Spawn-A / Spawn-E |
| **Triple Hub** | Standard | Slow | P1/P2 on W-S1 / E-S2 (triangle portals) |
| **Twin Wings** | Standard | Slow | P1/P2 on Spawn-A / Spawn-E (portal) |
| **Twin Blocks** | Standard | Slow | P1/P2 on Spawn-A / Spawn-E (portal) |
| **Twin Loop** | Standard | Slow | P1/P2 on Spawn-A / Spawn-E (dual portal) |
| **Matrix** | Standard | Medium | P1/P2 antipodal (Spawn-1 / Spawn-2) |
| **Hourglass** | Standard | Slow | P1/P2 on Spawn-1 / Spawn-8 (opposite arcs) |
| **Trident** | Standard | Slow | P1/P2 on Spawn-1 / Spawn-2 (Portal@150k) |

Lobby: pick any max8 template → seat two humans on Player1/Player2 → ally them → six AI on 3–8.

### Preview legend

Sidecar `.png` previews: **green** discs = spawn order (1 = Player1 seat, 2 = Player2 seat);
bronze + swords = Might arms; violet + gem = Magic arms; blue **H** = hub / hold city.

## Pacing families (Matrix-scaled)

Topology unchanged; economy uses Matrix role ladder × family factor (flat budgets, `*PerArea` = 0):

| Family | Templates | Factor | Spawn GCV target |
|---|---|---:|---:|
| **Lean** | Ring, Ring Ladder, Double Ring, Web, Star | 0.75× | ~338k |
| **Standard** | Mesh, Playoff Tree, Hub, Triple Hub, Twin Wings, Twin Blocks, Twin Loop, Matrix, Hourglass, Trident | 1.0× | 450k |
| **Dense** | Target Core, Twin Fans | 1.25× | ~563k |

Matrix role ladder (× factor): Spawn 450k → mid/Treasure 550k → junction/Connector 650k →
deep/SuperTreasure 900k → Center 1.0M. Base guards banded **15k / 35k / 85k** (`wi` 0.15), then
`apply_max8_ai_coop_ease.py` raises connection gates **×1.25**. Mid neutrals
use `AbandonedOutpost` (not City); human spawns carry City + Matrix spawn MC; AI spawns use lean
near/mid/far kits from `apply_max8_ai_coop_ease.py`.

**Win conditions (all 17):** `classic` only — no hold-city, no lost-start-city, no encounter holes.
Applied by `tools/max8/apply_max8_coop_classic.py`.

- **Matrix** — 5×5 lattice (25 zones); yellow 15K / orange 35K Direct; red 85K Portals into Center
- **Triple Hub** — three identical 3×3 blocks + Gate-W/M/E (30 zones); every block runs a
  school–Hub axis with corner spawns; co-op P1/P2 sit hub-adjacent on the south slot (Mid's south
  slot holds the Primal school); yellow 15K / orange 35K Direct inside blocks; triangle Portals
  Gate-W↔Gate-M↔Gate-E at **150k** (hubs one hop behind); Gate payloads are fully procedural from
  official connector pools. Regenerate: `python tools/max8/build_triad.py`.
- **Playoff Tree** — playoff tree 8→4→2→1 with unpredictable random-pool Leaf-1..8 farm pockets (23 zones); yellow 15K /
  orange 50K Direct; red 150K Portals into Final; rich spawn mandatories (hire 1–7 + mills);
  regenerate with `python tools/max8/build_bracket.py` then `apply_max8_coop_classic`.
- **Hourglass** — bilateral hourglass 5→4→3→2→1←2←3←4←5 (29 zones); each outer arc holds 4 spawns +
  1 neutral Rim; Rim/Mid content is random-pool generated; guards rise 15K / 35K / 50K / 85K
  Direct into Final; economy ladder
  Spawn 450k → Rim 500k → Low 550k → Mid 650k → Deep 900k → Final 1.0M. Regenerate with
  `python tools/max8/build_hourglass.py` then `apply_max8_coop_classic`.
- **Trident** — co-op shaft Spawn-1/2 (31 zones); Portal Gate-W↔Gate-E @ **150k**;
  Buffer→Might→Magic spines into Center; Deep-1/2/3 shields mesh to each other and Center;
  three AI tines on Might-1 / Magic-1 / Gate-S with Outer leaves. Regenerate: `python tools/max8/build_trident.py`.
- **Ring Ladder** — circular ladder Y16 (32 zones); every zone path-degree 3 (48 Direct); outer
  Spawn/Buffer ring + inner typed lean/rich ring (Might/Magic/Side/Connector/Outer/Deep) + spokes;
  AI red flanks toward P1/P2. Regenerate: `python tools/max8/build_prism.py`.
- **Double Ring** — Ring Ladder + sector diagonals (32 zones / 64 Direct); every zone degree 4.
  Regenerate: `python tools/max8/build_lattice.py`.
- **Twin Isles (Twin Wings / Twin Blocks / Twin Loop)** — two disconnected 4-player
  figures (Twin Wings/Twin Loop 24 zones, Twin Blocks 32); yellow 15K leaves, orange 35K into Hub; West↔East only via Portal(s)
  at **150k**. Regenerate: `python tools/max8/build_twins_set.py`.

Spawn content (all non-Matrix via normalize + spawn profile):

- **Mandatory per spawn:** watchtower, wood/ore mines, `random_hire_1`–`7`, market, tavern, mana well,
  storage_wood, common item.
- Utopia-tier / unfair objects capped by role (`max8_wiki_fairness_caps.json`): utopia / mirage /
  wind_rose / black_tower banned on spawn; utopia allowed on deep/center only.
- Each **bank type** capped at 1 per zone (spawn and neutral).
- Hub additionally drops mandatory spawn utopia SIDs; Center keeps OctoJebus multi-city layout.

**Deploy:** [`../../docs/install.md`](../../docs/install.md). Smoke-test in-game after deploy.
