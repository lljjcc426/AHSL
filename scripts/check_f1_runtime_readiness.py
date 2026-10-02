"""Generic WSL/Linux runtime readiness checks for the F1 environment."""

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


def memory_gb() -> float:
    meminfo = Path("/proc/meminfo")
    if not meminfo.exists():
        return 0.0
    first_line = meminfo.read_text(encoding="ascii").splitlines()[0]
    return round(int(first_line.split()[1]) / 1024**2, 1)


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
    disk_free_gb = round(shutil.disk_usage(Path.home()).free / 1024**3, 1)
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
        debugger_ok = check_debugger(executable)
        python_ok = check_python(work_dir)

    ahsl_ok = (args.ahsl_path / ".git").exists()
    disk_ok = disk_free_gb >= args.min_disk_gb
    required = [
        architecture_ok,
        wsl2_ok,
        docker_ok,
        container_ok,
        compiler_ok,
        debugger_ok,
        python_ok,
        ahsl_ok,
        disk_ok,
    ]
    if not architecture_ok or not wsl2_ok:
        status = "BLOCKED"
    elif all(required):
        status = "READY"
    else:
        status = "PARTIAL"

    values = {
        "architecture_ok": architecture_ok,
        "wsl2_ok": wsl2_ok,
        "docker_ok": docker_ok,
        "container_ok": container_ok,
        "compiler_ok": compiler_ok,
        "debugger_ok": debugger_ok,
        "python_ok": python_ok,
        "ahsl_ok": ahsl_ok,
        "disk_free_gb": disk_free_gb,
        "ram_gb": ram_gb,
        "cpu_count": cpu_count,
    }
    for key, value in values.items():
        print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    print(status)


if __name__ == "__main__":
    main()
