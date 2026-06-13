#!/usr/bin/env python3
"""Assign unique value-balanced mandatory packs to max8 neutral zones.

Reads pack definitions from lib/max8_neutral_packs.json and wires per-zone
mandatoryContent blocks. Peer zones within a tier keep equal total pool budget
after mandatory-value compensation.
"""

from __future__ import annotations

import copy
import re
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
ROOT = TOOLS.parent
MAX8 = ROOT / "templates" / "max8"
PACKS_PATH = ROOT / "lib" / "max8_neutral_packs.json"

if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from max8_economy import load_json, save_json, zone_total_budget  # noqa: E402

TARGET_PX = 240

# Generic block names replaced by numbered packs per tier.
SUPERSEDED_MANDATORY = {
    "mandatory_content_treasure",
    "mandatory_content_connector",
    "mandatory_content_supertreasure",
    "mandatory_content_side",
    "mandatory_content_buffer",
}

ROAD_RULE = {"type": "Road", "args": [], "targetMin": 0.15, "targetMax": 0.3, "weight": 1}


def load_packs() -> dict:
    return load_json(PACKS_PATH)


def pack_score(content: list, value_scores: dict) -> int:
    total = 0
    for item in content:
        if "includeLists" in item:
            total += value_scores.get("random_hire_list", 4000)
            continue
        sid = item.get("sid")
        if sid:
            total += value_scores.get(sid, 0)
    return total


def annotate_pack_scores(packs_lib: dict) -> None:
    scores = packs_lib["valueScores"]
    for tier in packs_lib["tiers"].values():
        for pack in tier["packs"]:
            pack["valueScore"] = pack_score(pack["content"], scores)
    for pack in packs_lib["centerRefresh"]:
        pack["valueScore"] = pack_score(pack["content"], scores)


def find_mandatory_block(data: dict, name: str) -> dict | None:
    for block in data.get("mandatoryContent", []):
        if block.get("name") == name:
            return block
    return None


def mandatory_content_sids(block: dict | None) -> set[str]:
    if not block:
        return set()
    sids: set[str] = set()
    for item in block.get("content", []):
        if "sid" in item:
            sids.add(item["sid"])
        if "includeLists" in item:
            sids.add("__includeLists__")
    return sids


def detect_treasure_tier(zone: dict, data: dict) -> str:
    mc_name = (zone.get("mandatoryContent") or [None])[0]
    block = find_mandatory_block(data, mc_name) if mc_name else None
    sids = mandatory_content_sids(block)
    if "random_item_legendary" in sids:
        return "full_treasure"
    if "dragon_utopia" in sids:
        return "lean_treasure"
    if block and len(block.get("content", [])) == 1:
        item = block["content"][0]
        if item.get("isMine") or item.get("sid", "").startswith("mine_"):
            return "spider_minimal"
    pools = " ".join(zone.get("guardedContentPool") or [])
    if "expanse" in pools.lower():
        return "lean_treasure"
    if "spider" in pools.lower() or "antares" in pools.lower():
        return "spider_minimal"
    if "diamond" in pools.lower() or "ikarus" in pools.lower() or "nosta" in pools.lower():
        return "full_treasure"
    return "full_treasure"


def classify_zone(name: str, zone: dict, data: dict) -> tuple[str, str] | None:
    """Return (role, tier_key) or None for spawn zones."""
    if name == "Center":
        return ("center", "center")
    if name.startswith("SuperTreasure-"):
        return ("supertreasure", "supertreasure")
    if name.startswith("Connector-"):
        return ("connector", "connector")
    if name.startswith("Buffer-") or name.startswith("Cross-Buffer-"):
        mc = (zone.get("mandatoryContent") or [None])[0]
        if mc == "mandatory_content_side" or (
            mc and str(mc).startswith("mandatory_content_buffer")
        ):
            return ("buffer", "buffer_side")
        if mc == "mandatory_content_treasure" or (
            mc and str(mc).startswith("mandatory_content_treasure")
        ):
            return ("buffer", "full_treasure")
        return ("buffer", detect_treasure_tier(zone, data))
    if name.startswith("Treasure-"):
        return ("treasure", detect_treasure_tier(zone, data))
    return None


def sorted_neutral_zones(zones: list[dict]) -> list[tuple[str, dict]]:
    """Stable ordering for deterministic pack assignment."""
    neutrals: list[tuple[str, dict, tuple]] = []
    for zone in zones:
        name = zone["name"]
        if name.startswith("Treasure-"):
            try:
                key = (0, int(name.split("-", 1)[1]))
            except ValueError:
                key = (0, 999, name)
        elif name.startswith("SuperTreasure-"):
            try:
                key = (1, int(name.split("-", 1)[1]))
            except ValueError:
                key = (1, 999, name)
        elif name.startswith("Connector-"):
            suffix = name.split("-", 1)[1]
            num = int(suffix) if suffix.isdigit() else 999
            key = (2, num, name)
        elif name.startswith("Buffer-") or name.startswith("Cross-Buffer-"):
            key = (3, name)
        elif name == "Center":
            key = (4, 0)
        else:
            continue
        neutrals.append((name, zone, key))
    neutrals.sort(key=lambda x: x[2])
    return [(n, z) for n, z, _ in neutrals]


def pack_block_name(prefix: str, pack_id: int) -> str:
    if prefix == "mandatory_content_supertreasure":
        return f"mandatory_content_supertreasure_{pack_id}"
    if prefix == "mandatory_content_buffer":
        return f"mandatory_content_buffer_{pack_id}"
    return f"{prefix}_{pack_id}"


def inject_tier_blocks(
    data: dict,
    tier_key: str,
    pack_ids: list[int],
    packs_lib: dict,
) -> dict[int, str]:
    tier = packs_lib["tiers"][tier_key]
    prefix = tier["mandatoryPrefix"]
    id_to_name: dict[int, str] = {}
    blocks = data.setdefault("mandatoryContent", [])
    existing = {b["name"] for b in blocks}

    for pid in sorted(set(pack_ids)):
        pack = next(p for p in tier["packs"] if p["id"] == pid)
        name = pack_block_name(prefix, pid)
        id_to_name[pid] = name
        block = {"name": name, "content": copy.deepcopy(pack["content"])}
        if name in existing:
            for i, b in enumerate(blocks):
                if b["name"] == name:
                    blocks[i] = block
                    break
        else:
            blocks.append(block)
    return id_to_name


def remove_superseded_blocks(data: dict, keep_names: set[str]) -> None:
    variant = data["variants"][0]
    referenced = set()
    for zone in variant["zones"]:
        for mc in zone.get("mandatoryContent") or []:
            referenced.add(mc)

    blocks = data.get("mandatoryContent", [])
    data["mandatoryContent"] = [
        b
        for b in blocks
        if b["name"] not in SUPERSEDED_MANDATORY
        or b["name"] in keep_names
        or b["name"] in referenced
    ]


def apply_center_refresh(data: dict, packs_lib: dict) -> None:
    template_name = data.get("name", "")
    variant_idx = sum(ord(c) for c in template_name) % len(packs_lib["centerRefresh"])
    refresh = packs_lib["centerRefresh"][variant_idx]
    blocks = data.setdefault("mandatoryContent", [])
    center_block = {
        "name": "mandatory_content_center",
        "content": copy.deepcopy(refresh["content"]),
    }
    replaced = False
    for i, block in enumerate(blocks):
        if block.get("name") == "mandatory_content_center":
            blocks[i] = center_block
            replaced = True
            break
    if not replaced:
        blocks.append(center_block)

    for zone in data["variants"][0]["zones"]:
        if zone.get("name") != "Center":
            continue
        mc = (zone.get("mandatoryContent") or [None])[0]
        if mc in SUPERSEDED_MANDATORY or mc is None:
            zone["mandatoryContent"] = ["mandatory_content_center"]
            limits = {b["name"] for b in data.get("contentCountLimits", [])}
            if "content_limits_center" in limits:
                zone["contentCountLimits"] = ["content_limits_center"]


def apply_main_object_flavor(zone: dict, index: int, packs_lib: dict) -> None:
    buildings = packs_lib.get("mainObjectBuildings") or []
    if not buildings:
        return
    for obj in zone.get("mainObjects", []):
        if obj.get("type") in ("City", "AbandonedOutpost") and "buildingsConstructionSid" in obj:
            obj["buildingsConstructionSid"] = buildings[index % len(buildings)]


def compensate_peer_budgets(
    peer_zones: list[dict],
    pack_scores: list[int],
    baseline_score: int,
    px: int,
    zone_count: int,
    *,
    snapshots: list[dict],
) -> None:
    if not peer_zones:
        return
    original_budgets = [
        zone_total_budget(s, px, zone_count) for s in snapshots
    ]
    target_budget = max(original_budgets)

    for zone, pscore in zip(peer_zones, pack_scores):
        delta_mandatory = pscore - baseline_score
        if delta_mandatory:
            guarded = int(zone.get("guardedContentValue") or 0)
            zone["guardedContentValue"] = max(0, guarded - delta_mandatory)

        current = zone_total_budget(zone, px, zone_count)
        adjust = int(round(target_budget - current))
        if adjust:
            guarded = int(zone.get("guardedContentValue") or 0)
            zone["guardedContentValue"] = max(0, guarded + adjust)


def apply_neutral_diversity(data: dict, packs_lib: dict | None = None) -> dict:
    """Apply unique neutral packs to an in-memory template dict. Returns summary."""
    if packs_lib is None:
        packs_lib = load_packs()
    annotate_pack_scores(packs_lib)

    variant = data["variants"][0]
    zones = variant["zones"]
    zone_count = len(zones)
    px = int(data.get("sizeX") or TARGET_PX)

    assignments: list[tuple[str, str, str, int]] = []
    groups: dict[str, list[tuple[str, dict]]] = {}

    for name, zone in sorted_neutral_zones(zones):
        classified = classify_zone(name, zone, data)
        if not classified:
            continue
        role, tier_key = classified
        if tier_key == "center":
            continue
        groups.setdefault(tier_key, []).append((name, zone))

    keep_names: set[str] = {"mandatory_content_center", "mandatory_content_spawn"}
    tier_pack_maps: dict[str, dict[int, str]] = {}

    for tier_key, members in groups.items():
        pack_ids = list(range(1, len(members) + 1))
        # Wrap if more zones than packs in library.
        tier = packs_lib["tiers"][tier_key]
        max_pack = max(p["id"] for p in tier["packs"])
        assigned_ids = [((i % max_pack) + 1) for i in range(len(members))]
        id_to_name = inject_tier_blocks(data, tier_key, assigned_ids, packs_lib)
        tier_pack_maps[tier_key] = id_to_name
        baseline = tier["baselineValueScore"]
        pack_score_list = [
            next(p for p in tier["packs"] if p["id"] == pid)["valueScore"] for pid in assigned_ids
        ]
        snapshots = [copy.deepcopy(z) for _, z in members]

        for idx, (name, zone) in enumerate(members):
            pid = assigned_ids[idx]
            mc_name = id_to_name[pid]
            zone["mandatoryContent"] = [mc_name]
            limits_ref = tier.get("limitsRef")
            if limits_ref:
                zone["contentCountLimits"] = [limits_ref]
            apply_main_object_flavor(zone, idx, packs_lib)
            assignments.append((name, tier_key, mc_name, pid))
            keep_names.add(mc_name)

        compensate_peer_budgets(
            [z for _, z in members],
            pack_score_list,
            baseline,
            px,
            zone_count,
            snapshots=snapshots,
        )

    remove_superseded_blocks(data, keep_names)

    has_center = any(z["name"] == "Center" for z in zones)
    if has_center:
        apply_center_refresh(data, packs_lib)

    return {
        "template": data.get("name"),
        "zones_updated": len(assignments),
        "assignments": assignments,
    }


def diversify_file(path: Path, packs_lib: dict | None = None) -> dict:
    data = load_json(path)
    summary = apply_neutral_diversity(data, packs_lib)
    save_json(path, data)
    return summary


def main() -> None:
    packs_lib = load_packs()
    annotate_pack_scores(packs_lib)
    targets = sorted(MAX8.glob("*.rmg.json"))
    if not targets:
        print("No max8 templates found.")
        return

    for path in targets:
        summary = diversify_file(path, packs_lib)
        print(f"{summary['template']}: {summary['zones_updated']} neutral zones diversified")

    print(f"Done — {len(targets)} templates updated.")


if __name__ == "__main__":
    main()
