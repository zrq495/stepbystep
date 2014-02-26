#!/usr/bin/env python
#coding=utf-8

import web
import os
import hashlib
import time
import datetime
import xlrd
import logging
import json
from autocache import memorize
from config import settings
from config.url import urls

app = web.application(urls, globals())

db = settings.db
render = settings.render

#session
curdir = os.path.dirname(__file__)
session = web.session.Session(app, web.session.DiskStore(os.path.join(curdir, 'sessions')), initializer={'login': 0})

#日志
logging.basicConfig(filename = os.path.join(os.getcwd(), 'log.txt'), level = logging.INFO, format = '%(asctime)s - %(levelname)s: %(message)s')

cate_len = [13, 20, 17, 14, 9, 12, 7, 7, 19, 17, 5, 14, 26, 15, 7, 24, 10, 15, 10, 4, 4, 9]   #每个分类的题数
rank = ['初级', '中级', '高级']   
rank_len = [7, 7, 8]    #每个等级的分类数

def is_valid_date(str):
    '''
    判断日期合法性
    '''
    try:
        time.strptime(str, "%Y-%m-%d")
        return True
    except Exception, e:
        logging.error(e)
        return False

def split_date(date):
    '''
    生成日期实例
    '''
    y = int(date.split('-')[0])
    m = int(date.split('-')[1])
    d = int(date.split('-')[2])
    return datetime.date(y, m, d)

def hashpasswd(passwd):
    '''
    加密密码
    '''
    pre = 'sA2lT7!54-'
    return hashlib.sha1(pre + passwd).hexdigest()

def logged():
    '''
    判断是否登录
    '''
    if session.login == 0:
        return False
    else:
        return True

class index:
    '''
    首页
    '''
    @memorize(3600)
    def GET(self):
        today = datetime.date.today()
        week_start = today - datetime.timedelta(today.weekday())
        week_end = week_start + datetime.timedelta(6)
        week_start = str(week_start).replace('-', '/')
        week_end = str(week_end).replace('-', '/')
        user = db.query('select u.user_id, u.user_name, u.class1, count(s.user_id) as "count" from solution s, user u where s.user_id = u.user_id and u.permission = 1 group by s.user_id order by u.grade desc, u.user_id desc')
        problem = db.query('select pid, deadline from problem order by pid')
        user = list(user)
        problem = list(problem)
        table_width = str(len(user)*100) + 'px'
        print week_start, week_end
        return render.index(user, table_width, problem, cate_len, week_start, week_end)
    def POST(self):
        user = db.query('select u.user_id, u.user_name, u.class1, count(s.user_id) as "count" from solution s, user u where s.user_id = u.user_id and u.permission = 1 group by s.user_id order by u.grade desc, u.user_id desc')
        problem = db.query('select pid, deadline from problem order by pid')
        solution = db.query('select solution.pid, solution.user_id, solution.actime from solution,user,problem where user.user_id = solution.user_id and problem.pid = solution.pid and user.permission=1 order by solution.pid, user.grade desc, user.user_id desc')
        user = list(user)
        problem = list(problem)
        solution = list(solution)
        pro_list = []
        flag = 0
        for pro in problem:
            pk = pro.pid
            pv = []
            for u in user:
                if flag == 0 and solution[0].pid == pro.pid and u.user_id == solution[0].user_id:
                    pv.append(solution[0].actime)
                    del solution[0]
                    if not solution:
                        flag = 1
                        continue
                else:
                    pv.append('')
            pd = dict([(pk, pv)])
            pro_list.append(pd)
        return json.dumps(pro_list, separators=(',',':'))

class login:
    '''
    登录
    '''
    def GET(self):
        if logged():
            raise web.seeother('/admin')
        return render.login()
    def POST(self):
        username = web.input().username
        passwd = web.input().passwd
        try:
            ident = db.query('select * from user where user_name = "%s" and permission = 2' %username)[0]
            if ident.passwd == hashpasswd(passwd):
                session.login = 1
                #raise web.seeother('/admin')
                user = db.query('select * from user where permission != 2 order by grade desc, user_id desc')
                category = db.query('select problem.cid, category.rank, category.cname, problem.deadline from problem, category where problem.cid = category.cid group by problem.cid order by problem.cid')
                start_date = db.query('select * from startdate order by DATE_FORMAT(start_date, "%%Y-%%m-%%d") desc')
                user = list(user)
                category = list(category)
                start_date = list(start_date)
                logging.info('登录成功：' + username.encode('utf8') + ':' + passwd.encode('utf8'))
                return render.admin(user, category, rank_len, start_date)
            else:
                logging.info('登录失败：' + username.encode('utf8') + ':' + passwd.encode('utf8'))
                return render.error('用户名或密码错误！', '/login')
        except Exception, e:
            logging.info('登录失败：' + username.encode('utf8') + ':' + passwd.encode('utf8'))
            logging.error(e)
            session.login = 0
            return render.error('error !', '/login')

class admin:
    '''
    管理
    '''
    def GET(self):
        if logged():
            user = db.query('select * from user where permission != 2 order by grade desc, user_id desc')
            category = db.query('select problem.cid, category.rank, category.cname, problem.deadline from problem, category where problem.cid = category.cid group by problem.cid order by problem.cid')
            start_date = db.query('select * from startdate order by DATE_FORMAT(start_date, "%%Y-%%m-%%d") desc')
            user = list(user)
            category = list(category)
            start_date = list(start_date)
            return render.admin(user, category, rank_len, start_date)
        else:
            raise web.seeother('/login')
    def POST(self):
        pass

class disabled:
    '''
    禁用用户
    '''
    def GET(self, user_id, permission):
        if not logged():
            raise web.seeother('/login')
        try:
            if permission == '0':
                db.query('update user set permission=1 where user_id = "%s" and permission=0' %user_id)
            elif permission == '1':
                db.query('update user set permission=0 where user_id = "%s" and permission=1' %user_id)
            else:
                raise 'error'
        except Exception, e:
            logging.error(e)
            return render.error('disabled or enable error !', '/admin')
        raise web.seeother('/admin')

class edituser:
    '''
    编辑用户, 包括单个和批量
    '''
    def GET(self):
        if logged():
            raise web.seeother('/admin')
        else:
            raise web.seeother('/login')
    def POST(self):
        if logged():
            for key in web.input().keys():
                value = web.input().get(key)
                if value:
                    try:
                        if key.startswith('editusername'):
                            l = key.split('-')[1]
                            db.query('update user set user_name="%s" where user_id="%s"' %(value.encode('utf-8'), l))
                        elif key.startswith('edituserpojname'):
                            l = key.split('-')[1]
                            db.query('update user set poj_name="%s" where user_id="%s"' %(value.encode('utf-8'), l))
                        elif key.startswith('editusergrade'):
                            l = key.split('-')[1]
                            db.query('update user set grade="%s" where user_id="%s"' %(value.encode('utf-8'), l))
                        elif key.startswith('edituserclass'):
                            l = key.split('-')[1]
                            db.query('update user set class1="%s" where user_id="%s"' %(value.encode('utf-8'), l))
                        else:
                            return render.error('input error !', '/admin')
                    except Exception, e:
                        logging.error(e)
                        return render.error('update user error !', '/admin')
            raise web.seeother('/admin')
        else:
            raise web.seeother('/login')

class editdeadline:
    '''
    编辑完成时间
    '''
    def GET(self):
        raise web.seeother('/login')
    def POST(self):
        if logged():
            for key in web.input().keys():
                try:
                    value = web.input().get(key)
                    if not is_valid_date(value):
                        return render.error('error !', '/admin')
                    if value:
                        l = key.split('-')[1]
                        db.query('update problem set deadline="%s" where cid = "%s"' %(value.encode('utf-8'), l))
                    else:
                        return render.error('error !', '/admin')
                except Exception, e:
                    logging.error(e)
                    return render.error('update deadline error !', '/admin')
            raise web.seeother('/admin')
        else:
            raise web.seeother('/login')

class adduser:
    '''
    添加用户，包括单个和批量
    '''
    def GET(self):
        raise web.seeother('/login')
    def POST(self):
        if logged():
            usernumber = web.input().get('usernumber-999999')
            items = web.input().items()
            items = sorted(items, key=lambda x:(x[0].split('-')[1], x[0].split('-')[0]))
            error = ''
            inserterror = ''
            for i in range(0, len(items)-1, 4):
                if items[i][1] and items[i+1][1] and items[i+2][1] and items[i+3][1]:
                    try:
                        if len(db.query('select * from user where user_name="%s" and class1="%s"' %(items[i+2][1], items[i][1]))):
                            error += items[i+2][1].encode('utf-8') + '<br>'
                        else:
                            db.query('insert into user(user_id, user_name, poj_name, grade, class1, permission) values(null, "%s", "%s", "%s", "%s", 1)' %(items[i+2][1], items[i+3][1], items[i+1][1], items[i][1]))
                    except Exception, e:
                        logging.error(e)
                        inserterror += items[i+2][1].encode('utf-8') + '<br>'
            content = '用户：<br>' + error
            if error:
                content += '已存在！<br>'
            if inserterror:
                content += '插入错误！<br>'
            if error or inserterror:
                return render.error(content, '/admin')
            raise web.seeother('/admin')
        else:
            raise web.seeother('/login')

class uploadfile:
    '''
    上传文件
    '''
    def GET(self):
        raise web.seeother('/login')
    def POST(self):
        if logged():
            x = web.input(myfile={})
            filedir = 'upload'
            if 'myfile' in x:
                filepath = x.myfile.filename.replace('\\', '/') 
                filename = filepath.split('/')[-1]
                logging.info('文件上传：' + filename)
                if filename.split('.')[-1] != 'xls' and filename.split('.')[-1] != 'xlsx':
                    return render.error('文件格式错误！', '/admin')
                fout = open(filedir + '/' + filename, 'wb')
                fout.write(x.myfile.file.read())
                fout.close()
                data = xlrd.open_workbook(filedir + '/' + filename)
                table = data.sheet_by_index(0)
                nrows = table.nrows
                user = []
                for i in range(nrows):
                    u = []
                    u.append(i)
                    for v in table.row_values(i):
                        if type(v) == float:
                            v = int(v)
                        u.append(v)
                    #u.extend(table.row_values(i))
                    user.append(u)
                return render.confirm(user)
            else:
                return render.error('请选择需要上传的文件！', '/admin')
        raise web.seeother('/login')

class statistics:
    '''
    总统计
    '''
    @memorize(3600)
    def GET(self):
        user = db.query('select * from user where permission=1 order by grade desc, user_id desc')
        count = []
        for u in user:
            singlecount = []
            singlecount.append(u.user_name + ' ' + u.class1)
            for r in rank:
                sc = db.query('select count(solution.pid) as cnt from solution, problem where solution.user_id="%s" and solution.pid = problem.pid and problem.cid in (select cid from category where rank="%s")' %(u.user_id, r))[0]
                singlecount.append(int(sc.cnt))
            singlecount.append(sum(singlecount[1:]))
            singlecount.append(u.poj_solved)
            singlecount.append(u.poj_rank)
            singlecount.append(u.poj_name)
            count.append(singlecount)
        count.sort(key=lambda x:(int(x[1])*1+int(x[2])*3+int(x[3])*10+(int(x[5])-int(x[4]))*2, x[5]), reverse=True)
        #初级×1 中级×3 高级×10 其他×2
        return render.statistics(count)

class statistics_year:
    '''
    按月统计
    '''
    @memorize(3600)
    def GET(self, year='year'):
        today = datetime.date.today()
        start_year = 2011
        this_year = today.year
        try:
            if year == 'year': 
                year = this_year
            if int(year) >= start_year and int(year) <= this_year:
                year = int(year)
            else:
                error = '年份错误！'
                return render.error(error, '/statistics/year')
        except Exception, e:
            logging.error(e)
            error = '年份错误！'
            return render.error(error, '/statistics/year')
        else:
            user = db.query('select * from user where permission=1 and grade>=%d and grade<=%d order by grade desc, user_id desc' %(year - 4, year))
            count = []
            for u in user:
                cnt = [0] * 15
                data = db.query('select * from solution, user where solution.user_id = user.user_id  and user.user_id = "%s" and solution.actime like "''%s''%%"' %(u.user_id, year))
                data = list(data)
                cnt[0] = u.user_name + ' ' + u.class1
                cnt[13] = len(data)
                cnt[14] = u.poj_name
                for d in data:
                    cnt[int(d.actime.split('-')[1])] += 1
                count.append(cnt)
            return render.statistics_year(count, year, start_year, this_year)

class statistics_week:
    '''
    按周统计，寒假、上半年、暑假、下半年分别为1、2、3、4。
    '''
    @memorize(3600)
    def GET(self, year, half):
        start_year = 2011               
        today = datetime.date.today()
        try:
            all_start_date = db.query('select start_date, half from startdate order by DATE_FORMAT(start_date, "%%Y-%%m-%%d")')             #查询所有开始时间，不包括寒暑假
            all_start_date = list(all_start_date)
        except Exception, e:
            logging.error(e)
            return render.error('查询错误！', '/statistics/year/week/half')
        t = []
        for i in all_start_date:      #生成所有开始时间
            i.start_date = split_date(i.start_date)
            i = dict(i)
            t.append(i)
            t.append({'start_date': i['start_date'] + datetime.timedelta(140), 'half': (i['half'] + 1) % 4})
        all_start_date = t
        all_start_date.append({'start_date': today, 'half': 999999})
        all_start_date.sort(key=lambda x:(x['start_date'], x['half']))       #按时间排序
        t = all_start_date
        for i, item in enumerate(all_start_date):     #查找today所在位置
            if item['half'] == 999999:
                item['half'] = all_start_date[i-1]['half']
                today_and_half = item
                del all_start_date[i]
                break
        flag_year = 0 
        if year == 'year' and half == 'half':
            year = today.year
            half = today_and_half['half']
            flag_year = 1
        else:
            try:
                year = int(year)
                half = int(half)
                if year < start_year or year > today.year:
                    return render.error('年份错误！', '/statistics/year/week/half')
                if half != 1 and half != 2 and half != 3 and half != 4:
                    return render.error('url error', '/statistics/year/week/half')
            except Exception, e:
                logging.error(e)
                return render.error('url error', '/statistics/year/week/half')
        flag = 0
        for i, item in enumerate(all_start_date):    #查找开始和结束时间
            if item['start_date'].year == year and item['half'] == half:
                start_date = item['start_date']
                if flag_year:
                    end_date = today
                else:
                    end_date = all_start_date[i+1]['start_date'] - datetime.timedelta(1)
                flag = 1
                break
        if not flag:
            return render.error('error', '/statistics/year/week/half')
        try:
            user = db.query('select * from user where permission=1 and grade>%d and grade<%d order by grade desc, user_id desc' %(year-4, year))
            user = list(user)
        except Exception, e:
            logging.error(e)
            return render.error('查询错误！', '/statistics/year/week/half')
        all_week = []
        t = start_date
        i = 0
        while t<=end_date:
            s = '%s' %t
            e = '%s' %(t + datetime.timedelta(6))
            t += datetime.timedelta(7)
            all_week.append([s, e, '第%d周' %(i+1)])
            i += 1
        try:
            data = db.query('select * from solution s, user u \
                            where u.user_id = s.user_id and u.permission=1 and u.grade>%d and u.grade<%d\
                            and DATE_FORMAT(s.actime, "%%Y-%%m-%%d") >= DATE_FORMAT("%s", "%%Y-%%m-%%d") \
                            and DATE_FORMAT(s.actime, "%%Y-%%m-%%d") <= DATE_FORMAT("%s", "%%Y-%%m-%%d") \
                            order by DATE_FORMAT(s.actime, "%%Y-%%m-%%d"), u.grade desc, u.user_id desc' \
                            %(year-4, year, start_date, end_date))
            data = list(data)
        except Exception, e:
            logging.error(e)
            return render.error('查询错误！', '/statistics/year/week/half')
        all_week_user = []
        flag = 0
        for week in all_week:          #统计题数
            week_user = {u.user_name : [0, u.grade, u.user_id, u.class1] for u in user}
            if not flag:
                for d in data:
                    if split_date(d.actime) >= split_date(week[0]) and split_date(d.actime) <= split_date(week[1]):
                        week_user[d.user_name][0] += 1
            all_week_user.append(sorted(week_user.items(), key=lambda x:(x[1][1], x[1][2]), reverse=1))
        all_week.reverse()
        all_week_user.reverse()
        table_width = str(len(user)*100) + 'px'
        return render.statistics_week(user, all_week, all_week_user, table_width, year, half, start_year, today_and_half)
    def POST(self):
        year, half = web.input().select_year, web.input().select_half
        raise web.seeother('statistics/%s/week/%s' %(year, half))

class logout:
    '''
    注销
    '''
    def GET(self):
        session.login = 0
        session.kill()
        raise web.seeother('/')

#from web.httpserver import StaticMiddleware
#application = app.wsgifunc(StaticMiddleware)
if __name__ == '__main__':
    app.run()
