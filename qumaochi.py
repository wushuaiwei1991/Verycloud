# -*- coding:utf-8 -*- 
#!/usr/bin/python
import os,sys,re,time

if len(sys.argv) != 3:
        print '参数数量不正确，本程序要求传入文件路径与带宽大小\n千M口请输入1000，万兆口请输入10000\n命令格式：python qumaoshi.py /var/www/html/rra/xxx/xxxxx.rrd 1000 | 10000)'
        quit()
else:
        file_path = sys.argv[1]
        daikuan = sys.argv[2]
        rrd_file = file_path.split('/')[6]
        xml_file = rrd_file.replace('.rrd','.xml')
        xml_new_file = rrd_file.replace('.rrd','_new.xml')
        xml_path = '/tmp/xml'
        if (daikuan == '1000' or daikuan == '10000') and os.path.exists(file_path):

                print '目标文件已找到 <br/>'
        else:
                print '参数错误:\n请检查文件路径和带宽参数'
                quit()

def write_xml(line):
        with open('/tmp/xml/%s' % (xml_new_file),'a') as f:
                f.write(line)

print '正在修复，请耐心等待。<br/>'
start = time.clock()
if daikuan == '10000':
        max_value = 1e+10
else:
        max_value = 1.5e+08
os.system('cd %s && rrdtool dump %s %s' % (xml_path,file_path,xml_file))
with open('/tmp/xml/%s' % (xml_file)) as f:
        content = f.readlines()
p1 = re.compile(r'\d\.\d{10}e\+\d{2}')
for line in content:
        value = p1.findall(line)
        if len(value) == 2:
                value_in = float(value[0])
                value_out = float(value[1])
                if (value_in > max_value) or (value_out > max_value):
                        str_value_in = format(value_in,'.10e')
                        str_value_out = format(value_out,'.10e')
                        str_value_in_last = format(value_in_last,'.10e')
                        str_value_out_last = format(value_out_last,'.10e')
                        line = line.replace(str_value_in,str_value_in_last).replace(str_value_out,str_value_out_last)
                        write_xml(line)
                else:
                        write_xml(line)
                        value_in_last = value_in
                        value_out_last = value_out
        elif len(value) == 1:
                value_in = float(value[0])
                if value_in > max_value:
                        str_value_in = format(value_in,'.10e')
                        str_value_in_last = format(value_in_last,'.10e')
                        line = line.replace(str_value_in,str_value_in_last)
                else:
                        write_xml(line)
                        value_in_last = value_in
        else:
                write_xml(line)
curtime =  time.strftime("%m-%d_%H:%M:%S", time.localtime())
print os.popen("cp -f %s /tmp/rrdbak/%s_%s" % (file_path,curtime,rrd_file)).read()+'<br/>'
print os.popen("rrdtool  restore -f /tmp/xml/%s %s" % (xml_new_file,file_path)).read()+'<br/>'
os.system("rm -f /tmp/xml/*")
finish = time.clock()
timer = finish - start
print ' 本次脚本运行耗费%fs,恭喜，毛刺去除成功！<br/>'%timer
