import pytest
import json
import base64
from new_case.secret.secret import Secret
from common import settings
from common.base_request import Common


@pytest.mark.BAT
@pytest.mark.acp_containerplatform
@pytest.mark.flaky(reruns=settings.RERUN_TIMES, reruns_delay=3)
class Testsecret(object):
    data_list = {
        "secret_name": "{}-ares-tls-secret".format(settings.RESOURCE_PREFIX),
        "secret_type": "kubernetes.io/tls",
        "tls_crt": str(base64.b64encode("tlscrt".encode('utf-8')), 'utf8'),
        "tls_key": str(base64.b64encode("tlskey".encode('utf-8')), 'utf8')
    }

    def setup_class(self):
        self.secret_tool = Secret()
        self.verify_template = Common.generate_jinja_template(self, './verify_data/secret/create_response.jinja2')
        self.verify_delete_template = Common.generate_jinja_template(self,
                                                                     './verify_data/secret/delete_response.jinja2')

    @pytest.mark.prepare
    def 测试TLS保密字典创建(self):
        self.data_list.update({"K8S_NAMESPACE": settings.K8S_NAMESPACE})
        # create manager_secret_basic_auth
        ret = self.secret_tool.create_secret('./test_data/secret/create_secret.jinja2', data=self.data_list)

        assert ret.status_code == 201, "创建{}类型保密字典失败:{}".format(self.data_list['secret_type'], ret.text)
        value = self.verify_template.render(self.data_list)

        assert self.secret_tool.is_sub_dict(json.loads(value), ret.json()), \
            "创建保密字典比对数据失败，返回数据:{},期望数据:{}".format(ret.json(), json.loads(value))

    @pytest.mark.upgrade
    def 测试获取保密字典列表(self):
        # get maanger_secret list
        ret = self.secret_tool.get_secret_list()
        assert ret.status_code == 200, "获取保密字典列表失败:{}".format(ret.text)

    @pytest.mark.upgrade
    def 测试更新TLS保密字典(self):
        self.data_list.update({"K8S_NAMESPACE": settings.K8S_NAMESPACE, "description": "update secret"})
        # update manager_secret_basic_auth
        ret = self.secret_tool.update_secret(self.data_list['secret_name'], './test_data/secret/create_secret.jinja2',
                                             data=self.data_list)
        assert ret.status_code == 200, "更新{}类型保密字典失败:{}".format(self.data_list["secret_type"], ret.text)
        value = self.verify_template.render(self.data_list)

        assert self.secret_tool.is_sub_dict(json.loads(value), ret.json()), \
            "更新保密字典比对数据失败，返回数据:{},期望数据:{}".format(ret.json(), json.loads(value))

    @pytest.mark.upgrade
    def 测试获取TLS保密字典详情(self):
        ret = self.secret_tool.get_secret_detail(self.data_list["secret_name"])
        assert ret.status_code == 200, "获取{}类型的保密字典详情失败{}".format(self.data_list["secret_type"], ret.text)
        assert self.data_list["secret_name"] in ret.text and "update secret" in ret.text, "{}类型的保密字典更新失败:{}".format(
            ret.text)
        value = self.verify_template.render(self.data_list)

        assert self.secret_tool.is_sub_dict(json.loads(value), ret.json()), \
            "获取保密字典比对数据失败，返回数据:{},期望数据:{}".format(ret.json(), json.loads(value))

    @pytest.mark.delete
    def 测试删除TLS保密字典(self):
        ret = self.secret_tool.delete_secret(self.data_list["secret_name"])
        assert ret.status_code == 200, "删除{}类型的保密字典失败:{}".format(self.data_list["secret_type", ret.text])

        assert self.secret_tool.check_exists(self.secret_tool.get_secret_url(secret_name=self.data_list["secret_name"]),
                                             404), "删除失败"
        value = self.verify_delete_template.render(self.data_list)

        assert self.secret_tool.is_sub_dict(json.loads(value), ret.json()), \
            "删除保密字典比对数据失败，返回数据:{},期望数据:{}".format(ret.json(), json.loads(value))
