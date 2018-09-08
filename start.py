#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from module.Spider import Spider

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
    elif 'test' in sys.argv:
        #测试模式
        pass
    else:
        print('您输入的命令不合法')

else :
    print("\n请附加命令")
    print("start:启动脚本")
    print("stop:停止脚本")
    print("fix:修复脚本")
