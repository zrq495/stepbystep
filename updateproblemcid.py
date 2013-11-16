#!/usr/bin/env python
#coding=utf-8
import MySQLdb

cate_len = [13, 20, 17, 14, 9, 12, 7, 7, 19, 17, 5, 14, 26, 15, 7, 24, 10, 15, 10, 4, 4, 9]

conn = MySQLdb.connect('localhost','root','rootpass','stepbystep',charset ='utf8')
cur = conn.cursor()
cid = 1
pid = 1
for i in cate_len:
    for j in range(i):
        sql_content = 'update problem set cid=%d where pid=%d' %(cid, pid)
        print sql_content
        cur.execute(sql_content)
        conn.commit()
        pid += 1
    cid += 1
