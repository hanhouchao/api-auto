import sys
from common.base_request import Common
from common.log import logger
from common.settings import DEFAULT_LABEL


class Domain(Common):
    def get_create_domain_url(self):
        return 'apis/crd.alauda.io/v2/domains'

    def get_common_domain_url(self, name=None):
        return name and 'apis/crd.alauda.io/v2/domains/{}'.format(name) or 'apis/crd.alauda.io/v2/domains'

    def list_domain_url(self, limits=20, continues='', project_name=''):
        path = 'apis/crd.alauda.io/v2/domains?limit={}'.format(limits)
        if continues != '':
            path = '{}&continue={}'.format(path, continues)
        if project_name != '':
            path = '{}&labelSelector=project.{}/name%20in%20({},ALL_ALL),' \
                   'cluster.{}/name%20in%20({},ALL_ALL)'.format(path, DEFAULT_LABEL, project_name, DEFAULT_LABEL, self.region_name)
        return path

    def create_domain(self, file, data):
        logger.info(sys._getframe().f_code.co_name.center(50, '*'))
        url = self.get_create_domain_url()
        data = self.generate_jinja_data(file, data)
        return self.send(method='post', path=url, json=data, params={})

    def list_domain(self, limits=20, continues='', project_name=''):
        logger.info(sys._getframe().f_code.co_name.center(50, '*'))
        url = self.list_domain_url(limits, continues, project_name)
        return self.send(method='get', path=url, params={})

    def detail_domain(self, name):
        logger.info(sys._getframe().f_code.co_name.center(50, '*'))
        url = self.get_common_domain_url(name)
        return self.send(method='get', path=url, params={})

    def update_domain(self, name, file, data):
        logger.info(sys._getframe().f_code.co_name.center(50, '*'))
        url = self.get_common_domain_url(name)
        data = self.generate_jinja_data(file, data)
        return self.send(method='patch', path=url, json=data, params={}, headers={"Content-Type": "application/merge-patch+json"})

    def delete_domain(self, name):
        logger.info(sys._getframe().f_code.co_name.center(50, '*'))
        url = self.get_common_domain_url(name)
        return self.send(method='delete', path=url, params={})
