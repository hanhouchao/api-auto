import pytest
from common.settings import RERUN_TIMES, K8S_NAMESPACE, USERNAME, REGION_NAME, AUDIT_UNABLED
from new_case.ingress.ingress import Ingress
from new_case.ingress.conftest import data_list, l1_create_casename


@pytest.mark.acp_containerplatform
@pytest.mark.flaky(reruns=RERUN_TIMES, reruns_delay=3)
class TestPutIngress(object):

    def setup_class(self):
        self.ingress_client = Ingress()
        self.k8s_namespace = K8S_NAMESPACE

    @pytest.mark.parametrize("data", data_list, ids=l1_create_casename)
    def 测试_标准API_删除访问规则L1(self, data):
        ret = self.ingress_client.delete_ingress(self.k8s_namespace, data['ingress_name'])
        assert ret.status_code == 200, "删除访问规则失败:{}".format(ret.text)
        values = self.ingress_client.generate_jinja_data("verify_data/ingress/delete_response.jinja2", data)
        assert self.ingress_client.is_sub_dict(values, ret.json()), \
            "删除访问规则比对数据失败，返回数据{}，期望数据{}".format(ret.json(), values)

    def 测试_标准API_删除访问规则L1_不存在(self):
        ingress_name = 'ingressnotexit'
        ret = self.ingress_client.delete_ingress(self.k8s_namespace, ingress_name)
        assert ret.status_code == 404, "删除不存在的访问规则失败:{}".format(ret.text)

    @pytest.mark.skipif(AUDIT_UNABLED, reason="do not have audit")
    def 测试访问规则删除审计(self):
        payload = {"user_name": USERNAME, "operation_type": "delete", "resource_type": "ingresses",
                   "resource_name": data_list[0]['ingress_name']}
        result = self.ingress_client.search_audit(payload)
        payload.update({"namespace": K8S_NAMESPACE, "region_name": REGION_NAME})
        values = self.ingress_client.generate_jinja_data("./verify_data/audit/audit.jinja2", payload)
        assert self.ingress_client.is_sub_dict(values, result.json()), "审计数据不符合预期"
