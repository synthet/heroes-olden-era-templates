# Max-Size 8-Player Co-op Template Set

11 templates, all **240×240** (max map size) and **8 players** (max), tuned for **2 human co-op +
6 FFA AI** with **classic win only** on every map. Seat humans on **Player1** and **Player2**
(maximally separated spawns — **Spawn-A** / **Spawn-B** on Corridor); Players 3–8 as AI.
Each name reflects its **topology**. Built with the recipe in
[`../../docs/oe/cookbook.md`](../../docs/oe/cookbook.md); economy scaled to 240 using flat
`*Value` × `240/oldPx` and per-area × `(240/oldPx)²`, with spawn zones normalized to native
240×240 density (see `tools/max8_economy.py`). Regenerate themed content and spawn discipline:

```bash
python tools/max8/build_max8_neutral_packs.py   # themed location packs
python tools/max8/build_max8_bank_limits.py     # per-zone bank caps catalog
python tools/max8/rescale_max8_economy.py       # economy rescale + full pipeline (preferred)
# Or step-by-step after hand edits:
python tools/max8/rewire_max8_pools.py          # lean max8 fill pools
python tools/max8/diversify_max8_neutrals.py    # biome-aware neutral pack assignment
python tools/max8/apply_max8_pacing_tweaks.py   # spawn mandatory + limits + economy trim
python tools/max8/apply_max8_coop_classic.py    # classic win + co-op tuning (run last)
```

Audit spawn/center economy bands: `python tools/max8/analyze_economy_density.py --matrix` (writes
[`../../content/catalogs/max8_macro_audit.json`](../../content/catalogs/max8_macro_audit.json)). Authoring metadata:
[`../../content/catalogs/max8_design_meta.json`](../../content/catalogs/max8_design_meta.json).

Economy rescale (when map size or base changes): `python tools/max8/rescale_max8_economy.py` runs rewire,
diversify, and pacing in order after rescaling. After rewire, pools must stay on **Expanse engine SIDs**
(never `content_pool_max8_*`). Fill roads after topology edits:
`python tools/max8/fill_max8_roads.py`. PNG previews: `python tools/preview/render_preview.py content/templates/max8`.

All 11 **PASS** `python tools/validate/validate_rmg.py content/templates/max8`.

| Template | Base (size) | Topology |
|---|---|---|
| **Ring** | Diamond (144, rewired) | Buffered ring — neutral between every spawn (16 zones, diameter 8) |
| **Mesh** | Diamond (144) | Dense bipartite diamond grid (16 zones) |
| **Spokes** | Ikarus (160, rewired) | Spawn → treasure → central `Center` prize (17 zones) |
| **Wheel** | Ikarus (160) | Hub + treasure mid-ring (17 zones) |
| **Web** | Mini-Nostalgia (144) | Dual-pole treasure web + spawn shortcuts (15 zones) |
| **Boomerang** | Boomerang (144) | Buffered arms → shared `Center` (15 zones) |
| **Spider** | Spider (208) | Multi-leg spider web (24 zones) |
| **Expanse** | Expanse (192) | Connector web (25 zones) |
| **Hub** | OctoJebus (240) | Isolated spawns → `Center` only (9 zones) |
| **Corridor** | Hard Place (144, co-op) | Linear spine + direct cross-AI · economy ×1.5 (17 zones) |
| **Matrix Map** | hand lattice (240) | 5×5 lattice — A-N home↔Spawn-N; B mid + Center; C magic schools; red Portals |

**Co-op corridor** (`Corridor`) uses the linear spine layout (P1 — buffers — AI — Center — AI — P2).
All other maps keep distinct topologies but share the same co-op rules shell via
`tools/max8/apply_max8_coop_classic.py` (classic win, PvE guard multiplier 0.85, diplomacy −0.5,
antipodal Player1/Player2 assignment).

Regenerate corridor topology: `python tools/max8/build_coop_corridor.py`. Flavor variant (Boomerang):
`python tools/max8/rework_max8_variants.py`.

**Diversity:** **11 distinct zone graphs**. Topologies: ring, mesh, spokes, wheel, web, boomerang,
spider, expanse, hub, corridor, and the **Matrix Map** 5×5 lattice.

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
C-1..4 are Nightshade/Daylight/Primal/Arcane school packs. Do **not** run `diversify_max8_neutrals.py`
or `rewire_max8_pools.py` on it (HAND_PACKAGED). Near-dupe check:
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
| **Expanse** | Standard | Medium | P1/P2 antipodal (auto) |
| **Hub** | Standard | Hub-only | P1/P2 antipodal hub |
| **Corridor** | Ultra | Slow | **Spawn-A / Spawn-B** |
| **Matrix Map** | Standard | Medium | P1/P2 antipodal (Spawn-1 / Spawn-2) |

Lobby: pick any max8 template → seat two humans on Player1/Player2 → ally them → six AI on 3–8.
Optional simultaneous turns work best on Corridor (~9 neutral hops between humans).

### Preview legend

Sidecar `.png` previews: **green** discs = spawn order (1 = `Spawn-A`, 2 = `Spawn-B` on Corridor);
bronze/silver = neutral buffers; blue **H** = hub / hold city.

## Pacing families

Player-feedback alignment (spawn-only trims + reward caps; topology unchanged):

| Family | Templates | Spawn character |
|---|---|---|
| **Slow Burn** | Ring, Wheel, Spokes | Lean spawns, exploration-first |
| **Standard** | Mesh, Expanse, Matrix Map | Moderate spawn budgets |
| **Competitive Dense** | Hub, Spider, Web, Boomerang | High macro; spawn trim ~15% when guarded ≥ 5M (Web / Boomerang: ~20% when ≥ 4M) |
| **Co-op Explore** | Corridor | Hoard/corridor intent (×1.5 economy); capped spawn clutter |

Design deltas (topology unchanged):

- **Mesh** — +10% spawn guarded vs Ring (grid = faster macro).
- **Spokes** — lean 1M center prize vs Wheel 3M; siege AbandonedOutpost focus.
- **Web** — direct spawn shortcuts guarded at 50K + `simTurnSquad`.
- **Boomerang** — tip arms (Treasure-1/6→Center) higher guards than inner arms; classic center prize.

**Win conditions (all 11):** `classic` only — no hold-city, no lost-start-city, no encounter holes.
Applied by `tools/max8/apply_max8_coop_classic.py`.

- **Matrix Map** — 5×5 lattice (25 zones); yellow 15K / orange 35K Direct; red 85K Portals into Center
  and marked mid edges; rich spawn mandatories (hire 1–7 + all weekly mills); regenerate with
  `python tools/max8/build_matrix_map.py` then `apply_max8_coop_classic`.

Spawn pacing rules (all 11), driven by [`../../content/catalogs/max8_spawn_profile.json`](../../content/catalogs/max8_spawn_profile.json):

- **Mandatory per spawn:** watchtower, wood/ore mines, 1–2 low-tier dwellings (levels 1–3), at most 1
  high-tier dwelling (4–7), weekly storage, and a power-up (mana well / stables).
- **Slow Burn** family gets 1 low + 1 high dwelling; **Standard / Competitive** get 2 low + 1 high.
- **Pool fill** excludes random hires and banks (mandatory owns those); caps prevent duplicate clutter.
- Premium POI caps in `content_limits_spawn` (maxCount 1 for shrines, trails, spheres, thrones).
- Each **bank type** capped at 1 per zone (spawn and neutral).
- Hub additionally drops mandatory spawn `dragon_utopia`.

**Deploy:** [`../../docs/install.md`](../../docs/install.md). Smoke-test in-game after deploy.
