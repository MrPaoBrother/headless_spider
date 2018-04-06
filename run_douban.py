# -*- coding:utf8 -*-


from chrome_spider import ChromeSpider
import settings
from datetime import datetime
import cmd.js_cmd as cmd


def write_to_file(path, data):
    with open(path, 'wb') as fs:
        fs.write(data.encode("utf8"))


# 有验证码的情况,表单填写
def run(url, save_path):
    chrome_spider = ChromeSpider(**settings.CONF)
    tab = chrome_spider.create_new_tab(url=url)
    chrome_spider.start_tab(tab)
    # 输入验证码:
    code = input("code:")
    # 填写表单
    msg = {
        # 自行填充
        "email": "****",
        "password": "*****",
        "captcha_field": code
    }
    chrome_spider.fill_form_by_id(tab, auto_sub=False, **msg)
    # 点击登录
    chrome_spider.click_by_class(tab=tab, attr_class="btn-submit")
    tab.wait(timeout=3)
    tab.Page.navigate(url="https://movie.douban.com/subject/26260853/comments?status=P", _timeout=5)
    count = 1
    while True:
        data = chrome_spider.download_html(tab=tab, delay=2, close_tab=False)
        count = count + 1
        if count % 10 == 0:
            print "当前爬取进度--%d页" % count
        if data:
            write_to_file(save_path % (datetime.now().strftime("%Y-%m-%d %H:%M:%S")), data)
        result = chrome_spider.exec_js_cmd(tab, cmd.GET_ATTR_BY_CLASS % ("next", "href"))
        if result["result"]["value"] is None or '' or len(result["result"]["value"]) < 2:
            print "爬到了底..."
            break
        # 点击下一页
        chrome_spider.click_by_class(tab=tab, attr_class="next")

if __name__ == "__main__":
    save_path = "./data/douban/%s.html"
    base_url = "https://accounts.douban.com/login"
    run(base_url, save_path)