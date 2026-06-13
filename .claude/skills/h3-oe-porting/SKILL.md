---
name: h3-oe-porting
description: >-
  Port Heroes 3 HotA tournament RMG templates to Olden Era format. Use when working
  with .h3t files, H3 topology, tournament template ports, h3-port scaffolds,
  PG guard values, or H3-OE matrix comparisons.
---

# H3 → OE tournament porting

## Workflow

1. Check inventory: `docs/h3/matrix.md` (match status, OE base).
2. Read H3 topology: `h3/layouts/official/{name}.topology.json` and comparison table in `h3/layouts/official/README.md`.
3. Compare OE summary: `h3/layouts/oe/{base}.summary.json`.
4. Start from scaffold in `templates/h3-port/` if present; otherwise clone nearest `templates/official/` base.
5. Tune zone graph, PG guards, economy to H3 parsed data.
6. Consult gap analysis: `docs/h3/tier1-audit.md`.
7. Validate: `python tools/validate_rmg.py templates/h3-port/Your Name.rmg.json`

## H3 size → OE px (ports)

M-U ≈ 96, L±U ≈ 144/160, XL±U ≈ 208.

## Regenerate derived data

```bash
python tools/oe_template_summary.py
python tools/parse_official_h3.py
python tools/build_h3_oe_matrix.py
python tools/scaffold_h3_port.py
```

See `tools/README.md` and `h3/README.md`.

## Do not edit

Auto-generated: `docs/h3/matrix.md`, `h3/layouts/official/README.md`, `templates/h3-port/README.md`.
