#!/usr/bin/env python3
"""Build max8 co-op corridor templates (2 humans + 6 AI FFA).

Pattern (linear spine):
  P1 — buffer — E1 — buffer — E2 — buffer — E3 — buffer — H — buffer — E4 — … — P2
Cross AI lanes: E1—E4, E2—E5, E3—E6 (direct or via cross-buffer zones in ladder mode).
"""

from __future__ import annotations

import copy
import json
import re
import sys
from pathlib import Path
from typing import Literal

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

# P1/E1-E3 left, P2/E4-E6 right (seat humans on Spawn-A and Spawn-B).
PLAYER_SLOTS = [
    ("Spawn-A", "Player1"),
    ("Spawn-B", "Player2"),
    ("Spawn-C", "Player3"),
    ("Spawn-D", "Player4"),
    ("Spawn-E", "Player5"),
    ("Spawn-F", "Player6"),
    ("Spawn-G", "Player7"),
    ("Spawn-H", "Player8"),
]

CROSS_PAIRS = [
    ("Spawn-C", "Spawn-F"),
    ("Spawn-D", "Spawn-G"),
    ("Spawn-E", "Spawn-H"),
]

LINEAR_SPINE = [
    "Spawn-A",
    "Buffer-P1-E1",
    "Spawn-C",
    "Buffer-E1-E2",
    "Spawn-D",
    "Buffer-E2-E3",
    "Spawn-E",
    "Buffer-E3-H",
    "Center",
    "Buffer-H-E4",
    "Spawn-F",
    "Buffer-E4-E5",
    "Spawn-G",
    "Buffer-E5-E6",
    "Spawn-H",
    "Buffer-E6-P2",
    "Spawn-B",
]

BOW_SPINE = [
    "Spawn-A",
    "Buffer-P1-E1",
    "Spawn-C",
    "Buffer-E1-E2",
    "Spawn-D",
    "Buffer-E2-E3",
    "Spawn-E",
    "Buffer-E3-H",
    "Center",
    "Buffer-H-E6",
    "Spawn-H",
    "Buffer-E6-E5",
    "Spawn-G",
    "Buffer-E5-E4",
    "Spawn-F",
    "Buffer-E4-P2",
    "Spawn-B",
]


def load_json(path: Path) -> dict:
    text = path.read_text(encoding="utf-8-sig")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return json.loads(re.sub(r",(\s*[}\]])", r"\1", text))


def save_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from max8_economy import (  # noqa: E402
    normalize_zone_density_to_240,
    scale_connection_guards,
    scale_content_count_limits,
    scale_zone_economy_from_base,
)
from diversify_max8_neutrals import apply_neutral_diversity  # noqa: E402


def stone_road(conn_name: str) -> dict:
    return {
        "type": "Stone",
        "from": {"type": "MainObject", "args": ["0"]},
        "to": {"type": "Connection", "args": [conn_name]},
    }


def direct_conn(
    a: str,
    b: str,
    name: str,
    *,
    guard: int = 15000,
    road: bool = True,
    sim_turn: bool = False,
) -> dict:
    conn = {
        "name": name,
        "from": a,
        "to": b,
        "connectionType": "Direct",
        "road": road,
        "guardValue": guard,
        "guardWeeklyIncrement": 0.2,
    }
    if sim_turn:
        conn["simTurnSquad"] = True
        conn["guardEscape"] = False
    return conn


def spawn_zone(prototype: dict, name: str, player: str) -> dict:
    z = copy.deepcopy(prototype)
    z["name"] = name
    z["layout"] = "zone_layout_spawns"
    z["mainObjects"] = [{"type": "Spawn", "spawn": player, "placement": "Uniform"}]
    z["roads"] = []
    return z


def buffer_zone(
    prototype: dict,
    name: str,
    *,
    layout: str = "zone_layout_treasure_zone",
    mandatory: str = "mandatory_content_treasure",
    limits: str = "content_limits_treasure",
) -> dict:
    z = copy.deepcopy(prototype)
    z["name"] = name
    z["layout"] = layout
    z["mainObjects"] = []
    z["roads"] = []
    z["size"] = 0.7
    z["mandatoryContent"] = [mandatory]
    z["contentCountLimits"] = [limits]
    return z


def center_zone(prototype: dict, *, hold: bool) -> dict:
    z = copy.deepcopy(prototype)
    z["name"] = "Center"
    z["layout"] = "zone_layout_center"
    z["roads"] = []
    if hold:
        z["mainObjects"] = [copy.deepcopy(HOLD_CITY)]
    else:
        z["mainObjects"] = [
            obj for obj in z.get("mainObjects", []) if obj.get("type") != "Spawn"
        ]
    return z


def wire_roads(zone: dict, conn_names: list[str]) -> None:
    zone["roads"] = [stone_road(n) for n in conn_names]


def build_connections(
    spine: list[str],
    *,
    cross_mode: Literal["direct", "ladder"],
) -> tuple[list[dict], list[str]]:
    """Return connections and extra buffer zone names for ladder cross lanes."""
    conns: list[dict] = []
    cross_buffers: list[str] = []

    for i in range(len(spine) - 1):
        a, b = spine[i], spine[i + 1]
        name = f"Spine-{a}-{b}"
        sim = b == "Center" or a == "Center"
        guard = 70000 if sim else 15000
        conns.append(direct_conn(a, b, name, guard=guard, sim_turn=sim))

    if cross_mode == "direct":
        for a, b in CROSS_PAIRS:
            stem = f"Cross-{a}-{b}"
            conns.append(direct_conn(a, b, stem, guard=12000, road=True))
    else:
        for idx, (a, b) in enumerate(CROSS_PAIRS, start=1):
            mid = f"Cross-Buffer-{idx}"
            cross_buffers.append(mid)
            conns.append(direct_conn(a, mid, f"{mid}-{a}", guard=12000))
            conns.append(direct_conn(mid, b, f"{mid}-{b}", guard=12000))

    return conns, cross_buffers


def conn_names_for_zone(zone_name: str, connections: list[dict]) -> list[str]:
    names: list[str] = []
    for c in connections:
        if c["from"] == zone_name or c["to"] == zone_name:
            names.append(c["name"])
    return names


def build_coop_template(
    *,
    shell_path: Path,
    spawn_proto: dict,
    buffer_proto: dict,
    buffer_layout: str,
    buffer_mandatory: str,
    buffer_limits: str,
    center_proto: dict,
    name: str,
    description: str,
    display_win: str,
    spine: list[str],
    cross_mode: Literal["direct", "ladder"],
    center_hold: bool,
    old_px: int,
    economy_extra: float = 1.0,
    guard_extra: float = 1.0,
) -> dict:
    data = load_json(shell_path)
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

    connections, cross_buffers = build_connections(spine, cross_mode=cross_mode)
    zones: list[dict] = []
    player_by_spawn = dict(PLAYER_SLOTS)

    for zn in spine:
        if zn == "Center":
            zones.append(center_zone(center_proto, hold=center_hold))
        elif zn.startswith("Buffer-") or zn.startswith("Cross-Buffer-"):
            zones.append(
                buffer_zone(
                    buffer_proto,
                    zn,
                    layout=buffer_layout,
                    mandatory=buffer_mandatory,
                    limits=buffer_limits,
                )
            )
        elif zn in player_by_spawn:
            zones.append(spawn_zone(spawn_proto, zn, player_by_spawn[zn]))

    for cb in cross_buffers:
        zones.append(
            buffer_zone(
                buffer_proto,
                cb,
                layout=buffer_layout,
                mandatory=buffer_mandatory,
                limits=buffer_limits,
            )
        )

    variant = data["variants"][0]
    variant["orientation"] = {"mode": "MinimalBoundingSquare", "zeroAngleZone": "Spawn-A"}
    variant["zones"] = zones
    variant["connections"] = connections

    zone_count = len(zones)
    for zone in zones:
        wire_roads(zone, conn_names_for_zone(zone["name"], connections))
        scale_zone_economy_from_base(zone, zone, old_px, extra_flat=economy_extra)
        normalize_zone_density_to_240(zone, zone_count)

    scale_connection_guards(variant, old_px, guard_extra)
    if "contentCountLimits" in data:
        scale_content_count_limits(data["contentCountLimits"], old_px)
    apply_neutral_diversity(data)
    return data


def build_hard_place_corridors() -> None:
    shell = load_json(ROOT / "templates/official/Hard Place.rmg.json")
    variant = shell["variants"][0]
    spawn_proto = next(z for z in variant["zones"] if z["name"] == "Spawn-1")
    center_proto = next(z for z in variant["zones"] if z["name"] == "Spawn-Player")
    buffer_proto = copy.deepcopy(spawn_proto)

    data = build_coop_template(
        shell_path=ROOT / "templates/official/Hard Place.rmg.json",
        spawn_proto=spawn_proto,
        buffer_proto=buffer_proto,
        buffer_layout="zone_layout_spawns",
        buffer_mandatory="mandatory_content_side",
        buffer_limits="content_limits_side",
        center_proto=center_proto,
        name="Hard Place Hoard Corridors",
        description="templates_description_pve_hard_place",
        display_win="win_condition_1",
        spine=LINEAR_SPINE,
        cross_mode="direct",
        center_hold=False,
        old_px=144,
        economy_extra=1.5,
        guard_extra=1.5,
    )
    wc = data["gameRules"].setdefault("winConditions", {})
    wc.update(MAX8_WIN_BASE)
    wc["lostStartCity"] = False
    wc["cityHold"] = False

    out = MAX8 / "Hard Place Hoard Corridors.rmg.json"
    save_json(out, data)
    for stale in (
        MAX8 / "Hard Place Hoard.rmg.json",
        MAX8 / "Hard Place Corridors.rmg.json",
    ):
        if stale.exists() and stale != out:
            stale.unlink()
    for stale_png in (
        MAX8 / "Hard Place Hoard.png",
        MAX8 / "Hard Place Corridors.png",
    ):
        if stale_png.exists():
            stale_png.unlink()


def build_ikarus_ladder_dominion() -> None:
    shell = load_json(MAX8 / "Ikarus Showdown.rmg.json")
    variant = shell["variants"][0]
    spawn_proto = next(z for z in variant["zones"] if z["name"] == "Spawn-A")
    buffer_proto = next(z for z in variant["zones"] if z["name"] == "Treasure-1")
    center_proto = next(z for z in variant["zones"] if z["name"] == "Center")

    data = build_coop_template(
        shell_path=MAX8 / "Ikarus Showdown.rmg.json",
        spawn_proto=spawn_proto,
        buffer_proto=buffer_proto,
        buffer_layout="zone_layout_center",
        buffer_mandatory="mandatory_content_treasure",
        buffer_limits="content_limits_treasure",
        center_proto=center_proto,
        name="Ikarus Ladder Dominion",
        description="templates_description_ikarus",
        display_win="win_condition_5",
        spine=LINEAR_SPINE,
        cross_mode="ladder",
        center_hold=True,
        old_px=240,
        economy_extra=1.0,
        guard_extra=1.0,
    )
    wc = data["gameRules"].setdefault("winConditions", {})
    wc.update(MAX8_WIN_BASE)
    wc["lostStartCity"] = False
    wc["cityHold"] = True
    wc["cityHoldDays"] = 6

    out = MAX8 / "Ikarus Ladder Dominion.rmg.json"
    save_json(out, data)
    for stale in (
        MAX8 / "Ikarus Dominion.rmg.json",
        MAX8 / "Ikarus Ladder.rmg.json",
    ):
        if stale.exists() and stale != out:
            stale.unlink()
    for stale_png in (
        MAX8 / "Ikarus Dominion.png",
        MAX8 / "Ikarus Ladder.png",
    ):
        if stale_png.exists():
            stale_png.unlink()


def main() -> None:
    build_hard_place_corridors()
    build_ikarus_ladder_dominion()
    print("Wrote co-op corridor templates.")


if __name__ == "__main__":
    main()
