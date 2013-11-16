#!/usr/bin/env python
#coding=utf-8
import MySQLdb
import os
account_path = os.path.join(os.getcwd(), 'pojaccount')
fp = open(account_path)
conn = MySQLdb.connect('localhost','root','rootpass','stepbystep',charset ='utf8')
cur = conn.cursor()
for line in fp.readlines():
    cun = line.split()
    #print cun
    sql_content = "update user set class1='%s',grade='%s' where user_name = '%s';"%(cun[3],cun[2],cun[0]) 
    #sql_content="insert into user(user_id,user_name,poj_name,grade,class1,permission) values(null,'%s','%s',%d,'%s',1)"%(cun[0],cun[1],int(cun[2]), cun[3])
    print sql_content
    cur.execute(sql_content)
    conn.commit()
