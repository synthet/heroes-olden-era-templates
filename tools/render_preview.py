#!/usr/bin/env python3
"""Render Olden Era `.rmg.json` templates to PNG previews.

Reproduces the game's preview legend (parchment node-graph) extracted from the Template Generator's
`TemplatePreviewPngWriter.cs`: numbered green player discs, bronze/silver/gold neutral tiers by zone
layout, a blue-grey hub, gold lines for Direct/Default connections and blue for Portals (Proximity
links are spacing-only and not drawn).

Usage:
    python tools/render_preview.py                       # render every template under templates/
    python tools/render_preview.py <file|dir> [more...]  # render specific files/folders
    [--size 700] [--out DIR] [--title]

- A `.rmg.json` path renders a sidecar `<name>.png` (next to it, or into --out).
- A directory renders every `*.rmg.json` inside it (non-recursive).
- With no path args, renders templates/{official,max8,h3-port} from tools/paths.py.

Layout is a schematic approximation (centers in the middle, spawns on the outer ring, other neutrals
on an inner ring); it conveys topology and roles, not exact in-game geometry.
"""
import json, math, os, re, sys, glob
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]

# ── Palette (from TemplatePreviewPngWriter.cs) ────────────────────────────────
BG          = (28, 22, 16)
BORDER_PEN  = (143, 115, 63)
BRONZE      = ((101, 67, 33),  (205, 127, 50))    # zone_layout_sides           (Low)
SILVER      = ((72, 76, 80),   (192, 192, 192))   # zone_layout_treasure_zone   (Med/High) + default neutral
GOLD        = ((120, 90, 20),  (255, 210, 50))    # zone_layout_center
SPAWN       = ((42, 90, 50),   (100, 200, 120))   # player spawn
HUB         = ((55, 80, 95),   (130, 180, 200))   # hub
DIRECT_LINE = (180, 145, 60)
PORTAL_LINE = (90, 170, 210)
TEXT        = (235, 225, 200)
ZONE_R_MAX  = 38

def _font(size, bold=True):
    cands = ("arialbd.ttf", "arial.ttf") if bold else ("arial.ttf",)
    for name in cands:
        for p in (name, f"C:/Windows/Fonts/{name}",
                  f"/usr/share/fonts/truetype/dejavu/DejaVuSans{'-Bold' if bold else ''}.ttf"):
            try: return ImageFont.truetype(p, size)
            except Exception: pass
    return ImageFont.load_default()

def load(p):
    t = open(p, encoding="utf-8-sig").read()
    try: return json.loads(t)
    except json.JSONDecodeError: return json.loads(re.sub(r",(\s*[}\]])", r"\1", t))

def classify(zone):
    name = zone.get("name") or ""
    layout = zone.get("layout") or ""
    players = [o["spawn"] for o in zone.get("mainObjects", []) if o.get("type") == "Spawn" and o.get("spawn")]
    # Only a genuinely-named hub is the central node; zone_layout_center is also used by treasure
    # zones, so colour tier comes from the layout but position role does not.
    is_hub = bool(re.search(r"\bhub\b|\bcore\b", name, re.I)) or name.strip().lower() in ("center", "centre")
    if players:
        role, colors = "spawn", SPAWN
    elif is_hub:
        role, colors = "center", HUB
    else:
        role = "neutral"
        colors = GOLD if "center" in layout else BRONZE if "sides" in layout else SILVER
    label = str(int(players[0].replace("Player", ""))) if players else ("H" if is_hub else "")
    return role, colors, label

def ring_positions(cx, cy, radius, items, start_zero=None):
    n = len(items)
    if n == 0: return {}
    if start_zero in items:
        i = items.index(start_zero); items = items[i:] + items[:i]
    return {nm: (cx + math.cos(-math.pi/2 + 2*math.pi*k/n) * radius,
                 cy + math.sin(-math.pi/2 + 2*math.pi*k/n) * radius)
            for k, nm in enumerate(items)}

def build_adj(zones, conns):
    """Adjacency from real connections only (Proximity is spacing-only, not a path)."""
    adj = {z["name"]: set() for z in zones if z.get("name")}
    for c in conns:
        if c.get("connectionType") == "Proximity":
            continue
        a, b = c.get("from"), c.get("to")
        if a in adj and b in adj and a != b:
            adj[a].add(b); adj[b].add(a)
    return adj

def layout_zones(zones, conns, zero_zone, W, H):
    """Deterministic force-directed (Fruchterman-Reingold) layout — the method the generator's own
    preview writer uses. Nodes are seeded symmetrically (spawns on an outer circle, others on an
    inner circle, in file order), then relaxed by edge attraction + all-pairs repulsion + mild
    gravity. Positions derive from the real connection graph, so the drawing matches the topology;
    a true hub (e.g. OctoJebus Center) is pulled to the middle for a clean star, and symmetric
    templates settle symmetrically. A final min-distance pass prevents disc overlap."""
    cx, cy = W / 2, H / 2
    meta, names, spawns = {}, [], set()
    for z in zones:
        nm = z.get("name")
        if not nm: continue
        role, colors, label = classify(z)
        meta[nm] = (role, colors, label)
        names.append(nm)
        if role == "spawn": spawns.add(nm)
    if not names: return {}, meta
    adj = build_adj(zones, conns)
    if len(names) == 1: return {names[0]: (cx, cy)}, meta
    # connected components (real edges); FR runs on the main graph, strays get ringed
    from collections import deque
    seen, comps = set(), []
    for z in names:
        if z in seen: continue
        c, q = [], deque([z]); seen.add(z)
        while q:
            u = q.popleft(); c.append(u)
            for w in adj[u]:
                if w not in seen: seen.add(w); q.append(w)
        comps.append(c)
    core = set(max(comps, key=len))
    floats = [nm for nm in names if nm not in core]
    core_names = [nm for nm in names if nm in core]
    n = len(core_names)
    sp = [nm for nm in core_names if nm in spawns]
    ot = [nm for nm in core_names if nm not in spawns]
    if zero_zone in sp:
        i = sp.index(zero_zone); sp = sp[i:] + sp[:i]
    pos = {}
    for k, nm in enumerate(sp):
        a = -math.pi/2 + 2*math.pi*k/max(len(sp), 1); pos[nm] = [cx+math.cos(a)*230, cy+math.sin(a)*230]
    for k, nm in enumerate(ot):
        a = -math.pi/2 + 2*math.pi*k/max(len(ot), 1); pos[nm] = [cx+math.cos(a)*85, cy+math.sin(a)*85]
    k = 0.85 * math.sqrt(((min(W, H) - 160) ** 2) / max(n, 2))   # ideal edge length
    t = k; cool = 0.95
    for _ in range(450):
        disp = {nm: [0.0, 0.0] for nm in core_names}
        for i in range(n):
            for j in range(i+1, n):
                a, b = core_names[i], core_names[j]
                dx, dy = pos[a][0]-pos[b][0], pos[a][1]-pos[b][1]
                d = math.hypot(dx, dy) or 0.01
                f = k*k/d; ux, uy = dx/d, dy/d
                disp[a][0] += ux*f; disp[a][1] += uy*f
                disp[b][0] -= ux*f; disp[b][1] -= uy*f
        for a in core_names:
            for b in adj[a]:
                if a < b and b in core:
                    dx, dy = pos[a][0]-pos[b][0], pos[a][1]-pos[b][1]
                    d = math.hypot(dx, dy) or 0.01
                    f = d*d/k; ux, uy = dx/d, dy/d
                    disp[a][0] -= ux*f; disp[a][1] -= uy*f
                    disp[b][0] += ux*f; disp[b][1] += uy*f
        for nm in core_names:  # gravity keeps the graph centered
            disp[nm][0] += (cx-pos[nm][0])*0.012; disp[nm][1] += (cy-pos[nm][1])*0.012
        for nm in core_names:
            dl = math.hypot(*disp[nm]) or 0.01; s = min(dl, t)
            pos[nm][0] += disp[nm][0]/dl*s; pos[nm][1] += disp[nm][1]/dl*s
        t = max(t*cool, k*0.01)
    xs = [pos[nm][0] for nm in core_names]; ys = [pos[nm][1] for nm in core_names]
    sx, sy = (max(xs)-min(xs)) or 1, (max(ys)-min(ys)) or 1
    m = 90 if floats else 80
    scale = min((W-2*m)/sx, (H-2*m)/sy)
    mx, my = (min(xs)+max(xs))/2, (min(ys)+max(ys))/2
    P = {nm: [cx+(pos[nm][0]-mx)*scale, cy+(pos[nm][1]-my)*scale] for nm in core_names}
    for idx, nm in enumerate(floats):  # isolated zones on the outer rim
        a = -math.pi/2 + 2*math.pi*idx/max(len(floats), 1)
        P[nm] = [cx+math.cos(a)*(min(W, H)/2 - 40), cy+math.sin(a)*(min(W, H)/2 - 40)]
    ks = list(P)  # min-distance spread
    for _ in range(140):
        moved = False
        for i in range(len(ks)):
            for j in range(i+1, len(ks)):
                a, b = ks[i], ks[j]
                dx, dy = P[a][0]-P[b][0], P[a][1]-P[b][1]
                d = math.hypot(dx, dy) or 0.001
                if d < 42:
                    push, ux, uy = (42-d)/2, dx/d, dy/d
                    P[a][0] += ux*push; P[a][1] += uy*push
                    P[b][0] -= ux*push; P[b][1] -= uy*push
                    moved = True
        if not moved: break
    return {nm: tuple(p) for nm, p in P.items()}, meta

def disc_radius(pos):
    pts = list(pos.values())
    md = min((math.hypot(pts[i][0]-pts[j][0], pts[i][1]-pts[j][1])
              for i in range(len(pts)) for j in range(i+1, len(pts))), default=2*ZONE_R_MAX)
    return max(9, min(ZONE_R_MAX, int(md/2 - 3)))

def render(template, W=700, H=700, title=False):
    img = Image.new("RGB", (W, H), BG)
    dc = ImageDraw.Draw(img, "RGBA")
    dc.rounded_rectangle([8, 8, W - 8, H - 8], radius=10, outline=BORDER_PEN, width=3)
    variant = (template.get("variants") or [{}])[0]
    zones = variant.get("zones", [])
    if not zones:
        dc.text((W/2, H/2), template.get("name", "?"), fill=TEXT, anchor="mm", font=_font(28)); return img
    zero = (variant.get("orientation") or {}).get("zeroAngleZone")
    pos, meta = layout_zones(zones, variant.get("connections", []), zero, W, H)
    r = disc_radius(pos)
    for c in variant.get("connections", []):
        ct = c.get("connectionType")
        if ct == "Proximity": continue
        a, b = pos.get(c.get("from")), pos.get(c.get("to"))
        if not a or not b: continue
        if ct == "Portal": dc.line([a, b], fill=PORTAL_LINE + (165,), width=2)
        else: dc.line([a, b], fill=DIRECT_LINE + (140,), width=max(2, r // 12))
    nf = _font(max(int(r * 1.1), 12))
    for nm in sorted(pos, key=lambda n: 0 if meta[n][0] != "spawn" else 1):
        x, y = pos[nm]; role, (fill, outline), label = meta[nm]
        rr = max(int(r * (0.7 if role == "center" and not label else 1.0)), 8)
        dc.ellipse([x-rr, y-rr, x+rr, y+rr], fill=fill, outline=outline, width=3)
        if label: dc.text((x, y), label, fill=TEXT, anchor="mm", font=nf)
    if title: dc.text((W/2, H-16), template.get("name", ""), fill=TEXT, anchor="mm", font=_font(18))
    return img

def collect(args):
    if not args:
        return [str(p) for d in ("official", "max8", "h3-port")
                for p in sorted((ROOT / "templates" / d).glob("*.rmg.json"))]
    files = []
    for a in args:
        if os.path.isdir(a): files += sorted(glob.glob(os.path.join(a, "*.rmg.json")))
        elif a.endswith(".rmg.json"): files.append(a)
    return files

def main(argv):
    paths, size, outdir, title = [], 700, None, False
    i = 1
    while i < len(argv):
        a = argv[i]
        if a == "--size": size = int(argv[i+1]); i += 2
        elif a == "--out": outdir = argv[i+1]; i += 2
        elif a == "--title": title = True; i += 1
        else: paths.append(a); i += 1
    files = collect(paths)
    if not files:
        print(__doc__); return 2
    ok = 0
    for f in files:
        try:
            img = render(load(f), W=size, H=size, title=title)
            base = os.path.basename(f)[:-len(".rmg.json")] + ".png"
            out = os.path.join(outdir, base) if outdir else f[:-len(".rmg.json")] + ".png"
            os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
            img.save(out); ok += 1
            print(f"  {out}")
        except Exception as e:
            print(f"  FAILED {f}: {e}")
    print(f"Done: {ok}/{len(files)} previews.")
    return 0 if ok == len(files) else 1

if __name__ == "__main__":
    sys.exit(main(sys.argv))
