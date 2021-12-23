# coding: utf-8
# ===============================================================================
#    Creation Date : 2020/11/19
#
#    作者 : Alan
#
#    微信 : 13125104933
#
#    邮箱 : 1924885288@qq.com
#
# ===============================================================================
import re
import json
import requests
import time
import random
import jieba.analyse
from imageio import imread
from wordcloud import WordCloud

global_max_id = 0
cookie_dict = 'SUB=_2A25MwEY_DeRhGeFK41QQ-SvLwjqIHXVsS2p3rDV6PUJbkdANLRP8kW1NQsIMnnA2Ng8D045z81zVDQ6zuVLgAoxb; _T_WM=53525751003; MLOGIN=1; WEIBOCN_FROM=1110006030; XSRF-TOKEN=d33313'
cookie = {item.split('=')[0]: item.split('=')[1] for item in cookie_dict.split('; ')}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
}
remove_words = {"视频", "微博"}  # 自定义需要剔除的文字


def gen_img(texts, img_file):
    data = ' '.join(text for text in texts)
    image_coloring = imread(img_file)
    wc = WordCloud(
        scale = 4,
        width = 1920,
        height = 1280,
        background_color="white",
        prefer_horizontal=0.5,
        repeat=True,
        # mask=image_coloring,
        font_path=r'C:\Windows\Fonts\FZSTK.TTF',  # 方正舒体
        contour_width=2,
        contour_color='pink',
        collocation_threshold=100,
        stopwords=remove_words,  # 去除关键字
    )
    wc.generate(data)
    wc.to_file(img_file.split('.')[0] + '_微博.png')


def clean_text(text):
    """清除文本中的标签等信息"""
    dr = re.compile(r'(<)[^>]+>', re.S)
    dd = dr.sub('', text)
    dr = re.compile(r'#[^#]+#', re.S)
    dd = dr.sub('', dd)
    dr = re.compile(r'@[^ ]+ ', re.S)
    dd = dr.sub('', dd)
    return dd.strip()


def fetch_data(maxid):
    """抓取关键词某一页的数据"""
    resp = requests.get(
        f"https://m.weibo.cn/comments/hotflow?id=4711696049900390&mid=4711696049900390&max_id_type=0&max_id={maxid}",
        headers=headers, cookies=cookie).json()
    datas = resp['data']['data']
    print('--- 评论条数:', len(datas))

    mblogs = []  # 保存处理过的微博
    for mblog in datas:
        blog = {'mid': mblog['id'],  # 微博id
                'text': clean_text(mblog['text']),  # 文本
                'userid': str(mblog['user']['id']),  # 用户id
                'username': mblog['user']['screen_name'],  # 用户名
                'max_id': resp['data']['max_id'],  # 最大爬取
                }
        mblogs.append(blog)
    return mblogs


def remove_duplication(mblogs):
    """根据微博的id对微博进行去重"""
    mid_set = {mblogs[0]['mid']}
    new_blogs = []
    for blog in mblogs[1:]:
        if blog['mid'] not in mid_set:
            new_blogs.append(blog)
            mid_set.add(blog['mid'])
    return new_blogs


def fetch_pages(query_val, max_page):
    """抓取关键词多页的数据"""
    pageno = 1
    global global_max_id
    mblogs = []
    while global_max_id >= 0:
        try:
            time.sleep(random.randint(2, 5))  # 设置随机休眠时间防止反爬
            mblogs.extend(fetch_data(global_max_id))
            print(f"第{pageno}页内容爬取完毕-------------------------")
            global_max_id = mblogs[-1]['max_id']
            print("max_id值", global_max_id)
            pageno += 1
        except Exception as e:
            print(e)
            print("被反爬无法获取评论内容")
            break
        if pageno > max_page:
            print(f"已经爬取了{max_page}页数据，想要继续爬取请自己设置爬取数量")
            break

    print("去重前：", len(mblogs))
    mblogs = remove_duplication(mblogs)
    print("去重后：", len(mblogs))

    # 保存到 result.json 文件中
    fp = open('{}.json'.format(query_val), 'w', encoding='utf-8')
    json.dump(mblogs, fp, ensure_ascii=False, indent=4)
    print("已保存至{}.json".format(query_val))


def parse_cloudpic(keyword):
    mblogs = json.loads(open('{}.json'.format(keyword), 'r', encoding='utf-8').read())
    print('a1零食研究所总评论数：', len(mblogs))
    words = []
    for blog in mblogs:
        words.extend(jieba.analyse.extract_tags(blog['text']))
    print("总词数：", len(words))
    gen_img(words, '苹果形状云图_.png')

if __name__ == '__main__':
    keyword = 'a1零食研究所'
    fetch_pages(keyword, max_page=1000000)  # 此处自定义需要爬取的页数
    parse_cloudpic(keyword)
