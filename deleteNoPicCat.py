#coding:utf8
from mmap import mmap, ACCESS_READ
from xlrd import open_workbook
import MySQLdb
con = MySQLdb.connect(host='192.168.3.120', user='root', passwd='badperson3', db='miamiao', charset='utf8')

sql = 'select * from people where id >= 18'
con.query(sql)
res = con.store_result().fetch_row(0, 1)
nowId = 18
for r in res:
    if r['name'].find(u'村民') == -1:
        print r['name']
        sql = 'delete from people where id = %d' % (r['id'])
        con.query(sql)
    else:
        sql = 'update people set id = %d where id = %d' % (nowId, r['id']) 
        con.query(sql)
        nowId = nowId+1

con.commit()
con.close()
