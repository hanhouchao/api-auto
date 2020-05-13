import base64
import os
import requests
import re
import urllib3
from time import sleep


def get_list_from_str(string, separator=','):
    if string is not None and string != '':
        return string.split(separator)


ENV = os.getenv("ENV", "staging")
RESOURCE_PREFIX = os.getenv("RESOURCE_PREFIX",
                            "local").replace(".", "").replace("_",
                                                              "-").lower()[0:10]
# necessary
API_URL = "https://10.0.129.100"
REGION_NAME = "high"
CALICO_REGION = "cls-w5xrsf62"
OVN_REGION = "high"
MACVLAN_REGION = os.getenv("MACVLAN_REGION")
GLOBAL_REGION_NAME = "global"
REGISTRY = "10.0.129.100:60080"
IMAGE = "{}/alaudaorg/qaimages:helloworld".format(REGISTRY)
GLOBAL_ALB_NAME = "alb2"
DEFAULT_NS = "alauda-system"
DEFAULT_LABEL = "alauda.io"
USERNAME = "admin@alauda.io"
PASSWORD = "password"
VM_USERNAME = "root"
OIDC_ISSUER_URL = os.getenv('OIDC_HOST',
                            'http://keycloak.qa.alauda.cn/auth/realms/master')
OIDC_SECRET_ID = os.getenv('OIDC_SECRET_ID',
                           '54043ce8-007d-490c-98db-b124acf1ab7b')
PROXY = {
}
# not necessary
TESTCASES = os.getenv("TESTCASES", "")
CASE_TYPE = os.getenv("CASE_TYPE", "")
PROJECT_NAME = "e2eproject"
K8S_NAMESPACE = "e2enamespace"
RECIPIENTS = get_list_from_str(os.getenv("RECIPIENTS", "testing@alauda.io"))

# 重试次数
RERUN_TIMES = int(os.getenv("RERUN_TIMES", 0))
# 日志级别和存储位置
LOG_LEVEL = "INFO"
LOG_PATH = "./report"
# 邮件服务器地址
SMTP = {
    'host': os.getenv('SMTP_HOST', 'smtp.163.com'),
    'port': os.getenv('SMTP_PORT', 465),
    'username': os.getenv('SMTP_USERNAME', '15830736131@163.com'),
    'password': os.getenv('SMTP_PASSWORD', 'xxx'),
    'sender': os.getenv('EMAIL_FROM', '15830736131@163.com'),
    'debug_level': 0,
    'smtp_ssl': True
}


def retry(times=3, sleep_secs=10):
    def retry_deco(func):
        def retry_deco_wrapper(*args, **kwargs):
            count = 0
            success = False
            data = None
            while not success and count < times:
                count += 1
                try:
                    data = func(*args, **kwargs)
                    success = True
                except Exception as e:
                    print("get token error:{}, sleep 10s,times={}".format(e, count))
                    sleep(sleep_secs)
                    if count == times:
                        assert False, "get token info failed"
            return data

        return retry_deco_wrapper

    return retry_deco


@retry()
def get_token(idp_name='local', username=USERNAME, password=PASSWORD):
    url = API_URL + "/console-acp/api/v1/token/login"
    urllib3.disable_warnings()
    headers = {"Referer": "{url}/console-acp".format(url=API_URL)}
    r = requests.get(url, verify=False, timeout=15, proxies=PROXY, headers=headers)
    auth_url = r.json()["auth_url"]
    auth_path = '/'.join(auth_url.split("/")[-2:])
    auth_url = API_URL + '/' + auth_path
    r = requests.get(auth_url, verify=False, proxies=PROXY)
    content = r.text
    req = re.search('req=[a-zA-Z0-9]{25}', content).group(0)[4:]
    url = API_URL + "/dex/auth/{}?req=".format(idp_name) + req
    # generate connectorID
    requests.get(url, verify=False, timeout=10, proxies=PROXY)
    # login acp platform
    params = {"login": username, "encrypt": str(base64.b64encode(password.encode('utf-8')), "utf8")}

    response = requests.post(
        url, params=params, verify=False, timeout=10, proxies=PROXY)
    content = response.history[1].text

    code = re.search('[a-zA-Z0-9]{25}', content).group(0)
    url = API_URL + "/console-acp/api/v1/token/callback?code={}&state=alauda-console".format(
        code)

    r = requests.get(url, verify=False, proxies=PROXY, headers=headers)
    ret = r.json()
    token = ret['id_token']
    token_type = ret['token_type']
    refresh_token = ret['refresh_token']
    auth = "{} {}".format(token_type.capitalize(), token)
    return auth, refresh_token


# 发送请求的headers
headers = {"Content-Type": "application/json", "Authorization": get_token()[0]}
AUDIT_UNABLED = True
