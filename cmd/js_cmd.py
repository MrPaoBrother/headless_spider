# -*- coding:utf8 -*-

DOWNLOAD_HTML = 'document.documentElement.outerHTML'
GET_CURRENT_HIGHT = 'document.body.scrollHeight'
SCROLL_TO_BOTTOM = 'window.scrollTo(0,document.body.scrollHeight)'
CLICK_BY_ID = 'document.getElementById("%s").click()'
# 默认只要有class的节点全部点击
CLICK_ALL_BY_CLASS = '''
var nodes = document.getElementsByClassName("%s");
for (var i=0;i<nodes.length;i++){
    nodes[i].click();
}
'''
# 从class中得到属性
GET_ATTR_BY_CLASS = '''
var nodes = document.getElementsByClassName("%s");
for (var i=0;i<nodes.length;i++){
    nodes[i].getAttribute("%s");
}
'''
# 选择点击某个,自己传参数进来
CLICK_ONE_BY_CLASS = 'document.getElementsByClassName("target")%s.click()'

# 根据id填写表单中某个属性的值
FILL_VALUE_IN_FORM = 'document.getElementById("%s").setAttribute("value", "%s");'

# 页面加载状态
GET_HTML_STATUS = "document.readyState"

# 关闭窗口
CLOSE_TAB = "window.close()"

# 得到class为某个类别的东西
GET_BY_CLASS = 'document.getElementsByClassName("%s");'