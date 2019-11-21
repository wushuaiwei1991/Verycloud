#coding:utf-8
import urllib
import http.cookiejar
import re
import json
import time

BaseURL = "http://10.30.20.6:7788"
#BaseURL && API
LoginURL = "/login_check.php"

#主页API
indexURL = "/index.php"
#根据地址查询账号
getofaccoundbyaddress = "/user.php?address="
regionsonid = "regionsonid="
#查询用户具体信息
user = "/user_edit.php?"

#登录账号信息
postdata =urllib.parse.urlencode({	
"username":"admin",
#"pwd":"yifan1018"
"pwd":"yexi2018"
}).encode('utf-8')

'''
#获取cookie
req = urllib.request.Request(BaseURL+LoginURL,postdata)

#自动记住cookie
cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
r = opener.open(req)	

#获取cookie 
req = urllib.request.Request(BaseURL+LoginURL,postdata)

#自动记住cookie
cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
#获取到cookie
r = opener.open(req)
'''


#用于存档
t = time.strftime("%Y-%m-%d_%H:%M:%S->", time.localtime())

def Login(InsertAddress,AreaID):
       #获取cookie
        req = urllib.request.Request(BaseURL+LoginURL,postdata)

#自动记住cookie
        cj = http.cookiejar.CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
        r = opener.open(req)	

#获取cookie 
        req = urllib.request.Request(BaseURL+LoginURL,postdata)

#自动记住cookie
        cj = http.cookiejar.CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
#获取到cookie
        r = opener.open(req)
        #携带cookie 发送请求
        r = opener.open(BaseURL+getofaccoundbyaddress+str(InsertAddress)+"&"+regionsonid+str(AreaID))
        #打印结果
        result = (r.read().decode('utf-8'))

	#正则部分
        pattern_account_first = r">(ad[0-9]+)"
        pattern_name_first = r"\"jmpz_name\">([0-9\u4e00-\u9fa5]{2,7})"
        pattern_address_first =r"\"jmpz_address\">[u\4e00-\u9fa5]{2,20}.[u\4e00-\u9fa5]{2,20}..[u\4e00-\u9fa5]{2,20}.([u\4e00-\u9fa5]{2,20}.[0-9a-zA-Z\-]{2,20}|[0-9a-zA-Z\-]+)"
        pattern_status_first = r"\"jmpz_online\">.img src=.[a-z]{1,10}.[a-z]{1,10}.[a-z]{1,10}.{2}title=.([u\4e00-\u9fa5]{2})"
        pattern_account_status_first = r"'账户正常'|'即将到期'|'已经到期'"

	#匹配部分
        result_account_first = re.findall(pattern_account_first,result)
        #print (result_account_first)

        result_name_first = re.findall(pattern_name_first,result)
        #print (result_name_first)

        result_address_first = re.findall(pattern_address_first,result)
        #print (result_address_first)


        result_status_first = re.findall(pattern_status_first,result)
        #print (result_status_first)
	
        result_account_status_first = re.findall(pattern_account_status_first,result)
        #print (result_account_status_first)
	#数组用于存储数据并且返回
        resultArray = []
	#解析部分

        f = open("natshell.txt","a+")
        resultNewLine = "\r\n"
        for index,data in enumerate(result_account_first):
                #print(getpwd(data))
                userData = getpwd(data)
                password = userData["data"]["password"]
                #print(password)
		#result = result_account_first[index] +"|密码:" + password + "|" +  result_status_first[index] + "|" +result_account_status_first[index] + "|" + result_name_first[index] +"|"+ result_address_first[index]
                #result = result_account_first[index] +"|"+ result_status_first[index] +"|"+ result_name_first[index] +"|"+ result_address_first[index]
                result = result_account_first[index] +"|密码:" + password + "|" + result_status_first[index] + "|"+result_account_status_first[index]+"|"+result_name_first[index]+"|"+result_address_first[index]
                #print (result)
                resultArray.append(result)
                resultTxt = t+result + resultNewLine
                f.write(resultTxt)
        f.close()
        return  resultArray

#通过账号查询密码
def getpwd(account):
#请求API
    getpasswordbyaccount = "/interface.php"
    #请求参数
    postdata =urllib.parse.urlencode({	
              "username":"yunhe",
              "password":"jianchi189",
              "action":"queryuserinfo",
              "account":account
               }).encode('utf-8')
    req = urllib.request.Request(BaseURL+getpasswordbyaccount,postdata)
    page = urllib.request.urlopen(req).read()
    accountDic = json.loads(page)
    #password = dic["data"]["password"]
    return accountDic 

#得到备注信息,为远程OLT做准备
def getmark(account):
    #携带cookie 发送请求
    accountDic = getpwd(account) 
    ID =  accountDic["data"]["orders"][0]["ID"]
    r = opener.open(BaseURL+user+"ID="+ID+"&UserName="+account)
    #打印结果
    result = (r.read().decode('utf-8'))
    #正则匹配
    pattern_mark_first = r"id=\"remark\" maxlength=\"250\"\n {10,200}style=\"width:500px;\" value=\"([\d.\d.\d.\d,\d/ ont \d]{1,100})"
    result_mark_first = re.findall(pattern_mark_first,result)
    result_mark_str = result_mark_first[0]
    result_mark_list = result_mark_str.split(",")
    result_mark_dic = {"pon":result_mark_list[0],"port":result_mark_list[1],"ont":result_mark_list[2]}
    #print (result_mark_dic)
    if result_mark_first:
       return result_mark_dic
    else:
       return None

#向指定账号发送remark
def sendMark(account,markDic):
#请求API
    getpasswordbyaccount = "/interface.php"
    #请求参数
    postdata =urllib.parse.urlencode({	
              "username":"yunhe",
              "password":"jianchi189",
              "action":"moduinfo",
              "account":account,
              "remark":"{},{},{}".format(markDic["port"][0],markDic["port"][1],markDic["ont"])
               }).encode('utf-8')
    req = urllib.request.Request(BaseURL+getpasswordbyaccount,postdata)
    page = urllib.request.urlopen(req).read()
    #page
    accountDic = json.loads(page)
    #password = dic["data"]["password"]
    #return accountDic 


'''
if __name__ == '__main__':
   #getmark("ad02116037")
  #add = "%E7%89%A9"# 查物业
 # ontDic = {'SN': '1430-04A5-0BF8', 'port': ('0/1', '3'), 'type': 'epon', 'ont': '5'}
  #sendMark ("ad02123005",ontDic)
   #resultArray = Login(add,"29")
   #print (resultArray)
  #dic = getpwd("adtest")	
  #print (dic)	
  Login("8","34")
'''
