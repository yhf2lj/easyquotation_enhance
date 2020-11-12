# easyquotation_enhance

快速下载全市场行情的利器，抄袭于easyquotation，增强于Demon Finch



### Function

- 修改了能批量插入数据库的数据结构
- 增加了单个线程超时的参数
- 加入了数据库sqlalchemy集成

### 注意事项
- 请不要使用机械硬盘运行（因为长期频繁的随机读操作可能让你的机械硬盘早夭）
- 硬盘io跟不上的时候，可以选择sqlite的内存数据库，中场休息再持久化到本地

### Install

```
pip install easyquotation_enhance
```


### Usage

###### Params

- database_engine: sqlalchemy的create_engine对象
- datatable: 存储数据的数据表
- timeout: 单个并发线程超时时间，默认为9999
- stock_num: 单个线程得到的股票数据量，sina默认为800，tencent默认为400
- is_log: 是否打印单个循环的时间日志，默认为True
- thread: 是否使用多线程，默认为True

###### Sina

```python
from sqlalchemy import create_engine
from datetime import datetime, time
from easyquotation_enhance import SinaQuotation, stock_a_hour
from time import sleep
import sys

if __name__ == '__main__':
    sqlite_loc = "%s-sina.db" % datetime.now().strftime("%Y-%m-%d")
    dl_sina = SinaQuotation(database_engine=create_engine("sqlite:///%s" % sqlite_loc),
                            datatable='stock_sina',
                            timeout=1.2,
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

```

Tencent

```python
from sqlalchemy import create_engine
from datetime import datetime, time
from easyquotation_enhance import TencentQuotation, stock_a_hour
from time import sleep
import sys

if __name__ == '__main__':
    sqlite_loc = "%s-qq.db" % datetime.now().strftime("%Y-%m-%d")
    dl_qq = TencentQuotation(database_engine=create_engine("sqlite:///%s" % sqlite_loc),
                             datatable='stock_qq',
                             timeout=1.2,
                             stock_num=400)

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

```
###### 获取单个或多个股票数据
```python
from easyquotation_enhance import SinaQuotation

dl_sina = SinaQuotation()
print(dl_sina.get_real(['sh515700', 'sz000001']))
```

###### 仅获取数据
```python
from easyquotation_enhance import SinaQuotation

dl_sina = SinaQuotation()
print(dl_sina.market_snapshot()[:5])
```

## Thanks

[![PyCharm](https://i.loli.net/2020/11/12/xz1UQq5kmWinCbl.png)](https://www.jetbrains.com/?from=yhf2lj)