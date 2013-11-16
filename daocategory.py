#!/usr/bin/env python
#coding=utf-8
import MySQLdb
import os
account_path = os.path.join(os.getcwd(), 'category.txt')
fp = open(account_path)
conn = MySQLdb.connect('localhost','root','rootpass','stepbystep',charset ='utf8')
cur = conn.cursor()
for line in fp.readlines():
    cun = line.split()
    #print cun
    sql_content="insert into category(cid, rank, cname) values(null, '%s', '%s')"%(cun[0],cun[1])
    print sql_content
    cur.execute(sql_content)
    conn.commit()
