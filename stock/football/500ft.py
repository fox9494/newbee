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
# logger.addHandler(handler)

logger2 = logging.getLogger("mylog")
logger2.addHandler(handler)


dic={"1072":"曼城","1075":"曼联","1238":"热刺","1011":"利物浦","1173":"切尔西","554":"阿森纳","700":"伯恩利",
     "565":"埃佛顿","973":"莱切","1137":"纽卡斯尔","516":"水晶宫","667":"伯恩茅斯","1286":"西汉姆联",
     "1274":"沃特福德","847":"哈德斯","721":"布莱顿","1128":"南安普顿","511":"斯旺西","1197":"斯托克"}

season={'9848':'16-17赛季','11734':'17-18赛季'}
def get_content_sh(start,end):
    # db = mydb.connectdb();
    header = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    for(j,h) in season.items():
      for (k,v) in dic.items():
        url = "http://liansai.500.com/index.php?c=score&a=getOneTeam&stid={}&teamId={}".format(j,k)
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
            match_num=0

            left=0
            left_num=0.0

            draw_num=0.0
            draw_total=0
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
                        logger.info("一个正盘,{} vs{},比分:{}-{},赔率:{}:{}:{}".format(host_name,guest_name,host_goal,guest_goal,win,draw,lost))
                        right=right+1
                        win_num=win_num+float(win)-1

                    if (host_goal == guest_goal and isdrawMin == True):
                        logger.info(
                            "一个正盘,{} vs{},比分:{}-{},赔率:{}:{}:{}".format(host_name, guest_name, host_goal, guest_goal, win,
                                                                       draw, lost))
                        win_num = win_num + float(draw) - 1
                        right=right+1

                    if (host_goal < guest_goal and isLostMin == True):
                        logger.info(
                            "一个正盘,{} vs{},比分:{}-{},赔率:{}:{}:{}".format(host_name, guest_name, host_goal, guest_goal, win,
                                                                       draw, lost))
                        win_num = win_num + float(lost) - 1
                        right = right + 1

                    if (host_goal > guest_goal and isWinMin == False):
                        logger.info(
                            "一个反盘,{} vs{},比分:{}-{},赔率:{}:{}:{}".format(host_name, guest_name, host_goal, guest_goal, win,
                                                                       draw, lost))
                        left = left + 1
                        left_num = left_num + float(win) - 1

                    # if (host_goal == guest_goal and isdrawMin == False):
                    #     logger.info(
                    #         "一个反盘,{} vs{},比分:{}-{},赔率:{}:{}:{}".format(host_name, guest_name, host_goal, guest_goal, win,
                    #                                                    draw, lost))
                    #     left_num = left_num + float(draw) - 1
                    #     left = left + 1

                    if (host_goal == guest_goal and isdrawMin == False):
                        logger.info("一个平盘,{} vs{},比分:{}-{},赔率:{}:{}:{}".format(host_name, guest_name, host_goal, guest_goal, win,
                                                                       draw, lost))
                        draw_num = draw_num + float(draw) - 1
                        draw_total = draw_total + 1

                    if (host_goal < guest_goal and isLostMin == False):
                        logger.info("一个反盘,{} vs{},比分:{}-{},赔率:{}:{}:{}".format(host_name, guest_name, host_goal, guest_goal, win,
                                                                       draw, lost))
                        left_num = left_num + float(lost) - 1
                        left = left + 1

                    match_num=match_num+1
                    # logger.info("处理date:%s成功", match)

            if match_num>0:
                logger2.info("赛季:{},队伍:{}".format(h,dic[k]))
                logger2.info("累计正盘盈利:{},正盘数量:{},损失:{},比赛场次:{},比率:{}".format(win_num,right,match_num-right,match_num,float(right)/match_num))
                logger2.info("累计反盘盈利:{},反盘数量:{},损失:{},比赛场次:{},比率:{}".format(left_num, left,match_num-left, match_num,float(left)/match_num))
                logger2.info("累计平盘盈利:{},平盘数量:{},损失:{},比赛场次:{},比率:{}".format(draw_num, draw_total, match_num-draw_total,match_num,float(draw_total)/match_num))


    return


if __name__=="__main__":
    start="2018-08-23"
    end="2018-09-01"
    logger.info("开始爬取数据 start:%s,end:%s",start,end)
    get_content_sh(start,end)