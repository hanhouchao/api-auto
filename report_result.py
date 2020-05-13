# -*- coding:utf-8 -*-
import json
import os
import testlink
import http.client
import xmlrpc.client
import ssl

url = 'http://testlink.alauda.cn/lib/api/xmlrpc/v1/xmlrpc.php'
key = '7ccbcfc2d1c580277d7b5ce1038c9ee6'
testplan_name = "2.6"
build_name = "2.6"
testproject_name = "ACPAPI"
testproject_prefix = "ACPAPI"


class ProxiedTransport(xmlrpc.client.Transport):
    def set_proxy(self, host, port=None, headers=None):
        self.proxy = host, port
        self.proxy_headers = headers
        self.contex = ssl._create_unverified_context()

    def make_connection(self, host):
        connection = http.client.HTTPSConnection(*self.proxy, context=self.contex)
        connection.set_tunnel(host)
        self._connection = host, connection
        return connection


proxy = ProxiedTransport()
proxy.set_proxy("139.186.2.80", 37491)
tlc = testlink.TestlinkAPIClient(url, key, transport=proxy)


# tlc = testlink.TestlinkAPIClient(url, key)


def update_case_status(testplan_id, case_id, status):
    try:
        tlc.reportTCResult(testcaseid=case_id, testplanid=testplan_id, buildname=build_name, status=status)
        print(case_id)
        return True
    except Exception as e:
        print(e)
        return False


def get_testplan_id():
    testplan = tlc.getTestPlanByName(testproject_name, testplan_name)
    testplan_id = testplan[0]["id"]
    return testplan_id


def report_test_result():
    result_file = open("./report/result.txt", "r")
    results = result_file.readlines()
    testplan_id = get_testplan_id()
    success_num = 0
    failed_num = 0
    error_num = 0
    for result in results:
        try:
            if result[0] == ".":
                case_name = result.split("::")[-1][2:]
                testcase_info = tlc.getTestCaseIDByName(case_name, testprojectname=testproject_name)
                case_id = testcase_info[0]["id"]
                if update_case_status(testplan_id, case_id, 'p'):
                    success_num += 1
            elif result[0] == "E" or result[0] == "F":
                case_name = result.split("::")[-1][2:]
                testcase_info = tlc.getTestCaseIDByName(case_name, testprojectname=testproject_name)
                case_id = testcase_info[0]["id"]
                if update_case_status(testplan_id, case_id, 'f'):
                    failed_num += 1
        except Exception as e:
            print(e)
            error_num += 1
            continue
    print("已经成功将%d个成功的用例和%d个失败的用例更新到testlink上，更新失败%d个" % (success_num, failed_num, error_num))


def create_test_case():
    testprojectid = tlc.getProjectIDByName(testproject_name)
    # testsuiteid = tlc.getTestSuite(testsuitename, testproject_prefix)[0]["id"]
    result_file = open("./report/result.txt", "r")
    results = result_file.readlines()
    for result in results:
        importance = 2
        executiontype = 2
        if result[0] == 's':
            executiontype = 1
            importance = 1
        elif result[0] == " ":
            continue
        testsuiteid = get_suite_id(result, testprojectid)
        case_name = result.split("::")[-1][2:]
        try:
            suitename = get_path_name(os.path.split(result)[0].split("/")[-1])

            testcase_info = tlc.getTestCaseIDByName(case_name, testsuitename=suitename,
                                                    testprojectname=testproject_name)
            id = "{}-{}".format(testproject_prefix, testcase_info[0]["tc_external_id"])
            tlc.updateTestCase(testcaseexternalid=id, executiontype=executiontype, importance=importance)
            testcase_info = tlc.getTestCase(testcaseexternalid=id)
        except Exception as e:
            print(e)
            testcase_info = tlc.createTestCase(case_name, testsuiteid, testprojectid, "hchan", "summary", steps=[],
                                               executiontype=executiontype,
                                               importance=importance)
        print(testcase_info)


def get_suite_id(case_path, testprojectid):
    suite_id = ""
    for path in os.path.split(case_path)[0].split("/")[1:]:
        path = get_path_name(path)
        suite = get_suite_info(path)
        if len(suite) > 0:
            suite_id = suite[0]["id"]
        elif suite_id:
            suite_id = tlc.createTestSuite(testprojectid, path, path, parentid=suite_id)[0]["id"]
        else:
            suite_id = tlc.createTestSuite(testprojectid, path, path)[0]["id"]
    return suite_id


def get_path_name(path):
    path_file = open("./test_data/global_data/casepath.json", "r")
    paths = path_file.read()
    return json.loads(paths)[path]


def get_suite_info(path):
    try:
        suite = tlc.getTestSuite(path, testproject_prefix)
    except Exception as e:
        print(e)
        suite = []
    finally:
        return suite


def get_suite():
    testprojectid = tlc.getProjectIDByName(testproject_name)
    firstsuites = tlc.getFirstLevelTestSuitesForTestProject(testprojectid)
    cnt = 0
    for firstsuite in firstsuites:
        cases = tlc.getTestCasesForTestSuite(testsuiteid=firstsuite["id"], details="full")
        for case in cases:
            if case["execution_type"] == '1':
                print(case["name"])
                tlc.updateTestCase(testcaseexternalid=case["external_id"], importance=2)
                cnt += 1
    print(cnt)


if __name__ == "__main__":
    # report_test_result()
    create_test_case()
    # get_suite()
