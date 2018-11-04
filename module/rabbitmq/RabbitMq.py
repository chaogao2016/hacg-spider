#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'gaochao'
import os
import pika
import json
import config.filesystem as filesystem
from module.storage.Db import Db
from module.aria2.Aria2 import Aria2

class RabbitMq(object):

    def __init__(self):
        self._connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
        self._channel = self._connection.channel()
        self._channel.queue_declare(queue = 'magnet_download',durable = True)

    # 获得实例
    @classmethod
    def instance(cls):
        if not hasattr(RabbitMq, "_instance"):
            RabbitMq._instance = RabbitMq()

        return RabbitMq._instance

    # 投递下载任务
    def push_magnet_task(self,message_body):
        if type(message_body) != dict or "magnet" not in message_body or "id" not in message_body :
            raise TypeError('投递任务格式不合法！')
        else:
            message = json.dumps(message_body)
            self._channel.basic_publish(
                exchange='',
                routing_key='magnet_download',
                body=message,
                properties=pika.BasicProperties(
                    delivery_mode=2,
                )
            )
            print("投递成功")

    # 消费下载任务
    def pop_magnet_task(self):
        def callback(ch,method,properties,body):
            print('接到任务')
            message = json.loads(body)
            magnet_file_dir = filesystem.ANIMATION_STORAGE_PATH + str(message['id']) + "/"
            magnet_file_path = magnet_file_dir + "/magnet.txt"

            if not os.path.exists(magnet_file_path):
                if not os.path.exists(magnet_file_dir):
                    os.mkdir(magnet_file_dir)

                os.system("touch " + magnet_file_path)
                Db.instance().update_store_dir(message['id'],magnet_file_dir)

                # 下载图片
                image_list = message['image']
                for image_url in image_list:
                    print(image_url)
                    Aria2.instance().download(image_url,magnet_file_dir)

            # 将本次需要下载的任务写进magnet.txt，标记为未完成
            magnet_list = message['magnet']
            with open(magnet_file_path,"a") as f_handle:
                for magnet in magnet_list:
                    f_handle.writelines(magnet + ",0")
                    # 将任务投递给aria2c
                    Aria2.instance().download("magnet:?xt=urn:btih:" + magnet + "&dn=aria2", magnet_file_dir)

            ch.basic_ack(delivery_tag = method.delivery_tag)

        # self._channel.basic_qos(prefetch_count=1)

        self._channel.basic_consume(
            callback,
            queue='magnet_download'
        )
        self._channel.start_consuming()

    def __del__(self):
        self._connection.close()
