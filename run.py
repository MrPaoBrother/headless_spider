# -*- coding:utf8 -*-

import sys
from chrome_spider import ChromeSpider
import settings
from datetime import datetime


def write_to_file(path, data):
    with open(path, 'wb') as fs:
        fs.write(data.encode("utf8"))


def get_cmd_result():
    if len(sys.argv) < 2:
        return None
    if sys.argv[1] == '--url':
        return sys.argv[2]
    return None


def run(url, save_path, delay=4):
    try:
        chrome_spider = ChromeSpider(**settings.CONF)
        # tab = chrome_spider.create_new_tab(url)
        # chrome_spider.start_tab(tab)

        html = chrome_spider.download_html(url=url, delay=delay, close_tab=False)
        write_to_file(save_path % (datetime.now().strftime("%Y-%m-%d %H:%M:%S")), html)
        print "download success..."
    except Exception as e:
        print "run error:", e

if __name__ == '__main__':
    url = get_cmd_result()
    if url:
        save_path = "./data/other/%s.html"
        run(url=url, save_path=save_path)
    else:
        print "url 格式错误...使用--url your url"