"""Generic WSL/Linux runtime checks, not F1 benchmark readiness.

``ahsl_ok`` only confirms that the requested checkout path contains ``.git``.
``python_ok`` creates a temporary venv and runs one Python statement; it does
not validate the AHSL Python version or dependencies. ``codex_cli_ok`` only
checks that the executable is on PATH and answers ``--version``; it does not
prove authentication, model access, or inference availability.
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import platform
import shutil
import subprocess
import tempfile


def run(command: list[str], timeout: int = 120) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired) as error:
        return subprocess.CompletedProcess(command, 127, "", str(error))


def compile_trivial_program(work_dir: Path) -> tuple[bool, Path | None]:
    compiler = shutil.which("gcc") or shutil.which("clang")
    if compiler is None:
        return False, None
    source = work_dir / "hello.c"
    executable = work_dir / "hello"
    source.write_text(
        '#include <stdio.h>\nint main(void) { puts("runtime-ok"); return 0; }\n',
        encoding="ascii",
    )
    built = run([compiler, str(source), "-o", str(executable)])
    executed = run([str(executable)]) if built.returncode == 0 else built
    return executed.returncode == 0 and executed.stdout.strip() == "runtime-ok", executable


def check_cmake(work_dir: Path) -> bool:
    cmake = shutil.which("cmake")
    if cmake is None:
        return False
    project_dir = work_dir / "cmake-project"
    build_dir = work_dir / "cmake-build"
    project_dir.mkdir()
    (project_dir / "CMakeLists.txt").write_text(
        "cmake_minimum_required(VERSION 3.16)\n"
        "project(runtime_check LANGUAGES CXX)\n"
        "add_executable(cmake_runtime main.cpp)\n",
        encoding="ascii",
    )
    (project_dir / "main.cpp").write_text(
        '#include <iostream>\nint main() { std::cout << "cmake-ok\\n"; }\n',
        encoding="ascii",
    )
    configured = run([cmake, "-S", str(project_dir), "-B", str(build_dir)])
    if configured.returncode != 0:
        return False
    built = run([cmake, "--build", str(build_dir)])
    if built.returncode != 0:
        return False
    executed = run([str(build_dir / "cmake_runtime")])
    return executed.returncode == 0 and executed.stdout.strip() == "cmake-ok"


def check_debugger(executable: Path | None) -> bool:
    lldb = shutil.which("lldb")
    if lldb is None or executable is None:
        return False
    result = run([lldb, "--batch", "-o", "run", "-o", "quit", str(executable)])
    return result.returncode == 0 and "runtime-ok" in result.stdout


def check_python(work_dir: Path) -> bool:
    python = shutil.which("python3")
    if python is None:
        return False
    environment = work_dir / "venv"
    created = run([python, "-m", "venv", str(environment)])
    if created.returncode != 0:
        return False
    interpreter = environment / "bin" / "python"
    result = run([str(interpreter), "-c", "print('python-ok')"])
    return result.returncode == 0 and result.stdout.strip() == "python-ok"


def check_codex_cli() -> bool:
    codex = shutil.which("codex")
    if codex is None:
        return False
    result = run([codex, "--version"])
    return result.returncode == 0 and "codex-cli" in result.stdout


def memory_gb() -> float:
    meminfo = Path("/proc/meminfo")
    if not meminfo.exists():
        return 0.0
    first_line = meminfo.read_text(encoding="ascii").splitlines()[0]
    return round(int(first_line.split()[1]) / 1024**2, 1)


def classify_readiness(*, architecture_ok: bool, wsl2_ok: bool, required: list[bool]) -> str:
    if not architecture_ok or not wsl2_ok:
        return "BLOCKED"
    return "READY" if all(required) else "PARTIAL"


def readiness_exit_code(status: str) -> int:
    return {"READY": 0, "PARTIAL": 1, "BLOCKED": 2}[status]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ahsl-path", type=Path, default=Path.home() / "research" / "AHSL")
    parser.add_argument("--container-image", default="ubuntu:24.04")
    parser.add_argument("--min-disk-gb", type=float, default=50.0)
    args = parser.parse_args()

    machine = platform.machine().lower()
    kernel = platform.release().lower()
    architecture_ok = machine in {"x86_64", "amd64"}
    wsl2_ok = "microsoft-standard-wsl2" in kernel
    disk_path = Path("/mnt/c") if wsl2_ok and Path("/mnt/c").exists() else Path.home()
    disk_free_gb = round(shutil.disk_usage(disk_path).free / 1024**3, 1)
    ram_gb = memory_gb()
    cpu_count = os.cpu_count() or 0

    docker_info = run(["docker", "info"], timeout=30)
    docker_ok = docker_info.returncode == 0
    container_ok = False
    if docker_ok:
        container = run(
            ["docker", "run", "--rm", args.container_image, "uname", "-m"],
            timeout=300,
        )
        container_ok = container.returncode == 0 and container.stdout.strip() in {
            "x86_64",
            "amd64",
        }

    with tempfile.TemporaryDirectory(prefix="f1-runtime-") as temporary:
        work_dir = Path(temporary)
        compiler_ok, executable = compile_trivial_program(work_dir)
        cmake_ok = check_cmake(work_dir)
        debugger_ok = check_debugger(executable)
        python_ok = check_python(work_dir)

    codex_cli_ok = check_codex_cli()
    ahsl_ok = (args.ahsl_path / ".git").exists()
    disk_ok = disk_free_gb >= args.min_disk_gb
    required = [
        architecture_ok,
        wsl2_ok,
        docker_ok,
        container_ok,
        compiler_ok,
        cmake_ok,
        debugger_ok,
        python_ok,
        codex_cli_ok,
        ahsl_ok,
        disk_ok,
    ]
    status = classify_readiness(
        architecture_ok=architecture_ok,
        wsl2_ok=wsl2_ok,
        required=required,
    )

    values = {
        "architecture_ok": architecture_ok,
        "wsl2_ok": wsl2_ok,
        "docker_ok": docker_ok,
        "container_ok": container_ok,
        "compiler_ok": compiler_ok,
        "cmake_ok": cmake_ok,
        "debugger_ok": debugger_ok,
        "python_ok": python_ok,
        "codex_cli_ok": codex_cli_ok,
        "ahsl_ok": ahsl_ok,
        "disk_free_gb": disk_free_gb,
        "ram_gb": ram_gb,
        "cpu_count": cpu_count,
    }
    for key, value in values.items():
        print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    print(status)
    raise SystemExit(readiness_exit_code(status))


if __name__ == "__main__":
    main()
