from common.base_request import Common
from common import settings
import yaml


class Configmap(Common):
    def __init__(self):
        super(Configmap, self).__init__()
        self.template = self.generate_jinja_template('./test_data/configmap/create_configmap.jinja2')

    def get_common_configmap_url(self, configmap_name=None, ns_name=settings.K8S_NAMESPACE):
        return configmap_name and \
               "kubernetes/{}/api/v1/namespaces/{}/configmaps/{}".format(self.region_name, ns_name, configmap_name) \
               or "kubernetes/{}/api/v1/namespaces/{}/configmaps".format(self.region_name, ns_name)

    def get_common_configmap_list_url(self, ns_name=settings.K8S_NAMESPACE):
        return "kubernetes/{}/api/v1/namespaces/{}/configmaps".format(self.region_name, ns_name)

    def get_configmap_workload_url(self, ns_name=settings.K8S_NAMESPACE, configmap_name=None):
        return "acp/v1/kubernetes/{}/topology/{}/configmap/{}".format(self.region_name, ns_name, configmap_name)

    def get_common_configmap_search_url_v1(self, ns_name=settings.K8S_NAMESPACE, limit=1, configmap_name=None):
        return limit and "acp/v1/resources/search/kubernetes/{}/api/v1/namespaces/{}/configmaps?" \
                         "limit={}&keyword={}&field=metadata.name".format(self.region_name, ns_name, limit,
                                                                          configmap_name)

    def create_configmap(self, data):
        path = self.get_common_configmap_url()
        data.update({"default_label": settings.DEFAULT_LABEL})
        tmp_data = self.template.render(data)
        data = yaml.safe_load(tmp_data)
        return self.send(method='post', path=path, json=data, params={})

    def get_configmap_list(self, params={}):
        path = self.get_common_configmap_list_url()
        return self.send(method='get', path=path, params=params)

    def get_configmap_detail(self, configmap_name):
        path = self.get_common_configmap_url(configmap_name=configmap_name)
        return self.send(method='get', path=path, params={})

    def delete_configmap(self, configmap_name):
        path = self.get_common_configmap_url(configmap_name=configmap_name)
        return self.send(method='delete', path=path, params={})

    def update_configmap(self, configmap_name, data):
        path = self.get_common_configmap_url(configmap_name=configmap_name)
        data.update({"default_label": settings.DEFAULT_LABEL})
        tmp_data = self.template.render(data)
        data = yaml.safe_load(tmp_data)
        return self.send(method='put', path=path, json=data, params={})

    def get_configmap_workload(self, configmap_name):
        path = self.get_configmap_workload_url(configmap_name=configmap_name)
        return self.send(method='get', path=path, params={})

    def search_configmap_jinja2_v1(self, ns_name="", limit=None, configmap_name=""):
        path = self.get_common_configmap_search_url_v1(ns_name=ns_name, limit=limit, configmap_name=configmap_name)
        return self.send(method='get', path=path)
