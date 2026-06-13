# Installation and deploy paths

Official templates in `templates/official/` trace to the community [Olden Era — Template Generator](https://github.com/KhanDevelopsGames/Olden-Era---Template-Generator) project.

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

Subfolders in this repo (`official/`, `max8/`, `h3-port/`) are organizational only — flatten when copying to the game, or copy only the subset you need.

## HotA tournament source (H3 porting)

Official tournament `.h3t` packs install with GOG HotA:

```
C:\Program Files (x86)\GOG Galaxy\Games\Heroes of Might and Magic III - Horn of the Abyss\HotA_RMGTemplates\
```

Copies used in this repo live under [`h3/sources/official/`](../h3/sources/official/). Re-copy from GOG after HotA updates, then run `python tools/parse_official_h3.py`.

Template editor: `h3hota_tmpled.exe` in the HotA install root.

## User override folder (optional)

The game may also read user templates from a `my_map_templates` folder under the user's app data. Prefer StreamingAssets for development copies that match this repo layout.
