import subprocess
def do_telnet(Host,username,password,finish,commands):
        import telnetlib
        import time
        for Host in Hosts:
                try:
                        tn = telnetlib.Telnet(Host, port=23, timeout=10)
                except:
                        print ("Can't connection")
                        e = 'echo "%s can not connection" |  mail -s "Backup failed"   501874532@qq.com,631082262@qq.com' % Host
                        subprocess.call(e , shell=True)
                        continue
                tn.set_debuglevel(2)
                tn.read_until('Username:')
                tn.write(username + '\n')
                tn.read_until('Password:')
                tn.write(password + '\n')
                tn.read_until(finish)
                for command in commands:
                        tn.write('%s\n' % command)
                        print ('%s is executing' % command)
                        time.sleep(1)
                time.sleep(3)
                msg=tn.read_very_eager()
                tem=open('/home/Script/Backtest/S6720/%s'% Host,'w')
                tem.write(msg)
                tem.close()
                tn.close()
if __name__=='__main__':
        Hosts = ['10.200.1.9','10.201.1.17','10.202.1.20','10.200.1.2','10.200.12.1','10.200.12.2','10.200.12.3','10.200.2.1','10.200.2.2','10.200.2.3','10.200.2.4','10.200.2.5','10.200.4.1','10.200.4.2','10.200.6.1','10.200.6.2','10.201.1.1','10.201.1.11','10.201.1.13','10.201.1.18','10.201.1.3','10.201.1.4','10.201.1.5','10.201.1.7','10.202.1.19','10.205.5.1','10.200.1.5','10.200.1.6','10.200.1.8','10.202.7.2','10.204.4.1','10.204.4.2','10.206.4.1','10.1.98.18','10.1.99.15','10.1.99.17','10.200.2.8','10.200.2.9','10.201.1.10','10.201.1.12','10.201.1.20','10.201.1.23','10.1.98.19','10.1.98.21','10.1.99.12']
        username = 'backup'
        password = 'jianchi189'
        finish = ''
        commands = ['sys','user-interface vty 0 4','screen-length 0','dis cur','user-interface vty 0 4','undo screen-length ','quit','quit']
        do_telnet(Hosts,username,password,finish,commands)


