import pytest
import base64
import json
from new_case.secret.secret import Secret
from common import settings
from common.base_request import Common


@pytest.mark.acp_containerplatform
@pytest.mark.flaky(reruns=settings.RERUN_TIMES, reruns_delay=3)
class TestPostSecret(object):
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

    @pytest.mark.parametrize("data", data_list, ids=Secret.casename_list)
    def 测试创建各种保密字典(self, data):
        data.update({"K8S_NAMESPACE": settings.K8S_NAMESPACE})
        # create manager_secret_basic_auth
        ret = self.secret_tool.create_secret('./test_data/secret/create_secret.jinja2', data=data)

        assert ret.status_code == 201, "创建{}类型保密字典失败:{}".format(data['secret_type'], ret.text)
        value = self.verify_template.render(data)

        assert self.secret_tool.is_sub_dict(json.loads(value), ret.json()), \
            "创建保密字典比对数据失败，返回数据:{},期望数据:{}".format(ret.json(), json.loads(value))

    def 测试创建包含多组数据的保密字典(self, data=data):
        data.update({"K8S_NAMESPACE": settings.K8S_NAMESPACE})
        ret = self.secret_tool.create_secret('./test_data/secret/create_secret.jinja2', data=data)

        assert ret.status_code == 201, "创建包含多组数据的{}类型的保密字典失败:{}".format(data['secret_type'], ret.text)
        value = self.verify_template.render(data)

        assert self.secret_tool.is_sub_dict(json.loads(value), ret.json()), \
            "创建保密字典比对数据失败，返回数据:{},期望数据:{}".format(ret.json(), json.loads(value))

    @pytest.mark.skipif(settings.AUDIT_UNABLED, reason="do not have audit")
    def 不测试保密字典创建审计(self):
        payload = {"user_name": settings.USERNAME, "operation_type": "create", "resource_type": "secrets",
                   "resource_name": self.data['secret_name']}
        result = self.secret_tool.search_audit(payload)
        payload.update({"namespace": settings.K8S_NAMESPACE, "region_name": settings.REGION_NAME, "code": 201})
        values = self.secret_tool.generate_jinja_data("./verify_data/audit/audit.jinja2", payload)
        assert self.secret_tool.is_sub_dict(values, result.json()), "审计数据不符合预期"
