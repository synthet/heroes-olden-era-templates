# H3 HotA template catalog

Downloaded `.h3t` / `rmg.txt` packs for cross-mapping with Olden Era templates.

## HotA install (official source)

```
C:\Program Files (x86)\GOG Galaxy\Games\Heroes of Might and Magic III - Horn of the Abyss\HotA_RMGTemplates\
```

All **27 tournament** `.h3t` packs are copied to [`../../h3/sources/official/`](../../h3/sources/official/). Parsed topology: [`../../h3/layouts/official/`](../../h3/layouts/official/).

Template editor: `h3hota_tmpled.exe` in the HotA install root.

## Sources

| Source | Notes |
|--------|-------|
| **GOG HotA install** (above) | Official tournament packs — primary source |
| [h3hota.com/en/templates](https://h3hota.com/en/templates) | Layout diagrams and richness presets |
| [h3hota template format](https://h3hota.com/en/template-format) | Field semantics |
| Community packs | [`../../h3/sources/community/`](../../h3/sources/community/) |

## OE counterparts

See [`matrix.md`](matrix.md) for the full tournament inventory and match status. Zone/connection comparison table: [`../../h3/layouts/official/README.md`](../../h3/layouts/official/README.md).

## Parse commands

HotA `.h3t` files are tab-separated text:

```bash
python tools/h3t_parser.py "h3/sources/official/Jebus Cross.h3t"
python tools/parse_official_h3.py
```

See [`../../tools/README.md`](../../tools/README.md) for the full regen workflow.
