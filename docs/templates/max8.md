---
type: Template Collection
title: Max8 Templates
description: 12 experimental 240×240 eight-player variants tuned for 2-human co-op + 6 FFA AI with classic win only. Each is derived from an official or h3-port base and economy-rescaled to 240×240.
resource: ../../templates/max8/
tags: [max8, coop, 8-player, 240x240, experimental]
timestamp: 2026-06-16T00:00:00Z
---

# Max8 Templates

12 templates in [`templates/max8/`](../../templates/max8/), all **240×240** (max map size), **8 players**, tuned for **2-human co-op + 6 FFA AI**, **classic win only**.

Seat humans on **Player1** and **Player2** (antipodal spawns — **Spawn-A** / **Spawn-B** on corridor maps); Players 3–8 as AI.

## Template Catalog

| Template | Base (size) | Topology |
|---|---|---|
| **Diamond Ring** | Diamond (144, rewired) | Buffered ring — neutral between every spawn (16 zones) |
| **Ikarus Showdown** | Ikarus (160, rewired) | Spawn → neutral → central `Center` prize (17 zones) |
| **Grand Nostalgia** | Mini-Nostalgia (144) | Nostalgia treasure web (15 zones) |
| **Diamond Colossus** | Diamond (144) | Diamond grid (16 zones) |
| **Ikarus Ascendant** | Ikarus (160) | Ikarus branched (17 zones) |
| **Spider Titan** | Spider (208) | Spider legs (24 zones) |
| **Boundless Expanse** | Expanse (192) | Connector web (25 zones) |
| **Octo Anarchy** | OctoJebus (240) | Isolated hub (spawns → `Center` only) |
| **Antares Maelstrom** | mt_Antares (144) | Spider legs with dual outer fork · `encounterHoles` |
| **Ikarus Ladder Dominion** | Ikarus (160, co-op) | Co-op corridor — cross-AI via neutral rungs · hold city (20 zones) |
| **Boomerang Crown** | Boomerang (144) | Buffered boomerang — spawn → arm treasure → `Center` hold (15 zones) |
| **Hard Place Hoard Corridors** | Hard Place (144, co-op) | Co-op corridor — linear spine, direct cross-AI · economy ×1.5 (17 zones) |

## Macro Tiers

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

## Pacing Families

| Family | Templates |
|---|---|
| **Slow Burn** | Diamond Ring, Ikarus Ascendant, Ikarus Showdown, Ikarus Ladder Dominion |
| **Standard** | Diamond Colossus, Boundless Expanse |
| **Competitive Dense** | Octo Anarchy, Spider Titan, Antares Maelstrom, Grand Nostalgia, Boomerang Crown |
| **Co-op Explore** | Hard Place Hoard Corridors, Ikarus Ladder Dominion |

## Regenerate

```bash
python tools/rescale_max8_economy.py      # economy rescale + full pipeline (preferred)
python tools/build_max8_neutral_packs.py  # themed location packs
python tools/build_max8_bank_limits.py    # per-zone bank caps catalog
python tools/render_preview.py templates/max8  # PNG previews
```

Validate: `python tools/validate_rmg.py templates/max8`

## Joins

- Economy rescaling documented in [OE cookbook](../oe/cookbook.md).
- Co-op balance criteria in [co-op fairness review](../oe/coop-fairness-review.md).
- Each entry's `Base` column refers to a template in [official](official.md) or [h3-port](h3-port.md).
