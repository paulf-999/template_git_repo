SHELL = /bin/sh

#================================================================
# Usage
#================================================================
# make installations	# install the package for the first time, managing dependencies & performing a housekeeping cleanup too
# make deps		# just install the dependencies
# make install		# perform the end-to-end install
# make clean		# perform a housekeeping cleanup



.EXPORT_ALL_VARIABLES: validate_user_ip

CONFIG_FILE := config.yaml
# the 2 vars below are just for formatting CLI message output
YELLOW := \033[0;33m
COLOUR_OFF := \033[0m

installations: deps install clean

deps: get_ips
	@echo "----------------------------------------------------------------------------------------------------------------------"
	@echo "${YELLOW}Target: 'deps'. Download the relevant pip package dependencies (note: ignore the pip depedency resolver errors.)${COLOUR_OFF}"
	@echo "----------------------------------------------------------------------------------------------------------------------"
	@virtualenv -p python3 venv; \
	source venv/bin/activate; \
	pip3 install -r requirements.txt; \

install: get_ips
	@echo "------------------------------------------------------------------"
	@echo "${YELLOW}Target: 'install'. Run the setup and install targets.${COLOUR_OFF}"
	@echo "------------------------------------------------------------------"

clean:
	@echo "------------------------------------------------------------------"
	@echo "${YELLOW}Target 'clean'. Remove any redundant files, e.g. downloads.${COLOUR_OFF}"
	@echo "------------------------------------------------------------------"

#############################################################################################
# Setup/validation targets: 'get_ips' & 'validate_user_ip'
#############################################################################################
get_ips:
	@echo "------------------------------------------------------------------"
	@echo "${YELLOW}Target: 'get_ips'. Get input args from config.yaml.${COLOUR_OFF}"
	@echo "------------------------------------------------------------------"
	$(eval CURRENT_DIR=$(shell pwd))
	$(eval ENV=$(shell yq -r '.general_params.env | select( . != null )' ${CONFIG_FILE}))

validate_user_ip: get_ips
	@echo "------------------------------------------------------------------"
	@echo "${YELLOW}Target: 'validate_user_ip'. Validate the user inputs.${COLOUR_OFF}"
	@echo "------------------------------------------------------------------"
	# INFO: Verify the user has provided a value for the key 'env' in ip/config.yaml
	@[ "${ENV}" ] || ( echo "\nError: 'ENV' key is empty in ip/config.yaml\n"; exit 1 )
