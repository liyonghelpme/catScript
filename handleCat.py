#coding:utf8
import os
import MySQLdb
if not os.path.exists('result'):
    os.mkdir('result')

con = MySQLdb.connect(host='192.168.3.120', user='root', passwd='badperson3', db='miamiao', charset='utf8')
sql = 'select * from people where id >= 9'
con.query(sql)
res = con.store_result().fetch_row(0, 1)
for i in res[1:]:
    if i['id'] == 15 or i['id'] == 13:
        if os.path.exists(i['name'].encode('gbk')):
            os.system('cp mvpic.py %s' %(i['name'].encode('gbk')))
            os.system('cp name.py %s' %(i['name'].encode('gbk')))
            os.chdir(i['name'].encode('gbk'))
            print i['name']
            os.system('python mvpic.py %d' % (i['id']))
            os.system('mv result/* ../result')
            os.chdir('..')
        else:
            print "Error no cat ", i['name'].encode('gbk')

