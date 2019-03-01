"""
Concierge repository projects management CLI.
"""
import click

from gitlab import Gitlab
from gitlab.config import GitlabConfigMissingError
from gitlab.exceptions import GitlabError
from requests.exceptions import RequestException

DEFAULT_GITLAB_URI = 'https://gitlab.com'
MAX_GROUPS = 999_999


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


@click.group()
def concierge_cli():
    """Concierge repository projects management CLI."""


@concierge_cli.group()
@click.option('--uri', help='Location of GitLab host, unless specified '
                            'in a configuration file (see '
                            'https://python-gitlab.readthedocs.io '
                            '> Configuration > Files), default: %s' %
                            DEFAULT_GITLAB_URI)
@click.option('--token', help='Optional access token. Anonymous access '
                              'if none is supplied.')
@click.pass_context
def gitlab(ctx, uri, token):
    """GitLab sub-commands."""
    ctx.obj = dict(uri=uri, token=token)


@gitlab.command()
@click.argument('group-project-filter', default='/')
@click.option('--empty/--no-empty', default=False,
              help='Select projects with an empty (or non-empty) topic list.')
@click.option('--set-topic', multiple=True,
              help='Use multiple times to set more than one topic. '
                   'Use "" to clear topics.')
@click.pass_context
def topics(ctx, group_project_filter, empty, set_topic):
    """
    List and manage topics on GitLab projects.

    Filter syntax:

    - foo/bar ... projects that have "bar" in their name,
    in groups that have "foo" in their name

    - foo/ ... filter for groups only, match any project

    - /bar ... filter for projects only, match any group
    """
    try:
        group_filter, project_filter = group_project_filter.split('/')
    except ValueError:
        group_filter, project_filter = '', group_project_filter

    topic_manager = TopicManager(
        uri=ctx.obj.get('uri'),
        token=ctx.obj.get('token'),
        group_filter=group_filter,
        project_filter=project_filter,
        empty=empty,
    )
    if set_topic:
        topic_manager.set(list(set_topic))
    else:
        topic_manager.show()


def main():
    """Main entry point for the CLI"""
    try:
        concierge_cli()
    except GitlabError as err:
        raise SystemExit('%s (GitLab)' % err.error_message)
    except RequestException as req:
        raise SystemExit(req)


if __name__ == '__main__':
    main()
