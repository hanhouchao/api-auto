import pytest
from common.settings import RERUN_TIMES, K8S_NAMESPACE, USERNAME, REGION_NAME, AUDIT_UNABLED
from new_case.service.conftest import data_list, wrong_list, create_casename_list
from new_case.service.service import Service


@pytest.mark.acp_containerplatform
@pytest.mark.flaky(reruns=RERUN_TIMES, reruns_delay=3)
class TestPostService(object):

    def setup_class(self):
        self.service_client = Service()
        self.k8s_namespace = K8S_NAMESPACE

    @pytest.mark.parametrize("data", data_list, ids=create_casename_list)
    def 测试_标准API_创建内部路由L1(self, data):
        data.update({"namespace": self.k8s_namespace})
        ret = self.service_client.create_service(self.k8s_namespace, './test_data/service/service.jinja2', data)
        assert ret.status_code == 201, "创建{}类型内部路由失败:{}".format(data['type'], ret.text)
        values = self.service_client.generate_jinja_data("verify_data/service/create_response.jinja2", data)
        assert self.service_client.is_sub_dict(values, ret.json()), \
            "创建内部路由比对数据失败，返回数据{}，期望数据{}".format(ret.json(), values)

    def 测试_标准API_创建内部路由L1_必填项校验(self):
        wrong_list.update({"namespace": self.k8s_namespace})
        ret = self.service_client.create_service(self.k8s_namespace, './test_data/service/service.jinja2', wrong_list)
        assert ret.status_code == 422, "创建内部路由(缺少必填项)失败:{}".format(ret.text)

    @pytest.mark.skipif(AUDIT_UNABLED, reason="do not have audit")
    def 不测试内部路由创建审计(self):
        payload = {"user_name": USERNAME, "operation_type": "create", "resource_type": "services",
                   "resource_name": data_list[-1]['service_name']}
        result = self.service_client.search_audit(payload)
        payload.update({"namespace": K8S_NAMESPACE, "region_name": REGION_NAME, "code": 201})
        values = self.service_client.generate_jinja_data("./verify_data/audit/audit.jinja2", payload)
        assert self.service_client.is_sub_dict(values, result.json()), "审计数据不符合预期"
