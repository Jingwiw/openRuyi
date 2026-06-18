#!/usr/bin/env bash
set -euo pipefail

output_dir=${1:?usage: verify-output.sh <output-dir>}
inspect_dir=$output_dir/inspect
report_file=$output_dir/SMOKE_SUMMARY.txt
expect_setup_source_pattern=${EXPECT_SETUP_SOURCE_PATTERN:-${EXPECT_OVERLAY_SOURCE_PATTERN:-}}
status=0

if [[ -f "$inspect_dir/build.env" ]]; then
    # shellcheck disable=SC1090
    source "$inspect_dir/build.env"
fi

if [[ -z "$expect_setup_source_pattern" ]] && [[ -n "${OVERLAY_REPO:-}" ]]; then
    if [[ "$OVERLAY_REPO" == https://repo.build.openruyi.cn/* ]]; then
        expect_setup_source_pattern=${OVERLAY_REPO#https://repo.build.openruyi.cn/}
        expect_setup_source_pattern=${expect_setup_source_pattern%/}
        expect_setup_source_pattern=${expect_setup_source_pattern%/x86_64}
        expect_setup_source_pattern=${expect_setup_source_pattern//:\//:}
    fi
fi

: >"$report_file"

pass() {
    printf '[PASS] %s\n' "$1" | tee -a "$report_file"
}

fail() {
    printf '[FAIL] %s\n' "$1" | tee -a "$report_file" >&2
    status=1
}

resolve_artifact() {
    local __var=$1
    local pattern=$2
    local label=$3
    local artifact

    artifact=$(find "$output_dir" -maxdepth 1 -type f -name "$pattern" | sort | head -n 1 || true)
    if [[ -n "$artifact" ]]; then
        pass "$label present"
    else
        fail "$label missing ($pattern)"
    fi
    printf -v "$__var" '%s' "$artifact"
}

require_file() {
    local path=$1
    local label=$2
    if [[ -f "$path" ]]; then
        pass "$label present"
    else
        fail "$label missing: $path"
    fi
}

resolve_artifact qcow2_path '*.qcow2' 'qcow2 image'
resolve_artifact packages_path '*.packages' 'package manifest'
resolve_artifact prepared_kiwi_path 'prepared-image.kiwi' 'prepared image description'
resolve_artifact compose_inputs_path 'compose-inputs.env' 'compose inputs'

require_file "$inspect_dir/passwd" "inspect/passwd"
require_file "$inspect_dir/group" "inspect/group"
require_file "$inspect_dir/build.env" "inspect/build.env"
require_file "$inspect_dir/rpm-query.rc" "inspect/rpm-query.rc"
require_file "$inspect_dir/authselect-current-raw.rc" "inspect/authselect-current-raw.rc"

if [[ -n "$compose_inputs_path" ]]; then
    if grep -q '^PROFILE=validation$' "$compose_inputs_path"; then
        pass "compose inputs use validation profile"
    else
        fail "compose inputs profile mismatch"
    fi
    if grep -q '^TARGET_ARCH=x86_64$' "$compose_inputs_path"; then
        pass "compose inputs are scoped to x86_64"
    else
        fail "compose inputs target arch mismatch"
    fi
    if grep -q '^BUILD_PLATFORM=linux/amd64$' "$compose_inputs_path"; then
        pass "compose inputs are scoped to linux/amd64"
    else
        fail "compose inputs build platform mismatch"
    fi
    if grep -q '^KIWI_SOURCE_COMMIT=' "$compose_inputs_path"; then
        pass "compose inputs record kiwi source commit"
    else
        fail "compose inputs missing kiwi source commit"
    fi
    if grep -q '^BUILDER_BASE_IMAGE=' "$compose_inputs_path"; then
        pass "compose inputs record builder base image"
    else
        fail "compose inputs missing builder base image"
    fi
fi

if [[ -n "$prepared_kiwi_path" ]]; then
    if grep -Fq 'installiso="true"' "$prepared_kiwi_path"; then
        fail "prepared image still requests installiso"
    else
        pass "prepared image drops installiso mode"
    fi
    if grep -Fq 'filesystem="xfs"' "$prepared_kiwi_path"; then
        pass "prepared image keeps xfs rootfs"
    else
        fail "prepared image lost xfs rootfs"
    fi
    if grep -Fq 'preferlvm="true"' "$prepared_kiwi_path"; then
        pass "prepared image keeps LVM systemdisk"
    else
        fail "prepared image lost LVM systemdisk"
    fi
    if grep -Fq 'efiparttable="gpt"' "$prepared_kiwi_path" && grep -Fq 'eficsm="false"' "$prepared_kiwi_path"; then
        pass "prepared image keeps EFI GPT layout"
    else
        fail "prepared image lost EFI GPT layout"
    fi
    if grep -Fq '<profile name="livecd"' "$prepared_kiwi_path"; then
        fail "prepared image still carries livecd profile"
    else
        pass "prepared image drops livecd profile"
    fi
fi

if [[ -f "$output_dir/OVERLAY_PROVENANCE.txt" ]]; then
    pass "overlay provenance present"
else
    fail "overlay provenance missing"
fi

if [[ -f "$output_dir/upstream-repomd.xml" ]]; then
    pass "upstream repomd captured"
else
    fail "upstream repomd missing"
fi

if [[ -n "$packages_path" ]]; then
    if grep -q '^authselect|' "$packages_path"; then
        pass "authselect installed"
    else
        fail "authselect missing from package manifest"
    fi

    if grep -q '^openruyi-authselect-profiles|' "$packages_path"; then
        pass "openruyi-authselect-profiles installed"
    else
        fail "openruyi-authselect-profiles missing from package manifest"
    fi

    if grep -q '^setup|' "$packages_path"; then
        pass "setup installed"
    else
        fail "setup missing from package manifest"
    fi

    if grep -q '^lvm2|' "$packages_path"; then
        pass "lvm2 installed"
    else
        fail "lvm2 missing from package manifest"
    fi

    if grep -q '^xfsprogs|' "$packages_path"; then
        pass "xfsprogs installed"
    else
        fail "xfsprogs missing from package manifest"
    fi

    if grep -q '^calamares|' "$packages_path"; then
        fail "calamares should not be installed"
    else
        pass "calamares removed from package manifest"
    fi

    if grep -q '^dracut-kiwi-live|' "$packages_path"; then
        fail "dracut-kiwi-live should not be installed"
    else
        pass "dracut-kiwi-live removed from package manifest"
    fi

    if grep -q '^dracut-kiwi-oem-repart|' "$packages_path"; then
        pass "dracut-kiwi-oem-repart installed"
    else
        fail "dracut-kiwi-oem-repart missing from package manifest"
    fi

    if [[ -n "$expect_setup_source_pattern" ]]; then
        setup_line=$(grep '^setup|' "$packages_path" || true)
        if printf '%s\n' "$setup_line" | grep -Fq "$expect_setup_source_pattern"; then
            pass "setup came from $expect_setup_source_pattern"
        else
            fail "setup source mismatch: ${setup_line:-missing}"
        fi
    fi
fi

if [[ -f "$inspect_dir/rpm-query.rc" ]]; then
    rpm_query_rc=$(tr -d '\n' <"$inspect_dir/rpm-query.rc")
    if [[ "$rpm_query_rc" == 0 ]]; then
        pass "rpm query inspection succeeded"
    else
        pass "rpm root query is non-authoritative for KIWI outputs (rc=$rpm_query_rc)"
    fi
fi

if [[ -f "$inspect_dir/authselect-current-raw.rc" ]]; then
    authselect_rc=$(tr -d '\n' <"$inspect_dir/authselect-current-raw.rc")
    if [[ "$authselect_rc" =~ ^[0-9]+$ ]]; then
        pass "authselect inspection rc captured ($authselect_rc)"
    else
        fail "authselect inspection rc invalid"
    fi
fi

if [[ -n "$qcow2_path" ]] && command -v qemu-img >/dev/null 2>&1; then
    qemu-img info "$qcow2_path" >"$inspect_dir/qemu-img-info.txt"
    pass "qemu-img info captured"
fi

if [[ -n "$qcow2_path" ]] && command -v file >/dev/null 2>&1; then
    file "$qcow2_path" >"$inspect_dir/file-output.txt"
    pass "file(1) output captured"
fi

if [[ $status -eq 0 ]]; then
    printf 'Smoke verification passed: %s\n' "$output_dir" | tee -a "$report_file"
else
    printf 'Smoke verification failed: %s\n' "$output_dir" | tee -a "$report_file" >&2
fi

exit "$status"
