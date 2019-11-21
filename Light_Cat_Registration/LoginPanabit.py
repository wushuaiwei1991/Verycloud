#coding:utf-8
import urllib
import http.cookiejar
import ssl

#取消HTTPS
ssl._create_default_https_context = ssl._create_unverified_context

#BaseURL && API
BaseURL = "https://10.30.20.201"
LoginURL = "/login/userverify.cgi"

#请求参数
postdata =urllib.parse.urlencode({	
"username":"admin",
"password":"verycloud@isp"
}).encode('utf-8')

#Login 获取cookie
req = urllib.request.Request(BaseURL+LoginURL,postdata)

#自动记住cookie
cj = http.cookiejar.CookieJar()
#创建opener
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

#打开带有cookie的req 
r = opener.open(req)

#查询连接数
def flowNumber():

 #使用带有cookie的opener 请求连接数
 r = opener.open("https://10.30.20.201/cgi-bin/Monitor/ajax_group_stat?type=datasnap&bridge=0")
 string = r.read()
 dic = eval(string)
 return dic["flow"] 
 

'''
if __name__ == '__main__':
  data = flowNumber()
  print (data)
'''
