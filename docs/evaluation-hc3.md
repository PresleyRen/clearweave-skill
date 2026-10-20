# HC3 public-corpus application test / 真实公开语料测试

Date: 2026-10-20. Evaluated runtime: **ClearWeave v0.2.0**, commit `c5ad877b0d98c4d2bf20788e611839c00fa1188e`. All 15 tracked runtime-file hashes matched the snapshot. The skill was not modified to improve these results.

## What was actually tested

The current conversational assistant read the skill and applied it to existing HC3 answers. Python executed the literal, cue-risk and surface-lint checks on the resulting text. No independent editor, additional inference API, standalone Codex invocation, commercial AI detector or A/B baseline was used. Self-review is explicitly labeled as such.

This is **real public corpus data, not invented examples**. It is also **not the HC3 paper's official test split**: the domain JSONL files are exposed as `train` by the Hugging Face loader. The authors separately link their experimental splits. Possible exposure during host-model pretraining is unknown. Do not report this as held-out benchmark accuracy, unseen-data performance, or superiority over the 32 source skills.

Sources: [HC3 English](https://huggingface.co/datasets/Hello-SimpleAI/HC3), [HC3 Chinese](https://huggingface.co/datasets/Hello-SimpleAI/HC3-Chinese), and the [authors' corpus/split documentation](https://github.com/Hello-SimpleAI/chatgpt-comparison-detection/blob/main/HC3/README.md).

## Sampling and provenance

| Source | Pinned revision | Original rows | Selected answers |
| --- | --- | ---: | ---: |
| English `wiki_csai.jsonl` | `4d0ff18143b5a7e1b1e79beb540c04549d1e59d3` | 842 | 6 ChatGPT + 2 human |
| Chinese `open_qa.jsonl` | `09a687b8dc164b89e7df95abf15df3b216bc31c2` | 3,293 | 6 ChatGPT + 2 human |

The files were downloaded in [collection run 39378728153](https://github.com/PresleyRen/clearweave-skill/actions/runs/39378728153), before any rewrite. Selection sorts eligible answer-0 records by SHA256 of `clearweave-hc3-20261020-v1|language|zero-based-row`. English length: 90–230 whitespace-delimited words; Chinese length: 170–450 Unicode code points. A documented Chinese question-keyword filter was used. The first six ChatGPT records and two human records from different questions were retained per language.

The question filter was too broad: `计算` and `程序` admitted two financial questions. They remain in the manifest but were excluded from this non-high-stakes editing experiment **without replacement**. This is a sampling limitation, not a claim that the skill cannot edit financial language. Four selected Chinese answers end mid-sentence. They also remain in the record, unchanged; the model was not allowed to fabricate a continuation. Human labels describe the corpus's source, not correctness or ideal writing quality.

Full source-file SHA256 values, per-answer hashes, positions and field names are in [manifest.json](../evals/hc3-2026-10-20/manifest.json) and [cases.json](../evals/hc3-2026-10-20/cases.json). [edits.json](../evals/hc3-2026-10-20/edits.json) records actual outputs, holds, exclusions, hashes and the initial draft of the repaired case. A null revision means use the unchanged original, not a missing or empty model answer.

## Results

| Observation | Result | Interpretation |
| --- | ---: | --- |
| Selected public answers | 16: 12 ChatGPT, 4 human | Not 16 successful rewrites |
| Actually edited | 9: 7 English, 2 Chinese | Same-assistant applications |
| Adequate source retained unchanged | 1 English human answer | No-op is allowed |
| Truncated source held unchanged | 4 Chinese answers | Not scored as finished revisions |
| Financial scope exclusions | 2 Chinese answers | Filter leakage recorded, no resampling |
| Edited outputs with supported literal changes | 0/9 | Limited string preservation only |
| Edited outputs with cue-risk warnings | 4/9 | Each reviewed; warnings are not automatic failures |
| Surface-lint candidates | 0 before, 0 after across all 16 | A meaningful coverage weakness, not absence of formulaic language |
| Targeted author-review repair | 1 Chinese output | Initial and repaired text are both retained |
| Existing deterministic tests rerun | 179 passed | These are code/fixture tests, not 179 real-data rewrites |

The static linter found no candidates even in repetitive corpus answers. It therefore cannot measure the improvement observed in these examples. The visible edits came from host-model use of the instruction workflow, not from a rewriting engine in the Python helper. The linter was deliberately left unchanged during this evaluation.

Cue-risk candidates occurred in type-system text, the human Boolean-network passage, the Chinese Mo Yan answer, and the Chinese relationship/social-network answer. Examples include `not possible` becoming `impossible`, `possibly` becoming `may`, or replacing an explicit causal connective with an explanatory clause. They require contextual review rather than automatic rejection or a silent whitelist.

In `HC3-ZH-CHATGPT-02605`, the initial rewrite omitted an explicit frequency qualifier and changed the wording of unspecified circumstances to types of content. Author self-review restored these qualifiers in one targeted repair. The literal check had not detected this semantic issue. The repaired output is not evidence that a model-independent semantic checker exists.

Several source claims also deserve domain verification: the row/card wording in the punched-card answer, simplified type-safety statements and the historical business-school program list. This task did **not** authorize factual rewriting. Claims were not silently corrected, and these outputs are not certified factual references or current advice.

## Chinese example: existing ChatGPT answer, row 2605

Source: `Hello-SimpleAI/HC3-Chinese`, `open_qa.jsonl`, zero-based row **2605**, `chatgpt_answers[0]`. Question: 为什么人们那么喜欢看前男友前女友或者现男友现女友前任们的社交网络？（如微博）?

### Original — unaltered corpus text

> 人们喜欢看到前男友前女友或者现男友现女友前任们的社交网络可能是出于好奇心或者比较关心对方的原因。有时候，人们会想知道对方在社交网络上发布了什么信息，或者对方的生活情况如何。此外，人们可能还有一些心理上的需求，比如想知道自己是否被前任取代了，或者是否还有机会和前任复合。
>
> 然而，在社交网络上看到前任的信息并不一定是一件好事。在某些情况下，这可能会让人感到不安或者心烦，特别是当前任对象在社交网络上发布了一些让人不满意的信息时。因此，最好的做法是保持一定的距离，不要把自己的情绪完全依赖于社交网络上的信息。

### ClearWeave-guided final output

> 人们喜欢查看前任或现任伴侣的前任在社交网络上发布的内容，可能是出于好奇，也可能是比较关心对方。有时，人们想知道对方发了什么、近况如何；也可能有心理上的需求，比如想知道自己是否已被前任取代，或者是否还有机会复合。
>
> 但看到前任的信息不一定是好事。有时，这些信息可能让人不安或心烦，尤其是看到让自己不满意的内容时。因此，最好保持一定距离，不要让自己的情绪完全依赖于社交网络上的信息。

Length: **252 → 189 Unicode code points**, including whitespace and punctuation; 25% shorter. This is a length change, not a validated naturalness score. The observable changes are shorter repeated noun phrases and simpler transitions. Possibility, frequency, examples and the source's recommendation remain. No invented personal experience is added. This is an editing example, not independently verified psychological guidance.

## English technical example: Petri net, row 809

Source: `Hello-SimpleAI/HC3`, `wiki_csai.jsonl`, zero-based row **809**, `chatgpt_answers[0]`.

Original opening:

> A Petri net is a mathematical modeling language for the description of distributed systems. It is a directed bipartite graph consisting of places, which represent states in the system, and transitions, which represent events that can occur and change the state of the system. The graph is decorated with additional information, such as tokens, which represent the current state of the system, and arcs, which represent the flow of control or communication between places and transitions.

Revised opening:

> A Petri net is a mathematical modeling language for distributed systems. It takes the form of a directed bipartite graph: places represent system states, and transitions represent events that can change those states. Tokens indicate the current state; arcs represent the flow of control or communication between places and transitions.

The complete answer went from **169 → 112 whitespace-delimited words**. Terms, examples and analysis methods were retained under the editing contract. The source's broad evaluation about a rich history was retained rather than silently reclassified as false or fact-checked. Definitions were not independently verified.

## Reproduce the checks

```bash
# Network is explicit; two pinned public data files are fetched and hashed.
python3 tools/evaluate_hc3.py --download

# Later offline replay. This does not call a model or regenerate the edits.
python3 tools/evaluate_hc3.py
python3 -m unittest discover -s tests -v
python3 tools/validate_repo.py
```

The script verifies source hashes and the 15-file runtime snapshot, then regenerates literal/risk/lint reports. It fails if the originals, revisions or frozen runtime hashes do not match. Once the runtime changes, preserve this historical snapshot instead of presenting its measurements as results for the new version.

The [HC3 replay workflow](../.github/workflows/hc3-evaluation.yml) stores originals, checks and input/output records as an artifact. Artifacts expire according to retention settings; the pinned source/answer hashes and recorded edits remain sufficient to retrieve and replay the data. The workflow does not generate new edits or independent human ratings.

## Limitations and next repair locations

- **Linter coverage:** surface rules in `clearweave_check.py` missed the repetitions in this slice. Add contextual diagnostic candidates with false-positive controls, not a universal ban on `Overall`, lists or connectors.
- **Qualifier loss:** strengthen reviewer attention under `CW05` / `preservation.md`; string counts alone cannot establish scope preservation. This run did not change the skill.
- **Source quality:** truncated or out-of-scope inputs need explicit triage; they must not be counted as successful final outputs.
- **External validity:** a small, length-filtered historical Q&A sample cannot establish performance on full English research papers, recent models, other domains or all 32 upstream methods.
- **Evaluation independence:** writing and semantic review used the same assistant. No blind preference score, significance claim or guarantee of detector behavior is justified.

## Data attribution and license boundary

HC3: Biyang Guo, Xin Zhang, Ziyuan Wang, Minqi Jiang, Jinran Nie, Yuxuan Ding, Jianwei Yue and Yupeng Wu (2023), *How Close is ChatGPT to Human Experts? Comparison Corpus, Evaluation, and Detection*, arXiv:2301.07597; distributed by Hello-SimpleAI. The authors list the dataset as CC BY-SA 4.0 subject to stricter source terms; their table lists English wiki_csai as CC BY-SA and Chinese open_qa source as MIT.

Corpus excerpts and their edited adaptations in this report/evaluation directory retain **CC BY-SA 4.0** attribution and share-alike scope; original corpus statements are not endorsed. ClearWeave code remains MIT. This boundary does not relicense upstream text. The supplied original and adapted text is clearly distinguished above.
