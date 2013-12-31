#coding:utf8
from mmap import mmap, ACCESS_READ
from xlrd import open_workbook
import MySQLdb
con = MySQLdb.connect(host='192.168.3.120', user='root', passwd='badperson3', db='miamiao', charset='utf8')
sql = 'select * from skill'
con.query(sql)
skill = con.store_result().fetch_row(0, 1)
temp = {}
for k in skill:
    temp[k['name']] = k
skill = temp

sql = 'select * from people'
con.query(sql)
people = con.store_result().fetch_row(0, 1)

#更新每只猫咪的 skillId信息
for k in people:
    if skill.get(k['skillName'], None) != None:
        sql = 'update people set skill = %d where id = %d' % (skill[k['skillName']]['id'], k['id'])
        print sql
        con.query(sql)

con.commit()
con.close()

