"""
Tests for concierge-cli's command line interface (CLI)
"""
import os
import pytest

from click.testing import CliRunner
from gitlab.exceptions import GitlabError
from requests.exceptions import RequestException
from unittest.mock import patch

import concierge_cli.cli


def test_runas_module():
    """
    Can this package be run as a Python module?
    """
    exit_status = os.system('python -m concierge_cli')
    assert exit_status == 0


def launch_cli(*args):
    """
    Helper for testing the click CLI.
    See https://click.palletsprojects.com/en/7.x/testing/
    """
    runner = CliRunner()
    result = runner.invoke(concierge_cli.cli.concierge_cli, args)
    return result


def test_entrypoint():
    """
    Is entrypoint script installed? (setup.py)
    """
    exit_status = os.system('concierge-cli --version')
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


@patch('concierge_cli.cli.GroupManager')
def test_gitlab_groups_show(mock_manager):
    """
    Does groups command run the manager's show method? (by default)
    """
    launch_cli('gitlab', 'groups', 'foo-user')
    assert mock_manager().show.called


@patch('concierge_cli.cli.GroupManager')
def test_gitlab_groups_set(mock_manager):
    """
    Does groups set option run the manager method?
    """
    launch_cli('gitlab', 'groups', 'foo-user', '--set-permission', 'none')
    assert mock_manager().set.called


def test_gitlab_projects_command():
    """
    Is subcommand available?
    """
    exit_status = os.system('concierge-cli gitlab projects --help')
    assert exit_status == 0


@patch('concierge_cli.cli.ProjectManager')
def test_gitlab_projects_show(mock_manager):
    """
    Does projects command run the manager's show method?
    """
    launch_cli('gitlab', 'projects', 'some/project', '--topic', 'foo')
    assert mock_manager().show.called


def test_gitlab_topics_command():
    """
    Is subcommand available?
    """
    exit_status = os.system('concierge-cli gitlab topics --help')
    assert exit_status == 0


@patch('concierge_cli.cli.TopicManager')
def test_gitlab_topics_show(mock_manager):
    """
    Does topics command run the manager's show method? (by default)
    """
    launch_cli('gitlab', 'topics', 'some/project')
    assert mock_manager().show.called


@patch('concierge_cli.cli.TopicManager')
def test_gitlab_topics_set(mock_manager):
    """
    Does topics set option run the manager method?
    """
    launch_cli('gitlab', 'topics', 'some/project', '--set-topic', 'foo')
    assert mock_manager().set.called


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
