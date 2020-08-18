from sqlalchemy import create_engine
from datetime import datetime, time
from easyquotation_enhance import SinaQuotation, stock_a_hour
from time import sleep
import sys

if __name__ == '__main__':
    sqlite_loc = "%s-sina.db" % datetime.now().strftime("%Y-%m-%d")
    dl_sina = SinaQuotation(database_engine=create_engine("sqlite:///%s" % sqlite_loc),
                            datatable='stock_sina',
                            timeout=0.8,
                            stock_num=800)

    while True:
        if stock_a_hour(datetime.now().timestamp()):
            try:
                dl_sina.downloadnow()
            except Exception as ee:
                print(ee)
        elif datetime.now().time() > time(15, 7):
            sys.exit(0)
        else:
            print("relax 10s , localtime: %s" % datetime.now())
            sleep(10)
