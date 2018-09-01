#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'gaochao'

import config.mysql as mysql
import pymysql
import time

class Db(object):

    # 构造方法
    def __init__(self):
        # 初始化数据库链接
        self._db = pymysql.connect(mysql.DB_HOST,mysql.DB_USER,mysql.DB_PASSWORD,mysql.DB_NAME)

    # 获取实例
    @classmethod
    def instance(cls):
        if not hasattr(Db,"_instance"):
            cls._instance = Db()

        return cls._instance

    # 存储爬虫基本数据
    def save_base_info(self,data):
        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = self._db.cursor()
        now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # 使用 execute()  方法执行 SQL 查询
        sql = 'INSERT INTO base_info(title,`desc`,image,cook_magnet,fresh_magnet,other_magnet,c_t,u_t) values(\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\')'.format(data['title'],data['desc'],data['image'],data['cook_magnet'],data['fresh_magnet'],data['other_magnet'],now_time,now_time)
        print(sql)
        cursor.execute(sql)
        self._db.commit()

    # 析构函数
    def __del__(self):
        self._db.close()