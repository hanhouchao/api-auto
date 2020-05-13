import pytest

from common.settings import RERUN_TIMES, K8S_NAMESPACE
from new_case.ingress.conftest import l2_data_list
from new_case.ingress.ingress import Ingress


@pytest.mark.Low
@pytest.mark.acp_containerplatform
@pytest.mark.flaky(reruns=RERUN_TIMES, reruns_delay=3)
class TestPostIngressNegative(object):

    def setup_class(self):
        self.ingress_client = Ingress()
        self.k8s_namespace = K8S_NAMESPACE
        self.teardown_class(self)

    def teardown_class(self):
        for item in l2_data_list:
            if item["ingress_name"]:
                self.ingress_client.delete_ingress(self.k8s_namespace, item["ingress_name"])

    def 测试_创建名称为空的访问规则L2(self):
        data = l2_data_list[0]
        data.update({"namespace": self.k8s_namespace})
        ret = self.ingress_client.create_ingress(self.k8s_namespace, './test_data/ingress/ingress.jinja2', data)
        assert ret.status_code == 422, "用例执行失败:{}".format(ret.status_code)
        values = self.ingress_client.generate_jinja_data("verify_data/ingress/create_response_failure.jinja2", data)
        assert self.ingress_client.is_sub_dict(values, ret.json()), \
            "创建访问规则比对数据失败，返回数据{}，期望数据{}".format(ret.json(), values)

    def 测试_创建名称为63位英文字符的访问规则L2(self):
        data = l2_data_list[1]
        data.update({"namespace": self.k8s_namespace})
        ret = self.ingress_client.create_ingress(self.k8s_namespace, './test_data/ingress/ingress.jinja2', data)
        assert ret.status_code == 201, "创建访问规则失败:{}".format(ret.text)
        values = self.ingress_client.generate_jinja_data("verify_data/ingress/create_response.jinja2", data)
        assert self.ingress_client.is_sub_dict(values, ret.json()), \
            "创建访问规则比对数据失败，返回数据{}，期望数据{}".format(ret.json(), values)

    @pytest.mark.skip(reason="http://jira.alauda.cn/browse/ACP-1576")
    def 测试_创建名称为64位英文字符的访问规则L2(self):
        data = l2_data_list[2]
        data.update({"namespace": self.k8s_namespace})
        ret = self.ingress_client.create_ingress(self.k8s_namespace, './test_data/ingress/ingress.jinja2', data)
        assert ret.status_code == 422, "创建访问规则失败:{}".format(ret.text)
        values = self.ingress_client.generate_jinja_data("verify_data/ingress/create_response_failure.jinja2", data)
        assert self.ingress_client.is_sub_dict(values, ret.json()), \
            "创建访问规则比对数据失败，返回数据{}，期望数据{}".format(ret.json(), values)

    def 测试_Body体里的namespace与请求路径里的不一致L2(self):
        data = l2_data_list[3]
        ret = self.ingress_client.create_ingress(self.k8s_namespace, './test_data/ingress/ingress.jinja2', data)
        assert ret.status_code == 400, "测试用例执行失败:{}".format(ret.text)
        values = self.ingress_client.generate_jinja_data("verify_data/ingress/create_response_failure.jinja2", data)
        assert self.ingress_client.is_sub_dict(values, ret.json()), \
            "创建访问规则比对数据失败，返回数据{}，期望数据{}".format(ret.json(), values)

    def 测试_创建内部路由为空的访问规则L2(self):
        data = l2_data_list[4]
        data.update({"namespace": self.k8s_namespace})
        ret = self.ingress_client.create_ingress(self.k8s_namespace,
                                                 './test_data/ingress/ingress_service_name_null.jinja2', data)
        assert ret.status_code == 422, "测试用例执行失败:{}".format(ret.text)
        values = self.ingress_client.generate_jinja_data("verify_data/ingress/create_response_failure.jinja2", data)
        assert self.ingress_client.is_sub_dict(values, ret.json()), \
            "创建访问规则比对数据失败，返回数据{}，期望数据{}".format(ret.json(), values)

    @pytest.mark.skip(reason="http://jira.alauda.cn/browse/ACP-1579")
    def 测试_创建服务端口号位65536的访问规则L2(self):
        data = l2_data_list[5]
        data.update({"namespace": self.k8s_namespace})
        ret = self.ingress_client.create_ingress(self.k8s_namespace, './test_data/ingress/ingress.jinja2', data)
        assert ret.status_code != 201, "测试用例执行失败:{}".format(ret.text)

    def 测试_创建名称已存在L2(self):
        data = l2_data_list[6]
        data.update({"namespace": self.k8s_namespace})
        for i in range(2):
            ret = self.ingress_client.create_ingress(self.k8s_namespace, './test_data/ingress/ingress.jinja2', data)
        assert ret.status_code == 409, "创建访问规则失败:{}".format(ret.text)
        values = self.ingress_client.generate_jinja_data("verify_data/ingress/create_response_failure.jinja2", data)
        assert self.ingress_client.is_sub_dict(values, ret.json()), \
            "创建访问规则比对数据失败，返回数据{}，期望数据{}".format(ret.json(), values)

    def 测试_创建名称带有非法字符的访问规则L2(self):
        data = l2_data_list[7]
        data.update({"namespace": self.k8s_namespace})
        ret = self.ingress_client.create_ingress(self.k8s_namespace, './test_data/ingress/ingress.jinja2', data)
        assert ret.status_code == 422, "用例执行失败:{}".format(ret.text)
        values = self.ingress_client.generate_jinja_data("verify_data/ingress/create_response_failure.jinja2", data)
        assert self.ingress_client.is_sub_dict(values, ret.json()), \
            "创建访问规则比对数据失败，返回数据{}，期望数据{}".format(ret.json(), values)

    def 测试_创建规则路径不以反斜线开头的访问规则L2(self):
        data = l2_data_list[8]
        data.update({"namespace": self.k8s_namespace})
        ret = self.ingress_client.create_ingress(self.k8s_namespace, './test_data/ingress/ingress.jinja2', data)
        assert ret.status_code == 422, "用例执行失败:{}".format(ret.text)
        values = self.ingress_client.generate_jinja_data("verify_data/ingress/create_response_failure.jinja2", data)
        assert self.ingress_client.is_sub_dict(values, ret.json()), \
            "创建访问规则比对数据失败，返回数据{}，期望数据{}".format(ret.json(), values)

    def 测试_创建域名含有特殊字符的访问规则L2(self):
        data = l2_data_list[9]
        data.update({"namespace": self.k8s_namespace})
        ret = self.ingress_client.create_ingress(self.k8s_namespace, './test_data/ingress/ingress.jinja2', data)
        assert ret.status_code == 422, "用例执行失败:{}".format(ret.text)
        values = self.ingress_client.generate_jinja_data("verify_data/ingress/create_response_failure.jinja2", data)
        assert self.ingress_client.is_sub_dict(values, ret.json()), \
            "创建访问规则比对数据失败，返回数据{}，期望数据{}".format(ret.json(), values)
