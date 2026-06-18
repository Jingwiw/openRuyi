#!/usr/bin/env bash
set -euo pipefail

while IFS= read -r path; do
    case "$path" in
        SPECS/*/*)
            path=${path#SPECS/}
            printf '%s\n' "${path%%/*}"
            ;;
    esac
done | awk 'NF && !seen[$0]++'
