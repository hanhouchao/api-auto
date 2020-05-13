from common import settings
from common.base_request import Common


class Ingress(Common):
    def __init__(self):
        super(Ingress, self).__init__()

    def get_ingress(self, namespace_name, ingress_name):
        path = "kubernetes/{}/apis/extensions/v1beta1/namespaces/{}/ingresses/{}".format(self.region_name,
                                                                                         namespace_name, ingress_name)
        return self.send(method='GET', path=path)

    def list_ingress(self, namespace_name, limits=20, continues='', selector=''):
        path = "kubernetes/{}/apis/extensions/v1beta1/namespaces/{}/ingresses?limit={}".format(self.region_name,
                                                                                               namespace_name, limits)
        if continues != '':
            path = '{}&continue={}'.format(path, continues)
        if selector != '':
            path = '{}&fieldSelector=metadata.name=={}'.format(path, selector)
        return self.send(method='GET', path=path)

    def delete_ingress(self, namespace_name, ingress_name):
        path = "kubernetes/{}/apis/extensions/v1beta1/namespaces/{}/ingresses/{}".format(self.region_name,
                                                                                         namespace_name, ingress_name)
        return self.send(method='DELETE', path=path)

    def create_ingress(self, namespace_name, file, data):
        path = "kubernetes/{}/apis/extensions/v1beta1/namespaces/{}/ingresses".format(self.region_name, namespace_name)
        data = self.generate_jinja_data(file, data)
        return self.send(method='POST', path=path, json=data)

    def update_ingress(self, namespace_name, ingress_name, file, data):
        path = "kubernetes/{}/apis/extensions/v1beta1/namespaces/{}/ingresses/{}".format(self.region_name,
                                                                                         namespace_name, ingress_name)
        data = self.generate_jinja_data(file, data)
        return self.send(method='PUT', path=path, json=data)

    def search_ingress(self, namespace_name, ingress_name, region_name=settings.REGION_NAME,
                       project_name=settings.PROJECT_NAME):
        url = "acp/v1/resources/search/kubernetes/{}/apis/extensions/v1beta1/namespaces/{}/ingresses?limit=20" \
              "&keyword={}&project={}&field=metadata.name".format(region_name, namespace_name, ingress_name,
                                                                  project_name)
        return self.send('get', url)
