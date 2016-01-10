# -*- coding:utf-8 -*-
import urllib.request
import urllib.parse
import urllib.request, urllib.parse, http.cookiejar
from bs4 import BeautifulSoup
__author__ = 'hunterhug'


def getHtml(url):
    """
    伪装头部并得到网页内容

    """
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    useragent3 = 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0'
    Accept='text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    cookie = """Cbid="FccuPZmq//0"; viewed="25923455_25867785_1520363_6397086_6431094_5338398_25862578_26589018_1002898_5922149"; gr_user_id=9fee2430-40d3-4f9d-a5aa-d3e295531497; __utma=30149280.372796509.1449028995.1450149245.1450165592.16; __utmz=30149280.1450149245.15.12.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utma=81379588.1458595321.1449028995.1450149245.1450165592.11; __utmz=81379588.1450149245.10.10.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; _pk_id.100001.3ac3=ff3d4ecea493334f.1449028995.11.1450166087.1450149661.; ll="118281"; _pk_ref.100001.3ac3=%5B%22%22%2C%22%22%2C1450165591%2C%22http%3A%2F%2Fwww.douban.com%2F%22%5D; ap=1; ct=y; ps=y; __utmv=30149280.13418; ue="569929309@qq.com"; push_noty_num=0; push_doumail_num=0; __utmc=30149280; __utmc=81379588; gr_session_id=8951b2b8-06a3-4a07-b066-0ee33d2be006; _pk_ses.100001.3ac3=*; __utmb=30149280.2.10.1450165592; __utmt_douban=1; __utmb=81379588.2.10.1450165592; __utmt=1"""
    opener.addheaders = [('User-Agent',useragent3),
                         ('Accept',Accept),
                         ('Cookie', cookie)]

    urllib.request.install_opener(opener)

    html_bytes = urllib.request.urlopen(url).read()
    html_string = html_bytes.decode('utf-8','ignore')
    return html_string


def getBinaryHtml(url,daili='42.96.162.252:3128'):
    """
    伪装头部并得到网页原始内容

    """
    cj = http.cookiejar.CookieJar()
    # 设置IP代理
    # http://www.youdaili.net/
    # http://www.youdaili.net/Daili/http/3917.html
    proxy_support = urllib.request.ProxyHandler({'http':'http://'+daili})
     # 开启代理支持
    opener = urllib.request.build_opener(proxy_support, urllib.request.HTTPCookieProcessor(cj), urllib.request.HTTPHandler)

    #opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    # 用户代理http://blog.csdn.net/lvjin110/article/details/12944397
    useragent = 'Mozilla/5.0 (iPhone; U; CPU like Mac OS X; en) AppleWebKit/420+ (KHTML, like Gecko) Version/3.0 Mobile/1C28 Safari/419.3'
    useragent1 ='Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36'
    useragent2 ='Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)'
    useragent3 = 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0'
    Accept='text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    opener.addheaders = [('User-Agent',useragent3),
                         ('Accept',Accept),
                         ('Cookie', '4564564564564564565646540')]

    urllib.request.install_opener(opener)

    html_bytes = urllib.request.urlopen(url).read()
    return html_bytes

def getSoup(html_content,parse='html.parser'):
    """
    得到网页解析后的对象，方便分拆数据

    """
    return BeautifulSoup(html_content,parse)

def test():
    getBinaryHtml('http://www.douban.com/tag/%E5%B0%8F%E8%AF%B4/book?start=195')

if __name__=='__main__':
    tag =getBinaryHtml('http://book.douban.com/tag/')
    file = open('../web/booktag.html','wb')
    file.write(tag)
    file.close()
    # content1 = getHtml("http://www.douban.com/tag/%E5%B0%8F%E8%AF%B4/book")
    # file1 = open('../web/books.html','wb')
    # content2 = getHtml("http://book.douban.com/subject/25862578/?from=tag_all")
    # file2 = open('../web/book.html','wb')
    # file1.write(content.encode('utf-8'))
    # file2.write(content.encode('utf-8'))
    # file1.close()
    # file2.close()
    # test()
