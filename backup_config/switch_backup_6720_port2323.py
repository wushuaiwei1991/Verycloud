import subprocess
def do_telnet(Host,username,password,finish,commands):
        import telnetlib
        import time
        for Host in Hosts:
                try:
                        tn = telnetlib.Telnet(Host, port=2323, timeout=10)
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
        Hosts = ['10.205.5.2','10.200.1.7']
        username = 'backup'
        password = 'jianchi189'
        finish = ''
        commands = ['sys','user-interface vty 0 4','screen-length 0','dis cur','user-interface vty 0 4','undo screen-length ','quit','quit']
        do_telnet(Hosts,username,password,finish,commands)


