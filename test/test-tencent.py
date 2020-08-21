from sqlalchemy import create_engine
from datetime import datetime, time
from easyquotation_enhance import TencentQuotation, stock_a_hour
from time import sleep
import sys

if __name__ == '__main__':
    sqlite_loc = "%s-qq.db" % datetime.now().strftime("%Y-%m-%d")
    dl_qq = TencentQuotation(database_engine=create_engine("sqlite:///%s" % sqlite_loc),
                             datatable='stock_qq',
                             timeout=0.8,
                             stock_num=400,
                             is_log=True,
                             thread=True)

    while True:
        if stock_a_hour(datetime.now().timestamp()):
            try:
                dl_qq.downloadnow()
            except Exception as ee:
                print(ee)
        elif datetime.now().time() > time(15, 7):
            sys.exit(0)
        else:
            print("relax 10s , localtime: %s" % datetime.now())
            sleep(10)
