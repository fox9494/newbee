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
handler = logging.FileHandler('500.log')  ##使用handler输出不同目的地
handler.setFormatter(logging.Formatter(FORMAT))
logger = logging.getLogger(__name__)
logger.addHandler(handler)




def get_content_sh(start,end):
    # db = mydb.connectdb();
    header = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    url = "http://liansai.500.com/index.php?c=score&a=getOneTeam&stid=11734&teamId=511"
    try:
        req = urllib2.Request(url, headers=header)
        url_content = urllib2.urlopen(req).read().decode('utf-8')
        result = json.loads(url_content, encoding='utf-8')
    except Exception:
        logger.exception("请求足球url失败,url:%s", url)
        return
    else:
        win_num=0.0
        right=0
        for match in result:
                gid=match["gid"]
                host_name=match["hname"]
                host_goal=match["hscore"]
                guest_name = match["gsxname"]
                guest_goal = match["gscore"]

                match_time=match["stime"]

                # mydb.insertdb(db,dic)
                list=[]
                win=match["win"]
                list.append(win)
                draw=match["draw"]
                list.append(draw)
                lost=match["lost"]
                list.append(lost)

                isWinMin=False
                if(win==min(list)):
                    isWinMin=True

                isdrawMin = False
                if (draw == min(list)):
                    isdrawMin = True

                isLostMin = False
                if (lost == min(list)):
                    isLostMin = True

                if (host_goal>guest_goal and isWinMin==True):
                    logger.info("一个正盘,{}".format(match))
                    right=right+1
                    win_num=win_num+float(win)-1

                if (host_goal == guest_goal and isdrawMin == True):
                    logger.info("一个正盘,{}".format(match))
                    win_num = win_num + float(draw) - 1
                    right=right+1

                if (host_goal < guest_goal and isLostMin == True):
                    logger.info("一个正盘,{}".format(match))
                    win_num = win_num + float(lost) - 1
                    right = right + 1

                logger.info("处理date:%s成功", match)

        logger.info("累计正盘盈利:{},正盘数量:{},损失:{}".format(win_num,right,38-right))


    return


if __name__=="__main__":
    start="2018-08-23"
    end="2018-09-01"
    logger.info("开始爬取数据 start:%s,end:%s",start,end)
    get_content_sh(start,end)