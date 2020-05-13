#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import tarfile
import pytest
from common import settings
from common.log import logger
from common.utils import send_email, get_failed_case
from report_result import create_test_case


def main():
    # 执行case
    testcases = settings.TESTCASES.split(" ")
    run_command = ["-n", "auto", "--dist=loaddir", '-s',
                   "--html=./report/pytest.html",
                   "--junitxml=./report/pytest.xml", "--resultlog=./report/result.txt", "--self-contained-html"]
    for testcase in testcases:
        run_command.append(testcase)
    if settings.CASE_TYPE:
        run_command.append("-m {}".format(settings.CASE_TYPE))
    logger.info('pytest command: {}'.format(run_command))
    pytest.main(run_command)

    if settings.RESOURCE_PREFIX != "local":
        # 如果有失败的用例循环几次
        for i in range(0, 1):
            failed_cases = get_failed_case()
            print("start to rerun failed cases: {},rerun times:{}".format(failed_cases, i + 1))
            if len(failed_cases) > 0:
                with tarfile.open("./report/report_failed_{}.tar".format(i + 1), "w:gz") as tar:
                    tar.add("./report/", arcname=os.path.basename("./report"))
                for testcase in testcases:
                    run_command.remove(testcase)
                run_command = run_command + failed_cases
                pytest.main(run_command)

    with tarfile.open("./report/report.tar", "w:gz") as tar:
        tar.add("./report/", arcname=os.path.basename("./report"))
    if settings.RESOURCE_PREFIX != "local":
        file_paths = ["./report/report.tar"]
        if os.path.exists("./report/report_failed.tar"):
            file_paths.append("./report/report_failed.tar")
        send_email(
            "({}) ({}) ({}) ({}) API E2E Test".format(settings.ENV, settings.REGION_NAME,
                                                      settings.CASE_TYPE, settings.RESOURCE_PREFIX),
            "html", settings.RECIPIENTS, file_paths)
    # 同步用例
    if settings.ENV == "staging2":
        create_test_case()


if __name__ == '__main__':
    main()
