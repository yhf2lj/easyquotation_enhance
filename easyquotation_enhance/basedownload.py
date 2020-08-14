import requests
import re
from multiprocessing.pool import ThreadPool
import easyquotation
from datetime import datetime
from func_timeout import FunctionTimedOut, func_timeout
from sqlalchemy import MetaData, Table, create_engine

easyquotation.update_stock_codes()
quotation = easyquotation.use('qq')


class BaseDownload:
    """基础行情类"""
    def __init__(self, database_engine: create_engine, datatable: str, timeout: float = 99999, is_log=True):
        self._session = requests.session()
        self.stock_list = quotation.stock_list
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

    @property
    def table_create(self) -> Table:
        return Table()

    def downloadnow(self):
        start_time = datetime.now()
        self.stock_insert.execute(self.get_stock_data())
        end_time = datetime.now()
        if self.is_log:
            print("localtime:%s  time:%s" % (end_time, end_time - start_time))

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
