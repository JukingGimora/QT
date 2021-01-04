from stockList import stockList
from common import common
import constants
import os
from sql import sql

def updateStockList():
    s = stockList()
    s.method()

    filePath = sorted(os.listdir(constants.stockListPath), reverse=True)

    c = common()
    stockDict = c.readCSV(constants.stockListPath + filePath[0])

    insert = []
    update = []

    if len(filePath) == 1:
        for key in stockDict.keys():
            insert.append([key, stockDict[key]])
    else:
        stockDictOld = c.readCSV(constants.stockListPath + filePath[1])
        for key in stockDict.keys() - stockDictOld.keys():
            insert.append([key, stockDict[key]])

        #修改名称
        for key in stockDict.keys() & stockDictOld.keys():
            if stockDict[key] != stockDictOld[key]:
                update.append([stockDict[key], key])

    return insert, update

def saveStockList(insert, update):
    s = sql()

    insert_head_sql = constants.insert_head_sql
    s.operation(insert_head_sql, insert)

    update_head_sql = constants.update_head_sql
    s.operation(update_head_sql, update)


if '__name__==__main__':
    insert, update = updateStockList()
    print(insert)
    print(update)
    #涉及数据库插入，所以最好待数据获取稳定时取消注释
    # saveStockList(insert, update)