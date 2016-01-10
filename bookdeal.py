# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
from tool.filetool import writeexcel
__author__ = 'hunterhug'
import json

def manybook(url_content):
	"""
	抓取图书信息元组

	"""
	books = []
	soup = BeautifulSoup(url_content, 'html.parser') # 开始解析

	booktable1 = soup.find_all("dl")  # 找到所有图书所在标记

	# 循环遍历图书列表
	for book in booktable1:
		simplebook = book

		subsoup = BeautifulSoup(str(simplebook), 'html.parser') # 单本书进行解析

		# 图书封面：
		# http://img4.doubanio.com/spic/s1237549.jpg
		# http://img4.doubanio.com/lpic/s1237549.jpg
		booksmallimg = subsoup.img['src']
		imgtemp = booksmallimg.split('/')
		imgtemp[len(imgtemp)-2] = 'lpic'
		booklargeimg = '/'.join(imgtemp)

		# 图书信息
		booklink = subsoup.dd.a['href']  # 图书链接：http://book.douban.com/subject/1084336/
		bookname1 = subsoup.dd.a.string # 图书名称：小王子
		bookinfo = subsoup.div.string # 图书出版信息：[法] 圣埃克苏佩里 / 马振聘 / 人民文学出版社 / 2003-8 / 22.00元
		try:
			bookstar = subsoup.find('span',attrs={"class": "rating_nums"}).string # 图书星级：9.0
		except:
			bookstar = ''
			pass
		bookinfo = bookinfo.strip(' \n')
		books.append([bookname1, booklink, booklargeimg, bookinfo, bookstar])
	# 返回图书列表
	return books


def onebook(url_content):
	"""
	抓取单本书

	"""
	soup = BeautifulSoup(url_content, 'html.parser') # 开始解析
	bookno=soup.find('meta',attrs={'http-equiv':'mobile-agent'})
	bookno=bookno['content'].split('subject/')[1].replace('/','')
	bookname=soup.find('h1').text.replace('\n','')
	#print(bookname)
	bookinfo = soup.find('div',attrs={"id": "info"}) # 出版信息
	bookp=soup.find('a',attrs={"class","rating_people"})
	books=soup.findAll('span',attrs={"class","rating_per"})
	bookintro = soup.findAll('div',attrs={"class": "intro"}) # 书籍及作者介绍
	bookalot = soup.findAll('div',attrs={"class": "subject_show block5"}) #众书信息 可能不存在
	bookamulu = soup.select('div[id*="dir"]')
	bookhotcomment1 = soup.select('div#wt_1 div.ctsh div.tlst div.ilst a')    # 评论头像
	bookhotcomment2 = soup.select('div#wt_1 div.ctsh div.tlst div.nlst h3 > a') # 评论详情
	bookhotcomment3 = soup.select('div#wt_1 div.ctsh div.tlst div.clst span.starb') # 用户简介
	try:
		bookinfo=bookinfo.text.replace(' \n','').replace('\n ','').replace(' ','')
	except:
		bookinfo='' 
	#print(bookinfo)
	try:
		bookintro1=bookintro[0].findAll('p')
	except:
		bookintro1=[]
	try:
		bookintro2=bookintro[1].findAll('p')
	except:
		bookintro2=[]
	tro1=''
	tro2=''
	for i in bookintro1:
		tro1=tro1+i.text+'\n'
	for i in bookintro2:
		tro2=tro2+i.text+'\n'
	#print(tro2)
	try:
		bookalot=bookalot[0].text.replace('\n','').replace(' ','')
	except:
		bookalot=''
	#print(bookalot)
	bookp=bookp.text
	try:
		bookamulu=bookamulu[0].text.replace(' ','')
		bookamulu=bookamulu[1].text.replace(' ','')
	except:
		bookamulu=''
	#print(bookhotcomment1[0])
	#print(bookhotcomment2[0])
	#print(bookhotcomment3[0])
	peoples = []
	for i in range(0,len(bookhotcomment1)):
		peoples.append('<br />'.join([str(bookhotcomment1[i]),str(bookhotcomment2[i]),str(bookhotcomment3[i]).replace('\xa0','')]))
	bookstar=[]
	for i in books:
		bookstar.append(i.text)
	peoples
	return  [bookno,bookname,bookinfo,tro1,tro2,int(bookp.replace('人评价','')),','.join(bookstar),bookalot,bookamulu,'<hr />'.join(peoples)]

def booktag(url_content, path = 'web/booktag.xlsx'):
	"""
	抓取标签提取 写入Excel

	"""
	soup = BeautifulSoup(url_content, 'html.parser') # 开始解析
	booktag1 = soup.select('div#content div.article div div')
	# print(booktag1[0])
	taglist = [['标签类别', '标签名', '链接']]
	for booktag2 in booktag1:
		soup1 = BeautifulSoup(str(booktag2), 'html.parser') # 开始解析
		booktag2 = soup1.find('a',attrs={'class':'tag-title-wrapper'})
		type = booktag2['name']  # 标签类别
		booktag3 = soup1.findAll('a',attrs={'class':'tag'})
		for i in booktag3:
			tag = i.string # 标签名
			taglink = i['href'] # 链接
			taglist.append([type, tag, taglink])
	print(taglist)
	writeexcel(path, taglist)
	print("写入EXCEL成功")


def testbooktag():
	file = open('web/booktag.html','rb')
	content = file.read()
	booktag(content)

def testmanybook():
	file = open('web/books.html','rb')
	content = file.read()
	books = manybook(content)
	for i in books:
		print(i)

def testonebook():
	file = open('web/book.html','rb')
	content = file.read()
	book = onebook(content)
	for i in book:
		print(i)
		print('*'*50)

if __name__=='__main__':
	# testmanybook()
	testonebook()
	#testbooktag()
