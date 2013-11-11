#!/usr/bin/env python
#coding=utf-8

import re
import urllib2

def crawl(username, problemid):
    statusurl = 'http://poj.org/status?problem_id=%s&user_id=%s&result=0&language=' %(problemid, username) 
    response = urllib2.urlopen(statusurl)
    html = response.read()
    tr = re.compile(r'<tr align=center><td>.*?</td><td><a href=userstatus\?user_id=.*?</a></td><td><a href=problem\?id=.*?</a></td><td><font color=blue>Accepted</font></td><td>.*?</td><td>.*?</td><td>.*?</td><td>.*?</td><td>(.*?)</td></tr>')
    datas = tr.findall(html)
    if datas:
        print datas[-1].split()[0]

if __name__ == '__main__':
    #username = raw_input('username:')
    #problemid = raw_input('problemid:')
    #crawl(username, problemid)
    crawl('pony1993', '3415')
