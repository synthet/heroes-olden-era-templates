#!/usr/bin/env python3
"""Compare effective zone economy budgets across template pairs."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REF_AREA = 6400


def load_json(path: Path) -> dict:
    text = path.read_text(encoding="utf-8-sig")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return json.loads(re.sub(r",(\s*[}\]])", r"\1", text))


def content_scale(px: int, zone_count: int) -> tuple[float, float]:
    area = (px * px) / zone_count
    cs = max(0.5, min(2.5, (area / REF_AREA) ** 0.5))
    return cs, area


def effective_budget(
    zone: dict,
    px: int,
    zone_count: int,
    struct_pct: float = 100.0,
    resource_pct: float = 100.0,
) -> dict[str, float]:
    cs, area = content_scale(px, zone_count)
    sm = struct_pct / 100.0
    rm = resource_pct / 200.0

    def channel(flat_key: str, area_key: str, mult: float) -> float:
        flat = zone.get(flat_key) or 0
        per_area = zone.get(area_key) or 0
        # Document formula (GenerationTuning)
        doc = flat * cs * mult + per_area * (cs**0.5) * mult
        # Hypothesis: per-area term also scales with zone tile area
        with_area = flat * cs * mult + per_area * area * (cs**0.5) * mult
        return doc, with_area

    g_doc, g_area = channel("guardedContentValue", "guardedContentValuePerArea", sm)
    u_doc, u_area = channel("unguardedContentValue", "unguardedContentValuePerArea", sm)
    r_doc, r_area = channel("resourcesValue", "resourcesValuePerArea", rm)
    return {
        "content_scale": cs,
        "zone_area": area,
        "guarded_doc": g_doc,
        "guarded_with_area": g_area,
        "unguarded_doc": u_doc,
        "unguarded_with_area": u_area,
        "resources_doc": r_doc,
        "resources_with_area": r_area,
        "total_doc": g_doc + u_doc + r_doc,
        "total_with_area": g_area + u_area + r_area,
        "density_doc": (g_doc + u_doc + r_doc) / area,
        "density_with_area": (g_area + u_area + r_area) / area,
    }


def density_pct(base: float, scaled: float) -> str:
    if base <= 0:
        return "n/a"
    return f"{100 * scaled / base:.1f}%"


def analyze_pair(base_path: Path, max8_path: Path, old_px: int | None = None) -> None:
    base = load_json(base_path)
    scaled = load_json(max8_path)
    bpx = base["sizeX"]
    mpx = scaled["sizeX"]
    if old_px is None:
        old_px = bpx
    bzones = base["variants"][0]["zones"]
    mzones = scaled["variants"][0]["zones"]
    struct = base.get("gameRules", {}).get("structureDensityPercent", 100)
    resource = base.get("gameRules", {}).get("resourceDensityPercent", 100)

    print(f"\n=== {max8_path.stem} ({old_px}->{mpx}px, {len(bzones)} zones) ===")
    for name in sorted({z["name"] for z in bzones} & {z["name"] for z in mzones}):
        bz = next(z for z in bzones if z["name"] == name)
        mz = next(z for z in mzones if z["name"] == name)
        bb = effective_budget(bz, bpx, len(bzones), struct, resource)
        mb = effective_budget(mz, mpx, len(mzones), struct, resource)
        print(f"  {name}:")
        print(
            f"    zone area {bb['zone_area']:.0f} -> {mb['zone_area']:.0f} "
            f"({density_pct(bb['zone_area'], mb['zone_area'])})"
        )
        print(
            f"    density/tile (doc): {bb['density_doc']:.1f} -> {mb['density_doc']:.1f} "
            f"({density_pct(bb['density_doc'], mb['density_doc'])})"
        )
        print(
            f"    density/tile (+area): {bb['density_with_area']:.1f} -> {mb['density_with_area']:.1f} "
            f"({density_pct(bb['density_with_area'], mb['density_with_area'])})"
        )


def main() -> None:
    pairs = [
        ("official/Spider.rmg.json", "max8/Spider Titan.rmg.json", 208),
        ("official/OctoJebus.rmg.json", "max8/Octo Anarchy.rmg.json", 240),
        ("official/Diamond.rmg.json", "max8/Diamond Colossus.rmg.json", 144),
        ("official/Diamond.rmg.json", "max8/Diamond Ring.rmg.json", 144),
        ("official/Ikarus.rmg.json", "max8/Ikarus Ascendant.rmg.json", 160),
        ("official/Mini-Nostalgia.rmg.json", "max8/Grand Nostalgia.rmg.json", 144),
        ("official/Expanse.rmg.json", "max8/Boundless Expanse.rmg.json", 192),
    ]
    for rel_base, rel_max8, old_px in pairs:
        analyze_pair(ROOT / "templates" / rel_base, ROOT / "templates" / rel_max8, old_px)


if __name__ == "__main__":
    main()
