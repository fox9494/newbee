# -*- coding: UTF-8 -*-
import urllib2
import re
import datetime
import json
import logging
import time
import requests
import  MySQLdb.cursors
import sys

##足彩数据

FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)
handler = logging.FileHandler('500.log')  ##使用handler输出不同目的地
handler.setFormatter(logging.Formatter(FORMAT))
logger = logging.getLogger(__name__)
# logger.addHandler(handler)

logger2 = logging.getLogger("ft.log")
logger2.addHandler(handler)

reload(sys)
sys.setdefaultencoding('utf-8')

connect = MySQLdb.connect("127.0.0.1", "root", "root", "test", charset='utf8',cursorclass=MySQLdb.cursors.DictCursor);

"""
#胜负表
CREATE TABLE `t_football_zg` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `match_time` datetime NOT NULL COMMENT '比赛日期',
  `league_name` varchar(50) DEFAULT NULL COMMENT '联赛名称',
  `host_name` varchar(100) DEFAULT NULL COMMENT '主队名称',
  `host_goal` int(11) DEFAULT NULL COMMENT '主队进球数',
  `guest_name` varchar(100) DEFAULT NULL COMMENT '客队名称',
  `guest_goal` int(11) DEFAULT NULL COMMENT '客队进球数',
  `source_match_id` varchar(50) DEFAULT NULL COMMENT '比赛ID',
  `modify_time` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mathch_id` (`source_match_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

#赔率表
CREATE TABLE `t_football_odd` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `source_match_id` varchar(50) DEFAULT NULL COMMENT '比赛ID',
  `company_name` varchar(50) DEFAULT NULL COMMENT '博彩公司名',
  `first_win` decimal(7,4) DEFAULT NULL COMMENT '初始主胜',
  `first_same` decimal(7,4) DEFAULT NULL COMMENT '初始平',
  `first_lost` decimal(7,4) DEFAULT NULL COMMENT '初始主负',
  `win` decimal(7,4) DEFAULT NULL COMMENT '终主胜',
  `same` decimal(7,4) DEFAULT NULL COMMENT '终平',
  `lost` decimal(7,4) DEFAULT NULL COMMENT '终主负',
  `modify_time` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `odd_ft` (`source_match_id`,`company_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



"""

##爬取数据
def get_content_sh(start,end):
    header = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    cursor = connect.cursor()
    datestart = datetime.datetime.strptime(start, '%Y-%m-%d')
    dateend = datetime.datetime.strptime(end, '%Y-%m-%d')
    while datestart <= dateend:
        mydate = datestart.strftime('%Y-%m-%d')
        url = "http://odds.zgzcw.com/odds/oyzs_ajax.action"
        datas={"type":"jc",
            "issue":"2018-09-04",
            "date":mydate,
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

                    odds = match["listOdds"]
                    for odd in odds:
                        if odd.has_key("SOURCE_MATCH_ID")==False:#可能没有公司的赔率，只有一个名称
                            continue
                        source_match_id = odd["SOURCE_MATCH_ID"]
                        company_name=odd["COMPANY_NAME"]
                        if odd.has_key("FIRST_WIN") == True:
                           first_win=odd["FIRST_WIN"]
                        if odd.has_key("FIRST_SAME") == True:
                           first_same=odd["FIRST_SAME"]
                        if odd.has_key("FIRST_LOST") == True:
                           first_lost=odd["FIRST_LOST"]
                        if odd.has_key("WIN") == True:
                           win=odd["WIN"]
                        if odd.has_key("SAME") == True:
                           same=odd["SAME"]
                        if odd.has_key("LOST") == True:
                           lost=odd["LOST"]
                        sql = "replace into t_football_odd(source_match_id,company_name,first_win,first_same,first_lost,win,same,lost,modify_time) " \
                              "values('%s','%s','%s','%s','%s','%s','%s','%s','%s') " % \
                              (source_match_id, company_name, first_win, first_same,first_lost,
                               win, same,lost, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                        cursor.execute(sql)
                        connect.commit()
                        logger.info("处理日期{},主队{}vs客队{}赔率成功,公司:{}".format(mydate,host_name,guest_name,company_name))
                        sql = "replace into t_football_zg(match_time,league_name,host_name,host_goal,guest_name,guest_goal,source_match_id,modify_time) " \
                              "values('%s','%s','%s','%s','%s','%s','%s','%s') " % \
                              (match_time, league_name, host_name, host_goal, guest_name,
                               guest_goal, source_match_id, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    cursor.execute(sql)
                    connect.commit()
                    logger.info("处理日期{},主队{}vs客队{}胜负成功".format(mydate, host_name, guest_name))


        datestart = datestart + datetime.timedelta(days=1)

    return

##分析数据
def  get_analysis(league_name,name,start,end,company_name):
    cursor = connect.cursor()
    # sql = "select match_time,host_name,host_goal,guest_name,guest_goal,company_name," \
    #       "first_win,first_same,first_lost,win,same,lost from t_football_zg a,t_football_odd b " \
    #       "where a.source_match_id=b.source_match_id and league_name='{}' " \
    #       "and company_name='{}' and (host_name='{}' or guest_name='{}') and match_time>='{}' and match_time<='{}' order by match_time;".\
    #     format(league_name,company_name,name,name,start,end)

    sql = """select
    match_time, host_name, host_goal, guest_name, guest_goal, company_name, first_win, first_same, first_lost, win, same, lost from t_football_zg a, t_football_odd b
    where a.source_match_id = b.source_match_id and company_name = '{}'""".format(company_name)

    if league_name != None:
        sql = sql + "and league_name='{}' ".format(league_name)
    if name!=None:
        sql = sql + " and (host_name='{}' or guest_name='{}')".format(name,name)
    sql = sql+" order by match_time"

    # sql="select match_time,host_name,host_goal,guest_name,guest_goal,company_name,first_win,first_same,first_lost,win,same,lost " \
    #     "from t_football_zg a,t_football_odd b where a.source_match_id=b.source_match_id and company_name='{}' order by match_time".format(company_name)
    cursor.execute(sql)
    win_num = 0.0
    right = 0
    left = 0
    left_num = 0.0
    draw_num = 0.0
    draw_total = 0
    match_num = 0
    for row in cursor:
        host_name = row["host_name"]
        host_goal = row["host_goal"]
        guest_name = row["guest_name"]
        guest_goal = row["guest_goal"]
        match_time = row["match_time"]
        company_name = row["company_name"]
        first_win = row["first_win"]
        first_same = row["first_same"]
        first_lost = row["first_lost"]
        list = []
        list.append(first_win)
        list.append(first_same)
        list.append(first_lost)

        isWinMin = False
        if (first_win == min(list)):
            isWinMin = True

        isdrawMin = False
        if (first_same == min(list)):
            isdrawMin = True

        isLostMin = False
        if (first_lost == min(list)):
            isLostMin = True

        if (host_goal > guest_goal and isWinMin == True):
            logger.info("一个正盘,时间:{},{} vs{},比分:{}-{},赔率:{}:{}:{}".format(match_time,host_name, guest_name, host_goal, guest_goal, first_win, first_same, first_lost))
            right = right + 1
            win_num = win_num + float(first_win) - 1

        if (host_goal == guest_goal and isdrawMin == True):
            logger.info(logger.info("一个正盘,时间:{},{} vs{},比分:{}-{},赔率:{}:{}:{}".format(match_time,host_name, guest_name, host_goal, guest_goal, first_win, first_same, first_lost)))
            win_num = win_num + float(first_same) - 1
            right = right + 1

        if (host_goal < guest_goal and isLostMin == True):
            logger.info(logger.info("一个正盘,时间:{},{} vs{},比分:{}-{},赔率:{}:{}:{}".format(match_time,host_name,guest_name, host_goal, guest_goal, first_win, first_same, first_lost)))
            win_num = win_num + float(first_lost) - 1
            right = right + 1

        if (host_goal > guest_goal and isWinMin == False):
            logger.info("一个反盘,时间:{},{} vs{},比分:{}-{},赔率:{}:{}:{}".format(match_time,host_name, guest_name, host_goal, guest_goal, first_win, first_same, first_lost))
            left = left + 1
            left_num = left_num + float(first_win) - 1

        if (host_goal == guest_goal and isdrawMin == False):
            logger.info("一个平盘,时间:{},{} vs{},比分:{}-{},赔率:{}:{}:{}".format(match_time,host_name, guest_name, host_goal,
                                                                         guest_goal, first_win, first_same, first_lost))
            draw_num = draw_num + float(first_same) - 1
            draw_total = draw_total + 1

        if (host_goal < guest_goal and isLostMin == False):
            logger.info("一个反盘,时间:{},{} vs{},比分:{}-{},赔率:{}:{}:{}".format(match_time,host_name, guest_name, host_goal,
                                                                         guest_goal, first_win, first_same, first_lost))
            left_num = left_num + float(first_lost) - 1
            left = left + 1
        match_num = match_num + 1
    if match_num > 0:
        logger2.info("start:{},end:{},队伍:{}".format(start,end,name))
        logger2.info("累计正盘盈利:{},正盘数量:{},损失:{},比赛场次:{},比率:{}".format(win_num, right, match_num - right, match_num,
                                                                    float(right) / match_num))
        logger2.info("累计反盘盈利:{},反盘数量:{},损失:{},比赛场次:{},比率:{}".format(left_num, left, match_num - left, match_num,
                                                                    float(left) / match_num))
        logger2.info(
            "累计平盘盈利:{},平盘数量:{},损失:{},比赛场次:{},比率:{}".format(draw_num, draw_total, match_num - draw_total, match_num,
                                                           float(draw_total) / match_num))

if __name__=="__main__":
    start="2017-05-01"
    end="2018-09-19"
    # logger.info("开始爬取数据 start:%s,end:%s",start,end)
    # get_content_sh(start,end)

    logger.info("开始计算数据 start:%s,end:%s", start, end)
    # get_analysis("意甲","尤文图斯",start, end,"立博")

    get_analysis("欧罗巴杯", "波尔多", start, end, "威廉希尔")
    connect.close()
