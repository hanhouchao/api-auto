import pytest
import json
import base64
from new_case.secret.secret import Secret
from common import settings
from common.base_request import Common


@pytest.mark.acp_containerplatform
@pytest.mark.flaky(reruns=settings.RERUN_TIMES, reruns_delay=3)
class TestDeleteSecret(object):
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
        self.verify_delete_template = Common.generate_jinja_template(self,
                                                                     './verify_data/secret/delete_response.jinja2')

    def 测试删除含有多组数据的保密字典(self):
        ret = self.secret_tool.delete_secret(self.data["secret_name"])
        assert ret.status_code == 200, "删除{}类型的保密字典失败:{}".format(self.data["secret_type", ret.text])

        assert self.secret_tool.check_exists(self.secret_tool.get_secret_url(secret_name=self.data["secret_name"]),
                                             404), "删除失败"
        value = self.verify_delete_template.render(self.data)

        assert self.secret_tool.is_sub_dict(json.loads(value), ret.json()), \
            "删除包含多组数据的保密字典比对数据失败，返回数据:{},期望数据:{}".format(ret.json(), json.loads(value))

    @pytest.mark.parametrize("data", data_list, ids=Secret.casename_list)
    def 测试删除保密字典(self, data):
        ret = self.secret_tool.delete_secret(data["secret_name"])
        assert ret.status_code == 200, "删除{}类型的保密字典失败:{}".format(data["secret_type", ret.text])

        assert self.secret_tool.check_exists(self.secret_tool.get_secret_url(secret_name=data["secret_name"]),
                                             404), "删除失败"
        value = self.verify_delete_template.render(data)

        assert self.secret_tool.is_sub_dict(json.loads(value), ret.json()), \
            "删除保密字典比对数据失败，返回数据:{},期望数据:{}".format(ret.json(), json.loads(value))

    @pytest.mark.skipif(settings.AUDIT_UNABLED, reason="do not have audit")
    def 测试保密字典删除审计(self):
        payload = {"user_name": settings.USERNAME, "operation_type": "delete", "resource_type": "secrets",
                   "resource_name": self.data['secret_name']}
        result = self.secret_tool.search_audit(payload)
        payload.update({"namespace": settings.K8S_NAMESPACE, "region_name": settings.REGION_NAME})
        values = self.secret_tool.generate_jinja_data("./verify_data/audit/audit.jinja2", payload)
        assert self.secret_tool.is_sub_dict(values, result.json()), "审计数据不符合预期"
