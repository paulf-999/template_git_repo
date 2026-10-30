# version: 1.0.0
# created: 2025-01-14
# updated: 2026-10-30
#=======================================================================
# Variables
#=======================================================================

# ANSI escape codes for color formatting
# cyan (for debug messages)
DEBUG := \033[0;36m
# purple (for lower-level debugging messages)
DEBUG_DETAILS := \033[0;35m
# green (for informational messages)
INFO := \033[0;32m
# yellow (for warning messages)
WARNING := \033[0;33m
# red (for error messages)
ERROR := \033[0;31m
# bold red (for critical errors)
CRITICAL := \033[1;31m
# reset text color
COLOUR_OFF := \033[0m
