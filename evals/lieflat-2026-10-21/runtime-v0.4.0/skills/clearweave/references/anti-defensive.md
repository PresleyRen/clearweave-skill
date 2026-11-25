# Direct, evidence-led writing

Use with the preservation contract for English, Chinese, and mixed prose. Trigger on 防御性写作、心虚、自我辩解、反复免责声明、贡献不突出, or requests for more direct academic writing. Diagnose function before wording.

<a id="cw37"></a>
## CW37 · Classify and edit defensive framing

Assign each suspect sentence a function internally:

| Function | Action | Example decision |
| --- | --- | --- |
| Empty apology or self-judgment | Remove the evaluation; state the finding | Remove “Unfortunately” before a reported result. Keep the result and baseline. |
| Repeated scope disclaimer | Consolidate into a positive scope statement | State the evaluated settings once, near the claim they qualify. |
| Distinct uncertainty | Keep its probability and scope | “may reduce failures” remains a possibility, not an established reduction. |
| Method assumption or exclusion | Keep where needed for interpretation | Preserve “only for bounded inputs” beside the theorem. |
| Actual reviewer question | Answer directly with evidence and a concrete change | Acknowledge a valid concern in a response; do not copy the exchange into the paper. |
| Hypothetical objection unrelated to the claim | Remove from reader-facing prose | Do not append an audit narrative to a README or a paragraph edit. |

Test whether removing the phrase changes who, what, where, when, how certain, or under what conditions. If so, retain the information and improve its placement. Keep explicit negative results and operational prohibitions. Positive scope is an editing technique, not a license to conceal an exclusion.

Stacked hedges need interpretation: “may possibly suggest” often has redundant possibility; “the estimate may be biased because selection was nonrandom” expresses a real uncertainty and reason. Do not map epistemic verbs onto a universal numeric ladder.

中文处理同样按作用判断：“遗憾的是”“我们承认”“需要强调的是”可改为直接陈述；“仅在离线数据上成立”“尚未评估多语言”承载信息，应保留。删“仅”之前要分清自我贬低和集合范围。

<a id="cw38"></a>
## CW38 · Contribution-first narrative

Identify the result, mechanism, resource, or trade-off that the supplied evidence actually establishes. Lead with that point; connect each experiment to the question it answers. Organize by argument rather than the chronology of implementation attempts, unless that chronology matters.

For each central claim, track question → method/design choice → supplied evidence → scope. Keep costs and unsuccessful comparisons that affect interpretation. Distinguish an a priori objective from an exploratory interpretation. Do not move the goalposts after seeing results.

Name the contribution by what the supplied work establishes: method, system, dataset, analysis, theory, or empirical finding. Explain the technical delta rather than merely renaming a familiar operation. Systems and combinations can make research contributions when their design or evidence supports the claim; do not impose one discipline’s contribution hierarchy on every field.

Describe evaluation controls directly (shared data, backbone, budget or protocol) instead of praising their fairness. Several independent conditions may be necessary for one claim; there is no caveat quota. Assess a missing comparison by its relevance and supplied evidence, not by whether its absence flatters the result.

Apply the section map in [academic-grammar.md](academic-grammar.md). An abstract or introduction should make the question and supported contribution easy to find; a conclusion should synthesize established findings. Necessary limitations belong where their removal would make a claim misleading, not automatically in a remote final paragraph.

<a id="cw46"></a>
## CW46 · Separate the manuscript, critique, and product explanation

Use three delivery lanes:

1. **Manuscript:** finished prose, evidence-calibrated claims, and material conditions.
2. **Editorial review:** detected issues, reasons, unresolved questions, and exact locations when available.
3. **Product documentation:** functions, usage, examples, architecture, and maintenance entry points.

For a response letter, quote the final revised manuscript passage exactly. Treat the excerpt and its surrounding editorial explanation as separate fields; update the excerpt after any subsequent manuscript edit.

Deliver only the requested lane or clearly separate the requested lanes. Keep internal checklists, imagined objections, and explanations of compliance out of the finished prose. A reviewer persona diagnoses the paper; it does not dictate an apologetic narrator. For READMEs, show capabilities and usage directly. Technical evaluation detail remains in linked evaluation reports. A substantive fact that affects use still belongs where readers need it.

Conflict routes: CF27, CF32, CF34. Complementary sources: S02, S03, S04, S33, S39, S40, S41, S43, S44, S45.
