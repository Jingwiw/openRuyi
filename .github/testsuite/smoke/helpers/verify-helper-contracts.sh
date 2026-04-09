#!/usr/bin/env bash
set -euo pipefail

repo_root=$(CDPATH= cd -- "$(dirname -- "$0")/../../../.." && pwd)
tmp_dir=$(mktemp -d "${TMPDIR:-/tmp}/openruyi-kiwi-helper-tests.XXXXXX")
status=0

cleanup() {
    rm -rf "$tmp_dir"
}
trap cleanup EXIT INT TERM

pass() {
    printf '[PASS] %s\n' "$1"
}

fail() {
    printf '[FAIL] %s\n' "$1" >&2
    status=1
}

assert_contains() {
    local file=$1
    local pattern=$2
    local label=$3
    if grep -Fq "$pattern" "$file"; then
        pass "$label"
    else
        fail "$label"
    fi
}

assert_not_contains() {
    local file=$1
    local pattern=$2
    local label=$3
    if grep -Fq "$pattern" "$file"; then
        fail "$label"
    else
        pass "$label"
    fi
}

build_workflow=$repo_root/.github/workflows/build.yaml
selftest_workflow=$repo_root/.github/workflows/ci-selftest.yaml
build_and_inspect=$repo_root/.github/image-build/kiwi-installiso/build-and-inspect.sh
build_image=$repo_root/.github/image-build/kiwi-installiso/build-image.sh
make_local_repo=$repo_root/.github/common/make-local-rpm-repo.sh
smoke_verify=$repo_root/.github/testsuite/smoke/installiso/verify-output.sh

assert_contains "$build_workflow" "     - 'SPECS/**'" "build workflow watches SPECS paths"
assert_not_contains "$build_workflow" ".github/common/**" "build workflow no longer watches helper-only changes"
assert_contains "$selftest_workflow" ".github/common/**" "selftest workflow watches helper changes"
assert_contains "$selftest_workflow" ".github/image-build/**" "selftest workflow watches image helper changes"
assert_contains "$selftest_workflow" ".github/testsuite/**" "selftest workflow watches testsuite changes"
assert_contains "$build_and_inspect" '-e CONTAINER_NAME="$container_name"' "build-and-inspect passes CONTAINER_NAME into container"
assert_contains "$build_and_inspect" 'CONTAINER_NAME=$CONTAINER_NAME' "build-and-inspect writes CONTAINER_NAME from container env"
assert_contains "$build_and_inspect" 'UPSTREAM_REPOMD_SHA256' "build-and-inspect records upstream repomd checksum"
assert_contains "$build_and_inspect" 'BUILD_PLATFORM=' "build-and-inspect uses explicit build platform"
assert_not_contains "$smoke_verify" "root shell is" "smoke suite no longer contains shell policy checks"
assert_not_contains "$smoke_verify" "authselect current profile is" "smoke suite no longer contains auth profile policy checks"

mkdir -p "$tmp_dir/bin" "$tmp_dir/image" "$tmp_dir/target" "$tmp_dir/artifacts/a" "$tmp_dir/artifacts/b"

cat >"$tmp_dir/bin/kiwi-ng" <<EOF
#!/usr/bin/env bash
printf '%s\n' "\$*" >"$tmp_dir/kiwi-args.log"
exit 0
EOF
chmod +x "$tmp_dir/bin/kiwi-ng"

cat >"$tmp_dir/image/image.kiwi" <<'EOF'
<image schemaversion="7.5" name="openRuyi">
  <preferences>
    <type image="oem" primary="true"/>
  </preferences>
  <repository type="rpm-md" alias="openruyi">
    <source path="obsrepositories:/"/>
  </repository>
  <packages type="bootstrap">
    <package name="filesystem"/>
  </packages>
</image>
EOF

: >"$tmp_dir/image/config.sh"

PATH="$tmp_dir/bin:$PATH" \
SUDO= \
PROFILE=installiso \
TARGET_ARCH=x86_64 \
BUILD_PLATFORM=linux/amd64 \
UPSTREAM_REPO=https://repo.build.openruyi.cn/openruyi/x86_64/ \
OVERLAY_REPO=file:///overlay/ \
KIWI_SOURCE_COMMIT=test-commit \
BUILDER_BASE_IMAGE=docker.io/example/builder@sha256:test \
bash "$build_image" "$tmp_dir/image" "$tmp_dir/target"

assert_contains "$tmp_dir/target/prepared-image.kiwi" 'alias="openruyi"' "prepared image keeps openruyi repo"
assert_contains "$tmp_dir/target/prepared-image.kiwi" 'path="https://repo.build.openruyi.cn/openruyi/x86_64/"' "prepared image points openruyi repo at upstream"
assert_contains "$tmp_dir/target/prepared-image.kiwi" 'alias="overlay"' "prepared image adds overlay repo"
assert_contains "$tmp_dir/target/prepared-image.kiwi" 'path="file:///overlay/"' "prepared image points overlay repo at overlay path"
assert_contains "$tmp_dir/target/prepared-image.kiwi" 'name="libudev-zero"' "prepared image injects libudev-zero ignore"
assert_contains "$tmp_dir/target/prepared-image.kiwi" 'name="systemd-udev"' "prepared image injects systemd-udev bootstrap package"
assert_contains "$tmp_dir/target/prepared-config.sh" 'openRuyi CI initrd hint' "prepared config appends CI initrd hint"
assert_contains "$tmp_dir/target/compose-inputs.env" 'TARGET_ARCH=x86_64' "prepared compose inputs record x86_64"
assert_contains "$tmp_dir/target/compose-inputs.env" 'BUILD_PLATFORM=linux/amd64' "prepared compose inputs record build platform"

if PATH="$tmp_dir/bin:$PATH" \
    SUDO= \
    TARGET_ARCH=aarch64 \
    BUILD_PLATFORM=linux/arm64 \
    bash "$build_image" "$tmp_dir/image" "$tmp_dir/target" >/dev/null 2>&1; then
    fail "build-image rejects unsupported arch"
else
    pass "build-image rejects unsupported arch"
fi

cat >"$tmp_dir/bin/createrepo_c" <<EOF
#!/usr/bin/env bash
mkdir -p "\$1/repodata"
exit 0
EOF
chmod +x "$tmp_dir/bin/createrepo_c"

: >"$tmp_dir/artifacts/a/pkg-1-1.noarch.rpm"
: >"$tmp_dir/artifacts/b/pkg-1-1.noarch.rpm"
if PATH="$tmp_dir/bin:$PATH" bash "$make_local_repo" "$tmp_dir/artifacts" "$tmp_dir/repo-dup" >/dev/null 2>&1; then
    fail "make-local-rpm-repo detects duplicate basenames"
else
    pass "make-local-rpm-repo detects duplicate basenames"
fi

rm -rf "$tmp_dir/artifacts" "$tmp_dir/repo-ok"
mkdir -p "$tmp_dir/artifacts/a" "$tmp_dir/artifacts/b"
: >"$tmp_dir/artifacts/a/pkg-a-1-1.noarch.rpm"
: >"$tmp_dir/artifacts/b/pkg-b-1-1.noarch.rpm"
PATH="$tmp_dir/bin:$PATH" bash "$make_local_repo" "$tmp_dir/artifacts" "$tmp_dir/repo-ok"
if [[ -f "$tmp_dir/repo-ok/PROVENANCE.txt" ]] && [[ -d "$tmp_dir/repo-ok/repodata" ]]; then
    pass "make-local-rpm-repo writes provenance and repo metadata"
else
    fail "make-local-rpm-repo writes provenance and repo metadata"
fi

exit "$status"
