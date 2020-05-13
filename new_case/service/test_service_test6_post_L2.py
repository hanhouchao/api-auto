import pytest

from common.log import logger
from common.settings import RERUN_TIMES, K8S_NAMESPACE
from new_case.service.conftest import l2_data_list, l2_create_casename_list, l2_wrong_list, \
    l2_wrong_create_list, l2_known_issues_data_list, l2_known_issues_create_list
from new_case.service.service import Service


@pytest.mark.Low
@pytest.mark.acp_containerplatform
@pytest.mark.flaky(reruns=RERUN_TIMES, reruns_delay=3)
class TestPostService(object):

    def setup_class(self):
        self.service_client = Service()
        self.k8s_namespace = K8S_NAMESPACE
        self.teardown_class(self)

    def teardown_class(self):
        for item in l2_data_list + l2_wrong_list + l2_known_issues_data_list:
            if item["service_name"]:
                self.service_client.delete_service(self.k8s_namespace, item['service_name'])

    @pytest.mark.parametrize("data", l2_data_list, ids=l2_create_casename_list)
    def 测试_标准API_创建内部路由L2_正向(self, data):
        data.update({"namespace": self.k8s_namespace})
        ret = self.service_client.create_service(self.k8s_namespace, './test_data/service/service.jinja2', data)
        assert ret.status_code == 201, "创建{}类型内部路由失败:{}".format(data['type'], ret.text)
        values = self.service_client.generate_jinja_data("verify_data/service/create_response.jinja2", data)
        assert self.service_client.is_sub_dict(values, ret.json()), \
            "创建内部路由比对数据失败，返回数据{}，期望数据{}".format(ret.json(), values)

    @pytest.mark.parametrize("data", l2_wrong_list, ids=l2_wrong_create_list)
    def 测试_标准API_创建内部路由L2_逆向(self, data):
        data.update({"namespace": self.k8s_namespace})
        if data.get("exist_name", ''):
            self.service_client.create_service(self.k8s_namespace, './test_data/service/service.jinja2', data)
        ret = self.service_client.create_service(self.k8s_namespace, './test_data/service/service.jinja2', data)
        logger.info(data['status_code'])
        assert ret.status_code == data['status_code'], "测试用例执行失败:{}".format(ret.text)
        values = self.service_client.generate_jinja_data("verify_data/service/create_response_failure.jinja2", data)
        assert self.service_client.is_sub_dict(values, ret.json()), \
            "创建内部路由比对数据失败，返回数据{}，期望数据{}".format(ret.json(), values)

    @pytest.mark.skip(reason="http://jira.alauda.cn/browse/ACP-1587, http://jira.alauda.cn/browse/ACP-1588")
    @pytest.mark.parametrize("data", l2_known_issues_data_list, ids=l2_known_issues_create_list)
    def 测试_标准API_创建内部路由L2_逆向_已知问题(self, data):
        data.update({"namespace": self.k8s_namespace})
        if data.get("exist_name", ''):
            self.service_client.create_service(self.k8s_namespace, './test_data/service/service.jinja2', data)
        ret = self.service_client.create_service(self.k8s_namespace, './test_data/service/service.jinja2', data)
        logger.info(data['status_code'])
        assert ret.status_code == data['status_code'], "测试用例执行失败:{}".format(ret.text)
        values = self.service_client.generate_jinja_data("verify_data/service/create_response_failure.jinja2", data)
        assert self.service_client.is_sub_dict(values, ret.json()), \
            "创建内部路由比对数据失败，返回数据{}，期望数据{}".format(ret.json(), values)
