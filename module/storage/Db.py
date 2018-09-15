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
        # 表名
        self._animation_table_name = "base_info"

    # 获取实例
    @classmethod
    def instance(cls):
        if not hasattr(Db,"_instance"):
            cls._instance = Db()

        return cls._instance

    # 存储爬虫基本数据
    def save_animation_base_info(self,data):
        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = self._db.cursor()
        now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # 使用 execute()  方法执行 SQL 查询
        field_list = []
        value_list = []
        for key,val in data.items() :
            field_list.append(key)
            value_list.append('\'' + val + '\'')
        field_list.extend(['c_t','u_t'])
        value_list.extend(['\'' + now_time + '\'','\'' + now_time + '\''])

        sql = 'INSERT INTO ' + self._animation_table_name + '(' + ','.join(field_list) + ')' + ' values(' + ','.join(value_list) + ')'
        print(sql)
        cursor.execute(sql)
        self._db.commit()

    # 获取所有未爬成功的数据
    def get_animation_all_fail_data(self):
        cursor = self._db.cursor(cursor=pymysql.cursors.DictCursor)
        sql = "SELECT * FROM `" + self._animation_table_name + "` WHERE cook_magnet = '[]' AND fresh_magnet = '[]' AND other_magnet = '[]';"

        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        return results

    # 更新未爬成功的数据
    def fix_animation_base_info(self,data):
        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = self._db.cursor()
        now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # 使用 execute()  方法执行 SQL 查询
        sql = 'UPDATE ' + self._animation_table_name + ' SET title=\'{}\',`describe`=\'{}\',title_md5=\'{}\',describe_md5=\'{}\',cook_magnet=\'{}\',fresh_magnet=\'{}\',other_magnet=\'{}\',u_t=\'{}\' WHERE id ={}'.format(
            data['title'],data['`describe`'],data['title_md5'],data['describe_md5'],data['cook_magnet'], data['fresh_magnet'], data['other_magnet'],now_time,data['id'])
        # print(sql)
        cursor.execute(sql)
        self._db.commit()

    # 清空表，并重置他的自增计数器
    def clear_animation_base_info(self):
        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = self._db.cursor()

        # 使用 execute()  方法执行 SQL 查询
        sql = 'truncate table ' + self._animation_table_name + ';'
        # print(sql)
        cursor.execute(sql)
        self._db.commit()

    # 根据base_url的散列值查出记录
    def get_animation_by_base_url(self,base_url_md5):
        cursor = self._db.cursor(cursor=pymysql.cursors.DictCursor)
        sql = "SELECT * FROM `" + self._animation_table_name + "` WHERE base_url_md5 = '" + base_url_md5 + "';"
        # print(sql)
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchone()
        return results

    # 析构函数
    def __del__(self):
        self._db.close()