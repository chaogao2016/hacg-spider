#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import config.app as app
import config.constant as constant

__author__ = 'gaochao'

class Spider(object):

    def __init__(self):
        print(112121)

    # 单例模式
    @classmethod
    def instance(cls):
        if not hasattr(Spider,'_instance'):
            Spider._instance = Spider()
        return Spider._instance

    def check_status(self):
        print("hello world \n")
        return False

    # 程序启动
    def run(self):
        sum = 0
        n = 99
        while n > 0 :
            self.check_status()
            sum += n
            n -= 2
        print(sum)