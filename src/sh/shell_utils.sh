#!/bin/bash
# version: 1.0.0
# created: 2025-09-12
# updated: 2026-10-30
# Reusable shell script vars & functions, sourced by other scripts (not run directly)
# ignore shell warnings, re: variables being unused
# shellcheck disable=SC2034

# Stop if run directly, since this file only defines vars & functions for other scripts
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    echo "shell_utils.sh is meant to be sourced by other scripts, not run directly." >&2
    exit 1
fi

#=======================================================================
# Variables
#=======================================================================

# setup colour formatting, using ANSI escape codes
# cyan (for debug messages)
DEBUG='\033[0;36m'
# purple (for lower-level debugging messages)
DEBUG_DETAILS='\033[0;35m'
# green (for informational messages)
INFO='\033[0;32m'
# yellow (for warning messages)
WARNING='\033[0;33m'
# red (for error messages)
ERROR='\033[0;31m'
# bold red (for critical errors)
CRITICAL='\033[1;31m'
# Text Reset
COLOUR_OFF='\033[0m'

#=======================================================================
# Functions
#=======================================================================

# Function to standardise log messaging
# Usage: log_message <level> <message> [leading blank line: true (default) or false]
log_message() {
    local LOGGING_LEVEL="${1}"
    local MESSAGE="${2}"
    local LEADING_BLANK_LINE="${3:-true}"
    if [[ "${LEADING_BLANK_LINE}" == true ]]; then
        echo
    fi
    echo -e "${LOGGING_LEVEL}${MESSAGE}${COLOUR_OFF}"
}

# Function to standardise log messaging - re: section headers
print_section_header() {
    local LOG_LEVEL="${1}"
    local MESSAGE="${2}"
    echo && echo -e "${LOG_LEVEL}#--------------------------------------------------------------------------------------------"
    echo -e "${LOG_LEVEL}# ${MESSAGE}${COLOUR_OFF}"
    echo -e "${LOG_LEVEL}#--------------------------------------------------------------------------------------------${COLOUR_OFF}"
}

# Function to check if a directory exists
dir_exists() {
    [[ -d "${1}" ]]
}

# Function to check if a file exists
file_exists() {
    [[ -f "${1}" ]]
}

# Signal handler to catch interruptions (Ctrl+C)
handle_interruption() {
    log_message "${WARNING}" "Script execution aborted by the user."
    exit 1
}
