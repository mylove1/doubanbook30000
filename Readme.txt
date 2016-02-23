爬虫程序运行请参考PDF
抓取豆瓣的大部分图书。
A project for catch the book of 豆瓣website in china.
please see the code source

using python3.4

本爬虫程序目录如下：
----book  抓取的图书详情页
  　----文学　　　 大分类
  　　　----1000121昆虫记.html 标号+标题
    ----文化
    ----生活
    ----流行
    ----经管
----books 提取的图书列表页
  　----文学　　　 大分类
  　　　----茨威格.xlsx  标签
    ----文化
    ----生活
    ----流行
    ----经管
----data  提取的数据库文件
    ----doubanbook.book.sql  图书基本信息
    ----doubanbook_booktag.sql 图书标签信息
----image　抓取的图片
----web  抓取的图书列表页
  　----文学　　　 大分类
  　　　----茨威格  标签
              ----0.html  列表页
			  ----1.html
    ----文化
    ----生活
    ----流行
    ----经管
    ----book.html　　　测试的图书详情页
    ----books.html　　测试的图书列表页
    ----booktag.html　测试图书标签页
    ----booktag.xlsx　提取的图书标签页
	
----tool  抓取工具
----源码
----pack 打包的所有东西，安装上面目录解压
