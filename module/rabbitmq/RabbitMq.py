#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'gaochao'
import pika
import json

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
            print(body)

            ch.basic_ack(delivery_tag = method.delivery_tag)

        # self._channel.basic_qos(prefetch_count=1)

        self._channel.basic_consume(
            callback,
            queue='magnet_download'
        )

    def __del__(self):
        self._connection.close()
