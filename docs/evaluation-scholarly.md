# Scholarly evaluation / 真实论文与文风测试

[简体中文](evaluation-scholarly.zh-CN.md) · [Documentation index](README.md)

Date: 2026-10-20. Runtime: ClearWeave **0.3.0**. Test inputs are existing public text, not rewritten synthetic “AI-sounding” prompts. Full source text, authors, licenses, pinned revisions and SHA256 values are saved in the raw record.

## Data and roles

| Role | Source | Records |
| --- | --- | ---: |
| Field profile | BERT, Stanza, Dense Passage Retrieval published abstracts | 3 |
| Published-paper editing | Sentence-BERT; scispaCy; SQuAD; Clinical Concept Extraction; Semantic Chain Shifts; Circular Economy | 6 |
| Chinese editing | HC3-Chinese `open_qa.jsonl`, rows 2188 and 2605, `chatgpt_answers[0]` | 2 |

ACL metadata is pinned at `acl-org/acl-anthology@0d4dd55c88a79724914e339ba3511086c05653d0`. The three profile records are disjoint in work ID and exact text from all edit records. They form a **multi-author NLP field profile**, not an individual author’s personal voice. The initial named records were collected before editing. Three W19 cases were added after inspecting abstracts containing framing or hedge cues. Chinese cases are complete examples reused from the earlier HC3 evaluation, pinned at `09a687b8dc164b89e7df95abf15df3b216bc31c2`.

This is a convenience/development application set, not a held-out benchmark. Sentence-BERT was inspected before narrow agreement patterns were implemented. Earlier HC3 exposure and unknown host pretraining exposure preclude unseen-data claims. The SQuAD XML has no abstract. The main branch supplied a reviewed excerpt from the same paper’s PDF; page 1 was visually checked in this session. It is included as an unchanged control, with the XML absence and PDF provenance retained.

## Procedure

The current conversational assistant read the final modules, used the three profile texts as descriptive field context, wrote the revisions, and performed one targeted self-review. No separate inference API, blind model comparison or independent human reviewer was used. Temperature and sampling seed were not exposed. Revisions and self-review are saved separately from executable checks.

The Python helper actually measured the profile, scanned originals and revisions, compared protected literals, reported lexical risk cues and checked the data/runtime fingerprints. Actual temporary-project installation and execution of scan/profile/compare-profile/learn succeeded; installed runtime hashes matched the tested files. The whole deterministic suite passed **287 tests**; this includes fixture and source-link tests, not 287 model rewrites.

## Measured results

| Measure | Result |
| --- | ---: |
| Usable editing inputs | 8: six papers and two Chinese answers |
| Revised | 6: four papers and two Chinese answers |
| Unchanged controls | 2: scispaCy and SQuAD |
| Academic scan candidates | 5 before → 0 after |
| Revised outputs with supported literal differences | 0/6 |
| Revised outputs with lexical risk candidates | 4/6 |
| Profile samples | 3, with separate IDs and hashes |
| Deterministic regressions | 287 passed |

Five-to-zero is the count of these narrow regex candidates in this selected set, not an AI probability, naturalness score or false-negative estimate. Zero literal differences means protected strings matched, not complete semantic equivalence. A single named unit such as Research and Development can legitimately trigger the coordinated-subject rule; this is retained as a candidate/false-positive test.

## What changed in the real examples

Sentence-BERT: corrected coordinated-subject agreement and a relative-clause verb; shortened the publication announcement and clarified the network-input requirement. All supported numerical/citation strings remained. The final pronoun `it` has an unresolved reference in the source; it was retained rather than broadening the comparative claim without full-paper evidence.

Clinical Concept Extraction: removed the emotional introduction to a negative result. The finding that the concepts did not improve the document-level task remained exactly present. Semantic Chain Shifts: consolidated duplicated possibility while retaining uncertainty, the likely mechanism and historical time range. Circular Economy: removed redundant framing and corrected agreement while retaining hypothesis and evidence statements.

scispaCy and SQuAD: retained as unchanged controls. SQuAD keeps the meaningful comparison with human performance, all figures and the source’s interpretation. scispaCy: its contrast and technical term robust serve the text. The Chinese cases shorten repeated descriptions. Self-review of row 2605 restored 喜欢 and the explicit alternative; both the initial draft and final revision remain in outputs.json. The literal checker did not identify that semantic detail.

## Risk-cue review

| Case | Cue change | Same-assistant review |
| --- | --- | --- |
| Sentence-BERT | requires → must / time required; causes → creating | Requirements and causal relationship retained; connective inventory changed. |
| Semantic Chain Shifts | may possibly → may | Redundant possibility removed; uncertainty remains. |
| HC3 row 2188 | 因为 → 因此 | The source speaker’s limitation remains the stated reason; historical claim not updated. |
| HC3 row 2605 | Three occurrences of 可能 → four | Alternatives expressed separately; additional cue is not a new causal claim. |

All four remain visible as warnings. This record does not benchmark the script’s semantic accuracy. The helper does not generate the revisions, prove authorship or run a commercial AI detector. The raw outputs support inspection and independent re-evaluation.

## Reproduce

```bash
python3 tools/evaluate_scholarly.py
python3 tools/evaluate_scholarly.py --download --write
python3 -m unittest discover -s tests -v
python3 tools/validate_repo.py
```

The first command replays diagnostics offline. `--download` retrieves pinned public source files and checks each XML/JSONL original against them; the recovered SQuAD excerpt is checked against the attributed reviewed record, not presented as a fresh PDF download; it sends no draft to an inference service. Replaying recorded outputs is distinct from a fresh editing run. For new model trials, use protocol.json, keep the role split, save newly generated outputs in another run folder, and report the model/configuration actually used.

[Raw record](../evals/scholarly-2026-10-20/) · [Originals and revisions](scholarly-examples.md) · [Integration decisions](scholarly-integration.md)

## Attribution

Published ACL text: [ACL licensing policy](https://aclanthology.org/faq/#what-is-the-copyright-for-materials-in-the-acl-anthology), CC BY 4.0 for these 2016–2020 papers. Authors, paper URLs and modifications are identified per sample. HC3: [Hello-SimpleAI/HC3-Chinese](https://huggingface.co/datasets/Hello-SimpleAI/HC3-Chinese), CC BY-SA 4.0; the test records preserve the corpus provenance. Examples are editing demonstrations, not corrections endorsed by the original authors.

## Historical replay

The v0.2.0 HC3 manifest and outputs remain unchanged. Its 15 runtime files are archived byte-for-byte under `evals/hc3-2026-10-20/runtime-v0.2.0`, and the historical evaluator uses those files. Current scholarly edits are checked with v0.3.0. `tools/preflight.py` runs both plus the main-branch source-collection integrity checks.
