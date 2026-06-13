# Documentation index

Heroes of Might and Magic **Olden Era** random-map-generator (RMG) templates — authoring specs, lookup data, and H3 HotA porting reference.

## Reading paths

### Author OE templates

1. [`oe/cookbook.md`](oe/cookbook.md) — step-by-step recipes (start here)
2. [`oe/rmg-format.md`](oe/rmg-format.md) — full `.rmg.json` schema reference
3. [`../lib/README.md`](../lib/README.md) — SID/value lookup JSON catalogs
4. [`../data/README.md`](../data/README.md) — bundled content pools, encounters, generator config

### Port H3 HotA tournaments

1. [`h3/matrix.md`](h3/matrix.md) — 27 tournament templates vs OE (generated)
2. [`h3/tier1-audit.md`](h3/tier1-audit.md) — gap analysis for direct-name matches
3. [`h3/catalog.md`](h3/catalog.md) — `.h3t` download sources and parse commands
4. [`../templates/h3-port/`](../templates/h3-port/) — scaffolded missing tournament ports

### Install and deploy

[`install.md`](install.md) — game deploy path, GOG HotA source path, user template folder.

### Tools

[`../tools/README.md`](../tools/README.md) — parsers, validators, regen commands.

## Authority model

| Question | Source |
|----------|--------|
| OE `.rmg.json` schema | [`oe/rmg-format.md`](oe/rmg-format.md) |
| How to author | [`oe/cookbook.md`](oe/cookbook.md) |
| SID / enum lookups | [`../lib/`](../lib/) |
| Engine content pools | [`../data/`](../data/) |
| H3 parsed topology | [`../h3/layouts/official/_index.json`](../h3/layouts/official/_index.json) |
| H3 ↔ OE inventory | [`h3/matrix.md`](h3/matrix.md) |
| H3 gap analysis | [`h3/tier1-audit.md`](h3/tier1-audit.md) |
| Validation | `python tools/validate_rmg.py templates/` |

## External research

[`external/deep-research-report.md`](external/deep-research-report.md) — third-party OE ecosystem notes (editors, competitive pools, licensing). Not maintained as part of the core spec.
