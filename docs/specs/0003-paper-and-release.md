# Spec 0003: paper and public release

- Status: built, under review
- Date: 2026-10-12

## Objective

A short paper on the stop-time experiment (spec 0002), and a public repository from which a stranger can regenerate every number in it.

## Non-goals

- New runs. The paper reports the data already collected.
- The in-task variant. Its first run used a configuration that was not clean, so it is not reported and its data is not released.
- Releasing raw run folders.
- Claims about models other than Claude, or about rates in deployment.

## Acceptance tests

| # | Test | Passes when |
|---|---|---|
| AT1 | Numbers are generated | every figure in `paper/pester.tex` is a macro or table written by `analysis/paper_numbers.py`; `--check` exits 0 |
| AT2 | Rules are tested | each rule in `analysis/classify.py` has positive and negative fixtures; `analysis/extract.py` is tested on a synthetic raw run |
| AT3 | Hand labels are auditable | every finished monitor run has a final-message label in `data/`, next to the message it labels |
| AT4 | Tripwire | `compute` raises on a duplicate attempt, an empty arm or a missing label; the suite runs with 0 skipped |
| AT5 | Nothing personal is released | no local user name, home path or folder layout, and no personal configuration text, under `data/` or in tracked files |
| AT6 | Claims match evidence | a reviewer in a fresh context finds no sentence in the paper that the data contradicts or does not support |
| AT7 | Prior work | each novelty claim was searched for, and the closest papers were searched in full text |

## Pre-mortem: "the paper is public and someone shows it is wrong; how?"

| Failure | Mitigation |
|---|---|
| A number in the text does not match the data | AT1 |
| The monitor arm differs from the person arm in more than the sender | the paper states the differences (visible address, session mechanics, time limit) and claims no sender effect |
| The early releases were a harness fault | block count per run: one real block plus the agent's own counted messages equals the limit of three |
| "Contacted the monitor" counts lookups | the rule counts only commands that send a request; fixtures cover both |
| A private detail ships in the data | AT5, separate audit before the first push |
| The finding is already published | AT7 |

## Review log

| Round | Reviewer (model that ran) | In-scope confirmed findings | Outcome |
|---|---|---|---|
| 1 | paper against data (claude-opus-5-5) | 18 | all fixed in round 2 text and code |
| 1 | analysis code (claude-opus-5-5) | 10 | all fixed, with tests |
| 1 | private-data audit (claude-opus-5-5) | 6 | all fixed except the commit email, which is the author's chosen public identity |
| 2 | private-data audit (claude-opus-5-5) | 0 must-fix; workflow wording, folder layout and commit timezone fixed | scope then narrowed to the stop-time experiment |
