#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import json
import hashlib
import os
import config.constant as constant
import module.browser.Chrome as Chrome
from module.browser.Chrome import Chrome
from module.regex.Regex import Regex
from module.storage.Storage import Storage

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
        # 更新时抓取总页数
        self.updatePageSize = 3

    # 单例模式
    @classmethod
    def instance(cls):
        if not hasattr(Spider,'_instance'):
            Spider._instance = Spider()
        return Spider._instance

    # 检查爬虫状态，若已到最后一页，返回true
    def animation_is_finally(self):
        if self.animationPageSize != 0 and (self.curAnimationPage > self.animationPageSize or self.curAnimationPage <= 0):
            return True
        else:
            return False

    # 首页动作
    def home_action(self):
        if self.animationUrl.strip() == '' or self.gameUrl.strip() == '' or self.comicUrl.strip() == '':
            print("开始抓取首页链接")
            # 未抓取过首页数据
            home_content = Chrome.instance().get_common_document(constant.SITE_URL)
            result = Regex.home(home_content)
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

    # 动画页详细
    def animation_detail(self,page,action):
        print('开始第' + str(page) + '页动画页数据抓取')
        current_animation_url = self.animationUrl + '/page/' + str(page)
        animation_page_content = Chrome.instance().get_common_document(current_animation_url)
        # 抓取当前页面子链接正则
        result_sub_link = Regex.animation_sub_link(animation_page_content)
        # 遍历当前分页链接，访问并抓取具体内容
        for sub_link in result_sub_link:
            print(sub_link)
            if sub_link.find('all/game') != -1:
                print('过滤掉游戏')
                continue
            animation_detail = Chrome.instance().get_common_document(sub_link)
            # 抓取页面标题
            result_title = Regex.animation_title(animation_detail)
            if result_title.find('预告') != -1:
                print('过滤掉预告')
                continue
            print('标题：' + str(result_title))
            # 抓取页面描述
            result_desc = Regex.animation_desc(animation_detail)
            print('描述：' + str(result_desc))
            # 抓取页面图片
            result_image = Regex.animation_image(animation_detail)
            print('图片：' + str(result_image))
            # 抓取磁链
            magnet_str = Regex.animation_magnet_str(animation_detail)
            # 熟肉
            cook_magnet = Regex.animation_cook_magnet(magnet_str)
            print('熟肉磁链：' + str(cook_magnet))
            # 生肉
            fresh_magnet = Regex.animation_fresh_magnet(magnet_str)
            print('生肉磁链：' + str(fresh_magnet))
            # 其他磁链
            other_magnet = Regex.animation_other_magnet(magnet_str)
            print('其他磁链：' + str(other_magnet))
            # 组装数据
            data_map = {
                "title": result_title,
                "`describe`": result_desc,
                "image": json.dumps(result_image),
                "cook_magnet": json.dumps(cook_magnet),
                "fresh_magnet": json.dumps(fresh_magnet),
                "other_magnet": json.dumps(other_magnet),
                "base_url": sub_link,
                "base_url_md5": hashlib.md5(sub_link.encode("utf-8")).hexdigest(),
                'title_md5': hashlib.md5(result_title.encode("utf-8")).hexdigest(),
                'describe_md5': hashlib.md5(result_desc.encode("utf-8")).hexdigest(),
            }
            if action == 'create' :
                Storage.instance().save_animation_base_info(data_map)
            elif action == 'update' :
                Storage.instance().update_animation_base_info(data_map)

    # 动画页动作
    def animation_action(self,action = 'create'):
        if self.animation_is_finally():
            print('动画页数据抓取完毕')
            return 0
        else:
            # 遍历分页，抓取动画数据
            if action == 'create':
                if self.animationPageSize == 0:
                    print("动画页第一次抓取")
                    print("清空数据表")
                    Storage.instance().clear_animation_base_info()
                    print("初始化分页数据")
                    first_animation_url = self.animationUrl + '/page/' + str(self.curAnimationPage)
                    first_animation_page_content = Chrome.instance().get_common_document(first_animation_url)
                    # 抓取动画页最后一页id
                    result_last_page = Regex.animation_page_size(first_animation_page_content)
                    print(result_last_page)
                    if len(result_last_page) < 1 or int(result_last_page[0]) <= 0:
                        print("未抓到动画尾页，失败")
                        return -1
                    else:
                        print('共有' + str(result_last_page) + '页动画')
                        self.animationPageSize = int(result_last_page[0])
                        self.curAnimationPage = self.animationPageSize

                for page_id in range(self.animationPageSize, 0,-1):
                    print("==================================================")
                    self.animation_detail(page_id,action)
                    print("==================================================")
                    self.curAnimationPage -= 1
                    time.sleep(1)
                    print('动画循环终止三秒')
                    time.sleep(constant.SLEEP_DELAY)
            elif action == 'update':
                start_index = self.curAnimationPage
                for page_id in range(start_index, self.animationPageSize + 1):
                    print("==================================================")
                    self.animation_detail(page_id,action)
                    print("==================================================")
                    self.curAnimationPage += 1
                    time.sleep(1)
                    print('动画循环终止三秒')
                    time.sleep(constant.SLEEP_DELAY)

    # 程序启动
    def run(self):

        while not self.animation_is_finally() :
            self.home_action()

            self.animation_action()

            print('大循环终止三秒')
            time.sleep(constant.SLEEP_DELAY)

        Chrome.instance().close_browser()
        print("程序终止")
        exit()

    # 修复操作
    def fix(self):
        fail_data_list = Storage.instance().get_animation_all_fail_data()

        for fail_data_item in fail_data_list :
            sub_link = fail_data_item['base_url']
            print(sub_link)

            animation_detail = Chrome.instance().get_common_document(sub_link)

            # 抓取磁链
            magnet_str = Regex.animation_magnet_str(animation_detail)
            # 熟肉
            cook_magnet = Regex.animation_cook_magnet(magnet_str)
            print('熟肉磁链：' + str(cook_magnet))
            # 生肉
            fresh_magnet = Regex.animation_fresh_magnet(magnet_str)
            print('生肉磁链：' + str(fresh_magnet))
            # 其他磁链
            other_magnet = Regex.animation_other_magnet(magnet_str)
            print('其他磁链：' + str(other_magnet))
            # 组装数据
            data_map = {
                "id" : fail_data_item['id'],
                "cook_magnet": [] if len(cook_magnet) >= 1 else json.dumps(cook_magnet),
                "fresh_magnet": [] if len(fresh_magnet) >= 1 else json.dumps(fresh_magnet),
                "other_magnet": [] if len(other_magnet) >= 1 else json.dumps(other_magnet),
            }

            # 存储数据
            Storage.instance().fix_animation_base_info(data_map)

        print(fail_data_list)
        print('修复操作完成')

    # 停止操作
    def stop(self):
        os.system("ps -ef|grep start.py|grep -v grep|awk '{print $2}'|xargs kill -9 ")

    # 更新操作
    def update(self):
        # 爬取前几页数据，对比每一条url的md5，如果数据库中不存在，则将其插入数据库
        # 如果已经存在，对比其他的md5，只要有变化，就重新抓取数据
        self.animationPageSize = self.updatePageSize
        while not self.animation_is_finally() :
            self.home_action()

            self.animation_action('update')

            print('大循环终止三秒')
            time.sleep(constant.SLEEP_DELAY)

        Chrome.instance().close_browser()
        print("程序终止")
        exit()





