# Heroes Olden Era Map Templates

Random Map Generator (RMG) template files for **Heroes of Might and Magic: Olden Era**.

## Install

Copy template files into the game's `StreamingAssets\map_templates` folder. Full paths and copy tips: [`docs/install.md`](docs/install.md).

## Docs

Documentation is structured as an [OKF](https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf) bundle under [`docs/`](docs/index.md):

| Doc | Description |
|-----|-------------|
| [`docs/index.md`](docs/index.md) | Bundle root — all concepts linked from here |
| [`docs/install.md`](docs/install.md) | Deploy paths and copy instructions |
| [`docs/templates/`](docs/templates/index.md) | Per-collection concept docs |
| [`docs/h3/matrix.md`](docs/h3/matrix.md) | H3 HotA → OE template cross-reference |
| [`docs/oe/cookbook.md`](docs/oe/cookbook.md) | Template authoring and economy rescaling recipe |
| [`docs/oe/coop-fairness-review.md`](docs/oe/coop-fairness-review.md) | Co-op balance criteria for max8 maps |

```
<Steam library>\steamapps\common\Heroes of Might and Magic Olden Era\HeroesOldenEra_Data\StreamingAssets\map_templates
```

Subfolders here (`official/`, `max8/`, `h3-port/`) are organizational only — flatten when copying, or copy only the subset you need.

## Contents

| Folder | Contents |
|--------|----------|
| [`templates/official/`](templates/official/) | 57 native OE templates |
| [`templates/max8/`](templates/max8/) | 12 experimental 240×240 eight-player variants |
| [`templates/h3-port/`](templates/h3-port/) | 20 scaffolded H3 HotA tournament ports |

Each template is a `.rmg.json` file; optional same-name `.png` previews show in the in-game picker when present.

## License

This project is not affiliated with or endorsed by the developers of Heroes of Might and Magic: Olden Era.  
Use generated templates at your own risk.

Official OE templates in `templates/official/` were sourced from the community [Olden Era — Template Generator](https://github.com/KhanDevelopsGames/Olden-Era---Template-Generator) project. See [`LICENSE`](LICENSE) for the full text.
