def do_telnet(Host,username,password,finish,commands):
        import telnetlib
        import time
        for Host in Hosts:
                tn = telnetlib.Telnet(Host, port=23, timeout=10)
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
                tem=open('/home/Script/Backtest/CE6870/%s'% Host,'w')
                tem.write(msg)
                tem.close()
                tn.close()
if __name__=='__main__':
        Hosts = ['10.200.1.3','10.200.10.1','10.200.2.6','10.200.4.3','10.200.5.1','10.200.6.3','10.200.6.4','10.200.7.1','10.200.7.2','10.200.8.1','10.201.1.2','10.201.1.24','10.201.1.8','10.202.1.2','10.202.4.1','10.202.5.1','10.202.7.1','10.200.11.1','10.205.5.3']
        username = 'backup'
        password = 'jianchi189'
        finish = ''
        commands = ['system-view immediately','user-interface vty 0 4','screen-length 0','dis cur','user-interface vty 0 4','undo screen-length ','quit','quit']
        do_telnet(Hosts,username,password,finish,commands)



