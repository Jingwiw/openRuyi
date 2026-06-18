#!/usr/bin/env bash
set -euo pipefail

image_repo_dir=${1:?usage: build-and-inspect.sh <image-repo-dir> <overlay-repo-dir> <output-dir>}
overlay_repo_dir=${2:?usage: build-and-inspect.sh <image-repo-dir> <overlay-repo-dir> <output-dir>}
output_dir=${3:?usage: build-and-inspect.sh <image-repo-dir> <overlay-repo-dir> <output-dir>}

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
profile=${PROFILE:-validation}
target_arch=${TARGET_ARCH:-x86_64}
build_platform=${BUILD_PLATFORM:-linux/amd64}
case "$target_arch" in
    x86_64) expected_platform=linux/amd64 ;;
    *)
        echo "unsupported TARGET_ARCH=$target_arch; only x86_64 is implemented today" >&2
        exit 1
        ;;
esac
if [[ "$build_platform" != "$expected_platform" ]]; then
    echo "BUILD_PLATFORM=$build_platform does not match TARGET_ARCH=$target_arch" >&2
    exit 1
fi

upstream_repo=${UPSTREAM_REPO:-https://repo.build.openruyi.cn/openruyi/x86_64/}
upstream_repomd_sha256=${UPSTREAM_REPOMD_SHA256:-}
kiwi_source_commit=${KIWI_SOURCE_COMMIT:-unknown}
builder_base_image=${BUILDER_BASE_IMAGE:-git.openruyi.cn/openruyi/creek-x86-64@sha256:ca64fcdb246b38a775ee586e8369d4432899a6d30f6c76340f2397d88efb865e}
builder_image=${BUILDER_IMAGE:-openruyi-kiwi-builder:ci}
build_dir_in_container=${BUILD_DIR_IN_CONTAINER:-/var/tmp/openruyi-${profile}-ci}
container_name=${CONTAINER_NAME:-kiwi-ci-${profile}-${GITHUB_RUN_ID:-$$}}
overlay_repo_url=${OVERLAY_REPO_URL:-file:///overlay/}
builder_dockerfile=${BUILDER_DOCKERFILE:-$script_dir/Dockerfile.builder}
build_script_in_container=${BUILD_SCRIPT_IN_CONTAINER:-/helper/build-image.sh}
docker_bin=${DOCKER_BIN:-docker}

rm -rf "$output_dir"
mkdir -p "$output_dir/inspect"

"$docker_bin" build --platform "$build_platform" \
    --build-arg BASE_IMAGE="$builder_base_image" \
    -t "$builder_image" \
    -f "$builder_dockerfile" \
    "$script_dir"

cleanup() {
    if "$docker_bin" ps -a --format '{{.Names}}' | grep -qx "$container_name"; then
        "$docker_bin" rm -f "$container_name" >/dev/null 2>&1 || true
    fi
}
trap cleanup EXIT INT TERM

cleanup

set +e
"$docker_bin" run --name "$container_name" \
    --platform "$build_platform" \
    --privileged \
    -e PROFILE="$profile" \
    -e TARGET_ARCH="$target_arch" \
    -e BUILD_PLATFORM="$build_platform" \
    -e UPSTREAM_REPO="$upstream_repo" \
    -e UPSTREAM_REPOMD_SHA256="$upstream_repomd_sha256" \
    -e OVERLAY_REPO="$overlay_repo_url" \
    -e KIWI_SOURCE_COMMIT="$kiwi_source_commit" \
    -e BUILDER_BASE_IMAGE="$builder_base_image" \
    -e BUILD_DIR_IN_CONTAINER="$build_dir_in_container" \
    -e CONTAINER_NAME="$container_name" \
    -v "$image_repo_dir":/image:ro \
    -v "$overlay_repo_dir":/overlay:ro \
    -v "$script_dir":/helper:ro \
    -v "$output_dir":/out \
    -w /image \
    "$builder_image" \
    bash -lc '
        set -euo pipefail

        capture_command() {
            local name=$1
            shift
            local out_file=/out/inspect/${name}.txt
            local err_file=/out/inspect/${name}.err
            local rc_file=/out/inspect/${name}.rc
            local rc=0

            set +e
            "$@" >"$out_file" 2>"$err_file"
            rc=$?
            set -e

            printf "%s\n" "$rc" >"$rc_file"
        }

        rm -rf "$BUILD_DIR_IN_CONTAINER"
        SUDO= PROFILE="$PROFILE" TARGET_ARCH="$TARGET_ARCH" BUILD_PLATFORM="$BUILD_PLATFORM" \
            UPSTREAM_REPO="$UPSTREAM_REPO" UPSTREAM_REPOMD_SHA256="$UPSTREAM_REPOMD_SHA256" \
            OVERLAY_REPO="$OVERLAY_REPO" KIWI_SOURCE_COMMIT="$KIWI_SOURCE_COMMIT" \
            BUILDER_BASE_IMAGE="$BUILDER_BASE_IMAGE" \
            bash "'"$build_script_in_container"'" /image "$BUILD_DIR_IN_CONTAINER"

        mkdir -p /out/inspect

        shopt -s nullglob
        for artifact in \
            "$BUILD_DIR_IN_CONTAINER"/*.qcow2 \
            "$BUILD_DIR_IN_CONTAINER"/*.raw \
            "$BUILD_DIR_IN_CONTAINER"/*.iso \
            "$BUILD_DIR_IN_CONTAINER"/*.packages \
            "$BUILD_DIR_IN_CONTAINER"/*.changes \
            "$BUILD_DIR_IN_CONTAINER"/*.verified \
            "$BUILD_DIR_IN_CONTAINER"/compose-inputs.env \
            "$BUILD_DIR_IN_CONTAINER"/prepared-image.kiwi \
            "$BUILD_DIR_IN_CONTAINER"/prepared-config.sh; do
            cp "$artifact" /out/
        done

        rootfs="$BUILD_DIR_IN_CONTAINER/build/image-root"
        cp "$rootfs/etc/passwd" /out/inspect/passwd
        cp "$rootfs/etc/group" /out/inspect/group
        if [[ -f "$rootfs/etc/nsswitch.conf" ]]; then
            cp "$rootfs/etc/nsswitch.conf" /out/inspect/nsswitch.conf
        fi
        if [[ -f "$rootfs/etc/authselect/authselect.conf" ]]; then
            cp "$rootfs/etc/authselect/authselect.conf" /out/inspect/authselect.conf
        fi
        for pam_name in system-auth password-auth postlogin; do
            if [[ -f "$rootfs/etc/pam.d/$pam_name" ]]; then
                cp "$rootfs/etc/pam.d/$pam_name" "/out/inspect/$pam_name"
            fi
            if [[ -f "$rootfs/etc/authselect/$pam_name" ]]; then
                cp "$rootfs/etc/authselect/$pam_name" "/out/inspect/authselect-$pam_name"
            fi
        done

        if [[ -x "$rootfs/usr/bin/authselect" ]]; then
            capture_command authselect-current-raw chroot "$rootfs" /usr/bin/authselect current --raw
        else
            : >/out/inspect/authselect-current-raw.txt
            printf "%s\n" "authselect missing from image rootfs" >/out/inspect/authselect-current-raw.err
            printf "%s\n" "127" >/out/inspect/authselect-current-raw.rc
        fi

        capture_command rpm-query rpm --root "$rootfs" --dbpath /usr/lib/sysimage/rpm -q \
            setup authselect openruyi-authselect-profiles system-user-root

        cat >/out/inspect/build.env <<EOF
PROFILE=$PROFILE
TARGET_ARCH=$TARGET_ARCH
BUILD_PLATFORM=$BUILD_PLATFORM
UPSTREAM_REPO=$UPSTREAM_REPO
UPSTREAM_REPOMD_SHA256=$UPSTREAM_REPOMD_SHA256
OVERLAY_REPO=$OVERLAY_REPO
BUILDER_BASE_IMAGE=$BUILDER_BASE_IMAGE
KIWI_SOURCE_COMMIT=$KIWI_SOURCE_COMMIT
BUILD_DIR_IN_CONTAINER=$BUILD_DIR_IN_CONTAINER
CONTAINER_NAME=$CONTAINER_NAME
EOF
    '
build_rc=$?
set -e

if [[ $build_rc -ne 0 ]]; then
    "$docker_bin" logs "$container_name" || true
    exit "$build_rc"
fi

if [[ -f "$overlay_repo_dir/PROVENANCE.txt" ]]; then
    cp "$overlay_repo_dir/PROVENANCE.txt" "$output_dir/OVERLAY_PROVENANCE.txt"
fi
