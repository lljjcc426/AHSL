"""F1-specific readiness checks with explicit tri-state results."""

from __future__ import annotations

import argparse
import importlib
import json
from pathlib import Path
import shutil
import sys
import xml.etree.ElementTree as ET


RESULT_CHOICES = ("PASS", "FAIL", "BLOCKED", "NOT_RUN", "UNKNOWN")
F1_MODULES = (
    "vulnerability_repair.f1_d1",
    "vulnerability_repair.f1_d1.runner",
    "vulnerability_repair.f1_d1.verifier",
)


def protocol_result(path: Path | None) -> str:
    if path is None:
        return "NOT_RUN"
    if not path.is_file():
        return "UNKNOWN"
    root = ET.parse(path).getroot()
    suites = [root] if root.tag == "testsuite" else list(root.findall("testsuite"))
    tests = sum(int(suite.attrib.get("tests", 0)) for suite in suites)
    failures = sum(int(suite.attrib.get("failures", 0)) for suite in suites)
    errors = sum(int(suite.attrib.get("errors", 0)) for suite in suites)
    skipped = sum(int(suite.attrib.get("skipped", 0)) for suite in suites)
    return "PASS" if tests > 0 and failures == errors == skipped == 0 else "FAIL"


def check_imports() -> str:
    try:
        for module in F1_MODULES:
            importlib.import_module(module)
    except (ImportError, ModuleNotFoundError):
        return "FAIL"
    return "PASS"


def overall_status(checks: dict[str, str]) -> str:
    if all(value == "PASS" for value in checks.values()):
        return "READY"
    if any(value == "BLOCKED" for value in checks.values()):
        return "BLOCKED"
    return "PARTIAL"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--protocol-junit", type=Path)
    parser.add_argument("--agent-access-result", choices=RESULT_CHOICES, default="NOT_RUN")
    parser.add_argument("--container-sanity-result", choices=RESULT_CHOICES, default="NOT_RUN")
    parser.add_argument("--verifier-sanity-result", choices=RESULT_CHOICES, default="NOT_RUN")
    parser.add_argument("--host-storage-path", type=Path, default=Path("/mnt/c"))
    parser.add_argument("--min-storage-gb", type=float, default=50.0)
    parser.add_argument("--json-output", type=Path)
    args = parser.parse_args()

    python_version_ok = "PASS" if sys.version_info >= (3, 11) else "FAIL"
    f1_imports_ok = check_imports()
    f1_protocol_tests_ok = protocol_result(args.protocol_junit)

    if args.host_storage_path.exists():
        disk_free_gb = round(shutil.disk_usage(args.host_storage_path).free / 1024**3, 1)
        benchmark_storage_feasible = "PASS" if disk_free_gb >= args.min_storage_gb else "BLOCKED"
    else:
        disk_free_gb = None
        benchmark_storage_feasible = "UNKNOWN"

    checks = {
        "python_version_ok": python_version_ok,
        "f1_imports_ok": f1_imports_ok,
        "f1_protocol_tests_ok": f1_protocol_tests_ok,
        "agent_access_ok": args.agent_access_result,
        "benchmark_storage_feasible": benchmark_storage_feasible,
        "benchmark_container_sanity": args.container_sanity_result,
        "verifier_sanity": args.verifier_sanity_result,
    }
    status = overall_status(checks)
    payload = {
        **checks,
        "host_storage_path": str(args.host_storage_path),
        "disk_free_gb": disk_free_gb,
        "min_storage_gb": args.min_storage_gb,
        "status": status,
    }
    for key, value in payload.items():
        print(f"{key}={value}")
    if args.json_output is not None:
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        args.json_output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    raise SystemExit({"READY": 0, "PARTIAL": 1, "BLOCKED": 2}[status])


if __name__ == "__main__":
    main()
