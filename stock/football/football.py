# -*- coding: UTF-8 -*-
import urllib2
import re
import datetime
import json
import logging
import time
import requests
import stock.mysql_st as mydb

##足彩数据

FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)
handler = logging.FileHandler('sh.log')  ##使用handler输出不同目的地
handler.setFormatter(logging.Formatter(FORMAT))
logger = logging.getLogger(__name__)
logger.addHandler(handler)




def get_content_sh(start,end):
    db = mydb.connectdb();
    header = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    datestart = datetime.datetime.strptime(start, '%Y-%m-%d')
    dateend = datetime.datetime.strptime(end, '%Y-%m-%d')
    while datestart <= dateend:
        mydate = datestart.strftime('%Y-%m-%d')
        url = "http://odds.zgzcw.com/odds/oyzs_ajax.action"
        datas={"type":"jc",
            "issue":"2018-09-04",
            "date":"2018-08-05",
            "companys":"4,9"}
        # req = urllib2.Request(url,json.dumps(datas),headers=header)
        try:
            url_content = requests.post(url,data=datas)
            # url_content = urllib2.urlopen(req).read().decode('utf-8')

            result = json.loads(url_content.content)
        except Exception:
            logger.exception("请求足球url失败,date:%s", mydate)
            return
        else:
            for match in result:
                    league_name=match["LEAGUE_NAME_SIMPLY"]
                    match_time=match["MATCH_TIME"]
                    host_name=match["HOST_NAME"]
                    host_goal=match["HOST_GOAL"]
                    guest_name = match["GUEST_NAME"]
                    guest_goal = match["GUEST_GOAL"]
                    source_match_id=match["SOURCE_MATCH_ID"]

                    # mydb.insertdb(db,dic)
                    odds = match["listOdds"]
                    for odd in odds:
                        source_match_id = odd["SOURCE_MATCH_ID"]
                        company_name=odd["COMPANY_NAME"]
                        first_win=odd["FIRST_WIN"]
                        first_same=odd["FIRST_SAME"]
                        first_lost=odd["FIRST_LOST"]
                        win=odd["WIN"]
                        same=odd["SAME"]
                        lost=odd["LOST"]
                    logger.info("处理date:%s成功", mydate)

        datestart = datestart + datetime.timedelta(days=1)

    return


start="2018-08-23"
end="2018-09-01"
logger.info("开始爬取数据 start:%s,end:%s",start,end)
get_content_sh(start,end)