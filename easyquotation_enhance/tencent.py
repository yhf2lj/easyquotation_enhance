from .basedownload import BaseDownload
from sqlalchemy import Column, Integer, String, Float, DateTime
from typing import Optional
from sqlalchemy import MetaData, Table, create_engine
from datetime import datetime


class TencentQuotation(BaseDownload):
    def __init__(self,
                 stock_num: int = 400,
                 timeout: float = 9999,
                 database_engine: create_engine = None,
                 datatable: str = None,
                 is_log: bool = True,
                 thread: bool = True):
        """
        :param database_engine: sqlalchemy的create_engine对象
        :param datatable: 存储数据的数据表
        :param timeout: 单个并发线程超时时间，默认为9999
        :param stock_num: 单个线程得到的股票数据量，默认400
        :param is_log: 是否在命令行打印单次循环时间信息
        """
        super().__init__(database_engine, datatable, timeout, stock_num, is_log, thread)
        self.datatable = datatable
        self.stock_api = "http://qt.gtimg.cn/q="

    @property
    def table_create(self) -> Table:
        return Table(self.datatable, MetaData(),
                     Column('code', String(), primary_key=True),
                     Column("name", String()),
                     Column("datetime", DateTime, primary_key=True),
                     Column("now", Float()),
                     Column("close", Float()),
                     Column("open", Float()),
                     Column("volume", Float()),
                     Column("bid_volume", Integer()),
                     Column("ask_volume", Float()),
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
                     Column("last_deal", String(), comment='最近逐笔成交'),
                     Column("phg", Float(), comment='涨跌'),
                     Column("phg_percent", Float(), comment='涨跌百分比'),
                     Column("high", Float()),
                     Column("low", Float()),
                     Column("price_volumn_turnover", String(60), comment='价格 / 成交量(手) / 成交额'),
                     Column("deal_column", Integer(), comment='成交量(手)'),
                     Column("deal_turnover", Float(), comment=' 成交额(万) '),
                     Column("turnover", Float()),
                     Column("PE", Float()),
                     Column("unknown", String(50)),
                     Column("high_2", Float(), comment='意义不明'),
                     Column("low_2", Float(), comment='意义不明'),
                     Column("amplitude", Float(), comment='振幅'),
                     Column("fluent_market_value", Float(), comment='流通市值'),
                     Column("all_market_value", Float(), comment='总市值'),
                     Column("PB", Float()),
                     Column("price_limit_s", Float(), comment='涨停价'),
                     Column("price_limit_x", Float(), comment='跌停价'),
                     Column("quant_ratio", Float(), comment='量比'),
                     Column("commission", Float(), comment='委差'),
                     Column("avg", Float(), comment='均价'),
                     Column("market_earning_d", Float(), comment='市盈(动)'),
                     Column("market_earning_j", Float(), comment='市盈(静)'),
                     )

    def format_response_data(self, rep_data):
        """
        将取得的数据格式化为list字典格式方便插入数据库
        :param rep_data: 取得的数据
        :return: 格式化好的数据库
        """
        stocks_detail = "".join(rep_data)
        stock_details = stocks_detail.split(";")
        stock_dict = list()
        for stock_detail in stock_details:
            stock = stock_detail.split("~")
            if len(stock) <= 49:
                continue
            stock_dict.append({
                "name": stock[1],
                "code": self.grep_stock_code.search(stock[0]).group(),
                "now": float(stock[3]),
                "close": float(stock[4]),
                "open": float(stock[5]),
                "volume": float(stock[6]) * 100,
                "bid_volume": int(stock[7]) * 100,
                "ask_volume": float(stock[8]) * 100,
                "bid1": float(stock[9]),
                "bid1_volume": int(stock[10]) * 100,
                "bid2": float(stock[11]),
                "bid2_volume": int(stock[12]) * 100,
                "bid3": float(stock[13]),
                "bid3_volume": int(stock[14]) * 100,
                "bid4": float(stock[15]),
                "bid4_volume": int(stock[16]) * 100,
                "bid5": float(stock[17]),
                "bid5_volume": int(stock[18]) * 100,
                "ask1": float(stock[19]),
                "ask1_volume": int(stock[20]) * 100,
                "ask2": float(stock[21]),
                "ask2_volume": int(stock[22]) * 100,
                "ask3": float(stock[23]),
                "ask3_volume": int(stock[24]) * 100,
                "ask4": float(stock[25]),
                "ask4_volume": int(stock[26]) * 100,
                "ask5": float(stock[27]),
                "ask5_volume": int(stock[28]) * 100,
                "last_deal": stock[29],
                "datetime": datetime.strptime(stock[30], "%Y%m%d%H%M%S"),
                "phg": float(stock[31]),
                "phg_percent": float(stock[32]),
                "high": float(stock[33]),
                "low": float(stock[34]),
                "price_volumn_turnover": stock[35],
                "deal_column": int(stock[36]) * 100,
                "deal_turnover": float(stock[37]) * 10000,
                "turnover": self._safe_float(stock[38]),
                "PE": self._safe_float(stock[39]),
                "unknown": stock[40],
                "high_2": float(stock[41]),  # 意义不明
                "low_2": float(stock[42]),  # 意义不明
                "amplitude": float(stock[43]),
                "fluent_market_value": self._safe_float(stock[44]),
                "all_market_value": self._safe_float(stock[45]),
                "PB": float(stock[46]),
                "price_limit_s": float(stock[47]),
                "price_limit_x": float(stock[48]),
                "quant_ratio": self._safe_float(stock[49]),
                "commission": self._safe_acquire_float(stock, 50),
                "avg": self._safe_acquire_float(stock, 51),
                "market_earning_d": self._safe_acquire_float(stock, 52),
                "market_earning_j": self._safe_acquire_float(stock, 53),
            })
        return stock_dict

    @staticmethod
    def _safe_float(s: str) -> Optional[float]:
        try:
            return float(s)
        except ValueError:
            return None

    def _safe_acquire_float(self, stock: list, idx: int) -> Optional[float]:
        """
        There are some securities that only have 50 fields. See example below:
        ['\nv_sh518801="1',
        '国泰申赎',
        '518801',
        '2.229',
        ......
         '', '0.000', '2.452', '2.006', '"']
        """
        try:
            return self._safe_float(stock[idx])
        except IndexError:
            return None
