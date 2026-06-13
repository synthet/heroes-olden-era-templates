---
name: oe-rmg-authoring
description: >-
  Author and validate Heroes Olden Era .rmg.json random-map templates. Use when
  creating, editing, or reviewing OE RMG templates, zone graphs, economy, content
  pools, validation errors, or deploy questions.
---

# OE RMG template authoring

## Workflow

1. Read the target in `docs/oe/cookbook.md` (recipes) and field semantics in `docs/oe/rmg-format.md`.
2. Clone the nearest official template from `templates/official/` — never start blank.
3. Edit identity (`name`, `description`, `sizeX`/`sizeZ`), zone graph, economy, rules.
4. Resolve SIDs via `lib/` (lookups) and `data/` (pools, lists, encounters).
5. Validate: `python tools/validate_rmg.py templates/official/Your Name.rmg.json`
6. Deploy per `docs/install.md`.

## Key constraints

- 32 zone cap; `sizeX == sizeZ`.
- Isolation: no `Direct` link between rival spawn zones.
- Pools/lists/layouts are external SIDs; mandatoryContent/contentCountLimits are inline refs.

## References

- Recipes: `docs/oe/cookbook.md`
- Schema: `docs/oe/rmg-format.md`
- Lookups: `lib/README.md`, `data/README.md`
- Checklist: `docs/oe/cookbook.md` §10
