import pytest

from common.settings import RERUN_TIMES, K8S_NAMESPACE
from new_case.service.conftest import data_list
from new_case.service.service import Service


@pytest.mark.acp_containerplatform
@pytest.mark.flaky(reruns=RERUN_TIMES, reruns_delay=3)
class TestListService(object):

    def setup_class(self):
        self.service_client = Service()
        self.k8s_namespace = K8S_NAMESPACE

    def 测试_标准API_内部路由列表L1_不存在(self):
        ret = self.service_client.list_service('namespacenotexit')
        assert ret.status_code == 200, "获取不存在的命名空间下的内部路由列表失败:{}".format(ret.text)
        items = self.service_client.get_value(ret.json(), "items")
        assert items == [], "获取不存在的命名空间下的内部路由列表失败:{}".format(ret.text)

    def 测试_标准API_内部路由列表L1_有limit和continue参数(self):
        ret = self.service_client.list_service(self.k8s_namespace, limits=1)
        assert ret.status_code == 200, "获取内部路由列表失败:{}".format(ret.text)
        continues = self.service_client.get_value(ret.json(), "metadata.continue")
        ret_cnt = self.service_client.list_service(self.k8s_namespace, limits=1, continues=continues)
        assert ret_cnt.status_code == 200, "获取内部路由列表失败:{}".format(ret_cnt.text)
        assert ret.json() != ret_cnt.json(), "分页数据相同，第一页数据:{},第二页数据:{}".format(ret.json(), ret_cnt.json())

    def 测试_标准API_内部路由列表L1_按名称搜索(self):
        data = data_list[0]
        data.update({"namespace": self.k8s_namespace})
        svc_name = data['service_name']
        names = [svc_name, svc_name.upper(), svc_name.capitalize(), svc_name[:-1]]
        for name in names:
            ret = self.service_client.search_service(self.k8s_namespace, name)
            assert ret.status_code == 200, "搜索内部路由失败:{}".format(ret.text)
            values = self.service_client.generate_jinja_data("verify_data/service/create_response.jinja2", data)
            content = self.service_client.get_k8s_resource_data(ret.json(), data['service_name'], 'items')
            assert self.service_client.is_sub_dict(values, content), \
                "搜索内部路由比对数据失败，返回数据{}，期望数据{}".format(content, values)

    def 测试_标准API_内部路由列表L1_按名称搜索_不存在(self):
        name = data_list[0]['service_name'] + 'notexist'
        ret = self.service_client.search_service(self.k8s_namespace, name)
        assert ret.status_code == 200, "搜索不存在的内部路由失败:{}".format(ret.text)
        content = self.service_client.get_value(ret.json(), 'items')
        assert content == [], "搜索不存在的内部路由比对数据失败，返回数据{}，期望数据{}".format(content, [])
