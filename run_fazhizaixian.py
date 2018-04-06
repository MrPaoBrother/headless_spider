# -*- coding:utf8 -*-

from chrome_spider import ChromeSpider
import settings
from datetime import datetime
from cmd import js_cmd
import re


def write_to_file(path, data):
    with open(path, 'wb') as fs:
        fs.write(data.encode("utf8"))


def get_page(html):
    html = html.replace("&amp;", '')
    pat = '<div class="page">(.*?)</div>'
    result = re.compile(pat, re.S).findall(html)
    if len(result) > 0:
        pat = 'page=(.*?)">'
        result = re.compile(pat, re.S).findall(result[0])
    else:
        return -1
    if len(result) < 1:
        return -1
    return int(result[-1])

def run():
    # chrome_spider = ChromeSpider(**settings.CONF)
    # tab = chrome_spider.create_new_tab(url=url)
    # chrome_spider.start_tab(tab)
    """
    测试代码
    """
    url_list = []
    base = "http://www.jindu626.com/e/action/ListInfo/?classid=%s&page=%s"
    base_url = "http://www.jindu626.com/e/action/ListInfo/?classid=%s&page=1"
    for i in range(3, 60):
        url = base_url % str(i)
        url_list.append(url)
    count = 3
    for url in url_list:
        chrome_spider = ChromeSpider(**settings.CONF)
        tab = chrome_spider.create_new_tab(url=url)
        chrome_spider.start_tab(tab)
        is_hub = chrome_spider.exec_js_cmd(tab, expression=js_cmd.GET_BY_CLASS % "page")
        if "result" in is_hub:
            result = is_hub["result"]
            if result:
                html = chrome_spider.download_html(url=url, delay=8, tab=tab, close_tab=True)
                pages = get_page(html)
                if pages is not -1:
                    print "%s 是种子页，抓取中..." % url
                    for j in range(1, pages + 1):
                        crawl_url = base % (str(count), str(j))
                        print "正在爬%s的第%d页" % (crawl_url, j)
                        data = chrome_spider.download_html(url=crawl_url, delay=3, close_tab=True)
                        write_to_file('./data/fazhizaixian/%s.html' % datetime.now().strftime("%Y-%m-%d %H:%M:%S"), data)
        count = count + 1
if __name__ == "__main__":
    run()


