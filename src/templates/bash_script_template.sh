#!/bin/bash
# version: 1.0.0
# created: 2025-10-14
# updated: 2026-10-30
set -euo pipefail  # Fail fast, including on unset variables and errors anywhere in a pipeline.

# <One line saying what this script does>
# Usage: src/sh/<script_name>.sh [args] (run from the repo root)

# Load reusable shell script vars & functions
source src/sh/shell_utils.sh

# Catch Ctrl+C, so an interrupted run says so and exits 1
trap handle_interruption SIGINT

#=======================================================================
# Variables
#=======================================================================

# shellcheck disable=SC2034  # intentionally unused: template placeholders
variable1="value1"

#=======================================================================
# Functions
#=======================================================================

# TODO: add functions here

#=======================================================================
# Main script logic
#=======================================================================
print_section_header "${DEBUG}" "Script execution started."

# TODO: add your code here

print_section_header "${DEBUG}" "Script execution completed." && echo
