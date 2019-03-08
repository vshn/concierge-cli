"""
Tests for concierge-cli's command line interface (CLI)
"""
import os
import pytest

from gitlab.exceptions import GitlabError
from requests.exceptions import RequestException
from unittest.mock import patch

import concierge_cli.cli


def test_entrypoint():
    """
    Is entrypoint script installed? (setup.py)
    """
    exit_status = os.system('concierge-cli --help')
    assert exit_status == 0


def test_gitlab_command():
    """
    Is command available?
    """
    exit_status = os.system('concierge-cli gitlab --help')
    assert exit_status == 0


def test_gitlab_groups_command():
    """
    Is subcommand available?
    """
    exit_status = os.system('concierge-cli gitlab groups --help')
    assert exit_status == 0


def test_gitlab_projects_command():
    """
    Is subcommand available?
    """
    exit_status = os.system('concierge-cli gitlab projects --help')
    assert exit_status == 0


def test_gitlab_topics_command():
    """
    Is subcommand available?
    """
    exit_status = os.system('concierge-cli gitlab topics --help')
    assert exit_status == 0


@patch('concierge_cli.cli.concierge_cli', side_effect=GitlabError)
def test_handle_gitlab_errors(mock_cli):
    """
    Are GitLab errors handled correctly? (catch + print + exit)
    """
    with pytest.raises(SystemExit):
        concierge_cli.cli.main()


@patch('concierge_cli.cli.concierge_cli', side_effect=RequestException)
def test_handle_requests_errors(mock_cli):
    """
    Are exceptions from requests handled correctly? (catch + print + exit)
    """
    with pytest.raises(SystemExit):
        concierge_cli.cli.main()


@patch('concierge_cli.cli.concierge_cli', side_effect=Exception)
def test_handle_other_errors(mock_cli):
    """
    Are any other exceptions handled correctly? (catch + print + exit)
    """
    with pytest.raises(SystemExit):
        concierge_cli.cli.main()
