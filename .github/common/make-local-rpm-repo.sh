#!/usr/bin/env bash
set -euo pipefail

artifact_dir=${1:?usage: make-local-rpm-repo.sh <artifact-dir> <output-repo-dir>}
output_repo_dir=${2:?usage: make-local-rpm-repo.sh <artifact-dir> <output-repo-dir>}
provenance_file=${PROVENANCE_FILE:-$output_repo_dir/PROVENANCE.txt}

rm -rf "$output_repo_dir"
mkdir -p "$output_repo_dir"

mapfile -d '' rpm_files < <(
    find "$artifact_dir" -type f -name '*.rpm' \
        ! -name '*.src.rpm' \
        ! -name '*-debuginfo-*.rpm' \
        ! -name '*-debugsource-*.rpm' \
        -print0
)

if [[ ${#rpm_files[@]} -eq 0 ]]; then
    echo "no binary rpms found under $artifact_dir" >&2
    exit 1
fi

declare -A seen_rpms=()
: >"$provenance_file"

for rpm_file in "${rpm_files[@]}"; do
    rpm_name=$(basename "$rpm_file")
    if [[ -n "${seen_rpms[$rpm_name]:-}" ]]; then
        echo "duplicate rpm basename detected: $rpm_name" >&2
        echo "first: ${seen_rpms[$rpm_name]}" >&2
        echo "second: $rpm_file" >&2
        exit 1
    fi
    seen_rpms[$rpm_name]=$rpm_file
    cp "$rpm_file" "$output_repo_dir/$rpm_name"
    printf '%s\t%s\n' "$rpm_name" "$rpm_file" >>"$provenance_file"
done

createrepo_c "$output_repo_dir"
