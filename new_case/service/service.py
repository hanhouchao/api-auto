from common import settings
from common.base_request import Common


class Service(Common):
    def __init__(self):
        super(Service, self).__init__()

    def get_service(self, namespace_name, service_name):
        path = "kubernetes/{}/api/v1/namespaces/{}/services/{}".format(self.region_name, namespace_name, service_name)
        return self.send(method='GET', path=path)

    def list_service(self, namespace_name, limits=1000, continues='', selector=''):
        path = "kubernetes/{}/api/v1/namespaces/{}/services?limit={}".format(self.region_name, namespace_name, limits)
        if continues != '':
            path = '{}&continue={}'.format(path, continues)
        if selector != '':
            path = '{}&fieldSelector=metadata.name=={}'.format(path, selector)
        return self.send(method='GET', path=path)

    def delete_service(self, namespace_name, service_name):
        path = "kubernetes/{}/api/v1/namespaces/{}/services/{}".format(self.region_name, namespace_name, service_name)
        return self.send(method='DELETE', path=path)

    def create_service(self, namespace_name, file, data):
        path = "kubernetes/{}/api/v1/namespaces/{}/services".format(self.region_name, namespace_name)
        data = self.generate_jinja_data(file, data)
        return self.send(method='POST', path=path, json=data)

    def update_service(self, namespace_name, service_name, file, data):
        path = "kubernetes/{}/api/v1/namespaces/{}/services/{}".format(self.region_name, namespace_name, service_name)
        data = self.generate_jinja_data(file, data)
        return self.send(method='PUT', path=path, json=data)

    def search_service(self, namespace_name, name, region_name=settings.REGION_NAME):
        url = "acp/v1/resources/search/kubernetes/{}/api/v1/namespaces/{}/services?limit=20&keyword={}" \
              "&field=metadata.name".format(region_name, namespace_name, name)
        return self.send('get', url)
