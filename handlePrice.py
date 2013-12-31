#coding:utf8
from mmap import mmap, ACCESS_READ
from xlrd import open_workbook
import MySQLdb
f = open_workbook((u'全数据.xls').encode('gbk'))

import re
con = MySQLdb.connect(host='192.168.3.120', user='root', passwd='badperson3', db='miamiao', charset='utf8')
for s in f.sheets():
    print s.name
    if s.name == u'price':
        for row in range(s.nrows):
            values = []
            for col in range(s.ncols):
                v = s.cell(row, col).value
                if v != '': 
                    values.append(v)
                    print v, ',',
            silver = 0
            gold = 0
            if values[1].find(u'金钱') != -1:
                silver = int(values[1].replace(u'金钱', ''))
            elif values[1].find(u'金块') != -1:
                gold = int(values[1].replace(u'金块', ''))
            elif values[1].find(u'直接') != -1: 
                pass
            
            sql = u'update people set silver = %d, gold = %d where name = "%s" ' % (silver, gold, values[0])
            print sql
            con.query(sql.encode('utf8'))

con.commit()
con.close()
