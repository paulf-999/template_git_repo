#!/bin/bash
# version: 1.0.1
# created: 2026-10-31
# updated: 2026-10-31
set -euo pipefail  # Fail fast, including on unset variables and errors anywhere in a pipeline.

# Description: Verify a PR title is a valid Conventional Commits header, since squash merges use it as the commit message on main
# Usage: src/sh/git_validate_pr_title.sh "<pr title>" (run from the repo root)

# Load reusable shell script vars & functions
source src/sh/shell_utils.sh

#=======================================================================
# Variables
#=======================================================================

PR_TITLE="${1:?Required: PR title (arg 1)}"
# type(scope): description, using the types allowed by @commitlint/config-conventional (type-enum)
VALID_PR_TITLE="^(build|chore|ci|docs|feat|fix|perf|refactor|revert|style|test)(\([a-z0-9._/-]+\))?!?: .+$"
# longest header commitlint allows (header-max-length)
MAX_TITLE_LENGTH=100

#=======================================================================
# Functions
#=======================================================================

# Explain why the title would fail commitlint, or print nothing if it's fine
title_problem() {
    local description="${PR_TITLE#*: }"
    if [[ ! "${PR_TITLE}" =~ ${VALID_PR_TITLE} ]]; then
        echo "Use the format 'type(scope): description', with a type such as feat, fix, docs, chore or ci, and a lowercase scope."
    elif [[ "${description}" =~ ^[A-Z] ]]; then
        echo "Start the description with a lowercase letter."
    elif [[ "${description}" == *. ]]; then
        echo "Drop the full stop at the end."
    elif (( ${#PR_TITLE} > MAX_TITLE_LENGTH )); then
        echo "Keep the title to ${MAX_TITLE_LENGTH} characters (it's ${#PR_TITLE})."
    fi
}

#=======================================================================
# Main script logic
#=======================================================================
print_section_header "${DEBUG}" "Script execution started."

PROBLEM="$(title_problem)"
if [[ -n "${PROBLEM}" ]]; then
    print_section_header "${ERROR}" "ERROR: Invalid PR title."
    printf 'PR title = %s\n\n%s\n' "${PR_TITLE}" "${PROBLEM}"
    echo "Squash merges use the PR title as the commit message on main, so it must follow Conventional Commits."
    exit 1
fi
print_section_header "${INFO}" "SUCCESS: Valid PR title"

print_section_header "${DEBUG}" "Script execution completed." && echo
