# -*- coding: utf-8 -*-
import re
from LoginNatshell import Login,getpwd,getmark
from LoginPanabit  import flowNumber
from qqbot import qqbotsched
from addressDic import addressDic
from areaID_To_OLT import  areaID_To_OLTDic
from OLT_sh_search import autoRegister,autoRegisterComfirm
#正则规则
add = (r'宏云|华鼎|巴士|波阳路|博达|'
        '富荣|高宝|华舟|金汇|金融街|'
        '凯迪克|联峰汇|林顿|芦恒路|'
        '美丽园|明园|内外联|时代|'
        '天瑞|天祥|天源|鑫和|亚都|'
        '裕安|兆成|中汇|中谊|中友|'
        '紫安|汇嘉|嘉利|金宏|新海')
num = (r'[0-9a-zA-Z\_\-]+')
wuye = "%E7%89%A9"
adaccount = r"[0-9a-zA-Z]{2,20}"
ontSN = r"([0-9A-Z]{4}\-[0-9A-Z]{4}\-[0-9A-Z]{4})"
def onQQMessage(bot, contact, member, content):
    if bot.isMe(contact,member):
       print ("is Me")
    else:
       #初级匹配 匹配关键字 查
       if re.search(r"查", content):
          #bot.SendTo(contact,"匹配到查")
          if re.findall(add,content):
            #bot.SendTo(contact,"匹配大厦名称")
            addr = re.findall(add,content)
            address = addr[0]
       #次级匹配 匹配门牌号
            if re.findall(r"物",content):
               resultArray = Login(wuye,addressDic[address])
               resultList(bot,contact,resultArray)
            if re.findall(num,content):
              #bot.SendTo(contact,"匹配到门牌号")
              #次级匹配 解析门牌号
              result = re.findall(num,content)
              #result [0] = ME , result[1] = 门牌号 ,需要把门牌号的数值,传给Login method
              resultArray = Login(result[0],addressDic[address])
              resultList(bot,contact,resultArray)
       #输入账号返回对应信息
       if re.search(r"注册", content):
           if re.findall(ontSN,content):
               ontList = re.findall(ontSN,content)
               SN = ontList[0]
               #print (ontList)
               if re.findall(adaccount,content):
                  account =reAccount(adaccount,content)
                  host = hostByaccount(account)
                  result_autoRegister = autoRegister(account,host,SN)
                  bot.SendTo(contact,result_autoRegister)
           elif re.findall(adaccount,content):
               account =reAccount(adaccount,content)
               #下三句是得到host
               userDic = getpwd(account)
               print (userDic)
               areaID = userDic["data"]["areaid"]
               host = areaID_To_OLTDic[areaID]
               ontDic = autoRegisterComfirm(account,host) 
               #print (ontDic)
               resultList(bot,contact,ontDic)
               bot.SendTo(contact,"使用以下格式注册:\r\n注册+账号+逗号+MAC地址\r\n例:\r\n注册ad02128007,30D1-7E6B-524C")
               #markDic = getmark(account)
               #print (markDic)
               #userDic = getpwd(content)
               #areaID = userDic["data"]["areaid"]
               #host = areaID_To_OLTDic[areaID]
               #autoSearch(markDic,host,account)
               #print (areaID)
               #print (host)
               #bot.SendTo(contact,"密码: "+password)
       #匹配账号 返回密码
       if content == '连接数':
          flow = flowNumber()
          if flow > 100000:
            bot.SendTo(contact,"目前连接数异常,连接数:"+str(flow))
          else:
            bot.SendTo(contact,"目前连接数没有异常,连接数:"+str(flow))

#用于返回目标host 实际OLT_IP地址
def hostByaccount(account):
    userDic = getpwd(account)
    #print (userDic)
    areaID = userDic["data"]["areaid"]
    host = areaID_To_OLTDic[areaID]
    return host


#用于匹配用户账号
def reAccount(adaccount,content):
     accountList = re.findall(adaccount,content)
     account = accountList[0]
     #userDic = getpwd(account)
     #areaID = userDic["data"]["areaid"]
     #host = areaID_To_OLTDic[areaID]
     #ontDic = autoRegisterComfirm(account,host) 
     #return ontDic
     return account

#结果列表负责输出结果
def resultList(bot,contact,Array):
    resultArray = Array
    if resultArray:
       for index in resultArray:
         bot.SendTo(contact,index)
    else:
       bot.SendTo(contact,"小哥哥,没有你要的结果")


#连接数,计划任务
'''
@qqbotsched(minute="0-55/5")
def mytask1(bot):
    gl = bot.List("group","云端上海ISP楼宇交流群")
    if gl is not None:
       for group in gl:
           flow = flowNumber()
           if flow > 110000:
             bot.SendTo(group,"异常,大于11万连接数:"+str(flow))
'''
