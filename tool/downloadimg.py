# -*- coding:utf-8 -*-
import os, urllib.request

# 保存图书封面
# 根据文件名创建文件
def createFileWithFileName(localPathParam,fileName):
	totalPath=localPathParam+'/'+fileName+'.jpg'
	if not os.path.exists(totalPath):
		file=open(totalPath,'a+')
		file.close()
		return totalPath


# 根据图片的地址，下载图片并保存在本地
def getAndSaveImg(imgUrl, fileName, localPath='../image'):
	if(len(imgUrl)!= 0):
		urllib.request.urlretrieve(imgUrl,createFileWithFileName(localPath,fileName))