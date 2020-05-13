from common.base_request import Common
from common import settings
import base64
from common.utils import dockerjson


class Secret(Common):
    data_list = [
        {
            "secret_name": "{}-ares-opaque-secret".format(settings.RESOURCE_PREFIX),
            "secret_type": "Opaque",
            "opaque_key": "opaque_key",
            "opaque_value": str(base64.b64encode("opaque_value".encode('utf-8')), 'utf8')
        },
        {
            "secret_name": "{}-ares-ssh-secret".format(settings.RESOURCE_PREFIX),
            "secret_type": "kubernetes.io/ssh-auth",
            "ssh_privatevalue": str(base64.b64encode("value".encode('utf-8')), 'utf8'),
        },
        {
            "secret_name": "{}-ares-base-secret".format(settings.RESOURCE_PREFIX),
            "secret_type": "kubernetes.io/basic-auth",
            "username": str(base64.b64encode("username".encode('utf-8')), 'utf8'),
            "password": str(base64.b64encode("password".encode('utf-8')), 'utf8')
        },
        {
            "secret_name": "{}-ares-docker-secret".format(settings.RESOURCE_PREFIX),
            "secret_type": "kubernetes.io/dockerconfigjson",
            "dockerconfigjson": dockerjson("index.alauda.cn", "alauda", "alauda", "hchan@alauda.io"),
        }
    ]
    casename_list = ["Opaque类型", "SSH类型", "用户名-密码类型", "镜像服务类型"]

    def create_secret_url(self, ns_name=settings.K8S_NAMESPACE):
        return "kubernetes/{}/api/v1/namespaces/{}/secrets".format(self.region_name, ns_name)

    def get_secret_url_list(self, ns_name=settings.K8S_NAMESPACE, limit=None):
        return limit and "kubernetes/{}/api/v1/namespaces/{}/secrets?limit={}".format(self.region_name, ns_name, limit) \
               or "kubernetes/{}/api/v1/namespaces/{}/secrets".format(self.region_name, ns_name)

    def get_secret_url(self, ns_name=settings.K8S_NAMESPACE, secret_name=''):
        return "kubernetes/{}/api/v1/namespaces/{}/secrets/{}".format(self.region_name, ns_name, secret_name)

    def updata_secret_url(self, ns_name=settings.K8S_NAMESPACE, secret_name=''):
        return "kubernetes/{}/api/v1/namespaces/{}/secrets/{}".format(self.region_name, ns_name, secret_name)

    def delete_secret_url(self, ns_name=settings.K8S_NAMESPACE, secret_name=''):
        return "kubernetes/{}/api/v1/namespaces/{}/secrets/{}".format(self.region_name, ns_name, secret_name)

    def get_common_secret_search_url_v1(self, ns_name=settings.K8S_NAMESPACE, limit=1, secret_name=None):
        return limit and "acp/v1/resources/search/kubernetes/{}/api/v1/namespaces/{}/secrets?" \
                         "limit={}&keyword={}&field=metadata.name".format(self.region_name, ns_name, limit, secret_name)

    def create_secret(self, file, data):
        path = self.create_secret_url()
        data = self.generate_jinja_data(file, data)
        return self.send(method='post', path=path, json=data, params={})

    def get_secret_list(self, limit=None):
        path = self.get_secret_url_list(limit=limit)
        return self.send(method='get', path=path, params={})

    def get_secret_detail(self, secret_name):
        path = self.get_secret_url(secret_name=secret_name)
        return self.send(method='get', path=path, params={})

    def delete_secret(self, secret_name, ns_name=settings.K8S_NAMESPACE):
        path = self.delete_secret_url(secret_name=secret_name, ns_name=ns_name)
        return self.send(method='delete', path=path, params={})

    def update_secret(self, secret_name, file, data):
        path = self.updata_secret_url(secret_name=secret_name)
        data = self.generate_jinja_data(file, data)
        return self.send(method='put', path=path, json=data, params={})

    def search_secret_jinja2_v1(self, ns_name="", limit=None, secret_name=""):
        path = self.get_common_secret_search_url_v1(ns_name=ns_name, limit=limit, secret_name=secret_name)
        return self.send(method='get', path=path)
