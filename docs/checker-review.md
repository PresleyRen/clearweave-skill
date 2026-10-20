# Local checker and installer review

## Scope and result

Reviewed `skills/clearweave/scripts/clearweave_check.py`, `tests/test_checker.py`, `tools/install_skill.py`, `tests/test_install.py`, and `skills/clearweave/references/tooling.md`, with the relevant installation and checker claims in `README.md` and `SKILL.md` as context. No writing evaluation candidates or outputs were read, and no implementation files were changed.

**All 37 existing unittests passed.** Focused independent probes found one moderate protection-boundary defect and one low-severity documentation mismatch. No material installer overwrite defect, false semantic-verification claim, input rewrite, or network behavior was found in the reviewed code and tested cases.

## Actionable findings

### P2 — Delimiters inside an outer protected block can hide subsequent prose

**Location:** `_structural_spans()`, `clearweave_check.py`, lines 147–179.

The fence scan runs through already recognized frontmatter, and the keep-tag scan runs through fenced code. A delimiter that is literal content of an outer block can therefore start a second protection region that extends beyond that block. Merging the partial overlap then protects ordinary body text through end of file.

Reproduction:

````text
---
example: |
  ```
---
It is worth noting that the cap remains.
````

Actual result: a single `overlapping_protection` span covers the entire input, and `lint_text()` returns `candidate_count: 0`. The final sentence is ordinary text outside the closed frontmatter and should produce `EN002`.

The same result occurs with this closed code example:

````text
```html
<!-- clearweave:keep -->
```
It is worth noting that the cap remains.
````

This can silently suppress the remaining lint report for a document containing delimiter examples. It can also cause unrelated body edits to be reported as changes to one oversized protected literal. It does not produce a semantic-pass claim.

**Recommended action:** establish containment-aware delimiter handling so literal fence markers inside frontmatter and keep markers inside code do not open regions outside their enclosing block. Add these two focused regressions. If literal markers are intentionally active in code, state that behavior explicitly; the current generic overlap explanation does not make this consequence clear.

### P3 — The advertised Pandoc marker syntax is broader than recognition

**Location:** `_CITATION_PATTERNS`, `clearweave_check.py`, line 120; citation row in `references/tooling.md`.

The documentation says simple Pandoc `@key` markers are supported, but the regular expression requires surrounding square brackets.

| Original | Revision | Actual result |
| --- | --- | --- |
| `See @alpha for details.` | `See @beta for details.` | No protected spans; `change_count: 0` |
| `See [@alpha] for details.` | `See [@beta] for details.` | One lost and one added citation; `change_count: 2` |

**Recommended action:** either document support precisely as bracketed `[@key]` citations, including the supported multi-key form, or add bare marker recognition with appropriate boundaries. Keep the semantic-review caveat in either case.

## What passed

- **Semantic honesty:** JSON reports always retain `semantic_review_required: true`; text reports say semantic review is required. Unchanged numeric counts, exchanged value roles, negation changes, and written-out number changes are explicitly treated as known limits rather than semantic approval. There is no authorship probability or automatic rewrite path.
- **Documented protection controls:** existing tests cover bilingual candidate coordinates, language selection, quote forms, fenced and inline code, frontmatter, keep blocks, mathematics, URLs with parentheses, Markdown targets, citations, custom literals, and outer-region counting. Listed numeric forms and unit changes were independently checked with `-5°C`, `1,024MiB`, `2e+3ms`, and `3 m/s²`; changing each unit produced the expected four lost and four added literals.
- **Explicit limitations remained explicit:** `3 weeks` → `3 months` is invisible to the numeric comparison because those unit words are not in the finite unit list. This agrees with the documented limitation and is not a new defect. An escaped opening quote can also overprotect text; escape-related heuristic limitations are already disclosed.
- **Input and error handling:** invalid UTF-8 in stdin and the protection file, directory input, missing files, invalid language, and two stdin comparison inputs return status `2`. Help returns `0` without reading the supplied missing input path. Normal lint returns `0`, and detected literal changes return `1`. Existing byte-preservation checks passed.
- **Installer boundaries:** independent probes confirmed refusal to replace existing regular files, directories, or dangling symlinks at the destination, with their contents or link targets unchanged. Symlinks at either `.agents` or `.agents/skills` pointing outside the chosen project were rejected without populating the outside directory. Missing and non-directory project arguments returned status `2` without tracebacks.
- **Copy integrity and side effects:** an installation into a temporary project contained all 10 packaged files byte-for-byte, excluding Python cache files as intended. The checker contains only reads and report output; the installer performs the explicitly requested project copy and has no network, dependency-install, or global-settings code path. No changes under `/root/.codex` were made.

## Validation command

```bash
python -m unittest discover -s tests -p 'test_*.py' -v
```

The independent probes were small temporary-file and in-memory cases aimed at the risks above. No writing-quality benchmarks were run.
