import pytest
from common.settings import RERUN_TIMES, K8S_NAMESPACE, USERNAME, REGION_NAME, AUDIT_UNABLED
from new_case.service.service import Service
from new_case.service.conftest import data_list, wrong_list, create_casename_list


@pytest.mark.acp_containerplatform
@pytest.mark.flaky(reruns=RERUN_TIMES, reruns_delay=3)
class TestPutService(object):

    def setup_class(self):
        self.service_client = Service()
        self.k8s_namespace = K8S_NAMESPACE

    def teardown_class(self):
        for item in data_list:
            self.service_client.delete_service(self.k8s_namespace, item['service_name'])

    @pytest.mark.parametrize("data", data_list, ids=create_casename_list)
    def 测试_标准API_删除内部路由L1(self, data):
        ret = self.service_client.delete_service(self.k8s_namespace, data['service_name'])
        assert ret.status_code == 200, "删除{}类型内部路由失败:{}".format(data['type'], ret.text)
        values = self.service_client.generate_jinja_data("verify_data/service/delete_response.jinja2", data)
        assert self.service_client.is_sub_dict(values, ret.json()), \
            "删除内部路由比对数据失败，返回数据{}，期望数据{}".format(ret.json(), values)

    def 测试_标准API_删除内部路由L1_不存在(self):
        ret = self.service_client.delete_service(self.k8s_namespace, wrong_list['service_name'])
        assert ret.status_code == 404, "删除不存在的内部路由失败:{}".format(ret.text)

    @pytest.mark.skipif(AUDIT_UNABLED, reason="do not have audit")
    def 测试内部路由删除审计(self):
        payload = {"user_name": USERNAME, "operation_type": "delete", "resource_type": "services",
                   "resource_name": data_list[0]['service_name']}
        result = self.service_client.search_audit(payload)
        payload.update({"namespace": K8S_NAMESPACE, "region_name": REGION_NAME})
        values = self.service_client.generate_jinja_data("./verify_data/audit/audit.jinja2", payload)
        assert self.service_client.is_sub_dict(values, result.json()), "审计数据不符合预期"
