SHELL = /bin/sh

#================================================================
# Usage
#================================================================
# make help		# list the available targets
# make deps		# install the dependencies and git hooks
# make install		# perform the end-to-end install
# make run		# launch the service
# make test		# run the tests (pytest)
# make clean		# perform a housekeeping cleanup

#=======================================================================
# Variables
#=======================================================================
.EXPORT_ALL_VARIABLES:

# load variables from separate file
include src/make/variables.mk # load variables from a separate makefile file

#=======================================================================
# Targets
#=======================================================================
all: deps install

help:
	@echo "${INFO}\nAvailable targets:${COLOUR_OFF}\n"
	@sed -n 's/^# make /make /p' Makefile

deps:
	@echo "${INFO}\nCalled makefile target 'deps'. Download any required libraries.${COLOUR_OFF}\n"
	@pip install -r requirements-dev.txt
	@pre-commit install

install:
	@echo "${INFO}\nCalled makefile target 'install'. Run the setup & install targets.\n${COLOUR_OFF}"

run:
	@echo "${INFO}\nCalled makefile target 'run'. Launch service.${COLOUR_OFF}\n"

test:
	@echo "${INFO}\nCalled makefile target 'test'. Perform any required tests.${COLOUR_OFF}\n"
	@pytest

clean:
	@echo "${INFO}\nCalled makefile target 'clean'. Restoring the repository to its initial state.${COLOUR_OFF}\n"

# Phony targets
.PHONY: all help deps install run test clean

# .PHONY tells Make that these targets don't represent files
# This prevents conflicts with any files named "all" or "clean"
