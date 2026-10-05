from __future__ import annotations

import os
from pathlib import Path
import shutil
import subprocess

from scripts.f1_d1_evaluator_dependency_recovery import (
    FORK_COMMIT,
    build_shell,
    cache_errors,
    compute_budget,
    compute_remaining_budget,
    deb_errors,
    make_parser,
    map_imports_to_requirements,
    lldb_profile_script,
    PACKAGE_TEST_SCRIPT,
    RecoveryError,
    require_capacity,
    static_import_closure,
    select_build_stage,
    TARGETS,
)


def test_cleanup_budget_reports_each_host_volume_shortfall():
    plan = compute_budget(
        artifact_free_gib=64.4,
        container_free_gib=46.5,
        reserve_gib=50.0,
        cleanup_successful_work=True,
        same_host_volume=False,
    )

    assert plan["status"] == "BLOCKED"
    assert "role_occupancy_gib" in plan["stage_rows"][0]
    assert "incremental_role_gib" not in plan["stage_rows"][0]
    assert plan["volume_requirements"]["artifact"]["required_start_free_gib"] == 76.6
    assert plan["volume_requirements"]["container"]["required_start_free_gib"] == 76.0


def test_retaining_build_trees_has_a_larger_artifact_peak():
    cleanup = compute_budget(200.0, 200.0, 50.0, True, False)
    retained = compute_budget(200.0, 200.0, 50.0, False, False)

    assert retained["volume_requirements"]["artifact"]["required_start_free_gib"] > cleanup[
        "volume_requirements"
    ]["artifact"]["required_start_free_gib"]


def test_remaining_budget_subtracts_only_confirmed_retained_roles_on_split_volumes():
    plan = compute_remaining_budget(
        artifact_free_gib=75.0,
        container_free_gib=60.0,
        reserve_gib=50.0,
        cleanup_successful_work=True,
        same_host_volume=False,
        current_stage="build-second",
        confirmed_retained_gib={"cache": 4.0, "logs": 0.25, "container": 3.0},
    )

    row = plan["stage_rows"][0]
    assert row["incremental_role_gib"] == {
        "work": 14.0,
        "cache": 3.0,
        "logs": 0.25,
        "container": 2.0,
    }
    assert row["artifact_required_start_free_gib"] == 72.35
    assert row["container_required_start_free_gib"] == 56.0


def test_remaining_budget_combines_pending_roles_when_paths_share_a_host_volume():
    plan = compute_remaining_budget(
        artifact_free_gib=80.0,
        container_free_gib=80.0,
        reserve_gib=50.0,
        cleanup_successful_work=True,
        same_host_volume=True,
        current_stage="build-second",
        confirmed_retained_gib={"cache": 4.0, "logs": 0.25, "container": 3.0},
    )

    assert plan["stage_rows"][0]["combined_required_start_free_gib"] == 78.35


def test_resume_at_package_does_not_charge_completed_cache_and_container_again():
    plan = compute_remaining_budget(
        artifact_free_gib=70.0,
        container_free_gib=55.0,
        reserve_gib=50.0,
        cleanup_successful_work=True,
        same_host_volume=False,
        current_stage="package",
        confirmed_retained_gib={"cache": 7.0, "logs": 0.5, "container": 5.0},
    )

    row = plan["stage_rows"][0]
    assert row["incremental_role_gib"] == {
        "work": 5.0,
        "cache": 0.0,
        "output": 2.0,
        "logs": 0.0,
        "container": 0.0,
    }
    assert row["artifact_required_start_free_gib"] == 61.5
    assert row["container_required_start_free_gib"] == 50.0


def test_capacity_gate_checks_subsequent_incremental_peak():
    remaining = compute_remaining_budget(
        artifact_free_gib=74.0,
        container_free_gib=80.0,
        reserve_gib=50.0,
        cleanup_successful_work=True,
        same_host_volume=False,
        current_stage="driver-dependencies",
        confirmed_retained_gib={},
    )

    assert remaining["stage_rows"][0]["volume_status"]["artifact"]["status"] == "PASS"
    try:
        require_capacity({"remaining_execution_plan": remaining}, "driver-dependencies")
    except RecoveryError as exc:
        assert "current and subsequent" in str(exc)
    else:
        raise AssertionError("future blocked stage must block large I/O")


def test_build_stage_distinguishes_first_second_and_completed_target():
    assert select_build_stage("20.04", set()) == "build-first"
    assert select_build_stage("16.04", {"20.04"}) == "build-second"
    assert select_build_stage("20.04", {"20.04"}) is None


def test_incomplete_cache_is_not_accepted(tmp_path: Path):
    rootfs = tmp_path / "rootfs"
    rootfs.mkdir()

    errors = cache_errors(rootfs)

    assert errors
    assert any("COMPLETE.json" in error for error in errors)


def test_empty_deb_is_not_accepted(tmp_path: Path):
    package = tmp_path / "differential-debugging-deps-16.04.deb"
    package.touch()

    assert deb_errors(package) == [f"missing_or_empty:{package}"]


def test_build_command_keeps_resources_explicit_and_does_not_mask_install_failure():
    script = build_shell(TARGETS["16.04"])

    assert '${JOBS:?JOBS must be set}' in script
    assert "nproc" not in script
    assert "sudo" not in script
    assert "/usr/local/python37/bin/python3.7 -c 'import ctypes, sqlite3, ssl" in script
    assert "ninja -C /work/llvm-build -j\"$JOBS\" lldb lldb-server" in script
    assert "install-lldb-python-scripts" in script
    assert "install-clang-resource-headers" in script
    assert "ninja -C /work/llvm-build -j\"$JOBS\" install\n" not in script
    assert "|| true" not in script
    assert FORK_COMMIT == "8a98628dc7941972c96ffac5e3f8fed839ad336a"


def test_cli_exposes_all_recovery_stages():
    choices = make_parser()._subparsers._group_actions[0].choices

    assert {
        "plan",
        "driver-check",
        "driver-sync",
        "prepare",
        "build",
        "package",
        "test",
    } <= set(choices)


def test_package_test_installs_its_inspection_tool():
    assert "apt-get install -y -qq file /tmp/deps.deb" in PACKAGE_TEST_SCRIPT


def test_lldb_profile_script_runs_under_set_u_for_unset_empty_and_existing_values():
    if os.name == "nt":
        candidate = Path(r"C:\Program Files\Git\bin\bash.exe")
        bash = str(candidate) if candidate.is_file() else None
    else:
        bash = shutil.which("bash")
    assert bash is not None, "A real Bash executable is required for this regression test"

    profile = lldb_profile_script("/actual/lldb/site-packages")
    cases = (
        (
            "unset PYTHONPATH LD_LIBRARY_PATH",
            "/actual/lldb/site-packages|/usr/local/lldb13/lib:/usr/local/python37/lib",
        ),
        (
            "export PYTHONPATH='' LD_LIBRARY_PATH=''",
            "/actual/lldb/site-packages|/usr/local/lldb13/lib:/usr/local/python37/lib",
        ),
        (
            "export PYTHONPATH='/existing/python' LD_LIBRARY_PATH='/existing/lib'",
            "/actual/lldb/site-packages:/existing/python|"
            "/usr/local/lldb13/lib:/usr/local/python37/lib:/existing/lib",
        ),
    )
    for setup, expected in cases:
        environment = os.environ.copy()
        environment.pop("PYTHONPATH", None)
        environment.pop("LD_LIBRARY_PATH", None)
        result = subprocess.run(
            [
                bash,
                "--noprofile",
                "--norc",
                "-c",
                "set -u\n"
                + setup
                + "\n"
                + profile
                + 'printf "%s|%s" "$PYTHONPATH" "$LD_LIBRARY_PATH"',
            ],
            env=environment,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        assert result.returncode == 0, result.stderr
        assert result.stdout == expected


def test_static_import_closure_separates_local_and_external_modules(tmp_path: Path):
    package = tmp_path / "sample"
    package.mkdir()
    (package / "__init__.py").write_text("", encoding="utf-8")
    (package / "entry.py").write_text(
        "import json\nimport yaml\nfrom . import helper\n",
        encoding="utf-8",
    )
    (package / "helper.py").write_text("import boto3\n", encoding="utf-8")

    closure = static_import_closure(tmp_path, "sample.entry")

    assert closure["external_imports"] == ["boto3", "yaml"]
    assert closure["unresolved_local_modules"] == []
    assert set(closure["visited_local_modules"]) == {"sample", "sample.entry", "sample.helper"}


def test_import_mapping_distinguishes_direct_transitive_and_undeclared():
    mapped = map_imports_to_requirements(
        ["botocore", "pkg_resources", "requests"],
        ["boto3==1.37.31", "setuptools==78.1.1"],
    )

    assert mapped == [
        {"module": "botocore", "coverage": "transitive", "requirement": "boto3==1.37.31"},
        {"module": "pkg_resources", "coverage": "direct", "requirement": "setuptools==78.1.1"},
        {"module": "requests", "coverage": "undeclared", "requirement": ""},
    ]
