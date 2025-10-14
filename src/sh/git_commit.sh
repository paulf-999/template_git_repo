#!/bin/bash
# Interactive commit helper that enforces "<type>(<file>): <message>"
# Usage: git_commit.sh [--no-verify] [--no-body]
#   --no-body -> subject is exactly "<type>(<file>)" (no message body)

# Keep nounset; avoid -e to prevent abrupt exits during prompts/subshells.
set -uo pipefail

# Try to source shell utils; continue without colours if missing
if ! source src/sh/shell_utils.sh 2>/dev/null; then
    DEBUG=""; DEBUG_DETAILS=""; COLOUR_OFF=""; ERROR=""
    log_message() { printf '%s\n' "$2"; }
fi

# Ensure we're in a git repo
if ! git rev-parse --git-dir >/dev/null 2>&1; then
    log_message "${ERROR}" "Not a git repository."
    exit 1
fi

# -----------------------------
# Configuration
# -----------------------------
TYPES=("chore" "docs" "feat" "fix")   # allowed commit types

# -----------------------------
# Globals (init to satisfy -u)
# -----------------------------
STAGED=()
DISPLAY_NAMES=()
TYPE=""
SCOPE=""
MSG=""
COMMIT_MSG=""
NO_BODY=false
GIT_FLAGS=()

# -----------------------------
# Helpers
# -----------------------------
# Truncate long filenames for commit scope/menu, keeping extension
truncate_scope() {
    local name="$1"
    local max_len=30  # max chars before extension

    local base ext
    if [[ "$name" == *.* && "${name##*.}" != "$name" ]]; then
        base="${name%.*}"
        ext=".${name##*.}"
    else
        base="$name"
        ext=""
    fi

    if ((${#base} > max_len)); then
        printf '%s\n' "${base:0:$max_len}…${ext}"
    else
        printf '%s\n' "${base}${ext}"
    fi
}

# Build a regex alternation from TYPES (e.g. chore|docs|feat|fix)
build_types_alt() {
    local IFS='|'
    echo "${TYPES[*]}"
}

# -----------------------------
# Argument parsing
# -----------------------------
parse_args() {
    for arg in "$@"; do
        case "$arg" in
            --no-body) NO_BODY=true ;;
            *) GIT_FLAGS+=("$arg") ;;
        esac
    done
}

# -----------------------------
# Menu for commit type
# -----------------------------
select_type() {
    log_message "${DEBUG}" "Select type of Git commit:\n"

    while true; do
        for i in "${!TYPES[@]}"; do
            local idx=$((i+1))
            echo -e "${DEBUG_DETAILS}${idx}) ${TYPES[$i]}${COLOUR_OFF}"
        done
        echo
        read -rp "$(echo -e "${DEBUG}Enter number for type: ${COLOUR_OFF}")" choice

        if [[ "$choice" =~ ^[0-9]+$ ]] && (( choice>=1 && choice<=${#TYPES[@]} )); then
            TYPE="${TYPES[$((choice-1))]}"
            break
        else
            log_message "${ERROR}" "Invalid selection. Choose a valid number."
        fi
    done
}

# -----------------------------
# Gather staged files (portable & robust)
# -----------------------------
gather_staged_files() {
    STAGED=()
    # Use a while-read fallback that works on older Bash too
    while IFS= read -r line; do
        [[ -n "$line" ]] && STAGED+=("$line")
    done < <(git diff --cached --name-only 2>/dev/null || printf '')
}

# Build display names for menu: truncated basenames w/ extension,
# disambiguate duplicates by appending parent dir in [brackets].
build_menu_display_names() {
    DISPLAY_NAMES=()
    for i in "${!STAGED[@]}"; do
        local filename
        filename="$(basename -- "${STAGED[$i]}")"
        DISPLAY_NAMES[$i]="$(truncate_scope "$filename")"
    done
    # Disambiguate duplicates (simple O(n^2) pass)
    for i in "${!DISPLAY_NAMES[@]}"; do
        local dup_count=0
        for j in "${!DISPLAY_NAMES[@]}"; do
            [[ "${DISPLAY_NAMES[$j]}" == "${DISPLAY_NAMES[$i]}" ]] && ((dup_count++))
        done
        if (( dup_count > 1 )); then
            local parent
            parent="$(basename -- "$(dirname -- "${STAGED[$i]}")")"
            DISPLAY_NAMES[$i]="${DISPLAY_NAMES[$i]} [${parent}]"
        fi
    done
}

# -----------------------------
# Menu for commit scope (file/directory)
# -----------------------------
select_scope() {
    echo -e "\n${DEBUG}Pick the file scope (used as (<file>) in the subject):\n${COLOUR_OFF}"

    if ((${#STAGED[@]} > 0)); then
        build_menu_display_names
        for i in "${!STAGED[@]}"; do
            local idx=$((i+1))
            echo -e "${DEBUG_DETAILS}${idx}) ${DISPLAY_NAMES[$i]}${COLOUR_OFF}"
        done
        echo -e "${DEBUG_DETAILS}0) Enter custom scope${COLOUR_OFF}"
    else
        echo -e "${DEBUG_DETAILS}(no staged files detected)${COLOUR_OFF}"
    fi

    while true; do
        read -rp "$(echo -e "\n${DEBUG}Choose number (or 0 to type): ${COLOUR_OFF}")" scope_choice

        if ((${#STAGED[@]} > 0)) && [[ "$scope_choice" =~ ^[0-9]+$ ]] && (( scope_choice>=1 && scope_choice<=${#STAGED[@]} )); then
            local filename
            filename="$(basename -- "${STAGED[$((scope_choice-1))]}")"
            SCOPE="$(truncate_scope "$filename")"
            break
        elif [[ "$scope_choice" == "0" || ${#STAGED[@]} -eq 0 ]]; then
            read -rp "$(echo -e "${DEBUG}Enter custom scope (e.g. file or directory): ${COLOUR_OFF}")" SCOPE
            SCOPE="${SCOPE// /-}"
            if [[ -n "$SCOPE" ]]; then
                break
            else
                log_message "${ERROR}" "Scope cannot be empty."
            fi
        else
            log_message "${ERROR}" "Invalid selection."
        fi
    done
}

# -----------------------------
# Prompt for commit message body (unless --no-body)
# -----------------------------
prompt_message() {
    if ${NO_BODY}; then
        MSG=""
        return
    fi
    read -rp "$(echo -e "${DEBUG}Enter commit message: ${COLOUR_OFF}")" MSG
    if [[ -z "$MSG" ]]; then
        log_message "${ERROR}" "Commit message cannot be empty."
        exit 1
    fi
}

# -----------------------------
# Build, validate and commit
# -----------------------------
build_commit_message() {
    if ${NO_BODY}; then
        COMMIT_MSG="${TYPE}(${SCOPE})"
    else
        COMMIT_MSG="${TYPE}(${SCOPE}): ${MSG}"
    fi
}

validate_commit_message() {
    local types_alt REGEX
    types_alt="$(build_types_alt)"
    if ${NO_BODY}; then
        REGEX="^(${types_alt})\([^)]+\)$"
    else
        REGEX="^(${types_alt})\([^)]+\): .+"
    fi
    if ! [[ "$COMMIT_MSG" =~ $REGEX ]]; then
        log_message "${ERROR}" "Commit subject must match ${REGEX}"
        echo "Got: $COMMIT_MSG"
        exit 1
    fi
}

confirm_and_commit() {
    echo -e "\n${DEBUG}Final commit:${COLOUR_OFF} $COMMIT_MSG"
    read -rp "Proceed? [y/N] " confirm
    [[ "$confirm" =~ ^[Yy]$ ]] || exit 0

    # Expand GIT_FLAGS safely under set -u
    if declare -p GIT_FLAGS >/dev/null 2>&1 && ((${#GIT_FLAGS[@]} > 0)); then
        git commit "${GIT_FLAGS[@]}" -m "$COMMIT_MSG"
    else
        git commit -m "$COMMIT_MSG"
    fi
}

# -----------------------------
# Main
# -----------------------------
parse_args "$@"
select_type
gather_staged_files
select_scope
prompt_message
build_commit_message
validate_commit_message
confirm_and_commit
