# v0.2.0 validation / 验证记录

Date: **2026-10-20**. This report distinguishes structural coverage, executable tool behavior, authored conflict fixtures, same-session applications, and historical model comparisons. None of them is an AI-authorship or detector benchmark.

## What changed

The v0.1 source audit was retained. The extension adds a 36-capability registry, a crosswalk for all 194 recorded source decisions, 26 named conflicts with English/Chinese scenarios, a local trace command, a read-only revision-risk helper, explicit file/long-document/voice-profile workflows, and generated capability tables in both READMEs.

Explicit Traditional Chinese variants were added to the existing linter phrase families. This is limited phrase recognition, not full locale coverage or script conversion. The original literal checker remains deliberately limited: it does not parse semantic roles or prove fidelity.

## Executed checks

| Layer | Actual observation | What it does not establish |
| --- | --- | --- |
| Baseline | The recovered v0.1 package passed 46 local tests before modification | Broad writing quality |
| Final deterministic suite | **179 tests passed on Python 3.13.5** | 179 independent editing experiments |
| Audit crosswalk | **32 sources; 92 adopted +102 adapted/excluded =194 statements; 36 capabilities; 26 conflicts; 52 authored cases; no structural errors** | An exhaustive inventory of every upstream subfeature or a test of all32 original implementations |
| Documentation | Both README capability tables and the atlas reproduce from the registry | Correct semantic editing |
| Installation smoke | Installed into a temporary project; trace and risk helpers ran from an unrelated working directory | Automatic host discovery or all-client compatibility |
| Same-session applications | 12 original inputs and revisions, with actual helper reports and author review | Independent, blinded, randomized, repeated, or comparative model evidence |

The 179 deterministic tests consist of **46 checker/installer tests, 24 risk tests, 22 trace/coverage tests, 52 authored-fixture tests, 32 source-link tests, and 3 application-record tests**. The fixture and source counts are included in179, not additional experiments.

Raw evidence:
- [Unit-test log](../evals/v0.2.0/unittest.log)
- [Coverage report](../evals/v0.2.0/coverage.json)
- [Environment and instruction-file hashes](../evals/v0.2.0/environment.json)
- [Installed-package smoke](../evals/v0.2.0/installed-smoke.json)
- [12 application inputs, outputs, reviews, and actual helper reports](../evals/v0.2.0/applications.json)
- [52 conflict fixtures](../evals/conflict-cases.json)

## Conflict testing: scope and design

Each CF01–CF26 family has one English and one Chinese original synthetic scenario. Each records a request, input, faithful example, unsafe counterexample, and explicit string constraints. Some scenarios test routing, privacy, diagnosis, or maintenance policy rather than prose rewriting.

All52 faithful fixtures satisfy their declared constraints, and all52 unsafe counterexamples violate at least one. This demonstrates that the **authored examples and their narrow test oracles are consistent**. It does not mean a host model generated those outputs correctly, and it is not52 measured editing wins.

Fault-injection tests deliberately remove or duplicate decisions, alter source text without remapping, mislabel an exclusion as adoption, point to unknown capabilities or anchors, remove a Chinese scenario, break bidirectional links, and make an unsafe example identical to the faithful one. These changes must fail validation. Unknown assertion kinds are rejected rather than silently accepted.

## Actual new applications

The assistant in this conversation authored12 synthetic inputs, applied the current editing guidance to produce revisions, then ran the real local helpers and reviewed its own changes. The API model identifier, sampling controls, and a separate clean-context runner were not available. The record labels this **same-session author-applied demonstration**, not an independent experiment.

Ten cases are editing tasks. All ten retain the literal inventory recognized by the checker. That is not proof of semantic fidelity. The other two deliberately have different contracts: APP09 is diagnosis-only and introduces quoted problem spans; APP10 is translation and changes the literal Chinese quantity `40个` into English `40`. Their two literal changes each were reviewed as expected, not hidden or counted as failures of an unchanged-text contract.

Risk candidates occur in APP06 (approximately→about, one candidate), APP09 (diagnosis rather than a replacement draft, one candidate), and APP10 (translation, four candidates). These are examples of why cue changes are **review prompts rather than verdicts**. The author identified no material meaning or task error in these twelve outputs; that self-review is qualitative and not a calibrated success rate.

### English example: academic scope retained

Before:

> It is important to note that our retrieval controller achieved 81.2% accuracy on 240 English queries. These results may suggest that the controller helps in this offline setting. Multilingual performance has not been evaluated.

After:

> Our retrieval controller achieved 81.2% accuracy on 240 English queries. These results may suggest that the controller helps in this offline setting. Multilingual performance has not been evaluated.

The edit removes an empty introduction, not the uncertainty, denominator, offline condition, or untested population. It makes no new causal or multilingual claim.

### Chinese example: obligations are not style filler

Before:

> 需要强调的是，负责人必须在周五前确认预算，其他成员可以补充意见。未经批准，不得对外发布结果。

After:

> 负责人必须在周五前确认预算，其他成员可以补充意见。未经批准，不得对外发布结果。

The obligation, permission, deadline, and prohibition remain. These are not interchangeable with a more casual or decisive tone.

## Bugs found and addressed

1. Adding explicit Traditional Chinese phrase variants made an old “zero matches” expectation obsolete. The test was renamed and updated to assert the newly supported behavior; it was not deleted.
2. `May 12` was initially flagged as the modal word “may.” Numbers had already been masked, so the exception looked at whitespace rather than the date. The check now uses the original text at the preserved offsets. This is a narrow month/date exemption, not a date parser.
3. The old literal comparator misses swaps between unchanged numeric values and ordinary-prose negation/status changes. The new risk helper surfaces some cue changes and numeric-order changes. **The underlying semantic limitation is not claimed solved.**

Known gaps have explicit tests: a role swap with unchanged numeric order and a negation-scope swap with the same cue inventory can still produce no risk candidate. Legitimate sentence reordering can trigger R08. A faithful “may”→“might” change can trigger a lexical warning. Protected quotations/code are checked separately because the risk helper masks them.

## Historical evidence remains historical

The repository retains the v0.1 comparison of18 paired outputs and4 follow-up regressions, including original outputs, condition mapping, reviews, and the instruction snapshot. In that model review, each condition was preferred once and16 pairs tied; fidelity was recorded for18/18 ClearWeave and17/18 plain outputs. These observations **do not establish broad superiority** and were not rerun as a new v0.2 comparative experiment.

Read the [historical report](evaluation.md). Do not add the old18 pairs, new52 fixtures, and12 author-applied examples together and call the result a single independent accuracy study.

## How to extend the evidence

For a behavioral claim, first save a new request, expected meaning constraints, host/model identifier when actually known, relevant skill version/hash, and a comparison condition. Run the host in separate contexts without showing it a desired answer. Preserve raw outputs, judge anonymously where feasible, add human review, and report failures and ties as well as preferences. Do not tune on a case and relabel it held-out.

The [maintenance workflow](../skills/clearweave/references/maintenance.md) and [capability atlas](capabilities.md) locate the responsible module. This release supplies a stronger regression framework; it does not pretend that the missing independent or long-document evaluations have already happened.
