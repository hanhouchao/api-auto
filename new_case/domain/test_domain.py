import pytest
from common.settings import RERUN_TIMES, REGION_NAME, RESOURCE_PREFIX, CASE_TYPE, PROJECT_NAME
from new_case.domain.domain import Domain


@pytest.mark.BAT
@pytest.mark.acp_containerplatform
@pytest.mark.flaky(reruns=RERUN_TIMES, reruns_delay=3)
class TestDomainSuite(object):
    def setup_class(self):
        self.domain = Domain()
        self.extensive_real_name = '{}.ares.extensive.domain'.format(RESOURCE_PREFIX)
        self.extensive_domain_name = self.extensive_real_name.replace('*', 'random')
        self.full_domain_name = '{}.ares.full.domain'.format(RESOURCE_PREFIX)
        self.cluster_name = REGION_NAME
        self.project_name = PROJECT_NAME

    def teardown_class(self):
        if CASE_TYPE not in ("prepare", "upgrade", "delete"):
            self.domain.delete_domain(self.extensive_domain_name)
            self.domain.delete_domain(self.full_domain_name)

    @pytest.mark.prepare
    def 测试域名之泛域名增加无集群无项目(self):
        # 创建前删除下资源
        self.domain.delete_domain(self.extensive_domain_name)

        # create domain
        createdomain_result = self.domain.create_domain("./test_data/domain/create_domain.jinja2",
                                                        {"timestamp": self.extensive_domain_name,
                                                         "name": self.extensive_real_name,
                                                         "kind": "extensive", "project_name": "",
                                                         "region_name": ""})
        assert createdomain_result.status_code == 201, "创建泛域名失败:{}".format(createdomain_result.text)

        value = self.domain.generate_jinja_data("verify_data/domain/create_response.jinja2",
                                                {"timestamp": self.extensive_domain_name,
                                                 "name": self.extensive_real_name,
                                                 "kind": "extensive", "project_name": "",
                                                 "region_name": ""})
        assert self.domain.is_sub_dict(value, createdomain_result.json()), \
            "创建泛域名比对数据失败，返回数据:{},期望数据:{}".format(createdomain_result.json(), value)

    @pytest.mark.prepare
    def 测试域名之全域名增加有集群无项目(self):
        # 创建前删除下资源
        self.domain.delete_domain(self.full_domain_name)

        # create domain
        createdomain_result = self.domain.create_domain("./test_data/domain/create_domain.jinja2",
                                                        {"timestamp": self.full_domain_name,
                                                         "name": self.full_domain_name,
                                                         "kind": "full", "project_name": "",
                                                         "region_name": self.cluster_name})
        assert createdomain_result.status_code == 201, "创建全域名失败:{}".format(createdomain_result.text)

        value = self.domain.generate_jinja_data("verify_data/domain/create_response.jinja2",
                                                {"timestamp": self.full_domain_name,
                                                 "name": self.full_domain_name,
                                                 "kind": "full", "project_name": "",
                                                 "region_name": self.cluster_name})
        assert self.domain.is_sub_dict(value, createdomain_result.json()), \
            "创建全域名比对数据失败，返回数据:{},期望数据:{}".format(createdomain_result.json(), value)

    @pytest.mark.upgrade
    def 测试域名之泛域名列表(self):
        # list domain
        list_result = self.domain.list_domain(limits=1000)
        assert list_result.status_code == 200, list_result.text
        # 比对泛域名
        content = self.domain.get_k8s_resource_data(list_result.json(), self.extensive_domain_name, list_key="items")
        data = {"region_name": "", "domain_real_name": self.extensive_real_name,
                "domain_name": self.extensive_domain_name, "type": "extensive"}
        value = self.domain.generate_jinja_data("verify_data/domain/list_domain.jinja2", data)
        assert self.domain.is_sub_dict(value, content), "获取泛域名列表比对数据失败，返回数据:{},期望数据:{}".format(content, value)

        # 比对全域名
        content = self.domain.get_k8s_resource_data(list_result.json(), self.full_domain_name, list_key="items")
        data = {"region_name": REGION_NAME, "domain_real_name": self.full_domain_name,
                "domain_name": self.full_domain_name, "type": "full"}
        value = self.domain.generate_jinja_data("verify_data/domain/list_domain.jinja2", data)
        assert self.domain.is_sub_dict(value, content), "获取全域名列表比对数据失败，返回数据:{},期望数据:{}".format(content, value)

    @pytest.mark.upgrade
    def 测试域名之泛域名更新添加集群(self):
        # update domain
        update_result = self.domain.update_domain(self.extensive_domain_name, "./test_data/domain/patch_domain.jinja2",
                                                  {"region_name": self.cluster_name, "project_name": self.project_name})
        assert update_result.status_code == 200, "更新泛域名出错:{}".format(update_result.text)

        value = self.domain.generate_jinja_data("verify_data/domain/list_domain.jinja2",
                                                {"region_name": REGION_NAME, "domain_real_name": self.extensive_real_name,
                                                 "domain_name": self.extensive_domain_name, "type": "extensive"})
        assert self.domain.is_sub_dict(value, update_result.json()), \
            "更新泛域名比对数据失败，返回数据:{},期望数据:{}".format(update_result.json(), value)

    @pytest.mark.upgrade
    def 测试域名之全域名更新去除集群(self):
        # update domain
        update_result = self.domain.update_domain(self.full_domain_name, "./test_data/domain/patch_domain.jinja2",
                                                  {"region_name": '', "project_name": self.project_name})
        assert update_result.status_code == 200, "更新全域名出错:{}".format(update_result.text)

        value = self.domain.generate_jinja_data("verify_data/domain/list_domain.jinja2",
                                                {"region_name": "", "domain_real_name": self.full_domain_name,
                                                 "domain_name": self.full_domain_name, "type": "full"})
        assert self.domain.is_sub_dict(value, update_result.json()), \
            "更新全域名比对数据失败，返回数据:{},期望数据:{}".format(update_result.json(), value)

    @pytest.mark.upgrade
    def 测试域名之泛域名详情(self):
        # detail domain
        detail_result = self.domain.detail_domain(self.extensive_domain_name)
        assert detail_result.status_code == 200, detail_result.text

        value = self.domain.generate_jinja_data("verify_data/domain/list_domain.jinja2",
                                                {"region_name": REGION_NAME, "domain_real_name": self.extensive_real_name,
                                                 "domain_name": self.extensive_domain_name, "type": "extensive"})
        assert self.domain.is_sub_dict(value, detail_result.json()), \
            "更新泛域名比对数据失败，返回数据:{},期望数据:{}".format(detail_result.json(), value)

    @pytest.mark.upgrade
    def 测试域名之全域名详情(self):
        # detail domain
        detail_result = self.domain.detail_domain(self.full_domain_name)
        assert detail_result.status_code == 200, detail_result.text

        value = self.domain.generate_jinja_data("verify_data/domain/list_domain.jinja2",
                                                {"region_name": "", "domain_real_name": self.full_domain_name,
                                                 "domain_name": self.full_domain_name, "type": "full"})
        assert self.domain.is_sub_dict(value, detail_result.json()), \
            "更新全域名比对数据失败，返回数据:{},期望数据:{}".format(detail_result.json(), value)

    @pytest.mark.delete
    def 测试域名之泛域名删除(self):
        # delete domain
        delete_result = self.domain.delete_domain(self.extensive_domain_name)
        assert delete_result.status_code == 200, "删除泛域名失败：{}".format(delete_result.text)
        assert self.domain.check_exists(self.domain.get_common_domain_url(self.extensive_domain_name), 404)

    @pytest.mark.delete
    def 测试域名之全域名删除(self):
        # delete domain
        delete_result = self.domain.delete_domain(self.full_domain_name)
        assert delete_result.status_code == 200, "删除全域名失败：{}".format(delete_result.text)
        assert self.domain.check_exists(self.domain.get_common_domain_url(self.full_domain_name), 404)
