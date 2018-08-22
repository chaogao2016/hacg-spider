#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import re
import requests
import config.constant as constant

__author__ = 'gaochao'

class Spider(object):

    def __init__(self):
        # 动画页url
        self.animationUrl = ''
        # 游戏页url
        self.gameUrl = ''
        # 文章页url
        self.comicUrl = ''
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
    def home_action(self):
        if self.animationUrl.strip() == '' or self.gameUrl.strip() == '' or self.comicUrl.strip() == '':
            print("开始抓取首页链接")
            # 未抓到，继续
            home_content = requests.get(constant.SITE_URL)
            regex = re.compile("(?<=top.{6}href=\").{4,}(?=\")")
            result = regex.findall(home_content.text)

            for uri in result :
                if uri.find("game") != -1 :
                    self.gameUrl = constant.SITE_URL + "/" + uri
                elif uri.find("anime") != -1 :
                    self.animationUrl = constant.SITE_URL + "/" + uri
                elif uri.find("comic") != -1 :
                    self.comicUrl = constant.SITE_URL + "/" + uri

            print("抓取成功")
            print(self.animationUrl)
            print(self.gameUrl)
            print(self.comicUrl)
        else:
            print("已经抓取")
            print(self.animationUrl)
            print(self.gameUrl)
            print(self.comicUrl)

    # 动画页动作
    def animation_action(self):
        pass

    # 程序启动
    def run(self):
        while self.check_status() :
            self.home_action()

            self.animation_action()

            time.sleep(constant.SLEEP_DELAY)

        print("程序终止")
        exit()

