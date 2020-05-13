import pytest

from common.settings import RERUN_TIMES, K8S_NAMESPACE, RESOURCE_PREFIX, CASE_TYPE
from new_case.configmap.configmap import Configmap


@pytest.mark.BAT
@pytest.mark.acp_containerplatform
@pytest.mark.flaky(reruns=RERUN_TIMES, reruns_delay=3)
class TestCMSuite(object):
    def setup_class(self):
        self.configmap = Configmap()
        self.configmap_ns = K8S_NAMESPACE
        self.configmap_name = '{}-ares-configmap'.format(RESOURCE_PREFIX)
        self.teardown_class(self)
        global data
        data = {
            "configmap_name": self.configmap_name,
            "description": "key-value",
            "namespace": self.configmap_ns,
            "configmap_key": "key",
            "configmap_value": "value"
        }

    def teardown_class(self):
        if CASE_TYPE not in ("prepare", "upgrade", "delete"):
            self.configmap.delete_configmap(self.configmap_name)

    @pytest.mark.prepare
    def 测试key_value模式配置字典增加(self):
        # create configmap
        createconfigmap_result = self.configmap.create_configmap(data)
        assert createconfigmap_result.status_code == 201, "创建配置字典失败:{}".format(createconfigmap_result.text)
        value = self.configmap.generate_jinja_data('verify_data/configmap/create_response.jinja2', data)
        assert self.configmap.is_sub_dict(value, createconfigmap_result.json()), \
            "创建configmap比对数据失败，返回数据:{},期望数据:{}".format(createconfigmap_result.json(), value)

    @pytest.mark.upgrade
    def 测试配置字典列表_无limit参数(self):
        # list configmap
        list_result = self.configmap.get_configmap_list()
        assert list_result.status_code == 200, list_result.text
        assert self.configmap_name in list_result.text, "列表：新建配置字典不在列表中"
        content = self.configmap.get_k8s_resource_data(list_result.json(), self.configmap_name, 'items')
        value = self.configmap.generate_jinja_data('verify_data/configmap/create_response.jinja2', data)
        value.pop('apiVersion')
        value.pop('kind')
        assert self.configmap.is_sub_dict(value, content), "configmap列表比对数据失败，返回数据:{},期望数据:{}".format(
            content, value)

    @pytest.mark.upgrade
    def 测试key_value模式配置字典更新(self):
        # update configmap
        data.update({"configmap_value": "updatecm"})
        update_result = self.configmap.update_configmap(self.configmap_name, data)
        assert update_result.status_code == 200, "更新配置字典出错:{}".format(update_result.text)
        value = self.configmap.generate_jinja_data('verify_data/configmap/create_response.jinja2', data)
        assert self.configmap.is_sub_dict(value, update_result.json()), \
            "更新configmap比对数据失败，返回数据:{},期望数据:{}".format(update_result.json(), value)

    @pytest.mark.upgrade
    def 测试key_value模式配置字典详情(self):
        # detail configmap
        detail_result = self.configmap.get_configmap_detail(self.configmap_name)
        assert detail_result.status_code == 200, detail_result.text
        data.update({"configmap_value": "updatecm"})
        value = self.configmap.generate_jinja_data('verify_data/configmap/create_response.jinja2', data)
        assert self.configmap.is_sub_dict(value, detail_result.json()), \
            "获取configmap详情比对数据失败，返回数据:{},期望数据:{}".format(detail_result.json(), value)

    @pytest.mark.delete
    def 测试key_value模式配置字典删除(self):
        # delete configmap
        delete_result = self.configmap.delete_configmap(self.configmap_name)
        assert delete_result.status_code == 200, "删除配置字典失败：{}".format(delete_result.text)
        value = self.configmap.generate_jinja_data('verify_data/configmap/delete_response.jinja2', data)
        assert self.configmap.is_sub_dict(value, delete_result.json()), \
            "删除configmap比对数据失败，返回数据:{},期望数据:{}".format(delete_result.json(), value)
        assert self.configmap.check_exists(
            self.configmap.get_common_configmap_url(self.configmap_name), 404)
