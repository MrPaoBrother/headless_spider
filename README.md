# Chrome Headless 爬虫终结者

* 简介: 自从Google开发了无形态浏览器后，爬虫已经基本0门槛，90%的网站都能通过模拟浏览器的方式进行抓取，
简单快捷的方式进行抓取。

## 安装

```
$ pip install pychrome
```

## 启动chrome headless

* Mac下在~/.bashrc下进行如下配置:
```
alias chrome="/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome"
alias chrome-canary="/Applications/Google\ Chrome\ Canary.app/Contents/MacOS/Google\ Chrome\ Canary"
alias chromium="/Applications/Chromium.app/Contents/MacOS/Chromium"
alias start_chrome_server="chrome --disable-gpu --remote-debugging-port=9222"
```

* 保存配置
```
$ source ~/.bashrc
```

* 关闭chrome浏览器(完全关闭),之后运行命令:
```
$ start_chrome_server
```

## 实战

**Ps.** 下面的所有结果都会保存在./data目录中，自行查找
### 任意网站测试

```
$ python run.py --url http://www.baidu.com
```

### 知乎自动下拉

```
$ python run_zhihu.py
```

### 法治在线自动翻页

```
$ python run_fazhizaixian.py

```

### 豆瓣模拟登陆

```
$ python run_douban.py

```

**Ps.** 豆瓣里面需要登录才能抓全，所以读者自行在源码中加入自己的账号密码...

## 其他功能介绍
* 模拟点击
* 表单自动填写
* 自动跳转
* ...

**Ps.** 只要浏览器能够完成的功能，程序都能完成...

## 总结

* 该项目适用于mac和ubuntu开发，win配置较为麻烦，自行找相关教程

* **基本的功能笔者都已经封装好，觉得好用麻烦给个star!**


## 参考文档

[1] [pychrome 源码](https://github.com/fate0/pychrome)

[2] [chrome headless 安装教程](https://www.jianshu.com/p/aec4b1216011)

[3] [Google Chrome 开发者协议文档](https://chromedevtools.github.io/devtools-protocol/)


