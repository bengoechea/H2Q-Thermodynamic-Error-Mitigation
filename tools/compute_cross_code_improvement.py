#!/usr/bin/env python3
"""Compute the known cross-code improvement number (~895.7%).

This script exists to make the repository's "~895.7% cross-code improvement" claim
reproducible from a small, explicit input table.

Definition used:
  improvement_pct = (h2q_pct - baseline_pct) / baseline_pct * 100

Usage:
  python3 tools/compute_cross_code_improvement.py \
    --input data/qec_cross_code_improvement.json

Outputs per-code improvement and the arithmetic mean across codes.
The input may also contain display-rounded fields (for narrative), while the
computation uses the numeric baseline_pct/h2q_pct values.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def compute_improvement(baseline_pct: float, h2q_pct: float) -> float:
    if baseline_pct <= 0:
        raise ValueError(f"baseline_pct must be > 0; got {baseline_pct}")
    return (h2q_pct - baseline_pct) / baseline_pct * 100.0


def main() -> None:
    parser = argparse.ArgumentParser(description="Compute cross-code improvement.")
    parser.add_argument(
        "--input",
        default="data/qec_cross_code_improvement.json",
        help="Path to input JSON containing per-code baseline/h2q rates.",
    )
    args = parser.parse_args()

    data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    codes = data.get("codes", [])
    if not codes:
        raise SystemExit("No codes found in input")

    imps: list[float] = []
    print("Per-code improvements (percent):")
    for row in codes:
        name = row["code"]
        base = float(row["baseline_pct"])
        h2q = float(row["h2q_pct"])
        imp = compute_improvement(base, h2q)
        imps.append(imp)
        disp_base = row.get("display_baseline_pct", base)
        disp_h2q = row.get("display_h2q_pct", h2q)
        disp_imp = row.get("display_improvement_pct", None)
        suffix = f"; display {disp_base:.2f}% -> {disp_h2q:.2f}%"
        if disp_imp is not None:
            suffix += f" (display improvement {float(disp_imp):.2f}%)"
        print(f"- {name}: {imp:.2f}% (computed from {base:.6f}% -> {h2q:.6f}%{suffix})")

    mean_imp = sum(imps) / len(imps)
    print("\nCross-code mean improvement:")
    mean_round_2 = round(mean_imp, 2)
    # Truncation is sometimes used in marketing summaries; make it explicit if used.
    mean_trunc_2 = int(mean_imp * 100) / 100.0
    print(f"- mean (raw): {mean_imp:.6f}% over n={len(imps)} codes")
    print(f"- mean (rounded to 2dp): {mean_round_2:.2f}%")
    print(f"- mean (truncated to 2dp): {mean_trunc_2:.2f}%")


if __name__ == "__main__":
    main()
