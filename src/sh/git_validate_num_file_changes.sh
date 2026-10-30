#!/bin/bash
# version: 1.0.0
# created: 2026-10-30
# updated: 2026-10-30
set -euo pipefail  # Fail fast, including on unset variables and errors anywhere in a pipeline.

# Fail a PR that changes more than the max number of files, unless it's on a release/ branch
# Usage: src/sh/git_validate_num_file_changes.sh <git branch name> <base ref> [head ref]
#        (head ref defaults to HEAD; run from the repo root)

# Load reusable shell script vars & functions
source src/sh/shell_utils.sh

#=======================================================================
# Variables
#=======================================================================

GIT_BRANCH_NAME="${1:?Required: git branch name (arg 1)}"
BASE_REF="${2:?Required: base ref to compare against (arg 2)}"
HEAD_REF="${3:-HEAD}"
# maximum number of files a PR can change; override via the MAX_FILES_ALLOWED env var
MAX_FILES_CHANGED="${MAX_FILES_ALLOWED:-20}"
# how many changed files to list before summarising the rest
MAX_FILES_LISTED=50

#=======================================================================
# Functions
#=======================================================================

# Check a ref resolves to a commit
ref_exists() {
    git rev-parse --verify --quiet "${1}^{commit}" >/dev/null
}

#=======================================================================
# Main script logic
#=======================================================================
print_section_header "${DEBUG}" "Script execution started."

# release branches are for large bulk changes (see docs/git_branching_strategy.md), so they skip the check
if [[ "${GIT_BRANCH_NAME}" == release/* ]]; then
    print_section_header "${INFO}" "Release branch - skip file count check." && echo
    exit 0
fi

# outside CI the base may not be fetched yet, so try fetching it from origin before giving up
if ! ref_exists "${BASE_REF}"; then
    log_message "${DEBUG_DETAILS}" "Base ref ${BASE_REF} not found locally - fetching it from origin."
    if git fetch --quiet --no-tags origin "${BASE_REF#origin/}" 2>/dev/null && ! ref_exists "${BASE_REF}"; then
        # a local branch name that only exists on origin lands in FETCH_HEAD
        BASE_REF="FETCH_HEAD"
    fi
    if ! ref_exists "${BASE_REF}"; then
        print_section_header "${ERROR}" "ERROR: base ref ${BASE_REF} not found, locally or on origin."
        exit 1
    fi
fi

# list added, deleted, modified and renamed files since the branch left the base
CHANGED_FILES=$(git diff --name-only --diff-filter=ADMR "${BASE_REF}...${HEAD_REF}")
# count non-empty lines; grep exits 1 when there are none, so don't let set -e stop the script
FILE_COUNT=$(grep -c . <<< "${CHANGED_FILES}" || true)

log_message "${DEBUG_DETAILS}" "Files changed (${FILE_COUNT}):"
# list the first files only, so a very large PR doesn't flood the log
head -n "${MAX_FILES_LISTED}" <<< "${CHANGED_FILES}"
if [[ "${FILE_COUNT}" -gt "${MAX_FILES_LISTED}" ]]; then
    echo "... and $((FILE_COUNT - MAX_FILES_LISTED)) more"
fi

if [[ "${FILE_COUNT}" -gt "${MAX_FILES_CHANGED}" ]]; then
    print_section_header "${ERROR}" "ERROR: number of files changed in PR (${FILE_COUNT}) exceeds the max (${MAX_FILES_CHANGED})."
    echo -e "Split the PR by logical area, or use a release/ branch for one bulk change (see docs/git_branching_strategy.md)."
    exit 1
fi
print_section_header "${INFO}" "SUCCESS: number of changed files (${FILE_COUNT}) is within the max (${MAX_FILES_CHANGED})."

print_section_header "${DEBUG}" "Script execution completed." && echo
