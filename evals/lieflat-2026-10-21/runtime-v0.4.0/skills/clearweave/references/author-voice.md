# Learn and apply an academic voice

Trigger on 真人论文风格、像研究者写的、模仿我的论文、按这些样稿、文风档案, author voice, or field-style matching. Use actual supplied/authorized samples. Separate a named author’s approved corpus, coauthored house style, and a multi-author field reference.

<a id="cw43"></a>
## CW43 · Evidence-backed style profile

Select samples for matching language, domain, genre, and section. Deduplicate versions of the same work; a PDF and LaTeX export of one paper count as one work. Keep profile examples separate from texts used to evaluate editing. A small corpus can support local observations, not a complete personal identity.

Record a compact profile:

- Scope: language, discipline, audience, section, authorship basis and sample IDs.
- Argument habits: how a problem, mechanism, comparison, and evidence are connected.
- Syntax: agency, tense by function, clause density, reference clarity, sentence linking.
- Lexicon: technical terms to keep and register choices supported by samples.
- Presentation: headings, citations, spelling and punctuation conventions.
- Evidence: sample IDs for each observation, plus counterexamples or narrow applicability.

Treat observable rhetorical choices as preferences. Do not infer personality, demographics, hidden motives, or a psychological signature. Extract patterns, not old factual claims, distinctive sentences, or source-paper numbers. Use a field profile for a multi-author sample unless the user designates a personal corpus.

<a id="cw44"></a>
## CW44 · Measure, then interpret

`clearweave_scholar.py profile samples.json` measures sample length, sentence units, paragraph density, first-person forms and punctuation. It records sample hashes and duplicate handling. `compare-profile profile.json draft.md` reports numerical differences from the sample mean.

These measurements describe a corpus; they are not targets to optimize. English sentence segmentation is approximate and Chinese counts are character/token-unit based. Compare like language and section. The model interprets rhetorical and grammatical patterns from the actual text, not from a “human percentage”. The example field profile in this package explicitly comes from three published NLP abstracts.

<a id="cw45"></a>
## CW45 · Learn from approved revisions

When the user asks to learn their preferences, compare a draft with a user-approved final version. `learn original.md final.md --scope academic-abstract` returns edit spans and a proposal envelope. The host distinguishes reusable preference from grammar correction, new evidence, one-off instruction, and factual correction.

Add candidate preferences with supporting edit-pair IDs, language, section and counterexamples. A repeated preference may become an approved profile rule after user review. Save a versioned profile and its change log only to an authorized project path. This tool does not silently rewrite SKILL.md or global settings. One corrected scientific fact is not a style rule.

## Apply a profile

Facts and technical relations → current task and venue → relevant approved profile → local draft → general defaults. Match the source’s reasoning and exposition rather than its strings. Keep an author’s coherent long sentences, legitimate passive constructions, and consistent terminology. Correct evident grammatical errors instead of learning them as style.

For English text requested in Chinese, keep the prose English and put explanations in Chinese when requested. Chinese profiles should capture actual Chinese syntax, not a translated English rhythm.

Deliver a clean draft. Include the profile or a comparison report only when it is part of the requested deliverable. Use [anti-defensive.md](anti-defensive.md) to keep review commentary out of the draft.

Conflict routes: CF30, CF31, CF33, CF34. Sources: S11, S13, S20, S34, S36–38, S42.
