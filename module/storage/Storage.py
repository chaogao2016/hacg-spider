#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'gaochao'

import config.app as app
from module.storage.File import File
from module.storage.Db import Db

class Storage(object):

    # 获取实例
    @classmethod
    def instance(cls):
        if not hasattr(Storage, "_instance"):
            cls._instance = Storage()

        return cls._instance

    # 构造方法
    def __init__(self):
        if app.STORAGE_DRIVER == 1 :
            self.storage_instance = File.instance()
        elif app.STORAGE_DRIVER == 2 :
            self.storage_instance = Db.instance()
        else:
            print("请选择正确的存储驱动")

    # 存储爬虫基本数据
    def save_animation_base_info(self,data):
        self.storage_instance.save_animation_base_info(data)

    # 获取爬失败的数据
    def get_animation_all_fail_data(self):
        self.storage_instance.get_animation_all_fail_data()

    # 修改爬失败的数据
    def fix_animation_base_info(self,data):
        return self.instance().fix_animation_base_info(data)

    # 清空失败的数据
    def clear_animation_base_info(self):
        return self.instance().clear_animation_base_info()

    # 更新最新的数据
    def update_animation_base_info(self, data):
        # 先根据base_url的散列值查出记录
        record = self.storage_instance.get_animation_by_base_url(data['base_url_md5'])
        if record :
            print(record['title'])