# -*- coding: UTF-8 -*-
##csv 文件操作举例
import csv
import logging

if __name__=="__main__":
    FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(format=FORMAT, level=logging.DEBUG)
    logging.info("开始运行")

    out = file('Stu_csv.csv','wb')  ##wb模式不空行
    csv_write = csv.writer(out)
    headers = ['id', 'username', 'password', 'age', 'country']
    csv_write.writerow(headers)
    rows = [(1001,'qiye','qiye_pass',20,'china'),(1002,'mary','mary_pass',23,'usa')]
    csv_write.writerows(rows)
    out.close()
    logging.info("写csv结束")

    logging.info("开始读csv文件")
    file = open("Stu_csv.csv","r")
    csv_reader = csv.reader(file)
    for row in csv_reader:
        logging.info("the csv value:{}".format(row))
