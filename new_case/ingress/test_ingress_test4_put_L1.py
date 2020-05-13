import pytest
from common.settings import RERUN_TIMES, K8S_NAMESPACE, USERNAME, REGION_NAME, AUDIT_UNABLED
from new_case.ingress.ingress import Ingress
from new_case.ingress.conftest import update_data_list, l0_data_list, l1_update_casename


@pytest.mark.acp_containerplatform
@pytest.mark.flaky(reruns=RERUN_TIMES, reruns_delay=3)
class TestUpdateIngress(object):

    def setup_class(self):
        self.ingress_client = Ingress()
        self.k8s_namespace = K8S_NAMESPACE

    @pytest.mark.parametrize("data", update_data_list, ids=l1_update_casename)
    def 测试_标准API_更新访问规则L1(self, data):
        ret = self.ingress_client.get_ingress(self.k8s_namespace, data['ingress_name'])
        resourceVersion = ret.json()['metadata']['resourceVersion']
        data.update({"namespace": self.k8s_namespace, 'resourceVersion': resourceVersion})
        ret = self.ingress_client.update_ingress(self.k8s_namespace, data['ingress_name'],
                                                 './test_data/ingress/ingress.jinja2', data)
        assert ret.status_code == 200, "更新访问规则失败:{}".format(ret.text)
        values = self.ingress_client.generate_jinja_data("verify_data/ingress/create_response.jinja2", data)
        assert self.ingress_client.is_sub_dict(values, ret.json()), \
            "更新访问规则比对数据失败，返回数据{}，期望数据{}".format(ret.json(), values)

    def 测试_标准API_更新访问规则L1_不存在(self):
        ingress_name = 'ingressnotexit'
        l0_data_list[0].update({"namespace": self.k8s_namespace, 'ingress_name': ingress_name})
        ret = self.ingress_client.update_ingress(self.k8s_namespace, ingress_name,
                                                 './test_data/ingress/ingress.jinja2', l0_data_list[0])
        assert ret.status_code == 404, "更新不存在的访问规则失败:{}".format(ret.text)

    @pytest.mark.skipif(AUDIT_UNABLED, reason="do not have audit")
    def 测试更新访问规则审计(self):
        payload = {"user_name": USERNAME, "operation_type": "update", "resource_type": "ingresses",
                   "resource_name": update_data_list[0]['ingress_name']}
        result = self.ingress_client.search_audit(payload)
        payload.update({"namespace": K8S_NAMESPACE, "region_name": REGION_NAME})
        values = self.ingress_client.generate_jinja_data("./verify_data/audit/audit.jinja2", payload)
        assert self.ingress_client.is_sub_dict(values, result.json()), "审计数据不符合预期"
