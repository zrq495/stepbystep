#!/usr/bin/env python
#coding=utf-8
import MySQLdb
fp = open("/home/timeship/pojplan")
conn = MySQLdb.connect('localhost','username','password','stepbystep',charset ='utf8')
cur = conn.cursor()
for line in fp.readlines():
    cun = line.split()
    print cun
    #sql_content = "update contest_user set name1='%s',password = '%s' where id = %d;"%(cun[1],cun[4],int(cun[0])) 
    sql_content="insert into problem(pid,poj_pid) values(null,%d);"%(int(cun[0]))
    print sql_content
    cur.execute(sql_content)
    conn.commit()