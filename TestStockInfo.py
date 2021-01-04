from common import common
import constants
import csv
import os
import time
from stockInfo import stockInfo
from sql import sql

def init(start, step):
    stockList = common.getStockList()
    end = start + step
    if end >= len(stockList):
        end = len(stockList)
    companyList = stockList[start:end:]

    return companyList

def getRestStockList(currentTime):
    stockList = common.getStockList()
    # 获取当日股票信息文件夹里的csv
    root = constants.stockInfoPath + currentTime + '/'
    filePath = os.listdir(root)
    fileList = []
    for file in filePath:
        fileList.append(file.replace('.csv', ''))

    ans = []
    for stock in stockList:
        if stock not in fileList:
            ans.append(stock)

    return ans

def updateStockInfo(stockList):
    filePath = sorted(os.listdir(constants.stockListPath), reverse=True)
    startTime = ''
    currentTime = filePath[0].replace('stockList_', '').replace('.csv', '')
    if len(filePath) > 1:
        startTime = filePath[1].replace('stockList_', '').replace('.csv', '')

    s = stockInfo()
    s.method(stockList, startTime, currentTime)

def judgeOrSaveStockInfo(currentTime, flag):
    # 获取文件夹里的csv
    root = constants.stockInfoPath
    root = root + currentTime + '/'
    filePath = os.listdir(root)

    ans = []
    num = 0
    for file in filePath:
        #若是缓存垃圾文件则继续
        if '.csv' not in file:
            continue
        #获得股票代码
        code = file.replace('.csv','')
        #打开股票列表
        file = root + file
        f = open(file, 'rt', encoding='gbk')
        f.seek(0)
        record = csv.reader(f)

        items = []
        idx = 0
        for item in record:
            #跳过第一行
            if idx == 0:
                idx = 1
                continue
            #保存有错误数据的股票代码，方便重新获取
            if len(item) != 15:
               ans.append(code)
               break
            if flag == 1:
                #上市首日计算指标为None，方便插入库改为0.0（后期若用该指标得考虑上市首日特殊情况）
                for index, value in enumerate(item):
                    if 'None' in value:
                        item[index] = '0.0'
                #替换掉一些特殊字符
                item[0] = item[0].replace('-', '')
                item[1] = item[1].replace('\'', '')
                if 'e' in item[13]:
                    item[13] = str(float(item[13]))
                if 'e' in item[14]:
                    item[14] = str(float(item[14]))

                items.append(item)

        if flag == 1:
            s = sql()
            s.operation(constants.insert_limb_sql, items)
            num = num + 1
            print(num, code+'入库成功')

    return ans

if '__name__==__main__':
    currentTime = time.strftime("%Y%m%d", time.localtime(time.time()))
    #手动按步长获取上市公司每日股票信息
    # stockList = init(4000, 1000)
    # updateStockInfo(stockList)

    #获取遗漏的每日股票信息获取
    # stockList = getRestStockList(currentTime)
    # print(len(stockList), stockList)
    # updateStockInfo(stockList)

    #判断有无数据爬取错误并打印
    # ans = judgeOrSaveStockInfo(currentTime, 0)
    # print(ans)

    #无误后进行数据库更新
    # judgeOrSaveStockInfo(currentTime, 1)