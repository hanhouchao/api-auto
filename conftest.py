# coding=utf-8
import pytest
from common import settings
from new_case.namespace.namespace import Namespace
from new_case.project.project import Project


@pytest.fixture(scope="session", autouse=True)
def prepare_and_clear():
    # 创建测试前准备的数据
    project = Project()
    data = {
        "project_name": settings.PROJECT_NAME,
        "regions": [settings.REGION_NAME],
        "display_name": settings.PROJECT_NAME,
        "description": "e2e test project",
    }
    create_project_result = project.create_project("./test_data/project/create_project.jinja2", data)
    assert create_project_result.status_code in (201, 409), "创建项目失败"
    namespace = Namespace()
    ns_data = {
        "namespace_name": settings.K8S_NAMESPACE,
        "display_name": settings.K8S_NAMESPACE,
        "cluster": settings.REGION_NAME,
        "project": settings.PROJECT_NAME,
        "ResourceQuota": "False",
        "morelabel": "False"
    }
    create_ns_result = namespace.create_namespace('./test_data/namespace/create_namespace.jinja2', ns_data,
                                                  region_name=settings.REGION_NAME)
    assert create_ns_result.status_code in (200, 409, 500), "创建新命名空间失败 {}".format(create_ns_result.text)
    yield
