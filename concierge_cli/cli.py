"""
CLI implementation for Concierge.
"""
import click

from gitlab.exceptions import GitlabError
from requests.exceptions import RequestException

from .manager import DEFAULT_GITLAB_URI, TopicManager


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
