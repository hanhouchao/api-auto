import pytest
from common.settings import RERUN_TIMES
from new_case.domain.conftest import full_data_list, ext_data_list, full_casename, ext_casename
from new_case.domain.domain import Domain


@pytest.mark.acp_containerplatform
@pytest.mark.flaky(reruns=RERUN_TIMES, reruns_delay=3)
class TestListDomain(object):

    def setup_class(self):
        self.domain = Domain()
        self.extensive_domain_name = ext_data_list[0]['name']
        self.full_domain_name = full_data_list[0]['name']

    def 测试_域名列表_L1(self):
        # list domain
        list_result = self.domain.list_domain()
        assert list_result.status_code == 200, list_result.text

        # 比对泛域名
        content = self.domain.get_k8s_resource_data(list_result.json(), self.extensive_domain_name, list_key="items")
        values = self.domain.generate_jinja_data("verify_data/domain/create_response.jinja2", ext_data_list[0])
        assert self.domain.is_sub_dict(values, content), \
            "获取域名列表比对数据泛域名失败，返回数据:{},期望数据:{}".format(content, values)

        # 比对全域名
        content = self.domain.get_k8s_resource_data(list_result.json(), self.full_domain_name, list_key="items")
        values = self.domain.generate_jinja_data("verify_data/domain/create_response.jinja2", full_data_list[0])
        assert self.domain.is_sub_dict(values, content), \
            "获取域名列表比对数据全域名失败，返回数据:{},期望数据:{}".format(content, values)

    def 测试_域名列表_L1_有limit和continue参数(self):
        ret = self.domain.list_domain(limits=1)
        assert ret.status_code == 200, "获取域名列表失败:{}".format(ret.text)
        continues = self.domain.get_value(ret.json(), "metadata.continue")
        ret_cnt = self.domain.list_domain(limits=1, continues=continues)
        assert ret_cnt.status_code == 200, "获取域名列表失败:{}".format(ret_cnt.text)
        assert ret.json() != ret_cnt.json(), "分页数据相同，第一页数据:{},第二页数据:{}".format(ret.json(), ret_cnt.json())

    @pytest.mark.parametrize("data", ext_data_list, ids=ext_casename)
    def 测试_域名列表L1_按项目搜索_验证泛域名(self, data):
        ret = self.domain.list_domain(project_name=self.domain.project_name)
        assert ret.status_code == 200, "获取域名列表失败:{}".format(ret.text)
        content = self.domain.get_k8s_resource_data(ret.json(), data['name'], 'items')
        values = self.domain.generate_jinja_data("verify_data/domain/create_response.jinja2", data)
        if data['region_name'] == self.domain.region_name and data['project_name'] == self.domain.project_name \
                or data['project_name'] == 'ALL_ALL':
            assert self.domain.is_sub_dict(values, content), \
                "按项目过滤域名列表比对数据失败，返回数据{}，期望数据{}".format(content, values)
        else:
            assert content == {}, \
                "按项目过滤域名列表存在不同项目的数据，比对数据失败，返回数据{}，期望数据{}".format(content, values)

    @pytest.mark.parametrize("data", full_data_list, ids=full_casename)
    def 测试_域名列表L1_按项目搜索_验证全域名(self, data):
        ret = self.domain.list_domain(project_name=self.domain.project_name)
        assert ret.status_code == 200, "获取域名列表失败:{}".format(ret.text)
        content = self.domain.get_k8s_resource_data(ret.json(), data['name'], 'items')
        values = self.domain.generate_jinja_data("verify_data/domain/create_response.jinja2", data)
        if data['region_name'] == self.domain.region_name and data['project_name'] == self.domain.project_name or \
                data['project_name'] == 'ALL_ALL':
            assert self.domain.is_sub_dict(values, content), \
                "按项目过滤域名列表比对数据失败，返回数据{}，期望数据{}".format(content, values)
        else:
            assert content == {}, \
                "按项目过滤域名列表存在不同项目的数据，比对数据失败，返回数据{}，期望数据{}".format(content, values)
