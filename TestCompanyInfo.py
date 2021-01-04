from common import common
import constants
import numpy as np
from companyInfo import companyInfo
from sql import sql

def init(cnt):
    stockList = common.getStockList()
    companyList = stockList[cnt::]

    return companyList

def operateCompanyInfo(companyList, cnt):
    c = companyInfo()

    idx = cnt
    for company in companyList:
        infoList = c.method(company)

        s = sql()
        s.operate(constants.insert_body_sql, infoList)

        #打印下爬取的上市公司基本信息
        print(idx, infoList)
        idx = idx + 1

def updateCompanyInfo(companyList):
    c = companyInfo()

    idx = 0
    for company in companyList:
        infoList = c.method(company)

        #打印下爬取的上市公司基本信息
        # for i in range(len(infoList)):
        #     if infoList[i] == '%' or infoList[i] == '':
        #         infoList[i] = "None"

        print(idx, infoList)
        idx = idx + 1

    return infoList

def saveCompanyInfo(infoList):
    s = sql()
    s.operation(constants.insert_body_sql, infoList)

if '__name__==__main__':
    #首次手动按步长获取公司基本信息
    # cnt = 0
    # companyList = init(cnt)
    # operateCompanyInfo(companyList, cnt)

    #之后将TestStockList打印出的最新公司复制粘贴至此，再进行基本信息获取
    insert = [['003026', '中晶科技']]
    companyList = np.array(insert)[:, 0]
    infoList = updateCompanyInfo(companyList)

    #涉及数据库插入，最好待数据稳定后打开注释
    # saveCompanyInfo(infoList)