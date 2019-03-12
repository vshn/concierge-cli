"""
Tests for concierge-cli's adapter classes
"""
from gitlab.v4.objects import (
    # Group as Gitlab_Group,
    # GroupMember as Gitlab_GroupMember,
    Project as Gitlab_Project,
)
from unittest.mock import Mock, patch

from concierge_cli.manager import GitlabAPI
from concierge_cli.adapter import (
    # GITLAB_PERMISSIONS,
    # GroupMembership,
    Project,
)


def mock_group_project():
    """Just a mock"""
    group_project = Mock('gitlab.v4.objects.Project')
    group_project.id = 42
    group_project.attributes = {
        'tag_list': [],
        'path_with_namespace': 'foo/bar',
    }
    return group_project


def mock_gitlab_api_projects():
    """A pseudo mock"""
    def save():
        pass

    def get(*args, **kwargs):
        project = Mock('gitlab.v4.objects.Project')
        project.save = save
        return project

    with patch('gitlab.Gitlab'):
        gitlab = GitlabAPI(uri=None, token=None, insecure=False)
        gitlab.api.projects = Mock('gitlab.v4.objects.ProjectManager')
        gitlab.api.projects.get = get
        return gitlab.api


@patch('concierge_cli.adapter.Project')
def test_project_set_topics(mock_project):
    """
    Are project topics updated on the API endpoint and the object?
    # TODO: verify that project.save() is called
    """
    # start with no topics
    project = Project(api=mock_gitlab_api_projects(),
                      project=mock_group_project())
    assert project.topic_list == []
    assert project.topic_count == 0

    new_topics = ['foo', 'bar', 'test:baz']

    with patch.object(Gitlab_Project, 'save'):  # as mock_save:
        project.set_topics(new_topics)
        # assert mock_save.called
        assert project.topic_list == new_topics
        assert project.topic_count == len(new_topics)


def test_groupmembership_join():
    """
    Is a non-member promoted to a member on the API endpoint and the object?
    # TODO: patch GroupMembership.group.members.get()
    """
    # start with a non-member
#     with patch.object(Gitlab_Group, 'members') as mock_members:
#         group_user = GroupMembership(group=None, user=None)
#         group_user.member = None
#         group_user.is_member = False
#         group_user.access_level = None
#
#     with patch.object(Gitlab_Group, 'members') as mock_members:
#         group_user.set_membership('maintainer')
#
#         assert mock_members.assert_called('create') is None
#         assert group_user.is_member
#         assert group_user.access_level == 'maintainer'
#         assert group_user.member.access_level == \
#             GITLAB_PERMISSIONS['maintainer']


def test_groupmembership_update():
    """
    Is a member access level updated on the API endpoint and the object?
    # TODO: patch GroupMembership.group.members.get()
    """
    # start with a member
#     with patch.object(Gitlab_Group, 'members') as mock_members:
#         group_user = GroupMembership(group=None, user=None)
#         group_user.is_member = True
#         group_user.access_level = 'maintainer'
#         group_user.member = Mock('gitlab.v4.objects.GroupMember')
#         group_user.member.access_level = GITLAB_PERMISSIONS['maintainer']
#
#     with patch.object(Gitlab_GroupMember, 'save') as mock_member_save:
#         group_user.set_membership('owner')
#
#         assert mock_member_save.called
#         assert group_user.is_member
#         assert group_user.access_level == 'owner'
#         assert group_user.member.access_level == GITLAB_PERMISSIONS['owner']


def test_groupmembership_withdraw():
    """
    Is a membership withdrawn on the API endpoint and the object?
    # TODO: patch GroupMembership.group.members.get()
    """
    # start with a member
#     with patch.object(Gitlab_Group, 'members') as mock_members:
#         group_user = GroupMembership(group=None, user=None)
#         group_user.is_member = True
#         group_user.access_level = 'maintainer'
#         group_user.member = Mock('gitlab.v4.objects.GroupMember')
#         group_user.member.access_level = GITLAB_PERMISSIONS['maintainer']
#
#     with patch.object(Gitlab_GroupMember, 'delete') as mock_member_delete:
#         group_user.set_membership('none')
#
#         assert mock_member_delete.called
#         assert not group_user.member
#         assert not group_user.is_member
#         assert group_user.access_level == 'none'
