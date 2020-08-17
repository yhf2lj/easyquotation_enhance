import requests
import re
from multiprocessing.pool import ThreadPool
import easyquotation
from datetime import datetime
from func_timeout import FunctionTimedOut, func_timeout
from sqlalchemy import MetaData, Table, create_engine
from . import helpers
import json

easyquotation.update_stock_codes()
quotation = easyquotation.use('qq')


class BaseDownload:
    """基础行情类"""

    def __init__(self, database_engine: create_engine,
                 datatable: str,
                 timeout: float = 99999,
                 stock_num: int = 800,
                 is_log=True):
        self._session = requests.session()
        self.max_num = stock_num
        self.stock_codes = self.load_stock_codes()
        self.stock_list = self.gen_stock_list(self.stock_codes)
        self.stock_api = None
        self.grep_stock_code = re.compile(r"(?<=_)\w+")
        self.database_engine = database_engine
        self.datatable = datatable
        self.table = self.table_create
        self.table.create(self.database_engine, checkfirst=True)
        self.stock_insert = Table(self.datatable, MetaData(self.database_engine),
                                  autoload=True).insert().prefix_with("OR IGNORE")
        self.timeout = timeout
        self.is_log = is_log
        self.headers = {
            "Accept-Encoding": "gzip, deflate, sdch",
            "User-Agent": (
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/54.0.2840.100 "
                "Safari/537.36"
            ),
        }

    @staticmethod
    def load_stock_codes():
        with open(helpers.STOCK_CODE_PATH) as f:
            return json.load(f)["stock"]

    def gen_stock_list(self, stock_codes):
        stock_with_exchange_list = self._gen_stock_prefix(stock_codes)

        if self.max_num > len(stock_with_exchange_list):
            request_list = ",".join(stock_with_exchange_list)
            return [request_list]

        stock_list = []
        for i in range(0, len(stock_codes), self.max_num):
            request_list = ",".join(
                stock_with_exchange_list[i: i + self.max_num]
            )
            stock_list.append(request_list)
        return stock_list

    @staticmethod
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

    def _gen_stock_prefix(self, stock_codes):
        return [
            self.get_stock_type(code) + code[-6:] for code in stock_codes
        ]

    @property
    def table_create(self) -> Table:
        return Table()

    def downloadnow(self):
        start_time = datetime.now()
        self.stock_insert.execute(self.get_stock_data())
        end_time = datetime.now()
        if self.is_log:
            print("localtime:%s  time:%s" % (end_time, end_time - start_time))

    def market_snapshot(self):
        return self.get_stock_data()

    def format_response_data(self, rep_data):
        """
        将取得的数据格式化为list字典格式方便插入数据库
        :param rep_data: 取得的数据
        :return: 格式化好的数据库
        """
        pass

    def get_stock_batch(self, params):
        return self._session.get(self.stock_api + params, headers=self.headers)

    def get_stocks_by_range(self, params):
        try:
            r = func_timeout(self.timeout, self.get_stock_batch, args=(params,))
            return r.text
        except FunctionTimedOut:
            print("batch timeout")
        except Exception as e:
            print("something wrong,tell author please\n", e)

    def _fetch_stock_data(self, stock_list):
        """获取股票信息"""
        pool = ThreadPool(len(stock_list))
        try:
            res = pool.map(self.get_stocks_by_range, stock_list)
        finally:
            pool.close()
        return [d for d in res if d is not None]

    def get_stock_data(self):
        """获取并格式化股票信息"""
        res = self._fetch_stock_data(self.stock_list)
        return self.format_response_data(res)
