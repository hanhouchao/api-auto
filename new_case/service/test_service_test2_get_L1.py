import pytest

from common.settings import RERUN_TIMES, K8S_NAMESPACE
from new_case.service.service import Service
from new_case.service.conftest import data_list, wrong_list, create_casename_list


@pytest.mark.acp_containerplatform
@pytest.mark.flaky(reruns=RERUN_TIMES, reruns_delay=3)
class TestGetService(object):

    def setup_class(self):
        self.service_client = Service()
        self.k8s_namespace = K8S_NAMESPACE

    @pytest.mark.parametrize("data", data_list, ids=create_casename_list)
    def 测试_标准API_内部路由详情L1(self, data):
        data.update({"namespace": self.k8s_namespace})
        ret = self.service_client.get_service(self.k8s_namespace, data['service_name'])
        assert ret.status_code == 200, "获取{}类型内部路由详情失败:{}".format(data['type'], ret.text)
        values = self.service_client.generate_jinja_data("verify_data/service/create_response.jinja2", data)
        assert self.service_client.is_sub_dict(values, ret.json()), \
            "获取内部路由详情比对数据失败，返回数据{}，期望数据{}".format(ret.json(), values)

    def 测试_标准API_内部路由详情L1_不存在(self):
        ret = self.service_client.get_service(self.k8s_namespace, wrong_list['service_name'])
        assert ret.status_code == 404, "获取不存在的内部路由详情失败:{}".format(ret.text)
