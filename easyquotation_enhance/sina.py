# coding:utf8
from .basedownload import BaseDownload
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy import MetaData, Table, create_engine
from datetime import datetime
import re
import time


class SinaQuotation(BaseDownload):
    """新浪免费行情获取"""

    grep_detail = re.compile(
        r"(\d+)=[^\s]([^\s,]+?)%s%s"
        % (r",([\.\d]+)" * 29, r",([-\.\d:]+)" * 2)
    )
    grep_detail_with_prefix = re.compile(
        r"(\w{2}\d+)=[^\s]([^\s,]+?)%s%s"
        % (r",([\.\d]+)" * 29, r",([-\.\d:]+)" * 2)
    )
    del_null_data_stock = re.compile(
        r"(\w{2}\d+)=\"\";"
    )

    def __init__(self,
                 stock_num: int = 800,
                 timeout: float = 9999,
                 database_engine: create_engine = None,
                 datatable: str = None,
                 is_log: bool = True,
                 thread: bool = True,
                 stocklist: list = None):
        """
        :param database_engine: sqlalchemy的create_engine对象
        :param datatable: 存储数据的数据表
        :param timeout: 单个并发线程超时时间
        :param stock_num: 单个线程得到的股票数据量
        :param is_log: 是否在命令行打印单次循环时间信息
        :param stocklist: 已分割的股票清单，eg：['sh000001,sz000002,sh515700','sh000003,sh039413,sz600232']
        """
        super().__init__(database_engine, datatable, timeout, stock_num, is_log, thread, stocklist)
        self.datatable = datatable
        self.stock_api = f"http://hq.sinajs.cn/rn={int(time.time() * 1000)}&list="

    @property
    def table_create(self) -> Table:
        return Table(self.datatable, MetaData(),
                     Column('code', String(), primary_key=True),
                     Column("name", String()),
                     Column("open", Float()),
                     Column("close", Float()),
                     Column("now", Float()),
                     Column("high", Float()),
                     Column("low", Float()),
                     Column("buy", Integer()),
                     Column("sell", Float()),
                     Column("turnover", Float()),
                     Column("volume", Float()),
                     Column("datetime", DateTime, primary_key=True),
                     Column("bid1", Float()),
                     Column("bid1_volume", Integer()),
                     Column("bid2", Float()),
                     Column("bid2_volume", Integer()),
                     Column("bid3", Float()),
                     Column("bid3_volume", Integer()),
                     Column("bid4", Float()),
                     Column("bid4_volume", Integer()),
                     Column("bid5", Float()),
                     Column("bid5_volume", Integer()),
                     Column("ask1", Float()),
                     Column("ask1_volume", Integer()),
                     Column("ask2", Float()),
                     Column("ask2_volume", Integer()),
                     Column("ask3", Float()),
                     Column("ask3_volume", Integer()),
                     Column("ask4", Float()),
                     Column("ask4_volume", Integer()),
                     Column("ask5", Float()),
                     Column("ask5_volume", Integer()),
                     )

    def format_response_data(self, rep_data):
        stocks_detail = "".join(rep_data)
        stocks_detail = self.del_null_data_stock.sub('', stocks_detail)
        stocks_detail = stocks_detail.replace(' ', '')
        result = self.grep_detail_with_prefix.finditer(stocks_detail)
        stock_list = list()
        for stock_match_object in result:
            stock = stock_match_object.groups()
            try:
                stock_list.append(dict(
                    code=stock[0],
                    name=stock[1],
                    open=float(stock[2]),
                    close=float(stock[3]),
                    now=float(stock[4]),
                    high=float(stock[5]),
                    low=float(stock[6]),
                    buy=float(stock[7]),
                    sell=float(stock[8]),
                    turnover=int(stock[9]),
                    volume=float(stock[10]),
                    bid1_volume=int(stock[11]),
                    bid1=float(stock[12]),
                    bid2_volume=int(stock[13]),
                    bid2=float(stock[14]),
                    bid3_volume=int(stock[15]),
                    bid3=float(stock[16]),
                    bid4_volume=int(stock[17]),
                    bid4=float(stock[18]),
                    bid5_volume=int(stock[19]),
                    bid5=float(stock[20]),
                    ask1_volume=int(stock[21]),
                    ask1=float(stock[22]),
                    ask2_volume=int(stock[23]),
                    ask2=float(stock[24]),
                    ask3_volume=int(stock[25]),
                    ask3=float(stock[26]),
                    ask4_volume=int(stock[27]),
                    ask4=float(stock[28]),
                    ask5_volume=int(stock[29]),
                    ask5=float(stock[30]),
                    datetime=datetime.strptime(stock[31] + " " + stock[32], "%Y-%m-%d %H:%M:%S"),
                ))
            except ValueError:
                continue
            except Exception as error:
                print("错误数据：", stock)
                print(error)
        return stock_list
