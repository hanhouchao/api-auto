import pytest
import base64
from new_case.secret.secret import Secret
from common import settings
from common.base_request import Common


@pytest.mark.acp_containerplatform
@pytest.mark.flaky(reruns=settings.RERUN_TIMES, reruns_delay=3)
class TestGetSecret(object):
    data = {
        "secret_name": "{}-ares-opaque-secret-2".format(settings.RESOURCE_PREFIX),
        "secret_type": "Opaque",
        "opaque_key": "opaque_key",
        "opaque_value": str(base64.b64encode("opaque_value".encode('utf-8')), 'utf8'),
        "description": "多组数据"
    }

    data_list = Secret.data_list

    def setup_class(self):
        self.secret_tool = Secret()
        self.verify_template = Common.generate_jinja_template(self, './verify_data/secret/create_response.jinja2')

    def 测试获取保密字典列表_不带limit(self):
        # 测试获取保密字典列表_不带limit
        ret = self.secret_tool.get_secret_list()
        assert ret.status_code == 200, "获取保密字典列表失败:{}".format(ret.text)

        secret_num = len(ret.json()["items"])
        assert secret_num >= len(self.data_list), "获取保密字典列表,不传limit时返回失败,预期至少返回{}个,实际返回{}个".format(len(self.data_list),
                                                                                                   secret_num)

    def 测试获取保密字典列表_带limit(self):
        # 测试获取保密字典列表,带limit
        ret = self.secret_tool.get_secret_list(limit=1)
        assert ret.status_code == 200, "获取保密字典列表失败:{}".format(ret.text)

        secret_num = len(ret.json()["items"])
        assert secret_num == 1, "获取保密字典列表,传limit=1时返回失败,预期返回1个,实际返回{}个".format(secret_num)

    def 测试_搜索secret(self):
        data = self.data
        data.update({"K8S_NAMESPACE": settings.K8S_NAMESPACE})
        ser = self.secret_tool.search_secret_jinja2_v1(ns_name=data["K8S_NAMESPACE"], limit=20,
                                                       secret_name=data["secret_name"])
        assert ser.status_code == 200, "没有搜索到{}，{}".format(data["secret_name"], ser.text)

        value = self.secret_tool.generate_jinja_data("./verify_data/secret/search_secret.jinja2", data)
        assert self.secret_tool.is_sub_dict(value, ser.json()), "搜索secret比对数据失败，返回数据:{},期望数据:{}".\
            format(ser.json(), value)
