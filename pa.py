#!/usr/bin/env python
#coding=utf-8
import urllib
import re
import MySQLdb
import time
conn = MySQLdb.connect('localhost','root','rootpass','stepbystep',charset='utf8')
cur =conn.cursor()
def gethtml(url):
    content = urllib.urlopen(url)
    html = content.read()
    content.close()
    return html
def getpicture(html):
    reg = '<tr align=center><td>.*?</td><td><a href=userstatus\?user_id=.*?>(.*?)</a></td><td><a href=problem\?id=\d+>(.*?)</a></td><td><font color=blue>Accepted</font></td><td>.*?</td><td>.*?</td><td>.*?</td><td>.*?</td><td>(.*?)</td></tr>'
    picturelist = re.compile(reg).findall(html)
    return picturelist
def gethtmlfun(uid):
    sql_content1="select poj_name from user where user_id=%d;"%int(uid)
    print sql_content1
    cur.execute(sql_content1)
    username=cur.fetchall()
    print "".join(username[0])
    sql_content2="select * from problem;"
    cur.execute(sql_content2)
    pid = cur.fetchall()
    sql_content3="select * from solution where user_id=%d;"%int(uid)
    cur.execute(sql_content3)
    checkuser=cur.fetchall()
    print checkuser[0][0],checkuser[0][1]
    for k in pid:
        getml = gethtml('http://poj.org/status?problem_id=%s&user_id=%s&result=&language=;'%(k[1],"".join(username[0])))
        list_all = getpicture(getml)
        if list_all:
            for i in list_all[-1:]:
                print i[0],i[1],i[2]
                if checkuser[0][0]!=int(uid) and checkuser[0][1]!=int(k[0]):
                    sql_content4="insert into solution(user_id,pid,actime) values(%d,%d,'%s');"%(int(uid),int(k[0]),i[2].split(' ')[0])
                    print sql_content4
                    cur.execute(sql_content4)
                    conn.commit()
                    time.sleep(0.5)
#user_id=raw_input("请输入用户id:")
sql_content5="select user_id from user where permission=1;"
cur.execute(sql_content5)
user_id_list=cur.fetchall()
[gethtmlfun(i[0]) for i in user_id_list]
