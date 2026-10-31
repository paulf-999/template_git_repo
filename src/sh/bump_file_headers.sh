#!/bin/bash
# version: 1.3.0
# created: 2026-10-31
# updated: 2026-10-31
set -euo pipefail  # Fail fast, including on unset variables and errors anywhere in a pipeline.

# Description: Bump the version header of each changed file (PATCH +1, updated = today), unless its version was already raised
#              A file moved with git mv is compared with its old path, so moving and editing it still bumps it
# Usage: src/sh/bump_file_headers.sh <file> [file ...] (run from the repo root; pre-commit passes the staged files)

# Load reusable shell script vars & functions
source src/sh/shell_utils.sh

# Catch Ctrl+C, so an interrupted run says so and exits 1
trap handle_interruption SIGINT

#=======================================================================
# Variables
#=======================================================================

TODAY="$(date +%F)"
# a header line, as an HTML comment in markdown (<!-- version: 1.2.3 -->) or a # comment elsewhere
HEADER_PREFIX='^(<!-- |# )'
VERSION_FORMAT='^[0-9]+\.[0-9]+\.[0-9]+$'
BUMPED_FILES=()
# the current file's path in the last commit, set by needs_header_check
HEAD_PATH=""
# set to true by bump_version or bump_updated when they edit the current file
FILE_CHANGED=false

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

# Print the path a file had in the last commit: its own, or the old path of a staged move, else nothing
head_path() {
    local file="${1}"
    if git cat-file -e "HEAD:${file}" 2>/dev/null; then
        echo "${file}"
        return 0
    fi
    # git lists a staged move as 'R<similarity><TAB>old path<TAB>new path'
    git diff --cached --name-status -M HEAD | awk -F'\t' -v f="${file}" '$1 ~ /^R/ && $3 == f { print $2; exit }'
}

# Succeed only for an existing file with a header that was in the last commit, at this path or a moved one,
# and has changed since. New files keep their starting 1.0.0, and unchanged ones are skipped (e.g. under
# pre-commit run --all-files), including a file that was moved but not edited
needs_header_check() {
    local file="${1}"
    [[ -f "${file}" && -n "$(header_line_number "${file}" version)" ]] || return 1
    HEAD_PATH="$(head_path "${file}")"
    [[ -n "${HEAD_PATH}" ]] || return 1
    ! git show "HEAD:${HEAD_PATH}" | cmp -s - "${file}"
}

# Stop with an error, before anything is edited, if the header can't be bumped safely
validate_header() {
    local file="${1}" version
    version="$(field_value version < "${file}")"
    if [[ ! "${version}" =~ ${VERSION_FORMAT} ]]; then
        log_message "${ERROR}" "${file}: version '${version}' isn't MAJOR.MINOR.PATCH - fix the header (see docs/maintenance/file_headers.md)."
        exit 1
    fi
    if [[ -z "$(header_line_number "${file}" updated)" ]]; then
        log_message "${ERROR}" "${file}: the header has no 'updated' line - add one (see docs/maintenance/file_headers.md)."
        exit 1
    fi
}

# Raise the PATCH version, unless it was already raised by hand (e.g. to a new MINOR or MAJOR)
bump_version() {
    local file="${1}" old_version new_version major minor patch
    old_version="$(git show "HEAD:${HEAD_PATH}" | field_value version)"
    new_version="$(field_value version < "${file}")"
    if [[ "${new_version}" != "${old_version}" ]]; then
        return 0
    fi
    IFS=. read -r major minor patch <<< "${new_version}"
    if ! patch="$(to_whole_number "${patch}")"; then
        log_message "${ERROR}" "${file}: PATCH version '${patch}' is too large to bump."
        exit 1
    fi
    set_field "${file}" version "${major}.${minor}.$((patch + 1))"
    FILE_CHANGED=true
}

# Set the updated date to today, if it isn't already
bump_updated() {
    local file="${1}"
    if [[ "$(field_value updated < "${file}")" == "${TODAY}" ]]; then
        return 0
    fi
    set_field "${file}" updated "${TODAY}"
    FILE_CHANGED=true
}

# List the bumped files and stop the commit so they can be reviewed and re-staged
report_bumped_files() {
    if ((${#BUMPED_FILES[@]} == 0)); then
        return 0
    fi
    print_section_header "${WARNING}" "Bumped the version header of ${#BUMPED_FILES[@]} file(s) - review, re-stage and commit again:"
    printf '  %s\n' "${BUMPED_FILES[@]}"
    echo "Set MINOR or MAJOR by hand instead if the change adds or removes behaviour (see docs/maintenance/file_headers.md)."
    exit 1
}

#=======================================================================
# Main script logic
#=======================================================================
print_section_header "${DEBUG}" "Script execution started."

for FILE in "$@"; do
    if ! needs_header_check "${FILE}"; then
        continue
    fi
    validate_header "${FILE}"
    FILE_CHANGED=false
    bump_version "${FILE}"
    bump_updated "${FILE}"
    if [[ "${FILE_CHANGED}" == true ]]; then
        BUMPED_FILES+=("${FILE}")
    fi
done

report_bumped_files

print_section_header "${DEBUG}" "Script execution completed." && echo
