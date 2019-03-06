"""
Concierge repository projects management CLI.
"""
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

        # get a full-featured project (a group project has limited features)
        project = self.api.projects.get(self.group_project.id, lazy=True)
        project.tag_list = new_topics
        project.save()

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
        self.member = self.group.members.get(self.user.id)
        self.is_member = self.member is not None
        self.access_level = 'n/a' if not self.member else \
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
        return f"Group {self.group.full_path}: " \
               f"{self.user.username} has " \
               f"access level '{self.access_level}'"
