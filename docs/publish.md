# Publishing templates to GitHub

This repo uses two branches:

| Branch | Audience | Contents |
|--------|----------|----------|
| `dev` | Authors / maintainers | Full workspace (`tools/`, `lib/`, `data/`, `h3/`, docs, agent config) |
| `main` | Players / downloaders | Template distro only (`templates/`, consumer `README.md`, `LICENSE`, `docs/install.md`) |

GitHub remote: [synthet/heroes-olden-era-templates](https://github.com/synthet/heroes-olden-era-templates)

## Daily workflow

Work on **`dev`** (default for local development):

```bash
git checkout dev
python tools/validate_rmg.py templates/
python tools/publish.py -m "Update max8 templates."
python tools/publish.py --push -m "Update max8 templates."
```

`tools/publish.py` copies the manifest into a linked worktree at [`.git-publish-worktree/`](../.git-publish-worktree/) on `main`, commits if needed, and optionally pushes.

## What gets published

Configured in [`publish.manifest.json`](../publish.manifest.json):

- **Directory:** `templates/` (all subfolders and previews)
- **Mapped files:**
  - `LICENSE` → `LICENSE`
  - `README.publish.md` → `README.md` (consumer landing page)
  - `docs/install.publish.md` → `docs/install.md` (player install guide)

Edit the `.publish.md` sources when changing public-facing docs. Keep full authoring docs in `README.md` and `docs/install.md` on `dev` only.

## First-time setup (already done in this repo)

```bash
git checkout -b dev
git add -A
git commit -m "Add dev workspace with publish workflow."
python tools/publish.py --push
git push -u origin dev
```

## Notes

- `.git-publish-worktree/` is gitignored; it is a `git worktree` checkout of `main`.
- Do not hand-edit files inside `.git-publish-worktree/` — changes will be overwritten on the next publish.
- `main` at the repo root tracks the last published commit after `git merge` or when checking out `main`; the worktree is the supported publish target.
