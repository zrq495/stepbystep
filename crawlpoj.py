#!/usr/bin/env python
#coding=utf-8

import re
import urllib2
import MySQLdb
import time
import datetime

conn = MySQLdb.connect('localhost','root','rootpass','stepbystep',charset='utf8')
cur =conn.cursor()

#proxy = {'http':'27.24.158.155:84'}                                                                                
proxy = {'http':'127.0.1:8087'}
proxy_support = urllib2.ProxyHandler(proxy)
opener = urllib2.build_opener(proxy_support)
urllib2.install_opener(opener)
i_headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.48'}

today = datetime.date.today()

def get_html(url):
    req = urllib2.Request(url, headers=i_headers) 
    res = urllib2.urlopen(req)
    html = res.read()
    return html

def re_find(comp, html):
    rec = re.compile(r'%s' %(comp))
    data = rec.findall(html)
    return data

def crawl_ac(user, t):
    cur.execute('select * from problem')
    problem = cur.fetchall()
    for pro in problem:
        cur.execute('select * from solution s where s.user_id=%d and s.pid=%d' %(user[0], pro[0]))
        solution = cur.fetchall()
        if solution:
            print user[1].encode('utf8'), pro[1], solution[0][2]
        else:
            tt = checkproblem(pro, t)
            if tt:
                statusurl = 'http://poj.org/status?problem_id=%d&user_id=%s&result=0&language=' %(pro[1], user[2]) 
                html = get_html(statusurl)
                datas = re_find('<tr align=center><td>.*?</td><td><a href=userstatus\?user_id=.*?</a></td><td><a href=problem\?id=.*?</a></td><td><font color=blue>Accepted</font></td><td>.*?</td><td>.*?</td><td>.*?</td><td>.*?</td><td>(.*?)</td></tr>', html)
                if datas:
                    actime = datas[-1]
                    print user[1].encode('utf8'), pro[1], actime , 'new'
                    cur.execute('insert into solution(user_id, pid, actime) values(%d, %d, "%s")' %(user[0], pro[0], actime.split()[0]))
                    conn.commit()
                else:
                    print user[1].encode('utf8'), pro[1], tt, pro[-1]
                time.sleep(0.5)

def crawl_solved(user):
    userstatusurl = 'http://poj.org/userstatus?user_id=%s' %(user[2])
    html = get_html(userstatusurl)
    rank = re_find('<font color=red>(.*?)</font></td>', html)
    solved = re_find('<td align=center width=25%><a href=status\?result=0&user_id=.*?>(.*?)</a></td>', html)
    print rank, solved
    if rank and solved:
        cur.execute('update user set poj_solved=%d, poj_rank=%d where user_id="%s"' %(int(solved[0]), int(rank[0]), user[0]))
        conn.commit()

def checkuser(user):
    t = (today.year - user[3]) / 4
    if t < 1:
        t = 1
    else:
        t = today.year - user[3] - 1
    if today.toordinal() % t == 0:
        return t
    return 0

def checkproblem(pro, t):
    if pro[-1] > 14:
        t *= 3
    elif pro[-1] > 7:
        t *= 2
    if today.toordinal() % t == 0:                                                               
        return t
    else:
        return 0

if __name__ == '__main__':
    cur.execute('select * from user')
    user = cur.fetchall()
    print time.ctime()
    for u in user:
        t = checkuser(u)
        if t:
            crawl_solved(u)
            crawl_ac(u, t)
