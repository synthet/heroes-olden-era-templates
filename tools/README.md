# Tools

Python CLI utilities for parsing H3 templates, summarizing OE topology, scaffolding ports, and validation. Stdlib only — no `requirements.txt`.

Run from repo root or from `tools/` (scripts import `paths.py` for repo-relative locations).

## Scripts

| Script | Purpose | Example |
|--------|---------|---------|
| `h3t_parser.py` | Parse one `.h3t` / `rmg.txt` → topology JSON | `python tools/h3t_parser.py h3/sources/official/Jebus Cross.h3t` |
| `parse_official_h3.py` | Batch-parse 27 official packs → `h3/layouts/official/` | `python tools/parse_official_h3.py` |
| `oe_template_summary.py` | Summarize OE `.rmg.json` → `h3/layouts/oe/` | `python tools/oe_template_summary.py` |
| `build_h3_oe_matrix.py` | Regenerate `docs/h3/matrix.md` | `python tools/build_h3_oe_matrix.py` |
| `scaffold_h3_port.py` | Scaffold `templates/h3-port/` from OE bases | `python tools/scaffold_h3_port.py` |
| `validate_rmg.py` | **Structural** validation (all templates) | `python tools/validate_rmg.py templates/` |
| `validate_template.py` | **Anarchy 8P/240** isolated spawn checker | `python tools/validate_template.py templates/max8/Octo Anarchy.rmg.json` |
| `publish.py` | Sync `templates/` to public `main` branch | `python tools/publish.py --push` |

## Publish workflow

See [`../docs/publish.md`](../docs/publish.md). From the `dev` branch:

```bash
python tools/validate_rmg.py templates/
python tools/publish.py --push -m "Update published templates."
```

## Typical regen workflow

```bash
python tools/oe_template_summary.py
python tools/parse_official_h3.py
python tools/build_h3_oe_matrix.py
python tools/scaffold_h3_port.py
python tools/validate_rmg.py templates/
```

## Path map

All repo paths are centralized in [`paths.py`](paths.py). Edit there when relocating folders.
