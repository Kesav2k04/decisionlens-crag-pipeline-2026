#!/usr/bin/env python
"""Regenerate the README metrics block from evaluation/results.json.

Single source of truth: evaluation/results.json (written by evaluation/evaluate.py).
No evaluation number is ever hand-typed in README.md; this script replaces the text
between the sentinel markers:

    <!-- METRICS:START -->
    ... generated table + provenance ...
    <!-- METRICS:END -->

Usage:
    python scripts/render_metrics.py            # rewrite README.md in place
    python scripts/render_metrics.py --print    # print the block, do not write
    python scripts/render_metrics.py --check     # exit 1 if README block is stale
"""
import argparse
import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RESULTS_PATH = BASE_DIR / "evaluation" / "results.json"
README_PATH = BASE_DIR / "README.md"
START = "<!-- METRICS:START -->"
END = "<!-- METRICS:END -->"


def _count(per_question, key):
    return sum(1 for r in per_question if r.get(key))


def build_block() -> str:
    data = json.loads(RESULTS_PATH.read_text(encoding="utf-8"))
    s = data["summary"]
    pq = data.get("per_question", [])
    total = s["total_questions"]

    # Counts derived from the per-question log so the "(n/total)" display can never
    # drift from the recorded run.
    cite = _count(pq, "citation_present")
    kw = _count(pq, "keywords_present")
    abst = _count(pq, "abstention_correct")
    dtype = _count(pq, "decision_type_correct")

    rows = [
        ("Citation accuracy", f"{s['citation_accuracy_pct']:.1f}% ({cite}/{total})"),
        ("Keyword accuracy", f"{s['keyword_accuracy_pct']:.1f}% ({kw}/{total})"),
        ("Abstention accuracy", f"{s['abstention_accuracy_pct']:.1f}% ({abst}/{total})"),
        ("Decision-type accuracy", f"{s['decision_type_accuracy_pct']:.1f}% ({dtype}/{total})"),
        ("Average latency", f"{s['avg_latency_seconds']:.1f}s per query (mean over all {total})"),
    ]
    gen = s.get("avg_latency_generative_seconds")
    gen_n = s.get("generative_questions")
    if gen is not None and gen_n:
        rows.append(("Generative latency",
                     f"{gen:.1f}s per query (mean over the {gen_n} that reach Granite)"))

    table = ["| Metric | Result |", "|---|---|"]
    table += [f"| {k} | {v} |" for k, v in rows]

    # Provenance line — machine, model, parser, index size, run date.
    src = s.get("source_counts", {})
    src_str = ", ".join(f"{n} {name}" for name, n in src.items()) if src else ""
    run_date = (s.get("run_date_utc") or "").split("T")[0]
    prov = (
        f"Measured by `evaluation/evaluate.py` over {total} golden questions "
        f"({s.get('chunks_indexed')} indexed chunks"
        f"{' — ' + src_str if src_str else ''}). "
        f"Model: {s.get('model')}. Parser: {s.get('parser')}. "
        f"Machine: {s.get('machine')}."
        f"{' Run: ' + run_date + '.' if run_date else ''} "
        f"All figures regenerated from `evaluation/results.json` by "
        f"`python scripts/render_metrics.py` — none are hand-typed."
    )

    return START + "\n" + "\n".join(table) + "\n\n" + prov + "\n" + END


def splice(readme: str, block: str) -> str:
    if START not in readme or END not in readme:
        raise SystemExit(
            f"README.md is missing the metric sentinels {START} / {END}. "
            "Add them around the metrics block once, then re-run."
        )
    pre = readme[: readme.index(START)]
    post = readme[readme.index(END) + len(END):]
    return pre + block + post


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--print", dest="print_only", action="store_true",
                    help="print the generated block, do not write")
    ap.add_argument("--check", action="store_true",
                    help="exit 1 if README metrics block is out of date")
    args = ap.parse_args()

    block = build_block()

    if args.print_only:
        print(block)
        return 0

    readme = README_PATH.read_text(encoding="utf-8")
    updated = splice(readme, block)

    if args.check:
        if readme != updated:
            print("README.md metrics block is STALE. Run: python scripts/render_metrics.py")
            return 1
        print("README.md metrics block is up to date.")
        return 0

    if readme != updated:
        README_PATH.write_text(updated, encoding="utf-8")
        print("README.md metrics block updated from evaluation/results.json.")
    else:
        print("README.md metrics block already current.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
