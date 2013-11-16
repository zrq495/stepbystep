#!/usr/bin/env python
#coding=utf-8

import web

web.config.debug = True 

urls =  (
    '/', 'index',
    '/admin', 'admin'
)

app = web.application(urls, globals())
db = web.database(dbn='mysql', db='stepbystep', user='root', pw='rootpass')
render = web.template.render('templates/', cache=False)

cate_len = [13, 20, 17, 14, 9, 12, 7, 7, 19, 17, 5, 14, 26, 15, 7, 24, 10, 15, 10, 4, 4, 9]

class index:
    def GET(self):
        user = db.query('select * from user order by grade desc, user_id desc')
        problem = db.query('select * from problem order by pid')
        solution = db.query('select * from solution')
        user = list(user)
        problem = list(problem)
        solution = list(solution)
        #print user
        #print problem
        #print solution
        table_width = str(len(user)*100) + 'px'
        return render.index2(user, problem, solution, table_width, cate_len)

class admin:
    def GET(self):
        pass
    def POST(self):
        pass

if __name__ == '__main__':
    app.run()
