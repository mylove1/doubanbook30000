# -*- coding:utf-8 -*-
from tool.gethtml import getHtml
import bookdeal
# 抓取分类标签页
tag =getHtml('http://book.douban.com/tag/')
file = open('web/booktag.html','wb')
file.write(tag.encode())
file.close()

# 抓取列表页方便测试
tag1 = getHtml("http://www.douban.com/tag/%E5%B0%8F%E8%AF%B4/book")
file1 = open('web/books.html','wb')
file1.write(tag1.encode())
file1.close()

# 抓取图书页方便测试
tag3 = getHtml("http://book.douban.com/subject/25862578/?from=tag_all")
file2 = open('web/book.html','wb')
file2.write(tag3.encode())
file2.close()
print("成功")
