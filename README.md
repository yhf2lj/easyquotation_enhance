# easyquotation_enhance

快速下载全市场行情的利器，抄袭于easyquotation，增强于Demon Finch



### Function

- 修改了能批量插入数据库的数据结构
- 增加了单个线程超时的参数
- 加入了数据库sqlalchemy集成



### Install

```
pip install easyquotation_enhance
```



### Usage

###### Params

- database_engine: sqlalchemy的create_engine对象
- datatable: 存储数据的数据表
- timeout: 单个并发线程超时时间，默认为9999
- stock_num: 单个线程得到的股票数据量，sina默认为800，tencent默认为100


###### Sina

```python
from sqlalchemy import create_engine
from datetime import datetime
from easyquotation_enhance import SinaQuotation, stock_a_hour
import time

if __name__ == '__main__':
    sqlite_loc = "%s-test.db" % datetime.now().strftime("%Y-%m-%d")
    dl_qq = SinaQuotation(database_engine=create_engine("sqlite:///%s" % sqlite_loc),
                          datatable='stock_sina',
                          timeout=1,
                          stock_num=800)
    while True:
        if stock_a_hour(datetime.now().timestamp()):
            try:
                dl_qq.downloadnow()
            except Exception as ee:
                print(ee)
        else:
            print("relax 10s")
            time.sleep(10)


```

Tencent

```python
from sqlalchemy import create_engine
from datetime import datetime
from easyquotation_enhance import TencentQuotation, stock_a_hour
import time

if __name__ == '__main__':
    sqlite_loc = "%s-test.db" % datetime.now().strftime("%Y-%m-%d")
    dl_qq = TencentQuotation(database_engine=create_engine("sqlite:///%s" % sqlite_loc),
                             datatable='stock_qq',
                             timeout=1,
                             stock_num=400)

    while True:
        if stock_a_hour(datetime.now().timestamp()):
            try:
                dl_qq.downloadnow()
            except Exception as ee:
                print(ee)
        else:
            print("relax 10s")
            time.sleep(10)


```

###### 仅获取数据

​	请使用easyquotation

