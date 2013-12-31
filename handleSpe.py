#coding:utf8
from mmap import mmap, ACCESS_READ
from xlrd import open_workbook
import MySQLdb
f = open_workbook((u'全数据.xls').encode('gbk'))

con = MySQLdb.connect(host='192.168.3.120', user='root', passwd='badperson3', db='miamiao', charset='utf8')
for s in f.sheets():
    print s.name
    if s.name == u'special':
        title = ['name', 'attribute', 'silver', 'subKind', 'other']
        subMap = {
                u'头部':0,
                u'胸部':1,
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
            
            price = 0
            try:
                price = int(values[2])
            except:
                price = 0
            sql = u'insert into equip (name, silver,  kind, attribute) values("%s", %d, 3, "%s")' % (values[0], price,  values[1])
            print sql
            con.query(sql.encode('utf8'))
con.commit()
con.close()
            


