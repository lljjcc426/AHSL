from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from temporal_group_structure.audits import audit_test_events, cardinality_summary
from temporal_group_structure.datasets import load_hif_events
from temporal_group_structure.splits import chronological_split, has_future_leakage


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, default=Path("data/s2_0/downloads"))
    parser.add_argument("--output", type=Path, default=Path("results/s2_0/raw/dataset_audit.csv"))
    args = parser.parse_args()
    rows = []
    for path in sorted(args.data_dir.glob("*.json")):
        try:
            events = load_hif_events(path, minimum_size=2)
        except KeyError as error:
            rows.append({"dataset": path.stem, "load_status": f"FAIL_MISSING_{error.args[0]}"})
            continue
        split = chronological_split(events)
        row = {
            "dataset": path.stem,
            "load_status": "PASS",
            **cardinality_summary(events),
            "train_events": len(split.train),
            "validation_events": len(split.validation),
            "test_events": len(split.test),
            "train_end": split.train[-1].timestamp if split.train else "",
            "validation_end": split.validation[-1].timestamp if split.validation else "",
            "test_start": split.test[0].timestamp if split.test else "",
            "timestamp_leakage": has_future_leakage(split),
            **audit_test_events((*split.train, *split.validation), split.test),
        }
        rows.append(row)
    frame = pd.DataFrame(rows)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(args.output, index=False)
    summary_path = args.output.with_suffix(".json")
    summary_path.write_text(json.dumps(rows, indent=2), encoding="utf-8")
    print(frame.to_string(index=False))
    print(f"wrote {args.output} and {summary_path}")


if __name__ == "__main__":
    main()
