#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'gaochao'
from module.rabbitmq.RabbitMq import RabbitMq
# 投递一条图片下载任务
# RabbitMq.instance().push_magnet_task({
#                 "id": 25,
#                 "image": ["http://llss.lol/wp/wp-content/uploads/2016/11/c933496sample12.jpg"],
#                 "magnet" : []
#             })

# 投递一条磁链下载任务
RabbitMq.instance().push_magnet_task({
                "id": 26,
                "image": ["http://llss.lol/wp/wp-content/uploads/2016/11/c933496sample12.jpg"],
                "magnet" : ["5D9AFCE48D38F70270D21D4843ADFB3DB0C56156"]
            })