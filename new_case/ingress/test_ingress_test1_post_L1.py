import pytest
from common.settings import RERUN_TIMES, K8S_NAMESPACE, REGION_NAME, USERNAME, AUDIT_UNABLED
from new_case.ingress.conftest import data_list, l1_create_casename
from new_case.ingress.ingress import Ingress


@pytest.mark.acp_containerplatform
@pytest.mark.flaky(reruns=RERUN_TIMES, reruns_delay=3)
class TestPostIngress(object):

    def setup_class(self):
        self.ingress_client = Ingress()
        self.k8s_namespace = K8S_NAMESPACE

    @pytest.mark.parametrize("data", data_list, ids=l1_create_casename)
    def 测试_标准API_创建访问规则L1(self, data):
        data.update({"namespace": self.k8s_namespace})
        ret = self.ingress_client.create_ingress(self.k8s_namespace, './test_data/ingress/ingress.jinja2', data)
        assert ret.status_code == 201, "创建访问规则失败:{}".format(ret.text)
        values = self.ingress_client.generate_jinja_data("verify_data/ingress/create_response.jinja2", data)
        assert self.ingress_client.is_sub_dict(values, ret.json()), \
            "创建访问规则比对数据失败，返回数据{}，期望数据{}".format(ret.json(), values)

    def 测试_标准API_创建访问规则L1_已存在(self):
        data = data_list[0]
        data.update({"namespace": self.k8s_namespace})
        ret = self.ingress_client.create_ingress(self.k8s_namespace, './test_data/ingress/ingress.jinja2', data)
        assert ret.status_code == 409, "创建已存在的访问规则失败:{}".format(ret.text)

    @pytest.mark.skipif(AUDIT_UNABLED, reason="do not have audit")
    def 不测试访问规则创建审计(self):
        payload = {"user_name": USERNAME, "operation_type": "create", "resource_type": "ingresses",
                   "resource_name": data_list[0]['ingress_name']}
        result = self.ingress_client.search_audit(payload)
        payload.update({"namespace": K8S_NAMESPACE, "region_name": REGION_NAME, "code": 201})
        values = self.ingress_client.generate_jinja_data("./verify_data/audit/audit.jinja2", payload)
        assert self.ingress_client.is_sub_dict(values, result.json()), "审计数据不符合预期"
