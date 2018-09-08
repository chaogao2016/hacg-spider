#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'gaochao'

class File(object):

    # 构造方法
    def __init__(self):
        pass

    # 获取实例
    @classmethod
    def instance(cls):
        if not hasattr(File,"_instance"):
            cls._instance = File()

        return cls._instance

    # 存储爬虫基本数据
    def save_animation_base_info(self,data):
        pass