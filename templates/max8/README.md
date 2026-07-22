# Max-Size 8-Player Co-op Template Set

17 templates, all **240×240** (max map size) and **8 players** (max), tuned for **2 human co-op +
6 FFA AI** with **classic win only** on every map. Seat humans on **Player1** and **Player2**
(maximally separated spawns; **Spawn-A** / **Spawn-E** on Hub and Twin Isles; tip **Spawn-A** /
**Spawn-B** on Boomerang); Players 3–8 as AI. Each name reflects its **topology**.

**Balance reference:** [Matrix Map](Matrix%20Map.rmg.json) — flat role budgets, yellow/orange/red
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
# Full rebuild from official bases (includes normalize + Web/Ring custom topologies):
python tools/max8/rescale_max8_economy.py
# Ring fully-buffered flanks only:
python tools/max8/build_ring_buffered.py
# Classic Boomerang (H3 L+U arms → 3 ST hubs; HAND_PACKAGED):
python tools/max8/build_boomerang_classic.py
# Compressed H3 8XM8 lattice (HAND_PACKAGED):
python tools/max8/build_citadel.py
# Bilateral hourglass 5→4→3→2→1←2←3←4←5 (HAND_PACKAGED):
python tools/max8/build_hourglass.py
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
| **Ring** | Diamond (144, rewired) | Fully buffered ring — every spawn CW+CCW flanks; hard AI exits (32 zones) |
| **Mesh** | Diamond (144) | Dense bipartite diamond grid (16 zones) |
| **Spokes** | Ikarus (160, rewired) | Spawn → treasure → central `Center` prize (17 zones) |
| **Wheel** | Ikarus (160) | Hub + treasure mid-ring (17 zones) |
| **Web** | Mini-Nostalgia (144, rewired) | Equal-leaf dual-pole web; neutral Buffer-N/S gate Center (19 zones) |
| **Wings** | Boomerang (144, rewired) | Mirrored twin wings; Elbow-W/E gate `Center` (19 zones) |
| **Boomerang** | Boomerang (144, classic) | Classic L+U arms; tip A/B mid-treasure only; inner C–H gate 3 ST hubs (17 zones) |
| **Spider** | Spider (208) | 8 radial legs + treasure mid-ring; 4 SuperTreasure each shared by a blue pair (20 zones) |
| **Bracket** | Expanse (192) | Playoff tree 8→4→2→1 + unpredictable random-pool Leaf-1..8 farm pockets (23 zones); steeper round guards |
| **Hub** | OctoJebus (240, rewired) | Dual Might/Magic spokes to `Center` (25 zones); private paths per spawn |
| **Triad** | hand lattice (240) | Three identical 3×3 blocks (hub-adjacent P1/P2) + unpredictable random-pool Gate-W/M/E + four magic schools; triangle Portals Gate↔Gate @ 150k (30 zones) |
| **Spine** | Wings (rewired) | Twin truss spines; 4 mirrored random-pool interior zones; Portal Treasure-A↔G (150k) (24 zones) |
| **Domino** | Wings (rewired) | Twin 3×4 blocks; 4 mirrored random-pool interior zones; Portal Treasure-A↔G (150k) (24 zones) |
| **Channel** | Wings (rewired) | Twin hourglasses with one random-pool deep prize per half; dual Portals @ 150k (24 zones) |
| **Matrix Map** | hand lattice (240) | 5×5 lattice — A-N home↔Spawn-N; B mid + Center; C magic schools; red Portals |
| **Citadel** | hand lattice (240) | Compressed H3 8XM8 — fully procedural mystery Treasuries, SuperTreasure wall, Might camps + Magic schools, 4 cardinal Hubs (29 zones) |
| **Hourglass** | hand lattice (240) | Bilateral hourglass 5→4→3→2→1←2←3←4←5 — 4 spawns + Rim gate per arc; guards rise 15k/35k/50k/85k into Final (29 zones) |

All maps share the same co-op rules shell via `tools/max8/apply_max8_coop_classic.py` (classic win,
PvE guard multiplier 0.85, diplomacy −0.5, antipodal Player1/Player2 assignment), then
`tools/max8/apply_max8_ai_coop_ease.py`: AI (P3–P8) spawn budgets at **60–80%** of human (closer hop
to P1/P2 → leaner), near/mid/far AI mandatory kits (curios / low hires; fewer mines), and connection
`guardValue` **×1.25** (15k→18750, 35k→43750, 85k→106250, 150k→187500). Re-run the ease pass after
any HAND_PACKAGED rebuild.

Twin-wing Wings: `python tools/max8/build_wings.py` (also via `rework_max8_variants.py`). Classic
Boomerang: `python tools/max8/build_boomerang_classic.py`. Regenerate Hub dual spokes:
`python tools/max8/build_hub_arms.py`. Twin Isles set (Spine / Domino / Channel):
`python tools/max8/build_twins_set.py`. Triad: `python tools/max8/build_triad.py`.
Citadel: `python tools/max8/build_citadel.py`.

**Diversity:** Distinct zone graphs across the max8 set. Topologies: ring, mesh, spokes, wheel, web,
twin-wing wings, classic boomerang, spider, bracket, hub, triad,
twin-isle spine/domino/channel, the **Matrix Map** 5×5 lattice, and **Citadel**
(compressed 8XM8).

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
C-1..4 are Nightshade/Daylight/Primal/Arcane school packs. **Triad** is hand-packaged
(`tools/max8/build_triad.py`) — three identical 3×3 blocks (30 zones); A-homes, Mid war camps,
Nightshade/Daylight/Primal/Arcane schools; Hub-W/M/E behind procedural random-pool Gate-W/M/E; triangle Portals
Gate↔Gate @ 150k. **Bracket** is hand-packaged
(`tools/max8/build_bracket.py`) — playoff 8→4→2→1 plus unpredictable random-pool Leaf-1..8 farm pockets (23 zones). **Hub** is hand-packaged (`tools/max8/build_hub_arms.py`) —
dual Might (WarCamp) / Magic (ArcaneSanctuary) private spokes. **Boomerang** is hand-packaged
(`tools/max8/build_boomerang_classic.py`) — unique blue Treasure vs orange SuperTreasure packs.
**Citadel** is hand-packaged (`tools/max8/build_citadel.py`) — compressed H3 8XM8 lattice with red
Player3/4/7/8 routes into Center.
**Hourglass** is hand-packaged (`tools/max8/build_hourglass.py`) — Rim and Mid payloads are fully
procedural from official Expanse pools; WarCamp west / utility east Lows; ArcaneSanctuary Deeps;
Final center prize.
Do **not** run `diversify_max8_neutrals.py`, `rewire_max8_pools.py`, or
`normalize_max8_to_matrix.py` on Matrix Map / Bracket / Hub / Ring / Boomerang / Triad / Citadel / Hourglass (HAND_PACKAGED).
Near-dupe check: `python tools/max8/topology_fingerprint.py content/templates/max8`.

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
| **Wings** | Dense | Medium | P1/P2 antipodal (auto) |
| **Boomerang** | Dense | Medium | P1/P2 tip Spawn-A / Spawn-B |
| **Spider** | Dense | Medium | P1/P2 antipodal (auto) |
| **Bracket** | Standard | Medium | P1/P2 on Spawn-1 / Spawn-8 |
| **Hub** | Standard | Slow | P1/P2 on Spawn-A / Spawn-E |
| **Triad** | Standard | Slow | P1/P2 on W-S1 / E-S2 (triangle portals) |
| **Spine** | Standard | Slow | P1/P2 on Spawn-A / Spawn-E (portal) |
| **Domino** | Standard | Slow | P1/P2 on Spawn-A / Spawn-E (portal) |
| **Channel** | Standard | Slow | P1/P2 on Spawn-A / Spawn-E (dual portal) |
| **Matrix Map** | Standard | Medium | P1/P2 antipodal (Spawn-1 / Spawn-2) |
| **Citadel** | Standard | Medium | P1/P2 antipodal (auto; Spawn-1 / Spawn-6) |
| **Hourglass** | Standard | Slow | P1/P2 on Spawn-1 / Spawn-8 (opposite arcs) |

Lobby: pick any max8 template → seat two humans on Player1/Player2 → ally them → six AI on 3–8.

### Preview legend

Sidecar `.png` previews: **green** discs = spawn order (1 = Player1 seat, 2 = Player2 seat);
bronze + swords = Might arms; violet + gem = Magic arms; blue **H** = hub / hold city.

## Pacing families (Matrix-scaled)

Topology unchanged; economy uses Matrix role ladder × family factor (flat budgets, `*PerArea` = 0):

| Family | Templates | Factor | Spawn GCV target |
|---|---|---:|---:|
| **Lean** | Ring, Wheel, Spokes | 0.75× | ~338k |
| **Standard** | Mesh, Bracket, Hub, Triad, Spine, Domino, Channel, Matrix Map, Citadel, Hourglass | 1.0× | 450k |
| **Dense** | Spider, Web, Wings, Boomerang | 1.25× | ~563k |

Matrix role ladder (× factor): Spawn 450k → mid/Treasure 550k → junction/Connector 650k →
deep/SuperTreasure 900k → Center 1.0M. Base guards banded **15k / 35k / 85k** (`wi` 0.15), then
`apply_max8_ai_coop_ease.py` raises connection gates **×1.25**. Mid neutrals
use `AbandonedOutpost` (not City); human spawns carry City + Matrix spawn MC; AI spawns use lean
near/mid/far kits from `apply_max8_ai_coop_ease.py`.

**Win conditions (all 17):** `classic` only — no hold-city, no lost-start-city, no encounter holes.
Applied by `tools/max8/apply_max8_coop_classic.py`.

- **Matrix Map** — 5×5 lattice (25 zones); yellow 15K / orange 35K Direct; red 85K Portals into Center
- **Citadel** — compressed H3 8XM8 (29 zones); Treasure-1/4/5/6 are fully procedural mystery
  pockets (no mandatory pack, caps, fixed biome, or fixed faction); SuperTreasure wall ring;
  the four Center approaches are themed Might war camps (P4/P8 side) and Magic schools
  (altar + amplifier, P3/P7 side); one cardinal Hub per side docked to both mid-wall
  SuperTreasures (orange); red approach↔Center routes.
  Regenerate: `python tools/max8/build_citadel.py`.
- **Triad** — three identical 3×3 blocks + Gate-W/M/E (30 zones); every block runs a
  school–Hub axis with corner spawns; co-op P1/P2 sit hub-adjacent on the south slot (Mid's south
  slot holds the Primal school); yellow 15K / orange 35K Direct inside blocks; triangle Portals
  Gate-W↔Gate-M↔Gate-E at **150k** (hubs one hop behind); Gate payloads are fully procedural from
  official connector pools. Regenerate: `python tools/max8/build_triad.py`.
- **Bracket** — playoff tree 8→4→2→1 with unpredictable random-pool Leaf-1..8 farm pockets (23 zones); yellow 15K /
  orange 50K Direct; red 150K Portals into Final; rich spawn mandatories (hire 1–7 + mills);
  regenerate with `python tools/max8/build_bracket.py` then `apply_max8_coop_classic`.
- **Hourglass** — bilateral hourglass 5→4→3→2→1←2←3←4←5 (29 zones); each outer arc holds 4 spawns +
  1 neutral Rim; Rim/Mid content is random-pool generated; guards rise 15K / 35K / 50K / 85K
  Direct into Final; economy ladder
  Spawn 450k → Rim 500k → Low 550k → Mid 650k → Deep 900k → Final 1.0M. Regenerate with
  `python tools/max8/build_hourglass.py` then `apply_max8_coop_classic`.
- **Twin Isles (Spine / Domino / Channel)** — two disconnected 4-player
  figures (24 zones); yellow 15K leaves, orange 35K into Hub; West↔East only via Portal(s)
  at **150k**. Regenerate: `python tools/max8/build_twins_set.py`.

Spawn content (all non-Matrix via normalize + spawn profile):

- **Mandatory per spawn:** watchtower, wood/ore mines, `random_hire_1`–`7`, market, tavern, mana well,
  storage_wood, common item.
- Utopia-tier / unfair objects capped by role (`max8_wiki_fairness_caps.json`): utopia / mirage /
  wind_rose / black_tower banned on spawn; utopia allowed on deep/center only.
- Each **bank type** capped at 1 per zone (spawn and neutral).
- Hub additionally drops mandatory spawn utopia SIDs; Center keeps OctoJebus multi-city layout.

**Deploy:** [`../../docs/install.md`](../../docs/install.md). Smoke-test in-game after deploy.
