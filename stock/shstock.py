# -*- coding: UTF-8 -*-
import urllib2
import re
import datetime
import json
import logging
import time
import mysql_st

##抓取上海证券所大盘数据

FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)
handler = logging.FileHandler('sh.log')  ##使用handler输出不同目的地
handler.setFormatter(logging.Formatter(FORMAT))
logger = logging.getLogger(__name__)
logger.addHandler(handler)


typedic = {"1":"上海A股","2":"深圳主板","3":"中小板","4":"创业板"}



def get_content_sh(start,end):
    db = mysql_st.connectdb();
    header = {'Referer': 'http://www.sse.com.cn/market/stockdata/overview/day/',
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3418.2 Safari/537.36'}

    datestart = datetime.datetime.strptime(start, '%Y-%m-%d')
    dateend = datetime.datetime.strptime(end, '%Y-%m-%d')
    while datestart <= dateend:
        mydate = datestart.strftime('%Y-%m-%d')
        url = "http://query.sse.com.cn/marketdata/tradedata/queryTradingByProdTypeData.do?jsonCallBack=jsonpCallback8286&searchDate=" + mydate+ "&prodType=gp&_=1525914100378"
        req = urllib2.Request(url, headers=header)
        try:
            url_content = urllib2.urlopen(req).read().decode('utf-8')
        except Exception:
            logger.info("请求上交所url失败,date:%s", mydate)
        else:
            result = url_content[url_content.find('{'):len(url_content) - 1]
            obj = json.loads(result, encoding='utf-8')
            result = obj['result']
            for info in result:
                if info['marketValue'] == "" and info['productType'] == "1":
                    continue
                dic={}
                if info['productType'] == "1":  ##只处理a股情况
                    dic['type'] ="1"
                    dic['typename']=typedic['1']
                    dic['pe'] = info['profitRate']
                    dic['totalvalue'] = info['marketValue']
                    dic['totalnum'] = info['trdVol']
                    dic['totalmoney'] = info['trdAmt']
                    dic['tradedate'] = info['searchDate']

                    mysql_st.insertdb(db,dic)
                    logger.info("处理date:%s成功", mydate)

        datestart = datestart + datetime.timedelta(days=1)

    return


start="2018-08-23"
end="2018-09-16"
logger.info("开始爬取数据 start:%s,end:%s",start,end)
get_content_sh(start,end)