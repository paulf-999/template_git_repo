#!/bin/bash
# version: 1.2.0
# created: 2025-10-14
# updated: 2026-10-30
set -euo pipefail  # Fail fast, including on unset variables and errors anywhere in a pipeline.

# Interactive commit helper that enforces "<type>(<scope>): <message>", where scope is the area of the repo changed
# Usage: src/sh/git_commit.sh [git commit flags, e.g. --no-verify] (run from the repo root)

# Load reusable shell script vars & functions
source src/sh/shell_utils.sh

#=======================================================================
# Variables
#=======================================================================

# allowed commit types, kept in step with the type-enum rule in @commitlint/config-conventional
TYPES=("chore" "docs" "feat" "refactor" "fix" "test" "perf" "build" "ci" "revert" "style")
# longest header commitlint allows (header-max-length in @commitlint/config-conventional)
MAX_HEADER_LENGTH=100
# longest custom scope, leaving room in the header for the message
MAX_SCOPE_LENGTH=30

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

        local number
        # -1 marks an answer that isn't a whole number
        number="$(to_whole_number "${choice}")" || number=-1
        if (( number>=1 && number<=${#TYPES[@]} )); then
            TYPE="${TYPES[$((number-1))]}"
            break
        else
            log_message "${ERROR}" "Invalid selection. Choose a valid number."
        fi
    done
}

# Gather staged files, using a while-read loop that works on older Bash too
# -z gives raw NUL-separated paths, so names like résumé.md aren't quoted and escaped
gather_staged_files() {
    STAGED=()
    while IFS= read -r -d '' line; do
        # an if, not [[ ]] &&, so an empty line can't trip set -e
        if [[ -n "${line}" ]]; then
            STAGED+=("${line}")
        fi
    done < <(git diff --cached --name-only -z 2>/dev/null || printf '')
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

        local number
        number="$(to_whole_number "${scope_choice}")" || number=-1
        if (( number>=1 && number<=${#AREAS[@]} )); then
            SCOPE="${AREAS[$((number-1))]}"
            break
        elif (( number==0 || ${#AREAS[@]}==0 )); then
            read -rp "$(echo -e "${DEBUG}Enter custom scope (e.g. makefile, ci, pre-commit): ${COLOUR_OFF}")" SCOPE
            # commitlint requires a lowercase scope (scope-case), so match the auto-detected areas
            SCOPE="$(printf '%s' "${SCOPE// /-}" | tr '[:upper:]' '[:lower:]')"
            if [[ -z "${SCOPE}" ]]; then
                log_message "${ERROR}" "Scope cannot be empty."
            elif [[ ! "${SCOPE}" =~ ^[a-z0-9][a-z0-9._/-]*$ ]]; then
                log_message "${ERROR}" "Use only letters, numbers and . _ / - in the scope."
            elif (( ${#SCOPE} > MAX_SCOPE_LENGTH )); then
                log_message "${ERROR}" "Keep the scope to ${MAX_SCOPE_LENGTH} characters."
            else
                break
            fi
        else
            log_message "${ERROR}" "Invalid selection."
        fi
    done
}

# Explain why a message would fail commitlint, or print nothing if it's fine
message_problem() {
    local message="${1}"
    local max_length=$((MAX_HEADER_LENGTH - ${#TYPE} - ${#SCOPE} - 4))
    if [[ -z "${message}" ]]; then
        echo "Commit message cannot be empty."
    elif [[ "${message}" =~ ^[A-Z] ]]; then
        echo "Start the message with a lowercase letter (commitlint rejects sentence, start and upper case)."
    elif [[ "${message}" == *. ]]; then
        echo "Drop the full stop at the end of the message."
    elif (( ${#message} > max_length )); then
        echo "Keep the message to ${max_length} characters, so the whole header fits in ${MAX_HEADER_LENGTH}."
    fi
}

# Prompt for the commit message until it would pass commitlint
prompt_message() {
    local problem
    while true; do
        read -rp "$(echo -e "${DEBUG}Enter commit message: ${COLOUR_OFF}")" MSG
        # trim surrounding spaces, so an all-spaces message counts as empty
        MSG="$(printf '%s' "${MSG}" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')"
        problem="$(message_problem "${MSG}")"
        if [[ -z "${problem}" ]]; then
            break
        fi
        log_message "${ERROR}" "${problem}"
    done
}

# Build and commit (type, scope and message are already checked as they're entered)
build_commit_message() {
    COMMIT_MSG="${TYPE}(${SCOPE}): ${MSG}"
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
confirm_and_commit

print_section_header "${DEBUG}" "Script execution completed." && echo
