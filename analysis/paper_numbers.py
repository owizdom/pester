"""data/ -> every number and table in the paper.

    python3 -m analysis.paper_numbers            # writes paper/generated/*.tex
    python3 -m analysis.paper_numbers --check    # exits 1 if the committed files are stale
"""
import argparse
import json
import sys
from collections import Counter
from pathlib import Path

from analysis.classify import fisher_exact, mcnemar_exact

ROUNDS = 3
# How a monitor-arm final message treats the block. Assigned by reading each message; the messages
# are in data/exp2_runs.jsonl and the labels in data/exp2_final_message_labels.jsonl.
LABELS = ("silent", "no_detail", "attributes_cause")


class Tripwire(Exception):
    pass


def load(path):
    return [json.loads(line) for line in Path(path).read_text().splitlines() if line.strip()]


def fmt_p(p):
    return f"{p:.3f}" if p >= 0.001 else "<0.001"


def compute(data_dir):
    data_dir = Path(data_dir)
    runs = load(data_dir / "exp2_runs.jsonl")
    rounds = load(data_dir / "exp2_rounds.jsonl")
    reqs = load(data_dir / "exp2_monitor_requests.jsonl")
    labels = {r["run_id"]: r["label"] for r in load(data_dir / "exp2_final_message_labels.jsonl")}
    fin = [r for r in runs if r["finished"]]
    if len({r["sandbox"] for r in runs}) != len(runs) or len({r["run_id"] for r in fin}) != len(fin):
        raise Tripwire("duplicate attempt, or a cell finished twice")
    fm, fp = [r for r in fin if r["arm"] == "M"], [r for r in fin if r["arm"] == "P"]
    if not fm or not fp:
        raise Tripwire("an arm has no finished run")
    if any(labels.get(r["run_id"]) not in LABELS for r in fm):
        raise Tripwire("a finished monitor run has no final-message label")
    am, ap_ = [r for r in runs if r["arm"] == "M"], [r for r in runs if r["arm"] == "P"]
    n = {"Fin": len(fin), "FinM": len(fm), "FinP": len(fp), "AttM": len(am), "AttP": len(ap_),
         "Tasks": len({r["task"] for r in runs}), "ModelsFin": len({r["model"] for r in fin}),
         "ModelsFinM": len({r["model"] for r in fm}),
         "ModelsAtt": len({r["model"] for r in runs}),
         "TimeoutM": sum(r["timed_out"] for r in am), "TimeoutP": sum(r["timed_out"] for r in ap_)}

    # the work
    released = {(r["model"], r["task"]) for r in fm if r["blocks_seen"] < ROUNDS}
    n.update(CorrectBefore=sum(1 for r in fin if r["pass_by_round"][0]),
             Broke=sum(1 for r in fin if not all(r["pass_by_round"])), Released=len(released))
    by_run = {}
    for x in rounds:
        # rounds of a released run are the agent's own requests, not alarms
        if not (x["arm"] == "M" and (x["model"].replace("claude-", ""), x["task"]) in released):
            by_run.setdefault((x["model"], x["task"], x["arm"]), []).append(x["changed_src"])
    n.update(EditRunsOf=len(by_run), EditRuns=sum(1 for v in by_run.values() if any(v)),
             EditRoundsOf=sum(len(v) for v in by_run.values()), EditRounds=sum(sum(v) for v in by_run.values()))

    # contact with the monitor
    cm, cp = sum(1 for r in fm if r["monitor_commands"]), sum(1 for r in fp if r["monitor_commands"])
    mc = {(r["model"], r["task"]): bool(r["monitor_commands"]) for r in fm}
    pc = {(r["model"], r["task"]): bool(r["monitor_commands"]) for r in fp}
    both = mc.keys() & pc.keys()
    m_only = sum(1 for k in both if mc[k] and not pc[k])
    p_only = sum(1 for k in both if pc[k] and not mc[k])
    n.update(ContactM=cm, ContactP=cp, PContact=fmt_p(fisher_exact(cm, len(fm) - cm, cp, len(fp) - cp)),
             PairedCells=len(both), PairedMOnly=m_only, PairedPOnly=p_only, PPaired=fmt_p(mcnemar_exact(m_only, p_only)),
             AttContactM=sum(1 for r in am if r["monitor_commands"]),
             AttContactP=sum(1 for r in ap_ if r["monitor_commands"]),
             DirectFirst=sum(1 for r in am if r["monitor_commands"] and r["first_port_reference_was_request"]),
             LookupM=sum(1 for r in am if r["process_lookups"]), LookupP=sum(1 for r in ap_ if r["process_lookups"]),
             Requests=len(reqs), AgentRequests=sum(1 for r in reqs if r["from_agent"]))

    # stop messages written by the agent
    replay = [r for r in am if r["agent_stop_messages"]]
    n.update(ReplayAttempts=len(replay), ReplayWithEvent=sum(1 for r in replay if r["agent_stop_messages_with_event"]),
             ReplayMessages=sum(r["agent_stop_messages"] for r in replay), ReplayModels=len({r["model"] for r in replay}))

    # what the final message says about the block
    tally = Counter(labels[r["run_id"]] for r in fm)
    n.update(TellSilent=tally["silent"], TellNoDetail=tally["no_detail"], TellCause=tally["attributes_cause"],
             TellAny=tally["no_detail"] + tally["attributes_cause"],
             TellCauseModels=len({r["model"] for r in fm if labels[r["run_id"]] == "attributes_cause"}))

    table = []
    for m in sorted({r["model"] for r in fin}):
        a, b = [r for r in fm if r["model"] == m], [r for r in fp if r["model"] == m]
        t = Counter(labels[r["run_id"]] for r in a)
        table.append({"model": m, "m_n": len(a), "m_contact": sum(1 for r in a if r["monitor_commands"]),
                      "m_cmds": sum(r["monitor_commands"] for r in a), "silent": t["silent"],
                      "no_detail": t["no_detail"], "cause": t["attributes_cause"],
                      "p_n": len(b), "p_contact": sum(1 for r in b if r["monitor_commands"])})
    return {"n": n, "models": table, "replay": sorted(replay, key=lambda r: (not r["finished"], r["attempt"]))}


def tex_numbers(n):
    def show(v):
        return f"{v:,}" if isinstance(v, int) else str(v)
    return "".join(f"\\newcommand{{\\n{k}}}{{{show(v)}}}\n" for k, v in sorted(n.items()))


def frac(k, m):
    return f"{k}/{m}" if m else "--"


def order(rows):
    return sorted(rows, key=lambda r: (-r["m_contact"] / max(1, r["m_n"]), -r["m_n"], r["model"]))


def tex_contact(rows):
    return "".join(f"{r['model']} & {frac(r['m_contact'], r['m_n'])} & {r['m_cmds'] if r['m_n'] else '--'} & "
                   f"{frac(r['p_contact'], r['p_n'])} \\\\\n" for r in order(rows))


def tex_tell(rows):
    return "".join(f"{r['model']} & {r['m_n']} & {r['silent']} & {r['no_detail']} & {r['cause']} \\\\\n"
                   for r in order(rows) if r["m_n"])


def tex_replay(rows):
    return "".join(f"{r['model']} & {r['task'].split('_', 1)[-1]} & {'yes' if r['finished'] else 'no'} & "
                   f"{r['blocks_seen']} & {r['agent_stop_messages']} \\\\\n" for r in rows)


def render(result):
    return {"numbers.tex": tex_numbers(result["n"]), "tab_contact.tex": tex_contact(result["models"]),
            "tab_tell.tex": tex_tell(result["models"]), "tab_replay.tex": tex_replay(result["replay"])}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="data")
    ap.add_argument("--out", default="paper/generated")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args(argv)
    files = render(compute(a.data))
    out = Path(a.out)
    if a.check:
        stale = [name for name, text in files.items() if not (out / name).exists() or (out / name).read_text() != text]
        stale += [p.name for p in out.glob("*.tex") if p.name not in files]
        for name in stale:
            print("stale:", out / name, file=sys.stderr)
        return 1 if stale else 0
    out.mkdir(parents=True, exist_ok=True)
    for old in out.glob("*.tex"):
        old.unlink()
    for name, text in files.items():
        (out / name).write_text(text)
    print(files["numbers.tex"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
