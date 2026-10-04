from __future__ import annotations

import pytest

from scripts.check_f1_d1_preflight import protocol_result
from scripts.check_f1_runtime_readiness import classify_readiness, readiness_exit_code


@pytest.mark.parametrize(
    ("status", "expected"),
    [("READY", 0), ("PARTIAL", 1), ("BLOCKED", 2)],
)
def test_readiness_exit_codes(status: str, expected: int):
    assert readiness_exit_code(status) == expected


def test_readiness_classification_distinguishes_runtime_states():
    assert classify_readiness(architecture_ok=True, wsl2_ok=True, required=[True, True]) == "READY"
    assert classify_readiness(architecture_ok=True, wsl2_ok=True, required=[True, False]) == "PARTIAL"
    assert classify_readiness(architecture_ok=True, wsl2_ok=False, required=[True, True]) == "BLOCKED"


def test_protocol_result_reads_pytest_testsuites(tmp_path):
    junit = tmp_path / "result.xml"
    junit.write_text(
        '<testsuites><testsuite tests="12" failures="0" errors="0" skipped="0" /></testsuites>',
        encoding="ascii",
    )
    assert protocol_result(junit) == "PASS"
