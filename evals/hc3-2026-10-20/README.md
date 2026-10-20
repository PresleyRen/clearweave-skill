# HC3 application evidence / 公开语料应用记录

See [the report](../../docs/evaluation-hc3.md). Runtime v0.2.0 was frozen. These are same-assistant edits and self-review, not an official-test-split benchmark or independent A/B result.

- `manifest.json`: pinned dataset files and hashes; runtime hashes.
- `cases.json`: fixed sample positions, source labels and per-answer hashes.
- `edits.json`: recorded revisions; null means retain the original for the stated no-op/hold/exclusion. The one repaired case retains its initial draft.
- `protocol.json`: actual method and limits.
- `samples.json` and `checks.json`: reconstruct using `python3 tools/evaluate_hc3.py --download`. Not bundled in Git; the CI artifact contains them.

Original excerpts and adapted text remain CC BY-SA 4.0, subject to stricter upstream-source terms, attributed to the HC3 authors/Hello-SimpleAI; see the report. The repository MIT license does not relicense these texts. The replay code is MIT. No external model or detector is invoked by the replay.
