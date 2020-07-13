#!/usr/bin/env python3
"""
    Copyright 2020 Mike Pawlowski

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

# Pylint Rule Overrides

# Modules

import sys
import os
import logging
import argparse
import github

from lib.constants import constants
from lib.classes.query_processor import QueryProcessor
from lib.utils import logger_util

# Authorship

# pylint: disable=unused-variable
__author__ = "Mike Pawlowski"
__copyright__ = "Copyright 2020 Mike Pawlowski."
__license__ = "Apache 2.0"
__version__ = "1.0.1"
__maintainer__ = "Mike Pawlowski"
__email__ = "TODO"
__status__ = "Production"
# pylint: enable=unused-variable

# Globals

MIN_VERSION_PYTHON = (3, 7)

ARGUMENT_PARSER_DESCRIPTION = \
    "A Python application that searches for code in GitHub repositories based on a user-defined queries."

ARGUMENT_PARSER_EPILOG = \
    "=== Documentation ===\n" \
    "\n" \
    "https://docs.github.com/en/github/searching-for-information-on-github/searching-code\n" \
    "\n" \
    "=== Environment Variables ===\n" \
    "\n" \
    "GITHUB_ACCESS_TOKEN : A personal access token with the \"repo\" scope selected.\n" \
    "\n" \
    "=== Examples ===\n" \
    "\n" \
    "export GITHUB_ACCESS_TOKEN=cabfe35410755fbb6c281e92902ed122144886c5\n" \
    "\n" \
    "python index.py -q \"org:dap path:/ filename:package.json request\"\n" \
    "python index.py -q \"org:dap filename:deploy.properties k8s_yp_prod_eu_de_STAGE\"\n" \
    "python index.py -q \"org:dap org:data-platform path:/ filename:package.json lodash\"\n" \
    "\n" \
    "\n"

DEFAULT_LOGGER = logging.getLogger("index")

# Functions ------------------------------------------------------------------->

def _validate_python_version(logger=DEFAULT_LOGGER):
    """
    Validates whether the minimum Python interpreter version is satisfied
    """

    if sys.version_info < MIN_VERSION_PYTHON:
        logger.error("Python version %s.%s or later is required.", MIN_VERSION_PYTHON[0], MIN_VERSION_PYTHON[1])
        return False

    logger_util.log_trace(
        logger,
        "Detected Python version: %s.%s.%s",
        sys.version_info.major,
        sys.version_info.minor,
        sys.version_info.micro)

    return True


def _validate_env_vars(logger=DEFAULT_LOGGER):
    """
    Validate required environment variables
    """

    if not constants.ENV_VAR_GITHUB_ACCESS_TOKEN in os.environ:
        logger.error("Environment variable not defined: %s.", constants.ENV_VAR_GITHUB_ACCESS_TOKEN)
        return False

    return True


def _get_parsed_args():
    """
    Parse command-line arguments
    """

    parser = argparse.ArgumentParser(
        description=ARGUMENT_PARSER_DESCRIPTION,
        epilog=ARGUMENT_PARSER_EPILOG,
        formatter_class=argparse.RawTextHelpFormatter)

    # Required

    parser.add_argument(
        "-q",
        "--query",
        required=True,
        help="A user-defined GitHub query.")

    # Optional

    parser.add_argument(
        "-o",
        "--hostname",
        choices=[
            constants.GITHUB_ENTERPRISE_IBM_API_DOMAIN,
            constants.GITHUB_PUBLIC_API_DOMAIN
        ],
        default=constants.GITHUB_ENTERPRISE_IBM_API_DOMAIN,
        help="The target GitHub API domain. "
             "Default: {0}.".format(constants.GITHUB_ENTERPRISE_IBM_API_DOMAIN))

    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="Enable debug mode. "
             "Default: False.")

    args = parser.parse_args()

    return args


def _display_parsed_args(args, logger=DEFAULT_LOGGER):
    """
    Display command-line argument values
    """

    separator = "\n"
    string_buffer = (
        "Parsed Command-line Arguments:",
        "- GitHub Query: \"{0}\".".format(args.query),
        "- GitHub API Domain: {0}.".format(args.hostname),
        "- Debug Mode: {0}.".format(args.debug)
    )
    content = separator.join(string_buffer)

    logger.info(content)


def _fatal_exit(logger=DEFAULT_LOGGER):
    """
    Exit script with fatal status
    """

    status = 1
    logger.critical("Fatal error encountered. Exit script status: %d.", status)
    sys.exit(status)


def _main(logger=DEFAULT_LOGGER):
    """
    The main function.
    """

    status = False

    # Logging

    status = logger_util.init_logging_subsystem(logger)

    if status is False:
        # Should never happen
        print("Failed to initialize the logging subsystem.")
        sys.exit(1)

    # Command-line arguments

    args = _get_parsed_args()

    # Script banner

    logger.info("[-- GitHub Search -------------------------------------------------------------".upper())

    # Python version

    status = _validate_python_version()

    if status is False:
        _fatal_exit()

    # Environment variables

    status = _validate_env_vars()

    if status is False:
        _fatal_exit()

    # Display command-line argument values

    _display_parsed_args(args)

    # Enable debug mode logging

    if args.debug:
        github.enable_console_debug_logging()

    # Process the GitHub query

    query_processor = QueryProcessor(
        hostname=args.hostname,
        query=args.query)

    status = query_processor.run()

    if status is False:
        _fatal_exit()

    # Exit process

    sys.exit(0)


# Main ------------------------------------------------------------------------>

if __name__ == "__main__":
    _main()
