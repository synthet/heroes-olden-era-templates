# heroes-templates

RMG template repo for **Heroes of Might and Magic Olden Era** with H3 HotA tournament porting.

## Layout

- `templates/` — deployable `.rmg.json` (`official/`, `max8/`, `h3-port/`)
- `data/` — engine content pools, encounters, generator config
- `lib/` — OE lookup JSON catalogs
- `h3/` — H3 `.h3t` sources and parsed topology
- `docs/` — start at `docs/README.md`
- `tools/` — parsers, validators (`paths.py` centralizes paths)

## Rules

- Clone-and-mutate from `templates/official/` — never blank files.
- Structural validation: `python tools/validate_rmg.py`
- Anarchy 8P/240 only: `python tools/validate_template.py`
- Do not hand-edit generated READMEs/matrix (`docs/h3/matrix.md`, `h3/layouts/official/README.md`, `templates/h3-port/README.md`)
- Deploy: see `docs/install.md`

## Skills

- `oe-rmg-authoring` — OE template authoring workflow
- `h3-oe-porting` — H3 tournament port workflow
- `template-preview` — generate PNG preview images (`python tools/render_preview.py`)

## Docs

- Author OE: `docs/oe/cookbook.md` → `docs/oe/rmg-format.md`
- Port H3: `docs/h3/matrix.md` → `docs/h3/tier1-audit.md`
