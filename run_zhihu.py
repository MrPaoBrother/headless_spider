# -*- coding:utf8 -*-

from chrome_spider import ChromeSpider
import settings
from datetime import datetime

"""
author:power
"""


def write_to_file(path, data):
    with open(path, 'wb') as fs:
        fs.write(data.encode("utf8"))


def run(url):
    chrome_spider = ChromeSpider(**settings.CONF)
    tab = chrome_spider.create_new_tab(url=url)
    chrome_spider.start_tab(tab)
    count = 1
    init_height = 0
    while True:
        chrome_spider.get_page_status(tab)
        count = count + 1
        if count % 10 == 0:
            print "当前爬取进度--%d页" % count
        if count % 10 == 0:
            data = chrome_spider.download_html(tab=tab, delay=1, disable_css=True, close_tab=False)
            write_to_file("./data/zhihu/%s.html" % (datetime.now().strftime("%Y-%m-%d %H:%M:%S")), data)
        chrome_spider.scroll_html(tab)
        tab.wait(1)

if __name__ == "__main__":
    zhihu_url = "https://www.zhihu.com/"
    run(zhihu_url)


