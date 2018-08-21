#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import config.constant as constant

__author__ = 'gaochao'

class Spider(object):

    def __init__(self):
        # 动画页url
        self.animationUrl = ''
        # 当前爬到的动画页数
        self.curAnimationPage = 0
        # 动画总页数
        self.animationPageSize = 0


    # 单例模式
    @classmethod
    def instance(cls):
        if not hasattr(Spider,'_instance'):
            Spider._instance = Spider()
        return Spider._instance

    # 检查爬虫状态，若已到最后一页，返回false
    def check_status(self):
        if self.curAnimationPage > self.animationPageSize:
            return False
        else:
            return True

    # 首页动作
    def homeAction(self):
    
        pass

    # 动画页动作
    def animationAction(self):
        pass

    # 程序启动
    def run(self):
        while self.check_status() :
            print('hello')
            time.sleep(constant.SLEEP_DELAY)

        exit()

