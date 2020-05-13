# coding=utf-8
import datetime

import requests
from requests.adapters import HTTPAdapter
import urllib3
from common import settings
from common.log import logger, color
import copy

s = requests.Session()
s.mount('http://', HTTPAdapter(max_retries=3))
s.mount('https://', HTTPAdapter(max_retries=3))


class AlaudaRequest(object):
    def __init__(self):
        self.endpoint = settings.API_URL
        self.region_name = settings.REGION_NAME
        self.calico_region = settings.CALICO_REGION
        self.k8s_namespace = settings.K8S_NAMESPACE
        self.project_name = settings.PROJECT_NAME
        self.default_ns = settings.DEFAULT_NS
        self.proxy = settings.PROXY
        self.headers = settings.headers

    def send(self, method, path, **content):
        """
        使用和原生的requests.request一致，只是对url和auth params做了些特殊处理
        :param method:
        :param path:
        :param auth:
        :param content:
        :return:
        """
        url = self._get_url(path)
        # if auth:
        #     content["auth"] = auth
        # else:
        #     content["auth"] = self.auth
        if "headers" in content and content['headers']:
            headers = copy.deepcopy(self.headers)
            headers.update(content['headers'])
            content["headers"] = headers
        else:
            content["headers"] = self.headers
        # if "params" not in content:
        #     content["params"] = copy.deepcopy(self.params)
        content["proxies"] = self.proxy
        content['verify'] = False
        if 'timeout' not in content:
            content["timeout"] = 20
        date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info("time={},Requesting url={}, method={}, args={}".format(date_time, url, method, content))
        urllib3.disable_warnings()
        try:
            response = s.request(method, url, **content)
        except Exception as e:
            logger.error(color.red(e))
            return requests.Response()
        if response.status_code < 200 or response.status_code > 300:
            logger.error(color.red("response code={}, text={}".format(response.status_code, response.text)))
        else:
            logger.info(color.green("response code={}".format(response.status_code)))
        return response

    def _get_url(self, path):
        return "{}/{}".format(self.endpoint, path)
