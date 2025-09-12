#!/bin/bash
# ignore shell warnings, re: variables being unused
# shellcheck disable=SC2034

#=======================================================================
# Variables
#=======================================================================

# setup colour formatting
# ANSI escape codes for color formatting
DEBUG='\033[0;36m' # cyan (for debug messages)
DEBUG_DETAILS='\033[0;35m' # purple (for lower-level debugging messages)
INFO='\033[0;32m' # green (for informational messages)
WARNING='\033[0;33m' # yellow (for warning messages)
ERROR='\033[0;31m' # red (for error messages)
CRITICAL='\033[1;31m' # bold red (for critical errors)
COLOUR_OFF='\033[0m' # Text Reset

# Function to check if a directory exists
dir_exists() {
    [ -d "$1" ]
}

# Function to check if a file exists
file_exists() {
    [ -f "$1" ]
}

log_message() {
    local LOGGING_LEVEL="$1"
    local MESSAGE="$2"
    echo && echo -e "${LOGGING_LEVEL}${MESSAGE}${COLOUR_OFF}"
}

print_section_header() {
    local LOG_LEVEL="$1"
    local MESSAGE="$2"
    echo && echo -e "${LOG_LEVEL}#--------------------------------------------------------------------------------------------"
    echo -e "${LOG_LEVEL}# ${MESSAGE}${COLOUR_OFF}"
    echo -e "${LOG_LEVEL}#--------------------------------------------------------------------------------------------${COLOUR_OFF}"
}

print_error_message() {
    local MESSAGE="$1"
    echo && echo -e "${ERROR}${MESSAGE}${COLOUR_OFF}"
}

# Signal handler to catch interruptions (Ctrl+C)
handle_interruption() {
    print_info_message "Script execution aborted by the user."
    exit 1
}
