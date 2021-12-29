import requests
import json
from pyquery import PyQuery as pq
import pandas as pd
import time
import random
import dateutil.parser as parser

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62',
}
cookie_dict = '_T_WM=61622863837; MLOGIN=0; XSRF-TOKEN=02ec06; WEIBOCN_FROM=1110006030; M_WEIBOCN_PARAMS=luicode=10000011&lfid=1076035675889356&fid=1076035675889356&uicode=10000011'
cookie = {item.split('=')[0]: item.split('=')[1] for item in cookie_dict.split('; ')}

weilai_list = []
xiaopeng_list = []
lixiang_lsit = []


def get_sendurl(uid, containerid, page, data_list):
    for i in range(1, page + 1):
        sendurl = f'https://m.weibo.cn/api/container/getIndex?uid={uid}&&luicode=10000011&lfid=…ue={uid}&containerid={containerid}&page={i}'
        print(f"正在爬取第{i}页,url是:{sendurl}")
        time.sleep(1)
        # time.sleep(random.randint(4, 6))
        try:
            response = requests.get(sendurl, headers=headers, cookies=cookie).json()
        except:
            print(f"该数据在第{i}页被反爬，等待10分钟")
            time.sleep(6000)
            break
        for card in response['data']['cards']:
            data_dict = {}
            try:
                data_dict['发布时间'] = parser.parse(card['mblog']['created_at']).isoformat()
                data_dict['文本内容'] = pq(card['mblog']['text']).text()
                data_dict['转发数量'] = card['mblog']['reposts_count']
                data_dict['评论数量'] = card['mblog']['comments_count']
                data_dict['点赞数量'] = card['mblog']['attitudes_count']
                # if "2021" not in data_dict['发布时间']:
                #     print("数据已经被爬完，请退出!")
                #     return data_list
                data_list.append(data_dict)
            except:
                print("数据已经被爬完，请退出!")
                fp = open(f'{uid}.json', 'w', encoding='utf-8')
                json.dump(data_list, fp, ensure_ascii=False, indent=4)
                return data_list
    fp = open(f'{uid}.json', 'w', encoding='utf-8')
    json.dump(data_list, fp, ensure_ascii=False, indent=4)
    return data_list


def DF2Excel(data_path, data_list, sheet_name_list):
    '''将多个dataframe 保存到同一个excel 的不同sheet 上
    参数：
    data_path：str
        需要保存的文件地址及文件名
    data_list：list
        需要保存到excel的dataframe
    sheet_name_list：list
        sheet name 每个sheet 的名称
    '''
    write = pd.ExcelWriter(data_path)
    # df_all = pd.merge(data_list[0],data_list[1],on ="ID").to_excel(write, sheet_name="数据汇总表", index=False)
    for da, sh_name in zip(data_list, sheet_name_list):
        da.to_excel(write, sheet_name=sh_name, index=False)
        da.to_csv(f"{sh_name}.csv", index=False, encoding="utf_8_sig")
    # 必须运行write.save()，不然不能输出到本地
    write.save()
    print(f"数据抓取完毕，保存在{data_path}中")


if __name__ == '__main__':
    print("------------------------------开始爬取数据：----------------------------------")
    page = 20000
    weilai_list = get_sendurl(uid=5675889356, containerid=1076035675889356, page=page, data_list=weilai_list)  # 蔚来
    xiaopeng_list = get_sendurl(uid=5710264970, containerid=1076035710264970, page=page, data_list=xiaopeng_list)  # 小鹏
    lixiang_lsit = get_sendurl(uid=6001272153, containerid=1076036001272153, page=page, data_list=lixiang_lsit)  # 理想
    data_path = 'weibo_car.xlsx'
    data_list = [pd.DataFrame(weilai_list), pd.DataFrame(xiaopeng_list), pd.DataFrame(lixiang_lsit)]
    sheet_name_list = ["蔚来", "小鹏", '理想']
    DF2Excel(data_path, data_list, sheet_name_list)
