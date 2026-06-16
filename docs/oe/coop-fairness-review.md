---
type: Review
title: Co-op Fairness Review
description: Spawn and economy balance criteria for the max8 co-op template set. Covers spawn pacing rules, neutral zone value bands, and per-family trim thresholds.
tags: [coop, fairness, balance, max8, economy, spawn]
timestamp: 2026-06-16T00:00:00Z
---

# Co-op Fairness Review

Balance criteria applied to all 12 [max8 templates](../templates/max8.md) to ensure fair co-op play between the two human players (Player1 / Player2) against six AI opponents.

## Win conditions (all 12 maps)

`classic` only — no hold-city, no lost-start-city, no encounter holes.  
Applied by `tools/apply_max8_coop_classic.py`.

## Spawn pacing rules

Driven by `lib/max8_spawn_profile.json`:

| Rule | Requirement |
|------|-------------|
| Watchtower | 1 mandatory per spawn |
| Basic mines | wood + ore mines mandatory per spawn |
| Low-tier dwellings | 1–2 per spawn (levels 1–3) |
| High-tier dwelling | at most 1 per spawn (levels 4–7) |
| Weekly storage | 1 mandatory per spawn |
| Power-up | mana well or stables mandatory per spawn |
| Pool fill | excludes random hires + banks (mandatory owns those) |
| Premium POI caps | maxCount 1 for shrines, trails, spheres, thrones |
| Bank type caps | maxCount 1 per bank type per zone (spawn + neutral) |

**Pacing family adjustments:**

- **Slow Burn** (Diamond Ring, Ikarus Ascendant, Ikarus Showdown, Ikarus Ladder Dominion): 1 low + 1 high dwelling per spawn.
- **Standard / Competitive** (all others): 2 low + 1 high dwelling per spawn.
- **Octo Anarchy**: additionally drops mandatory `dragon_utopia` per spawn.

## Spawn trim thresholds

| Condition | Trim |
|-----------|------|
| Guarded spawn value ≥ 5M (Grand Nostalgia / Boomerang Crown) | ~20% spawn trim |
| Guarded spawn value ≥ 5M (others) | ~15% spawn trim |

## Co-op rules shell

All 12 maps share the same co-op rules shell via `tools/apply_max8_coop_classic.py`:

- Classic win condition
- PvE guard multiplier: **0.85**
- Diplomacy modifier: **−0.5**
- Player1 + Player2 assigned to antipodal spawns (Spawn-A / Spawn-B on corridor maps)

## Corridor map fairness

**Hard Place Hoard Corridors** and **Ikarus Ladder Dominion** use linear spine layout:

```
P1 — buffers — AI — Center — AI — P2
```

- Symmetric spine ensures equal distance from humans to AI.
- ~9–10 neutral hops between humans (suitable for simultaneous turns).
- Hard Place: economy ×1.5 vs base; Ikarus Ladder: ×1.35 buffer economy.

## Economy audit

Run `python tools/analyze_economy_density.py --matrix` to verify spawn/center economy bands fall within approved ranges. Output: `lib/max8_macro_audit.json`.

## Joins

- Template details: [max8 collection](../templates/max8.md)
- Economy rescaling method: [OE cookbook](cookbook.md)
