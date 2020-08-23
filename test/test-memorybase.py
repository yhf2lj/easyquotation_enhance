from sqlalchemy import create_engine
from easyquotation_enhance import SinaQuotation, update_stock_codes

if __name__ == '__main__':
    update_stock_codes()
    sqlengine = create_engine("sqlite://")
    dl_sina = SinaQuotation(database_engine=sqlengine,
                            datatable='stock_sina',
                            timeout=0.8,
                            stock_num=800,
                            is_log=True,
                            thread=True)
    dl_sina.downloadnow()

    print(sqlengine.execute("select * from stock_sina limit 1").fetchall())
    print(sqlengine.execute("select count(*) from stock_sina ").fetchall())
