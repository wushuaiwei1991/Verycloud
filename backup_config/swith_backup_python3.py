from ftplib import FTP
import time,os
Today = time.strftime("%Y-%m-%d", time.localtime())
hosts = ['192.168.254.X',
         '192.168.254.X',
         '192.168.254.X',
         '192.168.254.X',
         '192.168.254.X',
         '192.168.254.X',
         '192.168.254.X',
         '192.168.254.X',
         '192.168.254.X',
         '192.168.254.X']
port = 21
user = 'admin'
pwd = 'XXXXXX'
for host in hosts:
    # if host not in os.listdir('./'):
    if os.path.exists(host) is False:#os.path.exists(path) 判断一个目录是否存在
        os.mkdir(host)#os.mkdir(path) 创建目录
        os.chdir(host)#os.mkdir(path) 改变当前目录
    else:
        os.chdir(host)
    ftp = FTP()
    ftp.set_debuglevel(2)
    ftp.connect(host,port)
    ftp.login(user,pwd)
    bufsize = 1024
    filename = "{}.zip".format(Today)
    file_handle = open(filename, "wb").write
    ftp.retrbinary("RETR vrpcfg.zip", file_handle, bufsize)
    ftp.set_debuglevel(0)
    ftp.quit()
    os.chdir('../')