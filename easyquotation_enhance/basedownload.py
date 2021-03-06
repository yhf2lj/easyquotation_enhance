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
                 is_log=True,
                 thread=True,
                 stocklist=None):
        helpers.update_stock_codes()
        self._session = requests.session()
        self.max_num = stock_num
        if stocklist:
            self.stock_list = stocklist
        else:
            self.stock_list = self.gen_stock_list(self.load_stock_codes())
        self.stock_api = None
        self.timeout = timeout
        self.grep_stock_code = re.compile(r"(?<=_)\w+")
        self.if_thread = thread
        if database_engine and datatable:
            self.database_engine = database_engine
            self.datatable = datatable
            self.table = self.table_create
            self.table.create(self.database_engine, checkfirst=True)
            self.stock_insert = Table(self.datatable, MetaData(self.database_engine),
                                      autoload=True).insert().prefix_with("OR IGNORE")
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
        """加载股票数据"""
        with open(helpers.STOCK_CODE_PATH) as f:
            return json.load(f)["stock"]

    def gen_stock_list(self, stock_codes):
        """获取股票分割清单"""
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
        """下载股票数据至数据库，需要database_engine不为空"""
        # if self.database_engine is None:
        #     raise Exception("仅获取股票数据请使用market_snapshot方法")
        if self.is_log:
            start_time = datetime.now()
            stockdata = self.get_stock_data()
            midtime = datetime.now()
            self.stock_insert.execute(stockdata)
            end_time = datetime.now()
            print("localtime:%s  time:%s  getdatatime:%s  tosqltime:%s" % (
                end_time, end_time - start_time, midtime - start_time, end_time - midtime))
        else:
            self.stock_insert.execute(self.get_stock_data())

    def market_snapshot(self):
        """获取市场截面数据"""
        return self.get_stock_data()

    def format_response_data(self, rep_data):
        """
        将取得的数据格式化为list字典格式方便插入数据库
        :param rep_data: 取得的数据
        :return: 格式化好的数据库
        """
        return list()

    def get_stock_batch(self, params):
        return self._session.get(self.stock_api + params, headers=self.headers)

    def get_stocks_by_range(self, params):
        try:
            r = func_timeout(self.timeout, self.get_stock_batch, args=(params,))
            return r.text
        except FunctionTimedOut:
            print("batch timeout,localtime:%s" % datetime.now())
            return ''
        except Exception as e:
            print("something wrong,tell author please\n", e)
            return ''

    def _fetch_stock_data(self, stock_list):
        """获取股票信息"""
        if self.if_thread:
            pool = ThreadPool(len(stock_list))
            try:
                res = pool.map(self.get_stocks_by_range, stock_list)
            finally:
                pool.close()
            return [d for d in res if d is not None]
        else:
            return [self.get_stocks_by_range(param) for param in stock_list]

    def get_stock_data(self):
        """获取并格式化股票信息"""
        res = self._fetch_stock_data(self.stock_list)
        return self.format_response_data(res)

    def get_real(self, stock_list: list):
        """获取单个的股票结果，传入list"""
        if len(stock_list) > 400:
            raise Exception("单次限制400个股票")
        res = [self.get_stock_batch(",".join(stock_list)).text]
        return self.format_response_data(res)
