"""Single source of truth for repo-relative paths."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

TEMPLATES = ROOT / "templates"
TEMPLATES_OFFICIAL = TEMPLATES / "official"
TEMPLATES_MAX8 = TEMPLATES / "max8"
TEMPLATES_H3_PORT = TEMPLATES / "h3-port"

DATA = ROOT / "data"
LIB = ROOT / "lib"

H3 = ROOT / "h3"
H3_SOURCES_OFFICIAL = H3 / "sources" / "official"
H3_SOURCES_COMMUNITY = H3 / "sources" / "community"
H3_LAYOUTS = H3 / "layouts"
H3_LAYOUTS_OFFICIAL = H3_LAYOUTS / "official"
H3_LAYOUTS_OE = H3_LAYOUTS / "oe"

DOCS = ROOT / "docs"
DOCS_H3_MATRIX = DOCS / "h3" / "matrix.md"
DOCS_H3_CATALOG = DOCS / "h3" / "catalog.md"
DOCS_H3_TIER1 = DOCS / "h3" / "tier1-audit.md"
DOCS_PUBLISH = DOCS / "publish.md"
DOCS_INSTALL_PUBLISH = DOCS / "install.publish.md"

PUBLISH_MANIFEST = ROOT / "publish.manifest.json"
PUBLISH_WORKTREE = ROOT.parent / ".heroes-templates-main-worktree"
README_PUBLISH = ROOT / "README.publish.md"

TOOLS = ROOT / "tools"
PUBLISH = TOOLS / "publish.py"
H3T_PARSER = TOOLS / "h3t_parser.py"

HOTA_INSTALL = Path(
    r"C:\Program Files (x86)\GOG Galaxy\Games"
    r"\Heroes of Might and Magic III - Horn of the Abyss"
)
