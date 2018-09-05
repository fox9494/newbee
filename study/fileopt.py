# -*- coding: UTF-8 -*-
##IO 文件操作举例
import chardet

if __name__=="__main__":
    file = open("io.txt","w")
    file.write("some thing 我得文字,what are you   !")
    file = open("io.txt","rb")
    pos=10
    while True:
        content = file.read(pos)
        if content=='':#判断文件结束
            break
        print content
    file.close()
