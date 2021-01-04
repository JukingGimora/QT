import random
from matplotlib.font_manager import FontProperties
from sql import sql
import constants
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

    ans = []
    for item in data:
        ans.append(float(item[0]))

    return ans

def getTurnoverInfo(code):
    select_turnover_sql = constants.select_turnover_sql%code
    s = sql()
    data = s.select(select_turnover_sql)

    ans = []
    for item in data:
        ans.append(float(item[0]))

    return ans

def getInfo(code):
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

def process2Audio(data):

    test = []
    for temp in data:
        tt = [temp for i in range(200)]
        test = test + tt

    test = np.array(data)

    test[:, 0] = 20 + (test[:, 0] - np.min(test[:, 0]))/(np.max(test[:, 0]) - np.min(test[:, 0]))*19080
    test[:, 1] = 20 + (test[:, 1] - np.min(test[:, 1]))/(np.max(test[:, 1]) - np.min(test[:, 1]))*19080

    wave_data = np.array(test)
    print(len(wave_data))
    wave_data = wave_data.astype(np.short)

    framerate = 44100
    # 打开WAV文档
    f = wave.open(r"file.wav", "wb")
    # 配置声道数、量化位数和取样频率
    f.setnchannels(2)
    f.setsampwidth(4)
    f.setframerate(framerate)
    # 将wav_data转换为二进制数据写入文件
    f.writeframes(wave_data.tostring())
    f.close()

    playsound('file.wav')

def process2Image(data):

    test = np.array(data)

    print(np.min(test[:, 0]), np.max(test[:, 0]))
    test[:, 0] = (test[:, 0] - np.min(test[:, 0]))/(np.max(test[:, 0]) - np.min(test[:, 0]))
    test[:, 1] = (test[:, 1] - np.min(test[:, 1]))/(np.max(test[:, 1]) - np.min(test[:, 1]))

    plt.scatter(test[:, 0], test[:, 1])
    plt.show()

def processByLSTM(data, scope_name, time_step, file_name):
    train_x, train_y, test_x = formData(data, time_step)
    l = lstm()
    if time_step != 160:
        l.train_lstm(train_x, train_y, scope_name, time_step, file_name)
    answer = l.prediction(train_x, scope_name, time_step, file_name)

    # error = computeError(answer, train_y)

    return answer

def normData(data):

    maxval = np.max(data)
    minval = np.min(data)

    ans = []
    for i in range(len(data)):
        ans.append([(data[i] - minval)/(maxval - minval)])
    return maxval, minval, ans

def formData(data, time_step):
    train_x, train_y = [], []
    for i in range(len(data) - time_step - 1):
        x = data[i: i + time_step]
        y = data[i+1: i + time_step + 1]
        train_x.append(x)
        train_y.append(y)

    test_x = []
    test_x.append(data[-1 * time_step::])

    return train_x, train_y, test_x

def computeError(pred, y):
    error = []
    for i in range(len(pred)):
        error.append(y[i] - pred[i])

    return error

def computerProduct(x, y):
    sum = 0
    for i in range(len(x)):
        sum = sum + x[i]*y[i]

    return sum

def coreOperation(ans):
    #创建模型文件夹
    modelPath = constants.modelPath
    c =common()
    c.mkdir(modelPath)

    ##############################################################
    #一层LSTM
    time_step1 = 15
    scope_name1 = modelPath + constants.scope_name + '_1'
    file_name1 = modelPath + constants.file_name.replace('.', '_1.')

    maxval1, minval1, train1 = normData(ans)
    data1 = processByLSTM(train1, scope_name1, time_step1, file_name1)

    #############################################################
    #二层LSTM
    time_step2 = 30
    scope_name2 = modelPath + constants.scope_name + '_2'
    file_name2 = modelPath + constants.file_name.replace('.', '_2.')

    res2 = np.array(data1)[:, -1, :]
    res2 = np.squeeze(res2)
    train2 = []

    for i in range(len(res2)):
        train2.append((res2[i] * (maxval1 - minval1) + minval1))

    maxval2, minval2, train2 = normData(train2)
    data2 = processByLSTM(train2, scope_name2, time_step2, file_name2)

    ######################################################
    #三层LSTM
    time_step3 = 90
    scope_name3 = modelPath + constants.scope_name + '_3'
    file_name3 = modelPath + constants.file_name.replace('.', '_3.')

    res3 = np.array(data2)[:, -1, :]
    res3 = np.squeeze(res3)
    train3 = []

    for i in range(len(res3)):
        train3.append(
                      (res3[i] * (maxval2 - minval2) + minval2))

    maxval3, minval3, train3 = normData(train3)
    data3 = processByLSTM(train3, scope_name3, time_step3, file_name3)

    ##################################################################
    #整合计算误差平方和
    res2 = res2[time_step2 + time_step3 + 2:]
    res2 = np.reshape(res2, (-1))
    res2 = res2 * (maxval1 - minval1) + minval1

    res3 = res3[time_step3 + 1:]
    res3 = np.reshape(res3, (-1))
    res3 = (res3 * (maxval2 - minval2) + minval2)

    pred = np.array(data3)[:, -1, :]
    pred = np.squeeze(pred)
    pred = pred * (maxval3 - minval3) + minval3

    plt.figure(1)
    plt.plot(ans[time_step1 + time_step2 + time_step3 + 3:],'r')
    plt.plot(res2, 'b')
    plt.figure(2)
    plt.plot(ans[time_step1 + time_step2 + time_step3 + 3:], 'r')
    plt.plot(res3, 'g')
    plt.figure(3)
    plt.plot(ans[time_step1 + time_step2 + time_step3 + 3:], 'r')
    plt.plot(pred, 'brown')
    plt.show()
    error1 = computeError(ans[time_step1 + time_step2 + time_step3 + 3:], res2)
    error2 = computeError(res2, res3)
    error3 = computeError(res3, pred)

    error1 = computerProduct(error1, error1)
    error2 = computerProduct(error2, error2)
    error3 = computerProduct(error3, error3)

    return error1, error2, error3

if '__name__==__main__':

    lst = getRangeInfo(5,10)
    idx = []

    for i in range(10):
        rand = random.randrange(len(lst))
        while rand in idx:
            rand = random.randrange(len(lst))
        idx.append(rand)

    f = open('test.csv','a+',encoding='utf-8')
    csv_writer = csv.writer(f)
    csv_writer.writerow(["所选股票代码", "一个LSTM的RSS", "两个LSTM的RSS","三个LSTM的RSS"])
    f.close()
    for index in idx:
        ans = getTcloseInfo(lst[index])
        error1, error2, error3 = coreOperation(ans)
        f = open('test.csv', 'a+', encoding='utf-8')
        csv_writer = csv.writer(f)
        csv_writer.writerow([lst[index], error1, error2, error3])
        f.close()
        break