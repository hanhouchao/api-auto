from time import sleep
from common.base_request import Common
from common import settings


class Project(Common):
    def get_project_list_or_detail_url(self, project_name=''):
        if project_name:
            return 'apis/auth.alauda.io/v1/projects/{}'.format(project_name)
        else:
            return 'apis/auth.alauda.io/v1/projects'

    def get_projectquota_url(self, name):
        return "kubernetes/{cluster}/apis/auth.alauda.io/v1/projectquotas/{name}".format(cluster=self.region_name, name=name)

    def create_project(self, file, data):
        path = "apis/auth.alauda.io/v1/projects"
        if file.endswith('jinja2'):
            data = self.generate_jinja_data(file, data)
            return self.send(method='post', path=path, json=data)
        else:
            data = self.generate_data(file, data)
            return self.send(method="POST", data=data, path=path)

    def delete_project(self, project_name):
        path = "apis/auth.alauda.io/v1/projects/{}".format(project_name)
        return self.send(method="DELETE", path=path)

    def get_project_list_or_detail(self, project_name=""):
        path = self.get_project_list_or_detail_url(project_name)
        return self.send(method="GET", path=path)

    def update_project(self, project_name, file, data={}):
        path = "apis/auth.alauda.io/v1/projects/{name}".format(name=project_name)
        if file.endswith('jinja2'):
            data = self.generate_jinja_data(file, data)
            return self.send(method='PATCH', path=path, json=data, headers={"Content-Type": "application/merge-patch+json"})
        else:
            data = self.generate_data(file, data)
            return self.send(method="PATCH", data=data, path=path)

    def get_project_namespace_list(self):
        path = "auth/v1/projects/{name}/clusters/{cluster}/namespaces".format(
            name=self.project_name, cluster=self.region_name)
        return self.send(method="GET", path=path)

    def get_project_list(self, params=None):
        if params is None:
            params = {"limit": 1000}
        path = "auth/v1/projects"
        return self.send(method="GET", path=path, params=params)

    def get_project_quota(self, name):
        path = self.get_projectquota_url(name=name)
        return self.send(method="GET", path=path)

    def check_project_exists(self, project_name, expect_status):
        path = self.get_project_list_or_detail_url(project_name)
        return self.check_exists(path, expect_status, params={})

    def check_project_ready(self, project_name, expected_value="Active", cycle=10):
        count = 0
        while count < cycle:
            count += 1
            ret = self.get_project_list_or_detail(project_name=project_name)
            if expected_value in ret.text:
                return True
            sleep(3)
        return False

    def get_available_resource(self):
        path = 'auth/v1/projects/available-resources'
        return self.send('GET', path=path)

    def filter_project(self, name, filterby="name", limit=20):
        path = 'auth/v1/projects?limit={}&filterBy={},{}'.format(limit, filterby, name)
        return self.send('GET', path=path)


data_list = [
    {
        "project_name": "{}-ares-test1".format(settings.RESOURCE_PREFIX),
        "regions": [settings.REGION_NAME]
    },
    {
        "project_name": "{}-ares-test2".format(settings.RESOURCE_PREFIX),
        "display_name": "必填项加上显示名称",
        "regions": [settings.REGION_NAME]
    },
    {
        "project_name": "{}-ares-test3".format(settings.RESOURCE_PREFIX),
        "description": "必填项加上多个集群和描述",
        "regions": [settings.REGION_NAME, settings.GLOBAL_REGION_NAME]
    }
]

casename_list = ["必填项", "必填项加上显示名称", "必填项加上多个集群和描述"]
