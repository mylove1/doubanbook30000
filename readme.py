# http://kw.gdufe.edu.cn:8080/index.html
# -*- coding:utf-8 -*-
import urllib.request
import urllib.parse
import urllib.request, urllib.parse, http.cookiejar
__author__ = 'hunterhug'


def getHtml(url, daili,postdata = {}):
    """
    抓取网页：支持cookie
    第一个参数为网址，第二个为POST的数据

    """
    # COOKIE文件保存路径
    filename = 'cookie.txt'

    # 声明一个MozillaCookieJar对象实例保存在文件中
    cj = http.cookiejar.MozillaCookieJar(filename)

    proxy_support = urllib.request.ProxyHandler({'http':'http://'+daili})

    # 从文件中读取cookie内容到变量
    # ignore_discard的意思是即使cookies将被丢弃也将它保存下来
    # ignore_expires的意思是如果在该文件中 cookies已经存在，则覆盖原文件写
    cj.load(filename, ignore_discard=True, ignore_expires=True)

    # 建造带有COOKIE处理器的打开专家
    # opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    opener = urllib.request.build_opener(proxy_support, urllib.request.HTTPCookieProcessor(cj), urllib.request.HTTPHandler)
    # 打开专家加头部
    opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:42.0) Gecko/20100101 Firefox/42.0'),
                         ('Referer','http://acm.gdufe.edu.cn/Feedback'),
						 ('Host','acm.gdufe.edu.cn')]

    # 分配专家
    urllib.request.install_opener(opener)

    # 有数据需要POST
    if postdata:

        # 数据URL编码
        postdata = urllib.parse.urlencode(postdata)

        # 抓取网页
        html_bytes = urllib.request.urlopen(url,postdata.encode()).read()
    else:
        html_bytes = urllib.request.urlopen(url).read()

    # 保存COOKIE到文件中
    cj.save(ignore_discard=True, ignore_expires=True)
    return html_bytes

if __name__=='__main__':
    daili='101.4.60.46:80'
    url='http://acm.gdufe.edu.cn/index.php/Feedback/insert'
    a="55"
    a=urllib.parse.quote(a)
    url=url+'?title='+a+'&content='+a
    print(url)
    while(True):
        print('1')
        print(getHtml(url,daili).decode('utf-8','ignore'))

