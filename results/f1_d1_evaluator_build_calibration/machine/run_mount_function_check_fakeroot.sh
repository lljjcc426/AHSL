#!/bin/bash
set -euo pipefail

result_root=/mnt/e/GHW/ahsl/results/f1_d1_evaluator_build_calibration
work="$result_root/runtime/work"
log="$result_root/logs/mount_function_check_fakeroot_raw.log"
exec > >(tee "$log") 2>&1

mapfile -t checks < <(find "$work" -maxdepth 1 -type d -name 'mount-check-*' -print)
if [[ ${#checks[@]} -ne 1 ]]; then
    printf 'expected_one_retained_check_directory found=%s\n' "${#checks[@]}"
    exit 2
fi
check=${checks[0]}

fakeroot -- bash -euo pipefail -c '
    root=$1
    find "$root/pkg" -type d -exec chmod 0755 {} +
    find "$root/pkg" -type f -exec chmod 0644 {} +
    chmod 0755 "$root/pkg/usr/local/bin/f1-mount-check"
    dpkg-deb --root-owner-group --build "$root/pkg" "$root/f1-mount-check.deb"
' bash "$check"

test "$(dpkg-deb --field "$check/f1-mount-check.deb" Package)" = f1-mount-check
dpkg-deb --contents "$check/f1-mount-check.deb"

resolved=$(realpath -e "$check")
case "$resolved" in
    "$work"/mount-check-*) ;;
    *)
        printf 'unsafe_cleanup_target=%s\n' "$resolved"
        exit 2
        ;;
esac
rm -rf -- "$resolved"
printf 'mount_function_check_fakeroot=PASS\n'
printf 'deleted_task_owned_check=%s\n' "$resolved"
