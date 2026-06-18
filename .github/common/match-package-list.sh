#!/usr/bin/env bash
set -euo pipefail

package_list=${1:?usage: match-package-list.sh <package-list>}
tmp_file=$(mktemp)

cleanup() {
    rm -f "$tmp_file"
}
trap cleanup EXIT INT TERM

grep -v '^[[:space:]]*#' "$package_list" | sed '/^[[:space:]]*$/d' | sort -u >"$tmp_file"

while IFS= read -r package; do
    if [[ -n "$package" ]] && grep -Fxq "$package" "$tmp_file"; then
        printf '%s\n' "$package"
    fi
done | awk 'NF && !seen[$0]++'
