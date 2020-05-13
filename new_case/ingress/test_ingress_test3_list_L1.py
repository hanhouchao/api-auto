import pytest

from common.settings import RERUN_TIMES, K8S_NAMESPACE
from new_case.ingress.conftest import data_list
from new_case.ingress.ingress import Ingress


@pytest.mark.acp_containerplatform
@pytest.mark.flaky(reruns=RERUN_TIMES, reruns_delay=3)
class TestListIngress(object):

    def setup_class(self):
        self.ingress_client = Ingress()
        self.k8s_namespace = K8S_NAMESPACE

    def 测试_标准API_访问规则列表L1_不存在(self):
        ret = self.ingress_client.list_ingress('namespacenotexit')
        assert ret.status_code == 200, "获取不存在的命名空间下的访问规则列表失败:{}".format(ret.text)
        items = self.ingress_client.get_value(ret.json(), "items")
        assert items == [], "获取不存在的命名空间下的访问规则列表失败:{}".format(ret.text)

    def 测试_标准API_访问规则列表L1_有limit和continue参数(self):
        ret = self.ingress_client.list_ingress(self.k8s_namespace, limits=1)
        assert ret.status_code == 200, "获取访问规则列表失败:{}".format(ret.text)
        continues = self.ingress_client.get_value(ret.json(), "metadata.continue")
        ret_cnt = self.ingress_client.list_ingress(self.k8s_namespace, limits=1, continues=continues)
        assert ret_cnt.status_code == 200, "获取访问规则列表失败:{}".format(ret_cnt.text)
        assert ret.json() != ret_cnt.json(), "分页数据相同，第一页数据:{},第二页数据:{}".format(ret.json(), ret_cnt.json())

    def 测试_标准API_访问规则列表L1_按名称搜索(self):
        data = data_list[0]
        data.update({"namespace": self.k8s_namespace})
        ingress_name = data['ingress_name']
        names = [ingress_name, ingress_name.upper(), ingress_name.capitalize(), ingress_name[:-1]]
        for name in names:
            ret = self.ingress_client.search_ingress(self.k8s_namespace, name)
            assert ret.status_code == 200, "搜索访问规则失败:{}".format(ret.text)
            values = self.ingress_client.generate_jinja_data("verify_data/ingress/create_response.jinja2", data)
            content = self.ingress_client.get_k8s_resource_data(ret.json(), data['ingress_name'], 'items')
            assert self.ingress_client.is_sub_dict(values, content), \
                "搜索访问规则比对数据失败，返回数据{}，期望数据{}".format(content, values)

    def 测试_标准API_访问规则列表L1_按名称搜索_不存在(self):
        name = data_list[0]['ingress_name'] + 'notexist'
        ret = self.ingress_client.search_ingress(self.k8s_namespace, name)
        assert ret.status_code == 200, "搜索不存在的访问规则失败:{}".format(ret.text)
        content = self.ingress_client.get_value(ret.json(), 'items')
        assert content == [], "搜索不存在的访问规则比对数据失败，返回数据{}，期望数据{}".format(content, [])
