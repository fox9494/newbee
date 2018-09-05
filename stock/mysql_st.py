#!/usr/bin/python
# -*- coding: UTF-8 -*-

import MySQLdb
import MySQLdb.cursors
import logging
import datetime
import time
import sys
import csv


reload(sys)
sys.setdefaultencoding('utf8')
ip="127.0.0.1"

# ip="172.20.78.57"



def connectdb():
    logging.info('连接到mysql服务器...')
    db = MySQLdb.connect(ip, "root", "root", "test", charset='utf8', cursorclass = MySQLdb.cursors.DictCursor);
    logging.info('连接上了!')
    return db

def insertdb(db,dic):
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    date = dic['tradedate']
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S");
    # SQL 插入语句
    sql = "replace into st_market(trade_date,type,type_name,total_value,total_num,total_money,pe,modify_time) " \
          "values('%s','%s','%s','%s','%s','%s','%s','%s') " % \
          (date,dic['type'],dic['typename'],dic['totalvalue'],
           dic['totalnum'],dic['totalmoney'],dic['pe'],now)
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except Exception:
        # Rollback in case there is any error
        logging.exception("插入失败")
        db.rollback()

def insertstock(db,dic):
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    date = dic['date']
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S");
    # SQL 插入语句
    sql = "replace into st_stock(trade_date,code,name,place,pe,pb,ps,price,modify_time) " \
          "values('%s','%s','%s','%s','%s','%s','%s','%s','%s') " % \
          (date,dic['code'],dic['name'],dic['place'],
           dic['pe'],dic['pb'],dic['ps'],dic['price'],now)

    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except Exception:
        # Rollback in case there is any error
        logging.exception("插入失败")
        db.rollback()

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
        csvFile2 = file(filename, 'w')
        writer = csv.writer(csvFile2)
        writer.writerow(['imei','uuid','touchId'])
        for row in cursor:
            userids = str(row[1])
            if userids=="":
                logging.warn("该用户组没有数据,groupid:{}".format(groupid))
                return
            users = userids.split(";")
            if len(users)==0:
                logging.warn("split后没有数据,groupid:{}".format(groupid))
                return
            for single in users:
              user= single.split(",")
              data[0] = user[0]
              data[1] = user[1]
              data[2] = touchid
              writer.writerow(data)
              data=['','','']

              logging.info("the row: {}".format(row))
        csvFile2.close()
    except Exception:
        logging.exception("查询失败")

if __name__=="__main__":
    connect = connectdb();
    queryData(connect,"ab.log",1793,184)
    print "从本模块运行执行此代码"