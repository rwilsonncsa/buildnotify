import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

import unittest
from buildnotifylib.core.projects import Project
from buildnotifylib.project_status_notification import ProjectStatus


class ProjectStatusNotificationTest(unittest.TestCase):
    def test_should_identify_failing_builds(self):
        old_projects = [Project({'server_url': 'url', 'name': 'proj1', 'lastBuildStatus': 'Success', 'activity': 'Sleeping', 'url': 'someurl', 'lastBuildTime': '2009-05-29T13:54:07'}),
                        Project({'server_url': 'url', 'name': 'proj2', 'lastBuildStatus': 'Success', 'activity': 'Sleeping', 'url': 'someurl', 'lastBuildTime': '2009-05-29T13:54:37'})]
        new_projects = [Project({'server_url': 'url', 'name': 'proj1', 'lastBuildStatus': 'Success', 'activity': 'Sleeping', 'url': 'someurl', 'lastBuildTime': '2009-05-29T13:54:07'}),
                        Project({'server_url': 'url', 'name': 'proj2', 'lastBuildStatus': 'Failure', 'activity': 'Sleeping', 'url': 'someurl', 'lastBuildTime': '2009-05-29T13:54:37'})]
        failing_builds = self.build(old_projects, new_projects).failing_builds()
        self.assertEquals(1, len(failing_builds))
        self.assertEquals("proj2", failing_builds[0])

    def test_should_identify_fixed_builds(self):
        old_projects = [Project({'server_url': 'url', 'name': 'proj1', 'lastBuildStatus': 'Failure', 'activity': 'Sleeping', 'url': 'someurl', 'lastBuildTime': '2009-05-29T13:54:07'}),
                        Project({'server_url': 'url', 'name': 'proj2', 'lastBuildStatus': 'Failure', 'activity': 'Sleeping', 'url': 'someurl', 'lastBuildTime': '2009-05-29T13:54:37'})]
        new_projects = [Project({'server_url': 'url', 'name': 'proj1', 'lastBuildStatus': 'Success', 'activity': 'Sleeping', 'url': 'someurl', 'lastBuildTime': '2009-05-29T13:54:07'}),
                        Project({'server_url': 'url', 'name': 'proj2', 'lastBuildStatus': 'Failure', 'activity': 'Sleeping', 'url': 'someurl', 'lastBuildTime': '2009-05-29T13:54:37'})]
        successful_builds = self.build(old_projects, new_projects).successful_builds()
        self.assertEquals(1, len(successful_builds))
        self.assertEquals("proj1", successful_builds[0])

    def test_should_identify_still_failing_builds(self):
        old_projects = [Project({'server_url': 'url', 'name': 'proj1', 'lastBuildStatus': 'Success', 'activity': 'Sleeping', 'url': 'someurl', 'lastBuildLabel': '1', 'lastBuildTime': '2009-05-29T13:54:07'}),
                        Project({'server_url': 'url', 'name': 'stillfailingbuild', 'lastBuildStatus': 'Failure', 'activity': 'Sleeping', 'url': 'someurl', 'lastBuildLabel': '10', 'lastBuildTime': '2009-05-29T13:54:37'})]
        new_projects = [Project({'server_url': 'url', 'name': 'proj1', 'lastBuildStatus': 'Success', 'activity': 'Sleeping', 'url': 'someurl', 'lastBuildLabel': '1', 'lastBuildTime': '2009-05-29T13:54:07'}),
                        Project({'server_url': 'url', 'name': 'stillfailingbuild', 'lastBuildStatus': 'Failure', 'activity': 'Sleeping', 'url': 'someurl', 'lastBuildLabel': '11', 'lastBuildTime': '2009-05-29T13:54:47'})]
        still_failing_builds = self.build(old_projects, new_projects).still_failing_builds()
        self.assertEquals(1, len(still_failing_builds))
        self.assertEquals("stillfailingbuild", still_failing_builds[0])

    def test_should_identify_still_successful_builds(self):
        old_projects = [Project({'server_url': 'url', 'name': 'proj1', 'lastBuildStatus': 'Success', 'activity': 'Sleeping', 'url': 'someurl', 'lastBuildLabel': '1', 'lastBuildTime': '2009-05-29T13:54:07'}),
                        Project({'server_url': 'url', 'name': 'Successbuild', 'lastBuildStatus': 'Success', 'activity': 'Sleeping', 'url': 'someurl', 'lastBuildLabel': '10', 'lastBuildTime': '2009-05-29T13:54:37'})]
        new_projects = [Project({'server_url': 'url', 'name': 'proj1', 'lastBuildStatus': 'Success', 'activity': 'Sleeping', 'url': 'someurl', 'lastBuildLabel': '1', 'lastBuildTime': '2009-05-29T13:54:07'}),
                        Project({'server_url': 'url', 'name': 'Successbuild', 'lastBuildStatus': 'Success', 'activity': 'Sleeping', 'url': 'someurl', 'lastBuildLabel': '11', 'lastBuildTime': '2009-05-29T13:54:47'})]
        still_successful_builds = self.build(old_projects, new_projects).still_successful_builds()
        self.assertEquals(1, len(still_successful_builds))
        self.assertEquals("Successbuild", still_successful_builds[0])

    def test_should_build_tuples_by_server_url_and_name(self):
        project_s1 = Project({'server_url': 's1', 'name': 'proj1', 'lastBuildStatus': 'Success', 'activity': 'Sleeping', 'url': 'someurl', 'lastBuildTime': '2009-05-29T13:54:07'})
        project_s2 = Project({'server_url': 's2', 'name': 'proj1', 'lastBuildStatus': 'Success', 'activity': 'Sleeping', 'url': 'someurl', 'lastBuildTime': '2009-05-29T13:54:07'})
        old_projects = [project_s1, project_s2]
        new_projects = [project_s2, project_s1]
        tuple = self.build(old_projects, new_projects).tuple_for(project_s2)
        self.assertEquals('s2', tuple.current_project.server_url)
        self.assertEquals('s2', tuple.old_project.server_url)

    def test_should_identify_new_builds(self):
        old_projects = [Project({'server_url': 'url', 'name': 'proj1', 'lastBuildStatus': 'Success', 'activity': 'Sleeping', 'url': 'someurl', 'lastBuildTime': '2009-05-29T13:54:07'})]
        new_projects = [Project({'server_url': 'url', 'name': 'proj1', 'lastBuildStatus': 'Success', 'activity': 'Sleeping', 'url': 'someurl', 'lastBuildTime': '2009-05-29T13:54:07'}),
                        Project({'server_url': 'url', 'name': 'Successbuild', 'lastBuildStatus': 'Success', 'activity': 'Sleeping', 'url': 'someurl', 'lastBuildTime': '2009-05-29T13:54:47'})]
        still_successful_builds = self.build(old_projects, new_projects).still_successful_builds()
        self.assertEquals(1, len(still_successful_builds))
        self.assertEquals("Successbuild", still_successful_builds[0])

    def build(self, old_projects, new_projects):
        return ProjectStatus(old_projects, new_projects)


if __name__ == '__main__':
    unittest.main()

