"""
Concierge repository projects management CLI.
"""


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
