#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import logging
from module.Spider import Spider

try:
    if len(sys.argv) > 1 :
        # 动作
        if 'start' in sys.argv:
            # 执行抓取动作
            Spider.instance().run()
        elif 'stop' in sys.argv:
            # 执行爬虫停止操作
            Spider.instance().stop()
        elif 'fix' in sys.argv:
            # 执行爬虫修复操作
            Spider.instance().fix()
        elif 'update' in sys.argv :
            # 执行爬虫更新操作
            Spider.instance().update()
        elif 'download' in sys.argv :
            # 从队列拉取数据并下载
            Spider.instance().download()
        elif 'test' in sys.argv:
            #测试模式
            pass
        else:
            print('您输入的命令不合法')
    else :
        print("请附加命令")
        print("start:启动脚本")
        print("stop:停止脚本")
        print("fix:修复脚本")
except Exception as e:
    logging.exception(e)
