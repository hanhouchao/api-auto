import pytest
import json
import base64
from new_case.secret.secret import Secret
from common import settings
from common.base_request import Common
from common.utils import dockerjson


@pytest.mark.acp_containerplatform
@pytest.mark.flaky(reruns=settings.RERUN_TIMES, reruns_delay=3)
class TestPutSecret(object):
    update_data = [
        {
            "secret_name": "{}-ares-opaque-secret".format(settings.RESOURCE_PREFIX),
            "secret_type": "Opaque",
            "opaque_key": "new_opaque_key",
            "opaque_value": str(base64.b64encode("new_opaque_value".encode('utf-8')), 'utf8')
        },
        {
            "secret_name": "{}-ares-ssh-secret".format(settings.RESOURCE_PREFIX),
            "secret_type": "kubernetes.io/ssh-auth",
            "ssh_privatevalue": str(base64.b64encode("new_value".encode('utf-8')), 'utf8'),
        },
        {
            "secret_name": "{}-ares-base-secret".format(settings.RESOURCE_PREFIX),
            "secret_type": "kubernetes.io/basic-auth",
            "username": str(base64.b64encode("new_username".encode('utf-8')), 'utf8'),
            "password": str(base64.b64encode("new_password".encode('utf-8')), 'utf8')
        },
        {
            "secret_name": "{}-ares-docker-secret".format(settings.RESOURCE_PREFIX),
            "secret_type": "kubernetes.io/dockerconfigjson",
            "dockerconfigjson": dockerjson("new.index.alauda.cn", "new_alauda", "new_alauda",
                                           "new_hchan@alauda.io"),
        }
    ]
    casename_list = ["Opaque类型", "SSH类型", "用户名-密码类型", "镜像服务类型"]

    def setup_class(self):
        self.secret_tool = Secret()
        self.verify_template = Common.generate_jinja_template(self, './verify_data/secret/create_response.jinja2')

    @pytest.mark.parametrize("data", update_data, ids=casename_list)
    def 测试更新各种类型保密字典的数据(self, data):
        data.update({"K8S_NAMESPACE": settings.K8S_NAMESPACE, "description": "update secret"})
        ret = self.secret_tool.update_secret(data['secret_name'], './test_data/secret/create_secret.jinja2', data=data)
        assert ret.status_code == 200, "更新{}类型保密字典失败:{}".format(data["secret_type"], ret.text)
        value = self.verify_template.render(data)

        assert self.secret_tool.is_sub_dict(json.loads(value), ret.json()), \
            "更新保密字典比对数据失败，返回数据:{},期望数据:{}".format(ret.json(), json.loads(value))

    @pytest.mark.skipif(settings.AUDIT_UNABLED, reason="do not have audit")
    def 测试保密字典更新审计(self):
        payload = {"user_name": settings.USERNAME, "operation_type": "update", "resource_type": "secrets",
                   "resource_name": self.update_data[0]['secret_name']}
        result = self.secret_tool.search_audit(payload)
        payload.update({"namespace": settings.K8S_NAMESPACE, "region_name": settings.REGION_NAME})
        values = self.secret_tool.generate_jinja_data("./verify_data/audit/audit.jinja2", payload)
        assert self.secret_tool.is_sub_dict(values, result.json()), "审计数据不符合预期"
