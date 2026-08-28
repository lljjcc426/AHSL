"""Reproduce the bounded AP-R0 artifact pre-gates.

This adapter does not implement a method.  It runs the frozen current-artifact
checks used to decide whether a candidate is eligible for a residual semifinal.
"""

from __future__ import annotations

import argparse
import csv
import os
import platform
import subprocess
import sys
import time
from pathlib import Path


FIELDS = [
    "candidate_id",
    "system",
    "version",
    "benchmark",
    "workload",
    "configuration",
    "metric",
    "baseline_value",
    "failure_value",
    "ratio_or_gap",
    "repeat_count",
    "correctness",
    "hardware",
    "gate_status",
    "notes",
]


def run(command: list[str], env: dict[str, str] | None = None) -> tuple[int, float, str]:
    started = time.perf_counter()
    completed = subprocess.run(
        command,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=env,
        timeout=120,
    )
    elapsed_ms = (time.perf_counter() - started) * 1000
    output = (completed.stdout + "\n" + completed.stderr).strip()
    return completed.returncode, elapsed_ms, output


def compact_failure(output: str) -> str:
    if "UnicodeDecodeError" in output:
        return "UnicodeDecodeError while loading an Inductor template under the default GBK locale"
    if "InvalidCxxCompiler" in output:
        return "InvalidCxxCompiler: cl is not found"
    lines = [line.strip() for line in output.splitlines() if line.strip()]
    return lines[-1][:300] if lines else "no diagnostic"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--torch-target", type=Path, required=True)
    parser.add_argument("--cpbench-root", type=Path, required=True)
    parser.add_argument("--cpmpy-target", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--hardware", default="")
    args = parser.parse_args()

    hardware = args.hardware or f"{platform.system()} {platform.release()}; {platform.machine()}"
    rows: list[dict[str, object]] = []
    torch_code = (
        "import torch; print(torch.__version__); "
        "f=torch.compile(lambda x:x.sin()+x.cos(),dynamic=None); "
        "print(float(f(torch.randn(32)).sum()))"
    )
    base_env = os.environ.copy()
    base_env["PYTHONPATH"] = str(args.torch_target)

    for label, utf8 in [("default_locale", None), ("utf8_mode", "1")]:
        env = base_env.copy()
        if utf8 is None:
            env.pop("PYTHONUTF8", None)
        else:
            env["PYTHONUTF8"] = utf8
        code, elapsed, output = run([sys.executable, "-c", torch_code], env)
        rows.append(
            {
                "candidate_id": "D1_dynamic_shape_compilation",
                "system": "PyTorch",
                "version": "2.13.0+cpu",
                "benchmark": "torch.compile artifact pre-gate",
                "workload": "elementwise sin+cos, shape 32",
                "configuration": label,
                "metric": "build_and_first_execution",
                "baseline_value": "NA",
                "failure_value": f"{elapsed:.3f} ms to failure" if code else f"{elapsed:.3f} ms",
                "ratio_or_gap": "NA",
                "repeat_count": 1,
                "correctness": str(code == 0).lower(),
                "hardware": hardware,
                "gate_status": "FAIL_PRE_GATE" if code else "PASS_PRE_GATE",
                "notes": "success" if code == 0 else compact_failure(output),
            }
        )

    cp_env = os.environ.copy()
    cp_env["PYTHONPATH"] = str(args.cpmpy_target)
    for name in ["bank_card.py", "color_simple.py", "five_floors.py"]:
        path = args.cpbench_root / "data" / "aplai_course" / name
        code, elapsed, output = run([sys.executable, str(path)], cp_env)
        rows.append(
            {
                "candidate_id": "E1_constraint_model_synthesis",
                "system": "CP-Bench/CPMpy",
                "version": "CP-Bench 92ba7dc; CPMpy 0.9.25; OR-Tools 9.14.6206",
                "benchmark": "CP-Bench APLAI course",
                "workload": name,
                "configuration": "published ground-truth model",
                "metric": "ground_truth_execution",
                "baseline_value": f"{elapsed:.3f} ms",
                "failure_value": "NA",
                "ratio_or_gap": "NA",
                "repeat_count": 1,
                "correctness": str(code == 0 and "{" in output).lower(),
                "hardware": hardware,
                "gate_status": "BENCHMARK_RUN_ONLY",
                "notes": "No current 2026 model output was generated; this is not residual evidence.",
            }
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    print(f"wrote {len(rows)} pre-gate rows to {args.output}")


if __name__ == "__main__":
    main()
