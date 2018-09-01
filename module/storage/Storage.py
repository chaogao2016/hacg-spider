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
