import pytest

from common.settings import K8S_NAMESPACE, RERUN_TIMES, CASE_TYPE
from new_case.service.conftest import l0_data_list
from new_case.service.service import Service
from time import sleep


@pytest.mark.BAT
@pytest.mark.acp_containerplatform
@pytest.mark.flaky(reruns=RERUN_TIMES, reruns_delay=3)
class TestService(object):

    def setup_class(self):
        self.service_client = Service()
        self.k8s_namespace = K8S_NAMESPACE
        l0_data_list.update({"namespace": self.k8s_namespace})

    def teardown_class(self):
        if CASE_TYPE not in ("prepare", "delete", "upgrade"):
            self.service_client.delete_service(self.k8s_namespace, l0_data_list["service_name"])

    @pytest.mark.prepare
    def 测试_标准API_创建内部路由_ClusterIP一组数据(self):
        ret = self.service_client.create_service(self.k8s_namespace, './test_data/service/service.jinja2', l0_data_list)
        assert ret.status_code == 201, "创建{}类型内部路由失败:{}".format(l0_data_list['type'], ret.text)
        values = self.service_client.generate_jinja_data("verify_data/service/create_response.jinja2", l0_data_list)
        assert self.service_client.is_sub_dict(values, ret.json()), \
            "创建内部路由比对数据失败，返回数据{}，期望数据{}".format(ret.json(), values)

    @pytest.mark.upgrade
    def 测试_标准API_内部路由详情_ClusterIP一组数据(self):
        ret = self.service_client.get_service(self.k8s_namespace, l0_data_list['service_name'])
        assert ret.status_code == 200, "获取{}类型内部路由详情失败:{}".format(l0_data_list['type'], ret.text)
        values = self.service_client.generate_jinja_data("verify_data/service/create_response.jinja2", l0_data_list)
        assert self.service_client.is_sub_dict(values, ret.json()), \
            "获取内部路由详情比对数据失败，返回数据{}，期望数据{}".format(ret.json(), values)

    @pytest.mark.upgrade
    def 测试_标准API_内部路由列表(self):
        sleep(5)
        ret = self.service_client.list_service(self.k8s_namespace)
        assert ret.status_code == 200, "获取内部路由列表失败:{}".format(ret.text)
        values = self.service_client.generate_jinja_data("verify_data/service/create_response.jinja2", l0_data_list)
        values.pop('kind')
        values.pop('apiVersion')
        content = self.service_client.get_k8s_resource_data(ret.json(), l0_data_list['service_name'], 'items')
        assert self.service_client.is_sub_dict(values, content), \
            "获取内部路由列表比对数据失败，返回数据{}，期望数据{}".format(content, values)

    @pytest.mark.upgrade
    def 测试_标准API_搜索内部路由_ClusterIP一组数据(self):
        l0_data_list.update({"namespace": self.k8s_namespace})
        ret = self.service_client.search_service(self.k8s_namespace, l0_data_list['service_name'])
        assert ret.status_code == 200, "搜索内部路由失败:{}".format(ret.text)
        values = self.service_client.generate_jinja_data("verify_data/service/create_response.jinja2", l0_data_list)
        content = self.service_client.get_k8s_resource_data(ret.json(), l0_data_list['service_name'], 'items')
        assert self.service_client.is_sub_dict(values, content), \
            "搜索内部路由比对数据失败，返回数据{}，期望数据{}".format(content, values)

    @pytest.mark.upgrade
    def 测试_标准API_更新内部路由_ClusterIP一组数据(self):
        ret = self.service_client.get_service(self.k8s_namespace, l0_data_list['service_name'])
        resourceVersion = ret.json()['metadata']['resourceVersion']
        clusterIP = ret.json()['spec']['clusterIP']
        l0_data_list.update({"namespace": self.k8s_namespace,
                             'selector': 'true', 'resourceVersion': resourceVersion, 'clusterIP': clusterIP})
        ret = self.service_client.update_service(self.k8s_namespace, l0_data_list['service_name'],
                                                 './test_data/service/service.jinja2', l0_data_list)
        assert ret.status_code == 200, "更新{}类型内部路由失败:{}".format(l0_data_list['type'], ret.text)
        values = self.service_client.generate_jinja_data("verify_data/service/create_response.jinja2", l0_data_list)
        assert self.service_client.is_sub_dict(values, ret.json()), \
            "更新内部路由比对数据失败，返回数据{}，期望数据{}".format(ret.json(), values)

    @pytest.mark.delete
    def 测试_标准API_删除内部路由_ClusterIP一组数据(self):
        l0_data_list.update({"namespace": self.k8s_namespace})
        ret = self.service_client.delete_service(self.k8s_namespace, l0_data_list['service_name'])
        assert ret.status_code == 200, "删除{}类型内部路由失败:{}".format(l0_data_list['type'], ret.text)
        values = self.service_client.generate_jinja_data("verify_data/service/delete_response.jinja2", l0_data_list)
        assert self.service_client.is_sub_dict(values, ret.json()), \
            "删除内部路由比对数据失败，返回数据{}，期望数据{}".format(ret.json(), values)
