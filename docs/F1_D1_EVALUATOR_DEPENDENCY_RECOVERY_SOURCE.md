# F1-D1 evaluator dependency recovery source note

## Upstream status

The frozen evaluator remains [`meta-llama/PurpleLlama` commit
`4be64c3a24442b51c76175e6ec67722cc3f5fe38`](https://github.com/meta-llama/PurpleLlama/commit/4be64c3a24442b51c76175e6ec67722cc3f5fe38).
[Issue 123](https://github.com/meta-llama/PurpleLlama/issues/123) was still open when
checked on 2026-10-05. Its only maintainer-visible follow-up reproduced the S3
`AccessDenied` response; no official replacement package or public retrieval
route was provided. The recovery path therefore does not retry the inaccessible
objects and does not use AWS or Codex credentials.

## Adopted source

The implementation uses the build sequence from
[`safety-research/PurpleLlama` commit
`8a98628dc7941972c96ffac5e3f8fed839ad336a`](https://github.com/safety-research/PurpleLlama/commit/8a98628dc7941972c96ffac5e3f8fed839ad336a)
as its starting point. The files
reviewed in full were:

- `CybersecurityBenchmarks/benchmark/autopatch/build/build_deb_packages.sh`
- `CybersecurityBenchmarks/benchmark/autopatch/build/test_deb_install.sh`
- `CybersecurityBenchmarks/benchmark/autopatch/build/README.md`

Only the dependency-build design was adopted. No fork benchmark code,
evaluator comparison logic, result field, dataset split, or reference repair
was copied into the frozen evaluator.

The fork's `CybersecurityBenchmarks/LICENSE` is the MIT License, copyright Meta
Platforms, Inc. and affiliates. The adapted recovery script retains that
attribution and the following permission notice:

> Permission is hereby granted, free of charge, to any person obtaining a copy
> of this software and associated documentation files (the "Software"), to deal
> in the Software without restriction, including without limitation the rights
> to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
> copies of the Software, and to permit persons to whom the Software is
> furnished to do so, subject to the conditions in the upstream MIT License.

The upstream software is provided "AS IS", without warranty of any kind. The
complete notice is retained in
`docs/third_party/F1_D1_PURPLELLAMA_BUILD_LICENSE.txt` and remains available in
the source repository's `CybersecurityBenchmarks/LICENSE`.

## Bounded modifications

The recovery implementation preserves the fork's Python 3.7.17 and
LLVM/LLDB 13.0.1 source-build route for Ubuntu 16.04 and 20.04. It changes the
operational wrapper as follows:

- all work, cache, output, log, container-store, and host-volume paths are
  explicit;
- build CPU count and memory are explicit;
- preparation, target builds, packaging, package tests, and driver import
  checks are separate commands;
- host `apt-get`, host `sudo`, fixed `/tmp` workspaces, interactive prompts,
  and implicit overwrite are removed;
- cached targets require Python, LLDB, Python bindings, the SWIG extension, and
  a completion marker;
- LLDB installation failure is fatal instead of being masked by `|| true`;
- the staged Python 3.7 interpreter and its shared-library-backed standard
  extensions must run before LLVM configuration starts;
- the former broad LLVM `install` target is limited to LLDB, `liblldb`, the
  Python scripts, `lldb-argdumper`, `lldb-server`, and Clang resource headers;
- generated shell environment variables append safely under `set -u` without
  adding an empty search-path element;
- resource output separates workflow-start cumulative occupancy from the
  remaining incremental peak at a confirmed checkpoint;
- generated packages declare their runtime library dependencies and identify
  themselves as `1.0.0+source1`;
- package tests cover package metadata, amd64 ELF architecture, dynamic
  dependencies, Python `import lldb`, the LLDB Python API, and an actual LLDB
  launch of `/bin/true`;
- a static import-closure check distinguishes the AutoPatch driver subset from
  the full benchmark requirements and reads omitted sparse-checkout modules
  from the pinned Git object without modifying the frozen checkout;
- the dedicated driver requirement file contains the nine directly relevant
  official constraints plus `requests==2.33.0`, a direct frozen-code import
  omitted by `CybersecurityBenchmarks/requirements.txt` but pinned elsewhere
  in the same repository commit; `botocore` remains a `boto3` dependency;
- `driver-sync` installs only into an active virtual environment, uses the
  explicit cache path, preserves the pip log, and then requires the real
  AutoPatch import to pass;
- large-I/O commands require an explicit flag and a passing stage budget.

The source-built packages are not claimed to be byte-identical to the
unavailable official binaries. Package tests also do not imply that the full
10445 evaluator chain has passed.
