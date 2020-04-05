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

import json
from json import JSONDecodeError
from github.GithubException import GithubException
from github.GithubException import BadAttributeException

from lib.constants import constants

# Globals

# Public Functions ------------------------------------------------------------>

def log_exception(logger, err): # pylint: disable=unused-variable
    """
    Log a general exception
    """

    separator = "\n"
    exception_name = type(err).__name__
    exception_message = str(err)
    string_buffer = (
        "Exception:",
        "Name: {0}.".format(exception_name),
        "Message: {0}.".format(exception_message)
    )
    content = separator.join(string_buffer)

    logger.exception(content)


def log_json_error(logger, err): # pylint: disable=unused-variable
    """
    Log a JSON decode exception
    """

    # See: https://docs.python.org/3/library/json.html

    exception_name = type(err).__name__

    if not isinstance(err, JSONDecodeError):
        message = "Exception is not an instance of JSONDecodeError: {0}".format(
            exception_name)
        logger.error(message)
        log_exception(logger, err)
        return

    separator = "\n"
    exception_message = str(err)
    string_buffer = (
        "Exception:",
        "Name: {0}.".format(exception_name),
        "Message: {0}.".format(err.msg),
        "Character Index: {0}.".format(err.pos),
        "Line Number: {0}.".format(err.lineno),
        "Column Number: {0}.".format(err.colno),
        "Error: {0}.".format(exception_message)
    )
    content = separator.join(string_buffer)

    logger.exception(content)
    logger.error("JSON Document:\n%s", err.doc)


def log_github_exception(logger, err): # pylint: disable=unused-variable
    """
    Log a GitHub exception
    """

    exception_name = type(err).__name__

    if not isinstance(err, GithubException):
        message = "Exception is not an instance of GithubException: {0}".format(
            exception_name)
        logger.error(message)
        log_exception(logger, err)
        return

    separator = "\n"
    exception_message = str(err)
    formatted_body = json.dumps(err.data, indent=constants.JSON_FORMAT_INDENT)
    string_buffer = (
        "Exception:",
        "Name: {0}.".format(exception_name),
        "Message: {0}.".format(exception_message),
        "Status Code: {0}.".format(err.status),
        "Data: {0}.".format(formatted_body),
    )
    content = separator.join(string_buffer)

    logger.exception(content)


def log_bad_attribute_exception(logger, err): # pylint: disable=unused-variable
    """
    Log a GitHub bad attribute exception
    """

    exception_name = type(err).__name__

    if not isinstance(err, BadAttributeException):
        message = "Exception is not an instance of BadAttributeException: {0}".format(
            exception_name)
        logger.error(message)
        log_exception(logger, err)
        return

    separator = "\n"
    exception_message = str(err)
    string_buffer = (
        "Exception:",
        "Name: {0}.".format(exception_name),
        "Message: {0}.".format(exception_message),
        "Actual Value: {0}.".format(err.actual_value),
        "Expected Type: {0}.".format(err.expected_type),
        "Transformation Exception: {0}.".format(err.transformation_exception)
    )
    content = separator.join(string_buffer)

    logger.exception(content)
