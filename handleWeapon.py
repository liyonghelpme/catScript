#coding:utf8
from mmap import mmap, ACCESS_READ
from xlrd import open_workbook
import MySQLdb
f = open_workbook((u'全数据.xls').encode('gbk'))

con = MySQLdb.connect(host='192.168.3.120', user='root', passwd='badperson3', db='miamiao', charset='utf8')
sql = 'select * from people '
con.query(sql)
allp = con.store_result().fetch_row(0, 1)

for s in f.sheets():
    print s.name
    if s.name == u'skill':
        title = ['name', 'attribute', 'silver', 'subKind', 'other']
        subMap = {
                u'刀':0,
                u'枪':1,
                u'弓':2,
                u'法杖':3,
                u'拳':4,
        }
        subKind = 0
        for row in xrange(0, s.nrows):
            values = []
            for col in range(s.ncols):
                v = s.cell(row, col).value
                if v != '':
                    values.append(v)
                    print v, ',',
            print
            '''
            try:
                newKind = subMap[values[3]]
                subKind = newKind
            except:
                newKind = subKind

            sql = u'insert into equip (name, silver, subKind, kind, attribute) values("%s", %d, %d, 0, "%s")' % (values[0], values[2], subKind, values[1])
            '''
            sql = u'update people set skillName = "%s" where name = "%s"' % (values[5], values[4])
            print sql
            con.query(sql.encode('utf8'))

con.commit()
con.close()
            


