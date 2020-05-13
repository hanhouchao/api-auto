from common.settings import RESOURCE_PREFIX

l0_data_list = {
    'service_name': "{}-cluster".format(RESOURCE_PREFIX),
    'type': 'ClusterIP',
    'sessionAffinity': 'None',
    'portdata': '一组数据'
}
create_casename_list = ["一组clusterip数据-源地址会话保持", "多组nodeport数据-源地址会话保持",
                        "一组clusterip数据-headless", "一组clusterip数据-headless关闭"]
data_list = [
    {'service_name': "{}-all".format(RESOURCE_PREFIX),
     'type': 'ClusterIP',
     'sessionAffinity': 'ClientIP',
     'portdata': '一组数据',
     'selector': True
     },
    {'service_name': "{}-nodeport".format(RESOURCE_PREFIX),
     'type': 'NodePort',
     'sessionAffinity': 'ClientIP',
     'portdata': '多组数据'
     },
    {'service_name': "{}-headless".format(RESOURCE_PREFIX),
     'type': 'ClusterIP',
     'sessionAffinity': 'None',
     'portdata': '一组数据',
     'ClusterIP': "None"
     },
    {'service_name': "{}-close-headless".format(RESOURCE_PREFIX),
     'type': 'ClusterIP',
     'sessionAffinity': 'None',
     'portdata': '一组数据',
     "ClusterIP": " ",
     'clusterIP': '"None"'
     }
]
wrong_list = {
    'service_name': "{}-noport".format(RESOURCE_PREFIX),
    'type': 'NodePort',
    'sessionAffinity': 'ClientIP'
}

l2_data_list = [
    {'service_name': "{}-only-udp".format(RESOURCE_PREFIX),
     'type': 'ClusterIP',
     'sessionAffinity': 'ClientIP',
     'portdata': '一组数据',
     'protocol_1': 'UDP',
     'p_name_1': 'udp'
     },
    {'service_name': "{}-only-http".format(RESOURCE_PREFIX),
     'type': 'ClusterIP',
     'sessionAffinity': 'ClientIP',
     'portdata': '一组数据',
     'protocol_1': 'TCP',
     'p_name_1': 'http'
     },
    {'service_name': "{}-only-https".format(RESOURCE_PREFIX),
     'type': 'ClusterIP',
     'sessionAffinity': 'ClientIP',
     'portdata': '一组数据',
     'protocol_1': 'TCP',
     'p_name_1': 'https'
     },
    {'service_name': "{}-only-http2".format(RESOURCE_PREFIX),
     'type': 'ClusterIP',
     'sessionAffinity': 'ClientIP',
     'portdata': '一组数据',
     'protocol_1': 'TCP',
     'p_name_1': 'http2'
     },
    {'service_name': "{}-only-grpc".format(RESOURCE_PREFIX),
     'type': 'ClusterIP',
     'sessionAffinity': 'ClientIP',
     'portdata': '一组数据',
     'protocol_1': 'TCP',
     'p_name_1': 'grpc'
     },
    {'service_name': "thirty-onethirty-onethirty-one12",
     'type': 'ClusterIP',
     'sessionAffinity': 'ClientIP',
     'portdata': '一组数据',
     'protocol_1': 'TCP'
     },
    {'service_name': "{}-tcp-udp-combine".format(RESOURCE_PREFIX),
     'type': 'ClusterIP',
     'sessionAffinity': 'ClientIP',
     'portdata': '多组数据',
     'protocol_1': 'TCP',
     'protocol_2': 'UDP',
     'p_name_2': 'udp'
     },
    {'service_name': "{}-port-65535".format(RESOURCE_PREFIX),
     'type': 'ClusterIP',
     'sessionAffinity': 'ClientIP',
     'portdata': '一组数据',
     'protocol_1': 'TCP',
     'port_1': 65535,
     },
    {'service_name': "{}-target-port-65535".format(RESOURCE_PREFIX),
     'type': 'ClusterIP',
     'sessionAffinity': 'ClientIP',
     'portdata': '一组数据',
     'protocol_1': 'UDP',
     'p_name_1': 'udp',
     'targetPort_1': 65535,
     },
    {'service_name': "{}-tcpudp-same-port".format(RESOURCE_PREFIX),
     'type': 'ClusterIP',
     'sessionAffinity': 'ClientIP',
     'portdata': '多组数据',
     'protocol_1': 'TCP',
     'port_1': 53,
     'protocol_2': 'UDP',
     'port_2': 53,
     'p_name_2': 'udp'
     },
    {'service_name': "{}-ares-2tcp-same-targetport".format(RESOURCE_PREFIX),
     'type': 'ClusterIP',
     'sessionAffinity': 'ClientIP',
     'portdata': '多组数据',
     'protocol_1': 'TCP',
     'targetPort_1': 77,
     'protocol_2': 'TCP',
     'targetPort_2': 77
     }
]

l2_create_casename_list = ["创建UDP协议的service",
                           "创建HTTP协议的service",
                           "创建HTTPS协议的service",
                           "创建HTTP2协议的service",
                           "创建gRPC协议的service",
                           "创建带有32个英文字符的名称的service",
                           "创建一个TCP一个UDP型端口",
                           "服务端口为65535",
                           "容器端口为65535",
                           "创建一个service使用不同的协议具有使用相同的服务端口",
                           "创建一个service使用相同的容器端口"]

l2_wrong_list = [
    {
        'service_name': "A",
        'type': 'ClusterIP',
        'sessionAffinity': 'ClientIP',
        'portdata': '一组数据',
        'message': r"Service \"A\" is invalid: metadata.name: Invalid value: \"A\": "
                   r"a DNS-1035 label must consist of lower case alphanumeric characters "
                   r"or '-', start with an alphabetic character, and end with an alphanumeric "
                   r"character (e.g. 'my-name',  or 'abc-123', regex used for validation is "
                   r"'[a-z]([-a-z0-9]*[a-z0-9])?')",
        'reason': 'Invalid',
        'details': True,
        'kind_2': "Service",
        'causes': True,
        'reason_2': "FieldValueInvalid",
        'message_2': r"Invalid value: \"A\": a DNS-1035 label must consist of lower case alphanumeric"
                    r" characters or '-', start with an alphabetic character, and end with an alphanumeric"
                    r" character (e.g. 'my-name',  or 'abc-123', regex used for validation is "
                    r"'[a-z]([-a-z0-9]*[a-z0-9])?')",
        'field': "metadata.name",
        'status_code': 422
    },
    {
        'service_name': "",
        'type': 'ClusterIP',
        'sessionAffinity': 'ClientIP',
        'portdata': '一组数据',
        'message': r"Service \"\" is invalid: metadata.name: Required value: name or generateName is required",
        'reason': 'Invalid',
        'details': True,
        'kind_2': "Service",
        'causes': True,
        'reason_2': "FieldValueRequired",
        'message_2': r"Required value: name or generateName is required",
        'field': "metadata.name",
        'status_code': 422
    },
    {
        'service_name': "{}-name-exist".format(RESOURCE_PREFIX),
        'type': 'ClusterIP',
        'sessionAffinity': 'ClientIP',
        'portdata': '一组数据',
        'message': r"services \"{}-name-exist\" already exists".format(RESOURCE_PREFIX),
        'reason': 'AlreadyExists',
        'details': True,
        'kind_2': "services",
        'status_code': 409,
        'exist_name': True
    },
    {
        'service_name': "{}-port-name-illegal".format(RESOURCE_PREFIX),
        'type': 'ClusterIP',
        'sessionAffinity': 'ClientIP',
        'portdata': '一组数据',
        'protocol_1': 'TCP',
        'p_name_1': 'Ahttp',
        'port_1': '10',
        'targetPort_1': '10',
        'message': r"Service \"{}-port-name-illegal\" is invalid: spec.ports[0].name: Invalid value: "
                   r"\"Ahttp-10-10\": a DNS-1123 label must consist of lower case alphanumeric characters or '-', "
                   r"and must start and end with an alphanumeric character (e.g. 'my-name',  "
                   r"or '123-abc', regex used for validation is "
                   r"'[a-z0-9]([-a-z0-9]*[a-z0-9])?')".format(RESOURCE_PREFIX),
        'reason': 'Invalid',
        'details': True,
        'causes': True,
        'reason_2': "FieldValueInvalid",
        'message_2': r"Invalid value: \"Ahttp-10-10\": a DNS-1123 label must consist of lower case alphanumeric "
                     r"characters or '-', and must start and end with an alphanumeric character (e.g. 'my-name',  "
                     r"or '123-abc', regex used for validation is '[a-z0-9]([-a-z0-9]*[a-z0-9])?')",
        'field': "spec.ports[0].name",
        'status_code': 422
    },
    {
        'service_name': "{}-protocol-invalid".format(RESOURCE_PREFIX),
        'type': 'ClusterIP',
        'sessionAffinity': 'ClientIP',
        'portdata': '一组数据',
        'protocol_1': 'aTCP',
        'message': r"Service \"{}-protocol-invalid\" is invalid: spec.ports[0].protocol: "
                   r"Unsupported value: \"aTCP\": supported values: \"SCTP\", \"TCP\", \"UDP\"".format(RESOURCE_PREFIX),
        'reason': 'Invalid',
        'details': True,
        'causes': True,
        'reason_2': "FieldValueNotSupported",
        'message_2': r"Unsupported value: \"aTCP\": supported values: \"SCTP\", \"TCP\", \"UDP\"",
        'field': "spec.ports[0].protocol",
        'status_code': 422
    },

    {
        'service_name': "{}-port-65536".format(RESOURCE_PREFIX),
        'type': 'ClusterIP',
        'sessionAffinity': 'ClientIP',
        'portdata': '一组数据',
        'p_name_1': 'http',
        'port_1': '65536',
        'message': r"Service \"{}-port-65536\" is invalid: spec.ports[0].port: "
                   r"Invalid value: 65536: must be between 1 and 65535, inclusive".format(RESOURCE_PREFIX),
        'reason': 'Invalid',
        'details': True,
        'causes': True,
        'reason_2': "FieldValueInvalid",
        'message_2': r"Invalid value: 65536: must be between 1 and 65535, inclusive",
        'field': "spec.ports[0].port",
        'status_code': 422
    },
    {
        'service_name': "{}-target-port-0".format(RESOURCE_PREFIX),
        'type': 'ClusterIP',
        'sessionAffinity': 'ClientIP',
        'portdata': '一组数据',
        'p_name_1': 'http',
        'port_1': '0',
        'message': r"Service \"{}-target-port-0\" is invalid: spec.ports[0].port: "
                   r"Invalid value: 0: must be between 1 and 65535, inclusive".format(RESOURCE_PREFIX),
        'reason': 'Invalid',
        'details': True,
        'causes': True,
        'reason_2': "FieldValueInvalid",
        'message_2': r"Invalid value: 0: must be between 1 and 65535, inclusive",
        'field': "spec.ports[0].port",
        'status_code': 422
    },
    {
        'service_name': "{}-target-port-65536".format(RESOURCE_PREFIX),
        'type': 'ClusterIP',
        'sessionAffinity': 'ClientIP',
        'portdata': '一组数据',
        'p_name_1': 'http',
        'targetPort_1': '65536',
        'message': r"Service \"{}-target-port-65536\" is invalid: spec.ports[0].targetPort: "
                   r"Invalid value: 65536: must be between 1 and 65535, inclusive".format(RESOURCE_PREFIX),
        'reason': 'Invalid',
        'details': True,
        'causes': True,
        'reason_2': "FieldValueInvalid",
        'message_2': r"Invalid value: 65536: must be between 1 and 65535, inclusive",
        'field': "spec.ports[0].targetPort",
        'status_code': 422
    },
    {
        'service_name': "{}-port-conflict".format(RESOURCE_PREFIX),
        'type': 'ClusterIP',
        'sessionAffinity': 'ClientIP',
        'protocol_1': 'TCP',
        'portdata': '多组数据',
        'port_1': '1000',
        'protocol_2': 'TCP',
        'port_2': '1000',
        'message': r'Service \"{}-port-conflict\" is invalid: spec.ports[1]: Duplicate value: '
                   r'core.ServicePort{{Name:\"\", Protocol:\"TCP\", Port:1000, TargetPort:intstr.IntOrString'
                   r'{{Type:0, IntVal:0, StrVal:\"\"}}, NodePort:0}}'.format(RESOURCE_PREFIX),
        'reason': 'Invalid',
        'details': True,
        'causes': True,
        'reason_2': "FieldValueDuplicate",
        'message_2': r"Duplicate value: core.ServicePort{Name:\"\", Protocol:\"TCP\", Port:1000, "
                     r"TargetPort:intstr.IntOrString{Type:0, IntVal:0, StrVal:\"\"}, NodePort:0}",
        'field': "spec.ports[1]",
        'status_code': 422
    }
]

l2_wrong_create_list = ["创建带有非法字名称的service",
                        "创建名称为空的service",
                        "创建与已存在的service同名的service",
                        "创建端口名称带有非法字符的service",
                        "创建一个不支持的协议类型",
                        "服务端口为65536",
                        "服务端口为0",
                        "容器端口为65536",
                        "创建一个service使用相同的协议具有相同的服务端口"
                        ]

l2_known_issues_data_list = [
    {
        'service_name': "{}-target-port-0".format(RESOURCE_PREFIX),
        'type': 'ClusterIP',
        'sessionAffinity': 'ClientIP',
        'portdata': '一组数据',
        'p_name_1': 'http',
        'targetPort_1': '0',
        'message': r"Service \"{}-target-port-0\" is invalid: spec.ports[0].targetPort: "
                    r"Invalid value: 65536: must be between 1 and 65535, inclusive".format(RESOURCE_PREFIX),
        'reason': 'Invalid',
        'details': True,
        'causes': True,
        'reason_2': "FieldValueInvalid",
        'message_2': r"Invalid value: 65536: must be between 1 and 65535, inclusive",
        'field': "spec.ports[0].targetPort",
        'status_code': 422
    },
    {
        'service_name': "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        'type': 'ClusterIP',
        'sessionAffinity': 'ClientIP',
        'portdata': '一组数据',
        'message': r"Service \"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\" is invalid: metadata.name: "
                   r"Invalid value: \"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\": "
                   r"must be no more than 31 characters",
        'reason': 'Invalid',
        'details': True,
        'causes': True,
        'reason_2': "FieldValueInvalid",
        'message_2': r"Invalid value: \"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\": must be no more than 31 characters",
        'field': "metadata.name",
        'status_code': 422
    }
]

l2_known_issues_create_list = [
        "容器端口为0",
        "创建带有33个英文字符的service"]

update_casename_list = ["一组clusterip数据-源地址会话保持更新为多组clusterip数据无会话保持",
                        "多组nodeport数据-源地址会话保持更新为nodeport多组数据源地址会话保持",
                        "一组clusterip数据-headless更新为多组数据"]
update_data_list = [
    {'service_name': "{}-all".format(RESOURCE_PREFIX),
     'type': 'ClusterIP',
     'sessionAffinity': 'None',
     'portdata': '多组数据',
     },
    {'service_name': "{}-nodeport".format(RESOURCE_PREFIX),
     'type': 'NodePort',
     'sessionAffinity': 'ClientIP',
     'portdata': '多组数据'
     },
    {'service_name': "{}-headless".format(RESOURCE_PREFIX),
     'type': 'ClusterIP',
     'sessionAffinity': 'ClientIP',
     'portdata': '多组数据',
     'ClusterIP': "None",
     'selector': True
     }
]
