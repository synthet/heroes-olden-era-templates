---
type: Guide
title: OE Template Authoring Cookbook
description: Step-by-step recipe for creating, scaling, and validating Olden Era RMG templates, including economy rescaling to max-size (240×240).
tags: [authoring, cookbook, economy, rescale, rmg]
timestamp: 2026-06-16T00:00:00Z
---

# OE Template Authoring Cookbook

Reference guide for creating and modifying Olden Era `.rmg.json` templates.

## Starting a new template

1. Clone the closest [official template](../templates/official.md) as your base.
2. Rename the file and update `"name"` at the top of the JSON.
3. Adjust zone topology (`zones` + `connections` arrays).
4. Validate: `python tools/validate_rmg.py templates/<folder>/<name>.rmg.json`

## Economy rescaling (size change)

When changing map size from `oldPx` to `newPx`:

- Flat values (`*Value` fields): multiply by `newPx / oldPx`
- Per-area values (`*ValuePerArea`): multiply by `(newPx / oldPx)²`
- Spawn zones: normalize to native target density

Run the automated pipeline:

```bash
python tools/rescale_max8_economy.py   # rewire → diversify → pacing in order
```

Step-by-step (after hand edits):

```bash
python tools/rewire_max8_pools.py          # lean fill pools
python tools/diversify_max8_neutrals.py    # biome-aware neutral pack assignment
python tools/apply_max8_pacing_tweaks.py   # spawn mandatory + limits + economy trim
python tools/apply_max8_coop_classic.py    # classic win + co-op tuning (run last)
```

## Neutral content theming

Mid-map neutral zones (Treasure, Buffer, Connector, SuperTreasure leg) use themed location mandatory packs. Packs group objects into cohesive settings:

| Pack | Contents |
|------|---------|
| ArcaneSanctuary | Altars, mystical towers, mana wells |
| WarCamp | Barracks, dwellings, creature banks |
| TradePost | Markets, taverns, forge |
| MiningOutpost | Mines, weekly storages |
| HeroShrine | Stat-upgrade buildings, colleges |

Packs are defined in `lib/max8_neutral_packs.json`. Assignment: `python tools/diversify_max8_neutrals.py`.

## Bank caps

Per-zone bank caps (`maxCount: 1` per bank type) are catalogued in `lib/max8_bank_limits.json`. Regenerate: `python tools/build_max8_bank_limits.py`.

## Economy audit

```bash
python tools/analyze_economy_density.py --matrix
# writes lib/max8_macro_audit.json
```

## PNG previews

```bash
python tools/render_preview.py templates/<folder>
```

## Validation

```bash
python tools/validate_rmg.py templates/
```

## Joins

- Max8-specific authoring decisions: [max8 collection](../templates/max8.md)
- Co-op balance criteria: [co-op fairness review](coop-fairness-review.md)
