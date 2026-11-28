# ClearWeave maintenance

Before completing a change, review the final diff and apply the matching items below. Keep related code, tests and documentation in the same change.

| When the change affects | Update together |
| --- | --- |
| A tool or writing behavior | Update the implementation and its usage reference. Exercise the actual entry point and cover the changed behavior in the relevant regression tests. Update `skills/clearweave/SKILL.md` if routing changes, and `skills/clearweave/agents/openai.yaml` if its advertised description or suggested prompt changes. |
| A public capability or conflict | In `skills/clearweave/assets/capabilities.json`, keep each capability's module, stable anchor, implementation boundary, source IDs and scenario IDs accurate. Reuse the existing capability ID for an extension. For a new conflict, link the affected capabilities to one English and one Chinese case in `evals/conflict-cases.json`. |
| An upstream source or audit decision | Update `docs/source-audit.json` and its matching entries in `docs/feature-map.json`, including decision hashes. Keep the declared source count and capability links in sync. |
| The catalog, source map or renderer | Run `python3 tools/render_catalog.py --write` and review the generated changes. Update any affected hand-written counts and summaries in both READMEs and the Chinese capability atlas. |
| Navigation, examples or explanatory prose | Edit outside the capability markers. Keep the matching English and Chinese user-facing guidance aligned. Regenerate when a generated block or its inputs change. |
| An intended version bump | Update `VERSION`, the catalog's `version`, `CHANGELOG.md`, `docs/releases/v<VERSION>.md` and its `.zh-CN.md` mirror together. Publish the GitHub Release only when authorized. |

## Before handing off

From the repository root, run the same offline checks as regular GitHub CI:

```bash
python3 tools/validate_repo.py --release
python3 -m unittest discover -s tests -v
```

Review the diff for unrelated edits and whitespace errors. Keep archived evaluation snapshots as historical evidence. Report the checks that actually ran and any remaining gap. For an authorized push, use the configured Git SSH remote and verify the GitHub Actions result for the pushed or merged commit.
