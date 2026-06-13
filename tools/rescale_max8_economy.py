#!/usr/bin/env python3
"""Rescale max8 template economy from official bases (cookbook §2.3, §8.A).

Fixes under-scaled per-area budgets (was sqrt(px ratio, should be px ratio²) and
raises flat-only legacy spawn zones to native 240×240 density (Full Hire reference).
"""

from __future__ import annotations

import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from max8_economy import apply_economy_from_base, load_json, save_json

ROOT = TOOLS.parent
MAX8 = ROOT / "templates" / "max8"

# (max8 file, base path relative to templates/, source px, extra flat multiplier)
DIRECT_RESCALES: list[tuple[str, str, int, float]] = [
    ("Spider Titan.rmg.json", "official/Spider.rmg.json", 208, 1.0),
    ("Octo Anarchy.rmg.json", "official/OctoJebus.rmg.json", 240, 1.0),
    ("Diamond Colossus.rmg.json", "official/Diamond.rmg.json", 144, 1.0),
    ("Diamond Ring.rmg.json", "official/Diamond.rmg.json", 144, 1.0),
    ("Ikarus Ascendant.rmg.json", "official/Ikarus.rmg.json", 160, 1.0),
    ("Ikarus Showdown.rmg.json", "official/Ikarus.rmg.json", 160, 1.0),
    ("Grand Nostalgia.rmg.json", "official/Mini-Nostalgia.rmg.json", 144, 1.0),
    ("Boundless Expanse.rmg.json", "official/Expanse.rmg.json", 192, 1.0),
]


def rescale_direct(max8_name: str, base_rel: str, old_px: int, extra_flat: float) -> None:
    max8_path = MAX8 / max8_name
    base_path = ROOT / "templates" / base_rel
    data = load_json(max8_path)
    base = load_json(base_path)
    apply_economy_from_base(
        data,
        base,
        old_px,
        extra_flat=extra_flat,
        normalize_density=True,
    )
    save_json(max8_path, data)
    print(f"Rescaled {max8_name} from {base_rel} ({old_px}px)")


def main() -> None:
    for max8_name, base_rel, old_px, extra_flat in DIRECT_RESCALES:
        rescale_direct(max8_name, base_rel, old_px, extra_flat)

    # Topology variants share economy helpers but rebuild zone graphs too.
    from build_coop_corridor import build_hard_place_corridors, build_ikarus_ladder_dominion
    from rework_max8_variants import build_antares_maelstrom, build_boomerang_crown

    build_antares_maelstrom()
    build_boomerang_crown()
    build_hard_place_corridors()
    build_ikarus_ladder_dominion()
    print("Rebuilt Antares Maelstrom, Boomerang Crown, co-op corridor maps.")


if __name__ == "__main__":
    main()
