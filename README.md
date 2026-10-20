# ClearWeave

**Natural English and Chinese, with meaning kept in view.**

[简体中文](README.zh-CN.md) · [Skill](skills/clearweave/SKILL.md) · [32-source audit](docs/sources.md) · [Evaluation report](docs/evaluation.md)

ClearWeave is one bilingual agent skill for removing formulaic prose, empty framing, and translation-shaped syntax. It combines a shared editing contract with English, Chinese, and academic references. The name joins **clear** expression with **weaving** together complementary methods.

It is an instruction package for an AI assistant, accompanied by an optional local Python checker. The host model performs the writing. The checker does not rewrite text or determine who wrote it.

## What it can do

| Capability | Behaviour |
| --- | --- |
| English, Chinese, and mixed editing | Keep each passage's language unless translation is requested; preserve Chinese script and English spelling conventions. |
| Minimal or structural editing | Default to the smallest useful change; reorganize an argument when requested. Good writing can remain unchanged. |
| Genre-aware expression | Academic/technical, business/formal, news/explanatory, and personal/social routes. Natural does not always mean casual. |
| Meaning preservation | Check claims, quantities, units, negation, scope, conditions, attribution, uncertainty, comparisons, and planned versus completed work. This is a workflow, not a guarantee. |
| Academic editing | Trim empty defensiveness while retaining justified uncertainty, limitations, adverse results, and stable terminology. |
| Translation in either direction | Produce natural target-language prose within the source's factual commitments. |
| Voice from supplied samples | Learn directness, register, rhythm, and formatting without importing sample facts or experiences. |
| Diagnosis and critique | Locate actual writing or argument problems and propose repairs; distinguish established defects from open questions. |
| Drafting from notes | Organize supplied material into prose without inventing results, evidence, or personal history. |
| Optional local checks | Find a limited set of surface-style candidates and compare supported protected literal spans. Python 3.10+; standard library only. |

The instructions do not require network access, a detector service, an API key, or any of the 32 upstream projects. A host may still have its own data handling and tool policies.

## Install

The installable directory is **`skills/clearweave/`**. It follows the [Agent Skills format](https://agentskills.io/specification). Installation and automatic selection depend on the host.

### Codex: project installation

Clone the repository, then copy the skill into the project in which you want to use it:

```bash
git clone https://github.com/PresleyRen/clearweave-skill.git
cd clearweave-skill
python3 tools/install_skill.py --project /absolute/path/to/your-project
```

The installer copies to `<project>/.agents/skills/clearweave` and refuses to overwrite an existing destination. It does not modify global settings or install dependencies. To update an existing installation, review the differences and replace it deliberately.

In Codex CLI or the IDE, invoke `$clearweave`. In a ChatGPT environment that has the skill installed, use its skill selector. See the host's [official skill documentation](https://learn.chatgpt.com/docs/build-skills) for discovery and installation. A public GitHub repository or GitHub Release is not, by itself, a listing in a plugin directory.

Other Agent Skills-compatible hosts may be able to load the folder, but this release does not claim end-to-end validation on every host. The project installer targets the documented Codex repository location.

## Use

```text
$clearweave
Edit this into natural English. Keep the facts, scope, and my voice.
Return only the revised text:
[paste text]
```

```text
$clearweave
给下面这段去 AI 味，保持中文、正式程度和原意，只给正文：
[粘贴原文]
```

For an English paper with Chinese discussion:

```text
$clearweave
润色下面的英文论文段落，正文保留英文。
保留研究条件、局限、数值、引用和证据强度。修改说明用中文：
[paste paragraph]
```

For other tasks, state the operation directly: “diagnose only,” “translate into Traditional Chinese for Taiwan,” “match these samples,” “draft from these notes,” or “review the argument rigorously.” Do not rely on an undocumented slash-command parser; these are natural-language instructions.

## Local checker

Run from the repository root:

```bash
python3 skills/clearweave/scripts/clearweave_check.py lint draft.md --format json
python3 skills/clearweave/scripts/clearweave_check.py compare original.md revised.md --format json
```

`lint` reports located candidates for review. It skips supported protected regions and has no blanket ban on passive voice, technical vocabulary, three-item lists, or em dashes. A clean report does not mean perfect writing.

`compare` reports added or missing supported literal spans. It can catch some changed numbers, units, quotations, links, citations, code, and formulas. It compares occurrences, not the full meaning: swapping who owns two unchanged numbers or changing a negation can escape it. It always says that semantic review is required. A legitimate requested translation or reference reformat may also produce differences.

See [checker documentation](skills/clearweave/references/tooling.md) for syntax coverage, custom protected spans, stdin, JSON fields, and exit codes. Neither command changes the input files.

## How the synthesis resolves conflicts

We inspected **32 implementations from the earlier inventory: 28 directly relevant skills and 4 auxiliary writing skills**. This is not a count of every such skill online, and forks are not independent evidence.

| Advice that conflicts across sources | ClearWeave rule |
| --- | --- |
| Delete all caveats / retain every caveat | Keep qualifications that change interpretation; remove empty or duplicated apology. |
| Ban punctuation, words, passive voice, or triads | Inspect the function in context; retain appropriate technical and grammatical forms. |
| Add personality and lived detail | Preserve the author's supplied voice and experiences; do not fabricate them. |
| Optimize sentence-length variation or detector scores | Improve readability and fidelity; no entropy targets, authorship probability, or detector-chasing loop. |
| Tell the strongest possible research story | Keep material adverse findings and the original evaluation criteria. |
| Rewrite until everything changes | One edit and at most one targeted repair; preserve good text and roll back known drift. |

Every source has an adoption/rejection entry and a destination module in the [full audit](docs/source-audit.json). The audit records mutable main-branch observations, provenance, and license uncertainty. We did not concatenate the source prompts or reproduce their claimed detector performance.

## Validation and evidence

The [evaluation report](docs/evaluation.md) contains the actual results, original outputs, identified limitations, and any repairs. The [protocol](evals/PROTOCOL.md) explains the fresh-context plain-versus-skill comparison and the separate anonymous model review.

In the initial 18-case comparison, the editor recorded fidelity in 18/18 ClearWeave responses and 17/18 ordinary responses, with one preference for each condition and 16 ties. A generic product-introduction rule was then clarified; four new targeted cases retained fidelity and task compliance. This small comparison does not establish broad superiority over ordinary prompting. Original responses and the pre-refinement instruction snapshot are retained.

Re-run deterministic checks:

```bash
python3 -m unittest discover -s tests -v
python3 tools/validate_repo.py
```

The writing evaluation uses original synthetic requests, one response per case and condition, and a single host model family. Its readability judgements are made by a model, not a blinded panel of human editors. It demonstrates observed behaviour on these cases; it does not establish universal superiority, a detector pass rate, or unchanged meaning on arbitrary documents.

## Limits

- This release does not include an AI-authorship classifier, GPTZero/Turnitin integration, or promised “human” score.
- It does not verify citations or factual truth during a normal style edit. Explicit fact-checking requires suitable evidence and the host's tools.
- The checker is a conservative regex-based helper, not a complete Markdown, LaTeX, citation, unit, or semantic parser.
- The skill depends on the host model's language and reasoning ability. Automatic skill selection and all third-party clients have not been validated end to end.
- Plain text and Markdown are the native deliverables. Preserving DOCX/PDF/slide formatting requires a separate document workflow; this repository does not implement one.
- Long manuscripts, specialist terminology, legal or medical accuracy, and subtle changes of implication still need domain-aware review.
- English and Chinese are the designed languages. Other languages are outside this release's stated scope.

## Project layout

| Path | Purpose |
| --- | --- |
| `skills/clearweave/SKILL.md` | Shared routing, editing contract, modes, and stopping rules |
| `skills/clearweave/references/` | English, Chinese, academic, preservation, conflict, and checker guidance |
| `skills/clearweave/scripts/` | Optional local Python checker |
| `docs/` | Source decisions and actual evaluation results |
| `evals/` | Requests, rubric, raw outputs, and review evidence |
| `tests/` | Deterministic regression tests |
| `tools/` | Project installer, validation, and review preparation |

## License and attribution

Original ClearWeave contributions are offered under [MIT](LICENSE). [NOTICE](NOTICE.md) retains source attribution and clarifies scope, including Lorena A. Barba's CC BY 4.0 *sciwrite*. Upstream projects retain their own licenses; an observed MIT label is not a full rights audit. No source author is represented as endorsing this project.
