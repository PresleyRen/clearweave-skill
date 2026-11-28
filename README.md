# ClearWeave · Scholarly

**English–Chinese natural prose, direct research writing, academic voice and precise finished-draft cleanup.**

[简体中文](README.zh-CN.md) · [Documentation](docs/README.md) · [Skill](skills/clearweave/SKILL.md) · [Capability index](docs/capabilities.md) · [Published-paper examples](docs/scholarly-examples.md)

ClearWeave drafts papers and technical documents from your notes and edits existing papers, READMEs, work emails and everyday writing. It removes stock phrasing and repetition, brings the contribution into focus, corrects academic grammar, and builds reusable style profiles from selected samples. Choose the language of the finished text and editorial notes separately.

For evidence mapping, section drafting, target-journal adaptation, submission consistency or formal LaTeX editing, see the [task-to-skill routing table](skills/clearweave/references/manuscript-routing.md). ClearWeave reuses an existing evidence map and section plan, selects a specialist when needed, and applies the academic language guidance from the first paragraph.

## Capabilities

| Module | What it does | Typical output |
| --- | --- | --- |
| **English academic language** | Applies the same evidence and expression rules in Draft, scoped Polish and fixed-structure Cleanup. | Supported first drafts, polished passages or minimal cleanup |
| **Lieflat precision cleanup** | Eleven Chinese pattern families, minimal rule-linked edits and fixed document structure. | Finished draft with unmatched text preserved |
| **Corpus and edit-ledger checks** | Candidate locations, comparable denominators, corpus comparisons and exact edit reconstruction. | Measurements and edit verification |
| **Natural bilingual prose** | Revises empty openings, mechanical paragraphs, repeated conclusions, over-explanation, translation-shaped Chinese and nominalized English. | Clear revised prose |
| **Anti-defensive editing** | Separates empty apologies and pre-emptive defenses from meaningful qualifications; states claims, evidence and comparison conditions directly. | Focused abstracts, introductions and conclusions |
| **Academic grammar** | Selects tense by sentence function; checks agreement, articles, number, pronouns, modifiers, parallelism and information flow. | Grammar edits with reasons |
| **Argument and section structure** | Connects questions, methods, evidence and contributions; synthesizes related work and distinguishes planned from completed research. | Reverse outlines and section drafts |
| **Sample-grounded voice** | Extracts syntax, register, structure and terminology habits from selected papers or personal samples, scoped by language, discipline and section. | Author, house or field profiles |
| **Revision-based preferences** | Compares an initial draft with an approved final version and records scoped preference proposals. | Evidence-linked edit records |
| **Meaning and terminology checks** | Reviews quantities, units, negation, conditions, evidence strength, comparison groups and work status; preserves quotes, citations, equations, LaTeX labels and reference keys, and code. | Differences and review locations |
| **Critique and responses** | Identifies argument gaps and inconsistencies, organizes point-by-point responses, and checks manuscript excerpts. | Reviews, response letters and clean drafts |
| **Translation, drafting and shortening** | Writes from supplied material, adapts language and locale, and consolidates repetition. | Target-language prose |
| **Long documents and maintenance** | Maintains terminology and claim ledgers, handles selected files and locates rules, sources, conflicts and tests. | Per-file results and extension routes |

**New in 0.5.0:** a built-in Academic Humanizer protocol for English Draft, Polish and Cleanup (CW55), optional source-specific academic guidance, and literal checks for LaTeX labels and cross-references.

## Function map

The request determines the language, genre, section, voice and editing scope. Facts, quantities, conditions, citations and terminology remain protected across the following routes.

| Material and request | Route | Editing scope |
| --- | --- | --- |
| Notes or evidence for new English academic prose | **Draft** | Read the academic guidance before the first paragraph; apply it while composing each paragraph from the existing evidence and plan. |
| An existing English academic passage | **Polish** | Correct grammar, clarity or voice within the requested scope; grammar-only requests stay grammar-only. |
| Finished English academic prose needing only specific expression fixes | **Cleanup** | Preserve headings, paragraph breaks, lists, tables, argument order and every unmatched span exactly. |
| A Chinese draft needing precision cleanup | **Lieflat** | Review LF01–LF11 candidates in context and make only the justified minimal edits. |

General bilingual editing, translation, restructuring, critiques and style profiles keep their task-specific routes. Diagnosis-only requests return located findings without changing the draft. The final review combines literal differences, tool-generated review cues and the editor's meaning check; a script result alone does not establish semantic equivalence.

## Install and use

```bash
git clone --branch main https://github.com/PresleyRen/clearweave-skill.git
cd clearweave-skill
python3 tools/install_skill.py --project /absolute/path/to/your-project
```

The installer copies the skill into `.agents/skills/clearweave` in your project. To update an older installation, move its directory to a backup location, then run the installer from the current `main` checkout. Python helpers use the Python 3.10+ standard library.

### Draft from notes

```text
$clearweave
Write a short Results paragraph for my paper in English using these notes.
Apply the academic Draft guidance from the first paragraph.
On the same 100 queries, the baseline ranked the correct answer first 71 times.
With reranking, it did so 76 times. We have not tested the difference for significance.
```

English manuscripts, abstracts, proposals and reviewer replies use the built-in [academic language protocol](skills/clearweave/references/academic-humanizer.md) before the first paragraph. The optional `academic-humanizer` companion supplies junbolian's academic guidance; `academic-humanizer-evidence` supplies the relevant AIScientists evidence, sample-style or proposal guidance when needed. Both inform the same writer, with one language edit for each passage. ClearWeave reads a matching local or pinned upstream guide when available and continues with its bundled rules offline. General English and Chinese writing retain their language-specific routes. See [first-draft guidance and guide selection](skills/clearweave/references/drafting.md).

### Edit or profile existing text

```text
$clearweave
Edit this paper paragraph for natural academic English. Remove empty defensive
framing and check agreement, tense, articles and modifiers. Keep numbers,
citations, terminology and evidence strength. Explain consequential edits in Chinese.
[paste draft]
```

For a finished English paper that needs only minimal cleanup:

```text
$clearweave
Clean up stock phrasing in this finished English paper using Cleanup mode.
Keep headings, paragraph breaks, lists, tables, argument order, citations,
equations, LaTeX labels and reference keys, and all unmatched text exactly.
Return only the revised passage.
[paste draft]
```

```text
$clearweave
Build a style profile from my supplied paper samples, grouped by section,
syntax, terminology and argument structure. Use it to revise this abstract.
Return only the English abstract.
[samples and draft]
```

```text
$clearweave
给这段中文去 AI 味，保留正式程度，压缩重复解释，只给修改后的正文。
[原文]
```

See [scholarly prompts](skills/clearweave/prompts/scholarly.md) and [precision prompts](skills/clearweave/prompts/precision.md).

## Lieflat finished-draft cleanup

Use this mode for **Chinese prose that should keep its structure and wording except for specific style issues**. The editor reads designated style evidence, locates a rule, reviews its function and changes only the relevant span.

| Rules | Capabilities |
| --- | --- |
| LF01–LF03 | Unnecessary antithesis, dense enumeration and adjacent sentence patterns, with real distinctions and list membership preserved. |
| LF04–LF06 | Functional review of dashes, prompt colons and decorative heading ordinals, calibrated to author habits and references. |
| LF07–LF09 | Idealized occupational analogies, summaries grounded in existing detail and empty opening cues. |
| LF10 | Long premodifiers, when-clauses, topic shells, initial connectors and restatement cues in Chinese. |
| LF11 | Clear antecedents for paragraph-opening commentary. |

```text
$clearweave
Use lieflat whitelist mode on this Chinese draft. Preserve headings, paragraphs,
lists, tables, facts and all unmatched text. Follow the supplied style guide.
Return the revised text only.
[Draft and style reference]
```

English academic cleanup uses the Academic Humanizer **Cleanup** route above. Lieflat remains a Chinese route; broader grammar, drafting and restructuring follow the requested task. See the [integration map](docs/lieflat-integration.md), [rule reference](skills/clearweave/references/lieflat.md) and [real-text records](docs/evaluation-lieflat.md).

```bash
python3 skills/clearweave/scripts/clearweave_tone.py scan draft.md --genre academic
python3 skills/clearweave/scripts/clearweave_tone.py scan draft.md --keep-rule LF04
python3 skills/clearweave/scripts/clearweave_tone.py measure corpus/
python3 skills/clearweave/scripts/clearweave_tone.py compare-corpora --a reference/ --b drafts/
python3 skills/clearweave/scripts/clearweave_tone.py verify-edits original.md revised.md edits.json
```

## Real-text examples

The scholarly application set uses published abstracts for grammar, anti-defensive editing and terminology checks; three separate NLP abstracts form a field-style profile. It also includes two historical Chinese HC3 answers.

| Source | Editing result |
| --- | --- |
| Sentence-BERT | Corrected coordinated-subject and relative-clause agreement; retained quantities, times and citations. |
| Clinical Concept Extraction | Removed an attitude marker while preserving the negative finding. |
| Semantic Chain Shifts | Consolidated stacked uncertainty while retaining `may`, `likely` and time scope. |
| scispaCy | Retained functional contrast, technical vocabulary and the existing structure. |
| Chinese HC3 answers | Compressed repeated descriptions while preserving stance, dates, conditions and uncertainty. |

Read the [originals and revisions](docs/scholarly-examples.md), [evaluation record](docs/evaluation-scholarly.md) and [earlier HC3 examples](docs/evaluation-hc3.md).

## Local tools

The host model edits, translates, reviews arguments and applies voice. Python reports locations, literal differences, review cues, corpus measurements and maintenance routes.

The comparison tool also reports changes to common LaTeX labels and cross-reference commands. This is a literal check with documented syntax coverage; the editor must still review what each number, citation and reference supports. See the [tool limits](skills/clearweave/references/tooling.md).

```bash
python3 skills/clearweave/scripts/clearweave_check.py lint draft.md --language both --format json
python3 skills/clearweave/scripts/clearweave_check.py compare original.md revised.md --format json
python3 skills/clearweave/scripts/clearweave_risk.py original.md revised.md --format json
python3 skills/clearweave/scripts/clearweave_scholar.py scan draft.md --language both
python3 skills/clearweave/scripts/clearweave_scholar.py profile samples.json --kind author --label my-papers > profile.json
python3 skills/clearweave/scripts/clearweave_scholar.py compare-profile profile.json draft.md
python3 skills/clearweave/scripts/clearweave_scholar.py learn original.md final.md --scope English-abstract
```

[Tool reference and sample schema](skills/clearweave/references/scholarly-tools.md).

## Locate and extend

| Concern | Entry point | Capability |
| --- | --- | --- |
| English academic Draft, Polish and Cleanup | `academic-humanizer.md` | CW55 |
| LF-only cleanup, Chinese pattern families and semantic exceptions | `lieflat.md`, `lieflat-rules.json` | CW49–51 |
| Corpus measurement, minimal edits and candidate review | `clearweave_tone.py` | CW52–54 |
| Stock phrasing, translation syntax, flow | `english.md`, `chinese.md` | CW10–14 |
| Defensive framing, contribution, editorial lanes | `anti-defensive.md` | CW37–38, CW46 |
| Tense, agreement, modifiers, semantic scope | `academic-grammar.md` | CW39–42 |
| Academic voice, profiles, approved revisions | `author-voice.md` | CW43–45 |
| Facts, conditions, numbers, references | `preservation.md` | CW03–09 |
| Academic scanner and profile implementation | `clearweave_scholar.py` | CW44–45, CW47 |
| Provenance, tests, failure localization | `maintenance.md`, `scholarly-tools.md` | CW31–32, CW48 |

```bash
python3 skills/clearweave/scripts/clearweave_trace.py --query "grammar agreement"
python3 skills/clearweave/scripts/clearweave_trace.py --id CW37
python3 tools/coverage.py --source S44
python3 tools/evaluate_scholarly.py
python3 -m unittest discover -s tests -v
python3 tools/validate_repo.py
python3 tools/render_catalog.py --write
```

Keep a minimal failure and a legitimate lookalike when adding a rule. Locate the responsible module, add tests, run the relevant public-text checks and update the capability index. See [integration and extension](docs/scholarly-integration.md).

<details>
<summary>All 55 capabilities and their rule locations</summary>

<!-- capabilities:start -->
| Capability | Implementation | Rule location |
| --- | --- | --- |
| **CW01** Task and scope contract | `host` | [SKILL.md](skills/clearweave/SKILL.md#cw01) |
| **CW02** Language, script and spelling | `host` | [references/chinese.md](skills/clearweave/references/chinese.md#cw02) |
| **CW03** Claim ledger and work status | `host+candidate` | [references/preservation.md](skills/clearweave/references/preservation.md#cw03) |
| **CW04** Quantities, units and ownership | `host+literal+candidate` | [references/preservation.md](skills/clearweave/references/preservation.md#cw04) |
| **CW05** Negation, exceptions and scope | `host+candidate` | [references/preservation.md](skills/clearweave/references/preservation.md#cw05) |
| **CW06** Uncertainty and obligation strength | `host+candidate` | [references/preservation.md](skills/clearweave/references/preservation.md#cw06) |
| **CW07** Causality and attribution | `host+candidate` | [references/preservation.md](skills/clearweave/references/preservation.md#cw07) |
| **CW08** Protected quotes, code and citations | `host+literal` | [references/preservation.md](skills/clearweave/references/preservation.md#cw08) |
| **CW09** Document instructions stay data | `host` | [SKILL.md](skills/clearweave/SKILL.md#cw09) |
| **CW10** Argument and paragraph structure | `host` | [references/english.md](skills/clearweave/references/english.md#cw10) |
| **CW11** Idiomatic English syntax | `host` | [references/english.md](skills/clearweave/references/english.md#cw11) |
| **CW12** Idiomatic Chinese and concrete jargon | `host` | [references/chinese.md](skills/clearweave/references/chinese.md#cw12) |
| **CW13** Stable technical terminology | `host` | [references/academic.md](skills/clearweave/references/academic.md#cw13) |
| **CW14** Functional rhythm, not quotas | `host` | [references/english.md](skills/clearweave/references/english.md#cw14) |
| **CW15** Author voice and preference precedence | `host` | [references/workflows.md](skills/clearweave/references/workflows.md#cw15) |
| **CW16** No invented nonfiction specifics | `host` | [references/preservation.md](skills/clearweave/references/preservation.md#cw16) |
| **CW17** Anti-defensive academic expression | `host` | [references/academic.md](skills/clearweave/references/academic.md#cw17) |
| **CW18** Claim–evidence and cross-section consistency | `host` | [references/academic.md](skills/clearweave/references/academic.md#cw18) |
| **CW19** Contribution narrative and adverse results | `host` | [references/academic.md](skills/clearweave/references/academic.md#cw19) |
| **CW20** Rigorous critique and author responses | `host` | [references/academic.md](skills/clearweave/references/academic.md#cw20) |
| **CW21** Diagnosis, no-op and bounded editing | `host` | [SKILL.md](skills/clearweave/SKILL.md#cw21) |
| **CW22** Explicit translation and localization | `host` | [references/workflows.md](skills/clearweave/references/workflows.md#cw22) |
| **CW23** Drafting and shortening from material | `host` | [references/preservation.md](skills/clearweave/references/preservation.md#cw23) |
| **CW24** Genre-aware business, news and personal prose | `host` | [references/workflows.md](skills/clearweave/references/workflows.md#cw24) |
| **CW25** Output, selected files and safe batches | `host` | [references/workflows.md](skills/clearweave/references/workflows.md#cw25) |
| **CW26** Long-document continuity | `host` | [references/workflows.md](skills/clearweave/references/workflows.md#cw26) |
| **CW27** Reusable voice profiles | `host` | [references/workflows.md](skills/clearweave/references/workflows.md#cw27) |
| **CW28** Located bilingual surface candidates | `script` | [references/tooling.md](skills/clearweave/references/tooling.md#cw28) |
| **CW29** Protected-literal comparison | `script` | [references/tooling.md](skills/clearweave/references/tooling.md#cw29) |
| **CW30** Revision-risk cue review | `script` | [references/tooling.md](skills/clearweave/references/tooling.md#cw30) |
| **CW31** Honest layered evaluation | `workflow` | [references/maintenance.md](skills/clearweave/references/maintenance.md#cw31) |
| **CW32** Traceable maintenance and conflict repair | `script+workflow` | [references/maintenance.md](skills/clearweave/references/maintenance.md#cw32) |
| **CW33** Privacy and host boundary | `host+workflow` | [references/workflows.md](skills/clearweave/references/workflows.md#cw33) |
| **CW34** Portable skill and optional tools | `package` | [references/maintenance.md](skills/clearweave/references/maintenance.md#cw34) |
| **CW35** Explicit evidence verification | `host` | [references/academic.md](skills/clearweave/references/academic.md#cw35) |
| **CW36** Clean deliverables and separate notes | `host` | [references/workflows.md](skills/clearweave/references/workflows.md#cw36) |
| **CW37** Function-based anti-defensive editing | `host` | [references/anti-defensive.md](skills/clearweave/references/anti-defensive.md#cw37) |
| **CW38** Contribution and section-function planning | `host` | [references/anti-defensive.md](skills/clearweave/references/anti-defensive.md#cw38) |
| **CW39** Function-sensitive tense and aspect | `host` | [references/academic-grammar.md](skills/clearweave/references/academic-grammar.md#cw39) |
| **CW40** Academic grammar and agreement | `host+candidate` | [references/academic-grammar.md](skills/clearweave/references/academic-grammar.md#cw40) |
| **CW41** Information flow and modifier scope | `host` | [references/academic-grammar.md](skills/clearweave/references/academic-grammar.md#cw41) |
| **CW42** Meaning-sensitive grammar | `host` | [references/academic-grammar.md](skills/clearweave/references/academic-grammar.md#cw42) |
| **CW43** Sample-grounded academic voice | `host` | [references/author-voice.md](skills/clearweave/references/author-voice.md#cw43) |
| **CW44** Corpus profile measurements | `script+host` | [references/author-voice.md](skills/clearweave/references/author-voice.md#cw44) |
| **CW45** Approved-revision preference learning | `script+host` | [references/author-voice.md](skills/clearweave/references/author-voice.md#cw45) |
| **CW46** Manuscript and editorial lanes | `host` | [references/anti-defensive.md](skills/clearweave/references/anti-defensive.md#cw46) |
| **CW47** Located scholarly candidates | `script` | [references/scholarly-tools.md](skills/clearweave/references/scholarly-tools.md#cw47) |
| **CW48** Provenance-separated scholarly evaluation | `workflow+script` | [references/scholarly-tools.md](skills/clearweave/references/scholarly-tools.md#cw48) |
| **CW49** Whitelist finished-draft mode | `host` | [references/lieflat.md](skills/clearweave/references/lieflat.md#cw49) |
| **CW50** Eleven localized Chinese patterns | `host+candidate` | [references/lieflat.md](skills/clearweave/references/lieflat.md#cw50) |
| **CW51** Five scoped translationese patterns | `host+candidate` | [references/lieflat.md](skills/clearweave/references/lieflat.md#cw51) |
| **CW52** Element-normalized corpus measurement | `script` | [references/lieflat.md](skills/clearweave/references/lieflat.md#cw52) |
| **CW53** Rule-linked minimal-edit ledger | `script+host` | [references/lieflat.md](skills/clearweave/references/lieflat.md#cw53) |
| **CW54** Candidate review and style exceptions | `host+script` | [references/lieflat.md](skills/clearweave/references/lieflat.md#cw54) |
| **CW55** Academic drafting and scoped cleanup | `host+literal+candidate` | [references/academic-humanizer.md](skills/clearweave/references/academic-humanizer.md#cw55) |
<!-- capabilities:end -->

</details>

## Sources and tests

Routine GitHub CI runs the offline unit suite and package checks on main pushes and pull requests. Superseded runs are cancelled; branch pushes do not duplicate PR checks. Release publishing and network-based source collection/replays are manual workflows. Routine CI and release CI both run `python3 tools/validate_repo.py --release`, so commit `docs/releases/v<VERSION>.md` with any version change. When changing generated capability documentation, update its source and run `python3 tools/render_catalog.py --write`, committing the generated files with that change.

The 0.5.0 [Academic Humanizer validation record](docs/evaluation-academic-humanizer.md) reports 411 passing local unit tests and a fresh-context four-case paired trial. Both versions met the scoped requests; all four comparisons tied.

The integration registry covers **48 sources, 278 adoption/adaptation decisions, 55 capabilities, 44 conflict families and 88 authored bilingual conflict cases**. This release adds the academic language protocol and LaTeX cross-reference protection. Authored cases document expected behavior; they do not establish writing quality or semantic guarantees.

[Documentation index](docs/README.md) · [Lieflat integration](docs/lieflat-integration.md) · [Precision tests](docs/evaluation-lieflat.md) · [Source decisions](docs/sources.md) · [Capability atlas](docs/capabilities.md) · [Scholarly integration](docs/scholarly-integration.md) · [Public-paper evaluation](docs/evaluation-scholarly.md) · [Raw records](evals/scholarly-2026-10-20/)

## License

Original code and instructions use [MIT](LICENSE). Method attribution is recorded in [NOTICE](NOTICE.md). Sample texts retain their source licenses: ACL examples use CC BY 4.0; HC3 examples use CC BY-SA 4.0.
