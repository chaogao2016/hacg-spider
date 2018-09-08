#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'gaochao'

import time
import requests
class Chrome(object):

    # 构造方法
    def __init__(self):
        pass

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

    # 关闭浏览器
    def close_browser(self):
        pass