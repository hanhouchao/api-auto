import pytest
from common.settings import RERUN_TIMES, USERNAME, GLOBAL_REGION_NAME, AUDIT_UNABLED
from new_case.domain.conftest import full_data_list, ext_data_list, full_casename, ext_casename
from new_case.domain.domain import Domain


@pytest.mark.acp_containerplatform
@pytest.mark.flaky(reruns=RERUN_TIMES, reruns_delay=3)
class TestPostDomain(object):

    def setup_class(self):
        self.domain_client = Domain()

    @pytest.mark.parametrize("data", full_data_list, ids=full_casename)
    def 测试_创建全域名_L1(self, data):
        ret = self.domain_client.create_domain('./test_data/domain/create_domain.jinja2', data)
        assert ret.status_code == 201, "创建全域名失败:{}".format(ret.text)
        values = self.domain_client.generate_jinja_data("verify_data/domain/create_response.jinja2", data)
        assert self.domain_client.is_sub_dict(values, ret.json()), \
            "创建全域名比对数据失败，返回数据{}，期望数据{}".format(ret.json(), values)

    @pytest.mark.parametrize("data", ext_data_list, ids=ext_casename)
    def 测试_创建泛域名_L1(self, data):
        ret = self.domain_client.create_domain('./test_data/domain/create_domain.jinja2', data)
        assert ret.status_code == 201, "创建泛域名失败:{}".format(ret.text)
        values = self.domain_client.generate_jinja_data("verify_data/domain/create_response.jinja2", data)
        assert self.domain_client.is_sub_dict(values, ret.json()), \
            "创建泛域名比对数据失败，返回数据{}，期望数据{}".format(ret.json(), values)

    @pytest.mark.skipif(AUDIT_UNABLED, reason="do not have audit")
    def 测试全域名创建审计(self):
        payload = {"user_name": USERNAME, "operation_type": "create", "resource_type": "domains",
                   "resource_name": full_data_list[0]['timestamp']}
        result = self.domain_client.search_audit(payload)
        payload.update({"namespace": "", "region_name": GLOBAL_REGION_NAME, "code": 201})
        values = self.domain_client.generate_jinja_data("./verify_data/audit/audit.jinja2", payload)
        assert self.domain_client.is_sub_dict(values, result.json()), "审计数据不符合预期"
