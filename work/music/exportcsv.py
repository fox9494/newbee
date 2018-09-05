# -*- coding: UTF-8 -*-
import MySQLdb.cursors
import logging
import sys
import csv

reload(sys)
sys.setdefaultencoding('utf8')

FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)
handler = logging.FileHandler('music.log')  ##使用handler输出不同目的地
formatter = logging.Formatter(FORMAT)
handler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.addHandler(handler)

def connectdb():
    logging.info('连接到mysql服务器...')
    connect = MySQLdb.connect("172.20.78.57", "root", "root", "qrqmdb", charset='utf8',cursorclass=MySQLdb.cursors.SSCursor);
    logger.info('连接上了!')
    return connect

def queryData(connect,filename,groupid,strategyid):
    cursor = connect.cursor()

    sql = "select * from migu_user_group_detail where group_id={}".format(groupid)

    sql_1 = "select * from migu_strategy where id={}".format(strategyid)

    try:
        cursor.execute(sql_1)
        data = ['','','']
        touchid=""
        for row in cursor:
            touchid = str(row[3])

        cursor.execute(sql)
        csvFile2 = file(filename, 'w')  # 设置newline，否则两行之间会空一行
        writer = csv.writer(csvFile2)
        writer.writerow(['imei','uuid','touchId'])
        for row in cursor:
            userids = str(row[1])
            if userids=="":
                logger.warn("该用户组没有数据,groupid:{}".format(groupid))
                return
            users = userids.split(";")
            if len(users)==0:
                logger.warn("split后没有数据,groupid:{}".format(groupid))
                return
            for single in users:
              user= single.split(",")
              data[0] = user[0]
              data[1] = user[1]
              data[2] = touchid
              writer.writerow(data)
              data=['','','']

            logger.info("the row: {}".format(row))
        csvFile2.close()
    except Exception:
        logger.exception("查询失败")
        connect.rollback()

groupid = 1803
strateid=184
filename="my.csv"
connect = connectdb();
queryData(connect,filename,groupid,strateid)
connect.close()
