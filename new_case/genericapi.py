import sys

from common import settings
from common.base_request import Common
from common.log import logger


class GenericApi(Common):
    def __init__(self, resource_type, region_name=settings.REGION_NAME):
        super(GenericApi, self).__init__()
        self.resource_type = resource_type
        self.region_name = region_name

    def get_resourcetype_url(self):
        return 'acp/v1/resources/{}/resourcetypes'.format(self.region_name)

    def list_resourcetypes(self):
        logger.info(sys._getframe().f_code.co_name.center(50, '*'))
        url = self.get_resourcetype_url()
        return self.send(method='get', path=url)

    def get_api(self, kind):
        contents = self.list_resourcetypes().json()
        for content in contents:
            for con in content['resources']:
                if con['name'] == kind:
                    if 'group' in con:
                        api = 'apis/{}/{}'.format(con['group'], con['version'])
                    else:
                        api = 'api/{}'.format(con['version'])
                    return api
        return ''

    # 集群级资源
    def get_region_resource_url(self, resource_name=None):
        api = self.get_api(self.resource_type)
        return resource_name and 'kubernetes/{}/{}/{}/{}'.format(self.region_name, api, self.resource_type,
                                                                 resource_name) or 'kubernetes/{}/{}/{}'.format(
            self.region_name, api, self.resource_type)

    # 命名空间级资源
    def get_namespace_resource_url(self, namespace_name, resource_name=None):
        api = self.get_api(self.resource_type)
        return resource_name and 'kubernetes/{}/{}/namespaces/{}/{}/{}'.format(self.region_name, api,
                                                                               self.resource_type, namespace_name,
                                                                               resource_name) or 'kubernetes/{}/{}/namespaces/{}/{}/'.format(
            self.region_name, api, self.resource_type, namespace_name)

    def create_region_resource(self, file, data, auth=None):
        logger.info(sys._getframe().f_code.co_name.center(50, '*'))
        url = self.get_region_resource_url()
        data = self.generate_data(file, data)
        return self.send(method='post', path=url, data=data, params={}, auth=auth)

    def list_region_resource(self, auth=None):
        logger.info(sys._getframe().f_code.co_name.center(50, '*'))
        url = self.get_region_resource_url()
        return self.send(method='get', path=url, params={}, auth=auth)

    def detail_region_resource(self, resource_name, auth=None):
        logger.info(sys._getframe().f_code.co_name.center(50, '*'))
        url = self.get_region_resource_url(resource_name)
        return self.send(method='get', path=url, params={}, auth=auth)

    def update_region_resource(self, resource_name, file, data, auth=None):
        logger.info(sys._getframe().f_code.co_name.center(50, '*'))
        url = self.get_region_resource_url(resource_name)
        data = self.generate_data(file, data)
        return self.send(method='put', path=url, data=data, params={}, auth=auth)

    def delete_region_resource(self, resource_name, auth=None):
        logger.info(sys._getframe().f_code.co_name.center(50, '*'))
        url = self.get_region_resource_url(resource_name)
        return self.send(method='delete', path=url, params={}, auth=auth)

    def create_namespace_resource(self, namespace_name, file, data, auth=None):
        logger.info(sys._getframe().f_code.co_name.center(50, '*'))
        url = self.get_namespace_resource_url(namespace_name)
        data = self.generate_data(file, data)
        return self.send(method='post', path=url, data=data, params={}, auth=auth)

    def list_namespace_resource(self, namespace_name, auth=None):
        logger.info(sys._getframe().f_code.co_name.center(50, '*'))
        url = self.get_namespace_resource_url(namespace_name)
        return self.send(method='get', path=url, params={}, auth=auth)

    def detail_namespace_resource(self, namespace_name, resource_name, auth=None):
        logger.info(sys._getframe().f_code.co_name.center(50, '*'))
        url = self.get_namespace_resource_url(namespace_name, resource_name)
        return self.send(method='get', path=url, params={}, auth=auth)

    def update_namespace_resource(self, namespace_name, resource_name, file, data, auth=None):
        logger.info(sys._getframe().f_code.co_name.center(50, '*'))
        url = self.get_namespace_resource_url(namespace_name, resource_name)
        data = self.generate_data(file, data)
        return self.send(method='put', path=url, data=data, params={}, auth=auth)

    def delete_namespace_resource(self, namespace_name, resource_name, auth=None):
        logger.info(sys._getframe().f_code.co_name.center(50, '*'))
        url = self.get_namespace_resource_url(namespace_name, resource_name)
        return self.send(method='delete', path=url, params={}, auth=auth)
