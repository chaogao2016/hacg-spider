#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'gaochao'

import json
import os
import config.app as app
from module.storage.File import File
from module.storage.Db import Db
from module.rabbitmq.RabbitMq import RabbitMq

class Storage(object):

    # 获取实例
    @classmethod
    def instance(cls):
        if not hasattr(Storage, "_instance"):
            cls._instance = Storage()

        return cls._instance

    # 构造方法
    def __init__(self):
        if app.STORAGE_DRIVER == 1 :
            self.storage_instance = File.instance()
        elif app.STORAGE_DRIVER == 2 :
            self.storage_instance = Db.instance()
        else:
            print("请选择正确的存储驱动")

    # 存储爬虫基本数据
    def save_animation_base_info(self,data):
        return self.storage_instance.save_animation_base_info(data)

    # 获取爬失败的数据
    def get_animation_all_fail_data(self):
        self.storage_instance.get_animation_all_fail_data()

    # 修改爬失败的数据
    def fix_animation_base_info(self,data):
        return self.storage_instance.instance().fix_animation_base_info(data)

    # 清空失败的数据
    def clear_animation_base_info(self):
        return self.storage_instance.instance().clear_animation_base_info()

    # 全投递
    @classmethod
    def all_delivery(cls,record_id,image,cook_magnet,fresh_magnet,other_magnet):
        # 遍历磁链，投递到下载队列中
        param = {
            "id": record_id,
            "image": image
        }
        if cook_magnet:
            param['magnet'] = cook_magnet
        elif fresh_magnet:
            param['magnet'] = fresh_magnet
        elif other_magnet:
            param['magnet'] = other_magnet
        else:
            print("id为%d的记录抓不到磁链" % record_id)

        if "magnet" in param:
            RabbitMq.instance().push_magnet_task(param)

    # 部分投递
    @classmethod
    def section_delivery(cls,store_dir,record_id,image,cook_magnet,fresh_magnet,other_magnet):
        magnet_list = []
        file_path = store_dir + "/magnet.txt"
        if os.path.exists(file_path) :
            with open(file_path) as f_handle:
                line = f_handle.readline()
                while line:
                    temp_list = line.split(',')
                    if temp_list[0]:
                        magnet_list.append(temp_list[0])
                    line = f_handle.readline()

        if cook_magnet:
            delivery_list = cook_magnet
        elif fresh_magnet:
            delivery_list = fresh_magnet
        elif other_magnet:
            delivery_list = other_magnet
        else:
            delivery_list = []

        inset_list = []
        for item in delivery_list :
            if item not in magnet_list :
                inset_list.append(item)

        if inset_list :
            RabbitMq.instance().push_magnet_task({
                "id": record_id,
                "image": image,
                "magnet" : inset_list
            })
        else:
            print("id为%d的记录没有需要新下载的磁链" % record_id)

    # 更新最新的数据
    def update_animation_base_info(self, data):
        cook_magnet = json.loads(data['cook_magnet'])
        fresh_magnet = json.loads(data['fresh_magnet'])
        other_magnet = json.loads(data['other_magnet'])
        image = json.loads(data['image'])

        # 先根据base_url的散列值查出记录
        record = self.storage_instance.get_animation_by_base_url(data['base_url_md5'])
        if record :
            if record['store_dir'] :
                if data['title_md5'] != record['title_md5'] or data['describe_md5'] != record['describe_md5'] or data[
                    'score'] != record['score']:
                    print('有更新')
                    data['id'] = record['id']
                    self.fix_animation_base_info(data)
                    Storage.section_delivery(record['store_dir'],record['id'], image, cook_magnet, fresh_magnet, other_magnet)
                else:
                    print('无更新')
            else:
                Storage.all_delivery(record['id'], image, cook_magnet, fresh_magnet, other_magnet)

        else:
            print('新插入')
            record_id = self.save_animation_base_info(data)
            Storage.all_delivery(record_id,image,cook_magnet,fresh_magnet,other_magnet)

    # 下载数据
    def down_from_queue(self):
        RabbitMq.instance().pop_magnet_task()

