#!/bin/bash
# version: 1.0.1
# created: 2026-10-31
# updated: 2026-10-31
set -euo pipefail  # Fail fast, including on unset variables and errors anywhere in a pipeline.

# Description: Bump the version header of each changed file (PATCH +1, updated = today), unless its version was already raised
# Usage: src/sh/bump_file_headers.sh <file> [file ...] (run from the repo root; pre-commit passes the staged files)

# Load reusable shell script vars & functions
source src/sh/shell_utils.sh

#=======================================================================
# Variables
#=======================================================================

TODAY="$(date +%F)"
# a header line, as an HTML comment in markdown (<!-- version: 1.2.3 -->) or a # comment elsewhere
HEADER_PREFIX='^(<!-- |# )'
BUMPED_FILES=()

#=======================================================================
# Functions
#=======================================================================

# Print the line number of a header field within a file's first 5 lines, or nothing if it's missing
header_line_number() {
    local file="${1}" field="${2}"
    head -n 5 "${file}" | grep -nE "${HEADER_PREFIX}${field}: " | head -n 1 | cut -d: -f1 || true
}

# Print a header field's value from file content on stdin, or nothing if it's missing
field_value() {
    head -n 5 | grep -oE "${HEADER_PREFIX}${1}: [^ ]+" | head -n 1 | sed -E 's/.*: //' || true
}

# Replace one header field's value on its own line, keeping the file's permissions
set_field() {
    local file="${1}" field="${2}" value="${3}" line tmp
    line="$(header_line_number "${file}" "${field}")"
    tmp="$(mktemp)"
    awk -v n="${line}" -v f="${field}" -v v="${value}" 'NR == n { sub(f ": [^ ]+", f ": " v) } { print }' "${file}" > "${tmp}"
    cat "${tmp}" > "${file}"
    rm -f "${tmp}"
}

#=======================================================================
# Main script logic
#=======================================================================

for file in "$@"; do
    # skip deleted files, files without a header, and files that are new since the last commit (they start at 1.0.0)
    if [[ ! -f "${file}" || -z "$(header_line_number "${file}" version)" ]]; then
        continue
    fi
    if ! git cat-file -e "HEAD:${file}" 2>/dev/null; then
        continue
    fi
    # skip files with no changes since the last commit (e.g. every other file under pre-commit run --all-files)
    if git diff --quiet HEAD -- "${file}"; then
        continue
    fi

    changed=false
    old_version="$(git show "HEAD:${file}" | field_value version)"
    new_version="$(field_value version < "${file}")"
    # only bump when the version wasn't already raised by hand (e.g. to a new MINOR or MAJOR)
    if [[ "${new_version}" == "${old_version}" ]]; then
        IFS=. read -r major minor patch <<< "${new_version}"
        set_field "${file}" version "${major}.${minor}.$((10#${patch} + 1))"
        changed=true
    fi
    if [[ "$(field_value updated < "${file}")" != "${TODAY}" ]]; then
        set_field "${file}" updated "${TODAY}"
        changed=true
    fi
    if [[ "${changed}" == true ]]; then
        BUMPED_FILES+=("${file}")
    fi
done

if ((${#BUMPED_FILES[@]} > 0)); then
    print_section_header "${WARNING}" "Bumped the version header of ${#BUMPED_FILES[@]} file(s) - review, re-stage and commit again:"
    printf '  %s\n' "${BUMPED_FILES[@]}"
    echo "Set MINOR or MAJOR by hand instead if the change adds or removes behaviour (see CONTRIBUTING.md)."
    exit 1
fi
