import requests
import chardet
import traceback
import json
import re
import pymysql

# to do : 解决当查询值为空时，跳过该词或者其他得方式

con = pymysql.connect(host='101.32.182.177',
                      port=3306,
                      user='liumeng',
                      passwd='lm@3199803',
                      db='workdb',
                      charset='utf8')
cursor = con.cursor()


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
        response = requests.post(url, data=_data, timeout=10)
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
            if news_dict['next_item'] != 0:
                serp_list = []
                for item in news_dict['items']:
                    serp = {}
                    serp['title'] = get_format_html(item['title'])
                    serp['desc'] = get_format_html(item['content'])
                    serp_list.append(serp)
                return serp_list
            else:
                return None
        except:
            print("读取失败")
            traceback.print_exc()
            return None


def parse_article_data(article_json):
    if article_json:
        try:
            news_dict = json.loads(article_json)
            if news_dict['recordCount'] != 0:
                serp_list = []
                for item in news_dict['items']:
                    serp = {}
                    serp['title'] = get_format_html(item['title'])
                    serp['author'] = get_format_html(item['author'])
                    serp['pubulish_year'] = get_format_html(item['year'])
                    serp_list.append(serp)
                return serp_list
            else:
                return None
        except:
            print("读取失败")
            traceback.print_exc()
            return None


def insert_db(sql):
    try:
        cursor.execute(sql)
        con.commit()
        return True

    except:
        traceback.print_exc()
        con.rollback()
        return False


def combain_info(kw):
    '''获取新闻得信息'''
    base_news_url = f"https://www.zte.com.cn/china/search?keyword={kw}&d=ws&searchword={kw}&pageIndex=1&startIndex=0&cateId=1_5_1"
    kw_news_json = request_json(base_news_url)
    kw_news_list = parse_news_data(kw_news_json)
    for item in kw_news_list:
        news_title = item['title']
        news_desc = item['desc']
        news_sql = f"insert into word_news(word,news_title,news_des)values('{kw}','{news_title}','{news_desc}')"
        insert_db(news_sql)
        print(f"{kw}<<<<<<<{news_title}")
    
    '''获取简讯信息'''
    base_tech_url = "https://www.zte.com.cn/china/about/magazine/zte-technologies/articles/?d=ws"
    kw_tech_json = post_json(base_tech_url, kw)
    kw_tech_list = parse_article_data(kw_tech_json)
    for item in kw_tech_list:
        tech_title = item['title']
        tech_author = item['author']
        tech_year = item['pubulish_year']
        tech_sql = f"insert into word_tech(word,tech_title,tech_author,tech_publishyear) values('{kw}','{tech_title}','{tech_author}','{tech_year}')"
        insert_db(tech_sql)
        print(f"{kw}<<<<<<<{tech_title}")



    '''获取非简讯信息'''
    base_comm_url = "https://www.zte.com.cn/china/about/magazine/zte-communications/articles/?d=ws"
    kw_comm_json = post_json(base_comm_url, kw)
    kw_comm_list = parse_article_data(kw_comm_json)
    for item in kw_comm_list:
        comm_title = item['title']
        comm_author = item['author']
        comm_year = item['pubulish_year']
        comm_sql = f"insert into word_comm(word,comm_title,comm_author,comm_publishyear) values('{kw}','{comm_title}','{comm_author}','{comm_year}')"
        insert_db(comm_sql)
        print(f"{kw}<<<<<<<{comm_title}")

    print("导入完毕")

def get_kw():
    with open("kws.txt", "r", encoding="utf8") as f:
        for line in f.readlines():
            line = line.strip("\n")
            sql = f"insert into words(word) values('{line}') "
            insert_db(sql)
            print("插入中")


if __name__ == "__main__":
    with open("kws.txt", "r", encoding="utf8") as f:
        for line in f.readlines():
            kw = line.strip("\n")
            combain_info(kw)