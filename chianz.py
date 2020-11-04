import lxml.html as lh

import downLoader
import time


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
        time.sleep(500)
    return kw_total_list


def get_domian():
    domain_list = []
    with open("domain.txt", 'w') as f:
        domain_list.append(f.readline())
    return domain_list


if __name__ == "__main__":
    base_url = "http://rank.chinaz.com/"
    compete_domain = get_domian()
    for domain in compete_domain:
        domain_url = base_url + f"{domain}/"
        orgine_html = downLoader.downLoader(domain_url, debug=True)
        pages = getPages(orgine_html)
        domain_kw_list = get_keyword(pages)
