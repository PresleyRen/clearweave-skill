# Evaluation protocol

This repository separates writing behaviour from deterministic script checks.

## Writing comparison

- Original synthetic requests are in `cases.json`; none are real user manuscripts.
- There are 18 requests covering English, Simplified Chinese, Traditional Chinese, mixed prose, academic and business editing, two good-text controls, translation in both directions, diagnosis, voice matching, drafting from notes, critique, and shortening.
- Each condition receives the identical request and source. The plain condition uses the host model's ordinary writing judgement. The ClearWeave condition additionally reads the skill and relevant references.
- Each condition is split into CW01–CW09 and CW10–CW18. Each batch runs in a newly spawned context without conversation history. Cases inside a batch share that context; this is not 18 fully isolated or repeated trials.
- Generation agents receive no expected answers, evaluator rubric, source audit, comparison outputs, or instructions to prove a benefit. They write their actual deliverables to `runs/`.
- The host environment provides the model; no separate provider API, temperature, or pinned model snapshot is configured by this repository. The work was performed in a ChatGPT agent session identified to the maintainer as GPT-6 Astra Pro. Child model snapshot and sampling parameters are not exposed. Do not treat this as a cross-model benchmark.
- One response per case and condition is retained. No cherry-picked rerolls. If a defect is repaired, keep the original result and label the later run as a regression check.

## Review

The rubric in `rubric.json` was written before the maintainer inspected generated outputs. A separate fresh-context reviewer sees the requests, sources, rubric, and candidates labelled A/B with their order alternated by case. It does not see the skill, condition mapping, or generation agents' reasoning. The reviewer reports fidelity, task compliance, restraint, an ordinal readability judgement, and A/B/tie with reasons.

The maintainer reviews the original outputs and flags disputed judgements separately. Blind model review is not independent human review, nor proof of unchanged meaning. Publish raw responses, rubric, candidate mapping, findings, and any repairs. Do not turn a small-case preference count into a population success rate.

## Deterministic checks

`python3 -m unittest discover -s tests -v` exercises the local checker with positive cases, false-positive controls, malformed inputs, and explicitly documented semantic blind spots. A literal comparison can miss swapped roles or changed negation. A lint finding is a candidate, not proof of poor style.

The repository validator checks packaging, reference links, and all 32 source IDs. These are structural checks, not writing-effect measurements.

## Reproduction

Re-run the deterministic checks locally. To reproduce writing behaviour, use a chosen model in fresh contexts with the exact requests in `cases.json`, using one batch per condition and the corresponding skill files. Record model identifier, parameters when available, date, prompt, outputs, and skill hashes. Readability and rewrites may vary; this repository contains no automatic model API runner or detector integration.
