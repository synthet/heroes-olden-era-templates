# Max-Size 8-Player Co-op Template Set

13 templates, all **240×240** (max map size) and **8 players** (max), tuned for **2 human co-op +
6 FFA AI** with **classic win only** on every map. Seat humans on **Player1** and **Player2**
(maximally separated spawns — **Spawn-A** / **Spawn-B** on corridor maps); Players 3–8 as AI.
Each name reflects its **source template** (official or h3-port base) and/or **topology**.
Built with the recipe in [`../../docs/oe/cookbook.md`](../../docs/oe/cookbook.md);
economy scaled to 240 using flat `*Value` × `240/oldPx` and per-area × `(240/oldPx)²`,
with spawn zones normalized to native 240×240 density (see `tools/max8_economy.py`).
Regenerate themed content and spawn discipline:

```bash
python tools/build_max8_neutral_packs.py   # themed location packs
python tools/build_max8_bank_limits.py     # per-zone bank caps catalog
python tools/rescale_max8_economy.py       # economy rescale + full pipeline (preferred)
# Or step-by-step after hand edits:
python tools/rewire_max8_pools.py          # lean max8 fill pools
python tools/diversify_max8_neutrals.py    # biome-aware neutral pack assignment
python tools/apply_max8_pacing_tweaks.py   # spawn mandatory + limits + economy trim
python tools/apply_max8_coop_classic.py    # classic win + co-op tuning (run last)
```

Audit spawn/center economy bands: `python tools/analyze_economy_density.py --matrix` (writes
[`../../lib/max8_macro_audit.json`](../../lib/max8_macro_audit.json)). Authoring metadata:
[`../../lib/max8_design_meta.json`](../../lib/max8_design_meta.json).

Economy rescale (when map size or base changes): `python tools/rescale_max8_economy.py` runs rewire,
diversify, and pacing in order after rescaling. PNG previews: `python tools/render_preview.py templates/max8`.

All 13 **PASS** `python tools/validate_rmg.py templates/max8`.

| Template | Base (size) | Name reflects | Topology |
|---|---|---|---|
| **Diamond Ring** | Diamond (144, rewired) | source + **ring** | Buffered ring — neutral between every spawn (16 zones, diameter 8) |
| **Ikarus Showdown** | Ikarus (160, rewired) | source + **showdown hub** | Spawn → neutral → central `Center` prize (17 zones) |
| **Grand Nostalgia** | Mini-Nostalgia (144) | source (scaled “Grand”) | Nostalgia treasure web (15 zones) |
| **Diamond Colossus** | Diamond (144) | source + scale | Diamond grid (16 zones) |
| **Ikarus Ascendant** | Ikarus (160) | source | Ikarus branched (17 zones) |
| **Spider Titan** | Spider (208) | source | Spider legs (24 zones) |
| **Boundless Expanse** | Expanse (192) | source | Connector web (25 zones) |
| **Octo Anarchy** | OctoJebus (240) | source + rules | Isolated hub (spawns → `Center` only) |
| **Antares Maelstrom** | mt_Antares (144) | source + chaos | Spider legs with **dual outer fork** on T3/T4 · `encounterHoles` |
| **Ikarus Ladder Dominion** | Ikarus (160, co-op) | source + **ladder** + **hold** | Co-op corridor — cross-AI via neutral rungs · hold city (20 zones) |
| **Boomerang Crown** | Boomerang (144) | source + **hold win** | Buffered boomerang — spawn → arm treasure → `Center` hold (15 zones) |
| **Hard Place Hoard Corridors** | Hard Place (144, co-op) | source + **hoard** + **corridors** | Co-op corridor — linear spine, direct cross-AI · economy ×1.5 (17 zones) |
| **Matrix Map** | hand lattice (240) | **matrix** 5×5 | 5×5 lattice — A-N home↔Spawn-N; B mid + Center; C magic schools; red Portals |

**Co-op corridor maps** (`Hard Place Hoard Corridors`, `Ikarus Ladder Dominion`) use the linear
spine layout (P1 — buffers — AI — Center — AI — P2). All other maps keep distinct topologies but
share the same co-op rules shell via `tools/apply_max8_coop_classic.py` (classic win, PvE guard
multiplier 0.85, diplomacy −0.5, antipodal Player1/Player2 assignment).

Regenerate corridor topology: `python tools/build_coop_corridor.py`. Flavor variants (Antares,
Boomerang): `python tools/rework_max8_variants.py`.

**Diversity:** **13 distinct zone graphs**. Topologies include ring, showdown hub, nostalgia web,
diamond grid, Ikarus branches, spider legs, maelstrom fork, expanse web, octo hub, boomerang, co-op
corridor (linear + direct cross), co-op ladder (linear + buffered cross), and the **Matrix Map** 5×5
lattice.

**Neutral content:** each mid-map neutral zone (Treasure, Buffer, Connector, SuperTreasure leg) gets a
**themed location** mandatory pack from [`../../lib/max8_neutral_packs.json`](../../lib/max8_neutral_packs.json).
Packs group objects into cohesive settings (ArcaneSanctuary, WarCamp, TradePost, MiningOutpost, HeroShrine)
with biome-matched banks, altars, dwellings, mines, weekly storages, and power-ups. Assignment is
biome-aware via `tools/diversify_max8_neutrals.py`; peer zones stay value-balanced. Procedural fill uses
lean max8 pools ([`../../data/content_pools/template_max8_fill_pools.json`](../../data/content_pools/template_max8_fill_pools.json))
so pools do not scatter duplicate banks/dwellings. **Per-zone bank caps** (`maxCount: 1` per bank type)
come from [`../../lib/max8_bank_limits.json`](../../lib/max8_bank_limits.json). Center/hub zones get a themed
refresh; **Octo Anarchy** uses the full official OctoJebus center grid via `centerOverrides`.
**Matrix Map** is hand-packaged (`tools/build_matrix_map.py`) — A-N packs match Spawn-N biome/faction;
C-1..4 are Nightshade/Daylight/Primal/Arcane school packs. Do **not** run `diversify_max8_neutrals.py`
on it (would overwrite school/home packs).

**Co-op fairness:** see [`../../docs/oe/coop-fairness-review.md`](../../docs/oe/coop-fairness-review.md).

## Player picker guide (macro tier + co-op)

All maps: **classic win**, **co-op tier A**. Ally Player1 + Player2; seat six AI on Player3–8.

| Template | Macro tier | Contact | Co-op seats |
|---|---|---|---|
| **Diamond Ring** | Lean | Slow | P1/P2 antipodal (auto) |
| **Diamond Colossus** | Standard | Medium | P1/P2 antipodal (auto) |
| **Ikarus Showdown** | Lean | Slow | P1/P2 antipodal hub arms |
| **Ikarus Ascendant** | Lean | Slow | P1/P2 antipodal (auto) |
| **Grand Nostalgia** | Dense | Fast | P1/P2 antipodal (auto) |
| **Boomerang Crown** | Dense | Medium | P1/P2 antipodal (auto) |
| **Spider Titan** | Dense | Medium | P1/P2 antipodal (auto) |
| **Antares Maelstrom** | Dense | Fast | P1/P2 antipodal (auto) |
| **Boundless Expanse** | Standard | Medium | P1/P2 antipodal (auto) |
| **Octo Anarchy** | Standard | Hub-only | P1/P2 antipodal hub |
| **Hard Place Hoard Corridors** | Ultra | Slow | **Spawn-A / Spawn-B** |
| **Ikarus Ladder Dominion** | Lean | Slow | **Spawn-A / Spawn-B** |
| **Matrix Map** | Standard | Medium | P1/P2 antipodal (Spawn-1 / Spawn-2) |

Lobby: pick any max8 template → seat two humans on Player1/Player2 → ally them → six AI on 3–8.
Optional simultaneous turns work best on corridor maps (~9–10 neutral hops between humans).

### Preview legend

Sidecar `.png` previews: **green** discs = spawn order (1 = `Spawn-A`, 2 = `Spawn-B` on corridor maps);
bronze/silver = neutral buffers; blue **H** = hub / hold city.

## Pacing families

Player-feedback alignment (spawn-only trims + reward caps; topology unchanged):

| Family | Templates | Spawn character |
|---|---|---|
| **Slow Burn** | Diamond Ring, Ikarus Ascendant, Ikarus Showdown, Ikarus Ladder Dominion | Lean spawns, exploration-first |
| **Standard** | Diamond Colossus, Boundless Expanse, Matrix Map | Moderate spawn budgets |
| **Competitive Dense** | Octo Anarchy, Spider Titan, Antares Maelstrom, Grand Nostalgia, Boomerang Crown | High macro; spawn trim ~15% when guarded ≥ 5M (Grand Nostalgia / Boomerang: ~20% when ≥ 4M) |
| **Co-op Explore** | Hard Place Hoard Corridors, Ikarus Ladder Dominion | Hoard/corridor intent (×1.5 on Hard Place; ×1.35 buffer economy on Ladder); capped spawn clutter |

Design deltas (topology unchanged):

- **Diamond Colossus** — +10% spawn guarded vs Ring (grid = faster macro).
- **Ikarus Showdown** — lean 1M center prize vs Ascendant 3M; siege AbandonedOutpost focus.
- **Grand Nostalgia** — direct spawn shortcuts guarded at 50K + `simTurnSquad`.
- **Antares Maelstrom** — costly T3/T4→SuperTreasure forks (75K scaled); WarCamp packs on fork legs; global `encounterHoles` (Spider Titan stays clean).
- **Boomerang Crown** — tip arms (Treasure-1/6→Center) higher guards than inner arms; classic center prize (no hold win).

**Win conditions (all 13):** `classic` only — no hold-city, no lost-start-city, no encounter holes.
Applied by `tools/apply_max8_coop_classic.py`.

- **Matrix Map** — 5×5 lattice (25 zones); yellow 15K / orange 35K Direct; red 85K Portals into Center
  and marked mid edges; rich spawn mandatories (hire 1–7 + all weekly mills); regenerate with
  `python tools/build_matrix_map.py` then `apply_max8_coop_classic`.

Spawn pacing rules (all 13), driven by [`../../lib/max8_spawn_profile.json`](../../lib/max8_spawn_profile.json):

- **Mandatory per spawn:** watchtower, wood/ore mines, 1–2 low-tier dwellings (levels 1–3), at most 1
  high-tier dwelling (4–7), weekly storage, and a power-up (mana well / stables).
- **Slow Burn** family gets 1 low + 1 high dwelling; **Standard / Competitive** get 2 low + 1 high.
- **Pool fill** excludes random hires and banks (mandatory owns those); caps prevent duplicate clutter.
- Premium POI caps in `content_limits_spawn` (maxCount 1 for shrines, trails, spheres, thrones).
- Each **bank type** capped at 1 per zone (spawn and neutral).
- Octo Anarchy additionally drops mandatory spawn `dragon_utopia`.

**Deploy:** [`../../docs/install.md`](../../docs/install.md). Smoke-test in-game after deploy.
