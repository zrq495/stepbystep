#!/usr/bin/env python
#coding=utf-8

import web
import os
import hashlib
import time

web.config.debug = False

urls =  (
    '/', 'index',
    '/admin', 'admin',
    '/statistics', 'statistics',
)

app = web.application(urls, globals())
db = web.database(dbn='mysql', db='stepbystep', user='root', pw='rootpass')
render = web.template.render('templates/', cache=False)

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
        user = db.query('select * from user where permission=1 order by grade desc, user_id desc')
        problem = db.query('select * from problem order by pid')
        #solution = db.query('select * from solution order by pid')
        solution = db.query('select solution.pid, solution.user_id, solution.actime from solution,user,problem where user.user_id = solution.user_id and problem.pid = solution.pid order by solution.pid, user.grade desc, user.user_id desc')
        #solution = db.query('select solution.pid, solution.user_id, solution.actime from solution,user,problem where user.user_id = solution.user_id and problem.pid = solution.pid order by solution.pid desc, user.grade asc, user.user_id asc')
        user = list(user)
        problem = list(problem)
        solution = list(solution)
        table_width = str(len(user)*100) + 'px'
        starttime = time.clock()
        pro_list = []
        flag = 0
        #for pro in problem:
        #    p_list = []
        #    for u in user:
        #        #flag = 0
        #        #for solu in solution:
        #        #    if solu.pid == pro.pid and u.user_id == solu.user_id:
        #        #        p_list.append(solu.actime)
        #        #        del solution[0]
        #        #        flag = 1
        #        #        break
        #        #if flag == 0:
        #        #    p_list.append(' ')
        #        if flag == 0 and solution[0].pid == pro.pid and u.user_id == solution[0].user_id:
        #            p_list.append(solution[0].actime)
        #            del solution[0]
        #            if not solution:
        #                flag = 1
        #                continue
        #            continue
        #        p_list.append(' ')
        #    pro_list.append(p_list)
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
        #return render.index(user, problem, solution, table_width, cate_len)
        return render.index(pro_list, user, problem, table_width, cate_len)

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

if __name__ == '__main__':
    app.run()
