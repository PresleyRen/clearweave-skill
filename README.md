# ClearWeave

**An English–Chinese writing skill for natural, clear prose that preserves meaning and the author's voice.**

[简体中文](README.zh-CN.md) · [Skill entry point](skills/clearweave/SKILL.md) · [Capability index](docs/capabilities.md) · [Public-corpus examples](docs/evaluation-hc3.md)

ClearWeave edits papers, technical documents, READMEs, work emails, and everyday writing. It addresses stock phrasing, mechanical paragraph structures, repetition, and translation-shaped syntax. It also helps organize arguments, keep terminology consistent, and match a supplied writing style. One skill handles English, Chinese, and mixed text, with separate language choices for the finished text and editorial notes.

## What it does

| Capability | Use |
| --- | --- |
| **Remove stock phrasing and repetition** | Cut empty openings, repeated conclusions, mechanical contrasts, and over-explanation so paragraphs reach their point sooner. |
| **Edit natural Chinese** | Improve translated syntax, long modifiers, and abstract jargon; clarify actors, actions, objects, and results; adapt script and regional vocabulary to the audience. |
| **Polish English** | Improve nominalizations, heavy syntax, references, and sentence connections while keeping spelling conventions consistent. |
| **Edit academic writing** | Focus on the research question, methods, and contribution; remove unnecessary apologies and pre-emptive defenses; align claim strength with evidence. |
| **Preserve meaning** | Check quantities, units, comparison targets, negation, conditions, scope, causality, attribution, and work status against the source. |
| **Protect terminology and references** | Keep technical terms, module names, and variables consistent; preserve quotations, citation keys, equations, code, and designated passages. |
| **Restructure and shorten** | Reorder information by paragraph purpose, combine repetition, and organize material around the central question. |
| **Match the author's voice** | Use supplied samples to learn register, syntax, rhythm, and expression preferences for subsequent edits. |
| **Translate and draft from notes** | Produce idiomatic target-language prose or organize notes, outlines, and source material into a draft. |
| **Critique and prepare responses** | Locate argument gaps, weak support, and inconsistencies; suggest specific repairs and organize point-by-point reviewer responses. |
| **Edit long documents and selected files** | Maintain terminology and claim ledgers across sections; use a file-capable host to edit selected paths and report results for each file. |
| **Inspect revisions and extend rules** | Use Python helpers to locate surface patterns, compare protected content, flag revision risks, and trace issues to rules and tests. |

## Quick start

Load `skills/clearweave/` in an Agent Skills-compatible tool. The project installer requires Python 3.10+ and uses the standard library.

```bash
git clone https://github.com/PresleyRen/clearweave-skill.git
cd clearweave-skill
python3 tools/install_skill.py --project /absolute/path/to/your-project
```

The skill is installed at `<project>/.agents/skills/clearweave`. To upgrade an existing installation, back up customizations before replacing the skill directory.

### Polish an English paper

```text
$clearweave
Edit the following English paper paragraph. Keep the prose in English
and explain consequential changes in Chinese.
Focus on stock phrasing, heavy syntax, and defensive writing.
Preserve terminology, numbers, citations, study conditions, and evidence strength.

[paste text]
```

### Edit Chinese prose

```text
$clearweave
编辑下面这段中文，去掉套话、重复解释和翻译腔。
保持原有正式程度、事实和立场，只输出修改后的正文。

[原文]
```

### Rewrite a README

```text
$clearweave
Rewrite the README for someone seeing the project for the first time.
Focus on features, use cases, installation, and example requests.
Keep the main text about the product and link to the evaluation details.
Retain the capability diagram and extension entry points.
```

## Choose a task and output

Name the task in the request. You can also specify the depth of editing, audience, and delivery format.

| Task | Example request | Output |
| --- | --- | --- |
| Polish | Keep the structure; make the smallest useful edits | Revised prose |
| Restructure | Reorganize around the main question and combine repetition | A restructured article |
| Diagnose | Locate issues, explain their effect, and suggest repairs | Located editorial notes |
| Translate | Use natural academic English; retain terms and citations | Target-language prose |
| Draft from material | Turn these notes into a project overview | A draft based on the supplied material |
| Match voice | Follow the register and sentence style in these samples | A voice-matched revision |
| Critique and respond | Review the argument, experiments, and evidence; prepare replies | Findings, revision suggestions, or a response draft |
| Edit files | Edit the selected files and provide a change summary | Updated files and a summary |

Finished prose, editorial notes, and verification records are separate deliverables. Reader-facing text stays focused on its subject; explanations of edits belong in the accompanying notes.

## Editing workflow

```text
Draft / selected files / notes + user request
                       |
                       v
Set the task: language, genre, audience, scope, output
                       |
                       v
Inventory the information to preserve
Claims · quantities · conditions · terms · citations · author positions
                       |
                       v
Load the relevant guidance
 English -------- Chinese -------- Academic writing
                       |
                       v
Edit by layer
Argument and paragraphs -> sentences -> words -> punctuation
                       |
                       v
Compare and review
Information retained · relationships accurate · voice consistent
                       |
                       v
Deliver prose / editorial notes / revised files
```

Edits address specific reading problems. Useful long sentences, repeated technical terms, and procedural passive constructions can remain. Empty self-evaluation and repetitive framing can go. In papers, study conditions and adverse findings stay with the claims they qualify so readers can interpret the results accurately.

## An editing example

**English draft**

> It is worth noting that the update introduces an export feature. This feature allows users to export reports as CSV files.

**Revision**

> The update lets users export reports as CSV files.

**Chinese draft**

> 值得注意的是，本次更新增加了导出功能。该功能可以帮助用户将报告导出为 CSV 文件。

**Revision**

> 本次更新支持将报告导出为 CSV 文件。

More source texts, revisions, and individual checks are available in the [HC3 public-corpus examples](docs/evaluation-hc3.md) and [application records](evals/v0.2.0/applications.json).

## Local checks

The host model performs the writing. Read-only Python helpers locate expression patterns, compare literal content, and flag risk cues for passage-by-passage review. Run these commands from the repository root:

```bash
# Locate English and Chinese surface patterns
python3 skills/clearweave/scripts/clearweave_check.py lint draft.md --language both --format json

# Compare protected numbers, citations, code, and other literals
python3 skills/clearweave/scripts/clearweave_check.py compare original.md revised.md --format json

# Flag changes in negation, modality, work status, and numeric order
python3 skills/clearweave/scripts/clearweave_risk.py original.md revised.md --format json
```

See the [tool reference](skills/clearweave/references/tooling.md) for parameters and output interpretation.

## Modules and extension

```text
skills/clearweave/
├── SKILL.md                    Task entry point and editing workflow
├── references/
│   ├── preservation.md         Meaning, quantities, relationships, references
│   ├── english.md              English expression
│   ├── chinese.md              Chinese expression and regional vocabulary
│   ├── academic.md             Papers, evidence, critique, responses
│   ├── workflows.md            Voice, long documents, files, deliverables
│   ├── conflicts.md            Conflicting-rule decisions
│   ├── tooling.md              Helper usage
│   └── maintenance.md          New rules and regression tests
├── scripts/                    Surface checks, risk cues, capability lookup
└── assets/capabilities.json     Capability IDs, rule locations, test links
```

### Find the right module

| Area to improve | Entry point |
| --- | --- |
| Quantities, negation, conditions, or claim strength | `preservation.md`, CW03–08 |
| English syntax, paragraph flow, and rhythm | `english.md`, CW10–11, CW14 |
| Chinese syntax, script, and regional usage | `chinese.md`, CW02, CW12 |
| Academic expression, evidence, and critique | `academic.md`, CW13, CW17–20, CW35 |
| Voice, long-document continuity, and file delivery | `workflows.md`, CW15, CW22, CW24–27, CW33, CW36 |
| Checkers and maintenance indexes | `scripts/`, `maintenance.md`, CW28–32, CW34 |

```bash
# Locate a symptom, capability, or conflict
python3 skills/clearweave/scripts/clearweave_trace.py --query "negation removed"
python3 skills/clearweave/scripts/clearweave_trace.py --id CW06
python3 skills/clearweave/scripts/clearweave_trace.py --id CF17

# Inspect the synthesis decisions for a source
python3 tools/coverage.py --source S01
```

For a revision that turns “may” into certainty, follow **CW06 → preservation.md / academic.md → CF01 / CF15** to the relevant guidance and cases. Save the source and problematic revision, add a faithful alternative and a drifting counterexample, then adjust the relevant rule.

```text
Example -> capability ID -> rule file -> conflict case
        -> rule change -> regression checks -> updated index
```

<details>
<summary>Browse all 36 capabilities and rule locations</summary>

In the index, `host` denotes model execution, `script` a Python tool, `literal` string comparison, `candidate` risk cues, `workflow` a procedure, and `package` the skill's folder structure.

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
<!-- capabilities:end -->

</details>

### Validate and update the documentation

```bash
python3 -m unittest discover -s tests -v
python3 tools/validate_repo.py
python3 tools/coverage.py --format json
python3 tools/render_catalog.py --write
```

The capability registry links sources, rules, and test scenarios. The generator synchronizes the capability indexes in both READMEs and the [atlas](docs/capabilities.md). See the [extension guide](skills/clearweave/references/maintenance.md) for the maintenance workflow.

## Method sources and test records

ClearWeave draws on 32 writing skills, combining bilingual editing, clear expression, anti-defensive academic writing, author voice, and preservation checks in a shared workflow. The [source notes](docs/sources.md) and [decision map](docs/feature-map.json) record what was adopted and how conflicting advice was resolved.

| Record | Contents |
| --- | --- |
| [Regression and installation checks](docs/evaluation-v0.2.0.md) | 179 tests covering checkers, command-line tools, installation, capability lookup, and fixture constraints. |
| [Bilingual conflict cases](evals/conflict-cases.json) | 26 conflict families and 52 English/Chinese scenarios with faithful examples and drifting counterexamples. |
| [HC3 public-corpus applications](docs/evaluation-hc3.md) | Sampling method, original answers, revisions, repair history, and individual check results. |

## License

Original code and instructions are [MIT licensed](LICENSE). Source attribution and related license notices are in [NOTICE](NOTICE.md).
