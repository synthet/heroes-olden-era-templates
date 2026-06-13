# H3 / OE layout extracts

## Official tournament topology

[`official/`](official/) — parsed from GOG `.h3t` via `tools/parse_official_h3.py`. Includes `_index.json` and an auto-generated comparison table in `official/README.md`.

## Community topology JSON

Parsed from [`../sources/community/`](../sources/community/) via `tools/h3t_parser.py`:

| File | Zones | Connections |
|------|-------|-------------|
| Balkans.topology.json | 115 | 122 |
| Diplo_Race.topology.json | 16 | 10 |
| Hundred_Fronts.topology.json | 64 | 84 |
| Island_Hop.topology.json | 28 | 24 |
| mt_Exile.topology.json | 5 | 11 |
| mt_Skeletents.topology.json | 56 | 64 |
| Treasure_Islands.topology.json | 66 | 36 |
| Wolf_and_Sheep.topology.json | 40 | 24 |
| Wungiel.topology.json | 32 | 75 |
| Jebus_Cross_2.0.topology.json | 5 | (community variant) |

## OE summaries

[`oe/`](oe/) — per-template JSON summaries from `tools/oe_template_summary.py` (zone names, spawns, connection guards for official OE templates).

See [`../../docs/h3/matrix.md`](../../docs/h3/matrix.md) for the H3 ↔ OE inventory.
