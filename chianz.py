import lxml.html as lh

import downLoader
import time
import pymysql

con = pymysql.connect(host='101.32.182.177',
                      port=3306,
                      user='liumeng',
                      passwd='lm@3199803',
                      db='workdb',
                      charset='utf8')
cursor = con.cursor()


def getPages(html):
    html_str = lh.document_fromstring(html)
    '找到翻页节点'
    fanYe_node = html_str.xpath(
        "//div[contains(@class,'_chinaz-rank-pag')]/a/text()")
    if fanYe_node[-1] == "...500":
        last_page = 50
    else:
        last_page = fanYe_node[-1]

    return last_page


def get_keyword(pages):
    url = "http://rank.chinaz.com/www.elecfans.com-0---0-"
    kw_total_list = []
    for i in range(1, pages):
        status, html, redirect = downLoader.downLoader(url + f"{i}",
                                                       debug=True)
        kw_list = lh.document_fromstring(html).xpath(
            "//a[contains(@class,'ellipsis') and contains(@class,'block')]/text()"
        )
        kw_total_list.extend(kw_list)
        time.sleep(1)
    return kw_total_list


def get_domian():
    domain_list = []
    with open("E:\\python_学习代码\\script\\domain.txt", mode="r") as f:
        result = f.readline()
        domain_list.append(result)
    return domain_list


if __name__ == "__main__":
    base_url = "http://rank.chinaz.com/"
    compete_domain = get_domian()
    for domain in compete_domain:
        domain_url = base_url + f"{domain}/"
        status, orgine_html, red = downLoader.downLoader(domain_url,
                                                         debug=True)
        pages = getPages(orgine_html)
        domain_kw_list = get_keyword(pages)
        sql = "insert into competerkw(domain, keyword) values( f'{domain}',f'{kw}');"
        for kw in domain_kw_list:
            cursor.execute(sql)
            print(f"{domain} :{kw}")
