import sys
import time
from common import settings
from common.base_request import Common
from common.log import logger


class Namespace(Common):
    def get_namespace_url(self, namesapce, region_name=settings.REGION_NAME):
        return "kubernetes/{}/api/v1/namespaces/{}".format(region_name, namesapce)

    def get_namespace_list_url(self, limit='', continues=''):
        if limit != '':
            path = 'auth/v1/projects/{}/clusters/{}/namespaces/?limit={}'.format(self.project_name, self.region_name,
                                                                                 limit)
            if continues != '':
                path = '{}&continue={}'.format(path, continues)
        elif limit == '':
            path = 'auth/v1/projects/{}/clusters/{}/namespaces/'.format(self.project_name, self.region_name)
            if continues != '':
                path = '{}&continue={}'.format(path, continues)
        return path

    def create_namespaces_url(self, region_name=settings.REGION_NAME):
        return "acp/v1/kubernetes/{}/general-namespaces".format(region_name)

    def get_resourcequota_url(self, namespace=''):
        return "kubernetes/{}/api/v1/namespaces/{}/resourcequotas/default".format(self.region_name, namespace)

    def get_limitrange_url(self, namespace=''):
        return "kubernetes/{}/api/v1/namespaces/{}/limitranges/default".format(self.region_name, namespace)

    def create_namespace(self, file, data, region_name=settings.REGION_NAME):
        logger.info(sys._getframe().f_code.co_name.center(50, '*'))
        url = self.create_namespaces_url(region_name)
        if file.endswith('jinja2'):
            data = self.generate_jinja_data(file, data)
            return self.send(method='post', path=url, json=data, params={})
        else:
            data = self.generate_data(file, data)
            return self.send(method='post', path=url, data=data, params={})

    def update_resourcequota(self, name, file, data, auth=None):
        logger.info(sys._getframe().f_code.co_name.center(50, '*'))
        path = self.get_resourcequota_url(namespace=name)
        data = self.generate_jinja_data(file, data)
        return self.send(method="PATCH", path=path, json=data, auth=auth, headers={"Content-Type": "application/merge-patch+json"})

    def update_limitrange(self, name, file, data, auth=None):
        logger.info(sys._getframe().f_code.co_name.center(50, '*'))
        path = self.get_limitrange_url(namespace=name)
        data = self.generate_jinja_data(file, data)
        return self.send(method="PATCH", path=path, json=data, auth=auth, headers={"Content-Type": "application/merge-patch+json"})

    def get_namespaces(self, namespace, region_name=settings.REGION_NAME):
        logger.info(sys._getframe().f_code.co_name.center(50, '*'))
        path = self.get_namespace_url(namespace, region_name)
        return self.send(method="GET", path=path)

    def delete_namespace(self, namespace, region_name=settings.REGION_NAME):
        logger.info(sys._getframe().f_code.co_name.center(50, '*'))
        path = "kubernetes/{}/api/v1/namespaces/{}".format(region_name, namespace)
        return self.send(method="DELETE", path=path)

    def list_namespaces(self, limit='', continues='', auth=None):
        logger.info(sys._getframe().f_code.co_name.center(50, '*'))
        path = self.get_namespace_list_url(limit, continues)
        return self.send(method="GET", path=path, params={}, auth=auth)

    def detail_resourcequota(self, namespace, auth=None):
        logger.info(sys._getframe().f_code.co_name.center(50, '*'))
        path = self.get_resourcequota_url(namespace)
        return self.send(method="GET", path=path, auth=auth)

    def detail_limitrange(self, namespace, auth=None):
        logger.info(sys._getframe().f_code.co_name.center(50, '*'))
        path = self.get_limitrange_url(namespace)
        return self.send(method="GET", path=path, auth=auth)

    # 查询没有关联到项目的命名空间列表
    def list_namespace_not_link_project(self, labelSelector="{}/project".format(settings.DEFAULT_LABEL), auth=None):
        logger.info(sys._getframe().f_code.co_name.center(50, '*'))
        path = "kubernetes/{}/api/v1/namespaces?labelSelector=!{}".format(self.region_name, labelSelector)
        return self.send(method="GET", path=path, auth=auth)

    # 导入命名空间,也就是把命名空间和项目关联起来
    def link_namespace_with_project(self, file, data, namespace, auth=None):
        logger.info(sys._getframe().f_code.co_name.center(50, '*'))
        path = "acp/v1/kubernetes/{}/general-namespaces/{}".format(self.region_name, namespace)
        data = self.generate_jinja_data(file, data)
        return self.send(method="PUT", path=path, json=data, auth=auth)

    # 从项目中移除命名空间
    def remove_namespace_from_project(self, namespace, auth=None):
        logger.info(sys._getframe().f_code.co_name.center(50, '*'))
        path = "kubernetes/{}/api/v1/namespaces/{}".format(self.region_name, namespace)
        data = {"metadata": {"labels": {"{}/project".format(settings.DEFAULT_LABEL): None}}}
        return self.send(method="PATCH", path=path, json=data, auth=auth, headers={"Content-Type": "application/merge-patch+json"})

    def get_namelist_of_namespace(self, rep_json):
        namelist = []
        items_list = rep_json.get("items")
        for data in items_list:
            namelist.append(data.get("metadata").get("name"))
        return namelist

    def wait_resourcequota_status(self, namespace, timeout=15):
        end_time = time.time() + timeout
        while time.time() < end_time:
            ret = self.detail_resourcequota(namespace)
            if ret.status_code == 200 and self.get_value(ret.json(), "status") != {}:
                return True
            else:
                time.sleep(1)
