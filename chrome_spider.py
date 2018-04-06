# -*- coding:utf8 -*-
import pychrome
import settings
from cmd import js_cmd

"""
该模块基于Google给出的chrome文档做了一层封装
"""


class ChromeSpider(object):
    def __init__(self, **conf):
        if conf["url"] is None or "":
            url = settings.CONF["url"]
        else:
            url = conf["url"]
        self.browser = pychrome.Browser(url=url)

    def create_new_tab(self, url=None, timeout=2):
        try:
            new_tab = self.browser.new_tab(url=url, timeout=timeout)
            return new_tab
        except Exception as e:
            print "create_new_tab error:", e

    def start_tab(self, tab):
        try:
            tab.start()
            tab.Network.enable()
            return tab
        except Exception as e:
            print "start_tab error:", e

    def stop_tab(self, tab):
        try:
            tab.stop()
        except Exception as e:
            print "stop_tab error:", e

    def close_tab(self, tab):
        try:
            if tab.id:
                self.browser.close_tab(tab_id=tab.id)
            else:
                self.exec_js_cmd(tab, js_cmd.CLOSE_TAB)
        except Exception as e:
            print "close_tab error:", e

    def exec_js_cmd(self, tab, expression):
        try:
            result = tab.Runtime.evaluate(expression=expression)
            return result
        except Exception as e:
            print "exec_js_cmd error:", e

    def download_html_auto(self, url, css_disable=False, delay=3, is_wait_loading_finished=False, wait_circle_time=0.5):
        """
        返回一个页面html,自动会打开和关闭tab
        :param url: 需要抓取的url链接
        :param delay:默认延迟3秒
        :param css_disable 禁用css，默认不禁止
        :param is_wait_loading_finished: 是否等待页面加载完成再获取数据,默认不允许
        :param wait_circle_time: 每次等待页面加载完成循环的时间
        :return: 返回html
        """
        try:
            tab = self.create_new_tab(url=url)
            if css_disable:
                self.disable_css(tab=tab)
            self.start_tab(tab=tab)
            # tab.wait(timeout=1)

            # 如果要的等待页面加载完成的话
            if is_wait_loading_finished:
                circle_times = delay / wait_circle_time + 1
                count = 0
                while not self.is_page_loading_finished(tab) and count is not circle_times:
                    # 0.5秒一次循环，
                    tab.wait(timeout=wait_circle_time)
                    count = count + 1
                if count == circle_times:
                    print "在规定的延迟%d秒条件下没有加载完页面，输出html..." % delay
                else:
                    print "页面加载完成..."

            html = self.exec_js_cmd(tab, js_cmd.DOWNLOAD_HTML)
            if html is not None:
                html = html["result"]["value"]
                # 得到结果关闭tab
                # self.close_tab(tab)
                self.exec_js_cmd(tab, js_cmd.CLOSE_TAB)
                return html
        except Exception as e:
            print "download_html error:", e
            return None

    def download_html(self, url=None, delay=1, tab=None, disable_css=False, close_tab=True):
        """
        单纯的返回一个页面的html(需要手动启动一个tab)
        :param tab: 页面对象,默认为空，自己会自动创建一个
        :param url: 传入的url
        :param delay: 下载延迟
        :param disable_css: 是否禁止CSS
        :param close_tab: 每次爬完是否关闭tab
        :return:
        """
        try:
            if tab is None:
                tab = self.create_new_tab(url=url)
                self.start_tab(tab)
            tab.wait(timeout=delay)
            html = self.exec_js_cmd(tab, js_cmd.DOWNLOAD_HTML)
            if disable_css:
                self.disable_css(tab=tab)
            if html is not None:
                html = html["result"]["value"]
                if close_tab:
                    self.close_tab(tab)
                return html
        except Exception as e:
            print "download_html error:", e
            self.close_tab(tab)
            return None

    def download_html_auto_scroll(self, tab, delay=1, auto_scroll=True, disable_css=False):
        """
        可以自动下滑的方式下载页面
        :param tab: 页面对象
        :param delay: 下载延迟
        :param auto_scroll: 是否自动下滑, 面对下滑刷新的情况
        :param disable_css: 禁止使用css, 默认不禁止
        :return: 返回的html是一个迭代器对象
        """
        try:
            tab.wait(timeout=delay)
            html = self.exec_js_cmd(tab, js_cmd.DOWNLOAD_HTML)
            if disable_css:
                self.disable_css(tab=tab)
            if html is not None:
                html = html["result"]["value"]
                yield html

            # 下滑判断结束，还没解决
            if auto_scroll:
                # 根据分页高度判断是否继续
                init_height = 0
                is_continue = True
                while is_continue:
                    current_height = self.get_tab_scroll_height(tab)
                    # 翻页会卡一下，有可能就结束了
                    tab.wait(0.5)
                    if current_height == init_height:
                        # 说明爬到了底部
                        print "================END==================="
                        is_continue = False
                    else:
                        is_continue = True
                    self.exec_js_cmd(tab, js_cmd.SCROLL_TO_BOTTOM)
                    html = self.exec_js_cmd(tab, js_cmd.DOWNLOAD_HTML)
                    html = html["result"]["value"]
                    yield html
        except Exception as e:
            print "download_html_auto error:", e
            yield None

    def fill_form_by_id(self, tab, sub_id=None, auto_sub=True, **kw):
        """
        根据表单属性id自动提交表单
        :param tab: 代表当前页面
        :param sub_id: 提交按钮的Id
        :param auto_sub: 是否自动提交，也就是是否自动点击
        :param kw: 里面是{"id_name": "value"}
        :return:
        """
        if kw:
            for k, v in kw.items():
                self.exec_js_cmd(tab, js_cmd.FILL_VALUE_IN_FORM % (k, v))
            if auto_sub:
                self.exec_js_cmd(tab, js_cmd.CLICK_BY_ID % sub_id)
        else:
            print "不存在表单数据..."

    def get_tab_scroll_height(self, tab):
        try:
            result = self.exec_js_cmd(tab=tab, expression=js_cmd.GET_CURRENT_HIGHT)
            if result:
                return result["result"]["value"]
            else:
                return None
        except Exception as e:
            print "get_tab_scroll_height error: ", e

    def click_by_id(self, tab, attr_id):
        """
        通过id节点去点击
        :param tab:
        :param attr_id: id名
        :return:
        """
        cmd = js_cmd.CLICK_BY_ID % attr_id
        result = self.exec_js_cmd(tab, cmd)
        return result

    def click_by_class(self, tab, attr_class, **kw):
        """
        通过class节点去点击,默认所有拥有该class的节点都点击一下
        :param tab:
        :param attr_class:
        :param kw: 点击的一些其他参数
        :return:
        """
        cmd = js_cmd.CLICK_ALL_BY_CLASS % attr_class
        result = self.exec_js_cmd(tab, cmd)
        return result

    def scroll_html(self, tab):
        """
        向下滑动
        :param tab: 页面
        :return:
        """
        try:
            result = self.exec_js_cmd(tab, js_cmd.SCROLL_TO_BOTTOM)
            return result
        except Exception as e:
            print "scroll_html error:", e

    def get_page_status(self, tab):
        """
        获取页面当前状态
        :param tab: 当前页面
        :return: 返回状态 加载完成，正在加载等等
        """
        try:
            result = self.exec_js_cmd(tab, js_cmd.GET_HTML_STATUS)
            return result["result"]["value"]
        except Exception as e:
            print "get_page_status error:", e
            return None

    def navigate_to(self, tab, url):
        """
        跳转到哪个url
        :param tab:
        :param url:
        :return:
        """
        try:
            tab.Page.navigate(url=url)
        except Exception as e:
            print "navigate_to error:", e

    def clear_browser_cache(self, tab):
        try:
            tab.Network.clearBrowserCache()
        except Exception as e:
            print "clear_browser_cache error:", e

    def is_page_loading_finished(self, tab):
        """
        页面是否加载完成了
        :param tab:
        :return: True,False,完成，未完成
        """
        try:
            if self.get_page_status(tab) == "complete":
                return True
        except Exception as e:
            print "is_page_loading_finished error:", e
            return False
        return None

    def disable_css(self, tab):
        """
        禁用Css
        :param tab:
        :return:
        """
        try:
            result = tab.CSS.disable()
            return result
        except Exception as e:
            print "disable_css error:", e

    def enable_css(self, tab):
        """
        启用Css
        :param tab:
        :return:
        """
        try:
            tab.CSS.enable()
        except Exception as e:
            print "enable_css error:", e

    def set_cookie(self, tab, name=None, value=None, url=None, domain=None):
        """
        设置cookie访问页面
        :param tab: 标签页
        :param name: cookie的name
        :param value: cookie的value
        :param url: 需要修改cookie的相关页面
        :param domain: 需要修改cookie的相关域名
        :return:
        """
        try:
            result= tab.Network.setCookie(name=name, value=value, url=url, domain=domain)
            return result
        except Exception as e:
            print "set_cookie error:", e
            return None

