import re
import csv
from common import common
import constants
import os
import time


class stockList:

    def method(self):
        c = common()

        stockListPath = constants.stockListPath
        c.mkdir(stockListPath)
        stockListUrl = constants.stockListUrl
        html = c.getHtml(stockListUrl)
        dataList = []
        rest = re.findall('\[{.*}\]', html, flags=0)

        for res in rest:
            res = res.replace("\"", "").replace("f12:", "").replace("f14:", "").replace("[", ""). \
                replace("]", "").replace("{", "").replace("}", "").split(",")
            dataList = dataList + res

        c = common
        stockListName = c.getCurrentTime()
        f = open(stockListPath + stockListName, 'w+', encoding='utf-8', newline="")

        writer = csv.writer(f)
        stockListTitle = constants.stockListTitle
        writer.writerow(stockListTitle)

        for idx in range(0, len(dataList) - 1, 2):
            writer.writerow((dataList[idx], dataList[idx + 1]))

        f.close()
