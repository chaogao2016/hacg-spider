#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'gaochao'
import requests
import json

import config.secret as secret

class Aria2 (object):
    # 获取实例
    @classmethod
    def instance(cls):
        if not hasattr(Aria2, "_instance"):
            cls._instance = Aria2()

        return cls._instance

    # 构造方法
    def __init__(self):
        pass

    # 下载
    @classmethod
    def download(cls,url,target_dir):
        params = json.dumps({
            "jsonrpc":"2.0",
            "id":"qwer",
            "method":"aria2.addUri",
            "params":[
                "token:" + str(secret.ARIA2_KEY),
                [url],
                {
                    "dir":target_dir
                }
            ]
        })
        print(params)
        result = requests.post("http://localhost:6800/jsonrpc", data=params)
        print(result.text)

