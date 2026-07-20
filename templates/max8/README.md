# Max-Size 8-Player Co-op Template Set

11 templates, all **240×240** (max map size) and **8 players** (max), tuned for **2 human co-op +
6 FFA AI** with **classic win only** on every map. Seat humans on **Player1** and **Player2**
(maximally separated spawns — **Spawn-A** / **Spawn-B** on Corridor); Players 3–8 as AI.
Each name reflects its **topology**.

**Balance reference:** [Matrix Map](Matrix%20Map.rmg.json) — flat role budgets, yellow/orange/red
connection guards (15k / 35k / 85k), rich spawn mandatory (hire 1–7 + market/tavern), wiki fairness
caps. Other templates keep their zone graphs but share that methodology via
`tools/max8/normalize_max8_to_matrix.py` (family-scaled).

```bash
python tools/max8/build_max8_neutral_packs.py   # themed location packs
python tools/max8/build_max8_bank_limits.py     # per-zone bank caps catalog
python tools/max8/normalize_max8_to_matrix.py   # Matrix economy + guards + spawn MC
python tools/max8/apply_max8_pacing_tweaks.py   # spawn profile sync + wiki caps (no budget trim)
python tools/max8/apply_max8_coop_classic.py    # classic win + co-op tuning (run last)
# Full rebuild from official bases (includes normalize):
python tools/max8/rescale_max8_economy.py
```

Audit spawn/center economy bands: `python tools/max8/analyze_economy_density.py --matrix` (writes
[`../../content/catalogs/max8_macro_audit.json`](../../content/catalogs/max8_macro_audit.json)). Authoring metadata:
[`../../content/catalogs/max8_design_meta.json`](../../content/catalogs/max8_design_meta.json).
Fairness caps: [`../../content/catalogs/max8_wiki_fairness_caps.json`](../../content/catalogs/max8_wiki_fairness_caps.json).

After rewire, pools must stay on **Expanse engine SIDs** (never `content_pool_max8_*`). Fill roads
after topology edits: `python tools/max8/fill_max8_roads.py`. PNG previews:
`python tools/preview/render_preview.py content/templates/max8`.

All 11 **PASS** `python tools/validate/validate_rmg.py content/templates/max8`.

| Template | Base (size) | Topology |
|---|---|---|
| **Ring** | Diamond (144, rewired) | Buffered ring — neutral between every spawn (16 zones, diameter 8) |
| **Mesh** | Diamond (144) | Dense bipartite diamond grid (16 zones) |
| **Spokes** | Ikarus (160, rewired) | Spawn → treasure → central `Center` prize (17 zones) |
| **Wheel** | Ikarus (160) | Hub + treasure mid-ring (17 zones) |
| **Web** | Mini-Nostalgia (144) | Dual-pole treasure web + spawn shortcuts (15 zones) |
| **Boomerang** | Boomerang (144) | Buffered arms → shared `Center` (15 zones) |
| **Spider** | Spider (208) | 8 radial legs + treasure mid-ring + SuperTreasure inner-ring (24 zones) |
| **Nexus** | Expanse (192) | Connector web (25 zones) |
| **Hub** | OctoJebus (240) | Isolated spawns → `Center` only (9 zones) |
| **Corridor** | Hard Place (144, co-op) | Linear spine + direct cross-AI · Ultra ×1.5 (17 zones) |
| **Matrix Map** | hand lattice (240) | 5×5 lattice — A-N home↔Spawn-N; B mid + Center; C magic schools; red Portals |

**Co-op corridor** (`Corridor`) uses the linear spine layout (P1 — buffers — AI — Center — AI — P2).
All other maps keep distinct topologies but share the same co-op rules shell via
`tools/max8/apply_max8_coop_classic.py` (classic win, PvE guard multiplier 0.85, diplomacy −0.5,
antipodal Player1/Player2 assignment).

Regenerate corridor topology: `python tools/max8/build_coop_corridor.py`. Flavor variant (Boomerang):
`python tools/max8/rework_max8_variants.py`.

**Diversity:** **11 distinct zone graphs**. Topologies: ring, mesh, spokes, wheel, web, boomerang,
spider, nexus, hub, corridor, and the **Matrix Map** 5×5 lattice.

**Neutral content:** each mid-map neutral zone (Treasure, Buffer, Connector, SuperTreasure leg) gets a
**themed location** mandatory pack from [`../../content/catalogs/max8_neutral_packs.json`](../../content/catalogs/max8_neutral_packs.json).
Packs group objects into cohesive settings (ArcaneSanctuary, WarCamp, TradePost, MiningOutpost, HeroShrine)
with biome-matched banks, altars, dwellings, mines, weekly storages, and power-ups. Assignment is
biome-aware via `tools/max8/diversify_max8_neutrals.py`; peer zones stay value-balanced. Procedural fill must
reuse **engine-known** pool SIDs (Expanse / official families) — never invent `content_pool_max8_*`
(breaks MapGen; see `docs/LESSONS_LEARNED.md`). **Per-zone bank caps** (`maxCount: 1` per bank type)
come from [`../../content/catalogs/max8_bank_limits.json`](../../content/catalogs/max8_bank_limits.json). Center/hub zones get a themed
refresh; **Hub** uses the full official OctoJebus center grid via `centerOverrides`.
**Matrix Map** is hand-packaged (`tools/max8/build_matrix_map.py`) — A-N packs match Spawn-N biome/faction;
C-1..4 are Nightshade/Daylight/Primal/Arcane school packs. Do **not** run `diversify_max8_neutrals.py`,
`rewire_max8_pools.py`, or `normalize_max8_to_matrix.py` on it (HAND_PACKAGED). Near-dupe check:
`python tools/max8/topology_fingerprint.py content/templates/max8`.

**Co-op fairness:** see [`../../docs/oe/coop-fairness-review.md`](../../docs/oe/coop-fairness-review.md).

## Player picker guide (macro tier + co-op)

All maps: **classic win**, **co-op tier A**. Ally Player1 + Player2; seat six AI on Player3–8.

| Template | Macro tier | Contact | Co-op seats |
|---|---|---|---|
| **Ring** | Lean | Slow | P1/P2 antipodal (auto) |
| **Mesh** | Standard | Medium | P1/P2 antipodal (auto) |
| **Spokes** | Lean | Slow | P1/P2 antipodal hub arms |
| **Wheel** | Lean | Slow | P1/P2 antipodal (auto) |
| **Web** | Dense | Fast | P1/P2 antipodal (auto) |
| **Boomerang** | Dense | Medium | P1/P2 antipodal (auto) |
| **Spider** | Dense | Medium | P1/P2 antipodal (auto) |
| **Nexus** | Standard | Medium | P1/P2 antipodal (auto) |
| **Hub** | Standard | Hub-only | P1/P2 antipodal hub |
| **Corridor** | Ultra | Slow | **Spawn-A / Spawn-B** |
| **Matrix Map** | Standard | Medium | P1/P2 antipodal (Spawn-1 / Spawn-2) |

Lobby: pick any max8 template → seat two humans on Player1/Player2 → ally them → six AI on 3–8.
Optional simultaneous turns work best on Corridor (~9 neutral hops between humans).

### Preview legend

Sidecar `.png` previews: **green** discs = spawn order (1 = `Spawn-A`, 2 = `Spawn-B` on Corridor);
bronze/silver = neutral buffers; blue **H** = hub / hold city.

## Pacing families (Matrix-scaled)

Topology unchanged; economy uses Matrix role ladder × family factor (flat budgets, `*PerArea` = 0):

| Family | Templates | Factor | Spawn GCV target |
|---|---|---:|---:|
| **Lean** | Ring, Wheel, Spokes | 0.75× | ~338k |
| **Standard** | Mesh, Nexus, Hub, Matrix Map | 1.0× | 450k |
| **Dense** | Spider, Web, Boomerang | 1.25× | ~563k |
| **Ultra** | Corridor | 1.5× | ~675k |

Matrix role ladder (× factor): Spawn 450k → mid/Treasure 550k → junction/Connector 650k →
deep/SuperTreasure 900k → Center 1.0M. Guards banded **15k / 35k / 85k** (`wi` 0.15). Mid neutrals
use `AbandonedOutpost` (not City); spawns carry City + Matrix spawn MC.

**Win conditions (all 11):** `classic` only — no hold-city, no lost-start-city, no encounter holes.
Applied by `tools/max8/apply_max8_coop_classic.py`.

- **Matrix Map** — 5×5 lattice (25 zones); yellow 15K / orange 35K Direct; red 85K Portals into Center
  and marked mid edges; rich spawn mandatories (hire 1–7 + mills); regenerate with
  `python tools/max8/build_matrix_map.py` then `apply_max8_coop_classic`.

Spawn content (all non-Matrix via normalize + spawn profile):

- **Mandatory per spawn:** watchtower, wood/ore mines, `random_hire_1`–`7`, market, tavern, mana well,
  storage_wood, common item.
- Utopia-tier / unfair objects capped by role (`max8_wiki_fairness_caps.json`): utopia / mirage /
  wind_rose / black_tower banned on spawn; utopia allowed on deep/center only.
- Each **bank type** capped at 1 per zone (spawn and neutral).
- Hub additionally drops mandatory spawn utopia SIDs; Center keeps OctoJebus multi-city layout.

**Deploy:** [`../../docs/install.md`](../../docs/install.md). Smoke-test in-game after deploy.
