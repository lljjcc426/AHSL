from __future__ import annotations

from pathlib import Path

from scripts.f1_d1_evaluator_dependency_recovery import (
    FORK_COMMIT,
    build_shell,
    cache_errors,
    compute_budget,
    deb_errors,
    make_parser,
    map_imports_to_requirements,
    PACKAGE_TEST_SCRIPT,
    static_import_closure,
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
    assert plan["volume_requirements"]["artifact"]["required_start_free_gib"] == 76.6
    assert plan["volume_requirements"]["container"]["required_start_free_gib"] == 76.0


def test_retaining_build_trees_has_a_larger_artifact_peak():
    cleanup = compute_budget(200.0, 200.0, 50.0, True, False)
    retained = compute_budget(200.0, 200.0, 50.0, False, False)

    assert retained["volume_requirements"]["artifact"]["required_start_free_gib"] > cleanup[
        "volume_requirements"
    ]["artifact"]["required_start_free_gib"]


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
    assert "ninja -C /work/llvm-build -j\"$JOBS\" install" in script
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
