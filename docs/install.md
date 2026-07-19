---
type: Runbook
title: Install (Publish)
description: Publish-facing install notes.
resource: install.publish.md
tags: [install, publish, okf]
timestamp: 2026-07-12T00:00:00Z
okf_version: 0.1
---

# Installation and deploy paths

This distribution includes community-authored templates (`max8/`, `h3-port/`). Stock/official OE templates are not redistributed here.

## Deploy OE templates to the game

Copy the contents of [`templates/`](../templates/) into the game's StreamingAssets folder:

```
<Steam library>\steamapps\common\Heroes of Might and Magic Olden Era\HeroesOldenEra_Data\StreamingAssets\map_templates
```

Example (adjust drive if your Steam library differs):

```
D:\SteamLibrary\steamapps\common\Heroes of Might and Magic Olden Era\HeroesOldenEra_Data\StreamingAssets\map_templates
```

Each shippable template is two files sharing a basename: `Name.rmg.json` and `Name.png` (preview image for the in-game picker).

Subfolders in this repo (`max8/`, `h3-port/`) are organizational only — flatten when copying to the game, or copy only the subset you need.

## User folders (optional)

Community-observed paths under
`%LOCALAPPDATALOW%\Unfrozen\HeroesOldenEra\users\<Steam_…>\`:

| Folder | UX |
|--------|-----|
| `downloads\map_templates` | Customs appear under **downloads** in custom game |
| `my_map_templates` | Alternate user-side drop folder |

Customs are generally not available via Quick Play without editing game files. Prefer StreamingAssets for copies that match this publish layout. Full notes: private-repo `docs/install.md` / `docs/external/garessta-text-editor-guide.md`.
