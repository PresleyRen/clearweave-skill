# ClearWeave · Scholarly

**English–Chinese natural prose, direct research writing, academic voice and precise finished-draft cleanup.**

[简体中文](README.zh-CN.md) · [Skill](skills/clearweave/SKILL.md) · [Capability index](docs/capabilities.md) · [Published-paper examples](docs/scholarly-examples.md)

ClearWeave edits papers, technical documents, READMEs, work emails and everyday writing. It removes stock phrasing and repetition, brings the contribution into focus, corrects academic grammar, and builds reusable style profiles from selected samples. Choose the language of the finished text and editorial notes separately.

## Capabilities

| Module | What it does | Typical output |
| --- | --- | --- |
| **Lieflat precision cleanup** | Eleven Chinese pattern families, minimal rule-linked edits and fixed document structure. | Finished draft with unmatched text preserved |
| **Corpus and edit-ledger checks** | Candidate locations, comparable denominators, corpus comparisons and exact edit reconstruction. | Measurements and edit verification |
| **Natural bilingual prose** | Revises empty openings, mechanical paragraphs, repeated conclusions, over-explanation, translation-shaped Chinese and nominalized English. | Clear revised prose |
| **Anti-defensive editing** | Separates empty apologies and pre-emptive defenses from meaningful qualifications; states claims, evidence and comparison conditions directly. | Focused abstracts, introductions and conclusions |
| **Academic grammar** | Selects tense by sentence function; checks agreement, articles, number, pronouns, modifiers, parallelism and information flow. | Grammar edits with reasons |
| **Argument and section structure** | Connects questions, methods, evidence and contributions; synthesizes related work and distinguishes planned from completed research. | Reverse outlines and section drafts |
| **Sample-grounded voice** | Extracts syntax, register, structure and terminology habits from selected papers or personal samples, scoped by language, discipline and section. | Author, house or field profiles |
| **Revision-based preferences** | Compares an initial draft with an approved final version and records scoped preference proposals. | Evidence-linked edit records |
| **Meaning and terminology checks** | Reviews quantities, units, negation, conditions, evidence strength, comparison groups and work status; preserves quotes, citations, equations and code. | Differences and review locations |
| **Critique and responses** | Identifies argument gaps and inconsistencies, organizes point-by-point responses, and checks manuscript excerpts. | Reviews, response letters and clean drafts |
| **Translation, drafting and shortening** | Writes from supplied material, adapts language and locale, and consolidates repetition. | Target-language prose |
| **Long documents and maintenance** | Maintains terminology and claim ledgers, handles selected files and locates rules, sources, conflicts and tests. | Per-file results and extension routes |

**New in 0.4.0:** LF01–LF11 Chinese precision cleanup, fixed-structure edit ledgers, element-normalized corpus measurement and style-specific exceptions (CW49–CW54).

## Function map

```text
Draft / paper / notes / designated samples + current request
                           |
                 Language / genre / section / scope / style guide
                           |
                 Facts / quantities / conditions / citations / terms
                           |
              +------------+-----------------------+
              |                                    |
       Full editing path                   Lieflat precision cleanup
       Polish / rewrite / translate        Lock structure and unmatched text
       Natural EN + ZH prose                        |
       Direct research writing             LF01–LF11 Chinese patterns
       Academic grammar                    Contrast / enumeration / sentence shape
       Argument / sampled author voice     Punctuation / heading ordinals
       Approved-revision preferences       Analogy / existing detail / openers
              |                            Five translation structures / reference
              |                                    |
              |                            Genre + author-style review
              |                            Rule → original span → minimal edit
              +------------+-----------------------+
                           |
       Literal differences / risk cues / semantic review
       Scholar: academic style; tone: candidates, corpus counts, edit ledger
                           |
              Revised text / diagnosis / response / style profile
Diagnosis-only requests leave the draft unchanged on either path.

Extend: issue → CW capability → LF rule / CF conflict → file → counterexamples → real-text test
```

## Install and use

```bash
git clone --branch v0.4.0 https://github.com/PresleyRen/clearweave-skill.git
cd clearweave-skill
python3 tools/install_skill.py --project /absolute/path/to/your-project
```

The project installation is `.agents/skills/clearweave`. Back up customizations before replacing an existing installation. Python helpers use the Python 3.10+ standard library.

```text
$clearweave
Edit this paper paragraph for natural academic English. Remove empty defensive
framing and check agreement, tense, articles and modifiers. Keep numbers,
citations, terminology and evidence strength. Explain consequential edits in Chinese.
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

The full editor remains available for English, academic grammar, drafting and restructuring. See the [integration map](docs/lieflat-integration.md), [rule reference](skills/clearweave/references/lieflat.md) and [real-text records](docs/evaluation-lieflat.md).

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
<summary>All 48 capabilities and their rule locations</summary>

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
<!-- capabilities:end -->

</details>

## Sources and tests

The integration registry covers **46 sources, 262 adoption/adaptation decisions, 54 capabilities, 42 conflict families and 84 bilingual conflict fixtures**. This release adds lieflat precision cleanup, corpus measurement and edit-ledger verification.

[Lieflat integration](docs/lieflat-integration.md) · [Precision tests](docs/evaluation-lieflat.md) · [Source decisions](docs/sources.md) · [Capability atlas](docs/capabilities.md) · [Integration guide](docs/scholarly-integration.md) · [Public-paper evaluation](docs/evaluation-scholarly.md) · [Raw records](evals/scholarly-2026-10-20/)

## License

Original code and instructions use [MIT](LICENSE). Method attribution is recorded in [NOTICE](NOTICE.md). Sample texts retain their source licenses: ACL examples use CC BY 4.0; HC3 examples use CC BY-SA 4.0.
