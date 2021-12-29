import requests
import json
from pyquery import PyQuery as pq
import pandas as pd
import time
import random
import dateutil.parser as parser
from lxml import etree

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62',
    'Referer': 'http://120.25.213.166/user/login.do'
}
cookie_dict = 'JSESSIONID=C2FE54F85C52939004EE593FFB19258B'
cookie = {item.split('=')[0]: item.split('=')[1] for item in cookie_dict.split('; ')}
datalist = []


def get_sendurl(page, timeout):
    session = requests.session()
    sendurl = f'http://120.25.213.166/user/home.do'
    response = session.get(sendurl, headers=headers, cookies=cookie)
    for id in range(889, 890):
        sendurl_user = f'http://120.25.213.166/user/detail.do?id={id}'
        user_dict = {}
        try:
            response = session.get(sendurl_user, headers=headers, cookies=cookie)
            response_user = response.text
            print("发送请求：", sendurl_user, response.status_code)
            # time.sleep(timeout)
            content = etree.HTML(response_user)
            user_dict["编号"] = id
            user_dict["用户名"] = content.xpath('//table//tr[2]/td[2]/text()')
            user_dict["账户余额"] = content.xpath('//table//tr[2]/td[4]/text()')
            user_dict["邮箱"] = content.xpath('//table//tr[3]/td[2]/text()')
            user_dict["真实姓名"] = content.xpath('//table//tr[3]/td[4]/text()')
            user_dict["LastName"] = content.xpath('//table//tr[4]/td[2]/text()')
            user_dict["注册时间"] = content.xpath('//table//tr[4]/td[4]/text()')
            user_dict["联系地址"] = content.xpath('/table//tr[5]/td[2]/text()')
            user_dict["电话号码"] = str(content.xpath('//table//tr[6]/td[2]/text()')).replace(u"\\xa0", "")
            user_dict["QQ"] = content.xpath('//table//tr[6]/td[4]/text()')
            user_dict["MSN"] = content.xpath('//table//tr[7]/td[2]/text()')
            user_dict["淘宝旺旺"] = content.xpath('/table//tr[7]/td[4]/text()')
            user_dict["推荐人"] = content.xpath('/table//tr[8]/td[2]/text()')
            user_dict["获取推荐奖励"] = content.xpath('//table//tr[8]/td[4]/text()')
            user_dict["身份证号"] = content.xpath('//table//tr[9]/td/p/text()')
            datalist.append(user_dict)
        except:
            print(f"第{id}次数据没有获取到")
    pd.DataFrame(datalist).to_csv("KK爬虫.csv", index=False, encoding="utf_8_sig")


if __name__ == '__main__':
    print("------------------------------开始爬取数据：----------------------------------")
    page = 40000
    timeout = 1
    get_sendurl(page, timeout)
