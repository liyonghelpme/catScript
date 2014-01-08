#coding:utf8
from mmap import mmap, ACCESS_READ
from xlrd import open_workbook
import MySQLdb
import json

con = MySQLdb.connect(host='192.168.3.120', user='root', passwd='badperson3', db='miamiao', charset='utf8')
sql = 'select * from buildings'
con.query(sql)
res = con.store_result().fetch_row(0, 1)
temp = {}
for k in res:
    temp[k['name']] = k

sql = 'select * from goods'
con.query(sql)
res = con.store_result().fetch_row(0, 1)
bidToGoods = {}
for k in res:
    print 'storeName', k['storeName']
    sn = temp.get(k['storeName'], None)
    if sn != None:
        sql = 'update goods set store = %d where id = %d' % (sn['id'], k['id'])
        con.query(sql)
        gl = bidToGoods.setdefault(sn['id'], [])
        gl.append(k['id'])
    else:
        print 'error'
for k in bidToGoods:
    sql = 'update buildings set goodsList = "%s"  where id = %d' % (json.dumps(bidToGoods[k]), k)
    con.query(sql)

con.commit()
con.close()

