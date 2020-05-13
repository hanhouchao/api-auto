import pytest
from common.settings import K8S_NAMESPACE, RERUN_TIMES, CASE_TYPE
from new_case.ingress.conftest import l0_data_list, l0_casemame
from new_case.ingress.ingress import Ingress


@pytest.mark.BAT
@pytest.mark.acp_containerplatform
@pytest.mark.flaky(reruns=RERUN_TIMES, reruns_delay=3)
class TestIngress(object):

    def setup_class(self):
        self.ingress_client = Ingress()
        self.k8s_namespace = K8S_NAMESPACE

    def teardown_class(self):
        if CASE_TYPE not in ("prepare", "upgrade", "delete"):
            for data in l0_data_list:
                self.ingress_client.delete_ingress(self.k8s_namespace, data["ingress_name"])

    @pytest.mark.prepare
    @pytest.mark.parametrize("data", l0_data_list, ids=l0_casemame)
    def 测试_标准API_创建访问规则(self, data):
        data.update({"namespace": self.k8s_namespace})
        ret = self.ingress_client.create_ingress(self.k8s_namespace, './test_data/ingress/ingress.jinja2', data)
        assert ret.status_code == 201, "创建访问规则失败:{}".format(ret.text)
        values = self.ingress_client.generate_jinja_data("verify_data/ingress/create_response.jinja2", data)
        assert self.ingress_client.is_sub_dict(values, ret.json()), \
            "创建访问规则比对数据失败，返回数据{}，期望数据{}".format(ret.json(), values)

    @pytest.mark.upgrade
    @pytest.mark.parametrize("data", l0_data_list, ids=l0_casemame)
    def 测试_标准API_访问规则详情(self, data):
        data.update({"namespace": self.k8s_namespace})
        ret = self.ingress_client.get_ingress(self.k8s_namespace, data['ingress_name'])
        assert ret.status_code == 200, "获取访问规则详情失败:{}".format(ret.text)
        values = self.ingress_client.generate_jinja_data("verify_data/ingress/create_response.jinja2", data)
        assert self.ingress_client.is_sub_dict(values, ret.json()), \
            "获取访问规则详情比对数据失败，返回数据{}，期望数据{}".format(ret.json(), values)

    @pytest.mark.upgrade
    @pytest.mark.parametrize("data", l0_data_list, ids=l0_casemame)
    def 测试_标准API_访问规则列表(self, data):
        data.update({"namespace": self.k8s_namespace})
        ret = self.ingress_client.list_ingress(self.k8s_namespace)
        assert ret.status_code == 200, "获取访问规则列表失败:{}".format(ret.text)
        values = self.ingress_client.generate_jinja_data("verify_data/ingress/create_response.jinja2", data)
        values.pop('kind')
        values.pop('apiVersion')
        content = self.ingress_client.get_k8s_resource_data(ret.json(), data['ingress_name'], 'items')
        assert self.ingress_client.is_sub_dict(values, content), \
            "获取访问规则列表比对数据失败，返回数据{}，期望数据{}".format(content, values)

    @pytest.mark.upgrade
    @pytest.mark.parametrize("data", l0_data_list, ids=l0_casemame)
    def 测试_标准API_搜索访问规则(self, data):
        data.update({"namespace": self.k8s_namespace})
        ret = self.ingress_client.search_ingress(self.k8s_namespace, data['ingress_name'])
        assert ret.status_code == 200, "搜索访问规则失败:{}".format(ret.text)
        values = self.ingress_client.generate_jinja_data("verify_data/ingress/create_response.jinja2", data)
        content = self.ingress_client.get_k8s_resource_data(ret.json(), data['ingress_name'], 'items')
        assert self.ingress_client.is_sub_dict(values, content), \
            "搜索访问规则比对数据失败，返回数据{}，期望数据{}".format(content, values)

    @pytest.mark.upgrade
    @pytest.mark.parametrize("data", l0_data_list, ids=l0_casemame)
    def 测试_标准API_更新访问规则(self, data):
        ret = self.ingress_client.get_ingress(self.k8s_namespace, data['ingress_name'])
        resourceVersion = ret.json()['metadata']['resourceVersion']
        data.update({"namespace": self.k8s_namespace, 'resourceVersion': resourceVersion})
        ret = self.ingress_client.update_ingress(self.k8s_namespace, data['ingress_name'],
                                                 './test_data/ingress/ingress.jinja2', data)
        assert ret.status_code == 200, "更新访问规则失败:{}".format(ret.text)
        values = self.ingress_client.generate_jinja_data("verify_data/ingress/create_response.jinja2", data)
        assert self.ingress_client.is_sub_dict(values, ret.json()), \
            "更新访问规则比对数据失败，返回数据{}，期望数据{}".format(ret.json(), values)

    @pytest.mark.delete
    @pytest.mark.parametrize("data", l0_data_list, ids=l0_casemame)
    def 测试_标准API_删除访问规则(self, data):
        data.update({"namespace": self.k8s_namespace})
        ret = self.ingress_client.delete_ingress(self.k8s_namespace, data['ingress_name'])
        assert ret.status_code == 200, "删除访问规则失败:{}".format(ret.text)
        values = self.ingress_client.generate_jinja_data("verify_data/ingress/delete_response.jinja2", data)
        assert self.ingress_client.is_sub_dict(values, ret.json()), \
            "删除访问规则比对数据失败，返回数据{}，期望数据{}".format(ret.json(), values)
