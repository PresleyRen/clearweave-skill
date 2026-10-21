# Lieflat integration evaluation / 精准清理测试

Date: 2026-10-21. ClearWeave 0.4.0. The new task is **LF-only Chinese finished-draft cleanup**, with original structure and unmatched wording fixed.

## Executed regression checks

383 deterministic tests passed on local CPython 3.13.5. These comprise the earlier 287 tests, 79 new tone-tool/data tests, 16 additional bilingual conflict cases and one new source-link test. The test count is not a count of model rewrites. Regression fixtures cover all eleven rule IDs, the five LF10 candidate subtypes, genre/style exceptions, paragraph segmentation, protected Markdown/code/quotes, denominator choice, zero ratios, exact ledger reconstruction, numbers, heading references, corrupted inputs and historical runtime hashes.

## Public-text application

Four existing public texts were selected from the stored scholarly evaluation: two complete HC3-Chinese answers, rows 2188 and 2605, and the Sentence-BERT and scispaCy abstracts as foreign-language controls. They were previously seen, not held-out examples. Original source identifiers, licenses, pinned revisions and SHA256 hashes are retained in [samples.json](../evals/lieflat-2026-10-21/samples.json).

The current conversational assistant read the new rules, made one new minimal edit and reviewed its effect. No second model API, blind baseline or independent human reviewer was used. The new output is not the broadly polished revision saved in 0.3.0.

| Measure | Observed result |
| --- | ---: |
| Public inputs | 4 |
| Changed Chinese input | 1 |
| Unchanged Chinese control | 1 |
| Unchanged English controls | 2 |
| Local edits | 1 |
| Candidate locations | 4 before → 3 after |
| Unlisted changes | 0 |
| Supported protected-literal changes | 0 |
| Structure/ledger checks | Passed for all 4 records |

The remaining three candidates were deliberately kept: a complete list of distinct domains, a meaningful contrast and an inference connector. Matching a surface rule did not force a rewrite. These counts document behavior on these examples; they are not a naturalness score, detection accuracy or evidence of reduced AI-detector scores.

## Actual example / 真实片段

Source: [HC3-Chinese](https://huggingface.co/datasets/Hello-SimpleAI/HC3-Chinese), `open_qa.jsonl`, revision `09a687b8dc164b89e7df95abf15df3b216bc31c2`, row 2605 (zero-based), `chatgpt_answers[0]`, CC BY-SA 4.0.

Before:

> 此外，人们可能还有一些心理上的需求，比如想知道自己是否被前任取代了，或者是否还有机会和前任复合。

After:

> 人们可能还有一些心理上的需求，比如想知道自己是否被前任取代了，或者是否还有机会和前任复合。

LF10d: `还` already expresses addition, so only the redundant initial connector was removed. The two-paragraph original, every other word, all uncertainty, and the contrast/inference markers remain exactly unchanged. This illustrates the requested minimum-change contract, not a large rewrite. The explanation in the corpus is not independently validated psychological advice.

The other Chinese record retained `历史、文化、政治` as distinct list members. The English controls stayed unchanged, including any grammar imperfections: Chinese precision cleanup does not silently invoke the broader grammar editor.

## Reproduce

```bash
python3 -m unittest discover -s tests -v
python3 tools/evaluate_lieflat.py
python3 tools/evaluate_lieflat.py --download
python3 tools/validate_repo.py
```

Offline replay checks stored original/output hashes, current runtime fingerprints and exact edit ledgers. `--download` retrieves the pinned public originals through the existing source verifier. It does not regenerate revisions. Full before/after texts, reasons and ledgers are in [outputs.json](../evals/lieflat-2026-10-21/outputs.json); machine results are in [report.json](../evals/lieflat-2026-10-21/report.json).

The 0.3.0 scholarly runtime is archived unchanged under `evals/scholarly-2026-10-20/runtime-v0.3.0`. Its original protocol, output revisions and test report are unchanged. The 0.2.0 HC3 snapshot remains unchanged as well.

## Upstream measurement reconciliation

The upstream research corpus is not distributed, so its corpus-size and rate claims were not independently reproduced. Inspection found different ratio directions between research text and a script, line-based versus blank-line paragraph definitions, a body-ordinal detector used for heading-related counts, and a start-only anaphora test. ClearWeave uses its own documented operators and tests those distinctions directly. Semantic applicability of a candidate, a true syntactic parse and a reference target are still reviewed by the editor rather than certified by regex.
