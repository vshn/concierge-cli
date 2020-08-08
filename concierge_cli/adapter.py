"""
Concierge repository projects management CLI.
"""
from gitlab import GitlabGetError

from .constants import GITLAB_PERMISSION_NAMES, GITLAB_PERMISSIONS


class Project:
    """
    Adapter wrapping a project from a repository service API
    """

    def __init__(self, api, project):
        """A GitLab API project, currently."""
        self.group_project = project
        self.name = project.attributes['path_with_namespace']
        self.topic_list = project.attributes['tag_list']
        self.topic_count = len(self.topic_list)
        self.api = api

        # a full-featured project (a group project has limited features)
        self.project = self.api.projects.get(self.group_project.id, lazy=True)

    def show_topics(self):
        """Display the project name and project topics"""
        if self.topic_count:
            print(f"{self.topic_count} topics in {self.name}: "
                  f"{str(self.topic_list)[1:-1]}")
        else:
            print(f"{self.name}")

    def set_topics(self, new_topics):
        """Update the project topics"""
        if self.topic_count:
            print(f"Replacing topics on {self.name}: "
                  f"{self.topic_list} -> {new_topics}")
        else:
            print(f"Setting new topics on {self.name}: {new_topics}")

        self.project.tag_list = new_topics
        self.project.save()

        self.topic_list = new_topics
        self.topic_count = len(new_topics)

    def get_mergerequests(self, state='opened', labels=(), wip='no'):
        """Return a list of the project's merge requests"""
        return self.project.mergerequests.list(state=state,
                                               labels=labels,
                                               wip=wip)

    def __str__(self):
        """Project name and its namespace"""
        return self.name


class GroupMembership:
    """
    Adapter wrapping a group from a repository service API
    """

    def __init__(self, group, user):
        """A GitLab API group, currently."""
        self.group = group
        self.user = user
        try:
            self.member = self.group.members.get(self.user.id)
        except GitlabGetError as err:
            if err.response_code != 404:
                raise
            self.member = None
            self.is_member = False
            self.access_level = None
        else:
            self.is_member = True
            self.access_level = \
                GITLAB_PERMISSION_NAMES[self.member.access_level]

    def set_membership(self, permission_name):
        """Update the user's permissions on the group"""
        new_access_level = GITLAB_PERMISSIONS[permission_name]

        if self.is_member:
            if permission_name == self.access_level:
                return

            print(f"Group {self.group.full_path}: "
                  f"Updating access level: '{self.access_level}' "
                  f"-> '{permission_name}'")

            if permission_name == GITLAB_PERMISSION_NAMES[None]:
                self.member.delete()
            else:
                self.member.access_level = new_access_level
                self.member.save()

        else:
            print(f"Group {self.group.full_path}: "
                  f"Adding {self.user.username} "
                  f"with access level '{permission_name}'")

            self.group.members.create({
                'user_id': self.user.id,
                'access_level': new_access_level,
            })

    def __str__(self):
        """Textual information about the group membership"""
        access_level = \
            f"has access level '{self.access_level}'" \
            if self.is_member else 'is not a member.'

        return f"Group {self.group.full_path}: " \
               f"{self.user.username} {access_level}"
