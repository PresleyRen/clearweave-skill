# Evaluation report / 实测报告

**Date: 2026-10-20.** This report distinguishes observed writing behaviour, subjective editorial judgements, literal checks, and packaging tests.

## Findings that matter

The initial 18-request comparison did **not** establish broad superiority over a capable model's ordinary writing. The anonymous editor preferred ClearWeave once, the ordinary flow once, and judged 16 cases tied. It found one instance of causal strengthening in the ordinary translation and none in the ClearWeave responses under the stated rubric.

ClearWeave's less-preferred product explanation retained a generic aspiration that could be removed. We clarified that rule and tested four new requests in a fresh context. Those four responses retained specific plans and an author's preference while removing generic product introductions. The original 18-case outputs remain unchanged and are not re-scored as if they came from the refined instructions.

This is evidence of behaviour on short synthetic cases. It is not a universal quality ranking, an authorship test, or a measurement of commercial detectors.

## 1. Setup and evidence trail

| Item | Actual setup |
| --- | --- |
| Writing input | 18 original synthetic requests, each with an explicit request and source |
| Conditions | Ordinary host-model writing; same task with ClearWeave instructions and relevant references |
| Context isolation | Two fresh batches per condition: CW01–CW09 and CW10–CW18; no inherited conversation history |
| Repetitions | One response per case per condition; no selected rerolls |
| Evaluation | Separate fresh-context A/B editor, unaware of the condition mapping; the editor also delegated a translation cross-check |
| Criteria | Meaning fidelity, task compliance, restraint, subjective readability, and A/B/tie preference |
| Model scope | A ChatGPT agent environment identified as GPT-6 Astra Pro; child snapshot and sampling parameters were not exposed or pinned |
| Additional check | Four new requests after the generic-aspiration clarification, with another fresh-context editor |

Generation agents received the writing requests and source text, without the expected answers, review rubric, source audit, or comparison outputs. Cases within a nine-request batch shared a context. This is not 18 fully isolated per-condition model calls and not a study involving independent human editors.

Evidence:

- [Requests](../evals/cases.json), [protocol](../evals/PROTOCOL.md), and [rubric](../evals/rubric.json).
- Ordinary outputs: [CW01–CW09](../evals/runs/plain-a.json), [CW10–CW18](../evals/runs/plain-b.json).
- Initial ClearWeave outputs: [CW01–CW09](../evals/runs/clearweave-a.json), [CW10–CW18](../evals/runs/clearweave-b.json).
- [Anonymous candidates](../evals/blind-review.json), [raw editor judgements](../evals/blind-review-results.json), and [revealed condition mapping](../evals/condition-map.json).
- [Initial instruction snapshot](../evals/snapshots/README.md) verified against the [recorded SHA-256 manifest](../evals/generation-manifest.json).
- [Machine-readable summary](../evals/summary.json). Run `python3 tools/summarize_evals.py` to recompute its counts from the retained judgements; it does not call a model or generate new reviews.

## 2. Initial writing results

“Pass” below means the model editor found no material violation of the published rubric. It is not an objective guarantee.

| Criterion | Ordinary flow | ClearWeave |
| --- | ---: | ---: |
| Meaning fidelity | 17 / 18 | 18 / 18 |
| Requested task / language / format | 18 / 18 | 18 / 18 |
| Appropriate restraint | 18 / 18 | 18 / 18 |
| Preferred by the anonymous editor | 1 | 1 |
| Ties | 16 | 16 |
| Good-text controls retained exactly | 2 / 2 | 2 / 2 |

The two preference findings need context:

**CW10 — translation and causal strength.** The Chinese source says mean recovery time decreased *after* a strategy was enabled. The ordinary response says “enabling the new strategy reduced the mean recovery time,” assigning the reduction to that strategy. The ClearWeave response keeps the temporal relationship: “mean recovery time fell … after the new policy was enabled.” Under the rubric's strict preservation standard, the editor counted the causal strengthening as a fidelity failure. The source describes a simulation, so a reader might infer an intervention effect; the reported distinction is the editor's conservative judgement about what the wording explicitly asserts. It does not prove that the ordinary model habitually makes causal errors.

**CW06 — a product notice that could be more direct.** ClearWeave retained a general wish to improve the user experience. The ordinary response opened with the available export function and addressed the reader politely. Both preserved the functional limits, administrator approval, Traditional Chinese, UI name, and API field. The ordinary response was preferred for directness; the ClearWeave response did not fail fidelity.

CW09's “warm cache” translation received an optional terminology suggestion in the ordinary response; it was not counted as a material error. The other cases were ties, including the academic limitation examples, mixed code-and-quotation text, sample-based voice tasks, note drafting, critique, and shortening.

## 3. Refinement and four new requests

We added a narrow distinction to the main workflow and preservation reference:

- Generic product aspirations can be removed when the actual feature description already communicates the purpose and the phrase adds no distinct commitment or condition.
- An author's actual preference, a specific goal, and a plan contingent on approval remain substantive information.
- The word “hope” does not itself decide whether to delete a sentence.

The four new requests were generated in a new context and reviewed by another editor that did not read the skill, previous outputs, or the earlier rubric.

| Case | Observed result |
| --- | --- |
| CW19, Traditional Chinese release note | Removed generic convenience/experience framing; kept JSON availability, planned CSV status, and required administrator approval |
| CW20, English personal note | Kept the note unchanged, including the author's preference for a manual check and its reason |
| CW21, Chinese conditional plan | Kept the hoped-for 2027 May pilot, East China-only scope, budget approval dependency, unknown launch date, and distinction from full deployment |
| CW22, English release note | Removed generic experience framing; kept JSON availability, planned CSV status, and administrator approval |

The second editor recorded fidelity and task compliance for **4 / 4**. Its readability ratings were subjective. These are targeted regression checks following an observed issue, not a second A/B benchmark or four extra wins over the ordinary flow.

See [requests](../evals/regression-requests.json), [actual outputs](../evals/runs/clearweave-regression.json), and [raw follow-up review](../evals/regression-review.json).

## 4. Local literal checks on generated writing

The helper compared the 12 initial edit/shorten outputs whose output contract permits a source-to-revision literal comparison. Translation, diagnosis, critique, and drafting were excluded from this particular count because they produce a different kind of deliverable.

Eleven of these 12 outputs had no changes in the helper's supported literal multiset. CW18 produced a warning because shortening reduced the repeated numeral `12` from two occurrences to one. The response still identified the 12 respondents and preserved the substantive counts. This is a legitimate deduplication under the user's shortening request, illustrating why a literal warning needs editorial judgement.

Conversely, a negation change or swapped number-to-actor assignment may produce no warning. The deterministic tests include both blind spots and require `semantic_review_required: true`. No zero-warning result is treated as proof of preserved meaning.

## 5. Code and packaging validation

The final local suite passed **46 tests: 43 checker tests and 3 installer tests**, on Python 3.12.14. Command results and run time are recorded in [validation.json](../evals/validation.json), with [unittest output](../evals/unittest.log). The suite exercises candidate locations, protected regions, quantities and units, URL brackets, code and citation changes, stdin, Unicode errors, exit codes, installer boundaries, and documented semantic blind spots.

A separate reviewer ran the initial 37-test suite and additional probes. The retained [code review](checker-review.md) identified two defects for correction before release:

1. Delimiter examples inside protected regions could extend protection into subsequent ordinary prose. The fix makes structural scanning respect enclosing regions and adds boundary regressions.
2. The documentation claimed simple bare Pandoc citation markers while the implementation recognized only bracketed forms. The final implementation records conservative bare `@key` matches as `at_key`, excludes common email and escaped forms, and documents the ambiguity with social mentions. It does not claim to establish bibliographic identity.

The [independent final review](checker-review-final.md) re-ran the 46-test suite and repository validator, confirmed both original reproductions were fixed, and checked that quotations containing inline code still protect the complete quoted text. It found no remaining material defect within that targeted scope. The tooling reference also states that Traditional Chinese phrase spelling coverage is limited.

The anonymous writing reviewer also found that the review-preparation script appended a literal backslash-n after the JSON object. We corrected the serializer and added a strict parse check for every JSON artifact. The correction changed serialization only; all candidate strings and judgements were preserved.

The final packaging gate also exposed over-escaped regular expressions in the repository validator itself. We corrected its frontmatter and reference-link patterns and re-ran the gate successfully. The skill-creator validator independently accepted the skill structure. The repository validator checks linked runtime references, all 32 source IDs and their target files, required release files, strict JSON parsing, and complete original output coverage. GitHub CI re-runs the deterministic suite and repository validation on Python 3.10 and 3.13. Its actual run status belongs to the repository's Actions history; this report does not substitute a planned workflow for a completed run.

## 6. What remains unproven

- No comparison across model providers, parameter settings, long-document workloads, or repeated random samples.
- No independent human editing panel and no objective measurement of “human voice.”
- No GPTZero, Turnitin, or other detector testing; no promised detector pass rate.
- No factual verification of real claims or literature during these synthetic editing tasks.
- No full DOCX/PDF layout-preservation test and no automatic skill-discovery test across all hosts.
- The checker remains a limited pattern recognizer. Markdown/LaTeX nesting, unknown units, written-out numbers, attribution, causation, and subtle implications require appropriate review.

The practical release claim is therefore narrow: ClearWeave provides one coherent bilingual editing workflow, traceable decisions from the 32-source inventory, local tools with tested contracts and explicit blind spots, and retained examples of its actual behaviour. The recorded results do not justify saying it is categorically better than ordinary prompting.
