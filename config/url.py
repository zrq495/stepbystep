#!/usr/bin/env python
#coding=utf-8

urls =  (
    '/', 'index',
    '/login', 'login',
    '/admin', 'admin',
    '/logout', 'logout',
    '/statistics/(.+)/week/(.+)', 'statistics_week',
    '/statistics_week', 'statistics_week',
    '/statistics/(.+)', 'statistics_year',
    '/statistics', 'statistics',
    '/disabled/(.+)/(.+)', 'disabled',
    '/edituser', 'edituser',
    '/editdeadline', 'editdeadline',
    '/adduser', 'adduser',
    '/uploadfile', 'uploadfile',
    '/statistics_all', 'statistics_all',
)
