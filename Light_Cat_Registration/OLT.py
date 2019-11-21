import pexpect
import re

#主方法用于登陆设备
def autoRegister(desc):
	child = pexpect.spawn('telnet 183.131.3.80 65534', encoding='utf-8')
	fileName = desc+".txt"
	fout = open(fileName,'w')
	child.logfile_read = fout
	child.expect('User name:')
	child.sendline('haoyunhe')
	child.expect('password:')
	child.sendline('jianchi189')
	child.expect('>')
	child.sendline('enable')
	child.expect('#')
	child.sendline('config')
	child.expect('#')
	child.sendline('display ont autofind all')
	child.expect('#')
	#如果没有发现设备/直接返回/否则进行注册操作
	pon = xpon()		
	if pon:
		ontDic = FSP()
		interfacePort = "interface "+pon +" "+ ontDic["port"][0]
		#根据SN PON口 PON类型 进入PON口
		child.sendline(interfacePort)
		child.expect('#')
		ont_add_first = "ont add "+ontDic["port"][1]+" sn-auth "+ontDic["SN"]+" omci ont-lineprofile-id 100 ont-srvprofile-id 20 desc "+desc  
		child.sendline(ont_add_first)
		child.expect('#')
		#添加ont-id
		ont_ONTID = ont_ONTID_second()
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
	else:
		print("没有发现光猫")



#日志输出,用于正则匹配使用
def mylog():
  f = open('mylog.txt')
  fr = f.read()
  return fr

#判断是GPON or EPON
def xpon():
  result_txt = mylog()
  pattern_xpon_first = r"GPON|EPON"
  result_xpon_first = re.findall(pattern_xpon_first,result_txt)
  if result_xpon_first:
     xpon = result_xpon_first[0]
  else:
     xpon = None
  return xpon

#得到X/X/X 用于进入PON口
def FSP():
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
  ontDic["SN"] = result_SN_first[0]
  #ontDic["service-port"] = result_FSP_first[0]
  ontDic["port"] = result_FSP_second[0]
  #print (ontDic)
  #print (ontDic["port"][0])
  return ontDic


#得到ONTID 注册第二条命令
def ont_ONTID_second():
  result_txt = mylog()
  pattern_ontID_first = r"ONTID :([\d]){1,3}"
  result_ontID_first = re.findall(pattern_ontID_first,result_txt)
  return result_ontID_first[0]

if __name__ == '__main__':
  autoRegister("beizhu") 
