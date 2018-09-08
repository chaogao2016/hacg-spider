#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'gaochao'

import regex as re

class Regex(object):

    # 构造方法
    def __init__(self):
        pass

    # 获得实例
    @classmethod
    def instance(cls):
        if not hasattr(Regex,"_instance") :
            Regex._instance = Regex()

        return Regex._instance

    # 首页匹配
    @classmethod
    def home(cls,content):
        regex = re.compile("(?<=top.*href=\").{4,}(?=/\")")
        result = regex.findall(content)
        return result

    # 动画页最大页数匹配
    @classmethod
    def animation_page_size(cls,content):
        regex_last_page = re.compile("(?<=['\"]wp-pagenavi['\"][\s\S]*last.*page/)\d*(?=/?)")
        result_last_page = regex_last_page.findall(content)
        return result_last_page

    # 动画页抓取子页面链接
    @classmethod
    def animation_sub_link(cls,content):
        regex_sub_link = re.compile("(?<=article[\s\S]*entry-title.*=\").*(?=\".*rel)")
        result_sub_link = regex_sub_link.findall(content)
        return result_sub_link

    # 动画页提取标题
    @classmethod
    def animation_title(cls,content):
        regex_title = re.compile("(?<=h1.*entry-title.*>).*(?=</h1>)")
        result = regex_title.findall(content)
        if len(result) < 1:
            return ''
        else:
            return result[0]

    # 动画页提取描述
    @classmethod
    def animation_desc(cls, content):
        regex_desc = re.compile("(?<=>)[^>]*(?=<span.*more-)")
        result = regex_desc.findall(content)
        if len(result) < 1:
            return ''
        else:
            return result[0]

    # 动画页提取图片
    @classmethod
    def animation_image(cls, content):
        regex_image = re.compile("(?<=wp-image.*src=\")[^\"]*(?=\")")
        result = regex_image.findall(content)
        return result

    # 动画页提取包含磁链的文本
    @classmethod
    def animation_magnet_str(cls, content):
        # 提取一部分包含磁链的字符串
        regex_pre_magnet = re.compile("<!-- MetaSlider -->[\s\S]*<!-- MetaSlider -->")
        result_pre = regex_pre_magnet.findall(content)
        if len(result_pre) < 1 :
            return ''
        else:
            return result_pre[0]

    # 动画页提取熟磁链
    @classmethod
    def animation_cook_magnet(cls,content):
        # 从预先提取的字符串中取得磁链
        regex_magnet = re.compile("(?<=熟)[\da-zA-Z]{30,}")
        result = regex_magnet.findall(content)
        return cls.magnet_filter(result)

    # 动画页提取生磁链
    @classmethod
    def animation_fresh_magnet(cls, content):
        # 从预先提取的字符串中取得磁链
        regex_magnet = re.compile("(?<=生)[\da-zA-Z]{30,}")
        result = regex_magnet.findall(content)
        return cls.magnet_filter(result)

    # 动画页提取其他磁链
    @classmethod
    def animation_other_magnet(cls, content):
        # 从预先提取的字符串中取得磁链
        regex_magnet = re.compile("(?<=[>\n@\s、:：\u2E80-\u9FFF])[\da-zA-Z]{30,}|(?<=[>\n\s])[\da-zA-Z]{15,}[\s\S]{0,40}[\da-zA-Z]{15,}")
        result = regex_magnet.findall(content)
        return cls.magnet_filter(result)

    # 过滤掉磁链中的中文字符和其他字符
    @classmethod
    def magnet_filter(cls,magnet_list):
        if len(magnet_list) < 1:
            return magnet_list
        else:
            result = []
            for magnet in magnet_list :
                regex_filter = re.compile("[\da-zA-Z]{10,}")
                temp_list = regex_filter.findall(magnet)
                magnet_str = ""
                for temp_str in temp_list:
                    magnet_str += temp_str
                result.append(magnet_str)
            return result

