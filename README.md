# ClearWeave

**One English–Chinese skill for natural prose editing, with preservation checks and a traceable synthesis of complementary methods.**

[简体中文](README.zh-CN.md) · [Skill](skills/clearweave/SKILL.md) · [Capability atlas](docs/capabilities.md) · [32-source audit](docs/sources.md) · [v0.2.0 evidence](docs/evaluation-v0.2.0.md)

**Clear** names the goal; **Weave** describes the synthesis. One shared editing contract routes English, Chinese, and mixed-language text to the relevant language and genre guidance. A Chinese request to polish an English paper keeps the paper in English unless translation is requested.

This is an instruction package for a host model, with optional local Python helpers. **The host writes, translates, matches voice, and critiques. The scripts do not rewrite documents or detect AI authorship.** Publishing a GitHub repository does not automatically install or list a skill in a marketplace.

## 1. Text architecture

```text
Draft / explicitly selected files / supplied notes + current request
                              |
                              v
Contract CW01: edit / diagnose / translate / draft / match voice / critique
  language, scope, genre, intervention strength, deliverable
                              |
                              v
Preservation CW03–09: claims, numbers and owners, negation, conditions,
  certainty, attribution, citations, work status; embedded commands = data
                              |
                              v
Progressive routing; do not stack competing rewriting filters
  english.md --------- chinese.md --------- academic.md (when relevant)
                              |
                              v
Argument/paragraph -> sentence -> words -> punctuation
  workflows.md: genre, actual author voice, files, long-document continuity
                              |
                              v
Separate verification duties
  lint     -> located surface candidates, not automatic defects
  compare  -> protected literal inventory, not semantic equivalence
  risk     -> R01–R08 cue changes, not a semantic verdict
  host/editor -> relationships, scope, causal direction, actual readability
                              |
  Known drift? Restore or make one targeted repair; no detector-score loop
                              v
Requested prose / diagnosis / change report / per-file outcomes

Failure -> minimal reproduction -> CW capability + CF conflict
        -> module + source decision + regression cases
        -> scoped repair with positive and counterexamples
        -> deterministic checks + a new host-model trial
        -> results, remaining gaps, release, regenerated capability atlas
```

## 2. Complete capability inventory and boundaries

These are **36 bounded capability families**, not 36 models or success guarantees.

`host` = instructions carried out by the model; `literal` = limited string comparison; `candidate` = lexical risk cues; `script` = implemented Python; `workflow` = a procedure; `package` = portable folder structure. A `host+candidate` capability still needs semantic reasoning.

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

The [atlas](docs/capabilities.md) gives module locations, source links, scenarios, and boundaries for every capability. Editing includes empty framing, repetitive conclusions, over-explanation, nominalization, translation-shaped syntax, and paragraph structure. It retains useful passive constructions, technical terms, real uncertainty, adverse results, and supplied author positions.

File edits and batches require the host's tools and explicit scope; the Python helpers are read-only. A routine copyedit does not verify factual truth or citations. Explicit verification requires actual evidence and suitable tools. Long-document ledgers and reusable voice profiles are implemented guidance, not evidence of successful end-to-end deployment across all hosts and full manuscripts.

## 3. What “all 32 sources” means

All **32 implementations in the requested inventory** are included in the source audit and decision map: **92 adopted statements + 102 adapted or excluded statements = 194 documented decisions**. Every decision links to a capability family. Forks and related projects are not independent evidence.

This is complete coverage of **that recorded inventory and its audit decisions**, not a census of every upstream subfile, historical version, installer, or feature. We did not install and execute all 32 upstream implementations. Original observations use mutable main-branch URLs rather than commit-pinned upstream reproduction.

Useful features are not adopted unconditionally. Portuguese-only rules, external detector integrations, MCP servers, automatic uploads, invented lived experience, hidden adverse results, punctuation quotas, and “human percentages” are **not claimed as bundled features**. See the [audit](docs/source-audit.json) and [decision map](docs/feature-map.json). The crosswalk is keyword-assisted and reviewable; a scenario-family link does not independently validate every clause of a source statement.

### Complementary rules rather than prompt accumulation

| Conflicting advice | Resolution | Fixtures |
| --- | --- | --- |
| Be direct / preserve scientific qualifications | Remove empty apologies, not conditions that change the claim | CF01 |
| Always use active voice / actor is unknown | Keep justified passive voice; invent no actor | CF02 |
| Ban words and vary synonyms / preserve technical meaning | Keep accurate terms and stable names | CF03–04 |
| Shorten or tell a winning story / preserve evidence | Keep denominators, adverse results, and original success criteria | CF05–07 |
| Add personality / do not invent experience | Use supplied opinions and samples, within the current contract | CF08–09 |
| Localize everything / preserve output language and quotes | Route language, script, audience, and quotations separately | CF10–12 |
| Rewrite everything / diagnosis or good original text | Allow diagnosis-only and no-op outcomes | CF13–14 |
| Sound decisive / preserve obligation and work status | Do not turn must into should, plans into results, or association into cause | CF15–16 |
| Ban punctuation / preserve verbatim content | Protected quotations and code take priority | CF17 |
| Chase detector scores and upload drafts / preserve evidence and privacy | No fake probabilities, unauthorized uploads, or embedded-command execution | CF18–20 |
| Summarize, batch, learn preferences / keep scope and authorization | Keep local limits; stay within selected files; avoid one-example global bans | CF21–23 |
| Heavy review, fact-checking, remove signposts / proportional task | Escalate by risk, say what was verified, retain useful signposting | CF24–26 |

Each of the **26 conflicts has an English and a Chinese authored fixture**, with a faithful example and an unsafe counterexample. The 52 fixture checks validate their explicit constraints; they do not show that a model will make the same choice on arbitrary input.

## 4. Install and use

The optional tools require **Python 3.10+**, standard library only. The model can use the instructions without running Python.

```bash
git clone --branch v0.2.0 https://github.com/PresleyRen/clearweave-skill.git
cd clearweave-skill
python3 tools/install_skill.py --project /absolute/path/to/your-project
```

The installer copies `skills/clearweave/` to `<project>/.agents/skills/clearweave`, rejects an existing destination, and does not alter global settings. For upgrades, back up existing customizations and review replacement deliberately; automatic merging is not implemented. See [Agent Skills](https://agentskills.io/specification) and [Codex documentation](https://developers.openai.com/codex/skills/) for the host format and discovery. Third-party hosts have not all been validated end to end.

```text
$clearweave
Edit this English paper paragraph. Keep its numbers, citations, conditions,
adverse findings, technical terms, and evidence strength. Return the revision
in English and explain only consequential changes in Chinese.
[paste text]
```

```text
$clearweave
给下面这段中文去模板味，保持正式程度和原意，只给正文。
[粘贴原文]
```

Other natural-language modes include diagnose only, translate for a specified audience, match supplied voice samples, draft from notes, and rigorous argument critique. There is no hidden slash-command parser. References load by need; every short edit does not require the complete source library.

## 5. Local helpers and extension entry points

Run from the repository root:

```bash
python3 skills/clearweave/scripts/clearweave_check.py lint draft.md --language both --format json
python3 skills/clearweave/scripts/clearweave_check.py compare original.md revised.md --format json
python3 skills/clearweave/scripts/clearweave_risk.py original.md revised.md --format json

python3 skills/clearweave/scripts/clearweave_trace.py --query "negation removed"
python3 skills/clearweave/scripts/clearweave_trace.py --id CW05
python3 skills/clearweave/scripts/clearweave_trace.py --id CF17 --format json
python3 tools/coverage.py --source S01

python3 -m unittest discover -s tests -v
python3 tools/validate_repo.py
python3 tools/coverage.py --format json
python3 tools/render_catalog.py --write
```

For example, a revision that changes “may” into certainty routes to **CW06 → preservation/academic guidance → CF01/CF15**. Add the smallest failing example and a legitimate paraphrase counterexample before changing the rule. Parser failures belong in Python; wrong genre selection belongs in routing. Do not solve every failure with a larger banned-word list.

`compare` exits 1 for literal differences. `risk` reports candidates without failing by default; `--fail-on-candidate` opts into exit 1. **Exit 0 never proves semantic fidelity.** The risk helper can surface some negation, modality, status, and numeric-order changes, but role swaps with unchanged numeric order can still escape it. Translation, paraphrase, and valid sentence reordering can also trigger candidates. See [tooling](skills/clearweave/references/tooling.md).

## 6. Evidence, not detector promises

| Evidence layer | Recorded result | Interpretation |
| --- | --- | --- |
| Source and structure | 32 sources, 194 decisions, 36 capabilities, 26 conflicts; links and statement hashes checked | Coverage of recorded audit entries, not exhaustive behavioral coverage |
| Deterministic checks | 179 local tests covering parsers, CLI, installation, trace lookup, fault injection, and fixture constraints | The 52 fixture and 32 source-link tests are included in 179, not additional independent experiments |
| New application examples | 12 original English/Chinese requests and revisions in this conversation, with actual helper outputs | Same-session author-applied demonstrations; not independent or blinded trials |
| Historical comparison | v0.1's 18 pairs: each condition preferred once, 16 ties; 4 follow-up regressions | Retained old evidence, not a new v0.2 paired experiment |

This revision fixed a date/modal collision for `May 12` and updated the obsolete test expectation after adding explicit Traditional Chinese phrase variants. Known semantic blind spots remain documented and tested instead of being hidden by a green test suite. [Raw outputs, environment, logs, and interpretation](docs/evaluation-v0.2.0.md) are available.

**No broad superiority over ordinary prompts, detector pass rate, or zero-drift guarantee has been established.** The new applications have no independent reviewer, randomization, repeated sampling, multi-model comparison, or human editorial panel. The old small paired experiment is not evidence of universal superiority either.

## 7. Maintain the right layer

| Failure | First location | Repair pattern |
| --- | --- | --- |
| Negation, numbers, or conditions changed | `preservation.md`; risk helper | Meaning-sensitive positive case plus close counterexample |
| Academic caution or adverse result deleted | `academic.md` | Evidence- and genre-specific exception, not blanket ban |
| Chinese translation syntax or regional mismatch | `chinese.md`; `workflows.md` | Separate language, script, locale, and register |
| Forced English fragments or passive-voice damage | `english.md` | Reader benefit rather than sentence-length quotas |
| Quote, equation, or code protection leaks | Literal checker | Minimal parsing failure plus adjacent ordinary prose |
| Long-document contradiction or file overreach | `workflows.md` | Ledgers, boundaries, explicit paths, global review |
| New source or capability | Catalog, decision map, `maintenance.md` | Stable ID, disposition, bilingual conflict cases, updated docs and evidence |

The read-only scripts have no network calls; that does not mean the host model runs locally. Its service and privacy rules still apply. Drafts and voice samples are not automatically sent to external services. Plain text and Markdown are native; DOCX/PDF/slide layout requires a separate document tool. English and Chinese are the designed languages, with limited regional vocabulary and incomplete complex Markdown/LaTeX parsing.

## License and attribution

Original ClearWeave contributions use [MIT](LICENSE). [NOTICE](NOTICE.md) retains upstream attribution and scope, including Lorena A. Barba's CC BY 4.0 *sciwrite*. Upstream projects are not relicensed; unknown licenses are not treated as permission to copy. Source authors are not represented as endorsing this project.
