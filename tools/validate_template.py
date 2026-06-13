#!/usr/bin/env python3
"""Validate an Olden Era .rmg.json template for the 8P/240 isolated-Anarchy spec.

Usage:  python tools/validate_template.py "templates/official/Random Anarchy.rmg.json"

Checks (errors fail; warnings are advisory):
  - parses as JSON
  - sizeX == sizeZ == 240
  - gameRules.encounterHoles == true
  - valueOverrides present with the 7 Anarchy guard sids
  - per variant: exactly 8 distinct spawns Player1..Player8
  - NO `Direct` connection links two spawn zones (isolation)
  - per-zone encounterHolesSettings present (warn)
"""
import json
import re
import sys
from pathlib import Path

ANARCHY_OVERRIDE_SIDS = {
    "boreal_call", "jousting_range", "petrified_memorial",
    "point_of_balance", "the_gorge", "unforgotten_grave", "ritual_pyre",
}


def load_lenient(path: Path):
    text = path.read_text(encoding="utf-8-sig")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # tolerate trailing commas, then retry
        stripped = re.sub(r",(\s*[}\]])", r"\1", text)
        return json.loads(stripped)


def main(argv):
    if len(argv) != 2:
        print(__doc__)
        return 2
    path = Path(argv[1])
    if not path.exists():
        print(f"ERROR: file not found: {path}")
        return 2

    errors, warnings = [], []
    try:
        data = load_lenient(path)
    except json.JSONDecodeError as e:
        print(f"ERROR: JSON parse failed: {e}")
        return 1

    # size
    if data.get("sizeX") != 240 or data.get("sizeZ") != 240:
        errors.append(f"size must be 240x240, got {data.get('sizeX')}x{data.get('sizeZ')}")

    # gameRules
    gr = data.get("gameRules", {})
    if gr.get("encounterHoles") is not True:
        errors.append("gameRules.encounterHoles must be true")
    if gr.get("heroCountMin") != 5 or gr.get("heroCountMax") != 10:
        warnings.append(f"hero count not 5/10 (got {gr.get('heroCountMin')}/{gr.get('heroCountMax')})")

    # valueOverrides
    vo = data.get("valueOverrides")
    if not isinstance(vo, list):
        errors.append("valueOverrides block missing")
    else:
        present = {o.get("sid") for o in vo}
        missing = ANARCHY_OVERRIDE_SIDS - present
        if missing:
            warnings.append(f"valueOverrides missing sids: {sorted(missing)}")

    # variants
    variants = data.get("variants", [])
    if not variants:
        errors.append("no variants")
    for vi, variant in enumerate(variants):
        zones = variant.get("zones", [])
        zone_players = {}  # zone name -> set of players spawning there
        spawns = []
        zones_missing_holes = []
        for z in zones:
            players = set()
            for mo in z.get("mainObjects", []):
                if mo.get("type") == "Spawn" and "spawn" in mo:
                    spawns.append(mo["spawn"])
                    players.add(mo["spawn"])
            if players:
                zone_players[z.get("name")] = players
            if "encounterHolesSettings" not in z:
                zones_missing_holes.append(z.get("name"))
        spawn_zone_names = set(zone_players)

        # exactly 8 distinct Player1..8
        expected = {f"Player{i}" for i in range(1, 9)}
        got = set(spawns)
        if got != expected:
            errors.append(f"variant[{vi}] spawns != Player1..8 (got {sorted(got)}, dupes={len(spawns)!=len(got)})")

        # isolation: no Direct connection between zones hosting DIFFERENT players
        # (same-player alternate-spawn zones may legitimately be linked)
        for c in variant.get("connections", []):
            if c.get("connectionType") == "Direct":
                f, t = c.get("from"), c.get("to")
                if f in spawn_zone_names and t in spawn_zone_names:
                    if zone_players[f] != zone_players[t]:
                        errors.append(f"variant[{vi}] Direct connection links rival spawns: "
                                      f"{f}{sorted(zone_players[f])} <-> {t}{sorted(zone_players[t])} "
                                      f"({c.get('name','unnamed')})")

        if zones_missing_holes:
            warnings.append(f"variant[{vi}] zones missing encounterHolesSettings: {zones_missing_holes}")

        print(f"variant[{vi}]: {len(zones)} zones, {len(spawn_zone_names)} spawn zones, "
              f"{len(variant.get('connections', []))} connections")

    print()
    for w in warnings:
        print(f"WARN : {w}")
    for e in errors:
        print(f"ERROR: {e}")
    print()
    if errors:
        print(f"FAIL ({len(errors)} error(s), {len(warnings)} warning(s))")
        return 1
    print(f"PASS ({len(warnings)} warning(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
