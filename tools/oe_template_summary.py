#!/usr/bin/env python3
"""Summarize Olden Era .rmg.json template topology for H3 cross-reference."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

from paths import H3_LAYOUTS_OE, TEMPLATES_OFFICIAL


def load_lenient(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8-sig")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return json.loads(re.sub(r",(\s*[}\]])", r"\1", text))


def summarize(path: Path) -> dict[str, Any]:
    data = load_lenient(path)
    variants_out = []
    for vi, variant in enumerate(data.get("variants", [])):
        zones = variant.get("zones", [])
        zone_names = [z.get("name") for z in zones]
        spawns = []
        cities = []
        for z in zones:
            for mo in z.get("mainObjects", []):
                if mo.get("type") == "Spawn":
                    spawns.append({"zone": z.get("name"), "player": mo.get("spawn")})
                if mo.get("type") == "City":
                    cities.append(z.get("name"))
        conns = []
        for c in variant.get("connections", []):
            if c.get("connectionType") in ("Direct", "Default", "Portal"):
                conns.append({
                    "from": c.get("from"),
                    "to": c.get("to"),
                    "type": c.get("connectionType"),
                    "guard": c.get("guardValue"),
                    "road": c.get("road"),
                })
        variants_out.append({
            "index": vi,
            "zone_count": len(zones),
            "zones": zone_names,
            "spawn_zones": spawns,
            "city_zones": cities,
            "connections": conns,
        })
    return {
        "file": path.name,
        "name": data.get("name"),
        "description_key": data.get("description"),
        "size": f"{data.get('sizeX')}x{data.get('sizeZ')}",
        "game_mode": data.get("gameMode"),
        "encounter_holes": data.get("gameRules", {}).get("encounterHoles"),
        "variant_count": len(variants_out),
        "variants": variants_out,
    }


def collect_templates(root: Path) -> list[Path]:
    if root.is_file():
        return [root]
    return sorted(root.rglob("*.rmg.json"))


def main(argv: list[str]) -> int:
    root = Path(argv[1]) if len(argv) > 1 else TEMPLATES_OFFICIAL
    out_dir = Path(argv[2]) if len(argv) > 2 else H3_LAYOUTS_OE
    out_dir.mkdir(parents=True, exist_ok=True)

    all_summaries = []
    for path in collect_templates(root):
        if "h3-port" in path.parts:
            continue
        s = summarize(path)
        all_summaries.append(s)
        (out_dir / f"{path.stem}.summary.json").write_text(
            json.dumps(s, indent=2), encoding="utf-8"
        )

    index = out_dir / "_index.json"
    index.write_text(json.dumps(all_summaries, indent=2), encoding="utf-8")
    print(f"Summarized {len(all_summaries)} templates -> {out_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
