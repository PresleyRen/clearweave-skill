# Diagnose a failure and extend the right module

<a id="cw31"></a>
<a id="cw32"></a>
<a id="cw34"></a>

## Trace the symptom

The machine-readable catalog is `assets/capabilities.json`. Each `CWxx` identifier
points to a runtime module, inspiration sources and repository regression cases.
Each `CFxx` identifier names a conflict with English and Chinese examples. IDs are
stable across releases; do not recycle an ID for an unrelated behavior.

Run from the installed skill directory:

```bash
python scripts/clearweave_trace.py --id CW05
python scripts/clearweave_trace.py --query "否定被删掉"
python scripts/clearweave_trace.py --id CF17 --format json
```

This is a local index lookup, not an automatic root-cause diagnosis. Keyword matches
can be incomplete. A valid unknown ID or unmatched query returns no matches instead
of inventing a capability. The installed package contains the catalog and runtime
modules; the complete source audit and test suite live in the repository.

## Extension loop

```text
Observed failure / 用户报告
  -> Smallest original + request + actual revision
  -> CW capability and CF conflict (or explicitly new capability)
  -> Distinguish prompt failure / literal-parser failure / context gap / wrong contract
  -> Locate module + source decision + existing regression case
  -> Add failing example AND a legitimate counterexample
  -> Small scoped change; no universal blacklist from one sample
  -> Run structural checks, parser tests and conflict fixtures
  -> Run a fresh host-model trial for behavioral claims
  -> Record actual outcome, remaining gap, version and changelog
```

A failure report should include the exact request and selected mode, original and
revision (redact private data), required meaning, observed change, affected IDs,
expected behavior, host/version when known, and the smallest reproducing case.
Never fabricate a model version or claim a hidden prompt was captured. Do not store
private manuscripts in public regression tests; create an original synthetic example
with the same failure mechanism.

## Rule admission and conflict precedence

Follow the runtime's instruction hierarchy. Within the authorized editing task,
use this order: factual and attribution integrity; protected material; explicit
current output/genre requirements; relevant approved voice preferences; optional
style heuristics. When a surface instruction conflicts with a quotation, retain
the quotation and flag the conflict separately. Do not use this local order to
replace system or application instructions.

Admit a rule only when its purpose, applicable genres/languages, exceptions and
regression cases are clear. Mark a rule as adopt, adapt, exclude or defer. An upstream
feature that fabricates experiences, hides unfavorable findings or promises detector
success is recorded as excluded, not silently called supported. Shared ancestry is
not independent evidence. Unknown licenses remain unknown; do not vendor upstream
text, examples or code without appropriate rights and attribution.

Do not automatically modify persistent rules from routine edits. Explicitly requested
maintenance may update the relevant module, catalog and tests. Prefer a local scope
condition or exemption to another global ban. Keep clean output and diagnostic
feedback separate.

## Evidence levels

Keep these results separate:

1. **Structural validation:** files, anchors, source-decision hashes and case links
   resolve. This detects missing coverage, not good writing.
2. **Deterministic tool tests:** Python behaves as documented on specified inputs.
   This does not validate host-model rewriting.
3. **Authored conflict fixtures:** known faithful/unsafe pairs exercise explicit
   constraints. They are examples and regression oracles, not independent trials.
4. **Host-model trials:** preserve exact task, input, instruction snapshot, model
   identity when actually available, output and review basis. Blind assessment,
   repeated runs and human reviewers improve evidence; claim only what occurred.

The v0.1.0 repository contains historical paired outputs. A new instruction or helper
version does not inherit their effect size or become tested merely by copying the
report. Re-run new behavior in the target host before claiming comparative improvement.
No test here estimates authorship, removes a watermark or guarantees a detector result.

## Portability and optional tooling

The skill uses a standard `SKILL.md` entry with relative resources. Python helpers
are optional and need Python 3.10+; the basic editing workflow does not require a
server, MCP integration, API key or internet. Host file-editing, independent agents,
fact verification, tracked changes and DOCX/PDF layout depend on tools actually
available in the host. Do not claim those integrations were tested without evidence.
GitHub publication is not marketplace approval or automatic client installation.
