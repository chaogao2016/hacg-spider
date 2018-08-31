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
        regex_sub_link = re.compile("(?<=article[\s\S]*entry-title.*=\").*(?=\" )")
        result_sub_link = regex_sub_link.findall(content)
        return result_sub_link

    # 动画页提取标题
    @classmethod
    def animation_title(cls,content):
        regex_title = re.compile("(?<=h1.*entry-title.*>).*(?=</h1>)")
        result = regex_title.findall(content)
        return result

    # 动画页提取描述
    @classmethod
    def animation_desc(cls, content):
        regex_desc = re.compile("(?<=>)[^>]*(?=<span.*more-)")
        result = regex_desc.findall(content)
        return result

    # 动画页提取图片
    @classmethod
    def animation_image(cls, content):
        regex_image = re.compile("(?<=wp-image.*src=\")[^\"]*(?=\")")
        result = regex_image.findall(content)
        return result

    # 动画页提取磁链
    @classmethod
    def animation_magnet(cls, content):
        # 先提取一部分包含磁链的字符串
        regex_pre_magnet = re.compile("<!-- MetaSlider -->[\s\S]*<!-- MetaSlider -->")
        result_pre = regex_pre_magnet.findall(content)
        if len(result_pre) < 1 :
            return []
        else:
            pre_str = result_pre[0]

            # 从预先提取的字符串中取得磁链
            regex_magnet = re.compile("[\da-zA-Z]{30,}")
            result = regex_magnet.findall(pre_str)

            return result
