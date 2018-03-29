#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib.request
import os
from pyquery import PyQuery as pq
from lxml import etree 
import multiprocessing

#  d = pq("http://www.meizitu.com/")
#  a = d('a')
#  geta = etree.HTML(str(a))
#  result = geta.xpath('//a/@href')
#  print(result)

class MeiZi:

    def __init__(self):
        self.mainurl = 'http://www.meizitu.com/a/more_%s.html'
        self.L = []
        self.L2 = []
        self.imgpages = []

    def getHtml(self, url):
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Accept':'text/html;q=0.9,*/*;q=0.8',
            'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding':'gzip',
            'Connection':'close',
            'Referer':'http://www.meizitu.com/' 
        }
        req = urllib.request.Request(url=url, headers=headers)
        res = urllib.request.urlopen(req)
        data = res.read()
        return data

    def queryHtml(self, url):
        return pq(str(self.getHtml(url)))

    def getA(self, url):
        return self.queryHtml(url)('a')

    def getData(self, url):
        data = self.getHtml(url)
        data = data.decode('gbk')
        html = pq(str(data))
        div_pic = html('div').attr('id','picture')('p')
        html2 = etree.HTML(str(div_pic))
        result = html2.xpath('//img/@alt')
        result = self.limitNum(result)
        img = html2.xpath('//img/@src')
        img = self.limitNum(img)
        imgdata = {}
        m = len(img) 
        for i in range(0, m):
            imgdata[result[i]]=img[i]
        return imgdata

    def limitNum(self, data):
        if len(data) > 10:
            data = data[:10]
        return data
    
    def handleA(self, url):
        html = etree.HTML(str(self.getA(url)))
        data = html.xpath('//a/@href')
        L = []
        for row in data:
            if 'www.meizitu.com/a/' in row:
                L.append(row)
        return L

    def getProcess(self, name, function, parameter):
        theprocess = multiprocessing.Process(name=name, target=function, args=(parameter,))
        theprocess.start()

    def dire(self, path):
        path = path.strip()
        isExists = os.path.exists(path)
        if not isExists:
            print('正在创建 ',path,' 文件夹')
            os.makedirs(path)
#          else:
#              print('名为',path,'的文件夹已经创建')

    def writeData(self, url):
        imgdata = self.getData(url)
        for row in imgdata: 
            # file = row[:-4]
            file = row.split('，')[0]
            self.dire(file)
            imgurl = imgdata[row]
            data = self.getHtml(imgurl)
            filename = row
            with open(file + '/' + filename + '.jpg', 'wb') as f:
                f.write(data)
                print('图片',filename,'已下载')

    # 执行url列表遍历获取图片
    def handleData(self, urls):
        for i in urls:
            urls = self.handleA(i)
            for url in urls:
                try:
                    self.writeData(url)
                except:
                    print('保存图片失败')

    # 第二步骤的页面，获取具体页面url
    def handleMainData(self, urls):
        n = 1
        for url in urls:
            theurls = self.handleA(url)
            for i in theurls:
                self.L2.append(i)
                n += 1
                if n%3 == 0:
                    self.getProcess('分离页面第三次分工'+str(n), self.handleData, self.L2)
                    print('分离页面第三次分工', self.L2)
                    self.L2 = []
            
    # 第一步骤的页面
    def Main(self):
        for i in range(1,65):
            url = self.mainurl%(str(i))
            self.L.append(url)
            if i%3 == 0:
                self.getProcess('分离页面'+str(i), self.handleMainData, self.L)
                print('开始分离页面',i, self.L)
                self.L = []

if __name__ == '__main__':
    mz = MeiZi()
    mz.Main()
