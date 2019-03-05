"""
Constants for Concierge CLI.
"""
import gitlab

GITLAB_DEFAULT_URI = 'https://gitlab.com'
GITLAB_PERMISSIONS = {
    'owner': gitlab.OWNER_ACCESS,
    'maintainer': gitlab.MAINTAINER_ACCESS,
    'developer': gitlab.DEVELOPER_ACCESS,
    'reporter': gitlab.REPORTER_ACCESS,
    'guest': gitlab.GUEST_ACCESS,
    'none': 0,
}
GITLAB_PERMISSION_NAMES = {
    gitlab.OWNER_ACCESS: 'owner',
    gitlab.MAINTAINER_ACCESS: 'maintainer',
    gitlab.DEVELOPER_ACCESS: 'developer',
    gitlab.REPORTER_ACCESS: 'reporter',
    gitlab.GUEST_ACCESS: 'guest',
    0: 'none',
}
