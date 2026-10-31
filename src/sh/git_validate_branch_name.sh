#!/bin/bash
# version: 1.1.0
# created: 2023-07-09
# updated: 2026-10-31
set -euo pipefail  # Fail fast, including on unset variables and errors anywhere in a pipeline.

# Description: Verify the git branch name follows the naming standard: ^(feature|hotfix|release)/[a-z0-9_]+$
# Usage: src/sh/git_validate_branch_name.sh [git branch name]
#        (defaults to the current local git branch name; run from the repo root)

# Load reusable shell script vars & functions
source src/sh/shell_utils.sh

# Catch Ctrl+C, so an interrupted run says so and exits 1
trap handle_interruption SIGINT

#=======================================================================
# Variables
#=======================================================================

# use the branch name passed in, else the name of the local git branch
LOCAL_GIT_BRANCH_NAME="${1:-$(git rev-parse --abbrev-ref HEAD)}"
# the regex for valid git branch names
VALID_GIT_BRANCH_NAME="^(feature|hotfix|release)/[a-z0-9_]+$"

#=======================================================================
# Functions
#=======================================================================

# Explain the naming standard and how to fix an invalid branch name
print_branch_name_error() {
    print_section_header "${ERROR}" "ERROR: Invalid Git branch name."
    echo -e "Local git branch name = ${LOCAL_GIT_BRANCH_NAME}"
    echo
    echo -e "Git branch name needs to adhere to the following regex: ${VALID_GIT_BRANCH_NAME}."
    echo
    echo -e "I.e., it needs to:"
    echo
    echo -e "* Start with either 'feature/', 'hotfix/' or 'release/'"
    echo -e "* Followed by a snake_case description of your change (note, hyphens aren't allowed)."
    echo
    echo -e "E.g.: feature/add_login_page, hotfix/fix_null_check or release/reformat_all_models"
    echo
}

#=======================================================================
# Main script logic
#=======================================================================
print_section_header "${DEBUG}" "Script execution started."

# Validate the Git branch name used
# the regex must stay unquoted, or [[ =~ ]] matches it as a literal string
if [[ ! "${LOCAL_GIT_BRANCH_NAME}" =~ ${VALID_GIT_BRANCH_NAME} ]]
then
    print_branch_name_error
    exit 1
fi
print_section_header "${INFO}" "SUCCESS: Valid Git branch name"

print_section_header "${DEBUG}" "Script execution completed." && echo
