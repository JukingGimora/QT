import urllib.request
import os
import csv
import random
import constants
import threading
import time

class common:

    # 随机获取伪装头
    def getHeaders(self):
        user_agent_list = [
            'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1464.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.16 Safari/537.36',
            'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.3319.102 Safari/537.36',
            'Mozilla/5.0 (X11; CrOS i686 3912.101.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36',
            'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:17.0) Gecko/20100101 Firefox/17.0.6',
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36',
            'Mozilla/5.0 (X11; CrOS i686 3912.101.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36']

        UserAgent = random.choice(user_agent_list)

        return UserAgent

    # 获取网页源代码
    def getHtml(self, url):
        html = urllib.request.urlopen(url).read()
        html = html.decode('utf-8')
        return html

    # 加伪装头获取网页源码
    def fakerHead(self, url):
        header = self.getHeaders()
        args = {'User-Agent': header}
        req = urllib.request.Request(url, headers=args)
        response = urllib.request.urlopen(req)
        html = response.read()
        return html

    # 创建文件夹
    def mkdir(self, path):
        path = path.strip()
        path = path.rstrip("\\")
        isExists = os.path.exists(path)
        if not isExists:
            os.makedirs(path)
            return True
        else:
            print(path + ' 目录已存在')
            return False

    # 读取股票列表CSV文件
    def readCSV(self, fileName):

        dictionary = {}
        f = open(fileName, 'r', encoding='utf-8')
        f.seek(0)
        reader = csv.reader(f)

        cnt = 0
        for item in reader:
            if cnt == 0:
                cnt = cnt + 1
                continue
            dictionary[item[0]] = item[1]
        f.close()

        return dictionary

    # 读取个股代码
    def getStockList():
        stockListName = common.getCurrentTime()
        f = open(constants.stockListPath + stockListName, 'r', encoding='utf-8')
        f.seek(0)
        reader = csv.reader(f)

        stockList = []
        for item in reader:
            stockList.append(item[0])
        f.close()

        stockList.pop(0)
        return stockList

    #下载文件
    def downloadFile(self, url, filepath):
        try:
            urllib.request.urlretrieve(url, filepath)
        except Exception as e:
            print(e)
        print(filepath)
        pass

    #多线程下载
    def downloadFileSem(self, url, filepath):
        # 设置信号量，控制线程并发数
        sem = threading.Semaphore(150)
        with sem:
            self.downloadFile(url, filepath)

    #获得当前时间的股票列表文件名
    def getCurrentTime():
        #获取股票列表文件名主体
        stockListName = constants.stockListName
        currentTime = time.strftime("%Y%m%d", time.localtime(time.time()))
        stockListName = stockListName.replace('_', '_' + currentTime)

        return stockListName

