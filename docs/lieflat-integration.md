# Lieflat integration / 精准清理能力整合

Source: [larashero3-dotcom/lieflat-less-ai-tone](https://github.com/larashero3-dotcom/lieflat-less-ai-tone/tree/27d29232f10124db904ca9c0536d0b67cb3b2833), MIT, Copyright (c) 2026 shiujan. Fixed revision and inspected Git blob IDs are in [source snapshot](lieflat-source-snapshot.json). ClearWeave 0.4.0 adds a selected precision mode to the existing bilingual editor.

## Coverage / 能力对应

| Upstream capability | Integration | Route |
| --- | --- | --- |
| Whitelist and smallest intervention | Explicit `lieflat` mode; unmatched text and structure locked | CW49, CW53 |
| Style guide before editing | Read designated/project-scoped guide; preserve punctuation preferences | CW49, CW54 |
| LF01–LF09 | Each family has a definition, context exceptions and located candidates | CW50; assets/lieflat-rules.json |
| LF10 and its five types | Five separate candidate subtypes plus semantic instructions | CW51 |
| LF11 paragraph reference | Nonfirst Chinese prose paragraphs, first-sentence reference review | CW50, CW54 |
| Excluded popular heuristics | Questions, passives, nominalization, noun repetition, in-sentence parallelism and regular length remain valid | CW54 |
| Sentence/paragraph/corpus scripts | Reimplemented as scan, measure and compare-corpora | CW52 |
| Final acceptance checklist | Rule-linked edit ledger, exact reconstruction, structure/literal checks | CW53 |
| Future rule revision | LF → CW → CF → source → implementation → test | CW54 |

## Resolved conflicts / 已处理冲突

| Issue in the upstream combination | ClearWeave decision | Tests |
| --- | --- | --- |
| Global whitelist would disable existing writing modes | Apply it only to explicitly selected finished-draft cleanup | CF35; mode routing tests |
| Removing antithesis can erase a real exclusion | Keep rejected alternatives when they define the claim | CF36; protected-negation fixtures |
| Enumeration examples can drop a middle item | Keep every item; alter only the connection | CF37; inventory fixtures |
| Style guide claimed unconditional priority | Style preferences govern style; facts and the current task remain fixed | CF38 |
| Removing 当…时 or swapping 然而 can change logic | Keep temporal, conditional, contrastive and causal relationships | CF39 |
| Research reports AI/human while one script reports human/AI | All new reports label the direction B/A; undefined ratios are null | CF40; rate tests |
| Research says blank-line paragraphs, script counts lines | Wrapped prose is grouped; supported code/quotes/list/table blocks excluded | CF41; parser tests |
| Heading regex also matches body ordinals in upstream | Actual heading nodes only; require three consecutive same-level ordinal headings; preserve references/procedure mode | CF42 |
| Nominalization accepted in rule 8 but rejected in research | No standalone nominalization trigger in precision mode; existing grammar editor remains separate | non-trigger tests |
| Missing reference checked only at the start by upstream script | Inspect the complete first sentence for reference cues; final antecedent choice is contextual | LF11 tests |
| Generic material-density or three-example claims | No data invention, generic threshold or compulsory three-item reduction | LF08 and narrative controls |

## Usage flow / 工作流

```text
Current task + Chinese draft + scoped style guide
    → choose full editing / diagnosis / lieflat precision
    → lock document structure and information
    → locate LF01–LF11 (LF10a–e)
    → review each candidate's genre, function and author habit
    → make minimal, rule-linked edits
    → reconstruct revision from ledger
    → compare protected literals and review actual meanings
    → deliver the selected output

Corpus analysis: local texts → same segmentation → counts + coverage + denominator
                → per-document results → B/A comparison → inspect examples
```

## Files and extension / 文件与扩展

Definitions: `skills/clearweave/assets/lieflat-rules.json`. Editing policy: `references/lieflat.md`. Local helper: `scripts/clearweave_tone.py`. Regression tests: `tests/test_tone.py`. The main registry has 46 sources, 262 source decisions, 54 capabilities and 42 conflict families. All original source decisions and capabilities are retained.

The source reports a 629-article corpus, but does not distribute it. Its historical numbers are not imported as thresholds, scores or ClearWeave test results. The new operators have their own documented counting scope. Candidate matches do not decide whether a valid contrast, time condition, metaphor or author preference should be edited. See [evaluation](evaluation-lieflat.md) for actual measurements on available public text and constructed regression cases.
