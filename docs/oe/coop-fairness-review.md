# Fair-play review — `templates/max8` for 2 co-op humans + 6 FFA AI

**Intended mode:** 2 **human** players in **co-op** (allied), placed **as far apart as possible** so
simultaneous/parallel turns persist (in HoMM, simultaneous turns end when players make contact) — plus
**6 AI** in a free-for-all that fight each other and the humans.

**What makes a map fair for this mode:**

1. **Buffered human starts** — no direct spawn↔spawn link between the two human slots. Neutral buffers
   between every hop on the human→center paths delay contact.
2. **Large human separation** — long graph distance between Player1 and Player2 (seat humans on
   `Spawn-A` / `Spawn-B` on the co-op corridor maps).
3. **AI flanks** — three AI per human side, with cross-lanes so the six AI can fight each other
   (`E1—E4`, `E2—E5`, `E3—E6` on corridor maps).
4. **Symmetric balance** — both human arms mirror through the central hub.

## Co-op corridor maps (purpose-built)

```
P1 — buf — E1 — buf — E2 — buf — E3 — buf — H — buf — E4 — buf — E5 — buf — E6 — buf — P2
         \________________ cross AI lanes ________________/
```

| Template | Human seats | P1↔P2 hops | Cross AI | Win |
|---|---|---|---|---|
| **Hard Place Hoard Corridors** | Player1 / Player2 | **9** | Direct (`E1—E4`, …) | Classic · hoard ×1.5 |
| **Ikarus Ladder Dominion** | Player1 / Player2 | **10** | Buffered rungs (`Cross-Buffer-1…3`) | Hold city 6 days |

Regenerate: `python tools/build_coop_corridor.py`

## Other Tier-A / B maps (general FFA seating)

| Template | buffered humans | notes |
|---|---|---|
| Diamond Ring | ✅ (if humans opposite on ring) | diameter 8 |
| Ikarus Showdown | ✅ | hub arms · seat humans antipodally |
| Spider Titan / Antares Maelstrom | ✅ | spider legs |
| Diamond Colossus / Boundless Expanse | ✅ | |
| Boomerang Crown | ✅ | all via arm treasure → hold |
| Ikarus Ascendant | ✅ | min spawn sep 3 |
| Octo Anarchy | ✅ | Tier B — equidistant hub |
| Grand Nostalgia | ❌ | Tier C — direct spawn shortcuts |

## Lobby setup (corridor maps)

1. Pick **Hard Place Hoard Corridors** or **Ikarus Ladder Dominion**.
2. Seat **Player1** and **Player2** as the two humans; **Players 3–8** as AI (no shared teams).
3. Ally the two humans.
4. Optional: simultaneous turns — humans stay apart ~9–10 neutral hops until mid-map contact.

> Previews in `templates/max8/*.png` — green discs = starts (1 = `Spawn-A`, 2 = `Spawn-B` on corridor
> maps), neutrals = bronze/silver buffers, blue `H` = hub / hold city.
