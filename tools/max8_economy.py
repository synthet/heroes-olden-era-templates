#!/usr/bin/env python3
"""Shared max8 economy scaling helpers (see docs/oe/cookbook.md §2.3)."""

from __future__ import annotations

import copy
import json
import re
from pathlib import Path

TARGET_PX = 240
REF_AREA = 6400

ECONOMY_KEYS = (
    "guardedContentValue",
    "unguardedContentValue",
    "resourcesValue",
    "guardedContentValuePerArea",
    "unguardedContentValuePerArea",
    "resourcesValuePerArea",
)

# Median total budget/tile from native 240×240 official templates (engine formula with zone.size).
LAYOUT_DENSITY_240 = {
    "zone_layout_spawns": 2949.0,  # Full Hire (8 spawns)
    "zone_layout_center": 9178.0,  # Full Hire treasure/connectors
    "zone_layout_treasure_zone": 9178.0,
    "zone_layout_sides": 2949.0,
}


def load_json(path: Path) -> dict:
    text = path.read_text(encoding="utf-8-sig")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return json.loads(re.sub(r",(\s*[}\]])", r"\1", text))


def save_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def scale_int(value: int | float | None, factor: float) -> int:
    if value is None:
        return 0
    return int(round(float(value) * factor))


def zone_tile_area(px: int, zone_count: int, size: float) -> float:
    return (px * px / zone_count) * (size * size)


def content_scale(area: float) -> float:
    return max(0.5, min(2.5, (area / REF_AREA) ** 0.5))


def channel_budget(flat: int | float, per_area: int | float, area: float, cs: float) -> float:
    return flat * cs + per_area * area * (cs**0.5)


def zone_total_budget(zone: dict, px: int, zone_count: int) -> float:
    size = float(zone.get("size", 1.0))
    area = zone_tile_area(px, zone_count, size)
    cs = content_scale(area)
    total = 0.0
    for flat_key, area_key in (
        ("guardedContentValue", "guardedContentValuePerArea"),
        ("unguardedContentValue", "unguardedContentValuePerArea"),
        ("resourcesValue", "resourcesValuePerArea"),
    ):
        total += channel_budget(
            zone.get(flat_key) or 0,
            zone.get(area_key) or 0,
            area,
            cs,
        )
    return total


def zone_density(zone: dict, px: int, zone_count: int) -> float:
    size = float(zone.get("size", 1.0))
    area = zone_tile_area(px, zone_count, size)
    return zone_total_budget(zone, px, zone_count) / area


def scale_zone_economy_from_base(
    zone: dict,
    base_zone: dict,
    old_px: int,
    *,
    extra_flat: float = 1.0,
) -> None:
    """Scale economy from an official base zone to 240px (cookbook: flat × px ratio, per-area × px ratio²)."""
    flat_factor = (TARGET_PX / old_px) * extra_flat
    area_factor = (TARGET_PX / old_px) ** 2 * extra_flat
    for key in ("guardedContentValue", "unguardedContentValue", "resourcesValue"):
        if key in base_zone and base_zone[key] is not None:
            zone[key] = scale_int(base_zone[key], flat_factor)
    for key in (
        "guardedContentValuePerArea",
        "unguardedContentValuePerArea",
        "resourcesValuePerArea",
    ):
        if key in base_zone and base_zone[key]:
            zone[key] = scale_int(base_zone[key], area_factor)
        elif key in zone:
            zone[key] = 0


def normalize_zone_density_to_240(zone: dict, zone_count: int) -> None:
    """Boost zones below native 240×240 density for their layout (fixes flat-only legacy spawns)."""
    layout = zone.get("layout", "")
    target = LAYOUT_DENSITY_240.get(layout)
    if not target:
        return
    current = zone_density(zone, TARGET_PX, zone_count)
    if current <= 0 or current >= target * 0.95:
        return
    boost = target / current
    for key in ECONOMY_KEYS:
        if key in zone and zone[key]:
            zone[key] = scale_int(zone[key], boost)


def scale_content_count_limits(blocks: list[dict], old_px: int) -> None:
    """Raise per-zone caps roughly with map area when upscaling to 240."""
    if old_px >= TARGET_PX:
        return
    factor = (TARGET_PX / old_px) ** 2
    for block in blocks:
        for limit in block.get("limits", []):
            if "maxCount" not in limit:
                continue
            scaled = int(round(limit["maxCount"] * factor))
            if limit["maxCount"] > 0:
                limit["maxCount"] = max(limit["maxCount"], scaled)
            elif scaled >= 1 and limit.get("includeLists"):
                limit["maxCount"] = scaled


def scale_connection_guards(variant: dict, old_px: int, extra: float = 1.0) -> None:
    factor = (TARGET_PX / old_px) * extra
    for conn in variant.get("connections", []):
        if "guardValue" in conn:
            conn["guardValue"] = scale_int(conn["guardValue"], factor)


def apply_economy_from_base(
    data: dict,
    base: dict,
    old_px: int,
    *,
    extra_flat: float = 1.0,
    normalize_density: bool = True,
) -> None:
    base_zones = {z["name"]: z for z in base["variants"][0]["zones"]}
    variant = data["variants"][0]
    zone_count = len(variant["zones"])
    for zone in variant["zones"]:
        base_zone = base_zones.get(zone["name"])
        if base_zone is None:
            continue
        scale_zone_economy_from_base(zone, base_zone, old_px, extra_flat=extra_flat)
        if normalize_density:
            normalize_zone_density_to_240(zone, zone_count)
    scale_connection_guards(variant, old_px, extra=extra_flat)
    if "contentCountLimits" in base:
        data["contentCountLimits"] = copy.deepcopy(base["contentCountLimits"])
        scale_content_count_limits(data["contentCountLimits"], old_px)
