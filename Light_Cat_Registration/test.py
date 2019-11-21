# -*- coding: utf-8 -*-
import re
from LoginNatshell import Login,getpwd
from LoginPanabit  import flowNumber
from qqbot import qqbotsched
from addressDic import addressDic

#正则规则
add = (r'宏云|华鼎|巴士|波阳路|博达|'
       '富荣|高宝|华舟|金汇|金融街|'
       '凯迪克|联峰汇|林顿|芦恒路|'
       '美丽园|明园|内外联|时代|'
       '天瑞|天祥|天源|鑫和|亚都|'
       '裕安|兆成|中汇|中谊|中友|'
       '紫安|汇嘉')
num = (r'[0-9a-zA-Z\_\-]+')
wuye = "%E7%89%A9"
def onQQMessage(content):
#判断是否是机器人发的消息,如果是不做回应.
    #初级匹配 匹配关键字 查
    if re.search(r"查", content):
    #次级匹配,匹配具体大楼
      if re.findall(add,content):
         addr = re.findall(add,content)
         address = addr[0]         
    #次级匹配 匹配门牌号
         if re.findall(num,content):
    #次级匹配 解析门牌号
           resul = re.findall(num,content)
           result = resul[0]
           resultArray = Login(result,addressDic[address])
           if resultArray:
             for index in resultArray:
                 print (index)
           else:
                 print ("None")
         elif re.search(r"物",content):
           resultArray = Login(wuye,addressDic[address])
           print (resultArray)
         else:
           print ("没有匹配到")



if __name__ == '__main__':
    onQQMessage("查宏云10")
