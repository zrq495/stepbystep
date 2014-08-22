#!/usr/bin/env python
#coding=utf-8

import re
import urllib2
import MySQLdb
import time
import datetime

conn = MySQLdb.connect('localhost','root','123456','stepbystep',charset='utf8')
cur =conn.cursor()
temp_conn = MySQLdb.connect('localhost', 'root', '123456', 'oj', charset='utf8')
temp_cur = temp_conn.cursor()

#proxy = {'http':'127.0.1:8087'}
#proxy_support = urllib2.ProxyHandler(proxy)
#opener = urllib2.build_opener(proxy_support)
#urllib2.install_opener(opener)
i_headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.48'}

today = datetime.date.today()

# oj信息，第一个是oj做题数（rating）在数据库中的字段名，第二个是用户在该oj的用户名字段在数据库中的列数， 第三个是oj上做题数有关的页面，第四个是匹配做题数的正则表达式。
# poj和sdutoj不加，特殊处理
oj_info = [
["hdoj_solved", 14, "http://acm.hdu.edu.cn/userstatus.php?user=%s", "<tr><td>Problems Solved</td><td align=center>(\d+)</td></tr>"],
["cf_rating", 16, "http://codeforces.com/profile/%s", "<span style=\"font-weight:bold;\" class=\"user-.*?\">(\d+)</span> <span"],
["tc_rating", 18, "http://community.topcoder.com/tc?module=SimpleSearch&ha=%s", "Rating</a></h3>[\s\S]*?<span class=\".*?\">(\d+)</span>"],
["bc_rating", 20, "http://bestcoder.hdu.edu.cn/rating.php?user=%s", "<p>Rating: </p>[\s\S]*?<p>(\d+) \(max \d+\)</p>"],
]

re_sdutoj = re.compile(r'<td align="right">Accept[\s\S]*?<td align="left">(\d+)</td>')
re_poj_ac = re.compile(r'<tr align=center><td>.*?</td><td><a href=userstatus\?user_id=.*?</a></td><td><a href=problem\?id=.*?</a></td><td><font color=blue>Accepted</font></td><td>.*?</td><td>.*?</td><td>.*?</td><td>.*?</td><td>(.*?)</td></tr>')
re_poj_pro = re.compile(r'p\((\d{4})\)')
re_poj_rank = re.compile(r'<font color=red>(.*?)</font></td>')
re_poj_solved = re.compile(r'<td align=center width=25%><a href=status\?result=0&user_id=.*?>(.*?)</a></td>')


def get_html(url):
    req = urllib2.Request(url, headers=i_headers) 
    res = urllib2.urlopen(req, timeout=10)
    html = res.read()
    return html


def re_find(comp, html):
    rec = re.compile(r'%s' %(comp))
    data = rec.findall(html)
    return data


def poj_ac(user, solved_problem):
    if user[2]:
        cur.execute('select * from problem')
        problem = cur.fetchall()
        for pro in problem:
            cur.execute('select * from solution s where s.user_id=%d and s.pid=%d' %(user[0], pro[0]))
            solution = cur.fetchall()
            if solution:
                #print user[1].encode('utf8'), pro[1], solution[0][2], 'exist'
                pass
            else:
                if str(pro[1]) in solved_problem:
                    statusurl = 'http://poj.org/status?problem_id=%d&user_id=%s&result=0&language=' %(pro[1], user[2]) 
                    html = get_html(statusurl)
                    datas = re_poj_ac.findall(html)
                    if datas:
                        actime = datas[-1]
                        print user[1].encode('utf8'), pro[1], actime , 'new !!!'
                        cur.execute('insert into solution(user_id, pid, actime) values(%d, %d, "%s")' %(user[0], pro[0], actime.split()[0]))
                        conn.commit()
                    else:
                        #print user[1].encode('utf8'), pro[1], 'waiting'
                        pass
                    time.sleep(0.5)
                #print user[1].encode('utf8'), pro[1], 'waiting'


def poj_solved(user):
    if user[2]:
        userstatusurl = 'http://poj.org/userstatus?user_id=%s' %(user[2])
        html = get_html(userstatusurl)
        rank = re_poj_rank.findall(html)
        solved = re_poj_solved.findall(html)
        problem = re_poj_pro.findall(html)
        print 'poj', rank, solved
        if rank and solved:
            cur.execute('update user set poj_solved=%d, poj_rank=%d where user_id="%s"' %(int(solved[0]), int(rank[0]), user[0]))
            conn.commit()
        return problem


def sdutoj_solved(user):
    if user[12]:
        temp_cur.execute('select user_id from user where user_name="%s"' % user[12])
        user_id = temp_cur.fetchall()
        if user_id:
            user_id = user_id[0]
            userstatusurl = 'http://acm.sdut.edu.cn/sdutoj/setting.php?userid=%s' %user_id
            html = get_html(userstatusurl)
            solved = re_sdutoj.findall(html)
            print 'sdutoj', solved
            if solved:
                cur.execute('update user set sdutoj_solved=%d where user_id="%s"' %(int(solved[0]), user[0]))
                conn.commit()


def oj_solved(user, info):
    if user[info[1]]:
        userstatusurl = info[2] % user[info[1]]
        html = get_html(userstatusurl)
        solved = info[3].findall(html)
        print info[0], solved
        if solved:
            cur.execute('update user set %s=%d where user_id="%s"' % (info[0], int(solved[0]), user[0]))
            conn.commit()


if __name__ == '__main__':
    print time.ctime()
    cur.execute('select * from user')
    user = cur.fetchall()
    for oj in oj_info:
        oj[3] = re.compile(r"%s" % oj[3])
    for u in user:
        try:
            print u[1].encode('utf-8')
            solved_problem = poj_solved(u)
            poj_ac(u, solved_problem)
            sdutoj_solved(u)
            for oj in oj_info:
                oj_solved(u, oj)
        except Exception:
            pass
    print time.ctime()
