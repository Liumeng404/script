import requests
import traceback
import chardet


def downLoader(url, timeout=10, debug=False, headers=None, binary=False):
    _headers = {
        "UserAgent":
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36 Edg/86.0.622.58",
        "Host": "rank.chinaz.com",
        "Referer": "http://tool.chinaz.com/"
    }

    redirected_url = url

    if headers:
        _headers = headers

    try:
        response = requests.get(url, headers=_headers, timeout=timeout)
        if binary:
            html = response.content
        else:
            encoding = chardet.detect(response.content)['encoding']
            html = response.content.decode(encoding=encoding)
        status = response.status_code
        redirected_url = response.url
    except:
        if debug:
            traceback.print_exc()
        msg = f"下载失败：{url}"
        print(msg)

        if binary:
            html = b''
        else:
            html = ''

        status = 0

    return status, html, redirected_url
