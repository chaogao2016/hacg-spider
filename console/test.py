import sys
import requests

# 定义常量
hacgUrl = "http://www.hacg.love/wp/category/all/anime/"

# 从页面中解析出单条item信息
def getItemInfo(htmlStr):
    pass

# 将item数据存入到数据库或文件中
def saveItem():
    pass

# 遍历所有分页，提取中其中的item
pageIndex = 1

while True:
    pageUrl = hacgUrl + ("page/%d/" % (pageIndex))

    r = requests.get(pageUrl,timeout=20)

    item = getItemInfo(r.content)

    print(pageIndex)

    pageIndex = pageIndex + 1

