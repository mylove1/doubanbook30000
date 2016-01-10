# -*- coding:utf-8 -*-
import pymysql

class Mysql:
	"""
	对pymysql的简单封装,实现基本的连接
	"""

	def __init__(self, host, user, pwd, db):
		self.host = host
		self.user = user
		self.pwd = pwd
		self.db = db
		self.cur=self.__GetConnect()

	def __GetConnect(self):
		"""
		得到连接信息
		返回: conn.cursor()
		"""
		if not self.db:
			raise (NameError, "没有设置数据库信息")
		self.conn = pymysql.connect(host=self.host, user=self.user, passwd=self.pwd, db=self.db, charset="utf8")
		cur = self.conn.cursor()
		if not cur:
			raise (NameError, "连接数据库失败")
		else:
			return cur

	def ExecQuery(self, sql):
		"""
		执行查询语句
		返回的是一个包含tuple的list，list的元素是记录行，tuple的元素是每行记录的字段

		调用示例：
				ms = MYSQL(host="localhost",user="sa",pwd="123456",db="PythonWeiboStatistics")
				resList = ms.ExecQuery("SELECT id,NickName FROM WeiBoUser")
				for (id,NickName) in resList:
					print str(id),NickName
		"""
		self.cur.execute(sql)
		#print("查询语句："+sql)
		resList = self.cur.fetchall()
		return resList

	def ExecNonQuery(self, sql):
		"""
		执行非查询语句

		调用示例：
			cur = self.__GetConnect()
			cur.execute(sql)
			self.conn.commit()
			self.conn.close()
		"""
		try:
			self.cur.execute(sql)
			self.conn.commit()
			print('执行语句成功')
		except Exception:  # 出现异常回滚
			self.conn.rollback()
			print('执行SQL语句失败：'+sql)
			raise


	def __del__(self):
		self.cur.close()

def init():
	return Mysql(host="localhost", user="root", pwd="6833066", db="doubanbook")

def testinsert():
	mysql1 = init()
	mysql1.ExecNonQuery("insert into `bookdetial` (booknafme) values ('你哈') ")

def testselect():
	mysql1 = init()
	print(mysql1.ExecQuery('SELECT bookname,bookkind,bookno FROM booktag group by bookno limit 0,5;')[0][0])
	print(mysql1.ExecQuery('SELECT bookname,bookkind,bookno FROM booktag group by bookno limit 5,5;'))
	print('-'*50)
	print(mysql1.ExecQuery('SELECT bookname,bookkind,bookno FROM booktag group by bookno limit 0,10;'))

def initdoubanbook():
	mysql = pymysql.connect(host="localhost", user="root", passwd="6833066", charset="utf8")
	cur = mysql.cursor()
	createsql = """
CREATE SCHEMA `doubanbook` ;
use `doubanbook`;
CREATE TABLE `book` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增ID',
  `bookname` varchar(100) NOT NULL COMMENT '书名',
  `bookurl` varchar(150) NOT NULL COMMENT '书入口',
  `bookimg` varchar(150) DEFAULT NULL COMMENT '书图片',
  `bookinfo` varchar(250) DEFAULT NULL COMMENT '书出版信息',
  `bookstar` varchar(45) DEFAULT NULL COMMENT '书评价星数',
  `bookno` varchar(45) NOT NULL COMMENT '书编号',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='书表';

CREATE TABLE `booktag` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `bookname` varchar(100) DEFAULT NULL COMMENT '书名',
  `bookno` varchar(45) DEFAULT NULL COMMENT '书编号',
  `booktag` varchar(45) DEFAULT NULL COMMENT '书标签',
  `bookkind` varchar(45) DEFAULT NULL COMMENT '书分类',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='书标签';"""
	try:
		cur.execute(createsql)
		mysql.commit()
		return createsql
	except:
		mysql.rollback()
		print("执行失败")

if __name__ == '__main__':
	# testinsert()
	testselect()


