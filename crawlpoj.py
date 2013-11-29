#!/usr/bin/env python
#coding=utf-8

import re
import urllib2
import MySQLdb
import time

conn = MySQLdb.connect('localhost','root','rootpass','stepbystep',charset='utf8')
cur =conn.cursor()

def crawl(user):
    cur.execute('select * from problem')
    problem = cur.fetchall()
    for pro in problem:
        cur.execute('select * from solution s where s.user_id=%d and s.pid=%d' %(user[0], pro[0]))
        solution = cur.fetchall()
        if solution:
            print user[1].encode('utf8'), pro[1], solution[0][2]
        else:
            statusurl = 'http://poj.org/status?problem_id=%d&user_id=%s&result=0&language=' %(pro[1], user[2]) 
            response = urllib2.urlopen(statusurl)
            html = response.read()
            tr = re.compile(r'<tr align=center><td>.*?</td><td><a href=userstatus\?user_id=.*?</a></td><td><a href=problem\?id=.*?</a></td><td><font color=blue>Accepted</font></td><td>.*?</td><td>.*?</td><td>.*?</td><td>.*?</td><td>(.*?)</td></tr>')
            datas = tr.findall(html)
            if datas:
                actime = datas[-1]
                print user[1].encode('utf8'), pro[1], actime , 'new'
                cur.execute('insert into solution(user_id, pid, actime) values(%d, %d, "%s")' %(user[0], pro[0], actime.split()[0]))
                conn.commit()
                time.sleep(0.5)

if __name__ == '__main__':
    cur.execute('select * from user')
    user = cur.fetchall()
    print time.ctime()
    for u in user:
        crawl(u)
