# -*- coding: UTF-8 -*-
import urllib2
import datetime
import json
import logging
import mysql_st
import time
from threading import Thread
import threading
from multiprocessing import Process
import multiprocessing

##抓取个股数据

def get_logger(name):
    FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(format=FORMAT, level=logging.DEBUG)
    handler = logging.FileHandler('log.log')  ##使用handler输出不同目的地
    handler.setFormatter(logging.Formatter(FORMAT))
    logger = logging.getLogger(name)
    logger.addHandler(handler)
    return logger


def get_content(start,end,code):
    logger = get_logger(__name__)
    db = mysql_st.connectdb();
    header = {'Referer': 'http://webapi.cninfo.com.cn/',
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3418.2 Safari/537.36',
              'Cookie':'JSESSIONID=0201E01B2963A6EA2814E11A8FF1C5D5;Hm_lvt_489bd07e99fbfc5f12cbb4145adb0a9b=1534925363;cninfo_user_browse=000002,gssz0000002,%E4%B8%87%20%20%E7%A7%91%EF%BC%A1;codeKey=b4145e7eaf;Hm_lpvt_489bd07e99fbfc5f12cbb4145adb0a9b=1534929204;api_user_platform=80971|138685|4D74BB00B90FECDC334EF434F3B03CF7;domain=webapi.cninfo.com.cn;Max-Age=315360000;path=/',
              }

    url="http://webapi.cninfo.com.cn/api/sysapi/p_sysapi1021?scode="+code+"&sdate="+start+"&edate="+end+"&@column=SECCODE,SECNAME,F001D,F015N,F036N,F006N,F002V,F037N,F025N"
    req = urllib2.Request(url, headers=header)
    n=0
    map={}
    while(n < 3):
        try:
            url_content = urllib2.urlopen(req).read().decode('utf-8')
            map = json.loads(url_content, encoding='utf-8')
            # metadata = info['resultcode']
            if map['resultcode'] != 200:
                n = n + 1
                if (n == 3):
                    logger.info("股票数据返回失败，状态码不正确,code:%s,最终停止", code)
                    return False
                logger.info("股票数据返回失败，状态码不正确,code:%s,重试一次,try number:%s", code,n)
                time.sleep(0.5)
                continue
            break
        except Exception:
            n =n+1
            time.sleep(0.5)
            if (n==3):
                logger.info("请求股票url失败,code:%s,start:%s,end:%s,最终停止", code, start, end)
                return False
            logger.info("请求股票url失败,code:%s,start:%s,end:%s,重试一次", code,start,end)


    records = map['records']
    if len(records)==0:
        logger.info("股票%s没有返回数据", code)
        return False

    # for record in records:
    for index in range(len(records)):
        record=records[index]
        dic={}
        dic['ps'] = record['F037N']
        dic['name'] = record['SECNAME']
        dic['date'] = record['F001D']
        dic['price'] = record['F006N']
        dic['code'] = str(record['SECCODE'])[0:6]
        dic['pe'] = record['F015N']
        dic['pb'] = record['F036N']
        dic['place'] = record['F002V']
        mysql_st.insertstock(db,dic)
        if index%300==0:
          logger.info("处理股票%s的日期%s成功",code,record['F001D'])

    logger.info("爬取结束,start:%s,end:%s,code:%s", begin, datetime.datetime.today(), code)
    return True



if __name__=="__main__":


    start="1990-01-05";end="2018-08-26"
    begin = datetime.datetime.today()
    codes=['000488',
'000576',
'000815',
'000833',
'002012',
'002067',
'002078',
'002303',
'002511',
'002521',
'002565',
'600069',
'600103',
'600235',
'600308',
'600356',
'600433',
'600567',
'600793',
'600963',
'600966',
'603165',
'603607',
'603733'

    ]
    logger = get_logger(__name__)
    # pool = multiprocessing.Pool(processes=4)
    #
    # processes=[]
    # for code in codes:
    #     pool.apply_async(get_content,(start,end,code))
    #     p = Process(target=get_content, args=(start,end,code))
    # pool.close()
    # pool.join()
    # pool.terminate()
    #
    # logger.info("爬取结束,start:%s,end:%s", begin, datetime.datetime.today())

    logger.info("%s,正式开始爬取数据", begin)
    """以下是线程方式"""
    threads = []
    for code in codes:
        # code="600036"
        t = Thread(target=get_content,args=(start,end,code))
        threads.append(t)
    for mythread in threads:
        mythread.start()
        while True:
            if (len(threading.enumerate()) < 50):
                break
    for mythread in threads:
        mythread.join()
    logger.info("爬取结束,start:%s,end:%s", begin, datetime.datetime.today())
    # get_content(start,end,code)
