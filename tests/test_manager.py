"""
Tests for concierge-cli's manager classes
"""
from gitlab import Gitlab
from gitlab.config import GitlabConfigMissingError
from unittest.mock import patch
from urllib3.exceptions import InsecureRequestWarning

from concierge_cli.manager import (
    # GITLAB_DEFAULT_URI,
    GitlabAPI,
    GroupManager,
    ProjectManager,
    TopicManager,
)

TEST_URI = 'https://some.gitlab.host'
TEST_TOKEN = '1234567890abcdefghijklmnopqrstuvwxyz'


@patch.object(Gitlab, 'from_config')
@patch('gitlab.Gitlab')
def test_gitlabapi_no_uri_with_config(mock_gitlab, mock_from_config):
    """
    Is python-gitlab config read from config file when no URI is provided?
    """
    GitlabAPI(uri=None, token=None, insecure=False)

    assert mock_from_config.called
    assert not mock_gitlab.called


@patch.object(Gitlab, 'from_config', side_effect=GitlabConfigMissingError)
@patch('gitlab.Gitlab')
def test_gitlabapi_no_uri_without_config(mock_gitlab, mock_from_config):
    """
    Do we fall back to a default URI when no config file is around?
    """
    GitlabAPI(uri=None, token=TEST_TOKEN, insecure=False)

    assert mock_from_config.called
#     assert mock_gitlab.assert_called_with(uri=GITLAB_DEFAULT_URI,
#                                           private_token=TEST_TOKEN,
#                                           per_page=100) is None


@patch('gitlab.Gitlab')
def test_gitlabapi_uri(mock_gitlab):
    """
    Is an API object constructed with the TEST_URI we specify?
    """
    GitlabAPI(uri=TEST_URI, token=TEST_TOKEN, insecure=False)

#     assert mock_gitlab.assert_called_with(uri=TEST_URI,
#                                           private_token=TEST_TOKEN,
#                                           per_page=100) is None


@patch('warnings.filterwarnings')
@patch('gitlab.Gitlab')
def test_gitlabapi_insecure(mock_gitlab, mock_filterwarnings):
    """
    Are SSL certificate warnings disabled when --insecure option is used?
    """
    api = GitlabAPI(uri=None, token=None, insecure=True)

    assert mock_filterwarnings.assert_called_with(
        'ignore', category=InsecureRequestWarning) is None
    assert api.api.ssl_verify is False


@patch('concierge_cli.adapter.Project')
def test_topicmanager_show(mock_project):
    """
    Is the show() method iterating over the list of projects?
    """
    with patch.object(TopicManager, 'projects', return_value=[
        mock_project,
        mock_project,
        mock_project,
    ]) as mock_manager_projects:

        topic_manager = TopicManager(
            group_filter='',
            project_filter='',
            empty=True,
            uri=TEST_URI,
            token=TEST_TOKEN,
            insecure=False,
        )
        assert isinstance(topic_manager, GitlabAPI)

        topic_manager.show()
        assert mock_manager_projects.called
        assert mock_project.show_topics.call_count == 3


@patch('concierge_cli.adapter.Project')
def test_topicmanager_set(mock_project):
    """
    Is the set() method iterating over the list of projects?
    """
    with patch.object(TopicManager, 'projects', return_value=[
        mock_project,
        mock_project,
        mock_project,
    ]) as mock_manager_projects:

        topic_manager = TopicManager(
            group_filter='',
            project_filter='',
            empty=True,
            uri=TEST_URI,
            token=TEST_TOKEN,
            insecure=False,
        )
        assert isinstance(topic_manager, GitlabAPI)

        topic_manager.set([None])
        assert mock_manager_projects.called
        assert mock_project.set_topics.call_count == 3


@patch('concierge_cli.adapter.Project')
def test_projectmanager_show(mock_project):
    """
    Is the show() method iterating over the list of projects?
    """
    with patch.object(ProjectManager, 'projects', return_value=[
        mock_project,
        mock_project,
        mock_project,
    ]) as mock_manager_projects:

        project_manager = ProjectManager(
            group_filter='',
            project_filter='',
            topic_list=[],
            uri=TEST_URI,
            token=TEST_TOKEN,
            insecure=False,
        )
        assert isinstance(project_manager, GitlabAPI)

        project_manager.show()
        assert mock_manager_projects.called


@patch('concierge_cli.adapter.GroupMembership')
def test_groupmanager_show(mock_membership):
    """
    Is the show() method iterating over the list of groups?
    """
    with patch.object(GroupManager, 'groups', return_value=[
        mock_membership,
        mock_membership,
        mock_membership,
    ]):  # as mock_manager_groups:

        # TODO: mock GroupManager.api.users.list()
        pass

        # group_manager = GroupManager(
        #     group_filter='',
        #     username='test.user',
        #     is_member=True,
        #     uri=TEST_URI,
        #     token=TEST_TOKEN,
        #     insecure=False,
        # )
        # assert isinstance(group_manager, GitlabAPI)
        #
        # group_manager.show()
        # assert mock_manager_groups.called


@patch('concierge_cli.manager.GitlabAPI')
@patch('concierge_cli.adapter.GroupMembership')
def test_groupmanager_set(mock_membership, mock_gitlabapi):
    """
    Is the set() method iterating over the list of groups?
    """
    with patch.object(GroupManager, 'groups', return_value=[
        mock_membership,
        mock_membership,
        mock_membership,
    ]):  # as mock_manager_groups:

        # TODO: mock GroupManager.api.users.list()
        pass

        # group_manager = GroupManager(
        #     group_filter='',
        #     username='test.user',
        #     is_member=True,
        #     uri=TEST_URI,
        #     token=TEST_TOKEN,
        #     insecure=False,
        # )
        # assert isinstance(group_manager, GitlabAPI)
        #
        # group_manager.set('none')
        # assert mock_manager_groups.called
        # assert mock_membership.set_membership.call_count == 3
