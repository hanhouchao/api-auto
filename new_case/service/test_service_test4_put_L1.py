import pytest
from common.settings import RERUN_TIMES, K8S_NAMESPACE, USERNAME, REGION_NAME, AUDIT_UNABLED
from new_case.service.service import Service
from new_case.service.conftest import update_data_list, wrong_list, update_casename_list


@pytest.mark.acp_containerplatform
@pytest.mark.flaky(reruns=RERUN_TIMES, reruns_delay=3)
class TestUpdateService(object):

    def setup_class(self):
        self.service_client = Service()
        self.k8s_namespace = K8S_NAMESPACE

    @pytest.mark.parametrize("data", update_data_list, ids=update_casename_list)
    def 测试_标准API_更新内部路由L1(self, data):
        ret = self.service_client.get_service(self.k8s_namespace, data['service_name'])
        resourceVersion = ret.json()['metadata']['resourceVersion']
        clusterIP = ret.json()['spec']['clusterIP']
        data.update({"namespace": self.k8s_namespace,
                     'selector': 'true', 'resourceVersion': resourceVersion, 'clusterIP': clusterIP})
        ret = self.service_client.update_service(self.k8s_namespace, data['service_name'],
                                                 './test_data/service/service.jinja2', data)
        assert ret.status_code == 200, "更新{}类型内部路由失败:{}".format(data['type'], ret.text)
        values = self.service_client.generate_jinja_data("verify_data/service/create_response.jinja2", data)
        assert self.service_client.is_sub_dict(values, ret.json()), \
            "更新内部路由比对数据失败，返回数据{}，期望数据{}".format(ret.json(), values)

    def 测试_标准API_更新内部路由L1_不存在(self):
        ret = self.service_client.update_service(self.k8s_namespace, wrong_list['service_name'],
                                                 './test_data/service/service.jinja2', wrong_list)
        assert ret.status_code == 404, "更新不存在的内部路由失败:{}".format(ret.text)

    @pytest.mark.skipif(AUDIT_UNABLED, reason="do not have audit")
    def 测试内部路由更新审计(self):
        payload = {"user_name": USERNAME, "operation_type": "update", "resource_type": "services",
                   "resource_name": update_data_list[0]['service_name']}
        result = self.service_client.search_audit(payload)
        payload.update({"namespace": K8S_NAMESPACE, "region_name": REGION_NAME})
        values = self.service_client.generate_jinja_data("./verify_data/audit/audit.jinja2", payload)
        assert self.service_client.is_sub_dict(values, result.json()), "审计数据不符合预期"
