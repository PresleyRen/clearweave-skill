# Attribution and licensing scope

ClearWeave contains newly written instructions, code, and examples. The MIT license applies to these original contributions. It does not relicense any upstream repository, Wikipedia material, or other source. Source repositories are not vendored, installed, or required at runtime.

The [32-entry audit](docs/source-audit.json) and [source index](docs/sources.md) identify each inspected project, its URL, relationships where observed, what was adopted at the level of editing principles, what was changed or rejected, and the observed license status. Some license entries are unknown; a README or frontmatter MIT label is not represented as a full rights review. Upstream claims about model detection or rewriting quality were not independently reproduced.

## Lorena A. Barba — sciwrite

The academic editing reference draws on principles described in [Lorena A. Barba's sciwrite / manuscript-writing-review](https://github.com/labarba/sciwrite/blob/main/SKILL.md), Copyright (c) Lorena A. Barba, made available under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). The inspected [license notice](https://github.com/labarba/sciwrite/blob/main/LICENSE) identifies that license.

Changes for ClearWeave: the instructions were rewritten, combined with additional evidence and scope constraints, routed by task, and supplied with new teaching examples. Original source examples were not reused. Retain this attribution and the source and license links with the academic reference. Nothing here restricts rights granted by the source license, and no endorsement by the author is implied.

## Other provenance

Several reviewed humanizer projects identify Wikipedia's Signs of AI writing or other reviewed projects as ancestors. We did not import a Wikipedia passage, an upstream word list, detector implementation, or a block of source prompt text into ClearWeave. Shared ancestry is recorded where observed; 32 implementations are not 32 independent validations.

Paul Goldsmith-Pinkham's [Writing & Thinking with AI Assistance](https://paulgp.substack.com/p/writing-and-thinking-with-ai-assistance) informed the separation of author control, voice samples, and editorial advice. It is an additional method source, not a 33rd skill.

The source audit is dated 2026-10-20 and records inspections of mutable main branches, sometimes drawing on a documented prior reading on 2026-10-19. No commit-pinned upstream snapshot or complete fork graph is claimed.

## Scholarly extension (v0.3.0)

S33–S42 are credited in docs/source-audit.json and docs/scholarly-source-snapshots.json. New runtime prose and Python code are independently written for ClearWeave. The GPL-3.0 HD0NG entry and the license-unknown shannhk entry were reviewed as conceptual references, not copied into the package. YoakeLee attributes an underlying educational framework separately from its repository wording. Allan9719 attributes SciWrite (Lorena A. Barba, CC BY 4.0) and a writing framework; neither the underlying book nor its section tables are reproduced here. Source licenses retain their original scope.

Public ACL abstract samples carry their authors, source URLs, and CC BY 4.0 attribution in evals/scholarly-2026-10-20. Revisions are labeled ClearWeave applications, not changes made by the original authors. HC3 source records retain the earlier CC BY-SA 4.0 notices and provenance.

Additional conceptual references: OvOYu/anti-defensive-writing and Worigin0314/academic-defensive-writing-auditor declare MIT in their inspected entries; Mseymur/HCI-Academic-Writing has a LICENSE file whose text was not inspected in this review. No upstream source text or code from these projects is reproduced in the runtime.

Lieflat integration (S46, 2026-10-21): rule design adapted from
larashero3-dotcom/lieflat-less-ai-tone, revision 27d29232f10124db904ca9c0536d0b67cb3b2833.
Copyright (c) 2026 shiujan, MIT. The complete upstream notice is included at
skills/clearweave/licenses/lieflat-MIT.txt. ClearWeave's Python candidate/ledger implementation is newly written.
