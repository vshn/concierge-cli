"""
Concierge repository projects management CLI.
"""
from gitlab import Gitlab
from gitlab.config import GitlabConfigMissingError

from .adapter import Project

DEFAULT_GITLAB_URI = 'https://gitlab.com'
MAX_GROUPS = 999_999


class TopicManager:
    """
    Manages topics on GitLab projects (visible in project settings).
    """

    def __init__(self, group_filter, project_filter, empty,
                 uri=None, token=None):
        """
        Connects to a GitLab instance using connection details from one of the
        local configuration files (see https://python-gitlab.readthedocs.io >
        Configuration > Files). Connects to GitLab.com by default if no config
        file is found. Specify an URI to override the config file lookup, the
        token is optional (anonymous access if none is supplied).
        """
        self.group_filter = group_filter
        self.project_filter = project_filter
        self.empty = empty

        if not uri:
            try:
                self.api = Gitlab.from_config()
            except GitlabConfigMissingError:
                uri = DEFAULT_GITLAB_URI

        if uri:
            self.api = Gitlab(uri, private_token=token)

    def projects(self):
        """
        List all projects and their topics, filtered by an optional
        search pattern.
        """
        for group in self.api.groups.list(search=self.group_filter,
                                          per_page=MAX_GROUPS):
            for project in group.projects.list(search=self.project_filter):
                project = Project(self.api, project)
                if (self.empty and not project.topic_count) or \
                        (not self.empty and project.topic_count):
                    yield project

    def show(self):
        """Display all found projects and their topics."""
        for project in self.projects():
            project.show_topics()

    def set(self, new_topics):
        """Set a list of topics on the projects found."""
        for project in self.projects():
            project.set_topics(new_topics)
