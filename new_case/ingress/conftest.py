import base64
import pytest
from common.log import logger
from common.settings import RESOURCE_PREFIX, K8S_NAMESPACE, PROJECT_NAME, REGION_NAME, CASE_TYPE
from new_case.domain.domain import Domain
from new_case.secret.secret import Secret
from new_case.service.service import Service

l0_data_list = [
    {
        'ingress_name': "{}-ares-acp-ingress-http".format(RESOURCE_PREFIX),
        'host': "{}.ares.acp.ingress.domain".format(RESOURCE_PREFIX),
        'service_name': "{}-ares-acp-ingress-service".format(RESOURCE_PREFIX),
        'ruledata': '一组数据'
    }
]
l0_casemame = ['http类型一组规则和一个域名']
data_list = [
    {
        'ingress_name': "{}-ares-acp-ingress-https".format(RESOURCE_PREFIX),
        'host': "{}.ares.acp.ingress.domain".format(RESOURCE_PREFIX),
        'service_name': "{}-ares-acp-ingress-service".format(RESOURCE_PREFIX),
        'secret_name': "{}-ares-acp-ingress-secret".format(RESOURCE_PREFIX),
        'ruledata': '一组数据'
    },
    {
        'ingress_name': "{}-ares-acp-ingress-norule".format(RESOURCE_PREFIX),
        'ruledata': '无数据'
    },
    {
        'ingress_name': "{}-ares-acp-ingress-manyrule".format(RESOURCE_PREFIX),
        'host': "{}.ares.acp.ingress.domain".format(RESOURCE_PREFIX),
        'service_name': "{}-ares-acp-ingress-service".format(RESOURCE_PREFIX),
        'host2': "{}.ares.acp.ingress.domain".format(RESOURCE_PREFIX),
        'service_name2': "{}-ares-acp-ingress-service".format(RESOURCE_PREFIX),
        'ruledata': '多组数据',
    },
    {
        'ingress_name': "{}-ares-acp-ingress-onlyservice".format(RESOURCE_PREFIX),
        'service_name': "{}-ares-acp-ingress-service".format(RESOURCE_PREFIX),
        'ruledata': '一组数据',
    },
    {
        'ingress_name': "{}-ares-acp-ingress-onlyhost".format(RESOURCE_PREFIX),
        'host': "{}.ares.acp.ingress.domain".format(RESOURCE_PREFIX),
        'ruledata': '一组数据',
    },
]
l1_create_casename = ["https类型一组规则和一个域名", "无数据", "http类型多组规则", "http类型只有规则", "http类型只有域名"]
update_data_list = [
    {
        'ingress_name': "{}-ares-acp-ingress-https".format(RESOURCE_PREFIX),
        'ruledata': '无数据'
    },
    {
        'ingress_name': "{}-ares-acp-ingress-norule".format(RESOURCE_PREFIX),
        'host': "{}.ares.acp.ingress.domain".format(RESOURCE_PREFIX),
        'service_name': "{}-ares-acp-ingress-service".format(RESOURCE_PREFIX),
        'secret_name': "{}-ares-acp-ingress-secret".format(RESOURCE_PREFIX),
        'ruledata': '一组数据'
    },
    {
        'ingress_name': "{}-ares-acp-ingress-manyrule".format(RESOURCE_PREFIX),
        'service_name': "{}-ares-acp-ingress-service".format(RESOURCE_PREFIX),
        'ruledata': '一组数据',
    },
    {
        'ingress_name': "{}-ares-acp-ingress-onlyservice".format(RESOURCE_PREFIX),
        'host': "{}.ares.acp.ingress.domain".format(RESOURCE_PREFIX),
        'service_name': "{}-ares-acp-ingress-service".format(RESOURCE_PREFIX),
        'host2': "{}.ares.acp.ingress.domain".format(RESOURCE_PREFIX),
        'service_name2': "{}-ares-acp-ingress-service".format(RESOURCE_PREFIX),
        'ruledata': '多组数据',
    },
    {
        'ingress_name': "{}-ares-acp-ingress-onlyhost".format(RESOURCE_PREFIX),
        'host': "{}.ares.acp.ingress.domain".format(RESOURCE_PREFIX),
        'service_name': "{}-ares-acp-ingress-service".format(RESOURCE_PREFIX),
        'ruledata': '一组数据',
    },
]
l1_update_casename = ["https类型一组规则和一个域名更新到无数据", "无数据更新到https类型一组规则和一个域名", "http类型多组规则更新到只有域名",
                      "http类型只有规则更新到http类型多组规则更新", "http类型只有域名http类型一组规则和一个域名"]
l2_data_list = [
    {
        'ingress_name': "",
        'host': "{}.ares.acp.ingress.domain".format(RESOURCE_PREFIX),
        'service_name': "{}-ares-acp-ingress-service".format(RESOURCE_PREFIX),
        'secret_name': "{}-ares-acp-ingress-secret".format(RESOURCE_PREFIX),
        'ruledata': '一组数据',
        'message': r"Ingress.extensions \"\" is invalid: metadata.name: Required value: name or generateName is required",
        'reason': 'Invalid',
        'reason2': "FieldValueRequired",
        'message2': "Required value: name or generateName is required",
        'field': "metadata.name",
        'code': "422",
    },
    {
        'ingress_name': "abcdefghijklmnopqrstuvwxyz1234567890123",
        'host': "{}.ares.acp.ingress.domain".format(RESOURCE_PREFIX),
        'service_name': "{}-ares-acp-ingress-service".format(RESOURCE_PREFIX),
        'secret_name': "{}-ares-acp-ingress-secret".format(RESOURCE_PREFIX),
        'ruledata': '一组数据',
    },
    {
        'ingress_name': "abcdefghijklmnopqrstuvwxyz12345678901234",
        'host': "{}.ares.acp.ingress.domain".format(RESOURCE_PREFIX),
        'service_name': "{}-ares-acp-ingress-service".format(RESOURCE_PREFIX),
        'secret_name': "{}-ares-acp-ingress-secret".format(RESOURCE_PREFIX),
        'ruledata': '一组数据',
        'message': r"Ingress.extensions \"\" is invalid: metadata.name: Required value: name or generateName is required",
        'reason': 'Invalid',
        'reason2': "FieldValueRequired",
        'message2': r"Ingress.extensions \"abcdefghijklmnopqrstuvwxyz12345678901234\" "
                    r"is invalid: metadata.name: Invalid value: \"abcdefghijklmnopqrstuvwxyz12345678901234\": "
                    r"must be no more than 63 characters",
        'field': "metadata.name",
        'code': "442",
    },
    {
        'ingress_name': "{}-ares-acp-ingress-https".format(RESOURCE_PREFIX),
        'host': "{}.ares.acp.ingress.domain".format(RESOURCE_PREFIX),
        'service_name': "{}-ares-acp-ingress-service".format(RESOURCE_PREFIX),
        'secret_name': "{}-ares-acp-ingress-secret".format(RESOURCE_PREFIX),
        'ruledata': '一组数据',
        'namespace': "aaaa",
        'message': "the namespace of the provided object does not match the namespace sent on the request",
        'reason': "BadRequest",
        'code': "400",
        'detail_hidden': "true",
    },
    {
        'ingress_name': "{}-ares-acp-ingress-https".format(RESOURCE_PREFIX),
        'host': "{}.ares.acp.ingress.domain".format(RESOURCE_PREFIX),
        'service_name_1': "test",
        "service_name_2": "",
        'secret_name': "{}-ares-acp-ingress-secret".format(RESOURCE_PREFIX),
        'ruledata': '一组数据',
        'message': r"Ingress.extensions \"{}-ares-acp-ingress-https\" is invalid: "
                   r"spec.rules[0].http.backend.serviceName: Required value".format(RESOURCE_PREFIX),
        'reason': 'Invalid',
        'reason2': "FieldValueRequired",
        'message2': r"Required value",
        'field': "spec.rules[0].http.backend.serviceName",
        'code': "422",

    },
    {
        'ingress_name': "{}-ares-acp-ingress-https".format(RESOURCE_PREFIX),
        'host': "{}.ares.acp.ingress.domain".format(RESOURCE_PREFIX),
        'service_name': "{}-ares-acp-ingress-service".format(RESOURCE_PREFIX),
        'secret_name': "{}-ares-acp-ingress-secret".format(RESOURCE_PREFIX),
        'ruledata': '一组数据',
        'service_port': '65536',
    },
    {
        'ingress_name': "duplication",
        'host': "{}.ares.acp.ingress.domain".format(RESOURCE_PREFIX),
        'service_name': "{}-ares-acp-ingress-service".format(RESOURCE_PREFIX),
        'secret_name': "{}-ares-acp-ingress-secret".format(RESOURCE_PREFIX),
        'ruledata': '一组数据',
        'message': r"ingresses.extensions \"duplication\" already exists",
        'reason': 'AlreadyExists',
        'reason2': "FieldValueInvalid",
        'field': "metadata.name",
        'code': "409",
        'kind2': "ingresses",
        'name': "duplication"
    },
    {
        'ingress_name': "A",
        'host': "{}.ares.acp.ingress.domain".format(RESOURCE_PREFIX),
        'service_name': "{}-ares-acp-ingress-service".format(RESOURCE_PREFIX),
        'secret_name': "{}-ares-acp-ingress-secret".format(RESOURCE_PREFIX),
        'ruledata': '一组数据',
        'message': r"Ingress.extensions \"A\" is invalid: metadata.name: Invalid value: \"A\": "
                   r"a DNS-1123 subdomain must consist of lower case alphanumeric characters, '-' or '.', "
                   r"and must start and end with an alphanumeric character (e.g. 'example.com', "
                   r"regex used for validation is '[a-z0-9]([-a-z0-9]*[a-z0-9])?(\\.[a-z0-9]([-a-z0-9]*[a-z0-9])?)*')",
        'reason': 'Invalid',
        'reason2': "FieldValueInvalid",
        'message2': r"Invalid value: \"A\": a DNS-1123 subdomain must consist of lower case alphanumeric characters,"
                    r" '-' or '.', and must start and end with an alphanumeric character (e.g. 'example.com',"
                    r" regex used for validation is"
                    r" '[a-z0-9]([-a-z0-9]*[a-z0-9])?(\\.[a-z0-9]([-a-z0-9]*[a-z0-9])?)*')",
        'field': "metadata.name",
        'code': "422",
    },
    {
        'ingress_name': "{}-ares-acp-ingress-https".format(RESOURCE_PREFIX),
        'host': "{}.ares.acp.ingress.domain".format(RESOURCE_PREFIX),
        'service_name': "{}-ares-acp-ingress-service".format(RESOURCE_PREFIX),
        'secret_name': "{}-ares-acp-ingress-secret".format(RESOURCE_PREFIX),
        'ruledata': '一组数据',
        'path': 'aaaa',
        'message': r"Ingress.extensions \"{}-ares-acp-ingress-https\" is invalid: "
                   r"spec.rules[0].http.paths[0].path: Invalid value: \"aaaa\": "
                   r"must be an absolute path".format(RESOURCE_PREFIX),
        'reason': 'Invalid',
        'reason2': "FieldValueInvalid",
        'message2': r"Invalid value: \"aaaa\": must be an absolute path",
        'field': "spec.rules[0].http.paths[0].path",
        'code': "422",

    },
    {
        'ingress_name': "{}-ares-acp-ingress-https".format(RESOURCE_PREFIX),
        'service_name': "{}-ares-acp-ingress-service".format(RESOURCE_PREFIX),
        'secret_name': "{}-ares-acp-ingress-secret".format(RESOURCE_PREFIX),
        'ruledata': '一组数据',
        'host': r"\%.xq3",
        'message': r"Ingress.extensions \"{}-ares-acp-ingress-https\" is invalid: [spec.rules[0].host: Invalid value: \"\\\\%.xq3\": "
                   r"a DNS-1123 subdomain must consist of lower case alphanumeric characters, '-' or '.', and must start and end with an "
                   r"alphanumeric character (e.g. 'example.com', regex used for validation is "
                   r"'[a-z0-9]([-a-z0-9]*[a-z0-9])?(\\.[a-z0-9]([-a-z0-9]*[a-z0-9])?)*'), spec.tls[0].hosts: Invalid value: \"\\\\%.xq3\": "
                   r"a DNS-1123 subdomain must consist of lower case alphanumeric characters, '-' or '.', and must start and end with an alphanumeric "
                   r"character (e.g. 'example.com', regex used for validation is"
                   r" '[a-z0-9]([-a-z0-9]*[a-z0-9])?(\\.[a-z0-9]([-a-z0-9]*[a-z0-9])?)*')]".format(RESOURCE_PREFIX),
        'reason': 'Invalid',
        'reason2': "FieldValueInvalid",
        'message2': r"Invalid value: \"\\\\%.xq3\": a DNS-1123 subdomain must consist of lower case alphanumeric characters, '-' or '.', "
                    r"and must start and end with an alphanumeric character (e.g. 'example.com', regex used for validation is"
                    r" '[a-z0-9]([-a-z0-9]*[a-z0-9])?(\\.[a-z0-9]([-a-z0-9]*[a-z0-9])?)*')",
        'causes': "ddd",
        'field': "spec.rules[0].host",
        'code': "422",
        'name': "{}-ares-acp-ingress-https".format(RESOURCE_PREFIX),

    },
]


@pytest.fixture(scope="session", autouse=True)
def Prepare_template():
    domain_client = Domain()
    secret_client = Secret()
    service_client = Service()
    ns_name = K8S_NAMESPACE
    logger.info(RESOURCE_PREFIX)
    domain_name = "{}.ares.acp.ingress.domain".format(RESOURCE_PREFIX)
    secret_name = "{}-ares-acp-ingress-secret".format(RESOURCE_PREFIX)
    service_name = "{}-ares-acp-ingress-service".format(RESOURCE_PREFIX)
    data = {"timestamp": domain_name,
            "name": domain_name,
            "kind": "full",
            "project_name": PROJECT_NAME,
            "region_name": REGION_NAME}
    domain_client.create_domain("./test_data/domain/create_domain.jinja2", data)
    data = {
        "secret_name": secret_name,
        "secret_type": "kubernetes.io/tls",
        "tls_crt": str(base64.b64encode("tlscrt".encode('utf-8')), 'utf8'),
        "tls_key": str(base64.b64encode("tlskey".encode('utf-8')), 'utf8')
    }
    secret_client.create_secret('./test_data/secret/create_secret.jinja2', data=data)
    data = {
        'service_name': service_name,
        'type': 'ClusterIP',
        'sessionAffinity': 'None',
        'portdata': '一组数据',
        'namespace': ns_name
    }
    service_client.create_service(ns_name, './test_data/service/service.jinja2', data)
    prepare_data = {
        "domain_name": domain_name,
        "secret_name": secret_name,
        "service_name": service_name
    }
    yield prepare_data
    if CASE_TYPE not in ("prepare", "prepare"):
        domain_client.delete_domain(domain_name)
        secret_client.delete_secret(secret_name, ns_name)
        service_client.delete_service(ns_name, service_name)
