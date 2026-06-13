# Engine data mirror

Bundled Olden Era content that `.rmg.json` templates reference by SID. The game loads the same data from its StreamingAssets; this copy lets you resolve pool names, encounter layouts, and object values while authoring offline.

## Layout

| Path | Contents |
|------|----------|
| `content_pools/` | `content_pool_*` / `template_pool_*` definitions |
| `content_lists/` | `basic_content_list_*` / `content_list_*` definitions |
| `zone_layouts/` | Default `zone_layout_*` definitions |
| `encounter_templates/` | 641 `rmg_*` encounter grid stamps |
| `generator_config.json` | Object gold values and guard values (economy backbone) |
| `generator_stats_config.json` | Objects counted toward stat distribution |
| `generator_environment_assets.json` | Biome → tileset → asset SIDs |

## Lookup catalogs

Enum IDs, bannable items, variant meanings, distance presets, and generator constants live in [`../lib/`](../lib/) — see [`../lib/README.md`](../lib/README.md).

## Format reference

How templates wire pools, lists, and zone layouts: [`../docs/oe/rmg-format.md`](../docs/oe/rmg-format.md) Part V.
