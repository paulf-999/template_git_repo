#!/bin/bash
# version: 1.0.0
# created: 2025-10-14
# updated: 2026-10-30
set -e  # Exit immediately if a command exits with a non-zero status (fail fast).
# Also fail on unset variables and on errors anywhere in a pipeline
set -uo pipefail

# Interactive commit helper that enforces "<type>(<scope>): <message>", where scope is the area of the repo changed
# Usage: src/sh/git_commit.sh [git commit flags, e.g. --no-verify] (run from the repo root)

# Load reusable shell script vars & functions
source src/sh/shell_utils.sh

#=======================================================================
# Variables
#=======================================================================

# allowed commit types, kept in step with the type-enum rule in @commitlint/config-conventional
TYPES=("chore" "docs" "feat" "refactor" "fix" "test" "perf" "build" "ci" "revert" "style")

# globals, initialised to satisfy set -u
STAGED=()
AREAS=()
TYPE=""
SCOPE=""
MSG=""
COMMIT_MSG=""
# every script argument is passed through to git commit
GIT_FLAGS=("$@")

#=======================================================================
# Functions
#=======================================================================

# Build a regex alternation from TYPES (e.g. chore|docs|feat|fix)
build_types_alt() {
    local IFS='|'
    echo "${TYPES[*]}"
}

# Menu for commit type
select_type() {
    log_message "${DEBUG}" "Select type of Git commit:\n"

    while true; do
        for i in "${!TYPES[@]}"; do
            local idx=$((i+1))
            echo -e "${DEBUG_DETAILS}${idx}) ${TYPES[$i]}${COLOUR_OFF}"
        done
        echo
        read -rp "$(echo -e "${DEBUG}Enter number for type: ${COLOUR_OFF}")" choice

        if [[ "${choice}" =~ ^[0-9]+$ ]] && (( choice>=1 && choice<=${#TYPES[@]} )); then
            TYPE="${TYPES[$((choice-1))]}"
            break
        else
            log_message "${ERROR}" "Invalid selection. Choose a valid number."
        fi
    done
}

# Gather staged files, using a while-read loop that works on older Bash too
gather_staged_files() {
    STAGED=()
    while IFS= read -r line; do
        # an if, not [[ ]] &&, so an empty line can't trip set -e
        if [[ -n "${line}" ]]; then
            STAGED+=("${line}")
        fi
    done < <(git diff --cached --name-only 2>/dev/null || printf '')
}

# Map a staged path to its repo area: the top-level folder, or for a root-level file its name
# without the extension, lowercased with any leading dot dropped (e.g. Makefile -> makefile, .github/x.yml -> github)
path_to_area() {
    local path="${1}"
    local area
    if [[ "${path}" == */* ]]; then
        area="${path%%/*}"
    else
        area="${path%.*}"
        # a dotfile with no other dot (e.g. .gitignore) would otherwise come out empty
        if [[ -z "${area}" ]]; then
            area="${path}"
        fi
    fi
    area="${area#.}"
    printf '%s\n' "${area}" | tr '[:upper:]' '[:lower:]'
}

# Collect the unique repo areas of the staged files, in the order they're first seen
build_areas() {
    AREAS=()
    local path area existing seen
    for path in "${STAGED[@]}"; do
        area="$(path_to_area "${path}")"
        seen=false
        # the ${arr[@]+...} form keeps an empty array safe under set -u on older Bash
        for existing in ${AREAS[@]+"${AREAS[@]}"}; do
            if [[ "${existing}" == "${area}" ]]; then
                seen=true
            fi
        done
        if [[ "${seen}" == false ]]; then
            AREAS+=("${area}")
        fi
    done
}

# Menu for commit scope (the area of the repo changed)
select_scope() {
    echo -e "\n${DEBUG}Pick the scope, i.e. the area of the repo changed (used as (<scope>) in the subject):\n${COLOUR_OFF}"

    if ((${#STAGED[@]} > 0)); then
        build_areas
        for i in "${!AREAS[@]}"; do
            local idx=$((i+1))
            echo -e "${DEBUG_DETAILS}${idx}) ${AREAS[$i]}${COLOUR_OFF}"
        done
        echo -e "${DEBUG_DETAILS}0) Enter custom scope${COLOUR_OFF}"
    else
        echo -e "${DEBUG_DETAILS}(no staged files detected)${COLOUR_OFF}"
    fi

    while true; do
        read -rp "$(echo -e "\n${DEBUG}Choose number (or 0 to type): ${COLOUR_OFF}")" scope_choice

        if ((${#AREAS[@]} > 0)) && [[ "${scope_choice}" =~ ^[0-9]+$ ]] && (( scope_choice>=1 && scope_choice<=${#AREAS[@]} )); then
            SCOPE="${AREAS[$((scope_choice-1))]}"
            break
        elif [[ "${scope_choice}" == "0" || ${#AREAS[@]} -eq 0 ]]; then
            read -rp "$(echo -e "${DEBUG}Enter custom scope (e.g. makefile, ci, pre-commit): ${COLOUR_OFF}")" SCOPE
            SCOPE="${SCOPE// /-}"
            if [[ -n "${SCOPE}" ]]; then
                break
            else
                log_message "${ERROR}" "Scope cannot be empty."
            fi
        else
            log_message "${ERROR}" "Invalid selection."
        fi
    done
}

# Prompt for commit message body
prompt_message() {
    read -rp "$(echo -e "${DEBUG}Enter commit message: ${COLOUR_OFF}")" MSG
    if [[ -z "${MSG}" ]]; then
        log_message "${ERROR}" "Commit message cannot be empty."
        exit 1
    fi
}

# Build, validate and commit
build_commit_message() {
    COMMIT_MSG="${TYPE}(${SCOPE}): ${MSG}"
}

validate_commit_message() {
    local types_alt REGEX
    types_alt="$(build_types_alt)"
    REGEX="^(${types_alt})\([^)]+\): .+"
    if ! [[ "${COMMIT_MSG}" =~ ${REGEX} ]]; then
        log_message "${ERROR}" "Commit subject must match ${REGEX}"
        echo "Got: ${COMMIT_MSG}"
        exit 1
    fi
}

confirm_and_commit() {
    echo -e "\n${DEBUG}Final commit:${COLOUR_OFF} ${COMMIT_MSG}"
    read -rp "Proceed? [y/N] " confirm
    [[ "${confirm}" =~ ^[Yy]$ ]] || exit 0

    if ((${#GIT_FLAGS[@]} > 0)); then
        git commit "${GIT_FLAGS[@]}" -m "${COMMIT_MSG}"
    else
        git commit -m "${COMMIT_MSG}"
    fi
}

#=======================================================================
# Main script logic
#=======================================================================
print_section_header "${DEBUG}" "Script execution started."

# Ensure we're in a git repo
if ! git rev-parse --git-dir >/dev/null 2>&1; then
    log_message "${ERROR}" "Not a git repository."
    exit 1
fi

select_type
gather_staged_files
select_scope
prompt_message
build_commit_message
validate_commit_message
confirm_and_commit

print_section_header "${DEBUG}" "Script execution completed." && echo
