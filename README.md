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

###### Sina

```python
from sqlalchemy import create_engine
from datetime import datetime
from easyquotation_enhance import SinaQuotation

if __name__ == '__main__':
    sqlite_loc = "%s-test.db" % datetime.now().strftime("%Y-%m-%d")
    dl_qq = SinaQuotation(database_engine=create_engine("sqlite:///%s" % sqlite_loc),
                          datatable='stock_sina',
                          timeout=1)
    """一直运行到15：06"""
    stop_time = int(datetime.strptime(datetime.now().strftime("%Y-%m-%d"), "%Y-%m-%d").timestamp()) + 3600 * 15.1
    """未开盘时间请改变条件"""
    while datetime.now().timestamp() > stop_time:
        try:
            dl_qq.downloadnow()
        except Exception as ee:
            print(ee)

```

Tencent

```python
from sqlalchemy import create_engine
from datetime import datetime
from easyquotation_enhance import TencentQuotation

if __name__ == '__main__':
    sqlite_loc = "%s-test.db" % datetime.now().strftime("%Y-%m-%d")
    dl_qq = TencentQuotation(database_engine=create_engine("sqlite:///%s" % sqlite_loc),
                             datatable='stock_qq',
                             timeout=3)
    """一直运行到15：06"""
    stop_time = int(datetime.strptime(datetime.now().strftime("%Y-%m-%d"), "%Y-%m-%d").timestamp()) + 3600 * 15.1
    """未开盘时间请改变条件"""
    while datetime.now().timestamp() > stop_time:
        try:
            dl_qq.downloadnow()
        except Exception as ee:
            print(ee)

        # break

```

###### 仅获取数据

​	请使用easyquotation

