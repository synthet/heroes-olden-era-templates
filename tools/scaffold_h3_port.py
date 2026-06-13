#!/usr/bin/env python3
"""Scaffold H3 tournament template ports into templates/h3-port/ from OE base templates."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from paths import TEMPLATES_H3_PORT, TEMPLATES_OFFICIAL

SCAFFOLDS: dict[str, dict] = {
    "Nostalgia": {
        "base": "Mini-Nostalgia",
        "size": 208,
        "description": "templates_description_nostalgia",
        "display_win": "win_condition_3",
        "notes": "XL+U scale-up of Mini-Nostalgia; H3 richness 53/244/292",
    },
    "Boomerang": {
        "base": "Mini-Nostalgia",
        "size": 144,
        "description": "templates_description_boomerang",
        "display_win": "win_condition_1",
        "notes": "L+U; many zones + rich central treasures (H3 preset 55/242)",
    },
    "Apocalypse": {
        "base": "Diamond",
        "size": 144,
        "description": "templates_description_apocalypse",
        "display_win": "win_condition_1",
        "notes": "L+U underground starts; sand surface zones",
    },
    "Black'n'Blue": {
        "base": "Jebus Cross Classic",
        "size": 144,
        "description": "templates_description_black_n_blue",
        "display_win": "win_condition_1",
        "notes": "L+U; Necropolis pairing rules in lobby",
    },
    "2sm4d(3)": {
        "base": "Diamond",
        "size": 144,
        "description": "templates_description_2sm4d",
        "display_win": "win_condition_1",
        "notes": "L+U legacy template; roadless treasure links",
    },
    "Firewalk": {
        "base": "Jebus Cross",
        "size": 208,
        "description": "templates_description_firewalk",
        "display_win": "win_condition_5",
        "notes": "XL+U dynamic; custom object rules per h3hota",
    },
    "Clash of Dragons": {
        "base": "Anarchy",
        "size": 208,
        "description": "templates_description_clash_of_dragons",
        "display_win": "win_condition_1",
        "encounter_holes": True,
        "notes": "XL+U diplomacy/dragon utopia focus",
    },
    "6lm10a": {
        "base": "Spider",
        "size": 208,
        "description": "templates_description_6lm10a",
        "display_win": "win_condition_1",
        "notes": "XL+U branched; 5 road layout variants in H3",
    },
    "8mm6a": {
        "base": "Crossroads",
        "size": 208,
        "description": "templates_description_8mm6a",
        "display_win": "win_condition_1",
        "notes": "XL+U contact template; central treasure clash",
    },
    "8xm12a": {
        "base": "Expanse",
        "size": 208,
        "description": "templates_description_8xm12a",
        "display_win": "win_condition_1",
        "notes": "XL+U exploration; rich central zone",
    },
    "h3dm1": {
        "base": "Symmetry",
        "size": 144,
        "description": "templates_description_h3dm1",
        "display_win": "win_condition_1",
        "notes": "Mirror L-U; start > secondary > treasure chain",
    },
    "mt_Jebus": {
        "base": "Jebus Cross Classic",
        "size": 160,
        "description": "templates_description_mt_jebus",
        "display_win": "win_condition_5",
        "notes": "Mirror L-U Jebus Cross variant",
    },
    "mt_Diamond": {
        "base": "Fair'n Square",
        "size": 144,
        "description": "templates_description_mt_diamond",
        "display_win": "win_condition_1",
        "notes": "Mirror L-U Diamond variant",
    },
    "mt_TeamJebus": {
        "base": "OctoJebus",
        "size": 160,
        "description": "templates_description_mt_teamjebus",
        "display_win": "win_condition_5",
        "notes": "Mirror 2v2 Jebus; ally zones not directly linked",
    },
    "mt_Andromeda": {
        "base": "Universe",
        "size": 208,
        "description": "templates_description_mt_andromeda",
        "display_win": "win_condition_1",
        "notes": "Mirror XL-U contactless exploration",
    },
    "mt_Antares": {
        "base": "Spider",
        "size": 144,
        "description": "templates_description_mt_antares",
        "display_win": "win_condition_1",
        "notes": "Mirror L-U early contact",
    },
    "mt_Firewalk": {
        "base": "Firewalk",
        "size": 160,
        "description": "templates_description_mt_firewalk",
        "display_win": "win_condition_5",
        "notes": "Mirror Firewalk; depends on Firewalk scaffold",
    },
    "2sm2c(2)": {
        "base": "Blitz",
        "size": 96,
        "description": "templates_description_2sm2c",
        "display_win": "win_condition_1",
        "notes": "M-U 200% template",
    },
    "Skirmish(M)": {
        "base": "Blitz",
        "size": 96,
        "description": "templates_description_skirmish_m",
        "display_win": "win_condition_1",
        "notes": "M-U 200% skirmish",
    },
    "Nine-day Wonder": {
        "base": "Sprint",
        "size": 96,
        "description": "templates_description_nine_day_wonder",
        "display_win": "win_condition_1",
        "notes": "M-U 200%; custom object value settings in H3",
    },
}


def load_lenient(path: Path) -> dict:
    text = path.read_text(encoding="utf-8-sig")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return json.loads(re.sub(r",(\s*[}\]])", r"\1", text))


def _normalize_zone_refs(data: dict) -> None:
    for variant in data.get("variants", []):
        for zone in variant.get("zones", []):
            for key in ("mandatoryContent", "contentCountLimits"):
                val = zone.get(key)
                if isinstance(val, str):
                    zone[key] = [val]


def apply_scaffold(name: str, cfg: dict) -> None:
    base_stem = cfg["base"]
    base_path = TEMPLATES_H3_PORT / f"{base_stem}.rmg.json"
    if not base_path.exists():
        base_path = TEMPLATES_OFFICIAL / f"{base_stem}.rmg.json"
    if not base_path.exists():
        raise FileNotFoundError(base_path)
    data = load_lenient(base_path)
    _normalize_zone_refs(data)
    for variant in data.get("variants", []):
        for zone in variant.get("zones", []):
            mc = zone.get("mandatoryContent", [])
            if isinstance(mc, list):
                zone["mandatoryContent"] = [
                    "mandatory_content_treasure_1" if x == "mandatory_content_treasur_1" else x
                    for x in mc
                ]
    data["name"] = name
    data["description"] = cfg["description"]
    if cfg.get("display_win"):
        data["displayWinCondition"] = cfg["display_win"]
    size = cfg.get("size")
    if size:
        data["sizeX"] = size
        data["sizeZ"] = size
    if "encounter_holes" in cfg:
        data.setdefault("gameRules", {})["encounterHoles"] = cfg["encounter_holes"]

    out_path = TEMPLATES_H3_PORT / f"{name}.rmg.json"
    out_path.write_text(json.dumps(data, indent="\t", ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"  {name} <- {cfg['base']} ({size}x{size})")


def main() -> int:
    TEMPLATES_H3_PORT.mkdir(parents=True, exist_ok=True)
    order = [k for k in SCAFFOLDS if k != "mt_Firewalk"] + ["mt_Firewalk"]
    print(f"Scaffolding {len(order)} H3 tournament ports -> {TEMPLATES_H3_PORT}")
    for name in order:
        apply_scaffold(name, SCAFFOLDS[name])

    readme = TEMPLATES_H3_PORT / "README.md"
    lines = [
        "# H3 HotA Tournament Template Ports",
        "",
        "> Auto-generated by `tools/scaffold_h3_port.py`. Do not edit by hand.",
        "",
        "Scaffolded from closest Olden Era templates. Each file inherits zone topology",
        "from its base template; names, sizes, and description keys target H3 tournament specs.",
        "",
        f"See [`docs/h3/matrix.md`](../../docs/h3/matrix.md) for cross-reference.",
        "",
        "| Template | Base | H3 size | Status |",
        "|----------|------|---------|--------|",
    ]
    for name, cfg in SCAFFOLDS.items():
        lines.append(
            f"| {name} | {cfg['base']} | {cfg.get('size', '?')} | scaffold — {cfg['notes']} |"
        )
    readme.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {readme}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
