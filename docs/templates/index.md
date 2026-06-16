---
type: Collection
title: Template Collections
description: Three collections of RMG templates organized by origin and design intent. Each template is a .rmg.json file paired with an optional .png preview.
tags: [templates, collections, rmg]
timestamp: 2026-06-16T00:00:00Z
---

# Template Collections

Deployable Olden Era `.rmg.json` files. Copy needed files into the game's `StreamingAssets\map_templates\` — see [Installation](../install.md).

| Collection | Templates | Description |
|------------|-----------|-------------|
| [official](official.md) | 57 | Native OE templates — start here for new authoring work |
| [max8](max8.md) | 12 | Experimental 240×240 eight-player co-op variants |
| [h3-port](h3-port.md) | 20 | Scaffolded H3 HotA tournament ports |

Subfolders in the repo (`official/`, `max8/`, `h3-port/`) are organizational only — flatten when copying to the game, or copy only the subset you need.

## Validate

```bash
python tools/validate_rmg.py templates/
```
