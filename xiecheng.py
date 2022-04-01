import requests
import json
import csv

postUrl = "https://m.ctrip.com/restapi/soa2/13444/json/getCommentCollapseList"

# 将景点poiId和名称添加到此处
urls = [
    ['76865', '星海广场'],
    ['75628', '棒棰岛'],
    ['75633', '大连森林动物园'],
    ['60514877', '三寰牧场'],
    ['75635', '劳动公园'],
    ['23035466', '东港音乐喷泉广场'],
    ['79494', '海之韵广场'],
    ['87618', '金石滩度假区'],
    ['87748', '滨海路'],
    ['87647', '滨海国家地质公园'],
    ['24845945', '莲花山观景台'],
    ['92196', '白玉山景区'],
    ['13301914', '大连天门山国家森林公园'],
]

for id in urls:
    print("正在爬取景点：", id[1])
    # 通过返回值判断总评论数，每页9条，计算出总页数，对大于2000条的数据只爬取两千条
    data_pre = {
        "arg": {
            "channelType": 2,
            "collapseType": 0,
            "commentTagId": 0,
            "pageIndex": 1,
            "pageSize": 10,
            "poiId": id[0],
            "sourceType": 1,
            "sortType": 3,
            "starType": 0
        },
        "head": {
            "cid": "09031069112760102754",
            "ctok": "",
            "cver": "1.0",
            "lang": "01",
            "sid": "8888",
            "syscode": "09",
            "auth": "",
            "xsid": "",
            "extension": []
        }
    }

    html = requests.post(postUrl, data=json.dumps(data_pre)).text
    html = json.loads(html)

    # 确定总页数总页数
    total_page = int(html['result']['totalCount'] / 10)
    if total_page > 300:
        total_page = 300
    # 遍历查询评论
    print("总页数:", total_page, "爬取中")

    # 创建写入csv文件
    path = './dalian/' + str(id[1]) + '.csv'
    xuhao = 0
    with open(path, 'w', newline='', encoding='utf-8') as f:
        file = csv.writer(f)
        file.writerow(['序号', '景区ID', '景区名称', '评论'])
        for page in range(1, int(total_page) + 1):
            data = {
                "arg": {
                    "channelType": 2,
                    "collapseType": 0,
                    "commentTagId": 0,
                    "pageIndex": page,
                    "pageSize": 10,
                    "poiId": id[0],
                    "sourceType": 1,
                    "sortType": 3,
                    "starType": 0
                },
                "head": {
                    "cid": "09031069112760102754",
                    "ctok": "",
                    "cver": "1.0",
                    "lang": "01",
                    "sid": "8888",
                    "syscode": "09",
                    "auth": "",
                    "xsid": "",
                    "extension": []
                }
            }
            html = requests.post(postUrl, data=json.dumps(data)).text
            html = json.loads(html)
            # 获取评论
            for j in range(10):
                result = html['result']['items'][j]['content']
                file.writerow([xuhao, id[0], id[1], result])
                print([xuhao, id[0], id[1], result])
                xuhao += 1
    print(id[1], "爬取完成")
