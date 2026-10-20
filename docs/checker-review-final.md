# Final targeted checker review

## Decision

**The two findings from `docs/checker-review.md` are resolved. No remaining material defect or boundary regression was found in this targeted review.** The original review is retained unchanged as the record of the earlier implementation.

This review examined the revised checker, its tests, and the updated protection documentation. It did not modify implementation or tests, inspect writing evaluation candidates or outputs, or expand into writing-quality benchmarks.

## Verification results

| Check | Result |
| --- | --- |
| `python -m unittest discover -s tests -p 'test_*.py' -v` | All 46 tests passed, including installer tests |
| `python3 tools/validate_repo.py` | Passed; the tool correctly identifies its result as a structure and coverage check |
| Original YAML fence reproduction | Only `frontmatter` is protected; the following ordinary sentence produces `EN002` at the correct source position |
| Original opening keep marker inside closed fenced code | Only `fenced_code` is protected; the following ordinary sentence produces `EN002` |
| Bare `@alpha` → `@beta` | Exactly one lost and one added `at_key` literal, with semantic review still required |
| Common email addresses and escaped `\@` | Six independently exercised cases produced no `at_key` or `citation` spans |
| Direct quotations containing inline code | All 12 independently exercised combinations preserved the complete outer quotation and detected its prose change |

## Resolution of the reported issues

### Former P2: delimiters inside an outer block

The revised structural scan advances in source order and skips the contents of a recognized region. A fence example inside frontmatter or a keep example inside fenced code therefore cannot start a region extending into later prose. I reran both exact reproductions from the original review, then checked a BOM/CRLF YAML block containing a tilde fence and a CRLF example with different opening and closing fence lengths. All cases retained the correct outer span and left the following sentence visible to lint.

Secondary quote and math delimiters printed inside inline code also remained confined to that code. Existing tests additionally cover nested keep behavior and unmatched inline-code delimiters near block boundaries.

### Former P3: bare citation-key wording and behavior

The implementation now reports supported bare keys separately as `at_key`. The documentation distinguishes these from bracketed Pandoc citations and states that an `@mention` cannot be identified as a bibliographic citation without additional context.

For `See @alpha for details.` → `See @beta for details.`, both the direct comparison API and the CLI returned the expected two literal changes. The CLI returned status `1` and left its input file unchanged. Independently checked exclusions included an ordinary email, a dotted local part with a plus tag and subdomain, a local part ending in a hyphen, a quoted local part, a Chinese local part, and a backslash-escaped `@`.

## Regression check: quotation containing inline code

The quote scan uses masked structural contents while retaining original offsets and original text in the resulting literal. I checked all four documented delimiter forms (`"…"`, `“…”`, `「…」`, and `『…』`) with three inline-code contents: `retry`, a literal double quote, and an opening keep marker.

In all 12 combinations, changing prose outside the inline code but inside the quotation produced exactly two `quotation` changes. The quotation counted once, its internal candidate was skipped, and a following unquoted sentence still produced its expected lint candidate. This resolves the specific outer-quotation regression risk raised during implementation.

## Remaining scope limits

The checker remains a documented heuristic literal checker. Unordered counts cannot verify roles, negation, attribution, or meaning; `semantic_review_required` remains true. Bare `at_key` tokens remain ambiguous, and complex email or citation syntax is outside the promised coverage. These are explicit limits rather than unresolved defects from this review.

No new network, input-write, dependency-install, or global-settings code path was introduced in the reviewed changes. Installer implementation was unchanged and its full test set passed again. No changes under `/root/.codex` were made.
