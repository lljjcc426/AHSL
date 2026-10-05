#!/bin/bash
set +e

result_root=/mnt/e/GHW/ahsl/results/f1_d1_evaluator_build_calibration
cd /home/cc/research/AHSL || exit 1
export PYTHONPATH=src

python=/home/cc/.venvs/ahsl-f1-d1-runtime-reentry/bin/python
log="$result_root/logs/targeted_tests_f1_python312_final_raw.log"
exit_file="$result_root/machine/targeted_tests_f1_python312_final.exit_code"
junit="$result_root/machine/targeted_tests_f1_python312_final.junit.xml"

"$python" --version >"$log" 2>&1
"$python" -m pytest -q tests/test_f1_d1_evaluator_dependency_recovery.py \
    --junitxml="$junit" >>"$log" 2>&1
exit_code=$?
printf '%s\n' "$exit_code" >"$exit_file"
cat "$log"
exit "$exit_code"
