#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'gaochao'

from selenium import webdriver
from pyvirtualdisplay import Display
from selenium.webdriver.support import expected_conditions as Ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

class Chrome(object):

    # 构造方法
    def __init__(self):
        # 无gui显示
        self.display = Display(visible=0, size=(800, 800))
        self.display.start()

        # 初始化浏览器参数
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("disable-gpu")
        options.add_argument('--no-sandbox')
        chrome_driver_binary = "/usr/local/bin/chromedriver"
        self.driver = webdriver.Chrome(chrome_driver_binary, chrome_options=options)

    # 单例模式
    @classmethod
    def instance(cls):
        if not hasattr(Chrome,'_instance'):
            Chrome._instance = Chrome()
        return Chrome._instance

    # 根据url获取首页全部文档
    def get_home_full_document(self,url):
        self.driver.get(url)
        full_document = self.driver.find_element_by_xpath('//*').get_attribute("outerHTML")
        return full_document

    # 根据url获取动画页全部文档
    def get_animation_full_document(self,url):
        self.driver.get(url)
        print(url)
        import time
        time.sleep(2)
        full_document = self.driver.find_element_by_xpath('//*').get_attribute("outerHTML")
        return full_document

    # 关闭浏览器
    def close_browser(self):
        self.driver.close()