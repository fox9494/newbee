# -*- coding: UTF-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plot

import MySQLdb

##pandas分析显示
connect = MySQLdb.connect("127.0.0.1", "root", "root", "test", charset='utf8')

##显示大盘pe
# typedic = {"1":"上海A股","2":"深圳主板","3":"中小板","4":"创业板"}
# type=1
# df = pd.read_sql("select * from st_market where type = {}".format(type),connect)
# df.plot("trade_date",["pe"])


##显示个股pe，pb的
code="000807"
df = pd.read_sql("select * from st_stock where code={}".format(code),connect)
df.plot("trade_date",["pb"])



# df.set_index("trade_date")
# df.plot("trade_date",["pb","pe"])


plot.legend()
plot.show()
with pd.option_context('display.max_rows', 20, 'display.max_columns', None):
    print df.head()




