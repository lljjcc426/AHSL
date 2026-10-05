#!/bin/bash
set -euo pipefail

result_root=/mnt/e/GHW/ahsl/results/f1_d1_evaluator_build_calibration
work="$result_root/runtime/work"
logs="$result_root/logs"
mkdir -p "$work" "$logs"

check="$work/mount-check-$(date -u +%Y%m%dT%H%M%SZ)-$$"
log="$logs/mount_function_check_raw.log"
exec > >(tee "$log") 2>&1

mkdir -p "$check/pkg/DEBIAN" "$check/pkg/usr/local/bin"
printf 'payload\n' >"$check/payload"
ln -s payload "$check/payload-link"
test "$(cat "$check/payload-link")" = payload

printf '#!/bin/sh\nprintf executable-ok\n' >"$check/pkg/usr/local/bin/f1-mount-check"
chmod 0755 "$check/pkg/usr/local/bin/f1-mount-check"
test "$("$check/pkg/usr/local/bin/f1-mount-check")" = executable-ok

printf '%s\n' \
    'Package: f1-mount-check' \
    'Version: 1' \
    'Architecture: all' \
    'Maintainer: AHSL' \
    'Description: mount operation check' >"$check/pkg/DEBIAN/control"
dpkg-deb --root-owner-group --build "$check/pkg" "$check/f1-mount-check.deb"
test "$(dpkg-deb --field "$check/f1-mount-check.deb" Package)" = f1-mount-check

resolved=$(realpath -e "$check")
case "$resolved" in
    "$work"/mount-check-*) ;;
    *)
        printf 'unsafe_cleanup_target=%s\n' "$resolved"
        exit 2
        ;;
esac
rm -rf -- "$resolved"
printf 'mount_function_check=PASS\n'
printf 'deleted_task_owned_check=%s\n' "$resolved"
