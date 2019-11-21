# -*- coding: utf-8 -*-
import re
from LoginNatshellone import Login,getpwd
from LoginPanabitone  import flowNumber
from qqbot import qqbotsched

def onQQMessage(bot, contact, member, content):
#判断是否是机器人发的消息,如果是不做回应.
    #初级匹配 匹配关键字 查/看/在/猫
    if re.search(r"查", content):
    #次级匹配 匹配门牌号
       if re.findall(r"[0-9a-zA-Z\_\-]+",content):
    #次级匹配 解析门牌号
         result = re.findall(r"[0-9a-zA-Z\_\-]+",content)
         #result [0] = ME , result[1] = 门牌号 ,需要把门牌号的数值,传给Login method
         #print (result[1])
    #把解析结果传给蓝海登陆模块
         resultArray = Login(result[0])
         if resultArray:
           for index in resultArray:
                bot.SendTo(contact,index)
         else:
               bot.SendTo(contact,"Hi,小哥哥,没有你要的结果")
   #匹配账号 返回密码
    if bot.isMe(contact,member):
       print ("is me")
    else:
        if re.search(r"ad[0-9a-zA-Z]{2,20}",content):
             password = (getpwd(content))
             bot.SendTo(contact,"密码: "+password)
    if content == '连接数':
       flow = flowNumber()
       if flow > 110000:
         bot.SendTo(contact,"异常,大于11万,连接数:"+str(flow))
       else:
         bot.SendTo(contact,"正常,连接数:"+str(flow))
         print ("目前连接数没有异常",flow)


@qqbotsched(minute="0-55/5")
def mytask1(bot):
    gl = bot.List("group","云端上海ISP楼宇交流群")
    if gl is not None:
       for group in gl:
           flow = flowNumber()
           if flow > 110000:
             bot.SendTo(group,"异常,大于11万连接数:"+str(flow))

