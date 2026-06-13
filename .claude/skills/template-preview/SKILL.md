---
name: template-preview
description: >-
  Generate PNG preview images for Heroes Olden Era .rmg.json templates. Use when
  asked to create, render, or regenerate the template picker thumbnails / sidecar
  .png previews for OE templates (single file, a folder, or all of templates/).
---

# OE template PNG preview generation

Renders the schematic node-graph the game shows in its template picker, using the legend extracted
from the generator's `TemplatePreviewPngWriter.cs`. A complete template is `Name.rmg.json` **+**
`Name.png`; this skill produces the `.png`.

## Workflow

1. Render with `tools/render_preview.py` (Pillow):
   ```bash
   python tools/render_preview.py                              # all of templates/{official,max8,h3-port}
   python tools/render_preview.py "templates/max8/Diamond Ring.rmg.json"   # one file → sidecar .png
   python tools/render_preview.py templates/max8                # a whole folder
   ```
2. Output is a sidecar `<name>.png` next to each input (or pass `--out DIR`).
3. Options: `--size 700` (canvas px, default 700×700 — the game's preview resolution),
   `--title` (caption the template name at the bottom).
4. Verify visually, then deploy the `.rmg.json` + `.png` pair per `docs/install.md`.

## Legend (what the image shows)

- **Green numbered disc** = player spawn (number = player slot).
- **Neutral tier by zone `layout`:** `zone_layout_sides` → bronze, `zone_layout_treasure_zone` →
  silver, `zone_layout_center` → gold; a `Hub`/center zone → blue-grey.
- **Lines:** gold = `Direct`/`Default` connection, blue = `Portal`. `Proximity` links are
  spacing-only and intentionally not drawn.

## Notes & limits

- Layout is a **schematic approximation** (centers middle, spawns outer ring, neutrals inner ring) —
  it conveys topology and roles, not exact in-game geometry. Good enough for the picker thumbnail.
- Reads variant 0; tolerates BOM and trailing commas.
- Requires Pillow (`pip install pillow`). Fonts fall back to a bundled bitmap font if Arial/DejaVu
  are unavailable.

## References

- Renderer: `tools/render_preview.py`
- Preview legend & layout source: `docs/oe/rmg-format.md` (Part III — Reading the PNG preview)
- Templates to render: `templates/{official,max8,h3-port}/`
