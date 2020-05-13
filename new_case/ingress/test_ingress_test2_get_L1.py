import pytest
from common.settings import RERUN_TIMES, K8S_NAMESPACE
from new_case.ingress.ingress import Ingress
from new_case.ingress.conftest import data_list, l1_create_casename


@pytest.mark.acp_containerplatform
@pytest.mark.flaky(reruns=RERUN_TIMES, reruns_delay=3)
class TestGetIngress(object):

    def setup_class(self):
        self.ingress_client = Ingress()
        self.k8s_namespace = K8S_NAMESPACE

    @pytest.mark.parametrize("data", data_list, ids=l1_create_casename)
    def 测试_标准API_访问规则详情L1(self, data):
        data.update({"namespace": self.k8s_namespace})
        ret = self.ingress_client.get_ingress(self.k8s_namespace, data['ingress_name'])
        assert ret.status_code == 200, "获取访问规则详情失败:{}".format(ret.text)
        values = self.ingress_client.generate_jinja_data("verify_data/ingress/create_response.jinja2", data)
        assert self.ingress_client.is_sub_dict(values, ret.json()), \
            "获取访问规则详情比对数据失败，返回数据{}，期望数据{}".format(ret.json(), values)

    def 测试_标准API_访问规则详情L1_不存在(self):
        ingress_name = 'ingressnotexit'
        ret = self.ingress_client.get_ingress(self.k8s_namespace, ingress_name)
        assert ret.status_code == 404, "获取不存在的访问规则详情失败:{}".format(ret.text)
