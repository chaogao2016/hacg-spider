#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import regex as re
import requests
import config.constant as constant
import module.browser.Chrome as Chrome
from module.browser.Chrome import Chrome

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
        self.curAnimationPage = 1
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
        if self.animationPageSize != 0 and (self.curAnimationPage > self.animationPageSize):
            return False
        else:
            return True

    # 首页动作
    def home_action(self):
        if self.animationUrl.strip() == '' or self.gameUrl.strip() == '' or self.comicUrl.strip() == '':
            print("开始抓取首页链接")
            # 未抓取过首页数据
            home_content = Chrome.instance().get_home_full_document(constant.SITE_URL)
            regex = re.compile("(?<=top.*href=\").{4,}(?=/\")")
            result = regex.findall(home_content)

            for uri in result :
                if uri.find("game") != -1 :
                    self.gameUrl = constant.SITE_URL + "/" + uri
                elif uri.find("anime") != -1 :
                    self.animationUrl = constant.SITE_URL + "/" + uri
                elif uri.find("comic") != -1 :
                    self.comicUrl = constant.SITE_URL + "/" + uri

            print("抓取首页成功")
            print(self.animationUrl)
            print(self.gameUrl)
            print(self.comicUrl)
        else:
            print("首页已经抓取")
            print(self.animationUrl)
            print(self.gameUrl)
            print(self.comicUrl)

    # 动画页动作
    def animation_action(self):
        if self.animationPageSize != 0 and (self.curAnimationPage > self.animationPageSize):
            print('动画页数据抓取完毕')
            return 0
        else:
            if self.animationPageSize == 0:
                print("动画页第一次抓取，先初始化分页数据")
                first_animation_url = self.animationUrl + 'page/' + str(self.curAnimationPage)
                first_animation_page_content = Chrome.instance().get_animation_full_document(first_animation_url)
                # 抓取动画页最后一页id
                regex_last_page = re.compile("(?<=['\"]wp-pagenavi['\"][\s\S]*last.*page/)\d*(?=/?)")
                result_last_page = regex_last_page.findall(first_animation_page_content)
                print(result_last_page)
                result_last_page = [88]
                if len(result_last_page) < 1 or int(result_last_page[0]) <= 0 :
                    print("未抓到动画尾页，失败")
                    return -1
                else:
                    print('共有' + str(result_last_page) + '页动画')
                    self.animationPageSize = result_last_page[0]

            # 遍历分页，抓取动画数据
            for page_id in range(1,self.animationPageSize + 1) :
                print('开始第' + str(self.curAnimationPage) + '页动画页数据抓取')
                current_animation_url = self.animationUrl + 'page/' + str(self.curAnimationPage)
                animation_page_content = Chrome.instance().get_animation_full_document(current_animation_url)
                # 抓取当前页面子链接正则
                regex_sub_link = re.compile("(?<=article[\s\S]*entry-title.*=\").*(?=\" )")
                result_sub_link = regex_sub_link.findall(animation_page_content)

                print("===========")
                f = open(constant.RUNTIME_PATH + '/test.log', 'w')
                f.write(animation_page_content)
                f.close()
                print("============")
                for sub_link in result_sub_link :
                    print(sub_link)
                self.curAnimationPage += 1
                print('动画循环终止三秒')
                time.sleep(constant.SLEEP_DELAY)

    # 程序启动
    def run(self):

        while self.check_status() :
            self.home_action()

            self.animation_action()

            print('大循环终止三秒')
            time.sleep(constant.SLEEP_DELAY)

        Chrome.instance().close_browser()
        print("程序终止")
        exit()

