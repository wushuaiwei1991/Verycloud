import pexpect
import re
import time
#from LoginNatshell import sendMark

#如果遇到多行使用自带正则进行匹配
moreLine = r"---- More ( Press 'Q' to break ) ----"
#主方法用于登陆设备
#为了便于兼容EPON/GPON 把EPON 的MAC字段的key 变为SN
def autoLogin(account,host):
	host = "telnet "+str(host)
	child = pexpect.spawn(str(host), encoding='utf-8',timeout=5)
	#用于存档
	t = time.strftime("%Y-%m-%d", time.localtime())
	#print (dateNow)
	fileName = t+"_"+account+".txt"
	fout = open(fileName,'w')
	#用于正则匹配
	mylog = open("mylog.txt","w")
	child.logfile_read  = fout
	child.logfile  = mylog
	child.expect('User name:')
	child.sendline('yifan')
	child.expect('password:')
	child.sendline('yifan1018')
	child.expect('>')
	child.sendline('enable')
	child.expect('#')
	child.sendline('config')
	child.expect('#')
	return child


#首先返回一个MAC地址 MAC地址确认后,进行注册
def autoRegisterComfirm(account,host):
    child = autoLogin(account,host)
    child.sendline('display ont autofind all')
    i = child.expect(['More','config\)#'])
    if i == 0:
       #print ("匹配More") 有多个设备
       while 1:
         child.sendline(' ')
         #print ("空格")
         j = child.expect(['More','config\)#'])
         if j == 1:
            break
    elif i == 1:
      None
      #print ("匹配#") #有一个设备
    #如果没有发现设备/直接返回/否则进行注册操作
    pontype = xpon()		
    if pontype:
       comfirm = 1#用于用户观看的数据
       ontDic = FSP(pontype,comfirm)
       #print (ontDic)
       return (ontDic["SN"])
       #print (result_last)
    else:
       result_last = ["没有发现光猫"]
       #print (result_last)
       return (result_last)

def autoRegister(account,host,SN):
  child = autoLogin(account,host)
  child.sendline('display ont autofind all')
  #如果没有发现设备/直接返回/否则进行注册操作
  i = child.expect(['More','config\)#'])
  if i == 0:
       #print ("匹配More") 有多个设备
       while 1:
           child.sendline(' ')
           #print ("空格")
           j = child.expect(['More','config\)#'])
           if j == 1:
              break
  elif i == 1:
       None 
       #print ("匹配#") #有一个设备
       #child.expect('config\)#')
  pontype = xpon()		
  if pontype:
        comfirm = 2#用于程序使用的数据
        ontDic_first = FSP(pontype,comfirm)
        ontDic = snComfirm(SN,ontDic_first)
        #print (ontDic)
        if ontDic["SN"] == None:
           result_first = "输入光猫MAC\r\n与待注册光猫MAC不匹配"
           #print (result_last)
           return (result_first)
        else:
           #print (ontDic)
           interfacePort = "interface "+pontype +" "+ontDic["port"][0]
           #print (interfacePort)
           #根据MAC|SN PON口 PON类型 进入PON口
           child.sendline(interfacePort)
           child.expect('#')
           #选择命令种类 GPON / EOPN
           #resultDic {'SN': '30D1-7E6B-524C', 'port': ('0/4', '4'), 'type': 'epon', 'ont': '4'}
           resultDic = commandSelect(pontype,child,ontDic,account)
           #由于脚本执行速度快,所以使程序休眠5秒,查询收光情况
           #将需要的内容通过蓝海接口发送到该用户的remark,为收光查询做准备 发送remark 在蓝海模块
           result_first = "注册完毕"
           #print (resultDic)
           sendMark(account,resultDic)
           return (result_first)
  else:
        result_last = "没有发现光猫"
        #print (result_last)
        return (result_first)

#确认MAC|SN 
def snComfirm(sn,snDic):
  #print (sn)  
  snList = snDic["SN"]
  #print (snList)
  ontDic = {}
  for index,data in enumerate(snList):
      #print (data)
      if sn == data:
         ontDic["SN"] = snDic["SN"][index]
         ontDic["port"] = snDic["port"][index]
         ontDic["type"] = snDic["type"]
         #print (ontDic)
         return (ontDic)
      else:
         #print ("MAC|SN 没有经过确认!")
         ontDic["SN"] = None
  #print (ontDic)
  return (ontDic)

#command 选择EPON/GPON 命令
def commandSelect(pontype,child,ontDic,account):
  if pontype == "gpon":
     resultDic = gponCommand(child,ontDic,account)
  else:
     resultDic = eponCommand(child,ontDic,account)
  return resultDic
#GPON 命令
def gponCommand(child,ontDic,account):
	ont_add_first = "ont add "+ontDic["port"][1]+" sn-auth "+ontDic["SN"]+" omci ont-lineprofile-id 100 ont-srvprofile-id 20 desc "+account  
	child.sendline(ont_add_first)
	child.expect('#')
	#添加ont-id
	ont_ONTID = ont_ONTID_second()
	print (ont_ONTID)

	ont_add_second = "ont port native-vlan "+ontDic["port"][1]+" "+str(ont_ONTID)+" eth 1 vlan 101 priority 0"
	#print (ont_add_second)
	child.sendline(ont_add_second)
	child.expect('#')
	child.sendline("quit")
	child.expect('#')
	#添加serverport
	service_port = "service-port vlan 1601 gpon "+ontDic["port"][0]+"/"+ontDic["port"][1]+" ont "+str(ont_ONTID)+" gemport 1 multi-service user-vlan 101 tag-transform translate-and-add inner-vlan 1000 inner-priority 0"
	print (service_port)
	child.sendline(service_port)
	child.expect(':')
	child.sendline(" ")
	child.expect('#')

def eponCommand(child,ontDic,account):
	#ont_add_first = "ont add "+ontDic["port"][1]+" sn-auth "+ontDic["SN"]+" omci ont-lineprofile-id 100 ont-srvprofile-id 20 desc "+account  
	ont_add_first = "ont add {} mac-auth {} oam ont-lineprofile-id 100 ont-srvprofile-id 10 desc {}".format(ontDic["port"][1],ontDic["SN"],account)
	#child.expect('#')
	child.sendline(ont_add_first)
	child.expect('#')
	child.sendline(" ")
	child.expect('#')

	#添加ont-id
	ont_ONTID = ont_ONTID_second()
	#print (ont_ONTID)

	#ont_add_second = "ont port native-vlan "+ontDic["port"][1]+" "+str(ont_ONTID)+" eth 1 vlan 101 priority 0"
	userVlan = 2100 + int(ont_ONTID)
	ontDic["ont"] = ont_ONTID
	#print (userVlan)
	ont_add_second = "ont port native-vlan {} {} eth 1 vlan {}".format(ontDic["port"][1],ont_ONTID,str(userVlan))
	#print (ont_add_second)
	child.sendline(ont_add_second)
	child.expect('#')
	child.sendline("quit")
	child.expect('#')
	#添加serverport
	service_port = "service-port  vlan 61 epon {}/{} ont {} multi-service user-vlan {} tag-transform translate-and-add inner-vlan {} inner-priority 0".format(ontDic["port"][0],ontDic["port"][1],ont_ONTID,userVlan,userVlan)
	#print (service_port)
	child.sendline(service_port)
	child.expect(':')
	child.sendline(" ")
	child.expect('#')
	child.sendline("save")
	child.expect(':')
	child.sendline(" ")
	child.expect('#')
	return ontDic




#查询命令 查光猫在线状态,以及收光情况
def autoSearch(portDic,host,account):
  child = autoLogin(account,host)
  child.sendline('display service-port port {}/{} ont  {}'.format(portDic["port"][0],portDic["port"][1],portDic["ont"]))
  child.expect(':')
  child.sendline(" ")
  child.expect('#')
  #获得pon 类型
  pontype = xpon()
  #获取光猫 up/down 状态 
  state = ontState()
  if state == "up":
     #print ("up")#如果up 查询收光
     interFace = "interface {} {}".format(pontype,portDic["port"][0])
     child.sendline(interFace)
     child.expect('#')
     optical = "display ont optical-info {} {}".format(portDic["port"][1],portDic["ont"])
     child.sendline(optical)
     child.expect('More')
     child.sendline('q')
     child.expect('#')
     Rxoptical()
  else:
     #print ("down")#如果down,查询最近2次下线记录
     interFace = "interface {} {}".format(pontype,portDic["port"][0])
  #做判断 如果光猫不在线,查询最近一次下线原因
  #interFace = "interface epon {}".format(portDic["pon"])
  #child.sendline(interFace)
  #child.expect('#')

#获取收光状态
def Rxoptical():
  result_txt = mylog()
  pattern_Rxoptical_first = r"Rx optical power\(dBm\)                  : (-\d+.\d+)"
  result_Rxoptical_first = re.findall(pattern_Rxoptical_first,result_txt)
  #return (result_ontState_first[0])
  print (result_Rxoptical_first)

#获取光猫up/down状态
def ontState():
  result_txt = mylog()
  pattern_ontState_first = r"up|down"
  result_ontState_first = re.findall(pattern_ontState_first,result_txt)
  return (result_ontState_first[0])


#日志输出,用于正则匹配使用
def mylog():
  f = open('mylog.txt')
  fr = f.read()
  return fr

#判断是GPON or EPON
def xpon():
  result_txt = mylog()
  pattern_xpon_first = r"GPON|EPON|gpon|epon"
  result_xpon_first = re.findall(pattern_xpon_first,result_txt)
  if result_xpon_first:
     xpon = result_xpon_first[0]
  else:
     xpon = None
  return xpon

#选择PON类型,从而匹配SN(GPON) 还是MAC(EPON)
def FSP(pontype,comfirm):
  if pontype == "EPON":
     ontDic = EponFSP(comfirm)
  else:
     ontDic = GponFSP(comfirm)
  
  return ontDic

#得到X/X/X 用于进入PON口GPON
def GponFSP(comfirm):
  result_txt = mylog()
  pattern_SN_first = r"Ont SN              : ([0-9A-Z]{16})"
  result_SN_first = re.findall(pattern_SN_first,result_txt)
  #print (result_SN_first)
  
  #pattern_FSP_first = r"F/S/P               : ([\d\/\d\/\d]{2,20})"
  pattern_FSP_second = r"F/S/P               : ([\d\/\d]{2,5})\/(\d){1,2}"
  #result_FSP_first = re.findall(pattern_FSP_first,result_txt)
  result_FSP_second = re.findall(pattern_FSP_second,result_txt)
  #print (result_FSP_first)
  #print (result_FSP_second)
  #创建字典并且添加key,value
  ontDic = {}
  #print (result_SN_first)
  ontDic["SN"] = result_SN_first[0]
  #ontDic["service-port"] = result_FSP_first[0]
  ontDic["port"] = result_FSP_second[0]
  ontDic["type"] = "gpon"
  #print (ontDic)
  #print (ontDic["port"][0])
  return ontDic

#得到X/X/X 用于进入PON口 EPON
def EponFSP(comfirm):
  result_txt = mylog()
  pattern_MAC_first = r"ONT MAC             : ([0-9A-Z]{4}\-[0-9A-Z]{4}\-[0-9A-Z]{4})"
  result_MAC_first = re.findall(pattern_MAC_first,result_txt)
  #print (result_MAC_first)
  
  pattern_FSP_second = r"F/S/P               : ([\d\/\d]{2,5})\/(\d+)"
  result_FSP_second = re.findall(pattern_FSP_second,result_txt)
  #print (result_FSP_second)
  #创建字典并且添加key,value

  ontDic = {}
  result_MAC_second = []
    #print (result_MAC_first)
  for index,data in enumerate(result_MAC_first):
      result = "待注册:"+data
      result_MAC_second.append(result)
  if comfirm == 1:
     ontDic["SN"] = result_MAC_second
  else:
     ontDic["SN"] = result_MAC_first
  #print (ontDic["SN"]) 
    #ontDic["service-port"] = result_FSP_first[0]
  ontDic["port"] = result_FSP_second
  ontDic["type"] = "epon"
    #print (ontDic)
    #print (ontDic["port"][0])
  return ontDic


#得到ONTID 注册第二条命令
def ont_ONTID_second():
  result_txt = mylog()
  pattern_ontID_first = r"ONTID :(\d+)"
  result_ontID_first = re.findall(pattern_ontID_first,result_txt)
  return result_ontID_first[0]



if __name__ == '__main__':
  autoSearch({'SN': '30D1-7E6B-524C', 'port': ('0/4', '0'), 'type': 'epon', 'ont': '0'},"10.1.98.7","ad02116037") 
  #ontDic = autoRegisterComfirm("autoReigster","10.1.98.7")
  #autoRegister("ad02128007","10.1.98.7","30D1-7E6B-524C")
 #ont_ONTID_second()

