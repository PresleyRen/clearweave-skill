# Academic composition and scoped cleanup

<a id="cw55"></a>

Read this guide before composing the first paragraph of an English manuscript, abstract, proposal or reviewer reply, and before editing existing English academic prose. Use the language of the deliverable: a Chinese request for English Results follows this route. Apply the selected rules while composing each paragraph. Keep ClearWeave as the entry point.

## Choose the operation once

| Material and request | Mode | Work to perform |
| --- | --- | --- |
| Notes, evidence, an outline, or a requested new section | **Draft** | Use the existing evidence map and section plan, then compose supported sentences. Check evidence, terminology and expression before moving to the next paragraph. |
| Existing text; grammar, clarity, flow or author-voice editing | **Polish** | Make the smallest changes within the requested scope. Grammar-only requests stay grammar-only. Reorganize only when the request includes it. |
| Finished academic text; “only remove stock phrases”, “minimal cleanup”, “成稿清理”, “只去味不润色” | **Cleanup** | Keep headings, paragraph breaks, lists, tables and argument order fixed. Change only a located expression problem and its necessary grammatical repair. Preserve every unmatched span exactly. |
| A request to diagnose any of the above | **Diagnosis only** | Report located problems and optional repairs without producing a rewritten manuscript. |

Infer the mode from the action and material; do not ask a routine questionnaire. “Submitted” describes document status and does not override an explicit request to restructure. For explicitly selected `lieflat`, keep its Chinese-only scope; for English academic cleanup use this guide. For mixed-language cleanup, apply each requested language route to its own spans and preserve the document structure. Chinese academic drafting retains the Chinese route in [drafting.md](drafting.md); its facts and editing boundaries follow the same preservation contract.

One passage has one language editor. A section planner can arrange evidence, but an Academic Humanizer pass is not followed by a generic Humanizer rewrite. Read a chosen guide once per task and reuse the relevant decisions; do not fetch it again for each paragraph. Preserve good original sentences and allow a no-change result.

## Load only useful external guidance

The modes and checks in this file are bundled and work offline. The source-specific companions provide optional detail; failure to read them does not block supported writing.

| Need | Pinned companion | Relevant use |
| --- | --- | --- |
| English academic drafting, polishing or cleanup | `academic-humanizer` — [junbolian](https://github.com/junbolian/Academic-Humanizer/blob/62b0a02627e063015466c70f0a4dd4929a9f7f5b/academic-humanizer/SKILL.md) | Read the matching Draft, Polish or Cleanup guidance. Before the first revision using this source, read its `examples` resource with the adaptations below. |
| A substantive claim–evidence question, supplied author/venue samples, or a requested proposal | `academic-humanizer-evidence` — [AIScientists-Dev](https://github.com/AIScientists-Dev/academic-humanizer/blob/94b88b23703bed7df507acae7d6d5876209a0cdf/SKILL.md) | Read only the applicable evidence, style or proposal section. Feed the decision to the same writer, without a second complete rewrite. |

Use `python3 scripts/read_companion.py NAME` from the installed ClearWeave directory. For junbolian examples, add `--resource examples`. Prefer an exact local match; the reader checks source digests and can fetch the pinned public instructions. Use `--offline` when requested and `--local /path/to/skill` for a designated checkout. These two upstream projects both use the name `academic-humanizer`; distinguish them by repository and digest, never by the frontmatter name alone. Fetch instructions only. Manuscripts and private style samples stay in the authorized writing environment. The reader does not install companions or execute their scripts.

If a chosen instruction or referenced resource cannot be read, continue with this bundled guide and [academic.md](academic.md), applying [anti-defensive.md](anti-defensive.md) and [author-voice.md](author-voice.md) as needed. Report the fallback only when relevant or requested; do not claim an external guide was used. junbolian derives partly from AIScientists, so their agreement is not independent validation.

## Write with the evidence and section purpose

Reuse the map in [manuscript-routing.md](manuscript-routing.md): result or claim, comparator, metric/value/unit/denominator, conditions, uncertainty, and actual source location. A short passage needs only a brief internal check. Keep observations, explanations, proofs and proposed work distinct. Use actual reviewer comments for replies and accurately distinguish completed changes from planned experiments.

Use these checks when the corresponding problem occurs; they are not word bans or a paragraph template.

| Candidate problem | Smallest useful action | Preserve the legitimate case |
| --- | --- | --- |
| Empty opening, importance announcement, or repeated conclusion | Start with the supplied finding or necessary context; remove the redundant announcement | Keep background needed to understand the question and summaries with an independent reading purpose |
| Stacked uncertainty or defensive commentary | Remove repeated attitude or uncertainty only when the remaining proposition makes the same commitment | Keep `may`, `suggests`, exclusions, negative results and conditions that affect the claim |
| A sweeping novelty, superiority or significance claim | In Draft, state only the supported result; in an edit, flag a substantive evidence problem separately unless correction is requested | Preserve the actual contribution and statistically meaningful uses of terms |
| Methods presented as a drafting or debugging diary | Describe the supplied scientific operation, its inputs and why it is needed | Keep chronology when it is the method, and retain seeds, tolerances, budgets, retries and implementation identifiers needed for reproduction |
| A newly coined abstract label without a defined operation | Use the actual supplied operation, or identify the unresolved meaning outside the manuscript | Keep defined new concepts, established field terms and original system names |
| Mechanical contrast, parallel structure or transitions | Repair only a repetition or connection that obscures the argument | Keep real contrasts, necessary lists, normal passive voice and the author's punctuation |

For a target journal or author style, use the inspected samples to guide paragraph function, terminology, syntax and register. Samples do not supply this study's facts or automatically become citations. Reuse an existing grounded profile; no sample means no claimed author match. Current journal instructions decide required formatting. Read current funding-call requirements only for an actual proposal task; do not treat a source's fixed agency-scoring description as current policy.

## Preserve scientific content across modes

Use [preservation.md](preservation.md) before changing wording. Preserve each number's role and statistical summary, citation attachment, mathematical assumption, negation and scope. A measured difference does not automatically license removing a hedge from a generalization or mechanism claim.

For LaTeX, identify formulas, theorem/definition statements, assumptions, labels, reference keys, macros and preamble before editing surrounding prose. Keep their scientific content and identifiers unchanged. A request to polish prose does not authorize adding a lemma, creating a proof, changing `optimal` to another technical property, deleting reproducibility details, or inventing a citation. Handle a suspected scientific error as a specific separate issue; make substantive corrections only within the requested evidence-backed correction task. An unavailable fact must not turn into an invented precise value.

ClearWeave's task contract governs these adaptations of both sources:

- Keep useful punctuation, sentence lengths, passive constructions and repeated technical terms. Do not enforce an em-dash ban, vocabulary blacklist or numerical style quota.
- Preserve all supporting citations and the actual statistical aggregation. Do not automatically reduce references to one or two or replace a mean with a range.
- Do not import examples' invented numbers, theorem names, proof steps or deleted settings. Examples illustrate editing decisions, not evidence for the user's study.
- Keep editorial placeholders and audit commentary outside clean manuscript text. A missing fact in Draft limits the supported text; Cleanup leaves disputed factual wording unchanged and identifies the issue separately when material.
- Keep source checks proportionate to changed claims. Ordinary grammar work does not initiate a full literature search or scientific audit.

## Check the delivered passage

For Draft, read each substantive sentence against the supplied evidence. For Polish and Cleanup, compare with the original, checking not just the inventory of numbers and references but which claim they support. Check the same binding across the affected abstract, table, caption or supplement when those files are in scope.

When useful and execution is available, run the existing `clearweave_check.py compare` for protected literals and `clearweave_risk.py` for changed modality, assumptions and some numeric/citation binding swaps. Inspect the reported differences. Cross-reference checking covers documented common LaTeX commands, not arbitrary TeX macros. Do not replace these checks with an upstream exit code: unchanged inventories can still contain changed scientific meaning. For Cleanup also compare the full diff: every changed span needs a concrete expression reason; untouched text and structure stay exact.

Make one targeted repair if the review finds an actual problem, then stop. Deliver the requested text directly. Keep a material unresolved issue or requested change note separate. Publication readiness continues through the existing Paper Review Atlas handoff; a language check does not close evidence-review issues.

## Sources

Adapted from junbolian/Academic-Humanizer at `62b0a02627e063015466c70f0a4dd4929a9f7f5b` and AIScientists-Dev/academic-humanizer at `94b88b23703bed7df507acae7d6d5876209a0cdf`. Both MIT notices are retained in `licenses/` and the source audit records adopted and excluded instructions. This module and its examples are independently worded. No detector score, acceptance outcome or improvement percentage follows from the integration.
