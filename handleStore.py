#coding:utf8
from mmap import mmap, ACCESS_READ
from xlrd import open_workbook
import MySQLdb
import json
f = open_workbook((u'全数据.xls').encode('gbk'))

con = MySQLdb.connect(host='192.168.3.120', user='root', passwd='badperson3', db='miamiao', charset='utf8')
import re
pat1 = re.compile(u'木材\*(\d+)')
pat2 = re.compile(u'食材\*(\d+)')
pat3 = re.compile(u'矿石\*(\d+)')
pat = re.compile(u'\d+')

for s in f.sheets():
    print s.name
    if s.name == u'goods':
        lastName = None
        for row in range(s.nrows):
            values = []
            for col in range(s.ncols):
                v = s.cell(row, col).value
                if v != '':
                    values.append(v)
                    #print v, ',',
            if len(values) == 5:
                lastName = values[0]
            else:
                temp = [lastName]
                for k in values:
                    temp.append(k)
                values = temp
            print json.dumps(values, ensure_ascii=False)
            wood = 0
            food = 0
            stone = 0
            cost = values[2]
            res = pat1.findall(cost)
            if len(res) > 0:
                wood = int(res[0])
            res = pat2.findall(cost)
            if len(res) > 0:
                food = int(res[0])
            res = pat3.findall(cost)
            if len(res) > 0:
                stone = int(res[0])

            res = pat.findall(values[4]) 
            cond = 0
            if len(res) > 0:
                cond = int(res[0])

            print wood, food, stone, cond
            sql = u'insert into goods (name, food, stone, wood, price, `condition`, storeName) values("%s", %d, %d, %d, %d, %d, "%s")' % (values[1], food, stone, wood, values[3], cond, values[0])
            print sql
            con.query(sql.encode('utf8'))
            print 

con.commit()
con.close()



