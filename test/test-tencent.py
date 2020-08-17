from sqlalchemy import create_engine
from datetime import datetime
from easyquotation_enhance import TencentQuotation

if __name__ == '__main__':
    sqlite_loc = "%s-test.db" % datetime.now().strftime("%Y-%m-%d")
    dl_qq = TencentQuotation(database_engine=create_engine("sqlite:///%s" % sqlite_loc),
                             datatable='stock_qq',
                             timeout=1,
                             stock_num=400)

    while True:
        try:
            dl_qq.downloadnow()
        except Exception as ee:
            print(ee)
