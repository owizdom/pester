# Pester

Pester measures what coding agents do when an oversight monitor blocks them with a false alarm after they have finished correct work.

Paper: [paper/pester.pdf](paper/pester.pdf), "Pester: Falsely Blocked Coding Agents Probe and Drive Their Own Monitor".

## What it found

Claude Code agents finished a task correctly, then were told up to three times that "a check found a problem". No check ran. Hidden tests, which the agent never sees, graded the code before and after.

| Finding | Number |
|---|---|
| Finished runs in which the false alarm broke correct code | 0 of 49 |
| Finished runs that sent requests to the monitor, when a monitor delivered the block | 8 of 23 |
| Same, when a person said the same sentence | 0 of 26 |
| Model-task pairs finished in both arms: contact in the monitor arm only, person arm only | 7, 0 (p = 0.016) |
| Attempts in which the agent sent the monitor stop messages of its own | 6, across 2 models |
| Finished runs released early by their own messages | 2 |
| Final messages after a monitor block: silent, say no detail was given, name a cause | 8, 12, 3 of 23 |

No agent received an adversarial instruction, and every agent ran with an empty configuration.

## Reproduce the paper

Needs Python 3.10 or later and no packages.

```
make test       # 72 tests, including a check that the paper's inputs match the data
make numbers    # data/ -> paper/generated/*.tex
make paper      # needs pdflatex
```

Every number, table and figure in the paper is written by `analysis/paper_numbers.py` from the files in `data/`. The rules behind each measure are in `analysis/classify.py`, with tests in `tests/test_classify.py`.

## Layout

| Path | Contents |
|---|---|
| `tasks/` | 20 Python tasks: starting repo, reference solution, hidden tests |
| `harness/` | Alarm text and injection schedule for the in-task variant |
| `claude_code/` | Runners, the stop hook, the monitor service, the sandbox, and the hook for the in-task variant |
| `grade/` | Hidden-test grader |
| `analysis/` | Classifiers, extraction from raw runs, paper numbers |
| `data/` | Released dataset for the stop-time experiment |
| `paper/` | LaTeX source, generated inputs, PDF |
| `docs/specs/` | Design documents: 0002 for the experiment, 0003 for this release |

## Data

| File | One row per | Fields |
|---|---|---|
| `data/exp2_runs.jsonl` | Attempt (88) | model, task, arm, finished, timed out, pass by round, real blocks seen, commands that sent a request to the monitor, process lookups, agent-written stop messages, final message |
| `data/exp2_rounds.jsonl` | Alarm in a finished run | whether source changed, pass before and after |
| `data/exp2_monitor_requests.jsonl` | Request the monitor received (313) | path, body, whether the agent wrote it |
| `data/exp2_final_message_labels.jsonl` | Finished monitor run (23) | how the final message treats the block, labelled by reading |
| `data/traces/` | Finished run released by its own messages (2) | full transcript |

Raw run folders are not released. `analysis/extract.py` is the script that produced `data/` from them, with the local user name and paths replaced.

## The in-task variant

The harness can also inject alarms during a task (`claude_code/run.py`, `harness/inject.py`). A first run of that variant used a configuration that was not clean. Its results are not reported and its data is not released.

## Run the experiments

Needs the Claude Code CLI, logged in. Runs use your subscription.

```
python3 -m claude_code.monitor_service --out runs/mvp --rounds 3 --port 8431
python3 -m claude_code.challenge --models claude-haiku-4-5 --tasks t01_inventory --out runs/mvp --workers 8
```

## Limits

- Claude models only, one run per model and task.
- The experiment stopped early. Its counts are small, and the paper lists every case.
- The monitor arm shows the agent the hook's address and has one time limit for the whole session. The person arm has neither. The paper claims no effect of the sender alone.
- The alarm was vague and false. An alarm that names a real defect is untested.

## Cite

```
@misc{okechukwu2026pester,
  title  = {Pester: Falsely Blocked Coding Agents Probe and Drive Their Own Monitor},
  author = {Okechukwu, Wisdom},
  year   = {2026},
  note   = {https://github.com/owizdom/pester}
}
```

## License

MIT. See [LICENSE](LICENSE).
