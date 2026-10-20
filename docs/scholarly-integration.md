# Scholarly integration / 学术写作整合说明

## Four editing layers / 四层编辑

| Layer | Work | Modules |
| --- | --- | --- |
| Natural prose | Structure, syntax, stock phrasing and translation artifacts | english.md, chinese.md |
| Direct research writing | Necessary qualifications, contribution focus, neutral result reporting | anti-defensive.md, academic.md |
| Academic grammar | Function-sensitive tense, agreement, articles, modifiers and information flow | academic-grammar.md |
| Observed voice | Sample selection, corpus measurement, rhetorical profile and approved-revision preferences | author-voice.md, clearweave_scholar.py |

All layers share preservation.md. Task routing, output language and intervention strength are defined in SKILL.md. The installed skill contains the references, prompts, tools and capability registry.

## New source-to-feature map / 新增来源如何互补

| ID | Reference | Adopted feature | Implementation |
| --- | --- | --- | --- |
| S33 | [mronkko/claude-academic-research](https://github.com/mronkko/claude-academic-research/blob/4579a86de137beb40ac2b31a143577115d721532/skills/academic-style/SKILL.md) | Choose tense by the rhetorical function of a sentence, and keep technical terminology consistent. Organize related work as a synthesis and calibrate uncertainty to the evidence. | CW38, CW39, CW42 |
| S34 | [HD0NG/claude-skills](https://github.com/HD0NG/claude-skills/blob/b5b99ff2383a6c050856c9e68646e8c43567bdb9/skills/academic-writing/SKILL.md) | Distinguish contribution statements, procedures, results and interpretation when choosing voice. Represent a reusable voice profile with domain and manuscript-section scope. | CW38, CW39, CW43 |
| S35 | [YoakeLee/academic-paper-writing-skill](https://github.com/YoakeLee/academic-paper-writing-skill/blob/ce4f3d8bc51ca88c7b68a770b17ba863ba456e4e/academic-paper-writing/SKILL.md) | Check grammatical heads, agreement, dangling modifiers, articles and related word forms. Use reverse outlines and a paragraph’s controlling purpose when restructuring is requested. | CW40, CW41, CW42 |
| S36 | [Jingyang-Zhu/personal-academic-writing-skill](https://github.com/Jingyang-Zhu/personal-academic-writing-skill/blob/114a4d3cab819a3505378b9a45f35d429e7fb114/SKILL.md) | Extract stable argument and exposition habits from actual technical papers, with sample provenance and duplicate-work handling. Link a stated challenge to a method component and its supporting evidence. | CW38, CW43, CW44 |
| S37 | [shannhk/writing-style-extractor](https://github.com/shannhk/writing-style-extractor/blob/a6b3ba0138cab32efc937b6f4491f49a23f750cc/SKILL.md) | Separate surface measurements, syntax, structure and a practical style profile. Support a style observation with actual samples rather than a generic adjective. | CW43, CW44 |
| S38 | [snowmays/style-alchemy](https://github.com/snowmays/style-alchemy/blob/b17cfa6e23433ac0e44ca6d899ac9922aaa0b240/SKILL.md) | Normalize and group samples by genre, then create a machine-readable profile with evidence. Keep thematic content preferences separate from writing style, and compare relevant profiles dimension by dimension. | CW43, CW44, CW45 |
| S39 | [YuanZHAO321/Scientific-Writing](https://github.com/YuanZHAO321/Scientific-Writing/blob/44b95b225866b463b8148dc612638b27bf60ec90/SKILL.md) | Revise document organization, paragraph relations and sentences in that order when structural editing is authorized. Use familiar-to-new information flow and distinguish grammatical corrections from matters of taste. | CW38, CW41, CW46 |
| S40 | [KalarisLabs/research-agent-skills](https://github.com/KalarisLabs/research-agent-skills/blob/1390e3aec9155c494fb5232891c23e9f5eedd566/skills/ml-paper-writing/SKILL.md) | Draft from supplied repository evidence and connect a contribution to questions, comparisons and findings. Keep narrative, experiments, and source-supported citations consistent. | CW38, CW42, CW48 |
| S41 | [Allan9719/scientific-writer-skill](https://github.com/Allan9719/scientific-writer-skill/blob/bce0a8f5b2a6ed0abd8ea897e37757fe9ab7b629/SKILL.md) | Choose a sentence’s communicative purpose before its grammatical form; separate drafting, editing, diagnosis and teaching. Review modifiers, referents, technical terms and quantitative statements together. | CW38, CW39, CW40, CW41, CW42 |
| S42 | [jzOcb/writing-style-skill](https://github.com/jzOcb/writing-style-skill/blob/d94826e1cd48f5403b82a5a909efdfab96221259/SKILL.md) | Use draft/final edit pairs to collect candidate writing preferences. Version preferences with supporting examples and retain a reversible review record. | CW43, CW45, CW46 |
| S43 | [OvOYu/anti-defensive-writing](https://github.com/OvOYu/anti-defensive-writing/blob/bdab0d2aeb082798ad71cac3ab24a616d2d82894/SKILL.md) | Separate audit, local polishing, restructuring and drafting; retain scope beside the claim it qualifies. When quoting the revised manuscript in a response letter, use the actual final passage rather than a separately rewritten quotation. | CW37, CW38, CW46 |
| S44 | [Worigin0314/academic-defensive-writing-auditor](https://github.com/Worigin0314/academic-defensive-writing-auditor/blob/89f26b8a7f8149e6458f657010d354587d42cfe9/SKILL.md) | Distinguish empty defensive wording, necessary qualification, mixed wording and clean prose before proposing an edit. Replace fairness self-praise with actual controls, and keep explanations of adverse results tied to supplied diagnostics. | CW37, CW38, CW47 |
| S45 | [Mseymur/HCI-Academic-Writing](https://github.com/Mseymur/HCI-Academic-Writing/blob/bd5d19c641dbc224b3e653b1e22b2b259e63be28/skills/hci-academic-writing/SKILL.md) | Separate register problems from contribution framing; describe the specific technical or empirical advance rather than relying on a flattering label. Distinguish proposed outcomes from delivered findings, and synthesize related work around the actual research question. | CW37, CW38, CW42, CW46 |

## Conflict decisions / 主要冲突与处理

| Conflict | Decision | Regression |
| --- | --- | --- |
| Stronger prose / uncertainty | Remove empty apology; preserve likelihood and scope. | CF27; W19-4703; W19-5028 |
| Correct grammar / exact quotation | Correct editable prose and annotate quoted errors separately. | CF28; protected-span tests |
| Past-tense Methods / current algorithm behavior | Select tense by sentence function, not section name alone. | CF29 |
| Sample imitation / source facts | Extract habits; retain the draft’s own facts. | CF30; profile/edit disjointness |
| Measured sentence length / quota | Report descriptive values; preserve coherent variation. | CF31 |
| Paper template / actual evidence | Select relevant rhetorical moves; keep system/theory/empirical contributions distinct. | CF32 |
| Grammar mistakes / author habit | Correct evident errors; match stable exposition preferences. | CF33; Sentence-BERT |
| Learned preference / global rule | Keep scope and pending approval attached to each proposal. | CF34; learn tests |
| Caveat quota / claim interpretation | Keep every material independent condition beside its claim. | CF01; CW37 |
| Response-letter quote / separately edited text | Copy the actual final manuscript excerpt; update it after manuscript changes. | CW46; shared quote protection |

## Extending a layer / 扩展步骤

1. Save the original, problematic output, requested mode and intended distinction.
2. Use clearweave_trace.py to locate CW capability, CF conflict, source decisions and module.
3. Add an incorrect example and a valid lookalike. Put parsing failures in Python tests and editing failures in application cases.
4. Change the smallest scoped rule, rerun tests and a new real-text application.
5. Update capabilities.json, feature-map.json, source audit and generated tables. Record measured results in the evaluation report.

## Source inspection

S33–S45 are pinned by commit; file hashes or Git blob IDs are recorded in scholarly-source-snapshots.json. Original source decisions are retained. The coverage count describes this reviewed inventory, not every skill on the internet. Source inspiration is distinct from running the upstream projects. New instructions and code are independently written. License observations and attribution are in NOTICE.md and source-audit.json.
