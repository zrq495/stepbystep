#!/usr/bin/env python
#coding=utf-8

import web
import datetime

#数据库链接
db = web.database(dbn='mysql', db='stepbystep', user='root', pw='rootpass')

#模板位置
render = web.template.render('templates/', cache=False)

#是否调试
web.config.debug = False

config = web.storage(
    email = 'zrq495@gmail.com',
    static = '/static',
    today = datetime.date.today(),
    )

web.template.Template.globals['config'] = config
web.template.Template.globals['render'] = render

