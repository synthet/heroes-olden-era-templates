# Heroes Olden Era Map Templates

Random Map Generator (RMG) template files for **Heroes of Might and Magic Olden Era**, plus research and ports for [HotA tournament templates](https://h3hota.com/en/rules#template-rules).

**Start here:** [`docs/README.md`](docs/README.md)

## Quick links

| Task | Doc |
|------|-----|
| Author a new OE template | [`docs/oe/cookbook.md`](docs/oe/cookbook.md) |
| Field reference | [`docs/oe/rmg-format.md`](docs/oe/rmg-format.md) |
| Install / deploy | [`docs/install.md`](docs/install.md) |
| Publish to GitHub | [`docs/publish.md`](docs/publish.md) |
| H3 ↔ OE matrix | [`docs/h3/matrix.md`](docs/h3/matrix.md) |
| H3 gap analysis | [`docs/h3/tier1-audit.md`](docs/h3/tier1-audit.md) |
| Tools | [`tools/README.md`](tools/README.md) |

## Repo layout

```
templates/   → ship to game (official, max8, h3-port)
data/        → engine content pools & encounters
lib/         → SID/value lookup JSON
h3/          → H3 sources & parsed topology
docs/        → authoring & porting docs
tools/       → parsers, validators, publish script
```

Copy contents of `templates/` into the game's `StreamingAssets\map_templates\` folder — see [`docs/install.md`](docs/install.md).

Public template-only release: [`docs/publish.md`](docs/publish.md) (`main` branch on GitHub).
