#!/usr/bin/env python3
"""Parse HotA .h3t / rmg.txt template packs (TSV) into structured topology JSON."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


def _cell(row: list[str], idx: dict[str, int], key: str, default: str = "") -> str:
    i = idx.get(key)
    if i is None or i >= len(row):
        return default
    return row[i].strip()


def _parse_treasure(cell: str) -> list[dict[str, int]]:
    parts = cell.split()
    out: list[dict[str, int]] = []
    i = 0
    while i + 2 < len(parts):
        try:
            out.append({
                "low": int(parts[i]),
                "high": int(parts[i + 1]),
                "density": int(parts[i + 2]),
            })
            i += 3
        except ValueError:
            break
    return out


def _parse_connection(row: list[str], idx: dict[str, int]) -> dict[str, Any] | None:
    z1 = _cell(row, idx, "Zone 1")
    z2 = _cell(row, idx, "Zone 2")
    if not z1 or not z2 or not z1.isdigit() or not z2.isdigit():
        return None
    val = _cell(row, idx, "Value")
    return {
        "from": int(z1),
        "to": int(z2),
        "guard_value": int(val) if val.isdigit() else None,
        "wide": _cell(row, idx, "Wide") == "x",
        "border_guard": _cell(row, idx, "Border Guard") == "x",
        "road": _cell(row, idx, "Road"),
        "type": _cell(row, idx, "Type"),
        "fictive": _cell(row, idx, "Fictive") == "x",
    }


def parse_h3t(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8-sig", errors="replace")
    lines = text.splitlines()
    if len(lines) < 4:
        raise ValueError(f"{path}: expected at least 4 header lines")

    field_names = [c.strip() for c in lines[1].split("\t")]
    sub_fields = [c.strip() for c in lines[2].split("\t")]

    columns: list[str] = []
    last_main = ""
    for main, sub in zip(field_names, sub_fields):
        main = main or last_main
        if main:
            last_main = main
        columns.append(sub if sub else main)

    idx = {k: i for i, k in enumerate(columns)}

    maps: list[dict[str, Any]] = []
    zones: list[dict[str, Any]] = []
    connections: list[dict[str, Any]] = []
    seen_conn: set[tuple[int, int, int | None]] = set()

    def add_connection(conn: dict[str, Any] | None) -> None:
        if not conn:
            return
        key = (conn["from"], conn["to"], conn["guard_value"])
        if key not in seen_conn:
            seen_conn.add(key)
            connections.append(conn)

    for line in lines[3:]:
        if not line.strip():
            continue
        row = line.split("\t")
        name = _cell(row, idx, "Name")
        zone_id = _cell(row, idx, "Id")

        if name and not zone_id and _cell(row, idx, "Minimum Size"):
            maps.append({
                "name": name,
                "min_size": _cell(row, idx, "Minimum Size"),
                "max_size": _cell(row, idx, "Maximum Size"),
                "min_players": _cell(row, idx, "Minimum human positions"),
                "max_players": _cell(row, idx, "Maximum human positions"),
                "mirror": _cell(row, idx, "Mirror") == "x",
                "anarchy": _cell(row, idx, "Anarchy") == "x",
            })
            add_connection(_parse_connection(row, idx))
            continue

        if zone_id and zone_id.isdigit():
            zones.append({
                "id": int(zone_id),
                "map_name": name or None,
                "player": _cell(row, idx, "human start") or None,
                "ai": _cell(row, idx, "computer start") or None,
                "base_size": _cell(row, idx, "Base Size"),
                "junction": _cell(row, idx, "Junction") == "x",
                "treasure": _parse_treasure(_cell(row, idx, "Treasure")),
                "placement": _cell(row, idx, "Placement"),
                "monsters": _cell(row, idx, "Strength"),
            })
            add_connection(_parse_connection(row, idx))
            continue

        add_connection(_parse_connection(row, idx))

    pack_meta = maps[0] if maps else {"name": path.stem}

    return {
        "source": str(path),
        "pack_name": pack_meta.get("name", path.stem),
        "maps": maps,
        "zones": zones,
        "connections": connections,
        "zone_count": len(zones),
        "connection_count": len(connections),
    }


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("Usage: python tools/h3t_parser.py <file.h3t> [out.json]")
        return 2
    src = Path(argv[1])
    data = parse_h3t(src)
    out = Path(argv[2]) if len(argv) > 2 else src.with_suffix(".topology.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, indent=2), encoding="utf-8")
    print(f"Wrote {out} ({data['zone_count']} zones, {data['connection_count']} connections)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
