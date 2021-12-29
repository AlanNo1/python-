import json
import csv
import time
from appium import webdriver as app_driver
from selenium.webdriver.common.by import By
import os
import pandas as pd
import random

# 爬取APP数据时候，请记得打开Fiddler和设置好手机代理,
# 在控制台运行：   mitmdump -s 抖音爬虫.py -p 8888
data_list = []

# 读取txt文本
def read_json_text(path):
    with open(path, mode='r', encoding="utf-8", errors='ignore') as f:
        item_data = json.loads(f.read())
        print(item_data)
        dic = {}
        item = item_data['data'][0]
        dic["用户ID"] = item["aweme_info"]['author']['uid']
        dic["用户昵称"] = item["aweme_info"]['author']['nickname']
        dic["性别"] = item["aweme_info"]['author']['gender']
        dic["用户签名"] = item["aweme_info"]['author']['signature']
        dic["抖音URL"] = item['aweme_info']['share_info']['share_url']
        dic["内容"] = item["aweme_info"]['desc']
        dic["点赞人数"] = item['aweme_info']['statistics']['digg_count']
        dic["评论人数"] = item['aweme_info']['statistics']['comment_count']
        dic["分享人数"] = item['aweme_info']['statistics']['share_count']
        dic["发布时间"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(item["aweme_info"]['create_time']))
        print(dic)

def parser_home(parser_home):
    home_data = json.loads(parser_home)
    for item in home_data["data"]:
        print("类型是:", type(item))
        dic = {}
        try:
            dic["用户ID"] = item["aweme_info"]['author']['uid']
            dic["用户昵称"] = item["aweme_info"]['author']['nickname']
            dic["性别"] = item["aweme_info"]['author']['gender']
            dic["用户签名"] = item["aweme_info"]['author']['signature']
            dic["抖音URL"] = item['aweme_info']['share_info']['share_url']
            dic["内容"] = item["aweme_info"]['desc']
            dic["点赞人数"] = item['aweme_info']['statistics']['digg_count']
            dic["评论人数"] = item['aweme_info']['statistics']['comment_count']
            dic["分享人数"] = item['aweme_info']['statistics']['share_count']
            dic["发布时间"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(item["aweme_info"]['create_time']))
            data_list.append(dic)
        except:
            print("忽略当前的值")
    return data_list

def save_data(data, path):
    write = pd.ExcelWriter(path)
    df = pd.DataFrame(data)
    df.to_csv(f"{path}", index=False, mode='a',encoding="utf_8_sig")
    # 必须运行write.save()，不然不能输出到本地
    write.save()
    print(f"数据抓取完毕，保存在{path}中")

def response(flow):
    try:
        os.system("adb shell input swipe 710 1100 710 500 240")
        if "https://aweme.snssdk.com/aweme/v1/general/search/single/?" in flow.request.url:
            print(flow.response.text)
            with open('json_file.txt', mode='a', encoding="utf-8") as f:
                f.write(flow.response.text)
            # 解析数据
            data = parser_home(flow.response.text)
            # 保存数据
            save_data(data=data, path='抖音爬虫.csv')
    except:
        print("---" * 100, "错误", "--" * 100)
        pass
    finally:
        for i in range(4):
            time.sleep(random.randint(5, 7))
            os.system("adb shell input swipe 710 1100 710 500 240")
