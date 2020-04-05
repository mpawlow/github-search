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

import os
import logging
import datetime
import json
import github

from lib.constants import constants
from lib.utils import error_util

# Globals

LINE_1 = '=' * 80
LINE_2 = '-' * 80

DEFAULT_LOGGER = logging.getLogger("query_processor")

# Classes --------------------------------------------------------------------->

class QueryProcessor: # pylint: disable=unused-variable
    """
    A GitHub query processor
    """

    def __init__(self, hostname, query):
        """
        Constructor
        """

        self._hostname = hostname
        self._query = query

        self._access_token = os.environ[constants.ENV_VAR_GITHUB_ACCESS_TOKEN]
        self._client = None
        self._query_results = None
        self._text_match_index = 1
        self._text_matches_count = 0
        self._elapsed_time = None


    def __str__(self):
        """
        Serializes the query results to String
        """
        return json.dumps(self._query_results, indent="\t")


    # Public Methods ---------------------------------------------------------->

    def run(self):
        """
        Processes the user-defined GitHub query
        """

        status = False

        # Start timer

        start_time = datetime.datetime.now()

        # GitHub Client

        status = self._get_client()

        if status is False:
            return False

        # Run GitHub query

        status = self._run_query()

        if status is False:
            return False

        # Display GitHub query results section

        self._display_query_results_section()

        # Stop timer

        end_time = datetime.datetime.now()
        self._elapsed_time = end_time - start_time

        # Display summary section

        self._display_summary_section()

        return True


    # Private Methods --------------------------------------------------------->

    def _get_client(self, logger=DEFAULT_LOGGER):
        """
        Sets up the GitHub client and connects to the GitHub API
        """

        if self._client:
            return True

        if self._hostname == constants.GITHUB_ENTERPRISE_IBM_API_DOMAIN: # pylint: disable=comparison-with-callable
            # GitHub Enterprise
            github_api_url = "https://{0}{1}".format(self._hostname, constants.GITHUB_ENTERPRISE_API_PATH)
        else:
            # GitHub Public
            github_api_url = "https://{0}".format(self._hostname)

        logger.info("Connecting to GitHub API v3: %s...", github_api_url)

        try:
            self._client = github.Github(
                base_url=github_api_url,
                login_or_token=self._access_token)
        except github.GithubException as err:
            logger.error("Failed to connect to GitHub API v3: %s.", github_api_url)
            error_util.log_github_exception(logger, err)
            return False
        except github.BadAttributeException as err:
            logger.error("Failed to connect to GitHub API v3: %s.", github_api_url)
            error_util.log_bad_attribute_exception(logger, err)
            return False

        logger.info("Successfully connected to GitHub API v3: %s.", github_api_url)

        return True


    def _run_query(self, logger=DEFAULT_LOGGER):
        """
        Runs the user-defined GitHub query
        """

        logger.info("Running user-defined GitHub query...")

        try:
            self._query_results = self._client.search_code(self._query, highlight=True)
        except github.GithubException as err:
            logger.error("Failed to run user-defined GitHub query.")
            error_util.log_github_exception(logger, err)
            return False
        except github.BadAttributeException as err:
            logger.error("Failed to run user-defined GitHub query.")
            error_util.log_bad_attribute_exception(logger, err)
            return False

        logger.info("Successfully ran user-defined GitHub query.")

        return True


    def _display_query_results_section(self):
        """
        Displays the user-defined GitHub query results
        """

        index = 1
        section = [
            "",
            LINE_1,
            "Query Results",
            LINE_1
        ]

        print("\n".join(section))

        if self._query_results.totalCount == 0:
            print("\nNo matches found.")
        else:
            for content_file in self._query_results:
                self._process_content_file(index, content_file)
                index += 1


    def _process_content_file(self, index, content_file):
        """
        Processes the content file from the user-defined GitHub query results
        """

        # See: https://developer.github.com/v3/search/#search-code

        code_result = [
            "",
            LINE_2,
            "[{0}]: {1}".format(index, content_file.repository.full_name),
            LINE_2,
            "",
            "- Path: {0}".format(content_file.path),
            "- URL:  {0}".format(content_file.html_url),
        ]

        print("\n".join(code_result))

        self._text_match_index = 1

        for text_match in content_file.text_matches:
            self._process_text_match(text_match)


    def _process_text_match(self, text_match):
        """
        Processes the text match in the content file from the user-defined GitHub query results
        """

        fragment = text_match["fragment"]
        matches = text_match["matches"]

        # Note: When the "filename:<filename>" search qualifier is specified in the GitHub query,
        # the first fragment is the filename itself (i.e. interpreted as a text match).
        # This appears to be working as designed as demonstrated within the GitHub Public Web UI.
        # e.g. "filename:package.json" will result in a text match of "package.json".

        print("\n{0}\n".format(fragment))

        for match in matches:
            indices = match["indices"]
            print("- [{0}]: Text Range {1}".format(self._text_match_index, str(indices)))
            self._text_match_index += 1
            self._text_matches_count += 1


    def _display_summary_section(self):
        """
        Displays a statistical summary of processing the user-defined GitHub query
        """

        section = [
            "",
            LINE_1,
            "Summary",
            LINE_1,
            "",
            "- GitHub Query:  \"{0}\".".format(self._query),
            "- File Matches:  {0}".format(self._query_results.totalCount),
            "- Text Matches:  {0}".format(self._text_matches_count),
            "- Elapsed Time:  {0}".format(self._elapsed_time),
            ""
        ]

        print("\n".join(section))
