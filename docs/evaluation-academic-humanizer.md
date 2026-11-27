# Academic Humanizer integration validation

[简体中文](evaluation-academic-humanizer.zh-CN.md) · [Documentation index](README.md)

Date: 2026-11-27. Runtime: ClearWeave **0.5.0**. The upgrade adds an English academic Draft / Polish / Cleanup route, source-specific companion selection, and literal protection for common LaTeX labels and cross-references. The source registry and authored conflict fixtures describe the intended behavior; the separate trials below record actual model outputs.

## Local checks

The complete unit suite passed **411 tests** on Python 3.12.14. Package/source validation, generated-document validation and the official skill structure validator passed. The existing scholarly and lieflat replay commands also passed against their own historical runtime snapshots; they were not relabeled as new 0.5.0 model trials.

The reader tests cover the two upstream projects sharing the name `academic-humanizer`, wrong-fork rejection, offline behavior, fixed upstream URLs and an independently hashed `examples` resource. Exact offline reads of the three real pinned files succeeded; deliberately swapping the two local sources failed. The checker tests cover labels and cross-reference keys without numbers, supported starred forms, protected outer regions and ordinary lookalikes.

These are local results. CI for a published commit is reported separately in [GitHub Actions](https://github.com/PresleyRen/clearweave-skill/actions/workflows/validate.yml).

## Fresh-context paired trial

Two agents started with no inherited conversation history. Each processed the same four synthetic requests in one batch, using either the existing `f25ac2e036616689e322d9eb857ccb1b287afe50` runtime or the upgraded local runtime. Both were asked to work offline. They received the ordinary requests and their designated skill, without expected answers, the review rubric or the other condition's outputs. The outputs were retained without maintainer editing.

A third fresh-context reviewer received only the requests, original material, rubric and alternated A/B outputs. It did not receive the condition mapping or either skill. All four comparisons were ties, and the reviewer found no fidelity or scope violation in either condition.

| Case | Request | Observed upgraded behavior |
| --- | --- | --- |
| AH01 | Draft English Results from Chinese experiment notes | Retained both methods' error counts and median latencies, the offline English setting, and the untested outcomes; added no significance claim. |
| AH02 | Minimal cleanup of final LaTeX prose | Removed one empty opener and capitalized the next word. All remaining wording, headings, paragraph breaks, mean latency, seed, tolerances, retries, labels and references stayed exact. |
| AH03 | Polish already clear academic text | Returned the original text unchanged. |
| AH04 | Correct subject–verb agreement only | Changed `suggests` to `suggest` and retained every other word. |

The three existing-text cases in both conditions also matched their scoped expected text exactly and had no protected-literal differences. The risk helper raised one candidate for the legitimate `suggests` → `suggest` inflection in each condition; manual review resolved it as the requested agreement correction. That candidate remains in the raw record rather than being silently counted as a semantic error or suppressed.

## Evidence and limits

[Raw record](../evals/academic-humanizer-2026-11-27/manifest.json) · [requests](../evals/academic-humanizer-2026-11-27/requests.json) · [rubric](../evals/academic-humanizer-2026-11-27/rubric.json) · [existing outputs](../evals/academic-humanizer-2026-11-27/outputs-baseline.json) · [upgraded outputs](../evals/academic-humanizer-2026-11-27/outputs-upgraded.json) · [blind review](../evals/academic-humanizer-2026-11-27/blind-review-results.json) · [mechanical checks](../evals/academic-humanizer-2026-11-27/mechanical-checks.json).

Reported read-file manifests preserve the exact instruction hashes. The parent environment identified itself as GPT-6 Astra Pro; the inherited child snapshot and sampling controls were not exposed or pinned. Cases within each condition shared a context. This is a small targeted regression with model-based review, not independent human evaluation, a long-document benchmark, native automatic skill-trigger testing or evidence of general quality improvement. The offline trials did not exercise live external-companion guidance. No detector or acceptance outcome was measured.
