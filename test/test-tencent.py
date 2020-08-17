from sqlalchemy import create_engine
from datetime import datetime
from easyquotation_enhance import TencentQuotation

if __name__ == '__main__':
    sqlite_loc = "%s-test.db" % datetime.now().strftime("%Y-%m-%d")
    dl_qq = TencentQuotation(database_engine=create_engine("sqlite:///%s" % sqlite_loc),
                             datatable='stock_qq',
                             timeout=1,
                             stock_num=400)
    """一直运行到15：06"""
    stop_time = int(datetime.strptime(datetime.now().strftime("%Y-%m-%d"), "%Y-%m-%d").timestamp()) + 3600 * 15.1
    """未开盘时间请改变条件"""
    while datetime.now().timestamp() > stop_time:
        try:
            dl_qq.downloadnow()
        except Exception as ee:
            print(ee)

        # break
