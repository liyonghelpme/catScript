#coding:utf8
from mmap import mmap, ACCESS_READ
from xlrd import open_workbook
import MySQLdb
f = open_workbook((u'角色新改.xlsx').encode('gbk'))

con = MySQLdb.connect(host='192.168.3.120', user='root', passwd='badperson3', db='miamiao', charset='utf8')
sql = 'select * from people'
con.query(sql)
allP = con.store_result().fetch_row(0, 1)
temp = {}
for k in allP:
    temp[k['name']] = k

for s in f.sheets():
    print s.name
    if s.name == u'角色数据补充':
        title = []
        cnTokey = {
                u'角色名':'name',
                u'初始体力':'health',
                u'体力成长':'healthAdd',
                u'初始腕力':'brawn',
                u'腕力成长':'brawnAdd',
                u'初始射击':'shoot',
                u'射击成长':'shootAdd',
                u'初始劳动':'labor',
                u'劳动成长':'laborAdd'
        }
        vmap = {}
        allKey = cnTokey.values()
        for row in range(s.nrows):
            values = []
            for col in range(s.ncols):
                v = s.cell(row, col).value
                values.append(v)
                print v, ',',
                if row == 0:
                    if v in cnTokey:
                        vmap[col] = cnTokey[v]
                else:
                    if vmap[col] != 'name':
                        if temp.get(values[0], None) == None:
                            sql = u'insert into people (name) values("%s")' % (values[0])
                            con.query(sql.encode('utf8'))
                            temp[values[0]] = True
                            #con.commit()
                        sql = u'update people set %s = %d where name = "%s" ' % (vmap[col], v, values[0])
                        print sql
                        con.query(sql.encode('utf8'))
            print 
        print vmap

con.commit()
con.close()

