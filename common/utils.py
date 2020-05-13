# coding=utf-8
import smtplib
import jinja2
import yaml
import os
import json
import base64
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from bs4 import BeautifulSoup
from common.settings import SMTP


def send_email(subject, body, recipients, file_paths):
    """class method to send an email"""

    # if settings.EMAIL is None or settings.SMTP is None:
    #    logger.error("No email/smtp config, email not sent.")
    #    return

    if not isinstance(recipients, list):
        raise TypeError(
            "{} should be a list".format(recipients))

    # we only support one sender for now
    from_email = SMTP['sender']

    # build message
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = ','.join(recipients)
    msg['Subject'] = Header(subject, 'utf8')
    msg.attach(MIMEText(body, 'html', 'utf8'))
    # add report html
    for file_path in file_paths:
        att = MIMEText(open(file_path, 'rb').read(), 'base64', 'gb2312')
        att["Content-Type"] = 'application/octet-stream'
        att["Content-Disposition"] = 'attachment; filename="{tar}"'.format(tar=os.path.split(file_path)[-1])
        msg.attach(att)

    try:
        server = smtplib.SMTP_SSL(host=SMTP['host'], port=SMTP['port'])
        server.set_debuglevel(SMTP['debug_level'])
        server.login(SMTP['username'], SMTP['password'])
        server.sendmail(from_email, recipients, msg.as_string())
        print("send email successfully")
    except Exception as e:
        # don't fatal if email was not send
        print("send email failed，the reason is：{}".format(e))
    # finally:
    #     if server:
    #         server.quit()


def read_result():
    with open("./report/pytest.html", "r") as fp:
        report = BeautifulSoup(fp, "html.parser")
        tbodys = report.select("tbody")
        pass_count = 0
        failed_count = 0
        rerun_count = 0
        skip_count = 0
        result_flag = 'Success'
        json_result = {"case_details": []}
        for tbody in tbodys:
            tds = tbody.select("td")
            extra = tbody.select("td.extra")
            if tds[1].text.split("::")[-1] != "setup":
                case_name = tds[1].text.split("::")[-1]
            else:
                case_name = tds[1].text.split("::")[-2]

            if tds[0].text == "Skipped":
                case_detail = tds[-1].select("div")[0].text.split(":")[-1].split("'")[0]
                json_result["case_details"].append(
                    {"case_name": case_name, "case_flag": tds[0].text, "case_detail": case_detail,
                     "case_time": tds[2].text, "case_location": tds[1].text, "extra": extra[0].text})
                skip_count += 1
            elif tds[0].text == "Passed" and tds[2].text != "0.00":
                pass_count += 1
            elif tds[0].text == "Failed" or tds[0].text == "Error":
                error_info = ""
                for content in tbody.select("span"):
                    error_info += content.text
                error_message = "{},失败请单独执行case:{}".format(error_info, tds[1].text)
                json_result["case_details"].append(
                    {"case_name": case_name, "case_flag": tds[0].text, "case_detail": error_message,
                     "case_time": tds[2].text, "case_location": tds[1].text, "extra": extra[0].text})
                failed_count += 1
                result_flag = 'Failed'
            elif tds[0].text == "Rerun":
                error_info = ""
                for content in tbody.select("span"):
                    error_info += content.text
                json_result["case_details"].append(
                    {"case_name": case_name, "case_flag": tds[0].text, "case_detail": error_info,
                     "case_time": tds[2].text, "case_location": tds[1].text, "extra": extra[0].text})
                rerun_count += 1
            else:
                pass
        json_result_summary = {
            "summary": report.select("p")[1].text,
            "pass_num": pass_count,
            "failed_num": failed_count,
            "rerun_num": rerun_count,
            "skip_num": skip_count
        }
        if pass_count == failed_count == rerun_count == skip_count == 0:
            result_flag = "Failed"
        json_result.update(json_result_summary)
        with open('./report/pytest.json', 'w') as f:
            f.write(json.dumps(json_result, indent=4, ensure_ascii=False))
        with open('./report/pytest.yaml', 'w') as f:
            f.write(yaml.dump(json_result, indent=4, allow_unicode=True))
    with open("./test_data/report_template/report.jinja2", "r") as fp:
        content = fp.read()
        template = jinja2.Template(content)
        html = template.render(json_result)
        return result_flag, html


def dockerjson(address, username, password, email):
    data = {
        "auths": {
            address: {
                "username": username,
                "password": password,
                "email": email
            }
        }
    }
    return str(base64.b64encode(json.dumps(data).encode('utf-8')), 'utf8')


def get_failed_case():
    result_file = open("report/result.txt", "r")
    results = result_file.readlines()

    rerun_case = []
    for result in results:
        if result[0] == "F" or result[0] == "E":
            case = os.path.split(result.split(" ")[1])[0]
            rerun_case.append(case)

    return list(set(rerun_case))
