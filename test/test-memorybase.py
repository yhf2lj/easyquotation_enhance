from sqlalchemy import create_engine
from datetime import datetime, time
from easyquotation_enhance import SinaQuotation, stock_a_hour, TencentQuotation
from time import sleep
import sys

if __name__ == '__main__':
    sqlengine = create_engine("sqlite://")
    dl_sina = SinaQuotation(database_engine=sqlengine,
                            datatable='stock_sina',
                            timeout=0.8,
                            stock_num=800,
                            is_log=True,
                            thread=False)
    for i in range(5):
        dl_sina.downloadnow()

    print(sqlengine.execute("select * from stock_sina limit 10").fetchall())
