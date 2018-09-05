# -*- coding: UTF-8 -*-
#日期时间
import datetime
import time

print int(round(time.time()*1000))  ##毫秒级时间戳
print datetime.datetime.now()
print type(datetime.datetime.now())  ##返回格式
print type(datetime.datetime.now().isoformat())  ##
print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  #转字符串

date_l=datetime.datetime.strptime("2015-07-17 16:58:46","%Y-%m-%d %H:%M:%S") #字符串转日期
print "date_1:{}".format(date_l)

date_2 = datetime.datetime.fromtimestamp(1437123812.0) ##时间戳转日期
print "date_2:{}".format(date_2)
print datetime.datetime.now()+datetime.timedelta(days=1) #时间加减
print datetime.datetime.now()+datetime.timedelta(hours=1)