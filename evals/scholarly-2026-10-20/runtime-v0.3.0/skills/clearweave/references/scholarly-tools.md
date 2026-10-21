# Scholarly tools and evaluation

Python 3.10+, standard library only. Commands print JSON and leave inputs unchanged. Run from the repository root, or use the corresponding installed skill paths.

<a id="cw47"></a>
## CW47 · Located academic review candidates

```bash
python3 skills/clearweave/scripts/clearweave_scholar.py scan draft.md --language both
python3 skills/clearweave/scripts/clearweave_scholar.py scan abstract.tex --language en
```

The scanner lists rule IDs, exact offsets, line/column positions and an editing question. AD rules identify stacked hedges, apologies, pre-emptive disclaimers and redundant framing. GR rules identify a few narrow agreement, article and word-form candidates. Quotes, code, math and other protected spans use the shared protection parser. A candidate requires contextual judgment; no automatic replacement is performed.

```bash
python3 skills/clearweave/scripts/clearweave_scholar.py profile samples.json --kind field --label nlp-abstract > profile.json
python3 skills/clearweave/scripts/clearweave_scholar.py compare-profile profile.json draft.md
python3 skills/clearweave/scripts/clearweave_scholar.py learn draft.md final.md --scope academic-abstract
```

`samples.json` contains `samples`, each with a unique `id`, `work_id`, `language` (`en` or `zh`), `text`, and optional `role` (`profile`). `kind` is `field`, `house`, or `author`; choosing `author` asserts the user has designated that corpus. Mixed-language profiles are rejected: create one profile per language. Empty samples are reported, exact duplicates and versions sharing a work ID are counted once. Metrics describe editable prose, with citation/URL protection and approximate sentence splitting.

Minimal `samples.json` structure (replace the illustrative text with your selected writing):

```json
{"samples": [{"id": "paper-a-abstract", "work_id": "paper-a", "language": "en", "role": "profile", "text": "We evaluate a retrieval method on the supplied corpus."}]}
```

`learn` outputs a proposed review record with original/final hashes and changed spans. It calls no model and learns no approved rule by itself. The host follows [author-voice.md](author-voice.md) to interpret and approve preferences.

<a id="cw48"></a>
## CW48 · Public-data evaluation with separate roles

Record source URL, authors, license, revision, exact input hash, requested operation, output, and what actually ran. Keep profile samples, editing samples and constructed conflict probes separately labeled. A published author text is useful for grammar and over-editing checks; it is not AI-generated just because an editor flags it.

Run literal comparison, semantic-cue review and academic scanning, then inspect the actual claims. Report script measurements separately from model/editor judgments. Preserve failed drafts, repairs, unchanged passages and missing-source exclusions. Replaying saved outputs tests the checker and record, not fresh generation.

```bash
python3 tools/evaluate_scholarly.py
python3 -m unittest discover -s tests -v
python3 tools/validate_repo.py
python3 skills/clearweave/scripts/clearweave_trace.py --query "主谓一致"
python3 tools/coverage.py --source S36
```

The public-data record includes a multi-author field-profile corpus, different published abstracts for editing, and Chinese HC3 answers. The current conversational assistant applies the skill and reviews outputs; no independent human panel or commercial detector is implied. Use the saved provenance and requests to run a new host evaluation separately.

## Extend the right component

| Symptom | Module / implementation | Add a regression |
| --- | --- | --- |
| Empty self-defense remains | anti-defensive.md; AD rule | One redundant apology and one necessary qualification |
| Grammar error remains | academic-grammar.md; GR rule | One incorrect form and one legitimate lookalike |
| Wrong author/domain voice | author-voice.md; profile metadata | Relevant vs irrelevant sample scope |
| Meaning changes during style matching | preservation.md; CF30 | Same style, different fact/number |
| Review notes enter the paper | anti-defensive.md; CW46 | Text-only task plus separate review request |

Update the capability catalog, source decision map, positive/counterexamples, and the public-data evaluation appropriate to the change. Re-generate the README tables with `tools/render_catalog.py --write`.
