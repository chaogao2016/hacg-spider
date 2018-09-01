#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from module.Spider import Spider

if len(sys.argv) > 1 :
    # 执行其他动作
    if '-fix' in sys.argv:
        # 执行爬虫修复操作
        Spider.instance().fix()
else :
    # 执行抓取动作
    Spider.instance().run()