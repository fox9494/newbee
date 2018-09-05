# -*- coding: UTF-8 -*-
import urllib2
import json
import time
import hashlib

##功能 :调用音乐push

timestamp=int(round(time.time()*1000))

appId="SKbwoq0xEe6SgkwvTzOAA6"
AppSecret="aowJcGTaSf64BV1AR3bXx5"
AppKey="JLZzdxb1qZ7SqlIxur2K18"
pushChannel="1"

pushContent="咪咕音乐欢迎你"
taskId=str(timestamp)

content_ojb={   "imgUrl": "",
                "pushContent": pushContent,
                "pushCreateTime": int(round(time.time()*1000)),
                "pushLinkType": 100,
                "pushLinkAddress": "mgmusic://album-info?id=1106188088",
                "pushTitle": "测试标题",
                "pushType": 100  }

content = "MIGU"+"\n"+taskId+"\n"+pushChannel+"\n"+pushContent+"\n"+str(timestamp)+"\n"+AppSecret+"\n"
m = hashlib.md5()
m.update(content)

Authorization  = AppKey+":"+m.hexdigest()

header = {
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3418.2 Safari/537.36',
          'Content-Type': 'application/json;charset=UTF-8',
          'timestamp':str(timestamp),
          'Authorization':Authorization
          }

uid=['383d3698-e7c4-443e-b768-2bebaf000344']
data={"appId":"SKbwoq0xEe6SgkwvTzOAA6","taskId":taskId,"topic":"测试推送","isSync":"false",
      "content":content_ojb,"pushChannel":pushChannel,"uid":None,"cid":None,"did":['867635030420306'],
      "policy":{"isOffline":None, "offlineExpireTime":None,"pushNetWorkType":None, "platform" :["ANDROID", "IOS"],
                  "region" :None, "tag":None, "broadcast":False, "speed":None, "freeTimePeriod":'null'},
      "extra":None
      }



json_data=json.dumps(data)
url = "http://218.200.160.98:18089/api/push.do"
request = urllib2.Request(url,json_data,headers=header)

url_content = urllib2.urlopen(request).read().decode('utf-8')
print url_content