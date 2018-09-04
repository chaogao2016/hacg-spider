#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'gaochao'

import time
from selenium import webdriver
from pyvirtualdisplay import Display
import requests
class Chrome(object):

    # 构造方法
    def __init__(self):
        pass
        # # 无gui显示
        # self.display = Display(visible=0, size=(800, 800))
        # self.display.start()
        #
        # # 初始化浏览器参数
        # options = webdriver.ChromeOptions()
        # options.add_argument("--headless")
        # options.add_argument("disable-gpu")
        # options.add_argument('--no-sandbox')
        # chrome_driver_binary = "/usr/local/bin/chromedriver"
        # self.driver = webdriver.Chrome(chrome_driver_binary, chrome_options=options)

    # 单例模式
    @classmethod
    def instance(cls):
        if not hasattr(Chrome,'_instance'):
            Chrome._instance = Chrome()
        return Chrome._instance

    # 根据url获取全部文档
    def get_common_document(self,url):
        result = requests.get(url)
        time.sleep(1)
        return result.text

        # self.driver.get(url)
        # time.sleep(1)
        # full_document = self.driver.find_element_by_xpath('//*').get_attribute("outerHTML")
        # self.close_browser()
        # return full_document

    # 关闭浏览器
    def close_browser(self):
        pass
        # self.driver.close()