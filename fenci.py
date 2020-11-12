import requests
import chardet
import traceback
import json
import re


def get_format_html(html):
    new_html = re.sub(r'<(?!p|img|/p)[^<>]*?>', '', html).strip()
    return new_html


def request_json(url, headers=None, timeout=10):
    _headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Content-Type": "application/json; charset=utf-8",
        "Referer": "https://www.zte.com.cn/china/search"
    }
    if headers:
        _headers = headers

    try:
        response = requests.get(url, headers=_headers, timeout=timeout)
        encoding = chardet.detect(response.content)['encoding']
        res_text = response.content.decode(encoding)
        return res_text
    except:
        print("请求失败，错误如下")
        traceback.print_exc()
        return None


def post_json(url, kw):
    _data = {"type": "title", "keyword": f"{kw}", "page": 1, "size": 10}

    try:
        response = requests.post(url, data=_data)
        encoding = chardet.detect(response.content)['encoding']
        res_text = response.content.decode(encoding)
        return res_text
    except:
        print("请求失败，错误如下")
        traceback.print_exc()
        return None


def parse_news_data(news_json):
    if news_json:
        try:
            news_dict = json.loads(news_json)
            serp_list = []
            for item in news_dict['items']:
                serp = {}
                serp['title'] = get_format_html(item['title'])
                serp['descrip'] = get_format_html(item['content'])
                serp_list.append(serp)
            print(serp_list)
        except:
            print("读取失败")
            traceback.print_exc()


def parse_article_data(article_json):
    if article_json:
        try:
            news_dict = json.loads(article_json)
            serp_list = []
            for item in news_dict['items']:
                serp = {}
                serp['title'] = get_format_html(item['title'])
                serp['author'] = get_format_html(item['author'])
                serp['pubulish_year'] = get_format_html(item['year'])
                serp_list.append(serp)
            print(serp_list)
        except:
            print("读取失败")
            traceback.print_exc()


if __name__ == "__main__":
    # url = "https://www.zte.com.cn/china/search?keyword=5G%E6%A0%B8%E5%BF%83%E7%BD%91&d=ws&searchword=5G%E6%A0%B8%E5%BF%83%E7%BD%91&pageIndex=1&startIndex=0&cateId=1_5_1&sortby=&_=1605164234203"
    # news_json = request_json(url)
    # parse_news_data(news_json)

    url_ = "https://www.zte.com.cn/china/about/magazine/zte-technologies/articles/?d=ws"
    kw = "5G核心网"
    article_json = post_json(url_, kw)
    parse_article_data(article_json)
