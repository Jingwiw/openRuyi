#!/usr/bin/env bash
set -euo pipefail

image_repo_dir=${1:?usage: build-image.sh <image-repo-dir> <target-dir>}
target_dir=${2:?usage: build-image.sh <image-repo-dir> <target-dir>}

profile=${PROFILE:-installiso}
target_arch=${TARGET_ARCH:-x86_64}
build_platform=${BUILD_PLATFORM:-linux/amd64}
case "$target_arch" in
    x86_64)
        expected_platform=linux/amd64
        default_upstream_repo=https://repo.build.openruyi.cn/openruyi/x86_64/
        ;;
    *)
        echo "unsupported TARGET_ARCH=$target_arch; only x86_64 is implemented today" >&2
        exit 1
        ;;
esac
if [[ "$build_platform" != "$expected_platform" ]]; then
    echo "BUILD_PLATFORM=$build_platform does not match TARGET_ARCH=$target_arch" >&2
    exit 1
fi

upstream_repo=${UPSTREAM_REPO:-${MAIN_REPO:-$default_upstream_repo}}
overlay_repo=${OVERLAY_REPO:-${FIX_REPO:-}}
upstream_repomd_url=${UPSTREAM_REPOMD_URL:-${upstream_repo%/}/repodata/repomd.xml}
upstream_repomd_sha256=${UPSTREAM_REPOMD_SHA256:-}
builder_base_image=${BUILDER_BASE_IMAGE:-docker.io/opensuse/tumbleweed@sha256:ef83be77fac5207611adab5407f6c8b0ca5dd4f1924ad30682f53e807dd13f3d}
kiwi_source_commit=${KIWI_SOURCE_COMMIT:-unknown}
sudo_cmd=${SUDO-sudo}
kiwi_part_mapper=${KIWI_PART_MAPPER:-}

if [[ ! -f "$image_repo_dir/image.kiwi" ]]; then
    echo "image.kiwi missing under $image_repo_dir" >&2
    exit 1
fi

mkdir -p "$target_dir"

if [[ -n "$upstream_repomd_sha256" ]]; then
    actual_repomd_sha256=$(curl -fsSL "$upstream_repomd_url" | sha256sum | awk '{print $1}')
    if [[ "$actual_repomd_sha256" != "$upstream_repomd_sha256" ]]; then
        echo "upstream repomd checksum mismatch: expected $upstream_repomd_sha256, got $actual_repomd_sha256" >&2
        exit 1
    fi
fi

work_dir=$(mktemp -d "${TMPDIR:-/tmp}/openruyi-kiwi.XXXXXX")
cleanup() {
    rm -rf "$work_dir"
}
trap cleanup EXIT INT TERM

(
    cd "$image_repo_dir"
    tar \
        --exclude='./.git' \
        --exclude='./.DS_Store' \
        --exclude='./out-*' \
        -cf - .
) | (
    cd "$work_dir"
    tar -xf -
)

IMAGE_KIWI_PATH=$work_dir/image.kiwi \
UPSTREAM_REPO_XML=$upstream_repo \
OVERLAY_REPO_XML=$overlay_repo \
python3 <<'PY'
import os
import xml.etree.ElementTree as ET


def local_name(tag: str) -> str:
    return tag.split("}", 1)[-1]


image_kiwi_path = os.environ["IMAGE_KIWI_PATH"]
upstream_repo = os.environ["UPSTREAM_REPO_XML"]
overlay_repo = os.environ["OVERLAY_REPO_XML"]

tree = ET.parse(image_kiwi_path)
root = tree.getroot()
children = list(root)

repo_candidates = []
for child in children:
    if local_name(child.tag) != "repository":
        continue
    if child.get("type") != "rpm-md" or child.get("alias") != "openruyi":
        continue
    source = next((node for node in child if local_name(node.tag) == "source"), None)
    if source is None or source.get("path") != "obsrepositories:/":
        continue
    repo_candidates.append(child)

if len(repo_candidates) != 1:
    raise SystemExit("expected exactly one openruyi obsrepositories:/ repository block")

openruyi_repo = repo_candidates[0]
repo_index = children.index(openruyi_repo)
root.remove(openruyi_repo)

def make_repo(alias: str, path: str):
    repo = ET.Element(openruyi_repo.tag, {"type": "rpm-md", "alias": alias})
    ET.SubElement(repo, "source", {"path": path})
    return repo


root.insert(repo_index, make_repo("openruyi", upstream_repo))
if overlay_repo:
    root.insert(repo_index + 1, make_repo("overlay", overlay_repo))

bootstrap_sections = [
    child for child in list(root)
    if local_name(child.tag) == "packages" and child.get("type") == "bootstrap"
]
if len(bootstrap_sections) != 1:
    raise SystemExit("expected exactly one bootstrap package section")

bootstrap = bootstrap_sections[0]
ignore_names = {node.get("name") for node in bootstrap if local_name(node.tag) == "ignore"}
package_names = {node.get("name") for node in bootstrap if local_name(node.tag) == "package"}

if "libudev-zero" not in ignore_names:
    bootstrap.append(ET.Element("ignore", {"name": "libudev-zero"}))
if "systemd-udev" not in package_names:
    bootstrap.append(ET.Element("package", {"name": "systemd-udev"}))

ET.indent(tree, space="  ")
tree.write(image_kiwi_path, encoding="utf-8", xml_declaration=False)

tree = ET.parse(image_kiwi_path)
root = tree.getroot()
repo_sources = {}
for child in list(root):
    if local_name(child.tag) != "repository":
        continue
    source = next((node for node in child if local_name(node.tag) == "source"), None)
    if source is not None:
        repo_sources[child.get("alias")] = source.get("path")

if repo_sources.get("openruyi") != upstream_repo:
    raise SystemExit("openruyi repository mutation did not take effect")
if overlay_repo and repo_sources.get("overlay") != overlay_repo:
    raise SystemExit("overlay repository mutation did not take effect")

bootstrap = next(
    child for child in list(root)
    if local_name(child.tag) == "packages" and child.get("type") == "bootstrap"
)
ignore_names = {node.get("name") for node in bootstrap if local_name(node.tag) == "ignore"}
package_names = {node.get("name") for node in bootstrap if local_name(node.tag) == "package"}
if "libudev-zero" not in ignore_names:
    raise SystemExit("bootstrap ignore injection did not take effect")
if "systemd-udev" not in package_names:
    raise SystemExit("bootstrap package injection did not take effect")
PY

if [[ ! -f "$work_dir/config.sh" ]]; then
    : > "$work_dir/config.sh"
fi

if ! grep -Fq '# openRuyi CI initrd hint' "$work_dir/config.sh"; then
cat >> "$work_dir/config.sh" <<'EOF'

# openRuyi CI initrd hint
# Keep a stable initramfs path for KIWI image verification.

kernel_dir=$(find /lib/modules -mindepth 1 -maxdepth 1 -type d | head -n 1 || true)
if [ -n "$kernel_dir" ]; then
    kernel_version=$(basename "$kernel_dir")
    initrd_hint="/boot/initramfs-${kernel_version}.img"
    if [ ! -e "$initrd_hint" ]; then
        : > "$initrd_hint"
    fi
fi
EOF
fi

kiwi_config_args=()
if [[ -z "$kiwi_part_mapper" ]] && [[ -r /sys/module/loop/parameters/max_part ]]; then
    if [[ "$(cat /sys/module/loop/parameters/max_part)" == 0 ]]; then
        kiwi_part_mapper=kpartx
    fi
fi
if [[ -n "$kiwi_part_mapper" ]]; then
    kiwi_config_file="$work_dir/kiwi.yml"
    cat > "$kiwi_config_file" <<EOF
mapper:
  - part_mapper: $kiwi_part_mapper
EOF
    kiwi_config_args+=(--config "$kiwi_config_file")
fi

cp "$work_dir/image.kiwi" "$target_dir/prepared-image.kiwi"
cp "$work_dir/config.sh" "$target_dir/prepared-config.sh"
cat > "$target_dir/compose-inputs.env" <<EOF
PROFILE=$profile
TARGET_ARCH=$target_arch
BUILD_PLATFORM=$build_platform
UPSTREAM_REPO=$upstream_repo
UPSTREAM_REPOMD_URL=$upstream_repomd_url
UPSTREAM_REPOMD_SHA256=$upstream_repomd_sha256
OVERLAY_REPO=$overlay_repo
BUILDER_BASE_IMAGE=$builder_base_image
KIWI_SOURCE_COMMIT=$kiwi_source_commit
KIWI_PART_MAPPER=$kiwi_part_mapper
EOF

kiwi_args=(
    "${kiwi_config_args[@]}"
    --profile "$profile"
    --target-arch "$target_arch"
    system build
    --description "$work_dir"
    --target-dir "$target_dir"
)

echo "Profile: $profile"
echo "Arch:    $target_arch"
echo "Platform: $build_platform"
echo "Target:  $target_dir"
echo "Upstream: $upstream_repo"
if [[ -n "$overlay_repo" ]]; then
    echo "Overlay: $overlay_repo"
fi
if [[ -n "$kiwi_part_mapper" ]]; then
    echo "Mapper:  $kiwi_part_mapper"
fi
echo "Builder base: $builder_base_image"
echo "KIWI source commit: $kiwi_source_commit"
if [[ -n "$upstream_repomd_sha256" ]]; then
    echo "Upstream repomd sha256: $upstream_repomd_sha256"
fi

if [[ -n "$sudo_cmd" ]]; then
    # shellcheck disable=SC2086
    exec $sudo_cmd kiwi-ng "${kiwi_args[@]}"
fi

exec kiwi-ng "${kiwi_args[@]}"
