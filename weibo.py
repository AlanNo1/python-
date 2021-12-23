"""使用PyExecJs实现对微信公众号的解密登录
安装此模块需提取安装nodejs
pip install PyExecJs"""
import execjs
import requests
import json
from pyquery import PyQuery as pq
import pandas as pd

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
}
comment_list=[]
comment_second_list=[]


def ger_sendurl():
    sendurl = 'https://m.weibo.cn/api/container/getIndex?containerid=231522type%3D1%26t%3D10%26q%3D%23%E6%9D%A8%E6%B4%8B%E7%9A%84a1%E5%A5%B6%E6%92%95%E5%87%BA%E5%9C%88%E4%BA%86%23&extparam=%23%E6%9D%A8%E6%B4%8B%E7%9A%84a1%E5%A5%B6%E6%92%95%E5%87%BA%E5%9C%88%E4%BA%86%23&page_type=searchall&page=40'
    response = requests.get(sendurl,headers=headers).json()
    for card in response['data']['cards']:
        for card_group in card['card_group']:
            comment_dict = {}
            comment_dict['ID'] = card_group['mblog']['id']
            comment_dict['用户名'] = card_group['mblog']['user']['screen_name']
            comment_dict['帖子标题'] = pq(card_group['mblog']['text']).text()
            comment_dict['评论数'] = card_group['mblog']['comments_count']
            comment_dict['mid'] = card_group['mblog']['mid']
            print("---------------------------------------------------------------------")
            comment_list.append(comment_dict)

def ger_senddentailurl():
    for urlid in comment_list:
        senddentailurl = f"https://m.weibo.cn/comments/hotflow?id={urlid['ID']}&mid={urlid['mid']}&max_id_type=0"
        if int(urlid['评论数']) > 0:
            print("评论的URL地址是：",senddentailurl)
            response = requests.get(senddentailurl,headers=headers).json()
            try:
                second_comment = response['data']['data']
            except:
                print("当前楼层没有评论")
            else:
                for second_comment_detail in second_comment:
                    second_dict = {}
                    second_dict[f"ID"] = urlid['ID']
                    second_dict[f"评论的用户名"] = second_comment_detail['user']['screen_name']
                    second_dict[f"评论的内容"] = pq(second_comment_detail['text']).text()
                    comment_second_list.append(second_dict)
        else:
            print("当前评论数为0：暂不抓取！")

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
    df_all = pd.merge(data_list[0],data_list[1],on ="ID").to_excel(write, sheet_name="数据汇总表", index=False)
    for da, sh_name in zip(data_list, sheet_name_list):
        da.to_excel(write, sheet_name=sh_name, index=False)
    # 必须运行write.save()，不然不能输出到本地
    write.save()
    print(f"数据抓取完毕，保存在{data_path}中")

if __name__ == '__main__':
    print("------------------------------开始爬取数据：----------------------------------")
    ger_sendurl()
    ger_senddentailurl()
    data_path = 'comment_dict.xlsx'
    data_list =[pd.DataFrame(comment_list),pd.DataFrame(comment_second_list)]
    sheet_name_list = ["帖子表","评论表"]
    DF2Excel(data_path, data_list, sheet_name_list)
