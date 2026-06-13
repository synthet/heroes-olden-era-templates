#!/usr/bin/env python3
"""General structural validation for Olden Era .rmg.json templates."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REQUIRED_TOP = {
    "name", "gameMode", "description", "displayWinCondition",
    "sizeX", "sizeZ", "gameRules", "variants",
    "zoneLayouts", "mandatoryContent", "contentCountLimits",
    "contentPools", "contentLists",
}


def load_lenient(path: Path) -> dict:
    text = path.read_text(encoding="utf-8-sig")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return json.loads(re.sub(r",(\s*[}\]])", r"\1", text))


def validate(data: dict, path: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    missing = REQUIRED_TOP - set(data.keys())
    if missing:
        errors.append(f"missing top-level keys: {sorted(missing)}")

    if data.get("sizeX") != data.get("sizeZ"):
        warnings.append(f"non-square map: {data.get('sizeX')}x{data.get('sizeZ')}")

    variants = data.get("variants", [])
    if not variants:
        errors.append("no variants")

    mc_names = {m.get("name") for m in data.get("mandatoryContent", [])}
    ccl_names = {c.get("name") for c in data.get("contentCountLimits", [])}
    zl_names = {z.get("name") for z in data.get("zoneLayouts", [])}

    for vi, variant in enumerate(variants):
        zones = variant.get("zones", [])
        zone_names = {z.get("name") for z in zones}
        if len(zone_names) != len(zones):
            errors.append(f"variant[{vi}]: duplicate zone names")

        for z in zones:
            if z.get("layout") not in zl_names:
                errors.append(f"variant[{vi}] zone {z.get('name')}: unknown layout {z.get('layout')}")
            mc_list = z.get("mandatoryContent", [])
            if isinstance(mc_list, str):
                mc_list = [mc_list]
            for mc in mc_list:
                if mc not in mc_names:
                    errors.append(f"variant[{vi}] zone {z.get('name')}: unknown mandatoryContent {mc}")
            cl_list = z.get("contentCountLimits", [])
            if isinstance(cl_list, str):
                cl_list = [cl_list]
            for cl in cl_list:
                if cl not in ccl_names:
                    errors.append(f"variant[{vi}] zone {z.get('name')}: unknown contentCountLimits {cl}")

        for c in variant.get("connections", []):
            f, t = c.get("from"), c.get("to")
            if f not in zone_names:
                errors.append(f"variant[{vi}] connection {c.get('name')}: unknown from zone {f}")
            if t not in zone_names:
                errors.append(f"variant[{vi}] connection {c.get('name')}: unknown to zone {t}")

    return errors, warnings


def collect_files(path: Path) -> list[Path]:
    if path.is_dir():
        return sorted(path.rglob("*.rmg.json"))
    return [path]


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("Usage: python tools/validate_rmg.py <file.rmg.json|directory> [more...]")
        return 2

    failed = 0
    for arg in argv[1:]:
        for f in collect_files(Path(arg)):
            try:
                data = load_lenient(f)
            except json.JSONDecodeError as e:
                print(f"{f}: PARSE ERROR {e}")
                failed += 1
                continue
            errors, warnings = validate(data, f)
            status = "PASS" if not errors else "FAIL"
            print(f"{f}: {status} ({len(errors)} errors, {len(warnings)} warnings)")
            for w in warnings:
                print(f"  WARN: {w}")
            for e in errors:
                print(f"  ERROR: {e}")
            if errors:
                failed += 1
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
