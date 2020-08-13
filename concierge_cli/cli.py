"""
CLI implementation for Concierge.
"""
import click

from gitlab.exceptions import GitlabError
from requests.exceptions import RequestException

from .constants import GITLAB_DEFAULT_URI, GITLAB_PERMISSIONS
from .manager import (
    GroupManager, MergeRequestManager, ProjectManager, TopicManager
)


@click.group()
@click.version_option()
def concierge_cli():
    """Concierge repository projects management CLI."""


@concierge_cli.group()
@click.option('--uri', envvar='CONCIERGE_GITLAB_URI',
              default=GITLAB_DEFAULT_URI, show_default=True,
              help='Location of the GitLab host. Alternatively, you may set'
                   ' the CONCIERGE_GITLAB_URI environment variable, or'
                   ' specify a host in a configuration file (see'
                   ' https://python-gitlab.readthedocs.io > CLI usage >'
                   ' Configuration > Files).')
@click.option('--token', envvar='CONCIERGE_GITLAB_TOKEN',
              help='Optional access token (access is anonymous if none is'
                   ' supplied). Alternatively, you may set the'
                   ' CONCIERGE_GITLAB_TOKEN environment variable.')
@click.option('--insecure/--secure',
              help='Disable SSL certificate check and related warnings.')
@click.pass_context
def gitlab(ctx, uri, token, insecure):
    """GitLab sub-commands."""
    ctx.obj = dict(uri=uri, token=token, insecure=insecure)


@gitlab.command()
@click.argument('group-project-filter', default='/')
@click.option('--empty/--no-empty', default=False,
              help='Select projects with an empty (or non-empty) topic list.')
@click.option('--set-topic', multiple=True,
              help='Use multiple times to set more than one topic.'
                   ' Use "" to clear topics.')
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
        insecure=ctx.obj.get('insecure'),
        group_filter=group_filter,
        project_filter=project_filter,
        empty=empty,
    )
    if set_topic:
        topic_manager.set(list(set_topic))
    else:
        topic_manager.show()


@gitlab.command()
@click.argument('group-project-filter', default='/')
@click.option('--label', multiple=True,
              help='Use multiple times to filter with more than one label.')
@click.option('--merge', default='no', show_default=True,
              type=click.Choice(['yes', 'no', 'automatic']),
              help='Merge all identified merge requests. With "yes", will '
                   'ask for confirmation interactively on each MR.')
@click.pass_context
def mrs(ctx, group_project_filter, label, merge):
    """
    List and manage merge requests of GitLab projects.

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

    mr_manager = MergeRequestManager(
        uri=ctx.obj.get('uri'),
        token=ctx.obj.get('token'),
        insecure=ctx.obj.get('insecure'),
        group_filter=group_filter,
        project_filter=project_filter,
        labels=list(label),
        merge_style=merge,
    )
    if merge in ['yes', 'automatic']:
        mr_manager.merge_all()
    else:
        mr_manager.show()


@gitlab.command()
@click.argument('group-project-filter', default='/')
@click.option('--topic', multiple=True,
              help='Use multiple times to filter with more than one topic.')
@click.pass_context
def projects(ctx, group_project_filter, topic):
    """
    List projects on GitLab, optionally by topic.

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

    project_manager = ProjectManager(
        uri=ctx.obj.get('uri'),
        token=ctx.obj.get('token'),
        insecure=ctx.obj.get('insecure'),
        group_filter=group_filter,
        project_filter=project_filter,
        topic_list=list(topic),
    )
    project_manager.show()


@gitlab.command()
@click.argument('username')
@click.option('--group-filter', default='',
              help='List only groups that match or contain a specific name.')
@click.option('--member/--no-member', default=True,
              help='Select groups where user is (not) a member of.')
@click.option('--set-permission',
              type=click.Choice(GITLAB_PERMISSIONS.keys()),
              help='Set user permission level on all matching groups.')
@click.pass_context
def groups(ctx, username, group_filter, member, set_permission):
    """
    Manage the access level for a user on GitLab groups.
    """
    group_manager = GroupManager(
        uri=ctx.obj.get('uri'),
        token=ctx.obj.get('token'),
        insecure=ctx.obj.get('insecure'),
        group_filter=group_filter,
        is_member=member,
        username=username,
    )
    if set_permission:
        group_manager.set(set_permission)
    else:
        group_manager.show()


def main():
    """Main entry point for the CLI"""
    try:
        concierge_cli()
    except GitlabError as err:
        raise SystemExit('%s 💣 GitLab error. Aborting.' % err.error_message)
    except RequestException as req:
        raise SystemExit('%s 💣 Communication error. Aborting.' % req)
    except Exception as other:
        raise SystemExit('%s 💣 Application error. Aborting.' % other)


if __name__ == '__main__':
    main()
