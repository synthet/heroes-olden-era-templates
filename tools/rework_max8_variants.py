#!/usr/bin/env python3
"""Rebuild the four max8 flavor variants with distinct topologies (see max8 README)."""

from __future__ import annotations

import copy
import json
import re
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from build_coop_corridor import build_hard_place_corridors, build_ikarus_ladder_dominion
from max8_economy import (
    normalize_zone_density_to_240,
    scale_connection_guards,
    scale_content_count_limits,
    scale_int,
    scale_zone_economy_from_base,
)
from diversify_max8_neutrals import apply_neutral_diversity

ROOT = Path(__file__).resolve().parent.parent
MAX8 = ROOT / "templates" / "max8"
TARGET_PX = 240

HOLD_CITY = {
    "type": "City",
    "guardChance": 1.0,
    "guardValue": 20000,
    "guardWeeklyIncrement": 0.2,
    "buildingsConstructionSid": "poor_buildings_construction",
    "placement": "Center",
    "holdCityWinCon": True,
}

MAX8_WIN_BASE = {
    "classic": True,
    "desertion": True,
    "desertionDay": 3,
    "desertionValue": 3000,
    "heroLighting": True,
    "heroLightingDay": 1,
    "lostStartHero": False,
    "lostStartCityDay": 3,
}


def load_json(path: Path) -> dict:
    text = path.read_text(encoding="utf-8-sig")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return json.loads(re.sub(r",(\s*[}\]])", r"\1", text))


def save_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def apply_max8_shell(data: dict, name: str, description: str, display_win: str, old_px: int) -> None:
    data["name"] = name
    data["description"] = description
    data["displayWinCondition"] = display_win
    data["sizeX"] = TARGET_PX
    data["sizeZ"] = TARGET_PX
    gr = data.setdefault("gameRules", {})
    gr["heroCountMin"] = 5
    gr["heroCountMax"] = 10
    gr["heroCountIncrement"] = 1
    gr["heroHireBan"] = False
    for key in ("factionLawsExpModifier", "astrologyExpModifier"):
        gr.pop(key, None)
    variant = data["variants"][0]
    zone_count = len(variant["zones"])
    for zone in variant["zones"]:
        scale_zone_economy_from_base(zone, zone, old_px)
        normalize_zone_density_to_240(zone, zone_count)
    scale_connection_guards(variant, old_px)
    if "contentCountLimits" in data:
        scale_content_count_limits(data["contentCountLimits"], old_px)


def multiply_zone_economy(zone: dict, factor: float) -> None:
    for key in (
        "guardedContentValue",
        "unguardedContentValue",
        "resourcesValue",
        "guardedContentValuePerArea",
        "unguardedContentValuePerArea",
        "resourcesValuePerArea",
    ):
        if key in zone and zone[key]:
            zone[key] = scale_int(zone[key], factor)


def multiply_connection_guards(variant: dict, factor: float) -> None:
    for conn in variant.get("connections", []):
        if "guardValue" in conn:
            conn["guardValue"] = scale_int(conn["guardValue"], factor)


def drop_roads_to_connections(variant: dict, conn_names: set[str]) -> None:
    for zone in variant["zones"]:
        roads = zone.get("roads", [])
        if not roads:
            continue
        kept = []
        for road in roads:
            refs = []
            for end in ("from", "to"):
                ref = road.get(end, {})
                if ref.get("type") == "Connection":
                    refs.append(ref.get("args", [None])[0])
            if any(name in conn_names for name in refs):
                continue
            kept.append(road)
        zone["roads"] = kept


def stone_road(conn_name: str) -> dict:
    return {
        "type": "Stone",
        "from": {"type": "MainObject", "args": ["0"]},
        "to": {"type": "Connection", "args": [conn_name]},
    }


def zone_by_name(variant: dict, name: str) -> dict:
    for zone in variant["zones"]:
        if zone["name"] == name:
            return zone
    raise KeyError(name)


def ensure_road(zone: dict, conn_name: str) -> None:
    roads = zone.setdefault("roads", [])
    for road in roads:
        ref = road.get("to", {})
        if ref.get("type") == "Connection" and ref.get("args") == [conn_name]:
            return
    roads.append(stone_road(conn_name))


def spawn_treasure_link(
    variant: dict, spawn: str, treasure: str, conn_name: str, guard_value: int = 10000
) -> None:
    variant["connections"].append(
        {
            "name": conn_name,
            "from": spawn,
            "to": treasure,
            "connectionType": "Direct",
            "road": True,
            "guardValue": guard_value,
            "guardWeeklyIncrement": 0.2,
        }
    )
    ensure_road(zone_by_name(variant, spawn), conn_name)
    ensure_road(zone_by_name(variant, treasure), conn_name)


def treasure_center_link(
    variant: dict, treasure: str, conn_name: str, guard_value: int = 70000
) -> None:
    variant["connections"].append(
        {
            "name": conn_name,
            "from": treasure,
            "to": "Center",
            "connectionType": "Direct",
            "road": True,
            "guardValue": guard_value,
            "guardEscape": False,
            "simTurnSquad": True,
            "guardWeeklyIncrement": 0.2,
        }
    )
    ensure_road(zone_by_name(variant, treasure), conn_name)
    ensure_road(zone_by_name(variant, "Center"), conn_name)


def apply_maelstrom_supertreasure_forks(variant: dict) -> None:
    """Mirror-Antares chaos: T3/T4 each fork to SuperTreasure-1 and their own outer node."""
    existing = {c["name"] for c in variant["connections"]}
    for treasure, super_t, stem in (
        ("Treasure-3", "SuperTreasure-1", "Treasure-3-SuperTreasure-1"),
        ("Treasure-4", "SuperTreasure-1", "Treasure-4-SuperTreasure-1"),
    ):
        for suffix in ("", " 2"):
            name = stem + suffix
            if name in existing:
                continue
            variant["connections"].append(
                {
                    "name": name,
                    "from": treasure,
                    "to": super_t,
                    "connectionType": "Default",
                    "road": False,
                    "guardValue": 9000,
                    "guardWeeklyIncrement": 0.2,
                }
            )


def build_antares_maelstrom() -> None:
    src = load_json(ROOT / "templates/h3-port/mt_Antares.rmg.json")
    variant = src["variants"][0]
    apply_maelstrom_supertreasure_forks(variant)
    apply_max8_shell(
        src,
        "Antares Maelstrom",
        "templates_description_mt_antares",
        "win_condition_1",
        144,
    )
    src["gameRules"]["encounterHoles"] = True
    wc = src["gameRules"].setdefault("winConditions", {})
    wc.update(MAX8_WIN_BASE)
    wc["lostStartCity"] = False
    apply_neutral_diversity(src)
    save_json(MAX8 / "Antares Maelstrom.rmg.json", src)


def build_hard_place_hoard() -> None:
    build_hard_place_corridors()


def build_ikarus_dominion() -> None:
    build_ikarus_ladder_dominion()


def spawn_zone_names(variant: dict) -> set[str]:
    names: set[str] = set()
    for zone in variant["zones"]:
        for obj in zone.get("mainObjects", []):
            if obj.get("type") == "Spawn":
                names.add(zone["name"])
    return names


def build_boomerang_crown() -> None:
    src = load_json(ROOT / "templates/h3-port/Boomerang.rmg.json")
    variant = src["variants"][0]
    spawn_names = spawn_zone_names(variant)

    removed = [
        c
        for c in variant["connections"]
        if c["from"] in spawn_names and c["to"] in spawn_names and c["from"] != c["to"]
    ]
    removed_names = {c["name"] for c in removed}
    variant["connections"] = [c for c in variant["connections"] if c["name"] not in removed_names]
    drop_roads_to_connections(variant, removed_names)

    # Original Boomerang tips (Spawn-A/B) shortcut straight to Center; drop all spawn→Center
    # links so every player routes spawn → arm treasure → Center (buffered boomerang).
    removed_center = {
        c["name"]
        for c in variant["connections"]
        if c["to"] == "Center" and c["from"] in spawn_names
    }
    variant["connections"] = [
        c for c in variant["connections"] if c["name"] not in removed_center
    ]
    drop_roads_to_connections(variant, removed_center)

    spawn_treasure_link(variant, "Spawn-A", "Treasure-1", "Spawn-A-Treasure-1")
    spawn_treasure_link(variant, "Spawn-B", "Treasure-6", "Spawn-B-Treasure-6")
    for i in range(1, 7):
        treasure_center_link(variant, f"Treasure-{i}", f"Treasure-{i}-Center")

    center = zone_by_name(variant, "Center")
    center["mainObjects"] = [copy.deepcopy(HOLD_CITY)]

    apply_max8_shell(
        src,
        "Boomerang Crown",
        "templates_description_boomerang",
        "win_condition_5",
        144,
    )

    wc = src["gameRules"].setdefault("winConditions", {})
    wc.update(MAX8_WIN_BASE)
    wc["lostStartCity"] = True
    wc["cityHold"] = True
    wc["cityHoldDays"] = 6

    apply_neutral_diversity(src)
    save_json(MAX8 / "Boomerang Crown.rmg.json", src)


def main() -> None:
    build_antares_maelstrom()
    build_hard_place_hoard()
    build_ikarus_dominion()
    build_boomerang_crown()
    print("Wrote four max8 flavor variants.")


if __name__ == "__main__":
    main()
