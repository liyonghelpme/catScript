#coding:utf8
from mmap import mmap, ACCESS_READ
from xlrd import open_workbook
import MySQLdb
con = MySQLdb.connect(host='192.168.3.120', user='root', passwd='badperson3', db='miamiao', charset='utf8')
sql = 'select * from equip where kind = 2'
con.query(sql)
res = con.store_result().fetch_row(0, 1)
import re
pat =re.compile('\+(-?\d+)')
for i in res:
    allAtt = i['attribute'].split()
    print allAtt
    for k in allAtt:
        if k.find('-') != -1:
            k = k.replace('-', '+-')
        num = int(pat.findall(k)[0])
        k = k.split('+')[0]
        vmap = {
            u'体力':'health',
            u'腕力':'brawn',
            u'劳动':'labor',
            u'远程':'shoot',
            u'攻击':'attack',
            u'防御':'defense'
        }
        print k
        sql = 'update equip set %s = %d where id = %d' % (vmap[k], num, i['id'])
        print sql
        con.query(sql)

con.commit()
con.close()
