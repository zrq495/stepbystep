#!/usr/bin/env python
#coding=utf-8

import re
import urllib2
import MySQLdb
import time
import datetime

conn = MySQLdb.connect('localhost', 'root', 'rootpass', 'stepbystep', charset='utf8')
cur = conn.cursor()

#proxy = {'http': '127.0.0.1:8087'}
#proxy_support = urllib2.ProxyHandler(proxy)
#opener = urllib2.build_opener(proxy_support)
#urllib2.install_opener(opener)

i_headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.48'}
base_url = 'http://poj.org/'

def get_html(url):
    req = urllib2.Request(url, headers=i_headers) 
    res = urllib2.urlopen(req)
    html = res.read()
    return html

def re_find(comp, html):
    rec = re.compile(r'%s' %(comp))
    data = rec.findall(html)
    return data

def crawl_solved(user):
    user_status_url = base_url + 'userstatus?user_id=%s' %(user[2])
    html = get_html(user_status_url)
    rank = re_find('<font color=red>(.*?)</font></td>', html)
    solved = re_find('<td align=center width=25%><a href=status\?result=0&user_id=.*?>(.*?)</a></td>', html)
    print rank, solved
    if rank and solved:
        cur.execute('update user set poj_solved=%d, poj_rank=%d where user_id="%s"' %(int(solved[0]), int(rank[0]), user[0]))
        conn.commit()

def del_repeat(d):
    k = d[0][:]
    for l in d[1:]:
        if l[1] != k[1]:
            yield k
            k = l
    yield k

def crawl_ac(user):
    user_all_solution = []
    top_status_url = base_url + 'status?result=0&user_id=%s' %(user[2])
    html = get_html(top_status_url)
    re_rule = '<tr align=center><td>(.*?)</td><td><a href=userstatus\?user_id=.*?<a href=problem\?id=(.*?)>.*?</font></td><td>.*?</td><td>.*?</td><td>.*?</td><td>.*?</td><td>(.*?)</td></tr>'
    solution = re_find(re_rule, html)
    while solution:
        user_all_solution.extend(solution)
        next_status_url = top_status_url + '&top=%s' %(solution[-1][0])
        html = get_html(next_status_url)
        solution = re_find(re_rule, html)
    user_all_solution.sort(key=lambda x:(int(x[1]), int(x[0])))
    user_all_solution = list(del_repeat(user_all_solution))

if __name__ == '__main__':
    print time.ctime()
    cur.execute('select * from user where permission=1')
    user = cur.fetchall()
    for u in user:
        crawl_solved(u)
        crawl_ac(u)
