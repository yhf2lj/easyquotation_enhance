from sqlalchemy import create_engine
from datetime import datetime, time
from easyquotation_enhance import SinaQuotation, stock_a_hour, TencentQuotation
from time import sleep
import sys

if __name__ == '__main__':
    dl_sina = TencentQuotation(timeout=0.8)
    while True:
        dl_sina.market_snapshot()
