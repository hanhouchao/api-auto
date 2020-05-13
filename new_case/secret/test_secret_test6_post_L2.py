import pytest
import base64
from new_case.secret.secret import Secret
from common import settings


@pytest.mark.Low
@pytest.mark.acp_containerplatform
@pytest.mark.flaky(reruns=settings.RERUN_TIMES, reruns_delay=3)
class TestPostSecret(object):
    # 正向测试用例
    l2_data_list_positive = [
        {
            "secret_name": "a123456789012345678901234567890123456789012345678901234567890123",
            "secret_type": "Opaque",
            "description": "保密字典名称为64个英文字符",
            "opaque_key": "opaque_key",
            "opaque_value": str(base64.b64encode("opaque_value".encode('utf-8')), 'utf8'),
            "status_code": 201
        },
        {
            "secret_name": "{}-ares-opaque-secret-key-253chars".format(settings.RESOURCE_PREFIX),
            "secret_type": "Opaque",
            "description": "创建Opaque保密字典key带有253个字符",
            "opaque_key": "opaque_key",
            "opaque_value": str(base64.b64encode("opaque_value".encode('utf-8')), 'utf8'),
            "status_code": 201
        },
        {
            "secret_name": "{}-ares-opaque-secret-data-null".format(settings.RESOURCE_PREFIX),
            "secret_type": "Opaque",
            "description": "创建Opaque保密字典data字段为空",
            "opaque_key": "opaque_key",
            "opaque_value": str(base64.b64encode("opaque_value".encode('utf-8')), 'utf8'),
            "status_code": 201
        }
    ]
    l2_casename_positive = ["创建保密字典名称为64个英文字符",
                            "创建Opaque保密字典key带有253个字符",
                            "创建Opaque保密字典data字段为空"]
    # 逆向测试用例
    l2_data_list_negative = [
        {
            "secret_name": "",
            "secret_type": "Opaque",
            "description": "创建Opaque保密字典名称为空",
            "opaque_key": "opaque_key",
            "opaque_value": str(base64.b64encode("opaque_value".encode('utf-8')), 'utf8'),
            "message": r"Secret \"\" is invalid: metadata.name: Required value: name or generateName is required",
            "reason": "Invalid",
            "details": True,
            "causes": True,
            "reason_2": "FieldValueRequired",
            "message_2": "Required value: name or generateName is required",
            "field": "metadata.name",
            "status_code": 422
        },
        {
            "secret_name": "a1234567890123456789012345678901234567890123456789012345678"
                           "901234567890123456789012345678901234567890123456789012345678"
                           "901234567890123456789012345678901234567890123456789012345678"
                           "901234567890123456789012345678901234567890123456789012345678"
                           "901234567890123",
            "secret_type": "Opaque",
            "description": "创建Opaque保密字典名称为254个英文字符",
            "opaque_key": "opaque_key",
            "opaque_value": str(base64.b64encode("opaque_value".encode('utf-8')), 'utf8'),
            "message": r"Secret "
                       r"\"a1234567890123456789012345678901234567890123456789012345678901234"
                       r"5678901234567890123456789012345678901234567890123456789012345678901"
                       r"2345678901234567890123456789012345678901234567890123456789012345678901"
                       r"2345678901234567890123456789012345678901234567890123\" is invalid: "
                       r"metadata.name: Invalid value: \"a12345678901234567890123456789012345"
                       r"6789012345678901234567890123456789012345678901234567890123456789012345"
                       r"67890123456789012345678901234567890123456789012345678901234567890123456"
                       r"789012345678901234567890123456789012345678901234567890123456789012345678"
                       r"90123\": must be no more than 253 characters",
            "reason": "Invalid",
            "details": True,
            "causes": True,
            "reason_2": "FieldValueInvalid",
            "message_2": r"Invalid value: \"a123456789012345678901234567890123456789012345678901"
                         r"234567890123456789012345678901234567890123456789012345678901234567890"
                         r"1234567890123456789012345678901234567890123456789012345678901234567890"
                         r"123456789012345678901234567890123456789012345678901234567890123\": must "
                         r"be no more than 253 characters",
            "field": "metadata.name",
            "status_code": 422
        },
        {
            "secret_name": "{}-ares-opaque-secret".format(settings.RESOURCE_PREFIX),
            "secret_type": "Opaque",
            "description": "创建Opaque保密字典与已存在的同名",
            "opaque_key": "opaque_key",
            "opaque_value": str(base64.b64encode("opaque_value".encode('utf-8')), 'utf8'),
            "message": r"secrets \"{}-ares-opaque-secret\" already exists".format(settings.RESOURCE_PREFIX),
            "reason": "AlreadyExists",
            "details": True,
            "kind_2": "secrets",
            "status_code": 409,
            "duplicate_name": True
        },
        {
            "secret_name": "A".format(settings.RESOURCE_PREFIX),
            "secret_type": "Opaque",
            "description": "创建Opaque保密字典名称包含非法字符",
            "opaque_key": "opaque_key",
            "opaque_value": str(base64.b64encode("opaque_value".encode('utf-8')), 'utf8'),
            "message": r"Secret \"A\" is invalid: metadata.name: Invalid value: \"A\": a DNS-1123 subdomain must "
                       r"consist of lower case alphanumeric characters, '-' or '.', and must start and end with an "
                       r"alphanumeric character (e.g. 'example.com', regex used for validation is '[a-z0-9](["
                       r"-a-z0-9]*[a-z0-9])?(\\.[a-z0-9]([-a-z0-9]*[a-z0-9])?)*')",
            "reason": "Invalid",
            "details": True,
            "causes": True,
            "message_2": r"Invalid value: \"A\": a DNS-1123 subdomain must consist of lower case alphanumeric "
                         r"characters, '-' or '.', and must start and end with an alphanumeric character (e.g. "
                         r"'example.com', regex used for validation is '[a-z0-9]([-a-z0-9]*[a-z0-9])?(\\.[a-z0-9](["
                         r"-a-z0-9]*[a-z0-9])?)*')",
            "reason_2": "FieldValueInvalid",
            "field": "metadata.name",
            "status_code": 422,
        },
        {
            "secret_name": "{}-ares-opaque-secret-key-null".format(settings.RESOURCE_PREFIX),
            "secret_type": "Opaque",
            "description": "创建Opaque保密字典key为空",
            "opaque_key": "null",
            "opaque_value": str(base64.b64encode("opaque_value".encode('utf-8')), 'utf8'),
            "message": r"Secret \"{}-ares-opaque-secret-key-null\" is invalid: data[]: Invalid value: \"\": "
                       r"a valid config key must consist of alphanumeric characters, '-', '_' or '.' (e.g. "
                       r"'key.name',  or 'KEY_NAME',  or 'key-name', regex used for validation is '"
                       r"[-._a-zA-Z0-9]+')".format(settings.RESOURCE_PREFIX),
            "reason": "Invalid",
            "details": True,
            "causes": True,
            "message_2": r"Invalid value: \"\": a valid config key must consist of alphanumeric characters,"
                         r" '-', '_' or '.' (e.g. 'key.name',  or 'KEY_NAME',  or 'key-name', regex used for "
                         r"validation is '[-._a-zA-Z0-9]+')",
            "reason_2": "FieldValueInvalid",
            "field": "data[]",
            "status_code": 422,
        },
        {
            "secret_name": "{}-ares-tls-secret-nokey".format(settings.RESOURCE_PREFIX),
            "secret_type": "kubernetes.io/tls",
            "description": "创建TLS保密字典仅有证书没有私钥",
            "tls_crt": str(base64.b64encode("tlscrt".encode('utf-8')), 'utf8'),
            "tls_key": "null",
            "message": r"Secret \"{}-ares-tls-secret-nokey\" is invalid: data[tls.key]: "
                       r"Required value".format(settings.RESOURCE_PREFIX),
            "reason": "Invalid",
            "details": True,
            "causes": True,
            "reason_2": "FieldValueRequired",
            "message_2": "Required value",
            "field": r"data[tls.key]",
            "status_code": 422,
        },
        {
            "secret_name": "{}-ares-tls-secret-nocrt".format(settings.RESOURCE_PREFIX),
            "secret_type": "kubernetes.io/tls",
            "description": "创建TLS保密字典仅有私钥没有证书",
            "tls_crt": "null",
            "tls_key": str(base64.b64encode("tlskey".encode('utf-8')), 'utf8'),
            "message": r"Secret \"{}-ares-tls-secret-nocrt\" is invalid: data[tls.crt]: "
                       r"Required value".format(settings.RESOURCE_PREFIX),
            "reason": "Invalid",
            "details": True,
            "causes": True,
            "reason_2": "FieldValueRequired",
            "message_2": "Required value",
            "field": r"data[tls.crt]",
            "status_code": 422,
        },
        {
            "secret_name": "{}-ares-ssh-secret-invalid-private".format(settings.RESOURCE_PREFIX),
            "secret_type": "kubernetes.io/ssh-auth",
            "description": "创建SSH认证保密字典使用非法的ssh私钥",
            "ssh_privatevalue": "hello",
            "message": r"Secret in version \"v1\" cannot be handled as a Secret: v1.Secret.Data: decode base64: "
                       r"illegal base64 data at input byte 4, error found in #10 byte of ...|\": \"hello\"}}|..., "
                       r"bigger context ...|s.io/ssh-auth\", \"data\": {\"ssh-privatekey\": \"hello\"}}|...",
            "reason": "BadRequest",
            "status_code": 400
        },
        {
            "secret_name": "{}-ares-ssh-secret-nokey".format(settings.RESOURCE_PREFIX),
            "secret_type": "kubernetes.io/ssh-auth",
            "description": "创建SSH认证保密字典ssh私钥为空",
            "ssh_privatevalue": "",
            "message": r"Secret \"{}-ares-ssh-secret-nokey\" is invalid: data[%s][ssh-privatekey]: "
                       r"Required value".format(settings.RESOURCE_PREFIX),
            "reason": "Invalid",
            "details": True,
            "causes": True,
            "reason_2": "FieldValueRequired",
            "message_2": "Required value",
            "field": r"data[%s][ssh-privatekey]",
            "status_code": 422
        },
        {
            "secret_name": "{}-ares-baseauth-secret-base".format(settings.RESOURCE_PREFIX),
            "secret_type": "kubernetes.io/basic-auth",
            "description": "创建基本认证data字段为空",
            "ssh_privatevalue": "",
            "message": r"Secret \"{}-ares-baseauth-secret-base\" is invalid: [data[%s][username]"
                       r": Required value, data[%s][password]: Required value]".format(settings.RESOURCE_PREFIX),
            "data": "null",
            "reason": "Invalid",
            "details": True,
            "causes": True,
            "reason_2": "FieldValueRequired",
            "message_2": "Required value",
            "field": r"data[%s][username]",
            "reason_3": "FieldValueRequired",
            "message_3": "Required value",
            "field_3": r"data[%s][password]",
            "status_code": 422
        },
        {
            "secret_name": "{}-ares-docker-secret".format(settings.RESOURCE_PREFIX),
            "secret_type": "kubernetes.io/dockerconfigjson",
            "description": "创建镜像服务dockerconfigjson为空",
            "dockerconfigjson": "null",
            "message": r"Secret \"{}-ares-docker-secret\" is invalid: data[.dockerconfigjson]: Invalid value: "
                       r"\"<secret contents redacted>\": unexpected end of JSON input".format(
                settings.RESOURCE_PREFIX),
            "reason": "Invalid",
            "details": True,
            "causes": True,
            "reason_2": "FieldValueInvalid",
            "message_2": r"Invalid value: \"<secret contents redacted>\": unexpected end of JSON input",
            "field": r"data[.dockerconfigjson]",
            "status_code": 422
        },
    ]
    l2_casename_negative = ["创建Opaque保密字典名称为空",
                            "创建Opaque保密字典名称为254个英文字符",
                            "创建Opaque保密字典与已存在的同名",
                            "创建Opaque保密字典名称包含非法字符",
                            "创建Opaque保密字典key为空",
                            "创建TLS保密字典仅有证书没有私钥",
                            "创建TLS保密字典仅有私钥没有证书",
                            "创建SSH认证保密字典使用非法的ssh私钥",
                            "创建SSH认证保密字典ssh私钥为空",
                            "创建基本认证data字段为空",
                            "创建镜像服务dockerconfigjson为空"
                            ]
    l2_data_list = l2_data_list_positive + l2_data_list_negative
    l2_casename = l2_casename_positive + l2_casename_negative

    def setup_class(self):
        self.secret_tool = Secret()
        self.teardown_class(self)

    def teardown_class(self):
        for item in self.l2_data_list:
            if item["secret_name"]:
                self.secret_tool.delete_secret(item['secret_name'])

    @pytest.mark.parametrize("data", l2_data_list, ids=l2_casename)
    def 测试创建各种保密字典L2(self, data):
        data.update({"K8S_NAMESPACE": settings.K8S_NAMESPACE})
        if data.get("duplicate_name", ""):
            self.secret_tool.create_secret("./test_data/secret/create_secret.jinja2", data=data)
        ret = self.secret_tool.create_secret("./test_data/secret/create_secret.jinja2", data=data)
        expected_code = data['status_code']
        assert ret.status_code == expected_code, "创建{}类型保密字典失败:{}".format(data['secret_type'], ret.text)
        verify_template_name = 'create_response.jinja2' if expected_code < 300 else 'create_response_failure.jinja2'
        verify_template_path = './verify_data/secret/{}'.format(verify_template_name)
        value = self.secret_tool.generate_jinja_data(verify_template_path, data)
        assert self.secret_tool.is_sub_dict(value, ret.json()), \
            "创建保密字典比对数据失败，返回数据:{},期望数据:{}".format(ret.json(), value)
