#switch_backup.py脚本代码

#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Name       : switch_backup.py
#Author     : MorphyHu
#Create Date: 2018-08-07 15:10
import paramiko
import time

baktime = time.strftime('%Y-%m-%d_%H-%M-%S') #备份时间

#配置全局变量
switchbrand = 'h3c' #or HUAWEI
tftpserver = '10.0.30.55'

def ssh2(ip,port,username,passwd,switchbrand,cmd):
        try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(hostname=ip,port=port,username=username,password=passwd,timeout=60,look_for_keys=False)
                #坑1，如果不设置look_for_keys为False,则SSH连接交换机有可能出现即使密码正确也会报Authentication failed.错误
                remote_conn = ssh.invoke_shell()
                remote_conn.send('save\n')
                while not remote_conn.recv_ready():
                        time.sleep(1)
                if switchbrand == 'h3c' :
                        remote_conn.send('y'+'\n')
                        while not remote_conn.recv_ready():
                                time.sleep(1)
                        remote_conn.send('\n')   
                        while not remote_conn.recv_ready():
                                time.sleep(1)
                remote_conn.send('y'+'\n')
                while not remote_conn.recv_ready():
                        time.sleep(1)
                print (cmd)
                #显示要执行的tftp命令
                remote_conn.send( cmd +'\n')
                while not remote_conn.recv_ready():
                        time.sleep(1)
                print ('%s\tOK'%(ip))
                ssh.close()
        except Exception as e:
                print ('%s\n'%(e))
if __name__=='__main__':
        print ("Backup Start......")
        if switchbrand == 'h3c' :
                fname='startup.cfg'  #H3C交换机文件名
        else: 
                fname='vrpcfg.zip'   #HUAWEI交换机文件名
        with open("./config.csv") as f:
                iplist=f.readlines()
                for line in iplist:
                        x = line.strip('\n')
                        y = x.split(',')
                        ip = str(y[0])
                        port = int(y[1])
                        username = y[2]
                        passwd = y[3]
                        backupname = baktime + '_' + ip + '_' + fname
                        cmd= 'tftp ' + tftpserver + ' put ' + fname + ' ' + backupname
                        ssh2(ip,port,username,passwd,switchbrand,cmd)
        print ("Backup Done......")



'''
config.csv 内容

10.0.50.1,22,sshadmin,password
10.0.50.11,22,sshadmin,password
10.0.50.12,22,sshadmin,password
10.0.50.13,22,sshadmin,password
10.0.50.14,22,sshadmin,password
10.0.50.15,22,sshadmin,password
10.0.50.16,22,sshadmin,password
10.0.50.17,22,sshadmin,password
10.0.50.18,22,sshadmin,password
10.0.50.19,22,sshadmin,password


执行结果

./switch_backup.py
Backup Start......
tftp 10.0.30.55 put startup.cfg 2018-08-08_14-53-59_10.0.50.1_startup.cfg
10.0.50.1       OK
tftp 10.0.30.55 put startup.cfg 2018-08-08_14-53-59_10.0.50.11_startup.cfg
10.0.50.11      OK
tftp 10.0.30.55 put startup.cfg 2018-08-08_14-53-59_10.0.50.12_startup.cfg
10.0.50.12      OK
tftp 10.0.30.55 put startup.cfg 2018-08-08_14-53-59_10.0.50.13_startup.cfg
10.0.50.13      OK
tftp 10.0.30.55 put startup.cfg 2018-08-08_14-53-59_10.0.50.14_startup.cfg
10.0.50.14      OK
tftp 10.0.30.55 put startup.cfg 2018-08-08_14-53-59_10.0.50.15_startup.cfg
10.0.50.15      OK
tftp 10.0.30.55 put startup.cfg 2018-08-08_14-53-59_10.0.50.16_startup.cfg
10.0.50.16      OK
tftp 10.0.30.55 put startup.cfg 2018-08-08_14-53-59_10.0.50.17_startup.cfg
10.0.50.17      OK
tftp 10.0.30.55 put startup.cfg 2018-08-08_14-53-59_10.0.50.18_startup.cfg
10.0.50.18      OK
tftp 10.0.30.55 put startup.cfg 2018-08-08_14-53-59_10.0.50.19_startup.cfg
10.0.50.19      OK
Backup Done......
'''




