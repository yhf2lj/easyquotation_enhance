# coding:utf8
import json
import os
import re
import requests
from datetime import datetime

STOCK_CODE_PATH = os.path.join(os.path.dirname(__file__), "stock_codes.conf")

current_day = datetime.now().strftime("%Y-%m-%d")
trd_hour_start_morning = int(datetime.strptime(current_day + ' ' + '09:08:00', '%Y-%m-%d %H:%M:%S').timestamp())
trd_hour_end_morning = int(datetime.strptime(current_day + ' ' + '11:32:00', '%Y-%m-%d %H:%M:%S').timestamp())
trd_hour_start_afternoon = int(datetime.strptime(current_day + ' ' + '12:58:00', '%Y-%m-%d %H:%M:%S').timestamp())
trd_hour_end_afternoon = int(datetime.strptime(current_day + ' ' + '15:02:00', '%Y-%m-%d %H:%M:%S').timestamp())


def stock_a_hour(current_time):
    """A股时间段判断
    :param current_time:当前时间的时间戳，eg：time.time() 或者 datetime.now().timestamp()
    """
    return (trd_hour_start_morning <= current_time <= trd_hour_end_morning) or (
            trd_hour_start_afternoon <= current_time <= trd_hour_end_afternoon)


def update_stock_codes():
    """获取所有股票 ID 到 all_stock_code 目录下"""
    try:
        response = requests.get("http://www.shdjt.com/js/lib/astock.js")
    except Exception as e:
        raise Exception("更新股票代码失败")
    stock_codes = re.findall(r"~([a-z0-9]*)`", response.text)
    with open(STOCK_CODE_PATH, "w") as f:
        f.write(json.dumps(dict(stock=stock_codes)))
    return stock_codes


def get_stock_codes(realtime=False):
    """获取所有股票 ID 到 all_stock_code 目录下"""
    if realtime:
        return update_stock_codes()
    with open(STOCK_CODE_PATH) as f:
        return json.load(f)["stock"]


def get_stock_type(stock_code):
    """判断股票ID对应的证券市场
    匹配规则
    ['50', '51', '60', '90', '110'] 为 sh
    ['00', '13', '18', '15', '16', '18', '20', '30', '39', '115'] 为 sz
    ['5', '6', '9'] 开头的为 sh， 其余为 sz
    :param stock_code:股票ID, 若以 'sz', 'sh' 开头直接返回对应类型，否则使用内置规则判断
    :return 'sh' or 'sz'"""
    assert type(stock_code) is str, "stock code need str type"
    sh_head = ("50", "51", "60", "90", "110", "113",
               "132", "204", "5", "6", "9", "7")
    if stock_code.startswith(("sh", "sz", "zz")):
        return stock_code[:2]
    else:
        return "sh" if stock_code.startswith(sh_head) else "sz"


if __name__ == '__main__':
    update_stock_codes()
