# -*- coding: UTF-8 -*-
import MySQLdb.cursors
import logging
import sys
import datetime

reload(sys)
sys.setdefaultencoding('utf8')

FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)
handler = logging.FileHandler('music.log')  ##使用handler输出不同目的地
formatter = logging.Formatter(FORMAT)
handler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.addHandler(handler)

def execute():
    connect = MySQLdb.connect("172.20.78.91", "root", "123456", "eagle2.0", charset='utf8',
                              cursorclass=MySQLdb.cursors.DictCursor);
    # connect = MySQLdb.connect("172.20.78.57", "root", "root", "portrait", charset='utf8',
    #                           cursorclass=MySQLdb.cursors.DictCursor);
    cursor = connect.cursor()
    sql = "select * from migu_tag_enum"
    try:
        cursor.execute(sql)
        for row in cursor:
                sql_insert = "insert into migu_tag_attribute_enum_relation(tag_id,enum_pid,create_time)" \
                             " value({},{},'{}')".format(row["enum_father"],row["id"],datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                cursor.execute(sql_insert)
                connect.commit()
                logger.info("插入数据成功,%s,%s", row["enum_father"], row["id"])
    except Exception:
      logger.exception("执行失败")
      connect.rollback()
    connect.close()


if __name__=="__main__":
    execute()
