# H3 HotA reference data

Machine-readable H3 topology extracts and source `.h3t` packs for cross-mapping with Olden Era templates.

## Layout

| Path | Contents |
|------|----------|
| `sources/official/` | 27 GOG tournament `.h3t` packs (canonical source) |
| `sources/community/` | Non-tournament community packs (Balkans, Jebus Cross 2.0, etc.) |
| `layouts/official/` | Parsed topology JSON + `_index.json` (from official `.h3t`) |
| `layouts/oe/` | OE template summaries (zone graphs, guards) |
| `layouts/*.topology.json` | Parsed community `.h3t` topologies |

## Authority

- **Parsed H3 topology:** `layouts/official/*.topology.json` from GOG `.h3t` — supersedes any legacy wiki notes.
- **H3 ↔ OE inventory:** [`docs/h3/matrix.md`](../docs/h3/matrix.md) (generated).
- **Gap analysis:** [`docs/h3/tier1-audit.md`](../docs/h3/tier1-audit.md) (human-written).

## Regenerate

```bash
python tools/oe_template_summary.py
python tools/parse_official_h3.py
python tools/build_h3_oe_matrix.py
```

See [`docs/h3/catalog.md`](../docs/h3/catalog.md) for download sources and [`tools/README.md`](../tools/README.md) for all commands.
