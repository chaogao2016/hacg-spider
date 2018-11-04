#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'gaochao'
import sys
import requests
import json
import config.secret as secret

if len(sys.argv) <= 3:
    print("只处理参数大于3的回调")
gid = sys.argv[1]
print("----------------")
print(sys.argv)

params = json.dumps({
    "jsonrpc":"2.0",
    "id":"qwer",
    "method":"aria2.tellStatus",
    "params":[
        "token:" + str(secret.ARIA2_KEY),
        gid
    ]
})
download_detail = json.loads(requests.post("http://localhost:6800/jsonrpc",data=params).text)
download_detail = download_detail['result']
print(download_detail)
print('infoHash' in download_detail)
if 'infoHash' in download_detail:
    # 磁力下载
    # 将magnet.txt中的状态修改为已完成标记为已完成
    store_dir = download_detail['dir']
    target_magnet = download_detail['infoHash']
    magnet_file_path = store_dir + "/magnet.txt"
    with open(magnet_file_path,"r+") as f_handle:
        line = f_handle.readline()
        print(line)
        magnet_list = []
        while line:
            split_list = line.split(",")
            print(split_list)
            print(split_list[0].lower() == target_magnet.lower())
            if split_list[0].lower() == target_magnet.lower() :
                magnet_list.append([target_magnet,1])

            line = f_handle.readline()
        print(magnet_list)
        f_handle.seek(0)
        f_handle.truncate()
        for magnet_item in magnet_list:
            print(str(magnet_item[0]) + "," + str(magnet_item[1]))
            f_handle.writelines(str(magnet_item[0]) + "," + str(magnet_item[1]))
else:
    # 普通下载
    pass

# 删除已完成任务
del_params = json.dumps({
    "jsonrpc":"2.0",
    "id":"qwer",
    "method":"aria2.removeDownloadResult",
    "params":
        [
            "token:" + str(secret.ARIA2_KEY),
            gid
        ]
})

result = requests.post("http://localhost:6800/jsonrpc",data=del_params)
print(result.text)
