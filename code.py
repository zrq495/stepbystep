#!/usr/bin/env python
#coding=utf-8

import web
import os
import hashlib
import time
import datetime

web.config.debug = False

urls =  (
    '/', 'index',
    '/admin', 'admin',
    '/statistics', 'statistics',
    '/statistics/(.+)', 'statistics_year',
)

app = web.application(urls, globals())
db = web.database(dbn='mysql', db='stepbystep', user='root', pw='rootpass')
render = web.template.render('templates/', cache=False)
web.template.Template.globals['render'] = render

curdir = os.path.dirname(__file__)
session = web.session.Session(app, web.session.DiskStore(curdir + '/' + 'sessions'), initializer={'login': 0, 'privilege':0})

cate_len = [13, 20, 17, 14, 9, 12, 7, 7, 19, 17, 5, 14, 26, 15, 7, 24, 10, 15, 10, 4, 4, 9]
rank = ['初级', '中级', '高级']

def logged():
    if session.login == 0:
        return False
    else:
        return True

def create_render(privilege):
    if logged():
        if privilege == 2:
            render = web.template.render('templates/admin/')
        else:
            render = web.template.render('templates/')
    else:
        render = web.template.render('templates/')
    return render

def hashpasswd(passwd):
    pre = 'sA2lT7!54-'
    return hashlib.sha1(pre + passwd).hexdigest()

class index:
    def GET(self):
        starttime = time.clock()
        #user = db.query('select * from user where permission=1 order by grade desc, user_id desc')
        user = db.query(' select u.*, count(s.user_id) as "count" from solution s, user u where s.user_id = u.user_id and u.permission = 1 group by s.user_id order by u.grade desc, u.user_id desc')
        problem = db.query('select * from problem order by pid')
        solution = db.query('select solution.pid, solution.user_id, solution.actime from solution,user,problem where user.user_id = solution.user_id and problem.pid = solution.pid order by solution.pid, user.grade desc, user.user_id desc')
        user = list(user)
        problem = list(problem)
        solution = list(solution)
        table_width = str(len(user)*100) + 'px'
        pro_list = []
        flag = 0
        for pro in problem:
            p_str = '<tr>'
            for u in user:
                if flag == 0 and solution[0].pid == pro.pid and u.user_id == solution[0].user_id:
                    p_str += '<td class="success">' + solution[0].actime + '</td>'
                    del solution[0]
                    if not solution:
                        flag = 1
                        continue
                    continue
                p_str += '<td>&nbsp;</td>'
            p_str += '</tr>'
            pro_list.append(p_str)
        endtime = time.clock()
        print endtime - starttime
        return render.index(pro_list, user, table_width, problem, cate_len)

class admin:
    def GET(self):
        if logged():
            pass
    def POST(self):
        pass

class statistics:
    def GET(self):
        user = db.query('select * from user where permission=1 order by grade desc, user_id desc')
        count = []
        for u in user:
            singlecount = []
            singlecount.append(u.user_name)
            for r in rank:
                sc = db.query('select count(solution.pid) as cnt from solution, problem where solution.user_id="%s" and solution.pid = problem.pid and problem.cid in (select cid from category where rank="%s")' %(u.user_id, r))[0]
                singlecount.append(int(sc.cnt))
            singlecount.append(sum(singlecount[1:]))
            count.append(singlecount)
        return render.statistics(count)

class statistics_year:
    def GET(self, year='year'):
        today = datetime.date.today()
        start_year = 2011
        this_year = today.year
        try:
            if year == 'year': 
                year = this_year
            if int(year) >= start_year and int(year) <= this_year:
                year = int(year)
        except:
            error = '年份错误！'
            return render.error(error, '/statistics/year')
        else:
            user = db.query('select * from user where permission=1 order by grade desc, user_id desc')
            count = []
            for u in user:
                cnt = [0] * 14
                data = db.query('select * from solution, user where solution.user_id = user.user_id  and user.user_id = "%s" and solution.actime like "''%s''%%"' %(u.user_id, year))
                data = list(data)
                cnt[0] = u.user_name
                cnt[13] = len(data)
                for d in data:
                    cnt[int(d.actime.split('-')[1])] += 1
                count.append(cnt)
            return render.statistics_year(count, year, start_year, this_year)

if __name__ == '__main__':
    app.run()
