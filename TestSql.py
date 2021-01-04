import random
from matplotlib.font_manager import FontProperties
from sql import sql
import constants
from datetime import datetime, date, timedelta
import wave
from playsound import playsound
import numpy as np
import matplotlib.pyplot as plt
from lstm import lstm
from common import common
import csv


font = FontProperties(fname=r"/usr/share/fonts/opentype/noto/NotoSerifCJK-SemiBold.ttc")

def getTcloseInfo(code):
    select_tclose_sql = constants.select_tclose_sql%code
    s = sql()
    data = s.select(select_tclose_sql)

    return float(data[0][0])

def getInfo(front,rear):
    front = (date.today() + timedelta(days=front)).strftime("%Y%m%d")
    rear = (date.today() + timedelta(days=rear)).strftime("%Y%m%d")

    select_turnover_sql = constants.select_turnover_sql%(front,rear)
    s = sql()
    data = s.select(select_turnover_sql)

    ans = []
    for item in data:
        ans.append([item[0], float(item[1]), float(item[2])])

    return ans

def getInfomation(code):
    select_info_sql = constants.select_tclose_turnover_sql%code
    s = sql()
    data = s.select(select_info_sql)

    ans = []
    for item in data:
        ans.append([float(item[0]), float(item[1])])

    return ans

def getRangeInfo(front, rear):

    select_range_info_sql = constants.select_tclose_range_sql%(front,rear)
    s = sql()
    data = s.select(select_range_info_sql)

    ans = []
    for item in data:
        ans.append(item[0])
    return ans


if '__name__==__main__':
    data1 = getInfo(-35,-8)
    data2 = getInfo(-7,-1)

    for data in data1:
        if data[2] <=5 or data[2] >=10:
            data1.remove(data)

    for data in data2:
        if data[2] <=5 or data[2] >=10:
            data2.remove(data)

    ans = []
    for i in range(len(data1)):
        for j in range(len(data2)):
            if data1[i][0] == data2[j][0]:
                temp = [data1[i][0], i-j, data1[i][1]-data2[j][1]]
                ans.append(temp)
                break

    ans = sorted(ans, key=lambda x: x[2])

    candidate = []
    for i in range(len(ans)-1,-1,-1):
        if ans[i][0][0] == "3":
            continue
        elif ans[i][1] <= -100 or ans[i][1] >= 50:
            continue
        elif ans[i][2] <= 1:
            continue
        else:
            candidate.append(ans[i])

    for temp in candidate:
        price = getTcloseInfo(temp[0])
        if price >5 and price <10:
            print(temp)