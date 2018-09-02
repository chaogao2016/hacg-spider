#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'gaochao'

import config.app as app
from module.storage.File import File
from module.storage.Db import Db

class Storage(object):

    # 构造方法
    def __init__(self):
        pass

    # 存储爬虫基本数据
    @classmethod
    def save_base_info(cls,data):
        if app.STORAGE_DRIVER == 1 :
            File.instance().save_base_info(data)
        elif app.STORAGE_DRIVER == 2 :
            Db.instance().save_base_info(data)
        elif app.STORAGE_DRIVER == 3 :
            File.instance().save_base_info(data)
            Db.instance().save_base_info(data)

    # 获取爬失败的数据
    @classmethod
    def get_all_fail_data(cls):
        if app.STORAGE_DRIVER == 1 :
            print('文件驱动暂不支持此操作')
        elif app.STORAGE_DRIVER == 2 :
            return Db.instance().get_all_fail_data()
        elif app.STORAGE_DRIVER == 3 :
            print('文件驱动暂不支持此操作')

    # 修改爬失败的数据
    @classmethod
    def update_base_info(cls,data):
        if app.STORAGE_DRIVER == 1 :
            print('文件驱动暂不支持此操作')
        elif app.STORAGE_DRIVER == 2 :
            return Db.instance().update_base_info(data)
        elif app.STORAGE_DRIVER == 3 :
            print('文件驱动暂不支持此操作')
