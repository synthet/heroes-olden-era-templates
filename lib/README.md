# Generator catalogs — lookup JSON

Structured lookup tables extracted from the (now-removed) Olden Era Template Generator C# source. Pairs with bundled engine data in [`../data/`](../data/) and the format spec in [`../docs/oe/rmg-format.md`](../docs/oe/rmg-format.md).

## Files

| File | Contents |
|------|----------|
| `content_ids.json` | 120 object/encounter SIDs → display names |
| `include_list_ids.json` | 36 common `*content_list_*` include-list SIDs |
| `variant_mappings.json` | `variant` int meanings for pandora_box, dragon_utopia, monty_hall |
| `known_values.json` | 21 enum/value catalogs (game modes, sizes, victory IDs, zone layouts, etc.) |
| `bannable_items.json` | 152 artifact IDs for `globalBans.items` |
| `bannable_magics.json` | 5 bannable spell IDs |
| `spells.json` | 78 learnable spells |
| `distance_presets.json` | 5 normalized distance bands for content placement |
| `content_count_limit_defaults.json` | 45 default per-SID `maxCount` caps |
| `generator_constants.json` | Scaling formula, border-guard bases, neutral profiles, zone limits |

## Related engine data

Content pool definitions, encounter templates, and object value tables: [`../data/`](../data/) — see [`../data/README.md`](../data/README.md).

Deploy paths: [`../docs/install.md`](../docs/install.md).
