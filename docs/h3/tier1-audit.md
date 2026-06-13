# Tier 1 Audit: H3 HotA ↔ Olden Era Direct Name Matches

Detailed gap analysis for templates that exist in both ecosystems by name.

## Jebus Cross

| Aspect | H3 HotA (official `.h3t`) | OE `Jebus Cross.rmg.json` | Verdict |
|--------|---------------------------|---------------------------|---------|
| Map size | XL-U (min size 9) | 160×160 | Match |
| Zone count | **5** (center + 4 player) | **5** (Center + Spawn-A/B + Side-C/D) | Partial — OE adds side zone names |
| Connections | **4** (hub 1 → 2,3,4,5) | **20** Direct (multi-guard lanes + side routes) | OE richer connection mesh |
| PG guard | **45000** (all 4 arms) | **55555–66666** | OE harder |
| Richness | 103 player / 610 center | `template_pool_jebus_cross_*` | Equivalent tier |
| Win condition | Classic + optional tournament city hold (lobby) | `cityHold` 6 days on center city | OE encodes tournament hold |
| Extra | — | Side zones Side-C/D, remote footholds, movement bonus | OE enrichment |

**Recommendation:** Keep OE design; document PG delta for competitive parity tuning if desired.

## Jebus Cross Classic

Same topology family as Jebus Cross with classic object set. OE ships both; Classic omits some modern OE-specific mandatory content. Audit same as Jebus Cross.

## Diamond

| Aspect | H3 (official) | OE | Verdict |
|--------|---------------|-----|---------|
| Size | L+U (18×18 min/max) | 144×144 | Match |
| Zones | **16** | **16+** (8 spawns + treasures) | Similar scale |
| Connections | **32** | many Default/road | Match complexity |
| Roads per spawn | 4 obligatory (H3 docs) | 4 stone roads per Spawn-A/B | Match |

**Recommendation:** Verified port; value overrides on standard POIs present in OE.

## Mini-Nostalgia

| Aspect | H3 (official) | OE | Verdict |
|--------|---------------|-----|---------|
| Size | L+U | 144×144 | Match |
| Zones | **15** | **15** (8 spawns + 6 treasures + Center) | Match |
| Connections | **14** | 14+ player/AI/treasure links | Match |
| Central PG | **45000** | heavy guards on Spawn→Center | Match intent |

**Recommendation:** Verified port.

## Spider

| Aspect | H3 (official) | OE | Verdict |
|--------|---------------|-----|---------|
| Size | XL+U | 208×208 | Match |
| Zones | **24** | check OE summary | Compare in `layouts/official/` |
| Connections | **32** | 3 roads/spawn pattern | Partial — guard values differ |

**Recommendation:** Topology match; tune connection guards if H3-feel desired.

## Kerberos

| Aspect | H3 (official) | OE | Verdict |
|--------|---------------|-----|---------|
| Size | XL+U | 128×128 | **Gap** — OE smaller |
| Zones | **33** | **13** | **Gap** — OE simplified |
| Connections | **39** | fewer | Partial |

**Recommendation:** OE Kerberos is inspired by H3 but not a faithful XL+U 2–3 player port; use h3-port scaffold or resize to 208 for tournament use.

## Anarchy

| Aspect | H3 | OE | Verdict |
|--------|----|----|---------|
| Variants | 12 random layouts per pack | 5 variants | **Gap** |
| encounterHoles / anarchy mode | Yes | `encounterHoles: true` | Match |
| Object rules | Legacy SoD bans lifted | `valueOverrides` on 7 POIs | Partial |

**Recommendation:** Add 7 more OE variants to reach H3's 12-layout variety, or accept 5-layout subset.

## Jebus Outcast

Community template (MKC / h3res). OE ships `Jebus Outcast.rmg.json` with dedicated pools (`template_jebus_outcast_pools.json`). Not in official h3hota rules list; OE-native competitive variant. No official `.h3t` downloaded; compare via h3res when available.

## OctoJebus

OE-original 8-player Jebus hub. No H3 namesake. Useful as base for `mt_TeamJebus` scaffold only.

---

Official topology data: [`h3/layouts/official/`](h3/layouts/official/) (parsed from GOG HotA install).
