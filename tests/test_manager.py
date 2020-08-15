"""
Tests for concierge-cli's manager classes
"""
from gitlab import Gitlab
from gitlab.config import GitlabConfigMissingError
from unittest.mock import call, patch, Mock
from urllib3.exceptions import InsecureRequestWarning

from concierge_cli.manager import (
    # GITLAB_DEFAULT_URI,
    GitlabAPI,
    GroupManager,
    MergeRequestManager,
    ProjectManager,
    TopicManager,
)

TEST_URI = 'https://some.gitlab.host'
TEST_TOKEN = '1234567890abcdefghijklmnopqrstuvwxyz'


def mock_pipelines(*statuses):
    """Fake implementation for ``merge_request.pipelines()``."""
    return Mock(return_value=[dict(status=status) for status in statuses])


def mock_ref(iid):
    """Fake ``references`` field of merge request API answer."""
    return dict(full=f"mockedgroup/mockedproject!{iid}", short=f"!{iid}")


class MergeRequestMock:
    """Fake merge request API object."""
    labels = []
    merge_status = 'can_be_merged'
    pipelines = mock_pipelines('success', 'failed')
    references = mock_ref(42)
    title = 'My mocked merge request'

    def __init__(self, **kwargs):
        self.__dict__.update(**kwargs)

    def merge(self):
        pass


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


@patch('builtins.print')
@patch.object(MergeRequestManager, 'merge_requests', return_value=[
    MergeRequestMock(title='Foo', references=mock_ref(3)),
    MergeRequestMock(title='Bar', merge_status='cannot_be_merged'),
    MergeRequestMock(title='Baz', references=mock_ref(17), pipelines=mock_pipelines('failed')),  # noqa
])
def test_mergerequestmanager_show(mock_manager_merge_requests, mock_print):
    """
    Does show() method call merge_requests() and prints all MRs?
    """
    mr_manager = MergeRequestManager(
        group_filter='',
        project_filter='',
        labels=[],
        merge_style='no',
    )
    assert isinstance(mr_manager, GitlabAPI)

    mr_manager.show()
    assert mock_manager_merge_requests.called
    assert mock_print.mock_calls == [
        call('Open merge requests: (mergeable, pipeline status)'),
        call('✓✓ mockedgroup/mockedproject!3: Foo'),
        call('✗✓ mockedgroup/mockedproject!42: Bar'),
        call('✓✗ mockedgroup/mockedproject!17: Baz'),
    ]


@patch('builtins.print')
@patch('builtins.input', return_value='y')
@patch.object(MergeRequestMock, 'merge')
@patch.object(MergeRequestManager, 'merge_requests', return_value=[
    MergeRequestMock(title='Foo', references=mock_ref(3)),
    MergeRequestMock(title='Bar', merge_status='cannot_be_merged'),
    MergeRequestMock(title='Baz', references=mock_ref(17), pipelines=mock_pipelines('failed')),  # noqa
])
def test_mergerequestmanager_merge_yes(mock_manager_merge_requests,
                                       mock_merge, mock_input, mock_print):
    """
    Does merge_all() method call merge_requests() and input() and print()?
    """
    mr_manager = MergeRequestManager(
        group_filter='',
        project_filter='',
        labels=[],
        merge_style='yes',
    )
    assert isinstance(mr_manager, GitlabAPI)

    mr_manager.merge_all()
    assert mock_manager_merge_requests.called
    assert mock_input.mock_calls == [
        call('Proceed with merging ✓✓ mockedgroup/mockedproject!3: Foo ? (y/n) [n] '),  # noqa
    ]
    assert mock_merge.called
    assert mock_print.mock_calls == [
        call('Merging merge requests:'),
        call("Ignoring mockedgroup/mockedproject!42: Bar ✗ Can't be merged"),
        call('Skipping mockedgroup/mockedproject!17: Baz ✗ Pipeline not succeeded'),  # noqa
        call('1 MRs merged.'),
    ]


@patch('builtins.print')
@patch.object(MergeRequestMock, 'merge')
@patch.object(MergeRequestManager, 'merge_requests', return_value=[
    MergeRequestMock(title='Foo', references=mock_ref(3)),
    MergeRequestMock(title='Bar', merge_status='cannot_be_merged'),
    MergeRequestMock(title='Baz', references=mock_ref(17), pipelines=mock_pipelines('failed')),  # noqa
])
def test_mergerequestmanager_merge_automatic(mock_manager_merge_requests,
                                             mock_merge, mock_print):
    """
    Does merge_all() method call merge_requests() and input() and print()?
    """
    mr_manager = MergeRequestManager(
        group_filter='',
        project_filter='',
        labels=[],
        merge_style='automatic',
    )
    assert isinstance(mr_manager, GitlabAPI)

    mr_manager.merge_all()
    assert mock_manager_merge_requests.called
    assert mock_merge.called
    assert mock_print.mock_calls == [
        call('Merging merge requests:'),
        call('Merging mockedgroup/mockedproject!3: Foo'),
        call("Ignoring mockedgroup/mockedproject!42: Bar ✗ Can't be merged"),
        call('Skipping mockedgroup/mockedproject!17: Baz ✗ Pipeline not succeeded'),  # noqa
        call('1 MRs merged.'),
    ]


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
