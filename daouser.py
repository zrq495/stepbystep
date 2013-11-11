#!/usr/bin/env python
#coding=utf-8
import MySQLdb
fp = open("/home/timeship/pojaccount")
conn = MySQLdb.connect('192.168.1.123','root','rootpass','stepbystep',charset ='utf8')
cur = conn.cursor()
for line in fp.readlines():
    cun = line.split()
    print cun
    #sql_content = "update contest_user set name1='%s',password = '%s' where id = %d;"%(cun[1],cun[4],int(cun[0])) 
    sql_content="insert into user(user_id,user_name,poj_name,grade) values(null,'%s','%s',%d)"%(cun[0],cun[1],int(cun[2]))
    print sql_content
    cur.execute(sql_content)
    conn.commit()
