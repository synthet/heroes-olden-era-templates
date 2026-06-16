---
type: Template Collection
title: Official Templates
description: 57 native Olden Era RMG templates sourced from the community Olden Era Template Generator project. Use these as the canonical base for new template authoring.
resource: ../../templates/official/
tags: [official, native, oe, base-templates]
timestamp: 2026-06-16T00:00:00Z
---

# Official Templates

57 native OE templates in [`templates/official/`](../../templates/official/).

These are the canonical base templates for Olden Era's Random Map Generator. When creating new templates, clone one of these as your starting point.

## Source

Sourced from the community [Olden Era — Template Generator](https://github.com/KhanDevelopsGames/Olden-Era---Template-Generator) project. See [`LICENSE`](../../LICENSE) for the full text.

## Usage

Copy any `.rmg.json` files (and optional matching `.png` previews) into the game's StreamingAssets folder:

```
<Steam library>\steamapps\common\Heroes of Might and Magic Olden Era\HeroesOldenEra_Data\StreamingAssets\map_templates
```

See [Installation](../install.md) for full path details.

## Validate

```bash
python tools/validate_rmg.py templates/official/
```

## Joins

- [Max8 templates](max8.md) are scaled variants derived from official bases — each `max8` entry names its source official template.
- [H3 HotA ports](h3-port.md) are scaffolded from official bases — see the [H3 cross-reference matrix](../h3/matrix.md) for the full mapping.
