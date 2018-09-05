# -*- coding: UTF-8 -*-
import urllib2
import re
import datetime
import json
import logging
import time
import mysql_st

##抓取深圳证券所大盘数据
FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)
handler = logging.FileHandler('sz.log')  ##使用handler输出不同目的地
handler.setFormatter(logging.Formatter(FORMAT))
logger = logging.getLogger(__name__)
logger.addHandler(handler)

typedic = {"1":"上海A股","2":"深圳市场","3":"深圳主板","4":"中小板","5":"创业板"}

def get_content_sz(start,end):
    db = mysql_st.connectdb();
    header = {'Referer': 'http://www.szse.cn/market/stock/indicator/index.html',
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3418.2 Safari/537.36'}

    datestart = datetime.datetime.strptime(start, '%Y-%m-%d')
    dateend = datetime.datetime.strptime(end, '%Y-%m-%d')
    while datestart <= dateend:
        mydate = datestart.strftime('%Y-%m-%d')
        for i in range(1,5):
            url="http://www.szse.cn/api/report/ShowReport/data?SHOWTYPE=JSON&CATALOGID=1803&TABKEY=tab"+str(i)+"&txtQueryDate="+mydate+"&random=0.024759974907214488"
            req = urllib2.Request(url, headers=header)
            try:
                url_content = urllib2.urlopen(req).read().decode('utf-8')
            except Exception:
                logging.info("请求深交所url失败,date:%s，tab:%s", mydate,i)
            else:
                havedata=False
                # result = url_content[url_content.find('{'):len(url_content) - 1]
                obj = json.loads(url_content, encoding='utf-8')
                for info in obj:
                    metadata = info['metadata']
                    if info['data'] == "" or len(info['data'])==0:
                        # logging.info("日期%s该板块%s没有数据",mydate,metadata['name'])
                        continue
                    dic={}
                    if metadata['tabkey'] == "tab1":  ##深圳市场
                        havedata = True
                        dic['type'] = "2"
                        dic['typename']=typedic['2']
                        dic['totalnum'] = 0
                        dic['tradedate'] = metadata['subname']
                        data = info['data']
                        dic['pe'] = "0.00"
                        for entity in data:
                            if entity['zbmc'] =="股票平均市盈率":
                                dic['pe'] = entity['brsz']
                            if entity['zbmc'] =="股票总市值（亿元）":
                                dic['totalvalue'] = str(entity['brsz']).replace(",","")
                            if entity['zbmc'] == "股票成交金额（亿元）":
                                dic['totalmoney'] = str(entity['brsz']).replace(",","")
                    if metadata['tabkey'] == "tab2":  ##深圳主板
                        havedata = True
                        dic['type'] = "3"
                        dic['typename']=typedic['3']
                        dic['tradedate'] = metadata['subname']
                        data = info['data']
                        dic['pe'] = "0.00"
                        for entity in data:
                            if entity['indicator'] =="股票平均市盈率":
                                dic['pe'] = str(entity['today']).replace(",","")
                            if entity['indicator'] =="平均市盈率(倍)":
                                dic['pe'] = str(entity['today']).replace(",","")
                            if entity['indicator'] =="上市公司市价总值(亿元)":
                                dic['totalvalue'] =str(entity['today']).replace(",","")
                            if entity['indicator'] == "总成交金额(亿元)":
                                dic['totalmoney'] = str(entity['today']).replace(",","")
                            if entity['indicator'] == "总成交股数(亿股)":
                                dic['totalnum'] = float(str(entity['today']).replace(",",""))*10000
                    if metadata['tabkey'] == "tab3":  ##中小板
                        havedata = True
                        dic['type'] = "4"
                        dic['typename']=typedic['4']
                        dic['tradedate'] = metadata['subname']
                        data = info['data']
                        dic['pe'] = "0.00"
                        for entity in data:
                            if entity['indicator'] =="平均市盈率(倍)":
                                dic['pe'] = str(entity['today']).replace(",","")
                            if entity['indicator'] =="上市公司市价总值(亿元)":
                                dic['totalvalue'] = str(entity['today']).replace(",","")
                            if entity['indicator'] == "总成交金额(亿元)":
                                dic['totalmoney'] = str(entity['today']).replace(",","")
                            if entity['indicator'] == "总成交股数(亿股)":
                                dic['totalnum'] = float(str(entity['today']).replace(",",""))*10000
                    if metadata['tabkey'] == "tab4":  ##创业板
                        havedata = True
                        dic['type'] = "5"
                        dic['typename']=typedic['5']
                        dic['tradedate'] = metadata['subname']
                        data = info['data']
                        dic['pe']="0.00"
                        for entity in data:
                            if entity['indicator'] =="平均市盈率(倍)":
                                dic['pe'] = str(entity['today']).replace(",","")
                            if entity['indicator'] =="上市公司市价总值(亿元)":
                                dic['totalvalue'] = str(entity['today']).replace(",","")
                            if entity['indicator'] == "总成交金额(亿元)":
                                dic['totalmoney'] = str(entity['today']).replace(",","")
                            if entity['indicator'] == "总成交股数(亿股)":
                                dic['totalnum'] =float(str(entity['today']).replace(",",""))*10000

                    mysql_st.insertdb(db,dic)
                    logger.info("处理date:%s成功", mydate)
                if havedata==False:
                    logger.info("该日%s没有数据",mydate)
        datestart = datestart + datetime.timedelta(days=1)

    return

if __name__=="__main__":
    start="2018-08-24";end="2018-09-01"
    begin = datetime.datetime.today()
    logger.info("%s,开始爬取数据 start:%s,end:%s",datetime.datetime.today(),start,end)
    get_content_sz(start,end)
    logger.info("爬取结束,start:%s,end:%s",begin,datetime.datetime.today())