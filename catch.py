# -*- coding:utf-8 -*-
# http://book.douban.com/tag/
# http://www.douban.com/tag/小说/book?start=0 书列表 间隔15
# http://book.douban.com/subject/25862578/?from=tag_all 书信息
# http://book.douban.com/subject/6082808/reviews?score=&start=0 书评 间隔25
from tool.gethtml import getHtml,getBinaryHtml
import time
import os.path
from tool.filetool import listfiles,readexcel,writeexcel,validateTitle
import bookdeal
import urllib.error
import urllib.parse
import re
from tool.daili import daili
from tool.mysql import Mysql
from pymysql import escape_string
#web504=['1002582','1010668',,'10459781']#'
web504=['1010668','1023322','10459781','1915375']
# 抓取书表：第一步
def catchbooklist(requreip = 0, v=0, lockprefix= 'lock'):
	"""
	输入参数为:
	是否使用代理，默认否
	是否限制爬虫速度，默认否，时间为1秒仿人工
	文件加锁后缀
	"""
	# 进行计时
	start = time.clock()
	taglist = readexcel('web/booktag.xlsx') # 读取标签
	daili0 = daili()   # 代理IP数组
	changeip = 0  # 代理ip下标
	# 循环对标签进行抓取
	for i in range(1,len(taglist)):
		kinds = taglist[i][0] # 大分类
		tagname = taglist[i][1] # 标签名
		tag = urllib.parse.quote(tagname) # url中文转码
		mulu0 = 'web/'+kinds
		# 存在大分类文件夹则跳过
		if os.path.exists(mulu0):
			pass
		else: # 否则新建
			print('新建大分类：'+mulu0)
			os.makedirs(mulu0)

		mulu = mulu0+'/'+tagname
		# 存在标签文件夹则跳过
		if os.path.exists(mulu):
			pass
		else: # 否则新建方便网页存放
			print('新建标签文件夹'+mulu)
			os.makedirs(mulu)

		# 网络中断后重新抓取时判断是否加锁
		ok = listfiles(mulu, '.'+lockprefix)
		if ok:
			print('类别：'+kinds+'----标签：'+tagname+'----已经抓完') # 抓完
			continue
		url = 'http://www.douban.com/tag/'+tag+'/book?start=' 	# 基础网址
		pagesize = 15									# 每页15本
		i = 0   # 翻页助手
		while(True):
			# 需要爬取的网页
			site = url+str(i*pagesize)

			# 开始爬取
			# 构造文件名称
			# web/小说/0.html
			src = mulu+'/'+str(i*15)+'.html'

			# 判断文件是否存在，存在则不抓取节省时间
			if(os.path.exists(src) == True):
				pass
			else:
				# 写入本地文件
				print('准备抓取：'+site+'类别：'+kinds+'----标签：'+tagname)
				iprefuse = 1  # 如果抓取成功设为0
				# 如果抓取出错那重新抓取
				while iprefuse:
					try:
						daili1= daili0[changeip]  # 代理ip
						# 爬虫速度控制
						if v:
							a = time.clock()
							time.sleep(v)
							b = time.clock()
							print('时间暂停:'+str(b-a))
						# 不需要代理
						if requreip==0:
							webcontent = getHtml(site).encode('utf-8') # 爬取
							# print(webcontent.decode('utf-8','ignore'))
							notnull = re.search(r'<dl>',webcontent.decode('utf-8','ignore')) # 匹配看是否抓取到末页
							iprefuse = 0 # 抓完设置0
						else: # 需要代理
							print('代理：'+daili1)
							webcontent = getBinaryHtml(site, daili1)
							# print(webcontent.decode('utf-8','ignore'))
							notnull = re.search(r'<dl>',webcontent.decode('utf-8','ignore'))
							print(notnull)
							iprefuse = 0
					except Exception as e:
						print(e)
						if requreip:
							changeip = changeip+1 # 更换ip下标
							if changeip==len(daili0): # 到达ip数组末循环再来
								changeip = 0
							print('更换代理：'+daili0[changeip])
						else:
							print("IP被封")
							raise
							return
						# break

				# 如果抓不到<dl>标签，证明已经抓取完
				if notnull:
					webfile = open(src, 'wb')
					webfile.write(webcontent)
					webfile.close()
					print("已经抓取:"+site+'类别：'+kinds+'----标签：'+tagname)
				else:
					lock = open(src.replace('html',lockprefix),'w') # 加锁证明抓完
					# 日期：http://blog.csdn.net/caisini_vc/article/details/5619954
					finish = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
					lock.write('抓取完成时间：'+finish)
					print("抓取完毕："+tagname)
					break
			i =i + 1  # 加页
	# 计时
	end = time.clock()
	print("爬取总共运行时间 : %.03f 秒" %(end-start))

# 分析提取书表：第二步
def dealbooklist():
	start = time.clock()
	putplace = 'books'
	# 判断存放位置是否存在
	if os.path.exists(putplace):
		pass
	else: # 否则新建
		print('新建图书提取存放excel处：'+putplace)
		os.makedirs(putplace)
	taglist = readexcel('web/booktag.xlsx') # 读取标签列表
	del taglist[0]
	# 对于每个标签
	for tag in taglist:

		# 图书按照标签存放于文件夹中
		mulu=putplace+'/'+tag[0]
		if os.path.exists(mulu):
			pass
		else:
			os.makedirs(mulu)

		excelpath = mulu+'/'+tag[1]+'.xlsx'
		# 存在处理过的excel文件则跳过
		if os.path.exists(excelpath):
			print(excelpath+'已经存在')
			continue

		tagbooks = [] # 该标签所有书存放处
		path = 'web/'+tag[0]+'/'+tag[1] # 构造读取文件夹入口
		print('本地提取：'+path)
		# 查找目录下已经抓取的Html
		files = listfiles(path)
		# 遍历分析
		for i in files:
			file = path+'/'+i
			print('提取：'+file)
			content = open(file,'rb').read()
			book = bookdeal.manybook(content) # 提取图书列表
			for j in book: # 重新包装图书
				# print('提取：'+','.join(j))
				tagbooks.append(j)

		# 将信息写入本地文件中
		booksattr=['书籍名','URL入口','图片地址','出版信息','评价星数']
		tagbooks.insert(0,booksattr)
		writeexcel(excelpath,tagbooks)
		print('写入成功：'+excelpath)
	end = time.clock()
	print("提取图书列表总共运行时间 : %.03f 秒" %(end-start))

# 书表去重并写入数据库：第三步
# 读取Excel，判断是否重复，先加入book表，重复则往booktag表插入标签记录
def mergeboolist():
	start = time.clock()
	taglist = readexcel('web/booktag.xlsx') # 读取标签列表
	del taglist[0]
	database = Mysql(host="localhost", user="root", pwd="6833066", db="doubanbook")
	for tag in taglist: # 遍历所有标签
		kind = tag[0] # 大类
		tagname = tag[1] # 标签
		excelpath = 'books/'+kind+'/'+tagname+'.xlsx' # 本地文件
		try:
			datas = readexcel(excelpath)
		except Exception as e:
			print(e)
			continue
		del datas[0] # 去掉标题
		#print(datas)
		# 提取图书插入数据库
		for data in datas:
			bookname = data[0].replace("'","\\'").replace('"','\\"')
			bookurl = data[1].replace("'","\\'").replace('"','\\"')
			bookimage = data[2].replace("'","\\'").replace('"','\\"')
			bookno = bookurl.split('/')[-2].replace("'","\\'").replace('"','\\"')
			try:
				bookinfo = data[3].replace("'","\\'").replace('"','\\"')
			except:
				bookinfo = ''
				pass
			try:
				bookstar = data[4]
			except:
				bookstar = '0'
				pass
			# select * from `book` where `bookno`='dc'
			searchsql1 = "select * from `book` where `bookno`='"+bookno+"'"
			print(searchsql1)
			try:
				isexist1 = database.ExecQuery(searchsql1)
			except Exception as e:
				print(e)
				pass
			# 如果图书记录存在，插Booktag表
			if isexist1:
				print(bookname+':'+bookurl+'已经存在')

			else:
				insertbooksql = "INSERT INTO `book` (`bookname`, `bookurl`, `bookimg`, `bookinfo`, `bookstar`, `bookno`) VALUES ('" \
							"{bookname}', '{bookurl}', '{bookimg}', '{bookinfo}', '{bookstar}', '{bookno}')"
				insert1 = insertbooksql.format(bookname=bookname, bookurl=bookurl, bookimg=bookimage, bookinfo=bookinfo, bookstar=bookstar, bookno=bookno)
				print(insert1)
				try:
					database.ExecNonQuery(insert1)
				except Exception as e:
					print(e)
					pass
			# 如果图书标签存在，则不插入
			searchsql = "select * from `booktag` where `bookno`='{bookno}' and `booktag`='{booktag}' and `bookkind`='{bookkind}'"
			searchsql2 = searchsql.format(bookno=bookno,booktag=tagname,bookkind=kind)
			print(searchsql2)
			try:
				isexist2 = database.ExecQuery(searchsql2)
			except Exception as e:
				print(e)
				pass
			if isexist2.__len__()==0:
				inserttag = "INSERT INTO `booktag`(`bookname`,`bookno`,`booktag`,`bookkind`) VALUES ('" \
							"{bookname}', '{bookno}', '{booktag}', '{bookkind}')"
				insert2 = inserttag.format(bookname=bookname, bookno=bookno, booktag=tagname, bookkind=kind)
				print(insert2)
				try:
					database.ExecNonQuery(insert2)
				except Exception as e:
					print(e)
					pass
			print('-'*100)
	print("插入数据库结束")
	end = time.clock()
	print("合并图书列表进数据库总共运行时间 : %.03f 秒" %(end-start))


# 抓取图书：第四步
# 读取book表，读取booktag表，抓取图书网页拷贝多份到不同标签目录
def catchbook(requreip = 0, v=0,startbook=0):
	"""
	输入参数为:
	是否使用代理，默认否
	是否限制爬虫速度，默认否，时间为1秒仿人工
	startbook = 0 查询起始位置
	"""
	# 进行计时
	start = time.clock()
	webe=[]
	selecttotal = 'select count(distinct bookno) from booktag'
	selectsql = 'SELECT bookname,bookkind,bookno FROM booktag group by bookno'
	database = Mysql(host="localhost", user="root", pwd="6833066", db="doubanbook")
	total = database.ExecQuery(selecttotal) # 总记录
	total=int(total[0][0])
	daili0 = daili()   # 代理IP数组
	dailino = 0
	changeip = 0  # 代理ip下标
	# 循环对分类进行抓取
	while startbook < total+100:
		selectsql1=selectsql+' limit '+str(startbook)+',100'
		taglist=database.ExecQuery(selectsql1)
		for i in range(0,len(taglist)):
			try:
				bookname = taglist[i][0]
				kinds = taglist[i][1] # 分类
				bookno = taglist[i][2] # 图书编号
				url = 'http://book.douban.com/subject/'+bookno # 抓取网址
				#http://book.douban.com/subject/25862578
			except:
				raise
				return
			mulu0 = 'book/'+kinds
			# 存在大分类文件夹则跳过
			if os.path.exists(mulu0):
				pass
			else: # 否则新建
				print('新建大分类：'+mulu0)
				os.makedirs(mulu0)
			# 判断文件是否存在，存在则不抓取节省时间
			try:
				filename =mulu0+'/'+bookno+validateTitle(bookname)+'.html'
				if(os.path.exists(filename) == True):
					print(filename+'：已经存在')
					continue
				elif bookno in web504:
					# 写入本地文件
					print('----'*5)
					print("504错误,跳过："+bookno)
					print('----'*5)
					continue
				else:
					#print("-"*50)
					print('准备抓取：'+url+'类别：'+kinds)
			except:
				print(filename+"文件名异常")
				continue
			iprefuse = 1  # 如果抓取成功设为0
			# 如果抓取出错那重新抓取
			while iprefuse:
				try:
					daili1= daili0[changeip]  # 代理ip
					# 爬虫速度控制
					if v:
						a = time.clock()
						time.sleep(v)
						b = time.clock()
						print('时间暂停:'+str(b-a))
					# 不需要代理
					if requreip==0:
						webcontent = getHtml(url).encode('utf-8') # 爬取，有时间限制，应对504错误
						notnull = re.search(r'<div class="top-nav-doubanapp">',webcontent.decode('utf-8','ignore'))
						if notnull:
							pass
						else:
							raise Exception("抓到的页面不是正确的页面"+filename)
						webfile = open(filename, 'wb')
						webfile.write(webcontent)
						webfile.close()
						print("已经抓取:"+url+'类别：'+kinds)
						iprefuse = 0 # 抓完设置0
					else: # 需要代理
						print('代理：'+daili1)
						webcontent = getBinaryHtml(url, daili1)
						notnull = re.search(r'<div class="top-nav-doubanapp">',webcontent.decode('utf-8','ignore'))
						if notnull:
							pass
						else:
							raise Exception("抓到的页面不是正确的页面"+filename)
						webfile = open(filename, 'wb')
						webfile.write(webcontent)
						webfile.close()
						print("已经抓取:"+url+'类别：'+kinds)
						iprefuse = 0
						dailino=dailino+1
						print('此次转换代理次数:'+str(dailino))
						if dailino>20:
							dailino=0
							requreip=0 # 代理100次后转为非代理
				#except urllib.error.URLError as e:
				except Exception as e:
					print(url)
					if hasattr(e, 'code'):
						print('页面不存在或时间太长.')
						print('Error code:', e.code)
						if e.code==404:
							print('404错误，忽略')
							webe.append(bookno)
							break
					elif hasattr(e, 'reason'):
						print("无法到达主机.")
						print('Reason:  ', e.reason)
					print(e)
					if requreip:
						changeip = changeip+1 # 更换ip下标
						if changeip==len(daili0): # 到达ip数组末循环再来
							changeip = 0
						print('更换代理：'+daili0[changeip])
						dailino=dailino+1
						print('此次转换代理次数:'+str(dailino))
						if dailino>20:
							dailino=0
							requreip=0 # 代理100次后转为非代理
					else:
						print("IP被封或断网")
						requreip=1 # 转为代理
		print('已经抓了'+str(startbook+100)+'本')
		print()
		print()
		print()
		startbook=startbook+100
		if len(webe) > 20:
			print(webe)
			webep=open("book/book.txt",'a+')
			webep.write(','.join(webe)+'/n')
			webep.close()
			webe=[]
		else:
			pass
	# 计时
	end = time.clock()
	print("爬取总共运行时间 : %.03f 秒" %(end-start))



# 提取图书：第五步
# 扫描book目录，找出所有图书详情表进行提取，插入数据库
def dealbook():
	rootdir='book'
	prefix='.html'
	database = Mysql(host="localhost", user="root", pwd="6833066", db="doubanbook")
	insertbooksql = "INSERT INTO `bookdetial` (`bookname`,`bookno`,`bookinfo`,`bookintro`,`authorintro`,`peoples`,`starts`,`other`,`mulu`,`comments`) VALUES (" \
							"{0}, {1}, {2},{3},{4},{5},{6},{7},{8},{9})"
	for parent,dirnames,filenames in os.walk(rootdir):
		for filename in filenames:
			if filename.endswith(prefix) :
				path=str(parent)+'/'+filename
				print(path)
				content=open(path,'rb').read()
				try:
					draw=bookdeal.onebook(content)
				except:
					continue
				insert1 = insertbooksql.format(escape_string(draw[1]),draw[0],escape_string(draw[2]),escape_string(draw[3]),\
                                                               escape_string(draw[4]),draw[5],escape_string(draw[6]),escape_string(draw[7]),escape_string(draw[8]),escape_string(draw[9]))
				try:
					database.ExecNonQuery(insert1)
					os.rename(path,path+'lockl')
				except Exception as e:
					print(e)
					continue
			else:
				pass

if __name__=='__main__':
	#catchbooklist(0,2,'lock3')
	#dealbooklist()
	#mergeboolist()
	catchbook(0,3,18200)#1900
