"""Recover AutoPatch evaluator packages from pinned source releases.

The build sequence is adapted from safety-research/PurpleLlama commit
8a98628dc7941972c96ffac5e3f8fed839ad336a, under the MIT license in that
repository's CybersecurityBenchmarks directory. See the project source note
for attribution and the exact changes made here.
"""

from __future__ import annotations

import argparse
import ast
from dataclasses import dataclass
from datetime import datetime, timezone
import importlib.metadata
import importlib.util
import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
import tarfile
import urllib.request
import uuid


GIB = 1024**3
MINIMUM_RESERVE_GIB = 50.0
FORK_COMMIT = "8a98628dc7941972c96ffac5e3f8fed839ad336a"
LLVM_VERSION = "13.0.1"
PYTHON_VERSION = "3.7.17"
CMAKE_VERSION = "3.20.0"


@dataclass(frozen=True)
class SourceArchive:
    filename: str
    url: str


@dataclass(frozen=True)
class Target:
    release: str
    image: str
    cache_name: str
    package_name: str
    needs_bootstrap_cmake: bool


SOURCES = (
    SourceArchive(
        f"llvmorg-{LLVM_VERSION}.tar.gz",
        f"https://github.com/llvm/llvm-project/archive/refs/tags/llvmorg-{LLVM_VERSION}.tar.gz",
    ),
    SourceArchive(
        f"Python-{PYTHON_VERSION}.tgz",
        f"https://www.python.org/ftp/python/{PYTHON_VERSION}/Python-{PYTHON_VERSION}.tgz",
    ),
    SourceArchive(
        f"cmake-{CMAKE_VERSION}.tar.gz",
        f"https://github.com/Kitware/CMake/releases/download/v{CMAKE_VERSION}/cmake-{CMAKE_VERSION}.tar.gz",
    ),
)

TARGETS = {
    "16.04": Target(
        release="16.04",
        image="docker.io/library/ubuntu:16.04",
        cache_name="ubuntu-16.04",
        package_name="differential-debugging-deps-16.04.deb",
        needs_bootstrap_cmake=True,
    ),
    "20.04": Target(
        release="20.04",
        image="docker.io/library/ubuntu:20.04",
        cache_name="ubuntu-20.04",
        package_name="differential-debugging-deps-20.04.deb",
        needs_bootstrap_cmake=False,
    ),
}

# Values are planning bounds in GiB, not measured guarantees. The active build
# allowance is 14 GiB per target: the fork reports roughly 10 GiB of build
# artifacts, with source extraction and install staging accounted for here.
# The separate margins below cover remaining uncertainty. Each row is maximum
# retained plus transient occupancy. The container row is cumulative because
# deleting files inside a WSL VHDX does not necessarily return host space
# without a separately authorized compaction.
CLEANUP_STAGE_ROLES_GIB = {
    "driver-dependencies": {"cache": 0.5, "logs": 0.1, "container": 0.75},
    "prepare": {"cache": 3.0, "logs": 0.1, "container": 1.0},
    "build-first": {"work": 14.0, "cache": 4.0, "logs": 0.25, "container": 3.0},
    "build-second": {"work": 14.0, "cache": 7.0, "logs": 0.5, "container": 5.0},
    "package": {"work": 5.0, "cache": 7.0, "output": 2.0, "logs": 0.5, "container": 5.0},
    "package-test": {"cache": 7.0, "output": 2.0, "logs": 0.75, "container": 7.0},
    "official-derived-images": {"cache": 7.0, "output": 2.0, "logs": 0.75, "container": 14.0},
    "evaluator-10445": {"cache": 7.0, "output": 2.0, "logs": 1.0, "container": 22.0},
}

RETAIN_STAGE_ROLES_GIB = {
    **CLEANUP_STAGE_ROLES_GIB,
    "build-second": {"work": 28.0, "cache": 7.0, "logs": 0.5, "container": 5.0},
    "package": {"work": 35.0, "cache": 7.0, "output": 2.0, "logs": 0.5, "container": 5.0},
    "package-test": {"work": 35.0, "cache": 7.0, "output": 2.0, "logs": 0.75, "container": 7.0},
    "official-derived-images": {"work": 35.0, "cache": 7.0, "output": 2.0, "logs": 0.75, "container": 14.0},
    "evaluator-10445": {"work": 35.0, "cache": 7.0, "output": 2.0, "logs": 1.0, "container": 22.0},
}

ROLE_MARGIN_GIB = {
    "work": 4.0,
    "cache": 1.0,
    "output": 0.5,
    "logs": 0.1,
    "container": 4.0,
}


class RecoveryError(RuntimeError):
    pass


@dataclass(frozen=True)
class RecoveryPaths:
    work: Path
    cache: Path
    output: Path
    logs: Path
    artifact_host_storage: Path
    container_store: Path
    container_host_storage: Path


class StageLog:
    def __init__(self, logs_dir: Path, stage: str) -> None:
        logs_dir.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
        self.path = logs_dir / f"{stamp}_{stage}.log"
        self.exit_path = logs_dir / f"{stamp}_{stage}.exit_code"
        self.handle = self.path.open("x", encoding="utf-8")

    def write(self, message: str) -> None:
        print(message)
        self.handle.write(message + "\n")
        self.handle.flush()

    def run(self, command: list[str], cwd: Path | None = None) -> None:
        self.write(f"$ {shlex.join(command)}")
        process = subprocess.Popen(
            command,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        assert process.stdout is not None
        for line in process.stdout:
            print(line, end="")
            self.handle.write(line)
            self.handle.flush()
        returncode = process.wait()
        self.write(f"command_exit_code={returncode}")
        if returncode != 0:
            raise RecoveryError(f"Command failed with exit code {returncode}")

    def close(self, exit_code: int) -> None:
        self.handle.close()
        self.exit_path.write_text(f"{exit_code}\n", encoding="ascii")


def nearest_existing(path: Path) -> Path:
    candidate = path.resolve()
    while not candidate.exists():
        parent = candidate.parent
        if parent == candidate:
            raise RecoveryError(f"No existing parent for {path}")
        candidate = parent
    return candidate


def same_filesystem(left: Path, right: Path) -> bool:
    return nearest_existing(left).stat().st_dev == nearest_existing(right).stat().st_dev


def free_gib(path: Path) -> float:
    return shutil.disk_usage(nearest_existing(path)).free / GIB


def validate_paths(paths: RecoveryPaths) -> None:
    for artifact_path in (paths.work, paths.cache, paths.output, paths.logs):
        if not same_filesystem(artifact_path, paths.artifact_host_storage):
            raise RecoveryError(
                f"{artifact_path} is not backed by the declared artifact host path "
                f"{paths.artifact_host_storage}"
            )


def compute_budget(
    artifact_free_gib: float,
    container_free_gib: float,
    reserve_gib: float,
    cleanup_successful_work: bool,
    same_host_volume: bool,
) -> dict[str, object]:
    stages = CLEANUP_STAGE_ROLES_GIB if cleanup_successful_work else RETAIN_STAGE_ROLES_GIB
    rows: list[dict[str, object]] = []
    maxima: dict[str, float] = {"artifact": 0.0, "container": 0.0, "combined": 0.0}

    for stage, roles in stages.items():
        artifact_roles = {key: value for key, value in roles.items() if key != "container"}
        artifact_peak = sum(artifact_roles.values())
        artifact_margin = sum(ROLE_MARGIN_GIB[key] for key, value in artifact_roles.items() if value > 0)
        container_peak = roles.get("container", 0.0)
        container_margin = ROLE_MARGIN_GIB["container"] if container_peak > 0 else 0.0
        artifact_required = reserve_gib + artifact_peak + artifact_margin
        container_required = reserve_gib + container_peak + container_margin
        combined_required = reserve_gib + artifact_peak + artifact_margin + container_peak + container_margin
        maxima["artifact"] = max(maxima["artifact"], artifact_required)
        maxima["container"] = max(maxima["container"], container_required)
        maxima["combined"] = max(maxima["combined"], combined_required)
        if same_host_volume:
            stage_volumes = {
                "combined": {
                    "free_gib": round(min(artifact_free_gib, container_free_gib), 2),
                    "required_start_free_gib": round(combined_required, 2),
                    "status": (
                        "PASS"
                        if min(artifact_free_gib, container_free_gib) >= combined_required
                        else "BLOCKED"
                    ),
                }
            }
        else:
            stage_volumes = {
                "artifact": {
                    "free_gib": round(artifact_free_gib, 2),
                    "required_start_free_gib": round(artifact_required, 2),
                    "status": "PASS" if artifact_free_gib >= artifact_required else "BLOCKED",
                },
                "container": {
                    "free_gib": round(container_free_gib, 2),
                    "required_start_free_gib": round(container_required, 2),
                    "status": "PASS" if container_free_gib >= container_required else "BLOCKED",
                },
            }
        rows.append(
            {
                "stage": stage,
                "role_occupancy_gib": roles,
                "artifact_required_start_free_gib": round(artifact_required, 2),
                "container_required_start_free_gib": round(container_required, 2),
                "combined_required_start_free_gib": round(combined_required, 2),
                "volume_status": stage_volumes,
            }
        )

    if same_host_volume:
        required = maxima["combined"]
        volumes = {
            "combined": {
                "free_gib": round(min(artifact_free_gib, container_free_gib), 2),
                "required_start_free_gib": round(required, 2),
                "additional_free_space_needed_gib": round(
                    max(0.0, required - min(artifact_free_gib, container_free_gib)), 2
                ),
            }
        }
    else:
        volumes = {
            "artifact": {
                "free_gib": round(artifact_free_gib, 2),
                "required_start_free_gib": round(maxima["artifact"], 2),
                "additional_free_space_needed_gib": round(
                    max(0.0, maxima["artifact"] - artifact_free_gib), 2
                ),
            },
            "container": {
                "free_gib": round(container_free_gib, 2),
                "required_start_free_gib": round(maxima["container"], 2),
                "additional_free_space_needed_gib": round(
                    max(0.0, maxima["container"] - container_free_gib), 2
                ),
            },
        }

    status = "PASS" if all(item["additional_free_space_needed_gib"] == 0 for item in volumes.values()) else "BLOCKED"
    return {
        "status": status,
        "reserve_gib": reserve_gib,
        "cleanup_successful_work": cleanup_successful_work,
        "estimate_class": "phase-specific planning bounds, not measured build peaks",
        "source_versions": {
            "python": PYTHON_VERSION,
            "llvm_lldb": LLVM_VERSION,
            "cmake_ubuntu_16_04": CMAKE_VERSION,
        },
        "stage_rows": rows,
        "volume_requirements": volumes,
    }


def budget_for_paths(paths: RecoveryPaths, reserve_gib: float, cleanup: bool) -> dict[str, object]:
    validate_paths(paths)
    same_host_volume = same_filesystem(
        paths.artifact_host_storage, paths.container_host_storage
    )
    plan = compute_budget(
        free_gib(paths.artifact_host_storage),
        free_gib(paths.container_host_storage),
        reserve_gib,
        cleanup,
        same_host_volume,
    )
    plan["paths"] = {
        "work_dir": str(paths.work),
        "cache_dir": str(paths.cache),
        "output_dir": str(paths.output),
        "logs_dir": str(paths.logs),
        "artifact_host_storage_path": str(paths.artifact_host_storage),
        "container_store": str(paths.container_store),
        "container_host_storage_path": str(paths.container_host_storage),
    }
    return plan


def require_capacity(plan: dict[str, object], command: str) -> None:
    stage_name = {
        "driver-sync": "driver-dependencies",
        "prepare": "prepare",
        "build": "build-second",
        "package": "package",
        "test": "package-test",
    }[command]
    stage_rows = plan["stage_rows"]
    assert isinstance(stage_rows, list)
    row = next(item for item in stage_rows if item["stage"] == stage_name)
    volume_status = row["volume_status"]
    assert isinstance(volume_status, dict)
    if any(item["status"] != "PASS" for item in volume_status.values()):
        raise RecoveryError(
            f"Resource plan is BLOCKED before {command} at budget stage {stage_name}; "
            "inspect the plan output and do not start large I/O"
        )


def validate_archive(path: Path) -> None:
    if not path.is_file() or path.stat().st_size == 0:
        raise RecoveryError(f"Missing or empty source archive: {path}")
    try:
        with tarfile.open(path, "r:gz") as archive:
            if archive.next() is None:
                raise RecoveryError(f"Empty source archive: {path}")
    except tarfile.TarError as exc:
        raise RecoveryError(f"Invalid source archive {path}: {exc}") from exc


def download_source(source: SourceArchive, cache_dir: Path, log: StageLog) -> None:
    destination = cache_dir / "sources" / source.filename
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        validate_archive(destination)
        log.write(f"source_cache=PASS path={destination}")
        return
    partial = destination.with_suffix(destination.suffix + ".part")
    if partial.exists():
        raise RecoveryError(f"Incomplete prior download exists: {partial}")
    log.write(f"download_url={source.url}")
    try:
        urllib.request.urlretrieve(source.url, partial)
        validate_archive(partial)
        partial.rename(destination)
    except Exception:
        log.write(f"incomplete_download_retained={partial}")
        raise
    log.write(f"source_download=PASS bytes={destination.stat().st_size} path={destination}")


def podman_image_exists(image: str) -> bool:
    return subprocess.run(
        ["podman", "image", "exists", image],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    ).returncode == 0


def extract_libstdcpp(paths: RecoveryPaths, log: StageLog) -> None:
    destination = paths.cache / "runtime" / "libstdc++.so.6"
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        if destination.stat().st_size == 0:
            raise RecoveryError(f"Existing libstdc++ cache is empty: {destination}")
        log.write(f"libstdcpp_cache=PASS path={destination}")
        return
    container_name = f"f1-deps-libstdcpp-{uuid.uuid4().hex[:12]}"
    log.run(
        [
            "podman",
            "create",
            "--pull=never",
            "--name",
            container_name,
            TARGETS["20.04"].image,
            "true",
        ]
    )
    try:
        log.run(
            [
                "podman",
                "cp",
                f"{container_name}:/usr/lib/x86_64-linux-gnu/libstdc++.so.6",
                str(destination),
            ]
        )
    finally:
        log.run(["podman", "rm", container_name])
    if destination.stat().st_size == 0:
        raise RecoveryError("Extracted libstdc++.so.6 is empty")


def prepare(paths: RecoveryPaths, log: StageLog) -> None:
    for source in SOURCES:
        download_source(source, paths.cache, log)
    for target in TARGETS.values():
        if podman_image_exists(target.image):
            log.write(f"image_cache=PASS image={target.image}")
        else:
            log.run(["podman", "pull", target.image])
    extract_libstdcpp(paths, log)


def build_shell(target: Target) -> str:
    if target.needs_bootstrap_cmake:
        cmake_setup = f"""
tar -xzf /cache/sources/cmake-{CMAKE_VERSION}.tar.gz -C /work/src
cd /work/src/cmake-{CMAKE_VERSION}
./bootstrap --parallel="$JOBS" -- -DCMAKE_BUILD_TYPE=Release
make -j"$JOBS"
make install
CMAKE=/usr/local/bin/cmake
"""
        compiler_setup = """
apt-get install -y -qq software-properties-common
add-apt-repository ppa:ubuntu-toolchain-r/test -y
apt-get update -qq
apt-get install -y -qq gcc-7 g++-7
update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-7 100
update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-7 100
"""
    else:
        cmake_setup = "CMAKE=/usr/bin/cmake\n"
        compiler_setup = ""

    return f"""#!/bin/bash
set -euo pipefail
export DEBIAN_FRONTEND=noninteractive
: "${{JOBS:?JOBS must be set}}"
apt-get update -qq
apt-get install -y -qq build-essential ninja-build swig cmake wget curl \\
    zlib1g-dev libssl-dev libffi-dev libbz2-dev libreadline-dev \\
    libsqlite3-dev libncurses5-dev libncursesw5-dev libedit-dev \\
    libxml2-dev libxmlsec1-dev liblzma-dev xz-utils tk-dev python3-dev
{compiler_setup}
mkdir -p /work/src /work/python-build /work/llvm-build /stage
tar -xzf /cache/sources/Python-{PYTHON_VERSION}.tgz -C /work/src
cd /work/src/Python-{PYTHON_VERSION}
./configure --prefix=/usr/local/python37 --with-ensurepip=install \\
    --enable-shared --disable-test-modules --quiet
make -j"$JOBS"
make install DESTDIR=/stage
ln -s /stage/usr/local/python37 /usr/local/python37
{cmake_setup}
tar -xzf /cache/sources/llvmorg-{LLVM_VERSION}.tar.gz -C /work/src
"$CMAKE" -G Ninja \\
    -S /work/src/llvm-project-llvmorg-{LLVM_VERSION}/llvm \\
    -B /work/llvm-build \\
    -DCMAKE_BUILD_TYPE=Release \\
    -DCMAKE_INSTALL_PREFIX=/usr/local/lldb13 \\
    -DLLVM_ENABLE_PROJECTS='clang;lldb' \\
    -DLLDB_ENABLE_PYTHON=ON \\
    -DPython3_EXECUTABLE=/usr/local/python37/bin/python3.7 \\
    -DPython3_LIBRARY=/usr/local/python37/lib/libpython3.7m.so \\
    -DPython3_INCLUDE_DIR=/usr/local/python37/include/python3.7m \\
    -DPython3_ROOT_DIR=/usr/local/python37 \\
    -DPYTHON_EXECUTABLE=/usr/local/python37/bin/python3.7 \\
    -DPYTHON_LIBRARY=/usr/local/python37/lib/libpython3.7m.so \\
    -DPYTHON_INCLUDE_DIR=/usr/local/python37/include/python3.7m \\
    -DLLVM_TARGETS_TO_BUILD=X86 \\
    -DLLVM_ENABLE_ASSERTIONS=OFF
ninja -C /work/llvm-build -j"$JOBS" lldb
DESTDIR=/stage ninja -C /work/llvm-build -j"$JOBS" install
test -x /stage/usr/local/python37/bin/python3.7
test -x /stage/usr/local/lldb13/bin/lldb
find /stage/usr/local/lldb13 -path '*/site-packages/lldb/__init__.py' -print -quit | grep -q .
find /stage/usr/local/lldb13 -path '*/site-packages/lldb/_lldb*.so' -print -quit | grep -q .
"""


def cache_errors(cache_root: Path, require_marker: bool = True) -> list[str]:
    expected = (
        cache_root / "usr/local/python37/bin/python3.7",
        cache_root / "usr/local/python37/lib/libpython3.7m.so",
        cache_root / "usr/local/lldb13/bin/lldb",
    )
    errors = [f"missing:{path}" for path in expected if not path.is_file() or path.stat().st_size == 0]
    lldb_package = list(cache_root.glob("usr/local/lldb13/**/site-packages/lldb/__init__.py"))
    lldb_extension = list(cache_root.glob("usr/local/lldb13/**/site-packages/lldb/_lldb*.so"))
    if not lldb_package:
        errors.append("missing:lldb/__init__.py")
    if not lldb_extension or all(path.stat().st_size == 0 for path in lldb_extension):
        errors.append("missing:lldb/_lldb*.so")
    marker = cache_root.parent / "COMPLETE.json"
    if require_marker and not marker.is_file():
        errors.append(f"missing:{marker}")
    return errors


def target_cache(paths: RecoveryPaths, target: Target) -> Path:
    return paths.cache / "builds" / target.cache_name


def build_target(
    paths: RecoveryPaths,
    target: Target,
    jobs: int,
    memory_gib: float,
    cleanup_successful_work: bool,
    log: StageLog,
) -> None:
    final_cache = target_cache(paths, target)
    if final_cache.exists():
        errors = cache_errors(final_cache / "rootfs")
        if errors:
            raise RecoveryError(
                "Existing target cache is incomplete; choose a new cache directory or explicitly remove "
                f"this task cache: {final_cache}; errors={errors}"
            )
        log.write(f"build_cache=PASS target={target.release} path={final_cache}")
        return

    for source in SOURCES:
        validate_archive(paths.cache / "sources" / source.filename)
    if not podman_image_exists(target.image):
        raise RecoveryError(f"Prepared image is missing: {target.image}")

    runs_root = paths.work / "runs"
    runs_root.mkdir(parents=True, exist_ok=True)
    run_dir = runs_root / f"build-{target.cache_name}-{uuid.uuid4().hex}"
    run_dir.mkdir()
    script_path = run_dir / "build.sh"
    script_path.write_text(build_shell(target), encoding="utf-8", newline="\n")

    staging = paths.cache / "builds" / f".staging-{target.cache_name}-{uuid.uuid4().hex}"
    staging.mkdir(parents=True)
    (staging / "rootfs").mkdir()
    log.run(
        [
            "podman",
            "run",
            "--rm",
            "--pull=never",
            f"--cpus={jobs}",
            f"--memory={memory_gib}g",
            "-e",
            f"JOBS={jobs}",
            "-v",
            f"{paths.cache}:/cache:ro",
            "-v",
            f"{run_dir}:/work",
            "-v",
            f"{staging / 'rootfs'}:/stage",
            "-v",
            f"{script_path}:/build.sh:ro",
            target.image,
            "bash",
            "/build.sh",
        ]
    )
    errors = cache_errors(staging / "rootfs", require_marker=False)
    if errors:
        raise RecoveryError(f"Build finished without complete cache artifacts: {errors}")
    (staging / "COMPLETE.json").write_text(
        json.dumps(
            {
                "target": target.release,
                "python": PYTHON_VERSION,
                "llvm_lldb": LLVM_VERSION,
                "source_fork_commit": FORK_COMMIT,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    staging.rename(final_cache)
    log.write(f"build_cache=PASS target={target.release} path={final_cache}")
    if cleanup_successful_work:
        shutil.rmtree(run_dir)
        log.write(f"deleted_task_owned_successful_work={run_dir}")


def write_package_metadata(rootfs: Path, target: Target) -> None:
    libstdcpp_source = rootfs.parent / "libstdc++.so.6"
    lldb_lib = rootfs / "usr/local/lldb13/lib"
    lldb_lib.mkdir(parents=True, exist_ok=True)
    shutil.copy2(libstdcpp_source, lldb_lib / "libstdc++.so.6")

    bin_dir = rootfs / "usr/bin"
    bin_dir.mkdir(parents=True, exist_ok=True)
    for name, destination in (
        ("python3.7", "/usr/local/python37/bin/python3.7"),
        ("lldb", "/usr/local/lldb13/bin/lldb"),
        ("lldb-13", "/usr/local/lldb13/bin/lldb"),
    ):
        os.symlink(destination, bin_dir / name)

    bindings = list(rootfs.glob("usr/local/lldb13/**/site-packages/lldb"))
    if len(bindings) != 1:
        raise RecoveryError(f"Expected one LLDB Python package, found {len(bindings)}")
    python_site = rootfs / "usr/local/python37/lib/python3.7/site-packages"
    python_site.mkdir(parents=True, exist_ok=True)
    os.symlink(
        "/" + bindings[0].relative_to(rootfs).as_posix(),
        python_site / "lldb",
    )

    ldconfig_dir = rootfs / "etc/ld.so.conf.d"
    ldconfig_dir.mkdir(parents=True, exist_ok=True)
    (ldconfig_dir / "python37.conf").write_text("/usr/local/python37/lib\n", encoding="ascii")
    (ldconfig_dir / "lldb13.conf").write_text("/usr/local/lldb13/lib\n", encoding="ascii")

    profile_dir = rootfs / "etc/profile.d"
    profile_dir.mkdir(parents=True, exist_ok=True)
    (profile_dir / "lldb-python.sh").write_text(
        'export PYTHONPATH="/usr/local/lldb13/lib/python3.7/site-packages:$PYTHONPATH"\n'
        'export LD_LIBRARY_PATH="/usr/local/lldb13/lib:/usr/local/python37/lib:$LD_LIBRARY_PATH"\n',
        encoding="ascii",
    )

    debian_dir = rootfs / "DEBIAN"
    debian_dir.mkdir(parents=True, exist_ok=True)
    (debian_dir / "control").write_text(
        "\n".join(
            (
                "Package: differential-debugging-deps",
                "Version: 1.0.0+source1",
                "Section: devel",
                "Priority: optional",
                "Architecture: amd64",
                "Maintainer: AHSL evaluator recovery",
                "Depends: libxml2, libedit2, zlib1g, libncurses5",
                "Description: Source-built LLDB 13 and Python 3.7 for AutoPatch",
                f" Built for Ubuntu {target.release}; not byte-identical to the unavailable official package.",
                "",
            )
        ),
        encoding="ascii",
    )
    postinst = debian_dir / "postinst"
    postinst.write_text("#!/bin/sh\nset -e\nldconfig\n", encoding="ascii")
    postinst.chmod(0o755)


def deb_errors(path: Path, runner=subprocess.run) -> list[str]:
    if not path.is_file() or path.stat().st_size == 0:
        return [f"missing_or_empty:{path}"]
    errors: list[str] = []
    for field, expected in (
        ("Package", "differential-debugging-deps"),
        ("Version", "1.0.0+source1"),
        ("Architecture", "amd64"),
    ):
        result = runner(
            ["dpkg-deb", "--field", str(path), field],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        if result.returncode != 0 or result.stdout.strip() != expected:
            errors.append(f"invalid_{field.lower()}:{result.stdout.strip()}")
    listing = runner(
        ["dpkg-deb", "--contents", str(path)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    required = ("usr/local/python37/bin/python3.7", "usr/local/lldb13/bin/lldb", "site-packages/lldb/")
    if listing.returncode != 0:
        errors.append("cannot_list_package")
    else:
        errors.extend(f"missing_content:{item}" for item in required if item not in listing.stdout)
    return errors


def package_both(paths: RecoveryPaths, cleanup_successful_work: bool, log: StageLog) -> None:
    runtime_lib = paths.cache / "runtime/libstdc++.so.6"
    if not runtime_lib.is_file() or runtime_lib.stat().st_size == 0:
        raise RecoveryError(f"Prepared runtime library is missing: {runtime_lib}")
    for target in TARGETS.values():
        cache = target_cache(paths, target)
        errors = cache_errors(cache / "rootfs")
        if errors:
            raise RecoveryError(f"Incomplete build cache for {target.release}: {errors}")
        output = paths.output / target.package_name
        if output.exists():
            raise RecoveryError(f"Refusing to overwrite existing package: {output}")

    run_dir = paths.work / "runs" / f"package-{uuid.uuid4().hex}"
    run_dir.mkdir(parents=True)
    paths.output.mkdir(parents=True, exist_ok=True)
    for target in TARGETS.values():
        package_root = run_dir / target.cache_name
        rootfs = package_root / "rootfs"
        shutil.copytree(target_cache(paths, target) / "rootfs", rootfs, symlinks=True)
        shutil.copy2(runtime_lib, package_root / "libstdc++.so.6")
        write_package_metadata(rootfs, target)
        candidate = package_root / target.package_name
        log.run(["dpkg-deb", "--root-owner-group", "--build", str(rootfs), str(candidate)])
        errors = deb_errors(candidate)
        if errors:
            raise RecoveryError(f"Invalid generated package {candidate}: {errors}")
        candidate.rename(paths.output / target.package_name)
        log.write(f"package=PASS target={target.release} path={paths.output / target.package_name}")
    if cleanup_successful_work:
        shutil.rmtree(run_dir)
        log.write(f"deleted_task_owned_successful_work={run_dir}")


PACKAGE_TEST_SCRIPT = r"""#!/bin/bash
set -euo pipefail
dpkg_arch=$(dpkg-deb --field /tmp/deps.deb Architecture)
test "$dpkg_arch" = amd64
test "$(dpkg-deb --field /tmp/deps.deb Version)" = 1.0.0+source1
apt-get update -qq
apt-get install -y -qq file /tmp/deps.deb
test "$(dpkg-query -W -f='${Architecture}' differential-debugging-deps)" = amd64
file /usr/local/lldb13/bin/lldb | grep -Eq 'ELF 64-bit.*x86-64'
/usr/local/python37/bin/python3.7 --version | grep -q '3.7.17'
/usr/local/lldb13/bin/lldb --version | grep -Eq '13\.0\.1|version 13'
! ldd /usr/local/lldb13/bin/lldb | grep -q 'not found'
source /etc/profile.d/lldb-python.sh
python3.7 -c 'import lldb; assert "13" in lldb.SBDebugger.GetVersionString(); d=lldb.SBDebugger.Create(); assert d.IsValid(); t=d.CreateTarget("/bin/true"); assert t.IsValid(); lldb.SBDebugger.Terminate()'
lldb --batch -o 'target create /bin/true' -o run -o 'process status' | grep -q 'exited with status = 0'
"""


def test_packages(
    paths: RecoveryPaths,
    memory_gib: float,
    cleanup_successful_work: bool,
    log: StageLog,
) -> None:
    run_dir = paths.work / "runs" / f"test-{uuid.uuid4().hex}"
    run_dir.mkdir(parents=True)
    test_script = run_dir / "test-package.sh"
    test_script.write_text(PACKAGE_TEST_SCRIPT, encoding="utf-8", newline="\n")
    for target in TARGETS.values():
        package = paths.output / target.package_name
        errors = deb_errors(package)
        if errors:
            raise RecoveryError(f"Package precheck failed for {package}: {errors}")
        if not podman_image_exists(target.image):
            raise RecoveryError(f"Prepared test image is missing: {target.image}")
        log.run(
            [
                "podman",
                "run",
                "--rm",
                "--pull=never",
                "--cap-add=SYS_PTRACE",
                "--security-opt",
                "seccomp=unconfined",
                f"--memory={memory_gib}g",
                "-v",
                f"{package}:/tmp/deps.deb:ro",
                "-v",
                f"{test_script}:/tmp/test-package.sh:ro",
                target.image,
                "bash",
                "/tmp/test-package.sh",
            ]
        )
        log.write(f"package_test=PASS target={target.release}")
    if cleanup_successful_work:
        shutil.rmtree(run_dir)
        log.write(f"deleted_task_owned_successful_work={run_dir}")


IMPORT_DISTRIBUTION_OVERRIDES = {
    "PIL": "pillow",
    "pkg_resources": "setuptools",
    "yaml": "pyyaml",
}
TRANSITIVE_IMPORT_PROVIDERS = {
    "botocore": "boto3",
}


def module_source(
    repository_root: Path,
    module: str,
    cache: dict[str, tuple[str, Path, str] | None],
) -> tuple[str, Path, str] | None:
    if module in cache:
        return cache[module]
    base = Path(*module.split("."))
    candidates = (base.with_suffix(".py"), base / "__init__.py")
    for relative in candidates:
        path = repository_root / relative
        if path.is_file():
            result = (path.read_text(encoding="utf-8"), relative, "working_tree")
            cache[module] = result
            return result
    for relative in candidates:
        result = subprocess.run(
            ["git", "-C", str(repository_root), "show", f"HEAD:{relative.as_posix()}"],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
        )
        if result.returncode == 0:
            value = (result.stdout, relative, "git_object")
            cache[module] = value
            return value
    cache[module] = None
    return None


def static_import_closure(repository_root: Path, entry_module: str) -> dict[str, object]:
    local_namespace = entry_module.partition(".")[0]
    pending = [entry_module]
    visited: set[str] = set()
    unresolved_local: set[str] = set()
    external: set[str] = set()
    sources: dict[str, str] = {}
    cache: dict[str, tuple[str, Path, str] | None] = {}

    while pending:
        module = pending.pop()
        if module in visited:
            continue
        loaded = module_source(repository_root, module, cache)
        if loaded is None:
            unresolved_local.add(module)
            continue
        source, relative, origin = loaded
        visited.add(module)
        sources[module] = f"{origin}:{relative.as_posix()}"
        package = module if relative.name == "__init__.py" else module.rpartition(".")[0]
        tree = ast.parse(source, filename=relative.as_posix())

        for node in ast.walk(tree):
            names: list[str] = []
            if isinstance(node, ast.Import):
                names = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom):
                if node.level:
                    relative_name = "." * node.level + (node.module or "")
                    try:
                        base_name = importlib.util.resolve_name(relative_name, package)
                    except ImportError:
                        unresolved_local.add(f"{module}:{relative_name}")
                        continue
                else:
                    base_name = node.module or ""
                if base_name:
                    names.append(base_name)
                    if base_name.partition(".")[0] == local_namespace:
                        for alias in node.names:
                            if alias.name != "*":
                                candidate = f"{base_name}.{alias.name}"
                                if module_source(repository_root, candidate, cache) is not None:
                                    names.append(candidate)
            else:
                continue

            for imported in names:
                top_level = imported.partition(".")[0]
                if top_level in sys.stdlib_module_names or top_level == "__future__":
                    continue
                if top_level == local_namespace:
                    if module_source(repository_root, imported, cache) is None:
                        unresolved_local.add(imported)
                    elif imported not in visited:
                        pending.append(imported)
                else:
                    external.add(top_level)

    return {
        "entry_module": entry_module,
        "visited_local_modules": sorted(visited),
        "module_sources": dict(sorted(sources.items())),
        "unresolved_local_modules": sorted(unresolved_local),
        "external_imports": sorted(external),
    }


def normalize_distribution(name: str) -> str:
    return name.lower().replace("_", "-").replace(".", "-")


def map_imports_to_requirements(
    external_imports: list[str],
    requirement_lines: list[str],
) -> list[dict[str, str]]:
    declared: dict[str, str] = {}
    for line in requirement_lines:
        distribution = line.partition("==")[0]
        declared[normalize_distribution(distribution)] = line

    mapped: list[dict[str, str]] = []
    for module in external_imports:
        distribution = IMPORT_DISTRIBUTION_OVERRIDES.get(module, module)
        normalized = normalize_distribution(distribution)
        if normalized in declared:
            mapped.append(
                {
                    "module": module,
                    "coverage": "direct",
                    "requirement": declared[normalized],
                }
            )
            continue
        provider = TRANSITIVE_IMPORT_PROVIDERS.get(module)
        if provider and normalize_distribution(provider) in declared:
            mapped.append(
                {
                    "module": module,
                    "coverage": "transitive",
                    "requirement": declared[normalize_distribution(provider)],
                }
            )
            continue
        mapped.append({"module": module, "coverage": "undeclared", "requirement": ""})
    return mapped


def sync_driver_dependencies(
    paths: RecoveryPaths,
    purplellama_dir: Path,
    requirements_file: Path,
    json_output: Path | None,
    log: StageLog,
) -> None:
    if sys.prefix == sys.base_prefix:
        raise RecoveryError("driver-sync must run from a dedicated virtual environment")
    if not requirements_file.is_file():
        raise RecoveryError(f"Missing driver requirements file: {requirements_file}")
    pip_cache = paths.cache / "pip"
    pip_cache.mkdir(parents=True, exist_ok=True)
    log.write(f"driver_python={sys.executable}")
    log.write(f"driver_requirements={requirements_file}")
    log.run(
        [
            sys.executable,
            "-m",
            "pip",
            "--disable-pip-version-check",
            "--require-virtualenv",
            "install",
            "--cache-dir",
            str(pip_cache),
            "--requirement",
            str(requirements_file),
        ]
    )
    result = audit_driver(purplellama_dir)
    log.write(json.dumps(result, indent=2))
    if json_output:
        json_output.parent.mkdir(parents=True, exist_ok=True)
        json_output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    if result["autopatching_import"] != "PASS":
        raise RecoveryError("Driver packages installed, but the frozen AutoPatch import still fails")


def audit_driver(purplellama_dir: Path) -> dict[str, object]:
    requirements_path = purplellama_dir / "CybersecurityBenchmarks/requirements.txt"
    if not requirements_path.is_file():
        raise RecoveryError(f"Missing frozen requirements file: {requirements_path}")
    installed: dict[str, str] = {}
    missing: list[str] = []
    mismatched: list[dict[str, str]] = []
    requirement_lines: list[str] = []
    for raw_line in requirements_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        requirement_lines.append(line)
        name, separator, expected = line.partition("==")
        try:
            actual = importlib.metadata.version(name)
            installed[name] = actual
            if separator and actual != expected:
                mismatched.append({"distribution": name, "expected": expected, "actual": actual})
        except importlib.metadata.PackageNotFoundError:
            missing.append(line)
    env = os.environ.copy()
    env["PYTHONPATH"] = str(purplellama_dir)
    import_result = subprocess.run(
        [sys.executable, "-c", "import CybersecurityBenchmarks.benchmark.autopatching_benchmark"],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    closure = static_import_closure(
        purplellama_dir,
        "CybersecurityBenchmarks.benchmark.autopatching_benchmark",
    )
    mapped_imports = map_imports_to_requirements(
        closure["external_imports"],
        requirement_lines,
    )
    repo_head_result = subprocess.run(
        ["git", "-C", str(purplellama_dir), "rev-parse", "HEAD"],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
    )
    return {
        "python": sys.version,
        "sys_executable": sys.executable,
        "repository_head": repo_head_result.stdout.strip() if repo_head_result.returncode == 0 else "UNKNOWN",
        "requirements_path": str(requirements_path),
        "declared_requirement_count": len(installed) + len(missing),
        "installed": installed,
        "missing": missing,
        "version_mismatches": mismatched,
        "autopatch_static_import_closure": closure,
        "autopatch_import_requirement_mapping": mapped_imports,
        "autopatching_import": "PASS" if import_result.returncode == 0 else "FAIL",
        "autopatching_import_stderr": import_result.stderr,
    }


def parse_paths(args: argparse.Namespace) -> RecoveryPaths:
    return RecoveryPaths(
        work=args.work_dir.resolve(),
        cache=args.cache_dir.resolve(),
        output=args.output_dir.resolve(),
        logs=args.logs_dir.resolve(),
        artifact_host_storage=args.artifact_host_storage_path.resolve(),
        container_store=args.container_store.resolve(),
        container_host_storage=args.container_host_storage_path.resolve(),
    )


def add_common_paths(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--work-dir", type=Path, required=True)
    parser.add_argument("--cache-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--logs-dir", type=Path, required=True)
    parser.add_argument("--artifact-host-storage-path", type=Path, required=True)
    parser.add_argument("--container-store", type=Path, required=True)
    parser.add_argument("--container-host-storage-path", type=Path, required=True)
    parser.add_argument("--reserve-gib", type=float, default=MINIMUM_RESERVE_GIB)
    parser.add_argument("--cleanup-successful-work", action="store_true")


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    plan_parser = subparsers.add_parser("plan")
    add_common_paths(plan_parser)
    plan_parser.add_argument("--json-output", type=Path)

    prepare_parser = subparsers.add_parser("prepare")
    add_common_paths(prepare_parser)
    prepare_parser.add_argument("--allow-large-io", action="store_true")

    build_parser = subparsers.add_parser("build")
    add_common_paths(build_parser)
    build_parser.add_argument("--target", choices=TARGETS, required=True)
    build_parser.add_argument("--jobs", type=int, required=True)
    build_parser.add_argument("--memory-gib", type=float, required=True)
    build_parser.add_argument("--allow-large-io", action="store_true")

    package_parser = subparsers.add_parser("package")
    add_common_paths(package_parser)
    package_parser.add_argument("--allow-large-io", action="store_true")

    test_parser = subparsers.add_parser("test")
    add_common_paths(test_parser)
    test_parser.add_argument("--memory-gib", type=float, required=True)
    test_parser.add_argument("--allow-large-io", action="store_true")

    driver_parser = subparsers.add_parser("driver-check")
    driver_parser.add_argument("--logs-dir", type=Path, required=True)
    driver_parser.add_argument("--purplellama-dir", type=Path, required=True)
    driver_parser.add_argument("--json-output", type=Path)

    driver_sync_parser = subparsers.add_parser("driver-sync")
    add_common_paths(driver_sync_parser)
    driver_sync_parser.add_argument("--purplellama-dir", type=Path, required=True)
    driver_sync_parser.add_argument("--requirements-file", type=Path, required=True)
    driver_sync_parser.add_argument("--json-output", type=Path)
    driver_sync_parser.add_argument("--allow-network", action="store_true")
    return parser


def main() -> None:
    args = make_parser().parse_args()
    log = StageLog(args.logs_dir.resolve(), args.command)
    exit_code = 1
    try:
        if args.command == "driver-check":
            result = audit_driver(args.purplellama_dir.resolve())
            log.write(json.dumps(result, indent=2))
            if args.json_output:
                args.json_output.parent.mkdir(parents=True, exist_ok=True)
                args.json_output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
            exit_code = 0 if result["autopatching_import"] == "PASS" else 2
            return

        if args.reserve_gib < MINIMUM_RESERVE_GIB:
            raise RecoveryError(
                f"reserve_gib={args.reserve_gib} is below the approved {MINIMUM_RESERVE_GIB} GiB floor"
            )
        paths = parse_paths(args)
        plan = budget_for_paths(paths, args.reserve_gib, args.cleanup_successful_work)
        log.write(json.dumps(plan, indent=2))
        if args.command == "plan":
            if args.json_output:
                args.json_output.parent.mkdir(parents=True, exist_ok=True)
                args.json_output.write_text(json.dumps(plan, indent=2) + "\n", encoding="utf-8")
            exit_code = 0
            return

        if args.command == "driver-sync" and not args.allow_network:
            raise RecoveryError("driver-sync requires explicit --allow-network")
        if args.command != "driver-sync" and not args.allow_large_io:
            raise RecoveryError(f"{args.command} requires explicit --allow-large-io")
        require_capacity(plan, args.command)
        for directory in (paths.work, paths.cache, paths.output):
            directory.mkdir(parents=True, exist_ok=True)

        if args.command == "driver-sync":
            sync_driver_dependencies(
                paths,
                args.purplellama_dir.resolve(),
                args.requirements_file.resolve(),
                args.json_output.resolve() if args.json_output else None,
                log,
            )
        elif args.command == "prepare":
            prepare(paths, log)
        elif args.command == "build":
            if args.jobs < 1 or args.memory_gib <= 0:
                raise RecoveryError("jobs and memory-gib must be positive")
            build_target(
                paths,
                TARGETS[args.target],
                args.jobs,
                args.memory_gib,
                args.cleanup_successful_work,
                log,
            )
        elif args.command == "package":
            package_both(paths, args.cleanup_successful_work, log)
        elif args.command == "test":
            if args.memory_gib <= 0:
                raise RecoveryError("memory-gib must be positive")
            test_packages(paths, args.memory_gib, args.cleanup_successful_work, log)
        exit_code = 0
    except RecoveryError as exc:
        log.write(f"ERROR: {exc}")
        exit_code = 2
    except Exception as exc:
        log.write(f"ERROR: {type(exc).__name__}: {exc}")
        exit_code = 1
    finally:
        log.close(exit_code)
        raise SystemExit(exit_code)


if __name__ == "__main__":
    main()
